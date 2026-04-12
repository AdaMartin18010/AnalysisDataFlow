> **状态**: 🔮 前瞻内容 | **风险等级**: 高 | **最后更新**: 2026-04
> 
> 此文档描述的内容处于早期规划阶段，可能与最终实现不符。请以 Apache Flink 官方发布为准。
# AnalysisDataFlow — Agent 工作上下文规范

> **版本**: v1.2 | **生效日期**: 2026-04-11 | **状态**: Production | **项目状态**: 100%完成 ✅ (v3.9 FINAL)

## 1. 项目定位

本项目是对**流计算的理论模型、层次结构、工程实践、业务建模**的全面梳理与体系构建。
目标是为学术研究、工业工程和技术选型提供**严格、完整、可导航**的知识库。

**当前状态**: 项目已达到100%完成状态，所有规划内容已全部交付。

## 2. 目录结构规范（三大输出目录）

所有新内容必须输出到以下三个目录之一，原始材料目录 `AcotorCSPWorkflow/` 仅作为迁移来源，最终将被删除。

```
.
├── Struct/               # 形式理论、分析论证、严格证明
├── Knowledge/            # 知识结构、设计模式、商业应用
├── Flink/                # Flink 专项：架构、机制、对比、路线图
└── AcotorCSPWorkflow/    # 原始材料（只读，待迁移完成后删除）
```

## 3. 文档编号与命名规范

### 3.1 文件命名

- 全部小写，使用连字符 `-` 分隔
- 前缀必须体现所属层级和序号
- 格式: `{层号}.{序号}-{主题关键词}.md`

### 3.2 定理/引理编号体系（Struct/ 强制使用）

采用全局统一编号：`{类型}-{阶段}-{文档序号}-{顺序号}`

| 类型 | 缩写 | 示例 |
|------|------|------|
| 定理 | Thm | `Thm-S-01-01` = Struct Stage, 01 文档, 第 1 个定理 |
| 引理 | Lemma | `Lemma-S-01-02` |
| 定义 | Def | `Def-S-01-01` |
| 命题 | Prop | `Prop-S-03-01` |
| 推论 | Cor | `Cor-S-02-01` |

Knowledge/ 和 Flink/ 文档使用内部编号（如 `Def-K-01-01`、`Thm-F-04-01`），不强制全局唯一但建议保持统一风格。

## 4. 文档六段式模板（强制结构）

每篇核心 Markdown 文档必须包含以下结构：

```markdown
   # 标题

   > 所属阶段: Struct/ Knowledge/ Flink/ | 前置依赖: [文档链接] | 形式化等级: L1-L6

   ## 1. 概念定义 (Definitions)
   严格的形式化定义 + 直观解释。必须包含至少一个 `Def-*` 编号。

   ## 2. 属性推导 (Properties)
   从定义直接推导的引理与性质。必须包含至少一个 `Lemma-*` 或 `Prop-*` 编号。

   ## 3. 关系建立 (Relations)
   与其他概念/模型/系统的关联、映射、编码关系。

   ## 4. 论证过程 (Argumentation)
   辅助定理、反例分析、边界讨论、构造性说明。

   ## 5. 形式证明 / 工程论证 (Proof / Engineering Argument)
   主要定理的完整证明，或工程选型的严谨论证。

   ## 6. 实例验证 (Examples)
   简化实例、代码片段、配置示例、真实案例。

   ## 7. 可视化 (Visualizations)
   至少一个 Mermaid 图（思维导图 / 层次图 / 执行树 / 对比矩阵 / 决策树 / 场景树）。

   ## 8. 引用参考 (References)
   使用 `[^n]` 上标格式，在文档末尾集中列出引用。
```

## 5. 引用格式规范

引用必须在文档末尾以列表形式集中呈现：

```markdown
[^1]: Apache Flink Documentation, "Checkpointing", 2025. https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/checkpointing/
[^2]: T. Akidau et al., "The Dataflow Model", PVLDB, 8(12), 2015.
[^3]: L. Lamport, "Time, Clocks, and the Ordering of Events in a Distributed System", CACM, 21(7), 1978.
```

优先引用的权威来源：

- **课程**: MIT 6.824 / 6.826, CMU 15-712, Stanford CS240, Berkeley CS162
- **论文**: VLDB, SIGMOD, OSDI, SOSP, CACM, POPL, PLDI
- **官方文档**: Apache Flink, Go Spec, Scala 3 Spec, Akka/Pekko Docs
- **经典书籍**: Kleppmann《DDIA》, Akidau《Streaming Systems》

## 6. Mermaid 可视化规范

所有 Mermaid 图必须：

