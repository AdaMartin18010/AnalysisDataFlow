# Watermark Algebra Formal Proof

> **Stage**: Struct/04-proofs | **Prerequisites**: [Watermark Monotonicity](watermark-monotonicity-theorem.md) | **Formalization Level**: L5
> **Translation Date**: 2026-04-21

## Abstract

Watermark values form a complete lattice under merge (⊔) and partial order (⊑).

---

## 1. Definitions

### Def-S-20-01 (Watermark Lattice Element)

Watermark $w \in \mathbb{W} = \mathbb{T} \cup \{\bot, \top\}$

### Def-S-20-02 (Merge Operator)

$$w_1 \sqcup w_2 = \min(w_1, w_2)$$

### Def-S-20-03 (Partial Order)

$$w_1 \sqsubseteq w_2 \iff w_1 \geq w_2$$

(Larger watermark means more progress)

---

## 2. Lattice Properties

| Property | Statement |
|----------|-----------|
| Associativity | $(w_1 \sqcup w_2) \sqcup w_3 = w_1 \sqcup (w_2 \sqcup w_3)$ |
| Commutativity | $w_1 \sqcup w_2 = w_2 \sqcup w_1$ |
| Idempotence | $w \sqcup w = w$ |
| Identity | $w \sqcup \top = w$ |

---

## 3. Key Theorem

### Thm-S-20-01 (Watermark Complete Lattice)

$(\mathbb{W}, \sqsubseteq, \sqcup, \sqcap, \bot, \top)$ is a complete lattice.

**Implication**: Watermark propagation is well-defined for arbitrary DAG topologies.

---

## 4. References
