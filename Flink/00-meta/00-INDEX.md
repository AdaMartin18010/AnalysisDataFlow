# Flink 专项文档导航索引

> 所属阶段: Flink/ | 前置依赖: [项目根目录](../../Knowledge/09-anti-patterns/README.md) | 状态: 持续更新

本文档是 **AnalysisDataFlow** 项目中 Flink 专项知识库的主索引，涵盖了从架构设计到生产实践的完整内容体系。

---

## 🚀 快速入门

| 文档 | 描述 | 版本 |
|------|------|------|
| [00-QUICK-START.md](00-QUICK-START.md) | Flink 快速入门指南：环境搭建、第一个程序、核心概念速览 | 1.17+ |

---

## 📚 核心模块索引

### 01. 架构设计 (Architecture)

| 文档 | 描述 | 版本 |
|------|------|------|
| [01-concepts/datastream-v2-semantics.md](../01-concepts/datastream-v2-semantics.md) | DataStream V2 API 语义设计与演进 | 1.19+ |
| [01-concepts/deployment-architectures.md](../01-concepts/deployment-architectures.md) | Flink 部署架构全解析：Standalone、YARN、K8s | 1.17+ |
| [01-concepts/disaggregated-state-analysis.md](../01-concepts/disaggregated-state-analysis.md) | 分离式状态存储架构深度分析 | 2.0+ |
| [01-concepts/flink-1.x-vs-2.0-comparison.md](../01-concepts/flink-1.x-vs-2.0-comparison.md) | Flink 1.x 与 2.0 架构对比分析 | 1.18 - 2.0 |

---

### 02. 核心机制 (Core Mechanisms) ⭐

> **核心模块**：Checkpoint、状态管理、时间语义、容错机制等 Flink 核心概念

#### Checkpoint 与容错

| 文档 | 描述 | 版本 |
|------|------|------|
| [02-core/checkpoint-mechanism-deep-dive.md](../02-core/checkpoint-mechanism-deep-dive.md) | Checkpoint 机制深度解析：Barrier、对齐、异步快照 | 1.17+ |
| [02-core/exactly-once-semantics-deep-dive.md](../02-core/exactly-once-semantics-deep-dive.md) | Exactly-Once 语义实现原理详解 | 1.17+ |
| [02-core/exactly-once-end-to-end.md](../02-core/exactly-once-end-to-end.md) | 端到端 Exactly-Once 实现指南 | 1.17+ |
| [02-core/smart-checkpointing-strategies.md](../02-core/smart-checkpointing-strategies.md) | 智能 Checkpoint 策略优化 | 1.18+ |

#### 状态管理

| 文档 | 描述 | 版本 |
|------|------|------|
| [02-core/flink-state-management-complete-guide.md](../02-core/flink-state-management-complete-guide.md) | 状态管理完整指南：类型、操作、TTL | 1.17+ |
| [02-core/flink-state-ttl-best-practices.md](../02-core/flink-state-ttl-best-practices.md) | 状态 TTL 最佳实践 | 1.17+ |
| [02-core/state-backends-deep-comparison.md](../02-core/state-backends-deep-comparison.md) | State Backend 深度对比：Memory、FsState、RocksDB | 1.17+ |
| [02-core/forst-state-backend.md](../02-core/forst-state-backend.md) | ForSt State Backend（Flink 2.0 新后端） | 2.0+ |
| [02-core/flink-2.0-forst-state-backend.md](../02-core/flink-2.0-forst-state-backend.md) | Flink 2.0 ForSt 后端详解 | 2.0+ |

#### 时间与 Watermark

| 文档 | 描述 | 版本 |
|------|------|------|
| [02-core/time-semantics-and-watermark.md](../02-core/time-semantics-and-watermark.md) | 时间语义与 Watermark 机制详解 | 1.17+ |

#### 执行模型与优化

| 文档 | 描述 | 版本 |
|------|------|------|
| [02-core/async-execution-model.md](../02-core/async-execution-model.md) | 异步执行模型设计 | 1.18+ |
| [02-core/flink-2.0-async-execution-model.md](../02-core/flink-2.0-async-execution-model.md) | Flink 2.0 异步执行模型 | 2.0+ |
| [02-core/adaptive-execution-engine-v2.md](../02-core/adaptive-execution-engine-v2.md) | 自适应执行引擎 V2 | 1.18+ |
| [02-core/backpressure-and-flow-control.md](../02-core/backpressure-and-flow-control.md) | 背压与流量控制机制 | 1.17+ |
| [02-core/multi-way-join-optimization.md](../02-core/multi-way-join-optimization.md) | 多路 Join 优化策略 | 1.18+ |
| [02-core/delta-join.md](../02-core/delta-join.md) | Delta Join 原理与实现 | 1.19+ |
| [02-core/delta-join-production-guide.md](../02-core/delta-join-production-guide.md) | Delta Join 生产实践指南 | 1.19+ |
| [02-core/streaming-etl-best-practices.md](../02-core/streaming-etl-best-practices.md) | 流式 ETL 最佳实践 | 1.17+ |
| [02-core/flink-2.2-frontier-features.md](../02-core/flink-2.2-frontier-features.md) | Flink 2.2 前沿特性预览 | 2.2+ |

---

### 03. SQL 与 Table API

| 文档 | 描述 | 版本 |
|------|------|------|
| [03-api/03.02-table-sql-api/flink-table-sql-complete-guide.md](../03-api/03.02-table-sql-api/flink-table-sql-complete-guide.md) | Table API & SQL 完整指南 | 1.17+ |
| [03-api/03.02-table-sql-api/flink-sql-window-functions-deep-dive.md](../03-api/03.02-table-sql-api/flink-sql-window-functions-deep-dive.md) | SQL 窗口函数深度解析 | 1.17+ |
| [03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md](../03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md) | Calcite 优化器深度解析 | 1.17+ |
| [03-api/03.02-table-sql-api/flink-sql-hints-optimization.md](../03-api/03.02-table-sql-api/flink-sql-hints-optimization.md) | SQL Hints 优化技巧 | 1.18+ |
| [03-api/03.02-table-sql-api/flink-process-table-functions.md](../03-api/03.02-table-sql-api/flink-process-table-functions.md) | Process Table Functions 详解 | 1.18+ |
| [03-api/03.02-table-sql-api/flink-cep-complete-guide.md](../03-api/03.02-table-sql-api/flink-cep-complete-guide.md) | CEP（复杂事件处理）完整指南 | 1.17+ |
| [03-api/03.02-table-sql-api/flink-materialized-table-deep-dive.md](../03-api/03.02-table-sql-api/flink-materialized-table-deep-dive.md) | 物化表深度解析 | 1.20+ |
| [03-api/03.02-table-sql-api/materialized-tables.md](../03-api/03.02-table-sql-api/materialized-tables.md) | 物化表使用指南 | 1.20+ |
| [03-api/03.02-table-sql-api/ansi-sql-2023-compliance-guide.md](../03-api/03.02-table-sql-api/ansi-sql-2023-compliance-guide.md) | ANSI SQL 2023 兼容性指南 | 1.19+ |
| [03-api/03.02-table-sql-api/built-in-functions-complete-list.md](../03-api/03.02-table-sql-api/built-in-functions-complete-list.md) | 内置函数完整列表 | 1.17+ |
| [03-api/03.02-table-sql-api/data-types-complete-reference.md](../data-types-complete-reference.md) | 数据类型完整参考 | 1.17+ |
| [03-api/03.02-table-sql-api/flink-python-udf.md](../03-api/03.02-table-sql-api/flink-python-udf.md) | Python UDF 开发指南 | 1.17+ |
| [03-api/03.02-table-sql-api/flink-vector-search-rag.md](../03-api/03.02-table-sql-api/flink-vector-search-rag.md) | 向量搜索与 RAG 实现 | 1.20+ |
| [03-api/03.02-table-sql-api/vector-search.md](../03-api/03.02-table-sql-api/vector-search.md) | 向量搜索功能指南 | 1.20+ |
| [03-api/03.02-table-sql-api/model-ddl-and-ml-predict.md](../03-api/03.02-table-sql-api/model-ddl-and-ml-predict.md) | Model DDL 与 ML 预测 | 1.19+ |
| [03-api/03.02-table-sql-api/query-optimization-analysis.md](../03-api/03.02-table-sql-api/query-optimization-analysis.md) | 查询优化分析 | 1.17+ |
| [03-api/03.02-table-sql-api/sql-functions-cheatsheet.md](../03-api/03.02-table-sql-api/sql-functions-cheatsheet.md) | SQL 函数速查表 | 1.17+ |
| [03-api/03.02-table-sql-api/sql-vs-datastream-comparison.md](../03-api/03.02-table-sql-api/sql-vs-datastream-comparison.md) | SQL vs DataStream API 对比 | 1.17+ |

