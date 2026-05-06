# AnalysisDataFlow — v8.0 短期冲刺执行计划（已确认版）

> **确认日期**: 2026-05-06 | **执行范围**: 仅短期冲刺（S1-S4）+ 形式化装饰风险评审 | **排除项**: 形式化债务透明度标注、英文本地化重构
> **执行模式**: myself + Agent 并行 | **目标交付**: ~30篇新文档 + ~10篇更新 | **周期**: 2026-05 至 2026-07

---

## 一、确认决策摘要

| 决策项 | 用户选择 | 说明 |
|--------|----------|------|
| 优先级范围 | **仅短期冲刺** | 聚焦S1-S4，中期/长期延后 |
| 形式化债务透明度 | **不做** | 42处Lean sorry维持现状，不标注分类 |
| 英文本地化重构 | **不做** | 303篇英文翻译维持现状 |
| 形式化装饰风险 | **重点治理** | 引入"形式化必要性评审"机制 |
| Flink-centrism修正 | **A: 增加非Flink专题** | 通过S4新兴引擎专题平衡 |
| 执行模式 | **A: myself+Agent并行** | 参考v7.1成功经验 |

---

## 二、新增专项：形式化装饰风险治理（SPRINT-X）

### 2.1 风险定义

**形式化装饰风险（Formalization Ornament Risk）**：指将工程常识或直观明显的实现细节，以严格的形式化语言（`Def-*`、`Thm-*`、`Lemma-*`）重新表述，导致：

- 阅读门槛不必要地升高
- 形式化元素数量虚高但知识密度下降
- 读者产生"为编号而编号"的负面印象
- 稀释真正高价值形式化内容（如Checkpoint正确性证明、类型安全定理）的注意力

### 2.2 评审标准（FORMAL-NECESSITY-CRITERIA）

对现有7,760+形式化元素，引入四级必要性评级：

| 评级 | 标准 | 示例 | 处理策略 |
|------|------|------|----------|
| **F0-核心** | 非形式化无法精确表述；是后续定理的依赖基础 | `Def-S-01-01` USTM统一元模型、`Thm-S-04-01` Checkpoint正确性 | 保留并强化 |
| **F1-有益** | 工程概念经形式化后揭示隐藏假设或边界条件 | `Def-K-02-01` 窗口聚合的语义边界、`Prop-F-02-01` Watermark单调性 | 保留并优化解释 |
| **F2-冗余** | 内容是工程常识的直接翻译，形式化未增加新洞察 | "Map算子对每条输入产生一条输出"的形式化定义 | **降级为正文描述，移除编号** |
| **F3-装饰** | 明显为凑数而设；与上下文无关；过度抽象 | "Docker容器是一个进程"的形式化定义（属于OS领域而非流计算） | **删除或归档** |

### 2.3 执行动作

**SPRINT-X-1**: 抽样审计

- 范围：Struct/ 01-foundation + Knowledge/ 02-design-patterns + Flink/ 02-core 各抽20%文档
- 方法：逐条审阅 `Def-*` / `Thm-*`，按F0-F3评级
- 产出：审计报告 + 候选降级/删除清单

**SPRINT-X-2**: 批量清理

- 对F3评级元素：直接删除编号，内容并入正文或删除
- 对F2评级元素：移除编号，改写为自然语言描述
- 对F0-F1评级元素：确保每个都有"直观解释"段落

**SPRINT-X-3**: 防御机制

- 在 `AGENTS.md` 中增加 `FORMAL-NECESSITY-GUIDELINE` 章节
- 新增质量门禁：`.scripts/formal-necessity-checker.py` — 检测疑似F2/F3的新增形式化元素
- 规则：新增`Def-*`必须伴随"非形式化无法精确表述"的论证段落

---

## 三、短期冲刺详细执行计划

### 批次 S1：Kafka 4.0 架构革命专题（🔴 P0， myself + Agent并行）

