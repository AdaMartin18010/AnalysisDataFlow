# v4.3 新文档交叉引用推荐映射表

> **生成日期**: 2026-04-18
> **版本**: v4.3
> **新文档数**: 10
> **推荐引用总数**: 42
> **生成方法**: 基于文档内容语义分析 + 现有文档关键词匹配

---

## 1. DBSP (Database Stream Processor) 理论框架

**目标文档**: `Struct/06-frontier/dbsp-theory-framework.md`

| 源文档 (Source) | 目标文档 (Target) | 推荐位置 | 推荐锚文本 |
|---|---|---|---|
| `Knowledge/01-concept-atlas/streaming-models-mindmap.md` | `Struct/06-frontier/dbsp-theory-framework.md` | §3 关系建立 → "关系 1: Dataflow ≈ Actor" 之后新增小节 | [DBSP理论框架：增量视图维护的代数基础](../../Struct/06-frontier/dbsp-theory-framework.md) |
| `Knowledge/01-concept-atlas/streaming-models-mindmap.md` | `Struct/06-frontier/dbsp-theory-framework.md` | §3 关系建立 → 新增 "关系 5: Dataflow ↦ DBSP（增量计算的代数编码）" | [DBSP将数据库查询与流处理统一到Z-set代数结构](../../Struct/06-frontier/dbsp-theory-framework.md) |
| `Flink/05-ecosystem/05.02-lakehouse/flink-paimon-integration.md` | `Struct/06-frontier/dbsp-theory-framework.md` | §1 Def-F-14-03 LSM-Tree增量日志模型之后 | [DBSP理论框架为增量视图维护提供严格数学基础](../../Struct/06-frontier/dbsp-theory-framework.md) |
| `Flink/05-ecosystem/05.02-lakehouse/flink-paimon-integration.md` | `Struct/06-frontier/dbsp-theory-framework.md` | §3.4 流数据库与Lakehouse的集成关系 | [DBSP的差分算子∇与积分算子∇⁻¹建立了完整的增量计算理论](../../Struct/06-frontier/dbsp-theory-framework.md) |
| `Knowledge/04-technology-selection/streaming-database-guide.md` | `Struct/06-frontier/dbsp-theory-framework.md` | §1.1 Def-K-04-10 Streaming Database定义之后 | [DBSP框架为流数据库的增量维护机制提供形式化基础](../../Struct/06-frontier/dbsp-theory-framework.md) |
| `Knowledge/04-technology-selection/streaming-database-guide.md` | `Struct/06-frontier/dbsp-theory-framework.md` | §2 Lemma-K-04-03 物化视图一致性维护开销下界之后 | [DBSP增量视图维护正确性定理严格证明了增量更新的数学正确性](../../Struct/06-frontier/dbsp-theory-framework.md) |
| `Struct/01-foundation/streaming-database-formal-definition.md` | `Struct/06-frontier/dbsp-theory-framework.md` | §3 关系建立 → "关系 3: SDB增量机制 ≈ DBSP ∇算子" 深化 | [DBSP理论框架的完整形式化定义与证明](../../Struct/06-frontier/dbsp-theory-framework.md) |

---

## 2. Calvin 确定性执行模型与流处理状态管理

**目标文档**: `Struct/06-frontier/calvin-deterministic-streaming.md`

