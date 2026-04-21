# Flink Checkpoint Correctness Proof

> **Stage**: Struct/04-proofs | **Prerequisites**: [Consistency Hierarchy](consistency-hierarchy.md) | **Formalization Level**: L5
> **Translation Date**: 2026-04-21

## Abstract

Formal proof that Flink's aligned checkpoint mechanism produces consistent global snapshots.

---

## 1. Definitions

### Def-S-17-01 (Checkpoint Barrier Semantics)

Barrier $B_n$ marks logical time $n$ for snapshotting.

### Def-S-17-03 (Checkpoint Alignment)

All barriers for checkpoint $n$ received before processing subsequent events.

### Def-S-17-04 (State Snapshot Atomicity)

$$\text{snapshot}(S) = S_{before} \text{ or } S_{after}, \text{ never intermediate}$$

---

## 2. Key Lemmas

### Lemma-S-17-01 (Barrier Propagation Invariant)

Barriers propagate through the DAG in topological order.

### Lemma-S-17-03 (Alignment Point Uniqueness)

For each checkpoint $n$, there is exactly one alignment point per operator.

---

## 3. Key Theorem

### Thm-S-17-01 (Flink Checkpoint Consistency)

Flink's aligned checkpoint mechanism records a consistent global state.

**Proof Sketch**:

1. Source injects barrier → causal closure
2. Barriers propagate topologically → all operators see barrier
3. Alignment ensures no straggler events
4. Snapshot union is a consistent cut

---

## 4. References
