# 📚 AnalysisDataFlow — 文档中心索引

> **文档版本**: v5.0  
> **最后更新**: 2026-04-12  
> **项目状态**: 100% 完成 ✅

---

## 🗺️ 文档中心导航

本文档中心包含项目的辅助文档，包括认证指南、国际化文档、贡献指南等。

```
docs/
├── 📋 certification/      # 认证考试指南 (CSA/CSE/CSP)
├── 🌍 i18n/              # 国际化文档 (英/日/德/法)
├── 🤝 contributing/      # 贡献指南与社区规范
├── 🧠 knowledge-graph/   # 知识图谱文档
├── 🤖 ai-features/       # AI功能设计文档
└── 📖 其他指南文档
```

---

## 📋 认证考试指南 (certification/)

### 认证体系概览

| 认证 | 全称 | 级别 | 目标人群 | 文档数 |
|------|------|------|----------|--------|
| **CSA** | Certified Streaming Analyst | 初级 | 分析师、业务人员 | 8 |
| **CSE** | Certified Streaming Engineer | 中级 | 开发工程师 | 4 |
| **CSP** | Certified Streaming Professional | 高级 | 架构师、专家 | 4 |

### 认证路径

```
初学者
    ↓
CSA (初级) ──→ 流处理基础、Flink入门
    ↓
CSE (中级) ──→ 核心机制、编程实践
    ↓
CSP (高级) ──→ 架构设计、性能调优
```

### 认证资源

| 资源类型 | 说明 | 链接 |
|----------|------|------|
| 考试大纲 | 各认证详细大纲 | [certification/README.md](./certification/README.md) |
| 学习指南 | CSA备考指南 | [csa/exam-guide-csa.md](./certification/csa/exam-guide-csa.md) |
| 动手实验 | 配套实验 | [csa/labs/](./certification/csa/labs/) |
| 模拟测验 | 练习题 | [csa/quizzes/](./certification/csa/quizzes/) |
| 综合项目 | 毕业设计 | [csa/resources/capstone-project-csa.md](./certification/csa/resources/capstone-project-csa.md) |
| 考试时间表 | 2026年安排 | [schedule-2026.md](./certification/schedule-2026.md) |

---

## 🌍 国际化文档 (i18n/)

### 支持语言

| 语言 | 代码 | 文档数 | 状态 | 路径 |
|------|------|--------|------|------|
| 英语 | en | 15+ | ✅ 活跃 | [i18n/en/](./i18n/en/) |
| 日语 | ja | 4 | ✅ 完成 | [i18n/ja/](./i18n/ja/) |
| 德语 | de | 3 | ✅ 完成 | [i18n/de/](./i18n/de/) |
| 法语 | fr | 2 | ✅ 完成 | [i18n/fr/](./i18n/fr/) |

### 英文文档结构 (i18n/en/)

| 文档 | 说明 | 路径 |
|------|------|------|
| **README.md** | 英文项目概览 | [i18n/en/README.md](./i18n/en/README.md) |
| **QUICK-START.md** | 英文快速开始 | [i18n/en/QUICK-START.md](./i18n/en/QUICK-START.md) |
| **ARCHITECTURE.md** | 英文架构文档 | [i18n/en/ARCHITECTURE.md](./i18n/en/ARCHITECTURE.md) |
| **GLOSSARY.md** | 英文术语表 | [i18n/en/GLOSSARY.md](./i18n/en/GLOSSARY.md) |
| Struct Guides | 形式理论指南 | [i18n/en/01-STRUCT-GUIDE.md](./i18n/en/01-STRUCT-GUIDE.md) |
| Knowledge Guides | 工程实践指南 | [i18n/en/02-KNOWLEDGE-GUIDE.md](./i18n/en/02-KNOWLEDGE-GUIDE.md) |
| Flink Guides | Flink专项指南 | [i18n/en/03-FLINK-GUIDE.md](./i18n/en/03-FLINK-GUIDE.md) |
| Learning Path | 学习路径 | [i18n/en/05-LEARNING-PATH.md](./i18n/en/05-LEARNING-PATH.md) |

### 翻译规范

| 规范 | 说明 | 文档 |
|------|------|------|
| 架构设计 | 国际化架构 | [i18n/ARCHITECTURE.md](./i18n/ARCHITECTURE.md) |
| 翻译模板 | 标准化模板 | [i18n/templates/translation-template.md](./i18n/templates/translation-template.md) |
| 术语库 | 核心术语 | 各语言目录下术语文件 |

---

## 🤝 贡献指南 (contributing/)

### 新贡献者入门

| 文档 | 说明 | 路径 |
|------|------|------|
| **Getting Started** | 新贡献者指南 | [contributing/getting-started.md](./contributing/getting-started.md) |
| **Writing Guide** | 文档编写规范 | [contributing/writing-guide.md](./contributing/writing-guide.md) |
| **Review Checklist** | 审查清单 | [contributing/review-checklist.md](./contributing/review-checklist.md) |
| **Code of Conduct** | 行为准则 | [contributing/code-of-conduct.md](./contributing/code-of-conduct.md) |

### 视频教程脚本

| 视频 | 主题 | 路径 |
|------|------|------|
| 01 | 第一次贡献 | [video-scripts/01-first-contribution.md](./contributing/video-scripts/01-first-contribution.md) |
| 02 | 编写定理 | [video-scripts/02-writing-theorem.md](./contributing/video-scripts/02-writing-theorem.md) |
| 03 | 创建Mermaid图 | [video-scripts/03-creating-mermaid.md](./contributing/video-scripts/03-creating-mermaid.md) |

