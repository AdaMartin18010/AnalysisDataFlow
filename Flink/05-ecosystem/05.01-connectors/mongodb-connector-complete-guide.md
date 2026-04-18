# MongoDB Connector 详细指南 (MongoDB Connector Complete Guide)

> **所属阶段**: Flink/04-connectors | **前置依赖**: [../../Flink/04-connectors/flink-connectors-ecosystem-complete-guide.md](flink-connectors-ecosystem-complete-guide.md), [../../Flink/02-core/exactly-once-end-to-end.md](../../02-core/exactly-once-end-to-end.md) | **形式化等级**: L4

---

## 目录

- [MongoDB Connector 详细指南 (MongoDB Connector Complete Guide)](#mongodb-connector-详细指南-mongodb-connector-complete-guide)
  - [目录](#目录)
  - [1. 概念定义 (Definitions)](#1-概念定义-definitions)
    - [Def-F-04-06 (MongoDB Source 定义)](#def-f-04-06-mongodb-source-定义)
    - [Def-F-04-07 (MongoDB Sink 定义)](#def-f-04-07-mongodb-sink-定义)
    - [Def-F-04-08 (集合/文档模型)](#def-f-04-08-集合文档模型)
    - [Def-F-04-09 (Change Streams CDC)](#def-f-04-09-change-streams-cdc)
    - [Def-F-04-10 (MongoDB 幂等写入语义)](#def-f-04-10-mongodb-幂等写入语义)
  - [2. 属性推导 (Properties)](#2-属性推导-properties)
    - [Lemma-F-04-03 (Change Streams 有序性保证)](#lemma-f-04-03-change-streams-有序性保证)
    - [Lemma-F-04-04 (批量写入原子性边界)](#lemma-f-04-04-批量写入原子性边界)
    - [Prop-F-04-02 (MongoDB Sink 幂等性条件)](#prop-f-04-02-mongodb-sink-幂等性条件)
  - [3. 关系建立 (Relations)](#3-关系建立-relations)
    - [关系 1: MongoDB 副本集与 Flink Checkpoint 的映射](#关系-1-mongodb-副本集与-flink-checkpoint-的映射)
    - [关系 2: Change Stream Resume Token 与 Flink 状态后端](#关系-2-change-stream-resume-token-与-flink-状态后端)
    - [关系 3: BSON 类型系统与 Flink SQL 类型的编码关系](#关系-3-bson-类型系统与-flink-sql-类型的编码关系)
  - [4. 论证过程 (Argumentation)](#4-论证过程-argumentation)
    - [4.1 Change Stream 事件排序与时序分析](#41-change-stream-事件排序与时序分析)
    - [4.2 分区策略与并行度匹配分析](#42-分区策略与并行度匹配分析)
    - [4.3 幂等写入与重复数据处理边界](#43-幂等写入与重复数据处理边界)
    - [4.4 连接池配置与资源管理权衡](#44-连接池配置与资源管理权衡)
  - [5. 形式证明 / 工程论证 (Proof / Engineering Argument)](#5-形式证明-工程论证-proof-engineering-argument)
    - [Thm-F-04-03 (Change Streams Source Exactly-Once 正确性)](#thm-f-04-03-change-streams-source-exactly-once-正确性)
    - [Thm-F-04-04 (MongoDB Sink 幂等写入保证)](#thm-f-04-04-mongodb-sink-幂等写入保证)
  - [6. 实例验证 (Examples)](#6-实例验证-examples)
    - [6.1 依赖配置](#61-依赖配置)
    - [6.2 MongoDB Source 基础配置](#62-mongodb-source-基础配置)
    - [6.3 Change Streams CDC 模式](#63-change-streams-cdc-模式)
    - [6.4 MongoDB Sink 基本配置](#64-mongodb-sink-基本配置)
    - [6.5 端到端 CDC 同步示例](#65-端到端-cdc-同步示例)
  - [7. 可视化 (Visualizations)](#7-可视化-visualizations)
    - [7.1 MongoDB-Flink 集成架构图](#71-mongodb-flink-集成架构图)
    - [7.2 Change Streams 事件流序列图](#72-change-streams-事件流序列图)
    - [7.3 批量写入流程图](#73-批量写入流程图)
    - [7.4 数据类型映射矩阵](#74-数据类型映射矩阵)
  - [8. 配置参考 (Configuration Reference)](#8-配置参考-configuration-reference)
    - [8.1 MongoDB Source 配置选项](#81-mongodb-source-配置选项)
    - [8.2 MongoDB Sink 配置选项](#82-mongodb-sink-配置选项)
    - [8.3 连接 URI 参数](#83-连接-uri-参数)
  - [9. 引用参考 (References)](#9-引用参考-references)

---

## 1. 概念定义 (Definitions)

### Def-F-04-06 (MongoDB Source 定义)

MongoDB Source 是从 MongoDB 集合中读取数据的 Flink Source 连接器。设 $M = (D, C, Q)$ 为一个 MongoDB 数据源，其中 $D$ 为数据库实例，$C$ 为目标集合，$Q$ 为查询过滤器：

$$\text{MongoSource}(M) = \{ d \mid d \in C \land Q(d) = \text{true} \}$$

**Source 操作模式**：

| 模式 | 描述 | 适用场景 |
|------|------|----------|
| **批量查询模式** | 一次性扫描集合，应用过滤器投影 | 初始化加载、离线分析 |
| **Change Streams CDC** | 监听变更流，实时捕获数据变化 | 实时同步、事件驱动处理 |
| **混合模式** | 先批量加载，后切换到 CDC | 全量+增量同步 |

**直观解释**：MongoDB Source 提供了两种数据摄取方式。批量模式适合历史数据加载，CDC 模式适合实时变更捕获。混合模式结合了两者优势，支持从任意时间点开始的增量同步[^1][^3]。

### Def-F-04-07 (MongoDB Sink 定义)

MongoDB Sink 是将 Flink 数据流写入 MongoDB 集合的输出连接器。设 $S = (D, C, W, U)$ 为一个 MongoDB Sink，其中 $D$ 为目标数据库，$C$ 为目标集合，$W$ 为写入模式，$U$ 为更新策略：

$$\text{MongoSink}(S, \{r_1, r_2, \dots, r_n\}) = \bigcup_{i=1}^{n} \text{Write}(C, r_i, W, U)$$

**写入模式 (Write Mode)**：

| 模式 | 语义 | 幂等性 |
|------|------|--------|
| **INSERT** | 直接插入，重复键报错 | 否 |
| **REPLACE** | 替换整个文档（upsert） | 是（有 _id） |
| **UPDATE** | 部分字段更新（upsert） | 是（有 _id） |
| **BULK_WRITE** | 批量混合操作 | 依赖具体操作类型 |

**直观解释**：Sink 的写入模式决定了数据如何映射到 MongoDB 文档。REPLACE 模式适合全量同步场景，UPDATE 模式适合增量更新。通过 `_id` 字段实现幂等性是保证 Exactly-Once 语义的关键[^1][^2]。

### Def-F-04-08 (集合/文档模型)

MongoDB 采用文档型数据模型，核心概念包括：

- **数据库 (Database)**: 物理上独立的存储单元，对应 MongoDB 实例中的命名空间
- **集合 (Collection)**: 文档的逻辑分组，无需预定义 Schema，类比关系型数据库的表
- **文档 (Document)**: BSON 格式的数据记录，键值对结构，支持嵌套文档和数组

**BSON 文档结构**：

```bson
{
  "_id": ObjectId("..."),           // 唯一标识符
  "field1": "string value",         // 字符串类型
  "field2": 123,                    // 数值类型
  "nested": {                       // 嵌套文档
    "subField": true
  },
  "tags": ["tag1", "tag2"],         // 数组
  "createdAt": ISODate("...")       // 日期类型
}
```

**与关系模型的映射关系**：

| 关系型数据库 | MongoDB | Flink SQL |
|-------------|---------|-----------|
| 表 (Table) | 集合 (Collection) | Table |
| 行 (Row) | 文档 (Document) | Row |
| 列 (Column) | 字段 (Field) | Field |
| 主键 (Primary Key) | _id | PRIMARY KEY |
| 索引 (Index) | Index | - |
| 外键 (Foreign Key) | 引用/嵌入 | - |

### Def-F-04-09 (Change Streams CDC)

Change Streams 是 MongoDB 3.6+ 提供的变更数据捕获 (CDC) 机制。设 $\mathcal{E}$ 为变更事件流，$t$ 为时间戳，$op$ 为操作类型：

$$\text{ChangeStream}(C) = \{ (t_i, op_i, doc_i, fullDoc_i, token_i) \mid t_i \in \mathbb{T}, op_i \in \{\text{insert}, \text{update}, \text{delete}, \text{replace}\} \}$$

**变更事件结构**：

| 字段 | 类型 | 描述 |
|------|------|------|
| `_id` | Document | 事件唯一标识（包含 resume token） |
| `operationType` | String | 操作类型：insert/update/delete/replace |
| `ns` | Document | 命名空间 { db, coll } |
| `documentKey` | Document | 被修改文档的 _id |
| `fullDocument` | Document | 完整文档内容（可配置） |
| `updateDescription` | Document | 更新字段描述（仅 update） |
| `clusterTime` | Timestamp | 操作时间戳 |

**Resume Token 机制**：

Resume Token 是 Change Stream 的位置标识符，支持从任意点恢复消费：

$$\text{Resume}(token_k) \Rightarrow \text{Stream from event } e_{k+1}$$

**直观解释**：Change Streams 基于 MongoDB oplog（操作日志）实现，提供与主从复制相同的强一致性保证。Resume Token 持久化到 Flink 状态后端后，可实现故障时的精确恢复[^1][^4]。

### Def-F-04-10 (MongoDB 幂等写入语义)

幂等写入保证相同操作多次执行结果一致。设 $w$ 为写入操作，$s$ 为文档状态：

$$\text{Idempotent}(w) \iff w(w(s)) = w(s)$$

**MongoDB 幂等写入实现**：

| 机制 | 实现方式 | 保证级别 |
|------|----------|----------|
| **_id 唯一性** | 文档主键约束 | 单文档级 |
| **ReplaceOne upsert** | 存在则替换，不存在则插入 | 文档级 |
| **UpdateOne upsert** | 基于操作符的部分更新 | 字段级 |
| **事务 (Multi-doc)** | 多文档 ACID 事务 | 事务级 |

**直观解释**：通过将 Flink 数据的唯一键映射到 MongoDB `_id` 字段，配合 upsert 语义，可以实现 Sink 端的幂等写入。这在 Flink 任务失败重试时防止数据重复[^2][^5]。

---

## 2. 属性推导 (Properties)

### Lemma-F-04-03 (Change Streams 有序性保证)

**陈述**：单个 Change Stream 中的事件严格按照操作发生的先后顺序排列。

**形式化表述**：设 $\mathcal{E} = (e_1, e_2, \dots, e_n)$ 为 Change Stream 事件序列，$t(e)$ 为事件时间戳：

$$\forall i, j. \; i < j \Rightarrow t(e_i) \leq t(e_j)$$

**证明**：

1. Change Stream 基于 MongoDB oplog 实现
2. oplog 是 MongoDB 主节点的 capped collection，记录所有写操作
3. MongoDB 保证 oplog 条目按照操作发生顺序追加
4. Change Stream 按顺序读取 oplog 并生成事件
5. 因此 Change Stream 事件顺序与原始操作顺序一致

注意：此保证仅限于**单个集合**的 Change Stream。跨集合或多分片场景下，事件顺序可能因网络延迟等因素产生相对乱序[^4]。∎

### Lemma-F-04-04 (批量写入原子性边界)

**陈述**：MongoDB 批量写入操作（BulkWrite）的原子性边界为单个批次，而非单个文档。

**形式化表述**：设 $B = \{w_1, w_2, \dots, w_n\}$ 为一个批量写入批次：

$$\text{Atomic}(B) \iff \forall w \in B. \; \text{Success}(w) \lor \forall w \in B. \; \text{Fail}(w)$$

**证明**：

1. MongoDB `bulkWrite` 操作默认使用 `ordered: true` 模式
2. 有序模式下，任一操作失败将中止后续操作
3. 已成功的操作不会回滚（无事务支持时）
4. 使用多文档事务时，整个批次作为原子单元提交
5. Flink MongoDB Connector 的批量写入不强制使用事务，因此原子性边界为批次级别

因此，在异常场景下，批量写入可能出现部分成功状态，需要配合幂等性机制保证数据一致性[^2]。∎

### Prop-F-04-02 (MongoDB Sink 幂等性条件)

**陈述**：MongoDB Sink 实现端到端 Exactly-Once 的充要条件为：(1) 每个记录具有唯一标识，(2) 使用 upsert 语义写入，(3) 开启 Flink Checkpoint。

**形式化表述**：

$$
\text{ExactlyOnce}(Sink) \iff \begin{cases}
\exists key(r). \; \forall r. \; \text{unique}(key(r)) \\
\text{WriteMode} \in \{REPLACE, UPDATE\} \land \text{upsert} = \text{true} \\
\text{CheckpointingEnabled} = \text{true}
\end{cases}
$$

**工程论证**：

1. **唯一标识**：将 Flink 记录的唯一键映射到 `_id`，确保相同记录多次写入定位到同一文档
2. **Upsert 语义**：REPLACE/UPDATE 模式配合 upsert=true，实现"存在则更新，不存在则插入"
3. **Checkpoint 机制**：Flink 两阶段提交保证"至少一次"写入，幂等性保证"至多一次"，合起来实现 Exactly-Once

因此，满足上述三个条件时，即使 Flink 任务失败重启，也不会产生重复数据[^5]。∎

---

## 3. 关系建立 (Relations)

### 关系 1: MongoDB 副本集与 Flink Checkpoint 的映射

MongoDB 副本集为 Change Streams 提供高可用基础，与 Flink Checkpoint 形成互补：

```
┌─────────────────────────────────────────────────────────────┐
│                    MongoDB Replica Set                       │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐             │
│  │ Primary  │────▶│ Secondary│     │ Secondary│             │
│  │ (oplog)  │     │ (sync)   │     │ (sync)   │             │
│  └────┬─────┘     └──────────┘     └──────────┘             │
│       │                                                      │
│       │ Change Stream                                        │
│       ▼                                                      │
│  ┌──────────┐                                                │
│  │  Events  │──────────────┐                                 │
│  └──────────┘              │                                 │
└────────────────────────────┼─────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    Flink Source Operator                     │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐             │
│  │  Event 1 │────▶│  Event 2 │────▶│  Event 3 │             │
│  └────┬─────┘     └────┬─────┘     └────┬─────┘             │
│       │                │                │                   │
│       └────────────────┴────────────────┘                   │
│                     │                                       │
│                     ▼ Checkpoint Barrier                    │
│              ┌──────────────┐                               │
│              │ Resume Token │───▶ State Backend            │
│              │   (offset)   │                               │
│              └──────────────┘                               │
└─────────────────────────────────────────────────────────────┘
```

**映射关系**：

| MongoDB 概念 | Flink 概念 | 作用 |
|-------------|-----------|------|
| Primary oplog | Event Source | 变更数据来源 |
| Resume Token | Offset / State | 消费位置标识 |
| Secondary 选举 | Failover | 高可用切换 |
| Read Concern | Consistency Level | 一致性级别 |

### 关系 2: Change Stream Resume Token 与 Flink 状态后端

Resume Token 的持久化是 Change Stream Source 实现容错的关键：

$$
\text{State}(checkpoint_k) = \{ token_k, ts_k, \text{pendingEvents}_k \}
$$

**状态恢复流程**：

1. **Checkpoint 触发**：Source 将当前 Resume Token 写入状态快照
2. **故障发生**：Flink 从最近成功的 Checkpoint 恢复
3. **状态恢复**：Source 读取 Resume Token，重建 Change Stream 游标
4. **数据重放**：从 Resume Token 对应位置继续消费，可能产生重复事件
5. **去重处理**：下游算子通过状态或 Sink 幂等性消除重复

### 关系 3: BSON 类型系统与 Flink SQL 类型的编码关系

BSON 到 Flink 类型的映射是数据互操作的基础：

$$
\text{Encode}: \text{BSON} \rightarrow \text{Flink SQL Type}
$$

| BSON 类型 | Flink SQL 类型 | 说明 |
|----------|----------------|------|
| ObjectId | STRING | 24 字符十六进制字符串 |
| String | STRING | 直接映射 |
| Int32 | INT | 32 位有符号整数 |
| Int64 | BIGINT | 64 位有符号整数 |
| Double | DOUBLE | 双精度浮点数 |
| Decimal128 | DECIMAL | 高精度十进制数 |
| Boolean | BOOLEAN | 布尔值 |
| Date | TIMESTAMP | 日期时间 |
| Array | ARRAY<T> | 元素类型需一致 |
| Document | ROW | 嵌套结构 |
| Null | NULL | 空值 |

---

## 4. 论证过程 (Argumentation)

### 4.1 Change Stream 事件排序与时序分析

**问题**：Change Stream 是否能保证全局有序？

**分析**：

1. **单集合有序性**：单个集合的 Change Stream 事件严格按照 oplog 顺序排列，即操作发生的因果顺序
2. **跨集合乱序**：多个 Change Stream 并发消费时，由于网络延迟和处理时间差异，事件到达顺序可能与发生顺序不一致
3. **分片集群**：分片集群中，Change Stream 需要聚合多个分片的 oplog，聚合过程中可能引入乱序

**解决方案**：

| 场景 | 策略 | 说明 |
|------|------|------|
| 严格有序 | 单分区 Source | 牺牲并行度换取顺序性 |
| 最终一致 | 事件时间+Watermark | 允许短暂乱序，按事件时间处理 |
| 因果一致 | 业务时间戳 | 使用文档中的业务时间字段排序 |

### 4.2 分区策略与并行度匹配分析

MongoDB Source 的分区策略影响读取性能：

| 分区策略 | 原理 | 适用场景 |
|----------|------|----------|
| **SplitVector** | 基于数据分布的均匀切分 | 大集合，数据分布均匀 |
| **Sample** | 随机采样估算边界 | 未知数据分布 |
| **_id 范围** | 基于 ObjectId 的时间范围 | 时序数据 |
| **自定义** | 用户指定分区键 | 已知最优分区键 |

**并行度匹配**：

```
并行度 = min(分区数, 可用 Slot 数)
```

- 分区数 > 并行度：部分 Slot 处理多个分区
- 分区数 < 并行度：部分 Slot 空闲
- 最优：分区数 = 并行度，实现负载均衡

### 4.3 幂等写入与重复数据处理边界

**重复数据来源**：

1. **Source 重放**：Change Stream 从 Resume Token 恢复后，可能重新发送已处理事件
2. **算子重算**：Flink 故障恢复后，部分算子需要重新处理数据
3. **Sink 重试**：网络超时导致的写入重试

**幂等写入边界**：

| 幂等性级别 | 实现方式 | 边界条件 |
|-----------|----------|----------|
| 文档级 | _id + upsert | 相同 _id 的重复写入 |
| 批次级 | 事务 + 唯一键 | 整个批次的重复提交 |
| 作业级 | 作业 ID + 版本 | 同一作业实例的重复执行 |

### 4.4 连接池配置与资源管理权衡

MongoDB Java Driver 连接池参数影响资源使用：

| 参数 | 作用 | 权衡 |
|------|------|------|
| `maxPoolSize` | 最大连接数 | 过大：资源浪费；过小：连接等待 |
| `minPoolSize` | 最小连接数 | 过大：空闲连接；过小：频繁创建 |
| `maxConnectionLifeTime` | 连接最大生命周期 | 过长：连接老化；过短：频繁重建 |
| `waitQueueTimeout` | 连接等待超时 | 过长：阻塞；过短：超时异常 |

**推荐配置**（根据 Flink 并行度）：

```
maxPoolSize = Flink 并行度 × 2 + 1
minPoolSize = Flink 并行度
```

---

## 5. 形式证明 / 工程论证 (Proof / Engineering Argument)

### Thm-F-04-03 (Change Streams Source Exactly-Once 正确性)

**定理**：在满足以下条件时，MongoDB Change Streams Source 与 Flink Checkpoint 结合可实现 Exactly-Once 语义：

1. Resume Token 持久化到状态后端
2. Change Stream 使用 `fullDocument: updateLookup` 或等效选项
3. 下游算子具备幂等性或去重能力

**证明**：

**引理 1**（Resume Token 单调性）：MongoDB Resume Token 具有单调递增特性，新事件的 Token 始终大于旧事件。

**引理 2**（状态快照一致性）：Flink Checkpoint 机制保证状态快照的原子性，Resume Token 的持久化与 Checkpoint 成功同步。

**主证明**：

设 $E = (e_1, e_2, \dots, e_n)$ 为 Change Stream 事件序列，$C_k$ 为第 $k$ 个 Checkpoint。

1. **正常流程**：
   - Source 消费事件 $e_i$，推进 Resume Token $token_i$
   - 触发 Checkpoint $C_k$，将 $token_{m}$ 持久化（$m$ 为 $C_k$ 前最后处理的事件）
   - Checkpoint 成功，已处理事件 $e_1$ 到 $e_m$ 的 Resume Token 已保存

2. **故障恢复**：
   - 故障发生后，Flink 从 Checkpoint $C_k$ 恢复
   - Source 读取保存的 $token_m$，重建 Change Stream 游标
   - 根据引理 1，新游标从 $e_{m+1}$ 开始消费

3. **边界分析**：
   - $e_m$ 可能已发送到下游但未确认（in-flight）
   - 下游算子可能重复处理 $e_m$
   - 根据条件 3，下游幂等性或去重机制消除重复

4. **Exactly-Once 保证**：
   - 不会丢失数据：Resume Token 保证从 $e_{m+1}$ 继续
   - 不会重复数据：下游幂等性消除重复
   - 因此实现 Exactly-Once

∎

### Thm-F-04-04 (MongoDB Sink 幂等写入保证)

**定理**：当使用 `_id` 字段作为唯一键并配合 upsert 语义时，MongoDB Sink 实现幂等写入。

**证明**：

设 $d$ 为待写入文档，$C$ 为目标集合，$s$ 为集合当前状态。

**情况 1**：文档不存在（首次写入）

$$C' = C \cup \{d\} \quad \text{where } d._id \notin \{c._id \mid c \in C\}$$

**情况 2**：文档已存在（重复写入）

$$\text{Replace}(C, d) = (C \setminus \{c \mid c._id = d._id\}) \cup \{d\}$$

**幂等性验证**：

$$\text{Replace}(\text{Replace}(C, d), d) = \text{Replace}(C, d)$$

两次 Replace 操作后，集合状态与一次 Replace 相同，因此幂等。

**扩展到 Flink 场景**：

设 $r$ 为 Flink 记录，$f$ 为映射函数 $r \rightarrow d$：

$$\text{Idempotent}(Sink) \iff \exists f. \; \forall r. \; f(r)._id = \text{unique}(r)$$

因此，只要保证：

1. 映射函数为相同记录生成相同 _id
2. 使用 upsert 语义

Sink 即实现幂等写入。∎

---

## 6. 实例验证 (Examples)

### 6.1 依赖配置

**Maven 依赖**：

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-mongodb</artifactId>
    <version>1.2.0</version>
</dependency>

<!-- MongoDB Java Driver (若连接器未包含) -->
<dependency>
    <groupId>org.mongodb</groupId>
    <artifactId>mongodb-driver-sync</artifactId>
    <version>4.11.1</version>
</dependency>
```

**Gradle 依赖**：

```groovy
dependencies {
    implementation 'org.apache.flink:flink-connector-mongodb:1.2.0'
    implementation 'org.mongodb:mongodb-driver-sync:4.11.1'
}
```

### 6.2 MongoDB Source 基础配置

**Java API 示例**（批量查询模式）：

```java
import org.apache.flink.connector.mongodb.source.MongoSource;
import org.apache.flink.connector.mongodb.source.config.MongoReadOptions;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

public class MongoDBSourceExample {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(2);

        // 配置 MongoDB Source
        MongoSource<Document> mongoSource = MongoSource.<Document>builder()
            .setUri("mongodb://user:password@localhost:27017")
            .setDatabase("mydb")
            .setCollection("users")
            // 查询过滤器 - 只读取 age >= 18 的文档
            .setFilter(BsonDocument.parse("{ \"age\": { \"$gte\": 18 } }"))
            // 投影优化 - 只读取需要的字段
            .setProjection(BsonDocument.parse("{ \"name\": 1, \"email\": 1, \"_id\": 1 }"))
            // 分区策略
            .setPartitionStrategy(PartitionStrategy.SAMPLE)
            .setSampleSize(1000)
            // 读取选项
            .setFetchSize(1000)
            .setLimit(10000L)
            .build();

        DataStream<Document> stream = env.fromSource(
            mongoSource,
            WatermarkStrategy.noWatermarks(),
            "MongoDB Source"
        );

        stream.print();
        env.execute("MongoDB Source Example");
    }
}
```

**SQL API 示例**：

```sql
-- 创建 MongoDB 表
CREATE TABLE users (
    _id STRING,
    name STRING,
    email STRING,
    age INT,
    created_at TIMESTAMP(3),
    PRIMARY KEY (_id) NOT ENFORCED
) WITH (
    'connector' = 'mongodb',
    'uri' = 'mongodb://user:password@localhost:27017',
    'database' = 'mydb',
    'collection' = 'users',
    'filter' = '{"age": {"$gte": 18}}',
    'projection' = '{"name": 1, "email": 1, "_id": 1}',
    'partitionStrategy' = 'SAMPLE',
    'fetchSize' = '1000'
);

-- 查询数据
SELECT name, email, age
FROM users
WHERE age >= 18;
```

### 6.3 Change Streams CDC 模式

**Java API 示例**（CDC 模式）：

```java
import org.apache.flink.connector.mongodb.source.MongoSource;
import org.apache.flink.connector.mongodb.source.config.MongoChangeStreamOptions;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;


public class MongoDBCDCExample {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.enableCheckpointing(60000); // 60 秒 Checkpoint

        // 配置 Change Stream Source
        MongoSource<ChangeStreamDocument<Document>> cdcSource = MongoSource
            .<ChangeStreamDocument<Document>>builder()
            .setUri("mongodb://user:password@localhost:27017/?replicaSet=rs0")
            .setDatabase("mydb")
            .setCollection("orders")
            // 启用 Change Streams
            .setChangeStreamOptions(
                MongoChangeStreamOptions.builder()
                    // 全文档查询 - 包含变更后的完整文档
                    .setFullDocument(FullDocument.UPDATE_LOOKUP)
                    // 监听操作类型
                    .setOperationTypes(
                        OperationType.INSERT,
                        OperationType.UPDATE,
                        OperationType.REPLACE
                    )
                    // 从当前时间点开始
                    .setStartAtOperationTime(Instant.now())
                    .build()
            )
            .build();

        DataStream<ChangeStreamDocument<Document>> changeStream = env.fromSource(
            cdcSource,
            WatermarkStrategy.forBoundedOutOfOrderness(
                Duration.ofSeconds(5)
            ),
            "MongoDB CDC Source"
        );

        // 处理变更事件
        changeStream.map(event -> {
            String operation = event.getOperationType().getValue();
            Document fullDoc = event.getFullDocument();
            BsonDocument key = event.getDocumentKey();

            System.out.printf("Operation: %s, Key: %s, Doc: %s%n",
                operation, key, fullDoc);
            return event;
        });

        env.execute("MongoDB CDC Example");
    }
}
```

**处理变更事件**：

```java
import org.apache.flink.api.common.functions.MapFunction;

// 将 Change Stream 事件转换为标准格式
public class ChangeStreamProcessor
    implements MapFunction<ChangeStreamDocument<Document>, Row> {

    @Override
    public Row map(ChangeStreamDocument<Document> event) {
        Row row = new Row(5);

        // 操作类型: INSERT/UPDATE/DELETE
        row.setField(0, event.getOperationType().getValue());

        // 文档主键
        row.setField(1, event.getDocumentKey().getObjectId("_id").toString());

        // 变更时间戳
        row.setField(2, event.getClusterTime());

        // 完整文档 (UPDATE_LOOKUP 模式)
        Document fullDoc = event.getFullDocument();
        row.setField(3, fullDoc != null ? fullDoc.toJson() : null);

        // 更新描述 (仅 UPDATE 操作)
        UpdateDescription updateDesc = event.getUpdateDescription();
        row.setField(4, updateDesc != null ? updateDesc.toString() : null);

        return row;
    }
}
```

### 6.4 MongoDB Sink 基本配置

**Java API 示例**（Replace 模式）：

```java
import org.apache.flink.connector.mongodb.sink.MongoSink;
import org.apache.flink.connector.mongodb.sink.config.MongoWriteOptions;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;


public class MongoDBSinkExample {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.enableCheckpointing(60000);

        // 输入数据流
        DataStream<Document> input = env.fromElements(
            new Document()
                .append("_id", new ObjectId())
                .append("user_id", "U001")
                .append("amount", 100.50)
                .append("status", "completed")
                .append("created_at", new Date())
        );

        // 配置 MongoDB Sink
        MongoSink<Document> mongoSink = MongoSink.<Document>builder()
            .setUri("mongodb://user:password@localhost:27017")
            .setDatabase("mydb")
            .setCollection("transactions")
            // 写入模式: REPLACE (upsert)
            .setWriteMode(WriteMode.REPLACE)
            // 批量配置
            .setBatchSize(1000)
            .setBatchIntervalMs(1000)
            // 重试配置
            .setMaxRetries(3)
            .setRetryIntervalMs(1000)
            // 连接选项
            .setMaxConnectionIdleTime(60000)
            .build();

        input.sinkTo(mongoSink);
        env.execute("MongoDB Sink Example");
    }
}
```

**Update 模式示例**：

```java
// 配置为 Update 模式 - 只更新指定字段
MongoSink<Document> updateSink = MongoSink.<Document>builder()
    .setUri("mongodb://user:password@localhost:27017")
    .setDatabase("mydb")
    .setCollection("users")
    .setWriteMode(WriteMode.UPDATE)
    // 更新键 - 用于定位文档
    .setUpdateKey("_id")
    // 允许 upsert
    .setUpsert(true)
    .setBatchSize(500)
    .build();

// 数据需要包含更新操作符
Document updateDoc = new Document()
    .append("_id", "user001")
    .append("$set", new Document()
        .append("last_login", new Date())
        .append("login_count", 1)
    )
    .append("$inc", new Document()
        .append("visit_count", 1)
    );
```

**SQL API 示例**：

```sql
-- 创建目标表
CREATE TABLE transactions_sink (
    _id STRING,
    user_id STRING,
    amount DECIMAL(10, 2),
    status STRING,
    created_at TIMESTAMP(3),
    PRIMARY KEY (_id) NOT ENFORCED
) WITH (
    'connector' = 'mongodb',
    'uri' = 'mongodb://user:password@localhost:27017',
    'database' = 'mydb',
    'collection' = 'transactions',
    'writeMode' = 'REPLACE',
    'batch.size' = '1000',
    'batch.intervalMs' = '1000',
    'maxRetries' = '3'
);

-- 插入数据
INSERT INTO transactions_sink
SELECT
    CAST(user_id AS STRING) as _id,
    user_id,
    amount,
    status,
    created_at
FROM orders
WHERE status = 'completed';
```

### 6.5 端到端 CDC 同步示例

**完整 CDC 同步 Pipeline**：

```java
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.TableEnvironment;


public class MongoDBCDCtoSinkExample {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.enableCheckpointing(60000);

        StreamTableEnvironment tEnv = StreamTableEnvironment.create(env);

        // ========== 1. 配置 CDC Source ==========
        MongoSource<ChangeStreamDocument<Document>> cdcSource = MongoSource
            .<ChangeStreamDocument<Document>>builder()
            .setUri("mongodb://srcUser:srcPass@srcHost:27017/?replicaSet=rs0")
            .setDatabase("source_db")
            .setCollection("orders")
            .setChangeStreamOptions(
                MongoChangeStreamOptions.builder()
                    .setFullDocument(FullDocument.UPDATE_LOOKUP)
                    .setOperationTypes(
                        OperationType.INSERT,
                        OperationType.UPDATE,
                        OperationType.REPLACE,
                        OperationType.DELETE
                    )
                    .build()
            )
            .build();

        DataStream<ChangeStreamDocument<Document>> cdcStream = env.fromSource(
            cdcSource,
            WatermarkStrategy.forMonotonousTimestamps(),
            "MongoDB CDC"
        );

        // ========== 2. 处理 CDC 事件 ==========
        DataStream<Document> processedStream = cdcStream
            .map(new CDCEventTransformer())
            .filter(Objects::nonNull);

        // ========== 3. 配置目标 Sink ==========
        MongoSink<Document> targetSink = MongoSink.<Document>builder()
            .setUri("mongodb://tgtUser:tgtPass@tgtHost:27017/?replicaSet=rs1")
            .setDatabase("target_db")
            .setCollection("orders_replica")
            .setWriteMode(WriteMode.REPLACE)
            .setUpsert(true)
            .setBatchSize(1000)
            .build();

        // ========== 4. 执行同步 ==========
        processedStream.sinkTo(targetSink);
        env.execute("MongoDB CDC Sync");
    }
}

// CDC 事件转换器
class CDCEventTransformer
    implements MapFunction<ChangeStreamDocument<Document>, Document> {

    @Override
    public Document map(ChangeStreamDocument<Document> event) {
        OperationType opType = event.getOperationType();

        switch (opType) {
            case INSERT:
            case REPLACE:
                // 直接写入完整文档
                return event.getFullDocument();

            case UPDATE:
                // 合并更新到完整文档
                Document fullDoc = event.getFullDocument();
                if (fullDoc != null) {
                    // 添加同步标记
                    fullDoc.append("_sync_time", new Date());
                    return fullDoc;
                }
                return null;

            case DELETE:
                // 发送删除标记或执行删除
                BsonDocument key = event.getDocumentKey();
                return new Document()
                    .append("_id", key.getObjectId("_id").getValue())
                    .append("_deleted", true)
                    .append("_deleted_at", new Date());

            default:
                return null;
        }
    }
}
```

---

## 7. 可视化 (Visualizations)

### 7.1 MongoDB-Flink 集成架构图

```mermaid
graph TB
    subgraph MongoDB_Cluster["MongoDB Cluster"]
        RS1["Primary (oplog)"]
        RS2["Secondary"]
        RS3["Secondary"]
        Collection[(Collection)]

        RS1 -->|"replicate"| RS2
        RS1 -->|"replicate"| RS3
        RS1 -->|"read/write"| Collection
    end

    subgraph Flink_Cluster["Flink Cluster"]
        subgraph Source_Operators["Source Operators"]
            S1["MongoSource<br/>Parallelism=2"]
            S2["ChangeStreamSource<br/>Parallelism=1"]
        end

        subgraph Processing["Processing"]
            P1["Map/Filter"]
            P2["Window/Aggregate"]
        end

        subgraph Sink_Operators["Sink Operators"]
            SK1["MongoSink<br/>Replace Mode"]
            SK2["MongoSink<br/>Update Mode"]
        end
    end

    subgraph State_Backend["State Backend"]
        Checkpoint[(Checkpoint)]
        ResumeToken["Resume Token"]
    end

    Collection -->|"Batch Query"| S1
    RS1 -->|"Change Stream"| S2
    S1 --> P1
    S2 --> P1
    P1 --> P2
    P2 --> SK1
    P2 --> SK2
    S2 -.->|"persist"| ResumeToken
    ResumeToken -.->|"snapshot"| Checkpoint
```

### 7.2 Change Streams 事件流序列图

```mermaid
sequenceDiagram
    participant App as Application
    participant FS as Flink Source
    participant MC as MongoDB Client
    participant MP as MongoDB Primary
    participant OP as Oplog

    App->>FS: Create Change Stream
    FS->>MC: watch(collection)
    MC->>MP: Establish cursor
    MP->>OP: Read oplog entries
    OP-->>MC: Stream changes
    MC-->>FS: ChangeStreamDocument
    FS->>FS: Deserialize to Row
    FS->>App: Emit record

    Note over FS,Checkpoint: Checkpoint Triggered
    FS->>FS: snapshotState()
    FS->>Checkpoint: Save Resume Token
    Checkpoint-->>FS: Confirm
    FS->>App: notifyCheckpointComplete()

    Note over App,MP: Failure & Recovery
    MP--xFS: Connection lost
    App->>FS: Restore from checkpoint
    FS->>Checkpoint: Get Resume Token
    FS->>MC: watch() with resumeAfter
    MC->>MP: Resume from token
    MP->>OP: Continue reading
```

### 7.3 批量写入流程图

```mermaid
flowchart TD
    A["Flink Record Stream"] --> B{"Buffer Records"}
    B -->|"Batch Size >= N"| C["Flush Batch"]
    B -->|"Interval >= T"| C
    C --> D["Create BulkWrite"]
    D --> E["Group by Operation Type"]
    E --> F["Send to MongoDB"]
    F --> G{"Success?"}
    G -->|"Yes"| H["Clear Buffer"]
    G -->|"No"| I{"Retry < Max?"}
    I -->|"Yes"| J["Wait Interval"]
    J --> F
    I -->|"No"| K["Throw Exception"]
    K --> L["Trigger Failover"]
    H --> M["Commit Checkpoint"]
```

### 7.4 数据类型映射矩阵

```mermaid
graph LR
    subgraph BSON["BSON Types"]
        B1[ObjectId]
        B2[String]
        B3[Int32]
        B4[Int64]
        B5[Double]
        B6[Decimal128]
        B7[Boolean]
        B8[Date]
        B9[Array]
        B10[Document]
        B11[Null]
    end

    subgraph Flink["Flink SQL Types"]
        F1[STRING]
        F2[STRING]
        F3[INT]
        F4[BIGINT]
        F5[DOUBLE]
        F6[DECIMAL]
        F7[BOOLEAN]
        F8[TIMESTAMP]
        F9[ARRAY<T>]
        F10[ROW]
        F11[NULL]
    end

    B1 -->|"toHexString"| F1
    B2 -->|"direct"| F2
    B3 -->|"intValue"| F3
    B4 -->|"longValue"| F4
    B5 -->|"doubleValue"| F5
    B6 -->|"bigDecimalValue"| F6
    B7 -->|"booleanValue"| F7
    B8 -->|"toInstant"| F8
    B9 -->|"toList"| F9
    B10 -->|"toRow"| F10
    B11 -->|"null"| F11
```

---

## 8. 配置参考 (Configuration Reference)

### 8.1 MongoDB Source 配置选项

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `uri` | String | 必填 | MongoDB 连接 URI |
| `database` | String | 必填 | 数据库名称 |
| `collection` | String | 必填 | 集合名称 |
| `filter` | String | null | 查询过滤器 (JSON) |
| `projection` | String | null | 投影字段 (JSON) |
| `partitionStrategy` | Enum | `SAMPLE` | 分区策略: `SAMPLE`, `SPLIT_VECTOR`, `ID_RANGE` |
| `splitSize` | Integer | 64MB | 分区大小 (字节) |
| `fetchSize` | Integer | 1000 | 每批次读取文档数 |
| `limit` | Long | null | 最大读取文档数 |
| `noCursorTimeout` | Boolean | true | 游标永不超时 |
| `readPreference` | String | `primary` | 读偏好: `primary`, `secondary`, `nearest` |
| `readConcern` | String | `majority` | 读关注级别 |

**CDC 专用配置**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `changeStreamFullDocument` | Enum | `UPDATE_LOOKUP` | 全文档模式: `DEFAULT`, `UPDATE_LOOKUP`, `REQUIRED` |
| `changeStreamOperationTypes` | List | all | 监听操作类型 |
| `changeStreamStartAt` | String | `now` | 起始点: `now`, `timestamp` |
| `changeStreamResumeAfter` | String | null | 从指定 Resume Token 恢复 |

### 8.2 MongoDB Sink 配置选项

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `uri` | String | 必填 | MongoDB 连接 URI |
| `database` | String | 必填 | 数据库名称 |
| `collection` | String | 必填 | 集合名称 |
| `writeMode` | Enum | `INSERT` | 写入模式: `INSERT`, `REPLACE`, `UPDATE` |
| `upsert` | Boolean | true | 允许 upsert (REPLACE/UPDATE) |
| `updateKey` | String | `_id` | 更新键字段 |
| `batchSize` | Integer | 1000 | 批量写入大小 |
| `batchIntervalMs` | Integer | 1000 | 批量间隔 (毫秒) |
| `maxRetries` | Integer | 3 | 最大重试次数 |
| `retryIntervalMs` | Integer | 1000 | 重试间隔 (毫秒) |
| `writeConcern` | String | `acknowledged` | 写关注: `w1`, `wmajority`, `jtrue` |

### 8.3 连接 URI 参数

**标准 URI 格式**：

```
mongodb://[username:password@]host1[:port1][,host2[:port2],...[/[database][?options]]
```

**常用连接参数**：

| 参数 | 说明 | 示例 |
|------|------|------|
| `replicaSet` | 副本集名称 | `replicaSet=rs0` |
| `authSource` | 认证数据库 | `authSource=admin` |
| `ssl` | 启用 SSL | `ssl=true` |
| `connectTimeoutMS` | 连接超时 | `connectTimeoutMS=10000` |
| `socketTimeoutMS` | Socket 超时 | `socketTimeoutMS=0` |
| `maxPoolSize` | 最大连接池 | `maxPoolSize=50` |
| `minPoolSize` | 最小连接池 | `minPoolSize=10` |
| `maxConnectionLifeTimeMS` | 连接最大生命周期 | `maxConnectionLifeTimeMS=0` |
| `waitQueueTimeoutMS` | 等待队列超时 | `waitQueueTimeoutMS=5000` |
| `readPreference` | 读偏好 | `readPreference=secondaryPreferred` |
| `readConcernLevel` | 读关注 | `readConcernLevel=majority` |
| `w` | 写关注 | `w=majority` |
| `journal` | 日志提交 | `journal=true` |

**完整示例**：

```
mongodb://user:pass@host1:27017,host2:27017,host3:27017/mydb?replicaSet=rs0&authSource=admin&maxPoolSize=50&w=majority&readPreference=secondaryPreferred
```

---

## 9. 引用参考 (References)

[^1]: Apache Flink Documentation, "MongoDB Connector", 2024. <https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/mongodb/>

[^2]: MongoDB Documentation, "MongoDB Connector for Apache Flink", 2024. <https://www.mongodb.com/docs/kafka-connector/current/>

[^3]: MongoDB Documentation, "Change Streams", 2024. <https://www.mongodb.com/docs/manual/changeStreams/>

[^4]: MongoDB Documentation, "Change Events", 2024. <https://www.mongodb.com/docs/manual/reference/change-events/>

[^5]: Apache Flink Documentation, "Exactly Once Semantics", 2024. <https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/streaming_analytics/>
