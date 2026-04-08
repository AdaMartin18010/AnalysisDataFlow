---
title: "[EN] 00 Index"
translation_status: "ai_translated"
source_file: "Struct/00-INDEX.md"
source_version: "9440fe02"
translator: "AI"
reviewer: null
translated_at: "2026-04-08T15:15:06.324523"
reviewed_at: null
quality_score: null
terminology_verified: false
---


<!-- AI Translation Template - Replace <!-- TRANSLATE --> markers with actual translation -->

<!-- TRANSLATE: # Struct/ 形式理论文档索引 -->

<!-- TRANSLATE: > **文档定位**: Struct 目录导航索引 | **形式化等级**: L1-L6 全覆盖 | **版本**: 2026.04 -->


<!-- TRANSLATE: ## 简介 -->

<!-- TRANSLATE: **Struct/** 目录包含流计算领域最严格的形式化理论文档，遵循六段式模板规范（概念定义→属性推导→关系建立→论证过程→形式证明→实例验证→可视化→引用参考）。本文档索引为整个形式理论体系提供结构化导航。 -->

<!-- TRANSLATE: **统计概览**: -->

<!-- TRANSLATE: - 总计: 43 篇形式化文档 -->
<!-- TRANSLATE: - 定理: 24 个 | 定义: 60 个 | 引理/命题: 80+ -->
<!-- TRANSLATE: - 覆盖: 进程演算、Actor模型、Dataflow、类型理论、验证方法 -->


<!-- TRANSLATE: ## 01-foundation/ 基础理论 (8篇) -->

<!-- TRANSLATE: 奠定流计算形式理论的元模型与核心概念基础。 -->

<!-- TRANSLATE: | 文档 | 描述 | 等级 | -->
<!-- TRANSLATE: |------|------|------| -->
<!-- TRANSLATE: | [01.01-unified-streaming-theory.md](./01-foundation/01.01-unified-streaming-theory.md) | **统一流计算元模型(USTM)** — 整合Actor、CSP、Dataflow、Petri网四大范式的形式化元理论，建立六层表达能力层次结构 | L6 | -->
<!-- TRANSLATE: | [01.02-process-calculus-primer.md](./01-foundation/01.02-process-calculus-primer.md) | **进程演算基础** — CCS、CSP、π-演算、会话类型的语法与操作语义，建立动态/静态通道模型的表达能力差异 | L3-L4 | -->
<!-- TRANSLATE: | [01.03-actor-model-formalization.md](./01-foundation/01.03-actor-model-formalization.md) | **Actor模型形式化** — Actor、Behavior、Mailbox、ActorRef、监督树的核心定义与串行处理引理 | L4-L5 | -->
<!-- TRANSLATE: | [01.04-dataflow-model-formalization.md](./01-foundation/01.04-dataflow-model-formalization.md) | **Dataflow模型形式化** — Dataflow图、算子语义、流作为偏序多重集、事件时间/处理时间/Watermark、窗口形式化 | L5 | -->
<!-- TRANSLATE: | [01.05-csp-formalization.md](./01-foundation/01.05-csp-formalization.md) | **CSP形式化** — CSP核心语法、结构化操作语义、迹/失败/发散语义、通道与同步原语 | L3 | -->
<!-- TRANSLATE: | [01.06-petri-net-formalization.md](./01-foundation/01.06-petri-net-formalization.md) | **Petri网形式化** — P/T网、变迁触发规则、可达性分析、着色Petri网(CPN)、时间Petri网(TPN)层次结构 | L2-L4 | -->
<!-- TRANSLATE: | [01.07-session-types.md](./01-foundation/01.07-session-types.md) | **会话类型** — 二元/多参会话类型语法、双寡规则、会话与进程的编码关系 | L4-L5 | -->
<!-- TRANSLATE: | [stream-processing-semantics-formalization.md](./01-foundation/stream-processing-semantics-formalization.md) | **流处理语义学形式化** — 流作为无限序列的形式化定义、时间模型、语义映射 | L5-L6 | -->


<!-- TRANSLATE: ## 03-relationships/ 关系建立 (5篇) -->

<!-- TRANSLATE: 不同模型、系统、语言之间的形式化关系与编码理论。 -->

<!-- TRANSLATE: | 文档 | 描述 | 等级 | -->
<!-- TRANSLATE: |------|------|------| -->
<!-- TRANSLATE: | [03.01-actor-to-csp-encoding.md](./03-relationships/03.01-actor-to-csp-encoding.md) | **Actor到CSP编码** — Actor→CSP编码函数`[[·]]_A→C`、Mailbox的Buffer进程编码、动态地址传递的不可编码性证明 | L4-L5 | -->
<!-- TRANSLATE: | [03.02-flink-to-process-calculus.md](./03-relationships/03.02-flink-to-process-calculus.md) | **Flink到进程演算编码** — Flink算子到π-演算进程、数据流边到通道、Checkpoint到屏障同步协议的编码 | L5 | -->
<!-- TRANSLATE: | [03.03-expressiveness-hierarchy.md](./03-relationships/03.03-expressiveness-hierarchy.md) | **表达能力层次定理** — 表达能力预序、六层层次(L1-L6)严格性证明、可判定性单调递减律 | L3-L6 | -->
<!-- TRANSLATE: | [03.04-bisimulation-equivalences.md](./03-relationships/03.04-bisimulation-equivalences.md) | **互模拟等价关系** — 强/弱/分支互模拟、互模拟游戏、同余关系、互模拟与迹等价的关系 | L3-L4 | -->
<!-- TRANSLATE: | [03.05-cross-model-mappings.md](./03-relationships/03.05-cross-model-mappings.md) | **跨模型统一映射框架** — 四层统一映射框架、层间Galois连接、跨层组合映射、语义保持性与精化关系 | L5-L6 | -->


<!-- TRANSLATE: ## 05-comparative-analysis/ 对比分析 (3篇) -->

<!-- TRANSLATE: 不同语言、模型、方法之间的系统性对比研究。 -->

<!-- TRANSLATE: | 文档 | 描述 | 等级 | -->
<!-- TRANSLATE: |------|------|------| -->
<!-- TRANSLATE: | [05.01-go-vs-scala-expressiveness.md](./05-comparative-analysis/05.01-go-vs-scala-expressiveness.md) | **Go vs Scala表达能力对比** — 类型系统层次、并发原语抽象层次、元编程能力差异、图灵完备性等价证明 | L4-L5 | -->
<!-- TRANSLATE: | [05.02-expressiveness-vs-decidability.md](./05-comparative-analysis/05.02-expressiveness-vs-decidability.md) | **表达能力与可判定性权衡** — 可判定性集合、Rice定理框架、停机问题归约、六层模型的权衡分析 | L5 | -->
<!-- TRANSLATE: | [05.03-encoding-completeness-analysis.md](./05-comparative-analysis/05.03-encoding-completeness-analysis.md) | **编码完备性分析** — 编码判据体系、满抽象(Full Abstraction)、完备性度量、忠实编码(Faithful Encoding) | L4-L5 | -->


<!-- TRANSLATE: ## 07-tools/ 工具实践 (5篇) -->

<!-- TRANSLATE: 形式化验证工具与机械化证明实践。 -->

<!-- TRANSLATE: | 文档 | 描述 | 等级 | -->
<!-- TRANSLATE: |------|------|------| -->
<!-- TRANSLATE: | [coq-mechanization.md](./07-tools/coq-mechanization.md) | **Coq机械化证明** — 归纳类型定义、流计算性质的Coq形式化、证明自动化策略 | L5-L6 | -->
<!-- TRANSLATE: | [iris-separation-logic.md](./07-tools/iris-separation-logic.md) | **Iris高阶并发分离逻辑** — 分离逻辑基础、高阶幽灵状态、原子性抬升、Flink并发性质的Iris证明 | L6 | -->
<!-- TRANSLATE: | [model-checking-practice.md](./07-tools/model-checking-practice.md) | **模型检查实践** — LTL/CTL时序逻辑、SPIN/NuSMV应用、流计算系统的模型检查方法 | L4 | -->
<!-- TRANSLATE: | [smart-casual-verification.md](./07-tools/smart-casual-verification.md) | **Smart Casual Verification** — 系统化形式化规范(TLA+)+自动化测试的混合验证方法、Microsoft CCF实践案例 | L4-L5 | -->
<!-- TRANSLATE: | [tla-for-flink.md](./07-tools/tla-for-flink.md) | **TLA+形式化验证Flink** — TLA+规格语言、PlusCal算法、Flink Checkpoint/Exactly-Once的TLA+规格与验证 | L5 | -->


<!-- TRANSLATE: ## 09-unified/ 统一图谱 (1篇) -->

<!-- TRANSLATE: 全项目统一关系图谱与跨模型整合。 -->

<!-- TRANSLATE: | 文档 | 描述 | 等级 | -->
<!-- TRANSLATE: |------|------|------| -->
<!-- TRANSLATE: | [Unified-Model-Relationship-Graph.md](./Unified-Model-Relationship-Graph.md) | **统一模型关系图谱** — 全项目计算模型的统一关系图谱，包括表达力层级、编码关系、等价关系、决策矩阵 | L4-L5 | -->


<!-- TRANSLATE: ## 导航链接 -->

<!-- TRANSLATE: **根目录索引**: -->

<!-- TRANSLATE: - [📁 项目根目录](../README.md) — 项目总览与快速开始 -->
<!-- TRANSLATE: - [📋 AGENTS.md](../AGENTS.md) — Agent工作上下文规范 -->
<!-- TRANSLATE: - [🗺️ NAVIGATION-INDEX.md](../NAVIGATION-INDEX.md) — 全局导航索引 -->

<!-- TRANSLATE: **其他核心索引**: -->

<!-- TRANSLATE: - [📚 Knowledge/索引](../Knowledge/00-INDEX.md) — 知识结构文档导航 -->
<!-- TRANSLATE: - [⚡ Flink/索引](../Struct/00-INDEX.md) — Flink专项文档导航 -->
<!-- TRANSLATE: - [📖 THEOREM-REGISTRY.md](../THEOREM-REGISTRY.md) — 全库定理注册表 -->

<!-- TRANSLATE: **学习路径**: -->

<!-- TRANSLATE: - [🎓 LEARNING-PATH-GUIDE.md](../LEARNING-PATH-GUIDE.md) — 学习路径指南 -->
<!-- TRANSLATE: - [🧮 GLOSSARY.md](../GLOSSARY.md) — 术语表 -->
