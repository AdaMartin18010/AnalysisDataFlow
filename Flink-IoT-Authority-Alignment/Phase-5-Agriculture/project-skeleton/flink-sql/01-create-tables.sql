-- =====================================================
-- 01-create-tables.sql
-- 绿野农场IoT平台 - Flink SQL 表定义
-- =====================================================

-- ------------------------------------------------
-- 1. 土壤传感器实时数据流（Kafka源表）
-- ------------------------------------------------
CREATE TABLE soil_sensor_stream (
    reading_id          STRING,
    sensor_id           STRING,
    device_eui          STRING,
    zone_id             STRING,
    `timestamp`         TIMESTAMP(3),
    
    -- 土壤测量值
    soil_moisture       DOUBLE COMMENT '土壤体积含水量 0-100%',
    soil_temperature    DOUBLE COMMENT '土壤温度 ℃',
    soil_ec             DOUBLE COMMENT '电导率 dS/m',
    soil_ph             DOUBLE COMMENT 'pH值（仅蔬菜区）',
    
    -- 设备状态
    battery_level       INT COMMENT '电池电量 0-100%',
    signal_rssi         INT COMMENT '信号强度 dBm',
    
    -- 处理时间与水印
    proctime            AS PROCTIME(),
    event_time          AS `timestamp`,
    WATERMARK FOR event_time AS event_time - INTERVAL '30' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'farm.soil.readings',
    'properties.bootstrap.servers' = 'kafka:9092',
    'properties.group.id' = 'flink-farm-processor',
    'scan.startup.mode' = 'latest-offset',
    'format' = 'json',
    'json.fail-on-missing-field' = 'false',
    'json.ignore-parse-errors' = 'true'
);

-- ------------------------------------------------
-- 2. 气象数据流
-- ------------------------------------------------
CREATE TABLE weather_stream (
    station_id          STRING,
    zone_id             STRING,
    `timestamp`         TIMESTAMP(3),
    
    -- 温湿压
    air_temperature     DOUBLE COMMENT '气温 ℃',
    relative_humidity   DOUBLE COMMENT '相对湿度 %',
    atmospheric_pressure DOUBLE COMMENT '气压 hPa',
    
    -- 风
    wind_speed          DOUBLE COMMENT '风速 m/s',
    wind_direction      DOUBLE COMMENT '风向 °',
    wind_gust           DOUBLE COMMENT '阵风 m/s',
    
    -- 辐射与降水
    solar_radiation     DOUBLE COMMENT '太阳辐射 W/m²',
    precipitation_mm    DOUBLE COMMENT '累计降水量 mm',
    
    -- 计算派生
    proctime            AS PROCTIME(),
    event_time          AS `timestamp`,
    WATERMARK FOR event_time AS event_time - INTERVAL '10' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'farm.weather.data',
    'properties.bootstrap.servers' = 'kafka:9092',
    'format' = 'json'
);

-- ------------------------------------------------
-- 3. 阀门控制指令表（Kafka输出）
-- ------------------------------------------------
CREATE TABLE valve_commands (
    command_id          STRING,
    valve_id            STRING,
    zone_id             STRING,
    command_type        STRING COMMENT 'OPEN, CLOSE, ADJUST',
    flow_rate_target    DOUBLE COMMENT '目标流量 m³/h',
    duration_minutes    INT COMMENT '计划持续分钟',
    scheduled_time      TIMESTAMP(3),
    priority            INT COMMENT '1-10',
    reason              STRING,
    created_at          TIMESTAMP(3),
    
    PRIMARY KEY (command_id) NOT ENFORCED
) WITH (
    'connector' = 'upsert-kafka',
    'topic' = 'farm.valve.commands',
    'properties.bootstrap.servers' = 'kafka:9092',
    'key.format' = 'json',
    'value.format' = 'json'
);

-- ------------------------------------------------
-- 4. 告警事件表
-- ------------------------------------------------
CREATE TABLE farm_alerts (
    alert_id            STRING,
    zone_id             STRING,
    alert_type          STRING COMMENT 'IRRIGATION, HEALTH, WEATHER, DEVICE',
    severity            STRING COMMENT 'CRITICAL, HIGH, MEDIUM, LOW',
    message             STRING,
    details             STRING,
    created_at          TIMESTAMP(3),
    
    PRIMARY KEY (alert_id) NOT ENFORCED
) WITH (
    'connector' = 'upsert-kafka',
    'topic' = 'farm.health.alerts',
    'properties.bootstrap.servers' = 'kafka:9092',
    'key.format' = 'json',
    'value.format' = 'json'
);

