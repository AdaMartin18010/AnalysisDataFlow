---
title: "Stream Processing Anti-pattern Detection Checklist"
translation_status: ai_translated_reviewed
source_version: v4.1
last_sync: "2026-04-15"
---

# Stream Processing Anti-pattern Detection Checklist

> **Stage**: Knowledge/09-anti-patterns | **Formalization Level**: L3 | **Purpose**: Code review, production inspection, troubleshooting
>
> This checklist provides systematic anti-pattern detection methods, covering code review, configuration audit, and runtime monitoring三个阶段.

---

## Table of Contents

- [Stream Processing Anti-pattern Detection Checklist](#stream-processing-anti-pattern-detection-checklist)
  - [Table of Contents](#table-of-contents)
  - [1. Detection Phase Overview](#1-detection-phase-overview)
  - [2. Code Review Checklist](#2-code-review-checklist)
    - [2.1 State Management (AP-01, AP-07)](#21-state-management-ap-01-ap-07)
    - [2.2 I/O Processing (AP-05)](#22-io-processing-ap-05)
    - [2.3 Serialization (AP-06)](#23-serialization-ap-06)
  - [3. Configuration Audit Checklist](#3-configuration-audit-checklist)
    - [3.1 Watermark Configuration (AP-02)](#31-watermark-configuration-ap-02)
    - [3.2 Checkpoint Configuration (AP-03)](#32-checkpoint-configuration-ap-03)
    - [3.3 Memory Configuration (AP-10)](#33-memory-configuration-ap-10)
  - [4. Runtime Monitoring Checklist](#4-runtime-monitoring-checklist)
    - [4.1 Data Skew Monitoring (AP-04)](#41-data-skew-monitoring-ap-04)
    - [4.2 Backpressure Monitoring (AP-08)](#42-backpressure-monitoring-ap-08)
    - [4.3 Memory and GC Monitoring (AP-10)](#43-memory-and-gc-monitoring-ap-10)
  - [5. Troubleshooting Quick Reference](#5-troubleshooting-quick-reference)
    - [5.1 Symptom → Anti-pattern Mapping](#51-symptom--anti-pattern-mapping)
    - [5.2 Emergency Handling Process](#52-emergency-handling-process)
  - [6. Tool Recommendations](#6-tool-recommendations)
    - [6.1 Static Analysis Tools](#61-static-analysis-tools)
    - [6.2 Runtime Monitoring Tools](#62-runtime-monitoring-tools)
    - [6.3 Diagnostic Scripts](#63-diagnostic-scripts)
  - [7. Summary](#7-summary)
    - [7.1 Detection Priority](#71-detection-priority)
    - [7.2 Team Collaboration Flow](#72-team-collaboration-flow)

---

## 1. Detection Phase Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Anti-pattern Detection Lifecycle                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Development Phase           Test Phase           Production Phase     │
│   ───────────────            ───────────           ───────────          │
│        │                          │                      │              │
│        ▼                          ▼                      ▼              │
│   ┌─────────┐               ┌─────────┐            ┌─────────┐         │
│   │Code Review│─────────────►│Performance Test│─────►│Monitoring & Alerts│         │
│   │Checklist│               │Checklist│            │Checklist│         │
│   └─────────┘               └─────────┘            └─────────┘         │
│        │                          │                      │              │
│        ▼                          ▼                      ▼              │
│   Find issues              Find performance bottlenecks  Find online issues│
│        │                          │                      │              │
│        └───────────────────────────┴──────────────────────┘              │
│                                    │                                    │
│                                    ▼                                    │
│                            ┌─────────────┐                              │
│                            │  Fix & Verify │                              │
│                            └─────────────┘                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Code Review Checklist

### 2.1 State Management (AP-01, AP-07)

| Check Item | Danger Signal | Correct Approach |
|------------|---------------|------------------|
| **Global State** | Using `static` variables or `object` singletons to store state | Use `getRuntimeContext.getState()` |
| **State Type** | Using `ListState` to store large amounts of raw events | Use `ValueState` to store accumulators |
| **Window Function** | `ProcessWindowFunction` directly processing `Iterable` | Combine with `AggregateFunction` for pre-aggregation |
| **State Cleanup** | States without TTL configuration | Configure `StateTtlConfig` |

```scala
// ❌ Danger code checkpoints
class DangerCheck {

  // Checkpoint 1: Static variables
  static Map<String, Counter> globalMap = ... // ❌ AP-01

  // Checkpoint 2: Raw event accumulation
  class BadWindowFn extends ProcessWindowFunction[Event, Result, String, TimeWindow] {
    override def process(key: String, ctx: Context, elements: Iterable[Event], out: Collector[Result]) = {
      // elements may contain millions of events ❌ AP-07
    }
  }

  // Checkpoint 3: No TTL state
  val state = getRuntimeContext.getState(descriptor) // Missing TTL config ❌
}
```

### 2.2 I/O Processing (AP-05)

| Check Item | Danger Signal | Correct Approach |
|------------|---------------|------------------|
| **Database Access** | Using `JdbcTemplate.query()` and other synchronous APIs | Use `AsyncFunction` + async client |
| **HTTP Calls** | Using `HttpClient.execute()` | Use `AsyncHttpClient` or Vert.x |
| **Redis Access** | Using `Jedis.get()` | Use `Lettuce` async API |
| **RPC Calls** | Using synchronous gRPC stub | Use async gRPC stub |

```scala
// ❌ Danger code patterns
class IoCheck {

  // Checkpoint 1: JDBC synchronous query
  def queryDb(id: String): Result = {
    val stmt = conn.prepareStatement("SELECT ...") // ❌ AP-05
    stmt.executeQuery() // Blocking!
  }

  // Checkpoint 2: HTTP synchronous call
  def callApi(url: String): Response = {
    httpClient.execute(new HttpGet(url)) // Blocking! ❌ AP-05
  }

  // Checkpoint 3: Redis synchronous access
  def getCache(key: String): String = {
    jedis.get(key) // Blocking network I/O ❌ AP-05
  }
}
```

### 2.3 Serialization (AP-06)

| Check Item | Danger Signal | Correct Approach |
|------------|---------------|------------------|
| **Type Registration** | Custom case class not registered with Kryo | `env.getConfig.registerKryoType(classOf[X])` |
| **POJO Specification** | Missing no-arg constructor or getter/setter | Add `@BeanProperty` and no-arg constructor |
| **Serializer** | Complex types using default serialization | Implement custom `Serializer[T]` |

```scala
// ❌ Danger code
class SerializationCheck {

  // Checkpoint 1: Unregistered type
  case class MyEvent(a: String, b: Int) // Not registered ❌ AP-06

  // Checkpoint 2: Non-POJO structure
  class InvalidPojo(val field: String) { // Missing no-arg constructor ❌
    // Missing getter/setter
  }
}
```

---

## 3. Configuration Audit Checklist

### 3.1 Watermark Configuration (AP-02)

| Configuration Item | Check Rule | Recommended Value |
|--------------------|------------|-------------------|
| `forBoundedOutOfOrderness` | Does delay match source out-of-order degree? | p99 out-of-order delay + 20% margin |
| `withIdleness` | Is it configured in multi-stream scenarios? | Idle timeout = 2-5 minutes |
| `allowedLateness` | Does the window allow extra latency? | Set according to business tolerance |

```yaml
# Configuration check template
watermark:
  bounded_out_of_orderness:
    value: 10s  # Check: Based on actual measurement?
    measured_p99: 8s  # Should have measurement basis
  idleness:
    enabled: true  # Required in multi-stream scenarios
    timeout: 2m
  allowed_lateness:
    value: 5m  # Check: Need to capture late data?
```

### 3.2 Checkpoint Configuration (AP-03)

| Configuration Item | Check Rule | Recommended Value |
|--------------------|------------|-------------------|
| `checkpointInterval` | Does it satisfy RTO/5 < interval < RTO/2? | Calculate based on RTO |
| `checkpointTimeout` | Is it greater than typical Checkpoint duration × 2? | 30s - 10min |
| `minPauseBetweenCheckpoints` | Is it greater than Checkpoint duration? | 5s - 1min |
| `incrementalCheckpoints` | Is it enabled for large state (>1GB)? | Must enable |

```yaml
# Configuration check template
checkpoint:
  interval: 60s  # Check: RTO / 5 < 60s < RTO / 2 ?
  timeout: 300s
  min_pause: 30s  # Check: > checkpoint_duration ?
  incremental: true  # Check: state > 1GB ?

  # Calculation verification
  sla:
    rto: 300s  # Recovery Time Objective
    calculated_max: 150s  # RTO/2
    calculated_min: 60s   # RTO/5
    current: 60s  # Should be within range ✓
```

### 3.3 Memory Configuration (AP-10)

| Configuration Item | Check Rule | Recommended Value |
|--------------------|------------|-------------------|
| `managedMemory` | Is it > estimated state size / parallelism × 1.5? | Based on state estimation |
| `networkMemory` | Does it satisfy min(parallelism×64MB, 1GB)? | 256MB - 1GB |
| `jvmHeap` | Is it > max(managed memory×0.5, 2GB)? | 2GB - 8GB |

```yaml
# Configuration check template
memory:
  estimated_state_gb: 50
  parallelism: 10

  calculated:
    managed_per_tm: 7.5gb  # 50/10 * 1.5
    required_total: 12gb   # (7.5 + 2 + 0.5) * 1.2

  configured:
    managed: 8gb  # Check: >= 7.5gb ?
    total: 12gb   # Check: >= 12gb ?
```

---

## 4. Runtime Monitoring Checklist

### 4.1 Data Skew Monitoring (AP-04)

| Metric | Alert Rule | Check Method |
|--------|------------|--------------|
| `recordsInPerSecond` | Difference between subtasks > 5x | Flink Web UI |
| `backPressuredTimeMsPerSecond` | Concentrated in few subtasks | Flink Web UI |
| `stateSize` | Difference between subtasks > 10x | Checkpoint statistics |

```bash
# Skew detection script (based on Flink REST API)
curl -s "http://flink:8081/jobs/${JOB_ID}/vertices/${VERTEX_ID}/subtasks/metrics?get=recordsInPerSecond" | \
  jq '.[].value' | \
  awk '{sum+=$1; max=$1>max?$1:max; min=$1<min||min==0?$1:min} END {print "Skew ratio:", max/min}'
# Output > 5 indicates skew exists
```

### 4.2 Backpressure Monitoring (AP-08)

| Metric | Alert Rule | Handling Recommendation |
|--------|------------|-------------------------|
| `backPressuredTimeMsPerSecond` | > 200ms/s | Scale out or optimize |
| `outputQueueLength` | Continuous growth | Check downstream bottleneck |
| `checkpointDuration` | Continuous growth | Large state or backpressure |

```yaml
# Prometheus alert rules
groups:
  - name: flink_backpressure
    rules:
      - alert: FlinkHighBackpressure
        expr: flink_taskmanager_job_task_backPressuredTimeMsPerSecond > 200
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Flink task backpressure high"

      - alert: FlinkCheckpointTimeout
        expr: flink_jobmanager_checkpoint_duration_time > 600000
        for: 1m
        labels:
          severity: critical
```

### 4.3 Memory and GC Monitoring (AP-10)

| Metric | Alert Rule | Handling Recommendation |
|--------|------------|-------------------------|
| `heapMemoryUsage` | > 85% | Increase heap memory |
| `gcCollectionTime` | > 10% | Optimize serialization or reduce state |
| `managedMemoryUsage` | > 90% | Increase managed memory |

---

## 5. Troubleshooting Quick Reference

### 5.1 Symptom → Anti-pattern Mapping

| Symptom | Possible Anti-pattern | Quick Check |
|---------|-----------------------|-------------|
| Throughput suddenly drops | AP-05, AP-08 | Check for blocking I/O, view backpressure |
| Frequent OOM | AP-07, AP-10 | Check window state size, memory config |
| Checkpoint timeout | AP-03, AP-07, AP-10 | Check interval config, state size |
| Inconsistent results | AP-02, AP-09 | Check Watermark config, multi-stream Join |
| Slow failure recovery | AP-03 | Check Checkpoint interval |
| Low CPU but high latency | AP-05 | Check for blocking I/O |
| Some subtasks particularly slow | AP-04 | Check data skew |

### 5.2 Emergency Handling Process

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Emergency Fault Handling Process                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  【Failure Discovered】                                                 │
│       │                                                                 │
│       ▼                                                                 │
│  【Assess Severity】                                                    │
│       │                                                                 │
│       ├──► Job Failed ──► 【Checkpoint Recovery】 ──► Success ──►      │
│       │                      │                    │                     │
│       │                      ▼                    ▼                     │
│       │                   No Checkpoint        Fix Anti-pattern         │
│       │                      │                    │                     │
│       │                      ▼                    ▼                     │
│       │                   【Data Replay】      【Regression Test】       │
│       │                      │                                          │
│       │                      ▼                                          │
│       │                   【Notify Business Team】                       │
│       │                                                                 │
│       └──► Performance Degraded ──► 【Check Metrics】                   │
│                              │                                          │
│                              ▼                                          │
│                      【Locate Bottleneck Operator】                     │
│                              │                                          │
│                              ▼                                          │
│                      【Apply Corresponding Solution】                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Tool Recommendations

### 6.1 Static Analysis Tools

| Tool | Purpose | Integration |
|------|---------|-------------|
| **Checkstyle** | Code style check | Maven/Gradle plugin |
| **SpotBugs** | Potential bug detection | CI/CD integration |
| **Custom AST Check** | Flink-specific anti-patterns | Pre-commit hook |

### 6.2 Runtime Monitoring Tools

| Tool | Purpose | Data Source |
|------|---------|-------------|
| **Flink Web UI** | Backpressure, latency, throughput visualization | Flink REST API |
| **Prometheus + Grafana** | Metrics collection and alerting | Flink Metrics Reporter |
| **Jaeger/Zipkin** | Distributed tracing | OpenTelemetry |

### 6.3 Diagnostic Scripts

```bash
#!/bin/bash
# Flink job health check script

JOB_ID=$1
FLINK_URL=${2:-"http://localhost:8081"}

echo "=== Flink Job Health Check ==="
echo "Job ID: $JOB_ID"

# 1. Check backpressure
echo -e "\n[1/5] Checking backpressure..."
BACKPRESSURE=$(curl -s "$FLINK_URL/jobs/$JOB_ID/vertices" | jq '.vertices[] | select(.metrics.backPressuredTimeMsPerSecond > 200) | .name')
if [ -n "$BACKPRESSURE" ]; then
  echo "⚠️  High backpressure detected in:"
  echo "$BACKPRESSURE"
else
  echo "✓ Backpressure normal"
fi

# 2. Check Checkpoint
echo -e "\n[2/5] Checking checkpoints..."
CHECKPOINT_STATS=$(curl -s "$FLINK_URL/jobs/$JOB_ID/checkpoints")
FAILED=$(echo $CHECKPOINT_STATS | jq '.counts.failed')
if [ "$FAILED" -gt 0 ]; then
  echo "⚠️  $FAILED failed checkpoints detected"
else
  echo "✓ Checkpoints healthy"
fi

# 3. Check data skew
echo -e "\n[3/5] Checking data skew..."
# Implement similar skew detection logic as above

echo -e "\n=== Check Complete ==="
```

---

## 7. Summary

### 7.1 Detection Priority

| Priority | Anti-pattern | Detection Timing | Detection Cost |
|----------|--------------|------------------|----------------|
| P0 | AP-08, AP-10 | Real-time monitoring | Low |
| P1 | AP-02, AP-03, AP-04, AP-05, AP-07, AP-09 | Code review + runtime | Medium |
| P2 | AP-01, AP-06 | Code review | Low |

### 7.2 Team Collaboration Flow

```
Developer ──► Code Review Checklist ──► Pre-submission self-check
    │
    ▼
Code Reviewer ──► Focus on AP-01, AP-05, AP-06
    │
    ▼
Test Engineer ──► Performance Test ──► Check AP-02, AP-03, AP-04
    │
    ▼
Ops Engineer ──► Production Monitoring ──► Check AP-08, AP-10
```

---

*Document Version: v1.0 | Updated: 2026-04-03 | Status: Complete*
