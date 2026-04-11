---
title: "[EN] Knowledge/ Knowledge Structure Navigation Index"
translation_status: "ai_translated"
source_file: "Knowledge/00-INDEX.md"
source_version: "k7l8m9n0"
translator: "AI"
reviewer: null
translated_at: "2026-04-08T14:30:00+08:00"
reviewed_at: null
quality_score: null
terminology_verified: true
---

# Knowledge/ Knowledge Structure Navigation Index

> **Stage**: Knowledge | **Prerequisites**: [../README.md](../README.md), [../QUICK-START.md](../QUICK-START.md) | **Formalization Level**: L3-L5

## Introduction

This directory contains practical documents on **knowledge structure, design patterns, business modeling, and technical selection** in the stream computing field. Unlike the theoretical rigor of `Struct/`, `Knowledge/` focuses on knowledge organization, pattern extraction, and experience summarization in engineering practice.

**Core Positioning**:

- 🗺️ **Concept Atlas**: Systematic organization of stream computing core concepts
- 🎨 **Design Patterns**: Reusable stream processing architecture patterns
- 💼 **Business Scenarios**: Typical industry applications and solutions
- ⚖️ **Technology Selection**: Guides for choosing engines, storage, and architectures
- 🔄 **Mapping Guides**: Migration paths from theory to practice, old systems to new
- 🚀 **Frontier Exploration**: Emerging directions like Real-time AI, Serverless, Data Mesh
- ✅ **Best Practices**: Production environment checklists and tuning guides
- 📋 **Standards**: Data governance and security compliance specifications
- ⚠️ **Anti-patterns**: Common pitfalls and avoidance strategies
- 📚 **Case Studies**: Real-world production case analyses

---

## Directory Structure

```
Knowledge/
├── 01-concept-atlas/          # Concept Atlas (3 documents)
├── 02-design-patterns/        # Design Patterns (8 documents)
├── 03-business-patterns/      # Business Scenarios (13 documents)
├── 04-technology-selection/   # Technology Selection (5 documents)
├── 05-mapping-guides/         # Mapping Guides (7 documents)
├── 06-frontier/               # Frontier Exploration (40+ documents)
├── 07-best-practices/         # Best Practices (7 documents)
├── 08-standards/              # Standards (2 documents)
├── 09-anti-patterns/          # Anti-patterns (11 documents)
├── 10-case-studies/           # Case Studies (independent index)
└── 98-exercises/              # Exercises and Cheatsheets (11 documents)
```

---

## 01. Concept Atlas

Systematic organization and visualization of stream computing core concepts.

| Document | Description | Use Case |
|----------|-------------|----------|
| [concurrency-paradigms-matrix.md](01-concept-atlas/concurrency-paradigms-matrix.md) | Concurrency Paradigms Comparison Matrix: Full-dimension comparison of Actor vs CSP vs Dataflow vs Thread | Technology selection, architecture design, team training |
| [data-streaming-landscape-2026-complete.md](01-concept-atlas/data-streaming-landscape-2026-complete.md) | 2026 Data Streaming Landscape: Complete overview of engines, databases, and ecosystems | Industry research, technology strategy, investment decisions |
| [streaming-models-mindmap.md](01-concept-atlas/streaming-models-mindmap.md) | Stream Computing Models Mind Map: Knowledge map from theoretical models to engineering implementation | Learning path planning, knowledge system construction |

---

## 02. Design Patterns

Reusable architecture and implementation patterns in stream processing.

| Document | Description | Use Case |
|----------|-------------|----------|
| [pattern-event-time-processing.md](02-design-patterns/pattern-event-time-processing.md) | Event Time Processing Pattern: Complete solution for Watermark, windows, and out-of-order handling | Real-time ETL, log analysis, IoT data processing |
| [pattern-windowed-aggregation.md](02-design-patterns/pattern-windowed-aggregation.md) | Windowed Aggregation Pattern: Design and implementation of tumbling, sliding, and session windows | Real-time metrics, behavior analysis, monitoring alerts |
| [pattern-stateful-computation.md](02-design-patterns/pattern-stateful-computation.md) | Stateful Computation Pattern: State Backend selection, state TTL, Queryable State | User sessions, real-time recommendations, pattern detection |
| [pattern-async-io-enrichment.md](02-design-patterns/pattern-async-io-enrichment.md) | Async I/O Enrichment Pattern: Best practices for high-concurrency external data association | Real-time risk control, user profiling enhancement, data completion |
| [pattern-side-output.md](02-design-patterns/pattern-side-output.md) | Side Output Pattern: Elegant implementation for anomaly data diversion and multi-way output | Data quality monitoring, exception handling, multi-target delivery |
| [pattern-cep-complex-event.md](02-design-patterns/pattern-cep-complex-event.md) | Complex Event Processing (CEP) Pattern: Pattern definition, matching strategies, timeout handling | Fraud detection, business process monitoring, security analysis |
| [pattern-checkpoint-recovery.md](02-design-patterns/pattern-checkpoint-recovery.md) | Checkpoint and Recovery Pattern: Exactly-Once implementation, Savepoint strategies | Financial transactions, critical business, fault tolerance design |
| [pattern-realtime-feature-engineering.md](02-design-patterns/pattern-realtime-feature-engineering.md) | Real-time Feature Engineering Pattern: Feature computation, online/offline consistency | ML feature platform, real-time recommendations, intelligent decisions |
| [pattern-log-analysis.md](02-design-patterns/pattern-log-analysis.md) | Log Real-time Analysis Pattern: Structured parsing, aggregation, anomaly detection | Ops monitoring, security audit, business analysis |

---

## 03. Business Scenarios

Typical stream computing application scenarios and solutions across industries.

| Document | Description | Use Case |
|----------|-------------|----------|
| [fintech-realtime-risk-control.md](03-business-patterns/fintech-realtime-risk-control.md) | Financial Real-time Risk Control: Anti-fraud, credit assessment, transaction monitoring | Banking, payments, insurance, securities |
| [real-time-recommendation.md](03-business-patterns/real-time-recommendation.md) | Real-time Recommendation System: Personalized recommendations, real-time feature updates | E-commerce, content platforms, social media |

---

## Navigation Links

- **Theory Layer**: [Struct/00-INDEX.md](../Struct/00-INDEX.md)
- **Implementation Layer**: [Flink/00-INDEX.md](../Flink/00-INDEX.md)
- **Visual Navigation**: [visuals/](../visuals/)

---

*For Chinese version, see [Knowledge/00-INDEX.md](../../Knowledge/00-INDEX.md)*
