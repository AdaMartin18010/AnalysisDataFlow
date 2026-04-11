# 定理依赖验证工具 - Theorem Dependency Validator

> **版本**: v1.0.0 | **Python**: 3.8+ | **状态**: Production Ready

## 简介

定理依赖验证工具是 AnalysisDataFlow 项目的自动化验证工具，用于扫描、验证和分析项目中的形式化元素（定理、定义、引理、命题、推论）之间的依赖关系。

## 功能特性

### 1. 依赖完整性检查 ✅

- 自动扫描所有 Markdown 文档提取形式化元素
- 识别定理/定义/引理/命题/推论 (Thm/Def/Lemma/Prop/Cor)
- 验证依赖声明是否存在
- 检测循环依赖
- 识别孤立元素（无依赖且无被引用）

### 2. 交叉引用验证 🔗

- 验证文档间链接有效性
- 检查 THEOREM-REGISTRY.md 同步状态
- 检测重复编号
- 识别注册表孤儿和未登记元素

### 3. 可视化生成 📊

- 自动生成 Mermaid 依赖图
- 导出 Neo4j 兼容的 CSV 文件
- 生成 Graphviz DOT 文件

### 4. 报告输出 📄

- Markdown 格式验证报告
- JSON 格式详细数据
- 依赖覆盖率统计
- 关键路径识别
- 彩色终端输出

## 安装

### 环境要求

- Python 3.8 或更高版本
- 无需外部依赖（仅使用 Python 标准库）

### 安装步骤

```bash
# 1. 进入工具目录
cd tools/

# 2. 验证 Python 版本
python --version  # 应显示 3.8 或更高

# 3. （可选）创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 4. 无需安装依赖，工具仅使用标准库
```

## 快速开始

### 基本用法

```bash
# 在当前目录运行验证（假设项目根目录为当前目录）
python theorem-dependency-validator.py

# 指定项目根目录
python theorem-dependency-validator.py -r /path/to/AnalysisDataFlow

# 指定输出目录
python theorem-dependency-validator.py -o ./my-reports
```

### 完整示例

```bash
# 1. 进入项目目录
cd e:/_src/AnalysisDataFlow

# 2. 运行验证工具
python tools/theorem-dependency-validator.py -r . -o ./validation-output -v

# 3. 查看生成的报告
cat ./validation-output/validation-report.md
```

## 命令行参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--root` | `-r` | 项目根目录 | `.` (当前目录) |
| `--output` | `-o` | 输出目录 | `./validation-output` |
| `--verbose` | `-v` | 启用详细输出 | `False` |
| `--no-color` | - | 禁用彩色输出 | `False` |
| `--scan-dirs` | - | 要扫描的目录列表 | `Struct Knowledge Flink` |

### 参数示例

```bash
# 详细输出模式
python theorem-dependency-validator.py -v

# 禁用颜色（适用于输出到文件）
python theorem-dependency-validator.py --no-color > report.txt

# 只扫描特定目录
python theorem-dependency-validator.py --scan-dirs Struct Flink

# 完整参数示例
python theorem-dependency-validator.py \
    -r /path/to/project \
    -o ./output \
    -v \
    --scan-dirs Struct Knowledge Flink
```

## 输出文件

运行工具后，将在输出目录生成以下文件：

### 报告文件

| 文件 | 格式 | 说明 |
|------|------|------|
| `validation-report.md` | Markdown | 人类可读的验证报告 |
| `validation-report.json` | JSON | 机器可读的详细数据 |

### 可视化文件

| 文件 | 格式 | 说明 |
|------|------|------|
| `dependency-graph.mermaid` | Mermaid | 依赖关系图（前50个节点） |
| `dependency-graph.dot` | Graphviz DOT | 完整依赖图 |
| `neo4j-nodes.csv` | CSV | Neo4j 图数据库节点导入文件 |
| `neo4j-edges.csv` | CSV | Neo4j 图数据库边导入文件 |

## 报告解读

### 验证报告结构

```markdown
# 定理依赖验证报告

## 摘要
- 扫描文件数: X
- 发现元素数: Y
- 问题总数: Z

## 统计概览
- 按类型分布
- 按阶段分布
- 形式化等级分布
- 依赖覆盖率

## 关键路径
# 最长的依赖链

## 问题详情
- 错误 (ERROR)
- 警告 (WARNING)
- 信息 (INFO)
```

### 问题代码说明

| 代码 | 严重程度 | 说明 |
|------|----------|------|
| `DUPLICATE_ID` | ERROR | 重复的元素编号 |
| `CIRCULAR_DEPENDENCY` | ERROR | 循环依赖 detected |
| `MISSING_DEPENDENCY` | WARNING | 依赖的元素不存在 |
| `REGISTRY_ORPHAN` | WARNING | 注册表中有但文档中不存在 |
| `NOT_IN_REGISTRY` | WARNING | 文档中有但未在注册表登记 |
| `ORPHANED_ELEMENT` | INFO | 孤立元素（非基础层） |

