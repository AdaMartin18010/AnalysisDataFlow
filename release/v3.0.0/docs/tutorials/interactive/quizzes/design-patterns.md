# 设计模式测验

> 所属阶段: 测验 | 前置依赖: [Knowledge/](../../../Knowledge/) 文档 | 预计时间: 30分钟

## 说明

本测验涵盖流计算中的常见设计模式，包括 Lambda 架构、Kappa 架构、事件溯源、CQRS 等。

---

## 第一部分：架构模式 (共5题)

### 问题 1

**Lambda 架构包含哪三层？**

- [ ] A. Input, Process, Output
- [ ] B. Batch Layer, Speed Layer, Serving Layer
- [ ] C. Source, Transform, Sink
- [ ] D. Map, Shuffle, Reduce

<details>
<summary>答案与解析</summary>

**答案：B**

Lambda 架构由 Batch Layer（批处理层，处理全量数据）、Speed Layer（速度层，处理实时增量）和 Serving Layer（服务层，合并结果）组成。

**参考**: Knowledge/stream-processing-architecture/lambda-architecture.md
</details>

### 问题 2

**Kappa 架构相比 Lambda 架构的主要改进是？**

- [ ] A. 增加了更多层
- [ ] B. 统一了批处理和流处理，消除了 Batch Layer
- [ ] C. 使用更多数据库
- [ ] D. 增加了离线处理

<details>
<summary>答案与解析</summary>

**答案：B**

Kappa 架构通过统一的流处理引擎处理实时和离线场景，消除了 Lambda 架构的 Batch Layer，简化了架构复杂性。
</details>

### 问题 3

**事件溯源 (Event Sourcing) 模式的核心思想是？**

- [ ] A. 只存储最终状态
- [ ] B. 存储状态变更事件序列，通过重放重建状态
- [ ] C. 删除历史数据
- [ ] D. 使用缓存提高性能

<details>
<summary>答案与解析</summary>

**答案：B**

事件溯源不存储当前状态，而是存储导致状态变更的所有事件。通过重放事件序列可以重建任意时刻的状态，支持审计和时序查询。
</details>

### 问题 4

**CQRS (命令查询职责分离) 模式的主要目的是？**

- [ ] A. 提高写入速度
- [ ] B. 分离读模型和写模型，各自优化
- [ ] C. 简化代码
- [ ] D. 减少存储

<details>
<summary>答案与解析</summary>

**答案：B**

CQRS 将读操作和写操作分离到不同的模型：写模型优化数据一致性，读模型优化查询性能。常与事件溯源结合使用。
</details>

### 问题 5

**在流处理系统中，Sidecar 模式通常用于？**

- [ ] A. 主数据处理
- [ ] B. 辅助功能如日志收集、监控、配置管理
- [ ] C. 数据存储
- [ ] D. 用户认证

<details>
<summary>答案与解析</summary>

**答案：B**

Sidecar 模式将辅助功能（日志、监控、配置、服务发现等）部署为独立的 Sidecar 容器/进程，与主应用分离，便于独立升级和维护。
</details>

---

## 第二部分：数据处理模式 (共5题)

### 问题 6

**幂等写入 (Idempotent Write) 的主要作用是？**

- [ ] A. 提高写入速度
- [ ] B. 确保重复处理不会产生副作用
- [ ] C. 压缩数据
- [ ] D. 加密数据

<details>
<summary>答案与解析</summary>

**答案：B**

幂等写入确保同一操作执行多次结果相同。在流处理中用于保证 Exactly-Once 语义：即使数据被重复处理，写入结果也不会改变。
</details>

### 问题 7

**Lookup Join 适用于什么场景？**

- [ ] A. 两个大表连接
- [ ] B. 流表与大维表连接，维表更新不频繁
- [ ] C. 实时聚合
- [ ] D. 窗口计算

<details>
<summary>答案与解析</summary>

**答案：B**

Lookup Join 用于将流表与外部维表（如 MySQL、Redis）连接，适用于维表数据量大但更新频率低的场景，避免维表全量加载到内存。
</details>

### 问题 8

**异步 Lookup 的主要优势是？**

- [ ] A. 减少网络请求
- [ ] B. 提高吞吐量，避免单条等待
- [ ] C. 简化代码
- [ ] D. 减少内存使用

<details>
<summary>答案与解析</summary>

**答案：B**

异步 Lookup 允许多个请求并发执行，不阻塞处理流程，显著提高吞吐量。Flink 提供 AsyncFunction 支持异步 IO。
</details>

### 问题 9

**CDC (Change Data Capture) 模式用于解决什么问题？**

- [ ] A. 数据压缩
- [ ] B. 实时捕获数据库变更
- [ ] C. 数据加密
- [ ] D. 批量导入

<details>
<summary>答案与解析</summary>

**答案：B**

CDC 捕获数据库的增量变更（INSERT/UPDATE/DELETE），将变更事件实时同步到其他系统，用于数据同步、缓存更新、事件驱动等场景。
</details>

### 问题 10

**Materialized View 在流处理中的实现方式是？**

- [ ] A. 定期全量刷新
- [ ] B. 基于变更日志增量维护
- [ ] C. 手动更新
- [ ] D. 不更新

<details>
<summary>答案与解析</summary>

**答案：B**

流处理中的物化视图通过持续消费变更日志（Changelog）来增量维护，而不是定期全量刷新，保证低延迟和高效性。

**参考**: Flink/03-sql-table-api/materialized-tables.md
</details>

