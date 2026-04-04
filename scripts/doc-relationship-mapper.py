#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AnalysisDataFlow 文档关系自动映射脚本

功能：
1. 分析文档间的交叉引用
2. 构建文档依赖图
3. 检测循环依赖
4. 生成文档关系报告

作者: AnalysisDataFlow Team
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
from collections import defaultdict, deque
from datetime import datetime


@dataclass
class DocumentNode:
    """文档节点"""
    id: str
    path: str
    title: str
    category: str  # Struct/Knowledge/Flink
    level: str = ""
    dependencies: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)
    referenced_by: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


@dataclass
class RelationshipEdge:
    """关系边"""
    source: str
    target: str
    type: str  # depends_on, references, contains
    strength: float = 1.0
    context: str = ""  # 引用的上下文


@dataclass
class CycleInfo:
    """循环依赖信息"""
    nodes: List[str]
    length: int
    severity: str  # high/medium/low
    description: str


class DocumentParser:
    """文档解析器"""
    
    # 正则表达式模式
    LINK_PATTERN = re.compile(
        r'\[([^\]]+)\]\(([^)]+\.md)\)',
        re.IGNORECASE
    )
    
    DEPENDENCY_PATTERN = re.compile(
        r'前置依赖[:：]\s*\[?([^\]\n\r]+)\]?\s*\(?([^\)]+)?\)?',
        re.IGNORECASE
    )
    
    META_PATTERN = re.compile(
        r'^>\s*\*\*([^:]+)\*\*[:：]\s*(.+)',
        re.MULTILINE
    )
    
    THEOREM_PATTERN = re.compile(
        r'(?:定理|Theorem)\s+([\w-]+)',
        re.IGNORECASE
    )
    
    DEFINITION_PATTERN = re.compile(
        r'(?:定义|Definition)\s+([\w-]+)',
        re.IGNORECASE
    )
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.documents: Dict[str, DocumentNode] = {}
        self.edges: List[RelationshipEdge] = []
        
    def scan_documents(self) -> Dict[str, DocumentNode]:
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
                    doc = self._parse_document(md_file)
                    if doc:
                        self.documents[doc.id] = doc
                        print(f"  📄 {doc.path}")
                except Exception as e:
                    print(f"  ❌ 解析失败 {md_file}: {e}")
        
        print(f"\n✅ 共扫描 {len(self.documents)} 个文档\n")
        return self.documents
    
    def _parse_document(self, file_path: Path) -> Optional[DocumentNode]:
        """解析单个文档"""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"  警告: 无法读取 {file_path}: {e}")
            return None
        
        rel_path = file_path.relative_to(self.base_path)
        doc_id = self._path_to_id(rel_path)
        
        # 提取标题
        title = self._extract_title(content, file_path)
        
        # 确定类别
        category = self._determine_category(rel_path)
        
        # 提取元数据
        metadata = self._extract_metadata(content)
        level = metadata.get('形式化等级', '')
        
        # 提取依赖
        dependencies = self._extract_dependencies(content, rel_path)
        
        # 提取引用
        references = self._extract_references(content, rel_path)
        
        # 提取形式化元素
        theorems = self.THEOREM_PATTERN.findall(content)
        definitions = self.DEFINITION_PATTERN.findall(content)
        
        return DocumentNode(
            id=doc_id,
            path=str(rel_path).replace('\\', '/'),
            title=title,
            category=category,
            level=level,
            dependencies=dependencies,
            references=references,
            metadata={
                'word_count': len(content),
                'theorems': theorems,
                'definitions': definitions,
                **metadata
            }
        )
    
    def _path_to_id(self, rel_path: Path) -> str:
        """将路径转换为ID"""
        return str(rel_path).replace('\\', '_').replace('/', '_').replace('.md', '')
    
    def _extract_title(self, content: str, file_path: Path) -> str:
        """提取文档标题"""
        # 查找一级标题
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            title = match.group(1).strip()
            # 移除括号内容
            title = re.sub(r'\s*\([^)]*\)$', '', title)
            return title
        return file_path.stem
    
    def _determine_category(self, rel_path: Path) -> str:
        """确定文档类别"""
        path_str = str(rel_path).lower()
        if path_str.startswith('struct'):
            return 'Struct'
        elif path_str.startswith('knowledge'):
            return 'Knowledge'
        elif path_str.startswith('flink'):
            return 'Flink'
        return 'Root'
    
    def _extract_metadata(self, content: str) -> Dict[str, str]:
        """提取文档元数据"""
        metadata = {}
        
        # 查找元数据块
        meta_block = re.search(r'^>\s*所属阶段:[^\n]+(\n>\s*[^\n]+)*', content, re.MULTILINE)
        if meta_block:
            block_content = meta_block.group(0)
            for match in re.finditer(r'>\s*\*\*([^:]+)\*\*[:：]\s*([^|\n]+)', block_content):
                key = match.group(1).strip()
                value = match.group(2).strip()
                metadata[key] = value
        
        return metadata
    
    def _extract_dependencies(self, content: str, rel_path: Path) -> List[str]:
        """提取文档依赖"""
        dependencies = []
        
        # 查找前置依赖
        for match in self.DEPENDENCY_PATTERN.finditer(content):
            dep_text = match.group(1).strip()
            dep_path = match.group(2) if match.group(2) else dep_text
            
            if dep_path and dep_path != '无':
                resolved = self._resolve_path(dep_path, rel_path)
                if resolved:
                    dependencies.append(resolved)
        
        # 查找关联文档部分
        related_section = re.search(
            r'##\s+(?:关联文档|Related Documents|前置知识|Prerequisites)[^#]*',
            content,
            re.IGNORECASE | re.DOTALL
        )
        if related_section:
            section_content = related_section.group(0)
            for match in self.LINK_PATTERN.finditer(section_content):
                link_path = match.group(2)
                resolved = self._resolve_path(link_path, rel_path)
                if resolved and resolved not in dependencies:
                    dependencies.append(resolved)
        
        return dependencies
    
    def _extract_references(self, content: str, rel_path: Path) -> List[str]:
        """提取文档引用"""
        references = []
        
        for match in self.LINK_PATTERN.finditer(content):
            link_path = match.group(2)
            resolved = self._resolve_path(link_path, rel_path)
            if resolved and resolved not in references:
                references.append(resolved)
        
        return references
    
    def _resolve_path(self, link_path: str, current_path: Path) -> Optional[str]:
        """解析链接路径为文档ID"""
        # 清理路径
        clean_path = link_path.replace('../', '').replace('./', '')
        clean_path = clean_path.replace('\\', '/')
        
        # 移除锚点
        clean_path = clean_path.split('#')[0]
        
        if clean_path.endswith('.md'):
            return clean_path.replace('/', '_').replace('.md', '')
        
        return None


