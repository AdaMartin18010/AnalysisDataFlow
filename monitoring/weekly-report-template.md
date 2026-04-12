# 📊 AnalysisDataFlow 质量监控周报

> **报告周期**: {{start_date}} - {{end_date}}
> **报告生成时间**: {{generated_at}}
> **监控版本**: v1.0.0
> **状态**: {{overall_status}}

---

## 📋 执行摘要

### 本周关键指标概览

| 指标 | 本周数值 | 上周数值 | 变化 | 状态 |
|------|----------|----------|------|------|
| 总体质量评分 | {{quality_overall}} | {{quality_overall_prev}} | {{quality_change}} | {{quality_status}} |
| 文档总数 | {{doc_count}} | {{doc_count_prev}} | {{doc_change}} | {{doc_status}} |
| 链接健康率 | {{link_health_rate}}% | {{link_health_rate_prev}}% | {{link_change}} | {{link_status}} |
| 形式化元素 | {{formal_elements}} | {{formal_elements_prev}} | {{formal_change}} | {{formal_status}} |
| 代码示例数 | {{code_blocks}} | {{code_blocks_prev}} | {{code_change}} | {{code_status}} |

### 本周亮点 ✨

{{highlights}}

### 需要关注的问题 ⚠️

{{concerns}}

---

## 📈 趋势分析

### 质量评分趋势 (过去4周)

```
Week -3: {{quality_w3}} │{{quality_bar_w3}}│
Week -2: {{quality_w2}} │{{quality_bar_w2}}│
Week -1: {{quality_w1}} │{{quality_bar_w1}}│
Week  0: {{quality_w0}} │{{quality_bar_w0}}│ ← 当前
         0----+----+----+----+----+----+----+----+----+----100
```

### 文档增长趋势

```
{{doc_trend_chart}}
```

### 链接健康趋势

```
{{link_trend_chart}}
```

---

## 📊 详细指标分析

### 1. 文档统计

#### 按目录分布

| 目录 | 文档数 | 占比 | 行数 | 大小 |
|------|--------|------|------|------|
| Struct | {{struct_count}} | {{struct_pct}}% | {{struct_lines}} | {{struct_size}}MB |
| Knowledge | {{knowledge_count}} | {{knowledge_pct}}% | {{knowledge_lines}} | {{knowledge_size}}MB |
| Flink | {{flink_count}} | {{flink_pct}}% | {{flink_lines}} | {{flink_size}}MB |
| Tutorials | {{tutorials_count}} | {{tutorials_pct}}% | {{tutorials_lines}} | {{tutorials_size}}MB |
| Visuals | {{visuals_count}} | {{visuals_pct}}% | {{visuals_lines}} | {{visuals_size}}MB |
| EN | {{en_count}} | {{en_pct}}% | {{en_lines}} | {{en_size}}MB |

#### 本周变更

- **新增文档**: {{docs_added}} 篇
- **修改文档**: {{docs_modified}} 篇
- **删除文档**: {{docs_deleted}} 篇
- **净增长**: {{docs_net_change}} 篇

### 2. 代码示例分析

#### 编程语言分布

| 语言 | 代码块数 | 占比 | 代码行数 |
|------|----------|------|----------|
| Java | {{java_blocks}} | {{java_pct}}% | {{java_lines}} |
| Python | {{python_blocks}} | {{python_pct}}% | {{python_lines}} |
| Scala | {{scala_blocks}} | {{scala_pct}}% | {{scala_lines}} |
| Go | {{go_blocks}} | {{go_pct}}% | {{go_lines}} |
| Rust | {{rust_blocks}} | {{rust_pct}}% | {{rust_lines}} |
| SQL | {{sql_blocks}} | {{sql_pct}}% | {{sql_lines}} |
| YAML | {{yaml_blocks}} | {{yaml_pct}}% | {{yaml_lines}} |
| 其他 | {{other_blocks}} | {{other_pct}}% | {{other_lines}} |

#### 本周变更

- **新增代码块**: {{code_added}} 个
- **新增代码行**: {{code_lines_added}} 行
- **覆盖率提升**: {{coverage_change}}%

### 3. 链接健康检查

#### 链接类型分布

| 类型 | 数量 | 健康率 | 失效数 |
|------|------|--------|--------|
| 内部链接 | {{internal_links}} | {{internal_health}}% | {{internal_broken}} |
| 外部链接 | {{external_links}} | {{external_health}}% | {{external_broken}} |
| 交叉引用 | {{cross_refs}} | {{cross_ref_health}}% | {{cross_ref_broken}} |

#### 失效链接详情