---

### 04. 连接器 (Connectors)

| 文档 | 描述 | 版本 |
|------|------|------|
| [05-ecosystem/05.01-connectors/flink-connectors-ecosystem-complete-guide.md](../05-ecosystem/05.01-connectors/flink-connectors-ecosystem-complete-guide.md) | 连接器生态完整指南 | 1.17+ |
| [05-ecosystem/05.01-connectors/flink-24-connectors-guide.md](../05-ecosystem/05.01-connectors/flink-24-connectors-guide.md) | Flink 2.4 连接器指南 | 2.4+ |
| [05-ecosystem/05.01-connectors/kafka-integration-patterns.md](../05-ecosystem/05.01-connectors/kafka-integration-patterns.md) | Kafka 集成模式 | 1.17+ |
| [05-ecosystem/05.01-connectors/flink-cdc-3.0-data-integration.md](../05-ecosystem/05.01-connectors/flink-cdc-3.0-data-integration.md) | CDC 3.0 数据集成 | 1.18+ |
| [05-ecosystem/05.01-connectors/04.04-cdc-debezium-integration.md](../05-ecosystem/05.01-connectors/04.04-cdc-debezium-integration.md) | Debezium CDC 集成 | 1.17+ |
| [05-ecosystem/05.01-connectors/jdbc-connector-complete-guide.md](../05-ecosystem/05.01-connectors/jdbc-connector-complete-guide.md) | JDBC 连接器完整指南 | 1.17+ |
| [05-ecosystem/05.01-connectors/elasticsearch-connector-complete-guide.md](../05-ecosystem/05.01-connectors/elasticsearch-connector-complete-guide.md) | Elasticsearch 连接器 | 1.17+ |
| [05-ecosystem/05.01-connectors/mongodb-connector-complete-guide.md](../05-ecosystem/05.01-connectors/mongodb-connector-complete-guide.md) | MongoDB 连接器 | 1.17+ |
| [05-ecosystem/05.01-connectors/pulsar-integration-guide.md](../05-ecosystem/05.01-connectors/pulsar-integration-guide.md) | Pulsar 集成指南 | 1.17+ |
| [05-ecosystem/05.01-connectors/flink-delta-lake-integration.md](../05-ecosystem/05.01-connectors/flink-delta-lake-integration.md) | Delta Lake 集成 | 1.18+ |
| [05-ecosystem/05.01-connectors/flink-iceberg-integration.md](../05-ecosystem/05.01-connectors/flink-iceberg-integration.md) | Iceberg 集成 | 1.18+ |
| [05-ecosystem/05.01-connectors/flink-paimon-integration.md](../05-ecosystem/05.01-connectors/flink-paimon-integration.md) | Paimon 集成 | 1.18+ |
| [05-ecosystem/05.01-connectors/fluss-integration.md](../05-ecosystem/05.01-connectors/fluss-integration.md) | Fluss 集成 | 2.0+ |
| [05-ecosystem/05.01-connectors/cloudevents-integration-guide.md](../05-ecosystem/05.01-connectors/cloudevents-integration-guide.md) | CloudEvents 集成 | 1.18+ |
| [05-ecosystem/05.01-connectors/diskless-kafka-cloud-native.md](../05-ecosystem/05.01-connectors/diskless-kafka-cloud-native.md) | 无盘 Kafka 云原生方案 | 1.19+ |

---

### 05. 运维与生产实践

| 文档 | 描述 | 版本 |
|------|------|------|
| [04-runtime/04.02-operations/production-checklist.md](../../Knowledge/production-checklist.md) | 生产环境检查清单 | 1.17+ |
| [04-runtime/04.02-operations/rest-api-complete-reference.md](../04-runtime/04.02-operations/rest-api-complete-reference.md) | REST API 完整参考 | 1.17+ |

---

### 06. 竞品对比 (vs Competitors)

| 文档 | 描述 | 版本 |
|------|------|------|
| [05-vs-competitors/flink-vs-spark-streaming.md](../09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-spark-streaming.md) | Flink vs Spark Streaming 对比 | 1.17+ |
| [05-vs-competitors/flink-vs-kafka-streams.md](../09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-kafka-streams.md) | Flink vs Kafka Streams 对比 | 1.17+ |
| [05-vs-competitors/linkedin-samza-deep-dive.md](../09-practices/09.03-performance-tuning/05-vs-competitors/linkedin-samza-deep-dive.md) | LinkedIn Samza 深度解析 | 1.17+ |

---

### 07. 工程实践 (Engineering)

| 文档 | 描述 | 版本 |
|------|------|------|
| [09-practices/09.03-performance-tuning/06.02-performance-optimization-complete.md](../09-practices/09.03-performance-tuning/06.02-performance-optimization-complete.md) | 性能优化完整指南 | 1.17+ |
| [09-practices/09.03-performance-tuning/performance-tuning-guide.md](../09-practices/09.03-performance-tuning/performance-tuning-guide.md) | 性能调优指南 | 1.17+ |
| [09-practices/09.03-performance-tuning/flink-24-performance-improvements.md](../09-practices/09.03-performance-tuning/flink-24-performance-improvements.md) | Flink 2.4 性能改进 | 2.4+ |
| [09-practices/09.03-performance-tuning/state-backend-selection.md](../09-practices/09.03-performance-tuning/state-backend-selection.md) | State Backend 选型指南 | 1.17+ |
| [09-practices/09.03-performance-tuning/flink-tco-cost-optimization-guide.md](../09-practices/09.03-performance-tuning/flink-tco-cost-optimization-guide.md) | TCO 成本优化指南 | 1.17+ |
| [09-practices/09.03-performance-tuning/stream-processing-cost-optimization.md](../09-practices/09.03-performance-tuning/stream-processing-cost-optimization.md) | 流处理成本优化 | 1.17+ |
| [09-practices/09.03-performance-tuning/stream-processing-testing-strategies.md](../09-practices/09.03-performance-tuning/stream-processing-testing-strategies.md) | 流处理测试策略 | 1.17+ |
| [09-practices/09.03-performance-tuning/flink-dbt-integration.md](../09-practices/09.03-performance-tuning/flink-dbt-integration.md) | dbt 集成指南 | 1.18+ |

---

### 08. 案例研究 (Case Studies)

| 文档 | 描述 | 版本 |
|------|------|------|
| [09-practices/09.01-case-studies/case-realtime-analytics.md](../09-practices/09.01-case-studies/case-realtime-analytics.md) | 实时分析通用案例 | 1.17+ |
| [09-practices/09.01-case-studies/case-fraud-detection-advanced.md](../09-practices/09.01-case-studies/case-fraud-detection-advanced.md) | 高级欺诈检测案例 | 1.17+ |
| [09-practices/09.01-case-studies/case-financial-realtime-risk-control.md](../09-practices/09.01-case-studies/case-financial-realtime-risk-control.md) | 金融实时风控 | 1.17+ |
| [09-practices/09.01-case-studies/case-ecommerce-realtime-recommendation.md](../09-practices/09.01-case-studies/case-ecommerce-realtime-recommendation.md) | 电商实时推荐 | 1.17+ |
| [09-practices/09.01-case-studies/case-clickstream-user-behavior-analytics.md](../09-practices/09.01-case-studies/case-clickstream-user-behavior-analytics.md) | 点击流用户行为分析 | 1.17+ |
| [09-practices/09.01-case-studies/case-iot-stream-processing.md](../09-practices/09.01-case-studies/case-iot-stream-processing.md) | IoT 流处理 | 1.17+ |
| [09-practices/09.01-case-studies/case-smart-city-iot.md](../09-practices/09.01-case-studies/case-smart-city-iot.md) | 智慧城市 IoT | 1.17+ |
| [09-practices/09.01-case-studies/case-smart-manufacturing-iot.md](../09-practices/09.01-case-studies/case-smart-manufacturing-iot.md) | 智能制造 IoT | 1.17+ |
| [09-practices/09.01-case-studies/case-smart-grid-energy-management.md](../09-practices/09.01-case-studies/case-smart-grid-energy-management.md) | 智能电网能源管理 | 1.17+ |
| [09-practices/09.01-case-studies/case-energy-grid-optimization.md](../09-practices/09.01-case-studies/case-energy-grid-optimization.md) | 能源网格优化 | 1.17+ |
| [09-practices/09.01-case-studies/case-logistics-realtime-tracking.md](../09-practices/09.01-case-studies/case-logistics-realtime-tracking.md) | 物流实时追踪 | 1.17+ |
| [09-practices/09.01-case-studies/case-supply-chain-optimization.md](../09-practices/09.01-case-studies/case-supply-chain-optimization.md) | 供应链优化 | 1.17+ |
| [09-practices/09.01-case-studies/case-social-media-analytics.md](../09-practices/09.01-case-studies/case-social-media-analytics.md) | 社交媒体分析 | 1.17+ |
| [09-practices/09.01-case-studies/case-gaming-realtime-analytics.md](../09-practices/09.01-case-studies/case-gaming-realtime-analytics.md) | 游戏实时分析 | 1.17+ |
| [09-practices/09.01-case-studies/case-healthcare-monitoring.md](../09-practices/09.01-case-studies/case-healthcare-monitoring.md) | 医疗健康监控 | 1.17+ |

