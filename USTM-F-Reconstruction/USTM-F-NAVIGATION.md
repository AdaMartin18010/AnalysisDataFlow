# USTM-F 统一流计算理论 - 导航索引

> **快速导航与交叉引用中心** | 32篇文档 | 完整形式化框架
> **版本**: v1.0 | **最后更新**: 2026-04-08

---

## 📋 文档总览

USTM-F (Unified Streaming Theory Meta-Framework) 是一个严格、系统、完整的数据流计算形式理论框架，包含 **32篇核心文档**，分为 **5个阶段**。

---

## 🗺️ 阶段导航

| 阶段 | 目录 | 文档数 | 主题 | 形式化等级 |
|------|------|--------|------|-----------|
| **L0** | [00-meta/](#l0-元理论基础) | 4 | 范畴论、格论、类型论 | L6 |
| **L1** | [01-unified-model/](#l1-统一流模型) | 6 | 流计算核心模型 | L6 |
| **L2** | [02-model-instantiation/](#l2-模型实例化) | 8 | 7大计算模型编码 | L5-L6 |
| **L3** | [03-proof-chains/](#l3-证明链) | 8 | 核心定理完整证明 | L6 |
| **L4** | [04-encoding-verification/](#l4-编码与验证) | 6 | 形式化验证工具 | L5-L6 |

---

## L0: 元理论基础

> 数学基础层 - 范畴论、格论、类型论

| 文档 | 核心内容 | 定义 | 定理 | 依赖 |
|------|----------|------|------|------|
| **[00.01-category-theory-foundation.md](./00-meta/00.01-category-theory-foundation.md)** | 范畴论基础 | Def-M-01~10 | Thm-M-01~03 | - |
| **[00.02-lattice-order-theory.md](./00-meta/00.02-lattice-order-theory.md)** | 格论与序理论 | Def-M-11~20 | Thm-M-04~05 | - |
| **[00.03-type-theory-foundation.md](./00-meta/00.03-type-theory-foundation.md)** | 类型论基础 | Def-M-21~30 | Thm-M-06~07 | - |
| **[00.00-ustm-f-overview.md](./00-meta/00.00-ustm-f-overview.md)** | 元理论概览 | Def-M-00,31~33 | Thm-M-08 | 00.01~00.03 |

**📖 推荐阅读顺序**: 00.01 → 00.02 → 00.03 → 00.00

---

## L1: 统一流模型

> 流计算核心理论 - USTM形式化定义

| 文档 | 核心内容 | 定义 | 定理 | 依赖 |
|------|----------|------|------|------|
| **[01.01-stream-mathematical-definition.md](./01-unified-model/01.01-stream-mathematical-definition.md)** | 流的数学定义 | Def-U-01~10 | Thm-U-01~02 | 00.01 |
| **[01.02-unified-time-model.md](./01-unified-model/01.02-unified-time-model.md)** | 统一时间模型 | Def-U-11~20 | Thm-U-03 | 01.01 |
| **[01.03-operator-algebra.md](./01-unified-model/01.03-operator-algebra.md)** | 算子代数 | Def-U-21~30 | - | 01.01 |
| **[01.04-composition-theory.md](./01-unified-model/01.04-composition-theory.md)** | 组合理论 | Def-U-31~40 | Thm-U-05~06 | 01.03 |
| **[01.05-ustm-core-semantics.md](./01-unified-model/01.05-ustm-core-semantics.md)** | USTM核心语义 | Def-U-41~50 | Thm-U-03~04 | 01.02, 01.04, 00.03 |
| **[01.00-unified-streaming-theory-v2.md](./01-unified-model/01.00-unified-streaming-theory-v2.md)** | USTM整合 | Def-U-51~58 | Thm-U-07~08 | 01.01~01.05 |

**📖 推荐阅读顺序**: 01.01 → 01.02 → 01.03 → 01.04 → 01.05 → 01.00

---

## L2: 模型实例化

> 7大计算模型到USTM的编码

### 框架文档

| 文档 | 核心内容 | 定义 | 定理 | 依赖 |
|------|----------|------|------|------|
| **[02.00-model-instantiation-framework.md](./02-model-instantiation/02.00-model-instantiation-framework.md)** | 模型实例化框架 | Def-I-00-01~07 | Thm-I-00-01~02 | 01.00 |

### 具体模型编码

| 文档 | 模型 | 表达能力 | 依赖 |
|------|------|----------|------|
| **[02.01-actor-in-ustm.md](./02-model-instantiation/02.01-actor-in-ustm.md)** | Actor模型 | L4 (Mobile) | 02.00, 01.01 |
| **[02.02-csp-in-ustm.md](./02-model-instantiation/02.02-csp-in-ustm.md)** | CSP | L3 (Process Algebra) | 02.00, 01.01 |
| **[02.03-dataflow-in-ustm.md](./02-model-instantiation/02.03-dataflow-in-ustm.md)** | Dataflow模型 | L4 (Mobile) | 02.00, 01.01 |
| **[02.04-petri-net-in-ustm.md](./02-model-instantiation/02.04-petri-net-in-ustm.md)** | Petri网 | L2-L4 | 02.00, 01.01 |
| **[02.05-pi-calculus-in-ustm.md](./02-model-instantiation/02.05-pi-calculus-in-ustm.md)** | π-演算 | L4 (Mobile) | 02.00, 01.01 |
| **[02.06-session-types-in-ustm.md](./02-model-instantiation/02.06-session-types-in-ustm.md)** | 会话类型 | L4-L5 | 02.00, 01.05 |
| **[02.07-flink-in-ustm.md](./02-model-instantiation/02.07-flink-in-ustm.md)** | Flink | L6 (Turing-Complete) | 02.00, 01.00 |

**📖 推荐阅读顺序**: 02.00 → (02.01~02.07 可并行阅读)

---

## L3: 证明链

> 核心定理的完整形式证明

### 基础与整合

| 文档 | 核心内容 | 引理/定理 | 依赖 | 被依赖 |
|------|----------|-----------|------|--------|
| **[03.01-fundamental-lemmas.md](./03-proof-chains/03.01-fundamental-lemmas.md)** | 基础引理库 | Lemma-U-01~50 | 01.01, 01.03, 01.05 | 全部03.x |
| **[03.00-proof-chains-compendium.md](./03-proof-chains/03.00-proof-chains-compendium.md)** | 证明链整合 | 全部证明链 | 03.01~03.07 | - |

### 核心定理证明

| 文档 | 定理 | 定理名称 | 关键引理 | 依赖 |
|------|------|----------|----------|------|
| **[03.02-determinism-theorem-proof.md](./03-proof-chains/03.02-determinism-theorem-proof.md)** | **Thm-U-20** | 流计算确定性定理 | Lemma-U-31~34 | 03.01 |
| **[03.03-consistency-lattice-theorem.md](./03-proof-chains/03.03-consistency-lattice-theorem.md)** | Thm-U-21~22 | 一致性格定理 | Lemma-U-35~37 | 03.01 |
| **[03.04-watermark-monotonicity-proof.md](./03-proof-chains/03.04-watermark-monotonicity-proof.md)** | **Thm-U-25** | Watermark单调性定理 | Lemma-U-38~40 | 03.01 |
| **[03.05-checkpoint-correctness-proof.md](./03-proof-chains/03.05-checkpoint-correctness-proof.md)** | **Thm-U-30** | Checkpoint一致性定理 | Lemma-U-41~43 | 03.01, 03.02 |
| **[03.06-exactly-once-semantics-proof.md](./03-proof-chains/03.06-exactly-once-semantics-proof.md)** | **Thm-U-35** | Exactly-Once语义定理 | Lemma-U-44~46 | 03.01, 03.03, 03.05 |
| **[03.07-type-safety-proof.md](./03-proof-chains/03.07-type-safety-proof.md)** | Thm-U-36~38 | FG/FGG类型安全定理 | Lemma-U-47~50 | 03.01 |

**📖 证明验证顺序**: 03.01 → 03.02 → 03.05 → 03.06 (核心链)

---

## L4: 编码与验证

> 模型间编码与形式化验证工具

| 文档 | 核心内容 | 依赖 | 工具 |
|------|----------|------|------|
| **[04.01-encoding-theory.md](./04-encoding-verification/04.01-encoding-theory.md)** | 编码一般理论 | 02.00 | - |
| **[04.02-actor-csp-encoding.md](./04-encoding-verification/04.02-actor-csp-encoding.md)** | Actor↔CSP编码 | 02.01, 02.02, 03.02 | - |
| **[04.03-dataflow-csp-encoding.md](./04-encoding-verification/04.03-dataflow-csp-encoding.md)** | Dataflow→CSP编码 | 02.03, 02.02 | - |
| **[04.04-expressiveness-hierarchy-v2.md](./04-encoding-verification/04.04-expressiveness-hierarchy-v2.md)** | 表达能力层次 | 02.00, 03.03 | - |
| **[04.05-coq-formalization.md](./04-encoding-verification/04.05-coq-formalization.md)** | Coq形式化 | 03.07 | Coq |
| **[04.06-tla-plus-specifications.md](./04-encoding-verification/04.06-tla-plus-specifications.md)** | TLA+规约 | 02.07, 03.05 | TLA+ |

---

## 🔑 关键定理快速索引

### 核心定理 (带证明文档链接)

| 定理 | 名称 | 证明文档 | 应用 |
|------|------|----------|------|
| [Thm-U-20](./03-proof-chains/03.02-determinism-theorem-proof.md#thm-u-20-流计算确定性定理) | 流计算确定性定理 | 03.02 | Flink确定性保证 |
| [Thm-U-21](./03-proof-chains/03.03-consistency-lattice-theorem.md#thm-u-21-一致性格定理) | 一致性格定理 | 03.03 | 一致性配置 |
| [Thm-U-25](./03-proof-chains/03.04-watermark-monotonicity-proof.md#thm-u-25-watermark单调性定理) | Watermark单调性定理 | 03.04 | 窗口触发 |
| [Thm-U-30](./03-proof-chains/03.05-checkpoint-correctness-proof.md#thm-u-30-checkpoint一致性定理) | Checkpoint一致性定理 | 03.05 | 故障恢复 |
| [Thm-U-35](./03-proof-chains/03.06-exactly-once-semantics-proof.md#thm-u-35-exactly-once语义定理) | Exactly-Once语义定理 | 03.06 | 端到端一致性 |
| [Thm-U-38](./03-proof-chains/03.07-type-safety-proof.md#thm-u-38-fgfgg类型安全定理) | FG/FGG类型安全定理 | 03.07 | 编译器验证 |

---

## 📊 形式化元素统计

| 阶段 | 定义 | 定理 | 引理 | 命题 |
|------|------|------|------|------|
| L0 元理论 | 34 | 8 | 11 | - |
| L1 统一模型 | 58 | 8 | 10 | - |
| L2 模型实例化 | 50+ | 2 | 3 | 1 |
| L3 证明链 | 10 | 10 | 53 | - |
| L4 编码验证 | 20+ | - | - | - |
| **总计** | **172+** | **28** | **77+** | **1** |

---

## 🔗 快速链接

### 辅助文档

- **[USTM-F-DEPENDENCY-GRAPH.md](./USTM-F-DEPENDENCY-GRAPH.md)** - 完整文档依赖关系图
- **[00-INDEX.md](./00-INDEX.md)** - 项目总索引
- **[templates/ustm-f-document-template.md](./templates/ustm-f-document-template.md)** - 文档模板

### 证明助手

- **[proof-assistant/coq/README.md](./04-encoding-verification/proof-assistant/coq/README.md)** - Coq形式化项目
- **[proof-assistant/tla/README.md](./04-encoding-verification/proof-assistant/tla/README.md)** - TLA+规约项目

---

## 📖 推荐阅读路径

### 路径1: 理论学习路径 (8周)

适合希望系统学习流计算理论的读者。

```
Week 1-2:  00.01 → 00.02 → 00.03 (元理论基础)
Week 3-4:  01.01 → 01.02 → 01.03 (核心概念)
Week 5:    01.04 → 01.05 (组合与语义)
Week 6:    01.00 (USTM整合)
Week 7:    02.00 → 02.07 (Flink实例化)
Week 8:    03.00 (证明链概览)
```

### 路径2: 定理验证路径 (4周)

适合希望深入理解证明细节的读者。

```
Week 1:  03.01 (基础引理库)
Week 2:  03.02 (确定性) → 03.05 (Checkpoint)
Week 3:  03.06 (Exactly-Once)
Week 4:  03.07 (类型安全)
```

### 路径3: 工程应用路径 (3周)

适合希望将理论应用于工程实践的读者。

```
Week 1:  01.00 → 02.07 (Flink实例化)
Week 2:  03.05 → 03.06 (容错语义)
Week 3:  04.06 (TLA+规约)
```

### 路径4: 快速概览路径 (1周)

适合希望快速了解USTM-F全貌的读者。

```
Day 1:  00.00 (概览)
Day 2:  01.00 (USTM整合)
Day 3:  02.00 (模型实例化框架)
Day 4:  03.00 (证明链整合)
Day 5:  04.04 (表达能力层次)
```

---

## 🎯 使用指南

### 如何查找特定主题

1. **使用文档头部信息**: 每篇文档头部包含"所属阶段"、"前置依赖"、"形式化等级"
2. **使用定理编号**: 所有定理遵循 `Thm-{阶段}-{序号}` 格式，可在[定理索引](#关键定理快速索引)中查找
3. **使用依赖图**: 参考 [USTM-F-DEPENDENCY-GRAPH.md](./USTM-F-DEPENDENCY-GRAPH.md) 了解文档间关系

### 如何验证证明

1. 从 [03.01-fundamental-lemmas.md](./03-proof-chains/03.01-fundamental-lemmas.md) 开始
2. 按依赖顺序阅读证明文档 (03.02 → 03.05 → 03.06)
3. 检查证明中引用的引理和定义
4. 使用 Coq/TLA+ 形式化验证 (04.05, 04.06)

### 如何贡献

1. 遵循 [文档模板](./templates/ustm-f-document-template.md)
2. 为新定义分配编号 (Def-X-XX)
3. 在 [USTM-F-NAVIGATION.md](./USTM-F-NAVIGATION.md) 中添加条目
4. 更新 [USTM-F-DEPENDENCY-GRAPH.md](./USTM-F-DEPENDENCY-GRAPH.md) 中的依赖关系

---

## 📚 引用格式

引用USTM-F文档时，请使用以下格式:

```
[文档编号] 文档标题, USTM-F Reconstruction, 2026.
https://github.com/[org]/AnalysisDataFlow/tree/main/USTM-F-Reconstruction/[路径]

例如:
[01.00] 统一流计算理论v2, USTM-F Reconstruction, 2026.
[03.02] 确定性定理完整证明, USTM-F Reconstruction, 2026.
```

---

*USTM-F 统一流计算理论元框架 | 版本 v1.0 | 最后更新: 2026-04-08*