{{#if broken_links_list}}

| 文件 | 目标链接 | 类型 |
|------|----------|------|
{{#each broken_links_list}}
| {{file}} | {{target}} | {{type}} |
{{/each}}
{{else}}
✅ 本周无失效链接
{{/if}}

#### 本周修复

- **修复链接**: {{links_fixed}} 个
- **新增失效**: {{new_broken}} 个
- **净改善**: {{links_improvement}} 个

### 4. 形式化元素统计

#### 按类型分布

| 类型 | 数量 | 本周新增 | 累计总数 |
|------|------|----------|----------|
| 定理 (Thm) | {{theorems}} | {{theorems_new}} | {{theorems_total}} |
| 定义 (Def) | {{definitions}} | {{definitions_new}} | {{definitions_total}} |
| 引理 (Lemma) | {{lemmas}} | {{lemmas_new}} | {{lemmas_total}} |
| 命题 (Prop) | {{propositions}} | {{propositions_new}} | {{propositions_total}} |
| 推论 (Cor) | {{corollaries}} | {{corollaries_new}} | {{corollaries_total}} |
| **总计** | **{{formal_total}}** | **{{formal_new}}** | **{{formal_cumulative}}** |

#### 按目录分布

| 目录 | 定理 | 定义 | 引理 | 命题 | 推论 |
|------|------|------|------|------|------|
| Struct | {{struct_thm}} | {{struct_def}} | {{struct_lemma}} | {{struct_prop}} | {{struct_cor}} |
| Knowledge | {{knowledge_thm}} | {{knowledge_def}} | {{knowledge_lemma}} | {{knowledge_prop}} | {{knowledge_cor}} |
| Flink | {{flink_thm}} | {{flink_def}} | {{flink_lemma}} | {{flink_prop}} | {{flink_cor}} |

### 5. 可视化统计

| 类型 | 数量 | 本周新增 |
|------|------|----------|
| Mermaid 图表 | {{mermaid_count}} | {{mermaid_new}} |
| 图片 | {{image_count}} | {{image_new}} |
| 含可视化文件 | {{visual_files}} | {{visual_files_new}} |

### 6. 质量评分详情

#### 评分维度

| 维度 | 评分 | 权重 | 加权得分 | 趋势 |
|------|------|------|----------|------|
| 完整性 | {{completeness}} | 25% | {{completeness_weighted}} | {{completeness_trend}} |
| 一致性 | {{consistency}} | 25% | {{consistency_weighted}} | {{consistency_trend}} |
| 覆盖率 | {{coverage}} | 25% | {{coverage_weighted}} | {{coverage_trend}} |
| 可维护性 | {{maintainability}} | 25% | {{maintainability_weighted}} | {{maintainability_trend}} |
| **总体** | **{{quality_overall}}** | 100% | **{{quality_overall}}** | **{{quality_trend}}** |

#### 评分历史 (4周)

| 周次 | 总体 | 完整性 | 一致性 | 覆盖率 | 可维护性 |
|------|------|--------|--------|--------|----------|
| W-3 | {{q_w3}} | {{c_w3}} | {{cn_w3}} | {{cv_w3}} | {{m_w3}} |
| W-2 | {{q_w2}} | {{c_w2}} | {{cn_w2}} | {{cv_w2}} | {{m_w2}} |
| W-1 | {{q_w1}} | {{c_w1}} | {{cn_w1}} | {{cv_w1}} | {{m_w1}} |
| W-0 | {{q_w0}} | {{c_w0}} | {{cn_w0}} | {{cv_w0}} | {{m_w0}} |

---

## 🚨 告警分析

### 本周告警统计

| 严重级别 | 数量 | 已解决 | 未解决 |
|----------|------|--------|--------|
| 🔴 Critical | {{critical_count}} | {{critical_resolved}} | {{critical_open}} |
| 🟡 Warning | {{warning_count}} | {{warning_resolved}} | {{warning_open}} |
| 🔵 Info | {{info_count}} | {{info_resolved}} | {{info_open}} |
| **总计** | **{{total_alerts}}** | **{{total_resolved}}** | **{{total_open}}** |

### 未解决告警

{{#if open_alerts}}

| 时间 | 级别 | 规则 | 消息 | 状态 |
|------|------|------|------|------|
{{#each open_alerts}}
| {{time}} | {{severity}} | {{rule}} | {{message}} | {{status}} |
{{/each}}
{{else}}
✅ 无未解决告警
{{/if}}

### 告警趋势

```
{{alert_trend_chart}}
```

---

## 📋 行动项

### 🔴 高优先级 (本周内)

{{#each high_priority_actions}}

- [ ] {{description}}
  - 负责人: {{assignee}}
  - 截止日期: {{due_date}}
  - 关联指标: {{metric}}
{{/each}}

### 🟡 中优先级 (两周内)

{{#each medium_priority_actions}}

- [ ] {{description}}
  - 负责人: {{assignee}}
  - 截止日期: {{due_date}}
  - 关联指标: {{metric}}
{{/each}}

### 🟢 低优先级 (持续改进)

{{#each low_priority_actions}}

- [ ] {{description}}
  - 建议时间: {{suggested_time}}
  - 预期收益: {{benefit}}
{{/each}}

---

## 🎯 目标与里程碑

### 本周目标回顾

| 目标 | 目标值 | 实际值 | 完成度 | 状态 |
|------|--------|--------|--------|------|
| 文档数量 | {{target_doc}} | {{actual_doc}} | {{doc_progress}}% | {{doc_goal_status}} |
| 链接健康率 | {{target_link}}% | {{actual_link}}% | {{link_progress}}% | {{link_goal_status}} |
| 质量评分 | {{target_quality}} | {{actual_quality}} | {{quality_progress}}% | {{quality_goal_status}} |
| 代码示例 | {{target_code}} | {{actual_code}} | {{code_progress}}% | {{code_goal_status}} |

### 下周目标

- 📄 文档数量: 目标 {{next_doc_target}} ({{next_doc_delta}})
- 🔗 链接健康率: 目标 {{next_link_target}}% ({{next_link_delta}}%)
- ⭐ 质量评分: 目标 {{next_quality_target}} ({{next_quality_delta}})
- 💻 代码示例: 目标 {{next_code_target}} ({{next_code_delta}})

---

## 📊 性能监控

### 构建性能

| 指标 | 本周平均 | 上周平均 | 变化 | 状态 |
|------|----------|----------|------|------|
| 构建时间 | {{build_time_avg}}s | {{build_time_prev}}s | {{build_time_change}} | {{build_time_status}} |
| 检查耗时 | {{check_duration_avg}}s | {{check_duration_prev}}s | {{check_duration_change}} | {{check_duration_status}} |
| 成功率 | {{success_rate}}% | {{success_rate_prev}}% | {{success_rate_change}} | {{success_rate_status}} |

### 资源使用

| 资源 | 本周峰值 | 平均值 | 趋势 |
|------|----------|--------|------|
| CPU | {{cpu_peak}}% | {{cpu_avg}}% | {{cpu_trend}} |
| 内存 | {{mem_peak}}MB | {{mem_avg}}MB | {{mem_trend}} |
| 磁盘 I/O | {{io_peak}}MB/s | {{io_avg}}MB/s | {{io_trend}} |

---

## 📚 附录

### A. 指标定义

| 指标 | 定义 | 计算方式 |
|------|------|----------|
| 总体质量评分 | 项目整体质量的综合评分 | (完整性 + 一致性 + 覆盖率 + 可维护性) / 4 |
| 完整性 | 文档结构的完整程度 | 实际文档数 / 目标文档数 × 100 |
| 一致性 | 文档间的一致程度 | 有效链接数 / 总链接数 × 100 |
| 覆盖率 | 代码示例和用例的覆盖程度 | 代码块数 / 目标代码块数 × 100 |
| 可维护性 | 项目的可维护程度 | 形式化元素数 / 目标数量 × 100 |
| 链接健康率 | 链接的有效程度 | 有效链接数 / 总链接数 × 100 |

### B. 阈值说明

| 指标 | Critical | Warning | Target |
|------|----------|---------|--------|
| 质量评分 | < 70 | < 85 | ≥ 95 |
| 链接健康率 | < 90% | < 95% | ≥ 99% |
| 构建时间 | > 600s | > 300s | ≤ 120s |
| 失效链接 | > 50 | > 10 | 0 |

### C. 数据来源

- 文档统计: 文件系统扫描
- 代码示例: 内容分析脚本
- 链接健康: 链接检查器
- 形式化元素: 内容正则匹配
- 质量评分: 综合计算

### D. 报告生成信息

- **生成脚本**: `.scripts/performance-monitor.py`
- **配置文件**: `monitoring/quality-dashboard-config.yml`
- **历史数据**: `monitoring/metrics-history.json`
- **原始数据**: `monitoring/performance-report.json`

---

## 📝 变更日志

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| 1.0.0 | 2026-04-12 | 初始版本，建立周报模板 |

---

*本报告由 AnalysisDataFlow 质量监控系统自动生成*
*如有问题，请联系: <maintainers@analysisdataflow.org>*
