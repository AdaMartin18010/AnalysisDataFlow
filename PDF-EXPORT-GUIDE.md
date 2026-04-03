# AnalysisDataFlow PDF 导出指南

> **本文档介绍如何将 Markdown 文档导出为 PDF 格式**

---

## 目录

1. [环境准备](#1-环境准备)
2. [快速开始](#2-快速开始)
3. [使用说明](#3-使用说明)
4. [自定义样式](#4-自定义样式)
5. [故障排除](#5-故障排除)

---

## 1. 环境准备

### 1.1 必需依赖

PDF 导出功能需要以下工具：

| 工具 | 用途 | 安装命令 |
|------|------|----------|
| **Python 3.8+** | 运行导出脚本 | 已随系统安装 |
| **Pandoc** | Markdown 到 LaTeX 转换 | 见下方说明 |
| **XeLaTeX** | PDF 生成 | 见下方说明 |

#### 安装 Pandoc

**macOS:**

```bash
brew install pandoc
```

**Windows:**

```powershell
# 使用 Chocolatey
choco install pandoc

# 或从官网下载安装包
# https://pandoc.org/installing.html
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt-get update
sudo apt-get install pandoc
```

#### 安装 TeX Live (含 XeLaTeX)

**macOS:**

```bash
brew install --cask mactex
# 或基础版
brew install --cask mactex-no-gui
```

**Windows:**

```powershell
# 使用 Chocolatey
choco install miktex

# 或下载 TeX Live
# https://tug.org/texlive/
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt-get install texlive-xetex texlive-lang-chinese \
    texlive-fonts-recommended texlive-latex-extra
```

### 1.2 可选依赖

| 工具 | 用途 | 安装命令 |
|------|------|----------|
| **Mermaid CLI** | 渲染 Mermaid 图表 | `npm install -g @mermaid-js/mermaid-cli` |

安装 Mermaid CLI（需要 Node.js）：

```bash
npm install -g @mermaid-js/mermaid-cli
```

### 1.3 检查环境

安装完成后，运行以下命令检查环境：

```bash
# 使用 Python 脚本检查
python .vscode/export-to-pdf.py check

# 或手动检查
pandoc --version
xelatex --version
mmdc --version  # 可选
```

---

## 2. 快速开始

### 2.1 单文档导出

导出单个 Markdown 文件：

```bash
# 基本用法
make pdf-single FILE=README.md

# 使用 Python 脚本
python .vscode/export-to-pdf.py single README.md

# 指定输出文件名
python .vscode/export-to-pdf.py single Struct/00-INDEX.md -o struct-index.pdf
```

### 2.2 批量导出

导出整个目录：

```bash
# 基本用法
make pdf-batch DIR=Struct/

# 使用 Python 脚本
python .vscode/export-to-pdf.py batch Struct/

# 指定输出目录
python .vscode/export-to-pdf.py batch Knowledge/ -o ./my-pdfs/
```

### 2.3 导出完整项目

导出所有文档：

```bash
# 使用 Make
make pdf-full

# 使用 Python 脚本
python .vscode/export-to-pdf.py full
```

导出结果将保存在 `pdf-output/` 目录：

```
pdf-output/
├── Struct/
│   ├── 01-foundation/
│   │   └── *.pdf
│   └── Struct-Complete.pdf
├── Knowledge/
│   └── ...
└── Flink/
    └── ...
```

---

## 3. 使用说明

### 3.1 命令行接口

```
用法: python .vscode/export-to-pdf.py [命令] [选项]

命令:
  single    导出单个 Markdown 文件
  batch     批量导出目录
  merge     合并多个文件导出
  full      导出完整项目
  check     检查依赖环境

全局选项:
  -h, --help  显示帮助信息
```

### 3.2 单文档导出

```bash
python .vscode/export-to-pdf.py single <input.md> [选项]

选项:
  -o, --output <file>    指定输出文件路径
  --no-mermaid          不渲染 Mermaid 图表
```

**示例:**

```bash
# 导出 README
python .vscode/export-to-pdf.py single README.md

# 导出指定文件并命名
python .vscode/export-to-pdf.py single Struct/00-INDEX.md -o index.pdf
```

### 3.3 批量导出

```bash
python .vscode/export-to-pdf.py batch <目录> [选项]

选项:
  -o, --output <dir>     指定输出目录
  -p, --pattern <glob>   文件匹配模式 (默认: *.md)
  --flat                 平铺输出，不保留目录结构
```

**示例:**

```bash
# 导出 Struct 目录所有文档
python .vscode/export-to-pdf.py batch Struct/

# 只导出特定模式的文件
python .vscode/export-to-pdf.py batch Struct/ -p "*-deep-dive.md"

# 平铺输出到单个目录
python .vscode/export-to-pdf.py batch Struct/ -o ./flat-output/ --flat
```

### 3.4 合并导出

将多个 Markdown 文件合并为一个 PDF：

```bash
python .vscode/export-to-pdf.py merge <文件1> <文件2> ... [选项]

选项:
  -o, --output <file>    输出文件路径 (必需)
  --no-page-break       文档间不添加分页
```

**示例:**

```bash
# 合并多个文件
python .vscode/export-to-pdf.py merge \
    Struct/01-foundation/*.md \
    -o foundation-complete.pdf

# 合并特定文件
python .vscode/export-to-pdf.py merge \
    README.md \
    Struct/00-INDEX.md \
    Knowledge/00-INDEX.md \
    -o overview.pdf
```

### 3.5 完整项目导出

```bash
python .vscode/export-to-pdf.py full
```

这将：

1. 分别导出 `Struct/`、`Knowledge/`、`Flink/` 三个目录
2. 为每个目录生成合并版 PDF
3. 保留原始目录结构

---

## 4. 自定义样式

### 4.1 配置文件

PDF 导出的配置保存在 `.vscode/pdf-config.yaml`，可修改：

```yaml
# 页面设置
page:
  size: a4                    # 页面大小: a4, letter, a5
  margin:
    top: 25
    bottom: 25
    left: 30
    right: 25

# 字体设置
fonts:
  chinese:
    main: "Source Han Serif SC"    # 思源宋体
    sans: "Source Han Sans SC"     # 思源黑体

# 目录设置
table_of_contents:
  enabled: true
  depth: 3                    # 目录深度 1-4

# 代码块样式
code_blocks:
  highlight_theme: tango      # 语法高亮主题
  line_numbers: true          # 显示行号
```

### 4.2 LaTeX 模板

高级样式定制可修改 `.vscode/pdf-template.tex`：

- **颜色定义**: 修改 `\definecolor` 定义项目品牌色
- **页眉页脚**: 修改 `\fancyhead` 和 `\fancyfoot` 设置
- **定理框**: 修改 `\newtcolorbox` 定义不同框样式
- **代码样式**: 修改 `\lstset` 配置代码块外观

### 4.3 常用自定义示例

#### 修改主色调

编辑 `.vscode/pdf-template.tex`：

```latex
\definecolor{ADFPrimary}{HTML}{1565C0}    % 改为你的主色
\definecolor{ADFSecondary}{HTML}{2E7D32}  % 改为你的次色
```

#### 修改页眉文本

编辑 `.vscode/pdf-template.tex`：

```latex
\fancyhead[L]{\small\textcolor{ADFGray}{你的项目名称}}
\fancyhead[R]{\small\textcolor{ADFGray}{\leftmark}}
```

#### 添加水印（可选）

在 `.vscode/pdf-template.tex` 的导言区添加：

```latex
\usepackage{draftwatermark}
\SetWatermarkText{DRAFT}
\SetWatermarkScale{0.3}
\SetWatermarkColor{gray!30}
```

---

## 5. 故障排除

### 5.1 常见问题

#### Q: 导出失败，提示 "pandoc: command not found"

**A:** 确保 Pandoc 已安装并在 PATH 中：

```bash
# 检查安装
which pandoc

# 重新安装
# macOS
brew install pandoc

# Windows
choco install pandoc
```

#### Q: 提示 "xelatex: command not found"

**A:** 安装 TeX Live 或 MiKTeX：

```bash
# macOS
brew install --cask mactex-no-gui

# Windows
choco install miktex

# Linux
sudo apt-get install texlive-xetex
```

#### Q: 中文字体缺失或显示为方框

**A:** 安装思源字体：

```bash
# macOS
brew install --cask font-source-han-serif
brew install --cask font-source-han-sans

# 或手动下载
# https://github.com/adobe-fonts/source-han-serif/releases
# https://github.com/adobe-fonts/source-han-sans/releases
```

#### Q: Mermaid 图表未渲染

**A:** 安装 Mermaid CLI：

```bash
npm install -g @mermaid-js/mermaid-cli
```

或在导出时跳过 Mermaid：

```bash
python .vscode/export-to-pdf.py single file.md --no-mermaid
```

#### Q: 表格显示不正确

**A:** 确保表格使用标准 Markdown 语法：

```markdown
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| A   | B   | C   |
| D   | E   | F   |
```

#### Q: 代码块语法高亮不正确

**A:** 确保代码块指定了语言：

```markdown
```python
def hello():
    print("Hello")
```

```

### 5.2 错误代码参考

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `File not found` | 输入文件不存在 | 检查文件路径 |
| `Permission denied` | 无写入权限 | 检查输出目录权限 |
| `Missing font` | 字体未安装 | 安装缺失字体 |
| `Out of memory` | 文档过大 | 分批导出 |
| `Mermaid render failed` | 图表语法错误 | 检查 Mermaid 语法 |

### 5.3 调试模式

获取详细错误信息：
```bash
# 查看完整 pandoc 输出
pandoc input.md --pdf-engine=xelatex -o output.pdf --verbose

# 查看 LaTeX 编译日志
pandoc input.md --pdf-engine=xelatex -o output.pdf 2>&1 | tee log.txt
```

### 5.4 获取帮助

如仍有问题，请：

1. 运行环境检查: `python .vscode/export-to-pdf.py check`
2. 查看详细错误输出
3. 检查输入 Markdown 文件语法
4. 尝试简化文档进行测试

---

## 附录

### A. 支持的语法高亮语言

Pandoc 支持以下语言的语法高亮：

- 编程语言: python, java, scala, go, rust, cpp, c, javascript, typescript
- 标记语言: markdown, yaml, json, xml, html, latex
- 配置语言: bash, powershell, dockerfile, makefile
- 查询语言: sql, graphql

### B. 导出质量建议

1. **图片处理**: 使用相对路径引用图片，确保图片文件存在
2. **表格优化**: 避免过宽表格，复杂表格考虑使用图片代替
3. **公式支持**: LaTeX 公式会自动渲染，确保语法正确
4. **链接处理**: 内部链接会保留，外部链接在 PDF 中可点击

### C. 性能优化

- 大型文档（>100页）建议分批导出
- 使用 `--no-mermaid` 跳过图表渲染以加快速度
- 批量导出时使用 `--flat` 减少目录操作

---

*最后更新: 2026-04-03 | PDF Export Tool v1.0*
