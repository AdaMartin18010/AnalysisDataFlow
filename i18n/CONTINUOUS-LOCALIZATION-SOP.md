# 持续本地化标准操作流程 (SOP)

> **版本**: 1.0.0 | **生效日期**: 2026-04-15 | **状态**: Active
>
> **关联文档**: [TRANSLATION-STRATEGY.md](./TRANSLATION-STRATEGY.md)

---

## 1. 目标

确保中文源文档的更新能在合理时间窗口内同步到英文及其他语言版本，防止多语言内容漂移成为不可维护的技术债务。

---

## 2. 触发条件

以下任一情况发生时，必须启动持续本地化流程：

| 触发条件 | 优先级 | 响应时限 |
|----------|--------|----------|
| 中文 P0/P1 文档发生实质性修改（>10% 内容变更） | P0 | 7 天内 |
| 中文文档的定理/定义/代码示例发生修改 | P0 | 7 天内 |
| 术语库核心术语定义发生变更 | P0 | 3 天内 |
| 新增中文文档且被标记为 P0/P1 | P1 | 14 天内 |
| 中文 P2/P3 文档发生修改 | P2 | 30 天内 |
| 根目录导航页（README.md、QUICK-START.md）修改 | P0 | 3 天内 |

---

## 3. 工作流程

### 3.1 变更检测（自动化）

`i18n-sync.yml` 每周日自动运行，检测以下变更：

1. 根目录中文文档与英文版本的修改时间差异
2. `i18n/en/` 和 `docs/i18n/en/` 的目录结构一致性
3. 术语库变更

`sync-tracker.py` 可手动运行以生成紧急变更队列：

```bash
python i18n/translation-workflow/sync-tracker.py
```

### 3.2 变更评估（人工）

维护者需在收到变更通知后 24 小时内完成评估：

1. **识别影响范围**: 哪些英文文档需要更新
2. **确定内容层级**: 按 [TRANSLATION-STRATEGY.md](./TRANSLATION-STRATEGY.md) 的 A/B/C 分层选择翻译策略
3. **分配责任人**: A 层分配给译者/B 层分配给领域专家/C 层分配给形式化专家

### 3.3 翻译与审校

| 层级 | 翻译方式 | 审校要求 | 完成标准 |
|------|----------|----------|----------|
| A | AI 预翻译 + 轻量修改 | 技术写作者快速审校 | `quality-checker.py` 通过，无 broken link |
| B | AI 初稿 + 专家逐句审校 | 领域专家签名 | 术语一致性 ≥ 98%，逻辑链条完整 |
| C | 人工主导（AI 仅辅助非证明段落） | 第二人交叉审校 | 数学语义等价，审校签名完整 |

### 3.4 质量检查

所有翻译产出在合并前必须通过：

```bash
python i18n/translation-workflow/quality-checker.py . [target_dir]
```

A/B 层文档出现 error 时必须修复，warning 数量不得超过 5 个。

### 3.5 发布与同步

英文翻译完成后：

1. **工作区**: `i18n/en/` 用于 AI 翻译草稿和迭代
2. **站点源**: `docs/i18n/en/` 用于面向读者的正式发布
3. **同步规则**:
   - A/B 层文档通过质量门禁后，由维护者同步到 `docs/i18n/en/`
   - C 层文档通过专家审校后，方可发布到 `docs/i18n/en/Struct/04-proofs/`

### 3.6 进度报告

`report-generator.py` 每周自动生成覆盖率报告：

```bash
python i18n/translation-workflow/report-generator.py
```

报告位置：

- JSON: `i18n/translation-workflow/reports/i18n-progress-report.json`
- Markdown: `i18n/translation-workflow/reports/i18n-progress-report.md`

---

## 4. 内容漂移防控措施

### 4.1 禁止事项

- **禁止**在未同步英文版本的情况下，长期保留已废弃的中文文档
- **禁止**将 C 层内容直接发布到 `docs/i18n/en/` 而不经过人工审校
- **禁止**在 `en/` 根目录创建新的独立英文文档（所有新增内容必须进入 `docs/i18n/en/` 或 `i18n/en/`）

### 4.2 回退机制

若英文版本严重落后于中文版本（>90 天未同步），执行以下回退：

1. 在英文页面顶部添加 `outdated` 警告横幅
2. 将该文档的 `translation_status` 降级为 `stale`
3. 在 14 天内安排重新翻译或更新

警告模板：

```markdown
> ⚠️ **Outdated Translation**: This English version is significantly behind the Chinese source. Please refer to the [Chinese version](../../path-to-zh.md) for the latest information.
```

---

## 5. 职责矩阵

| 角色 | 职责 |
|------|------|
| **项目维护者** | 监控变更、分配任务、同步 `docs/i18n/en/`、审批发布 |
| **译者/技术写作者** | 完成 A 层翻译和基础审校 |
| **领域技术专家** | 完成 B 层审校，确保概念和逻辑准确 |
| **形式化专家** | 完成 C 层翻译和审校，确保证明严谨 |
| **CI 系统** | 自动运行进度检查、质量门禁、报告生成 |

---

## 6. 参考

- [TRANSLATION-STRATEGY.md](./TRANSLATION-STRATEGY.md)
- [AI-TRANSLATION-AUDIT-REPORT-20260415.md](./translation-workflow/reports/AI-TRANSLATION-AUDIT-REPORT-20260415.md)
- [C-LAYER-TRANSLATION-PILOT.md](./C-LAYER-TRANSLATION-PILOT.md)

---

> **Last Updated**: 2026-04-15
