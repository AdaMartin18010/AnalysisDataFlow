#!/usr/bin/env python3
"""
AnalysisDataFlow 项目关系查询工具

功能:
- 查询元素的所有依赖
- 查询元素被谁依赖
- 查询两点间路径
- 生成子图
- 导出关系报告

使用方法:
    python relationship-query-tool.py --query-deps Thm-S-04-01
    python relationship-query-tool.py --query-dependents Def-S-01-04
    python relationship-query-tool.py --find-path Def-S-01-04 Thm-S-04-01
    python relationship-query-tool.py --extract-subgraph Thm-S-04-01 --depth 2 --output subgraph.html

作者: Agent
版本: 1.0
日期: 2026-04-06
"""

import json
import argparse
import sys
from pathlib import Path
from collections import deque
from typing import List, Dict, Set, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import heapq


class RelationType(Enum):
    """关系类型枚举"""
    DEPENDENCY = "dependency"           # 依赖关系
    CITATION = "citation"               # 引用关系
    CONTAINS = "contains"               # 包含关系
    INSTANTIATES = "instantiates"       # 实例化关系
    EVOLVES = "evolves"                 # 演进关系
    DERIVES = "derives"                 # 导出关系
    IMPLEMENTS = "implements"           # 实现关系
    EQUIVALENT = "equivalent"           # 等价关系


@dataclass
class Node:
    """节点数据类"""
    id: str
    label: str
    type: str
    group: str
    layer: int = 0
    path: str = ""
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.id == other.id
        return False


@dataclass
class Edge:
    """边数据类"""
    source: str
    target: str
    type: str
    weight: float = 1.0
    label: str = ""
    properties: Dict = None
    
    def __post_init__(self):
        if self.properties is None:
            self.properties = {}
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def __repr__(self):
        return f"Edge({self.source} -> {self.target}, {self.type})"


