# CI/CD 质量门禁指南

> **版本**: v2.0 | **日期**: 2026-04-08 | **状态**: Production

## 📋 概述

本文档详细介绍 AnalysisDataFlow 项目的 CI/CD 质量门禁系统，包括所有检查项的说明、级别配置、故障排查方法以及维护指南。

## 🎯 质量门禁矩阵

| 检查项 | 级别 | 目标状态 | 实现方式 | 触发条件 |
|--------|------|----------|----------|----------|
| Markdown语法检查 | 🔴 阻塞合并 | ✅ 生产 | markdownlint | PR创建/更新 |
| 定理编号唯一性 | 🔴 阻塞合并 | ✅ 生产 | theorem-uniqueness-checker.py | PR创建/更新 |
| 交叉引用完整性 | 🔴 阻塞合并 | ✅ 生产 | validate-cross-refs.py | PR创建/更新 |
| Mermaid语法验证 | 🔴 阻塞合并 | ✅ 生产 | mermaid-syntax-validator.py | PR创建/更新 |
| 内部链接健康检查 | 🔴 阻塞合并 | ✅ 生产 | link-health-checker.py | PR创建/更新 |
| 前瞻性内容标记 | 🔴 阻塞合并 | ✅ 生产 | check_prospective_content.py | PR创建/更新 |
| 外部链接有效性 | 🟢 通知 | ✅ 生产 | link-health-checker.py | 每日定时 |
| 六段式模板结构 | 🟡 警告 | ✅ 生产 | template-structure-checker.py | PR创建/更新 |
| 形式化元素完整性 | 🟡 警告 | ✅ 生产 | formal-element-checker.py | PR创建/更新 |

> **覆盖率**: 100% (9/9 检查项已上线)

## 🔴 阻塞级别检查项

### 1. Markdown语法检查

**工作流**: `pr-quality-gate.yml` → `markdown-lint`

**检查内容**:

- YAML frontmatter 格式正确性
- 表格语法完整性
- Markdown 标准规范

**故障排查**:

```bash
# 本地运行检查
npm install -g markdownlint-cli@0.41.0
markdownlint your-file.md

# 查看详细错误
markdownlint your-file.md --config .markdownlint.json
```

**常见错误**:

| 错误 | 解决方案 |
|------|----------|
| YAML frontmatter 格式错误 | 确保 `---` 开头和结尾 |
| 表格分隔符不完整 | 检查 `|---|---|` 格式 |
| 标题层级跳跃 | 使用连续的 `#` 层级 |

### 2. 定理编号唯一性验证

**工作流**: `pr-quality-gate.yml` → `theorem-validate`

**检查内容**:

- 全局定理编号唯一性
- PR 中新定理不与现有定理冲突
- 格式规范: `Type-Stage-DocNum-SeqNum`

**故障排查**:

```bash
# 本地运行检查
python .scripts/quality-gates/theorem-uniqueness-checker.py --strict

# 查看重复定理
python scripts/theorem-validator.py --strict
```

**修复步骤**:

1. 查看报告 `reports/theorem-uniqueness-report.md`
2. 定位重复的定理ID
3. 修改为新编号（遵循命名规范）
4. 更新 THEOREM-REGISTRY.md

### 3. 交叉引用完整性检查

**工作流**: `pr-quality-gate.yml` → `cross-ref-check`

**检查内容**:

- 文档间链接有效性
- 定理引用正确性
- 内部路径有效性

**故障排查**:

```bash
# 检查内部链接
python scripts/link-health-checker.py --path . --output reports/link-report.md
```

**常见错误**:

| 错误 | 解决方案 |
|------|----------|
| 引用的文档不存在 | 创建文档或更新链接 |
| 相对路径错误 | 使用正确的 `./` 或 `../` 路径 |
| 定理ID拼写错误 | 核对 THEOREM-REGISTRY.md |

### 4. Mermaid语法验证

**工作流**: `pr-quality-gate.yml` → `mermaid-validate`

**检查内容**:

- 图表类型有效性
- 方向定义（graph TD/TB/LR/RL）
- 括号匹配
- 引号配对

**故障排查**:

