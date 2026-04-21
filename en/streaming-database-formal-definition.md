# Streaming Database Formal Definition

> **Stage**: Struct/01-foundation | **Prerequisites**: [Streaming DB Formalization](streaming-database-formalization.md) | **Formalization Level**: L5-L6
> **Translation Date**: 2026-04-21

## Abstract

Strict octuple formalization of Streaming Database (SDB) contrasting with Stream Processing Engine (SPE) heptuple model.

---

## 1. Definitions

### Def-S-01-12-01 (Streaming Database)

$$SDB = (S, Q, V, \Delta, \Sigma, \tau, \pi, \kappa)$$

- $S$: input streams
- $Q$: SQL query workload
- $V$: materialized views (first-class citizen)
- $\Delta$: incremental view maintenance
- $\Sigma$: consistency level
- $\tau$: transaction manager
- $\pi$: persistence layer
- $\kappa$: SQL compatibility

### Def-S-01-12-02 (Stream Processing Engine)

$$SPE = (S, T, O, C, \Sigma, \tau, \sigma)$$

- $T$: transformation operators
- $O$: output sinks
- $\sigma$: state backend

**Key difference**: SDB has persistent materialized views; SPE outputs to external sinks.

---

## 2. Comparison

| Aspect | SDB (RisingWave) | SPE (Flink) |
|--------|-----------------|-------------|
| Storage | Built-in persistent | External only |
| Query | Ad-hoc SQL | Predefined DAG |
| Views | Materialized, queryable | Not queryable |
| Consistency | Serializable | Exactly-once |
| Use case | Real-time analytics | ETL, pipelines |

---

## 3. References
