# Flink 特性成熟度矩阵

> **版本**: v1.0 | **更新日期**: 2026-04-07 | **状态**: Active

本文档汇总了本项目中涉及的所有 Flink 相关特性的成熟度状态，明确标注哪些特性是已发布的、哪些是前瞻性的，帮助读者正确理解文档内容的可靠程度。

---

## 成熟度等级定义

| 等级 | 图标 | 名称 | 说明 | 使用建议 |
|------|------|------|------|----------|
| **L5** | ✅ | **已发布 (Released)** | 官方正式发布，生产可用 | 可放心使用 |
| **L4** | 🟢 | **稳定 (Stable)** | 已发布多个版本，API稳定 | 生产环境推荐使用 |
| **L3** | 🟡 | **预览 (Preview)** | 官方标记为Preview/Experimental | 可试用，不推荐生产 |
| **L2** | 🟠 | **讨论中 (Under Discussion)** | 社区正在讨论，无正式FLIP | 关注进展，勿依赖 |
| **L1** | 🔴 | **概念设计 (Concept)** | 前瞻性分析，技术愿景 | 仅作参考，可能变化 |
| **L0** | ⚪ | **推测性 (Speculative)** | 长期愿景，高度不确定 | 纯技术探索性质 |

---

## Flink 版本特性矩阵

### Flink 2.0 (已发布 ✅)

| 特性 | 官方状态 | 本文档状态 | 成熟度 | 备注 |
|------|----------|-----------|--------|------|
| **DataStream API V2** | Experimental | ✅ 已同步 | 🟡 L3 | Flink 2.0 实验性发布 |
| **ForSt State Backend** | Released | ✅ 已同步 | ✅ L5 | Flink 2.0 正式发布 |
| **Materialized Table** | Released | ✅ 已同步 | ✅ L5 | Flink 2.0 正式发布 |
| **Async Execution Model** | Released | ✅ 已同步 | ✅ L5 | Flink 2.0 正式发布 |
| **Disaggregated State** | Released | ✅ 已同步 | ✅ L5 | Flink 2.0 正式发布 |
| **Java 21 Support** | Released | ✅ 已同步 | ✅ L5 | Flink 2.0 正式发布 |
| **New Config Format (YAML)** | Released | ✅ 已同步 | ✅ L5 | Flink 2.0 正式发布 |
| **Adaptive Batch Execution** | Released | ✅ 已同步 | ✅ L5 | Flink 2.0 正式发布 |

