-- =====================================================
-- 02-irrigation-rules.sql
-- 绿野农场IoT平台 - 灌溉决策规则
-- =====================================================

-- ------------------------------------------------
-- 1. 土壤湿度分钟级聚合视图
-- ------------------------------------------------
CREATE VIEW soil_moisture_5min AS
SELECT
    Z.zone_id,
    Z.crop_type,
    Z.growth_stage,
    TUMBLE_START(S.event_time, INTERVAL '5' MINUTE) AS window_start,
    TUMBLE_END(S.event_time, INTERVAL '5' MINUTE) AS window_end,
    
    -- 湿度统计
    AVG(S.soil_moisture) AS avg_moisture,
    MIN(S.soil_moisture) AS min_moisture,
    MAX(S.soil_moisture) AS max_moisture,
    STDDEV_SAMP(S.soil_moisture) AS std_moisture,
    COUNT(*) AS reading_count,
    
    -- 温度统计
    AVG(S.soil_temperature) AS avg_temperature,
    
    -- 与阈值比较
    Z.moisture_critical,
    Z.moisture_target,
    Z.field_capacity,
    Z.wilting_point,
    CASE 
        WHEN AVG(S.soil_moisture) < Z.moisture_critical THEN 'CRITICAL'
        WHEN AVG(S.soil_moisture) < Z.moisture_target * 0.9 THEN 'WARNING'
        ELSE 'NORMAL'
    END AS moisture_status,
    
    -- 有效水分计算
    (AVG(S.soil_moisture) - Z.wilting_point) / 
        NULLIF(Z.field_capacity - Z.wilting_point, 0) AS aw_fraction,
    
    -- 趋势变化（与上一窗口比较）
    AVG(S.soil_moisture) - LAG(AVG(S.soil_moisture), 1) OVER (
        PARTITION BY Z.zone_id ORDER BY TUMBLE_END(S.event_time, INTERVAL '5' MINUTE)
    ) AS moisture_change,
    
    -- 数据质量标记
    CASE
        WHEN COUNT(*) < 2 THEN 'INSUFFICIENT_DATA'
        WHEN AVG(S.battery_level) < 20 THEN 'LOW_BATTERY'
        ELSE 'GOOD'
    END AS data_quality

FROM soil_sensor_stream S
JOIN zone_config FOR SYSTEM_TIME AS OF S.proctime AS Z
    ON S.zone_id = Z.zone_id

WHERE S.soil_moisture BETWEEN 0 AND 100
  AND S.soil_temperature BETWEEN -20 AND 60
  AND S.battery_level > 10

GROUP BY 
    Z.zone_id, Z.crop_type, Z.growth_stage,
    Z.moisture_critical, Z.moisture_target,
    Z.field_capacity, Z.wilting_point,
    TUMBLE(S.event_time, INTERVAL '5' MINUTE);

-- ------------------------------------------------
-- 2. 紧急灌溉触发（CEP模式检测）
-- ------------------------------------------------
INSERT INTO valve_commands
SELECT
    CONCAT('EMRG-', UUID()) AS command_id,
    V.valve_id,
    T.zone_id,
    'OPEN' AS command_type,
    V.max_flow_rate * 0.9 AS flow_rate_target,
    30 AS duration_minutes,
    CURRENT_TIMESTAMP AS scheduled_time,
    10 AS priority,
    CONCAT('Emergency: moisture ', CAST(ROUND(T.min_moisture, 1) AS STRING), 
           '% below critical ', CAST(T.moisture_critical AS STRING), '%') AS reason,
    CURRENT_TIMESTAMP AS created_at

FROM soil_moisture_5min T
JOIN valve_config V ON T.zone_id = V.zone_id

