-- ============================================================================
-- 5G电信网络智能运维平台 - Flink SQL Pipeline部署
-- 说明: 启动所有流处理作业
-- 执行: docker-compose exec flink-sql-client ./bin/sql-client.sh -f /opt/flink/sql-scripts/04_deploy_pipelines.sql
-- ============================================================================

SET 'pipeline.name' = 'Telecom-Network-Pipeline';
SET 'execution.checkpointing.interval' = '60s';
SET 'execution.checkpointing.min-pause' = '30s';
SET 'execution.checkpointing.max-concurrent-checkpoints' = '1';
SET 'state.backend' = 'rocksdb';
SET 'state.backend.incremental' = 'true';
SET 'restart-strategy' = 'fixed-delay';
SET 'restart-strategy.fixed-delay.attempts' = '10';
SET 'restart-strategy.fixed-delay.delay' = '30s';

-- ============================================================================
-- Pipeline 1: KPI实时聚合 (15s -> 1min)
-- ============================================================================
INSERT INTO kpi_1min_sink
SELECT
    cell_id,
    window_start,
    window_end,
    rsrp_avg,
    rsrp_min,
    rsrp_max,
    dl_throughput_avg,
    dl_throughput_peak,
    ul_throughput_avg,
    dl_prb_util_avg,
    dl_prb_util_peak,
    max_ue_count,
    avg_ue_count,
    ho_success_rate,
    call_drop_rate,
    cpu_util_peak,
    memory_util_peak,
    temperature_peak,
    total_samples
FROM kpi_1min_aggregated;

-- ============================================================================
-- Pipeline 2: 异常检测告警 (双写到JDBC和Kafka)
-- ============================================================================
INSERT INTO kpi_alerts_jdbc
SELECT
    CONCAT(cell_id, '-', CAST(window_start AS STRING)) as alert_id,
    cell_id,
    CASE 
        WHEN rsrp_status != 'NORMAL' THEN rsrp_status
        WHEN throughput_status != 'NORMAL' THEN throughput_status
        WHEN call_drop_status != 'NORMAL' THEN call_drop_status
        WHEN resource_status != 'NORMAL' THEN resource_status
        ELSE 'GENERAL_ANOMALY'
    END as alert_type,
    CASE 
        WHEN anomaly_score > 90 THEN 'CRITICAL'
        WHEN anomaly_score > 70 THEN 'MAJOR'
        WHEN anomaly_score > 50 THEN 'MINOR'
        ELSE 'WARNING'
    END as severity,
    anomaly_score,
    rsrp_status,
    throughput_status,
    call_drop_status,
    resource_status,
    CONCAT('Anomaly detected with score ', CAST(anomaly_score AS STRING)) as description,
    window_start as event_time
FROM anomaly_detection
WHERE anomaly_score > 50;

INSERT INTO kpi_alerts_kafka
SELECT
    CONCAT(cell_id, '-', CAST(window_start AS STRING)) as alert_id,
    cell_id,
    CASE 
        WHEN rsrp_status != 'NORMAL' THEN rsrp_status
        WHEN throughput_status != 'NORMAL' THEN throughput_status
        WHEN call_drop_status != 'NORMAL' THEN call_drop_status
        WHEN resource_status != 'NORMAL' THEN resource_status
        ELSE 'GENERAL_ANOMALY'
    END as alert_type,
    CASE 
        WHEN anomaly_score > 90 THEN 'CRITICAL'
        WHEN anomaly_score > 70 THEN 'MAJOR'
        WHEN anomaly_score > 50 THEN 'MINOR'
        ELSE 'WARNING'
    END as severity,
    CONCAT('Anomaly detected with score ', CAST(anomaly_score AS STRING)) as description,
    window_start as event_time
FROM anomaly_detection
WHERE anomaly_score > 50;

-- ============================================================================
-- Pipeline 3: 切片SLA监控
-- ============================================================================
INSERT INTO slice_sla_sink
SELECT
    slice_id,
    slice_type,
    tenant_id,
    event_time,
    cpu_usage_pct,
    memory_usage_pct,
    bandwidth_usage_pct,
    latency_avg_ms,
    throughput_mbps,
    availability_pct,
    latency_status,
    throughput_status,
    availability_status,
    sla_score
FROM slice_sla_monitor;

-- ============================================================================
-- Pipeline 4: 自动扩缩容决策
-- ============================================================================
INSERT INTO auto_scaling_decisions
SELECT
    CONCAT(slice_id, '-', CAST(event_time AS STRING)) as decision_id,
    slice_id,
    CASE
        WHEN cpu_usage_pct > 85 OR cpu_predicted_15min > 90 THEN 'SCALE_UP'
        WHEN active_sessions > session_threshold * 0.9 THEN 'SCALE_UP'
        WHEN cpu_usage_pct < 30 AND trend_status = 'STABLE' THEN 'SCALE_DOWN'
        ELSE 'MAINTAIN'
    END as decision_type,
    CASE
        WHEN cpu_usage_pct > 95 THEN 1
        WHEN cpu_usage_pct > 85 THEN 2
        ELSE 3
    END as priority,
    0 as current_replicas,
    CASE
        WHEN cpu_usage_pct > 95 THEN 2
        WHEN cpu_usage_pct > 85 THEN 1
        ELSE 0
    END as target_replicas,
    CASE 
        WHEN cpu_usage_pct > 85 THEN 'CPU_USAGE'
        WHEN active_sessions > session_threshold * 0.9 THEN 'SESSION_COUNT'
        ELSE 'LOAD_BALANCE'
    END as trigger_metric,
    cpu_usage_pct as trigger_value,
    85.0 as threshold_value,
    CONCAT('CPU:', CAST(ROUND(cpu_usage_pct, 2) AS STRING), '%, Trend:', trend_status) as reason,
    CASE 
        WHEN ABS(cpu_usage_pct - 50) > 30 THEN 0.9
        WHEN ABS(cpu_usage_pct - 50) > 20 THEN 0.7
        ELSE 0.5
    END as confidence,
    event_time as created_at,
    NULL as executed_at,
    'PENDING' as status
