# Struct/ Formal Theory Document Index

> **Document Positioning**: Struct directory navigation index | **Formalization Level**: L1-L6 full coverage | **Version**: 2026.04-v2.0

---

## Statistics Overview

| Metric | Count | Update |
|--------|-------|--------|
| **Total Documents** | 53+ | +3 new docs |
| **Theorems (Thm)** | 385+ | +5 new theorems |
| **Definitions (Def)** | 858+ | +8 new definitions |
| **Lemmas/Propositions** | 1705+ | +5 new lemmas |
| **Formalization Coverage** | L1-L6 | Complete |

---

## Directory Structure

### 01-foundation/ Fundamental Theory (11 docs) [v4.4 updated]

| Document | Description | Level |
|----------|-------------|-------|
| [01.01-unified-streaming-theory-en.md](01-foundation/01.01-unified-streaming-theory-en.md) | USTM Unified Meta-Model | L6 |
| [01.02-process-calculus-primer-en.md](01-foundation/01.02-process-calculus-primer-en.md) | Process Calculus Fundamentals | L3-L4 |
| [01.03-actor-model-formalization-en.md](01-foundation/01.03-actor-model-formalization-en.md) | Actor Model Formalization | L4-L5 |
| [01.04-dataflow-model-formalization-en.md](01-foundation/01.04-dataflow-model-formalization-en.md) | Dataflow Model Formalization | L5 |
| [01.05-csp-formalization-en.md](01-foundation/01.05-csp-formalization-en.md) | CSP Formalization | L3 |
| [01.06-petri-net-formalization-en.md](01-foundation/01.06-petri-net-formalization-en.md) | Petri Net Formalization | L2-L4 |
| [01.07-session-types-en.md](01-foundation/01.07-session-types-en.md) | Session Types | L4-L5 |
| [01.08-streaming-database-formalization-en.md](01-foundation/01.08-streaming-database-formalization-en.md) | Streaming Database Formalization | L4 |
| [01.09-edge-streaming-semantics-en.md](01-foundation/01.09-edge-streaming-semantics-en.md) | Edge Streaming Semantics | L4 |
| [01.10-network-calculus-en.md](01-foundation/network-calculus/network-calculus-streaming-en.md) | Network Calculus | L4-L5 | 🆕 |
| [01.11-dbsp-differential-dataflow-en.md](01-foundation/01.11-dbsp-differential-dataflow-en.md) | DBSP/Differential Dataflow Theory | L5-L6 | 🆕 v4.4 |

### 02-properties/ Property Derivation (9 docs) [100%]

| Document | Description | Level |
|----------|-------------|-------|
| [02.01-determinism-in-streaming-en.md](02-properties/02.01-determinism-in-streaming-en.md) | Streaming Determinism | L5 |
| [02.02-consistency-hierarchy-en.md](02-properties/02.02-consistency-hierarchy-en.md) | Consistency Hierarchy | L5 |
| [02.03-watermark-monotonicity-en.md](02-properties/02.03-watermark-monotonicity-en.md) | Watermark Monotonicity | L5 |
| [02.04-liveness-and-safety-en.md](02-properties/02.04-liveness-and-safety-en.md) | Liveness and Safety | L4-L5 |
| [02.05-type-safety-derivation-en.md](02-properties/02.05-type-safety-derivation-en.md) | Type Safety Derivation | L5 |
| [02.06-calm-theorem-en.md](02-properties/02.06-calm-theorem-en.md) | CALM Theorem | L5 |
| [02.07-encrypted-stream-processing-en.md](02-properties/02.07-encrypted-stream-processing-en.md) | Encrypted Stream Processing | L5 |
| [02.08-differential-privacy-streaming-en.md](02-properties/02.08-differential-privacy-streaming-en.md) | Differential Privacy | L5 |

### 03-relationships/ Relationship Establishment (6 docs) [100%]

| Document | Description | Level |
|----------|-------------|-------|
| [03.01-actor-to-csp-encoding-en.md](03-relationships/03.01-actor-to-csp-encoding-en.md) | Actor→CSP Encoding | L4-L5 |
| [03.02-flink-to-process-calculus-en.md](03-relationships/03.02-flink-to-process-calculus-en.md) | Flink→Process Calculus | L5 |
| [03.03-expressiveness-hierarchy-en.md](03-relationships/03.03-expressiveness-hierarchy-en.md) | Expressiveness Hierarchy | L3-L6 |
| [03.04-bisimulation-equivalences-en.md](03-relationships/03.04-bisimulation-equivalences-en.md) | Bisimulation Equivalences | L3-L4 |
| [03.05-cross-model-mappings-en.md](03-relationships/03.05-cross-model-mappings-en.md) | Cross-Model Mappings | L5-L6 |
| [03.06-flink-distributed-architecture-en.md](03-relationships/03.06-flink-distributed-architecture-en.md) | Flink Distributed Architecture | L4 |

### 04-proofs/ Formal Proofs (8 docs) [100%]

| Document | Description | Level |
|----------|-------------|-------|
| [04.01-flink-checkpoint-correctness-en.md](04-proofs/04.01-flink-checkpoint-correctness-en.md) | Checkpoint Correctness | L5 |
| [04.02-flink-exactly-once-correctness-en.md](04-proofs/04.02-flink-exactly-once-correctness-en.md) | Exactly-Once Correctness | L5 |
| [04.03-chandy-lamport-consistency-en.md](04-proofs/04.03-chandy-lamport-consistency-en.md) | Chandy-Lamport Consistency | L5 |
| [04.04-watermark-algebra-formal-proof-en.md](04-proofs/04.04-watermark-algebra-formal-proof-en.md) | Watermark Algebra Proof | L5 |
| [04.05-type-safety-fg-fgg-en.md](04-proofs/04.05-type-safety-fg-fgg-en.md) | FG/FGG Type Safety | L5-L6 |
| [04.06-dot-subtyping-completeness-en.md](04-proofs/04.06-dot-subtyping-completeness-en.md) | DOT Subtyping Completeness | L5-L6 |
| [04.07-deadlock-freedom-choreographic-en.md](04-proofs/04.07-deadlock-freedom-choreographic-en.md) | Choreographic Deadlock Freedom | L5 |

### 05-comparative-analysis/ Comparative Analysis (5 docs) [100%]

| Document | Description | Level |
|----------|-------------|-------|
| [05.01-go-vs-scala-expressiveness-en.md](05-comparative-analysis/05.01-go-vs-scala-expressiveness-en.md) | Go vs Scala | L4-L5 |
| [05.02-expressiveness-vs-decidability-en.md](05-comparative-analysis/05.02-expressiveness-vs-decidability-en.md) | Expressiveness vs Decidability | L5 |
| [05.03-encoding-completeness-analysis-en.md](05-comparative-analysis/05.03-encoding-completeness-analysis-en.md) | Encoding Completeness | L4-L5 |
| [05.04-concurrency-models-2025-comparison-en.md](05-comparative-analysis/05.04-concurrency-models-2025-comparison-en.md) | Concurrency Models 2025 | L5 |

---

*Document Version: v1.0 | Created: 2026-04-20*
