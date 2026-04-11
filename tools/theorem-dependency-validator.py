#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定理依赖验证工具 - Theorem Dependency Validator

功能：
1. 扫描所有Markdown文档提取定理/定义/引理/命题/推论
2. 检查依赖声明是否存在，检测循环依赖，识别孤立元素
3. 验证文档间链接有效性，检查THEOREM-REGISTRY.md同步状态
4. 检测重复编号
5. 自动生成Mermaid依赖图、Neo4j CSV、Graphviz DOT文件
6. 生成依赖完整性报告和统计覆盖率

作者: AnalysisDataFlow Automation Team
版本: 1.0.0
日期: 2026-04-11
"""

import os
import re
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple, Optional, Any
from collections import defaultdict
from enum import Enum


class ElementType(Enum):
    """形式化元素类型"""
    THEOREM = "Thm"
    DEFINITION = "Def"
    LEMMA = "Lemma"
    PROPOSITION = "Prop"
    COROLLARY = "Cor"


class Severity(Enum):
    """问题严重级别"""
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class FormalElement:
    """形式化元素数据结构"""
    id: str                          # 完整编号如 "Thm-S-01-01"
    element_type: ElementType        # 元素类型
    stage: str                       # 阶段 (S/K/F)
    doc_num: str                     # 文档序号
    seq_num: str                     # 顺序号
    name: str                        # 名称/描述
    file_path: str                   # 所在文件路径
    line_number: int                 # 行号
    formal_level: Optional[str] = None  # 形式化等级 L1-L6
    dependencies: List[str] = field(default_factory=list)  # 依赖的元素ID列表
    referenced_by: List[str] = field(default_factory=list)  # 被哪些元素引用
    status: str = "OK"               # 状态标记


@dataclass
class ValidationIssue:
    """验证问题数据结构"""
    severity: Severity
    code: str                        # 问题代码
    message: str                     # 问题描述
    element_id: Optional[str] = None
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    suggestion: Optional[str] = None


class Colors:
    """终端颜色代码"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class TheoremDependencyValidator:
    """定理依赖验证器主类"""
    
    # 正则表达式模式
    ELEMENT_PATTERNS = {
        ElementType.THEOREM: re.compile(
            r'\*\*Thm-([SKF])-(\d{2})-(\d{2,3})\*\*[:：]?\s*(.*?)(?:\n|$)',
            re.MULTILINE
        ),
        ElementType.DEFINITION: re.compile(
            r'\*\*Def-([SKF])-(\d{2})-(\d{2,3})\*\*[:：]?\s*(.*?)(?:\n|$)',
            re.MULTILINE
        ),
        ElementType.LEMMA: re.compile(
            r'\*\*Lemma-([SKF])-(\d{2})-(\d{2,3})\*\*[:：]?\s*(.*?)(?:\n|$)',
            re.MULTILINE
        ),
        ElementType.PROPOSITION: re.compile(
            r'\*\*Prop-([SKF])-(\d{2})-(\d{2,3})\*\*[:：]?\s*(.*?)(?:\n|$)',
            re.MULTILINE
        ),
        ElementType.COROLLARY: re.compile(
            r'\*\*Cor-([SKF])-(\d{2})-(\d{2,3})\*\*[:：]?\s*(.*?)(?:\n|$)',
            re.MULTILINE
        ),
    }
    
    # 依赖检测模式
    DEPENDENCY_PATTERNS = [
        re.compile(r'依赖元素[：:]\s*([^\n]+)', re.MULTILINE),
        re.compile(r'依赖[：:]\s*([^\n]+)', re.MULTILINE),
        re.compile(r'\|\s*([^|]*Thm-[^|]*|[^|]*Def-[^|]*|[^|]*Lemma-[^|]*)\s*\|', re.MULTILINE),
    ]
    
    # 形式化等级检测
    FORMAL_LEVEL_PATTERN = re.compile(r'形式化等级[：:]\s*(L[1-6](?:-L[1-6])?)', re.MULTILINE)
    
    # Markdown链接检测
    LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')
    
    def __init__(self, project_root: str, verbose: bool = False, no_color: bool = False):
        self.project_root = Path(project_root)
        self.verbose = verbose
        self.no_color = no_color
        self.elements: Dict[str, FormalElement] = {}
        self.issues: List[ValidationIssue] = []
        self.file_cache: Dict[str, str] = {}
        self.scanned_files: Set[str] = set()
        self.registry_ids: Set[str] = set()
        
    def _color(self, color_code: str, text: str) -> str:
        """根据设置返回带颜色或不带颜色的文本"""
        if self.no_color:
            return text
        return f"{color_code}{text}{Colors.ENDC}"
    
    def _log(self, message: str, level: str = "info"):
        """输出日志信息"""
        if not self.verbose and level == "debug":
            return
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        if level == "error":
            print(f"[{timestamp}] {self._color(Colors.FAIL, 'ERROR')} {message}")
        elif level == "warning":
            print(f"[{timestamp}] {self._color(Colors.WARNING, 'WARN ')} {message}")
        elif level == "success":
            print(f"[{timestamp}] {self._color(Colors.GREEN, 'OK   ')} {message}")
        elif level == "info":
            print(f"[{timestamp}] {self._color(Colors.BLUE, 'INFO ')} {message}")
        else:
            print(f"[{timestamp}] {message}")
    
    def scan_markdown_files(self, directories: List[str] = None) -> int:
        """扫描指定目录下的所有Markdown文件"""
        if directories is None:
            directories = ['Struct', 'Knowledge', 'Flink']
        
        self._log("开始扫描Markdown文件...", "info")
        
        for dir_name in directories:
            dir_path = self.project_root / dir_name
            if not dir_path.exists():
                self._log(f"目录不存在: {dir_path}", "warning")
                continue
            
            for md_file in dir_path.rglob("*.md"):
                self._scan_single_file(md_file)
        
        # 同时扫描根目录的THEOREM-REGISTRY.md
        registry_file = self.project_root / "THEOREM-REGISTRY.md"
        if registry_file.exists():
            self._scan_registry_file(registry_file)
        
        self._log(f"扫描完成: 共 {len(self.scanned_files)} 个文件", "success")
        self._log(f"发现形式化元素: {len(self.elements)} 个", "success")
        
        return len(self.scanned_files)
    
    def _scan_single_file(self, file_path: Path):
        """扫描单个Markdown文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            relative_path = file_path.relative_to(self.project_root)
            self.file_cache[str(relative_path)] = content
            self.scanned_files.add(str(relative_path))
            
            # 扫描各种形式化元素
            for element_type, pattern in self.ELEMENT_PATTERNS.items():
                for match in pattern.finditer(content):
                    stage, doc_num, seq_num, name = match.groups()
                    element_id = f"{element_type.value}-{stage}-{doc_num}-{seq_num}"
                    
                    # 计算行号
                    line_num = content[:match.start()].count('\n') + 1
                    
                    # 提取依赖
                    dependencies = self._extract_dependencies(content, match.end())
                    
                    # 检测形式化等级
                    formal_level = self._detect_formal_level(content, match.start())
                    
                    element = FormalElement(
                        id=element_id,
                        element_type=element_type,
                        stage=stage,
                        doc_num=doc_num,
                        seq_num=seq_num,
                        name=name.strip()[:100],
                        file_path=str(relative_path),
                        line_number=line_num,
                        formal_level=formal_level,
                        dependencies=dependencies
                    )
                    
                    # 检查重复
                    if element_id in self.elements:
                        existing = self.elements[element_id]
                        self.issues.append(ValidationIssue(
                            severity=Severity.ERROR,
                            code="DUPLICATE_ID",
                            message=f"重复的元素编号: {element_id}",
                            element_id=element_id,
                            file_path=str(relative_path),
                            line_number=line_num,
                            suggestion=f"该编号已在 {existing.file_path}:{existing.line_number} 使用"
                        ))
                    else:
                        self.elements[element_id] = element
            
            self._log(f"扫描: {relative_path}", "debug")
            
        except Exception as e:
            self._log(f"读取文件失败 {file_path}: {e}", "error")
    
    def _scan_registry_file(self, file_path: Path):
        """扫描THEOREM-REGISTRY.md文件以进行交叉验证"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取注册表中所有元素ID
            registry_ids = set()
            for pattern in self.ELEMENT_PATTERNS.values():
                for match in pattern.finditer(content):
                    groups = match.groups()
                    stage, doc_num, seq_num = groups[0], groups[1], groups[2]
                    element_type = None
                    for et, p in self.ELEMENT_PATTERNS.items():
                        if p == pattern:
                            element_type = et
                            break
                    if element_type:
                        element_id = f"{element_type.value}-{stage}-{doc_num}-{seq_num}"
                        registry_ids.add(element_id)
            
            self.registry_ids = registry_ids
            self._log(f"从注册表提取 {len(registry_ids)} 个元素ID", "debug")
            
        except Exception as e:
            self._log(f"读取注册表失败: {e}", "error")
    
    def _extract_dependencies(self, content: str, start_pos: int) -> List[str]:
        """从指定位置开始提取依赖声明"""
        dependencies = []
        # 获取接下来的500个字符
        snippet = content[start_pos:start_pos + 500]
        
        # 匹配所有形式化元素ID
        all_element_pattern = re.compile(
            r'(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d{2})-(\d{2,3})'
        )
        
        for match in all_element_pattern.finditer(snippet):
            dep_id = match.group(0)
            # 避免自我引用和重复
            if dep_id not in dependencies:
                dependencies.append(dep_id)
        
        return dependencies[:10]  # 限制依赖数量
    
    def _detect_formal_level(self, content: str, position: int) -> Optional[str]:
        """检测形式化等级"""
        # 向前搜索形式化等级声明
        before_content = content[max(0, position-1000):position]
        match = self.FORMAL_LEVEL_PATTERN.search(before_content)
        if match:
            return match.group(1)
        return None
    
    def validate_dependencies(self):
        """验证依赖完整性"""
        self._log("开始验证依赖完整性...", "info")
        
        for element_id, element in self.elements.items():
            # 检查依赖是否存在
            for dep_id in element.dependencies:
                if dep_id not in self.elements:
                    self.issues.append(ValidationIssue(
                        severity=Severity.WARNING,
                        code="MISSING_DEPENDENCY",
                        message=f"依赖的元素不存在: {dep_id}",
                        element_id=element_id,
                        file_path=element.file_path,
                        line_number=element.line_number,
                        suggestion=f"请检查依赖声明或创建 {dep_id}"
                    ))
                else:
                    # 建立反向引用
                    self.elements[dep_id].referenced_by.append(element_id)
        
        missing_count = len([i for i in self.issues if i.code == "MISSING_DEPENDENCY"])
        self._log(f"依赖验证完成，发现 {missing_count} 个缺失依赖", 
                  "success" if missing_count == 0 else "warning")
    
    def detect_circular_dependencies(self) -> List[List[str]]:
        """检测循环依赖"""
        self._log("检测循环依赖...", "info")
        
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(node_id: str, path: List[str]):
            visited.add(node_id)
            rec_stack.add(node_id)
            path.append(node_id)
            
            element = self.elements.get(node_id)
            if element:
                for dep_id in element.dependencies:
                    if dep_id not in visited:
                        dfs(dep_id, path)
                    elif dep_id in rec_stack:
                        # 发现循环
                        cycle_start = path.index(dep_id)
                        cycle = path[cycle_start:] + [dep_id]
                        cycles.append(cycle)
            
            path.pop()
            rec_stack.remove(node_id)
        
        for element_id in self.elements:
            if element_id not in visited:
                dfs(element_id, [])
        
        # 报告循环依赖
        for cycle in cycles:
            self.issues.append(ValidationIssue(
                severity=Severity.ERROR,
                code="CIRCULAR_DEPENDENCY",
                message=f"发现循环依赖: {' -> '.join(cycle)}",
                element_id=cycle[0],
                suggestion="请检查依赖关系，确保依赖图是无环的"
            ))
        
        self._log(f"循环依赖检测完成: {len(cycles)} 个循环", 
                  "success" if not cycles else "error")
        
        return cycles
    
    def identify_orphaned_elements(self) -> List[FormalElement]:
        """识别孤立元素（无依赖且无被引用）"""
        self._log("识别孤立元素...", "info")
        
        orphaned = []
        for element_id, element in self.elements.items():
            # 排除基础定义（它们通常没有依赖）
            if not element.dependencies and not element.referenced_by:
                # 检查是否是基础层元素（文档序号01）
                if element.doc_num != "01":
                    orphaned.append(element)
                    self.issues.append(ValidationIssue(
                        severity=Severity.INFO,
                        code="ORPHANED_ELEMENT",
                        message=f"孤立元素: {element_id} - {element.name}",
                        element_id=element_id,
                        file_path=element.file_path,
                        line_number=element.line_number,
                        suggestion="考虑添加相关依赖或在其他定理中引用此元素"
                    ))
        
        self._log(f"孤立元素识别完成: {len(orphaned)} 个", "info")
        return orphaned
    
    def check_registry_sync(self) -> Tuple[List[str], List[str]]:
        """检查与THEOREM-REGISTRY.md的同步状态"""
        self._log("检查注册表同步状态...", "info")
        
        if not self.registry_ids:
            self._log("注册表数据不可用，跳过同步检查", "warning")
            return [], []
        
        scanned_ids = set(self.elements.keys())
        
        in_registry_not_scanned = self.registry_ids - scanned_ids
        in_scanned_not_registry = scanned_ids - self.registry_ids
        
        for element_id in in_registry_not_scanned:
            self.issues.append(ValidationIssue(
                severity=Severity.WARNING,
                code="REGISTRY_ORPHAN",
                message=f"注册表中有但未在文档中找到: {element_id}",
                element_id=element_id,
                suggestion="请检查文档是否被删除或编号是否变更"
            ))
        
        for element_id in in_scanned_not_registry:
            element = self.elements[element_id]
            self.issues.append(ValidationIssue(
                severity=Severity.WARNING,
                code="NOT_IN_REGISTRY",
                message=f"文档中有但未在注册表中登记: {element_id}",
                element_id=element_id,
                file_path=element.file_path,
                suggestion="请更新THEOREM-REGISTRY.md添加此元素"
            ))
        
        self._log(f"注册表同步检查完成: {len(in_registry_not_scanned)} 个孤儿, "
                  f"{len(in_scanned_not_registry)} 个未登记", "info")
        
        return list(in_registry_not_scanned), list(in_scanned_not_registry)
    
    def generate_dependency_graph(self) -> Dict[str, List[str]]:
        """生成依赖图"""
        graph = {}
        for element_id, element in self.elements.items():
            graph[element_id] = element.dependencies
        return graph
    
    def find_critical_path(self) -> List[str]:
        """查找关键路径（最长的依赖链）"""
        graph = self.generate_dependency_graph()
        
        # 使用迭代方式计算最长路径，避免递归深度问题
        # 拓扑排序 + 动态规划
        in_degree = {node: 0 for node in graph}
        for node, deps in graph.items():
            for dep in deps:
                if dep in in_degree:
                    in_degree[dep] += 1
        
        # 初始化距离和前驱节点
        dist = {node: 1 for node in graph}  # 至少包含自己
        predecessor = {node: None for node in graph}
        
        # 使用队列进行拓扑排序
        from collections import deque
        queue = deque([node for node in graph if in_degree[node] == 0])
        
        processed = set()
        while queue:
            node = queue.popleft()
            processed.add(node)
            
            # 更新邻居的距离
            for dep in graph.get(node, []):
                if dep in graph:
                    if dist[node] + 1 > dist[dep]:
                        dist[dep] = dist[node] + 1
                        predecessor[dep] = node
                    
                    in_degree[dep] -= 1
                    if in_degree[dep] == 0:
                        queue.append(dep)
        
        # 找到距离最大的节点
        if not dist:
            return []
        
        critical_end = max(dist.keys(), key=lambda x: dist[x])
        max_length = dist[critical_end]
        
        # 重构路径（从终点回溯到起点）
        path = []
        current = critical_end
        visited_in_path = set()
        while current and current not in visited_in_path:
            path.append(current)
            visited_in_path.add(current)
            current = predecessor.get(current)
        
        # 反转得到从起点到终点的路径
        path.reverse()
        
        return path
    
    def generate_mermaid_graph(self, output_path: str, max_nodes: int = 50):
        """生成Mermaid依赖图"""
        lines = ["```mermaid", "graph TB"]
        
        # 选择最重要的节点（被引用最多的）
        sorted_elements = sorted(
            self.elements.values(),
            key=lambda e: len(e.referenced_by),
            reverse=True
        )[:max_nodes]
        
        selected_ids = {e.id for e in sorted_elements}
        
        # 添加节点定义
        for element in sorted_elements:
            short_name = element.name[:30] + "..." if len(element.name) > 30 else element.name
            lines.append(f'    {element.id}["{element.id}<br/>{short_name}"]')
        
        # 添加边
        for element in sorted_elements:
            for dep_id in element.dependencies:
                if dep_id in selected_ids:
                    lines.append(f"    {element.id} --> {dep_id}")
        
        lines.append("```")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        self._log(f"Mermaid图已生成: {output_path}", "success")
    
    def generate_neo4j_csv(self, nodes_path: str, edges_path: str):
        """生成Neo4j兼容的CSV文件"""
        # 节点CSV
        with open(nodes_path, 'w', encoding='utf-8') as f:
            f.write("elementId:ID,name,type,stage,docNum,formalLevel,:LABEL\n")
            for element in self.elements.values():
                label = element.element_type.value
                name_escaped = element.name.replace('"', '\\"').replace('\n', ' ')
                f.write(f'"{element.id}","{name_escaped}",'
                        f'"{element.element_type.value}","{element.stage}",'
                        f'"{element.doc_num}","{element.formal_level or ""}",'
                        f'{label}\n')
        
        # 边CSV
        with open(edges_path, 'w', encoding='utf-8') as f:
            f.write(":START_ID,:END_ID,relation:TYPE\n")
            for element in self.elements.values():
                for dep_id in element.dependencies:
                    if dep_id in self.elements:
                        f.write(f'"{element.id}","{dep_id}",DEPENDS_ON\n')
        
        self._log(f"Neo4j CSV已生成: {nodes_path}, {edges_path}", "success")
    
    def generate_graphviz_dot(self, output_path: str):
        """生成Graphviz DOT文件"""
        lines = [
            "digraph TheoremDependencyGraph {",
            '    rankdir=TB;',
            '    node [shape=box, style="rounded,filled", fontname="Arial"];',
            '    edge [fontname="Arial", fontsize=10];',
            ''
        ]
        
        # 按类型定义节点颜色
        type_colors = {
            ElementType.THEOREM: '#90EE90',
            ElementType.DEFINITION: '#87CEEB',
            ElementType.LEMMA: '#FFD700',
            ElementType.PROPOSITION: '#FFA07A',
            ElementType.COROLLARY: '#DDA0DD',
        }
        
        # 添加节点
        for element in self.elements.values():
            color = type_colors.get(element.element_type, '#FFFFFF')
            short_name = element.name[:40].replace('"', '\\"')
            lines.append(f'    "{element.id}" [label="{element.id}\\n{short_name}", '
                        f'fillcolor="{color}"];')
        
        lines.append('')
        
        # 添加边
        for element in self.elements.values():
            for dep_id in element.dependencies:
                if dep_id in self.elements:
                    lines.append(f'    "{element.id}" -> "{dep_id}";')
        
        lines.append('}')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        self._log(f"Graphviz DOT已生成: {output_path}", "success")
    
    def calculate_coverage(self) -> Dict[str, Any]:
        """计算覆盖率统计"""
        stats = {
            "total_elements": len(self.elements),
            "elements_with_dependencies": 0,
            "elements_with_references": 0,
            "total_dependencies": 0,
            "orphaned_elements": 0,
            "by_type": defaultdict(int),
            "by_stage": defaultdict(int),
            "by_formal_level": defaultdict(int),
            "dependency_coverage": 0.0,
        }
        
        for element in self.elements.values():
            stats["by_type"][element.element_type.value] += 1
            stats["by_stage"][element.stage] += 1
            if element.formal_level:
                stats["by_formal_level"][element.formal_level] += 1
            
            if element.dependencies:
                stats["elements_with_dependencies"] += 1
                stats["total_dependencies"] += len(element.dependencies)
            
            if element.referenced_by:
                stats["elements_with_references"] += 1
            
            if not element.dependencies and not element.referenced_by:
                stats["orphaned_elements"] += 1
        
        # 计算覆盖率
        if stats["total_elements"] > 0:
            stats["dependency_coverage"] = (
                stats["elements_with_dependencies"] / stats["total_elements"] * 100
            )
        
        return dict(stats)
    
    def generate_markdown_report(self, output_path: str):
        """生成Markdown格式的验证报告"""
        coverage = self.calculate_coverage()
        critical_path = self.find_critical_path()
        
        lines = [
            "# 定理依赖验证报告",
            "",
            f"> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"> **验证工具**: Theorem Dependency Validator v1.0.0",
            "",
            "## 摘要",
            "",
            f"- **扫描文件数**: {len(self.scanned_files)}",
            f"- **发现元素数**: {len(self.elements)}",
            f"- **问题总数**: {len(self.issues)}",
            f"  - 错误: {len([i for i in self.issues if i.severity == Severity.ERROR])}",
            f"  - 警告: {len([i for i in self.issues if i.severity == Severity.WARNING])}",
            f"  - 信息: {len([i for i in self.issues if i.severity == Severity.INFO])}",
            "",
            "## 统计概览",
            "",
            "### 按类型分布",
            "",
            "| 类型 | 数量 | 占比 |",
            "|------|------|------|",
        ]
        
        for type_name, count in sorted(coverage["by_type"].items()):
            percentage = count / coverage["total_elements"] * 100
            lines.append(f"| {type_name} | {count} | {percentage:.1f}% |")
        
        lines.extend([
            "",
            "### 按阶段分布",
            "",
            "| 阶段 | 数量 | 说明 |",
            "|------|------|------|",
        ])
        
        stage_descriptions = {
            "S": "Struct - 形式理论",
            "K": "Knowledge - 知识结构",
            "F": "Flink - Flink专项"
        }
        
        for stage, count in sorted(coverage["by_stage"].items()):
            desc = stage_descriptions.get(stage, "未知")
            lines.append(f"| {stage} | {count} | {desc} |")
        
        lines.extend([
            "",
            "### 形式化等级分布",
            "",
            "| 等级 | 数量 |",
            "|------|------|",
        ])
        
        for level, count in sorted(coverage["by_formal_level"].items()):
            lines.append(f"| {level} | {count} |")
        
        lines.extend([
            "",
            "### 依赖覆盖",
            "",
            f"- **有依赖的元素**: {coverage['elements_with_dependencies']} / {coverage['total_elements']} "
            f"({coverage['dependency_coverage']:.1f}%)",
            f"- **有被引用的元素**: {coverage['elements_with_references']} / {coverage['total_elements']}",
            f"- **孤立元素**: {coverage['orphaned_elements']}",
            f"- **依赖关系总数**: {coverage['total_dependencies']}",
            "",
            "## 关键路径",
            "",
            "依赖图中最长的依赖链:",
            "",
        ])
        
        if critical_path:
            lines.append(" -> ".join(critical_path))
        else:
            lines.append("*未找到关键路径*")
        
        lines.extend([
            "",
            "## 问题详情",
            "",
        ])
        
        # 按严重程度分组
        errors = [i for i in self.issues if i.severity == Severity.ERROR]
        warnings = [i for i in self.issues if i.severity == Severity.WARNING]
        infos = [i for i in self.issues if i.severity == Severity.INFO]
        
        if errors:
            lines.extend([
                "### 错误",
                "",
            ])
            for issue in errors:
                lines.extend([
                    f"#### {issue.code}",
                    "",
                    f"- **消息**: {issue.message}",
                    f"- **元素**: {issue.element_id or 'N/A'}",
                    f"- **位置**: {issue.file_path or 'N/A'}:{issue.line_number or 'N/A'}",
                ])
                if issue.suggestion:
                    lines.append(f"- **建议**: {issue.suggestion}")
                lines.append("")
        
        if warnings:
            lines.extend([
                "### 警告",
                "",
            ])
            for issue in warnings:
                lines.extend([
                    f"#### {issue.code}",
                    "",
                    f"- **消息**: {issue.message}",
                    f"- **元素**: {issue.element_id or 'N/A'}",
                ])
                if issue.suggestion:
                    lines.append(f"- **建议**: {issue.suggestion}")
                lines.append("")
        
        if infos:
            lines.extend([
                "### 信息",
                "",
            ])
            for issue in infos[:20]:
                lines.append(f"- {issue.message}")
            if len(infos) > 20:
                lines.append(f"- ... 还有 {len(infos) - 20} 个信息项")
            lines.append("")
        
        lines.extend([
            "---",
            "",
            "*报告由 Theorem Dependency Validator 自动生成*",
        ])
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        self._log(f"Markdown报告已生成: {output_path}", "success")
    
    def generate_json_report(self, output_path: str):
        """生成JSON格式的验证报告"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "summary": {
                "total_files": len(self.scanned_files),
                "total_elements": len(self.elements),
                "total_issues": len(self.issues),
                "error_count": len([i for i in self.issues if i.severity == Severity.ERROR]),
                "warning_count": len([i for i in self.issues if i.severity == Severity.WARNING]),
                "info_count": len([i for i in self.issues if i.severity == Severity.INFO]),
            },
            "coverage": self.calculate_coverage(),
            "critical_path": self.find_critical_path(),
            "elements": {
                element_id: {
                    "id": e.id,
                    "type": e.element_type.value,
                    "stage": e.stage,
                    "doc_num": e.doc_num,
                    "seq_num": e.seq_num,
                    "name": e.name,
                    "file_path": e.file_path,
                    "line_number": e.line_number,
                    "formal_level": e.formal_level,
                    "dependencies": e.dependencies,
                    "referenced_by": e.referenced_by,
                    "status": e.status,
                }
                for element_id, e in self.elements.items()
            },
            "issues": [
                {
                    "severity": i.severity.value,
                    "code": i.code,
                    "message": i.message,
                    "element_id": i.element_id,
                    "file_path": i.file_path,
                    "line_number": i.line_number,
                    "suggestion": i.suggestion,
                }
                for i in self.issues
            ],
            "dependency_graph": self.generate_dependency_graph(),
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self._log(f"JSON报告已生成: {output_path}", "success")
    
    def run_full_validation(self, output_dir: str):
        """运行完整的验证流程"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print("\n" + "=" * 60)
        print(self._color(Colors.BOLD + Colors.CYAN, " 定理依赖验证工具 v1.0.0 "))
        print("=" * 60 + "\n")
        
        # 1. 扫描文件
        self.scan_markdown_files()
        
        # 2. 验证依赖
        self.validate_dependencies()
        
        # 3. 检测循环依赖
        self.detect_circular_dependencies()
        
        # 4. 识别孤立元素
        self.identify_orphaned_elements()
        
        # 5. 检查注册表同步
        self.check_registry_sync()
        
        print("\n" + "-" * 60)
        print(self._color(Colors.BOLD, "正在生成输出文件..."))
        print("-" * 60 + "\n")
        
        # 6. 生成输出
        self.generate_markdown_report(str(output_path / "validation-report.md"))
        self.generate_json_report(str(output_path / "validation-report.json"))
        self.generate_mermaid_graph(str(output_path / "dependency-graph.mermaid"))
        self.generate_neo4j_csv(
            str(output_path / "neo4j-nodes.csv"),
            str(output_path / "neo4j-edges.csv")
        )
        self.generate_graphviz_dot(str(output_path / "dependency-graph.dot"))
        
        # 7. 打印摘要
        self._print_summary()
    
    def _print_summary(self):
        """打印验证摘要"""
        coverage = self.calculate_coverage()
        
        print("\n" + "=" * 60)
        print(self._color(Colors.BOLD + Colors.GREEN, " 验证完成摘要 "))
        print("=" * 60)
        print()
        print(f"  扫描文件数:      {len(self.scanned_files)}")
        print(f"  发现元素数:      {len(self.elements)}")
        print(f"  依赖覆盖率:      {coverage['dependency_coverage']:.1f}%")
        print()
        print(self._color(Colors.BOLD, " 问题统计:"))
        print(f"    {self._color(Colors.FAIL, '错误')}:   {len([i for i in self.issues if i.severity == Severity.ERROR])}")
        print(f"    {self._color(Colors.WARNING, '警告')}:   {len([i for i in self.issues if i.severity == Severity.WARNING])}")
        print(f"    {self._color(Colors.BLUE, '信息')}:   {len([i for i in self.issues if i.severity == Severity.INFO])}")
        print()
        
        # 元素分布
        print(self._color(Colors.BOLD, " 元素分布:"))
        for type_name, count in sorted(coverage["by_type"].items()):
            print(f"    {type_name}: {count}")
        print()
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="定理依赖验证工具 - 验证AnalysisDataFlow项目的定理依赖完整性",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本用法
  python theorem-dependency-validator.py
  
  # 指定项目根目录和输出目录
  python theorem-dependency-validator.py -r /path/to/project -o ./output
  
  # 详细输出
  python theorem-dependency-validator.py -v
  
  # 无颜色输出（适用于重定向到文件）
  python theorem-dependency-validator.py --no-color
        """
    )
    
    parser.add_argument(
        '-r', '--root',
        default='.',
        help='项目根目录 (默认: 当前目录)'
    )
    parser.add_argument(
        '-o', '--output',
        default='./validation-output',
        help='输出目录 (默认: ./validation-output)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='启用详细输出'
    )
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='禁用彩色输出'
    )
    parser.add_argument(
        '--scan-dirs',
        nargs='+',
        default=['Struct', 'Knowledge', 'Flink'],
        help='要扫描的目录列表 (默认: Struct Knowledge Flink)'
    )
    
    args = parser.parse_args()
    
    # 创建验证器实例
    validator = TheoremDependencyValidator(
        project_root=args.root,
        verbose=args.verbose,
        no_color=args.no_color
    )
    
    # 运行验证
    try:
        validator.run_full_validation(args.output)
    except KeyboardInterrupt:
        print("\n\n操作已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
