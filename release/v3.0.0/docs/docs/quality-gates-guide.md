# 质量门禁使用指南

> 所属阶段: CI/CD | 形式化等级: L2 | 版本: 1.0.0

本文档说明 AnalysisDataFlow 项目的自动化质量门禁系统如何工作以及如何使用。

---

## 1. 质量门禁概述

质量门禁系统确保项目文档的持续质量，防止新的链接错误、格式问题和定理编号冲突进入主分支。

### 1.1 检查层级

```
┌─────────────────────────────────────────────────────────┐
│                    质量门禁体系                          │
├─────────────────────────────────────────────────────────┤
│  Level 1: 本地检查 (最快)                                │
│    └── 预提交钩子 → 只检查变更文件                        │
├─────────────────────────────────────────────────────────┤
│  Level 2: PR快速检查 (快速)                              │
│    └── PR自动触发 → 只检查变更文件                        │
├─────────────────────────────────────────────────────────┤
│  Level 3: 完整质量门禁 (全面)                            │
│    └── Push/定时触发 → 全面检查                          │
├─────────────────────────────────────────────────────────┤
│  Level 4: 月度深度检查 (最全面)                          │
│    └── 月度定时触发 → 包含外部链接检查                    │
└─────────────────────────────────────────────────────────┘
```

---

## 2. CI/CD 工作流

### 2.1 工作流文件

| 工作流文件 | 触发条件 | 检查范围 | 预计时间 |
|------------|----------|----------|----------|
| `pr-check.yml` | PR创建/更新 | 变更文件 | <2分钟 |
| `quality-gates.yml` | Push到main/PR/每周日 | 所有文件 | ~5分钟 |
| `link-check.yml` | 每月1日 | 外部链接 | ~30分钟 |

### 2.2 检查项目

| 检查项 | PR检查 | 质量门禁 | 月度检查 | 说明 |
|--------|--------|----------|----------|------|
| 内部链接 | ✅ | ✅ | ✅ | 验证文件引用正确 |
| 锚点检查 | ✅ | ✅ | ✅ | 验证锚点存在 |
| 交叉引用 | ✅ | ✅ | ✅ | 验证文档间引用 |
| 定理编号 | ❌ | ✅ | ✅ | 验证编号唯一性 |
| 外部链接 | ❌ | 可选 | ✅ | 验证HTTP链接 |
| Markdown格式 | ❌ | ✅ | ✅ | 基础格式检查 |
| Mermaid语法 | ❌ | ✅ | ✅ | 图表语法验证 |

---

## 3. 本地检查命令

### 3.1 快速检查（推荐）

检查暂存区和未跟踪的Markdown文件：

```bash
# 基本检查
python .scripts/quick-check.py

# 只检查暂存区文件
python .scripts/quick-check.py --staged-only

# 检查所有文件
python .scripts/quick-check.py --all

# 失败时返回非零退出码
python .scripts/quick-check.py --fail-on-error
```

### 3.2 统一质量检查

```bash
# 基本检查（内部链接+锚点）
python .scripts/quality-gates.py

# 包含外部链接检查（较慢）
python .scripts/quality-gates.py --check-external

# 执行所有检查
python .scripts/quality-gates.py --all

# 严格模式（任何错误都失败）
python .scripts/quality-gates.py --all --fail-threshold 0

# 指定输出报告
python .scripts/quality-gates.py --all --output reports/check.md --json reports/check.json
```

### 3.3 链接健康检查

```bash
# 全量链接检查（包含外部链接）
python .scripts/link_checker.py

# 只检查内部链接
python .scripts/link_checker.py --skip-external

# 生成报告
python .scripts/link_checker.py --output reports/links.md --json reports/links.json
```

### 3.4 交叉引用验证

```bash
# 验证交叉引用
python .scripts/validate_cross_refs.py

# 或使用v2版本
python .scripts/validate_cross_refs_v2.py
```

---

## 4. 预提交钩子

### 4.1 安装预提交钩子

项目已配置预提交钩子，在 `.git/hooks/pre-commit`：

```bash
#!/bin/bash
# 本地提交前快速检查
echo "🔍 运行提交前检查..."

python .scripts/quick-check.py --staged-only --fail-on-error

if [ $? -ne 0 ]; then
    echo "❌ 检查失败，请修复问题后再提交"
    echo ""
    echo "提示:"
    echo "  - 使用 git add 更新修改"
    echo "  - 使用 git commit --no-verify 跳过检查（不推荐）"
    exit 1
fi

echo "✅ 检查通过"
```

### 4.2 手动安装

如果钩子未生效，可以手动创建：

```bash
# 创建钩子文件
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "🔍 运行提交前检查..."
python .scripts/quick-check.py --staged-only --fail-on-error
exit $?
EOF

# 添加执行权限
chmod +x .git/hooks/pre-commit
```

### 4.3 跳过检查（紧急情况）

```bash
# 跳过预提交钩子
git commit --no-verify -m "你的提交信息"

# 或使用简写
git commit -n -m "你的提交信息"
```

> ⚠️ **警告**: 跳过检查应仅在紧急情况下使用，可能引入质量问题。

---

## 5. 常见问题解决

### 5.1 链接检查失败

**问题**: 内部链接检查失败

**解决方案**:

```bash
# 1. 查看详细错误
python .scripts/quick-check.py --fail-on-error

# 2. 修复失效链接
# - 检查文件路径是否正确
# - 确认目标文件是否存在
# - 使用相对路径或绝对路径（以/开头）

# 3. 如果链接正确但检查失败，可能是缓存问题
rm -rf .link-checker-cache
python .scripts/quick-check.py
```