## 使用场景

### 场景1: 日常验证

```bash
# 在开发过程中快速验证
python theorem-dependency-validator.py -v
```

### 场景2: CI/CD 集成

```bash
# 在持续集成中运行，检查是否有错误
python theorem-dependency-validator.py --no-color
# 检查退出码，非0表示有错误
```

### 场景3: 生成可视化

```bash
# 生成 Graphviz 图
python theorem-dependency-validator.py -o ./viz

# 转换为 PNG（需要安装 Graphviz）
dot -Tpng ./viz/dependency-graph.dot -o dependency-graph.png
```

### 场景4: Neo4j 导入

```bash
# 1. 生成 CSV 文件
python theorem-dependency-validator.py -o ./neo4j-import

# 2. 使用 Neo4j 导入工具
cypher-shell -u neo4j -p password '
    LOAD CSV WITH HEADERS FROM "file:///neo4j-nodes.csv" AS row
    CREATE (e:Element {
        id: row.elementId,
        name: row.name,
        type: row.type,
        stage: row.stage
    });
'
```

## 架构说明

### 类结构

```
TheoremDependencyValidator
├── scan_markdown_files()      # 扫描 Markdown 文件
├── validate_dependencies()    # 验证依赖完整性
├── detect_circular_deps()     # 检测循环依赖
├── identify_orphaned()        # 识别孤立元素
├── check_registry_sync()      # 检查注册表同步
├── generate_*()               # 各种输出生成器
└── calculate_coverage()       # 计算覆盖率
```

### 数据模型

```python
FormalElement
├── id: str              # Thm-S-01-01
├── element_type: Enum   # THEOREM/DEFINITION/LEMMA/PROPOSITION/COROLLARY
├── stage: str           # S/K/F
├── doc_num: str         # 01
├── seq_num: str         # 01
├── name: str            # 元素名称
├── file_path: str       # 所在文件
├── line_number: int     # 行号
├── formal_level: str    # L1-L6
├── dependencies: list   # 依赖的元素ID列表
└── referenced_by: list  # 被引用的元素ID列表
```

## 集成到 CI/CD

### GitHub Actions 示例

```yaml
name: Theorem Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Run theorem validation
        run: |
          python tools/theorem-dependency-validator.py \
            -r . \
            -o ./validation-output \
            --no-color

      - name: Upload reports
        uses: actions/upload-artifact@v3
        with:
          name: validation-reports
          path: ./validation-output/

      - name: Check for errors
        run: |
          # 如果有 ERROR 级别的问题，返回非0退出码
          if grep -q '"severity": "ERROR"' ./validation-output/validation-report.json; then
            echo "发现验证错误"
            exit 1
          fi
```

## 故障排除

### 问题1: 扫描不到元素

**症状**: 报告中的元素数为0
**解决**:

1. 检查 `--root` 参数是否正确指向项目根目录
2. 确认 `--scan-dirs` 包含正确的目录名
3. 检查 Markdown 文件中的定理格式是否符合规范

### 问题2: 编码错误

**症状**: `UnicodeDecodeError`
**解决**:

- 确保所有 Markdown 文件使用 UTF-8 编码
- 在 Windows 上使用 `--no-color` 避免编码问题

### 问题3: 内存不足

**症状**: 扫描大项目时崩溃
**解决**:

- 分批扫描不同的目录
- 限制 `--scan-dirs` 只扫描需要的目录

## 开发与扩展

### 添加新的检测规则

在 `TheoremDependencyValidator` 类中添加新方法：

```python
def check_custom_rule(self):
    """自定义检查规则"""
    for element_id, element in self.elements.items():
        # 自定义逻辑
        if some_condition:
            self.issues.append(ValidationIssue(
                severity=Severity.WARNING,
                code="CUSTOM_RULE",
                message=f"自定义问题: {element_id}",
                element_id=element_id,
                suggestion="建议如何修复"
            ))
```

### 添加新的输出格式

```python
def generate_custom_output(self, output_path: str):
    """生成自定义格式输出"""
    data = {
        "elements": [e.id for e in self.elements.values()],
        "issues": len(self.issues)
    }
    with open(output_path, 'w') as f:
        json.dump(data, f)
```

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0.0 | 2026-04-11 | 初始版本，完整功能实现 |

## 许可证

本项目遵循与 AnalysisDataFlow 相同的许可证。

## 贡献

欢迎提交 Issue 和 PR！

---

*由 AnalysisDataFlow 自动化团队开发维护*
