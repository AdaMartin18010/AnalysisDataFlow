-- ============================================================================
-- Flink IoT SQL - 03. 时间语义与水印配置
-- 文档编号: F-WATERMARK-03
-- 形式化等级: L4
-- 创建时间: 2026-04-05
-- 
-- 功能: 配置事件时间处理、水印策略、窗口计算
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. 水印基础配置
-- ----------------------------------------------------------------------------

-- 1.1 标准水印配置 (30秒延迟)
-- 适用于传感器数据: 允许30秒的乱序到达
CREATE TEMPORARY VIEW watermark_30s AS
SELECT 
    reading_id,
    device_id,
    device_type,
    location,
    temperature,
    pressure,
    humidity,
    event_time,
    
    -- 当前水印值查询
    CURRENT_WATERMARK(event_time) AS current_watermark,
    
    -- 延迟计算: 事件时间与水印的差距
    TIMESTAMPDIFF(SECOND, event_time, CURRENT_WATERMARK(event_time)) AS lateness_seconds
    
FROM sensor_readings;

-- 1.2 验证水印推进
SELECT 
    device_type,
    COUNT(*) AS event_count,
    MIN(event_time) AS min_event_time,
    MAX(event_time) AS max_event_time,
    MAX(current_watermark) AS latest_watermark,
    TIMESTAMPDIFF(SECOND, MAX(event_time), MAX(current_watermark)) AS max_lateness
FROM watermark_30s
GROUP BY device_type;

-- ----------------------------------------------------------------------------
-- 2. 乱序数据处理
-- ----------------------------------------------------------------------------

-- 2.1 识别乱序事件
-- 事件时间早于当前水印的事件被认为是乱序的
CREATE TEMPORARY VIEW out_of_order_events AS
SELECT 
    reading_id,
    device_id,
    device_type,
    temperature,
    event_time,
    current_watermark,
    lateness_seconds,
    
    -- 乱序分类
    CASE 
        WHEN lateness_seconds > 30 THEN 'SEVERELY_LATE'
        WHEN lateness_seconds > 0 THEN 'SLIGHTLY_LATE'
        ELSE 'ON_TIME'
    END AS timeliness_status
    
FROM watermark_30s
WHERE lateness_seconds IS NOT NULL;

-- 2.2 乱序统计
SELECT 
    device_type,
    timeliness_status,
    COUNT(*) AS event_count,
    AVG(ABS(lateness_seconds)) AS avg_lateness_sec,
    MAX(ABS(lateness_seconds)) AS max_lateness_sec,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY device_type), 2) AS percentage
FROM out_of_order_events
GROUP BY device_type, timeliness_status
ORDER BY device_type, timeliness_status;

-- ----------------------------------------------------------------------------
-- 3. 严格水印 vs 宽松水印对比
-- ----------------------------------------------------------------------------

-- 3.1 严格水印配置 (5秒延迟)
-- 适用于低延迟要求的场景
CREATE TEMPORARY VIEW strict_watermark AS
SELECT 
    reading_id,
    device_id,
    device_type,
    temperature,
    event_time,
    event_time - INTERVAL '5' SECOND AS strict_watermark_value,
    CURRENT_TIMESTAMP AS processing_time
FROM sensor_readings;

-- 3.2 宽松水印配置 (2分钟延迟)
-- 适用于网络不稳定的场景
CREATE TEMPORARY VIEW lenient_watermark AS
SELECT 
    reading_id,
    device_id,
    device_type,
    temperature,
    event_time,
    event_time - INTERVAL '2' MINUTE AS lenient_watermark_value,
    CURRENT_TIMESTAMP AS processing_time
FROM sensor_readings;

-- 3.3 不同水印策略的延迟容忍度对比
SELECT 
    'STRICT_5S' AS watermark_strategy,
    COUNT(*) AS on_time_events,
    AVG(TIMESTAMPDIFF(SECOND, event_time, processing_time)) AS avg_processing_delay
FROM strict_watermark
WHERE event_time > strict_watermark_value

UNION ALL

SELECT 
    'STANDARD_30S' AS watermark_strategy,
    COUNT(*),
    AVG(TIMESTAMPDIFF(SECOND, event_time, processing_time))
FROM watermark_30s
WHERE event_time > current_watermark

UNION ALL

