# 文档质量保障自动化工具

本目录包含5个自动化Python工具，用于保障项目文档的质量和一致性。

## 工具列表

### 1. cross-ref-validator.py - 交叉引用自动检查器

扫描并验证Markdown文件中的所有链接。

**功能特性：**
- 扫描所有Markdown文件中的链接
- 验证内部链接有效性（文件存在、锚点存在）
- 验证外部链接可访问性（HTTP 200）
- 生成详细的错误报告
- 支持增量检查（只检查变更文件）

**使用方法：**
```bash
# 检查所有Markdown文件
python cross-ref-validator.py

# 只检查指定文件（增量模式）
python cross-ref-validator.py --incremental file1.md file2.md

# 跳过外部链接检查
python cross-ref-validator.py --skip-external

# 指定输出目录
python cross-ref-validator.py --output-dir ./reports
```

**输出：**
- JSON报告：`cross-ref-report-{timestamp}.json`
- Markdown摘要：`cross-ref-summary-{timestamp}.md`

---

### 2. template-validator.py - 六段式模板验证器

验证文档是否遵循项目规定的六段式结构。

**功能特性：**
- 验证文档六段式结构完整性
- 检查必要的章节是否存在
- 验证形式化元素编号格式（Def-*, Thm-*, Lemma-*）
- 检查Mermaid图表存在性
- 检查引用格式
- 提供修复建议

**使用方法：**
```bash
# 验证当前目录
python template-validator.py

# 验证指定目录
python template-validator.py -d ./Struct

# 严格模式（将警告视为错误）
python template-validator.py --strict

# 使用配置文件
python template-validator.py --config template-rules.json
```

**输出：**
- JSON报告：`template-validation-{timestamp}.json`
- Markdown报告：`template-validation-{timestamp}.md`

---

### 3. formal-element-tracker.py - 形式化元素自动编号工具

管理和追踪所有形式化元素（定义、定理、引理等）。

**功能特性：**
- 扫描所有文档中的形式化元素
- 检测编号冲突和重复
- 自动建议新编号
- 生成全局形式化元素索引
- 检查编号连续性
- 可更新THEOREM-REGISTRY.md

**使用方法：**
```bash
# 扫描整个项目
python formal-element-tracker.py

# 只扫描指定阶段
python formal-element-tracker.py --stages S K

# 建议新编号
python formal-element-tracker.py --suggest Def S 01

# 更新定理注册表
python formal-element-tracker.py --update-registry
```

**输出：**
- JSON数据库：`formal-elements-{timestamp}.json`
- Markdown报告：`formal-elements-{timestamp}.md`

---

### 4. mermaid-syntax-checker.py - Mermaid图表语法检查器

验证Mermaid图表的语法正确性。

**功能特性：**
- 提取所有Mermaid代码块
- 验证语法正确性
- 检查节点ID有效性
- 验证链接一致性
- 生成图表预览（可选）
- 支持flowchart, graph, sequenceDiagram, classDiagram等

**使用方法：**
```bash
# 基本检查
python mermaid-syntax-checker.py

# 使用Mermaid CLI进行深度验证
python mermaid-syntax-checker.py --use-cli

# 生成HTML预览
python mermaid-syntax-checker.py --preview

# 指定CLI路径
python mermaid-syntax-checker.py --use-cli --mmdc-path /usr/local/bin/mmdc
```

**输出：**
- JSON报告：`mermaid-check-{timestamp}.json`
- Markdown报告：`mermaid-check-{timestamp}.md`
- HTML预览：`mermaid-preview-{timestamp}.html`（使用--preview）

---

### 5. doc-quality-dashboard.py - 文档质量仪表板生成器

综合展示文档质量状况。

**功能特性：**
- 聚合各工具的检查结果
- 生成HTML质量仪表板
- 计算质量评分
- 趋势分析（历史对比）
- 生成改进建议
- 支持GitHub Actions报告

**使用方法：**
```bash
# 生成HTML仪表板
python doc-quality-dashboard.py

# 指定报告目录
python doc-quality-dashboard.py -r ./validation-reports

# 生成GitHub Actions格式报告
python doc-quality-dashboard.py --github-actions -o $GITHUB_STEP_SUMMARY

# 不保存历史数据
python doc-quality-dashboard.py --no-save-history
```

**输出：**
- HTML仪表板：`quality-dashboard.html`
- GitHub Actions报告（使用--github-actions）

---

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt

