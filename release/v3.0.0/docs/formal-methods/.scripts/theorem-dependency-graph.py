#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定理依赖图生成器

功能：
1. 扫描所有 .md 文件，提取形式化元素（Def-*, Thm-*, Lemma-*, Prop-*, Cor-*）
2. 构建依赖图，识别循环依赖和孤立节点
3. 生成 Mermaid 图、JSON 数据和 Markdown 报告

用法：
    python theorem-dependency-graph.py [选项]

选项：
    --topic {lambda,types,concurrency,all}  按主题筛选 (默认: all)
    --limit N                               限制节点数量 (默认: 100)
    --output-dir DIR                        输出目录 (默认: ../../visuals)
    --input-dir DIR                         输入目录 (默认: ..)
    --help                                  显示帮助信息

作者: AI Assistant
日期: 2026-04-10
"""

import os
import re
import json
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional

# 形式化元素的正则表达式模式
FORMAL_ELEMENT_PATTERNS = {
    'Def': r'Def-[A-Za-z]+-\d+-\d+',
    'Thm': r'Thm-[A-Za-z]+-\d+-\d+',
    'Lemma': r'Lemma-[A-Za-z]+-\d+-\d+',
    'Prop': r'Prop-[A-Za-z]+-\d+-\d+',
    'Cor': r'Cor-[A-Za-z]+-\d+-\d+',
}

# 引用模式：识别文本中对其他形式化元素的引用
REFERENCE_PATTERNS = [
    # 直接引用: "由Lemma A-04-01"、"根据Def-F-05-01"
    rf'(?:由|根据|依据|引用|见|参见|如|例如)\s*(Def|Thm|Lemma|Prop|Cor)[-\s]+([A-Za-z]+-\d+-\d+)',
    # 括号引用: "(Lemma A-04-01)"、"[Thm-S-01-01]"
    rf'[\(\[](Def|Thm|Lemma|Prop|Cor)[-\s]+([A-Za-z]+-\d+-\d+)[\)\]]',
    # 直接提及: "Lemma A-04-01 表明"
    rf'(Def|Thm|Lemma|Prop|Cor)[-\s]+([A-Za-z]+-\d+-\d+)\s*(?:表明|说明|指出|给出|蕴含|推导|证明)',
    # 依赖声明: "依赖于 Def-F-05-01"
    rf'(?:依赖于|依赖|使用|利用|基于|通过)\s+(Def|Thm|Lemma|Prop|Cor)[-\s]+([A-Za-z]+-\d+-\d+)',
]

# 主题关键词映射
TOPIC_KEYWORDS = {
    'lambda': [
        'lambda', 'λ', '演算', 'calculus', '类型', 'type', '归约', 'reduction',
        'substitution', '替换', 'binder', '变量', 'variable'
    ],
    'types': [
        'type', '类型', 'typing', '类型系统', 'type system', 'polymorphism',
        '多态', 'inference', '推导', 'curry-howard', '类型安全', 'type safety'
    ],
    'concurrency': [
        'concurrent', '并发', 'process', '进程', 'pi-calculus', 'π演算',
        'ccs', 'csp', 'actor', 'bisimulation', '互模拟', 'deadlock', '死锁',
        'race', '竞态', 'synchronization', '同步'
    ],
}


class FormalElement:
    """形式化元素类"""
    
    def __init__(self, elem_type: str, category: str, doc_num: str, seq_num: str,
                 name: str = "", file_path: str = "", line_num: int = 0):
        self.elem_type = elem_type  # Def, Thm, Lemma, Prop, Cor
        self.category = category    # F, C, T, V, A, S, K 等
        self.doc_num = doc_num      # 文档序号
        self.seq_num = seq_num      # 顺序号
        self.name = name            # 元素名称/标题
        self.file_path = file_path  # 所在文件路径
        self.line_num = line_num    # 所在行号
        self.references: Set[str] = set()  # 引用的其他元素ID
        self.referenced_by: Set[str] = set()  # 被哪些元素引用
        self.topic: Optional[str] = None  # 所属主题
        
    @property
    def id(self) -> str:
        """完整ID"""
        return f"{self.elem_type}-{self.category}-{self.doc_num}-{self.seq_num}"
    
    @property
    def short_id(self) -> str:
        """短ID（用于显示）"""
        return f"{self.elem_type}-{self.category}-{self.doc_num}-{self.seq_num}"
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'id': self.id,
            'type': self.elem_type,
            'category': self.category,
            'doc_num': self.doc_num,
            'seq_num': self.seq_num,
            'name': self.name,
            'file_path': self.file_path,
            'line_num': self.line_num,
            'references': list(self.references),
            'referenced_by': list(self.referenced_by),
            'topic': self.topic,
        }
    
    def __repr__(self):
        return f"FormalElement({self.id}: {self.name[:30]})"


class DependencyGraph:
    """依赖图类"""
    
    def __init__(self):
        self.elements: Dict[str, FormalElement] = {}
        self.edges: List[Tuple[str, str]] = []  # (source, target)
        self.cycles: List[List[str]] = []
        self.isolated: Set[str] = set()
        
    def add_element(self, element: FormalElement):
        """添加元素"""
        self.elements[element.id] = element
        
    def add_edge(self, source: str, target: str):
        """添加边（source 依赖于 target）"""
        if source in self.elements and target in self.elements:
            self.edges.append((source, target))
            self.elements[source].references.add(target)
            self.elements[target].referenced_by.add(source)
    
    def detect_cycles(self) -> List[List[str]]:
        """检测循环依赖"""
        # 使用 DFS 检测环
        visited = set()
        rec_stack = set()
        cycles = []
        
        def dfs(node: str, path: List[str]):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            # 查找从当前节点引用的所有元素
            if node in self.elements:
                for ref in self.elements[node].references:
                    if ref not in visited:
                        dfs(ref, path.copy())
                    elif ref in rec_stack:
                        # 发现环
                        cycle_start = path.index(ref)
                        cycle = path[cycle_start:] + [ref]
                        cycles.append(cycle)
            
            rec_stack.remove(node)
        
        for node in self.elements:
            if node not in visited:
                dfs(node, [])
        
        self.cycles = cycles
        return cycles
    
    def find_isolated(self) -> Set[str]:
        """找出孤立节点（无引用也无被引用）"""
        isolated = set()
        for elem_id, elem in self.elements.items():
            if not elem.references and not elem.referenced_by:
                isolated.add(elem_id)
        self.isolated = isolated
        return isolated
    
    def get_dependency_depth(self, elem_id: str, memo: Dict[str, int] = None, 
                             visited: Set[str] = None) -> int:
        """计算元素的依赖深度（使用迭代避免递归深度问题）"""
        if memo is None:
            memo = {}
        if visited is None:
            visited = set()
        
        if elem_id in memo:
            return memo[elem_id]
        
        if elem_id in visited:
            # 检测到循环，返回当前深度
            return 0
        
        elem = self.elements.get(elem_id)
        if not elem or not elem.references:
            memo[elem_id] = 0
            return 0
        
        visited.add(elem_id)
        max_depth = 0
        
        for ref in elem.references:
            if ref in self.elements and ref not in visited:
                depth = self.get_dependency_depth(ref, memo, visited)
                max_depth = max(max_depth, depth + 1)
        
        visited.discard(elem_id)
        memo[elem_id] = max_depth
        return max_depth
    
    def get_critical_path(self, target: str, max_depth: int = 100) -> List[str]:
        """获取到目标的最长依赖路径（使用动态规划，限制深度避免循环）"""
        if target not in self.elements:
            return [target]
        
        # 使用BFS找到最长路径
        from collections import deque
        queue = deque([(target, [target], 0)])
        longest_path = [target]
        visited_global = set()
        
        while queue:
            node, path, depth = queue.popleft()
            
            if depth > max_depth:
                continue
                
            if node in visited_global:
                continue
            visited_global.add(node)
            
            elem = self.elements.get(node)
            if not elem or not elem.references:
                if len(path) > len(longest_path):
                    longest_path = path
                continue
            
            has_ref = False
            for ref in elem.references:
                if ref in self.elements and ref not in path:  # 避免循环
                    has_ref = True
                    new_path = path + [ref]
                    queue.append((ref, new_path, depth + 1))
            
            if not has_ref and len(path) > len(longest_path):
                longest_path = path
        
        # 反转路径使其从基础到目标
        return longest_path[::-1]
    
    def filter_by_topic(self, topic: str) -> 'DependencyGraph':
        """按主题筛选"""
        if topic == 'all' or topic not in TOPIC_KEYWORDS:
            return self
        
        keywords = TOPIC_KEYWORDS[topic]
        filtered = DependencyGraph()
        
        # 筛选符合条件的元素
        for elem_id, elem in self.elements.items():
            elem_text = f"{elem.name} {elem.file_path}".lower()
            if any(kw.lower() in elem_text for kw in keywords):
                elem.topic = topic
                filtered.add_element(elem)
        
        # 重建边
        for elem_id, elem in filtered.elements.items():
            for ref in self.elements[elem_id].references:
                if ref in filtered.elements:
                    filtered.add_edge(elem_id, ref)
        
        return filtered
    
    def limit_nodes(self, limit: int) -> 'DependencyGraph':
        """限制节点数量（保留引用最多的节点）"""
        if len(self.elements) <= limit:
            return self
        
        # 按被引用次数排序
        sorted_elems = sorted(
            self.elements.values(),
            key=lambda e: len(e.referenced_by),
            reverse=True
        )
        
        # 选择前 N 个节点
        selected = set(e.id for e in sorted_elems[:limit])
        
        # 创建新图
        limited = DependencyGraph()
        for elem_id in selected:
            limited.add_element(self.elements[elem_id])
        
        # 重建边（只保留选中节点之间的边）
        for elem_id in selected:
            elem = self.elements[elem_id]
            for ref in elem.references:
                if ref in selected:
                    limited.add_edge(elem_id, ref)
        
        return limited
    
    def to_mermaid(self, title: str = "定理依赖图") -> str:
        """生成 Mermaid 图"""
        lines = ["graph TB"]
        lines.append(f"    %% {title}")
        lines.append(f"    %% 生成时间: {datetime.now().isoformat()}")
        lines.append("")
        
        # 按类型分组
        type_groups = defaultdict(list)
        for elem_id, elem in self.elements.items():
            type_groups[elem.elem_type].append(elem)
        
        # 定义节点样式
        type_styles = {
            'Def': ('fill:#e1f5fe', '定义'),
            'Thm': ('fill:#fff3e0', '定理'),
            'Lemma': ('fill:#f3e5f5', '引理'),
            'Prop': ('fill:#e8f5e9', '命题'),
            'Cor': ('fill:#fce4ec', '推论'),
        }
        
        # 添加子图
        for elem_type in ['Def', 'Lemma', 'Prop', 'Thm', 'Cor']:
            if elem_type in type_groups:
                elems = type_groups[elem_type]
                type_name = type_styles.get(elem_type, ('', elem_type))[1]
                lines.append(f"    subgraph {elem_type}Group[{type_name}]")
                
                for elem in elems:
                    display_name = elem.name[:30] if elem.name else elem.id
                    lines.append(f'        {elem.id}["{elem.short_id}<br/>{display_name}"]')
                
                lines.append("    end")
                lines.append("")
        
        # 添加边
        lines.append("    %% 依赖关系")
        for source, target in self.edges:
            lines.append(f"    {target} --> {source}")
        
        lines.append("")
        
        # 添加样式
        lines.append("    %% 样式定义")
        for elem_type, (style, _) in type_styles.items():
            lines.append(f"    classDef {elem_type}Style {style},stroke:#333,stroke-width:1px")
        
        lines.append("")
        lines.append("    %% 应用样式")
        for elem_type in type_styles:
            if elem_type in type_groups:
                elem_ids = [e.id for e in type_groups[elem_type]]
                lines.append(f"    class {','.join(elem_ids[:10])} {elem_type}Style")
        
        return '\n'.join(lines)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_elements': len(self.elements),
                'total_edges': len(self.edges),
                'cycles_detected': len(self.cycles),
                'isolated_nodes': len(self.isolated),
            },
            'elements': {k: v.to_dict() for k, v in self.elements.items()},
            'edges': [{'source': s, 'target': t} for s, t in self.edges],
            'cycles': self.cycles,
            'isolated': list(self.isolated),
            'statistics': self._calculate_statistics(),
        }
    
    def _calculate_statistics(self) -> Dict:
        """计算统计信息"""
        if not self.elements:
            return {}
        
        type_counts = defaultdict(int)
        category_counts = defaultdict(int)
        depths = []
        
        for elem in self.elements.values():
            type_counts[elem.elem_type] += 1
            category_counts[elem.category] += 1
            depths.append(self.get_dependency_depth(elem.id))
        
        return {
            'by_type': dict(type_counts),
            'by_category': dict(category_counts),
            'avg_references': sum(len(e.references) for e in self.elements.values()) / len(self.elements),
            'max_depth': max(depths) if depths else 0,
            'avg_depth': sum(depths) / len(depths) if depths else 0,
            'most_referenced': sorted(
                [(e.id, len(e.referenced_by)) for e in self.elements.values()],
                key=lambda x: x[1],
                reverse=True
            )[:10],
        }


def scan_markdown_files(input_dir: str) -> List[Path]:
    """扫描所有 Markdown 文件"""
    input_path = Path(input_dir)
    md_files = []
    
    for pattern in ['**/*.md', '**/*.markdown']:
        md_files.extend(input_path.rglob(pattern))
    
    return md_files


def extract_formal_elements(file_path: Path, base_dir: Path = None) -> List[FormalElement]:
    """从文件中提取形式化元素"""
    elements = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception as e:
        print(f"警告: 无法读取文件 {file_path}: {e}")
        return elements
    
    # 计算相对路径
    if base_dir:
        try:
            rel_path = str(file_path.relative_to(base_dir))
        except ValueError:
            rel_path = str(file_path)
    else:
        rel_path = str(file_path)
    
    # 提取形式化元素定义
    for line_num, line in enumerate(lines, 1):
        for elem_type, pattern in FORMAL_ELEMENT_PATTERNS.items():
            matches = re.finditer(pattern, line)
            for match in matches:
                full_match = match.group(0)
                # 解析元素ID
                parts = full_match.split('-')
                if len(parts) >= 4:
                    category = parts[1]
                    doc_num = parts[2]
                    seq_num = parts[3]
                    
                    # 提取名称（通常是同一行或下一行的内容）
                    name = ""
                    if ':' in line:
                        name = line.split(':', 1)[1].strip()[:100]
                    elif line_num < len(lines):
                        next_line = lines[line_num].strip()
                        if next_line and not next_line.startswith('#'):
                            name = next_line[:100]
                    
                    element = FormalElement(
                        elem_type=elem_type,
                        category=category,
                        doc_num=doc_num,
                        seq_num=seq_num,
                        name=name,
                        file_path=rel_path,
                        line_num=line_num
                    )
                    elements.append(element)
    
    return elements


def extract_references(content: str, current_element: FormalElement) -> Set[str]:
    """从内容中提取对形式化元素的引用"""
    references = set()
    
    for pattern in REFERENCE_PATTERNS:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            elem_type = match.group(1)
            elem_id = match.group(2)
            full_id = f"{elem_type}-{elem_id}"
            if full_id != current_element.id:
                references.add(full_id)
    
    # 同时搜索所有形式化元素ID的直接出现
    for elem_type, pattern in FORMAL_ELEMENT_PATTERNS.items():
        matches = re.finditer(pattern, content)
        for match in matches:
            full_id = match.group(0)
            if full_id != current_element.id:
                references.add(full_id)
    
    return references


def build_dependency_graph(input_dir: str) -> DependencyGraph:
    """构建依赖图"""
    print(f"扫描目录: {input_dir}")
    
    md_files = scan_markdown_files(input_dir)
    print(f"找到 {len(md_files)} 个 Markdown 文件")
    
    graph = DependencyGraph()
    
    # 第一阶段：收集所有形式化元素
    print("第一阶段: 提取形式化元素...")
    file_elements = {}  # 文件 -> 元素列表
    
    input_path = Path(input_dir)
    for file_path in md_files:
        elements = extract_formal_elements(file_path, input_path)
        if elements:
            file_elements[file_path] = elements
            for elem in elements:
                graph.add_element(elem)
    
    print(f"提取到 {len(graph.elements)} 个形式化元素")
    
    # 第二阶段：提取引用关系
    print("第二阶段: 提取引用关系...")
    
    for file_path, elements in file_elements.items():
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            continue
        
        # 为每个元素提取引用
        for elem in elements:
            # 提取元素周围的上下文（前后1000字符）
            lines = content.split('\n')
            if elem.line_num <= len(lines):
                # 找到元素所在位置
                start_line = max(0, elem.line_num - 1)
                end_line = min(len(lines), elem.line_num + 50)
                context = '\n'.join(lines[start_line:end_line])
                
                references = extract_references(context, elem)
                for ref_id in references:
                    if ref_id in graph.elements:
                        graph.add_edge(elem.id, ref_id)
    
    print(f"构建了 {len(graph.edges)} 条依赖边")
    
    return graph


def generate_markdown_report(graph: DependencyGraph, output_path: Path, topic: str):
    """生成 Markdown 报告"""
    stats = graph._calculate_statistics()
    
    lines = [
        "# 定理依赖图分析报告",
        "",
        f"> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"> **分析主题**: {topic if topic != 'all' else '全部'}",
        f"> **统计范围**: {len(graph.elements)} 个形式化元素, {len(graph.edges)} 条依赖边",
        "",
        "## 1. 概述 (Overview)",
        "",
        "本报告分析了形式化方法文档中的定理依赖关系，包括定义、定理、引理、命题和推论之间的引用关系。",
        "",
        "## 2. 统计数据 (Statistics)",
        "",
        "### 2.1 元素类型分布",
        "",
        "| 类型 | 数量 | 占比 |",
        "|------|------|------|",
    ]
    
    total = len(graph.elements)
    for elem_type, count in sorted(stats.get('by_type', {}).items()):
        percentage = (count / total * 100) if total > 0 else 0
        type_names = {'Def': '定义', 'Thm': '定理', 'Lemma': '引理', 'Prop': '命题', 'Cor': '推论'}
        type_name = type_names.get(elem_type, elem_type)
        lines.append(f"| {type_name} ({elem_type}) | {count} | {percentage:.1f}% |")
    
    lines.extend([
        "",
        "### 2.2 依赖深度统计",
        "",
        f"- **最大依赖深度**: {stats.get('max_depth', 0)}",
        f"- **平均依赖深度**: {stats.get('avg_depth', 0):.2f}",
        f"- **平均引用数**: {stats.get('avg_references', 0):.2f}",
        "",
        "### 2.3 核心元素（被引用最多）",
        "",
        "| 排名 | 元素ID | 被引用次数 |",
        "|------|--------|-----------|",
    ])
    
    for i, (elem_id, count) in enumerate(stats.get('most_referenced', [])[:10], 1):
        lines.append(f"| {i} | `{elem_id}` | {count} |")
    
    # 循环依赖检测
    lines.extend([
        "",
        "## 3. 循环依赖检测 (Cycle Detection)",
        "",
    ])
    
    if graph.cycles:
        lines.append(f"检测到 **{len(graph.cycles)}** 个循环依赖：")
        lines.append("")
        for i, cycle in enumerate(graph.cycles[:10], 1):
            cycle_str = ' → '.join(cycle)
            lines.append(f"{i}. `{cycle_str}`")
        if len(graph.cycles) > 10:
            lines.append(f"\n... 还有 {len(graph.cycles) - 10} 个循环")
    else:
        lines.append("✅ **未检测到循环依赖**，依赖图是无环的（DAG）。")
    
    # 孤立节点
    lines.extend([
        "",
        "## 4. 孤立节点分析 (Isolated Nodes)",
        "",
    ])
    
    if graph.isolated:
        lines.append(f"发现 **{len(graph.isolated)}** 个孤立节点（无引用关系）：")
        lines.append("")
        lines.append("| 元素ID | 名称 | 文件 |")
        lines.append("|--------|------|------|")
        for elem_id in sorted(list(graph.isolated))[:20]:
            elem = graph.elements.get(elem_id)
            if elem:
                name = (elem.name[:30] + '...') if len(elem.name) > 30 else elem.name
                file_path = elem.file_path.split('/')[-1] if elem.file_path else 'N/A'
                lines.append(f"| `{elem_id}` | {name} | {file_path} |")
        if len(graph.isolated) > 20:
            lines.append(f"| ... | ... | ... |")
            lines.append(f"\n还有 {len(graph.isolated) - 20} 个孤立节点未显示")
    else:
        lines.append("✅ **所有节点都有引用关系**，无孤立节点。")
    
    # 关键路径
    lines.extend([
        "",
        "## 5. 关键证明路径 (Critical Paths)",
        "",
        "以下是依赖深度最长的几条证明路径：",
        "",
    ])
    
    # 找出依赖深度最大的元素
    max_depth_elems = sorted(
        graph.elements.values(),
        key=lambda e: graph.get_dependency_depth(e.id),
        reverse=True
    )[:5]
    
    for i, elem in enumerate(max_depth_elems, 1):
        path = graph.get_critical_path(elem.id)
        depth = len(path) - 1
        lines.append(f"### 5.{i} 路径 {i} (深度: {depth})")
        lines.append("")
        lines.append("```")
        for j, node_id in enumerate(path):
            node = graph.elements.get(node_id)
            indent = "  " * j
            name = f" ({node.name[:40]})" if node and node.name else ""
            lines.append(f"{indent}{node_id}{name}")
        lines.append("```")
        lines.append("")
    
    # 使用说明
    lines.extend([
        "## 6. 输出文件说明",
        "",
        "本分析生成了以下文件：",
        "",
        "| 文件 | 说明 |",
        "|------|------|",
        "| `theorem-dependency-graph.mmd` | Mermaid 依赖图（可在支持 Mermaid 的编辑器中查看） |",
        "| `theorem-dependency-data.json` | 完整的依赖数据（JSON格式） |",
        "| `theorem-dependency-report.md` | 本分析报告 |",
        "",
        "## 7. 附录 (Appendix)",
        "",
        "### 7.1 元素分类说明",
        "",
        "| 分类 | 含义 |",
        "|------|------|",
        "| F | Foundations (基础理论) |",
        "| C | Calculi (进程演算) |",
        "| T | Type Theory (类型论) |",
        "| V | Verification (验证方法) |",
        "| A | Application (应用层) |",
        "| S | Struct (结构文档) |",
        "| K | Knowledge (知识文档) |",
        "",
        "### 7.2 生成工具",
        "",
        "本报告由 `theorem-dependency-graph.py` 自动生成。",
        "",
        "---",
        "",
        "*报告生成时间: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "*",
    ])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"Markdown 报告已生成: {output_path}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='定理依赖图生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python theorem-dependency-graph.py
    python theorem-dependency-graph.py --topic lambda --limit 50
    python theorem-dependency-graph.py --input-dir ../docs --output-dir ./output
        """
    )
    
    parser.add_argument('--topic', type=str, default='all',
                        choices=['all', 'lambda', 'types', 'concurrency'],
                        help='按主题筛选 (默认: all)')
    parser.add_argument('--limit', type=int, default=100,
                        help='限制节点数量，保留引用最多的节点 (默认: 100)')
    parser.add_argument('--output-dir', type=str, default='../../visuals',
                        help='输出目录 (默认: ../../visuals)')
    parser.add_argument('--input-dir', type=str, default='..',
                        help='输入目录 (默认: ..)')
    parser.add_argument('--no-cycles-check', action='store_true',
                        help='跳过循环依赖检测（加快速度）')
    
    args = parser.parse_args()
    
    # 设置路径
    input_dir = os.path.abspath(args.input_dir)
    output_dir = os.path.abspath(args.output_dir)
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("定理依赖图生成器")
    print("=" * 60)
    print(f"输入目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    print(f"主题筛选: {args.topic}")
    print(f"节点限制: {args.limit}")
    print("=" * 60)
    
    # 构建依赖图
    graph = build_dependency_graph(input_dir)
    
    if len(graph.elements) == 0:
        print("错误: 未找到任何形式化元素")
        return 1
    
    # 主题筛选
    if args.topic != 'all':
        print(f"按主题 '{args.topic}' 筛选...")
        graph = graph.filter_by_topic(args.topic)
        print(f"筛选后剩余 {len(graph.elements)} 个元素")
    
    # 限制节点数量
    if len(graph.elements) > args.limit:
        print(f"限制节点数量至 {args.limit}...")
        graph = graph.limit_nodes(args.limit)
    
    # 检测循环依赖
    if not args.no_cycles_check:
        print("检测循环依赖...")
        cycles = graph.detect_cycles()
        print(f"发现 {len(cycles)} 个循环依赖")
    
    # 找出孤立节点
    isolated = graph.find_isolated()
    print(f"发现 {len(isolated)} 个孤立节点")
    
    # 生成输出
    print("\n生成输出文件...")
    
    # 1. Mermaid 图
    mermaid_path = Path(output_dir) / 'theorem-dependency-graph.mmd'
    mermaid_content = graph.to_mermaid(
        title=f"定理依赖图 ({args.topic})" if args.topic != 'all' else "定理依赖图"
    )
    with open(mermaid_path, 'w', encoding='utf-8') as f:
        f.write(mermaid_content)
    print(f"✓ Mermaid 图: {mermaid_path}")
    
    # 2. JSON 数据
    json_path = Path(output_dir) / 'theorem-dependency-data.json'
    json_content = graph.to_dict()
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_content, f, ensure_ascii=False, indent=2)
    print(f"✓ JSON 数据: {json_path}")
    
    # 3. Markdown 报告
    report_path = Path(output_dir) / 'theorem-dependency-report.md'
    generate_markdown_report(graph, report_path, args.topic)
    print(f"✓ Markdown 报告: {report_path}")
    
    # 打印统计摘要
    print("\n" + "=" * 60)
    print("统计摘要")
    print("=" * 60)
    stats = graph._calculate_statistics()
    print(f"总元素数: {len(graph.elements)}")
    print(f"总依赖边: {len(graph.edges)}")
    print(f"循环依赖: {len(graph.cycles)}")
    print(f"孤立节点: {len(graph.isolated)}")
    print(f"最大深度: {stats.get('max_depth', 0)}")
    print(f"平均深度: {stats.get('avg_depth', 0):.2f}")
    print("=" * 60)
    print("✅ 完成!")
    
    return 0


if __name__ == '__main__':
    exit(main())
