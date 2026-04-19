# Knowledge/ Knowledge Structure Navigation Index

> **Stage**: Knowledge | **Prerequisites**: [../README.md](../README.md), [../QUICK-START.md](../QUICK-START.md) | **Formalization Level**: L3-L5

## Introduction

This directory contains practical documents on **knowledge organization, design patterns, business modeling, and technology selection** in the stream computing domain. Unlike the theoretical rigor of `Struct/`, `Knowledge/` focuses on engineering practice, pattern extraction, and experience summarization.

**Core Positioning**:

- 🗺️ Concept Atlas: Systematic organization of stream computing core concepts
- 🎨 Design Patterns: Reusable stream processing architecture patterns
- 💼 Business Scenarios: Industry typical applications and solutions
- ⚖️ Technology Selection: Guides for choosing engines, storage, and architectures
- 🔄 Mapping Guides: Migration paths from theory to practice, old systems to new systems
- 🚀 Frontier Exploration: Emerging directions like real-time AI, Serverless, Data Mesh
- ✅ Best Practices: Production checklists and tuning guides
- 📋 Standards: Data governance and security compliance specifications
- ⚠️ Anti-Patterns: Common pitfalls and avoidance strategies
- 📚 Case Studies: Real production case analyses

---

## Directory Structure

```
Knowledge/
├── 01-concept-atlas/          # Concept Atlas (3 docs)
├── 02-design-patterns/        # Design Patterns (8 docs)
├── 03-business-patterns/      # Business Scenarios (13 docs)
├── 04-technology-selection/   # Technology Selection (5 docs)
├── 05-mapping-guides/         # Mapping Guides (7 docs)
├── 06-frontier/               # Frontier Exploration (40+ docs)
├── 07-best-practices/         # Best Practices (7 docs)
├── 08-standards/              # Standards (2 docs)
├── 09-anti-patterns/          # Anti-Patterns (11 docs)
├── 10-case-studies/           # Case Studies (separate index)
└── 98-exercises/              # Exercises & Cheatsheets (11 docs)
```

---

## 01. Concept Atlas

Systematic organization and visualization of stream computing core concepts.

| Document | Description | Use Cases |
|----------|-------------|-----------|
| [concurrency-paradigms-matrix-en.md](01-concept-atlas/concurrency-paradigms-matrix-en.md) | Concurrency paradigm comparison matrix: Actor vs CSP vs Dataflow vs Thread | Technology selection, architecture design, team training |
| [data-streaming-landscape-2026-complete-en.md](01-concept-atlas/data-streaming-landscape-2026-complete-en.md) | 2026 Stream Computing Landscape: engines, databases, ecosystems | Industry research, tech strategy, investment decisions |
| [streaming-models-mindmap-en.md](01-concept-atlas/streaming-models-mindmap-en.md) | Streaming Models Mindmap: knowledge map from theory to implementation | Learning path planning, knowledge system building |
| [go-concurrency-evolution-2025-en.md](01-concept-atlas/go-concurrency-evolution-2025-en.md) | Go 1.22/1.23/1.24 new features and stream computing applications | Go stream processing system upgrades |
| [streaming-languages-landscape-2025-en.md](01-concept-atlas/streaming-languages-landscape-2025-en.md) | 2025 Stream Computing Language Ecosystem: Java/Scala/Go/Rust/Python | Language selection for stream computing projects |

---

## 02. Design Patterns

Reusable architecture and implementation patterns in stream processing.

| Document | Description | Use Cases |
|----------|-------------|-----------|
| [pattern-event-time-processing-en.md](02-design-patterns/pattern-event-time-processing-en.md) | Event Time Processing: Watermark, windows, out-of-order handling | Real-time ETL, log analysis, IoT data processing |
| [pattern-windowed-aggregation-en.md](02-design-patterns/pattern-windowed-aggregation-en.md) | Windowed Aggregation: tumbling, sliding, session windows | Real-time metrics, behavior analysis, monitoring alerts |
| [pattern-stateful-computation-en.md](02-design-patterns/pattern-stateful-computation-en.md) | Stateful Computation: State Backend selection, TTL, Queryable State | User sessions, real-time recommendations, pattern detection |
| [pattern-async-io-enrichment-en.md](02-design-patterns/pattern-async-io-enrichment-en.md) | Async IO Dimension Table Enrichment: high-concurrency external data joins | Real-time risk control, user profiling, data enrichment |
| [pattern-side-output-en.md](02-design-patterns/pattern-side-output-en.md) | Side Output Pattern: anomaly data分流, multi-target output | Data quality monitoring, exception handling |
| [pattern-cep-complex-event-en.md](02-design-patterns/pattern-cep-complex-event-en.md) | Complex Event Processing (CEP): pattern definition, matching, timeouts | Fraud detection, business process monitoring |
| [pattern-checkpoint-recovery-en.md](02-design-patterns/pattern-checkpoint-recovery-en.md) | Checkpoint & Recovery: Exactly-Once implementation, Savepoint | Financial transactions, critical business, fault tolerance |
| [pattern-realtime-feature-engineering-en.md](02-design-patterns/pattern-realtime-feature-engineering-en.md) | Real-time Feature Engineering: feature computation, online/offline consistency | ML feature platforms, real-time recommendations |
| [pattern-log-analysis-en.md](02-design-patterns/pattern-log-analysis-en.md) | Log Real-time Analysis: structured parsing, aggregation, anomaly detection | Operations monitoring, security audit, business analysis |
| [polyglot-streaming-patterns-en.md](02-design-patterns/polyglot-streaming-patterns-en.md) | Polyglot Stream Processing: Flink+Rust/Python/Go integration | Multi-language stream processing, UDF optimization |

---

*Document Version: v1.0 | Created: 2026-04-20*
