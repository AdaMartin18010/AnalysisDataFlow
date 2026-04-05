-- ============================================================================
-- 5G电信网络智能运维平台 - Flink SQL处理作业
-- 说明: 创建所有处理视图和中间结果表
-- 执行: docker-compose exec flink-sql-client ./bin/sql-client.sh -f /opt/flink/sql-scripts/02_create_processing_jobs.sql
-- ============================================================================

SET 'pipeline.name' = 'Telecom-Network-Processing';
SET 'execution.checkpointing.interval' = '60s';
SET 'state.backend' = 'rocksdb';
SET 'state.backend.incremental' = 'true';

-- ============================================================================
-- 阶段1: KPI数据清洗与标准化
-- ============================================================================
CREATE VIEW IF NOT EXISTS kpi_cleaned AS
SELECT
    -- 基础字段
    cell_id,
    gnb_id,
    tac,
    plmn_id,
    event_time,
    
    -- RSRP标准化: 有效范围[-140, -44] dBm
    CASE 
        WHEN rsrp IS NULL OR rsrp < -140 OR rsrp > -44 THEN NULL
        ELSE rsrp
    END as rsrp,
    
    -- RSRQ标准化: 有效范围[-20, -3] dB
    CASE 
        WHEN rsrq IS NULL OR rsrq < -20 OR rsrq > -3 THEN NULL
        ELSE rsrq
    END as rsrq,
    
    -- SINR标准化
    CASE 
        WHEN sinr IS NULL OR sinr < -20 THEN NULL
        ELSE sinr
    END as sinr,
    
    -- 利用率标准化到[0, 100]
    GREATEST(0, LEAST(100, dl_prb_util)) as dl_prb_util,
    GREATEST(0, LEAST(100, ul_prb_util)) as ul_prb_util,
    
    -- 吞吐量标准化 (去除异常大值)
    CASE 
        WHEN dl_throughput_mbps < 0 OR dl_throughput_mbps > 10000 THEN NULL
        ELSE dl_throughput_mbps
    END as dl_throughput_mbps,
    
    CASE 
        WHEN ul_throughput_mbps < 0 OR ul_throughput_mbps > 5000 THEN NULL
        ELSE ul_throughput_mbps
    END as ul_throughput_mbps,
    
    -- 用户数标准化
    GREATEST(0, max_connected_ue) as max_connected_ue,
    GREATEST(0, avg_connected_ue) as avg_connected_ue,
    
    -- 切换成功率计算
    CASE 
        WHEN ho_attempts > 0 
        THEN CAST(ho_success AS DOUBLE) / ho_attempts * 100
        ELSE 100.0
    END as ho_success_rate,
    
    -- 掉话率计算 (E-RAB异常释放率)
    CASE 
        WHEN erab_releases > 0 
        THEN CAST(erab_abnormal_releases AS DOUBLE) / erab_releases * 100
        ELSE 0.0
    END as call_drop_rate,
    
    -- 设备资源
    GREATEST(0, LEAST(100, cpu_util)) as cpu_util,
    GREATEST(0, LEAST(100, memory_util)) as memory_util,
    GREATEST(-40, LEAST(85, temperature)) as temperature
    
FROM base_station_kpi
WHERE cell_id IS NOT NULL 
  AND event_time IS NOT NULL;

-- ============================================================================
-- 阶段2: 15秒原始窗口聚合
-- ============================================================================
CREATE VIEW IF NOT EXISTS kpi_15s_aggregated AS
SELECT
    cell_id,
    TUMBLE_START(event_time, INTERVAL '15' SECOND) as window_start,
    TUMBLE_END(event_time, INTERVAL '15' SECOND) as window_end,
    
    -- RSRP统计
    COUNT(rsrp) as rsrp_count,
    AVG(rsrp) as rsrp_avg,
    MIN(rsrp) as rsrp_min,
    MAX(rsrp) as rsrp_max,
    STDDEV(rsrp) as rsrp_std,
    
    -- SINR统计
    AVG(sinr) as sinr_avg,
    MIN(sinr) as sinr_min,
    
    -- 吞吐量统计
    AVG(dl_throughput_mbps) as dl_throughput_avg,
    MAX(dl_throughput_mbps) as dl_throughput_max,
    SUM(dl_throughput_mbps) as dl_throughput_sum,
    AVG(ul_throughput_mbps) as ul_throughput_avg,
    
    -- PRB利用率
    AVG(dl_prb_util) as dl_prb_util_avg,
    MAX(dl_prb_util) as dl_prb_util_max,
    
    -- 用户数统计
    MAX(max_connected_ue) as max_ue_count,
    AVG(avg_connected_ue) as avg_ue_count,
    
    -- 质量指标
    MIN(ho_success_rate) as ho_success_rate_min,
    AVG(call_drop_rate) as call_drop_rate_avg,
    MAX(call_drop_rate) as call_drop_rate_max,
    
    -- 资源指标
    MAX(cpu_util) as cpu_util_max,
    MAX(memory_util) as memory_util_max,
    MAX(temperature) as temperature_max,
    
    -- 样本计数
    COUNT(*) as sample_count

