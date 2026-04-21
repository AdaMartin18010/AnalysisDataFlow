# Flink Time Semantics and Watermark

> **Stage**: Flink/02-core | **Prerequisites**: [Deployment Architecture](../01-concepts/deployment-architectures.md) | **Formal Level**: L4
>
> Event Time vs Processing Time vs Ingestion Time, Watermark mechanism, generation strategies, and window types.

---

## 1. Definitions

**Def-F-02-87: Event Time**

Timestamp embedded in each record representing when the event occurred in the real world.

**Def-F-02-88: Processing Time**

Wall-clock time at the operator when processing the record.

**Def-F-02-89: Ingestion Time**

Time when the record enters the Flink source.

**Def-F-02-90: Watermark**

Progress marker indicating no records with timestamp earlier than $W$ are expected:

$$
\text{Watermark}(W) \implies \forall r \in \text{future}. \; \text{timestamp}(r) \geq W
$$

**Def-F-02-91: Allowed Lateness**

Maximum duration after window end during which late records are still accepted.

---

## 2. Properties

**Lemma-F-02-41: Watermark Monotonicity**

Watermarks are non-decreasing within each parallel subtask.

**Lemma-F-02-42: Window Assignment Completeness**

For tumbling windows of size $T$, every record belongs to exactly one window.

**Lemma-F-02-43: Lateness Upper Bound**

With `BoundedOutOfOrderness(maxDelay)`, maximum lateness is bounded by `maxDelay`.

---

## 3. Relations

- **with Dataflow Model**: Event Time + Watermark implements the Dataflow Model's temporal abstraction.
- **with Kahn Process Networks**: Watermark serves as progress indicator.

---

## 4. Argumentation

**Time Semantics Comparison**:

| Semantics | Determinism | Latency | Use Case |
|-----------|-------------|---------|----------|
| Event Time | ✓ | Higher | Analytics, billing |
| Processing Time | ✗ | Lower | Monitoring, alerts |
| Ingestion Time | Partial | Medium | Log processing |

**Watermark Strategies**:

| Strategy | Latency | Completeness | Use Case |
|----------|---------|--------------|----------|
| Fixed Delay | Higher | Guaranteed | Ordered logs |
| Punctuated | Lower | Source-dependent | Event-punctuated |
| Idle Timeout | Handles idle | Configurable | Multi-source joins |

---

## 5. Engineering Argument

**Thm-F-02-12 (Event Time Determinism)**: Given identical input records, Event Time processing produces deterministic results regardless of execution speed or cluster topology.

---

## 6. Examples

```java
// Watermark strategy with idle source handling
WatermarkStrategy<MyEvent> strategy = WatermarkStrategy
    .<MyEvent>forBoundedOutOfOrderness(Duration.ofSeconds(5))
    .withTimestampAssigner((event, ts) -> event.getEventTime())
    .withIdleness(Duration.ofMinutes(1));

stream.assignTimestampsAndWatermarks(strategy)
    .keyBy(MyEvent::getUserId)
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .aggregate(new CountAggregate());
```

---

## 7. Visualizations

**Watermark Propagation**:

```mermaid
graph LR
    S[Source<br/>W=12:00] -->|W=12:00| M[Map]
    M -->|min(W1,W2)| J[Join]
    S2[Source2<br/>W=11:58] -->|W=11:58| J
    J -->|W=11:58| Sink
```

---

## 8. References
