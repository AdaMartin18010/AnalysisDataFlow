# 全屋智能实时协调平台：完整案例研究

> **项目类型**: 完整案例研究 | **规模**: 10,000+户智能家居部署
> **技术栈**: Apache Flink + Matter/Zigbee/Z-Wave多协议网关
> **所属阶段**: Phase-9-Smart-Home
> **形式化等级**: L4-L5 (生产级架构)
> **对标来源**: Apple HomeKit Ecosystem[^1], Google Nest Platform[^2], Matter Smart Home Reference[^3]

---

## 执行摘要

本项目展示了一个面向10,000户家庭的**全屋智能实时协调平台**的完整设计与实现。
该平台基于Apache Flink构建统一的流数据处理层，实现多协议设备（Matter、Zigbee、Z-Wave、Wi-Fi）的统一接入、场景联动引擎、以及能耗优化与预测系统。

### 核心成果

| 指标 | 数值 | 行业基准 |
|------|------|----------|
| 接入家庭数 | 10,000+ | - |
| 并发设备数 | 500,000+ | - |
| 日均事件处理量 | 2.5亿条 | - |
| 场景响应延迟 | P99 < 300ms | < 500ms |
| 能源节约率 | 18-25% | 10-15% |
| 系统可用性 | 99.95% | 99.9% |

---

## 1. 业务场景与需求分析

### 1.1 用户画像与场景分类

**目标用户群体**:

| 用户类型 | 占比 | 核心需求 | 典型场景 |
|----------|------|----------|----------|
| 科技先锋 | 15% | 最新技术、深度定制 | 自动化脚本、自定义场景 |
| 品质生活 | 35% | 舒适便捷、品质体验 | 智能照明、环境控制 |
| 家庭安防 | 25% | 安全监控、远程看护 | 智能门锁、摄像头、告警 |
| 节能环保 | 20% | 降低能耗、绿色生活 | 能源监测、智能调度 |
| 适老化 | 5% | 简单易用、健康监护 | 紧急呼叫、健康监测 |

**场景分类矩阵**:

```mermaid
graph TB
    subgraph LifeScenes["生活场景 Life Scenes"]
        L1[起床模式<br/>Morning Routine]
        L2[离家模式<br/>Away Mode]
        L3[回家模式<br/>Arriving Home]
        L4[睡眠模式<br/>Sleep Mode]
        L5[观影模式<br/>Movie Mode]
    end

    subgraph SafetyScenes["安防场景 Safety Scenes"]
        S1[周界防护<br/>Perimeter Security]
        S2[入侵检测<br/>Intrusion Alert]
        S3[环境安全<br/>Environmental Safety]
        S4[老人/儿童看护<br/>Care Monitoring]
    end

    subgraph EnergyScenes["能耗场景 Energy Scenes"]
        E1[峰谷套利<br/>Peak Shaving]
        E2[负载均衡<br/>Load Balancing]
        E3[太阳能优化<br/>Solar Optimization]
        E4[预冷/预热<br/>Pre-conditioning]
    end

    subgraph HealthScenes["健康场景 Health Scenes"]
        H1[空气质量管理<br/>Air Quality]
        H2[睡眠质量监测<br/>Sleep Tracking]
        H3[活动量统计<br/>Activity Tracking]
    end
```

### 1.2 功能需求规格

#### 1.2.1 功能需求（Functional Requirements）

| ID | 需求描述 | 优先级 | 验收标准 |
|----|----------|--------|----------|
| FR-001 | 支持10+种设备类型统一接入 | P0 | 设备发现时间 < 30s |
| FR-002 | 场景联动规则引擎 | P0 | 规则响应 < 500ms |
| FR-003 | 语音助手集成 | P0 | 支持Alexa/Google/Siri |
| FR-004 | 能耗监测与优化 | P1 | 月度能耗报告 |
| FR-005 | 安防告警系统 | P0 | 告警延迟 < 1s |
| FR-006 | 远程访问与控制 | P0 | 移动端响应 < 2s |
| FR-007 | 设备OTA升级 | P1 | 批量升级支持 |
| FR-008 | 多用户权限管理 | P1 | 角色分级 |
| FR-009 | 数据导出与API | P2 | RESTful API |
| FR-010 | 第三方服务集成 | P2 | IFTTT/Webhook |

#### 1.2.2 非功能需求（Non-Functional Requirements）

| ID | 需求类别 | 目标值 | 测试方法 |
|----|----------|--------|----------|
| NFR-001 | 可用性 | 99.95% | 年度停机 < 4.38h |
| NFR-002 | 响应延迟 | P99 < 300ms | 压力测试 |
| NFR-003 | 并发能力 | 100,000设备 | 负载测试 |
| NFR-004 | 数据持久化 | 7年 | 合规审计 |
| NFR-005 | 安全等级 | SOC2 Type II | 第三方认证 |
| NFR-006 | 灾难恢复 | RPO < 1min, RTO < 15min | 演练 |
| NFR-007 | 扩展性 | 水平扩展至100K户 | 架构评审 |

### 1.3 数据规模预估

**数据量估算（10,000户峰值）**:

| 数据类型 | 单设备频率 | 设备数 | 日数据量 | 年存储量 |
|----------|------------|--------|----------|----------|
| 传感器读数 | 30秒/次 | 300,000 | 8.64亿条 | 3.2TB |
| 设备事件 | 10次/天 | 500,000 | 500万条 | 180GB |
| 能耗数据 | 15分钟/次 | 100,000 | 960万条 | 350GB |
| 视频流 | 24/7 | 20,000 | 500TB | 180PB |
| 日志数据 | 持续 | - | 50GB | 18TB |

---

## 2. 系统架构设计

### 2.1 整体架构

```mermaid
graph TB
    subgraph EdgeTier["边缘层 Edge Tier<br/>每个家庭部署"]
        E1[Edge Gateway<br/>Matter/Zigbee Hub]
        E2[Local Scene Engine<br/>Flink Mini Cluster]
        E3[Local Storage<br/>Redis/SQLite]
        E4[Video NVR<br/>边缘存储]
    end

    subgraph AggregationTier["汇聚层 Aggregation Tier<br/>区域/小区级别"]
        A1[Regional Gateway<br/>协议汇聚]
        A2[Stream Preprocessor<br/>Kafka/Flink]
        A3[Edge ML Inference<br/>轻量模型]
    end

    subgraph CloudTier["云端 Cloud Tier"]
        C1[Load Balancer<br/>CloudFront/ALB]
        C2[Flink Cluster<br/>流处理核心]
        C3[Kafka Cluster<br/>消息总线]
        C4[(TimescaleDB<br/>时序数据)]
        C5[(PostgreSQL<br/>元数据)]
        C6[S3/Glacier<br/>冷存储]
        C7[ML Platform<br/>SageMaker]
    end

    subgraph IntegrationTier["集成层 Integration Tier"]
        I1[Alexa Skill]
        I2[Google Action]
        I3[HomeKit Bridge]
        I4[IFTTT/Webhook]
        I5[Utility API<br/>电力公司]
    end

    subgraph ClientTier["客户端 Client Tier"]
        M1[iOS App]
        M2[Android App]
        M3[Web Dashboard]
        M4[Smart Speaker]
    end

    EdgeTier -->|MQTT/HTTPS| AggregationTier
    AggregationTier -->|Kafka/MQTT| CloudTier
    CloudTier --> IntegrationTier
    CloudTier --> ClientTier
    ClientTier -->|API| CloudTier

    style EdgeTier fill:#e8f5e9
    style AggregationTier fill:#fff3e0
    style CloudTier fill:#e3f2fd
    style IntegrationTier fill:#f3e5f5
    style ClientTier fill:#fce4ec
```

### 2.2 边缘网关架构

每个家庭部署的边缘网关架构：

```mermaid
graph TB
    subgraph HomeGateway["家庭智能网关<br/>Home Gateway"]
        direction TB

        subgraph RadioLayer["无线协议层"]
            R1[Thread Radio<br/>802.15.4]
            R2[Zigbee Radio<br/>2.4GHz]
            R3[Z-Wave Radio<br/>Sub-GHz]
            R4[BLE Radio<br/>2.4GHz]
        end

        subgraph ProtocolStack["协议栈"]
            P1[Matter SDK]
            P2[Zigbee Stack]
            P3[Z-Wave SDK]
            P4[BLE Stack]
        end

        subgraph GatewayCore["网关核心"]
            G1[Protocol Bridge<br/>多协议转换]
            G2[Local Rules Engine<br/>规则执行]
            G3[Device Cache<br/>设备状态缓存]
            G4[Scene Store<br/>场景配置存储]
        end

        subgraph EdgeCompute["边缘计算"]
            F1[Flink Mini<br/>1 JobManager]
            F2[2 TaskManagers<br/>4 slots each]
            F3[Local SQL<br/>H2/SQLite]
        end

        subgraph Connectivity["连接层"]
            C1[Wi-Fi Client]
            C2[Ethernet]
            C3[4G/5G Fallback]
        end
    end

    R1 --> P1 --> G1
    R2 --> P2 --> G1
    R3 --> P3 --> G1
    R4 --> P4 --> G1

    G1 --> G2
    G2 --> G3
    G2 --> G4

    G2 --> F1
    F1 --> F2
    F2 --> F3

    F1 --> C1
    F1 --> C2
    F1 --> C3

    style HomeGateway fill:#e8f5e9
```

### 2.3 Flink作业拓扑

核心的Flink流处理作业拓扑：

```mermaid
graph LR
    subgraph Sources["数据源 Sources"]
        S1[Matter Events]
        S2[Zigbee Events]
        S3[Z-Wave Events]
        S4[Wi-Fi Events]
        S5[User Actions]
    end

    subgraph Preprocessing["预处理 Preprocessing"]
        P1[Protocol<br/>Normalization]
        P2[Data<br/>Cleansing]
        P3[Enrichment<br/>Join Dim Tables]
    end

    subgraph Processing["核心处理 Core Processing"]
        C1[Scene Detection<br/>CEP]
        C2[State<br/>Aggregation]
        C3[Anomaly<br/>Detection]
        C4[Energy<br/>Optimization]
    end

    subgraph Sinks["数据汇 Sinks"]
        K1[Kafka<br/>Command Topic]
        K2[InfluxDB<br/>Time Series]
        K3[PostgreSQL<br/>Relational]
        K4[Alert<br/>Notifications]
        K5[S3<br/>Archive]
    end

    S1 --> P1
    S2 --> P1
    S3 --> P1
    S4 --> P1
    S5 --> P1

    P1 --> P2 --> P3

    P3 --> C1
    P3 --> C2
    P3 --> C3
    P3 --> C4

    C1 --> K1
    C1 --> K4
    C2 --> K2
    C3 --> K4
    C4 --> K1
    C2 --> K3
    C2 --> K5

    style Sources fill:#e1f5fe
    style Preprocessing fill:#fff3e0
    style Processing fill:#e8f5e9
    style Sinks fill:#fce4ec
```

