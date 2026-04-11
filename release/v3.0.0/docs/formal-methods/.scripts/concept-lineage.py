#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
概念谱系图生成工具 (Concept Lineage Generator)

功能:
    - 扫描所有定义 (Def-*)，构建概念层次关系
    - 从引用中提取年份信息，生成概念发展时间线
    - 输出 Mermaid 思维导图 (概念层次)
    - 输出 Mermaid 时间线图 (历史发展)
    - 输出 JSON 数据文件
    - 生成聚焦视图: Lambda演算、类型系统、并发理论、验证方法

作者: AnalysisDataFlow Project
版本: 1.0.0
日期: 2026-04-10
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Set, Tuple, Any


# =============================================================================
# 配置常量
# =============================================================================

DEFAULT_ENCODING = "utf-8"
DEFAULT_LOG_LEVEL = logging.INFO

# 定义编号模式
DEF_PATTERN = r"Def-[SKF]-(\d{2})-(\d{2})"
FORMAL_ELEMENT_PATTERN = r"(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d{2})-(\d{2})"

# 年份提取模式
YEAR_PATTERNS = [
    r"(\d{4})[\.\,]?\s*年?",  # 标准4位年份
    r"['\"](\d{2})[\.\,]?",   # 缩略年份 '92
    r"\((\d{4})\)",           # (1992)
    r"(\d{4})[\.\,]?\s*[–-]\s*",  # 1992-
]

# 概念分类关键词
CONCEPT_CATEGORIES = {
    "lambda_calculus": {
        "keywords": ["lambda", "λ演算", "lambda calculus", "λ-calculus", "抽象", "abstraction"],
        "display_name": "Lambda演算",
        "color": "#4A90D9",
    },
    "type_theory": {
        "keywords": ["类型", "type", "typing", "type system", "多态", "polymorphism", "依赖类型"],
        "display_name": "类型理论",
        "color": "#7B68EE",
    },
    "concurrency": {
        "keywords": ["并发", "concurrent", "process", "进程", "actor", "csp", "ccs", "π演算", "pi-calculus"],
        "display_name": "并发理论",
        "color": "#E74C3C",
    },
    "verification": {
        "keywords": ["验证", "verification", "model checking", "模型检测", "定理证明", "theorem proving", "logic", "逻辑"],
        "display_name": "验证方法",
        "color": "#27AE60",
    },
    "logic": {
        "keywords": ["逻辑", "logic", "命题", "谓词", "propositional", "predicate", "temporal", "时序"],
        "display_name": "逻辑基础",
        "color": "#F39C12",
    },
    "semantics": {
        "keywords": ["语义", "semantics", "指称", "denotational", "操作", "operational", "公理", "axiomatic"],
        "display_name": "语义理论",
        "color": "#9B59B6",
    },
    "category_theory": {
        "keywords": ["范畴", "category", "functor", "natural transformation", "余代数", "coalgebra"],
        "display_name": "范畴论",
        "color": "#1ABC9C",
    },
    "domain_theory": {
        "keywords": ["域论", "domain", "cpo", "完全偏序", "complete partial order", "连续性"],
        "display_name": "域理论",
        "color": "#34495E",
    },
}

# 层次关系关键词
HIERARCHY_KEYWORDS = {
    "parent": ["基于", "扩展", "派生", "generalization", "基于...定义", "是...的特例"],
    "child": ["包含", "特例", "instance", "example", "具体化"],
    "related": ["相关", "对比", "similar", "比较", "等价"],
}

# 默认忽略的文件/目录
DEFAULT_IGNORE_PATTERNS = [
    ".git",
    ".github",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "*.pyc",
    "*.pyo",
    ".DS_Store",
    "Thumbs.db",
    "*.log",
    "*.tmp",
    "*.temp",
]


# =============================================================================
# 数据类定义
# =============================================================================

@dataclass
class Concept:
    """概念数据结构"""
    concept_id: str  # Def-X-XX-XX
    name: str
    name_en: Optional[str]
    category: str  # lambda_calculus, type_theory, etc.
    file_path: str
    line_number: int
    content: str
    year: Optional[int] = None
    parent_concepts: List[str] = field(default_factory=list)
    child_concepts: List[str] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)
    hierarchy_level: int = 0  # 0=基础, 1=派生, 2=应用
    references: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TimelineEvent:
    """时间线事件"""
    year: int
    concept_id: str
    concept_name: str
    category: str
    description: str
    importance: int = 1  # 1-5, 5为最高


