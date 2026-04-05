-- ============================================================================
-- Flink IoT SQL - 04. 查询示例集合
-- 文档编号: F-QUERIES-04
-- 形式化等级: L4
-- 创建时间: 2026-04-05
-- 
-- 包含: 5+ 生产级查询示例
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 查询示例 1: 实时温度异常检测 (阈值告警)
-- 检测超过安全阈值的温度读数
-- ----------------------------------------------------------------------------
CREATE TEMPORARY VIEW temperature_alerts AS
SELECT 
    CONCAT('TEMP_ALERT_', reading_id) AS alert_id,
    event_time AS alert_time,
    device_id,
    device_type,
    location,
    'THRESHOLD_EXCEEDED' AS alert_type,
    CASE 
        WHEN temperature > 70 THEN 'CRITICAL'
        WHEN temperature > 50 THEN 'HIGH'
        WHEN temperature < -20 THEN 'HIGH'
        ELSE 'MEDIUM'
    END AS severity,
    'temperature' AS metric_name,
    temperature AS metric_value,
    CASE 
        WHEN temperature > 70 THEN 70
        WHEN temperature > 50 THEN 50
        WHEN temperature < -20 THEN -20
        ELSE 0
    END AS threshold_value,
    CONCAT('Temperature ', temperature, '°C exceeds threshold at ', location) AS description
FROM sensor_readings
WHERE 
    temperature > 50  -- 高温告警
    OR temperature < -20  -- 低温告警
    OR temperature IS NULL;  -- 数据丢失告警

-- 将告警插入告警表
INSERT INTO alerts
SELECT * FROM temperature_alerts;

-- 查询最近的温度告警
SELECT 
    alert_id,
    device_id,
    device_type,
    location,
    severity,
    metric_value,
    threshold_value,
    description,
    alert_time
FROM temperature_alerts
ORDER BY alert_time DESC
LIMIT 20;

