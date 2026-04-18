> **状态**: 🔮 前瞻内容 | **风险等级**: 高 | **最后更新**: 2026-04
> 
> 此文档描述的内容处于早期规划阶段，可能与最终实现不符。请以 Apache Flink 官方发布为准。
# 全量交叉引用验证报告 v3

> 生成时间: 2026-04-11T20:55:38.896287
> 验证范围: Struct/ Knowledge/ Flink/ 目录下的所有Markdown文件
> 验证版本: v3（支持带数字前缀的标题锚点）

## 📊 统计概览

| 指标 | 数值 |
|------|------|
| **扫描文件数** | 655 |
| **总引用数** | 11,976 |
| **有效引用** | 10,155 |
| **已忽略** (外部链接/代码) | 121 |
| **断裂引用** | 1,700 |
| **文件不存在** | 12 |
| **锚点不存在** | 1,688 |
| **有效引用率** | 85.66% |

## 🔴 断裂引用详情

### 1. 文件不存在错误 (12 个)

| 源文件 | 行号 | 链接文本 | 目标路径 | 代码片段 |
|--------|------|----------|----------|----------|
| `Flink\03-api\09-language-foundations\02.01-java-api-from-scala.md` | 108 | Integer | `Flink\03-api\09-language-foundations\_.l` | `stream.map[Integer](_.length)  // 显式指定返回` |
| `Flink\03-api\09-language-foundations\05-datastream-v2-api.md` | 902 | Long | `Flink\03-api\09-language-foundations\"co` | `.valueState[Long]("counter")  // 类型参数 Lo` |
| `Knowledge\case-studies\ecommerce-realtime-recommendation-v2.md` | 3 | Knowledge/10-case-studies/ecom | `10-case-studies\ecommerce\10.2.1-realtim` | `> **所属阶段**: Knowledge/case-studies/ecomm` |
| `Knowledge\case-studies\fraud-detection-production-case.md` | 3 | Knowledge/case-studies/finance | `Knowledge\case-studies\realtime-anti-fra` | `> **所属阶段**: Knowledge/case-studies/finan` |
| `Knowledge\case-studies\gaming-analytics-platform-case.md` | 3 | Knowledge/case-studies/gaming/ | `Knowledge\case-studies\realtime-game-ana` | `> **所属阶段**: Knowledge/case-studies/gamin` |
| `Knowledge\case-studies\iot-smart-grid-case-study.md` | 3 | Knowledge/10-case-studies/iot/ | `10-case-studies\iot\10.3.1-smart-meter-d` | `> **所属阶段**: Knowledge/case-studies/iot |` |
| `Struct\01-foundation\01.10-schema-evolution-formalization.md` | 790 | Flink Schema Evolution Guide | `Struct\Flink\flink-schema-evolution-guid` | `- [Flink Schema Evolution Guide](../Flin` |
| `Struct\01-foundation\01.10-schema-evolution-formalization.md` | 791 | Knowledge/Schema Design Patter | `Struct\Knowledge\03-data-management\sche` | `- [Knowledge/Schema Design Patterns](../` |
| `Struct\04-proofs\04.05-type-safety-fg-fgg.md` | 172 | \bar{\sigma} | `Struct\04-proofs\v_1, ...` | `\text{(R-Call-G)} & v.m[\bar{\sigma}](v_` |
| `Struct\06-frontier\06.05-ai-agent-streaming-formalization.md` | 3 | 05.03-streaming-dataflow-equiv | `Struct\05-foundations\05.03-streaming-da` | `> **所属阶段**: Struct/06-frontier | **前置依赖*` |
| `Struct\06-frontier\research-trends-analysis-2024-2026.md` | 518 | 02-B-evolution/flink-2.0-async | `Flink\02-core\02-B-evolution\flink-2.0-a` | `- [02-B-evolution/flink-2.0-async-execut` |
| `Struct\Proof-Chains-Process-Calculus-Foundation.md` | 323 | νx | `Struct\·` | `- 限制上下文[νx](·): 限制不破坏模拟关系` |