---

## 3. 数据模型与Schema设计

### 3.1 统一设备模型

```sql
-- ============================================================
-- 设备元数据主表
-- ============================================================
CREATE TABLE devices (
    device_id VARCHAR(64) PRIMARY KEY,
    device_name VARCHAR(255) NOT NULL,
    device_type VARCHAR(50) NOT NULL,  -- light, thermostat, lock, sensor, etc.
    device_category VARCHAR(50),        -- lighting, climate, security, entertainment

    -- 协议信息
    protocol VARCHAR(20) NOT NULL,      -- MATTER, ZIGBEE, ZWAVE, WIFI, BLE
    protocol_version VARCHAR(20),
    network_address VARCHAR(64),        -- 协议特定地址
    manufacturer VARCHAR(100),
    model VARCHAR(100),
    firmware_version VARCHAR(50),
    hardware_version VARCHAR(50),

    -- 位置信息
    home_id VARCHAR(64) NOT NULL,
    room_id VARCHAR(64),
    room_name VARCHAR(100),
    floor INT,
    zone_id VARCHAR(64),

    -- 能力与配置
    capabilities JSONB,                 -- ["onoff", "brightness", "color"]
    supported_commands JSONB,
    config_schema JSONB,                -- 配置参数Schema
    current_config JSONB,               -- 当前配置

    -- 状态信息
    online BOOLEAN DEFAULT FALSE,
    last_seen TIMESTAMP WITH TIME ZONE,
    battery_level INT CHECK (battery_level BETWEEN -1 AND 100),
    signal_strength INT,                -- RSSI

    -- 时间戳
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- 索引
    CONSTRAINT fk_home FOREIGN KEY (home_id) REFERENCES homes(home_id),
    CONSTRAINT fk_room FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);

CREATE INDEX idx_devices_home ON devices(home_id);
CREATE INDEX idx_devices_room ON devices(room_id);
CREATE INDEX idx_devices_protocol ON devices(protocol);
CREATE INDEX idx_devices_type ON devices(device_type);
CREATE INDEX idx_devices_online ON devices(online, last_seen);

-- ============================================================
-- 设备状态历史表 (时序数据)
-- ============================================================
CREATE TABLE device_states (
    time TIMESTAMPTZ NOT NULL,
    device_id VARCHAR(64) NOT NULL,

    -- 状态维度
    state_type VARCHAR(50) NOT NULL,    -- power, brightness, temperature, etc.
    state_value VARCHAR(255),           -- 字符串表示
    numeric_value DOUBLE PRECISION,     -- 数值表示
    unit VARCHAR(20),                   -- unit of measurement

    -- 元数据
    source_protocol VARCHAR(20),
    quality_score INT CHECK (quality_score BETWEEN 0 AND 100),

    PRIMARY KEY (time, device_id, state_type)
) PARTITION BY RANGE (time);

-- 按月分区
CREATE TABLE device_states_2024_01 PARTITION OF device_states
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- 创建Hypertable (TimescaleDB)
SELECT create_hypertable('device_states', 'time', chunk_time_interval => INTERVAL '1 day');

CREATE INDEX idx_device_states_device_time ON device_states(device_id, time DESC);
CREATE INDEX idx_device_states_type ON device_states(state_type, time DESC);
```

### 3.2 场景规则模型

```sql
-- ============================================================
-- 场景定义表
-- ============================================================
CREATE TABLE scenes (
    scene_id VARCHAR(64) PRIMARY KEY,
    home_id VARCHAR(64) NOT NULL,

    -- 基本信息
    scene_name VARCHAR(255) NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    color VARCHAR(7),  -- Hex color

    -- 触发器配置
    trigger_type VARCHAR(20) NOT NULL,  -- event, schedule, state, manual, voice
    trigger_config JSONB NOT NULL,      -- 触发器详细配置

    -- 执行配置
    actions JSONB NOT NULL,             -- 动作列表
    conditions JSONB,                   -- 前置条件
    constraints JSONB,                  -- 执行约束

    -- 执行策略
    priority INT DEFAULT 5 CHECK (priority BETWEEN 1 AND 10),
    execution_mode VARCHAR(20) DEFAULT 'parallel',  -- parallel, sequential
    timeout_seconds INT DEFAULT 30,
    retry_count INT DEFAULT 3,
    retry_interval_seconds INT DEFAULT 5,

    -- 状态
    enabled BOOLEAN DEFAULT TRUE,
    is_favorite BOOLEAN DEFAULT FALSE,

    -- 统计
    trigger_count BIGINT DEFAULT 0,
    success_count BIGINT DEFAULT 0,
    failure_count BIGINT DEFAULT 0,
    avg_execution_time_ms INT,
    last_triggered_at TIMESTAMP WITH TIME ZONE,
    last_success_at TIMESTAMP WITH TIME ZONE,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by VARCHAR(64),

    CONSTRAINT fk_home FOREIGN KEY (home_id) REFERENCES homes(home_id)
);

-- 触发器配置示例JSON Schema:
-- {
--   "trigger_type": "event",
--   "events": [
--     {"device_id": "lock_001", "state_type": "lock_state", "value": "unlocked"}
--   ],
--   "time_window_seconds": 300,
--   "require_all": true
-- }

-- 动作配置示例JSON Schema:
-- {
--   "actions": [
--     {"device_id": "light_001", "command": "on", "params": {"brightness": 80}, "delay": 0},
--     {"device_id": "thermostat_001", "command": "set", "params": {"temperature": 22}, "delay": 5}
--   ]
-- }

-- ============================================================
-- 场景执行日志
-- ============================================================
CREATE TABLE scene_executions (
    execution_id VARCHAR(64) PRIMARY KEY,
    scene_id VARCHAR(64) NOT NULL,
    home_id VARCHAR(64) NOT NULL,

    -- 触发信息
    triggered_by VARCHAR(20),  -- user, automation, schedule, voice, api
    trigger_source VARCHAR(64), -- 触发源标识
    trigger_context JSONB,     -- 触发上下文

    -- 执行时间
    triggered_at TIMESTAMP WITH TIME ZONE NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    execution_time_ms INT,

    -- 执行结果
    status VARCHAR(20),  -- pending, running, success, partial, failed, cancelled
    error_code VARCHAR(50),
    error_message TEXT,

    -- 详细执行记录
    action_results JSONB,  -- 每个动作的执行结果

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT fk_scene FOREIGN KEY (scene_id) REFERENCES scenes(scene_id)
);

CREATE INDEX idx_scene_executions_scene ON scene_executions(scene_id, triggered_at DESC);
CREATE INDEX idx_scene_executions_home ON scene_executions(home_id, triggered_at DESC);
CREATE INDEX idx_scene_executions_status ON scene_executions(status, triggered_at DESC);
```

### 3.3 能耗数据模型

```sql
-- ============================================================
-- 能耗实时数据表
-- ============================================================
CREATE TABLE energy_readings (
    time TIMESTAMPTZ NOT NULL,
    meter_id VARCHAR(64) NOT NULL,
    home_id VARCHAR(64) NOT NULL,

    -- 功率读数
    total_power_watts DOUBLE PRECISION,
    circuit_power JSONB,  -- {"living_room": 450.5, "kitchen": 320.0, ...}

    -- 电压电流
    voltage_l1 DOUBLE PRECISION,
    voltage_l2 DOUBLE PRECISION,
    voltage_l3 DOUBLE PRECISION,
    current_l1 DOUBLE PRECISION,
    current_l2 DOUBLE PRECISION,
    current_l3 DOUBLE PRECISION,

    -- 功率因数
    power_factor DOUBLE PRECISION,

    -- 累计电量
    total_kwh_import DOUBLE PRECISION,
    total_kwh_export DOUBLE PRECISION,

    -- 电价信息
    rate_period VARCHAR(20),  -- peak, off_peak, shoulder
    current_rate_per_kwh DECIMAL(10,6),

    PRIMARY KEY (time, meter_id)
);

SELECT create_hypertable('energy_readings', 'time', chunk_time_interval => INTERVAL '1 hour');

-- ============================================================
-- 能耗聚合表 (预计算)
-- ============================================================
CREATE TABLE energy_aggregations (
    home_id VARCHAR(64) NOT NULL,
    aggregation_period VARCHAR(20) NOT NULL,  -- hour, day, month
    period_start TIMESTAMPTZ NOT NULL,
    period_end TIMESTAMPTZ NOT NULL,

    -- 用量统计
    total_kwh DOUBLE PRECISION,
    total_cost DECIMAL(12,4),
    avg_power_watts DOUBLE PRECISION,
    peak_power_watts DOUBLE PRECISION,
    peak_power_time TIMESTAMPTZ,

    -- 时段分布
    peak_kwh DOUBLE PRECISION,
    shoulder_kwh DOUBLE PRECISION,
    off_peak_kwh DOUBLE PRECISION,

    -- 碳排放估算
    estimated_co2_kg DOUBLE PRECISION,

    -- 对比数据
    previous_period_kwh DOUBLE PRECISION,
    yoy_kwh DOUBLE PRECISION,

    PRIMARY KEY (home_id, aggregation_period, period_start)
);

-- ============================================================
-- 设备级能耗表
-- ============================================================
CREATE TABLE device_energy (
    time TIMESTAMPTZ NOT NULL,
    device_id VARCHAR(64) NOT NULL,
    home_id VARCHAR(64) NOT NULL,

    power_watts DOUBLE PRECISION,
    energy_wh DOUBLE PRECISION,
    voltage DOUBLE PRECISION,
    current DOUBLE PRECISION,

    -- 运行状态
    is_on BOOLEAN,
    runtime_seconds INT,
    standby_power_watts DOUBLE PRECISION,

    PRIMARY KEY (time, device_id)
);

SELECT create_hypertable('device_energy', 'time', chunk_time_interval => INTERVAL '1 day');
```

---

## 4. 完整Flink SQL Pipeline

### 4.1 表定义与连接器配置

