-- ============================================================================
-- 5G电信网络智能运维平台 - Flink SQL数据源定义
-- 说明: 创建所有Kafka源表和维度表
-- 执行: docker-compose exec flink-sql-client ./bin/sql-client.sh -f /opt/flink/sql-scripts/01_create_sources.sql
-- ============================================================================

-- 设置作业参数
SET 'pipeline.name' = 'Telecom-Network-Sources';
SET 'execution.checkpointing.interval' = '60s';
SET 'execution.checkpointing.min-pause' = '30s';
SET 'state.backend' = 'rocksdb';
SET 'state.backend.incremental' = 'true';
SET 'table.exec.mini-batch.enabled' = 'true';
SET 'table.exec.mini-batch.allow-latency' = '5s';
SET 'table.exec.mini-batch.size' = '5000';

-- ============================================================================
-- 1. 基站KPI数据源表
-- ============================================================================
CREATE TABLE IF NOT EXISTS base_station_kpi (
    -- 主键维度
    cell_id STRING COMMENT '小区ID, e.g., 460-00-1234567-1',
    gnb_id STRING COMMENT 'gNodeB ID',
    tac STRING COMMENT 'Tracking Area Code',
    plmn_id STRING COMMENT 'PLMN标识',
    
    -- 时间维度
    event_time TIMESTAMP(3) COMMENT '事件时间',
    report_period INT COMMENT '上报周期(秒)',
    
    -- 无线层指标 - 覆盖
    rsrp FLOAT COMMENT '参考信号接收功率(dBm), [-140,-44]',
    rsrq FLOAT COMMENT '参考信号接收质量(dB), [-20,-3]',
    sinr FLOAT COMMENT '信干噪比(dB), [-20,30]',
    rssinr FLOAT COMMENT 'RS SINR(dB)',
    
    -- 无线层指标 - 业务
    dl_prb_util FLOAT COMMENT '下行PRB利用率(%)',
    ul_prb_util FLOAT COMMENT '上行PRB利用率(%)',
    pdcch_util FLOAT COMMENT 'PDCCH利用率(%)',
    
    -- 吞吐量指标
    dl_throughput_mbps FLOAT COMMENT '下行吞吐量(Mbps)',
    ul_throughput_mbps FLOAT COMMENT '上行吞吐量(Mbps)',
    dl_cell_throughput_mbps FLOAT COMMENT '小区下行吞吐量',
    ul_cell_throughput_mbps FLOAT COMMENT '小区上行吞吐量',
    
    -- 用户面指标
    max_connected_ue INT COMMENT '最大连接用户数',
    avg_connected_ue FLOAT COMMENT '平均连接用户数',
    active_ue_dl INT COMMENT '下行激活用户数',
    active_ue_ul INT COMMENT '上行激活用户数',
    
    -- 移动性指标
    ho_attempts INT COMMENT '切换尝试次数',
    ho_success INT COMMENT '切换成功次数',
    ho_failures INT COMMENT '切换失败次数',
    
    -- 保持性指标
    erab_releases INT COMMENT 'E-RAB释放次数',
    erab_abnormal_releases INT COMMENT '异常释放次数',
    rrc_rejects INT COMMENT 'RRC拒绝次数',
    
    -- 资源指标
    cpu_util FLOAT COMMENT 'CPU利用率(%)',
    memory_util FLOAT COMMENT '内存利用率(%)',
    temperature FLOAT COMMENT '设备温度(°C)',
    
    -- Watermark: 允许10秒乱序
    WATERMARK FOR event_time AS event_time - INTERVAL '10' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'telecom.bs.kpi.raw',
    'properties.bootstrap.servers' = 'kafka-1:19092,kafka-2:19092,kafka-3:19092',
    'properties.group.id' = 'flink-kpi-processor',
    'properties.auto.offset.reset' = 'latest',
    'format' = 'json',
    'json.timestamp-format.standard' = 'ISO-8601',
    'json.ignore-parse-errors' = 'true',
    'json.fail-on-missing-field' = 'false'
);

-- ============================================================================
-- 2. 基站静态信息维度表 (JDBC)
-- ============================================================================
CREATE TABLE IF NOT EXISTS base_station_info (
    cell_id STRING,
    gnb_id STRING,
    cell_name STRING COMMENT '小区名称',
    city STRING COMMENT '所属城市',
    district STRING COMMENT '所属区县',
    address STRING COMMENT '详细地址',
    longitude FLOAT COMMENT '经度',
    latitude FLOAT COMMENT '纬度',
    altitude FLOAT COMMENT '海拔',
    vendor STRING COMMENT '设备厂商',
    band STRING COMMENT '频段',
    bandwidth_mhz INT COMMENT '带宽(MHz)',
    pci INT COMMENT '物理小区ID',
    azimuth INT COMMENT '方位角',
    downtilt INT COMMENT '下倾角',
    PRIMARY KEY (cell_id) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/telecom',
    'table-name' = 'base_station_info',
    'username' = 'flink',
    'password' = 'flink_secure_2025',
    'driver' = 'org.postgresql.Driver',
    'scan.fetch-size' = '1000',
    'lookup.cache.max-rows' = '10000',
    'lookup.cache.ttl' = '10min'
);

