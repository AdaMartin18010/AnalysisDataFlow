#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AnalysisDataFlow 文档关系自动映射器 (P2-11)

功能：
1. 扫描所有文档的前置依赖
2. 提取交叉引用关系
3. 生成关系图谱数据（JSON格式）
4. 检测循环依赖
5. 识别孤立文档

输出：
- KNOWLEDGE-GRAPH/relationship-map.json - 完整关系图谱
- KNOWLEDGE-GRAPH/doc-dependencies.json - 文档依赖关系
- KNOWLEDGE-GRAPH/circular-deps.json - 循环依赖检测

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
from collections import defaultdict, deque
import argparse
from datetime import datetime


@dataclass
class DocumentNode:
    """文档节点"""
    id: str
    path: str
    title: str
    category: str  # Struct, Knowledge, Flink
    level: str = ""  # 形式化等级 L1-L6
    dependencies: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)
    referenced_by: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


@dataclass
class RelationshipEdge:
    """关系边"""
    source: str
    target: str
    type: str  # depends_on, references, cites
    weight: float = 1.0


class DocumentScanner:
    """文档扫描器"""
    
    # 正则表达式模式
    HEADER_PATTERN = re.compile(r'^#\s+(.+)$', re.MULTILINE)
    
    # 前置依赖模式
    DEPENDENCY_PATTERNS = [
        re.compile(r'前置依赖:\s*\[([^\]]+)\]\(([^)]+)\)'),
        re.compile(r'前置依赖:\s*([^\n]+)'),
        re.compile(r'Dependencies?:\s*\[([^\]]+)\]\(([^)]+)\)'),
    ]
    
    # 内部链接模式
    INTERNAL_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(\.?/?([^)]+\.md)\)')
    
    # 引用模式 [^n]: ...
    CITATION_PATTERN = re.compile(r'\[\^(\d+)\]:\s*(.+)')
    
    # 形式化元素引用
    FORMAL_REF_PATTERN = re.compile(r'(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d+)-(\d+)', re.IGNORECASE)
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.documents: Dict[str, DocumentNode] = {}
        self.edges: List[RelationshipEdge] = []
        
    def scan_all_documents(self) -> Tuple[List[DocumentNode], List[RelationshipEdge]]:
        """扫描所有文档"""
        print("🔍 开始扫描文档...")
        
        directories = ['Struct', 'Knowledge', 'Flink']
        
        for directory in directories:
            dir_path = self.base_path / directory
            if not dir_path.exists():
                print(f"  ⚠️ 目录不存在: {directory}")
                continue
            
            print(f"  📁 扫描 {directory}/")
            for md_file in dir_path.rglob('*.md'):
                self._parse_document(md_file)
        
        # 构建边关系
        self._build_relationships()
        
        print(f"\n✅ 扫描完成: {len(self.documents)} 个文档, {len(self.edges)} 个关系")
        
        return list(self.documents.values()), self.edges
    
    def _parse_document(self, file_path: Path):
        """解析单个文档"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"    ⚠️ 无法读取: {file_path.name} - {e}")
            return
        
        rel_path = file_path.relative_to(self.base_path)
        doc_id = str(rel_path).replace('\\', '/').replace('/', '_').replace('.md', '')
        
        # 提取标题
        title_match = self.HEADER_PATTERN.search(content)
        title = title_match.group(1) if title_match else file_path.stem
        title = re.sub(r'\([^)]+\)$', '', title).strip()
        
        # 确定类别
        category = self._determine_category(rel_path)
        
        # 提取元数据
        metadata = self._extract_metadata(content)
        level = metadata.get('形式化等级', '')
        
        # 提取依赖
        dependencies = self._extract_dependencies(content, str(rel_path))
        
        # 提取引用
        references = self._extract_references(content, str(rel_path))
        
        doc = DocumentNode(
            id=doc_id,
            path=str(rel_path).replace('\\', '/'),
            title=title,
            category=category,
            level=level,
            dependencies=dependencies,
            references=references,
            metadata=metadata
        )
        
        self.documents[doc_id] = doc
        print(f"    ✓ {rel_path.name}")
    
    def _determine_category(self, rel_path: Path) -> str:
        """确定文档类别"""
        path_str = str(rel_path).lower()
        if path_str.startswith('struct'):
            return 'Struct'
        elif path_str.startswith('knowledge'):
            return 'Knowledge'
        elif path_str.startswith('flink'):
            return 'Flink'
        return 'Other'
    
    def _extract_metadata(self, content: str) -> Dict[str, str]:
        """提取元数据"""
        metadata = {}
        
        # 查找元数据块
        meta_block = re.search(r'^>\s*所属阶段:[^\n]+(\n>\s*[^\n]+)*', content, re.MULTILINE)
        if meta_block:
            block_content = meta_block.group(0)
            for match in re.finditer(r'>\s*\*\*([^:]+)\*\*:\s*([^|\n]+)', block_content):
                key = match.group(1).strip()
                value = match.group(2).strip()
                metadata[key] = value
        
        return metadata
    
    def _extract_dependencies(self, content: str, current_path: str) -> List[str]:
        """提取前置依赖"""
        dependencies = []
        
        for pattern in self.DEPENDENCY_PATTERNS:
            for match in pattern.finditer(content):
                if len(match.groups()) >= 2:
                    dep_path = match.group(2)
                else:
                    dep_path = match.group(1)
                
                # 解析相对路径
                resolved_path = self._resolve_path(dep_path, current_path)
                if resolved_path:
                    dep_id = resolved_path.replace('/', '_').replace('.md', '')
                    if dep_id not in dependencies:
                        dependencies.append(dep_id)
        
        return dependencies
    
    def _extract_references(self, content: str, current_path: str) -> List[str]:
        """提取文档引用"""
        references = []
        
        for match in self.INTERNAL_LINK_PATTERN.finditer(content):
            ref_path = match.group(2)
            resolved_path = self._resolve_path(ref_path, current_path)
            if resolved_path:
                ref_id = resolved_path.replace('/', '_').replace('.md', '')
                if ref_id not in references:
                    references.append(ref_id)
        
        return references
    
    def _resolve_path(self, link_path: str, current_path: str) -> Optional[str]:
        """解析链接路径"""
        # 清理路径
        clean_path = link_path.replace('../', '').replace('./', '')
        clean_path = clean_path.replace('\\', '/')
        
        # 尝试直接匹配
        if clean_path in [doc.path for doc in self.documents.values()]:
            return clean_path
        
        # 尝试添加 .md 后缀
        if not clean_path.endswith('.md'):
            clean_path_md = clean_path + '.md'
            if clean_path_md in [doc.path for doc in self.documents.values()]:
                return clean_path_md
        
        return clean_path if clean_path.endswith('.md') else None
    
    def _build_relationships(self):
        """构建文档间关系"""
        # 从依赖构建边
        for doc_id, doc in self.documents.items():
            for dep_id in doc.dependencies:
                if dep_id in self.documents:
                    self.edges.append(RelationshipEdge(
                        source=doc_id,
                        target=dep_id,
                        type='depends_on',
                        weight=2.0
                    ))
                    # 更新反向引用
                    self.documents[dep_id].referenced_by.append(doc_id)
            
            for ref_id in doc.references:
                if ref_id in self.documents and ref_id not in doc.dependencies:
                    self.edges.append(RelationshipEdge(
                        source=doc_id,
                        target=ref_id,
                        type='references',
                        weight=1.0
                    ))
                    # 更新反向引用
                    if ref_id in self.documents:
                        self.documents[ref_id].referenced_by.append(doc_id)


class CircularDependencyDetector:
    """循环依赖检测器"""
    
    def __init__(self, documents: Dict[str, DocumentNode], edges: List[RelationshipEdge]):
        self.documents = documents
        self.edges = edges
        self.adjacency = defaultdict(list)
        self._build_adjacency()
    
    def _build_adjacency(self):
        """构建邻接表"""
        for edge in self.edges:
            if edge.type == 'depends_on':
                self.adjacency[edge.source].append(edge.target)
    
    def detect_cycles(self) -> List[List[str]]:
        """检测所有循环依赖（使用DFS）"""
        cycles = []
        visited = set()
        rec_stack = set()
        path = []
        
        def dfs(node):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in self.adjacency[node]:
                if neighbor not in visited:
                    result = dfs(neighbor)
                    if result:
                        return result
                elif neighbor in rec_stack:
                    # 找到循环
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    cycles.append(cycle)
            
            path.pop()
            rec_stack.remove(node)
            return None
        
        for node in self.documents:
            if node not in visited:
                dfs(node)
        
        return cycles
    
    def find_entry_points(self) -> List[str]:
        """找到入口点（无依赖的文档）"""
        entry_points = []
        for doc_id, doc in self.documents.items():
            if not doc.dependencies:
                entry_points.append(doc_id)
        return entry_points
    
    def find_isolated_documents(self) -> List[str]:
        """找到孤立文档（无依赖也无被引用）"""
        isolated = []
        for doc_id, doc in self.documents.items():
            if not doc.dependencies and not doc.referenced_by and not doc.references:
                isolated.append(doc_id)
        return isolated


class RelationshipMapExporter:
    """关系图谱导出器"""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_full_map(self, documents: List[DocumentNode], edges: List[RelationshipEdge]):
        """导出完整关系图谱"""
        data = {
            'metadata': {
                'version': '2.0',
                'generated_at': datetime.now().isoformat(),
                'total_documents': len(documents),
                'total_relationships': len(edges)
            },
            'nodes': [asdict(doc) for doc in documents],
            'edges': [asdict(edge) for edge in edges]
        }
        
        output_path = self.output_dir / 'relationship-map.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"  ✓ 导出完整关系图谱: {output_path}")
        return output_path
    
    def export_dependencies(self, documents: List[DocumentNode]):
        """导出依赖关系"""
        deps = {}
        for doc in documents:
            deps[doc.id] = {
                'path': doc.path,
                'title': doc.title,
                'dependencies': doc.dependencies,
                'references': doc.references,
                'referenced_by': doc.referenced_by
            }
        
        output_path = self.output_dir / 'doc-dependencies.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(deps, f, ensure_ascii=False, indent=2)
        
        print(f"  ✓ 导出依赖关系: {output_path}")
        return output_path
    
    def export_circular_deps(self, cycles: List[List[str]], documents: Dict[str, DocumentNode]):
        """导出循环依赖"""
        data = {
            'count': len(cycles),
            'cycles': []
        }
        
        for cycle in cycles:
            cycle_info = {
                'length': len(cycle) - 1,
                'documents': [
                    {
                        'id': doc_id,
                        'path': documents.get(doc_id, DocumentNode(id=doc_id, path='', title='', category='')).path,
                        'title': documents.get(doc_id, DocumentNode(id=doc_id, path='', title='', category='')).title
                    }
                    for doc_id in cycle[:-1]
                ]
            }
            data['cycles'].append(cycle_info)
        
        output_path = self.output_dir / 'circular-deps.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"  ✓ 导出循环依赖: {output_path}")
        return output_path
    
    def export_graphviz_dot(self, documents: List[DocumentNode], edges: List[RelationshipEdge]):
        """导出Graphviz DOT格式"""
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
            'Other': '#f3e5f5'
        }
        
        # 子图分组
        categories = defaultdict(list)
        for doc in documents:
            categories[doc.category].append(doc)
        
        for category, docs in categories.items():
            lines.append(f'  subgraph cluster_{category} {{')
            lines.append(f'    label="{category}";')
            lines.append(f'    style=filled;')
            lines.append(f'    color={color_map.get(category, "#eeeeee")};')
            lines.append(f'    fontname="Microsoft YaHei";')
            
            for doc in docs:
                label = doc.title.replace('"', '\\"')
                lines.append(f'    "{doc.id}" [label="{label}", fillcolor={color_map.get(category, "#ffffff")}];')
            
            lines.append('  }')
            lines.append('')
        
        # 边
        for edge in edges:
            style = 'dashed' if edge.type == 'depends_on' else 'solid'
            lines.append(f'  "{edge.source}" -> "{edge.target}" [style={style}];')
        
        lines.append('}')
        
        output_path = self.output_dir / 'relationship-graph.dot'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"  ✓ 导出 DOT 格式: {output_path}")
        return output_path


def generate_report(documents: List[DocumentNode], edges: List[RelationshipEdge], 
                   cycles: List[List[str]], entry_points: List[str], 
                   isolated: List[str], output_dir: Path):
    """生成关系分析报告"""
    report_path = output_dir / 'RELATIONSHIP-ANALYSIS-REPORT.md'
    
    # 统计信息
    category_counts = defaultdict(int)
    for doc in documents:
        category_counts[doc.category] += 1
    
    edge_type_counts = defaultdict(int)
    for edge in edges:
        edge_type_counts[edge.type] += 1
    
    report = f"""# AnalysisDataFlow 文档关系分析报告

> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> **文档总数**: {len(documents)}
> **关系总数**: {len(edges)}

---

## 📊 概览统计

### 文档分布

| 类别 | 数量 | 占比 |
|------|------|------|
| Struct | {category_counts.get('Struct', 0)} | {category_counts.get('Struct', 0)/len(documents)*100:.1f}% |
| Knowledge | {category_counts.get('Knowledge', 0)} | {category_counts.get('Knowledge', 0)/len(documents)*100:.1f}% |
| Flink | {category_counts.get('Flink', 0)} | {category_counts.get('Flink', 0)/len(documents)*100:.1f}% |

### 关系类型

| 类型 | 数量 | 说明 |
|------|------|------|
| 依赖 (depends_on) | {edge_type_counts.get('depends_on', 0)} | 前置依赖关系 |
| 引用 (references) | {edge_type_counts.get('references', 0)} | 一般引用关系 |

---

## 🔄 循环依赖检测

**检测结果**: {'✅ 未发现循环依赖' if not cycles else f'⚠️ 发现 {len(cycles)} 个循环依赖'}

"""
    
    if cycles:
        report += "### 循环详情\n\n"
        for i, cycle in enumerate(cycles, 1):
            report += f"#### 循环 #{i}\n"
            report += "依赖路径: " + " → ".join(cycle) + "\n\n"
    
    report += f"""
