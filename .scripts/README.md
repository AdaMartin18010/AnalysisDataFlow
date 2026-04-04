# Knowledge Graph Generator

AnalysisDataFlow 知识图谱生成工具

## 功能特性

- 📄 **文档扫描**: 自动扫描 Struct/、Knowledge/、Flink/ 目录下的所有 Markdown 文件
- 🔗 **关系提取**: 解析文档间的引用、依赖关系
- 📊 **多格式输出**: 支持 Cytoscape JSON、D3.js JSON、Graphviz DOT 格式
- 🌐 **交互式可视化**: 生成交互式 HTML 页面，支持缩放、拖拽、筛选
- 📚 **学习路径**: 生成结构化的学习路径页面
- 🔄 **CI/CD 集成**: 支持 GitHub Actions 自动更新

## 使用方法

### 本地运行

```bash
# 基础用法
python .scripts/knowledge-graph-generator.py

# 指定项目路径和输出目录
python .scripts/knowledge-graph-generator.py --base-path /path/to/project --output visuals

# 只扫描特定目录
python .scripts/knowledge-graph-generator.py --directories Struct Knowledge
```

### 查看结果

```bash
# 启动本地服务器查看交互式图谱
cd visuals
python -m http.server 8000

# 在浏览器中打开
open http://localhost:8000/knowledge-graph.html
open http://localhost:8000/learning-path.html
```

## 输出文件

| 文件 | 说明 |
|------|------|
| `knowledge-graph-cytoscape.json` | Cytoscape.js 格式图谱数据 |
| `knowledge-graph-d3.json` | D3.js 格式图谱数据 |
| `knowledge-hierarchy.json` | 层级结构数据 |
| `knowledge-graph.dot` | Graphviz DOT 格式 |
| `knowledge-graph.html` | 交互式图谱页面 |
| `learning-path.html` | 学习路径页面 |

## 使用 Graphviz 生成静态图

```bash
# 生成 SVG
dot -Tsvg visuals/knowledge-graph.dot -o visuals/knowledge-graph.svg

# 生成 PNG
dot -Tpng visuals/knowledge-graph.dot -o visuals/knowledge-graph.png -Gdpi=300

# 生成 PDF
dot -Tpdf visuals/knowledge-graph.dot -o visuals/knowledge-graph.pdf
```

## CI/CD 集成

已配置 GitHub Actions 工作流 (`.github/workflows/knowledge-graph.yml`)：

- 当 Markdown 文件变更时自动触发
- 自动生成并提交更新的图谱
- 支持手动触发 (`workflow_dispatch`)

## 数据模型

### 节点类型

- `document`: Markdown 文档
- `concept`: 概念定义
- `theorem`: 定理
- `definition`: 定义
- `lemma`: 引理
- `proposition`: 命题
- `corollary`: 推论

### 边类型

- `references`: 文档引用
- `depends_on`: 依赖关系
- `relates_to`: 相关关系
- `proves`: 证明关系
- `defines`: 定义关系
- `extends`: 扩展关系

## 配置说明

### 节点属性

| 属性 | 说明 |
|------|------|
| `id` | 唯一标识符 |
| `label` | 显示标签 |
| `type` | 节点类型 |
| `category` | 类别 (Struct/Knowledge/Flink) |
| `level` | 形式化等级 (L1-L6) |
| `path` | 文件路径 |
| `description` | 文档描述 |
| `tags` | 标签列表 |
| `dependencies` | 依赖文档列表 |

### 边属性

| 属性 | 说明 |
|------|------|
| `source` | 源节点 ID |
| `target` | 目标节点 ID |
| `type` | 边类型 |
| `label` | 显示标签 |
| `weight` | 权重 |

## 扩展开发

### 添加新的节点类型

在 `DocumentParser` 类中扩展解析逻辑：

```python
def _extract_custom_elements(self, content: str, document_id: str):
    # 自定义提取逻辑
    pass
```

### 自定义可视化样式

在 `HTMLGenerator` 类中修改 Cytoscape 样式配置：

```javascript
style: [
    {
        selector: 'node[type="custom"]',
        style: {
            'background-color': '#custom-color'
        }
    }
]
```

## 依赖项

- Python 3.8+
- 标准库: `os`, `re`, `json`, `pathlib`, `dataclasses`, `collections`
- 前端: Cytoscape.js 3.26+, D3.js (可选)

## 许可证

与项目主许可证保持一致