---

## 第三部分：容错与一致性模式 (共5题)

### 问题 11

**Saga 模式用于解决什么问题？**

- [ ] A. 提高性能
- [ ] B. 分布式长事务管理
- [ ] C. 数据压缩
- [ ] D. 缓存管理

<details>
<summary>答案与解析</summary>

**答案：B**

Saga 模式将长事务拆分为多个本地事务，每个有对应的补偿操作。如果某步失败，执行前面步骤的补偿操作回滚，避免分布式锁和长事务阻塞。
</details>

### 问题 12

**Circuit Breaker (断路器) 模式的作用是？**

- [ ] A. 提高网络速度
- [ ] B. 防止故障级联，快速失败
- [ ] C. 数据加密
- [ ] D. 负载均衡

<details>
<summary>答案与解析</summary>

**答案：B**

断路器在检测到下游服务故障时快速失败，避免请求堆积和资源耗尽，防止故障蔓延。经过冷却期后会尝试恢复。
</details>

### 问题 13

**在流处理中，Dead Letter Queue (DLQ) 用于？**

- [ ] A. 提高吞吐量
- [ ] B. 存储处理失败的消息，避免阻塞主流程
- [ ] C. 数据压缩
- [ ] D. 负载均衡

<details>
<summary>答案与解析</summary>

**答案：B**

DLQ 存储无法正常处理的消息（如格式错误、处理异常），使主流程继续处理其他消息，失败消息可以单独分析、重试或人工处理。
</details>

### 问题 14

**Two-Phase Commit (2PC) 的主要缺点是？**

- [ ] A. 实现简单
- [ ] B. 同步阻塞，性能较低
- [ ] C. 不支持分布式
- [ ] D. 不保证一致性

<details>
<summary>答案与解析</summary>

**答案：B**

2PC 是强一致性协议，但存在同步阻塞、单点故障（协调者）、数据不一致（协调者故障时）等问题，性能较低。
</details>

### 问题 15

**在流处理系统中，Watermark 模式属于？**

- [ ] A. 同步模式
- [ ] B. 乱序数据处理模式
- [ ] C. 加密模式
- [ ] D. 压缩模式

<details>
<summary>答案与解析</summary>

**答案：B**

Watermark 是流处理中处理乱序数据、平衡延迟和准确性的核心模式，通过延迟触发计算来等待迟到数据。
</details>

---

## 第四部分：扩展性与性能模式 (共5题)

### 问题 16

**Partitioning 和 Rebalancing 的区别是？**

- [ ] A. 没有区别
- [ ] B. Partitioning 按 key 分组，Rebalancing 随机重分布
- [ ] C. Partitioning 更快
- [ ] D. Rebalancing 按 key 分组

<details>
<summary>答案与解析</summary>

**答案：B**

Partitioning（keyBy）按 key 的 hash 将数据发送到特定分区，保证相同 key 到同一分区；Rebalance 是轮询随机重分布，用于负载均衡。
</details>

### 问题 17

**Bloom Filter 在流处理中的典型用途是？**

- [ ] A. 精确去重
- [ ] B. 近似去重，节省内存
- [ ] C. 排序
- [ ] D. 聚合

<details>
<summary>答案与解析</summary>

**答案：B**

Bloom Filter 是一种概率数据结构，用于快速判断元素是否可能存在（可能误判存在，但不会误判不存在），适合大规模近似去重场景。
</details>

### 问题 18

**HyperLogLog 算法主要用于？**

- [ ] A. 精确计数
- [ ] B. 基数估计（去重计数），使用固定内存
- [ ] C. 排序
- [ ] D. 分组

<details>
<summary>答案与解析</summary>

**答案：B**

HyperLogLog 是基数估计算法，使用固定的小量内存（通常几KB）估计海量数据的唯一值数量，误差约 0.81%，适用于 UV 统计等场景。
</details>

### 问题 19

**Backpressure 机制属于什么类型的模式？**

- [ ] A. 数据模式
- [ ] B. 流量控制模式
- [ ] C. 存储模式
- [ ] D. 安全模式

<details>
<summary>答案与解析</summary>

**答案：B**

Backpressure 是流系统的流量控制模式，当下游处理不过来时向上游传递压力信号，减慢数据产生速度，防止系统崩溃。
</details>

### 问题 20

**Shard 模式在流处理中的主要目的是？**

- [ ] A. 数据加密
- [ ] B. 水平扩展，将数据分布到多个分区
- [ ] C. 数据压缩
- [ ] D. 负载均衡

<details>
<summary>答案与解析</summary>

**答案：B**

Sharding（分片）将数据分布到多个独立处理单元，实现水平扩展。Kafka 的 Partition、Flink 的 Parallelism 都是 Sharding 的实现。
</details>

---

## 成绩统计

| 部分 | 题数 | 正确率 |
|------|------|--------|
| 架构模式 | 5 | ___/5 |
| 数据处理模式 | 5 | ___/5 |
| 容错与一致性 | 5 | ___/5 |
| 扩展性与性能 | 5 | ___/5 |
| **总计** | **20** | **___/20** |

### 评分标准

- 18-20 分：架构专家，能够设计复杂系统
- 15-17 分：资深开发者，熟练掌握常用模式
- 12-14 分：中级水平，了解基本概念
- <12 分：建议深入学习设计模式相关文档

## 下一步

- [综合测试](./comprehensive-test.md)
- [编程挑战](../coding-challenges/README.md)