---

### 09. 路线图与版本演进 (Roadmap) ⭐

> **重点模块**：Flink 各版本特性演进与未来规划

#### 版本专题

| 文档 | 描述 | 版本 |
|------|------|------|
| [08-roadmap/08.01-flink-24/flink-version-evolution-complete-guide.md](../08-roadmap/08.01-flink-24/flink-version-evolution-complete-guide.md) | 版本演进完整指南 | 1.17 - 3.0 |
| [08-roadmap/08.01-flink-24/flink-version-comparison-matrix.md](../08-roadmap/08.01-flink-24/flink-version-comparison-matrix.md) | 版本对比矩阵 | 1.17 - 3.0 |
| [08-roadmap/08.01-flink-24/FLIP-TRACKING-SYSTEM.md](../08-roadmap/08.01-flink-24/FLIP-TRACKING-SYSTEM.md) | FLIP 追踪系统 | 全版本 |

#### Flink 2.4 专题

| 文档 | 描述 | 版本 |
|------|------|------|
| [08-roadmap/08.01-flink-24/flink-2.4-tracking.md](../08-roadmap/08.01-flink-24/flink-2.4-tracking.md) | Flink 2.4 特性追踪 | 2.4 |
| [flink-24/flink-24-adaptive-execution-v2.md](../08-roadmap/08.01-flink-24/flink-2.4-tracking.md) | 自适应执行 V2 | 2.4 |
| [flink-24/flink-24-ansi-sql-2023.md](../08-roadmap/08.01-flink-24/flink-2.4-tracking.md) | ANSI SQL 2023 支持 | 2.4 |
| [flink-24/flink-24-new-connectors.md](../08-roadmap/08.01-flink-24/flink-2.4-tracking.md) | 新连接器 | 2.4 |
| [flink-24/flink-24-deployment-improvements.md](../04-runtime/04.01-deployment/flink-24-deployment-improvements.md) | 部署改进 | 2.4 |
| [flink-24/flink-24-performance-improvements.md](../09-practices/09.03-performance-tuning/flink-24-performance-improvements.md) | 性能改进 | 2.4 |
| [flink-24/flink-24-observability-enhancements.md](../08-roadmap/08.01-flink-24/flink-2.4-tracking.md) | 可观测性增强 | 2.4 |
| [flink-24/flink-24-security-enhancements.md](../09-practices/09.04-security/flink-24-security-enhancements.md) | 安全增强 | 2.4 |
| [flink-24/flink-24-smart-checkpointing.md](../08-roadmap/08.01-flink-24/flink-2.4-tracking.md) | 智能 Checkpoint | 2.4 |
| [flink-24/flink-24-serverless-ga.md](../08-roadmap/08.01-flink-24/flink-2.4-tracking.md) | Serverless GA | 2.4 |
| [flink-24/flink-24-ai-agents-ga.md](../06-ai-ml/flink-ai-agents-flip-531.md) | AI Agents GA | 2.4 |

#### Flink 2.5 专题

| 文档 | 描述 | 版本 |
|------|------|------|
| [08-roadmap/08.01-flink-24/flink-2.5-preview.md](../08-roadmap/08.01-flink-24/flink-2.5-preview.md) | Flink 2.5 预览 | 2.5 |
| [08-roadmap/08.01-flink-24/flink-25-stream-batch-unification.md](../08-roadmap/08.01-flink-24/flink-25-stream-batch-unification.md) | 流批一体 | 2.5 |
| [flink-25/flink-25-stream-batch-unified.md](../08-roadmap/08.01-flink-24/flink-25-stream-batch-unification.md) | 流批统一实现 | 2.5 |
| [flink-25/flink-25-wasm-udf-ga.md](../03-api/09-language-foundations/flink-25-wasm-udf-ga.md) | WASM UDF GA | 2.5 |
| [flink-25/flink-25-gpu-acceleration.md](../06-ai-ml/flink-25-gpu-acceleration.md) | GPU 加速 | 2.5 |
| [flink-25/flink-25-ai-ml-production.md](../06-ai-ml/flink-ai-agents-flip-531.md) | AI/ML 生产级支持 | 2.5 |
| [flink-25/flink-25-serverless-v2.md](../08-roadmap/08.01-flink-24/flink-2.5-preview.md) | Serverless V2 | 2.5 |
| [flink-25/flink-25-storage-backends.md](../02-core/state-backends-deep-comparison.md) | 存储后端增强 | 2.5 |
| [flink-25/flink-25-performance.md](../09-practices/09.03-performance-tuning/flink-24-performance-improvements.md) | 性能提升 | 2.5 |
| [flink-25/flink-25-observability.md](../04-runtime/04.03-observability/distributed-tracing.md) | 可观测性 | 2.5 |
| [flink-25/flink-25-deployment.md](../04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md) | 部署优化 | 2.5 |
| [flink-25/flink-25-new-connectors.md](../08-roadmap/08.01-flink-24/flink-2.5-preview.md) | 新连接器 | 2.5 |

#### Flink 3.0 专题

| 文档 | 描述 | 版本 |
|------|------|------|
| [08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md](../08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md) | 架构重设计 | 3.0 |
| [08-roadmap/08.01-flink-24/flink-2.3-2.4-roadmap.md](../08-roadmap/08.01-flink-24/flink-2.3-2.4-roadmap.md) | 2.3-2.4 路线图 | 2.3 - 2.4 |
| [flink-30/flink-30-architecture-changes.md](../08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md) | 架构变更 | 3.0 |
| [flink-30/flink-30-api-redesign.md](../08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md) | API 重设计 | 3.0 |
| [flink-30/flink-30-cloud-native.md](../08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md) | 云原生支持 | 3.0 |
| [flink-30/flink-30-state-management.md](../02-core/state-backends-deep-comparison.md) | 状态管理演进 | 3.0 |
| [flink-30/flink-30-ai-native.md](../06-ai-ml/flink-ai-agents-flip-531.md) | AI Native 支持 | 3.0 |
| [flink-30/flink-30-performance.md](../09-practices/09.03-performance-tuning/flink-24-performance-improvements.md) | 性能目标 | 3.0 |
| [flink-30/flink-30-security.md](../09-practices/09.04-security/flink-security-complete-guide.md) | 安全架构 | 3.0 |
| [flink-30/flink-30-connectors.md](../05-ecosystem/05.01-connectors/flink-connectors-ecosystem-complete-guide.md) | 连接器生态 | 3.0 |
| [flink-30/flink-30-observability.md](../04-runtime/04.03-observability/distributed-tracing.md) | 可观测性 | 3.0 |
| [flink-30/flink-30-sql-standard.md](../03-api/03.02-table-sql-api/ansi-sql-2023-compliance-guide.md) | SQL 标准 | 3.0 |

#### 前沿追踪

