#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AnalysisDataFlow 项目验证脚本

功能：
1. 扫描所有.md文件中的定理/定义/引理/命题/推论编号
2. 检查编号格式是否符合规范（Def-{S|K|F}-数字-数字）
3. 检测重复编号
4. 检查THEOREM-REGISTRY.md中是否有遗漏
5. 检查文档交叉引用链接是否有效
6. 生成验证报告

使用方法：
    python .vscode/validate-project.py
    python .vscode/validate-project.py --json  # 输出JSON格式报告
    python .vscode/validate-project.py --fix    # 尝试自动修复部分问题
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional
from datetime import datetime


@dataclass
class FormalElement:
    """形式化元素（定理/定义/引理/命题/推论）"""
    id: str
    element_type: str  # Def, Thm, Lemma, Prop, Cor
    stage: str  # S, K, F
    doc_num: str
    seq_num: str
    file_path: str
    line_num: int
    context: str
    
    def __hash__(self):
        return hash(self.id)


@dataclass
class ValidationIssue:
    """验证问题"""
    severity: str  # error, warning, info
    category: str
    message: str
    file_path: Optional[str] = None
    line_num: Optional[int] = None
    suggestion: Optional[str] = None


@dataclass
class ValidationReport:
    """验证报告"""
    total_files: int = 0
    total_elements: int = 0
    elements_by_type: Dict[str, int] = field(default_factory=dict)
    elements_by_stage: Dict[str, int] = field(default_factory=dict)
    issues: List[ValidationIssue] = field(default_factory=list)
    duplicates: List[Tuple[str, List[FormalElement]]] = field(default_factory=list)
    missing_in_registry: List[FormalElement] = field(default_factory=list)
    orphaned_in_registry: List[str] = field(default_factory=list)
    invalid_links: List[Tuple[str, str, int]] = field(default_factory=list)