| 源文档 (Source) | 目标文档 (Target) | 推荐位置 | 推荐锚文本 |
|---|---|---|---|
| `Flink/02-core/exactly-once-semantics-deep-dive.md` | `Struct/06-frontier/calvin-deterministic-streaming.md` | §1.2 两阶段提交协议形式化之后 | [Calvin确定性协议彻底消除2PC开销，实现跨分区事务线性扩展](../../Struct/06-frontier/calvin-deterministic-streaming.md) |
| `Flink/02-core/exactly-once-semantics-deep-dive.md` | `Struct/06-frontier/calvin-deterministic-streaming.md` | §3 关系建立 → 新增 "Calvin与Flink Exactly-Once语义对比" | [Calvin确定性重放与Flink Checkpoint的深层形式化映射](../../Struct/06-frontier/calvin-deterministic-streaming.md) |
| `Flink/02-core/flink-2.0-async-execution-model.md` | `Struct/06-frontier/calvin-deterministic-streaming.md` | §4 论证过程 → 异步执行与确定性边界讨论 | [Calvin通过前置排序+无副作用重放消除运行时不确定性](../../Struct/06-frontier/calvin-deterministic-streaming.md) |
| `Knowledge/exactly-once-comparison.md` | `Struct/06-frontier/calvin-deterministic-streaming.md` | §2 属性推导 → 一致性语义分类对比之后 | [Calvin确定性执行定理：全局排序一致下所有副本无需协调即可达相同终态](../../Struct/06-frontier/calvin-deterministic-streaming.md) |
| `Knowledge/acid-in-stream-processing.md` | `Struct/06-frontier/calvin-deterministic-streaming.md` | §1 概念定义 → 事务隔离级别定义之后 | [Calvin将事务处理拆分为预处理、全局排序、确定性执行三阶段](../../Struct/06-frontier/calvin-deterministic-streaming.md) |
| `Struct/transactional-stream-semantics.md` | `Struct/06-frontier/calvin-deterministic-streaming.md` | §3 关系建立 → 事务协议对比 | [Calvin与2PC、Raft、Paxos的严格形式化对比分析](../../Struct/06-frontier/calvin-deterministic-streaming.md) |
| `Flink/04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md` | `Struct/06-frontier/calvin-deterministic-streaming.md` | §1 Def-F-10-44 JobManager高可用性模式之后 | [Calvin对Flink JobManager高可用机制的启示：确定性预排序替代运行时协调](../../Struct/06-frontier/calvin-deterministic-streaming.md) |
| `Flink/04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md` | `Struct/06-frontier/calvin-deterministic-streaming.md` | §6.9 高可用配置完整示例之后 | [Calvin式确定性执行可能突破Checkpoint机制在超低延迟场景的根本局限](../../Struct/06-frontier/calvin-deterministic-streaming.md) |

---

## 3. AI Agent 行为契约验证方法

**目标文档**: `formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md`

| 源文档 (Source) | 目标文档 (Target) | 推荐位置 | 推荐锚文本 |
|---|---|---|---|
| `Flink/06-ai-ml/flink-agents-architecture-deep-dive.md` | `formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md` | §1 Def-P2-02 Agent生命周期状态机之后 | [Agent行为契约验证为Flink Agent生命周期状态转换提供形式化安全保证](../../formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md) |
| `Flink/06-ai-ml/flink-agents-architecture-deep-dive.md` | `formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md` | §3 关系建立 → Agent安全架构小节 | [AgentAssert与AgentAssay框架的完整形式化语义与工程实践](../../formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md) |
| `Flink/06-ai-ml/flink-mcp-protocol-integration.md` | `formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md` | §1 Def-F-12-48 MCP工具定义之后 | [MCP工具调用的安全验证：行为契约与前置/后置条件形式化检查](../../formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md) |
| `Flink/06-ai-ml/flink-mcp-protocol-integration.md` | `formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md` | §4 论证过程 → MCP安全风险分析 | [44%的MCP服务器缺乏认证——Agent行为契约验证的核心技术框架](../../formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md) |
| `Knowledge/06-frontier/mcp-security-governance-2026.md` | `formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md` | §1 Def-K-06-300 MCP安全态势之后 | [Agent行为契约验证：从安全态势评估到运行时监控的完整方法论](../../formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md) |
| `Knowledge/06-frontier/mcp-security-governance-2026.md` | `formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md` | §3 企业部署指南 → 技术控制措施 | [基于TLA+与Session Types的Agent工具调用安全验证实例](../../formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md) |
| `Flink/06-ai-ml/ai-agent-flink-deep-integration.md` | `formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md` | §2 属性推导 → 集成安全性分析 | [多Agent协作中的死锁、竞态条件和工具冲突形式化检测](../../formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md) |
| `Flink/06-ai-ml/flip-531-ai-agents-ga-guide.md` | `formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md` | §5 生产部署检查清单 → 安全验证项 | [A2A Agent Cards契约检查的完整形式化流程与TLA+规约](../../formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md) |

---

## 4. Streaming Database 形式化定义与理论体系

**目标文档**: `Struct/01-foundation/streaming-database-formal-definition.md`

