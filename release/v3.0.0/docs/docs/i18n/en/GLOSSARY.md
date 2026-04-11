---
title: "AnalysisDataFlow Glossary"
source_file: "GLOSSARY.md"
source_version: "v3.3.0"
translation_status: "completed"
completion_percentage: 100
language: "en"
last_sync: "2026-04-08T09:52:41Z"
---

# AnalysisDataFlow Glossary

> **Version**: v1.1 | **Last Updated**: 2026-04-08 | **Scope**: Full Project
>
> **Version Notes**: Terms marked with [2.0], [2.4], [2.5], [3.0] indicate introduction or core feature in corresponding Flink versions
>
> This document is the authoritative terminology reference for the AnalysisDataFlow project, arranged alphabetically, covering stream computing theory, Flink engineering practice, and frontier technology domains.
>
> 🌐 **中文版** | **English Version**

---

## Table of Contents

- [Glossary Navigation](#glossary-navigation)
- [Term Category Index](#term-category-index)
- [A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [Q](#q) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [W](#w) · [X](#x)

---

## Glossary Navigation

| Category | Term Count | Main Domain |
|----------|------------|-------------|
| [Basic Terms](#1-basic-terms) | 35+ | Stream Computing, Batch Processing, Real-time Processing |
| [Theoretical Terms](#2-theoretical-terms) | 40+ | Process Calculus, Formal Verification, Type Theory |
| [Flink Terms](#3-flink-terms) | 50+ | Core Concepts, APIs, Configuration Parameters |
| [Engineering Terms](#4-engineering-terms) | 30+ | Design Patterns, Architecture, Operations |
| [Frontier Terms](#5-frontier-terms) | 35+ | AI Agents, Streaming Databases, Cloud Native |

---

## Term Category Index

### 1. Basic Terms

- **Stream Computing Related**: Dataflow, Event Time, Processing Time, Watermark, Window
- **Batch Processing Related**: Batch Processing, Bounded Stream, Checkpoint
- **Real-time Processing Related**: Real-time Processing, Latency, Throughput

### 2. Theoretical Terms

- **Process Calculus Terms**: CCS, CSP, π-Calculus, Actor Model, Session Types
- **Formal Verification Terms**: Bisimulation, Model Checking, TLA+, Iris
- **Type Theory Terms**: FG/FGG, DOT, Path-Dependent Types

### 3. Flink Terms

- **Core Concepts**: JobManager, TaskManager, Operator, State Backend
- **API Related**: DataStream API, Table API, SQL
- **Configuration Parameters**: Parallelism, Checkpoint Interval, Watermark Strategy

### 4. Engineering Terms

- **Design Pattern Terms**: Windowed Aggregation, Async I/O, Side Output
- **Architecture Terms**: Microservices, Event-Driven Architecture, Data Mesh
- **Operations Terms**: Backpressure, Monitoring, Autoscaling

### 5. Frontier Terms

- **AI Agent Terms**: AI Agent, ReAct, MCP, A2A, Agentic Workflow, FLIP-531, Tool Calling
- **Serverless Terms**: Serverless Flink, Scale-to-Zero, FaaS
- **Performance Optimization Terms**: Adaptive Execution Engine, Smart Checkpointing, GPU Acceleration
- **Stream-Batch Unification Terms**: Stream-Batch Unification, Unified Execution Engine
- **WASM Terms**: WebAssembly UDF, WASI, WASM
- **Streaming Database Terms**: Materialized View, Continuous Query, Incremental Update
- **Cloud Native Terms**: Kubernetes, Serverless, WASM, Lakehouse

---

## A

### Adaptive Execution Engine (AEE) [Flink 1.17+]

**Definition**: Flink's intelligent execution optimization framework that can dynamically adjust execution plans, resource allocation, and parallelism based on runtime statistics.

**Formal Definition**:

```
AEE-V2 = (𝒫, ℳ, 𝒜, 𝒞, ℛ, δ, π)
```

Where 𝒫 is physical execution plan, ℳ is runtime metrics, 𝒜 is adaptive actions, 𝒞 is constraints, ℛ is re-optimizer, δ is decision function, π is performance prediction model.

**Core Capabilities**: Automatic data skew handling, dynamic parallelism adjustment, adaptive resource allocation

**Related Concepts**: Smart Checkpointing, Backpressure, Parallelism

**Reference Documents**:

- `Flink/02-core-mechanisms/adaptive-execution-engine-v2.md` (Def-F-02-87, Thm-F-02-56)

---

### Actor Model

**Definition**: A concurrent computing model where the basic unit of computation is an Actor—an autonomous entity capable of receiving messages, making decisions, creating new Actors, and sending messages.

**Formal Definition**:

```
Actor ::= ⟨Mailbox, Behavior, State, Children, Supervisor⟩
```

**Related Concepts**: CSP, π-Calculus, Message Passing

**Reference Documents**:

- `Struct/01-foundation/01.03-actor-model-formalization.md` (Def-S-03-01)
- `Struct/03-relationships/03.01-actor-to-csp-encoding.md`

---

### AI Agent

**Definition**: An intelligent system capable of autonomous perception, reasoning, action, and learning in an environment, formalized as a six-tuple:

```
𝒜_agent ≜ ⟨𝒮, 𝒫, 𝒟, 𝒜, ℳ, 𝒢⟩
```

Where 𝒮 is state space, 𝒫 is perception, 𝒟 is decision-making, 𝒜 is action, ℳ is memory, 𝒢 is goal.

**Flink Integration**: Flink Agent is an AI Agent implementation based on stream computing frameworks

**Related Concepts**: ReAct, MCP, A2A, Multi-Agent, FLIP-531

**Reference Documents**:

- `Knowledge/06-frontier/ai-agent-streaming-architecture.md` (Def-K-06-110)
- `Flink/12-ai-ml/flink-agents-flip-531.md` (Def-F-12-30)

---

### A2A Protocol (Agent-to-Agent Protocol) [Google 2025]

**Definition**: Google's open Agent interoperability standard supporting task delegation, state synchronization, and result return between Agents.

**Formal Definition**:

```
A2A_Flink = ⟨𝒫, ℳ, 𝒮, 𝒜⟩
```

Where 𝒫 is participating Agent set, ℳ is message types, 𝒮 is session state machine, 𝒜 is authentication/authorization mechanism.

**Task State Flow**: `pending → working → input-required → completed/failed`

**Related Concepts**: AI Agent, MCP, Orchestration, FLIP-531

**Reference Documents**:

- `Flink/12-ai-ml/flink-agents-flip-531.md` (Def-F-12-33)
- `Knowledge/06-frontier/a2a-protocol-agent-communication.md`

---

### Aligned Checkpoint

**Definition**: In Flink, the mechanism where operators trigger state snapshots only after receiving **all** input channel Barriers.

**Formal Definition**:

```
AlignedSnapshot(t, n) ⟺ ∀c ∈ Inputs(t): Barrier(n) ∈ Received(c)
```

**Related Concepts**: Unaligned Checkpoint, Barrier, Exactly-Once

**Reference Documents**:

- `Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md` (Def-F-02-03)
- `Struct/04-proofs/04.01-flink-checkpoint-correctness.md` (Thm-S-17-01)

---

### Async I/O

**Definition**: A pattern allowing stream processing operators to concurrently execute external system calls, avoiding blocking data stream processing.

**Formal Definition**:

```
AsyncFunction: I × C → Future[O]
```

Where C is concurrency parameter controlling simultaneous async requests.

**Related Concepts**: Backpressure, Enrichment, Concurrency

**Reference Documents**:

- `Knowledge/02-design-patterns/pattern-async-io-enrichment.md`
- `Flink/02-core-mechanisms/async-execution-model.md`

---

### At-Least-Once

**Definition**: Stream computing semantics guaranteeing each input data's effect on the external world occurs **at least once**.

**Formal Definition**:

```
AtLeastOnce(e) ⟹ Count(effect(e)) ≥ 1
```

**Implementation Mechanism**: Retry/Replay

**Applicable Scenarios**: Recommendation systems, statistics

**Related Concepts**: At-Most-Once, Exactly-Once

---

### At-Most-Once

**Definition**: Stream computing semantics guaranteeing each input data's effect on the external world occurs **at most once**.

**Formal Definition**:

```
AtMostOnce(e) ⟹ Count(effect(e)) ≤ 1
```

**Implementation Mechanism**: Deduplication/Idempotency

**Applicable Scenarios**: Log aggregation, monitoring

---

## B

### Backpressure

**Definition**: A mechanism where consumers provide feedback to producers about processing capacity.

**Formal Definition**:

```
Backpressure(t) = 1 - (Throughput(t) / InputRate(t))
```

When Backpressure > threshold, flow control is triggered.

**Related Concepts**: Credit-based Flow Control, Buffer Management

---

### Barrier

**Definition**: Special control events injected by Flink's Checkpoint Coordinator that flow through the dataflow graph to trigger consistent state snapshots.

**Formal Definition**:

```
Barrier(n) ::= ⟨type = CHECKPOINT_BARRIER, checkpointId = n, timestamp⟩
```

**Related Concepts**: Checkpoint, Aligned Checkpoint, Unaligned Checkpoint

---

### Batch Processing

**Definition**: Computing paradigm processing bounded datasets offline.

**Formal Definition**:

```
BatchJob = ⟨D, f, t⟩
  where D is bounded dataset, f is transformation function, t is trigger time
```

**Related Concepts**: Stream Processing, Bounded Stream

---

### Bisimulation

**Definition**: A method for verifying process equivalence relations.

**Formal Definition**:

```
P ~ Q ⟺ ∃R. R is bisimulation ∧ (P, Q) ∈ R
```

Where R is a symmetric binary relation satisfying bisimulation conditions.

**Related Concepts**: Trace Equivalence, Process Calculus

---

### Bounded Stream

**Definition**: A data stream with definite start and end.

**Formal Definition**:

```
BoundedStream = ⟨S, E, {e₁, ..., eₙ}⟩
  where S is start time, E is end time, n is finite
```

**Related Concepts**: Unbounded Stream, Batch Processing

---

## C

### CALM Theorem (Consistency As Logical Monotonicity)

**Definition**: A theorem stating that consistency can be achieved without coordination in logically monotonic programs.

**Formal Statement**:

```
Monotonic(Program) ⟹ CoordinationFree(Program) ∧ EventuallyConsistent(Program)
```

**Reference Documents**:

- `Struct/02-properties/02.06-calm-theorem.md` (Thm-S-06-01)

---

### CEP (Complex Event Processing)

**Definition**: Technology for detecting complex patterns from event streams.

**Formal Definition**:

```
CEP = ⟨Pattern, InputStream, OutputStream, Window⟩
Pattern ::= Sequence | Parallel | Negation | Iteration
```

---

### Checkpoint

**Definition**: A globally consistent snapshot of distributed system state.

**Formal Definition**:

```
Checkpoint = ⟨G, 𝒮, 𝒞, t⟩
  where G is global state, 𝒮 is operator states, 𝒞 is checkpoint coordinator, t is timestamp
```

**Related Concepts**: Savepoint, State Backend, Exactly-Once

---

### Choreographic Programming

**Definition**: A programming paradigm describing distributed system interactions from a global perspective.

**Related Concepts**: Session Types, Multi-Party Session Types (MPST)

---

### Cloud Native

**Definition**: Architectural approach leveraging cloud computing characteristics (elasticity, distributed, automated management).

**Related Concepts**: Kubernetes, Serverless, Microservices

---

### Consistency Hierarchy

**Definition**: Classification of consistency levels from weak to strong.

**Hierarchy**:

```
Linearizability > Sequential Consistency > Causal Consistency > Eventual Consistency
```

**Reference Documents**:

- `Struct/02-properties/02.02-consistency-hierarchy.md`

---

### CSP (Communicating Sequential Processes)

**Definition**: A formal language for concurrency proposed by Hoare.

**Formal Definition**:

```
P ::= STOP | SKIP | a → P | P ⊓ Q | P □ Q | P ∥ Q | P ; Q | P \ A
```

**Related Concepts**: CCS, π-Calculus, Process Algebra

---

## D

### Dataflow Model

**Definition**: A computational model describing data processing as directed graphs.

**Formal Definition**:

```
DataflowGraph = ⟨V, E, Op, S⟩
  where V is vertices (operators), E is edges (data streams), Op is operator semantics, S is stream semantics
```

**Reference Documents**:

- `Struct/01-foundation/01.04-dataflow-model-formalization.md`

---

### Data Mesh

**Definition**: Decentralized data architecture treating data as products owned by domain teams.

**Four Principles**: Domain Ownership, Data as Product, Self-serve Platform, Federated Governance

---

### Determinism

**Definition**: Property where the same input always produces the same output.

**Formal Definition**:

```
Deterministic(f) ⟺ ∀x, y. x = y ⟹ f(x) = f(y)
```

---

### Distributed Snapshot

**Definition**: Consistent state capture of a distributed system at a specific moment.

**Related Concepts**: Chandy-Lamport Algorithm, Checkpoint

---

## E

### Edge Computing

**Definition**: Processing data near the data source rather than in centralized data centers.

**Related Concepts**: IoT, Fog Computing, Cloud-Edge Continuum

---

### Event Time

**Definition**: Timestamp when data is generated.

**Formal Definition**:

```
EventTime(e) = Timestamp when event e occurred at source
```

**Related Concepts**: Processing Time, Ingestion Time, Watermark

---

### Exactly-Once

**Definition**: Stream computing semantics guaranteeing each input data's effect on the external world occurs **exactly once**.

**Formal Definition**:

```
ExactlyOnce(e) ⟹ Count(effect(e)) = 1
```

**Implementation Mechanism**: Replayable Source + Checkpoint + Transactional Sink

**Applicable Scenarios**: Financial transactions, order processing

---

### Expressiveness Hierarchy

**Definition**: Six-layer computational model expressiveness hierarchy.

**Hierarchy**:

```
L₆: Turing-Complete (Undecidable) ── λ-calculus, Turing Machine
L₅: Higher-Order (Mostly Undecidable) ── HOπ, Ambient
L₄: Mobile (Partially Undecidable) ── π-calculus, Actor
L₃: Process Algebra (EXPTIME) ── CSP, CCS
L₂: Context-Free (PSPACE) ── PDA, BPA
L₁: Regular (P-Complete) ── FSM, Regex
```

**Reference Documents**:

- `Struct/03-relationships/03.03-expressiveness-hierarchy.md`

---

## F

### Fault Tolerance

**Definition**: System ability to continue operation when components fail.

**Flink Implementation**: Checkpoint + State Backend + Restart Strategy

---

### Feature Store

**Definition**: Centralized storage and management system for ML features.

**Components**: Online Store, Offline Store, Feature Registry, Feature Serving

---

### Flink

**Definition**: Apache Flink is an open-source stream processing framework with high throughput, low latency, and exactly-once semantics.

**Core Components**: JobManager, TaskManager, Checkpoint Coordinator, State Backend

---

### FLIP (Flink Improvement Proposal)

**Definition**: Flink community's process for proposing major feature improvements.

**Related Concepts**: FLIP-531 (AI Agents)

---

## G

### Global State

**Definition**: Combined state of all processes in a distributed system.

**Formal Definition**:

```
GlobalState(t) = ⋃ᵢ LocalState(pᵢ, t)
```

---

## H

### High Availability (HA)

**Definition**: System ability to remain operational with high probability.

**Flink Implementation**: JobManager HA, Kubernetes HA mode

---

## I

### Incremental Checkpoint

**Definition**: Checkpoint mechanism only persisting state changes since last checkpoint.

**Advantage**: Reduces checkpoint duration and storage requirements

---

### Ingestion Time

**Definition**: Timestamp when data enters the stream processing system.

**Related Concepts**: Event Time, Processing Time

---

## J

### JobManager

**Definition**: Flink cluster's master process responsible for scheduling and coordination.

**Responsibilities**: Job scheduling, checkpoint coordination, resource management

---

## K

### Kafka

**Definition**: Apache Kafka is a distributed streaming platform.

**Core Concepts**: Topic, Partition, Offset, Consumer Group

---

### Kubernetes (K8s)

**Definition**: Open-source container orchestration platform.

**Flink Integration**: Flink Kubernetes Operator, Native K8s mode

---

## L

### Lakehouse

**Definition**: Architecture combining data lake and data warehouse advantages.

**Key Technologies**: Delta Lake, Apache Iceberg, Apache Hudi, Apache Paimon

---

### Latency

**Definition**: Time delay from data generation to processing result.

**Formal Definition**:

```
Latency = T_process - T_event
```

---

### Liveness

**Definition**: Temporal property stating "something good eventually happens".

**Related Concepts**: Safety, LTL

---

## M

### Materialized View

**Definition**: Pre-computed query results automatically updated when base data changes.

**Streaming Implementation**: Continuous SQL queries with incremental updates

---

### MCP (Model Context Protocol)

**Definition**: Protocol standard for AI model context exchange.

**Related Concepts**: AI Agent, A2A

---

### Microservices

**Definition**: Architectural style structuring applications as loosely coupled services.

---

## N

### Nexmark Benchmark

**Definition**: Standard benchmark for evaluating stream processing systems.

**Queries**: 22 SQL queries covering common stream processing scenarios

---

## O

### Observability

**Definition**: Ability to understand system internal state from external outputs.

**Three Pillars**: Metrics, Logs, Traces

---

### Operator

**Definition**: Basic computation unit in Flink's Dataflow graph.

**Types**: Source, Transform, Sink

---

## P

### Parallelism

**Definition**: Degree of concurrent execution for Flink operators.

**Configuration**: `parallelism.default`, per-operator parallelism

---

### Process Calculus

**Definition**: Formal language for describing concurrent process behavior.

**Main Branches**: CCS, CSP, π-Calculus

---

### Processing Time

**Definition**: Timestamp when data is processed.

**Formal Definition**:

```
ProcessingTime(e) = Current system time when processing e
```

---

## Q

### Queryable State

**Definition**: Flink feature allowing external queries of operator state.

**Use Cases**: Operational analytics, debugging, monitoring

---

## R

### RAG (Retrieval-Augmented Generation)

**Definition**: AI architecture combining retrieval systems with generation models.

**Streaming Integration**: Real-time knowledge base updates

---

### Real-time Processing

**Definition**: Processing data with low latency requirements (typically sub-second).

---

### RocksDB

**Definition**: Embedded key-value storage engine, Flink's default state backend.

**Advantages**: Disk-based, supports large state, incremental checkpoints

---

## S

### Safety

**Definition**: Temporal property stating "something bad never happens".

**Related Concepts**: Liveness, Invariant

---

### Savepoint

**Definition**: User-triggered, manually manageable Flink state snapshot.

**Use Cases**: Version upgrades, application migration, A/B testing

---

### Serverless

**Definition**: Cloud computing model where cloud provider manages infrastructure.

**Flink Integration**: Serverless Flink on AWS, GCP, Alibaba Cloud

---

### Session Types

**Definition**: Type systems describing communication protocols.

**Formal Definition**:

```
S ::= !T.S | ?T.S | S₁ ⊕ S₂ | S₁ & S₂ | μX.S | X | end
```

---

### Side Output

**Definition**: Flink mechanism for diverting specific data to separate streams.

**Use Cases**: Late data handling, exception data collection

---

### Sink

**Definition**: Operator outputting data to external systems.

**Examples**: KafkaSink, FileSink, JdbcSink

---

### Source

**Definition**: Operator reading data from external systems.

**Examples**: KafkaSource, FileSource, SocketSource

---

### State Backend

**Definition**: Flink component managing operator state storage.

**Types**: HashMapStateBackend, RocksDBStateBackend, CustomStateBackend

---

### Stream Processing

**Definition**: Computing paradigm processing unbounded data streams in real-time.

**Formal Definition**:

```
StreamJob = ⟨S, f⟩
  where S is unbounded stream, f is continuous transformation
```

---

### Streaming Database

**Definition**: Database system designed for continuous query processing on streams.

**Examples**: RisingWave, Materialize, Timeplus

---

### Stream-Batch Unification

**Definition**: Processing paradigm unifying stream and batch processing with single API.

**Flink Implementation**: DataStream API, Table API unified processing

---

## T

### TaskManager

**Definition**: Flink cluster's worker process executing tasks.

**Responsibilities**: Task execution, state management, network communication

---

### TGN (Temporal Graph Networks)

**Definition**: Graph neural networks handling dynamic graphs with temporal information.

**Streaming Integration**: Real-time graph updates, continuous embedding computation

---

### Throughput

**Definition**: Data processing rate (records/second or bytes/second).

---

### TLA+

**Definition**: Formal specification language for describing and verifying concurrent systems.

**Flink Application**: Checkpoint, Exactly-Once protocol verification

---

### TTL (Time-To-Live)

**Definition**: State expiration mechanism automatically cleaning outdated state.

**Configuration**: `StateTtlConfig`, update type, visibility

---

## U

### Unaligned Checkpoint

**Definition**: Checkpoint mechanism not requiring alignment of all input channels.

**Advantage**: Reduces checkpoint latency for high backpressure scenarios

---

### Unbounded Stream

**Definition**: Data stream with definite start but no definite end.

**Related Concepts**: Bounded Stream, Stream Processing

---

## V

### Vector Search

**Definition**: Similarity search technology in vector space.

**Streaming Integration**: Real-time vector index updates

---

## W

### Watermark

**Definition**: Timestamp marker indicating event time progress.

**Formal Definition**:

```
Watermark(t) ⟹ All events with timestamp ≤ t have arrived
```

**Related Concepts**: Event Time, Window, Late Data

---

### WASM (WebAssembly)

**Definition**: Binary instruction format for stack-based virtual machines.

**Flink Integration**: WASM UDF, cross-platform execution

---

### Window

**Definition**: Logical boundary dividing stream data into bounded sets.

**Types**: Tumbling, Sliding, Session, Global

---

## X

### Exactly-Once ( continued from E )

See [Exactly-Once](#exactly-once)

---

> **Note**: This glossary provides core term definitions. For complete formal definitions, please refer to corresponding documents in THEOREM-REGISTRY.md.
>
> **Last Updated**: 2026-04-08
