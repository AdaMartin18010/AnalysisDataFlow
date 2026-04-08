#!/usr/bin/env python3
"""
六段式模板结构检查器
检查文档是否符合AnalysisDataFlow六段式模板规范

用法:
    python template-structure-checker.py [--strict] [--fix]

选项:
    --strict  严格模式，发现问题时报错退出
    --fix     尝试自动修复（添加缺失的章节标题）

AGENTS.md规定的六段式模板:
    1. 概念定义 (Definitions)
    2. 属性推导 (Properties)
    3. 关系建立 (Relations)
    4. 论证过程 (Argumentation)
    5. 形式证明 / 工程论证 (Proof / Engineering Argument)
    6. 实例验证 (Examples)
    7. 可视化 (Visualizations)
    8. 引用参考 (References)
"""

import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple


# 六段式模板必需章节（中英文标题）
REQUIRED_SECTIONS = [
    {
        'names': ['概念定义', 'Definitions', '定义'],
        'id': 'definitions',
        'required': True,
        'min_content': 50  # 最小内容长度
    },
    {
        'names': ['属性推导', 'Properties', '性质推导', '引理'],
        'id': 'properties',
        'required': True,
        'min_content': 30
    },
    {
        'names': ['关系建立', 'Relations', '关系', '关联'],
        'id': 'relations',
        'required': False,  # 可选，但推荐
        'min_content': 20
    },
    {
        'names': ['论证过程', 'Argumentation', '论证'],
        'id': 'argumentation',
        'required': False,
        'min_content': 50
    },
    {
        'names': ['形式证明', '工程论证', 'Proof', 'Engineering Argument'],
        'id': 'proof',
        'required': False,
        'min_content': 30
    },
    {
        'names': ['实例验证', 'Examples', '实例', '示例', '验证'],
        'id': 'examples',
        'required': True,
        'min_content': 50
    },
    {
        'names': ['可视化', 'Visualizations', '图表', 'Mermaid'],
        'id': 'visualizations',
        'required': True,
        'min_content': 20  # Mermaid代码块长度
    },
    {
        'names': ['引用参考', 'References', '参考', '引用'],
        'id': 'references',
        'required': True,
        'min_content': 10
    }
]

# 元数据检查
METADATA_PATTERNS = {
    'stage': re.compile(r'所属阶段[:：]\s*(Struct|Knowledge|Flink)', re.IGNORECASE),
    'prerequisites': re.compile(r'前置依赖[:：]'),
    'formalization': re.compile(r'形式化等级[:：]\s*L\d', re.IGNORECASE)
}


