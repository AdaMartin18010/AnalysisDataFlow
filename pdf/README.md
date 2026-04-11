# AnalysisDataFlow PDF 文档库

> 流计算推导链文档 PDF 导出目录

## 📁 目录结构

```
pdf/
├── README.md                    # 本文件
├── struct/                      # Struct/ 形式理论 PDF
├── knowledge/                   # Knowledge/ 知识结构 PDF
├── flink/                       # Flink/ 专项 PDF
├── chains/                      # 推导链合集 PDF
└── merged/                      # 合并导出 PDF
```

## 🚀 快速使用

### 导出单个文件

```bash
./scripts/export-to-pdf.sh single Struct/00-INDEX.md
```

### 批量导出目录

```bash
# 导出整个 Struct 目录
./scripts/export-to-pdf.sh batch Struct/ pdf/struct/

# 导出整个 Knowledge 目录
./scripts/export-to-pdf.sh batch Knowledge/ pdf/knowledge/

# 导出整个 Flink 目录
./scripts/export-to-pdf.sh batch Flink/ pdf/flink/
```

### 导出推导链

```bash
# 导出 Flink 架构推导链
./scripts/export-to-pdf.sh chain flink-architecture

# 导出 Struct 基础理论推导链
./scripts/export-to-pdf.sh chain struct-basics

# 导出流计算概念分析推导链
./scripts/export-to-pdf.sh chain streaming-concepts
```

### 合并多个文件

```bash
./scripts/export-to-pdf.sh merge output.pdf file1.md file2.md file3.md
```

## 📋 可用推导链

| 推导链名称 | 包含内容 | 描述 |
|-----------|---------|------|
| `struct-basics` | Struct/00-INDEX.md, 01-streaming-model-intro.md | 基础理论 |
| `knowledge-patterns` | Knowledge/00-INDEX.md, design-patterns/ | 设计模式 |
| `flink-architecture` | Flink/00-INDEX.md, 01-flink-intro.md | Flink 架构 |
| `streaming-concepts` | STREAMING-CONCEPTS-COMPREHENSIVE-ANALYSIS.md | 流计算概念 |
| `design-principles` | DESIGN-PRINCIPLES.md | 设计原则 |
| `best-practices` | BEST-PRACTICES.md | 最佳实践 |

## 📄 配置文件

### 导出脚本

- **位置**: `scripts/export-to-pdf.sh`
- **功能**: 主导出脚本，支持 single/batch/merge/chain/index 命令
- **依赖**: pandoc, wkhtmltopdf

### PDF 样式

- **位置**: `scripts/pdf-styles.css`
- **功能**: PDF 排版样式，包含中文字体、代码高亮、表格样式
- **特性**: A4 页面、页眉页脚、目录样式

### 封面模板

- **位置**: `scripts/pdf-cover.md`
- **功能**: PDF 封面模板，支持变量替换
- **变量**: {{TITLE}}, {{SUBTITLE}}, {{VERSION}}, {{DATE}}

## 🔧 依赖安装

### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install -y pandoc wkhtmltopdf poppler-utils fonts-noto-cjk
```

### macOS

```bash
brew install pandoc wkhtmltopdf poppler font-noto-sans-cjk
```

### Windows (Chocolatey)

```powershell
choco install pandoc wkhtmltopdf
```

## 🎨 PDF 特性

| 特性 | 说明 |
|------|------|
| 页面尺寸 | A4 (210×297mm) |
| 页边距 | 2.5cm |
| 主字体 | Noto Serif CJK SC |
| 代码字体 | Consolas, Monaco |
| 代码高亮 | 支持 |
| 数学公式 | KaTeX 支持 |
| 目录 | 自动生成 |
| 页眉 | 当前章节标题 |
| 页脚 | 页码 |
| 封面 | 自动生成 |

## 📖 与其他导出工具的关系

| 工具 | 位置 | 用途 |
|------|------|------|
| `pdf-export.py` | 根目录 | Python 版导出工具 (pandoc + xelatex) |
| `generate-pdfs.py` | scripts/ | 白皮书 PDF 生成 |
| `generate-pdf-html.js` | scripts/ | HTML 版本 PDF 生成 |
| `export-to-pdf.sh` | scripts/ | Shell 版导出工具 (本配置) |

## 📝 更新日志

| 日期 | 版本 | 更新内容 |
|------|------|---------|
| 2026-04-11 | v1.0 | 初始版本，创建 PDF 导出配置 |

---

*AnalysisDataFlow Project | 流计算领域权威知识库*
