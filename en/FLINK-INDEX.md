# Flink/ Technology - English Navigation

> **Document Position**: Flink/ English Content Index | **Version**: 2026.04 | **Status**: Index Only

---

## Overview

The **Flink/** directory contains Flink-specific technology documentation, including architecture design, core mechanisms, SQL/API guides, connectors, and engineering practices.

**Note**: Currently, Flink/ documents are primarily in Chinese. This index provides navigation to key Flink concepts with English summaries.

---

## Directory Structure

```
Flink/
├── 01-architecture/          # Architecture design
├── 02-core-mechanisms/       # Core mechanisms (Checkpoint, Watermark, etc.)
├── 03-sql-table-api/         # SQL and Table API
├── 04-connectors/            # Connector ecosystem
├── 05-vs-competitors/        # Competitor comparison
├── 06-engineering/           # Engineering practice
├── 08-roadmap/               # Roadmap and version tracking
├── 09-language-foundations/  # Multi-language foundations
├── 10-deployment/            # Deployment and operations
├── 11-benchmarking/          # Performance benchmarking
├── 12-ai-ml/                 # AI/ML integration
├── 13-security/              # Security and compliance
├── 14-lakehouse/             # Streaming Lakehouse
└── 15-observability/         # Observability
```

---

## Core Topics

### 01. Architecture

| Topic | Chinese Document | Description |
|-------|-----------------|-------------|
| Architecture Overview | [01-architecture/flink-architecture-evolution.md](../Flink/01-architecture/flink-architecture-evolution.md) | 1.x vs 2.x/3.0 architecture evolution |
| Storage-Compute Separation | [01-architecture/flink-storage-compute-separation.md](../Flink/01-architecture/flink-storage-compute-separation.md) | Cloud-native disaggregated architecture |
| Cloud-Native Design | [01-architecture/flink-cloud-native-deep-dive.md](../Flink/01-architecture/flink-cloud-native-deep-dive.md) | Kubernetes-native deployment |

### 02. Core Mechanisms

| Mechanism | Chinese Document | Key Concepts |
|-----------|-----------------|--------------|
| Checkpoint | [02-core-mechanisms/checkpoint-mechanism-deep-dive.md](../Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md) | Barrier alignment, exactly-once |
| State Backend | [02-core-mechanisms/state-backend-evolution-analysis.md](../Flink/02-core-mechanisms/state-backend-evolution-analysis.md) | Heap, RocksDB, remote state |
| Time & Watermark | [02-core-mechanisms/time-semantics-and-watermark.md](../Flink/02-core-mechanisms/time-semantics-and-watermark.md) | Event time, processing time |
| Network Stack | [02-core-mechanisms/network-stack-deep-dive.md](../Flink/02-core-mechanisms/network-stack-deep-dive.md) | Netty, credit-based flow control |
| Backpressure | [02-core-mechanisms/backpressure-and-flow-control.md](../Flink/02-core-mechanisms/backpressure-and-flow-control.md) | Backpressure propagation |

**Checkpoint Deep Dive**:
- **Barrier**: Special record triggering state snapshots
- **Alignment**: Synchronizing barriers across parallel instances
- **State Backend**: Storage mechanism for keyed and operator state
  - HeapKeyedStateBackend: In-memory, fast access
  - RocksDBKeyedStateBackend: Disk-based, larger state

### 03. SQL & Table API

| Topic | Chinese Document | Description |
|-------|-----------------|-------------|
| Table API Complete Guide | [03-sql-table-api/flink-table-sql-complete-guide.md](../Flink/03-sql-table-api/flink-table-sql-complete-guide.md) | Comprehensive SQL/Table API reference |
| SQL Optimization | [03-sql-table-api/flink-sql-optimization-guide.md](../Flink/03-sql-table-api/flink-sql-optimization-guide.md) | Query planning and optimization |
| UDF Development | [03-sql-table-api/flink-udf-development-guide.md](../Flink/03-sql-table-api/flink-udf-development-guide.md) | User-defined functions |

### 04. Connectors

| Connector | Chinese Document | Type |
|-----------|-----------------|------|
| Kafka | [04-connectors/kafka-integration-patterns.md](../Flink/04-connectors/kafka-integration-patterns.md) | Source/Sink |
| JDBC | [jdbc-connector-guide.md](../Flink/jdbc-connector-guide.md) | Sink |
| Elasticsearch | [elasticsearch-connector-guide.md](../Flink/elasticsearch-connector-guide.md) | Sink |
| MongoDB | [mongodb-connector-guide.md](../Flink/mongodb-connector-guide.md) | Source/Sink |
| Pulsar | [pulsar-functions-integration.md](../Flink/pulsar-functions-integration.md) | Source/Sink |

### 05. Competitor Comparison

| Comparison | Chinese Document | Focus |
|------------|-----------------|-------|
| Flink vs RisingWave | [05-vs-competitors/flink-vs-risingwave.md](../Flink/05-vs-competitors/flink-vs-risingwave.md) | Stream processor vs stream database |
| Flink vs Spark Streaming | [05-vs-competitors/flink-vs-spark-streaming.md](../Flink/05-vs-competitors/flink-vs-spark-streaming.md) | Latency and state management |
| Flink vs Kafka Streams | [05-vs-competitors/flink-vs-kafka-streams.md](../Flink/05-vs-competitors/flink-vs-kafka-streams.md) | Microservices vs analytics |

### 06. Engineering Practice

| Topic | Chinese Document | Purpose |
|-------|-----------------|---------|
| Production Checklist | [06-engineering/production-checklist.md](../Flink/06-engineering/production-checklist.md) | Pre-production validation |
| Performance Tuning | [06-engineering/performance-tuning-guide.md](../Flink/06-engineering/performance-tuning-guide.md) | Optimization strategies |
| Cost Optimization | [06-engineering/cost-optimization-patterns.md](../Flink/06-engineering/cost-optimization-patterns.md) | Resource efficiency |

### 10. Deployment

| Topic | Chinese Document | Platform |
|-------|-----------------|----------|
| Kubernetes Deployment | [10-deployment/kubernetes-deployment-production-guide.md](../Flink/10-deployment/kubernetes-deployment-production-guide.md) | K8s |
| Docker Compose | [10-deployment/docker-compose-setup.md](../Flink/10-deployment/docker-compose-setup.md) | Docker |
| Standalone | [10-deployment/standalone-deployment-guide.md](../Flink/10-deployment/standalone-deployment-guide.md) | Bare metal |

### 12. AI/ML Integration

| Topic | Chinese Document | Description |
|-------|-----------------|-------------|
| AI/ML Integration | [12-ai-ml/flink-ai-ml-integration-complete-guide.md](../Flink/12-ai-ml/flink-ai-ml-integration-complete-guide.md) | ML inference in streaming |
| FLIP-531 Agents | [12-ai-ml/flip-531-agent-streaming.md](../Flink/12-ai-ml/flip-531-agent-streaming.md) | Real-time graph streaming |
| TGN Integration | [12-ai-ml/temporal-graph-networks-streaming.md](../Flink/12-ai-ml/temporal-graph-networks-streaming.md) | Temporal Graph Networks |
| Multimodal Streaming | [12-ai-ml/multimodal-streaming-processing.md](../Flink/12-ai-ml/multimodal-streaming-processing.md) | Text/image/audio processing |

### 14. Lakehouse

| Topic | Chinese Document | Description |
|-------|-----------------|-------------|
| Streaming Lakehouse | [14-lakehouse/streaming-lakehouse-architecture.md](../Flink/14-lakehouse/streaming-lakehouse-architecture.md) | Iceberg/Delta integration |
| Flink + Iceberg | [14-lakehouse/flink-iceberg-integration.md](../Flink/14-lakehouse/flink-iceberg-integration.md) | Practical integration guide |
| Flink + Paimon | [14-lakehouse/flink-paimon-integration.md](../Flink/14-lakehouse/flink-paimon-integration.md) | Apache Paimon integration |

### 15. Observability

| Topic | Chinese Document | Description |
|-------|-----------------|-------------|
| Observability Complete | [15-observability/flink-observability-complete-guide.md](../Flink/15-observability/flink-observability-complete-guide.md) | Metrics, logs, traces |
| OpenTelemetry | [15-observability/flink-opentelemetry-integration.md](../Flink/15-observability/flink-opentelemetry-integration.md) | OTel integration |
| SLO Monitoring | [15-observability/flink-slo-monitoring.md](../Flink/15-observability/flink-slo-monitoring.md) | Service level objectives |

---

## Version Roadmap

| Version | Status | Key Features | Document |
|---------|--------|--------------|----------|
| Flink 2.0 | Released | Storage-compute separation, unified scheduler | [08-roadmap/flink-2.0-roadmap.md](../Flink/08-roadmap/flink-2.0-roadmap.md) |
| Flink 2.4 | Released | Checkpoint improvements, adaptive scheduler | [08-roadmap/flink-2.4-roadmap.md](../Flink/08-roadmap/flink-2.4-roadmap.md) |
| Flink 2.5 | Released | State backend evolution, SQL enhancements | [08-roadmap/flink-2.5-roadmap.md](../Flink/08-roadmap/flink-2.5-roadmap.md) |
| Flink 3.0 | Planned | Cloud-native redesign, ML-native | [08-roadmap/flink-3.0-roadmap.md](../Flink/08-roadmap/flink-3.0-roadmap.md) |

---

## Language Foundations

### Multi-Language Support

| Language | Chinese Document | Status |
|----------|-----------------|--------|
| Scala 3 | [09-language-foundations/scala-3-streaming-guide.md](../Flink/09-language-foundations/scala-3-streaming-guide.md) | Primary |
| Python (PyFlink) | [09-language-foundations/pyflink-deep-guide.md](../Flink/09-language-foundations/pyflink-deep-guide.md) | Full support |
| Rust | [09-language-foundations/rust-flink-native.md](../Flink/09-language-foundations/rust-flink-native.md) | Experimental |
| Go | [09-language-foundations/go-flink-client-guide.md](../Flink/09-language-foundations/go-flink-client-guide.md) | Client only |

---

## Key Concepts (English)

### Checkpointing
- **Distributed Snapshots**: Periodic consistent snapshots of distributed state
- **Barrier**: Special control record triggering state snapshots
- **Alignment**: Synchronizing barriers across parallel instances
- **Exactly-Once**: End-to-end exactly-once processing guarantee

### State Management
- **Keyed State**: State scoped to a specific key
- **Operator State**: State not associated with any key
- **State Backend**: Pluggable storage implementation
- **Queryable State**: Direct access to runtime state

### Time Semantics
- **Event Time**: Timestamp when event occurred (business time)
- **Processing Time**: Timestamp when event is processed (wall clock)
- **Ingestion Time**: Timestamp when event enters the system
- **Watermark**: Progress indicator for event time

### Windows
- **Tumbling Window**: Fixed-size, non-overlapping windows
- **Sliding Window**: Fixed-size, overlapping windows
- **Session Window**: Dynamic windows by activity gaps
- **Global Window**: Single window for all data

---

## Benchmarking

| Benchmark | Chinese Document | Description |
|-----------|-----------------|-------------|
| NexMark | [11-benchmarking/flink-nexmark-benchmark-guide.md](../Flink/11-benchmarking/flink-nexmark-benchmark-guide.md) | Standard streaming benchmark suite |
| YCSB | [11-benchmarking/flink-ycsb-benchmark-guide.md](../Flink/11-benchmarking/flink-ycsb-benchmark-guide.md) | Yahoo Cloud Serving Benchmark |
| Performance Suite | [11-benchmarking/flink-performance-benchmark-suite.md](../Flink/11-benchmarking/flink-performance-benchmark-suite.md) | Comprehensive performance tests |

---

## Cross-References

- [Struct/ Index](./STRUCT-INDEX.md) - Formal theory navigation
- [Knowledge/ Index](./KNOWLEDGE-INDEX.md) - Engineering practice navigation
- [Full Flink/ Index](../Flink/00-FLINK-TECH-STACK-DEPENDENCY.md) - Complete Chinese navigation

---

*Last updated: 2026-04-12 | For full Chinese content, see [../Flink/](../Flink/)*