class TemplateChecker:
    """六段式模板结构检查器"""
    
    def __init__(self):
        self.issues = []
        self.stats = {
            'files_checked': 0,
            'compliant_files': 0,
            'non_compliant_files': 0,
            'missing_sections': defaultdict(int),
            'missing_metadata': defaultdict(int)
        }
    
    def check_document(self, file_path: Path) -> dict:
        """检查单个文档的结构合规性"""
        try:
            content = file_path.read_text(encoding='utf-8')
            rel_path = str(file_path.relative_to('.')).replace('\\', '/')
        except Exception as e:
            return {
                'file': str(file_path),
                'error': f'Could not read file: {e}',
                'compliant': False
            }
        
        # 检查是否应该应用六段式（核心文档）
        if not self._should_apply_six_section(content, file_path):
            return {
                'file': rel_path,
                'skipped': True,
                'reason': 'Not a core document'
            }
        
        result = {
            'file': rel_path,
            'compliant': True,
            'sections': {},
            'metadata': {},
            'issues': [],
            'warnings': []
        }
        
        # 1. 检查元数据
        result['metadata'] = self._check_metadata(content)
        
        # 2. 检查章节结构
        sections_found = self._find_sections(content)
        result['sections'] = sections_found
        
        # 3. 验证必需章节
        for section_def in REQUIRED_SECTIONS:
            section_id = section_def['id']
            found = sections_found.get(section_id, {}).get('found', False)
            
            if section_def['required'] and not found:
                result['issues'].append({
                    'type': 'missing_section',
                    'section': section_id,
                    'message': f"Missing required section: {', '.join(section_def['names'])}"
                })
                result['compliant'] = False
                self.stats['missing_sections'][section_id] += 1
            elif found and section_def['required']:
                # 检查内容长度
                content_length = len(sections_found[section_id].get('content', ''))
                if content_length < section_def['min_content']:
                    result['warnings'].append({
                        'type': 'short_section',
                        'section': section_id,
                        'message': f"Section '{section_id}' content may be too short ({content_length} chars, min {section_def['min_content']})"
                    })
        
        # 4. 检查定理编号
        theorem_check = self._check_theorem_ids(content, file_path)
        result['theorem_check'] = theorem_check
        
        if theorem_check['issues']:
            result['issues'].extend(theorem_check['issues'])
        
        # 5. 检查引用格式
        citation_check = self._check_citations(content)
        result['citation_check'] = citation_check
        
        if citation_check['issues']:
            result['warnings'].extend(citation_check['issues'])
        
        # 更新统计
        if result['compliant'] and not result['issues']:
            self.stats['compliant_files'] += 1
        else:
            self.stats['non_compliant_files'] += 1
        
        return result
    
    def _should_apply_six_section(self, content: str, file_path: Path) -> bool:
        """判断是否应该对文档应用六段式检查"""
        # 跳过特定文件
        skip_patterns = [
            'README', 'CHANGELOG', 'CONTRIBUTING', 'LICENSE',
            'QUICK-START', 'FAQ', 'GLOSSARY', 'ROADMAP',
            'INDEX', 'NAVIGATION', 'PROJECT-TRACKING'
        ]
        
        file_name = file_path.name.upper()
        for pattern in skip_patterns:
            if pattern in file_name:
                return False
        
        # 检查是否在核心目录
        core_dirs = ['Struct', 'Knowledge', 'Flink']
        path_str = str(file_path)
        for d in core_dirs:
            if f'/{d}/' in path_str or path_str.startswith(f'{d}/'):
                # 检查文档是否有"所属阶段"标记
                if re.search(r'所属阶段[:：]', content):
                    return True
        
        return False
    
    def _check_metadata(self, content: str) -> dict:
        """检查文档元数据"""
        metadata = {}
        
        # 提取标题后的元数据块
        meta_match = re.search(r'^>\s*所属阶段[:：][^\n]+(\n>\s*[^\n]+)*', content, re.MULTILINE)
        
        if meta_match:
            metadata['has_metadata_block'] = True
            meta_block = meta_match.group(0)
            
            for key, pattern in METADATA_PATTERNS.items():
                match = pattern.search(meta_block)
                metadata[f'has_{key}'] = match is not None
                if match:
                    metadata[key] = match.group(0)
        else:
            metadata['has_metadata_block'] = False
            for key in METADATA_PATTERNS.keys():
                metadata[f'has_{key}'] = False
                self.stats['missing_metadata'][key] += 1
        
        return metadata
    
    def _find_sections(self, content: str) -> dict:
        """查找文档中的章节"""
        sections = {}
        lines = content.split('\n')
        
        for section_def in REQUIRED_SECTIONS:
            section_id = section_def['id']
            sections[section_id] = {'found': False, 'title': None, 'content': ''}
            
            # 查找章节标题（支持 ## 和 ### 级别）
            for i, line in enumerate(lines):
                # 匹配章节标题
                for name in section_def['names']:
                    # ## 1. 概念定义 (Definitions)
                    pattern = rf'^##+\s*\d*\.?\s*{re.escape(name)}'
                    if re.search(pattern, line, re.IGNORECASE):
                        sections[section_id]['found'] = True
                        sections[section_id]['title'] = line.strip()
                        sections[section_id]['line'] = i + 1
                        
                        # 提取章节内容（到下一个同级或更高级标题）
                        content_lines = []
                        for j in range(i + 1, len(lines)):
                            next_line = lines[j]
                            # 检查是否是下一个章节
                            if re.match(r'^##+\s', next_line):
                                break
                            content_lines.append(next_line)
                        
                        sections[section_id]['content'] = '\n'.join(content_lines)
                        break
                
                if sections[section_id]['found']:
                    break
        
        return sections
    
    def _check_theorem_ids(self, content: str, file_path: Path) -> dict:
        """检查定理编号的规范性"""
        result = {'valid': True, 'issues': [], 'theorems': []}
        
        # 定理编号模式
        theorem_pattern = re.compile(r'(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d{2})-(\d{2})')
        
        matches = theorem_pattern.findall(content)
        
        # 从文件路径推断期望的阶段
        path_str = str(file_path)
        expected_stage = None
        if '/Struct/' in path_str or path_str.startswith('Struct/'):
            expected_stage = 'S'
        elif '/Knowledge/' in path_str or path_str.startswith('Knowledge/'):
            expected_stage = 'K'
        elif '/Flink/' in path_str or path_str.startswith('Flink/'):
            expected_stage = 'F'
        
        for match in matches:
            thm_type, stage, doc_num, seq_num = match
            full_id = f"{thm_type}-{stage}-{doc_num}-{seq_num}"
            result['theorems'].append(full_id)
            
            # 检查阶段是否匹配
            if expected_stage and stage != expected_stage:
                result['issues'].append({
                    'type': 'stage_mismatch',
                    'theorem': full_id,
                    'message': f"Theorem stage '{stage}' doesn't match expected '{expected_stage}' for this directory"
                })
                result['valid'] = False
        
        return result
    
    def _check_citations(self, content: str) -> dict:
        """检查引用格式"""
        result = {'valid': True, 'issues': []}
        
        # 查找 [^n] 格式的引用
        citation_pattern = re.compile(r'\[\^(\d+)\]')
        citations = citation_pattern.findall(content)
        
        # 查找引用列表
        ref_section = re.search(r'##+\s*引用参考.*$([\s\S]*)', content, re.MULTILINE | re.IGNORECASE)
        
        if citations and not ref_section:
            result['issues'].append({
                'type': 'missing_references',
                'message': f"Document has {len(citations)} citations but no References section"
            })
        
        # 检查是否有未定义的引用
        if ref_section:
            ref_content = ref_section.group(1)
            defined_refs = set(re.findall(r'^\[\^(\d+)\]:', ref_content, re.MULTILINE))
            used_refs = set(citations)
            
            undefined = used_refs - defined_refs
            if undefined:
                result['issues'].append({
                    'type': 'undefined_citations',
                    'message': f"Citations not defined in References: {', '.join(f'[^{r}]' for r in sorted(undefined))}"
                })
        
        return result
    
    def check_all(self, directories: List[str]) -> List[dict]:
        """检查所有文档"""
        results = []
        
        for directory in directories:
            dir_path = Path(directory)
            if not dir_path.exists():
                continue
            
            for md_file in dir_path.rglob('*.md'):
                # 跳过隐藏目录
                if any(part.startswith('.') for part in md_file.parts):
                    continue
                
                self.stats['files_checked'] += 1
                result = self.check_document(md_file)
                
                if not result.get('skipped'):
                    results.append(result)
        
        return results


