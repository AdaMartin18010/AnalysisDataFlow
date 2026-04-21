# State Management Concepts

> **Stage**: Knowledge/01-concept-atlas | **Prerequisites**: [Time Semantics](time-semantics.md) | **Formalization Level**: L3-L4
> **Translation Date**: 2026-04-21

## Abstract

State types, backends, and consistency models in stream processing systems.

---

## 1. Definitions

### Def-K-04-01 (State)

$$State: (K, V, T) \rightarrow V'$$

- $K$: Key space (optional)
- $V$: Value space
- $T$: Time domain (for TTL)

### Def-K-04-02 (Operator State)

$$OperatorState: Op \rightarrow 2^{(K \times V)}$$

Bound to operator instance. All parallel subtasks share same state logic.

### Def-K-04-03 (Keyed State)

$$KeyedState: K \rightarrow V$$

Partitioned by data key. Same-key data guaranteed on same subtask.

### Def-K-04-04 (ValueState)

Stores single value per key.

---

## 2. State Types

| Type | API | Use Case |
|------|-----|----------|
| ValueState | `get()`, `update()` | Single value (counters) |
| ListState | `add()`, `get()` | Ordered collections |
| MapState | `put()`, `get()` | Key-value maps |
| ReducingState | `add()` | Incremental reduce |
| AggregatingState | `add()` | Incremental aggregate |

---

## 3. State Backends

| Backend | Storage | Best For |
|---------|---------|----------|
| HashMapStateBackend | JVM Heap | Small state, fast access |
| RocksDBStateBackend | Embedded RocksDB | Large state, spill to disk |
| ForStStateBackend (Flink 2.0) | Disaggregated (S3/HDFS) | Cloud-native, unlimited |

---

## 4. References

[^1]: Apache Flink Documentation, "State Backends", 2025.
[^2]: M. Kleppmann, "Designing Data-Intensive Applications", O'Reilly, 2017.
