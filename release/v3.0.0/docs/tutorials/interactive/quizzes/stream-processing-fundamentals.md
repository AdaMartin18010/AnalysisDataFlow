# 流计算基础知识测验

> 所属阶段: 测验 | 前置依赖: [Struct/](../../../Struct/) 理论文档 | 预计时间: 30分钟

## 说明

本测验涵盖流计算的基础理论概念，包括时间语义、窗口、一致性模型等。每题有4个选项，请选择最佳答案。

---

## 第一部分：时间语义 (共5题)

### 问题 1

**在流处理中，Event Time 指的是什么？**

- [ ] A. 数据到达 Flink 的时间
- [ ] B. 数据被处理的时间
- [ ] C. 数据实际产生的时间
- [ ] D. 作业启动的时间

<details>
<summary>答案与解析</summary>

**答案：C**

Event Time 是事件实际发生的时间，通常嵌入在数据本身中。与之相对的是 Ingestion Time（数据进入Flink的时间）和 Processing Time（数据被处理的时间）。

**参考**: [Lab 2: Event Time 处理](../hands-on-labs/lab-02-event-time.md)
</details>

### 问题 2

**Watermark 的主要作用是什么？**

- [ ] A. 加速数据处理
- [ ] B. 处理乱序数据，触发窗口计算
- [ ] C. 压缩数据传输
- [ ] D. 加密敏感数据

<details>
<summary>答案与解析</summary>

**答案：B**

Watermark 是 Flink 处理乱序数据的核心机制。它表示"所有时间戳小于等于该值的事件都已到达"，用于触发窗口计算和处理延迟数据。

**参考**: Flink/02-core-mechanisms/time-semantics-and-watermark.md
</details>

### 问题 3

**以下哪种情况最适合使用 Processing Time？**

- [ ] A. 金融交易对账
- [ ] B. 实时告警系统（低延迟优先）
- [ ] C. 用户行为分析
- [ ] D. 日志审计

<details>
<summary>答案与解析</summary>

**答案：B**

Processing Time 提供最低的延迟，适用于对延迟敏感、可以容忍一定不确定性的场景，如实时告警。对于需要精确结果的场景（如金融交易），应该使用 Event Time。
</details>

### 问题 4

**当 Watermark 为 10:00:00 时，以下哪个事件会被认为是迟到数据？**

- [ ] A. 时间戳为 09:59:55 的事件
- [ ] B. 时间戳为 10:00:00 的事件
- [ ] C. 时间戳为 10:00:01 的事件
- [ ] D. 以上都不是

<details>
<summary>答案与解析</summary>

**答案：A**

Watermark 10:00:00 表示所有时间戳 <= 10:00:00 的事件应该都已到达。因此，时间戳 09:59:55 的事件在 Watermark 10:00:00 之后才到达，属于迟到数据。
</details>

### 问题 5

**Allowed Lateness 的作用是？**

- [ ] A. 增加处理延迟
- [ ] B. 允许在窗口触发后继续接收迟到数据并更新结果
- [ ] C. 减少 Checkpoint 间隔
- [ ] D. 禁用 Watermark

<details>
<summary>答案与解析</summary>

**答案：B**

Allowed Lateness 允许在窗口触发后的一段时间内继续接收和处理迟到数据，并可能更新窗口结果。这对于需要一定准确性的场景很有用。
</details>

---

## 第二部分：窗口机制 (共5题)

### 问题 6

**滚动窗口 (Tumbling Window) 的特点是？**

- [ ] A. 窗口之间可能有重叠
- [ ] B. 每个事件只属于一个窗口，窗口之间不重叠
- [ ] C. 窗口大小不固定
- [ ] D. 窗口之间必须有间隔

<details>
<summary>答案与解析</summary>

**答案：B**

滚动窗口的窗口之间不重叠，每个事件只属于一个窗口。例如，1分钟滚动窗口会将时间划分为 [0,60), [60,120), [120,180) 等不重叠的区间。

**参考**: [Lab 3: Window 聚合](../hands-on-labs/lab-03-window-aggregation.md)
</details>

### 问题 7

**滑动窗口 (Sliding Window) 的参数包括？**

