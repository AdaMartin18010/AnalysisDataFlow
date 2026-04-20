# Pattern: Stateful Computation

> **Language**: English | **Translated from**: [Knowledge/02-design-patterns/pattern-stateful-computation.md](../../../Knowledge/02-design-patterns/pattern-stateful-computation.md) | **Translation date**: 2026-04-20
>
> **Stage**: Knowledge | **Prerequisites**: [Related Documents] | **Formalization Level**: L3
>
> **Pattern ID**: 05/7 | **Series**: Knowledge/02-design-patterns | **Formalization Level**: L4-L5
>
> This pattern resolves the core contradiction between **state consistency**, **fault-tolerant recovery**, and **large-scale state management** in distributed stream processing.

---

## Table of Contents

- [Pattern: Stateful Computation](#pattern-stateful-computation)
  - [Table of Contents](#table-of-contents)
  - [1. Definitions](#1-definitions)
    - [Def-K-02-04 (Operator State)](#def-k-02-04-operator-state)
    - [Def-K-02-05 (Keyed State)](#def-k-02-05-keyed-state)
    - [Def-K-02-06 (State Backend)](#def-k-02-06-state-backend)
    - [Def-K-02-07 (State TTL)](#def-k-02-07-state-ttl)
    - [Def-K-02-08 (Queryable State)](#def-k-02-08-queryable-state)
  - [2. Properties](#2-properties)
    - [Prop-K-02-03 (State Partitioning Determinism)](#prop-k-02-03-state-partitioning-determinism)
    - [Prop-K-02-04 (TTL Validity Boundary)](#prop-k-02-04-ttl-validity-boundary)
    - [Prop-K-02-05 (State Backend Access Latency)](#prop-k-02-05-state-backend-access-latency)
  - [3. Relations](#3-relations)
    - [Relationship with Event Time Processing](#relationship-with-event-time-processing)
    - [Relationship with Windowed Aggregation](#relationship-with-windowed-aggregation)
    - [Relationship with Checkpoint Mechanism](#relationship-with-checkpoint-mechanism)
  - [4. Argumentation](#4-argumentation)
    - [4.1 Challenges of Distributed Stateful Computation](#41-challenges-of-distributed-stateful-computation)
    - [4.2 State Backend Selection Argument](#42-state-backend-selection-argument)
    - [4.3 Applicability Analysis](#43-applicability-analysis)
  - [5. Proof / Engineering Argument](#5-proof-engineering-argument)
    - [5.1 Keyed State Local Determinism Argument](#51-keyed-state-local-determinism-argument)
    - [5.2 Incremental Checkpoint Consistency Argument](#52-incremental-checkpoint-consistency-argument)
    - [5.3 State Backend Selection Engineering Trade-offs](#53-state-backend-selection-engineering-trade-offs)
  - [6. Examples](#6-examples)
    - [6.1 Keyed State Basic Usage](#61-keyed-state-basic-usage)
    - [6.2 State TTL Configuration](#62-state-ttl-configuration)
    - [6.3 State Backend Configuration](#63-state-backend-configuration)
    - [6.4 Queryable State Implementation](#64-queryable-state-implementation)
  - [7. Visualizations](#7-visualizations)
    - [7.1 State Management Architecture Diagram](#71-state-management-architecture-diagram)
    - [7.2 State Backend Selection Decision Tree](#72-state-backend-selection-decision-tree)
  - [8. Formal Guarantees](#8-formal-guarantees)
    - [8.1 Dependent Formal Definitions](#81-dependent-formal-definitions)
    - [8.2 Satisfied Formal Properties](#82-satisfied-formal-properties)
    - [8.3 Property Preservation in Pattern Composition](#83-property-preservation-in-pattern-composition)
    - [8.4 Boundary Conditions and Constraints](#84-boundary-conditions-and-constraints)
    - [8.5 Formal Characteristics of State Backends](#85-formal-characteristics-of-state-backends)
  - [9. References](#9-references)

---

## 1. Definitions

### Def-K-02-04 (Operator State)

**Definition**: Operator State is global state bound to an operator instance; all records in the stream share the same state replica [^1].

Formally, let the operator instance be $o_i$, then:

$$
S_{\text{operator}}(o_i) \in \mathcal{V}
$$

Where $\mathcal{V}$ is the state value space. Typical uses of Operator State include: Kafka Source offset recording, Broadcast State global configuration table.

---

### Def-K-02-05 (Keyed State)

**Definition**: Keyed State is local state partitioned by key; each key has an independent state replica [^1].

$$
S_{\text{keyed}}: (\text{TaskInstance} \times \text{Key}) \to \text{StateValue}
$$

Keyed State access is strictly restricted to operators after `keyBy()`. Flink guarantees that all records with the same key are routed to the same parallel subtask, ensuring serialized state updates (**Thm-S-03-01**).

**State Types** [^1]:

| Type | Description | Scenario |
|------|-------------|----------|
| ValueState | Single value state | Counter |
| ListState | List state | Historical records |
| MapState | Map structure | Key-value collection |
| ReducingState | Reducible state | Incremental aggregation |

---

### Def-K-02-06 (State Backend)

**Definition**: State Backend is the pluggable abstraction layer in Flink responsible for state storage, access, and Checkpoint snapshot persistence [^2].

$$
\mathcal{B} = (S_{\text{storage}}, \Phi_{\text{access}}, \Psi_{\text{snapshot}}, \Omega_{\text{recovery}})
$$

Where:

- $S_{\text{storage}}$: Physical storage medium (JVM Heap or local disk)
- $\Phi_{\text{access}}$: State read/write interface
- $\Psi_{\text{snapshot}}$: Asynchronous snapshot mechanism
- $\Omega_{\text{recovery}}$: Fault recovery process

**Main Implementation Comparison**:

| Characteristic | HashMapStateBackend | RocksDBStateBackend |
|----------------|---------------------|---------------------|
| Storage location | JVM Heap memory | Local disk (RocksDB) |
| State size limit | Limited by TaskManager memory | Limited by local disk capacity |
| Access latency | Extremely low (direct memory access) | Low (memory + disk cache) |
| Incremental Checkpoint | Supported (requires configuration) | Native support (based on SST) |
| Large state support | Not suitable (> 100MB) | Suitable (TB level) |

---

### Def-K-02-07 (State TTL)

**Definition**: TTL (Time-To-Live) defines the valid lifetime of state. State exceeding TTL is considered expired and triggers cleanup [^6].

$$
\text{Valid}(S_k, t) \iff t - \text{LastAccess}(S_k) < \text{TTL}
$$

**Cleanup Strategies**:

| Strategy | Trigger Timing | Applicable Backend |
|----------|---------------|-------------------|
| Full Snapshot | At Checkpoint | General |
| Incremental | At state access | General |
| RocksDB Compaction | During compaction | RocksDB-specific |

---

### Def-K-02-08 (Queryable State)

**Definition**: Queryable State allows external clients to read-only access operator internal Keyed State via RPC [^8].

```
Client ──RPC──► Queryable State Server ◄──Local── Task Manager
                                                │
                                                ▼
                                          Keyed State
```

**Limitations**: Read-only access, only supports Keyed State, high network overhead. Queryable State has been marked as deprecated in Flink 1.17+; REST API or external storage is recommended instead [^8].

---

## 2. Properties

### Prop-K-02-03 (State Partitioning Determinism)

**Proposition**: Keyed State is distributed to parallel subtasks by the hash value of the key. All records with the same key are necessarily routed to the same subtask.

$$
\text{Partition}(key) = \text{hash}(key) \mod \text{parallelism}
$$

**Derivation**:

1. The `keyBy()` operator partitions based on the hash value of the key
2. Flink's data exchange layer guarantees that data with the same partition number is sent to the same Task instance
3. Therefore, state updates for the same key are executed serially within a single thread
4. Combined with **Lemma-S-03-01** (Actor mailbox serial processing lemma), Keyed State updates satisfy local determinism (**Thm-S-03-01**)

---

### Prop-K-02-04 (TTL Validity Boundary)

**Proposition**: Let the last access time of state be $t_{\text{last}}$ and TTL be $T$. The necessary and sufficient condition for state $S_k$ to be valid at time $t$ is:

$$
t - t_{\text{last}} < T
$$

**Engineering constraints**:

- TTL cleanup is asynchronous/lazy; expired state may still be briefly accessed before cleanup
- `StateVisibility.NeverReturnExpired` configuration ensures expired state is not returned
- TTL setting should be less than the Checkpoint retention period to avoid state bloat causing increased recovery time

---

### Prop-K-02-05 (State Backend Access Latency)

**Proposition**: Let the state size be $|S|$. HashMapStateBackend access latency is $O(1)$, independent of state size; RocksDBStateBackend access latency is $O(\log |S|)$ (based on LSM-Tree level lookup).

**Performance Comparison** (typical scenarios):

| State Size | HashMap Access Latency | RocksDB Access Latency | Recommendation |
|-----------|----------------------|----------------------|----------------|
| 10 MB | ~0.1 μs | ~5 μs | HashMap |
| 100 MB | ~0.5 μs | ~5 μs | HashMap |
| 1 GB | OOM | ~10 μs | RocksDB |
| 100 GB | N/A | ~50 μs | RocksDB |

---

## 3. Relations

### Relationship with Event Time Processing

Stateful computation is deeply coupled with Event Time [^10]:

- State access can combine event timestamps to implement time-windowed state (e.g., session windows)
- Watermark advancement can drive state expiration cleanup (TTL)
- Event time monotonicity guarantees states are updated in the correct temporal order

### Relationship with Windowed Aggregation

Windowed aggregation internally depends on Keyed State implementation [^11]:

- Tumbling/Sliding/Session Window aggregation results are stored in ValueState or ListState
- Window trigger state (Trigger State) is stored separately from computation state
- Window Allowed Lateness mechanism relies on persistent retention of state

### Relationship with Checkpoint Mechanism

Checkpoint is the foundation of fault tolerance for stateful computation [^2][^9]:

- State backend implements the snapshot requirements of **Thm-S-17-01**, capturing a consistent global state
- Incremental Checkpoint only persists changed portions of state, optimizing storage efficiency without changing consistency guarantees
- During fault recovery, state is reconstructed from the Checkpoint, and combined with Source replay to achieve Exactly-Once (**Thm-S-18-01**)

---

## 4. Argumentation

### 4.1 Challenges of Distributed Stateful Computation

In distributed stream processing, stateful computation needs to maintain context information across events:

| Challenge Dimension | Problem Description | Typical Impact |
|--------------------|---------------------|----------------|
| **Fault-tolerant consistency** | How to recover state when a node fails | Exactly-Once semantics violation |
| **State scale** | Storage and access of massive key-value pairs | OOM, GC pauses |
| **State expiration** | Cleanup of invalid state | State bloat |
| **External queries** | External access to runtime state | Insufficient observability |

**Formal description**: Let the state of operator $o_i$ at time $t$ be $S_t(o_i)$. Stateful computation satisfies:

$$
\text{Output}(o_i, r_j, t) = f(r_j, S_{t-1}(o_i))
$$

That is, output depends on historically accumulated state, so fault recovery must precisely reconstruct historical state.

**Core Contradiction Triangle**:

```
         Consistency
              ▲
             /|\
            / | \
           /  |  \
          /   |   \
Low Latency ◄──────────────► Large Scale
```

- Strong consistency requires Barrier alignment, increasing latency
- Large-scale state requires disk storage, with high access latency
- Low latency requires in-memory computation, limiting state scale

---

### 4.2 State Backend Selection Argument

**HashMapStateBackend Applicable Scenarios** [^9]:

- State size < 100MB
- Requires extremely low access latency (< 1ms)
- Short window aggregation (minute-level)
- Configuration parameter state

**RocksDBStateBackend Applicable Scenarios** [^9]:

- State size > 100MB or unknown
- Long window aggregation (hour/day-level)
- Large keyspace (millions of keys)
- Incremental Checkpoint optimizes storage cost

**Selection Decision Tree** [^9]:

```
State size < 30% of TM heap memory?
├── Yes ──► HashMapStateBackend (low latency)
└── No ──► RocksDBStateBackend (large state)
```

---

### 4.3 Applicability Analysis

**Recommended** [^1][^9]:

| Scenario | Rationale | Configuration |
|----------|-----------|---------------|
| Session windows | Cross-event session maintenance | ValueState + TTL |
| Cumulative metrics | Daily/monthly cumulative statistics | ReducingState + Incremental Checkpoint |
| CEP pattern matching | NFA state machine | MapState + Short TTL |
| Deduplication filtering | Exact deduplication | ValueState + Expiration cleanup |

**Not Recommended** [^1]:

| Scenario | Rationale | Alternative |
|----------|-----------|-------------|
| Pure stateless transformation | No state needed | map/filter |
| Large object caching | Not suitable for caching | Redis |
| Cross-job sharing | Job isolation | External database |

---

## 5. Proof / Engineering Argument

### 5.1 Keyed State Local Determinism Argument

**Theorem Statement** (citing **Thm-S-03-01**) [^12]:

> In the Actor model, the local execution of a single Actor is deterministic; that is, for the same initial state and the same message sequence, the output state sequence is unique.

**Mapping to Flink Keyed State**:

1. Flink's `keyBy()` partitions the stream by key, equivalent to creating a logical Actor for each key
2. All records with the same key are delivered to the same Task thread in FIFO order (**Lemma-S-03-01**)
3. Keyed State `update()` operations execute serially within a single thread, with no data races
4. Therefore, the evolution of Keyed State satisfies local determinism

**Engineering significance**: Local determinism is the foundation for guaranteeing reproducibility after fault recovery. Even though parallel processing across different keys may have scheduling non-determinism, the state evolution path of a single key is deterministic.

---

### 5.2 Incremental Checkpoint Consistency Argument

**Argument Goal**: Prove that incremental Checkpoint optimizes storage efficiency without breaking global state consistency (**Thm-S-17-01**).

**Argument Structure**:

1. **Completeness of state snapshot**: Each Checkpoint captures incremental changes plus a baseline full-state snapshot, which can completely reconstruct the global state at that moment
2. **SST immutability**: Once RocksDB's SST files are generated, they are not modified; incremental snapshots only need to reference new SSTs, naturally satisfying the consistent cut requirement
3. **Recovery correctness**: During recovery, Flink automatically merges baseline and incremental files; the reconstructed state is semantically equivalent to a full snapshot
4. **No orphan messages**: Incremental Checkpoint does not change Barrier alignment semantics, so in-flight message processing is consistent with full snapshots (**Lemma-S-17-04**)

**Conclusion**: Incremental Checkpoint is an optimized implementation of **Thm-S-17-01**, not a weakened implementation.

---

### 5.3 State Backend Selection Engineering Trade-offs

**Trade-off Matrix**:

| Dimension | HashMapStateBackend | RocksDBStateBackend |
|-----------|---------------------|---------------------|
| Access latency | ~10-100 ns | 1-100 μs |
| State capacity | Several MB - Several GB | TB level |
| GC impact | Large state causes frequent Full GC | Minimal impact on JVM Heap |
| Incremental Checkpoint | Not supported (object-level comparison overhead is high) | Native support (SST-level) |
| Recovery speed | Fast (memory loading) | Medium (requires rebuilding LSM-Tree) |

**Decision Rule**:

$$
\text{Backend} = \begin{cases}
\text{HashMap} & \text{if } |S| < 0.3 \times \text{TM\_Heap} \land \text{Latency} < 1\text{ms} \\
\text{RocksDB} & \text{otherwise}
\end{cases}
$$

Where $|S|$ is the estimated state size and TM_Heap is the TaskManager heap memory.

---

## 6. Examples

### 6.1 Keyed State Basic Usage

```scala
class UserVisitCounter extends ProcessFunction[UserEvent, UserStats] {
  private var visitCountState: ValueState[Long] = _

  override def open(parameters: Configuration): Unit = {
    val descriptor = new ValueStateDescriptor[Long](
      "visit-count", classOf[Long]
    )
    visitCountState = getRuntimeContext.getState(descriptor)
  }

  override def processElement(
    event: UserEvent,
    ctx: Context,
    out: Collector[UserStats]
  ): Unit = {
    val currentCount = Option(visitCountState.value()).getOrElse(0L)
    val newCount = currentCount + 1
    visitCountState.update(newCount)
    out.collect(UserStats(event.userId, newCount))
  }
}
```

---

### 6.2 State TTL Configuration

```scala
val ttlConfig = StateTtlConfig
  .newBuilder(Time.minutes(30))
  .setUpdateType(OnCreateAndWrite)
  .setStateVisibility(NeverReturnExpired)
  .cleanupFullSnapshot()
  .build()

val descriptor = new ValueStateDescriptor[SessionInfo](
  "session", classOf[SessionInfo]
)
descriptor.enableTimeToLive(ttlConfig)
```

---

### 6.3 State Backend Configuration

**HashMapStateBackend** (small state) [^9]:

```scala
env.setStateBackend(new HashMapStateBackend())
env.getCheckpointConfig.setCheckpointStorage("hdfs:///checkpoints")
```

**RocksDBStateBackend** (large state + incremental) [^9]:

```scala
val rocksDbBackend = new EmbeddedRocksDBStateBackend(true) // true = incremental
env.setStateBackend(rocksDbBackend)
env.getCheckpointConfig.setCheckpointStorage("hdfs:///checkpoints")
```

---

### 6.4 Queryable State Implementation

```scala
val descriptor = new ValueStateDescriptor[UserProfile](
  "user-profile", classOf[UserProfile]
)
descriptor.setQueryable("queryable-user-profile")
```

External query [^8]:

```scala
val client = new QueryableStateClient("jobmanager", 9069)
val future = client.getKvState(
  jobId, "queryable-user-profile", "user_123",
  keySerializer, stateDescriptor
)
```

---

## 7. Visualizations

### 7.1 State Management Architecture Diagram

The following Mermaid diagram shows the core components and hierarchical relationships of the Stateful Computation pattern:

```mermaid
graph TB
    subgraph "Input"
        I1[Keyed Stream]
    end

    subgraph "State Backend"
        SB1[HashMap<br/>JVM Heap]
        SB2[RocksDB<br/>Local Disk]
    end

    subgraph "State Types"
        ST1[ValueState]
        ST2[ListState]
        ST3[MapState]
    end

    subgraph "Management"
        LM1[TTL Config]
        LM2[Queryable]
    end

    subgraph "Fault Tolerance"
        FT1[Checkpoint]
        FT2[Incremental]
    end

    I1 --> SB1
    I1 --> SB2
    SB1 --> ST1 & ST2 & ST3
    SB2 --> ST1 & ST2 & ST3
    ST1 --> LM1
    LM1 --> FT1
    ST1 -.-> LM2
    FT1 --> FT2

    style SB1 fill:#bbdefb,stroke:#1565c0
    style SB2 fill:#fff9c4,stroke:#f57f17
    style FT1 fill:#c8e6c9,stroke:#2e7d32
```

---

### 7.2 State Backend Selection Decision Tree

The following decision tree helps select the appropriate state backend in different scenarios:

```mermaid
flowchart TD
    A[State Backend Selection] --> B{State size <br/>< 30% of TM heap memory?}
    B -->|Yes| C{Latency requirement < 1ms?}
    B -->|No| D[RocksDBStateBackend<br/>Large State / Incremental Checkpoint]

    C -->|Yes| E[HashMapStateBackend<br/>Low Latency / Memory Access]
    C -->|No| F{Need incremental Checkpoint?}
    F -->|Yes| D
    F -->|No| G[HashMapStateBackend<br/>Medium State]

    style A fill:#e3f2fd,stroke:#1565c0
    style E fill:#c8e6c9,stroke:#2e7d32
    style D fill:#fff9c4,stroke:#f57f17
    style G fill:#e1bee7,stroke:#6a1b9a
```

---

## 8. Formal Guarantees

This section establishes the formal connection between the Stateful Computation pattern and the Struct/ theoretical layer.

### 8.1 Dependent Formal Definitions

| Definition ID | Name | Source | Role in This Pattern |
|---------------|------|--------|---------------------|
| **Def-S-03-01** | Classic Actor Quadruple | Struct/01.03 | Concurrency model foundation of Keyed State: $\langle \alpha, b, m, \sigma \rangle$ |
| **Def-S-04-01** | Dataflow Graph (DAG) | Struct/01.04 | Stateful operators as stateful vertices $\langle V, E, P, \Sigma, \mathbb{T} \rangle$ |
| **Def-S-17-02** | Consistent Global State | Struct/04.01 | Checkpoint captured state must form a consistent cut |
| **Def-S-18-05** | Idempotence | Struct/04.02 | State update replay must satisfy idempotence |

### 8.2 Satisfied Formal Properties

| Theorem/Lemma ID | Name | Source | Guarantee |
|------------------|------|--------|-----------|
| **Thm-S-03-01** | Actor Local Determinism Theorem | Struct/01.03 | Single-key state update serialization guarantees local determinism |
| **Lemma-S-03-01** | Actor Mailbox Serial Processing Lemma | Struct/01.03 | Messages with the same key are processed in FIFO order |
| **Thm-S-17-01** | Checkpoint Consistency Theorem | Struct/04.01 | State snapshot forms a consistent global state |
| **Thm-S-18-01** | Exactly-Once Correctness Theorem | Struct/04.02 | State recovery + Source replay = Exactly-Once |
| **Lemma-S-18-03** | State Recovery Consistency Lemma | Struct/04.02 | Recovered state is consistent with some moment before the fault |

### 8.3 Property Preservation in Pattern Composition

**Stateful Computation + Event Time**:

- State access can combine event timestamps to implement time-windowed state
- Watermark drives state expiration cleanup (TTL)

**Stateful Computation + Checkpoint**:

- State backend implements the snapshot requirements of **Thm-S-17-01**
- Incremental Checkpoint optimization does not change consistency guarantees

**Stateful Computation + Windowed Aggregation**:

- Window state uses Keyed State implementation
- Window trigger state and computation state are stored separately

### 8.4 Boundary Conditions and Constraints

| Constraint | Formal Description | Violation Consequence |
|------------|-------------------|----------------------|
| Fixed key partitioning | $\text{hash}(k) \mod \text{parallelism}$ unchanged | Key drift, state loss |
| Finite state size | $\|S\| < \infty$ | OOM, job crash |
| Reasonable TTL configuration | TTL < Checkpoint interval $\times N$ | State bloat, increased recovery time |
| Concurrent access isolation | Single key single-thread access | Data race, state corruption |

### 8.5 Formal Characteristics of State Backends

| Backend Type | Storage Model | Consistency Guarantee | Applicable Scenario |
|--------------|---------------|----------------------|---------------------|
| HashMapStateBackend | In-memory KV | **Thm-S-17-01** | Small state (<100MB) |
| RocksDBStateBackend | LSM-Tree | **Thm-S-17-01** | Large state (TB level) |

---

## 9. References

[^1]: Flink State Documentation. <https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/state/>

[^2]: Carbone et al., "State Management in Apache Flink," *PVLDB*, 2017.

[^6]: Flink State TTL. <https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/state/#state-time-to-live-ttl>

[^8]: Flink Queryable State. <https://archive.org/web/*/https://nightlies.apache.org/flink/flink-docs-release-1.16/docs/dev/datastream/fault-tolerance/queryable_state/> <!-- 404 as of 2026-04: deprecated in Flink 1.17+ -->

[^9]: Flink State Backend Selection. [Flink/09-practices/09.03-performance-tuning/state-backend-selection.md](../../Flink/09-practices/09.03-performance-tuning/state-backend-selection.md)

[^10]: Flink Time Semantics. [Flink/02-core/time-semantics-and-watermark.md](../../Flink/02-core/time-semantics-and-watermark.md)

[^11]: Flink Checkpoint Mechanism. [Flink/02-core/checkpoint-mechanism-deep-dive.md](../../Flink/02-core/checkpoint-mechanism-deep-dive.md)

[^12]: Type Safety Derivation. [Struct/02-properties/02.05-type-safety-derivation.md](../../Struct/02-properties/02.05-type-safety-derivation.md)

---

*Document Version: v1.0 | Updated: 2026-04-02*

---

*Document Version: v1.0 | Created: 2026-04-20*
