# Flink MongoDB Connector 详细指南

> **所属阶段**: Flink/connectors | **前置依赖**: [Flink Connectors生态](flink-connectors-ecosystem-complete-guide.md), [Exactly-Once语义](../../02-core/exactly-once-end-to-end.md) | **形式化等级**: L4

---

## 目录

- [Flink MongoDB Connector 详细指南](#flink-mongodb-connector-详细指南)
  - [目录](#目录)
  - [1. 概念定义 (Definitions)](#1-概念定义-definitions)
    - [Def-F-CM-01 (MongoDB Connector 形式化定义)](#def-f-cm-01-mongodb-connector-形式化定义)
    - [Def-F-CM-02 (连接配置模型)](#def-f-cm-02-连接配置模型)
    - [Def-F-CM-03 (Change Streams CDC 定义)](#def-f-cm-03-change-streams-cdc-定义)
    - [Def-F-CM-04 (写入语义模型)](#def-f-cm-04-写入语义模型)
    - [Def-F-CM-05 (BSON 类型映射)](#def-f-cm-05-bson-类型映射)
  - [2. 属性推导 (Properties)](#2-属性推导-properties)
    - [Prop-F-CM-01 (Change Streams 有序性保证)](#prop-f-cm-01-change-streams-有序性保证)
    - [Lemma-F-CM-01 (批量写入原子性边界)](#lemma-f-cm-01-批量写入原子性边界)
    - [Prop-F-CM-02 (Resume Token 持久化保证)](#prop-f-cm-02-resume-token-持久化保证)
  - [3. 关系建立 (Relations)](#3-关系建立-relations)
    - [3.1 MongoDB Connector 与 Flink 组件的关系](#31-mongodb-connector-与-flink-组件的关系)
    - [3.2 与 CDC 生态的关系](#32-与-cdc-生态的关系)
    - [3.3 Change Stream 与 Flink Checkpoint 关系](#33-change-stream-与-flink-checkpoint-关系)
  - [4. 论证过程 (Argumentation)](#4-论证过程-argumentation)
    - [4.1 Change Stream 事件排序与时序分析](#41-change-stream-事件排序与时序分析)
    - [4.2 分区策略与并行度匹配](#42-分区策略与并行度匹配)
    - [4.3 幂等写入与重复数据处理](#43-幂等写入与重复数据处理)
  - [5. 形式证明 / 工程论证 (Proof / Engineering Argument)](#5-形式证明--工程论证-proof--engineering-argument)
    - [Thm-F-CM-01 (Change Stream Source Exactly-Once 正确性定理)](#thm-f-cm-01-change-stream-source-exactly-once-正确性定理)
    - [Thm-F-CM-02 (MongoDB Sink 幂等写入定理)](#thm-f-cm-02-mongodb-sink-幂等写入定理)
  - [6. 实例验证 (Examples)](#6-实例验证-examples)
    - [6.1 Maven 依赖配置](#61-maven-依赖配置)
    - [6.2 DataStream API - Batch Source](#62-datastream-api---batch-source)
    - [6.3 DataStream API - Change Stream Source (CDC)](#63-datastream-api---change-stream-source-cdc)
    - [6.4 DataStream API - MongoDB Sink](#64-datastream-api---mongodb-sink)
    - [6.5 Table API / SQL 配置](#65-table-api--sql-配置)
    - [6.6 聚合操作示例](#66-聚合操作示例)
  - [7. 可视化 (Visualizations)](#7-可视化-visualizations)
    - [7.1 MongoDB-Flink 集成架构](#71-mongodb-flink-集成架构)
    - [7.2 Change Stream 事件流](#72-change-stream-事件流)
    - [7.3 数据类型映射矩阵](#73-数据类型映射矩阵)
  - [8. 故障排查 (Troubleshooting)](#8-故障排查-troubleshooting)
    - [8.1 常见问题与解决方案](#81-常见问题与解决方案)
      - [问题 1: Change Stream 无法恢复 (Resume Token Expired)](#问题-1-change-stream-无法恢复-resume-token-expired)
      - [问题 2: 写入冲突 (DuplicateKeyException)](#问题-2-写入冲突-duplicatekeyexception)
      - [问题 3: 连接池耗尽](#问题-3-连接池耗尽)
      - [问题 4: 序列化异常](#问题-4-序列化异常)
    - [8.2 诊断命令](#82-诊断命令)
  - [9. 性能优化 (Performance Optimization)](#9-性能优化-performance-optimization)
    - [9.1 读取性能优化](#91-读取性能优化)
    - [9.2 写入性能优化](#92-写入性能优化)
    - [9.3 Change Stream 优化](#93-change-stream-优化)
    - [9.4 索引优化](#94-索引优化)
  - [10. 引用参考 (References)](#10-引用参考-references)

---

## 1. 概念定义 (Definitions)

### Def-F-CM-01 (MongoDB Connector 形式化定义)

**定义**: Flink MongoDB Connector 是通过 MongoDB 驱动与 MongoDB 集群交互的连接器，支持 Source（读取）、Sink（写入）和 CDC（变更流捕获）三种模式。

**形式化结构**:

```
MongoDBConnector = ⟨Connection, Source, Sink, ChangeStream⟩

其中:
- Connection: 连接配置 ⟨uri, database, credentials, pool⟩
- Source: 批量查询模式 ⟨filter, projection, batchSize⟩
- Sink: 写入模式 ⟨writeMode, batchSize, ordered⟩
- ChangeStream: CDC 模式 ⟨resumeToken, fullDocument⟩
```

**操作模式对比**:

| 模式 | 数据获取方式 | 实时性 | 适用场景 |
|------|-------------|--------|----------|
| **Batch Source** | 一次性查询 | 离线 | 初始化加载、离线分析 |
| **Change Streams** | 监听 oplog | 毫秒级 | 实时同步、CDC |
| **Hybrid** | 批量 + CDC | 混合 | 全量+增量同步 |

---

### Def-F-CM-02 (连接配置模型)

**定义**: MongoDB 连接使用标准 URI 格式，支持副本集、分片集群和多种认证方式。

**URI 格式**:

```
mongodb[+srv]://[username:password@]host1[:port1][,host2[:port2],...][/database][?options]
```

**核心连接参数**:

| 参数 | 说明 | 默认值 | 推荐值 |
|------|------|--------|--------|
| `maxPoolSize` | 连接池最大连接数 | 100 | 50-100 |
| `minPoolSize` | 连接池最小连接数 | 0 | 10-20 |
| `maxIdleTimeMS` | 连接最大空闲时间 | 0 | 60000 |
| `waitQueueTimeoutMS` | 获取连接超时 | 120000 | 5000 |
| `serverSelectionTimeoutMS` | 服务器选择超时 | 30000 | 10000 |
| `socketTimeoutMS` | Socket 超时 | 0 | 30000 |
| `connectTimeoutMS` | 连接超时 | 10000 | 10000 |

**副本集连接示例**:

```
mongodb://user:pass@rs1.host:27017,rs2.host:27017,rs3.host:27017/mydb?replicaSet=myRs&readPreference=primaryPreferred
```

**分片集群连接示例**:

```
mongodb://user:pass@mongos1.host:27017,mongos2.host:27017/mydb?readPreference=nearest
```

---

### Def-F-CM-03 (Change Streams CDC 定义)

**定义**: Change Streams 是 MongoDB 3.6+ 提供的 CDC 机制，基于 oplog 实现，支持从任意时间点恢复消费。

**形式化定义**:

```
ChangeStream = ⟨Events, ResumeToken, Options⟩

Events = [Insert | Update | Delete | Replace | Invalidate]⁺

Event = ⟨operationType, documentKey, fullDocument, updateDescription,
         clusterTime, txnNumber, lsid⟩

ResumeToken: BSON Document,唯一标识事件位置
```

**Change Stream 事件结构**:

| 字段 | 类型 | 描述 |
|------|------|------|
| `_id` | Document | Resume Token（事件标识） |
| `operationType` | String | insert/update/delete/replace |
| `ns` | Document | 命名空间 `{ db, coll }` |
| `documentKey` | Document | 被修改文档的 `_id` |
| `fullDocument` | Document | 完整文档内容（可选） |
| `updateDescription` | Document | 更新字段描述 |
| `clusterTime` | Timestamp | 集群时间戳 |

**Resume Token 机制**:

```
Resume Token = BSON Document with:
  - _data: 二进制位置标识
  - _typeBits: 类型信息

恢复公式:
Resume(token_k) ⇒ 从事件 e_{k+1} 开始消费
```

---

### Def-F-CM-04 (写入语义模型)

**定义**: MongoDB Sink 支持多种写入模式，满足不同一致性要求。

```
WriteMode = {INSERT, REPLACE, UPDATE, BULK_WRITE}

INSERT: db.collection.insertOne(document)
        - 插入新文档,_id 冲突报错

REPLACE: db.collection.replaceOne(filter, replacement, { upsert: true })
         - 替换整个文档,支持 upsert

UPDATE: db.collection.updateOne(filter, update, { upsert: true })
        - 部分字段更新,支持 upsert

BULK_WRITE: db.collection.bulkWrite(operations)
            - 批量混合操作
```

**写入模式对比**:

| 模式 | 幂等性 | 性能 | 原子性 | 适用场景 |
|------|--------|------|--------|----------|
| INSERT | ❌ 否 | ⭐⭐⭐ | 单文档 | 仅插入场景 |
| REPLACE | ✅ 是 | ⭐⭐ | 单文档 | 全量同步 |
| UPDATE | ✅ 是 | ⭐⭐ | 单文档 | 增量更新 |
| BULK_WRITE | 依赖操作 | ⭐⭐⭐ | 批量 | 高吞吐写入 |

---

### Def-F-CM-05 (BSON 类型映射)

**定义**: MongoDB 使用 BSON 格式存储数据，需要与 Flink 类型系统映射。

**类型映射表**:

| BSON Type | Java Type | Flink SQL Type | 说明 |
|-----------|-----------|----------------|------|
| `ObjectId` | `ObjectId` | `STRING` | 自动生成的唯一标识 |
| `String` | `String` | `STRING` | UTF-8 字符串 |
| `Int32` | `Integer` | `INT` | 32位整数 |
| `Int64` | `Long` | `BIGINT` | 64位整数 |
| `Double` | `Double` | `DOUBLE` | 64位浮点 |
| `Decimal128` | `BigDecimal` | `DECIMAL(38, 18)` | 高精度小数 |
| `Boolean` | `Boolean` | `BOOLEAN` | 布尔值 |
| `Date` | `Date` | `TIMESTAMP(3)` | UTC 日期时间 |
| `Binary` | `byte[]` | `BYTES` | 二进制数据 |
| `Array` | `List` | `ARRAY<T>` | 数组 |
| `Document` | `Document` | `MAP<STRING, T>` | 嵌套文档 |

---

## 2. 属性推导 (Properties)

### Prop-F-CM-01 (Change Streams 有序性保证)

**命题**: Change Streams 保证同一文档的事件按发生的先后顺序传递。

```
∀ doc ∈ Collection, ∀ e_i, e_j ∈ Events(doc):
    if (e_i.clusterTime < e_j.clusterTime)
    then (e_i is delivered before e_j)
```

**全局有序性**: Change Streams 默认保证全局有序（单 Change Stream），但多并行度消费时不保证跨文档有序。

---

### Lemma-F-CM-01 (批量写入原子性边界)

**引理**: MongoDB 批量写入的原子性受以下约束：

```
BulkWrite Atomicity:
- ordered=true: 遇到错误停止,已写入的不回滚
- ordered=false: 并行执行,各自独立
- 事务中: 多文档 ACID(MongoDB 4.0+ 副本集,4.2+ 分片)
```

---

### Prop-F-CM-02 (Resume Token 持久化保证)

**命题**: 将 Resume Token 持久化到 Flink State 后，可实现故障时的精确恢复。

```
Recovery Guarantee:
- Checkpoint success: Resume Token 已持久化
- Failure recovery: 从 Checkpoint 恢复 Resume Token
- Resume: ChangeStream.resumeAfter(resumeToken)
- Result: No duplicate, no missing (within retention window)
```

**前提条件**: oplog 保留窗口必须大于 Checkpoint 间隔 + 最大故障恢复时间。

---

## 3. 关系建立 (Relations)

### 3.1 MongoDB Connector 与 Flink 组件的关系

```
┌─────────────────────────────────────────────────────────────────┐
│                         Flink Runtime                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ Batch       │  │ Change      │  │ MongoDB Sink            │ │
│  │ Source      │  │ Stream      │  │ (INSERT/REPLACE/UPDATE) │ │
│  │ (find)      │  │ Source      │  │                         │ │
│  └──────┬──────┘  └──────┬──────┘  └────────────┬────────────┘ │
│         │                │                      │              │
│         └────────────────┴──────────────────────┘              │
│                          │                                     │
│                    MongoDB Driver                              │
│                    (Java Driver 4.x)                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌────────────┐  ┌────────────┐  ┌────────────┐
    │ Primary    │  │ Secondary  │  │ Secondary  │
    │ (Writes)   │  │ (Reads)    │  │ (Reads)    │
    └─────┬──────┘  └────────────┘  └────────────┘
          │
          ▼
    ┌────────────┐
    │ oplog      │ ◀── Change Streams
    └────────────┘
```

### 3.2 与 CDC 生态的关系

```
┌─────────────────────────────────────────────────────────────────┐
│                    MongoDB CDC 生态                              │
├──────────────┬──────────────────┬───────────────────────────────┤
│ Change       │ Debezium         │ Flink CDC Connector           │
│ Streams      │ MongoDB          │ (Debezium-based)              │
│ (Native)     │ Connector        │                               │
├──────────────┼──────────────────┼───────────────────────────────┤
│ 原生支持     │ 独立服务         │ Flink 原生集成                │
│ 无需额外组件 │ Kafka Connect    │ 无 Kafka 依赖                 │
│ 功能有限     │ 功能完整         │ 功能完整 + Flink 生态         │
└──────────────┴──────────────────┴───────────────────────────────┘

推荐: Flink CDC Connector for MongoDB (基于 Debezium)
```

### 3.3 Change Stream 与 Flink Checkpoint 关系

```
Checkpoint 周期:
    │
    ├── 正常消费
    │   └── Change Stream → Deserialize → Process
    │
    ├── Checkpoint 触发
    │   └── 获取当前 Resume Token
    │   └── 持久化到 State
    │   └── 确认 Checkpoint
    │
    └── 恢复时
        └── 从 State 读取 Resume Token
        └── resumeAfter(token)
        └── 继续消费(无重复、无丢失)
```

---

## 4. 论证过程 (Argumentation)

### 4.1 Change Stream 事件排序与时序分析

**时序约束**:

```
事件时间线:
t1: insert doc { _id: 1, status: "new" }
t2: update doc { _id: 1, status: "processing" }
t3: update doc { _id: 1, status: "done" }

Change Stream 输出顺序:
1. { op: "insert", clusterTime: t1, fullDocument: {...} }
2. { op: "update", clusterTime: t2, updateDescription: {...} }
3. { op: "update", clusterTime: t3, updateDescription: {...} }

保证: t1 < t2 < t3 ⇒ 输出顺序 1 → 2 → 3
```

**乱序处理**:

```java

import org.apache.flink.streaming.api.datastream.DataStream;

// 使用 Watermark 处理可能的乱序
DataStream<ChangeEvent> events = env
    .fromSource(
        changeStreamSource,
        WatermarkStrategy
            .<ChangeEvent>forBoundedOutOfOrderness(
                Duration.ofSeconds(5)
            )
            .withIdleness(Duration.ofMinutes(1)),
        "mongo-cdc"
    );
```

### 4.2 分区策略与并行度匹配

**默认限制**: MongoDB Change Stream 不支持多并行度消费（单管道有序性）。

**并行化策略**:

```
策略 1: 按命名空间并行
- Task 1: 监听 db1.collection1
- Task 2: 监听 db1.collection2
- Task 3: 监听 db2.collection1

策略 2: 按 Shard Key 并行(自定义)
- 需要多个 Change Stream,每个带 filter
- Task 1: 监听 shard_key range [A-M)
- Task 2: 监听 shard_key range [M-Z]

策略 3: 下游并行处理
- Change Stream 单并行度读取
- KeyBy 后多并行度处理
```

### 4.3 幂等写入与重复数据处理

**重复数据来源**:

1. At-Least-Once 语义下的重试
2. Checkpoint 失败后的重放
3. Change Stream Resume 后的重复事件

**幂等策略**:

```java
// 策略 1: 使用 _id 作为文档 ID(天然幂等)
ReplaceOneModel<Document> replace = new ReplaceOneModel<>(
    Filters.eq("_id", event.getId()),
    document,
    new ReplaceOptions().upsert(true)
);

// 策略 2: 使用业务主键 + 版本号
UpdateOneModel<Document> update = new UpdateOneModel<>(
    Filters.and(
        Filters.eq("orderId", event.getOrderId()),
        Filters.lt("version", event.getVersion())
    ),
    Updates.combine(
        Updates.set("status", event.getStatus()),
        Updates.set("version", event.getVersion())
    ),
    new UpdateOptions().upsert(true)
);

// 策略 3: 使用唯一索引 + 去重表
duplicateCollection.createIndex(
    Indexes.ascending("eventId"),
    new IndexOptions().unique(true)
);
```

---

## 5. 形式证明 / 工程论证 (Proof / Engineering Argument)

### Thm-F-CM-01 (Change Stream Source Exactly-Once 正确性定理)

**定理**: 在启用 Checkpoint 且 oplog 保留窗口充足的情况下，Change Stream Source 保证 Exactly-Once 语义。

**证明**:

**前提**:

1. Resume Token 唯一标识 Change Stream 位置
2. Checkpoint 持久化 Resume Token
3. oplog 保留窗口 > Checkpoint 间隔 + 恢复时间

**执行流程**:

```
正常消费:
  Change Stream → Process → Update Resume Token in State

Checkpoint:
  1. 获取当前 Resume Token: T_k
  2. 持久化 T_k 到 Checkpoint
  3. 确认 Checkpoint

故障恢复:
  1. 从 Checkpoint 恢复状态,获取 T_k
  2. 执行 resumeAfter(T_k)
  3. 从 T_k 之后的第一个事件继续消费
  4. 由于 T_k 对应的事件已被确认处理,不会重复

oplog 约束:
  保留窗口 W ≥ CheckpointInterval + RecoveryTime + Margin
  确保 Resume Token T_k 对应的 oplog 条目仍存在
```

**结论**: 每条事件恰好被处理一次。

---

### Thm-F-CM-02 (MongoDB Sink 幂等写入定理)

**定理**: 使用 Replace 或 Update 模式并指定文档 ID 时，MongoDB Sink 提供幂等写入保证。

**证明**:

**Replace 模式**:

```
第一次写入: replaceOne({ _id: X }, doc) → inserted
第二次写入: replaceOne({ _id: X }, doc) → replaced (结果相同)

∴ 幂等性成立
```

**Update 模式（带版本控制）**:

```
条件: updateOne({ _id: X, version < V }, { $set: { ... } })

第一次: version = null < V → 更新成功
第二次: version = V ≮ V → 无匹配,不更新(无副作用)

∴ 幂等性成立
```

---

## 6. 实例验证 (Examples)

### 6.1 Maven 依赖配置

```xml
<!-- Flink MongoDB Connector -->
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-mongodb</artifactId>
    <version>${flink.version}</version>
</dependency>

<!-- MongoDB Java Driver -->
<dependency>
    <groupId>org.mongodb</groupId>
    <artifactId>mongodb-driver-sync</artifactId>
    <version>4.11.1</version>
</dependency>

<!-- Flink CDC MongoDB (如果使用 CDC) -->
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-mongodb-cdc</artifactId>
    <version>3.0.0</version>
</dependency>
```

### 6.2 DataStream API - Batch Source

```java
import org.apache.flink.connector.mongodb.source.MongoSource;
import org.apache.flink.connector.mongodb.common.config.MongoConnectionOptions;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;


public class MongoBatchSourceExample {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        // 连接配置
        MongoConnectionOptions connectionOptions =
            MongoConnectionOptions.builder()
                .setUri("mongodb://user:pass@localhost:27017/mydb")
                .setDatabase("mydb")
                .setCollection("orders")
                .build();

        // 创建 Batch Source
        MongoSource<Order> source = MongoSource.<Order>builder()
            .setConnectionOptions(connectionOptions)
            .setFetchSize(1000)
            .setNoCursorTimeout(true)
            .setProjection(
                Projections.include(
                    "orderId", "userId", "amount", "status", "createTime"
                )
            )
            .setLimit(100000L)  // 可选:限制读取数量
            .setDeserializationSchema(new OrderDeserializationSchema())
            .build();

        DataStream<Order> orders = env.fromSource(
            source,
            WatermarkStrategy.noWatermarks(),
            "mongo-batch-source"
        );

        // 处理数据
        orders.print();

        env.execute("MongoDB Batch Source");
    }
}
```

### 6.3 DataStream API - Change Stream Source (CDC)

```java
import org.apache.flink.connector.mongodb.source.MongoChangeStreamSource;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;


public class MongoCDCExample {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();
        env.enableCheckpointing(60000);

        // Change Stream 配置
        MongoChangeStreamSource<ChangeEvent> source =
            MongoChangeStreamSource.<ChangeEvent>builder()
                .setUri("mongodb://user:pass@rs1:27017,rs2:27017,rs3:27017/mydb?replicaSet=myRs")
                .setDatabase("mydb")
                .setCollection("orders")  // null 表示监听所有集合
                .setFullDocumentBeforeChange(FullDocumentBeforeChange.WHEN_AVAILABLE)
                .setFullDocument(FullDocument.UPDATE_LOOKUP)
                .setDeserializationSchema(new ChangeEventDeserializationSchema())
                .build();

        DataStream<ChangeEvent> changes = env.fromSource(
            source,
            WatermarkStrategy.forBoundedOutOfOrderness(
                Duration.ofSeconds(5)
            ),
            "mongo-cdc-source"
        );

        // 处理变更事件
        changes.map(event -> {
            switch (event.getOperationType()) {
                case "insert":
                    return handleInsert(event);
                case "update":
                    return handleUpdate(event);
                case "delete":
                    return handleDelete(event);
                default:
                    return null;
            }
        }).print();

        env.execute("MongoDB Change Stream");
    }
}
```

### 6.4 DataStream API - MongoDB Sink

```java
import org.apache.flink.connector.mongodb.sink.MongoSink;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;


public class MongoSinkExample {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        DataStream<Order> orders = env.addSource(new OrderSource());

        // 创建 MongoDB Sink
        MongoSink<Order> sink = MongoSink.<Order>builder()
            .setUri("mongodb://user:pass@localhost:27017")
            .setDatabase("mydb")
            .setCollection("orders")
            .setSerializationSchema((order, context) -> {
                Document doc = new Document();
                doc.put("_id", order.getOrderId());  // 指定 _id 实现幂等
                doc.put("userId", order.getUserId());
                doc.put("amount", order.getAmount());
                doc.put("status", order.getStatus());
                doc.put("items", order.getItems());
                doc.put("createTime", order.getCreateTime());
                doc.put("updateTime", new Date());
                return new ReplaceOneModel<>(
                    Filters.eq("_id", order.getOrderId()),
                    doc,
                    new ReplaceOptions().upsert(true)
                );
            })
            .setBatchSize(1000)
            .setBatchIntervalMs(1000)
            .setMaxRetries(3)
            .build();

        orders.sinkTo(sink);

        env.execute("MongoDB Sink");
    }
}
```

### 6.5 Table API / SQL 配置

```java
// 创建 MongoDB 表
// 批量读取表
tableEnv.executeSql("""
    CREATE TABLE mongo_orders (
        _id STRING,
        orderId STRING,
        userId STRING,
        amount DECIMAL(10, 2),
        status STRING,
        items ARRAY<MAP<STRING, STRING>>,
        createTime TIMESTAMP(3),

        PRIMARY KEY (_id) NOT ENFORCED
    ) WITH (
        'connector' = 'mongodb',
        'uri' = 'mongodb://user:pass@localhost:27017',
        'database' = 'mydb',
        'collection' = 'orders',

        -- 读取配置
        'fetch-size' = '1000',
        'no-cursor-timeout' = 'true',

        -- 写入配置
        'sink.batch.size' = '1000',
        'sink.batch.flush-interval' = '1000ms',
        'sink.max-retries' = '3'
    )
""");

// CDC 表 (使用 Flink CDC)
tableEnv.executeSql("""
    CREATE TABLE mongo_orders_cdc (
        _id STRING,
        orderId STRING,
        userId STRING,
        amount DECIMAL(10, 2),
        status STRING,
        createTime TIMESTAMP(3),

        PRIMARY KEY (_id) NOT ENFORCED
    ) WITH (
        'connector' = 'mongodb-cdc',
        'hosts' = 'rs1:27017,rs2:27017,rs3:27017',
        'username' = 'cdc_user',
        'password' = 'cdc_pass',
        'database' = 'mydb',
        'collection' = 'orders',

        -- 初始快照
        'scan.startup.mode' = 'initial',

        -- 心跳配置
        'heartbeat.interval.ms' = '10000'
    )
""");

// 聚合写入示例
tableEnv.executeSql("""
    INSERT INTO mongo_order_stats
    SELECT
        userId,
        COUNT(*) as orderCount,
        SUM(amount) as totalAmount,
        MAX(createTime) as lastOrderTime
    FROM mongo_orders
    GROUP BY userId
""");
```

### 6.6 聚合操作示例

```java
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.streaming.api.windowing.time.Time;


public class MongoAggregationExample {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        // 读取订单流
        DataStream<Order> orders = env.addSource(new OrderSource());

        // 窗口聚合
        DataStream<UserStats> stats = orders
            .keyBy(Order::getUserId)
            .window(TumblingEventTimeWindows.of(Time.hours(1)))
            .aggregate(new OrderAggregateFunction());

        // 写入 MongoDB(更新或插入)
        stats.addSink(new MongoSink<UserStats>() {
            @Override
            public void invoke(UserStats value, Context context) {
                MongoClient client = MongoClients.create(
                    "mongodb://localhost:27017"
                );
                MongoCollection<Document> coll = client
                    .getDatabase("analytics")
                    .getCollection("user_stats");

                // 使用 $inc 进行增量更新
                coll.updateOne(
                    Filters.eq("userId", value.getUserId()),
                    Updates.combine(
                        Updates.inc("orderCount", value.getOrderCount()),
                        Updates.inc("totalAmount", value.getTotalAmount()),
                        Updates.max("lastOrderTime", value.getLastOrderTime()),
                        Updates.setOnInsert("createTime", new Date())
                    ),
                    new UpdateOptions().upsert(true)
                );

                client.close();
            }
        });

        env.execute("MongoDB Aggregation");
    }
}
```

---

## 7. 可视化 (Visualizations)

### 7.1 MongoDB-Flink 集成架构

```mermaid
graph TB
    subgraph "Flink Cluster"
        BS[Batch Source]
        CS[Change Stream Source]
        P[Processing]
        S[MongoDB Sink]

        BS --> P
        CS --> P
        P --> S
    end

    subgraph "MongoDB Replica Set"
        subgraph "Primary Node"
            PR[(Primary)]
            OP[oplog]
        end

        subgraph "Secondary Nodes"
            S1[(Secondary 1)]
            S2[(Secondary 2)]
        end

        PR -.->|Replication| S1
        PR -.->|Replication| S2
        PR -.->|oplog| OP
    end

    BS -.->|Query| S1
    CS -.->|Change Stream| PR
    S -.->|Write| PR
    OP -.->|CDC Events| CS

    style PR fill:#ff9999
    style OP fill:#ffff99
    style CS fill:#99ff99
    style S fill:#99ccff
```

### 7.2 Change Stream 事件流

```mermaid
sequenceDiagram
    participant F as Flink Task
    participant MC as MongoDB Client
    participant PR as Primary
    participant OP as Oplog

    F->>MC: watch(database, collection)
    MC->>PR: $changeStream
    PR->>OP: 读取 oplog 位置
    OP-->>PR: 返回 cursor
    PR-->>MC: Change Stream Cursor

    loop 持续监听
        OP->>PR: 新写入操作
        PR->>MC: 推送变更事件
        MC->>F: deserialize(event)
        F->>F: process(event)
        F->>MC: 确认消费
    end

    F->>F: Checkpoint
    F->>F: 持久化 Resume Token
```

### 7.3 数据类型映射矩阵

```mermaid
graph LR
    subgraph "BSON Types"
        O[ObjectId]
        S[String]
        I32[Int32]
        I64[Int64]
        D[Double]
        DT[Date]
        B[Binary]
        A[Array]
        DOC[Document]
    end

    subgraph "Flink SQL Types"
        FS[STRING]
        FI[INT]
        FL[BIGINT]
        FD[DOUBLE]
        FT[TIMESTAMP]
        FB[BYTES]
        FA[ARRAY]
        FM[MAP]
    end

    O --> FS
    S --> FS
    I32 --> FI
    I64 --> FL
    D --> FD
    DT --> FT
    B --> FB
    A --> FA
    DOC --> FM

    style O fill:#ff9999
    style DT fill:#99ccff
    style DOC fill:#99ff99
```

---

## 8. 故障排查 (Troubleshooting)

### 8.1 常见问题与解决方案

#### 问题 1: Change Stream 无法恢复 (Resume Token Expired)

**现象**:

```
com.mongodb.MongoCommandException: Command failed with error 280 (ChangeStreamFatalError):
'cannot resume stream; the resume token was not found. ...'
```

**原因**: oplog 保留窗口不足，Resume Token 对应的 oplog 条目已被清理。

**解决方案**:

```bash
# 1. 检查 oplog 大小和保留时间
rs.printReplicationInfo()

# 2. 增加 oplog 大小(需要重启)
# 停止 MongoDB
# 删除 local/oplog.rs
# 以更大大小重新创建
mongod --replSet rs0 --oplogSize 10240  # 10GB

# 3. Flink 侧配置
// 缩短 Checkpoint 间隔
env.enableCheckpointing(30000);  // 30秒

// 监控 Checkpoint 成功率
// 如果频繁失败,需要调整 oplog
```

---

#### 问题 2: 写入冲突 (DuplicateKeyException)

**现象**:

```
com.mongodb.DuplicateKeyException: Write failed with error code 11000
and error message 'E11000 duplicate key error collection: mydb.orders index: _id_ dup key: { _id: "xxx" }'
```

**原因**: 使用 INSERT 模式时，相同 _id 的文档被重复插入。

**解决方案**:

```java
// 1. 使用 Replace 模式(Upsert)
ReplaceOneModel<Document> replace = new ReplaceOneModel<>(
    Filters.eq("_id", doc.getId()),
    doc,
    new ReplaceOptions().upsert(true)
);

// 2. 使用 Update 模式
UpdateOneModel<Document> update = new UpdateOneModel<>(
    Filters.eq("_id", doc.getId()),
    Updates.combine(
        Updates.set("field1", value1),
        Updates.setOnInsert("createTime", new Date())
    ),
    new UpdateOptions().upsert(true)
);

// 3. 批量写入使用 ordered=false
bulkWrite(operations, new BulkWriteOptions().ordered(false));
```

---

#### 问题 3: 连接池耗尽

**现象**:

```
com.mongodb.MongoWaitQueueFullException: Too many threads are already waiting for a connection.
Max number of threads (maxWaitQueueSize of 500) has been exceeded.
```

**原因**: 并发度过高，连接池配置不足。

**解决方案**:

```java
// 1. 调整连接池参数
MongoClientSettings settings = MongoClientSettings.builder()
    .applyConnectionString(new ConnectionString(uri))
    .applyToConnectionPoolSettings(builder -> {
        builder.maxSize(200);           // 增加最大连接数
        builder.minSize(20);            // 保持最小连接
        builder.maxWaitTime(5000, TimeUnit.MILLISECONDS);
        builder.maxConnectionLifeTime(30, TimeUnit.MINUTES);
    })
    .applyToSocketSettings(builder -> {
        builder.connectTimeout(10000, TimeUnit.MILLISECONDS);
        builder.readTimeout(30000, TimeUnit.MILLISECONDS);
    })
    .build();

// 2. 降低 Sink 并行度
orders.sinkTo(sink).setParallelism(4);

// 3. 使用连接池监控
MongoClient client = MongoClients.create(settings);
client.getClusterDescription();  // 监控连接状态
```

---

#### 问题 4: 序列化异常

**现象**:

```
org.bson.codecs.configuration.CodecConfigurationException:
Can't find a codec for class com.example.MyClass.
```

**解决方案**:

```java
// 1. 自定义 Codec
public class MyClassCodec implements Codec<MyClass> {
    @Override
    public void encode(BsonWriter writer, MyClass value, EncoderContext encoderContext) {
        writer.writeStartDocument();
        writer.writeString("field1", value.getField1());
        writer.writeInt32("field2", value.getField2());
        writer.writeEndDocument();
    }

    @Override
    public MyClass decode(BsonReader reader, DecoderContext decoderContext) {
        // 解码逻辑
    }

    @Override
    public Class<MyClass> getEncoderClass() {
        return MyClass.class;
    }
}

// 2. 注册 Codec
CodecRegistry customCodecRegistry = CodecRegistries.fromCodecs(
    new MyClassCodec()
);

CodecRegistry codecRegistry = CodecRegistries.fromRegistries(
    MongoClientSettings.getDefaultCodecRegistry(),
    customCodecRegistry
);

MongoClientSettings settings = MongoClientSettings.builder()
    .codecRegistry(codecRegistry)
    .build();
```

---

### 8.2 诊断命令

```bash
# 查看副本集状态
rs.status()

# 查看 oplog 统计
rs.printReplicationInfo()
rs.printSlaveReplicationInfo()

# 查看当前操作
db.currentOp()

# 查看慢查询
db.setProfilingLevel(2)  # 记录所有操作
db.system.profile.find().sort({$natural: -1}).limit(10)

# 查看集合统计
db.orders.stats()
db.orders.totalIndexSize()

# 查看 Change Stream 状态
db.adminCommand({aggregate: 1, pipeline: [{ $changeStream: {} }], cursor: {}})
```

---

## 9. 性能优化 (Performance Optimization)

### 9.1 读取性能优化

| 优化项 | 配置 | 建议值 | 效果 |
|--------|------|--------|------|
| 批量大小 | `fetchSize` | 1000-5000 | 减少网络往返 |
| 投影 | `projection` | 只读取必要字段 | 减少 I/O |
| 索引 | `hint()` | 使用覆盖索引 | 避免文档查找 |
| 游标 | `noCursorTimeout` | true | 防止超时 |
| 读取偏好 | `readPreference` | secondaryPreferred | 分担主节点压力 |
| 并行分区 | `splitVector` | 按 _id 范围 | 并行读取 |

```java
// 读取优化示例
FindIterable<Document> iterable = collection
    .find(Filters.gte("createTime", startTime))
    .projection(Projections.include("orderId", "status", "amount"))
    .hint(Indexes.ascending("createTime"))  // 强制使用索引
    .batchSize(5000)
    .noCursorTimeout(true);
```

---

### 9.2 写入性能优化

| 优化项 | 配置 | 建议值 | 效果 |
|--------|------|--------|------|
| 批量大小 | `batchSize` | 1000-5000 | 提高吞吐 |
| 有序写入 | `ordered` | false | 并行处理 |
|  WriteConcern | `w` | 1 | 平衡性能与一致性 |
| Journal | `j` | false | 降低延迟 |
| 预分配 | 禁用 | - | 减少碎片 |

```java
// 写入优化配置
BulkWriteOptions options = new BulkWriteOptions()
    .ordered(false);  // 无序写入,错误继续

List<WriteModel<Document>> operations = new ArrayList<>();
// 添加操作...

collection.bulkWrite(operations, options);

// WriteConcern 配置
MongoClientSettings settings = MongoClientSettings.builder()
    .applyToClusterSettings(builder -> {
        builder.serverSelectionTimeout(5000, TimeUnit.MILLISECONDS);
    })
    .applyToSocketSettings(builder -> {
        builder.readTimeout(30000, TimeUnit.MILLISECONDS);
    })
    .writeConcern(WriteConcern.W1)  // 写入到主节点即可
    .build();
```

---

### 9.3 Change Stream 优化

```java
// Change Stream 优化配置
MongoChangeStreamSource<ChangeEvent> source =
    MongoChangeStreamSource.<ChangeEvent>builder()
        .setUri(uri)
        .setDatabase("mydb")
        .setCollection("orders")

        // 只监听需要的操作类型
        .setPipeline(Arrays.asList(
            Aggregates.match(
                Filters.in("operationType",
                    Arrays.asList("insert", "update"))
            )
        ))

        // 优化 fullDocument 选项
        .setFullDocument(FullDocument.DEFAULT)  // 不查找完整文档

        // 缩短 Checkpoint 间隔,减少 oplog 压力
        .setCheckpointInterval(30000)

        .build();
```

---

### 9.4 索引优化

```javascript
// 创建复合索引(覆盖查询)
db.orders.createIndex({
    userId: 1,
    createTime: -1,
    status: 1
}, {
    name: "idx_user_time_status",
    background: true  // 后台创建
});

// TTL 索引(自动过期)
db.sessions.createIndex({
    lastAccessTime: 1
}, {
    expireAfterSeconds: 3600  // 1小时后过期
});

// 部分索引
ndb.orders.createIndex({
    urgent: 1
}, {
    partialFilterExpression: { urgent: true }
});
```

---

## 10. 引用参考 (References)