| 文档 | 描述 | 版本 |
|------|------|------|
| [08-roadmap/08.01-flink-24/flink-2.1-frontier-tracking.md](../08-roadmap/08.01-flink-24/flink-2.1-frontier-tracking.md) | Flink 2.1 前沿追踪 | 2.1 |
| [08-roadmap/08.01-flink-24/2026-q2-flink-tasks.md](../08-roadmap/08.01-flink-24/2026-q2-flink-tasks.md) | 2026 Q2 任务清单 | - |
| [08-roadmap/08.01-flink-24/community-dynamics-tracking.md](../08-roadmap/08.01-flink-24/community-dynamics-tracking.md) | 社区动态追踪 | - |
| [version-tracking/flink-26-27-roadmap.md](version-tracking/flink-26-27-roadmap.md) | Flink 2.6-2.7 路线图 | 2.6 - 2.7 |
| [version-tracking/flink-26-27-status-report.md](version-tracking/flink-26-27-status-report.md) | 2.6-2.7 状态报告 | 2.6 - 2.7 |

---

### 10. 语言基础 (Language Foundations)

| 文档 | 描述 | 版本 |
|------|------|------|
| [03-api/09-language-foundations/flink-datastream-api-complete-guide.md](../03-api/09-language-foundations/flink-datastream-api-complete-guide.md) | DataStream API 完整指南 | 1.17+ |
| [03-api/09-language-foundations/datastream-api-cheatsheet.md](../03-api/09-language-foundations/datastream-api-cheatsheet.md) | DataStream API 速查表 | 1.17+ |
| [03-api/09-language-foundations/05-datastream-v2-api.md](../03-api/09-language-foundations/05-datastream-v2-api.md) | DataStream V2 API | 1.19+ |
| [03-api/09-language-foundations/pyflink-complete-guide.md](../03-api/09-language-foundations/pyflink-complete-guide.md) | PyFlink 完整指南 | 1.17+ |
| [03-api/09-language-foundations/flink-pyflink-deep-dive.md](../flink-pyflink-deep-dive.md) | PyFlink 深度解析 | 1.17+ |
| [03-api/09-language-foundations/02.03-python-async-api.md](../03-api/09-language-foundations/02.03-python-async-api.md) | Python 异步 API | 1.18+ |
| [03-api/09-language-foundations/01.01-scala-types-for-streaming.md](../03-api/09-language-foundations/01.01-scala-types-for-streaming.md) | Scala 流处理类型系统 | 1.17+ |
| [03-api/09-language-foundations/01.02-typeinformation-derivation.md](../03-api/09-language-foundations/01.02-typeinformation-derivation.md) | TypeInformation 推导 | 1.17+ |
| [03-api/09-language-foundations/01.03-scala3-type-system-formalization.md](../03-api/09-language-foundations/01.03-scala3-type-system-formalization.md) | Scala 3 类型系统形式化 | 1.18+ |
| [03-api/09-language-foundations/flink-language-support-complete-guide.md](../03-api/09-language-foundations/flink-language-support-complete-guide.md) | 语言支持完整指南 | 1.17+ |
| [03-api/09-language-foundations/flink-rust-native-api-guide.md](../03-api/09-language-foundations/flink-rust-native-api-guide.md) | Rust Native API 指南 | 2.0+ |
| [03-api/09-language-foundations/03.01-migration-guide.md](../03-api/09-language-foundations/03.01-migration-guide.md) | 语言迁移指南 | 1.17+ |
| [03-api/09-language-foundations/02.01-java-api-from-scala.md](../03-api/09-language-foundations/02.01-java-api-from-scala.md) | Scala 到 Java API 迁移 | 1.17+ |
| [03-api/09-language-foundations/02.02-flink-scala-api-community.md](../03-api/09-language-foundations/02.02-flink-scala-api-community.md) | Flink Scala API 社区 | 1.17+ |

---

### 11. 部署指南 (Deployment)

| 文档 | 描述 | 版本 |
|------|------|------|
| [04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md](../04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md) | 部署运维完整指南 | 1.17+ |
| [04-runtime/04.01-deployment/kubernetes-deployment.md](../04-runtime/04.01-deployment/kubernetes-deployment.md) | Kubernetes 部署 | 1.17+ |
| [04-runtime/04.01-deployment/kubernetes-deployment-production-guide.md](../04-runtime/04.01-deployment/kubernetes-deployment-production-guide.md) | K8s 生产部署指南 | 1.17+ |
| [04-runtime/04.01-deployment/flink-kubernetes-operator-deep-dive.md](../04-runtime/04.01-deployment/flink-kubernetes-operator-deep-dive.md) | K8s Operator 深度解析 | 1.17+ |
| [04-runtime/04.01-deployment/flink-kubernetes-autoscaler-deep-dive.md](../04-runtime/04.01-deployment/flink-kubernetes-autoscaler-deep-dive.md) | K8s Autoscaler 深度解析 | 1.18+ |
| [04-runtime/04.01-deployment/flink-serverless-architecture.md](../04-runtime/04.01-deployment/flink-serverless-architecture.md) | Serverless 架构 | 1.19+ |
| [04-runtime/04.01-deployment/serverless-flink-ga-guide.md](../04-runtime/04.01-deployment/serverless-flink-ga-guide.md) | Serverless GA 指南 | 2.4+ |
| [04-runtime/04.01-deployment/multi-cloud-deployment-templates.md](../04-runtime/04.01-deployment/multi-cloud-deployment-templates.md) | 多云部署模板 | 1.17+ |
| [04-runtime/04.01-deployment/flink-24-deployment-improvements.md](../04-runtime/04.01-deployment/flink-24-deployment-improvements.md) | 2.4 部署改进 | 2.4+ |
| [04-runtime/04.01-deployment/cost-optimization-calculator.md](../04-runtime/04.01-deployment/cost-optimization-calculator.md) | 成本优化计算器 | 1.17+ |

---

### 12. 性能测试 (Benchmarking)

| 文档 | 描述 | 版本 |
|------|------|------|
| [09-practices/09.02-benchmarking/performance-benchmarking-guide.md](../09-practices/09.02-benchmarking/performance-benchmarking-guide.md) | 性能测试指南 | 1.17+ |
| [09-practices/09.02-benchmarking/performance-benchmark-suite.md](../09-practices/09.02-benchmarking/performance-benchmark-suite.md) | 性能测试套件 | 1.17+ |
| [09-practices/09.02-benchmarking/streaming-benchmarks.md](../09-practices/09.02-benchmarking/streaming-benchmarks.md) | 流处理基准测试 | 1.17+ |
| [09-practices/09.02-benchmarking/flink-24-25-benchmark-results.md](../09-practices/09.02-benchmarking/flink-24-25-benchmark-results.md) | 2.4/2.5 基准测试结果 | 2.4 - 2.5 |

---

### 13. AI/ML 集成

| 文档 | 描述 | 版本 |
|------|------|------|
| [06-ai-ml/flink-ai-ml-integration-complete-guide.md](../06-ai-ml/flink-ai-ml-integration-complete-guide.md) | AI/ML 集成完整指南 | 1.19+ |
| [06-ai-ml/flink-ml-architecture.md](../06-ai-ml/flink-ml-architecture.md) | ML 架构设计 | 1.19+ |
| [06-ai-ml/flink-realtime-ml-inference.md](../06-ai-ml/flink-realtime-ml-inference.md) | 实时 ML 推理 | 1.19+ |
| [06-ai-ml/model-serving-streaming.md](../06-ai-ml/model-serving-streaming.md) | 流式模型服务 | 1.19+ |
| [06-ai-ml/online-learning-algorithms.md](../06-ai-ml/online-learning-algorithms.md) | 在线学习算法 | 1.19+ |
| [06-ai-ml/online-learning-production.md](../06-ai-ml/online-learning-production.md) | 在线学习生产实践 | 1.19+ |
| [06-ai-ml/flink-llm-integration.md](../06-ai-ml/flink-llm-integration.md) | LLM 集成 | 1.20+ |
| [06-ai-ml/flink-llm-realtime-rag-architecture.md](../06-ai-ml/flink-llm-realtime-rag-architecture.md) | 实时 RAG 架构 | 1.20+ |
| [06-ai-ml/rag-streaming-architecture.md](../06-ai-ml/rag-streaming-architecture.md) | RAG 流式架构 | 1.20+ |
| [06-ai-ml/vector-database-integration.md](../06-ai-ml/vector-database-integration.md) | 向量数据库集成 | 1.20+ |
| [06-ai-ml/flink-agents-flip-531.md](../06-ai-ml/flink-agents-flip-531.md) | FLIP-531 AI Agents | 2.4+ |
| [06-ai-ml/flink-ai-agents-flip-531.md](../06-ai-ml/flink-ai-agents-flip-531.md) | Flink AI Agents 详解 | 2.4+ |
| [06-ai-ml/flip-531-ai-agents-ga-guide.md](../06-ai-ml/flip-531-ai-agents-ga-guide.md) | FLIP-531 GA 指南 | 2.4+ |
| [06-ai-ml/ai-agent-flink-deep-integration.md](../06-ai-ml/ai-agent-flink-deep-integration.md) | AI Agent 深度集成 | 2.4+ |
| [06-ai-ml/flink-mcp-protocol-integration.md](../06-ai-ml/flink-mcp-protocol-integration.md) | MCP 协议集成 | 2.5+ |
| [06-ai-ml/realtime-feature-engineering-feature-store.md](../06-ai-ml/realtime-feature-engineering-feature-store.md) | 实时特征工程 | 1.19+ |
| [06-ai-ml/flink-25-gpu-acceleration.md](../06-ai-ml/flink-25-gpu-acceleration.md) | GPU 加速 | 2.5+ |