-- ============================================================================
-- 3. 网络切片性能数据表
-- ============================================================================
CREATE TABLE IF NOT EXISTS network_slice_kpi (
    slice_id STRING COMMENT '切片标识',
    slice_type STRING COMMENT 'eMBB/URLLC/mMTC',
    tenant_id STRING COMMENT '租户ID',
    nsi_id STRING COMMENT '网络切片实例ID',
    
    event_time TIMESTAMP(3),
    
    -- 资源使用
    cpu_cores_used INT COMMENT '使用CPU核数',
    cpu_cores_total INT COMMENT '总CPU核数',
    memory_gb_used FLOAT COMMENT '使用内存(GB)',
    memory_gb_total FLOAT COMMENT '总内存(GB)',
    bandwidth_mbps_used FLOAT COMMENT '使用带宽(Mbps)',
    bandwidth_mbps_total FLOAT COMMENT '总带宽(Mbps)',
    
    -- SLA指标
    latency_avg_ms FLOAT COMMENT '平均延迟(ms)',
    latency_p99_ms FLOAT COMMENT 'P99延迟(ms)',
    throughput_mbps FLOAT COMMENT '吞吐量(Mbps)',
    packet_loss_rate FLOAT COMMENT '丢包率(%)',
    jitter_ms FLOAT COMMENT '抖动(ms)',
    availability_pct FLOAT COMMENT '可用性(%)',
    
    -- 会话指标
    active_sessions INT COMMENT '活跃会话数',
    session_attempts INT COMMENT '会话尝试数',
    session_success INT COMMENT '会话成功数',
    
    WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'telecom.slice.kpi',
    'properties.bootstrap.servers' = 'kafka-1:19092,kafka-2:19092,kafka-3:19092',
    'properties.group.id' = 'flink-slice-processor',
    'format' = 'json',
    'json.ignore-parse-errors' = 'true'
);

-- ============================================================================
-- 4. 切片SLA配置维度表
-- ============================================================================
CREATE TABLE IF NOT EXISTS slice_sla_config (
    slice_id STRING,
    slice_type STRING,
    latency_sla_ms INT COMMENT '延迟SLA(ms)',
    throughput_sla_mbps INT COMMENT '吞吐量SLA(Mbps)',
    reliability_sla_pct FLOAT COMMENT '可靠性SLA(%)',
    availability_sla_pct FLOAT COMMENT '可用性SLA(%)',
    cpu_quota INT COMMENT 'CPU配额',
    memory_quota_gb INT COMMENT '内存配额(GB)',
    min_replicas INT COMMENT '最小副本数',
    max_replicas INT COMMENT '最大副本数',
    session_threshold INT COMMENT '会话数阈值',
    PRIMARY KEY (slice_id) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/telecom',
    'table-name' = 'slice_sla_config',
    'username' = 'flink',
    'password' = 'flink_secure_2025',
    'driver' = 'org.postgresql.Driver',
    'lookup.cache.max-rows' = '1000',
    'lookup.cache.ttl' = '5min'
);

-- ============================================================================
-- 5. 网络告警数据表
-- ============================================================================
CREATE TABLE IF NOT EXISTS network_alarms (
    alarm_id STRING COMMENT '告警唯一ID',
    alarm_seq BIGINT COMMENT '告警序列号',
    
    -- 告警来源
    ne_id STRING COMMENT '网元ID',
    ne_type STRING COMMENT '网元类型(gNB/AMF/UPF...)',
    ne_name STRING COMMENT '网元名称',
    location STRING COMMENT '物理位置',
    
    -- 告警分类
    alarm_type STRING COMMENT '告警类型',
    alarm_category STRING COMMENT '告警类别',
    severity STRING COMMENT '严重级别(CRITICAL/MAJOR/MINOR/WARNING)',
    probable_cause STRING COMMENT '可能原因',
    specific_problem STRING COMMENT '具体问题',
    
    -- 告警状态
    alarm_status STRING COMMENT '告警状态(ACTIVE/CLEARED)',
    ack_status STRING COMMENT '确认状态',
    
    -- 时间戳
    event_time TIMESTAMP(3) COMMENT '事件时间',
    first_occurrence TIMESTAMP(3) COMMENT '首次发生时间',
    cleared_time TIMESTAMP(3) COMMENT '清除时间',
    
    -- 附加信息
    additional_info STRING COMMENT '附加信息(JSON)',
    
    WATERMARK FOR event_time AS event_time - INTERVAL '15' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'telecom.alarms.raw',
    'properties.bootstrap.servers' = 'kafka-1:19092,kafka-2:19092,kafka-3:19092',
    'properties.group.id' = 'flink-alarm-processor',
    'format' = 'json',
    'json.ignore-parse-errors' = 'true'
);

-- ============================================================================
-- 6. 用户会话指标表 (可选，用于端到端SLA)
-- ============================================================================
CREATE TABLE IF NOT EXISTS user_session_metrics (
    ue_id STRING COMMENT '用户设备ID',
    slice_id STRING COMMENT '切片ID',
    session_id STRING COMMENT '会话ID',
    cell_id STRING COMMENT '服务小区',
    
    event_time TIMESTAMP(3),
    
    -- RAN侧指标
    ran_latency_ms FLOAT COMMENT 'RAN侧延迟',
    ran_throughput_mbps FLOAT COMMENT 'RAN侧吞吐量',
    rsrp FLOAT COMMENT 'RSRP(dBm)',
    
    -- 传输网指标
    transport_latency_ms FLOAT COMMENT '传输延迟',
    transport_packet_loss_pct FLOAT COMMENT '传输丢包率',
    transport_bandwidth_mbps FLOAT COMMENT '传输带宽',
    
    -- 核心网指标
    core_latency_ms FLOAT COMMENT '核心网延迟',
    upf_processing_time_ms FLOAT COMMENT 'UPF处理时间',
    upf_throughput_mbps FLOAT COMMENT 'UPF吞吐量',
    
    WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'telecom.user.session',
    'properties.bootstrap.servers' = 'kafka-1:19092,kafka-2:19092,kafka-3:19092',
    'properties.group.id' = 'flink-session-processor',
    'format' = 'json',
    'json.ignore-parse-errors' = 'true'
);

-- ============================================================================
-- 验证表创建成功
-- ============================================================================
SHOW TABLES;
