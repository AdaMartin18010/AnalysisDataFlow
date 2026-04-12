> **状态**: 🔮 前瞻内容 | **风险等级**: 高 | **最后更新**: 2026-04
> 
> 此文档描述的内容处于早期规划阶段，可能与最终实现不符。请以 Apache Flink 官方发布为准。
# 内容新鲜度标记模板

## 标记格式

在每篇Markdown文档的顶部添加YAML front matter：

```yaml
---
freshness:
  last_updated: "YYYY-MM-DD"        # 最后更新日期
  tech_version: "Flink X.Y"         # 主要技术版本
  confidence_level: "high|medium|low" # 置信度评级
  content_type: "core|reference|frontier|practice" # 内容类型
  refs_count: N                      # 引用数量
  validation_status: "pending|validated|deprecated" # 验证状态
  next_review: "YYYY-MM-DD"         # 建议下次审查日期
  tags:                              # 额外标签
    - "tag1"
    - "tag2"
---
```

## 标记示例

### 高置信度 - 核心机制文档

```yaml
---
freshness:
  last_updated: "2026-04-04"
  tech_version: "Flink 2.2"
  confidence_level: "high"
  content_type: "core"
  refs_count: 15
  validation_status: "validated"
  next_review: "2026-10-04"
  tags:
    - "checkpoint"
    - "fault-tolerance"
    - "state-management"
---
```

### 中等置信度 - 前沿特性文档

```yaml
---
freshness:
  last_updated: "2026-04-02"
  tech_version: "Flink 2.3"
  confidence_level: "medium"
  content_type: "frontier"
  refs_count: 8
  validation_status: "pending"
  next_review: "2026-06-02"
  tags:
    - "ai-agent"
    - "flip-531"
    - "experimental"
---
```

### 低置信度 - 旧版本文档

```yaml
---
freshness:
  last_updated: "2025-06-15"
  tech_version: "Flink 1.18"
  confidence_level: "low"
  content_type: "reference"
  refs_count: 5
  validation_status: "deprecated"
  next_review: "2026-04-15"
  tags:
    - "legacy"
    - "migration-needed"
---
```

## 置信度评级标准

### High (高置信度)

**判定标准**：

- 最后更新在 90 天内
- 技术版本为当前主流版本 (Flink 2.0+)
- 引用数量 ≥ 8
- 核心概念/稳定API文档

**使用建议**：可直接参考，内容可靠

### Medium (中等置信度)

**判定标准**：

- 最后更新在 90-180 天内
- 技术版本为兼容版本 (Flink 1.17+)
- 引用数量 3-7
- 前沿特性/预览功能文档

**使用建议**：基本可靠，关键信息需验证

### Low (低置信度)

**判定标准**：

- 最后更新超过 180 天
- 技术版本较旧 (Flink 1.16 或更早)
- 引用数量 < 3
- 未验证的实践/案例

**使用建议**：内容可能过时，必须验证后使用

## 内容类型说明

| 类型 | 说明 | 示例 |
|------|------|------|
| **core** | 核心机制、架构设计、基础概念 | Checkpoint机制、状态管理 |
| **reference** | API参考、配置文档、函数列表 | SQL函数参考、连接器配置 |
| **frontier** | 前沿特性、路线图、实验性功能 | AI Agent、Rust原生支持 |
| **practice** | 实践指南、案例研究、最佳实践 | 性能调优、生产部署 |

## 自动化规则

### 下次审查日期计算

```text
# 根据置信度自动计算下次审查日期
if confidence_level == "high":
    next_review = last_updated + 6个月
elif confidence_level == "medium":
    next_review = last_updated + 3个月
else:  # low
    next_review = last_updated + 1个月
```

### 版本EOL检测

```python
# 检测技术版本是否已EOL
EOL_VERSIONS = ["1.13", "1.14", "1.15", "1.16"]
if tech_version in EOL_VERSIONS:
    validation_status = "deprecated"
    confidence_level = "low"
```
