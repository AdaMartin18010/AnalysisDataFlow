# Flink + Delta Lake 深度集成：流批统一的 Lakehouse 存储

> **所属阶段**: Flink/04-connectors | **前置依赖**: [04.04-cdc-debezium-integration.md](./04.04-cdc-debezium-integration.md), [../14-lakehouse/streaming-lakehouse-architecture.md](../05.02-lakehouse/streaming-lakehouse-architecture.md) | **形式化等级**: L4-L5 | **版本**: Flink 1.17+, Delta Lake 3.0+

---

## 目录

- [Flink + Delta Lake 深度集成：流批统一的 Lakehouse 存储](#flink--delta-lake-深度集成流批统一的-lakehouse-存储)
  - [目录](#目录)
  - [1. 概念定义 (Definitions)](#1-概念定义-definitions)
    - [Def-F-04-40 (Delta Lake 表格式形式化)](#def-f-04-40-delta-lake-表格式形式化)
    - [Def-F-04-41 (Lakehouse 架构定义)](#def-f-04-41-lakehouse-架构定义)
    - [Def-F-04-42 (ACID 事务协议)](#def-f-04-42-acid-事务协议)
    - [Def-F-04-43 (Time Travel 与版本控制)](#def-f-04-43-time-travel-与版本控制)
    - [Def-F-04-44 (Schema 演进机制)](#def-f-04-44-schema-演进机制)
    - [Def-F-04-45 (Flink-Delta Source 语义)](#def-f-04-45-flink-delta-source-语义)
    - [Def-F-04-46 (Flink-Delta Sink 语义)](#def-f-04-46-flink-delta-sink-语义)
    - [Def-F-04-47 (CDC Merge 语义)](#def-f-04-47-cdc-merge-语义)
  - [2. 属性推导 (Properties)](#2-属性推导-properties)
    - [Lemma-F-04-40 (Delta 写入原子性)](#lemma-f-04-40-delta-写入原子性)
    - [Lemma-F-04-41 (并发写入隔离性)](#lemma-f-04-41-并发写入隔离性)
    - [Lemma-F-04-42 (Z-Ordering 查询优化边界)](#lemma-f-04-42-z-ordering-查询优化边界)
    - [Prop-F-04-40 (流批一致性保证)](#prop-f-04-40-流批一致性保证)
  - [3. 关系建立 (Relations)](#3-关系建立-relations)
    - [关系1: Delta Lake vs Apache Iceberg 对比](#关系1-delta-lake-vs-apache-iceberg-对比)
    - [关系2: Delta Lake vs Apache Hudi 对比](#关系2-delta-lake-vs-apache-hudi-对比)
    - [关系3: Delta Lake 与 Hive 的兼容性映射](#关系3-delta-lake-与-hive-的兼容性映射)
    - [关系4: Flink-Delta 与 Spark-Delta 能力矩阵](#关系4-flink-delta-与-spark-delta-能力矩阵)
  - [4. 论证过程 (Argumentation)](#4-论证过程-argumentation)
    - [4.1 Lakehouse 架构选型论证](#41-lakehouse-架构选型论证)
    - [4.2 流式写入 vs 批量写入边界](#42-流式写入-vs-批量写入边界)
    - [4.3 乐观并发控制 vs 悲观并发控制](#43-乐观并发控制-vs-悲观并发控制)
    - [4.4 Liquid Clustering 优化论证](#44-liquid-clustering-优化论证)
  - [5. 形式证明 / 工程论证 (Proof / Engineering Argument)](#5-形式证明--工程论证-proof--engineering-argument)
    - [Thm-F-04-30 (Flink-Delta Exactly-Once 正确性)](#thm-f-04-30-flink-delta-exactly-once-正确性)
    - [Thm-F-04-31 (CDC Merge 一致性定理)](#thm-f-04-31-cdc-merge-一致性定理)
    - [Thm-F-04-32 (并发写入冲突解决定理)](#thm-f-04-32-并发写入冲突解决定理)
    - [Thm-F-04-33 (分区修剪优化有效性)](#thm-f-04-33-分区修剪优化有效性)
  - [6. 实例验证 (Examples)](#6-实例验证-examples)
    - [6.1 Delta Source 配置与读取](#61-delta-source-配置与读取)
    - [6.2 Delta Sink 流式写入配置](#62-delta-sink-流式写入配置)
    - [6.3 MySQL CDC -\> Delta Lake 完整实现](#63-mysql-cdc---delta-lake-完整实现)
    - [6.4 PostgreSQL CDC -\> Delta Lake 实现](#64-postgresql-cdc---delta-lake-实现)
    - [6.5 CDC Merge 实现 (Upsert 场景)](#65-cdc-merge-实现-upsert-场景)
    - [6.6 流批一体查询实现](#66-流批一体查询实现)
    - [6.7 Z-Ordering 与 Liquid Clustering 配置](#67-z-ordering-与-liquid-clustering-配置)
  - [7. 可视化 (Visualizations)](#7-可视化-visualizations)
    - [7.1 Delta Lake 架构层次图](#71-delta-lake-架构层次图)
    - [7.2 Flink-Delta 集成数据流图](#72-flink-delta-集成数据流图)
    - [7.3 CDC -\> Delta 数据处理流程](#73-cdc---delta-数据处理流程)
    - [7.4 流批一体架构图](#74-流批一体架构图)
    - [7.5 并发控制状态机](#75-并发控制状态机)
  - [8. 性能调优指南](#8-性能调优指南)
    - [8.1 写入优化配置](#81-写入优化配置)
    - [8.2 读取优化配置](#82-读取优化配置)
    - [8.3 压缩策略](#83-压缩策略)
    - [8.4 缓存策略](#84-缓存策略)
  - [9. 引用参考 (References)](#9-引用参考-references)

---

## 1. 概念定义 (Definitions)

### Def-F-04-40 (Delta Lake 表格式形式化)

**定义**: Delta Lake 是一种**开放表格式 (Open Table Format)**，基于 Apache Parquet 文件格式和事务日志实现 ACID 事务、可扩展元数据管理和时间旅行查询。

**形式化结构**:

```
DeltaTable = <TablePath, Schema, Protocol, History, Checkpoints>

其中:
- TablePath: 表存储路径 (DBFS/S3/ADLS/HDFS)
- Schema: 列定义与类型系统 (Parquet Schema + Delta 扩展)
- Protocol: 读写协议版本 (minReaderVersion, minWriterVersion)
- History: 事务日志序列 (JSON 格式)
- Checkpoints: 周期性元数据检查点 (Parquet 格式)
```

**事务日志结构形式化**:

```
TransactionLog = {δ_0, δ_1, δ_2, ..., δ_n}

其中每个 δ_i 是一个原子操作集合:
δ_i = { add_file(f_1, stats_1), add_file(f_2, stats_2),
        remove_file(f_3), set_transaction(appId, version),
        commit_info(metadata) }

文件命名: {version:020d}.json  (e.g., 00000000000000000001.json)
```

**关键特性**:

| 特性 | 实现机制 | 协议版本 |
|------|----------|----------|
| **ACID 事务** | 乐观并发控制 + 原子日志提交 | V1 |
| **Schema 演进** | 元数据中的 schema 字段变更 | V2 |
| **分区演进** | 分区列可动态添加 | V2 |
| **列映射** | 物理列名与逻辑列名解耦 | V3 |
| **Deletion Vectors** | 标记删除而非重写文件 | V4 |
| **Liquid Clustering** | 自适应数据布局优化 | V4 |

---

### Def-F-04-41 (Lakehouse 架构定义)

**定义**: Lakehouse 是一种**统一数据架构范式**，将数据湖的低成本存储与数据仓库的 ACID 事务、数据质量管理能力结合。

**形式化定义**:

```
Lakehouse = <StorageLayer, TableFormat, ComputeEngines, Governance>

其中:
- StorageLayer: 对象存储 (S3/ADLS/GCS/OSS/HDFS)
- TableFormat: 开放表格式 (Delta/Iceberg/Hudi)
- ComputeEngines: {Flink, Spark, Trino, Presto, Hive, ...}
- Governance: 权限控制、数据血缘、质量监控
```

---

### Def-F-04-42 (ACID 事务协议)

**定义**: Delta Lake 的 ACID 保证通过**乐观并发控制 (Optimistic Concurrency Control)** 和**原子事务日志**实现。

**事务协议形式化**:

```
设:
- 事务 T_i 的读取版本: readVersion(T_i)
- 事务 T_i 的目标写入版本: writeVersion(T_i) = readVersion(T_i) + 1
- 冲突检测函数: Conflict(T_i, T_j) -> {true, false}

事务执行流程:
1. START: 获取当前最新版本 V_current 作为 readVersion
2. READ: 基于 V_current 读取数据
3. WRITE: 生成变更集 Δ (add/remove files)
4. VALIDATE: 检查冲突 Conflict(T_i, T_committed_since_read)
5. COMMIT: 若 Conflict=false, 原子写入 _delta_log/{V_current+1}.json
```

**隔离级别实现**:

| 隔离级别 | 实现方式 | Delta Lake 支持 |
|----------|----------|-----------------|
| **读未提交** | 直接读取最新日志 | 否 |
| **读已提交** | 基于快照版本读取 | 默认 |
| **可重复读** | 固定快照版本 | 支持 |
| **串行化** | 乐观并发控制 | 支持 |

---

### Def-F-04-43 (Time Travel 与版本控制)

**定义**: Time Travel 是 Delta Lake 支持查询历史数据版本的能力，通过不可变的事务日志和快照机制实现。

**形式化定义**:

```
设事务日志为有序序列 L = [δ_0, δ_1, ..., δ_n]

版本 V_k 的快照定义为:
Snapshot(V_k) = Apply(δ_0, δ_1, ..., δ_k)

Time Travel 查询:
QueryAt(version=k) = Snapshot(V_k)
QueryAt(timestamp=t) = Snapshot(V_{max{i | timestamp(δ_i) <= t}})
```

---

### Def-F-04-44 (Schema 演进机制)

**定义**: Schema 演进允许表结构随时间变化，同时保持向后兼容性，通过 Delta 协议中的 schema 字段版本化实现。

**Schema 兼容性规则**:

| 变更类型 | 读取兼容性 | 写入兼容性 | 自动支持 |
|----------|-----------|-----------|----------|
| 添加可空列 | 支持 | 支持 | 是 |
| 删除列 | 支持 (忽略) | 不支持 | 需配置 |
| 类型拓宽 (int->long) | 支持 | 支持 | 否 |
| 类型收窄 | 不支持 | 不支持 | 否 |
| 重命名列 | 不支持 | 不支持 | 需配置 |

---

### Def-F-04-45 (Flink-Delta Source 语义)

**定义**: Flink Delta Source 支持以批处理和流处理模式读取 Delta 表，利用快照隔离保证一致性。

**形式化语义**:

```
DeltaSource = <SnapshotSelector, ReadMode, SchemaProjection, FilterPushdown>

读取模式:
1. BATCH: 读取特定快照版本
   Source(V_k) = Snapshot(V_k).files

2. STREAMING: 增量读取新提交
   Source(V_start) = Stream of ΔV_i where V_i > V_start
   ΔV_i = Snapshot(V_i).files \ Snapshot(V_{i-1}).files
```

---

### Def-F-04-46 (Flink-Delta Sink 语义)

**定义**: Flink Delta Sink 支持流式和批量写入 Delta 表，通过两阶段提交协议实现 Exactly-Once 语义。

**两阶段提交协议**:

```
Phase 1 (Pre-commit):
  - 写入数据文件到临时位置
  - 记录 pending 文件列表到 State

Phase 2 (Commit):
  - Checkpoint 成功后，原子提交到 _delta_log
  - 生成 {version}.json 事务日志
  - 数据立即可见
```

---

### Def-F-04-47 (CDC Merge 语义)

**定义**: CDC Merge 是将变更数据捕获 (CDC) 流应用到 Delta 表的机制，支持 INSERT、UPDATE、DELETE 操作的幂等应用。

**CDC 事件处理矩阵**:

| CDC 操作 | 目标存在 | 动作 | 幂等性 |
|----------|----------|------|--------|
| INSERT | No | 插入新行 | 基于主键去重 |
| INSERT | Yes | 忽略/报错 | 配置决定 |
| UPDATE | Yes | 更新行 | 基于序列号 |
| UPDATE | No | 插入新行 | CDC 晚于快照 |
| DELETE | Yes | 删除行 | 基于序列号 |
| DELETE | No | 忽略 | 已删除/不存在 |

---

## 2. 属性推导 (Properties)

### Lemma-F-04-40 (Delta 写入原子性)

**引理**: Delta Lake 的写入操作满足原子性——事务内的所有变更要么全部提交，要么全部回滚。

**证明概要**:

事务日志写入是原子的 (文件系统 rename 保证)，数据文件先写入临时位置，日志提交后才可见。失败场景均有恢复机制，因此满足 AllOrNothing(T) = true。

---

### Lemma-F-04-41 (并发写入隔离性)

**引理**: 多个并发写入事务通过乐观并发控制实现可串行化隔离。

---

### Lemma-F-04-42 (Z-Ordering 查询优化边界)

**引理**: Z-Ordering 对多维过滤查询的 I/O 减少量与维度数和过滤选择性相关。

**边界分析**:

```
设维度数为 d，查询过滤选择性为 s (0 < s <= 1)

I/O 减少因子:
  无排序: I/O_base = 全表扫描
  Z-Order: I/O_zorder ≈ s^(1/d) * I/O_base

维度诅咒: 当 d -> ∞, s^(1/d) -> 1, 优化效果趋于消失
最优维度数: d <= 4 (实践建议)
```

---

### Prop-F-04-40 (流批一致性保证)

**命题**: Flink 以批处理和流处理模式写入 Delta 表，读取时具有一致的快照视图。

**证明**: 批写入生成单一版本 V_B，流写入生成版本序列 V_{Si}，任意读取时间 t 都会基于快照模型看到统一视图。

---

## 3. 关系建立 (Relations)

### 关系1: Delta Lake vs Apache Iceberg 对比

| 维度 | Delta Lake | Apache Iceberg |
|------|------------|----------------|
| **诞生背景** | Databricks (2019) | Netflix/Apple (2018) |
| **存储格式** | Parquet (默认) | Parquet/ORC/Avro |
| **隐藏分区** | 有限支持 | 原生支持 |
| **删除向量** | V4 支持 | 支持 |
| **商业化** | Databricks 深度绑定 | 开源中立 |

---

### 关系2: Delta Lake vs Apache Hudi 对比

| 维度 | Delta Lake | Apache Hudi |
|------|------------|-------------|
| **设计哲学** | 表格式 + 事务 | 增量处理优先 |
| **更新模型** | COW/MOR | COW/MOR 原生 |
| **索引支持** | 有限 (DVs) | 丰富 (Bloom/记录级) |
| **增量查询** | 基于版本 | 原生增量时间线 |
| **流处理** | 良好支持 | 原生流式优先 |

---

### 关系3: Delta Lake 与 Hive 的兼容性映射

```sql
-- 在 Hive 中注册 Delta 表
CREATE EXTERNAL TABLE hive_delta_table
STORED BY 'org.apache.hadoop.hive.delta.DeltaStorageHandler'
LOCATION 's3://bucket/delta-table/'
TBLPROPERTIES ('delta.table.version' = '1');
```

---

### 关系4: Flink-Delta 与 Spark-Delta 能力矩阵

| 功能特性 | Flink-Delta | Spark-Delta |
|----------|-------------|-------------|
| **流式写入** | 完全支持 | 原生支持 |
| **MERGE/Upsert** | 有限支持 | 完整支持 |
| **OPTIMIZE** | 需外部触发 | 内置支持 |
| **VACUUM** | 需外部触发 | 内置支持 |
| **Liquid Clustering** | 读取支持 | 完整支持 |

**推荐实践**: Flink 负责实时摄入，Spark 负责元数据维护 (OPTIMIZE/VACUUM)。

---

## 4. 论证过程 (Argumentation)

### 4.1 Lakehouse 架构选型论证

| 架构范式 | 数据仓库 | 数据湖 | Lakehouse |
|----------|----------|--------|-----------|
| **存储成本** | 高 | 低 | 低 |
| **ACID 支持** | 强 | 弱 | 强 |
| **Schema 管理** | 严格 | 灵活但弱 | 严格且灵活 |
| **存算分离** | 紧耦合 | 天然支持 | 天然支持 |

### 4.2 流式写入 vs 批量写入边界

| 场景 | 推荐模式 | 延迟 | Checkpoint 间隔 |
|------|----------|------|-----------------|
| 实时 CDC 同步 | 流式写入 | 秒级-分钟级 | 30s-60s |
| 小时级批量 ETL | 批量写入 | 小时级 | 作业级 |
| 微批处理 | 流式写入 | 分钟级 | 5-10min |

### 4.3 乐观并发控制 vs 悲观并发控制

**Delta Lake OCC 优点**:

- 无锁开销，高并发读取
- 冲突概率低时性能优异
- 天然适合云存储 (S3 无原生锁)

**冲突处理策略**: RETRY (自动重试)、FAIL (抛出异常)、MERGE (合并非冲突变更)

### 4.4 Liquid Clustering 优化论证

**Liquid Clustering 原理**: 使用 Z-Order/Hilbert 曲线多维聚类，数据按查询模式自适应分布。

**性能收益**:

- 时间范围查询: 30-50% 提升
- 多维过滤: 40-60% 提升
- 点查: 70-90% 提升

---

## 5. 形式证明 / 工程论证 (Proof / Engineering Argument)

### Thm-F-04-30 (Flink-Delta Exactly-Once 正确性)

**定理**: Flink Delta Sink 结合 Checkpoint 机制实现端到端 Exactly-Once 语义。

**证明**:

```
Exactly-Once 条件:
  1. 不丢失: 所有输入记录被处理并提交到 Delta
  2. 不重复: 每条记录在 Delta 中只出现一次

证明 1 (不丢失):
  - Flink Checkpoint 保证所有记录在 C_k 前被处理并持久化到 State
  - Delta Sink 在 notifyCheckpointComplete 时才提交事务
  - 若提交失败，从上一个成功 Checkpoint 恢复，重放未提交记录
  - 因此所有记录最终都被提交

证明 2 (不重复):
  - 每个 Checkpoint 对应唯一 Delta 版本 V_k
  - 事务提交是幂等的 (基于版本号)
  - 即使重放，相同版本的事务会被检测为已存在
  - 因此不会重复写入
```

**工程实现要点**:

```java
// DeltaSink 提交逻辑
public void notifyCheckpointComplete(long checkpointId) {
    // 1. 获取 pending 文件列表
    List<DeltaPendingFile> pending = state.getPendingFiles();

    // 2. 原子提交到 Delta Log
    DeltaLog log = DeltaLog.forTable(conf, tablePath);
    long version = log.startTransaction().commit(
        pending.stream().map(f -> f.toAddFileAction()),
        new Operation(Operation.Name.WRITE),
        engineInfo
    );

    // 3. 提交成功后清理 pending
    state.clearPendingFiles();
}
```

---

### Thm-F-04-31 (CDC Merge 一致性定理)

**定理**: 基于主键的 CDC Merge 操作保证最终一致性与幂等性。

**证明**:

```
最终一致性:
  设 CDC 事件序列 E = [e_1, e_2, ..., e_n]，其中 e_i = (op, key, ts, data)
  按 ts 排序后应用，最终状态等于源数据库在该时间点的状态

幂等性:
  INSERT: 若 key 不存在则插入，存在则忽略 (或报错)
  UPDATE: 更新为相同值 (幂等)
  DELETE: 删除不存在的数据 (幂等)
  通过 Merge 条件的精确匹配，多次应用结果相同
```

---

### Thm-F-04-32 (并发写入冲突解决定理)

**定理**: 在乐观并发控制下，冲突事务可通过重试策略最终完成。

**证明**:

```
设事务 T 遇到冲突概率为 p，最大重试次数为 k:
  成功概率: P_success = 1 - p^(k+1)
  当 k -> ∞, P_success -> 1 (概率收敛)

实际系统中，p 通常很小 (< 0.1)，期望重试次数:
  E[retries] = p / (1-p) ≈ 0.11 (当 p=0.1)

因此事务最终完成
```

---

### Thm-F-04-33 (分区修剪优化有效性)

**定理**: 基于元数据的分区修剪可显著减少查询 I/O。

**证明**:

```
设:
  - 总数据文件数: N
  - 分区数: P
  - 查询涉及分区数: P_q (P_q <= P)
  - 每分区平均文件数: N_p = N / P

无修剪时 I/O: I/O_full = N * file_size
有修剪时 I/O: I/O_pruned = P_q * N_p * file_size = (P_q/P) * I/O_full

优化比率: η = I/O_pruned / I/O_full = P_q / P

当查询针对特定分区 (P_q = 1): η = 1/P
例如按天分区 (P=365)，单日查询 I/O 减少 99.7%
```

---

## 6. 实例验证 (Examples)

### 6.1 Delta Source 配置与读取

**Maven 依赖**:

```xml
<dependency>
    <groupId>io.delta</groupId>
    <artifactId>delta-flink</artifactId>
    <version>3.0.0</version>
</dependency>
```

**批量读取 (DataStream API)**:

```java

import org.apache.flink.streaming.api.datastream.DataStream;

DeltaSource<RowData> deltaSource = DeltaSource
    .forBoundedRowData(
        new Path("s3://bucket/delta-table"),
        new Configuration()
    )
    .build();

DataStream<RowData> stream = env.fromSource(
    deltaSource,
    WatermarkStrategy.noWatermarks(),
    "delta-batch-source"
);
```

**流式增量读取**:

```java
DeltaSource<RowData> streamingSource = DeltaSource
    .forContinuousRowData(
        new Path("s3://bucket/delta-table"),
        new Configuration()
    )
    .startingVersion(100)
    .build();
```

---

### 6.2 Delta Sink 流式写入配置

**DataStream API 写入**:

```java
DeltaSink<RowData> deltaSink = DeltaSink
    .forRowData(
        new Path("s3://bucket/output-table"),
        new Configuration(),
        rowType
    )
    .withPartitionColumns("event_date", "region")
    .withMergeSchema(true)
    .build();

stream.sinkTo(deltaSink);
```

**Checkpoint 配置**:

```java

import org.apache.flink.streaming.api.CheckpointingMode;

env.enableCheckpointing(60000);
env.getCheckpointConfig().setCheckpointingMode(
    CheckpointingMode.EXACTLY_ONCE
);
env.setStateBackend(new EmbeddedRocksDBStateBackend(true));
```

---

### 6.3 MySQL CDC -> Delta Lake 完整实现

```java
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

import org.apache.flink.streaming.api.datastream.DataStream;


public class MySqlCdcToDelta {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();
        env.enableCheckpointing(60000);

        // 1. MySQL CDC Source
        MySqlSource<String> mysqlSource = MySqlSource.<String>builder()
            .hostname("mysql-host")
            .port(3306)
            .databaseList("production_db")
            .tableList("production_db.users")
            .username("cdc_user")
            .password("cdc_password")
            .deserializer(new JsonDebeziumDeserializationSchema())
            .startupOptions(StartupOptions.initial())
            .build();

        DataStream<String> cdcStream = env.fromSource(
            mysqlSource,
            WatermarkStrategy.noWatermarks(),
            "mysql-cdc"
        );

        // 2. 解析并写入 Delta
        DataStream<RowData> parsedStream = cdcStream
            .map(new CdcJsonToRowDataMapper());

        DeltaSink<RowData> deltaSink = DeltaSink
            .forRowData(
                new Path("s3://datalake/silver/users"),
                new Configuration(),
                rowType
            )
            .withPartitionColumns("date")
            .build();

        parsedStream.sinkTo(deltaSink);
        env.execute("MySQL CDC to Delta");
    }
}
```

---

### 6.4 PostgreSQL CDC -> Delta Lake 实现

```java
PostgresSource<String> pgSource = PostgresSource.<String>builder()
    .hostname("postgres-host")
    .port(5432)
    .database("production_db")
    .schemaList("public")
    .tableList("public.users", "public.orders")
    .username("cdc_user")
    .password("cdc_password")
    .decodingPluginName("pgoutput")
    .deserializer(new JsonDebeziumDeserializationSchema())
    .startupOptions(StartupOptions.initial())
    .build();
```

---

### 6.5 CDC Merge 实现 (Upsert 场景)

**Delta MERGE SQL (通过 Spark 执行)**:

```sql
MERGE INTO target_users t
USING (
  SELECT
    user_id, name, email, updated_at, op,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY updated_at DESC) as rn
  FROM staging_cdc_events
) s
ON t.user_id = s.user_id AND s.rn = 1
WHEN MATCHED AND s.op = 'd' THEN DELETE
WHEN MATCHED AND s.op IN ('u', 'c') THEN UPDATE SET *
WHEN NOT MATCHED AND s.op IN ('u', 'c') THEN INSERT *
```

---

### 6.6 流批一体查询实现

```sql
-- 创建统一视图
CREATE VIEW unified_events AS
SELECT * FROM delta_table_events
WHERE event_time >= CURRENT_DATE - INTERVAL '30' DAY;

-- 流式查询
SET 'execution.runtime-mode' = 'streaming';
SELECT user_id, COUNT(*) as event_count,
    TUMBLE_START(event_time, INTERVAL '5' MINUTE) as window_start
FROM unified_events
GROUP BY user_id, TUMBLE(event_time, INTERVAL '5' MINUTE);

-- 批处理查询
SET 'execution.runtime-mode' = 'batch';
SELECT user_id, COUNT(*) as total_events, AVG(amount) as avg_amount
FROM unified_events
WHERE event_time >= TIMESTAMP '2024-01-01'
GROUP BY user_id;
```

---

### 6.7 Z-Ordering 与 Liquid Clustering 配置

**Z-Ordering (Spark)**:

```python
spark.sql("OPTIMIZE delta_table ZORDER BY (user_id, event_type)")
```

**Liquid Clustering**:

```sql
CREATE TABLE clustered_events (
    event_id STRING,
    user_id STRING,
    event_type STRING,
    event_time TIMESTAMP
) USING DELTA
CLUSTER BY (user_id, event_type);

ALTER TABLE clustered_events RECLUSTER;
```

---

## 7. 可视化 (Visualizations)

### 7.1 Delta Lake 架构层次图

```
查询层:        Flink | Spark | Trino | Hive
                  |
表格式层:      Delta Lake
                  |
元数据层:      _delta_log/
              ├── 00001.json
              ├── checkpoint.parquet
              └── _last_checkpoint
                  |
数据层:        part-00001.parquet
              part-00002.parquet
                  |
存储层:        S3 | ADLS | GCS | HDFS
```

### 7.2 Flink-Delta 集成数据流图

```
数据源 → Flink Source → Transformation → Delta Sink → Delta Lake → Object Storage
                ↑                              |
                └──── Checkpoint Coordinator ←─┘
```

### 7.3 CDC -> Delta 数据处理流程

```
1. DB 事务提交 (binlog/WAL)
2. CDC Connector 读取变更事件
3. Flink 解析 & 转换
4. 写入数据文件 (临时位置)
5. 上传 Parquet 文件到存储
6. 触发 Checkpoint
7. preCommit (pending 文件列表)
8. Checkpoint 成功
9. notifyCheckpointComplete
10. 原子提交事务到 _delta_log/{version}.json
11. 写入日志文件
```

### 7.4 流批一体架构图

```
Kafka/MySQL/API → Flink Streaming → 实时聚合 → Delta Sink (实时表)
                                              ↓
Delta Lake ←──────────────────────────────────┘
(统一存储层)
  ├── 实时数据分区
  └── 历史数据分区
       ↑
       └── Flink Batch → 批量聚合 → Delta Sink (历史表)

查询层: Flink SQL / Spark SQL / BI 工具
```

### 7.5 并发控制状态机

```
[开始] → Start → Read → Write → Validate
                          ↓
                    无冲突 → Commit → [结束]
                          ↓
                    有冲突 → Retry → Read (重试)
                          ↓
                    超次数 → Fail → [结束]
```

---

## 8. 性能调优指南

### 8.1 写入优化配置

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `checkpoint.interval` | Checkpoint 间隔 | 60s |
| `sink.parquet.row-group.size` | Parquet 行组大小 | 128MB |
| `sink.mergeSchema` | 自动合并 Schema | true |

### 8.2 读取优化配置

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `read.stats.skipping` | 启用统计信息跳过 | true |
| `read.parquet.vectorized.batchSize` | 向量化读取批次 | 4096 |

### 8.3 压缩策略

```python
# Spark OPTIMIZE
spark.sql("OPTIMIZE delta_table")

# 按分区优化
spark.sql("OPTIMIZE delta_table WHERE date >= '2024-01-01'")

# 自动优化
spark.sql("""
    ALTER TABLE delta_table SET TBLPROPERTIES (
        'delta.autoOptimize.optimizeWrite' = 'true',
        'delta.autoOptimize.autoCompact' = 'true'
    )
""")
```

### 8.4 缓存策略

**元数据缓存**:

```java
conf.set("delta.logRetentionDuration", "interval 30 days");
conf.set("delta.cacheMetadata", "true");
```

---

## 9. 引用参考 (References)
