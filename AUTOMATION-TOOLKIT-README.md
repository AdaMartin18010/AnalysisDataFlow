# AnalysisDataFlow 自动化工具集

> **版本**: v1.0 | **更新日期**: 2026-04-04 | **状态**: 生产就绪

本自动化工具集为 AnalysisDataFlow 项目提供全面的质量保证和项目管理自动化支持。

---

## 📋 目录

- [概述](#概述)
- [安装要求](#安装要求)
- [脚本清单](#脚本清单)
- [使用方法](#使用方法)
- [Makefile 命令](#makefile-命令)
- [CI/CD 集成](#ci-cd-集成)
- [故障排除](#故障排除)

---

## 概述

自动化工具集包含 6 个核心脚本，覆盖以下功能领域：

| 功能领域 | 脚本 | 说明 |
|:---------|:-----|:-----|
| 定理验证 | `validate_theorem_numbers.py` | 检查定理/定义/引理编号的连续性和唯一性 |
| 图表验证 | `validate_mermaid.py` | 验证 Mermaid 图表语法正确性 |
| 统计报告 | `generate_stats_report.py` | 自动生成项目统计报告 |
| 健康检查 | `health_check_dashboard.py` | 综合项目健康状态仪表盘 |
| 一致性检查 | `check_consistency.py` | 检查术语和格式一致性 |
| 进度更新 | `update_progress.py` | 自动更新 PROJECT-TRACKING.md |

---

## 安装要求

### 必需依赖

- Python 3.8+
- 标准库（无需额外安装）

### 可选依赖

```bash
# 安装 mermaid-cli 以获得完整的 Mermaid 语法验证
npm install -g @mermaid-js/mermaid-cli
```

---

## 脚本清单

### 1. 定理编号验证脚本

**文件**: `.scripts/validate_theorem_numbers.py`

**功能**:
- 检查所有定理/定义/引理/命题/推论编号的连续性
- 检测重复编号
- 验证与 THEOREM-REGISTRY.md 的一致性
- 检测格式不规范的编号

**使用示例**:
```bash
# 基本验证
python .scripts/validate_theorem_numbers.py

# 输出 JSON 格式报告
python .scripts/validate_theorem_numbers.py --json > report.json

# 显示详细信息
python .scripts/validate_theorem_numbers.py --verbose

# 尝试自动修复（开发中）
python .scripts/validate_theorem_numbers.py --fix
```

**退出码**:
- `0` - 所有检查通过
- `1` - 发现错误
- `2` - 运行异常

---

### 2. Mermaid 语法校验脚本

**文件**: `.scripts/validate_mermaid.py`

**功能**:
- 提取所有 Markdown 文件中的 Mermaid 代码块
- 使用本地 mermaid-cli 或在线 API 验证语法
- 检测括号不匹配、无效节点等常见问题
- 支持基本语法检查（无需外部依赖）

**使用示例**:
```bash
# 基本验证（使用基本语法检查）
python .scripts/validate_mermaid.py

# 使用在线 API 验证
python .scripts/validate_mermaid.py --online

# 只验证指定目录
python .scripts/validate_mermaid.py Struct/ Knowledge/

# 输出 JSON 格式
python .scripts/validate_mermaid.py --json

# 尝试自动修复
python .scripts/validate_mermaid.py --fix
```

**退出码**:
- `0` - 所有检查通过
- `1` - 发现语法错误
- `2` - 运行异常

---

### 3. 统计报告自动生成

**文件**: `.scripts/generate_stats_report.py`

**功能**:
- 自动统计文档数量、分布
- 统计形式化元素（定理/定义/引理等）
- 统计代码行数、Mermaid 图表数量
- 自动更新 STATISTICS-REPORT.md

**使用示例**:
```bash
# 显示统计摘要
python .scripts/generate_stats_report.py

# 更新统计报告文件
python .scripts/generate_stats_report.py --update

# 输出 JSON 格式
python .scripts/generate_stats_report.py --json

# 保存到自定义路径
python .scripts/generate_stats_report.py --output my-report.md
```

**退出码**:
- `0` - 执行成功
- `1` - 执行出错

---

### 4. 项目健康检查仪表盘

**文件**: `.scripts/health_check_dashboard.py`

**功能**:
- 综合检查所有健康指标
- 文档覆盖率检查
- 定理注册表同步状态
- 链接健康状态
- Mermaid 图表健康
- 文档新鲜度分析
- 趋势分析和历史对比

**使用示例**:
```bash
# 运行健康检查
python .scripts/health_check_dashboard.py

# 保存到历史记录
python .scripts/health_check_dashboard.py --save

# 输出 JSON 格式
python .scripts/health_check_dashboard.py --json

# 显示趋势分析
python .scripts/health_check_dashboard.py --trend
```

**输出指标**:
| 指标 | 说明 | 阈值 |
|:-----|:-----|:-----|
| document_coverage | 核心文档覆盖率 | > 90% |
| theorem_registry_sync | 定理注册表同步率 | > 95% |
| link_health | 链接健康度 | 错误 < 10 |
| mermaid_health | Mermaid 图表健康度 | 问题 < 5% |
| document_freshness | 文档新鲜度 | 过时 < 10 |
| progress_alignment | 进度跟踪对齐 | 已更新 |

**退出码**:
- `0` - 健康状态良好
- `1` - 发现需要关注的问题
- `2` - 运行异常

---

### 5. 文档一致性检查

**文件**: `.scripts/check_consistency.py`

**功能**:
- 检查术语使用一致性
- 检查格式一致性（标题、列表、代码块）
- 检查引用格式一致性
- 检查六段式模板遵循情况
- 生成术语使用统计

**使用示例**:
```bash
# 检查整个项目
python .scripts/check_consistency.py

# 只检查指定目录
python .scripts/check_consistency.py Struct/ Knowledge/

# 输出 JSON 格式
python .scripts/check_consistency.py --json

# 尝试自动修复
python .scripts/check_consistency.py --fix
```

**检查项**:
- 标题层级跳跃
- 标题末尾标点
- 术语变体检测（如 Dataflow vs Data Flow）
- 代码块语言标签
- 引用编号连续性
- 列表标记一致性

**退出码**:
- `0` - 一致性良好
- `1` - 发现不一致问题
- `2` - 运行异常

---

### 6. 进度自动更新

**文件**: `.scripts/update_progress.py`

**功能**:
- 自动扫描项目文档计算实际进度
- 更新 PROJECT-TRACKING.md 中的进度条
- 支持手动指定进度数值
- 生成进度更新报告

**使用示例**:
```bash
# 自动扫描并显示进度
python .scripts/update_progress.py --auto

# 自动扫描并更新文件
python .scripts/update_progress.py --auto --update-file

# 手动指定进度并更新
python .scripts/update_progress.py --struct 45 --knowledge 120 --flink 130 --update-file

# 预览更改（不写入）
python .scripts/update_progress.py --dry-run
```

**退出码**:
- `0` - 更新成功
- `1` - 更新失败
- `2` - 运行异常

---

## 使用方法

### 快速开始

```bash
# 查看所有可用命令
make help

# 查看自动化工具集专用帮助
make automation-help

# 运行完整检查套件
make all-checks
```

### 日常使用流程

```bash
# 1. 验证定理编号
make validate-theorems

# 2. 验证 Mermaid 图表
make validate-mermaid

# 3. 检查文档一致性
make check-consistency

# 4. 运行健康检查
make health-check

# 5. 更新统计报告
make update-stats

# 6. 更新项目进度
make update-progress
```

---

## Makefile 命令

### 验证命令

| 命令 | 说明 |
|:-----|:-----|
| `make validate-theorems` | 验证定理编号连续性和唯一性 |
| `make validate-mermaid` | 验证 Mermaid 图表语法 |
| `make validate-crossrefs` | 验证交叉引用链接 |
| `make check-consistency` | 检查文档一致性 |

### 统计与报告

| 命令 | 说明 |
|:-----|:-----|
| `make current-stats` | 显示项目统计摘要 |
| `make update-stats` | 更新 STATISTICS-REPORT.md |
| `make health-check` | 运行项目健康检查仪表盘 |
| `make health-check-json` | 输出 JSON 格式健康报告 |

### 维护命令

| 命令 | 说明 |
|:-----|:-----|
| `make update-progress` | 自动更新 PROJECT-TRACKING.md 进度 |
| `make fix-links` | 修复文档链接问题 |
| `make update-index` | 更新所有索引 |

### 综合命令

| 命令 | 说明 |
|:-----|:-----|
| `make all-checks` | 运行所有检查（完整套件） |
| `make validate` | 运行标准验证（项目+交叉引用+Mermaid） |
| `make automation-help` | 显示自动化工具集详细帮助 |

---

## CI/CD 集成

### GitHub Actions 示例

```yaml
name: Project Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Validate Theorem Numbers
        run: python .scripts/validate_theorem_numbers.py --json
        continue-on-error: true
      
      - name: Validate Mermaid
        run: python .scripts/validate_mermaid.py --json
        continue-on-error: true
      
      - name: Health Check
        run: python .scripts/health_check_dashboard.py --json
      
      - name: Check Consistency
        run: python .scripts/check_consistency.py --json
```

### 预提交钩子示例

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: validate-theorems
        name: Validate theorem numbers
        entry: python .scripts/validate_theorem_numbers.py
        language: system
        pass_filenames: false
      
      - id: check-consistency
        name: Check document consistency
        entry: python .scripts/check_consistency.py
        language: system
        pass_filenames: false
```

---

## 故障排除

### 常见问题

#### 1. Mermaid 验证失败

**问题**: `mmdc` 命令未找到

**解决**:
```bash
# 安装 mermaid-cli
npm install -g @mermaid-js/mermaid-cli

# 或使用在线验证
python .scripts/validate_mermaid.py --online
```

#### 2. 定理编号验证报告大量警告

**问题**: 注册表中缺少部分定理

**解决**:
```bash
# 查看详细报告
python .scripts/validate_theorem_numbers.py --verbose

# 手动更新 THEOREM-REGISTRY.md
```

#### 3. 健康检查运行缓慢

**问题**: 交叉引用验证耗时较长

**解决**:
```bash
# 单独运行健康检查（跳过交叉引用）
python .scripts/health_check_dashboard.py

# 或限制超时时间
python .scripts/validate_cross_refs.py  # 单独运行
```

### 调试模式

所有脚本都支持 `--verbose` 或 `-v` 参数显示详细信息：

```bash
python .scripts/validate_theorem_numbers.py --verbose
python .scripts/check_consistency.py --verbose
```

---

## 版本历史

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| v1.0 | 2026-04-04 | 初始发布，包含 6 个核心脚本 |

---

## 贡献指南

如需添加新脚本或改进现有脚本：

1. 将脚本放入 `.scripts/` 目录
2. 确保脚本支持 `--help` 参数
3. 添加适当的退出码
4. 在 Makefile 中添加对应的命令
5. 更新本文档

---

*本工具集是 AnalysisDataFlow 项目的一部分，遵循项目整体规范和许可证。*
