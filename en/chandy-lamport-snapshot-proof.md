# Chandy-Lamport Snapshot Consistency Proof

> **Stage**: Struct/04-proofs | **Prerequisites**: [Checkpoint Correctness](flink-checkpoint-correctness-proof.md) | **Formalization Level**: L5
> **Translation Date**: 2026-04-21

## Abstract

Formal proof that the Chandy-Lamport distributed snapshot algorithm records a consistent global state.

---

## 1. Definitions

### Def-S-19-01 (Global State)

$$G = (S_1, S_2, \ldots, S_n, C_{12}, C_{21}, \ldots)$$

- $S_i$: Local state of process $i$
- $C_{ij}$: State of channel from $i$ to $j$

### Def-S-19-02 (Consistent Cut)

A cut $C$ is consistent if:

$$\forall e \in C: \text{pred}(e) \in C$$

If an event is in the cut, all its causal predecessors are also in the cut.

### Def-S-19-04 (Marker Message)

A special control message $M$ that triggers state recording without affecting application logic.

---

## 2. Properties

### Lemma-S-19-01 (Marker Propagation Invariant)

Once a process records its state upon receiving a marker, it forwards the marker on all outgoing channels.

### Lemma-S-19-02 (Consistent Cut Lemma)

The set of events recorded before receiving a marker forms a consistent cut.

---

## 3. Key Theorem

### Thm-S-19-01 (Chandy-Lamport Records Consistent Global State)

The Chandy-Lamport algorithm produces a consistent global state snapshot.

**Proof Sketch**:

1. Marker FIFO property ensures causal ordering
2. Each process snapshots before forwarding → no missed events
3. Channel recording rule captures in-flight messages
4. Union of local snapshots forms consistent cut

---

## 4. Relationship to Flink

| Chandy-Lamport | Flink Checkpoint |
|----------------|------------------|
| Marker | Checkpoint Barrier |
| Local snapshot | Operator state snapshot |
| Channel state | In-flight data buffer |
| Consistent cut | Aligned checkpoint |

---

## 5. References
