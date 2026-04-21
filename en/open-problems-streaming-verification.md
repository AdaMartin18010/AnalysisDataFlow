# Open Problems in Streaming Verification

> **Stage**: Struct/06-frontier | **Prerequisites**: [Checkpoint Correctness](flink-checkpoint-correctness-proof.md) | **Formalization Level**: L4-L6
> **Translation Date**: 2026-04-21

## Abstract

Six major open problems at the frontier of stream processing formal verification.

---

## 1. Open Problems

### OP-1: Dynamic Topology Real-Time Verification

Can we verify stream processing correctness when operators are added/removed at runtime?

**Challenge**: State space depends on topology; dynamic changes require re-verification.

### OP-2: End-to-End Exactly-Once Automated Proof

Automate the proof that a given Flink job satisfies exactly-once end-to-end.

**Challenge**: Requires modeling source, engine, and sink semantics simultaneously.

### OP-3: Watermark Progress Formal Reasoning

Prove that watermark progress guarantees eventual output completeness.

**Challenge**: Watermark depends on input data distribution.

### OP-4: Compositional Stateful Operator Verification

Verify composed operators by verifying each in isolation.

**Challenge**: State sharing and feedback loops break compositionality.

### OP-5: Heterogeneous System Interoperability

Verify correctness when multiple stream processors interact.

**Challenge**: Different semantics, time models, and consistency guarantees.

### OP-6: ML + Streaming Hybrid Verification

Verify pipelines that combine stream processing with ML inference.

**Challenge**: ML models are probabilistic and hard to formally specify.

---

## 2. Key Insight

$$\text{Expressiveness} \uparrow \Rightarrow \text{Verifiability} \downarrow$$

The trade-off between expressive power and formal verifiability is fundamental.

---

## 3. References