-- ----------------------------------------------------------------------------
-- 查询示例 2: 设备健康状态实时监控 (5分钟窗口)
-- 监控设备在线状态和数据质量
-- ----------------------------------------------------------------------------
CREATE TEMPORARY VIEW device_health_metrics AS
SELECT 
    device_id,
    device_type,
    location,
    TUMBLE_START(event_time, INTERVAL '5' MINUTE) AS window_start,
    TUMBLE_END(event_time, INTERVAL '5' MINUTE) AS window_end,
    
    -- 数据量统计
    COUNT(*) AS total_readings,
    
    -- 数据完整性
    SUM(CASE WHEN temperature IS NOT NULL THEN 1 ELSE 0 END) AS temp_readings,
    SUM(CASE WHEN pressure IS NOT NULL THEN 1 ELSE 0 END) AS pressure_readings,
    SUM(CASE WHEN humidity IS NOT NULL THEN 1 ELSE 0 END) AS humidity_readings,
    
    -- 数据质量指标
    ROUND(
        (SUM(CASE WHEN temperature IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 
        2
    ) AS data_completeness_pct,
    
    -- 传感器数值范围
    AVG(temperature) AS avg_temperature,
    MIN(temperature) AS min_temperature,
    MAX(temperature) AS max_temperature,
    STDDEV(temperature) AS temp_stddev,
    
    -- 健康评分 (0-100)
    CASE 
        WHEN COUNT(*) < 5 THEN 'CRITICAL'  -- 数据量过少
        WHEN SUM(CASE WHEN temperature IS NULL THEN 1 ELSE 0 END) > COUNT(*) * 0.2 THEN 'WARNING'  -- 缺失率>20%
        WHEN STDDEV(temperature) IS NULL OR STDDEV(temperature) = 0 THEN 'WARNING'  -- 数据无变化
        ELSE 'HEALTHY'
    END AS health_status
    
FROM sensor_readings
GROUP BY 
    device_id,
    device_type,
    location,
    TUMBLE(event_time, INTERVAL '5' MINUTE);

-- 查询设备健康状态
SELECT 
    device_id,
    device_type,
    location,
    window_start,
    total_readings,
    data_completeness_pct,
    avg_temperature,
    health_status
FROM device_health_metrics
ORDER BY 
    CASE health_status 
        WHEN 'CRITICAL' THEN 1 
        WHEN 'WARNING' THEN 2 
        ELSE 3 
    END,
    window_start DESC
LIMIT 30;

-- ----------------------------------------------------------------------------
-- 查询示例 3: 区域级聚合统计 (按位置和小时)
-- 分析不同区域的环境趋势
-- ----------------------------------------------------------------------------
CREATE TEMPORARY VIEW zone_hourly_stats AS
SELECT 
    location,
    zone,
    building,
    DATE_FORMAT(event_time, 'yyyy-MM-dd HH:00:00') AS hour_bucket,
    
    -- 设备活跃度
    COUNT(DISTINCT device_id) AS active_devices,
    COUNT(*) AS total_readings,
    
    -- 温度统计
    ROUND(AVG(temperature), 2) AS avg_temperature,
    ROUND(MIN(temperature), 2) AS min_temperature,
    ROUND(MAX(temperature), 2) AS max_temperature,
    ROUND(MAX(temperature) - MIN(temperature), 2) AS temp_range,
    
    -- 压力统计
    ROUND(AVG(pressure), 2) AS avg_pressure,
    ROUND(MIN(pressure), 2) AS min_pressure,
    ROUND(MAX(pressure), 2) AS max_pressure,
    
    -- 湿度统计
    ROUND(AVG(humidity), 2) AS avg_humidity,
    ROUND(MIN(humidity), 2) AS min_humidity,
    ROUND(MAX(humidity), 2) AS max_humidity,
    
    -- 异常检测
    SUM(CASE WHEN temperature > 50 OR temperature < -20 THEN 1 ELSE 0 END) AS temp_anomalies,
    SUM(CASE WHEN pressure > 400 OR pressure < 50 THEN 1 ELSE 0 END) AS pressure_anomalies
    
FROM enriched_sensor_readings  -- 使用关联后的数据
GROUP BY 
    location,
    zone,
    building,
    DATE_FORMAT(event_time, 'yyyy-MM-dd HH:00:00');

-- 查询区域统计
SELECT 
    location,
    building,
    hour_bucket,
    active_devices,
    total_readings,
    avg_temperature,
    avg_humidity,
    temp_anomalies,
    CASE 
        WHEN temp_anomalies > 0 THEN '⚠️ ANOMALY DETECTED'
        WHEN avg_temperature > 35 THEN '🔥 HIGH TEMP'
        WHEN avg_temperature < 5 THEN '❄️ LOW TEMP'
        ELSE '✅ NORMAL'
    END AS status
FROM zone_hourly_stats
ORDER BY hour_bucket DESC, location
LIMIT 30;

-- ----------------------------------------------------------------------------
-- 查询示例 4: 设备离线检测 (基于心跳缺失)
-- 检测可能离线的设备
-- ----------------------------------------------------------------------------
CREATE TEMPORARY VIEW device_offline_detection AS
WITH last_device_activity AS (
    SELECT 
        device_id,
        device_type,
        location,
        MAX(event_time) AS last_seen,
        COUNT(*) AS readings_in_last_10min
    FROM sensor_readings
    WHERE event_time > PROCTIME() - INTERVAL '10' MINUTE
    GROUP BY device_id, device_type, location
),
all_active_devices AS (
    SELECT DISTINCT device_id, device_type, location
    FROM sensor_readings
    WHERE event_time > PROCTIME() - INTERVAL '1' HOUR
)

SELECT 
    d.device_id,
    d.device_type,
    d.location,
    COALESCE(a.last_seen, 'NO_DATA') AS last_seen,
    COALESCE(a.readings_in_last_10min, 0) AS recent_readings,
    TIMESTAMPDIFF(MINUTE, a.last_seen, PROCTIME()) AS minutes_since_last_seen,
    CASE 
        WHEN a.last_seen IS NULL THEN 'OFFLINE_1H_PLUS'
        WHEN a.readings_in_last_10min = 0 THEN 'OFFLINE_10MIN'
        WHEN a.readings_in_last_10min < 3 THEN 'LOW_ACTIVITY'
        ELSE 'ONLINE'
    END AS connectivity_status
FROM all_active_devices d
LEFT JOIN last_device_activity a ON d.device_id = a.device_id
WHERE 
    a.last_seen IS NULL 
    OR a.readings_in_last_10min < 3;

-- 查询离线设备
SELECT 
    device_id,
    device_type,
    location,
    last_seen,
    recent_readings,
    minutes_since_last_seen,
    connectivity_status
FROM device_offline_detection
ORDER BY 
    CASE connectivity_status 
        WHEN 'OFFLINE_1H_PLUS' THEN 1
        WHEN 'OFFLINE_10MIN' THEN 2
        WHEN 'LOW_ACTIVITY' THEN 3
        ELSE 4
    END,
    minutes_since_last_seen DESC
LIMIT 30;

-- ----------------------------------------------------------------------------
-- 查询示例 5: 趋势分析和预测基础 (滑动窗口)
-- 计算温度变化趋势
-- ----------------------------------------------------------------------------
CREATE TEMPORARY VIEW temperature_trends AS
SELECT 
    device_id,
    device_type,
    location,
    
    -- 当前窗口 (最近5分钟)
    HOP_START(event_time, INTERVAL '1' MINUTE, INTERVAL '5' MINUTE) AS window_start,
    HOP_END(event_time, INTERVAL '1' MINUTE, INTERVAL '5' MINUTE) AS window_end,
    
    -- 当前统计
    AVG(temperature) AS current_avg_temp,
    STDDEV(temperature) AS temp_volatility,
    COUNT(*) AS sample_count,
    
    -- 延迟1分钟的窗口 (用于对比)
    LAG(AVG(temperature), 1) OVER (
        PARTITION BY device_id 
        ORDER BY HOP_START(event_time, INTERVAL '1' MINUTE, INTERVAL '5' MINUTE)
    ) AS prev_avg_temp,
    
    -- 延迟5分钟的窗口
    LAG(AVG(temperature), 5) OVER (
        PARTITION BY device_id 
        ORDER BY HOP_START(event_time, INTERVAL '1' MINUTE, INTERVAL '5' MINUTE)
    ) AS avg_temp_5min_ago

FROM sensor_readings
GROUP BY 
    device_id,
    device_type,
    location,
    HOP(event_time, INTERVAL '1' MINUTE, INTERVAL '5' MINUTE);

-- 查询温度趋势
SELECT 
    device_id,
    device_type,
    location,
    window_start,
    window_end,
    ROUND(current_avg_temp, 2) AS current_avg_temp,
    ROUND(prev_avg_temp, 2) AS prev_avg_temp,
    ROUND(avg_temp_5min_ago, 2) AS avg_temp_5min_ago,
    ROUND(current_avg_temp - prev_avg_temp, 2) AS temp_change_1min,
    ROUND(current_avg_temp - avg_temp_5min_ago, 2) AS temp_change_5min,
    ROUND(temp_volatility, 2) AS volatility,
    
    -- 趋势方向
    CASE 
        WHEN current_avg_temp - avg_temp_5min_ago > 2 THEN '📈 RISING_FAST'
        WHEN current_avg_temp - avg_temp_5min_ago > 0.5 THEN '📈 RISING'
        WHEN current_avg_temp - avg_temp_5min_ago < -2 THEN '📉 FALLING_FAST'
        WHEN current_avg_temp - avg_temp_5min_ago < -0.5 THEN '📉 FALLING'
        ELSE '➡️ STABLE'
    END AS trend_direction,
    
    -- 预警
    CASE 
        WHEN temp_volatility > 5 THEN 'HIGH_VOLATILITY'
        WHEN ABS(current_avg_temp - avg_temp_5min_ago) > 5 THEN 'RAPID_CHANGE'
        ELSE 'NORMAL'
    END AS alert_level
    
FROM temperature_trends
WHERE prev_avg_temp IS NOT NULL  -- 确保有对比数据
ORDER BY 
    CASE alert_level 
        WHEN 'HIGH_VOLATILITY' THEN 1
        WHEN 'RAPID_CHANGE' THEN 2
        ELSE 3
    END,
    ABS(temp_change_5min) DESC
LIMIT 40;

-- ----------------------------------------------------------------------------
-- 查询示例 6: 多维度聚合仪表板查询
-- 为Grafana仪表板提供数据
-- ----------------------------------------------------------------------------
CREATE TEMPORARY VIEW dashboard_metrics AS
SELECT 
    -- 时间维度
    TUMBLE_START(event_time, INTERVAL '1' MINUTE) AS time_bucket,
    
    -- 分组维度
    device_type,
    location,
    zone,
    
    -- 核心指标
    COUNT(DISTINCT device_id) AS unique_devices,
    COUNT(*) AS total_readings,
    
    -- 温度指标
    AVG(temperature) AS avg_temperature,
    MIN(temperature) AS min_temperature,
    MAX(temperature) AS max_temperature,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY temperature) AS median_temperature,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY temperature) AS p95_temperature,
    PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY temperature) AS p99_temperature,
    STDDEV(temperature) AS stddev_temperature,
    
    -- 数据质量指标
    SUM(CASE WHEN temperature IS NULL THEN 1 ELSE 0 END) AS missing_temp_count,
    SUM(CASE WHEN pressure IS NULL THEN 1 ELSE 0 END) AS missing_pressure_count,
    SUM(CASE WHEN humidity IS NULL THEN 1 ELSE 0 END) AS missing_humidity_count,
    
    -- 告警计数
    SUM(CASE WHEN temperature > 50 OR temperature < -20 THEN 1 ELSE 0 END) AS temp_alerts,
    SUM(CASE WHEN pressure > 400 OR pressure < 50 THEN 1 ELSE 0 END) AS pressure_alerts
    