def generate_report(results: List[dict], stats: dict, output_path: Path = None) -> str:
    """生成检查报告"""
    lines = [
        "# Six-Section Template Structure Check Report",
        "",
        f"**Generated**: {datetime.now().isoformat()}",
        "",
        "## Summary",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Files Checked | {stats['files_checked']} |",
        f"| ✅ Compliant | {stats['compliant_files']} |",
        f"| ❌ Non-Compliant | {stats['non_compliant_files']} |",
        ""
    ]
    
    if stats['missing_sections']:
        lines.extend([
            "## Missing Sections (Most Common)",
            "",
            "| Section | Count |",
            "|---------|-------|"
        ])
        
        for section, count in sorted(stats['missing_sections'].items(), key=lambda x: -x[1]):
            lines.append(f"| {section} | {count} |")
        
        lines.append("")
    
    if stats['missing_metadata']:
        lines.extend([
            "## Missing Metadata (Most Common)",
            "",
            "| Metadata | Count |",
            "|----------|-------|"
        ])
        
        for meta, count in sorted(stats['missing_metadata'].items(), key=lambda x: -x[1]):
            lines.append(f"| {meta} | {count} |")
        
        lines.append("")
    
    # 不合规文档详情
    non_compliant = [r for r in results if not r.get('skipped') and (not r.get('compliant') or r.get('issues'))]
    
    if non_compliant:
        lines.extend([
            "## ❌ Non-Compliant Documents",
            "",
            "| File | Issues | Warnings |",
            "|------|--------|----------|"
        ])
        
        for doc in sorted(non_compliant, key=lambda x: x['file']):
            issue_count = len(doc.get('issues', []))
            warning_count = len(doc.get('warnings', []))
            lines.append(f"| {doc['file']} | {issue_count} | {warning_count} |")
        
        lines.append("")
        
        # 详细问题
        lines.extend([
            "### Detailed Issues",
            ""
        ])
        
        for doc in sorted(non_compliant, key=lambda x: x['file'])[:20]:  # 限制显示数量
            if doc.get('issues'):
                lines.extend([
                    f"#### {doc['file']}",
                    ""
                ])
                
                for issue in doc['issues']:
                    lines.append(f"- **{issue['type']}**: {issue['message']}")
                
                if doc.get('warnings'):
                    for warning in doc['warnings'][:3]:  # 只显示前3个警告
                        lines.append(f"- ⚠️ **{warning['type']}**: {warning['message']}")
                
                lines.append("")
    
    # 合规率
    if stats['files_checked'] > 0:
        compliance_rate = stats['compliant_files'] / (stats['compliant_files'] + stats['non_compliant_files']) * 100
        lines.extend([
            "## Compliance Rate",
            "",
            f"**{compliance_rate:.1f}%** ({stats['compliant_files']}/{stats['compliant_files'] + stats['non_compliant_files']})",
            ""
        ])
    
    lines.extend([
        "## Recommendations",
        "",
        "1. Ensure all core documents have the six required sections",
        "2. Add metadata block with stage, prerequisites, and formalization level",
        "3. Include at least one Mermaid diagram in each document",
        "4. Use [^n] format for citations and define them in References section",
        "5. Follow theorem numbering convention: Type-Stage-DocNum-SeqNum",
        "",
        "---",
        "",
        "*This report was generated by template-structure-checker.py*"
    ])
    
    report = '\n'.join(lines)
    
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding='utf-8')
    
    return report


