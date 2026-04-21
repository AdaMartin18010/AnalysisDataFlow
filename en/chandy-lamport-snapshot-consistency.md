# Chandy-Lamport Snapshot Consistency Proof

> **Stage**: Struct/04-proofs | **Prerequisites**: [Flink Checkpoint Correctness](flink-checkpoint-correctness.md) | **Formalization Level**: L5
> **Translation Date**: 2026-04-21

## Abstract

The Chandy-Lamport algorithm records a consistent global state of a distributed system using marker messages. This document formalizes the proof of consistency.

---

## 1. Definitions

### Def-S-19-01 (Global State)

A **global state** $GS$ is the union of all local states and channel states:

$$GS = \left( \bigcup_{p \in P} LS_p \right) \cup \left( \bigcup_{c \in C} CS_c \right)$$

### Def-S-19-02 (Consistent Cut)

A **consistent cut** is a partition of events into past and future such that:

$$\forall e_1, e_2: e_1 \to e_2 \land e_2 \in \text{Past} \Rightarrow e_1 \in \text{Past}$$

(No future event causally influences a past event)

### Def-S-19-03 (Channel State)

**Channel state** $CS_c$ records all messages in transit on channel $c$:

$$CS_c = \{ m \mid \text{send}(m) \in \text{Past} \land \text{receive}(m) \notin \text{Past} \}$$

### Def-S-19-04 (Marker Message)

A **marker** is a special control message that triggers snapshot recording at each process.

### Def-S-19-05 (Local Snapshot)

**Local snapshot** $LS_p$ records process $p$'s state upon first marker receipt.

---

## 2. Key Lemmas

### Lemma-S-19-01 (Marker Propagation Invariant)

Markers propagate along all channels, ensuring every process receives a marker.

### Lemma-S-19-02 (Consistent Cut Lemma)

The set of local snapshot events forms a consistent cut.

**Proof.** By construction: a process records its state upon first marker receipt. All events before the marker are in the past; all events after are in the future. Since channels are FIFO, no message sent after the marker can be received before it. ∎

### Lemma-S-19-03 (Channel State Completeness)

Channel state records all and only messages in transit at the cut.

### Lemma-S-19-04 (No Orphan Messages)

No message is recorded as both sent and not received unless it is genuinely in transit.

---

## 3. Correctness Theorem

### Thm-S-19-01 (Chandy-Lamport Records Consistent Global State)

The Chandy-Lamport algorithm produces a consistent global state.

**Proof.**

1. Marker propagation ensures all processes participate (Lemma-S-19-01).
2. Local snapshots form a consistent cut (Lemma-S-19-02).
3. Channel states capture exactly the in-transit messages (Lemma-S-19-03).
4. No orphan messages exist (Lemma-S-19-04).

Thus, the recorded state is a valid global state consistent with a consistent cut. ∎

---

## 4. References
