#!/usr/bin/env python3
"""
形式化元素完整性检查器
检查文档中的定理、定义、引理等形式化元素的完整性

用法:
    python formal-element-checker.py [--strict] [--warning]

选项:
    --strict   严格模式，发现问题时报错退出
    --warning  仅警告级别，不阻塞合并（默认）

AGENTS.md规定的形式化元素:
    - 定理 (Thm): Thm-{Stage}-{DocNum}-{SeqNum}
    - 定义 (Def): Def-{Stage}-{DocNum}-{SeqNum}
    - 引理 (Lemma): Lemma-{Stage}-{DocNum}-{SeqNum}
    - 命题 (Prop): Prop-{Stage}-{DocNum}-{SeqNum}
    - 推论 (Cor): Cor-{Stage}-{DocNum}-{SeqNum}
"""

import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple, Set


# 形式化元素模式
FORMAL_ELEMENT_PATTERNS = {
    'Thm': re.compile(r'Thm-[SKF]-\d{2}-\d{2}'),
    'Def': re.compile(r'Def-[SKF]-\d{2}-\d{2}'),
    'Lemma': re.compile(r'Lemma-[SKF]-\d{2}-\d{2}'),
    'Prop': re.compile(r'Prop-[SKF]-\d{2}-\d{2}'),
    'Cor': re.compile(r'Cor-[SKF]-\d{2}-\d{2}')
}

# 六段式必需章节
REQUIRED_SECTIONS = [
    {
        'names': ['概念定义', 'Definitions', '定义'],
        'id': 'definitions',
        'required': True,
        'check_elements': ['Def']  # 此章节应包含定义
    },
    {
        'names': ['属性推导', 'Properties', '性质推导'],
        'id': 'properties',
        'required': True,
        'check_elements': ['Lemma', 'Prop']  # 此章节应包含引理/命题
    },
    {
        'names': ['形式证明', 'Proof', '工程论证', 'Engineering Argument'],
        'id': 'proof',
        'required': False,
        'check_elements': ['Thm']  # 此章节应包含定理
    },
    {
        'names': ['实例验证', 'Examples', '实例', '示例'],
        'id': 'examples',
        'required': True,
        'check_elements': []  # 示例不强制要求形式化元素
    },
    {
        'names': ['可视化', 'Visualizations', '图表'],
        'id': 'visualizations',
        'required': True,
        'check_elements': []  # 可视化章节
    },
    {
        'names': ['引用参考', 'References', '参考', '引用'],
        'id': 'references',
        'required': True,
        'check_elements': []  # 引用章节
    }
]


