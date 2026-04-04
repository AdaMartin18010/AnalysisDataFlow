#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AnalysisDataFlow 概念依赖图自动生成器 (P2-13)

功能：
1. 提取定理/定义之间的依赖关系
2. 生成依赖图数据
3. 输出为 Mermaid 或 D3 格式
4. 识别依赖链和层次结构

输出：
- KNOWLEDGE-GRAPH/concept-dependencies.json - 概念依赖数据
- KNOWLEDGE-GRAPH/dependency-graph-mermaid.md - Mermaid格式
- KNOWLEDGE-GRAPH/dependency-graph-d3.json - D3格式
- KNOWLEDGE-GRAPH/theorem-hierarchy.md - 定理层次结构

作者: Agent
版本: 1.0.0
日期: 2026-04-04
"""

import os
import re
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
import argparse
from datetime import datetime


@dataclass
class FormalElement:
    """形式化元素（定理、定义等）"""
    id: str
    name: str
    type: str  # theorem, definition, lemma, proposition, corollary
    document: str
    document_path: str
    description: str = ""
    depends_on: List[str] = field(default_factory=list)
    used_by: List[str] = field(default_factory=list)
    level: int = 0  # 依赖层级


@dataclass
class DependencyEdge:
    """依赖边"""
    source: str
    target: str
    type: str  # proves, uses, extends, implements


class FormalElementExtractor:
    """形式化元素提取器"""
    
    # 形式化元素ID模式
    FORMAL_ID_PATTERNS = {
        'theorem': re.compile(r'Thm-([SKF])-(\d+)-(\d+)', re.IGNORECASE),
        'definition': re.compile(r'Def-([SKF])-(\d+)-(\d+)', re.IGNORECASE),
        'lemma': re.compile(r'Lemma-([SKF])-(\d+)-(\d+)', re.IGNORECASE),
        'proposition': re.compile(r'Prop-([SKF])-(\d+)-(\d+)', re.IGNORECASE),
        'corollary': re.compile(r'Cor-([SKF])-(\d+)-(\d+)', re.IGNORECASE),
    }
    
    # 依赖模式
    DEPENDENCY_PATTERNS = [
        re.compile(r'依赖于\s*\*\*(Thm|Def|Lemma|Prop|Cor)-[^*]+\*\*', re.IGNORECASE),
        re.compile(r'由\s*\*\*(Thm|Def|Lemma|Prop|Cor)-[^*]+\*\*\s*可得', re.IGNORECASE),
        re.compile(r'根据\s*\*\*(Thm|Def|Lemma|Prop|Cor)-[^*]+\*\*', re.IGNORECASE),
        re.compile(r'由\s*\([^)]*\)\s*和\s*\([^)]*\)', re.IGNORECASE),
    ]
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.elements: Dict[str, FormalElement] = {}
        self.edges: List[DependencyEdge] = []
        
    def extract_all_elements(self) -> Tuple[List[FormalElement], List[DependencyEdge]]:
        """提取所有形式化元素"""
        print("🔍 开始提取形式化元素...")
        
        directories = ['Struct', 'Knowledge', 'Flink']
        
        for directory in directories:
            dir_path = self.base_path / directory
            if not dir_path.exists():
                continue
            
            print(f"  📁 扫描 {directory}/")
            for md_file in dir_path.rglob('*.md'):
                self._parse_document(md_file)
        
        # 构建依赖关系
        self._build_dependencies()
        
        # 计算层级
        self._calculate_levels()
        
        print(f"\n✅ 提取完成: {len(self.elements)} 个形式化元素, {len(self.edges)} 个依赖")
        
        return list(self.elements.values()), self.edges
    
    def _parse_document(self, file_path: Path):
        """解析文档中的形式化元素"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return
        
        rel_path = file_path.relative_to(self.base_path)
        doc_id = str(rel_path).replace('\\', '/').replace('/', '_').replace('.md', '')
        
        # 提取各种形式化元素
        for elem_type, pattern in self.FORMAL_ID_PATTERNS.items():
            for match in pattern.finditer(content):
                elem_id = match.group(0)
                
                # 提取描述（前后文）
                start = max(0, match.start() - 200)
                end = min(len(content), match.end() + 200)
                context = content[start:end]
                
                # 提取名称（如果在附近）
                name = self._extract_name(content, match.end())
                
                if elem_id not in self.elements:
                    self.elements[elem_id] = FormalElement(
                        id=elem_id,
                        name=name or elem_id,
                        type=elem_type,
                        document=doc_id,
                        document_path=str(rel_path).replace('\\', '/'),
                        description=context[:150] + '...' if len(context) > 150 else context
                    )
    
    def _extract_name(self, content: str, pos: int) -> Optional[str]:
        """提取元素名称"""
        # 查找后面的括号或粗体内容
        after = content[pos:pos+100]
        
        # 匹配 (**名称**)
        name_match = re.search(r'\(\*\*([^*]+)\*\*\)', after)
        if name_match:
            return name_match.group(1)
        
        # 匹配 (名称)
        name_match = re.search(r'\(([^(]+)\)', after)
        if name_match:
            return name_match.group(1)
        
        return None
    
    def _build_dependencies(self):
        """构建元素间依赖关系"""
        print("  🔗 构建依赖关系...")
        
        # 分析每个元素的依赖
        for elem_id, elem in self.elements.items():
            # 在描述中查找对其他元素的引用
            for other_id, other_elem in self.elements.items():
                if other_id != elem_id and other_id in elem.description:
                    elem.depends_on.append(other_id)
                    other_elem.used_by.append(elem_id)
                    
                    edge_type = self._determine_edge_type(elem.type, other_elem.type)
                    self.edges.append(DependencyEdge(
                        source=elem_id,
                        target=other_id,
                        type=edge_type
                    ))
    
    def _determine_edge_type(self, source_type: str, target_type: str) -> str:
        """确定边的类型"""
        if source_type == 'theorem' and target_type == 'definition':
            return 'proves'
        elif source_type == 'lemma' and target_type == 'theorem':
            return 'supports'
        elif source_type == 'corollary' and target_type == 'theorem':
            return 'extends'
        elif source_type == 'proposition':
            return 'uses'
        else:
            return 'depends_on'
    
    def _calculate_levels(self):
        """计算元素的依赖层级"""
        # 拓扑排序计算层级
        in_degree = defaultdict(int)
        
        for edge in self.edges:
            in_degree[edge.source] += 1
        
        # BFS
        queue = []
        for elem_id in self.elements:
            if in_degree[elem_id] == 0:
                queue.append(elem_id)
                self.elements[elem_id].level = 0
        
        while queue:
            current = queue.pop(0)
            current_level = self.elements[current].level
            
            for edge in self.edges:
                if edge.target == current:
                    source = edge.source
                    new_level = current_level + 1
                    if new_level > self.elements[source].level:
                        self.elements[source].level = new_level
                    queue.append(source)


