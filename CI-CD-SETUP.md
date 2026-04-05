# CI/CD 自动化流水线设置指南

> **版本**: v1.0 | **日期**: 2026-04-05 | **状态**: Production

## 📋 概述

本文档介绍 AnalysisDataFlow 项目的 GitHub Actions CI/CD 自动化流水线配置。

## 🎯 工作流概览

### 1. PR Quality Gate (PR质量门禁)

**文件**: `.github/workflows/pr-quality-gate.yml`

**触发条件**:

- Pull Request 创建 (`opened`)
- Pull Request 更新 (`synchronize`)
- Pull Request 重新打开 (`reopened`)

**检查任务**:

| 任务 | 描述 | 工具 |
|------|------|------|
| Markdown Syntax Check | 检查Markdown语法正确性 | markdownlint |
| Theorem Registry Validation | 验证定理编号唯一性 | 自定义Python脚本 |
| Mermaid Syntax Validation | 验证Mermaid图表语法 | Python正则表达式 |
| Internal Link Health Check | 检查内部链接有效性 | Python脚本 |
| Prospective Content Check | 检查前瞻性内容标记 | Python脚本 |

**使用方式**:

```bash
# 本地模拟PR检查
python scripts/ci-check-scripts.py --changed-only --base-ref main

# 详细输出
python scripts/ci-check-scripts.py --verbose
```

### 2. Scheduled Maintenance (定时维护任务)

**文件**: `.github/workflows/scheduled-maintenance.yml`

**触发条件**:

- 定时触发: 每周一凌晨 2:00 UTC (北京时间周一上午10:00)
- 手动触发: 通过 GitHub Actions 界面

**维护任务**:

| 任务 | 描述 | 输出 |
|------|------|------|
| External Link Check | 检查外部链接健康状态 | 链接健康报告 |
| Generate Maintenance Report | 生成维护报告 | maintenance-report.md |
| Create Maintenance Issues | 自动创建维护Issue | GitHub Issue |

**手动触发**:

1. 进入 GitHub 仓库页面
2. 点击 Actions → Scheduled Maintenance
3. 点击 "Run workflow"
4. 选择检查类型: `full`, `links-only`, 或 `stats-only`

### 3. Document Update Sync (文档更新同步)

**文件**: `.github/workflows/doc-update-sync.yml`

**触发条件**:

- Push 到 `main` 或 `master` 分支
- 变更路径为 Markdown 文件或核心目录

**同步任务**:

| 任务 | 描述 | 目标文件 |
|------|------|----------|
| Update PROJECT-TRACKING.md | 自动更新项目统计 | PROJECT-TRACKING.md |
| Update Theorem Registry | 扫描并更新定理注册表 | THEOREM-REGISTRY.md |
| Update Navigation Index | 生成最新导航索引 | NAVIGATION-INDEX.md |
| Update README Badges | 更新README统计徽章 | README.md |

## 🔧 环境要求

### GitHub Actions Runner

- **操作系统**: Ubuntu Latest
- **Python版本**: 3.11
- **Node.js版本**: 20

### 依赖安装

```bash
# Python依赖
pip install aiohttp

# Node.js依赖 (由CI自动安装)
npm install -g markdownlint-cli@0.41.0
npm install -g @mermaid-js/mermaid-cli@10.9.1
```

## 📁 脚本说明

### 1. 定理验证器 (`scripts/theorem-validator.py`)

**功能**:

- 扫描所有Markdown文档中的定理/定义/引理
- 验证编号格式规范
- 检测重复ID
- 验证定理注册表完整性

**使用方法**:

```bash
# 基本验证
python scripts/theorem-validator.py

# 严格模式（发现重复时报错）
python scripts/theorem-validator.py --strict

# 检查注册表完整性
python scripts/theorem-validator.py --check-registry

# 指定输出路径
python scripts/theorem-validator.py --output reports/validation.md
```

### 2. 链接健康检查器 (`scripts/link-health-checker.py`)

**功能**:

- 异步HTTP检查外部链接
- 支持断点续查和缓存
- 分类统计（正常/失效/重定向/超时）
- 生成Markdown和JSON报告

**使用方法**:

```bash
# 基本使用
python scripts/link-health-checker.py

# 指定目录和输出
python scripts/link-health-checker.py --path ./docs --output reports/link-report.md

# 快速模式
python scripts/link-health-checker.py --retries 1 --timeout 15

# 清除缓存
python scripts/link-health-checker.py --clear-cache
```

### 3. CI集成检查脚本 (`scripts/ci-check-scripts.py`)

**功能**:

- 整合所有检查功能
- 支持本地运行和CI环境
- 生成JSON格式报告
- 提供详细或简洁输出模式

**使用方法**:

```bash
# 检查所有文件
python scripts/ci-check-scripts.py

# 只检查变更的文件
python scripts/ci-check-scripts.py --changed-only --base-ref main

# 生成JSON报告
python scripts/ci-check-scripts.py --json reports/ci-check-results.json

# 详细输出
python scripts/ci-check-scripts.py --verbose
```

### 4. 文档关系映射器 (`scripts/doc-relationship-mapper.py`)

**功能**:

- 分析文档间的交叉引用
- 构建文档依赖图
- 检测循环依赖
- 生成文档关系报告

**使用方法**:

```bash
# 基本用法
python scripts/doc-relationship-mapper.py

# 指定输出目录
python scripts/doc-relationship-mapper.py --output ./reports

# 仅检测循环依赖
python scripts/doc-relationship-mapper.py --cycles-only
```

