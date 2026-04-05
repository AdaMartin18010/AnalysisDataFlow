-- =====================================
-- Flink IoT Smart Building - Data Cleaning Views
-- 数据清洗与验证视图
-- =====================================

-- 1. 能耗数据清洗视图
CREATE VIEW view_energy_cleaned AS
SELECT 
    e.device_id,
    d.device_type,
    d.building_id,
    d.floor_id,
    d.zone_id,
    d.tenant_id,
    d.rated_power_kw,
    e.reading_time,
    -- 数据质量标记
    CASE 
        WHEN e.active_power_kw < 0 THEN -1
        WHEN e.active_power_kw > d.rated_power_kw * 1.5 THEN -2
        WHEN e.power_factor < 0 OR e.power_factor > 1 THEN -3
        WHEN e.voltage_v < 180 OR e.voltage_v > 260 THEN -4
        WHEN e.quality_code > 0 THEN -5
        ELSE 0
    END as data_quality_flag,
    -- 清洗后的功率值
    CASE 
        WHEN e.active_power_kw < 0 THEN NULL
        WHEN e.active_power_kw > d.rated_power_kw * 1.5 THEN d.rated_power_kw
        ELSE e.active_power_kw
    END as active_power_kw_cleaned,
    -- 清洗后的功率因数
    CASE 
        WHEN e.power_factor < 0 OR e.power_factor > 1 THEN 0.85
        ELSE e.power_factor
    END as power_factor_cleaned,
    e.reactive_power_kvar,
    e.voltage_v,
    e.current_a,
    e.cumulative_kwh,
    e.frequency_hz
FROM source_energy_readings e
LEFT JOIN dim_device FOR SYSTEM_TIME AS OF e.reading_time AS d 
    ON e.device_id = d.device_id;

-- 2. 环境数据清洗视图
CREATE VIEW view_environmental_cleaned AS
SELECT 
    s.sensor_id,
    d.building_id,
    d.floor_id,
    d.zone_id,
    s.sensor_type,
    s.reading_time,
    s.unit,
    -- 范围验证和清洗
    CASE 
        WHEN s.sensor_type = 'TEMPERATURE' AND (s.value < -20 OR s.value > 60) THEN NULL
        WHEN s.sensor_type = 'HUMIDITY' AND (s.value < 0 OR s.value > 100) THEN NULL
        WHEN s.sensor_type = 'CO2' AND (s.value < 300 OR s.value > 5000) THEN NULL
        WHEN s.sensor_type = 'ILLUMINANCE' AND (s.value < 0 OR s.value > 100000) THEN NULL
        WHEN s.quality_flag > 0 THEN NULL
        ELSE s.value
    END as value_cleaned,
    s.quality_flag
FROM source_environmental s
LEFT JOIN dim_device FOR SYSTEM_TIME AS OF s.reading_time AS d 
    ON s.sensor_id = d.device_id
WHERE s.sensor_type IN ('TEMPERATURE', 'HUMIDITY', 'CO2', 'ILLUMINANCE', 'PRESSURE');

-- 3. 数据质量统计视图
CREATE VIEW view_data_quality_stats AS
SELECT 
    building_id,
    device_type,
    TUMBLE_START(reading_time, INTERVAL '5' MINUTE) as window_start,
    COUNT(*) as total_readings,
    SUM(CASE WHEN data_quality_flag = 0 THEN 1 ELSE 0 END) as good_readings,
    SUM(CASE WHEN data_quality_flag < 0 THEN 1 ELSE 0 END) as bad_readings,
    -- 各类错误统计
    SUM(CASE WHEN data_quality_flag = -1 THEN 1 ELSE 0 END) as negative_value_errors,
    SUM(CASE WHEN data_quality_flag = -2 THEN 1 ELSE 0 END) as overload_errors,
    SUM(CASE WHEN data_quality_flag = -3 THEN 1 ELSE 0 END) as power_factor_errors,
    SUM(CASE WHEN data_quality_flag = -4 THEN 1 ELSE 0 END) as voltage_errors,
    SUM(CASE WHEN data_quality_flag = -5 THEN 1 ELSE 0 END) as device_flag_errors,
    ROUND(
        SUM(CASE WHEN data_quality_flag = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 
        2
    ) as data_quality_percent
FROM view_energy_cleaned
GROUP BY building_id, device_type, TUMBLE(reading_time, INTERVAL '5' MINUTE);

-- 4. 设备状态清洗视图
CREATE VIEW view_equipment_status_cleaned AS
SELECT 
    s.device_id,
    d.building_id,
    d.zone_id,
    d.device_type,
    s.status_time,
    s.operational_status,
    s.running_hours,
    s.fault_code,
    s.maintenance_flag,
    -- 状态有效性检查
    CASE 
        WHEN s.operational_status NOT IN ('RUNNING', 'STOPPED', 'STANDBY', 'FAULT', 'MAINTENANCE') 
        THEN 'UNKNOWN'
        ELSE s.operational_status
    END as status_validated,
    -- 维护预警
    CASE 
        WHEN s.maintenance_flag = TRUE THEN 'SCHEDULED'
        WHEN s.fault_code IS NOT NULL THEN 'FAULT'
        WHEN s.operational_status = 'RUNNING' AND s.running_hours > 8760 THEN 'OVERDUE'
        ELSE 'NORMAL'
    END as maintenance_alert
FROM source_equipment_status s
LEFT JOIN dim_device FOR SYSTEM_TIME AS OF s.status_time AS d 
    ON s.device_id = d.device_id;
