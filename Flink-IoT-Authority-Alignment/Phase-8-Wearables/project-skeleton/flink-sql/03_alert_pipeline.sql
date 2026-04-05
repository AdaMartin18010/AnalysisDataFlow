-- ============================================================
-- 告警聚合与通知 Pipeline
-- Alert Aggregation and Notification Pipeline
-- ============================================================

SET 'pipeline.name' = 'Alert-Aggregation-Pipeline';
SET 'checkpointing.interval' = '10s';

-- ============================================================
-- 1. 告警Kafka源表
-- ============================================================

CREATE TABLE health_alert_source (
    patient_id STRING,
    device_id STRING,
    alert_type STRING,
    alert_level STRING,
    glucose_value INT,
    threshold_value INT,
    trend_arrow STRING,
    is_rapid_decline BOOLEAN,
    event_time TIMESTAMP(3),
    processing_time TIMESTAMP(3),
    WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'health-alerts',
    'properties.bootstrap.servers' = 'kafka:29092',
    'properties.group.id' = 'flink-alert-consumer',
    'format' = 'json',
    'scan.startup.mode' = 'latest-offset'
);

-- ============================================================
-- 2. 告警去重与抑制（5分钟内相同类型告警抑制）
-- ============================================================

CREATE VIEW deduplicated_alerts AS
SELECT 
    patient_id,
    device_id,
    alert_type,
    alert_level,
    glucose_value,
    threshold_value,
    trend_arrow,
    is_rapid_decline,
    event_time,
    processing_time,
    -- 使用Deduplicate去重
    ROW_NUMBER() OVER (
        PARTITION BY patient_id, alert_type 
        ORDER BY event_time DESC
    ) as rn
FROM health_alert_source;

CREATE VIEW unique_alerts AS
SELECT *
FROM deduplicated_alerts
WHERE rn = 1;

-- ============================================================
-- 3. 告警分级聚合（按患者+小时窗口）
-- ============================================================

CREATE VIEW hourly_alert_summary AS
SELECT 
    patient_id,
    TUMBLE_START(event_time, INTERVAL '1' HOUR) as window_start,
    TUMBLE_END(event_time, INTERVAL '1' HOUR) as window_end,
    COUNT(*) as total_alerts,
    COUNT(*) FILTER (WHERE alert_level LIKE 'CRITICAL%') as critical_count,
    COUNT(*) FILTER (WHERE alert_level LIKE 'WARNING%') as warning_count,
    ARRAY_AGG(DISTINCT alert_type) as alert_types,
    MAX(glucose_value) FILTER (WHERE alert_type = 'HIGH_GLUCOSE') as max_glucose,
    MIN(glucose_value) FILTER (WHERE alert_type = 'LOW_GLUCOSE') as min_glucose
FROM unique_alerts
GROUP BY 
    patient_id,
    TUMBLE(event_time, INTERVAL '1' HOUR)
HAVING COUNT(*) >= 3;

-- ============================================================
-- 4. 医生通知聚合视图
-- ============================================================

CREATE TABLE patients_dim (
    patient_id STRING,
    primary_physician_id STRING,
    emergency_contact_name STRING,
    emergency_contact_phone STRING,
    PRIMARY KEY (patient_id) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://timescaledb:5432/health_db',
    'table-name' = 'patients',
    'username' = 'health_user',
    'password' = 'health_pass',
    'lookup.cache.max-rows' = '10000'
);

CREATE VIEW physician_notifications AS
SELECT 
    p.primary_physician_id as doctor_id,
    h.patient_id,
    h.window_start,
    h.window_end,
    h.total_alerts,
    h.critical_count,
    h.alert_types,
    h.max_glucose,
    h.min_glucose,
    CASE 
        WHEN h.critical_count > 0 THEN 'URGENT'
        WHEN h.total_alerts >= 5 THEN 'HIGH'
        ELSE 'NORMAL'
    END as notification_priority
FROM hourly_alert_summary h
JOIN patients_dim FOR SYSTEM_TIME AS OF h.window_start AS p
    ON h.patient_id = p.patient_id
WHERE p.primary_physician_id IS NOT NULL;

-- ============================================================
-- 5. 医生通知输出
-- ============================================================