def main():
    parser = argparse.ArgumentParser(
        description='Check six-section template compliance in Markdown documents'
    )
    parser.add_argument(
        '--strict', action='store_true',
        help='Exit with error code if non-compliant documents found'
    )
    parser.add_argument(
        '--fix', action='store_true',
        help='Attempt to auto-fix common issues (not implemented)'
    )
    parser.add_argument(
        '--output', '-o', type=str,
        default='reports/template-structure-report.md',
        help='Output report path'
    )
    parser.add_argument(
        '--dirs', nargs='+',
        default=['Struct', 'Knowledge', 'Flink'],
        help='Directories to scan'
    )
    
    args = parser.parse_args()
    
    print("🔍 Checking six-section template compliance...")
    
    checker = TemplateChecker()
    results = checker.check_all(args.dirs)
    
    print(f"   Files checked: {checker.stats['files_checked']}")
    print(f"   Compliant: {checker.stats['compliant_files']}")
    print(f"   Non-compliant: {checker.stats['non_compliant_files']}")
    
    # 生成报告
    output_path = Path(args.output)
    report = generate_report(results, checker.stats, output_path)
    print(f"\n📄 Report saved to: {output_path}")
    
    # 严格模式退出
    if args.strict and checker.stats['non_compliant_files'] > 0:
        print(f"\n❌ Found {checker.stats['non_compliant_files']} non-compliant documents")
        sys.exit(1)
    
    print("\n✅ Template structure check completed")
    sys.exit(0)


if __name__ == '__main__':
    main()