1. 使用 ````mermaid` 代码块包裹
2. 在图前添加简短文字说明
3. 选择恰当的图表类型：
   - `graph TB/TD` — 层次结构、映射关系
   - `flowchart TD` — 决策树、流程图
   - `gantt` — 路线图、时间线
   - `stateDiagram-v2` — 状态转移、执行树
   - `classDiagram` — 类型/模型结构

## 7. 工作推进规范

### 7.1 并发推进原则

- 三大目录可以**并行推进**
- 每个目录内部按**依赖顺序**串行，无依赖的文档可并行
- 优先完成 `Struct/` 核心理论，再向 `Knowledge/` 和 `Flink/` 辐射

### 7.2 进度跟踪

- 使用 `PROJECT-TRACKING.md` 作为唯一进度看板
- 每完成一篇文档，更新一次 PROJECT-TRACKING.md
- 进度百分比 = 已完成任务数 / 总任务数

### 7.3 质量门禁

- 每篇文档必须经过六段式检查
- 引用的外部链接必须可验证（优先使用 DOI 或稳定 URL）
- Mermaid 图语法必须通过基本校验
- **新增** 可视化内容需遵循 [Mermaid风格指南](./docs/mermaid-style-guide.md)

## 8. 前置知识假设

处理本项目时，Agent 需要掌握以下领域知识：

- 进程演算（CCS, CSP, π-calculus）
- Actor 模型与并发语义
- Dataflow 模型与流计算系统
- 类型理论（FG, FGG, DOT, Session Types）
- 分布式一致性模型与容错机制
- Flink 架构（Checkpoint, Watermark, Exactly-Once, Backpressure）
- 形式化验证方法（TLA+, Iris, Model Checking）

## 9. 禁止事项

- **禁止** 修改 `AcotorCSPWorkflow/` 中的任何文件（只读源库）
- **禁止** 在根目录创建与三大输出目录无关的新文件
- **禁止** 跳过六段式模板中的核心章节
- **禁止** 使用不可靠来源作为技术论据

## 10. 项目状态看板

```
总体进度: [████████████████████] 100% (项目完成 ✅ v3.9 FINAL)
Struct/:    [████████████████████] 100% (74文档, 380定理, 835定义)
Knowledge/: [████████████████████] 100% (226文档, 77定理, 228定义)
Flink/:     [████████████████████] 100% (382文档, 693定理, 1889定义)
en/:        [████████████████████] 100% (4文档)
定理注册表: v3.9 | 总计: 10,745形式化元素 (1,940定理+4,657定义+1,610引理+1,224命题+121推论)

最新扩展: **Flink源码深度分析** (12篇, ~590KB) | Checkpoint/StateBackend/Network Stack源码
          | **Knowledge核心概念补全** (5篇) | 时间语义/窗口/状态/一致性模型
          | **设计模式扩展** (3篇) | Stream Join/双流处理/Backpressure
          | **Tutorials增强** (4篇) | Flink SQL/Connectors/K8s/PyFlink
          | **根级索引完善** (4个README) | API/Runtime/Ecosystem/AI-ML导航
          | **英文核心文档** (4篇) | README/QuickStart/Architecture/Glossary
          | Flink Agents (FLIP-531) | 实时图流处理TGN | 多模态流处理
          | **交叉引用清零 (730→0)** | **形式化验证完成 (Coq+TLA+)**

完成里程碑:
- ✅ 2026-04-04: v3.3 路线图发布, Flink 2.4/2.5/3.0 100子任务完成
- ✅ 2026-04-06: v3.4 关系梳理完成, 500+关系边
- ✅ 2026-04-08: v3.5 AI Agent深化, 24个形式化元素
- ✅ 2026-04-11: v3.6 100%完成, 交叉引用清零+形式化验证
- ✅ 2026-04-11: v3.7 Flink源码分析完成, 12篇深度文档
- ✅ 2026-04-11: v3.8 知识库全面补全, 16篇新文档+195形式化元素
- ✅ 2026-04-11: v3.9 FINAL, 英文核心文档完成, 项目100%交付

关键完成报告:
- [100-PERCENT-COMPLETION-FINAL-REPORT.md](./100-PERCENT-COMPLETION-FINAL-REPORT.md)
- [FLINK-24-25-30-COMPLETION-REPORT.md](./archive/completion-reports/FLINK-24-25-30-COMPLETION-REPORT.md)
- [cross-ref-fix-report.md](./cross-ref-fix-report.md)
- [COQ-COMPILATION-REPORT.md](./reconstruction/phase4-verification/COQ-COMPILATION-REPORT.md)
- [TLA-MODEL-CHECK-REPORT.md](./reconstruction/phase4-verification/TLA-MODEL-CHECK-REPORT.md)
```

---

*本文件由 Agent 在执行任务时自动读取并遵守。更新本文件时务必同步更新看板百分比。*