WHERE T.moisture_status = 'CRITICAL'
  AND T.reading_count >= 2
  AND T.data_quality = 'GOOD'
  -- 4小时内未触发过紧急灌溉
  AND NOT EXISTS (
      SELECT 1 FROM valve_commands C
      WHERE C.zone_id = T.zone_id
        AND C.command_type = 'OPEN'
        AND C.priority = 10
        AND C.created_at > CURRENT_TIMESTAMP - INTERVAL '4' HOUR
  );

-- ------------------------------------------------
-- 3. 定时灌溉调度（基于水分平衡）
-- ------------------------------------------------
INSERT INTO valve_commands
SELECT
    CONCAT('SCHD-', UUID()) AS command_id,
    V.valve_id,
    W.zone_id,
    'OPEN' AS command_type,
    V.max_flow_rate * 
        CASE 
            WHEN W.aw_fraction < 0.3 THEN 1.0
            WHEN W.aw_fraction < 0.5 THEN 0.8
            ELSE 0.6
        END AS flow_rate_target,
    -- 计算灌溉时长（根据亏缺量）
    GREATEST(15, CEIL(
        (Z.field_capacity * 0.8 - W.avg_moisture) * Z.area_ha * 100 / 
        (V.max_flow_rate * Z.application_efficiency * 60)
    )) AS duration_minutes,
    -- 最佳灌溉时间（夜间优先）
    CASE 
        WHEN EXTRACT(HOUR FROM CURRENT_TIMESTAMP) BETWEEN 19 AND 23
        THEN CURRENT_TIMESTAMP + INTERVAL '10' MINUTE
        WHEN EXTRACT(HOUR FROM CURRENT_TIMESTAMP) BETWEEN 0 AND 6
        THEN CURRENT_TIMESTAMP + INTERVAL '5' MINUTE
        ELSE DATE_TRUNC('day', CURRENT_TIMESTAMP + INTERVAL '1' DAY) + INTERVAL '20' HOUR
    END AS scheduled_time,
    5 AS priority,
    CONCAT('Scheduled: AW at ', CAST(ROUND(W.aw_fraction * 100, 1) AS STRING), 
           '%, refill to ', CAST(ROUND(Z.field_capacity * 0.8, 1) AS STRING), '%') AS reason,
    CURRENT_TIMESTAMP AS created_at

FROM (
    SELECT * FROM soil_moisture_5min
    WHERE window_end = (
        SELECT MAX(window_end) FROM soil_moisture_5min
    )
) W
JOIN zone_config Z ON W.zone_id = Z.zone_id
JOIN valve_config V ON W.zone_id = V.zone_id

WHERE W.moisture_status = 'WARNING'
  AND W.data_quality = 'GOOD'
  -- 12小时内无显著降雨预报（简化处理）
  AND NOT EXISTS (
      SELECT 1 FROM weather_stream WF
      WHERE WF.zone_id = W.zone_id
        AND WF.event_time > CURRENT_TIMESTAMP - INTERVAL '1' HOUR
        AND WF.precipitation_mm > 5
  )
  -- 6小时内未调度过
  AND NOT EXISTS (
      SELECT 1 FROM valve_commands C
      WHERE C.zone_id = W.zone_id
        AND C.priority = 5
        AND C.created_at > CURRENT_TIMESTAMP - INTERVAL '6' HOUR
  );

-- ------------------------------------------------
-- 4. 告警生成（设备离线）
-- ------------------------------------------------
INSERT INTO farm_alerts
SELECT
    CONCAT('DEV-', UUID()) AS alert_id,
    S.zone_id,
    'DEVICE' AS alert_type,
    'HIGH' AS severity,
    CONCAT('Sensor ', S.sensor_id, ' offline for > 30 minutes') AS message,
    CONCAT('Last seen: ', CAST(MAX(S.event_time) AS STRING)) AS details,
    CURRENT_TIMESTAMP AS created_at

FROM soil_sensor_stream S
GROUP BY S.sensor_id, S.zone_id
HAVING 
    MAX(S.event_time) < CURRENT_TIMESTAMP - INTERVAL '30' MINUTE
    AND COUNT(*) = 0;  -- 当前窗口无数据