# 可选：安装Mermaid CLI（用于深度语法检查）
npm install -g @mermaid-js/mermaid-cli
```

### 运行所有检查

```bash
# 创建报告目录
mkdir -p validation-reports

# 1. 检查交叉引用
python cross-ref-validator.py --output-dir validation-reports

# 2. 验证模板合规
python template-validator.py -o validation-reports

# 3. 检查形式化元素
python formal-element-tracker.py -o validation-reports

# 4. 检查Mermaid语法
python mermaid-syntax-checker.py -o validation-reports --preview

# 5. 生成质量仪表板
python doc-quality-dashboard.py -r validation-reports
```

### 集成到CI/CD

**GitHub Actions示例：**

```yaml
name: Documentation Quality Check

on: [push, pull_request]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
          
      - name: Install dependencies
        run: |
          pip install -r .scripts/automation/requirements.txt
          
      - name: Run quality checks
        run: |
          mkdir -p validation-reports
          python .scripts/automation/cross-ref-validator.py --output-dir validation-reports
          python .scripts/automation/template-validator.py -o validation-reports
          python .scripts/automation/formal-element-tracker.py -o validation-reports
          python .scripts/automation/mermaid-syntax-checker.py -o validation-reports
          
      - name: Generate dashboard
        run: |
          python .scripts/automation/doc-quality-dashboard.py \
            -r validation-reports \
            --github-actions \
            -o $GITHUB_STEP_SUMMARY
            
      - name: Upload reports
        uses: actions/upload-artifact@v3
        with:
          name: quality-reports
          path: validation-reports/
```

---

## 项目结构

```
.scripts/automation/
├── README.md                           # 本文件
├── requirements.txt                    # Python依赖
├── cross-ref-validator.py              # 工具1: 交叉引用检查
├── template-validator.py               # 工具2: 模板验证
├── formal-element-tracker.py           # 工具3: 形式化元素追踪
├── mermaid-syntax-checker.py           # 工具4: Mermaid语法检查
├── doc-quality-dashboard.py            # 工具5: 质量仪表板
└── tests/                              # 单元测试
    ├── __init__.py
    ├── test_cross_ref_validator.py
    ├── test_template_validator.py
    ├── test_formal_element_tracker.py
    └── test_mermaid_checker.py
```

---

## 测试

运行单元测试：

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python -m pytest tests/test_cross_ref_validator.py

# 带覆盖率报告
python -m pytest tests/ --cov=. --cov-report=html
```

---

## 配置

### 自定义验证规则

创建 `template-rules.json`：

```json
{
  "required_sections": [
    "概念定义",
    "属性推导",
    "形式证明",
    "实例验证"
  ],
  "skip_patterns": [
    "node_modules",
    ".git",
    "archive"
  ],
  "formal_element_types": [
    "Def",
    "Thm",
    "Lemma",
    "Prop",
    "Cor"
  ]
}
```

使用配置：
```bash
python template-validator.py --config template-rules.json
```

### 质量评分权重

在 `doc-quality-dashboard.py` 中修改默认权重：

```python
DEFAULT_WEIGHTS = {
    'cross_ref': 0.25,      # 交叉引用完整性
    'template': 0.25,       # 模板合规性
    'formal_element': 0.20, # 形式化元素规范
    'mermaid': 0.15,        # Mermaid语法
    'readability': 0.15,    # 可读性
}
```

---

## 退出码

所有工具都遵循以下退出码约定：

- `0` - 检查通过，无错误或问题
- `1` - 发现问题或错误

可以在CI/CD管道中使用这些退出码来决定是否继续构建。

---

## 故障排除

### 外部链接检查超时

```bash
# 增加超时时间
python cross-ref-validator.py --timeout 60

# 跳过外部链接检查
python cross-ref-validator.py --skip-external
```

### Mermaid CLI未找到

```bash
# 安装Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# 或使用Docker
docker pull minlag/mermaid-cli
```

### 内存不足

对于大型项目，可以分批处理：

```bash
# 只处理特定目录
python cross-ref-validator.py -d ./Struct

# 增量检查
python cross-ref-validator.py --incremental $(git diff --name-only HEAD~1)
```

---

## 贡献指南

1. 确保代码通过所有测试
2. 添加新功能时同步更新测试
3. 遵循PEP 8代码风格
4. 使用类型注解
5. 更新文档

---

## 许可证

与主项目相同。

---

## 作者

Automation Agent

版本: 1.0.0
日期: 2026-04-11
