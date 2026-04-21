# Flink-to-Process Calculus Encoding

> **Stage**: Struct/03-relationships | **Prerequisites**: [Dataflow Model](dataflow-model-formalization.md), [Process Calculus](process-calculus-primer.md) | **Formalization Level**: L5
> **Translation Date**: 2026-04-21

## Abstract

Formal encoding from Flink Dataflow graphs to π-calculus process networks with exactly-once preservation.

---

## 1. Definitions

### Def-S-13-01 (Operator to π-Calculus Process)

Flink operator $Op$ maps to π-calculus process $P_{Op}$:

$$\llbracket Op \rrbracket_\pi = (\nu c_{in})(\nu c_{out})(\text{Operator}(c_{in}, c_{out}) \mid \text{StateManager})$$

### Def-S-13-02 (Dataflow Edge to Channel)

Dataflow edge $e: Op_1 \to Op_2$ maps to π-calculus channel:

$$\llbracket e \rrbracket_\pi = c_e : \text{Channel}(\text{Type}(e))$$

### Def-S-13-03 (Checkpoint Barrier Protocol)

Barrier synchronization encoded as:

$$\text{Barrier}_n = \bar{b}\langle n \rangle.\text{wait}(\text{ack}_n).\text{snapshot}$$

---

## 2. Properties

### Lemma-S-13-01 (Local Determinism Preservation)

Deterministic operators encode to deterministic π-processes.

### Lemma-S-13-02 (Barrier Alignment Guarantees Snapshot Consistency)

All barriers received $\Rightarrow$ consistent global snapshot.

---

## 3. Key Theorem

### Thm-S-13-01 (Exactly-Once Preservation)

Flink Dataflow with aligned checkpointing encodes to π-calculus with exactly-once semantics.

---

## 4. References