FROM kpi_cleaned
GROUP BY cell_id, TUMBLE(event_time, INTERVAL '15' SECOND);

-- ============================================================================
-- 阶段3: 1分钟级联聚合
-- ============================================================================
CREATE VIEW IF NOT EXISTS kpi_1min_aggregated AS
SELECT
    cell_id,
    TUMBLE_START(window_end, INTERVAL '1' MINUTE) as window_start,
    TUMBLE_END(window_end, INTERVAL '1' MINUTE) as window_end,
    
    -- 加权平均 (按sample_count加权)
    SUM(rsrp_avg * sample_count) / SUM(sample_count) as rsrp_avg,
    MIN(rsrp_min) as rsrp_min,
    MAX(rsrp_max) as rsrp_max,
    
    -- 吞吐量
    SUM(dl_throughput_sum) / 4 as dl_throughput_avg,
    MAX(dl_throughput_max) as dl_throughput_peak,
    AVG(ul_throughput_avg) as ul_throughput_avg,
    
    -- PRB利用率
    AVG(dl_prb_util_avg) as dl_prb_util_avg,
    MAX(dl_prb_util_max) as dl_prb_util_peak,
    
    -- 用户数
    MAX(max_ue_count) as max_ue_count,
    AVG(avg_ue_count) as avg_ue_count,
    
    -- 切换成功率 (取最小值作为最差情况)
    MIN(ho_success_rate_min) as ho_success_rate,
    
    -- 掉话率 (取平均值)
    AVG(call_drop_rate_avg) as call_drop_rate,
    MAX(call_drop_rate_max) as call_drop_rate_peak,
    
    -- 资源峰值
    MAX(cpu_util_max) as cpu_util_peak,
    MAX(memory_util_max) as memory_util_peak,
    MAX(temperature_max) as temperature_peak,
    
    -- 时间特征
    HOUR(TUMBLE_START(window_end, INTERVAL '1' MINUTE)) as hour_of_day,
    DAYOFWEEK(TUMBLE_START(window_end, INTERVAL '1' MINUTE)) as day_of_week,
    
    -- 总计样本数
    SUM(sample_count) as total_samples

FROM kpi_15s_aggregated
GROUP BY cell_id, TUMBLE(window_end, INTERVAL '1' MINUTE);

-- ============================================================================
-- 阶段4: 15分钟业务粒度聚合
-- ============================================================================
CREATE VIEW IF NOT EXISTS kpi_15min_business AS
SELECT
    cell_id,
    TUMBLE_START(window_end, INTERVAL '15' MINUTE) as window_start,
    
    -- 无线覆盖质量
    AVG(rsrp_avg) as rsrp_avg,
    PERCENTILE(rsrp_avg, 0.05) as rsrp_p5,
    PERCENTILE(rsrp_avg, 0.95) as rsrp_p95,
    
    -- 业务体验
    AVG(dl_throughput_avg) as throughput_avg,
    MIN(dl_throughput_avg) as throughput_min,
    PERCENTILE(dl_throughput_avg, 0.50) as throughput_p50,
    
    -- 容量指标
    AVG(max_ue_count) as max_ue_avg,
    MAX(max_ue_count) as max_ue_peak,
    AVG(dl_prb_util_avg) as prb_util_avg,
    MAX(dl_prb_util_peak) as prb_util_peak,
    
    -- 质量评分 (综合指标)
    (AVG(ho_success_rate) * 0.3 + 
     (100 - AVG(call_drop_rate)) * 0.4 + 
     (CASE WHEN AVG(rsrp_avg) > -100 THEN 100 ELSE 50 END) * 0.3
    ) as quality_score,
    
    -- 负荷等级
    CASE 
        WHEN AVG(dl_prb_util_avg) > 80 THEN 'HIGH'
        WHEN AVG(dl_prb_util_avg) > 50 THEN 'MEDIUM'
        ELSE 'LOW'
    END as load_level,
    
    -- 网络健康度
    CASE 
        WHEN AVG(rsrp_avg) > -90 AND AVG(call_drop_rate) < 0.5 AND AVG(ho_success_rate) > 98 THEN 'EXCELLENT'
        WHEN AVG(rsrp_avg) > -100 AND AVG(call_drop_rate) < 1 AND AVG(ho_success_rate) > 95 THEN 'GOOD'
        WHEN AVG(rsrp_avg) > -110 AND AVG(call_drop_rate) < 2 THEN 'FAIR'
        ELSE 'POOR'
    END as network_health