CREATE TABLE physician_notification_sink (
    doctor_id STRING,
    patient_id STRING,
    notification_priority STRING,
    total_alerts BIGINT,
    critical_count BIGINT,
    alert_types STRING,
    window_start TIMESTAMP(3),
    created_at TIMESTAMP(3)
) WITH (
    'connector' = 'kafka',
    'topic' = 'physician-notifications',
    'properties.bootstrap.servers' = 'kafka:29092',
    'format' = 'json'
);

INSERT INTO physician_notification_sink
SELECT 
    doctor_id,
    patient_id,
    notification_priority,
    total_alerts,
    critical_count,
    CAST(alert_types AS STRING),
    window_start,
    PROCTIME()
FROM physician_notifications;

-- ============================================================
-- 6. 紧急事件实时通知（旁路延迟约束）
-- ============================================================

CREATE VIEW emergency_alerts AS
SELECT 
    patient_id,
    device_id,
    alert_type,
    alert_level,
    glucose_value,
    event_time,
    PROCTIME() as notification_time,
    -- 紧急判定
    CASE 
        WHEN alert_type = 'LOW_GLUCOSE' AND alert_level = 'CRITICAL_LOW' THEN TRUE
        WHEN alert_type = 'HIGH_GLUCOSE' AND alert_level = 'CRITICAL_HIGH' THEN TRUE
        WHEN alert_type = 'ARRHYTHMIA_DETECTED' THEN TRUE
        WHEN alert_type = 'CRITICAL_TACHYCARDIA' THEN TRUE
        ELSE FALSE
    END as is_emergency
FROM unique_alerts
WHERE alert_level LIKE 'CRITICAL%' 
   OR alert_type = 'ARRHYTHMIA_DETECTED';

-- 紧急事件立即输出到优先级队列
CREATE TABLE emergency_alert_sink (
    patient_id STRING,
    device_id STRING,
    alert_type STRING,
    alert_level STRING,
    glucose_value INT,
    event_time TIMESTAMP(3),
    notification_time TIMESTAMP(3)
) WITH (
    'connector' = 'kafka',
    'topic' = 'emergency-alerts',
    'properties.bootstrap.servers' = 'kafka:29092',
    'format' = 'json'
);

INSERT INTO emergency_alert_sink
SELECT 
    patient_id,
    device_id,
    alert_type,
    alert_level,
    glucose_value,
    event_time,
    notification_time
FROM emergency_alerts
WHERE is_emergency = TRUE;

-- ============================================================
-- 7. 告警统计指标（用于监控）
-- ============================================================

CREATE VIEW alert_metrics AS
SELECT 
    TUMBLE_START(event_time, INTERVAL '1' MINUTE) as window_time,
    COUNT(*) as total_alerts,
    COUNT(DISTINCT patient_id) as affected_patients,
    COUNT(*) FILTER (WHERE alert_type = 'LOW_GLUCOSE') as low_glucose_count,
    COUNT(*) FILTER (WHERE alert_type = 'HIGH_GLUCOSE') as high_glucose_count,
    COUNT(*) FILTER (WHERE alert_type = 'ARRHYTHMIA_DETECTED') as arrhythmia_count,
    COUNT(*) FILTER (WHERE alert_level LIKE 'CRITICAL%') as critical_count,
    AVG(processing_time - event_time) as avg_processing_latency_ms
FROM health_alert_source
GROUP BY TUMBLE(event_time, INTERVAL '1' MINUTE);

-- 指标输出到Kafka用于Grafana
CREATE TABLE metrics_sink (
    metric_name STRING,
    metric_value BIGINT,
    labels STRING,
    timestamp TIMESTAMP(3)
) WITH (
    'connector' = 'kafka',
    'topic' = 'platform-metrics',
    'properties.bootstrap.servers' = 'kafka:29092',
    'format' = 'json'
);

INSERT INTO metrics_sink
SELECT 
    'total_alerts_per_minute',
    total_alerts,
    '{}',
    window_time
FROM alert_metrics;

INSERT INTO metrics_sink
SELECT 
    'critical_alerts_per_minute',
    critical_count,
    '{}',
    window_time
FROM alert_metrics;
