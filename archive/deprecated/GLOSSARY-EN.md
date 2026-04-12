> **状态**: 🔮 前瞻内容 | **风险等级**: 高 | **最后更新**: 2026-04
> 
> 此文档描述的内容处于早期规划阶段，可能与最终实现不符。请以 Apache Flink 官方发布为准。
# AnalysisDataFlow Glossary (English)

> **Version**: v1.0 | **Last Updated**: 2026-04-04 | **Scope**: Full Project
>
> **Version Annotations**: Terms marked with [2.0], [2.4], [2.5], [3.0] indicate introduction or core feature in corresponding Flink versions
>
> This document serves as the authoritative terminology reference for the AnalysisDataFlow project, organized alphabetically, covering stream computing theory, Flink engineering practices, and cutting-edge technologies.

---

## Table of Contents

- [Glossary Navigation](#glossary-navigation)
- [Term Category Index](#term-category-index)
- [A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [Q](#q) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [W](#w) · [X](#x) · [Y](#y) · [Z](#z)

---

## Glossary Navigation

| Category | Term Count | Primary Domain |
|----------|------------|----------------|
| [Basic Terms](#1-basic-terms) | 35+ | Stream Computing, Batch Processing, Real-time Processing |
| [Theoretical Terms](#2-theoretical-terms) | 40+ | Process Calculus, Formal Verification, Type Theory |
| [Flink Terms](#3-flink-terms) | 50+ | Core Concepts, APIs, Configuration Parameters |
| [Engineering Terms](#4-engineering-terms) | 30+ | Design Patterns, Architecture, Operations |
| [Frontier Terms](#5-frontier-terms) | 35+ | AI Agent, Streaming Databases, Cloud Native |

---

## Term Category Index

### 1. Basic Terms

- [Stream Computing](#1-basic-terms): Dataflow, Event Time, Processing Time, Watermark, Window
- [Batch Processing](#1-basic-terms): Batch Processing, Bounded Stream, Checkpoint
- [Real-time Processing](#1-basic-terms): Real-time Processing, Latency, Throughput

### 2. Theoretical Terms

- [Process Calculus Terms](#2-theoretical-terms): CCS, CSP, π-Calculus, Actor Model, Session Types
- [Formal Verification Terms](#2-theoretical-terms): Bisimulation, Model Checking, TLA+, Iris
- [Type Theory Terms](#2-theoretical-terms): FG/FGG, DOT, Path-Dependent Types

### 3. Flink Terms

- [Core Concepts](#3-flink-terms): JobManager, TaskManager, Operator, State Backend
- [API Related](#a): DataStream API, Table API, SQL
- [Configuration Parameters](#3-flink-terms): Parallelism, Checkpoint Interval, Watermark Strategy

### 4. Engineering Terms

- [Design Pattern Terms](#4-engineering-terms): Windowed Aggregation, Async I/O, Side Output
- [Architecture Terms](#4-engineering-terms): Microservices, Event-Driven Architecture, Data Mesh
- [Operations Terms](#4-engineering-terms): Backpressure, Monitoring, Autoscaling

### 5. Frontier Terms

- [AI Agent Terms](#a): AI Agent, ReAct, MCP, A2A, Agentic Workflow, FLIP-531, Tool Calling
- [Serverless Terms](#e): Serverless Flink, Scale-to-Zero, FaaS
- [Performance Optimization Terms](#5-frontier-terms): Adaptive Execution Engine, Smart Checkpointing, GPU Acceleration
- [Stream-Batch Unification Terms](#5-frontier-terms): Stream-Batch Unification, Unified Execution Engine
- [WASM Terms](#a): WebAssembly UDF, WASI, WASM
- [Streaming Database Terms](#5-frontier-terms): Materialized View, Continuous Query, Incremental Update
- [Cloud Native Terms](#5-frontier-terms): Kubernetes, Serverless, WASM, Lakehouse

---

## A

### Adaptive Execution Engine [Flink 1.17+]

**Definition**: Flink's intelligent execution optimization framework that dynamically adjusts execution plans, resource allocation, and parallelism based on runtime statistics.

**Formal Definition**:

```
AEE-V2 = (𝒫, ℳ, 𝒜, 𝒞, ℛ, δ, π)
```

Where 𝒫 is the physical execution plan, ℳ is runtime metrics, 𝒜 is adaptive actions, 𝒞 is constraints, ℛ is the re-optimizer, δ is the decision function, and π is the performance prediction model.

**Core Capabilities**: Automatic data skew handling, dynamic parallelism adjustment, adaptive resource allocation

**Related Concepts**: Smart Checkpointing, Backpressure, Parallelism

**Reference Documents**:

- `Flink/02-core/adaptive-execution-engine-v2.md` (Def-F-02-87, Thm-F-02-56)

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

### AI Agent [General Term]

**Definition**: An intelligent system capable of autonomously perceiving, reasoning, acting, and learning in an environment, formalized as a six-tuple:

```
𝒜_agent ≜ ⟨𝒮, 𝒫, 𝒟, 𝒜, ℳ, 𝒢⟩
```

Where 𝒮 is the state space, 𝒫 is perception, 𝒟 is decision-making, 𝒜 is action, ℳ is memory, and 𝒢 is goal.

**Flink Integration**: Flink Agent is an AI Agent implementation based on the stream computing framework

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

Where 𝒫 is the set of participating Agents, ℳ is message types, 𝒮 is the session state machine, and 𝒜 is the authentication/authorization mechanism.

**Task State Transition**: `pending → working → input-required → completed/failed`

**Related Concepts**: AI Agent, MCP, Orchestration, FLIP-531

**Reference Documents**:

- `Flink/12-ai-ml/flink-agents-flip-531.md` (Def-F-12-33)
- `Knowledge/06-frontier/a2a-protocol-agent-communication.md`

---

### Aligned Checkpoint

**Definition**: In Flink, a mechanism where operators trigger state snapshots only after receiving Barrier from **all** input channels.

**Formal Definition**:

```
AlignedSnapshot(t, n) ⟺ ∀c ∈ Inputs(t): Barrier(n) ∈ Received(c)
```

**Related Concepts**: Unaligned Checkpoint, Barrier, Exactly-Once

**Reference Documents**:

- `Flink/02-core/checkpoint-mechanism-deep-dive.md` (Def-F-02-03)
- `Struct/04-proofs/04.01-flink-checkpoint-correctness.md` (Thm-S-17-01)

---

### Async I/O

**Definition**: A pattern allowing stream processing operators to execute external system calls concurrently, avoiding blocking data flow processing.

**Formal Definition**:

```
AsyncFunction: I × C → Future[O]
```

Where C is the concurrency parameter, controlling the number of simultaneous async requests.

**Related Concepts**: Backpressure, Enrichment, Concurrency

**Reference Documents**:

- `Knowledge/02-design-patterns/pattern-async-io-enrichment.md`
- `Flink/02-core/async-execution-model.md`

---

### At-Least-Once

**Definition**: A stream computing system guarantee that each input record affects the external world **at least once**.

**Formal Definition**:

```
∀r ∈ I. c(r, 𝒯) ≥ 1
```

Where c(r, 𝒯) is the causal impact count.

**Related Concepts**: At-Most-Once, Exactly-Once, Delivery Guarantee

**Reference Documents**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-03)

---

### At-Most-Once

**Definition**: A stream computing system guarantee that each input record affects the external world **at most once**, allowing data loss.

**Formal Definition**:

```
∀r ∈ I. c(r, 𝒯) ≤ 1
```

**Related Concepts**: At-Least-Once, Exactly-Once, Best-Effort

**Reference Documents**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-02)

---

## B

### Backpressure

**Definition**: A flow control signal mechanism in stream processing systems where downstream processing speed falls below upstream, propagating back to slow down the flow.

**Principle**: Credit-based flow control where sending pauses when receive buffers are full.

**Related Concepts**: Flow Control, Buffer, Credit-Based

**Reference Documents**:

- `Flink/02-core/backpressure-and-flow-control.md`
- `Knowledge/09-anti-patterns/anti-pattern-08-ignoring-backpressure.md`

---

### Barrier (Checkpoint Barrier)

**Definition**: A special control event injected into the data stream in Flink to separate data boundaries between different Checkpoints.

**Formal Definition**:

```
Barrier(n) = ⟨Type = CONTROL, checkpointId = n, timestamp = ts⟩
```

**Related Concepts**: Checkpoint, Aligned Checkpoint, Unaligned Checkpoint

**Reference Documents**:

- `Flink/02-core/checkpoint-mechanism-deep-dive.md` (Def-F-02-02)

---

### Batch Processing

**Definition**: A computing pattern processing finite, bounded datasets where data is fully available before computation begins.

**Characteristics**:

- Input data is bounded
- Can access complete dataset
- Latency-insensitive, pursuit of high throughput

**Related Concepts**: Stream Processing, Bounded Stream, Lambda Architecture

**Reference Documents**:

- `Struct/01-foundation/01.04-dataflow-model-formalization.md`

---

### Best-Effort

**Definition**: A delivery semantics providing no consistency guarantees; the system processes data as best effort without guaranteeing no loss or duplication.

**Related Concepts**: At-Most-Once, Delivery Guarantee

---

### Bisimulation

**Definition**: A relation in process algebra for determining behavioral equivalence between two processes, requiring both processes to simulate each other on all possible actions.

**Formal Definition**:

```
R is bisimulation ⟺ ∀(P,Q)∈R. ∀α. P→αP' ⇒ ∃Q'. Q→αQ' ∧ (P',Q')∈R
```

**Related Concepts**: Process Calculus, Trace Equivalence, CCS

**Reference Documents**:

- `Struct/03-relationships/03.04-bisimulation-equivalences.md` (Thm-S-15-01)

---

### Bounded Stream

**Definition**: A data stream with finite data volume; the data abstraction for batch processing.

**Formal Definition**:

```
Bounded(S) ⟺ |S| < ∞
```

**Related Concepts**: Unbounded Stream, Batch Processing

---

### Buffer

**Definition**: A memory area in stream processing for temporarily storing data, located between producers and consumers.

**Related Concepts**: Backpressure, Queue, Network Buffer

---

## C

### CALM Theorem

**Definition**: Consistency As Logical Monotonicity — logically monotonic programs can guarantee consistency without coordination.

**Formal Statement**:

```
Program P requires no coordination ⟺ P is logically monotonic
```

**Related Concepts**: Eventual Consistency, Coordination

**Reference Documents**:

- `Struct/02-properties/02.06-calm-theorem.md` (Thm-S-02-08)

---

### Causal Consistency

**Definition**: A consistency model in distributed systems preserving the order of causally dependent operations.

**Formal Definition**:

```
∀op_i, op_j. op_i ≺hb op_j ⇒ op_i ≺obs op_j
```

**Related Concepts**: Strong Consistency, Eventual Consistency, Happens-Before

**Reference Documents**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-08)

---

### CEP (Complex Event Processing)

**Definition**: A technique for detecting complex patterns from event streams and generating composite events.

**Formal Definition**:

```
CEP: Stream × Pattern → DetectedEvents
```

**Related Concepts**: Pattern Matching, Event Pattern, Window

**Reference Documents**:

- `Knowledge/02-design-patterns/pattern-cep-complex-event.md`

---

### CCS (Calculus of Communicating Systems)

**Definition**: A process algebra based on labeled synchronization proposed by Milner in 1980.

**Syntax**:

```
P, Q ::= 0 | α.P | P + Q | P | Q | P \ L | P[f]
```

**Related Concepts**: CSP, π-Calculus, Process Algebra

**Reference Documents**:

- `Struct/01-foundation/01.02-process-calculus-primer.md` (Def-S-02-01)

---

### CDC (Change Data Capture)

**Definition**: A technology for capturing database change events (inserts, updates, deletes) and propagating them to downstream systems in real-time.

**Related Concepts**: Debezium, Streaming ETL, Log Mining

**Reference Documents**:

- `Flink/04-connectors/flink-cdc-3.0-data-integration.md`
- `Flink/04-connectors/04.04-cdc-debezium-integration.md`

---

### Checkpoint

**Definition**: A globally consistent state snapshot of a distributed stream processing job at a specific moment, used for fault recovery.

**Formal Definition**:

```
CP = ⟨ID, TS, {S_i}_{i∈Tasks}, Metadata⟩
```

**Related Concepts**: Savepoint, State Backend, Recovery

**Reference Documents**:

- `Flink/02-core/checkpoint-mechanism-deep-dive.md` (Def-F-02-01)
- `Struct/04-proofs/04.01-flink-checkpoint-correctness.md` (Thm-S-17-01)

---

### Chandy-Lamport Algorithm

**Definition**: A classic algorithm in distributed systems for capturing globally consistent snapshots; the theoretical foundation of Flink Checkpoint.

**Related Concepts**: Global Snapshot, Consistent Cut, Checkpoint

**Reference Documents**:

- `Struct/04-proofs/04.03-chandy-lamport-consistency.md` (Thm-S-19-01)

---

### Choreographic Programming

**Definition**: A distributed programming paradigm describing multi-party interaction protocols from a global perspective, then projecting to each participant.

**Related Concepts**: Session Types, Endpoint Projection, Deadlock Freedom

**Reference Documents**:

- `Struct/06-frontier/06.02-choreographic-streaming-programming.md`
- `Struct/04-proofs/04.07-deadlock-freedom-choreographic.md` (Thm-S-23-01)

---

### Cloud-Native

**Definition**: A methodology for building and running applications that leverage cloud computing advantages, emphasizing containerization, microservices, continuous delivery, and DevOps.

**Related Concepts**: Kubernetes, Containerization, Microservices

**Reference Documents**:

- `Flink/10-deployment/flink-kubernetes-operator-deep-dive.md`
- `Knowledge/06-frontier/serverless-stream-processing-architecture.md`

---

### Concurrency

**Definition**: The ability of multiple computational tasks to execute during overlapping time periods, distinct from Parallelism.

**Related Concepts**: Parallelism, Race Condition, Synchronization

---

### Consistency Model

**Definition**: A set of rules defining data operation visibility and ordering in distributed systems.

**Hierarchy**: Strong Consistency → Causal Consistency → Eventual Consistency

**Related Concepts**: Linearizability, Serializability, CAP Theorem

**Reference Documents**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Thm-S-08-03)

---

### Continuous Query

**Definition**: A query that runs continuously in stream databases, automatically updating results as data arrives.

**Formal Definition**:

```
q: S → 𝒱, where q is a time-varying function
```

**Related Concepts**: Materialized View, Streaming Database

**Reference Documents**:

- `Knowledge/06-frontier/streaming-databases.md` (Def-K-06-14)

---

### Coordination

**Definition**: Communication and synchronization among nodes in distributed systems to achieve consistent behavior.

**Related Concepts**: CALM Theorem, Consensus, Distributed Transaction

---

### Credit-Based Flow Control

**Definition**: A flow control mechanism where the receiver informs the sender of the amount of data it can receive by sending credit values.

**Related Concepts**: Backpressure, Flow Control

---

### CSP (Communicating Sequential Processes)

**Definition**: A process algebra based on synchronous communication and static event names proposed by Hoare in 1985.

**Syntax**:

```
P, Q ::= STOP | SKIP | a → P | P □ Q | P ⊓ Q | P ||| Q | P |[A]| Q
```

**Related Concepts**: CCS, π-Calculus, Go Channels

**Reference Documents**:

- `Struct/01-foundation/01.05-csp-formalization.md` (Def-S-02-02)
- `Struct/03-relationships/03.01-actor-to-csp-encoding.md` (Thm-S-12-01)

---

## D

### Data Enrichment

**Definition**: The process of associating raw data streams with external data sources to supplement contextual information.

**Related Concepts**: Async I/O, Lookup Join, Dimension Table

**Reference Documents**:

- `Knowledge/02-design-patterns/pattern-async-io-enrichment.md`

---

### Data Mesh

**Definition**: A decentralized data architecture paradigm treating data as a product, autonomously managed by domain teams.

**Related Concepts**: Data Product, Domain-Driven Design, Self-Serve Platform

**Reference Documents**:

- `Knowledge/03-business-patterns/data-mesh-streaming-architecture-2026.md`
- `Knowledge/06-frontier/streaming-data-mesh-architecture.md`

---

### Data Product

**Definition**: An autonomous data unit in Data Mesh that can be independently discovered, addressed, and consumed.

**Related Concepts**: Data Mesh, Data as a Product

---

### Dataflow Model

**Definition**: A graph model representing computation as data flowing between operators; the core theoretical foundation of stream computing.

**Formal Definition**:

```
𝒢 = (V, E, P, Σ, 𝕋)
```

Where V is the vertex set, E is the edge set, P is processing functions, Σ is state, and 𝕋 is the time model.

**Related Concepts**: DAG, Operator, Stream Graph

**Reference Documents**:

- `Struct/01-foundation/01.04-dataflow-model-formalization.md` (Def-S-04-01)
- `Struct/02-properties/02.01-determinism-in-streaming.md` (Thm-S-04-01)

---

### DAG (Directed Acyclic Graph)

**Definition**: A graph structure representing data flow processing topology, with nodes as operators and edges as data flows, without cycles.

**Related Concepts**: Dataflow Model, Job Graph, Execution Graph

---

### Deadlock Freedom

**Definition**: A property guaranteeing that no process in the system is permanently blocked waiting for an event that will never occur.

**Related Concepts**: Liveness, Choreographic Programming, Session Types

**Reference Documents**:

- `Struct/04-proofs/04.07-deadlock-freedom-choreographic.md` (Thm-S-23-01)

---

### Delivery Guarantee

**Definition**: A stream processing system's promise of message delivery reliability, categorized as At-Most-Once, At-Least-Once, Exactly-Once.

**Related Concepts**: At-Most-Once, At-Least-Once, Exactly-Once

**Reference Documents**:

- `Struct/02-properties/02.02-consistency-hierarchy.md`

---

### Determinism

**Definition**: A property where a system always produces the same output given the same input.

**Formal Definition**:

```
Deterministic(P) ⟺ ∀x. P(x) = P(x)
```

**Related Concepts**: Reproducibility, Consistency

**Reference Documents**:

- `Struct/02-properties/02.01-determinism-in-streaming.md` (Thm-S-07-01)

---

### Differential Dataflow

**Definition**: A stream processing model supporting incremental computation and recursion, based on differential update propagation.

**Related Concepts**: Incremental Computation, Materialize

---

### Distributed Snapshot

**Definition**: A consistent snapshot capturing the global state of a distributed system at a specific moment.

**Related Concepts**: Chandy-Lamport Algorithm, Checkpoint, Consistent Cut

---

### DOT (Dependent Object Types)

**Definition**: An advanced type system supporting path-dependent types and family polymorphism; the theoretical foundation of Scala.

**Related Concepts**: Path-Dependent Types, FGG, Subtyping

**Reference Documents**:

- `Struct/04-proofs/04.06-dot-subtyping-completeness.md` (Thm-S-22-01)

---

## E

### Edge Computing

**Definition**: A computing paradigm processing data near the data source (network edge), reducing latency and bandwidth consumption.

**Related Concepts**: Cloud-Edge Continuum, IoT, Latency

**Reference Documents**:

- `Knowledge/06-frontier/edge-streaming-architecture.md`

---

### End-to-End Consistency

**Definition**: Consistency guarantee across the entire pipeline from external data source to external data sink.

**Formal Definition**:

```
End-to-End-EO(J) ⟺ Replayable(Src) ∧ ConsistentCheckpoint(Ops) ∧ AtomicOutput(Snk)
```

**Related Concepts**: Internal Consistency, Exactly-Once, Source, Sink

**Reference Documents**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-05)

---

### Event-Driven Architecture

**Definition**: A software architecture pattern organizing component interaction around event production, detection, and consumption.

**Related Concepts**: Event Streaming, Pub/Sub, CQRS

---

### Event Pattern

**Definition**: Templates in CEP for matching event sequences, supporting sequence, choice, repetition, and other operators.

**Related Concepts**: CEP, Pattern Matching

---

### Event Sourcing

**Definition**: A persistence pattern using event sequences as the source of truth for system state.

**Related Concepts**: CQRS, Event Store, Audit Log

---

### Event Streaming

**Definition**: A computing pattern for continuously capturing, processing, and responding to event streams.

**Related Concepts**: Stream Processing, Event-Driven Architecture

---

### Event Time

**Definition**: The timestamp assigned by the data source when a data record is generated.

**Formal Definition**:

```
t_e: Record → Timestamp
```

**Related Concepts**: Processing Time, Ingestion Time, Watermark

**Reference Documents**:

- `Struct/01-foundation/01.01-unified-streaming-theory.md` (Def-S-01-05)
- `Flink/02-core/time-semantics-and-watermark.md`

---

### Eventual Consistency

**Definition**: A consistency model guaranteeing that eventually all replicas will converge to the same value if no new updates occur.

**Formal Definition**:

```
◇□(replicas converge)
```

**Related Concepts**: Strong Consistency, Causal Consistency, CALM Theorem

**Reference Documents**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-09)

---

### Exactly-Once

**Definition**: A stream computing system guarantee that each input record affects the external world **exactly once**.

**Formal Definition**:

```
∀r ∈ I. c(r, 𝒯) = 1
```

**Related Concepts**: At-Least-Once, At-Most-Once, Idempotency

**Reference Documents**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-04)
- `Struct/04-proofs/04.02-flink-exactly-once-correctness.md` (Thm-S-18-01)
- `Flink/02-core/exactly-once-semantics-deep-dive.md`

---

### Execution Graph

**Definition**: The graph structure in Flink that converts logical JobGraph to physical execution plans, containing specific parallel instances.

**Related Concepts**: Job Graph, Task, Parallelism

---

### Explicit State

**Definition**: Stream processing state explicitly declared and managed by user code, supported by Flink API.

**Related Concepts**: Implicit State, Keyed State, Operator State

---

## F

### FG (Featherweight Generic)

**Definition**: A lightweight formal model of Java generics used for type safety proofs.

**Related Concepts**: FGG, Type Safety, Java Generics

**Reference Documents**:

- `Struct/04-proofs/04.05-type-safety-fg-fgg.md` (Thm-S-21-01)

---

### FGG (Featherweight Generic Go)

**Definition**: A lightweight formal model of Go generics.

**Related Concepts**: FG, Go, Parametric Polymorphism

**Reference Documents**:

- `Struct/04-proofs/04.05-type-safety-fg-fgg.md` (Thm-S-21-01)

---

### Flink Agent [Flink 2.0+, FLIP-531]

**Definition**: An autonomous agent built on the Flink stream computing framework, supporting continuous perception, decision-making, and action.

**Formal Definition**:

```
𝒜_Flink = ⟨𝒮_state, 𝒫_perception, 𝒟_decision, 𝒜_action, ℳ_memory, 𝒢_goal⟩
```

**Core Features**: State persistence, Replayability, distributed execution, Exactly-Once semantics

**Related Concepts**: AI Agent, FLIP-531, MCP, A2A, Stateful Stream Processing

**Reference Documents**:

- `Flink/12-ai-ml/flink-agents-flip-531.md` (Def-F-12-30)
- `Flink/12-ai-ml/flip-531-ai-agents-ga-guide.md`

---

### FLIP-531 (Flink AI Agents Proposal) [Flink 2.0+]

**Definition**: Apache Flink official feature proposal introducing AI Agent native runtime support, achieving deep integration of stream computing and AI agents.

**Core Components**:

- **Flink Agent Runtime**: Agent execution environment
- **MCP Integration**: Model Context Protocol support
- **A2A Protocol**: Inter-Agent interoperability
- **Agentic Workflow**: Agent workflow orchestration

**Formal Definition**:

```
FLIP-531 = ⟨ℛ_agent, ℐ_mcp, 𝒫_a2a, 𝒲_workflow⟩
```

**Related Concepts**: Flink Agent, MCP, A2A, Agentic Workflow

**Reference Documents**:

- `Flink/12-ai-ml/flink-agents-flip-531.md`
- `Flink/12-ai-ml/flip-531-ai-agents-ga-guide.md`

---

### Flow Control

**Definition**: A mechanism regulating data transfer rates between data producers and consumers.

**Related Concepts**: Backpressure, Credit-Based, Buffer

---

### ForSt State Backend

**Definition**: The next-generation state backend introduced in Flink 2.0, based on RocksDB improvements, supporting the async execution model.

**Related Concepts**: State Backend, RocksDB, Incremental Checkpoint

**Reference Documents**:

- `Flink/02-core/forst-state-backend.md` (Thm-F-02-45)
- `Flink/02-core/flink-2.0-forst-state-backend.md`

---

### Function as a Service (FaaS)

**Definition**: A serverless computing model where users write function code and the platform manages infrastructure and auto-scaling.

**Related Concepts**: Serverless, Lambda, Cloud-Native

**Reference Documents**:

- `Knowledge/06-frontier/faas-dataflow.md`
- `Knowledge/06-frontier/serverless-stream-processing-architecture.md`

---

## G

### GPU Acceleration [Flink 2.5+]

**Definition**: Utilizing GPU's massive parallel computing capabilities to execute stream processing operators, offloading compute-intensive operations from CPU to GPU via CUDA/OpenCL.

**Formal Definition**:

```
𝒪_GPU(D) = GPUKernel(Transfer(D_CPU→GPU))
```

**Speedup Ratio**: S_GPU = T_CPU / (T_transfer + T_kernel + T_sync)

**Applicable Conditions**: Batch size n > n_threshold and compute/transfer ratio > γ

**Accelerated Operator Types**: GPU aggregation, GPU Join, GPU UDF, vector search

**Related Concepts**: CUDA, Vector Search, Flink-CUDA Runtime

**Reference Documents**:

- `Flink/12-ai-ml/flink-25-gpu-acceleration.md` (Def-F-12-50)

---

### Global Snapshot

**Definition**: A collection of all process states in a distributed system at a specific moment, used for fault recovery and consistency checking.

**Related Concepts**: Distributed Snapshot, Chandy-Lamport Algorithm, Checkpoint

---

### Global Window

**Definition**: A single window containing all records, typically used with custom triggers.

**Formal Definition**:

```
Global: wid_global = (-∞, +∞)
```

**Related Concepts**: Tumbling Window, Sliding Window, Session Window

**Reference Documents**:

- `Knowledge/02-design-patterns/pattern-windowed-aggregation.md` (Def-K-02-02)

---

### Go Channels

**Definition**: Synchronous communication primitives in Go language based on the CSP model.

**Related Concepts**: CSP, Channel, Goroutine

**Reference Documents**:

- `Struct/05-comparative/05.01-go-vs-scala-expressiveness.md` (Thm-S-24-01)

---

## H

### Happens-Before

**Definition**: A relation defining causal partial order between events; the foundation of distributed consistency.

**Formal Definition**:

```
∀e₁, e₂. e₁ ≺hb e₂ ⟺ e₁ causally affects e₂
```

**Related Concepts**: Causal Consistency, Lamport Clock, Vector Clock

---

### HashMapStateBackend

**Definition**: A heap-memory-based state backend in Flink, suitable for small state, low-latency scenarios.

**Related Concepts**: State Backend, RocksDBStateBackend, ForSt

**Reference Documents**:

- `Flink/02-core/checkpoint-mechanism-deep-dive.md` (Def-F-02-06)

---

### Hot Key

**Definition**: A key in data distribution with frequency much higher than other keys, leading to data skew and performance bottlenecks.

**Related Concepts**: Data Skew, Key Group, Rebalancing

**Reference Documents**:

- `Knowledge/09-anti-patterns/anti-pattern-04-hot-key-skew.md`

---

## I

### Idempotency

**Definition**: A property where an operation produces the same result whether executed once or multiple times; key to achieving Exactly-Once.

**Formal Definition**:

```
f is idempotent ⟺ ∀x. f(f(x)) = f(x)
```

**Related Concepts**: Exactly-Once, Idempotent Sink, Dedup

---

### Idempotent Sink

**Definition**: An external system receiver capable of safely handling duplicate writes, typically based on primary key deduplication.

**Related Concepts**: Sink, Idempotency, Exactly-Once

---

### Incremental Checkpoint

**Definition**: Capturing only the portion of state that has changed since the last Checkpoint.

**Formal Definition**:

```
ΔS_n = S_{t_n} \ S_{t_{n-1}}, CP_n^inc = ⟨Base, {ΔS_i}_{i=1}^n⟩
```

**Related Concepts**: Checkpoint, State Backend, RocksDB

**Reference Documents**:

- `Flink/02-core/checkpoint-mechanism-deep-dive.md` (Def-F-02-05, Thm-F-02-02)

---

### Incremental Computation

**Definition**: A computing pattern that calculates output changes based on input changes, avoiding full recomputation.

**Formal Definition**:

```
δv = ℱ_q(δD, D), v_new = v ⊕ δv
```

**Related Concepts**: Materialized View, Differential Dataflow

---

### Ingestion Time

**Definition**: The timestamp when a data record enters the stream processing system.

**Formal Definition**:

```
t_i: Record → Timestamp_system
```

**Related Concepts**: Event Time, Processing Time

---

### Internal Consistency

**Definition**: Consistency of a stream processing engine's internal operator state with global snapshots after fault recovery.

**Formal Definition**:

```
Internal-Consistency(Ops) ⟺ ∀k. Consistent(𝒢_k) ∧ NoOrphans(𝒢_k) ∧ Reachable(𝒢_k)
```

**Related Concepts**: End-to-End Consistency, Checkpoint

**Reference Documents**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-06)

---

### IoT (Internet of Things)

**Definition**: A network of physical devices and sensors producing massive stream data.

**Related Concepts**: Edge Computing, Sensor Data, Stream Processing

**Reference Documents**:

- `Knowledge/03-business-patterns/iot-stream-processing.md`
- `Flink/07-case-studies/case-iot-stream-processing.md`

---

### Iris

**Definition**: A higher-order separation logic-based concurrent program verification framework.

**Related Concepts**: Separation Logic, Formal Verification, Model Checking

**Reference Documents**:

- `Struct/07-tools/iris-separation-logic.md`

---

## J

### Job Graph

**Definition**: The logical execution graph in Flink after user program compilation, representing data flow relationships between operators.

**Related Concepts**: Execution Graph, DAG, Operator

---

### JobManager

**Definition**: The master process in a Flink cluster responsible for task scheduling, coordination, and fault recovery.

**Related Concepts**: TaskManager, ResourceManager, Dispatcher

**Reference Documents**:

- `Flink/01-architecture/deployment-architectures.md`

---

### Join

**Definition**: An operation merging two data streams according to join conditions.

**Types**:

- **Interval Join**: Stream join based on time intervals
- **Temporal Join**: Temporal table join
- **Lookup Join**: Dimension table join
- **Delta Join**: Incremental join

**Related Concepts**: Stream Join, Window Join

**Reference Documents**:

- `Flink/02-core/delta-join.md`

---

## K

### Key Group

**Definition**: The partitioning unit for Keyed State in Flink, determining state distribution among parallel instances.

**Related Concepts**: Keyed State, Parallelism, State Partitioning

---

### Keyed State

**Definition**: State stored by Key partition, where each Key has independent state space.

**Formal Definition**:

```
KeyedState: (K, State[K]) → State[K]
```

**Related Concepts**: Operator State, State Backend, Key Group

---

### KeyedProcessFunction

**Definition**: A low-level processing function in Flink DataStream API providing access to Keyed State and timers.

**Related Concepts**: ProcessFunction, Keyed State, Timer

---

### KeyedStream

**Definition**: A data stream partitioned by Key in Flink, supporting Keyed State operations.

**Related Concepts**: DataStream, Keyed State, Partitioning

---

### Kubernetes

**Definition**: An open-source container orchestration platform; Flink's primary deployment target.

**Related Concepts**: Container, Operator Pattern, Cloud-Native

**Reference Documents**:

- `Flink/10-deployment/flink-kubernetes-operator-deep-dive.md`
- `Flink/10-deployment/kubernetes-deployment-production-guide.md`

---

## L

### Lakehouse

**Definition**: An architectural paradigm combining the advantages of data lakes (low-cost storage) and data warehouses (high-performance analytics).

**Related Concepts**: Delta Lake, Iceberg, Paimon

**Reference Documents**:

- `Flink/14-lakehouse/streaming-lakehouse-architecture.md`
- `Knowledge/06-frontier/streaming-lakehouse-iceberg-delta.md`

---

### Lambda Architecture

**Definition**: A batch-stream separation architecture proposed by Nathan Marz, maintaining separate batch and speed layers.

**Related Concepts**: Kappa Architecture, Batch Processing, Stream Processing

---

### Latency

**Definition**: The time interval from event occurrence to result processing/visibility.

**Types**:

- **Processing Latency**: Processing delay
- **End-to-End Latency**: End-to-end delay
- **Watermark Latency**: Watermark delay

**Related Concepts**: Throughput, SLA, Real-time

---

### LSM-Tree (Log-Structured Merge Tree)

**Definition**: A write-optimized disk data structure; the foundation of RocksDB.

**Related Concepts**: RocksDB, State Backend, Compaction

---

## M

### Materialized View

**Definition**: Precomputed and physically stored query results, automatically incrementally maintained in stream databases.

**Formal Definition**:

```
v = q(D), when δD occurs: v_new = v ⊕ ℱ_q(δD, D)
```

**Related Concepts**: View Maintenance, Incremental Computation, Continuous Query

**Reference Documents**:

- `Knowledge/06-frontier/streaming-databases.md` (Def-K-06-13)
- `Flink/03-sql-table-api/materialized-tables.md`

---

### MCP (Model Context Protocol) [Anthropic 2024, Flink 2.0+]

**Definition**: An open protocol proposed by Anthropic for standardizing LLM interaction with external tools.

**Formal Definition**:

```
MCP_Flink = ⟨𝒯, ℛ, 𝒞, ℋ⟩
```

Where 𝒯 is the tool set, ℛ is the tool selection function, 𝒞 is the call construction function, and ℋ is the memory mapping.

**Core Capabilities**: Tool discovery, call construction, result observation, memory update

**Related Concepts**: AI Agent, Tool Calling, A2A, FLIP-531

**Reference Documents**:

- `Flink/12-ai-ml/flink-agents-flip-531.md` (Def-F-12-32)
- `Knowledge/06-frontier/mcp-protocol-agent-streaming.md`

---

### Message Passing

**Definition**: A communication model between concurrent entities through sending and receiving messages.

**Related Concepts**: Actor Model, CSP, Shared Memory

---

### Microservices

**Definition**: An architectural style breaking applications into small, autonomous services communicating via APIs.

**Related Concepts**: Service Mesh, Domain-Driven Design, Cloud-Native

---

### Model Checking

**Definition**: An automated formal method for verifying whether finite state systems satisfy specifications.

**Related Concepts**: Formal Verification, TLA+, State Space

**Reference Documents**:

- `Struct/07-tools/model-checking-practice.md`
- `Struct/07-tools/tla-for-flink.md`

---

### Multi-Agent

**Definition**: A system architecture where multiple AI Agents collaborate to complete complex tasks.

**Architecture Patterns**:

- **Orchestrator-Worker**: Central coordinator assigns tasks
- **Supervisor + Workers**: Supervisor monitors Worker status
- **Decentralized**: Direct decentralized communication

**Related Concepts**: AI Agent, A2A, Coordination

**Reference Documents**:

- `Knowledge/06-frontier/ai-agent-streaming-architecture.md` (Def-K-06-114)

---

## N

### Network Buffer

**Definition**: Memory buffers in Flink for network data transmission.

**Related Concepts**: Buffer, Backpressure, Credit-Based

---

## O

### Observability

**Definition**: The ability to understand internal system state through system outputs (metrics, logs, traces).

**Three Pillars**:

- **Metrics**: Indicators
- **Logs**: Log records
- **Traces**: Distributed tracing

**Related Concepts**: Monitoring, OpenTelemetry, SLA

**Reference Documents**:

- `Flink/15-observability/opentelemetry-streaming-observability.md`
- `Flink/15-observability/flink-opentelemetry-observability.md`

---

### OpenTelemetry

**Definition**: An open-source observability framework providing unified standards for metrics, logs, and traces.

**Related Concepts**: Observability, Metrics, Tracing

---

### Operator

**Definition**: The basic computational unit in Flink performing data transformations.

**Categories**:

- **Source**: Data source
- **Transformation**: Transformation
- **Sink**: Data sink

**Formal Definition**:

```
Operator: Input × State → Output × State
```

**Related Concepts**: Dataflow Model, Task, UDF

---

### Operator State

**Definition**: State bound to operator instances, not partitioned by Key.

**Related Concepts**: Keyed State, Broadcast State, State Backend

---

### Orchestration

**Definition**: A pattern coordinating multiple services or components to complete business processes.

**Related Concepts**: Multi-Agent, Workflow, Choreography

---

## P

### Parallelism

**Definition**: The number of parallel execution instances of an operator or task.

**Formal Definition**:

```
Parallelism(op) = |{instance_i(op)}|
```

**Related Concepts**: Slot, Task, Key Group

---

### Path-Dependent Types

**Definition**: Types that depend on values, such as `x.type` depending on the value of `x`.

**Related Concepts**: DOT, Scala, Dependent Types

**Reference Documents**:

- `Struct/06-frontier/06.04-pdot-path-dependent-types.md`

---

### Pattern Matching

**Definition**: A mechanism for conditional branching based on data structure patterns.

**Related Concepts**: CEP, Event Pattern

---

### Petri Net

**Definition**: A graphical mathematical model for modeling concurrent systems, composed of places and transitions.

**Related Concepts**: Process Calculus, Concurrency, Workflow

**Reference Documents**:

- `Struct/01-foundation/01.06-petri-net-formalization.md` (Thm-S-06-01)

---

### π-Calculus

**Definition**: A process algebra supporting name passing (mobility) proposed by Milner et al. in 1992.

**Syntax**:

```
P, Q ::= 0 | a(x).P | ā⟨b⟩.P | τ.P | P + Q | P | Q | (νa)P | !P
```

**Related Concepts**: CCS, CSP, Mobile Processes, Session Types

**Reference Documents**:

- `Struct/01-foundation/01.02-process-calculus-primer.md` (Def-S-02-03, Thm-S-02-01)

---

### Processing Time

**Definition**: The machine time when a data record is processed by an operator.

**Formal Definition**:

```
t_p: () → Timestamp_wall
```

**Related Concepts**: Event Time, Ingestion Time

---

### Process Calculus

**Definition**: A family of algebraic frameworks for describing concurrent system formal semantics.

**Major Members**: CCS, CSP, π-Calculus, Actor Calculus

**Reference Documents**:

- `Struct/01-foundation/01.02-process-calculus-primer.md`

---

### ProcessFunction

**Definition**: A low-level processing function in Flink DataStream API providing fine-grained control over time and state.

**Related Concepts**: KeyedProcessFunction, Timer, State

---

### Progress

**Definition**: A type safety property ensuring well-typed programs don't get stuck (in a state that is neither terminating nor erroneous).

**Related Concepts**: Preservation, Type Safety, Deadlock Freedom

---

### Pub/Sub (Publish-Subscribe)

**Definition**: A message passing pattern where publishers send messages to topics and subscribers receive messages from topics of interest.

**Related Concepts**: Message Passing, Kafka, Event Streaming

---

## Q

### Query Optimization

**Definition**: The process of automatically selecting query execution plans to minimize resource consumption.

**Related Concepts**: Calcite, Cost-Based Optimization, Rule-Based Optimization

**Reference Documents**:

- `Flink/03-sql-table-api/flink-sql-calcite-optimizer-deep-dive.md`

---

## R

### RAG (Retrieval-Augmented Generation)

**Definition**: An AI architecture combining retrieval systems and generation models, enhancing LLM output by retrieving external knowledge.

**Formal Definition**:

```
RAG(q) = Generate(q, Retrieve(q, KnowledgeBase))
```

**Related Concepts**: Vector Search, LLM, Knowledge Base

**Reference Documents**:

- `Knowledge/06-frontier/real-time-rag-architecture.md`
- `Flink/12-ai-ml/rag-streaming-architecture.md`

---

### Real-Time

**Definition**: A system characteristic producing results within strict time constraints.

**Categories**:

- **Hard Real-Time**: Missing deadlines causes system failure
- **Soft Real-Time**: Missing deadlines degrades service quality
- **Near Real-Time**: Second-level latency acceptable

**Related Concepts**: Latency, SLA

---

### ReAct (Reasoning + Acting)

**Definition**: An AI Agent architecture pattern interleaving reasoning (Thought) and action (Action) loops to solve complex problems.

**Formal Definition**:

```
ReAct: 𝒪_t → Thought → τ_t → Action → a_t → Observation → 𝒪_{t+1}
```

**Related Concepts**: AI Agent, Chain-of-Thought

**Reference Documents**:

- `Knowledge/06-frontier/ai-agent-streaming-architecture.md` (Def-K-06-111)

---

### Recovery

**Definition**: The process of reconstructing system state from Checkpoint or Savepoint after failure.

**Related Concepts**: Checkpoint, Savepoint, Failover

---

### Replayability

**Definition**: The ability to fully replay execution history from Checkpoint; a core feature of Flink Agent.

**Formal Definition**:

```
ℛ_replay = ⟨𝒞, ℒ, ℋ⟩
```

**Related Concepts**: Checkpoint, Audit, Debugging

**Reference Documents**:

- `Flink/12-ai-ml/flink-agents-flip-531.md` (Def-F-12-35)

---

### ResourceManager

**Definition**: A component in Flink responsible for cluster resource allocation and management.

**Related Concepts**: JobManager, TaskManager, Slot

---

### RocksDB

**Definition**: An embedded key-value store developed by Facebook, based on LSM-Tree.

**Related Concepts**: LSM-Tree, State Backend, EmbeddedRocksDBStateBackend

---

### RocksDBStateBackend

**Definition**: A RocksDB-based state backend in Flink, supporting large state and incremental Checkpoint.

**Related Concepts**: State Backend, RocksDB, Incremental Checkpoint

**Reference Documents**:

- `Flink/02-core/checkpoint-mechanism-deep-dive.md` (Def-F-02-06)

---

## S

### Savepoint

**Definition**: A user-triggered globally consistent snapshot for application upgrades, migrations, and backups; same semantics as Checkpoint but different lifecycle management.

**Related Concepts**: Checkpoint, Recovery, Upgrading

---

### Scala

**Definition**: A JVM language fusing object-oriented and functional programming; one of Flink's native API languages.

**Related Concepts**: Type System, Akka, JVM

**Reference Documents**:

- `Flink/09-language-foundations/01.01-scala-types-for-streaming.md`
- `Flink/09-language-foundations/01.03-scala3-type-system-formalization.md`

---

### Scale-Up / Scale-Out

**Definition**:

- **Scale-Up**: Enhancing single-node computing power
- **Scale-Out**: Increasing node count to expand processing capacity

**Related Concepts**: Elasticity, Autoscaling, Parallelism

---

### Semantic Matching

**Definition**: Data matching technology based on semantic similarity rather than exact value matching, commonly used in RAG and vector search.

**Related Concepts**: Vector Search, Embedding, Similarity Search

---

### Separation Logic

**Definition**: A logical framework for reasoning about mutable data structures, supporting local reasoning.

**Related Concepts**: Iris, Formal Verification, Concurrent Separation Logic

**Reference Documents**:

- `Struct/07-tools/iris-separation-logic.md`

---

### Serverless

**Definition**: A cloud computing execution model where cloud providers dynamically manage machine resource allocation.

**Related Concepts**: Serverless Flink, FaaS, Cloud-Native, Autoscaling

**Reference Documents**:

- `Knowledge/06-frontier/serverless-stream-processing-architecture.md`
- `Flink/10-deployment/flink-serverless-architecture.md`

---

### Serverless Flink [Flink 2.0+ GA]

**Definition**: Apache Flink's production-grade serverless implementation on Kubernetes, supporting Scale-to-Zero and pay-per-use billing.

**Formal Definition**:

```
ServerlessFlink_GA = ⟨𝒦, 𝒜, 𝒮, 𝒞, ℬ⟩
```

Where 𝒦 is Kubernetes Native, 𝒜 is Autoscaler, 𝒮 is disaggregated state storage, 𝒞 is incremental async checkpoint, and ℬ is GB-second precise billing.

**Core Features**:

- **Scale-to-Zero**: Scaling resources to zero when no load
- **Cold start optimization**: <10s snapshot recovery (traditional 110-420s)
- **Precise billing**: Second-level billing granularity
- **SLA guarantee**: 99.9% availability

**Related Concepts**: Serverless, Scale-to-Zero, ForSt, Kubernetes

**Reference Documents**:

- `Flink/10-deployment/serverless-flink-ga-guide.md` (Def-F-10-50)
- `Flink/10-deployment/flink-serverless-architecture.md`

---

### Session Types

**Definition**: A type system describing communication protocol structures, guaranteeing communication safety and deadlock freedom.

**Formal Definition**:

```
S ::= !T.S | ?T.S | ⊕{l_i: S_i} | &{l_i: S_i} | end
```

**Related Concepts**: Type Safety, Deadlock Freedom, Protocol Compliance

**Reference Documents**:

- `Struct/01-foundation/01.07-session-types.md` (Thm-S-01-03, Thm-S-01-04)

---

### Session Window

**Definition**: Windows dynamically divided based on activity gaps, closing after inactivity exceeds the gap.

**Formal Definition**:

```
Session(g, r₁, r₂, ...): wid = [t_first, t_last + g)
```

**Related Concepts**: Tumbling Window, Sliding Window, Window

**Reference Documents**:

- `Knowledge/02-design-patterns/pattern-windowed-aggregation.md` (Def-K-02-02)

---

### Shared Memory

**Definition**: A communication model where multiple concurrent entities access the same memory region; distinct from message passing.

**Related Concepts**: Message Passing, Race Condition, Synchronization

---

### Side Output

**Definition**: A mechanism separating specific data from the main stream to a side stream, used for handling late data or anomalies.

**Related Concepts**: Late Data, Data Splitting, Main Stream

**Reference Documents**:

- `Knowledge/02-design-patterns/pattern-side-output.md`

---

### Smart Checkpointing [Flink 2.0+]

**Definition**: An adaptive distributed state snapshot mechanism capable of dynamically adjusting checkpoint strategies based on runtime load.

**Core Strategies**:

- **Adaptive checkpoint interval**: Dynamic adjustment based on load
- **Incremental checkpoint optimization**: Capturing only changed state
- **Partial checkpoint**: Fault-domain isolated snapshots
- **Checkpoint parallelism optimization**: Dynamic parallelism adjustment

**Formal Definition**:

```
SmartCP = ⟨ℐ_adaptive, Δ_incremental, 𝒫_partial, 𝒫_parallel⟩
```

**Related Concepts**: Checkpoint, Incremental Checkpoint, Adaptive Execution Engine, ForSt

**Reference Documents**:

- `Flink/02-core/smart-checkpointing-strategies.md` (Def-F-02-110, Thm-F-02-60)

---

### Sink

**Definition**: A component in stream processing that writes data to external systems.

**Related Concepts**: Source, Connector, Exactly-Once

---

### Sliding Window

**Definition**: Fixed-size windows sliding by fixed steps, with possible overlap between windows.

**Formal Definition**:

```
Sliding(δ, s): wid_n = [n·s, n·s + δ)
```

**Related Concepts**: Tumbling Window, Session Window, Window

---

### Slot

**Definition**: The basic unit of resource allocation in Flink TaskManager; one Task Slot can execute one task chain.

**Related Concepts**: TaskManager, Task, Resource

---

### Source

**Definition**: A component in stream processing that reads data from external systems.

**Related Concepts**: Sink, Connector, Offset

---

### Source Split

**Definition**: A parallel readable unit of data sources, such as Kafka partitions.

**Related Concepts**: Source, Parallelism, Partition

---

### Split-Level Watermark

**Definition**: A mechanism for generating Watermarks at the Source Split level, supporting finer-grained flow control.

**Related Concepts**: Watermark, Source Split

**Reference Documents**:

- `Flink/15-observability/split-level-watermark-metrics.md`

---

### SQL/Table API

**Definition**: A declarative API provided by Flink supporting standard SQL and Table DSL.

**Related Concepts**: DataStream API, Query Optimization, Calcite

**Reference Documents**:

- `Flink/03-sql-table-api/sql-vs-datastream-comparison.md`

---

### State

**Definition**: Data maintained across records in stream processing; the foundation of stateful computation.

**Categories**:

- **Keyed State**: Keyed state
- **Operator State**: Operator state
- **Broadcast State**: Broadcast state

**Related Concepts**: Stateful Processing, State Backend

---

### State Backend

**Definition**: A runtime component responsible for state storage, access, and snapshot persistence.

**Implementation Types**:

- **HashMapStateBackend**: Memory storage
- **EmbeddedRocksDBStateBackend**: Disk storage
- **ForStStateBackend**: Flink 2.0 next-generation backend

**Related Concepts**: State, Checkpoint, Recovery

**Reference Documents**:

- `Flink/02-core/checkpoint-mechanism-deep-dive.md` (Def-F-02-06)
- `Flink/06-engineering/state-backend-selection.md`

---

### Stateful Stream Processing

**Definition**: A stream computing pattern maintaining and using state across records.

**Formal Definition**:

```
F: (K, V) × State[K] → State[K] × O
```

**Related Concepts**: Stateless Processing, State, Keyed State

---

### State Partitioning

**Definition**: A strategy for distributing Keyed State to multiple parallel instances.

**Related Concepts**: Key Group, Parallelism, Keyed State

---

### State TTL

**Definition**: Setting expiration times for state, automatically cleaning expired data.

**Related Concepts**: State, Cleanup, Expiration

---

### Stream Processing

**Definition**: A computing pattern processing infinite, unbounded data streams in real-time or near-real-time.

**Characteristics**:

- Input data is unbounded
- Sequential processing, record-by-record
- Latency-sensitive, pursuit of low latency

**Related Concepts**: Batch Processing, Unbounded Stream, Real-time Processing

---

### Streaming Database

**Definition**: A database system natively supporting continuous queries and automatic incremental view maintenance.

**Representative Systems**: RisingWave, Materialize, Timeplus

**Related Concepts**: Materialized View, Continuous Query, Stream Processing

**Reference Documents**:

- `Knowledge/06-frontier/streaming-databases.md`

---

### Strong Consistency

**Definition**: The strongest consistency model requiring all operations to appear as if executed atomically at a single point in time.

**Related Concepts**: Linearizability, Serializability, Causal Consistency

---

### Synchronization

**Definition**: Coordination mechanisms between concurrent entities to control execution order and access to shared resources.

**Related Concepts**: Concurrency, Race Condition, Mutex

---

## T

### Table API

**Definition**: A relational API provided by Flink using Table abstraction and embedded DSL.

**Related Concepts**: SQL, DataStream API, Relational Algebra

---

### Task

**Definition**: The basic unit of execution in Flink, representing an instance of an operator or operator chain.

**Related Concepts**: Operator, TaskManager, Slot

---

### TaskManager

**Definition**: A worker process in Flink cluster responsible for executing tasks and maintaining local state.

**Related Concepts**: JobManager, ResourceManager, Slot

---

### TLA+

**Definition**: A formal specification language for describing and verifying concurrent and distributed systems.

**Related Concepts**: Model Checking, Formal Verification, Temporal Logic

**Reference Documents**:

- `Struct/07-tools/tla-for-flink.md`

---

### Throughput

**Definition**: The number of records or data volume processed per unit time.

**Related Concepts**: Latency, Performance, Scalability

---

### Timer

**Definition**: A mechanism for triggering callbacks at specific time points in Flink.

**Types**: Processing Time Timer, Event Time Timer

**Related Concepts**: ProcessFunction, Event Time, Window

---

### Time Window

**Definition**: A window defined by time boundaries.

**Types**: Tumbling Window, Sliding Window, Session Window

**Related Concepts**: Window, Event Time, Processing Time

---

### Transaction

**Definition**: A logical unit of work with ACID properties (Atomicity, Consistency, Isolation, Durability).

**Related Concepts**: Exactly-Once, 2PC, Distributed Transaction

---

### Trigger

**Definition**: A mechanism determining when window results are calculated and emitted.

**Related Concepts**: Window, Emit, Pane

---

### Tumbling Window

**Definition**: Fixed-size, non-overlapping windows.

**Formal Definition**:

```
Tumbling(δ): wid_n = [n·δ, (n+1)·δ)
```

**Related Concepts**: Sliding Window, Session Window, Window

---

### Type Safety

**Definition**: A property where well-typed programs do not exhibit type errors at runtime.

**Formal Definition**:

```
⊢ P: T ∧ P →* P' ⇒ ⊢ P': T
```

**Related Concepts**: Type System, Type Checking, Preservation

---

## U

### UDF (User-Defined Function)

**Definition**: Custom functions provided by users extending Flink's built-in capabilities.

**Types**: Scalar Function, Table Function, Aggregate Function

**Related Concepts**: Operator, SQL, Table API

---

### Unaligned Checkpoint

**Definition**: In Flink, a Checkpoint mechanism that buffers in-flight data without requiring operator alignment.

**Related Concepts**: Aligned Checkpoint, Barrier, Buffer

**Reference Documents**:

- `Flink/02-core/checkpoint-mechanism-deep-dive.md`

---

### Unbounded Stream

**Definition**: A data stream with infinite data volume; the data abstraction for stream processing.

**Formal Definition**:

```
Unbounded(S) ⟺ |S| = ∞
```

**Related Concepts**: Bounded Stream, Stream Processing

---

## V

### Vector Clock

**Definition**: A logical clock mechanism capturing causal relationships between events in distributed systems.

**Related Concepts**: Lamport Clock, Happens-Before, Causal Consistency

---

### Vector Search

**Definition**: A search technology based on vector similarity calculation, used in semantic search and RAG.

**Related Concepts**: Embedding, RAG, Semantic Matching, Vector Database

---

### Version Control

**Definition**: A system for tracking and managing changes to documents and code.

**Related Concepts**: Git, State Versioning, Checkpoint

---

## W

### WAL (Write-Ahead Log)

**Definition**: A durability technique where changes are first written to a log before being applied to the database.

**Related Concepts**: Durability, Checkpoint, Recovery

---

### Watermark

**Definition**: A timestamp marker in Flink indicating the progress of event time.

**Formal Definition**:

```
WM(t): t_event ≤ t is considered complete
```

**Related Concepts**: Event Time, Lateness, Window

**Reference Documents**:

- `Struct/01-foundation/01.01-unified-streaming-theory.md` (Def-S-01-06)
- `Flink/02-core/time-semantics-and-watermark.md`

---

### WebAssembly (WASM)

**Definition**: A portable binary instruction format enabling high-performance execution in web browsers and other environments.

**Flink Applications**: WASM UDF, cross-language portability

**Related Concepts**: UDF, Portable, Polyglot

---

### Window

**Definition**: A mechanism dividing unbounded streams into bounded collections for processing.

**Types**: Tumbling Window, Sliding Window, Session Window, Global Window

**Related Concepts**: Event Time, Processing Time, Trigger

---

### Windowed Aggregation

**Definition**: Aggregation operations performed within window boundaries.

**Related Concepts**: Window, Aggregation, Group By

---

## X

(No entries)

---

## Y

(No entries)

---

## Z

(No entries)

---

## Appendix A: Chinese-English Terminology Mapping

| Chinese | English | Abbreviation |
|---------|---------|--------------|
| 流处理 | Stream Processing | SP |
| 批处理 | Batch Processing | BP |
| 检查点 | Checkpoint | CP |
| 水印 | Watermark | WM |
| 窗口 | Window | - |
| 恰好一次 | Exactly-Once | EO |
| 至少一次 | At-Least-Once | ALO |
| 最多一次 | At-Most-Once | AMO |
| 背压 | Backpressure | BP |
| 状态管理 | State Management | - |
| 事件时间 | Event Time | - |
| 处理时间 | Processing Time | - |
| Actor 模型 | Actor Model | - |
| 通信顺序进程 | Communicating Sequential Processes | CSP |
| 消息传递 | Message Passing | - |
| 进程演算 | Process Calculus | - |
| 双模拟 | Bisimulation | - |
| 类型系统 | Type System | - |
| 物化视图 | Materialized View | MV |
| 持续查询 | Continuous Query | CQ |

---

## Appendix B: Flink Version Annotations

| Annotation | Meaning |
|------------|---------|
| [Flink 1.x] | Features introduced in Flink 1.x versions |
| [Flink 2.0+] | Features introduced in Flink 2.0 and later |
| [Flink 2.4] | Features planned/introduced in Flink 2.4 |
| [Flink 2.5+] | Features planned/introduced in Flink 2.5 and later |
| [Flink 3.0] | Features planned for Flink 3.0 |
| [GA] | General Availability - production ready |
| [Preview] | Preview feature - early access |

---

**Document Version History**:

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-04-04 | Initial English version translated from GLOSSARY.md |

---

*This document is the English version of the AnalysisDataFlow project glossary. For the Chinese source version, please refer to [GLOSSARY.md](./GLOSSARY.md)*