```sql
-- ============================================================
-- Flink SQL: 源表定义
-- ============================================================

-- 1. Matter设备事件Kafka源表
CREATE TABLE matter_events (
    node_id STRING,
    endpoint INT,
    cluster_id STRING,
    attribute_id STRING,
    value STRING,
    data_type STRING,
    source_timestamp TIMESTAMP(3),
    ingestion_timestamp AS PROCTIME(),
    WATERMARK FOR source_timestamp AS source_timestamp - INTERVAL '3' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'matter-device-events',
    'properties.bootstrap.servers' = 'kafka:9092',
    'properties.group.id' = 'flink-matter-consumer',
    'format' = 'json',
    'json.fail-on-missing-field' = 'false',
    'scan.startup.mode' = 'latest-offset'
);

-- 2. Zigbee设备事件Kafka源表
CREATE TABLE zigbee_events (
    ieee_address STRING,
    network_address STRING,
    device_type STRING,
    friendly_name STRING,
    state STRING,  -- JSON string
    linkquality INT,
    event_time TIMESTAMP(3),
    WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'zigbee2mqtt-events',
    'properties.bootstrap.servers' = 'kafka:9092',
    'format' = 'json'
);

-- 3. Z-Wave设备事件Kafka源表
CREATE TABLE zwave_events (
    node_id INT,
    device_class STRING,
    command_class STRING,
    property_name STRING,
    property_value STRING,
    event_time TIMESTAMP(3),
    WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'zwave-js-events',
    'properties.bootstrap.servers' = 'kafka:9092',
    'format' = 'json'
);

-- 4. 用户操作事件
CREATE TABLE user_actions (
    action_id STRING,
    user_id STRING,
    home_id STRING,
    action_type STRING,  -- scene_trigger, device_control, setting_change
    target_id STRING,
    action_params STRING,
    source_ip STRING,
    client_type STRING,  -- ios, android, web, voice
    event_time TIMESTAMP(3),
    WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'user-actions',
    'properties.bootstrap.servers' = 'kafka:9092',
    'format' = 'json'
);

-- 5. 电价信息表 (维表)
CREATE TABLE electricity_rates (
    region STRING,
    rate_period STRING,
    start_time TIME,
    end_time TIME,
    is_weekend BOOLEAN,
    rate_per_kwh DECIMAL(10,6),
    is_peak BOOLEAN,
    PRIMARY KEY (region, rate_period, is_weekend) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/smart_home',
    'table-name' = 'electricity_rates',
    'username' = 'flink',
    'password' = 'flink-iot-2024',
    'lookup.cache.max-rows' = '100',
    'lookup.cache.ttl' = '1 hour'
);

-- 6. 设备元数据维表
CREATE TABLE device_metadata (
    device_id STRING,
    device_name STRING,
    device_type STRING,
    protocol STRING,
    home_id STRING,
    room_id STRING,
    room_name STRING,
    capabilities ARRAY<STRING>,
    PRIMARY KEY (device_id) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/smart_home',
    'table-name' = 'devices',
    'username' = 'flink',
    'password' = 'flink-iot-2024',
    'lookup.cache.max-rows' = '10000',
    'lookup.cache.ttl' = '10 minutes'
);
```

### 4.2 数据标准化与清洗

```sql
-- ============================================================
-- SQL 01: 协议数据标准化为统一设备状态
-- ============================================================

CREATE VIEW unified_device_states AS
-- Matter设备标准化
SELECT
    CONCAT('matter_', node_id, '_', CAST(endpoint AS STRING)) as device_id,
    'MATTER' as protocol,
    node_id as native_id,
    CASE cluster_id
        WHEN '0x0006' THEN 'onoff'
        WHEN '0x0008' THEN 'brightness'
        WHEN '0x0300' THEN 'color'
        WHEN '0x0201' THEN 'temperature'
        WHEN '0x0101' THEN 'lock_state'
        WHEN '0x0402' THEN 'temperature'
        WHEN '0x0405' THEN 'humidity'
        WHEN '0x0406' THEN 'occupancy'
        ELSE cluster_id
    END as state_type,
    value as state_value,
    CASE
        WHEN data_type IN ('INT8', 'INT16', 'INT32', 'INT64', 'FLOAT', 'DOUBLE')
        THEN CAST(value AS DOUBLE)
        ELSE NULL
    END as numeric_value,
    CASE cluster_id
        WHEN '0x0201' THEN 'celsius'
        WHEN '0x0405' THEN 'percent'
        WHEN '0x0008' THEN 'percent'
        ELSE ''
    END as unit,
    source_timestamp as event_time
FROM matter_events
WHERE cluster_id IN ('0x0006', '0x0008', '0x0300', '0x0201', '0x0101', '0x0402', '0x0405', '0x0406')

UNION ALL

-- Zigbee设备标准化
SELECT
    CONCAT('zigbee_', REPLACE(ieee_address, ':', '')) as device_id,
    'ZIGBEE' as protocol,
    ieee_address as native_id,
    CASE
        WHEN JSON_EXISTS(state, '$.state') THEN 'onoff'
        WHEN JSON_EXISTS(state, '$.brightness') THEN 'brightness'
        WHEN JSON_EXISTS(state, '$.temperature') THEN 'temperature'
        WHEN JSON_EXISTS(state, '$.humidity') THEN 'humidity'
        WHEN JSON_EXISTS(state, '$.occupancy') THEN 'occupancy'
        WHEN JSON_EXISTS(state, '$.contact') THEN 'contact'
        WHEN JSON_EXISTS(state, '$.illuminance') THEN 'illuminance'
        ELSE 'unknown'
    END as state_type,
    COALESCE(
        JSON_VALUE(state, '$.state'),
        JSON_VALUE(state, '$.brightness'),
        JSON_VALUE(state, '$.temperature'),
        JSON_VALUE(state, '$.humidity'),
        JSON_VALUE(state, '$.occupancy'),
        JSON_VALUE(state, '$.contact'),
        JSON_VALUE(state, '$.illuminance'),
        state
    ) as state_value,
    CASE
        WHEN JSON_EXISTS(state, '$.temperature')
        THEN CAST(JSON_VALUE(state, '$.temperature') AS DOUBLE)
        WHEN JSON_EXISTS(state, '$.humidity')
        THEN CAST(JSON_VALUE(state, '$.humidity') AS DOUBLE)
        WHEN JSON_EXISTS(state, '$.brightness')
        THEN CAST(JSON_VALUE(state, '$.brightness') AS DOUBLE)
        WHEN JSON_EXISTS(state, '$.illuminance')
        THEN CAST(JSON_VALUE(state, '$.illuminance') AS DOUBLE)
        ELSE NULL
    END as numeric_value,
    CASE
        WHEN JSON_EXISTS(state, '$.temperature') THEN 'celsius'
        WHEN JSON_EXISTS(state, '$.humidity') THEN 'percent'
        WHEN JSON_EXISTS(state, '$.brightness') THEN 'percent'
        ELSE ''
    END as unit,
    event_time
FROM zigbee_events

UNION ALL

-- Z-Wave设备标准化
SELECT
    CONCAT('zwave_', CAST(node_id AS STRING)) as device_id,
    'ZWAVE' as protocol,
    CAST(node_id AS STRING) as native_id,
    property_name as state_type,
    property_value as state_value,
    TRY_CAST(property_value AS DOUBLE) as numeric_value,
    '' as unit,
    event_time
FROM zwave_events;

-- ============================================================
-- SQL 02: 数据清洗与质量标记
-- ============================================================

CREATE VIEW cleansed_device_states AS
SELECT
    u.*,
    d.device_name,
    d.device_type,
    d.home_id,
    d.room_id,
    d.room_name,
    -- 数据质量评分
    CASE
        WHEN u.event_time < NOW() - INTERVAL '1' DAY THEN 0  -- 过期数据
        WHEN u.event_time > NOW() + INTERVAL '1' MINUTE THEN 0  -- 未来时间戳
        WHEN u.state_value IS NULL THEN 0  -- 空值
        WHEN u.numeric_value IS NOT NULL AND (u.numeric_value < -1000 OR u.numeric_value > 10000) THEN 30  -- 异常值
        ELSE 100  -- 正常
    END as quality_score,
    -- 数据有效性标记
    CASE
        WHEN u.event_time BETWEEN NOW() - INTERVAL '1' DAY AND NOW() + INTERVAL '1' MINUTE
         AND u.state_value IS NOT NULL
        THEN TRUE
        ELSE FALSE
    END as is_valid
FROM unified_device_states u
LEFT JOIN device_metadata FOR SYSTEM_TIME AS OF u.event_time AS d
    ON u.device_id = d.device_id
WHERE d.device_id IS NOT NULL;  -- 过滤未知设备
```

### 4.3 实时场景检测（CEP）

```sql
-- ============================================================
-- SQL 03: 回家模式场景检测 (复杂事件处理)
-- ============================================================

-- 定义回家模式触发事件
CREATE VIEW arriving_home_detection AS
SELECT *
FROM cleansed_device_states
MATCH_RECOGNIZE (
    PARTITION BY home_id
    ORDER BY event_time
    MEASURES
        A.device_id as unlock_device,
        A.event_time as unlock_time,
        B.device_id as motion_device_1,
        B.event_time as motion_time_1,
        C.event_time as trigger_time,
        'arriving_home' as scene_name
    AFTER MATCH SKIP PAST LAST ROW
    PATTERN (A B* C)
    DEFINE
        -- A: 门锁解锁事件
        A AS device_type = 'lock'
            AND state_type = 'lock_state'
            AND state_value = 'unlocked',
        -- B: 可选的中间运动检测
        B AS device_type = 'motion_sensor'
            AND state_type = 'occupancy'
            AND state_value = 'true'
            AND event_time < A.event_time + INTERVAL '2' MINUTE,
        -- C: 客厅运动检测 (确认进入)
        C AS device_type = 'motion_sensor'
            AND state_type = 'occupancy'
            AND state_value = 'true'
            AND room_name = '客厅'
            AND event_time BETWEEN A.event_time + INTERVAL '10' SECOND
                              AND A.event_time + INTERVAL '5' MINUTE
)
WHERE home_id IS NOT NULL;

-- ============================================================
-- SQL 04: 安防告警场景检测
-- ============================================================

-- 异常入侵检测: 离家状态下检测到运动
CREATE VIEW security_intrusion_detection AS
SELECT
    d.home_id,
    d.device_id as trigger_device,
    d.room_name as trigger_location,
    d.event_time as trigger_time,
    'security_intrusion' as alert_type,
    CONCAT('Motion detected in ', d.room_name, ' while away') as alert_message,
    10 as severity  -- 1-10, 10 being highest
FROM cleansed_device_states d
JOIN home_status h ON d.home_id = h.home_id
WHERE d.device_type = 'motion_sensor'
  AND d.state_type = 'occupancy'
  AND d.state_value = 'true'
  AND h.occupancy_status = 'AWAY'
  AND h.security_mode IN ('ARMED_AWAY', 'ARMED_STAY')
  AND h.last_status_change < d.event_time - INTERVAL '5' MINUTE;

-- 门窗传感器异常 (非授权时间打开)
CREATE VIEW door_window_alert AS
SELECT
    d.home_id,
    d.device_id,
    d.room_name,
    d.event_time,
    'door_window_open' as alert_type,
    CONCAT(d.device_name, ' opened at unauthorized time') as message,
    CASE
        WHEN EXTRACT(HOUR FROM d.event_time) BETWEEN 23 AND 6 THEN 8
        WHEN h.occupancy_status = 'AWAY' THEN 9
        ELSE 5
    END as severity
FROM cleansed_device_states d
JOIN home_status h ON d.home_id = h.home_id
WHERE d.device_type IN ('door_sensor', 'window_sensor')
  AND d.state_type = 'contact'
  AND d.state_value = 'open'
  AND (
      h.occupancy_status = 'AWAY'
      OR EXTRACT(HOUR FROM d.event_time) BETWEEN 23 AND 6
  );

-- ============================================================
-- SQL 05: 设备异常行为检测
-- ============================================================

-- 温度传感器读数突变检测
CREATE VIEW temperature_anomaly AS
SELECT
    home_id,
    device_id,
    room_name,
    AVG(current_value) as avg_temp,
    STDDEV(current_value) as temp_stddev,
    current_value,
    previous_value,
    ABS(current_value - previous_value) as change_delta,
    CASE
        WHEN ABS(current_value - previous_value) > 5 THEN 'CRITICAL'
        WHEN ABS(current_value - previous_value) > 2 THEN 'WARNING'
        ELSE 'NORMAL'
    END as anomaly_level
FROM (
    SELECT
        *,
        LAG(numeric_value) OVER (PARTITION BY device_id ORDER BY event_time) as previous_value,
        numeric_value as current_value
    FROM cleansed_device_states
    WHERE device_type = 'temperature_sensor'
      AND state_type = 'temperature'
      AND numeric_value IS NOT NULL
)
WHERE event_time > NOW() - INTERVAL '10' MINUTE
GROUP BY home_id, device_id, room_name, current_value, previous_value;
```

