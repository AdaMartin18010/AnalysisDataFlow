#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AnalysisDataFlow 知识图谱数据生成器 v2.0

功能：
1. 自动扫描所有.md文档
2. 提取形式化元素（定理、定义、引理）
3. 提取文档依赖关系
4. 生成知识图谱数据文件（JSON格式）
5. 支持增量更新

作者: AnalysisDataFlow Team
版本: 2.0.0
日期: 2026-04-04
"""

import os
import re
import json
import hashlib
import argparse
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
from datetime import datetime


@dataclass
class GraphNode:
    """图谱节点"""
    id: str
    label: str
    type: str  # document, theorem, definition, lemma, proposition, corollary, concept
    group: str  # Struct, Knowledge, Flink
    size: float
    color: str
    metadata: Dict = field(default_factory=dict)


@dataclass
class GraphEdge:
    """图谱边"""
    source: str
    target: str
    type: str  # contains, dependency, citation, hierarchy, proves, defines
    weight: float = 1.0


@dataclass
class FormalElement:
    """形式化元素"""
    id: str
    type: str  # theorem, definition, lemma, proposition, corollary
    name: str
    document_id: str
    document_path: str
    description: str = ""
    dependencies: List[str] = field(default_factory=list)


class FormalElementExtractor:
    """形式化元素提取器"""
    
    # 定理模式: **定理 X.X (Thm-S-01-01)** 或 Thm-S-01-01
    THEOREM_PATTERNS = [
        re.compile(r'\*\*定理\s*[\d.]+\s*\((Thm-[SKF]-\d+-\d+)\)\s*\*\*', re.IGNORECASE),
        re.compile(r'\*\*定理\s+[\d.]+[:：]\s*([^\*\n]+)\*\*', re.IGNORECASE),
        re.compile(r'\*\*\s*(Thm-[SKF]-\d+-\d+)\s*\*\*', re.IGNORECASE),
    ]
    
    # 定义模式
    DEFINITION_PATTERNS = [
        re.compile(r'\*\*定义\s*[\d.]+\s*\((Def-[SKF]-\d+-\d+)\)\s*\*\*', re.IGNORECASE),
        re.compile(r'\*\*定义\s+[\d.]+[:：]\s*([^\*\n]+)\*\*', re.IGNORECASE),
        re.compile(r'\*\*\s*(Def-[SKF]-\d+-\d+)\s*\*\*', re.IGNORECASE),
    ]
    
    # 引理模式
    LEMMA_PATTERNS = [
        re.compile(r'\*\*引理\s*[\d.]+\s*\((Lemma-[SKF]-\d+-\d+)\)\s*\*\*', re.IGNORECASE),
        re.compile(r'\*\*引理\s+[\d.]+[:：]\s*([^\*\n]+)\*\*', re.IGNORECASE),
        re.compile(r'\*\*\s*(Lemma-[SKF]-\d+-\d+)\s*\*\*', re.IGNORECASE),
    ]
    
    # 命题模式
    PROPOSITION_PATTERNS = [
        re.compile(r'\*\*命题\s*[\d.]+\s*\((Prop-[SKF]-\d+-\d+)\)\s*\*\*', re.IGNORECASE),
        re.compile(r'\*\*命题\s+[\d.]+[:：]\s*([^\*\n]+)\*\*', re.IGNORECASE),
        re.compile(r'\*\*\s*(Prop-[SKF]-\d+-\d+)\s*\*\*', re.IGNORECASE),
    ]
    
    # 推论模式
    COROLLARY_PATTERNS = [
        re.compile(r'\*\*推论\s*[\d.]+\s*\((Cor-[SKF]-\d+-\d+)\)\s*\*\*', re.IGNORECASE),
        re.compile(r'\*\*推论\s+[\d.]+[:：]\s*([^\*\n]+)\*\*', re.IGNORECASE),
        re.compile(r'\*\*\s*(Cor-[SKF]-\d+-\d+)\s*\*\*', re.IGNORECASE),
    ]
    
    # 形式化ID模式 (全局搜索)
    FORMAL_ID_PATTERN = re.compile(
        r'\b(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d+)-(\d+)\b',
        re.IGNORECASE
    )
    
    # 引用形式化元素的模式
    REFERENCE_PATTERN = re.compile(
        r'(?:参见|see|引用|ref)[:：]?\s*(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d+)-(\d+)',
        re.IGNORECASE
    )
    
    COLORS = {
        'theorem': '#D9534F',
        'definition': '#9B59B6',
        'lemma': '#17A2B8',
        'proposition': '#E83E8C',
        'corollary': '#6C757D'
    }
    
    def __init__(self):
        self.elements: Dict[str, FormalElement] = {}
    
    def extract_from_content(self, content: str, document_id: str, document_path: str) -> List[FormalElement]:
        """从文档内容中提取形式化元素"""
        found = []
        
        # 提取定理
        for pattern in self.THEOREM_PATTERNS:
            for match in pattern.finditer(content):
                elem_id = match.group(1) if '(' in match.group(0) else f"Thm-{document_id[:1].upper()}-{hash(match.group(0)) % 1000:03d}"
                elem_name = match.group(1) if len(match.groups()) > 0 else match.group(0)
                
                # 提取描述（后续3行）
                desc = self._extract_description(content, match.end())
                
                element = FormalElement(
                    id=elem_id,
                    type='theorem',
                    name=elem_name,
                    document_id=document_id,
                    document_path=document_path,
                    description=desc
                )
                
                if elem_id not in self.elements:
                    self.elements[elem_id] = element
                    found.append(element)
        
        # 提取定义
        for pattern in self.DEFINITION_PATTERNS:
            for match in pattern.finditer(content):
                elem_id = match.group(1) if '(' in match.group(0) else f"Def-{document_id[:1].upper()}-{hash(match.group(0)) % 1000:03d}"
                elem_name = match.group(1) if len(match.groups()) > 0 else match.group(0)
                desc = self._extract_description(content, match.end())
                
                element = FormalElement(
                    id=elem_id,
                    type='definition',
                    name=elem_name,
                    document_id=document_id,
                    document_path=document_path,
                    description=desc
                )
                
                if elem_id not in self.elements:
                    self.elements[elem_id] = element
                    found.append(element)
        
        # 提取引理
        for pattern in self.LEMMA_PATTERNS:
            for match in pattern.finditer(content):
                elem_id = match.group(1) if '(' in match.group(0) else f"Lemma-{document_id[:1].upper()}-{hash(match.group(0)) % 1000:03d}"
                elem_name = match.group(1) if len(match.groups()) > 0 else match.group(0)
                desc = self._extract_description(content, match.end())
                
                element = FormalElement(
                    id=elem_id,
                    type='lemma',
                    name=elem_name,
                    document_id=document_id,
                    document_path=document_path,
                    description=desc
                )
                
                if elem_id not in self.elements:
                    self.elements[elem_id] = element
                    found.append(element)
        
        # 提取命题
        for pattern in self.PROPOSITION_PATTERNS:
            for match in pattern.finditer(content):
                elem_id = match.group(1) if '(' in match.group(0) else f"Prop-{document_id[:1].upper()}-{hash(match.group(0)) % 1000:03d}"
                elem_name = match.group(1) if len(match.groups()) > 0 else match.group(0)
                desc = self._extract_description(content, match.end())
                
                element = FormalElement(
                    id=elem_id,
                    type='proposition',
                    name=elem_name,
                    document_id=document_id,
                    document_path=document_path,
                    description=desc
                )
                
                if elem_id not in self.elements:
                    self.elements[elem_id] = element
                    found.append(element)
        
        # 提取推论
        for pattern in self.COROLLARY_PATTERNS:
            for match in pattern.finditer(content):
                elem_id = match.group(1) if '(' in match.group(0) else f"Cor-{document_id[:1].upper()}-{hash(match.group(0)) % 1000:03d}"
                elem_name = match.group(1) if len(match.groups()) > 0 else match.group(0)
                desc = self._extract_description(content, match.end())
                
                element = FormalElement(
                    id=elem_id,
                    type='corollary',
                    name=elem_name,
                    document_id=document_id,
                    document_path=document_path,
                    description=desc
                )
                
                if elem_id not in self.elements:
                    self.elements[elem_id] = element
                    found.append(element)
        
        return found
    
    def _extract_description(self, content: str, start_pos: int) -> str:
        """提取描述（从指定位置开始的3行）"""
        lines = content[start_pos:start_pos + 500].split('\n')
        desc_lines = []
        
        for line in lines[1:]:  # 跳过匹配行
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('>'):
                continue
            if line.startswith('**定义**') or line.startswith('**定理**'):
                break
            
            # 清理Markdown标记
            clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
            clean = re.sub(r'`([^`]+)`', r'\1', clean)
            
            if clean:
                desc_lines.append(clean)
                if len(desc_lines) >= 2:
                    break
        
        return ' '.join(desc_lines)[:200]
    
    def extract_cross_references(self, content: str) -> List[Tuple[str, str]]:
        """提取交叉引用"""
        refs = []
        for match in self.REFERENCE_PATTERN.finditer(content):
            elem_type = match.group(1)
            stage = match.group(2)
            num1 = match.group(3)
            num2 = match.group(4)
            elem_id = f"{elem_type}-{stage}-{num1}-{num2}"
            refs.append((elem_id, match.group(0)))
        return refs
    
    def get_all_elements(self) -> List[FormalElement]:
        """获取所有提取的形式化元素"""
        return list(self.elements.values())


class DocumentScanner:
    """文档扫描器"""
    
    # 链接模式
    LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+\.md)\)')
    
    # 依赖模式
    DEPENDENCY_PATTERN = re.compile(
        r'前置依赖[:：]\s*\[?([^\]\n]+)\]?\s*\(?([^\)]+)?\)?',
        re.IGNORECASE
    )
    
    # 元数据模式
    META_PATTERN = re.compile(
        r'^>\s*\*\*([^:]+)\*\*[:：]\s*(.+)',
        re.MULTILINE
    )
    
    COLORS = {
        'Struct': '#4A90D9',
        'Knowledge': '#5CB85C',
        'Flink': '#F0AD4E'
    }
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.documents: List[Dict] = []
        
    def scan_all(self) -> List[Dict]:
        """扫描所有文档"""
        print("🔍 扫描文档...")
        
        directories = ['Struct', 'Knowledge', 'Flink']
        
        for directory in directories:
            dir_path = self.base_path / directory
            if not dir_path.exists():
                print(f"  ⚠️ 目录不存在: {directory}")
                continue
            
            for md_file in dir_path.rglob('*.md'):
                try:
                    doc = self._parse_document(md_file, directory)
                    if doc:
                        self.documents.append(doc)
                        print(f"  📄 {doc['path']}")
                except Exception as e:
                    print(f"  ❌ 解析失败 {md_file}: {e}")
        
        print(f"\n✅ 共扫描 {len(self.documents)} 个文档\n")
        return self.documents
    
    def _parse_document(self, file_path: Path, category: str) -> Optional[Dict]:
        """解析单个文档"""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return None
        
        rel_path = file_path.relative_to(self.base_path)
        doc_id = str(rel_path).replace('\\', '_').replace('/', '_').replace('.md', '')
        
        # 提取标题
        title = self._extract_title(content, file_path)
        
        # 提取元数据
        metadata = self._extract_metadata(content)
        level = metadata.get('形式化等级', '')
        
        # 提取链接
        links = self._extract_links(content, rel_path)
        
        # 提取依赖
        dependencies = self._extract_dependencies(content)
        
        # 计算文档大小（基于字数）
        word_count = len(content)
        
        # 计算节点大小
        size = 15 + min(word_count / 1000, 30)
        
        return {
            'id': doc_id,
            'label': title,
            'type': 'document',
            'group': category,
            'size': size,
            'color': self.COLORS.get(category, '#999999'),
            'path': str(rel_path).replace('\\', '/'),
            'level': level,
            'word_count': word_count,
            'metadata': metadata,
            'links': links,
            'dependencies': dependencies,
            'content': content[:5000]  # 保留部分内容用于后续处理
        }
    
    def _extract_title(self, content: str, file_path: Path) -> str:
        """提取标题"""
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            title = match.group(1).strip()
            title = re.sub(r'\s*\([^)]*\)$', '', title)
            return title
        return file_path.stem
    
    def _extract_metadata(self, content: str) -> Dict[str, str]:
        """提取元数据"""
        metadata = {}
        
        meta_block = re.search(r'^>\s*所属阶段:[^\n]+(\n>\s*[^\n]+)*', content, re.MULTILINE)
        if meta_block:
            block_content = meta_block.group(0)
            for match in re.finditer(r'>\s*\*\*([^:]+)\*\*[:：]\s*([^|\n]+)', block_content):
                key = match.group(1).strip()
                value = match.group(2).strip()
                metadata[key] = value
        
        return metadata
    
    def _extract_links(self, content: str, rel_path: Path) -> List[Tuple[str, str]]:
        """提取链接"""
        links = []
        for match in self.LINK_PATTERN.finditer(content):
            link_text = match.group(1)
            link_path = match.group(2)
            links.append((link_text, link_path))
        return links
    
    def _extract_dependencies(self, content: str) -> List[str]:
        """提取依赖"""
        dependencies = []
        
        for match in self.DEPENDENCY_PATTERN.finditer(content):
            dep_text = match.group(1).strip()
            dep_path = match.group(2) if match.group(2) else dep_text
            if dep_path and dep_path != '无':
                dependencies.append(dep_path)
        
        return dependencies


class GraphBuilder:
    """图谱构建器"""
    
    def __init__(self, documents: List[Dict], formal_elements: List[FormalElement]):
        self.documents = documents
        self.formal_elements = formal_elements
        self.nodes: List[GraphNode] = []
        self.edges: List[GraphEdge] = []
        
    def build(self) -> Dict:
        """构建知识图谱"""
        print("🏗️ 构建知识图谱...")
        
        # 添加文档节点
        self._add_document_nodes()
        
        # 添加形式化元素节点
        self._add_formal_element_nodes()
        
        # 添加包含关系（文档 -> 形式化元素）
        self._add_contains_edges()
        
        # 添加依赖关系（文档 -> 文档）
        self._add_dependency_edges()
        
        # 添加引用关系
        self._add_citation_edges()
        
        # 添加层次关系
        self._add_hierarchy_edges()
        
        print(f"  节点: {len(self.nodes)}")
        print(f"  边: {len(self.edges)}\n")
        
        return {
            'nodes': [self._node_to_dict(n) for n in self.nodes],
            'edges': [self._edge_to_dict(e) for e in self.edges],
            'stats': self._calculate_stats()
        }
    
    def _add_document_nodes(self):
        """添加文档节点"""
        for doc in self.documents:
            node = GraphNode(
                id=doc['id'],
                label=doc['label'],
                type='document',
                group=doc['group'],
                size=doc['size'],
                color=doc['color'],
                metadata={
                    'path': doc['path'],
                    'formality_level': doc['level'],
                    'category': doc['path'].split('/')[1] if '/' in doc['path'] else '',
                    'word_count': doc['word_count']
                }
            )
            self.nodes.append(node)
    
    def _add_formal_element_nodes(self):
        """添加形式化元素节点"""
        colors = {
            'theorem': '#D9534F',
            'definition': '#9B59B6',
            'lemma': '#17A2B8',
            'proposition': '#E83E8C',
            'corollary': '#6C757D'
        }
        
        for elem in self.formal_elements:
            node = GraphNode(
                id=elem.id,
                label=elem.name,
                type=elem.type,
                group=elem.type,
                size=10,
                color=colors.get(elem.type, '#999999'),
                metadata={
                    'description': elem.description,
                    'document': elem.document_id,
                    'path': elem.document_path
                }
            )
            self.nodes.append(node)
    
    def _add_contains_edges(self):
        """添加包含关系边"""
        for elem in self.formal_elements:
            edge = GraphEdge(
                source=elem.document_id,
                target=elem.id,
                type='contains',
                weight=1
            )
            self.edges.append(edge)
    
    def _add_dependency_edges(self):
        """添加依赖关系边"""
        doc_map = {doc['id']: doc for doc in self.documents}
        
        for doc in self.documents:
            for dep_path in doc.get('dependencies', []):
                # 尝试匹配依赖
                for target_doc in self.documents:
                    if dep_path in target_doc['path'] or target_doc['path'] in dep_path:
                        if doc['id'] != target_doc['id']:
                            edge = GraphEdge(
                                source=doc['id'],
                                target=target_doc['id'],
                                type='dependency',
                                weight=2
                            )
                            self.edges.append(edge)
                        break
    
    def _add_citation_edges(self):
        """添加引用关系边"""
        doc_map = {doc['id']: doc for doc in self.documents}
        
        for doc in self.documents:
            content = doc.get('content', '')
            
            # 查找对其他文档的引用
            for target_doc in self.documents:
                if doc['id'] != target_doc['id']:
                    # 检查标题引用
                    if target_doc['label'] in content:
                        edge = GraphEdge(
                            source=doc['id'],
                            target=target_doc['id'],
                            type='citation',
                            weight=1
                        )
                        self.edges.append(edge)
    
    def _add_hierarchy_edges(self):
        """添加层次关系边（基于路径结构）"""
        for doc in self.documents:
            path_parts = doc['path'].split('/')
            
            # 寻找父文档
            if len(path_parts) > 2:
                parent_path = '/'.join(path_parts[:-1])
                for target_doc in self.documents:
                    if target_doc['path'].startswith(parent_path) and target_doc['id'] != doc['id']:
                        # 检查是否直接父子关系
                        target_parts = target_doc['path'].split('/')
                        if len(target_parts) == len(path_parts) - 1:
                            edge = GraphEdge(
                                source=doc['id'],
                                target=target_doc['id'],
                                type='hierarchy',
                                weight=0.5
                            )
                            self.edges.append(edge)
                            break
    
    def _node_to_dict(self, node: GraphNode) -> Dict:
        """节点转字典"""
        return {
            'id': node.id,
            'label': node.label,
            'type': node.type,
            'group': node.group,
            'size': node.size,
            'color': node.color,
            'metadata': node.metadata
        }
    
    def _edge_to_dict(self, edge: GraphEdge) -> Dict:
        """边转字典"""
        return {
            'source': edge.source,
            'target': edge.target,
            'type': edge.type,
            'weight': edge.weight
        }
    
    def _calculate_stats(self) -> Dict:
        """计算统计信息"""
        doc_nodes = [n for n in self.nodes if n.type == 'document']
        formal_nodes = [n for n in self.nodes if n.type != 'document']
        
        return {
            'total_nodes': len(self.nodes),
            'total_edges': len(self.edges),
            'documents': len(doc_nodes),
            'theorems': len([n for n in formal_nodes if n.type == 'theorem']),
            'definitions': len([n for n in formal_nodes if n.type == 'definition']),
            'lemmas': len([n for n in formal_nodes if n.type == 'lemma']),
            'propositions': len([n for n in formal_nodes if n.type == 'proposition']),
            'corollaries': len([n for n in formal_nodes if n.type == 'corollary']),
            'isolated_documents': self._count_isolated_docs(),
            'generated_at': datetime.now().isoformat()
        }
    
    def _count_isolated_docs(self) -> int:
        """统计孤立文档数"""
        connected = set()
        for edge in self.edges:
            connected.add(edge.source)
            connected.add(edge.target)
        
        isolated = 0
        for node in self.nodes:
            if node.type == 'document' and node.id not in connected:
                isolated += 1
        
        return isolated


class IncrementalUpdater:
    """增量更新器"""
    
    def __init__(self, cache_file: str):
        self.cache_file = Path(cache_file)
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """加载缓存"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_cache(self):
        """保存缓存"""
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)
    
    def get_file_hash(self, file_path: Path) -> str:
        """计算文件哈希"""
        content = file_path.read_bytes()
        return hashlib.md5(content).hexdigest()
    
    def needs_update(self, file_path: Path) -> bool:
        """检查文件是否需要更新"""
        current_hash = self.get_file_hash(file_path)
        cached_hash = self.cache.get(str(file_path))
        return current_hash != cached_hash
    
    def update_cache(self, file_path: Path):
        """更新缓存"""
        self.cache[str(file_path)] = self.get_file_hash(file_path)
        self._save_cache()
    
    def get_modified_files(self, base_path: Path) -> List[Path]:
        """获取修改过的文件列表"""
        modified = []
        
        for directory in ['Struct', 'Knowledge', 'Flink']:
            dir_path = base_path / directory
            if dir_path.exists():
                for md_file in dir_path.rglob('*.md'):
                    if self.needs_update(md_file):
                        modified.append(md_file)
        
        return modified


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='AnalysisDataFlow 知识图谱数据生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本用法
  python knowledge-graph-generator.py
  
  # 指定输出路径
  python knowledge-graph-generator.py --output ./data/graph.json
  
  # 强制完整更新（忽略缓存）
  python knowledge-graph-generator.py --force
  
  # 显示统计信息
  python knowledge-graph-generator.py --stats
        """
    )
    
    parser.add_argument(
        '--base-path', '-b',
        default='.',
        help='项目根目录 (默认: 当前目录)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='.vscode/graph-data.json',
        help='输出文件路径 (默认: .vscode/graph-data.json)'
    )
    
    parser.add_argument(
        '--cache',
        default='.cache/kg-cache.json',
        help='缓存文件路径 (默认: .cache/kg-cache.json)'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='强制完整更新，忽略缓存'
    )
    
    parser.add_argument(
        '--stats',
        action='store_true',
        help='显示统计信息'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("  AnalysisDataFlow 知识图谱数据生成器 v2.0")
    print("=" * 60)
    print()
    
    base_path = Path(args.base_path)
    
    # 初始化增量更新器
    updater = IncrementalUpdater(args.cache)
    
    # 检查修改的文件
    if not args.force:
        modified_files = updater.get_modified_files(base_path)
        if modified_files:
            print(f"📝 发现 {len(modified_files)} 个修改的文件")
        else:
            print("✅ 所有文件均为最新，无需更新")
            if not args.stats:
                return
    
    # 扫描文档
    scanner = DocumentScanner(base_path)
    documents = scanner.scan_all()
    
    if not documents:
        print("❌ 未找到任何文档，请检查目录结构")
        return
    
    # 提取形式化元素
    print("🔬 提取形式化元素...")
    extractor = FormalElementExtractor()
    
    for doc in documents:
        elements = extractor.extract_from_content(
            doc['content'],
            doc['id'],
            doc['path']
        )
        if elements:
            print(f"  从 {doc['path']} 提取 {len(elements)} 个元素")
    
    formal_elements = extractor.get_all_elements()
    print(f"\n✅ 共提取 {len(formal_elements)} 个形式化元素\n")
    
    # 构建图谱
    builder = GraphBuilder(documents, formal_elements)
    graph_data = builder.build()
    
    # 保存结果
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 图谱数据已保存: {output_path}")
    
    # 更新缓存
    for doc in documents:
        file_path = base_path / doc['path']
        if file_path.exists():
            updater.update_cache(file_path)
    
    # 显示统计
    if args.stats or True:
        print("\n" + "=" * 60)
        print("  📊 统计信息")
        print("=" * 60)
        stats = graph_data['stats']
        print(f"  总节点数: {stats['total_nodes']}")
        print(f"  总边数: {stats['total_edges']}")
        print(f"  文档数: {stats['documents']}")
        print(f"  定理数: {stats['theorems']}")
        print(f"  定义数: {stats['definitions']}")
        print(f"  引理数: {stats['lemmas']}")
        print(f"  孤立文档: {stats['isolated_documents']}")
        print("=" * 60)
    
    print("\n✅ 知识图谱生成完成！")


if __name__ == '__main__':
    main()
