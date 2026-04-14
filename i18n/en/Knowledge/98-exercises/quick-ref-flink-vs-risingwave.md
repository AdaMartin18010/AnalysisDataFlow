---
title: "Flink vs RisingWave Quick Reference Card"
translation_status: ai_translated_reviewed
source_version: v4.1
last_sync: "2026-04-15"
---

# Flink vs RisingWave Quick Reference Card

> **Quick Reference**: Stream processing engine selection decisions, performance comparisons, and feature matrices
>
> **Full Document**: [flink-vs-risingwave.md](../04-technology-selection/flink-vs-risingwave.md)

---

## 🎯 Selection Decision Quick Reference

### 30-Second Decision Method

```
┌─────────────────────────────────────────────────────────────┐
│                    Core Decision Path                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Latency requirement < 50ms? ──YES──► Choose Flink       │
│                            │                                │
│                            NO                               │
│                            ▼                                │
│  2. Need CEP / complex event matching? ──YES──► Choose Flink│
│                                   │                         │
│                                   NO                        │
│                                   ▼                         │
│  3. Need custom operators (non-SQL logic)? ──YES──► Choose Flink│
│                                        │                    │
│                                        NO                   │
│                                        ▼                    │
│  4. State size > 10TB? ──YES──► Choose RisingWave           │
│                            │                                │
│                            NO                               │
│                            ▼                                │
│  5. Team familiar with PostgreSQL? ──YES──► Choose RisingWave│
│                                │                            │
│                                NO                           │
│                                ▼                            │
│  6. Need low operational cost? ──YES──► Choose RisingWave   │
│                         │                                   │
│                         NO                                  │
│                         ▼                                   │
│                    Both are viable, decide by team experience│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Scenario Matching Quick Reference

| Application Scenario | Preferred Choice | Reason |
|----------------------|------------------|--------|
| **Real-time data warehouse / CDC sync** | RisingWave | Native CDC + materialized views, no Kafka needed |
| **Real-time recommendations (low latency)** | Flink | Millisecond-level latency advantage |
| **Financial risk control CEP** | Flink | RisingWave does not support MATCH_RECOGNIZE |
| **IoT data analysis** | RisingWave | Unlimited state support |
| **Real-time reports / dashboards** | RisingWave | Ad-hoc query friendly, PostgreSQL protocol |
| **Complex ETL pipelines** | Flink | Richer connector ecosystem |
| **Edge stream processing** | Flink | Better support for resource-constrained environments |

---

## ⚡ Performance Comparison Quick Reference

### Nexmark Benchmark

| Query | Description | RisingWave | Flink | Difference |
|-------|-------------|------------|-------|------------|
| q0-q3 | Simple throughput | ~893k r/s | ~800k r/s | RW +12% |
| q4 | Window aggregation | 84.3k r/s | 70k r/s | RW +20% |
| q7 | Complex state | **219k r/s** | ~3.5k r/s | **RW 62x** |
| q7-optimized | Rewritten version | **770k r/s** | - | **RW 220x** |

### Key Performance Metrics

| Metric | Flink 1.18 | RisingWave | Winner |
|--------|------------|------------|--------|
| **Minimum Latency** | ~5ms | ~50ms | Flink |
| **Typical Latency** | 10-100ms | 100ms-1s | Flink |
| **Checkpoint Time** | 30s-minute level | **1s** | RisingWave |
| **Failure Recovery** | Minute-level | **Second-level** | RisingWave |
| **Complex Join Throughput** | 3.5k r/s | **219k r/s** | RisingWave |
| **Memory Efficiency** | Medium | **High** | RisingWave |
| **CPU Utilization** | Medium | **High** | RisingWave |

### Architecture Comparison

```
┌─────────────────────────────────────────────────────────────┐
│  Apache Flink                    RisingWave                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐                ┌──────────────┐          │
│  │  JobManager  │                │   Meta Node  │          │
│  │  (Scheduling)│                │  (Scheduling)│          │
│  └──────┬───────┘                └──────┬───────┘          │
│         │                               │                   │
│  ┌──────▼──────────────────┐   ┌────────▼────────┐         │
│  │    TaskManager Pool     │   │  Compute Nodes  │         │
│  │  ┌─────┐ ┌─────┐ ┌────┐ │   │  (Stateless)    │         │
│  │  │Slot │ │Slot │ │Slot│ │   └────────┬────────┘         │
│  │  │+    │ │+    │ │+   │ │            │                   │
│  │  │Rock│ │Rock│ │Rock│ │   ┌─────────▼─────────┐         │
│  │  │sDB │ │sDB │ │sDB │ │   │  Hummock Layer    │         │
│  │  └─────┘ └─────┘ └────┘ │   │  (LSM-Tree)       │         │
│  │   ↑Local state storage   │   └─────────┬─────────┘         │
│  │   ↓Async snapshot        │             │                   │
│  │  ┌─────────────────────┐ │   ┌─────────▼─────────┐         │
│  └──┤  S3/HDFS Checkpoint │─┘   │  S3/GCS/Azure Blob│         │
│     └─────────────────────┘     │  (Primary Storage)│         │
│                                 └───────────────────┘         │
│                                                             │
│  Tight compute-storage coupling    Compute-storage separation │
│  Local state access (low latency)  Remote state access (scalable)│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Feature Comparison Matrix