| 任务ID | 交付物 | 路径 | 规模 | 负责人 | 依赖 |
|--------|--------|------|------|--------|------|
| S1-1 | Kafka 4.0 架构革命深度解析 | `Knowledge/06-frontier/kafka-4.0-architecture-revolution.md` | ~25KB | Agent | 无 |
| S1-2 | KIP-848 新消费者组协议详解 | `Knowledge/06-frontier/kafka-kip-848-consumer-protocol.md` | ~20KB | Agent | 无 |
| S1-3 | KIP-932 Queues for Kafka 分析 | `Knowledge/06-frontier/kafka-kip-932-queues.md` | ~15KB | Agent | 无 |
| S1-4 | Kafka 4.0 ZK→KRaft 迁移完整指南 | `Knowledge/07-best-practices/kafka-4.0-migration-guide.md` | ~20KB | Agent | S1-1 |
| S1-5 | 更新 Flink/Kafka 集成文档（Java版本、协议配置） | `Flink/05-ecosystem/05.01-connectors/*` 等 5-8篇 | 增量更新 | myself | S1-1完成 |

**关键内容要求**：

- 明确宣告"ZooKeeper已死"的历史意义
- 新消费者协议的性能对比数据（rebalance时间、延迟影响）
- Queues语义与传统Kafka分区模型的差异
- Java 17迁移对生产环境的影响

---

### 批次 S2：Streaming Agents × AI 融合专题（🔴 P0， myself主导+Agent辅助）

| 任务ID | 交付物 | 路径 | 规模 | 负责人 | 依赖 |
|--------|--------|------|------|--------|------|
| S2-1 | Confluent Streaming Agents 深度解析 | `Knowledge/06-frontier/confluent-streaming-agents-deep-dive.md` | ~35KB | myself | 无 |
| S2-2 | Agentic Data Analytics 前沿 | `Knowledge/06-frontier/agentic-data-analytics-streaming.md` | ~25KB | Agent | 无 |
| S2-3 | 流式Agent架构模式 | `Knowledge/02-design-patterns/streaming-agents-architecture-patterns.md` | ~20KB | Agent | S2-1 |
| S2-4 | LLM Serving for Agentic Workflows | `Knowledge/06-frontier/llm-serving-for-agentic-workflows.md` | ~15KB | Agent | 无 |
| S2-5 | 更新 AI Agent 流式架构文档 | `Knowledge/06-frontier/ai-agent-streaming-architecture.md` | 增量更新 | myself | S2-1完成 |

**关键内容要求**：

- Confluent Streaming Agents = Flink SQL + Model Inference + Real-time Embeddings + MCP 的原生集成
- 与传统"Flink job调用外部LLM API"架构的对比（延迟、成本、可靠性）
- Agentic Data Analytics的学术前沿（arXiv 2026-04）
- Helium framework的workflow-aware serving原理

---

### 批次 S3：Streaming-First Lakehouse 专题（🔴 P0，Agent并行）

| 任务ID | 交付物 | 路径 | 规模 | 负责人 | 依赖 |
|--------|--------|------|------|--------|------|
| S3-1 | Streaming-First Lakehouse 2026 总论 | `Knowledge/06-frontier/streaming-first-lakehouse-2026.md` | ~30KB | Agent | 无 |
| S3-2 | Apache Paimon LSM-tree 架构深度解析 | `Knowledge/06-frontier/apache-paimon-lsm-tree-architecture.md` | ~25KB | Agent | 无 |
| S3-3 | Redpanda Iceberg Topics 架构分析 | `Knowledge/06-frontier/redpanda-iceberg-topics-analysis.md` | ~15KB | Agent | 无 |
| S3-4 | Lakehouse Table Format 2026 决策矩阵 | `Knowledge/04-technology-selection/lakehouse-table-format-decision-matrix-2026.md` | ~20KB | Agent | S3-1,S3-2 |
| S3-5 | 更新 Lakehouse 集成文档（Tableflow、Snapshot Queries） | `Flink/05-ecosystem/05.02-lakehouse/*` 等 3-5篇 | 增量更新 | myself | S3-1完成 |

**关键内容要求**：

- "2026年是Streaming-first Lakehouse元年"的论证
- Paimon LSM-tree vs Iceberg树形元数据的架构差异
- Redpanda Iceberg Topics的"流即表"理念
- 四格式（Iceberg/Delta/Hudi/Paimon）2026年定位分化

---

### 批次 S4：新兴引擎与竞争格局（🟡 P1，Agent并行）

