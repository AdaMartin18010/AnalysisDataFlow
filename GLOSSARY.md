# AnalysisDataFlow 术语表 (Glossary)

> **版本**: v1.1 | **更新日期**: 2026-04-04 | **范围**: 全项目
>
> **版本标注说明**: 术语后标注 [2.0]、[2.4]、[2.5]、[3.0] 等表示该术语在 Flink 对应版本中引入或成为核心特性
>
> 本文档是 AnalysisDataFlow 项目的权威术语参考，按字母顺序排列，涵盖流计算理论、Flink 工程实践及前沿技术领域。

---

## 目录

- [术语表导航](#术语表导航)
- [术语分类索引](#术语分类索引)
- [A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [Q](#q) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [W](#w) · [X](#adaptive-execution-engine-自适应执行引擎-flink-117) · [Y](#analysisdataflow-术语表-glossary) · [Z](#materialized-view-物化视图)

---

## 术语表导航

| 分类 | 术语数量 | 主要领域 |
|------|----------|----------|
| [基础术语](#1-基础术语) | 35+ | 流计算、批处理、实时处理 |
| [理论术语](#2-理论术语) | 40+ | 进程演算、形式化验证、类型理论 |
| [Flink术语](#3-flink术语) | 50+ | 核心概念、API、配置参数 |
| [工程术语](#4-工程术语) | 30+ | 设计模式、架构、运维 |
| [前沿术语](#5-前沿术语) | 35+ | AI Agent、流数据库、云原生 |

---

## 术语分类索引

### 1. 基础术语

- [流计算相关](#1-基础术语): Dataflow, Event Time, Processing Time, Watermark, Window
- [批处理相关](#1-基础术语): Batch Processing, Bounded Stream, Checkpoint
- [实时处理相关](#1-基础术语): Real-time Processing, Latency, Throughput

### 2. 理论术语

- [进程演算术语](#2-理论术语): CCS, CSP, π-Calculus, Actor Model, Session Types
- [形式化验证术语](#2-理论术语): Bisimulation, Model Checking, TLA+, Iris
- [类型理论术语](#2-理论术语): FG/FGG, DOT, Path-Dependent Types

### 3. Flink术语

- [核心概念](#3-flink术语): JobManager, TaskManager, Operator, State Backend
- [API相关](#a): DataStream API, Table API, SQL
- [配置参数](#3-flink术语): Parallelism, Checkpoint Interval, Watermark Strategy

### 4. 工程术语

- [设计模式术语](#4-工程术语): Windowed Aggregation, Async I/O, Side Output
- [架构术语](#4-工程术语): Microservices, Event-Driven Architecture, Data Mesh
- [运维术语](#4-工程术语): Backpressure, Monitoring, Autoscaling

### 5. 前沿术语

- [AI Agent术语](#a): AI Agent, ReAct, MCP, A2A, Agentic Workflow, FLIP-531, Tool Calling
- [Serverless术语](#e): Serverless Flink, Scale-to-Zero, FaaS
- [性能优化术语](#5-前沿术语): Adaptive Execution Engine, Smart Checkpointing, GPU Acceleration
- [流批一体术语](#5-前沿术语): Stream-Batch Unification, Unified Execution Engine
- [WASM术语](#a): WebAssembly UDF, WASI, WASM
- [流数据库术语](#5-前沿术语): Materialized View, Continuous Query, Incremental Update
- [云原生术语](#5-前沿术语): Kubernetes, Serverless, WASM, Lakehouse

---

## A

### Adaptive Execution Engine (自适应执行引擎) [Flink 1.17+]

**定义**: Flink 引入的智能执行优化框架，能够根据运行时统计信息动态调整执行计划、资源分配和并行度。

**形式化定义**:

```
AEE-V2 = (𝒫, ℳ, 𝒜, 𝒞, ℛ, δ, π)
```

其中 𝒫 为物理执行计划，ℳ 为运行时指标，𝒜 为自适应动作，𝒞 为约束条件，ℛ 为重优化器，δ 为决策函数，π 为性能预测模型。

**核心能力**: 数据倾斜自动处理、并行度动态调整、资源自适应分配

**相关概念**: [Smart Checkpointing](#a), [Backpressure](#backpressure-反压), [Parallelism](#parallelism-并行度)

**参考文档**:

- `Flink/02-core/adaptive-execution-engine-v2.md` (Def-F-02-87, Thm-F-02-56)

---

### Actor Model (Actor 模型)

**定义**: 一种并发计算模型，其中计算的基本单元是 Actor——能够接收消息、做出决策、创建新 Actor 和发送消息的自治实体。

**形式化定义**:

```
Actor ::= ⟨Mailbox, Behavior, State, Children, Supervisor⟩
```

**相关概念**: [CSP](#csp-communicating-sequential-processes), [π-Calculus](#a), [消息传递](#a)

**参考文档**:

- `Struct/01-foundation/01.03-actor-model-formalization.md` (Def-S-03-01)
- `Struct/03-relationships/03.01-actor-to-csp-encoding.md`

---

### AI Agent (人工智能代理) [通用术语]

**定义**: 能够在环境中自主感知、推理、行动和学习的智能系统，形式化为六元组：

```
𝒜_agent ≜ ⟨𝒮, 𝒫, 𝒟, 𝒜, ℳ, 𝒢⟩
```

其中 𝒮 为状态空间，𝒫 为感知，𝒟 为决策，𝒜 为行动，ℳ 为记忆，𝒢 为目标。

**Flink 集成**: [Flink Agent](#a) 是基于流计算框架的 AI Agent 实现

**相关概念**: [ReAct](#a), [MCP](#c), [A2A](#a), [Multi-Agent](#a), [FLIP-531](#f)

**参考文档**:

- `Knowledge/06-frontier/ai-agent-streaming-architecture.md` (Def-K-06-110)
- `Flink/12-ai-ml/flink-agents-flip-531.md` (Def-F-12-30)

---

### A2A Protocol (Agent-to-Agent Protocol) [Google 2025]

**定义**: Google 提出的开放 Agent 互操作标准，支持 Agent 间的任务委托、状态同步和结果返回。

**形式化定义**:

```
A2A_Flink = ⟨𝒫, ℳ, 𝒮, 𝒜⟩
```

其中 𝒫 为参与 Agent 集合，ℳ 为消息类型，𝒮 为会话状态机，𝒜 为认证授权机制。

**任务状态流转**: `pending → working → input-required → completed/failed`

**相关概念**: [AI Agent](#a), [MCP](#c), [Orchestration](#a), [FLIP-531](#f)

**参考文档**:

- `Flink/12-ai-ml/flink-agents-flip-531.md` (Def-F-12-33)
- `Knowledge/06-frontier/a2a-protocol-agent-communication.md`

---

### Aligned Checkpoint (对齐 Checkpoint)

**定义**: Flink 中算子在收到**所有**输入通道的 Barrier 后才触发状态快照的机制。

**形式化定义**:

```
AlignedSnapshot(t, n) ⟺ ∀c ∈ Inputs(t): Barrier(n) ∈ Received(c)
```

**相关概念**: [Unaligned Checkpoint](#a), [Barrier](#a), [Exactly-Once](#a)

**参考文档**:

- `Flink/02-core/checkpoint-mechanism-deep-dive.md` (Def-F-02-03)
- `Struct/04-proofs/04.01-flink-checkpoint-correctness.md` (Thm-S-17-01)

---

### Async I/O (异步 I/O)

**定义**: 允许流处理算子并发执行外部系统调用的模式，避免阻塞数据流处理。

**形式化定义**:

```
AsyncFunction: I × C → Future[O]
```

其中 C 为并发度参数，控制同时进行的异步请求数量。

**相关概念**: [Backpressure](#a), [Enrichment](#a), [Concurrency](#c)

**参考文档**:

- `Knowledge/02-design-patterns/pattern-async-io-enrichment.md`
- `Flink/02-core/async-execution-model.md`

---

### At-Least-Once (至少一次语义)

**定义**: 流计算系统保证每条输入数据对最终外部世界的影响**至少有一次**的语义。

**形式化定义**:

```
∀r ∈ I. c(r, 𝒯) ≥ 1
```

其中 c(r, 𝒯) 为因果影响计数。

**相关概念**: [At-Most-Once](#a), [Exactly-Once](#a), [Delivery Guarantee](#a)

**参考文档**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-03)

---

### At-Most-Once (至多一次语义)

**定义**: 流计算系统保证每条输入数据对最终外部世界的影响**最多只有一次**的语义，允许数据丢失。

**形式化定义**:

```
∀r ∈ I. c(r, 𝒯) ≤ 1
```

**相关概念**: [At-Least-Once](#a), [Exactly-Once](#a), [Best-Effort](#b)

**参考文档**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-02)

---

## B

### Backpressure (反压)

**定义**: 流处理系统中下游处理速度低于上游时，向上游传递的流速控制信号机制。

**原理**: 基于信用值(credit-based)的流量控制，当接收缓冲区满时暂停发送。

**相关概念**: [Flow Control](#c), [Buffer](#b), [Credit-Based](#a)

**参考文档**:

- `Flink/02-core/backpressure-and-flow-control.md`
- `Knowledge/09-anti-patterns/anti-pattern-08-ignoring-backpressure.md`

---

### Barrier (Checkpoint Barrier)

**定义**: Flink 中注入到数据流中的特殊控制事件，用于分隔不同 Checkpoint 的数据边界。

**形式化定义**:

```
Barrier(n) = ⟨Type = CONTROL, checkpointId = n, timestamp = ts⟩
```

**相关概念**: [Checkpoint](#aligned-checkpoint-对齐-checkpoint), [Aligned Checkpoint](#a), [Unaligned Checkpoint](#a)

**参考文档**:

- `Flink/02-core/checkpoint-mechanism-deep-dive.md` (Def-F-02-02)

---

### Batch Processing (批处理)

**定义**: 处理有限、有界数据集的计算模式，数据在计算开始前已完全可用。

**特征**:

- 输入数据有界(Bounded)
- 可访问完整数据集
- 延迟不敏感，追求高吞吐

**相关概念**: [Stream Processing](#a), [Bounded Stream](#a), [Lambda Architecture](#a)

**参考文档**:

- `Struct/01-foundation/01.04-dataflow-model-formalization.md`

---

### Best-Effort (尽力而为)

**定义**: 不提供任何一致性保证的交付语义，系统尽力处理数据但不保证不丢失、不重复。

**相关概念**: [At-Most-Once](#a), [Delivery Guarantee](#a)

---

### Bisimulation (互模拟)

**定义**: 进程代数中判断两个进程行为等价的关系，要求两个进程在所有可能的动作上都能相互模拟。

**形式化定义**:

```
R 是互模拟 ⟺ ∀(P,Q)∈R. ∀α. P→αP' ⇒ ∃Q'. Q→αQ' ∧ (P',Q')∈R
```

**相关概念**: [Process Calculus](#a), [Trace Equivalence](#a), [CCS](#c)

**参考文档**:

- `Struct/03-relationships/03.04-bisimulation-equivalences.md` (Thm-S-15-01)

---

### Bounded Stream (有界流)

**定义**: 具有有限数据量的数据流，批处理的数据抽象。

**形式化定义**:

```
Bounded(S) ⟺ |S| < ∞
```

**相关概念**: [Unbounded Stream](#a), [Batch Processing](#a)

---

### Buffer (缓冲区)

**定义**: 流处理中用于临时存储数据的内存区域，位于生产者和消费者之间。

**相关概念**: [Backpressure](#a), [Queue](#e), [Network Buffer](#b)

---

## C

### CALM Theorem (CALM 定理)

**定义**: Consistency As Logical Monotonicity —— 逻辑单调的程序无需协调即可保证一致性。

**形式化表述**:

```
程序 P 无需协调 ⟺ P 是逻辑单调的
```

**相关概念**: [Eventual Consistency](#a), [Coordination](#a)

**参考文档**:

- `Struct/02-properties/02.06-calm-theorem.md` (Thm-S-02-08)

---

### Causal Consistency (因果一致性)

**定义**: 分布式系统中保留因果依赖关系操作顺序的一致性模型。

**形式化定义**:

```
∀op_i, op_j. op_i ≺hb op_j ⇒ op_i ≺obs op_j
```

**相关概念**: [Strong Consistency](#c), [Eventual Consistency](#a), [Happens-Before](#a)

**参考文档**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-08)

---

### CEP (Complex Event Processing, 复杂事件处理)

**定义**: 从事件流中检测复杂模式并生成复合事件的技术。

**形式化定义**:

```
CEP: Stream × Pattern → DetectedEvents
```

**相关概念**: [Pattern Matching](#a), [Event Pattern](#a), [Window](#d)

**参考文档**:

- `Knowledge/02-design-patterns/pattern-cep-complex-event.md`

---

### CCS (Calculus of Communicating Systems)

**定义**: Milner 于 1980 年提出的基于标签化同步的进程代数。

**语法**:

```
P, Q ::= 0 | α.P | P + Q | P | Q | P \\ L | P[f]
```

**相关概念**: [CSP](#c), [π-Calculus](#a), [Process Algebra](#a)

**参考文档**:

- `Struct/01-foundation/01.02-process-calculus-primer.md` (Def-S-02-01)

---

### CDC (Change Data Capture, 变更数据捕获)

**定义**: 捕获数据库变更事件（插入、更新、删除）并实时传播到下游系统的技术。

**相关概念**: [Debezium](#b), [Streaming ETL](#a), [Log Mining](#g)

**参考文档**:

- `Flink/04-connectors/flink-cdc-3.0-data-integration.md`
- `Flink/04-connectors/04.04-cdc-debezium-integration.md`

---

### Checkpoint (检查点)

**定义**: 分布式流处理作业在某一时刻的全局一致状态快照，用于故障恢复。

**形式化定义**:

```
CP = ⟨ID, TS, {S_i}_{i∈Tasks}, Metadata⟩
```

**相关概念**: [Savepoint](#a), [State Backend](#a), [Recovery](#c)

**参考文档**:

- `Flink/02-core/checkpoint-mechanism-deep-dive.md` (Def-F-02-01)
- `Struct/04-proofs/04.01-flink-checkpoint-correctness.md` (Thm-S-17-01)

---

### Chandy-Lamport Algorithm

**定义**: 分布式系统中用于捕获全局一致快照的经典算法，Flink Checkpoint 的理论基础。

**相关概念**: [Global Snapshot](#a), [Consistent Cut](#c), [Checkpoint](#aligned-checkpoint-对齐-checkpoint)

**参考文档**:

- `Struct/04-proofs/04.03-chandy-lamport-consistency.md` (Thm-S-19-01)

---

### Choreographic Programming (编舞式编程)

**定义**: 一种分布式编程范式，从全局视角描述多方交互协议，然后投影到各参与方。

**相关概念**: [Session Types](#e), [Endpoint Projection](#c), [Deadlock Freedom](#a)

**参考文档**:

- `Struct/06-frontier/06.02-choreographic-streaming-programming.md`
- `Struct/04-proofs/04.07-deadlock-freedom-choreographic.md` (Thm-S-23-01)

---

### Cloud-Native (云原生)

**定义**: 利用云计算优势构建和运行应用程序的方法论，强调容器化、微服务、持续交付和 DevOps。

**相关概念**: [Kubernetes](#kubernetes), [Containerization](#a), [Microservices](#c)

**参考文档**:

- `Flink/10-deployment/flink-kubernetes-operator-deep-dive.md`
- `Knowledge/06-frontier/serverless-stream-processing-architecture.md`

---

### Concurrency (并发)

**定义**: 多个计算任务在重叠时间段内执行的能力，区别于并行(Parallelism)。

**相关概念**: [Parallelism](#a), [Race Condition](#a), [Synchronization](#a)

---

### Consistency Model (一致性模型)

**定义**: 定义分布式系统中数据操作可见性和顺序性的规则集合。

**层次结构**: Strong Consistency → Causal Consistency → Eventual Consistency

**相关概念**: [Linearizability](#a), [Serializability](#a), [CAP Theorem](#a)

**参考文档**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Thm-S-08-03)

---

### Continuous Query (持续查询)

**定义**: 流数据库中持续运行、随数据到达自动更新结果的查询。

**形式化定义**:

```
q: S → 𝒱, 其中 q 是时变函数
```

**相关概念**: [Materialized View](#a), [Streaming Database](#a)

**参考文档**:

- `Knowledge/06-frontier/streaming-databases.md` (Def-K-06-14)

---

### Coordination (协调)

**定义**: 分布式系统中各节点之间为实现一致行为而进行的通信和同步。

**相关概念**: [CALM Theorem](#a), [Consensus](#c), [Distributed Transaction](#a)

---

### Credit-Based Flow Control (基于信用的流控)

**定义**: 接收方通过发送信用值(credit)告知发送方可接收的数据量，实现流量控制。

**相关概念**: [Backpressure](#a), [Flow Control](#c)

---

### CSP (Communicating Sequential Processes)

**定义**: Hoare 于 1985 年提出的基于同步通信和静态事件名的进程代数。

**语法**:

```
P, Q ::= STOP | SKIP | a → P | P □ Q | P ⊓ Q | P ||| Q | P |[A]| Q
```

**相关概念**: [CCS](#c), [π-Calculus](#a), [Go Channels](#go-channels)

**参考文档**:

- `Struct/01-foundation/01.05-csp-formalization.md` (Def-S-02-02)
- `Struct/03-relationships/03.01-actor-to-csp-encoding.md` (Thm-S-12-01)

---

## D

### Data Enrichment (数据富化)

**定义**: 将原始数据流与外部数据源关联，补充上下文信息的过程。

**相关概念**: [Async I/O](#a), [Lookup Join](#i), [Dimension Table](#a)

**参考文档**:

- `Knowledge/02-design-patterns/pattern-async-io-enrichment.md`

---

### Data Mesh (数据网格)

**定义**: 一种去中心化的数据架构范式，将数据视为产品，由领域团队自治管理。

**相关概念**: [Data Product](#a), [Domain-Driven Design](#a), [Self-Serve Platform](#a)

**参考文档**:

- `Knowledge/03-business-patterns/data-mesh-streaming-architecture-2026.md`
- `Knowledge/06-frontier/streaming-data-mesh-architecture.md`

---

### Data Product (数据产品)

**定义**: 数据网格中可独立发现、寻址和消费的自治数据单元。

**相关概念**: [Data Mesh](#a), [Data as a Product](#a)

---

### Dataflow Model (Dataflow 模型)

**定义**: 将计算表示为数据在操作符之间流动的图模型，流计算的核心理论基础。

**形式化定义**:

```
𝒢 = (V, E, P, Σ, 𝕋)
```

其中 V 为顶点集，E 为边集，P 为处理函数，Σ 为状态，𝕋 为时间模型。

**相关概念**: [DAG](#a), [Operator](#a), [Stream Graph](#a)

**参考文档**:

- `Struct/01-foundation/01.04-dataflow-model-formalization.md` (Def-S-04-01)
- `Struct/02-properties/02.01-determinism-in-streaming.md` (Thm-S-04-01)

---

### DAG (Directed Acyclic Graph, 有向无环图)

**定义**: 表示数据流处理拓扑的图结构，节点为算子，边为数据流，无循环。

**相关概念**: [Dataflow Model](#a), [Job Graph](#a), [Execution Graph](#a)

---

### Deadlock Freedom (无死锁性)

**定义**: 系统保证不存在任何进程因等待永远不会发生的事件而永久阻塞的性质。

**相关概念**: [Liveness](#e), [Choreographic Programming](#a), [Session Types](#e)

**参考文档**:

- `Struct/04-proofs/04.07-deadlock-freedom-choreographic.md` (Thm-S-23-01)

---

### Delivery Guarantee (交付保证)

**定义**: 流处理系统对消息传递可靠性的承诺，分为 At-Most-Once、At-Least-Once、Exactly-Once。

**相关概念**: [At-Most-Once](#a), [At-Least-Once](#a), [Exactly-Once](#a)

**参考文档**:

- `Struct/02-properties/02.02-consistency-hierarchy.md`

---

### Determinism (确定性)

**定义**: 给定相同输入，系统总是产生相同输出的性质。

**形式化定义**:

```
Deterministic(P) ⟺ ∀x. P(x) = P(x)
```

**相关概念**: [Reproducibility](#b), [Consistency](#c)

**参考文档**:

- `Struct/02-properties/02.01-determinism-in-streaming.md` (Thm-S-07-01)

---

### Differential Dataflow

**定义**: 支持增量计算和递归的流处理模型，基于差分更新传播变化。

**相关概念**: [Incremental Computation](#a), [Materialize](#a)

---

### Distributed Snapshot (分布式快照)

**定义**: 捕获分布式系统某一时刻全局状态的一致性快照。

**相关概念**: [Chandy-Lamport Algorithm](#chandy-lamport-algorithm), [Checkpoint](#aligned-checkpoint-对齐-checkpoint), [Consistent Cut](#c)

---

### DOT (Dependent Object Types)

**定义**: 支持路径依赖类型和家族多态的高级类型系统，Scala 的理论基础。

**相关概念**: [Path-Dependent Types](#a), [FGG](#f), [Subtyping](#b)

**参考文档**:

- `Struct/04-proofs/04.06-dot-subtyping-completeness.md` (Thm-S-22-01)

---

## E

### Edge Computing (边缘计算)

**定义**: 在数据源附近（网络边缘）进行数据处理的计算范式，降低延迟和带宽消耗。

**相关概念**: [Cloud-Edge Continuum](#c), [IoT](#e), [Latency](#a)

**参考文档**:

- `Knowledge/06-frontier/edge-streaming-architecture.md`

---

### End-to-End Consistency (端到端一致性)

**定义**: 从外部数据源到外部数据汇的整个管道的一致性保证。

**形式化定义**:

```
End-to-End-EO(J) ⟺ Replayable(Src) ∧ ConsistentCheckpoint(Ops) ∧ AtomicOutput(Snk)
```

**相关概念**: [Internal Consistency](#a), [Exactly-Once](#a), [Source](#c), [Sink](#i)

**参考文档**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-05)

---

### Event-Driven Architecture (事件驱动架构)

**定义**: 以事件产生、检测和消费为核心组织组件交互的软件架构模式。

**相关概念**: [Event Streaming](#a), [Pub/Sub](#b), [CQRS](#c)

---

### Event Pattern (事件模式)

**定义**: CEP 中用于匹配事件序列的模板，支持顺序、选择、重复等运算符。

**相关概念**: [CEP](#c), [Pattern Matching](#a)

---

### Event Sourcing (事件溯源)

**定义**: 以事件序列作为系统状态真相来源的持久化模式。

**相关概念**: [CQRS](#c), [Event Store](#e), [Audit Log](#a)

---

### Event Streaming (事件流)

**定义**: 持续捕获、处理和响应事件流的计算模式。

**相关概念**: [Stream Processing](#a), [Event-Driven Architecture](#a)

---

### Event Time (事件时间)

**定义**: 数据记录产生的时间戳，由数据源赋予。

**形式化定义**:

```
t_e: Record → Timestamp
```

**相关概念**: [Processing Time](#c), [Ingestion Time](#e), [Watermark](#a)

**参考文档**:

- `Struct/01-foundation/01.01-unified-streaming-theory.md` (Def-S-01-05)
- `Flink/02-core/time-semantics-and-watermark.md`

---

### Eventual Consistency (最终一致性)

**定义**: 保证在没有新更新的情况下，最终所有副本都会收敛到相同值的一致性模型。

**形式化定义**:

```
◇□(replicas converge)
```

**相关概念**: [Strong Consistency](#c), [Causal Consistency](#a), [CALM Theorem](#a)

**参考文档**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-09)

---

### Exactly-Once (精确一次语义)

**定义**: 流计算系统保证每条输入数据对最终外部世界的影响**有且仅有一次**的语义。

**形式化定义**:

```
∀r ∈ I. c(r, 𝒯) = 1
```

**相关概念**: [At-Least-Once](#a), [At-Most-Once](#a), [Idempotency](#c)

**参考文档**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-04)
- `Struct/04-proofs/04.02-flink-exactly-once-correctness.md` (Thm-S-18-01)
- `Flink/02-core/exactly-once-semantics-deep-dive.md`

---

### Execution Graph (执行图)

**定义**: Flink 中将逻辑 JobGraph 转换为物理执行计划的图结构，包含具体的并行实例。

**相关概念**: [Job Graph](#a), [Task](#a), [Parallelism](#a)

---

### Explicit State (显式状态)

**定义**: 由用户代码显式声明和管理的流处理状态，Flink 提供 API 支持。

**相关概念**: [Implicit State](#a), [Keyed State](#a), [Operator State](#a)

---

## F

### FG (Featherweight Generic)

**定义**: Java 泛型的轻量级形式化模型，用于类型安全证明。

**相关概念**: [FGG](#f), [Type Safety](#a), [Java Generics](#a)

**参考文档**:

- `Struct/04-proofs/04.05-type-safety-fg-fgg.md` (Thm-S-21-01)

---

### FGG (Featherweight Generic Go)

**定义**: Go 泛型的轻量级形式化模型。

**相关概念**: [FG](#f), [Go](#a), [Parametric Polymorphism](#a)

**参考文档**:

- `Struct/04-proofs/04.05-type-safety-fg-fgg.md` (Thm-S-21-01)

---

### Flink Agent [Flink 2.0+, FLIP-531]

**定义**: 基于 Flink 流计算框架构建的自主智能体，支持持续感知、决策和行动。

**形式化定义**:

```
𝒜_Flink = ⟨𝒮_state, 𝒫_perception, 𝒟_decision, 𝒜_action, ℳ_memory, 𝒢_goal⟩
```

**核心特性**: 状态持久化、[Replayability](#replayability-可重放性)、分布式执行、Exactly-Once 语义

**相关概念**: [AI Agent](#a), [FLIP-531](#f), [MCP](#c), [A2A](#a), [Stateful Stream Processing](#a)

**参考文档**:

- `Flink/12-ai-ml/flink-agents-flip-531.md` (Def-F-12-30)
- `Flink/12-ai-ml/flip-531-ai-agents-ga-guide.md`

---

### FLIP-531 (Flink AI Agents 提案) [Flink 2.0+]

**定义**: Apache Flink 官方功能提案，引入 AI Agent 原生运行时支持，实现流计算与 AI 智能体的深度融合。

**核心组件**:

- **Flink Agent Runtime**: Agent 执行环境
- **MCP 集成**: Model Context Protocol 支持
- **A2A 协议**: Agent 间互操作
- **Agentic Workflow**: 智能体工作流编排

**形式化定义**:

```
FLIP-531 = ⟨ℛ_agent, ℐ_mcp, 𝒫_a2a, 𝒲_workflow⟩
```

**相关概念**: [Flink Agent](#a), [MCP](#c), [A2A](#a), [Agentic Workflow](#a)

**参考文档**:

- `Flink/12-ai-ml/flink-agents-flip-531.md`
- `Flink/12-ai-ml/flip-531-ai-agents-ga-guide.md`

---

### Flow Control (流量控制)

**定义**: 调节数据生产者和消费者之间数据传输速率的机制。

**相关概念**: [Backpressure](#a), [Credit-Based](#a), [Buffer](#b)

---

### ForSt State Backend

**定义**: Flink 2.0 引入的新一代状态后端，基于 RocksDB 改进，支持异步执行模型。

**相关概念**: [State Backend](#a), [RocksDB](#rocksdb), [Incremental Checkpoint](#a)

**参考文档**:

- `Flink/02-core/forst-state-backend.md` (Thm-F-02-45)
- `Flink/02-core/flink-2.0-forst-state-backend.md`

---

### Function as a Service (FaaS)

**定义**: 无服务器计算模式，用户编写函数代码，由平台管理基础设施和自动扩缩容。

**相关概念**: [Serverless](#e), [Lambda](#a), [Cloud-Native](#a)

**参考文档**:

- `Knowledge/06-frontier/faas-dataflow.md`
- `Knowledge/06-frontier/serverless-stream-processing-architecture.md`

---

## G

### GPU Acceleration (GPU 加速) [Flink 2.5+]

**定义**: 利用 GPU 的大规模并行计算能力执行流处理算子，通过 CUDA/OpenCL 将计算密集型操作从 CPU 卸载到 GPU。

**形式化定义**:

```
𝒪_GPU(D) = GPUKernel(Transfer(D_CPU→GPU))
```

**加速比**: S_GPU = T_CPU / (T_transfer + T_kernel + T_sync)

**适用条件**: 批次大小 n > n_threshold 且计算/传输比 > γ

**加速算子类型**: GPU 聚合、GPU Join、GPU UDF、向量搜索

**相关概念**: [CUDA](#a), [Vector Search](#a), [Flink-CUDA Runtime](#a)

**参考文档**:

- `Flink/12-ai-ml/flink-25-gpu-acceleration.md` (Def-F-12-50)

---

### Global Snapshot (全局快照)

**定义**: 分布式系统某一时刻所有进程状态的集合，用于故障恢复和一致性检查。

**相关概念**: [Distributed Snapshot](#a), [Chandy-Lamport Algorithm](#chandy-lamport-algorithm), [Checkpoint](#aligned-checkpoint-对齐-checkpoint)

---

### Global Window (全局窗口)

**定义**: 包含所有记录的单一窗口，通常配合自定义触发器使用。

**形式化定义**:

```
Global: wid_global = (-∞, +∞)
```

**相关概念**: [Tumbling Window](#b), [Sliding Window](#d), [Session Window](#d)

**参考文档**:

- `Knowledge/02-design-patterns/pattern-windowed-aggregation.md` (Def-K-02-02)

---

### Go Channels

**定义**: Go 语言中基于 CSP 模型的同步通信原语。

**相关概念**: [CSP](#c), [Channel](#a), [Goroutine](#e)

**参考文档**:

- `Struct/05-comparative/05.01-go-vs-scala-expressiveness.md` (Thm-S-24-01)

---

## H

### Happens-Before (先于关系)

**定义**: 定义事件之间因果偏序的关系，是分布式一致性的基础。

**形式化定义**:

```
∀e₁, e₂. e₁ ≺hb e₂ ⟺ e₁ 因果影响 e₂
```

**相关概念**: [Causal Consistency](#a), [Lamport Clock](#a), [Vector Clock](#c)

---

### HashMapStateBackend

**定义**: Flink 中基于堆内存的状态后端，适用于小状态、低延迟场景。

**相关概念**: [State Backend](#a), [RocksDBStateBackend](#rocksdbstatebackend), [ForSt](#forst-state-backend)

**参考文档**:

- `Flink/02-core/checkpoint-mechanism-deep-dive.md` (Def-F-02-06)

---

### Hot Key (热键)

**定义**: 数据分布中频率远高于其他键的键，导致数据倾斜和性能瓶颈。

**相关概念**: [Data Skew](#a), [Key Group](#e), [Rebalancing](#a)

**参考文档**:

- `Knowledge/09-anti-patterns/anti-pattern-04-hot-key-skew.md`

---

## I

### Idempotency (幂等性)

**定义**: 操作执行一次或多次产生相同结果的性质，是实现 Exactly-Once 的关键。

**形式化定义**:

```
f 是幂等的 ⟺ ∀x. f(f(x)) = f(x)
```

**相关概念**: [Exactly-Once](#a), [Idempotent Sink](#d), [Dedup](#a)

---

### Idempotent Sink (幂等 Sink)

**定义**: 能够安全处理重复写入的外部系统接收端，通常基于主键去重。

**相关概念**: [Sink](#i), [Idempotency](#c), [Exactly-Once](#a)

---

### Incremental Checkpoint (增量 Checkpoint)

**定义**: 仅捕获自上次 Checkpoint 以来发生变化的状态部分。

**形式化定义**:

```
ΔS_n = S_{t_n} \\ S_{t_{n-1}}, CP_n^inc = ⟨Base, {ΔS_i}_{i=1}^n⟩
```

**相关概念**: [Checkpoint](#aligned-checkpoint-对齐-checkpoint), [State Backend](#a), [RocksDB](#rocksdb)

**参考文档**:

- `Flink/02-core/checkpoint-mechanism-deep-dive.md` (Def-F-02-05, Thm-F-02-02)

---

### Incremental Computation (增量计算)

**定义**: 基于输入变化量计算输出变化量的计算模式，避免全量重算。

**形式化定义**:

```
δv = ℱ_q(δD, D), v_new = v ⊕ δv
```

**相关概念**: [Materialized View](#a), [Differential Dataflow](#differential-dataflow)

---

### Ingestion Time (摄入时间)

**定义**: 数据记录进入流处理系统的时间戳。

**形式化定义**:

```
t_i: Record → Timestamp_system
```

**相关概念**: [Event Time](#e), [Processing Time](#c)

---

### Internal Consistency (内部一致性)

**定义**: 流处理引擎自身在故障恢复后，其内部算子状态与全局快照的一致性。

**形式化定义**:

```
Internal-Consistency(Ops) ⟺ ∀k. Consistent(𝒢_k) ∧ NoOrphans(𝒢_k) ∧ Reachable(𝒢_k)
```

**相关概念**: [End-to-End Consistency](#c), [Checkpoint](#aligned-checkpoint-对齐-checkpoint)

**参考文档**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-06)

---

### IoT (Internet of Things, 物联网)

**定义**: 由物理设备、传感器等组成的网络，产生大规模流数据。

**相关概念**: [Edge Computing](#c), [Sensor Data](#a), [Stream Processing](#a)

**参考文档**:

- `Knowledge/03-business-patterns/iot-stream-processing.md`
- `Flink/07-case-studies/case-iot-stream-processing.md`

---

### Iris

**定义**: 基于高阶分离逻辑的并发程序验证框架。

**相关概念**: [Separation Logic](#a), [Formal Verification](#a), [Model Checking](#c)

**参考文档**:

- `Struct/07-tools/iris-separation-logic.md`

---

## J

### Job Graph (作业图)

**定义**: Flink 中用户程序编译后的逻辑执行图，表示算子间的数据流关系。

**相关概念**: [Execution Graph](#a), [DAG](#a), [Operator](#a)

---

### JobManager

**定义**: Flink 集群中的主控进程，负责任务调度、协调和故障恢复。

**相关概念**: [TaskManager](#taskmanager), [ResourceManager](#resourcemanager), [Dispatcher](#a)

**参考文档**:

- `Flink/01-architecture/deployment-architectures.md`

---

### Join

**定义**: 将两个数据流按关联条件合并的操作。

**类型**:

- **Interval Join**: 基于时间间隔的流 Join
- **Temporal Join**: 时态表 Join
- **Lookup Join**: 维表 Join
- **Delta Join**: 增量 Join

**相关概念**: [Stream Join](#a), [Window Join](#d)

**参考文档**:

- `Flink/02-core/delta-join.md`

---

## K

### Key Group (键组)

**定义**: Flink 中 Keyed State 的分区单位，决定状态在并行实例间的分布。

**相关概念**: [Keyed State](#a), [Parallelism](#a), [State Partitioning](#a)

---

### Keyed State (键控状态)

**定义**: 按 Key 分区存储的状态，每个 Key 有独立的状态空间。

**形式化定义**:

```
KeyedState: (K, State[K]) → State[K]
```

**相关概念**: [Operator State](#a), [State Backend](#a), [Key Group](#e)

---

### KeyedProcessFunction

**定义**: Flink DataStream API 中访问 Keyed State 和定时器的低级处理函数。

**相关概念**: [ProcessFunction](#processfunction), [Keyed State](#a), [Timer](#e)

---

### KeyedStream

**定义**: Flink 中按 Key 分区的数据流，支持 Keyed State 操作。

**相关概念**: [DataStream](#a), [Keyed State](#a), [Partitioning](#a)

---

### Kubernetes

**定义**: 开源容器编排平台，Flink 的主要部署目标。

**相关概念**: [Container](#a), [Operator Pattern](#a), [Cloud-Native](#a)

**参考文档**:

- `Flink/10-deployment/flink-kubernetes-operator-deep-dive.md`
- `Flink/10-deployment/kubernetes-deployment-production-guide.md`

---

## L

### Lakehouse (湖仓一体)

**定义**: 结合数据湖（低成本存储）和数据仓库（高性能分析）优点的架构范式。

**相关概念**: [Delta Lake](#a), [Iceberg](#a), [Paimon](#a)

**参考文档**:

- `Flink/14-lakehouse/streaming-lakehouse-architecture.md`
- `Knowledge/06-frontier/streaming-lakehouse-iceberg-delta.md`

---

### Lambda Architecture (Lambda 架构)

**定义**:  Nathan Marz 提出的批流分离架构，维护批处理层和速度层两套系统。

**相关概念**: [Kappa Architecture](#a), [Batch Processing](#a), [Stream Processing](#a)

---

### Latency (延迟)

**定义**: 从事件发生到结果被处理/可见的时间间隔。

**类型**:

- **Processing Latency**: 处理延迟
- **End-to-End Latency**: 端到端延迟
- **Watermark Latency**: Watermark 延迟

**相关概念**: [Throughput](#g), [SLA](#a), [Real-time](#a)

---

### LSM-Tree (Log-Structured Merge Tree)

**定义**: 写优化的磁盘数据结构，RocksDB 的基础。

**相关概念**: [RocksDB](#rocksdb), [State Backend](#a), [Compaction](#a)

---

## M

### Materialized View (物化视图)

**定义**: 预计算并物理存储的查询结果，流数据库中自动增量维护。

**形式化定义**:

```
v = q(D), 当 δD 发生时: v_new = v ⊕ ℱ_q(δD, D)
```

**相关概念**: [View Maintenance](#a), [Incremental Computation](#a), [Continuous Query](#c)

**参考文档**:

- `Knowledge/06-frontier/streaming-databases.md` (Def-K-06-13)
- `Flink/03-sql-table-api/materialized-tables.md`

---

### MCP (Model Context Protocol) [Anthropic 2024, Flink 2.0+]

**定义**: Anthropic 提出的开放协议，用于标准化 LLM 与外部工具的交互。

**形式化定义**:

```
MCP_Flink = ⟨𝒯, ℛ, 𝒞, ℋ⟩
```

其中 𝒯 为工具集合，ℛ 为工具选择函数，𝒞 为调用构造函数，ℋ 为记忆映射。

**核心能力**: 工具发现、调用构造、结果观察、记忆更新

**相关概念**: [AI Agent](#a), [Tool Calling](#a), [A2A](#a), [FLIP-531](#f)

**参考文档**:

- `Flink/12-ai-ml/flink-agents-flip-531.md` (Def-F-12-32)
- `Knowledge/06-frontier/mcp-protocol-agent-streaming.md`

---

### Message Passing (消息传递)

**定义**: 并发实体间通过发送和接收消息进行通信的模型。

**相关概念**: [Actor Model](#a), [CSP](#c), [Shared Memory](#a)

---

### Microservices (微服务)

**定义**: 将应用拆分为小型、自治服务的架构风格，服务间通过 API 通信。

**相关概念**: [Service Mesh](#c), [Domain-Driven Design](#a), [Cloud-Native](#a)

---

### Model Checking (模型检测)

**定义**: 自动验证有限状态系统是否满足规约的形式化方法。

**相关概念**: [Formal Verification](#a), [TLA+](#tla), [State Space](#a)

**参考文档**:

- `Struct/07-tools/model-checking-practice.md`
- `Struct/07-tools/tla-for-flink.md`

---

### Multi-Agent (多智能体)

**定义**: 多个 AI Agent 协作完成复杂任务的系统架构。

**架构模式**:

- **Orchestrator-Worker**: 中央协调器分配任务
- **Supervisor + Workers**: 监督者监控 Worker 状态
- **Decentralized**: 去中心化直接通信

**相关概念**: [AI Agent](#a), [A2A](#a), [Coordination](#a)

**参考文档**:

- `Knowledge/06-frontier/ai-agent-streaming-architecture.md` (Def-K-06-114)

---

## N

### Network Buffer (网络缓冲区)

**定义**: Flink 中用于网络数据传输的内存缓冲区。

**相关概念**: [Buffer](#b), [Backpressure](#a), [Credit-Based](#a)

---

## O

### Observability (可观测性)

**定义**: 通过系统输出（指标、日志、追踪）理解内部状态的能力。

**三大支柱**:

- **Metrics**: 指标
- **Logs**: 日志
- **Traces**: 分布式追踪

**相关概念**: [Monitoring](#g), [OpenTelemetry](#opentelemetry), [SLA](#a)

**参考文档**:

- `Flink/15-observability/opentelemetry-streaming-observability.md`
- `Flink/15-observability/flink-opentelemetry-observability.md`

---

### OpenTelemetry

**定义**: 开源可观测性框架，提供统一的指标、日志和追踪标准。

**相关概念**: [Observability](#a), [Metrics](#c), [Tracing](#a)

---

### Operator (算子)

**定义**: Flink 中执行数据转换的基本计算单元。

**分类**:

- **Source**: 数据源
- **Transformation**: 转换
- **Sink**: 数据汇

**形式化定义**:

```
Operator: Input × State → Output × State
```

**相关概念**: [Dataflow Model](#a), [Task](#a), [UDF](#c)

---

### Operator State (算子状态)

**定义**: 与算子实例绑定的状态，不按 Key 分区。

**相关概念**: [Keyed State](#a), [Broadcast State](#a), [State Backend](#a)

---

### Orchestration (编排)

**定义**: 协调多个服务或组件完成业务流程的模式。

**相关概念**: [Multi-Agent](#a), [Workflow](#f), [Choreography](#a)

---

## P

### Parallelism (并行度)

**定义**: 算子或任务的并行执行实例数量。

**形式化定义**:

```
Parallelism(op) = |{instance_i(op)}|
```

**相关概念**: [Slot](#slot), [Task](#a), [Key Group](#e)

---

### Path-Dependent Types (路径依赖类型)

**定义**: 依赖于值的类型的类型，如 `x.type` 依赖于 `x` 的值。

**相关概念**: [DOT](#dot-dependent-object-types), [Scala](#scala), [Dependent Types](#d)

**参考文档**:

- `Struct/06-frontier/06.04-pdot-path-dependent-types.md`

---

### Pattern Matching (模式匹配)

**定义**: 根据数据结构模式进行条件分支的机制。

**相关概念**: [CEP](#c), [Event Pattern](#a)

---

### Petri Net (Petri 网)

**定义**: 用于建模并发系统的图形化数学模型，由库所(place)和变迁(transition)组成。

**相关概念**: [Process Calculus](#a), [Concurrency](#c), [Workflow](#f)

**参考文档**:

- `Struct/01-foundation/01.06-petri-net-formalization.md` (Thm-S-06-01)

---

### π-Calculus (π 演算)

**定义**: Milner 等人于 1992 年提出的支持名字传递(移动性)的进程代数。

**语法**:

```
P, Q ::= 0 | a(x).P | ā⟨b⟩.P | τ.P | P + Q | P | Q | (νa)P | !P
```

**相关概念**: [CCS](#c), [CSP](#c), [Mobile Processes](#b), [Session Types](#e)

**参考文档**:

- `Struct/01-foundation/01.02-process-calculus-primer.md` (Def-S-02-03, Thm-S-02-01)

---

### Processing Time (处理时间)

**定义**: 数据记录被算子处理时的机器时间。

**形式化定义**:

```
t_p: () → Timestamp_wall
```

**相关概念**: [Event Time](#e), [Ingestion Time](#e)

---

### Process Calculus (进程演算)

**定义**: 用于描述并发系统形式化语义的代数框架家族。

**主要成员**: [CCS](#c), [CSP](#c), [π-Calculus](#a), [Actor Calculus](#a)

**参考文档**:

- `Struct/01-foundation/01.02-process-calculus-primer.md`

---

### ProcessFunction

**定义**: Flink DataStream API 中提供对时间和状态细粒度控制的底层处理函数。

**相关概念**: [KeyedProcessFunction](#keyedprocessfunction), [Timer](#e), [State](#a)

---

### Progress (进展性)

**定义**: 类型安全性质之一，保证良类型程序不会 stuck（陷入非终止也非错误的状态）。

**相关概念**: [Preservation](#a), [Type Safety](#a), [Deadlock Freedom](#a)

---

### Pub/Sub (发布-订阅)

**定义**: 消息传递模式，发布者发送消息到主题，订阅者接收感兴趣的主题消息。

**相关概念**: [Message Passing](#a), [Kafka](#a), [Event Streaming](#a)

---

## Q

### Query Optimization (查询优化)

**定义**: 自动选择查询执行计划以最小化资源消耗的过程。

**相关概念**: [Calcite](#a), [Cost-Based Optimization](#a), [Rule-Based Optimization](#a)

**参考文档**:

- `Flink/03-sql-table-api/flink-sql-calcite-optimizer-deep-dive.md`

---

## R

### RAG (Retrieval-Augmented Generation)

**定义**: 结合检索系统和生成模型的 AI 架构，通过检索外部知识增强 LLM 输出。

**形式化定义**:

```
RAG(q) = Generate(q, Retrieve(q, KnowledgeBase))
```

**相关概念**: [Vector Search](#a), [LLM](#l), [Knowledge Base](#a)

**参考文档**:

- `Knowledge/06-frontier/real-time-rag-architecture.md`
- `Flink/12-ai-ml/rag-streaming-architecture.md`

---

### Real-Time (实时)

**定义**: 在严格时间约束内产生结果的系统特性。

**分类**:

- **Hard Real-Time**: 硬实时，错过截止期限导致系统失败
- **Soft Real-Time**: 软实时，错过截止期限降低服务质量
- **Near Real-Time**: 近实时，秒级延迟可接受

**相关概念**: [Latency](#a), [SLA](#a)

---

### ReAct (Reasoning + Acting)

**定义**: AI Agent 架构模式，交错推理(Thought)和行动(Action)循环解决复杂问题。

**形式化定义**:

```
ReAct: 𝒪_t → Thought → τ_t → Action → a_t → Observation → 𝒪_{t+1}
```

**相关概念**: [AI Agent](#a), [Chain-of-Thought](#a)

**参考文档**:

- `Knowledge/06-frontier/ai-agent-streaming-architecture.md` (Def-K-06-111)

---

### Recovery (恢复)

**定义**: 故障后从 Checkpoint 或 Savepoint 重建系统状态的过程。

**相关概念**: [Checkpoint](#aligned-checkpoint-对齐-checkpoint), [Savepoint](#a), [Failover](#a)

---

### Replayability (可重放性)

**定义**: 从 Checkpoint 完整重放执行历史的能力，Flink Agent 的核心特性。

**形式化定义**:

```
ℛ_replay = ⟨𝒞, ℒ, ℋ⟩
```

**相关概念**: [Checkpoint](#aligned-checkpoint-对齐-checkpoint), [Audit](#a), [Debugging](#b)

**参考文档**:

- `Flink/12-ai-ml/flink-agents-flip-531.md` (Def-F-12-35)

---

### ResourceManager

**定义**: Flink 中负责集群资源分配和管理的组件。

**相关概念**: [JobManager](#jobmanager), [TaskManager](#taskmanager), [Slot](#slot)

---

### RocksDB

**定义**: Facebook 开发的嵌入式键值存储，基于 LSM-Tree。

**相关概念**: [LSM-Tree](#e), [State Backend](#a), [EmbeddedRocksDBStateBackend](#rocksdbstatebackend)

---

### RocksDBStateBackend

**定义**: Flink 中基于 RocksDB 的状态后端，支持大状态、增量 Checkpoint。

**相关概念**: [State Backend](#a), [RocksDB](#rocksdb), [Incremental Checkpoint](#a)

**参考文档**:

- `Flink/02-core/checkpoint-mechanism-deep-dive.md` (Def-F-02-06)

---

## S

### Savepoint (保存点)

**定义**: 用户触发的全局一致快照，用于应用升级、迁移和备份，与 Checkpoint 语义相同但生命周期管理不同。

**相关概念**: [Checkpoint](#aligned-checkpoint-对齐-checkpoint), [Recovery](#c), [Upgrading](#a)

---

### Scala

**定义**: 融合面向对象和函数式编程的 JVM 语言，Flink 的原生 API 语言之一。

**相关概念**: [Type System](#e), [Akka](#a), [JVM](#j)

**参考文档**:

- `Flink/09-language-foundations/01.01-scala-types-for-streaming.md`
- `Flink/09-language-foundations/01.03-scala3-type-system-formalization.md`

---

### Scale-Up / Scale-Out (纵向/横向扩展)

**定义**:

- **Scale-Up**: 增强单个节点的计算能力
- **Scale-Out**: 增加节点数量扩展处理能力

**相关概念**: [Elasticity](#a), [Autoscaling](#a), [Parallelism](#a)

---

### Semantic Matching (语义匹配)

**定义**: 基于语义相似度而非精确值匹配数据的技术，常用于 RAG 和向量搜索。

**相关概念**: [Vector Search](#a), [Embedding](#b), [Similarity Search](#a)

---

### Separation Logic (分离逻辑)

**定义**: 用于推理可变数据结构的逻辑框架，支持局部推理。

**相关概念**: [Iris](#iris), [Formal Verification](#a), [Concurrent Separation Logic](#a)

**参考文档**:

- `Struct/07-tools/iris-separation-logic.md`

---

### Serverless (无服务器)

**定义**: 云计算执行模型，云提供商动态管理机器资源的分配。

**相关概念**: [Serverless Flink](#e), [FaaS](#a), [Cloud-Native](#a), [Autoscaling](#a)

**参考文档**:

- `Knowledge/06-frontier/serverless-stream-processing-architecture.md`
- `Flink/10-deployment/flink-serverless-architecture.md`

---

### Serverless Flink [Flink 2.0+ GA]

**定义**: Apache Flink 在 Kubernetes 上的生产级无服务器实现，支持 Scale-to-Zero 和按需计费。

**形式化定义**:

```
ServerlessFlink_GA = ⟨𝒦, 𝒜, 𝒮, 𝒞, ℬ⟩
```

其中 𝒦 为 Kubernetes Native，𝒜 为 Autoscaler，𝒮 为分离式状态存储，𝒞 为增量异步检查点，ℬ 为 GB-秒精确计费。

**核心特性**:

- **Scale-to-Zero**: 无负载时缩减资源至零
- **冷启动优化**: <10s 快照恢复（传统 110-420s）
- **精确计费**: 秒级计费粒度
- **SLA 保证**: 99.9% 可用性

**相关概念**: [Serverless](#e), [Scale-to-Zero](#a), [ForSt](#forst-state-backend), [Kubernetes](#kubernetes)

**参考文档**:

- `Flink/10-deployment/serverless-flink-ga-guide.md` (Def-F-10-50)
- `Flink/10-deployment/flink-serverless-architecture.md`

---

### Session Types (会话类型)

**定义**: 描述通信协议结构的类型系统，保证通信安全和无死锁。

**形式化定义**:

```
S ::= !T.S | ?T.S | ⊕{l_i: S_i} | &{l_i: S_i} | end
```

**相关概念**: [Type Safety](#a), [Deadlock Freedom](#a), [Protocol Compliance](#a)

**参考文档**:

- `Struct/01-foundation/01.07-session-types.md` (Thm-S-01-03, Thm-S-01-04)

---

### Session Window (会话窗口)

**定义**: 根据活动间隙动态划分的窗口，无活动超过 gap 后关闭。

**形式化定义**:

```
Session(g, r₁, r₂, ...): wid = [t_first, t_last + g)
```

**相关概念**: [Tumbling Window](#b), [Sliding Window](#d), [Window](#d)

**参考文档**:

- `Knowledge/02-design-patterns/pattern-windowed-aggregation.md` (Def-K-02-02)

---

### Shared Memory (共享内存)

**定义**: 多个并发实体访问同一内存区域的通信模型，区别于消息传递。

**相关概念**: [Message Passing](#a), [Race Condition](#a), [Synchronization](#a)

---

### Side Output (侧输出)

**定义**: 从主流分离特定数据到旁路流的机制，用于处理迟到数据或异常。

**相关概念**: [Late Data](#a), [Data Splitting](#a), [Main Stream](#a)

**参考文档**:

- `Knowledge/02-design-patterns/pattern-side-output.md`

---

### Smart Checkpointing (智能检查点) [Flink 2.0+]

**定义**: 自适应的分布式状态快照机制，能够根据运行时负载动态调整检查点策略。

**核心策略**:

- **自适应检查点间隔**: 基于负载动态调整
- **增量检查点优化**: 仅捕获变更状态
- **局部检查点**: 故障域隔离的快照
- **检查点并行度优化**: 动态并行度调整

**形式化定义**:

```
SmartCP = ⟨ℐ_adaptive, Δ_incremental, 𝒫_partial, 𝒫_parallel⟩
```

**相关概念**: [Checkpoint](#aligned-checkpoint-对齐-checkpoint), [Incremental Checkpoint](#a), [Adaptive Execution Engine](#a), [ForSt](#forst-state-backend)

**参考文档**:

- `Flink/02-core/smart-checkpointing-strategies.md` (Def-F-02-110, Thm-F-02-60)

---

### Sink (数据汇)

**定义**: 流处理中将数据写入外部系统的组件。

**相关概念**: [Source](#c), [Connector](#c), [Exactly-Once](#a)

---

### Sliding Window (滑动窗口)

**定义**: 固定大小、按固定步长滑动的窗口，窗口间可能重叠。

**形式化定义**:

```
Sliding(δ, s): wid_n = [n·s, n·s + δ)
```

**相关概念**: [Tumbling Window](#b), [Session Window](#d), [Window](#d)

---

### Slot

**定义**: Flink TaskManager 中资源分配的基本单位，一个 Task Slot 可执行一个任务链。

**相关概念**: [TaskManager](#taskmanager), [Task](#a), [Resource](#c)

---

### Source (数据源)

**定义**: 流处理中从外部系统读取数据的组件。

**相关概念**: [Sink](#i), [Connector](#c), [Offset](#e)

---

### Source Split (源分片)

**定义**: 数据源的可并行读取单元，如 Kafka 的 partition。

**相关概念**: [Source](#c), [Parallelism](#a), [Partition](#a)

---

### Split-Level Watermark

**定义**: 在 Source Split 级别生成 Watermark 的机制，支持更精细的流控制。

**相关概念**: [Watermark](#a), [Source Split](#c)

**参考文档**:

- `Flink/15-observability/split-level-watermark-metrics.md`

---

### SQL/Table API

**定义**: Flink 提供的声明式 API，支持标准 SQL 和 Table DSL。

**相关概念**: [DataStream API](#a), [Query Optimization](#a), [Calcite](#a)

**参考文档**:

- `Flink/03-sql-table-api/sql-vs-datastream-comparison.md`

---

### State (状态)

**定义**: 流处理中跨记录保持的数据，是有状态计算的基础。

**分类**:

- **Keyed State**: 键控状态
- **Operator State**: 算子状态
- **Broadcast State**: 广播状态

**相关概念**: [Stateful Processing](#a), [State Backend](#a)

---

### State Backend (状态后端)

**定义**: 负责状态存储、访问和快照持久化的运行时组件。

**实现类型**:

- **HashMapStateBackend**: 内存存储
- **EmbeddedRocksDBStateBackend**: 磁盘存储
- **ForStStateBackend**: Flink 2.0 新一代后端

**相关概念**: [State](#a), [Checkpoint](#aligned-checkpoint-对齐-checkpoint), [Recovery](#c)

**参考文档**:

- `Flink/02-core/checkpoint-mechanism-deep-dive.md` (Def-F-02-06)
- `Flink/06-engineering/state-backend-selection.md`

---

### Stateful Stream Processing (有状态流处理)

**定义**: 维护和使用跨记录状态的流计算模式。

**形式化定义**:

```
F: (K, V) × State[K] → State[K] × O
```

**相关概念**: [Stateless Processing](#a), [State](#a), [Keyed State](#a)

---

### State Partitioning (状态分区)

**定义**: 将 Keyed State 分布到多个并行实例的策略。

**相关概念**: [Key Group](#e), [Parallelism](#a), [Keyed State](#a)

---

### State TTL (状态生存时间)

**定义**: 为状态设置过期时间，自动清理过期数据。

**相关概念**: [State](#a), [Cleanup](#a), [Expiration](#a)

**参考文档**:

- `Flink/02-core/flink-state-ttl-best-practices.md`

---

### Stateless Processing (无状态处理)

**定义**: 不维护跨记录状态的流计算模式，每条记录独立处理。

**形式化定义**:

```
F: I → O (纯函数)
```

**相关概念**: [Stateful Processing](#a), [Pure Function](#c)

---

### Stream Graph (流图)

**定义**: Flink 程序最初生成的逻辑执行图，表示用户定义的数据流转换。

**相关概念**: [Job Graph](#a), [Execution Graph](#a), [Dataflow](#a)

---

### Stream Join (流 Join)

**定义**: 将两个流按关联条件合并的操作，需处理无界性挑战。

**相关概念**: [Join](#join), [Window Join](#d), [Interval Join](#a)

---

### Stream-Batch Unification (流批一体) [Flink 2.5+]

**定义**: Flink 2.5 的核心演进目标，从架构层面彻底消除流处理与批处理的边界。

**架构演进**:

- **Flink 1.x**: DataStream API (流) + DataSet API (批) - 双 API 分离
- **Flink 2.0**: DataStream API 统一 - 执行层部分统一
- **Flink 2.5**: 完全统一架构 - 执行引擎、存储层、API 全面统一

**形式化定义**:

```
UnifiedArch = ⟨ℱ, 𝒰_exec, 𝒰_storage, 𝒰_api⟩
```

**核心特性**: 统一执行引擎、统一存储层、统一 API 层、自适应执行模式选择

**相关概念**: [DataStream API](#a), [Batch Processing](#a), [Adaptive Execution Engine](#a), [Unified Planner](#a)

**参考文档**:

- `Flink/08-roadmap/flink-25-stream-batch-unification.md` (Def-F-08-56)

---

### Stream Processing (流处理)

**定义**: 处理无界、持续到达数据流的计算模式。

**特征**:

- 数据无界(Unbounded)
- 持续计算
- 低延迟要求

**相关概念**: [Batch Processing](#a), [Event Stream](#a), [Real-Time](#a)

---

### Streaming Database (流数据库)

**定义**: 专为连续数据流设计的数据库系统，支持持续查询和物化视图增量维护。

**形式化定义**:

```
𝒮𝒟 = (S, 𝒬, 𝒱, Δ, τ)
```

**相关概念**: [Materialized View](#a), [Continuous Query](#c), [RisingWave](#a)

**参考文档**:

- `Knowledge/06-frontier/streaming-databases.md` (Def-K-06-12)
- `Knowledge/04-technology-selection/streaming-database-guide.md`

---

### Streaming ETL (流式 ETL)

**定义**: 以流方式持续执行抽取(Extract)、转换(Transform)、加载(Load)的数据集成模式。

**相关概念**: [CDC](#a), [Data Pipeline](#a), [Real-Time Analytics](#a)

**参考文档**:

- `Flink/02-core/streaming-etl-best-practices.md`

---

### Strong Consistency (强一致性)

**定义**: 所有操作在全局历史上存在唯一线性化点，外部观察者看到的顺序与真实时间一致。

**形式化定义**:

```
∀op_i, op_j. t_real(op_i) ≺ t_real(op_j) ⟹ op_i ≺_S op_j
```

**相关概念**: [Linearizability](#a), [Causal Consistency](#a), [Eventual Consistency](#a)

**参考文档**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-07)

---

### Subtyping (子类型)

**定义**: 类型系统中，若类型 S 的值可在任何期望类型 T 的上下文中使用，则 S 是 T 的子类型。

**形式化定义**:

```
S <: T ⟺ ∀v: S. v: T
```

**相关概念**: [Type System](#e), [Variance](#a), [DOT](#dot-dependent-object-types)

---

## T

### Table API

**定义**: Flink 提供的基于 Table 的声明式 API，类型安全的 SQL 替代。

**相关概念**: [SQL](#l), [DataStream API](#a), [Calcite](#a)

---

### Task (任务)

**定义**: Flink 执行图中的基本执行单元，对应算子的一个并行实例。

**相关概念**: [Operator](#a), [Subtask](#a), [TaskManager](#taskmanager)

---

### TaskManager

**定义**: Flink 集群中的工作进程，负责执行具体的数据处理任务。

**相关概念**: [JobManager](#jobmanager), [Slot](#slot), [Task](#a)

---

### TEE (Trusted Execution Environment, 可信执行环境)

**定义**: 处理器中的安全区域，保证代码和数据的机密性和完整性。

**相关概念**: [Confidential Computing](#a), [Security](#c), [Privacy](#a)

**参考文档**:

- `Flink/13-security/trusted-execution-flink.md`
- `Flink/13-security/gpu-confidential-computing.md`

---

### TLA+

**定义**: Leslie Lamport 开发的形式化规约语言，用于描述和验证并发和分布式系统。

**相关概念**: [Model Checking](#c), [Formal Verification](#a), [Temporal Logic](#a)

**参考文档**:

- `Struct/07-tools/tla-for-flink.md`

---

### Timer (定时器)

**定义**: Flink ProcessFunction 中用于在特定时间点触发回调的机制。

**类型**:

- **Event Time Timer**: 基于事件时间
- **Processing Time Timer**: 基于处理时间

**相关概念**: [ProcessFunction](#processfunction), [Event Time](#e), [Window](#d)

---

### Tool Calling (工具调用)

**定义**: LLM 调用外部 API 或函数的能力，AI Agent 的核心能力。

**相关概念**: [MCP](#c), [Function Calling](#a), [AI Agent](#a)

---

### Trace Equivalence (迹等价)

**定义**: 两个进程如果可以执行相同的动作序列则迹等价。

**形式化定义**:

```
P ≈_T Q ⟺ traces(P) = traces(Q)
```

**相关概念**: [Bisimulation](#a), [Process Calculus](#a), [CCS](#c)

---

### Trigger (触发器)

**定义**: 决定窗口何时输出计算结果的谓词函数。

**形式化定义**:

```
Trigger: WindowID × 𝕋_watermark × State → {FIRE, CONTINUE, PURGE}
```

**相关概念**: [Window](#d), [Evictor](#c), [Watermark](#a)

**参考文档**:

- `Knowledge/02-design-patterns/pattern-windowed-aggregation.md` (Def-K-02-03)

---

### Tumbling Window (滚动窗口)

**定义**: 固定大小、不重叠的窗口，每条记录精确属于一个窗口。

**形式化定义**:

```
Tumbling(δ): wid_n = [nδ, (n+1)δ)
```

**相关概念**: [Sliding Window](#d), [Session Window](#d), [Window](#d)

**参考文档**:

- `Knowledge/02-design-patterns/pattern-windowed-aggregation.md` (Def-K-02-02)

---

### Type Safety (类型安全)

**定义**: 程序执行过程中不会出现类型错误的保证，由 Progress + Preservation 组成。

**形式化定义**:

```
Type Safety = Progress ∧ Preservation
```

**相关概念**: [Progress](#e), [Preservation](#a), [Type System](#e)

**参考文档**:

- `Struct/02-properties/02.05-type-safety-derivation.md` (Thm-S-11-01)

---

### Type System (类型系统)

**定义**: 编程语言中用于分类表达式、避免运行时错误的逻辑系统。

**相关概念**: [Type Safety](#a), [Subtyping](#b), [Polymorphism](#h)

---

## U

### USTM (Unified Streaming Theory Model)

**定义**: 统一流计算元模型，整合 Actor、CSP、Dataflow、Petri 网四大范式。

**形式化定义**:

```
USTM ::= (ℒ, ℳ, 𝒫, 𝒞, 𝒮, 𝒯, Σ, Φ)
```

**相关概念**: [Dataflow Model](#a), [Actor Model](#a), [CSP](#c)

**参考文档**:

- `Struct/01-foundation/01.01-unified-streaming-theory.md` (Def-S-01-01)

---

### Unaligned Checkpoint (非对齐 Checkpoint)

**定义**: 算子在收到**任意**输入通道的 Barrier 时立即触发快照，将其他通道未处理的记录作为状态保存。

**形式化定义**:

```
UnalignedSnapshot(t, n) ⟺ ∃c ∈ Inputs(t): Barrier(n) ∈ Received(c)
```

**相关概念**: [Aligned Checkpoint](#a), [Barrier](#a), [In-Flight Data](#a)

**参考文档**:

- `Flink/02-core/checkpoint-mechanism-deep-dive.md` (Def-F-02-04)

---

### Unbounded Stream (无界流)

**定义**: 数据量理论上无限的数据流，流处理的主要数据抽象。

**形式化定义**:

```
Unbounded(S) ⟺ |S| = ∞
```

**相关概念**: [Bounded Stream](#a), [Stream Processing](#a)

---

## V

### Vector Search (向量搜索)

**定义**: 基于向量相似度而非精确匹配的数据检索技术，用于 RAG 和语义搜索。

**形式化定义**:

```
Search(q, V, k) = TopK(Embed(q), V, k)
```

**相关概念**: [RAG](#rag-retrieval-augmented-generation), [Embedding](#b), [Similarity Search](#a)

**参考文档**:

- `Flink/03-sql-table-api/vector-search.md`
- `Flink/12-ai-ml/vector-database-integration.md`

---

### View Maintenance (视图维护)

**定义**: 基础数据变化时增量更新物化视图的过程。

**策略**:

- **Immediate**: 立即维护
- **Deferred**: 延迟维护
- **On-demand**: 按需维护

**相关概念**: [Materialized View](#a), [Incremental Computation](#a)

---

## W

### WASM (WebAssembly) [Flink 2.0+]

**定义**: 面向 Web 的二进制指令格式，也可用于服务器端计算。Flink 2.0+ 支持 WebAssembly UDF。

**WASM UDF 特性**:

- 多语言支持 (Rust, C++, Go)
- 沙箱安全执行
- 接近原生的性能
- 冷启动优化

**相关概念**: [WASI](#wasi), [WebAssembly UDF](#a), [Serverless](#e), [UDF](#c)

**参考文档**:

- `Flink/13-wasm/wasm-streaming.md`
- `Flink/09-language-foundations/09-wasm-udf-frameworks.md`

---

### WASI

**定义**: WebAssembly System Interface，提供 WASM 模块与系统资源交互的标准接口。

**相关概念**: [WASM](#a), [WebAssembly UDF](#a), [Component Model](#c)

**参考文档**:

- `Flink/13-wasm/wasi-0.3-async-preview.md`
- `Flink/09-language-foundations/10-wasi-component-model.md`

---

### WebAssembly UDF (WASM UDF) [Flink 2.0+]

**定义**: 使用 WebAssembly 技术实现的用户定义函数，支持多语言编写并在沙箱环境中安全执行。

**核心优势**:

- **语言无关**: 支持 Rust, C/C++, Go, AssemblyScript
- **性能**: 接近原生代码的执行效率
- **安全**: 沙箱隔离，细粒度权限控制
- **可移植**: Write Once, Run Anywhere

**形式化定义**:

```
WASM_UDF = ⟨ℳ_wasm, ℐ_interface, 𝒮_sandbox, 𝒫_perf⟩
```

**相关概念**: [WASM](#a), [WASI](#wasi), [UDF](#c)

**参考文档**:

- `Flink/09-language-foundations/09-wasm-udf-frameworks.md`
- `Flink/13-wasm/wasm-streaming.md`

---

### Watermark (水印)

**定义**: 流处理中用于衡量事件时间进展的特殊标记，表示特定时间戳之前的数据已到达。

**形式化定义**:

```
Watermark(t_w) ::= ∀e ∈ Stream. t_e(e) ≤ t_w ∨ late(e)
```

**相关概念**: [Event Time](#e), [Window](#d), [Late Data](#a)

**参考文档**:

- `Struct/02-properties/02.03-watermark-monotonicity.md` (Thm-S-09-01)
- `Struct/04-proofs/04.04-watermark-algebra-formal-proof.md` (Thm-S-20-01)
- `Flink/02-core/time-semantics-and-watermark.md`

---

### Window (窗口)

**定义**: 将无界流切分为有限时间桶进行计算的抽象。

**类型**:

- [Tumbling Window](#b)
- [Sliding Window](#d)
- [Session Window](#d)
- [Global Window](#a)

**形式化定义**:

```
Window(S, ω) = {S_w : w ∈ ω}, S_w = {e ∈ S | e.time ∈ w}
```

**相关概念**: [Window Assigner](#a), [Trigger](#e), [Evictor](#c)

**参考文档**:

- `Knowledge/02-design-patterns/pattern-windowed-aggregation.md` (Def-K-02-01, Def-K-02-02)

---

### Window Assigner (窗口分配器)

**定义**: 将流中每条记录映射到一组时间窗口的函数。

**形式化定义**:

```
Assigner: 𝒟 × 𝕋 → 𝒫(WindowID)
```

**相关概念**: [Window](#d), [Trigger](#e), [Event Time](#e)

---

### Windowed Aggregation (窗口聚合)

**定义**: 将无界数据流切分为有限窗口进行聚合计算的设计模式。

**相关概念**: [Window](#d), [Aggregation](#a), [Trigger](#e)

**参考文档**:

- `Knowledge/02-design-patterns/pattern-windowed-aggregation.md` (Thm-K-02-01)

---

## 符号参考

### 形式化符号表

| 符号 | 含义 | 使用场景 |
|------|------|----------|
| `∀` | 全称量词 | 所有...都满足... |
| `∃` | 存在量词 | 存在...满足... |
| `∧` / `∨` | 合取 / 析取 | 逻辑与 / 或 |
| `⟹` / `⟺` | 蕴含 / 等价 | 如果...则... / 当且仅当 |
| `≺` | 先于 / 偏序 | happens-before 关系 |
| `□` / `◇` | 必然 / 可能 | 时序逻辑算子 |
| `⟨⟩` / `[]` | 元组 / 集合 | 数据结构表示 |
| `→` | 映射 / 函数 | 类型签名 |
| `×` | 笛卡尔积 | 类型组合 |
| `\` / `\\` | 差集 / 限制 | 集合运算 |
| `|` | 并行组合 | 进程代数 |
| `⊕` / `&` | 内部 / 外部选择 | 会话类型 |
| `!` / `?` | 发送 / 接收 | 会话类型 |
| `ν` / `(νa)` | 新名字创建 | π-演算限制算子 |

---

## 引用参考











---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.1 | 2026-04-04 | 新增 Flink 2.4/2.5/3.0 术语: AI Agent、Serverless Flink、Adaptive Execution Engine、Smart Checkpointing、GPU Acceleration、WebAssembly UDF、Stream-Batch Unification、FLIP-531、MCP Protocol、A2A Protocol；添加版本标注 |
| v1.0 | 2026-04-03 | 初始版本，包含 190+ 术语 |

---

*本文档遵循 AGENTS.md 定义的术语规范，与 THEOREM-REGISTRY.md 中的形式化定义保持一致。*
