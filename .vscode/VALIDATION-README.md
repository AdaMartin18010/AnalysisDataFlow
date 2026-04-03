# AnalysisDataFlow 项目验证脚本使用指南

## 概述

本项目提供三个自动化验证脚本，用于维护文档质量和一致性：

| 脚本 | 功能 | 主要检查项 |
|------|------|-----------|
| `validate-project.py` | 项目完整性验证 | 定理/定义编号格式、重复检测、注册表一致性、链接有效性 |
| `validate-mermaid.py` | Mermaid图表验证 | 语法检查、图表类型统计 |
| `validate-cross-refs.py` | 交叉引用验证 | 文档链接、前置依赖、循环依赖检测 |

## 快速开始

### 在 VS Code 中运行

1. 按 `Ctrl+Shift+P` 打开命令面板
2. 输入 `Tasks: Run Task`
3. 选择以下任务之一：
   - `Validate Project - Full` - 完整项目验证
   - `Validate Mermaid Diagrams` - Mermaid图表验证
   - `Validate Cross References` - 交叉引用验证
   - `Run All Validations` - 运行所有验证

### 命令行运行

```bash
# 项目验证
python .vscode/validate-project.py

# Mermaid验证
python .vscode/validate-mermaid.py

# 交叉引用验证
python .vscode/validate-cross-refs.py

# 运行所有验证
echo "=== 项目验证 ===" && python .vscode/validate-project.py && echo "" && echo "=== Mermaid验证 ===" && python .vscode/validate-mermaid.py && echo "" && echo "=== 交叉引用验证 ===" && python .vscode/validate-cross-refs.py
```

## 脚本详解

### 1. validate-project.py

**功能**：扫描所有 Markdown 文件，验证定理/定义/引理/命题/编号的完整性和一致性。

**检查项**：

- ✅ 编号格式是否符合规范 (`Def-{S|K|F}-数字-数字`)
- ✅ 检测重复编号
- ✅ 检查 THEOREM-REGISTRY.md 中是否有遗漏
- ✅ 检查文档交叉引用链接是否有效

**使用方法**：

```bash
# 基本使用
python .vscode/validate-project.py

# 输出 JSON 格式报告
python .vscode/validate-project.py --json > validation-report.json

# 尝试自动修复部分问题（开发中）
python .vscode/validate-project.py --fix
```

**输出示例**：

```
================================================================================
AnalysisDataFlow 项目验证报告
================================================================================

📊 统计信息:
   扫描文件数: 266
   形式化元素总数: 499

   按类型分布:
      Def: 249
      Thm: 87
      Lemma: 114
      Prop: 43
      Cor: 6

🔍 问题汇总:
   错误: 451
   警告: 866
```

### 2. validate-mermaid.py

**功能**：提取并验证所有 Mermaid 图表的语法。

**检查项**：

- ✅ 图表语法正确性
- ✅ 图表类型统计（graph、flowchart、sequenceDiagram等）
- ✅ 括号匹配检查
- ✅ 节点定义有效性

**使用方法**：

```bash
# 基本使用（基本语法检查，不依赖外部工具）
python .vscode/validate-mermaid.py

# 使用在线API验证（需要网络连接）
python .vscode/validate-mermaid.py --online

# 输出 JSON 格式
python .vscode/validate-mermaid.py --json
```

**安装 mermaid-cli（推荐）**：

```bash
# 使用 npm 安装
npm install -g @mermaid-js/mermaid-cli

# 验证安装
mmdc --version
```

**输出示例**：

```
================================================================================
Mermaid 图表验证报告
================================================================================

📊 统计信息:
   扫描文件数: 284
   Mermaid代码块: 1210
   ✅ 有效: 19
   ❌ 无效: 1191

📈 图表类型分布:
   graph: 651
   flowchart: 325
   sequenceDiagram: 79
   stateDiagram: 54
   ...
```

### 3. validate-cross-refs.py

**功能**：验证文档间的交叉引用和链接。

**检查项**：

- ✅ 相对路径链接有效性
- ✅ 引用的文档是否存在
- ✅ 定理/定义引用是否有对应注册
- ✅ 前置依赖声明的完整性
- ✅ 循环依赖检测

**使用方法**：

```bash
# 基本使用
python .vscode/validate-cross-refs.py

# 输出 JSON 格式
python .vscode/validate-cross-refs.py --json
```