SELECT 
    'LENIENT_2M' AS watermark_strategy,
    COUNT(*),
    AVG(TIMESTAMPDIFF(SECOND, event_time, processing_time))
FROM lenient_watermark
WHERE event_time > lenient_watermark_value;

-- ----------------------------------------------------------------------------
-- 4. 事件时间窗口计算
-- ----------------------------------------------------------------------------

-- 4.1 滚动窗口 (Tumbling Window)
-- 每分钟统计传感器数据
SELECT 
    device_type,
    TUMBLE_START(event_time, INTERVAL '1' MINUTE) AS window_start,
    TUMBLE_END(event_time, INTERVAL '1' MINUTE) AS window_end,
    COUNT(*) AS reading_count,
    AVG(temperature) AS avg_temperature,
    MIN(temperature) AS min_temperature,
    MAX(temperature) AS max_temperature,
    STDDEV(temperature) AS stddev_temperature
FROM sensor_readings
GROUP BY 
    device_type,
    TUMBLE(event_time, INTERVAL '1' MINUTE)
ORDER BY window_start DESC, device_type
LIMIT 20;

-- 4.2 滑动窗口 (Hop Window)
-- 每30秒计算过去2分钟的统计数据
SELECT 
    device_type,
    HOP_START(event_time, INTERVAL '30' SECOND, INTERVAL '2' MINUTE) AS window_start,
    HOP_END(event_time, INTERVAL '30' SECOND, INTERVAL '2' MINUTE) AS window_end,
    COUNT(*) AS reading_count,
    AVG(temperature) AS avg_temperature,
    AVG(pressure) AS avg_pressure,
    AVG(humidity) AS avg_humidity
FROM sensor_readings
GROUP BY 
    device_type,
    HOP(event_time, INTERVAL '30' SECOND, INTERVAL '2' MINUTE)
ORDER BY window_start DESC
LIMIT 20;

-- 4.3 会话窗口 (Session Window)
-- 检测设备活动会话 (5分钟无活动视为会话结束)
SELECT 
    device_id,
    device_type,
    SESSION_START(event_time, INTERVAL '5' MINUTE) AS session_start,
    SESSION_END(event_time, INTERVAL '5' MINUTE) AS session_end,
    COUNT(*) AS events_in_session,
    TIMESTAMPDIFF(MINUTE, 
        SESSION_START(event_time, INTERVAL '5' MINUTE),
        SESSION_END(event_time, INTERVAL '5' MINUTE)
    ) AS session_duration_min,
    AVG(temperature) AS avg_temp_in_session
FROM sensor_readings
GROUP BY 
    device_id,
    device_type,
    SESSION(event_time, INTERVAL '5' MINUTE)
HAVING COUNT(*) >= 3  -- 至少3个事件的会话
ORDER BY session_start DESC
LIMIT 20;

-- ----------------------------------------------------------------------------
-- 5. 水位线延迟处理策略
-- ----------------------------------------------------------------------------

-- 5.1 迟到数据处理 (Late Data Handling)
-- 配置允许的迟到时间 (30秒水印 + 60秒允许迟到 = 90秒总容忍)
CREATE TEMPORARY VIEW late_data_handling AS
SELECT 
    reading_id,
    device_id,
    device_type,
    temperature,
    event_time,
    
    -- 当前水印
    CURRENT_WATERMARK(event_time) AS watermark,
    
    -- 是否迟到
    CASE 
        WHEN event_time < CURRENT_WATERMARK(event_time) - INTERVAL '60' SECOND 
        THEN 'DROPPED'
        WHEN event_time < CURRENT_WATERMARK(event_time) 
        THEN 'LATE_BUT_ACCEPTED'
        ELSE 'ON_TIME'
    END AS late_data_status
    
FROM sensor_readings;

-- 5.2 迟到数据统计
SELECT 
    late_data_status,
    COUNT(*) AS event_count,
    COUNT(DISTINCT device_id) AS affected_devices,
    AVG(temperature) AS avg_temperature
FROM late_data_handling
GROUP BY late_data_status;

-- ----------------------------------------------------------------------------
-- 6. 多流时间对齐 (Interval Join)
-- ----------------------------------------------------------------------------

