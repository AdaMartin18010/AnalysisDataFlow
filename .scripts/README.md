# AnalysisDataFlow 脚本工具集

> **版本**: v2.0 | **更新日期**: 2026-04-04

本目录包含 AnalysisDataFlow 项目的自动化脚本工具集，分为以下几个类别：

---

## 📂 脚本分类

### 1. 自动化工具集 (Automation Toolkit) - v1.0 ⭐ 新增

| 脚本 | 功能 | 状态 |
|:-----|:-----|:----:|
| `validate_theorem_numbers.py` | 定理编号验证：检查连续性、唯一性、注册表同步 | ✅ |
| `validate_mermaid.py` | Mermaid 语法校验：图表语法检查和修复建议 | ✅ |
| `generate_stats_report.py` | 统计报告生成：自动更新 STATISTICS-REPORT.md | ✅ |
| `health_check_dashboard.py` | 健康检查仪表盘：综合项目健康指标 | ✅ |
| `check_consistency.py` | 一致性检查：术语、格式、模板遵循情况 | ✅ |
| `update_progress.py` | 进度更新：自动更新 PROJECT-TRACKING.md | ✅ |

**使用方法**:
```bash
# 查看帮助
make automation-help

# 运行完整检查套件
make all-checks

# 单独运行某个检查
make validate-theorems
make validate-mermaid
make health-check
make check-consistency
make update-stats
make update-progress
```

**详细文档**: 参见项目根目录 `AUTOMATION-TOOLKIT-README.md`

---

### 2. 知识图谱工具

| 脚本 | 功能 | 状态 |
|:-----|:-----|:----:|
| `knowledge-graph-generator.py` | 生成知识图谱数据（Cytoscape/D3/Graphviz格式） | ✅ |

**使用方法**:
```bash
python .scripts/knowledge-graph-generator.py
```

---

### 3. 交叉引用工具

| 脚本 | 功能 | 状态 |
|:-----|:-----|:----:|
| `validate_cross_refs.py` | 验证交叉引用链接有效性 | ✅ |
| `fix_cross_refs.py` | 修复交叉引用问题 | ✅ |
| `fix_all_cross_refs.py` | 批量修复交叉引用 | ✅ |

---

### 4. Flink 监控工具

| 脚本 | 功能 | 状态 |
|:-----|:-----|:----:|
| `flink-release-monitor.py` | Flink 版本发布监控 | ✅ |
| `flink-version-tracking` | 版本跟踪数据 | ✅ |

---

### 5. 国际化工具

| 脚本 | 功能 | 状态 |
|:-----|:-----|:----:|
| `i18n-manager.py` | 国际化内容管理 | ✅ |

---

### 6. 反馈与统计工具

| 脚本 | 功能 | 状态 |
|:-----|:-----|:----:|
| `feedback-aggregator.py` | 反馈聚合 | ✅ |
| `feedback-dashboard.py` | 反馈仪表盘 | ✅ |
| `stats-updater` | 统计更新 | ✅ |
| `update-stats.py` | 更新统计 | ✅ |

---

### 7. 学习路径工具

| 脚本 | 功能 | 状态 |
|:-----|:-----|:----:|
| `learning-path-recommender.py` | 学习路径推荐 | ✅ |

---

## 🚀 快速开始

### 安装依赖

大多数脚本仅依赖 Python 3.8+ 标准库，无需额外安装。

**可选依赖**（用于增强功能）：
```bash
# Mermaid 图表验证（本地完整验证）
npm install -g @mermaid-js/mermaid-cli
```

### 运行检查

```bash
# 完整项目检查
make all-checks

# 或单独运行特定检查
python .scripts/validate_theorem_numbers.py
python .scripts/validate_mermaid.py
python .scripts/health_check_dashboard.py
```

---

## 📊 退出码约定

所有脚本遵循以下退出码约定：

| 退出码 | 含义 |
|-------:|:-----|
| `0` | 执行成功/检查通过 |
| `1` | 发现错误/检查未通过 |
| `2` | 运行异常/系统错误 |
| `130` | 用户取消 (Ctrl+C) |

---

## 🔧 开发指南

### 添加新脚本

1. 将脚本放入 `.scripts/` 目录
2. 添加标准文件头：
   ```python
   #!/usr/bin/env python3
   # -*- coding: utf-8 -*-
   """
   脚本描述 - AnalysisDataFlow 自动化工具集
   
   功能：...
   使用方法：...
   退出码：...
   """
   ```
3. 实现 `--help` 参数
4. 遵循退出码约定
5. 在 `Makefile` 中添加对应命令（如适用）
6. 更新本文档

### 代码规范

- 使用 Python 3.8+ 语法
- 使用 `pathlib` 处理路径
- 使用 `dataclasses` 定义数据结构
- 添加适当的错误处理
- 支持 `--json` 输出格式（用于 CI/CD）

---

## 📚 相关文档

- [自动化工具集详细文档](../AUTOMATION-TOOLKIT-README.md)
- [项目跟踪](../PROJECT-TRACKING.md)
- [定理注册表](../THEOREM-REGISTRY.md)
- [统计报告](../STATISTICS-REPORT.md)

---

*最后更新: 2026-04-04*
