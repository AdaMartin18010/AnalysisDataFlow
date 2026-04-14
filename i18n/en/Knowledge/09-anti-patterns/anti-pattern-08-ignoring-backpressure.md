---
title: "Anti-Pattern AP-08: Ignoring Backpressure Signals"
translation_status: ai_translated_reviewed
source_version: v4.1
last_sync: "2026-04-15"
---

# Anti-Pattern AP-08: Ignoring Backpressure Signals

> **Anti-Pattern ID**: AP-08 | **Category**: Resource Management | **Severity**: P0 | **Detection Difficulty**: Extremely Hard
>
> Ignoring Flink's backpressure signals, continuously increasing input rates or refusing to scale out, leading to system cascading failures, data loss, or service unavailability.

---

## Table of Contents

- [Anti-Pattern AP-08: Ignoring Backpressure Signals](#anti-pattern-ap-08-ignoring-backpressure-signals)
  - [Table of Contents](#table-of-contents)
  - [1. Anti-Pattern Definition (Definition)](#1-anti-pattern-definition-definition)
  - [2. Symptoms (Symptoms)](#2-symptoms-symptoms)
  - [3. Negative Impacts (Negative Impacts)](#3-negative-impacts-negative-impacts)
    - [3.1 Cascading Failure](#31-cascading-failure)
  - [4. Solutions (Solution)](#4-solutions-solution)
    - [4.1 Monitor Backpressure Metrics](#41-monitor-backpressure-metrics)
    - [4.2 Auto-Scaling](#42-auto-scaling)
    - [4.3 Throttling and Degradation](#43-throttling-and-degradation)
  - [5. Code Examples (Code Examples)](#5-code-examples-code-examples)
    - [5.1 Incorrect Approach](#51-incorrect-approach)
    - [5.2 Correct Approach](#52-correct-approach)
  - [6. Example Verification (Examples)](#6-example-verification-examples)
    - [Case: System Crash During Peak Promotion](#case-system-crash-during-peak-promotion)
  - [7. Visualizations (Visualizations)](#7-visualizations-visualizations)
  - [8. References (References)](#8-references-references)

---

## 1. Anti-Pattern Definition (Definition)

**Definition (Def-K-09-08)**:

> Ignoring backpressure signals means that when a Flink job experiences backpressure, no mitigation measures are taken (scaling out, optimization, throttling), and instead input load is continuously increased or resource adjustments are refused, causing the system to evolve from local overload to global failure.

**Backpressure Propagation Mechanism** [^1]:

```
Downstream slow ──► Buffer full ──► Pause reading ──► Upstream buffer full ──► Propagates level by level
     │                                                                    │
     └── Backpressure signal ◄────────────────────────────────────────────┘
```

---

## 2. Symptoms (Symptoms)

| Symptom | Manifestation |
|---------|---------------|
| Backpressure spreads | Diffuses from downstream to upstream |
| Checkpoint timeout | Barriers cannot pass blocked operators |
| Latency spikes | Data queues in buffers |
| OOM | Buffers occupy heap memory |

---

## 3. Negative Impacts (Negative Impacts)

### 3.1 Cascading Failure

```
[Sink slow] ──► [Window blocked] ──► [Map blocked] ──► [Source blocked]
     │                                                  │
     ▼                                                  ▼
 Buffer full                                      Kafka Lag growth
     │                                                  │
     ▼                                                  ▼
 Checkpoint timeout                              Data expiration / loss
```

---

## 4. Solutions (Solution)

### 4.1 Monitor Backpressure Metrics

```scala
// Backpressure monitoring configuration
val env = StreamExecutionEnvironment.getExecutionEnvironment
env.getConfig.setAutoWatermarkInterval(200)

// Key metrics:
// - backPressuredTimeMsPerSecond
// - outputQueueLength
// - inputQueueLength
```

### 4.2 Auto-Scaling

```yaml
# Flink Kubernetes Operator autoscaling configuration
spec:
  podTemplate:
    spec:
      containers:
        - name: flink-main-container
          resources:
            limits:
              cpu: "4"
              memory: "8Gi"
  jobManager:
    resource:
      memory: "2Gi"
      cpu: 1
  taskManager:
    resource:
      memory: "4Gi"
      cpu: 2
    replicas: 2
  # Autoscaling policy
  autoScaler:
    enabled: true
    targetUtilization: 0.7
    scaleUpDelay: 5m
    scaleDownDelay: 10m
```

### 4.3 Throttling and Degradation

```scala
// Throttle at the Source
stream
  .map(event => {
    // Monitor processing latency; drop low-priority data if threshold exceeded
    if (latency > THRESHOLD && event.priority == LOW) {
      metrics.counter("dropped_events").inc()
      null
    } else {
      event
    }
  })
  .filter(_ != null)
```

---

## 5. Code Examples (Code Examples)

### 5.1 Incorrect Approach

```scala
// ❌ Incorrect: ignore backpressure and keep increasing load
while (true) {
  kafkaProducer.send(new ProducerRecord("topic", event))
  // Does not check Flink consumption speed
}
```

### 5.2 Correct Approach

```scala
// ✅ Correct: monitor Kafka Lag and slow down when backpressure occurs
val kafkaSource = KafkaSource.builder()
  .setProperty("max.poll.records", "100")
  .setProperty("fetch.max.wait.ms", "500")
  .build()

// Dynamically adjust consumption rate based on lag
if (lag > HIGH_THRESHOLD) {
  kafkaConsumer.pause()
} else if (lag < LOW_THRESHOLD) {
  kafkaConsumer.resume()
}
```

---

## 6. Example Verification (Examples)

### Case: System Crash During Peak Promotion

**Problem**:

- Traffic surged during promotion; backpressure signals were ignored
- Operations continued to push marketing data
- System cascading failure caused all jobs to restart

**Resolution**:

- Implement auto-scaling
- Configure Source throttling
- Establish backpressure alerting mechanisms

---

## 7. Visualizations (Visualizations)

```mermaid
graph LR
    A[Normal State] -->|Traffic increases| B[Mild Backpressure]
    B -->|Timely handled| A
    B -->|Ignored| C[Severe Backpressure]
    C -->|Timely handled| B
    C -->|Continued Ignorance| D[System Crash]

    style A fill:#c8e6c9,stroke:#2e7d32
    style B fill:#fff9c4,stroke:#f57f17
    style C fill:#ffcdd2,stroke:#c62828
    style D fill:#b71c1c,stroke:#b71c1c
```

---

## 8. References (References)

[^1]: Apache Flink Documentation, "Backpressure Monitoring," 2025.

---

*Document Version: v1.0 | Last Updated: 2026-04-03 | Status: Completed*