class DependencyAnalyzer:
    """依赖分析器"""
    
    def __init__(self, documents: Dict[str, DocumentNode]):
        self.documents = documents
        self.adjacency_list: Dict[str, Set[str]] = defaultdict(set)
        self.reverse_adjacency: Dict[str, Set[str]] = defaultdict(set)
        self.build_graph()
    
    def build_graph(self):
        """构建依赖图"""
        for doc_id, doc in self.documents.items():
            for dep in doc.dependencies:
                if dep in self.documents:
                    self.adjacency_list[doc_id].add(dep)
                    self.reverse_adjacency[dep].add(doc_id)
            
            for ref in doc.references:
                if ref in self.documents and ref not in doc.dependencies:
                    self.adjacency_list[doc_id].add(ref)
                    self.reverse_adjacency[ref].add(doc_id)
    
    def detect_cycles(self) -> List[CycleInfo]:
        """检测循环依赖"""
        print("🔄 检测循环依赖...")
        
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(node: str, path: List[str]):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in self.adjacency_list[node]:
                if neighbor not in visited:
                    dfs(neighbor, path)
                elif neighbor in rec_stack:
                    # 发现循环
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    cycles.append(cycle)
            
            path.pop()
            rec_stack.remove(node)
        
        for node in self.documents:
            if node not in visited:
                dfs(node, [])
        
        # 去重并创建CycleInfo对象
        unique_cycles = []
        seen = set()
        
        for cycle in cycles:
            cycle_tuple = tuple(sorted(cycle))
            if cycle_tuple not in seen:
                seen.add(cycle_tuple)
                
                # 确定严重程度
                severity = self._determine_cycle_severity(cycle)
                
                unique_cycles.append(CycleInfo(
                    nodes=cycle[:-1],  # 移除重复的末尾节点
                    length=len(cycle) - 1,
                    severity=severity,
                    description=self._describe_cycle(cycle)
                ))
        
        print(f"  发现 {len(unique_cycles)} 个循环依赖\n")
        return unique_cycles
    
    def _determine_cycle_severity(self, cycle: List[str]) -> str:
        """确定循环依赖的严重程度"""
        length = len(cycle) - 1
        
        if length <= 2:
            return 'high'
        elif length <= 4:
            return 'medium'
        else:
            return 'low'
    
    def _describe_cycle(self, cycle: List[str]) -> str:
        """描述循环依赖"""
        nodes = cycle[:-1]  # 移除重复的末尾节点
        descriptions = []
        
        for node_id in nodes:
            doc = self.documents.get(node_id)
            if doc:
                descriptions.append(f"{doc.title} ({node_id})")
            else:
                descriptions.append(node_id)
        
        return ' → '.join(descriptions) + ' → (回到起点)'
    
    def calculate_centrality(self) -> Dict[str, float]:
        """计算节点中心性（PageRank简化版）"""
        print("📊 计算节点中心性...")
        
        damping = 0.85
        iterations = 20
        scores = {node: 1.0 / len(self.documents) for node in self.documents}
        
        for _ in range(iterations):
            new_scores = {}
            
            for node in self.documents:
                score = (1 - damping) / len(self.documents)
                
                # 从引用该节点的其他节点获得分数
                for ref in self.reverse_adjacency[node]:
                    out_degree = len(self.adjacency_list[ref])
                    if out_degree > 0:
                        score += damping * scores[ref] / out_degree
                
                new_scores[node] = score
            
            scores = new_scores
        
        # 归一化
        max_score = max(scores.values())
        if max_score > 0:
            scores = {k: v / max_score for k, v in scores.items()}
        
        print(f"  完成 {len(scores)} 个节点的中心性计算\n")
        return scores
    
    def find_entry_points(self) -> List[str]:
        """查找入口点（无依赖的文档）"""
        entry_points = []
        
        for doc_id, doc in self.documents.items():
            if not doc.dependencies:
                entry_points.append(doc_id)
        
        return entry_points
    
    def find_isolated_nodes(self) -> List[str]:
        """查找孤立节点（无依赖且未被引用）"""
        isolated = []
        
        for doc_id in self.documents:
            in_degree = len(self.reverse_adjacency[doc_id])
            out_degree = len(self.adjacency_list[doc_id])
            
            if in_degree == 0 and out_degree == 0:
                isolated.append(doc_id)
        
        return isolated
    
    def calculate_depth(self) -> Dict[str, int]:
        """计算每个节点的依赖深度"""
        depths = {}
        
        def get_depth(node_id: str, visited: Set[str]) -> int:
            if node_id in depths:
                return depths[node_id]
            
            if node_id in visited:
                return 0  # 循环依赖
            
            visited.add(node_id)
            
            deps = self.adjacency_list[node_id]
            if not deps:
                depths[node_id] = 0
            else:
                max_dep_depth = max(
                    get_depth(dep, visited.copy())
                    for dep in deps
                )
                depths[node_id] = max_dep_depth + 1
            
            return depths[node_id]
        
        for node_id in self.documents:
            get_depth(node_id, set())
        
        return depths


