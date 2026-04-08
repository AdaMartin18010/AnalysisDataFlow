# AnalysisDataFlow — 综合导航索引

> **一站式导航中心** | 389篇技术文档 | 9,164+形式化元素 | 1,600+Mermaid图表

---

## 📋 目录

1. [快速入口导航](#1-快速入口导航)
2. [可视化文档导航](#2-可视化文档导航)
3. [文档类型索引](#3-文档类型索引)
4. [工具与资源导航](#4-工具与资源导航)
5. [学习资源导航](#5-学习资源导航)
6. [维护与贡献导航](#6-维护与贡献导航)

---

## 1. 快速入口导航

### 1.1 按角色入口

| 角色 | 推荐入口 | 核心关注点 |
|------|----------|------------|
| **架构师** | [Knowledge/04-technology-selection/engine-selection-guide.md](Knowledge/04-technology-selection/engine-selection-guide.md) | 技术选型、容量规划、成本模型 |
| | [Flink/01-concepts/deployment-architectures.md](Flink/01-concepts/deployment-architectures.md) | 部署架构、高可用设计 |
| | [Knowledge/03-business-patterns/data-mesh-streaming-architecture-2026.md](Knowledge/03-business-patterns/data-mesh-streaming-architecture-2026.md) | 数据网格、组织治理 |
| **开发工程师** | [Flink/02-core/checkpoint-mechanism-deep-dive.md](Flink/02-core/checkpoint-mechanism-deep-dive.md) | Checkpoint机制、容错实现 |
| | [Knowledge/02-design-patterns/](Knowledge/02-design-patterns/) | 设计模式、代码实践 |
| | [Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md](Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md) | 性能调优、问题诊断 |
| **研究员** | [Struct/01-foundation/01.01-unified-streaming-theory.md](Struct/01-foundation/01.01-unified-streaming-theory.md) | 统一流理论、形式化基础 |
| | [Struct/04-proofs/04.01-flink-checkpoint-correctness.md](Struct/04-proofs/04.01-flink-checkpoint-correctness.md) | 正确性证明、形式化验证 |
| | [Struct/07-tools/smart-casual-verification.md](Struct/07-tools/smart-casual-verification.md) | 前沿验证方法 |
| **学生/初学者** | [tutorials/00-5-MINUTE-QUICK-START.md](tutorials/00-5-MINUTE-QUICK-START.md) | 5分钟快速上手 |
| | [tutorials/02-first-flink-job.md](tutorials/02-first-flink-job.md) | 第一个Flink作业 |
| | [Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-spark-streaming.md](Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-spark-streaming.md) | 流计算入门、概念对比 |
| | [Knowledge/98-exercises/exercise-01-process-calculus.md](Knowledge/98-exercises/exercise-01-process-calculus.md) | 渐进式练习 |
| | [Knowledge/01-concept-atlas/streaming-models-mindmap.md](Knowledge/01-concept-atlas/streaming-models-mindmap.md) | 概念图谱 |
| **运维工程师** | [Flink/04-runtime/04.01-deployment/kubernetes-deployment-production-guide.md](Flink/04-runtime/04.01-deployment/kubernetes-deployment-production-guide.md) | K8s部署、生产运维 |
| | [Flink/04-runtime/04.03-observability/metrics-and-monitoring.md](Flink/04-runtime/04.03-observability/metrics-and-monitoring.md) | 监控指标、可观测性 |
| | [Flink/02-core/backpressure-and-flow-control.md](Flink/02-core/backpressure-and-flow-control.md) | 背压处理、流控机制 |

### 1.2 按主题入口

| 主题 | 核心文档 | 相关资源 |
|------|----------|----------|
| **理论基础** | [Struct/01-foundation/01.01-unified-streaming-theory.md](Struct/01-foundation/01.01-unified-streaming-theory.md) | USTM统一理论 |
| | [Struct/01-foundation/01.02-process-calculus-primer.md](Struct/01-foundation/01.02-process-calculus-primer.md) | 进程演算入门 |
| | [Struct/02-properties/02.02-consistency-hierarchy.md](Struct/02-properties/02.02-consistency-hierarchy.md) | 一致性层级 |
| **工程实践** | [Knowledge/02-design-patterns/](Knowledge/02-design-patterns/) | 8大设计模式 |
| | [Knowledge/09-anti-patterns/](Knowledge/09-anti-patterns/) | 10大反模式 |
| | [Knowledge/03-business-patterns/](Knowledge/03-business-patterns/) | 业务场景实践 |
| | [Knowledge/07-best-practices/](Knowledge/07-best-practices/) | 最佳实践 |
| **Flink专项** | [Flink/02-core/](Flink/02-core/) | 核心机制 |
| | [Flink/03-api/03.02-table-sql-api/](Flink/03-api/03.02-table-sql-api/) | SQL与Table API |
| | [Flink/05-ecosystem/05.01-connectors/](Flink/05-ecosystem/05.01-connectors/) | 连接器生态 |
| | [Flink/06-ai-ml/](Flink/06-ai-ml/) | AI/ML集成 |
| **前沿技术** | [Knowledge/06-frontier/realtime-ai-streaming-2026.md](Knowledge/06-frontier/realtime-ai-streaming-2026.md) | 实时AI流处理 |
| | [Knowledge/06-frontier/vector-search-streaming-convergence.md](Knowledge/06-frontier/vector-search-streaming-convergence.md) | 向量搜索集成 |
| | [Flink/06-ai-ml/flink-agents-flip-531.md](Flink/06-ai-ml/flink-agents-flip-531.md) | Flink AI Agents |
| | [Knowledge/06-frontier/streaming-lakehouse-iceberg-delta.md](Knowledge/06-frontier/streaming-lakehouse-iceberg-delta.md) | Streaming Lakehouse |
| | [Knowledge/06-frontier/mcp-protocol-agent-streaming.md](Knowledge/06-frontier/mcp-protocol-agent-streaming.md) | MCP协议 |
| | [Knowledge/06-frontier/a2a-protocol-agent-communication.md](Knowledge/06-frontier/a2a-protocol-agent-communication.md) | A2A协议 |

### 1.3 用户角色导航路径

针对不同用户背景，提供渐进式学习/工作路径：

#### 学术研究者路径

**阶段1 - 理论基础** (1-2天):

| 步骤 | 文档 | 预期产出 |
|------|------|---------|
| 1.1 | [Struct/00-INDEX.md](Struct/00-INDEX.md) | 了解形式化等级体系 |
| 1.2 | [Struct/01-foundation/01.01-unified-streaming-theory.md](Struct/01-foundation/01.01-unified-streaming-theory.md) | 掌握统一流理论框架 |
| 1.3 | [Struct/01-foundation/01.02-process-calculus-primer.md](Struct/01-foundation/01.02-process-calculus-primer.md) | 理解进程演算基础 |

**阶段2 - 形式证明** (2-3天):

| 步骤 | 文档 | 预期产出 |
|------|------|---------|
| 2.1 | [Struct/02-properties/02.02-consistency-hierarchy.md](Struct/02-properties/02.02-consistency-hierarchy.md) | 掌握一致性层级 |
| 2.2 | [Struct/04-proofs/04.01-flink-checkpoint-correctness.md](Struct/04-proofs/04.01-flink-checkpoint-correctness.md) | 理解Checkpoint正确性证明 |

**阶段3 - 前沿探索** (持续):

- [Struct/06-frontier/](Struct/06-frontier/) - 前沿研究
- [Struct/07-tools/smart-casual-verification.md](Struct/07-tools/smart-casual-verification.md) - 验证方法

#### 工程师路径

**阶段1 - 快速入门** (半天):

| 步骤 | 文档 | 预期产出 |
|------|------|---------|
| 1.1 | [tutorials/00-5-MINUTE-QUICK-START.md](tutorials/00-5-MINUTE-QUICK-START.md) | 建立基础概念 |
| 1.2 | [Knowledge/01-concept-atlas/streaming-models-mindmap.md](Knowledge/01-concept-atlas/streaming-models-mindmap.md) | 理解概念关系 |

**阶段2 - 设计模式** (1-2天):

| 步骤 | 文档 | 技能 |
|------|------|------|
| 2.1 | [Knowledge/02-design-patterns/pattern-event-time-processing.md](Knowledge/02-design-patterns/pattern-event-time-processing.md) | 事件时间处理 |
| 2.2 | [Knowledge/02-design-patterns/pattern-stateful-computation.md](Knowledge/02-design-patterns/pattern-stateful-computation.md) | 有状态计算 |
| 2.3 | [Knowledge/02-design-patterns/pattern-windowed-aggregation.md](Knowledge/02-design-patterns/pattern-windowed-aggregation.md) | 窗口聚合 |

**阶段3 - 避坑实践** (半天):

- [Knowledge/09-anti-patterns/](Knowledge/09-anti-patterns/) - 10大反模式
- [Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md](Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md) - 性能调优

**阶段4 - 项目实战** (1-2天):

- [tutorials/02-first-flink-job.md](tutorials/02-first-flink-job.md) - 第一个作业
- [CASE-STUDIES.md](CASE-STUDIES.md) - 案例研究

#### 架构师路径

**阶段1 - 全景认知** (半天):

| 步骤 | 文档 | 目标 |
|------|------|------|
| 1.1 | [README.md](README.md) | 项目概览 |
| 1.2 | [NAVIGATION-INDEX.md](NAVIGATION-INDEX.md) | 导航体系 |
| 1.3 | [visuals/matrix-engines.md](visuals/matrix-engines.md) | 引擎对比矩阵 |

**阶段2 - 技术选型** (1-2天):

| 步骤 | 文档 | 决策支持 |
|------|------|---------|
| 2.1 | [Knowledge/04-technology-selection/engine-selection-guide.md](Knowledge/04-technology-selection/engine-selection-guide.md) | 引擎选型决策树 |
| 2.2 | [Knowledge/04-technology-selection/flink-vs-risingwave.md](Knowledge/04-technology-selection/flink-vs-risingwave.md) | Flink vs RisingWave |
| 2.3 | [Struct/02-properties/02.02-consistency-hierarchy.md](Struct/02-properties/02.02-consistency-hierarchy.md) | 一致性选型 |

**阶段3 - 架构设计** (持续):

- [Flink/01-concepts/deployment-architectures.md](Flink/01-concepts/deployment-architectures.md) - 部署架构
- [Knowledge/03-business-patterns/data-mesh-streaming-architecture-2026.md](Knowledge/03-business-patterns/data-mesh-streaming-architecture-2026.md) - 数据网格
- [DEPLOYMENT-ARCHITECTURES.md](DEPLOYMENT-ARCHITECTURES.md) - 架构集

> **详细路径规划**: 参见 [QUICK-START-PATHS.md](QUICK-START-PATHS.md)

### 1.4 按问题入口

| 问题场景 | 诊断文档 | 解决方案 |
|----------|----------|----------|
| **Checkpoint失败** | [Flink/02-core/checkpoint-mechanism-deep-dive.md](Flink/02-core/checkpoint-mechanism-deep-dive.md) | 超时调优、增量配置 |
| | [Knowledge/09-anti-patterns/anti-pattern-03-checkpoint-interval-misconfig.md](Knowledge/09-anti-patterns/anti-pattern-03-checkpoint-interval-misconfig.md) | 间隔优化 |
| **背压问题** | [Flink/02-core/backpressure-and-flow-control.md](Flink/02-core/backpressure-and-flow-control.md) | 背压机制详解 |
| | [Knowledge/09-anti-patterns/anti-pattern-08-ignoring-backpressure.md](Knowledge/09-anti-patterns/anti-pattern-08-ignoring-backpressure.md) | 背压处理策略 |
| **数据倾斜** | [Knowledge/09-anti-patterns/anti-pattern-04-hot-key-skew.md](Knowledge/09-anti-patterns/anti-pattern-04-hot-key-skew.md) | 热点Key处理 |
| | [Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md](Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md) | 分区优化 |
| **Exactly-Once保证** | [Flink/02-core/exactly-once-semantics-deep-dive.md](Flink/02-core/exactly-once-semantics-deep-dive.md) | 端到端语义 |
| | [Struct/04-proofs/04.02-flink-exactly-once-correctness.md](Struct/04-proofs/04.02-flink-exactly-once-correctness.md) | 正确性证明 |
| **Watermark设置** | [Flink/02-core/time-semantics-and-watermark.md](Flink/02-core/time-semantics-and-watermark.md) | 时间语义详解 |
| | [Knowledge/09-anti-patterns/anti-pattern-02-watermark-misconfiguration.md](Knowledge/09-anti-patterns/anti-pattern-02-watermark-misconfiguration.md) | 配置优化 |
| **OOM问题** | [Knowledge/09-anti-patterns/anti-pattern-07-window-state-explosion.md](Knowledge/09-anti-patterns/anti-pattern-07-window-state-explosion.md) | 窗口状态管理 |
| | [Knowledge/09-anti-patterns/anti-pattern-10-resource-estimation-oom.md](Knowledge/09-anti-patterns/anti-pattern-10-resource-estimation-oom.md) | 资源估算 |
| **多流Join** | [Flink/02-core/delta-join.md](Flink/02-core/delta-join.md) | Delta Join优化 |
| | [Knowledge/09-anti-patterns/anti-pattern-09-multi-stream-join-misalignment.md](Knowledge/09-anti-patterns/anti-pattern-09-multi-stream-join-misalignment.md) | Join对齐策略 |
| **技术选型** | [Knowledge/04-technology-selection/engine-selection-guide.md](Knowledge/04-technology-selection/engine-selection-guide.md) | 引擎选型决策树 |
| | [Knowledge/04-technology-selection/flink-vs-risingwave.md](Knowledge/04-technology-selection/flink-vs-risingwave.md) | Flink vs RisingWave |
| | [Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-spark-streaming.md](Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-spark-streaming.md) | Flink vs Spark |

---

## 2. 可视化文档导航

### 2.1 决策树导航 (8个)

| 决策树 | 文档路径 | 适用场景 |
|--------|----------|----------|
| **流处理引擎选型决策树** | [Knowledge/04-technology-selection/engine-selection-guide.md](Knowledge/04-technology-selection/engine-selection-guide.md) | 选择Flink/Spark/Kafka Streams |
| **状态后端选型决策树** | [Flink/09-practices/09.03-performance-tuning/state-backend-selection.md](Flink/09-practices/09.03-performance-tuning/state-backend-selection.md) | RocksDB/HashMap/Forst选择 |
| **部署模式决策树** | [Flink/01-concepts/deployment-architectures.md](Flink/01-concepts/deployment-architectures.md) | Standalone/YARN/K8s选择 |
| **一致性级别决策树** | [Struct/02-properties/02.02-consistency-hierarchy.md](Struct/02-properties/02.02-consistency-hierarchy.md) | At-Most-Once/At-Least-Once/Exactly-Once选择 |
| **技术范式决策树** | [Knowledge/04-technology-selection/paradigm-selection-guide.md](Knowledge/04-technology-selection/paradigm-selection-guide.md) | Dataflow/Actor/CSP选择 |
| **存储选型决策树** | [Knowledge/04-technology-selection/storage-selection-guide.md](Knowledge/04-technology-selection/storage-selection-guide.md) | 状态存储选择 |
| **流数据库选型决策树** | [Knowledge/04-technology-selection/streaming-database-guide.md](Knowledge/04-technology-selection/streaming-database-guide.md) | RisingWave/Materialize选择 |
| **AI Agent架构决策树** | [Knowledge/06-frontier/ai-agent-streaming-architecture.md](Knowledge/06-frontier/ai-agent-streaming-architecture.md) | Agent架构选择 |

### 2.2 矩阵对比导航 (8个)

| 对比矩阵 | 文档路径 | 对比维度 |
|----------|----------|----------|
| **并发范式对比矩阵** | [Knowledge/01-concept-atlas/concurrency-paradigms-matrix.md](Knowledge/01-concept-atlas/concurrency-paradigms-matrix.md) | Actor/CSP/Dataflow/π-calculus |
| **Flink vs Spark Streaming** | [Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-spark-streaming.md](Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-spark-streaming.md) | 架构/语义/性能/生态 |
| **Flink vs RisingWave** | [Knowledge/04-technology-selection/flink-vs-risingwave.md](Knowledge/04-technology-selection/flink-vs-risingwave.md) | 架构/成本/适用场景 |
| **流数据库生态对比** | [Knowledge/06-frontier/streaming-database-ecosystem-comparison.md](Knowledge/06-frontier/streaming-database-ecosystem-comparison.md) | RisingWave/Materialize/Timeplus |
| **Rust流处理生态对比** | [Knowledge/06-frontier/rust-streaming-ecosystem.md](Knowledge/06-frontier/rust-streaming-ecosystem.md) | Arroyo/RisingWave/Timeplus |
| **Streaming Lakehouse格式对比** | [Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-architecture.md](Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-architecture.md) | Iceberg/Delta/Paimon |
| **多Agent框架对比** | [Knowledge/05-mapping-guides/multi-agent-frameworks-2026-comparison.md](Knowledge/05-mapping-guides/multi-agent-frameworks-2026-comparison.md) | A2A/MCP/ACP |
| **Streaming SQL引擎对比** | [Knowledge/05-mapping-guides/streaming-sql-engines-2026-comparison.md](Knowledge/05-mapping-guides/streaming-sql-engines-2026-comparison.md) | Flink SQL/RisingWave SQL |

### 2.3 关系图导航 (8个)

| 关系图 | 文档路径 | 展示内容 |
|--------|----------|----------|
| **流计算概念图谱** | [Knowledge/01-concept-atlas/streaming-models-mindmap.md](Knowledge/01-concept-atlas/streaming-models-mindmap.md) | 概念层次关系 |
| **Actor到CSP编码关系** | [Struct/03-relationships/03.01-actor-to-csp-encoding.md](Struct/03-relationships/03.01-actor-to-csp-encoding.md) | 模型转换关系 |
| **Flink到进程演算映射** | [Struct/03-relationships/03.02-flink-to-process-calculus.md](Struct/03-relationships/03.02-flink-to-process-calculus.md) | 语义映射关系 |
| **表达能力层次图** | [Struct/03-relationships/03.03-expressiveness-hierarchy.md](Struct/03-relationships/03.03-expressiveness-hierarchy.md) | 模型表达能力关系 |
| **Struct到Flink映射** | [Knowledge/05-mapping-guides/struct-to-flink-mapping.md](Knowledge/05-mapping-guides/struct-to-flink-mapping.md) | 理论到实现映射 |
| **形式化到代码模式映射** | [Knowledge/05-mapping-guides/theory-to-code-patterns.md](Knowledge/05-mapping-guides/theory-to-code-patterns.md) | 理论到代码映射 |
| **流处理生态系统图** | [Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md](Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md) | 生态组件关系 |
| **Streaming ETL工具全景** | [Knowledge/05-mapping-guides/streaming-etl-tools-landscape-2026.md](Knowledge/05-mapping-guides/streaming-etl-tools-landscape-2026.md) | ETL工具关系 |

### 2.4 综合可视化导航 (8个)

| 可视化 | 文档路径 | 图表类型 |
|--------|----------|----------|
| **Chandy-Lamport算法执行树** | [Struct/04-proofs/04.03-chandy-lamport-consistency.md](Struct/04-proofs/04.03-chandy-lamport-consistency.md) | 状态图/时序图 |
| **Checkpoint状态机** | [Flink/02-core/checkpoint-mechanism-deep-dive.md](Flink/02-core/checkpoint-mechanism-deep-dive.md) | 状态图 |
| **Watermark传播图** | [Struct/04-proofs/04.04-watermark-algebra-formal-proof.md](Struct/04-proofs/04.04-watermark-algebra-formal-proof.md) | 代数图/时序图 |
| **Flink 1.x vs 2.0架构对比** | [Flink/01-concepts/flink-1.x-vs-2.0-comparison.md](Flink/01-concepts/flink-1.x-vs-2.0-comparison.md) | 架构图对比 |
| **Flink 2.3路线图** | [Flink/08-roadmap/08.01-flink-24/flink-2.3-2.4-roadmap.md](Flink/08-roadmap/08.01-flink-24/flink-2.3-2.4-roadmap.md) | 甘特图/路线图 |
| **Streaming Lakehouse架构** | [Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-architecture.md](Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-architecture.md) | 分层架构图 |
| **实时AI流处理架构** | [Knowledge/06-frontier/multimodal-streaming-architecture.md](Knowledge/06-frontier/multimodal-streaming-architecture.md) | 多模态架构图 |
| **RAG流式架构** | [Flink/06-ai-ml/rag-streaming-architecture.md](Flink/06-ai-ml/rag-streaming-architecture.md) | 系统架构图 |

---

## 3. 文档类型索引

### 3.1 形式化理论文档索引 (Struct/)

#### 基础理论 (01-foundation/)

| 文档 | 编号 | 核心定理/定义 |
|------|------|---------------|
| [统一流计算理论](Struct/01-foundation/01.01-unified-streaming-theory.md) | S-01 | Def-S-01-01~12, Thm-S-01-01~03 |
| [进程演算入门](Struct/01-foundation/01.02-process-calculus-primer.md) | S-02 | Def-S-02-01~08 |
| [Actor模型形式化](Struct/01-foundation/01.03-actor-model-formalization.md) | S-03 | Def-S-03-01~06 |
| [Dataflow模型形式化](Struct/01-foundation/01.04-dataflow-model-formalization.md) | S-04 | Def-S-04-01~10 |
| [CSP形式化](Struct/01-foundation/01.05-csp-formalization.md) | S-05 | Def-S-05-01~07 |
| [Petri网形式化](Struct/01-foundation/01.06-petri-net-formalization.md) | S-06 | Def-S-06-01~05 |
| [Session Types](Struct/01-foundation/01.07-session-types.md) | S-07 | Def-S-07-01~08 |

#### 性质推导 (02-properties/)

| 文档 | 编号 | 核心定理/定义 |
|------|------|---------------|
| [流处理确定性](Struct/02-properties/02.01-determinism-in-streaming.md) | S-08 | Thm-S-08-01~02 |
| [一致性层级](Struct/02-properties/02.02-consistency-hierarchy.md) | S-09 | Def-S-09-01~04, Thm-S-09-01 |
| [Watermark单调性](Struct/02-properties/02.03-watermark-monotonicity.md) | S-10 | Lemma-S-10-01~03 |
| [活性与安全](Struct/02-properties/02.04-liveness-and-safety.md) | S-11 | Def-S-11-01~02 |
| [类型安全推导](Struct/02-properties/02.05-type-safety-derivation.md) | S-12 | Thm-S-12-01 |
| [CALM定理](Struct/02-properties/02.06-calm-theorem.md) | S-13 | Thm-S-13-01 |
| [加密流处理](Struct/02-properties/02.07-encrypted-stream-processing.md) | S-14 | Def-S-14-01~03 |
| [差分隐私](Struct/02-properties/02.08-differential-privacy-streaming.md) | S-15 | Def-S-15-01~04 |

#### 形式证明 (04-proofs/)

| 文档 | 编号 | 核心定理 |
|------|------|----------|
| [Checkpoint正确性证明](Struct/04-proofs/04.01-flink-checkpoint-correctness.md) | S-17 | Thm-S-17-01~03 |
| [Exactly-Once正确性证明](Struct/04-proofs/04.02-flink-exactly-once-correctness.md) | S-18 | Thm-S-18-01~02 |
| [Chandy-Lamport一致性](Struct/04-proofs/04.03-chandy-lamport-consistency.md) | S-19 | Thm-S-19-01 |
| [Watermark代数证明](Struct/04-proofs/04.04-watermark-algebra-formal-proof.md) | S-20 | Thm-S-20-01~04 |
| [FG/FGG类型安全](Struct/04-proofs/04.05-type-safety-fg-fgg.md) | S-21 | Thm-S-21-01 |
| [DOT子类型完备性](Struct/04-proofs/04.06-dot-subtyping-completeness.md) | S-22 | Thm-S-22-01 |

#### 验证工具 (07-tools/)

| 文档 | 编号 | 核心内容 |
|------|------|----------|
| [Smart Casual Verification](Struct/07-tools/smart-casual-verification.md) | S-24 | 轻量级形式化验证 |
| [TLA+ for Flink](Struct/07-tools/tla-for-flink.md) | S-25 | TLA+规范 |
| [Coq Mechanization](Struct/07-tools/coq-mechanization.md) | S-26 | Coq形式化 |
| [Iris Separation Logic](Struct/07-tools/iris-separation-logic.md) | S-27 | Iris分离逻辑 |
| [Model Checking Practice](Struct/07-tools/model-checking-practice.md) | S-28 | 模型检测实践 |

### 3.2 工程实践文档索引 (Knowledge/)

#### 设计模式 (02-design-patterns/)

| 模式 | 文档 | 应用场景 |
|------|------|----------|
| 事件时间处理 | [pattern-event-time-processing.md](Knowledge/02-design-patterns/pattern-event-time-processing.md) | 乱序数据处理 |
| 窗口聚合 | [pattern-windowed-aggregation.md](Knowledge/02-design-patterns/pattern-windowed-aggregation.md) | 时间窗口计算 |
| 状态计算 | [pattern-stateful-computation.md](Knowledge/02-design-patterns/pattern-stateful-computation.md) | 有状态处理 |
| 异步IO富化 | [pattern-async-io-enrichment.md](Knowledge/02-design-patterns/pattern-async-io-enrichment.md) | 外部数据查询 |
| 复杂事件处理 | [pattern-cep-complex-event.md](Knowledge/02-design-patterns/pattern-cep-complex-event.md) | 模式匹配 |
| 旁路输出 | [pattern-side-output.md](Knowledge/02-design-patterns/pattern-side-output.md) | 分流处理 |
| Checkpoint恢复 | [pattern-checkpoint-recovery.md](Knowledge/02-design-patterns/pattern-checkpoint-recovery.md) | 容错恢复 |
| 实时特征工程 | [pattern-realtime-feature-engineering.md](Knowledge/02-design-patterns/pattern-realtime-feature-engineering.md) | ML特征生成 |

#### 业务场景 (03-business-patterns/)

| 场景 | 文档 | 技术要点 |
|------|------|----------|
| 金融实时风控 | [fintech-realtime-risk-control.md](Knowledge/03-business-patterns/fintech-realtime-risk-control.md) | 低延迟、规则引擎 |
| 电商实时推荐 | [real-time-recommendation.md](Knowledge/03-business-patterns/real-time-recommendation.md) | 特征实时化 |
| 物联网处理 | [iot-stream-processing.md](Knowledge/03-business-patterns/iot-stream-processing.md) | 边缘计算、海量设备 |
| 日志监控 | [log-monitoring.md](Knowledge/03-business-patterns/log-monitoring.md) | 实时告警、日志分析 |
| 游戏分析 | [gaming-analytics.md](Knowledge/03-business-patterns/gaming-analytics.md) | 实时指标、玩家行为 |
| 阿里巴巴双11 | [alibaba-double11-flink.md](Knowledge/03-business-patterns/alibaba-double11-flink.md) | 超大规模 |
| Netflix流水线 | [netflix-streaming-pipeline.md](Knowledge/03-business-patterns/netflix-streaming-pipeline.md) | 实时个性化 |
| Uber实时平台 | [uber-realtime-platform.md](Knowledge/03-business-patterns/uber-realtime-platform.md) | 实时定价 |
| Stripe支付处理 | [stripe-payment-processing.md](Knowledge/03-business-patterns/stripe-payment-processing.md) | 金融级一致性 |
| Spotify推荐 | [spotify-music-recommendation.md](Knowledge/03-business-patterns/spotify-music-recommendation.md) | 实时音乐推荐 |
| Airbnb市场 | [airbnb-marketplace-dynamics.md](Knowledge/03-business-patterns/airbnb-marketplace-dynamics.md) | 市场动态定价 |
| 数据网格 | [data-mesh-streaming-architecture-2026.md](Knowledge/03-business-patterns/data-mesh-streaming-architecture-2026.md) | 数据产品架构 |

#### 反模式 (09-anti-patterns/)

| 反模式 | 文档 | 风险等级 |
|--------|------|----------|
| 全局状态滥用 | [anti-pattern-01-global-state-abuse.md](Knowledge/09-anti-patterns/anti-pattern-01-global-state-abuse.md) | 🔴 高 |
| Watermark配置不当 | [anti-pattern-02-watermark-misconfiguration.md](Knowledge/09-anti-patterns/anti-pattern-02-watermark-misconfiguration.md) | 🔴 高 |
| Checkpoint间隔不合理 | [anti-pattern-03-checkpoint-interval-misconfig.md](Knowledge/09-anti-patterns/anti-pattern-03-checkpoint-interval-misconfig.md) | 🟡 中 |
| 热点Key未处理 | [anti-pattern-04-hot-key-skew.md](Knowledge/09-anti-patterns/anti-pattern-04-hot-key-skew.md) | 🔴 高 |
| ProcessFunction阻塞IO | [anti-pattern-05-blocking-io-processfunction.md](Knowledge/09-anti-patterns/anti-pattern-05-blocking-io-processfunction.md) | 🟡 中 |
| 序列化开销忽视 | [anti-pattern-06-serialization-overhead.md](Knowledge/09-anti-patterns/anti-pattern-06-serialization-overhead.md) | 🟢 低 |
| 窗口状态爆炸 | [anti-pattern-07-window-state-explosion.md](Knowledge/09-anti-patterns/anti-pattern-07-window-state-explosion.md) | 🔴 高 |
| 忽略背压信号 | [anti-pattern-08-ignoring-backpressure.md](Knowledge/09-anti-patterns/anti-pattern-08-ignoring-backpressure.md) | 🔴 高 |
| 多流Join未对齐 | [anti-pattern-09-multi-stream-join-misalignment.md](Knowledge/09-anti-patterns/anti-pattern-09-multi-stream-join-misalignment.md) | 🟡 中 |
| 资源估算OOM | [anti-pattern-10-resource-estimation-oom.md](Knowledge/09-anti-patterns/anti-pattern-10-resource-estimation-oom.md) | 🔴 高 |

### 3.3 Flink专项文档索引 (Flink/)

#### 核心机制 (02-core-mechanisms/)

| 主题 | 文档 | 关键内容 |
|------|------|----------|
| Checkpoint机制 | [checkpoint-mechanism-deep-dive.md](Flink/02-core/checkpoint-mechanism-deep-dive.md) | Barrier算法、增量Checkpoint |
| Exactly-Once语义 | [exactly-once-semantics-deep-dive.md](Flink/02-core/exactly-once-semantics-deep-dive.md) | 两阶段提交、事务Sink |
| 背压与流控 | [backpressure-and-flow-control.md](Flink/02-core/backpressure-and-flow-control.md) | 信用值机制、反压传播 |
| 时间语义 | [time-semantics-and-watermark.md](Flink/02-core/time-semantics-and-watermark.md) | Event Time/Processing Time |
| Delta Join | [delta-join.md](Flink/02-core/delta-join.md) | 大状态Join优化 |
| Async执行模型 | [async-execution-model.md](Flink/02-core/async-execution-model.md) | Flink 2.0新特性 |
| ForState Backend | [forst-state-backend.md](Flink/02-core/forst-state-backend.md) | 云原生状态存储 |
| 智能Checkpoint | [smart-checkpointing-strategies.md](Flink/02-core/smart-checkpointing-strategies.md) | 自适应策略 |

#### SQL与Table API (03-sql-table-api/)

| 主题 | 文档 | 关键内容 |
|------|------|----------|
| 窗口函数 | [flink-sql-window-functions-deep-dive.md](Flink/03-api/03.02-table-sql-api/flink-sql-window-functions-deep-dive.md) | TUMBLE/HOP/SESSION |
| 查询优化 | [flink-sql-calcite-optimizer-deep-dive.md](Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md) | Calcite优化器 |
| SQL Hints | [flink-sql-hints-optimization.md](Flink/03-api/03.02-table-sql-api/flink-sql-hints-optimization.md) | 执行计划调优 |
| Model DDL | [model-ddl-and-ml-predict.md](Flink/03-api/03.02-table-sql-api/model-ddl-and-ml-predict.md) | AI推理集成 |
| 向量搜索 | [flink-vector-search-rag.md](Flink/03-api/03.02-table-sql-api/flink-vector-search-rag.md) | VECTOR_SEARCH函数 |
| 物化表 | [materialized-tables.md](Flink/03-api/03.02-table-sql-api/materialized-tables.md) | FRESHNESS语义 |
| SQL速查表 | [sql-functions-cheatsheet.md](Flink/03-api/03.02-table-sql-api/sql-functions-cheatsheet.md) | 150+函数速查 |

#### 连接器生态 (04-connectors/)

| 连接器 | 文档 | 特性 |
|--------|------|------|
| Kafka集成 | [kafka-integration-patterns.md](Flink/05-ecosystem/05.01-connectors/kafka-integration-patterns.md) | Source/Sink、精确一次 |
| CDC Debezium | [04.04-cdc-debezium-integration.md](Flink/05-ecosystem/05.01-connectors/04.04-cdc-debezium-integration.md) | 变更数据捕获 |
| Flink CDC 3.0 | [flink-cdc-3.0-data-integration.md](Flink/05-ecosystem/05.01-connectors/flink-cdc-3.0-data-integration.md) | 数据集成框架 |
| Iceberg | [flink-iceberg-integration.md](Flink/05-ecosystem/05.01-connectors/flink-iceberg-integration.md) | Lakehouse集成 |
| Paimon | [flink-paimon-integration.md](Flink/05-ecosystem/05.01-connectors/flink-paimon-integration.md) | 流式数据湖 |
| Delta Lake | [flink-delta-lake-integration.md](Flink/05-ecosystem/05.01-connectors/flink-delta-lake-integration.md) | Delta格式支持 |
| Apache Fluss | [fluss-integration.md](Flink/05-ecosystem/05.01-connectors/fluss-integration.md) | 流分析存储 |
| CloudEvents | [cloudevents-integration-guide.md](Flink/05-ecosystem/05.01-connectors/cloudevents-integration-guide.md) | CNCF标准集成 |

#### 部署与运维 (10-deployment/)

| 主题 | 文档 | 关键内容 |
|------|------|----------|
| K8s生产部署 | [kubernetes-deployment-production-guide.md](Flink/04-runtime/04.01-deployment/kubernetes-deployment-production-guide.md) | Operator、HA配置 |
| K8s Autoscaler | [flink-kubernetes-autoscaler-deep-dive.md](Flink/04-runtime/04.01-deployment/flink-kubernetes-autoscaler-deep-dive.md) | 自动扩缩容 |
| Serverless架构 | [flink-serverless-architecture.md](Flink/04-runtime/04.01-deployment/flink-serverless-architecture.md) | 无服务器部署 |
| Serverless GA | [serverless-flink-ga-guide.md](Flink/04-runtime/04.01-deployment/serverless-flink-ga-guide.md) | 完全指南 |
| 多云部署模板 | [multi-cloud-deployment-templates.md](Flink/04-runtime/04.01-deployment/multi-cloud-deployment-templates.md) | 5大云平台模板 |
| 成本优化计算器 | [cost-optimization-calculator.md](Flink/04-runtime/04.01-deployment/cost-optimization-calculator.md) | Python成本工具 |

#### AI/ML集成 (12-ai-ml/)

| 主题 | 文档 | 关键内容 |
|------|------|----------|
| Flink AI Agents | [flink-agents-flip-531.md](Flink/06-ai-ml/flink-agents-flip-531.md) | FLIP-531原生Agent |
| LLM集成 | [flink-llm-integration.md](Flink/06-ai-ml/flink-llm-integration.md) | 大模型集成 |
| 实时推理 | [flink-realtime-ml-inference.md](Flink/06-ai-ml/flink-realtime-ml-inference.md) | 在线预测 |
| 特征工程 | [realtime-feature-engineering-feature-store.md](Flink/06-ai-ml/realtime-feature-engineering-feature-store.md) | 特征平台 |
| 向量数据库 | [vector-database-integration.md](Flink/06-ai-ml/vector-database-integration.md) | Milvus/Pinecone |
| RAG架构 | [rag-streaming-architecture.md](Flink/06-ai-ml/rag-streaming-architecture.md) | 检索增强生成 |
| 在线学习 | [online-learning-algorithms.md](Flink/06-ai-ml/online-learning-algorithms.md) | 增量学习 |
| AI Agents GA | [flip-531-ai-agents-ga-guide.md](Flink/06-ai-ml/flip-531-ai-agents-ga-guide.md) | 生产级发布 |

### 3.4 前沿技术文档索引 (Knowledge/06-frontier/ & Flink/前沿/)

| 技术方向 | 文档 | 成熟度 |
|----------|------|--------|
| **AI Agent流处理** | [ai-agent-streaming-architecture.md](Knowledge/06-frontier/ai-agent-streaming-architecture.md) | 🔶 新兴 |
| | [Flink/06-ai-ml/flink-agents-flip-531.md](Flink/06-ai-ml/flink-agents-flip-531.md) | 🔶 新兴 |
| **MCP协议** | [mcp-protocol-agent-streaming.md](Knowledge/06-frontier/mcp-protocol-agent-streaming.md) | 🔶 新兴 |
| **A2A协议** | [a2a-protocol-agent-communication.md](Knowledge/06-frontier/a2a-protocol-agent-communication.md) | 🔶 新兴 |
| **多模态流处理** | [multimodal-streaming-architecture.md](Knowledge/06-frontier/multimodal-streaming-architecture.md) | 🔶 新兴 |
| **实时RAG** | [real-time-rag-architecture.md](Knowledge/06-frontier/real-time-rag-architecture.md) | 🔷 成熟 |
| | [Flink/06-ai-ml/rag-streaming-architecture.md](Flink/06-ai-ml/rag-streaming-architecture.md) | 🔷 成熟 |
| **Streaming Lakehouse** | [streaming-lakehouse-iceberg-delta.md](Knowledge/06-frontier/streaming-lakehouse-iceberg-delta.md) | 🔷 成熟 |
| | [Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-architecture.md](Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-architecture.md) | 🔷 成熟 |
| **流数据库** | [streaming-databases.md](Knowledge/06-frontier/streaming-databases.md) | 🔷 成熟 |
| | [risingwave-deep-dive.md](Knowledge/06-frontier/risingwave-deep-dive.md) | 🔷 成熟 |
| **实时特征平台** | [realtime-feature-store-architecture.md](Knowledge/06-frontier/realtime-feature-store-architecture.md) | 🔷 成熟 |
| **边缘流处理** | [edge-streaming-architecture.md](Knowledge/06-frontier/edge-streaming-architecture.md) | 🔶 新兴 |
| | [edge-llm-realtime-inference.md](Knowledge/06-frontier/edge-llm-realtime-inference.md) | 🔶 新兴 |
| **实时数据网格** | [realtime-data-mesh-practice.md](Knowledge/06-frontier/realtime-data-mesh-practice.md) | 🔷 成熟 |
| **Serverless流处理** | [serverless-stream-processing-architecture.md](Knowledge/06-frontier/serverless-stream-processing-architecture.md) | 🔷 成熟 |
| **实时图流处理** | [streaming-graph-processing-tgn.md](Knowledge/06-frontier/streaming-graph-processing-tgn.md) | 🔶 新兴 |
| | [realtime-graph-streaming-tgnn.md](Knowledge/06-frontier/realtime-graph-streaming-tgnn.md) | 🔶 新兴 |
| **WebAssembly数据流** | [wasm-dataflow-patterns.md](Knowledge/06-frontier/wasm-dataflow-patterns.md) | 🔶 新兴 |
| **Rust流处理生态** | [rust-streaming-ecosystem.md](Knowledge/06-frontier/rust-streaming-ecosystem.md) | 🔷 成熟 |
| **GPU可信执行** | [Flink/09-practices/09.04-security/gpu-confidential-computing.md](Flink/09-practices/09.04-security/gpu-confidential-computing.md) | 🔶 新兴 |
| **Temporal+Flink** | [temporal-flink-layered-architecture.md](Knowledge/06-frontier/temporal-flink-layered-architecture.md) | 🔶 新兴 |

---

## 4. 工具与资源导航

### 4.1 自动化脚本工具 (.scripts/)

| 脚本类型 | 路径 | 功能 | 状态 |
|----------|------|------|------|
| **Flink版本跟踪** | `.scripts/flink-version-tracking/` | 监控Flink官方发布，自动更新版本文档 | ✅ 运行中 |
| **链接检查器** | `.scripts/link-checker/` | 检测失效链接，生成修复建议 | ✅ 运行中 |
| **质量门禁** | `.scripts/quality-gates/` | 文档格式检查、前瞻内容检测 | ✅ 运行中 |
| **统计更新** | `.scripts/stats-updater/` | 自动更新项目统计和进度 | ✅ 运行中 |
| **通知服务** | `.scripts/notifications/` | 变更通知(Slack/邮件/Webhook) | ✅ 运行中 |
| **版本对比** | `.scripts/version-comparison/` | 生成版本差异报告 | ✅ 运行中 |

### 4.2 CI/CD 工作流 (.github/workflows/)

| 工作流 | 文件 | 触发条件 | 功能 |
|--------|------|----------|------|
| **项目验证** | `validate.yml` | PR/Push | 文档结构、引用完整性 |
| **链接检查** | `check-links.yml` | 定时/手动 | 死链检测 |
| **统计更新** | `update-stats.yml` | 定时 | 文档数量、定理统计 |

### 4.3 Docker环境入口

| 环境 | 文档 | 用途 |
|------|------|------|
| Flink本地开发 | [Flink/04-runtime/04.01-deployment/kubernetes-deployment.md](Flink/04-runtime/04.01-deployment/kubernetes-deployment.md) | 本地K8s部署 |
| 流处理实验环境 | [tutorials/interactive/README.md](tutorials/interactive/README.md) | 练习环境 |

### 4.4 搜索工具入口

| 搜索方式 | 方法 | 示例 |
|----------|------|------|
| **全文搜索** | GitHub搜索 | `repo:luyanfeng/AnalysisDataFlow checkpoint` |
| **定理编号搜索** | THEOREM-REGISTRY.md | 查找 `Thm-S-17-01` |
| **目录索引** | 00-INDEX.md | [Struct/00-INDEX.md](Struct/00-INDEX.md) |
| | | [Knowledge/00-INDEX.md](Knowledge/00-INDEX.md) |
| | | [Flink/00-INDEX.md](Flink/00-INDEX.md) |

### 4.5 PDF导出入口

> 目前项目以Markdown为主，PDF导出可通过以下方式：

| 方法 | 工具 | 说明 |
|------|------|------|
| Markdown转PDF | Pandoc | `pandoc input.md -o output.pdf` |
| VSCode插件 | Markdown PDF | 右键导出 |
| 批量导出 | 自定义脚本 | 遍历所有md文件 |

---

## 5. 学习资源导航

### 5.1 快速上手指南

| 难度 | 指南 | 预计时间 |
|------|------|----------|
| 🟢 入门级 | [tutorials/00-5-MINUTE-QUICK-START.md](tutorials/00-5-MINUTE-QUICK-START.md) | 5分钟 |
| 🟢 入门级 | [tutorials/01-environment-setup.md](tutorials/01-environment-setup.md) | 30分钟 |
| 🟢 入门级 | [tutorials/02-first-flink-job.md](tutorials/02-first-flink-job.md) | 1小时 |
| 🟢 入门级 | [Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-spark-streaming.md](Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-spark-streaming.md) | 1小时 |
| 🟢 入门级 | [Knowledge/01-concept-atlas/streaming-models-mindmap.md](Knowledge/01-concept-atlas/streaming-models-mindmap.md) | 30分钟 |
| 🟡 中级 | [Flink/02-core/time-semantics-and-watermark.md](Flink/02-core/time-semantics-and-watermark.md) | 2小时 |
| 🟡 中级 | [Knowledge/02-design-patterns/pattern-event-time-processing.md](Knowledge/02-design-patterns/pattern-event-time-processing.md) | 2小时 |
| 🔴 高级 | [Struct/04-proofs/04.01-flink-checkpoint-correctness.md](Struct/04-proofs/04.01-flink-checkpoint-correctness.md) | 4小时 |
| 🔴 高级 | [Flink/02-core/checkpoint-mechanism-deep-dive.md](Flink/02-core/checkpoint-mechanism-deep-dive.md) | 4小时 |

### 5.2 学习路径引导

#### 初学者路径 (2-3周)

```
Week 1: tutorials/00-5-MINUTE-QUICK-START.md (5分钟快速体验)
        → tutorials/01-environment-setup.md (环境搭建)
        → tutorials/02-first-flink-job.md (第一个Flink作业)
Week 2: Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-spark-streaming.md
        → Knowledge/01-concept-atlas/streaming-models-mindmap.md
Week 3: Flink/02-core/time-semantics-and-watermark.md
        → Knowledge/02-design-patterns/pattern-event-time-processing.md
Week 4: Knowledge/02-design-patterns/ (全模式深入)
        → Knowledge/98-exercises/exercise-02-flink-basics.md
```

#### 进阶工程师路径 (4-6周)

```
Week 1-2: Flink/02-core/checkpoint-mechanism-deep-dive.md
          → Flink/02-core/exactly-once-semantics-deep-dive.md
Week 3-4: Struct/04-proofs/04.01-flink-checkpoint-correctness.md
          → Struct/04-proofs/04.02-flink-exactly-once-correctness.md
Week 5-6: Knowledge/02-design-patterns/ (全模式深入)
          → Knowledge/09-anti-patterns/ (反模式识别)
```

#### 架构师路径 (持续)

```
Struct/01-foundation/ (理论基础)
  → Knowledge/04-technology-selection/ (选型决策)
    → Flink/01-concepts/ (架构实现)
      → Knowledge/03-business-patterns/ (业务场景)
        → Struct/06-frontier/ (前沿探索)
```

### 5.3 快速参考卡片

| 参考卡 | 路径 | 内容概要 |
|--------|------|----------|
| **5分钟快速入门** | [tutorials/00-5-MINUTE-QUICK-START.md](tutorials/00-5-MINUTE-QUICK-START.md) | 最简Flink作业创建与运行 |
| **环境搭建指南** | [tutorials/01-environment-setup.md](tutorials/01-environment-setup.md) | JDK/Maven/Flink安装配置 |
| **第一个Flink作业** | [tutorials/02-first-flink-job.md](tutorials/02-first-flink-job.md) | WordCount完整开发流程 |
| **DataStream API速查** | [Flink/03-api/09-language-foundations/datastream-api-cheatsheet.md](Flink/03-api/09-language-foundations/datastream-api-cheatsheet.md) | Source/Transformation/Sink速查 |
| **SQL函数速查** | [Flink/03-api/03.02-table-sql-api/sql-functions-cheatsheet.md](Flink/03-api/03.02-table-sql-api/sql-functions-cheatsheet.md) | Flink SQL内置函数参考 |
| **Checkpoint调优速查** | [Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md](Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md) | 参数配置、超时处理 |
| **Flink vs RisingWave速查** | [Knowledge/98-exercises/quick-ref-flink-vs-risingwave.md](Knowledge/98-exercises/quick-ref-flink-vs-risingwave.md) | 选型对比 |
| **Temporal+Flink速查** | [Knowledge/98-exercises/quick-ref-temporal-flink.md](Knowledge/98-exercises/quick-ref-temporal-flink.md) | 集成要点 |
| **安全合规速查** | [Knowledge/98-exercises/quick-ref-security-compliance.md](Knowledge/98-exercises/quick-ref-security-compliance.md) | GDPR/CCPA |
| **反模式速查** | [Knowledge/98-exercises/quick-ref-streaming-anti-patterns.md](Knowledge/98-exercises/quick-ref-streaming-anti-patterns.md) | 10大反模式 |
| **A2A协议速查** | [Knowledge/98-exercises/quick-ref-a2a-protocol.md](Knowledge/98-exercises/quick-ref-a2a-protocol.md) | Agent互操作 |

### 5.4 交互式学习资源

| 资源 | 路径 | 类型 |
|------|------|------|
| **编程挑战** | [tutorials/interactive/coding-challenges/](tutorials/interactive/coding-challenges/) | 5个实战挑战 |
| **动手实验室** | [tutorials/interactive/hands-on-labs/](tutorials/interactive/hands-on-labs/) | 6个实验课程 |
| **综合测试** | [tutorials/interactive/quizzes/](tutorials/interactive/quizzes/) | 4套测验 |
| **Flink Playground** | [tutorials/interactive/flink-playground/](tutorials/interactive/flink-playground/) | 在线环境 |

### 5.5 演示文稿大纲

| 主题 | 推荐文档组合 | 时长 |
|------|--------------|------|
| **流计算基础** | USTM + Dataflow模型 + Watermark | 45分钟 |
| **Flink核心机制** | Checkpoint + Exactly-Once + Backpressure | 60分钟 |
| **实时AI架构** | Flink AI Agents + RAG + 向量搜索 | 45分钟 |
| **Streaming Lakehouse** | Iceberg + Paimon + 流批一体 | 45分钟 |
| **形式化验证** | TLA+ + Smart Casual + Iris | 60分钟 |

---

## 6. 维护与贡献导航

### 6.1 维护手册

| 文档 | 路径 | 内容 |
|------|------|------|
| **项目跟踪** | [PROJECT-TRACKING.md](PROJECT-TRACKING.md) | 进度看板、完成状态 |
| **版本跟踪** | [PROJECT-VERSION-TRACKING.md](PROJECT-VERSION-TRACKING.md) | 版本历史、变更记录 |
| **v3.3路线图** | [ROADMAP-v3.3-and-beyond.md](ROADMAP-v3.3-and-beyond.md) | 未来规划、P0-P3任务 |
| **定理注册表** | [THEOREM-REGISTRY.md](THEOREM-REGISTRY.md) | 所有定理/定义索引 |
| **Agent工作规范** | [AGENTS.md](AGENTS.md) | 文档编写规范 |

### 6.2 贡献指南

| 指南 | 路径 | 要点 |
|------|------|------|
| **文档结构规范** | [AGENTS.md](AGENTS.md) | 六段式模板 |
| **编号规范** | [AGENTS.md](AGENTS.md) | Thm/Def/Lemma编号 |
| **引用规范** | [AGENTS.md](AGENTS.md) | [^n]格式 |
| **Mermaid规范** | [AGENTS.md](AGENTS.md) | 图表类型选择 |
| **贡献流程** | [CONTRIBUTING.md](CONTRIBUTING.md) | PR流程、代码审查 |

### 6.3 验证报告

| 报告 | 路径 | 内容 |
|------|------|------|
| **最终验证报告** | [FINAL-VALIDATION-REPORT.md](FINAL-VALIDATION-REPORT.md) | 全面验证结果 |
| **v3.2完成报告** | [FULL-COMPLETION-REPORT-v3.2.md](FULL-COMPLETION-REPORT-v3.2.md) | v3.2全面推进总结 |
| **完成报告v5.0** | [FINAL-COMPLETION-REPORT-v5.0.md](FINAL-COMPLETION-REPORT-v5.0.md) | v5.0交付总结 |
| **E1-E4修复报告** | [E1-E4-ACCURACY-FIX-COMPLETION-REPORT.md](E1-E4-ACCURACY-FIX-COMPLETION-REPORT.md) | 准确性修复 |
| **Flink-Scala-Rust报告** | [FLINK-SCALA-RUST-COMPLETION-REPORT.md](FLINK-SCALA-RUST-COMPLETION-REPORT.md) | 多语言专项 |
| **持续扩展报告** | [CONTINUOUS-EXPANSION-REPORT.md](CONTINUOUS-EXPANSION-REPORT.md) | 扩展记录 |

### 6.4 更新日志

| 版本 | 日期 | 主要更新 |
|------|------|----------|
| **v3.3路线图** | 2026-04-04 | v3.3规划发布，P0-P3优先级任务 |
| **v2.9** | 2026-04-04 | E1-E4错误修复完成、tutorials目录完善、DataStream/SQL速查表新增、A2A协议、Smart Casual Verification |
| **v2.8** | 2026-04-02 | Flink AI Agents、图流处理TGN、多模态流处理、Flink 2.3路线图 |
| **v2.7** | 2026-03-15 | Temporal+Flink分层架构、Serverless成本优化 |
| **v2.6** | 2026-03-01 | 流处理反模式专题(10个)、安全合规指南 |
| **v2.5** | 2026-02-15 | Streaming Lakehouse、GPU TEE、RAG Streaming |

---

## 附录

### A. 项目统计 (v3.3 最新)

```
总文档数: 389篇
├── Struct/: 43篇 (形式化理论)
├── Knowledge/: 134篇 (工程实践)
├── Flink/: 164篇 (Flink专项)
├── tutorials/: 27篇 (实践教程)
└── visuals/: 21篇 (可视化文档)

形式化元素: 9,164+
├── 定理 (Thm): 1,880个
├── 定义 (Def): 4,499个
├── 引理 (Lemma): 1,538个
├── 命题 (Prop): 1,176个
└── 推论 (Cor): 71个

Mermaid图表: 1,600+
代码示例: 4,500+
代码行数: 29,920+
Markdown行数: 338,716+
项目大小: 20+ MB
```

### B. 目录索引快速入口

- [Struct/00-INDEX.md](Struct/00-INDEX.md) — 形式化理论完整索引
- [Knowledge/00-INDEX.md](Knowledge/00-INDEX.md) — 工程实践完整索引
- [Flink/00-INDEX.md](Flink/00-INDEX.md) — Flink专项完整索引
- [tutorials/interactive/README.md](tutorials/interactive/README.md) — 交互式学习资源
- [.scripts/README.md](.scripts/) — 自动化脚本工具

### C. 外部资源链接

| 资源 | 链接 |
|------|------|
| Apache Flink官方文档 | <https://nightlies.apache.org/flink/> |
| Flink FLIP提案 | <https://github.com/apache/flink/tree/master/flink-docs/docs/flips> |
| Dataflow模型论文 | <https://www.vldb.org/pvldb/vol8/p1792-Akidau.pdf> |
| MIT 6.824分布式系统 | <https://pdos.csail.mit.edu/6.824/> |

### D. v3.3路线图关键里程碑

| 版本 | 日期 | 目标 | 关键交付 |
|------|------|------|----------|
| v3.2.1 | 2026-04-11 | 交叉引用修复 | 错误数=0 |
| v3.2.2 | 2026-04-30 | 质量门禁上线 | CI自动化完成 |
| v3.3 | 2026-06-30 | P0/P1内容补齐 | 400+文档 |
| v3.4 | 2026-09-30 | 知识图谱2.0 | 交互式图谱 |
| v4.0 | 2027-Q1 | 国际化发布 | 中英双语 |

---

> **最后更新**: 2026-04-04 | **版本**: v2.9 | **状态**: 生产就绪 ✅ | **v3.3路线图**: 已发布 🗺️
