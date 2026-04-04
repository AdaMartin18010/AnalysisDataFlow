#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定理编号验证脚本 - AnalysisDataFlow 自动化工具集

功能：
1. 检查所有定理/定义/引理/命题/推论编号的连续性
2. 检测编号重复、缺失、格式错误
3. 验证编号与文档的对应关系
4. 生成详细的验证报告

使用方法：
    python .scripts/validate_theorem_numbers.py
    python .scripts/validate_theorem_numbers.py --json
    python .scripts/validate_theorem_numbers.py --fix
    python .scripts/validate_theorem_numbers.py --verbose

退出码：
    0 - 所有检查通过
    1 - 发现错误
    2 - 运行异常
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Set, Tuple, Optional
from datetime import datetime
from collections import defaultdict


@dataclass
class TheoremElement:
    """形式化元素数据类"""
    id: str
    element_type: str  # Def, Thm, Lemma, Prop, Cor
    stage: str  # S, K, F
    doc_num: int
    seq_num: str
    file_path: str
    line_num: int
    context: str
    
    def __hash__(self):
        return hash(self.id)


@dataclass
class ValidationIssue:
    """验证问题数据类"""
    severity: str  # error, warning, info
    category: str
    message: str
    file_path: Optional[str] = None
    line_num: Optional[int] = None
    suggestion: Optional[str] = None
    element_id: Optional[str] = None


@dataclass
class ValidationReport:
    """验证报告数据类"""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    total_files: int = 0
    total_elements: int = 0
    elements_by_type: Dict[str, int] = field(default_factory=dict)
    elements_by_stage: Dict[str, int] = field(default_factory=dict)
    issues: List[ValidationIssue] = field(default_factory=list)
    duplicates: List[Tuple[str, List[TheoremElement]]] = field(default_factory=list)
    missing_numbers: List[Dict] = field(default_factory=list)
    invalid_formats: List[Dict] = field(default_factory=list)
    continuity_issues: List[Dict] = field(default_factory=list)


