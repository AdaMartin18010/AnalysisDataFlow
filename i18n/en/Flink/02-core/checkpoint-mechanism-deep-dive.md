---
title: "Flink Checkpoint Mechanism Deep Dive"
translation_status: ai_translated_pending_expert_review
source_version: v4.1
last_sync: "2026-04-15"
---

# Flink Checkpoint Mechanism Deep Dive

> Stage: Flink/02-core-mechanisms | Prerequisites: [02.02-consistency-hierarchy.md](../../Struct/02-properties/02.02-consistency-hierarchy.md) | Formalization Level: L4

---

## Table of Contents

- [Flink Checkpoint Mechanism Deep Dive {#flink-checkpoint-mechanism-deep-dive}](#flink-checkpoint-mechanism-deep-dive)
  - [Table of Contents {#table-of-contents}](#table-of-contents)
  - [1. Definitions {#1-definitions}](#1-definitions)
    - [Def-F-02-01 (Checkpoint Core Abstraction)](#def-f-02-01-checkpoint-core-abstraction)
    - [Def-F-02-02 (Checkpoint Barrier)](#def-f-02-02-checkpoint-barrier)
    - [Def-F-02-03 (Aligned Checkpoint)](#def-f-02-03-aligned-checkpoint)
    - [Def-F-02-04 (Unaligned Checkpoint)](#def-f-02-04-unaligned-checkpoint)
    - [Def-F-02-05 (Incremental Checkpoint)](#def-f-02-05-incremental-checkpoint)
    - [Def-F-02-06 (State Backend)](#def-f-02-06-state-backend)
    - [Def-F-02-07 (Checkpoint Coordinator)](#def-f-02-07-checkpoint-coordinator)
    - [Def-F-02-08 (Changelog State Backend)](#def-f-02-08-changelog-state-backend)
  - [2. Properties {#2-properties}](#2-properties)
    - [Lemma-F-02-01 (Barrier Alignment Guarantees State Consistency)](#lemma-f-02-01-barrier-alignment-guarantees-state-consistency)
    - [Lemma-F-02-02 (Asynchronous Checkpoint Low-Latency Property)](#lemma-f-02-02-asynchronous-checkpoint-low-latency-property)
    - [Lemma-F-02-03 (Incremental Checkpoint Storage Optimization)](#lemma-f-02-03-incremental-checkpoint-storage-optimization)
    - [Prop-F-02-01 (Checkpoint Type Selection Trade-offs)](#prop-f-02-01-checkpoint-type-selection-trade-offs)
  - [3. Relations {#3-relations}](#3-relations)
    - [Relation 1: Flink Checkpoint ↔ Chandy-Lamport Distributed Snapshot](#relation-1-flink-checkpoint--chandy-lamport-distributed-snapshot)
    - [Relation 2: Checkpoint Mechanism ⟹ Exactly-Once Semantics](#relation-2-checkpoint-mechanism--exactly-once-semantics)
    - [Relation 3: State Backend Type ↔ Application Scenarios](#relation-3-state-backend-type--application-scenarios)
  - [4. Argumentation {#4-argumentation}](#4-argumentation)
    - [4.1 Checkpoint Architecture: JM/TM Coordination {#41-checkpoint-architecture-jmtm-coordination}](#41-checkpoint-architecture-jmtm-coordination)
    - [4.2 Aligned vs Unaligned: In-Depth Comparison {#42-aligned-vs-unaligned-in-depth-comparison}](#42-aligned-vs-unaligned-in-depth-comparison)
      - [Aligned Checkpoint Workflow](#aligned-checkpoint-workflow)
      - [Unaligned Checkpoint Workflow](#unaligned-checkpoint-workflow)
    - [4.3 Incremental Checkpoint Engineering Implementation {#43-incremental-checkpoint-engineering-implementation}](#43-incremental-checkpoint-engineering-implementation)
      - [4.3.1 RocksDB Incremental Checkpoint Principles {#431-rocksdb-incremental-checkpoint-principles}](#431-rocksdb-incremental-checkpoint-principles)
      - [Configuration Parameters {#configuration-parameters}](#configuration-parameters)
    - [4.4 State Backend Snapshot Process Details {#44-state-backend-snapshot-process-details}](#44-state-backend-snapshot-process-details)
      - [HashMapStateBackend Snapshot Process {#hashmapstatebackend-snapshot-process}](#hashmapstatebackend-snapshot-process)
      - [RocksDBStateBackend Snapshot Process {#rocksdbstatebackend-snapshot-process}](#rocksdbstatebackend-snapshot-process)
  - [5. Proof / Engineering Argument {#5-proof--engineering-argument}](#5-proof--engineering-argument)
    - [Thm-F-02-01 (System State Equivalence After Checkpoint Recovery) {#thm-f-02-01-system-state-equivalence-after-checkpoint-recovery}](#thm-f-02-01-system-state-equivalence-after-checkpoint-recovery)
    - [Thm-F-02-02 (Incremental Checkpoint Completeness) {#thm-f-02-02-incremental-checkpoint-completeness}](#thm-f-02-02-incremental-checkpoint-completeness)
    - [Thm-F-02-01 Source Code Verification {#thm-f-02-01-source-code-verification}](#thm-f-02-01-source-code-verification)
    - [Thm-F-02-02 Source Code Verification {#thm-f-02-02-source-code-verification}](#thm-f-02-02-source-code-verification)
  - [6. Examples {#6-examples}](#6-examples)
    - [6.1 Configuration Example: Aligned Checkpoint {#61-configuration-example-aligned-checkpoint}](#61-configuration-example-aligned-checkpoint)
    - [6.2 Configuration Example: Unaligned Checkpoint {#62-configuration-example-unaligned-checkpoint}](#62-configuration-example-unaligned-checkpoint)
    - [6.3 Configuration Example: Incremental Checkpoint {#63-configuration-example-incremental-checkpoint}](#63-configuration-example-incremental-checkpoint)
    - [6.4 Configuration Example: Changelog State Backend {#64-configuration-example-changelog-state-backend}](#64-configuration-example-changelog-state-backend)
    - [6.5 Fault Recovery Case Study {#65-fault-recovery-case-study}](#65-fault-recovery-case-study)
  - [7. Visualizations {#7-visualizations}](#7-visualizations)
    - [7.1 Checkpoint Lifecycle Sequence Diagram {#71-checkpoint-lifecycle-sequence-diagram}](#71-checkpoint-lifecycle-sequence-diagram)
    - [7.2 State Backend Snapshot Flowchart {#72-state-backend-snapshot-flowchart}](#72-state-backend-snapshot-flowchart)
    - [7.3 Checkpoint Type Comparison Decision Tree {#73-checkpoint-type-comparison-decision-tree}](#73-checkpoint-type-comparison-decision-tree)
    - [7.4 Architecture Layer Relationship Diagram {#74-architecture-layer-relationship-diagram}](#74-architecture-layer-relationship-diagram)
  - [8. Tuning Recommendations and Monitoring Metrics {#8-tuning-recommendations-and-monitoring-metrics}](#8-tuning-recommendations-and-monitoring-metrics)
    - [8.1 Checkpoint Tuning Best Practices {#81-checkpoint-tuning-best-practices}](#81-checkpoint-tuning-best-practices)
      - [Basic Configuration Principles {#basic-configuration-principles}](#basic-configuration-principles)
      - [Large-State Job Tuning {#large-state-job-tuning}](#large-state-job-tuning)
      - [Low-Latency Job Tuning {#low-latency-job-tuning}](#low-latency-job-tuning)
    - [8.2 Key Monitoring Metrics {#82-key-monitoring-metrics}](#82-key-monitoring-metrics)
      - [Flink Native Metrics {#flink-native-metrics}](#flink-native-metrics)
      - [JVM and System Metrics {#jvm-and-system-metrics}](#jvm-and-system-metrics)
      - [Custom Monitoring Alerts {#custom-monitoring-alerts}](#custom-monitoring-alerts)
    - [8.3 Common Issue Diagnosis {#83-common-issue-diagnosis}](#83-common-issue-diagnosis)
      - [Issue 1: Frequent Checkpoint Timeouts {#issue-1-frequent-checkpoint-timeouts}](#issue-1-frequent-checkpoint-timeouts)
      - [Issue 2: Long Checkpoint Alignment Time {#issue-2-long-checkpoint-alignment-time}](#issue-2-long-checkpoint-alignment-time)
      - [Issue 3: Slow State Recovery {#issue-3-slow-state-recovery}](#issue-3-slow-state-recovery)
  - [9. References {#9-references}](#9-references)

---

## 1. Definitions

This section establishes rigorous formal definitions for the Flink Checkpoint mechanism, laying the theoretical foundation for subsequent analysis. All definitions are consistent with the semantic hierarchy in [02.02-consistency-hierarchy.md](../../Struct/02-properties/02.02-consistency-hierarchy.md)[^1][^2].

---

### Def-F-02-01 (Checkpoint Core Abstraction)

A **Checkpoint** is a globally consistent state snapshot of a distributed stream processing job at a specific point in time, formally defined as:

$$
CP = \langle ID, TS, \{S_i\}_{i \in Tasks}, Metadata \rangle
$$

Where:

- $ID \in \mathbb{N}^+$: Unique monotonically increasing Checkpoint identifier
- $TS \in \mathbb{R}^+$: Creation timestamp
- $S_i$: State snapshot of task $i$, containing Keyed State and Operator State
- $Metadata$: Metadata (storage location, state size, operator mapping, etc.)

**Intuitive explanation**: A Checkpoint is a "global photograph" taken of a distributed stream processing job running at high speed, freezing the state of all operator instances at the same logical moment so that processing can resume from that consistent state after a failure[^1].

**Source code implementation**:

- Checkpoint coordinator: `org.apache.flink.runtime.checkpoint.CheckpointCoordinator`
- Checkpoint storage: `org.apache.flink.runtime.state.CheckpointStreamFactory`
- Module: `flink-runtime`
- Flink official docs: <https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/checkpointing/>

---

### Def-F-02-02 (Checkpoint Barrier)

A **Barrier** is a special control event injected into the data stream to separate data boundaries between different Checkpoints:

$$
Barrier(n) = \langle Type = CONTROL, checkpointId = n, timestamp = ts \rangle
$$

**Core functions**:

1. Serves as a logical time boundary, separating data before and after $CP_n$
2. Propagates through the data stream, triggering operator state snapshots
3. Achieves distributed coordination without a global clock[^2][^3]

**Source code implementation**:

- Barrier definition: `org.apache.flink.runtime.checkpoint.CheckpointBarrier`
- Barrier handler: `org.apache.flink.streaming.runtime.io.CheckpointBarrierHandler`
- Aligned handler: `org.apache.flink.streaming.runtime.io.CheckpointBarrierAligner`
- Unaligned handler: `org.apache.flink.streaming.runtime.io.CheckpointBarrierUnaligner`
- Module: `flink-runtime` (`flink-streaming-java`)

---

### Def-F-02-03 (Aligned Checkpoint)

An **Aligned Checkpoint** means the operator triggers a state snapshot only after receiving Barriers from **all** input channels:

$$
\text{AlignedSnapshot}(t, n) \iff \forall c \in Inputs(t): Barrier(n) \in Received(c)
$$

**Characteristics**:

- Guarantees that the snapshot state precisely corresponds to the processing results of all data up to the Barrier
- Introduces backpressure waiting: channels that receive the Barrier first must wait for others
- Simple to implement with strong consistency guarantees[^1][^4]

---

### Def-F-02-04 (Unaligned Checkpoint)

An **Unaligned Checkpoint** allows an operator to trigger a snapshot immediately upon receiving a Barrier from **any** input channel, saving unprocessed records from other channels (in-flight data) as part of the state:

$$
\text{UnalignedSnapshot}(t, n) \iff \exists c \in Inputs(t): Barrier(n) \in Received(c)
$$

**Characteristics**:

- Eliminates Barrier alignment waiting, reducing Checkpoint impact on latency
- Requires saving in-flight data, increasing state size
- Suitable for high-backpressure, high-latency scenarios[^4][^5]

---

### Def-F-02-05 (Incremental Checkpoint)

An **Incremental Checkpoint** captures only the portions of state that have changed since the last Checkpoint:

$$
\Delta S_n = S_{t_n} \setminus S_{t_{n-1}}, \quad CP_n^{inc} = \langle Base, \{\Delta S_i\}_{i=1}^{n} \rangle
$$

**RocksDB implementation principles**:

- Based on the immutability of SST files in the LSM-Tree
- Backs up only newly created or modified SST files
- During recovery, reconstructs the full state from the base Checkpoint + incremental chain[^5][^6]

---

### Def-F-02-06 (State Backend)

A **State Backend** is the runtime component responsible for state storage, access, and snapshot persistence:

```java
// Source path: org.apache.flink.runtime.state.StateBackend
interface StateBackend {
    createKeyedStateBackend(env, stateHandles): AbstractKeyedStateBackend<K>
    createOperatorStateBackend(env, stateHandles): OperatorStateBackend
    snapshot(checkpointId): RunnableFuture<SnapshotResult>
    restore(stateHandles): StateBackend
}
```

**Main implementation types**:

| Backend | Storage Medium | Snapshot Method | Applicable Scenarios |
|---------|----------------|-----------------|----------------------|
| HashMapStateBackend | Memory (Heap) | Full sync/async | Small state, low latency |
| EmbeddedRocksDBStateBackend | Local Disk (RocksDB) | Incremental async | Large state, high throughput |

[^5][^6]

**Source code implementation**:

- Abstract base class: `org.apache.flink.runtime.state.AbstractStateBackend`
- HashMap implementation: `org.apache.flink.runtime.state.hashmap.HashMapStateBackend`
- RocksDB implementation: `org.apache.flink.runtime.state.rocksdb.EmbeddedRocksDBStateBackend`
- Module: `flink-runtime` / `flink-state-backends`
- Flink official docs: <https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/state_backends/>

---

### Def-F-02-07 (Checkpoint Coordinator)

The **Checkpoint Coordinator** is the JobManager component responsible for the global Checkpoint lifecycle management:

$$
Coordinator = \langle PendingCP, CompletedCP, TimeoutTimer, AckCallbacks \rangle
$$

**Responsibilities**:

1. Trigger Checkpoints at configured intervals (sending `TriggerCheckpoint` to Sources)
2. Collect acknowledgments (Ack) from all tasks
3. Manage Checkpoint timeouts and failure handling
4. Maintain metadata for completed Checkpoints[^1][^4]

### Def-F-02-08 (Changelog State Backend)

The **Changelog State Backend** is a state backend enhancement introduced in Flink 1.15+, which materializes state changes to distributed storage in real time to achieve second-level recovery[^7]:

$$
\text{ChangelogStateBackend} = \langle \text{BaseBackend}, \text{ChangelogStorage}, \text{MaterializationStrategy} \rangle
$$

**Core mechanisms**:

1. **Real-time Materialization**: State changes are written to the Changelog in real time, rather than only at periodic Checkpoints
2. **Incremental Sync**: Background threads continuously upload state changes, reducing I/O spikes during Checkpoint
3. **Recovery Acceleration**: During recovery, the base Checkpoint and subsequent Changelog are read in parallel, enabling second-level recovery

**Official configuration** (flink-conf.yaml):

```yaml
# Enable Changelog State Backend
state.backend.changelog.enabled: true
state.backend.changelog.storage: filesystem

# Materialization configuration
execution.checkpointing.max-concurrent-checkpoints: 1
state.backend.changelog.periodic-materialization.interval: 10min
state.backend.changelog.materialization.max-concurrent: 1
```

**Comparison with Incremental Checkpoint**:

| Feature | Incremental Checkpoint | Changelog State Backend |
|---------|------------------------|-------------------------|
| Trigger Timing | Periodic (seconds/minutes) | Real-time continuous materialization |
| Recovery Time | Minutes (needs incremental chain merge) | Seconds (parallel read) |
| I/O Overhead | Low (only incremental files) | High (continuous write) |
| Storage Cost | Low (shared SST files) | Medium (needs Changelog storage) |
| Applicable Scenarios | Large state, tolerates minute-level recovery | Latency-sensitive, second-level recovery required |

**Source code implementation**:

- Changelog state backend: `org.apache.flink.runtime.state.changelog.ChangelogStateBackend`
- Materialization service: `org.apache.flink.runtime.state.changelog.PeriodicMaterializationManager`
- Module: `flink-runtime` (Flink 1.15+)

---

## 2. Properties

Building on the definitions in Section 1, this section derives the core properties of the Checkpoint mechanism.

---

### Lemma-F-02-01 (Barrier Alignment Guarantees State Consistency)

**Statement**: If all input channels of operator $t$ have received $Barrier(n)$, then the state $S_t^{(n)}$ of $t$ at the snapshot moment is consistent with the state induced by all input data up to $Barrier(n)$.

**Proof**:

1. By Def-F-02-02, $Barrier(n)$ is a logical time boundary separating data before and after $CP_n$.
2. By Def-F-02-03, operator $t$ only triggers a snapshot after receiving $Barrier(n)$ from all input channels.
3. Therefore, before the snapshot is triggered, $t$ has processed all input data up to $Barrier(n)$, and has not yet processed any data after $Barrier(n)$.
4. Hence $S_t^{(n)}$ precisely corresponds to the state induced by "input up to $Barrier(n)$", with neither lead nor lag.
5. Q.E.D.

> **Inference [Theory→Implementation]**: Barrier alignment is the core mechanism by which Flink achieves internal consistency (see [02.02-consistency-hierarchy.md](../../Struct/02-properties/02.02-consistency-hierarchy.md) Def-S-08-06).

---

### Lemma-F-02-02 (Asynchronous Checkpoint Low-Latency Property)

**Statement**: In asynchronous Checkpoint mode, the latency of operator data processing is not affected by the duration of state snapshot persistence.

**Proof**:

1. By Def-F-02-06, State Backend snapshots are divided into a synchronous phase (obtaining state reference/copy) and an asynchronous phase (serialization and upload).
2. After the synchronous phase completes, the operator immediately resumes data processing, while the asynchronous upload runs in a background thread.
3. Let the synchronous phase duration be $\delta_{sync}$ and the asynchronous phase duration be $\delta_{async}$.
4. The time the operator pauses processing is only $\delta_{sync}$, independent of $\delta_{async}$.
5. Therefore, even if the state is large ($\delta_{async} \gg \delta_{sync}$), the tail latency of data processing is controlled at the $\delta_{sync}$ magnitude.
6. Q.E.D.

---

### Lemma-F-02-03 (Incremental Checkpoint Storage Optimization)

**Statement**: For RocksDB-based incremental Checkpoints, the storage overhead $Storage(n)$ of the $n$-th Checkpoint satisfies:

$$
Storage(n) \ll Storage_{full}(n)
$$

Where $Storage_{full}(n)$ is the storage overhead of a full Checkpoint for the same state.

**Proof**:

1. Due to the LSM-Tree structure of RocksDB, written SST files are immutable.
2. Incremental Checkpoint only backs up SST files newly created or modified since the last Checkpoint ($\Delta SST$).
3. For stable workloads, $|\Delta SST| \ll |Total SST|$.
4. Therefore $Storage(n) = |\Delta SST_n|$, while $Storage_{full}(n) = |Total SST_n|$.
5. Q.E.D.

---

### Prop-F-02-01 (Checkpoint Type Selection Trade-offs)

**Statement**: The four Checkpoint mechanisms—Aligned, Unaligned, Incremental, and Changelog—exhibit the following trade-offs across five dimensions: latency, throughput, storage, recovery time, and consistency guarantee:

| Dimension | Aligned | Unaligned | Incremental | Changelog |
|-----------|---------|-----------|-------------|-----------|
| Latency Impact | Medium (alignment wait) | Low (no alignment wait) | Low (async upload) | Low (real-time materialization) |
| Throughput Impact | Medium (backpressure propagation) | Low (alleviates backpressure) | Low (reduces I/O) | Medium (continuous I/O) |
| Storage Overhead | Standard | High (in-flight data) | Low (only increments) | Medium (Changelog storage) |
| Recovery Speed | Standard | Standard | Slower (needs merge) | Fast (seconds) |
| Consistency Guarantee | Strong | Strong | Strong | Strong |

**Engineering inference**: No single optimal configuration exists; a combined strategy must be chosen based on job characteristics (state size, latency requirements, recovery time SLA, network bandwidth).

| Dimension | Aligned | Unaligned | Incremental |
|-----------|---------|-----------|-------------|
| Latency Impact | Medium (alignment wait) | Low (no alignment wait) | Low (async upload) |
| Throughput Impact | Medium (backpressure propagation) | Low (alleviates backpressure) | Low (reduces I/O) |
| Storage Overhead | Standard | High (in-flight data) | Low (only increments) |
| Recovery Speed | Standard | Standard | Slower (needs merge) |
| Consistency Guarantee | Strong | Strong | Strong |

**Engineering inference**: No single optimal configuration exists; a combined strategy must be chosen based on job characteristics (state size, latency requirements, network bandwidth).

---

## 3. Relations

This section establishes the mapping between the Checkpoint mechanism and distributed systems theory, consistency semantics, and engineering practice.

---

### Relation 1: Flink Checkpoint ↔ Chandy-Lamport Distributed Snapshot

**Argumentation**:

Flink's Checkpoint mechanism is an engineering implementation of the Chandy-Lamport distributed snapshot algorithm[^3] in the stream processing context:

| Chandy-Lamport Concept | Flink Implementation | Semantic Correspondence |
|------------------------|----------------------|-------------------------|
| Marker message | Checkpoint Barrier | Logical time boundary |
| Process local state record | Operator state snapshot | Task instance state |
| Channel state record | in-flight data persistence | Unprocessed data |
| Consistent Cut | Global Checkpoint | Globally consistent state |

By the Chandy-Lamport theorem, this snapshot satisfies:

1. **Consistent Cut**: No message crosses the cut boundary
2. **No Orphans**: All in-flight messages are captured
3. **Reachable**: The recovered state is reachable from the initial state

Therefore:

$$
\text{Flink-Checkpoint} \approx \text{Chandy-Lamport-Snapshot}
$$

> **See also**: [02.02-consistency-hierarchy.md](../../Struct/02-properties/02.02-consistency-hierarchy.md) Relation 2 provides a more detailed correspondence analysis.

---

### Relation 2: Checkpoint Mechanism ⟹ Exactly-Once Semantics

**Argumentation**:

**Prerequisites**:

1. Data source is replayable (e.g., Kafka offsets can be rewound)
2. Operator processing is deterministic
3. Sink supports transactional or idempotent writes

**Derivation**:

By Lemma-F-02-01, the Checkpoint captures a globally consistent state. During fault recovery, the system restores state from $CP_n$ and replays subsequent data. Due to operator determinism, replay produces exactly the same state and output as the first execution. Combined with the two-phase commit of a transactional Sink, the external system observes neither duplicate nor missing data.

**Conclusion**:

$$
\text{Checkpoint} + \text{Replayable Source} + \text{Atomic Sink} \implies \text{Exactly-Once}
$$

> **See also**: [02.02-consistency-hierarchy.md](../../Struct/02-properties/02.02-consistency-hierarchy.md) Thm-S-08-02 provides a complete correctness proof for end-to-end Exactly-Once.

---

### Relation 3: State Backend Type ↔ Application Scenarios

**Argumentation**:

The choice of State Backend directly determines the performance characteristics and applicable scenarios of Checkpoints:

| Scenario Characteristics | Recommended Backend | Reason |
|--------------------------|---------------------|--------|
| State < 100MB, latency-sensitive | HashMapStateBackend | In-memory access, nanosecond-level latency |
| State 100MB–10GB | RocksDB + Full Checkpoint | Disk storage, async snapshots |
| State > 10GB | RocksDB + Incremental Checkpoint | Reduced I/O, lower timeout risk |
| Frequent state updates | RocksDB | LSM-Tree optimizes write amplification |
| Heavy point lookups | HashMapStateBackend | In-memory hash table O(1) query |

---

## 4. Argumentation

This section provides an in-depth analysis of the core engineering implementation details of the Checkpoint mechanism.

---

### 4.1 Checkpoint Architecture: JM/TM Coordination

Flink Checkpoint adopts a **master-worker coordination** architecture, with the CheckpointCoordinator on the JobManager (JM) collaborating with Checkpoint tasks on the TaskManager (TM):

**Phase 1: Trigger Phase**

1. The CheckpointCoordinator triggers periodically according to `checkpointInterval`
2. Generates a monotonically increasing Checkpoint ID
3. Sends `TriggerCheckpoint` RPC to all Source operators

**Phase 2: Propagation Phase**

1. Source operators inject Barriers into the data stream
2. Barriers propagate downstream along the DAG topology
3. Each operator processes Barriers in either aligned or unaligned mode according to configuration

**Phase 3: Snapshot Phase**

1. Operator triggers State Backend snapshot
2. Synchronous phase: obtain state reference/copy
3. Asynchronous phase: serialize and upload to distributed storage (HDFS/S3)

**Phase 4: Acknowledgment Phase**

1. TM sends `AcknowledgeCheckpoint` to JM
2. Coordinator collects all Acks
3. If all are received before timeout, marks as COMPLETED; otherwise marks as FAILED

```
JM (CheckpointCoordinator)                    TM (Task with State)
         |                                             |
         |------ TriggerCheckpoint(ID) ---------------->|
         |                                             |
         |<----- AcknowledgeCheckpoint(ID) ------------|
         |          (contains StateHandle reference)   |
         |                                             |
```

---

### 4.2 Aligned vs Unaligned: In-Depth Comparison

#### Aligned Checkpoint Workflow

1. The operator maintains the Barrier arrival status for each input channel
2. Channels that have received Barrier $n$ stop processing and buffer data
3. Wait for Barrier $n$ to arrive on all input channels
4. Trigger state snapshot and forward Barrier $n$ downstream
5. Resume data processing, consuming buffered data

**Advantages**:

- Simple implementation; state contains only internal operator state
- Directly achieves Exactly-Once semantics when combined with two-phase commit

**Disadvantages**:

- Alignment waiting introduces additional latency
- Under backpressure, Barrier propagation is blocked, increasing Checkpoint timeout risk

#### Unaligned Checkpoint Workflow

1. The operator triggers a snapshot immediately upon receiving Barrier $n$ from any input channel
2. Unprocessed records from other channels (in-flight) are saved as part of the state
3. Snapshot contains: internal operator state + in-flight data
4. Immediately forward Barrier $n$ downstream

**Advantages**:

- Eliminates alignment waiting, reducing Checkpoint impact on latency
- Can still complete Checkpoints quickly under backpressure

**Disadvantages**:

- Increased state size (includes in-flight data)
- During recovery, in-flight data must be replayed, increasing recovery time
- Higher implementation complexity

---

### 4.3 Incremental Checkpoint Engineering Implementation

#### 4.3.1 RocksDB Incremental Checkpoint Principles

Based on the architectural characteristics of RocksDB's LSM-Tree:

1. **SST File Immutability**: Once written, SST files are never modified
2. **Manifest File**: Records metadata for all active SST files
3. **Incremental Detection**: By comparing the SST file sets between two consecutive Checkpoints

**Implementation flow**:

```
Checkpoint N:   Back up all SST files (Base)
                ↓
Checkpoint N+1: Identify newly added SST files (Δ₁)
                Back up new files + update Manifest
                ↓
Checkpoint N+2: Identify newly added SST files (Δ₂)
                Back up new files + update Manifest
```

**Recovery flow**:

$$
S_{recovered} = Base \cup \Delta_1 \cup \Delta_2 \cup \cdots \cup \Delta_n
$$

#### Configuration Parameters

```java
// Enable incremental Checkpoint
EmbeddedRocksDBStateBackend rocksDbBackend = new EmbeddedRocksDBStateBackend(true);
env.setStateBackend(rocksDbBackend);

// Enable Unaligned Checkpoint
env.getCheckpointConfig().enableUnalignedCheckpoints();

// Configure incremental Checkpoint interval
env.getCheckpointConfig().setMinPauseBetweenCheckpoints(500);

// RocksDB-specific configuration
DefaultConfigurableStateBackend stateBackend = new EmbeddedRocksDBStateBackend(true);
```

---

### 4.4 State Backend Snapshot Process Details

#### HashMapStateBackend Snapshot Process

```
[Sync Phase]
    ↓
Copy HashMap reference / shallow copy
    ↓
[Async Phase - Background Thread]
    ↓
Serialize Keyed State (using TypeSerializer)
    ↓
Serialize Operator State
    ↓
Write to distributed file system (HDFS/S3)
    ↓
Generate StateHandle
    ↓
Send Ack to JM
```

**Sync phase duration**: Proportional to the number of state entries, $O(|S|)$

#### RocksDBStateBackend Snapshot Process

```
[Sync Phase]
    ↓
Obtain RocksDB SST file list
Mark current state version (create Checkpoint marker)
    ↓
[Async Phase - Background Thread]
    ↓
Upload new/modified SST files (incremental mode)
Or upload all SST files (full mode)
    ↓
Upload Manifest file
    ↓
Generate StateHandle
    ↓
Send Ack to JM
```

**Sync phase duration**: Only involves file list operations, $O(1)$ (independent of state size)

---

## 5. Proof / Engineering Argument

### Thm-F-02-01 (System State Equivalence After Checkpoint Recovery)

**Statement**: Suppose the system fails at time $\tau_f$ during execution, and the last successfully completed Checkpoint is $CP_n$. After recovering from $CP_n$ and completing Replay, the system is observationally equivalent to a continuation of some consistent cut $C$, where $C$ corresponds to the global state captured by $CP_n$.

**Proof**:

**Step 1: Establish the consistent cut correspondence**

By Lemma-F-02-01 and Relation 1, the state set $Snapshot(n) = \{S_t^{(n)} \mid t \in Tasks\}$ captured by $CP_n$ constitutes a consistent cut $C_n$ (see Chandy-Lamport theorem[^3]).

**Step 2: Analyze the pre-failure execution history**

Let the pre-failure execution history be the event sequence $E = e_1, e_2, \ldots, e_k$. Let the history prefix corresponding to $C_n$ be $E_{prefix} = e_1, \ldots, e_p$, i.e., $CP_n$ captures the global state after executing $E_{prefix}$.

By the Checkpoint protocol and Lemma-F-02-01, $E_{prefix}$ exactly contains all events located before $Barrier(n)$ at their respective operators. For any event $e_j \in E_{prefix}$ and $e_l \notin E_{prefix}$, there is no $e_l \rightarrow e_j$ (otherwise $e_l$ would also be before $Barrier(n)$). Therefore $E_{prefix}$ is downward closed under the happens-before relation, i.e., $C_n$ is a consistent cut.

**Step 3: Semantics of recovery and Replay**

The recovery process performs:

1. $Restore(CP_n)$: Resets each operator $t$'s state to $S_t^{(n)}$.
2. $Replay$: The data source re-consumes data from the offset recorded in $CP_n$, i.e., replays the input records corresponding to $E_{suffix} = e_{p+1}, \ldots, e_k$.

**Step 4: Determinism guarantees equivalence**

Since Flink operators are deterministic (the same input and state produce the same output and state updates), replaying $E_{suffix}$ produces an event sequence that is completely consistent in state and output effects with the first execution of $E_{suffix}$.

**Step 5: Observational equivalence**

For an external observer, the recovered system starts from global state $G_n$ (i.e., consistent cut $C_n$) and continues executing the same event suffix as before the failure. Therefore, the recovered system trace $tr'$ and the original system trace $tr$ satisfy:

$$
tr = E_{prefix} \circ E_{suffix}, \quad tr' = E_{prefix} \circ E_{suffix}
$$

That is, $tr$ and $tr'$ completely coincide after $C_n$. The observer cannot distinguish between the original execution and the recovered execution.

∎

> **Note**: For a more detailed formal proof, see [04.01-flink-checkpoint-correctness.md](../../Struct/04-proofs/04.01-flink-checkpoint-correctness.md).

---

### Thm-F-02-02 (Incremental Checkpoint Completeness)

**Statement**: Let $Base$ be the state set captured by a full Checkpoint, and $\Delta_1, \Delta_2, \ldots, \Delta_n$ be the incremental state sets captured by the subsequent $n$ incremental Checkpoints. Then the recovered state $S_{restore}$ after the $n$-th incremental Checkpoint satisfies:

$$
S_{restore} = Base \cup \bigcup_{i=1}^{n} \Delta_i = S_n
$$

Where $S_n$ is the complete state at the moment of the $n$-th Checkpoint.

**Proof**:

**Step 1: RocksDB SST Immutability**

RocksDB is based on the LSM-Tree architecture; once data is written to an SST (Sorted String Table) file, it cannot be modified. Subsequent write operations only create new SST files; old SST files remain unchanged.

**Step 2: Semantics of incremental sets**

Let $F_t$ be the RocksDB SST file set at time $t$. Due to immutability:

$$
F_{t_2} = F_{t_1} \cup F_{new}, \quad t_2 > t_1
$$

Where $F_{new}$ is the set of SST files newly created during $(t_1, t_2]$.

**Step 3: Construction of incremental Checkpoints**

- $Base = F_{t_0}$ (all SST files backed up by the base full Checkpoint)
- $\Delta_i = F_{t_i} \setminus F_{t_{i-1}}$ (new SST files backed up by the $i$-th incremental Checkpoint)

**Step 4: Completeness derivation**

$$
\begin{aligned}
S_{restore} &= Base \cup \bigcup_{i=1}^{n} \Delta_i \\
&= F_{t_0} \cup \bigcup_{i=1}^{n} (F_{t_i} \setminus F_{t_{i-1}}) \\
&= F_{t_0} \cup (F_{t_1} \setminus F_{t_0}) \cup (F_{t_2} \setminus F_{t_1}) \cup \ldots \cup (F_{t_n} \setminus F_{t_{n-1}}) \\
&= F_{t_n} \\
&= S_n
\end{aligned}
$$

**Step 5: Consistency guarantee**

RocksDB's manifest file records metadata for all active SST files. Incremental Checkpoint simultaneously backs up incremental manifest changes, ensuring that reference relationships and hierarchical structure among SST files are correctly reconstructed during recovery.

∎

---

### Thm-F-02-01 Source Code Verification

**Theorem**: System State Equivalence After Checkpoint Recovery

**Source code verification**:

```java
// CheckpointCoordinator.java (lines 850-920)
public boolean restoreSavepoint(
        SavepointRestoreSettings savepointRestoreSettings,
        Map<JobVertexID, ExecutionJobVertex> tasks,
        ClassLoader userClassLoader) throws Exception {

    // 1. Load Checkpoint/Savepoint metadata (corresponds to Metadata component)
    CompletedCheckpoint savepoint =
        Checkpoints.loadAndValidateCheckpoint(
            job,
            savepointRestoreSettings.getRestorePath(),
            userClassLoader,
            savepointRestoreSettings.allowNonRestoredState()
        );

    // 2. Validate state integrity (corresponds to theorem conditions)
    if (!savepoint.getOperatorStates().isEmpty()) {
        // Validate the validity of each operator state handle
        for (OperatorState operatorState : savepoint.getOperatorStates()) {
            if (!validateStateHandle(operatorState)) {
                throw new IllegalStateException("Checkpoint state corrupted for operator: "
                    + operatorState.getOperatorID());
            }
        }
    }

    // 3. Restore each operator state (corresponds to S_i recovery)
    for (Map.Entry<JobVertexID, ExecutionJobVertex> task : tasks.entrySet()) {
        ExecutionJobVertex vertex = task.getValue();
        OperatorState operatorState = savepoint.getOperatorState(vertex.getOperatorIDs());
        if (operatorState != null) {
            restoreOperatorState(vertex, operatorState, userClassLoader);
        }
    }

    // 4. Initialize Checkpoint statistics
    checkpointStatsTracker.reportRestoredCheckpoint(savepoint);

    LOG.info("Successfully restore savepoint {}.", savepoint.getCheckpointID());
    return true;
}

// Internal method for restoring operator state
private void restoreOperatorState(
        ExecutionJobVertex vertex,
        OperatorState operatorState,
        ClassLoader classLoader) throws Exception {

    // Get all parallel subtasks of this operator
    int parallelism = vertex.getParallelism();
    for (int subtaskIndex = 0; subtaskIndex < parallelism; subtaskIndex++) {
        OperatorSubtaskState subtaskState =
            operatorState.getState(subtaskIndex);

        // Restore Keyed State (corresponds to Keyed portion of S_i)
        if (subtaskState.getManagedKeyedState() != null) {
            vertex.getTaskVertices()[subtaskIndex].setInitialState(
                subtaskState,
                allowNonRestoredState
            );
        }

        // Restore Operator State (corresponds to Operator portion of S_i)
        if (subtaskState.getManagedOperatorState() != null) {
            vertex.getTaskVertices()[subtaskIndex].setInitialState(
                subtaskState,
                allowNonRestoredState
            );
        }
    }
}
```

**Verification conclusions**:

- ✅ Metadata loading corresponds to $Metadata$ component: `Checkpoints.loadAndValidateCheckpoint()` loads the complete Checkpoint metadata
- ✅ Operator state recovery corresponds to $\{S_i\}$ set: `restoreOperatorState()` iterates over all operator parallel subtasks, restoring their respective Keyed State and Operator State
- ✅ Integrity validation corresponds to state equivalence condition: `validateStateHandle()` ensures each state handle is valid, guaranteeing that the recovered state is consistent with the Checkpoint moment
- ✅ Recovery process follows Chandy-Lamport global snapshot semantics: all operators recover from the same Checkpoint ID, ensuring global consistency

---

### Thm-F-02-02 Source Code Verification

**Theorem**: Incremental Checkpoint Completeness

**Source code verification**:

```java
// RocksDBIncrementalCheckpoint series implementation
// EmbeddedRocksDBStateBackend.java (incremental Checkpoint related)

public class EmbeddedRocksDBStateBackend extends AbstractManagedMemoryStateBackend {

    // Incremental Checkpoint flag
    private final boolean incrementalCheckpointMode;

    @Override
    public <K> CheckpointableKeyedStateBackend<K> createCheckpointableStateBackend(
            Environment env,
            JobID jobID,
            String operatorIdentifier,
            TypeSerializer<K> keySerializer,
            int numberOfKeyGroups,
            KeyGroupRange keyGroupRange,
            TaskKvStateRegistry kvStateRegistry,
            TtlTimeProvider ttlTimeProvider,
            MetricGroup metricGroup,
            @NonNull Collection<KeyedStateHandle> stateHandles,
            CloseableRegistry cancelStreamRegistry) throws Exception {

        // Create RocksDB state backend supporting incremental Checkpoint
        RocksDBStateBackend backend = new RocksDBStateBackend(
            env.getTaskManagerInfo().getConfiguration(),
            env.getUserCodeClassLoader(),
            incrementalCheckpointMode  // Enable incremental mode
        );

        // Restore base state (Base)
        if (!stateHandles.isEmpty()) {
            backend.restoreBaseState(stateHandles);
        }

        return backend;
    }
}

// RocksDBStateUploader.java (incremental upload implementation)
public class RocksDBStateUploader extends StateUploader {

    /**
     * Upload incremental SST files
     * Only upload files added or modified since the last Checkpoint
     */
    public List<StreamStateHandle> uploadIncrementalState(
            Set<SSTFileInfo> newSstFiles,     // New SST files (Δ)
            Set<SSTFileInfo> reusedSstFiles,  // Reused SST files (Base)
            CheckpointStreamFactory streamFactory,
            CheckpointedStateScope stateScope) throws IOException {

        List<StreamStateHandle> handles = new ArrayList<>();

        // 1. Reuse existing SST file references (corresponds to Base)
        for (SSTFileInfo reused : reusedSstFiles) {
            handles.add(new FileStateHandle(reused.getPath(), reused.getSize()));
        }

        // 2. Upload new SST files (corresponds to Δ)
        for (SSTFileInfo newFile : newSstFiles) {
            StreamStateHandle handle = uploadSSTFile(newFile, streamFactory, stateScope);
            handles.add(handle);
        }

        // 3. Upload Manifest file (reference relationships)
        StreamStateHandle manifestHandle = uploadManifest(streamFactory, stateScope);
        handles.add(manifestHandle);

        return handles;
    }
}
```

**Verification conclusions**:

- ✅ SST file immutability guarantee: once created, `SSTFileInfo` content is immutable; incrementality is achieved through reference reuse
- ✅ Base state recovery (Base): `restoreBaseState()` recovers from the base state of the last Checkpoint
- ✅ Incremental upload (Δ): `uploadIncrementalState()` only uploads new/modified SST files
- ✅ Manifest maintains reference relationships: the Manifest file records all active SST files, ensuring correct hierarchical structure during recovery
- ✅ Completeness verification: $S_{restore} = Base \cup \bigcup_{i=1}^{n} \Delta_i$ is implemented through the union of SST file sets

---

## 6. Examples

### 6.1 Configuration Example: Aligned Checkpoint

```java

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.CheckpointingMode;

StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// Enable Checkpoint with 10-second interval
env.enableCheckpointing(10000);

// Configure as Aligned Checkpoint (default)
env.getCheckpointConfig().setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE);

// Timeout of 60 seconds
env.getCheckpointConfig().setCheckpointTimeout(60000);

// Maximum concurrent Checkpoints
env.getCheckpointConfig().setMaxConcurrentCheckpoints(1);

// Minimum interval 500ms
env.getCheckpointConfig().setMinPauseBetweenCheckpoints(500);

// Use RocksDB State Backend
EmbeddedRocksDBStateBackend rocksDbBackend = new EmbeddedRocksDBStateBackend();
env.setStateBackend(rocksDbBackend);

// Checkpoint storage path
env.getCheckpointConfig().setCheckpointStorage("hdfs:///flink/checkpoints");
```

---

### 6.2 Configuration Example: Unaligned Checkpoint

```java

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

env.enableCheckpointing(10000);

// Enable Unaligned Checkpoint
env.getCheckpointConfig().enableUnalignedCheckpoints();

// Configure alignment timeout (automatically switches to Unaligned after this time)
env.getCheckpointConfig().setAlignmentTimeout(Duration.ofSeconds(30));

// Configure in-flight data size threshold
env.getCheckpointConfig().setMaxUnalignedCheckpoints(2);

// Use RocksDB State Backend (recommended with Unaligned Checkpoint)
env.setStateBackend(new EmbeddedRocksDBStateBackend());

env.getCheckpointConfig().setCheckpointStorage("hdfs:///flink/checkpoints");
```

---

### 6.3 Configuration Example: Incremental Checkpoint

```java

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

env.enableCheckpointing(60000); // Slightly longer interval recommended for incremental Checkpoint

// Use RocksDB State Backend, enable incremental Checkpoint
// The second parameter true enables incrementality
EmbeddedRocksDBStateBackend rocksDbBackend = new EmbeddedRocksDBStateBackend(true);
env.setStateBackend(rocksDbBackend);

// Checkpoint storage path
env.getCheckpointConfig().setCheckpointStorage("hdfs:///flink/checkpoints");
```

---

### 6.4 Configuration Example: Changelog State Backend

```java

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

env.enableCheckpointing(60000);

// Enable Changelog State Backend
env.setStateBackend(new EmbeddedRocksDBStateBackend());

// Configure in flink-conf.yaml:
// state.backend.changelog.enabled: true
// state.backend.changelog.storage: filesystem

// Or configure via code
Configuration config = new Configuration();
config.setBoolean("state.backend.changelog.enabled", true);
config.setString("state.backend.changelog.storage", "filesystem");
env.configure(config);

env.getCheckpointConfig().setCheckpointStorage("hdfs:///flink/checkpoints");
```

**Key configuration notes**:

| Configuration Item | Default | Description |
|--------------------|---------|-------------|
| `state.backend.changelog.enabled` | false | Whether to enable Changelog State Backend |
| `state.backend.changelog.storage` | filesystem | Changelog storage type (filesystem/memory) |
| `state.backend.changelog.periodic-materialization.interval` | 10min | Materialization interval |
| `state.backend.changelog.materialization.max-concurrent` | 1 | Maximum concurrent materialization tasks |

---

### 6.5 Fault Recovery Case Study

```java
// Use RocksDB State Backend, enable incremental Checkpoint
// The second parameter true enables incrementality
EmbeddedRocksDBStateBackend rocksDbBackend = new EmbeddedRocksDBStateBackend(true);
env.setStateBackend(rocksDbBackend);

// Configure incremental Checkpoint history retention count
// Retain the most recent 10 incremental Checkpoints
Configuration rocksDbConfig = new Configuration();
rocksDbConfig.setString("state.backend.incremental", "true");
rocksDbConfig.setString("state.backend.rocksdb.predefined-options", "FLASH_SSD_OPTIMIZED");

env.configure(rocksDbConfig);

env.getCheckpointConfig().setCheckpointStorage("hdfs:///flink/checkpoints");
```

---

**Scenario**: E-commerce real-time transaction analysis job processing Kafka transaction streams, with state size around 50GB, using RocksDB + Incremental Checkpoint.

**Recovery time comparison** (based on 50GB state):

| Checkpoint Type | Recovery Time | Applicable Scenario |
|-----------------|---------------|---------------------|
| Full Checkpoint | ~8 minutes | Small state, fast recovery needed |
| Incremental Checkpoint | ~12 minutes | Large state, limited network bandwidth |
| Changelog State Backend | ~30 seconds | Latency-sensitive, second-level SLA required |

**Fault occurrence**: TaskManager node goes down due to disk failure.

**Recovery process**:

1. **Fault detection**: JobManager does not receive heartbeats within `heartbeat.interval` (default 10s), marking the TM as failed.

2. **Job restart decision**: According to `restart-strategy` configuration, triggers fixed-delay restart.

3. **State recovery**:

```

- Query latest successful Checkpoint: CP_150
- Base Checkpoint: CP_140 (full)
- Incremental chain: CP_141, CP_142, ..., CP_150
- Merge recovery: S = CP_140 ∪ CP_141 ∪ ... ∪ CP_150

   ```

1. **Task rescheduling**: Reschedule failed tasks to healthy nodes.

2. **Source replay**: Kafka Consumer starts consuming from the offset recorded in CP_150.

3. **State validation**: After Checkpoint recovery, verify that state size and key count match expectations.

**Recovery time**: About 3 minutes (main time spent pulling incremental files from HDFS)

---

## 7. Visualizations

### 7.1 Checkpoint Lifecycle Sequence Diagram

```mermaid
sequenceDiagram
    participant JM as JobManager<br/>(CheckpointCoordinator)
    participant SRC as Source Task
    participant OP1 as Intermediate Task
    participant SNK as Sink Task
    participant DFS as Distributed Storage

    Note over JM: Trigger Checkpoint N
    JM->>SRC: TriggerCheckpoint(N)
    activate SRC

    SRC->>SRC: Inject Barrier(N) into output
    SRC->>OP1: Barrier(N) + Data
    SRC->>JM: AckCheckpoint(N, StateHandle)
    deactivate SRC

    activate OP1
    OP1->>OP1: Align Barrier(N)
    OP1->>OP1: Trigger state snapshot
    OP1->>DFS: Async upload state
    OP1->>SNK: Barrier(N) + Data

    DFS-->>OP1: Upload Complete
    OP1->>JM: AckCheckpoint(N, StateHandle)
    deactivate OP1

    activate SNK
    SNK->>SNK: Align Barrier(N)
    SNK->>SNK: Pre-commit transaction
    SNK->>DFS: Async upload state

    DFS-->>SNK: Upload Complete
    SNK->>JM: AckCheckpoint(N, StateHandle)
    deactivate SNK

    JM->>JM: All Acks received
    JM->>JM: Mark CP(N) as COMPLETED
    JM->>SNK: NotifyCheckpointComplete(N)

    activate SNK
    SNK->>SNK: Commit transaction
    deactivate SNK
```

**Diagram notes**:

- Shows the complete lifecycle from JM triggering Checkpoint to Sink committing transaction
- Each Task triggers a snapshot after receiving all input Barriers
- Sink uses two-phase commit (pre-commit + post-ack commit) to guarantee end-to-end Exactly-Once

---

### 7.2 State Backend Snapshot Flowchart

```mermaid
flowchart TD
    subgraph "Sync Phase"
        S1[Start Snapshot] --> S2{State Backend Type}
        S2 -->|HashMap| H1[Copy HashMap reference]
        S2 -->|RocksDB| R1[Obtain SST file list]
        H1 --> S3[Create state copy/marker]
        R1 --> S3
    end

    subgraph "Async Phase"
        S3 --> A1[Serialize state data]
        A1 --> A2{Checkpoint Mode}
        A2 -->|Full| F1[Upload all state files]
        A2 -->|Incremental| I1[Identify changed files]
        I1 --> I2[Upload only new SST files]
        F1 --> A3[Generate StateHandle]
        I2 --> A3
    end

    subgraph "Completion Phase"
        A3 --> C1[Upload metadata to JM]
        C1 --> C2[Send Ack]
        C2 --> C3[Clean up expired Checkpoints]
    end

    style S1 fill:#fff9c4,stroke:#f57f17
    style S3 fill:#bbdefb,stroke:#1565c0
    style A3 fill:#c8e6c9,stroke:#2e7d32
    style C3 fill:#e1bee7,stroke:#6a1b9a
```

**Diagram notes**:

- Synchronous phase blocks data processing and should be as fast as possible
- Asynchronous phase runs in the background without affecting data processing latency
- Incremental mode significantly reduces data transfer volume in the asynchronous phase

---

### 7.3 Checkpoint Type Comparison Decision Tree

```mermaid
flowchart TD
    START[Select Checkpoint Strategy] --> Q1{Job Latency Requirement?}

    Q1 -->|Second-level latency| A1[Aligned Checkpoint]
    Q1 -->|Millisecond-level latency| Q2{Backpressure present?}

    Q2 -->|Yes| A2[Unaligned Checkpoint]
    Q2 -->|No| A3[Aligned + Tuned Timeout]

    A1 --> Q3{State Size?}
    A2 --> Q3
    A3 --> Q3

    Q3 -->|&lt; 100MB| B1[HashMapStateBackend<br/>Full Checkpoint]
    Q3 -->|100MB - 10GB| B2[RocksDB<br/>Full Checkpoint]
    Q3 -->|&gt; 10GB| B3[RocksDB<br/>Incremental Checkpoint]

    B1 --> C1[Configuration Complete]
    B2 --> C1
    B3 --> C1

    style START fill:#fff9c4,stroke:#f57f17
    style A2 fill:#c8e6c9,stroke:#2e7d32
    style B3 fill:#bbdefb,stroke:#1565c0
    style C1 fill:#e1bee7,stroke:#6a1b9a
```

**Diagram notes**:

- Decision tree starts from latency requirements and progressively determines Checkpoint type
- State size is the key factor in choosing incremental Checkpoint
- RocksDB with incremental Checkpoint is the standard solution for large-state scenarios

---

### 7.4 Architecture Layer Relationship Diagram

```mermaid
graph TB
    subgraph "Control Layer"
        C1[CheckpointCoordinator<br/>Trigger/Coordination/Timeout Management]
        C2[Checkpoint Configuration Policy<br/>Interval/Mode/Storage]
    end

    subgraph "Execution Layer"
        E1[Barrier Propagation Engine<br/>Aligned/Unaligned Mode]
        E2[State Backend Interface<br/>Heap/RocksDB]
        E3[Async Snapshot Thread Pool<br/>Upload/Serialization]
    end

    subgraph "Data Layer"
        D1[Distributed Storage<br/>HDFS/S3/OSS]
        D2[State File Format<br/>SST/Manifest/Metadata]
        D3[Recovery State Reconstruction<br/>Full/Incremental Merge]
    end

    subgraph "Semantics Layer"
        S1[Exactly-Once Guarantee<br/>Barrier Alignment]
        S2[End-to-End Consistency<br/>Source + Checkpoint + Sink]
    end

    C1 --> E1
    C2 --> E2
    E1 --> E3
    E2 --> E3
    E3 --> D1
    E2 --> D2
    D1 --> D3
    D2 --> D3
    D3 --> S1
    S1 --> S2

    style C1 fill:#fff9c4,stroke:#f57f17
    style E2 fill:#bbdefb,stroke:#1565c0
    style D1 fill:#c8e6c9,stroke:#2e7d32
    style S2 fill:#e1bee7,stroke:#6a1b9a
```

**Diagram notes**:

- Control layer determines Checkpoint policies and constrains execution layer behavior
- Execution layer implements the snapshot mechanism through Barrier propagation and State Backend
- Data layer is responsible for persistent storage and recovery reconstruction of state
- Semantics layer achieves Exactly-Once guarantees through the above mechanisms

---

## 8. Tuning Recommendations and Monitoring Metrics

### 8.1 Checkpoint Tuning Best Practices

#### Basic Configuration Principles

| Parameter | Recommended Value | Description |
|-----------|-------------------|-------------|
| `checkpointInterval` | 10s - 60s | Adjust according to business tolerance for recovery time |
| `checkpointTimeout` | 3-5x average completion time | Avoid premature timeouts |
| `minPauseBetweenCheckpoints` | 500ms - 5s | Ensure data processing time slices |
| `maxConcurrentCheckpoints` | 1 | Single concurrency is usually sufficient |

#### Large-State Job Tuning

**Problem**: When state > 10GB, Checkpoints are prone to time out.

**Solutions**:

1. **Enable incremental Checkpoint** (required)

```java
   new EmbeddedRocksDBStateBackend(true)  // true enables incremental
```

1. **Tune RocksDB parameters**

```java
   DefaultConfigurableStateBackend backend = new EmbeddedRocksDBStateBackend(true);
   Configuration config = new Configuration();
   config.setString("state.backend.rocksdb.predefined-options", "FLASH_SSD_OPTIMIZED");
   config.setString("state.backend.rocksdb.thread.num", "4");
```

1. **Increase Checkpoint interval**

```java
   env.enableCheckpointing(60000);  // 1 minute, reduce frequency
```

1. **Use local recovery**

```java
   env.getCheckpointConfig().setPreferCheckpointForRecovery(true);
```

#### Low-Latency Job Tuning

**Problem**: Checkpoint alignment waiting increases latency.

**Solutions**:

1. **Enable Unaligned Checkpoint**

```java
   env.getCheckpointConfig().enableUnalignedCheckpoints();
   env.getCheckpointConfig().setAlignmentTimeout(Duration.ofSeconds(1));
```

1. **Reduce state size**
   - Use shorter state TTL
   - Optimize state data structures

2. **Use asynchronous Checkpoint mode**

```java

import org.apache.flink.streaming.api.CheckpointingMode;

   env.getCheckpointConfig().setCheckpointingMode(CheckpointingMode.AT_LEAST_ONCE);
```

   (Only when At-Least-Once is acceptable)

---

### 8.2 Key Monitoring Metrics

#### Flink Native Metrics

| Metric Name | Type | Healthy Threshold | Description |
|-------------|------|-------------------|-------------|
| `checkpointDuration` | Gauge | < 50% of timeout | Checkpoint completion time |
| `checkpointedBytes` | Gauge | Evaluate based on bandwidth | Checkpoint data volume |
| `numberOfFailedCheckpoints` | Counter | 0 | Number of failed Checkpoints |
| `numberOfPendingCheckpoints` | Gauge | ≤ 1 | Number of in-progress Checkpoints |
| `lastCheckpointFullSize` | Gauge | Trend monitoring | Full Checkpoint size |
| `lastCheckpointIncrementSize` | Gauge | Trend monitoring | Incremental Checkpoint size |

#### JVM and System Metrics

| Metric Name | Type | Healthy Threshold | Description |
|-------------|------|-------------------|-------------|
| `JVM.Heap.Used` | Gauge | < 70% heap | Heap memory usage (HashMapStateBackend) |
| `JVM.NonHeap.Used` | Gauge | Trend monitoring | Non-heap memory usage |
| `RocksDB.BlockCacheUsage` | Gauge | < 80% BlockCache | RocksDB cache usage |
| `RocksDB.EstimatedTableReadersMem` | Gauge | Trend monitoring | SST file index memory |

#### Custom Monitoring Alerts

```yaml
# Prometheus Alert example
- alert: FlinkCheckpointTimeout
  expr: |
    flink_jobmanager_checkpoint_duration_time >
    flink_jobmanager_checkpoint_timeout_time * 0.8
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "Flink Checkpoint approaching timeout"

- alert: FlinkCheckpointFailure
  expr: |
    increase(flink_jobmanager_number_of_failed_checkpoints[5m]) > 0
  for: 1m
  labels:
    severity: critical
  annotations:
    summary: "Flink Checkpoint failure"
```

---

### 8.3 Common Issue Diagnosis

#### Issue 1: Frequent Checkpoint Timeouts

**Symptoms**: `numberOfFailedCheckpoints` continuously increases, job logs show `Checkpoint expired`.

**Diagnosis steps**:

1. Check `checkpointedBytes` to confirm state size
2. Check network bandwidth (HDFS/S3 upload speed)
3. Check RocksDB background compaction activity

**Solutions**:

- State > 10GB: enable incremental Checkpoint
- Network bottleneck: increase `checkpointTimeout` or optimize network
- Compaction interference: adjust RocksDB `maxBackgroundJobs`

#### Issue 2: Long Checkpoint Alignment Time

**Symptoms**: `checkpointAlignmentTime` continuously increases, job exhibits backpressure.

**Diagnosis steps**:

1. Check Flink Web UI Backpressure tab
2. Analyze data skew (some subtasks process slowly)

**Solutions**:

- Enable Unaligned Checkpoint
- Resolve data skew (repartition keys)
- Increase operator parallelism

#### Issue 3: Slow State Recovery

**Symptoms**: Fault recovery takes a long time, affecting business availability.

**Diagnosis steps**:

1. Check `latestRestoredCheckpointStateSize`
2. Check network bandwidth from HDFS/S3 to TM

**Solutions**:

- Use incremental Checkpoint to reduce recovery data volume
- Enable local recovery (`setPreferCheckpointForRecovery`)
- Consider using `savepoint` as recovery point (full, faster)

---

## 9. References

[^1]: Apache Flink Documentation, "Checkpointing", 2025. <https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/checkpointing/>

[^2]: Apache Flink Documentation, "Exactly-Once Semantics", 2025. <https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/fault_tolerance/>

[^3]: K. M. Chandy and L. Lamport, "Distributed Snapshots: Determining Global States of Distributed Systems," *ACM Transactions on Computer Systems*, 3(1), 1985.

[^4]: Apache Flink Documentation, "Unaligned Checkpoints", 2025. <https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/checkpointing_under_backpressure/>

[^5]: Apache Flink Documentation, "RocksDB State Backend: Incremental Checkpointing", 2025. <https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/large_state_tuning/>

[^6]: S. Das et al., "Apache Flink: Stream and Batch Processing in a Single Engine," *IEEE Data Engineering Bulletin*, 38(4), 2015.

[^7]: Apache Flink Documentation, "State Backends", 2025. <https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/state_backends/>

---
