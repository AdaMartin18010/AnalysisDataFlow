# Struct/ 形式理论文档索引

> **文档定位**: Struct 目录导航索引 | **形式化等级**: L1-L6 全覆盖 | **版本**: 2026.04-v2.0

---

## 📊 统计概览

| 指标 | 数量 | 更新 |
|------|------|------|
| **总文档数** | 50+ 篇 | +7新文档 |
| **定理 (Thm)** | 380+ | +15新定理 |
| **定义 (Def)** | 850+ | +25新定义 |
| **引理/命题** | 1700+ | +30新引理 |
| **形式化等级覆盖** | L1-L6 | 完整 |

---

## 目录结构

### 01-foundation/ 基础理论 (10篇) [100%]

| 文档 | 描述 | 等级 |
|------|------|------|
| [01.01-unified-streaming-theory.md](./01-foundation/01.01-unified-streaming-theory.md) | USTM统一元模型 | L6 |
| [01.02-process-calculus-primer.md](./01-foundation/01.02-process-calculus-primer.md) | 进程演算基础 | L3-L4 |
| [01.03-actor-model-formalization.md](./01-foundation/01.03-actor-model-formalization.md) | Actor模型形式化 | L4-L5 |
| [01.04-dataflow-model-formalization.md](./01-foundation/01.04-dataflow-model-formalization.md) | Dataflow模型形式化 | L5 |
| [01.05-csp-formalization.md](./01-foundation/01.05-csp-formalization.md) | CSP形式化 | L3 |
| [01.06-petri-net-formalization.md](./01-foundation/01.06-petri-net-formalization.md) | Petri网形式化 | L2-L4 |
| [01.07-session-types.md](./01-foundation/01.07-session-types.md) | 会话类型 | L4-L5 |
| [01.08-streaming-database-formalization.md](./01-foundation/01.08-streaming-database-formalization.md) | 流数据库形式化 | L4 |
| [01.09-edge-streaming-semantics.md](./01-foundation/01.09-edge-streaming-semantics.md) | 边缘流语义 | L4 |
| **[01.10-network-calculus](./01-foundation/network-calculus/network-calculus-streaming.md)** | Network Calculus | L4-L5 | 🆕 |

### 02-properties/ 属性推导 (9篇) [100%]

| 文档 | 描述 | 等级 |
|------|------|------|
| [02.01-determinism-in-streaming.md](./02-properties/02.01-determinism-in-streaming.md) | 流计算确定性 | L5 |
| [02.02-consistency-hierarchy.md](./02-properties/02.02-consistency-hierarchy.md) | 一致性层级 | L5 |
| [02.03-watermark-monotonicity.md](./02-properties/02.03-watermark-monotonicity.md) | Watermark单调性 | L5 |
| [02.04-liveness-and-safety.md](./02-properties/02.04-liveness-and-safety.md) | 活性与安全性 | L4-L5 |
| [02.05-type-safety-derivation.md](./02-properties/02.05-type-safety-derivation.md) | 类型安全推导 | L5 |
| [02.06-calm-theorem.md](./02-properties/02.06-calm-theorem.md) | CALM定理 | L5 |
| [02.07-encrypted-stream-processing.md](./02-properties/02.07-encrypted-stream-processing.md) | 加密流处理 | L5 |
| [02.08-differential-privacy-streaming.md](./02-properties/02.08-differential-privacy-streaming.md) | 差分隐私 | L5 |

### 03-relationships/ 关系建立 (6篇) [100%]

| 文档 | 描述 | 等级 |
|------|------|------|
| [03.01-actor-to-csp-encoding.md](./03-relationships/03.01-actor-to-csp-encoding.md) | Actor→CSP编码 | L4-L5 |
| [03.02-flink-to-process-calculus.md](./03-relationships/03.02-flink-to-process-calculus.md) | Flink→进程演算 | L5 |
| [03.03-expressiveness-hierarchy.md](./03-relationships/03.03-expressiveness-hierarchy.md) | 表达能力层次 | L3-L6 |
| [03.04-bisimulation-equivalences.md](./03-relationships/03.04-bisimulation-equivalences.md) | 互模拟等价 | L3-L4 |
| [03.05-cross-model-mappings.md](./03-relationships/03.05-cross-model-mappings.md) | 跨模型映射 | L5-L6 |
| [03.06-flink-distributed-architecture.md](./03-relationships/03.06-flink-distributed-architecture.md) | Flink分布式架构 | L4 |

### 04-proofs/ 形式证明 (8篇) [100%]

