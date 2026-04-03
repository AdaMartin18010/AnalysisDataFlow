#!/usr/bin/env python3
"""
AnalysisDataFlow 知识图谱构建脚本

功能：
- 解析所有.md文件，提取文档节点、定理/定义节点
- 提取引用关系（文档→文档、定理→定理）
- 提取依赖关系（前置依赖声明）
- 生成GraphJSON格式的图谱数据

用法：
    python .vscode/build-knowledge-graph.py
    python .vscode/build-knowledge-graph.py --output graph-data.json
    python .vscode/build-knowledge-graph.py --stats
"""

import os
import re
import json
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Any

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 三大输出目录
DIRECTORIES = ['Struct', 'Knowledge', 'Flink']

# 颜色配置（用于可视化）
COLORS = {
    'Struct': '#4A90D9',      # 蓝色 - 形式理论
    'Knowledge': '#5CB85C',   # 绿色 - 知识结构
    'Flink': '#F0AD4E',       # 橙色 - Flink专项
    'theorem': '#D9534F',     # 红色 - 定理
    'definition': '#9B59B6',  # 紫色 - 定义
    'lemma': '#17A2B8',       # 青色 - 引理
    'proposition': '#E83E8C', # 粉色 - 命题
    'corollary': '#6C757D',   # 灰色 - 推论
}

