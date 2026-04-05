-- ============================================================
-- CGM (Continuous Glucose Monitoring) 数据处理 Pipeline
-- 连续血糖监测数据处理
-- ============================================================

-- 设置执行参数
SET 'pipeline.name' = 'CGM-Processing-Pipeline';
SET 'checkpointing.interval' = '30s';
SET 'checkpointing.timeout' = '10min';
SET 'state.backend' = 'rocksdb';
SET 'table.exec.state.ttl' = '24h';
SET 'table.exec.mini-batch.enabled' = 'true';
SET 'table.exec.mini-batch.allow-latency' = '5s';
SET 'table.exec.mini-batch.size' = '1000';

-- ============================================================
-- 1. 数据源定义
-- ============================================================

-- CGM Kafka源表
CREATE TABLE cgm_kafka_source (
    device_id STRING,
    transmitter_id STRING,
    patient_id STRING,
    glucose_mg_dl INT,
    trend_arrow STRING,
    reading_time TIMESTAMP(3),
    sensor_id STRING,
    raw_voltage DECIMAL(10, 6),
    -- 水印：允许30秒乱序
    WATERMARK FOR reading_time AS reading_time - INTERVAL '30' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'cgm-raw-readings',
    'properties.bootstrap.servers' = 'kafka:29092',
    'properties.group.id' = 'flink-cgm-consumer-v1',
    'scan.startup.mode' = 'latest-offset',
    'format' = 'json',
    'json.ignore-parse-errors' = 'true',
    'json.fail-on-missing-field' = 'false'
);

-- ============================================================
-- 2. 数据清洗与验证
-- ============================================================

CREATE VIEW cgm_cleaned AS
SELECT 
    device_id,
    transmitter_id,
    patient_id,
    glucose_mg_dl,
    trend_arrow,
    reading_time,
    sensor_id,
    -- 数据质量标记
    CASE 
        WHEN glucose_mg_dl BETWEEN 40 AND 400 THEN 'VALID'
        WHEN glucose_mg_dl IS NULL THEN 'MISSING'
        ELSE 'OUT_OF_RANGE'
    END as data_quality,
    -- 置信度计算
    CASE 
        WHEN glucose_mg_dl BETWEEN 40 AND 400 THEN 0.95
        ELSE 0.5
    END as confidence_score
FROM cgm_kafka_source
WHERE patient_id IS NOT NULL
  AND device_id IS NOT NULL
  AND reading_time IS NOT NULL;

-- ============================================================
-- 3. 患者阈值维表（JDBC Lookup）
-- ============================================================

CREATE TABLE patient_thresholds_dim (
    patient_id STRING,
    glucose_low INT,
    glucose_critical_low INT,
    glucose_high INT,
    glucose_critical_high INT,
    PRIMARY KEY (patient_id) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://timescaledb:5432/health_db',
    'table-name' = 'patient_thresholds',
    'username' = 'health_user',
    'password' = 'health_pass',
    'lookup.cache.max-rows' = '10000',
    'lookup.cache.ttl' = '10min',
    'lookup.max-retries' = '3'
);

-- ============================================================
-- 4. 低血糖实时检测
-- ============================================================

CREATE VIEW low_glucose_alerts AS
SELECT 
    c.device_id,
    c.patient_id,
    c.glucose_mg_dl,
    c.reading_time,
    c.trend_arrow,
    t.glucose_low,
    t.glucose_critical_low,
    CASE 
        WHEN c.glucose_mg_dl < t.glucose_critical_low THEN 'CRITICAL_LOW'
        WHEN c.glucose_mg_dl < t.glucose_low THEN 'WARNING_LOW'
        ELSE 'NORMAL'
    END as alert_level,
    CASE 
        WHEN c.trend_arrow IN ('↓↓', '↓') AND c.glucose_mg_dl < 80 THEN TRUE
        ELSE FALSE
    END as is_rapid_decline
FROM cgm_cleaned c
JOIN patient_thresholds_dim FOR SYSTEM_TIME AS OF c.reading_time AS t
    ON c.patient_id = t.patient_id
WHERE c.data_quality = 'VALID'
  AND (c.glucose_mg_dl < t.glucose_low
   OR (c.trend_arrow IN ('↓↓', '↓') AND c.glucose_mg_dl < 80));

-- ============================================================
-- 5. 高血糖实时检测
-- ============================================================