```bash
# 本地验证
python .scripts/quality-gates/mermaid-syntax-validator.py --strict

# 使用Mermaid CLI
npm install -g @mermaid-js/mermaid-cli@10.9.1
mmdc -i diagram.mmd -o output.svg
```

**常见错误**:

| 错误 | 解决方案 |
|------|----------|
| Unknown chart type | 使用支持的类型: graph/flowchart/sequenceDiagram |
| Missing direction | 添加 TD/TB/LR/RL 方向 |
| Unbalanced brackets | 检查 `[]` `{}` `()` 配对 |

### 5. 内部链接健康检查

**工作流**: `pr-quality-gate.yml` → `internal-link-check`

**检查内容**:

- 内部文档链接有效性
- 相对路径正确性
- 损坏率阈值: <3%

**故障排查**:

```bash
# 本地检查内部链接
python << 'PYEOF'
import re
from pathlib import Path

# 检查特定文件
file_path = "your-file.md"
content = Path(file_path).read_text(encoding='utf-8')
links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)

for text, link in links:
    if not link.startswith(('http://', 'https://', '#')):
        print(f"Link: {link}")
PYEOF
```

### 6. 前瞻性内容标记检查

**工作流**: `pr-quality-gate.yml` → `prospective-content-check`

**检查内容**:

- 前瞻性内容必须有明确标记
- 虚构API需要注释说明
- 版本规划内容需要兼容性说明

**正确示例**:

```markdown
> ⚠️ **前瞻性声明**
> 以下内容涉及尚未发布的 Flink 2.4 功能，仅作参考。

<!-- 虚构API: 此API为概念设计，尚未实现 -->
```java
CREATE AGENT ...
```

```

**故障排查**:
```bash
# 检查前瞻性标记
python scripts/add-prospective-banners.py --check-only
```

## 🟡 警告级别检查项

### 7. 六段式模板结构检查

**工作流**: `pr-quality-gate.yml` → `template-structure-check`

**检查内容**:

- 必需章节存在性
- 元数据完整性
- 内容长度合理性

**六段式模板**:

```markdown
# 标题

> 所属阶段: Struct/Knowledge/Flink
> 前置依赖: [文档链接]
> 形式化等级: L1-L6

## 1. 概念定义 (Definitions)
## 2. 属性推导 (Properties)
## 3. 关系建立 (Relations) [可选]
## 4. 论证过程 (Argumentation) [可选]
## 5. 形式证明 / 工程论证 (Proof)
## 6. 实例验证 (Examples)
## 7. 可视化 (Visualizations)
## 8. 引用参考 (References)
```

**故障排查**:

```bash
# 本地检查模板结构
python .scripts/quality-gates/template-structure-checker.py
```

### 8. 形式化元素完整性检查

**工作流**: `pr-quality-gate.yml` → `formal-element-check`

**检查内容**:

- 形式化元素定义格式
- 元素与章节的匹配性
- 引用格式规范

**故障排查**:

```bash
# 本地检查
python .scripts/formal-element-checker.py --warning
```

## 🟢 通知级别检查项

### 9. 外部链接有效性检查

**工作流**: `link-checker.yml`

**触发**: 每日 01:00 UTC (北京时间 09:00)

**检查内容**:

- 外部HTTP链接有效性
- 重定向链接检测
- 超时链接识别

**通知方式**:

- 发现失效链接时自动创建/更新 GitHub Issue
- 包含详细的失效链接报告

**故障排查**:

```bash
# 本地运行外部链接检查
pip install aiohttp
python scripts/link-health-checker.py \
  --path . \
  --output reports/external-link-report.md \
  --timeout 30 \
  --retries 2
```

**自动修复**:

```bash
# 自动修复重定向链接
python scripts/link-auto-fix.py --fix-redirects
```

## 🛠️ 故障排查手册

### 通用排查流程

```bash
# 1. 确定失败的检查项
# 查看 GitHub Actions 输出

# 2. 下载详细报告
# Actions → 具体工作流运行 → Artifacts

# 3. 本地复现问题
# 根据上文章节运行对应的本地检查命令

# 4. 修复问题并验证
# 修改文件后重新运行本地检查

# 5. 提交修复
# 推送后等待 CI 重新运行
```