-- 6.1 传感器数据与设备心跳对齐
-- 查找在传感器读数前后30秒内有心跳的设备
SELECT 
    s.device_id,
    s.device_type,
    s.temperature,
    s.event_time AS sensor_time,
    d.changed_at AS heartbeat_time,
    TIMESTAMPDIFF(SECOND, s.event_time, d.changed_at) AS time_diff_sec
FROM sensor_readings s
JOIN device_status_log d
    ON s.device_id = d.device_id
    AND d.changed_at BETWEEN s.event_time - INTERVAL '30' SECOND 
                         AND s.event_time + INTERVAL '30' SECOND
WHERE d.new_status = 'ACTIVE'
LIMIT 20;

-- ----------------------------------------------------------------------------
-- 7. 时间属性函数示例
-- ----------------------------------------------------------------------------

-- 7.1 时间转换和提取
SELECT 
    reading_id,
    device_id,
    event_time,
    
    -- 日期提取
    EXTRACT(YEAR FROM event_time) AS year,
    EXTRACT(MONTH FROM event_time) AS month,
    EXTRACT(DAY FROM event_time) AS day,
    EXTRACT(HOUR FROM event_time) AS hour,
    EXTRACT(MINUTE FROM event_time) AS minute,
    EXTRACT(DOW FROM event_time) AS day_of_week,  -- 0=Sunday, 6=Saturday
    
    -- 时间格式化
    DATE_FORMAT(event_time, 'yyyy-MM-dd') AS date_str,
    DATE_FORMAT(event_time, 'HH:mm:ss') AS time_str,
    DATE_FORMAT(event_time, 'yyyy-MM-dd HH:mm:ss') AS datetime_str,
    
    -- 处理时间对比
    PROCTIME() AS processing_time,
    TIMESTAMPDIFF(SECOND, event_time, PROCTIME()) AS processing_delay_sec
    
FROM sensor_readings
LIMIT 10;

-- ----------------------------------------------------------------------------
-- 8. 窗口聚合进阶示例
-- ----------------------------------------------------------------------------

-- 8.1 累积窗口 (Cumulative Window)
-- 每小时累积统计
SELECT 
    device_type,
    CUMULATE_START(event_time, INTERVAL '1' HOUR, INTERVAL '10' MINUTE) AS window_start,
    CUMULATE_END(event_time, INTERVAL '1' HOUR, INTERVAL '10' MINUTE) AS window_end,
    COUNT(*) AS cumulative_count,
    AVG(temperature) AS cumulative_avg_temp
FROM sensor_readings
GROUP BY 
    device_type,
    CUMULATE(event_time, INTERVAL '1' HOUR, INTERVAL '10' MINUTE)
ORDER BY window_start DESC
LIMIT 20;

-- 8.2 OVER窗口 (分析函数)
-- 计算移动平均和趋势
SELECT 
    device_id,
    device_type,
    event_time,
    temperature,
    
    -- 过去5个读数的移动平均
    AVG(temperature) OVER (
        PARTITION BY device_id 
        ORDER BY event_time 
        ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
    ) AS moving_avg_5,
    
    -- 过去10分钟的移动平均
    AVG(temperature) OVER (
        PARTITION BY device_id 
        ORDER BY event_time 
        RANGE BETWEEN INTERVAL '10' MINUTE PRECEDING AND CURRENT ROW
    ) AS time_based_avg,
    
    -- 排名
    ROW_NUMBER() OVER (
        PARTITION BY device_id 
        ORDER BY event_time DESC
    ) AS reading_rank
    
FROM sensor_readings
WHERE device_type = 'TEMPERATURE_SENSOR'
ORDER BY device_id, event_time DESC
LIMIT 50;

-- ----------------------------------------------------------------------------
-- 9. 水印监控查询
-- ----------------------------------------------------------------------------

-- 9.1 实时水印健康检查
SELECT 
    'WATERMARK_HEALTH' AS check_type,
    COUNT(*) AS total_events,
    SUM(CASE WHEN CURRENT_WATERMARK(event_time) IS NOT NULL THEN 1 ELSE 0 END) AS with_watermark,
    MAX(CURRENT_WATERMARK(event_time)) AS latest_watermark,
    MIN(CURRENT_WATERMARK(event_time)) AS earliest_watermark,
    TIMESTAMPDIFF(SECOND, 
        MIN(CURRENT_WATERMARK(event_time)), 
        MAX(CURRENT_WATERMARK(event_time))
    ) AS watermark_spread_sec
FROM sensor_readings;