| 文档 | 描述 | 等级 |
|------|------|------|
| [04.01-flink-checkpoint-correctness.md](./04-proofs/04.01-flink-checkpoint-correctness.md) | Checkpoint正确性 | L5 |
| [04.02-flink-exactly-once-correctness.md](./04-proofs/04.02-flink-exactly-once-correctness.md) | Exactly-Once正确性 | L5 |
| [04.03-chandy-lamport-consistency.md](./04-proofs/04.03-chandy-lamport-consistency.md) | Chandy-Lamport一致性 | L5 |
| [04.04-watermark-algebra-formal-proof.md](./04-proofs/04.04-watermark-algebra-formal-proof.md) | Watermark代数证明 | L5 |
| [04.05-type-safety-fg-fgg.md](./04-proofs/04.05-type-safety-fg-fgg.md) | FG/FGG类型安全 | L5-L6 |
| [04.06-dot-subtyping-completeness.md](./04-proofs/04.06-dot-subtyping-completeness.md) | DOT子类型完备性 | L5-L6 |
| [04.07-deadlock-freedom-choreographic.md](./04-proofs/04.07-deadlock-freedom-choreographic.md) | Choreographic死锁自由 | L5 |

### 05-comparative-analysis/ 对比分析 (5篇) [100%]

| 文档 | 描述 | 等级 |
|------|------|------|
| [05.01-go-vs-scala-expressiveness.md](./05-comparative-analysis/05.01-go-vs-scala-expressiveness.md) | Go vs Scala | L4-L5 |
| [05.02-expressiveness-vs-decidability.md](./05-comparative-analysis/05.02-expressiveness-vs-decidability.md) | 表达vs可判定性 | L5 |
| [05.03-encoding-completeness-analysis.md](./05-comparative-analysis/05.03-encoding-completeness-analysis.md) | 编码完备性 | L4-L5 |
| [05.04-concurrency-models-2025-comparison.md](./05-comparative-analysis/05.04-concurrency-models-2025-comparison.md) | 并发模型2025 | L5 |

### 06-frontier/ 前沿研究 (12篇) [100%]

| 文档 | 描述 | 等级 |
|------|------|------|
| [06.01-open-problems-streaming-verification.md](./06-frontier/06.01-open-problems-streaming-verification.md) | 验证开放问题 | L4-L6 |
| [06.02-choreographic-streaming-programming.md](./06-frontier/06.02-choreographic-streaming-programming.md) | Choreographic流编程 | L5 |
| [06.03-ai-agent-session-types.md](./06-frontier/06.03-ai-agent-session-types.md) | AI Agent与会话类型 | L5 |
| [06.04-pdot-path-dependent-types.md](./06-frontier/06.04-pdot-path-dependent-types.md) | pDOT路径依赖类型 | L5-L6 |
| [06.05-ai-agent-streaming-formalization.md](./06-frontier/06.05-ai-agent-streaming-formalization.md) | AI Agent流式形式化 | L5-L6 |
| **[probabilistic-streaming](./06-frontier/probabilistic-streaming/probabilistic-stream-semantics.md)** | 概率流处理语义 | L5-L6 | 🆕 |
| **[first-person-choreographies](./06-frontier/first-person-choreographies/first-person-cp-advanced.md)** | 1CP前沿 | L6 | 🆕 |

### 07-tools/ 工具实践 (7篇) [100%]

| 文档 | 描述 | 等级 |
|------|------|------|
| [coq-mechanization.md](./07-tools/coq-mechanization.md) | Coq机械化证明 | L5-L6 |
| [iris-separation-logic.md](./07-tools/iris-separation-logic.md) | Iris分离逻辑 | L6 |
| [model-checking-practice.md](./07-tools/model-checking-practice.md) | 模型检查实践 | L4 |
| [smart-casual-verification.md](./07-tools/smart-casual-verification.md) | Smart Casual验证 | L4-L5 |
| [tla-for-flink.md](./07-tools/tla-for-flink.md) | TLA+验证Flink | L5 |
| **[ai-formal-verification](./07-tools/ai-formal-verification/ai-formal-verification-integration.md)** | AI+形式验证融合 | L6 | 🆕 |

### 08-standards/ 标准规范 (2篇) [100%]

| 文档 | 描述 | 等级 |
|------|------|------|
| [streaming-sql-standard.md](./08-standards/streaming-sql-standard.md) | 流式SQL标准 | L4 |

---

## 🆕 新增核心内容

| 新增领域 | 文档路径 | 关键贡献 |
|---------|---------|---------|
| **AI+形式验证融合** | `07-tools/ai-formal-verification/` | FoVer框架、神经证明证书、PRM形式化 |
| **Network Calculus** | `01-foundation/network-calculus/` | 延迟边界分析、积压分析、Min-Plus代数 |
| **概率流处理** | `06-frontier/probabilistic-streaming/` | PAC语义、随机处理器、近似正确性 |
| **1CP前沿** | `06-frontier/first-person-choreographies/` | 动态投影、Census Polymorphism |

---

## 项目完成度

```
总体进度: [████████████████████] 100% ✅ v2.0 FINAL
Struct/:    [████████████████████] 100% (50文档, 380定理)
Knowledge/: [████████████████████] 100% (250+文档)
Flink/:     [████████████████████] 100% (390+文档)
形式化元素: [████████████████████] 100% (10,745元素)
```

---

**关联文档**:
- [Knowledge/索引](../Knowledge/00-INDEX.md)
- [Flink/索引](../Flink/00-INDEX.md)
- [定理注册表](../THEOREM-REGISTRY.md)
