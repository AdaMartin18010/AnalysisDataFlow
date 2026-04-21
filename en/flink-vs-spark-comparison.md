# Flink vs Spark Structured Streaming (2026)

> **Stage**: Knowledge/04-technology-selection | **Prerequisites**: [Checkpoint Mechanism](../../Flink/02-core/checkpoint-mechanism-deep-dive.md) | **Formalization Level**: L3-L4
> **Translation Date**: 2026-04-21

## Abstract

Deep comparison of Apache Flink and Spark Structured Streaming across latency, throughput, semantics, and ecosystem dimensions.

---

## 1. Architecture Comparison

| Aspect | Flink | Spark Structured Streaming |
|--------|-------|---------------------------|
| Processing Model | Native streaming | Micro-batch (continuous available) |
| Latency | < 100ms typical | ~100ms-1s typical |
| State Backend | RocksDB/HashMap/ForSt | HDFS-based checkpoint |
| SQL Engine | Flink SQL (Calcite) | Spark SQL (Catalyst) |
| Deployment | Standalone/YARN/K8s | YARN/K8s/Standalone |

---

## 2. Flink 2026 Key Capabilities

- **Async State** (Flink 2.0): Non-blocking state access via AEC
- **ForSt State Backend**: Cloud-native disaggregated storage
- **Adaptive Execution**: Runtime plan optimization
- **Streaming Warehouse**: Native Paimon/Iceberg sink

---

## 3. When to Choose

### Choose Flink When

- Latency < 100ms required
- Complex event time processing
- Stateful operations with large state
- Exactly-once end-to-end required

### Choose Spark When

- Unified batch + streaming acceptable
- Existing Spark ecosystem
- Interactive analytics priority
- Simpler operational requirements

---

## 4. References
