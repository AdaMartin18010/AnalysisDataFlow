#!/usr/bin/env python3
"""
六段式模板验证器 v2.0
功能：
- 验证文档六段式结构
- 检查定理/定义编号格式
- 验证Mermaid图表存在性
- **新增**: 内容充实度评分（0-10分）
- 生成合规报告

作者: AnalysisDataFlow Toolchain Team
版本: 2.0.0
日期: 2026-04-24
"""

import re
import os
import json
import glob
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Set, Optional, Tuple
from collections import defaultdict
import argparse


@dataclass
class ValidationIssue:
    """验证问题记录"""
    file_path: str
    line_number: int
    check_type: str
    severity: str  # 'error', 'warning', 'info'
    message: str
    suggestion: str


@dataclass
class ValidationStats:
    """验证统计"""
    total_files: int
    compliant_files: int
    non_compliant_files: int
    total_issues: int
    by_severity: Dict[str, int]
    by_check_type: Dict[str, int]


@dataclass
class SectionScore:
    """章节评分"""
    section_name: str
    score: float
    max_score: float
    details: str


@dataclass
class ContentRichnessReport:
    """内容充实度报告"""
    file_path: str
    total_score: float
    max_score: float
    grade: str  # A, B, C, N/A
    section_scores: List[SectionScore]
    is_six_section: bool


