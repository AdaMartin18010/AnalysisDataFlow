---
title: "{{TITLE}}"
subtitle: "AnalysisDataFlow Project"
author: "流计算领域权威知识库"
date: "{{DATE}}"
version: "{{VERSION}}"
---

<!--
=============================================================================
AnalysisDataFlow PDF 封面模板
=============================================================================
使用方法:
1. 复制此文件并重命名
2. 替换 {{TITLE}}, {{DATE}}, {{VERSION}} 等占位符
3. 使用 pandoc 转换为 HTML 后生成 PDF 封面

示例:
  pandoc cover.md -o cover.html --template=default.html
  wkhtmltopdf cover.html cover.pdf
=============================================================================
-->

<style>
.cover-page {
    width: 210mm;
    height: 297mm;
    margin: 0;
    padding: 0;
    position: relative;
    background: linear-gradient(135deg, #1f4e79 0%, #3a7bd5 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: white;
    text-align: center;
    font-family: "Noto Serif CJK SC", "Source Han Serif SC", serif;
}

.cover-badge {
    font-size: 24pt;
    letter-spacing: 8px;
    margin-bottom: 40px;
    opacity: 0.9;
    font-weight: 300;
}

.cover-title {
    font-size: 36pt;
    font-weight: bold;
    margin-bottom: 20px;
    padding: 0 40px;
    line-height: 1.3;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.cover-subtitle {
    font-size: 16pt;
    opacity: 0.85;
    margin-bottom: 60px;
    font-weight: 300;
}

.cover-divider {
    width: 200px;
    height: 3px;
    background: #c5a464;
    margin: 30px 0;
}

.cover-meta {
    font-size: 12pt;
    opacity: 0.8;
    line-height: 2;
}

.cover-meta-item {
    margin: 5px 0;
}

.cover-footer {
    position: absolute;
    bottom: 50px;
    left: 0;
    right: 0;
    text-align: center;
}

.cover-url {
    font-size: 10pt;
    opacity: 0.6;
}

.cover-logo {
    position: absolute;
    top: 50px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 14pt;
    letter-spacing: 4px;
    opacity: 0.7;
}
</style>

<div class="cover-page">
    <div class="cover-logo">ANALYSISDATAFLOW</div>
    <div class="cover-badge">PDF DOCUMENT</div>
    <div class="cover-title">{{TITLE}}</div>
    <div class="cover-subtitle">{{SUBTITLE}}</div>
    <div class="cover-divider"></div>
    <div class="cover-meta">
        <div class="cover-meta-item">版本: {{VERSION}}</div>
        <div class="cover-meta-item">导出日期: {{DATE}}</div>
        <div class="cover-meta-item">流计算领域权威知识库</div>
    </div>
    <div class="cover-footer">
        <div class="cover-url">https://github.com/AnalysisDataFlow</div>
    </div>
</div>

---

<!--
=============================================================================
封面模板变量说明:

{{TITLE}}       - 文档主标题
{{SUBTITLE}}    - 副标题/描述
{{VERSION}}     - 文档版本号
{{DATE}}        - 导出日期 (YYYY-MM-DD格式)

使用脚本自动替换:
  sed -i "s/{{TITLE}}/实际标题/g" cover.md
  sed -i "s/{{DATE}}/$(date +%Y-%m-%d)/g" cover.md
=============================================================================
-->

# 文档信息

| 属性 | 值 |
|------|-----|
| **文档名称** | {{TITLE}} |
| **所属项目** | AnalysisDataFlow |
| **文档版本** | {{VERSION}} |
| **导出日期** | {{DATE}} |
| **项目主页** | <https://github.com/AnalysisDataFlow> |

## 关于本项目

AnalysisDataFlow 是对**流计算的理论模型、层次结构、工程实践、业务建模**的全面梳理与体系构建。目标是为学术研究、工业工程和技术选型提供**严格、完整、可导航**的知识库。

## 目录结构

- **Struct/** - 形式理论、分析论证、严格证明
- **Knowledge/** - 知识结构、设计模式、商业应用
- **Flink/** - Flink 专项：架构、机制、对比、路线图

## 版权声明

本文档由 AnalysisDataFlow Project 出品，仅供学习交流使用。

---

*本 PDF 由自动化脚本生成，如有排版问题请访问在线版本。*
