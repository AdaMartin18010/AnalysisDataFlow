#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AnalysisDataFlow 知识图谱生成器
P2-10 任务：创建交互式知识图谱可视化

功能：
1. 扫描所有Markdown文件，提取节点和边
2. 生成Graphviz DOT格式
3. 生成Cytoscape JSON格式
4. 生成HTML交互式页面（D3.js + Cytoscape.js）
5. 支持层级图谱和学习路径图谱
6. 输出到visuals/目录

作者: Agent
版本: 1.0.0
日期: 2026-04-04
"""

import os
import re
import json
import hashlib
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
import argparse


# =============================================================================
# 数据模型
# =============================================================================

@dataclass
class Node:
    """图谱节点"""
    id: str
    label: str
    type: str  # document, concept, theorem, definition, lemma, proposition, corollary
    category: str  # Struct, Knowledge, Flink, Root
    level: str = ""  # L1-L6 形式化等级
    path: str = ""
    description: str = ""
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Edge:
    """图谱边"""
    source: str
    target: str
    type: str  # references, depends_on, relates_to, proves, defines, extends
    label: str = ""
    weight: float = 1.0
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class FormalElement:
    """形式化元素（定理、定义、引理等）"""
    id: str
    type: str  # theorem, definition, lemma, proposition, corollary
    name: str
    document: str
    document_path: str
    description: str = ""


# =============================================================================
# 文档解析器
# =============================================================================

class DocumentParser:
    """Markdown文档解析器"""
    
    # 正则表达式模式
    HEADER_PATTERN = re.compile(r'^#\s+(.+)$', re.MULTILINE)
    META_PATTERN = re.compile(r'^>\s*\*\*([^:]+)\*\*:\s*(.+)$', re.MULTILINE)
    DEPENDENCY_PATTERN = re.compile(r'前置依赖:\s*\[([^\]]+)\]\(([^)]+)\)')
    
    # 形式化元素模式 (Thm-S-01-01, Def-K-02-01, etc.)
    THEOREM_PATTERN = re.compile(r'\*\*定理\s+([\d.]+)\s*\(([^)]+)\)\s*\*\*', re.IGNORECASE)
    DEF_PATTERN = re.compile(r'\*\*定义\s+([\d.]+)\s*\(([^)]+)\)\s*\*\*', re.IGNORECASE)
    LEMMA_PATTERN = re.compile(r'\*\*引理\s+([\d.]+)\s*\(([^)]+)\)\s*\*\*', re.IGNORECASE)
    PROP_PATTERN = re.compile(r'\*\*命题\s+([\d.]+)\s*\(([^)]+)\)\s*\*\*', re.IGNORECASE)
    COR_PATTERN = re.compile(r'\*\*推论\s+([\d.]+)\s*\(([^)]+)\)\s*\*\*', re.IGNORECASE)
    
    # 编号形式: Thm-S-01-01, Def-K-02-01, Lemma-F-03-01
    FORMAL_ID_PATTERN = re.compile(r'(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d+)-(\d+)', re.IGNORECASE)
    
    # 内部链接模式
    INTERNAL_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(\.?/?([^)]+\.md)\)')
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.formal_elements: Dict[str, FormalElement] = {}
        
    def generate_node_id(self, path: str) -> str:
        """为文档生成唯一节点ID"""
        rel_path = Path(path).relative_to(self.base_path)
        return str(rel_path).replace('\\', '/').replace('/', '_').replace('.md', '')
    
    def parse_document(self, file_path: Path) -> Optional[Node]:
        """解析单个Markdown文档"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"  警告: 无法读取文件 {file_path}: {e}")
            return None
        
        rel_path = file_path.relative_to(self.base_path)
        node_id = self.generate_node_id(file_path)
        
        # 提取标题
        title_match = self.HEADER_PATTERN.search(content)
        title = title_match.group(1) if title_match else file_path.stem
        
        # 清理标题
        title = re.sub(r'\([^)]+\)$', '', title).strip()
        
        # 确定类别 (Struct/Knowledge/Flink)
        category = self._determine_category(rel_path)
        
        # 提取元数据
        metadata = self._extract_metadata(content)
        level = metadata.get('形式化等级', '')
        if not level and 'formalization_level' in metadata:
            level = metadata['formalization_level']
        
        # 提取描述（第一个段落）
        description = self._extract_description(content)
        
        # 提取标签
        tags = self._extract_tags(content, category)
        
        # 提取依赖关系
        dependencies = self._extract_dependencies(content)
        
        # 提取形式化元素
        self._extract_formal_elements(content, node_id, str(rel_path))
        
        # 提取内部链接
        internal_links = self._extract_internal_links(content)
        
        node = Node(
            id=node_id,
            label=title,
            type='document',
            category=category,
            level=level,
            path=str(rel_path).replace('\\', '/'),
            description=description[:200] + '...' if len(description) > 200 else description,
            tags=tags,
            dependencies=dependencies,
            metadata=metadata
        )
        
        return node, internal_links
    
    def _determine_category(self, rel_path: Path) -> str:
        """确定文档类别"""
        path_str = str(rel_path).lower()
        if path_str.startswith('struct'):
            return 'Struct'
        elif path_str.startswith('knowledge'):
            return 'Knowledge'
        elif path_str.startswith('flink'):
            return 'Flink'
        else:
            return 'Root'
    
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
        # 跳过标题和元数据块，找第一个段落
        lines = content.split('\n')
        description = []
        in_meta = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                continue
            if line.startswith('>') or line.startswith('|'):
                continue
            if line.startswith('```') or line.startswith('---'):
                continue
            if line.startswith('[') and line.endswith(')'):
                continue
            
            # 清理Markdown标记
            clean_line = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
            clean_line = re.sub(r'\*([^*]+)\*', r'\1', clean_line)
            clean_line = re.sub(r'`([^`]+)`', r'\1', clean_line)
            
            if clean_line:
                description.append(clean_line)
                if len(description) >= 3:
                    break
        
        return ' '.join(description)
    
    def _extract_tags(self, content: str, category: str) -> List[str]:
        """提取文档标签"""
        tags = [category]
        
        # 根据内容添加标签
        if 'checkpoint' in content.lower() or 'checkpoint' in str(Path).lower():
            tags.append('Checkpoint')
        if 'watermark' in content.lower():
            tags.append('Watermark')
        if 'exactly-once' in content.lower() or 'exactly once' in content.lower():
            tags.append('Exactly-Once')
        if 'state' in content.lower():
            tags.append('State')
        if 'pattern' in str(Path).lower():
            tags.append('Pattern')
        if 'proof' in str(Path).lower():
            tags.append('Proof')
        if 'formal' in content.lower() or '定理' in content or '定义' in content:
            tags.append('Formal')
        if 'flink' in content.lower():
            tags.append('Flink')
        
        return list(set(tags))
    
    def _extract_dependencies(self, content: str) -> List[str]:
        """提取文档依赖关系"""
        dependencies = []
        
        # 查找关联文档部分
        related_section = re.search(r'##\s+关联文档[^#]*', content, re.IGNORECASE | re.DOTALL)
        if related_section:
            section_content = related_section.group(0)
            for match in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', section_content):
                dep_path = match.group(2)
                dependencies.append(dep_path)
        
        # 查找前置依赖
        dep_match = self.DEPENDENCY_PATTERN.search(content)
        if dep_match:
            dep_path = dep_match.group(2)
            if dep_path not in dependencies and dep_path != '无':
                dependencies.append(dep_path)
        
        return dependencies
    
    def _extract_formal_elements(self, content: str, document_id: str, document_path: str):
        """提取形式化元素（定理、定义等）"""
        
        # 提取带编号的形式化元素
        for pattern, elem_type in [
            (self.FORMAL_ID_PATTERN, 'formal_id'),
        ]:
            for match in pattern.finditer(content):
                elem_id = match.group(0)
                elem_name = match.group(0)
                
                if elem_id not in self.formal_elements:
                    self.formal_elements[elem_id] = FormalElement(
                        id=elem_id,
                        type=elem_type,
                        name=elem_name,
                        document=document_id,
                        document_path=document_path
                    )
    
    def _extract_internal_links(self, content: str) -> List[Tuple[str, str]]:
        """提取内部链接"""
        links = []
        for match in self.INTERNAL_LINK_PATTERN.finditer(content):
            link_text = match.group(1)
            link_path = match.group(2)
            links.append((link_text, link_path))
        return links
    
    def scan_directory(self, directory: str) -> Tuple[List[Node], List[Edge]]:
        """扫描目录中的所有Markdown文件"""
        print(f"扫描目录: {directory}")
        
        base_path = Path(self.base_path) / directory
        if not base_path.exists():
            print(f"  警告: 目录不存在 {base_path}")
            return [], []
        
        all_internal_links = {}  # node_id -> [(text, path), ...]
        
        for md_file in base_path.rglob('*.md'):
            result = self.parse_document(md_file)
            if result:
                node, internal_links = result
                self.nodes[node.id] = node
                all_internal_links[node.id] = internal_links
                print(f"  解析: {node.path} -> {node.id}")
        
        # 构建边关系
        self._build_edges(all_internal_links)
        
        return list(self.nodes.values()), self.edges
    
    def _build_edges(self, all_internal_links: Dict[str, List[Tuple[str, str]]]):
        """构建文档间边关系"""
        
        # 从内部链接构建边
        for source_id, links in all_internal_links.items():
            for link_text, link_path in links:
                # 解析目标路径
                target_id = self._resolve_link_path(link_path)
                if target_id and target_id in self.nodes and target_id != source_id:
                    edge = Edge(
                        source=source_id,
                        target=target_id,
                        type='references',
                        label='引用'
                    )
                    self.edges.append(edge)
        
        # 从依赖关系构建边
        for node in self.nodes.values():
            for dep_path in node.dependencies:
                target_id = self._resolve_link_path(dep_path)
                if target_id and target_id in self.nodes and target_id != node.id:
                    edge = Edge(
                        source=node.id,
                        target=target_id,
                        type='depends_on',
                        label='依赖'
                    )
                    self.edges.append(edge)
    
    def _resolve_link_path(self, link_path: str) -> Optional[str]:
        """解析链接路径为节点ID"""
        # 清理路径
        clean_path = link_path.replace('../', '').replace('./', '')
        clean_path = clean_path.replace('\\', '/')
        
        # 尝试匹配节点
        for node_id, node in self.nodes.items():
            if node.path.endswith(clean_path) or clean_path in node.path:
                return node_id
        
        # 尝试从路径生成ID
        if clean_path.endswith('.md'):
            return clean_path.replace('/', '_').replace('.md', '')
        
        return None


