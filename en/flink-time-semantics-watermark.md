# Flink Time Semantics and Watermark

> **Stage**: Flink/02-core | **Prerequisites**: [Deployment Architecture](../01-concepts/deployment-architectures.md) | **Formal Level**: L4
>
> Comprehensive guide to Flink time semantics: Event Time vs Processing Time vs Ingestion Time, Watermark mechanism, generation strategies, window types, and late data handling.

---

## 1. Definitions

**Def-F-02-07: Event Time**

The timestamp embedded in each data record, representing when the event actually occurred in the real world.

**Def-F-02-08: Processing Time**

The wall-clock time at the operator when the record is being processed. Lowest latency but non-deterministic across runs.

**Def-F-02-09: Watermark**

A metadata marker indicating that no records with timestamp earlier than $T$ are expected to arrive[^1]:

$$
\text{Watermark}(t) \implies \forall r \in \text{future}. \; \text{timestamp}(r) \geq t
$$

**Def-F-02-10: Allowed Lateness**

The maximum duration after window end during which late records are still accepted and may update previously emitted results.

---

## 2. Properties

**Lemma-F-02-04: Watermark Monotonicity**

Watermarks must be non-decreasing within each parallel subtask:

$$
\forall i. \; W_i(t_1) \leq W_i(t_2) \text{ for } t_1 < t_2
$$

**Lemma-F-02-05: Lateness Upper Bound**

With watermark strategy `BoundedOutOfOrderness(maxDelay)`, the maximum lateness for any record is bounded by `maxDelay`.

---

## 3. Relations

- **with Dataflow Model**: Event Time + Watermark directly implements the Dataflow Model's temporal abstraction.
- **with Kahn Process Networks**: Watermark serves as a progress indicator analogous to KPN termination detection.

---

## 4. Argumentation

**Watermark Generation Strategies**:

| Strategy | Latency | Completeness | Use Case |
|----------|---------|--------------|----------|
| Fixed Delay | Higher | Guaranteed | Ordered logs |
| Punctuated | Lower | Source-dependent | Event-punctuated streams |
| Idle Timeout | Handles idle sources | Configurable | Multi-source joins |

---

## 5. Engineering Argument

**Thm-F-02-01 (Event Time Determinism)**: Given identical input records, Event Time processing with watermarks produces deterministic results regardless of processing speed or cluster topology.

*Proof Sketch*: Window triggers depend only on Event Time timestamps and watermark progression, both independent of execution environment. ∎

---

## 6. Examples

```java
// Watermark strategy
WatermarkStrategy<MyEvent> strategy = WatermarkStrategy
    .<MyEvent>forBoundedOutOfOrderness(Duration.ofSeconds(5))
    .withTimestampAssigner((event, ts) -> event.getEventTime());

stream.assignTimestampsAndWatermarks(strategy)
    .keyBy(MyEvent::getUserId)
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .aggregate(new CountAggregate());
```

---

## 7. Visualizations

**Watermark Propagation in DAG**:

```mermaid
graph LR
    S[Source<br/>W=12:00] -->|W=12:00| M[Map]
    M -->|min(W1,W2)| J[Join]
    S2[Source2<br/>W=11:58] -->|W=11:58| J
    J -->|W=11:58| Sink
```

---

## 8. References

[^1]: T. Akidau et al., "The Dataflow Model", PVLDB, 8(12), 2015.