---

### 14. 安全 (Security)

| 文档 | 描述 | 版本 |
|------|------|------|
| [09-practices/09.04-security/flink-security-complete-guide.md](../09-practices/09.04-security/flink-security-complete-guide.md) | 安全完整指南 | 1.17+ |
| [09-practices/09.04-security/security-hardening-guide.md](../09-practices/09.04-security/security-hardening-guide.md) | 安全加固指南 | 1.17+ |
| [09-practices/09.04-security/flink-24-security-enhancements.md](../09-practices/09.04-security/flink-24-security-enhancements.md) | 2.4 安全增强 | 2.4 |
| [09-practices/09.04-security/streaming-security-best-practices.md](../09-practices/09.04-security/streaming-security-best-practices.md) | 流处理安全最佳实践 | 1.17+ |
| [09-practices/09.04-security/spiffe-spire-integration-guide.md](../09-practices/09.04-security/spiffe-spire-integration-guide.md) | SPIFFE/SPIRE 集成 | 1.19+ |
| [09-practices/09.04-security/trusted-execution-flink.md](../09-practices/09.04-security/trusted-execution-flink.md) | 可信执行环境 | 1.20+ |
| [09-practices/09.04-security/gpu-confidential-computing.md](../09-practices/09.04-security/gpu-confidential-computing.md) | GPU 机密计算 | 2.5+ |

---

### 15. WebAssembly (WASM)

| 文档 | 描述 | 版本 |
|------|------|------|
| [05-ecosystem/05.03-wasm-udf/wasm-streaming.md](../05-ecosystem/05.03-wasm-udf/wasm-streaming.md) | WASM 流处理 | 1.19+ |
| [05-ecosystem/05.03-wasm-udf/wasi-0.3-async-preview.md](../05-ecosystem/05.03-wasm-udf/wasi-0.3-async-preview.md) | WASI 0.3 异步预览 | 2.0+ |

---

### 16. 图处理 (Graph)

| 文档 | 描述 | 版本 |
|------|------|------|
| [05-ecosystem/05.04-graph/flink-gelly.md](../05-ecosystem/05.04-graph/flink-gelly.md) | Gelly 图计算库 | 1.17+ |
| [05-ecosystem/05.04-graph/flink-gelly-streaming-graph-processing.md](../05-ecosystem/05.04-graph/flink-gelly-streaming-graph-processing.md) | 流式图处理 | 1.17+ |

---

### 17. Lakehouse 集成

| 文档 | 描述 | 版本 |
|------|------|------|
| [05-ecosystem/05.02-lakehouse/README.md](../../Knowledge/09-anti-patterns/README.md) | Lakehouse 集成概览 | 1.18+ |
| [05-ecosystem/05.02-lakehouse/streaming-lakehouse-architecture.md](../05-ecosystem/05.02-lakehouse/streaming-lakehouse-architecture.md) | 流式 Lakehouse 架构 | 1.18+ |
| [05-ecosystem/05.02-lakehouse/streaming-lakehouse-deep-dive-2026.md](../05-ecosystem/05.02-lakehouse/streaming-lakehouse-deep-dive-2026.md) | Lakehouse 深度解析 2026 | 1.19+ |
| [05-ecosystem/05.02-lakehouse/flink-iceberg-integration.md](../05-ecosystem/05.01-connectors/flink-iceberg-integration.md) | Iceberg 集成 | 1.18+ |
| [05-ecosystem/05.02-lakehouse/flink-paimon-integration.md](../05-ecosystem/05.01-connectors/flink-paimon-integration.md) | Paimon 集成 | 1.18+ |

---

### 18. Rust/汇编生态 (Rust Assembly Ecosystem)

> **重点模块**：Flink 与 Rust 生态的集成，包括高性能 UDF、WASM、SIMD 优化等

#### 导航与索引

| 文档 | 描述 | 版本 |
|------|------|------|
| [07-rust-native/00-MASTER-INDEX.md](../../Knowledge/Flink-Scala-Rust-Comprehensive/00-MASTER-INDEX.md) | Rust 生态主索引 | - |
| [07-rust-native/README.md](../../Knowledge/09-anti-patterns/README.md) | Rust 生态概览 | 2.0+ |

#### 架构与趋势

| 文档 | 描述 | 版本 |
|------|------|------|
| [07-rust-native/ai-native-streaming/01-ai-native-architecture.md](../07-rust-native/ai-native-streaming/01-ai-native-architecture.md) | AI Native 流式架构 | 2.5+ |
| [07-rust-native/ai-native-streaming/02-llm-streaming-integration.md](../07-rust-native/ai-native-streaming/02-llm-streaming-integration.md) | LLM 流式集成 | 2.5+ |
| [07-rust-native/ai-native-streaming/03-vector-search-streaming.md](../07-rust-native/ai-native-streaming/03-vector-search-streaming.md) | 流式向量搜索 | 2.5+ |
| [07-rust-native/ai-native-streaming/04-ml-inference-optimization.md](../07-rust-native/ai-native-streaming/04-ml-inference-optimization.md) | ML 推理优化 | 2.5+ |
| [07-rust-native/trends/01-flink-rust-ecosystem-trends-2026.md](../07-rust-native/trends/01-flink-rust-ecosystem-trends-2026.md) | 2026 Rust 生态趋势 | 2.0+ |

#### Flash 引擎

| 文档 | 描述 | 版本 |
|------|------|------|
| [07-rust-native/flash-engine/01-flash-architecture.md](../07-rust-native/flash-engine/01-flash-architecture.md) | Flash 引擎架构 | 2.0+ |
| [07-rust-native/flash-engine/02-falcon-vector-layer.md](../07-rust-native/flash-engine/02-falcon-vector-layer.md) | Falcon 向量层 | 2.0+ |
| [07-rust-native/flash-engine/03-forstdb-storage.md](../07-rust-native/flash-engine/03-forstdb-storage.md) | ForStDB 存储 | 2.0+ |
| [07-rust-native/flash-engine/04-nexmark-benchmark-analysis.md](../07-rust-native/flash-engine/04-nexmark-benchmark-analysis.md) | Nexmark 基准分析 | 2.0+ |
| [07-rust-native/flash-engine/05-flink-compatibility.md](../07-rust-native/flash-engine/05-flink-compatibility.md) | Flink 兼容性 | 2.0+ |
| [07-rust-native/flash-engine/06-production-deployment-2025.md](../07-rust-native/flash-engine/06-production-deployment-2025.md) | 2025 生产部署 | 2.0+ |

#### SIMD 优化

| 文档 | 描述 | 版本 |
|------|------|------|
| [07-rust-native/simd-optimization/01-simd-fundamentals.md](../07-rust-native/simd-optimization/01-simd-fundamentals.md) | SIMD 基础 | 2.0+ |
| [07-rust-native/simd-optimization/02-avx2-avx512-guide.md](../07-rust-native/simd-optimization/02-avx2-avx512-guide.md) | AVX2/AVX512 指南 | 2.0+ |
| [07-rust-native/simd-optimization/03-jni-assembly-bridge.md](../07-rust-native/simd-optimization/03-jni-assembly-bridge.md) | JNI 汇编桥接 | 2.0+ |
| [07-rust-native/simd-optimization/04-vectorized-udf-patterns.md](../07-rust-native/simd-optimization/04-vectorized-udf-patterns.md) | 向量化 UDF 模式 | 2.0+ |
| [07-rust-native/simd-optimization/05-arm-neon-sve-guide.md](../07-rust-native/simd-optimization/05-arm-neon-sve-guide.md) | ARM NEON/SVE 指南 | 2.0+ |

