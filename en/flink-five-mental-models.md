# Flink: Five Mental Models for Stream Processing

> **Stage**: Flink/01-concepts | **Prerequisites**: [Unified Streaming Theory](unified-streaming-theory.md) | **Formalization Level**: L3-L4
> **Translation Date**: 2026-04-21

## Abstract

Five fundamental mental models that expert Flink practitioners use to reason about stream processing systems.

---

## 1. Mental Model 1: Stream-First Data View

> Treat all data as streams. Batch is a special case of streaming (bounded stream).

**Formalization**:

- Bounded stream: $\exists t_{end}: \forall e \in S, t_e(e) < t_{end}$
- Unbounded stream: $\neg\exists t_{end}: \forall e \in S, t_e(e) < t_{end}$

**Controversy**: Lambda (batch + stream separately) vs Kappa (stream-only). The debate has largely resolved in favor of unified streaming.

---

## 2. Mental Model 2: Event Time Semantics

> Use event time for correctness, processing time for simplicity.

$$\text{Event Time}: t_e(e) = \text{timestamp when event occurred}$$
$$\text{Processing Time}: t_p(e) = \text{timestamp when event is processed}$$

| Aspect | Event Time | Processing Time |
|--------|-----------|-----------------|
| Correctness | Deterministic results | Non-deterministic |
| Latency | Higher (waits for watermark) | Lower |
| Complexity | Needs watermark strategy | Simple |

---

## 3. Mental Model 3: Windowing Operator

> Windows partition unbounded streams into finite buckets.

| Type | Formula | Use Case |
|------|---------|----------|
| Tumbling | $[k\Delta, (k+1)\Delta)$ | Fixed-period aggregates |
| Sliding | $[k\Delta_s, k\Delta_s + \Delta_w)$ | Moving averages |
| Session | $[t_{first}, t_{last} + g)$ | User behavior analysis |

---

## 4. Mental Model 4: Keyed State

> Partitioned state enables scalable stateful computation.

$$\text{State}_k = \{ s \in \text{State} \mid \text{key}(s) = k \}$$

**State types**: ValueState, ListState, MapState, ReducingState, AggregatingState.

---

## 5. Mental Model 5: Exactly-Once Fault Tolerance

> Chandy-Lamport snapshots + barrier alignment = exactly-once semantics.

**Thm-F-01-04**: Chandy-Lamport distributed snapshots are correct under Flink's barrier alignment mechanism.

---

## 6. References