### Core Features

| Feature | Flink | RisingWave | Notes |
|---------|-------|------------|-------|
| **SQL Dialect** | Flink SQL | PostgreSQL | RW compatible with psql ecosystem |
| **Materialized Views** | ⚠️ Limited | ✅ Native core | RW incremental maintenance |
| **Ad-hoc Queries** | ❌ Needs external DB | ✅ Built-in | RW supports point lookups |
| **CDC Sources** | Flink CDC | Native direct connection | RW no Kafka middleware needed |
| **CEP Support** | ✅ MATCH_RECOGNIZE | ❌ Not supported | Flink advantage scenario |
| **Window Types** | Rich | Standard | Flink more flexible |
| **Custom Operators** | ✅ DataStream API | ❌ SQL only | Flink highly extensible |
| **UDF Support** | Java/Python/Scala | Python/Java/Rust | Comparable |
| **Connector Count** | 50+ | 50+ | Comparable |
| **Data Lake Sink** | Paimon/Iceberg | Iceberg/Delta | Comparable |
| **Vector Search** | ❌ | ✅ v2.6+ | RW leading |

### Architecture Features

| Feature | Flink 1.x | Flink 2.0 | RisingWave |
|---------|-----------|-----------|------------|
| **Compute-Storage** | Tight coupling | Loose coupling (ForSt) | Fully separated |
| **State Location** | Local RocksDB | Local+S3 | S3 primary storage |
| **State Access Latency** | ~10μs | ~10μs-10ms | ~10ms (cacheable) |
| **Compute Nodes** | Stateful | Hybrid | Stateless |
| **Scaling Operation** | Stop→Redistribute→Start | Progressive rebalancing | Hot scaling |
| **Programming Language** | Java/Scala | Java/Scala | Rust |
| **Runtime** | JVM | JVM | Native binary |

---

## 💰 Operational Cost Comparison

| Cost Item | Flink | RisingWave | Winner |
|-----------|-------|------------|--------|
| **Infrastructure Cost** | High (large memory + SSD) | Low (S3 + small memory) | RW |
| **Ops Personnel** | High (cluster management) | Low (managed service-like) | RW |
| **State Tuning** | Needs RocksDB expertise | No tuning needed | RW |
| **Scaling Operation** | Downtime redistribution | Hot scaling | RW |
| **Learning Curve** | Steep (many concepts) | Gentle (SQL only) | RW |
| **Cloud Service Maturity** | High (Ververica, etc.) | Medium (growing) | Flink |
| **Community Size** | Large (top Apache project) | Medium (rapidly growing) | Flink |

---

## ✅ Selection Checklist

### Choose Flink if any condition applies

- [ ] End-to-end latency requirement < 50ms
- [ ] Need complex event processing (CEP / MATCH_RECOGNIZE)
- [ ] Need custom operators (logic not expressible in SQL)
- [ ] Need DataStream API for fine-grained control
- [ ] Have dedicated stream processing team willing to invest learning cost
- [ ] Have existing Flink infrastructure and operational experience
- [ ] Need deep integration with specific ecosystems (e.g., Paimon)

### Choose RisingWave if any condition applies

- [ ] Team familiar with PostgreSQL, wants SQL-first development
- [ ] Expected state size exceeds 10TB or unpredictable
- [ ] Need built-in materialized views and ad-hoc query capabilities
- [ ] Want to simplify CDC pipelines (direct MySQL/PostgreSQL connection)
- [ ] Want to reduce operational complexity (single-binary deployment)
- [ ] Want to reduce storage costs (S3 instead of SSD)
- [ ] Need fast failure recovery (second-level RTO)
- [ ] Frequent elastic scaling needs (cloud-native environment)

### Consider hybrid architecture if

- [ ] Have both low-latency scenarios and SQL analytics needs
- [ ] Have existing Flink cluster but want to simplify some SQL pipelines
- [ ] Data volume is extremely large, need tiered processing (real-time + analytics layers)

---

## 🔄 Migration Recommendations Quick Reference

| Migration Path | Difficulty | Risk | Recommendation |
|----------------|------------|------|----------------|
| Flink SQL → RisingWave | Low | Low | SQL semantics compatible, direct migration possible |
| Flink DataStream → RisingWave | High | High | Need to rewrite as SQL, assess feasibility |
| Spark Streaming → RisingWave | Medium | Medium | SQL layer migration relatively smooth |
| ksqlDB → RisingWave | Low | Low | RisingWave fully covers ksqlDB capabilities |
| RisingWave → Flink | Medium | Medium | If CEP or lower latency needed |

---

## 📚 Further Reading

| Document | Content |
|----------|---------|
| [flink-vs-risingwave.md](../04-technology-selection/flink-vs-risingwave.md) | Full in-depth comparison analysis |
| [risingwave-deep-dive.md](../06-frontier/risingwave-deep-dive.md) | RisingWave deep dive |
| [engine-selection-guide.md](../04-technology-selection/engine-selection-guide.md) | General stream processing engine selection guide |
| [streaming-database-guide.md](../04-technology-selection/streaming-database-guide.md) | Streaming database selection guide |

---

*Quick Reference Card v1.0 | Last Updated: 2026-04-03*
