# Concurrency Paradigm Selection Guide

> **Stage**: Knowledge/04-technology-selection | **Prerequisites**: [Concurrency Paradigms Matrix](concurrency-paradigms-matrix.md) | **Formalization Level**: L3-L6
> **Translation Date**: 2026-04-21

## Abstract

This guide compares five core concurrency paradigms—Actor, CSP, Dataflow, Shared Memory, and STM—providing a decision framework for system design.

---

## 1. Definitions

### Def-K-04-01 (Concurrency Paradigm)

A **concurrency paradigm** defines how parallel computations interact and synchronize.

### Def-K-04-02 (Selection Decision Space)

The decision space spans five paradigms:

| Paradigm | Communication | State | Best For |
|----------|--------------|-------|----------|
| Actor | Async messages | Local | Distributed systems, fault tolerance |
| CSP | Synchronous channels | Local | Pipeline parallelism, Go |
| Dataflow | Token passing | Implicit | Stream processing, DAG execution |
| Shared Memory | Direct access | Shared | Multi-threading, low latency |
| STM | Transactions | Shared | Concurrent data structures |

---

## 2. Properties

### Lemma-K-04-01 (Expressiveness Hierarchy Mapping)

| Paradigm | Expressiveness Level | Decidable Properties |
|----------|---------------------|---------------------|
| Dataflow | L4 | Limited |
| Actor | L3 | Safety (bounded) |
| CSP | L2 | Deadlock, determinism |
| Shared Memory | L5+ | None (general) |
| STM | L4 | Limited |

### Lemma-K-04-02 (Paradigm Composition Boundary)

Actor + CSP can be composed via mailbox-as-channel encoding.
Shared Memory + STM cannot be composed safely without hardware support.

---

## 3. Decision Tree

```
Is the system distributed across nodes?
├── YES → Need fault isolation?
│         ├── YES → Actor
│         └── NO  → CSP
└── NO  → Is it stream processing?
          ├── YES → Dataflow
          └── NO  → Need atomic transactions?
                    ├── YES → STM
                    └── NO  → Shared Memory
```

---

## 4. References
