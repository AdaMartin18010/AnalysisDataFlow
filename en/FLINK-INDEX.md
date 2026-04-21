# Flink Knowledge Index (English)

> **Language**: English | **Source**: [Flink/](../Flink/) | **Last Updated**: 2026-04-21

---

## Overview

This index provides a navigational entry point to the English-language Flink documentation within the AnalysisDataFlow project. For the complete Chinese source, see [Flink/00-INDEX.md](../Flink/00-INDEX.md).

## Directory Structure

| Directory | Topic | Key Documents |
|-----------|-------|---------------|
| `01-concepts/` | Core Concepts | Streaming fundamentals, Dataflow model, Time semantics |
| `02-core/` | Core Mechanisms | Checkpointing, state backends, watermark propagation, backpressure |
| `03-api/` | APIs | DataStream API, Table API, SQL, connectors |
| `04-runtime/` | Runtime | Task scheduling, network stack, memory management, fault tolerance |
| `05-ecosystem/` | Ecosystem | Connectors, formats, deployment modes, Kubernetes integration |
| `06-ai-ml/` | AI/ML | Flink ML, inference serving, feature engineering |
| `07-roadmap/` | Roadmap | Flink 2.x/3.0 roadmap, FLIP tracking, release notes |

## Key Documents

### Getting Started

- [Flink Quick Start](FLINK-QUICK-START.md) — Single-node setup and first streaming job
- [Architecture Overview](ARCHITECTURE.md) — Flink architecture and component map

### Core Mechanisms

- [Checkpoint Deep Dive](flink-checkpoint-deep-dive.md) — Checkpoint algorithm, barriers, alignment
- [State Backends](flink-state-backends.md) — Heap vs RocksDB, incremental checkpoints
- [Watermark Propagation](flink-watermark-propagation.md) — Watermark generation, idle sources, late data

### Advanced Topics

- [Exactly-Once Semantics](flink-exactly-once.md) — Two-phase commit, idempotent sinks, end-to-end guarantees
- [Backpressure Mechanism](flink-backpressure.md) — Detection, propagation, mitigation strategies

## Formal Elements

The Flink directory contains **433+ documents**, **752+ theorems**, and **1,982+ definitions** as of v6.2.

## References
