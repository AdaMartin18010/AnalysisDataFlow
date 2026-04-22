# Consistency Hierarchy in Stream Processing

> **Stage**: Struct/02-properties | **Prerequisites**: [Dataflow Model](dataflow-model-formalization.md) | **Formalization Level**: L5
> **Translation Date**: 2026-04-21

## Abstract

Formal hierarchy of consistency guarantees in streaming systems from At-Most-Once to Exactly-Once, with end-to-end correctness conditions.

---

## 1. Definitions

### Def-S-08-02 (At-Most-Once)

$$\forall e \in I: \quad |\{ o \in O \mid o \text{ derived from } e \}| \leq 1$$

May lose, never duplicate.

### Def-S-08-03 (At-Least-Once)

$$\forall e \in I: \quad |\{ o \in O \mid o \text{ derived from } e \}| \geq 1$$

Never lose, may duplicate.

### Def-S-08-04 (Exactly-Once)

$$\forall e \in I: \quad |\{ o \in O \mid o \text{ derived from } e \}| = 1$$

Neither lose nor duplicate.

### Def-S-08-05 (End-to-End Exactly-Once)

Requires: Replayable Source + Engine Exactly-Once + Transactional Sink.

---

## 2. Properties

### Lemma-S-08-01 (Exactly-Once ⟹ At-Least-Once)

$$|O_e| = 1 \Rightarrow |O_e| \geq 1$$

### Lemma-S-08-02 (Exactly-Once ⟹ At-Most-Once)

$$|O_e| = 1 \Rightarrow |O_e| \leq 1$$

### Lemma-S-08-04 (Strong ⟹ Causal)

Strong consistency implies causal consistency.

### Lemma-S-08-05 (Causal ⟹ Eventual)

Causal consistency implies eventual consistency.

---

## 3. Consistency Lattice

```
        Strong Consistency
              |
        Causal Consistency
              |
       Eventual Consistency
```

---

## 4. Key Theorems

### Thm-S-08-03 (Unified Consistency Implication Chain)

$$\text{Exactly-Once} \Rightarrow \text{At-Least-Once} \land \text{At-Most-Once}$$
$$\text{Strong} \Rightarrow \text{Causal} \Rightarrow \text{Eventual}$$

---

## 5. References
