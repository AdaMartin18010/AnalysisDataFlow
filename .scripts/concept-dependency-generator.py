#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AnalysisDataFlow 概念依赖图自动生成器 (P2-13)
Concept Dependency Graph Generator

功能：
1. 从文档中自动提取概念定义
2. 分析概念间的依赖关系
3. 生成 Mermaid 依赖图
4. 支持多级依赖层次可视化
5. 检测概念覆盖缺口

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
import textwrap


# =============================================================================
# 数据模型
# =============================================================================

@dataclass
class Concept:
    """概念定义"""
    id: str
    name: str
    definition: str
    source_file: str
    category: str  # Struct, Knowledge, Flink
    level: int = 1  # 难度等级 L1-L6
    depends_on: List[str] = field(default_factory=list)
    used_by: List[str] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)
    line_number: int = 0
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ConceptEdge:
    """概念依赖边"""
    source: str
    target: str
    type: str  # depends_on, extends, implements, uses
    strength: float = 1.0
    evidence: str = ""


@dataclass
class DependencyLevel:
    """依赖层级"""
    level: int
    concepts: List[str]
    description: str


# =============================================================================
# 概念提取器
# =============================================================================

class ConceptExtractor:
    """概念提取器"""
    
    # 形式化元素模式
    DEFINITION_PATTERN = re.compile(
        r'\*\*定义\s+([\d.]+)\s*\(([^)]+)\)\s*\*\*[:\s]*([^\n]+)',
        re.IGNORECASE
    )
    
    FORMAL_DEF_PATTERN = re.compile(
        r'`?(Def-[SKF]-\d{2}-\d{2})`?[:\s]*([^\n]+)',
        re.IGNORECASE
    )
    
    THEOREM_PATTERN = re.compile(
        r'`?(Thm-[SKF]-\d{2}-\d{2})`?[:\s]*([^\n]+)',
        re.IGNORECASE
    )
    
    # 依赖关系模式
    DEPENDS_PATTERN = re.compile(
        r'(?:依赖|depends\s+on|requires)[\s:：]+([^\n.]+)',
        re.IGNORECASE
    )
    
    # 概念引用模式
    CONCEPT_REF_PATTERN = re.compile(
        r'参见\s*\[([^\]]+)\]|refer\s+to\s*\[([^\]]+)\]',
        re.IGNORECASE
    )
    
    # 前置知识模式
    PREREQ_PATTERN = re.compile(
        r'前置知识[:：]\s*([^\n]+)|prerequisites[:：]\s*([^\n]+)',
        re.IGNORECASE
    )
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.concepts: Dict[str, Concept] = {}
        self.edges: List[ConceptEdge] = []
        
    def extract_from_file(self, file_path: Path) -> List[Concept]:
        """从单个文件提取概念"""
        concepts = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            print(f"  警告: 无法读取文件 {file_path}: {e}")
            return concepts
        
        rel_path = file_path.relative_to(self.base_path)
        category = self._determine_category(rel_path)
        
        # 提取形式化定义
        for line_num, line in enumerate(lines, 1):
            # 标准定义格式: **定义 X.X (Def-X-XX-XX)**
            for match in self.DEFINITION_PATTERN.finditer(line):
                def_num = match.group(1)
                def_id = match.group(2)
                def_text = match.group(3).strip()
                
                concept = Concept(
                    id=def_id,
                    name=def_text[:50],
                    definition=def_text,
                    source_file=str(rel_path).replace('\\', '/'),
                    category=category,
                    line_number=line_num
                )
                concepts.append(concept)
                self.concepts[def_id] = concept
            
            # 形式化ID格式: Def-X-XX-XX
            for match in self.FORMAL_DEF_PATTERN.finditer(line):
                def_id = match.group(1)
                def_text = match.group(2).strip()
                
                if def_id not in self.concepts:
                    concept = Concept(
                        id=def_id,
                        name=def_text[:50] if def_text else def_id,
                        definition=def_text,
                        source_file=str(rel_path).replace('\\', '/'),
                        category=category,
                        line_number=line_num
                    )
                    concepts.append(concept)
                    self.concepts[def_id] = concept
            
            # 定理作为概念
            for match in self.THEOREM_PATTERN.finditer(line):
                thm_id = match.group(1)
                thm_text = match.group(2).strip()
                
                if thm_id not in self.concepts:
                    concept = Concept(
                        id=thm_id,
                        name=thm_text[:50] if thm_text else thm_id,
                        definition=thm_text,
                        source_file=str(rel_path).replace('\\', '/'),
                        category=category,
                        level=4,  # 定理默认难度较高
                        line_number=line_num
                    )
                    concepts.append(concept)
                    self.concepts[thm_id] = concept
        
        # 提取依赖关系
        for concept in concepts:
            self._extract_dependencies(concept, content)
        
        return concepts
    
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
    
    def _extract_dependencies(self, concept: Concept, content: str):
        """提取概念的依赖关系"""
        # 找到概念定义后的段落
        lines = content.split('\n')
        
        # 找到概念所在行
        start_line = concept.line_number
        end_line = min(start_line + 20, len(lines))  # 向后看20行
        
        context = '\n'.join(lines[start_line-1:end_line])
        
        # 提取显式依赖
        for match in self.DEPENDS_PATTERN.finditer(context):
            dep_text = (match.group(1) or match.group(0)).strip()
            # 查找依赖的概念ID
            for concept_id in self.concepts:
                if concept_id in dep_text or self.concepts[concept_id].name in dep_text:
                    if concept_id not in concept.depends_on:
                        concept.depends_on.append(concept_id)
        
        # 提取概念引用
        for match in self.CONCEPT_REF_PATTERN.finditer(context):
            ref_text = match.group(1) or match.group(2)
            for concept_id in self.concepts:
                if concept_id in ref_text:
                    if concept_id not in concept.related_concepts:
                        concept.related_concepts.append(concept_id)
        
        # 根据ID推断依赖（形式化编号依赖）
        self._infer_dependencies_by_id(concept)
    
    def _infer_dependencies_by_id(self, concept: Concept):
        """通过ID推断依赖关系"""
        # 解析 Def-X-XX-XX 格式
        match = re.match(r'(Def|Thm|Lemma|Prop)-([SKF])-(\d{2})-(\d{2})', concept.id)
        if match:
            elem_type, category, doc_num, seq_num = match.groups()
            
            # 同一文档内的前置定义可能是依赖
            if int(seq_num) > 1:
                prev_seq = f"{int(seq_num) - 1:02d}"
                prev_id = f"{elem_type}-{category}-{doc_num}-{prev_seq}"
                if prev_id in self.concepts and prev_id not in concept.depends_on:
                    concept.depends_on.append(prev_id)
            
            # 文档编号较小可能是基础依赖
            if int(doc_num) > 1:
                # 查找同类别的基础文档
                for other_id, other_concept in self.concepts.items():
                    other_match = re.match(r'(Def|Thm)-([SKF])-(\d{2})-(\d{2})', other_id)
                    if other_match:
                        other_type, other_cat, other_doc, other_seq = other_match.groups()
                        if other_cat == category and int(other_doc) < int(doc_num):
                            if other_id not in concept.depends_on and int(other_seq) <= 2:
                                concept.depends_on.append(other_id)
    
    def scan_directory(self, directory: str) -> List[Concept]:
        """扫描目录提取概念"""
        print(f"扫描目录: {directory}")
        
        dir_path = self.base_path / directory
        if not dir_path.exists():
            print(f"  警告: 目录不存在 {dir_path}")
            return []
        
        all_concepts = []
        
        for md_file in dir_path.rglob('*.md'):
            concepts = self.extract_from_file(md_file)
            all_concepts.extend(concepts)
            if concepts:
                print(f"  {md_file.relative_to(self.base_path)}: {len(concepts)} 个概念")
        
        # 构建反向依赖（used_by）
        self._build_reverse_dependencies()
        
        print(f"  总计: {len(all_concepts)} 个概念")
        return all_concepts
    
    def _build_reverse_dependencies(self):
        """构建反向依赖关系"""
        for concept_id, concept in self.concepts.items():
            for dep_id in concept.depends_on:
                if dep_id in self.concepts:
                    if concept_id not in self.concepts[dep_id].used_by:
                        self.concepts[dep_id].used_by.append(concept_id)


