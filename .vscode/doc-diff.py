#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AnalysisDataFlow 文档差异分析工具

功能：
1. 文档变更检测 - 比较文档版本差异，识别新增/删除/修改的定理和定义
2. 交叉引用影响分析 - 检测文档变更对其他文档的影响
3. 变更分类统计 - 按类型分类变更，统计变更规模，生成变更日志建议
4. 质量回归检测 - 检测链接破坏、定理编号冲突、格式规范
5. 合并建议生成 - 分析PR的变更，生成合并建议，识别潜在冲突

使用方法：
    python .vscode/doc-diff.py --base <base_commit> --head <head_commit>
    python .vscode/doc-diff.py --pr <pr_number>
    python .vscode/doc-diff.py --files file1.md file2.md
    python .vscode/doc-diff.py --staged  # 检查暂存区变更
    python .vscode/doc-diff.py --json    # 输出JSON格式报告
    python .vscode/doc-diff.py --impact  # 分析交叉引用影响

作者: AnalysisDataFlow Project
版本: 1.0.0
"""

import os
import re
import sys
import json
import argparse
import subprocess
import difflib
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Set, Tuple, Optional, NamedTuple
from datetime import datetime
from enum import Enum
from collections import defaultdict


class ChangeType(Enum):
    """变更类型"""
    ADDED = "added"
    DELETED = "deleted"
    MODIFIED = "modified"
    RENAMED = "renamed"


class ElementType(Enum):
    """形式化元素类型"""
    THEOREM = "Thm"
    DEFINITION = "Def"
    LEMMA = "Lemma"
    PROPOSITION = "Prop"
    COROLLARY = "Cor"


class Severity(Enum):
    """问题严重程度"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class FormalElement:
    """形式化元素（定理/定义/引理/命题/推论）"""
    id: str
    element_type: str  # Def, Thm, Lemma, Prop, Cor
    stage: str  # S, K, F
    doc_num: str
    seq_num: str
    name: str
    content: str
    line_num: int
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if isinstance(other, FormalElement):
            return self.id == other.id
        return False


@dataclass
class CrossRef:
    """交叉引用"""
    source_file: str
    source_line: int
    ref_type: str  # link, theorem, definition, prerequisite
    target: str
    target_file: Optional[str] = None
    anchor: Optional[str] = None
    context: str = ""


@dataclass
class DocumentChange:
    """文档变更"""
    file_path: str
    change_type: ChangeType
    old_content: Optional[str] = None
    new_content: Optional[str] = None
    old_path: Optional[str] = None  # 用于重命名
    diff_stats: Dict = field(default_factory=dict)


@dataclass
class FormalElementChange:
    """形式化元素变更"""
    element: FormalElement
    change_type: ChangeType
    old_element: Optional[FormalElement] = None
    diff_content: Optional[str] = None


@dataclass
class ImpactAnalysis:
    """影响分析结果"""
    affected_files: List[str] = field(default_factory=list)
    broken_refs: List[CrossRef] = field(default_factory=list)
    outdated_refs: List[CrossRef] = field(default_factory=list)
    potential_conflicts: List[str] = field(default_factory=list)


@dataclass
class QualityIssue:
    """质量问题"""
    severity: Severity
    category: str
    message: str
    file_path: str
    line_num: Optional[int] = None
    suggestion: Optional[str] = None


@dataclass
class MergeRecommendation:
    """合并建议"""
    recommendation: str = "merge"  # merge, review, block
    confidence: float = 0.0  # 0.0 - 1.0
    reasons: List[str] = field(default_factory=list)
    suggested_actions: List[str] = field(default_factory=list)


@dataclass
class ChangeStatistics:
    """变更统计"""
    total_files_changed: int = 0
    files_added: int = 0
    files_deleted: int = 0
    files_modified: int = 0
    files_renamed: int = 0
    
    total_elements_changed: int = 0
    elements_added: int = 0
    elements_deleted: int = 0
    elements_modified: int = 0
    
    by_type: Dict[str, int] = field(default_factory=dict)
    by_stage: Dict[str, int] = field(default_factory=dict)
    by_category: Dict[str, int] = field(default_factory=dict)


@dataclass
class DiffReport:
    """差异分析报告"""
    timestamp: str
    base_ref: str
    head_ref: str
    
    document_changes: List[DocumentChange] = field(default_factory=list)
    element_changes: List[FormalElementChange] = field(default_factory=list)
    impact_analysis: ImpactAnalysis = field(default_factory=ImpactAnalysis)
    quality_issues: List[QualityIssue] = field(default_factory=list)
    statistics: ChangeStatistics = field(default_factory=ChangeStatistics)
    merge_recommendation: Optional[MergeRecommendation] = None
    changelog_suggestion: str = ""