**官方参考**: [Flink 2.0 Release Notes](https://nightlies.apache.org/flink/flink-docs-stable/release-notes/flink-2.0/)

---

### Flink 2.1/2.2 (已发布 ✅)

| 特性 | 官方状态 | 本文档状态 | 成熟度 | 备注 |
|------|----------|-----------|--------|------|
| **Model DDL & ML_PREDICT** | Released (2.2) | ✅ 已同步 | ✅ L5 | Flink 2.2 正式发布 |
| **Vector Search** | Released (2.2) | ✅ 已同步 | ✅ L5 | Flink 2.2 正式发布 |
| **State V2 API GA** | Released (2.2) | ✅ 已同步 | ✅ L5 | Flink 2.2 正式发布 |
| **PyFlink 改进** | Released (2.2) | ✅ 已同步 | ✅ L5 | Flink 2.2 正式发布 |
| **Paimon 集成增强** | Released (2.2) | ✅ 已同步 | ✅ L5 | Flink 2.2 正式发布 |

---

### Flink 2.3 (规划中 🟡)

| 特性 | 官方状态 | 本文档状态 | 成熟度 | 备注 |
|------|----------|-----------|--------|------|
| **Release Plan** | 社区讨论中 | 🟡 前瞻分析 | 🟡 L2 | 无官方时间表 |
| **AI Agent (FLIP-531)** | 早期讨论 | 🔴 概念设计 | 🔴 L1 | 尚未成为正式FLIP |
| **GPU Acceleration** | 提案阶段 | 🟡 前瞻分析 | 🟡 L2 | 社区探索中 |
| **WASM UDF GA** | Preview | 🟡 前瞻分析 | 🟡 L3 | 可能2.3或更晚 |

**说明**: Flink 2.3 尚未有官方发布计划，本文档内容为基于社区讨论的前瞻性分析。

---

### Flink 2.4/2.5 (前瞻内容 🔴)

| 特性 | 官方状态 | 本文档状态 | 成熟度 | 备注 |
|------|----------|-----------|--------|------|
| **Release Plan** | 未讨论 | 🔴 高度推测 | ⚪ L0 | 无官方计划 |
| **FLIP-531 AI Agent GA** | 未接受 | 🔴 概念设计 | 🔴 L1 | 纯技术愿景 |
| **Serverless Flink Architecture** | 未讨论 | 🔴 概念设计 | 🔴 L1 | 趋势分析 |
| **Unified Stream-Batch (FLIP-435)** | 占位符 | 🔴 概念设计 | 🔴 L1 | 无正式FLIP编号 |
| **Next-Gen State Management** | 未讨论 | 🔴 概念设计 | 🔴 L1 | 架构探索 |
| **ANSI SQL 2023 Full Compliance** | 进行中 | 🟡 部分实现 | 🟡 L2 | 持续改进 |

**重要声明**:

- Flink 2.4/2.5 尚未进入官方规划
- 本文档所有描述均为**技术愿景和假设性设计**
- 发布时间、特性和API都可能与实际完全不同

---

### Flink 3.0 (长期愿景 ⚪)

| 特性 | 官方状态 | 本文档状态 | 成熟度 | 备注 |
|------|----------|-----------|--------|------|
| **Release Plan** | 未启动 | ⚪ 纯推测 | ⚪ L0 | 社区尚未讨论 |
| **Unified Execution Layer** | 概念阶段 | ⚪ 纯推测 | ⚪ L0 | 架构探索 |
| **Architecture Redesign** | 概念阶段 | ⚪ 纯推测 | ⚪ L0 | 技术愿景 |
| **Cloud-Native 2.0** | 概念阶段 | ⚪ 纯推测 | ⚪ L0 | 趋势分析 |

**重要声明**:

- Flink 3.0 目前**不存在**于官方路线图中
- Flink 2.x 将长期维护，3.0 并非迫在眉睫
- 本文档内容为**纯粹的技术探索**，与实际发展可能完全不同

---

## AI/ML 相关特性矩阵

| 特性 | 官方状态 | 本文档状态 | 成熟度 | 备注 |
|------|----------|-----------|--------|------|
| **Flink ML (Alink)** | Released | ✅ 已同步 | ✅ L5 | 官方稳定版 |
| **ML_PREDICT SQL函数** | Released (2.2) | ✅ 已同步 | ✅ L5 | Flink 2.2 GA |
| **Vector Search** | Released (2.2) | ✅ 已同步 | ✅ L5 | Flink 2.2 GA |
| **Model DDL** | Released (2.2) | ✅ 已同步 | ✅ L5 | Flink 2.2 GA |
| **FLIP-531 AI Agents** | 未接受 | 🔴 概念设计 | 🔴 L1 | 非官方特性 |
| **MCP Protocol集成** | 未讨论 | 🔴 概念设计 | 🔴 L1 | 前瞻性设计 |
| **A2A Protocol集成** | 未讨论 | 🔴 概念设计 | 🔴 L1 | 前瞻性设计 |
| **GPU Acceleration** | 提案阶段 | 🟡 前瞻分析 | 🟡 L2 | 社区探索 |

---

## 状态后端特性矩阵

| 特性 | 官方状态 | 本文档状态 | 成熟度 | 备注 |
|------|----------|-----------|--------|------|
| **MemoryStateBackend** | Deprecated | ✅ 已同步 | 🟢 L4 | 2.0中已弃用 |
| **HashMapStateBackend** | Released | ✅ 已同步 | ✅ L5 | 稳定可用 |
| **RocksDBStateBackend** | Released | ✅ 已同步 | ✅ L5 | 稳定可用 |
| **ForStStateBackend** | Released (2.0) | ✅ 已同步 | ✅ L5 | Flink 2.0 GA |
| **Changelog State Backend** | Released | ✅ 已同步 | ✅ L5 | 生产可用 |
| **Incremental Checkpoint** | Released | ✅ 已同步 | ✅ L5 | 稳定可用 |
| **Disaggregated State** | Released (2.0) | ✅ 已同步 | ✅ L5 | Flink 2.0 GA |
| **Next-Gen State Management** | 未讨论 | 🔴 概念设计 | 🔴 L1 | 前瞻愿景 |

---

## 部署特性矩阵

| 特性 | 官方状态 | 本文档状态 | 成熟度 | 备注 |
|------|----------|-----------|--------|------|
| **Standalone Mode** | Released | ✅ 已同步 | ✅ L5 | 稳定可用 |
| **YARN Deployment** | Released | ✅ 已同步 | ✅ L5 | 稳定可用 |
| **Kubernetes Deployment** | Released | ✅ 已同步 | ✅ L5 | 稳定可用 |
| **Kubernetes Operator** | Released | ✅ 已同步 | ✅ L5 | 官方支持 |
| **Native K8s Integration** | Released | ✅ 已同步 | ✅ L5 | 稳定可用 |
| **AWS EMR Serverless** | 第三方 | ✅ 已同步 | 🟢 L4 | 云厂商方案 |
| **Azure Stream Analytics** | 第三方 | ✅ 已同步 | 🟢 L4 | 云厂商方案 |
| **GCP Dataflow** | 第三方 | ✅ 已同步 | 🟢 L4 | 云厂商方案 |
| **Serverless Flink (Native)** | 未讨论 | 🔴 概念设计 | 🔴 L1 | 前瞻愿景 |
| **Scale-to-Zero** | 未讨论 | 🔴 概念设计 | 🔴 L1 | 前瞻愿景 |

---

## 连接器特性矩阵

| 特性 | 官方状态 | 本文档状态 | 成熟度 | 备注 |
|------|----------|-----------|--------|------|
| **Kafka Connector** | Released | ✅ 已同步 | ✅ L5 | 稳定可用 |
| **JDBC Connector** | Released | ✅ 已同步 | ✅ L5 | 稳定可用 |
| **Elasticsearch Connector** | Released | ✅ 已同步 | ✅ L5 | 稳定可用 |
| **Filesystem Connector** | Released | ✅ 已同步 | ✅ L5 | 稳定可用 |
| **CDC Connectors (Debezium)** | Released | ✅ 已同步 | ✅ L5 | 稳定可用 |
| **Paimon Integration** | Released | ✅ 已同步 | ✅ L5 | 稳定可用 |
| **Iceberg Integration** | Released | ✅ 已同步 | ✅ L5 | 稳定可用 |
| **Pulsar Connector** | Released | ✅ 已同步 | ✅ L5 | 稳定可用 |

---

## 如何使用本文档

### 对于生产环境用户

- **仅使用 L4-L5 (🟢-✅) 特性**: 这些是官方发布的稳定特性
- **谨慎使用 L3 (🟡) 特性**: Preview 特性可能变更，需评估风险
- **避免使用 L0-L2 (⚪-🔴) 特性**: 这些是前瞻性内容，不适合生产

### 对于架构师和研究者

- **L5-L4**: 可靠的当前能力基线
- **L3**: 即将可用的技术方向
- **L2-L1**: 值得关注的社区动态
- **L0**: 长期技术趋势参考

### 对于贡献者

本文档需要定期更新以反映：

1. Flink 官方新版本发布
2. FLIP 提案状态变化
3. 社区路线图更新

---

## 相关文档

- [Flink 2.4 跟踪文档](Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md)
- [Flink 2.5 预览文档](Flink/08-roadmap/08.01-flink-24/flink-2.5-preview.md)
- [Flink 3.0 架构愿景](Flink/08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md)
- [FLIP-531 概念设计](Flink/06-ai-ml/flink-ai-agents-flip-531.md)
- [Flink 官方路线图](https://nightlies.apache.org/flink/flink-docs-stable/roadmap/)

---

*本文档最后更新于 2026-04-07*
*如发现内容过期或不准确，请提交 Issue 或 PR 更新*
