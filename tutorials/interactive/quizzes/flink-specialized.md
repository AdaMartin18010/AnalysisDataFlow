# Flink 专项测验

> 所属阶段: 测验 | 前置依赖: [Flink/](../../../Flink/) 文档 | 预计时间: 30分钟

## 说明

本测验专注于 Flink 的特定功能和最佳实践，包括 DataStream API、SQL/Table API、Connectors、部署等。

---

## 第一部分：DataStream API (共5题)

### 问题 1

**以下哪个是 Flink DataStream 的转换操作？**

- [ ] A. groupByKey()
- [ ] B. reduceByKey()
- [ ] C. keyBy()
- [ ] D. cogroup()

<details>
<summary>答案与解析</summary>

**答案：C**

Flink DataStream API 使用 `keyBy()` 进行逻辑分区（类似于 key 分组）。`groupByKey()` 和 `reduceByKey()` 是 Spark API，`cogroup()` 不是标准转换。
</details>

### 问题 2

**FlatMapFunction 的返回值是？**

- [ ] A. 单个元素
- [ ] B. 集合
- [ ] C. 通过 Collector 输出零个或多个元素
- [ ] D. 布尔值

<details>
<summary>答案与解析</summary>

**答案：C**

FlatMapFunction 通过 Collector 输出零个或多个元素，实现一对一、一对多或过滤（零个输出）的转换。

**参考**: [Lab 1: 第一个 Flink 程序](../hands-on-labs/lab-01-first-flink-program.md)
</details>

### 问题 3

**在 Flink 中，以下哪种方式可以实现双流 Join？**

- [ ] A. union()
- [ ] B. connect()
- [ ] C. join() 和 coGroup()
- [ ] D. merge()

<details>
<summary>答案与解析</summary>

**答案：C**

Flink 提供 `join()` 用于窗口内内连接，`coGroup()` 用于更灵活的窗口连接。`union()` 只是简单合并流，`connect()` 连接后需要定义 CoProcessFunction。
</details>

### 问题 4

**ProcessFunction 相比普通转换函数的优势是？**

- [ ] A. 执行速度更快
- [ ] B. 可以访问状态和时间（event time/processing time）
- [ ] C. 使用更少的内存
- [ ] D. 自动并行化

<details>
<summary>答案与解析</summary>

**答案：B**

ProcessFunction 是 Flink 提供的低阶 API，可以访问 Keyed State、注册定时器（Timer）和访问时间戳，适合实现复杂的有状态事件驱动逻辑。
</details>

### 问题 5

**Side Output 的主要用途是？**

- [ ] A. 增加并行度
- [ ] B. 将不符合条件的数据分流到旁路输出
- [ ] C. 压缩数据
- [ ] D. 加速处理

<details>
<summary>答案与解析</summary>

**答案：B**

Side Output 允许将数据分流到多个输出流，常用于处理迟到数据、异常数据分离等场景。
</details>

---

## 第二部分：SQL/Table API (共5题)

### 问题 6

**Flink SQL 中 TUMBLE 窗口函数的参数包括？**

- [ ] A. TABLE, DESCRIPTOR(timecol), INTERVAL
- [ ] B. TABLE, COLUMN
- [ ] C. START, END
- [ ] D. RANGE, SLIDE

<details>
<summary>答案与解析</summary>

**答案：A**

Flink SQL 中 `TUMBLE(TABLE data, DESCRIPTOR(ts), INTERVAL '10' MINUTES)` 定义滚动窗口，需要表、时间属性列描述符和窗口间隔。
</details>

### 问题 7

**Table API 和 DataStream API 之间的关系是？**

- [ ] A. 完全独立，不能互操作
- [ ] B. Table API 可以转换为 DataStream，反之亦然
- [ ] C. Table API 性能更好
- [ ] D. DataStream API 将被废弃

<details>
<summary>答案与解析</summary>

**答案：B**