# =============================================================================
# 图谱生成器
# =============================================================================

class GraphGenerator:
    """图谱生成器"""
    
    def __init__(self, nodes: List[Node], edges: List[Edge], output_dir: str):
        self.nodes = nodes
        self.edges = edges
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_cytoscape_json(self) -> str:
        """生成Cytoscape JSON格式"""
        elements = []
        
        # 颜色映射
        color_map = {
            'Struct': '#e3f2fd',      # 浅蓝
            'Knowledge': '#e8f5e9',   # 浅绿
            'Flink': '#fff3e0',       # 浅橙
            'Root': '#f3e5f5'         # 浅紫
        }
        
        border_map = {
            'Struct': '#1976d2',
            'Knowledge': '#388e3c',
            'Flink': '#f57c00',
            'Root': '#7b1fa2'
        }
        
        for node in self.nodes:
            elements.append({
                'data': {
                    'id': node.id,
                    'label': node.label,
                    'type': node.type,
                    'category': node.category,
                    'level': node.level,
                    'path': node.path,
                    'description': node.description,
                    'tags': node.tags,
                    'color': color_map.get(node.category, '#eeeeee'),
                    'borderColor': border_map.get(node.category, '#666666')
                }
            })
        
        for edge in self.edges:
            elements.append({
                'data': {
                    'id': f"{edge.source}_{edge.target}_{edge.type}",
                    'source': edge.source,
                    'target': edge.target,
                    'type': edge.type,
                    'label': edge.label,
                    'weight': edge.weight
                }
            })
        
        output_path = self.output_dir / 'knowledge-graph-cytoscape.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(elements, f, ensure_ascii=False, indent=2)
        
        print(f"  生成: {output_path}")
        return str(output_path)
    
    def generate_graphviz_dot(self) -> str:
        """生成Graphviz DOT格式"""
        lines = ['digraph KnowledgeGraph {']
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
        
        # 子图分组
        categories = defaultdict(list)
        for node in self.nodes:
            categories[node.category].append(node)
        
        for category, nodes in categories.items():
            lines.append(f'  subgraph cluster_{category} {{')
            lines.append(f'    label="{category}";')
            lines.append(f'    style=filled;')
            lines.append(f'    color={color_map.get(category, "#eeeeee")};')
            lines.append(f'    fontname="Microsoft YaHei";')
            
            for node in nodes:
                label = node.label.replace('"', '\\"')
                tooltip = node.description.replace('"', '\\"') if node.description else label
                lines.append(f'    "{node.id}" [label="{label}", fillcolor={color_map.get(category, "#ffffff")}, tooltip="{tooltip[:100]}..."];')
            
            lines.append('  }')
            lines.append('')
        
        # 边
        for edge in self.edges:
            lines.append(f'  "{edge.source}" -> "{edge.target}" [label="{edge.label}", color="#666666"];')
        
        lines.append('}')
        
        output_path = self.output_dir / 'knowledge-graph.dot'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"  生成: {output_path}")
        return str(output_path)
    
    def generate_d3_json(self) -> str:
        """生成D3.js可用的JSON格式"""
        data = {
            'nodes': [node.to_dict() for node in self.nodes],
            'links': [edge.to_dict() for edge in self.edges]
        }
        
        output_path = self.output_dir / 'knowledge-graph-d3.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"  生成: {output_path}")
        return str(output_path)
    
    def generate_hierarchy_json(self) -> str:
        """生成层级结构JSON"""
        hierarchy = {
            'name': 'AnalysisDataFlow',
            'children': []
        }
        
        # 按类别分组
        categories = defaultdict(lambda: {'name': '', 'children': []})
        
        for node in self.nodes:
            cat = node.category
            if cat not in categories:
                categories[cat]['name'] = cat
            
            # 提取子目录
            path_parts = node.path.split('/')
            if len(path_parts) > 1:
                subdir = path_parts[1] if path_parts[0] == cat else path_parts[0]
            else:
                subdir = '其他'
            
            # 查找或创建子目录
            subdir_found = False
            for child in categories[cat]['children']:
                if child['name'] == subdir:
                    child['children'].append({
                        'name': node.label,
                        'id': node.id,
                        'path': node.path,
                        'level': node.level
                    })
                    subdir_found = True
                    break
            
            if not subdir_found:
                categories[cat]['children'].append({
                    'name': subdir,
                    'children': [{
                        'name': node.label,
                        'id': node.id,
                        'path': node.path,
                        'level': node.level
                    }]
                })
        
        hierarchy['children'] = list(categories.values())
        
        output_path = self.output_dir / 'knowledge-hierarchy.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(hierarchy, f, ensure_ascii=False, indent=2)
        
        print(f"  生成: {output_path}")
        return str(output_path)


