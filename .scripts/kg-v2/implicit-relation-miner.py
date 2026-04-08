#!/usr/bin/env python3
"""
AnalysisDataFlow 知识图谱 v2.0 - 隐式关系挖掘器
基于图神经网络(GNN)的关系推理与隐式关系发现

功能:
1. 使用 GCN/GAT 学习节点嵌入
2. 基于嵌入相似度发现隐式关系
3. 关系类型预测与置信度计算
4. 知识图谱补全

依赖:
    pip install torch torch-geometric networkx numpy scikit-learn tqdm

Usage:
    python implicit-relation-miner.py
    python implicit-relation-miner.py --epochs 200 --hidden-dim 128
    python implicit-relation-miner.py --predict --source Thm-S-01-01 --target Def-S-01-02
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from collections import defaultdict
from datetime import datetime

import numpy as np
import networkx as nx
from tqdm import tqdm

# PyTorch and PyG imports
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch.utils.data import DataLoader
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("Warning: PyTorch not available, using NetworkX fallback")

try:
    from torch_geometric.nn import GCNConv, GATConv, GraphSAGE
    from torch_geometric.data import Data as PyGData
    PYG_AVAILABLE = True
except ImportError:
    PYG_AVAILABLE = False
    print("Warning: PyTorch Geometric not available")

try:
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import roc_auc_score, average_precision_score
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


# ============================================
# Configuration
# ============================================

PROJECT_ROOT = Path(__file__).parent.parent.parent
RELATION_TYPES = [
    'dependency',      # 依赖
    'citation',        # 引用
    'contains',        # 包含
    'instantiates',    # 实例化
    'evolves',         # 演进
    'similar',         # 相似 (隐式)
    'prerequisite',    # 前置知识 (隐式)
    'alternative',     # 替代方案 (隐式)
    'extension'        # 扩展 (隐式)
]


# ============================================
# Data Structures
# ============================================

@dataclass
class RelationPrediction:
    """关系预测结果"""
    source: str
    target: str
    relation_type: str
    confidence: float
    explanation: str


@dataclass
class ImplicitRelation:
    """隐式关系定义"""
    source_id: str
    target_id: str
    relation_type: str
    confidence: float
    evidence: List[str]
    discovered_by: str  # 'gnn', 'similarity', 'structural', 'ensemble'


# ============================================
# Graph Neural Network Models
# ============================================

class GCNLinkPredictor(nn.Module):
    """GCN链接预测模型"""
    
    def __init__(
        self,
        in_channels: int,
        hidden_channels: int,
        out_channels: int,
        num_layers: int = 3,
        dropout: float = 0.3
    ):
        super().__init__()
        
        self.convs = nn.ModuleList()
        self.convs.append(GCNConv(in_channels, hidden_channels))
        
        for _ in range(num_layers - 2):
            self.convs.append(GCNConv(hidden_channels, hidden_channels))
        
        self.convs.append(GCNConv(hidden_channels, out_channels))
        
        self.dropout = dropout
        self.predictor = nn.Sequential(
            nn.Linear(out_channels * 2, hidden_channels),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_channels, 1)
        )
    
    def encode(self, x, edge_index):
        """节点编码"""
        for conv in self.convs[:-1]:
            x = conv(x, edge_index)
            x = F.relu(x)
            x = F.dropout(x, p=self.dropout, training=self.training)
        
        x = self.convs[-1](x, edge_index)
        return x
    
    def decode(self, z, edge_index):
        """链接解码"""
        src, dst = edge_index
        features = torch.cat([z[src], z[dst]], dim=1)
        return torch.sigmoid(self.predictor(features)).squeeze()
    
    def forward(self, x, edge_index):
        z = self.encode(x, edge_index)
        return z


class GATLinkPredictor(nn.Module):
    """GAT链接预测模型 (带注意力机制)"""
    
    def __init__(
        self,
        in_channels: int,
        hidden_channels: int,
        out_channels: int,
        heads: int = 4,
        dropout: float = 0.3
    ):
        super().__init__()
        
        self.conv1 = GATConv(in_channels, hidden_channels, heads=heads, dropout=dropout)
        self.conv2 = GATConv(hidden_channels * heads, hidden_channels, heads=heads, dropout=dropout)
        self.conv3 = GATConv(hidden_channels * heads, out_channels, heads=1, concat=False, dropout=dropout)
        
        self.predictor = nn.Sequential(
            nn.Linear(out_channels * 2, hidden_channels),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_channels, 1)
        )
    
    def encode(self, x, edge_index):
        x = F.relu(self.conv1(x, edge_index))
        x = F.relu(self.conv2(x, edge_index))
        x = self.conv3(x, edge_index)
        return x
    
    def decode(self, z, edge_index):
        src, dst = edge_index
        features = torch.cat([z[src], z[dst]], dim=1)
        return torch.sigmoid(self.predictor(features)).squeeze()


# ============================================
# Knowledge Graph Loader
# ============================================

class KnowledgeGraphLoader:
    """知识图谱数据加载器"""
    
    def __init__(self, graph_path: Path):
        self.graph_path = graph_path
        self.graph = nx.DiGraph()
        self.node_features = {}
        self.node_to_idx = {}
        self.idx_to_node = {}
        self.edge_type_to_idx = {rt: i for i, rt in enumerate(RELATION_TYPES)}
    
    def load(self) -> nx.DiGraph:
        """加载知识图谱"""
        if not self.graph_path.exists():
            print(f"Graph file not found: {self.graph_path}")
            return self._create_sample_graph()
        
        with open(self.graph_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add nodes
        for node in data.get('nodes', []):
            node_id = node['id']
            self.graph.add_node(node_id, **node)
            
            # Create feature vector
            features = self._extract_node_features(node)
            self.node_features[node_id] = features
        
        # Add edges
        for edge in data.get('edges', []):
            source = edge.get('source', '')
            target = edge.get('target', '')
            
            if isinstance(source, dict):
                source = source.get('id', '')
            if isinstance(target, dict):
                target = target.get('id', '')
            
            if source and target:
                self.graph.add_edge(source, target, **edge)
        
        # Create index mappings
        nodes = sorted(self.graph.nodes())
        self.node_to_idx = {n: i for i, n in enumerate(nodes)}
        self.idx_to_node = {i: n for n, i in self.node_to_idx.items()}
        
        print(f"Loaded graph: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges")
        return self.graph
    
    def _extract_node_features(self, node: Dict) -> np.ndarray:
        """提取节点特征"""
        features = []
        
        # Type encoding
        type_encoding = {
            'document': [1, 0, 0, 0, 0, 0],
            'theorem': [0, 1, 0, 0, 0, 0],
            'definition': [0, 0, 1, 0, 0, 0],
            'lemma': [0, 0, 0, 1, 0, 0],
            'proposition': [0, 0, 0, 0, 1, 0],
            'corollary': [0, 0, 0, 0, 0, 1]
        }
        features.extend(type_encoding.get(node.get('type'), [0, 0, 0, 0, 0, 0]))
        
        # Group encoding
        group_encoding = {
            'Struct': [1, 0, 0],
            'Knowledge': [0, 1, 0],
            'Flink': [0, 0, 1]
        }
        features.extend(group_encoding.get(node.get('group'), [0, 0, 0]))
        
        # Size (normalized)
        size = node.get('size', 10)
        features.append(size / 50.0)
        
        # Degree features
        features.append(self.graph.degree(node.get('id', '')) / 10.0)
        
        return np.array(features, dtype=np.float32)
    
    def _create_sample_graph(self) -> nx.DiGraph:
        """创建示例图"""
        nodes = [
            ('Def-S-01-01', {'type': 'definition', 'group': 'Struct', 'size': 15}),
            ('Def-S-01-02', {'type': 'definition', 'group': 'Struct', 'size': 15}),
            ('Thm-S-01-01', {'type': 'theorem', 'group': 'Struct', 'size': 20}),
            ('Def-S-07-01', {'type': 'definition', 'group': 'Struct', 'size': 15}),
            ('Thm-S-07-01', {'type': 'theorem', 'group': 'Struct', 'size': 20}),
            ('Def-K-02-01', {'type': 'definition', 'group': 'Knowledge', 'size': 15}),
            ('Thm-K-04-01', {'type': 'theorem', 'group': 'Knowledge', 'size': 20}),
            ('Def-F-02-01', {'type': 'definition', 'group': 'Flink', 'size': 15}),
            ('Thm-F-02-01', {'type': 'theorem', 'group': 'Flink', 'size': 20}),
        ]
        
        edges = [
            ('Def-S-01-01', 'Thm-S-01-01', {'type': 'dependency'}),
            ('Def-S-01-02', 'Thm-S-01-01', {'type': 'dependency'}),
            ('Thm-S-01-01', 'Def-S-07-01', {'type': 'evolves'}),
            ('Def-S-07-01', 'Thm-S-07-01', {'type': 'dependency'}),
            ('Def-S-01-02', 'Def-K-02-01', {'type': 'instantiates'}),
            ('Def-K-02-01', 'Thm-K-04-01', {'type': 'citation'}),
            ('Thm-S-07-01', 'Def-F-02-01', {'type': 'evolves'}),
            ('Def-F-02-01', 'Thm-F-02-01', {'type': 'dependency'}),
        ]
        
        for node_id, attrs in nodes:
            self.graph.add_node(node_id, **attrs)
            self.node_features[node_id] = self._extract_node_features({'id': node_id, **attrs})
        
        for src, dst, attrs in edges:
            self.graph.add_edge(src, dst, **attrs)
        
        nodes = sorted(self.graph.nodes())
        self.node_to_idx = {n: i for i, n in enumerate(nodes)}
        self.idx_to_node = {i: n for n, i in self.node_to_idx.items()}
        
        return self.graph
    
    def to_pyg_data(self) -> Optional[PyGData]:
        """转换为PyG数据格式"""
        if not TORCH_AVAILABLE or not PYG_AVAILABLE:
            return None
        
        # Node features
        num_nodes = len(self.node_to_idx)
        feature_dim = len(next(iter(self.node_features.values())))
        x = torch.zeros((num_nodes, feature_dim), dtype=torch.float)
        
        for node_id, features in self.node_features.items():
            idx = self.node_to_idx[node_id]
            x[idx] = torch.tensor(features, dtype=torch.float)
        
        # Edge index
        edge_list = []
        for src, dst in self.graph.edges():
            src_idx = self.node_to_idx[src]
            dst_idx = self.node_to_idx[dst]
            edge_list.append([src_idx, dst_idx])
        
        if edge_list:
            edge_index = torch.tensor(edge_list, dtype=torch.long).t().contiguous()
        else:
            edge_index = torch.zeros((2, 0), dtype=torch.long)
        
        return PyGData(x=x, edge_index=edge_index)


# ============================================
# Implicit Relation Miner
# ============================================

class ImplicitRelationMiner:
    """隐式关系挖掘器"""
    
    def __init__(self, graph: nx.DiGraph, loader: KnowledgeGraphLoader):
        self.graph = graph
        self.loader = loader
        self.model = None
        self.node_embeddings = None
        self.discovered_relations: List[ImplicitRelation] = []
    
    def train_gnn(
        self,
        hidden_dim: int = 64,
        out_dim: int = 32,
        epochs: int = 200,
        lr: float = 0.01
    ):
        """训练GNN模型"""
        if not TORCH_AVAILABLE or not PYG_AVAILABLE:
            print("GNN training not available, using structural methods")
            return
        
        print(f"\nTraining GNN model (hidden={hidden_dim}, epochs={epochs})...")
        
        # Prepare data
        data = self.loader.to_pyg_data()
        if data is None:
            return
        
        # Create model
        self.model = GCNLinkPredictor(
            in_channels=data.x.size(1),
            hidden_channels=hidden_dim,
            out_channels=out_dim
        )
        
        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        
        # Generate negative samples
        num_edges = data.edge_index.size(1)
        neg_edges = self._sample_negative_edges(num_edges)
        
        # Training loop
        self.model.train()
        for epoch in tqdm(range(epochs)):
            optimizer.zero_grad()
            
            # Encode nodes
            z = self.model.encode(data.x, data.edge_index)
            
            # Positive samples
            pos_pred = self.model.decode(z, data.edge_index)
            pos_loss = -torch.log(pos_pred + 1e-8).mean()
            
            # Negative samples
            neg_pred = self.model.decode(z, neg_edges)
            neg_loss = -torch.log(1 - neg_pred + 1e-8).mean()
            
            # Total loss
            loss = pos_loss + neg_loss
            
            loss.backward()
            optimizer.step()
            
            if (epoch + 1) % 50 == 0:
                print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")
        
        # Extract embeddings
        self.model.eval()
        with torch.no_grad():
            self.node_embeddings = self.model.encode(data.x, data.edge_index).numpy()
        
        print("GNN training complete")
    
    def _sample_negative_edges(self, num_samples: int) -> torch.Tensor:
        """采样负例边"""
        num_nodes = len(self.loader.node_to_idx)
        existing_edges = set()
        
        for src, dst in self.graph.edges():
            src_idx = self.loader.node_to_idx[src]
            dst_idx = self.loader.node_to_idx[dst]
            existing_edges.add((src_idx, dst_idx))
        
        neg_edges = []
        while len(neg_edges) < num_samples:
            src = np.random.randint(0, num_nodes)
            dst = np.random.randint(0, num_nodes)
            if src != dst and (src, dst) not in existing_edges:
                neg_edges.append([src, dst])
        
        return torch.tensor(neg_edges, dtype=torch.long).t().contiguous()
    
    def discover_by_similarity(self, threshold: float = 0.8) -> List[ImplicitRelation]:
        """基于嵌入相似度发现隐式关系"""
        if self.node_embeddings is None:
            print("No embeddings available, computing structural similarity...")
            return self._discover_by_structural_similarity(threshold)
        
        print(f"\nDiscovering relations by embedding similarity (threshold={threshold})...")
        
        relations = []
        num_nodes = len(self.node_embeddings)
        
        # Compute pairwise similarities
        from sklearn.metrics.pairwise import cosine_similarity
        similarities = cosine_similarity(self.node_embeddings)
        
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                sim = similarities[i, j]
                if sim >= threshold:
                    node_i = self.loader.idx_to_node[i]
                    node_j = self.loader.idx_to_node[j]
                    
                    # Skip if already connected
                    if self.graph.has_edge(node_i, node_j) or self.graph.has_edge(node_j, node_i):
                        continue
                    
                    # Determine relation type based on node types
                    type_i = self.graph.nodes[node_i].get('type', 'unknown')
                    type_j = self.graph.nodes[node_j].get('type', 'unknown')
                    
                    relation_type = self._infer_relation_type(type_i, type_j)
                    
                    relations.append(ImplicitRelation(
                        source_id=node_i,
                        target_id=node_j,
                        relation_type=relation_type,
                        confidence=float(sim),
                        evidence=[f"Embedding similarity: {sim:.3f}"],
                        discovered_by='gnn_similarity'
                    ))
        
        print(f"Discovered {len(relations)} relations by similarity")
        return relations
    
    def _discover_by_structural_similarity(self, threshold: float = 0.8) -> List[ImplicitRelation]:
        """基于结构相似度发现关系 (NetworkX fallback)"""
        print(f"\nDiscovering relations by structural similarity (threshold={threshold})...")
        
        relations = []
        
        # Use Jaccard similarity of neighbors
        for node_i in self.graph.nodes():
            neighbors_i = set(self.graph.neighbors(node_i)) | set(self.graph.predecessors(node_i))
            
            for node_j in self.graph.nodes():
                if node_i >= node_j:
                    continue
                
                neighbors_j = set(self.graph.neighbors(node_j)) | set(self.graph.predecessors(node_j))
                
                # Jaccard similarity
                intersection = len(neighbors_i & neighbors_j)
                union = len(neighbors_i | neighbors_j)
                
                if union == 0:
                    continue
                
                sim = intersection / union
                
                if sim >= threshold:
                    if self.graph.has_edge(node_i, node_j) or self.graph.has_edge(node_j, node_i):
                        continue
                    
                    type_i = self.graph.nodes[node_i].get('type', 'unknown')
                    type_j = self.graph.nodes[node_j].get('type', 'unknown')
                    relation_type = self._infer_relation_type(type_i, type_j)
                    
                    relations.append(ImplicitRelation(
                        source_id=node_i,
                        target_id=node_j,
                        relation_type=relation_type,
                        confidence=float(sim),
                        evidence=[f"Common neighbors: {intersection}"],
                        discovered_by='structural'
                    ))
        
        print(f"Discovered {len(relations)} relations by structural similarity")
        return relations
    
    def _infer_relation_type(self, type_a: str, type_b: str) -> str:
        """根据节点类型推断关系类型"""
        type_pair = tuple(sorted([type_a, type_b]))
        
        inference_rules = {
            ('definition', 'theorem'): 'prerequisite',
            ('definition', 'definition'): 'similar',
            ('theorem', 'theorem'): 'alternative',
            ('lemma', 'theorem'): 'extension',
            ('proposition', 'theorem'): 'extension',
            ('document', 'document'): 'citation',
        }
        
        return inference_rules.get(type_pair, 'similar')
    
    def predict_relation(
        self,
        source: str,
        target: str
    ) -> Optional[RelationPrediction]:
        """预测两个节点之间的关系"""
        if not TORCH_AVAILABLE or self.model is None:
            # Fallback: use simple heuristics
            return self._heuristic_predict(source, target)
        
        data = self.loader.to_pyg_data()
        if data is None:
            return None
        
        src_idx = self.loader.node_to_idx.get(source)
        dst_idx = self.loader.node_to_idx.get(target)
        
        if src_idx is None or dst_idx is None:
            return None
        
        self.model.eval()
        with torch.no_grad():
            z = self.model.encode(data.x, data.edge_index)
            
            edge_index = torch.tensor([[src_idx], [dst_idx]], dtype=torch.long)
            score = self.model.decode(z, edge_index).item()
        
        # Determine relation type
        type_src = self.graph.nodes[source].get('type', 'unknown')
        type_dst = self.graph.nodes[target].get('type', 'unknown')
        relation_type = self._infer_relation_type(type_src, type_dst)
        
        return RelationPrediction(
            source=source,
            target=target,
            relation_type=relation_type,
            confidence=score,
            explanation=f"GNN link prediction score: {score:.3f}"
        )
    
    def _heuristic_predict(self, source: str, target: str) -> Optional[RelationPrediction]:
        """启发式关系预测 (fallback)"""
        if source not in self.graph or target not in self.graph:
            return None
        
        # Check common neighbors
        src_neighbors = set(self.graph.neighbors(source)) | set(self.graph.predecessors(source))
        dst_neighbors = set(self.graph.neighbors(target)) | set(self.graph.predecessors(target))
        common = len(src_neighbors & dst_neighbors)
        
        # Simple scoring
        score = min(common / 5.0, 1.0)
        
        type_src = self.graph.nodes[source].get('type', 'unknown')
        type_dst = self.graph.nodes[target].get('type', 'unknown')
        relation_type = self._infer_relation_type(type_src, type_dst)
        
        return RelationPrediction(
            source=source,
            target=target,
            relation_type=relation_type,
            confidence=score,
            explanation=f"Common neighbors: {common}"
        )
    
    def save_results(self, output_path: Path):
        """保存挖掘结果"""
        output_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_relations': len(self.discovered_relations),
                'methods_used': list(set(r.discovered_by for r in self.discovered_relations))
            },
            'implicit_relations': [
                {
                    'source': r.source_id,
                    'target': r.target_id,
                    'type': r.relation_type,
                    'confidence': r.confidence,
                    'evidence': r.evidence,
                    'discovered_by': r.discovered_by
                }
                for r in self.discovered_relations
            ]
        }
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"\nResults saved to {output_path}")


# ============================================
# Main
# ============================================

def main():
    parser = argparse.ArgumentParser(description='Implicit Relation Miner for Knowledge Graph v2.0')
    parser.add_argument('--graph-path', type=Path, default=PROJECT_ROOT / '.vscode' / 'graph-data.json')
    parser.add_argument('--output', type=Path, default=PROJECT_ROOT / '.scripts' / 'kg-v2' / 'implicit-relations.json')
    parser.add_argument('--train', action='store_true', help='Train GNN model')
    parser.add_argument('--epochs', type=int, default=200, help='Training epochs')
    parser.add_argument('--hidden-dim', type=int, default=64, help='Hidden dimension')
    parser.add_argument('--similarity-threshold', type=float, default=0.8, help='Similarity threshold')
    parser.add_argument('--predict', action='store_true', help='Predict specific relation')
    parser.add_argument('--source', help='Source node for prediction')
    parser.add_argument('--target', help='Target node for prediction')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("AnalysisDataFlow 知识图谱 v2.0 - 隐式关系挖掘器")
    print("=" * 60)
    
    # Load graph
    print("\n[1/4] Loading knowledge graph...")
    loader = KnowledgeGraphLoader(args.graph_path)
    graph = loader.load()
    
    # Initialize miner
    miner = ImplicitRelationMiner(graph, loader)
    
    # Train if requested
    if args.train and TORCH_AVAILABLE and PYG_AVAILABLE:
        print("\n[2/4] Training GNN model...")
        miner.train_gnn(
            hidden_dim=args.hidden_dim,
            epochs=args.epochs
        )
    else:
        print("\n[2/4] Skipping GNN training (using structural methods)")
    
    # Predict specific relation if requested
    if args.predict and args.source and args.target:
        print(f"\n[3/4] Predicting relation between {args.source} and {args.target}...")
        prediction = miner.predict_relation(args.source, args.target)
        if prediction:
            print(f"\nPrediction:")
            print(f"  Type: {prediction.relation_type}")
            print(f"  Confidence: {prediction.confidence:.3f}")
            print(f"  Explanation: {prediction.explanation}")
        else:
            print("  Could not predict relation")
    else:
        # Discover all implicit relations
        print("\n[3/4] Discovering implicit relations...")
        relations = miner.discover_by_similarity(threshold=args.similarity_threshold)
        miner.discovered_relations = relations
    
    # Save results
    print("\n[4/4] Saving results...")
    miner.save_results(args.output)
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Total nodes: {graph.number_of_nodes()}")
    print(f"Total edges: {graph.number_of_edges()}")
    print(f"Discovered implicit relations: {len(miner.discovered_relations)}")
    
    if miner.discovered_relations:
        by_type = defaultdict(int)
        for r in miner.discovered_relations:
            by_type[r.relation_type] += 1
        
        print("\nBy relation type:")
        for rt, count in sorted(by_type.items(), key=lambda x: -x[1]):
            print(f"  {rt}: {count}")
        
        by_method = defaultdict(int)
        for r in miner.discovered_relations:
            by_method[r.discovered_by] += 1
        
        print("\nBy discovery method:")
        for method, count in sorted(by_method.items(), key=lambda x: -x[1]):
            print(f"  {method}: {count}")
    
    print("=" * 60)
    print("✅ Implicit relation mining complete!")


if __name__ == '__main__':
    main()
