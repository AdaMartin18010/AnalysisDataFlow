-- ============================================================
-- 活动数据与睡眠监测 Pipeline
-- Activity and Sleep Monitoring Pipeline
-- ============================================================

SET 'pipeline.name' = 'Activity-Sleep-Processing-Pipeline';
SET 'checkpointing.interval' = '60s';

-- ============================================================
-- 1. 活动数据Kafka源表
-- ============================================================

CREATE TABLE activity_kafka_source (
    device_id STRING,
    patient_id STRING,
    steps INT,
    distance_meters INT,
    calories INT,
    active_minutes INT,
    floor_count INT,
    sleep_stage STRING,
    heart_rate_avg INT,
    timestamp TIMESTAMP(3),
    WATERMARK FOR timestamp AS timestamp - INTERVAL '1' MINUTE
) WITH (
    'connector' = 'kafka',
    'topic' = 'activity-raw-readings',
    'properties.bootstrap.servers' = 'kafka:29092',
    'properties.group.id' = 'flink-activity-consumer',
    'format' = 'json'
);

-- ============================================================
-- 2. 活动数据清洗
-- ============================================================

CREATE VIEW activity_cleaned AS
SELECT 
    device_id,
    patient_id,
    COALESCE(steps, 0) as steps,
    COALESCE(distance_meters, 0) as distance_meters,
    COALESCE(calories, 0) as calories,
    COALESCE(active_minutes, 0) as active_minutes,
    COALESCE(floor_count, 0) as floor_count,
    sleep_stage,
    heart_rate_avg,
    timestamp,
    -- 活动类型分类
    CASE 
        WHEN steps > 100 AND active_minutes > 0 THEN 'ACTIVE'
        WHEN sleep_stage IS NOT NULL THEN 'SLEEPING'
        ELSE 'SEDENTARY'
    END as activity_type
FROM activity_kafka_source
WHERE patient_id IS NOT NULL;

-- ============================================================
-- 3. 每日活动汇总
-- ============================================================

CREATE VIEW daily_activity_summary AS
SELECT 
    patient_id,
    device_id,
    TUMBLE_START(timestamp, INTERVAL '1' DAY) as date,
    SUM(steps) as total_steps,
    SUM(distance_meters) as total_distance,
    SUM(calories) as total_calories,
    SUM(active_minutes) as active_minutes,
    SUM(floor_count) as floors_climbed,
    -- 活动目标达成率（假设目标10000步）
    LEAST(SUM(steps) * 100.0 / 10000, 100) as step_goal_percent,
    -- 睡眠统计
    COUNT(*) FILTER (WHERE sleep_stage = 'deep') * 5 as deep_sleep_minutes,
    COUNT(*) FILTER (WHERE sleep_stage = 'rem') * 5 as rem_sleep_minutes,
    COUNT(*) FILTER (WHERE sleep_stage = 'light') * 5 as light_sleep_minutes,
    COUNT(*) FILTER (WHERE sleep_stage = 'awake') * 5 as awake_minutes
FROM activity_cleaned
GROUP BY 
    patient_id,
    device_id,
    TUMBLE(timestamp, INTERVAL '1' DAY);

-- ============================================================
-- 4. 活动数据写入数据库
-- ============================================================

CREATE TABLE daily_activity_sink (
    date TIMESTAMP(3),
    patient_id STRING,
    device_id STRING,
    total_steps BIGINT,
    total_distance BIGINT,
    total_calories BIGINT,
    active_minutes BIGINT,
    floors_climbed BIGINT,
    step_goal_percent DECIMAL(6,2),
    deep_sleep_minutes BIGINT,
    rem_sleep_minutes BIGINT,
    light_sleep_minutes BIGINT,
    awake_minutes BIGINT,
    PRIMARY KEY (patient_id, date, device_id) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://timescaledb:5432/health_db',
    'table-name' = 'daily_activity_summary',
    'username' = 'health_user',
    'password' = 'health_pass',
    'sink.buffer-flush.max-rows' = '100',
    'sink.buffer-flush.interval' = '30s'
);

INSERT INTO daily_activity_sink
SELECT * FROM daily_activity_summary;

-- ============================================================
-- 5. 实时活动指标（用于看板）
-- ============================================================

CREATE VIEW realtime_activity_metrics AS
SELECT 
    TUMBLE_START(timestamp, INTERVAL '5' MINUTE) as window_start,
    COUNT(DISTINCT patient_id) as active_users,
    SUM(steps) as total_steps,
    SUM(calories) as total_calories,
    AVG(heart_rate_avg) as avg_heart_rate,
    COUNT(*) FILTER (WHERE sleep_stage IS NOT NULL) as sleeping_users
FROM activity_cleaned
GROUP BY TUMBLE(timestamp, INTERVAL '5' MINUTE);

-- 输出到监控topic
CREATE TABLE activity_metrics_sink (
    metric_name STRING,
    metric_value BIGINT,
    window_start TIMESTAMP(3)
) WITH (
    'connector' = 'kafka',
    'topic' = 'platform-metrics',
    'properties.bootstrap.servers' = 'kafka:29092',
    'format' = 'json'
);

INSERT INTO activity_metrics_sink
SELECT 
    'active_users',
    active_users,
    window_start
FROM realtime_activity_metrics;

-- ============================================================
-- 6. 久坐提醒检测（连续2小时无活动）
-- ============================================================

CREATE VIEW sedentary_alert AS
SELECT *
FROM activity_cleaned
    MATCH_RECOGNIZE(
        PARTITION BY patient_id
        ORDER BY timestamp
        MEASURES
            FIRST(A.timestamp) as sedentary_start,
            LAST(A.timestamp) as alert_time,
            COUNT(*) as inactive_readings
        ONE ROW PER MATCH
        AFTER MATCH SKIP PAST LAST ROW
        PATTERN (A{24,})  -- 24个5分钟间隔 = 2小时
        DEFINE
            A AS A.steps = 0 AND A.sleep_stage IS NULL
    );

-- 久坐提醒输出
CREATE TABLE sedentary_alert_sink (
    patient_id STRING,
    device_id STRING,
    alert_type STRING,
    sedentary_duration_minutes BIGINT,
    alert_time TIMESTAMP(3)
) WITH (
    'connector' = 'kafka',
    'topic' = 'health-alerts',
    'properties.bootstrap.servers' = 'kafka:29092',
    'format' = 'json'
);

INSERT INTO sedentary_alert_sink
SELECT 
    patient_id,
    device_id,
    'SEDENTARY_REMINDER',
    120,  -- 2小时
    alert_time
FROM sedentary_alert;

-- ============================================================
-- 7. 睡眠质量评分
-- ============================================================

CREATE VIEW sleep_quality_score AS
SELECT 
    patient_id,
    device_id,
    TUMBLE_START(timestamp, INTERVAL '1' DAY) as sleep_date,
    SUM(CASE 
        WHEN sleep_stage = 'deep' THEN 5 * 3  -- 深度睡眠权重3
        WHEN sleep_stage = 'rem' THEN 5 * 2   -- REM睡眠权重2
        WHEN sleep_stage = 'light' THEN 5 * 1 -- 浅睡眠权重1
        ELSE 0
    END) as sleep_quality_score,
    COUNT(*) FILTER (WHERE sleep_stage IS NOT NULL) * 5 as total_sleep_minutes
FROM activity_cleaned
WHERE sleep_stage IS NOT NULL
GROUP BY 
    patient_id,
    device_id,
    TUMBLE(timestamp, INTERVAL '1' DAY)
HAVING COUNT(*) FILTER (WHERE sleep_stage IS NOT NULL) > 0;