class DocDiffAnalyzer:
    """文档差异分析器"""
    
    # 形式化元素编号正则 - 标准格式: **Def-S-01-01** 或 **Def-S-01-01 (名称)**
    ELEMENT_PATTERN = re.compile(
        r'\*\*\s*(Def|Thm|Lemma|Prop|Cor)-([SFK])-(\d{2})-(\d{2,3}[a-zA-Z]?)',
        re.IGNORECASE
    )
    
    # 元素名称正则（通常跟在编号后面）
    ELEMENT_NAME_PATTERN = re.compile(
        r'\*\*\s*(?:Def|Thm|Lemma|Prop|Cor)-[SFK]-\d{2}-\d{2,3}[a-zA-Z]?\s*\*\*\s*[:：]\s*([^\n]+)',
        re.IGNORECASE
    )
    
    # 表格中的元素引用 - 用于THEOREM-REGISTRY.md等
    TABLE_ELEMENT_PATTERN = re.compile(
        r'\|\s*(Def|Thm|Lemma|Prop|Cor)-([SFK])-(\d{2})-(\d{2,3}[a-zA-Z]?)\s*\|',
        re.IGNORECASE
    )
    
    # 文档中的中文定义格式: **定义 1.1 (名称)**
    CHINESE_DEF_PATTERN = re.compile(
        r'\*\*定义\s+(\d+)\.(\d+)\s*\(([^)]+)\)\s*\*\*',
        re.IGNORECASE
    )
    
    # 文档中的中文定理格式: **定理 X.X (名称)**
    CHINESE_THM_PATTERN = re.compile(
        r'\*\*定理\s+(\d+)\.(\d+)\s*\(([^)]+)\)\s*\*\*',
        re.IGNORECASE
    )
    
    # Markdown链接正则
    LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    
    # 定理/定义引用正则
    REF_PATTERN = re.compile(
        r'(Thm|Def|Lemma|Prop|Cor)-([SFK])-(\d{2})-(\d{2,3}[a-zA-Z]?)',
        re.IGNORECASE
    )
    
    # 文档头部元数据正则
    HEADER_META_PATTERN = re.compile(
        r'>\s*\*\*?所属阶段\*\*?:?\s*([^|]+)',
        re.IGNORECASE
    )
    PREREQ_META_PATTERN = re.compile(
        r'>\s*\*\*?前置依赖\*\*?:?\s*([^|]+)',
        re.IGNORECASE
    )
    FORMAL_LEVEL_PATTERN = re.compile(
        r'>\s*\*\*?形式化等级\*\*?:?\s*([^|]+)',
        re.IGNORECASE
    )
    
    # 六段式章节标题
    REQUIRED_SECTIONS = [
        "概念定义",
        "属性推导",
        "关系建立",
        "论证过程",
        "形式证明",
        "实例验证",
        "可视化",
        "引用参考"
    ]
    
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.report = DiffReport(
            timestamp=datetime.now().isoformat(),
            base_ref="",
            head_ref=""
        )
        self.all_elements: Dict[str, FormalElement] = {}
        self.all_refs: List[CrossRef] = []
        
    def run_git_command(self, args: List[str]) -> str:
        """运行Git命令"""
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.root_dir,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            if result.returncode != 0:
                print(f"Git命令错误: {result.stderr}", file=sys.stderr)
                return ""
            return result.stdout
        except Exception as e:
            print(f"运行Git命令失败: {e}", file=sys.stderr)
            return ""
    
    def get_changed_files(self, base_ref: str, head_ref: str) -> List[DocumentChange]:
        """获取变更的文件列表"""
        changes = []
        
        # 获取变更的文件列表
        output = self.run_git_command([
            "diff", "--name-status", base_ref, head_ref
        ])
        
        for line in output.strip().split('\n'):
            if not line:
                continue
            
            parts = line.split('\t')
            status = parts[0]
            
            if status.startswith('A'):
                # 新增
                changes.append(DocumentChange(
                    file_path=parts[1],
                    change_type=ChangeType.ADDED
                ))
            elif status.startswith('D'):
                # 删除
                changes.append(DocumentChange(
                    file_path=parts[1],
                    change_type=ChangeType.DELETED
                ))
            elif status.startswith('M'):
                # 修改
                changes.append(DocumentChange(
                    file_path=parts[1],
                    change_type=ChangeType.MODIFIED
                ))
            elif status.startswith('R'):
                # 重命名
                changes.append(DocumentChange(
                    file_path=parts[2],
                    change_type=ChangeType.RENAMED,
                    old_path=parts[1]
                ))
        
        return changes
    
    def get_file_content_at_ref(self, file_path: str, ref: str) -> Optional[str]:
        """获取文件在指定引用的内容"""
        output = self.run_git_command(["show", f"{ref}:{file_path}"])
        return output if output else None
    
    def get_staged_changes(self) -> List[DocumentChange]:
        """获取暂存区的变更"""
        changes = []
        
        output = self.run_git_command([
            "diff", "--cached", "--name-status"
        ])
        
        for line in output.strip().split('\n'):
            if not line:
                continue
            
            parts = line.split('\t')
            status = parts[0]
            
            if status.startswith('A'):
                changes.append(DocumentChange(
                    file_path=parts[1],
                    change_type=ChangeType.ADDED
                ))
            elif status.startswith('D'):
                changes.append(DocumentChange(
                    file_path=parts[1],
                    change_type=ChangeType.DELETED
                ))
            elif status.startswith('M'):
                changes.append(DocumentChange(
                    file_path=parts[1],
                    change_type=ChangeType.MODIFIED
                ))
        
        return changes
    
    def get_unstaged_changes(self) -> List[DocumentChange]:
        """获取未暂存的变更"""
        changes = []
        
        output = self.run_git_command([
            "diff", "--name-status"
        ])
        
        for line in output.strip().split('\n'):
            if not line:
                continue
            
            parts = line.split('\t')
            status = parts[0]
            
            if status.startswith('A'):
                changes.append(DocumentChange(
                    file_path=parts[1],
                    change_type=ChangeType.ADDED
                ))
            elif status.startswith('D'):
                changes.append(DocumentChange(
                    file_path=parts[1],
                    change_type=ChangeType.DELETED
                ))
            elif status.startswith('M'):
                changes.append(DocumentChange(
                    file_path=parts[1],
                    change_type=ChangeType.MODIFIED
                ))
        
        return changes
    
    def parse_formal_elements(self, content: str, file_path: str) -> List[FormalElement]:
        """解析文档中的形式化元素"""
        elements = []
        lines = content.split('\n')
        
        # 从文件路径推断阶段和文档编号
        inferred_stage = self._infer_stage_from_path(file_path)
        inferred_doc_num = self._infer_doc_num_from_path(file_path)
        
        for line_num, line in enumerate(lines, 1):
            # 匹配标准格式: **Def-S-01-01**
            matches = self.ELEMENT_PATTERN.finditer(line)
            for match in matches:
                element_type = match.group(1)
                stage = match.group(2)
                doc_num = match.group(3)
                seq_num = match.group(4)
                element_id = f"{element_type}-{stage}-{doc_num}-{seq_num}"
                
                # 尝试提取名称
                name = ""
                name_match = self.ELEMENT_NAME_PATTERN.search(line)
                if name_match:
                    name = name_match.group(1).strip()
                
                # 提取上下文（前后3行）
                context_start = max(0, line_num - 2)
                context_end = min(len(lines), line_num + 3)
                context = '\n'.join(lines[context_start:context_end])
                
                element = FormalElement(
                    id=element_id,
                    element_type=element_type,
                    stage=stage,
                    doc_num=doc_num,
                    seq_num=seq_num,
                    name=name,
                    content=context,
                    line_num=line_num
                )
                elements.append(element)
            
            # 匹配表格中的元素引用
            table_matches = self.TABLE_ELEMENT_PATTERN.finditer(line)
            for match in table_matches:
                element_type = match.group(1)
                stage = match.group(2)
                doc_num = match.group(3)
                seq_num = match.group(4)
                element_id = f"{element_type}-{stage}-{doc_num}-{seq_num}"
                
                context_start = max(0, line_num - 2)
                context_end = min(len(lines), line_num + 3)
                context = '\n'.join(lines[context_start:context_end])
                
                element = FormalElement(
                    id=element_id,
                    element_type=element_type,
                    stage=stage,
                    doc_num=doc_num,
                    seq_num=seq_num,
                    name="",
                    content=context,
                    line_num=line_num
                )
                if not any(e.id == element_id for e in elements):
                    elements.append(element)
        
        return elements
    
    def _infer_stage_from_path(self, file_path: str) -> str:
        """从文件路径推断阶段标识"""
        if 'Struct/' in file_path or file_path.startswith('Struct/'):
            return 'S'
        elif 'Knowledge/' in file_path or file_path.startswith('Knowledge/'):
            return 'K'
        elif 'Flink/' in file_path or file_path.startswith('Flink/'):
            return 'F'
        return 'S'
    
    def _infer_doc_num_from_path(self, file_path: str) -> str:
        """从文件路径推断文档编号"""
        # 尝试匹配类似 01.01 或 01-foundation 的格式
        match = re.search(r'(\d{2})[.-]', file_path)
        if match:
            return match.group(1)
        return '01'
    
    def extract_cross_refs(self, content: str, file_path: str) -> List[CrossRef]:
        """提取文档中的交叉引用"""
        refs = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # 跳过代码块
            if line.strip().startswith('```'):
                continue
            
            # 提取Markdown链接
            for match in self.LINK_PATTERN.finditer(line):
                link_text = match.group(1)
                link_target = match.group(2)
                
                ref = CrossRef(
                    source_file=file_path,
                    source_line=line_num,
                    ref_type="link",
                    target=link_target,
                    context=line.strip()
                )
                refs.append(ref)
            
            # 提取定理/定义引用
            for match in self.REF_PATTERN.finditer(line):
                ref_id = match.group(0)
                ref = CrossRef(
                    source_file=file_path,
                    source_line=line_num,
                    ref_type="element_ref",
                    target=ref_id,
                    context=line.strip()
                )
                refs.append(ref)
        
        return refs
    
    def analyze_element_changes(
        self,
        old_content: Optional[str],
        new_content: Optional[str],
        file_path: str
    ) -> List[FormalElementChange]:
        """分析形式化元素的变更"""
        changes = []
        
        old_elements = {}
        new_elements = {}
        
        if old_content:
            for elem in self.parse_formal_elements(old_content, file_path):
                old_elements[elem.id] = elem
        
        if new_content:
            for elem in self.parse_formal_elements(new_content, file_path):
                new_elements[elem.id] = elem
        
        # 检测新增的元素
        for elem_id, elem in new_elements.items():
            if elem_id not in old_elements:
                changes.append(FormalElementChange(
                    element=elem,
                    change_type=ChangeType.ADDED
                ))
            elif old_elements[elem_id].content != elem.content:
                # 内容有变化
                diff = self.generate_diff(
                    old_elements[elem_id].content,
                    elem.content,
                    elem_id
                )
                changes.append(FormalElementChange(
                    element=elem,
                    change_type=ChangeType.MODIFIED,
                    old_element=old_elements[elem_id],
                    diff_content=diff
                ))
        
        # 检测删除的元素
        for elem_id, elem in old_elements.items():
            if elem_id not in new_elements:
                changes.append(FormalElementChange(
                    element=elem,
                    change_type=ChangeType.DELETED
                ))
        
        return changes
    
    def generate_diff(self, old_content: str, new_content: str, label: str) -> str:
        """生成差异内容"""
        old_lines = old_content.split('\n')
        new_lines = new_content.split('\n')
        
        diff = difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=f"{label}(old)",
            tofile=f"{label}(new)",
            lineterm=''
        )
        
        return '\n'.join(diff)
    
    def analyze_cross_ref_impact(
        self,
        changes: List[DocumentChange],
        element_changes: List[FormalElementChange]
    ) -> ImpactAnalysis:
        """分析交叉引用影响"""
        impact = ImpactAnalysis()
        
        # 收集所有被删除或修改的元素ID
        affected_elements = set()
        for change in element_changes:
            if change.change_type in [ChangeType.DELETED, ChangeType.MODIFIED]:
                affected_elements.add(change.element.id)
        
        # 收集所有被删除或重命名的文件
        affected_files = set()
        for change in changes:
            if change.change_type in [ChangeType.DELETED, ChangeType.RENAMED]:
                affected_files.add(change.file_path)
            if change.old_path:
                affected_files.add(change.old_path)
        
        # 扫描所有文档，检查是否有引用被影响
        for md_file in self.root_dir.glob('**/*.md'):
            rel_path = str(md_file.relative_to(self.root_dir))
            
            # 跳过根目录的特殊文件
            if md_file.parent == self.root_dir:
                continue
            
            try:
                content = md_file.read_text(encoding='utf-8')
                refs = self.extract_cross_refs(content, rel_path)
                
                for ref in refs:
                    # 检查是否引用了被删除的元素
                    if ref.target in affected_elements:
                        impact.broken_refs.append(ref)
                        if rel_path not in impact.affected_files:
                            impact.affected_files.append(rel_path)
                    
                    # 检查是否引用了被删除的文件
                    if ref.ref_type == "link":
                        target_file = ref.target.split('#')[0]
                        if target_file in affected_files:
                            impact.broken_refs.append(ref)
                            if rel_path not in impact.affected_files:
                                impact.affected_files.append(rel_path)
            
            except Exception as e:
                print(f"读取文件失败 {rel_path}: {e}", file=sys.stderr)
        
        return impact
    
    def check_quality_regression(
        self,
        changes: List[DocumentChange],
        element_changes: List[FormalElementChange]
    ) -> List[QualityIssue]:
        """检查质量回归"""
        issues = []
        
        # 检查定理编号冲突
        all_element_ids: Dict[str, List[str]] = defaultdict(list)
        
        for change in changes:
            if change.change_type == ChangeType.ADDED:
                # 读取新文件内容
                file_path = self.root_dir / change.file_path
                if file_path.exists():
                    try:
                        content = file_path.read_text(encoding='utf-8')
                        elements = self.parse_formal_elements(content, change.file_path)
                        for elem in elements:
                            all_element_ids[elem.id].append(change.file_path)
                    except Exception:
                        pass
        
        for elem_id, files in all_element_ids.items():
            if len(files) > 1:
                issues.append(QualityIssue(
                    severity=Severity.CRITICAL,
                    category="编号冲突",
                    message=f"元素编号 {elem_id} 在多个文件中重复定义",
                    file_path=files[0],
                    suggestion=f"请确保 {elem_id} 在所有文档中唯一，涉及文件: {', '.join(files)}"
                ))
        
        # 检查格式规范
        for change in changes:
            if change.change_type in [ChangeType.ADDED, ChangeType.MODIFIED]:
                file_path = self.root_dir / change.file_path
                if file_path.exists():
                    try:
                        content = file_path.read_text(encoding='utf-8')
                        issues.extend(self._check_document_format(content, change.file_path))
                    except Exception:
                        pass
        
        # 检查删除元素的影响
        for elem_change in element_changes:
            if elem_change.change_type == ChangeType.DELETED:
                issues.append(QualityIssue(
                    severity=Severity.HIGH,
                    category="元素删除",
                    message=f"元素 {elem_change.element.id} 被删除，可能影响其他文档的引用",
                    file_path=elem_change.element.id,
                    suggestion=f"检查并更新所有引用 {elem_change.element.id} 的文档"
                ))
        
        return issues
    
    def _check_document_format(self, content: str, file_path: str) -> List[QualityIssue]:
        """检查文档格式规范"""
        issues = []
        lines = content.split('\n')
        
        # 检查六段式结构
        has_sections = {section: False for section in self.REQUIRED_SECTIONS}
        
        for line in lines:
            for section in self.REQUIRED_SECTIONS:
                if f"## " in line and section in line:
                    has_sections[section] = True
        
        # 对于主要文档，要求有基本章节
        if file_path.endswith('.md') and not file_path.endswith('INDEX.md'):
            missing_sections = [s for s, v in has_sections.items() if not v]
            if len(missing_sections) > 4:  # 允许缺失大部分（可能是特殊文档）
                issues.append(QualityIssue(
                    severity=Severity.LOW,
                    category="格式规范",
                    message=f"文档可能缺少标准章节结构",
                    file_path=file_path,
                    suggestion=f"建议添加以下章节: {', '.join(missing_sections[:3])}"
                ))
        
        # 检查是否有Mermaid图
        if '```mermaid' not in content:
            issues.append(QualityIssue(
                severity=Severity.LOW,
                category="可视化",
                message="文档缺少Mermaid可视化图表",
                file_path=file_path,
                suggestion="建议添加至少一个Mermaid图表（思维导图/层次图/流程图等）"
            ))
        
        # 检查引用格式
        ref_pattern = re.compile(r'\[\^(\d+)\]')
        refs = ref_pattern.findall(content)
        if refs and "## 引用参考" not in content:
            issues.append(QualityIssue(
                severity=Severity.MEDIUM,
                category="引用格式",
                message="文档使用了引用标记但可能缺少引用参考章节",
                file_path=file_path,
                suggestion="添加 '## 引用参考' 章节并在其中列出所有引用"
            ))
        
        return issues
    
    def calculate_statistics(
        self,
        changes: List[DocumentChange],
        element_changes: List[FormalElementChange]
    ) -> ChangeStatistics:
        """计算变更统计"""
        stats = ChangeStatistics()
        
        # 文件统计
        stats.total_files_changed = len(changes)
        for change in changes:
            if change.change_type == ChangeType.ADDED:
                stats.files_added += 1
            elif change.change_type == ChangeType.DELETED:
                stats.files_deleted += 1
            elif change.change_type == ChangeType.MODIFIED:
                stats.files_modified += 1
            elif change.change_type == ChangeType.RENAMED:
                stats.files_renamed += 1
        
        # 元素统计
        stats.total_elements_changed = len(element_changes)
        for change in element_changes:
            if change.change_type == ChangeType.ADDED:
                stats.elements_added += 1
            elif change.change_type == ChangeType.DELETED:
                stats.elements_deleted += 1
            elif change.change_type == ChangeType.MODIFIED:
                stats.elements_modified += 1
            
            # 按类型统计
            elem_type = change.element.element_type
            stats.by_type[elem_type] = stats.by_type.get(elem_type, 0) + 1
            
            # 按阶段统计
            stage = change.element.stage
            stats.by_stage[stage] = stats.by_stage.get(stage, 0) + 1
        
        # 按类别分类
        for change in changes:
            if 'Struct/' in change.file_path:
                stats.by_category['理论'] = stats.by_category.get('理论', 0) + 1
            elif 'Knowledge/' in change.file_path:
                stats.by_category['实践'] = stats.by_category.get('实践', 0) + 1
            elif 'Flink/' in change.file_path:
                stats.by_category['Flink'] = stats.by_category.get('Flink', 0) + 1
        
        return stats
    
    def generate_merge_recommendation(
        self,
        changes: List[DocumentChange],
        element_changes: List[FormalElementChange],
        impact: ImpactAnalysis,
        issues: List[QualityIssue]
    ) -> MergeRecommendation:
        """生成合并建议"""
        recommendation = MergeRecommendation()
        
        critical_issues = [i for i in issues if i.severity == Severity.CRITICAL]
        high_issues = [i for i in issues if i.severity == Severity.HIGH]
        
        # 判断建议
        if critical_issues:
            recommendation.recommendation = "block"
            recommendation.confidence = 0.95
            recommendation.reasons.append(f"发现 {len(critical_issues)} 个严重问题需要修复")
        elif high_issues or len(impact.broken_refs) > 5:
            recommendation.recommendation = "review"
            recommendation.confidence = 0.75
            if high_issues:
                recommendation.reasons.append(f"发现 {len(high_issues)} 个高风险问题")
            if impact.broken_refs:
                recommendation.reasons.append(f"发现 {len(impact.broken_refs)} 个断裂的交叉引用")
        else:
            recommendation.recommendation = "merge"
            recommendation.confidence = 0.9
            recommendation.reasons.append("未发现严重问题，变更健康")
        
        # 建议行动
        if critical_issues:
            recommendation.suggested_actions.append("修复所有严重问题后再合并")
        if impact.broken_refs:
            recommendation.suggested_actions.append("更新或修复断裂的交叉引用")
        if any(e.change_type == ChangeType.DELETED for e in element_changes):
            recommendation.suggested_actions.append("确认删除的元素是否被其他文档引用")
        if any(c.change_type == ChangeType.ADDED for c in changes):
            recommendation.suggested_actions.append("考虑更新 THEOREM-REGISTRY.md 注册新元素")
        
        return recommendation
    
    def generate_changelog_suggestion(self, stats: ChangeStatistics, element_changes: List[FormalElementChange]) -> str:
        """生成变更日志建议"""
        lines = []
        lines.append("### 建议变更日志")
        lines.append("")
        
        # 新增
        added_elements = [e for e in element_changes if e.change_type == ChangeType.ADDED]
        if added_elements:
            lines.append("#### ✨ 新增")
            for change in added_elements[:5]:  # 最多显示5个
                elem = change.element
                lines.append(f"- **{elem.id}**: {elem.name or '新元素'}")
            if len(added_elements) > 5:
                lines.append(f"- 以及 {len(added_elements) - 5} 个其他新增元素...")
            lines.append("")
        
        # 修改
        modified_elements = [e for e in element_changes if e.change_type == ChangeType.MODIFIED]
        if modified_elements:
            lines.append("#### 🔄 改进")
            for change in modified_elements[:3]:
                elem = change.element
                lines.append(f"- **{elem.id}**: 优化了定义/证明")
            if len(modified_elements) > 3:
                lines.append(f"- 以及 {len(modified_elements) - 3} 个其他改进...")
            lines.append("")
        
        # 统计
        lines.append("#### 📊 统计")
        lines.append(f"- 新增: {stats.elements_added} 个形式化元素")
        lines.append(f"- 修改: {stats.elements_modified} 个形式化元素")
        lines.append(f"- 删除: {stats.elements_deleted} 个形式化元素")
        lines.append(f"- 文件变更: {stats.total_files_changed} 个")
        
        return '\n'.join(lines)
    
    def analyze(
        self,
        base_ref: str,
        head_ref: str,
        include_impact: bool = True
    ) -> DiffReport:
        """执行完整的差异分析"""
        self.report.base_ref = base_ref
        self.report.head_ref = head_ref
        
        print(f"🔍 分析变更: {base_ref}..{head_ref}")
        
        # 1. 获取文档变更
        print("  📄 扫描文档变更...")
        doc_changes = self.get_changed_files(base_ref, head_ref)
        self.report.document_changes = doc_changes
        print(f"     发现 {len(doc_changes)} 个文件变更")
        
        # 2. 分析形式化元素变更
        print("  🧮 分析形式化元素变更...")
        all_element_changes = []
        for change in doc_changes:
            if change.file_path.endswith('.md'):
                old_content = self.get_file_content_at_ref(change.file_path, base_ref)
                new_content = self.get_file_content_at_ref(change.file_path, head_ref)
                
                if change.change_type == ChangeType.ADDED:
                    old_content = None
                elif change.change_type == ChangeType.DELETED:
                    new_content = None
                
                element_changes = self.analyze_element_changes(
                    old_content, new_content, change.file_path
                )
                all_element_changes.extend(element_changes)
        
        self.report.element_changes = all_element_changes
        print(f"     发现 {len(all_element_changes)} 个形式化元素变更")
        
        # 3. 交叉引用影响分析
        if include_impact:
            print("  🔗 分析交叉引用影响...")
            impact = self.analyze_cross_ref_impact(doc_changes, all_element_changes)
            self.report.impact_analysis = impact
            print(f"     影响 {len(impact.affected_files)} 个文件，{len(impact.broken_refs)} 个断裂引用")
        
        # 4. 质量回归检测
        print("  ✅ 检查质量回归...")
        issues = self.check_quality_regression(doc_changes, all_element_changes)
        self.report.quality_issues = issues
        critical_count = len([i for i in issues if i.severity == Severity.CRITICAL])
        high_count = len([i for i in issues if i.severity == Severity.HIGH])
        print(f"     发现 {critical_count} 个严重问题，{high_count} 个高风险问题")
        
        # 5. 计算统计
        print("  📊 计算变更统计...")
        stats = self.calculate_statistics(doc_changes, all_element_changes)
        self.report.statistics = stats
        
        # 6. 生成合并建议
        print("  💡 生成合并建议...")
        recommendation = self.generate_merge_recommendation(
            doc_changes, all_element_changes, self.report.impact_analysis, issues
        )
        self.report.merge_recommendation = recommendation
        
        # 7. 生成变更日志建议
        self.report.changelog_suggestion = self.generate_changelog_suggestion(stats, all_element_changes)
        
        return self.report
    
    def analyze_staged(self, include_impact: bool = True) -> DiffReport:
        """分析暂存区的变更"""
        self.report.base_ref = "HEAD"
        self.report.head_ref = "STAGED"
        
        print("🔍 分析暂存区变更")
        
        # 获取暂存区变更
        doc_changes = self.get_staged_changes()
        self.report.document_changes = doc_changes
        
        # 分析形式化元素变更
        all_element_changes = []
        for change in doc_changes:
            if change.file_path.endswith('.md'):
                # 获取HEAD版本的内容
                old_content = self.get_file_content_at_ref(change.file_path, "HEAD")
                
                # 获取暂存区内容
                file_path = self.root_dir / change.file_path
                new_content = None
                if file_path.exists():
                    new_content = file_path.read_text(encoding='utf-8')
                
                element_changes = self.analyze_element_changes(
                    old_content, new_content, change.file_path
                )
                all_element_changes.extend(element_changes)
        
        self.report.element_changes = all_element_changes
        
        # 其他分析步骤
        if include_impact:
            self.report.impact_analysis = self.analyze_cross_ref_impact(doc_changes, all_element_changes)
        
        self.report.quality_issues = self.check_quality_regression(doc_changes, all_element_changes)
        self.report.statistics = self.calculate_statistics(doc_changes, all_element_changes)
        self.report.merge_recommendation = self.generate_merge_recommendation(
            doc_changes, all_element_changes, self.report.impact_analysis, self.report.quality_issues
        )
        self.report.changelog_suggestion = self.generate_changelog_suggestion(
            self.report.statistics, all_element_changes
        )
        
        return self.report
    
    def analyze_files(self, file_paths: List[str]) -> DiffReport:
        """分析指定文件的当前变更"""
        self.report.base_ref = "WORKING"
        self.report.head_ref = "CURRENT"
        
        print(f"🔍 分析指定文件: {', '.join(file_paths)}")
        
        doc_changes = []
        all_element_changes = []
        
        for file_path in file_paths:
            if not file_path.endswith('.md'):
                continue
            
            full_path = self.root_dir / file_path
            if not full_path.exists():
                continue
            
            # 获取当前内容
            new_content = full_path.read_text(encoding='utf-8')
            
            # 尝试获取Git版本的内容作为对比
            old_content = self.get_file_content_at_ref(file_path, "HEAD")
            
            change_type = ChangeType.MODIFIED if old_content else ChangeType.ADDED
            
            doc_changes.append(DocumentChange(
                file_path=file_path,
                change_type=change_type
            ))
            
            element_changes = self.analyze_element_changes(
                old_content, new_content, file_path
            )
            all_element_changes.extend(element_changes)
        
        self.report.document_changes = doc_changes
        self.report.element_changes = all_element_changes
        self.report.impact_analysis = self.analyze_cross_ref_impact(doc_changes, all_element_changes)
        self.report.quality_issues = self.check_quality_regression(doc_changes, all_element_changes)
        self.report.statistics = self.calculate_statistics(doc_changes, all_element_changes)
        self.report.merge_recommendation = self.generate_merge_recommendation(
            doc_changes, all_element_changes, self.report.impact_analysis, self.report.quality_issues
        )
        self.report.changelog_suggestion = self.generate_changelog_suggestion(
            self.report.statistics, all_element_changes
        )
        
        return self.report


