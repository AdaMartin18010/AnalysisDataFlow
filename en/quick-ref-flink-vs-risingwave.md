# Flink vs RisingWave Quick Reference

> **Language**: English | **Source**: [Knowledge/98-exercises/quick-ref-flink-vs-risingwave.md](../Knowledge/98-exercises/quick-ref-flink-vs-risingwave.md) | **Last Updated**: 2026-04-21

---

## 30-Second Decision Guide

```
┌─────────────────────────────────────────────────────────────┐
│                    Core Decision Path                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Latency requirement < 50ms? ──YES──► Choose Flink       │
│                            │                                │
│                            NO                               │
│                            ▼                                │
│  2. Need CEP / Complex Event Matching? ──YES──► Choose Flink│
│                                   │                         │
│                                   NO                        │
│                                   ▼                         │
│  3. Need custom operators (non-SQL logic)? ──YES──► Flink   │
│                                        │                    │
│                                        NO                   │
│                                        ▼                    │
│  4. State size > 10TB? ──YES──► Choose RisingWave           │
│                            │                                │
│                            NO                               │
│                            ▼                                │
│  5. Team familiar with PostgreSQL? ──YES──► RisingWave      │
│                                │                            │
│                                NO                           │
│                                ▼                            │
│  6. Need low operational cost? ──YES──► RisingWave          │
│                         │                                   │
│                         NO                                  │
│                         ▼                                   │
│                    Either; go with team experience          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Scenario Matching

| Scenario | Preferred | Rationale |
|----------|-----------|-----------|
| Real-time fraud detection (< 100ms) | Flink | Low-latency stateful processing |
| Complex event processing (CEP) | Flink | Native CEP library |
| Ad-hoc analytics on streams | RisingWave | Materialized views, PostgreSQL protocol |
| Large-scale state (> 10TB) | RisingWave | Disaggregated state on S3 |
| Custom UDF/operator logic | Flink | DataStream API flexibility |
| Low-ops stream warehouse | RisingWave | Auto-scaling, serverless feel |

## Feature Matrix

| Feature | Flink | RisingWave |
|---------|-------|------------|
| **API** | DataStream, Table, SQL | SQL only |
| **Latency** | Sub-second to ms | Sub-second to seconds |
| **State Backend** | Heap, RocksDB, Incremental | Remote (S3/MinIO) |
| **CEP** | ✅ Native | ❌ Limited |
| **Custom Operators** | ✅ Full support | ❌ SQL UDF only |
| **Deployment** | K8s, YARN, Standalone | K8s, Docker |
| **Protocol** | Custom | PostgreSQL wire |

## When to Use Both

- **Flink** for ingestion, complex transformation, and CEP
- **RisingWave** for serving materialized views to BI tools
- Sync via Kafka or shared storage

## References
