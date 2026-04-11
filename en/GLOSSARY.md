# AnalysisDataFlow Glossary

> **Version**: v1.1 | **Last Updated**: 2026-04-11 | **Scope**: Full Project
>
> **Version Annotations**: Terms marked with [2.0], [2.4], [2.5], [3.0] indicate the Flink version where the term was introduced or became a core feature.
>
> This document is the authoritative terminology reference for the AnalysisDataFlow project, arranged alphabetically, covering stream computing theory, Flink engineering practice, and frontier technology domains.

---

## Table of Contents

- [Glossary Navigation](#glossary-navigation)
- [Terminology Category Index](#terminology-category-index)
- [A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [Q](#q) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [W](#w)

---

## Glossary Navigation

| Category | Term Count | Primary Domain |
|----------|------------|----------------|
| [Basic Terms](#1-basic-terms) | 35+ | Stream computing, batch processing, real-time processing |
| [Theoretical Terms](#2-theoretical-terms) | 40+ | Process calculus, formal verification, type theory |
| [Flink Terms](#3-flink-terms) | 50+ | Core concepts, API, configuration parameters |
| [Engineering Terms](#4-engineering-terms) | 30+ | Design patterns, architecture, operations |
| [Frontier Terms](#5-frontier-terms) | 35+ | AI Agent, streaming databases, cloud-native |

---

## Terminology Category Index

### 1. Basic Terms

- **Stream Computing**: Dataflow, Event Time, Processing Time, Watermark, Window
- **Batch Processing**: Batch Processing, Bounded Stream, Checkpoint
- **Real-time Processing**: Real-time Processing, Latency, Throughput

### 2. Theoretical Terms

- **Process Calculus**: CCS, CSP, π-Calculus, Actor Model, Session Types
- **Formal Verification**: Bisimulation, Model Checking, TLA+, Iris
- **Type Theory**: FG/FGG, DOT, Path-Dependent Types

### 3. Flink Terms

- **Core Concepts**: JobManager, TaskManager, Operator, State Backend
- **API Related**: DataStream API, Table API, SQL
- **Configuration**: Parallelism, Checkpoint Interval, Watermark Strategy

### 4. Engineering Terms

- **Design Patterns**: Windowed Aggregation, Async I/O, Side Output
- **Architecture**: Microservices, Event-Driven Architecture, Data Mesh
- **Operations**: Backpressure, Monitoring, Autoscaling

### 5. Frontier Terms

- **AI Agent**: AI Agent, ReAct, MCP, A2A, Agentic Workflow
- **Serverless**: Serverless Flink, Scale-to-Zero, FaaS
- **Streaming Database**: Materialized View, Continuous Query, Incremental Update

---

## A

### Adaptive Execution Engine (自适应执行引擎) [Flink 1.17+]

**Definition**: Flink's intelligent execution optimization framework that dynamically adjusts execution plans, resource allocation, and parallelism based on runtime statistics.

**Formal Definition**:

```
AEE-V2 = (𝒫, ℳ, 𝒜, 𝒞, ℛ, δ, π)
```

Where 𝒫 is the physical execution plan, ℳ is runtime metrics, 𝒜 is adaptive actions, 𝒞 is constraints, ℛ is the re-optimizer, δ is the decision function, and π is the performance prediction model.

**Core Capabilities**: Automatic data skew handling, dynamic parallelism adjustment, adaptive resource allocation

**Related Concepts**: Smart Checkpointing, Backpressure, Parallelism

---

### Actor Model (Actor 模型)

**Definition**: A concurrent computing model where the basic unit of computation is an Actor—an autonomous entity capable of receiving messages, making decisions, creating new Actors, and sending messages.

**Formal Definition**:

```
Actor ::= ⟨Mailbox, Behavior, State, Children, Supervisor⟩
```

**Related Concepts**: CSP, π-Calculus, Message Passing

---

### AI Agent (人工智能代理) [General Term]

**Definition**: An intelligent system capable of autonomously perceiving, reasoning, acting, and learning in an environment, formalized as a 6-tuple:

```
𝒜_agent ≜ ⟨𝒮, 𝒫, 𝒟, 𝒜, ℳ, 𝒢⟩
```

Where 𝒮 is the state space, 𝒫 is perception, 𝒟 is decision-making, 𝒜 is action, ℳ is memory, and 𝒢 is the goal.

**Flink Integration**: Flink Agent is an AI Agent implementation based on the stream computing framework

**Related Concepts**: ReAct, MCP, A2A, Multi-Agent

---

### A2A Protocol (Agent-to-Agent Protocol) [Google 2025]

**定义**: Google 提出的开放 Agent 互操作标准，支持 Agent 间的任务委托、状态同步和结果返回。

**形式化定义**:

```
A2A_Flink = ⟨𝒫, ℳ, 𝒮, 𝒜⟩
```

其中 𝒫 为参与 Agent 集合，ℳ 为消息类型，𝒮 为会话状态机，𝒜 为认证授权机制。

**Task State Flow**: `pending → working → input-required → completed/failed`

**Related Concepts**: AI Agent, MCP, Orchestration

---

### Apache Flink (Apache Flink)

**Definition**: An open-source stream processing framework with powerful stateful stream processing capabilities, supporting both batch and stream processing with exactly-once semantics.

**Key Features**:

- Event time processing with Watermarks
- Stateful stream processing
- Exactly-once consistency guarantees
- High throughput and low latency

---

## B

### Backpressure (背压 / 反压)

**Definition**: A flow control mechanism where downstream operators slow down consumption when they cannot keep up with upstream production, propagating back through the pipeline.

**Formal Definition**:

```
Backpressure(O_downstream, O_upstream) ≡
  rate(O_upstream) > processing_rate(O_downstream)
  → throttle(O_upstream)
```

**Related Concepts**: Flow Control, Credit-based Flow Control

---

### Batch Processing (批处理)

**定义**: 对有限数据集进行的离线计算，数据边界明确、计算完成即结束。

**Formal Definition**:

```
Batch(D, f) = ⋃_{d ∈ D} f(d)  where |D| < ∞
```

**Comparison with Stream Processing**:

| Aspect | Batch Processing | Stream Processing |
|--------|------------------|-------------------|
| Data Boundary | Bounded | Unbounded |
| Latency | Minutes to hours | Milliseconds to seconds |
| Throughput | Very high | High |
| Use Case | Historical analysis | Real-time analytics |

---

### Bounded Stream (有界流)

**定义**: 具有明确开始和结束的数据流，批处理是有界流的特例。

**Related Concepts**: Unbounded Stream, Stream Processing

---

### Bisimulation (互模拟)

**Definition**: A binary relation between process calculus systems where two systems can simulate each other's behavior, used to prove behavioral equivalence.

**Related Concepts**: Process Calculus, Behavioral Equivalence

---

## C

### CCS (Calculus of Communicating Systems / 通信系统演算)

**定义**: Robin Milner 提出的进程演算，用于描述并发系统的通信行为。

**Syntax**:

```
P, Q ::= 0 | α.P | P + Q | P | Q | (νx)P | !P
α ::= x(y) | x̄⟨y⟩ | τ
```

**Related Concepts**: CSP, π-Calculus, Process Algebra

---

### Checkpoint (检查点)

**定义**: Flink 的分布式快照机制，用于故障恢复和状态一致性保证。

**Formal Definition**:

```
Checkpoint(G, t) = ⋃_{v ∈ V} State(v, t)  where G = (V, E)
```

**Related Concepts**: State Backend, Exactly-Once, Savepoint

---

### Choreographic Programming (编舞式编程)

**定义**: 一种分布式编程范式，强调参与者之间的交互协议而非集中式编排。

**Related Concepts**: Orchestration, Session Types

---

### Cloud-Native (云原生)

**定义**: 基于容器化、微服务、动态编排的现代化应用开发与部署方式。

**Flink Integration**: Kubernetes Operator, Serverless Flink

---

### Consistency (一致性)

**定义**: 分布式系统中多个副本或参与者对数据状态达成一致的性质。

**Levels**:

- **At-Most-Once**: Messages may be lost
- **At-Least-Once**: No loss, possible duplicates
- **Exactly-Once**: No loss, no duplicates

---

### CSP (Communicating Sequential Processes / 通信顺序进程)

**定义**: Tony Hoare 提出的进程演算，强调通过通道进行同步通信。

**Syntax**:

```
P ::= STOP | SKIP | a → P | P ⊓ Q | P □ Q | P ||| Q | P |[X]| Q
```

**Related Concepts**: CCS, π-Calculus, Channel-based Communication

---

## D

### Dataflow Model (数据流模型)

**定义**: Google 提出的统一批流处理模型，基于事件时间和窗口的抽象。

**Formal Definition**:

```
Dataflow = ⟨Input, Transformations, Windows, Triggers, Watermarks, Accumulation⟩
```

**Reference**: T. Akidau et al., "The Dataflow Model", PVLDB, 2015

---

### Determinism (确定性)

**定义**: 给定相同输入，系统总是产生相同输出的性质。

**In Stream Processing**: Requires event time semantics and ordered processing

---

### Distributed Snapshot (分布式快照)

**定义**: 在分布式系统中捕获全局一致状态的机制，Flink 使用 Chandy-Lamport 算法。

**Related Concepts**: Checkpoint, Global Consistency

---

## E

### Event Time (事件时间)

**定义**: 数据记录实际发生的时间，由数据本身携带的时间戳。

**Comparison**:

| Time Type | Definition | Use Case |
|-----------|------------|----------|
| Event Time | When event occurred | Correctness-critical applications |
| Processing Time | When event is processed | Low-latency, approximate results |
| Ingestion Time | When event enters system | Ordering guarantees |

---

### Exactly-Once (精确一次)

**定义**: 消息处理语义保证每条记录被处理且仅被处理一次，无丢失无重复。

**Formal Definition**:

```
Exactly-Once(f, D) = ∀d ∈ D: count(processed(f(d))) = 1
```

**Flink Implementation**: Distributed snapshots (Checkpoints) + Transactional sinks

---

### Execution Graph (执行图)

**定义**: Flink 作业的逻辑执行计划，包含算子、数据流和分区信息。

**Hierarchy**:

1. **StreamGraph**: User API level
2. **JobGraph**: Optimized logical graph
3. **ExecutionGraph**: Physical execution plan

---

## F

### Fault Tolerance (容错)

**定义**: 系统在部分组件失败时仍能继续正确运行的能力。

**Flink Mechanisms**:

- Checkpointing for state recovery
- Automatic job restart
- Savepoint for manual recovery

---

### Flink JobManager (Flink 作业管理器)

**定义**: Flink 集群的主节点，负责协调分布式执行、调度任务、管理检查点。

**Components**:

- Dispatcher: Job submission
- JobMaster: Job execution coordination
- ResourceManager: Resource allocation

---

### Flink TaskManager (Flink 任务管理器)

**定义**: Flink 集群的工作节点，负责执行具体任务、管理本地状态。

**Key Resources**:

- Task Slots: Units of parallelism
- Memory: Network, managed, and heap
- State Backends: Local state storage

---

### FLIP (Flink Improvement Proposal / Flink 改进提案)

**定义**: Flink 社区的功能设计和改进提案流程，类似于 Python 的 PEP。

**Notable FLIPs**:

- FLIP-27: Refactored Source Interface
- FLIP-147: Support SQL Windowing Table-Valued Functions
- FLIP-531: Flink AI Agents

---

### Flow Control (流控)

**定义**: 调节数据在生产者和消费者之间流动速率的机制。

**Types**:

- Backpressure-based
- Credit-based
- Rate limiting

---

## G

### Global Consistency (全局一致性)

**定义**: 分布式系统中所有节点对共享状态达成一致的性质。

**Flink Guarantees**: Checkpoints provide global consistency snapshots

---

## H

### High Availability (高可用性)

**定义**: 系统在面对故障时保持可用状态的能力。

**Flink Implementation**: Multiple JobManagers with leader election

---

## I

### Incremental Checkpoint (增量检查点)

**定义**: 仅持久化自上次检查点以来发生变化的状态，减少 I/O 开销。

**Related Concepts**: Full Checkpoint, RocksDB State Backend

---

### Ingestion Time (摄入时间)

**定义**: 数据记录进入 Flink 系统的时间，由 Source 算子附加时间戳。

**Related Concepts**: Event Time, Processing Time

---

## J

### Job Graph (作业图)

**定义**: Flink 的优化逻辑执行图，由客户端生成并提交给 JobManager。

**Related Concepts**: StreamGraph, ExecutionGraph

---

### JSON (JavaScript Object Notation)

**定义**: 轻量级数据交换格式，常用于配置和事件序列化。

**Flink Usage**: JSON format support in Table API/SQL

---

## K

### Kafka (Apache Kafka)

**定义**: 分布式流处理平台，常用于 Flink 的数据源和数据汇。

**Flink Integration**: Kafka Connector with exactly-once semantics

---

### KeyBy (按键分区)

**定义**: Flink 的算子，按指定键将数据分区到相同并行实例。

```java
stream.keyBy(event -> event.getUserId())
      .window(TumblingEventTimeWindows.of(Time.minutes(5)))
      .aggregate(new CountAggregate());
```

---

### Kubernetes (Kubernetes / K8s)

**定义**: 容器编排平台，Flink 2.0+ 的主要部署目标。

**Flink Integration**: Flink Kubernetes Operator

---

## L

### Latency (延迟)

**定义**: 从事件发生到结果被处理的时间间隔。

**Types**:

- Processing latency
- End-to-end latency
- Watermark latency

---

### Late Data (延迟数据)

**定义**: 在 Watermark 已经超过其时间戳后才到达的数据。

**Handling Strategies**:

- Drop
- Update results (allowed lateness)
- Side output

---

### Local Recovery (本地恢复)

**定义**: 从 TaskManager 本地磁盘恢复状态，减少网络传输。

**Related Concepts**: Incremental Checkpoint, State Backend

---

## M

### Managed State (托管状态)

**定义**: Flink 自动管理的状态，包括 ValueState, ListState, MapState, ReducingState.

**Example**:

```java
ValueStateDescriptor<Long> descriptor =
    new ValueStateDescriptor<>("counter", Types.LONG);
ValueState<Long> counter = getRuntimeContext().getState(descriptor);
```

---

### Materialized View (物化视图)

**定义**: 预先计算并存储的查询结果，流数据库中持续更新的视图。

**Related Concepts**: Continuous Query, Streaming Database

---

### MCP (Model Context Protocol / 模型上下文协议) [Anthropic 2024]

**定义**: Anthropic 提出的标准化协议，用于 AI 模型与外部工具、数据源之间的安全通信。

**Flink Integration**: Streaming data source for AI Agents

---

### Metric (指标)

**定义**: 用于监控和观测系统行为的量化数据。

**Flink Metrics**: Latency, throughput, checkpoint duration, backpressure

---n

## N

### Non-Determinism (非确定性)

**定义**: 相同输入可能产生不同输出的系统行为。

**Sources**: Network delays, scheduling, out-of-order events

---

## O

### Observability (可观测性)

**定义**: 通过指标、日志、追踪了解系统内部状态的能力。

**Pillars**: Metrics, Logging, Tracing

**Flink Tools**: Web UI, Prometheus, OpenTelemetry

---

### Operator (算子)

**定义**: Flink 数据处理的基本单元，对数据流执行变换。

**Types**:

- Source: Data input
- Transformation: Map, Filter, KeyBy, Window
- Sink: Data output

---

### Orchestration (编排)

**定义**: 集中式协调多个服务或任务执行的架构模式。

**Comparison with Choreography**:

| Orchestration | Choreography |
|---------------|--------------|
| Central coordinator | Decentralized |
| Clear control flow | Emergent behavior |
| Easier to debug | More flexible |

---

## P

### Parallelism (并行度)

**定义**: Flink 算子同时执行的实例数量。

**Configuration**:

```java
env.setParallelism(4);  // Global parallelism
operator.setParallelism(8);  // Operator-specific
```

---

### π-Calculus (π 演算)

**定义**: Robin Milner 提出的进程演算，支持动态通道创建和通信。

**Syntax**:

```
P, Q ::= 0 | α.P | P + Q | P | Q | (νx)P | !P
α ::= x(y) | x̄⟨y⟩ | τ
```

**Related Concepts**: CCS, CSP, Mobility

---

### Processing Time (处理时间)

**定义**: 算子执行处理时机器的本地系统时间。

**Characteristics**: Simple, low latency, non-deterministic

---

## Q

### Query (查询)

**定义**: 从数据源检索或计算信息的请求。

**Flink SQL**: Continuous SQL queries on streaming data

---

## R

### Real-time Processing (实时处理)

**定义**: 数据到达后立即或短时间内完成处理的计算模式。

**Types**:

- Hard real-time: Strict deadlines
- Soft real-time: Best effort

---

### ReAct (Reasoning and Acting / 推理与行动) [General Term]

**定义**: AI Agent 的循环决策模式，交替进行推理和行动。

```
ReAct Loop: Thought → Action → Observation → ...
```

**Related Concepts**: AI Agent, Tool Calling

---

### RocksDB State Backend (RocksDB 状态后端)

**定义**: 基于 RocksDB 的嵌入式键值存储状态后端，支持大状态。

**Configuration**:

```java
env.setStateBackend(new EmbeddedRocksDBStateBackend());
env.getCheckpointConfig().setCheckpointStorage("hdfs:///checkpoints");
```

---

## S

### Savepoint (保存点)

**定义**: 用户触发的手动检查点，用于升级、迁移或备份。

**Difference from Checkpoint**:

| Checkpoint | Savepoint |
|------------|-----------|
| Automatic | Manual |
| Internal use | User-managed |
| May be incremental | Always full |

---

### Session Window (会话窗口)

**定义**: 根据活动间隙动态定义的窗口，用于用户会话分析。

```java
stream.keyBy(Event::getUserId)
      .window(EventTimeSessionWindows.withDynamicGap(...))
      .aggregate(...);
```

---

### Side Output (侧输出)

**定义**: 从主数据流中分离特定数据的分流机制。

**Use Cases**: Late data, error handling, monitoring

---

### Sink (数据汇)

**定义**: 数据流的输出端，将处理结果写入外部系统。

**Examples**: Kafka Sink, JDBC Sink, File Sink, Elasticsearch Sink

---

### Slot (任务槽)

**定义**: TaskManager 中资源分配的基本单位。

**Sharing**: Multiple operators can share a slot if resource-compatible

---

### Source (数据源)

**定义**: 数据流的输入端，从外部系统读取数据。

**Examples**: Kafka Source, File Source, Socket Source, CDC Source

---

### State Backend (状态后端)

**定义**: 负责存储和管理算子状态的组件。

**Types**:

- HashMapStateBackend: In-memory, fast
- EmbeddedRocksDBStateBackend: Disk-based, large state

---

### Stream Processing (流处理)

**定义**: 对无界数据流进行连续、实时的计算。

**Formal Definition**:

```
Stream(f) = lim_{t→∞} ⋃_{i=0}^{t} f(d_i)  where d_i arrives continuously
```

---

### Structured Streaming (结构化流)

**定义**: Apache Spark 的流处理引擎，使用微批处理模型。

**Flink Comparison**: Flink uses native streaming, lower latency

---

## T

### Task (任务)

**定义**: 算子的具体执行实例，在 TaskManager 的 Slot 中运行。

**Relationship**: Job → Task → Subtask

---

### Throughput (吞吐量)

**定义**: 系统单位时间内处理的数据量。

**Measurement**: Records/second, MB/second

---

### Time Window (时间窗口)

**定义**: 基于时间维度定义的数据分组，如滚动窗口、滑动窗口。

**Types**:

- Tumbling Window: Fixed size, no overlap
- Sliding Window: Fixed size, with overlap
- Session Window: Dynamic gap-based

---

### Trigger (触发器)

**定义**: 决定窗口何时计算并输出结果的策略。

**Built-in Triggers**: Event time, processing time, count-based

---

### Tumbling Window (滚动窗口)

**定义**: 固定大小、不重叠、连续排列的时间窗口。

```java
stream.window(TumblingEventTimeWindows.of(Time.minutes(5)))
```

---

## U

### Unbounded Stream (无界流)

**定义**: 没有明确结束的数据流，持续产生数据。

**Characteristics**: Continuous, infinite, real-time

**Related Concepts**: Bounded Stream, Stream Processing

---

### USTM (Unified Streaming Theory Model / 统一流计算理论模型)

**定义**: AnalysisDataFlow 提出的统一流计算形式化理论框架。

**Components**:

- Stream Representation
- Time Semantics
- Consistency Levels
- Expressiveness Hierarchy

---

## V

### Vector Search (向量搜索)

**定义**: 在高维向量空间中寻找相似向量的技术，用于 RAG 等 AI 应用。

**Flink Integration**: Streaming vector index updates

---

## W

### Watermark (水位线)

**定义**: 表示事件时间进度的特殊时间戳，用于处理乱序数据。

**Formal Definition**:

```
Watermark(t) ≡ ∀e ∈ Stream: timestamp(e) ≤ t → e has arrived
```

**Types**:

- Periodic Watermarks
- Punctuated Watermarks

---

### Window (窗口)

**定义**: 将无界流切分为有限数据集进行计算的抽象。

**Window Types**:

| Type | Characteristics |
|------|-----------------|
| Tumbling | Fixed size, no overlap |
| Sliding | Fixed size, with overlap |
| Session | Dynamic, activity-based |
| Global | Single window for all data |

---

### Window Function (窗口函数)

**定义**: 对窗口内数据进行聚合计算的函数。

**Types**: ReduceFunction, AggregateFunction, ProcessWindowFunction

---

## References
