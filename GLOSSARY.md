# AnalysisDataFlow 术语表 (Glossary)

> **版本**: v1.0 | **更新日期**: 2026-04-03 | **范围**: 全项目
>
> 本文档是 AnalysisDataFlow 项目的权威术语参考，按字母顺序排列，涵盖流计算理论、Flink 工程实践及前沿技术领域。

---

## 目录

- [术语表导航](#术语表导航)
- [术语分类索引](#术语分类索引)
- [A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [Q](#q) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [W](#w) · [X](#x) · [Y](#y) · [Z](#z)

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

- [流计算相关](#流计算相关): Dataflow, Event Time, Processing Time, Watermark, Window
- [批处理相关](#批处理相关): Batch Processing, Bounded Stream, Checkpoint
- [实时处理相关](#实时处理相关): Real-time Processing, Latency, Throughput

### 2. 理论术语

- [进程演算术语](#进程演算术语): CCS, CSP, π-Calculus, Actor Model, Session Types
- [形式化验证术语](#形式化验证术语): Bisimulation, Model Checking, TLA+, Iris
- [类型理论术语](#类型理论术语): FG/FGG, DOT, Path-Dependent Types

### 3. Flink术语

- [核心概念](#核心概念): JobManager, TaskManager, Operator, State Backend
- [API相关](#api相关): DataStream API, Table API, SQL
- [配置参数](#配置参数): Parallelism, Checkpoint Interval, Watermark Strategy

### 4. 工程术语

- [设计模式术语](#设计模式术语): Windowed Aggregation, Async I/O, Side Output
- [架构术语](#架构术语): Microservices, Event-Driven Architecture, Data Mesh
- [运维术语](#运维术语): Backpressure, Monitoring, Autoscaling

### 5. 前沿术语

- [AI Agent术语](#ai-agent术语): ReAct, MCP, A2A, Agentic Workflow
- [流数据库术语](#流数据库术语): Materialized View, Continuous Query, Incremental Update
- [云原生术语](#云原生术语): Kubernetes, Serverless, WASM, Lakehouse

---

## A

### Actor Model (Actor 模型)

**定义**: 一种并发计算模型，其中计算的基本单元是 Actor——能够接收消息、做出决策、创建新 Actor 和发送消息的自治实体。

**形式化定义**:

```
Actor ::= ⟨Mailbox, Behavior, State, Children, Supervisor⟩
```

**相关概念**: [CSP](#csp-communicating-sequential-processes), [π-Calculus](#π-calculus), [消息传递](#message-passing)

**参考文档**:

- `Struct/01-foundation/01.03-actor-model-formalization.md` (Def-S-03-01)
- `Struct/03-relationships/03.01-actor-to-csp-encoding.md`

---

### AI Agent (人工智能代理)

**定义**: 能够在环境中自主感知、推理、行动和学习的智能系统，形式化为五元组：

```
𝒜_agent ≜ ⟨𝒫, ℛ, 𝒜, ℳ, 𝒢⟩
```

其中 𝒫 为感知，ℛ 为推理，𝒜 为行动，ℳ 为记忆，𝒢 为目标。

**相关概念**: [ReAct](#react), [MCP](#mcp-model-context-protocol), [Multi-Agent](#multi-agent)

**参考文档**:

- `Knowledge/06-frontier/ai-agent-streaming-architecture.md` (Def-K-06-110)
- `Flink/12-ai-ml/flink-agents-flip-531.md` (Def-F-12-30)

---

### A2A Protocol (Agent-to-Agent Protocol)

**定义**: Google 提出的开放 Agent 互操作标准，支持 Agent 间的任务委托、状态同步和结果返回。

**形式化定义**:

```
A2A_Flink = ⟨𝒫, ℳ, 𝒮, 𝒜⟩
```

**相关概念**: [AI Agent](#ai-agent-人工智能代理), [MCP](#mcp-model-context-protocol), [Orchestration](#orchestration)

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

**相关概念**: [Unaligned Checkpoint](#unaligned-checkpoint), [Barrier](#barrier), [Exactly-Once](#exactly-once)

**参考文档**:

- `Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md` (Def-F-02-03)
- `Struct/04-proofs/04.01-flink-checkpoint-correctness.md` (Thm-S-17-01)

---

### Async I/O (异步 I/O)

**定义**: 允许流处理算子并发执行外部系统调用的模式，避免阻塞数据流处理。

**形式化定义**:

```
AsyncFunction: I × C → Future[O]
```

其中 C 为并发度参数，控制同时进行的异步请求数量。

**相关概念**: [Backpressure](#backpressure), [Enrichment](#data-enrichment), [Concurrency](#concurrency)

**参考文档**:

- `Knowledge/02-design-patterns/pattern-async-io-enrichment.md`
- `Flink/02-core-mechanisms/async-execution-model.md`

---

### At-Least-Once (至少一次语义)

**定义**: 流计算系统保证每条输入数据对最终外部世界的影响**至少有一次**的语义。

**形式化定义**:

```
∀r ∈ I. c(r, 𝒯) ≥ 1
```

其中 c(r, 𝒯) 为因果影响计数。

**相关概念**: [At-Most-Once](#at-most-once), [Exactly-Once](#exactly-once), [Delivery Guarantee](#delivery-guarantee)

**参考文档**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-03)

---

### At-Most-Once (至多一次语义)

**定义**: 流计算系统保证每条输入数据对最终外部世界的影响**最多只有一次**的语义，允许数据丢失。

**形式化定义**:

```
∀r ∈ I. c(r, 𝒯) ≤ 1
```

**相关概念**: [At-Least-Once](#at-least-once), [Exactly-Once](#exactly-once), [Best-Effort](#best-effort)

**参考文档**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-02)

---

## B

### Backpressure (反压)

**定义**: 流处理系统中下游处理速度低于上游时，向上游传递的流速控制信号机制。

**原理**: 基于信用值(credit-based)的流量控制，当接收缓冲区满时暂停发送。

**相关概念**: [Flow Control](#flow-control), [Buffer](#buffer), [Credit-Based](#credit-based)

**参考文档**:

- `Flink/02-core-mechanisms/backpressure-and-flow-control.md`
- `Knowledge/09-anti-patterns/anti-pattern-08-ignoring-backpressure.md`

---

### Barrier (Checkpoint Barrier)

**定义**: Flink 中注入到数据流中的特殊控制事件，用于分隔不同 Checkpoint 的数据边界。

**形式化定义**:

```
Barrier(n) = ⟨Type = CONTROL, checkpointId = n, timestamp = ts⟩
```

**相关概念**: [Checkpoint](#checkpoint), [Aligned Checkpoint](#aligned-checkpoint), [Unaligned Checkpoint](#unaligned-checkpoint)

**参考文档**:

- `Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md` (Def-F-02-02)

---

### Batch Processing (批处理)

**定义**: 处理有限、有界数据集的计算模式，数据在计算开始前已完全可用。

**特征**:

- 输入数据有界(Bounded)
- 可访问完整数据集
- 延迟不敏感，追求高吞吐

**相关概念**: [Stream Processing](#stream-processing), [Bounded Stream](#bounded-stream), [Lambda Architecture](#lambda-architecture)

**参考文档**:

- `Struct/01-foundation/01.04-dataflow-model-formalization.md`

---

### Best-Effort (尽力而为)

**定义**: 不提供任何一致性保证的交付语义，系统尽力处理数据但不保证不丢失、不重复。

**相关概念**: [At-Most-Once](#at-most-once), [Delivery Guarantee](#delivery-guarantee)

---

### Bisimulation (互模拟)

**定义**: 进程代数中判断两个进程行为等价的关系，要求两个进程在所有可能的动作上都能相互模拟。

**形式化定义**:

```
R 是互模拟 ⟺ ∀(P,Q)∈R. ∀α. P→αP' ⇒ ∃Q'. Q→αQ' ∧ (P',Q')∈R
```

**相关概念**: [Process Calculus](#process-calculus), [Trace Equivalence](#trace-equivalence), [CCS](#ccs)

**参考文档**:

- `Struct/03-relationships/03.04-bisimulation-equivalences.md` (Thm-S-15-01)

---

### Bounded Stream (有界流)

**定义**: 具有有限数据量的数据流，批处理的数据抽象。

**形式化定义**:

```
Bounded(S) ⟺ |S| < ∞
```

**相关概念**: [Unbounded Stream](#unbounded-stream), [Batch Processing](#batch-processing)

---

### Buffer (缓冲区)

**定义**: 流处理中用于临时存储数据的内存区域，位于生产者和消费者之间。

**相关概念**: [Backpressure](#backpressure), [Queue](#queue), [Network Buffer](#network-buffer)

---

## C

### CALM Theorem (CALM 定理)

**定义**: Consistency As Logical Monotonicity —— 逻辑单调的程序无需协调即可保证一致性。

**形式化表述**:

```
程序 P 无需协调 ⟺ P 是逻辑单调的
```

**相关概念**: [Eventual Consistency](#eventual-consistency), [Coordination](#coordination)

**参考文档**:

- `Struct/02-properties/02.06-calm-theorem.md` (Thm-S-02-08)

---

### Causal Consistency (因果一致性)

**定义**: 分布式系统中保留因果依赖关系操作顺序的一致性模型。

**形式化定义**:

```
∀op_i, op_j. op_i ≺hb op_j ⇒ op_i ≺obs op_j
```

**相关概念**: [Strong Consistency](#strong-consistency), [Eventual Consistency](#eventual-consistency), [Happens-Before](#happens-before)

**参考文档**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-08)

---

### CEP (Complex Event Processing, 复杂事件处理)

**定义**: 从事件流中检测复杂模式并生成复合事件的技术。

**形式化定义**:

```
CEP: Stream × Pattern → DetectedEvents
```

**相关概念**: [Pattern Matching](#pattern-matching), [Event Pattern](#event-pattern), [Window](#window)

**参考文档**:

- `Knowledge/02-design-patterns/pattern-cep-complex-event.md`

---

### CCS (Calculus of Communicating Systems)

**定义**: Milner 于 1980 年提出的基于标签化同步的进程代数。

**语法**:

```
P, Q ::= 0 | α.P | P + Q | P | Q | P \\ L | P[f]
```

**相关概念**: [CSP](#csp), [π-Calculus](#π-calculus), [Process Algebra](#process-algebra)

**参考文档**:

- `Struct/01-foundation/01.02-process-calculus-primer.md` (Def-S-02-01)

---

### CDC (Change Data Capture, 变更数据捕获)

**定义**: 捕获数据库变更事件（插入、更新、删除）并实时传播到下游系统的技术。

**相关概念**: [Debezium](#debezium), [Streaming ETL](#streaming-etl), [Log Mining](#log-mining)

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

**相关概念**: [Savepoint](#savepoint), [State Backend](#state-backend), [Recovery](#recovery)

**参考文档**:

- `Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md` (Def-F-02-01)
- `Struct/04-proofs/04.01-flink-checkpoint-correctness.md` (Thm-S-17-01)

---

### Chandy-Lamport Algorithm

**定义**: 分布式系统中用于捕获全局一致快照的经典算法，Flink Checkpoint 的理论基础。

**相关概念**: [Global Snapshot](#global-snapshot), [Consistent Cut](#consistent-cut), [Checkpoint](#checkpoint)

**参考文档**:

- `Struct/04-proofs/04.03-chandy-lamport-consistency.md` (Thm-S-19-01)

---

### Choreographic Programming (编舞式编程)

**定义**: 一种分布式编程范式，从全局视角描述多方交互协议，然后投影到各参与方。

**相关概念**: [Session Types](#session-types), [Endpoint Projection](#endpoint-projection), [Deadlock Freedom](#deadlock-freedom)

**参考文档**:

- `Struct/06-frontier/06.02-choreographic-streaming-programming.md`
- `Struct/04-proofs/04.07-deadlock-freedom-choreographic.md` (Thm-S-23-01)

---

### Cloud-Native (云原生)

**定义**: 利用云计算优势构建和运行应用程序的方法论，强调容器化、微服务、持续交付和 DevOps。

**相关概念**: [Kubernetes](#kubernetes), [Containerization](#containerization), [Microservices](#microservices)

**参考文档**:

- `Flink/10-deployment/flink-kubernetes-operator-deep-dive.md`
- `Knowledge/06-frontier/serverless-stream-processing-architecture.md`

---

### Concurrency (并发)

**定义**: 多个计算任务在重叠时间段内执行的能力，区别于并行(Parallelism)。

**相关概念**: [Parallelism](#parallelism), [Race Condition](#race-condition), [Synchronization](#synchronization)

---

### Consistency Model (一致性模型)

**定义**: 定义分布式系统中数据操作可见性和顺序性的规则集合。

**层次结构**: Strong Consistency → Causal Consistency → Eventual Consistency

**相关概念**: [Linearizability](#linearizability), [Serializability](#serializability), [CAP Theorem](#cap-theorem)

**参考文档**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Thm-S-08-03)

---

### Continuous Query (持续查询)

**定义**: 流数据库中持续运行、随数据到达自动更新结果的查询。

**形式化定义**:

```
q: S → 𝒱, 其中 q 是时变函数
```

**相关概念**: [Materialized View](#materialized-view), [Streaming Database](#streaming-database)

**参考文档**:

- `Knowledge/06-frontier/streaming-databases.md` (Def-K-06-14)

---

### Coordination (协调)

**定义**: 分布式系统中各节点之间为实现一致行为而进行的通信和同步。

**相关概念**: [CALM Theorem](#calm-theorem), [Consensus](#consensus), [Distributed Transaction](#distributed-transaction)

---

### Credit-Based Flow Control (基于信用的流控)

**定义**: 接收方通过发送信用值(credit)告知发送方可接收的数据量，实现流量控制。

**相关概念**: [Backpressure](#backpressure), [Flow Control](#flow-control)

---

### CSP (Communicating Sequential Processes)

**定义**: Hoare 于 1985 年提出的基于同步通信和静态事件名的进程代数。

**语法**:

```
P, Q ::= STOP | SKIP | a → P | P □ Q | P ⊓ Q | P ||| Q | P |[A]| Q
```

**相关概念**: [CCS](#ccs), [π-Calculus](#π-calculus), [Go Channels](#go-channels)

**参考文档**:

- `Struct/01-foundation/01.05-csp-formalization.md` (Def-S-02-02)
- `Struct/03-relationships/03.01-actor-to-csp-encoding.md` (Thm-S-12-01)

---

## D

### Data Enrichment (数据富化)

**定义**: 将原始数据流与外部数据源关联，补充上下文信息的过程。

**相关概念**: [Async I/O](#async-io), [Lookup Join](#lookup-join), [Dimension Table](#dimension-table)

**参考文档**:

- `Knowledge/02-design-patterns/pattern-async-io-enrichment.md`

---

### Data Mesh (数据网格)

**定义**: 一种去中心化的数据架构范式，将数据视为产品，由领域团队自治管理。

**相关概念**: [Data Product](#data-product), [Domain-Driven Design](#domain-driven-design), [Self-Serve Platform](#self-serve-platform)

**参考文档**:

- `Knowledge/03-business-patterns/data-mesh-streaming-architecture-2026.md`
- `Knowledge/06-frontier/streaming-data-mesh-architecture.md`

---

### Data Product (数据产品)

**定义**: 数据网格中可独立发现、寻址和消费的自治数据单元。

**相关概念**: [Data Mesh](#data-mesh), [Data as a Product](#data-as-a-product)

---

### Dataflow Model (Dataflow 模型)

**定义**: 将计算表示为数据在操作符之间流动的图模型，流计算的核心理论基础。

**形式化定义**:

```
𝒢 = (V, E, P, Σ, 𝕋)
```

其中 V 为顶点集，E 为边集，P 为处理函数，Σ 为状态，𝕋 为时间模型。

**相关概念**: [DAG](#dag-directed-acyclic-graph), [Operator](#operator), [Stream Graph](#stream-graph)

**参考文档**:

- `Struct/01-foundation/01.04-dataflow-model-formalization.md` (Def-S-04-01)
- `Struct/02-properties/02.01-determinism-in-streaming.md` (Thm-S-04-01)

---

### DAG (Directed Acyclic Graph, 有向无环图)

**定义**: 表示数据流处理拓扑的图结构，节点为算子，边为数据流，无循环。

**相关概念**: [Dataflow Model](#dataflow-model), [Job Graph](#job-graph), [Execution Graph](#execution-graph)

---

### Deadlock Freedom (无死锁性)

**定义**: 系统保证不存在任何进程因等待永远不会发生的事件而永久阻塞的性质。

**相关概念**: [Liveness](#liveness), [Choreographic Programming](#choreographic-programming), [Session Types](#session-types)

**参考文档**:

- `Struct/04-proofs/04.07-deadlock-freedom-choreographic.md` (Thm-S-23-01)

---

### Delivery Guarantee (交付保证)

**定义**: 流处理系统对消息传递可靠性的承诺，分为 At-Most-Once、At-Least-Once、Exactly-Once。

**相关概念**: [At-Most-Once](#at-most-once), [At-Least-Once](#at-least-once), [Exactly-Once](#exactly-once)

**参考文档**:

- `Struct/02-properties/02.02-consistency-hierarchy.md`

---

### Determinism (确定性)

**定义**: 给定相同输入，系统总是产生相同输出的性质。

**形式化定义**:

```
Deterministic(P) ⟺ ∀x. P(x) = P(x)
```

**相关概念**: [Reproducibility](#reproducibility), [Consistency](#consistency-model)

**参考文档**:

- `Struct/02-properties/02.01-determinism-in-streaming.md` (Thm-S-07-01)

---

### Differential Dataflow

**定义**: 支持增量计算和递归的流处理模型，基于差分更新传播变化。

**相关概念**: [Incremental Computation](#incremental-computation), [Materialize](#materialize)

---

### Distributed Snapshot (分布式快照)

**定义**: 捕获分布式系统某一时刻全局状态的一致性快照。

**相关概念**: [Chandy-Lamport Algorithm](#chandy-lamport-algorithm), [Checkpoint](#checkpoint), [Consistent Cut](#consistent-cut)

---

### DOT (Dependent Object Types)

**定义**: 支持路径依赖类型和家族多态的高级类型系统，Scala 的理论基础。

**相关概念**: [Path-Dependent Types](#path-dependent-types), [FGG](#fgg), [Subtyping](#subtyping)

**参考文档**:

- `Struct/04-proofs/04.06-dot-subtyping-completeness.md` (Thm-S-22-01)

---

## E

### Edge Computing (边缘计算)

**定义**: 在数据源附近（网络边缘）进行数据处理的计算范式，降低延迟和带宽消耗。

**相关概念**: [Cloud-Edge Continuum](#cloud-edge-continuum), [IoT](#internet-of-things), [Latency](#latency)

**参考文档**:

- `Knowledge/06-frontier/edge-streaming-architecture.md`

---

### End-to-End Consistency (端到端一致性)

**定义**: 从外部数据源到外部数据汇的整个管道的一致性保证。

**形式化定义**:

```
End-to-End-EO(J) ⟺ Replayable(Src) ∧ ConsistentCheckpoint(Ops) ∧ AtomicOutput(Snk)
```

**相关概念**: [Internal Consistency](#internal-consistency), [Exactly-Once](#exactly-once), [Source](#source), [Sink](#sink)

**参考文档**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-05)

---

### Event-Driven Architecture (事件驱动架构)

**定义**: 以事件产生、检测和消费为核心组织组件交互的软件架构模式。

**相关概念**: [Event Streaming](#event-streaming), [Pub/Sub](#publish-subscribe), [CQRS](#cqrs)

---

### Event Pattern (事件模式)

**定义**: CEP 中用于匹配事件序列的模板，支持顺序、选择、重复等运算符。

**相关概念**: [CEP](#cep-complex-event-processing), [Pattern Matching](#pattern-matching)

---

### Event Sourcing (事件溯源)

**定义**: 以事件序列作为系统状态真相来源的持久化模式。

**相关概念**: [CQRS](#cqrs), [Event Store](#event-store), [Audit Log](#audit-log)

---

### Event Streaming (事件流)

**定义**: 持续捕获、处理和响应事件流的计算模式。

**相关概念**: [Stream Processing](#stream-processing), [Event-Driven Architecture](#event-driven-architecture)

---

### Event Time (事件时间)

**定义**: 数据记录产生的时间戳，由数据源赋予。

**形式化定义**:

```
t_e: Record → Timestamp
```

**相关概念**: [Processing Time](#processing-time), [Ingestion Time](#ingestion-time), [Watermark](#watermark)

**参考文档**:

- `Struct/01-foundation/01.01-unified-streaming-theory.md` (Def-S-01-05)
- `Flink/02-core-mechanisms/time-semantics-and-watermark.md`

---

### Eventual Consistency (最终一致性)

**定义**: 保证在没有新更新的情况下，最终所有副本都会收敛到相同值的一致性模型。

**形式化定义**:

```
◇□(replicas converge)
```

**相关概念**: [Strong Consistency](#strong-consistency), [Causal Consistency](#causal-consistency), [CALM Theorem](#calm-theorem)

**参考文档**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-09)

---

### Exactly-Once (精确一次语义)

**定义**: 流计算系统保证每条输入数据对最终外部世界的影响**有且仅有一次**的语义。

**形式化定义**:

```
∀r ∈ I. c(r, 𝒯) = 1
```

**相关概念**: [At-Least-Once](#at-least-once), [At-Most-Once](#at-most-once), [Idempotency](#idempotency)

**参考文档**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-04)
- `Struct/04-proofs/04.02-flink-exactly-once-correctness.md` (Thm-S-18-01)
- `Flink/02-core-mechanisms/exactly-once-semantics-deep-dive.md`

---

### Execution Graph (执行图)

**定义**: Flink 中将逻辑 JobGraph 转换为物理执行计划的图结构，包含具体的并行实例。

**相关概念**: [Job Graph](#job-graph), [Task](#task), [Parallelism](#parallelism)

---

### Explicit State (显式状态)

**定义**: 由用户代码显式声明和管理的流处理状态，Flink 提供 API 支持。

**相关概念**: [Implicit State](#implicit-state), [Keyed State](#keyed-state), [Operator State](#operator-state)

---

## F

### FG (Featherweight Generic)

**定义**: Java 泛型的轻量级形式化模型，用于类型安全证明。

**相关概念**: [FGG](#fgg), [Type Safety](#type-safety), [Java Generics](#java-generics)

**参考文档**:

- `Struct/04-proofs/04.05-type-safety-fg-fgg.md` (Thm-S-21-01)

---

### FGG (Featherweight Generic Go)

**定义**: Go 泛型的轻量级形式化模型。

**相关概念**: [FG](#fg), [Go](#go-language), [Parametric Polymorphism](#parametric-polymorphism)

**参考文档**:

- `Struct/04-proofs/04.05-type-safety-fg-fgg.md` (Thm-S-21-01)

---

### Flink Agent

**定义**: 基于 Flink 流计算框架构建的自主智能体，支持持续感知、决策和行动。

**形式化定义**:

```
𝒜_Flink = ⟨S_state, P_perception, D_decision, A_action, M_memory, G_goal⟩
```

**相关概念**: [AI Agent](#ai-agent-人工智能代理), [Stateful Stream Processing](#stateful-stream-processing)

**参考文档**:

- `Flink/12-ai-ml/flink-agents-flip-531.md` (Def-F-12-30)

---

### Flow Control (流量控制)

**定义**: 调节数据生产者和消费者之间数据传输速率的机制。

**相关概念**: [Backpressure](#backpressure), [Credit-Based](#credit-based-flow-control), [Buffer](#buffer)

---

### ForSt State Backend

**定义**: Flink 2.0 引入的新一代状态后端，基于 RocksDB 改进，支持异步执行模型。

**相关概念**: [State Backend](#state-backend), [RocksDB](#rocksdb), [Incremental Checkpoint](#incremental-checkpoint)

**参考文档**:

- `Flink/02-core-mechanisms/forst-state-backend.md` (Thm-F-02-45)
- `Flink/02-core-mechanisms/flink-2.0-forst-state-backend.md`

---

### Function as a Service (FaaS)

**定义**: 无服务器计算模式，用户编写函数代码，由平台管理基础设施和自动扩缩容。

**相关概念**: [Serverless](#serverless), [Lambda](#lambda-architecture), [Cloud-Native](#cloud-native)

**参考文档**:

- `Knowledge/06-frontier/faas-dataflow.md`
- `Knowledge/06-frontier/serverless-stream-processing-architecture.md`

---

## G

### Global Snapshot (全局快照)

**定义**: 分布式系统某一时刻所有进程状态的集合，用于故障恢复和一致性检查。

**相关概念**: [Distributed Snapshot](#distributed-snapshot), [Chandy-Lamport Algorithm](#chandy-lamport-algorithm), [Checkpoint](#checkpoint)

---

### Global Window (全局窗口)

**定义**: 包含所有记录的单一窗口，通常配合自定义触发器使用。

**形式化定义**:

```
Global: wid_global = (-∞, +∞)
```

**相关概念**: [Tumbling Window](#tumbling-window), [Sliding Window](#sliding-window), [Session Window](#session-window)

**参考文档**:

- `Knowledge/02-design-patterns/pattern-windowed-aggregation.md` (Def-K-02-02)

---

### Go Channels

**定义**: Go 语言中基于 CSP 模型的同步通信原语。

**相关概念**: [CSP](#csp), [Channel](#channel), [Goroutine](#goroutine)

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

**相关概念**: [Causal Consistency](#causal-consistency), [Lamport Clock](#lamport-clock), [Vector Clock](#vector-clock)

---

### HashMapStateBackend

**定义**: Flink 中基于堆内存的状态后端，适用于小状态、低延迟场景。

**相关概念**: [State Backend](#state-backend), [RocksDBStateBackend](#rocksdbstatebackend), [ForSt](#forst-state-backend)

**参考文档**:

- `Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md` (Def-F-02-06)

---

### Hot Key (热键)

**定义**: 数据分布中频率远高于其他键的键，导致数据倾斜和性能瓶颈。

**相关概念**: [Data Skew](#data-skew), [Key Group](#key-group), [Rebalancing](#rebalancing)

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

**相关概念**: [Exactly-Once](#exactly-once), [Idempotent Sink](#idempotent-sink), [Dedup](#deduplication)

---

### Idempotent Sink (幂等 Sink)

**定义**: 能够安全处理重复写入的外部系统接收端，通常基于主键去重。

**相关概念**: [Sink](#sink), [Idempotency](#idempotency), [Exactly-Once](#exactly-once)

---

### Incremental Checkpoint (增量 Checkpoint)

**定义**: 仅捕获自上次 Checkpoint 以来发生变化的状态部分。

**形式化定义**:

```
ΔS_n = S_{t_n} \\ S_{t_{n-1}}, CP_n^inc = ⟨Base, {ΔS_i}_{i=1}^n⟩
```

**相关概念**: [Checkpoint](#checkpoint), [State Backend](#state-backend), [RocksDB](#rocksdb)

**参考文档**:

- `Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md` (Def-F-02-05, Thm-F-02-02)

---

### Incremental Computation (增量计算)

**定义**: 基于输入变化量计算输出变化量的计算模式，避免全量重算。

**形式化定义**:

```
δv = ℱ_q(δD, D), v_new = v ⊕ δv
```

**相关概念**: [Materialized View](#materialized-view), [Differential Dataflow](#differential-dataflow)

---

### Ingestion Time (摄入时间)

**定义**: 数据记录进入流处理系统的时间戳。

**形式化定义**:

```
t_i: Record → Timestamp_system
```

**相关概念**: [Event Time](#event-time), [Processing Time](#processing-time)

---

### Internal Consistency (内部一致性)

**定义**: 流处理引擎自身在故障恢复后，其内部算子状态与全局快照的一致性。

**形式化定义**:

```
Internal-Consistency(Ops) ⟺ ∀k. Consistent(𝒢_k) ∧ NoOrphans(𝒢_k) ∧ Reachable(𝒢_k)
```

**相关概念**: [End-to-End Consistency](#end-to-end-consistency), [Checkpoint](#checkpoint)

**参考文档**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-06)

---

### IoT (Internet of Things, 物联网)

**定义**: 由物理设备、传感器等组成的网络，产生大规模流数据。

**相关概念**: [Edge Computing](#edge-computing), [Sensor Data](#sensor-data), [Stream Processing](#stream-processing)

**参考文档**:

- `Knowledge/03-business-patterns/iot-stream-processing.md`
- `Flink/07-case-studies/case-iot-stream-processing.md`

---

### Iris

**定义**: 基于高阶分离逻辑的并发程序验证框架。

**相关概念**: [Separation Logic](#separation-logic), [Formal Verification](#formal-verification), [Model Checking](#model-checking)

**参考文档**:

- `Struct/07-tools/iris-separation-logic.md`

---

## J

### Job Graph (作业图)

**定义**: Flink 中用户程序编译后的逻辑执行图，表示算子间的数据流关系。

**相关概念**: [Execution Graph](#execution-graph), [DAG](#dag-directed-acyclic-graph), [Operator](#operator)

---

### JobManager

**定义**: Flink 集群中的主控进程，负责任务调度、协调和故障恢复。

**相关概念**: [TaskManager](#taskmanager), [ResourceManager](#resourcemanager), [Dispatcher](#dispatcher)

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

**相关概念**: [Stream Join](#stream-join), [Window Join](#window-join)

**参考文档**:

- `Flink/02-core-mechanisms/delta-join.md`

---

## K

### Key Group (键组)

**定义**: Flink 中 Keyed State 的分区单位，决定状态在并行实例间的分布。

**相关概念**: [Keyed State](#keyed-state), [Parallelism](#parallelism), [State Partitioning](#state-partitioning)

---

### Keyed State (键控状态)

**定义**: 按 Key 分区存储的状态，每个 Key 有独立的状态空间。

**形式化定义**:

```
KeyedState: (K, State[K]) → State[K]
```

**相关概念**: [Operator State](#operator-state), [State Backend](#state-backend), [Key Group](#key-group)

---

### KeyedProcessFunction

**定义**: Flink DataStream API 中访问 Keyed State 和定时器的低级处理函数。

**相关概念**: [ProcessFunction](#processfunction), [Keyed State](#keyed-state), [Timer](#timer)

---

### KeyedStream

**定义**: Flink 中按 Key 分区的数据流，支持 Keyed State 操作。

**相关概念**: [DataStream](#datastream), [Keyed State](#keyed-state), [Partitioning](#partitioning)

---

### Kubernetes

**定义**: 开源容器编排平台，Flink 的主要部署目标。

**相关概念**: [Container](#container), [Operator Pattern](#operator-pattern), [Cloud-Native](#cloud-native)

**参考文档**:

- `Flink/10-deployment/flink-kubernetes-operator-deep-dive.md`
- `Flink/10-deployment/kubernetes-deployment-production-guide.md`

---

## L

### Lakehouse (湖仓一体)

**定义**: 结合数据湖（低成本存储）和数据仓库（高性能分析）优点的架构范式。

**相关概念**: [Delta Lake](#delta-lake), [Iceberg](#apache-iceberg), [Paimon](#apache-paimon)

**参考文档**:

- `Flink/14-lakehouse/streaming-lakehouse-architecture.md`
- `Knowledge/06-frontier/streaming-lakehouse-iceberg-delta.md`

---

### Lambda Architecture (Lambda 架构)

**定义**:  Nathan Marz 提出的批流分离架构，维护批处理层和速度层两套系统。

**相关概念**: [Kappa Architecture](#kappa-architecture), [Batch Processing](#batch-processing), [Stream Processing](#stream-processing)

---

### Latency (延迟)

**定义**: 从事件发生到结果被处理/可见的时间间隔。

**类型**:

- **Processing Latency**: 处理延迟
- **End-to-End Latency**: 端到端延迟
- **Watermark Latency**: Watermark 延迟

**相关概念**: [Throughput](#throughput), [SLA](#sla-service-level-agreement), [Real-time](#real-time)

---

### LSM-Tree (Log-Structured Merge Tree)

**定义**: 写优化的磁盘数据结构，RocksDB 的基础。

**相关概念**: [RocksDB](#rocksdb), [State Backend](#state-backend), [Compaction](#compaction)

---

## M

### Materialized View (物化视图)

**定义**: 预计算并物理存储的查询结果，流数据库中自动增量维护。

**形式化定义**:

```
v = q(D), 当 δD 发生时: v_new = v ⊕ ℱ_q(δD, D)
```

**相关概念**: [View Maintenance](#view-maintenance), [Incremental Computation](#incremental-computation), [Continuous Query](#continuous-query)

**参考文档**:

- `Knowledge/06-frontier/streaming-databases.md` (Def-K-06-13)
- `Flink/03-sql-table-api/materialized-tables.md`

---

### MCP (Model Context Protocol)

**定义**: Anthropic 提出的开放协议，用于标准化 LLM 与外部工具的交互。

**形式化定义**:

```
MCP_Flink = ⟨𝒯, ℛ, 𝒞, ℋ⟩
```

**相关概念**: [AI Agent](#ai-agent-人工智能代理), [Tool Calling](#tool-calling), [A2A](#a2a-protocol)

**参考文档**:

- `Flink/12-ai-ml/flink-agents-flip-531.md` (Def-F-12-32)
- `Knowledge/06-frontier/mcp-protocol-agent-streaming.md`

---

### Message Passing (消息传递)

**定义**: 并发实体间通过发送和接收消息进行通信的模型。

**相关概念**: [Actor Model](#actor-model), [CSP](#csp), [Shared Memory](#shared-memory)

---

### Microservices (微服务)

**定义**: 将应用拆分为小型、自治服务的架构风格，服务间通过 API 通信。

**相关概念**: [Service Mesh](#service-mesh), [Domain-Driven Design](#domain-driven-design), [Cloud-Native](#cloud-native)

---

### Model Checking (模型检测)

**定义**: 自动验证有限状态系统是否满足规约的形式化方法。

**相关概念**: [Formal Verification](#formal-verification), [TLA+](#tla), [State Space](#state-space)

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

**相关概念**: [AI Agent](#ai-agent-人工智能代理), [A2A](#a2a-protocol), [Coordination](#coordination)

**参考文档**:

- `Knowledge/06-frontier/ai-agent-streaming-architecture.md` (Def-K-06-114)

---

## N

### Network Buffer (网络缓冲区)

**定义**: Flink 中用于网络数据传输的内存缓冲区。

**相关概念**: [Buffer](#buffer), [Backpressure](#backpressure), [Credit-Based](#credit-based-flow-control)

---

## O

### Observability (可观测性)

**定义**: 通过系统输出（指标、日志、追踪）理解内部状态的能力。

**三大支柱**:

- **Metrics**: 指标
- **Logs**: 日志
- **Traces**: 分布式追踪

**相关概念**: [Monitoring](#monitoring), [OpenTelemetry](#opentelemetry), [SLA](#sla-service-level-agreement)

**参考文档**:

- `Flink/15-observability/opentelemetry-streaming-observability.md`
- `Flink/15-observability/flink-opentelemetry-observability.md`

---

### OpenTelemetry

**定义**: 开源可观测性框架，提供统一的指标、日志和追踪标准。

**相关概念**: [Observability](#observability), [Metrics](#metrics), [Tracing](#tracing)

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

**相关概念**: [Dataflow Model](#dataflow-model), [Task](#task), [UDF](#user-defined-function)

---

### Operator State (算子状态)

**定义**: 与算子实例绑定的状态，不按 Key 分区。

**相关概念**: [Keyed State](#keyed-state), [Broadcast State](#broadcast-state), [State Backend](#state-backend)

---

### Orchestration (编排)

**定义**: 协调多个服务或组件完成业务流程的模式。

**相关概念**: [Multi-Agent](#multi-agent), [Workflow](#workflow), [Choreography](#choreography)

---

## P

### Parallelism (并行度)

**定义**: 算子或任务的并行执行实例数量。

**形式化定义**:

```
Parallelism(op) = |{instance_i(op)}|
```

**相关概念**: [Slot](#slot), [Task](#task), [Key Group](#key-group)

---

### Path-Dependent Types (路径依赖类型)

**定义**: 依赖于值的类型的类型，如 `x.type` 依赖于 `x` 的值。

**相关概念**: [DOT](#dot-dependent-object-types), [Scala](#scala), [Dependent Types](#dependent-types)

**参考文档**:

- `Struct/06-frontier/06.04-pdot-path-dependent-types.md`

---

### Pattern Matching (模式匹配)

**定义**: 根据数据结构模式进行条件分支的机制。

**相关概念**: [CEP](#cep-complex-event-processing), [Event Pattern](#event-pattern)

---

### Petri Net (Petri 网)

**定义**: 用于建模并发系统的图形化数学模型，由库所(place)和变迁(transition)组成。

**相关概念**: [Process Calculus](#process-calculus), [Concurrency](#concurrency), [Workflow](#workflow)

**参考文档**:

- `Struct/01-foundation/01.06-petri-net-formalization.md` (Thm-S-06-01)

---

### π-Calculus (π 演算)

**定义**: Milner 等人于 1992 年提出的支持名字传递(移动性)的进程代数。

**语法**:

```
P, Q ::= 0 | a(x).P | ā⟨b⟩.P | τ.P | P + Q | P | Q | (νa)P | !P
```

**相关概念**: [CCS](#ccs), [CSP](#csp), [Mobile Processes](#mobile-processes), [Session Types](#session-types)

**参考文档**:

- `Struct/01-foundation/01.02-process-calculus-primer.md` (Def-S-02-03, Thm-S-02-01)

---

### Processing Time (处理时间)

**定义**: 数据记录被算子处理时的机器时间。

**形式化定义**:

```
t_p: () → Timestamp_wall
```

**相关概念**: [Event Time](#event-time), [Ingestion Time](#ingestion-time)

---

### Process Calculus (进程演算)

**定义**: 用于描述并发系统形式化语义的代数框架家族。

**主要成员**: [CCS](#ccs), [CSP](#csp), [π-Calculus](#π-calculus), [Actor Calculus](#actor-model)

**参考文档**:

- `Struct/01-foundation/01.02-process-calculus-primer.md`

---

### ProcessFunction

**定义**: Flink DataStream API 中提供对时间和状态细粒度控制的底层处理函数。

**相关概念**: [KeyedProcessFunction](#keyedprocessfunction), [Timer](#timer), [State](#state)

---

### Progress (进展性)

**定义**: 类型安全性质之一，保证良类型程序不会 stuck（陷入非终止也非错误的状态）。

**相关概念**: [Preservation](#preservation), [Type Safety](#type-safety), [Deadlock Freedom](#deadlock-freedom)

---

### Pub/Sub (发布-订阅)

**定义**: 消息传递模式，发布者发送消息到主题，订阅者接收感兴趣的主题消息。

**相关概念**: [Message Passing](#message-passing), [Kafka](#apache-kafka), [Event Streaming](#event-streaming)

---

## Q

### Query Optimization (查询优化)

**定义**: 自动选择查询执行计划以最小化资源消耗的过程。

**相关概念**: [Calcite](#apache-calcite), [Cost-Based Optimization](#cost-based-optimization), [Rule-Based Optimization](#rule-based-optimization)

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

**相关概念**: [Vector Search](#vector-search), [LLM](#llm), [Knowledge Base](#knowledge-base)

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

**相关概念**: [Latency](#latency), [SLA](#sla-service-level-agreement)

---

### ReAct (Reasoning + Acting)

**定义**: AI Agent 架构模式，交错推理(Thought)和行动(Action)循环解决复杂问题。

**形式化定义**:

```
ReAct: 𝒪_t → Thought → τ_t → Action → a_t → Observation → 𝒪_{t+1}
```

**相关概念**: [AI Agent](#ai-agent-人工智能代理), [Chain-of-Thought](#chain-of-thought)

**参考文档**:

- `Knowledge/06-frontier/ai-agent-streaming-architecture.md` (Def-K-06-111)

---

### Recovery (恢复)

**定义**: 故障后从 Checkpoint 或 Savepoint 重建系统状态的过程。

**相关概念**: [Checkpoint](#checkpoint), [Savepoint](#savepoint), [Failover](#failover)

---

### Replayability (可重放性)

**定义**: 从 Checkpoint 完整重放执行历史的能力，Flink Agent 的核心特性。

**形式化定义**:

```
ℛ_replay = ⟨𝒞, ℒ, ℋ⟩
```

**相关概念**: [Checkpoint](#checkpoint), [Audit](#audit-log), [Debugging](#debugging)

**参考文档**:

- `Flink/12-ai-ml/flink-agents-flip-531.md` (Def-F-12-35)

---

### ResourceManager

**定义**: Flink 中负责集群资源分配和管理的组件。

**相关概念**: [JobManager](#jobmanager), [TaskManager](#taskmanager), [Slot](#slot)

---

### RocksDB

**定义**: Facebook 开发的嵌入式键值存储，基于 LSM-Tree。

**相关概念**: [LSM-Tree](#lsm-tree), [State Backend](#state-backend), [EmbeddedRocksDBStateBackend](#rocksdbstatebackend)

---

### RocksDBStateBackend

**定义**: Flink 中基于 RocksDB 的状态后端，支持大状态、增量 Checkpoint。

**相关概念**: [State Backend](#state-backend), [RocksDB](#rocksdb), [Incremental Checkpoint](#incremental-checkpoint)

**参考文档**:

- `Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md` (Def-F-02-06)

---

## S

### Savepoint (保存点)

**定义**: 用户触发的全局一致快照，用于应用升级、迁移和备份，与 Checkpoint 语义相同但生命周期管理不同。

**相关概念**: [Checkpoint](#checkpoint), [Recovery](#recovery), [Upgrading](#upgrading)

---

### Scala

**定义**: 融合面向对象和函数式编程的 JVM 语言，Flink 的原生 API 语言之一。

**相关概念**: [Type System](#type-system), [Akka](#akka), [JVM](#jvm)

**参考文档**:

- `Flink/09-language-foundations/01.01-scala-types-for-streaming.md`
- `Flink/09-language-foundations/01.03-scala3-type-system-formalization.md`

---

### Scale-Up / Scale-Out (纵向/横向扩展)

**定义**:

- **Scale-Up**: 增强单个节点的计算能力
- **Scale-Out**: 增加节点数量扩展处理能力

**相关概念**: [Elasticity](#elasticity), [Autoscaling](#autoscaling), [Parallelism](#parallelism)

---

### Semantic Matching (语义匹配)

**定义**: 基于语义相似度而非精确值匹配数据的技术，常用于 RAG 和向量搜索。

**相关概念**: [Vector Search](#vector-search), [Embedding](#embedding), [Similarity Search](#similarity-search)

---

### Separation Logic (分离逻辑)

**定义**: 用于推理可变数据结构的逻辑框架，支持局部推理。

**相关概念**: [Iris](#iris), [Formal Verification](#formal-verification), [Concurrent Separation Logic](#concurrent-separation-logic)

**参考文档**:

- `Struct/07-tools/iris-separation-logic.md`

---

### Serverless (无服务器)

**定义**: 云计算执行模型，云提供商动态管理机器资源的分配。

**相关概念**: [FaaS](#function-as-a-service), [Cloud-Native](#cloud-native), [Autoscaling](#autoscaling)

**参考文档**:

- `Knowledge/06-frontier/serverless-stream-processing-architecture.md`
- `Flink/10-deployment/flink-serverless-architecture.md`

---

### Session Types (会话类型)

**定义**: 描述通信协议结构的类型系统，保证通信安全和无死锁。

**形式化定义**:

```
S ::= !T.S | ?T.S | ⊕{l_i: S_i} | &{l_i: S_i} | end
```

**相关概念**: [Type Safety](#type-safety), [Deadlock Freedom](#deadlock-freedom), [Protocol Compliance](#protocol-compliance)

**参考文档**:

- `Struct/01-foundation/01.07-session-types.md` (Thm-S-01-03, Thm-S-01-04)

---

### Session Window (会话窗口)

**定义**: 根据活动间隙动态划分的窗口，无活动超过 gap 后关闭。

**形式化定义**:

```
Session(g, r₁, r₂, ...): wid = [t_first, t_last + g)
```

**相关概念**: [Tumbling Window](#tumbling-window), [Sliding Window](#sliding-window), [Window](#window)

**参考文档**:

- `Knowledge/02-design-patterns/pattern-windowed-aggregation.md` (Def-K-02-02)

---

### Shared Memory (共享内存)

**定义**: 多个并发实体访问同一内存区域的通信模型，区别于消息传递。

**相关概念**: [Message Passing](#message-passing), [Race Condition](#race-condition), [Synchronization](#synchronization)

---

### Side Output (侧输出)

**定义**: 从主流分离特定数据到旁路流的机制，用于处理迟到数据或异常。

**相关概念**: [Late Data](#late-data), [Data Splitting](#data-splitting), [Main Stream](#main-stream)

**参考文档**:

- `Knowledge/02-design-patterns/pattern-side-output.md`

---

### Sink (数据汇)

**定义**: 流处理中将数据写入外部系统的组件。

**相关概念**: [Source](#source), [Connector](#connector), [Exactly-Once](#exactly-once)

---

### Sliding Window (滑动窗口)

**定义**: 固定大小、按固定步长滑动的窗口，窗口间可能重叠。

**形式化定义**:

```
Sliding(δ, s): wid_n = [n·s, n·s + δ)
```

**相关概念**: [Tumbling Window](#tumbling-window), [Session Window](#session-window), [Window](#window)

---

### Slot

**定义**: Flink TaskManager 中资源分配的基本单位，一个 Task Slot 可执行一个任务链。

**相关概念**: [TaskManager](#taskmanager), [Task](#task), [Resource](#resource)

---

### Source (数据源)

**定义**: 流处理中从外部系统读取数据的组件。

**相关概念**: [Sink](#sink), [Connector](#connector), [Offset](#offset)

---

### Source Split (源分片)

**定义**: 数据源的可并行读取单元，如 Kafka 的 partition。

**相关概念**: [Source](#source), [Parallelism](#parallelism), [Partition](#partition)

---

### Split-Level Watermark

**定义**: 在 Source Split 级别生成 Watermark 的机制，支持更精细的流控制。

**相关概念**: [Watermark](#watermark), [Source Split](#source-split)

**参考文档**:

- `Flink/15-observability/split-level-watermark-metrics.md`

---

### SQL/Table API

**定义**: Flink 提供的声明式 API，支持标准 SQL 和 Table DSL。

**相关概念**: [DataStream API](#datastream-api), [Query Optimization](#query-optimization), [Calcite](#apache-calcite)

**参考文档**:

- `Flink/03-sql-table-api/sql-vs-datastream-comparison.md`

---

### State (状态)

**定义**: 流处理中跨记录保持的数据，是有状态计算的基础。

**分类**:

- **Keyed State**: 键控状态
- **Operator State**: 算子状态
- **Broadcast State**: 广播状态

**相关概念**: [Stateful Processing](#stateful-stream-processing), [State Backend](#state-backend)

---

### State Backend (状态后端)

**定义**: 负责状态存储、访问和快照持久化的运行时组件。

**实现类型**:

- **HashMapStateBackend**: 内存存储
- **EmbeddedRocksDBStateBackend**: 磁盘存储
- **ForStStateBackend**: Flink 2.0 新一代后端

**相关概念**: [State](#state), [Checkpoint](#checkpoint), [Recovery](#recovery)

**参考文档**:

- `Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md` (Def-F-02-06)
- `Flink/06-engineering/state-backend-selection.md`

---

### Stateful Stream Processing (有状态流处理)

**定义**: 维护和使用跨记录状态的流计算模式。

**形式化定义**:

```
F: (K, V) × State[K] → State[K] × O
```

**相关概念**: [Stateless Processing](#stateless-processing), [State](#state), [Keyed State](#keyed-state)

---

### State Partitioning (状态分区)

**定义**: 将 Keyed State 分布到多个并行实例的策略。

**相关概念**: [Key Group](#key-group), [Parallelism](#parallelism), [Keyed State](#keyed-state)

---

### State TTL (状态生存时间)

**定义**: 为状态设置过期时间，自动清理过期数据。

**相关概念**: [State](#state), [Cleanup](#cleanup), [Expiration](#expiration)

**参考文档**:

- `Flink/02-core-mechanisms/flink-state-ttl-best-practices.md`

---

### Stateless Processing (无状态处理)

**定义**: 不维护跨记录状态的流计算模式，每条记录独立处理。

**形式化定义**:

```
F: I → O (纯函数)
```

**相关概念**: [Stateful Processing](#stateful-stream-processing), [Pure Function](#pure-function)

---

### Stream Graph (流图)

**定义**: Flink 程序最初生成的逻辑执行图，表示用户定义的数据流转换。

**相关概念**: [Job Graph](#job-graph), [Execution Graph](#execution-graph), [Dataflow](#dataflow-model)

---

### Stream Join (流 Join)

**定义**: 将两个流按关联条件合并的操作，需处理无界性挑战。

**相关概念**: [Join](#join), [Window Join](#window-join), [Interval Join](#interval-join)

---

### Stream Processing (流处理)

**定义**: 处理无界、持续到达数据流的计算模式。

**特征**:

- 数据无界(Unbounded)
- 持续计算
- 低延迟要求

**相关概念**: [Batch Processing](#batch-processing), [Event Stream](#event-streaming), [Real-Time](#real-time)

---

### Streaming Database (流数据库)

**定义**: 专为连续数据流设计的数据库系统，支持持续查询和物化视图增量维护。

**形式化定义**:

```
𝒮𝒟 = (S, 𝒬, 𝒱, Δ, τ)
```

**相关概念**: [Materialized View](#materialized-view), [Continuous Query](#continuous-query), [RisingWave](#risingwave)

**参考文档**:

- `Knowledge/06-frontier/streaming-databases.md` (Def-K-06-12)
- `Knowledge/04-technology-selection/streaming-database-guide.md`

---

### Streaming ETL (流式 ETL)

**定义**: 以流方式持续执行抽取(Extract)、转换(Transform)、加载(Load)的数据集成模式。

**相关概念**: [CDC](#cdc-change-data-capture), [Data Pipeline](#data-pipeline), [Real-Time Analytics](#real-time-analytics)

**参考文档**:

- `Flink/02-core-mechanisms/streaming-etl-best-practices.md`

---

### Strong Consistency (强一致性)

**定义**: 所有操作在全局历史上存在唯一线性化点，外部观察者看到的顺序与真实时间一致。

**形式化定义**:

```
∀op_i, op_j. t_real(op_i) ≺ t_real(op_j) ⟹ op_i ≺_S op_j
```

**相关概念**: [Linearizability](#linearizability), [Causal Consistency](#causal-consistency), [Eventual Consistency](#eventual-consistency)

**参考文档**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-07)

---

### Subtyping (子类型)

**定义**: 类型系统中，若类型 S 的值可在任何期望类型 T 的上下文中使用，则 S 是 T 的子类型。

**形式化定义**:

```
S <: T ⟺ ∀v: S. v: T
```

**相关概念**: [Type System](#type-system), [Variance](#variance), [DOT](#dot-dependent-object-types)

---

## T

### Table API

**定义**: Flink 提供的基于 Table 的声明式 API，类型安全的 SQL 替代。

**相关概念**: [SQL](#sql), [DataStream API](#datastream-api), [Calcite](#apache-calcite)

---

### Task (任务)

**定义**: Flink 执行图中的基本执行单元，对应算子的一个并行实例。

**相关概念**: [Operator](#operator), [Subtask](#subtask), [TaskManager](#taskmanager)

---

### TaskManager

**定义**: Flink 集群中的工作进程，负责执行具体的数据处理任务。

**相关概念**: [JobManager](#jobmanager), [Slot](#slot), [Task](#task)

---

### TEE (Trusted Execution Environment, 可信执行环境)

**定义**: 处理器中的安全区域，保证代码和数据的机密性和完整性。

**相关概念**: [Confidential Computing](#confidential-computing), [Security](#security), [Privacy](#privacy)

**参考文档**:

- `Flink/13-security/trusted-execution-flink.md`
- `Flink/13-security/gpu-confidential-computing.md`

---

### TLA+

**定义**: Leslie Lamport 开发的形式化规约语言，用于描述和验证并发和分布式系统。

**相关概念**: [Model Checking](#model-checking), [Formal Verification](#formal-verification), [Temporal Logic](#temporal-logic)

**参考文档**:

- `Struct/07-tools/tla-for-flink.md`

---

### Timer (定时器)

**定义**: Flink ProcessFunction 中用于在特定时间点触发回调的机制。

**类型**:

- **Event Time Timer**: 基于事件时间
- **Processing Time Timer**: 基于处理时间

**相关概念**: [ProcessFunction](#processfunction), [Event Time](#event-time), [Window](#window)

---

### Tool Calling (工具调用)

**定义**: LLM 调用外部 API 或函数的能力，AI Agent 的核心能力。

**相关概念**: [MCP](#mcp-model-context-protocol), [Function Calling](#function-calling), [AI Agent](#ai-agent-人工智能代理)

---

### Trace Equivalence (迹等价)

**定义**: 两个进程如果可以执行相同的动作序列则迹等价。

**形式化定义**:

```
P ≈_T Q ⟺ traces(P) = traces(Q)
```

**相关概念**: [Bisimulation](#bisimulation), [Process Calculus](#process-calculus), [CCS](#ccs)

---

### Trigger (触发器)

**定义**: 决定窗口何时输出计算结果的谓词函数。

**形式化定义**:

```
Trigger: WindowID × 𝕋_watermark × State → {FIRE, CONTINUE, PURGE}
```

**相关概念**: [Window](#window), [Evictor](#evictor), [Watermark](#watermark)

**参考文档**:

- `Knowledge/02-design-patterns/pattern-windowed-aggregation.md` (Def-K-02-03)

---

### Tumbling Window (滚动窗口)

**定义**: 固定大小、不重叠的窗口，每条记录精确属于一个窗口。

**形式化定义**:

```
Tumbling(δ): wid_n = [nδ, (n+1)δ)
```

**相关概念**: [Sliding Window](#sliding-window), [Session Window](#session-window), [Window](#window)

**参考文档**:

- `Knowledge/02-design-patterns/pattern-windowed-aggregation.md` (Def-K-02-02)

---

### Type Safety (类型安全)

**定义**: 程序执行过程中不会出现类型错误的保证，由 Progress + Preservation 组成。

**形式化定义**:

```
Type Safety = Progress ∧ Preservation
```

**相关概念**: [Progress](#progress), [Preservation](#preservation), [Type System](#type-system)

**参考文档**:

- `Struct/02-properties/02.05-type-safety-derivation.md` (Thm-S-11-01)

---

### Type System (类型系统)

**定义**: 编程语言中用于分类表达式、避免运行时错误的逻辑系统。

**相关概念**: [Type Safety](#type-safety), [Subtyping](#subtyping), [Polymorphism](#polymorphism)

---

## U

### USTM (Unified Streaming Theory Model)

**定义**: 统一流计算元模型，整合 Actor、CSP、Dataflow、Petri 网四大范式。

**形式化定义**:

```
USTM ::= (ℒ, ℳ, 𝒫, 𝒞, 𝒮, 𝒯, Σ, Φ)
```

**相关概念**: [Dataflow Model](#dataflow-model), [Actor Model](#actor-model), [CSP](#csp)

**参考文档**:

- `Struct/01-foundation/01.01-unified-streaming-theory.md` (Def-S-01-01)

---

### Unaligned Checkpoint (非对齐 Checkpoint)

**定义**: 算子在收到**任意**输入通道的 Barrier 时立即触发快照，将其他通道未处理的记录作为状态保存。

**形式化定义**:

```
UnalignedSnapshot(t, n) ⟺ ∃c ∈ Inputs(t): Barrier(n) ∈ Received(c)
```

**相关概念**: [Aligned Checkpoint](#aligned-checkpoint), [Barrier](#barrier), [In-Flight Data](#in-flight-data)

**参考文档**:

- `Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md` (Def-F-02-04)

---

### Unbounded Stream (无界流)

**定义**: 数据量理论上无限的数据流，流处理的主要数据抽象。

**形式化定义**:

```
Unbounded(S) ⟺ |S| = ∞
```

**相关概念**: [Bounded Stream](#bounded-stream), [Stream Processing](#stream-processing)

---

## V

### Vector Search (向量搜索)

**定义**: 基于向量相似度而非精确匹配的数据检索技术，用于 RAG 和语义搜索。

**形式化定义**:

```
Search(q, V, k) = TopK(Embed(q), V, k)
```

**相关概念**: [RAG](#rag-retrieval-augmented-generation), [Embedding](#embedding), [Similarity Search](#similarity-search)

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

**相关概念**: [Materialized View](#materialized-view), [Incremental Computation](#incremental-computation)

---

## W

### WASM (WebAssembly)

**定义**: 面向 Web 的二进制指令格式，也可用于服务器端计算。

**相关概念**: [WASI](#wasi), [Serverless](#serverless), [UDF](#user-defined-function)

**参考文档**:

- `Flink/13-wasm/wasm-streaming.md`
- `Flink/09-language-foundations/09-wasm-udf-frameworks.md`

---

### WASI

**定义**: WebAssembly System Interface，提供 WASM 模块与系统资源交互的标准接口。

**相关概念**: [WASM](#wasm), [Component Model](#component-model)

**参考文档**:

- `Flink/13-wasm/wasi-0.3-async-preview.md`
- `Flink/09-language-foundations/10-wasi-component-model.md`

---

### Watermark (水印)

**定义**: 流处理中用于衡量事件时间进展的特殊标记，表示特定时间戳之前的数据已到达。

**形式化定义**:

```
Watermark(t_w) ::= ∀e ∈ Stream. t_e(e) ≤ t_w ∨ late(e)
```

**相关概念**: [Event Time](#event-time), [Window](#window), [Late Data](#late-data)

**参考文档**:

- `Struct/02-properties/02.03-watermark-monotonicity.md` (Thm-S-09-01)
- `Struct/04-proofs/04.04-watermark-algebra-formal-proof.md` (Thm-S-20-01)
- `Flink/02-core-mechanisms/time-semantics-and-watermark.md`

---

### Window (窗口)

**定义**: 将无界流切分为有限时间桶进行计算的抽象。

**类型**:

- [Tumbling Window](#tumbling-window)
- [Sliding Window](#sliding-window)
- [Session Window](#session-window)
- [Global Window](#global-window)

**形式化定义**:

```
Window(S, ω) = {S_w : w ∈ ω}, S_w = {e ∈ S | e.time ∈ w}
```

**相关概念**: [Window Assigner](#window-assigner), [Trigger](#trigger), [Evictor](#evictor)

**参考文档**:

- `Knowledge/02-design-patterns/pattern-windowed-aggregation.md` (Def-K-02-01, Def-K-02-02)

---

### Window Assigner (窗口分配器)

**定义**: 将流中每条记录映射到一组时间窗口的函数。

**形式化定义**:

```
Assigner: 𝒟 × 𝕋 → 𝒫(WindowID)
```

**相关概念**: [Window](#window), [Trigger](#trigger), [Event Time](#event-time)

---

### Windowed Aggregation (窗口聚合)

**定义**: 将无界数据流切分为有限窗口进行聚合计算的设计模式。

**相关概念**: [Window](#window), [Aggregation](#aggregation), [Trigger](#trigger)

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
| v1.0 | 2026-04-03 | 初始版本，包含 190+ 术语 |

---

*本文档遵循 AGENTS.md 定义的术语规范，与 THEOREM-REGISTRY.md 中的形式化定义保持一致。*
