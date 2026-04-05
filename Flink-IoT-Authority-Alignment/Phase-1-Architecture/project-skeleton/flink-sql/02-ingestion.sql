-- ============================================================================
-- Flink IoT SQL - 02. 数据摄取逻辑
-- 文档编号: F-INGEST-02
-- 形式化等级: L4
-- 创建时间: 2026-04-05
-- 
-- 功能: 定义从源系统到Flink的数据摄取管道
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. 基础数据摄取 - 从Kafka读取传感器数据
-- ----------------------------------------------------------------------------

-- 1.1 实时查看原始数据流
SELECT 
    reading_id,
    device_id,
    device_type,
    location,
    temperature,
    pressure,
    humidity,
    event_time,
    CURRENT_WATERMARK(event_time) AS current_watermark
FROM sensor_readings
LIMIT 10;

-- 1.2 数据质量检查 - 识别异常值
SELECT 
    device_id,
    device_type,
    location,
    temperature,
    pressure,
    humidity,
    CASE 
        WHEN temperature IS NULL THEN 'MISSING_TEMP'
        WHEN temperature < -50 OR temperature > 100 THEN 'INVALID_TEMP'
        WHEN pressure IS NULL THEN 'MISSING_PRESSURE'
        WHEN pressure < 0 OR pressure > 1000 THEN 'INVALID_PRESSURE'
        WHEN humidity IS NULL THEN 'MISSING_HUMIDITY'
        WHEN humidity < 0 OR humidity > 100 THEN 'INVALID_HUMIDITY'
        ELSE 'VALID'
    END AS data_quality_status,
    event_time
FROM sensor_readings
WHERE 
    temperature IS NULL 
    OR temperature < -50 OR temperature > 100
    OR pressure IS NULL 
    OR pressure < 0 OR pressure > 1000
    OR humidity IS NULL 
    OR humidity < 0 OR humidity > 100;

-- ----------------------------------------------------------------------------
-- 2. 数据清洗与标准化
-- ----------------------------------------------------------------------------

-- 2.1 创建清洗后的数据视图
CREATE TEMPORARY VIEW cleaned_sensor_readings AS
SELECT 
    reading_id,
    event_time,
    device_id,
    COALESCE(device_type, 'UNKNOWN') AS device_type,
    COALESCE(location, 'UNKNOWN') AS location,
    
    -- 清洗温度数据: 设置合理范围并处理NULL
    CASE 
        WHEN temperature IS NULL THEN NULL
        WHEN temperature < -40 THEN -40
        WHEN temperature > 80 THEN 80
        ELSE temperature
    END AS temperature,
    
    -- 清洗压力数据
    CASE 
        WHEN pressure IS NULL THEN NULL
        WHEN pressure < 0 THEN 0
        WHEN pressure > 500 THEN 500
        ELSE pressure
    END AS pressure,
    
    -- 清洗湿度数据
    CASE 
        WHEN humidity IS NULL THEN NULL
        WHEN humidity < 0 THEN 0
        WHEN humidity > 100 THEN 100
        ELSE humidity
    END AS humidity,
    
    -- 电压数据清洗
    CASE 
        WHEN voltage IS NULL THEN 3.3
        WHEN voltage < 0 THEN 0
        WHEN voltage > 5 THEN 5
        ELSE voltage
    END AS voltage,
    
    sensor_version,
    firmware_version,
    
    -- 数据质量标记
    CASE 
        WHEN temperature IS NULL OR pressure IS NULL OR humidity IS NULL 
        THEN FALSE 
        ELSE TRUE 
    END AS is_complete,
    
    -- 数据清洗标记
    CASE 
        WHEN temperature != CASE 
            WHEN temperature IS NULL THEN NULL
            WHEN temperature < -40 THEN -40
            WHEN temperature > 80 THEN 80
            ELSE temperature
        END THEN TRUE
        WHEN pressure != CASE 
            WHEN pressure IS NULL THEN NULL
            WHEN pressure < 0 THEN 0
            WHEN pressure > 500 THEN 500
            ELSE pressure
        END THEN TRUE
        ELSE FALSE
    END AS was_cleaned
    
FROM sensor_readings;

-- 2.2 验证清洗后的数据
SELECT 
    device_type,
    COUNT(*) AS total_count,
    AVG(temperature) AS avg_temp,
    AVG(pressure) AS avg_pressure,
    AVG(humidity) AS avg_humidity,
    SUM(CASE WHEN is_complete THEN 1 ELSE 0 END) AS complete_count,
    SUM(CASE WHEN was_cleaned THEN 1 ELSE 0 END) AS cleaned_count
FROM cleaned_sensor_readings
GROUP BY device_type;

-- ----------------------------------------------------------------------------
-- 3. 设备信息关联 (Temporal Join)
-- ----------------------------------------------------------------------------