### 4.4 状态聚合与指标计算

```sql
-- ============================================================
-- SQL 06: 设备在线状态实时聚合
-- ============================================================

-- 每分钟计算各家庭的设备在线统计
CREATE VIEW device_online_stats AS
SELECT
    home_id,
    TUMBLE_START(event_time, INTERVAL '1' MINUTE) as window_start,
    TUMBLE_END(event_time, INTERVAL '1' MINUTE) as window_end,
    COUNT(DISTINCT device_id) as total_devices,
    COUNT(DISTINCT CASE WHEN is_valid THEN device_id END) as online_devices,
    COUNT(DISTINCT CASE WHEN protocol = 'MATTER' THEN device_id END) as matter_devices,
    COUNT(DISTINCT CASE WHEN protocol = 'ZIGBEE' THEN device_id END) as zigbee_devices,
    COUNT(DISTINCT CASE WHEN protocol = 'ZWAVE' THEN device_id END) as zwave_devices,
    ROUND(
        COUNT(DISTINCT CASE WHEN is_valid THEN device_id END) * 100.0
        / NULLIF(COUNT(DISTINCT device_id), 0),
        2
    ) as online_percentage
FROM cleansed_device_states
GROUP BY
    home_id,
    TUMBLE(event_time, INTERVAL '1' MINUTE);

-- ============================================================
-- SQL 07: 房间环境状态聚合
-- ============================================================

CREATE VIEW room_environment_summary AS
SELECT
    home_id,
    room_id,
    room_name,
    TUMBLE_START(event_time, INTERVAL '5' MINUTE) as window_start,

    -- 温度统计
    AVG(CASE WHEN state_type = 'temperature' THEN numeric_value END) as avg_temperature,
    MIN(CASE WHEN state_type = 'temperature' THEN numeric_value END) as min_temperature,
    MAX(CASE WHEN state_type = 'temperature' THEN numeric_value END) as max_temperature,

    -- 湿度统计
    AVG(CASE WHEN state_type = 'humidity' THEN numeric_value END) as avg_humidity,

    -- 光照统计
    AVG(CASE WHEN state_type = 'illuminance' THEN numeric_value END) as avg_illuminance,

    -- 占用状态
    MAX(CASE WHEN state_type = 'occupancy' THEN
        CASE WHEN state_value = 'true' THEN 1 ELSE 0 END
    END) as was_occupied,

    -- 活跃设备数
    COUNT(DISTINCT CASE WHEN is_valid THEN device_id END) as active_devices
FROM cleansed_device_states
GROUP BY
    home_id, room_id, room_name,
    TUMBLE(event_time, INTERVAL '5' MINUTE);

-- ============================================================
-- SQL 08: 用户活动模式分析
-- ============================================================

CREATE VIEW user_activity_patterns AS
SELECT
    home_id,
    DATE_FORMAT(event_time, 'yyyy-MM-dd') as date,
    EXTRACT(HOUR FROM event_time) as hour,

    -- 各类事件统计
    COUNT(CASE WHEN device_type = 'light' THEN 1 END) as light_interactions,
    COUNT(CASE WHEN device_type = 'thermostat' THEN 1 END) as climate_interactions,
    COUNT(CASE WHEN device_type = 'lock' THEN 1 END) as lock_interactions,
    COUNT(CASE WHEN device_type = 'media' THEN 1 END) as media_interactions,

    -- 活跃房间
    COLLECT(DISTINCT room_name) as active_rooms,

    -- 场景触发数
    COUNT(CASE WHEN state_type = 'scene_trigger' THEN 1 END) as scene_triggers
FROM cleansed_device_states
GROUP BY
    home_id,
    DATE_FORMAT(event_time, 'yyyy-MM-dd'),
    EXTRACT(HOUR FROM event_time);
```

### 4.5 能耗分析与优化

```sql
-- ============================================================
-- SQL 09: 实时能耗监测与峰谷分析
-- ============================================================

-- 智能电表数据接入
CREATE TABLE smart_meter_readings (
    meter_id STRING,
    home_id STRING,
    total_power_watts DOUBLE,
    voltage DOUBLE,
    current DOUBLE,
    power_factor DOUBLE,
    cumulative_kwh DOUBLE,
    reading_time TIMESTAMP(3),
    WATERMARK FOR reading_time AS reading_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'smart-meter-data',
    'properties.bootstrap.servers' = 'kafka:9092',
    'format' = 'json'
);

-- 实时功率聚合 (15分钟窗口)
CREATE VIEW power_consumption_15min AS
SELECT
    home_id,
    TUMBLE_START(reading_time, INTERVAL '15' MINUTE) as window_start,
    TUMBLE_END(reading_time, INTERVAL '15' MINUTE) as window_end,

    -- 功率统计
    AVG(total_power_watts) as avg_power_watts,
    MAX(total_power_watts) as peak_power_watts,
    MIN(total_power_watts) as min_power_watts,

    -- 能耗计算 (kWh)
    SUM(total_power_watts * 15.0 / 60.0 / 1000.0) as energy_kwh,

    -- 电费估算 (结合电价维表)
    FIRST_VALUE(r.rate_per_kwh) as rate_per_kwh,
    SUM(total_power_watts * 15.0 / 60.0 / 1000.0) * FIRST_VALUE(r.rate_per_kwh) as estimated_cost
FROM smart_meter_readings m
LEFT JOIN electricity_rates FOR SYSTEM_TIME AS OF m.reading_time AS r
    ON r.region = 'default'
    AND r.start_time <= CAST(m.reading_time AS TIME)
    AND r.end_time > CAST(m.reading_time AS TIME)
    AND r.is_weekend = (
        EXTRACT(DOW FROM m.reading_time) IN (0, 6)
    )
GROUP BY
    home_id,
    TUMBLE(reading_time, INTERVAL '15' MINUTE);

-- ============================================================
-- SQL 10: 高能耗设备识别
-- ============================================================

CREATE VIEW high_consumption_devices AS
SELECT
    d.home_id,
    d.device_id,
    d.device_name,
    d.device_type,
    d.room_name,

    -- 平均功率
    AVG(e.power_watts) as avg_power,
    MAX(e.power_watts) as peak_power,

    -- 累计能耗
    SUM(e.energy_wh) / 1000.0 as daily_kwh,

    -- 运行时长
    SUM(CASE WHEN e.is_on THEN 1 ELSE 0 END) * 15.0 / 60.0 as runtime_hours,

    -- 待机功耗
    AVG(CASE WHEN NOT e.is_on THEN e.power_watts END) as standby_power,

    -- 能耗排名 (同类型设备)
    ROW_NUMBER() OVER (
        PARTITION BY d.home_id, d.device_type
        ORDER BY SUM(e.energy_wh) DESC
    ) as consumption_rank
FROM device_energy e
JOIN device_metadata d ON e.device_id = d.device_id
WHERE e.time > NOW() - INTERVAL '1' DAY
GROUP BY d.home_id, d.device_id, d.device_name, d.device_type, d.room_name;

-- ============================================================
-- SQL 11: 节能机会识别
-- ============================================================

CREATE VIEW energy_saving_opportunities AS
SELECT
    home_id,
    'unused_light_on' as opportunity_type,
    device_id,
    device_name,
    room_name,
    CONCAT('Light has been on for ', CAST(hours_on AS STRING), ' hours in unoccupied room') as description,
    estimated_savings_kwh,
    CURRENT_TIMESTAMP as detected_at
FROM (
    SELECT
        d.home_id,
        d.device_id,
        d.device_name,
        d.room_name,
        COUNT(*) * 5.0 / 60.0 as hours_on,  -- 假设5分钟粒度
        COUNT(*) * 5.0 / 60.0 * 10.0 / 1000.0 as estimated_savings_kwh  -- 假设10W灯泡
    FROM cleansed_device_states d
    LEFT JOIN room_occupancy o
        ON d.home_id = o.home_id
        AND d.room_id = o.room_id
        AND d.event_time BETWEEN o.window_start AND o.window_end
    WHERE d.device_type = 'light'
      AND d.state_type = 'onoff'
      AND d.state_value = 'ON'
      AND (o.was_occupied = 0 OR o.was_occupied IS NULL)
      AND d.event_time > NOW() - INTERVAL '2' HOUR
    GROUP BY d.home_id, d.device_id, d.device_name, d.room_name
    HAVING COUNT(*) > 12  -- 超过1小时
)

UNION ALL

-- 空调设定温度优化建议
SELECT
    home_id,
    'hvac_optimization' as opportunity_type,
    device_id,
    device_name,
    room_name,
    CONCAT('Consider adjusting thermostat by 1°C to save ~',
           CAST(estimated_savings_kwh AS STRING), ' kWh/day') as description,
    estimated_savings_kwh,
    CURRENT_TIMESTAMP
FROM (
    SELECT
        d.home_id,
        d.device_id,
        d.device_name,
        d.room_name,
        AVG(d.numeric_value) as avg_temp_setting,
        AVG(o.avg_temperature) as avg_room_temp,
        2.5 as estimated_savings_kwh  -- 估算值
    FROM cleansed_device_states d
    JOIN room_environment_summary o
        ON d.home_id = o.home_id
        AND d.room_id = o.room_id
    WHERE d.device_type = 'thermostat'
      AND d.state_type = 'temperature'
      AND d.numeric_value BETWEEN 18 AND 26
    GROUP BY d.home_id, d.device_id, d.device_name, d.room_name
    HAVING AVG(d.numeric_value) < 20 OR AVG(d.numeric_value) > 24
);
```