| 源文档 (Source) | 目标文档 (Target) | 推荐位置 | 推荐锚文本 |
|---|---|---|---|
| `Flink/03-api/09-language-foundations/06-risingwave-deep-dive.md` | `Struct/01-foundation/streaming-database-formal-definition.md` | §1 RisingWave架构概述之后 | [Streaming Database严格八元组形式化模型与RisingWave架构的精确映射](../../Struct/01-foundation/streaming-database-formal-definition.md) |
| `Flink/07-rust-native/risingwave-comparison/01-risingwave-architecture.md` | `Struct/01-foundation/streaming-database-formal-definition.md` | §2 RisingWave存储-计算分离架构分析之后 | [流数据库与流处理引擎的严格七元组/八元组模型对比](../../Struct/01-foundation/streaming-database-formal-definition.md) |
| `Flink/07-rust-native/risingwave-comparison/01-risingwave-architecture.md` | `Struct/01-foundation/streaming-database-formal-definition.md` | §3 与Flink的对比矩阵之后 | [快照语义与流语义的查询理论严格定义](../../Struct/01-foundation/streaming-database-formal-definition.md) |
| `Knowledge/04-technology-selection/streaming-database-guide.md` | `Struct/01-foundation/streaming-database-formal-definition.md` | §1.1 Def-K-04-10 Streaming Database定义段落 | [更严格的流数据库八元组形式化定义：物化视图、增量更新、SQL兼容性与持久化存储](../../Struct/01-foundation/streaming-database-formal-definition.md) |
| `Knowledge/04-technology-selection/streaming-databases-2026-comparison.md` | `Struct/01-foundation/streaming-database-formal-definition.md` | §4 六类流数据库详细对比矩阵 → 理论根基列 | [SDB vs SPE形式化区分：物化视图为第一公民的架构本质](../../Struct/01-foundation/streaming-database-formal-definition.md) |
| `Knowledge/04-technology-selection/streaming-databases-2026-comparison.md` | `Struct/01-foundation/streaming-database-formal-definition.md` | §5 场景驱动选型论证之后 | [查询可增量性的形式化定义与不可增量化查询类的边界分析](../../Struct/01-foundation/streaming-database-formal-definition.md) |
| `Flink/05-ecosystem/05.01-connectors/fluss-integration.md` | `Struct/01-foundation/streaming-database-formal-definition.md` | §3 与Flink生态关系 → 存储语义讨论 | [Fluss作为流存储层与Streaming Database持久化存储模型的形式化关系](../../Struct/01-foundation/streaming-database-formal-definition.md) |
| `Struct/06-frontier/dbsp-theory-framework.md` | `Struct/01-foundation/streaming-database-formal-definition.md` | §3.4 DBSP与Dataflow Model语义映射之后 | [Streaming Database作为独立计算范式的统一数学模型](../../Struct/01-foundation/streaming-database-formal-definition.md) |

---

## 5. 最小会话类型理论 (Minimal Session Types Theory)

**目标文档**: `Struct/01-foundation/minimal-session-types-theory.md`

| 源文档 (Source) | 目标文档 (Target) | 推荐位置 | 推荐锚文本 |
|---|---|---|---|
| `Struct/03-relationships/03.01-actor-to-csp-encoding.md` | `Struct/01-foundation/minimal-session-types-theory.md` | §3 关系建立 → Actor-CSP编码之后新增小节 | [最小会话类型：仅含输出、输入、终止三构造子即可表达所有标准会话协议](../../Struct/01-foundation/minimal-session-types-theory.md) |
| `Struct/03-relationships/03.01-actor-to-csp-encoding.md` | `Struct/01-foundation/minimal-session-types-theory.md` | §5 形式证明 → 编码完备性证明之后 | [MST与标准会话类型的表达能力等价性定理及其对编译器设计的影响](../../Struct/01-foundation/minimal-session-types-theory.md) |
| `Struct/06-frontier/06.03-ai-agent-session-types.md` | `Struct/01-foundation/minimal-session-types-theory.md` | §1 概念定义 → AI Agent会话类型定义之后 | [最小会话类型理论为Agent间通信协议的类型安全检查提供最小化基础](../../Struct/01-foundation/minimal-session-types-theory.md) |
| `Struct/06-frontier/first-person-choreographies.md` | `Struct/01-foundation/minimal-session-types-theory.md` | §3 关系建立 → Choreographic Programming关联 | [MST与Choreographic Programming的理论关联：顺序性可通过进程同步精确模拟](../../Struct/01-foundation/minimal-session-types-theory.md) |
| `Struct/06-frontier/ai-agent-streaming-formal-theory.md` | `Struct/01-foundation/minimal-session-types-theory.md` | §3 关系建立 → 流计算系统理论映射 | [流处理算子链的最小会话类型建模与类型检查算法](../../Struct/01-foundation/minimal-session-types-theory.md) |
| `Knowledge/05-mapping-guides/struct-to-flink-mapping.md` | `Struct/01-foundation/minimal-session-types-theory.md` | §3 关系建立 → 类型系统映射小节 | [从标准会话类型到MST的编译算法及其在流处理类型检查中的应用](../../Struct/01-foundation/minimal-session-types-theory.md) |

