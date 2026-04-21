# Anti-Pattern AP-07: Window State Explosion

> **Stage**: Knowledge/09-anti-patterns | **Prerequisites**: [Window Concepts](window-concepts.md) | **Formalization Level**: L3
> **Translation Date**: 2026-04-21

## Abstract

Storing all raw events in window operators without incremental aggregation causes unbounded state growth, leading to OOM or checkpoint timeouts.

---

## 1. Definition

### Def-K-09-07 (Window State Explosion)

**Window state explosion** occurs when `ProcessWindowFunction` stores all raw events instead of using `AggregateFunction` for incremental aggregation.

**State growth model**:

```
State Size = #Windows × Events/Window × Event Size

Incorrect:
- 1-min window × 1M events/min × 1KB = 1GB/window

Correct:
- 1-min window × 1 accumulator × 100B = 100B/window

Optimization ratio: 1GB / 100B = 10,000,000x!
```

---

## 2. Solution

### 2.1 Use AggregateFunction

```java
// Incremental aggregation
DataStream<Result> aggregated = stream
    .keyBy(Event::getKey)
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .aggregate(new AverageAggregate());  // O(1) state per window
```

### 2.2 Combine Aggregate + ProcessWindow

```java
// Pre-aggregate then process
DataStream<Result> result = stream
    .keyBy(Event::getKey)
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .aggregate(new SumAggregate())
    .process(new PostProcessFunction());  // Only receives aggregated value
```

### 2.3 Use Evictor

```java
// Limit events per window
stream
    .windowAll(TumblingEventTimeWindows.of(Time.minutes(1)))
    .evictor(CountEvictor.of(1000));  // Keep only 1000 events
```

---

## 3. References
