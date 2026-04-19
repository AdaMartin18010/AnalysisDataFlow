# Flink/ Specialized Document Index

> **Stage**: Flink/ | **Prerequisites**: [Project Root](../README.md), [Knowledge/00-INDEX-en.md](../Knowledge/00-INDEX-en.md) | **Status**: Continuously Updated

## Introduction

**Flink/** directory contains comprehensive technical documentation for the Apache Flink stream computing framework, covering everything from core concepts to production practices.

**Core Positioning**:

- 🏗️ Architecture Design: Flink system architecture and deployment patterns
- ⚙️ Core Mechanisms: Checkpoint, state management, time semantics
- 🔌 API Ecosystem: DataStream, Table API, SQL
- 🌐 Ecosystem: Connectors, Lakehouse integration
- 🤖 AI/ML Integration: Real-time machine learning, LLM integration
- 🦀 Rust Ecosystem: WASM UDF, high-performance computing
- 📊 Performance Optimization: Benchmarks, tuning guides
- 🚀 Roadmap: Flink 2.4/2.5/3.0 version evolution

---

## Quick Navigation

| Entry | Description | Recommendation |
|-------|-------------|----------------|
| [00-meta/00-INDEX.md](00-meta/00-INDEX.md) | Detailed category index | ⭐⭐⭐⭐⭐ |
| [00-meta/00-QUICK-START.md](00-meta/00-QUICK-START.md) | Quick start guide | ⭐⭐⭐⭐⭐ |
| [02-core/checkpoint-mechanism-deep-dive-en.md](02-core/checkpoint-mechanism-deep-dive-en.md) | Checkpoint mechanism deep dive | ⭐⭐⭐⭐⭐ |
| [03-api/03.02-table-sql-api/flink-table-sql-complete-guide-en.md](03-api/03.02-table-sql-api/flink-table-sql-complete-guide-en.md) | SQL complete guide | ⭐⭐⭐⭐⭐ |

---

## Module Index

### 01. Architecture Design

> System architecture, deployment patterns, version evolution

| Document | Description | Version |
|----------|-------------|---------|
| [01-concepts/deployment-architectures-en.md](01-concepts/deployment-architectures-en.md) | Deployment architectures | 1.17+ |
| [01-concepts/flink-1.x-vs-2.0-comparison-en.md](01-concepts/flink-1.x-vs-2.0-comparison-en.md) | 1.x vs 2.0 comparison | 1.18-2.0 |
| [01-concepts/flink-system-architecture-deep-dive-en.md](01-concepts/flink-system-architecture-deep-dive-en.md) | System architecture deep dive | 1.17+ |
| [01-concepts/disaggregated-state-analysis-en.md](01-concepts/disaggregated-state-analysis-en.md) | Disaggregated state storage | 2.0+ |

---

### 02. Core Mechanisms

> Checkpoint, state management, time semantics, fault tolerance

#### Checkpoint & Fault Tolerance ⭐

| Document | Description | Version |
|----------|-------------|---------|
| [02-core/checkpoint-mechanism-deep-dive-en.md](02-core/checkpoint-mechanism-deep-dive-en.md) | Checkpoint mechanism deep dive | 1.17+ |
| [02-core/exactly-once-semantics-deep-dive-en.md](02-core/exactly-once-semantics-deep-dive-en.md) | Exactly-Once semantics | 1.17+ |
| [02-core/exactly-once-end-to-end-en.md](02-core/exactly-once-end-to-end-en.md) | End-to-end Exactly-Once | 1.17+ |
| [02-core/smart-checkpointing-strategies-en.md](02-core/smart-checkpointing-strategies-en.md) | Smart checkpoint strategies | 1.18+ |

#### State Management ⭐

| Document | Description | Version |
|----------|-------------|---------|
| [02-core/flink-state-management-complete-guide-en.md](02-core/flink-state-management-complete-guide-en.md) | State management complete guide | 1.17+ |
| [02-core/state-backends-deep-comparison-en.md](02-core/state-backends-deep-comparison-en.md) | State Backend deep comparison | 1.17+ |
| [02-core/forst-state-backend-en.md](02-core/forst-state-backend-en.md) | ForSt State Backend | 2.0+ |
| [02-core/flink-state-ttl-best-practices-en.md](02-core/flink-state-ttl-best-practices-en.md) | State TTL best practices | 1.17+ |

#### Time & Watermark ⭐

| Document | Description | Version |
|----------|-------------|---------|
| [02-core/time-semantics-and-watermark-en.md](02-core/time-semantics-and-watermark-en.md) | Time semantics and Watermark | 1.17+ |

#### Execution Optimization

| Document | Description | Version |
|----------|-------------|---------|
| [02-core/backpressure-and-flow-control-en.md](02-core/backpressure-and-flow-control-en.md) | Backpressure and flow control | 1.17+ |

---

*Document Version: v1.0 | Created: 2026-04-20*