#### WASM 3.0

| 文档 | 描述 | 版本 |
|------|------|------|
| [07-rust-native/wasm-3.0/01-wasm-3.0-spec-guide.md](../07-rust-native/wasm-3.0/01-wasm-3.0-spec-guide.md) | WASM 3.0 规范指南 | 2.0+ |
| [07-rust-native/wasm-3.0/02-memory64-deep-dive.md](../07-rust-native/wasm-3.0/02-memory64-deep-dive.md) | Memory64 深度解析 | 2.0+ |
| [07-rust-native/wasm-3.0/03-relaxed-simd-guide.md](../07-rust-native/wasm-3.0/03-relaxed-simd-guide.md) | Relaxed SIMD 指南 | 2.0+ |
| [07-rust-native/wasm-3.0/04-exception-handling-patterns.md](../07-rust-native/wasm-3.0/04-exception-handling-patterns.md) | 异常处理模式 | 2.0+ |

#### WASI 0.3

| 文档 | 描述 | 版本 |
|------|------|------|
| [07-rust-native/wasi-0.3-async/01-wasi-0.3-spec-guide.md](../07-rust-native/wasi-0.3-async/01-wasi-0.3-spec-guide.md) | WASI 0.3 规范指南 | 2.5+ |
| [07-rust-native/wasi-0.3-async/02-async-streaming-patterns.md](../07-rust-native/wasi-0.3-async/02-async-streaming-patterns.md) | 异步流式模式 | 2.5+ |
| [07-rust-native/wasi-0.3-async/03-component-model-guide.md](../07-rust-native/wasi-0.3-async/03-component-model-guide.md) | 组件模型指南 | 2.5+ |
| [07-rust-native/wasi-0.3-async/04-edge-compute-integration.md](../07-rust-native/wasi-0.3-async/04-edge-compute-integration.md) | 边缘计算集成 | 2.5+ |

#### 异构计算

| 文档 | 描述 | 版本 |
|------|------|------|
| [07-rust-native/heterogeneous-computing/01-gpu-udf-cuda.md](../07-rust-native/heterogeneous-computing/01-gpu-udf-cuda.md) | GPU UDF (CUDA) | 2.5+ |
| [07-rust-native/heterogeneous-computing/02-gpu-udf-rocm.md](../07-rust-native/heterogeneous-computing/02-gpu-udf-rocm.md) | GPU UDF (ROCm) | 2.5+ |
| [07-rust-native/heterogeneous-computing/03-fpga-acceleration.md](../07-rust-native/heterogeneous-computing/03-fpga-acceleration.md) | FPGA 加速 | 2.5+ |
| [07-rust-native/heterogeneous-computing/04-unified-acceleration-api.md](../07-rust-native/heterogeneous-computing/04-unified-acceleration-api.md) | 统一加速 API | 2.5+ |

#### 向量化和 Iron Functions

| 文档 | 描述 | 版本 |
|------|------|------|
| [07-rust-native/vectorized-udfs/01-vectorized-udf-intro.md](../07-rust-native/vectorized-udfs/01-vectorized-udf-intro.md) | 向量化 UDF 简介 | 2.0+ |
| [07-rust-native/vectorized-udfs/02-arrow-format-integration.md](../07-rust-native/vectorized-udfs/02-arrow-format-integration.md) | Arrow 格式集成 | 2.0+ |
| [07-rust-native/vectorized-udfs/03-columnar-processing.md](../07-rust-native/vectorized-udfs/03-columnar-processing.md) | 列式处理 | 2.0+ |
| [07-rust-native/vectorized-udfs/04-performance-tuning.md](../07-rust-native/vectorized-udfs/04-performance-tuning.md) | 性能调优 | 2.0+ |
| [07-rust-native/iron-functions/01-iron-functions-complete-guide.md](../07-rust-native/iron-functions/01-iron-functions-complete-guide.md) | Iron Functions 完整指南 | 2.0+ |

#### 边缘计算与 RisingWave

| 文档 | 描述 | 版本 |
|------|------|------|
| [07-rust-native/edge-wasm-runtime/01-edge-architecture.md](../07-rust-native/edge-wasm-runtime/01-edge-architecture.md) | 边缘架构 | 2.0+ |
| [07-rust-native/edge-wasm-runtime/02-iot-gateway-patterns.md](../07-rust-native/edge-wasm-runtime/02-iot-gateway-patterns.md) | IoT 网关模式 | 2.0+ |
| [07-rust-native/edge-wasm-runtime/03-5g-mec-integration.md](../07-rust-native/edge-wasm-runtime/03-5g-mec-integration.md) | 5G MEC 集成 | 2.0+ |
| [07-rust-native/edge-wasm-runtime/04-offline-sync-strategies.md](../07-rust-native/edge-wasm-runtime/04-offline-sync-strategies.md) | 离线同步策略 | 2.0+ |
| [07-rust-native/risingwave-comparison/01-risingwave-architecture.md](../07-rust-native/risingwave-comparison/01-risingwave-architecture.md) | RisingWave 架构 | 2.0+ |
| [07-rust-native/risingwave-comparison/02-nexmark-head-to-head.md](../07-rust-native/risingwave-comparison/02-nexmark-head-to-head.md) | Nexmark 对比 | 2.0+ |
| [07-rust-native/risingwave-comparison/03-migration-guide.md](../07-rust-native/risingwave-comparison/03-migration-guide.md) | 迁移指南 | 2.0+ |
| [07-rust-native/risingwave-comparison/04-hybrid-deployment.md](../07-rust-native/risingwave-comparison/04-hybrid-deployment.md) | 混合部署 | 2.0+ |
| [07-rust-native/risingwave-comparison/04-risingwave-rust-udf-guide.md](../07-rust-native/risingwave-comparison/04-risingwave-rust-udf-guide.md) | RisingWave Rust UDF | 2.0+ |

---

### 19. 可观测性 (Observability)

| 文档 | 描述 | 版本 |
|------|------|------|
| [04-runtime/04.03-observability/flink-observability-complete-guide.md](../04-runtime/04.03-observability/flink-observability-complete-guide.md) | 可观测性完整指南 | 1.17+ |
| [04-runtime/04.03-observability/metrics-and-monitoring.md](../04-runtime/04.03-observability/metrics-and-monitoring.md) | 指标与监控 | 1.17+ |
| [04-runtime/04.03-observability/distributed-tracing.md](../04-runtime/04.03-observability/distributed-tracing.md) | 分布式追踪 | 1.18+ |
| [04-runtime/04.03-observability/event-reporting.md](../04-runtime/04.03-observability/event-reporting.md) | 事件报告 | 1.17+ |
| [04-runtime/04.03-observability/flink-opentelemetry-observability.md](../04-runtime/04.03-observability/flink-opentelemetry-observability.md) | OpenTelemetry 集成 | 1.18+ |
| [04-runtime/04.03-observability/opentelemetry-streaming-observability.md](../04-runtime/04.03-observability/opentelemetry-streaming-observability.md) | 流式可观测性 | 1.18+ |
| [04-runtime/04.03-observability/realtime-data-quality-monitoring.md](../04-runtime/04.03-observability/realtime-data-quality-monitoring.md) | 实时数据质量监控 | 1.19+ |
| [04-runtime/04.03-observability/split-level-watermark-metrics.md](../04-runtime/04.03-observability/split-level-watermark-metrics.md) | Split 级别 Watermark 指标 | 1.19+ |
| [04-runtime/04.03-observability/streaming-metrics-monitoring-slo.md](../04-runtime/04.03-observability/streaming-metrics-monitoring-slo.md) | SLO 监控 | 1.18+ |

---

### 20. 生态集成

| 文档 | 描述 | 版本 |
|------|------|------|
| [05-ecosystem/ecosystem/kafka-streams-migration.md](../../Knowledge/05-mapping-guides/migration-guides/05.2-kafka-streams-to-flink-migration.md) | Kafka Streams 迁移指南 | 1.17+ |
| [05-ecosystem/ecosystem/materialize-comparison.md](../materialize-comparison.md) | Materialize 对比 | 1.18+ |
| [05-ecosystem/ecosystem/pulsar-functions-integration.md](../pulsar-functions-integration.md) | Pulsar Functions 集成 | 1.17+ |
| [05-ecosystem/ecosystem/risingwave-integration-guide.md](../../Knowledge/06-frontier/risingwave-integration-guide.md) | RisingWave 集成指南 | 1.18+ |

