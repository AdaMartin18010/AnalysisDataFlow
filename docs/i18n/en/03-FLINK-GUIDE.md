---
title: "Flink/ Directory Guide - Flink-Specific Technology"
source_file: "Flink/00-INDEX.md"
source_version: "v3.3.0"
translation_status: "completed"
completion_percentage: 100
language: "en"
last_sync: "2026-04-08T09:52:41Z"
---

# Flink/ Flink-Specific Technology Guide

> **Document Position**: Flink Technology Navigation Index | **Version**: 2026.04 | **Status**: Active Maintenance
>
> 🌐 **中文版** | **English Version**

---

## Introduction

The **Flink/** directory contains Flink-specific technology documents, covering architecture design, core mechanisms, SQL/API, engineering practices, AI/ML integration, and other full-stack content. This directory is the core implementation layer of the project, mapping formal theories from `Struct/` and design patterns from `Knowledge/` to Flink-specific implementations.

**Core Positioning**:

- 🏗️ **Architecture Design**: Flink 1.x vs 2.x/3.0 evolution, storage-compute separation, cloud-native
- ⚙️ **Core Mechanisms**: Checkpoint, Exactly-Once, Watermark, backpressure
- 💻 **SQL & Table API**: Flink SQL, Table API, UDF development
- 🔌 **Connector Ecosystem**: Kafka, CDC, Paimon, Iceberg integration
- ⚔️ **Competitor Comparison**: Flink vs Spark, RisingWave, Kafka Streams
- 🛠️ **Engineering Practices**: Cost optimization, testing strategies, performance tuning
- 🤖 **AI/ML Integration**: AI Agents, TGN, multimodal processing
- ☁️ **Deployment & Operations**: Kubernetes, Serverless, cloud provider integration

---

## Directory Structure

```
Flink/
├── 01-architecture/           # Architecture Design (8 documents)
├── 02-core-mechanisms/        # Core Mechanisms (12 documents)
├── 03-sql-table-api/          # SQL and Table API (10 documents)
├── 04-connectors/             # Connector Ecosystem (15 documents)
├── 05-vs-competitors/         # Competitor Comparison (8 documents)
├── 06-engineering/            # Engineering Practices (10 documents)
├── 07-case-studies/           # Case Studies (12 documents)
├── 08-roadmap/                # Roadmaps (6 documents)
├── 09-language-foundations/   # Multi-language Foundations (8 documents)
├── 10-deployment/             # Deployment and Operations (10 documents)
├── 11-benchmarking/           # Performance Benchmarking (5 documents)
├── 12-ai-ml/                  # AI/ML Integration (15 documents)
├── 13-security/               # Security and Compliance (5 documents)
├── 14-lakehouse/              # Streaming Lakehouse (6 documents)
└── 15-observability/          # Observability (8 documents)
```

---

## 01. Architecture Design

Flink system architecture, evolution, and design principles.

| Document | Description | Key Points |
|----------|-------------|------------|
| [01.01-flink-1.x-vs-2.x-architecture.md](../../../Flink/01-concepts/flink-1.x-vs-2.0-comparison.md) | Flink 1.x vs 2.x Architecture Comparison | Storage-compute separation, unified batch-streaming scheduler |
| [01.02-flink-3.0-vision.md](../../../Flink/08-roadmap/flink-2.4-2.5-3.0-tracking.md) | Flink 3.0 Vision and Architecture | Next-generation architecture, cloud-native deep integration |
| [01.03-disaggregated-storage.md](../../../Flink/01-concepts/disaggregated-state-analysis.md) | Disaggregated Storage Architecture | Remote state storage, tiered storage strategies |
| [01.04-cloud-native-deep-dive.md](../../../Flink/03-flink-23/flink-23-cloud-native.md) | Cloud-Native Deep Dive | Kubernetes-native design, elastic scaling |
| [01.05-adaptive-scheduler.md](../../../Flink/03-flink-23/flink-23-adaptive-scheduler.md) | Adaptive Scheduler | Dynamic resource allocation, auto-parallelism adjustment |
| [01.06-resource-management.md](../../../Flink/10-internals/memory-management-internals.md) | Resource Management | Slot allocation, resource scheduling strategies |
| [01.07-network-stack.md](../../../Flink/02-core/network-stack-evolution.md) | Network Stack Deep Dive | Credit-based flow control, buffer management |
| [01.08-memory-management.md](../../../Flink/10-internals/memory-management-internals.md) | Memory Management | Managed memory, off-heap memory, GC optimization |

---

## 02. Core Mechanisms

Flink's core runtime mechanisms and implementation principles.

| Document | Description | Key Points |
|----------|-------------|------------|
| [02.01-checkpoint-mechanism.md](../../../Flink/02-core/checkpoint-mechanism-deep-dive.md) | Checkpoint Mechanism Deep Dive | Barrier alignment, incremental checkpoint, exactly-once |
| [02.02-exactly-once-semantics.md](../../../Flink/02-core/exactly-once-semantics-deep-dive.md) | Exactly-Once Semantics | End-to-end consistency, 2PC protocol implementation |
| [02.03-time-semantics-watermark.md](../../../Flink/02-core/time-semantics-and-watermark.md) | Time Semantics and Watermark | Event time, processing time, ingestion time, Watermark propagation |
| [02.04-state-backends.md](../../../Flink/02-core/state-backends-deep-comparison.md) | State Backends Deep Dive | HashMapStateBackend, RocksDBStateBackend comparison |
| [02.05-backpressure-flow-control.md](../../../Flink/02-core/backpressure-and-flow-control.md) | Backpressure and Flow Control | Credit-based backpressure, dynamic buffer expansion |
| [02.06-fault-tolerance-recovery.md] | Fault Tolerance and Recovery | Failure detection, automatic restart, local recovery |
| [02.07-savepoint-operations.md] | Savepoint Operations | State migration, version upgrade, application evolution |
| [02.08-broadcast-state.md] | Broadcast State Pattern | Rule updates, configuration broadcasting |
| [02.09-queryable-state.md] | Queryable State | Real-time state queries, operational analytics |
| [02.10-side-outputs.md] | Side Outputs | Late data handling, multi-stream output |
| [02.11-async-checkpointing.md](../../../Flink/02-core/smart-checkpointing-strategies.md) | Asynchronous Checkpointing | Non-blocking checkpoints, performance optimization |
| [02.12-state-ttl.md](../../../Flink/02-core/flink-state-ttl-best-practices.md) | State TTL Management | Automatic state expiration, cleanup strategies |

---

## 03. SQL and Table API

Flink SQL, Table API, and declarative stream processing.

| Document | Description | Key Points |
|----------|-------------|------------|
| [03.01-flink-sql-overview.md](../../../Flink/03-api/03.02-table-sql-api/flink-table-sql-complete-guide.md) | Flink SQL Overview | SQL capabilities, streaming SQL semantics |
| [03.02-table-api-guide.md](../../../Flink/03-api/03.02-table-sql-api/flink-table-sql-complete-guide.md) | Table API Programming Guide | Table API usage, DataStream-Table conversion |
| [03.03-window-functions.md](../../../Flink/03-api/03.02-table-sql-api/flink-sql-window-functions-deep-dive.md) | Window Functions | TUMBLE, HOP, SESSION, CUMULATE windows |
| [03.04-udfs-development.md](../../../Flink/03-api/03.02-table-sql-api/flink-python-udf.md) | UDF Development | Scalar, table, aggregate UDF implementation |
| [03.05-sql-optimization.md](../../../Flink/03-api/03.02-table-sql-api/query-optimization-analysis.md) | SQL Optimization | Query optimization, execution plan analysis |
| [03.06-dynamic-tables.md](../../../Flink/03-api/03.02-table-sql-api/materialized-tables.md) | Dynamic Tables | Changelog streams, materialized views |
| [03.07-pattern-recognition.md](../../../Flink/03-api/03.02-table-sql-api/flink-cep-complete-guide.md) | Pattern Recognition (MATCH_RECOGNIZE) | CEP in SQL, complex event matching |
| [03.08-sql-client.md] | SQL Client | Interactive SQL, script execution |
| [03.09-catalogs.md] | Catalogs and Metadata | Hive catalog, JDBC catalog, custom catalogs |
| [03.10-sql-gateway.md] | SQL Gateway | REST API, multi-client support |

---

## 04. Connectors

Flink connector ecosystem and data integration.

| Document | Description | Key Points |
|----------|-------------|------------|
| [04.01-kafka-connector.md](../../../Flink/05-ecosystem/05.01-connectors/evolution/kafka-connector.md) | Kafka Connector | Producer, consumer, exactly-once integration |
| [04.02-filesystem-connector.md](../../../Flink/05-ecosystem/05.01-connectors/evolution/file-connector.md) | Filesystem Connector | Parquet, ORC, CSV, streaming file sink |
| [04.03-jdbc-connector.md](../../../Flink/05-ecosystem/05.01-connectors/evolution/jdbc-connector.md) | JDBC Connector | Database read/write, batch optimization |
| [04.04-elasticsearch-connector.md](../../../Flink/05-ecosystem/05.01-connectors/elasticsearch-connector-complete-guide.md) | Elasticsearch Connector | Real-time indexing, bulk operations |
| [04.05-cdc-connectors.md](../../../Flink/05-ecosystem/05.01-connectors/flink-cdc-3.0-data-integration.md) | CDC Connectors | Debezium, Canal, change data capture |
| [04.06-pulsar-connector.md](../../../Flink/05-ecosystem/05.01-connectors/pulsar-integration-guide.md) | Pulsar Connector | Tiered storage, multi-tenancy integration |
| [04.07-rabbitmq-connector.md](../../../Flink/05-ecosystem/05.01-connectors/evolution/mq-connector.md) | RabbitMQ Connector | AMQP integration, queue semantics |
| [04.08-kinesis-connector.md] | Kinesis Connector | AWS Kinesis, serverless streaming |
| [04.09-paimon-connector.md](../../../Flink/05-ecosystem/05.01-connectors/flink-paimon-integration.md) | Apache Paimon Connector | Lakehouse streaming, incremental processing |
| [04.10-iceberg-connector.md](../../../Flink/05-ecosystem/05.01-connectors/flink-iceberg-integration.md) | Apache Iceberg Connector | Time travel, schema evolution |
| [04.11-hudi-connector.md] | Apache Hudi Connector | Upsert streams, incremental views |
| [04.12-delta-connector.md](../../../Flink/05-ecosystem/05.01-connectors/flink-delta-lake-integration.md) | Delta Lake Connector | ACID transactions, streaming writes |
| [04.13-custom-connector.md](../../../Flink/05-ecosystem/05.01-connectors/evolution/custom-connector.md) | Custom Connector Development | Source/Sink API, implementation guide |
| [04.14-connector-best-practices.md](../../../Flink/05-ecosystem/05.01-connectors/flink-connectors-ecosystem-complete-guide.md) | Connector Best Practices | Configuration tuning, fault handling |
| [04.15-schema-registry.md] | Schema Registry Integration | Avro, Protobuf, schema evolution |

---

## 05. Competitor Comparison

Flink comparison with other stream processing engines.

| Document | Description | Key Points |
|----------|-------------|------------|
| [05.01-flink-vs-spark-streaming.md](../../../Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-spark-streaming.md) | Flink vs Spark Streaming | Architecture, latency, throughput comparison |
| [05.02-flink-vs-kafka-streams.md](../../../Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-kafka-streams.md) | Flink vs Kafka Streams | Use case fit, complexity, ecosystem |
| [05.03-flink-vs-storm.md] | Flink vs Apache Storm | Legacy comparison, migration path |
| [05.04-flink-vs-risingwave.md](../../../Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-risingwave-deep-dive.md) | Flink vs RisingWave | Stream processing vs stream database |
| [05.05-flink-vs-materialize.md](../../../Flink/05-ecosystem/ecosystem/materialize-comparison.md) | Flink vs Materialize | SQL-first streaming comparison |
| [05.06-engine-selection-guide.md] | Stream Engine Selection Guide | Decision matrix, use case mapping |
| [05.07-migration-guide-spark-to-flink.md](../../../Knowledge/05-mapping-guides/migration-guides/05.2-kafka-streams-to-flink-migration.md) | Spark to Flink Migration | Code conversion, semantic mapping |
| [05.08-hybrid-architectures.md](../../../Flink/07-rust-native/risingwave-comparison/04-hybrid-deployment.md) | Hybrid Architectures | Multi-engine coexistence patterns |

---

## 06. Engineering Practices

Production engineering practices and operational guidelines.

| Document | Description | Key Points |
|----------|-------------|------------|
| [06.01-performance-tuning.md](../../../Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md) | Performance Tuning Guide | Backpressure optimization, serialization tuning |
| [06.02-production-checklist.md](../../../Knowledge/07-best-practices/07.01-flink-production-checklist.md) | Production Checklist | Pre-launch verification, monitoring setup |
| [06.03-testing-strategies.md](../../../Flink/09-practices/09.03-performance-tuning/stream-processing-testing-strategies.md) | Testing Strategies | Unit testing, integration testing, chaos engineering |
| [06.04-monitoring-alerting.md](../../../Flink/04-runtime/04.03-observability/metrics-and-monitoring.md) | Monitoring and Alerting | Metrics, logs, tracing, alert rules |
| [06.05-cost-optimization.md](../../../Flink/09-practices/09.03-performance-tuning/flink-tco-cost-optimization-guide.md) | Cost Optimization | Resource right-sizing, spot instances |
| [06.06-ci-cd-pipelines.md] | CI/CD Pipelines | Automated testing, deployment automation |
| [06.07-config-management.md](../../../Flink/04-runtime/04.01-deployment/evolution/config-management.md) | Configuration Management | Dynamic config, environment separation |
| [06.08-version-upgrades.md](../../../Flink/00-meta/version-tracking.md) | Version Upgrade Guide | Migration strategies, compatibility testing |
| [06.09-disaster-recovery.md] | Disaster Recovery | Multi-region deployment, backup strategies |
| [06.10-security-hardening.md](../../../Flink/09-practices/09.04-security/flink-security-complete-guide.md) | Security Hardening | Authentication, encryption, network policies |

---

## 07. Case Studies

Real-world Flink production case studies.

| Document | Description | Industry |
|----------|-------------|----------|
| [07.01-alibaba-double11.md] | Alibaba Double 11 | E-commerce |
| [07.02-netflix-streaming.md] | Netflix Real-time Processing | Video Streaming |
| [07.03-uber-marketplace.md] | Uber Marketplace Platform | Mobility |
| [07.04-linkedin-analytics.md](../../../Flink/09-practices/09.01-case-studies/case-realtime-analytics.md) | LinkedIn Real-time Analytics | Social Network |
| [07.05-airbnb-search.md] | Airbnb Search Ranking | Travel |
| [07.06-stripe-fraud-detection.md](../../../Flink/09-practices/09.01-case-studies/case-fraud-detection-advanced.md) | Stripe Fraud Detection | Fintech |
| [07.07-spotify-recommendations.md](../../../Flink/09-practices/09.01-case-studies/case-ecommerce-realtime-recommendation.md) | Spotify Recommendations | Music |
| [07.08-lyft-rider-platform.md] | Lyft Rider Platform | Mobility |
| [07.09-pinterest-analytics.md](../../../Flink/09-practices/09.01-case-studies/case-realtime-analytics.md) | Pinterest Analytics | Social Media |
| [07.10-tencent-gaming.md](../../../Flink/09-practices/09.01-case-studies/case-gaming-realtime-analytics.md) | Tencent Gaming Analytics | Gaming |
| [07.11-bytedance-content.md] | ByteDance Content Recommendation | Content |
| [07.12-comcast-video.md] | Comcast Video Analytics | Media |

---

## 08. Roadmaps

Flink version roadmaps and feature tracking.

| Document | Description | Key Points |
|----------|-------------|------------|
| [08.01-flink-1.18-roadmap.md](../../../Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md) | Flink 1.18 Roadmap | Latest stable features |
| [08.02-flink-1.19-roadmap.md](../../../Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md) | Flink 1.19 Roadmap | Upcoming features |
| [08.03-flink-2.0-preview.md](../../../Flink/08-roadmap/08.01-flink-24/flink-2.5-preview.md) | Flink 2.0 Preview | Next-generation architecture |
| [08.04-flink-3.0-vision.md](../../../Flink/08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md) | Flink 3.0 Vision | Long-term vision |
| [08.05-flip-tracking.md](../../../Flink/08-roadmap/08.01-flink-24/FLIP-TRACKING-SYSTEM.md) | FLIP Tracking | Feature proposal tracking |
| [08.06-community-update.md](../../../Flink/08-roadmap/08.01-flink-24/community-dynamics-tracking.md) | Community Update | Contribution guidelines, events |

---

## 09. Multi-language Foundations

Flink's multi-language support and development.

| Document | Description | Language |
|----------|-------------|----------|
| [09.01-java-development.md](../../../Flink/03-api/09-language-foundations/02.01-java-api-from-scala.md) | Java Development Guide | Java |
| [09.02-scala-development.md](../../../Flink/03-api/09-language-foundations/01.01-scala-types-for-streaming.md) | Scala Development Guide | Scala |
| [09.03-python-pyflink.md](../../../Flink/03-api/09-language-foundations/pyflink-complete-guide.md) | PyFlink Guide | Python |
| [09.04-sql-development.md](../../../Flink/03-api/03.02-table-sql-api/flink-table-sql-complete-guide.md) | SQL Development Guide | SQL |
| [09.05-go-sdk-preview.md] | Go SDK Preview | Go |
| [09.06-rust-udf.md](../../../Flink/03-api/09-language-foundations/03-rust-native.md) | Rust UDF Development | Rust |
| [09.07-wasm-udf.md](../../../Flink/03-api/09-language-foundations/09-wasm-udf-frameworks.md) | WebAssembly UDF | WASM |
| [09.08-language-comparison.md](../../../Flink/03-api/09-language-foundations/flink-language-support-complete-guide.md) | Language Comparison | All |

---

## 10. Deployment and Operations

Flink deployment options and operational practices.

| Document | Description | Environment |
|----------|-------------|-------------|
| [10.01-local-setup.md] | Local Development Setup | Local |
| [10.02-standalone-cluster.md](../../../Flink/04-runtime/04.01-deployment/evolution/standalone-deploy.md) | Standalone Cluster | On-premise |
| [10.03-kubernetes-operator.md](../../../Flink/04-runtime/04.01-deployment/flink-kubernetes-operator-deep-dive.md) | Kubernetes Operator | K8s |
| [10.04-docker-deployment.md](../../../Flink/04-runtime/04.01-deployment/kubernetes-deployment.md) | Docker Deployment | Container |
| [10.05-aws-integration.md] | AWS Integration | AWS |
| [10.06-gcp-integration.md] | GCP Integration | GCP |
| [10.07-azure-integration.md] | Azure Integration | Azure |
| [10.08-alibaba-cloud-integration.md] | Alibaba Cloud Integration | Alibaba Cloud |
| [10.09-serverless-flink.md](../../../Flink/04-runtime/04.01-deployment/serverless-flink-ga-guide.md) | Serverless Flink | Serverless |
| [10.10-high-availability.md](../../../Flink/04-runtime/04.01-deployment/evolution/ha-evolution.md) | High Availability Setup | Production |

---

## 11. Performance Benchmarking

Flink performance testing and benchmarking.

| Document | Description | Focus |
|----------|-------------|-------|
| [11.01-nexmark-benchmark.md](../../../Flink/09-practices/09.02-benchmarking/nexmark-2026-benchmark.md) | Nexmark Benchmark | Standard SQL benchmark |
| [11.02-custom-benchmarks.md](../../../Flink/09-practices/09.02-benchmarking/streaming-benchmarks.md) | Custom Benchmarks | Domain-specific testing |
| [11.03-latency-throughput.md](../../../Flink/09-practices/09.02-benchmarking/performance-benchmarking-guide.md) | Latency vs Throughput | Trade-off analysis |
| [11.04-state-access-performance.md](../../../Flink/02-core/state-backends-deep-comparison.md) | State Access Performance | State backend comparison |
| [11.05-serialization-benchmarks.md](../../../Flink/10-internals/serialization-internals.md) | Serialization Benchmarks | Serializer comparison |

---

## 12. AI/ML Integration

Flink integration with AI/ML workloads.

| Document | Description | Focus |
|----------|-------------|-------|
| [12.01-ml-inference-streaming.md](../../../Flink/06-ai-ml/flink-realtime-ml-inference.md) | ML Inference in Streaming | Real-time model serving |
| [12.02-feature-engineering.md](../../../Flink/06-ai-ml/realtime-feature-engineering-guide.md) | Feature Engineering | Real-time feature computation |
| [12.03-flink-ai-flow.md](../../../Flink/06-ai-ml/flink-ai-ml-integration-complete-guide.md) | Flink AI Flow | ML pipeline orchestration |
| [12.04-tensorflow-integration.md] | TensorFlow Integration | TensorFlow + Flink |
| [12.05-pytorch-integration.md] | PyTorch Integration | PyTorch + Flink |
| [12.06-online-learning.md](../../../Flink/06-ai-ml/online-learning-algorithms.md) | Online Learning | Incremental model updates |
| [12.07-model-serving.md](../../../Flink/06-ai-ml/model-serving-streaming.md) | Model Serving Patterns | Low-latency inference |
| [12.08-flip-531-ai-agents.md](../../../Flink/06-ai-ml/flink-ai-agents-flip-531.md) | FLIP-531 AI Agents | Flink AI Agents proposal |
| [12.09-multimodal-streaming.md](../../../Flink/06-ai-ml/llm-streaming-inference-architecture.md) | Multimodal Streaming | Text/image/video processing |
| [12.10-graph-neural-networks.md] | Graph Neural Networks | TGN, TGNN integration |
| [12.11-vector-search-integration.md](../../../Flink/06-ai-ml/vector-database-integration.md) | Vector Search Integration | RAG, vector databases |
| [12.12-llm-pipeline.md](../../../Flink/06-ai-ml/flink-llm-integration.md) | LLM Pipeline | Large language model workflows |
| [12.13-mlflow-integration.md] | MLflow Integration | ML experiment tracking |
| [12.14-kubeflow-integration.md] | Kubeflow Integration | K8s-native ML pipelines |
| [12.15-ai-ops.md] | AIOps | Intelligent operations |

---

## 13. Security and Compliance

Flink security features and compliance practices.

| Document | Description | Focus |
|----------|-------------|-------|
| [13.01-authentication.md](../../../Flink/09-practices/09.04-security/security/evolution/auth-evolution.md) | Authentication | Kerberos, OAuth, JWT |
| [13.02-authorization.md](../../../Flink/09-practices/09.04-security/security/evolution/authorization-evolution.md) | Authorization | RBAC, ACLs |
| [13.03-data-encryption.md](../../../Flink/09-practices/09.04-security/security/evolution/encryption-evolution.md) | Data Encryption | TLS, encryption at rest |
| [13.04-audit-logging.md](../../../Flink/09-practices/09.04-security/security/evolution/audit-evolution.md) | Audit Logging | Compliance logging |
| [13.05-gdpr-compliance.md](../../../Flink/09-practices/09.04-security/security/evolution/compliance-evolution.md) | GDPR Compliance | Data privacy, right to be forgotten |

---

## 14. Streaming Lakehouse

Flink integration with Lakehouse architectures.

| Document | Description | Focus |
|----------|-------------|-------|
| [14.01-lakehouse-overview.md](../../../Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-architecture.md) | Lakehouse Overview | Architecture concepts |
| [14.02-paimon-deep-dive.md](../../../Flink/05-ecosystem/05.02-lakehouse/flink-paimon-integration.md) | Apache Paimon Deep Dive | Streaming lakehouse format |
| [14.03-iceberg-integration.md](../../../Flink/05-ecosystem/05.02-lakehouse/flink-iceberg-integration.md) | Iceberg Integration | Time travel, schema evolution |
| [14.04-delta-integration.md](../../../Flink/05-ecosystem/05.01-connectors/flink-delta-lake-integration.md) | Delta Lake Integration | ACID transactions |
| [14.05-hudi-integration.md] | Hudi Integration | Upsert streams |
| [14.06-lakehouse-best-practices.md](../../../Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-deep-dive-2026.md) | Lakehouse Best Practices | Design patterns |

---

## 15. Observability

Flink observability and monitoring.

| Document | Description | Focus |
|----------|-------------|-------|
| [15.01-metrics-system.md](../../../Flink/04-runtime/04.03-observability/metrics-and-monitoring.md) | Metrics System | Built-in metrics, custom metrics |
| [15.02-opentelemetry-integration.md](../../../Flink/04-runtime/04.03-observability/opentelemetry-streaming-observability.md) | OpenTelemetry Integration | Distributed tracing |
| [15.03-logging-best-practices.md](../../../Flink/04-runtime/04.03-observability/evolution/logging-evolution.md) | Logging Best Practices | Structured logging, log aggregation |
| [15.04-slo-definition.md](../../../Flink/04-runtime/04.03-observability/streaming-metrics-monitoring-slo.md) | SLO Definition | Service level objectives |
| [15.05-alerting-strategies.md](../../../Flink/04-runtime/04.03-observability/evolution/alerting-evolution.md) | Alerting Strategies | Alert rules, incident response |
| [15.06-dashboard-creation.md](../../../Flink/04-runtime/04.03-observability/flink-observability-complete-guide.md) | Dashboard Creation | Grafana, Prometheus |
| [15.07-debugging-techniques.md](../../../Flink/09-practices/09.06-debugging/source-code-debugging.md) | Debugging Techniques | Local debugging, remote debugging |
| [15.08-profiling-tools.md](../../../Flink/04-runtime/04.03-observability/evolution/profiling-evolution.md) | Profiling Tools | CPU profiling, memory profiling |

---

## Navigation Links

**Root Directory Indexes**:

- [📁 Project Root](../../../README.md) — Project Overview
- [📋 AGENTS.md](../../../AGENTS.md) — Agent Work Context
- [🗺️ NAVIGATION-INDEX.md](../../../NAVIGATION-INDEX.md) — Global Navigation

**Other Core Indexes**:

- [📐 Struct/Index](../../../Struct/00-INDEX.md) — Formal Theory
- [📚 Knowledge/Index](../../../Knowledge/00-INDEX.md) — Knowledge Structure

**Learning Resources**:

- [🎓 LEARNING-PATH-GUIDE.md](../../../LEARNING-PATH-GUIDE.md) — Learning Paths
- [🧮 GLOSSARY.md](../../../GLOSSARY.md) — Glossary (Chinese)
- [🧮 GLOSSARY-EN.md](../../../GLOSSARY-EN.md) — Glossary (English)

---

> **Document Specification**: This document follows the six-section template in [AGENTS.md](../../../AGENTS.md)
> **Last Updated**: 2026-04-08
