-- =====================================
-- Flink IoT Smart Building - Source Tables
-- 数据源定义
-- =====================================

-- 1. 设备元数据维度表
CREATE TABLE IF NOT EXISTS dim_device (
    device_id STRING,
    device_code STRING,
    device_name STRING,
    device_type STRING,
    device_model STRING,
    manufacturer STRING,
    building_id STRING,
    floor_id STRING,
    zone_id STRING,
    tenant_id STRING,
    installation_date DATE,
    rated_power_kw DECIMAL(8,2),
    lifecycle_status STRING,
    PRIMARY KEY (device_id) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/building_db',
    'table-name' = 'dim_device',
    'username' = 'flink_user',
    'password' = 'flink_password',
    'lookup.cache.max-rows' = '10000',
    'lookup.cache.ttl' = '10 min'
);

-- 2. 租户维度表
CREATE TABLE IF NOT EXISTS dim_tenant (
    tenant_id STRING,
    tenant_code STRING,
    tenant_name STRING,
    tenant_type STRING,
    leased_area_sqm DECIMAL(10,2),
    building_id STRING,
    billing_cycle STRING,
    PRIMARY KEY (tenant_id) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/building_db',
    'table-name' = 'dim_tenant',
    'username' = 'flink_user',
    'password' = 'flink_password'
);

-- 3. 电价维度表
CREATE TABLE IF NOT EXISTS dim_electricity_tariff (
    tariff_type STRING,
    effective_date TIMESTAMP(3),
    hour_of_day INT,
    day_type STRING,
    price_per_kwh DECIMAL(8,4),
    PRIMARY KEY (tariff_type, hour_of_day, day_type) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/building_db',
    'table-name' = 'electricity_tariff',
    'username' = 'flink_user',
    'password' = 'flink_password'
);

-- 4. 能耗传感器数据源（Kafka）
CREATE TABLE IF NOT EXISTS source_energy_readings (
    device_id STRING,
    reading_time TIMESTAMP(3),
    active_power_kw DECIMAL(10,3),
    reactive_power_kvar DECIMAL(10,3),
    voltage_v DECIMAL(8,2),
    current_a DECIMAL(8,3),
    power_factor DECIMAL(4,3),
    cumulative_kwh DECIMAL(12,3),
    frequency_hz DECIMAL(6,3),
    quality_code INT,
    WATERMARK FOR reading_time AS reading_time - INTERVAL '30' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'building.energy.readings',
    'properties.bootstrap.servers' = 'kafka:29092',
    'properties.group.id' = 'flink-energy-consumption',
    'format' = 'json',
    'json.ignore-parse-errors' = 'true',
    'scan.startup.mode' = 'latest-offset'
);

-- 5. 环境传感器数据源（Kafka）
CREATE TABLE IF NOT EXISTS source_environmental (
    sensor_id STRING,
    sensor_type STRING,
    reading_time TIMESTAMP(3),
    value DECIMAL(10,4),
    unit STRING,
    quality_flag INT,
    WATERMARK FOR reading_time AS reading_time - INTERVAL '1' MINUTE
) WITH (
    'connector' = 'kafka',
    'topic' = 'building.environmental',
    'properties.bootstrap.servers' = 'kafka:29092',
    'properties.group.id' = 'flink-environmental',
    'format' = 'json',
    'json.ignore-parse-errors' = 'true'
);

-- 6. occupancy传感器数据源
CREATE TABLE IF NOT EXISTS source_occupancy (
    sensor_id STRING,
    zone_id STRING,
    reading_time TIMESTAMP(3),
    occupancy_count INT,
    confidence DECIMAL(4,3),
    WATERMARK FOR reading_time AS reading_time - INTERVAL '30' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'building.occupancy',
    'properties.bootstrap.servers' = 'kafka:29092',
    'properties.group.id' = 'flink-occupancy',
    'format' = 'json'
);

-- 7. 设备状态数据源
CREATE TABLE IF NOT EXISTS source_equipment_status (
    device_id STRING,
    status_time TIMESTAMP(3),
    operational_status STRING,
    running_hours DECIMAL(10,2),
    fault_code STRING,
    maintenance_flag BOOLEAN,
    WATERMARK FOR status_time AS status_time - INTERVAL '1' MINUTE
) WITH (
    'connector' = 'kafka',
    'topic' = 'building.equipment.status',
    'properties.bootstrap.servers' = 'kafka:29092',
    'properties.group.id' = 'flink-equipment',
    'format' = 'json'
);
