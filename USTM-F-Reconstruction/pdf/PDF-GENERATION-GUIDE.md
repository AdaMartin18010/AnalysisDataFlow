# USTM-F PDF 生成指南

> 如何将合并的Markdown文档转换为PDF格式

---

## 交付物说明

由于当前环境中 `pandoc` 不可用，我们已为您准备了所有必要文件以便生成PDF：

| 文件 | 说明 |
|------|------|
| `USTM-F-Combined.md` | 合并后的32篇文档 (约600KB) |
| `PDF-GENERATION-GUIDE.md` | 本指南 |

---

## 方法1: 使用 Pandoc (推荐)

### 安装 Pandoc

**Windows:**

```powershell
# 使用 Chocolatey
choco install pandoc

# 或使用 MSI 安装包从 https://pandoc.org/installing.html 下载
```

**macOS:**

```bash
brew install pandoc
```

**Linux:**

```bash
sudo apt-get install pandoc texlive-xetex
```

### 生成 PDF

```bash
# 基础命令
cd USTM-F-Reconstruction/pdf
pandoc USTM-F-Combined.md -o USTM-F-Complete.pdf

# 带样式的高级命令
pandoc USTM-F-Combined.md \
  -o USTM-F-Complete.pdf \
  --pdf-engine=xelatex \
  -V CJKmainfont="Noto Sans CJK SC" \
  -V geometry:margin=2.5cm \
  --toc \
  --toc-depth=3 \
  -V colorlinks=true \
  -V linkcolor=blue \
  -V urlcolor=blue
```

---

## 方法2: 使用 Markdown-PDF (Node.js)

```bash
# 安装
npm install -g markdown-pdf

# 生成 PDF
cd USTM-F-Reconstruction/pdf
markdown-pdf USTM-F-Combined.md -o USTM-F-Complete.pdf
```

---

## 方法3: 使用 VS Code 扩展

1. 安装 **"Markdown PDF"** 扩展 (yzane.markdown-pdf)
2. 打开 `USTM-F-Combined.md`
3. 右键 → **Markdown PDF: Export (pdf)**

---

## 方法4: 在线转换工具

1. 访问 <https://www.markdowntopdf.com/> 或类似网站
2. 上传 `USTM-F-Combined.md`
3. 下载生成的PDF

---

## 预期输出

生成的PDF将包含：

- **标题页**: USTM-F 统一流计算理论元框架
- **目录**: 自动生成的5级目录
- **正文**: 全部32篇文档，按L0-L4层次组织
- **附录**: 依赖关系图和导航索引引用

**预计页数**: 400-600页 (取决于格式设置)

---

## 文档结构预览

```
USTM-F-Complete.pdf
├── 标题页
├── 目录
├── L0: 元理论基础 (4篇)
│   ├── 00.01 范畴论基础
│   ├── 00.02 格论与序理论
│   ├── 00.03 类型论基础
│   └── 00.00 USTM-F概览
├── L1: 统一流模型 (6篇)
│   ├── 01.01 流的数学定义
│   ├── 01.02 统一时间模型
│   ├── 01.03 算子代数
│   ├── 01.04 组合理论
│   ├── 01.05 USTM核心语义
│   └── 01.00 USTM整合
├── L2: 模型实例化 (8篇)
│   ├── 02.00 模型实例化框架
│   ├── 02.01 Actor模型
│   ├── 02.02 CSP
│   ├── 02.03 Dataflow
│   ├── 02.04 Petri网
│   ├── 02.05 π-演算
│   ├── 02.06 会话类型
│   └── 02.07 Flink
├── L3: 证明链 (8篇)
│   ├── 03.01 基础引理库
│   ├── 03.02 确定性定理
│   ├── 03.03 一致性格定理
│   ├── 03.04 Watermark单调性
│   ├── 03.05 Checkpoint正确性
│   ├── 03.06 Exactly-Once语义
│   ├── 03.07 类型安全
│   └── 03.00 证明链整合
└── L4: 编码与验证 (6篇)
    ├── 04.01 编码理论
    ├── 04.02 Actor-CSP编码
    ├── 04.03 Dataflow-CSP编码
    ├── 04.04 表达能力层次
    ├── 04.05 Coq形式化
    └── 04.06 TLA+规约
```

---

## 交叉引用说明

生成的PDF中将包含以下交叉引用：

1. **文档间链接**: 32篇文档之间的双向引用
2. **定理引用链接**: 如 Thm-U-20 链接到证明文档
3. **定义引用**: 如 Def-U-01 链接到定义位置
4. **导航链接**: 指向导航索引和依赖关系图

---

## 统计信息

| 项目 | 数量 |
|------|------|
| 总文档数 | 32 |
| 已添加交叉引用 | 17 (53.1%) |
| 内部链接数 | 155+ |
| 形式化定义 | 172+ |
| 定理 | 28 |
| 引理 | 77+ |

---

*USTM-F 重构项目 | PDF生成指南 | 2026-04-08*
