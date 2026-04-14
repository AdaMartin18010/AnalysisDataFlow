# AnalysisDataFlow 翻译策略文档

> **版本**: v1.1.0 | **生效日期**: 2026-04-15 | **状态**: Active
>
> **适用范围**: 所有国际化（i18n）内容产出与审校流程

---

## 1. 策略背景与目标

### 1.1 问题背景

AnalysisDataFlow 项目的内容体量庞大且深度差异显著：

- **中文源文档**: 760+ 篇（Struct/ 93 篇、Knowledge/ 262 篇、Flink/ 408+ 篇）
- **英文覆盖率**: 约 9.5%（以数量计），但核心形式化证明文档覆盖率极低
- **AI 翻译风险**: 当前 LLM 在数学证明、形式化语义、双模拟等价等严密推理任务上存在系统性缺陷（研究显示完整证明生成准确率可跌至 ~50%）

### 1.2 核心目标

1. **消除内容漂移**: 同一主题的多语言版本必须保持语义等价
2. **防止推理幻觉**: 形式化证明类内容禁止纯 AI 翻译
3. **提升翻译效率**: 对低风险内容充分利用 AI 辅助，对高风险内容投入专家资源
4. **建立可持续流程**: 翻译工作与中文源文档更新同步，避免债务累积

---

## 2. 内容风险分层模型

所有待翻译内容按 **AI 翻译风险** 与 **人工审校必要性** 分为三层：

| 层级 | 代号 | 内容类型 | 翻译策略 | 审校强度 | 责任人 |
|------|------|----------|----------|----------|--------|
| **A** | `AI-DOMINANT` | 导航页、索引、生产清单、配置说明、案例研究、连接器指南 | AI 预翻译 + 轻量审校 | 低 | 技术写作者 / 社区贡献者 |
| **B** | `AI-ASSISTED` | 概念定义、属性推导、工程论证、设计模式、架构对比、最佳实践 | AI 生成初稿 + 专家逐句审校 | 中 | 领域技术专家 |
| **C** | `HUMAN-DOMINANT` | 形式化证明（`Struct/04-proofs/`）、定理完整证明、双模拟等价、类型安全证明、Checkpoint 正确性严格证明 | **禁止纯 AI 翻译** | 高 | 形式化方法背景专家 |

### 2.1 A 层内容详细说明

**定义**: 以信息传递为主、逻辑严密性要求相对较低的内容。

**示例**:

- `Flink/04-connectors/kafka-connector-guide.md`
- `Knowledge/07-best-practices/production-checklist.md`
- `en/00-INDEX.md`、`docs/i18n/en/_sidebar.md`
- 所有案例研究、部署配置示例

**流程**:

1. 使用 `auto-translate.py` 生成初稿
2. 运行 `quality-checker.py` 检查术语一致性和格式
3. 轻量人工审校：重点检查术语、代码示例、链接有效性
4. 标记 `translation_status: ai_translated_reviewed`

### 2.2 B 层内容详细说明

**定义**: 需要准确传达技术概念和工程逻辑，但不需要严格数学证明的内容。

**示例**:

- `Struct/01-foundation/unified-streaming-model.md`
- `Struct/02-properties/consistency-hierarchy.md`
- `Knowledge/02-design-patterns/stateful-streaming-patterns.md`
- `Flink/02-core/checkpoint-mechanism.md`（机制说明，非正确性证明）

**流程**:

1. 使用 `auto-translate.py` 生成初稿
2. 领域专家逐句审校，重点检查：
   - 概念定义是否失真
   - 逻辑推导链条是否完整
   - 技术细节是否与中文原文一致
3. 审校者需在文档末尾添加审校签名：

   ```markdown
   <!-- Reviewed by: [Name], [Date] -->
   ```

4. 标记 `translation_status: expert_reviewed`

### 2.3 C 层内容详细说明

**定义**: 包含数学证明、形式化语义、严格等价关系推导的内容。AI 在此类任务上极易产生"推理幻觉"（reasoning illusion），即生成看似合理但逻辑有漏洞的证明。

**示例**:

- `Struct/04-proofs/bisimulation-equivalence-proof.md`
- `Struct/04-proofs/type-safety-proof.md`
- `Struct/04-proofs/checkpoint-correctness-proof.md`
- 任何包含 `Thm-*` 完整证明链的文档

**流程**:

1. **禁止**使用 `auto-translate.py` 直接生成完整文档
2. 允许使用 AI 作为辅助工具：
   - 翻译非证明段落（如引言、符号说明）
   - 生成 LaTeX 公式格式
   - 提供英文术语建议