class SixSectionValidator:
    """六段式模板验证器"""
    
    # 必需的章节（六段式）
    REQUIRED_SECTIONS = [
        ('concept_definition', r'##\s*1\.\s*概念定义|##\s*1\.\s*Definitions'),
        ('property_derivation', r'##\s*2\.\s*属性推导|##\s*2\.\s*Properties'),
        ('relation_establishment', r'##\s*3\.\s*关系建立|##\s*3\.\s*Relations'),
        ('argumentation', r'##\s*4\.\s*论证过程|##\s*4\.\s*Argumentation'),
        ('proof', r'##\s*5\.\s*形式证明|##\s*5\.\s*Proof|##\s*5\.\s*Engineering'),
        ('examples', r'##\s*6\.\s*实例验证|##\s*6\.\s*Examples'),
    ]
    
    # 推荐的章节
    RECOMMENDED_SECTIONS = [
        ('visualization', r'##\s*7\.\s*可视化|##\s*7\.\s*Visualizations'),
        ('references', r'##\s*8\.\s*引用参考|##\s*8\.\s*References'),
    ]
    
    # 形式化元素编号模式
    FORMAL_ELEMENT_PATTERNS = {
        'theorem': r'(Thm-[SKF]-\d{2}-\d{2,3})',
        'definition': r'(Def-[SKF]-\d{2}-\d{2,3})',
        'lemma': r'(Lemma-[SKF]-\d{2}-\d{2,3})',
        'proposition': r'(Prop-[SKF]-\d{2}-\d{2,3})',
        'corollary': r'(Cor-[SKF]-\d{2}-\d{2,3})',
    }
    
    # 章节评分权重（默认）
    DEFAULT_WEIGHTS = {
        'definitions': 2.0,
        'properties': 1.0,
        'relations': 1.0,
        'argumentation': 1.0,
        'proofs': 2.0,
        'examples': 1.0,
        'visualizations': 1.0,
        'references': 1.0,
    }
    
    # 业务模式文档评分权重（降低Properties/Proofs，增加Examples/Visualizations）
    BUSINESS_PATTERN_WEIGHTS = {
        'definitions': 2.0,
        'properties': 0.5,
        'relations': 1.0,
        'argumentation': 1.0,
        'proofs': 0.5,
        'examples': 1.5,
        'visualizations': 1.5,
        'references': 2.0,
    }
    
    # 所有章节定义（用于内容提取）
    ALL_SECTION_PATTERNS = [
        ('definitions', r'##\s*1\.\s*概念定义|##\s*1\.\s*Definitions'),
        ('properties', r'##\s*2\.\s*属性推导|##\s*2\.\s*Properties'),
        ('relations', r'##\s*3\.\s*关系建立|##\s*3\.\s*Relations'),
        ('argumentation', r'##\s*4\.\s*论证过程|##\s*4\.\s*Argumentation'),
        ('proofs', r'##\s*5\.\s*形式证明|##\s*5\.\s*Proof|##\s*5\.\s*Engineering'),
        ('examples', r'##\s*6\.\s*实例验证|##\s*6\.\s*Examples'),
        ('visualizations', r'##\s*7\.\s*可视化|##\s*7\.\s*Visualizations'),
        ('references', r'##\s*8\.\s*引用参考|##\s*8\.\s*References'),
    ]
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path).resolve()
        self.issues: List[ValidationIssue] = []
        self.formal_elements: Dict[str, List[str]] = defaultdict(list)
        self.content_reports: List[ContentRichnessReport] = []
        self.grade_counts: Dict[str, int] = {'A': 0, 'B': 0, 'C': 0}
        self.shell_docs: List[str] = []
        self.missing_refs_docs: List[str] = []
        self.missing_viz_docs: List[str] = []
        
    def scan_target_files(self) -> List[Path]:
        """扫描需要验证的目标文件"""
        md_files = []
        patterns = [
            "Struct/**/*.md",
            "Knowledge/**/*.md",
            "Flink/**/*.md",
        ]
        
        # 非核心文档排除模式（不应强制六段式）
        SKIP_PATTERNS = [
            'README', 'CHANGELOG', 'CONTRIBUTING', 'LICENSE',
            'QUICK-START', 'FAQ', 'GLOSSARY', 'ROADMAP',
            'INDEX', 'NAVIGATION', 'PROJECT-TRACKING', 'BEST-PRACTICES',
            'CHEATSHEET', 'CHECKLIST', 'COMPLETION-REPORT',
            'AGENT-', 'COMPLETION-REPORT', 'AUDIT-REPORT',
            'QUARTERLY-REVIEWS', 'verify-examples',
            'TASK-ASSIGNMENTS', 'THEOREM-INDEX',
            '00-meta', 'version-tracking', 'status-report',
            '_in-progress', 'archive', 'deprecated',
            'Flink-Scala-Rust-Comprehensive', '98-exercises',
            'docs/', 'i18n/',
            # 参考手册/速查表类（不应强制六段式）
            'complete-reference', 'functions-reference', 'cheatsheet',
            'data-types-reference', 'built-in-functions',
            'rest-api-complete-reference', 'sql-functions',
            'datastream-api-cheatsheet',
            # 案例研究汇编/注释类
            'CODE-RUNNABILITY-NOTES', 'PERFORMANCE-DATA-NOTES',
            # 证明链/推导链文档（特殊结构）
            'STRUCT-DERIVATION-CHAIN', 'PROOF-CHAIN',
            # 报告/追踪类
            'COMPLETENESS-REPORT', 'FORMAL-ELEMENT-FIX-REPORT',
            'BENCHMARK-RESULT', 'BENCHMARK-REPORT',
            # 练习/习题类
            'exercises', 'EXERCISES',
            # 案例研究类（汇编/单篇案例不应强制六段式）
            'case-studies', 'case-study',
            # 指南/迁移/对比类
            'migration-guide', 'upgrade-guide',
            'connector-guide', 'integration-guide',
            'security-hardening-guide', 'production-checklist',
            'state-backends-comparison', 'comparison-matrix',
            'market-report', 'annual-case-collection',
            'key-theorem-proof-chains',
            # 反模式/前沿分析/教程类
            'anti-patterns', 'research-trends', 'project-supplementation',
            'deep-comparison', 'complete-tutorial', 'complete-guide',
            'progress-tracking', 'proof-graph',
            # 对比/分析/集成/迁移类（特定文件，避免过度匹配）
            'materialize-comparison', 'flink-1.x-vs-2.0',
            'flink-vs-risingwave', 'rust-streaming-engines-comparison',
            'query-optimization-analysis', 'cloudflare-pipelines-analysis',
            'pulsar-functions-integration',
            'kafka-streams-migration', 'streaming-databases-market-analysis',
            'concurrency-paradigms-matrix', 'streaming-database-comprehensive-matrix',
            'deployment-architectures',
        ]
        
        for pattern in patterns:
            files = glob.glob(str(self.base_path / pattern), recursive=True)
            for f in files:
                path = Path(f).resolve()
                path_str = str(path).replace('\\', '/')
                # 排除非核心文档（大小写不敏感匹配）
                path_str_lower = path_str.lower()
                if any(x.lower() in path_str_lower for x in SKIP_PATTERNS):
                    continue
                # 排除模板文件、索引文件等
                if not any(x in path_str for x in ['TEMPLATE', '_TEMPLATE', '00-INDEX']):
                    md_files.append(path)
                    
        return list(set(md_files))
    
    def check_section_structure(self, content: str, file_path: Path) -> List[ValidationIssue]:
        """检查六段式结构"""
        issues = []
        rel_path = str(file_path.relative_to(self.base_path))
        
        # 检查必需章节
        for section_name, pattern in self.REQUIRED_SECTIONS:
            if not re.search(pattern, content, re.IGNORECASE):
                issues.append(ValidationIssue(
                    file_path=rel_path,
                    line_number=0,
                    check_type='missing_required_section',
                    severity='error',
                    message=f'缺少必需章节: {section_name}',
                    suggestion=f'请添加符合 "{pattern}" 格式的章节标题'
                ))
                
        # 检查推荐章节（仅警告）
        for section_name, pattern in self.RECOMMENDED_SECTIONS:
            if not re.search(pattern, content, re.IGNORECASE):
                issues.append(ValidationIssue(
                    file_path=rel_path,
                    line_number=0,
                    check_type='missing_recommended_section',
                    severity='warning',
                    message=f'缺少推荐章节: {section_name}',
                    suggestion=f'建议添加 "{pattern}" 章节以完善文档结构'
                ))
                
        return issues
    
    def check_formal_elements(self, content: str, file_path: Path) -> List[ValidationIssue]:
        """检查形式化元素编号"""
        issues = []
        rel_path = str(file_path.relative_to(self.base_path))
        lines = content.split('\n')
        
        # 提取文档类型前缀
        doc_prefix = None
        if 'Struct/' in rel_path:
            doc_prefix = 'S'
        elif 'Knowledge/' in rel_path:
            doc_prefix = 'K'
        elif 'Flink/' in rel_path:
            doc_prefix = 'F'
            
        # 检查每个形式化元素
        for elem_type, pattern in self.FORMAL_ELEMENT_PATTERNS.items():
            for line_num, line in enumerate(lines, 1):
                matches = re.findall(pattern, line)
                for match in matches:
                    self.formal_elements[elem_type].append(match)
                    
                    # 检查前缀是否匹配文档位置
                    if doc_prefix and not match.startswith(f'{elem_type.capitalize()[:3] if elem_type != "corollary" else "Cor"}-{doc_prefix}-'):
                        # 允许引用其他区域的元素
                        pass
                        
        # 检查是否有未编号的形式化定义
        unnumbered_patterns = [
            (r'\*\*定理\*\*[^:]|\*\*Theorem\*\*[^:]', 'theorem'),
            (r'\*\*定义\*\*[^:]|\*\*Definition\*\*[^:]', 'definition'),
            (r'\*\*引理\*\*[^:]|\*\*Lemma\*\*[^:]', 'lemma'),
        ]
        
        for pattern, elem_type in unnumbered_patterns:
            for line_num, line in enumerate(lines, 1):
                if re.search(pattern, line) and not re.search(rf'{self.FORMAL_ELEMENT_PATTERNS[elem_type]}', line):
                    issues.append(ValidationIssue(
                        file_path=rel_path,
                        line_number=line_num,
                        check_type='unnumbered_formal_element',
                        severity='warning',
                        message=f'发现可能未编号的{elem_type}',
                        suggestion=f'请添加格式为 "{elem_type.upper()}-{doc_prefix}-XX-XX" 的编号'
                    ))
                    
        return issues
    
    def check_mermaid_diagrams(self, content: str, file_path: Path) -> List[ValidationIssue]:
        """检查Mermaid图表"""
        issues = []
        rel_path = str(file_path.relative_to(self.base_path))
        
        # 提取所有Mermaid代码块
        mermaid_pattern = re.compile(r'```mermaid\s*(.*?)```', re.DOTALL)
        mermaid_blocks = mermaid_pattern.findall(content)
        
        if not mermaid_blocks:
            issues.append(ValidationIssue(
                file_path=rel_path,
                line_number=0,
                check_type='missing_mermaid_diagram',
                severity='warning',
                message='文档缺少Mermaid图表',
                suggestion='请至少添加一个Mermaid图表以增强可视化效果'
            ))
        else:
            # 检查每个Mermaid块的语法
            for i, block in enumerate(mermaid_blocks, 1):
                lines = block.strip().split('\n')
                if not lines:
                    continue
                    
                # 检查图表类型
                first_line = lines[0].strip().lower()
                valid_types = ['graph', 'flowchart', 'sequence', 'class', 'state', 'er', 'gantt', 'pie', 'git', 'journey']
                
                if not any(first_line.startswith(t) for t in valid_types):
                    issues.append(ValidationIssue(
                        file_path=rel_path,
                        line_number=0,
                        check_type='invalid_mermaid_type',
                        severity='warning',
                        message=f'第{i}个Mermaid图表类型可能无效: {first_line}',
                        suggestion=f'请使用有效的图表类型: {", ".join(valid_types)}'
                    ))
                    
                # 检查基本语法
                if 'graph' in first_line or 'flowchart' in first_line:
                    # 检查节点定义
                    node_pattern = re.compile(r'\[\[.*?\]\]|\[.*?\]|\(.*?\)|\{.*?\}')
                    if not node_pattern.search(block):
                        issues.append(ValidationIssue(
                            file_path=rel_path,
                            line_number=0,
                            check_type='empty_mermaid_graph',
                            severity='warning',
                            message=f'第{i}个Mermaid图可能没有节点定义',
                            suggestion='请添加节点和边的定义'
                        ))
                        
        return issues
    
    def check_header_metadata(self, content: str, file_path: Path) -> List[ValidationIssue]:
        """检查头部元数据"""
        issues = []
        rel_path = str(file_path.relative_to(self.base_path))
        
        # 检查是否有所属阶段声明
        stage_pattern = r'所属阶段[:：]\s*(Struct|Knowledge|Flink)'
        if not re.search(stage_pattern, content, re.IGNORECASE):
            # 检查是否在正确的位置（标题后）
            first_lines = '\n'.join(content.split('\n')[:10])
            if not re.search(stage_pattern, first_lines, re.IGNORECASE):
                issues.append(ValidationIssue(
                    file_path=rel_path,
                    line_number=1,
                    check_type='missing_stage_metadata',
                    severity='warning',
                    message='缺少所属阶段声明',
                    suggestion='请在文档开头添加: > 所属阶段: Struct/ Knowledge/ Flink'
                ))
                
        # 检查是否有前置依赖声明
        dependency_pattern = r'前置依赖[:：]\s*\['
        if not re.search(dependency_pattern, content):
            issues.append(ValidationIssue(
                file_path=rel_path,
                line_number=1,
                check_type='missing_dependency_metadata',
                severity='info',
                message='缺少前置依赖声明',
                suggestion='建议添加: > 前置依赖: [相关文档链接]'
            ))
            
        return issues
    
    def check_references_format(self, content: str, file_path: Path) -> List[ValidationIssue]:
        """检查引用格式"""
        issues = []
        rel_path = str(file_path.relative_to(self.base_path))
        
        # 检查引用格式 [^n]
        ref_pattern = re.compile(r'\[\^(\d+)\]')
        refs = ref_pattern.findall(content)
        
        if refs and '## 8.' not in content and '## 8 ' not in content:
            # 有引用但没有References章节
            pass  # 可能在其他位置
            
        # 检查引用是否连续（建议）
        if refs:
            ref_nums = sorted([int(r) for r in refs])
            if ref_nums:
                expected = list(range(1, max(ref_nums) + 1))
                missing = set(expected) - set(ref_nums)
                if missing:
                    issues.append(ValidationIssue(
                        file_path=rel_path,
                        line_number=0,
                        check_type='non_consecutive_references',
                        severity='info',
                        message=f'引用编号不连续，缺少: {sorted(missing)}',
                        suggestion='建议保持引用编号连续'
                    ))
                    
        return issues
    
    # ========== 内容充实度评分模块（v2.0 新增） ==========
    
    def is_six_section_document(self, content: str) -> bool:
        """判断是否是六段式文档（至少包含1个必需章节标题）"""
        for _, pattern in self.REQUIRED_SECTIONS:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
    
    def is_business_pattern_doc(self, file_path: Path) -> bool:
        """判断是否是业务模式文档（降低Properties/Proofs权重）"""
        rel_path = str(file_path.relative_to(self.base_path)).replace('\\', '/')
        return 'Knowledge/03-business-patterns/' in rel_path
    
    def extract_sections(self, content: str) -> Dict[str, str]:
        """提取各章节内容"""
        sections = {}
        
        # 找到所有章节的位置
        section_positions = []
        for name, pattern in self.ALL_SECTION_PATTERNS:
            match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
            if match:
                section_positions.append((name, match.start(), match.end()))
        
        if not section_positions:
            return sections
        
        # 按位置排序
        section_positions.sort(key=lambda x: x[1])
        
        # 提取每个章节的内容
        for i, (name, start, end) in enumerate(section_positions):
            if i + 1 < len(section_positions):
                next_start = section_positions[i + 1][1]
                section_content = content[end:next_start]
            else:
                section_content = content[end:]
            sections[name] = section_content.strip()
        
        return sections
    
    def count_content_chars(self, text: str) -> int:
        """计算文本的实际内容字数（中文字符+英文单词）"""
        if not text:
            return 0
        # 移除markdown标记和空白
        clean = re.sub(r'[#*`\[\](){}|!\-_>\s]', ' ', text)
        # 移除URL
        clean = re.sub(r'https?://\S+', ' ', clean)
        # 中文字符
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', clean))
        # 英文单词（至少2个字母）
        english_words = len(re.findall(r'[a-zA-Z]{2,}', clean))
        return chinese_chars + english_words
    
    def score_definitions(self, content: str, max_score: float = 2.0) -> Tuple[float, str]:
        """评分 Definitions 章节：包含≥2个 Def-* 编号块"""
        defs = re.findall(r'Def-[SKF]-\d{2}-\d{2,3}', content)
        count = len(set(defs))
        if count >= 2:
            return max_score, f"包含 {count} 个 Def-* 编号"
        elif count == 1:
            return max_score * 0.5, f"仅包含 1 个 Def-* 编号（需≥2）"
        else:
            return 0.0, "缺少 Def-* 编号"
    
    def score_properties(self, content: str, max_score: float = 1.0) -> Tuple[float, str]:
        """评分 Properties 章节：包含≥1个 Lemma-* 或 Prop-*"""
        lemmas = re.findall(r'Lemma-[SKF]-\d{2}-\d{2,3}', content)
        props = re.findall(r'Prop-[SKF]-\d{2}-\d{2,3}', content)
        count = len(set(lemmas)) + len(set(props))
        if count >= 1:
            return max_score, f"包含 {len(set(lemmas))} 个 Lemma-* 和 {len(set(props))} 个 Prop-*"
        else:
            return 0.0, "缺少 Lemma-* 或 Prop-* 编号"
    
    def score_relations(self, content: str, max_score: float = 1.0) -> Tuple[float, str]:
        """评分 Relations 章节：包含≥1个关系论证段落（≥100字）"""
        char_count = self.count_content_chars(content)
        if char_count >= 100:
            return max_score, f"关系论证段落约 {char_count} 字"
        else:
            return 0.0, f"关系论证段落仅约 {char_count} 字（需≥100）"
    
    def score_argumentation(self, content: str, max_score: float = 1.0) -> Tuple[float, str]:
        """评分 Argumentation 章节：包含≥1个论证段落（≥100字）"""
        char_count = self.count_content_chars(content)
        if char_count >= 100:
            return max_score, f"论证段落约 {char_count} 字"
        else:
            return 0.0, f"论证段落仅约 {char_count} 字（需≥100）"
    
    def score_proofs(self, content: str, max_score: float = 2.0) -> Tuple[float, str]:
        """评分 Proofs 章节：包含≥1个 Thm-* 及证明内容（≥50字）"""
        thms = re.findall(r'Thm-[SKF]-\d{2}-\d{2,3}', content)
        if not thms:
            return 0.0, "缺少 Thm-* 编号"
        
        char_count = self.count_content_chars(content)
        if char_count >= 50:
            return max_score, f"包含 {len(set(thms))} 个 Thm-*，证明内容约 {char_count} 字"
        else:
            return max_score * 0.5, f"包含 Thm-* 但证明内容仅约 {char_count} 字（需≥50）"
    
    def score_examples(self, content: str, max_score: float = 1.0) -> Tuple[float, str]:
        """评分 Examples 章节：包含≥1个代码/配置示例或案例"""
        # 检查代码块（包括 ```java, ```python 等）
        code_blocks = re.findall(r'```[\w]*\s*[\s\S]*?```', content)
        # 检查配置示例（key: value 模式，至少3处）
        config_patterns = re.findall(r'[\w-]+:\s*\S+', content)
        # 检查案例描述
        case_patterns = re.findall(r'案例|case study|example|实例|示例', content, re.IGNORECASE)
        
        has_code = len(code_blocks) > 0
        has_config = len(config_patterns) >= 3
        has_case = len(case_patterns) >= 2
        
        if has_code or has_config or has_case:
            details = []
            if has_code:
                details.append(f"{len(code_blocks)} 个代码块")
            if has_config:
                details.append(f"{len(config_patterns)} 处配置项")
            if has_case:
                details.append(f"{len(case_patterns)} 处案例提及")
            return max_score, "包含 " + ", ".join(details)
        else:
            return 0.0, "缺少代码/配置示例或案例"
    
    def score_visualizations(self, content: str, max_score: float = 1.0) -> Tuple[float, str]:
        """评分 Visualizations 章节：包含≥1个Mermaid图"""
        mermaid_blocks = re.findall(r'```mermaid\s*[\s\S]*?```', content)
        if mermaid_blocks:
            return max_score, f"包含 {len(mermaid_blocks)} 个 Mermaid 图"
        else:
            return 0.0, "缺少 Mermaid 图"
    
    def score_references(self, content: str, max_score: float = 1.0) -> Tuple[float, str]:
        """评分 References 章节：包含≥3条 [^n] 引用"""
        refs = re.findall(r'\[\^(\d+)\]', content)
        unique_refs = len(set(refs))
        if unique_refs >= 3:
            return max_score, f"包含 {unique_refs} 条引用"
        else:
            return 0.0, f"仅 {unique_refs} 条引用（需≥3）"
    
    def calculate_content_score(self, content: str, file_path: Path) -> Optional[ContentRichnessReport]:
        """计算内容充实度评分"""
        rel_path = str(file_path.relative_to(self.base_path)).replace('\\', '/')
        
        # 检查是否是六段式文档
        if not self.is_six_section_document(content):
            return ContentRichnessReport(
                file_path=rel_path,
                total_score=0.0,
                max_score=0.0,
                grade='N/A',
                section_scores=[],
                is_six_section=False
            )
        
        # 判断是否是业务模式文档
        is_business = self.is_business_pattern_doc(file_path)
        weights = self.BUSINESS_PATTERN_WEIGHTS if is_business else self.DEFAULT_WEIGHTS
        
        # 提取各章节内容
        sections = self.extract_sections(content)
        
        section_scores = []
        total_score = 0.0
        total_max = 0.0
        
        # 评分各章节
        scoring_methods = {
            'definitions': self.score_definitions,
            'properties': self.score_properties,
            'relations': self.score_relations,
            'argumentation': self.score_argumentation,
            'proofs': self.score_proofs,
            'examples': self.score_examples,
            'visualizations': self.score_visualizations,
            'references': self.score_references,
        }
        
        for section_name, scorer in scoring_methods.items():
            section_content = sections.get(section_name, '')
            max_score = weights.get(section_name, 1.0)
            score, details = scorer(section_content, max_score)
            section_scores.append(SectionScore(
                section_name=section_name,
                score=round(score, 1),
                max_score=max_score,
                details=details
            ))
            total_score += score
            total_max += max_score
        
        # 确定等级
        if total_score >= 8:
            grade = 'A'
        elif total_score >= 5:
            grade = 'B'
        else:
            grade = 'C'
        
        return ContentRichnessReport(
            file_path=rel_path,
            total_score=round(total_score, 1),
            max_score=total_max,
            grade=grade,
            section_scores=section_scores,
            is_six_section=True
        )
    
    def validate_file(self, file_path: Path) -> List[ValidationIssue]:
        """验证单个文件"""
        issues = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return [ValidationIssue(
                file_path=str(file_path.relative_to(self.base_path)),
                line_number=0,
                check_type='read_error',
                severity='error',
                message=f'无法读取文件: {e}',
                suggestion='检查文件编码和权限'
            )]
            
        # 执行各项检查
        issues.extend(self.check_section_structure(content, file_path))
        issues.extend(self.check_formal_elements(content, file_path))
        issues.extend(self.check_mermaid_diagrams(content, file_path))
        issues.extend(self.check_header_metadata(content, file_path))
        issues.extend(self.check_references_format(content, file_path))
        
        # 新增: 内容充实度评分
        score_report = self.calculate_content_score(content, file_path)
        if score_report:
            self.content_reports.append(score_report)
        
        return issues
    
    def run_validation(self) -> Tuple[List[ValidationIssue], ValidationStats]:
        """运行完整验证"""
        print("📐 Six-Section Template Validator v2.0")
        print("=" * 50)
        
        files = self.scan_target_files()
        print(f"\n📁 Found {len(files)} target files")
        
        all_issues = []
        compliant_count = 0
        self.content_reports = []
        
        print("\n🔎 Validating files...")
        for i, file_path in enumerate(files, 1):
            if i % 50 == 0:
                print(f"   Progress: {i}/{len(files)} files")
                
            issues = self.validate_file(file_path)
            all_issues.extend(issues)
            
            # 如果没有错误，则认为合规
            if not [i for i in issues if i.severity == 'error']:
                compliant_count += 1
                
        # 统计
        stats = ValidationStats(
            total_files=len(files),
            compliant_files=compliant_count,
            non_compliant_files=len(files) - compliant_count,
            total_issues=len(all_issues),
            by_severity={
                'error': len([i for i in all_issues if i.severity == 'error']),
                'warning': len([i for i in all_issues if i.severity == 'warning']),
                'info': len([i for i in all_issues if i.severity == 'info']),
            },
            by_check_type=defaultdict(int)
        )
        
        for issue in all_issues:
            stats.by_check_type[issue.check_type] += 1
            
        self.issues = all_issues
        
        # 内容充实度统计（仅统计六段式文档）
        scored_docs = [r for r in self.content_reports if r.is_six_section]
        self.grade_counts = {'A': 0, 'B': 0, 'C': 0}
        self.shell_docs = []
        self.missing_refs_docs = []
        self.missing_viz_docs = []
        
        for report in scored_docs:
            self.grade_counts[report.grade] += 1
            if report.grade == 'C':
                self.shell_docs.append(report.file_path)
            # 引用缺失（References 未得满分）
            ref_score = next((s for s in report.section_scores if s.section_name == 'references'), None)
            if ref_score and ref_score.score < ref_score.max_score:
                self.missing_refs_docs.append(report.file_path)
            # 可视化缺失（Visualizations 未得满分）
            viz_score = next((s for s in report.section_scores if s.section_name == 'visualizations'), None)
            if viz_score and viz_score.score < viz_score.max_score:
                self.missing_viz_docs.append(report.file_path)
        
        return all_issues, stats
    
    def generate_report(self, output_path: str, stats: ValidationStats):
        """生成验证报告"""
        report = {
            'version': '2.0.0',
            'validator': 'Six-Section Template Validator',
            'stats': asdict(stats),
            'issues': [asdict(issue) for issue in self.issues],
            'formal_elements_summary': {
                elem_type: len(elements) 
                for elem_type, elements in self.formal_elements.items()
            },
            'compliance_rate': round(stats.compliant_files / stats.total_files * 100, 2) if stats.total_files > 0 else 0,
            'content_richness': {
                'graded_documents': len([r for r in self.content_reports if r.is_six_section]),
                'grade_distribution': self.grade_counts,
                'shell_documents': self.shell_docs,
                'missing_references_documents': self.missing_refs_docs,
                'missing_visualizations_documents': self.missing_viz_docs,
                'detailed_scores': [
                    {
                        'file_path': r.file_path,
                        'total_score': r.total_score,
                        'max_score': r.max_score,
                        'grade': r.grade,
                        'sections': [
                            {
                                'name': s.section_name,
                                'score': s.score,
                                'max_score': s.max_score,
                                'details': s.details
                            }
                            for s in r.section_scores
                        ]
                    }
                    for r in self.content_reports if r.is_six_section
                ]
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        return report


def main():
    parser = argparse.ArgumentParser(description='Six-Section Template Validator v2.0')
    parser.add_argument('--base-path', default='.', help='项目根目录')
    parser.add_argument('--output', default='six-section-validation-report.json', help='输出报告路径')
    parser.add_argument('--fail-on-error', action='store_true', help='发现错误时返回非零退出码')
    
    args = parser.parse_args()
    
    validator = SixSectionValidator(args.base_path)
    issues, stats = validator.run_validation()
    
    # 生成报告
    report = validator.generate_report(args.output, stats)
    
    # 打印摘要
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    print(f"Total files:        {stats.total_files}")
    print(f"Compliant files:    {stats.compliant_files} ({report['compliance_rate']}%)")
    print(f"Non-compliant:      {stats.non_compliant_files}")
    print(f"Total issues:       {stats.total_issues}")
    print(f"  Errors:           {stats.by_severity.get('error', 0)}")
    print(f"  Warnings:         {stats.by_severity.get('warning', 0)}")
    print(f"  Info:             {stats.by_severity.get('info', 0)}")
    print("=" * 50)
    
    # 形式化元素统计
    print("\n📐 Formal Elements Summary:")
    for elem_type, count in report['formal_elements_summary'].items():
        print(f"  {elem_type.capitalize():12s}: {count}")
    
    # 内容充实度评分
    print("\n📝 Content Richness Scores:")
    grade_counts = report['content_richness']['grade_distribution']
    total_graded = sum(grade_counts.values())
    print(f"  Documents scored: {total_graded}")
    print(f"  Grade A (8-10):   {grade_counts['A']} ✅")
    print(f"  Grade B (5-7):    {grade_counts['B']} ⚠️")
    print(f"  Grade C (0-4):    {grade_counts['C']} ❌")
    
    if validator.shell_docs:
        print(f"\n  ❌ Shell documents ({len(validator.shell_docs)}):")
        for doc in validator.shell_docs[:10]:
            print(f"     - {doc}")
        if len(validator.shell_docs) > 10:
            print(f"     ... and {len(validator.shell_docs) - 10} more")
    
    if validator.missing_refs_docs:
        print(f"\n  📚 Missing references ({len(validator.missing_refs_docs)}):")
        for doc in validator.missing_refs_docs[:10]:
            print(f"     - {doc}")
        if len(validator.missing_refs_docs) > 10:
            print(f"     ... and {len(validator.missing_refs_docs) - 10} more")
    
    if validator.missing_viz_docs:
        print(f"\n  📊 Missing visualizations ({len(validator.missing_viz_docs)}):")
        for doc in validator.missing_viz_docs[:10]:
            print(f"     - {doc}")
        if len(validator.missing_viz_docs) > 10:
            print(f"     ... and {len(validator.missing_viz_docs) - 10} more")
        
    print(f"\n✅ Report saved to: {args.output}")
    
    if args.fail_on_error and stats.by_severity.get('error', 0) > 0:
        return 1
    return 0


if __name__ == '__main__':
    exit(main())
