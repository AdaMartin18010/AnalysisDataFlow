-- ============================================================================
-- 5G电信网络智能运维平台 - Flink SQL Sink表定义
-- 说明: 创建所有输出目标表
-- 执行: docker-compose exec flink-sql-client ./bin/sql-client.sh -f /opt/flink/sql-scripts/03_create_sinks.sql
-- ============================================================================

SET 'pipeline.name' = 'Telecom-Network-Sinks';

-- ============================================================================
-- 1. KPI聚合结果Sink (TimescaleDB)
-- ============================================================================
CREATE TABLE IF NOT EXISTS kpi_1min_sink (
    cell_id STRING,
    window_start TIMESTAMP(3),
    window_end TIMESTAMP(3),
    rsrp_avg DOUBLE,
    rsrp_min DOUBLE,
    rsrp_max DOUBLE,
    dl_throughput_avg DOUBLE,
    dl_throughput_peak DOUBLE,
    ul_throughput_avg DOUBLE,
    dl_prb_util_avg DOUBLE,
    dl_prb_util_peak DOUBLE,
    max_ue_count INT,
    avg_ue_count DOUBLE,
    ho_success_rate DOUBLE,
    call_drop_rate DOUBLE,
    cpu_util_peak DOUBLE,
    memory_util_peak DOUBLE,
    temperature_peak DOUBLE,
    total_samples BIGINT,
    PRIMARY KEY (cell_id, window_start) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/telecom',
    'table-name' = 'kpi_1min_aggregated',
    'username' = 'flink',
    'password' = 'flink_secure_2025',
    'driver' = 'org.postgresql.Driver',
    'sink.buffer-flush.max-rows' = '1000',
    'sink.buffer-flush.interval' = '5s',
    'sink.max-retries' = '3'
);

-- ============================================================================
-- 2. 异常告警Sink (JDBC + Kafka双写)
-- ============================================================================
CREATE TABLE IF NOT EXISTS kpi_alerts_jdbc (
    alert_id STRING,
    cell_id STRING,
    alert_type STRING,
    severity STRING,
    anomaly_score DOUBLE,
    rsrp_status STRING,
    throughput_status STRING,
    call_drop_status STRING,
    resource_status STRING,
    description STRING,
    event_time TIMESTAMP(3),
    PRIMARY KEY (alert_id) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/telecom',
    'table-name' = 'kpi_alerts',
    'username' = 'flink',
    'password' = 'flink_secure_2025',
    'driver' = 'org.postgresql.Driver'
);

CREATE TABLE IF NOT EXISTS kpi_alerts_kafka (
    alert_id STRING,
    cell_id STRING,
    alert_type STRING,
    severity STRING,
    anomaly_score DOUBLE,
    description STRING,
    event_time TIMESTAMP(3)
) WITH (
    'connector' = 'kafka',
    'topic' = 'telecom.alerts.generated',
    'properties.bootstrap.servers' = 'kafka-1:19092,kafka-2:19092,kafka-3:19092',
    'format' = 'json',
    'sink.partitioner' = 'round-robin'
);

-- ============================================================================
-- 3. 网络健康度评分Sink
-- ============================================================================
CREATE TABLE IF NOT EXISTS network_health_sink (
    window_start TIMESTAMP(3),
    city STRING,
    district STRING,
    health_score DOUBLE,
    coverage_score DOUBLE,
    retention_score DOUBLE,
    mobility_score DOUBLE,
    resource_score DOUBLE,
    health_level STRING,
    cell_count BIGINT,
    anomaly_cell_count BIGINT,
    anomaly_rate_pct DOUBLE,
    PRIMARY KEY (window_start, city, district) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/telecom',
    'table-name' = 'network_health_score',
    'username' = 'flink',
    'password' = 'flink_secure_2025',
    'driver' = 'org.postgresql.Driver'
);

-- ============================================================================
-- 4. 切片SLA监控Sink
-- ============================================================================
CREATE TABLE IF NOT EXISTS slice_sla_sink (
    slice_id STRING,
    slice_type STRING,
    tenant_id STRING,
    event_time TIMESTAMP(3),
    cpu_usage_pct DOUBLE,
    memory_usage_pct DOUBLE,
    bandwidth_usage_pct DOUBLE,
    latency_avg_ms DOUBLE,
    throughput_mbps DOUBLE,
    availability_pct DOUBLE,
    latency_status STRING,
    throughput_status STRING,
    availability_status STRING,
    sla_score INT,
    PRIMARY KEY (slice_id, event_time) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/telecom',
    'table-name' = 'slice_sla_monitor',
    'username' = 'flink',
    'password' = 'flink_secure_2025',
    'driver' = 'org.postgresql.Driver'
);

