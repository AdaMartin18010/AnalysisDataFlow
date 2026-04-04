# AnalysisDataFlow Glossary (English)

> **Version**: v1.0 | **Last Updated**: 2026-04-04 | **Scope**: Project-wide
>
> This document serves as the authoritative terminology reference for the AnalysisDataFlow project, organized alphabetically and covering stream computing theory, Flink engineering practices, and frontier technologies.

---

## Table of Contents

- [Navigation](#navigation)
- [Category Index](#category-index)
- [A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [Q](#q) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [W](#w)

---

## Navigation

| Category | Term Count | Main Domains |
|----------|------------|--------------|
| [Core Terms](#1-core-terms) | 35+ | Stream Computing, Batch Processing, Real-time Processing |
| [Theoretical Terms](#2-theoretical-terms) | 40+ | Process Calculus, Formal Verification, Type Theory |
| [Flink Terms](#3-flink-terms) | 50+ | Core Concepts, APIs, Configuration |
| [Engineering Terms](#4-engineering-terms) | 30+ | Design Patterns, Architecture, Operations |
| [Frontier Terms](#5-frontier-terms) | 35+ | AI Agents, Stream Databases, Cloud-Native |

---

## Category Index

### 1. Core Terms

- **Stream Computing**: Dataflow, Event Time, Processing Time, Watermark, Window
- **Batch Processing**: Batch Processing, Bounded Stream, Checkpoint
- **Real-time Processing**: Real-time Processing, Latency, Throughput

### 2. Theoretical Terms

- **Process Calculus**: CCS, CSP, π-Calculus, Actor Model, Session Types
- **Formal Verification**: Bisimulation, Model Checking, TLA+, Iris
- **Type Theory**: FG/FGG, DOT, Path-Dependent Types

### 3. Flink Terms

- **Core Concepts**: JobManager, TaskManager, Operator, State Backend
- **APIs**: DataStream API, Table API, SQL
- **Configuration**: Parallelism, Checkpoint Interval, Watermark Strategy

### 4. Engineering Terms

- **Design Patterns**: Windowed Aggregation, Async I/O, Side Output
- **Architecture**: Microservices, Event-Driven Architecture, Data Mesh
- **Operations**: Backpressure, Monitoring, Autoscaling

### 5. Frontier Terms

- **AI Agents**: AI Agent, ReAct, MCP, A2A, Agentic Workflow, FLIP-531
- **Serverless**: Serverless Flink, Scale-to-Zero, FaaS
- **Optimization**: Adaptive Execution Engine, Smart Checkpointing, GPU Acceleration
- **Stream-Batch**: Stream-Batch Unification, Unified Execution Engine

---

## A

### Adaptive Execution Engine (AEE) [Flink 1.17+]

**Definition**: An intelligent execution optimization framework introduced in Flink that dynamically adjusts execution plans, resource allocation, and parallelism based on runtime statistics.

**Formal Definition**:

```
AEE-V2 = (𝒫, ℳ, 𝒜, 𝒞, ℛ, δ, π)
```

Where 𝒫 is the physical execution plan, ℳ is runtime metrics, 𝒜 is adaptive actions, 𝒞 is constraints, ℛ is the re-optimizer, δ is the decision function, and π is the performance prediction model.

**Core Capabilities**: Automatic skew handling, dynamic parallelism adjustment, adaptive resource allocation

**Related**: [Smart Checkpointing](#s), [Backpressure](#b), [Parallelism](#p)

**Reference**:

- `Flink/02-core-mechanisms/adaptive-execution-engine-v2.md` (Def-F-02-87, Thm-F-02-56)

---

### Actor Model

**Definition**: A concurrent computing model where the basic unit of computation is an Actor—an autonomous entity capable of receiving messages, making decisions, creating new Actors, and sending messages.

**Formal Definition**:

```
Actor ::= ⟨Mailbox, Behavior, State, Children, Supervisor⟩
```

**Related**: [CSP](#c), [π-Calculus](#p), [Message Passing](#m)

**Reference**:

- `Struct/01-foundation/01.03-actor-model-formalization.md` (Def-S-03-01)
- `Struct/03-relationships/03.01-actor-to-csp-encoding.md`

---

### AI Agent

**Definition**: An intelligent system capable of autonomously perceiving, reasoning, acting, and learning in an environment, formally defined as a sextuple:

```
𝒜_agent ≜ ⟨𝒮, 𝒫, 𝒟, 𝒜, ℳ, 𝒢⟩
```

Where 𝒮 is the state space, 𝒫 is perception, 𝒟 is decision-making, 𝒜 is actions, ℳ is memory, and 𝒢 is goals.

**Flink Integration**: [Flink Agent](#f) is an AI Agent implementation based on the stream computing framework.

**Related**: [ReAct](#r), [MCP](#m), [A2A](#a), [Multi-Agent](#m), [FLIP-531](#f)

**Reference**:

- `Knowledge/06-frontier/ai-agent-streaming-architecture.md` (Def-K-06-110)
- `Flink/12-ai-ml/flink-agents-flip-531.md` (Def-F-12-30)

---

### A2A Protocol (Agent-to-Agent Protocol) [Google 2025]

**Definition**: An open Agent interoperability standard proposed by Google, supporting task delegation, state synchronization, and result return between Agents.

**Formal Definition**:

```
A2A_Flink = ⟨𝒫, ℳ, 𝒮, 𝒜⟩
```

Where 𝒫 is the set of participating Agents, ℳ is message types, 𝒮 is the session state machine, and 𝒜 is the authentication and authorization mechanism.

**Task State Flow**: `pending → working → input-required → completed/failed`

**Related**: [AI Agent](#a), [MCP](#m), [Orchestration](#o), [FLIP-531](#f)

**Reference**:

- `Flink/12-ai-ml/flink-agents-flip-531.md` (Def-F-12-33)
- `Knowledge/06-frontier/a2a-protocol-agent-communication.md`

---

### Aligned Checkpoint

**Definition**: A mechanism in Flink where an operator triggers a state snapshot only after receiving barriers from **all** input channels.

**Formal Definition**:

```
AlignedSnapshot(t, n) ⟺ ∀c ∈ Inputs(t): Barrier(n) ∈ Received(c)
```

**Related**: [Unaligned Checkpoint](#u), [Barrier](#b), [Exactly-Once](#e)

**Reference**:

- `Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md` (Def-F-02-03)
- `Struct/04-proofs/04.01-flink-checkpoint-correctness.md` (Thm-S-17-01)

---

### Async I/O

**Definition**: A pattern that allows stream processing operators to execute external system calls concurrently, avoiding blocking of the data stream processing.

**Formal Definition**:

```
AsyncFunction: I × C → Future[O]
```

Where C is the concurrency parameter controlling the number of simultaneous asynchronous requests.

**Related**: [Backpressure](#b), [Enrichment](#e), [Concurrency](#c)

**Reference**:

- `Knowledge/02-design-patterns/pattern-async-io-enrichment.md`
- `Flink/02-core-mechanisms/async-execution-model.md`

---

### At-Least-Once

**Definition**: A delivery semantics where the stream computing system guarantees that the effect of each input record on the external world occurs **at least once**.

**Formal Definition**:

```
∀r ∈ I. c(r, 𝒯) ≥ 1
```

Where c(r, 𝒯) is the causal effect count.

**Related**: [At-Most-Once](#a), [Exactly-Once](#e), [Delivery Guarantee](#d)

**Reference**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-03)

---

### At-Most-Once

**Definition**: A delivery semantics where the stream computing system guarantees that the effect of each input record on the external world occurs **at most once**, allowing data loss.

**Formal Definition**:

```
∀r ∈ I. c(r, 𝒯) ≤ 1
```

**Related**: [At-Least-Once](#a), [Exactly-Once](#e), [Best-Effort](#b)

**Reference**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-02)

---

## B

### Backpressure

**Definition**: A flow control signal mechanism in stream processing systems that propagates upstream when downstream processing speed is lower than upstream.

**Principle**: Credit-based flow control that pauses sending when the receive buffer is full.

**Related**: [Flow Control](#f), [Buffer](#b), [Credit-Based](#c)

**Reference**:

- `Flink/02-core-mechanisms/backpressure-and-flow-control.md`
- `Knowledge/09-anti-patterns/anti-pattern-08-ignoring-backpressure.md`

---

### Barrier (Checkpoint Barrier)

**Definition**: A special control event injected into the data stream in Flink, used to separate data boundaries between different checkpoints.

**Formal Definition**:

```
Barrier(n) = ⟨Type = CONTROL, checkpointId = n, timestamp = ts⟩
```

**Related**: [Checkpoint](#c), [Aligned Checkpoint](#a), [Unaligned Checkpoint](#u)

**Reference**:

- `Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md` (Def-F-02-02)

---

### Batch Processing

**Definition**: A computing pattern that processes finite, bounded datasets where all data is fully available before computation begins.

**Characteristics**:

- Input data is bounded
- Full dataset is accessible
- Latency-insensitive, throughput-oriented

**Related**: [Stream Processing](#s), [Bounded Stream](#b), [Lambda Architecture](#l)

**Reference**:

- `Struct/01-foundation/01.04-dataflow-model-formalization.md`

---

### Best-Effort

**Definition**: A delivery semantics that provides no consistency guarantees—the system attempts to process data but does not guarantee no loss or no duplication.

**Related**: [At-Most-Once](#a), [Delivery Guarantee](#d)

---

### Bisimulation

**Definition**: A relation in process algebra for determining behavioral equivalence between two processes, requiring that both processes can simulate each other on all possible actions.

**Formal Definition**:

```
R is a bisimulation ⟺ ∀(P,Q)∈R. ∀α. P→αP' ⇒ ∃Q'. Q→αQ' ∧ (P',Q')∈R
```

**Related**: [Process Calculus](#p), [Trace Equivalence](#t), [CCS](#c)

**Reference**:

- `Struct/03-relationships/03.04-bisimulation-equivalences.md` (Thm-S-15-01)

---

### Bounded Stream

**Definition**: A data stream with a finite amount of data, the data abstraction for batch processing.

**Formal Definition**:

```
Bounded(S) ⟺ |S| < ∞
```

**Related**: [Unbounded Stream](#u), [Batch Processing](#b)

---

### Buffer

**Definition**: A memory area in stream processing used for temporarily storing data between producers and consumers.

**Related**: [Backpressure](#b), [Queue](#q), [Network Buffer](#n)

---

## C

### CALM Theorem

**Definition**: Consistency As Logical Monotonicity—a logically monotonic program can guarantee consistency without coordination.

**Formal Statement**:

```
Program P requires no coordination ⟺ P is logically monotonic
```

**Related**: [Eventual Consistency](#e), [Coordination](#c)

**Reference**:

- `Struct/02-properties/02.06-calm-theorem.md` (Thm-S-02-08)

---

### Causal Consistency

**Definition**: A consistency model in distributed systems that preserves the ordering of causally dependent operations.

**Formal Definition**:

```
∀op_i, op_j. op_i ≺hb op_j ⇒ op_i ≺obs op_j
```

**Related**: [Strong Consistency](#s), [Eventual Consistency](#e), [Happens-Before](#h)

**Reference**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Def-S-08-08)

---

### CEP (Complex Event Processing)

**Definition**: A technology for detecting complex patterns from event streams and generating composite events.

**Formal Definition**:

```
CEP: Stream × Pattern → DetectedEvents
```

**Related**: [Pattern Matching](#p), [Event Pattern](#e), [Window](#w)

**Reference**:

- `Knowledge/02-design-patterns/pattern-cep-complex-event.md`

---

### CCS (Calculus of Communicating Systems)

**Definition**: A process algebra based on labeled synchronization proposed by Milner in 1980.

**Syntax**:

```
P, Q ::= 0 | α.P | P + Q | P | Q | P \ L | P[f]
```

**Related**: [CSP](#c), [π-Calculus](#p), [Process Algebra](#p)

**Reference**:

- `Struct/01-foundation/01.02-process-calculus-primer.md` (Def-S-02-01)

---

### CDC (Change Data Capture)

**Definition**: A technology for capturing database change events (inserts, updates, deletes) and propagating them to downstream systems in real-time.

**Related**: [Debezium](#d), [Streaming ETL](#s), [Log Mining](#l)

**Reference**:

- `Flink/04-connectors/flink-cdc-3.0-data-integration.md`
- `Flink/04-connectors/04.04-cdc-debezium-integration.md`

---

### Checkpoint

**Definition**: A globally consistent snapshot of a distributed stream processing job at a specific moment, used for fault recovery.

**Formal Definition**:

```
CP = ⟨ID, TS, {S_i}_{i∈Tasks}, Metadata⟩
```

**Related**: [Savepoint](#s), [State Backend](#s), [Recovery](#r)

**Reference**:

- `Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md` (Def-F-02-01)
- `Struct/04-proofs/04.01-flink-checkpoint-correctness.md` (Thm-S-17-01)

---

### Chandy-Lamport Algorithm

**Definition**: A classical algorithm for capturing globally consistent snapshots in distributed systems, the theoretical foundation of Flink Checkpoint.

**Related**: [Global Snapshot](#g), [Consistent Cut](#c), [Checkpoint](#c)

**Reference**:

- `Struct/04-proofs/04.03-chandy-lamport-consistency.md` (Thm-S-19-01)

---

### Choreographic Programming

**Definition**: A distributed programming paradigm that describes multi-party interaction protocols from a global perspective, then projects them to individual participants.

**Related**: [Session Types](#s), [Endpoint Projection](#e), [Deadlock Freedom](#d)

**Reference**:

- `Struct/06-frontier/06.02-choreographic-streaming-programming.md`
- `Struct/04-proofs/04.07-deadlock-freedom-choreographic.md` (Thm-S-23-01)

---

### Cloud-Native

**Definition**: A methodology for building and running applications that exploits the advantages of cloud computing, emphasizing containerization, microservices, continuous delivery, and DevOps.

**Related**: [Kubernetes](#k), [Containerization](#c), [Microservices](#m)

**Reference**:

- `Flink/10-deployment/flink-kubernetes-operator-deep-dive.md`
- `Knowledge/06-frontier/serverless-stream-processing-architecture.md`

---

### Concurrency

**Definition**: The ability of multiple computational tasks to execute during overlapping time periods, distinct from parallelism.

**Related**: [Parallelism](#p), [Race Condition](#r), [Synchronization](#s)

---

### Consistency Model

**Definition**: A set of rules defining the visibility and ordering of data operations in distributed systems.

**Hierarchy**: Strong Consistency → Causal Consistency → Eventual Consistency

**Related**: [Linearizability](#l), [Serializability](#s), [CAP Theorem](#c)

**Reference**:

- `Struct/02-properties/02.02-consistency-hierarchy.md` (Thm-S-08-03)

---

## D

### Dataflow Model

**Definition**: A computational model for processing continuous data streams, where data flows through a directed graph of processing elements.

**Related**: [Stream Processing](#s), [Pipeline](#p), [DAG](#d)

---

### Delivery Guarantee

**Definition**: The set of promises a stream processing system makes about message processing semantics.

**Levels**: Best-Effort → At-Most-Once → At-Least-Once → Exactly-Once

**Related**: [Exactly-Once](#e), [Fault Tolerance](#f)

---

## E

### Exactly-Once

**Definition**: A delivery semantics where the stream computing system guarantees that the effect of each input record on the external world occurs **exactly once**.

**Formal Definition**:

```
∀r ∈ I. c(r, 𝒯) = 1
```

**Related**: [At-Least-Once](#a), [At-Most-Once](#a), [Idempotency](#i)

**Reference**:

- `Flink/02-core-mechanisms/exactly-once-end-to-end.md`
- `Struct/04-proofs/04.02-flink-exactly-once-correctness.md` (Thm-S-18-01)

---

### Event Time

**Definition**: The time at which an event actually occurred, typically recorded as a timestamp in the event data itself.

**Related**: [Processing Time](#p), [Watermark](#w), [Timestamp](#t)

---

### Event-Driven Architecture

**Definition**: An architectural pattern where system behavior is determined by events—significant changes in state.

**Related**: [Microservices](#m), [Message Queue](#m), [Pub/Sub](#p)

---

## F

### Fault Tolerance

**Definition**: The ability of a system to continue operating properly in the event of failures of some of its components.

**Related**: [Checkpoint](#c), [Recovery](#r), [High Availability](#h)

---

### Flink

**Definition**: An open-source stream processing framework for distributed, high-performing, always-available, and accurate data streaming applications.

**Related**: [DataStream API](#d), [Table API](#t), [SQL](#s)

---

## G

### Global Snapshot

**Definition**: A consistent snapshot of the entire distributed system state at a particular point in logical time.

**Related**: [Checkpoint](#c), [Chandy-Lamport Algorithm](#c), [Consistent Cut](#c)

---

## H

### Happens-Before

**Definition**: A relation between events in a distributed system indicating that one event causally affects another.

**Related**: [Causal Consistency](#c), [Vector Clock](#v)

---

## I

### Idempotency

**Definition**: The property of an operation where applying it multiple times has the same effect as applying it once.

**Related**: [Exactly-Once](#e), [Fault Tolerance](#f)

---

## K

### Kafka

**Definition**: A distributed event streaming platform used for high-performance data pipelines, streaming analytics, and data integration.

**Related**: [CDC](#c), [Event Streaming](#e), [Connector](#c)

---

## L

### Lakehouse

**Definition**: An architectural pattern that combines the best aspects of data lakes and data warehouses.

**Related**: [Streaming Lakehouse](#s), [Delta Lake](#d), [Iceberg](#i)

---

### Latency

**Definition**: The time delay between the occurrence of an event and the system response to that event.

**Related**: [Throughput](#t), [SLA](#s), [Real-time](#r)

---

## M

### Materialized View

**Definition**: A database object that contains the results of a query, physically stored and updated incrementally.

**Related**: [Streaming Database](#s), [Continuous Query](#c), [Incremental Update](#i)

---

### Microservices

**Definition**: An architectural style that structures an application as a collection of loosely coupled services.

**Related**: [Event-Driven Architecture](#e), [Containerization](#c), [Cloud-Native](#c)

---

## P

### Parallelism

**Definition**: The degree to which a stream processing job can be executed concurrently across multiple computing resources.

**Related**: [Concurrency](#c), [Scaling](#s), [Throughput](#t)

---

### Process Calculus

**Definition**: A family of formalisms for modeling concurrent systems and their interactions.

**Related**: [CCS](#c), [CSP](#c), [π-Calculus](#p), [Actor Model](#a)

---

### Processing Time

**Definition**: The time at which an event is processed by the system, typically the current wall-clock time.

**Related**: [Event Time](#e), [Watermark](#w), [Ingestion Time](#i)

---

## Q

### Queryable State

**Definition**: A feature allowing external systems to query the internal state of a running Flink application.

**Related**: [State Backend](#s), [Monitoring](#m)

---

## R

### Recovery

**Definition**: The process of restoring a system to a correct state after a failure has occurred.

**Related**: [Checkpoint](#c), [Fault Tolerance](#f), [Savepoint](#s)

---

## S

### Savepoint

**Definition**: A manually triggered, consistent snapshot of a Flink application state, used for planned upgrades and migrations.

**Related**: [Checkpoint](#c), [Recovery](#r), [State Backend](#s)

---

### Session Window

**Definition**: A window that groups events into sessions based on periods of activity separated by gaps of inactivity.

**Related**: [Window](#w), [Event Time](#e), [CEP](#c)

---

### State Backend

**Definition**: The mechanism and storage system used by Flink to maintain and checkpoint operator state.

**Types**: MemoryStateBackend, FsStateBackend, RocksDBStateBackend

**Related**: [Checkpoint](#c), [Queryable State](#q), [Recovery](#r)

---

### Stream Processing

**Definition**: A computing paradigm for processing continuous, potentially unbounded data streams in real-time.

**Related**: [Batch Processing](#b), [Event Time](#e), [Dataflow](#d)

---

## T

### Table API

**Definition**: A declarative, unified API for batch and stream processing in Flink, based on relational concepts.

**Related**: [SQL](#s), [DataStream API](#d), [Flink](#f)

---

### Throughput

**Definition**: The rate at which a system can process data, typically measured in records or bytes per second.

**Related**: [Latency](#l), [Backpressure](#b), [Parallelism](#p)

---

### Time Window

**Definition**: A window that groups events based on time boundaries.

**Types**: Tumbling Window, Sliding Window, Session Window

**Related**: [Window](#w), [Event Time](#e), [Watermark](#w)

---

## U

### Unaligned Checkpoint

**Definition**: A checkpoint mechanism where operators can snapshot state without waiting for barriers from all inputs, reducing latency impact.

**Related**: [Aligned Checkpoint](#a), [Barrier](#b), [Checkpoint](#c)

---

### Unbounded Stream

**Definition**: A data stream with no predefined end, potentially infinite.

**Related**: [Bounded Stream](#b), [Stream Processing](#s)

---

## W

### Watermark

**Definition**: A metadata record in stream processing that indicates the progress of event time and helps determine when windows can be closed.

**Formal Definition**:

```
Watermark(t) ⟺ ∀e ∈ Stream: timestamp(e) ≤ t ⟹ e has arrived
```

**Related**: [Event Time](#e), [Window](#w), [Late Data](#l)

**Reference**:

- `Flink/02-core-mechanisms/time-semantics-and-watermark.md`
- `Struct/02-properties/02.03-watermark-monotonicity.md` (Lemma-S-04-02)

---

### Window

**Definition**: A logical grouping of events based on time or other criteria for aggregation and analysis.

**Types**: Tumbling, Sliding, Session, Global

**Related**: [Windowed Aggregation](#w), [Event Time](#e), [Watermark](#w)

---

## Appendix: Abbreviations

| Abbreviation | Full Form |
|--------------|-----------|
| AEE | Adaptive Execution Engine |
| AL | At-Least-Once |
| AM | At-Most-Once |
| CEP | Complex Event Processing |
| CDC | Change Data Capture |
| CCS | Calculus of Communicating Systems |
| CSP | Communicating Sequential Processes |
| EO | Exactly-Once |
| FLIP | Flink Improvement Proposal |
| MCP | Model Context Protocol |
| SLA | Service Level Agreement |
| SQL | Structured Query Language |

---

*This glossary follows the AnalysisDataFlow six-section documentation template*