def format_severity(severity: Severity) -> str:
    """格式化严重级别"""
    colors = {
        Severity.CRITICAL: "🔴",
        Severity.HIGH: "🟠",
        Severity.MEDIUM: "🟡",
        Severity.LOW: "🔵",
        Severity.INFO: "⚪"
    }
    return f"{colors.get(severity, '⚪')} {severity.value.upper()}"


def format_change_type(change_type: ChangeType) -> str:
    """格式化变更类型"""
    icons = {
        ChangeType.ADDED: "➕",
        ChangeType.DELETED: "➖",
        ChangeType.MODIFIED: "📝",
        ChangeType.RENAMED: "📛"
    }
    return f"{icons.get(change_type, '❓')} {change_type.value.upper()}"


def print_report(report: DiffReport, output_json: bool = False):
    """打印报告"""
    if output_json:
        # 转换为JSON可序列化的格式
        def serialize(obj):
            if isinstance(obj, Enum):
                return obj.value
            if isinstance(obj, (datetime,)):
                return obj.isoformat()
            if isinstance(obj, list):
                return [serialize(item) for item in obj]
            if isinstance(obj, dict):
                return {k: serialize(v) for k, v in obj.items()}
            if hasattr(obj, '__dataclass_fields__'):
                return {k: serialize(v) for k, v in obj.__dict__.items()}
            return obj
        
        print(json.dumps(serialize(report), indent=2, ensure_ascii=False))
        return
    
    # 打印文本报告
    print("\n" + "=" * 80)
    print("📋 AnalysisDataFlow 文档差异分析报告")
    print("=" * 80)
    print(f"时间: {report.timestamp}")
    print(f"对比: {report.base_ref} → {report.head_ref}")
    print()
    
    # 变更统计
    print("-" * 80)
    print("📊 变更统计")
    print("-" * 80)
    stats = report.statistics
    print(f"  文件变更: {stats.total_files_changed} 个")
    print(f"    - 新增: {stats.files_added}")
    print(f"    - 删除: {stats.files_deleted}")
    print(f"    - 修改: {stats.files_modified}")
    print(f"    - 重命名: {stats.files_renamed}")
    print()
    print(f"  形式化元素变更: {stats.total_elements_changed} 个")
    print(f"    - 新增: {stats.elements_added}")
    print(f"    - 删除: {stats.elements_deleted}")
    print(f"    - 修改: {stats.elements_modified}")
    print()
    
    if stats.by_type:
        print("  按类型分布:")
        for elem_type, count in sorted(stats.by_type.items()):
            print(f"    - {elem_type}: {count}")
        print()
    
    if stats.by_category:
        print("  按类别分布:")
        for category, count in sorted(stats.by_category.items(), key=lambda x: -x[1]):
            print(f"    - {category}: {count}")
        print()
    
    # 文档变更详情
    if report.document_changes:
        print("-" * 80)
        print("📄 文档变更详情")
        print("-" * 80)
        for change in report.document_changes:
            print(f"  {format_change_type(change.change_type)} {change.file_path}")
        print()
    
    # 形式化元素变更
    if report.element_changes:
        print("-" * 80)
        print("🧮 形式化元素变更")
        print("-" * 80)
        
        added = [e for e in report.element_changes if e.change_type == ChangeType.ADDED]
        deleted = [e for e in report.element_changes if e.change_type == ChangeType.DELETED]
        modified = [e for e in report.element_changes if e.change_type == ChangeType.MODIFIED]
        
        if added:
            print("\n  ➕ 新增元素:")
            for change in added:
                elem = change.element
                print(f"    - {elem.id}: {elem.name or '(未命名)'}")
        
        if deleted:
            print("\n  ➖ 删除元素:")
            for change in deleted:
                elem = change.element
                print(f"    - {elem.id}: {elem.name or '(未命名)'}")
        
        if modified:
            print("\n  📝 修改元素:")
            for change in modified:
                elem = change.element
                print(f"    - {elem.id}: {elem.name or '(未命名)'}")
        print()
    
    # 影响分析
    impact = report.impact_analysis
    if impact.affected_files or impact.broken_refs:
        print("-" * 80)
        print("🔗 交叉引用影响分析")
        print("-" * 80)
        print(f"  受影响文件: {len(impact.affected_files)} 个")
        if impact.affected_files:
            for f in impact.affected_files[:5]:
                print(f"    - {f}")
            if len(impact.affected_files) > 5:
                print(f"    ... 以及 {len(impact.affected_files) - 5} 个其他文件")
        print()
        print(f"  断裂引用: {len(impact.broken_refs)} 个")
        if impact.broken_refs:
            for ref in impact.broken_refs[:5]:
                print(f"    - {ref.source_file}:{ref.source_line} → {ref.target}")
            if len(impact.broken_refs) > 5:
                print(f"    ... 以及 {len(impact.broken_refs) - 5} 个其他引用")
        print()
    
    # 质量问题
    if report.quality_issues:
        print("-" * 80)
        print("⚠️  质量问题")
        print("-" * 80)
        
        # 按严重级别分组
        issues_by_severity = defaultdict(list)
        for issue in report.quality_issues:
            issues_by_severity[issue.severity].append(issue)
        
        for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
            if severity in issues_by_severity:
                issues = issues_by_severity[severity]
                print(f"\n  {format_severity(severity)} ({len(issues)} 个问题)")
                for issue in issues[:3]:
                    print(f"    [{issue.category}] {issue.message}")
                    if issue.suggestion:
                        print(f"    💡 建议: {issue.suggestion}")
                if len(issues) > 3:
                    print(f"    ... 以及 {len(issues) - 3} 个其他问题")
        print()
    
    # 合并建议
    if report.merge_recommendation:
        print("-" * 80)
        print("💡 合并建议")
        print("-" * 80)
        rec = report.merge_recommendation
        
        icons = {
            "merge": "✅",
            "review": "⚠️",
            "block": "❌"
        }
        print(f"  建议: {icons.get(rec.recommendation, '❓')} {rec.recommendation.upper()}")
        print(f"  置信度: {rec.confidence * 100:.0f}%")
        print()
        
        if rec.reasons:
            print("  原因:")
            for reason in rec.reasons:
                print(f"    - {reason}")
            print()
        
        if rec.suggested_actions:
            print("  建议行动:")
            for action in rec.suggested_actions:
                print(f"    - {action}")
            print()
    
    # 变更日志建议
    if report.changelog_suggestion:
        print("-" * 80)
        print(report.changelog_suggestion)
        print()
    
    print("=" * 80)
    print("分析完成")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="AnalysisDataFlow 文档差异分析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python .vscode/doc-diff.py --base main --head feature-branch
  python .vscode/doc-diff.py --staged
  python .vscode/doc-diff.py --files Struct/01-foundation/01.01-ustm.md
  python .vscode/doc-diff.py --base HEAD~1 --head HEAD --json
        """
    )
    
    parser.add_argument(
        "--base",
        default="HEAD",
        help="基准引用 (默认: HEAD)"
    )
    parser.add_argument(
        "--head",
        default="",
        help="目标引用 (默认: 工作目录)"
    )
    parser.add_argument(
        "--staged",
        action="store_true",
        help="分析暂存区的变更"
    )
    parser.add_argument(
        "--files",
        nargs="+",
        help="分析指定的文件"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="输出JSON格式报告"
    )
    parser.add_argument(
        "--no-impact",
        action="store_true",
        help="跳过影响分析（加快速度）"
    )
    parser.add_argument(
        "--root",
        default=".",
        help="项目根目录 (默认: 当前目录)"
    )
    
    args = parser.parse_args()
    
    # 确定项目根目录
    root_dir = Path(args.root).resolve()
    if not (root_dir / "Struct").exists():
        # 尝试从脚本位置确定
        script_dir = Path(__file__).parent.parent
        if (script_dir / "Struct").exists():
            root_dir = script_dir
    
    # 创建分析器
    analyzer = DocDiffAnalyzer(str(root_dir))
    
    # 执行分析
    if args.staged:
        report = analyzer.analyze_staged(include_impact=not args.no_impact)
    elif args.files:
        report = analyzer.analyze_files(args.files)
    else:
        head_ref = args.head or "HEAD"
        report = analyzer.analyze(args.base, head_ref, include_impact=not args.no_impact)
    
    # 打印报告
    print_report(report, output_json=args.json)
    
    # 返回适当的退出码
    if report.merge_recommendation:
        if report.merge_recommendation.recommendation == "block":
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
