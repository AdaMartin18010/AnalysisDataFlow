# Knowledge/ Engineering Practice - English Navigation

> **Document Position**: Knowledge/ English Content Index | **Version**: 2026.04 | **Status**: Index Only

---

## Overview

The **Knowledge/** directory contains practical engineering knowledge for stream computing, including design patterns, business scenarios, technology selection guides, and best practices.

**Note**: Currently, Knowledge/ documents are primarily in Chinese. This index provides navigation to key practical concepts with English summaries.

---

## Content Areas

### 01. Concept Atlas

Systematic mapping of stream computing core concepts.

| Document | Chinese Path | Description |
|----------|-------------|-------------|
| Concurrency Paradigms Matrix | [01-concept-atlas/concurrency-paradigms-matrix.md](../Knowledge/01-concept-atlas/concurrency-paradigms-matrix.md) | Actor vs CSP vs Dataflow vs Thread comparison |
| Streaming Landscape 2026 | [01-concept-atlas/data-streaming-landscape-2026-complete.md](../Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md) | Complete ecosystem overview |
| Streaming Models Mindmap | [01-concept-atlas/streaming-models-mindmap.md](../Knowledge/01-concept-atlas/streaming-models-mindmap.md) | Knowledge map from theory to practice |

**Key Concepts**:
- **Concurrency Paradigms**: Actor (message passing), CSP (synchronous channels), Dataflow (stream graphs), Threads (shared memory)
- **Streaming Engines**: Flink, Spark Streaming, Kafka Streams, RisingWave comparison
- **Time Semantics**: Event time vs Processing time vs Ingestion time

### 02. Design Patterns

Reusable stream processing architecture patterns.

| Pattern | Chinese Path | Use Case |
|---------|-------------|----------|
| Event Time Processing | [02-design-patterns/pattern-event-time-processing.md](../Knowledge/02-design-patterns/pattern-event-time-processing.md) | Real-time ETL, log analysis |
| Windowed Aggregation | [02-design-patterns/pattern-windowed-aggregation.md](../Knowledge/02-design-patterns/pattern-windowed-aggregation.md) | Real-time metrics, monitoring |
| Stateful Computation | [02-design-patterns/pattern-stateful-computation.md](../Knowledge/02-design-patterns/pattern-stateful-computation.md) | User sessions, recommendations |
| Async IO Enrichment | [02-design-patterns/pattern-async-io-enrichment.md](../Knowledge/02-design-patterns/pattern-async-io-enrichment.md) | Real-time risk control |
| Side Output | [02-design-patterns/pattern-side-output.md](../Knowledge/02-design-patterns/pattern-side-output.md) | Data quality monitoring |
| CEP | [02-design-patterns/pattern-cep-complex-event.md](../Knowledge/02-design-patterns/pattern-cep-complex-event.md) | Fraud detection, security |
| Checkpoint Recovery | [02-design-patterns/pattern-checkpoint-recovery.md](../Knowledge/02-design-patterns/pattern-checkpoint-recovery.md) | Financial transactions |

### 03. Business Patterns

Industry-specific stream computing applications.

| Industry | Document | Chinese Path |
|----------|----------|-------------|
| Fintech | Real-time Risk Control | [03-business-patterns/fintech-realtime-risk-control.md](../Knowledge/03-business-patterns/fintech-realtime-risk-control.md) |
| E-commerce | Real-time Recommendation | [03-business-patterns/real-time-recommendation.md](../Knowledge/03-business-patterns/real-time-recommendation.md) |
| IoT | IoT Stream Processing | [03-business-patterns/iot-stream-processing.md](../Knowledge/03-business-patterns/iot-stream-processing.md) |
| Operations | Log Monitoring | [03-business-patterns/log-monitoring.md](../Knowledge/03-business-patterns/log-monitoring.md) |
| Gaming | Gaming Analytics | [03-business-patterns/gaming-analytics.md](../Knowledge/03-business-patterns/gaming-analytics.md) |

**Alibaba Double 11**:
- [alibaba-double11-flink.md](../Knowledge/03-business-patterns/alibaba-double11-flink.md) - Large-scale stream processing architecture

### 04. Technology Selection

Guides for choosing stream computing technologies.

| Guide | Chinese Path | Focus |
|-------|-------------|-------|
| Paradigm Selection | [04-technology-selection/paradigm-selection-guide.md](../Knowledge/04-technology-selection/paradigm-selection-guide.md) | Actor/CSP/Dataflow decision tree |
| Engine Selection | [04-technology-selection/engine-selection-guide.md](../Knowledge/04-technology-selection/engine-selection-guide.md) | Flink/Spark/Kafka Streams comparison |
| Streaming Database | [04-technology-selection/streaming-database-guide.md](../Knowledge/04-technology-selection/streaming-database-guide.md) | Materialize/RisingWave/Timeplus |
| Storage Selection | [04-technology-selection/storage-selection-guide.md](../Knowledge/04-technology-selection/storage-selection-guide.md) | State Backend and sink storage |

### 05. Mapping Guides

Theory-to-code and migration guides.

| Guide | Chinese Path | Purpose |
|-------|-------------|---------|
| Struct to Flink | [05-mapping-guides/struct-to-flink-mapping.md](../Knowledge/05-mapping-guides/struct-to-flink-mapping.md) | Theory concepts to Flink API mapping |
| Spark to Flink | [05-mapping-guides/migration-guides/05.1-spark-streaming-to-flink-migration.md](../Knowledge/05-mapping-guides/migration-guides/05.1-spark-streaming-to-flink-migration.md) | Migration guide |
| Kafka Streams to Flink | [05-mapping-guides/migration-guides/05.2-kafka-streams-to-flink-migration.md](../Knowledge/05-mapping-guides/migration-guides/05.2-kafka-streams-to-flink-migration.md) | DSL conversion |

### 06. Frontier Technologies

Emerging trends in stream computing.

#### Real-time AI & Agents
| Document | Chinese Path | Topic |
|----------|-------------|-------|
| AI Agent Streaming Architecture | [06-frontier/ai-agent-streaming-architecture.md](../Knowledge/06-frontier/ai-agent-streaming-architecture.md) | Stream computing driven agent workflows |
| MCP Protocol | [06-frontier/mcp-protocol-agent-streaming.md](../Knowledge/06-frontier/mcp-protocol-agent-streaming.md) | Model Context Protocol integration |
| A2A Protocol | [06-frontier/a2a-protocol-agent-communication.md](../Knowledge/06-frontier/a2a-protocol-agent-communication.md) | Agent-to-Agent communication |
| Real-time RAG | [06-frontier/real-time-rag-architecture.md](../Knowledge/06-frontier/real-time-rag-architecture.md) | Streaming knowledge base updates |

#### Streaming Databases
| Document | Chinese Path | Topic |
|----------|-------------|-------|
| Streaming Databases Overview | [06-frontier/streaming-databases.md](../Knowledge/06-frontier/streaming-databases.md) | Architecture and capabilities |
| RisingWave Deep Dive | [06-frontier/risingwave-deep-dive.md](../Knowledge/06-frontier/risingwave-deep-dive.md) | Architecture and best practices |
| Vector Search Convergence | [06-frontier/vector-search-streaming-convergence.md](../Knowledge/06-frontier/vector-search-streaming-convergence.md) | Real-time vector index updates |

#### Serverless & Cloud Native
| Document | Chinese Path | Topic |
|----------|-------------|-------|
| Serverless Streaming | [06-frontier/serverless-stream-processing-architecture.md](../Knowledge/06-frontier/serverless-stream-processing-architecture.md) | Elastic workloads and cost optimization |
| WebAssembly Dataflow | [06-frontier/wasm-dataflow-patterns.md](../Knowledge/06-frontier/wasm-dataflow-patterns.md) | WASM and stream computing |

### 07. Best Practices

Production environment guides.

| Practice | Chinese Path | Purpose |
|----------|-------------|---------|
| Production Checklist | [07-best-practices/07.01-flink-production-checklist.md](../Knowledge/07-best-practices/07.01-flink-production-checklist.md) | Pre-launch checklist |
| Performance Tuning | [07-best-practices/07.02-performance-tuning-patterns.md](../Knowledge/07-best-practices/07.02-performance-tuning-patterns.md) | Backpressure and serialization optimization |
| Troubleshooting | [07-best-practices/07.03-troubleshooting-guide.md](../Knowledge/07-best-practices/07.03-troubleshooting-guide.md) | Common issues diagnosis |
| Cost Optimization | [07-best-practices/07.04-cost-optimization-patterns.md](../Knowledge/07-best-practices/07.04-cost-optimization-patterns.md) | FinOps and cost reduction |
| Security Hardening | [07-best-practices/07.05-security-hardening-guide.md](../Knowledge/07-best-practices/07.05-security-hardening-guide.md) | Authentication and encryption |

### 09. Anti-Patterns

Common pitfalls and mitigation strategies.

| Anti-Pattern | Chinese Path | Issue |
|--------------|-------------|-------|
| Global State Abuse | [09-anti-patterns/anti-pattern-01-global-state-abuse.md](../Knowledge/09-anti-patterns/anti-pattern-01-global-state-abuse.md) | Concurrency safety |
| Watermark Misconfiguration | [09-anti-patterns/anti-pattern-02-watermark-misconfiguration.md](../Knowledge/09-anti-patterns/anti-pattern-02-watermark-misconfiguration.md) | Late data handling |
| Checkpoint Misconfig | [09-anti-patterns/anti-pattern-03-checkpoint-interval-misconfig.md](../Knowledge/09-anti-patterns/anti-pattern-03-checkpoint-interval-misconfig.md) | Fault tolerance design |
| Hot Key Skew | [09-anti-patterns/anti-pattern-04-hot-key-skew.md](../Knowledge/09-anti-patterns/anti-pattern-04-hot-key-skew.md) | Data distribution |
| Blocking IO in ProcessFunction | [09-anti-patterns/anti-pattern-05-blocking-io-processfunction.md](../Knowledge/09-anti-patterns/anti-pattern-05-blocking-io-processfunction.md) | Async design |

---

## Learning Paths

### By Role

**Architect**:
1. Concept Atlas → Technology Selection → Frontier Technologies

**Developer**:
1. Design Patterns → Best Practices → Anti-Patterns

**Data Engineer**:
1. Business Patterns → Mapping Guides → Case Studies

**Operations Engineer**:
1. Best Practices → Anti-Patterns → Standards

---

## Key Terms (English-Chinese)

| English | Chinese | Category |
|---------|---------|----------|
| Design Pattern | 设计模式 | Pattern |
| Anti-Pattern | 反模式 | Pattern |
| Event Time | 事件时间 | Time |
| Processing Time | 处理时间 | Time |
| Watermark | 水印 | Time |
| Checkpoint | 检查点 | Fault Tolerance |
| State Backend | 状态后端 | State |
| Side Output | 侧输出 | Pattern |
| CEP (Complex Event Processing) | 复杂事件处理 | Pattern |
| Streaming Database | 流数据库 | Technology |

---

## Cross-References

- [Struct/ Index](./STRUCT-INDEX.md) - Formal theory navigation
- [Flink/ Index](./FLINK-INDEX.md) - Flink-specific technology
- [Full Knowledge/ Index](../Knowledge/00-INDEX.md) - Complete Chinese navigation

---

*Last updated: 2026-04-12 | For full Chinese content, see [../Knowledge/00-INDEX.md](../Knowledge/00-INDEX.md)*
