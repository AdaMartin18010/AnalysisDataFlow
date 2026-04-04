#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AnalysisDataFlow 文档关系自动映射器 (P2-11)
Document Relationship Mapper

功能：
1. 自动扫描所有 Markdown 文档
2. 提取文档间的引用关系（内部链接、前置依赖）
3. 生成关系图谱数据（JSON、GraphML、DOT格式）
4. 检测孤立文档和循环依赖
5. 输出关系报告

作者: AnalysisDataFlow Agent
版本: 2.0.0
日期: 2026-04-04
"""

import os
import re
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
from datetime import datetime
import xml.etree.ElementTree as ET


# =============================================================================
# 数据模型
# =============================================================================

@dataclass
class DocumentNode:
    """文档节点"""
    id: str
    title: str
    path: str
    category: str  # Struct, Knowledge, Flink
    subcategory: str = ""
    word_count: int = 0
    formality_level: str = ""
    description: str = ""
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class DocumentEdge:
    """文档关系边"""
    source: str
    target: str
    type: str  # references, depends_on, cites, extends
    context: str = ""  # 引用上下文
    line_number: int = 0
    strength: float = 1.0
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class RelationshipReport:
    """关系分析报告"""
    total_documents: int = 0
    total_relationships: int = 0
    isolated_documents: List[str] = field(default_factory=list)
    circular_dependencies: List[List[str]] = field(default_factory=list)
    category_connections: Dict[str, Dict] = field(default_factory=dict)
    most_referenced: List[Tuple[str, int]] = field(default_factory=list)
    most_referencing: List[Tuple[str, int]] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            'total_documents': self.total_documents,
            'total_relationships': self.total_relationships,
            'isolated_documents': self.isolated_documents,
            'circular_dependencies': self.circular_dependencies,
            'category_connections': self.category_connections,
            'most_referenced': self.most_referenced,
            'most_referencing': self.most_referencing
        }


# =============================================================================
# 文档解析器
# =============================================================================

class DocumentParser:
    """Markdown文档解析器"""
    
    # 正则表达式模式
    HEADER_PATTERN = re.compile(r'^#\s+(.+)$', re.MULTILINE)
    LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+\.md)\)')
    DEPENDENCY_PATTERN = re.compile(r'前置依赖:\s*\[([^\]]+)\]\(([^)]+)\)')
    META_PATTERN = re.compile(r'^>\s*\*\*([^:]+)\*\*:\s*(.+)$', re.MULTILINE)
    SECTION_PATTERN = re.compile(r'^##+\s+(.+)$', re.MULTILINE)
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.nodes: Dict[str, DocumentNode] = {}
        self.edges: List[DocumentEdge] = []
        
    def parse_document(self, file_path: Path) -> Optional[DocumentNode]:
        """解析单个Markdown文档"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            print(f"  警告: 无法读取文件 {file_path}: {e}")
            return None
        
        rel_path = file_path.relative_to(self.base_path)
        node_id = self._generate_node_id(rel_path)
        
        # 提取标题
        title_match = self.HEADER_PATTERN.search(content)
        title = title_match.group(1) if title_match else file_path.stem
        title = re.sub(r'\([^)]+\)$', '', title).strip()
        
        # 确定类别
        category, subcategory = self._determine_categories(rel_path)
        
        # 提取元数据
        metadata = self._extract_metadata(content)
        formality_level = metadata.get('形式化等级', '')
        
        # 提取描述
        description = self._extract_description(content)
        
        # 统计字数
        word_count = len(content.split())
        
        # 提取标签
        tags = self._extract_tags(content, category, subcategory)
        
        node = DocumentNode(
            id=node_id,
            title=title,
            path=str(rel_path).replace('\\', '/'),
            category=category,
            subcategory=subcategory,
            word_count=word_count,
            formality_level=formality_level,
            description=description,
            tags=tags
        )
        
        return node
    
    def _generate_node_id(self, rel_path: Path) -> str:
        """生成节点ID"""
        return str(rel_path).replace('\\', '/').replace('/', '_').replace('.md', '')
    
    def _determine_categories(self, rel_path: Path) -> Tuple[str, str]:
        """确定文档类别和子类别"""
        path_str = str(rel_path).lower()
        parts = path_str.split('/')
        
        category = 'Root'
        subcategory = ''
        
        if len(parts) > 0:
            if parts[0] == 'struct':
                category = 'Struct'
            elif parts[0] == 'knowledge':
                category = 'Knowledge'
            elif parts[0] == 'flink':
                category = 'Flink'
        
        if len(parts) > 1:
            subcategory = parts[1]
        
        return category, subcategory
    
    def _extract_metadata(self, content: str) -> Dict[str, str]:
        """提取文档元数据"""
        metadata = {}
        
        # 查找元数据块
        meta_block = re.search(r'^>\s*所属阶段:[^\n]+(\n>\s*[^\n]+)*', content, re.MULTILINE)
        if meta_block:
            block_content = meta_block.group(0)
            for match in re.finditer(r'>\s*\*\*([^:]+)\*\*:\s*([^|\n]+)', block_content):
                key = match.group(1).strip()
                value = match.group(2).strip()
                metadata[key] = value
        
        # 提取前置依赖
        dep_match = self.DEPENDENCY_PATTERN.search(content)
        if dep_match:
            metadata['前置依赖'] = dep_match.group(2)
        
        return metadata
    
    def _extract_description(self, content: str) -> str:
        """提取文档描述"""
        lines = content.split('\n')
        description = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#') or line.startswith('>') or line.startswith('|'):
                continue
            if line.startswith('```') or line.startswith('---'):
                continue
            if line.startswith('[') and line.endswith(')'):
                continue
            
            clean_line = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
            clean_line = re.sub(r'\*([^*]+)\*', r'\1', clean_line)
            clean_line = re.sub(r'`([^`]+)`', r'\1', clean_line)
            
            if clean_line:
                description.append(clean_line)
                if len(description) >= 2:
                    break
        
        return ' '.join(description)[:200]
    
    def _extract_tags(self, content: str, category: str, subcategory: str) -> List[str]:
        """提取文档标签"""
        tags = [category]
        
        content_lower = content.lower()
        
        # 关键词标签
        keywords = {
            'checkpoint': 'Checkpoint',
            'watermark': 'Watermark',
            'exactly-once': 'Exactly-Once',
            'state': 'State',
            'pattern': 'Pattern',
            'theorem': 'Theorem',
            'proof': 'Proof',
            'flink': 'Flink',
            'kafka': 'Kafka',
            'sql': 'SQL',
            'performance': 'Performance'
        }
        
        for keyword, tag in keywords.items():
            if keyword in content_lower:
                tags.append(tag)
        
        if subcategory:
            tags.append(subcategory)
        
        return list(set(tags))
    
    def extract_relationships(self, file_path: Path, node_id: str) -> List[DocumentEdge]:
        """提取文档关系"""
        edges = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            return edges
        
        # 提取内部链接
        for line_num, line in enumerate(lines, 1):
            for match in self.LINK_PATTERN.finditer(line):
                link_text = match.group(1)
                link_path = match.group(2)
                
                target_id = self._resolve_link_path(link_path, file_path.parent)
                if target_id and target_id != node_id:
                    edge = DocumentEdge(
                        source=node_id,
                        target=target_id,
                        type='references',
                        context=link_text,
                        line_number=line_num
                    )
                    edges.append(edge)
        
        # 提取前置依赖
        dep_match = self.DEPENDENCY_PATTERN.search(content)
        if dep_match:
            dep_path = dep_match.group(2)
            target_id = self._resolve_link_path(dep_path, file_path.parent)
            if target_id and target_id != node_id:
                edge = DocumentEdge(
                    source=node_id,
                    target=target_id,
                    type='depends_on',
                    context='前置依赖',
                    strength=2.0
                )
                edges.append(edge)
        
        return edges
    
    def _resolve_link_path(self, link_path: str, base_dir: Path) -> Optional[str]:
        """解析链接路径为节点ID"""
        # 清理路径
        clean_path = link_path.replace('../', '').replace('./', '')
        clean_path = clean_path.replace('\\', '/')
        
        # 尝试匹配现有节点
        for node_id, node in self.nodes.items():
            if node.path.endswith(clean_path) or clean_path in node.path:
                return node_id
        
        # 从路径生成ID
        if clean_path.endswith('.md'):
            return clean_path.replace('/', '_').replace('.md', '')
        
        return None
    
    def scan_directory(self, directory: str) -> Tuple[List[DocumentNode], List[DocumentEdge]]:
        """扫描目录中的所有文档"""
        print(f"扫描目录: {directory}")
        
        dir_path = self.base_path / directory
        if not dir_path.exists():
            print(f"  警告: 目录不存在 {dir_path}")
            return [], []
        
        # 第一阶段：收集所有节点
        for md_file in dir_path.rglob('*.md'):
            node = self.parse_document(md_file)
            if node:
                self.nodes[node.id] = node
                print(f"  发现文档: {node.path}")
        
        # 第二阶段：提取关系
        for md_file in dir_path.rglob('*.md'):
            node_id = self._generate_node_id(md_file.relative_to(self.base_path))
            edges = self.extract_relationships(md_file, node_id)
            self.edges.extend(edges)
        
        print(f"  总计: {len(self.nodes)} 个文档, {len(self.edges)} 个关系")
        
        return list(self.nodes.values()), self.edges