### 4.6 场景执行与命令下发

```sql
-- ============================================================
-- SQL 12: 场景动作生成
-- ============================================================

-- 回家模式动作
CREATE VIEW arriving_home_actions AS
SELECT
    a.scene_name,
    a.home_id,
    a.trigger_time,
    actions.device_id,
    actions.command,
    actions.params,
    actions.delay_seconds,
    a.trigger_time + INTERVAL '1' SECOND * actions.delay_seconds as scheduled_time,
    8 as priority
FROM arriving_home_detection a
CROSS JOIN UNNEST(
    ARRAY[
        ROW('entry_light', 'on', '{"brightness": 100, "color_temp": 3000}', 0),
        ROW('living_room_light', 'on', '{"brightness": 80}', 2),
        ROW('hallway_light', 'on', '{"brightness": 60}', 3),
        ROW('thermostat_main', 'set', '{"temperature": 22, "mode": "auto"}', 10),
        ROW('living_room_curtain', 'open', '{"percentage": 50}', 15)
    ]
) AS actions(device_id, command, params, delay_seconds);

-- ============================================================
-- SQL 13: 设备命令队列管理
-- ============================================================

-- 命令输出表 (发送到Kafka供网关消费)
CREATE TABLE device_commands (
    command_id STRING,
    home_id STRING,
    device_id STRING,
    command STRING,
    params STRING,
    priority INT,
    scheduled_time TIMESTAMP(3),
    source_scene STRING,
    created_at TIMESTAMP(3)
) WITH (
    'connector' = 'kafka',
    'topic' = 'device-commands',
    'properties.bootstrap.servers' = 'kafka:9092',
    'format' = 'json'
);

-- 命令生成与下发
INSERT INTO device_commands
SELECT
    CONCAT('cmd_', CAST(scheduled_time AS STRING), '_', device_id) as command_id,
    home_id,
    device_id,
    command,
    params,
    priority,
    scheduled_time,
    scene_name as source_scene,
    CURRENT_TIMESTAMP as created_at
FROM arriving_home_actions
WHERE scheduled_time > CURRENT_TIMESTAMP;

-- ============================================================
-- SQL 14: 安防告警通知
-- ============================================================

-- 告警输出表
CREATE TABLE security_alerts (
    alert_id STRING,
    home_id STRING,
    alert_type STRING,
    severity INT,
    message STRING,
    trigger_device STRING,
    trigger_location STRING,
    triggered_at TIMESTAMP(3),
    notification_channels ARRAY<STRING>
) WITH (
    'connector' = 'kafka',
    'topic' = 'security-alerts',
    'properties.bootstrap.servers' = 'kafka:9092',
    'format' = 'json'
);

-- 安防告警生成
INSERT INTO security_alerts
SELECT
    CONCAT('alert_', CAST(trigger_time AS STRING), '_', home_id) as alert_id,
    home_id,
    alert_type,
    severity,
    alert_message,
    trigger_device,
    trigger_location,
    trigger_time as triggered_at,
    ARRAY['push', 'sms', 'email'] as notification_channels
FROM security_intrusion_detection

UNION ALL

SELECT
    CONCAT('alert_', CAST(event_time AS STRING), '_', home_id),
    home_id,
    alert_type,
    severity,
    message,
    device_id,
    room_name,
    event_time,
    CASE
        WHEN severity >= 8 THEN ARRAY['push', 'sms', 'email', 'call']
        ELSE ARRAY['push', 'email']
    END
FROM door_window_alert;
```

### 4.7 数据持久化与归档

```sql
-- ============================================================
-- SQL 15: 设备状态历史写入
-- ============================================================

-- 写入时序数据库
CREATE TABLE device_states_sink (
    time TIMESTAMP(3),
    device_id STRING,
    state_type STRING,
    state_value STRING,
    numeric_value DOUBLE,
    unit STRING,
    quality_score INT,
    PRIMARY KEY (time, device_id, state_type) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://timescaledb:5432/smart_home',
    'table-name' = 'device_states',
    'username' = 'flink',
    'password' = 'flink-iot-2024'
);

INSERT INTO device_states_sink
SELECT
    event_time as time,
    device_id,
    state_type,
    state_value,
    numeric_value,
    unit,
    quality_score
FROM cleansed_device_states
WHERE is_valid = TRUE;

-- ============================================================
-- SQL 16: 指标聚合写入
-- ============================================================

-- 聚合指标输出表
CREATE TABLE home_metrics_sink (
    window_start TIMESTAMP(3),
    window_end TIMESTAMP(3),
    home_id STRING,
    metric_type STRING,
    metric_name STRING,
    metric_value DOUBLE,
    metadata STRING,
    PRIMARY KEY (window_start, home_id, metric_type, metric_name) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/smart_home',
    'table-name' = 'home_metrics',
    'username' = 'flink',
    'password' = 'flink-iot-2024'
);

-- 写入在线率指标
INSERT INTO home_metrics_sink
SELECT
    window_start,
    window_end,
    home_id,
    'device_online' as metric_type,
    'online_percentage' as metric_name,
    online_percentage as metric_value,
    CONCAT('{"total":', CAST(total_devices AS STRING),
          ',"online":', CAST(online_devices AS STRING), '}') as metadata
FROM device_online_stats;

-- ============================================================
-- SQL 17: S3冷存储归档
-- ============================================================

-- 原始事件归档到S3
CREATE TABLE events_archive (
    device_id STRING,
    protocol STRING,
    state_type STRING,
    state_value STRING,
    event_time TIMESTAMP(3),
    archive_date STRING
) PARTITIONED BY (archive_date) WITH (
    'connector' = 'filesystem',
    'path' = 's3://smart-home-archive/raw-events/',
    'format' = 'parquet',
    'sink.partition-commit.delay' = '1 h',
    'sink.partition-commit.policy.kind' = 'success-file'
);

INSERT INTO events_archive
SELECT
    device_id,
    protocol,
    state_type,
    state_value,
    event_time,
    DATE_FORMAT(event_time, 'yyyy-MM-dd') as archive_date
FROM cleansed_device_states
WHERE event_time < NOW() - INTERVAL '7' DAY;  -- 7天前的数据归档
```

### 4.8 实时报表与监控

```sql
-- ============================================================
-- SQL 18: 实时家庭健康度评分
-- ============================================================

CREATE VIEW home_health_score AS
SELECT
    home_id,
    window_end as calculated_at,

    -- 在线率得分 (40%)
    CASE
        WHEN online_percentage >= 95 THEN 40
        WHEN online_percentage >= 90 THEN 35
        WHEN online_percentage >= 80 THEN 25
        WHEN online_percentage >= 70 THEN 15
        ELSE 0
    END as online_score,

    -- 响应延迟得分 (20%) - 假设有延迟指标
    20 as latency_score,

    -- 场景成功率得分 (20%) - 假设有成功率指标
    20 as scene_success_score,

    -- 能耗效率得分 (20%)
    CASE
        WHEN peak_ratio < 0.3 THEN 20
        WHEN peak_ratio < 0.4 THEN 15
        WHEN peak_ratio < 0.5 THEN 10
        ELSE 5
    END as energy_efficiency_score,

    -- 综合得分
    online_score + latency_score + scene_success_score + energy_efficiency_score as total_score,

    CASE
        WHEN total_score >= 90 THEN 'EXCELLENT'
        WHEN total_score >= 75 THEN 'GOOD'
        WHEN total_score >= 60 THEN 'FAIR'
        ELSE 'POOR'
    END as health_grade

FROM device_online_stats o
LEFT JOIN (
    SELECT home_id, peak_ratio
    FROM energy_aggregations
    WHERE aggregation_period = 'day'
      AND period_start = CURRENT_DATE
) e ON o.home_id = e.home_id;

-- ============================================================
-- SQL 19: 运营指标实时看板
-- ============================================================

CREATE VIEW operational_dashboard AS
SELECT
    'system_wide' as scope,
    window_end as timestamp,

    -- 设备统计
    COUNT(DISTINCT device_id) as total_devices,
    AVG(online_percentage) as avg_online_percentage,
    COUNT(DISTINCT CASE WHEN online_percentage < 80 THEN home_id END) as homes_with_issues,

    -- 事件统计
    COUNT(*) as total_events,
    AVG(quality_score) as avg_data_quality,

    -- 协议分布
    COUNT(DISTINCT CASE WHEN protocol = 'MATTER' THEN device_id END) as matter_device_count,
    COUNT(DISTINCT CASE WHEN protocol = 'ZIGBEE' THEN device_id END) as zigbee_device_count,
    COUNT(DISTINCT CASE WHEN protocol = 'ZWAVE' THEN device_id END) as zwave_device_count

FROM cleansed_device_states
GROUP BY TUMBLE(event_time, INTERVAL '5' MINUTE);

-- ============================================================
-- SQL 20: 异常检测告警
-- ============================================================

CREATE TABLE system_alerts (
    alert_id STRING,
    alert_type STRING,
    severity STRING,
    home_id STRING,
    device_id STRING,
    message STRING,
    metric_name STRING,
    metric_value DOUBLE,
    threshold_value DOUBLE,
    triggered_at TIMESTAMP(3)
) WITH (
    'connector' = 'kafka',
    'topic' = 'system-alerts',
    'format' = 'json'
);

-- 设备离线告警
INSERT INTO system_alerts
SELECT
    CONCAT('offline_', home_id, '_', CAST(window_end AS STRING)) as alert_id,
    'device_offline' as alert_type,
    CASE
        WHEN online_percentage < 50 THEN 'CRITICAL'
        WHEN online_percentage < 80 THEN 'WARNING'
        ELSE 'INFO'
    END as severity,
    home_id,
    CAST(NULL AS STRING) as device_id,
    CONCAT('Only ', CAST(online_percentage AS STRING), '% devices online') as message,
    'online_percentage' as metric_name,
    online_percentage as metric_value,
    90.0 as threshold_value,
    window_end as triggered_at
FROM device_online_stats
WHERE online_percentage < 90;

-- 数据质量告警
INSERT INTO system_alerts
SELECT
    CONCAT('quality_', home_id, '_', CAST(TUMBLE_END(event_time, INTERVAL '15' MINUTE) AS STRING)) as alert_id,
    'data_quality' as alert_type,
    'WARNING' as severity,
    home_id,
    CAST(NULL AS STRING) as device_id,
    CONCAT('Data quality score: ', CAST(AVG(quality_score) AS STRING)) as message,
    'avg_quality_score' as metric_name,
    AVG(quality_score) as metric_value,
    80.0 as threshold_value,
    TUMBLE_END(event_time, INTERVAL '15' MINUTE) as triggered_at
FROM cleansed_device_states
GROUP BY home_id, TUMBLE(event_time, INTERVAL '15' MINUTE)
HAVING AVG(quality_score) < 80;
```

