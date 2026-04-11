---
title: "Knowledge/ Directory Guide - Engineering Knowledge"
source_file: "Knowledge/00-INDEX.md"
source_version: "v3.3.0"
translation_status: "completed"
completion_percentage: 100
language: "en"
last_sync: "2026-04-08T09:52:41Z"
---

# Knowledge/ Knowledge Structure Navigation Index

> Stage: Knowledge | Prerequisites: [../README.md](../../../README.md), [../QUICK-START.md](../../../QUICK-START.md) | Formalization Level: L3-L5
>
> 🌐 **中文版** | **English Version**

---

## Introduction

This directory contains **knowledge structures, design patterns, business modeling, and technology selection** documents for the stream computing domain. Unlike the theoretical rigor of `Struct/`, `Knowledge/` focuses on knowledge organization, pattern extraction, and experience summarization in engineering practice.

**Core Positioning**:

- 🗺️ **Concept Atlas**: Systematic organization of stream computing core concepts
- 🎨 **Design Patterns**: Reusable stream processing architecture patterns
- 💼 **Business Scenarios**: Industry typical applications and solutions
- ⚖️ **Technology Selection**: Guides for choosing engines, storage, and architectures
- 🔄 **Mapping Guides**: Paths from theory to practice, from old systems to new systems
- 🚀 **Frontier Exploration**: Emerging directions like real-time AI, Serverless, Data Mesh
- ✅ **Best Practices**: Production environment checklists and tuning guides
- 📋 **Standards**: Data governance, security compliance specifications
- ⚠️ **Anti-Patterns**: Common pitfalls and avoidance strategies
- 📚 **Case Studies**: Real production case analysis

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
├── 08-standards/              # Standards and Specifications (2 documents)
├── 09-anti-patterns/          # Anti-Patterns (11 documents)
├── 10-case-studies/           # Case Studies (independent index)
└── 98-exercises/              # Exercises and Quick Reference (11 documents)
```

---

## 01. Concept Atlas

Systematic organization and visualization of stream computing core concepts.

| Document | Description | Use Case |
|----------|-------------|----------|
| [concurrency-paradigms-matrix.md](../../../Knowledge/01-concept-atlas/concurrency-paradigms-matrix.md) | Concurrency Paradigms Comparison Matrix: Full-dimensional comparison of Actor vs CSP vs Dataflow vs Thread | Technology selection, architecture design, team training |
| [data-streaming-landscape-2026-complete.md](../../../Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md) | 2026 Streaming Landscape: Complete overview of engines, databases, and ecosystems | Industry research, technology strategy, investment decisions |
| [streaming-models-mindmap.md](../../../Knowledge/01-concept-atlas/streaming-models-mindmap.md) | Stream Computing Models Mind Map: Knowledge map from theoretical models to engineering implementation | Learning path planning, knowledge system construction |

---

## 02. Design Patterns

Reusable architecture and implementation patterns in the stream processing domain.

| Document | Description | Use Case |
|----------|-------------|----------|
| [pattern-event-time-processing.md](../../../Knowledge/02-design-patterns/pattern-event-time-processing.md) | Event Time Processing Pattern: Complete solution for Watermark, windows, and out-of-order processing | Real-time ETL, log analysis, IoT data processing |
| [pattern-windowed-aggregation.md](../../../Knowledge/02-design-patterns/pattern-windowed-aggregation.md) | Windowed Aggregation Pattern: Design and implementation of tumbling, sliding, and session windows | Real-time metrics calculation, behavior analysis, monitoring alerts |
| [pattern-stateful-computation.md](../../../Knowledge/02-design-patterns/pattern-stateful-computation.md) | Stateful Computation Pattern: State Backend selection, state TTL, Queryable State | User sessions, real-time recommendations, pattern detection |
| [pattern-async-io-enrichment.md](../../../Knowledge/02-design-patterns/pattern-async-io-enrichment.md) | Async I/O Enrichment Pattern: Best practices for high-concurrency external data association | Real-time risk control, user profile enhancement, data completion |
| [pattern-side-output.md](../../../Knowledge/02-design-patterns/pattern-side-output.md) | Side Output Pattern: Elegant implementation for anomaly data diversion and multi-channel output | Data quality monitoring, exception handling, multi-target delivery |
| [pattern-cep-complex-event.md](../../../Knowledge/02-design-patterns/pattern-cep-complex-event.md) | Complex Event Processing (CEP) Pattern: Pattern definition, matching strategies, timeout handling | Fraud detection, business process monitoring, security analysis |
| [pattern-checkpoint-recovery.md](../../../Knowledge/02-design-patterns/pattern-checkpoint-recovery.md) | Checkpoint & Recovery Pattern: Exactly-Once implementation, Savepoint strategies | Financial transactions, critical business, fault tolerance design |
| [pattern-realtime-feature-engineering.md](../../../Knowledge/02-design-patterns/pattern-realtime-feature-engineering.md) | Real-time Feature Engineering Pattern: Feature calculation, online/offline consistency | ML feature platforms, real-time recommendations, intelligent decisions |
| [pattern-log-analysis.md](../../../Knowledge/02-design-patterns/pattern-log-analysis.md) | Log Real-time Analysis Pattern: Structured parsing, aggregation, anomaly detection | Operations monitoring, security auditing, business analysis |

---

## 03. Business Patterns

Typical application scenarios and solutions for stream computing across industries.

| Document | Description | Use Case |
|----------|-------------|----------|
| [fintech-realtime-risk-control.md](../../../Knowledge/03-business-patterns/fintech-realtime-risk-control.md) | Financial Real-time Risk Control: Anti-fraud, credit assessment, transaction monitoring | Banking, payments, insurance, securities |
| [real-time-recommendation.md](../../../Knowledge/03-business-patterns/real-time-recommendation.md) | Real-time Recommendation System: Personalized recommendations, real-time feature updates | E-commerce, content platforms, social media |
| [iot-stream-processing.md](../../../Knowledge/03-business-patterns/iot-stream-processing.md) | IoT Stream Processing: Device data collection, edge computing, real-time monitoring | Smart manufacturing, connected vehicles, energy management |
| [log-monitoring.md](../../../Knowledge/03-business-patterns/log-monitoring.md) | Log Monitoring and Alerting: Centralized collection, real-time analysis, intelligent alerts | Operations observability, DevOps, SRE |
| [alibaba-double11-flink.md](../../../Knowledge/03-business-patterns/alibaba-double11-flink.md) | Alibaba Double 11 Real-time Computing: Ultra-large-scale stream processing architecture | Sales events, traffic peaks, e-commerce core systems |
| [netflix-streaming-pipeline.md](../../../Knowledge/03-business-patterns/netflix-streaming-pipeline.md) | Netflix Real-time Data Processing: Playback experience optimization, content recommendations | Video streaming, user experience optimization |
| [uber-realtime-platform.md](../../../Knowledge/03-business-patterns/uber-realtime-platform.md) | Uber Real-time Platform: Supply-demand matching, dynamic pricing, ETA calculation | Sharing economy, mobility services, logistics scheduling |
| [spotify-music-recommendation.md](../../../Knowledge/03-business-patterns/spotify-music-recommendation.md) | Spotify Music Recommendation: Real-time music recommendations and discovery | Music platforms, content discovery, personalized experience |
| [stripe-payment-processing.md](../../../Knowledge/03-business-patterns/stripe-payment-processing.md) | Stripe Payment Processing: Real-time payment risk control and reconciliation | Payment processing, fintech, transaction compliance |
| [gaming-analytics.md](../../../Knowledge/03-business-patterns/gaming-analytics.md) | Gaming Real-time Analytics: Player behavior, anti-cheating, operational decisions | Gaming industry, real-time operations, player experience |
| [airbnb-marketplace-dynamics.md](../../../Knowledge/03-business-patterns/airbnb-marketplace-dynamics.md) | Airbnb Marketplace Dynamics: Supply-demand balance, pricing strategies, search ranking | Two-sided markets, platform economy, dynamic pricing |
| [data-mesh-streaming-architecture-2026.md](../../../Knowledge/03-business-patterns/data-mesh-streaming-architecture-2026.md) | Data Mesh Streaming Architecture: Domain-driven data products, self-service | Large enterprises, data platforms, organizational transformation |
| [streaming-data-product-economics.md](../../../Knowledge/03-business-patterns/streaming-data-product-economics.md) | Streaming Data Product Economics: Cost models, value assessment, ROI analysis | Data product management, cost control, value measurement |

---

## 04. Technology Selection

Guides for selecting stream computing engines, storage systems, and architecture solutions.

| Document | Description | Use Case |
|----------|-------------|----------|
| [paradigm-selection-guide.md](../../../Knowledge/04-technology-selection/paradigm-selection-guide.md) | Concurrency Paradigm Selection Guide: Decision tree for Actor/CSP/Dataflow selection | Early architecture design, technology stack evaluation |
| [engine-selection-guide.md](../../../Knowledge/04-technology-selection/engine-selection-guide.md) | Stream Processing Engine Selection: Flink/Spark/Kafka Streams comparison | Stream processing platform selection, engine migration evaluation |
| [streaming-database-guide.md](../../../Knowledge/04-technology-selection/streaming-database-guide.md) | Streaming Database Selection: Materialize/Risingwave/Timeplus comparison | Real-time analytics, materialized views, stream SQL requirements |
| [storage-selection-guide.md](../../../Knowledge/04-technology-selection/storage-selection-guide.md) | Storage System Selection: State Backend, Sink storage selection | State storage, data persistence, query requirements |
| [flink-vs-risingwave.md](../../../Knowledge/04-technology-selection/flink-vs-risingwave.md) | Flink vs RisingWave Deep Comparison: Architecture, scenarios, costs | Stream processing vs stream database, simplified architecture evaluation |

---

## 05. Mapping Guides

Paths from theory to code, from old systems to new systems.

| Document | Description | Use Case |
|----------|-------------|----------|
| [struct-to-flink-mapping.md](../../../Knowledge/05-mapping-guides/struct-to-flink-mapping.md) | Struct to Flink Mapping: Correspondence between theoretical concepts and Flink APIs | Engineering practice after theoretical learning, API selection |
| [theory-to-code-patterns.md](../../../Knowledge/05-mapping-guides/theory-to-code-patterns.md) | Theory to Code Patterns: Process calculus, type theory to implementation | Academic research to engineering, formal methods application |
| [migration-guides/05.1-spark-streaming-to-flink-migration.md](../../../Knowledge/05-mapping-guides/migration-guides/05.1-spark-streaming-to-flink-migration.md) | Spark Streaming to Flink Migration: Code transformation, semantic mapping | Spark user migration, technology stack unification |
| [migration-guides/05.2-kafka-streams-to-flink-migration.md](../../../Knowledge/05-mapping-guides/migration-guides/05.2-kafka-streams-to-flink-migration.md) | Kafka Streams to Flink Migration: DSL transformation, state migration | Kafka Streams expansion, complex processing requirements |
| [migration-guides/05.3-storm-to-flink-migration.md](../../../Knowledge/05-mapping-guides/migration-guides/05.3-storm-to-flink-migration.md) | Storm to Flink Migration: Topology transformation, semantic upgrade | Storm system modernization, Exactly-Once requirements |
| [migration-guides/05.4-flink-1x-to-2x-migration.md](../../../Knowledge/05-mapping-guides/migration-guides/05.4-flink-1x-to-2x-migration.md) | Flink 1.x to 2.x Migration: API changes, configuration adjustments, compatibility | Flink version upgrade, new feature adoption |
| [migration-guides/05.5-batch-to-streaming-migration.md](../../../Knowledge/05-mapping-guides/migration-guides/05.5-batch-to-streaming-migration.md) | Batch to Streaming Migration: Architecture transformation, mindset shift | Lambda architecture simplification, real-time transformation |
| [streaming-etl-tools-landscape-2026.md](../../../Knowledge/05-mapping-guides/streaming-etl-tools-landscape-2026.md) | 2026 Streaming ETL Tools Landscape: Tool comparison and selection | ETL modernization, data integration projects |
| [streaming-sql-engines-2026-comparison.md](../../../Knowledge/05-mapping-guides/streaming-sql-engines-2026-comparison.md) | 2026 Streaming SQL Engine Comparison: Flink SQL, RisingWave, etc. | SQL-first teams, lowering development barriers |
| [multi-agent-frameworks-2026-comparison.md](../../../Knowledge/05-mapping-guides/multi-agent-frameworks-2026-comparison.md) | 2026 Multi-Agent Framework Comparison: AutoGen, LangGraph, etc. | AI Agent architecture, multi-agent systems |

---

## 06. Frontier Exploration

Exploration of convergence between stream computing and AI, Serverless, Data Mesh, and other emerging directions.

### Real-time AI & Agents

| Document | Description | Use Case |
|----------|-------------|----------|
| [realtime-ai-streaming-2026.md](../../../Knowledge/06-frontier/realtime-ai-streaming-2026.md) | 2026 Real-time AI and Streaming Convergence Landscape | AI engineering, real-time intelligent decisions |
| [ai-agent-streaming-architecture.md](../../../Knowledge/06-frontier/ai-agent-streaming-architecture.md) | AI Agent Streaming Architecture: Stream computing-driven agent workflows | Agent systems, AI workflow orchestration |
| [mcp-protocol-agent-streaming.md](../../../Knowledge/06-frontier/mcp-protocol-agent-streaming.md) | MCP Protocol and Agent Streaming Processing | AI tool integration, protocol standards |
| [a2a-protocol-agent-communication.md](../../../Knowledge/06-frontier/a2a-protocol-agent-communication.md) | A2A Protocol: Agent communication standards and streaming implementation | Multi-agent collaboration, Google A2A |
| [ai-agent-a2a-protocol.md](../../../Knowledge/06-frontier/ai-agent-a2a-protocol.md) | AI Agent A2A Protocol Detailed Analysis | Agent communication, enterprise AI |
| [real-time-rag-architecture.md](../../../Knowledge/06-frontier/real-time-rag-architecture.md) | Real-time RAG Architecture: Streaming knowledge base updates and retrieval | Real-time knowledge enhancement, dynamic RAG |
| [multimodal-streaming-architecture.md](../../../Knowledge/06-frontier/multimodal-streaming-architecture.md) | Multimodal Streaming Architecture: Real-time text/image/audio processing | Multimedia AI, real-time content understanding |
| [multimodal-ai-streaming-architecture.md](../../../Knowledge/06-frontier/multimodal-ai-streaming-architecture.md) | Multimodal AI Streaming Architecture Detailed | Cross-modal real-time analysis, intelligent monitoring |
| [edge-llm-realtime-inference.md](../../../Knowledge/06-frontier/edge-llm-realtime-inference.md) | Edge LLM Real-time Inference: Edge large models and stream computing | Edge AI, low-latency inference |
| [ai-agent-database-workloads.md](../../../Knowledge/06-frontier/ai-agent-database-workloads.md) | AI Agent Database Workloads: Vector+Stream+Transaction convergence | AI data infrastructure, unified storage |

### Streaming Databases

| Document | Description | Use Case |
|----------|-------------|----------|
| [streaming-databases.md](../../../Knowledge/06-frontier/streaming-databases.md) | Streaming Databases Overview: Architecture, capabilities, use cases | Simplified real-time analytics architecture, SQL-first |
| [streaming-database-ecosystem-comparison.md](../../../Knowledge/06-frontier/streaming-database-ecosystem-comparison.md) | Streaming Database Ecosystem Comparison | Technology selection, ecosystem evaluation |
| [risingwave-deep-dive.md](../../../Knowledge/06-frontier/risingwave-deep-dive.md) | RisingWave Deep Dive: Architecture, performance, best practices | RisingWave adoption, technology evaluation |
| [risingwave-integration-guide.md](../../../Knowledge/06-frontier/risingwave-integration-guide.md) | RisingWave Integration Guide: Integration with Flink, Kafka, etc. | Hybrid architecture, gradual adoption |
| [materialize-comparison-guide.md](../../../Knowledge/06-frontier/materialize-comparison-guide.md) | Materialize Comparison Guide: SQL materialized view engine | Real-time materialized views, SQL stream processing |
| [streaming-materialized-view-architecture.md](../../../Knowledge/06-frontier/streaming-materialized-view-architecture.md) | Streaming Materialized View Architecture Design | Real-time reports, incremental computation |
| [vector-search-streaming-convergence.md](../../../Knowledge/06-frontier/vector-search-streaming-convergence.md) | Vector Search and Streaming Convergence: Real-time vector index updates | RAG systems, real-time semantic search |

### Serverless & Cloud Native

| Document | Description | Use Case |
|----------|-------------|----------|
| [serverless-stream-processing-architecture.md](../../../Knowledge/06-frontier/serverless-stream-processing-architecture.md) | Serverless Stream Processing Architecture | Elastic workloads, cost optimization |
| [serverless-streaming-architecture.md](../../../Knowledge/06-frontier/serverless-streaming-architecture.md) | Serverless Streaming Architecture Detailed | Cloud-native stream processing, pay-per-use |
| [serverless-streaming-cost-optimization.md](../../../Knowledge/06-frontier/serverless-streaming-cost-optimization.md) | Serverless Streaming Cost Optimization | FinOps, cost control |
| [stateful-serverless.md](../../../Knowledge/06-frontier/stateful-serverless.md) | Stateful Serverless: State management and function computing | Complex serverless applications, long-running |
| [faas-dataflow.md](../../../Knowledge/06-frontier/faas-dataflow.md) | FaaS Dataflow Patterns: Function orchestration and dataflow | Event-driven architecture, function workflows |
| [wasm-dataflow-patterns.md](../../../Knowledge/06-frontier/wasm-dataflow-patterns.md) | WebAssembly Dataflow Patterns: WASM and stream computing | Edge computing, cross-platform runtime |
| [multi-cloud-streaming-architecture.md](../../../Knowledge/06-frontier/multi-cloud-streaming-architecture.md) | Multi-cloud Streaming Architecture | Cloud provider decoupling, disaster recovery design |

### Data Mesh

| Document | Description | Use Case |
|----------|-------------|----------|
| [streaming-data-mesh-architecture.md](../../../Knowledge/06-frontier/streaming-data-mesh-architecture.md) | Streaming Data Mesh Architecture | Enterprise data platforms, domain-driven design |
| [realtime-data-mesh-practice.md](../../../Knowledge/06-frontier/realtime-data-mesh-practice.md) | Real-time Data Mesh Practice | Data mesh implementation, real-time data products |
| [realtime-data-product-architecture.md](../../../Knowledge/06-frontier/realtime-data-product-architecture.md) | Real-time Data Product Architecture | Data as product, self-service |

### Graph Streaming & Real-time Features

| Document | Description | Use Case |
|----------|-------------|----------|
| [streaming-graph-processing-tgn.md](../../../Knowledge/06-frontier/streaming-graph-processing-tgn.md) | Streaming Graph Processing and TGN (Temporal Graph Networks) | Real-time graph analysis, social networks |
| [realtime-graph-streaming-tgnn.md](../../../Knowledge/06-frontier/realtime-graph-streaming-tgnn.md) | Real-time Graph Streaming and TGNN | Graph neural networks, dynamic graph analysis |
| [realtime-feature-store-architecture.md](../../../Knowledge/06-frontier/realtime-feature-store-architecture.md) | Real-time Feature Store Architecture | MLOps, feature platforms |
| [realtime-digital-twin-streaming.md](../../../Knowledge/06-frontier/realtime-digital-twin-streaming.md) | Real-time Digital Twin Streaming | Industry 4.0, simulation |

### Edge Computing

| Document | Description | Use Case |
|----------|-------------|----------|
| [edge-streaming-architecture.md](../../../Knowledge/06-frontier/edge-streaming-architecture.md) | Edge Streaming Architecture | Edge AI, industrial IoT |
| [edge-streaming-patterns.md](../../../Knowledge/06-frontier/edge-streaming-patterns.md) | Edge Streaming Patterns | Edge computing best practices |
| [cloud-edge-continuum.md](../../../Knowledge/06-frontier/cloud-edge-continuum.md) | Cloud-Edge Continuum Architecture | Cloud-edge collaboration, hierarchical processing |

---

## 07. Best Practices

Production environment checklists, tuning guides, and operations strategies.

| Document | Description | Use Case |
|----------|-------------|----------|
| [07.01-flink-production-checklist.md](../../../Knowledge/07-best-practices/07.01-flink-production-checklist.md) | Flink Production Checklist: Complete pre-launch checklist | Production launch, operations audit, compliance checks |
| [07.02-performance-tuning-patterns.md](../../../Knowledge/07-best-practices/07.02-performance-tuning-patterns.md) | Performance Tuning Patterns: Backpressure optimization, serialization optimization, parallelism tuning | Performance optimization, bottleneck troubleshooting |
| [07.03-troubleshooting-guide.md](../../../Knowledge/07-best-practices/07.03-troubleshooting-guide.md) | Troubleshooting Guide: Common problem diagnosis and resolution | Production issues, emergency fixes |
| [07.04-cost-optimization-patterns.md](../../../Knowledge/07-best-practices/07.04-cost-optimization-patterns.md) | Cost Optimization Patterns: Resource utilization, storage costs, computation optimization | FinOps, cost reduction |
| [07.05-security-hardening-guide.md](../../../Knowledge/07-best-practices/07.05-security-hardening-guide.md) | Security Hardening Guide: Authentication, authorization, encryption, auditing | Security compliance, production hardening |
| [07.06-high-availability-patterns.md](../../../Knowledge/07-best-practices/07.06-high-availability-patterns.md) | High Availability Patterns: Failover, multi-active architecture, disaster recovery | Critical business, SLA guarantees |
| [07.07-testing-strategies-complete.md](../../../Knowledge/07-best-practices/07.07-testing-strategies-complete.md) | Testing Strategies Complete Guide: Unit, integration, end-to-end testing | Quality assurance, CI/CD |

---

## 08. Standards

Industry standards and best practices for data governance and security compliance.

| Document | Description | Use Case |
|----------|-------------|----------|
| [streaming-data-governance.md](../../../Knowledge/08-standards/streaming-data-governance.md) | Streaming Data Governance: Metadata management, data lineage, quality standards | Data governance projects, compliance requirements |
| [streaming-data-governance-quality.md](../../../Knowledge/08-standards/streaming-data-governance-quality.md) | Streaming Data Governance and Quality: Quality rules, monitoring, improvement | Data quality management, continuous improvement |

---

## 09. Anti-Patterns

Common pitfalls, bad practices, and avoidance strategies in stream processing.

| Document | Description | Use Case |
|----------|-------------|----------|
| [README.md](../../../Knowledge/09-anti-patterns/README.md) | Anti-Patterns Overview and Index | Anti-pattern introduction, quick browsing |
| [anti-pattern-checklist.md](../../../Knowledge/09-anti-patterns/anti-pattern-checklist.md) | Anti-Pattern Checklist: Code review, design review | Code review, design review |
| [anti-pattern-01-global-state-abuse.md](../../../Knowledge/09-anti-patterns/anti-pattern-01-global-state-abuse.md) | Anti-Pattern 01: Global State Abuse | State design, concurrency safety |
| [anti-pattern-02-watermark-misconfiguration.md](../../../Knowledge/09-anti-patterns/anti-pattern-02-watermark-misconfiguration.md) | Anti-Pattern 02: Watermark Misconfiguration | Time processing, late data |
| [anti-pattern-03-checkpoint-interval-misconfig.md](../../../Knowledge/09-anti-patterns/anti-pattern-03-checkpoint-interval-misconfig.md) | Anti-Pattern 03: Checkpoint Interval Misconfiguration | Fault tolerance design, performance optimization |
| [anti-pattern-04-hot-key-skew.md](../../../Knowledge/09-anti-patterns/anti-pattern-04-hot-key-skew.md) | Anti-Pattern 04: Hot Key Skew | Data distribution, load balancing |
| [anti-pattern-05-blocking-io-processfunction.md](../../../Knowledge/09-anti-patterns/anti-pattern-05-blocking-io-processfunction.md) | Anti-Pattern 05: Blocking I/O in ProcessFunction | Async design, performance optimization |
| [anti-pattern-06-serialization-overhead.md](../../../Knowledge/09-anti-patterns/anti-pattern-06-serialization-overhead.md) | Anti-Pattern 06: Serialization Overhead | Performance optimization, serialization selection |
| [anti-pattern-07-window-state-explosion.md](../../../Knowledge/09-anti-patterns/anti-pattern-07-window-state-explosion.md) | Anti-Pattern 07: Window State Explosion | State management, memory optimization |
| [anti-pattern-08-ignoring-backpressure.md](../../../Knowledge/09-anti-patterns/anti-pattern-08-ignoring-backpressure.md) | Anti-Pattern 08: Ignoring Backpressure Signals | Flow control design, stability assurance |
| [anti-pattern-09-multi-stream-join-misalignment.md](../../../Knowledge/09-anti-patterns/anti-pattern-09-multi-stream-join-misalignment.md) | Anti-Pattern 09: Multi-Stream Join Misalignment | Join design, time alignment |
| [anti-pattern-10-resource-estimation-oom.md](../../../Knowledge/09-anti-patterns/anti-pattern-10-resource-estimation-oom.md) | Anti-Pattern 10: Resource Estimation OOM | Capacity planning, resource management |
| [streaming-anti-patterns.md](../../../Knowledge/09-anti-patterns/streaming-anti-patterns.md) | Streaming Anti-Patterns Comprehensive Guide | Systematic anti-pattern learning |

---

## Navigation Links

### Project Indexes

| Target | Path |
|--------|------|
| 🏠 Project Root | [../../../README.md](../../../README.md) |
| 🚀 Quick Start | [../../../QUICK-START.md](../../../QUICK-START.md) |
| 📊 Project Tracking | [../../../PROJECT-TRACKING.md](../../../PROJECT-TRACKING.md) |
| 🔧 Theorem Registry | [../../../THEOREM-REGISTRY.md](../../../THEOREM-REGISTRY.md) |
| 🗺️ Roadmap | [../../../ROADMAP.md](../../../ROADMAP.md) |
| 📖 English README | [../../../README-EN.md](../../../README-EN.md) |
| 🚀 English Quick Start | [../../../QUICK-START-EN.md](../../../QUICK-START-EN.md) |

### Sister Directory Indexes

| Directory | Index | Description |
|-----------|-------|-------------|
| Struct/ | [../../../Struct/00-INDEX.md](../../../Struct/00-INDEX.md) | Formal Theory and Rigorous Proofs |
| Flink/ | [../../../Flink/00-INDEX.md](../../../Flink/00-INDEX.md) | Flink-Specific Technology and Implementation |

---

## Statistics

```
Knowledge/ Directory Statistics:
├── 01-concept-atlas/:        3 documents
├── 02-design-patterns/:      9 documents
├── 03-business-patterns/:   13 documents
├── 04-technology-selection/: 5 documents
├── 05-mapping-guides/:      10 documents
├── 06-frontier/:            40+ documents
├── 07-best-practices/:       7 documents
├── 08-standards/:            2 documents
├── 09-anti-patterns/:       13 documents
├── 10-case-studies/:        14 documents (independent index)
└── 98-exercises/:           12 documents
----------------------------------------
Total: Approximately 128+ documents
```

---

## Usage Recommendations

### 🎯 By Role

- **Architects**: 01-concept-atlas → 04-technology-selection → 06-frontier
- **Developers**: 02-design-patterns → 07-best-practices → 09-anti-patterns
- **Data Engineers**: 03-business-patterns → 05-mapping-guides → 10-case-studies
- **Operations Engineers**: 07-best-practices → 09-anti-patterns → 08-standards
- **Learners**: 98-exercises → 01-concept-atlas → 02-design-patterns

### 🔄 Typical Learning Paths

1. **Beginner Path**: Concept Atlas → Design Patterns → Exercises → Case Studies
2. **Advanced Path**: Business Scenarios → Technology Selection → Best Practices → Frontier Exploration
3. **Expert Path**: Frontier Exploration → Mapping Guides → Anti-Patterns → Standards

---

> **Document Specification**: This document follows the six-section template specification in [AGENTS.md](../../../AGENTS.md)
> **Last Updated**: 2026-04-08