class MermaidExporter:
    """Mermaid格式导出器"""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_full_graph(self, elements: List[FormalElement], edges: List[DependencyEdge]):
        """导出完整依赖图"""
        lines = ['```mermaid', 'graph TB']
        
        # 按类别分组
        categories = defaultdict(list)
        for elem in elements:
            cat = elem.id.split('-')[1] if '-' in elem.id else 'Other'
            categories[cat].append(elem)
        
        # 生成节点定义
        for category, elems in categories.items():
            lines.append(f'    subgraph {category}')
            for elem in elems:
                node_def = f'        {elem.id}[{elem.name}]'
                lines.append(node_def)
            lines.append('    end')
        
        lines.append('')
        
        # 生成边
        for edge in edges:
            lines.append(f'    {edge.target} --> {edge.source}')
        
        lines.append('```')
        
        output_path = self.output_dir / 'dependency-graph-mermaid.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"  ✓ 导出 Mermaid 格式: {output_path}")
        return output_path
    
    def export_by_category(self, elements: List[FormalElement], edges: List[DependencyEdge]):
        """按类别导出依赖图"""
        output_files = []
        
        categories = defaultdict(list)
        for elem in elements:
            cat = elem.id.split('-')[1] if '-' in elem.id else 'Other'
            categories[cat].append(elem)
        
        for category, elems in categories.items():
            lines = ['```mermaid', 'graph TB']
            
            elem_ids = {e.id for e in elems}
            
            # 节点
            for elem in elems:
                lines.append(f'    {elem.id}[{elem.name}]')
            
            # 内部边
            for edge in edges:
                if edge.source in elem_ids and edge.target in elem_ids:
                    lines.append(f'    {edge.target} --> {edge.source}')
            
            lines.append('```')
            
            output_path = self.output_dir / f'dependency-graph-{category.lower()}.md'
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            
            output_files.append(output_path)
            print(f"  ✓ 导出 {category} 依赖图: {output_path}")
        
        return output_files
    
    def export_theorem_hierarchy(self, elements: List[FormalElement], edges: List[DependencyEdge]):
        """导出定理层次结构"""
        lines = ['# 定理/定义层次结构', '']
        lines.append(f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # 按层级分组
        levels = defaultdict(list)
        for elem in elements:
            levels[elem.level].append(elem)
        
        # 生成层次图
        lines.append("## 依赖层次图")
        lines.append("")
        lines.append("```mermaid")
        lines.append("graph TB")
        
        for level in sorted(levels.keys()):
            elems = levels[level]
            lines.append(f'    subgraph Level{level}[层级 {level}]')
            for elem in elems:
                lines.append(f'        {elem.id}[{elem.name}]')
            lines.append('    end')
        
        lines.append('')
        
        # 添加跨层级边
        for edge in edges:
            lines.append(f'    {edge.target} --> {edge.source}')
        
        lines.append('```')
        lines.append('')
        
        # 详细列表
        lines.append("## 按层级详细列表")
        lines.append('')
        
        for level in sorted(levels.keys()):
            lines.append(f"### 层级 {level}")
            lines.append('')
            
            for elem in levels[level]:
                lines.append(f"- **{elem.id}**: {elem.name}")
                lines.append(f"  - 文档: `{elem.document_path}`")
                if elem.depends_on:
                    lines.append(f"  - 依赖于: {', '.join(elem.depends_on[:3])}")
                lines.append('')
        
        output_path = self.output_dir / 'theorem-hierarchy.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"  ✓ 导出定理层次结构: {output_path}")
        return output_path


class D3Exporter:
    """D3格式导出器"""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_d3_json(self, elements: List[FormalElement], edges: List[DependencyEdge]):
        """导出D3可用的JSON格式"""
        # 颜色映射
        color_map = {
            'theorem': '#D9534F',
            'definition': '#9B59B6',
            'lemma': '#17A2B8',
            'proposition': '#E83E8C',
            'corollary': '#6C757D'
        }
        
        nodes = []
        for elem in elements:
            cat = elem.id.split('-')[1] if '-' in elem.id else 'Other'
            nodes.append({
                'id': elem.id,
                'name': elem.name,
                'type': elem.type,
                'category': cat,
                'level': elem.level,
                'document': elem.document_path,
                'description': elem.description,
                'color': color_map.get(elem.type, '#999'),
                'size': 10 + elem.level * 3
            })
        
        links = []
        for edge in edges:
            links.append({
                'source': edge.source,
                'target': edge.target,
                'type': edge.type
            })
        
        data = {
            'nodes': nodes,
            'links': links,
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_elements': len(nodes),
                'total_dependencies': len(links)
            }
        }
        
        output_path = self.output_dir / 'dependency-graph-d3.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"  ✓ 导出 D3 格式: {output_path}")
        return output_path