### 5.2 外部链接超时

**问题**: 外部链接检查超时

**解决方案**:

```bash
# 增加超时时间
python .scripts/link_checker.py --timeout 60

# 跳过外部链接检查（仅CI/CD）
python .scripts/quality-gates.py --check-internal --check-anchors
```

### 5.3 定理编号冲突

**问题**: 定理编号重复

**解决方案**:

1. 查看 `THEOREM-REGISTRY.md` 了解编号规则
2. 确保新定理编号全局唯一
3. 格式: `{类型}-{阶段}-{文档序号}-{顺序号}`
   - 类型: Thm/Lemma/Def/Prop/Cor
   - 阶段: S (Struct)/K (Knowledge)/F (Flink)
   - 示例: `Thm-S-01-01`

### 5.4 PR检查超时

**问题**: PR检查超过2分钟

**原因和解决方案**:

1. **变更文件过多**: 分批提交
2. **外部链接检查**: 外部链接检查较慢，仅必要时启用
3. **网络问题**: 重新运行工作流

---

## 6. 配置选项

### 6.1 失败阈值

质量门禁支持配置失败阈值：

```bash
# 严格模式（0个错误即失败）
python .scripts/quality-gates.py --fail-threshold 0

# 宽松模式（允许5个错误）
python .scripts/quality-gates.py --fail-threshold 5

# 最宽松（仅报告）
python .scripts/quality-gates.py --fail-threshold 999
```

### 6.2 检查范围

```bash
# 只检查内部链接
python .scripts/quality-gates.py --check-internal

# 检查内部链接和锚点
python .scripts/quality-gates.py --check-internal --check-anchors

# 完整检查（包含外部链接）
python .scripts/quality-gates.py --all
```

### 6.3 CI/CD 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `CHECK_EXTERNAL` | 检查外部链接 | `false` |
| `STRICT_MODE` | 严格模式 | `false` |
| `FAIL_ON_ERROR` | 错误时失败 | `true` |
| `MAX_CHECK_TIME` | 最大检查时间(秒) | `120` |

---

## 7. 报告解读

### 7.1 快速检查报告

```
======================================================================
📋 快速检查结果
======================================================================

⚠️  发现 3 个问题：

📄 docs/example.md
   [内部链接] [目标文档](./non-existent.md)
   → 文件不存在: non-existent.md

   [锚点] [跳转到章节](#non-existent-section)
   → 锚点不存在: non-existent-section

======================================================================
```

### 7.2 质量门禁报告

报告包含以下部分：

1. **检查摘要** - 总体统计
2. **详细结果** - 每个检查项的状态
3. **错误汇总** - 具体错误列表
4. **建议操作** - 修复建议

### 7.3 JSON 报告

机器可读的JSON报告可用于自动化处理：

```json
{
  "summary": {
    "total_checks": 5,
    "passed": 3,
    "failed": 2,
    "broken_links": 5
  },
  "checks": [
    {
      "name": "内部链接检查",
      "passed": false,
      "error_count": 3,
      "details": [...]
    }
  ]
}
```

---

## 8. 最佳实践

### 8.1 开发流程

```
1. 本地编辑文档
        ↓
2. git add 暂存更改
        ↓
3. 预提交钩子自动检查
   └── 通过 → 继续
   └── 失败 → 修复问题 → 回到步骤2
        ↓
4. git commit 提交
        ↓
5. 推送并创建PR
        ↓
6. PR自动检查
   └── 通过 → 可合并
   └── 失败 → 修复问题 → 推送更新
```

### 8.2 建议

1. **本地优先**: 在提交前运行本地检查
2. **小步快跑**: 小批量提交，减少检查时间
3. **及时修复**: 发现问题立即修复，不要累积
4. **关注报告**: 定期查看月度链接健康报告

### 8.3 链接维护

```bash
# 查看当前链接健康状况
cat reports/link-health-report.md

# 自动修复重定向链接
python .scripts/link_checker.py --auto-fix --dry-run  # 先试运行
python .scripts/link_checker.py --auto-fix            # 实际执行

# 查找Wayback存档
python .scripts/link_checker.py --wayback
```

---

## 9. 故障排除

### 9.1 检查脚本权限

```bash
# 确保脚本可执行
chmod +x .scripts/*.py
```

### 9.2 依赖安装

```bash
# 安装Python依赖
pip install -r .scripts/requirements.txt

# 或安装Node.js依赖（用于markdownlint）
npm install -g markdownlint-cli
```

### 9.3 清理缓存

```bash
# 清理链接检查缓存
rm -rf .link-checker-cache

# 清理所有缓存
rm -rf .link-checker-cache reports/*.json
```

### 9.4 调试模式

```bash
# 启用详细输出
python .scripts/quality-gates.py --all --verbose

# 只检查特定文件
python .scripts/quick-check.py --files "docs/file1.md,docs/file2.md"
```

---

## 10. 相关文档

- [PROJECT-TRACKING.md](../PROJECT-TRACKING.md) - 项目进度跟踪
- [LINK-HEALTH-AUTOMATION.md](../LINK-HEALTH-AUTOMATION.md) - 链接健康自动化
- [THEOREM-REGISTRY.md](../THEOREM-REGISTRY.md) - 定理编号注册表

---

## 11. 引用参考
