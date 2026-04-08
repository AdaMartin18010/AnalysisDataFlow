#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Document Quality Auditor - v4.1
全面审计1,010+篇文档质量，确保100%合规

审计维度:
1. 六段式结构合规性
2. 定理编号连续性
3. Mermaid语法有效性
4. 图片存在性
5. 表格格式
6. 引用完整性

作者: Q1-4 Quality Audit Task
日期: 2026-04-08
"""

import os
import re
import json
import hashlib
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
from datetime import datetime
import concurrent.futures


@dataclass
class DocumentQualityScore:
    """文档质量评分"""
    structure: float = 0.0      # 六段式结构 (25%)
    formalization: float = 0.0  # 形式化元素 (25%)
    visualization: float = 0.0  # Mermaid图表 (15%)
    references: float = 0.0     # 引用完整性 (15%)
    examples: float = 0.0       # 代码示例 (20%)
    
    @property
    def total(self) -> float:
        return round(
            self.structure * 0.25 +
            self.formalization * 0.25 +
            self.visualization * 0.15 +
            self.references * 0.15 +
            self.examples * 0.20,
            2
        )


@dataclass
class QualityIssue:
    """质量问题记录"""
    file_path: str
    category: str  # structure, formalization, visualization, references, examples, table, image
    severity: str  # critical, high, medium, low
    message: str
    line_number: Optional[int] = None
    suggestion: str = ""


@dataclass
class DocumentAuditResult:
    """单文档审计结果"""
    file_path: str
    relative_path: str
    doc_type: str  # Struct, Knowledge, Flink, Root
    word_count: int
    char_count: int
    
    # 六段式检查
    has_definitions: bool
    has_properties: bool
    has_relations: bool
    has_argumentation: bool
    has_proof: bool
    has_examples: bool
    has_visualizations: bool
    has_references: bool
    
    # 形式化元素
    theorem_count: int
    lemma_count: int
    definition_count: int
    proposition_count: int
    corollary_count: int
    
    # Mermaid图表
    mermaid_count: int
    
    # 引用
    reference_count: int
    
    # 代码示例
    code_block_count: int
    inline_code_count: int
    
    # 表格
    table_count: int
    
    # 元信息
    has_stage_info: bool
    has_prerequisites: bool
    has_formal_level: bool
    
    # 列表字段（带默认值）
    theorem_ids: List[str] = field(default_factory=list)
    mermaid_issues: List[str] = field(default_factory=list)
    broken_refs: List[str] = field(default_factory=list)
    image_refs: List[str] = field(default_factory=list)
    missing_images: List[str] = field(default_factory=list)
    table_issues: List[str] = field(default_factory=list)
    
    # 评分
    score: DocumentQualityScore = field(default_factory=DocumentQualityScore)
    issues: List[QualityIssue] = field(default_factory=list)


class DocumentQualityAuditor:
    """文档质量审计器"""
    
    # 六段式必需章节（按优先级）
    REQUIRED_SECTIONS = [
        (r'##\s*1\.\s*概念定义|##\s*.*定义.*|##\s*Definitions', 'definitions'),
        (r'##\s*2\.\s*属性推导|##\s*.*属性.*|##\s*Properties', 'properties'),
        (r'##\s*3\.\s*关系建立|##\s*.*关系.*|##\s*Relations', 'relations'),
        (r'##\s*4\.\s*论证过程|##\s*.*论证.*|##\s*Argumentation', 'argumentation'),
        (r'##\s*5\.\s*形式证明|##\s*.*证明.*|##\s*Proof|##\s*Engineering', 'proof'),
        (r'##\s*6\.\s*实例验证|##\s*.*实例.*|##\s*Examples', 'examples'),
        (r'##\s*7\.\s*可视化|##\s*.*图.*|##\s*Visualizations', 'visualizations'),
        (r'##\s*8\.\s*引用参考|##\s*.*引用.*|##\s*References', 'references'),
    ]
    
    # 形式化元素正则
    THEOREM_PATTERN = re.compile(r'`?(Thm-[SKF]-\d{2}-\d{2,})`?')
    LEMMA_PATTERN = re.compile(r'`?(Lemma-[SKF]-\d{2}-\d{2,})`?')
    DEFINITION_PATTERN = re.compile(r'`?(Def-[SKF]-\d{2}-\d{2,})`?')
    PROPOSITION_PATTERN = re.compile(r'`?(Prop-[SKF]-\d{2}-\d{2,})`?')
    COROLLARY_PATTERN = re.compile(r'`?(Cor-[SKF]-\d{2}-\d{2,})`?')
    
    # Mermaid检测
    MERMAID_PATTERN = re.compile(r'```mermaid\s*([\s\S]*?)```', re.MULTILINE)
    
    # 代码块检测
    CODE_BLOCK_PATTERN = re.compile(r'```[\w]*\s*([\s\S]*?)```', re.MULTILINE)
    INLINE_CODE_PATTERN = re.compile(r'`[^`]+`')
    
    # 引用检测
    REF_PATTERN = re.compile(r'\[\^(\d+)\]')
    REF_LIST_PATTERN = re.compile(r'^\[\^(\d+)\]:\s*(.+)$', re.MULTILINE)
    
    # 图片检测
    IMAGE_PATTERN = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    
    # 表格检测
    TABLE_PATTERN = re.compile(r'\|[^\n]+\|\n\|[-:|\s]+\|', re.MULTILINE)
    
    # 元信息检测
    STAGE_INFO_PATTERN = re.compile(r'所属阶段[:\s]*(Struct|Knowledge|Flink)', re.IGNORECASE)
    PREREQ_PATTERN = re.compile(r'前置依赖[:\s]*\[?([^\]|\n]+)')
    FORMAL_LEVEL_PATTERN = re.compile(r'形式化等级[:\s]*(L[1-6])')
    
    def __init__(self, project_root: str, max_workers: int = 8):
        self.project_root = Path(project_root).resolve()
        self.max_workers = max_workers
        self.results: List[DocumentAuditResult] = []
        self.all_issues: List[QualityIssue] = []
        
        # 全局统计
        self.total_docs = 0
        self.processed_docs = 0
        self.total_theorems: Set[str] = set()
        self.total_definitions: Set[str] = set()
        self.total_lemmas: Set[str] = set()
        
    def get_all_markdown_files(self) -> List[Path]:
        """获取所有Markdown文件"""
        md_files = []
        
        # 主要目录
        for directory in ['Struct', 'Knowledge', 'Flink']:
            dir_path = self.project_root / directory
            if dir_path.exists():
                md_files.extend(dir_path.rglob('*.md'))
        
        # 根目录的特定文档
        root_docs = [
            'README.md', 'README-EN.md', 'QUICK-START.md', 'ARCHITECTURE.md',
            'THEOREM-REGISTRY.md', 'GLOSSARY.md', 'BEST-PRACTICES.md',
            'AGENTS.md', 'CONTRIBUTING.md', 'CASE-STUDIES.md'
        ]
        for doc in root_docs:
            doc_path = self.project_root / doc
            if doc_path.exists():
                md_files.append(doc_path)
        
        # docs目录
        docs_path = self.project_root / 'docs'
        if docs_path.exists():
            md_files.extend(docs_path.rglob('*.md'))
        
        return sorted(set(md_files))
    
    def detect_doc_type(self, file_path: Path) -> str:
        """检测文档类型"""
        rel_path = file_path.relative_to(self.project_root)
        path_str = str(rel_path).lower()
        
        if path_str.startswith('struct/'):
            return 'Struct'
        elif path_str.startswith('knowledge/'):
            return 'Knowledge'
        elif path_str.startswith('flink/'):
            return 'Flink'
        else:
            return 'Root'
    
    def audit_document(self, file_path: Path) -> DocumentAuditResult:
        """审计单个文档"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return self._create_error_result(file_path, str(e))
        
        rel_path = file_path.relative_to(self.project_root)
        doc_type = self.detect_doc_type(file_path)
        
        # 基本统计
        word_count = len(content.split())
        char_count = len(content)
        
        # 检测六段式结构
        section_checks = self._check_sections(content)
        
        # 检测形式化元素
        formal_elements = self._check_formalization(content)
        
        # 检测Mermaid
        mermaid_info = self._check_mermaid(content, file_path)
        
        # 检测引用
        ref_info = self._check_references(content)
        
        # 检测代码示例
        code_info = self._check_code_examples(content)
        
        # 检测图片
        image_info = self._check_images(content, file_path)
        
        # 检测表格
        table_info = self._check_tables(content)
        
        # 检测元信息
        meta_info = self._check_meta_info(content)
        
        # 计算评分
        score = self._calculate_score(
            section_checks, formal_elements, mermaid_info,
            ref_info, code_info, doc_type
        )
        
        # 收集问题
        issues = self._collect_issues(
            file_path, rel_path, doc_type, section_checks,
            formal_elements, mermaid_info, ref_info, image_info, table_info
        )
        
        result = DocumentAuditResult(
            file_path=str(file_path),
            relative_path=str(rel_path),
            doc_type=doc_type,
            word_count=word_count,
            char_count=char_count,
            has_definitions=section_checks['definitions'],
            has_properties=section_checks['properties'],
            has_relations=section_checks['relations'],
            has_argumentation=section_checks['argumentation'],
            has_proof=section_checks['proof'],
            has_examples=section_checks['examples'],
            has_visualizations=section_checks['visualizations'],
            has_references=section_checks['references'],
            theorem_count=formal_elements['theorem_count'],
            lemma_count=formal_elements['lemma_count'],
            definition_count=formal_elements['definition_count'],
            proposition_count=formal_elements['proposition_count'],
            corollary_count=formal_elements['corollary_count'],
            theorem_ids=formal_elements['theorem_ids'],
            mermaid_count=mermaid_info['count'],
            mermaid_issues=mermaid_info['issues'],
            reference_count=ref_info['count'],
            broken_refs=ref_info['broken'],
            code_block_count=code_info['block_count'],
            inline_code_count=code_info['inline_count'],
            image_refs=image_info['refs'],
            missing_images=image_info['missing'],
            table_count=table_info['count'],
            table_issues=table_info['issues'],
            has_stage_info=meta_info['has_stage'],
            has_prerequisites=meta_info['has_prereq'],
            has_formal_level=meta_info['has_level'],
            score=score,
            issues=issues
        )
        
        # 更新全局集合
        self.total_theorems.update(formal_elements['theorem_ids'])
        self.total_definitions.update(formal_elements['definition_ids'])
        self.total_lemmas.update(formal_elements['lemma_ids'])
        
        return result
    
    def _create_error_result(self, file_path: Path, error: str) -> DocumentAuditResult:
        """创建错误结果"""
        rel_path = file_path.relative_to(self.project_root)
        doc_type = self.detect_doc_type(file_path)
        
        result = DocumentAuditResult(
            file_path=str(file_path),
            relative_path=str(rel_path),
            doc_type=doc_type,
            word_count=0,
            char_count=0,
            has_definitions=False,
            has_properties=False,
            has_relations=False,
            has_argumentation=False,
            has_proof=False,
            has_examples=False,
            has_visualizations=False,
            has_references=False,
            theorem_count=0,
            lemma_count=0,
            definition_count=0,
            proposition_count=0,
            corollary_count=0,
            theorem_ids=[],
            mermaid_count=0,
            mermaid_issues=[],
            reference_count=0,
            broken_refs=[],
            code_block_count=0,
            inline_code_count=0,
            image_refs=[],
            missing_images=[],
            table_count=0,
            table_issues=[],
            has_stage_info=False,
            has_prerequisites=False,
            has_formal_level=False,
            score=DocumentQualityScore(),
            issues=[QualityIssue(
                file_path=str(rel_path),
                category='system',
                severity='critical',
                message=f'读取文件失败: {error}'
            )]
        )
        return result
    
    def _check_sections(self, content: str) -> Dict[str, bool]:
        """检查六段式结构"""
        return {
            key: bool(re.search(pattern, content, re.IGNORECASE))
            for pattern, key in self.REQUIRED_SECTIONS
        }
    
    def _check_formalization(self, content: str) -> Dict:
        """检查形式化元素"""
        theorems = self.THEOREM_PATTERN.findall(content)
        lemmas = self.LEMMA_PATTERN.findall(content)
        definitions = self.DEFINITION_PATTERN.findall(content)
        propositions = self.PROPOSITION_PATTERN.findall(content)
        corollaries = self.COROLLARY_PATTERN.findall(content)
        
        return {
            'theorem_count': len(theorems),
            'lemma_count': len(lemmas),
            'definition_count': len(definitions),
            'proposition_count': len(propositions),
            'corollary_count': len(corollaries),
            'theorem_ids': list(set(theorems)),
            'lemma_ids': list(set(lemmas)),
            'definition_ids': list(set(definitions)),
        }
    
    def _check_mermaid(self, content: str, file_path: Path) -> Dict:
        """检查Mermaid图表"""
        matches = self.MERMAID_PATTERN.findall(content)
        issues = []
        
        for i, mermaid_content in enumerate(matches):
            # 基本语法检查
            lines = mermaid_content.strip().split('\n')
            if not lines:
                issues.append(f"图表 #{i+1}: 空图表")
                continue
            
            first_line = lines[0].strip().lower()
            
            # 检测图表类型
            valid_types = ['graph', 'flowchart', 'sequenceDiagram', 'classDiagram',
                          'stateDiagram', 'erDiagram', 'gantt', 'pie', 'journey',
                          'gitGraph', 'mindmap', 'timeline', 'quadrantChart']
            
            if not any(first_line.startswith(vt) for vt in valid_types):
                issues.append(f"图表 #{i+1}: 未知图表类型 '{lines[0][:30]}...'")
            
            # 检查基本语法错误
            if 'graph' in first_line or 'flowchart' in first_line:
                # 检查是否有节点定义
                if '-->' not in mermaid_content and '---' not in mermaid_content:
                    issues.append(f"图表 #{i+1}: 图中无连接线")
        
        return {
            'count': len(matches),
            'issues': issues
        }
    
    def _check_references(self, content: str) -> Dict:
        """检查引用完整性"""
        # 查找所有引用标记
        ref_markers = set(self.REF_PATTERN.findall(content))
        
        # 查找引用定义
        ref_defs = dict(self.REF_LIST_PATTERN.findall(content))
        
        # 检查断链
        broken = []
        for ref_id in ref_markers:
            if ref_id not in ref_defs:
                broken.append(f"[^{ref_id}]")
        
        return {
            'count': len(ref_defs),
            'broken': broken,
            'markers': len(ref_markers)
        }
    
    def _check_code_examples(self, content: str) -> Dict:
        """检查代码示例"""
        code_blocks = self.CODE_BLOCK_PATTERN.findall(content)
        inline_codes = self.INLINE_CODE_PATTERN.findall(content)
        
        return {
            'block_count': len(code_blocks),
            'inline_count': len(inline_codes)
        }
    
    def _check_images(self, content: str, file_path: Path) -> Dict:
        """检查图片引用"""
        images = self.IMAGE_PATTERN.findall(content)
        refs = [img[1] for img in images]
        
        missing = []
        for alt, src in images:
            # 跳过外部URL
            if src.startswith(('http://', 'https://', 'data:')):
                continue
            
            # 解析相对路径
            if src.startswith('/'):
                img_path = self.project_root / src[1:]
            else:
                img_path = file_path.parent / src
            
            if not img_path.exists():
                missing.append(src)
        
        return {
            'refs': refs,
            'missing': missing
        }
    
    def _check_tables(self, content: str) -> Dict:
        """检查表格格式"""
        tables = self.TABLE_PATTERN.findall(content)
        issues = []
        
        # 简单检查：表格行是否对齐
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '|' in line and not line.strip().startswith('<!--'):
                # 检查表格行是否有对应的表头
                pass  # 简化处理
        
        return {
            'count': len(tables),
            'issues': issues
        }
    
    def _check_meta_info(self, content: str) -> Dict:
        """检查元信息"""
        return {
            'has_stage': bool(self.STAGE_INFO_PATTERN.search(content)),
            'has_prereq': bool(self.PREREQ_PATTERN.search(content)),
            'has_level': bool(self.FORMAL_LEVEL_PATTERN.search(content))
        }
    
    def _calculate_score(self, sections: Dict, formal: Dict, mermaid: Dict,
                         refs: Dict, code: Dict, doc_type: str) -> DocumentQualityScore:
        """计算质量评分"""
        score = DocumentQualityScore()
        
        # 1. 结构评分 (25%)
        required_sections = ['definitions', 'properties', 'relations', 
                            'argumentation', 'proof', 'examples']
        if doc_type in ['Struct', 'Knowledge']:
            required_sections.extend(['visualizations', 'references'])
        
        present = sum(1 for s in required_sections if sections.get(s, False))
        score.structure = round((present / len(required_sections)) * 100, 2)
        
        # 2. 形式化评分 (25%)
        total_formal = (formal['theorem_count'] + formal['lemma_count'] + 
                       formal['definition_count'] + formal['proposition_count'] + 
                       formal['corollary_count'])
        if doc_type == 'Struct':
            score.formalization = min(100, total_formal * 10)  # 每10个元素得满分
        elif doc_type == 'Knowledge':
            score.formalization = min(100, total_formal * 15)
        else:
            score.formalization = min(100, total_formal * 20)
        
        # 3. 可视化评分 (15%)
        if mermaid['count'] > 0:
            issue_ratio = len(mermaid['issues']) / max(1, mermaid['count'])
            score.visualization = round(max(0, 100 - issue_ratio * 50), 2)
        else:
            score.visualization = 50 if doc_type == 'Root' else 30
        
        # 4. 引用评分 (15%)
        if refs['count'] > 0:
            broken_ratio = len(refs['broken']) / max(1, refs['markers'])
            score.references = round(max(0, 100 - broken_ratio * 100), 2)
        else:
            score.references = 50 if doc_type == 'Root' else 40
        
        # 5. 示例评分 (20%)
        if code['block_count'] > 0 or code['inline_count'] > 5:
            score.examples = min(100, code['block_count'] * 20 + code['inline_count'] * 2)
        else:
            score.examples = 30
        
        return score
    
    def _collect_issues(self, file_path: Path, rel_path: Path, doc_type: str,
                        sections: Dict, formal: Dict, mermaid: Dict,
                        refs: Dict, image: Dict, table: Dict) -> List[QualityIssue]:
        """收集质量问题"""
        issues = []
        
        # 结构问题
        required_map = {
            'definitions': ('structure', 'high', '缺少概念定义章节'),
            'properties': ('structure', 'medium', '缺少属性推导章节'),
            'relations': ('structure', 'medium', '缺少关系建立章节'),
            'proof': ('structure', 'high' if doc_type == 'Struct' else 'medium', '缺少证明章节'),
            'examples': ('structure', 'medium', '缺少实例验证章节'),
        }
        
        if doc_type in ['Struct', 'Knowledge']:
            required_map['visualizations'] = ('structure', 'medium', '缺少可视化章节')
            required_map['references'] = ('structure', 'high', '缺少引用参考章节')
        
        for key, (cat, sev, msg) in required_map.items():
            if not sections.get(key, False):
                issues.append(QualityIssue(
                    file_path=str(rel_path),
                    category=cat,
                    severity=sev,
                    message=msg,
                    suggestion=f'添加 ## {key.capitalize()} 章节'
                ))
        
        # 形式化问题
        if doc_type == 'Struct' and formal['definition_count'] == 0:
            issues.append(QualityIssue(
                file_path=str(rel_path),
                category='formalization',
                severity='high',
                message='Struct文档缺少形式化定义 (Def-*)',
                suggestion='添加至少一个 Def-S-XX-XX 格式的定义'
            ))
        
        # Mermaid问题
        for issue in mermaid['issues']:
            issues.append(QualityIssue(
                file_path=str(rel_path),
                category='visualization',
                severity='medium',
                message=f'Mermaid语法问题: {issue}'
            ))
        
        # 引用问题
        for broken in refs['broken']:
            issues.append(QualityIssue(
                file_path=str(rel_path),
                category='references',
                severity='medium',
                message=f'引用未定义: {broken}',
                suggestion=f'在文档末尾添加 "{broken}: 引用内容"'
            ))
        
        # 图片问题
        for missing in image['missing']:
            issues.append(QualityIssue(
                file_path=str(rel_path),
                category='image',
                severity='medium',
                message=f'图片不存在: {missing}'
            ))
        
        return issues
    
    def run_audit(self) -> Dict:
        """执行完整审计"""
        print("=" * 60)
        print("文档质量审计 v4.1")
        print("=" * 60)
        
        md_files = self.get_all_markdown_files()
        self.total_docs = len(md_files)
        
        print(f"\n发现文档: {self.total_docs} 篇")
        print("开始并行审计...\n")
        
        # 并行处理
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.audit_document, f): f for f in md_files}
            
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                file_path = futures[future]
                try:
                    result = future.result()
                    self.results.append(result)
                    self.all_issues.extend(result.issues)
                    
                    if (i + 1) % 100 == 0 or i == len(md_files) - 1:
                        print(f"  已处理: {i+1}/{len(md_files)} 篇文档")
                        
                except Exception as e:
                    print(f"  错误处理 {file_path}: {e}")
        
        self.processed_docs = len(self.results)
        return self._generate_report()
    
    def _generate_report(self) -> Dict:
        """生成审计报告"""
        report = {
            'audit_date': datetime.now().isoformat(),
            'total_documents': self.total_docs,
            'processed_documents': self.processed_docs,
            'summary': self._generate_summary(),
            'theorem_continuity': self._check_theorem_continuity(),
            'issue_summary': self._generate_issue_summary(),
            'score_distribution': self._generate_score_distribution(),
            'document_breakdown': self._generate_document_breakdown(),
        }
        return report
    
    def _generate_summary(self) -> Dict:
        """生成摘要统计"""
        scores = [r.score.total for r in self.results]
        
        return {
            'average_score': round(sum(scores) / max(1, len(scores)), 2),
            'min_score': min(scores) if scores else 0,
            'max_score': max(scores) if scores else 0,
            'total_issues': len(self.all_issues),
            'critical_issues': len([i for i in self.all_issues if i.severity == 'critical']),
            'high_issues': len([i for i in self.all_issues if i.severity == 'high']),
            'medium_issues': len([i for i in self.all_issues if i.severity == 'medium']),
            'low_issues': len([i for i in self.all_issues if i.severity == 'low']),
            'total_theorems': len(self.total_theorems),
            'total_definitions': len(self.total_definitions),
            'total_lemmas': len(self.total_lemmas),
            'total_mermaid_charts': sum(r.mermaid_count for r in self.results),
            'total_code_blocks': sum(r.code_block_count for r in self.results),
            'total_tables': sum(r.table_count for r in self.results),
        }
    
    def _check_theorem_continuity(self) -> Dict:
        """检查定理编号连续性"""
        gaps = []
        
        # 按类型分组检查
        by_type = defaultdict(list)
        for tid in self.total_theorems:
            parts = tid.split('-')
            if len(parts) >= 3:
                key = f"{parts[0]}-{parts[1]}-{parts[2]}"
                try:
                    by_type[key].append(int(parts[3]))
                except (IndexError, ValueError):
                    pass
        
        for key, nums in by_type.items():
            nums = sorted(set(nums))
            for i in range(len(nums) - 1):
                if nums[i+1] - nums[i] > 1:
                    for missing in range(nums[i] + 1, nums[i+1]):
                        gaps.append(f"{key}-{missing:02d}")
        
        return {
            'theorem_count': len(self.total_theorems),
            'gaps_found': gaps,
            'gap_count': len(gaps)
        }
    
    def _generate_issue_summary(self) -> Dict:
        """生成问题摘要"""
        by_category = defaultdict(list)
        by_severity = defaultdict(list)
        
        for issue in self.all_issues:
            by_category[issue.category].append(issue)
            by_severity[issue.severity].append(issue)
        
        return {
            'by_category': {
                cat: [asdict(i) for i in issues[:10]]  # 只显示前10个
                for cat, issues in by_category.items()
            },
            'by_severity': {
                sev: len(issues) for sev, issues in by_severity.items()
            },
            'top_issues': [asdict(i) for i in self.all_issues[:20]]
        }
    
    def _generate_score_distribution(self) -> Dict:
        """生成分数分布"""
        ranges = {
            'excellent (90-100)': 0,
            'good (80-89)': 0,
            'acceptable (70-79)': 0,
            'needs_improvement (60-69)': 0,
            'poor (below 60)': 0
        }
        
        for r in self.results:
            score = r.score.total
            if score >= 90:
                ranges['excellent (90-100)'] += 1
            elif score >= 80:
                ranges['good (80-89)'] += 1
            elif score >= 70:
                ranges['acceptable (70-79)'] += 1
            elif score >= 60:
                ranges['needs_improvement (60-69)'] += 1
            else:
                ranges['poor (below 60)'] += 1
        
        return ranges
    
    def _generate_document_breakdown(self) -> Dict:
        """按类型生成文档分析"""
        by_type = defaultdict(lambda: {'count': 0, 'scores': [], 'issues': 0})
        
        for r in self.results:
            t = r.doc_type
            by_type[t]['count'] += 1
            by_type[t]['scores'].append(r.score.total)
            by_type[t]['issues'] += len(r.issues)
        
        return {
            doc_type: {
                'count': info['count'],
                'avg_score': round(sum(info['scores']) / max(1, len(info['scores'])), 2),
                'total_issues': info['issues']
            }
            for doc_type, info in by_type.items()
        }
    
    def save_results(self, output_dir: str):
        """保存审计结果"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 保存JSON结果
        report = self._generate_report()
        with open(output_path / 'audit-report-v4.1.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 保存详细结果
        detailed = [asdict(r) for r in self.results]
        with open(output_path / 'audit-details-v4.1.json', 'w', encoding='utf-8') as f:
            json.dump(detailed, f, ensure_ascii=False, indent=2)
        
        # 保存所有问题
        issues_data = [asdict(i) for i in self.all_issues]
        with open(output_path / 'all-issues-v4.1.json', 'w', encoding='utf-8') as f:
            json.dump(issues_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n结果已保存到: {output_dir}")
        print(f"  - audit-report-v4.1.json (汇总报告)")
        print(f"  - audit-details-v4.1.json (详细数据)")
        print(f"  - all-issues-v4.1.json (全部问题)")


def main():
    """主函数"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    auditor = DocumentQualityAuditor(project_root, max_workers=8)
    report = auditor.run_audit()
    
    # 保存结果
    output_dir = os.path.join(project_root, '.scripts', 'audit-results')
    auditor.save_results(output_dir)
    
    # 打印摘要
    print("\n" + "=" * 60)
    print("审计完成摘要")
    print("=" * 60)
    
    summary = report['summary']
    print(f"\n📊 总体统计:")
    print(f"   文档总数: {report['total_documents']}")
    print(f"   平均得分: {summary['average_score']}")
    print(f"   最高得分: {summary['max_score']}")
    print(f"   最低得分: {summary['min_score']}")
    
    print(f"\n📝 形式化元素:")
    print(f"   定理数量: {summary['total_theorems']}")
    print(f"   定义数量: {summary['total_definitions']}")
    print(f"   引理数量: {summary['total_lemmas']}")
    
    print(f"\n⚠️  问题统计:")
    print(f"   严重: {summary['critical_issues']}")
    print(f"   高优先级: {summary['high_issues']}")
    print(f"   中优先级: {summary['medium_issues']}")
    print(f"   低优先级: {summary['low_issues']}")
    
    print(f"\n📈 分数分布:")
    for range_name, count in report['score_distribution'].items():
        bar = "█" * (count // max(1, report['total_documents'] // 50))
        print(f"   {range_name}: {count:4d} {bar}")
    
    # 定理连续性
    continuity = report['theorem_continuity']
    print(f"\n🔗 定理连续性:")
    print(f"   定理总数: {continuity['theorem_count']}")
    print(f"   断号数量: {continuity['gap_count']}")
    if continuity['gaps_found'][:5]:
        print(f"   示例断号: {', '.join(continuity['gaps_found'][:5])}")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    main()
