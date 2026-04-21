# Choreographic Deadlock Freedom

> **Stage**: Struct/04-proofs | **Prerequisites**: [Bisimulation](bisimulation-equivalences.md) | **Formalization Level**: L5
> **Translation Date**: 2026-04-21

## Abstract

Deadlock freedom for choreographic programs via Endpoint Projection (EPP) and global types.

---

## 1. Definitions

### Def-S-23-01 (Choreographic Programming)

Global specification of multi-party communication:

$$C ::= x \to y: T; C \mid \text{if } e \text{ then } C_1 \text{ else } C_2 \mid 0$$

### Def-S-23-03 (Endpoint Projection)

$$\llbracket C \rrbracket_p = \text{local behavior of role } p \text{ in choreography } C$$

### Def-S-23-04 (Deadlock Freedom)

$$\forall C \text{ well-typed}: \neg\exists \sigma: \sigma \text{ stuck and not terminated}$$

---

## 2. Key Theorem

### Thm-S-23-01 (Choreographic Deadlock Freedom)

Well-typed choreographies project to deadlock-free endpoint processes.

**Key Insight**: Global type discipline ensures all branches are matched.

---

## 3. References
