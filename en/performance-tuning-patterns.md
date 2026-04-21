# Performance Tuning Patterns

> **Stage**: Knowledge/07-best-practices | **Prerequisites**: [Serialization Overhead Anti-pattern](anti-pattern-serialization-overhead.md) | **Formalization Level**: L3
> **Translation Date**: 2026-04-21

## Abstract

This document provides systematic performance tuning patterns for Flink jobs, covering serialization, network, state access, and JVM optimizations.

---

## 1. Definitions

### Def-K-07-02 (Performance Tuning Pattern)

A **performance tuning pattern** is a reusable optimization for common stream processing bottlenecks, reducing compute, network, or storage overhead.

### Key Performance Indicators (KPIs)

| Metric | Definition | Measurement | Goal |
|--------|-----------|-------------|------|
| **Throughput** | Records processed per second | `numRecordsInPerSecond` | Maximize |
| **Latency** | Input-to-output time | `currentOutputWatermark - inputTimestamp` | Minimize |
| **Backpressure** | Upstream blocking due to slow downstream | `backPressuredTimeMsPerSecond` | Minimize |
| **Checkpoint Duration** | State snapshot time | `checkpointDuration` | Minimize |
| **CPU Utilization** | Effective compute ratio | `cpuTime` / wallTime | Maximize |

---

## 2. Optimization Patterns

### 2.1 Serialization Optimization

**Problem**: Java serialization is slow and creates garbage.

**Solutions**:

| Approach | Speedup | Effort |
|----------|---------|--------|
| POJOs with Flink serializers | 2-5x | Low (use plain classes) |
| Avro/Protobuf/Thrift | 3-10x | Medium (schema definition) |
| Kryo (custom registrators) | 1.5-3x | Low |
| Off-heap binary formats | 5-20x | High |

```java
// Use POJOs for automatic serializer generation
public class ClickEvent {
    public long userId;
    public long itemId;
    public long timestamp;
}

// Or register Kryo serializers
env.getConfig().registerTypeWithKryoSerializer(MyClass.class, MySerializer.class);
```

### 2.2 Network Optimization

**Problem**: Network buffers are the bottleneck for shuffle-heavy jobs.

**Solutions**:
- Increase network buffer fraction: `taskmanager.memory.network.fraction = 0.15`
- Enable compression for large records: `pipeline.compression = SNAPPY`
- Reduce object reuse: `object-reuse-mode = true`

### 2.3 State Access Optimization

**Problem**: State backend choice dramatically impacts performance.

| Backend | Latency | Capacity | Best For |
|---------|---------|----------|----------|
| Memory | ~100ns | Heap-limited | Small state, dev |
| RocksDB | ~1-10μs | Disk | Large state, production |
| ForSt | ~10-100μs | Cloud storage | Disaggregated state |

**State access patterns**:
- Use `ValueState` over `ListState` for single values
- Enable incremental checkpointing for large state
- Use state TTL to prevent unbounded growth

### 2.4 JVM Optimization

```java
// JVM options for Flink
-Xms4g -Xmx4g                    // Fixed heap size
-XX:+UseG1GC                     // G1 garbage collector
-XX:MaxDirectMemorySize=1g       // Off-heap memory
-XX:+UnlockDiagnosticVMOptions   // Advanced diagnostics
```

---

## 3. Tuning Decision Tree

```
Is throughput the bottleneck?
├── YES → Is serialization CPU-bound?
│         ├── YES → Use POJOs / Avro
│         └── NO  → Is network saturated?
│                   ├── YES → Increase buffers, enable compression
│                   └── NO  → Is state access slow?
│                             ├── YES → Tune RocksDB, enable cache
│                             └── NO  → Scale out (add parallelism)
└── NO  → Is latency the bottleneck?
          ├── YES → Reduce buffer timeout, enable object reuse
          └── NO  → Is checkpoint too slow?
                    ├── YES → Incremental checkpoint, tune timeout
                    └── NO  → Profile JVM (GC, heap)
```

---

## 4. References

[^1]: Apache Flink Documentation, "Performance Tuning", 2025.
[^2]: Apache Flink Documentation, "Memory Configuration", 2025.
[^3]: RocksDB Documentation, "Tuning Guide", Meta, 2025.
