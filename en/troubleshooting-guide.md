# Troubleshooting Guide

> **Stage**: Knowledge/07-best-practices | **Prerequisites**: [Anti-pattern Checklist](anti-pattern-checklist.md) | **Formalization Level**: L3
> **Translation Date**: 2026-04-21

## Abstract

Systematic troubleshooting流程 for Flink jobs, covering symptom-to-root-cause mapping, diagnostic tools, and debugging techniques.

---

## 1. Definitions

### Def-K-07-03 (Troubleshooting Process)

**Troubleshooting process**: systematic steps to locate, analyze, and resolve anomalous behavior and performance issues.

### Fault Classification

```
Flink Fault Classification
├── Job-Level Faults
│   ├── Crash (OOM, exception)
│   ├── Backpressure
│   ├── Checkpoint failure
│   └── Data skew
├── Cluster-Level Faults
│   ├── TM failure
│   ├── JM failure
│   └── Network partition
└── External Faults
    ├── Source lag
    ├── Sink slowdown
    └── Dependency outage
```

---

## 2. Diagnostic Methodology

### Phase 1: Information Gathering

1. Check job status (Web UI / CLI)
2. Review exception logs
3. Examine metrics (backpressure, checkpoint, throughput)
4. Verify configuration

### Phase 2: Common Fault Diagnosis

| Symptom | Likely Cause | Diagnostic Tool |
|---------|-------------|-----------------|
| OOM | Memory leak, large state | Heap dump, GC log |
| Backpressure | Slow sink, data skew | Backpressure metric, flame graph |
| Checkpoint timeout | Large state, network issue | Checkpoint metric, TM log |
| Low throughput | Serialization, I/O wait | CPU profile, network monitor |

---

## 3. Debugging Techniques

### 3.1 Local Replay

```bash
# Run job locally with test data
flink run -local my-job.jar
```

### 3.2 Logging

```java
// Structured logging
LOG.info("Processing record: {}", record,
    StructuredArguments.keyValue("partition", ctx.getIndex()));
```

### 3.3 Metrics Inspection

Key metrics to monitor:

- `numRecordsInPerSecond` / `numRecordsOutPerSecond`
- `backPressuredTimeMsPerSecond`
- `checkpointDuration`
- `heapUsed` / `heapCommitted`

---

## 4. Quick Fix Cheat Sheet

| Problem | Quick Fix |
|---------|-----------|
| OOM | Increase heap, use RocksDB, check for memory leaks |
| Backpressure | Scale out, optimize sink, enable async I/O |
| Skew | Rescale key distribution, use salting |
| Slow checkpoint | Incremental checkpoint, tune timeout |

---

## 5. References
