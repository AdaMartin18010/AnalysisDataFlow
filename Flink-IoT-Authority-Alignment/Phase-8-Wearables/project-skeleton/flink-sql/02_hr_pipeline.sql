-- ============================================================
-- 心率(HR)和心率变异性(HRV)数据处理 Pipeline
-- Heart Rate and Heart Rate Variability Processing
-- ============================================================

SET 'pipeline.name' = 'HR-HRV-Processing-Pipeline';
SET 'checkpointing.interval' = '30s';

-- ============================================================
-- 1. 心率Kafka源表
-- ============================================================

CREATE TABLE hr_kafka_source (
    device_id STRING,
    patient_id STRING,
    heart_rate INT,
    rr_interval_ms INT,
    confidence DECIMAL(3,2),
    timestamp TIMESTAMP(3),
    motion_flag BOOLEAN,
    WATERMARK FOR timestamp AS timestamp - INTERVAL '10' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'hr-raw-readings',
    'properties.bootstrap.servers' = 'kafka:29092',
    'properties.group.id' = 'flink-hr-consumer-v1',
    'format' = 'json',
    'json.ignore-parse-errors' = 'true'
);

-- ============================================================
-- 2. 心率数据清洗
-- ============================================================

CREATE VIEW hr_cleaned AS
SELECT 
    device_id,
    patient_id,
    heart_rate,
    rr_interval_ms,
    confidence,
    timestamp,
    motion_flag,
    -- 心率有效性检查
    CASE 
        WHEN heart_rate BETWEEN 30 AND 220 THEN 'VALID'
        ELSE 'INVALID'
    END as hr_validity,
    -- 运动伪影标记
    CASE 
        WHEN motion_flag = TRUE AND confidence < 0.7 THEN 'ARTIFACT'
        ELSE 'CLEAN'
    END as artifact_flag
FROM hr_kafka_source
WHERE heart_rate IS NOT NULL
  AND patient_id IS NOT NULL;

-- ============================================================
-- 3. 心率阈值维表
-- ============================================================

CREATE TABLE hr_thresholds_dim (
    patient_id STRING,
    hr_resting_low INT,
    hr_resting_high INT,
    hr_max INT,
    PRIMARY KEY (patient_id) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://timescaledb:5432/health_db',
    'table-name' = 'patient_thresholds',
    'username' = 'health_user',
    'password' = 'health_pass',
    'lookup.cache.max-rows' = '10000',
    'lookup.cache.ttl' = '10min'
);

-- ============================================================
-- 4. 心动过速/心动过缓检测
-- ============================================================

CREATE VIEW hr_abnormal_alerts AS
SELECT 
    h.patient_id,
    h.device_id,
    h.timestamp,
    h.heart_rate,
    h.rr_interval_ms,
    t.hr_resting_low,
    t.hr_resting_high,
    t.hr_max,
    CASE 
        WHEN h.heart_rate > t.hr_max THEN 'CRITICAL_TACHYCARDIA'
        WHEN h.heart_rate > t.hr_resting_high THEN 'TACHYCARDIA'
        WHEN h.heart_rate < t.hr_resting_low THEN 'BRADYCARDIA'
        ELSE 'NORMAL'
    END as hr_alert_type
FROM hr_cleaned h
JOIN hr_thresholds_dim FOR SYSTEM_TIME AS OF h.timestamp AS t
    ON h.patient_id = t.patient_id
WHERE h.artifact_flag = 'CLEAN'
  AND (h.heart_rate > t.hr_resting_high OR h.heart_rate < t.hr_resting_low);

-- ============================================================
-- 5. 心率告警输出
-- ============================================================

CREATE TABLE hr_alert_sink (
    patient_id STRING,
    device_id STRING,
    alert_type STRING,
    heart_rate INT,
    threshold_low INT,
    threshold_high INT,
    event_time TIMESTAMP(3)
) WITH (
    'connector' = 'kafka',
    'topic' = 'health-alerts',
    'properties.bootstrap.servers' = 'kafka:29092',
    'format' = 'json'
);

INSERT INTO hr_alert_sink
SELECT 
    patient_id,
    device_id,
    hr_alert_type,
    heart_rate,
    hr_resting_low,
    hr_resting_high,
    timestamp
FROM hr_abnormal_alerts;

-- ============================================================
-- 6. 房颤检测（基于RR间期不规则性）
-- ============================================================

CREATE VIEW afib_detection AS
SELECT 
    patient_id,
    device_id,
    window_start,
    window_end,
    avg_hr,
    rr_variability,
    irregular_ratio,
    CASE 
        WHEN irregular_ratio > 0.7 AND rr_variability > 100 THEN 'AFIB_SUSPECTED'
        WHEN irregular_ratio > 0.5 AND rr_variability > 80 THEN 'IRREGULAR_RHYTHM'
        ELSE 'NORMAL'
    END as rhythm_status
