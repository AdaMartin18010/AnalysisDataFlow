# Expressiveness Hierarchy Theorem

> **Stage**: Struct/03-relationships | **Prerequisites**: [Unified Streaming Theory](unified-streaming-theory.md), [Process Calculus](process-calculus-primer.md) | **Formalization Level**: L3-L6
> **Translation Date**: 2026-04-21

## Abstract

Six-layer expressiveness hierarchy for concurrent models, with strict separation theorems.

---

## 1. Definitions

### Def-S-14-01 (Expressiveness Preorder)

$$L_1 \leq L_2 \iff \exists \text{ encoding } [\![\cdot]\!]: L_1 \to L_2 \text{ preserving observables}$$

### Def-S-14-03 (Six-Layer Hierarchy)

| Layer | Model | Key Feature |
|-------|-------|-------------|
| $L_1$ | Finite Automata | No concurrency |
| $L_2$ | CSP (finite) | Static channels |
| $L_3$ | CCS | Labelled synchronization |
| $L_4$ | π-calculus | Channel passing |
| $L_5$ | Higher-order π | Process passing |
| $L_6$ | Turing-complete | General computation |

---

## 2. Key Relations

| Relation | Result |
|----------|--------|
| $L_1 \subset L_2 \subset L_3 \subset L_4 \subset L_5 \subset L_6$ | Strict inclusion chain |
| CSP $\subset$ π-calculus | Channel mobility adds power |
| Actor $\perp$ π-calculus | Incomparable |
| Synchronous π $\supset$ Async π | Strictly more expressive |

---

## 3. Key Theorem

### Thm-S-14-01 (Strict Expressiveness Hierarchy)

$$L_i \subset L_{i+1} \text{ for all } i \in \{1, \ldots, 5\}$$

Each layer strictly increases expressive power.

### Cor-S-14-01 (Decidability Decreases)

Higher layers have strictly fewer decidable properties.

---

## 4. References