3. 核心证明必须由具备以下背景之一的人员撰写或深度改写：
   - 形式化方法、进程演算、类型理论研究经历
   - 熟悉 Coq/Lean/TLA+ 等证明辅助工具
4. 标记 `translation_status: formally_verified_human_translation`
5. 强烈建议附上中文原文作者的交叉验证

---

## 3. 术语管理与一致性

### 3.1 权威术语源

| 资源 | 路径 | 状态 |
|------|------|------|
| 核心术语库 | `i18n/terminology/core-terms.json` | 30 条（已校准） |
| Flink 术语库 | `i18n/terminology/flink-terms.json` | 30 条（已校准） |
| 验证规则 | `i18n/terminology/verification-rules.json` | 完整 |

### 3.2 术语使用规范

1. **强制匹配**: A/B 层文档必须通过 `quality-checker.py` 的术语一致性检查
2. **禁止变体**: 如 "背压" 的禁止变体为 "反压"、"反向压力"，翻译中必须使用 "Backpressure"
3. **保留原文**: Flink 专有名词（JobManager, TaskManager, DataStream API 等）保留英文

---

## 4. 质量门禁与 CI/CD

### 4.1 自动化检查

| 检查项 | 工具 | 触发条件 |
|--------|------|----------|
| 翻译进度统计 | `report-generator.py` | 每周日 `i18n-sync.yml` |
| 目录一致性 | 内嵌 Python | 每周日 `i18n-sync.yml` |
| 术语/格式检查 | `quality-checker.py` | PR 触发 `i18n-quality-gate.yml` |
| Frontmatter 检查 | 内嵌 Python | PR 触发 `i18n-quality-gate.yml` |

### 4.2 强制 Frontmatter 字段

所有新增或修改的翻译文档必须包含：

```yaml
---
title: "文档标题"
translation_status: "ai_translated_reviewed" # 或 expert_reviewed / formally_verified_human_translation
source_version: "vX.Y.Z"  # 对应中文源文档版本
last_sync: "2026-04-15"   # 最后同步日期
---
```

### 4.3 质量阈值

- **A 层**: 术语一致性 ≥ 95%，格式验证通过，无 broken link
- **B 层**: 术语一致性 ≥ 98%，必须经过人工审校签名
- **C 层**: 100% 人工主导，AI 仅允许辅助非证明段落

---

## 5. 多语言目录架构（统一后）

```
i18n/
├── en/                    # AI 翻译工作区（A/B 层草稿）
├── de/                    # 冻结维护（仅保留入口页）
├── fr/                    # 冻结维护（仅保留入口页）
├── ja/                    # 冻结维护（仅保留入口页）
├── zh/
│   └── README.md          # 源语言锚点
├── terminology/           # 术语库
├── translation-workflow/  # 工具链
│   ├── auto-translate.py
│   ├── quality-checker.py
│   ├── sync-tracker.py
│   └── report-generator.py
└── TRANSLATION-STRATEGY.md  # 本文件

docs/i18n/
├── en/                    # 文档站点源（最终用户可见）
│   ├── 00-OVERVIEW.md
│   ├── 00-INDEX.md
│   ├── 01-STRUCT-GUIDE.md
│   ├── ...
│   └── _sidebar.md
├── de/
├── fr/
├── ja/
└── zh/

en/                        # 根目录英文导航页（已统一为 redirect）
├── 00-INDEX.md            -> redirect to docs/i18n/en/00-INDEX.md
├── README.md              -> redirect to docs/i18n/en/README.md
└── ...
```

---

## 6. 持续更新与债务控制

### 6.1 更新触发条件

当以下情况发生时，必须在 **14 天内**同步对应英文文档：

1. 中文源文档的定理/定义/代码示例发生修改
2. 新增中文文档且被标记为 P0/P1 优先级
3. 术语库中的核心术语定义发生变更

### 6.2 债务控制原则

- **禁止**在英文目录统一完成前新建第三套英文内容
- **禁止**对 C 层内容使用纯 AI 翻译
- **禁止**合并未通过 `quality-checker.py` 的 A/B 层文档

---

## 7. 参考与依据

- Mathematical Proof as a Litmus Test: Revealing Failure Modes of Advanced Large Reasoning Models (2025)
- Natural Language Translation of Formal Proofs (ACL 2025)
- Benchmarking LLMs on Advanced Mathematical Reasoning (Berkeley EECS 2025)
- InfoSync: Information Synchronization across Multilingual Semi-structured Tables
- Frontiers in Computer Science: Practices, opportunities and challenges in the fusion of knowledge graphs and large language models (2025)

---

> **Last Updated**: 2026-04-15
>
> 本策略由 Agent 与用户共同确认生效。任何修改需经过双方讨论并更新本文件版本号。
