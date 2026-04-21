# Quick Reference: Flink vs RisingWave

> **Stage**: Knowledge/98-exercises | **Prerequisites**: [Engine Selection Guide](engine-selection-guide.md) | **Formalization Level**: L3
> **Translation Date**: 2026-04-21

## Abstract

Quick comparison between Apache Flink and RisingWave for stream processing workloads.

---

## 1. Comparison Matrix

| Dimension | Apache Flink | RisingWave |
|-----------|-------------|------------|
| **Model** | Dataflow / DAG | Streaming SQL / Materialized Views |
| **State** | Explicit (Keyed/Operator) | Implicit (Materialized Views) |
| **API** | DataStream, Table API, SQL | SQL only |
| **Deployment** | Self-hosted, K8s, Ververica | Cloud-native, Serverless |
| **Latency** | ~10-100ms | ~100ms-1s |
| **Throughput** | Very high | High |
| **Use Case** | Complex event processing, ETL | Real-time analytics, dashboards |

---

## 2. Decision Guide

```
Need complex event-time processing?
├── YES → Flink
└── NO  → Need declarative SQL-only?
          ├── YES → RisingWave
          └── NO  → Evaluate both
```

---

## 3. References