class TheoremNumberValidator:
    """定理编号验证器"""
    
    # 编号格式正则表达式：匹配 **Def-S-01-01** 或 | Def-S-01-01 |
    ID_PATTERN = re.compile(
        r'(?:\*\*|\|\s*)(Def|Thm|Lemma|Prop|Cor)-([SFK])-(\d{1,2})-(\d{1,3}[a-zA-Z]?)\s*(?:\*\*|\|)',
        re.IGNORECASE
    )
    
    # 宽松的编号匹配（用于检测可能的格式错误）
    LOOSE_PATTERN = re.compile(
        r'(Def|Thm|Lemma|Prop|Cor)\s*[-–—]\s*([SFK])\s*[-–—]\s*(\d+)\s*[-–—]\s*(\d+)',
        re.IGNORECASE
    )
    
    VALID_STAGES = {'S', 'K', 'F'}
    VALID_TYPES = {'Def', 'Thm', 'Lemma', 'Prop', 'Cor'}
    STAGE_NAMES = {'S': 'Struct', 'K': 'Knowledge', 'F': 'Flink'}
    
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.report = ValidationReport()
        self.all_elements: Dict[str, TheoremElement] = {}
        self.elements_by_doc: Dict[str, Dict[int, List[TheoremElement]]] = defaultdict(
            lambda: defaultdict(list)
        )
        
    def scan_all_files(self) -> None:
        """扫描所有Markdown文件"""
        md_files = []
        for pattern in ['Struct/**/*.md', 'Knowledge/**/*.md', 'Flink/**/*.md', '*.md']:
            md_files.extend(self.root_dir.glob(pattern))
        
        # 过滤掉根目录下非项目文档的文件
        md_files = [f for f in md_files if not self._should_skip_file(f)]
        
        self.report.total_files = len(md_files)
        
        for file_path in md_files:
            self._scan_file(file_path)
    
    def _should_skip_file(self, file_path: Path) -> bool:
        """判断是否应该跳过该文件"""
        skip_list = {
            'THEOREM-REGISTRY.md', 'STATISTICS-REPORT.md', 'PROJECT-TRACKING.md',
            'CHANGELOG.md', 'README.md', 'AGENTS.md', 'AUTOMATION-TOOLKIT-README.md'
        }
        return file_path.name in skip_list
    
    def _scan_file(self, file_path: Path) -> None:
        """扫描单个文件"""
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            rel_path = str(file_path.relative_to(self.root_dir))
            
            for line_num, line in enumerate(lines, 1):
                # 匹配标准格式
                for match in self.ID_PATTERN.finditer(line):
                    self._process_element(match, rel_path, line_num, line)
                
                # 检测可能的格式错误（宽松匹配但未命中严格匹配）
                if self.LOOSE_PATTERN.search(line) and not self.ID_PATTERN.search(line):
                    self.report.invalid_formats.append({
                        'file': rel_path,
                        'line': line_num,
                        'content': line.strip()[:80],
                        'reason': '编号格式不规范，请使用 **Type-Stage-NN-NN** 格式'
                    })
        except Exception as e:
            self.report.issues.append(ValidationIssue(
                severity='error',
                category='file_read',
                message=f'无法读取文件: {e}',
                file_path=str(rel_path)
            ))
    
    def _process_element(self, match: re.Match, file_path: str, line_num: int, context: str) -> None:
        """处理匹配到的形式化元素"""
        element_type = match.group(1).capitalize()
        stage = match.group(2).upper()
        doc_num = int(match.group(3))
        seq_num = match.group(4)
        
        element_id = f"{element_type}-{stage}-{doc_num:02d}-{seq_num}"
        
        element = TheoremElement(
            id=element_id,
            element_type=element_type,
            stage=stage,
            doc_num=doc_num,
            seq_num=seq_num,
            file_path=file_path,
            line_num=line_num,
            context=context.strip()[:100]
        )
        
        # 检查重复
        if element_id in self.all_elements:
            existing = self.all_elements[element_id]
            self.report.duplicates.append((element_id, [existing, element]))
            self.report.issues.append(ValidationIssue(
                severity='error',
                category='duplicate_id',
                message=f'重复编号: {element_id}',
                file_path=file_path,
                line_num=line_num,
                element_id=element_id,
                suggestion=f'该编号已在 {existing.file_path}:{existing.line_num} 使用，请分配新编号'
            ))
        else:
            self.all_elements[element_id] = element
            self.elements_by_doc[f"{stage}-{doc_num:02d}"].append(element)
    
    def validate_continuity(self) -> None:
        """验证编号连续性"""
        # 按阶段和文档分组检查
        for stage in self.VALID_STAGES:
            stage_elements = [e for e in self.all_elements.values() if e.stage == stage]
            
            # 按文档分组
            docs = defaultdict(list)
            for e in stage_elements:
                docs[e.doc_num].append(e)
            
            for doc_num, elements in sorted(docs.items()):
                # 按类型分组检查连续性
                by_type = defaultdict(list)
                for e in elements:
                    by_type[e.element_type].append(e)
                
                for elem_type, type_elements in by_type.items():
                    sorted_elems = sorted(type_elements, key=lambda x: (
                        int(re.match(r'\d+', x.seq_num).group()) if re.match(r'\d+', x.seq_num) else 0,
                        x.seq_num
                    ))
                    
                    # 检查序列号是否连续
                    seq_numbers = []
                    for e in sorted_elems:
                        match = re.match(r'(\d+)([a-zA-Z]?)', e.seq_num)
                        if match:
                            seq_numbers.append((int(match.group(1)), match.group(2), e))
                    
                    for i in range(1, len(seq_numbers)):
                        prev_num, prev_suffix, prev_elem = seq_numbers[i-1]
                        curr_num, curr_suffix, curr_elem = seq_numbers[i]
                        
                        # 检查是否有跳号（允许子编号如 01a, 01b）
                        if curr_num > prev_num + 1 and not prev_suffix:
                            self.report.continuity_issues.append({
                                'stage': stage,
                                'doc_num': doc_num,
                                'element_type': elem_type,
                                'gap': (prev_num, curr_num),
                                'missing': list(range(prev_num + 1, curr_num)),
                                'after_element': prev_elem.id,
                                'before_element': curr_elem.id
                            })
                            self.report.issues.append(ValidationIssue(
                                severity='warning',
                                category='continuity_gap',
                                message=f'{elem_type}-{stage}-{doc_num:02d} 编号不连续: {prev_num} -> {curr_num}',
                                file_path=curr_elem.file_path,
                                suggestion=f'缺少编号: {", ".join(f"{elem_type}-{stage}-{doc_num:02d}-{n:02d}" for n in range(prev_num + 1, curr_num))}'
                            ))
    
    def validate_registry_consistency(self) -> None:
        """验证与定理注册表的一致性"""
        registry_path = self.root_dir / 'THEOREM-REGISTRY.md'
        if not registry_path.exists():
            self.report.issues.append(ValidationIssue(
                severity='warning',
                category='registry_missing',
                message='THEOREM-REGISTRY.md 不存在，跳过注册表一致性检查'
            ))
            return
        
        try:
            content = registry_path.read_text(encoding='utf-8')
            registry_ids = set()
            
            for match in self.ID_PATTERN.finditer(content):
                element_type = match.group(1).capitalize()
                stage = match.group(2).upper()
                doc_num = int(match.group(3))
                seq_num = match.group(4)
                element_id = f"{element_type}-{stage}-{doc_num:02d}-{seq_num}"
                registry_ids.add(element_id)
            
            # 检查文档中有但注册表中没有的
            for element_id in self.all_elements:
                if element_id not in registry_ids:
                    elem = self.all_elements[element_id]
                    self.report.issues.append(ValidationIssue(
                        severity='warning',
                        category='missing_in_registry',
                        message=f'{element_id} 未在 THEOREM-REGISTRY.md 中注册',
                        file_path=elem.file_path,
                        line_num=elem.line_num,
                        element_id=element_id,
                        suggestion=f'请在 THEOREM-REGISTRY.md 中添加 {element_id}'
                    ))
            
            # 检查注册表中有但文档中没有的
            for element_id in registry_ids:
                if element_id not in self.all_elements:
                    self.report.issues.append(ValidationIssue(
                        severity='warning',
                        category='orphaned_in_registry',
                        message=f'{element_id} 在注册表中但文档中未找到',
                        element_id=element_id,
                        suggestion=f'请检查 {element_id} 是否已删除或编号有误'
                    ))
        
        except Exception as e:
            self.report.issues.append(ValidationIssue(
                severity='error',
                category='registry_read',
                message=f'读取 THEOREM-REGISTRY.md 失败: {e}'
            ))
    
    def validate(self) -> None:
        """执行所有验证"""
        self.validate_continuity()
        self.validate_registry_consistency()
        
        # 统计
        self.report.total_elements = len(self.all_elements)
        for element in self.all_elements.values():
            t = element.element_type
            s = element.stage
            self.report.elements_by_type[t] = self.report.elements_by_type.get(t, 0) + 1
            self.report.elements_by_stage[s] = self.report.elements_by_stage.get(s, 0) + 1
    
    def print_report(self, json_output: bool = False, verbose: bool = False) -> int:
        """打印验证报告"""
        if json_output:
            report_dict = {
                'timestamp': self.report.timestamp,
                'summary': {
                    'total_files': self.report.total_files,
                    'total_elements': self.report.total_elements,
                    'elements_by_type': self.report.elements_by_type,
                    'elements_by_stage': self.report.elements_by_stage,
                    'issue_count': len(self.report.issues),
                    'error_count': sum(1 for i in self.report.issues if i.severity == 'error'),
                    'warning_count': sum(1 for i in self.report.issues if i.severity == 'warning'),
                    'duplicate_count': len(self.report.duplicates),
                    'continuity_issues': len(self.report.continuity_issues),
                    'invalid_formats': len(self.report.invalid_formats)
                },
                'issues': [asdict(i) for i in self.report.issues],
                'duplicates': [
                    {
                        'id': d[0],
                        'locations': [
                            {
                                'file': loc.file_path,
                                'line': loc.line_num,
                                'context': loc.context
                            }
                            for loc in d[1]
                        ]
                    }
                    for d in self.report.duplicates
                ],
                'continuity_issues': self.report.continuity_issues,
                'invalid_formats': self.report.invalid_formats
            }
            print(json.dumps(report_dict, indent=2, ensure_ascii=False))
        else:
            print("=" * 80)
            print("AnalysisDataFlow 定理编号验证报告")
            print("=" * 80)
            print(f"\n📊 统计信息:")
            print(f"   扫描文件数: {self.report.total_files}")
            print(f"   形式化元素总数: {self.report.total_elements}")
            
            if self.report.elements_by_type:
                print(f"\n   按类型分布:")
                for t, count in sorted(self.report.elements_by_type.items()):
                    type_name = {'Def': '定义', 'Thm': '定理', 'Lemma': '引理', 
                                'Prop': '命题', 'Cor': '推论'}.get(t, t)
                    print(f"      {type_name}({t}): {count}")
            
            if self.report.elements_by_stage:
                print(f"\n   按阶段分布:")
                for s, count in sorted(self.report.elements_by_stage.items()):
                    print(f"      {s} ({self.STAGE_NAMES.get(s, 'Unknown')}): {count}")
            
            errors = [i for i in self.report.issues if i.severity == 'error']
            warnings = [i for i in self.report.issues if i.severity == 'warning']
            
            print(f"\n🔍 问题汇总:")
            print(f"   错误: {len(errors)}")
            print(f"   警告: {len(warnings)}")
            print(f"   重复编号: {len(self.report.duplicates)}")
            print(f"   连续性问题: {len(self.report.continuity_issues)}")
            print(f"   格式错误: {len(self.report.invalid_formats)}")
            
            if errors:
                print(f"\n❌ 错误详情:")
                for issue in errors[:15]:
                    print(f"\n   [{issue.category}] {issue.message}")
                    if issue.file_path:
                        print(f"   位置: {issue.file_path}:{issue.line_num or 'N/A'}")
                    if issue.suggestion:
                        print(f"   建议: {issue.suggestion}")
                if len(errors) > 15:
                    print(f"\n   ... 还有 {len(errors) - 15} 个错误未显示")
            
            if warnings and verbose:
                print(f"\n⚠️  警告详情:")
                for issue in warnings[:10]:
                    print(f"\n   [{issue.category}] {issue.message}")
                    if issue.file_path:
                        print(f"   位置: {issue.file_path}:{issue.line_num or 'N/A'}")
            
            if self.report.duplicates:
                print(f"\n🔁 重复编号详情:")
                for element_id, locations in self.report.duplicates[:5]:
                    print(f"\n   {element_id}:")
                    for loc in locations:
                        print(f"      - {loc.file_path}:{loc.line_num}")
            
            if not errors and not warnings:
                print(f"\n✅ 所有检查通过！编号规范且连续。")
            elif not errors:
                print(f"\n⚠️  未发现错误，但有 {len(warnings)} 个警告，建议检查。")
            
            print("\n" + "=" * 80)
        
        return 1 if any(i.severity == 'error' for i in self.report.issues) else 0


def main():
    parser = argparse.ArgumentParser(
        description='AnalysisDataFlow 定理编号验证工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python .scripts/validate_theorem_numbers.py
  python .scripts/validate_theorem_numbers.py --json > theorem-report.json
  python .scripts/validate_theorem_numbers.py --verbose
  python .scripts/validate_theorem_numbers.py --fix
        """
    )
    parser.add_argument('--json', action='store_true', help='输出JSON格式报告')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')
    parser.add_argument('--fix', action='store_true', help='尝试自动修复部分问题（开发中）')
    
    args = parser.parse_args()
    
    # 确定项目根目录
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    
    if not args.json:
        print(f"正在验证定理编号: {root_dir}")
    
    try:
        validator = TheoremNumberValidator(str(root_dir))
        validator.scan_all_files()
        validator.validate()
        
        exit_code = validator.print_report(json_output=args.json, verbose=args.verbose)
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n操作已取消", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 运行错误: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(2)


if __name__ == '__main__':
    main()
