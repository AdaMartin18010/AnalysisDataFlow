# Flink State Management Complete Guide

> **Stage**: Flink/02-core | **Prerequisites**: [Checkpoint Mechanism](flink-checkpoint-mechanism.md) | **Formalization Level**: L4
> **Translation Date**: 2026-04-21

## Abstract

Comprehensive guide to Flink state backends, state types, TTL, and checkpoint mechanisms.

---

## 1. State Backends

| Backend | Storage | Latency | Capacity | Best For |
|---------|---------|---------|----------|----------|
| HashMapStateBackend | JVM Heap | < 1μs | Limited by heap | Small state, fast access |
| EmbeddedRocksDBStateBackend | Local RocksDB | ~10μs | Limited by disk | Large state, spillable |
| ForStStateBackend (Flink 2.0+) | Disaggregated (S3/HDFS) | ~100μs | Unlimited | Cloud-native, elastic |

---

## 2. State Types

```java
// ValueState
ValueStateDescriptor<Long> descriptor =
    new ValueStateDescriptor<>("counter", Types.LONG);
ValueState<Long> state = getRuntimeContext().getState(descriptor);

// ListState
ListStateDescriptor<Event> listDescriptor =
    new ListStateDescriptor<>("events", Event.class);

// MapState
MapStateDescriptor<String, Integer> mapDescriptor =
    new MapStateDescriptor<>("counts", String.class, Integer.class);
```

---

## 3. State TTL

```java
StateTtlConfig ttlConfig = StateTtlConfig
    .newBuilder(Time.hours(24))
    .setUpdateType(StateTtlConfig.UpdateType.OnCreateAndWrite)
    .setStateVisibility(StateTtlConfig.StateVisibility.NeverReturnExpired)
    .build();
descriptor.enableTimeToLive(ttlConfig);
```

---

## 4. References
