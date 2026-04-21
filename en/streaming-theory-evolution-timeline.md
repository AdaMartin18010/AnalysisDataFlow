# Streaming Theory Evolution Timeline

> **Stage**: Struct/06-frontier | **Prerequisites**: [Expressiveness Hierarchy](expressiveness-hierarchy.md) | **Formalization Level**: L3
> **Translation Date**: 2026-04-21

## Abstract

This document traces the evolution of streaming theory from the 1960s to present, covering Petri nets, KPN, CSP, Actor model, CCS, π-calculus, Dataflow model, and streaming databases.

---

## 1. Definitions

### Def-S-06-01 (Streaming Theory Evolution)

The **evolution of streaming theory** is the theoretical lineage around data stream processing, spanning concurrency models, process calculi, distributed systems, and practical engines.

### Def-S-06-02 (Kahn Process Networks — KPN)

Gilles Kahn (1974): Networks of sequential processes connected by **unbounded FIFO channels**. Processes interact via blocking `read` and `write`. Semantics defined by **fixed points** on Scott domains.

### Def-S-06-03 (Communicating Sequential Processes — CSP)

C.A.R. Hoare (1978): Concurrent programming formalism with **synchronous communication** (rendezvous). Core operators: `!` (output), `?` (input), `□` (external choice). Foundation for OCCAM, Go.

### Def-S-06-04 (Petri Nets)

Carl Adam Petri (1962): $N = (P, T, F, M_0)$ where $P$ = places, $T$ = transitions, $F$ = flow relation, $M_0$ = initial marking. Models **concurrency, conflict, and synchronization**.

### Def-S-06-05 (Dataflow Computing)

1970s-1980s: Data availability drives execution. Static dataflow (Dennis, 1974) uses dataflow graphs with **token** passing. Dynamic dataflow (Arvind, 1977) adds **tagged tokens** for conditionals and loops.

### Def-S-06-06 (Actor Model)

Carl Hewitt (1973), Agha formalized (1985): Actors have **state**, **behavior**, and **mailbox**. Communication via **asynchronous message passing**. System: $\langle A, M, \to \rangle$.

### Def-S-06-07 (Calculus of Communicating Systems — CCS)

Robin Milner (1980): Process calculus with action prefix, parallel composition, choice, and restriction. **Bisimulation** (1989) as process equivalence standard.

### Def-S-06-08 (π-Calculus)

Milner, Parrow, Walker (1992): **Mobile process calculus**. Channels can be passed as messages, enabling dynamic topology. Core syntax: $P ::= 0 \mid \alpha.P \mid P+P \mid P|P \mid (\nu x)P \mid !P$.

### Def-S-06-09 (Dataflow Model)

Akidau et al. (2015, VLDB): Programming model with:

- **What**: window and trigger-based computation
- **Where**: event-time window assignment
- **When**: watermark-driven triggering
- **How**: accumulation modes

### Def-S-06-10 (Streaming Database)

2020s: Unified stream processing and storage. Systems: Materialize, RisingWave, Timeplus, Arroyo. Formally: continuous query evaluator $Q: \text{Stream}(T) \to \text{Stream}(U)$.

---

## 2. Properties

### Prop-S-06-01 (KPN Determinism)

KPN is **deterministic**: given the same input history, the network always produces the same output history, independent of scheduling.

**Proof sketch**: Continuous functions on CPOs have unique least fixed points. ∎

### Prop-S-06-02 (Actor No-Shared-State Implies Locality)

No shared state implies behavior depends only on message sequence and internal state, yielding natural **fault isolation** and **location transparency**.

### Prop-S-06-03 (π-Calculus Turing Completeness)

π-calculus is Turing-complete (encodes λ-calculus). **Dynamic reconfiguration** via name passing distinguishes it from CCS.

---

## 3. Theory Genealogy

| Decade | Theory | Core Contribution | Successor Influence |
|--------|--------|-------------------|---------------------|
| 1960s | Petri Nets | Concurrent modeling formalism | Token mechanisms in dataflow |
| 1970s | KPN | Deterministic dataflow | Streaming semantics |
| 1978 | CSP | Synchronous communication | Go channels, Occam |
| 1980 | CCS | Process equivalence | π-calculus |
| 1985 | Actor Model | Async messaging | Akka, Erlang |
| 1992 | π-Calculus | Mobile processes | Session types |
| 2015 | Dataflow Model | Unified batch/stream | Flink, Beam |
| 2020s | Streaming DB | Stream + storage unified | RisingWave, Materialize |

---

## 4. References
