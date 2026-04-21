# Watermark Monotonicity Theorem

> **Stage**: Struct/02-properties | **Prerequisites**: [Dataflow Model](dataflow-model-formalization.md) | **Formalization Level**: L5
> **Translation Date**: 2026-04-21

## Abstract

Watermark values are monotonically non-decreasing throughout the Dataflow DAG, providing a formal guarantee of progress.

---

## 1. Definitions

### Def-S-09-01 (Event Time)

$$t_e: \text{Record} \to \mathbb{T}, \quad \mathbb{T} = \mathbb{R}_{\geq 0}$$

### Def-S-09-02 (Watermark)

For source $s$:

$$w_s(t) = \max_{r \in R_s(t)} t_e(r) - \delta_s$$

Where $\delta_s \geq 0$ is the maximum out-of-orderness tolerance.

---

## 2. Theorem

### Thm-S-09-01 (Watermark Monotonicity)

For any operator $v$ in a Dataflow DAG:

$$t_1 < t_2 \Rightarrow w_v(t_1) \leq w_v(t_2)$$

**Proof Sketch**:
1. **Base case**: Source watermark $w_s(t)$ is monotonic by definition (max over growing set)
2. **Inductive step**: 
   - Single-input operators preserve monotonicity
   - Multi-input operators: $w_{out} = \min(w_{in_1}, w_{in_2}, \ldots)$ — min of monotonic functions is monotonic
3. By topological induction, all operators preserve monotonicity

---

## 3. Corollaries

- Window triggers fire at most once per watermark value
- Late data is deterministically identified
- Progress can be measured globally

---

## 4. References

[^1]: T. Akidau et al., "The Dataflow Model", PVLDB, 2015.
[^2]: Apache Flink Documentation, "Watermarks", 2025.
