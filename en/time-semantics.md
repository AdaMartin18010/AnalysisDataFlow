# Time Semantics in Stream Processing

> **Stage**: Knowledge/01-concept-atlas | **Prerequisites**: [Stream Processing Fundamentals](stream-processing-fundamentals.md) | **Formalization Level**: L3-L4
> **Translation Date**: 2026-04-21

## Abstract

Three time domains in stream processing: Event Time, Processing Time, and Ingestion Time — with formal definitions and trade-offs.

---

## 1. Definitions

### Def-K-02-01 (Time Domain)

$$\mathbb{T} = \{ \mathbb{T}_{event}, \mathbb{T}_{proc}, \mathbb{T}_{ingest} \}$$

### Def-K-02-02 (Event Time)

$$t_{event}: E \rightarrow \mathbb{T}_{event}, \quad t_{event}(e) = \text{timestamp when event occurred}$$

Objective and immutable.

### Def-K-02-03 (Processing Time)

$$t_{proc}: E \times Op \rightarrow \mathbb{T}_{proc}, \quad t_{proc}(e, op) = \text{when } e \text{ is processed by } op$$

Subjective and relative to execution environment clock.

### Def-K-02-04 (Ingestion Time)

$$t_{ingest}: E \rightarrow \mathbb{T}_{ingest}, \quad t_{ingest}(e) = \text{when } e \text{ arrives at Source}$$

Between event time and processing time.

### Def-K-02-05 (Total Latency)

$$\Delta t_{total}(e) = t_{proc}(e) - t_{event}(e)$$

---

## 2. Comparison

| Aspect | Event Time | Processing Time | Ingestion Time |
|--------|-----------|-----------------|----------------|
| Correctness | Deterministic | Non-deterministic | Partial |
| Latency | Higher | Lower | Medium |
| Complexity | Watermark needed | Simple | Moderate |
| Use Case | Analytics | Monitoring | Quick start |

---

## 3. Flink Example

```java
// Event time with watermark
stream.assignTimestampsAndWatermarks(
    WatermarkStrategy.<Event>forBoundedOutOfOrderness(
        Duration.ofSeconds(5))
);

// Processing time
stream.timeWindow(Time.seconds(10));  // Deprecated, use WindowAssigner
```

---

## 4. References