CREATE VIEW high_glucose_alerts AS
SELECT 
    c.device_id,
    c.patient_id,
    c.glucose_mg_dl,
    c.reading_time,
    c.trend_arrow,
    t.glucose_high,
    t.glucose_critical_high,
    CASE 
        WHEN c.glucose_mg_dl > t.glucose_critical_high THEN 'CRITICAL_HIGH'
        WHEN c.glucose_mg_dl > t.glucose_high THEN 'WARNING_HIGH'
        ELSE 'NORMAL'
    END as alert_level
FROM cgm_cleaned c
JOIN patient_thresholds_dim FOR SYSTEM_TIME AS OF c.reading_time AS t
    ON c.patient_id = t.patient_id
WHERE c.data_quality = 'VALID'
  AND c.glucose_mg_dl > t.glucose_high;

-- ============================================================
-- 6. 告警输出到Kafka
-- ============================================================

CREATE TABLE glucose_alert_sink (
    patient_id STRING,
    device_id STRING,
    alert_type STRING,
    alert_level STRING,
    glucose_value INT,
    threshold_value INT,
    trend_arrow STRING,
    is_rapid_decline BOOLEAN,
    event_time TIMESTAMP(3),
    processing_time TIMESTAMP(3)
) WITH (
    'connector' = 'kafka',
    'topic' = 'health-alerts',
    'properties.bootstrap.servers' = 'kafka:29092',
    'format' = 'json',
    'sink.partitioner' = 'round-robin'
);

-- 低血糖告警输出
INSERT INTO glucose_alert_sink
SELECT 
    patient_id,
    device_id,
    'LOW_GLUCOSE',
    alert_level,
    glucose_mg_dl,
    CASE alert_level 
        WHEN 'CRITICAL_LOW' THEN glucose_critical_low 
        ELSE glucose_low 
    END,
    trend_arrow,
    is_rapid_decline,
    reading_time,
    PROCTIME()
FROM low_glucose_alerts;

-- 高血糖告警输出
INSERT INTO glucose_alert_sink
SELECT 
    patient_id,
    device_id,
    'HIGH_GLUCOSE',
    alert_level,
    glucose_mg_dl,
    CASE alert_level 
        WHEN 'CRITICAL_HIGH' THEN glucose_critical_high 
        ELSE glucose_high 
    END,
    trend_arrow,
    FALSE,
    reading_time,
    PROCTIME()
FROM high_glucose_alerts;

-- ============================================================
-- 7. 每日血糖统计（TIR/TBR/TAR）
-- ============================================================

CREATE VIEW daily_glucose_metrics AS
SELECT 
    patient_id,
    TUMBLE_START(reading_time, INTERVAL '1' DAY) as date,
    COUNT(*) as total_readings,
    AVG(glucose_mg_dl) as mean_glucose,
    STDDEV(glucose_mg_dl) as glucose_sd,
    MIN(glucose_mg_dl) as min_glucose,
    MAX(glucose_mg_dl) as max_glucose,
    -- Time in Range (70-180 mg/dL)
    COUNT(*) FILTER (WHERE glucose_mg_dl BETWEEN 70 AND 180) as tir_count,
    ROUND(COUNT(*) FILTER (WHERE glucose_mg_dl BETWEEN 70 AND 180) * 100.0 / COUNT(*), 2) as tir_percent,
    -- Time Below Range (<70 mg/dL)
    COUNT(*) FILTER (WHERE glucose_mg_dl < 70) as tbr_count,
    ROUND(COUNT(*) FILTER (WHERE glucose_mg_dl < 70) * 100.0 / COUNT(*), 2) as tbr_percent,
    -- Time Above Range (>180 mg/dL)
    COUNT(*) FILTER (WHERE glucose_mg_dl > 180) as tar_count,
    ROUND(COUNT(*) FILTER (WHERE glucose_mg_dl > 180) * 100.0 / COUNT(*), 2) as tar_percent,
    -- 严重事件计数
    COUNT(*) FILTER (WHERE glucose_mg_dl < 54) as severe_hypo_count,
    COUNT(*) FILTER (WHERE glucose_mg_dl > 250) as severe_hyper_count,
    -- 血糖管理指标(GMI)估算：GMI = 3.31 + 0.02392 × 平均血糖
    ROUND(3.31 + 0.02392 * AVG(glucose_mg_dl), 2) as estimated_gmi
