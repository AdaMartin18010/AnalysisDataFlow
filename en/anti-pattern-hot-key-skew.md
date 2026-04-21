# Anti-Pattern AP-04: Hot Key Skew

> **Stage**: Knowledge/09-anti-patterns | **Category**: Data Distribution | **Severity**: P1 | **Detection**: Hard
> **Translation Date**: 2026-04-21

## Abstract

Data skew causes some subtasks to be overloaded, creating processing bottlenecks where overall throughput is limited by the slowest subtask.

---

## 1. Definition

**Anti-Pattern**: Uneven key distribution where a small number of keys carry a disproportionate share of the data volume.

---

## 2. Symptoms

| Symptom | Indicator |
|---------|-----------|
| Web UI | Some subtasks show much higher backpressure |
| Metrics | `recordsInPerSecond` varies wildly across subtasks |
| State | Checkpoint size uneven across subtasks |

---

## 3. Solutions

### Two-Phase Aggregation

```java
// Phase 1: Local pre-aggregation with salted key
stream
    .map(e -> Tuple2.of(e.key + "_" + random.nextInt(SALT_COUNT), e.value))
    .keyBy(t -> t.f0)
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .aggregate(new PartialAggregate())
    // Phase 2: Global aggregation on original key
    .map(t -> Tuple2.of(t.f0.split("_")[0], t.f1))
    .keyBy(t -> t.f0)
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .aggregate(new FinalAggregate());
```

### Key Salting

Add random suffix to hot keys for initial distribution, then remove for final aggregation.

### Local Aggregation + Global Merge

Pre-aggregate at the source before shuffling.

---

## 4. References
