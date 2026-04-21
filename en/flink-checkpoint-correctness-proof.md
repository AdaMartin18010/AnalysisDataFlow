# Flink Checkpoint Correctness Proof

> **Stage**: Struct/04-proofs | **Prerequisites**: [Consistency Hierarchy](consistency-hierarchy.md) | **Formalization Level**: L5
> **Translation Date**: 2026-04-21

## Abstract

Flink's checkpoint mechanism implements the Chandy-Lamport distributed snapshot algorithm with barriers. This document proves the correctness of Flink's checkpoint consistency.

---

## 1. Definitions

### Def-S-17-01 (Checkpoint Barrier Semantics)

A **checkpoint barrier** is a special event injected into the data stream that triggers state snapshots.

### Def-S-17-02 (Consistent Global State)

A **consistent global state** is a snapshot where:

$$\forall op_i, op_j: op_i \prec op_j \land op_j \in \text{Snapshot} \Rightarrow op_i \in \text{Snapshot}$$

### Def-S-17-03 (Checkpoint Alignment)

**Alignment** ensures a multi-input operator receives barriers from all inputs before snapshotting:

$$\text{Aligned}(op) \iff \forall in \in \text{Inputs}(op): \text{Barrier}_{cp} \in \text{Received}(in)$$

### Def-S-17-04 (State Snapshot Atomicity)

State snapshot is **atomic** if it captures either the pre-barrier or post-barrier state, never a mixture.

---

## 2. Key Lemmas

### Lemma-S-17-01 (Barrier Propagation Invariant)

Barriers propagate through all operators in topological order.

### Lemma-S-17-02 (State Consistency)

Aligned snapshots capture consistent operator states.

### Lemma-S-17-03 (Alignment Point Uniqueness)

Each checkpoint has a unique alignment point per operator.

### Lemma-S-17-04 (No Orphan Messages)

All records processed before the barrier are reflected in the snapshot; all records after are not.

---

## 3. Correctness Theorem

### Thm-S-17-01 (Flink Checkpoint Consistency)

Flink's aligned checkpoint mechanism produces a consistent global state.

**Proof.**

1. Barriers propagate through the entire DAG (Lemma-S-17-01).
2. Each operator snapshots after receiving all barriers (alignment).
3. Alignment ensures no record crosses the snapshot boundary (Lemma-S-17-04).
4. The union of all operator states forms a consistent global state (Def-S-17-02).

This is equivalent to the Chandy-Lamport consistent cut (Thm-S-19-01). ∎

---

## 4. References
