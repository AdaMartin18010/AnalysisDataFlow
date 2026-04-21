# Streaming Systems Comparison 2026

> **Stage**: Struct/05-comparative-analysis | **Prerequisites**: [Expressiveness Hierarchy](expressiveness-hierarchy.md) | **Formalization Level**: L4-L5
> **Translation Date**: 2026-04-21

## Abstract

Formal comparison of major stream processing systems across computation model, time semantics, state model, fault tolerance, and consistency guarantees.

---

## 1. Definitions

### Def-S-05-05-01 (Stream Processing System Formal Tuple)

A stream processing system $\mathcal{S}$ is an 8-tuple:

$$\mathcal{S} = (\mathcal{M}, \mathcal{O}, \mathcal{T}, \mathcal{S}_t, \mathcal{F}, \mathcal{C}, \mathcal{R}, \mathcal{P})$$

where:

- $\mathcal{M}$: computation model (Dataflow / Actor / CSP / EPC)
- $\mathcal{O}$: operator set
- $\mathcal{T}$: time semantics (Event / Processing / Ingestion)
- $\mathcal{S}_t$: state model (Keyed / Operator / None)
- $\mathcal{F}$: fault tolerance (Checkpoint / WAL / None)
- $\mathcal{C}$: consistency (Exactly-Once / At-Least-Once / At-Most-Once)
- $\mathcal{R}$: resource scheduling
- $\mathcal{P}$: programming interface (SQL / DataStream / DAG)

---

## 2. System Comparison

| System | Model | Time | State | Fault Tolerance | Consistency |
|--------|-------|------|-------|----------------|-------------|
| Apache Flink | Dataflow | Event Time | Keyed + Operator | Chandy-Lamport Checkpoint | Exactly-Once |
| Spark Streaming | Micro-batch | Processing | None | RDD Lineage | Exactly-Once |
| Kafka Streams | Processor Topology | Event Time | Keyed | Standby Replicas | Exactly-Once |
| RisingWave | Streaming SQL | Event Time | Materialized View | WAL + Snapshot | Exactly-Once |
| Materialize | Differential Dataflow | Event Time | Arrangements | Determinism | Strict Serializability |
| Pulsar Functions | Event-driven | Processing | None | Redelivery | At-Least-Once |
| Storm | DAG | Processing | None | Record ACK | At-Least-Once |

---

## 3. Properties

### Lemma-S-05-05-01 (Model Expressiveness implies Operator Completeness)

If $\mathcal{M}_1 \succeq \mathcal{M}_2$, then $\mathcal{O}_1$ can simulate all operators in $\mathcal{O}_2$.

### Lemma-S-05-05-02 (Time-Consistency Coupling)

- Event Time + Exactly-Once requires watermark monotonicity
- Processing Time + Exactly-Once requires only idempotent sinks

---

## 4. References
