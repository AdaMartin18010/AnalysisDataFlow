# Watermark Monotonicity Theorem

> **Stage**: Struct/02-properties | **Prerequisites**: [Dataflow Model Formalization](dataflow-model-formalization.md) | **Formalization Level**: L5
> **Translation Date**: 2026-04-21

## Abstract

The **Watermark Monotonicity Theorem** establishes that watermarks in a Dataflow graph propagate monotonically (non-decreasing) across all operators, provided certain structural conditions hold. This theorem is foundational for event-time correctness in stream processing systems.

---

## 1. Definitions

### Def-S-09-01 (Event Time)

Let $\text{Record}$ be the set of all possible records in a stream, and $\mathbb{T} = \mathbb{R}_{\geq 0}$ the time domain. **Event time** is a mapping from records to the time domain:

$$t_e: \text{Record} \to \mathbb{T}$$

For a record $r \in \text{Record}$, $t_e(r)$ denotes the timestamp when the event occurred in the physical world.

### Def-S-09-02 (Watermark)

A **watermark** $w$ at an operator $v$ at processing time $t$ is defined as:

$$w_v(t) = \min_{s \in \text{Src}(v)} \left( \max_{r \in R_s(t)} t_e(r) - \delta_s \right)$$

where:
- $\text{Src}(v)$ is the set of source operators upstream of $v$
- $R_s(t)$ is the set of records observed by source $s$ up to time $t$
- $\delta_s \geq 0$ is the fixed maximum out-of-orderness tolerance for source $s$

A watermark serves as a **progress indicator** for event time: all events with timestamp less than $w_v(t)$ are considered "on time" (already observed or permanently late).

---

## 2. Properties

### Lemma-S-09-01 (Minimum Preservation Monotonicity)

For any finite non-empty set of monotone non-decreasing functions $\{f_1, f_2, \ldots, f_n\}$ with $f_i: \mathbb{T} \to \mathbb{T}$, the pointwise minimum $g(t) = \min_{1 \leq i \leq n} f_i(t)$ is also monotone non-decreasing.

**Proof.** Let $t_1 \leq t_2$. For each $i$, $f_i(t_1) \leq f_i(t_2)$ by monotonicity of $f_i$. Thus:

$$g(t_1) = \min_i f_i(t_1) \leq \min_i f_i(t_2) = g(t_2)$$

∎

---

## 3. Relations

### Relation 1: Watermark Monotonicity and Dataflow Model Formalization

Watermark monotonicity directly connects to the Dataflow model's notion of event-time progress. The Dataflow model guarantees that windows complete when the watermark passes their end boundary—this guarantee relies on watermark monotonicity.

### Relation 2: Watermark Monotonicity and Kahn Process Networks

In Kahn Process Networks (KPN), the partial order of message delivery ensures determinism. Watermark monotonicity generalizes this partial order to event time: it imposes a causal ordering on **temporal observations** rather than just message delivery.

### Relation 3: Watermark Monotonicity and Checkpoint Consistency

Exactly-once checkpointing requires consistent snapshots across operators. Watermark monotonicity ensures that checkpoint barriers align with temporal progress, preventing temporal inconsistencies in recovery.

---

## 4. Argumentation

### 4.1 Inductive Framework Based on Stream Prefix Partial Order

Watermark monotonicity can be proved by structural induction over the operator DAG:

1. **Base case**: Source operators generate watermarks from observed record timestamps.
2. **Inductive step**: Each operator preserves monotonicity by construction (min/max operations).

### 4.2 Idle Sources and Watermark Progress

When a source becomes idle (no new records), watermark progress stalls. This is the intended behavior—the watermark cannot advance without new observations. Systems like Flink implement **idle source timeouts** to allow watermark progress despite idle partitions.

### 4.3 Counterexample: Non-Monotonic Watermark

Consider a misconfigured system where an operator reassigns event timestamps based on wall-clock time. If clock adjustments occur (e.g., NTP corrections), the resulting "watermark" may decrease, violating monotonicity. This leads to:
- Window re-firing with incorrect results
- Late data being classified as "on time"
- Inconsistent exactly-once semantics

---

## 5. Formal Proof

### Thm-S-09-01 (Watermark Monotonicity Theorem)

For any operator $v$ in a Dataflow graph $G = (V, E)$, the output watermark $w_v(t)$ is monotone non-decreasing in processing time $t$:

