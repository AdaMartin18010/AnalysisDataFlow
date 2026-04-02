# 练习 03: Checkpoint 分析

> 所属阶段: Knowledge | 前置依赖: [Flink/03-fault-tolerance.md](../Flink/03-fault-tolerance.md), [exercise-02](./exercise-02-flink-basics.md) | 形式化等级: L4

---

## 目录

- [练习 03: Checkpoint 分析](#练习-03-checkpoint-分析)
  - [目录](#目录)
  - [1. 学习目标](#1-学习目标)
  - [2. 预备知识](#2-预备知识)
    - [2.1 Checkpoint 核心概念](#21-checkpoint-核心概念)
    - [2.2 关键配置参数](#22-关键配置参数)
  - [3. 练习题](#3-练习题)
    - [3.1 理论题 (40分)](#31-理论题-40分)
      - [题目 3.1: Checkpoint 执行流程 (10分)](#题目-31-checkpoint-执行流程-10分)
      - [题目 3.2: Exactly-Once 语义分析 (10分)](#题目-32-exactly-once-语义分析-10分)
      - [题目 3.3: Checkpoint 失败诊断 (10分)](#题目-33-checkpoint-失败诊断-10分)
      - [题目 3.4: 状态后端对比 (10分)\\n](#题目-34-状态后端对比-10分n)
    - [3.2 编程与分析题 (60分)](#32-编程与分析题-60分)
      - [题目 3.5: Checkpoint 配置优化 (15分)](#题目-35-checkpoint-配置优化-15分)
      - [题目 3.6: Checkpoint 性能分析 (20分)](#题目-36-checkpoint-性能分析-20分)
      - [题目 3.7: 故障恢复测试 (15分)](#题目-37-故障恢复测试-15分)
      - [题目 3.8: 非对齐 Checkpoint 分析 (10分)](#题目-38-非对齐-checkpoint-分析-10分)
  - [4. 参考答案链接](#4-参考答案链接)
  - [5. 评分标准](#5-评分标准)
    - [总分分布](#总分分布)
    - [重点评分项](#重点评分项)
  - [6. 进阶挑战 (Bonus)](#6-进阶挑战-bonus)
  - [7. 参考资源](#7-参考资源)
  - [8. 可视化](#8-可视化)
    - [Checkpoint 执行流程](#checkpoint-执行流程)

## 1. 学习目标

完成本练习后，你将能够：

- **Def-K-03-01**: 深入理解 Checkpoint 的触发机制与执行流程
- **Def-K-03-02**: 掌握 Checkpoint 超时、失败的诊断方法
- **Def-K-03-03**: 能够配置与优化 Checkpoint 参数
- **Def-K-03-04**: 理解 Exactly-Once 语义在 Checkpoint 中的实现

---

## 2. 预备知识

### 2.1 Checkpoint 核心概念

| 概念 | 说明 |
|------|------|
| Checkpoint Barrier | 特殊的记录，用于分隔前后 Checkpoint 的数据 |
| Snapshot | 各算子状态的一致性快照 |
| Checkpoint Coordinator | JobManager 组件，负责协调 Checkpoint |
| State Backend | 状态存储后端（Memory/FS/RocksDB）|
| Incremental Checkpoint | 仅保存增量状态变更 |

### 2.2 关键配置参数

```java
// Checkpoint 配置示例
env.enableCheckpointing(60000);  // 1分钟
env.getCheckpointConfig().setCheckpointingMode(
    CheckpointingMode.EXACTLY_ONCE);
env.getCheckpointConfig().setMinPauseBetweenCheckpoints(30000);
env.getCheckpointConfig().setCheckpointTimeout(600000);
env.getCheckpointConfig().setMaxConcurrentCheckpoints(1);
env.getCheckpointConfig().enableExternalizedCheckpoints(
    ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION);
```

---

## 3. 练习题

### 3.1 理论题 (40分)

#### 题目 3.1: Checkpoint 执行流程 (10分)

**难度**: L4

描述 Flink Checkpoint 的完整执行流程：

1. 从 Checkpoint Coordinator 发起，到完成的完整步骤 (6分)
2. 画出 Barrier 在流中的传播过程 (4分)

**答题要点**：

- 同步阶段与异步阶段的区分
- Barrier 对齐与非对齐的区别
- 状态快照的触发时机

---

#### 题目 3.2: Exactly-Once 语义分析 (10分)

**难度**: L4

分析以下场景下 Exactly-Once 的保障机制：

**场景 A**：使用 Kafka Source + 内存状态 + Print Sink
**场景 B**：使用 Kafka Source + RocksDB + Kafka Sink（两阶段提交）

请回答：

1. 场景 A 能否保证 Exactly-Once？为什么？(4分)
2. 场景 B 的两阶段提交流程是什么？(4分)
3. 如果 Sink 不支持两阶段提交，如何实现端到端 Exactly-Once？(2分)

---

#### 题目 3.3: Checkpoint 失败诊断 (10分)

**难度**: L4

给定以下日志片段：

```
2024-01-15 10:23:45,123 WARN  Checkpoint 123 - expired before completing
2024-01-15 10:23:45,234 INFO  Failed to trigger checkpoint 123
    due to CheckpointExpiredException
2024-01-15 10:24:00,456 WARN  Source: CustomSource -> Map
    back-pressured, buffer usage: 95%
```

请回答：

1. 分析 Checkpoint 失败的根本原因 (4分)
2. 提出至少3种解决方案 (4分)
3. 如何调整参数避免类似问题？(2分)

---

#### 题目 3.4: 状态后端对比 (10分)\n

**难度**: L4

对比三种状态后端：

| 特性 | MemoryStateBackend | FsStateBackend | RocksDBStateBackend |
|------|-------------------|----------------|---------------------|
| 存储位置 | | | |
| 状态大小限制 | | | |
| 增量 Checkpoint | | | |
| 适用场景 | | | |
| 性能特点 | | | |

请补充上表，并针对以下场景推荐合适的 State Backend：

- 小型状态 (< 100MB)，快速恢复
- 大型状态 (> 10GB)，增量备份
- 需要随机读写的 MapState

---

### 3.2 编程与分析题 (60分)

#### 题目 3.5: Checkpoint 配置优化 (15分)

**难度**: L4

给定一个处理大规模 IoT 数据的 Flink 作业，特征如下：

- 10万+ 设备，每个设备有 100 个传感器
- 每秒 100万 条记录
- 需要保存 24 小时的历史状态用于异常检测
- 使用 Kafka Source 和 HBase Sink

**任务**：

1. 选择合适的 State Backend 并说明理由 (3分)
2. 配置 Checkpoint 参数（间隔、超时、并发数等）(6分)
3. 配置增量 Checkpoint 和本地恢复 (3分)
4. 配置 HBase Sink 的 Exactly-Once 写入 (3分)

---

#### 题目 3.6: Checkpoint 性能分析 (20分)

**难度**: L4

使用以下程序生成 Checkpoint 指标数据：

```java
public class CheckpointMetricsJob {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        // 启用 Checkpoint
        env.enableCheckpointing(10000);
        env.getCheckpointConfig().setCheckpointTimeout(60000);

        // TODO: 配置 RocksDB 和增量 Checkpoint

        // 模拟有状态的计算
        env.fromSource(new RateLimitedSource(10000),
                       WatermarkStrategy.noWatermarks(), "source")
           .keyBy(event -> event.sensorId)
           .process(new StatefulProcessFunction())
           .addSink(new DiscardingSink<>());

        env.execute();
    }
}
```

**任务**：

1. 运行程序并收集 Checkpoint 指标（持续时间、大小、对齐时间）(6分)
2. 分析指标数据，找出潜在瓶颈 (7分)
3. 提出并实施优化方案 (7分)

**提交要求**：

- Flink Web UI 截图（Checkpoint 页面）
- 分析报告（包括优化前后的对比）

---

#### 题目 3.7: 故障恢复测试 (15分)

**难度**: L4

**任务**：

1. 编写一个有状态的 Flink 程序（如累加器）(4分)
2. 手动触发 Checkpoint 并保存到指定路径 (3分)
3. 模拟 TaskManager 失败（kill 进程）(3分)
4. 从 Checkpoint 恢复作业，验证状态一致性 (5分)

**参考命令**：

```bash
# 保存 Checkpoint
flink savepoint <jobId> <targetPath>

# 从 Checkpoint 恢复
flink run -s <checkpointPath> <jarFile>
```

---

#### 题目 3.8: 非对齐 Checkpoint 分析 (10分)

**难度**: L5

**背景**：Flink 1.11+ 引入了非对齐 Checkpoint (Unaligned Checkpoint) 机制。

**任务**：

1. 解释非对齐 Checkpoint 的工作原理 (4分)
2. 对比对齐与非对齐 Checkpoint 的优缺点 (3分)
3. 编写配置启用非对齐 Checkpoint (3分)

```java
// TODO: 配置非对齐 Checkpoint
```

---

## 4. 参考答案链接

| 题目 | 答案位置 | 补充说明 |
|------|----------|----------|
| 3.1 | [answers/03-checkpoint.md](./answers/03-checkpoint.md#31) | 含流程图 |
| 3.2 | [answers/03-checkpoint.md](./answers/03-checkpoint.md#32) | 端到端一致性详解 |
| 3.3 | [answers/03-checkpoint.md](./answers/03-checkpoint.md#33) | 诊断决策树 |
| 3.4 | [answers/03-checkpoint.md](./answers/03-checkpoint.md#34) | 后端对比表 |
| 3.5 | [answers/03-code/CheckpointConfig.java](./answers/03-code/CheckpointConfig.java) | 配置示例 |
| 3.6 | [answers/03-code/CheckpointMetricsAnalysis.md](./answers/03-code/CheckpointMetricsAnalysis.md) | 分析模板 |
| 3.7 | [answers/03-code/FaultRecoveryTest.md](./answers/03-code/FaultRecoveryTest.md) | 测试步骤 |
| 3.8 | [answers/03-code/UnalignedCheckpoint.java](./answers/03-code/UnalignedCheckpoint.java) | 配置代码 |

---

## 5. 评分标准

### 总分分布

| 等级 | 分数区间 | 要求 |
|------|----------|------|
| S | 95-100 | 全部分析深入，优化方案有效 |
| A | 85-94 | 理论正确，实验数据完整 |
| B | 70-84 | 主要概念理解，实验基本完成 |
| C | 60-69 | 基本概念掌握 |
| F | <60 | 概念理解有误 |

### 重点评分项

| 题目 | 分值 | 关键评分点 |
|------|------|------------|
| 3.1 | 10 | Barrier 传播过程描述准确 |
| 3.2 | 10 | 端到端一致性理解深入 |
| 3.6 | 20 | 实验数据真实，分析有深度 |
| 3.7 | 15 | 恢复测试成功，状态一致 |

---

## 6. 进阶挑战 (Bonus)

完成以下任一任务可获得额外 10 分：

1. **大规模状态测试**：在 10GB+ 状态下测试 Checkpoint 性能
2. **自定义 State Backend**：实现一个简单的自定义 State Backend
3. **Checkpoint 监控 Dashboard**：使用 Prometheus + Grafana 搭建 Checkpoint 监控面板

---

## 7. 参考资源


---

## 8. 可视化

### Checkpoint 执行流程

```mermaid
sequenceDiagram
    participant JM as JobManager<br/>CheckpointCoordinator
    participant SRC as Source<br/>Task
    participant MAP as Map<br/>Task
    participant SNK as Sink<br/>Task

    JM->>+SRC: Trigger Checkpoint 123
    SRC->>SRC: 保存本地状态
    SRC->>SRC: 向下游广播 Barrier
    SRC-->>-JM: ACK Checkpoint 123

    SRC->>+MAP: Emit Barrier
    MAP->>MAP: Barrier 对齐
    MAP->>MAP: 保存本地状态
    MAP->>MAP: 向下游广播 Barrier
    MAP-->>-JM: ACK Checkpoint 123

    MAP->>+SNK: Emit Barrier
    SNK->>SNK: 保存状态<br/>预提交事务
    SNK-->>-JM: ACK Checkpoint 123

    JM->>JM: 收到所有 ACK
    JM->>JM: 完成 Checkpoint 123
```

---

*最后更新: 2026-04-02*