FROM kpi_1min_aggregated
GROUP BY cell_id, TUMBLE(window_end, INTERVAL '15' MINUTE);

-- ============================================================================
-- 阶段5: 动态基线计算
-- ============================================================================
CREATE VIEW IF NOT EXISTS kpi_baseline AS
SELECT
    cell_id,
    hour_of_day,
    day_of_week,
    
    -- RSRP基线
    AVG(rsrp_avg) as rsrp_baseline_mean,
    STDDEV(rsrp_avg) as rsrp_baseline_std,
    PERCENTILE(rsrp_avg, 0.05) as rsrp_baseline_p5,
    PERCENTILE(rsrp_avg, 0.95) as rsrp_baseline_p95,
    
    -- 吞吐量基线
    AVG(dl_throughput_avg) as throughput_baseline_mean,
    STDDEV(dl_throughput_avg) as throughput_baseline_std,
    
    -- 用户数基线
    AVG(max_ue_count) as ue_baseline_mean,
    STDDEV(max_ue_count) as ue_baseline_std

FROM kpi_1min_aggregated
WHERE window_start >= NOW() - INTERVAL '7' DAY
GROUP BY cell_id, hour_of_day, day_of_week;

-- ============================================================================
-- 阶段6: 异常检测视图
-- ============================================================================
CREATE VIEW IF NOT EXISTS anomaly_detection AS
SELECT
    k.cell_id,
    k.window_start,
    k.rsrp_avg,
    k.dl_throughput_avg,
    k.max_ue_count,
    k.call_drop_rate,
    k.ho_success_rate,
    k.cpu_util_peak,
    k.memory_util_peak,
    k.dl_prb_util_peak,
    
    -- RSRP异常检测
    CASE 
        WHEN ABS(k.rsrp_avg - b.rsrp_baseline_mean) > 3 * b.rsrp_baseline_std 
             AND k.rsrp_avg < -110
        THEN 'RSRP_CRITICAL'
        WHEN ABS(k.rsrp_avg - b.rsrp_baseline_mean) > 2 * b.rsrp_baseline_std
        THEN 'RSRP_WARNING'
        ELSE 'NORMAL'
    END as rsrp_status,
    
    -- 吞吐量异常检测
    CASE 
        WHEN k.dl_throughput_avg < b.throughput_baseline_mean - 3 * b.throughput_baseline_std
             AND k.dl_prb_util_peak > 70
        THEN 'CONGESTION_SUSPECTED'
        WHEN k.dl_throughput_avg < b.throughput_baseline_mean * 0.5
        THEN 'THROUGHPUT_DEGRADED'
        ELSE 'NORMAL'
    END as throughput_status,
    
    -- 掉话率异常
    CASE 
        WHEN k.call_drop_rate > 5 THEN 'CALL_DROP_CRITICAL'
        WHEN k.call_drop_rate > 2 THEN 'CALL_DROP_WARNING'
        ELSE 'NORMAL'
    END as call_drop_status,
    
    -- 切换成功率异常
    CASE 
        WHEN k.ho_success_rate < 90 THEN 'HO_FAILURE_HIGH'
        ELSE 'NORMAL'
    END as ho_status,
    
    -- 设备资源异常
    CASE 
        WHEN k.cpu_util_peak > 90 OR k.memory_util_peak > 90 
        THEN 'RESOURCE_EXHAUSTION'
        WHEN k.temperature_max > 75 
        THEN 'TEMPERATURE_HIGH'
        ELSE 'NORMAL'
    END as resource_status,
    
    -- 综合异常评分 (0-100)
    LEAST(100, GREATEST(0,
        (CASE WHEN k.rsrp_avg < -110 THEN 30 ELSE 0 END) +
        (CASE WHEN k.call_drop_rate > 2 THEN 25 ELSE 0 END) +
        (CASE WHEN k.ho_success_rate < 95 THEN 20 ELSE 0 END) +
        (CASE WHEN k.cpu_util_peak > 85 THEN 15 ELSE 0 END) +
        (CASE WHEN k.dl_prb_util_peak > 80 THEN 10 ELSE 0 END)
    )) as anomaly_score