---

## 6. Veil Framework — 基于 Lean 4 的迁移系统验证框架

**目标文档**: `formal-methods/06-tools/veil-framework-lean4.md`

| 源文档 (Source) | 目标文档 (Target) | 推荐位置 | 推荐锚文本 |
|---|---|---|---|
| `docs/formal-verification-toolchain-guide.md` | `formal-methods/06-tools/veil-framework-lean4.md` | §2 工具链概览 → 新增Veil条目 | [Veil Framework：嵌入Lean 4的迁移系统验证框架，具备机器检验的VC生成器可靠性证明](../../formal-methods/06-tools/veil-framework-lean4.md) |
| `Struct/07-tools/coq-mechanization.md` | `formal-methods/06-tools/veil-framework-lean4.md` | §3 关系建立 → Coq生态工具对比 | [Veil与Coq的对比：SMT自动化求解与交互式证明的融合路径](../../formal-methods/06-tools/veil-framework-lean4.md) |
| `Struct/07-tools/tla-for-flink.md` | `formal-methods/06-tools/veil-framework-lean4.md` | §3 关系建立 → TLA+工具生态 | [Veil与TLA+的对比：关系建模语言与状态机规约的不同抽象层级](../../formal-methods/06-tools/veil-framework-lean4.md) |
| `Struct/07-tools/smart-casual-verification.md` | `formal-methods/06-tools/veil-framework-lean4.md` | §3 关系建立 → 验证方法谱系定位 | [Veil在形式化验证工具谱系中的定位：自动化与交互式的双重能力融合](../../formal-methods/06-tools/veil-framework-lean4.md) |
| `Struct/06-frontier/llm-guided-formal-proof-automation.md` | `formal-methods/06-tools/veil-framework-lean4.md` | §6 实例验证 → Lean 4策略推荐实例之后 | [Veil 2.0与Loom的多模态语义基础：形式化验证工具的工程实践参考](../../formal-methods/06-tools/veil-framework-lean4.md) |
| `Struct/04-proofs/04.01-flink-checkpoint-correctness.md` | `formal-methods/06-tools/veil-framework-lean4.md` | §3 关系建立 → 验证工具选型 | [使用Veil对分布式协议进行自动化安全性验证的工程路径](../../formal-methods/06-tools/veil-framework-lean4.md) |

---

## 7. CD-Raft: 跨域场景下的 Raft 共识优化

**目标文档**: `Knowledge/06-frontier/cd-raft-cross-domain-consensus.md`