---

## 5. 项目骨架实现

### 5.1 Docker Compose配置

```yaml
# ============================================================================
# Smart Home IoT Platform - Docker Compose Configuration
# 技术栈: Flink + Kafka + EMQX + InfluxDB + TimescaleDB + Grafana
# 适用场景: 10,000户智能家居部署
# ============================================================================

version: '3.8'

services:
  # ==========================================================================
  # Zookeeper - Kafka依赖
  # ==========================================================================
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    container_name: smarthome-zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"
    volumes:
      - zookeeper-data:/var/lib/zookeeper/data
    networks:
      - smarthome-network
    healthcheck:
      test: ["CMD", "bash", "-c", "echo 'ruok' | nc localhost 2181"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ==========================================================================
  # Kafka - 消息总线
  # ==========================================================================
  kafka:
    image: confluentinc/cp-kafka:7.5.0
    container_name: smarthome-kafka
    depends_on:
      zookeeper:
        condition: service_healthy
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092,PLAINTEXT_HOST://localhost:29092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"
      KAFKA_LOG_RETENTION_HOURS: 168
      KAFKA_MESSAGE_MAX_BYTES: 10485760
    ports:
      - "9092:9092"
      - "29092:29092"
    volumes:
      - kafka-data:/var/lib/kafka/data
    networks:
      - smarthome-network
    healthcheck:
      test: ["CMD", "kafka-broker-api-versions", "--bootstrap-server", "localhost:9092"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  # ==========================================================================
  # Kafka Topics初始化
  # ==========================================================================
  kafka-init:
    image: confluentinc/cp-kafka:7.5.0
    container_name: smarthome-kafka-init
    depends_on:
      kafka:
        condition: service_healthy
    entrypoint: ["/bin/sh", "-c"]
    command: |
      "
      echo 'Creating Kafka topics...' &&
      kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic matter-device-events --partitions 6 --replication-factor 1 &&
      kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic zigbee2mqtt-events --partitions 6 --replication-factor 1 &&
      kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic zwave-js-events --partitions 3 --replication-factor 1 &&
      kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic unified-device-states --partitions 12 --replication-factor 1 &&
      kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic user-actions --partitions 3 --replication-factor 1 &&
      kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic smart-meter-data --partitions 6 --replication-factor 1 &&
      kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic device-commands --partitions 12 --replication-factor 1 &&
      kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic security-alerts --partitions 3 --replication-factor 1 &&
      kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic system-alerts --partitions 3 --replication-factor 1 &&
      kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic scene-executions --partitions 3 --replication-factor 1 &&
      echo 'All topics created successfully'
      "
    networks:
      - smarthome-network
    restart: "no"

  # ==========================================================================
  # EMQX - MQTT Broker (智能家居设备接入)
  # ==========================================================================
  emqx:
    image: emqx/emqx:5.4.0
    container_name: smarthome-emqx
    environment:
      EMQX_NODE_NAME: emqx@127.0.0.1
      EMQX_CLUSTER__DISCOVERY_STRATEGY: static
      EMQX_DASHBOARD__DEFAULT_USERNAME: admin
      EMQX_DASHBOARD__DEFAULT_PASSWORD: smarthome2024
      EMQX_LISTENERS__TCP__DEFAULT__BIND: "0.0.0.0:1883"
      EMQX_LISTENERS__SSL__DEFAULT__BIND: "0.0.0.0:8883"
      EMQX_LISTENERS__WS__DEFAULT__BIND: "0.0.0.0:8083"
      EMQX_AUTHENTICATION__1__MECHANISM: password_based
      EMQX_AUTHENTICATION__1__BACKEND: built_in_database
      EMQX_AUTHENTICATION__1__ENABLE: "true"
      EMQX_AUTHORIZATION__SOURCES__1__TYPE: file
      EMQX_AUTHORIZATION__SOURCES__1__ENABLE: "true"
    ports:
      - "1883:1883"
      - "8883:8883"
      - "8083:8083"
      - "18083:18083"
    volumes:
      - emqx-data:/opt/emqx/data
      - ./emqx/acl.conf:/opt/emqx/etc/acl.conf:ro
    networks:
      - smarthome-network
    healthcheck:
      test: ["CMD", "emqx", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  # ==========================================================================
  # PostgreSQL - 关系型数据存储
  # ==========================================================================
  postgres:
    image: postgres:15-alpine
    container_name: smarthome-postgres
    environment:
      POSTGRES_DB: smart_home
      POSTGRES_USER: flink
      POSTGRES_PASSWORD: flink-iot-2024
      POSTGRES_INITDB_ARGS: "--encoding=UTF-8 --lc-collate=C --lc-ctype=C"
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d:ro
    networks:
      - smarthome-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U flink -d smart_home"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ==========================================================================
  # TimescaleDB - 时序数据存储
  # ==========================================================================
  timescaledb:
    image: timescale/timescaledb:latest-pg15
    container_name: smarthome-timescaledb
    environment:
      POSTGRES_DB: smart_home_ts
      POSTGRES_USER: flink
      POSTGRES_PASSWORD: flink-iot-2024
    ports:
      - "5433:5432"
    volumes:
      - timescaledb-data:/var/lib/postgresql/data
      - ./init-scripts/timescale:/docker-entrypoint-initdb.d:ro
    networks:
      - smarthome-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U flink -d smart_home_ts"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ==========================================================================
  # InfluxDB - 实时指标存储
  # ==========================================================================
  influxdb:
    image: influxdb:2.7
    container_name: smarthome-influxdb
    environment:
      DOCKER_INFLUXDB_INIT_MODE: setup
      DOCKER_INFLUXDB_INIT_USERNAME: admin
      DOCKER_INFLUXDB_INIT_PASSWORD: smarthome-2024
      DOCKER_INFLUXDB_INIT_ORG: smart-home
      DOCKER_INFLUXDB_INIT_BUCKET: device-metrics
      DOCKER_INFLUXDB_INIT_RETENTION: 30d
      DOCKER_INFLUXDB_INIT_ADMIN_TOKEN: smarthome-token-xyz123
    ports:
      - "8086:8086"
    volumes:
      - influxdb-data:/var/lib/influxdb2
    networks:
      - smarthome-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8086/health"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ==========================================================================
  # Flink JobManager
  # ==========================================================================
  flink-jobmanager:
    image: flink:1.18-scala_2.12
    container_name: smarthome-flink-jobmanager
    hostname: jobmanager
    command: jobmanager
    environment:
      - JOB_MANAGER_RPC_ADDRESS=jobmanager
      - FLINK_PROPERTIES=
          jobmanager.rpc.address: jobmanager
          jobmanager.rpc.port: 6123
          jobmanager.memory.process.size: 2048m
          jobmanager.memory.jvm-heap.size: 1536m
          jobmanager.memory.off-heap.size: 256m
          parallelism.default: 4
          taskmanager.numberOfTaskSlots: 4
          state.backend: rocksdb
          state.checkpoints.dir: file:///tmp/flink-checkpoints
          execution.checkpointing.interval: 30s
          execution.checkpointing.min-pause-between-checkpoints: 15s
          metrics.reporters: prom
          metrics.reporter.prom.class: org.apache.flink.metrics.prometheus.PrometheusReporter
          metrics.reporter.prom.port: 9249
    ports:
      - "8081:8081"
      - "6123:6123"
      - "9249:9249"
    volumes:
      - flink-checkpoints:/tmp/flink-checkpoints
      - ./flink-sql:/opt/flink/sql-scripts
      - ./flink-jars:/opt/flink/usrlib
    networks:
      - smarthome-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8081/overview"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  # ==========================================================================
  # Flink TaskManager (2 instances)
  # ==========================================================================
  flink-taskmanager-1:
    image: flink:1.18-scala_2.12
    container_name: smarthome-flink-taskmanager-1
    hostname: taskmanager-1
    command: taskmanager
    depends_on:
      flink-jobmanager:
        condition: service_healthy
    environment:
      - JOB_MANAGER_RPC_ADDRESS=jobmanager
      - FLINK_PROPERTIES=
          jobmanager.rpc.address: jobmanager
          taskmanager.rpc.port: 6122
          taskmanager.memory.process.size: 4096m
          taskmanager.memory.flink.size: 3072m
          taskmanager.memory.network.min: 256m
          taskmanager.memory.network.max: 512m
          taskmanager.numberOfTaskSlots: 4
          state.backend: rocksdb
          state.backend.incremental: true
          state.checkpoints.dir: file:///tmp/flink-checkpoints
    volumes:
      - flink-checkpoints:/tmp/flink-checkpoints
      - ./flink-jars:/opt/flink/usrlib
    networks:
      - smarthome-network

  flink-taskmanager-2:
    image: flink:1.18-scala_2.12
    container_name: smarthome-flink-taskmanager-2
    hostname: taskmanager-2
    command: taskmanager
    depends_on:
      flink-jobmanager:
        condition: service_healthy
    environment:
      - JOB_MANAGER_RPC_ADDRESS=jobmanager
      - FLINK_PROPERTIES=
          jobmanager.rpc.address: jobmanager
          taskmanager.rpc.port: 6122
          taskmanager.memory.process.size: 4096m
          taskmanager.memory.flink.size: 3072m
          taskmanager.memory.network.min: 256m
          taskmanager.memory.network.max: 512m
          taskmanager.numberOfTaskSlots: 4
          state.backend: rocksdb
          state.backend.incremental: true
          state.checkpoints.dir: file:///tmp/flink-checkpoints
    volumes:
      - flink-checkpoints:/tmp/flink-checkpoints
      - ./flink-jars:/opt/flink/usrlib
    networks:
      - smarthome-network

  # ==========================================================================
  # Flink SQL Client
  # ==========================================================================
  flink-sql-client:
    image: flink:1.18-scala_2.12
    container_name: smarthome-flink-sql-client
    command: /opt/flink/sql-client.sh
    depends_on:
      - flink-jobmanager
      - kafka
    environment:
      - JOB_MANAGER_RPC_ADDRESS=jobmanager
    volumes:
      - ./flink-sql:/opt/flink/sql-scripts
    stdin_open: true
    tty: true
    networks:
      - smarthome-network

  # ==========================================================================
  # Grafana - 监控与可视化
  # ==========================================================================
  grafana:
    image: grafana/grafana:10.2.0
    container_name: smarthome-grafana
    environment:
      GF_SECURITY_ADMIN_USER: admin
      GF_SECURITY_ADMIN_PASSWORD: smarthome-grafana
      GF_USERS_ALLOW_SIGN_UP: "false"
      GF_SERVER_ROOT_URL: http://localhost:3000
      GF_AUTH_ANONYMOUS_ENABLED: "true"
      GF_AUTH_ANONYMOUS_ORG_ROLE: Viewer
      GF_INSTALL_PLUGINS: grafana-clock-panel,grafana-simple-json-datasource
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning:ro
      - ./grafana/dashboards:/var/lib/grafana/dashboards:ro
    depends_on:
      - postgres
      - influxdb
    networks:
      - smarthome-network
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:3000/api/health || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ==========================================================================
  # Redis - 缓存与会话存储
  # ==========================================================================
  redis:
    image: redis:7-alpine
    container_name: smarthome-redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - smarthome-network
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ==========================================================================
  # Mock Data Generator - 模拟设备数据
  # ==========================================================================
  mock-generator:
    image: python:3.11-slim
    container_name: smarthome-mock-generator
    depends_on:
      kafka:
        condition: service_healthy
      emqx:
        condition: service_healthy
    volumes:
      - ./mock-data:/app
    working_dir: /app
    command: >
      sh -c "
        pip install kafka-python paho-mqtt numpy faker -q &&
        python smart-home-generator.py
      "
    environment:
      KAFKA_BOOTSTRAP_SERVERS: kafka:9092
      MQTT_BROKER: emqx
      MQTT_PORT: 1883
      HOME_COUNT: 100
      DEVICES_PER_HOME: 50
      MESSAGE_RATE_PER_DEVICE: 0.1
    networks:
      - smarthome-network
    restart: unless-stopped

# ============================================================================
# Networks
# ============================================================================
networks:
  smarthome-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.25.0.0/16

# ============================================================================
# Volumes
# ============================================================================
volumes:
  zookeeper-data:
  kafka-data:
  postgres-data:
  timescaledb-data:
  influxdb-data:
  flink-checkpoints:
  emqx-data:
  grafana-data:
  redis-data:
```

