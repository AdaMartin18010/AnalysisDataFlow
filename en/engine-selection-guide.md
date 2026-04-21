# Stream Processing Engine Selection Guide

> **Stage**: Knowledge/04-technology-selection | **Prerequisites**: [Expressiveness Hierarchy](../../Struct/03-relationships/03.03-expressiveness-hierarchy.md) | **Formalization Level**: L4-L6
> **Translation Date**: 2026-04-21

## Abstract

Decision framework for selecting stream processing engines across six dimensions: latency, throughput, semantics, state management, ecosystem, and operability.

---

## 1. Engine Definitions

| Engine | Architecture | Latency | Exactly-Once |
|--------|-------------|---------|--------------|
| Apache Flink | Native streaming | < 100ms | Yes (checkpoint) |
| Kafka Streams | Embedded library | < 10ms | Yes (transactions) |
| Spark Structured Streaming | Micro-batch | ~100ms-seconds | Yes (WAL+checkpoint) |
| Apache Storm | Native streaming | < 10ms | No (at-least-once) |
| Pulsar Functions | Serverless | < 100ms | Yes (transactions) |

---

## 2. Key Properties

### Lemma-K-04-01 (Latency-Throughput Trade-off Upper Bound)

For any engine: $L \cdot T \leq C$ (constant bounded by architecture).

### Prop-K-04-02 (Micro-batch Latency Lower Bound)

Micro-batch engines have latency lower bound: $L \geq \Delta_{batch}$.

---

## 3. Selection Matrix

| Scenario | Recommended | Reason |
|----------|-------------|--------|
| Real-time ML inference | Flink | Low latency + stateful |
| ETL pipelines | Spark | Batch heritage + SQL |
| Event-driven microservices | Kafka Streams | Embedded simplicity |
| Simple transformations | Pulsar Functions | Serverless ease |
| Legacy migration | Storm → Flink | Similar semantics |

---

## 4. References