# =============================================================================
# 依赖图生成器
# =============================================================================

class DependencyGraphGenerator:
    """依赖图生成器"""
    
    def __init__(self, concepts: Dict[str, Concept], output_dir: Path):
        self.concepts = concepts
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def calculate_dependency_levels(self) -> List[DependencyLevel]:
        """计算概念依赖层级"""
        levels = []
        remaining = set(self.concepts.keys())
        current_level = 0
        
        while remaining:
            current_level += 1
            # 找出当前没有未满足依赖的概念
            level_concepts = []
            
            for concept_id in list(remaining):
                concept = self.concepts[concept_id]
                # 检查所有依赖是否已在之前的层级
                unsatisfied = [d for d in concept.depends_on if d in remaining]
                if not unsatisfied:
                    level_concepts.append(concept_id)
            
            if not level_concepts:
                # 有循环依赖，强制分配
                level_concepts = list(remaining)[:5]  # 每级最多5个
            
            for cid in level_concepts:
                remaining.remove(cid)
            
            levels.append(DependencyLevel(
                level=current_level,
                concepts=level_concepts,
                description=f"第{current_level}层：基础概念" if current_level == 1 else f"第{current_level}层：进阶概念"
            ))
        
        return levels
    
    def generate_mermaid_graph(self, category: Optional[str] = None, 
                               max_nodes: int = 30) -> str:
        """生成 Mermaid 图"""
        # 筛选概念
        filtered_concepts = {
            k: v for k, v in self.concepts.items()
            if category is None or v.category == category
        }
        
        # 限制节点数量
        if len(filtered_concepts) > max_nodes:
            # 按重要性排序（被引用次数）
            sorted_concepts = sorted(
                filtered_concepts.items(),
                key=lambda x: len(x[1].used_by),
                reverse=True
            )
            selected_ids = {k for k, _ in sorted_concepts[:max_nodes]}
        else:
            selected_ids = set(filtered_concepts.keys())
        
        lines = ['```mermaid', 'graph TD']
        
        # 添加节点定义
        color_map = {
            'Struct': '#e3f2fd',
            'Knowledge': '#e8f5e9',
            'Flink': '#fff3e0'
        }
        
        for concept_id in selected_ids:
            concept = self.concepts[concept_id]
            safe_id = self._sanitize_id(concept_id)
            label = concept.name[:30].replace('"', '\\"')
            color = color_map.get(concept.category, '#ffffff')
            
            lines.append(f'    {safe_id}["{label}"]')
        
        lines.append('')
        
        # 添加依赖边
        added_edges = set()
        for concept_id in selected_ids:
            concept = self.concepts[concept_id]
            source_id = self._sanitize_id(concept_id)
            
            for dep_id in concept.depends_on:
                if dep_id in selected_ids:
                    target_id = self._sanitize_id(dep_id)
                    edge_key = (target_id, source_id)
                    
                    if edge_key not in added_edges:
                        lines.append(f'    {target_id} --> {source_id}')
                        added_edges.add(edge_key)
        
        # 添加样式
        for concept_id in selected_ids:
            concept = self.concepts[concept_id]
            safe_id = self._sanitize_id(concept_id)
            color = color_map.get(concept.category, '#ffffff')
            lines.append(f'    style {safe_id} fill:{color}')
        
        lines.append('```')
        return '\n'.join(lines)
    
    def _sanitize_id(self, concept_id: str) -> str:
        """清理ID用于 Mermaid"""
        return re.sub(r'[^a-zA-Z0-9_]', '_', concept_id)
    
    def generate_hierarchy_mermaid(self) -> str:
        """生成层次结构 Mermaid 图"""
        levels = self.calculate_dependency_levels()
        
        lines = ['```mermaid', 'graph TB']
        
        # 按层级组织
        for level in levels[:5]:  # 最多显示5层
            level_id = f"Level{level.level}"
            lines.append(f'    subgraph {level_id}["{level.description}"]')
            
            for concept_id in level.concepts[:10]:  # 每层最多10个
                concept = self.concepts[concept_id]
                safe_id = self._sanitize_id(concept_id)
                label = concept.name[:25].replace('"', '\\"')
                lines.append(f'        {safe_id}["{label}"]')
            
            lines.append('    end')
        
        lines.append('')
        
        # 添加层间连接
        for i in range(min(4, len(levels) - 1)):
            current_level = levels[i]
            next_level = levels[i + 1]
            
            # 连接代表性概念
            if current_level.concepts and next_level.concepts:
                source = self._sanitize_id(current_level.concepts[0])
                target = self._sanitize_id(next_level.concepts[0])
                lines.append(f'    {source} -.-> {target}')
        
        lines.append('```')
        return '\n'.join(lines)
    
    def generate_category_mermaid(self) -> str:
        """生成按类别组织的 Mermaid 图"""
        categories = defaultdict(list)
        for concept_id, concept in self.concepts.items():
            categories[concept.category].append(concept)
        
        lines = ['```mermaid', 'graph LR']
        
        # 为每个类别创建子图
        for category, concepts in categories.items():
            safe_cat = category.replace('/', '_')
            lines.append(f'    subgraph {safe_cat}["{category}"]')
            
            for concept in concepts[:8]:  # 每类最多8个
                safe_id = self._sanitize_id(concept.id)
                label = concept.name[:20].replace('"', '\\"')
                lines.append(f'        {safe_id}["{label}"]')
            
            lines.append('    end')
        
        lines.append('')
        
        # 添加类别间连接
        cross_category_edges = []
        for concept_id, concept in self.concepts.items():
            for dep_id in concept.depends_on:
                if dep_id in self.concepts:
                    if self.concepts[dep_id].category != concept.category:
                        source = self._sanitize_id(dep_id)
                        target = self._sanitize_id(concept_id)
                        cross_category_edges.append((source, target))
        
        # 去重并限制数量
        seen = set()
        for source, target in cross_category_edges[:15]:
            if (source, target) not in seen:
                lines.append(f'    {source} --> {target}')
                seen.add((source, target))
        
        lines.append('```')
        return '\n'.join(lines)
    
    def generate_dependency_matrix(self) -> str:
        """生成依赖矩阵 Markdown"""
        concepts_list = list(self.concepts.values())[:20]  # 限制20x20
        
        lines = ['## 概念依赖矩阵\n']
        lines.append('| 概念 | ' + ' | '.join([c.id[:10] for c in concepts_list]) + ' |')
        lines.append('|------|' + '|'.join(['------' for _ in concepts_list]) + '|')
        
        for row_concept in concepts_list:
            row = f"| {row_concept.id[:15]} |"
            for col_concept in concepts_list:
                if col_concept.id in row_concept.depends_on:
                    row += " D |"  # Depends
                elif row_concept.id in col_concept.depends_on:
                    row += " U |"  # Used by
                elif col_concept.id == row_concept.id:
                    row += " ● |"  # Self
                else:
                    row += "   |"  # No relation
            lines.append(row)
        
        lines.append('\n**图例**: D=依赖, U=被使用, ●=自身')
        return '\n'.join(lines)
    
    def export_json(self) -> str:
        """导出为 JSON"""
        data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'version': '2.0.0',
                'total_concepts': len(self.concepts)
            },
            'concepts': [c.to_dict() for c in self.concepts.values()]
        }
        
        output_path = self.output_dir / 'concept-dependencies.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"  导出: {output_path}")
        return str(output_path)
    
    def export_markdown_report(self) -> str:
        """导出 Markdown 报告"""
        lines = ['# 概念依赖关系报告\n']
        lines.append(f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        lines.append(f"**总概念数**: {len(self.concepts)}\n")
        
        # 按类别统计
        category_stats = defaultdict(int)
        for concept in self.concepts.values():
            category_stats[concept.category] += 1
        
        lines.append('## 类别统计\n')
        for cat, count in sorted(category_stats.items()):
            lines.append(f"- **{cat}**: {count} 个概念")
        
        lines.append('\n---\n')
        
        # 依赖层级
        levels = self.calculate_dependency_levels()
        lines.append(f'## 依赖层级 ({len(levels)} 层)\n')
        
        for level in levels:
            lines.append(f"### {level.description}")
            lines.append(f"概念数: {len(level.concepts)}\n")
            for concept_id in level.concepts[:10]:
                concept = self.concepts[concept_id]
                deps = len(concept.depends_on)
                used = len(concept.used_by)
                lines.append(f"- `{concept_id}` - {concept.name[:40]} (依赖: {deps}, 被用: {used})")
            if len(level.concepts) > 10:
                lines.append(f"- ... 还有 {len(level.concepts) - 10} 个概念")
            lines.append('')
        
        lines.append('\n---\n')
        
        # Mermaid 图
        lines.append('## 全局依赖图\n')
        lines.append(self.generate_mermaid_graph(max_nodes=25))
        
        lines.append('\n\n## 层次结构图\n')
        lines.append(self.generate_hierarchy_mermaid())
        
        lines.append('\n\n## 类别关系图\n')
        lines.append(self.generate_category_mermaid())
        
        lines.append('\n\n---\n')
        
        # 依赖矩阵
        lines.append(self.generate_dependency_matrix())
        
        # 核心概念列表
        lines.append('\n## 核心概念 (按引用次数排序)\n')
        sorted_concepts = sorted(
            self.concepts.values(),
            key=lambda x: len(x.used_by),
            reverse=True
        )
        
        for i, concept in enumerate(sorted_concepts[:20], 1):
            lines.append(f"{i}. **{concept.id}** - {concept.name}")
            lines.append(f"   - 来源: `{concept.source_file}`")
            lines.append(f"   - 被引用: {len(concept.used_by)} 次")
            if concept.depends_on:
                lines.append(f"   - 依赖: {', '.join(concept.depends_on[:5])}")
            lines.append('')
        
        output_path = self.output_dir / 'concept-dependencies.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"  导出: {output_path}")
        return str(output_path)


# =============================================================================
# 集成到文档
# =============================================================================

class DocumentIntegrator:
    """将生成的图集成到现有文档"""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
    
    def integrate_to_index(self, mermaid_graph: str, category: str):
        """将依赖图集成到目录文档"""
        index_file = self.base_path / category / '00-INDEX.md'
        
        if not index_file.exists():
            print(f"  警告: 索引文件不存在 {index_file}")
            return
        
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找或创建概念依赖图部分
            marker = '## 8. 文档依赖图'
            
            if marker in content:
                # 更新现有部分
                parts = content.split(marker)
                before = parts[0]
                after_parts = parts[1].split('##', 1)
                after = '##' + after_parts[1] if len(after_parts) > 1 else ''
                
                new_section = f"{marker}\n\n### 8.1 自动生成的概念依赖图\n\n{mermaid_graph}\n\n"
                
                content = before + new_section + '\n' + after
            else:
                # 在文件末尾添加
                content += f"\n\n{marker}\n\n{mermaid_graph}\n"
            
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  已更新: {index_file}")
            
        except Exception as e:
            print(f"  错误: 无法更新 {index_file}: {e}")


# =============================================================================
# 主程序
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='概念依赖图自动生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 扫描所有目录
  python concept-dependency-generator.py
  
  # 扫描指定目录
  python concept-dependency-generator.py --dirs Struct Knowledge
  
  # 生成特定类别的图
  python concept-dependency-generator.py --category Struct
  
  # 集成到文档
  python concept-dependency-generator.py --integrate
        """
    )
    
    parser.add_argument('--base-path', default='.', help='项目根目录')
    parser.add_argument('--dirs', nargs='+',
                       default=['Struct', 'Knowledge', 'Flink'],
                       help='要扫描的目录')
    parser.add_argument('--output', default='KNOWLEDGE-GRAPH/data',
                       help='输出目录')
    parser.add_argument('--category', help='仅生成特定类别的图')
    parser.add_argument('--max-nodes', type=int, default=30,
                       help='图中最大节点数')
    parser.add_argument('--integrate', action='store_true',
                       help='将图集成到目录文档')
    parser.add_argument('--export-formats', nargs='+',
                       default=['json', 'markdown'],
                       help='导出格式: json, markdown')
    
    args = parser.parse_args()
    
    base_path = Path(args.base_path).resolve()
    output_dir = base_path / args.output
    
    print("=" * 60)
    print("概念依赖图自动生成器 v2.0.0")
    print("=" * 60)
    print(f"项目路径: {base_path}")
    print(f"输出目录: {output_dir}")
    print()
    
    # 提取概念
    extractor = ConceptExtractor(base_path)
    all_concepts = []
    
    for directory in args.dirs:
        dir_path = base_path / directory
        if dir_path.exists():
            concepts = extractor.scan_directory(directory)
            all_concepts.extend(concepts)
        else:
            print(f"警告: 目录 {directory} 不存在，跳过")
    
    if not all_concepts:
        print("\n未找到任何概念定义")
        return
    
    print(f"\n总计发现: {len(all_concepts)} 个概念")
    
    # 生成依赖图
    generator = DependencyGraphGenerator(extractor.concepts, output_dir)
    
    print("\n生成 Mermaid 图...")
    
    # 生成各类图表
    if args.category:
        mermaid = generator.generate_mermaid_graph(
            category=args.category,
            max_nodes=args.max_nodes
        )
        print(f"\n{args.category} 类别依赖图:\n")
        print(mermaid)
    else:
        # 生成全局图
        mermaid = generator.generate_mermaid_graph(max_nodes=args.max_nodes)
        hierarchy = generator.generate_hierarchy_mermaid()
        category_graph = generator.generate_category_mermaid()
    
    # 导出文件
    print("\n导出文件...")
    
    if 'json' in args.export_formats:
        generator.export_json()
    
    if 'markdown' in args.export_formats:
        generator.export_markdown_report()
    
    # 集成到文档
    if args.integrate:
        print("\n集成到文档...")
        integrator = DocumentIntegrator(base_path)
        
        for category in ['Struct', 'Knowledge', 'Flink']:
            cat_mermaid = generator.generate_mermaid_graph(
                category=category,
                max_nodes=20
            )
            integrator.integrate_to_index(cat_mermaid, category)
    
    print("\n" + "=" * 60)
    print("完成!")
    print("=" * 60)
    print(f"\n输出文件:")
    if 'json' in args.export_formats:
        print(f"  📊 concept-dependencies.json - JSON数据")
    if 'markdown' in args.export_formats:
        print(f"  📝 concept-dependencies.md - Markdown报告")
    print(f"\n使用方式:")
    print(f"  1. 查看报告: {output_dir}/concept-dependencies.md")
    print(f"  2. 复制Mermaid代码到支持Mermaid的编辑器")
    print(f"  3. 使用VSCode插件 'Markdown Preview Mermaid Support' 预览")
    print()


if __name__ == '__main__':
    main()