class RelationshipGraph:
    """关系图类 - 管理项目中的所有关系和节点"""
    
    def __init__(self, data_path: Optional[str] = None):
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.adjacency_list: Dict[str, List[Tuple[str, Edge]]] = {}
        self.reverse_adjacency: Dict[str, List[Tuple[str, Edge]]] = {}
        self._data_path = data_path
        
    def load_from_json(self, json_path: str) -> bool:
        """从JSON文件加载图数据"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 加载节点
            for node_data in data.get('nodes', []):
                node = Node(
                    id=node_data['id'],
                    label=node_data.get('label', node_data['id']),
                    type=node_data.get('type', 'unknown'),
                    group=node_data.get('group', 'unknown'),
                    layer=node_data.get('layer', 0),
                    path=node_data.get('path', ''),
                    metadata=node_data.get('metadata', {})
                )
                self.nodes[node.id] = node
            
            # 加载边
            for edge_data in data.get('edges', []):
                edge = Edge(
                    source=edge_data['source'],
                    target=edge_data['target'],
                    type=edge_data.get('type', 'unknown'),
                    weight=edge_data.get('weight', 1.0),
                    label=edge_data.get('label', ''),
                    properties=edge_data.get('properties', {})
                )
                self.edges.append(edge)
            
            self._build_indices()
            return True
            
        except Exception as e:
            print(f"❌ 加载数据失败: {e}", file=sys.stderr)
            return False
    
    def _build_indices(self):
        """构建邻接表索引"""
        self.adjacency_list = {node_id: [] for node_id in self.nodes}
        self.reverse_adjacency = {node_id: [] for node_id in self.nodes}
        
        for edge in self.edges:
            self.adjacency_list[edge.source].append((edge.target, edge))
            self.reverse_adjacency[edge.target].append((edge.source, edge))
    
    def query_dependencies(self, element_id: str, max_depth: int = -1, 
                          relation_types: Optional[List[str]] = None) -> List[Dict]:
        """
        查询元素依赖的所有元素
        
        Args:
            element_id: 元素ID
            max_depth: 最大深度，-1表示无限制
            relation_types: 限制关系类型，None表示所有类型
            
        Returns:
            依赖元素列表，包含路径信息
        """
        if element_id not in self.nodes:
            return []
        
        results = []
        visited = {element_id}
        queue = deque([(element_id, 0, [])])
        
        while queue:
            current_id, depth, path = queue.popleft()
            
            if max_depth >= 0 and depth > max_depth:
                continue
            
            for target_id, edge in self.adjacency_list.get(current_id, []):
                if relation_types and edge.type not in relation_types:
                    continue
                    
                if target_id not in visited:
                    visited.add(target_id)
                    new_path = path + [{
                        'from': current_id,
                        'to': target_id,
                        'relation': edge.type,
                        'weight': edge.weight
                    }]
                    
                    results.append({
                        'element': self.nodes[target_id].to_dict(),
                        'depth': depth + 1,
                        'path': new_path,
                        'relation_type': edge.type
                    })
                    
                    queue.append((target_id, depth + 1, new_path))
        
        return results
    
    def query_dependents(self, element_id: str, max_depth: int = -1,
                        relation_types: Optional[List[str]] = None) -> List[Dict]:
        """
        查询依赖该元素的所有元素
        
        Args:
            element_id: 元素ID
            max_depth: 最大深度，-1表示无限制
            relation_types: 限制关系类型
            
        Returns:
            依赖该元素的元素列表
        """
        if element_id not in self.nodes:
            return []
        
        results = []
        visited = {element_id}
        queue = deque([(element_id, 0, [])])
        
        while queue:
            current_id, depth, path = queue.popleft()
            
            if max_depth >= 0 and depth > max_depth:
                continue
            
            for source_id, edge in self.reverse_adjacency.get(current_id, []):
                if relation_types and edge.type not in relation_types:
                    continue
                    
                if source_id not in visited:
                    visited.add(source_id)
                    new_path = path + [{
                        'from': source_id,
                        'to': current_id,
                        'relation': edge.type,
                        'weight': edge.weight
                    }]
                    
                    results.append({
                        'element': self.nodes[source_id].to_dict(),
                        'depth': depth + 1,
                        'path': new_path,
                        'relation_type': edge.type
                    })
                    
                    queue.append((source_id, depth + 1, new_path))
        
        return results
    
    def find_path(self, source: str, target: str, 
                  algorithm: str = "dijkstra") -> Optional[Dict]:
        """
        查询从source到target的路径
        
        Args:
            source: 起点ID
            target: 终点ID
            algorithm: 算法类型 ('dijkstra', 'bfs', 'all')
            
        Returns:
            路径信息字典
        """
        if source not in self.nodes or target not in self.nodes:
            return None
        
        if algorithm == "dijkstra":
            return self._dijkstra(source, target)
        elif algorithm == "bfs":
            return self._bfs_path(source, target)
        else:
            return self._dijkstra(source, target)
    
    def _dijkstra(self, source: str, target: str) -> Optional[Dict]:
        """Dijkstra最短路径算法"""
        distances = {node_id: float('inf') for node_id in self.nodes}
        distances[source] = 0
        previous = {node_id: None for node_id in self.nodes}
        
        pq = [(0, source)]
        visited = set()
        
        while pq:
            dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            visited.add(current)
            
            if current == target:
                break
            
            for neighbor_id, edge in self.adjacency_list.get(current, []):
                weight = edge.weight
                new_dist = dist + weight
                
                if new_dist < distances[neighbor_id]:
                    distances[neighbor_id] = new_dist
                    previous[neighbor_id] = current
                    heapq.heappush(pq, (new_dist, neighbor_id))
        
        if previous[target] is None and source != target:
            return None
        
        # 重建路径
        path = []
        current = target
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        
        # 构建边信息
        edges_info = []
        for i in range(len(path) - 1):
            for neighbor_id, edge in self.adjacency_list[path[i]]:
                if neighbor_id == path[i + 1]:
                    edges_info.append({
                        'from': path[i],
                        'to': path[i + 1],
                        'type': edge.type,
                        'weight': edge.weight
                    })
                    break
        
        return {
            'source': source,
            'target': target,
            'path': path,
            'edges': edges_info,
            'total_distance': distances[target],
            'hops': len(path) - 1
        }
    
    def _bfs_path(self, source: str, target: str) -> Optional[Dict]:
        """BFS最短路径（最少边数）"""
        if source == target:
            return {'source': source, 'target': target, 'path': [source], 'edges': [], 'hops': 0}
        
        queue = deque([(source, [source])])
        visited = {source}
        
        while queue:
            current, path = queue.popleft()
            
            for neighbor_id, edge in self.adjacency_list.get(current, []):
                if neighbor_id not in visited:
                    if neighbor_id == target:
                        final_path = path + [target]
                        return {
                            'source': source,
                            'target': target,
                            'path': final_path,
                            'hops': len(final_path) - 1
                        }
                    
                    visited.add(neighbor_id)
                    queue.append((neighbor_id, path + [neighbor_id]))
        
        return None
    
    def find_all_paths(self, source: str, target: str, 
                       max_length: int = 10) -> List[Dict]:
        """
        查找所有可能的路径
        
        Args:
            source: 起点ID
            target: 终点ID
            max_length: 最大路径长度
            
        Returns:
            所有路径列表
        """
        if source not in self.nodes or target not in self.nodes:
            return []
        
        paths = []
        
        def dfs(current: str, target: str, path: List[str], 
                edges: List[Dict], visited: Set[str]):
            if len(path) > max_length:
                return
            
            if current == target:
                paths.append({
                    'path': path.copy(),
                    'edges': edges.copy(),
                    'hops': len(path) - 1
                })
                return
            
            for neighbor_id, edge in self.adjacency_list.get(current, []):
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    path.append(neighbor_id)
                    edges.append({
                        'from': current,
                        'to': neighbor_id,
                        'type': edge.type,
                        'weight': edge.weight
                    })
                    
                    dfs(neighbor_id, target, path, edges, visited)
                    
                    visited.remove(neighbor_id)
                    path.pop()
                    edges.pop()
        
        visited = {source}
        dfs(source, target, [source], [], visited)
        
        return paths
    
    def extract_subgraph(self, center: str, depth: int = 2) -> Dict:
        """
        提取以center为中心，depth为深度的子图
        
        Args:
            center: 中心节点ID
            depth: 深度
            
        Returns:
            子图数据字典
        """
        if center not in self.nodes:
            return {'nodes': [], 'edges': []}
        
        included_nodes = {center}
        included_edges = []
        
        # BFS扩展
        current_level = {center}
        for _ in range(depth):
            next_level = set()
            for node_id in current_level:
                # 出边
                for target_id, edge in self.adjacency_list.get(node_id, []):
                    included_edges.append(edge.to_dict())
                    if target_id not in included_nodes:
                        included_nodes.add(target_id)
                        next_level.add(target_id)
                
                # 入边
                for source_id, edge in self.reverse_adjacency.get(node_id, []):
                    included_edges.append(edge.to_dict())
                    if source_id not in included_nodes:
                        included_nodes.add(source_id)
                        next_level.add(source_id)
            
            current_level = next_level
        
        return {
            'nodes': [self.nodes[nid].to_dict() for nid in included_nodes],
            'edges': included_edges,
            'center': center,
            'depth': depth,
            'node_count': len(included_nodes),
            'edge_count': len(included_edges)
        }
    
    def get_cross_layer_relations(self, layer1: int, layer2: int) -> List[Dict]:
        """
        获取跨层级的对角关系
        
        Args:
            layer1: 第一层
            layer2: 第二层
            
        Returns:
            跨层关系列表
        """
        relations = []
        
        for edge in self.edges:
            source_node = self.nodes.get(edge.source)
            target_node = self.nodes.get(edge.target)
            
            if source_node and target_node:
                if (source_node.layer == layer1 and target_node.layer == layer2) or \
                   (source_node.layer == layer2 and target_node.layer == layer1):
                    relations.append({
                        'source': source_node.to_dict(),
                        'target': target_node.to_dict(),
                        'relation': edge.to_dict()
                    })
        
        return relations
    
    def analyze_impact(self, element_id: str) -> Dict:
        """
        分析元素变更的影响范围
        
        Args:
            element_id: 元素ID
            
        Returns:
            影响分析报告
        """
        if element_id not in self.nodes:
            return {}
        
        # 直接影响（依赖该元素的所有元素）
        direct_impact = self.query_dependents(element_id, max_depth=1)
        
        # 间接影响（第二层依赖）
        indirect_impact = []
        for direct in direct_impact:
            indirect = self.query_dependents(direct['element']['id'], max_depth=1)
            indirect_impact.extend(indirect)
        
        # 按层级分组
        by_layer = {}
        for item in direct_impact + indirect_impact:
            layer = item['element'].get('layer', 0)
            if layer not in by_layer:
                by_layer[layer] = []
            by_layer[layer].append(item['element']['id'])
        
        return {
            'element': element_id,
            'direct_impact_count': len(direct_impact),
            'indirect_impact_count': len(indirect_impact),
            'total_affected': len(set([item['element']['id'] for item in direct_impact + indirect_impact])),
            'by_layer': by_layer,
            'critical_paths': self._find_critical_paths(element_id)
        }
    
    def _find_critical_paths(self, element_id: str) -> List[List[str]]:
        """查找关键路径"""
        critical_paths = []
        
        # 找到所有"定理"元素
        theorems = [nid for nid, node in self.nodes.items() 
                   if node.type == 'theorem']
        
        for theorem in theorems:
            path = self.find_path(element_id, theorem)
            if path and path['hops'] <= 3:
                critical_paths.append(path['path'])
        
        return critical_paths[:5]  # 返回前5条
    
    def export_html(self, subgraph: Dict, output_path: str):
        """导出子图为可交互HTML"""
        html_content = self._generate_html(subgraph)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def _generate_html(self, subgraph: Dict) -> str:
        """生成HTML可视化"""
        nodes_json = json.dumps(subgraph['nodes'])
        edges_json = json.dumps(subgraph['edges'])
        
        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>关系子图 - {subgraph['center']}</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {{ margin: 0; overflow: hidden; font-family: sans-serif; background: #0d1117; color: #c9d1d9; }}
        #graph {{ width: 100vw; height: 100vh; }}
        .node {{ cursor: pointer; }}
        .link {{ stroke-opacity: 0.6; }}
        .node-label {{ font-size: 10px; fill: #c9d1d9; pointer-events: none; }}
    </style>
</head>
<body>
    <svg id="graph"></svg>
    <script>
        const nodes = {nodes_json};
        const edges = {edges_json};
        
        const width = window.innerWidth;
        const height = window.innerHeight;
        const svg = d3.select('#graph').attr('width', width).attr('height', height);
        const g = svg.append('g');
        
        const zoom = d3.zoom().on('zoom', (e) => g.attr('transform', e.transform));
        svg.call(zoom);
        
        const simulation = d3.forceSimulation(nodes)
            .force('link', d3.forceLink(edges).id(d => d.id).distance(100))
            .force('charge', d3.forceManyBody().strength(-300))
            .force('center', d3.forceCenter(width / 2, height / 2));
        
        const link = g.selectAll('line')
            .data(edges)
            .enter().append('line')
            .attr('class', 'link')
            .attr('stroke', '#58a6ff')
            .attr('stroke-width', 1.5);
        
        const node = g.selectAll('g')
            .data(nodes)
            .enter().append('g')
            .attr('class', 'node')
            .call(d3.drag());
        
        node.append('circle')
            .attr('r', d => d.type === 'document' ? 15 : 8)
            .attr('fill', d => d.group === 'Struct' ? '#4A90D9' : d.group === 'Knowledge' ? '#5CB85C' : '#F0AD4E');
        
        node.append('text')
            .attr('class', 'node-label')
            .attr('dy', 25)
            .attr('text-anchor', 'middle')
            .text(d => d.label || d.id);
        
        simulation.on('tick', () => {{
            link.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
            node.attr('transform', d => `translate(${{d.x}},${{d.y}})`);
        }});
    </script>
</body>
</html>'''
        return html


def print_results(results: Any, format_type: str = 'table'):
    """打印结果"""
    if format_type == 'json':
        print(json.dumps(results, indent=2, ensure_ascii=False))
    elif format_type == 'table':
        if isinstance(results, list):
            for i, item in enumerate(results[:20], 1):  # 最多显示20条
                if isinstance(item, dict) and 'element' in item:
                    elem = item['element']
                    print(f"{i}. [{elem.get('group', 'N/A')}] {elem.get('label', elem['id'])} "
                          f"(深度: {item.get('depth', 'N/A')}, 关系: {item.get('relation_type', 'N/A')})")
                else:
                    print(f"{i}. {item}")
            if len(results) > 20:
                print(f"\n... 还有 {len(results) - 20} 条结果")
        elif isinstance(results, dict):
            for key, value in results.items():
                print(f"{key}: {value}")
        else:
            print(results)


def main():
    parser = argparse.ArgumentParser(
        description='AnalysisDataFlow 项目关系查询工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python relationship-query-tool.py --query-deps Thm-S-04-01
  python relationship-query-tool.py --query-dependents Def-S-01-04 --depth 2
  python relationship-query-tool.py --find-path Def-S-01-04 Thm-S-04-01
  python relationship-query-tool.py --extract-subgraph Thm-S-04-01 --depth 2 --output subgraph.html
  python relationship-query-tool.py --impact-analysis Thm-S-04-01
        '''
    )
    
    parser.add_argument('--data', '-d', default='.vscode/graph-data.json',
                       help='图数据JSON文件路径 (默认: .vscode/graph-data.json)')
    parser.add_argument('--format', '-f', choices=['table', 'json'], default='table',
                       help='输出格式 (默认: table)')
    
    # 查询命令
    subparsers = parser.add_subparsers(dest='command', help='查询命令')
    
    # 查询依赖
    deps_parser = subparsers.add_parser('query-deps', help='查询元素的依赖')
    deps_parser.add_argument('element_id', help='元素ID')
    deps_parser.add_argument('--depth', '-D', type=int, default=-1,
                            help='最大深度，-1表示无限制 (默认: -1)')
    deps_parser.add_argument('--type', '-t', nargs='+',
                            help='限制关系类型')
    
    # 查询被依赖
    dependents_parser = subparsers.add_parser('query-dependents', 
                                             help='查询依赖该元素的元素')
    dependents_parser.add_argument('element_id', help='元素ID')
    dependents_parser.add_argument('--depth', '-D', type=int, default=-1,
                                  help='最大深度 (默认: -1)')
    dependents_parser.add_argument('--type', '-t', nargs='+',
                                  help='限制关系类型')
    
    # 查找路径
    path_parser = subparsers.add_parser('find-path', help='查找两点间路径')
    path_parser.add_argument('source', help='起点ID')
    path_parser.add_argument('target', help='终点ID')
    path_parser.add_argument('--algorithm', '-a', 
                            choices=['dijkstra', 'bfs', 'all'],
                            default='dijkstra',
                            help='路径算法 (默认: dijkstra)')
    
    # 提取子图
    subgraph_parser = subparsers.add_parser('extract-subgraph', 
                                           help='提取子图')
    subgraph_parser.add_argument('center', help='中心节点ID')
    subgraph_parser.add_argument('--depth', '-D', type=int, default=2,
                                help='深度 (默认: 2)')
    subgraph_parser.add_argument('--output', '-o', required=True,
                                help='输出HTML文件路径')
    
    # 影响分析
    impact_parser = subparsers.add_parser('impact-analysis',
                                         help='分析元素变更影响范围')
    impact_parser.add_argument('element_id', help='元素ID')
    
    # 跨层关系
    cross_parser = subparsers.add_parser('cross-layer',
                                        help='查询跨层级关系')
    cross_parser.add_argument('layer1', type=int, help='第一层')
    cross_parser.add_argument('layer2', type=int, help='第二层')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 初始化图
    graph = RelationshipGraph()
    
    # 尝试加载数据
    data_paths = [
        args.data,
        '../.vscode/graph-data.json',
        '.vscode/graph-data.json',
        'graph-data.json'
    ]
    
    loaded = False
    for path in data_paths:
        if Path(path).exists():
            if graph.load_from_json(path):
                print(f"✅ 已加载数据: {path}")
                loaded = True
                break
    
    if not loaded:
        print("⚠️ 警告: 未找到数据文件，使用示例数据进行演示")
        # 创建示例数据
        graph.nodes['Thm-S-04-01'] = Node('Thm-S-04-01', 'Checkpoint Correctness', 'theorem', 'Struct', 1)
        graph.nodes['Def-S-01-04'] = Node('Def-S-01-04', 'Dataflow Model', 'definition', 'Struct', 1)
        graph.nodes['pattern-checkpoint'] = Node('pattern-checkpoint', 'Checkpoint Pattern', 'pattern', 'Knowledge', 2)
        graph.nodes['flink-checkpoint'] = Node('flink-checkpoint', 'Flink Checkpoint', 'document', 'Flink', 3)
        graph._build_indices()
    
    # 执行命令
    if args.command == 'query-deps':
        results = graph.query_dependencies(args.element_id, args.depth, args.type)
        print(f"\n📦 元素 '{args.element_id}' 的依赖关系:\n")
        print_results(results, args.format)
        print(f"\n总计: {len(results)} 个依赖")
    
    elif args.command == 'query-dependents':
        results = graph.query_dependents(args.element_id, args.depth, args.type)
        print(f"\n🔗 依赖 '{args.element_id}' 的元素:\n")
        print_results(results, args.format)
        print(f"\n总计: {len(results)} 个依赖者")
    
    elif args.command == 'find-path':
        result = graph.find_path(args.source, args.target, args.algorithm)
        if result:
            print(f"\n🔍 从 '{args.source}' 到 '{args.target}' 的路径:\n")
            if args.format == 'json':
                print_results(result, 'json')
            else:
                print(f"路径: {' -> '.join(result['path'])}")
                print(f"跳数: {result['hops']}")
                if 'total_distance' in result:
                    print(f"总权重: {result['total_distance']}")
                if 'edges' in result:
                    print("\n边详情:")
                    for edge in result['edges']:
                        print(f"  {edge['from']} --[{edge['type']}]--> {edge['to']}")
        else:
            print(f"❌ 未找到从 '{args.source}' 到 '{args.target}' 的路径")
    
    elif args.command == 'extract-subgraph':
        subgraph = graph.extract_subgraph(args.center, args.depth)
        output_path = graph.export_html(subgraph, args.output)
        print(f"✅ 子图已导出: {output_path}")
        print(f"   节点数: {subgraph['node_count']}")
        print(f"   边数: {subgraph['edge_count']}")
    
    elif args.command == 'impact-analysis':
        result = graph.analyze_impact(args.element_id)
        print(f"\n💥 元素 '{args.element_id}' 变更影响分析:\n")
        print_results(result, args.format)
    
    elif args.command == 'cross-layer':
        results = graph.get_cross_layer_relations(args.layer1, args.layer2)
        print(f"\n🌉 层级 {args.layer1} 和 {args.layer2} 之间的跨层关系:\n")
        print_results(results, args.format)
        print(f"\n总计: {len(results)} 条跨层关系")


if __name__ == '__main__':
    main()