FROM slice_load_prediction
JOIN slice_sla_config ON slice_load_prediction.slice_id = slice_sla_config.slice_id
WHERE cpu_usage_pct > 80 OR cpu_usage_pct < 35;

-- ============================================================================
-- Pipeline 5: 自愈动作决策
-- ============================================================================
INSERT INTO self_healing_actions
SELECT
    CONCAT('HEAL-', cell_id, '-', CAST(window_start AS STRING)) as action_id,
    CONCAT('ANOMALY-', cell_id, '-', CAST(window_start AS STRING)) as trigger_event_id,
    cell_id,
    CASE 
        WHEN rsrp_status != 'NORMAL' THEN 'COVERAGE_DEGRADATION'
        WHEN call_drop_status != 'NORMAL' THEN 'CALL_QUALITY_DEGRADATION'
        WHEN resource_status = 'RESOURCE_EXHAUSTION' THEN 'RESOURCE_SATURATION'
        WHEN ho_status != 'NORMAL' THEN 'MOBILITY_FAILURE'
        ELSE 'GENERAL_DEGRADATION'
    END as fault_type,
    CONCAT(rsrp_status, '|', throughput_status, '|', resource_status) as root_cause,
    CASE 
        WHEN resource_status = 'RESOURCE_EXHAUSTION' AND cpu_util_peak > 95 THEN 'SCALE'
        WHEN call_drop_status = 'CALL_DROP_CRITICAL' AND ho_success_rate < 80 THEN 'RESTART'
        WHEN rsrp_status = 'RSRP_CRITICAL' THEN 'SWITCH'
        WHEN cpu_util_peak > 90 OR memory_util_peak > 90 THEN 'RESTART'
        ELSE 'ESCALATE'
    END as action_type,
    CASE 
        WHEN resource_status = 'RESOURCE_EXHAUSTION' THEN '{"scale_type": "horizontal", "delta": 1}'
        WHEN call_drop_status = 'CALL_DROP_CRITICAL' THEN '{"restart_type": "service", "target": "rrc_service"}'
        ELSE '{"escalation_level": "L2", "reason": "complex_fault"}'
    END as action_params,
    CASE 
        WHEN resource_status = 'RESOURCE_EXHAUSTION' THEN 180
        WHEN call_drop_status = 'CALL_DROP_CRITICAL' THEN 60
        ELSE 0
    END as expected_duration,
    CASE 
        WHEN resource_status = 'RESOURCE_EXHAUSTION' THEN 'scale_down_to_previous'
        WHEN call_drop_status = 'CALL_DROP_CRITICAL' THEN 'service_rollback'
        ELSE 'manual_intervention_required'
    END as rollback_plan,
    window_start as created_at,
    NULL as executed_at,
    NULL as completed_at,
    'PENDING' as status,
    NULL as result_message
FROM anomaly_detection
WHERE anomaly_score > 70
  AND (rsrp_status != 'NORMAL' 
       OR call_drop_status != 'NORMAL' 
       OR resource_status != 'NORMAL');

-- ============================================================================
-- Pipeline 6: 告警聚合面板 (到Elasticsearch)
-- ============================================================================
INSERT INTO alert_dashboard_sink
SELECT
    TUMBLE_START(event_time, INTERVAL '1' MINUTE) as dashboard_time,
    COUNT(*) as total_alarms,
    COUNT(DISTINCT ne_id) as affected_network_elements,
    SUM(CASE WHEN severity = 'CRITICAL' THEN 1 ELSE 0 END) as critical_count,
    SUM(CASE WHEN severity = 'MAJOR' THEN 1 ELSE 0 END) as major_count,
    SUM(CASE WHEN severity = 'MINOR' THEN 1 ELSE 0 END) as minor_count,
    SUM(CASE WHEN severity = 'WARNING' THEN 1 ELSE 0 END) as warning_count,
    SUM(CASE WHEN alarm_category = 'RADIO' THEN 1 ELSE 0 END) as radio_alarms,
    SUM(CASE WHEN alarm_category = 'TRANSPORT' THEN 1 ELSE 0 END) as transport_alarms,
    SUM(CASE WHEN alarm_category = 'CORE' THEN 1 ELSE 0 END) as core_alarms,
    SUM(CASE WHEN alarm_category = 'INFRA' THEN 1 ELSE 0 END) as infra_alarms,
    0 as root_cause_count,
    NULL as avg_clear_time_minutes
FROM network_alarms
GROUP BY TUMBLE(event_time, INTERVAL '1' MINUTE);

-- ============================================================================
-- 部署完成
-- ============================================================================
SELECT 'All pipelines deployed successfully!' as status;