-- 3.1 传感器数据关联设备注册信息
CREATE TEMPORARY VIEW enriched_sensor_readings AS
SELECT 
    s.reading_id,
    s.event_time,
    s.device_id,
    s.device_type,
    s.location,
    s.temperature,
    s.pressure,
    s.humidity,
    s.voltage,
    s.is_complete,
    s.was_cleaned,
    
    -- 设备注册表信息
    d.device_name,
    d.zone,
    d.floor,
    d.building,
    d.manufacturer,
    d.calibration_offset,
    d.alert_threshold_high,
    d.alert_threshold_low,
    d.sampling_interval,
    d.status AS device_status,
    
    -- 应用校准偏移
    s.temperature + COALESCE(d.calibration_offset, 0) AS calibrated_temperature
    
FROM cleaned_sensor_readings s
LEFT JOIN device_registry FOR SYSTEM_TIME AS OF s.event_time AS d
    ON s.device_id = d.device_id;

-- 3.2 验证关联结果
SELECT 
    device_type,
    zone,
    COUNT(*) AS reading_count,
    AVG(calibrated_temperature) AS avg_calibrated_temp,
    COUNT(DISTINCT device_id) AS unique_devices
FROM enriched_sensor_readings
WHERE device_status = 'ACTIVE'
GROUP BY device_type, zone
ORDER BY reading_count DESC
LIMIT 20;

-- ----------------------------------------------------------------------------
-- 4. 数据分流 - 根据业务规则分发数据
-- ----------------------------------------------------------------------------

-- 4.1 创建数据分流视图
CREATE TEMPORARY VIEW data_routing AS
SELECT 
    *,
    CASE 
        -- 紧急告警数据 -> 实时告警处理
        WHEN calibrated_temperature > alert_threshold_high 
             OR calibrated_temperature < alert_threshold_low
        THEN 'ALERT_QUEUE'
        
        -- 设备离线检测
        WHEN device_status != 'ACTIVE'
        THEN 'MAINTENANCE_QUEUE'
        
        -- 正常数据 -> 长期存储
        ELSE 'STORAGE_QUEUE'
    END AS routing_target
FROM enriched_sensor_readings;

-- 4.2 查看数据分发统计
SELECT 
    routing_target,
    COUNT(*) AS message_count,
    COUNT(DISTINCT device_id) AS device_count,
    MIN(event_time) AS earliest_time,
    MAX(event_time) AS latest_time
FROM data_routing
GROUP BY routing_target;

-- ----------------------------------------------------------------------------
-- 5. 批量数据摄取 (批量模式)
-- ----------------------------------------------------------------------------

-- 5.1 模拟批量上报的数据处理
-- 处理设备批量上传的历史数据
CREATE TEMPORARY VIEW batch_ingestion AS
SELECT 
    reading_id,
    event_time,
    device_id,
    device_type,
    location,
    temperature,
    pressure,
    humidity,
    voltage,
    
    -- 批量数据标记
    CASE 
        WHEN event_time < PROCTIME() - INTERVAL '1' HOUR 
        THEN 'HISTORICAL_BATCH'
        ELSE 'REALTIME'
    END AS ingestion_mode,
    
    -- 延迟计算
    TIMESTAMPDIFF(SECOND, event_time, PROCTIME()) AS ingestion_latency_sec
    
FROM sensor_readings
WHERE event_time IS NOT NULL;

-- 5.2 批量数据统计
SELECT 
    ingestion_mode,
    COUNT(*) AS record_count,
    AVG(ingestion_latency_sec) AS avg_latency_sec,
    MAX(ingestion_latency_sec) AS max_latency_sec,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY ingestion_latency_sec) AS p95_latency_sec
FROM batch_ingestion
GROUP BY ingestion_mode;

-- ----------------------------------------------------------------------------
-- 6. 数据格式转换示例
-- ----------------------------------------------------------------------------

-- 6.1 转换为标准JSON输出格式
SELECT 
    device_id,
    TO_JSON(
        MAP[
            'device_id', device_id,
            'timestamp', CAST(event_time AS STRING),
            'readings', TO_JSON(MAP[
                'temperature', CAST(temperature AS STRING),
                'pressure', CAST(pressure AS STRING),
                'humidity', CAST(humidity AS STRING)
            ]),
            'metadata', TO_JSON(MAP[
                'location', location,
                'device_type', device_type,
                'quality_check', CAST(is_complete AS STRING)
            ])
        ]
    ) AS json_output
FROM cleaned_sensor_readings
LIMIT 5;

-- ----------------------------------------------------------------------------
-- 7. 摄取监控指标
-- ----------------------------------------------------------------------------

-- 7.1 按时间窗口统计摄取速率
SELECT 
    TUMBLE_START(event_time, INTERVAL '1' MINUTE) AS window_start,
    TUMBLE_END(event_time, INTERVAL '1' MINUTE) AS window_end,
    COUNT(*) AS messages_per_minute,
    COUNT(DISTINCT device_id) AS active_devices,
    AVG(temperature) AS avg_temperature,
    SUM(CASE WHEN temperature IS NULL THEN 1 ELSE 0 END) AS null_temp_count
FROM sensor_readings
GROUP BY TUMBLE(event_time, INTERVAL '1' MINUTE)
ORDER BY window_start DESC
LIMIT 10;