FROM kpi_1min_aggregated k
LEFT JOIN kpi_baseline b
    ON k.cell_id = b.cell_id
    AND k.hour_of_day = b.hour_of_day
    AND k.day_of_week = b.day_of_week;

-- ============================================================================
-- 阶段7: 告警风暴检测
-- ============================================================================
CREATE VIEW IF NOT EXISTS alarm_storm_detection AS
SELECT *
FROM network_alarms
MATCH_RECOGNIZE(
    PARTITION BY ne_id, alarm_category
    ORDER BY event_time
    MEASURES
        A.alarm_id as first_alarm_id,
        A.alarm_type as storm_type,
        COUNT(*) as storm_count,
        FIRST(A.event_time) as storm_start,
        LAST(B.event_time) as storm_end,
        COLLECT(DISTINCT B.severity) as severity_levels,
        COLLECT(DISTINCT B.probable_cause) as probable_causes
    ONE ROW PER MATCH
    AFTER MATCH SKIP PAST LAST ROW
    PATTERN (A B{3,})
    DEFINE
        A as A.severity IN ('CRITICAL', 'MAJOR'),
        B as B.event_time < A.event_time + INTERVAL '5' MINUTE
            AND (B.probable_cause = A.probable_cause 
                 OR B.alarm_type LIKE CONCAT(SUBSTRING(A.alarm_type, 1, 3), '%'))
)
WHERE storm_count >= 5;

-- ============================================================================
-- 阶段8: 根因告警识别
-- ============================================================================
CREATE VIEW IF NOT EXISTS root_cause_alarms AS
WITH alarm_impact AS (
    SELECT
        a.alarm_id,
        a.ne_id,
        a.alarm_type,
        a.probable_cause,
        a.event_time,
        a.severity,
        COUNT(b.alarm_id) as impacted_alarms,
        COLLECT(DISTINCT b.alarm_type) as impacted_types
    FROM network_alarms a
    LEFT JOIN network_alarms b
        ON a.ne_id = b.ne_id
        AND b.event_time BETWEEN a.event_time AND a.event_time + INTERVAL '5' MINUTE
        AND b.alarm_id != a.alarm_id
    WHERE a.severity IN ('CRITICAL', 'MAJOR')
      AND a.event_time >= NOW() - INTERVAL '1' HOUR
    GROUP BY a.alarm_id, a.ne_id, a.alarm_type, a.probable_cause, a.event_time, a.severity
)
SELECT
    alarm_id,
    ne_id,
    alarm_type,
    probable_cause,
    event_time,
    (impacted_alarms * 10 + 
     CASE severity 
        WHEN 'CRITICAL' THEN 50 
        WHEN 'MAJOR' THEN 30 
        ELSE 10 
     END +
     20 / (1 + UNIX_TIMESTAMP(NOW()) - UNIX_TIMESTAMP(event_time))
    ) as root_cause_score,
    impacted_alarms,
    CASE 
        WHEN (impacted_alarms * 10 + CASE severity WHEN 'CRITICAL' THEN 50 WHEN 'MAJOR' THEN 30 ELSE 10 END) > 200 
        THEN 'HIGH_LIKELIHOOD'
        WHEN (impacted_alarms * 10 + CASE severity WHEN 'CRITICAL' THEN 50 WHEN 'MAJOR' THEN 30 ELSE 10 END) > 100 
        THEN 'MEDIUM_LIKELIHOOD'
        ELSE 'LOW_LIKELIHOOD'
    END as root_cause_confidence