## 🚀 快速开始

### 首次设置

1. **确保文件权限正确**:

   ```bash
   chmod +x scripts/*.py
   ```

2. **测试本地检查**:

   ```bash
   python scripts/ci-check-scripts.py --verbose
   ```

3. **推送到GitHub**:

   ```bash
   git add .github/workflows/
   git add scripts/
   git commit -m "Add CI/CD automation workflows"
   git push origin main
   ```

### 验证工作流

1. 创建一个测试PR
2. 检查 PR Quality Gate 是否运行
3. 查看 GitHub Actions 输出
4. 确认所有检查通过

## 📊 报告输出

### 报告位置

所有报告默认输出到 `reports/` 目录:

| 报告文件 | 来源工作流 | 说明 |
|----------|-----------|------|
| `theorem-validation-report.md` | PR Quality Gate | 定理验证报告 |
| `mermaid-validation-report.md` | PR Quality Gate | Mermaid语法报告 |
| `internal-link-report.md` | PR Quality Gate | 内部链接检查报告 |
| `prospective-content-report.md` | PR Quality Gate | 前瞻性内容检查报告 |
| `external-link-report.md` | Scheduled Maintenance | 外部链接健康报告 |
| `maintenance-report.md` | Scheduled Maintenance | 维护综合报告 |
| `theorem-update-report.md` | Doc Update Sync | 定理更新报告 |

### 查看报告

1. **PR中查看**: 检查完成后，报告作为Artifacts上传
2. **GitHub Actions页面**: 进入具体工作流运行，下载Artifacts
3. **本地查看**: 本地运行脚本后直接在 `reports/` 目录查看

## ⚙️ 配置说明

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `PYTHON_VERSION` | `3.11` | Python版本 |
| `NODE_VERSION` | `20` | Node.js版本 |

### 缓存配置

链接检查器使用缓存避免重复检查:

- **缓存位置**: `.link-checker-cache/`
- **缓存TTL**: 24小时
- **恢复键**: `link-checker-cache-`

### 并发设置

| 任务 | 并发数 | 说明 |
|------|--------|------|
| 外部链接检查 | 30 | 同时检查的链接数 |
| 文档处理 | 10 | 同时处理的文件数 |

## 🔒 权限配置

### GitHub Token权限

工作流使用默认的 `GITHUB_TOKEN`，需要以下权限:

- **contents**: write (用于推送自动更新)
- **issues**: write (用于创建维护Issue)
- **actions**: write (用于上传Artifacts)

### 分支保护规则

建议为主分支配置以下保护规则:

1. **Require status checks to pass**:
   - PR Quality Gate / Markdown Syntax Check
   - PR Quality Gate / Theorem Registry Validation
   - PR Quality Gate / Mermaid Syntax Validation
   - PR Quality Gate / Internal Link Health Check
   - PR Quality Gate / Prospective Content Check

2. **Require branches to be up to date**: 启用

## 🛠️ 故障排除

### 常见问题

#### 1. 工作流运行失败

**症状**: GitHub Actions 显示失败状态

**排查步骤**:

```bash
# 1. 检查本地脚本是否可以运行
python scripts/ci-check-scripts.py --verbose

# 2. 检查文件权限
ls -la scripts/*.py

# 3. 检查依赖安装
pip list | grep -E "aiohttp|regex"
```

#### 2. 链接检查超时

**症状**: 外部链接检查任务超时

**解决方案**:

- 增加 `timeout-minutes` 配置
- 减少并发数 (`--concurrent`)
- 使用缓存避免重复检查

#### 3. 定理验证失败

**症状**: 发现重复定理ID

**解决方案**:

```bash
# 1. 查看详细报告
cat reports/theorem-validation-report.md

# 2. 手动修复重复ID
# 编辑相关文件，确保每个ID唯一
```

#### 4. 自动提交失败

**症状**: Document Update Sync 无法推送更改

**排查步骤**:

1. 检查 `GITHUB_TOKEN` 权限
2. 确认分支保护规则允许GitHub Actions推送
3. 检查是否有冲突需要手动解决

### 调试模式

在本地调试工作流:

```bash
# 使用 act 工具 (https://github.com/nektos/act)
act pull_request -W .github/workflows/pr-quality-gate.yml

# 手动运行单个检查
python scripts/theorem-validator.py --strict --check-registry
```

## 📈 监控和维护

### 监控指标

| 指标 | 目标 | 告警阈值 |
|------|------|----------|
| 外部链接健康度 | >95% | <90% |
| 定理重复率 | 0% | >0% |
| Mermaid错误率 | <1% | >5% |
| 内部链接失效率 | <5% | >10% |

### 定期维护任务

| 频率 | 任务 | 负责人 |
|------|------|--------|
| 每周 | 检查Scheduled Maintenance报告 | 自动化 |
| 每月 | 审查前瞻性内容标记 | 维护团队 |
| 每季度 | 更新CI/CD依赖版本 | DevOps团队 |
| 每年 | 审查和优化工作流配置 | 架构团队 |

## 📝 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-04-05 | 初始版本，包含三个核心工作流 |

## 📚 参考资源

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Project AGENTS.md](./AGENTS.md) - 项目开发规范
- [PROJECT-TRACKING.md](./PROJECT-TRACKING.md) - 项目进度跟踪

---

*本文档由 CI/CD 自动化流水线维护，最后更新: 2026-04-05*