---

## 📖 演进文档 (Evolution Docs)

### API 演进

| 模块 | 路径 | 描述 |
|------|------|------|
| DataStream API | [api-evolution/datastream-24.md](../08-roadmap/08.01-flink-24/flink-2.4-tracking.md), [datastream-25.md](../08-roadmap/08.01-flink-24/flink-2.5-preview.md), [datastream-30.md](../08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md) | 各版本演进 |
| SQL API | [api-evolution/sql-24.md](../03-api/03.02-table-sql-api/flink-table-sql-complete-guide.md), [sql-25.md](../08-roadmap/08.01-flink-24/flink-2.5-preview.md), [sql-30.md](../08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md) | SQL 演进 |
| Window API | [api-evolution/window-api.md](../03-api/03.02-table-sql-api/flink-sql-window-functions-deep-dive.md), [window-sql.md](../03-api/03.02-table-sql-api/flink-sql-window-functions-deep-dive.md) | 窗口演进 |
| State API | [api-evolution/state-api.md](../02-core/flink-state-management-complete-guide.md) | 状态 API |
| Async API | [api-evolution/async-api.md](../02-core/async-execution-model.md) | 异步 API |
| CEP | [api-evolution/cep-evolution.md](../03-api/03.02-table-sql-api/flink-cep-complete-guide.md) | CEP 演进 |
| 聚合 | [api-evolution/agg-sql.md](../03-api/03.02-table-sql-api/flink-sql-window-functions-deep-dive.md) | 聚合函数 |
| Join | [api-evolution/join-sql.md](../02-core/multi-way-join-optimization.md) | Join 演进 |
| UDF | [api-evolution/udf-sql.md](../03-api/03.02-table-sql-api/flink-python-udf.md) | UDF 演进 |
| 物化视图 | [api-evolution/materialized-view.md](../03-api/03.02-table-sql-api/flink-materialized-table-deep-dive.md) | 物化视图 |

### 连接器演进

| 路径 | 描述 |
|------|------|
| [connectors/evolution/kafka-connector.md](../05-ecosystem/05.01-connectors/evolution/kafka-connector.md) | Kafka 连接器 |
| [connectors/evolution/cdc-connector.md](../05-ecosystem/05.01-connectors/evolution/cdc-connector.md) | CDC 连接器 |
| [connectors/evolution/jdbc-connector.md](../05-ecosystem/05.01-connectors/evolution/jdbc-connector.md) | JDBC 连接器 |
| [connectors/evolution/file-connector.md](../05-ecosystem/05.01-connectors/evolution/file-connector.md) | 文件连接器 |
| [connectors/evolution/lakehouse-connector.md](../05-ecosystem/05.01-connectors/evolution/lakehouse-connector.md) | Lakehouse 连接器 |
| [connectors/evolution/nosql-connector.md](../05-ecosystem/05.01-connectors/evolution/nosql-connector.md) | NoSQL 连接器 |
| [connectors/evolution/mq-connector.md](../05-ecosystem/05.01-connectors/evolution/mq-connector.md) | 消息队列连接器 |
| [connectors/evolution/cloud-connector.md](../05-ecosystem/05.01-connectors/evolution/cloud-connector.md) | 云连接器 |
| [connectors/evolution/custom-connector.md](../05-ecosystem/05.01-connectors/evolution/custom-connector.md) | 自定义连接器 |
| [connectors/evolution/connector-framework.md](../05-ecosystem/05.01-connectors/evolution/connector-framework.md) | 连接器框架 |

### 部署演进

| 路径 | 描述 |
|------|------|
| [04-runtime/04.01-deployment/evolution/standalone-deploy.md](../04-runtime/04.01-deployment/evolution/standalone-deploy.md) | Standalone 部署 |
| [04-runtime/04.01-deployment/evolution/yarn-deploy.md](../04-runtime/04.01-deployment/evolution/yarn-deploy.md) | YARN 部署 |
| [04-runtime/04.01-deployment/evolution/k8s-deploy.md](../04-runtime/04.01-deployment/evolution/k8s-deploy.md) | K8s 部署 |
| [04-runtime/04.01-deployment/evolution/cloud-deploy.md](../04-runtime/04.01-deployment/evolution/cloud-deploy.md) | 云部署 |
| [04-runtime/04.01-deployment/evolution/serverless-deploy.md](../04-runtime/04.01-deployment/evolution/serverless-deploy.md) | Serverless 部署 |
| [04-runtime/04.01-deployment/evolution/autoscaling-evolution.md](../04-runtime/04.01-deployment/evolution/autoscaling-evolution.md) | 自动扩缩容 |
| [04-runtime/04.01-deployment/evolution/ha-evolution.md](../04-runtime/04.01-deployment/evolution/ha-evolution.md) | 高可用演进 |
| [04-runtime/04.01-deployment/evolution/scheduling-evolution.md](../04-runtime/04.01-deployment/evolution/scheduling-evolution.md) | 调度演进 |
| [04-runtime/04.01-deployment/evolution/upgrade-strategy.md](../04-runtime/04.01-deployment/evolution/upgrade-strategy.md) | 升级策略 |
| [04-runtime/04.01-deployment/evolution/config-management.md](../04-runtime/04.01-deployment/evolution/config-management.md) | 配置管理 |

### 可观测性演进

| 路径 | 描述 |
|------|------|
| [04-runtime/04.03-observability/evolution/metrics-evolution.md](../04-runtime/04.03-observability/evolution/metrics-evolution.md) | 指标演进 |
| [04-runtime/04.03-observability/evolution/tracing-evolution.md](../04-runtime/04.03-observability/evolution/tracing-evolution.md) | 追踪演进 |
| [04-runtime/04.03-observability/evolution/logging-evolution.md](../04-runtime/04.03-observability/evolution/logging-evolution.md) | 日志演进 |
| [04-runtime/04.03-observability/evolution/alerting-evolution.md](../04-runtime/04.03-observability/evolution/alerting-evolution.md) | 告警演进 |
| [04-runtime/04.03-observability/evolution/profiling-evolution.md](../04-runtime/04.03-observability/evolution/profiling-evolution.md) | 性能分析 |
| [04-runtime/04.03-observability/evolution/webui-evolution.md](../04-runtime/04.03-observability/evolution/webui-evolution.md) | Web UI 演进 |
| [04-runtime/04.03-observability/evolution/debugging-evolution.md](../04-runtime/04.03-observability/evolution/debugging-evolution.md) | 调试演进 |
| [04-runtime/04.03-observability/evolution/testing-evolution.md](../04-runtime/04.03-observability/evolution/testing-evolution.md) | 测试演进 |
| [04-runtime/04.03-observability/evolution/obs-integration.md](../04-runtime/04.03-observability/evolution/obs-integration.md) | 集成演进 |
| [04-runtime/04.03-observability/evolution/slo-evolution.md](../04-runtime/04.03-observability/evolution/slo-evolution.md) | SLO 演进 |

### 安全演进

| 路径 | 描述 |
|------|------|
| [09-practices/09.04-security/evolution/auth-evolution.md](../09-practices/09.04-security/security/evolution/auth-evolution.md) | 认证演进 |
| [09-practices/09.04-security/evolution/authorization-evolution.md](../09-practices/09.04-security/security/evolution/authorization-evolution.md) | 授权演进 |
| [09-practices/09.04-security/evolution/encryption-evolution.md](../09-practices/09.04-security/security/evolution/encryption-evolution.md) | 加密演进 |
| [09-practices/09.04-security/evolution/key-management-evolution.md](../09-practices/09.04-security/security/evolution/key-management-evolution.md) | 密钥管理 |
| [09-practices/09.04-security/evolution/audit-evolution.md](../09-practices/09.04-security/security/evolution/audit-evolution.md) | 审计演进 |
| [09-practices/09.04-security/evolution/tee-evolution.md](../09-practices/09.04-security/security/evolution/tee-evolution.md) | TEE 演进 |
| [09-practices/09.04-security/evolution/security-policy-evolution.md](../09-practices/09.04-security/security/evolution/security-policy-evolution.md) | 安全策略 |
| [09-practices/09.04-security/evolution/compliance-evolution.md](../09-practices/09.04-security/security/evolution/compliance-evolution.md) | 合规演进 |
| [09-practices/09.04-security/evolution/data-governance-evolution.md](../09-practices/09.04-security/security/evolution/data-governance-evolution.md) | 数据治理 |
| [09-practices/09.04-security/evolution/lineage-evolution.md](../09-practices/09.04-security/security/evolution/lineage-evolution.md) | 血缘演进 |