| 任务ID | 交付物 | 路径 | 规模 | 负责人 | 依赖 |
|--------|--------|------|------|--------|------|
| S4-1 | Pathway 统一批流引擎深度解析 | `Knowledge/06-frontier/pathway-python-rust-streaming-engine.md` | ~20KB | Agent | 无 |
| S4-2 | Bytewax Python-native 流处理 | `Knowledge/06-frontier/bytewax-python-native-streaming.md` | ~15KB | Agent | 无 |
| S4-3 | 流处理引擎全景图 2026 | `Knowledge/01-concept-atlas/stream-processing-engine-landscape-2026.md` | ~25KB | myself | S4-1,S4-2 |
| S4-4 | Confluent Snapshot Queries 分析 | `Knowledge/06-frontier/confluent-snapshot-queries-analysis.md` | ~15KB | Agent | 无 |

**关键内容要求**：

- Pathway的"统一batch/streaming引擎"架构（Python API + Rust runtime）
- Bytewax的Timely Dataflow Rust核心 + Python生态优势（25x内存降低）
- 2026年引擎选型决策树（Flink vs RisingWave vs Pathway vs Bytewax vs Spark）
- Snapshot Queries的batch+stream统一SQL接口（50-100x历史查询加速）

---

### 批次 SPRINT-X：形式化装饰风险治理（ myself主导）

| 任务ID | 交付物 | 路径/范围 | 规模 | 负责人 | 依赖 |
|--------|--------|----------|------|--------|------|
| X-1 | 形式化元素抽样审计报告 | `.improvement-tracking/formal-necessity-audit-report.md` | ~10KB | myself | 无 |
| X-2 | F2/F3元素批量清理（第一批） | Struct/01-foundation + Knowledge/02-design-patterns | 代码修改 | myself | X-1 |
| X-3 | 形式化必要性指南（AGENTS.md更新） | `AGENTS.md` 新增章节 | ~2KB | myself | X-1 |
| X-4 | 形式化必要性检查脚本 | `.scripts/formal-necessity-checker.py` | ~3KB | myself | X-3 |

---

## 四、执行时序与并发计划

```
Week 1-2 (2026-05-06 至 05-19):
  ├── S1-1/1-2/1-3/1-4 (Agent ×4 并行)
  ├── S2-2/2-4 (Agent ×2 并行)
  ├── S3-1/3-2/3-3 (Agent ×3 并行)
  ├── S4-1/4-2/4-4 (Agent ×3 并行)
  └── X-1 (myself: 形式化审计)

Week 3-4 (2026-05-20 至 06-02):
  ├── S1-5 (myself: 更新现有文档)
  ├── S2-1 (myself: Confluent Streaming Agents深度解析)
  ├── S2-3 (Agent, 依赖S2-1)
  ├── S3-4 (Agent, 依赖S3-1/3-2)
  ├── S2-5 (myself: 更新AI Agent文档)
  └── X-2/X-3 (myself: 清理+指南)

Week 5-6 (2026-06-03 至 06-16):
  ├── S4-3 (myself: 引擎全景图)
  ├── S3-5 (myself: 更新Lakehouse文档)
  ├── X-4 (myself: 检查脚本)
  └── 质量门禁：全量交叉引用 + 六段式 + Mermaid

Week 7-8 (2026-06-17 至 06-30):
  ├── 全量审阅与修复
  ├── PROJECT-TRACKING.md 更新
  └── v8.0-alpha 发布
```

**并发峰值**: 12个Agent并行（Week 1-2） + myself持续处理

---

## 五、质量门禁（保持不变）

每篇新增/更新文档必须通过：

- [ ] 六段式模板合规检查
- [ ] 交叉引用0 errors
- [ ] Mermaid语法0 errors
- [ ] 形式化元素编号不冲突（THEOREM-REGISTRY同步）
- [ ] **新增**：形式化必要性检查（X-4脚本运行通过）
- [ ] 外部引用可验证（优先DOI/稳定URL）

---

## 六、排除项声明

以下批次**明确排除**在本次v8.0短期冲刺之外：

| 排除批次 | 排除原因 | 未来处理 |
|----------|----------|----------|
| S5（形式化债务透明度） | 用户确认不做 | 维持现状，不标注sorry分类 |
| S6-2（英文本地化重构） | 用户确认不做 | 303篇英文翻译维持现状 |
| S6-1（英文核心原创） | 用户确认不做 | 未来版本再说 |
| M1-M4（中期建设） | 范围限制为短期冲刺 | v8.1或后续版本 |
| L1-L4（长期愿景） | 范围限制为短期冲刺 | v9.0规划 |

---

*本计划已根据用户确认决策精简。如无进一步修改，将立即按此时序启动交付。*