### 快速修复命令

```bash
# 修复所有检查
python scripts/ci-check-scripts.py --verbose

# 自动修复链接
python scripts/link-auto-fix.py --fix-redirects
python scripts/link-quick-fix.py

# 添加前瞻性标记
python scripts/add-prospective-banners.py

# 更新定理注册表
python scripts/update_registry_v4.py
```

### 常见CI失败场景

#### 场景1: 定理编号重复

```
❌ Duplicate theorem ID found: Thm-S-01-05
   Found in: Struct/1.1-topic.md, Struct/1.2-other.md
```

**解决方案**:

1. 检查两个文件中 `Thm-S-01-05` 的定义
2. 将其中一个修改为新的唯一编号
3. 更新引用该定理的其他文档

#### 场景2: Mermaid语法错误

```
❌ Syntax error in: docs/example.md (diagram 2)
   Message: Unbalanced brackets
```

**解决方案**:

1. 打开文档找到对应图表
2. 检查 `[]` `{}` `()` 是否配对
3. 使用 Mermaid Live Editor 验证: <https://mermaid.live>

#### 场景3: 内部链接损坏

```
❌ Broken link rate 5.2% exceeds threshold (3%)
```

**解决方案**:

1. 下载 `internal-link-report.md`
2. 找到损坏的链接
3. 修复路径或创建目标文档

#### 场景4: 缺失前瞻性标记

```
❌ Errors (missing prospective markers):
  - Flink/roadmap-2.4.md: Missing prospective content marker
```

**解决方案**:

```markdown
在文档开头添加:
> ⚠️ **前瞻性声明**
> 本文档内容基于尚未发布的功能规划，可能会有变更。
```

## 📊 监控和度量

### 关键指标

| 指标 | 目标 | 告警阈值 |
|------|------|----------|
| CI 成功率 | >95% | <90% |
| 外部链接健康度 | >95% | <90% |
| 定理重复率 | 0% | >0% |
| Mermaid错误率 | <1% | >5% |
| 内部链接失效率 | <3% | >10% |

### 查看报告

所有报告可在 GitHub Actions 运行页面下载:

1. 进入仓库 Actions 页面
2. 选择对应的工作流运行
3. 滚动到 Artifacts 部分
4. 下载所需报告

### 报告位置

```
reports/
├── theorem-uniqueness-report.md
├── mermaid-validation-report.md
├── mermaid-validation-results.json
├── template-structure-report.md
├── internal-link-report.md
├── prospective-content-report.md
├── cross-reference-report.md
├── formal-element-check-report.md
├── external-link-report.md (每日生成)
└── maintenance-report.md (每周生成)
```

## 🔧 配置和维护

### 调整检查阈值

编辑对应的工作流文件 (`.github/workflows/*.yml`):

```yaml
# 例如修改 Mermaid 错误率阈值
python .scripts/quality-gates/mermaid-syntax-validator.py \
  --strict \
  --threshold 0.10  # 改为 10%
```

### 添加新的检查项

1. 创建检查脚本到 `.scripts/quality-gates/`
2. 在 `pr-quality-gate.yml` 中添加新的 job
3. 更新本指南文档
4. 设置适当的级别 (BLOCKING/WARNING/NOTICE)

### 禁用特定检查

**不推荐**，但紧急情况下可以:

```yaml
# 在对应 job 中添加
continue-on-error: true
```

## 📚 相关文档

- [CI-CD-SETUP.md](./CI-CD-SETUP.md) - CI/CD 基础设置
- [AGENTS.md](./AGENTS.md) - 项目开发规范
- [PROJECT-TRACKING.md](./PROJECT-TRACKING.md) - 项目进度跟踪
- [THEOREM-REGISTRY.md](./THEOREM-REGISTRY.md) - 定理注册表

## 📝 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.0 | 2026-04-08 | P1-2 完成: 100% 覆盖率, 9项检查上线 |
| v1.1 | 2026-04-05 | 新增形式化元素检查、交叉引用检查 |
| v1.0 | 2026-04-02 | 初始版本, 6项基础检查 |

---

*本指南由 CI/CD 质量门禁系统自动维护*
*最后更新: 2026-04-08*