| 源文档 (Source) | 目标文档 (Target) | 推荐位置 | 推荐锚文本 |
|---|---|---|---|
| `Flink/02-core/checkpoint-mechanism-deep-dive.md` | `Knowledge/06-frontier/cd-raft-cross-domain-consensus.md` | §1.1 一致性语义形式化 → Checkpoint协调器之后 | [CD-Raft跨域共识优化对Flink Checkpoint JobManager高可用的启示：Fast Return策略](../../Knowledge/06-frontier/cd-raft-cross-domain-consensus.md) |
| `Flink/04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md` | `Knowledge/06-frontier/cd-raft-cross-domain-consensus.md` | §1 Def-F-10-44 JobManager高可用性模式 | [CD-Raft：跨域Raft部署的平均延迟降低34-41%、P99降低42-53%](../../Knowledge/06-frontier/cd-raft-cross-domain-consensus.md) |
| `Flink/04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md` | `Knowledge/06-frontier/cd-raft-cross-domain-consensus.md` | §6.9 高可用配置完整示例 → 多地域部署场景 | [Optimal Global Leader Position策略动态计算全局最优Leader部署位置](../../Knowledge/06-frontier/cd-raft-cross-domain-consensus.md) |
| `Struct/04-proofs/distributed-consensus-formal-proof.md` | `Knowledge/06-frontier/cd-raft-cross-domain-consensus.md` | §3 关系建立 → Raft变体对比 | [CD-Raft Fast Return与Optimal Leader的形式化安全性分析](../../Knowledge/06-frontier/cd-raft-cross-domain-consensus.md) |
| `Knowledge/07-best-practices/07.06-high-availability-patterns.md` | `Knowledge/06-frontier/cd-raft-cross-domain-consensus.md` | §1 概念定义 → 跨地域HA模式 | [跨域共识的延迟不对称性建模与CD-Raft优化策略的形式化描述](../../Knowledge/06-frontier/cd-raft-cross-domain-consensus.md) |
| `Flink/09-practices/09.04-deployment/flink-k8s-operator-migration-1.13-to-1.14.md` | `Knowledge/06-frontier/cd-raft-cross-domain-consensus.md` | §3 关系建立 → HA后端演进 | [JobManager HA后端从ZooKeeper到Kubernetes-native的演进中，跨域共识优化的适用性分析](../../Knowledge/06-frontier/cd-raft-cross-domain-consensus.md) |

---

## 8. Flink Dynamic Iceberg Sink 完整指南

**目标文档**: `Flink/05-ecosystem/flink-dynamic-iceberg-sink-guide.md`

| 源文档 (Source) | 目标文档 (Target) | 推荐位置 | 推荐锚文本 |
|---|---|---|---|
| `Flink/05-ecosystem/05.02-lakehouse/flink-paimon-integration.md` | `Flink/05-ecosystem/flink-dynamic-iceberg-sink-guide.md` | §1 Def-F-14-01 Paimon形式化定义之后 | [Flink Dynamic Iceberg Sink：无感自动化的Topic-to-Table路由与Schema Evolution](../../Flink/05-ecosystem/flink-dynamic-iceberg-sink-guide.md) |
| `Flink/05-ecosystem/05.02-lakehouse/flink-paimon-integration.md` | `Flink/05-ecosystem/flink-dynamic-iceberg-sink-guide.md` | §3.4 流数据库与Lakehouse集成关系 | [Dynamic Iceberg Sink与Paimon在流批统一存储场景下的对比矩阵](../../Flink/05-ecosystem/flink-dynamic-iceberg-sink-guide.md) |
| `Flink/05-ecosystem/05.01-connectors/flink-24-connectors-guide.md` | `Flink/05-ecosystem/flink-dynamic-iceberg-sink-guide.md` | §2 连接器生态概览 → Sink连接器分类 | [2025年11月发布的Dynamic Iceberg Sink：支持数千Topic动态路由的数据湖集成新模式](../../Flink/05-ecosystem/flink-dynamic-iceberg-sink-guide.md) |
| `Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md` | `Flink/05-ecosystem/flink-dynamic-iceberg-sink-guide.md` | §3 功能跟踪 → 生态系统特性 | [Dynamic Iceberg Sink作为Flink 2.4+数据湖集成的核心能力演进](../../Flink/05-ecosystem/flink-dynamic-iceberg-sink-guide.md) |
| `Knowledge/feature-store-architecture.md` | `Flink/05-ecosystem/flink-dynamic-iceberg-sink-guide.md` | §3 关系建立 → 数据湖集成小节 | [Dynamic Iceberg Sink在特征存储数据湖沉淀场景中的Schema Evolution实践](../../Flink/05-ecosystem/flink-dynamic-iceberg-sink-guide.md) |
| `Flink/02-core/streaming-etl-best-practices.md` | `Flink/05-ecosystem/flink-dynamic-iceberg-sink-guide.md` | §6 实例验证 → 数据入湖最佳实践 | [大规模实时数据入湖的Dynamic Sink配置：Flink SQL/Table API/DataStream API完整示例](../../Flink/05-ecosystem/flink-dynamic-iceberg-sink-guide.md) |

