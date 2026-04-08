# AnalysisDataFlow AI 辅助文档生成工具

> 纯本地运行的文档智能化工具集，无需 API Key

## 工具概览

| 工具 | 功能 | 文件 |
|------|------|------|
| 文档摘要生成器 | 生成结构化摘要、提取关键元素、改进建议 | `doc-summarizer.py` |
| 自动翻译助手 | Markdown 中英互译、术语对照 | `auto-translator.py` |
| 代码注释生成器 | 多语言文档字符串/注释生成 | `code-comment-generator.py` |
| 交叉引用建议器 | 文档相似度分析、链接建议 | `cross-ref-suggester.py` |

## 快速开始

### 1. 文档摘要生成

```bash
# 单文件处理
python .scripts/ai-assistant/doc-summarizer.py Struct/00-INDEX.md

# 批量处理目录
python .scripts/ai-assistant/doc-summarizer.py Struct/ --batch

# 输出到标准输出
python .scripts/ai-assistant/doc-summarizer.py Knowledge/cep-complete-tutorial.md --stdout
```

**输出示例：**

```markdown
# 文档摘要: CEP 复杂事件处理完整教程

> 生成时间: 2026-04-08T10:30:00
> 原文档: `Knowledge/cep-complete-tutorial.md`
> 形式化等级: L3-APPLIED

## 结构分析

| 章节 | 状态 | 内容量 |
|------|------|--------|
| 概念定义 | ✅ | 1250 字符 |
| 属性推导 | ✅ | 890 字符 |
| 关系建立 | ✅ | 1560 字符 |
| ... | ... | ... |

## 关键元素

### 定义 (3)

- **Def-K-01-01**: 复杂事件处理 (CEP) 是一种...

### 定理/引理 (2)

- **Thm-K-01-01**: CEP 的匹配复杂度为 O(n²)
```

### 2. 自动翻译

```bash
# 中文 -> 英文
python .scripts/ai-assistant/auto-translator.py Flink/flink-checkpoint.md -t en

# 英文 -> 中文
python .scripts/ai-assistant/auto-translator.py README-EN.md -t zh

# 批量翻译
python .scripts/ai-assistant/auto-translator.py Knowledge/ --batch -t en

# 自动检测源语言
python .scripts/ai-assistant/auto-translator.py input.md --source auto -t en
```

**翻译特点：**
- 保留代码块和公式
- 术语对照表自动替换
- 章节标题智能映射
- 定理/定义编号保持不变

### 3. 代码注释生成

```bash
# Python 文件
python .scripts/ai-assistant/code-comment-generator.py scripts/dataflow.py

# 批量处理
python .scripts/ai-assistant/code-comment-generator.py scripts/ --batch

# 添加行内注释
python .scripts/ai-assistant/code-comment-generator.py src/processor.py --inline

# 指定输出文件
python .scripts/ai-assistant/code-comment-generator.py main.py -o main-commented.py
```

**支持语言：**
- Python (`.py`)
- Java (`.java`)
- Scala (`.scala`)
- Rust (`.rs`)
- Go (`.go`)
- JavaScript (`.js`)
- TypeScript (`.ts`)

### 4. 交叉引用建议

```bash
# 分析整个项目
python .scripts/ai-assistant/cross-ref-suggester.py . -o cross-ref-report.md

# 只分析特定目录
python .scripts/ai-assistant/cross-ref-suggester.py Struct/

# 导出 JSON 格式
python .scripts/ai-assistant/cross-ref-suggester.py . --json suggestions.json

# 为单个文档生成建议
python .scripts/ai-assistant/cross-ref-suggester.py . --suggest-for Struct/00-INDEX.md
```

## 配置说明

编辑 `config.yaml` 自定义工具行为：

```yaml
# 文档结构规范
document_structure:
  sections:
    - name: "概念定义"
      id: "definitions"
      required: true
      patterns:
        - "## 1. 概念定义"
        - "## Definitions"

# 术语对照表
translator:
  terminology:
    - zh: "流计算"
      en: "Stream Computing"
    - zh: "数据流"
      en: "Dataflow"

# 相似度阈值
cross_ref:
  similarity_threshold: 0.6
  max_suggestions: 5

# 输出配置
output:
  default_format: "markdown"
  save_directory: ".scripts/ai-assistant/output"
```

## 输出目录结构

```
.scripts/ai-assistant/
├── output/                    # 默认输出目录
│   ├── 00-INDEX.summary.md    # 文档摘要
│   ├── 00-INDEX.summary.json  # JSON 格式摘要
│   └── ...
├── logs/                      # 日志文件
│   └── ai-assistant.log
├── config.yaml               # 配置文件
└── README.md                 # 本文件
```

## 集成到工作流

### Makefile 集成