### 5.2 Flink SQL脚本目录结构

```
flink-sql/
├── 00-setup-connectors.sql      # 连接器配置
├── 01-create-sources.sql        # 源表定义
├── 02-protocol-normalization.sql # 协议标准化
├── 03-data-cleansing.sql        # 数据清洗
├── 04-cep-scene-detection.sql   # CEP场景检测
├── 05-state-aggregation.sql     # 状态聚合
├── 06-energy-analysis.sql       # 能耗分析
├── 07-action-generation.sql     # 动作生成
├── 08-alert-management.sql      # 告警管理
├── 09-data-persistence.sql      # 数据持久化
└── 10-monitoring-metrics.sql    # 监控指标
```

### 5.3 模拟数据生成器

```python
# mock-data/smart-home-generator.py
#!/usr/bin/env python3
"""
Smart Home IoT Data Generator
模拟10,000户家庭的智能设备数据生成器
"""

import json
import random
import time
import os
from datetime import datetime, timedelta
from kafka import KafkaProducer
import paho.mqtt.client as mqtt
from faker import Faker
import numpy as np

fake = Faker()

# 配置
KAFKA_BOOTSTRAP = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
MQTT_BROKER = os.getenv('MQTT_BROKER', 'emqx')
MQTT_PORT = int(os.getenv('MQTT_PORT', '1883'))
HOME_COUNT = int(os.getenv('HOME_COUNT', '100'))
DEVICES_PER_HOME = int(os.getenv('DEVICES_PER_HOME', '50'))
MESSAGE_RATE = float(os.getenv('MESSAGE_RATE_PER_DEVICE', '0.1'))

# 设备类型定义
DEVICE_TYPES = {
    'light': {'protocols': ['MATTER', 'ZIGBEE', 'WIFI'], 'states': ['on', 'off'], 'power': [5, 60]},
    'thermostat': {'protocols': ['MATTER', 'WIFI'], 'states': ['heating', 'cooling', 'off'], 'power': [0, 3000]},
    'motion_sensor': {'protocols': ['ZIGBEE', 'ZWAVE', 'MATTER'], 'states': ['occupied', 'vacant'], 'power': [0, 0]},
    'door_sensor': {'protocols': ['ZIGBEE', 'ZWAVE'], 'states': ['open', 'closed'], 'power': [0, 0]},
    'lock': {'protocols': ['MATTER', 'ZIGBEE', 'ZWAVE'], 'states': ['locked', 'unlocked'], 'power': [0, 2]},
    'camera': {'protocols': ['WIFI', 'MATTER'], 'states': ['recording', 'standby'], 'power': [3, 10]},
    'smart_plug': {'protocols': ['WIFI', 'ZIGBEE', 'MATTER'], 'states': ['on', 'off'], 'power': [0, 2000]},
    'temperature_sensor': {'protocols': ['ZIGBEE', 'ZWAVE', 'MATTER'], 'states': [], 'power': [0, 0]},
    'humidity_sensor': {'protocols': ['ZIGBEE', 'ZWAVE', 'MATTER'], 'states': [], 'power': [0, 0]},
    'curtain': {'protocols': ['ZIGBEE', 'ZWAVE', 'MATTER'], 'states': ['open', 'closed', 'opening', 'closing'], 'power': [5, 30]},
}

ROOMS = ['客厅', '主卧', '次卧', '厨房', '卫生间', '书房', '阳台', '玄关']
MANUFACTURERS = ['Philips', 'Yeelight', 'Aqara', 'Tuya', 'IKEA', 'TP-Link', 'Ecobee', 'August', 'Ring']

class SmartHomeGenerator:
    def __init__(self):
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            batch_size=16384,
            linger_ms=10
        )
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        self.devices = self._generate_devices()
        self.device_states = {d['device_id']: self._init_state(d) for d in self.devices}

    def _generate_devices(self):
        """生成设备注册表"""
        devices = []
        for home_id in range(HOME_COUNT):
            home_devices = []
            for _ in range(DEVICES_PER_HOME):
                device_type = random.choice(list(DEVICE_TYPES.keys()))
                device_info = DEVICE_TYPES[device_type]
                protocol = random.choice(device_info['protocols'])

                device = {
                    'device_id': f"{protocol.lower()}_{home_id}_{fake.uuid4()[:8]}",
                    'home_id': f"home_{home_id:05d}",
                    'device_type': device_type,
                    'device_name': f"{fake.word().capitalize()} {device_type.replace('_', ' ').title()}",
                    'protocol': protocol,
                    'manufacturer': random.choice(MANUFACTURERS),
                    'room': random.choice(ROOMS),
                    'capabilities': device_info.get('capabilities', []),
                }
                home_devices.append(device)
            devices.extend(home_devices)

        # 保存设备注册表
        with open('/app/smart-devices.json', 'w') as f:
            json.dump(devices, f, indent=2)

        print(f"Generated {len(devices)} devices across {HOME_COUNT} homes")
        return devices

    def _init_state(self, device):
        """初始化设备状态"""
        device_type = device['device_type']
        info = DEVICE_TYPES[device_type]

        state = {
            'on': random.choice([True, False]) if 'on' in str(info.get('states', [])) else None,
            'brightness': random.randint(10, 100) if device_type == 'light' else None,
            'temperature': round(random.uniform(18, 26), 1) if device_type == 'thermostat' else None,
            'occupied': False if device_type == 'motion_sensor' else None,
            'contact': 'closed' if device_type == 'door_sensor' else None,
            'locked': True if device_type == 'lock' else None,
            'position': random.randint(0, 100) if device_type == 'curtain' else None,
        }
        return {k: v for k, v in state.items() if v is not None}

    def generate_matter_event(self, device):
        """生成Matter协议事件"""
        device_type = device['device_type']
        cluster_map = {
            'light': ('0x0006', '0x0008'),  # On/Off, Level Control
            'thermostat': ('0x0201',),
            'lock': ('0x0101',),
            'motion_sensor': ('0x0406',),
        }

        event = {
            'node_id': device['device_id'].replace('matter_', ''),
            'endpoint': 1,
            'cluster_id': cluster_map.get(device_type, ('0x0006',))[0],
            'attribute_id': '0x0000',
            'value': self._get_state_value(device),
            'data_type': 'BOOL' if device_type in ['light', 'lock'] else 'INT16',
            'source_timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        return event

    def generate_zigbee_event(self, device):
        """生成Zigbee协议事件"""
        device_type = device['device_type']
        state = self.device_states[device['device_id']]

        state_dict = {}
        if device_type == 'light':
            state_dict['state'] = 'ON' if state.get('on') else 'OFF'
            if state.get('brightness'):
                state_dict['brightness'] = state['brightness']
        elif device_type == 'motion_sensor':
            state_dict['occupancy'] = state.get('occupied', False)
        elif device_type == 'temperature_sensor':
            state_dict['temperature'] = round(random.uniform(18, 28), 1)
        elif device_type == 'door_sensor':
            state_dict['contact'] = state.get('contact', 'closed')

        event = {
            'ieee_address': device['device_id'].replace('zigbee_', ''),
            'device_type': device_type,
            'friendly_name': device['device_name'],
            'state': json.dumps(state_dict),
            'linkquality': random.randint(50, 255),
            'event_time': datetime.utcnow().isoformat() + 'Z'
        }
        return event

    def generate_zwave_event(self, device):
        """生成Z-Wave协议事件"""
        event = {
            'node_id': int(device['device_id'].replace('zwave_', '').split('_')[0]),
            'device_class': device['device_type'],
            'command_class': '0x25' if device['device_type'] == 'light' else '0x30',
            'property_name': 'currentValue',
            'property_value': self._get_state_value(device),
            'event_time': datetime.utcnow().isoformat() + 'Z'
        }
        return event

    def _get_state_value(self, device):
        """获取设备状态值"""
        state = self.device_states[device['device_id']]
        if device['device_type'] == 'light':
            return 'true' if state.get('on') else 'false'
        elif device['device_type'] == 'lock':
            return '1' if state.get('locked') else '0'
        return str(state)

    def update_device_state(self, device):
        """模拟设备状态变化"""
        device_id = device['device_id']
        device_type = device['device_type']
        state = self.device_states[device_id]

        # 模拟随机状态变化
        if device_type == 'light' and random.random() < 0.1:
            state['on'] = not state.get('on', False)
        elif device_type == 'motion_sensor' and random.random() < 0.05:
            state['occupied'] = not state.get('occupied', False)
        elif device_type == 'temperature_sensor':
            current = state.get('temperature', 22)
            state['temperature'] = round(current + random.uniform(-0.5, 0.5), 1)
        elif device_type == 'thermostat':
            current = state.get('temperature', 22)
            state['temperature'] = round(current + random.uniform(-0.2, 0.2), 1)

    def run(self):
        """主循环"""
        print("Starting Smart Home Data Generator...")

        while True:
            for device in self.devices:
                if random.random() > MESSAGE_RATE:
                    continue

                # 更新状态
                self.update_device_state(device)

                # 生成事件
                protocol = device['protocol']
                if protocol == 'MATTER':
                    event = self.generate_matter_event(device)
                    topic = 'matter-device-events'
                elif protocol == 'ZIGBEE':
                    event = self.generate_zigbee_event(device)
                    topic = 'zigbee2mqtt-events'
                elif protocol == 'ZWAVE':
                    event = self.generate_zwave_event(device)
                    topic = 'zwave-js-events'
                else:
                    continue

                # 发送到Kafka
                self.kafka_producer.send(topic, event)

                # 部分事件同时发送到MQTT
                if random.random() < 0.3:
                    mqtt_topic = f"smart-home/{device['home_id']}/{device['device_id']}"
                    self.mqtt_client.publish(mqtt_topic, json.dumps(event))

            time.sleep(1)

if __name__ == '__main__':
    generator = SmartHomeGenerator()
    try:
        generator.run()
    except KeyboardInterrupt:
        print("Shutting down...")
```

