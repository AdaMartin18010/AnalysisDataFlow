# A1 - 内容新鲜度扫描执行报告

生成时间: 2026-04-05T15:23:50.804040
扫描目录: Flink/
总文件数: 326

## 执行摘要

本次扫描分析了Flink目录下的所有markdown文档，基于以下维度评估内容新鲜度：

- 文档最后修改时间
- 技术版本相关性
- 引用数量和质量
- 内容类型分类

## 置信度分布

| 等级 | 数量 | 百分比 | 说明 |
|------|------|--------|------|
| high | 203 | 62.3% | 内容可靠，可直接参考 |
| medium | 123 | 37.7% | 基本可靠，关键信息需验证 |
| low | 0 | 0.0% | 可能过时，必须验证后使用 |

## 内容类型分布

| 类型 | 数量 | 说明 |
|------|------|------|
| frontier | 109 | 前沿特性、实验功能 |
| reference | 95 | API参考、配置文档 |
| practice | 78 | 实践指南、案例研究 |
| core | 44 | 核心机制、架构设计 |

## 版本分布

| 版本 | 数量 |
|------|------|
| 2.0 | 28 |
| 2.1 | 5 |
| 2.2 | 236 |
| 2.3 | 23 |
| 2.4 | 13 |
| 2.5 | 10 |
| 2.6 | 2 |
| 2.7 | 2 |
| 3.0 | 6 |
| 3.1 | 1 |

## 低置信度文件列表（需优先审查）


## 高置信度文件示例

- `Flink/built-in-functions-reference.md` (v2.2, refs: 0)
- `Flink/data-types-complete-reference.md` (v2.2, refs: 0)
- `Flink/elasticsearch-connector-guide.md` (v2.2, refs: 0)
- `Flink/flink-built-in-functions-reference.md` (v2.2, refs: 0)
- `Flink/flink-cep-complete-tutorial.md` (v2.2, refs: 0)
- `Flink/flink-data-types-reference.md` (v2.2, refs: 7)
- `Flink/flink-pyflink-deep-dive.md` (v2.2, refs: 8)
- `Flink/jdbc-connector-guide.md` (v2.2, refs: 0)
- `Flink/materialize-comparison.md` (v2.2, refs: 3)
- `Flink/mongodb-connector-guide.md` (v2.2, refs: 0)
- `Flink/pulsar-functions-integration.md` (v2.2, refs: 0)
- `Flink/pyflink-deep-guide.md` (v2.2, refs: 0)
- `Flink/risingwave-integration-guide.md` (v2.2, refs: 3)
- `Flink/state-backends-comparison.md` (v2.0, refs: 5)
- `Flink/01-concepts/datastream-v2-semantics.md` (v2.0, refs: 9)

## 生成的文件

1. `freshness-metadata.json` - 完整元数据文件
2. `freshness-template.md` - 新鲜度标记模板
3. `content-freshness-system.md` - 系统设计文档
4. `apply-freshness-tags.py` - 批量标记应用脚本

## 后续操作

1. 审查低置信度文件，更新过期内容
2. 运行 `python apply-freshness-tags.py` 应用标记（试运行）
3. 确认无误后运行 `python apply-freshness-tags.py --apply` 正式应用

---

*报告由内容新鲜度标记系统自动生成*