class DependencyAnalyzer:
    """依赖关系分析器"""
    
    def analyze(self, elements: List[FormalElement], edges: List[DependencyEdge]) -> Dict:
        """分析依赖关系"""
        analysis = {
            'total_elements': len(elements),
            'total_dependencies': len(edges),
            'by_type': defaultdict(int),
            'by_category': defaultdict(int),
            'max_level': 0,
            'most_depended': [],
            'longest_chains': []
        }
        
        # 按类型统计
        for elem in elements:
            analysis['by_type'][elem.type] += 1
            cat = elem.id.split('-')[1] if '-' in elem.id else 'Other'
            analysis['by_category'][cat] += 1
            analysis['max_level'] = max(analysis['max_level'], elem.level)
        
        # 找出被依赖最多的元素
        used_count = defaultdict(int)
        for edge in edges:
            used_count[edge.target] += 1
        
        most_depended = sorted(used_count.items(), key=lambda x: x[1], reverse=True)[:10]
        analysis['most_depended'] = [
            {'id': elem_id, 'count': count}
            for elem_id, count in most_depended
        ]
        
        return analysis


def generate_analysis_report(analysis: Dict, output_dir: Path):
    """生成分析报告"""
    report_path = output_dir / 'CONCEPT-DEPENDENCY-ANALYSIS.md'
    
    report = f"""# 概念依赖图分析报告

> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 概览统计

| 指标 | 数值 |
|------|------|
| 形式化元素总数 | {analysis['total_elements']} |
| 依赖关系总数 | {analysis['total_dependencies']} |
| 最大依赖层级 | {analysis['max_level']} |

### 按类型分布

| 类型 | 数量 |
|------|------|
"""
    
    for elem_type, count in sorted(analysis['by_type'].items()):
        report += f"| {elem_type.capitalize()} | {count} |\n"
    
    report += """
### 按类别分布

| 类别 | 数量 |
|------|------|
"""
    
    for cat, count in sorted(analysis['by_category'].items()):
        report += f"| {cat} | {count} |\n"
    
    report += """
---

## 🔗 核心概念

被依赖最多的概念（核心基础）：

| 概念ID | 被依赖次数 |
|--------|-----------|
"""
    
    for item in analysis['most_depended']:
        report += f"| {item['id']} | {item['count']} |\n"
    
    report += """
---

## 📁 输出文件

| 文件 | 描述 |
|------|------|
| `concept-dependencies.json` | 完整概念依赖数据 |
| `dependency-graph-mermaid.md` | Mermaid格式依赖图 |
| `dependency-graph-d3.json` | D3.js可用数据 |
| `theorem-hierarchy.md` | 定理层次结构文档 |

---

*本报告由概念依赖图生成器自动生成*
"""
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"  ✓ 生成分析报告: {report_path}")
    return report_path