class FormalElementChecker:
    """形式化元素完整性检查器"""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.stats = {
            'files_checked': 0,
            'files_with_issues': 0,
            'total_elements': defaultdict(int),
            'missing_sections': defaultdict(int),
            'orphaned_elements': []  # 未在正确章节中的元素
        }
    
    def extract_formal_elements(self, content: str) -> Dict[str, List[Dict]]:
        """提取文档中所有形式化元素"""
        elements = defaultdict(list)
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for elem_type, pattern in FORMAL_ELEMENT_PATTERNS.items():
                matches = pattern.findall(line)
                for match in matches:
                    elements[elem_type].append({
                        'id': match,
                        'line': line_num,
                        'context': line.strip()[:100]
                    })
        
        return elements
    
    def find_sections(self, content: str) -> Dict[str, Dict]:
        """查找文档中的章节及其范围"""
        sections = {}
        lines = content.split('\n')
        section_positions = []
        
        # 查找所有章节标题
        for i, line in enumerate(lines):
            for section_def in REQUIRED_SECTIONS:
                for name in section_def['names']:
                    pattern = rf'^##+\s*\d*\.?\s*{re.escape(name)}'
                    if re.search(pattern, line, re.IGNORECASE):
                        section_positions.append({
                            'id': section_def['id'],
                            'name': name,
                            'line': i,
                            'title': line.strip()
                        })
                        break
        
        # 按行号排序
        section_positions.sort(key=lambda x: x['line'])
        
        # 确定每个章节的范围
        for i, sec in enumerate(section_positions):
            start_line = sec['line']
            end_line = section_positions[i + 1]['line'] if i + 1 < len(section_positions) else len(lines)
            
            sections[sec['id']] = {
                'title': sec['title'],
                'start_line': start_line,
                'end_line': end_line,
                'content': '\n'.join(lines[start_line:end_line])
            }
        
        return sections
    
    def check_document(self, file_path: Path) -> Dict:
        """检查单个文档的形式化元素完整性"""
        try:
            content = file_path.read_text(encoding='utf-8')
            rel_path = str(file_path.relative_to('.')).replace('\\', '/')
        except Exception as e:
            return {
                'file': str(file_path),
                'error': f'Could not read file: {e}',
                'compliant': False
            }
        
        # 检查是否应该应用检查（核心文档）
        if not self._should_check(content, file_path):
            return {
                'file': rel_path,
                'skipped': True,
                'reason': 'Not a core formal document'
            }
        
        self.stats['files_checked'] += 1
        
        result = {
            'file': rel_path,
            'compliant': True,
            'issues': [],
            'warnings': [],
            'elements': {},
            'sections': {}
        }
        
        # 1. 提取所有形式化元素
        elements = self.extract_formal_elements(content)
        result['elements'] = elements
        
        for elem_type, elems in elements.items():
            self.stats['total_elements'][elem_type] += len(elems)
        
        # 2. 查找章节
        sections = self.find_sections(content)
        result['sections'] = sections
        
        # 3. 检查必需章节是否存在
        for section_def in REQUIRED_SECTIONS:
            if section_def['required'] and section_def['id'] not in sections:
                result['issues'].append({
                    'type': 'missing_section',
                    'section': section_def['id'],
                    'message': f"Missing required section: {', '.join(section_def['names'])}"
                })
                result['compliant'] = False
                self.stats['missing_sections'][section_def['id']] += 1
        
        # 4. 检查形式化元素是否在正确的章节中
        for elem_type, expected_sections in [
            ('Def', ['definitions']),
            ('Lemma', ['properties', 'argumentation']),
            ('Prop', ['properties', 'argumentation']),
            ('Thm', ['proof', 'argumentation']),
            ('Cor', ['proof', 'properties'])
        ]:
            for elem in elements.get(elem_type, []):
                elem_line = elem['line']
                in_correct_section = False
                
                for sec_id in expected_sections:
                    if sec_id in sections:
                        sec = sections[sec_id]
                        if sec['start_line'] <= elem_line <= sec['end_line']:
                            in_correct_section = True
                            break
                
                # 如果不在任何正确的章节中，记录警告
                if not in_correct_section and sections:
                    # 检查是否在文档的任何章节中
                    in_any_section = any(
                        sec['start_line'] <= elem_line <= sec['end_line']
                        for sec in sections.values()
                    )
                    
                    if in_any_section:
                        result['warnings'].append({
                            'type': 'element_in_wrong_section',
                            'element': elem['id'],
                            'element_type': elem_type,
                            'line': elem_line,
                            'message': f"{elem_type} {elem['id']} may be in the wrong section (expected in {', '.join(expected_sections)})"
                        })
        
        # 5. 检查形式化元素定义格式
        for elem_type, elems in elements.items():
            for elem in elems:
                # 检查定义格式（应在行首或紧跟在破折号后）
                line = content.split('\n')[elem['line'] - 1]
                
                # 检查是否有适当的定义前缀（如 "**定义 X**" 或 "Def-X-X-X"）
                if not re.search(rf'(^|\*\*)\s*{re.escape(elem["id"])}\s*[：:]', line):
                    if not re.search(rf'\*\*{elem["id"]}\*\*', line):
                        result['warnings'].append({
                            'type': 'element_format',
                            'element': elem['id'],
                            'line': elem['line'],
                            'message': f"Consider using bold format: **{elem['id']}**: description"
                        })
        
        # 6. 检查是否有孤立的定义（定义后没有使用）
        if 'Def' in elements:
            for def_elem in elements['Def']:
                def_id = def_elem['id']
                # 简单的检查：定义是否在文档中被引用（除了定义本身）
                # 这里简化处理，实际可能需要更复杂的分析
                pass
        
        # 7. 检查六段式元数据
        if '所属阶段' not in content:
            result['warnings'].append({
                'type': 'missing_metadata',
                'message': "Missing '所属阶段' metadata block"
            })
        
        if '形式化等级' not in content:
            result['warnings'].append({
                'type': 'missing_metadata',
                'message': "Missing '形式化等级' in metadata"
            })
        
        # 更新合规状态
        if result['issues']:
            result['compliant'] = False
            self.stats['files_with_issues'] += 1
        
        return result
    
    def _should_check(self, content: str, file_path: Path) -> bool:
        """判断是否应该对文档进行形式化元素检查"""
        # 跳过特定文件
        skip_patterns = [
            'README', 'CHANGELOG', 'CONTRIBUTING', 'LICENSE',
            'QUICK-START', 'FAQ', 'GLOSSARY', 'ROADMAP',
            'INDEX', 'NAVIGATION', 'PROJECT-TRACKING', 'BEST-PRACTICES',
            'CHEATSHEET', 'CHECKLIST', 'COMPLETION-REPORT'
        ]
        
        file_name = file_path.name.upper()
        for pattern in skip_patterns:
            if pattern in file_name:
                return False
        
        # 跳过特定目录类型（非核心形式化文档）
        skip_dir_patterns = [
            '/98-exercises/', '/10-case-studies/',
            '/09-anti-patterns/', '/09-practices/09.01-case-studies/',
            '/09-practices/09.03-performance-tuning/05-vs-competitors/'
        ]
        path_str_norm = str(file_path).replace('\\', '/').upper()
        for pattern in skip_dir_patterns:
            if pattern.upper() in path_str_norm:
                return False
        
        # 跳过特定类型文档
        skip_name_prefixes = [
            'Proof-Chains-', 'PROOF-GRAPH-', 'PROOF-CHAIN-',
            'case-', 'anti-pattern-', 'exercise-',
            'academic-frontier-', 'research-trends-analysis-',
            'project-supplementation-plan'
        ]
        for prefix in skip_name_prefixes:
            if file_name.startswith(prefix.upper()):
                return False
        
        # 跳过补充/索引类文档（文件名包含特定关键词）
        skip_name_keywords = [
            'supplement', '-supplement-', 'derivation-chain',
            'expressiveness-hierarchy-supplement'
        ]
        for keyword in skip_name_keywords:
            if keyword.upper() in file_name:
                return False
        
        # 跳过非核心形式化文档类型
        skip_doc_types = [
            '-matrix', '-migration-guide', '-complete-guide',
            '-architecture', '-derivation-chain'
        ]
        for suffix in skip_doc_types:
            if suffix.upper() in file_name:
                return False
        
        # 检查是否在核心目录
        core_dirs = ['Struct', 'Knowledge', 'Flink']
        path_str = str(file_path).replace('\\', '/')
        for d in core_dirs:
            if f'/{d}/' in path_str or path_str.startswith(f'{d}/'):
                # 检查是否有形式化元素
                has_formal = any(
                    pattern.search(content)
                    for pattern in FORMAL_ELEMENT_PATTERNS.values()
                )
                return has_formal
        
        return False
    
    def check_all(self, directories: List[str]) -> List[Dict]:
        """检查所有文档"""
        results = []
        
        for directory in directories:
            dir_path = Path(directory)
            if not dir_path.exists():
                continue
            
            for md_file in dir_path.rglob('*.md'):
                if any(part.startswith('.') for part in md_file.parts):
                    continue
                
                result = self.check_document(md_file)
                if not result.get('skipped'):
                    results.append(result)
        
        return results