### AI/ML 演进

| 路径 | 描述 |
|------|------|
| [06-ai-ml/evolution/ai-agent-24.md](../06-ai-ml/ai-ml/evolution/ai-agent-24.md) | AI Agent 2.4 |
| [06-ai-ml/evolution/ai-agent-25.md](../06-ai-ml/ai-ml/evolution/ai-agent-25.md) | AI Agent 2.5 |
| [06-ai-ml/evolution/ai-agent-30.md](../06-ai-ml/ai-ml/evolution/ai-agent-30.md) | AI Agent 3.0 |
| [06-ai-ml/evolution/llm-integration.md](../06-ai-ml/ai-ml/evolution/llm-integration.md) | LLM 集成 |
| [06-ai-ml/evolution/mcp-protocol.md](../06-ai-ml/ai-ml/evolution/mcp-protocol.md) | MCP 协议 |
| [06-ai-ml/evolution/a2a-protocol.md](../06-ai-ml/ai-ml/evolution/a2a-protocol.md) | A2A 协议 |
| [06-ai-ml/evolution/ml-inference.md](../06-ai-ml/ai-ml/evolution/ml-inference.md) | ML 推理 |
| [06-ai-ml/evolution/model-serving.md](../06-ai-ml/ai-ml/evolution/model-serving.md) | 模型服务 |
| [06-ai-ml/evolution/feature-store.md](../06-ai-ml/ai-ml/evolution/feature-store.md) | 特征存储 |
| [06-ai-ml/evolution/vector-search.md](../03-api/03.02-table-sql-api/vector-search.md) | 向量搜索 |

---

## 📊 快速参考文档

| 文档 | 描述 | 版本 |
|------|------|------|
| [built-in-functions-reference.md](../built-in-functions-reference.md) | 内置函数参考 | 1.17+ |
| [flink-built-in-functions-reference.md](../flink-built-in-functions-reference.md) | Flink 内置函数参考 | 1.17+ |
| [data-types-complete-reference.md](../data-types-complete-reference.md) | 数据类型参考 | 1.17+ |
| [flink-data-types-reference.md](../flink-data-types-reference.md) | Flink 数据类型参考 | 1.17+ |
| [flink-cep-complete-tutorial.md](../flink-cep-complete-tutorial.md) | CEP 完整教程 | 1.17+ |
| [state-backends-comparison.md](../state-backends-comparison.md) | State Backend 对比 | 1.17+ |
| [flink-state-backends-comparison.md](../flink-state-backends-comparison.md) | Flink State Backend 对比 | 1.17+ |
| [3.9-state-backends-deep-comparison.md](../3.9-state-backends-deep-comparison.md) | State Backend 深度对比 | 1.17+ |
| [version-tracking.md](version-tracking.md) | 版本追踪 | 全版本 |

---

## 🔗 导航链接

### 项目导航

- [📁 项目根目录](../../Knowledge/09-anti-patterns/README.md) - 返回项目主页
- [📖 项目英文 README](../../README-EN.md) - English README
- [📚 术语表](../../GLOSSARY.md) - 流计算术语表
- [📚 术语表(英文)](../../GLOSSARY.md) - Glossary (English)
- [🗺️ 学习路径](../../LEARNING-PATHS/00-INDEX.md) - 动态学习路径
- [📊 项目追踪](../../PROJECT-TRACKING.md) - 项目进度看板
- [🔍 搜索指南](../../SEARCH-GUIDE.md) - 如何高效搜索

### 其他专项索引

- [🧮 Struct 理论索引](../../Struct/00-INDEX.md) - 形式理论与分析
- [📘 Knowledge 知识索引](../../Struct/00-INDEX.md) - 工程知识与设计模式
- [🐍 03-api/09-language-foundations/00-INDEX.md](../../Struct/00-INDEX.md) - 语言基础子索引

### 辅助工具

- [🔧 定理注册表](../../THEOREM-REGISTRY.md) - 形式化元素注册表
- [📋 完成清单](../../PROJECT-TRACKING.md) - 项目完成状态
- [🗺️ 知识图谱](../../knowledge-graph.html) - 交互式知识图谱

---

## 📈 版本支持矩阵

| Flink 版本 | 状态 | 推荐度 | 主要特性 |
|-----------|------|--------|----------|
| 1.17.x | 维护中 | ⭐⭐⭐ | 稳定生产版本 |
| 1.18.x | 维护中 | ⭐⭐⭐⭐ | 自适应执行 |
| 1.19.x | 维护中 | ⭐⭐⭐⭐ | DataStream V2 |
| 2.0.x | 稳定版 | ⭐⭐⭐⭐⭐ | 架构重设计、ForSt |
| 2.1.x | 稳定版 | ⭐⭐⭐⭐⭐ | 异步执行 |
| 2.2.x | 最新稳定 | ⭐⭐⭐⭐⭐ | 前沿特性 |
| 2.3.x | 开发中 | ⭐⭐⭐⭐ | 即将发布 |
| 2.4.x | 预览版 | ⭐⭐⭐ | Serverless GA |
| 2.5.x | 预览版 | ⭐⭐⭐ | WASM UDF GA |
| 3.0.x | 规划中 | ⭐⭐ | 下一代架构 |

---

## 🎯 推荐阅读路径

### 初学者路径

1. [00-QUICK-START.md](00-QUICK-START.md) - 快速入门
2. [02-core/checkpoint-mechanism-deep-dive.md](../02-core/checkpoint-mechanism-deep-dive.md) - Checkpoint 机制
3. [02-core/time-semantics-and-watermark.md](../02-core/time-semantics-and-watermark.md) - 时间语义
4. [03-api/09-language-foundations/flink-datastream-api-complete-guide.md](../03-api/09-language-foundations/flink-datastream-api-complete-guide.md) - DataStream API
5. [03-api/03.02-table-sql-api/flink-table-sql-complete-guide.md](../03-api/03.02-table-sql-api/flink-table-sql-complete-guide.md) - SQL 指南

### 进阶开发者路径

1. [02-core/flink-state-management-complete-guide.md](../02-core/flink-state-management-complete-guide.md) - 状态管理
2. [02-core/exactly-once-semantics-deep-dive.md](../02-core/exactly-once-semantics-deep-dive.md) - Exactly-Once
3. [05-ecosystem/05.01-connectors/flink-connectors-ecosystem-complete-guide.md](../05-ecosystem/05.01-connectors/flink-connectors-ecosystem-complete-guide.md) - 连接器
4. [09-practices/09.03-performance-tuning/06.02-performance-optimization-complete.md](../09-practices/09.03-performance-tuning/06.02-performance-optimization-complete.md) - 性能优化
5. [04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md](../04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md) - 部署运维

### 架构师路径

1. [08-roadmap/08.01-flink-24/flink-version-evolution-complete-guide.md](../08-roadmap/08.01-flink-24/flink-version-evolution-complete-guide.md) - 版本演进
2. [01-concepts/deployment-architectures.md](../01-concepts/deployment-architectures.md) - 部署架构
3. [flink-24/], [flink-25/], [flink-30/] - 版本专题
4. [06-ai-ml/] - AI/ML 集成
5. [07-rust-native/] - Rust 生态

---

## 📝 维护信息

- **创建时间**: 2026-04-05
- **最后更新**: 2026-04-05
- **文档总数**: 350+ 篇
- **覆盖版本**: Flink 1.17 - 3.0
- **状态**: 持续更新中

---

## 🏷️ 标签说明

| 标签 | 含义 |
|------|------|
| ⭐ | 重点推荐 |
| 🔥 | 热门文档 |
| 🆕 | 新增内容 |
| 🧪 | 实验性特性 |
| ⚠️ | 注意事项 |

---

*本索引由 AnalysisDataFlow 项目自动生成并维护。如有遗漏或错误，请参考 [CONTRIBUTING.md](../../CONTRIBUTING.md) 提交反馈。*
