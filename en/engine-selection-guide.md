# Stream Processing Engine Selection Guide

> **Stage**: Knowledge/04-technology-selection | **Prerequisites**: [Expressiveness Hierarchy](expressiveness-hierarchy.md) | **Formalization Level**: L4-L6
> **Translation Date**: 2026-04-21

## Abstract

This guide provides a systematic framework for selecting stream processing engines across six dimensions: latency, throughput, state management, consistency, expressiveness, and ecosystem.

---

## 1. Definitions

### Def-K-04-01 (Apache Flink)

Native streaming engine with event-time semantics, exactly-once guarantees, and advanced state management.

### Def-K-04-02 (Kafka Streams)

Lightweight stream processing library embedded in Kafka clients. Best for stream-stream joins and event-driven microservices.

### Def-K-04-03 (Spark Structured Streaming)

Micro-batch engine with Spark SQL integration. Best for unified batch/streaming analytics.

### Def-K-04-04 (Apache Storm)

Low-latency record-at-a-time engine. Best for sub-10ms latency requirements.

### Def-K-04-05 (Pulsar Functions)

Serverless event processing on Pulsar topics. Best for simple transformations.

---

## 2. Comparison Matrix

| Dimension | Flink | Kafka Streams | Spark SS | Storm |
|-----------|-------|--------------|----------|-------|
| Latency | 10-100ms | 10-100ms | 100ms-1s | <10ms |
| Throughput | Very High | High | High | Very High |
| State | Advanced (RocksDB) | Local (RocksDB) | HDFS-based | In-memory |
| Exactly-Once | ✅ Native | ✅ Transactional | ✅ Idempotent | ⚠️ At-Least-Once |
| Event Time | ✅ Native | ✅ Supported | ✅ Supported | ❌ |
| SQL | ✅ Table API | ❌ KSQL | ✅ Spark SQL | ❌ |

---

## 3. Decision Framework

```
Need sub-100ms latency?
├── YES → Need exactly-once?
│         ├── YES → Flink
│         └── NO  → Storm
└── NO  → Need unified batch/streaming?
          ├── YES → Spark SS
          └── NO  → Already using Kafka?
                    ├── YES → Kafka Streams
                    └── NO  → Flink (default)
```

---

## 4. References

[^1]: Apache Flink Documentation, 2025.
[^2]: Confluent, "Kafka Streams vs Flink", 2024.
[^3]: Databricks, "Structured Streaming Guide", 2025.
