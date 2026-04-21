# Streaming Database Formalization

> **Stage**: Struct/01-foundation | **Prerequisites**: [Dataflow Model](dataflow-model-formalization.md) | **Formalization Level**: L5
> **Translation Date**: 2026-04-21

## Abstract

Formal model of streaming databases: materialized views, incremental maintenance, and consistency levels.

---

## 1. Definitions

### Def-S-01-80 (Streaming Database Core Model)

$$SDB = (S, Q, V, \Delta, \Sigma, \tau, \prec)$$

- $S$: input streams
- $Q$: query workload
- $V$: materialized views
- $\Delta$: incremental update operator
- $\Sigma$: consistency specification
- $\tau$: transaction manager
- $\prec$: happens-before relation

### Def-S-01-81 (Materialized View)

$$V_q(t) = \{ r \mid r \in q(S_{\leq t}) \}$$

The snapshot of query $q$ over all events up to time $t$.

---

## 2. Consistency Levels

| Level | Definition | System Example |
|-------|-----------|----------------|
| Strict Serializability | All transactions appear to execute in some serial order | Traditional RDBMS |
| Snapshot Isolation | Reads from consistent snapshot, no write-write conflicts | PostgreSQL |
| Read Committed | Only committed data visible | MySQL (default) |

---

## 3. Key Theorem

### Thm-S-01-80 (Streaming Database Consistency Equivalence)

Under deterministic operators and replayable sources, materialized view consistency is equivalent to stream processing exactly-once semantics.

---

## 4. References