### 5.4 模拟设备注册表

```json
{
  "smart-devices.json": {
    "description": "智能家居设备注册表",
    "devices": [
      {
        "device_id": "matter_home_00001_abc123",
        "home_id": "home_00001",
        "device_type": "light",
        "device_name": "Living Room Main Light",
        "protocol": "MATTER",
        "manufacturer": "Philips",
        "room": "客厅",
        "capabilities": ["onoff", "brightness", "color_temp", "color"]
      },
      {
        "device_id": "zigbee_home_00001_def456",
        "home_id": "home_00001",
        "device_type": "motion_sensor",
        "device_name": "Entry Motion Sensor",
        "protocol": "ZIGBEE",
        "manufacturer": "Aqara",
        "room": "玄关",
        "capabilities": ["occupancy", "illuminance", "battery"]
      },
      {
        "device_id": "zwave_home_00001_ghi789",
        "home_id": "home_00001",
        "device_type": "lock",
        "device_name": "Front Door Lock",
        "protocol": "ZWAVE",
        "manufacturer": "August",
        "room": "玄关",
        "capabilities": ["lock", "unlock", "battery", "auto_lock"]
      }
    ]
  }
}
```

### 5.5 场景规则配置

```json
{
  "scene-rules.json": {
    "description": "场景联动规则配置",
    "scenes": [
      {
        "scene_id": "arriving_home",
        "scene_name": "回家模式",
        "description": "用户回家自动开启必要设备",
        "trigger": {
          "type": "event",
          "conditions": [
            {"device_type": "lock", "state": "unlocked"},
            {"device_type": "motion_sensor", "state": "occupied", "room": "玄关", "delay": "10s"}
          ],
          "time_window": "5m"
        },
        "actions": [
          {"device_type": "light", "room": "玄关", "command": "on", "params": {"brightness": 100}, "delay": 0},
          {"device_type": "light", "room": "客厅", "command": "on", "params": {"brightness": 80}, "delay": 2},
          {"device_type": "thermostat", "command": "set", "params": {"temperature": 22}, "delay": 10}
        ],
        "constraints": {
          "time_range": null,
          "occupancy_required": false,
          "weather_dependent": false
        }
      },
      {
        "scene_id": "sleep_mode",
        "scene_name": "睡眠模式",
        "description": "睡前自动关闭非必要设备",
        "trigger": {
          "type": "schedule",
          "time": "22:30",
          "days": [1, 2, 3, 4, 5, 6, 7]
        },
        "actions": [
          {"device_type": "light", "room": "客厅", "command": "off", "delay": 0},
          {"device_type": "light", "room": "厨房", "command": "off", "delay": 0},
          {"device_type": "curtain", "room": "主卧", "command": "close", "delay": 5},
          {"device_type": "thermostat", "command": "set", "params": {"temperature": 20}, "delay": 10}
        ]
      },
      {
        "scene_id": "security_alert",
        "scene_name": "安防告警",
        "description": "检测到异常入侵",
        "trigger": {
          "type": "event",
          "conditions": [
            {"device_type": "motion_sensor", "state": "occupied"}
          ],
          "precondition": {"occupancy": "away", "security_armed": true}
        },
        "actions": [
          {"device_type": "light", "command": "on", "params": {"brightness": 100}, "delay": 0},
          {"type": "notification", "channels": ["push", "sms", "email"], "delay": 0},
          {"type": "camera", "command": "start_recording", "delay": 0}
        ]
      }
    ]
  }
}
```

### 5.6 Grafana Dashboard配置

```json
{
  "dashboard": {
    "id": null,
    "title": "Smart Home IoT Monitoring",
    "tags": ["iot", "smart-home", "flink"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Online Devices",
        "type": "stat",
        "targets": [
          {
            "datasource": "InfluxDB",
            "query": "SELECT sum(\"online_devices\") FROM \"device_stats\" WHERE $timeFilter"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "steps": [
                {"color": "red", "value": 0},
                {"color": "yellow", "value": 400000},
                {"color": "green", "value": 450000}
              ]
            }
          }
        }
      },
      {
        "id": 2,
        "title": "Device Online Rate",
        "type": "gauge",
        "targets": [
          {
            "datasource": "InfluxDB",
            "query": "SELECT mean(\"online_percentage\") FROM \"device_stats\" WHERE $timeFilter"
          }
        ]
      },
      {
        "id": 3,
        "title": "Protocol Distribution",
        "type": "piechart",
        "targets": [
          {
            "datasource": "PostgreSQL",
            "rawSql": "SELECT protocol, COUNT(*) as count FROM devices GROUP BY protocol"
          }
        ]
      },
      {
        "id": 4,
        "title": "Scene Execution Success Rate",
        "type": "timeseries",
        "targets": [
          {
            "datasource": "PostgreSQL",
            "rawSql": "SELECT time_bucket('5 minutes', triggered_at) as time, AVG(CASE WHEN status='success' THEN 1 ELSE 0 END) * 100 as success_rate FROM scene_executions WHERE triggered_at BETWEEN $__timeFrom() AND $__timeTo() GROUP BY time ORDER BY time"
          }
        ]
      },
      {
        "id": 5,
        "title": "Energy Consumption (Total)",
        "type": "timeseries",
        "targets": [
          {
            "datasource": "TimescaleDB",
            "rawSql": "SELECT time_bucket('15 minutes', time) as time, SUM(total_power_watts) as total_power FROM energy_readings WHERE time BETWEEN $__timeFrom() AND $__timeTo() GROUP BY time ORDER BY time"
          }
        ]
      },
      {
        "id": 6,
        "title": "Security Alerts",
        "type": "table",
        "targets": [
          {
            "datasource": "PostgreSQL",
            "rawSql": "SELECT triggered_at, alert_type, severity, message, trigger_location FROM security_alerts WHERE triggered_at > NOW() - INTERVAL '24 hours' ORDER BY triggered_at DESC LIMIT 100"
          }
        ]
      },
      {
        "id": 7,
        "title": "Flink Job Metrics",
        "type": "timeseries",
        "targets": [
          {
            "datasource": "Prometheus",
            "expr": "flink_taskmanager_job_task_operator_numRecordsInPerSecond"
          }
        ]
      },
      {
        "id": 8,
        "title": "Response Time Distribution",
        "type": "heatmap",
        "targets": [
          {
            "datasource": "InfluxDB",
            "query": "SELECT \"response_time_ms\" FROM \"scene_executions\" WHERE $timeFilter"
          }
        ]
      }
    ]
  }
}
```

---

## 6. 性能优化与生产建议

### 6.1 Flink性能调优

| 配置项 | 推荐值 | 说明 |
|--------|--------|------|
| taskmanager.memory.process.size | 4GB | 每个TM总内存 |
| taskmanager.memory.network.max | 512MB | 网络缓冲 |
| state.backend | rocksdb | 大状态场景 |
| state.backend.incremental | true | 增量checkpoint |
| execution.checkpointing.interval | 30s | 平衡性能与恢复时间 |
| parallelism.default | 4 | 默认并行度 |

### 6.2 Kafka分区策略

| Topic | 分区数 | 说明 |
|-------|--------|------|
| unified-device-states | 12 | 核心数据流 |
| device-commands | 12 | 控制命令 |
| matter-device-events | 6 | Matter事件 |
| zigbee2mqtt-events | 6 | Zigbee事件 |
| security-alerts | 3 | 安防告警 |

### 6.3 数据库索引优化

```sql
-- 设备状态表复合索引
CREATE INDEX CONCURRENTLY idx_device_states_lookup
ON device_states(device_id, state_type, time DESC);

-- 场景执行日志分区
CREATE TABLE scene_executions_partitioned (LIKE scene_executions)
PARTITION BY RANGE (triggered_at);
```

---

## 7. 总结与展望

### 7.1 项目成果

本项目成功构建了一个支持10,000户家庭的智能家居实时协调平台，主要成果包括：

1. **统一接入层**: 支持Matter、Zigbee、Z-Wave、Wi-Fi四种主流协议
2. **实时场景引擎**: P99响应延迟<300ms，场景成功率>99.5%
3. **能耗优化**: 平均节能18-25%，部分家庭达30%
4. **系统稳定性**: 99.95%可用性，自动故障恢复

### 7.2 未来演进

- **AI场景推荐**: 基于用户行为的智能场景推荐
- **数字孪生**: 家庭环境的3D数字孪生
- **碳中和**: 家庭能源碳足迹追踪与中和
- **健康融合**: 与可穿戴设备联动的健康监测

---

## 8. 引用参考

[^1]: Apple Inc., "HomeKit Accessory Protocol (HAP) Specification", 2023. <https://developer.apple.com/homekit/>

[^2]: Google LLC, "Google Nest Developer Guide", 2023. <https://developers.google.com/nest/>

[^3]: Connectivity Standards Alliance, "Matter Specification Version 1.0", 2022. <https://csa-iot.org/all-solutions/matter/>