@dataclass
class ConceptHierarchy:
    """概念层次结构"""
    root_concepts: List[str] = field(default_factory=list)
    concept_map: Dict[str, Concept] = field(default_factory=dict)
    level_map: Dict[int, List[str]] = field(default_factory=dict)  # level -> concept_ids


@dataclass
class LineageResult:
    """谱系分析结果"""
    concepts: Dict[str, Concept] = field(default_factory=dict)
    timeline: List[TimelineEvent] = field(default_factory=list)
    hierarchies: Dict[str, ConceptHierarchy] = field(default_factory=dict)  # category -> hierarchy
    category_map: Dict[str, List[str]] = field(default_factory=dict)  # category -> concept_ids
    year_range: Tuple[int, int] = (1900, 2030)
    stats: Dict[str, Any] = field(default_factory=lambda: {
        "total_concepts": 0,
        "categorized": 0,
        "with_year": 0,
        "with_relations": 0,
        "categories": {},
    })


# =============================================================================
# 核心分析器类
# =============================================================================

class ConceptLineageAnalyzer:
    """
    概念谱系分析器
    
    负责扫描文档、解析定义、识别层次关系、提取时间信息。
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.def_regex = re.compile(DEF_PATTERN)
        self.year_regexes = [re.compile(p) for p in YEAR_PATTERNS]
        
    def analyze_directory(self, root_dir: str) -> LineageResult:
        """
        分析目录中的所有Markdown文件
        
        Args:
            root_dir: 根目录路径
            
        Returns:
            LineageResult 包含所有分析结果
        """
        result = LineageResult()
        root_path = Path(root_dir).resolve()
        
        self.logger.info(f"开始分析目录: {root_path}")
        
        # 第一遍：扫描所有概念
        for file_path in root_path.rglob("*.md"):
            if self._should_ignore(file_path):
                continue
            try:
                self._process_file(file_path, result, pass_num=1)
            except Exception as e:
                self.logger.warning(f"处理文件失败 {file_path}: {e}")
        
        # 第二遍：建立关系
        for file_path in root_path.rglob("*.md"):
            if self._should_ignore(file_path):
                continue
            try:
                self._process_file(file_path, result, pass_num=2)
            except Exception as e:
                self.logger.warning(f"处理文件失败 {file_path}: {e}")
        
        # 构建层次结构
        self._build_hierarchies(result)
        
        # 构建时间线
        self._build_timeline(result)
        
        # 更新统计
        self._update_statistics(result)
        
        self.logger.info(f"分析完成: {result.stats['total_concepts']} 个概念")
        
        return result

    def _should_ignore(self, file_path: Path) -> bool:
        """检查文件是否应该被忽略"""
        path_str = str(file_path)
        for pattern in DEFAULT_IGNORE_PATTERNS:
            if pattern in path_str:
                return True
        return False

    def _process_file(self, file_path: Path, result: LineageResult, pass_num: int = 1) -> None:
        """处理单个文件"""
        rel_path = str(file_path.relative_to(Path.cwd()))
        
        try:
            with open(file_path, "r", encoding=DEFAULT_ENCODING) as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="gbk", errors="ignore") as f:
                content = f.read()
        
        lines = content.split('\n')
        
        if pass_num == 1:
            self._extract_concepts(lines, rel_path, result)
        else:
            self._extract_relations(lines, rel_path, result)

    def _extract_concepts(self, lines: List[str], file_path: str, result: LineageResult) -> None:
        """提取概念定义"""
        current_concept: Optional[Concept] = None
        current_content: List[str] = []
        
        for line_num, line in enumerate(lines, 1):
            # 检查是否是定义行
            def_match = re.search(r"\*\*Def-([SKF])-(\d{2})-(\d{2})[:：]\s*([^*]+)\*\*", line)
            
            if def_match:
                # 保存之前的概念
                if current_concept:
                    current_concept.content = '\n'.join(current_content)
                    result.concepts[current_concept.concept_id] = current_concept
                
                stage = def_match.group(1)
                doc_num = def_match.group(2)
                seq_num = def_match.group(3)
                name = def_match.group(4).strip()
                
                concept_id = f"Def-{stage}-{doc_num}-{seq_num}"
                
                # 提取英文名称（如果有）
                name_en = None
                if '(' in name and ')' in name:
                    match = re.search(r'\(([A-Za-z][A-Za-z\s\-]+)\)', name)
                    if match:
                        name_en = match.group(1).strip()
                        name = name.split('(')[0].strip()
                
                # 分类
                category = self._categorize_concept(name, name_en or "")
                
                # 提取年份
                year = self._extract_year(line, lines, line_num)
                
                current_concept = Concept(
                    concept_id=concept_id,
                    name=name,
                    name_en=name_en,
                    category=category,
                    file_path=file_path,
                    line_number=line_num,
                    content="",
                    year=year,
                )
                current_content = [line]
            elif current_concept:
                current_content.append(line)
                
                # 提取引用
                refs = re.findall(r"\[\^(\d+)\]", line)
                current_concept.references.extend(refs)
        
        # 保存最后一个概念
        if current_concept:
            current_concept.content = '\n'.join(current_content)
            result.concepts[current_concept.concept_id] = current_concept

    def _extract_relations(self, lines: List[str], file_path: str, result: LineageResult) -> None:
        """提取概念间关系"""
        content = '\n'.join(lines)
        
        for concept_id, concept in result.concepts.items():
            if concept.file_path != file_path:
                continue
            
            # 查找父概念引用
            for other_id, other in result.concepts.items():
                if other_id == concept_id:
                    continue
                
                # 检查内容中是否提及其他概念
                if other.name in concept.content or (other.name_en and other.name_en in concept.content):
                    # 判断关系类型
                    relation_type = self._determine_relation_type(concept.content, other.name, other.name_en)
                    
                    if relation_type == "parent":
                        if other_id not in concept.parent_concepts:
                            concept.parent_concepts.append(other_id)
                        if concept_id not in other.child_concepts:
                            other.child_concepts.append(concept_id)
                    elif relation_type == "related":
                        if other_id not in concept.related_concepts:
                            concept.related_concepts.append(other_id)

    def _categorize_concept(self, name: str, name_en: str) -> str:
        """对概念进行分类"""
        text = (name + " " + name_en).lower()
        
        scores = {}
        for cat_id, cat_info in CONCEPT_CATEGORIES.items():
            score = 0
            for keyword in cat_info["keywords"]:
                if keyword.lower() in text:
                    score += 1
            scores[cat_id] = score
        
        if scores:
            best_match = max(scores, key=scores.get)
            if scores[best_match] > 0:
                return best_match
        
        return "other"

    def _extract_year(self, line: str, lines: List[str], line_num: int) -> Optional[int]:
        """提取年份信息"""
        # 优先在当前行查找
        for regex in self.year_regexes:
            match = regex.search(line)
            if match:
                year_str = match.group(1)
                if len(year_str) == 2:
                    year_int = int(year_str)
                    if year_int >= 50:
                        return 1900 + year_int
                    else:
                        return 2000 + year_int
                else:
                    year = int(year_str)
                    if 1900 <= year <= 2030:
                        return year
        
        # 在后续几行查找引用
        for i in range(line_num, min(line_num + 10, len(lines))):
            if i < len(lines):
                for regex in self.year_regexes:
                    match = regex.search(lines[i])
                    if match:
                        year_str = match.group(1)
                        if len(year_str) == 4:
                            year = int(year_str)
                            if 1900 <= year <= 2030:
                                return year
        
        return None

    def _determine_relation_type(self, content: str, other_name: str, other_name_en: Optional[str]) -> str:
        """确定概念间关系类型"""
        content_lower = content.lower()
        
        # 检查父概念关键词
        parent_keywords = ["基于", "扩展", "派生", "generalization", "推广", "泛化"]
        for kw in parent_keywords:
            if kw in content_lower:
                # 检查是否在提到父概念的上下文中
                idx = content_lower.find(kw)
                surrounding = content_lower[max(0, idx-50):min(len(content_lower), idx+50)]
                if other_name.lower() in surrounding or (other_name_en and other_name_en.lower() in surrounding):
                    return "parent"
        
        return "related"

    def _build_hierarchies(self, result: LineageResult) -> None:
        """构建层次结构"""
        # 按类别分组
        for concept_id, concept in result.concepts.items():
            if concept.category not in result.category_map:
                result.category_map[concept.category] = []
            result.category_map[concept.category].append(concept_id)
        
        # 为每个类别构建层次
        for category, concept_ids in result.category_map.items():
            hierarchy = ConceptHierarchy()
            
            # 计算层次级别
            for concept_id in concept_ids:
                concept = result.concepts[concept_id]
                level = self._calculate_hierarchy_level(concept, result)
                concept.hierarchy_level = level
                
                if level not in hierarchy.level_map:
                    hierarchy.level_map[level] = []
                hierarchy.level_map[level].append(concept_id)
                hierarchy.concept_map[concept_id] = concept
            
            # 识别根概念（没有父概念的）
            hierarchy.root_concepts = [
                cid for cid in concept_ids 
                if not result.concepts[cid].parent_concepts
            ]
            
            result.hierarchies[category] = hierarchy

    def _calculate_hierarchy_level(self, concept: Concept, result: LineageResult) -> int:
        """计算概念的层次级别"""
        if not concept.parent_concepts:
            return 0
        
        # 递归计算最大深度
        max_parent_level = -1
        for parent_id in concept.parent_concepts:
            if parent_id in result.concepts:
                parent = result.concepts[parent_id]
                if parent.hierarchy_level == 0 and not parent.parent_concepts:
                    max_parent_level = max(max_parent_level, 0)
                else:
                    parent_level = self._calculate_hierarchy_level(parent, result)
                    max_parent_level = max(max_parent_level, parent_level)
        
        return max_parent_level + 1 if max_parent_level >= 0 else 0

    def _build_timeline(self, result: LineageResult) -> None:
        """构建时间线"""
        events = []
        years = []
        
        for concept_id, concept in result.concepts.items():
            if concept.year:
                years.append(concept.year)
                
                # 确定重要性
                importance = 1
                if concept.hierarchy_level == 0:
                    importance = 5  # 基础概念
                elif len(concept.child_concepts) > 2:
                    importance = 4  # 有多个派生
                elif concept.category in ["lambda_calculus", "type_theory"]:
                    importance = 3
                
                events.append(TimelineEvent(
                    year=concept.year,
                    concept_id=concept_id,
                    concept_name=concept.name,
                    category=concept.category,
                    description=concept.name_en or "",
                    importance=importance,
                ))
        
        # 排序
        result.timeline = sorted(events, key=lambda e: (e.year, e.importance))
        
        if years:
            result.year_range = (min(years), max(years))

    def _update_statistics(self, result: LineageResult) -> None:
        """更新统计信息"""
        result.stats["total_concepts"] = len(result.concepts)
        result.stats["categorized"] = sum(
            1 for c in result.concepts.values() 
            if c.category != "other"
        )
        result.stats["with_year"] = sum(
            1 for c in result.concepts.values() 
            if c.year is not None
        )
        result.stats["with_relations"] = sum(
            1 for c in result.concepts.values() 
            if c.parent_concepts or c.child_concepts
        )
        
        # 按类别统计
        category_counts = {}
        for concept in result.concepts.values():
            cat = concept.category
            category_counts[cat] = category_counts.get(cat, 0) + 1
        result.stats["categories"] = category_counts


# =============================================================================
# 可视化生成器
# =============================================================================

class MermaidGenerator:
    """Mermaid图表生成器"""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def generate_mindmap(self, result: LineageResult, category: Optional[str] = None) -> str:
        """
        生成思维导图 (Mindmap)
        
        Args:
            result: 分析结果
            category: 特定类别，None表示全部
            
        Returns:
            Mermaid mindmap 代码
        """
        lines = ["```mermaid", "mindmap"]
        lines.append("  root((形式化方法\n概念谱系))")
        
        categories_to_include = [category] if category else list(result.hierarchies.keys())
        
        for cat_id in categories_to_include:
            if cat_id not in result.hierarchies:
                continue
                
            cat_info = CONCEPT_CATEGORIES.get(cat_id, {"display_name": cat_id, "color": "#3498DB"})
            hierarchy = result.hierarchies[cat_id]
            
            lines.append(f"    {cat_info['display_name']}")
            
            # 添加根概念
            for root_id in hierarchy.root_concepts[:5]:  # 限制数量
                root = hierarchy.concept_map[root_id]
                lines.append(f"      {root.name}")
                
                # 添加子概念
                for child_id in root.child_concepts[:3]:
                    if child_id in hierarchy.concept_map:
                        child = hierarchy.concept_map[child_id]
                        lines.append(f"        {child.name}")
        
        lines.append("```")
        return '\n'.join(lines)

    def generate_timeline(self, result: LineageResult) -> str:
        """
        生成时间线图
        
        Args:
            result: 分析结果
            
        Returns:
            Mermaid timeline 代码
        """
        lines = ["```mermaid", "timeline"]
        lines.append("  title 形式化方法概念发展时间线")
        
        # 按年代分组
        decades = {}
        for event in result.timeline:
            decade = (event.year // 10) * 10
            if decade not in decades:
                decades[decade] = []
            decades[decade].append(event)
        
        # 生成时间线
        for decade in sorted(decades.keys()):
            lines.append(f"  section {decade}s")
            
            # 选择重要事件
            important = [e for e in decades[decade] if e.importance >= 3]
            if not important:
                important = decades[decade][:3]
            
            for event in important[:5]:
                cat_info = CONCEPT_CATEGORIES.get(event.category, {"display_name": event.category})
                lines.append(f"    {event.year} : {event.concept_name} ({cat_info['display_name']})")
        
        lines.append("```")
        return '\n'.join(lines)

    def generate_graph(self, result: LineageResult, category: Optional[str] = None) -> str:
        """
        生成关系图 (Graph)
        
        Args:
            result: 分析结果
            category: 特定类别
            
        Returns:
            Mermaid graph 代码
        """
        lines = ["```mermaid", "graph TD"]
        lines.append("  %%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#e1f5fe'}}}%%")
        
        categories_to_include = [category] if category else ["lambda_calculus", "type_theory"]
        
        for cat_id in categories_to_include:
            if cat_id not in result.hierarchies:
                continue
                
            hierarchy = result.hierarchies[cat_id]
            cat_info = CONCEPT_CATEGORIES.get(cat_id, {"display_name": cat_id})
            
            lines.append(f"  subgraph {cat_id}[{cat_info['display_name']}]")
            lines.append("    direction TB")
            
            # 添加节点
            for concept_id in list(hierarchy.concept_map.keys())[:10]:
                concept = hierarchy.concept_map[concept_id]
                node_id = concept_id.replace("-", "_")
                lines.append(f"    {node_id}[{concept.name}]")
            
            # 添加边
            for concept_id in list(hierarchy.concept_map.keys())[:10]:
                concept = hierarchy.concept_map[concept_id]
                node_id = concept_id.replace("-", "_")
                
                for child_id in concept.child_concepts[:3]:
                    if child_id in hierarchy.concept_map:
                        child_node_id = child_id.replace("-", "_")
                        lines.append(f"    {node_id} --> {child_node_id}")
            
            lines.append("  end")
        
        lines.append("```")
        return '\n'.join(lines)

    def generate_focused_lineage(self, result: LineageResult, focus: str) -> str:
        """
        生成聚焦谱系图
        
        Args:
            result: 分析结果
            focus: 聚焦类型 (lambda, types, concurrency, verification)
            
        Returns:
            Mermaid 图表代码
        """
        focus_map = {
            "lambda": "lambda_calculus",
            "types": "type_theory", 
            "concurrency": "concurrency",
            "verification": "verification",
        }
        
        category = focus_map.get(focus)
        if not category or category not in result.hierarchies:
            return self.generate_mindmap(result, category)
        
        hierarchy = result.hierarchies[category]
        cat_info = CONCEPT_CATEGORIES.get(category, {"display_name": category})
        
        lines = ["```mermaid", "graph TB"]
        lines.append(f'  subgraph {focus}[{cat_info["display_name"]} 谱系]')
        
        # 按层次组织
        for level in sorted(hierarchy.level_map.keys()):
            concept_ids = hierarchy.level_map[level][:8]
            
            for concept_id in concept_ids:
                concept = hierarchy.concept_map[concept_id]
                node_id = f"L{level}_{concept_id.replace('-', '_')}"
                
                style = ""
                if level == 0:
                    style = ":::root"
                elif level == 1:
                    style = ":::derived"
                else:
                    style = ":::applied"
                
                lines.append(f"    {node_id}[{concept.name}]{style}")
        
        # 添加边
        for level in sorted(hierarchy.level_map.keys()):
            for concept_id in hierarchy.level_map[level][:8]:
                concept = hierarchy.concept_map[concept_id]
                node_id = f"L{level}_{concept_id.replace('-', '_')}"
                
                for child_id in concept.child_concepts[:4]:
                    if child_id in hierarchy.concept_map:
                        child_level = hierarchy.concept_map[child_id].hierarchy_level
                        child_node_id = f"L{child_level}_{child_id.replace('-', '_')}"
                        lines.append(f"    {node_id} --> {child_node_id}")
        
        lines.append("  end")
        
        # 添加样式类
        lines.append("  classDef root fill:#e1f5fe,stroke:#01579b,stroke-width:2px")
        lines.append("  classDef derived fill:#fff3e0,stroke:#e65100,stroke-width:1px")
        lines.append("  classDef applied fill:#f3e5f5,stroke:#4a148c,stroke-width:1px")
        
        lines.append("```")
        return '\n'.join(lines)


# =============================================================================
# JSON导出器
# =============================================================================

class JSONExporter:
    """JSON数据导出器"""

    def export_full_data(self, result: LineageResult) -> str:
        """导出完整数据"""
        data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_concepts": result.stats["total_concepts"],
                "year_range": result.year_range,
            },
            "concepts": {
                cid: c.to_dict() 
                for cid, c in result.concepts.items()
            },
            "timeline": [
                {
                    "year": e.year,
                    "concept_id": e.concept_id,
                    "concept_name": e.concept_name,
                    "category": e.category,
                    "description": e.description,
                    "importance": e.importance,
                }
                for e in result.timeline
            ],
            "categories": {
                cat_id: {
                    "display_name": info["display_name"],
                    "concept_count": len(result.category_map.get(cat_id, [])),
                    "concepts": result.category_map.get(cat_id, []),
                }
                for cat_id, info in CONCEPT_CATEGORIES.items()
            },
            "hierarchies": {
                cat_id: {
                    "root_concepts": h.root_concepts,
                    "level_map": h.level_map,
                }
                for cat_id, h in result.hierarchies.items()
            },
            "statistics": result.stats,
        }
        return json.dumps(data, indent=2, ensure_ascii=False)

    def export_category_data(self, result: LineageResult, category: str) -> str:
        """导出特定类别数据"""
        if category not in result.hierarchies:
            return json.dumps({"error": f"Category {category} not found"})
        
        hierarchy = result.hierarchies[category]
        cat_info = CONCEPT_CATEGORIES.get(category, {"display_name": category})
        
        data = {
            "category": category,
            "display_name": cat_info["display_name"],
            "concepts": {
                cid: result.concepts[cid].to_dict()
                for cid in hierarchy.concept_map.keys()
            },
            "hierarchy": {
                "root_concepts": hierarchy.root_concepts,
                "levels": hierarchy.level_map,
            },
        }
        return json.dumps(data, indent=2, ensure_ascii=False)


# =============================================================================
# 报告生成器
# =============================================================================

class ReportGenerator:
    """分析报告生成器"""

    def __init__(self, result: LineageResult) -> None:
        self.result = result
        self.mermaid = MermaidGenerator()
        self.json_exporter = JSONExporter()

    def generate_markdown_report(self) -> str:
        """生成Markdown格式的完整报告"""
        lines = []
        lines.append("# 概念谱系分析报告")
        lines.append("")
        lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("")
        
        # 统计摘要
        lines.append("## 📊 统计摘要")
        lines.append("")
        lines.append("| 指标 | 数值 |")
        lines.append("|------|------|")
        lines.append(f"| 概念总数 | {self.result.stats['total_concepts']} |")
        lines.append(f"| 已分类 | {self.result.stats['categorized']} |")
        lines.append(f"| 含年份信息 | {self.result.stats['with_year']} |")
        lines.append(f"| 含关系信息 | {self.result.stats['with_relations']} |")
        lines.append("")
        
        # 分类统计
        lines.append("### 按类别分布")
        lines.append("")
        lines.append("| 类别 | 数量 | 占比 |")
        lines.append("|------|------|------|")
        for cat_id, count in sorted(self.result.stats["categories"].items(), key=lambda x: -x[1]):
            cat_name = CONCEPT_CATEGORIES.get(cat_id, {"display_name": cat_id})["display_name"]
            percentage = count / self.result.stats["total_concepts"] * 100
            lines.append(f"| {cat_name} | {count} | {percentage:.1f}% |")
        lines.append("")
        
        # 时间范围
        lines.append("## 📅 时间范围")
        lines.append("")
        lines.append(f"概念发展时间跨度: **{self.result.year_range[0]} - {self.result.year_range[1]}**")
        lines.append("")
        
        # 概念层次总览
        lines.append("## 🗺️ 概念层次总览")
        lines.append("")
        lines.append(self.mermaid.generate_mindmap(self.result))
        lines.append("")
        
        # 发展时间线
        lines.append("## 📈 概念发展时间线")
        lines.append("")
        lines.append(self.mermaid.generate_timeline(self.result))
        lines.append("")
        
        # 聚焦谱系
        lines.append("## 🔍 聚焦谱系")
        lines.append("")
        
        for focus in ["lambda", "types", "concurrency", "verification"]:
            cat_id = {
                "lambda": "lambda_calculus",
                "types": "type_theory",
                "concurrency": "concurrency",
                "verification": "verification",
            }.get(focus)
            
            if cat_id in self.result.hierarchies:
                cat_name = CONCEPT_CATEGORIES.get(cat_id, {"display_name": cat_id})["display_name"]
                lines.append(f"### {cat_name}")
                lines.append("")
                lines.append(self.mermaid.generate_focused_lineage(self.result, focus))
                lines.append("")
        
        # 根概念列表
        lines.append("## 🌳 基础概念（根概念）")
        lines.append("")
        
        for cat_id, hierarchy in self.result.hierarchies.items():
            if not hierarchy.root_concepts:
                continue
            
            cat_name = CONCEPT_CATEGORIES.get(cat_id, {"display_name": cat_id})["display_name"]
            lines.append(f"### {cat_name}")
            lines.append("")
            
            for root_id in hierarchy.root_concepts[:10]:
                root = hierarchy.concept_map[root_id]
                year_str = f" ({root.year})" if root.year else ""
                lines.append(f"- **{root.name}**{year_str} - `{root_id}`")
                if root.name_en:
                    lines.append(f"  - 英文: {root.name_en}")
                if root.child_concepts:
                    lines.append(f"  - 派生概念: {len(root.child_concepts)} 个")
            lines.append("")
        
        # 里程碑事件
        lines.append("## ⭐ 关键里程碑")
        lines.append("")
        
        important_events = [e for e in self.result.timeline if e.importance >= 4]
        for event in important_events[:15]:
            cat_name = CONCEPT_CATEGORIES.get(event.category, {"display_name": event.category})["display_name"]
            lines.append(f"- **{event.year}** - {event.concept_name} ({cat_name})")
        lines.append("")
        
        lines.append("---")
        lines.append("*报告由 concept-lineage.py 自动生成*")
        
        return '\n'.join(lines)

    def generate_console_summary(self) -> str:
        """生成控制台摘要"""
        lines = []
        lines.append("=" * 60)
        lines.append("概念谱系分析摘要")
        lines.append("=" * 60)
        lines.append("")
        lines.append(f"📊 概念总数: {self.result.stats['total_concepts']}")
        lines.append(f"📂 已分类: {self.result.stats['categorized']}")
        lines.append(f"📅 含年份: {self.result.stats['with_year']}")
        lines.append(f"🔗 含关系: {self.result.stats['with_relations']}")
        lines.append("")
        
        lines.append("分类分布:")
        for cat_id, count in sorted(self.result.stats["categories"].items(), key=lambda x: -x[1])[:8]:
            cat_name = CONCEPT_CATEGORIES.get(cat_id, {"display_name": cat_id})["display_name"]
            lines.append(f"  - {cat_name}: {count}")
        lines.append("")
        
        lines.append(f"时间跨度: {self.result.year_range[0]} - {self.result.year_range[1]}")
        lines.append("")
        
        # 重要里程碑
        lines.append("关键里程碑:")
        important = [e for e in self.result.timeline if e.importance >= 4][:10]
        for event in important:
            lines.append(f"  {event.year}: {event.concept_name}")
        lines.append("")
        
        lines.append("=" * 60)
        
        return '\n'.join(lines)


# =============================================================================
# CLI 接口
# =============================================================================

def create_argument_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        prog="concept-lineage",
        description="概念谱系图生成工具 - 分析形式化方法概念的层次关系和发展时间线",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --dir ./formal-methods                    # 分析目录
  %(prog)s --dir ./formal-methods --output lineage/  # 输出到目录
  %(prog)s --focus lambda --output lambda.md         # Lambda演算谱系
  %(prog)s --json --output data.json                 # JSON输出
  %(prog)s --timeline --output timeline.md           # 仅时间线
        """,
    )
    
    parser.add_argument(
        "--dir",
        "-d",
        type=str,
        default="./formal-methods",
        help="要分析的根目录 (默认: ./formal-methods)",
    )
    
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="输出文件或目录路径",
    )
    
    parser.add_argument(
        "--format",
        "-f",
        choices=["markdown", "md", "json", "console", "all"],
        default="all",
        help="输出格式 (默认: all)",
    )
    
    parser.add_argument(
        "--focus",
        choices=["lambda", "types", "concurrency", "verification"],
        help="生成特定聚焦谱系图",
    )
    
    parser.add_argument(
        "--timeline",
        action="store_true",
        help="仅生成时间线",
    )
    
    parser.add_argument(
        "--mindmap",
        action="store_true",
        help="仅生成思维导图",
    )
    
    parser.add_argument(
        "--category",
        type=str,
        help="指定类别进行详细分析",
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="显示详细信息",
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0",
    )
    
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """主入口函数"""
    parser = create_argument_parser()
    args = parser.parse_args(argv)
    
    # 设置日志
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s",
    )
    logger = logging.getLogger(__name__)
    
    # 运行分析
    logger.info(f"开始分析目录: {args.dir}")
    analyzer = ConceptLineageAnalyzer()
    result = analyzer.analyze_directory(args.dir)
    
    # 创建报告生成器
    report_gen = ReportGenerator(result)
    mermaid_gen = MermaidGenerator()
    json_exporter = JSONExporter()
    
    # 生成输出
    outputs = {}
    
    if args.format in ("console", "all"):
        outputs["console"] = report_gen.generate_console_summary()
    
    if args.format in ("markdown", "md", "all"):
        if args.timeline:
            outputs["markdown"] = mermaid_gen.generate_timeline(result)
        elif args.mindmap:
            outputs["markdown"] = mermaid_gen.generate_mindmap(result, args.category)
        elif args.focus:
            outputs["markdown"] = mermaid_gen.generate_focused_lineage(result, args.focus)
        else:
            outputs["markdown"] = report_gen.generate_markdown_report()
    
    if args.format in ("json", "all"):
        if args.category:
            outputs["json"] = json_exporter.export_category_data(result, args.category)
        else:
            outputs["json"] = json_exporter.export_full_data(result)
    
    # 输出结果
    if args.output:
        output_path = Path(args.output)
        
        if output_path.suffix:  # 是文件
            # 确定格式
            fmt = output_path.suffix.lstrip('.')
            if fmt in ("md", "markdown") and "markdown" in outputs:
                content = outputs["markdown"]
            elif fmt == "json" and "json" in outputs:
                content = outputs["json"]
            else:
                content = outputs.get("markdown", outputs.get("console", ""))
            
            try:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "w", encoding=DEFAULT_ENCODING) as f:
                    f.write(content)
                print(f"输出已保存到: {output_path}")
            except Exception as e:
                print(f"写入文件失败: {e}")
                return 1
        else:  # 是目录
            try:
                output_path.mkdir(parents=True, exist_ok=True)
                
                # 写入多个文件
                if "markdown" in outputs:
                    md_path = output_path / "concept-lineage-report.md"
                    with open(md_path, "w", encoding=DEFAULT_ENCODING) as f:
                        f.write(outputs["markdown"])
                    print(f"Markdown报告: {md_path}")
                
                if "json" in outputs:
                    json_path = output_path / "concept-lineage-data.json"
                    with open(json_path, "w", encoding=DEFAULT_ENCODING) as f:
                        f.write(outputs["json"])
                    print(f"JSON数据: {json_path}")
                
                # 生成聚焦视图
                for focus in ["lambda", "types", "concurrency", "verification"]:
                    focus_path = output_path / f"{focus}-lineage.md"
                    with open(focus_path, "w", encoding=DEFAULT_ENCODING) as f:
                        f.write(mermaid_gen.generate_focused_lineage(result, focus))
                    print(f"聚焦视图 ({focus}): {focus_path}")
                
                # 单独的时间线
                timeline_path = output_path / "timeline.md"
                with open(timeline_path, "w", encoding=DEFAULT_ENCODING) as f:
                    f.write(mermaid_gen.generate_timeline(result))
                print(f"时间线: {timeline_path}")
                
            except Exception as e:
                print(f"写入目录失败: {e}")
                return 1
    else:
        # 输出到控制台
        if "console" in outputs:
            print(outputs["console"])
        elif "markdown" in outputs:
            print(outputs["markdown"])
        elif "json" in outputs:
            print(outputs["json"])
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