-- ============================================================================
-- 5. 自动扩缩容决策Sink (Kafka)
-- ============================================================================
CREATE TABLE IF NOT EXISTS auto_scaling_decisions (
    decision_id STRING,
    slice_id STRING,
    decision_type STRING,
    priority INT,
    current_replicas INT,
    target_replicas INT,
    trigger_metric STRING,
    trigger_value DOUBLE,
    threshold_value DOUBLE,
    reason STRING,
    confidence DOUBLE,
    created_at TIMESTAMP(3),
    executed_at TIMESTAMP(3),
    status STRING,
    PRIMARY KEY (decision_id) NOT ENFORCED
) WITH (
    'connector' = 'kafka',
    'topic' = 'telecom.scaling.decisions',
    'properties.bootstrap.servers' = 'kafka-1:19092,kafka-2:19092,kafka-3:19092',
    'format' = 'json'
);

-- ============================================================================
-- 6. 自愈动作决策Sink (JDBC)
-- ============================================================================
CREATE TABLE IF NOT EXISTS self_healing_actions (
    action_id STRING,
    trigger_event_id STRING,
    cell_id STRING,
    fault_type STRING,
    root_cause STRING,
    action_type STRING,
    action_params STRING,
    expected_duration INT,
    rollback_plan STRING,
    created_at TIMESTAMP(3),
    executed_at TIMESTAMP(3),
    completed_at TIMESTAMP(3),
    status STRING,
    result_message STRING,
    PRIMARY KEY (action_id) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/telecom',
    'table-name' = 'self_healing_actions',
    'username' = 'flink',
    'password' = 'flink_secure_2025',
    'driver' = 'org.postgresql.Driver'
);

-- ============================================================================
-- 7. 告警聚合面板Sink (Elasticsearch)
-- ============================================================================
CREATE TABLE IF NOT EXISTS alert_dashboard_sink (
    dashboard_time TIMESTAMP(3),
    total_alarms BIGINT,
    affected_network_elements BIGINT,
    critical_count BIGINT,
    major_count BIGINT,
    minor_count BIGINT,
    warning_count BIGINT,
    radio_alarms BIGINT,
    transport_alarms BIGINT,
    core_alarms BIGINT,
    infra_alarms BIGINT,
    root_cause_count BIGINT,
    avg_clear_time_minutes DOUBLE,
    PRIMARY KEY (dashboard_time) NOT ENFORCED
) WITH (
    'connector' = 'elasticsearch-7',
    'hosts' = 'http://elasticsearch:9200',
    'index' = 'telecom-alert-dashboard',
    'document-type' = '_doc',
    'format' = 'json'
);

-- ============================================================================
-- 8. 小时级性能报表Sink
-- ============================================================================
CREATE TABLE IF NOT EXISTS hourly_performance_sink (
    hour_bucket STRING,
    total_cells BIGINT,
    good_coverage_pct DOUBLE,
    acceptable_coverage_pct DOUBLE,
    avg_throughput_mbps DOUBLE,
    throughput_p5 DOUBLE,
    throughput_p95 DOUBLE,
    total_peak_users BIGINT,
    avg_users_per_cell DOUBLE,
    avg_call_drop_rate DOUBLE,
    max_call_drop_rate DOUBLE,
    avg_ho_success_rate DOUBLE,
    min_ho_success_rate DOUBLE,
    avg_prb_utilization DOUBLE,
    peak_prb_utilization DOUBLE,
    anomaly_count BIGINT,
    avg_anomaly_score DOUBLE,
    hour_of_day INT,
    PRIMARY KEY (hour_bucket) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/telecom',
    'table-name' = 'hourly_performance_report',
    'username' = 'flink',
    'password' = 'flink_secure_2025',
    'driver' = 'org.postgresql.Driver'
);

-- ============================================================================
-- 9. 切片计费数据Sink
-- ============================================================================
CREATE TABLE IF NOT EXISTS slice_billing_sink (
    slice_id STRING,
    tenant_id STRING,
    billing_hour STRING,
    slice_type STRING,
    cpu_peak_cores INT,
    memory_peak_gb DOUBLE,
    bandwidth_peak_mbps DOUBLE,
    cpu_core_hours DOUBLE,
    memory_gb_hours DOUBLE,
    data_volume_gb DOUBLE,
    sla_compliance_pct DOUBLE,
    min_availability_pct DOUBLE,
    peak_sessions INT,
    avg_sessions DOUBLE,
    total_session_success BIGINT,
    total_session_attempts BIGINT,
    estimated_charge_usd DOUBLE,
    PRIMARY KEY (slice_id, billing_hour) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/telecom',
    'table-name' = 'slice_billing_hourly',
    'username' = 'flink',
    'password' = 'flink_secure_2025',
    'driver' = 'org.postgresql.Driver'
);

-- ============================================================================
-- 验证表创建成功
-- ============================================================================
SHOW TABLES;
