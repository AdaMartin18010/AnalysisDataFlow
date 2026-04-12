# Struct/ Formal Theory - English Navigation

> **Document Position**: Struct/ English Content Index | **Version**: 2026.04 | **Status**: Index Only

---

## Overview

The **Struct/** directory contains the most rigorous formal theoretical documents for stream computing, following the six-section template (Definitions → Properties → Relations → Argumentation → Proof → Examples → Visualizations → References).

**Note**: Currently, Struct/ documents are primarily in Chinese. This index provides navigation to key theoretical concepts with English summaries.

---

## Theoretical Foundations

### 01. Unified Streaming Theory (USTM)

| Concept | Chinese Document | English Summary |
|---------|-----------------|-----------------|
| USTM Meta-model | [01.01-unified-streaming-theory.md](../Struct/01-foundation/01.01-unified-streaming-theory.md) | Eight-tuple framework unifying Actor, CSP, Dataflow, and Petri net semantics |
| Process Calculus | [01.02-process-calculus-primer.md](../Struct/01-foundation/01.02-process-calculus-primer.md) | CCS, CSP, π-calculus, and Session Types fundamentals |
| Actor Model | [01.03-actor-model-formalization.md](../Struct/01-foundation/01.03-actor-model-formalization.md) | Formal Actor, Behavior, Mailbox, and Supervision Tree definitions |
| Dataflow Model | [01.04-dataflow-model-formalization.md](../Struct/01-foundation/01.04-dataflow-model-formalization.md) | Dataflow graphs, operator semantics, and time domains |

### 02. Property Derivations

| Property | Chinese Document | Description |
|----------|-----------------|-------------|
| Determinism | [02.01-determinism-in-streaming.md](../Struct/02-properties/02.01-determinism-in-streaming.md) | Confluence reduction and observable determinism |
| Consistency Hierarchy | [02.02-consistency-hierarchy.md](../Struct/02-properties/02.02-consistency-hierarchy.md) | At-Most-Once/At-Least-Once/Exactly-Once semantics |
| Watermark Monotonicity | [02.03-watermark-monotonicity.md](../Struct/02-properties/02.03-watermark-monotonicity.md) | Lattice structure and monotonicity preservation |
| Liveness & Safety | [02.04-liveness-and-safety.md](../Struct/02-properties/02.04-liveness-and-safety.md) | Trace properties and Alpern-Schneider decomposition |

### 03. Cross-Model Relationships

| Relationship | Chinese Document | Key Concepts |
|--------------|-----------------|--------------|
| Actor→CSP Encoding | [03.01-actor-to-csp-encoding.md](../Struct/03-relationships/03.01-actor-to-csp-encoding.md) | Encoding function `[[·]]_A→C`, mailbox buffer processes |
| Flink→Process Calculus | [03.02-flink-to-process-calculus.md](../Struct/03-relationships/03.02-flink-to-process-calculus.md) | Operator-to-process encoding, checkpoint synchronization |
| Expressiveness Hierarchy | [03.03-expressiveness-hierarchy.md](../Struct/03-relationships/03.03-expressiveness-hierarchy.md) | Six-level hierarchy (L1-L6) with strictness proofs |

### 04. Formal Proofs

| Theorem | Chinese Document | Statement |
|---------|-----------------|-----------|
| Checkpoint Correctness | [04.01-flink-checkpoint-correctness.md](../Struct/04-proofs/04.01-flink-checkpoint-correctness.md) | Barrier propagation invariants and state consistency |
| Exactly-Once Correctness | [04.02-flink-exactly-once-correctness.md](../Struct/04-proofs/04.02-flink-exactly-once-correctness.md) | End-to-end consistency with 2PC formalization |
| Chandy-Lamport Consistency | [04.03-chandy-lamport-consistency.md](../Struct/04-proofs/04.03-chandy-lamport-consistency.md) | Consistent cut lemma and marker propagation |

---

## Key Theorems (English Summary)

### Thm-S-01-01: USTM Completeness

**Statement**: The Unified Streaming Theory Meta-model (USTM) provides a complete formal framework for describing stream computing systems across six expressiveness levels.

**Key Components**:

- $(\mathcal{L}, \mathcal{M}, \mathcal{P}, \mathcal{C}, \mathcal{S}, \mathcal{T}, \Sigma, \Phi)$
- Six expressiveness levels from L1 (descriptive) to L6 (mechanized verification)

### Thm-S-02-01: Determinism Preservation

**Statement**: A stream processing system is deterministic if and only if all operators are pure functions and channel ordering is preserved.

**Conditions**:

1. Pure function operators: $f: \mathcal{D}_{in} \rightarrow \mathcal{D}_{out}$
2. FIFO channel semantics
3. No external side effects

### Thm-S-04-01: Checkpoint Correctness

**Statement**: Flink's checkpoint mechanism guarantees consistent global snapshots with no orphan messages.

**Proof Structure**:

1. Barrier alignment invariants
2. State consistency at alignment points
3. Exactly-once processing guarantee

---

## Formalization Levels

| Level | Name | Description | Verification |
|-------|------|-------------|--------------|
| L1 | Conceptual | Informal/semi-formal descriptions | Expert review |
| L2 | Structured | Mathematical definitions with notation | Syntax checking |
| L3 | Operational | Structured Operational Semantics (SOS) | Interpreter validation |
| L4 | Denotational | Domain theory/algebraic semantics | Model checking |
| L5 | Formal Proof | Theorem-proof structures | Theorem provers |
| L6 | Mechanized | Type theory, Coq/Lean proofs | Computer verification |

---

## Cross-References

### Chinese Documentation

- [Struct/ Full Index](../Struct/00-INDEX.md) - Complete Chinese navigation
- [THEOREM-REGISTRY.md](../THEOREM-REGISTRY.md) - All formal elements registry

### English Documentation

- [Knowledge/ Index](./KNOWLEDGE-INDEX.md) - Engineering practice navigation
- [Flink/ Index](./FLINK-INDEX.md) - Flink-specific technology navigation

---

## Contributing

To contribute English translations of Struct/ documents:

1. Follow the six-section template
2. Maintain theorem numbering consistency (Thm-S-XX-XX)
3. Include both formal definitions and intuitive explanations
4. Add Mermaid diagrams for visualizations

See [I18N-ROADMAP.md](../I18N-ROADMAP.md) for translation priorities.

---

## Key Terms (English-Chinese)

| English | Chinese | Formal Symbol |
|---------|---------|---------------|
| Unified Streaming Theory Meta-model | 统一流计算元模型 | USTM |
| Process Calculus | 进程演算 | - |
| Actor Model | Actor模型 | - |
| Dataflow Model | Dataflow模型 | - |
| Checkpoint | 检查点 | - |
| Watermark | 水印 | $wm: \text{Stream} \to \mathbb{T}$ |
| Exactly-Once | 精确一次 | - |
| Determinism | 确定性 | - |
| Bisimulation | 互模拟 | $\sim$ |

---

*Last updated: 2026-04-12 | For full Chinese content, see [../Struct/00-INDEX.md](../Struct/00-INDEX.md)*