$$\forall t_1, t_2 \in \mathbb{T}: t_1 \leq t_2 \Rightarrow w_v(t_1) \leq w_v(t_2)$$

provided that:
1. Source watermarks are computed from maximum observed event times.
2. Single-input operators propagate $\min$ or preserve the input watermark.
3. Multi-input operators compute the minimum across all input watermarks.
4. The system does not retroactively modify historical event timestamps.

**Proof by structural induction over operator DAG.**

**Step 1 (Base Case — Source Operators).**

For any source $s \in V_{\text{src}}$, the watermark is:

$$w_s(t) = \max_{r \in R_s(t)} t_e(r) - \delta_s$$

For $t_1 \leq t_2$, we have $R_s(t_1) \subseteq R_s(t_2)$, so:

$$\max_{r \in R_s(t_1)} t_e(r) \leq \max_{r \in R_s(t_2)} t_e(r)$$

Subtracting $\delta_s$ preserves the inequality, establishing $w_s(t_1) \leq w_s(t_2)$.

**Step 2 (Inductive Hypothesis).**

Assume for the first $k-1$ operators in topological order that each output watermark is monotone non-decreasing.

**Step 3 (Inductive Step).**

Consider the $k$-th operator $v_k$.

- **Case A (Single-input operators)**: Map, Filter, FlatMap.
  
  These operators output a watermark $w_{\text{out}}(t) = w_{\text{in}}(t)$ or a non-decreasing function thereof. By the inductive hypothesis, $w_{\text{in}}$ is monotone; thus $w_{\text{out}}$ is monotone.

- **Case B (Multi-input operators)**: Join, Union, CoGroup.
  
  These compute $w_{\text{out}}(t) = \min_{i} w_i(t)$ across input watermarks. By Lemma-S-09-01, the minimum of monotone non-decreasing functions is monotone non-decreasing. ∎

### Corollaries

1. **Window Trigger Correctness**: If window $[a, b)$ triggers when $w_v(t) \geq b$, then once triggered, the window will never "un-trigger."

2. **Late Data Bound**: Any record with $t_e(r) < w_v(t)$ arriving after time $t$ is definitively late (no future watermark decrease can reclassify it as on-time).

3. **Exactly-Once Alignment**: Checkpoint barriers align with watermark progress, ensuring consistent snapshot boundaries in event time.

---

## 6. Examples

### Example 6.1: Three-Operator DAG

Consider a DAG: `Source → Map → WindowAgg`.

| Time | Source WM | Map WM | WindowAgg WM |
|------|-----------|--------|--------------|
| t=1  | 10        | 10     | 10           |
| t=2  | 15        | 15     | 15           |
| t=3  | 18        | 18     | 18           |

All watermarks advance monotonically at the same rate (assuming no additional delay).

### Example 6.2: Counterexample — Non-Monotonic Watermark

If a buggy operator computes watermark as average instead of minimum:

| Time | Input WM 1 | Input WM 2 | Avg WM |
|------|------------|------------|--------|
| t=1  | 10         | 20         | 15     |
| t=2  | 25         | 12         | 18.5   |

If Input WM 2 decreases (due to a bug), the average decreases from 15 to 18.5 → actually still increases here. A true counterexample requires WM decrease: if at t=3, inputs are 25 and 5 (bug), average = 15, which **decreases** from 18.5. This demonstrates why `min` is required for monotonicity.

---

## 7. Visualizations

```mermaid
graph TD
    A[Source S1] -->|w₁(t)| C[Join Operator]
    B[Source S2] -->|w₂(t)| C
    C -->|w_out(t) = min(w₁, w₂)| D[Downstream]
    
    style A fill:#e1f5fe
    style B fill:#e1f5fe
    style C fill:#fff3e0
    style D fill:#e8f5e9
```

**Watermark propagation in a multi-input operator.** The output watermark is the minimum of all input watermarks, preserving monotonicity.

---

## 8. References

[^1]: T. Akidau et al., "The Dataflow Model", PVLDB, 8(12), 2015.
[^2]: Apache Flink Documentation, "Event Time and Watermarks", 2025. https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/
[^3]: L. Lamport, "Time, Clocks, and the Ordering of Events in a Distributed System", CACM, 21(7), 1978.
