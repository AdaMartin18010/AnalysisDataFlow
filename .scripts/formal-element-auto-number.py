#!/usr/bin/env python3
"""
形式化元素自动编号工具
功能：
- 自动检测未编号定理/定义
- 生成唯一编号
- 检查编号冲突
- 自动修复建议

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
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
import argparse


@dataclass
class FormalElement:
    """形式化元素记录"""
    element_type: str  # 'theorem', 'definition', 'lemma', 'proposition', 'corollary'
    stage: str  # 'S', 'K', 'F'
    doc_num: str
    seq_num: int
    full_id: str
    file_path: str
    line_number: int
    content: str
    title: str


@dataclass
class NumberingIssue:
    """编号问题记录"""
    file_path: str
    line_number: int
    issue_type: str  # 'missing_number', 'duplicate_number', 'invalid_format', 'wrong_sequence'
    element_type: str
    current_text: str
    suggestion: str
    auto_fix: Optional[str]


class FormalElementAutoNumber:
    """形式化元素自动编号器"""
    
    # 元素类型映射
    ELEMENT_TYPES = {
        'theorem': 'Thm',
        'definition': 'Def',
        'lemma': 'Lemma',
        'proposition': 'Prop',
        'corollary': 'Cor'
    }
    
    # 检测模式（中文和英文）
    DETECTION_PATTERNS = {
        'theorem': [
            r'\*\*定理\s*\d*\s*[:：]',
            r'\*\*Theorem\s*\d*\s*:',
            r'^#{1,4}\s+定理\s*\d*',
            r'^#{1,4}\s+Theorem\s*\d*'
        ],
        'definition': [
            r'\*\*定义\s*\d*\s*[:：]',
            r'\*\*Definition\s*\d*\s*:',
            r'^#{1,4}\s+定义\s*\d*',
            r'^#{1,4}\s+Definition\s*\d*'
        ],
        'lemma': [
            r'\*\*引理\s*\d*\s*[:：]',
            r'\*\*Lemma\s*\d*\s*:',
            r'^#{1,4}\s+引理\s*\d*',
            r'^#{1,4}\s+Lemma\s*\d*'
        ],
        'proposition': [
            r'\*\*命题\s*\d*\s*[:：]',
            r'\*\*Proposition\s*\d*\s*:',
            r'^#{1,4}\s+命题\s*\d*',
            r'^#{1,4}\s+Proposition\s*\d*'
        ],
        'corollary': [
            r'\*\*推论\s*\d*\s*[:：]',
            r'\*\*Corollary\s*\d*\s*:',
            r'^#{1,4}\s+推论\s*\d*',
            r'^#{1,4}\s+Corollary\s*\d*'
        ]
    }
    
    # 已编号元素的匹配模式
    NUMBERED_PATTERN = re.compile(
        r'(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d{2})-(\d{2,3})'
    )
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path).resolve()
        self.elements: List[FormalElement] = []
        self.issues: List[NumberingIssue] = []
        self.existing_numbers: Dict[str, Set[str]] = defaultdict(set)
        self.next_sequence: Dict[str, int] = defaultdict(lambda: 1)
        
    def scan_all_files(self) -> List[Path]:
        """扫描所有Markdown文件"""
        md_files = []
        patterns = ["Struct/**/*.md", "Knowledge/**/*.md", "Flink/**/*.md"]
        
        for pattern in patterns:
            files = glob.glob(str(self.base_path / pattern), recursive=True)
            for f in files:
                path = Path(f).resolve()
                if not any(x in str(path) for x in ['TEMPLATE', '_TEMPLATE']):
                    md_files.append(path)
                    
        return sorted(set(md_files))
    
    def extract_doc_number(self, file_path: Path) -> Tuple[str, str]:
        """从文件路径提取文档编号"""
        rel_path = str(file_path.relative_to(self.base_path))
        
        # 确定阶段
        stage = None
        if 'Struct/' in rel_path:
            stage = 'S'
        elif 'Knowledge/' in rel_path:
            stage = 'K'
        elif 'Flink/' in rel_path:
            stage = 'F'
        else:
            stage = 'S'  # 默认
            
        # 尝试从文件名提取编号
        doc_match = re.search(r'(\d{2})\.', file_path.name)
        if doc_match:
            doc_num = doc_match.group(1)
        else:
            # 根据目录顺序分配
            doc_num = '01'
            
        return stage, doc_num
    
    def find_existing_elements(self, content: str, file_path: Path) -> List[FormalElement]:
        """查找已编号的形式化元素"""
        elements = []
        lines = content.split('\n')
        stage, doc_num = self.extract_doc_number(file_path)
        rel_path = str(file_path.relative_to(self.base_path))
        
        for line_num, line in enumerate(lines, 1):
            matches = self.NUMBERED_PATTERN.finditer(line)
            for match in matches:
                elem_type_abbr, elem_stage, elem_doc, elem_seq = match.groups()
                full_id = match.group(0)
                
                # 提取标题
                title_match = re.search(r'[:：]\s*(.+?)(?:\*\*|$)', line)
                title = title_match.group(1).strip() if title_match else ''
                
                elem_type = {v: k for k, v in self.ELEMENT_TYPES.items()}.get(elem_type_abbr, 'unknown')
                
                element = FormalElement(
                    element_type=elem_type,
                    stage=elem_stage,
                    doc_num=elem_doc,
                    seq_num=int(elem_seq),
                    full_id=full_id,
                    file_path=rel_path,
                    line_number=line_num,
                    content=line.strip(),
                    title=title
                )
                elements.append(element)
                self.existing_numbers[full_id].add(rel_path)
                
        return elements
    
    def find_unnumbered_elements(self, content: str, file_path: Path) -> List[Tuple[int, str, str]]:
        """查找未编号的形式化元素"""
        unnumbered = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # 跳过已编号的行
            if self.NUMBERED_PATTERN.search(line):
                continue
                
            # 检查每种元素类型
            for elem_type, patterns in self.DETECTION_PATTERNS.items():
                for pattern in patterns:
                    if re.search(pattern, line):
                        unnumbered.append((line_num, elem_type, line.strip()))
                        break
                        
        return unnumbered
    
    def check_duplicates(self) -> List[NumberingIssue]:
        """检查重复编号"""
        issues = []
        
        for full_id, files in self.existing_numbers.items():
            if len(files) > 1:
                issues.append(NumberingIssue(
                    file_path=list(files)[0],
                    line_number=0,
                    issue_type='duplicate_number',
                    element_type='unknown',
                    current_text=full_id,
                    suggestion=f'编号 {full_id} 在多个文件中出现: {", ".join(files)}',
                    auto_fix=None
                ))
                
        return issues
    
    def suggest_number(self, elem_type: str, file_path: Path) -> str:
        """为未编号元素建议编号"""
        stage, doc_num = self.extract_doc_number(file_path)
        type_abbr = self.ELEMENT_TYPES.get(elem_type, 'Def')
        
        # 查找该文件该类型下一个可用序号
        key = f"{stage}-{doc_num}-{type_abbr}"
        seq = self.next_sequence[key]
        
        # 检查是否已存在
        while f"{type_abbr}-{stage}-{doc_num}-{seq:02d}" in self.existing_numbers:
            seq += 1
            
        self.next_sequence[key] = seq + 1
        return f"{type_abbr}-{stage}-{doc_num}-{seq:02d}"
    
    def analyze_file(self, file_path: Path) -> Tuple[List[FormalElement], List[NumberingIssue]]:
        """分析单个文件"""
        elements = []
        issues = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return [], [NumberingIssue(
                file_path=str(file_path.relative_to(self.base_path)),
                line_number=0,
                issue_type='read_error',
                element_type='unknown',
                current_text='',
                suggestion=f'无法读取文件: {e}',
                auto_fix=None
            )]
            
        rel_path = str(file_path.relative_to(self.base_path))
        
        # 1. 查找已编号元素
        existing = self.find_existing_elements(content, file_path)
        elements.extend(existing)
        
        # 2. 查找未编号元素
        unnumbered = self.find_unnumbered_elements(content, file_path)
        for line_num, elem_type, line_content in unnumbered:
            suggested_num = self.suggest_number(elem_type, file_path)
            
            # 生成修复建议
            type_abbr = self.ELEMENT_TYPES.get(elem_type, 'Def')
            auto_fix = line_content.replace(
                '**定理**', f'**定理 ({suggested_num})**'
            ).replace(
                '**定义**', f'**定义 ({suggested_num})**'
            ).replace(
                '**Theorem**', f'**Theorem ({suggested_num})**'
            ).replace(
                '**Definition**', f'**Definition ({suggested_num})**'
            )
            
            issues.append(NumberingIssue(
                file_path=rel_path,
                line_number=line_num,
                issue_type='missing_number',
                element_type=elem_type,
                current_text=line_content,
                suggestion=f'建议添加编号: {suggested_num}',
                auto_fix=auto_fix
            ))
            
        return elements, issues
    
    def run_analysis(self, auto_fix: bool = False) -> Tuple[List[FormalElement], List[NumberingIssue], Dict]:
        """运行完整分析"""
        print("🔢 Formal Element Auto-Number Tool")
        print("=" * 50)
        
        files = self.scan_all_files()
        print(f"\n📁 Found {len(files)} target files")
        
        all_elements = []
        all_issues = []
        
        print("\n🔎 Analyzing files...")
        for i, file_path in enumerate(files, 1):
            if i % 50 == 0:
                print(f"   Progress: {i}/{len(files)} files")
                
            elements, issues = self.analyze_file(file_path)
            all_elements.extend(elements)
            all_issues.extend(issues)
            
        # 检查重复
        print("\n🔄 Checking for duplicates...")
        duplicate_issues = self.check_duplicates()
        all_issues.extend(duplicate_issues)
        
        # 统计
        stats = {
            'total_files': len(files),
            'total_elements': len(all_elements),
            'unnumbered_elements': len([i for i in all_issues if i.issue_type == 'missing_number']),
            'duplicate_numbers': len([i for i in all_issues if i.issue_type == 'duplicate_number']),
            'by_type': defaultdict(int),
            'by_stage': defaultdict(int)
        }
        
        for elem in all_elements:
            stats['by_type'][elem.element_type] += 1
            stats['by_stage'][elem.stage] += 1
            
        self.elements = all_elements
        self.issues = all_issues
        
        # 如果需要自动修复
        if auto_fix:
            self.apply_fixes()
            
        return all_elements, all_issues, stats
    
    def apply_fixes(self):
        """应用自动修复"""
        print("\n🔧 Applying auto-fixes...")
        
        # 按文件分组
        fixes_by_file = defaultdict(list)
        for issue in self.issues:
            if issue.issue_type == 'missing_number' and issue.auto_fix:
                fixes_by_file[issue.file_path].append(issue)
                
        for file_path, fixes in fixes_by_file.items():
            full_path = self.base_path / file_path
            try:
                content = full_path.read_text(encoding='utf-8')
                lines = content.split('\n')
                
                # 按行号倒序处理（避免行号变化）
                for fix in sorted(fixes, key=lambda x: x.line_number, reverse=True):
                    if 1 <= fix.line_number <= len(lines):
                        old_line = lines[fix.line_number - 1]
                        new_line = fix.auto_fix
                        lines[fix.line_number - 1] = new_line
                        print(f"   Fixed: {file_path}:{fix.line_number}")
                        
                full_path.write_text('\n'.join(lines), encoding='utf-8')
                
            except Exception as e:
                print(f"   Error fixing {file_path}: {e}")
                
    def generate_report(self, output_path: str, stats: Dict):
        """生成报告"""
        report = {
            'version': '1.0.0',
            'tool': 'Formal Element Auto-Number',
            'stats': stats,
            'elements': [asdict(e) for e in self.elements],
            'issues': [asdict(i) for i in self.issues],
            'numbering_suggestions': [
                {
                    'file': i.file_path,
                    'line': i.line_number,
                    'type': i.element_type,
                    'current': i.current_text[:100],
                    'suggestion': i.suggestion,
                    'auto_fix': i.auto_fix
                }
                for i in self.issues if i.issue_type == 'missing_number'
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        return report


def main():
    parser = argparse.ArgumentParser(description='Formal Element Auto-Number Tool')
    parser.add_argument('--base-path', default='.', help='项目根目录')
    parser.add_argument('--output', default='formal-element-numbering-report.json', help='输出报告路径')
    parser.add_argument('--auto-fix', action='store_true', help='自动应用修复')
    parser.add_argument('--dry-run', action='store_true', help='仅预览不修改')
    
    args = parser.parse_args()
    
    tool = FormalElementAutoNumber(args.base_path)
    elements, issues, stats = tool.run_analysis(auto_fix=args.auto_fix and not args.dry_run)
    
    # 生成报告
    report = tool.generate_report(args.output, stats)
    
    # 打印摘要
    print("\n" + "=" * 50)
    print("📊 ANALYSIS SUMMARY")
    print("=" * 50)
    print(f"Total files:          {stats['total_files']}")
    print(f"Total elements:       {stats['total_elements']}")
    print(f"Unnumbered elements:  {stats['unnumbered_elements']}")
    print(f"Duplicate numbers:    {stats['duplicate_numbers']}")
    print("\nBy type:")
    for elem_type, count in stats['by_type'].items():
        print(f"  {elem_type.capitalize():12s}: {count}")
    print("\nBy stage:")
    for stage, count in stats['by_stage'].items():
        stage_name = {'S': 'Struct', 'K': 'Knowledge', 'F': 'Flink'}.get(stage, stage)
        print(f"  {stage_name:12s}: {count}")
    print("=" * 50)
    print(f"\n✅ Report saved to: {args.output}")
    
    if args.dry_run:
        print("\n⚠️ Dry run mode - no changes were made")
        
    return 0


if __name__ == '__main__':
    exit(main())
