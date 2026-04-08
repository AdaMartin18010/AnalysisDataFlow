# AnalysisDataFlow 白皮书 PDF 导出系统

> 专业学术排版PDF自动生成与下载

## 📁 文件结构

```
whitepapers/
├── streaming-technology-trends-2026.md          # 原始Markdown源文件
├── flink-enterprise-implementation-guide.md     # 原始Markdown源文件
├── realtime-ai-architecture-practice.md         # 原始Markdown源文件
├── WHITEPAPER-INDEX.md                          # 白皮书索引
└── pdf/                                         # PDF输出目录
    ├── README.md                                # 本文件
    ├── index.html                               # 下载页面
    ├── metadata.json                            # PDF元数据
    ├── streaming-technology-trends-2026.pdf     # PDF输出
    ├── flink-enterprise-implementation-guide.pdf # PDF输出
    └── realtime-ai-architecture-practice.pdf    # PDF输出
```

## 🚀 快速下载

| 白皮书 | 页数 | 下载 |
|--------|------|------|
| 流计算技术趋势白皮书 2026 | 40+ | [📄 下载](./streaming-technology-trends-2026.pdf) |
| Flink企业落地指南 | 60+ | [📄 下载](./flink-enterprise-implementation-guide.pdf) |
| 实时AI架构实践白皮书 | 50+ | [📄 下载](./realtime-ai-architecture-practice.pdf) |

## 🛠️ 本地生成

### 方式1: 自动化脚本 (推荐)

```bash
# 运行生成脚本
python scripts/generate-pdfs.py

# 生成单个白皮书
python scripts/generate-pdfs.py -p streaming-technology-trends-2026

# 指定输出目录
python scripts/generate-pdfs.py -o ./my-pdfs
```

### 方式2: Pandoc 手动生成

```bash
# 安装依赖
# macOS:
brew install pandoc

# Ubuntu:
sudo apt-get install pandoc texlive-xetex texlive-lang-chinese

# 生成PDF
pandoc whitepapers/streaming-technology-trends-2026.md \
  --pdf-engine=xelatex \
  --output=streaming-technology-trends-2026.pdf \
  --toc \
  --toc-depth=3 \
  --number-sections \
  -V geometry:margin=2.5cm \
  -V CJKmainfont="Noto Serif CJK SC" \
  -V colorlinks=true
```

## 🔄 自动导出 (GitHub Actions)

### 触发方式

1. **自动触发**: 推送到 `main` 分支且Markdown文件变更
2. **手动触发**: GitHub Actions 页面 → PDF Export → Run workflow

### 工作流程

1. 检出代码
2. 安装依赖 (pandoc, texlive, 中文字体)
3. 生成封面页 (LaTeX)
4. 转换Markdown → PDF
5. 合并封面与正文
6. 上传到GitHub Pages
7. 提交PDF到仓库 (可选)

### 访问下载页面

- **GitHub Pages**: `https://<username>.github.io/AnalysisDataFlow/whitepapers/`

## 📝 PDF特性

### 排版规范

- **页面**: A4纸张，2.5cm边距
- **字体**: Noto Serif/Sans CJK SC (中日韩统一字体)
- **行距**: 1.3倍
- **页眉**: 当前章节 | AnalysisDataFlow Whitepaper
- **页脚**: 页码居中

### 包含内容

- ✅ 精美封面页
- ✅ 自动生成的目录
- ✅ 章节编号
- ✅ 代码高亮
- ✅ 表格与图表
- ✅ 超链接可点击

## 🎨 自定义模板

LaTeX模板位置: `templates/whitepaper-template.tex`

修改后重新生成即可应用新样式。

## 📊 PDF规格

| 属性 | 规格 |
|------|------|
| 页面尺寸 | A4 (210×297mm) |
| 页边距 | 上下2.5cm，左右2.5cm |
| 主字体 | 11pt |
| 颜色方案 | 学术蓝(#1f4e79) + 金色(#c5a464) |
| 引擎 | XeLaTeX |

## 🔧 故障排除

### 中文字体缺失

```bash
# macOS
brew install font-noto-cjk

# Ubuntu
sudo apt-get install fonts-noto-cjk
```

### 缺少pypdf

```bash
pip install pypdf
```

### LaTeX包缺失

```bash
# 安装完整texlive
tlmgr install ctex xeCJK fancyhdr titlesec
```

## 📚 相关文档

- [白皮书索引](../WHITEPAPER-INDEX.md)
- [GitHub Actions工作流](../../.github/workflows/pdf-export.yml)
- [生成脚本](../../scripts/generate-pdfs.py)

---

*最后更新: 2026-04-08*
