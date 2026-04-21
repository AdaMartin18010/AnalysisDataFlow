# Anti-Pattern AP-10: Insufficient Resource Estimation (OOM)

> **Stage**: Knowledge/09-anti-patterns | **Prerequisites**: [State Management Concepts](state-management-concepts.md) | **Formalization Level**: L3
> **Translation Date**: 2026-04-21

## Abstract

Deploying Flink jobs without proper memory estimation leads to OOM errors, frequent Full GC, and checkpoint failures. This anti-pattern formalizes the memory model and provides estimation formulas.

---

## 1. Definition

### Def-K-09-10 (Insufficient Resource Estimation)

**Insufficient resource estimation** means deploying Flink jobs without accounting for state size, network buffers, JVM overhead, causing runtime OOM or frequent Full GC.

**Memory requirement model**:

```
Total Memory =
  + Managed Memory (state)
  + Network Memory (buffers)
  + JVM Metaspace
  + JVM Heap Memory
  + Native Memory (RocksDB)
  + Reserve (20%)
```

---

## 2. Symptoms

- `OutOfMemoryError` in TaskManager logs
- Frequent Full GC pauses (> 1s)
- Checkpoint timeouts due to GC pressure
- TaskManager container restarts (Kubernetes OOMKill)

## 3. Negative Impacts

### 3.1 OOM Cascade Failure

```
TM1 OOM → Restart → State recovery from checkpoint → Higher memory pressure → Faster OOM
     ↓
JobManager marks task as failed → Restart strategy triggers → Cascading restart loop
```

---

## 4. Solution

### 4.1 Memory Estimation Formula

$$\text{TM Memory} = \text{State Size} \times 1.5 + \text{Network Buffer} + \text{JVM Heap} + \text{Native} + 20\%$$

| Component | Formula | Example |
|-----------|---------|---------|
| State (RocksDB) | StateSize × 1.5 (index overhead) | 10GB state → 15GB |
| Network Buffer | #Slots × BufferSize × #Channels | 4 slots × 32KB × 100 = 12.8MB |
| JVM Heap | User objects + Framework overhead | 2-4GB typical |
| Native | RocksDB block cache + OS buffers | 10-20% of managed |

### 4.2 Correct Configuration

```java
// Flink configuration
env.setParallelism(4);

// TaskManager: 8GB total, 4 slots → 2GB per slot
// taskmanager.memory.process.size: 8192m
// taskmanager.memory.managed.fraction: 0.4 (for RocksDB)
// taskmanager.memory.network.fraction: 0.1
```

### 4.3 Use RocksDB for Large State

```java
// Switch to RocksDB to reduce heap pressure
env.setStateBackend(new EmbeddedRocksDBStateBackend(true));
```

---

## 5. Code Examples

### 5.1 Incorrect (OOM-prone)

```java
// Using MemoryStateBackend with 100GB state
env.setStateBackend(new MemoryStateBackend());  // Will OOM!
```

### 5.2 Correct

```java
// Using RocksDBStateBackend for large state
env.setStateBackend(new EmbeddedRocksDBStateBackend(true));
env.getCheckpointConfig().setCheckpointStorage("hdfs:///checkpoints");
```

---

## 6. References

[^1]: Apache Flink Documentation, "Memory Configuration", 2025.
[^2]: Apache Flink Documentation, "State Backends", 2025.
[^3]: RocksDB Documentation, "Memory Usage", Meta, 2025.