---

## 🧠 知识图谱文档 (knowledge-graph/)

| 文档 | 说明 | 路径 |
|------|------|------|
| **README.md** | 知识图谱说明 | [knowledge-graph/README.md](./knowledge-graph/README.md) |
| **部署指南** | 图谱部署 | [KNOWLEDGE-GRAPH-DEPLOYMENT-GUIDE.md](../KNOWLEDGE-GRAPH-DEPLOYMENT-GUIDE.md) |
| **V2指南** | v2.0增强功能 | [KNOWLEDGE-GRAPH-V2-GUIDE.md](../KNOWLEDGE-GRAPH-V2-GUIDE.md) |

### 知识图谱版本

| 版本 | 技术栈 | 特性 | 文件 |
|------|--------|------|------|
| v1.0 | D3.js | 基础2D图 | [knowledge-graph.html](../knowledge-graph.html) |
| v2.0 | React 18 + D3.js v7 | 语义搜索 | [knowledge-graph-v2.html](../knowledge-graph-v2.html) |
| v3.0 | D3.js + 增强布局 | 定理网络 | [knowledge-graph-v3.html](../knowledge-graph-v3.html) |
| v4.0 | React 18 + Three.js | 3D可视化 | [knowledge-graph-v4.html](../knowledge-graph-v4.html) |

---

## 🤖 AI功能设计 (ai-features/)

| 文档 | 说明 | 路径 |
|------|------|------|
| **AI Search Design** | AI搜索架构 | [AI-SEARCH-DESIGN.md](./ai-features/AI-SEARCH-DESIGN.md) |
| **RAG Architecture** | RAG系统设计 | [RAG-ARCHITECTURE.md](./RAG-ARCHITECTURE.md) |
| **Chatbot Integration** | 聊天机器人集成 | [chatbot-integration.md](./chatbot-integration.md) |
| **Learning Path Personalization** | 个性化学习路径 | [LEARNING-PATH-PERSONALIZATION.md](./LEARNING-PATH-PERSONALIZATION.md) |

---

## 📖 其他重要文档

### 质量标准与指南

| 文档 | 说明 | 路径 |
|------|------|------|
| **文档质量标准** | 质量要求 | [doc-quality-standards.md](./doc-quality-standards.md) |
| **质量门禁指南** | CI/CD检查 | [quality-gates-guide.md](./quality-gates-guide.md) |

### 社区与生产

| 文档 | 说明 | 路径 |
|------|------|------|
| **生产验证指南** | 生产环境验证 | [COMMUNITY/PRODUCTION-VERIFICATION-GUIDE.md](./COMMUNITY/PRODUCTION-VERIFICATION-GUIDE.md) |

---

## 📊 文档统计

| 目录 | 文档数 | 大小 | 说明 |
|------|--------|------|------|
| certification/ | 17 | ~500KB | 认证体系完整文档 |
| i18n/ | 30+ | ~1MB | 多语言支持 |
| contributing/ | 8 | ~200KB | 贡献指南 |
| knowledge-graph/ | 1 | ~10KB | 图谱文档 |
| ai-features/ | 4 | ~150KB | AI功能设计 |
| 其他 | 10 | ~300KB | 质量标准等 |
| **总计** | **70+** | **~2.5MB** | **完整文档中心** |

---

## 🔍 快速查找

### 按角色查找

| 角色 | 推荐文档 |
|------|----------|
| 新用户 | [certification/csa/exam-guide-csa.md](./certification/csa/exam-guide-csa.md) |
| 贡献者 | [contributing/getting-started.md](./contributing/getting-started.md) |
| 国际化 | [i18n/ARCHITECTURE.md](./i18n/ARCHITECTURE.md) |
| 开发者 | [quality-gates-guide.md](./quality-gates-guide.md) |

### 按主题查找

| 主题 | 文档路径 |
|------|----------|
| 认证考试 | [certification/](./certification/) |
| 英文文档 | [i18n/en/](./i18n/en/) |
| 贡献指南 | [contributing/](./contributing/) |
| 知识图谱 | [knowledge-graph/](./knowledge-graph/) |
| AI功能 | [ai-features/](./ai-features/) |

---

## 🔄 维护计划

| 周期 | 任务 | 负责人 |
|------|------|--------|
| 每周 | 更新翻译状态 | 自动化 |
| 每月 | 审查认证内容 | 核心团队 |
| 每季度 | 更新i18n进度 | 社区 |
| 每年 | 认证题库更新 | 核心团队 |

---

## 📞 获取帮助

### 文档相关

- 文档错误报告: [GitHub Issues](https://github.com/luyanfeng/AnalysisDataFlow/issues)
- 翻译贡献: [i18n/README.md](./i18n/README.md)
- 一般讨论: [GitHub Discussions](https://github.com/luyanfeng/AnalysisDataFlow/discussions)

### 认证相关

- 考试咨询: 查看各认证目录下的README
- 学习资源: [certification/](./certification/)

---

**文档生成时间**: 2026-04-12  
**文档版本**: v5.0  
**项目状态**: 🎉 **100% 完成**

---

*返回项目主页*: [../README.md](../README.md)
