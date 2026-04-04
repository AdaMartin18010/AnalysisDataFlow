# 翻译规范指南

> 本指南定义 AnalysisDataFlow 项目文档翻译的标准和规范。

## 1. 翻译原则

### 1.1 准确性优先

- 技术概念必须准确传达
- 形式化定义需保持一致
- 数学符号和公式保持原样

### 1.2 可读性

- 符合目标语言表达习惯
- 避免直译造成的生硬表达
- 保持文档流畅度

### 1.3 一致性

- 术语翻译全文统一
- 风格保持一致
- 遵循项目模板规范

## 2. 术语翻译规则

### 2.1 保留原文的情况

- 专有名词：Flink、Kafka、Kubernetes
- 代码标识符：类名、方法名、变量名
- 文件路径和URL
- 定理/定义编号：Thm-S-01-01

### 2.2 首次出现标注

技术术语首次出现时标注原文：

```markdown
检查点 (Checkpoint) 是 Flink 容错机制的核心。
```

### 2.3 不翻译的内容

- Mermaid 图表中的标识符
- 代码块中的注释（除非特别说明）
- 数学公式和符号
- 引用标记 [^1]

## 3. 文档结构保留

### 3.1 六段式模板

翻译后的文档必须保留原文结构：

1. 概念定义 (Definitions)
2. 属性推导 (Properties)
3. 关系建立 (Relations)
4. 论证过程 (Argumentation)
5. 形式证明 / 工程论证 (Proof)
6. 实例验证 (Examples)
7. 可视化 (Visualizations)
8. 引用参考 (References)

### 3.2 元数据头

每篇翻译文档必须包含：

```markdown
---
source: ../原始文档路径.md
source_version: v2.8
source_hash: abc123
translated_at: 2026-04-04
translator: ai-assisted
status: draft|review|published
language: en
---
```

## 4. 格式规范

### 4.1 Markdown 格式

- 保持原有标题层级
- 保留表格格式
- 代码块语言标记不变

### 4.2 数学公式

- LaTeX 公式保持原样
- 公式编号保持不变
- 公式引用保持一致

### 4.3 链接处理

```markdown
<!-- 内部链接：指向英文版 -->
[Unified Streaming Theory](./struct/01-unified-streaming-theory.md)

<!-- 外部链接：保持不变 -->
[Apache Flink](https://flink.apache.org)

<!-- 锚点链接：保持对应 -->
[See Definitions](#1-concept-definitions)
```

## 5. 质量检查清单

### 5.1 翻译前

- [ ] 已查阅术语表
- [ ] 理解原文技术内容
- [ ] 确认翻译范围

### 5.2 翻译中

- [ ] 术语使用一致
- [ ] 保留所有代码示例
- [ ] 图表标签翻译准确

### 5.3 翻译后

- [ ] 运行术语一致性检查
- [ ] 验证所有链接
- [ ] 检查Mermaid语法
- [ ] 确认元数据完整

## 6. 常见问题

### Q: 如何处理多义词？

根据上下文选择最准确的技术含义，必要时添加说明。

### Q: 长句如何翻译？

适当拆分，保持逻辑清晰，不要追求一对一的词句对应。

### Q: 文化差异如何处理？

- 保留技术准确性
- 适当调整表达方式
- 避免使用特定文化隐喻

## 7. 工具使用

### 7.1 AI辅助翻译

```bash
# 生成翻译草稿
python scripts/ai-features/document-summarizer.py \
  --source Struct/01-foundation/01.01-unified-streaming-theory.md \
  --target-lang en \
  --output i18n/en/struct/01-unified-streaming-theory.md
```

### 7.2 术语检查

```bash
# 验证术语一致性
python scripts/i18n/validate-terminology.py --document i18n/en/struct/01-unified-streaming-theory.md
```

## 8. 参考资源

- [中文技术文档写作规范](https://github.com/ruanyf/document-style-guide)
- [Microsoft Writing Style Guide](https://docs.microsoft.com/en-us/style-guide/)
- [Google Developer Documentation Style Guide](https://developers.google.com/style)