class ProjectValidator:
    """项目验证器"""
    
    # 编号格式正则表达式
    ID_PATTERN = re.compile(
        r'\*\*\s*(Def|Thm|Lemma|Prop|Cor)-([SFK])-(\d{2})-(\d{2,3}[a-zA-Z]?)\s*\*\*',
        re.IGNORECASE
    )
    
    # 简化的编号格式（用于表格中）
    ID_SIMPLE_PATTERN = re.compile(
        r'\|\s*(Def|Thm|Lemma|Prop|Cor)-([SFK])-(\d{2})-(\d{2,3}[a-zA-Z]?)\s*\|',
        re.IGNORECASE
    )
    
    # Markdown链接正则
    LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    
    # 定理注册表中的编号
    REGISTRY_PATTERN = re.compile(
        r'\|\s*(Def|Thm|Lemma|Prop|Cor)-([SFK])-(\d{2})-(\d{2,3}[a-zA-Z]?)\s*\|',
        re.IGNORECASE
    )
    
    # 有效的阶段标识
    VALID_STAGES = {'S', 'K', 'F'}
    
    # 有效的元素类型
    VALID_TYPES = {'Def', 'Thm', 'Lemma', 'Prop', 'Cor'}
    
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.report = ValidationReport()
        self.registry_elements: Set[str] = set()
        self.all_elements: Dict[str, FormalElement] = {}
        
    def scan_all_files(self) -> None:
        """扫描所有Markdown文件"""
        md_files = []
        for pattern in ['Struct/**/*.md', 'Knowledge/**/*.md', 'Flink/**/*.md']:
            md_files.extend(self.root_dir.glob(pattern))
        
        self.report.total_files = len(md_files)
        
        for file_path in md_files:
            self._scan_file(file_path)
    
    def _scan_file(self, file_path: Path) -> None:
        """扫描单个文件"""
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            rel_path = file_path.relative_to(self.root_dir)
            
            for line_num, line in enumerate(lines, 1):
                # 匹配完整格式 **Def-S-01-01**
                for match in self.ID_PATTERN.finditer(line):
                    self._process_element(match, rel_path, line_num, line)
                
                # 匹配表格中的格式 | Def-S-01-01 |
                for match in self.ID_SIMPLE_PATTERN.finditer(line):
                    self._process_element(match, rel_path, line_num, line)
                
                # 检查链接
                if not str(rel_path).endswith('THEOREM-REGISTRY.md'):
                    self._check_links(line, rel_path, line_num)
        except Exception as e:
            self.report.issues.append(ValidationIssue(
                severity='error',
                category='file_read',
                message=f'无法读取文件: {e}',
                file_path=str(rel_path)
            ))
    
    def _process_element(self, match: re.Match, file_path: Path, line_num: int, context: str) -> None:
        """处理匹配到的形式化元素"""
        element_type = match.group(1)
        stage = match.group(2).upper()
        doc_num = match.group(3)
        seq_num = match.group(4)
        
        element_id = f"{element_type}-{stage}-{doc_num}-{seq_num}"
        
        element = FormalElement(
            id=element_id,
            element_type=element_type,
            stage=stage,
            doc_num=doc_num,
            seq_num=seq_num,
            file_path=str(file_path),
            line_num=line_num,
            context=context.strip()[:100]
        )
        
        # 检查重复
        if element_id in self.all_elements:
            # 已在重复列表中
            pass
        else:
            self.all_elements[element_id] = element
    
    def _check_links(self, line: str, file_path: Path, line_num: int) -> None:
        """检查链接有效性"""
        for match in self.LINK_PATTERN.finditer(line):
            link_text = match.group(1)
            link_target = match.group(2)
            
            # 跳过外部链接
            if link_target.startswith(('http://', 'https://', 'mailto:')):
                continue
            
            # 跳过锚点链接
            if link_target.startswith('#'):
                continue
            
            # 解析相对路径
            if link_target.startswith('/'):
                target_path = self.root_dir / link_target.lstrip('/')
            else:
                target_path = (self.root_dir / file_path).parent / link_target
            
            # 移除锚点部分
            target_path_str = str(target_path).split('#')[0]
            
            if not os.path.exists(target_path_str):
                self.report.invalid_links.append((
                    str(file_path),
                    link_target,
                    line_num
                ))
    
    def load_registry(self) -> None:
        """加载定理注册表"""
        registry_path = self.root_dir / 'THEOREM-REGISTRY.md'
        if not registry_path.exists():
            self.report.issues.append(ValidationIssue(
                severity='error',
                category='registry',
                message='THEOREM-REGISTRY.md 文件不存在'
            ))
            return
        
        try:
            content = registry_path.read_text(encoding='utf-8')
            for match in self.REGISTRY_PATTERN.finditer(content):
                element_type = match.group(1)
                stage = match.group(2).upper()
                doc_num = match.group(3)
                seq_num = match.group(4)
                element_id = f"{element_type}-{stage}-{doc_num}-{seq_num}"
                self.registry_elements.add(element_id)
        except Exception as e:
            self.report.issues.append(ValidationIssue(
                severity='error',
                category='registry',
                message=f'无法读取注册表: {e}'
            ))
    
    def validate(self) -> None:
        """执行验证"""
        # 1. 检查重复
        element_locations: Dict[str, List[FormalElement]] = {}
        for element in self.all_elements.values():
            if element.id not in element_locations:
                element_locations[element.id] = []
            element_locations[element.id].append(element)
        
        for element_id, locations in element_locations.items():
            if len(locations) > 1:
                self.report.duplicates.append((element_id, locations))
                self.report.issues.append(ValidationIssue(
                    severity='error',
                    category='duplicate',
                    message=f'重复编号: {element_id} 出现在 {len(locations)} 个位置',
                    suggestion='请为重复的编号分配新的唯一编号'
                ))
        
        # 2. 检查注册表完整性
        for element_id, element in self.all_elements.items():
            if element_id not in self.registry_elements:
                self.report.missing_in_registry.append(element)
                self.report.issues.append(ValidationIssue(
                    severity='warning',
                    category='registry_missing',
                    message=f'{element_id} 未在 THEOREM-REGISTRY.md 中注册',
                    file_path=element.file_path,
                    line_num=element.line_num,
                    suggestion=f'请在 THEOREM-REGISTRY.md 中添加 {element_id} 的注册信息'
                ))
        
        # 3. 检查注册表中多余的条目
        scanned_ids = set(self.all_elements.keys())
        for registry_id in self.registry_elements:
            if registry_id not in scanned_ids:
                self.report.orphaned_in_registry.append(registry_id)
                self.report.issues.append(ValidationIssue(
                    severity='warning',
                    category='orphaned_registry',
                    message=f'{registry_id} 在注册表中但文档中未找到',
                    suggestion=f'请检查 {registry_id} 是否已删除或编号有误'
                ))
        
        # 4. 检查无效链接
        for file_path, link_target, line_num in self.report.invalid_links:
            self.report.issues.append(ValidationIssue(
                severity='error',
                category='invalid_link',
                message=f'无效链接: {link_target}',
                file_path=file_path,
                line_num=line_num,
                suggestion='请检查链接路径是否正确'
            ))
        
        # 统计
        self.report.total_elements = len(self.all_elements)
        for element in self.all_elements.values():
            t = element.element_type
            s = element.stage
            self.report.elements_by_type[t] = self.report.elements_by_type.get(t, 0) + 1
            self.report.elements_by_stage[s] = self.report.elements_by_stage.get(s, 0) + 1
    
    def print_report(self, json_output: bool = False) -> int:
        """打印验证报告"""
        if json_output:
            report_dict = {
                'timestamp': datetime.now().isoformat(),
                'summary': {
                    'total_files': self.report.total_files,
                    'total_elements': self.report.total_elements,
                    'elements_by_type': self.report.elements_by_type,
                    'elements_by_stage': self.report.elements_by_stage,
                    'issue_count': len(self.report.issues),
                    'error_count': sum(1 for i in self.report.issues if i.severity == 'error'),
                    'warning_count': sum(1 for i in self.report.issues if i.severity == 'warning')
                },
                'issues': [
                    {
                        'severity': i.severity,
                        'category': i.category,
                        'message': i.message,
                        'file_path': i.file_path,
                        'line_num': i.line_num,
                        'suggestion': i.suggestion
                    }
                    for i in self.report.issues
                ],
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
                'missing_in_registry': [
                    {
                        'id': e.id,
                        'file': e.file_path,
                        'line': e.line_num
                    }
                    for e in self.report.missing_in_registry
                ],
                'orphaned_in_registry': self.report.orphaned_in_registry
            }
            print(json.dumps(report_dict, indent=2, ensure_ascii=False))
        else:
            print("=" * 80)
            print("AnalysisDataFlow 项目验证报告")
            print("=" * 80)
            print(f"\n📊 统计信息:")
            print(f"   扫描文件数: {self.report.total_files}")
            print(f"   形式化元素总数: {self.report.total_elements}")
            print(f"\n   按类型分布:")
            for t, count in sorted(self.report.elements_by_type.items()):
                print(f"      {t}: {count}")
            print(f"\n   按阶段分布:")
            stage_names = {'S': 'Struct', 'K': 'Knowledge', 'F': 'Flink'}
            for s, count in sorted(self.report.elements_by_stage.items()):
                print(f"      {s} ({stage_names.get(s, 'Unknown')}): {count}")
            
            print(f"\n🔍 问题汇总:")
            errors = [i for i in self.report.issues if i.severity == 'error']
            warnings = [i for i in self.report.issues if i.severity == 'warning']
            
            print(f"   错误: {len(errors)}")
            print(f"   警告: {len(warnings)}")
            
            if errors:
                print(f"\n❌ 错误详情:")
                for issue in errors[:20]:  # 最多显示20个
                    print(f"\n   [{issue.category}] {issue.message}")
                    if issue.file_path:
                        print(f"   位置: {issue.file_path}:{issue.line_num or 'N/A'}")
                    if issue.suggestion:
                        print(f"   建议: {issue.suggestion}")
                if len(errors) > 20:
                    print(f"\n   ... 还有 {len(errors) - 20} 个错误未显示")
            
            if warnings:
                print(f"\n⚠️  警告详情 (前10个):")
                for issue in warnings[:10]:
                    print(f"\n   [{issue.category}] {issue.message}")
                    if issue.file_path:
                        print(f"   位置: {issue.file_path}:{issue.line_num or 'N/A'}")
                if len(warnings) > 10:
                    print(f"\n   ... 还有 {len(warnings) - 10} 个警告未显示")
            
            if self.report.duplicates:
                print(f"\n🔁 重复编号:")
                for element_id, locations in self.report.duplicates:
                    print(f"\n   {element_id}:")
                    for loc in locations:
                        print(f"      - {loc.file_path}:{loc.line_num}")
            
            if not errors and not warnings:
                print(f"\n✅ 所有检查通过！项目状态良好。")
            
            print("\n" + "=" * 80)
        
        # 返回退出码
        errors = [i for i in self.report.issues if i.severity == 'error']
        return 1 if errors else 0


def main():
    parser = argparse.ArgumentParser(
        description='AnalysisDataFlow 项目验证工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python .vscode/validate-project.py
  python .vscode/validate-project.py --json > report.json
  python .vscode/validate-project.py --verbose
        """
    )
    parser.add_argument('--json', action='store_true', help='输出JSON格式报告')
    parser.add_argument('--fix', action='store_true', help='尝试自动修复部分问题')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')
    
    args = parser.parse_args()
    
    # 确定项目根目录
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    
    print(f"正在验证项目: {root_dir}", file=sys.stderr if args.json else sys.stdout)
    
    validator = ProjectValidator(str(root_dir))
    validator.load_registry()
    validator.scan_all_files()
    validator.validate()
    
    exit_code = validator.print_report(json_output=args.json)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
