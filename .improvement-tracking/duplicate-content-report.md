# 重复内容检测报告

> 生成时间: 2026-04-05 15:30:22
> 相似度阈值: 70%

## 摘要

| 类别 | 数量 | 严重程度 |
|------|------|----------|
| 🚨 完全相同 | 1 | 高 |
| 🔴 高度相似 (≥80%) | 1 | 高 |
| 🟡 中度相似 (60-80%) | 0 | 中 |
| 🟢 部分相似 (40-60%) | 0 | 低 |
| 📝 标题重复 | 9 | 中 |
| **总计** | **11** | - |

---

## 1. 完全相同的文档

以下文件内容完全相同，建议保留一个，删除或归档其他副本：

### 1.1 哈希: a80f0820

| 文件路径 | 大小 |
|----------|------|
| `reports\weekly\weekly-report-latest.md` | 4366 bytes |
| `reports\weekly\weekly-report-W14-20260404.md` | 4366 bytes |

**建议操作**: 保留最新版本，归档或删除其他副本

---

## 2. 高度相似的文档 (≥80%)

以下内容高度相似，可能是重复内容或应该合并：

### 2.1 相似度: 100.0%

- **文档A**: `reports\weekly\weekly-report-latest.md`
  - 标题: 📊 AnalysisDataFlow 项目周报...
  - 字数: 168
  - 定义数: 0, 定理数: 0

- **文档B**: `reports\weekly\weekly-report-W14-20260404.md`
  - 标题: 📊 AnalysisDataFlow 项目周报...
  - 字数: 168
  - 定义数: 0, 定理数: 0

**建议操作**: 检查是否可以合并为一篇文档

---

## 3. 中度相似的文档 (60-80%)

以下内容中度相似，可能包含重复章节：

| 相似度 | 文档A | 文档B |
|--------|-------|-------|
✅ 未发现中度相似的文档


---

## 4. 标题重复的文档

以下文档标题相同或非常相似：

### 4.1 标题: AnalysisDataFlow Quick Start Guide

- `QUICK-START-EN.md`
- `docs\i18n\en\QUICK-START.md`

### 4.2 标题: AnalysisDataFlow

- `README-EN.md`
- `README.md`
- `docs\i18n\en\README.md`
- `i18n\en\README.md`

### 4.3 标题: Flink State Backends 深度对比与选型指南

- `Flink\3.9-state-backends-deep-comparison.md`
- `Flink\flink-state-backends-comparison.md`

### 4.4 标题: Flink Built-in Functions 完整参考

- `Flink\built-in-functions-reference.md`
- `Flink\flink-built-in-functions-reference.md`

### 4.5 标题: Flink Data Types 完整参考

- `Flink\data-types-complete-reference.md`
- `Flink\flink-data-types-reference.md`
- `Flink\03-api\03.02-table-sql-api\data-types-complete-reference.md`

### 4.6 标题: Flink 生产环境检查清单

- `Flink\04-runtime\04.02-operations\production-checklist.md`
- `Knowledge\production-checklist.md`

### 4.7 标题: Kafka Streams 到 Flink 迁移指南

- `Knowledge\05-mapping-guides\migration-guides\05.2-kafka-streams-to-flink-migration.md`
- `Knowledge\05-migrations\kafka-streams-to-flink-guide.md`

### 4.8 标题: AnalysisDataFlow 虚构内容审计报告

- `reports\fictional-content-audit-20260405_143730.md`
- `scripts\config\audit-report-template.md`

### 4.9 标题: 📊 AnalysisDataFlow 项目周报

- `reports\weekly\weekly-report-latest.md`
- `reports\weekly\weekly-report-W14-20260404.md`

---

## 5. 建议的合并策略

### 5.1 短期行动

1. **处理完全重复的文档**: 立即删除或归档
2. **处理标题重复**: 重命名以区分内容
3. **审查高度相似文档**: 决定是否合并

### 5.2 长期改进

1. **建立文档模板**: 减少重复内容产生
2. **内容引用机制**: 使用链接代替复制
3. **定期检测**: 每月运行此脚本

### 5.3 合并脚本示例

```bash
# 示例：合并两个高度相似的文档
cat doc1.md > merged.md
echo "" >> merged.md
echo "<!-- 以下内容来自 doc2.md -->" >> merged.md
cat doc2.md >> merged.md
```