# =============================================================================
# HTML交互页面生成器
# =============================================================================

class HTMLGenerator:
    """HTML交互页面生成器"""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
    
    def generate_interactive_html(self) -> str:
        """生成交互式HTML页面"""
        html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AnalysisDataFlow 知识图谱</title>
    <script src="https://unpkg.com/cytoscape@3.26.0/dist/cytoscape.min.js"></script>
    <script src="https://unpkg.com/dagre@0.8.5/dist/dagre.min.js"></script>
    <script src="https://unpkg.com/cytoscape-dagre@2.5.0/cytoscape-dagre.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Microsoft YaHei', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            padding: 15px 30px;
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .header h1 {
            font-size: 24px;
            color: #333;
            font-weight: 600;
        }
        
        .header .subtitle {
            font-size: 14px;
            color: #666;
            margin-left: 10px;
        }
        
        .controls {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        
        .control-btn {
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            background: #667eea;
            color: white;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
        }
        
        .control-btn:hover {
            background: #5a6fd6;
            transform: translateY(-2px);
        }
        
        .control-select {
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 14px;
            background: white;
        }
        
        .search-box {
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 14px;
            width: 200px;
        }
        
        .main-container {
            display: flex;
            height: 100vh;
            padding-top: 70px;
        }
        
        .sidebar {
            width: 300px;
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            overflow-y: auto;
            box-shadow: 2px 0 20px rgba(0,0,0,0.1);
        }
        
        .sidebar h3 {
            font-size: 16px;
            margin-bottom: 15px;
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 8px;
        }
        
        .legend {
            margin-bottom: 25px;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            margin: 8px 0;
            font-size: 14px;
            color: #555;
        }
        
        .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 4px;
            margin-right: 10px;
            border: 2px solid;
        }
        
        .legend-struct { background: #e3f2fd; border-color: #1976d2; }
        .legend-knowledge { background: #e8f5e9; border-color: #388e3c; }
        .legend-flink { background: #fff3e0; border-color: #f57c00; }
        
        .stats {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .stat-item {
            display: flex;
            justify-content: space-between;
            margin: 8px 0;
            font-size: 14px;
        }
        
        .stat-value {
            font-weight: 600;
            color: #667eea;
        }
        
        .node-info {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
        }
        
        .node-info h4 {
            font-size: 16px;
            margin-bottom: 10px;
            color: #333;
        }
        
        .node-info p {
            font-size: 14px;
            color: #666;
            line-height: 1.6;
            margin: 8px 0;
        }
        
        .node-info .tag {
            display: inline-block;
            padding: 3px 8px;
            background: #e3f2fd;
            color: #1976d2;
            border-radius: 4px;
            font-size: 12px;
            margin: 2px;
        }
        
        .node-info a {
            color: #667eea;
            text-decoration: none;
        }
        
        .node-info a:hover {
            text-decoration: underline;
        }
        
        #cy {
            flex: 1;
            background: #fafafa;
        }
        
        .tooltip {
            position: absolute;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 12px;
            pointer-events: none;
            z-index: 1000;
            max-width: 300px;
            display: none;
        }
        
        .loading {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 30px 50px;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            text-align: center;
            z-index: 2000;
        }
        
        .loading-spinner {
            width: 40px;
            height: 40px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .filter-section {
            margin-bottom: 20px;
        }
        
        .filter-section h4 {
            font-size: 14px;
            margin-bottom: 10px;
            color: #333;
        }
        
        .filter-checkbox {
            display: flex;
            align-items: center;
            margin: 5px 0;
            font-size: 13px;
            color: #555;
        }
        
        .filter-checkbox input {
            margin-right: 8px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>📚 AnalysisDataFlow 知识图谱</h1>
            <span class="subtitle">流计算理论与工程实践知识库可视化</span>
        </div>
        <div class="controls">
            <input type="text" class="search-box" id="searchBox" placeholder="搜索文档...">
            <select class="control-select" id="layoutSelect">
                <option value="dagre">层次布局</option>
                <option value="cose">有机布局</option>
                <option value="circle">环形布局</option>
                <option value="grid">网格布局</option>
            </select>
            <button class="control-btn" onclick="resetZoom()">重置视图</button>
            <button class="control-btn" onclick="exportGraph()">导出图片</button>
        </div>
    </div>
    
    <div class="main-container">
        <div class="sidebar">
            <div class="stats">
                <h3>📊 统计信息</h3>
                <div class="stat-item">
                    <span>文档总数</span>
                    <span class="stat-value" id="nodeCount">0</span>
                </div>
                <div class="stat-item">
                    <span>引用关系</span>
                    <span class="stat-value" id="edgeCount">0</span>
                </div>
                <div class="stat-item">
                    <span>Struct文档</span>
                    <span class="stat-value" id="structCount">0</span>
                </div>
                <div class="stat-item">
                    <span>Knowledge文档</span>
                    <span class="stat-value" id="knowledgeCount">0</span>
                </div>
                <div class="stat-item">
                    <span>Flink文档</span>
                    <span class="stat-value" id="flinkCount">0</span>
                </div>
            </div>
            
            <div class="legend">
                <h3>📌 图例说明</h3>
                <div class="legend-item">
                    <div class="legend-color legend-struct"></div>
                    <span>Struct - 形式理论</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color legend-knowledge"></div>
                    <span>Knowledge - 工程知识</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color legend-flink"></div>
                    <span>Flink - 技术专项</span>
                </div>
            </div>
            
            <div class="filter-section">
                <h4>🔍 筛选显示</h4>
                <label class="filter-checkbox">
                    <input type="checkbox" id="showStruct" checked onchange="applyFilters()">
                    <span>显示 Struct 文档</span>
                </label>
                <label class="filter-checkbox">
                    <input type="checkbox" id="showKnowledge" checked onchange="applyFilters()">
                    <span>显示 Knowledge 文档</span>
                </label>
                <label class="filter-checkbox">
                    <input type="checkbox" id="showFlink" checked onchange="applyFilters()">
                    <span>显示 Flink 文档</span>
                </label>
            </div>
            
            <div class="node-info" id="nodeInfo">
                <h4>ℹ️ 节点信息</h4>
                <p>点击图谱中的节点查看详细信息</p>
            </div>
        </div>
        
        <div id="cy"></div>
    </div>
    
    <div class="tooltip" id="tooltip"></div>
    
    <div class="loading" id="loading">
        <div class="loading-spinner"></div>
        <p>正在加载知识图谱...</p>
    </div>

    <script>
        let cy = null;
        let allElements = [];
        
        // 初始化图谱
        async function initGraph() {
            try {
                // 加载数据
                const response = await fetch('knowledge-graph-cytoscape.json');
                allElements = await response.json();
                
                // 统计
                const nodes = allElements.filter(e => e.data.id && !e.data.source);
                const edges = allElements.filter(e => e.data.source);
                
                document.getElementById('nodeCount').textContent = nodes.length;
                document.getElementById('edgeCount').textContent = edges.length;
                document.getElementById('structCount').textContent = 
                    nodes.filter(n => n.data.category === 'Struct').length;
                document.getElementById('knowledgeCount').textContent = 
                    nodes.filter(n => n.data.category === 'Knowledge').length;
                document.getElementById('flinkCount').textContent = 
                    nodes.filter(n => n.data.category === 'Flink').length;
                
                // 初始化 Cytoscape
                cy = cytoscape({
                    container: document.getElementById('cy'),
                    elements: allElements,
                    style: [
                        {
                            selector: 'node',
                            style: {
                                'background-color': 'data(color)',
                                'border-color': 'data(borderColor)',
                                'border-width': 2,
                                'label': 'data(label)',
                                'width': 40,
                                'height': 40,
                                'font-size': '12px',
                                'font-family': 'Microsoft YaHei',
                                'text-valign': 'bottom',
                                'text-halign': 'center',
                                'text-margin-y': 5,
                                'text-background-color': 'rgba(255,255,255,0.8)',
                                'text-background-opacity': 0.8,
                                'text-background-padding': '2px 4px',
                                'text-background-shape': 'roundrectangle'
                            }
                        },
                        {
                            selector: 'edge',
                            style: {
                                'width': 1,
                                'line-color': '#999',
                                'target-arrow-color': '#999',
                                'target-arrow-shape': 'triangle',
                                'curve-style': 'bezier',
                                'label': 'data(label)',
                                'font-size': '10px',
                                'font-family': 'Microsoft YaHei'
                            }
                        },
                        {
                            selector: ':selected',
                            style: {
                                'border-width': 4,
                                'border-color': '#ff5722',
                                'shadow-blur': 10,
                                'shadow-color': '#ff5722'
                            }
                        }
                    ],
                    layout: {
                        name: 'dagre',
                        rankDir: 'TB',
                        nodeSep: 50,
                        edgeSep: 20,
                        rankSep: 80,
                        padding: 20
                    }
                });
                
                // 事件绑定
                cy.on('tap', 'node', function(evt) {
                    showNodeInfo(evt.target);
                });
                
                cy.on('mouseover', 'node', function(evt) {
                    const node = evt.target;
                    const tooltip = document.getElementById('tooltip');
                    tooltip.innerHTML = `<strong>${node.data('label')}</strong><br>${node.data('category')}`;
                    tooltip.style.display = 'block';
                });
                
                cy.on('mousemove', 'node', function(evt) {
                    const tooltip = document.getElementById('tooltip');
                    tooltip.style.left = evt.originalEvent.pageX + 10 + 'px';
                    tooltip.style.top = evt.originalEvent.pageY + 10 + 'px';
                });
                
                cy.on('mouseout', 'node', function() {
                    document.getElementById('tooltip').style.display = 'none';
                });
                
                // 布局切换
                document.getElementById('layoutSelect').addEventListener('change', function(e) {
                    applyLayout(e.target.value);
                });
                
                // 搜索
                document.getElementById('searchBox').addEventListener('input', function(e) {
                    searchNodes(e.target.value);
                });
                
                // 隐藏加载
                document.getElementById('loading').style.display = 'none';
                
            } catch (error) {
                console.error('加载图谱失败:', error);
                document.getElementById('loading').innerHTML = 
                    `<p style="color:red">加载失败: ${error.message}</p>`;
            }
        }
        
        // 显示节点信息
        function showNodeInfo(node) {
            const data = node.data();
            const tags = data.tags ? data.tags.map(t => `<span class="tag">${t}</span>`).join('') : '';
            const level = data.level ? `<p><strong>形式化等级:</strong> ${data.level}</p>` : '';
            
            document.getElementById('nodeInfo').innerHTML = `
                <h4>${data.label}</h4>
                <p><strong>类别:</strong> ${data.category}</p>
                ${level}
                <p><strong>路径:</strong> ${data.path}</p>
                <p>${data.description || ''}</p>
                <div>${tags}</div>
                <p style="margin-top:10px">
                    <a href="../${data.path}" target="_blank">📄 查看文档</a>
                </p>
            `;
        }
        
        // 应用布局
        function applyLayout(layoutName) {
            let layout;
            switch(layoutName) {
                case 'dagre':
                    layout = cy.layout({
                        name: 'dagre',
                        rankDir: 'TB',
                        nodeSep: 50,
                        edgeSep: 20,
                        rankSep: 80,
                        padding: 20
                    });
                    break;
                case 'cose':
                    layout = cy.layout({
                        name: 'cose',
                        padding: 20,
                        nodeRepulsion: 8000,
                        edgeElasticity: 100,
                        nestingFactor: 5
                    });
                    break;
                case 'circle':
                    layout = cy.layout({
                        name: 'circle',
                        padding: 20
                    });
                    break;
                case 'grid':
                    layout = cy.layout({
                        name: 'grid',
                        padding: 20
                    });
                    break;
            }
            if (layout) layout.run();
        }
        
        // 搜索节点
        function searchNodes(query) {
            if (!query) {
                cy.elements().show();
                return;
            }
            
            const matched = cy.nodes().filter(n => {
                const data = n.data();
                return data.label.toLowerCase().includes(query.toLowerCase()) ||
                       data.path.toLowerCase().includes(query.toLowerCase());
            });
            
            cy.elements().hide();
            matched.show();
            matched.connectedEdges().show();
            matched.neighborhood().show();
        }
        
        // 应用筛选
        function applyFilters() {
            const showStruct = document.getElementById('showStruct').checked;
            const showKnowledge = document.getElementById('showKnowledge').checked;
            const showFlink = document.getElementById('showFlink').checked;
            
            cy.nodes().forEach(node => {
                const category = node.data('category');
                let shouldShow = false;
                if (category === 'Struct' && showStruct) shouldShow = true;
                if (category === 'Knowledge' && showKnowledge) shouldShow = true;
                if (category === 'Flink' && showFlink) shouldShow = true;
                
                if (shouldShow) {
                    node.show();
                } else {
                    node.hide();
                }
            });
            
            // 隐藏孤立的边
            cy.edges().forEach(edge => {
                if (edge.source().visible() && edge.target().visible()) {
                    edge.show();
                } else {
                    edge.hide();
                }
            });
        }
        
        // 重置缩放
        function resetZoom() {
            cy.fit();
            cy.center();
        }
        
        // 导出图片
        function exportGraph() {
            const png = cy.png({
                bg: 'white',
                full: true,
                maxWidth: 4000,
                maxHeight: 4000
            });
            const link = document.createElement('a');
            link.download = 'knowledge-graph.png';
            link.href = png;
            link.click();
        }
        
        // 启动
        document.addEventListener('DOMContentLoaded', initGraph);
    </script>
</body>
</html>
'''
        
        output_path = self.output_dir / 'knowledge-graph.html'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"  生成: {output_path}")
        return str(output_path)
    
    def generate_learning_path_html(self) -> str:
        """生成学习路径HTML页面"""
        html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AnalysisDataFlow 学习路径</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Microsoft YaHei', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        h1 {
            text-align: center;
            color: white;
            font-size: 36px;
            margin-bottom: 10px;
        }
        
        .subtitle {
            text-align: center;
            color: rgba(255,255,255,0.8);
            margin-bottom: 40px;
        }
        
        .path-container {
            background: white;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        
        .path-title {
            font-size: 24px;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }
        
        .path-title.struct { border-color: #1976d2; }
        .path-title.knowledge { border-color: #388e3c; }
        .path-title.flink { border-color: #f57c00; }
        
        .path-steps {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .step {
            display: flex;
            align-items: center;
            padding: 15px 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            transition: all 0.3s;
        }
        
        .step:hover {
            transform: translateX(10px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .step-number {
            width: 36px;
            height: 36px;
            background: #667eea;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 15px;
            flex-shrink: 0;
        }
        
        .step-content {
            flex: 1;
        }
        
        .step-title {
            font-size: 16px;
            font-weight: 600;
            color: #333;
            margin-bottom: 4px;
        }
        
        .step-desc {
            font-size: 14px;
            color: #666;
        }
        
        .step-link {
            padding: 8px 16px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-size: 14px;
            transition: all 0.3s;
        }
        
        .step-link:hover {
            background: #5a6fd6;
        }
        
        .back-link {
            text-align: center;
            margin-top: 30px;
        }
        
        .back-link a {
            color: white;
            text-decoration: none;
            font-size: 16px;
            padding: 12px 30px;
            background: rgba(255,255,255,0.2);
            border-radius: 30px;
            transition: all 0.3s;
        }
        
        .back-link a:hover {
            background: rgba(255,255,255,0.3);
        }
        
        .level-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            margin-left: 8px;
        }
        
        .level-L1 { background: #e8f5e9; color: #2e7d32; }
        .level-L2 { background: #e3f2fd; color: #1565c0; }
        .level-L3 { background: #fff3e0; color: #ef6c00; }
        .level-L4 { background: #fce4ec; color: #c2185b; }
        .level-L5 { background: #f3e5f5; color: #7b1fa2; }
        .level-L6 { background: #ffebee; color: #c62828; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 AnalysisDataFlow 学习路径</h1>
        <p class="subtitle">从理论到实践，系统化掌握流计算知识体系</p>
        
        <div class="path-container">
            <h2 class="path-title struct">🔬 Struct 理论路径</h2>
            <div class="path-steps">
                <div class="step">
                    <div class="step-number">1</div>
                    <div class="step-content">
                        <div class="step-title">统一流计算理论 <span class="level-badge level-L6">L6</span></div>
                        <div class="step-desc">USTM元模型、六层表达能力层次、统一并发模型表示</div>
                    </div>
                    <a href="../Struct/01-foundation/01.01-unified-streaming-theory.md" class="step-link">开始学习</a>
                </div>
                <div class="step">
                    <div class="step-number">2</div>
                    <div class="step-content">
                        <div class="step-title">进程演算基础 <span class="level-badge level-L4">L4</span></div>
                        <div class="step-desc">CCS、CSP、π-calculus基础概念与语法</div>
                    </div>
                    <a href="../Struct/01-foundation/01.02-process-calculus-primer.md" class="step-link">开始学习</a>
                </div>
                <div class="step">
                    <div class="step-number">3</div>
                    <div class="step-content">
                        <div class="step-title">Actor模型形式化 <span class="level-badge level-L4">L4</span></div>
                        <div class="step-desc">Actor模型语义、消息传递、监督策略</div>
                    </div>
                    <a href="../Struct/01-foundation/01.03-actor-model-formalization.md" class="step-link">开始学习</a>
                </div>
                <div class="step">
                    <div class="step-number">4</div>
                    <div class="step-content">
                        <div class="step-title">流计算正确性证明 <span class="level-badge level-L6">L6</span></div>
                        <div class="step-desc">Checkpoint一致性、Exactly-Once正确性证明</div>
                    </div>
                    <a href="../Struct/04-proofs/04.01-flink-checkpoint-correctness.md" class="step-link">开始学习</a>
                </div>
            </div>
        </div>
        
        <div class="path-container">
            <h2 class="path-title knowledge">🛠️ Knowledge 工程路径</h2>
            <div class="path-steps">
                <div class="step">
                    <div class="step-number">1</div>
                    <div class="step-content">
                        <div class="step-title">并发范式对比矩阵 <span class="level-badge level-L3">L3</span></div>
                        <div class="step-desc">Actor、CSP、Dataflow等并发模型对比</div>
                    </div>
                    <a href="../Knowledge/01-concept-atlas/concurrency-paradigms-matrix.md" class="step-link">开始学习</a>
                </div>
                <div class="step">
                    <div class="step-number">2</div>
                    <div class="step-content">
                        <div class="step-title">设计模式: Checkpoint与故障恢复 <span class="level-badge level-L5">L5</span></div>
                        <div class="step-desc">分布式快照、Barrier对齐、状态后端选择</div>
                    </div>
                    <a href="../Knowledge/02-design-patterns/pattern-checkpoint-recovery.md" class="step-link">开始学习</a>
                </div>
                <div class="step">
                    <div class="step-number">3</div>
                    <div class="step-content">
                        <div class="step-title">电商实时推荐案例 <span class="level-badge level-L4">L4</span></div>
                        <div class="step-desc">实时特征工程、推荐系统架构实践</div>
                    </div>
                    <a href="../Knowledge/03-business-patterns/real-time-recommendation.md" class="step-link">开始学习</a>
                </div>
                <div class="step">
                    <div class="step-number">4</div>
                    <div class="step-content">
                        <div class="step-title">反模式识别 <span class="level-badge level-L3">L3</span></div>
                        <div class="step-desc">常见流处理错误模式与解决方案</div>
                    </div>
                    <a href="../Knowledge/09-anti-patterns/anti-pattern-checklist.md" class="step-link">开始学习</a>
                </div>
            </div>
        </div>
        
        <div class="path-container">
            <h2 class="path-title flink">⚡ Flink 技术路径</h2>
            <div class="path-steps">
                <div class="step">
                    <div class="step-number">1</div>
                    <div class="step-content">
                        <div class="step-title">Flink架构概览 <span class="level-badge level-L4">L4</span></div>
                        <div class="step-desc">Runtime架构、部署模式、DataStream API</div>
                    </div>
                    <a href="../Flink/01-architecture/deployment-architectures.md" class="step-link">开始学习</a>
                </div>
                <div class="step">
                    <div class="step-number">2</div>
                    <div class="step-content">
                        <div class="step-title">Checkpoint机制深度剖析 <span class="level-badge level-L4">L4</span></div>
                        <div class="step-desc">Barrier传播、对齐/非对齐Checkpoint、增量快照</div>
                    </div>
                    <a href="../Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md" class="step-link">开始学习</a>
                </div>
                <div class="step">
                    <div class="step-number">3</div>
                    <div class="step-content">
                        <div class="step-title">SQL与Table API <span class="level-badge level-L4">L4</span></div>
                        <div class="step-desc">Flink SQL、窗口函数、物化表</div>
                    </div>
                    <a href="../Flink/03-sql-table-api/flink-table-sql-complete-guide.md" class="step-link">开始学习</a>
                </div>
                <div class="step">
                    <div class="step-number">4</div>
                    <div class="step-content">
                        <div class="step-title">性能调优指南 <span class="level-badge level-L4">L4</span></div>
                        <div class="step-desc">State后端选择、内存调优、反压处理</div>
                    </div>
                    <a href="../Flink/06-engineering/performance-tuning-guide.md" class="step-link">开始学习</a>
                </div>
            </div>
        </div>
        
        <div class="back-link">
            <a href="knowledge-graph.html">🔙 返回知识图谱</a>
        </div>
    </div>
</body>
</html>
'''
        
        output_path = self.output_dir / 'learning-path.html'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"  生成: {output_path}")
        return str(output_path)


# =============================================================================
# 主程序
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='AnalysisDataFlow 知识图谱生成器')
    parser.add_argument('--base-path', default='.', help='项目根目录')
    parser.add_argument('--output', default='visuals', help='输出目录')
    parser.add_argument('--directories', nargs='+', default=['Struct', 'Knowledge', 'Flink'],
                       help='要扫描的目录')
    args = parser.parse_args()
    
    base_path = Path(args.base_path).resolve()
    output_dir = base_path / args.output
    
    print("=" * 60)
    print("AnalysisDataFlow 知识图谱生成器 v1.0.0")
    print("=" * 60)
    print(f"项目路径: {base_path}")
    print(f"输出目录: {output_dir}")
    print()
    
    # 创建解析器
    parser_obj = DocumentParser(base_path)
    
    all_nodes = []
    all_edges = []
    
    # 扫描各目录
    for directory in args.directories:
        print(f"\n扫描 {directory}/ ...")
        dir_path = base_path / directory
        if dir_path.exists():
            nodes, edges = parser_obj.scan_directory(directory)
            all_nodes.extend(nodes)
            all_edges.extend(edges)
            print(f"  发现 {len(nodes)} 个文档, {len(edges)} 个关系")
        else:
            print(f"  警告: 目录 {directory} 不存在")
    
    print(f"\n总计: {len(all_nodes)} 个文档, {len(all_edges)} 个关系")
    print(f"形式化元素: {len(parser_obj.formal_elements)} 个")
    
    # 生成图谱数据
    print("\n生成图谱数据...")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generator = GraphGenerator(all_nodes, all_edges, output_dir)
    
    generator.generate_cytoscape_json()
    generator.generate_graphviz_dot()
    generator.generate_d3_json()
    generator.generate_hierarchy_json()
    
    # 生成HTML页面
    print("\n生成交互式页面...")
    html_gen = HTMLGenerator(output_dir)
    html_gen.generate_interactive_html()
    html_gen.generate_learning_path_html()
    
    # 输出统计
    print("\n" + "=" * 60)
    print("生成完成!")
    print("=" * 60)
    print(f"\n输出文件:")
    print(f"  📊 knowledge-graph-cytoscape.json - Cytoscape JSON格式")
    print(f"  📊 knowledge-graph-d3.json - D3.js JSON格式")
    print(f"  📊 knowledge-hierarchy.json - 层级结构JSON")
    print(f"  📝 knowledge-graph.dot - Graphviz DOT格式")
    print(f"  🌐 knowledge-graph.html - 交互式图谱页面")
    print(f"  📖 learning-path.html - 学习路径页面")
    print(f"\n使用方法:")
    print(f"  1. 在浏览器中打开: {output_dir}/knowledge-graph.html")
    print(f"  2. 查看学习路径: {output_dir}/learning-path.html")
    print(f"  3. 使用Graphviz生成SVG: dot -Tsvg {output_dir}/knowledge-graph.dot -o graph.svg")
    print()


if __name__ == '__main__':
    main()