---

## 9. 流处理 Data Mesh 架构与实时数据产品

**目标文档**: `Knowledge/06-frontier/streaming-data-mesh-architecture.md`

| 源文档 (Source) | 目标文档 (Target) | 推荐位置 | 推荐锚文本 |
|---|---|---|---|
| `Knowledge/06-frontier/realtime-data-product-architecture.md` | `Knowledge/06-frontier/streaming-data-mesh-architecture.md` | §1 Def-K-06-101 实时数据产品定义之后 | [流处理Data Mesh架构：域所有权、数据即产品、自服务平台、联邦治理四原则形式化](../../Knowledge/06-frontier/streaming-data-mesh-architecture.md) |
| `Knowledge/06-frontier/realtime-data-mesh-practice.md` | `Knowledge/06-frontier/streaming-data-mesh-architecture.md` | §1 概念定义 → Data Mesh基础定义 | [流处理Data Mesh的形式化定义与实时数据产品的严格模型](../../Knowledge/06-frontier/streaming-data-mesh-architecture.md) |
| `Knowledge/03-business-patterns/streaming-data-product-economics.md` | `Knowledge/06-frontier/streaming-data-mesh-architecture.md` | §3 关系建立 → 数据产品经济模型 | [实时数据产品的网络效应：域数量、产品数量与延迟的量化关系](../../Knowledge/06-frontier/streaming-data-mesh-architecture.md) |
| `Flink/06-ai-ml/flink-22-data-ai-platform.md` | `Knowledge/06-frontier/streaming-data-mesh-architecture.md` | §3 关系建立 → 数据平台架构 | [Data Mesh范式下Flink实时数据平台的域自治与联邦治理架构设计](../../Knowledge/06-frontier/streaming-data-mesh-architecture.md) |
| `Knowledge/08-standards/streaming-data-governance.md` | `Knowledge/06-frontier/streaming-data-mesh-architecture.md` | §2 属性推导 → 治理策略 | [数据契约的形式化定义：Schema版本控制、兼容性规则与SLA承诺的工程实践](../../Knowledge/06-frontier/streaming-data-mesh-architecture.md) |
| `Flink/05-ecosystem/05.01-connectors/flink-cdc-3.0-data-integration.md` | `Knowledge/06-frontier/streaming-data-mesh-architecture.md` | §3 关系建立 → CDC作为域间数据流 | [CDC数据流在Data Mesh域边界间的数据契约与Schema演化治理](../../Knowledge/06-frontier/streaming-data-mesh-architecture.md) |

---

## 10. LLM 辅助形式化证明自动化

**目标文档**: `Struct/06-frontier/llm-guided-formal-proof-automation.md`

| 源文档 (Source) | 目标文档 (Target) | 推荐位置 | 推荐锚文本 |
|---|---|---|---|
| `Struct/07-tools/ai-formal-verification/ai-formal-verification-integration.md` | `Struct/06-frontier/llm-guided-formal-proof-automation.md` | §1 概念定义 → AI形式化验证定义之后 | [LLM辅助形式化证明自动化的七元组工作流模型与PGSR度量体系](../../Struct/06-frontier/llm-guided-formal-proof-automation.md) |
| `Knowledge/06-frontier/ai-agent-formal-methods.md` | `Struct/06-frontier/llm-guided-formal-proof-automation.md` | §3 关系建立 → Agent验证工具链 | [Claude-3.7-Sonnet在分布式协议基准上证明率42.3%，DeepSeek-V3.2-Exp达50.0%](../../Struct/06-frontier/llm-guided-formal-proof-automation.md) |
| `docs/formal-verification-toolchain-guide.md` | `Struct/06-frontier/llm-guided-formal-proof-automation.md` | §2 工具链概览 → 新增LLM辅助验证条目 | [LLM与TLA+/Coq/Lean 4三大主流工具的集成现状与可验证性安全框架](../../Struct/06-frontier/llm-guided-formal-proof-automation.md) |
| `Struct/07-tools/proof-automation-guide.md` | `Struct/06-frontier/llm-guided-formal-proof-automation.md` | §3 关系建立 → 自动定理证明演进 | [LFPA与传统ATP的精确关系映射：生成角色与裁判角色的分离](../../Struct/06-frontier/llm-guided-formal-proof-automation.md) |
| `formal-methods/06-tools/veil-framework-lean4.md` | `Struct/06-frontier/llm-guided-formal-proof-automation.md` | §3 关系建立 → 与自动化工具的互补 | [Veil的SMT自动化与LLM策略推荐的协同：从Ivy规约到Lean证明的LLM辅助路径](../../Struct/06-frontier/llm-guided-formal-proof-automation.md) |
| `Flink/02-core/checkpoint-mechanism-deep-dive.md` | `Struct/06-frontier/llm-guided-formal-proof-automation.md` | §3 关系建立 → 形式化验证应用 | [LLM辅助生成Flink Checkpoint正确性证明草图的工程可行性分析](../../Struct/06-frontier/llm-guided-formal-proof-automation.md) |

