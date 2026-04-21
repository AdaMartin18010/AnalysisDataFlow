# Pattern: Windowed Aggregation

> **Stage**: Knowledge/02-design-patterns | **Prerequisites**: [Window Concepts](window-concepts.md) | **Formalization Level**: L4
> **Translation Date**: 2026-04-21

## Abstract

Windowed aggregation partitions unbounded streams into finite buckets for computation, bridging batch semantics and streaming execution.

---

## 1. Definitions

### Def-K-02-01 (Window Assigner)

A **window assigner** maps each element to one or more windows:

$$\text{Assign}: \text{Element} \to 2^{\text{Window}}$$

### Def-K-02-02 (Window Types)

| Type | Formula | Overlap |
|------|---------|---------|
| Tumbling | $[k\Delta, (k+1)\Delta)$ | None |
| Sliding | $[k\Delta_s, k\Delta_s + \Delta_w)$ | Yes |
| Session | $[t_{first}, t_{last} + g)$ | Dynamic |
| Global | $[0, \infty)$ | All data |

### Def-K-02-03 (Trigger)

A **trigger** determines when window results are emitted:

$$\text{Trigger}: \text{Window} \times \text{Watermark} \to \{\text{FIRE}, \text{CONTINUE}, \text{PURGE}\}$$

### Def-K-02-04 (Evictor)

An **evictor** removes elements from a window before/after processing.

---

## 2. Properties

### Prop-K-02-01 (Window Time Coverage Completeness)

Tumbling windows cover all time without gaps:

$$\bigcup_k [k\Delta, (k+1)\Delta) = [0, \infty)$$

### Prop-K-02-02 (Window Assignment Determinism)

Given the same element and window parameters, assignment is deterministic.

---

## 3. Flink Examples

### DataStream API

```java
stream
    .keyBy(Event::getKey)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .trigger(EventTimeTrigger.create())
    .aggregate(new AverageAggregate());
```

### SQL

```sql
SELECT 
    TUMBLE_START(event_time, INTERVAL '5' MINUTE) as window_start,
    key,
    AVG(value) as avg_value
FROM events
GROUP BY 
    TUMBLE(event_time, INTERVAL '5' MINUTE),
    key;
```

---

## 4. References

[^1]: Apache Flink Documentation, "Windows", 2025.
[^2]: T. Akidau et al., "The Dataflow Model", PVLDB, 2015.