FROM alarm_impact
WHERE (impacted_alarms * 10 + CASE severity WHEN 'CRITICAL' THEN 50 WHEN 'MAJOR' THEN 30 ELSE 10 END) > 50
ORDER BY root_cause_score DESC;

-- ============================================================================
-- 阶段9: 切片SLA监控
-- ============================================================================
CREATE VIEW IF NOT EXISTS slice_sla_monitor AS
SELECT
    s.slice_id,
    s.slice_type,
    s.tenant_id,
    s.event_time,
    
    -- 资源使用率
    CAST(s.cpu_cores_used AS DOUBLE) / NULLIF(s.cpu_cores_total, 0) * 100 as cpu_usage_pct,
    s.memory_gb_used / NULLIF(s.memory_gb_total, 0) * 100 as memory_usage_pct,
    s.bandwidth_mbps_used / NULLIF(s.bandwidth_mbps_total, 0) * 100 as bandwidth_usage_pct,
    
    -- SLA指标
    s.latency_avg_ms,
    c.latency_sla_ms,
    s.throughput_mbps,
    c.throughput_sla_mbps,
    s.availability_pct,
    c.availability_sla_pct,
    s.active_sessions,
    c.session_threshold,
    
    -- SLA满足状态
    CASE 
        WHEN s.latency_avg_ms > c.latency_sla_ms THEN 'LATENCY_VIOLATION'
        ELSE 'LATENCY_OK'
    END as latency_status,
    
    CASE 
        WHEN s.throughput_mbps < c.throughput_sla_mbps * 0.9 THEN 'THROUGHPUT_VIOLATION'
        ELSE 'THROUGHPUT_OK'
    END as throughput_status,
    
    CASE 
        WHEN s.availability_pct < c.availability_sla_pct THEN 'AVAILABILITY_VIOLATION'
        ELSE 'AVAILABILITY_OK'
    END as availability_status,
    
    -- 综合SLA得分
    (
        CASE WHEN s.latency_avg_ms <= c.latency_sla_ms THEN 40 ELSE 0 END +
        CASE WHEN s.throughput_mbps >= c.throughput_sla_mbps * 0.9 THEN 35 ELSE 0 END +
        CASE WHEN s.availability_pct >= c.availability_sla_pct THEN 25 ELSE 0 END
    ) as sla_score

FROM network_slice_kpi s
JOIN slice_sla_config FOR SYSTEM_TIME AS OF s.event_time AS c
    ON s.slice_id = c.slice_id;

-- ============================================================================
-- 阶段10: 切片负载预测
-- ============================================================================
CREATE VIEW IF NOT EXISTS slice_load_prediction AS
WITH slice_trend AS (
    SELECT
        slice_id,
        event_time,
        cpu_usage_pct,
        memory_usage_pct,
        bandwidth_usage_pct,
        active_sessions,
        cpu_usage_pct - LAG(cpu_usage_pct, 12) OVER (
            PARTITION BY slice_id ORDER BY event_time
        ) as cpu_delta_1h,
        AVG(cpu_usage_pct) OVER (
            PARTITION BY slice_id 
            ORDER BY event_time 
            ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
        ) as cpu_ma5,
        cpu_usage_pct + (cpu_usage_pct - LAG(cpu_usage_pct, 4) OVER (
            PARTITION BY slice_id ORDER BY event_time
        )) as cpu_predicted_15min
    FROM slice_sla_monitor
)
SELECT
    slice_id,
    event_time,
    cpu_usage_pct,
    cpu_ma5,
    cpu_predicted_15min,
    CASE 
        WHEN cpu_predicted_15min > 90 THEN 'CRITICAL_PREDICTED'
        WHEN cpu_predicted_15min > 80 THEN 'WARNING_PREDICTED'
        WHEN cpu_delta_1h > 20 THEN 'RAPID_INCREASE'
        WHEN cpu_delta_1h < -20 THEN 'RAPID_DECREASE'
        ELSE 'STABLE'
    END as trend_status
FROM slice_trend;

-- ============================================================================
-- 验证视图创建成功
-- ============================================================================
SHOW VIEWS;