def generate_report(results: List[Dict], stats: Dict, output_path: Path = None) -> str:
    """生成检查报告"""
    lines = [
        "# Formal Element Integrity Check Report",
        "",
        f"**Generated**: {datetime.now().isoformat()}",
        "",
        "## Summary",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Files Checked | {stats['files_checked']} |",
        f"| Files with Issues | {stats['files_with_issues']} |",
        ""
    ]
    
    # 形式化元素统计
    if stats['total_elements']:
        lines.extend([
            "## Formal Elements Found",
            "",
            "| Type | Count |",
            "|------|-------|"
        ])
        
        type_names = {
            'Thm': 'Theorem (定理)',
            'Def': 'Definition (定义)',
            'Lemma': 'Lemma (引理)',
            'Prop': 'Proposition (命题)',
            'Cor': 'Corollary (推论)'
        }
        
        for elem_type, count in sorted(stats['total_elements'].items()):
            name = type_names.get(elem_type, elem_type)
            lines.append(f"| {name} | {count} |")
        
        lines.append("")
    
    # 缺失章节统计
    if stats['missing_sections']:
        lines.extend([
            "## Missing Sections",
            "",
            "| Section | Count |",
            "|---------|-------|"
        ])
        
        for section, count in sorted(stats['missing_sections'].items()):
            lines.append(f"| {section} | {count} |")
        
        lines.append("")
    
    # 问题文件详情
    non_compliant = [r for r in results if not r.get('skipped') and (not r.get('compliant') or r.get('issues'))]
    
    if non_compliant:
        lines.extend([
            "## ❌ Files with Issues",
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
        
        for doc in sorted(non_compliant, key=lambda x: x['file'])[:20]:
            if doc.get('issues'):
                lines.extend([
                    f"#### {doc['file']}",
                    ""
                ])
                
                for issue in doc['issues']:
                    lines.append(f"- **{issue['type']}**: {issue['message']}")
                
                if doc.get('warnings'):
                    for warning in doc['warnings'][:3]:
                        lines.append(f"- ⚠️ **{warning['type']}**: {warning['message']}")
                
                lines.append("")
    
    # 只有警告的文件
    warning_only = [r for r in results if not r.get('skipped') and r.get('compliant') and r.get('warnings')]
    
    if warning_only:
        lines.extend([
            "## ⚠️ Files with Warnings Only",
            "",
            "| File | Warnings |",
            "|------|----------|"
        ])
        
        for doc in sorted(warning_only, key=lambda x: x['file']):
            warning_count = len(doc.get('warnings', []))
            lines.append(f"| {doc['file']} | {warning_count} |")
        
        lines.append("")
    
    # 合规率
    if stats['files_checked'] > 0:
        compliant_count = stats['files_checked'] - stats['files_with_issues']
        compliance_rate = compliant_count / stats['files_checked'] * 100
        lines.extend([
            "## Compliance Rate",
            "",
            f"**{compliance_rate:.1f}%** ({compliant_count}/{stats['files_checked']})",
            ""
        ])
    
    lines.extend([
        "## Recommendations",
        "",
        "1. Ensure all formal elements follow the naming convention: Type-Stage-DocNum-SeqNum",
        "2. Place definitions in the '概念定义' section",
        "3. Place lemmas and propositions in the '属性推导' section",
        "4. Place theorems in the '形式证明' section",
        "5. Use bold format for element definitions: **Element-ID**: description",
        "6. Include '所属阶段' and '形式化等级' in the metadata block",
        "",
        "---",
        "",
        "*This report was generated by formal-element-checker.py*",
        "*Status: Warning level (non-blocking unless --strict is used)*"
    ])
    
    report = '\n'.join(lines)
    
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding='utf-8')
    
    return report


def main():
    parser = argparse.ArgumentParser(
        description='Check formal element integrity in Markdown documents'
    )
    parser.add_argument(
        '--strict', action='store_true',
        help='Exit with error code if issues found (blocking mode)'
    )
    parser.add_argument(
        '--warning', action='store_true',
        help='Warning level only (non-blocking, default)'
    )
    parser.add_argument(
        '--output', '-o', type=str,
        default='reports/formal-element-check-report.md',
        help='Output report path'
    )
    parser.add_argument(
        '--dirs', nargs='+',
        default=['Struct', 'Knowledge', 'Flink'],
        help='Directories to scan'
    )
    
    args = parser.parse_args()
    
    print("🔍 Checking formal element integrity...")
    
    checker = FormalElementChecker()
    results = checker.check_all(args.dirs)
    
    total_elements = sum(checker.stats['total_elements'].values())
    
    print(f"   Files checked: {checker.stats['files_checked']}")
    print(f"   Files with issues: {checker.stats['files_with_issues']}")
    print(f"   Total formal elements: {total_elements}")
    
    if checker.stats['total_elements']:
        print("   Elements by type:")
        for elem_type, count in sorted(checker.stats['total_elements'].items()):
            print(f"     - {elem_type}: {count}")
    
    # 生成报告
    output_path = Path(args.output)
    report = generate_report(results, checker.stats, output_path)
    print(f"\n📄 Report saved to: {output_path}")
    
    # 确定退出码
    if args.strict and checker.stats['files_with_issues'] > 0:
        print(f"\n❌ Found {checker.stats['files_with_issues']} files with issues (strict mode)")
        sys.exit(1)
    elif checker.stats['files_with_issues'] > 0:
        print(f"\n⚠️ Found {checker.stats['files_with_issues']} files with issues (warning level)")
        sys.exit(0)  # 警告级别不返回错误码
    
    print("\n✅ All files passed formal element check")
    sys.exit(0)


if __name__ == '__main__':
    main()