-- ------------------------------------------------
-- 5. 告警生成（极端气象条件）
-- ------------------------------------------------
INSERT INTO farm_alerts
SELECT
    CONCAT('WTH-', UUID()) AS alert_id,
    W.zone_id,
    'WEATHER' AS alert_type,
    CASE 
        WHEN W.air_temperature > 38 THEN 'CRITICAL'
        WHEN W.air_temperature > 35 THEN 'HIGH'
        ELSE 'MEDIUM'
    END AS severity,
    CONCAT('Extreme temperature: ', CAST(ROUND(W.air_temperature, 1) AS STRING), '°C') AS message,
    CONCAT('Wind: ', CAST(ROUND(W.wind_speed, 1) AS STRING), ' m/s, ',
           'Humidity: ', CAST(ROUND(W.relative_humidity, 1) AS STRING), '%') AS details,
    W.event_time AS created_at

FROM weather_stream W
WHERE 
    W.air_temperature > 35  -- 高温告警
    OR W.wind_speed > 15     -- 大风告警
    OR W.precipitation_mm > 50;  -- 暴雨告警

-- ------------------------------------------------
-- 6. 时序数据写入InfluxDB
-- ------------------------------------------------
INSERT INTO soil_metrics_influx
SELECT
    zone_id,
    crop_type,
    window_end AS time,
    avg_moisture,
    min_moisture,
    max_moisture,
    std_moisture,
    reading_count
FROM soil_moisture_5min
WHERE data_quality = 'GOOD';

-- ------------------------------------------------
-- 7. 每日统计聚合（每小时更新）
-- ------------------------------------------------
INSERT INTO daily_irrigation_stats
SELECT
    DATE(T.window_time) AS stat_date,
    T.zone_id,
    MAX(T.crop_type) AS crop_type,
    COUNT(*) AS irrigation_count,
    SUM(T.duration_minutes) AS total_duration_min,
    SUM(T.water_volume_m3) AS total_water_m3,
    AVG(T.flow_rate) AS avg_flow_rate,
    SUM(T.energy_kwh) AS total_energy_kwh,
    SUM(T.water_volume_m3) / MAX(Z.area_ha) AS water_per_ha

FROM (
    SELECT
        zone_id,
        crop_type,
        TUMBLE_END(event_time, INTERVAL '1' HOUR) AS window_time,
        AVG(duration_minutes) AS duration_minutes,
        SUM(flow_rate_target * duration_minutes / 60) AS water_volume_m3,
        AVG(flow_rate_target) AS flow_rate,
        SUM(flow_rate_target * duration_minutes / 60 * 0.15) AS energy_kwh  -- 估算能耗
    FROM valve_commands
    WHERE command_type = 'OPEN'
    GROUP BY zone_id, crop_type, TUMBLE(event_time, INTERVAL '1' HOUR)
) T
JOIN zone_config Z ON T.zone_id = Z.zone_id

GROUP BY DATE(T.window_time), T.zone_id;

-- ------------------------------------------------
-- 8. 健康评分计算（简化版）
-- ------------------------------------------------
CREATE VIEW zone_health_score AS
SELECT
    M.zone_id,
    M.crop_type,
    M.window_end AS calculation_time,
    
    -- 水分健康得分 (0-100)
    GREATEST(0, LEAST(100, M.aw_fraction * 100)) AS water_score,
    
    -- 综合健康评分
    CASE
        WHEN M.moisture_status = 'CRITICAL' THEN 30
        WHEN M.moisture_status = 'WARNING' THEN 60
        WHEN M.aw_fraction > 0.8 THEN 90
        ELSE 75
    END AS overall_health,
    
    M.moisture_status,
    M.data_quality

FROM soil_moisture_5min M
WHERE M.window_end = (
    SELECT MAX(window_end) FROM soil_moisture_5min
);

-- 打印规则加载成功信息
SELECT 'Irrigation rules loaded successfully!' AS status;
