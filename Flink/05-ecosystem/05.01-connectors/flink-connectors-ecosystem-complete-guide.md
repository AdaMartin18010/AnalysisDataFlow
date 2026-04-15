# Flink 连接器生态完整指南 (Flink Connectors Ecosystem Complete Guide)

> **所属阶段**: Flink/04-connectors | **前置依赖**: [kafka-integration-patterns.md](./kafka-integration-patterns.md), [flink-iceberg-integration.md](./flink-iceberg-integration.md), [flink-cdc-3.0-data-integration.md](./flink-cdc-3.0-data-integration.md) | **形式化等级**: L4 | **覆盖范围**: 消息队列/文件系统/数据库/Lakehouse/CDC

---

## 目录

- [Flink 连接器生态完整指南 (Flink Connectors Ecosystem Complete Guide)](#flink-连接器生态完整指南-flink-connectors-ecosystem-complete-guide)
  - [目录](#目录)
  - [1. 概念定义 (Definitions)](#1-概念定义-definitions)
    - [Def-F-04-100 (Flink 连接器形式化定义)](#def-f-04-100-flink-连接器形式化定义)
    - [Def-F-04-101 (连接器交付保证语义)](#def-f-04-101-连接器交付保证语义)
    - [Def-F-04-102 (Source 连接器接口契约)](#def-f-04-102-source-连接器接口契约)
    - [Def-F-04-103 (Sink 连接器接口契约)](#def-f-04-103-sink-连接器接口契约)
    - [Def-F-04-104 (连接器生态分层模型)](#def-f-04-104-连接器生态分层模型)
  - [2. 属性推导 (Properties)](#2-属性推导-properties)
    - [Lemma-F-04-100 (连接器组合封闭性)](#lemma-f-04-100-连接器组合封闭性)
    - [Lemma-F-04-101 (交付保证传递性)](#lemma-f-04-101-交付保证传递性)
    - [Prop-F-04-100 (端到端一致性约束)](#prop-f-04-100-端到端一致性约束)
    - [Prop-F-04-101 (连接器并行度扩展性)](#prop-f-04-101-连接器并行度扩展性)
  - [3. 关系建立 (Relations)](#3-关系建立-relations)
    - [3.1 连接器分类体系](#31-连接器分类体系)
    - [3.2 连接器与存储系统映射](#32-连接器与存储系统映射)
    - [3.3 连接器版本兼容性矩阵](#33-连接器版本兼容性矩阵)
  - [4. 论证过程 (Argumentation)](#4-论证过程-argumentation)
    - [4.1 连接器选型决策框架](#41-连接器选型决策框架)
    - [4.2 性能权衡分析](#42-性能权衡分析)
    - [4.3 故障场景与恢复策略](#43-故障场景与恢复策略)
  - [5. 形式证明 / 工程论证 (Proof / Engineering Argument)](#5-形式证明--工程论证-proof--engineering-argument)
    - [Thm-F-04-100 (连接器生态完备性定理)](#thm-f-04-100-连接器生态完备性定理)
    - [Thm-F-04-101 (多连接器组合一致性定理)](#thm-f-04-101-多连接器组合一致性定理)
  - [6. 实例验证 (Examples)](#6-实例验证-examples)
    - [6.1 消息队列连接器](#61-消息队列连接器)
      - [6.1.1 Kafka 连接器](#611-kafka-连接器)
      - [6.1.2 Apache Pulsar 连接器](#612-apache-pulsar-连接器)
      - [6.1.3 RabbitMQ 连接器](#613-rabbitmq-连接器)
      - [6.1.4 Amazon Kinesis 连接器](#614-amazon-kinesis-连接器)
      - [6.1.5 Google Cloud Pub/Sub 连接器](#615-google-cloud-pubsub-连接器)
      - [6.1.6 MQTT 连接器](#616-mqtt-连接器)
    - [6.2 文件系统连接器](#62-文件系统连接器)
      - [6.2.1 通用文件系统配置](#621-通用文件系统配置)
      - [6.2.2 文件 Source (Bulk Format)](#622-文件-source-bulk-format)
      - [6.2.3 文件 Sink (Streaming)](#623-文件-sink-streaming)
    - [6.3 数据库连接器](#63-数据库连接器)
      - [6.3.1 JDBC 连接器](#631-jdbc-连接器)
      - [6.3.2 Apache Cassandra 连接器](#632-apache-cassandra-连接器)
      - [6.3.3 Apache HBase 连接器](#633-apache-hbase-连接器)
      - [6.3.4 Elasticsearch 连接器](#634-elasticsearch-连接器)
      - [6.3.5 MongoDB 连接器](#635-mongodb-连接器)
      - [6.3.6 Redis 连接器](#636-redis-连接器)
      - [6.3.7 InfluxDB 连接器](#637-influxdb-连接器)
    - [6.4 Lakehouse 连接器](#64-lakehouse-连接器)
      - [6.4.1 Apache Iceberg 连接器](#641-apache-iceberg-连接器)
      - [6.4.2 Apache Hudi 连接器](#642-apache-hudi-连接器)
      - [6.4.3 Apache Paimon 连接器](#643-apache-paimon-连接器)
      - [6.4.4 Delta Lake 连接器](#644-delta-lake-连接器)
      - [6.4.5 Apache Fluss 连接器](#645-apache-fluss-连接器)
    - [6.5 CDC 连接器](#65-cdc-连接器)
      - [6.5.1 Flink CDC 3.0 基础配置](#651-flink-cdc-30-基础配置)
      - [6.5.2 CDC Pipeline YAML 配置](#652-cdc-pipeline-yaml-配置)
      - [6.5.3 CDC 到 Lakehouse](#653-cdc-到-lakehouse)
  - [7. 可视化 (Visualizations)](#7-可视化-visualizations)
    - [7.1 连接器生态全景图](#71-连接器生态全景图)
    - [7.2 连接器选型决策树](#72-连接器选型决策树)
    - [7.3 数据流集成架构图](#73-数据流集成架构图)
    - [7.4 连接器状态机](#74-连接器状态机)
  - [8. 配置参考与性能对比 (Configuration \& Performance)](#8-配置参考与性能对比-configuration--performance)
    - [8.1 全局配置最佳实践](#81-全局配置最佳实践)
    - [8.2 连接器性能对比矩阵](#82-连接器性能对比矩阵)
    - [8.3 常见问题排查指南](#83-常见问题排查指南)
  - [9. 引用参考 (References)](#9-引用参考-references)

---

## 1. 概念定义 (Definitions)

### Def-F-04-100 (Flink 连接器形式化定义)

**定义**: Flink 连接器是连接 Flink 计算引擎与外部数据系统的桥梁，实现了统一的数据读写接口，支持批处理和流处理两种模式。

**形式化结构**:

```
FlinkConnector = ⟨Type, Interface, Semantics, Config, Compatibility⟩

其中:
- Type: {Source, Sink, Lookup, Scan}
- Interface: DataStream API | Table API | SQL
- Semantics: {EXACTLY_ONCE, AT_LEAST_ONCE, AT_MOST_ONCE}
- Config: 配置参数空间 ⟨参数名, 类型, 默认值, 约束⟩
- Compatibility: 版本兼容性 ⟨FlinkVersion, ExternalSystemVersion⟩
```

**连接器类型分类**:

| 类型 | 方向 | 功能 | 典型场景 |
|------|------|------|----------|
| **Source** | 输入 | 从外部系统读取数据 | Kafka消费、数据库查询 |
| **Sink** | 输出 | 向外部系统写入数据 | 数据持久化、结果输出 |
| **Lookup** | 维表 | 点查外部系统 | 维表Join、数据补全 |
| **Scan** | 批读取 | 批量扫描外部数据 | 离线分析、全量同步 |

---

### Def-F-04-101 (连接器交付保证语义)

**定义**: 连接器交付保证定义了数据在传输过程中的可靠性级别，分为三个层次：

**形式化定义**:

```
设:
- E: 事件集合
- Src: Source 连接器产生的记录
- Sink: Sink 连接器写入的记录
- 理想情况: ∀e ∈ Src, ∃! s ∈ Sink: e ~ s (一一对应)

交付保证:
┌─────────────────────────────────────────────────────────────┐
│ EXACTLY_ONCE (恰好一次):                                    │
│   ∀e ∈ Src: |{s ∈ Sink | s ~ e}| = 1                       │
│   每个事件恰好被处理一次,无丢失、无重复                      │
├─────────────────────────────────────────────────────────────┤
│ AT_LEAST_ONCE (至少一次):                                   │
│   ∀e ∈ Src: |{s ∈ Sink | s ~ e}| ≥ 1                       │
│   每个事件至少被处理一次,允许重复                            │
├─────────────────────────────────────────────────────────────┤
│ AT_MOST_ONCE (至多一次):                                    │
│   ∀e ∈ Src: |{s ∈ Sink | s ~ e}| ≤ 1                       │
│   每个事件至多被处理一次,允许丢失                            │
└─────────────────────────────────────────────────────────────┘
```

**各连接器交付保证能力**:

| 连接器 | Source 保证 | Sink 保证 | 实现机制 |
|--------|-------------|-----------|----------|
| Kafka | EXACTLY_ONCE | EXACTLY_ONCE | 偏移量 + 事务 |
| Pulsar | EXACTLY_ONCE | EXACTLY_ONCE | 游标 + 事务 |
| JDBC | AT_LEAST_ONCE | EXACTLY_ONCE | Checkpoint + XA |
| Iceberg | EXACTLY_ONCE | EXACTLY_ONCE | 快照隔离 + 2PC |
| Files | EXACTLY_ONCE | EXACTLY_ONCE | 文件原子重命名 |
| Redis | AT_LEAST_ONCE | AT_LEAST_ONCE | 异步写入 |

---

### Def-F-04-102 (Source 连接器接口契约)

**定义**: Source 连接器必须实现 `Source` 接口，支持分片枚举、读取器创建和偏移量管理。

**形式化契约**:

```java
interface Source<T, SplitT extends SourceSplit, EnumChkT>
    extends SourceReaderFactory<T, SplitT> {

    // 创建分片枚举器,负责发现和分配数据分片
    SplitEnumerator<SplitT, EnumChkT> createEnumerator();

    // 从检查点恢复分片枚举器
    SplitEnumerator<SplitT, EnumChkT> restoreEnumerator(EnumChkT checkpoint);

    // 创建 SourceReader 工厂
    SourceReader<T, SplitT> createReader(SourceReaderContext context);

    // 序列化/反序列化分片
    SimpleVersionedSerializer<SplitT> getSplitSerializer();
    SimpleVersionedSerializer<EnumChkT> getEnumeratorCheckpointSerializer();
}
```

**Source 读取语义**:

| 语义 | 定义 | 适用场景 |
|------|------|----------|
| **Bounded** | 有限数据集，读取完成后结束 | 批处理、历史数据 |
| **Unbounded** | 无限数据流，持续读取 | 流处理、实时数据 |
| **Snapshot** | 基于时间点的快照读取 | 一致性备份、时间旅行 |
| **Incremental** | 增量读取变更数据 | CDC、增量同步 |

---

### Def-F-04-103 (Sink 连接器接口契约)

**定义**: Sink 连接器必须实现 `Sink` 接口，支持写入操作的两阶段提交以保证 Exactly-Once 语义。

**形式化契约**:

```java
interface Sink<InputT> {
    // 创建 SinkWriter,负责实际写入
    SinkWriter<InputT> createWriter(InitContext context);

    // 创建提交器(用于两阶段提交)
    Optional<Committer<?>> createCommitter();

    // 创建全局提交器(用于全局协调)
    Optional<GlobalCommitter<?, ?>> createGlobalCommitter();
}

// 两阶段提交接口
interface TwoPhaseCommitSinkFunction<IN, TXN, CONTEXT> {
    void beginTransaction();                    // 开始事务
    void preCommit(TXN transaction);           // 预提交
    void commit(TXN transaction);              // 提交事务
    void abort(TXN transaction);               // 中止事务
}
```

**Sink 写入模式**:

| 模式 | 延迟 | 吞吐 | 一致性 |
|------|------|------|--------|
| **Append** | 低 | 高 | 最终一致 |
| **Upsert** | 中 | 中 | 按主键去重 |
| **Batch** | 高 | 最高 | Checkpoint 边界 |
| **Streaming** | 低 | 高 | 事务保证 |

---

### Def-F-04-104 (连接器生态分层模型)

**定义**: Flink 连接器生态采用分层架构，从底层存储到上层应用形成完整的集成体系。

**分层结构**:

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 5: 应用层 (Application Layer)                          │
│  - CDC 数据同步、实时数仓、流式ETL、AI/ML 特征工程            │
├─────────────────────────────────────────────────────────────┤
│ Layer 4: 处理层 (Processing Layer)                           │
│  - Flink SQL/DataStream API、窗口计算、状态处理               │
├─────────────────────────────────────────────────────────────┤
│ Layer 3: 连接器层 (Connector Layer)                          │
│  - Source/Sink Connectors、Format 序列化                     │
├─────────────────────────────────────────────────────────────┤
│ Layer 2: 协议层 (Protocol Layer)                             │
│  - Kafka Protocol、JDBC、HTTP/REST、File Format              │
├─────────────────────────────────────────────────────────────┤
│ Layer 1: 存储层 (Storage Layer)                              │
│  - 消息队列、数据库、文件系统、对象存储                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 属性推导 (Properties)

### Lemma-F-04-100 (连接器组合封闭性)

**引理**: 多个 Flink 连接器组合使用时，整个数据流的语义在特定条件下保持封闭性。

**证明概要**:

```
设:
- C₁, C₂, ..., Cₙ 为一组连接器
- 每个连接器的语义函数: fᵢ: Input → Output
- 组合语义: F = fₙ ∘ fₙ₋₁ ∘ ... ∘ f₁

封闭性条件:
1. 类型兼容: ∀i: Output(fᵢ) ⊆ Input(fᵢ₊₁)
2. 序列化一致: 相邻连接器使用相同的序列化格式
3. 语义兼容: 上游的交付保证 ≥ 下游的要求

若满足上述条件,则组合后的数据流保持确定的语义。
```

**示例**:

| 组合 | 是否封闭 | 原因 |
|------|----------|------|
| Kafka Source → Iceberg Sink | ✅ | 两者支持 EXACTLY_ONCE |
| JDBC Source → Kafka Sink | ✅ | JDBC AT_LEAST_ONCE + Kafka EOS |
| Files Source → Redis Sink | ✅ | 最终一致性场景可接受 |
| Kafka Source → JDBC Sink (无XA) | ⚠️ | JDBC Sink 需额外配置保证一致性 |

---

### Lemma-F-04-101 (交付保证传递性)

**引理**: 端到端交付保证由数据流中最弱的连接器决定。

**形式化表述**:

```
设数据流包含 n 个连接器,其交付保证分别为 g₁, g₂, ..., gₙ
其中保证级别排序: AT_MOST_ONCE < AT_LEAST_ONCE < EXACTLY_ONCE

端到端保证: G_end_to_end = min(g₁, g₂, ..., gₙ)

示例:
- Kafka Source (EXACTLY_ONCE) → Processing → JDBC Sink (AT_LEAST_ONCE)
- 结果: 端到端保证为 AT_LEAST_ONCE
```

**提升策略**:

| 场景 | 策略 | 结果 |
|------|------|------|
| Source 为 AT_LEAST_ONCE | 启用幂等 Sink | 等效 EXACTLY_ONCE |
| Sink 为 AT_LEAST_ONCE | 使用事务 Sink (如 Kafka) | 提升为 EXACTLY_ONCE |
| 中间算子 | 启用 Checkpoint | 保持上游保证 |

---

### Prop-F-04-100 (端到端一致性约束)

**命题**: 实现端到端 Exactly-Once 需要满足三个必要条件：

1. **Source 可重放**: 支持从特定位置重新读取
2. **引擎一致性**: Flink Checkpoint 保证内部状态一致
3. **Sink 事务性**: 支持两阶段提交或幂等写入

**形式化推导**:

```
ExactlyOnce(Source, Engine, Sink) ⟺
    Replayable(Source) ∧
    ConsistentCheckpoint(Engine) ∧
    (Transactional(Sink) ∨ Idempotent(Sink))
```

**各连接器满足度**:

| 连接器 | 可重放 | 事务性 | 幂等性 | EO支持 |
|--------|--------|--------|--------|--------|
| Kafka | ✅ 偏移量 | ✅ 2PC | ✅ 幂等生产者 | ✅ |
| Pulsar | ✅ 游标 | ✅ 事务 | ✅ | ✅ |
| Iceberg | ✅ 快照 | ✅ 2PC | ✅ | ✅ |
| JDBC | ❌ 依赖查询 | ⚠️ XA有限 | ❌ | ⚠️ |
| Redis | ❌ | ❌ | ✅ 幂等操作 | ⚠️ |
| Files | ✅ 文件位置 | ✅ 原子重命名 | ✅ | ✅ |

---

### Prop-F-04-101 (连接器并行度扩展性)

**命题**: 连接器并行度受限于外部系统的分片/分区能力。

**形式化分析**:

```
设:
- P_Flink: Flink 并行度
- P_External: 外部系统分区数

最优并行度: P_optimal = min(P_Flink, P_External)

若 P_Flink > P_External:
  - 部分 Subtask 空闲,资源浪费

若 P_Flink < P_External:
  - 单个 Subtask 处理多个分区
  - 可能存在数据倾斜
```

**各连接器并行度约束**:

| 连接器 | 分区依据 | 最大并行度 | 动态扩展 |
|--------|----------|------------|----------|
| Kafka | Topic Partition | Partition 数 | ✅ 支持 |
| Pulsar | Partition | Partition 数 | ✅ 支持 |
| JDBC | Chunk/Shard | 数据库连接限制 | ⚠️ 有限 |
| Iceberg | File Split | 文件数 | ✅ 支持 |
| Files | Block/File | 文件数 | ✅ 支持 |
| Elasticsearch | Shard | Shard 数 | ⚠️ 有限 |

---

## 3. 关系建立 (Relations)

### 3.1 连接器分类体系

**消息队列连接器**:

```mermaid
graph TD
    MQ[消息队列连接器] --> KAFKA[Apache Kafka]
    MQ --> PULSAR[Apache Pulsar]
    MQ --> RABBIT[RabbitMQ]
    MQ --> KINESIS[Amazon Kinesis]
    MQ --> PUBSUB[Google Cloud Pub/Sub]
    MQ --> MQTT[MQTT Broker]

    KAFKA --> K_SOURCE[Kafka Source<br/>Offset管理]
    KAFKA --> K_SINK[Kafka Sink<br/>事务支持]

    PULSAR --> P_SOURCE[Pulsar Source<br/>Cursor管理]
    PULSAR --> P_SINK[Pulsar Sink<br/>事务支持]
```

**文件系统连接器**:

```mermaid
graph TD
    FS[文件系统连接器] --> LOCAL[本地文件系统]
    FS --> HDFS[HDFS]
    FS --> S3[Amazon S3]
    FS --> GCS[Google Cloud Storage]
    FS --> AZURE[Azure Blob Storage]
    FS --> OSS[Alibaba OSS]

    S3 --> S3_PARQUET[Parquet格式]
    S3 --> S3_ORC[ORC格式]
    S3 --> S3_CSV[CSV格式]
    S3 --> S3_JSON[JSON格式]

    HDFS --> HIVE_PARTITION[Hive分区]
    HDFS --> BUCKETING[分桶存储]
```

**数据库连接器**:

```mermaid
graph TD
    DB[数据库连接器] --> JDBC[JDBC连接器]
    DB --> CASSANDRA[Apache Cassandra]
    DB --> HBASE[Apache HBase]
    DB --> ES[Elasticsearch]
    DB --> MONGODB[MongoDB]
    DB --> REDIS[Redis]
    DB --> INFLUX[InfluxDB]

    JDBC --> MYSQL[MySQL]
    JDBC --> PG[PostgreSQL]
    JDBC --> ORACLE[Oracle]
    JDBC --> SQLSERVER[SQL Server]
    JDBC --> DB2[DB2]
```

**Lakehouse 连接器**:

```mermaid
graph TD
    LAKE[Lakehouse连接器] --> ICEBERG[Apache Iceberg]
    LAKE --> HUDI[Apache Hudi]
    LAKE --> PAIMON[Apache Paimon]
    LAKE --> DELTA[Delta Lake]
    LAKE --> FLUSS[Apache Fluss]

    ICEBERG --> ICE_SOURCE[Source<br/>快照读取]
    ICEBERG --> ICE_SINK[Sink<br/>UPSERT/Append]
    ICEBERG --> ICE_CATALOG[Catalog<br/>元数据管理]
```

---

### 3.2 连接器与存储系统映射

**功能特性映射矩阵**:

| 存储系统 | Source | Sink | Lookup | CDC Source | 事务支持 | 流批统一 |
|----------|--------|------|--------|------------|----------|----------|
| **Kafka** | ✅ | ✅ | ❌ | ✅ (CDC) | ✅ | ✅ |
| **Pulsar** | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| **RabbitMQ** | ✅ | ✅ | ❌ | ❌ | ❌ | ⚠️ |
| **Kinesis** | ✅ | ✅ | ❌ | ❌ | ⚠️ | ✅ |
| **JDBC** | ✅ | ✅ | ✅ | ⚠️ (需CDC) | ⚠️ (XA) | ✅ |
| **Cassandra** | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| **HBase** | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| **Elasticsearch** | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| **MongoDB** | ✅ | ✅ | ✅ | ✅ (CDC) | ⚠️ | ✅ |
| **Redis** | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| **Iceberg** | ✅ | ✅ | ❌ | ✅ (CDC) | ✅ | ✅ |
| **Hudi** | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| **Paimon** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

### 3.3 连接器版本兼容性矩阵

**Flink 版本与连接器版本对应**:

| 连接器 | Flink 1.14 | Flink 1.15 | Flink 1.16 | Flink 1.17 | Flink 1.18 | Flink 1.19+ |
|--------|------------|------------|------------|------------|------------|-------------|
| **Kafka** | 1.14.x | 1.15.x | 1.16.x | 3.0.x | 3.1.x | 3.2.x |
| **Pulsar** | 2.7.x | 2.8.x | 2.9.x | 3.0.x | 4.0.x | 4.1.x |
| **JDBC** | 1.14.x | 1.15.x | 1.16.x | 3.1.x | 3.1.x | 3.2.x |
| **Iceberg** | 0.13.x | 0.14.x | 1.0.x | 1.3.x | 1.4.x | 1.5.x+ |
| **Hudi** | 0.10.x | 0.11.x | 0.12.x | 0.13.x | 0.14.x | 0.15.x+ |
| **Paimon** | N/A | N/A | 0.4.x | 0.6.x | 0.8.x | 0.9.x+ |
| **Flink CDC** | 2.2.x | 2.3.x | 2.4.x | 3.0.x | 3.0.x | 3.1.x+ |

**外部系统版本兼容性**:

| 连接器 | 最低版本 | 推荐版本 | 最高测试版本 |
|--------|----------|----------|--------------|
| **Kafka** | 0.11 | 2.8+ / 3.5+ | 3.7 |
| **Pulsar** | 2.8 | 2.11+ / 3.0+ | 3.3 |
| **MySQL** | 5.6 | 8.0+ | 8.4 |
| **PostgreSQL** | 9.6 | 14+ | 16 |
| **Elasticsearch** | 6.8 | 7.17+ / 8.11+ | 8.14 |
| **MongoDB** | 3.6 | 5.0+ / 6.0+ | 7.0 |
| **Redis** | 3.0 | 6.2+ / 7.0+ | 7.2 |
| **Iceberg** | 0.13 | 1.4+ | 1.6 |

---

## 4. 论证过程 (Argumentation)

### 4.1 连接器选型决策框架

**决策维度分析**:

```
连接器选型需要综合考虑以下维度:

┌─────────────────────────────────────────────────────────────┐
│ 1. 功能需求                                                  │
│    - 需要 Source/Sink/Lookup/CDC 中的哪些能力?               │
│    - 是否需要 Exactly-Once 语义?                             │
│    - 延迟要求 (毫秒级/秒级/分钟级)?                          │
├─────────────────────────────────────────────────────────────┤
│ 2. 性能需求                                                  │
│    - 吞吐要求 (万/十万/百万条/秒)?                           │
│    - 是否需要水平扩展?                                       │
│    - 数据倾斜容忍度?                                         │
├─────────────────────────────────────────────────────────────┤
│ 3. 运维需求                                                  │
│    - 连接器成熟度与社区活跃度                                │
│    - 版本升级兼容性                                          │
│    - 监控指标丰富度                                          │
├─────────────────────────────────────────────────────────────┤
│ 4. 成本约束                                                  │
│    - 外部系统授权成本                                        │
│    - 基础设施成本                                            │
│    - 运维人力成本                                            │
└─────────────────────────────────────────────────────────────┘
```

**消息队列选型对比**:

| 维度 | Kafka | Pulsar | RabbitMQ | Kinesis | Pub/Sub |
|------|-------|--------|----------|---------|---------|
| **吞吐** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **延迟** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **扩展性** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **成本** | 低 | 中 | 低 | 高(AWS) | 中(GCP) |
| **生态** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **多租户** | ❌ | ✅ | ❌ | ✅ | ✅ |
| **地理复制** | ⚠️ | ✅ | ❌ | ✅ | ✅ |

---

### 4.2 性能权衡分析

**吞吐 vs 延迟权衡**:

```
Flink 连接器性能调优的核心是平衡吞吐和延迟:

高吞吐配置:
┌─────────────────────────────────────────────────────────────┐
│  - 增大 batch.size (Kafka: 32768, JDBC: 5000)              │
│  - 增大 buffer.memory (Kafka: 64MB+)                       │
│  - 增加 Checkpoint 间隔 (5-10分钟)                         │
│  - 启用压缩 (lz4/snappy)                                   │
│  - 结果: 高吞吐,较高延迟 (秒级)                            │
└─────────────────────────────────────────────────────────────┘

低延迟配置:
┌─────────────────────────────────────────────────────────────┐
│  - 减小 batch.size (Kafka: 16384)                          │
│  - 减小 linger.ms (Kafka: 0-5ms)                           │
│  - 减小 Checkpoint 间隔 (1-5秒)                            │
│  - 禁用压缩或压缩级别降低                                   │
│  - 结果: 低延迟 (毫秒级),较低吞吐                          │
└─────────────────────────────────────────────────────────────┘
```

**文件格式性能对比**:

| 格式 | 压缩率 | 读取速度 | 写入速度 | 列式存储 | Schema演进 |
|------|--------|----------|----------|----------|------------|
| **Parquet** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ✅ |
| **ORC** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ⚠️ |
| **Avro** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ | ✅ |
| **JSON** | ⭐⭐ | ⭐⭐ | ⭐⭐ | ❌ | ⚠️ |
| **CSV** | ⭐ | ⭐ | ⭐⭐ | ❌ | ❌ |

---

### 4.3 故障场景与恢复策略

**常见故障场景**:

| 故障类型 | 影响 | 恢复策略 | 预防措施 |
|----------|------|----------|----------|
| **网络分区** | 连接中断 | 自动重连 + 指数退避 | 多可用区部署 |
| **外部系统过载** | 写入失败 | 背压 + 重试队列 | 限流 + 扩容 |
| **Checkpoint 失败** | 状态不一致 | 从上一个成功点恢复 | 调优 Checkpoint 参数 |
| **Schema 变更** | 序列化失败 | Schema Registry + 兼容性检查 | 提前验证 Schema |
| **数据倾斜** | 部分 Subtask 积压 | 重新分区 + 负载均衡 | 合理选择分区键 |

**Source 故障恢复**:

```
场景: Kafka Source 消费延迟过高

诊断步骤:
1. 检查消费延迟指标: records-lag-max
2. 检查 Flink 反压指标: backPressuredTimeMsPerSecond
3. 检查 Kafka 分区分布: 是否存在数据倾斜?

解决策略:
┌─────────────────────────────────────────────────────────────┐
│ 若分区数 < 并行度:                                           │
│   - 增加 Kafka 分区数                                        │
│   - 调整 Flink 并行度匹配分区数                              │
│                                                             │
│ 若存在数据倾斜:                                              │
│   - 检查 Key 分布,考虑加盐                                  │
│   - 调整分区策略                                             │
│                                                             │
│ 若处理逻辑复杂:                                              │
│   - 优化处理算子                                             │
│   - 增加并行度                                               │
└─────────────────────────────────────────────────────────────┘
```

**Sink 故障恢复**:

```
场景: JDBC Sink 连接超时

诊断步骤:
1. 检查数据库连接池状态
2. 检查网络延迟和稳定性
3. 检查数据库负载

解决策略:
┌─────────────────────────────────────────────────────────────┐
│ 连接超时:                                                    │
│   - 增加 connection.timeout                                  │
│   - 配置连接池最大连接数                                     │
│                                                             │
│ 写入超时:                                                    │
│   - 减小 batch.size                                          │
│   - 增加写入超时时间                                         │
│                                                             │
│ 主键冲突:                                                    │
│   - 启用 UPSERT 模式                                         │
│   - 检查数据唯一性                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. 形式证明 / 工程论证 (Proof / Engineering Argument)

### Thm-F-04-100 (连接器生态完备性定理)

**定理**: Flink 连接器生态覆盖主流数据存储系统，能够满足企业级数据集成需求。

**证明**:

**前提假设**:

- P1: 企业数据存储可分为消息队列、文件系统、数据库、数据湖四大类
- P2: 每类存储系统有行业主流实现
- P3: Flink 为每类主流实现提供官方或社区连接器

**分类论证**:

```
消息队列类 (Streaming Data Ingestion):
┌─────────────────────────────────────────────────────────────┐
│ 主流系统: Kafka, Pulsar, RabbitMQ, Kinesis, Pub/Sub        │
│ Flink 支持: ✅ 官方连接器覆盖所有主流系统                    │
│ 语义保证: ✅ Source/Sink 均支持 EXACTLY_ONCE              │
└─────────────────────────────────────────────────────────────┘

文件系统类 (Batch Data Storage):
┌─────────────────────────────────────────────────────────────┐
│ 主流系统: HDFS, S3, GCS, Azure Blob, OSS                   │
│ Flink 支持: ✅ 统一 FileSystem 抽象,支持所有主流对象存储   │
│ 格式支持: ✅ Parquet/ORC/Avro/JSON/CSV                    │
└─────────────────────────────────────────────────────────────┘

数据库类 (Structured Data Storage):
┌─────────────────────────────────────────────────────────────┐
│ 关系型: MySQL, PostgreSQL, Oracle, SQL Server, DB2         │
│ NoSQL: Cassandra, MongoDB, HBase, Elasticsearch, Redis     │
│ Flink 支持: ✅ JDBC 通用 + 专用连接器覆盖                   │
│ 查询能力: ✅ Source/Sink/Lookup 支持                       │
└─────────────────────────────────────────────────────────────┘

数据湖类 (Lakehouse Storage):
┌─────────────────────────────────────────────────────────────┐
│ 主流格式: Iceberg, Hudi, Paimon, Delta Lake, Fluss         │
│ Flink 支持: ✅ 与所有主流格式深度集成                       │
│ 流批统一: ✅ 支持流式写入和批式查询                         │
└─────────────────────────────────────────────────────────────┘

综上,Flink 连接器生态在四大存储类别中均有完整覆盖,完备性得证。∎
```

---

### Thm-F-04-101 (多连接器组合一致性定理)

**定理**: 在 Flink 中，多个连接器组合使用时，通过 Checkpoint 机制可以保证端到端一致性。

**证明**:

**系统模型**:

```
设数据流为: Source → [Operators] → Sink

定义:
- S: Source 连接器,产生记录序列 ⟨e₁, e₂, ..., eₙ⟩
- O: 算子集合,处理记录并维护状态
- K: Sink 连接器,输出记录到外部系统
- C: Checkpoint 协调器,周期触发一致性快照
```

**两阶段提交流程**:

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: Checkpoint 触发                                    │
│ ─────────────────────────────────────────────────────────  │
│ 1. CheckpointCoordinator 向所有算子发送 Checkpoint Barrier │
│ 2. Source: 保存当前读取位置到 StateBackend                  │
│ 3. Operators: 保存计算状态到 StateBackend                   │
│ 4. Sink: 执行 preCommit(),准备事务                         │
│                                                             │
│ 不变式 I1: 所有 preCommit 完成前,Sink 输出不可见           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Phase 2: Checkpoint 完成                                    │
│ ─────────────────────────────────────────────────────────  │
│ 触发条件: 所有算子完成 snapshotState                        │
│                                                             │
│ 操作:                                                       │
│ 1. CheckpointCoordinator 确认全局快照成功                   │
│ 2. Source: 可选地提交偏移量到外部系统                        │
│ 3. Sink: 执行 commit(),事务提交,输出可见                   │
│                                                             │
│ 不变式 I2: Checkpoint 成功后,Sink 输出永久可见             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 故障恢复场景                                                │
│ ─────────────────────────────────────────────────────────  │
│ 场景1: Checkpoint 进行中失败                                │
│   - 触发 notifyCheckpointAborted()                          │
│   - Sink 执行 abort(),回滚事务                             │
│   - 从上一个成功 Checkpoint 恢复                            │
│   - 结果: 无数据丢失,无重复                                │
│                                                             │
│ 场景2: Checkpoint 成功后 Sink 提交前失败                    │
│   - 新 Sink 实例从 Checkpoint 恢复                          │
│   - 重新执行 commit() (幂等)                                │
│   - 结果: 数据不重复                                        │
│                                                             │
│ 场景3: Source 故障                                          │
│   - 从 StateBackend 恢复读取位置                            │
│   - 重新消费未确认的数据                                    │
│   - 结果: At-Least-Once,配合 Sink 幂等实现 Exactly-Once   │
└─────────────────────────────────────────────────────────────┘
```

**一致性保证**:

| 条件 | 保证 | 依赖 |
|------|------|------|
| Source 可重放 | 不丢失 | 偏移量/快照持久化 |
| Checkpoint 成功 | 状态一致 | Barrier 对齐 |
| Sink 事务提交 | 输出不重复 | 2PC/幂等机制 |
| 三者结合 | Exactly-Once | 系统协同 |

综上，多连接器组合一致性得证。∎

---

## 6. 实例验证 (Examples)

### 6.1 消息队列连接器

#### 6.1.1 Kafka 连接器

**Maven 依赖**:

```xml
<!-- Kafka Connector -->
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-kafka</artifactId>
    <version>3.2.0-1.19</version>
</dependency>
```

**Source 配置**:

```java

import org.apache.flink.streaming.api.datastream.DataStream;

// Kafka Source (Flink 1.14+ 新 API)
KafkaSource<String> source = KafkaSource.<String>builder()
    .setBootstrapServers("kafka-1:9092,kafka-2:9092")
    .setTopics("input-topic")
    .setGroupId("flink-consumer-group")
    .setStartingOffsets(OffsetsInitializer.earliest())
    .setValueOnlyDeserializer(new SimpleStringSchema())
    .setProperty("partition.discovery.interval.ms", "10000")
    .setProperty("isolation.level", "read_committed")
    .build();

DataStream<String> stream = env.fromSource(
    source,
    WatermarkStrategy.forBoundedOutOfOrderness(Duration.ofSeconds(5)),
    "Kafka Source"
);
```

**Sink 配置**:

```java
// Kafka Sink with Exactly-Once
KafkaSink<String> sink = KafkaSink.<String>builder()
    .setBootstrapServers("kafka-1:9092,kafka-2:9092")
    .setRecordSerializer(KafkaRecordSerializationSchema.builder()
        .setTopic("output-topic")
        .setValueSerializationSchema(new SimpleStringSchema())
        .build())
    .setDeliveryGuarantee(DeliveryGuarantee.EXACTLY_ONCE)
    .setProperty("transaction.timeout.ms", "900000")
    .setProperty("enable.idempotence", "true")
    .setTransactionalIdPrefix("flink-job-")
    .build();

stream.sinkTo(sink);
```

**关键配置参数**:

| 参数 | Source/Sink | 默认值 | 说明 |
|------|-------------|--------|------|
| `bootstrap.servers` | Both | 必填 | Kafka 集群地址 |
| `group.id` | Source | 必填 | 消费者组 ID |
| `auto.offset.reset` | Source | latest | 起始偏移量策略 |
| `isolation.level` | Source | read_uncommitted | 隔离级别 |
| `enable.idempotence` | Sink | true | 幂等生产者 |
| `transaction.timeout.ms` | Sink | 60000 | 事务超时 |
| `delivery.guarantee` | Sink | AT_LEAST_ONCE | 交付保证 |

---

#### 6.1.2 Apache Pulsar 连接器

**Maven 依赖**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-pulsar</artifactId>
    <version>4.1.0-1.19</version>
</dependency>
```

**Source 配置**:

```java

import org.apache.flink.streaming.api.datastream.DataStream;

// Pulsar Source
PulsarSource<String> source = PulsarSource.builder()
    .setServiceUrl("pulsar://pulsar-broker:6650")
    .setAdminUrl("http://pulsar-admin:8080")
    .setTopics("persistent://public/default/input-topic")
    .setDeserializationSchema(new SimpleStringSchema())
    .setSubscriptionName("flink-subscription")
    .setSubscriptionType(SubscriptionType.Exclusive)
    .setStartCursor(StartCursor.earliest())
    .setBoundedStopCursor(StopCursor.never())
    .build();

DataStream<String> stream = env.fromSource(
    source,
    WatermarkStrategy.noWatermarks(),
    "Pulsar Source"
);
```

**Sink 配置**:

```java
// Pulsar Sink
PulsarSink<String> sink = PulsarSink.builder()
    .setServiceUrl("pulsar://pulsar-broker:6650")
    .setAdminUrl("http://pulsar-admin:8080")
    .setTopics("persistent://public/default/output-topic")
    .setSerializationSchema(new SimpleStringSchema())
    .setDeliveryGuarantee(DeliveryGuarantee.EXACTLY_ONCE)
    .setConfig(PulsarOptions.PULSAR_TRANSACTION_TIMEOUT_MILLIS, 600000L)
    .build();

stream.sinkTo(sink);
```

---

#### 6.1.3 RabbitMQ 连接器

**Maven 依赖**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-rabbitmq</artifactId>
    <version>3.0.1-1.17</version>
</dependency>
```

**Source/Sink 配置**:

```java

import org.apache.flink.streaming.api.datastream.DataStream;

// RabbitMQ Connection Config
RMQConnectionConfig connectionConfig = new RMQConnectionConfig.Builder()
    .setHost("rabbitmq-host")
    .setPort(5672)
    .setUserName("user")
    .setPassword("password")
    .setVirtualHost("/")
    .build();

// RabbitMQ Source
DataStream<String> stream = env.addSource(
    new RMQSource<>(
        connectionConfig,
        "input-queue",
        true,  // useCorrelationId
        new SimpleStringSchema()
    )
).setParallelism(1);

// RabbitMQ Sink
RMQSink<String> sink = new RMQSink<>(
    connectionConfig,
    "output-queue",
    new SimpleStringSchema()
);

stream.addSink(sink);
```

---

#### 6.1.4 Amazon Kinesis 连接器

**Maven 依赖**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-aws-kinesis-streams</artifactId>
    <version>4.3.0-1.19</version>
</dependency>
```

**Source 配置**:

```java

import org.apache.flink.streaming.api.datastream.DataStream;

// Kinesis Source
Properties consumerConfig = new Properties();
consumerConfig.put(AWSConfigConstants.AWS_REGION, "us-east-1");
consumerConfig.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "access-key");
consumerConfig.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "secret-key");

KinesisSource<String> source = KinesisSource.<String>builder()
    .setKinesisStreamName("input-stream")
    .setConsumerConfig(consumerConfig)
    .setDeserializationSchema(new SimpleStringSchema())
    .setInitialPosition(StreamPosition.LATEST)
    .build();

DataStream<String> stream = env.fromSource(
    source,
    WatermarkStrategy.forBoundedOutOfOrderness(Duration.ofSeconds(5)),
    "Kinesis Source"
);
```

**Sink 配置**:

```java
// Kinesis Sink
Properties producerConfig = new Properties();
producerConfig.put(AWSConfigConstants.AWS_REGION, "us-east-1");

KinesisStreamsSink<String> sink = KinesisStreamsSink.<String>builder()
    .setKinesisClientProperties(producerConfig)
    .setSerializationSchema(new SimpleStringSchema())
    .setPartitionKeyGenerator(element -> String.valueOf(element.hashCode()))
    .setStreamName("output-stream")
    .setFailOnError(false)
    .setMaxBatchSize(500)
    .setMaxInFlightRequests(50)
    .setMaxBufferedRequests(10000)
    .setMaxBatchSizeInBytes(5 * 1024 * 1024)
    .setMaxTimeInBufferMS(5000)
    .build();

stream.sinkTo(sink);
```

---

#### 6.1.5 Google Cloud Pub/Sub 连接器

**Maven 依赖**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-gcp-pubsub</artifactId>
    <version>3.0.1-1.17</version>
</dependency>
```

**Source/Sink 配置**:

```java

import org.apache.flink.streaming.api.datastream.DataStream;

// Pub/Sub Source
DeserializationSchema<String> deserializer = new SimpleStringSchema();

PubSubSource<String> source = PubSubSource.newBuilder()
    .withDeserializationSchema(deserializer)
    .withProjectName("my-project")
    .withSubscriptionName("my-subscription")
    .withCredentials(GoogleCredentials.fromStream(new FileInputStream("key.json")))
    .build();

DataStream<String> stream = env.addSource(source);

// Pub/Sub Sink
PubSubSink<String> sink = PubSubSink.newBuilder()
    .withSerializationSchema(new SimpleStringSchema())
    .withProjectName("my-project")
    .withTopicName("my-topic")
    .withCredentials(GoogleCredentials.fromStream(new FileInputStream("key.json")))
    .build();

stream.addSink(sink);
```

---

#### 6.1.6 MQTT 连接器

**Maven 依赖**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-mqtt</artifactId>
    <version>3.0.0-1.17</version>
</dependency>
```

**Source/Sink 配置**:

```java

import org.apache.flink.streaming.api.datastream.DataStream;

// MQTT Source
MQTTSource<String> source = MQTTSource.<String>builder()
    .setBrokerUrl("tcp://mqtt-broker:1883")
    .setTopics(Arrays.asList("sensor/temperature", "sensor/humidity"))
    .setClientIdPrefix("flink-mqtt-client")
    .setDeserializationSchema(new SimpleStringSchema())
    .setQoS(1)
    .setAutomaticReconnect(true)
    .setCleanSession(false)
    .build();

DataStream<String> stream = env.fromSource(
    source,
    WatermarkStrategy.noWatermarks(),
    "MQTT Source"
);

// MQTT Sink
MQTTSink<String> sink = MQTTSink.<String>builder()
    .setBrokerUrl("tcp://mqtt-broker:1883")
    .setTopic("output/topic")
    .setClientId("flink-mqtt-sink")
    .setSerializationSchema(new SimpleStringSchema())
    .setQoS(1)
    .setRetained(false)
    .build();

stream.sinkTo(sink);
```

---

### 6.2 文件系统连接器

#### 6.2.1 通用文件系统配置

**支持的文件系统**:

| 文件系统 | Scheme | 依赖 | 说明 |
|----------|--------|------|------|
| 本地文件 | `file://` | 内置 | 本地测试 |
| HDFS | `hdfs://` | hadoop-client | 分布式文件系统 |
| S3 | `s3://` | flink-s3-fs | AWS 对象存储 |
| GCS | `gs://` | flink-gs-fs | Google 对象存储 |
| Azure | `wasb://` | flink-azure-fs | Azure Blob |
| OSS | `oss://` | flink-oss-fs | 阿里云对象存储 |

**文件系统配置示例**:

```java
// 创建 FileSystem 实例
FileSystem fs = FileSystem.get(new URI("s3://my-bucket/data"));

// S3 配置
Configuration conf = new Configuration();
conf.setString("s3.access-key", "AKIA...");
conf.setString("s3.secret-key", "...");
conf.setString("s3.endpoint", "s3.amazonaws.com");

// 注册文件系统
FileSystem.initialize(conf, null);
```

---

#### 6.2.2 文件 Source (Bulk Format)

**Parquet 文件读取**:

```java

import org.apache.flink.streaming.api.datastream.DataStream;

// Parquet Source
FileSource<Row> source = FileSource.forRecordStreamFormat(
    new ParquetRecordFormat(),
    new Path("s3://bucket/data/")
).build();

DataStream<Row> stream = env.fromSource(
    source,
    WatermarkStrategy.noWatermarks(),
    "Parquet File Source"
);
```

**Avro 文件读取**:

```java
// Avro Source with Schema
Schema schema = new Schema.Parser().parse(
    new File("user.avsc")
);

FileSource<GenericRecord> source = FileSource.forRecordStreamFormat(
    new AvroRecordFormat<>(schema),
    new Path("hdfs://namenode/data/")
).build();
```

---

#### 6.2.3 文件 Sink (Streaming)

**Parquet 文件写入**:

```java
// Streaming File Sink with Parquet
final StreamingFileSink<Row> sink = StreamingFileSink
    .forBulkFormat(
        new Path("s3://bucket/output/"),
        ParquetRowFormat.forRowType(
            rowType,
            HadoopCompressionCodecName.SNAPPY
        )
    )
    .withBucketAssigner(new DateTimeBucketAssigner<>("yyyy-MM-dd--HH"))
    .withRollingPolicy(
        OnCheckpointRollingPolicy.build()
    )
    .build();

stream.addSink(sink);
```

**Flink 1.14+ FileSink API**:

```java
// New FileSink API (Recommended)
FileSink<Row> sink = FileSink.forBulkFormat(
    new Path("s3://bucket/output/"),
    ParquetAvroWriters.forSpecificRecord(User.class)
)
.withBucketAssigner(new DateTimeBucketAssigner<>())
.withRollingPolicy(
    DefaultRollingPolicy.builder()
        .withRolloverInterval(Duration.ofMinutes(15))
        .withInactivityInterval(Duration.ofMinutes(5))
        .withMaxPartSize(MemorySize.ofMebiBytes(128))
        .build()
)
.withBucketCheckInterval(Duration.ofSeconds(10))
.build();

stream.sinkTo(sink);
```

---

### 6.3 数据库连接器

#### 6.3.1 JDBC 连接器

**Maven 依赖**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-jdbc</artifactId>
    <version>3.2.0-1.19</version>
</dependency>
<!-- 数据库驱动 -->
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.33</version>
</dependency>
```

**JDBC Source**:

```java

import org.apache.flink.streaming.api.datastream.DataStream;

// JDBC Source (Bounded)
JdbcSource<Row> source = JdbcSource.<Row>builder()
    .setUrl("jdbc:mysql://localhost:3306/mydb")
    .setDriverName("com.mysql.cj.jdbc.Driver")
    .setUsername("user")
    .setPassword("password")
    .setQuery("SELECT id, name, amount FROM orders WHERE create_time > ?")
    .setRowTypeInfo(rowTypeInfo)
    .setFetchSize(1000)
    .build();

DataStream<Row> stream = env.fromSource(
    source,
    WatermarkStrategy.noWatermarks(),
    "JDBC Source"
);
```

**JDBC Sink**:

```java
// JDBC Sink with Exactly-Once (XA)
JdbcExactlyOnceSink<Row> sink = JdbcExactlyOnceSink.sink(
    "INSERT INTO orders (id, name, amount) VALUES (?, ?, ?) " +
    "ON DUPLICATE KEY UPDATE amount = VALUES(amount)",
    (ps, row) -> {
        ps.setLong(1, row.getField(0));
        ps.setString(2, row.getField(1));
        ps.setBigDecimal(3, row.getField(2));
    },
    JdbcExecutionOptions.builder()
        .withBatchSize(1000)
        .withBatchIntervalMs(200)
        .withMaxRetries(3)
        .build(),
    JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
        .withUrl("jdbc:mysql://localhost:3306/mydb")
        .withDriverName("com.mysql.cj.jdbc.Driver")
        .withUsername("user")
        .withPassword("password")
        .build()
);

stream.addSink(sink);
```

**JDBC Lookup Join**:

```sql
-- Flink SQL Lookup Join
CREATE TABLE orders (
    order_id STRING,
    user_id STRING,
    amount DECIMAL(10, 2),
    proctime AS PROCTIME()
) WITH (
    'connector' = 'kafka',
    ...
);

CREATE TABLE users (
    user_id STRING,
    user_name STRING,
    age INT,
    PRIMARY KEY (user_id) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:mysql://localhost:3306/mydb',
    'table-name' = 'users',
    'username' = 'user',
    'password' = 'password',
    'lookup.cache.max-rows' = '5000',
    'lookup.cache.ttl' = '10 min'
);

-- Lookup Join
SELECT o.order_id, o.amount, u.user_name
FROM orders AS o
LEFT JOIN users FOR SYSTEM_TIME AS OF o.proctime AS u
ON o.user_id = u.user_id;
```

---

#### 6.3.2 Apache Cassandra 连接器

**Maven 依赖**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-cassandra_2.12</artifactId>
    <version>3.1.0-1.17</version>
</dependency>
```

**Cassandra Sink**:

```java
// Cassandra Sink
ClusterBuilder clusterBuilder = new ClusterBuilder() {
    @Override
    protected Cluster buildCluster(Cluster.Builder builder) {
        return builder.addContactPoint("cassandra-host")
            .withPort(9042)
            .withCredentials("username", "password")
            .build();
    }
};

CassandraSink.addSink(stream)
    .setQuery("INSERT INTO mykeyspace.orders (id, name, amount) VALUES (?, ?, ?)")
    .setClusterBuilder(clusterBuilder)
    .setFailureHandler(new CassandraFailureHandler() {
        @Override
        public void onFailure(Throwable throwable) {
            // 处理写入失败
        }
    })
    .build();
```

---

#### 6.3.3 Apache HBase 连接器

**Maven 依赖**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-hbase-2.2</artifactId>
    <version>3.0.0-1.17</version>
</dependency>
```

**HBase Source/Sink**:

```java
// HBase Source
HBaseSourceFunction<Row> source = new HBaseSourceFunction<>(
    "mytable",
    new HBaseConfiguration(),
    rowTypeInfo,
    row -> {
        // 转换 HBase Result 到 Row
    }
);

// HBase Sink
HBaseSinkFunction<Row> sink = new HBaseSinkFunction<>(
    "mytable",
    new HBaseConfiguration(),
    row -> {
        // 将 Row 转换为 Put
        return new Put(Bytes.toBytes(row.getField(0).toString()))
            .addColumn(Bytes.toBytes("cf"), Bytes.toBytes("col"),
                      Bytes.toBytes(row.getField(1).toString()));
    }
);

stream.addSink(sink);
```

---

#### 6.3.4 Elasticsearch 连接器

**Maven 依赖**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-elasticsearch8</artifactId>
    <version>3.0.1-1.17</version>
</dependency>
```

**Elasticsearch Sink**:

```java
// Elasticsearch Sink
List<HttpHost> httpHosts = Arrays.asList(
    new HttpHost("es-host-1", 9200),
    new HttpHost("es-host-2", 9200)
);

ElasticsearchSink.Builder<String> builder = new ElasticsearchSink.Builder<>(
    httpHosts,
    new ElasticsearchSinkFunction<String>() {
        @Override
        public void process(String element, RuntimeContext ctx,
                           RequestIndexer indexer) {
            indexer.add(new IndexRequest("my-index")
                .id(element.getId())
                .source(element, XContentType.JSON));
        }
    }
);

builder.setBulkFlushMaxActions(1000);
builder.setBulkFlushInterval(5000);
builder.setFailureHandler(new RetryRejectedExecutionFailureHandler());

stream.addSink(builder.build());
```

---

#### 6.3.5 MongoDB 连接器

**Maven 依赖**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-mongodb</artifactId>
    <version>1.2.0</version>
</dependency>
```

**MongoDB Source/Sink**:

```java

import org.apache.flink.streaming.api.datastream.DataStream;

// MongoDB Source
MongoSource<String> source = MongoSource.<String>builder()
    .setUri("mongodb://user:password@mongodb:27017")
    .setDatabase("mydb")
    .setCollection("events")
    .setDeserializationSchema(new JsonDeserializationSchema())
    .setFetchSize(1000)
    .build();

DataStream<String> stream = env.fromSource(
    source,
    WatermarkStrategy.noWatermarks(),
    "MongoDB Source"
);

// MongoDB Sink
MongoSink<Document> sink = MongoSink.<Document>builder()
    .setUri("mongodb://user:password@mongodb:27017")
    .setDatabase("mydb")
    .setCollection("output")
    .setSerializationSchema(
        (doc, ctx) -> new InsertOneModel<>(doc)
    )
    .build();

stream.map(Json::parse).map(Document::parse).sinkTo(sink);
```

---

#### 6.3.6 Redis 连接器

**Maven 依赖** (社区连接器):

```xml
<dependency>
    <groupId>io.github.leefige</groupId>
    <artifactId>flink-connector-redis</artifactId>
    <version>1.3.0</version>
</dependency>
```

**Redis Sink**:

```java
// Redis Sink Configuration
FlinkJedisPoolConfig conf = new FlinkJedisPoolConfig.Builder()
    .setHost("redis-host")
    .setPort(6379)
    .setPassword("password")
    .setDatabase(0)
    .setMaxTotal(100)
    .setMaxIdle(50)
    .setMinIdle(10)
    .build();

// Redis Sink
RedisSink<Tuple2<String, String>> redisSink = new RedisSink<>(
    conf,
    new RedisMapper<Tuple2<String, String>>() {
        @Override
        public RedisCommandDescription getCommandDescription() {
            return new RedisCommandDescription(RedisCommand.HSET, "myhash");
        }

        @Override
        public String getKeyFromData(Tuple2<String, String> data) {
            return data.f0;
        }

        @Override
        public String getValueFromData(Tuple2<String, String> data) {
            return data.f1;
        }
    }
);

stream.addSink(redisSink);
```

---

#### 6.3.7 InfluxDB 连接器

**Maven 依赖** (社区连接器):

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-influxdb</artifactId>
    <version>1.0.0</version>
</dependency>
```

**InfluxDB Sink**:

```java
// InfluxDB Sink
InfluxDBSink<String> sink = InfluxDBSink.builder()
    .setInfluxDBUrl("http://influxdb:8086")
    .setInfluxDBUsername("user")
    .setInfluxDBPassword("password")
    .setDatabase("metrics")
    .setMeasurement("events")
    .setSerializationSchema((element, ctx) -> {
        return Point.measurement("events")
            .time(System.currentTimeMillis(), TimeUnit.MILLISECONDS)
            .tag("type", "click")
            .addField("value", element)
            .build();
    })
    .setWriteBufferSize(1000)
    .setFlushInterval(1000)
    .build();

stream.sinkTo(sink);
```

---

### 6.4 Lakehouse 连接器

#### 6.4.1 Apache Iceberg 连接器

**Maven 依赖**:

```xml
<dependency>
    <groupId>org.apache.iceberg</groupId>
    <artifactId>iceberg-flink-runtime-1.19</artifactId>
    <version>1.5.0</version>
</dependency>
```

**Iceberg Catalog 配置**:

```java
// Hive Catalog
CatalogLoader catalogLoader = CatalogLoader.hive(
    "hive_catalog",
    new Configuration(),
    ImmutableMap.of(
        "uri", "thrift://hive-metastore:9083",
        "warehouse", "s3://bucket/warehouse",
        "io-impl", "org.apache.iceberg.aws.s3.S3FileIO"
    )
);

Catalog catalog = catalogLoader.loadCatalog();
```

**Iceberg SQL 集成**:

```sql
-- 创建 Iceberg Catalog
CREATE CATALOG iceberg_catalog WITH (
    'type' = 'iceberg',
    'catalog-type' = 'hive',
    'uri' = 'thrift://hive-metastore:9083',
    'warehouse' = 's3://bucket/warehouse',
    'io-impl' = 'org.apache.iceberg.aws.s3.S3FileIO'
);

USE CATALOG iceberg_catalog;

-- 创建 Iceberg 表
CREATE TABLE user_events (
    user_id STRING,
    event_type STRING,
    event_time TIMESTAMP(3),
    properties MAP<STRING, STRING>
) PARTITIONED BY (
    days(event_time)
) WITH (
    'write.format.default' = 'parquet',
    'write.parquet.compression-codec' = 'zstd',
    'write.target-file-size-bytes' = '134217728',
    'read.streaming.enabled' = 'true',
    'read.streaming.start-mode' = 'earliest'
);

-- 流式写入
INSERT INTO user_events
SELECT user_id, event_type, event_time, properties
FROM kafka_source;
```

**Iceberg Source (流式读取)**:

```java

import org.apache.flink.streaming.api.datastream.DataStream;

// Iceberg Streaming Source
Table table = catalog.loadTable(TableIdentifier.of("db", "user_events"));

IcebergSource<Row> source = IcebergSource.forRowData()
    .tableLoader(() -> table)
    .streaming(true)
    .monitorInterval(Duration.ofSeconds(10))
    .startSnapshotId(table.currentSnapshot().snapshotId())
    .build();

DataStream<Row> stream = env.fromSource(
    source,
    WatermarkStrategy.forBoundedOutOfOrderness(Duration.ofSeconds(5)),
    "Iceberg Source"
);
```

---

#### 6.4.2 Apache Hudi 连接器

**Maven 依赖**:

```xml
<dependency>
    <groupId>org.apache.hudi</groupId>
    <artifactId>hudi-flink1.19-bundle</artifactId>
    <version>0.14.0</version>
</dependency>
```

**Hudi SQL 集成**:

```sql
-- 创建 Hudi 表
CREATE TABLE hudi_users (
    id STRING PRIMARY KEY NOT ENFORCED,
    name STRING,
    age INT,
    ts TIMESTAMP(3)
) WITH (
    'connector' = 'hudi',
    'path' = 's3://bucket/hudi/users',
    'table.type' = 'MERGE_ON_READ',
    'write.operation' = 'upsert',
    'write.precombine.field' = 'ts',
    'write.tasks' = '4',
    'compaction.tasks' = '4',
    'compaction.schedule.enabled' = 'true',
    'compaction.delta_commits' = '5'
);

-- UPSERT 写入
INSERT INTO hudi_users
SELECT id, name, age, ts FROM kafka_users;
```

---

#### 6.4.3 Apache Paimon 连接器

**Maven 依赖**:

```xml
<dependency>
    <groupId>org.apache.paimon</groupId>
    <artifactId>paimon-flink-1.19</artifactId>
    <version>0.8.0</version>
</dependency>
```

**Paimon SQL 集成**:

```sql
-- 创建 Paimon Catalog
CREATE CATALOG paimon_catalog WITH (
    'type' = 'paimon',
    'warehouse' = 's3://bucket/paimon',
    's3.endpoint' = 's3.amazonaws.com'
);

USE CATALOG paimon_catalog;

-- 创建 Paimon 表
CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY NOT ENFORCED,
    user_id STRING,
    product_id STRING,
    amount DECIMAL(10, 2),
    order_time TIMESTAMP(3)
) WITH (
    'bucket' = '8',
    'bucket-key' = 'order_id',
    'changelog-producer' = 'input',
    'merge-engine' = 'deduplicate',
    'sequence.field' = 'order_time'
);

-- 流式写入
INSERT INTO orders
SELECT * FROM kafka_orders;
```

---

#### 6.4.4 Delta Lake 连接器

**Maven 依赖**:

```xml
<dependency>
    <groupId>io.delta</groupId>
    <artifactId>delta-flink</artifactId>
    <version>3.2.0</version>
</dependency>
```

**Delta Lake Sink**:

```java
// Delta Lake Sink
DeltaSink<Row> deltaSink = DeltaSink
    .forRowData(
        new Path("s3://bucket/delta-table/"),
        new Configuration(),
        rowType
    )
    .withPartitionColumns("date")
    .build();

stream.sinkTo(deltaSink);
```

---

#### 6.4.5 Apache Fluss 连接器

**Maven 依赖**:

```xml
<dependency>
    <groupId>org.apache.fluss</groupId>
    <artifactId>fluss-flink-connector</artifactId>
    <version>0.5.0</version>
</dependency>
```

**Fluss SQL 集成**:

```sql
-- 创建 Fluss Catalog
CREATE CATALOG fluss_catalog WITH (
    'type' = 'fluss',
    'bootstrap.servers' = 'fluss-server:9123'
);

USE CATALOG fluss_catalog;

-- 创建 Fluss 表 (Streaming Lakehouse)
CREATE TABLE realtime_events (
    event_id STRING PRIMARY KEY NOT ENFORCED,
    user_id STRING,
    event_data STRING,
    event_time TIMESTAMP(3),
    WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
) WITH (
    'kafka.retention.time' = '7d',
    'lakehouse.trigger.interval' = '1h'
);
```

---

### 6.5 CDC 连接器

#### 6.5.1 Flink CDC 3.0 基础配置

**Maven 依赖**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-cdc-dist</artifactId>
    <version>3.0.1</version>
</dependency>
```

**MySQL CDC Source**:

```java
// MySQL CDC Source
MySqlSource<String> mySqlSource = MySqlSource.<String>builder()
    .hostname("mysql-host")
    .port(3306)
    .databaseList("inventory")
    .tableList("inventory.products", "inventory.orders")
    .username("cdc_user")
    .password("password")
    .deserializer(new JsonDebeziumDeserializationSchema())
    .startupOptions(StartupOptions.initial())
    .build();

env.fromSource(mySqlSource, WatermarkStrategy.noWatermarks(), "MySQL CDC")
    .print();
```

**Flink SQL CDC**:

```sql
-- MySQL CDC Table
CREATE TABLE mysql_products (
    id INT PRIMARY KEY NOT ENFORCED,
    name STRING,
    description STRING,
    weight DECIMAL(10, 3)
) WITH (
    'connector' = 'mysql-cdc',
    'hostname' = 'mysql-host',
    'port' = '3306',
    'username' = 'cdc_user',
    'password' = 'password',
    'database-name' = 'inventory',
    'table-name' = 'products',
    'scan.startup.mode' = 'initial',
    'server-id' = '5400-5404'
);

-- PostgreSQL CDC Table
CREATE TABLE pg_users (
    id INT PRIMARY KEY NOT ENFORCED,
    name STRING,
    email STRING
) WITH (
    'connector' = 'postgres-cdc',
    'hostname' = 'postgres-host',
    'port' = '5432',
    'username' = 'cdc_user',
    'password' = 'password',
    'database-name' = 'mydb',
    'schema-name' = 'public',
    'table-name' = 'users',
    'decoding.plugin.name' = 'pgoutput',
    'slot.name' = 'flink_slot'
);
```

---

#### 6.5.2 CDC Pipeline YAML 配置

**MySQL → Doris 同步**:

```yaml
# pipeline.yaml
pipeline:
  name: mysql-to-doris-pipeline
  parallelism: 4

source:
  type: mysql
  hostname: mysql-host
  port: 3306
  username: ${MYSQL_USER}
  password: ${MYSQL_PASSWORD}
  database-list: inventory,orders
  table-list: inventory\..*,orders\..*

  # 无锁读取配置
  scan.incremental.snapshot.enabled: true
  scan.snapshot.fetch.size: 1024
  scan.incremental.snapshot.chunk.size: 8096
  scan.startup.mode: initial

  # Schema 变更捕获
  include.schema.changes: true

sink:
  type: doris
  fenodes: doris-fe:8030
  username: ${DORIS_USER}
  password: ${DORIS_PASSWORD}
  database: ods

  # 写入配置
  sink.enable.batch-mode: true
  sink.buffer-flush.interval: 10s
  sink.buffer-flush.max-rows: 50000
  sink.max-retries: 3

  # 表创建选项
  table.create.properties.replication_num: 3
  table.create.properties.storage_format: MOR

# 数据转换 (可选)
transform:
  - source-table: inventory\.customers
    projection: id, name, email, region
    filter: region = 'APAC'
    description: "Filter APAC customers"

# 路由规则 (可选)
route:
  - source-table: orders\.order_\d+
    sink-table: ods.orders_all
    description: "Merge all order shards"
```

---

#### 6.5.3 CDC 到 Lakehouse

**MySQL CDC → Iceberg**:

```sql
-- 1. 创建 CDC Source 表
CREATE TABLE mysql_orders_cdc (
    order_id BIGINT,
    user_id STRING,
    amount DECIMAL(10, 2),
    status STRING,
    create_time TIMESTAMP(3),
    PRIMARY KEY (order_id) NOT ENFORCED
) WITH (
    'connector' = 'mysql-cdc',
    'hostname' = 'mysql-host',
    'port' = '3306',
    'username' = 'cdc_user',
    'password' = 'password',
    'database-name' = 'mydb',
    'table-name' = 'orders'
);

-- 2. 创建 Iceberg Sink 表
CREATE TABLE iceberg_orders (
    order_id BIGINT,
    user_id STRING,
    amount DECIMAL(10, 2),
    status STRING,
    create_time TIMESTAMP(3),
    PRIMARY KEY (order_id) NOT ENFORCED
) WITH (
    'connector' = 'iceberg',
    'catalog-type' = 'hive',
    'catalog-database' = 'default',
    'catalog-table' = 'orders',
    'write.upsert.enabled' = 'true',
    'write.parquet.compression-codec' = 'zstd'
);

-- 3. 启动 CDC 同步
INSERT INTO iceberg_orders
SELECT * FROM mysql_orders_cdc;
```

**CDC 到 Paimon (推荐)**:

```sql
-- Paimon CDC 同步
CREATE TABLE paimon_orders (
    order_id BIGINT PRIMARY KEY NOT ENFORCED,
    user_id STRING,
    amount DECIMAL(10, 2),
    status STRING,
    create_time TIMESTAMP(3)
) WITH (
    'connector' = 'paimon',
    'path' = 's3://bucket/paimon/orders',
    'bucket' = '8',
    'merge-engine' = 'deduplicate',
    'changelog-producer' = 'input',
    'sequence.field' = 'create_time'
);

-- 同步作业
INSERT INTO paimon_orders
SELECT * FROM mysql_orders_cdc;
```

---

## 7. 可视化 (Visualizations)

### 7.1 连接器生态全景图

```mermaid
graph TB
    subgraph "Flink 连接器生态系统"
        subgraph "消息队列层"
            K[Kafka]
            P[Pulsar]
            R[RabbitMQ]
            KIN[Amazon Kinesis]
            PS[Google Pub/Sub]
            M[MQTT]
        end

        subgraph "文件系统层"
            H[HDFS]
            S3[Amazon S3]
            GCS[Google Cloud Storage]
            AZ[Azure Blob Storage]
            OSS[Alibaba OSS]
        end

        subgraph "数据库层"
            JDBC[JDBC<br/>MySQL/PG/Oracle]
            C[Cassandra]
            HB[HBase]
            ES[Elasticsearch]
            MG[MongoDB]
            RD[Redis]
            INF[InfluxDB]
        end

        subgraph "Lakehouse层"
            ICE[Apache Iceberg]
            HUD[Apache Hudi]
            PAI[Apache Paimon]
            DL[Delta Lake]
            FL[Apache Fluss]
        end

        subgraph "CDC层"
            CDC_M[MySQL CDC]
            CDC_P[PostgreSQL CDC]
            CDC_O[Oracle CDC]
            CDC_MG[MongoDB CDC]
            CDC_S[SQL Server CDC]
        end
    end

    subgraph "Flink 计算引擎"
        FS[Flink Streaming]
        FB[Flink Batch]
        SQL[Flink SQL]
    end

    K --> FS
    P --> FS
    R --> FS
    KIN --> FS
    PS --> FS
    M --> FS

    H --> FB
    S3 --> FB
    GCS --> FB
    AZ --> FB
    OSS --> FB

    JDBC --> FS
    C --> FS
    HB --> FS
    ES --> FS
    MG --> FS
    RD --> FS
    INF --> FS

    ICE --> FS
    ICE --> FB
    HUD --> FS
    HUD --> FB
    PAI --> FS
    DL --> FB
    FL --> FS

    CDC_M --> FS
    CDC_P --> FS
    CDC_O --> FS
    CDC_MG --> FS
    CDC_S --> FS

    FS --> K
    FS --> P
    FB --> S3
    FB --> H
    FS --> JDBC
    FS --> ES
    FS --> ICE
    FS --> HUD
    FS --> PAI
```

---

### 7.2 连接器选型决策树

```mermaid
flowchart TD
    A[数据源/目标类型] --> B{需要实时流处理?}

    B -->|是| C{消息类型?}
    B -->|否| D{批处理数据?}

    C -->|日志/事件| E[选择 Kafka/Pulsar]
    C -->|IoT/MQTT| F[选择 MQTT Broker]
    C -->|云服务| G{云平台?}

    G -->|AWS| H[选择 Kinesis]
    G -->|GCP| I[选择 Pub/Sub]
    G -->|Azure| J[选择 Event Hubs]

    D -->|文件数据| K{存储位置?}
    D -->|结构化数据| L{数据规模?}

    K -->|本地/HDFS| M[选择 FileSystem Connector]
    K -->|云对象存储| N{云厂商?}
    N -->|AWS| O[选择 S3 Connector]
    N -->|GCP| P[选择 GCS Connector]
    N -->|Azure| Q[选择 Azure Blob Connector]
    N -->|阿里云| R[选择 OSS Connector]

    L -->|TB级+| S{分析需求?}
    L -->|GB级| T[选择 JDBC Connector]

    S -->|实时分析| U[选择 Lakehouse<br/>Iceberg/Hudi/Paimon]
    S -->|离线分析| V[选择数据湖格式<br/>Parquet/ORC on S3]

    T --> W{数据库类型?}
    W -->|关系型| X[MySQL/PostgreSQL/Oracle]
    W -->|NoSQL| Y{访问模式?}

    Y -->|Key-Value| Z[选择 Redis/HBase]
    Y -->|文档| AA[选择 MongoDB]
    Y -->|搜索| AB[选择 Elasticsearch]
    Y -->|宽列| AC[选择 Cassandra]

    E --> AD{需要 Exactly-Once?}
    AD -->|是| AE[启用 Kafka 事务]
    AD -->|否| AF[At-Least-Once 模式]
```

---

### 7.3 数据流集成架构图

```mermaid
graph TB
    subgraph "数据源层"
        DB1[(MySQL)]
        DB2[(PostgreSQL)]
        KAFKA[Kafka Cluster]
        FILES[Data Files<br/>S3/HDFS]
    end

    subgraph "CDC & 摄取层"
        CDC[Flink CDC 3.0]
        K_SOURCE[Kafka Source]
        F_SOURCE[File Source]
    end

    subgraph "Flink 处理层"
        subgraph "流处理"
            STREAM[DataStream API]
            SQL[Flink SQL]
        end
        subgraph "状态管理"
            STATE[Keyed State]
            WINDOW[Window State]
        end
        subgraph "处理逻辑"
            JOIN[Stream Join]
            AGG[Aggregation]
            FILTER[Filter/Map]
        end
    end

    subgraph "数据目标层"
        ICE[(Iceberg<br/>Lakehouse)]
        HUD[(Hudi)]
        PAI[(Paimon)]
        DW[(Doris<br/>StarRocks)]
        ES2[(Elasticsearch)]
        K_SINK[Kafka Output]
    end

    DB1 --> CDC
    DB2 --> CDC
    KAFKA --> K_SOURCE
    FILES --> F_SOURCE

    CDC --> STREAM
    K_SOURCE --> STREAM
    F_SOURCE --> STREAM

    STREAM --> SQL
    SQL --> JOIN
    JOIN --> AGG
    AGG --> STATE
    AGG --> WINDOW
    WINDOW --> FILTER

    FILTER --> ICE
    FILTER --> HUD
    FILTER --> PAI
    FILTER --> DW
    FILTER --> ES2
    FILTER --> K_SINK
```

---

### 7.4 连接器状态机

```mermaid
stateDiagram-v2
    [*] --> CREATED: 创建连接器
    CREATED --> INITIALIZING: 初始化配置

    INITIALIZING --> RUNNING: 启动成功
    INITIALIZING --> FAILED: 配置错误

    RUNNING --> CHECKPOINTING: Checkpoint 触发
    CHECKPOINTING --> RUNNING: Checkpoint 成功
    CHECKPOINTING --> FAILED: Checkpoint 失败

    RUNNING --> RECOVERING: 故障检测
    RECOVERING --> RUNNING: 恢复成功
    RECOVERING --> FAILED: 恢复失败

    RUNNING --> SUSPENDED: 暂停作业
    SUSPENDED --> RUNNING: 恢复作业
    SUSPENDED --> CANCELLED: 取消作业

    RUNNING --> CANCELLED: 正常关闭
    FAILED --> CANCELLED: 清理资源

    CANCELLED --> [*]

    note right of CHECKPOINTING
        Source: 保存读取位置
        Sink: preCommit
        State: 持久化状态
    end note

    note right of RECOVERING
        从 Checkpoint 恢复
        Source: seek 到保存位置
        Sink: 清理 pending 事务
    end note
```

---

## 8. 配置参考与性能对比 (Configuration & Performance)

### 8.1 全局配置最佳实践

**Checkpoint 配置**:

```java

import org.apache.flink.streaming.api.CheckpointingMode;

// Checkpoint 配置
env.enableCheckpointing(60000, CheckpointingMode.EXACTLY_ONCE);
env.getCheckpointConfig().setCheckpointTimeout(600000);
env.getCheckpointConfig().setMinPauseBetweenCheckpoints(30000);
env.getCheckpointConfig().setMaxConcurrentCheckpoints(1);
env.getCheckpointConfig().setExternalizedCheckpointCleanup(
    CheckpointConfig.ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION);

// 状态后端配置
env.setStateBackend(new EmbeddedRocksDBStateBackend(true));
env.getCheckpointConfig().setCheckpointStorage("s3://bucket/checkpoints");
```

**网络与序列化配置**:

```java
// 网络缓冲配置
Configuration conf = new Configuration();
conf.setInteger("taskmanager.memory.network.max", 256 << 20); // 256MB
conf.setInteger("taskmanager.memory.network.min", 128 << 20); // 128MB

// 序列化配置
env.getConfig().setAutoTypeRegistrationWithKryo(true);
env.getConfig().addDefaultKryoSerializer(MyClass.class, MySerializer.class);
```

**Source 通用配置**:

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| `source.parallelism` | 与外部分区数匹配 | 避免资源浪费 |
| `source.watermark-interval` | 200ms | Watermark 生成间隔 |
| `source.idle-timeout` | 30s | 空闲 Source 检测 |

**Sink 通用配置**:

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| `sink.buffer-flush.max-rows` | 1000-5000 | 批量写入大小 |
| `sink.buffer-flush.interval` | 1-5s | 批量刷新间隔 |
| `sink.max-retries` | 3-10 | 最大重试次数 |
| `sink.retry-interval` | 1-5s | 重试间隔 |

---

### 8.2 连接器性能对比矩阵

**Source 性能对比**:

| 连接器 | 吞吐 (records/s) | 延迟 | 扩展性 | CPU 占用 | 内存占用 |
|--------|------------------|------|--------|----------|----------|
| **Kafka** | 500K-2M | 低 (ms) | ⭐⭐⭐⭐⭐ | 中 | 中 |
| **Pulsar** | 400K-1.5M | 低 (ms) | ⭐⭐⭐⭐⭐ | 中 | 中 |
| **Kinesis** | 200K-500K | 中 (100ms) | ⭐⭐⭐⭐ | 中 | 中 |
| **JDBC** | 10K-50K | 高 (100ms+) | ⭐⭐⭐ | 低 | 低 |
| **Iceberg** | 100K-500K | 高 (秒级) | ⭐⭐⭐⭐⭐ | 中 | 高 |
| **Files** | 50K-200K | 高 (秒级) | ⭐⭐⭐⭐ | 低 | 低 |

**Sink 性能对比**:

| 连接器 | 吞吐 (records/s) | 延迟 | Exactly-Once 开销 | 推荐场景 |
|--------|------------------|------|-------------------|----------|
| **Kafka** | 300K-1M | 低 | 20-30% | 实时管道 |
| **Pulsar** | 250K-800K | 低 | 20-30% | 实时管道 |
| **Iceberg** | 50K-200K | 中 | 10-20% | 数据湖 |
| **Hudi** | 30K-100K | 中 | 15-25% | 增量更新 |
| **Paimon** | 50K-150K | 低 | 10-15% | 流批统一 |
| **JDBC** | 5K-20K | 高 | 30-50% | 关系型存储 |
| **Elasticsearch** | 20K-50K | 低 | 无 | 全文搜索 |
| **Redis** | 100K-300K | 极低 | 无 | 缓存 |

**端到端延迟对比** (Source → Flink → Sink):

| 链路组合 | 典型延迟 | 适用场景 |
|----------|----------|----------|
| Kafka → Flink → Kafka | 50-200ms | 实时流处理 |
| Kafka → Flink → Iceberg | 5-30s | 实时入湖 |
| MySQL CDC → Flink → Doris | 100ms-2s | 实时数仓 |
| Files → Flink → S3 | 分钟级 | 离线批处理 |
| Kinesis → Flink → Kinesis | 100-500ms | AWS 实时处理 |

---

### 8.3 常见问题排查指南

**问题1: Kafka Source 消费延迟**

```
症状: records-lag-max 持续增长

诊断:
1. 检查 Flink 反压: backPressuredTimeMsPerSecond
2. 检查并行度是否匹配 Kafka 分区数
3. 检查数据倾斜: 各 Subtask 处理速率

解决:
- 增加 Flink 并行度 = Kafka 分区数
- 优化下游处理逻辑
- 扩容 Kafka 分区数
```

**问题2: JDBC Sink 连接超时**

```
症状: Connection timeout / Connection pool exhausted

诊断:
1. 检查数据库连接数限制
2. 检查网络稳定性
3. 检查 Checkpoint 间隔与事务超时

解决:
- 增加 connection.max-retry-timeout
- 减小 batch.size 和增加 flush.interval
- 使用连接池 (HikariCP)
- 增加数据库连接数限制
```

**问题3: Iceberg Sink 小文件过多**

```
症状: 元数据文件膨胀,查询性能下降

诊断:
1. 检查 Checkpoint 间隔是否过短
2. 检查数据量与文件大小比例

解决:
- 增加 Checkpoint 间隔 (建议 1-5 分钟)
- 配置 Compaction 任务
- 调整 write.target-file-size-bytes (建议 128MB+)
```

**问题4: CDC 同步数据不一致**

```
症状: 目标端数据与源端不一致

诊断:
1. 检查 Schema 变更是否同步
2. 检查主键冲突处理
3. 检查时间戳字段配置

解决:
- 启用 include.schema.changes
- 配置正确的 merge-engine
- 验证主键唯一性
```

**问题5: Checkpoint 超时**

```
症状: Checkpoint 经常超时失败

诊断:
1. 检查 State 大小
2. 检查 Sink 端是否阻塞
3. 检查网络带宽

解决:
- 增加 Checkpoint 超时时间
- 启用增量 Checkpoint
- 优化 State TTL
- 检查外部系统健康状况
```

---

## 9. 引用参考 (References)













---

*文档版本: v1.0 | 创建日期: 2026-04-04 | 最后更新: 2026-04-04 | 覆盖连接器: 30+ | 形式化元素: 10+ (5定义+2引理+2命题+2定理)*
