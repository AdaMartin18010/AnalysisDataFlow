# CI/CD 工作流文档

本目录包含 AnalysisDataFlow 项目的 CI/CD 流水线配置。

## 工作流概览

| 工作流 | 触发条件 | 用途 |
|--------|----------|------|
| `quality-gate.yml` | PR、Push、手动 | PR质量门禁 |
| `nightly-check.yml` | 定时(每日)、手动 | 夜间维护检查 |
| `release-automation.yml` | Tag推送、手动 | 发布自动化 |
| `formal-verification.yml` | Coq/TLA+变更、定时 | 形式化验证 |
| `dependency-update.yml` | 定时(每周)、手动 | 依赖更新检查 |

---

## 1. Quality Gate (质量门禁)

**文件**: `quality-gate.yml`

### 触发条件

- Pull Request 创建/更新
- 代码推送到 main/master 分支
- 手动触发 (`workflow_dispatch`)

### 质量检查项

| 检查项 | 级别 | 说明 |
|--------|------|------|
| Markdown语法检查 | 🔴 阻塞 | 验证Markdown格式 |
| 交叉引用验证 | 🔴 阻塞 | 验证定理/文档引用 |
| Mermaid语法检查 | 🔴 阻塞 | 验证图表语法 |
| 内部链接检查 | 🔴 阻塞 | 验证文档内链接 |
| 前瞻性内容检查 | 🔴 阻塞 | 验证前瞻性标记 |
| 定理编号唯一性 | 🔴 阻塞 | 验证定理ID不重复 |
| 六段式模板验证 | 🟡 警告 | 检查文档结构 |
| 形式化元素检查 | 🟡 警告 | 检查定理/定义 |

### 使用方式

```bash
# 手动触发
gh workflow run quality-gate.yml

# 指定检查类型
gh workflow run quality-gate.yml -f check_type=quick
```

---

## 2. Nightly Check (夜间检查)

**文件**: `nightly-check.yml`

### 触发条件

- 每天凌晨 2:00 UTC (北京时间 10:00)
- 手动触发

### 任务

1. **外部链接健康检查** - 检查所有外部链接是否可访问
2. **知识图谱更新** - 更新知识图谱数据
3. **文档统计更新** - 统计文档数量、定理数量等
4. **生成夜间报告** - 汇总所有检查结果
5. **发送通知** - 发现问题时创建GitHub Issue

### 使用方式

```bash
# 手动触发全量检查
gh workflow run nightly-check.yml

# 只检查链接
gh workflow run nightly-check.yml -f task_type=links-only
```

---

## 3. Release Automation (发布自动化)

**文件**: `release-automation.yml`

### 触发条件

- Tag推送 (`v*.*.*`)
- 手动触发

### 发布流程

1. 验证版本号格式
2. 运行完整质量检查
3. 生成发布说明 (从CHANGELOG提取)
4. 创建发布包 (tar.gz + zip)
5. 创建GitHub Release
6. 更新PROJECT-TRACKING.md
7. 更新版本文档

### 使用方式

```bash
# 推送Tag触发
 git tag v2.8.0
git push origin v2.8.0

# 手动触发
gh workflow run release-automation.yml -f version=2.8.0
```

---

## 4. Formal Verification (形式化验证)

**文件**: `formal-verification.yml`

### 触发条件

- Coq/TLA+/Lean文件变更
- 每周日凌晨 3:00 UTC
- 手动触发

### 支持的验证工具

| 工具 | 版本 | 用途 |
|------|------|------|
| Coq | 8.17.1 | 定理证明 |
| TLA+ | 1.7.4 | 模型检查 |
| Lean 4 | latest | 定理证明 |

### 使用方式

```bash
# 运行所有验证
gh workflow run formal-verification.yml

# 只验证Coq
gh workflow run formal-verification.yml -f verification_type=coq-only
```

---

## 5. Dependency Update (依赖更新)

**文件**: `dependency-update.yml`

### 触发条件

- 每周一凌晨 4:00 UTC
- 手动触发

### 检查内容

1. **Flink新版本** - 检查Apache Flink最新发布
2. **Python依赖** - 检查requirements.txt更新
3. **Node.js依赖** - 检查package.json更新
4. **创建更新PR** - 自动创建依赖更新PR

### 使用方式

```bash
# 手动触发
gh workflow run dependency-update.yml

# 只检查Flink
gh workflow run dependency-update.yml -f check_type=flink-only
```

---

## 辅助脚本

位于 `.github/action-scripts/` 目录:

| 脚本 | 用途 |
|------|------|
| `quality-score-calculator.py` | 计算质量评分 |
| `pr-comment-generator.py` | 生成PR评论 |
| `notify-slack.sh` | Slack通知 |

---

## 状态徽章

在README.md中添加:

```markdown
![Quality Gate](https://github.com/OWNER/REPO/workflows/Quality%20Gate/badge.svg)
![Nightly Check](https://github.com/OWNER/REPO/workflows/Nightly%20Check/badge.svg)
![Release](https://github.com/OWNER/REPO/workflows/Release%20Automation/badge.svg)
```

---

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `PYTHON_VERSION` | 3.11 | Python版本 |
| `NODE_VERSION` | 20 | Node.js版本 |
| `COQ_VERSION` | 8.17.1 | Coq版本 |

---

## 故障排除

### 工作流运行失败

1. 查看 Actions 页面获取详细日志
2. 下载 Artifacts 查看详细报告
3. 本地运行脚本复现问题:

```bash
# 本地运行质量检查
python .scripts/quality-gates/theorem-uniqueness-checker.py --dirs Struct Knowledge Flink
```

### 通知问题

- GitHub Issue 创建需要 `issues: write` 权限
- Slack 通知需要配置 `SLACK_WEBHOOK` secret

---

## 维护指南

### 更新工作流

1. 修改对应的 `.yml` 文件
2. 在测试分支验证
3. 提交 PR 并通过质量门禁
4. 合并到主分支

### 添加新的质量检查

1. 在 `quality-gate.yml` 中添加新的 job
2. 定义检查级别 (blocking/warning)
3. 在 summary job 中添加汇总逻辑
4. 更新本文档

---

*最后更新: 2026-04-11*