# =============================================================================
# 关系分析器
# =============================================================================

class RelationshipAnalyzer:
    """关系分析器"""
    
    def __init__(self, nodes: List[DocumentNode], edges: List[DocumentEdge]):
        self.nodes = {n.id: n for n in nodes}
        self.edges = edges
        self.adjacency = self._build_adjacency()
    
    def _build_adjacency(self) -> Dict[str, List[str]]:
        """构建邻接表"""
        adj = defaultdict(list)
        for edge in self.edges:
            adj[edge.source].append(edge.target)
        return adj
    
    def find_isolated_documents(self) -> List[str]:
        """查找孤立文档（无入边也无出边）"""
        has_incoming = set()
        has_outgoing = set()
        
        for edge in self.edges:
            has_outgoing.add(edge.source)
            has_incoming.add(edge.target)
        
        isolated = []
        for node_id in self.nodes:
            if node_id not in has_incoming and node_id not in has_outgoing:
                isolated.append(node_id)
        
        return isolated
    
    def find_circular_dependencies(self) -> List[List[str]]:
        """查找循环依赖"""
        cycles = []
        visited = set()
        rec_stack = set()
        path = []
        
        def dfs(node_id):
            visited.add(node_id)
            rec_stack.add(node_id)
            path.append(node_id)
            
            for neighbor in self.adjacency[node_id]:
                if neighbor not in visited:
                    result = dfs(neighbor)
                    if result:
                        return result
                elif neighbor in rec_stack:
                    # 发现循环
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    cycles.append(cycle)
            
            path.pop()
            rec_stack.remove(node_id)
            return None
        
        for node_id in self.nodes:
            if node_id not in visited:
                dfs(node_id)
        
        return cycles
    
    def analyze_category_connections(self) -> Dict[str, Dict]:
        """分析类别间连接"""
        connections = defaultdict(lambda: {'incoming': 0, 'outgoing': 0, 'connections': set()})
        
        for edge in self.edges:
            source_node = self.nodes.get(edge.source)
            target_node = self.nodes.get(edge.target)
            
            if source_node and target_node:
                source_cat = source_node.category
                target_cat = target_node.category
                
                connections[source_cat]['outgoing'] += 1
                connections[target_cat]['incoming'] += 1
                connections[source_cat]['connections'].add(target_cat)
        
        # 转换集合为列表
        result = {}
        for cat, data in connections.items():
            result[cat] = {
                'incoming': data['incoming'],
                'outgoing': data['outgoing'],
                'connected_categories': list(data['connections'])
            }
        
        return result
    
    def get_most_referenced(self, limit: int = 10) -> List[Tuple[str, int]]:
        """获取被引用最多的文档"""
        reference_count = defaultdict(int)
        
        for edge in self.edges:
            reference_count[edge.target] += 1
        
        sorted_refs = sorted(reference_count.items(), key=lambda x: x[1], reverse=True)
        return sorted_refs[:limit]
    
    def get_most_referencing(self, limit: int = 10) -> List[Tuple[str, int]]:
        """获取引用最多的文档"""
        reference_count = defaultdict(int)
        
        for edge in self.edges:
            reference_count[edge.source] += 1
        
        sorted_refs = sorted(reference_count.items(), key=lambda x: x[1], reverse=True)
        return sorted_refs[:limit]
    
    def generate_report(self) -> RelationshipReport:
        """生成完整分析报告"""
        print("\n分析文档关系...")
        
        isolated = self.find_isolated_documents()
        print(f"  孤立文档: {len(isolated)} 个")
        
        cycles = self.find_circular_dependencies()
        print(f"  循环依赖: {len(cycles)} 个")
        
        category_connections = self.analyze_category_connections()
        
        most_referenced = self.get_most_referenced()
        most_referencing = self.get_most_referencing()
        
        return RelationshipReport(
            total_documents=len(self.nodes),
            total_relationships=len(self.edges),
            isolated_documents=isolated,
            circular_dependencies=cycles,
            category_connections=category_connections,
            most_referenced=most_referenced,
            most_referencing=most_referencing
        )