FROM (
    SELECT 
        patient_id,
        device_id,
        TUMBLE_START(timestamp, INTERVAL '1' MINUTE) as window_start,
        TUMBLE_END(timestamp, INTERVAL '1' MINUTE) as window_end,
        AVG(heart_rate) as avg_hr,
        STDDEV(rr_interval_ms) as rr_variability,
        AVG(CASE WHEN ABS(rr_interval_ms - LAG(rr_interval_ms) OVER (PARTITION BY patient_id ORDER BY timestamp)) > 50 THEN 1.0 ELSE 0.0 END) as irregular_ratio
    FROM hr_cleaned
    WHERE artifact_flag = 'CLEAN'
      AND heart_rate BETWEEN 40 AND 150
    GROUP BY 
        patient_id,
        device_id,
        TUMBLE(timestamp, INTERVAL '1' MINUTE)
    HAVING COUNT(*) >= 10
);

-- 房颤告警输出
CREATE TABLE afib_alert_sink (
    patient_id STRING,
    device_id STRING,
    alert_type STRING,
    rhythm_status STRING,
    avg_hr DECIMAL(6,2),
    rr_variability DECIMAL(10,2),
    irregular_ratio DECIMAL(4,3),
    window_start TIMESTAMP(3),
    window_end TIMESTAMP(3)
) WITH (
    'connector' = 'kafka',
    'topic' = 'health-alerts',
    'properties.bootstrap.servers' = 'kafka:29092',
    'format' = 'json'
);

INSERT INTO afib_alert_sink
SELECT 
    patient_id,
    device_id,
    'ARRHYTHMIA_DETECTED',
    rhythm_status,
    avg_hr,
    rr_variability,
    irregular_ratio,
    window_start,
    window_end
FROM afib_detection
WHERE rhythm_status IN ('AFIB_SUSPECTED', 'IRREGULAR_RHYTHM');

-- ============================================================
-- 7. 心率变异性(HRV)指标计算
-- ============================================================

CREATE VIEW hourly_hrv_metrics AS
SELECT 
    patient_id,
    device_id,
    TUMBLE_START(timestamp, INTERVAL '1' HOUR) as hour_start,
    AVG(heart_rate) as mean_hr,
    STDDEV(rr_interval_ms) as sdnn,
    MIN(rr_interval_ms) as min_rr,
    MAX(rr_interval_ms) as max_rr,
    COUNT(*) as valid_beats,
    -- HRV状态评估
    CASE 
        WHEN STDDEV(rr_interval_ms) < 20 THEN 'VERY_LOW'
        WHEN STDDEV(rr_interval_ms) < 50 THEN 'LOW'
        WHEN STDDEV(rr_interval_ms) > 100 THEN 'HIGH'
        ELSE 'NORMAL'
    END as hrv_status
FROM hr_cleaned
WHERE artifact_flag = 'CLEAN'
GROUP BY 
    patient_id,
    device_id,
    TUMBLE(timestamp, INTERVAL '1' HOUR)
HAVING COUNT(*) >= 30;

-- ============================================================
-- 8. HRV指标写入数据库
-- ============================================================

CREATE TABLE hrv_metrics_sink (
    hour_start TIMESTAMP(3),
    patient_id STRING,
    device_id STRING,
    mean_hr DECIMAL(6,2),
    sdnn DECIMAL(10,2),
    min_rr INT,
    max_rr INT,
    valid_beats BIGINT,
    hrv_status STRING
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://timescaledb:5432/health_db',
    'table-name' = 'hrv_hourly_metrics',
    'username' = 'health_user',
    'password' = 'health_pass',
    'sink.buffer-flush.max-rows' = '100',
    'sink.buffer-flush.interval' = '10s'
);

INSERT INTO hrv_metrics_sink
SELECT * FROM hourly_hrv_metrics;

-- ============================================================
-- 9. 原始心率数据写入数据库
-- ============================================================

CREATE TABLE hr_timescale_sink (
    time TIMESTAMP(3),
    device_id STRING,
    patient_id STRING,
    heart_rate INT,
    rr_interval_ms INT,
    confidence DECIMAL(3,2),
    motion_flag BOOLEAN,
    artifact_flag STRING
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://timescaledb:5432/health_db',
    'table-name' = 'heart_rate_readings',
    'username' = 'health_user',
    'password' = 'health_pass',
    'sink.buffer-flush.max-rows' = '1000',
    'sink.buffer-flush.interval' = '5s'
);

INSERT INTO hr_timescale_sink
SELECT 
    timestamp,
    device_id,
    patient_id,
    heart_rate,
    rr_interval_ms,
    confidence,
    motion_flag,
    artifact_flag
FROM hr_cleaned;
