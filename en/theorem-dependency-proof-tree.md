# Theorem Dependency Network and Proof Tree

> **Stage**: Struct/03-relationships | **Prerequisites**: [Three-Layer Relationship](three-layer-relationship.md) | **Formalization Level**: L5-L6
> **Translation Date**: 2026-04-21

## Abstract

Complete dependency graph of all formal elements (theorems, lemmas, propositions) and inference decision tree.

---

## 1. Definitions

### Def-S-17-01 (Theorem Dependency Graph)

$$\mathcal{G}_{dep} = (V_{Thm}, E_{dep})$$

- $V_{Thm}$: all theorems, lemmas, propositions
- $E_{dep}$: dependency edges where $(t_1, t_2)$ means $t_2$'s proof depends on $t_1$

### Def-S-17-02 (Inference Decision Tree)

$$\mathcal{T}_{inf}: \text{rooted tree where leaves are decidable conclusions}$$

---

## 2. Properties

### Prop-S-17-01 (Dependency Graph Acyclicity)

Well-formed dependency graphs are acyclic:

$$\mathcal{G}_{dep} \text{ well-formed} \Rightarrow \nexists \text{ cycle in } \mathcal{G}_{dep}$$

**Proof**: A cycle $t_1 \to \ldots \to t_n \to t_1$ implies $t_1$ depends on itself, violating well-foundedness.

### Prop-S-17-02 (Bounded Dependency Depth)

Maximum dependency depth in this project: $d_{max} \leq 6$.

---

## 3. References