# =============================================================================
# 导出器
# =============================================================================

class GraphExporter:
    """图谱数据导出器"""
    
    def __init__(self, nodes: List[DocumentNode], edges: List[DocumentEdge], output_dir: Path):
        self.nodes = nodes
        self.edges = edges
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_json(self) -> str:
        """导出为JSON格式"""
        data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'version': '2.0.0',
                'total_nodes': len(self.nodes),
                'total_edges': len(self.edges)
            },
            'nodes': [node.to_dict() for node in self.nodes],
            'edges': [edge.to_dict() for edge in self.edges]
        }
        
        output_path = self.output_dir / 'doc-relationships.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"  导出: {output_path}")
        return str(output_path)
    
    def export_graphml(self) -> str:
        """导出为GraphML格式"""
        # 创建根元素
        root = ET.Element('graphml')
        root.set('xmlns', 'http://graphml.graphdrawing.org/xmlns')
        
        # 定义属性
        key_id = ET.SubElement(root, 'key')
        key_id.set('id', 'label')
        key_id.set('for', 'node')
        key_id.set('attr.name', 'label')
        key_id.set('attr.type', 'string')
        
        key_cat = ET.SubElement(root, 'key')
        key_cat.set('id', 'category')
        key_cat.set('for', 'node')
        key_cat.set('attr.name', 'category')
        key_cat.set('attr.type', 'string')
        
        key_type = ET.SubElement(root, 'key')
        key_type.set('id', 'edge_type')
        key_type.set('for', 'edge')
        key_type.set('attr.name', 'type')
        key_type.set('attr.type', 'string')
        
        # 创建图
        graph = ET.SubElement(root, 'graph')
        graph.set('id', 'G')
        graph.set('edgedefault', 'directed')
        
        # 添加节点
        for node in self.nodes:
            node_elem = ET.SubElement(graph, 'node')
            node_elem.set('id', node.id)
            
            data_label = ET.SubElement(node_elem, 'data')
            data_label.set('key', 'label')
            data_label.text = node.title
            
            data_cat = ET.SubElement(node_elem, 'data')
            data_cat.set('key', 'category')
            data_cat.text = node.category
        
        # 添加边
        for i, edge in enumerate(self.edges):
            edge_elem = ET.SubElement(graph, 'edge')
            edge_elem.set('id', f'e{i}')
            edge_elem.set('source', edge.source)
            edge_elem.set('target', edge.target)
            
            data_type = ET.SubElement(edge_elem, 'data')
            data_type.set('key', 'edge_type')
            data_type.text = edge.type
        
        # 写入文件
        output_path = self.output_dir / 'doc-relationships.graphml'
        tree = ET.ElementTree(root)
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
        
        print(f"  导出: {output_path}")
        return str(output_path)
    
    def export_dot(self) -> str:
        """导出为Graphviz DOT格式"""
        lines = ['digraph DocumentRelationships {']
        lines.append('  rankdir=TB;')
        lines.append('  node [shape=box, style="rounded,filled", fontname="Microsoft YaHei"];')
        lines.append('  edge [fontname="Microsoft YaHei", fontsize=10];')
        lines.append('')
        
        # 颜色映射
        color_map = {
            'Struct': '#e3f2fd',
            'Knowledge': '#e8f5e9',
            'Flink': '#fff3e0',
            'Root': '#f3e5f5'
        }
        
        # 按类别分组
        categories = defaultdict(list)
        for node in self.nodes:
            categories[node.category].append(node)
        
        # 添加子图
        for category, nodes in categories.items():
            lines.append(f'  subgraph cluster_{category} {{')
            lines.append(f'    label="{category}";')
            lines.append(f'    style=filled;')
            lines.append(f'    color={color_map.get(category, "#eeeeee")};')
            
            for node in nodes:
                label = node.title.replace('"', '\\"')
                lines.append(f'    "{node.id}" [label="{label}", fillcolor={color_map.get(category, "#ffffff")}];')
            
            lines.append('  }')
            lines.append('')
        
        # 添加边
        edge_colors = {
            'references': '#666666',
            'depends_on': '#f0ad4e',
            'cites': '#5cb85c'
        }
        
        for edge in self.edges:
            color = edge_colors.get(edge.type, '#666666')
            style = 'dashed' if edge.type == 'depends_on' else 'solid'
            lines.append(f'  "{edge.source}" -> "{edge.target}" [color="{color}", style={style}];')
        
        lines.append('}')
        
        output_path = self.output_dir / 'doc-relationships.dot'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"  导出: {output_path}")
        return str(output_path)
    
    def export_cytoscape(self) -> str:
        """导出为Cytoscape JSON格式"""
        elements = []
        
        color_map = {
            'Struct': '#4A90D9',
            'Knowledge': '#5CB85C',
            'Flink': '#F0AD4E',
            'Root': '#9B59B6'
        }
        
        for node in self.nodes:
            elements.append({
                'data': {
                    'id': node.id,
                    'label': node.title,
                    'category': node.category,
                    'path': node.path,
                    'color': color_map.get(node.category, '#999999')
                }
            })
        
        for edge in self.edges:
            elements.append({
                'data': {
                    'source': edge.source,
                    'target': edge.target,
                    'type': edge.type
                }
            })
        
        output_path = self.output_dir / 'doc-relationships-cytoscape.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(elements, f, ensure_ascii=False, indent=2)
        
        print(f"  导出: {output_path}")
        return str(output_path)
    
    def export_report(self, report: RelationshipReport) -> str:
        """导出分析报告为Markdown"""
        lines = ['# 文档关系分析报告\n']
        lines.append(f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        lines.append('## 统计概览\n')
        lines.append(f"- **总文档数**: {report.total_documents}")
        lines.append(f"- **总关系数**: {report.total_relationships}")
        lines.append(f"- **孤立文档**: {len(report.isolated_documents)} 个")
        lines.append(f"- **循环依赖**: {len(report.circular_dependencies)} 个\n")
        
        lines.append('## 类别连接分析\n')
        for cat, data in report.category_connections.items():
            lines.append(f"### {cat}")
            lines.append(f"- 入度: {data['incoming']}")
            lines.append(f"- 出度: {data['outgoing']}")
            lines.append(f"- 连接类别: {', '.join(data['connected_categories'])}\n")
        
        lines.append('## 被引用最多的文档 (Top 10)\n')
        for doc_id, count in report.most_referenced:
            node = self.nodes.get(doc_id)
            if node:
                lines.append(f"- **{node.title}** ({count} 次引用) - `{node.path}`")
        
        lines.append('\n## 引用最多的文档 (Top 10)\n')
        for doc_id, count in report.most_referencing:
            node = self.nodes.get(doc_id)
            if node:
                lines.append(f"- **{node.title}** (引用 {count} 个文档) - `{node.path}`")
        
        if report.isolated_documents:
            lines.append('\n## 孤立文档\n')
            lines.append("以下文档没有任何引用关系:\n")
            for doc_id in report.isolated_documents:
                node = self.nodes.get(doc_id)
                if node:
                    lines.append(f"- `{node.path}` - {node.title}")
        
        if report.circular_dependencies:
            lines.append('\n## 循环依赖\n')
            for i, cycle in enumerate(report.circular_dependencies, 1):
                lines.append(f"### 循环 {i}")
                for doc_id in cycle:
                    node = self.nodes.get(doc_id)
                    if node:
                        lines.append(f"- {node.title}")
                lines.append('')
        
        output_path = self.output_dir / 'doc-relationship-report.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"  导出: {output_path}")
        return str(output_path)


# =============================================================================
# 主程序
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='文档关系自动映射器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 扫描所有目录
  python doc-relationship-mapper.py
  
  # 扫描指定目录
  python doc-relationship-mapper.py --dirs Struct Knowledge
  
  # 指定输出目录
  python doc-relationship-mapper.py --output my-output
  
  # 仅生成报告
  python doc-relationship-mapper.py --report-only
        """
    )
    
    parser.add_argument('--base-path', default='.', help='项目根目录')
    parser.add_argument('--dirs', nargs='+', 
                       default=['Struct', 'Knowledge', 'Flink'],
                       help='要扫描的目录')
    parser.add_argument('--output', default='KNOWLEDGE-GRAPH/data',
                       help='输出目录')
    parser.add_argument('--formats', nargs='+',
                       default=['json', 'graphml', 'dot', 'cytoscape'],
                       help='导出格式')
    parser.add_argument('--report-only', action='store_true',
                       help='仅生成报告')
    
    args = parser.parse_args()
    
    base_path = Path(args.base_path).resolve()
    output_dir = base_path / args.output
    
    print("=" * 60)
    print("文档关系自动映射器 v2.0.0")
    print("=" * 60)
    print(f"项目路径: {base_path}")
    print(f"输出目录: {output_dir}")
    print(f"扫描目录: {', '.join(args.dirs)}")
    print()
    
    # 创建解析器
    parser_obj = DocumentParser(base_path)
    
    all_nodes = []
    all_edges = []
    
    # 扫描各目录
    for directory in args.dirs:
        dir_path = base_path / directory
        if dir_path.exists():
            nodes, edges = parser_obj.scan_directory(directory)
            all_nodes.extend(nodes)
            all_edges.extend(edges)
        else:
            print(f"警告: 目录 {directory} 不存在，跳过")
    
    print(f"\n总计发现: {len(all_nodes)} 个文档, {len(all_edges)} 个关系")
    
    if not args.report_only:
        # 导出图谱数据
        print("\n导出图谱数据...")
        exporter = GraphExporter(all_nodes, all_edges, output_dir)
        
        if 'json' in args.formats:
            exporter.export_json()
        if 'graphml' in args.formats:
            exporter.export_graphml()
        if 'dot' in args.formats:
            exporter.export_dot()
        if 'cytoscape' in args.formats:
            exporter.export_cytoscape()
    
    # 生成分析报告
    print("\n生成分析报告...")
    analyzer = RelationshipAnalyzer(all_nodes, all_edges)
    report = analyzer.generate_report()
    
    exporter = GraphExporter(all_nodes, all_edges, output_dir)
    exporter.export_report(report)
    
    print("\n" + "=" * 60)
    print("完成!")
    print("=" * 60)
    print(f"\n输出文件:")
    if not args.report_only:
        print(f"  📊 doc-relationships.json - JSON格式")
        print(f"  📊 doc-relationships.graphml - GraphML格式")
        print(f"  📊 doc-relationships.dot - Graphviz DOT格式")
        print(f"  📊 doc-relationships-cytoscape.json - Cytoscape格式")
    print(f"  📝 doc-relationship-report.md - 分析报告")
    print()


if __name__ == '__main__':
    main()