FROM enriched_sensor_readings
GROUP BY 
    TUMBLE(event_time, INTERVAL '1' MINUTE),
    device_type,
    location,
    zone;

-- 仪表板数据源查询
SELECT 
    time_bucket,
    device_type,
    location,
    unique_devices,
    total_readings,
    ROUND(avg_temperature, 2) AS avg_temperature,
    ROUND(min_temperature, 2) AS min_temperature,
    ROUND(max_temperature, 2) AS max_temperature,
    ROUND(p95_temperature, 2) AS p95_temperature,
    ROUND(stddev_temperature, 2) AS stddev_temperature,
    temp_alerts + pressure_alerts AS total_alerts,
    missing_temp_count + missing_pressure_count + missing_humidity_count AS total_missing
FROM dashboard_metrics
ORDER BY time_bucket DESC, total_alerts DESC
LIMIT 50;

-- ----------------------------------------------------------------------------
-- 查询示例 7: 设备对比分析 (Top-N)
-- 找出最热/最冷的设备
-- ----------------------------------------------------------------------------
CREATE TEMPORARY VIEW device_ranking AS
SELECT 
    device_id,
    device_type,
    location,
    AVG(temperature) AS avg_temp,
    MAX(temperature) AS max_temp,
    COUNT(*) AS reading_count,
    
    -- 排名
    ROW_NUMBER() OVER (ORDER BY AVG(temperature) DESC) AS hottest_rank,
    ROW_NUMBER() OVER (ORDER BY AVG(temperature) ASC) AS coldest_rank
FROM sensor_readings
WHERE event_time > PROCTIME() - INTERVAL '10' MINUTE
GROUP BY device_id, device_type, location;

-- 最热的10个设备
SELECT 
    'HOTTEST' AS category,
    device_id,
    device_type,
    location,
    ROUND(avg_temp, 2) AS avg_temp,
    ROUND(max_temp, 2) AS max_temp,
    reading_count,
    hottest_rank AS rank
FROM device_ranking
WHERE hottest_rank <= 10
ORDER BY hottest_rank;

-- 最冷的10个设备
SELECT 
    'COLDEST' AS category,
    device_id,
    device_type,
    location,
    ROUND(avg_temp, 2) AS avg_temp,
    ROUND(max_temp, 2) AS max_temp,
    reading_count,
    coldest_rank AS rank
FROM device_ranking
WHERE coldest_rank <= 10
ORDER BY coldest_rank;
