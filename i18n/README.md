# AnalysisDataFlow 国际化 (i18n) 指南

本目录包含项目的国际化架构和翻译内容。

## 快速开始

### 目录结构

```
i18n/
├── README.md                 # 本文件
├── i18n-architecture.md      # 架构设计文档
├── terminology-glossary.csv  # 术语翻译对照表
├── config/                   # 配置文件
│   └── i18n-config.json     # 主配置
└── en/                       # 英文翻译内容
    ├── README.md
    └── struct/              # Struct核心理论文档
```

### 支持的语种

| 语言代码 | 语言 | 完成度 | 状态 |
|---------|------|--------|------|
| zh | 中文 (源语言) | 100% | ✅ 完整 |
| en | English | ~5% | 🔄 进行中 |

## 翻译流程

### 1. 选择文档

参考 `i18n-architecture.md` 中的翻译优先级表选择待翻译文档。

### 2. 术语准备

查阅 `terminology-glossary.csv` 确保术语翻译一致性。

### 3. 翻译执行

使用AI辅助翻译工具：

```bash
# 使用AI辅助翻译单篇文档
python scripts/ai-features/document-summarizer.py --translate Struct/01-foundation/01.01-unified-streaming-theory.md --target-lang en
```

### 4. 质量审核

- 检查术语一致性
- 验证Mermaid图表
- 确认链接有效性

### 5. 提交PR

```bash
git checkout -b i18n/en-{document-name}
git add i18n/en/...
git commit -m "i18n: translate {document-name} to English"
git push origin i18n/en-{document-name}
```

## 术语管理

### 添加新术语

1. 编辑 `terminology-glossary.csv`
2. 按字母顺序添加
3. 包含完整定义和上下文

### 术语格式

```csv
term_en,term_zh,category,definition_en,context,notes
Watermark,水位线,Mechanism,Timestamp marker for event time progress,Flink/02-core-mechanisms,Monotonic timestamp
```

## 同步机制

当源文档(中文)更新时：

1. 系统自动检测变更
2. 标记受影响翻译文档
3. 生成更新任务
4. 通知翻译维护者

## 贡献指南

1. 阅读 [翻译规范](./translation-guide.md)
2. 查阅术语表
3. 保持六段式文档结构
4. 验证所有外部链接
5. 通过自动化检查

## 相关资源

- [架构设计](./i18n-architecture.md)
- [术语表](./terminology-glossary.csv)
- [项目规范](../AGENTS.md)
