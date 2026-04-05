-- ============================================================================
-- Flink IoT SQL - 01. 创建表结构
-- 文档编号: F-SCHEMA-01
-- 形式化等级: L4
-- 创建时间: 2026-04-05
-- 
-- 依赖: Kafka, InfluxDB, EMQX 已启动
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. 原始传感器数据表 - Kafka Source
-- 存储从IoT设备接收的原始传感器读数
-- ----------------------------------------------------------------------------
CREATE TABLE sensor_readings (
    -- 主键与时间戳
    reading_id STRING,
    event_time TIMESTAMP(3),
    
    -- 设备标识
    device_id STRING,
    device_type STRING,
    location STRING,
    
    -- 传感器读数
    temperature DOUBLE,
    pressure DOUBLE,
    humidity DOUBLE,
    voltage DOUBLE,
    
    -- 元数据
    sensor_version STRING,
    firmware_version STRING,
    
    -- 水印策略 (30秒延迟)
    WATERMARK FOR event_time AS event_time - INTERVAL '30' SECOND,
    
    -- 主键约束
    PRIMARY KEY (reading_id) NOT ENFORCED
) WITH (
    'connector' = 'kafka',
    'topic' = 'sensor-readings',
    'properties.bootstrap.servers' = 'kafka:9092',
    'properties.group.id' = 'flink-sensor-consumer',
    'format' = 'json',
    'json.ignore-parse-errors' = 'true',
    'scan.startup.mode' = 'latest-offset',
    'sink.partitioner' = 'round-robin'
);

-- ----------------------------------------------------------------------------
-- 2. 设备注册表 - Kafka Source (维度表)
-- 存储设备元信息和注册状态
-- ----------------------------------------------------------------------------
CREATE TABLE device_registry (
    -- 设备标识
    device_id STRING,
    device_name STRING,
    device_type STRING,
    
    -- 位置信息
    location STRING,
    zone STRING,
    floor STRING,
    building STRING,
    
    -- 设备属性
    manufacturer STRING,
    model STRING,
    serial_number STRING,
    
    -- 配置参数
    calibration_offset DOUBLE,
    alert_threshold_high DOUBLE,
    alert_threshold_low DOUBLE,
    sampling_interval INT,
    
    -- 状态
    status STRING,  -- ACTIVE, INACTIVE, MAINTENANCE, DECOMMISSIONED
    
    -- 时间戳
    registered_at TIMESTAMP(3),
    last_seen_at TIMESTAMP(3),
    
    -- 主键
    PRIMARY KEY (device_id) NOT ENFORCED
) WITH (
    'connector' = 'kafka',
    'topic' = 'device-events',
    'properties.bootstrap.servers' = 'kafka:9092',
    'properties.group.id' = 'flink-device-consumer',
    'format' = 'json',
    'json.ignore-parse-errors' = 'true',
    'scan.startup.mode' = 'earliest-offset'
);

-- ----------------------------------------------------------------------------
-- 3. 处理后的指标数据 - InfluxDB Sink
-- 聚合后的时序数据输出到InfluxDB
-- ----------------------------------------------------------------------------
CREATE TABLE processed_metrics (
    -- 时间戳 (InfluxDB 使用的时间)
    time TIMESTAMP(3),
    
    -- 标签 (Tags) - 用于索引
    device_id STRING,
    device_type STRING,
    location STRING,
    zone STRING,
    metric_type STRING,  -- temperature, pressure, humidity, etc.
    
    -- 字段 (Fields) - 存储数据
    value DOUBLE,
    avg_value DOUBLE,
    min_value DOUBLE,
    max_value DOUBLE,
    count_value BIGINT,
    
    -- 元数据
    window_start TIMESTAMP(3),
    window_end TIMESTAMP(3)
) WITH (
    'connector' = 'influxdb',
    'url' = 'http://influxdb:8086',
    'database' = 'sensor-data',
    'username' = 'admin',
    'password' = 'flink-iot-2024',
    'measurement' = 'processed_metrics'
);

-- ----------------------------------------------------------------------------
-- 4. 告警表 - Kafka Sink
-- 实时告警事件输出
-- ----------------------------------------------------------------------------
CREATE TABLE alerts (
    -- 告警标识
    alert_id STRING,
    alert_time TIMESTAMP(3),
    
    -- 关联设备
    device_id STRING,
    device_type STRING,
    location STRING,
    
    -- 告警详情
    alert_type STRING,      -- THRESHOLD_EXCEEDED, DEVICE_OFFLINE, ANOMALY_DETECTED
    severity STRING,        -- CRITICAL, HIGH, MEDIUM, LOW, INFO
    metric_name STRING,
    metric_value DOUBLE,
    threshold_value DOUBLE,
    
    -- 描述
    description STRING,
    
    -- 处理状态
    status STRING DEFAULT 'NEW',  -- NEW, ACKNOWLEDGED, RESOLVED, IGNORED
    
    -- 水印
    WATERMARK FOR alert_time AS alert_time - INTERVAL '30' SECOND,
    
    PRIMARY KEY (alert_id) NOT ENFORCED
) WITH (
    'connector' = 'kafka',
    'topic' = 'alerts',
    'properties.bootstrap.servers' = 'kafka:9092',
    'format' = 'json',
    'json.fail-on-missing-field' = 'false',
    'sink.partitioner' = 'default'
);

-- ----------------------------------------------------------------------------
-- 5. MQTT 输入表 - 直接接收EMQX数据
-- 用于直接从MQTT Broker接收数据
-- ----------------------------------------------------------------------------
CREATE TABLE mqtt_sensor_readings (
    -- MQTT主题解析的字段
    topic STRING,
    payload STRING,  -- JSON payload
    
    -- 解析后的字段 (使用JSON函数提取)
    device_id AS JSON_VALUE(payload, '$.device_id'),
    event_time AS TO_TIMESTAMP(JSON_VALUE(payload, '$.timestamp')),
    temperature AS CAST(JSON_VALUE(payload, '$.temperature') AS DOUBLE),
    pressure AS CAST(JSON_VALUE(payload, '$.pressure') AS DOUBLE),
    humidity AS CAST(JSON_VALUE(payload, '$.humidity') AS DOUBLE),
    
    -- 事件时间处理
    proc_time AS PROCTIME(),
    
    -- 水印
    WATERMARK FOR event_time AS event_time - INTERVAL '30' SECOND
) WITH (
    'connector' = 'mqtt',
    'hostUrl' = 'tcp://emqx:1883',
    'username' = 'admin',
    'password' = 'public',
    'topics' = 'sensors/+/data',
    'format' = 'raw'
);

-- ----------------------------------------------------------------------------
-- 6. 设备状态变更日志表
-- 用于CDC捕获设备状态变化
-- ----------------------------------------------------------------------------
CREATE TABLE device_status_log (
    log_id STRING,
    device_id STRING,
    old_status STRING,
    new_status STRING,
    changed_at TIMESTAMP(3),
    changed_by STRING,
    reason STRING,
    
    WATERMARK FOR changed_at AS changed_at - INTERVAL '30' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'device-events',
    'properties.bootstrap.servers' = 'kafka:9092',
    'properties.group.id' = 'flink-status-consumer',
    'format' = 'json',
    'scan.startup.mode' = 'earliest-offset'
);

-- ----------------------------------------------------------------------------
-- 验证表创建
-- ----------------------------------------------------------------------------
SHOW TABLES;

-- 查看表结构详情
DESCRIBE sensor_readings;
DESCRIBE device_registry;