**输出示例**：

```
================================================================================
交叉引用验证报告
================================================================================

📊 统计信息:
   扫描文件数: 275
   总引用数: 6536
   无效链接: 898
   可疑锚点: 5120
   缺失前置依赖: 11
   循环依赖: 0
```

## VS Code 任务配置

`.vscode/tasks.json` 中预定义了以下任务：

| 任务名 | 快捷键 | 说明 |
|--------|--------|------|
| `Validate Project - Full` | - | 完整项目验证 |
| `Validate Project - JSON Output` | - | 输出JSON报告 |
| `Validate Mermaid Diagrams` | - | Mermaid语法验证 |
| `Validate Mermaid - Online` | - | 在线Mermaid验证 |
| `Validate Cross References` | - | 交叉引用验证 |
| `Run All Validations` | - | 运行所有验证 |
| `Generate Validation Report (JSON)` | - | 生成JSON报告文件 |
| `Check Theorem Registry Consistency` | - | 检查注册表一致性 |

## 编号规范

### 定理/定义编号格式

```
{类型}-{阶段}-{文档序号}-{顺序号}
```

**类型**：

- `Def` - 定义
- `Thm` - 定理
- `Lemma` - 引理
- `Prop` - 命题
- `Cor` - 推论

**阶段**：

- `S` - Struct/（形式理论）
- `K` - Knowledge/（知识结构）
- `F` - Flink/（Flink专项）

**示例**：

- `Def-S-01-01` - Struct阶段，01文档，第1个定义
- `Thm-F-02-05` - Flink阶段，02文档，第5个定理
- `Lemma-K-06-03` - Knowledge阶段，06文档，第3个引理

### 在文档中声明形式化元素

```markdown
**Def-S-01-01 (统一流计算元模型 USTM)**.

**Thm-F-02-05 (Checkpoint一致性定理)**: ...

**Lemma-K-06-03 (性能边界引理)**:
```

## CI/CD 集成

可以在 GitHub Actions 或 Azure DevOps 中集成这些验证脚本：

### GitHub Actions 示例

```yaml
name: Documentation Validation

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Run Project Validation
      run: python .vscode/validate-project.py --json > validation-report.json

    - name: Run Cross Reference Validation
      run: python .vscode/validate-cross-refs.py --json > crossrefs-report.json

    - name: Upload Reports
      uses: actions/upload-artifact@v3
      with:
        name: validation-reports
        path: '*.json'
```

## 常见问题

### Q1: 验证报告中的错误都是真实问题吗？

A: 是的，验证脚本发现的错误都是基于实际扫描结果。常见错误类型：

- **无效链接**：文档中引用了不存在的文件
- **未注册元素**：文档中定义了定理/定义，但未在 THEOREM-REGISTRY.md 中注册
- **重复编号**：同一个编号在多个位置使用

### Q2: 如何修复 Mermaid 语法错误？

A:

1. 安装 mermaid-cli 进行更准确的验证
2. 使用 [Mermaid Live Editor](https://mermaid.live/) 在线调试
3. 检查常见错误：括号匹配、节点ID格式、箭头语法

### Q3: 可以自动修复问题吗？

A: 部分问题可以通过 `--fix` 参数自动修复：

- 格式化不规范的编号
- 修复简单的链接路径问题

⚠️ 建议在使用 `--fix` 前备份文件或提交到版本控制。

### Q4: 如何处理大量的注册表缺失警告？

A:

1. 批量更新 THEOREM-REGISTRY.md
2. 使用脚本生成的 JSON 报告定位未注册的元素
3. 建立文档编写规范，要求新建文档时同步更新注册表

## 维护建议

1. **定期运行验证**：建议每次重大更新后运行完整验证
2. **关注错误优先**：优先修复错误级别的问题
3. **逐步减少警告**：警告不会阻止构建，但应该逐步清理
4. **更新注册表**：新增形式化元素时同步更新 THEOREM-REGISTRY.md
5. **使用 JSON 报告**：大型项目中使用 `--json` 输出便于后续处理

## 技术支持

如有问题或建议，请：

1. 检查脚本帮助信息：`python .vscode/validate-project.py --help`
2. 查看项目 AGENTS.md 了解文档规范
3. 参考 THEOREM-REGISTRY.md 了解编号体系
