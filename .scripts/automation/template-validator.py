#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
六段式模板验证器 (Template Validator)

功能：
- 验证文档是否遵循六段式结构
- 检查必要的章节是否存在
- 验证形式化元素编号格式（Def-*, Thm-*, Lemma-*）
- 检查Mermaid图表存在性
- 检查引用格式
- 提供修复建议

作者: Automation Agent
版本: 1.0.0
"""

import re
import json
import argparse
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Any, Tuple
from enum import Enum
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ValidationLevel(Enum):
    """验证级别"""
    ERROR = "error"       # 必须修复
    WARNING = "warning"   # 建议修复
    INFO = "info"         # 提示信息


class SectionType(Enum):
    """章节类型"""
    DEFINITIONS = "definitions"
    PROPERTIES = "properties"
    RELATIONS = "relations"
    ARGUMENTATION = "argumentation"
    PROOF = "proof"
    EXAMPLES = "examples"
    VISUALIZATIONS = "visualizations"
    REFERENCES = "references"


@dataclass
class ValidationIssue:
    """验证问题"""
    file_path: str
    line_number: int
    level: ValidationLevel
    category: str
    message: str
    suggestion: str = ""


@dataclass
class FormalElement:
    """形式化元素"""
    element_type: str  # Def, Thm, Lemma, Prop, Cor
    stage: str         # S, K, F
    doc_num: str
    seq_num: str
    full_id: str
    line_number: int
    context: str


@dataclass
class SectionInfo:
    """章节信息"""
    section_type: SectionType
    title: str
    line_start: int
    line_end: int
    content_length: int
    has_content: bool


@dataclass
class ValidationResult:
    """验证结果"""
    file_path: str
    is_valid: bool = True
    issues: List[ValidationIssue] = field(default_factory=list)
    sections: List[SectionInfo] = field(default_factory=list)
    formal_elements: List[FormalElement] = field(default_factory=list)
    mermaid_count: int = 0
    has_header: bool = False
    formalization_level: str = ""
    score: float = 0.0


class TemplateValidator:
    """模板验证器"""
    
    # 六段式必需章节（中英文标题）
    REQUIRED_SECTIONS = {
        SectionType.DEFINITIONS: [
            r'概念定义|定义|Definitions?'
        ],
        SectionType.PROPERTIES: [
            r'属性推导|性质|Properties?|Attributes?'
        ],
        SectionType.RELATIONS: [
            r'关系建立|关系|Relations?'
        ],
        SectionType.ARGUMENTATION: [
            r'论证过程|论证|Argumentation|Discussion'
        ],
        SectionType.PROOF: [
            r'形式证明|证明|Proof|Engineering Argument'
        ],
        SectionType.EXAMPLES: [
            r'实例验证|示例|Examples?|Cases?'
        ],
        SectionType.VISUALIZATIONS: [
            r'可视化|图表|Visualizations?|Diagrams?'
        ],
        SectionType.REFERENCES: [
            r'引用参考|参考|References?|Citations?'
        ],
    }
    
    # 形式化元素编号正则
    FORMAL_ELEMENT_PATTERN = re.compile(
        r'(Def|Thm|Theorem|Lemma|Prop|Proposition|Cor|Corollary)'  # 类型
        r'[-\s]*'  # 分隔符
        r'([SKF])'  # 阶段
        r'[-\s]*'  # 分隔符
        r'(\d+)'  # 文档序号
        r'[-\s]*'  # 分隔符
        r'(\d+)',  # 顺序号
        re.IGNORECASE
    )
    
    # 标准形式化元素ID正则
    STANDARD_FORMAL_PATTERN = re.compile(
        r'`(Def|Thm|Lemma|Prop|Cor)-(S|K|F)-(\d{2})-(\d{2})`'
    )
    
    # Mermaid图表正则
    MERMAID_PATTERN = re.compile(
        r'```mermaid\s*\n(.*?)```',
        re.DOTALL | re.IGNORECASE
    )
    
    # 引用格式正则
    REF_PATTERN = re.compile(r'\[\^(\d+)\]')
    REF_DEF_PATTERN = re.compile(r'^\[\^(\d+)\]:\s*(.+)')
    
    # 头部元信息正则
    HEADER_META_PATTERN = re.compile(
        r'>\s*所属阶段:\s*(Struct|Knowledge|Flink)/?',
        re.IGNORECASE
    )
    FORMALIZATION_LEVEL_PATTERN = re.compile(
        r'>\s*形式化等级:\s*L([1-6])',
        re.IGNORECASE
    )
    
    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        strict_mode: bool = False
    ):
        """
        初始化验证器
        
        Args:
            config: 自定义配置
            strict_mode: 严格模式
        """
        self.config = config or {}
        self.strict_mode = strict_mode
        self.skip_patterns = self.config.get('skip_patterns', [
            'node_modules', '.git', '__pycache__', '.venv', 'venv', 'archive'
        ])
        
    def _should_skip_file(self, file_path: Path) -> bool:
        """判断是否应该跳过文件"""
        path_str = str(file_path)
        return any(pattern in path_str for pattern in self.skip_patterns)
        
    def _extract_sections(self, content: str) -> List[SectionInfo]:
        """提取章节信息"""
        sections = []
        lines = content.split('\n')
        
        # 查找所有二级标题
        heading_pattern = re.compile(r'^(##)\s+(.+)$')
        headings = []
        
        for i, line in enumerate(lines, 1):
            match = heading_pattern.match(line)
            if match:
                headings.append((i, match.group(2).strip()))
                
        # 确定章节范围
        for idx, (line_num, title) in enumerate(headings):
            line_start = line_num
            line_end = headings[idx + 1][0] - 1 if idx + 1 < len(headings) else len(lines)
            
            section_content = '\n'.join(lines[line_start:line_end])
            content_length = len(section_content.strip())
            
            # 确定章节类型
            section_type = self._classify_section(title)
            
            sections.append(SectionInfo(
                section_type=section_type,
                title=title,
                line_start=line_start,
                line_end=line_end,
                content_length=content_length,
                has_content=content_length > 50
            ))
            
        return sections
        
    def _classify_section(self, title: str) -> Optional[SectionType]:
        """根据标题分类章节"""
        for section_type, patterns in self.REQUIRED_SECTIONS.items():
            for pattern in patterns:
                if re.search(pattern, title, re.IGNORECASE):
                    return section_type
        return None
        
    def _extract_formal_elements(self, content: str) -> List[FormalElement]:
        """提取形式化元素"""
        elements = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            for match in self.FORMAL_ELEMENT_PATTERN.finditer(line):
                element_type = match.group(1)
                stage = match.group(2).upper()
                doc_num = match.group(3)
                seq_num = match.group(4)
                
                # 标准化类型名称
                type_mapping = {
                    'Theorem': 'Thm',
                    'Proposition': 'Prop',
                    'Corollary': 'Cor'
                }
                element_type = type_mapping.get(element_type, element_type)
                
                full_id = f"{element_type}-{stage}-{int(doc_num):02d}-{int(seq_num):02d}"
                
                elements.append(FormalElement(
                    element_type=element_type,
                    stage=stage,
                    doc_num=f"{int(doc_num):02d}",
                    seq_num=f"{int(seq_num):02d}",
                    full_id=full_id,
                    line_number=i,
                    context=line.strip()[:100]
                ))
                
        return elements
        
    def _count_mermaid_diagrams(self, content: str) -> int:
        """统计Mermaid图表数量"""
        return len(self.MERMAID_PATTERN.findall(content))
        
    def _check_header_meta(self, content: str) -> Tuple[bool, str]:
        """检查头部元信息"""
        has_header = bool(self.HEADER_META_PATTERN.search(content))
        
        level_match = self.FORMALIZATION_LEVEL_PATTERN.search(content)
        formalization_level = f"L{level_match.group(1)}" if level_match else ""
        
        return has_header, formalization_level
        
    def _validate_section_completeness(
        self,
        file_path: str,
        sections: List[SectionInfo]
    ) -> List[ValidationIssue]:
        """验证章节完整性"""
        issues = []
        found_sections = {s.section_type for s in sections if s.section_type}
        
        # 检查必需章节
        required = [
            SectionType.DEFINITIONS,
            SectionType.PROPERTIES,
            SectionType.VISUALIZATIONS,
            SectionType.REFERENCES
        ]
        
        for section_type in required:
            if section_type not in found_sections:
                # 查找可能的章节标题
                patterns = self.REQUIRED_SECTIONS[section_type]
                expected_title = patterns[0].split('|')[0]
                
                issues.append(ValidationIssue(
                    file_path=file_path,
                    line_number=0,
                    level=ValidationLevel.ERROR if self.strict_mode else ValidationLevel.WARNING,
                    category="章节缺失",
                    message=f"缺少必需章节: {section_type.value}",
                    suggestion=f"添加 '## {expected_title}' 章节"
                ))
            else:
                # 检查章节内容
                section = next(s for s in sections if s.section_type == section_type)
                if not section.has_content:
                    issues.append(ValidationIssue(
                        file_path=file_path,
                        line_number=section.line_start,
                        level=ValidationLevel.WARNING,
                        category="内容不足",
                        message=f"章节 '{section.title}' 内容过少",
                        suggestion="添加更多内容到该章节"
                    ))
                    
        return issues
        
    def _validate_formal_elements(
        self,
        file_path: str,
        elements: List[FormalElement],
        sections: List[SectionInfo]
    ) -> List[ValidationIssue]:
        """验证形式化元素"""
        issues = []
        
        # 检查编号格式
        for elem in elements:
            # 检查是否使用标准格式
            if not self.STANDARD_FORMAL_PATTERN.search(elem.context):
                issues.append(ValidationIssue(
                    file_path=file_path,
                    line_number=elem.line_number,
                    level=ValidationLevel.WARNING,
                    category="编号格式",
                    message=f"形式化元素 '{elem.full_id}' 未使用标准格式",
                    suggestion=f"使用反引号包裹: `{elem.full_id}`"
                ))
                
        # 检查定义章节是否有定义
        def_section = None
        for s in sections:
            if s.section_type == SectionType.DEFINITIONS:
                def_section = s
                break
                
        if def_section:
            def_elements = [
                e for e in elements 
                if def_section.line_start <= e.line_number <= def_section.line_end
            ]
            if not def_elements:
                issues.append(ValidationIssue(
                    file_path=file_path,
                    line_number=def_section.line_start,
                    level=ValidationLevel.WARNING,
                    category="定义缺失",
                    message="概念定义章节中未找到形式化定义",
                    suggestion="添加至少一个 Def-* 定义"
                ))
            elif not any(e.element_type == 'Def' for e in def_elements):
                issues.append(ValidationIssue(
                    file_path=file_path,
                    line_number=def_section.line_start,
                    level=ValidationLevel.WARNING,
                    category="定义类型",
                    message="概念定义章节应包含至少一个 Def-* 定义",
                    suggestion="添加 Def-* 定义"
                ))
                
        # 检查属性章节是否有引理或命题
        prop_section = None
        for s in sections:
            if s.section_type == SectionType.PROPERTIES:
                prop_section = s
                break
                
        if prop_section:
            prop_elements = [
                e for e in elements 
                if prop_section.line_start <= e.line_number <= prop_section.line_end
            ]
            if prop_elements:
                if not any(e.element_type in ['Lemma', 'Prop'] for e in prop_elements):
                    issues.append(ValidationIssue(
                        file_path=file_path,
                        line_number=prop_section.line_start,
                        level=ValidationLevel.INFO,
                        category="属性类型",
                        message="属性推导章节建议包含 Lemma-* 或 Prop-*",
                        suggestion="添加引理或命题"
                    ))
                    
        return issues
        
    def _validate_references(
        self,
        file_path: str,
        content: str
    ) -> List[ValidationIssue]:
        """验证引用格式"""
        issues = []
        
        # 提取所有引用和定义
        refs = set(self.REF_PATTERN.findall(content))
        ref_defs = {
            m.group(1) for m in self.REF_DEF_PATTERN.finditer(content)
        }
        
        # 检查未定义的引用
        for ref_id in refs:
            if ref_id not in ref_defs:
                # 查找引用位置
                for i, line in enumerate(content.split('\n'), 1):
                    if f'[^{ref_id}]' in line and ']:' not in line:
                        issues.append(ValidationIssue(
                            file_path=file_path,
                            line_number=i,
                            level=ValidationLevel.ERROR,
                            category="引用错误",
                            message=f"引用 [^{ref_id}] 未定义",
                            suggestion=f"在文档末尾添加: [^{ref_id}]: 引用内容"
                        ))
                        break
                        
        # 检查未使用的定义
        for ref_id in ref_defs:
            if ref_id not in refs:
                issues.append(ValidationIssue(
                    file_path=file_path,
                    line_number=0,
                    level=ValidationLevel.INFO,
                    category="冗余引用",
                    message=f"引用定义 [^{ref_id}] 未被使用",
                    suggestion="删除未使用的引用定义"
                ))
                
        return issues
        
    def _validate_mermaid(
        self,
        file_path: str,
        content: str,
        sections: List[SectionInfo]
    ) -> List[ValidationIssue]:
        """验证Mermaid图表"""
        issues = []
        mermaid_count = self._count_mermaid_diagrams(content)
        
        if mermaid_count == 0:
            viz_section = None
            for s in sections:
                if s.section_type == SectionType.VISUALIZATIONS:
                    viz_section = s
                    break
                    
            if viz_section:
                issues.append(ValidationIssue(
                    file_path=file_path,
                    line_number=viz_section.line_start,
                    level=ValidationLevel.WARNING,
                    category="图表缺失",
                    message="可视化章节中未找到Mermaid图表",
                    suggestion="添加至少一个Mermaid图表"
                ))
        else:
            # 检查Mermaid语法基础
            for match in self.MERMAID_PATTERN.finditer(content):
                diagram_content = match.group(1)
                
                # 检查是否有图表类型声明
                valid_types = ['graph', 'flowchart', 'sequenceDiagram', 
                              'classDiagram', 'stateDiagram', 'gantt',
                              'pie', 'erDiagram', 'journey', 'gitGraph']
                has_type = any(
                    diagram_content.strip().lower().startswith(t.lower())
                    for t in valid_types
                )
                
                if not has_type:
                    line_num = content[:match.start()].count('\n') + 1
                    issues.append(ValidationIssue(
                        file_path=file_path,
                        line_number=line_num,
                        level=ValidationLevel.WARNING,
                        category="Mermaid语法",
                        message="Mermaid图表缺少有效的图表类型声明",
                        suggestion=f"使用有效的图表类型: {', '.join(valid_types)}"
                    ))
                    
        return issues
        
    def validate_file(self, file_path: Path) -> ValidationResult:
        """
        验证单个文件
        
        Args:
            file_path: Markdown文件路径
            
        Returns:
            验证结果
        """
        result = ValidationResult(file_path=str(file_path.relative_to(Path.cwd())))
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            result.is_valid = False
            result.issues.append(ValidationIssue(
                file_path=result.file_path,
                line_number=0,
                level=ValidationLevel.ERROR,
                category="文件读取",
                message=f"无法读取文件: {e}",
                suggestion="检查文件编码和权限"
            ))
            return result
            
        # 提取信息
        result.sections = self._extract_sections(content)
        result.formal_elements = self._extract_formal_elements(content)
        result.mermaid_count = self._count_mermaid_diagrams(content)
        result.has_header, result.formalization_level = self._check_header_meta(content)
        
        # 验证头部元信息
        if not result.has_header:
            result.issues.append(ValidationIssue(
                file_path=result.file_path,
                line_number=1,
                level=ValidationLevel.WARNING,
                category="头部元信息",
                message="缺少头部元信息（所属阶段）",
                suggestion='在标题后添加: > 所属阶段: Struct/ | 前置依赖: [] | 形式化等级: L1-L6'
            ))
            
        # 验证章节完整性
        result.issues.extend(self._validate_section_completeness(
            result.file_path, result.sections
        ))
        
        # 验证形式化元素
        result.issues.extend(self._validate_formal_elements(
            result.file_path, result.formal_elements, result.sections
        ))
        
        # 验证引用
        result.issues.extend(self._validate_references(
            result.file_path, content
        ))
        
        # 验证Mermaid
        result.issues.extend(self._validate_mermaid(
            result.file_path, content, result.sections
        ))
        
        # 计算评分
        error_count = sum(1 for i in result.issues if i.level == ValidationLevel.ERROR)
        warning_count = sum(1 for i in result.issues if i.level == ValidationLevel.WARNING)
        
        # 基础分100，错误扣10分，警告扣5分
        result.score = max(0, 100 - error_count * 10 - warning_count * 5)
        result.is_valid = error_count == 0
        
        return result
        
    def validate_directory(
        self,
        root_dir: Path,
        pattern: str = "**/*.md"
    ) -> List[ValidationResult]:
        """
        验证目录中的所有Markdown文件
        
        Args:
            root_dir: 根目录
            pattern: 文件匹配模式
            
        Returns:
            验证结果列表
        """
        results = []
        md_files = list(root_dir.glob(pattern))
        
        logger.info(f"发现 {len(md_files)} 个Markdown文件")
        
        for file_path in md_files:
            if self._should_skip_file(file_path):
                continue
                
            logger.debug(f"验证文件: {file_path}")
            result = self.validate_file(file_path)
            results.append(result)
            
        return results
        
    def generate_json_report(
        self,
        results: List[ValidationResult],
        output_path: Path
    ) -> None:
        """生成JSON报告"""
        report_data = {
            'scan_time': datetime.now().isoformat(),
            'summary': {
                'total_files': len(results),
                'valid_files': sum(1 for r in results if r.is_valid),
                'invalid_files': sum(1 for r in results if not r.is_valid),
                'total_issues': sum(len(r.issues) for r in results),
                'total_errors': sum(
                    sum(1 for i in r.issues if i.level == ValidationLevel.ERROR)
                    for r in results
                ),
                'total_warnings': sum(
                    sum(1 for i in r.issues if i.level == ValidationLevel.WARNING)
                    for r in results
                ),
                'average_score': round(
                    sum(r.score for r in results) / len(results), 2
                ) if results else 0
            },
            'files': [
                {
                    'file_path': r.file_path,
                    'is_valid': r.is_valid,
                    'score': r.score,
                    'formalization_level': r.formalization_level,
                    'mermaid_count': r.mermaid_count,
                    'formal_element_count': len(r.formal_elements),
                    'sections': [
                        {
                            'type': s.section_type.value if s.section_type else None,
                            'title': s.title,
                            'has_content': s.has_content
                        }
                        for s in r.sections
                    ],
                    'formal_elements': [
                        {
                            'type': e.element_type,
                            'id': e.full_id,
                            'line': e.line_number
                        }
                        for e in r.formal_elements
                    ],
                    'issues': [
                        {
                            'line': i.line_number,
                            'level': i.level.value,
                            'category': i.category,
                            'message': i.message,
                            'suggestion': i.suggestion
                        }
                        for i in r.issues
                    ]
                }
                for r in results
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
            
        logger.info(f"JSON报告已生成: {output_path}")
        
    def generate_markdown_report(
        self,
        results: List[ValidationResult],
        output_path: Path
    ) -> None:
        """生成Markdown报告"""
        lines = [
            "# 模板验证报告",
            "",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 统计摘要",
            "",
        ]
        
        total_files = len(results)
        valid_files = sum(1 for r in results if r.is_valid)
        total_issues = sum(len(r.issues) for r in results)
        total_errors = sum(
            sum(1 for i in r.issues if i.level == ValidationLevel.ERROR)
            for r in results
        )
        total_warnings = sum(
            sum(1 for i in r.issues if i.level == ValidationLevel.WARNING)
            for r in results
        )
        avg_score = round(sum(r.score for r in results) / len(results), 2) if results else 0
        
        lines.extend([
            f"| 指标 | 数值 |",
            f"|------|------|",
            f"| 总文件数 | {total_files} |",
            f"| 有效文件 | {valid_files} |",
            f"| 无效文件 | {total_files - valid_files} |",
            f"| 总问题数 | {total_issues} |",
            f"| 错误数 | {total_errors} |",
            f"| 警告数 | {total_warnings} |",
            f"| 平均得分 | {avg_score}/100 |",
            "",
            "## 问题详情",
            "",
        ])
        
        # 按错误级别排序的问题
        for result in sorted(results, key=lambda r: r.score):
            if not result.issues:
                continue
                
            lines.extend([
                f"### {result.file_path}",
                f"",
                f"**得分**: {result.score}/100 | **元素数**: {len(result.formal_elements)} | **图表数**: {result.mermaid_count}",
                f"",
            ])
            
            # 按级别分组
            errors = [i for i in result.issues if i.level == ValidationLevel.ERROR]
            warnings = [i for i in result.issues if i.level == ValidationLevel.WARNING]
            infos = [i for i in result.issues if i.level == ValidationLevel.INFO]
            
            if errors:
                lines.extend(["**错误**:", ""])
                for issue in errors:
                    lines.append(f"- ❌ **{issue.category}** (行 {issue.line_number}): {issue.message}")
                    if issue.suggestion:
                        lines.append(f"  - 💡 建议: {issue.suggestion}")
                lines.append("")
                
            if warnings:
                lines.extend(["**警告**:", ""])
                for issue in warnings[:10]:  # 最多显示10条警告
                    lines.append(f"- ⚠️ **{issue.category}** (行 {issue.line_number}): {issue.message}")
                if len(warnings) > 10:
                    lines.append(f"- ... 还有 {len(warnings) - 10} 条警告")
                lines.append("")
                
            if infos and len(lines) < 200:  # 限制报告长度
                lines.extend(["**提示**:", ""])
                for issue in infos[:5]:
                    lines.append(f"- ℹ️ {issue.message}")
                lines.append("")
                
        lines.extend([
            "",
            "---",
            "*由 template-validator.py 自动生成*",
        ])
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
            
        logger.info(f"Markdown报告已生成: {output_path}")


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='六段式模板验证器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                           # 验证当前目录
  %(prog)s -d ./docs                 # 验证指定目录
  %(prog)s --strict                  # 严格模式
  %(prog)s --output ./reports        # 指定输出目录
        """
    )
    
    parser.add_argument(
        '-d', '--directory',
        type=str,
        default='.',
        help='目标目录 (默认: 当前目录)'
    )
    
    parser.add_argument(
        '-p', '--pattern',
        type=str,
        default='**/*.md',
        help='文件匹配模式 (默认: **/*.md)'
    )
    
    parser.add_argument(
        '--strict',
        action='store_true',
        help='严格模式：将警告视为错误'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='./template-validation-reports',
        help='输出目录 (默认: ./template-validation-reports)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='配置文件路径 (JSON格式)'
    )
    
    args = parser.parse_args()
    
    # 加载配置
    config = {}
    if args.config:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
    # 创建验证器
    validator = TemplateValidator(config=config, strict_mode=args.strict)
    
    # 执行验证
    root_dir = Path(args.directory).resolve()
    results = validator.validate_directory(root_dir, args.pattern)
    
    # 创建输出目录
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成报告
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    json_path = output_dir / f"template-validation-{timestamp}.json"
    validator.generate_json_report(results, json_path)
    
    md_path = output_dir / f"template-validation-{timestamp}.md"
    validator.generate_markdown_report(results, md_path)
    
    # 输出摘要
    total_files = len(results)
    valid_files = sum(1 for r in results if r.is_valid)
    total_issues = sum(len(r.issues) for r in results)
    
    print(f"\n{'='*60}")
    print("模板验证完成")
    print(f"{'='*60}")
    print(f"总文件数: {total_files}")
    print(f"有效文件: {valid_files}")
    print(f"无效文件: {total_files - valid_files}")
    print(f"总问题数: {total_issues}")
    print(f"平均得分: {round(sum(r.score for r in results) / len(results), 2) if results else 0}/100")
    print(f"{'='*60}")
    print(f"报告已保存至: {output_dir}")
    
    return 0 if valid_files == total_files else 1


if __name__ == '__main__':
    exit(main())
