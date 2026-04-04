#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档一致性检查脚本 - AnalysisDataFlow 自动化工具集

功能：
1. 检查术语使用一致性
2. 检查格式一致性（标题、列表、代码块等）
3. 检查引用格式一致性
4. 检查六段式模板遵循情况
5. 生成一致性报告

使用方法：
    python .scripts/check_consistency.py
    python .scripts/check_consistency.py --json
    python .scripts/check_consistency.py --fix
    python .scripts/check_consistency.py Struct/ Knowledge/

退出码：
    0 - 一致性良好
    1 - 发现不一致问题
    2 - 运行异常
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
from datetime import datetime


@dataclass
class ConsistencyIssue:
    """一致性问题数据类"""
    severity: str  # error, warning, info
    category: str
    message: str
    file_path: str
    line_num: Optional[int] = None
    suggestion: Optional[str] = None
    context: Optional[str] = None


@dataclass
class ConsistencyReport:
    """一致性报告数据类"""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    total_files: int = 0
    issues: List[ConsistencyIssue] = field(default_factory=list)
    term_variations: Dict[str, List[str]] = field(default_factory=dict)
    format_stats: Dict[str, int] = field(default_factory=dict)


class ConsistencyChecker:
    """一致性检查器"""
    
    # 术语标准化映射（标准形式 -> 变体列表）
    TERM_STANDARDS = {
        'Dataflow': ['dataflow', 'DataFlow', 'data flow', 'Data Flow'],
        'DataStream': ['datastream', 'Data Stream', 'data stream'],
        'Checkpoint': ['checkpoint', 'check point', 'CheckPoint'],
        'Watermark': ['watermark', 'water mark', 'WaterMark'],
        'Exactly-Once': ['exactly once', 'Exactly Once', 'exactly-once'],
        'At-Least-Once': ['at least once', 'At Least Once', 'at-least-once'],
        'At-Most-Once': ['at most once', 'At Most Once', 'at-most-once'],
        'Backpressure': ['backpressure', 'back pressure', 'BackPressure'],
        'Flink': ['flink', 'FLINK'],
        'Kafka': ['kafka', 'KAFKA'],
        'Kubernetes': ['kubernetes', 'k8s', 'K8s'],
    }
    
    # 六段式模板必需章节
    REQUIRED_SECTIONS = [
        ('概念定义', ['概念定义', '定义', 'Definitions']),
        ('属性推导', ['属性推导', '性质', 'Properties']),
        ('论证过程', ['论证过程', '论证', 'Argumentation']),
        ('形式证明', ['形式证明', '证明', 'Proof']),
        ('实例验证', ['实例验证', '实例', 'Examples']),
    ]
    
    # 标题格式模式
    TITLE_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$')
    
    # 代码块模式
    CODE_BLOCK_PATTERN = re.compile(r'```(\w*)')
    
    # 引用模式
    CITATION_PATTERN = re.compile(r'\[\^(\d+)\]')
    
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.report = ConsistencyReport()
        self.markdown_files: List[Path] = []
        self.all_terms: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        
    def collect_files(self, paths: Optional[List[str]] = None) -> None:
        """收集要检查的文件"""
        if paths:
            for path in paths:
                p = Path(path)
                if p.is_dir():
                    self.markdown_files.extend(p.rglob('*.md'))
                elif p.is_file() and p.suffix == '.md':
                    self.markdown_files.append(p)
        else:
            # 默认检查核心目录
            for dir_name in ['Struct', 'Knowledge', 'Flink']:
                dir_path = self.root_dir / dir_name
                if dir_path.exists():
                    self.markdown_files.extend(dir_path.rglob('*.md'))
        
        # 去重并排序
        self.markdown_files = sorted(set(self.markdown_files))
        self.report.total_files = len(self.markdown_files)
    
    def check_file(self, file_path: Path) -> None:
        """检查单个文件的一致性"""
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            rel_path = str(file_path.relative_to(self.root_dir))
            
            # 检查标题格式
            self._check_heading_consistency(lines, rel_path)
            
            # 检查术语使用
            self._check_term_consistency(content, rel_path)
            
            # 检查代码块语言标签
            self._check_code_block_labels(content, rel_path)
            
            # 检查引用格式
            self._check_citation_format(content, rel_path)
            
            # 检查六段式模板（针对核心文档）
            if any(d in rel_path for d in ['Struct/', 'Knowledge/', 'Flink/']):
                self._check_six_section_template(content, rel_path)
            
            # 检查列表格式一致性
            self._check_list_consistency(lines, rel_path)
            
        except Exception as e:
            self.report.issues.append(ConsistencyIssue(
                severity='error',
                category='file_read',
                message=f'无法读取文件: {e}',
                file_path=str(file_path)
            ))
    
    def _check_heading_consistency(self, lines: List[str], file_path: str) -> None:
        """检查标题格式一致性"""
        prev_level = 0
        
        for line_num, line in enumerate(lines, 1):
            match = self.TITLE_PATTERN.match(line)
            if match:
                level = len(match.group(1))
                title = match.group(2)
                
                # 检查标题跳跃（如从 h1 直接跳到 h3）
                if prev_level > 0 and level > prev_level + 1:
                    self.report.issues.append(ConsistencyIssue(
                        severity='warning',
                        category='heading_structure',
                        message=f'标题层级跳跃: H{prev_level} -> H{level}',
                        file_path=file_path,
                        line_num=line_num,
                        suggestion=f'考虑添加 H{prev_level + 1} 标题',
                        context=line.strip()[:50]
                    ))
                
                # 检查标题末尾标点
                if title.rstrip()[-1:] in '。，；：':
                    self.report.issues.append(ConsistencyIssue(
                        severity='info',
                        category='heading_format',
                        message='标题末尾不应有标点符号',
                        file_path=file_path,
                        line_num=line_num,
                        suggestion='移除标题末尾的标点符号',
                        context=line.strip()[:50]
                    ))
                
                # 检查标题大小写（英文标题）
                if any(c.isalpha() and c.isascii() for c in title):
                    # 简单检查：如果首字母小写可能是问题
                    words = title.split()
                    if words and words[0][0].islower() and words[0][0].isalpha():
                        if not words[0] in ['a', 'an', 'the', 'in', 'on', 'at', 'to']:
                            self.report.issues.append(ConsistencyIssue(
                                severity='info',
                                category='heading_case',
                                message='英文标题首词建议首字母大写',
                                file_path=file_path,
                                line_num=line_num,
                                suggestion='将首词首字母大写',
                                context=line.strip()[:50]
                            ))
                
                prev_level = level
    
    def _check_term_consistency(self, content: str, file_path: str) -> None:
        """检查术语使用一致性"""
        for standard, variations in self.TERM_STANDARDS.items():
            for variation in variations:
                # 检查变体是否出现在内容中（排除代码块）
                pattern = re.compile(r'(?<![\w\-])' + re.escape(variation) + r'(?![\w\-])', re.IGNORECASE)
                matches = list(pattern.finditer(content))
                
                for match in matches:
                    # 计算行号
                    line_num = content[:match.start()].count('\n') + 1
                    
                    # 检查是否在代码块内
                    lines_before = content[:match.start()].split('\n')
                    in_code_block = False
                    for line in lines_before:
                        if line.strip().startswith('```'):
                            in_code_block = not in_code_block
                    
                    if not in_code_block:
                        self.all_terms[standard][variation] += 1
                        self.report.issues.append(ConsistencyIssue(
                            severity='info',
                            category='term_consistency',
                            message=f'术语变体 "{variation}" 建议使用标准形式 "{standard}"',
                            file_path=file_path,
                            line_num=line_num,
                            suggestion=f'统一使用 "{standard}"'
                        ))
    
    def _check_code_block_labels(self, content: str, file_path: str) -> None:
        """检查代码块语言标签一致性"""
        code_blocks = self.CODE_BLOCK_PATTERN.findall(content)
        
        # 统计语言标签
        lang_counts = defaultdict(int)
        for lang in code_blocks:
            lang_counts[lang.lower()] += 1
        
        self.report.format_stats['code_blocks_by_language'] = dict(lang_counts)
        
        # 检查无标签代码块
        if '' in code_blocks:
            # 查找具体位置
            for match in self.CODE_BLOCK_PATTERN.finditer(content):
                if match.group(1) == '':
                    line_num = content[:match.start()].count('\n') + 1
                    self.report.issues.append(ConsistencyIssue(
                        severity='info',
                        category='code_block_label',
                        message='代码块缺少语言标签',
                        file_path=file_path,
                        line_num=line_num,
                        suggestion='建议添加语言标签，如 ```python、```java、```bash'
                    ))
    
    def _check_citation_format(self, content: str, file_path: str) -> None:
        """检查引用格式一致性"""
        citations = self.CITATION_PATTERN.findall(content)
        
        if not citations:
            return
        
        # 检查引用编号是否连续
        cite_nums = sorted([int(c) for c in citations])
        if cite_nums:
            expected = list(range(1, max(cite_nums) + 1))
            missing = set(expected) - set(cite_nums)
            
            if missing:
                self.report.issues.append(ConsistencyIssue(
                    severity='info',
                    category='citation_sequence',
                    message=f'引用编号不连续，缺少: {sorted(missing)[:5]}',
                    file_path=file_path,
                    suggestion='检查并补充缺失的引用编号'
                ))
        
        # 检查引用定义是否存在
        for cite_num in set(citations):
            cite_def_pattern = re.compile(rf'^\[\^{cite_num}\]:', re.MULTILINE)
            if not cite_def_pattern.search(content):
                self.report.issues.append(ConsistencyIssue(
                    severity='warning',
                    category='citation_definition',
                    message=f'引用 [^{cite_num}] 缺少定义',
                    file_path=file_path,
                    suggestion=f'在文档末尾添加 [^{cite_num}]: 引用信息'
                ))
    
    def _check_six_section_template(self, content: str, file_path: str) -> None:
        """检查六段式模板遵循情况"""
        found_sections = []
        
        for section_name, keywords in self.REQUIRED_SECTIONS:
            for keyword in keywords:
                pattern = re.compile(rf'^#+\s+.*{re.escape(keyword)}', re.MULTILINE | re.IGNORECASE)
                if pattern.search(content):
                    found_sections.append(section_name)
                    break
        
        missing_sections = set([s[0] for s in self.REQUIRED_SECTIONS]) - set(found_sections)
        
        if missing_sections:
            self.report.issues.append(ConsistencyIssue(
                severity='info',
                category='template_compliance',
                message=f'可能缺少六段式模板章节: {", ".join(missing_sections)}',
                file_path=file_path,
                suggestion='确保文档遵循六段式模板结构'
            ))
    
    def _check_list_consistency(self, lines: List[str], file_path: str) -> None:
        """检查列表格式一致性"""
        unordered_patterns = []
        ordered_patterns = []
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.lstrip()
            
            # 无序列表
            if re.match(r'^[\*\-\+]\s', stripped):
                marker = stripped[0]
                unordered_patterns.append((line_num, marker))
            
            # 有序列表
            if re.match(r'^\d+\.\s', stripped):
                ordered_patterns.append((line_num, stripped.split('.')[0]))
        
        # 检查无序列表标记一致性（单个文件内）
        if unordered_patterns:
            markers = set(m for _, m in unordered_patterns)
            if len(markers) > 1:
                self.report.issues.append(ConsistencyIssue(
                    severity='info',
                    category='list_format',
                    message=f'无序列表标记不一致: {", ".join(sorted(markers))}',
                    file_path=file_path,
                    suggestion='统一使用同一种列表标记（建议 -）'
                ))
    
    def check_all(self) -> None:
        """检查所有文件"""
        print(f"正在检查 {len(self.markdown_files)} 个文件的一致性...")
        
        for i, file_path in enumerate(self.markdown_files, 1):
            if i % 50 == 0:
                print(f"  进度: {i}/{len(self.markdown_files)}")
            self.check_file(file_path)
        
        # 整理术语统计
        for standard, variations in self.all_terms.items():
            if variations:
                self.report.term_variations[standard] = [
                    f"{v} ({c}次)" for v, c in sorted(variations.items(), key=lambda x: -x[1])
                ]
    
    def print_report(self, json_output: bool = False) -> int:
        """打印报告"""
        if json_output:
            report_dict = {
                'timestamp': self.report.timestamp,
                'summary': {
                    'total_files': self.report.total_files,
                    'total_issues': len(self.report.issues),
                    'errors': len([i for i in self.report.issues if i.severity == 'error']),
                    'warnings': len([i for i in self.report.issues if i.severity == 'warning']),
                    'infos': len([i for i in self.report.issues if i.severity == 'info'])
                },
                'term_variations': self.report.term_variations,
                'format_stats': self.report.format_stats,
                'issues': [
                    {
                        'severity': i.severity,
                        'category': i.category,
                        'message': i.message,
                        'file': i.file_path,
                        'line': i.line_num,
                        'suggestion': i.suggestion,
                        'context': i.context
                    }
                    for i in self.report.issues
                ]
            }
            print(json.dumps(report_dict, indent=2, ensure_ascii=False))
        else:
            print("\n" + "=" * 70)
            print("文档一致性检查报告")
            print("=" * 70)
            
            print(f"\n📊 检查统计:")
            print(f"   检查文件数: {self.report.total_files}")
            print(f"   发现问题数: {len(self.report.issues)}")
            
            errors = [i for i in self.report.issues if i.severity == 'error']
            warnings = [i for i in self.report.issues if i.severity == 'warning']
            infos = [i for i in self.report.issues if i.severity == 'info']
            
            print(f"   错误: {len(errors)}")
            print(f"   警告: {len(warnings)}")
            print(f"   提示: {len(infos)}")
            
            if self.report.term_variations:
                print(f"\n📝 术语使用统计（发现变体）:")
                for standard, variations in sorted(self.report.term_variations.items())[:10]:
                    print(f"   {standard}: {', '.join(variations[:3])}")
            
            if self.report.format_stats.get('code_blocks_by_language'):
                print(f"\n💻 代码块语言分布:")
                langs = self.report.format_stats['code_blocks_by_language']
                for lang, count in sorted(langs.items(), key=lambda x: -x[1])[:10]:
                    lang_display = lang if lang else '(无标签)'
                    print(f"   {lang_display}: {count}")
            
            if errors:
                print(f"\n❌ 错误详情（前10个）:")
                for issue in errors[:10]:
                    print(f"\n   [{issue.category}] {issue.message}")
                    print(f"   位置: {issue.file_path}:{issue.line_num or 'N/A'}")
                    if issue.suggestion:
                        print(f"   建议: {issue.suggestion}")
            
            if warnings:
                print(f"\n⚠️  警告详情（前10个）:")
                for issue in warnings[:10]:
                    print(f"\n   [{issue.category}] {issue.message}")
                    print(f"   位置: {issue.file_path}:{issue.line_num or 'N/A'}")
            
            if not errors and not warnings:
                print(f"\n✅ 未发现严重一致性问题！")
            
            print("\n" + "=" * 70)
        
        return 1 if errors else 0


def main():
    parser = argparse.ArgumentParser(
        description='AnalysisDataFlow 文档一致性检查工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python .scripts/check_consistency.py
  python .scripts/check_consistency.py --json
  python .scripts/check_consistency.py Struct/ Knowledge/
  python .scripts/check_consistency.py --fix
        """
    )
    parser.add_argument('paths', nargs='*', help='指定要检查的路径')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式报告')
    parser.add_argument('--fix', action='store_true', help='尝试自动修复问题（开发中）')
    
    args = parser.parse_args()
    
    # 确定项目根目录
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    
    try:
        checker = ConsistencyChecker(str(root_dir))
        checker.collect_files(args.paths if args.paths else None)
        checker.check_all()
        
        exit_code = checker.print_report(json_output=args.json)
        sys.exit(exit_code)
    
    except KeyboardInterrupt:
        print("\n\n操作已取消", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 运行错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == '__main__':
    main()