FROM cgm_cleaned
WHERE data_quality = 'VALID'
GROUP BY 
    patient_id,
    TUMBLE(reading_time, INTERVAL '1' DAY);

-- ============================================================
-- 8. 每日统计输出到数据库
-- ============================================================

CREATE TABLE daily_glucose_sink (
    patient_id STRING,
    date TIMESTAMP(3),
    total_readings BIGINT,
    mean_glucose DECIMAL(6,2),
    tir_percent DECIMAL(5,2),
    tbr_percent DECIMAL(5,2),
    tar_percent DECIMAL(5,2),
    severe_hypo_count BIGINT,
    severe_hyper_count BIGINT,
    estimated_gmi DECIMAL(4,2),
    PRIMARY KEY (patient_id, date) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://timescaledb:5432/health_db',
    'table-name' = 'daily_glucose_summary',
    'username' = 'health_user',
    'password' = 'health_pass',
    'sink.buffer-flush.max-rows' = '100',
    'sink.buffer-flush.interval' = '5s',
    'sink.max-retries' = '3'
);

INSERT INTO daily_glucose_sink
SELECT 
    patient_id,
    date,
    total_readings,
    mean_glucose,
    tir_percent,
    tbr_percent,
    tar_percent,
    severe_hypo_count,
    severe_hyper_count,
    estimated_gmi
FROM daily_glucose_metrics;

-- ============================================================
-- 9. 原始数据写入TimescaleDB
-- ============================================================

CREATE TABLE cgm_timescale_sink (
    time TIMESTAMP(3),
    device_id STRING,
    patient_id STRING,
    glucose_mg_dl INT,
    trend_arrow INT,
    data_quality STRING,
    confidence_score DECIMAL(3,2)
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://timescaledb:5432/health_db',
    'table-name' = 'cgm_readings',
    'username' = 'health_user',
    'password' = 'health_pass',
    'sink.buffer-flush.max-rows' = '1000',
    'sink.buffer-flush.interval' = '5s',
    'sink.max-retries' = '3'
);

INSERT INTO cgm_timescale_sink
SELECT 
    reading_time,
    device_id,
    patient_id,
    glucose_mg_dl,
    CASE trend_arrow 
        WHEN '↓↓' THEN -2 
        WHEN '↓' THEN -1 
        WHEN '→' THEN 0 
        WHEN '↑' THEN 1 
        WHEN '↑↑' THEN 2 
        ELSE 0
    END,
    data_quality,
    confidence_score
FROM cgm_cleaned;

-- ============================================================
-- 10. CEP复合事件检测：持续下降趋势+阈值突破
-- ============================================================

CREATE VIEW cep_hypoglycemia AS
SELECT *
FROM cgm_cleaned
    MATCH_RECOGNIZE(
        PARTITION BY patient_id
        ORDER BY reading_time
        MEASURES
            FIRST(A.reading_time) as trend_start_time,
            LAST(C.reading_time) as alert_time,
            FIRST(A.glucose_mg_dl) as start_glucose,
            AVG(B.glucose_mg_dl) as avg_decline_glucose,
            LAST(C.glucose_mg_dl) as current_glucose,
            COUNT(*) as readings_count,
            LAST(C.trend_arrow) as final_trend
        ONE ROW PER MATCH
        AFTER MATCH SKIP PAST LAST ROW
        PATTERN (A B{2,} C)
        DEFINE
            A AS A.glucose_mg_dl >= 80 AND A.trend_arrow IN ('↓', '↓↓'),
            B AS B.glucose_mg_dl < PREV(B.glucose_mg_dl) AND B.glucose_mg_dl >= 70,
            C AS C.glucose_mg_dl < 70
    );

-- CEP告警输出
CREATE TABLE cep_alert_sink (
    patient_id STRING,
    alert_type STRING,
    severity STRING,
    start_glucose INT,
    current_glucose INT,
    trend_start_time TIMESTAMP(3),
    alert_time TIMESTAMP(3),
    readings_count BIGINT
) WITH (
    'connector' = 'kafka',
    'topic' = 'cep-alerts',
    'properties.bootstrap.servers' = 'kafka:29092',
    'format' = 'json'
);

INSERT INTO cep_alert_sink
SELECT 
    patient_id,
    'PATTERN_HYPOGLYCEMIA',
    'HIGH',
    start_glucose,
    current_glucose,
    trend_start_time,
    alert_time,
    readings_count
FROM cep_hypoglycemia;
