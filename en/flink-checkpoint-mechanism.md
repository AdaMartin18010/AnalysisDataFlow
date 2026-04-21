# Flink Checkpoint Mechanism Deep Dive

> **Stage**: Flink/02-core | **Prerequisites**: [Consistency Hierarchy](../../Struct/02-properties/02.02-consistency-hierarchy.md) | **Formalization Level**: L4
> **Translation Date**: 2026-04-21

## Abstract

Flink's checkpoint mechanism provides distributed snapshot-based fault tolerance via Chandy-Lamport algorithm with barrier alignment.

---

## 1. Definitions

### Def-F-02-01 (Checkpoint)

A **checkpoint** is a consistent snapshot of all operator states at a global logical timestamp.

### Def-F-02-02 (Checkpoint Barrier)

A **barrier** is a special control event injected into data streams to mark the logical time for snapshotting.

### Def-F-02-03 (Aligned Checkpoint)

Blocks input channels until all barriers for checkpoint $n$ are received:

$$\forall c: \text{barrier}_n^c \text{ received} \Rightarrow \text{snapshot state}$$

### Def-F-02-04 (Unaligned Checkpoint)

Snapshots in-flight data immediately without blocking:

$$\text{barrier}_n \text{ injected} \Rightarrow \text{snapshot state + in-flight data}$$

---

## 2. Properties

### Lemma-F-02-01 (Barrier Alignment Guarantees Consistency)

Aligned barriers ensure all operators snapshot at the same logical timestamp.

### Lemma-F-02-02 (Asynchronous Checkpoint Low Latency)

State materialization happens asynchronously; only state pointer is included in synchronous phase.

---

## 3. Configuration

```java
// Aligned checkpoint
env.enableCheckpointing(60000);
env.getCheckpointConfig().setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE);

// Unaligned checkpoint (Flink 1.13+)
env.getCheckpointConfig().enableUnalignedCheckpoints();
env.getCheckpointConfig().setAlignmentTimeout(Duration.ofSeconds(30));

// Incremental checkpoint with RocksDB
env.setStateBackend(new EmbeddedRocksDBStateBackend(true));
```

---

## 4. References
