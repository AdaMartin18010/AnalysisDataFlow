# Streaming Troubleshooting Guide

> **Language**: English | **Source**: [Knowledge/07-best-practices/07.03-troubleshooting-guide.md](../Knowledge/07-best-practices/07.03-troubleshooting-guide.md) | **Last Updated**: 2026-04-21

---

## Symptom → Cause → Fix

### Checkpoint Timeouts

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Checkpoint expired` | State too large; slow storage | Enable incremental checkpoints; use RocksDB with SSD |
| `Alignment timeout` | Backpressure during checkpoint | Reduce `alignmentTimeout`; enable unaligned checkpoints |
| `Async phase slow` | Serialization bottleneck | Use `TypeInformation`; avoid Java Serialization |

### Backpressure

```bash
# Identify backpressure source
flink run -d -p 4 my-job.jar
# Check Flink Web UI: Backpressure tab
# Red = HIGH, Yellow = LOW, Green = OK
```

| Backpressure Location | Action |
|-----------------------|--------|
| **Source** | Scale source partitions; check external system lag |
| **Operator** | Increase parallelism; optimize UDF; enable async I/O |
| **Sink** | Scale sink tasks; batch writes; use async sink |

### OOM / GC Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `OutOfMemoryError` | State too large for heap | Switch to RocksDB state backend |
| Long GC pauses | Large object allocation | Tune G1GC; reduce object churn |
| Metaspace OOM | Dynamic classloading | Increase `MaxMetaspaceSize` |

### Data Skew

```bash
# Check subtask records count in Flink UI
# If one subtask has 10x+ records:
```

| Skew Type | Mitigation |
|-----------|------------|
| **Hot key** | Add random salt; use two-phase aggregation |
| **Partition imbalance** | Custom partitioner; rebalance before keyed ops |
| **Time-window skew** | Use session windows; pre-aggregate per key |

### Watermark Lag

| Cause | Fix |
|-------|-----|
| Idle source partitions | Enable `withIdleness()` in WatermarkStrategy |
| Late data burst | Increase `allowedLateness`; route to side output |
| Clock skew | Use event time; sync NTP on source systems |

## Quick Diagnostic Commands

```bash
# JVM heap dump on OOM
-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp

# Flink job metrics via REST
curl http://jobmanager:8081/jobs/<job-id>/metrics

# Check RocksDB SST file count
ls -la $CHECKPOINT_DIR/*/chk-*/shared/*sst | wc -l
```

## References
