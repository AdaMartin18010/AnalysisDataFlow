#!/usr/bin/env python3
"""
六段式模板验证器
功能：
- 验证文档六段式结构
- 检查定理/定义编号格式
- 验证Mermaid图表存在性
- 生成合规报告

作者: AnalysisDataFlow Toolchain Team
版本: 1.0.0
日期: 2026-04-11
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
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path).resolve()
        self.issues: List[ValidationIssue] = []
        self.formal_elements: Dict[str, List[str]] = defaultdict(list)
        
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
        
        return issues
    
    def run_validation(self) -> Tuple[List[ValidationIssue], ValidationStats]:
        """运行完整验证"""
        print("📐 Six-Section Template Validator")
        print("=" * 50)
        
        files = self.scan_target_files()
        print(f"\n📁 Found {len(files)} target files")
        
        all_issues = []
        compliant_count = 0
        
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
        return all_issues, stats
    
    def generate_report(self, output_path: str, stats: ValidationStats):
        """生成验证报告"""
        report = {
            'version': '1.0.0',
            'validator': 'Six-Section Template Validator',
            'stats': asdict(stats),
            'issues': [asdict(issue) for issue in self.issues],
            'formal_elements_summary': {
                elem_type: len(elements) 
                for elem_type, elements in self.formal_elements.items()
            },
            'compliance_rate': round(stats.compliant_files / stats.total_files * 100, 2) if stats.total_files > 0 else 0
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        return report


def main():
    parser = argparse.ArgumentParser(description='Six-Section Template Validator')
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
        
    print(f"\n✅ Report saved to: {args.output}")
    
    if args.fail_on_error and stats.by_severity.get('error', 0) > 0:
        return 1
    return 0


if __name__ == '__main__':
    exit(main())