- [ ] A. 仅窗口大小
- [ ] B. 窗口大小和滑动间隔
- [ ] C. 仅滑动间隔
- [ ] D. 窗口大小和会话超时

<details>
<summary>答案与解析</summary>

**答案：B**

滑动窗口有两个参数：窗口大小（Window Size）和滑动间隔（Slide Interval）。如果滑动间隔 < 窗口大小，窗口会重叠，一个事件可能属于多个窗口。
</details>

### 问题 8

**会话窗口 (Session Window) 的关键特性是？**

- [ ] A. 固定大小
- [ ] B. 固定起始时间
- [ ] C. 根据活动间隔动态合并
- [ ] D. 全局唯一

<details>
<summary>答案与解析</summary>

**答案：C**

会话窗口根据活动间隙（Gap）动态创建和合并。如果在指定时间内没有新事件，会话结束；如果新事件在 Gap 内到达，会话会扩展。
</details>

### 问题 9

**AggregateFunction 相比 ProcessWindowFunction 的优势是？**

- [ ] A. 可以访问窗口元数据
- [ ] B. 可以访问窗口内所有数据
- [ ] C. 内存效率更高，支持增量计算
- [ ] D. 支持更复杂的逻辑

<details>
<summary>答案与解析</summary>

**答案：C**

AggregateFunction 支持增量计算，只需要维护一个累加器状态，内存效率高。ProcessWindowFunction 需要缓存窗口内所有元素，内存开销大但功能更强。
</details>

### 问题 10

**窗口触发器 (Trigger) 的作用是？**

- [ ] A. 创建窗口
- [ ] B. 决定何时计算和输出窗口结果
- [ ] C. 删除过期窗口
- [ ] D. 分配事件到窗口

<details>
<summary>答案与解析</summary>

**答案：B**

Trigger 决定何时触发窗口计算并输出结果。默认情况下，当 Watermark 超过窗口结束时间时触发，但可以通过自定义 Trigger 实现提前触发或延迟触发。
</details>

---

## 第三部分：一致性模型 (共5题)

### 问题 11

**Exactly-Once 语义的含义是？**

- [ ] A. 每条数据至少被处理一次
- [ ] B. 每条数据最多被处理一次
- [ ] C. 每条数据恰好被处理一次，结果正确
- [ ] D. 数据不丢失但也不处理

<details>
<summary>答案与解析</summary>

**答案：C**

Exactly-Once 保证每条数据在发生故障恢复后，最终效果等价于恰好处理一次，不会丢失也不会重复处理。注意这指的是结果正确性，而非实际处理次数。

**参考**: Flink/02-core-mechanisms/exactly-once-semantics-deep-dive.md
</details>

### 问题 12

**Flink 的 Checkpoint 机制基于？**

- [ ] A. 两阶段提交
- [ ] B. Chandy-Lamport 分布式快照算法
- [ ] C. Raft 共识算法
- [ ] D. Paxos 算法

<details>
<summary>答案与解析</summary>

**答案：B**

Flink 使用基于 Chandy-Lamport 算法的分布式异步快照机制实现 Checkpoint。这是一种轻量级的快照方式，不会暂停整个流处理。

**参考**: [Lab 5: Checkpoint 与恢复](../hands-on-labs/lab-05-checkpoint.md)
</details>

### 问题 13

**以下哪个不是实现 Exactly-Once 的必要条件？**

- [ ] A. 可重放的数据源
- [ ] B. 状态快照
- [ ] C. 事务性输出
- [ ] D. 无限内存

<details>
<summary>答案与解析</summary>

**答案：D**

Exactly-Once 需要：1) 可重放的数据源（如 Kafka），2) 定期状态快照（Checkpoint），3) 事务性或幂等性输出。不需要无限内存。
</details>

### 问题 14

**Checkpoint 和 Savepoint 的主要区别是？**

- [ ] A. Checkpoint 用于升级，Savepoint 用于容错
- [ ] B. Checkpoint 由 Flink 自动触发，Savepoint 由用户手动触发
- [ ] C. Checkpoint 保存状态，Savepoint 不保存
- [ ] D. Checkpoint 仅支持内存状态

<details>
<summary>答案与解析</summary>

