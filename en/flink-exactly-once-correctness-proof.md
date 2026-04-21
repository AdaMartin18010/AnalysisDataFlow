# Flink Exactly-Once Correctness Proof

> **Stage**: Struct/04-proofs | **Prerequisites**: [Checkpoint Correctness](flink-checkpoint-correctness-proof.md) | **Formalization Level**: L5
> **Translation Date**: 2026-04-21

## Abstract

Proof that Flink's exactly-once semantics hold end-to-end: no lost records, no duplicates.

---

## 1. Definitions

### Def-S-18-01 (Exactly-Once Observable Effect)

$$\forall e \in I: \quad |\{ o \in O \mid o \text{ derived from } e \land \text{committed}(o) \}| = 1$$

### Def-S-18-03 (Two-Phase Commit)

1. **Prepare**: Sink pre-commits output
2. **Commit**: On checkpoint success, finalize
3. **Abort**: On checkpoint failure, rollback

---

## 2. Key Lemmas

### Lemma-S-18-01 (Source Replayability)

Replayable sources guarantee at-least-once:

$$\exists \text{replay}: \text{Offset} \to I_{\geq \text{offset}}$$

### Lemma-S-18-02 (2PC Atomicity)

Commit is atomic with respect to checkpoint.

---

## 3. Main Theorem

### Thm-S-18-01 (Flink Exactly-Once Correctness)

**Proof** (3 steps):

1. **At-Least-Once**: Replayable source + checkpoint recovery
2. **At-Most-Once**: 2PC atomic commit + deterministic operators
3. **Exactly-Once**: At-Least-Once ∧ At-Most-Once

---

## 4. References
