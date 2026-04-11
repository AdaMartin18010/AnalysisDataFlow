# AnalysisDataFlow 白皮书 PDF 导出指南

> 完整的专业PDF导出解决方案

## 📋 任务完成清单

| 任务 | 状态 | 文件位置 |
|------|------|----------|
| GitHub Actions自动导出 | ✅ 完成 | `.github/workflows/pdf-export.yml` |
| Docker备用导出工作流 | ✅ 完成 | `.github/workflows/pdf-export-docker.yml` |
| LaTeX模板 | ✅ 完成 | `templates/whitepaper-template.tex` |
| 本地生成脚本 (Python) | ✅ 完成 | `scripts/generate-pdfs.py` |
| HTML生成脚本 (Node.js) | ✅ 完成 | `scripts/generate-pdf-html.js` |
| 下载页面 | ✅ 完成 | `whitepapers/pdf/index.html` |
| PDF元数据 | ✅ 完成 | `whitepapers/pdf/metadata.json` |
| 白皮书索引更新 | ✅ 完成 | `whitepapers/WHITEPAPER-INDEX.md` |

---

## 🚀 快速开始

### 方式1: GitHub Actions自动导出 (推荐)

1. 推送代码到 `main` 分支
2. GitHub Actions自动触发PDF生成
3. PDF文件自动上传到GitHub Pages
4. 访问 `https://<username>.github.io/AnalysisDataFlow/whitepapers/`

### 方式2: 手动触发GitHub Actions

1. 进入GitHub仓库 → Actions → PDF Export
2. 点击 "Run workflow"
3. 选择要导出的白皮书（可选）
4. 等待完成后下载Artifacts

### 方式3: 本地生成

```bash
# 使用Python脚本
python scripts/generate-pdfs.py

# 或使用Node.js脚本 (需安装Playwright)
node scripts/generate-pdf-html.js
```

---

## 📁 文件结构

```
AnalysisDataFlow/
├── .github/
│   └── workflows/
│       ├── pdf-export.yml           # 主PDF导出工作流 (LaTeX/XeLaTeX)
│       └── pdf-export-docker.yml    # Docker备用工作流
├── templates/
│   └── whitepaper-template.tex      # LaTeX排版模板
├── scripts/
│   ├── generate-pdfs.py             # Python生成脚本
│   └── generate-pdf-html.js         # Node.js/HTML生成脚本
├── whitepapers/
│   ├── streaming-technology-trends-2026.md
│   ├── flink-enterprise-implementation-guide.md
│   ├── realtime-ai-architecture-practice.md
│   ├── WHITEPAPER-INDEX.md          # 更新后的索引
│   └── pdf/
│       ├── index.html               # 下载页面
│       ├── metadata.json            # 元数据
│       ├── README.md                # PDF目录说明
│       ├── streaming-technology-trends-2026.pdf
│       ├── flink-enterprise-implementation-guide.pdf
│       └── realtime-ai-architecture-practice.pdf
└── PDF-EXPORT-GUIDE.md              # 本文件
```

---

## 🎨 PDF排版特性

### 学术格式规范

| 特性 | 规格 |
|------|------|
| **页面** | A4 (210×297mm) |
| **页边距** | 2.5cm 四边等距 |
| **主字体** | Noto Serif CJK SC 11pt |
| **行距** | 1.3倍 |
| **颜色方案** | 学术蓝(#1f4e79) + 金色(#c5a464) |

### 包含内容

- ✅ **精美封面页** - 专业白皮书风格
- ✅ **自动生成目录** - 三级标题导航
- ✅ **章节编号** - 自动编号系统
- ✅ **页眉页脚** - 当前章节 | AnalysisDataFlow
- ✅ **代码高亮** - 语法着色显示
- ✅ **表格渲染** - 专业表格样式
- ✅ **超链接** - 可点击的目录和链接
- ✅ **可打印质量** - 矢量图形，高质量输出

---

## 📥 下载链接

| 白皮书 | 页数 | 下载 |
|--------|------|------|
| 流计算技术趋势白皮书 2026 | 40+ | [下载PDF](./whitepapers/pdf/streaming-technology-trends-2026.pdf) |
| Flink企业落地指南 | 60+ | [下载PDF](./whitepapers/pdf/flink-enterprise-implementation-guide.pdf) |
| 实时AI架构实践白皮书 | 50+ | [下载PDF](./whitepapers/pdf/realtime-ai-architecture-practice.pdf) |

**在线下载页面**: [whitepapers/pdf/index.html](./whitepapers/pdf/index.html)

---

## 🔧 技术细节

### GitHub Actions工作流

```yaml
触发条件:
  - 推送到 main 分支且 markdown 文件变更
  - 手动触发 (workflow_dispatch)

执行步骤:
  1. 检出代码
  2. 安装依赖 (pandoc/latex, 中文字体)
  3. 生成封面页 (LaTeX)
  4. 转换 Markdown → PDF
  5. 合并封面与正文
  6. 上传Artifacts
  7. 部署到GitHub Pages
```

### 依赖要求

#### GitHub Actions环境

- `pandoc/latex:3.1` Docker镜像
- `font-noto-cjk` 中文字体包
- `texlive-xetex` XeLaTeX引擎

#### 本地环境

**Python方式:**

```bash
pip install pypdf
# 系统依赖: pandoc, texlive-xetex, fonts-noto-cjk
```

**Node.js方式:**

```bash
npm install playwright
npx playwright install chromium
```

---

## 🛠️ 自定义配置

### 修改LaTeX模板

编辑 `templates/whitepaper-template.tex`:

```latex
% 修改颜色
\definecolor{primaryblue}{RGB}{31,78,121}

% 修改页边距
\geometry{margin=2.5cm}

% 修改字体
\setCJKmainfont{Noto Serif CJK SC}
```

### 修改封面样式

编辑GitHub Actions工作流中的 `cover-template.tex` 部分。

---

## 📊 PDF规格对比

| 方法 | 质量 | 速度 | 复杂度 | 推荐场景 |
|------|------|------|--------|----------|
| GitHub Actions (LaTeX) | ⭐⭐⭐⭐⭐ | 中等 | 低 | 生产环境 |
| Docker (LaTeX) | ⭐⭐⭐⭐⭐ | 中等 | 低 | CI/CD |
| Python脚本 | ⭐⭐⭐⭐⭐ | 慢 | 中 | 本地开发 |
| HTML/Playwright | ⭐⭐⭐⭐ | 快 | 中 | 快速预览 |

---

## 🔍 故障排除

### GitHub Actions失败

```bash
# 检查工作流日志
GitHub → Actions → PDF Export → 最新运行
```

常见原因:

- 中文字体缺失 → 已配置自动安装
- LaTeX包缺失 → 已配置完整texlive
- 内存不足 → 已优化容器设置

### 本地生成失败

```bash
# 检查依赖
python scripts/generate-pdfs.py --check

# 安装缺失依赖
# macOS:
brew install pandoc
brew install --cask font-noto-sans-cjk

# Ubuntu:
sudo apt-get install pandoc texlive-xetex fonts-noto-cjk
```

---

## 📚 相关文档

- [白皮书索引](./whitepapers/WHITEPAPER-INDEX.md)
- [PDF目录说明](./whitepapers/pdf/README.md)
- [项目架构](./ARCHITECTURE.md)

---

## 📝 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v1.0 | 2026-04-08 | 初始版本，完整PDF导出系统 |

---

*AnalysisDataFlow Project | 流计算领域权威知识库*
