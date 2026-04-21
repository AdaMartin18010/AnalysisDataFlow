# Comprehensive Relation Index: 5D Relation Network Overview

> **Stage**: Struct/03-relationships | **Prerequisites**: [Three-Layer Relationship](three-layer-relationship-comprehensive.md), [Theorem Dependency Tree](theorem-dependency-proof-tree.md) | **Formalization Level**: L3-L5
> **Translation Date**: 2026-04-21

## Abstract

This document provides a 5-dimensional relation model for navigating the knowledge base: vertical, horizontal, hierarchical, dependency, and cross-cutting dimensions.

---

## 1. Definitions

### Def-S-19-01 (5-Dimensional Relation Model)

The knowledge base relation network consists of five dimensions:

1. **Vertical**: Struct → Knowledge → Flink hierarchical mapping
2. **Horizontal**: Equivalence, encoding, and inclusion relations within the same layer
3. **Hierarchical**: Abstraction levels within models (syntax → semantics → implementation)
4. **Dependency**: Proof dependency network among theorems, lemmas, and definitions
5. **Cross-Cutting**: Theme associations spanning multiple layers (consistency, fault tolerance, performance)

### Def-S-19-02 (Relation Strength)

**Relation strength** $\rho(r) \in [0, 1]$ quantifies the tightness between two entities:

- $\rho = 1.0$: Formal equivalence (e.g., bisimulation equivalence)
- $\rho \in [0.7, 1.0)$: Encoding preservation (e.g., Actor→CSP encoding)
- $\rho \in [0.4, 0.7)$: Semantic approximation (e.g., Dataflow→Flink implementation)
- $\rho \in [0, 0.4)$: Conceptual association (e.g., heuristic inspiration)

---

## 2. Properties

### Prop-S-19-01 (Relation Network Connectivity)

The knowledge base relation network is weakly connected:

$$\forall e_i, e_j \in \mathcal{E}, \exists \text{ path } p: e_i \leadsto e_j$$

### Prop-S-19-02 (Relation Transitivity)

For encoding/mapping relations, transitivity holds:

$$e_1 \xrightarrow{\Phi_1} e_2 \land e_2 \xrightarrow{\Phi_2} e_3 \implies e_1 \xrightarrow{\Phi_2 \circ \Phi_1} e_3$$

---

## 3. Vertical Dimension Mapping

| Source (High-level) | Target (Low-level) | Mapping | Document |
|--------------------|-------------------|---------|----------|
| Actor Model | Async I/O Pattern | Behavior instantiation | pattern-async-io-enrichment |
| Dataflow Model | Flink Runtime | Implementation mapping | flink-system-architecture |
| Session Types | Stream Processing Pipeline | Protocol modeling | session-types |
| CALM Theorem | Flink Checkpoint | Coordination analysis | checkpoint-mechanism |

---

## 4. Horizontal Dimension Relations

| Relation | Entities | Strength | Type |
|----------|----------|----------|------|
| Equivalence | Erlang Actor ≈ Akka Actor | 0.95 | Bisimulation |
| Encoding | Actor → π-calculus | 0.85 | Structural |
| Inclusion | SDF ⊂ DDF | 1.0 | Subset |
| Approximation | Dataflow → Flink | 0.65 | Implementation |

---

## 5. References

[^1]: Project Internal, "Relation Index", 2026.