### 2. 锚点不存在错误 (1688 个)

展示前100个:

| 源文件 | 行号 | 链接文本 | 目标文件 | 缺失锚点 |
|--------|------|----------|----------|----------|
| `Flink\00-FLINK-TECH-STACK-DEPENDENCY.md` | 25 | 关系 1: Core → API 支撑关系 | `Flink\00-FLINK-TECH-STACK-DEPENDENC` | `#关系-1-core--api-支撑关系` |
| `Flink\00-FLINK-TECH-STACK-DEPENDENCY.md` | 26 | 关系 2: API → Runtime 依赖关系 | `Flink\00-FLINK-TECH-STACK-DEPENDENC` | `#关系-2-api--runtime-依赖关系` |
| `Flink\00-FLINK-TECH-STACK-DEPENDENCY.md` | 27 | 关系 3: Runtime → Ecosystem | `Flink\00-FLINK-TECH-STACK-DEPENDENC` | `#关系-3-runtime--ecosystem-集成关系` |
| `Flink\00-FLINK-TECH-STACK-DEPENDENCY.md` | 28 | 关系 4: Ecosystem → Practic | `Flink\00-FLINK-TECH-STACK-DEPENDENC` | `#关系-4-ecosystem--practices-指导关系` |
| `Flink\00-FLINK-TECH-STACK-DEPENDENCY.md` | 36 | 6.1 Core → API 依赖实例 | `Flink\00-FLINK-TECH-STACK-DEPENDENC` | `#61-core--api-依赖实例` |
| `Flink\00-FLINK-TECH-STACK-DEPENDENCY.md` | 37 | 6.2 API → Runtime 依赖实例 | `Flink\00-FLINK-TECH-STACK-DEPENDENC` | `#62-api--runtime-依赖实例` |
| `Flink\00-FLINK-TECH-STACK-DEPENDENCY.md` | 38 | 6.3 Runtime → Ecosystem 依 | `Flink\00-FLINK-TECH-STACK-DEPENDENC` | `#63-runtime--ecosystem-依赖实例` |
| `Flink\00-FLINK-TECH-STACK-DEPENDENCY.md` | 39 | 6.4 Ecosystem → Practices | `Flink\00-FLINK-TECH-STACK-DEPENDENC` | `#64-ecosystem--practices-依赖实例` |
| `Flink\00-meta\00-QUICK-START.md` | 11 | Flink 2.4/2.5 快速开始指南 | `Flink\00-meta\00-QUICK-START.md` | `#flink-2425-快速开始指南` |
| `Flink\00-meta\00-QUICK-START.md` | 17 | 2. Flink 2.4 新特性快速体验 | `Flink\00-meta\00-QUICK-START.md` | `#2-flink-24-新特性快速体验` |
| `Flink\00-meta\00-QUICK-START.md` | 21 | 3. Flink 2.5 预览体验 | `Flink\00-meta\00-QUICK-START.md` | `#3-flink-25-预览体验` |
| `Flink\00-meta\00-QUICK-START.md` | 32 | 5.1 初学者路径（2-3 周） | `Flink\00-meta\00-QUICK-START.md` | `#51-初学者路径2-3-周` |
| `Flink\00-meta\00-QUICK-START.md` | 33 | 5.2 进阶路径（AI/ML 方向） | `Flink\00-meta\00-QUICK-START.md` | `#52-进阶路径aiml-方向` |
| `Flink\00-meta\00-QUICK-START.md` | 37 | 6.2 Flink 2.4/2.5 特性矩阵 | `Flink\00-meta\00-QUICK-START.md` | `#62-flink-2425-特性矩阵` |
| `Flink\00-meta\version-tracking\flink-26-27-roadmap` | 12 | .scripts/flink-release-tr | `Flink\00-meta\version-tracking\flin` | `#` |
| `Flink\01-concepts\datastream-v2-semantics.md` | 24 | 关系 1: DataStream V1 `↦` D | `Flink\01-concepts\datastream-v2-sem` | `#关系-1-datastream-v1--datastream-v2` |
| `Flink\01-concepts\datastream-v2-semantics.md` | 25 | 关系 2: DataStream V2 `≈` D | `Flink\01-concepts\datastream-v2-sem` | `#关系-2-datastream-v2--dataflow-模型` |
| `Flink\01-concepts\datastream-v2-semantics.md` | 26 | 关系 3: Async State Access  | `Flink\01-concepts\datastream-v2-sem` | `#关系-3-async-state-access--分离状态存储架构` |
| `Flink\01-concepts\datastream-v2-semantics.md` | 29 | 4.2 反例：V1 运行时类型错误 | `Flink\01-concepts\datastream-v2-sem` | `#42-反例v1-运行时类型错误` |
| `Flink\01-concepts\datastream-v2-semantics.md` | 30 | 4.3 反例：异步读写乱序完成 | `Flink\01-concepts\datastream-v2-sem` | `#43-反例异步读写乱序完成` |
| `Flink\01-concepts\datastream-v2-semantics.md` | 31 | 4.4 边界讨论：延迟-一致性权衡 | `Flink\01-concepts\datastream-v2-sem` | `#44-边界讨论延迟-一致性权衡` |
| `Flink\01-concepts\datastream-v2-semantics.md` | 32 | 5. 形式证明 / 工程论证 (Proof / E | `Flink\01-concepts\datastream-v2-sem` | `#5-形式证明--工程论证-proof--engineering-argument` |
| `Flink\01-concepts\datastream-v2-semantics.md` | 35 | 工程论证：V2 选型决策 | `Flink\01-concepts\datastream-v2-sem` | `#工程论证v2-选型决策` |
| `Flink\01-concepts\datastream-v2-semantics.md` | 37 | 示例 6.1: 端到端 DataStream V2 | `Flink\01-concepts\datastream-v2-sem` | `#示例-61-端到端-datastream-v2-作业` |
| `Flink\01-concepts\datastream-v2-semantics.md` | 38 | 示例 6.2: Record Attributes | `Flink\01-concepts\datastream-v2-sem` | `#示例-62-record-attributes-的使用` |
| `Flink\01-concepts\deployment-architectures.md` | 17 | 2. 属性/特征 (Properties) | `Flink\01-concepts\deployment-archit` | `#2-属性特征-properties` |
| `Flink\01-concepts\deployment-architectures.md` | 20 | 3. 关系/对比 (Relations \& Co | `Flink\01-concepts\deployment-archit` | `#3-关系对比-relations--comparisons` |
| `Flink\01-concepts\deployment-architectures.md` | 21 | 3.1 部署模式 × 资源平台的组合空间 | `Flink\01-concepts\deployment-archit` | `#31-部署模式--资源平台的组合空间` |
| `Flink\01-concepts\deployment-architectures.md` | 25 | 4. 论证/选型逻辑 (Argumentation | `Flink\01-concepts\deployment-archit` | `#4-论证选型逻辑-argumentation--selection-logic` |
| `Flink\01-concepts\deployment-architectures.md` | 27 | 4.2 决策树：选择哪种部署模式？ | `Flink\01-concepts\deployment-archit` | `#42-决策树选择哪种部署模式` |
| `Flink\01-concepts\deployment-architectures.md` | 30 | 5.1 实例 1：Kubernetes Nativ | `Flink\01-concepts\deployment-archit` | `#51-实例-1kubernetes-native-application-mode-部署` |
| `Flink\01-concepts\deployment-architectures.md` | 31 | 5.2 实例 2：YARN Session Clu | `Flink\01-concepts\deployment-archit` | `#52-实例-2yarn-session-cluster-部署多租户数据平台` |
| `Flink\01-concepts\deployment-architectures.md` | 32 | 5.3 实例 3：Standalone Per-J | `Flink\01-concepts\deployment-archit` | `#53-实例-3standalone-per-job-的变通实现边缘计算` |
| `Flink\01-concepts\disaggregated-state-analysis.md` | 25 | 引理 4.1 (分离存储故障恢复加速原理) | `Flink\01-concepts\disaggregated-sta` | `#引理-41-分离存储故障恢复加速原理` |
| `Flink\01-concepts\disaggregated-state-analysis.md` | 26 | 引理 4.2 (增量 Checkpoint 的存储 | `Flink\01-concepts\disaggregated-sta` | `#引理-42-增量-checkpoint-的存储效率` |
| `Flink\01-concepts\disaggregated-state-analysis.md` | 27 | 反例 4.1 (网络分区下的缓存不一致) | `Flink\01-concepts\disaggregated-sta` | `#反例-41-网络分区下的缓存不一致` |
| `Flink\01-concepts\disaggregated-state-analysis.md` | 32 | 示例 6.1: 大状态作业从 MemoryStat | `Flink\01-concepts\disaggregated-sta` | `#示例-61-大状态作业从-memorystatebackend-迁移到分离存储` |
| `Flink\01-concepts\disaggregated-state-analysis.md` | 33 | 示例 6.2: 实时风控场景的同步策略配置 | `Flink\01-concepts\disaggregated-sta` | `#示例-62-实时风控场景的同步策略配置` |
| `Flink\01-concepts\disaggregated-state-analysis.md` | 34 | 示例 6.3: 跨可用区故障恢复对比 | `Flink\01-concepts\disaggregated-sta` | `#示例-63-跨可用区故障恢复对比` |
| `Flink\01-concepts\flink-1.x-vs-2.0-comparison.md` | 11 | Flink 1.x vs 2.0 架构对比 (Fl | `Flink\01-concepts\flink-1.x-vs-2.0-` | `#flink-1x-vs-20-架构对比-flink-1x-vs-20-architecture-comparison` |
| `Flink\01-concepts\flink-1.x-vs-2.0-comparison.md` | 15 | 2.1 Flink 1.x 架构模型 | `Flink\01-concepts\flink-1.x-vs-2.0-` | `#21-flink-1x-架构模型` |
| `Flink\01-concepts\flink-1.x-vs-2.0-comparison.md` | 16 | 2.2 Flink 2.0 架构模型 | `Flink\01-concepts\flink-1.x-vs-2.0-` | `#22-flink-20-架构模型` |
| `Flink\01-concepts\flink-1.x-vs-2.0-comparison.md` | 20 | 4.1 本地状态存储 (Flink 1.x) | `Flink\01-concepts\flink-1.x-vs-2.0-` | `#41-本地状态存储-flink-1x` |
| `Flink\01-concepts\flink-1.x-vs-2.0-comparison.md` | 21 | 4.2 分离状态存储 (Flink 2.0) | `Flink\01-concepts\flink-1.x-vs-2.0-` | `#42-分离状态存储-flink-20` |
| `Flink\01-concepts\flink-1.x-vs-2.0-comparison.md` | 36 | 从 Flink 1.x 创建 Savepoint | `Flink\01-concepts\flink-1.x-vs-2.0-` | `#从-flink-1x-创建-savepoint` |
| `Flink\01-concepts\flink-1.x-vs-2.0-comparison.md` | 37 | 使用 Flink 2.0 恢复 | `Flink\01-concepts\flink-1.x-vs-2.0-` | `#使用-flink-20-恢复` |
| `Flink\02-core\adaptive-execution-engine-v2.md` | 45 | 论证 4.1: 为什么需要自适应执行引擎？ | `Flink\02-core\adaptive-execution-en` | `#论证-41-为什么需要自适应执行引擎` |
| `Flink\02-core\adaptive-execution-engine-v2.md` | 46 | 论证 4.2: 数据倾斜自动处理策略 | `Flink\02-core\adaptive-execution-en` | `#论证-42-数据倾斜自动处理策略` |
| `Flink\02-core\adaptive-execution-engine-v2.md` | 47 | 论证 4.3: 资源自适应分配算法 | `Flink\02-core\adaptive-execution-en` | `#论证-43-资源自适应分配算法` |
| `Flink\02-core\adaptive-execution-engine-v2.md` | 48 | 反例 4.1: 自适应调整过度振荡 | `Flink\02-core\adaptive-execution-en` | `#反例-41-自适应调整过度振荡` |
| `Flink\02-core\adaptive-execution-engine-v2.md` | 49 | 5. 形式证明 / 工程论证 (Proof / E | `Flink\02-core\adaptive-execution-en` | `#5-形式证明--工程论证-proof--engineering-argument` |
| `Flink\02-core\adaptive-execution-engine-v2.md` | 53 | 示例 6.1: 配置参数详解 | `Flink\02-core\adaptive-execution-en` | `#示例-61-配置参数详解` |
| `Flink\02-core\adaptive-execution-engine-v2.md` | 54 | 示例 6.2: 性能提升数据实测 | `Flink\02-core\adaptive-execution-en` | `#示例-62-性能提升数据实测` |
| `Flink\02-core\adaptive-execution-engine-v2.md` | 55 | 示例 6.3: 最佳实践配置 | `Flink\02-core\adaptive-execution-en` | `#示例-63-最佳实践配置` |
| `Flink\02-core\adaptive-execution-engine-v2.md` | 56 | 示例 6.4: 故障排查指南 | `Flink\02-core\adaptive-execution-en` | `#示例-64-故障排查指南` |
| `Flink\02-core\async-execution-model.md` | 9 | Flink 2.0 异步执行模型与 AEC (As | `Flink\02-core\async-execution-model` | `#flink-20-异步执行模型与-aec-asynchronous-execution-controller` |
| `Flink\02-core\async-execution-model.md` | 25 | 论证 4.1: 为什么异步执行不破坏 Flink  | `Flink\02-core\async-execution-model` | `#论证-41-为什么异步执行不破坏-flink-1x-语义` |
| `Flink\02-core\async-execution-model.md` | 26 | 论证 4.2: AEC 如何保持按键处理顺序？ | `Flink\02-core\async-execution-model` | `#论证-42-aec-如何保持按键处理顺序` |
| `Flink\02-core\async-execution-model.md` | 27 | 论证 4.3: 异步执行与 Disaggregat | `Flink\02-core\async-execution-model` | `#论证-43-异步执行与-disaggregated-state-的协同` |
| `Flink\02-core\async-execution-model.md` | 28 | 反例 4.1: 不恰当使用异步 API 的陷阱 | `Flink\02-core\async-execution-model` | `#反例-41-不恰当使用异步-api-的陷阱` |
| `Flink\02-core\async-execution-model.md` | 33 | 示例 6.1: 异步状态访问的基本模式 | `Flink\02-core\async-execution-model` | `#示例-61-异步状态访问的基本模式` |
| `Flink\02-core\async-execution-model.md` | 34 | 示例 6.2: 批量异步状态操作 | `Flink\02-core\async-execution-model` | `#示例-62-批量异步状态操作` |
| `Flink\02-core\async-execution-model.md` | 35 | 示例 6.3: 异步执行错误处理模式 | `Flink\02-core\async-execution-model` | `#示例-63-异步执行错误处理模式` |
| `Flink\02-core\async-execution-model.md` | 36 | 示例 6.4: DataStream 启用异步状态 | `Flink\02-core\async-execution-model` | `#示例-64-datastream-启用异步状态-enableasyncstate` |
| `Flink\02-core\async-execution-model.md` | 37 | 示例 6.5: 与同步模式的性能对比实测 | `Flink\02-core\async-execution-model` | `#示例-65-与同步模式的性能对比实测` |
| `Flink\02-core\backpressure-and-flow-control.md` | 26 | 关系 1: Flink CBFC `⊃` TCP  | `Flink\02-core\backpressure-and-flow` | `#关系-1-flink-cbfc--tcp-flow-control` |
| `Flink\02-core\backpressure-and-flow-control.md` | 27 | 关系 2: 本地背压 `→` 端到端背压 | `Flink\02-core\backpressure-and-flow` | `#关系-2-本地背压--端到端背压` |
| `Flink\02-core\backpressure-and-flow-control.md` | 28 | 关系 3: Backpressure `↔` Ch | `Flink\02-core\backpressure-and-flow` | `#关系-3-backpressure--checkpoint-可靠性` |
| `Flink\02-core\backpressure-and-flow-control.md` | 30 | 4.1 为什么 Flink 1.5 必须用 CBF | `Flink\02-core\backpressure-and-flow` | `#41-为什么-flink-15-必须用-cbfc-取代-tcp-流控` |
| `Flink\02-core\backpressure-and-flow-control.md` | 34 | 5. 形式证明 / 工程论证 (Proof / E | `Flink\02-core\backpressure-and-flow` | `#5-形式证明--工程论证-proof--engineering-argument` |
| `Flink\02-core\backpressure-and-flow-control.md` | 35 | 定理 5.1 (CBFC 安全性 / Safety | `Flink\02-core\backpressure-and-flow` | `#定理-51-cbfc-安全性--safety` |
| `Flink\02-core\backpressure-and-flow-control.md` | 36 | 定理 5.2 (反压传播有限步收敛) | `Flink\02-core\backpressure-and-flow` | `#定理-52-反压传播有限步收敛` |
| `Flink\02-core\backpressure-and-flow-control.md` | 37 | 工程论证 5.3 (Buffer Debloati | `Flink\02-core\backpressure-and-flow` | `#工程论证-53-buffer-debloating--unaligned-checkpoint-联合选型` |
| `Flink\02-core\backpressure-and-flow-control.md` | 39 | 示例 6.1: 正常 Credit-based 背 | `Flink\02-core\backpressure-and-flow` | `#示例-61-正常-credit-based-背压传播` |
| `Flink\02-core\backpressure-and-flow-control.md` | 40 | 反例 6.2: 高并行度落差导致 OOM | `Flink\02-core\backpressure-and-flow` | `#反例-62-高并行度落差导致-oom` |
| `Flink\02-core\backpressure-and-flow-control.md` | 41 | 示例 6.3: Buffer Debloating | `Flink\02-core\backpressure-and-flow` | `#示例-63-buffer-debloating-调参配置` |
| `Flink\02-core\backpressure-and-flow-control.md` | 42 | 反例 6.4: Kafka Source 背压盲区 | `Flink\02-core\backpressure-and-flow` | `#反例-64-kafka-source-背压盲区` |
| `Flink\02-core\backpressure-and-flow-control.md` | 44 | 图 7.1: Credit-based 背压在 F | `Flink\02-core\backpressure-and-flow` | `#图-71-credit-based-背压在-flink-流水线中的传播` |
| `Flink\02-core\backpressure-and-flow-control.md` | 45 | 图 7.2: 控制-执行-数据层关联图 | `Flink\02-core\backpressure-and-flow` | `#图-72-控制-执行-数据层关联图` |
| `Flink\02-core\backpressure-and-flow-control.md` | 46 | 图 7.3: 背压诊断与调优决策树 | `Flink\02-core\backpressure-and-flow` | `#图-73-背压诊断与调优决策树` |
| `Flink\02-core\checkpoint-mechanism-deep-dive.md` | 9 | Flink Checkpoint 机制深度剖析 ( | `Flink\02-core\checkpoint-mechanism-` | `#flink-checkpoint-机制深度剖析-checkpoint-mechanism-deep-dive` |
| `Flink\02-core\checkpoint-mechanism-deep-dive.md` | 10 | 目录 {#目录} | `Flink\02-core\checkpoint-mechanism-` | `#目录` |
| `Flink\02-core\checkpoint-mechanism-deep-dive.md` | 11 | 1. 概念定义 (Definitions) {#1 | `Flink\02-core\checkpoint-mechanism-` | `#1-概念定义-definitions` |
| `Flink\02-core\checkpoint-mechanism-deep-dive.md` | 12 | Def-F-02-01 (Checkpoint 核 | `Flink\02-core\checkpoint-mechanism-` | `#def-f-02-01-checkpoint-核心抽象` |
| `Flink\02-core\checkpoint-mechanism-deep-dive.md` | 13 | Def-F-02-02 (Checkpoint B | `Flink\02-core\checkpoint-mechanism-` | `#def-f-02-02-checkpoint-barrier` |
| `Flink\02-core\checkpoint-mechanism-deep-dive.md` | 14 | Def-F-02-03 (Aligned Chec | `Flink\02-core\checkpoint-mechanism-` | `#def-f-02-03-aligned-checkpoint` |
| `Flink\02-core\checkpoint-mechanism-deep-dive.md` | 15 | Def-F-02-04 (Unaligned Ch | `Flink\02-core\checkpoint-mechanism-` | `#def-f-02-04-unaligned-checkpoint` |
| `Flink\02-core\checkpoint-mechanism-deep-dive.md` | 16 | Def-F-02-05 (Incremental  | `Flink\02-core\checkpoint-mechanism-` | `#def-f-02-05-incremental-checkpoint` |
| `Flink\02-core\checkpoint-mechanism-deep-dive.md` | 17 | Def-F-02-06 (State Backen | `Flink\02-core\checkpoint-mechanism-` | `#def-f-02-06-state-backend` |
| `Flink\02-core\checkpoint-mechanism-deep-dive.md` | 18 | Def-F-02-07 (Checkpoint 协 | `Flink\02-core\checkpoint-mechanism-` | `#def-f-02-07-checkpoint-协调器` |
| `Flink\02-core\checkpoint-mechanism-deep-dive.md` | 19 | Def-F-02-08 (Changelog St | `Flink\02-core\checkpoint-mechanism-` | `#def-f-02-08-changelog-state-backend` |
| `Flink\02-core\checkpoint-mechanism-deep-dive.md` | 20 | 2. 属性推导 (Properties) {#2- | `Flink\02-core\checkpoint-mechanism-` | `#2-属性推导-properties` |
| `Flink\02-core\checkpoint-mechanism-deep-dive.md` | 21 | Lemma-F-02-01 (Barrier 对齐 | `Flink\02-core\checkpoint-mechanism-` | `#lemma-f-02-01-barrier-对齐保证状态一致性` |
| `Flink\02-core\checkpoint-mechanism-deep-dive.md` | 22 | Lemma-F-02-02 (异步 Checkpo | `Flink\02-core\checkpoint-mechanism-` | `#lemma-f-02-02-异步-checkpoint-的低延迟特性` |
| `Flink\02-core\checkpoint-mechanism-deep-dive.md` | 23 | Lemma-F-02-03 (增量 Checkpo | `Flink\02-core\checkpoint-mechanism-` | `#lemma-f-02-03-增量-checkpoint-的存储优化` |
| `Flink\02-core\checkpoint-mechanism-deep-dive.md` | 24 | Prop-F-02-01 (Checkpoint  | `Flink\02-core\checkpoint-mechanism-` | `#prop-f-02-01-checkpoint-类型选择的权衡空间` |
| `Flink\02-core\checkpoint-mechanism-deep-dive.md` | 25 | 3. 关系建立 (Relations) {#3-关 | `Flink\02-core\checkpoint-mechanism-` | `#3-关系建立-relations` |
| `Flink\02-core\checkpoint-mechanism-deep-dive.md` | 26 | 关系 1: Flink Checkpoint ↔  | `Flink\02-core\checkpoint-mechanism-` | `#关系-1-flink-checkpoint--chandy-lamport-分布式快照` |
| `Flink\02-core\checkpoint-mechanism-deep-dive.md` | 27 | 关系 2: Checkpoint 机制 ⟹ Exa | `Flink\02-core\checkpoint-mechanism-` | `#关系-2-checkpoint-机制--exactly-once-语义` |
| `Flink\02-core\checkpoint-mechanism-deep-dive.md` | 28 | 关系 3: State Backend 类型 ↔  | `Flink\02-core\checkpoint-mechanism-` | `#关系-3-state-backend-类型--应用场景` |

## 📁 问题文件Top 30

以下文件包含最多的断裂引用：

| 排名 | 文件路径 | 断裂引用数 |
|------|----------|------------|
| 1 | `Knowledge\09-anti-patterns\streaming-anti-patterns.md` | 61 |
| 2 | `Knowledge\01-concept-atlas\data-streaming-landscape-2026-complete.md` | 59 |
| 3 | `Knowledge\04-technology-selection\engine-selection-guide.md` | 55 |
| 4 | `Flink\02-core\checkpoint-mechanism-deep-dive.md` | 54 |
| 5 | `Struct\03-relationships\03.03-expressiveness-hierarchy-supplement.md` | 35 |
| 6 | `Struct\01-foundation\01.02-process-calculus-primer.md` | 32 |
| 7 | `Knowledge\06-frontier\streaming-databases.md` | 29 |
| 8 | `Struct\00-STRUCT-DERIVATION-CHAIN.md` | 27 |
| 9 | `Struct\Proof-Chains-Flink-Complete.md` | 22 |
| 10 | `Struct\06-frontier\06.05-ai-agent-streaming-formalization.md` | 21 |
| 11 | `Struct\06-frontier\research-trends-analysis-2024-2026.md` | 21 |
| 12 | `Struct\01-foundation\01.03-actor-model-formalization.md` | 20 |
| 13 | `Struct\02-properties\02.04-liveness-and-safety.md` | 20 |
| 14 | `Struct\04-proofs\04.07-deadlock-freedom-choreographic.md` | 20 |
| 15 | `Struct\Proof-Chains-Actor-Model.md` | 20 |
| 16 | `Struct\Struct-to-Knowledge-Mapping.md` | 20 |
| 17 | `Flink\08-roadmap\08.01-flink-24\flink-version-evolution-complete-guide.md` | 19 |
| 18 | `Knowledge\01-concept-atlas\streaming-models-mindmap.md` | 19 |
| 19 | `Knowledge\01-concept-atlas\concurrency-paradigms-matrix.md` | 18 |
| 20 | `Knowledge\04-technology-selection\streaming-database-guide.md` | 18 |
| 21 | `Struct\06-frontier\06.03-ai-agent-session-types.md` | 18 |
| 22 | `Struct\04-proofs\04.04-watermark-algebra-formal-proof.md` | 17 |
| 23 | `Struct\Key-Theorem-Proof-Chains.md` | 17 |
| 24 | `Flink\05-ecosystem\05.01-connectors\flink-24-connectors-guide.md` | 16 |
| 25 | `Struct\03-relationships\03.03-expressiveness-hierarchy.md` | 16 |
| 26 | `Struct\05-comparative-analysis\05.02-expressiveness-vs-decidability.md` | 16 |
| 27 | `Struct\Model-Selection-Decision-Tree.md` | 16 |
| 28 | `Struct\Proof-Chains-Proofs-Remaining.md` | 16 |
| 29 | `Flink\02-core\backpressure-and-flow-control.md` | 15 |
| 30 | `Struct\05-comparative-analysis\05.03-encoding-completeness-analysis.md` | 15 |

## 🔧 修复建议

### 文件不存在错误
1. 检查链接路径是否正确
2. 确认目标文件是否被移动或重命名
3. 使用相对路径时，确保路径相对于当前文件位置正确

### 锚点不存在错误
1. 检查锚点标识符是否拼写正确
2. 确认目标标题是否包含显式锚点定义 `{#anchor}`
3. 如果是隐式锚点，确保与GitHub生成的锚点格式一致（小写，空格替换为连字符）
4. 标题中的数字前缀（如 "1. "）会被GitHub处理为锚点的一部分

## 📋 验证规则说明

- **代码块过滤**: 代码块（```...```）中的内容被忽略
- **泛型语法过滤**: 代码中的泛型参数如 `[T]`、`[String]` 等被忽略
- **外部链接**: `http://` 和 `https://` 开头的链接被忽略
- **锚点匹配**: 支持多种锚点格式变体（带/不带数字前缀）
- **大小写不敏感**: 锚点检查不区分大小写