Flink 支持 Table API 和 DataStream API 之间的互操作。可以通过 `toDataStream()` 将 Table 转为 DataStream，通过 `fromDataStream()` 将 DataStream 转为 Table。
</details>

### 问题 8

**Flink SQL 中处理更新流的 Changelog 模式包括？**

- [ ] A. INSERT, DELETE
- [ ] B. APPEND, RETRACT, UPSERT
- [ ] C. ADD, REMOVE
- [ ] D. CREATE, DROP

<details>
<summary>答案与解析</summary>

**答案：B**

Flink SQL 支持三种 Changelog 模式：APPEND（仅插入）、RETRACT（回撤更新）、UPSERT（主键更新）。不同模式适用于不同场景。
</details>

### 问题 9

**CREATE TABLE 语句中的 WATERMARK 用于？**

- [ ] A. 加密数据
- [ ] B. 声明 Event Time 属性和乱序延迟
- [ ] C. 压缩数据
- [ ] D. 创建索引

<details>
<summary>答案与解析</summary>

**答案：B**

WATERMARK 声明用于指定哪一列是 Event Time 以及乱序延迟时间，例如：`WATERMARK FOR ts AS ts - INTERVAL '5' SECOND`。
</details>

### 问题 10

**以下哪个不是 Flink SQL 的内置窗口类型？**

- [ ] A. TUMBLE
- [ ] B. HOP
- [ ] C. SESSION
- [ ] D. SLIDING

<details>
<summary>答案与解析</summary>

**答案：D**

Flink SQL 支持 TUMBLE（滚动）、HOP（滑动）、SESSION（会话）和 CUMULATE（累积）窗口。SLIDING 不是 Flink SQL 的标准窗口类型（DataStream API 使用 Sliding）。
</details>

---

## 第三部分：Connectors 与生态 (共5题)

### 问题 11

**Flink Kafka Consumer 中，`setStartFromLatest()` 的含义是？**

- [ ] A. 从最早的消息开始消费
- [ ] B. 从最新的消息开始消费
- [ ] C. 从 Group 提交的 Offset 开始消费
- [ ] D. 从指定时间开始消费

<details>
<summary>答案与解析</summary>

**答案：B**

`setStartFromLatest()` 表示从 Kafka 最新的消息（队尾）开始消费。`setStartFromEarliest()` 从最早开始，`setStartFromGroupOffsets()` 从 Group Offset 开始。
</details>

### 问题 12

**Flink CDC Connectors 的主要用途是？**

- [ ] A. 批量导入数据
- [ ] B. 捕获数据库变更日志
- [ ] C. 压缩数据
- [ ] D. 数据加密

<details>
<summary>答案与解析</summary>

**答案：B**

CDC (Change Data Capture) Connectors 用于捕获数据库的变更日志（INSERT/UPDATE/DELETE），实现实时数据同步。

**参考**: Flink/04-connectors/flink-cdc-3.0-data-integration.md
</details>

### 问题 13

**使用 Flink 写入 Kafka 时，如何实现 Exactly-Once？**

- [ ] A. 使用 at-least-once 模式
- [ ] B. 启用 Kafka 事务和两阶段提交
- [ ] C. 增加并行度
- [ ] D. 减少 Checkpoint 间隔

<details>
<summary>答案与解析</summary>

**答案：B**

FlinkKafkaProducer 支持通过 Kafka 事务实现 Exactly-Once。配置 `Semantic.EXACTLY_ONCE` 并确保事务超时大于 Checkpoint 间隔。

**参考**: [Lab 5: Checkpoint 与恢复](../hands-on-labs/lab-05-checkpoint.md)
</details>

### 问题 14

**Flink 的 Hive Catalog 作用是？**

- [ ] A. 存储 Checkpoint
- [ ] B. 与 Hive Metastore 集成，复用 Hive 表定义
- [ ] C. 压缩数据
- [ ] D. 数据加密

<details>
<summary>答案与解析</summary>

**答案：B**

Hive Catalog 允许 Flink SQL 连接到 Hive Metastore，复用 Hive 的表、分区等元数据，实现与 Hive 生态的无缝集成。
</details>