```makefile
# AI Assistant Targets
.PHONY: summarize translate comments cross-ref

SUMMARIZER := python .scripts/ai-assistant/doc-summarizer.py
TRANSLATOR := python .scripts/ai-assistant/auto-translator.py
COMMENTER := python .scripts/ai-assistant/code-comment-generator.py
REF_SUGGESTER := python .scripts/ai-assistant/cross-ref-suggester.py

# 生成所有文档摘要
summarize:
	$(SUMMARIZER) Struct/ --batch -o .scripts/ai-assistant/output
	$(SUMMARIZER) Knowledge/ --batch -o .scripts/ai-assistant/output
	$(SUMMARIZER) Flink/ --batch -o .scripts/ai-assistant/output

# 翻译所有文档为英文
translate-en:
	$(TRANSLATOR) . --batch -t en

# 为所有代码添加注释
comments:
	$(COMMENTER) scripts/ --batch --inline

# 生成交叉引用报告
cross-ref:
	$(REF_SUGGESTER) . -o CROSS-REF-REPORT.md --json cross-ref.json

# 一键运行所有分析
ai-analysis: summarize cross-ref
	@echo "AI analysis complete. Check output/ directory."
```

### Git Hook 集成

```bash
#!/bin/bash
# .git/hooks/pre-commit

# 检查新增 Markdown 文档并生成摘要
for file in $(git diff --cached --name-only --diff-filter=A | grep '\.md$'); do
    if [ -f "$file" ]; then
        echo "Generating summary for: $file"
        python .scripts/ai-assistant/doc-summarizer.py "$file"
    fi
done
```

## 示例输出

### 文档摘要示例

详见 `output/` 目录生成的 `.summary.md` 文件，包含：
- 内容概要
- 六段式结构分析
- 定义/定理提取
- 改进建议
- Mermaid 图建议

### 翻译示例

**原文 (中文)：**
```markdown
## 1. 概念定义

**Def-F-01-01** (流计算): 流计算是一种处理...
```

**译文 (英文)：**
```markdown
## 1. Concept Definitions

**Def-F-01-01** (Stream Computing): Stream computing is a processing...
```

### 代码注释示例

**Python 函数注释：**
```python
def process_event(event, timestamp):
    """
    process_event
    
    功能: 实现process_event功能
    
    参数:
        event (Any): 参数描述
        timestamp (Any): 参数描述
    
    返回:
        Any: 返回描述
    
    示例:
        >>> process_event(event, timestamp)
        结果
    """
    # 处理逻辑
    pass
```

### 交叉引用报告示例

```markdown
## 链接建议

### CEP 复杂事件处理完整教程
**文件**: `Knowledge/cep-complete-tutorial.md`

建议添加以下链接：

| 目标文档 | 相似度 | 理由 | 建议链接 |
|----------|--------|------|----------|
| Flink CEP 模式 | 0.72 | 共同关键词: 模式, CEP, 事件 | `[Flink CEP 模式](../Flink/flink-cep-patterns.md)` |
| 生产检查清单 | 0.45 | 共同关键词: 生产, 部署 | `[生产检查清单](production-checklist.md)` |
```

## 高级用法

### 自定义术语表

在 `config.yaml` 中添加：

```yaml
translator:
  terminology:
    - zh: "你的术语"
      en: "Your Terminology"
```

### 批量处理特定类型文件

```bash
# 只处理 Flink 目录下的文档
python .scripts/ai-assistant/doc-summarizer.py Flink/ --batch

# 只处理 Python 代码
python .scripts/ai-assistant/code-comment-generator.py . --batch --extensions py
```

### 结合其他工具

```bash
# 生成摘要后翻译
for file in Struct/*.md; do
    python .scripts/ai-assistant/doc-summarizer.py "$file" --stdout > /tmp/summary.md
    python .scripts/ai-assistant/auto-translator.py /tmp/summary.md -t en -o "${file%.md}-en.summary.md"
done
```

## 故障排除

### 中文乱码

确保文件使用 UTF-8 编码：
```bash
# 转换文件编码
iconv -f GBK -t UTF-8 input.md > output.md
```

### 内存不足 (批量处理大目录)

```bash
# 分批处理
find . -name "*.md" | head -100 | xargs -I {} python .scripts/ai-assistant/doc-summarizer.py {}
```

### 配置文件加载失败

```bash
# 显式指定配置文件
python .scripts/ai-assistant/doc-summarizer.py input.md -c .scripts/ai-assistant/config.yaml
```

## 性能说明

- 所有工具**纯本地运行**，无需网络连接
- 处理速度：约 100 页/秒 (取决于文档大小)
- 内存占用：约 50MB + 文档内容大小
- 支持增量处理（不会重复处理已分析文件）

## 贡献指南

如需改进工具：
1. 修改相应 `.py` 文件
2. 更新 `config.yaml` 中的规则
3. 在 `README.md` 添加使用示例
4. 提交 PR

## 许可证

与 AnalysisDataFlow 项目保持一致。
