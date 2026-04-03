# VSCode/Cursor 配置说明


## 目录

- [VSCode/Cursor 配置说明](#vscodecursor-配置说明)
  - [目录](#目录)
  - [自动 Markdown 格式化配置](#自动-markdown-格式化配置)
  - [📦 需要安装的扩展](#-需要安装的扩展)
  - [⚙️ 配置文件说明](#️-配置文件说明)
    - [`settings.json`](#settingsjson)
    - [`.markdownlint.json`](#markdownlintjson)
  - [🚀 使用方法](#-使用方法)
    - [自动格式化](#自动格式化)
    - [手动格式化](#手动格式化)
    - [查看和修复 Linter 错误](#查看和修复-linter-错误)
  - [🎯 快捷键](#-快捷键)
  - [📝 规则说明](#-规则说明)
    - [允许的格式](#允许的格式)
    - [自动修复的问题](#自动修复的问题)
  - [🔧 自定义配置](#-自定义配置)
  - [🐛 故障排除](#-故障排除)
    - [格式化不生效](#格式化不生效)
    - [某些规则想要禁用](#某些规则想要禁用)
    - [某个文件想要跳过检查](#某个文件想要跳过检查)
  - [📄 PDF 导出功能](#-pdf-导出功能)
    - [PDF 导出文件](#pdf-导出文件)
    - [快速使用](#快速使用)
  - [🔍 文档差异分析工具](#-文档差异分析工具)
    - [功能特性](#功能特性)
    - [使用方法](#使用方法)
    - [命令行参数](#命令行参数)
    - [报告输出](#报告输出)
    - [在CI/CD中使用](#在cicd中使用)
  - [📚 参考文档](#-参考文档)

---


## 自动 Markdown 格式化配置

本目录包含 VSCode/Cursor 的配置文件，用于在保存 Markdown 文件时自动格式化。

## 📦 需要安装的扩展

打开 Cursor/VSCode 后，会自动提示安装推荐的扩展，或者手动安装：

1. **Markdownlint** (必需)
   - ID: `DavidAnson.vscode-markdownlint`
   - 功能：Markdown 格式检查和自动修复

2. **Markdown All in One** (推荐)
   - ID: `yzhang.markdown-all-in-one`
   - 功能：TOC 生成、快捷键、列表自动续写等

## ⚙️ 配置文件说明

### `settings.json`

主要配置：

- ✅ 保存时自动格式化 Markdown
- ✅ 自动删除行尾空格
- ✅ 文件末尾自动添加新行
- ✅ 允许使用 HTML 标签（`<details>`, `<summary>` 等）
- ✅ 允许同级标题重复

### `.markdownlint.json`

Markdownlint 规则配置（项目根目录）：

- MD033: false - 允许内联 HTML
- MD024: siblings_only - 允许非同级标题重复
- MD013: false - 不限制行长度
- MD012: false - 允许多个空行

## 🚀 使用方法

### 自动格式化

1. 打开任意 Markdown 文件
2. 修改内容
3. 按 `Ctrl+S` (Windows) 或 `Cmd+S` (Mac) 保存
4. 文件会自动格式化

### 手动格式化

- **格式化整个文档**: `Shift+Alt+F` (Windows) / `Shift+Option+F` (Mac)
- **格式化选中内容**: 选中文本后右键 → "Format Selection"

### 查看和修复 Linter 错误

1. 打开 Markdown 文件
2. 查看编辑器中的波浪线提示
3. 点击灯泡图标 💡 查看快速修复选项
4. 或在命令面板中运行: `Markdownlint: Fix all supported markdownlint violations in document`

## 🎯 快捷键

| 功能 | Windows/Linux | Mac |
|------|--------------|-----|
| 保存并格式化 | `Ctrl+S` | `Cmd+S` |
| 格式化文档 | `Shift+Alt+F` | `Shift+Option+F` |
| 修复所有错误 | `Ctrl+Shift+P` → "Fix all" | `Cmd+Shift+P` → "Fix all" |

## 📝 规则说明

### 允许的格式

```markdown
<!-- ✅ 允许使用 HTML -->
<details>
<summary>点击展开</summary>
内容
</details>

<!-- ✅ 允许重复标题（不同章节） -->
## 概述
### 示例
## 实现
### 示例  <!-- 允许，因为不是同级 -->

<!-- ✅ 允许长行（代码块、链接等） -->
这是一个很长很长很长的行...
```

### 自动修复的问题

- ❌ 行尾空格 → ✅ 自动删除
- ❌ 缺少文件末尾新行 → ✅ 自动添加
- ❌ 不一致的列表缩进 → ✅ 自动修正
- ❌ 代码块缺少语言标识 → ✅ 自动添加空标识

## 🔧 自定义配置

如果需要修改规则，编辑以下文件：

- **VSCode 设置**: `.vscode/settings.json`
- **Markdownlint 规则**: `.markdownlint.json`（项目根目录）

## 🐛 故障排除

### 格式化不生效

1. 确认已安装 Markdownlint 扩展
2. 重新加载窗口: `Ctrl+Shift+P` → "Reload Window"
3. 检查输出面板: `Ctrl+Shift+U` → 选择 "Markdownlint"

### 某些规则想要禁用

在 `.markdownlint.json` 中设置为 `false`:

```json
{
  "MD规则编号": false
}
```

### 某个文件想要跳过检查

在文件开头添加注释：

```markdown
<!-- markdownlint-disable -->
文件内容
<!-- markdownlint-enable -->
```

或禁用特定规则：

```markdown
<!-- markdownlint-disable MD033 -->
<details>内容</details>
<!-- markdownlint-enable MD033 -->
```

## 📄 PDF 导出功能

本项目支持将 Markdown 文档导出为 PDF 格式，便于离线阅读和分享。

### PDF 导出文件

| 文件 | 说明 |
|------|------|
| `export-to-pdf.py` | PDF 导出主脚本 |
| `pdf-config.yaml` | PDF 导出配置 |
| `pdf-template.tex` | LaTeX 模板 |

### 快速使用

```bash
# 检查环境
make check

# 导出单个文件
make pdf-single FILE=README.md

# 批量导出目录
make pdf-batch DIR=Struct/

# 导出完整项目
make pdf-full
```

更多详情请参阅项目根目录的 `PDF-EXPORT-GUIDE.md`。

---

## 🔍 文档差异分析工具

`doc-diff.py` 是一个用于分析文档变更的专业工具，可以检测变更、分析影响、检查质量回归，并生成合并建议。

### 功能特性

1. **文档变更检测** - 比较文档版本差异，识别新增/删除/修改的定理和定义
2. **交叉引用影响分析** - 检测文档变更对其他文档的影响
3. **变更分类统计** - 按类型分类变更，统计变更规模
4. **质量回归检测** - 检测链接破坏、定理编号冲突、格式规范
5. **合并建议生成** - 分析PR变更，生成合并建议，识别潜在冲突

### 使用方法

```bash
# 分析两个提交之间的差异
python .vscode/doc-diff.py --base main --head feature-branch

# 分析暂存区的变更
python .vscode/doc-diff.py --staged

# 分析指定文件
python .vscode/doc-diff.py --files Struct/01-foundation/01.01-ustm.md

# 输出JSON格式报告
python .vscode/doc-diff.py --base HEAD~1 --head HEAD --json

# 跳过影响分析（加快分析速度）
python .vscode/doc-diff.py --base main --head HEAD --no-impact
```

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--base` | 基准引用 | `HEAD` |
| `--head` | 目标引用 | 工作目录 |
| `--staged` | 分析暂存区变更 | - |
| `--files` | 分析指定文件 | - |
| `--json` | 输出JSON格式 | - |
| `--no-impact` | 跳过影响分析 | - |
| `--root` | 项目根目录 | `.` |

### 报告输出

工具会生成详细的分析报告，包括：

- 📊 变更统计（文件数、元素数、按类型/阶段分布）
- 🧮 形式化元素变更详情
- 🔗 交叉引用影响分析
- ⚠️ 质量问题检测
- 💡 合并建议
- 📝 变更日志建议

### 在CI/CD中使用

工具返回适当的退出码：

- `0` - 建议合并（无严重问题）
- `1` - 建议阻止合并（存在严重问题）

示例 GitHub Actions 工作流：

```yaml
- name: Analyze Documentation Changes
  run: |
    python .vscode/doc-diff.py --base origin/main --head HEAD
```

## 📚 参考文档

- [Markdownlint 规则列表](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
- [VSCode Markdown 支持](https://code.visualstudio.com/docs/languages/markdown)
- [PDF 导出指南](../PDF-EXPORT-GUIDE.md)
