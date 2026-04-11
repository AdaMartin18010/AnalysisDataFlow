# 知识图谱管理和分析工具

一套用于知识库文档分析、概念提取、定理依赖分析和智能检索的Python工具集。

## 工具概览

| 工具 | 功能 | 输出 |
|------|------|------|
| `concept-map-builder.py` | 概念关系图谱构建器 | Cypher, GEXF, JSON |
| `theorem-dependency-analyzer.py` | 定理依赖关系分析器 | 依赖图, 关键路径 |
| `doc-similarity-analyzer.py` | 文档相似度分析器 | 相似度矩阵, 聚类 |
| `knowledge-search-engine.py` | 知识检索系统 | 倒排索引, 搜索界面 |

## 快速开始

### 安装依赖

```bash
cd .scripts/knowledge-graph
pip install -r requirements.txt
```

### 配置

编辑 `config.json` 配置文件：

```json
{
  "base_path": "../..",
  "source_directories": ["Struct", "Knowledge", "Flink"],
  "use_whoosh": true,
  "use_semantic": true
}
```

### 运行所有工具

```bash
# 1. 构建概念图谱
python concept-map-builder.py

# 2. 分析定理依赖
python theorem-dependency-analyzer.py

# 3. 分析文档相似度
python doc-similarity-analyzer.py

# 4. 构建搜索索引
python knowledge-search-engine.py index
```

## 工具详细说明

### 1. 概念关系图谱构建器

从所有文档中提取概念定义，构建概念关系图谱。

**功能：**

- 提取定义、定理、引理、命题、推论
- 识别概念间的依赖、引用、等价关系
- 生成Neo4j兼容的Cypher导入脚本
- 生成Gephi兼容的GEXF格式
- 计算概念中心性指标（PageRank、介数中心性等）

**使用：**

```bash
python concept-map-builder.py -c config.json
```

**输出：**

- `output/graph-data.cypher` - Neo4j导入脚本
- `output/graph.gexf` - Gephi可视化文件
- `output/concept-summary.json` - 概念摘要

### 2. 定理依赖关系分析器

解析定理、引理、命题之间的依赖关系。

**功能：**

- 提取证明中的依赖关系
- 构建依赖图
- 检测循环依赖
- 计算证明深度和复杂度
- 识别关键路径

**使用：**

```bash
# 完整分析
python theorem-dependency-analyzer.py

# 分析特定定理的关键路径
python theorem-dependency-analyzer.py -t "Thm-S-01-01"
```

**输出：**

- `output/theorem-dependencies.json` - 依赖关系数据
- `output/critical-path.txt` - 关键路径报告

### 3. 文档相似度分析器

使用TF-IDF和BERT嵌入计算文档相似度。

**功能：**

- TF-IDF和BERT嵌入计算
- 检测重复或高度相似内容
- 文档聚类（K-Means、层次聚类）
- 识别内容缺口
- 推荐相关文档

**使用：**

```bash
# 使用TF-IDF
python doc-similarity-analyzer.py --method tfidf

# 使用BERT（更准确但较慢）
python doc-similarity-analyzer.py --method bert
```

**输出：**

- `output/similarity-matrix.json` - 相似度矩阵
- `output/doc-clusters.json` - 聚类结果
- `output/doc-recommendations.json` - 文档推荐
- `output/content-gaps.json` - 内容缺口分析

### 4. 知识检索系统

构建倒排索引，支持全文搜索和语义搜索。

**功能：**

- 倒排索引（Whoosh）
- 全文搜索（支持布尔查询）
- 语义搜索（BERT嵌入）
- 混合搜索
- CLI和Web界面

**使用：**

```bash
# 构建索引
python knowledge-search-engine.py index

# 命令行界面
python knowledge-search-engine.py cli

# Web界面
python knowledge-search-engine.py web --port 5000
```

**CLI命令：**

- `/quit`, `/q` - 退出
- `/semantic`, `/s` - 切换语义搜索
- `/hybrid`, `/y` - 切换混合搜索
- `/type <type>` - 按类型过滤

**Web界面：**
访问 `http://localhost:5000`

## CI/CD集成

### GitHub Actions 示例

```yaml
name: Knowledge Graph Analysis

on:
  push:
    paths:
      - 'Struct/**'
      - 'Knowledge/**'
      - 'Flink/**'

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install -r .scripts/knowledge-graph/requirements.txt

      - name: Build concept map
        run: python .scripts/knowledge-graph/concept-map-builder.py

      - name: Analyze theorem dependencies
        run: python .scripts/knowledge-graph/theorem-dependency-analyzer.py

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: knowledge-graph-output
          path: .scripts/knowledge-graph/output/
```

## 输出可视化

### Neo4j 导入

```bash
# 使用cypher-shell导入
cypher-shell -u neo4j -p password < output/graph-data.cypher
```

### Gephi 可视化

1. 打开Gephi
2. 数据实验室 → 导入电子表格
3. 选择 `output/graph.gexf`

## API 文档

### 概念图谱构建器

```python
from concept_map_builder import ConceptMapBuilder

config = {
    'base_path': '.',
    'output_dir': 'output',
    'source_directories': ['Struct', 'Knowledge']
}

builder = ConceptMapBuilder(config)
builder.run()
```

### 定理依赖分析器

```python
from theorem_dependency_analyzer import TheoremDependencyAnalyzer

analyzer = TheoremDependencyAnalyzer(config)
analyzer.run()

# 获取关键路径
path = analyzer.analyzer.find_critical_path("Thm-S-01-01")
```

### 文档相似度分析器

```python
from doc_similarity_analyzer import DocSimilarityAnalyzer

analyzer = DocSimilarityAnalyzer(config)
analyzer.run()

# 获取相关文档
related = analyzer.calculator.get_related_documents("doc_id", top_k=5)
```

### 知识检索系统

```python
from knowledge_search_engine import KnowledgeSearchSystem

system = KnowledgeSearchSystem(config)
system.build_index()

# 搜索
results = system.search_engine.search_hybrid("checkpoint机制", top_k=10)
```

## 配置选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `base_path` | 项目根目录 | `../..` |
| `output_dir` | 输出目录 | `output` |
| `source_directories` | 源文档目录 | `["Struct", "Knowledge", "Flink"]` |
| `use_whoosh` | 启用Whoosh索引 | `true` |
| `use_semantic` | 启用语义搜索 | `true` |
| `similarity_method` | 相似度计算方法 | `tfidf` |
| `n_clusters` | 聚类数量 | `10` |
| `bert_model` | BERT模型名称 | `paraphrase-MiniLM-L3-v2` |

## 故障排除

### 内存不足

对于大型知识库，使用增量模式：

```json
{
  "enable_incremental": true,
  "cache_embeddings": false
}
```

### BERT模型下载慢

手动下载模型：

```bash
pip install huggingface-hub
huggingface-cli download sentence-transformers/paraphrase-MiniLM-L3-v2
```

### Whoosh索引损坏

删除索引目录重建：

```bash
rm -rf .scripts/knowledge-graph/index
python knowledge-search-engine.py index
```

## 贡献

欢迎提交Issue和PR！

## 许可证

MIT License
