# GitHub 优化任务跟踪

> 创建日期: 2026-04-08
> 目标: GitHub友好配置
> 预算: ¥0

---

## 任务总览

```
阶段一 - 立即清理 : [░░░░░░░░░░░░░░░░░░░░] 0% (3任务)
阶段二 - CI/CD优化 : [░░░░░░░░░░░░░░░░░░░░] 0% (3任务)
阶段三 - 自动化配置: [░░░░░░░░░░░░░░░░░░░░] 0% (2任务)
```

---

## 阶段一: 立即清理 (今天 - 30分钟)

| # | 任务 | 工时 | 状态 | 命令 |
|---|------|------|------|------|
| 1 | 更新 `.gitignore` | 10min | ⏳ | 文件已创建 |
| 2 | 执行清理脚本 | 5min | ⏳ | `.scripts/cleanup-repo.ps1` |
| 3 | 提交清理commit | 5min | ⏳ | `git add -A && git commit` |

**预计效果**: 清理600-800MB

---

## 阶段二: CI/CD优化 (本周 - 4小时)

| # | 任务 | 工时 | 状态 | 产出 |
|---|------|------|------|------|
| 4 | 优化GitHub Actions | 2h | ⏳ | 合并工作流, 添加缓存 |
| 5 | 配置分支保护 | 30min | ⏳ | main分支保护规则 |
| 6 | 设置Issue/PR模板 | 1h | ⏳ | 简化模板, 添加中文 |

---

## 阶段三: 自动化配置 (下周 - 1小时)

| # | 任务 | 工时 | 状态 | 产出 |
|---|------|------|------|------|
| 7 | 配置Dependabot | 30min | ⏳ | 依赖自动更新 |
| 8 | 配置CodeQL | 30min | ⏳ | 安全扫描 |

---

## 执行命令速查

### 步骤1: 备份

```powershell
git branch backup-20260408
```

### 步骤2: 清理

```powershell
cd e:\_src\AnalysisDataFlow
. .scripts/cleanup-repo.ps1
```

### 步骤3: 提交

```powershell
git add -A
git commit -m "chore: cleanup build artifacts and update .gitignore

- Update .gitignore with comprehensive rules (19 categories)
- Remove Python __pycache__ and .pyc files
- Remove Node.js node_modules and .next build output
- Remove Java Maven target directories
- Remove IDE configuration files
- Remove OS-specific files
- Remove generated JSON data files

Saves ~600-800 MB repository size"

git push origin main
```

---

## 验证清单

### 清理验证

- [ ] `git status` 干净
- [ ] `git log` 显示清理commit
- [ ] GitHub仓库大小减小

### CI/CD验证

- [ ] PR触发CI检查
- [ ] 分支保护生效
- [ ] 合并后自动部署

---

## 发现的问题清单

| 问题 | 位置 | 严重程度 | 解决方案 |
|------|------|----------|----------|
| `__pycache__` | `.scripts/ai-assistant/` | 中 | 清理+忽略 |
| `target/` | `Knowledge/Flink-Scala-Rust-Comprehensive/...` | 高 | 清理+忽略 |
| `.next/` | `learning-platform/` | 高 | 清理+忽略 |
| `node_modules/` | `learning-platform/` | 高 | 清理+忽略 |
| 生成JSON | 根目录/`.scripts/` | 中 | 清理+忽略 |

---

## 预期改善

| 指标 | 当前 | 目标 | 改善 |
|------|------|------|------|
| 仓库大小 | 25.7 MB | ~20 MB | -22% |
| CI时间 | ~15min | ~8min | -47% |
| 克隆时间 | ~30s | ~15s | -50% |

---

**状态**: 🟡 待确认执行
