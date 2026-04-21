# Iris Separation Logic Extensions for Stream Processing

> **Language**: English | **Source**: [Knowledge/06-frontier/iris-separation-logic-streaming-extension.md](../Knowledge/06-frontier/iris-separation-logic-streaming-extension.md) | **Last Updated**: 2026-04-21

---

## 1. Definitions

### Def-K-06-EN-325: Streaming State Resource

Traditional Iris separation logic describes **point-in-time state** (e.g., $l \mapsto v$). Stream processing requires extension to **time-evolving state sequences**.

**Definition**: A streaming state resource is a time-indexed family of resources:

$$
\mathcal{R}_{stream} = \{ R_t \in \text{iProp} \}_{t \in \mathcal{T}}
$$

where $\mathcal{T}$ is the event time domain, $R_t$ is the Iris resource assertion at time $t$.

**Temporal separation conjunction** $\bigotimes$:

$$
\frac{\forall t_i \in \mathcal{T}.\ \vdash R_{t_i} : \text{iProp} \quad \forall t_i \neq t_j.\ \text{dom}(R_{t_i}) \cap \text{dom}(R_{t_j}) = \emptyset}{\vdash \bigotimes_{t_i \in \mathcal{T}} R_{t_i} : \text{StreamResource}}
$$

### Def-K-06-EN-326: Stream Operator Hoare Triple

$$
\{ \mathcal{R}_{in} \}\ \text{Op}\ \{ \mathcal{R}_{out} \}
$$

where $\mathcal{R}_{in}$ and $\mathcal{R}_{out}$ are streaming state resources at input and output.

### Def-K-06-EN-328: Checkpoint Resource Contract

A checkpoint establishes a resource invariant:

$$
\text{Checkpoint}(id) \triangleq \exists S.\ \text{StateSnapshot}(S, id) \ast \text{Recoverable}(S, id)
$$

## 2. Properties

### Lemma-K-06-EN-321: Streaming Frame Rule

If an operator satisfies its Hoare triple, adding disjoint temporal resources preserves correctness:

$$
\frac{\{ R \}\ Op\ \{ R' \} \quad \text{dom}(F) \cap \text{dom}(R) = \emptyset}{\{ R \ast F \}\ Op\ \{ R' \ast F \}}
$$

### Thm-K-06-EN-321: Operator Composition Safety

For operators $Op_1$ and $Op_2$ with compatible interfaces:

$$
\frac{\{ R_0 \}\ Op_1\ \{ R_1 \} \quad \{ R_1 \}\ Op_2\ \{ R_2 \}}{\{ R_0 \}\ Op_1; Op_2\ \{ R_2 \}}
$$

### Prop-K-06-EN-322: Temporal Resource Monotonicity

Stream resources are monotonic with respect to watermark advancement:

$$
t_1 \leq t_2 \Rightarrow \mathcal{R}_{t_1} \sqsubseteq \mathcal{R}_{t_2}
$$

## 3. Mapping to Flink Concepts

| Iris Concept | Flink Equivalent |
|-------------|------------------|
| $R_t$ (time-indexed resource) | Operator state at epoch $t$ |
| $\bigotimes$ (temporal sep-conj) | Union of state across epochs |
| $\text{Checkpoint}(id)$ | Consistent snapshot handle |
| $\text{Recoverable}(S, id)$ | State backend restore capability |
| Watermark $w$ | Lower bound on valid $t$ for $R_t$ |

## 4. Example: Tumbling Window Verification

```
{ StreamResource(events, [t_0, t_1)) }
TumblingWindow(size = T)
{ WindowContent(events, [t_0, t_0+T)) ⊗ StreamResource(events, [t_0+T, t_1)) }
```

**Proof sketch**:
1. Temporal separation ensures events in $[t_0, t_0+T)$ are independent of $[t_0+T, t_1)$
2. Frame rule allows window aggregation without affecting downstream resources
3. Checkpoint at $t_0+T$ captures $\text{WindowContent} \ast \text{EmptyStream}$ invariant

## References

[^1]: Jung et al., "Iris: Monoids and Invariants as an Orthogonal Basis for Concurrent Reasoning", POPL 2015.
[^2]: Krebbers et al., "The Essence of Higher-Order Concurrent Separation Logic", ESOP 2017.
[^3]: Apache Flink Documentation, "Checkpointing", 2025.
