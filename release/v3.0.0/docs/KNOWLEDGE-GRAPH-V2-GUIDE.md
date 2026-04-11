# AnalysisDataFlow 知识图谱 v2.0 架构指南

> **版本**: v2.0 | **更新日期**: 2026-04-08 | **状态**: 技术预研完成

---

## 目录

- [AnalysisDataFlow 知识图谱 v2.0 架构指南](#analysisdataflow-知识图谱-v20-架构指南)
  - [目录](#目录)
  - [概述](#概述)
    - [核心升级](#核心升级)
    - [系统架构](#系统架构)
  - [架构设计](#架构设计)
    - [1. 前端层](#1-前端层)
      - [React 组件架构](#react-组件架构)
      - [组件层次](#组件层次)
    - [2. AI/ML 服务层](#2-aiml-服务层)
      - [2.1 语义搜索引擎 (SemanticSearchEngine)](#21-语义搜索引擎-semanticsearchengine)
      - [2.2 强化学习推荐器 (DQNAgent)](#22-强化学习推荐器-dqnagent)
      - [2.3 图神经网络关系挖掘 (GNNLinkPredictor)](#23-图神经网络关系挖掘-gnnlinkpredictor)
    - [3. 数据处理层](#3-数据处理层)
      - [3.1 概念嵌入生成器](#31-概念嵌入生成器)
      - [3.2 强化学习路径推荐器](#32-强化学习路径推荐器)
      - [3.3 隐式关系挖掘器](#33-隐式关系挖掘器)
  - [部署指南](#部署指南)
    - [环境要求](#环境要求)
    - [数据准备](#数据准备)
    - [启动前端](#启动前端)
  - [API文档](#api文档)
    - [Semantic Search API](#semantic-search-api)
    - [Learning Path API](#learning-path-api)
    - [Relation Discovery API](#relation-discovery-api)
  - [使用示例](#使用示例)
    - [示例1: 语义搜索](#示例1-语义搜索)
    - [示例2: 生成学习路径](#示例2-生成学习路径)
    - [示例3: 发现隐式关系](#示例3-发现隐式关系)
  - [性能优化](#性能优化)
    - [1. 嵌入缓存](#1-嵌入缓存)
    - [2. 索引优化](#2-索引优化)
    - [3. GNN训练优化](#3-gnn训练优化)
  - [故障排除](#故障排除)
    - [问题1: 语义搜索返回空结果](#问题1-语义搜索返回空结果)
    - [问题2: GNN训练内存不足](#问题2-gnn训练内存不足)
    - [问题3: 推荐路径质量不高](#问题3-推荐路径质量不高)
    - [问题4: 3D可视化性能低](#问题4-3d可视化性能低)
  - [路线图](#路线图)
    - [v2.1 (计划中)](#v21-计划中)
    - [v2.2 (计划中)](#v22-计划中)
  - [参考](#参考)

---

## 概述

知识图谱 v2.0 是 AnalysisDataFlow 项目的智能化知识管理系统，从 v1.0 的静态 D3.js 可视化升级到**交互式 React + 3D 可视化 + AI 增强**的现代架构。

### 核心升级

| 能力 | v1.0 | v2.0 |
|------|------|------|
| 前端框架 | 静态 D3.js | React 18 + TypeScript |
| 可视化 | 2D 力导向图 | 3D 力导向 + Three.js |
| 搜索 | 简单关键词过滤 | 语义搜索 (Sentence-BERT) |
| 推荐 | 基于 PageRank | 强化学习 (DQN/PPO) |
| 关系发现 | 仅显式关系 | GNN 隐式关系挖掘 |

### 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        知识图谱 v2.0 架构                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    前端层 (Frontend)                      │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │  │
│  │  │ knowledge-   │  │   React 18   │  │   Three.js   │   │  │
│  │  │ graph-v4.html│  │  Components  │  │    3D Viz    │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   AI/ML 服务层                            │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │  │
│  │  │  Semantic    │  │      RL      │  │     GNN      │   │  │
│  │  │    Search    │  │RecommenderV2 │  │Link Predictor│   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   数据处理层                              │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │  │
│  │  │  Concept     │  │   Learning   │  │   Implicit   │   │  │
│  │  │  Embedding   │  │    Path      │  │   Relation   │   │  │
│  │  │  Generator   │  │RecommenderV2 │  │    Miner     │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   数据存储层                              │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │  │
│  │  │   graph-     │  │   concept-   │  │   learning-  │   │  │
│  │  │  data.json   │  │embeddings.*  │  │   path.json  │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 架构设计

### 1. 前端层

#### React 组件架构

```typescript
// 核心组件接口
interface KnowledgeGraphV2 {
  // 语义搜索
  semanticSearch(query: string): Promise<Concept[]>;

  // 动态学习路径
  generateLearningPath(goal: string, level: Level): Promise<Path>;

  // 关系发现
  discoverImplicitRelations(concept: Concept): Promise<Relation[]>;

  // 3D可视化
  render3DGraph(container: HTMLElement): void;
}
```

#### 组件层次

```
knowledge-graph-v4.html
├── App (KnowledgeGraphApp)
│   ├── Header
│   ├── Sidebar
│   │   ├── TabNavigation
│   │   ├── SearchPanel (Semantic Search)
│   │   ├── FilterPanel
│   │   ├── PathFinder
│   │   └── NodeDetails
│   ├── GraphContainer
│   │   ├── D3Graph (2D Mode)
│   │   ├── ThreeJSGraph (3D Mode)
│   │   ├── Toolbar
│   │   └── StatsBar
│   └── Tooltip
```

### 2. AI/ML 服务层

#### 2.1 语义搜索引擎 (SemanticSearchEngine)

```python
class SemanticSearchEngine:
    """
    基于 Sentence-BERT 的语义搜索
    - 概念嵌入生成
    - 相似度计算 (Cosine Similarity)
    - 快速索引 (FAISS/Annoy)
    """

    async def search(query: str, limit: int = 10) -> List[SearchResult]:
        # 1. 编码查询
        query_embedding = model.encode(query)

        # 2. 相似度搜索
        similarities = cosine_similarity(query_embedding, concept_embeddings)

        # 3. 返回Top-K结果
        return top_k_results(similarities, limit)
```

#### 2.2 强化学习推荐器 (DQNAgent)

```python
class DQNAgent:
    """
    基于深度Q网络的学习路径推荐
    - 状态: 用户知识状态向量
    - 动作: 选择下一个学习概念
    - 奖励: 学习进度 + 知识覆盖 + 难度匹配
    """

    def select_action(state: np.ndarray, valid_actions: List[int]) -> int:
        # ε-greedy策略
        if random() < epsilon:
            return random.choice(valid_actions)
        return argmax(Q_network(state))

    def calculate_reward(action: str) -> float:
        reward = 1.0  # 基础奖励
        reward += goal_bonus(action)  # 目标达成奖励
        reward += unlock_bonus(action)  # 解锁新内容奖励
        reward -= difficulty_penalty(action)  # 难度不匹配惩罚
        return reward
```

#### 2.3 图神经网络关系挖掘 (GNNLinkPredictor)

```python
class GNNLinkPredictor(nn.Module):
    """
    基于GCN/GAT的链接预测
    - 节点编码: GCNConv layers
    - 链接解码: MLP predictor
    - 发现隐式关系
    """

    def forward(self, x, edge_index):
        # GCN编码
        z = self.encode(x, edge_index)

        # 预测链接概率
        return self.decode(z, edge_index)
```

### 3. 数据处理层

#### 3.1 概念嵌入生成器

**文件**: `.scripts/kg-v2/concept-embedding-generator.py`

**功能**:

1. 从 THEOREM-REGISTRY.md 提取形式化元素
2. 使用 Sentence-BERT 生成 384 维嵌入
3. 构建 FAISS/Annoy 索引
4. 输出相似概念对

**输出文件**:

- `concept-embeddings.json` - 元数据
- `concept-embeddings.npy` - NumPy嵌入矩阵
- `concept-embeddings.h5` - HDF5格式
- `similarity-pairs.json` - 高相似度概念对
- `concept-index.ann` - Annoy索引
- `concept-index.faiss` - FAISS索引

#### 3.2 强化学习路径推荐器

**文件**: `.scripts/kg-v2/learning-path-recommender-v2.py`

**功能**:

1. 知识图谱环境建模 (KnowledgeGraphEnv)
2. DQN智能体训练
3. 动态路径生成
4. 多目标优化

**核心算法**:

```
推荐得分 = 重要性(25%) + 依赖满足度(30%) + 进度(20%) + 类型(15%) + 层次(10%)
```

#### 3.3 隐式关系挖掘器

**文件**: `.scripts/kg-v2/implicit-relation-miner.py`

**功能**:

1. GCN/GAT模型训练
2. 链接预测
3. 隐式关系发现
4. 关系类型推断

---

## 部署指南

### 环境要求

```bash
# Python 3.8+
python --version

# Node.js 16+ (for React build)
node --version

# 依赖安装
pip install sentence-transformers torch torch-geometric \
    numpy scikit-learn networkx h5py tqdm
```

### 数据准备

```bash
# 1. 生成概念嵌入
cd e:\_src\AnalysisDataFlow
python .scripts/kg-v2/concept-embedding-generator.py

# 2. 训练强化学习推荐器
python .scripts/kg-v2/learning-path-recommender-v2.py --train --epochs 1000

# 3. 挖掘隐式关系
python .scripts/kg-v2/implicit-relation-miner.py --train --epochs 200
```

### 启动前端

```bash
# 方式1: 直接打开 (推荐)
start knowledge-graph-v4.html

# 方式2: 使用 Python HTTP 服务器
python -m http.server 8000
# 访问 http://localhost:8000/knowledge-graph-v4.html

# 方式3: 使用 Node.js serve
npx serve .
```

---

## API文档

### Semantic Search API

```typescript
interface SemanticSearchRequest {
  query: string;
  limit?: number;
  filters?: {
    types?: string[];
    stages?: string[];
  };
}

interface SemanticSearchResponse {
  results: {
    id: string;
    label: string;
    type: string;
    score: number;
    description?: string;
  }[];
  total: number;
  query_time_ms: number;
}

// 使用示例
const results = await semanticSearch({
  query: "流计算确定性",
  limit: 10
});
```

### Learning Path API

```typescript
interface GeneratePathRequest {
  goal: string | string[];
  current_knowledge?: string[];
  time_budget?: number;  // hours
  difficulty_preference?: number;  // 0-1
}

interface GeneratePathResponse {
  path: {
    step: number;
    concept: string;
    label: string;
    difficulty: number;
    estimated_time: number;
    prerequisites: string[];
  }[];
  total_time: number;
  coverage_score: number;
  difficulty_curve: number[];
}

// 使用示例
const path = await generateLearningPath({
  goal: ["Thm-S-08-02", "Thm-F-02-01"],
  time_budget: 20
});
```

### Relation Discovery API

```typescript
interface RelationDiscoveryRequest {
  concept_id: string;
  discovery_types?: string[];  // ['similarity', 'structural', 'gnn']
  confidence_threshold?: number;
}

interface RelationDiscoveryResponse {
  relations: {
    source: string;
    target: string;
    type: string;
    confidence: number;
    evidence: string[];
    discovered_by: string;
  }[];
}

// 使用示例
const relations = await discoverImplicitRelations({
  concept_id: "Thm-S-01-01",
  confidence_threshold: 0.8
});
```

---

## 使用示例

### 示例1: 语义搜索

```javascript
// 在知识图谱页面中
const searchResults = await semanticSearch("Exactly-Once语义");
console.log(searchResults);
// Output:
// [
//   { id: "Thm-S-08-02", label: "Exactly-Once正确性", score: 0.95 },
//   { id: "Def-S-08-01", label: "Exactly-Once定义", score: 0.92 },
//   ...
// ]
```

### 示例2: 生成学习路径

```javascript
// 设定学习目标
const path = await generateLearningPath({
  goal: ["Thm-F-02-01", "Thm-F-02-02"],  // Flink核心定理
  current_knowledge: ["Def-S-01-01"],     // 已掌握基础
  time_budget: 15
});

// 路径结果
console.log(path.steps);
// [
//   { step: 1, concept: "Def-S-08-01", label: "Exactly-Once定义", ... },
//   { step: 2, concept: "Thm-S-08-02", label: "Exactly-Once正确性", ... },
//   { step: 3, concept: "Def-F-02-01", label: "Flink Checkpoint", ... },
//   ...
// ]
```

### 示例3: 发现隐式关系

```python
# Python API 使用
from implicit_relation_miner import ImplicitRelationMiner

miner = ImplicitRelationMiner(graph, loader)
miner.train_gnn(epochs=200)

# 发现与"Thm-S-01-01"相关的隐式关系
relations = miner.discover_by_similarity(threshold=0.8)

for r in relations[:5]:
    print(f"{r.source_id} --[{r.relation_type}]--> {r.target_id} ({r.confidence:.2f})")
```

---

## 性能优化

### 1. 嵌入缓存

```python
# 预计算并缓存概念嵌入
@lru_cache(maxsize=10000)
def get_concept_embedding(concept_id: str) -> np.ndarray:
    return embedding_cache[concept_id]
```

### 2. 索引优化

| 索引类型 | 适用场景 | 构建时间 | 查询时间 |
|----------|----------|----------|----------|
| FAISS (Flat) | 精确搜索 | 快 | O(n) |
| FAISS (IVF) | 大规模近似 | 中等 | O(√n) |
| Annoy | 内存受限 | 慢 | O(log n) |

### 3. GNN训练优化

```python
# 使用GPU加速
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# 批量训练
batch_size = 256
data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
```

---

## 故障排除

### 问题1: 语义搜索返回空结果

**原因**: 概念嵌入文件未生成

**解决**:

```bash
python .scripts/kg-v2/concept-embedding-generator.py
```

### 问题2: GNN训练内存不足

**解决**:

```bash
# 减少隐藏层维度
python .scripts/kg-v2/implicit-relation-miner.py --hidden-dim 32

# 或使用CPU
export CUDA_VISIBLE_DEVICES=""
```

### 问题3: 推荐路径质量不高

**解决**:

```bash
# 增加训练轮数
python .scripts/kg-v2/learning-path-recommender-v2.py --train --epochs 2000

# 调整奖励函数参数 (编辑源码)
# weights = { importance: 0.3, dependency: 0.35, ... }
```

### 问题4: 3D可视化性能低

**解决**:

- 减少同时渲染的节点数 (< 1000)
- 使用 Level-of-Detail (LOD) 技术
- 禁用阴影和后期效果

---

## 路线图

### v2.1 (计划中)

- [ ] 实时协作编辑
- [ ] 多模态嵌入 (文本+图像)
- [ ] 增量学习更新

### v2.2 (计划中)

- [ ] 知识图谱版本控制
- [ ] A/B测试框架
- [ ] 用户行为分析仪表板

---

## 参考

- [Sentence-BERT Documentation](https://www.sbert.net/)
- [PyTorch Geometric](https://pytorch-geometric.readthedocs.io/)
- [D3.js v7 API](https://d3js.org/d3-force)
- [Three.js Documentation](https://threejs.org/docs/)

---

*本指南由知识图谱 v2.0 自动生成系统创建*
