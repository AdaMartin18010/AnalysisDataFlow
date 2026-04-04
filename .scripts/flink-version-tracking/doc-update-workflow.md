# Flink 版本发布后文档更新流程

> **版本**: v1.0 | **适用**: Flink 2.4/2.5/3.0 发布后文档更新

## 流程概览

版本发布后的文档更新分为3个阶段，目标是在3天内完成所有更新。

```
Day 1: 检测与通知 ──────────────────────────────
  ├── GitHub Actions 自动检测新版本
  ├── 创建 GitHub Issue 跟踪更新任务
  └── 发送 Slack/邮件通知

Day 2: 验证与规划 ──────────────────────────────
  ├── 获取官方 Release Notes
  ├── 对比前瞻文档与实际发布
  ├── 识别差异点
  └── 制定更新计划

Day 3: 执行更新 ────────────────────────────────
  ├── 批量更新状态标记
  ├── 验证配置示例
  ├── 更新 Maven 依赖
  └── 关闭 GitHub Issue
```

## Day 1: 检测与通知

### 自动触发

GitHub Actions 工作流 `.github/workflows/flink-release-tracker.yml` 会自动:

1. 每6小时检查 Maven Central 和 GitHub Releases
2. 发现新版本时:
   - 创建 GitHub Issue (带有 `release-tracking` 标签)
   - 发送 Slack 通知 (如果配置了 `SLACK_WEBHOOK_URL`)
   - 更新 `.tasks/flink-release-tracker.md`

### 手动触发

```bash
# 手动运行检查
gh workflow run flink-release-tracker.yml

# 查看运行状态
gh run list --workflow=flink-release-tracker.yml
```

## Day 2: 验证与规划

### Step 1: 获取官方发布信息

```bash
# 设置版本号
RELEASE_VERSION="2.4.0"

# 获取官方 Release Notes
curl -s https://api.github.com/repos/apache/flink/releases/tags/release-${RELEASE_VERSION} | \
  jq -r '.body' > /tmp/flink-${RELEASE_VERSION}-release-notes.md

# 查看 Maven Central 发布信息
curl -s "https://search.maven.org/solrsearch/select?q=g:org.apache.flink+AND+a:flink-core+AND+v:${RELEASE_VERSION}&rows=5&wt=json" | \
  jq '.response.docs[0]'
```

### Step 2: 对比前瞻文档

使用脚本对比前瞻文档中的特性清单与实际发布:

```bash
cd .scripts/flink-version-tracking

# 生成对比报告
python3 << 'EOF'
import json
import re
from pathlib import Path

release_version = "2.4.0"
major_minor = ".".join(release_version.split(".")[:2])

# 读取所有前瞻文档
docs_dir = Path(f"../../Flink")
preview_docs = list(docs_dir.rglob(f"*{major_minor}*.md"))

print(f"=== 找到 {len(preview_docs)} 个前瞻文档 ===")
for doc in preview_docs:
    print(f"  - {doc}")

# 检查每个文档的状态标记
print("\n=== 文档状态标记检查 ===")
for doc in preview_docs:
    content = doc.read_text(encoding='utf-8')
    status_match = re.search(r'status[:\s]+(\w+)', content)
    status = status_match.group(1) if status_match else "unknown"
    print(f"  {doc.name}: {status}")
EOF
```

### Step 3: 创建更新任务清单

在 GitHub Issue 中添加具体任务:

```markdown
## 更新任务清单

### 状态标记更新
- [ ] `Flink/08-roadmap/flink-2.4-tracking.md`: status: preview → released
- [ ] `Flink/02-core-mechanisms/adaptive-execution-engine-v2.md`: since: 2.4-preview → since: 2.4
- [ ] `Flink/10-deployment/serverless-flink-ga-guide.md`: status: preview → released

### 内容验证
- [ ] 验证 FLIP 实现状态与实际一致
- [ ] 验证配置参数有效性
- [ ] 验证 API 签名正确性

### 示例代码更新
- [ ] 更新所有 Maven 依赖版本号
- [ ] 更新配置示例中的注释标记
- [ ] 验证代码片段语法

### 文档结构
- [ ] 更新发布日期
- [ ] 添加官方发布链接
- [ ] 更新破坏性变更列表
```

## Day 3: 执行更新

### 使用辅助脚本批量更新