def main():
    parser = argparse.ArgumentParser(description='AnalysisDataFlow 概念依赖图生成器')
    parser.add_argument('-b', '--base-path', default='.', help='项目根目录')
    parser.add_argument('-o', '--output', default='KNOWLEDGE-GRAPH', help='输出目录')
    parser.add_argument('--format', choices=['mermaid', 'd3', 'all'], default='all',
                       help='输出格式')
    args = parser.parse_args()
    
    print("=" * 60)
    print("🔗 AnalysisDataFlow 概念依赖图生成器 (P2-13)")
    print("=" * 60)
    
    # 提取形式化元素
    extractor = FormalElementExtractor(args.base_path)
    elements, edges = extractor.extract_all_elements()
    
    # 分析依赖
    print("\n📊 分析依赖关系...")
    analyzer = DependencyAnalyzer()
    analysis = analyzer.analyze(elements, edges)
    
    print(f"  形式化元素: {analysis['total_elements']}")
    print(f"  依赖关系: {analysis['total_dependencies']}")
    print(f"  最大层级: {analysis['max_level']}")
    
    # 导出结果
    print("\n📤 导出结果...")
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 导出JSON
    json_path = output_dir / 'concept-dependencies.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            'elements': [asdict(e) for e in elements],
            'edges': [asdict(e) for e in edges],
            'analysis': analysis,
            'generated_at': datetime.now().isoformat()
        }, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 导出 JSON: {json_path}")
    
    # 导出Mermaid
    if args.format in ['mermaid', 'all']:
        mermaid_exporter = MermaidExporter(args.output)
        mermaid_exporter.export_full_graph(elements, edges)
        mermaid_exporter.export_by_category(elements, edges)
        mermaid_exporter.export_theorem_hierarchy(elements, edges)
    
    # 导出D3
    if args.format in ['d3', 'all']:
        d3_exporter = D3Exporter(args.output)
        d3_exporter.export_d3_json(elements, edges)
    
    # 生成报告
    print("\n📝 生成分析报告...")
    generate_analysis_report(analysis, output_dir)
    
    print("\n" + "=" * 60)
    print("✅ 概念依赖图生成完成!")
    print(f"📁 输出目录: {output_dir.absolute()}")
    print("=" * 60)


if __name__ == '__main__':
    main()