class KnowledgeGraphBuilder:
    """知识图谱构建器"""
    
    def __init__(self):
        self.nodes: List[Dict[str, Any]] = []
        self.edges: List[Dict[str, Any]] = []
        self.node_ids: Set[str] = set()
        self.edge_set: Set[Tuple[str, str, str]] = set()  # (source, target, type)
        
        # 统计信息
        self.stats = {
            'documents': {'Struct': 0, 'Knowledge': 0, 'Flink': 0},
            'theorems': 0,
            'definitions': 0,
            'lemmas': 0,
            'propositions': 0,
            'corollaries': 0,
            'citations': 0,
            'dependencies': 0,
        }
        
        # 定理/定义注册表（用于关联）
        self.theorem_registry: Dict[str, Dict] = {}
        self.doc_registry: Dict[str, Dict] = {}
    
    def extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """提取YAML frontmatter（如果有）"""
        frontmatter = {}
        fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if fm_match:
            yaml_content = fm_match.group(1)
            # 简单解析key: value
            for line in yaml_content.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip()
        return frontmatter
    
    def extract_title(self, content: str, filename: str) -> str:
        """提取文档标题"""
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()
        return Path(filename).stem
    
    def extract_theorems(self, content: str, doc_id: str) -> List[Dict]:
        """提取定理定义（Thm-*）"""
        theorems = []
        # 匹配定理定义：Thm-S-01-01 或 **Thm-S-01-01**
        pattern = r'(?:^|\*\*)((?:Thm|Theorem)-([SKF])-(\d+)-(\d+))\*?\*?(?::|：)?\s*([^\n]+)'
        for match in re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE):
            theorem_id = match.group(1)
            stage = match.group(2)
            doc_num = match.group(3)
            seq_num = match.group(4)
            description = match.group(5).strip()[:100]
            
            theorems.append({
                'id': theorem_id,
                'stage': stage,
                'doc_num': doc_num,
                'seq_num': seq_num,
                'description': description,
                'full_id': f"{theorem_id}"
            })
        return theorems
    
    def extract_definitions(self, content: str, doc_id: str) -> List[Dict]:
        """提取定义（Def-*）"""
        definitions = []
        pattern = r'(?:^|\*\*)((?:Def|Definition)-([SKF])-(\d+)-(\d+))\*?\*?(?::|：)?\s*([^\n]+)'
        for match in re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE):
            def_id = match.group(1)
            stage = match.group(2)
            doc_num = match.group(3)
            seq_num = match.group(4)
            description = match.group(5).strip()[:100]
            
            definitions.append({
                'id': def_id,
                'stage': stage,
                'doc_num': doc_num,
                'seq_num': seq_num,
                'description': description,
                'full_id': f"{def_id}"
            })
        return definitions
    
    def extract_lemmas(self, content: str, doc_id: str) -> List[Dict]:
        """提取引理（Lemma-*）"""
        lemmas = []
        pattern = r'(?:^|\*\*)(Lemma-([SKF])-(\d+)-(\d+))\*?\*?(?::|：)?\s*([^\n]+)'
        for match in re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE):
            lemma_id = match.group(1)
            stage = match.group(2)
            doc_num = match.group(3)
            seq_num = match.group(4)
            description = match.group(5).strip()[:100]
            
            lemmas.append({
                'id': lemma_id,
                'stage': stage,
                'doc_num': doc_num,
                'seq_num': seq_num,
                'description': description,
                'full_id': f"{lemma_id}"
            })
        return lemmas
    
    def extract_propositions(self, content: str, doc_id: str) -> List[Dict]:
        """提取命题（Prop-*）"""
        propositions = []
        pattern = r'(?:^|\*\*)((?:Prop|Proposition)-([SKF])-(\d+)-(\d+))\*?\*?(?::|：)?\s*([^\n]+)'
        for match in re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE):
            prop_id = match.group(1)
            stage = match.group(2)
            doc_num = match.group(3)
            seq_num = match.group(4)
            description = match.group(5).strip()[:100]
            
            propositions.append({
                'id': prop_id,
                'stage': stage,
                'doc_num': doc_num,
                'seq_num': seq_num,
                'description': description,
                'full_id': f"{prop_id}"
            })
        return propositions
    
    def extract_corollaries(self, content: str, doc_id: str) -> List[Dict]:
        """提取推论（Cor-*）"""
        corollaries = []
        pattern = r'(?:^|\*\*)((?:Cor|Corollary)-([SKF])-(\d+)-(\d+))\*?\*?(?::|：)?\s*([^\n]+)'
        for match in re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE):
            cor_id = match.group(1)
            stage = match.group(2)
            doc_num = match.group(3)
            seq_num = match.group(4)
            description = match.group(5).strip()[:100]
            
            corollaries.append({
                'id': cor_id,
                'stage': stage,
                'doc_num': doc_num,
                'seq_num': seq_num,
                'description': description,
                'full_id': f"{cor_id}"
            })
        return corollaries
    
    def extract_dependencies(self, content: str, doc_id: str) -> List[str]:
        """提取前置依赖声明"""
        deps = []
        # 匹配 "前置依赖:" 或 "依赖:" 后的文档链接
        dep_section = re.search(r'(?:前置依赖|依赖|Prerequisites):\s*([^\n]+(?:\n[^#\n]+)*)', content, re.IGNORECASE)
        if dep_section:
            dep_text = dep_section.group(1)
            # 提取Markdown链接
            links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', dep_text)
            for name, link in links:
                deps.append({'name': name, 'link': link})
        return deps
    
    def extract_citations(self, content: str, doc_id: str) -> List[Dict]:
        """提取引用关系（[^n]格式）"""
        citations = []
        # 匹配引用标记 [^n] 或 [^label]
        pattern = r'\[\^([^\]]+)\]'
        for match in re.finditer(pattern, content):
            ref_id = match.group(1)
            citations.append({
                'ref_id': ref_id,
                'context': content[max(0, match.start()-50):min(len(content), match.end()+50)]
            })
        return citations
    
    def extract_cross_refs(self, content: str, doc_id: str) -> List[Dict]:
        """提取交叉引用（引用其他定理/定义）"""
        refs = []
        # 匹配引用其他定理/定义，如 "由 Thm-S-01-01 可知" 或 "参见 Def-K-02-01"
        pattern = r'(?:由|参见|根据|引用|应用|使用|基于)\s*((?:Thm|Theorem|Def|Definition|Lemma|Prop|Proposition|Cor|Corollary)-[SKF]-\d+-\d+)'
        for match in re.finditer(pattern, content, re.IGNORECASE):
            target_id = match.group(1)
            # 规范化ID
            target_id = target_id.replace('Theorem', 'Thm').replace('Definition', 'Def').replace('Proposition', 'Prop').replace('Corollary', 'Cor')
            refs.append({
                'target': target_id,
                'context': content[max(0, match.start()-30):min(len(content), match.end()+30)]
            })
        return refs
    
    def get_doc_category(self, rel_path: str) -> str:
        """获取文档分类（基于路径）"""
        parts = rel_path.split(os.sep)
        if len(parts) > 1:
            return parts[1] if parts[1] not in ['00-INDEX.md'] else 'index'
        return 'root'
    
    def get_formality_level(self, content: str) -> str:
        """检测形式化等级（L1-L6）"""
        if '形式化等级: L6' in content or 'L6' in content[:500]:
            return 'L6'
        elif '形式化等级: L5' in content or 'L5' in content[:500]:
            return 'L5'
        elif '形式化等级: L4' in content or 'L4' in content[:500]:
            return 'L4'
        elif '形式化等级: L3' in content or 'L3' in content[:500]:
            return 'L3'
        elif '形式化等级: L2' in content or 'L2' in content[:500]:
            return 'L2'
        return 'L1'
    
    def parse_document(self, filepath: Path, directory: str) -> Dict:
        """解析单个文档"""
        rel_path = str(filepath.relative_to(PROJECT_ROOT))
        doc_id = f"{directory}/{filepath.stem}"
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"  警告: 无法读取文件 {filepath}: {e}")
            return None
        
        title = self.extract_title(content, filepath.name)
        frontmatter = self.extract_frontmatter(content)
        
        # 提取各种形式化元素
        theorems = self.extract_theorems(content, doc_id)
        definitions = self.extract_definitions(content, doc_id)
        lemmas = self.extract_lemmas(content, doc_id)
        propositions = self.extract_propositions(content, doc_id)
        corollaries = self.extract_corollaries(content, doc_id)
        dependencies = self.extract_dependencies(content, doc_id)
        citations = self.extract_citations(content, doc_id)
        cross_refs = self.extract_cross_refs(content, doc_id)
        
        return {
            'id': doc_id,
            'path': rel_path,
            'title': title,
            'directory': directory,
            'category': self.get_doc_category(rel_path),
            'formality_level': self.get_formality_level(content),
            'frontmatter': frontmatter,
            'theorems': theorems,
            'definitions': definitions,
            'lemmas': lemmas,
            'propositions': propositions,
            'corollaries': corollaries,
            'dependencies': dependencies,
            'citations': citations,
            'cross_refs': cross_refs,
            'word_count': len(content.split()),
        }
    
    def add_node(self, node_id: str, label: str, node_type: str, group: str, 
                 size: int = 10, metadata: Dict = None):
        """添加节点"""
        if node_id in self.node_ids:
            return
        
        node = {
            'id': node_id,
            'label': label,
            'type': node_type,
            'group': group,
            'size': size,
            'color': COLORS.get(group, '#999999'),
        }
        if metadata:
            node['metadata'] = metadata
        
        self.nodes.append(node)
        self.node_ids.add(node_id)
    
    def add_edge(self, source: str, target: str, edge_type: str, weight: int = 1):
        """添加边"""
        edge_key = (source, target, edge_type)
        if edge_key in self.edge_set:
            return
        
        self.edges.append({
            'source': source,
            'target': target,
            'type': edge_type,
            'weight': weight,
        })
        self.edge_set.add(edge_key)
    
    def process_document(self, doc: Dict):
        """处理文档，添加节点和边"""
        doc_id = doc['id']
        directory = doc['directory']
        
        # 添加文档节点
        self.add_node(
            node_id=doc_id,
            label=doc['title'][:50],
            node_type='document',
            group=directory,
            size=min(30, 10 + doc['word_count'] // 500),
            metadata={
                'path': doc['path'],
                'formality_level': doc['formality_level'],
                'category': doc['category'],
                'word_count': doc['word_count'],
            }
        )
        
        # 添加定理节点和边
        for theorem in doc['theorems']:
            thm_id = theorem['full_id']
            self.add_node(
                node_id=thm_id,
                label=f"{theorem['id']}",
                node_type='theorem',
                group='theorem',
                size=8,
                metadata={
                    'description': theorem['description'],
                    'document': doc_id,
                    'stage': theorem['stage'],
                }
            )
            self.add_edge(doc_id, thm_id, 'contains')
            self.theorem_registry[thm_id] = theorem
            self.stats['theorems'] += 1
        
        # 添加定义节点和边
        for definition in doc['definitions']:
            def_id = definition['full_id']
            self.add_node(
                node_id=def_id,
                label=f"{definition['id']}",
                node_type='definition',
                group='definition',
                size=7,
                metadata={
                    'description': definition['description'],
                    'document': doc_id,
                    'stage': definition['stage'],
                }
            )
            self.add_edge(doc_id, def_id, 'contains')
            self.theorem_registry[def_id] = definition
            self.stats['definitions'] += 1
        
        # 添加引理节点和边
        for lemma in doc['lemmas']:
            lemma_id = lemma['full_id']
            self.add_node(
                node_id=lemma_id,
                label=f"{lemma['id']}",
                node_type='lemma',
                group='lemma',
                size=6,
                metadata={
                    'description': lemma['description'],
                    'document': doc_id,
                    'stage': lemma['stage'],
                }
            )
            self.add_edge(doc_id, lemma_id, 'contains')
            self.theorem_registry[lemma_id] = lemma
            self.stats['lemmas'] += 1
        
        # 添加命题节点和边
        for prop in doc['propositions']:
            prop_id = prop['full_id']
            self.add_node(
                node_id=prop_id,
                label=f"{prop['id']}",
                node_type='proposition',
                group='proposition',
                size=6,
                metadata={
                    'description': prop['description'],
                    'document': doc_id,
                    'stage': prop['stage'],
                }
            )
            self.add_edge(doc_id, prop_id, 'contains')
            self.theorem_registry[prop_id] = prop
            self.stats['propositions'] += 1
        
        # 添加推论节点和边
        for cor in doc['corollaries']:
            cor_id = cor['full_id']
            self.add_node(
                node_id=cor_id,
                label=f"{cor['id']}",
                node_type='corollary',
                group='corollary',
                size=5,
                metadata={
                    'description': cor['description'],
                    'document': doc_id,
                    'stage': cor['stage'],
                }
            )
            self.add_edge(doc_id, cor_id, 'contains')
            self.theorem_registry[cor_id] = cor
            self.stats['corollaries'] += 1
        
        # 处理依赖关系
        for dep in doc['dependencies']:
            dep_link = dep['link']
            # 解析相对路径
            if dep_link.startswith('./') or dep_link.startswith('../'):
                # 尝试解析为目标文档ID
                target_doc = self.resolve_doc_link(dep_link, doc['path'])
                if target_doc and target_doc != doc_id:
                    self.add_edge(doc_id, target_doc, 'depends_on', 2)
                    self.stats['dependencies'] += 1
        
        # 处理交叉引用
        for ref in doc['cross_refs']:
            target_id = ref['target']
            if target_id in self.theorem_registry or target_id in self.node_ids:
                self.add_edge(doc_id, target_id, 'references', 1)
                self.stats['citations'] += 1
        
        self.doc_registry[doc_id] = doc
        self.stats['documents'][directory] += 1
    
    def resolve_doc_link(self, link: str, source_path: str) -> str:
        """解析文档链接为目标文档ID"""
        # 简化处理：提取路径中的目录和文件名
        link_clean = link.replace('./', '').replace('../', '')
        link_clean = re.sub(r'\.md$', '', link_clean)
        
        # 尝试匹配已知文档
        for doc_id in self.doc_registry:
            if link_clean in doc_id or doc_id.endswith(link_clean.split('/')[-1]):
                return doc_id
        
        return None
    
    def build_cross_document_refs(self):
        """构建跨文档引用关系"""
        for doc_id, doc in self.doc_registry.items():
            for ref in doc['cross_refs']:
                target_id = ref['target']
                if target_id in self.node_ids:
                    self.add_edge(doc_id, target_id, 'cites_theorem', 1)
    
    def find_isolated_nodes(self) -> List[str]:
        """找出孤立节点（无入边也无出边的文档节点）"""
        connected = set()
        for edge in self.edges:
            connected.add(edge['source'])
            connected.add(edge['target'])
        
        isolated = []
        for node in self.nodes:
            if node['type'] == 'document' and node['id'] not in connected:
                isolated.append(node['id'])
        
        return isolated
    
    def find_hot_documents(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """找出热门文档（被引用最多）"""
        citation_count = defaultdict(int)
        for edge in self.edges:
            if edge['target'] in self.doc_registry:
                citation_count[edge['target']] += 1
        
        return sorted(citation_count.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    def build(self):
        """构建完整知识图谱"""
        print("=" * 60)
        print("AnalysisDataFlow 知识图谱构建")
        print("=" * 60)
        
        # 第一阶段：解析所有文档
        print("\n📄 第一阶段：解析文档...")
        all_docs = []
        
        for directory in DIRECTORIES:
            dir_path = PROJECT_ROOT / directory
            if not dir_path.exists():
                print(f"  警告: 目录不存在 {directory}")
                continue
            
            md_files = list(dir_path.rglob('*.md'))
            print(f"  {directory}/: 找到 {len(md_files)} 个Markdown文件")
            
            for md_file in md_files:
                doc = self.parse_document(md_file, directory)
                if doc:
                    all_docs.append(doc)
        
        print(f"\n  总计解析: {len(all_docs)} 个文档")
        
        # 第二阶段：处理文档（添加节点）
        print("\n🏗️  第二阶段：构建节点...")
        for doc in all_docs:
            self.process_document(doc)
        
        # 第三阶段：构建跨文档引用
        print("\n🔗 第三阶段：构建引用关系...")
        self.build_cross_document_refs()
        
        # 第四阶段：分析
        print("\n📊 第四阶段：分析图谱...")
        isolated = self.find_isolated_nodes()
        hot_docs = self.find_hot_documents(10)
        
        print(f"  孤立文档: {len(isolated)} 个")
        print(f"  热门文档（Top 5）:")
        for doc_id, count in hot_docs[:5]:
            doc_title = self.doc_registry.get(doc_id, {}).get('title', doc_id)
            print(f"    - {doc_title[:40]}: {count} 引用")
        
        return {
            'nodes': self.nodes,
            'edges': self.edges,
            'stats': {
                **self.stats,
                'total_nodes': len(self.nodes),
                'total_edges': len(self.edges),
                'isolated_documents': len(isolated),
                'hot_documents': hot_docs,
            },
            'metadata': {
                'generated_at': str(Path().stat().st_mtime if False else 'now'),
                'version': '1.0',
                'project': 'AnalysisDataFlow',
            }
        }
    
    def export_graphjson(self, output_path: str):
        """导出为GraphJSON格式"""
        data = self.build()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 知识图谱已导出到: {output_path}")
        print(f"   节点: {data['stats']['total_nodes']}")
        print(f"   边: {data['stats']['total_edges']}")
        return data


def print_stats(data: Dict):
    """打印统计信息"""
    stats = data['stats']
    print("\n" + "=" * 60)
    print("知识图谱统计")
    print("=" * 60)
    print(f"\n📁 文档分布:")
    for dir_name, count in stats['documents'].items():
        print(f"   {dir_name}/: {count} 文档")
    
    print(f"\n📐 形式化元素:")
    print(f"   定理: {stats['theorems']}")
    print(f"   定义: {stats['definitions']}")
    print(f"   引理: {stats['lemmas']}")
    print(f"   命题: {stats['propositions']}")
    print(f"   推论: {stats['corollaries']}")
    
    print(f"\n🔗 关系:")
    print(f"   引用关系: {stats['citations']}")
    print(f"   依赖关系: {stats['dependencies']}")
    print(f"   总边数: {stats['total_edges']}")
    
    print(f"\n📈 图谱规模:")
    print(f"   总节点: {stats['total_nodes']}")
    print(f"   孤立文档: {stats['isolated_documents']}")


def main():
    parser = argparse.ArgumentParser(
        description='构建 AnalysisDataFlow 知识图谱',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python build-knowledge-graph.py
  python build-knowledge-graph.py --output graph-data.json
  python build-knowledge-graph.py --stats --output graph-data.json
        """
    )
    parser.add_argument('-o', '--output', default='.vscode/graph-data.json',
                        help='输出文件路径 (默认: .vscode/graph-data.json)')
    parser.add_argument('-s', '--stats', action='store_true',
                        help='打印详细统计信息')
    parser.add_argument('--generate-html', action='store_true',
                        help='同时生成HTML可视化页面')
    
    args = parser.parse_args()
    
    # 构建图谱
    builder = KnowledgeGraphBuilder()
    data = builder.export_graphjson(args.output)
    
    # 打印统计
    if args.stats:
        print_stats(data)
    
    print("\n🎉 知识图谱构建完成!")
    print(f"   打开 knowledge-graph.html 查看可视化")


if __name__ == '__main__':
    main()