```bash
# 设置版本
OLD_VERSION="2.4-preview"
NEW_VERSION="2.4"
GA_DATE="2026-10-15"

# 运行批量更新脚本
cd .scripts/flink-version-tracking
python update-docs-on-release.py \
  --old-version "$OLD_VERSION" \
  --new-version "$NEW_VERSION" \
  --ga-date "$GA_DATE" \
  --dry-run  # 先预览变更

# 确认无误后执行实际更新
python update-docs-on-release.py \
  --old-version "$OLD_VERSION" \
  --new-version "$NEW_VERSION" \
  --ga-date "$GA_DATE"
```

### 手动更新检查清单

#### 1. 更新状态标记

```bash
# 查找所有包含前瞻标记的文档
grep -r "status: preview" Flink/ --include="*.md" | grep -E "(2\.4|2\.5|3\.0)"

# 批量替换状态标记 (谨慎使用)
sed -i 's/status: preview/status: released/g' Flink/08-roadmap/flink-2.4-tracking.md
```

#### 2. 更新版本标记

```bash
# 更新 since 标记
grep -r "since: 2.4-preview" Flink/ --include="*.md"
sed -i 's/since: 2.4-preview/since: 2.4/g' Flink/02-core-mechanisms/adaptive-execution-engine-v2.md
```

#### 3. 更新代码示例中的注释

```bash
# 查找所有前瞻标记的代码注释
grep -rn "\[Flink 2.4 前瞻\]" Flink/ --include="*.md"

# 更新为正式版本标记
sed -i 's/\[Flink 2.4 前瞻\]/[Flink 2.4]/g' Flink/02-core-mechanisms/adaptive-execution-engine-v2.md
```

### 验证更新

```bash
# 1. 检查 Markdown 语法
find Flink/ -name "*.md" -exec markdownlint {} \;

# 2. 验证链接有效性
python ../link-checker/check-links.py --dir Flink/

# 3. 检查形式化元素编号
python ../validate_cross_refs.py --check-theorems
```

## 更新模板

### 文档头部更新模板

**Before (前瞻)**:
```markdown
<!-- 版本状态标记: status=preview, target=2026-Q3-Q4 -->
> ⚠️ **前瞻性声明**
> 本文档包含Flink 2.4的前瞻性设计内容。
> 
> | 属性 | 值 |
> |------|-----|
> | **文档状态** | 🔍 前瞻 (Preview) |
> | **目标版本** | Flink 2.4.0 |
> | **预计发布时间** | 2026 Q3-Q4 |
```

**After (发布后)**:
```markdown
<!-- 版本状态标记: status=released, ga=2026-10-15 -->
> ✅ **版本已发布**
> Flink 2.4.0 已于 2026-10-15 正式发布。
> 
> | 属性 | 值 |
> |------|-----|
> | **文档状态** | ✅ 已更新 (Updated) |
> | **发布版本** | 2.4.0 GA |
> | **发布日期** | 2026-10-15 |
> | **官方发布** | [GitHub Release](https://github.com/apache/flink/releases/tag/release-2.4.0) |
> | **Maven Central** | [flink-core:2.4.0](https://search.maven.org/artifact/org.apache.flink/flink-core/2.4.0) |
```

### 代码示例更新模板

**Before**:
```xml
<!-- [Flink 2.4 前瞻] 版本号尚未发布 -->
<version>2.4.0</version>
```

**After**:
```xml
<!-- [Flink 2.4] GA版本 -->
<version>2.4.0</version>
```

## 质量门禁

更新完成后必须通过以下检查:

1. **形式化元素完整性**
   - [ ] 所有 `Def-*` 定义存在
   - [ ] 所有 `Thm-*` 定理存在
   - [ ] 编号格式正确

2. **引用有效性**
   - [ ] 内部链接可访问
   - [ ] 外部链接有效
   - [ ] 引用文献完整

3. **代码示例**
   - [ ] XML 语法正确
   - [ ] Java 语法正确
   - [ ] YAML 语法正确

4. **版本标记一致性**
   - [ ] 所有前瞻标记已更新
   - [ ] 状态标记一致
   - [ ] 发布日期准确

## 提交与关闭

```bash
# 提交所有更新
git add -A
git commit -m "docs: 更新 Flink 2.4.0 发布后文档

- 更新版本状态标记: preview → released
- 更新代码示例版本标记
- 添加官方发布链接
- 更新发布日期

Fixes #<issue-number>"

git push
```

在 GitHub Issue 中:
1. 勾选所有完成的任务
2. 添加关闭评论
3. 关闭 Issue

---

*此流程由自动化系统辅助执行*
