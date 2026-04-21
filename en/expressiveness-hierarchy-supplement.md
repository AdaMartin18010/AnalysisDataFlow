# Expressiveness Hierarchy Supplement

> **Stage**: Struct/03-relationships | **Prerequisites**: [Expressiveness Hierarchy](expressiveness-hierarchy.md) | **Formalization Level**: L3-L5
> **Translation Date**: 2026-04-21

## Abstract

Extended models beyond the six-layer hierarchy: Session Types, CRDTs, Choreographic Programming, TLA+, and Separation Logic.

---

## 1. Definitions

### Def-S-15-01 (Session Types)

Type discipline for structured communication protocols.

### Def-S-15-03 (CRDTs)

Conflict-free Replicated Data Types with monotonic merge:

$$\forall x, y: x \sqcup y = y \sqcup x \land x \sqsubseteq x \sqcup y$$

### Def-S-15-04 (TLA+)

Temporal Logic of Actions for specifying and verifying concurrent systems.

---

## 2. Key Theorems

### Thm-S-15-01 (Session Types Deadlock Freedom)

Well-typed session processes are deadlock-free.

### Thm-S-15-02 (CRDT Strong Eventual Consistency)

CRDTs guarantee convergence without coordination:

$$\forall r_i, r_j: \text{delivered}(r_i) \land \text{delivered}(r_j) \Rightarrow \text{state}_i = \text{state}_j$$

---

## 3. Verification Methods vs Models

| Model | Verification Method | Orthogonal? |
|-------|---------------------|-------------|
| π-calculus | Session Types | Yes |
| Actor | TLA+ | Yes |
| Dataflow | Separation Logic | Yes |
| CRDT | Model Checking | Yes |

---

## 4. References