---

## 附录：按源文档聚合的引用推荐

以下视图便于批量编辑现有文档时参考：

### `Knowledge/01-concept-atlas/streaming-models-mindmap.md`

- → `Struct/06-frontier/dbsp-theory-framework.md` (2处)

### `Flink/02-core/exactly-once-semantics-deep-dive.md`

- → `Struct/06-frontier/calvin-deterministic-streaming.md` (2处)

### `Flink/02-core/flink-2.0-async-execution-model.md`

- → `Struct/06-frontier/calvin-deterministic-streaming.md` (1处)

### `Flink/02-core/checkpoint-mechanism-deep-dive.md`

- → `Knowledge/06-frontier/cd-raft-cross-domain-consensus.md` (1处)
- → `Struct/06-frontier/llm-guided-formal-proof-automation.md` (1处)

### `Flink/03-api/09-language-foundations/06-risingwave-deep-dive.md`

- → `Struct/01-foundation/streaming-database-formal-definition.md` (1处)

### `Flink/04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md`

- → `Struct/06-frontier/calvin-deterministic-streaming.md` (2处)
- → `Knowledge/06-frontier/cd-raft-cross-domain-consensus.md` (2处)

### `Flink/05-ecosystem/05.01-connectors/flink-24-connectors-guide.md`

- → `Flink/05-ecosystem/flink-dynamic-iceberg-sink-guide.md` (1处)

### `Flink/05-ecosystem/05.01-connectors/fluss-integration.md`

- → `Struct/01-foundation/streaming-database-formal-definition.md` (1处)

### `Flink/05-ecosystem/05.02-lakehouse/flink-paimon-integration.md`

- → `Struct/06-frontier/dbsp-theory-framework.md` (2处)
- → `Flink/05-ecosystem/flink-dynamic-iceberg-sink-guide.md` (2处)

### `Flink/06-ai-ml/ai-agent-flink-deep-integration.md`

- → `formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md` (1处)

### `Flink/06-ai-ml/flink-agents-architecture-deep-dive.md`

- → `formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md` (2处)

### `Flink/06-ai-ml/flink-mcp-protocol-integration.md`

- → `formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md` (2处)

### `Flink/06-ai-ml/flink-22-data-ai-platform.md`

- → `Knowledge/06-frontier/streaming-data-mesh-architecture.md` (1处)

### `Flink/06-ai-ml/flip-531-ai-agents-ga-guide.md`

- → `formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md` (1处)

### `Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md`

- → `Flink/05-ecosystem/flink-dynamic-iceberg-sink-guide.md` (1处)

### `Flink/09-practices/09.04-deployment/flink-k8s-operator-migration-1.13-to-1.14.md`

- → `Knowledge/06-frontier/cd-raft-cross-domain-consensus.md` (1处)

### `Knowledge/03-business-patterns/streaming-data-product-economics.md`

- → `Knowledge/06-frontier/streaming-data-mesh-architecture.md` (1处)

### `Knowledge/04-technology-selection/streaming-database-guide.md`

- → `Struct/06-frontier/dbsp-theory-framework.md` (2处)
- → `Struct/01-foundation/streaming-database-formal-definition.md` (1处)