---

## 🚪 入口点文档

**数量**: {len(entry_points)}

入口点是指没有前置依赖的文档，适合作为学习起点：

"""
    
    for doc_id in entry_points[:20]:  # 只显示前20个
        doc = next((d for d in documents if d.id == doc_id), None)
        if doc:
            report += f"- **{doc.title}** (`{doc.path}`)\n"
    
    if len(entry_points) > 20:
        report += f"\n... 还有 {len(entry_points) - 20} 个入口点\n"
    
    report += f"""

---

## 🔍 孤立文档

**数量**: {len(isolated)}

孤立文档是指既无依赖也无被引用的文档：

"""
    
    if isolated:
        for doc_id in isolated:
            doc = next((d for d in documents if d.id == doc_id), None)
            if doc:
                report += f"- **{doc.title}** (`{doc.path}`)\n"
    else:
        report += "✅ 未发现孤立文档\n"
    
    report += """

---

## 📁 输出文件

| 文件 | 描述 |
|------|------|
| `relationship-map.json` | 完整关系图谱 (JSON) |
| `doc-dependencies.json` | 文档依赖关系 |
| `circular-deps.json` | 循环依赖检测 |
| `relationship-graph.dot` | Graphviz DOT格式 |

---

*本报告由文档关系自动映射器生成*
"""
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"  ✓ 生成分析报告: {report_path}")
    return report_path


def main():
    parser = argparse.ArgumentParser(description='AnalysisDataFlow 文档关系自动映射器')
    parser.add_argument('-b', '--base-path', default='.', help='项目根目录')
    parser.add_argument('-o', '--output', default='KNOWLEDGE-GRAPH', help='输出目录')
    parser.add_argument('--cycles-only', action='store_true', help='仅检测循环依赖')
    args = parser.parse_args()
    
    print("=" * 60)
    print("🔍 AnalysisDataFlow 文档关系自动映射器 (P2-11)")
    print("=" * 60)
    
    # 扫描文档
    scanner = DocumentScanner(args.base_path)
    documents, edges = scanner.scan_all_documents()
    
    # 检测循环依赖
    print("\n🔄 检测循环依赖...")
    detector = CircularDependencyDetector(scanner.documents, edges)
    cycles = detector.detect_cycles()
    entry_points = detector.find_entry_points()
    isolated = detector.find_isolated_documents()
    
    print(f"  发现 {len(cycles)} 个循环依赖")
    print(f"  发现 {len(entry_points)} 个入口点")
    print(f"  发现 {len(isolated)} 个孤立文档")
    
    # 导出结果
    print("\n📤 导出结果...")
    exporter = RelationshipMapExporter(args.output)
    exporter.export_full_map(documents, edges)
    exporter.export_dependencies(documents)
    exporter.export_circular_deps(cycles, scanner.documents)
    exporter.export_graphviz_dot(documents, edges)
    
    # 生成报告
    print("\n📝 生成报告...")
    generate_report(documents, edges, cycles, entry_points, isolated, exporter.output_dir)
    
    print("\n" + "=" * 60)
    print("✅ 文档关系映射完成!")
    print(f"📁 输出目录: {Path(args.output).absolute()}")
    print("=" * 60)


if __name__ == '__main__':
    main()
