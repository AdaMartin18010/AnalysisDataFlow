# Stream Processing Semantics Formalization

> **Stage**: Struct/01-foundation | **Prerequisites**: [Dataflow Model](dataflow-model-formalization.md) | **Formalization Level**: L5-L6
> **Translation Date**: 2026-04-21

## Abstract

Formal semantics of streams as infinite sequences with event time and processing time dimensions.

---

## 1. Definitions

### Def-S-01-50 (Stream as Infinite Sequence)

$$\mathcal{S}: \mathbb{N} \to \mathcal{D} \times \mathcal{T} \times \mathcal{T}$$

Event $e_i = (d_i, t_i^{(e)}, t_i^{(p)})$:

- $d_i$: data payload
- $t_i^{(e)}$: event time
- $t_i^{(p)}$: processing time

### Def-S-01-51 (Time Domain Structure)

$(\mathcal{T}, \leq, +, 0)$ is a totally ordered commutative monoid:

1. **Totality**: $(\mathcal{T}, \leq)$ is totally ordered
2. **Monotonicity**: $\tau_1 \leq \tau_2 \Rightarrow \tau_1 + \delta \leq \tau_2 + \delta$
3. **Identity**: $\exists 0: \tau + 0 = \tau$

---

## 2. Event-Time Ordering

**In-order stream**:

$$\forall i, j: i \leq j \Rightarrow t_i^{(e)} \leq t_j^{(e)}$$

**Out-of-order stream**: $\exists i < j: t_i^{(e)} > t_j^{(e)}$

---

## 3. References
