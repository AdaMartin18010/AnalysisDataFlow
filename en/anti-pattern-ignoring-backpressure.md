# Anti-Pattern AP-08: Ignoring Backpressure Signals

> **Stage**: Knowledge/09-anti-patterns | **Prerequisites**: [Backpressure Guide](backpressure-guide.md) | **Formalization Level**: L3
> **Translation Date**: 2026-04-21

## Abstract

Ignoring Flink's backpressure signals and continuing to increase input rate leads to cascading failures, data loss, and service unavailability.

---

## 1. Definition

### Def-K-09-08 (Ignoring Backpressure)

**Ignoring backpressure** means taking no mitigation measures when backpressure occurs, instead increasing input load or refusing resource adjustments.

**Backpressure propagation**:

```
Slow downstream → Buffer full → Pause read → Upstream buffer full → Propagate
       ↑                                                           │
       └── Backpressure signal ◄────────────────────────────────────┘
```

---

## 2. Symptoms

- Increasing end-to-end latency
- Dropping throughput despite increased input
- Growing memory usage (buffers accumulating)
- Checkpoint timeouts
- Eventually: OOM or job failure

## 3. Negative Impacts

### 3.1 Cascade Failure

```
Backpressure at Sink → TM buffer full → Network credit = 0
    → Source reduces read → Source backlog grows → Kafka lag spikes
    → Consumer group rebalances → Additional disruption
```

---

## 4. Solution

### 4.1 Monitor Backpressure Metrics

```java
// Key metrics to watch
backPressuredTimeMsPerSecond > 100  // Warning
backPressuredTimeMsPerSecond > 500  // Critical
```

### 4.2 Auto-Scaling

```yaml
# Kubernetes HPA for Flink
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: flink-taskmanager
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Pods
    pods:
      metric:
        name: flink_taskmanager_job_task_backPressuredTimeMsPerSecond
      target:
        type: AverageValue
        averageValue: "200"
```

### 4.3 Rate Limiting

```java
// Source rate limiting
env.setBufferTimeout(100);  // Reduce buffer timeout to propagate backpressure faster
```

---

## 5. References