-- ------------------------------------------------
-- 5. 区域配置维表（JDBC）
-- ------------------------------------------------
CREATE TABLE zone_config (
    zone_id             STRING,
    zone_name           STRING,
    crop_type           STRING,
    growth_stage        STRING,
    soil_type           STRING,
    area_ha             DOUBLE,
    
    -- 土壤参数
    field_capacity      DOUBLE COMMENT '田间持水量 %',
    wilting_point       DOUBLE COMMENT '凋萎点 %',
    mad_pct             DOUBLE COMMENT '管理允许亏缺比例',
    
    -- 灌溉参数
    max_flow_rate       DOUBLE COMMENT '最大流量 m³/h',
    application_efficiency DOUBLE COMMENT '灌溉效率 0-1',
    
    -- 阈值配置
    moisture_critical   DOUBLE COMMENT '紧急灌溉阈值 %',
    moisture_target     DOUBLE COMMENT '目标湿度 %',
    
    PRIMARY KEY (zone_id) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:mysql://mysql:3306/farm_db',
    'table-name' = 'zone_config',
    'username' = 'farm_user',
    'password' = 'farm_pass123',
    'lookup.cache.max-rows' = '1000',
    'lookup.cache.ttl' = '5 min'
);

-- ------------------------------------------------
-- 6. 阀门配置维表
-- ------------------------------------------------
CREATE TABLE valve_config (
    valve_id            STRING,
    zone_id             STRING,
    valve_type          STRING,
    max_flow_rate       DOUBLE,
    control_protocol    STRING,
    
    PRIMARY KEY (valve_id) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:mysql://mysql:3306/farm_db',
    'table-name' = 'valve_config',
    'username' = 'farm_user',
    'password' = 'farm_pass123'
);

-- ------------------------------------------------
-- 7. 灌溉执行记录表（JDBC输出）
-- ------------------------------------------------
CREATE TABLE irrigation_records (
    record_id           STRING PRIMARY KEY NOT ENFORCED,
    valve_id            STRING,
    zone_id             STRING,
    command_id          STRING,
    start_time          TIMESTAMP(3),
    end_time            TIMESTAMP(3),
    actual_duration_min INT,
    water_volume_m3     DOUBLE,
    energy_consumed_kwh DOUBLE,
    trigger_reason      STRING,
    status              STRING COMMENT 'COMPLETED, INTERRUPTED, FAILED'
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:mysql://mysql:3306/farm_db',
    'table-name' = 'irrigation_records',
    'username' = 'farm_user',
    'password' = 'farm_pass123',
    'sink.buffer-flush.max-rows' = '100',
    'sink.buffer-flush.interval' = '5s'
);

-- ------------------------------------------------
-- 8. 时序数据输出到InfluxDB
-- ------------------------------------------------
CREATE TABLE soil_metrics_influx (
    zone_id             STRING,
    crop_type           STRING,
    time                TIMESTAMP(3),
    avg_moisture        DOUBLE,
    min_moisture        DOUBLE,
    max_moisture        DOUBLE,
    std_moisture        DOUBLE,
    reading_count       BIGINT,
    
    PRIMARY KEY (zone_id, time) NOT ENFORCED
) WITH (
    'connector' = 'influxdb',
    'url' = 'http://influxdb:8086',
    'database' = 'farm_metrics',
    'measurement' = 'soil_moisture_5min',
    'username' = 'farm_admin',
    'password' = 'farmpass123',
    'token' = 'farm-token-2024',
    'org' = 'greenfield',
    'write.mode' = 'ASYNC',
    'sink.batch.size' = '1000',
    'sink.flush.interval' = '5000ms'
);

-- ------------------------------------------------
-- 9. 每日灌溉统计表
-- ------------------------------------------------
CREATE TABLE daily_irrigation_stats (
    stat_date           DATE,
    zone_id             STRING,
    crop_type           STRING,
    irrigation_count    INT,
    total_duration_min  INT,
    total_water_m3      DOUBLE,
    avg_flow_rate       DOUBLE,
    total_energy_kwh    DOUBLE,
    water_per_ha        DOUBLE,
    
    PRIMARY KEY (stat_date, zone_id) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:mysql://mysql:3306/farm_db',
    'table-name' = 'daily_irrigation_stats',
    'username' = 'farm_user',
    'password' = 'farm_pass123'
);

-- 打印创建成功信息
SELECT 'Tables created successfully!' AS status;