### `Knowledge/04-technology-selection/streaming-databases-2026-comparison.md`

- → `Struct/01-foundation/streaming-database-formal-definition.md` (2处)

### `Knowledge/05-mapping-guides/struct-to-flink-mapping.md`

- → `Struct/01-foundation/minimal-session-types-theory.md` (1处)

### `Knowledge/06-frontier/ai-agent-formal-methods.md`

- → `Struct/06-frontier/llm-guided-formal-proof-automation.md` (1处)

### `Knowledge/06-frontier/mcp-security-governance-2026.md`

- → `formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md` (2处)

### `Knowledge/06-frontier/realtime-data-mesh-practice.md`

- → `Knowledge/06-frontier/streaming-data-mesh-architecture.md` (1处)

### `Knowledge/06-frontier/realtime-data-product-architecture.md`

- → `Knowledge/06-frontier/streaming-data-mesh-architecture.md` (1处)

### `Knowledge/07-best-practices/07.06-high-availability-patterns.md`

- → `Knowledge/06-frontier/cd-raft-cross-domain-consensus.md` (1处)

### `Knowledge/08-standards/streaming-data-governance.md`

- → `Knowledge/06-frontier/streaming-data-mesh-architecture.md` (1处)

### `Knowledge/exactly-once-comparison.md`

- → `Struct/06-frontier/calvin-deterministic-streaming.md` (1处)

### `Knowledge/acid-in-stream-processing.md`

- → `Struct/06-frontier/calvin-deterministic-streaming.md` (1处)

### `Knowledge/feature-store-architecture.md`

- → `Flink/05-ecosystem/flink-dynamic-iceberg-sink-guide.md` (1处)

### `Struct/03-relationships/03.01-actor-to-csp-encoding.md`

- → `Struct/01-foundation/minimal-session-types-theory.md` (2处)

### `Struct/04-proofs/04.01-flink-checkpoint-correctness.md`

- → `formal-methods/06-tools/veil-framework-lean4.md` (1处)

### `Struct/04-proofs/distributed-consensus-formal-proof.md`

- → `Knowledge/06-frontier/cd-raft-cross-domain-consensus.md` (1处)

### `Struct/06-frontier/06.03-ai-agent-session-types.md`

- → `Struct/01-foundation/minimal-session-types-theory.md` (1处)

### `Struct/06-frontier/ai-agent-streaming-formal-theory.md`

- → `Struct/01-foundation/minimal-session-types-theory.md` (1处)

### `Struct/06-frontier/dbsp-theory-framework.md`

- → `Struct/01-foundation/streaming-database-formal-definition.md` (1处)

### `Struct/06-frontier/first-person-choreographies.md`

- → `Struct/01-foundation/minimal-session-types-theory.md` (1处)

### `Struct/06-frontier/llm-guided-formal-proof-automation.md`

- → `formal-methods/06-tools/veil-framework-lean4.md` (1处)

### `Struct/07-tools/coq-mechanization.md`

- → `formal-methods/06-tools/veil-framework-lean4.md` (1处)

### `Struct/07-tools/proof-automation-guide.md`

- → `Struct/06-frontier/llm-guided-formal-proof-automation.md` (1处)

### `Struct/07-tools/smart-casual-verification.md`

- → `formal-methods/06-tools/veil-framework-lean4.md` (1处)

### `Struct/07-tools/tla-for-flink.md`

- → `formal-methods/06-tools/veil-framework-lean4.md` (1处)

### `Struct/transactional-stream-semantics.md`

- → `Struct/06-frontier/calvin-deterministic-streaming.md` (1处)

### `docs/formal-verification-toolchain-guide.md`

- → `formal-methods/06-tools/veil-framework-lean4.md` (1处)
- → `Struct/06-frontier/llm-guided-formal-proof-automation.md` (1处)

### `Flink/02-core/streaming-etl-best-practices.md`

- → `Flink/05-ecosystem/flink-dynamic-iceberg-sink-guide.md` (1处)

### `Flink/05-ecosystem/05.01-connectors/flink-cdc-3.0-data-integration.md`

- → `Knowledge/06-frontier/streaming-data-mesh-architecture.md` (1处)
