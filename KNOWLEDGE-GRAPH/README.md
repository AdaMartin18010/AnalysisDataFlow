# AnalysisDataFlow 知识图谱可视化系统

> **版本**: v1.0 | **更新日期**: 2026-04-04 | **状态**: Production

## 📋 目录

- [系统概述](#系统概述)
- [快速开始](#快速开始)
- [图谱类型](#图谱类型)
- [可视化界面](#可视化界面)
- [导出格式](#导出格式)
- [自动提取](#自动提取)
- [API参考](#api参考)

---

## 系统概述

AnalysisDataFlow 知识图谱可视化系统是一个完整的知识管理和可视化解决方案，包含：

### 组件架构

```
KNOWLEDGE-GRAPH/
├── data/                          # 图谱数据文件
│   ├── streaming-theory-graph.json    # 流计算理论图谱
│   ├── flink-technology-graph.json    # Flink技术图谱
│   ├── design-patterns-graph.json     # 设计模式图谱
│   ├── concept-dependency-graph.json  # 概念依赖关系图
│   ├── tech-decision-graph.json       # 技术选型决策图
│   └── learning-path-graph.json       # 学习路径图
├── scripts/                       # 自动化脚本
│   ├── export_formats.py          # 格式导出工具
│   ├── extract_entities.py        # 实体提取器
│   └── auto_update.py             # 自动更新脚本
├── visualizations/                # 可视化界面
│   ├── index.html                 # 主界面
│   └── graph-visualizer.js        # D3.js可视化引擎
└── README.md                      # 本文档
```

### 功能特性

| 特性 | 描述 |
|------|------|
| 🎯 **主题图谱** | 流计算理论、Flink技术、设计模式三大主题 |
| 🔗 **关系图谱** | 概念依赖、技术选型、学习路径关系 |
| 🖥️ **交互可视化** | D3.js实现，支持缩放、拖拽、搜索 |
| 📤 **多格式导出** | JSON, GraphML, Cypher, GEXF, DOT |
| 🤖 **自动提取** | 从Markdown自动提取实体和关系 |
| 🔄 **自动更新** | 监控文档变化，自动更新图谱 |

---

## 快速开始

### 1. 启动可视化界面

**方式一：直接打开**

```bash
# 使用浏览器打开
start KNOWLEDGE-GRAPH/visualizations/index.html
```

**方式二：使用Python HTTP服务器**

```bash
cd KNOWLEDGE-GRAPH/visualizations
python -m http.server 8080
# 访问 http://localhost:8080
```

**方式三：使用 VS Code Live Server**

1. 安装 "Live Server" 插件
2. 右键 `index.html` → "Open with Live Server"

### 2. 导出图谱数据

```bash
cd KNOWLEDGE-GRAPH

# 导出所有格式
python scripts/export_formats.py data/streaming-theory-graph.json -o exports

# 导出特定格式
python scripts/export_formats.py data/flink-technology-graph.json -f cypher -o exports
```

### 3. 自动提取实体

```bash
# 从文档提取实体
cd KNOWLEDGE-GRAPH
python scripts/extract_entities.py --base-dir .. --output extracted.json Struct Knowledge Flink

# 构建依赖图
python scripts/extract_entities.py --build-deps --output deps.json ..
```

### 4. 自动更新图谱

```bash
# 运行一次更新
cd KNOWLEDGE-GRAPH
python scripts/auto_update.py --once

# 持续监控
python scripts/auto_update.py --watch --interval 60
```

---

## 图谱类型

### 1. 主题知识图谱

#### 流计算理论图谱

- **文件**: `data/streaming-theory-graph.json`
- **节点**: 53个概念节点
- **边**: 68条关系边
- **内容**: 涵盖Dataflow模型、时间语义、窗口机制、一致性模型等核心理论

#### Flink技术图谱

- **文件**: `data/flink-technology-graph.json`
- **节点**: 58个技术组件
- **边**: 74条依赖关系
- **内容**: 涵盖Flink架构、API、状态管理、容错机制、连接器生态

#### 设计模式图谱

- **文件**: `data/design-patterns-graph.json`
- **节点**: 52个设计模式
- **边**: 60条关系
- **内容**: 涵盖架构模式、弹性模式、流处理模式、CEP模式

### 2. 关系图谱

#### 概念依赖关系图

- **文件**: `data/concept-dependency-graph.json`
- **层次**: 5层概念依赖
- **用途**: 理解学习前置条件

#### 技术选型决策图

- **文件**: `data/tech-decision-graph.json`
- **决策点**: 11个决策节点
- **技术选项**: 17个技术选择

#### 学习路径图

- **文件**: `data/learning-path-graph.json`
- **阶段**: 10个学习阶段
- **预计时长**: 14周完整路径

---

## 可视化界面

### 界面布局

```
┌─────────────────────────────────────────────────────────────┐
│ 🔮 AnalysisDataFlow 知识图谱                    [+] [−] [⊡] │
├──────────────┬──────────────────────────────────────────────┤
│              │                                              │
│  📊 选择图谱  │                                              │
│  [流计算理论▼]│                   知识图谱                    │
│              │              ╭───────────╮                   │
│  🔍 搜索     │    ╭────────│  Dataflow │────────╮          │
│  [________]  │    │        ╰─────┬─────╯        │          │
│              │  ╭─┴─╮            │            ╭─┴─╮        │
│  ☑ 文档      │  │Event         Watermark     State│        │
│  ☑ 定理      │  │Time              │         Mgmt │        │
│  ☑ 定义      │  ╰──┬──────────────┼────────────┬──╯        │
│              │     │         ╭────┴────╮       │           │
│  ─────────   │  ╭──┴──╮      │ Window  │    ╭─┴──╮         │
│              │  │Exactly      ╰────┬────╯    │Checkpoint│  │
│  📈 图例     │  │Once              │         ╰──────╯      │
│  ● 基础     │  ╰─────┴─────────────┴────────────────       │
│  ● 机制     │                                              │
│              │                                              │
│  ─────────   │  节点: 53  边: 68  类别: 15                 │
│              │                                              │
│  📋 节点详情 │                                              │
│  [选中节点]  │                                              │
│              │                                              │
└──────────────┴──────────────────────────────────────────────┘
```

### 交互功能

| 操作 | 说明 |
|------|------|
| **拖拽节点** | 调整节点位置 |
| **滚轮** | 缩放视图 |
| **点击节点** | 选中并查看详情 |
| **双击空白** | 重置视图 |
| **搜索框** | 快速定位节点 |
| **类型过滤** | 按类别显示/隐藏 |

### 工具栏按钮

- `+` / `−` : 放大 / 缩小
- `⊡` : 适应窗口
- `↺` : 重置视图
- `⬇` : 导出图谱

---

## 导出格式

### 支持的格式

| 格式 | 扩展名 | 用途 |
|------|--------|------|
| JSON | `.json` | Web应用、JavaScript |
| GraphML | `.graphml` | Gephi, yEd, Cytoscape |
| Cypher | `.cypher` | Neo4j图数据库 |
| GEXF | `.gexf` | Gephi |
| DOT | `.dot` | Graphviz |

### 导出示例

```bash
# 导出为Neo4j Cypher
python scripts/export_formats.py data/streaming-theory-graph.json -f cypher -o exports

# 输出文件: exports/streaming-theory-graph.cypher
```

```cypher
// 在Neo4j中执行
MATCH (n) DETACH DELETE n;  // 清空现有数据
:source exports/streaming-theory-graph.cypher  // 导入数据

// 查询示例
MATCH (n:Concept)-[:REQUIRES]->(m:Concept)
RETURN n.label, m.label
```

---

## 自动提取

### 提取规则

实体提取器自动识别以下模式：

```python
PATTERNS = {
    # 形式化元素
    "theorem": r'`?(Thm-[A-Z]-\d{2}-\d{2})`?...',
    "definition": r'`?(Def-[A-Z]-\d{2}-\d{2})`?...',
    "lemma": r'`?(Lemma-[A-Z]-\d{2}-\d{2})`?...',

    # 章节标题
    "section": r'^##+\s+(.+)$',

    # 文档链接
    "doc_link": r'\[([^\]]+)\]\(([^)]+\.md)\)',

    # Flink类引用
    "flink_class": r'`?(\w+Function|(\w+)Sink|...)`?',
}
```

### 提取结果示例

```json
{
  "entities": [
    {
      "id": "Thm-S-01-01",
      "label": "流计算统一理论存在性定理",
      "type": "theorem",
      "category": "formal",
      "description": "...",
      "source_file": "Struct/01.01-unified-streaming-theory.md",
      "line_number": 45
    }
  ],
  "relations": [
    {
      "source": "Struct_01.01-unified-streaming-theory",
      "target": "Thm-S-01-01",
      "type": "contains",
      "label": "包含"
    }
  ]
}
```

---

## API参考

### GraphExporter 类

```python
from export_formats import GraphExporter

# 加载图谱数据
with open("data/streaming-theory-graph.json") as f:
    graph_data = json.load(f)

exporter = GraphExporter(graph_data)

# 导出为各种格式
json_str = exporter.to_json()
graphml_str = exporter.to_graphml()
cypher_str = exporter.to_cypher()
gexf_str = exporter.to_gexf()
dot_str = exporter.to_dot()

# 批量导出
exports = exporter.export_all(Path("./exports"))
```

### MarkdownEntityExtractor 类

```python
from extract_entities import MarkdownEntityExtractor

extractor = MarkdownEntityExtractor(base_dir=Path(".."))

# 从单个文件提取
entities, relations = extractor.extract_from_file(Path("../Struct/01.01-theory.md"))

# 从目录批量提取
result = extractor.extract_from_directory(Path("Struct"))

# 构建依赖图
dep_graph = extractor.build_dependency_graph()
```

### GraphAutoUpdater 类

```python
from auto_update import GraphAutoUpdater

updater = GraphAutoUpdater(base_dir=Path(".."))

# 更新特定图谱
updater.update_graph("streaming-theory", ["Struct"])

# 导出所有格式
updater.export_all_formats("streaming-theory")

# 运行完整更新
updater.run_full_update()
```

---

## 数据结构规范

### 图谱JSON Schema

```json
{
  "name": "图谱名称",
  "description": "图谱描述",
  "version": "1.0",
  "lastUpdated": "2026-04-04",
  "nodes": [
    {
      "id": "唯一标识",
      "label": "显示标签",
      "type": "节点类型",
      "category": "分类",
      "description": "描述",
      "level": 1,
      "color": "#hexcolor"
    }
  ],
  "edges": [
    {
      "source": "源节点ID",
      "target": "目标节点ID",
      "type": "关系类型",
      "label": "关系标签",
      "weight": 1.0
    }
  ],
  "categories": {
    "category-id": {
      "label": "显示名称",
      "color": "#hexcolor"
    }
  },
  "relationTypes": {
    "relation-id": {
      "label": "显示名称",
      "color": "#hexcolor",
      "style": "solid|dashed|dotted"
    }
  }
}
```

---

## 故障排除

### 可视化界面无法加载

1. 检查数据文件是否存在: `data/*.json`
2. 确认使用HTTP服务器访问（不是file://协议）
3. 查看浏览器控制台错误信息

### 实体提取失败

1. 确认Python版本 >= 3.7
2. 检查文件编码为UTF-8
3. 验证文档路径正确

### 导出格式错误

1. 确认输入JSON格式正确
2. 检查输出目录可写
3. 验证文件路径无特殊字符

---

## 参考

- [D3.js Documentation](https://d3js.org/)
- [GraphML Specification](http://graphml.graphdrawing.org/)
- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/)
- [AnalysisDataFlow 项目文档](../README.md)

---

*本系统由 AnalysisDataFlow 项目自动生成和维护。*
