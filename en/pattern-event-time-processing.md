# Pattern: Event Time Processing

> **Stage**: Knowledge/02-design-patterns | **Prerequisites**: [Time Semantics](time-semantics.md) | **Formalization Level**: L4-L5
> **Translation Date**: 2026-04-21

## Abstract

This pattern addresses out-of-order data, late data, and result determinism in distributed stream processing through Watermark-based progress tracking.

---

## 1. Definitions

### Def-K-02-01 (Event Time)

**Event time** $t_e(e)$ is the timestamp when the event occurred in the physical world.

### Def-K-02-02 (Watermark)

A **watermark** $w(t)$ is a progress metric in event time:

$$w(t) = \min_{s \in \text{Sources}} \left( \max_{r \in R_s(t)} t_e(r) - \delta_s \right)$$

### Def-K-02-03 (Late Data)

**Late data** arrives after the watermark has passed its event time:

$$\text{Late}(e) \iff t_e(e) < w(t_{\text{arrival}})$$

---

## 2. Properties

### Prop-K-02-01 (Watermark Monotonicity Propagation)

Watermarks propagate monotonically through the DAG.

### Prop-K-02-02 (Late Data Processing Semantics)

Late data can be:
- **Dropped**: Discarded (default)
- **Allowed**: Processed if within allowed lateness
- **Side-output**: Routed to separate stream

---

## 3. Flink Implementation

```java
// Watermark strategy with allowed lateness
DataStream<Event> withTimestamps = stream
    .assignTimestampsAndWatermarks(
        WatermarkStrategy
            .<Event>forBoundedOutOfOrderness(Duration.ofSeconds(5))
            .withIdleness(Duration.ofMinutes(1))
    );

// Window with late data handling
withTimestamps
    .keyBy(Event::getKey)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .allowedLateness(Time.minutes(2))
    .sideOutputLateData(lateDataTag)
    .aggregate(new CountAggregate());
```

---

## 4. References

[^1]: T. Akidau et al., "The Dataflow Model", PVLDB, 2015.
[^2]: Apache Flink Documentation, "Event Time", 2025.