### 问题 15

**以下哪个 Sink 连接器通常需要实现两阶段提交以保证 Exactly-Once？**

- [ ] A. Print Sink
- [ ] B. FileSystem Sink
- [ ] C. Collection Sink
- [ ] D. 内存 Sink

<details>
<summary>答案与解析</summary>

**答案：B**

FileSystem Sink（如 HDFS、S3）通常需要实现 TwoPhaseCommitSinkFunction，通过预提交和正式提交两个阶段保证 Exactly-Once。
</details>

---

## 第四部分：部署与运维 (共5题)

### 问题 16

**Flink on Kubernetes 部署时，Native 模式的优势是？**

- [ ] A. 配置更简单
- [ ] B. Flink 直接管理 Kubernetes 资源，支持动态扩缩容
- [ ] C. 不需要 Docker 镜像
- [ ] D. 性能更好

<details>
<summary>答案与解析</summary>

**答案：B**

Native Kubernetes 模式让 Flink 直接与 K8s API 交互，动态创建/销毁 TaskManager Pod，支持更灵活的资源管理。

**参考**: Flink/10-deployment/kubernetes-deployment.md
</details>

### 问题 17

**Flink 的 Task Slot 的主要作用是？**

- [ ] A. 限制并发度
- [ ] B. 资源隔离和并行度控制
- [ ] C. 数据分区
- [ ] D. 状态存储

<details>
<summary>答案与解析</summary>

**答案：B**

Task Slot 是 TaskManager 的资源单元，控制并发度和资源隔离。一个 TaskManager 可以有多个 Slot，不同算子可以共享 Slot（如果 Chain 在一起）。
</details>

### 问题 18

**Backpressure 在 Flink 中是指？**

- [ ] A. 网络压力
- [ ] B. 数据从下游向上游传播反压信号
- [ ] C. 磁盘压力
- [ ] D. CPU 压力

<details>
<summary>答案与解析</summary>

**答案：B**

Backpressure（反压）是流处理的流量控制机制。当下游处理速度慢于上游时，反压信号向上游传播，减慢数据源发送速度，防止系统过载。

**参考**: Flink/02-core-mechanisms/backpressure-and-flow-control.md
</details>

### 问题 19

**Flink Web UI 中，Checkpoint 页面的 `End to End Duration` 表示？**

- [ ] A. 作业运行总时间
- [ ] B. 从触发到完成的总时间
- [ ] C. 状态大小
- [ ] D. 失败次数

<details>
<summary>答案与解析</summary>

**答案：B**

End to End Duration 表示从 Checkpoint 触发到所有 Task 确认完成的时间，是衡量 Checkpoint 性能的重要指标。
</details>

### 问题 20

**以下哪个不是 Flink 的 Restart Strategy？**

- [ ] A. fixed-delay
- [ ] B. failure-rate
- [ ] C. exponential-delay
- [ ] D. checkpoint-restart

<details>
<summary>答案与解析</summary>

**答案：D**

Flink 支持 fixed-delay（固定延迟重试）、failure-rate（按失败率重试）、exponential-delay（指数退避）和 no-restart（不重试）策略，没有 checkpoint-restart 策略。
</details>

---

## 成绩统计

| 部分 | 题数 | 正确率 |
|------|------|--------|
| DataStream API | 5 | ___/5 |
| SQL/Table API | 5 | ___/5 |
| Connectors | 5 | ___/5 |
| 部署与运维 | 5 | ___/5 |
| **总计** | **20** | **___/20** |

### 评分标准

- 18-20 分：Flink 专家，可以处理复杂场景
- 15-17 分：熟练开发者，能够独立完成大部分任务
- 12-14 分：初级水平，需要继续实践
- <12 分：建议系统学习 Flink 文档和实验

## 下一步

- [设计模式测验](./design-patterns.md)
- [综合测试](./comprehensive-test.md)
- [编程挑战](../coding-challenges/README.md)