**答案：B**

Checkpoint 是自动触发的容错机制，用于故障恢复；Savepoint 是用户手动触发的，用于作业升级、迁移等运维操作。两者都保存完整状态。

**参考**: [Lab 5: Checkpoint 与恢复](../hands-on-labs/lab-05-checkpoint.md)
</details>

### 问题 15

**Barriers 在 Checkpoint 中的作用是？**

- [ ] A. 分隔数据
- [ ] B. 标记快照边界，确保一致性
- [ ] C. 压缩数据
- [ ] D. 加密数据

<details>
<summary>答案与解析</summary>

**答案：B**

Barriers 是 Flink Checkpoint 的核心机制。它们被周期性地注入数据流，作为快照的边界。当算子收到所有输入流的 Barrier 时，就知道可以安全地对当前状态进行快照。
</details>

---

## 第四部分：状态管理 (共5题)

### 问题 16

**ValueState 和 MapState 的主要区别是？**

- [ ] A. ValueState 更快
- [ ] B. MapState 可以存储键值对集合
- [ ] C. ValueState 支持 TTL
- [ ] D. MapState 只能存储一个值

<details>
<summary>答案与解析</summary>

**答案：B**

ValueState 为每个 key 存储单个值，MapState 为每个 key 存储一个 Map（键值对集合）。两者都支持 TTL。

**参考**: [Lab 4: 状态管理](../hands-on-labs/lab-04-state-management.md)
</details>

### 问题 17

**State TTL 用于解决什么问题？**

- [ ] A. 提高处理速度
- [ ] B. 自动清理过期状态，防止无限增长
- [ ] C. 增加状态可见性
- [ ] D. 减少网络传输

<details>
<summary>答案与解析</summary>

**答案：B**

State TTL（Time-To-Live）允许为状态设置过期时间，过期后自动清理，防止状态无限增长导致内存溢出。
</details>

### 问题 18

**Keyed State 和 Operator State 的区别是？**

- [ ] A. Keyed State 只能用于 Source
- [ ] B. Operator State 按 key 分区
- [ ] C. Keyed State 按 key 分区，Operator State 不分区
- [ ] D. 没有区别

<details>
<summary>答案与解析</summary>

**答案：C**

Keyed State 与特定 key 关联，按 key 分区和并发处理；Operator State 与算子实例关联，通常用于 Source/Sink 等非 keyBy 场景。

**参考**: [Lab 4: 状态管理](../hands-on-labs/lab-04-state-management.md)
</details>

### 问题 19

**RocksDBStateBackend 适合什么场景？**

- [ ] A. 小状态，快速访问
- [ ] B. 大状态，内存有限
- [ ] C. 只读状态
- [ ] D. 临时状态

<details>
<summary>答案与解析</summary>

**答案：B**

RocksDBStateBackend 将状态存储在磁盘上，适合大状态场景。MemoryStateBackend 适合小状态，FsStateBackend 适合中等大小状态。
</details>

### 问题 20

**在 Flink 中，以下哪个操作会自动触发 Checkpoint？**

- [ ] A. map()
- [ ] B. filter()
- [ ] C. keyBy()
- [ ] D. 以上都不会

<details>
<summary>答案与解析</summary>

**答案：D**

Checkpoint 由 Checkpoint Coordinator 周期性地触发，与具体算子操作无关。用户可以通过 env.enableCheckpointing(interval) 启用和配置 Checkpoint。
</details>

---

## 成绩统计

| 部分 | 题数 | 正确率 |
|------|------|--------|
| 时间语义 | 5 | ___/5 |
| 窗口机制 | 5 | ___/5 |
| 一致性模型 | 5 | ___/5 |
| 状态管理 | 5 | ___/5 |
| **总计** | **20** | **___/20** |

### 评分标准

- 18-20 分：优秀，理论基础扎实
- 15-17 分：良好，大部分概念掌握
- 12-14 分：及格，需要复习薄弱环节
- <12 分：建议重新学习相关理论文档

## 下一步

- [Flink 专项测验](./flink-specialized.md)
- [设计模式测验](./design-patterns.md)
- [综合测试](./comprehensive-test.md)