class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, documents: Dict[str, DocumentNode], 
                 analyzer: DependencyAnalyzer,
                 output_dir: str):
        self.documents = documents
        self.analyzer = analyzer
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_all_reports(self):
        """生成所有报告"""
        print("📄 生成报告...\n")
        
        self.generate_json_report()
        self.generate_markdown_report()
        self.generate_dot_graph()
        self.generate_statistics()
        
        print(f"✅ 报告已保存到: {self.output_dir}\n")
    
    def generate_json_report(self):
        """生成JSON格式报告"""
        cycles = self.analyzer.detect_cycles()
        centrality = self.analyzer.calculate_centrality()
        entry_points = self.analyzer.find_entry_points()
        isolated = self.analyzer.find_isolated_nodes()
        depths = self.analyzer.calculate_depth()
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_documents': len(self.documents),
                'total_relationships': sum(
                    len(doc.dependencies) + len(doc.references)
                    for doc in self.documents.values()
                ),
                'cycles_detected': len(cycles),
                'entry_points': len(entry_points),
                'isolated_documents': len(isolated)
            },
            'cycles': [
                {
                    'nodes': cycle.nodes,
                    'length': cycle.length,
                    'severity': cycle.severity,
                    'description': cycle.description
                }
                for cycle in cycles
            ],
            'centrality': {
                k: round(v, 4) for k, v in sorted(
                    centrality.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:20]
            },
            'entry_points': entry_points,
            'isolated_nodes': isolated,
            'depth_distribution': self._calculate_depth_distribution(depths),
            'documents': {
                doc_id: {
                    'title': doc.title,
                    'path': doc.path,
                    'category': doc.category,
                    'dependencies': doc.dependencies,
                    'references': doc.references,
                    'centrality': round(centrality.get(doc_id, 0), 4),
                    'depth': depths.get(doc_id, 0)
                }
                for doc_id, doc in self.documents.items()
            }
        }
        
        output_path = self.output_dir / 'doc-relationship-report.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"  ✓ JSON报告: {output_path}")
    
    def generate_markdown_report(self):
        """生成Markdown格式报告"""
        cycles = self.analyzer.detect_cycles()
        entry_points = self.analyzer.find_entry_points()
        isolated = self.analyzer.find_isolated_nodes()
        centrality = self.analyzer.calculate_centrality()
        
        md = f"""# 📊 AnalysisDataFlow 文档关系映射报告

> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📈 概览统计

| 指标 | 数值 |
|------|------|
| 文档总数 | {len(self.documents)} |
| 循环依赖数 | {len(cycles)} |
| 入口点数量 | {len(entry_points)} |
| 孤立文档数 | {len(isolated)} |

## 🔄 循环依赖

"""
        
        if cycles:
            md += f"共发现 **{len(cycles)}** 个循环依赖:\n\n"
            
            for i, cycle in enumerate(cycles, 1):
                severity_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(cycle.severity, '⚪')
                md += f"### {severity_emoji} 循环 #{i}\n\n"
                md += f"- **严重程度**: {cycle.severity.upper()}\n"
                md += f"- **涉及节点**: {cycle.length} 个\n"
                md += f"- **路径**: {cycle.description}\n\n"
        else:
            md += "✅ 未发现循环依赖\n\n"
        
        md += "## 🚪 入口点\n\n"
        md += "以下文档无前置依赖，可作为学习起点:\n\n"
        for ep in entry_points[:10]:
            doc = self.documents.get(ep)
            if doc:
                md += f"- **{doc.title}** (`{doc.path}`)\n"
        
        if len(entry_points) > 10:
            md += f"\n... 还有 {len(entry_points) - 10} 个入口点\n"
        
        md += "\n## 🏝️ 孤立文档\n\n"
        if isolated:
            md += f"发现 **{len(isolated)}** 个孤立文档（建议检查是否需要建立关联）:\n\n"
            for iso in isolated[:10]:
                doc = self.documents.get(iso)
                if doc:
                    md += f"- `{doc.path}`\n"
        else:
            md += "✅ 未发现孤立文档\n"
        
        md += "\n## 🌟 核心文档\n\n"
        md += "按中心性排序的前20个文档:\n\n"
        md += "| 排名 | 文档 | 类别 | 中心性得分 |\n"
        md += "|------|------|------|------------|\n"
        
        sorted_cent = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:20]
        for rank, (doc_id, score) in enumerate(sorted_cent, 1):
            doc = self.documents.get(doc_id)
            if doc:
                md += f"| {rank} | {doc.title} | {doc.category} | {score:.4f} |\n"
        
        md += """

## 📋 术语说明

- **入口点**: 无前置依赖的文档，适合作为学习起点
- **孤立文档**: 既无依赖也未被引用的文档
- **中心性**: 基于PageRank算法计算的文档重要性
- **循环依赖**: 文档A依赖B，B又直接或间接依赖A的情况

---

*此报告由文档关系自动映射脚本生成*
"""
        
        output_path = self.output_dir / 'doc-relationship-report.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md)
        
        print(f"  ✓ Markdown报告: {output_path}")
    
    def generate_dot_graph(self):
        """生成Graphviz DOT格式图"""
        lines = [
            'digraph DocumentGraph {',
            '  rankdir=TB;',
            '  node [shape=box, style="rounded,filled", fontname="Microsoft YaHei"];',
            '  edge [fontname="Microsoft YaHei", fontsize=10];',
            ''
        ]
        
        # 颜色映射
        colors = {
            'Struct': '#e3f2fd',
            'Knowledge': '#e8f5e9',
            'Flink': '#fff3e0'
        }
        
        border_colors = {
            'Struct': '#1976d2',
            'Knowledge': '#388e3c',
            'Flink': '#f57c00'
        }
        
        # 按类别分组
        by_category = defaultdict(list)
        for doc_id, doc in self.documents.items():
            by_category[doc.category].append(doc)
        
        # 添加子图
        for category, docs in by_category.items():
            lines.append(f'  subgraph cluster_{category} {{')
            lines.append(f'    label="{category}";')
            lines.append(f'    style=filled;')
            lines.append(f'    color="{colors.get(category, '#eeeeee')}";')
            lines.append(f'    fontname="Microsoft YaHei";')
            
            for doc in docs:
                label = doc.title.replace('"', '\\"')
                lines.append(
                    f'    "{doc.id}" [label="{label}", '
                    f'fillcolor="{colors.get(category, '#ffffff')}", '
                    f'color="{border_colors.get(category, '#666666')}"];'
                )
            
            lines.append('  }')
            lines.append('')
        
        # 添加边
        added_edges = set()
        for doc_id, doc in self.documents.items():
            for dep in doc.dependencies:
                if dep in self.documents:
                    edge_key = (doc_id, dep)
                    if edge_key not in added_edges:
                        added_edges.add(edge_key)
                        lines.append(
                            f'  "{doc_id}" -> "{dep}" '
                            f'[color="#f57c00", style=dashed, label="依赖"];'
                        )
            
            for ref in doc.references:
                if ref in self.documents and ref not in doc.dependencies:
                    edge_key = (doc_id, ref)
                    if edge_key not in added_edges:
                        added_edges.add(edge_key)
                        lines.append(
                            f'  "{doc_id}" -> "{ref}" '
                            f'[color="#4caf50", label="引用"];'
                        )
        
        lines.append('}')
        
        output_path = self.output_dir / 'doc-relationship-graph.dot'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"  ✓ DOT图: {output_path}")
    
    def generate_statistics(self):
        """生成统计信息"""
        # 按类别统计
        by_category = defaultdict(int)
        for doc in self.documents.values():
            by_category[doc.category] += 1
        
        # 按依赖数量统计
        dep_counts = defaultdict(int)
        for doc in self.documents.values():
            dep_counts[len(doc.dependencies)] += 1
        
        stats = {
            'by_category': dict(by_category),
            'dependency_distribution': dict(dep_counts),
            'generated_at': datetime.now().isoformat()
        }
        
        output_path = self.output_dir / 'doc-statistics.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        print(f"  ✓ 统计数据: {output_path}")
    
    def _calculate_depth_distribution(self, depths: Dict[str, int]) -> Dict[str, int]:
        """计算深度分布"""
        distribution = defaultdict(int)
        for depth in depths.values():
            distribution[str(depth)] += 1
        return dict(distribution)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='AnalysisDataFlow 文档关系自动映射脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本用法
  python doc-relationship-mapper.py
  
  # 指定输出目录
  python doc-relationship-mapper.py --output ./reports
  
  # 仅检测循环依赖
  python doc-relationship-mapper.py --cycles-only
        """
    )
    
    parser.add_argument(
        '--base-path', '-b',
        default='.',
        help='项目根目录 (默认: 当前目录)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='./reports',
        help='输出目录 (默认: ./reports)'
    )
    
    parser.add_argument(
        '--cycles-only',
        action='store_true',
        help='仅检测循环依赖'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("  AnalysisDataFlow 文档关系自动映射")
    print("=" * 60)
    print()
    
    # 解析文档
    parser_obj = DocumentParser(args.base_path)
    documents = parser_obj.scan_documents()
    
    if not documents:
        print("❌ 未找到任何文档，请检查目录结构")
        return
    
    # 分析依赖
    analyzer = DependencyAnalyzer(documents)
    
    # 仅检测循环依赖
    if args.cycles_only:
        cycles = analyzer.detect_cycles()
        if cycles:
            print("\n发现的循环依赖:\n")
            for cycle in cycles:
                print(f"  [{cycle.severity.upper()}] {cycle.description}")
        else:
            print("\n✅ 未发现循环依赖")
        return
    
    # 生成报告
    reporter = ReportGenerator(documents, analyzer, args.output)
    reporter.generate_all_reports()
    
    print("=" * 60)
    print("  文档关系映射完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
