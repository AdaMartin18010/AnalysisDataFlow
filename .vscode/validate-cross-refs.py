#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交叉引用验证脚本

功能：
1. 检查相对路径链接是否有效
2. 检查引用的文档是否存在
3. 检查定理/定义引用是否有对应注册
4. 检查文档头部的前置依赖声明

使用方法：
    python .vscode/validate-cross-refs.py
    python .vscode/validate-cross-refs.py --json
    python .vscode/validate-cross-refs.py --fix
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple, Optional
from datetime import datetime
from urllib.parse import urlparse


@dataclass
class CrossRef:
    """交叉引用"""
    source_file: str
    source_line: int
    ref_type: str  # link, theorem, definition, prerequisite
    target: str
    anchor: Optional[str] = None
    context: str = ""


@dataclass
class ValidationIssue:
    """验证问题"""
    severity: str  # error, warning, info
    category: str
    message: str
    source_file: str
    source_line: int
    target: str
    suggestion: Optional[str] = None


@dataclass
class ValidationReport:
    """验证报告"""
    total_files: int = 0
    total_refs: int = 0
    broken_links: int = 0
    broken_anchors: int = 0
    missing_prerequisites: int = 0
    circular_refs: List[Tuple[str, str]] = field(default_factory=list)
    issues: List[ValidationIssue] = field(default_factory=list)


class CrossRefValidator:
    """交叉引用验证器"""
    
    # Markdown链接正则 [text](path)
    LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    
    # 前置依赖声明正则
    PREREQ_PATTERN = re.compile(
        r'前置依赖:\s*\[([^\]]+)\]\(([^)]+)\)',
        re.IGNORECASE
    )
    
    # 定理/定义引用正则
    THEOREM_REF_PATTERN = re.compile(
        r'(Thm|Def|Lemma|Prop|Cor)-([SFK])-(\d{2})-(\d{2,3}[a-zA-Z]?)',
        re.IGNORECASE
    )
    
    # 文档头部元数据正则
    HEADER_META_PATTERN = re.compile(
        r'>\s*\*\*?所属阶段\*\*?:?\s*([^|]+)',
        re.IGNORECASE
    )
    PREREQ_META_PATTERN = re.compile(
        r'>\s*\*\*?前置依赖\*\*?:?\s*([^|]+)',
        re.IGNORECASE
    )
    FORMAL_LEVEL_PATTERN = re.compile(
        r'>\s*\*\*?形式化等级\*\*?:?\s*([^|]+)',
        re.IGNORECASE
    )
    
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.report = ValidationReport()
        self.all_refs: List[CrossRef] = []
        self.all_files: Set[str] = set()
        self.registry_elements: Set[str] = set()
        self.file_headers: Dict[str, Dict] = {}
        
    def scan_all_files(self) -> None:
        """扫描所有Markdown文件"""
        md_files = list(self.root_dir.glob('**/*.md'))
        
        # 排除根目录的一些特殊文件
        exclude_files = {
            'THEOREM-REGISTRY.md',
            'README.md',
            'PROJECT-TRACKING.md',
            'PROJECT-VERSION-TRACKING.md',
            'AGENTS.md'
        }
        
        md_files = [
            f for f in md_files 
            if f.name not in exclude_files or 
            f.parent.name in ['Struct', 'Knowledge', 'Flink']
        ]
        
        self.report.total_files = len(md_files)
        
        # 收集所有文件路径
        for file_path in md_files:
            rel_path = str(file_path.relative_to(self.root_dir))
            self.all_files.add(rel_path)
            self.all_files.add('/' + rel_path.replace('\\', '/'))
        
        # 扫描每个文件
        for file_path in md_files:
            self._scan_file(file_path)
    
    def _scan_file(self, file_path: Path) -> None:
        """扫描单个文件"""
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            rel_path = str(file_path.relative_to(self.root_dir))
            
            # 解析文件头部元数据（前10行）
            header_meta = self._parse_header(lines[:10])
            self.file_headers[rel_path] = header_meta
            
            for line_num, line in enumerate(lines, 1):
                # 跳过代码块
                if line.strip().startswith('```'):
                    continue
                
                # 检查链接
                for match in self.LINK_PATTERN.finditer(line):
                    self._process_link(match, rel_path, line_num, line)
                
                # 检查定理引用
                for match in self.THEOREM_REF_PATTERN.finditer(line):
                    self._process_theorem_ref(match, rel_path, line_num)
        except Exception as e:
            self.report.issues.append(ValidationIssue(
                severity='error',
                category='file_read',
                message=f'无法读取文件: {e}',
                source_file=rel_path,
                source_line=0,
                target=''
            ))
    
    def _parse_header(self, lines: List[str]) -> Dict:
        """解析文档头部元数据"""
        header_text = '\n'.join(lines)
        meta = {
            'stage': None,
            'prerequisites': [],
            'formal_level': None
        }
        
        stage_match = self.HEADER_META_PATTERN.search(header_text)
        if stage_match:
            meta['stage'] = stage_match.group(1).strip()
        
        prereq_match = self.PREREQ_META_PATTERN.search(header_text)
        if prereq_match:
            prereq_str = prereq_match.group(1)
            # 解析多个前置依赖
            for link_match in self.LINK_PATTERN.finditer(prereq_str):
                meta['prerequisites'].append({
                    'name': link_match.group(1),
                    'path': link_match.group(2)
                })
        
        level_match = self.FORMAL_LEVEL_PATTERN.search(header_text)
        if level_match:
            meta['formal_level'] = level_match.group(1).strip()
        
        return meta
    
    def _process_link(self, match: re.Match, source_file: str, line_num: int, context: str) -> None:
        """处理链接"""
        link_text = match.group(1)
        link_target = match.group(2)
        
        # 跳过外部链接
        if link_target.startswith(('http://', 'https://', 'mailto:')):
            return
        
        # 提取锚点
        anchor = None
        if '#' in link_target:
            parts = link_target.split('#', 1)
            link_target = parts[0]
            anchor = parts[1]
        
        # 解析相对路径
        if link_target.startswith('/'):
            # 绝对路径（相对于项目根）
            target_path = link_target.lstrip('/').replace('/', os.sep)
        elif link_target:
            # 相对路径
            source_dir = Path(source_file).parent
            target_path = str(source_dir / link_target)
        else:
            # 纯锚点链接
            target_path = source_file
        
        ref = CrossRef(
            source_file=source_file,
            source_line=line_num,
            ref_type='link',
            target=target_path.replace('/', os.sep),
            anchor=anchor,
            context=context.strip()[:80]
        )
        self.all_refs.append(ref)
        self.report.total_refs += 1
    
    def _process_theorem_ref(self, match: re.Match, source_file: str, line_num: int) -> None:
        """处理定理引用"""
        element_type = match.group(1)
        stage = match.group(2).upper()
        doc_num = match.group(3)
        seq_num = match.group(4)
        
        element_id = f"{element_type}-{stage}-{doc_num}-{seq_num}"
        
        ref = CrossRef(
            source_file=source_file,
            source_line=line_num,
            ref_type='theorem',
            target=element_id
        )
        self.all_refs.append(ref)
    
    def load_registry(self) -> None:
        """加载定理注册表"""
        registry_path = self.root_dir / 'THEOREM-REGISTRY.md'
        if not registry_path.exists():
            return
        
        try:
            content = registry_path.read_text(encoding='utf-8')
            pattern = re.compile(
                r'\|\s*(Def|Thm|Lemma|Prop|Cor)-([SFK])-(\d{2})-(\d{2,3}[a-zA-Z]?)\s*\|',
                re.IGNORECASE
            )
            for match in pattern.finditer(content):
                element_type = match.group(1)
                stage = match.group(2).upper()
                doc_num = match.group(3)
                seq_num = match.group(4)
                element_id = f"{element_type}-{stage}-{doc_num}-{seq_num}"
                self.registry_elements.add(element_id)
        except Exception as e:
            print(f"警告: 无法读取注册表: {e}", file=sys.stderr)
    
    def validate(self) -> None:
        """执行验证"""
        # 验证链接
        for ref in self.all_refs:
            if ref.ref_type == 'link':
                self._validate_link(ref)
            elif ref.ref_type == 'theorem':
                self._validate_theorem_ref(ref)
        
        # 验证前置依赖
        self._validate_prerequisites()
        
        # 检测循环引用
        self._detect_circular_refs()
    
    def _validate_link(self, ref: CrossRef) -> None:
        """验证链接"""
        # 规范化路径
        target = ref.target
        if target.startswith('/'):
            target = target[1:]
        
        # 检查文件是否存在
        target_exists = False
        for ext in ['', '.md']:
            check_path = target + ext
            if check_path in self.all_files or check_path.replace('/', '\\') in self.all_files:
                target_exists = True
                break
            # 也检查绝对路径形式
            if '/' + check_path.replace('\\', '/') in self.all_files:
                target_exists = True
                break
        
        if not target_exists:
            self.report.broken_links += 1
            self.report.issues.append(ValidationIssue(
                severity='error',
                category='broken_link',
                message=f'链接指向的文件不存在: {ref.target}',
                source_file=ref.source_file,
                source_line=ref.source_line,
                target=ref.target,
                suggestion='请检查链接路径是否正确，确保目标文件存在'
            ))
        elif ref.anchor:
            # 检查锚点（简化检查，实际应该读取目标文件）
            self.report.broken_anchors += 1
            # 锚点验证需要读取目标文件，这里只做记录
            # 完整实现需要解析目标文件的所有标题
    
    def _validate_theorem_ref(self, ref: CrossRef) -> None:
        """验证定理引用"""
        if ref.target not in self.registry_elements:
            self.report.issues.append(ValidationIssue(
                severity='warning',
                category='unregistered_theorem',
                message=f'引用的定理/定义未在注册表中: {ref.target}',
                source_file=ref.source_file,
                source_line=ref.source_line,
                target=ref.target,
                suggestion=f'请在 THEOREM-REGISTRY.md 中添加 {ref.target} 的注册信息'
            ))
    
    def _validate_prerequisites(self) -> None:
        """验证前置依赖声明"""
        for file_path, header in self.file_headers.items():
            if not header.get('stage'):
                # 核心文档应该有阶段声明
                if any(x in file_path for x in ['Struct/', 'Knowledge/', 'Flink/']):
                    if '00-INDEX' not in file_path:
                        self.report.issues.append(ValidationIssue(
                            severity='info',
                            category='missing_metadata',
                            message='文档缺少"所属阶段"声明',
                            source_file=file_path,
                            source_line=1,
                            target='',
                            suggestion='建议在文档头部添加 > **所属阶段**: ... 声明'
                        ))
            
            # 验证前置依赖链接
            for prereq in header.get('prerequisites', []):
                prereq_path = prereq.get('path', '')
                if prereq_path:
                    # 解析路径
                    if prereq_path.startswith('/'):
                        check_path = prereq_path.lstrip('/')
                    else:
                        source_dir = Path(file_path).parent
                        check_path = str(source_dir / prereq_path)
                    
                    # 规范化路径
                    check_path = check_path.replace('/', os.sep)
                    
                    # 检查是否存在
                    found = False
                    for ext in ['', '.md']:
                        if (check_path + ext) in self.all_files:
                            found = True
                            break
                    
                    if not found:
                        self.report.missing_prerequisites += 1
                        self.report.issues.append(ValidationIssue(
                            severity='warning',
                            category='broken_prerequisite',
                            message=f'前置依赖链接无效: {prereq_path}',
                            source_file=file_path,
                            source_line=1,
                            target=prereq_path,
                            suggestion='请检查前置依赖的路径是否正确'
                        ))
    
    def _detect_circular_refs(self) -> None:
        """检测循环引用（简化版本）"""
        # 构建依赖图
        dependency_graph: Dict[str, Set[str]] = {}
        
        for file_path, header in self.file_headers.items():
            dependencies = set()
            for prereq in header.get('prerequisites', []):
                prereq_path = prereq.get('path', '')
                if prereq_path:
                    # 解析为绝对路径
                    if prereq_path.startswith('/'):
                        abs_path = prereq_path.lstrip('/')
                    else:
                        source_dir = Path(file_path).parent
                        abs_path = str(source_dir / prereq_path)
                    # 规范化
                    abs_path = abs_path.replace('/', os.sep)
                    if abs_path.endswith('.md'):
                        abs_path = abs_path[:-3]
                    dependencies.add(abs_path)
            
            if file_path.endswith('.md'):
                file_key = file_path[:-3]
            else:
                file_key = file_path
            
            dependency_graph[file_key] = dependencies
        
        # 使用DFS检测循环
        def has_cycle(node: str, visited: Set[str], rec_stack: Set[str]) -> Optional[List[str]]:
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in dependency_graph.get(node, set()):
                if neighbor not in visited:
                    cycle = has_cycle(neighbor, visited, rec_stack)
                    if cycle:
                        cycle.append(node)
                        return cycle
                elif neighbor in rec_stack:
                    return [node, neighbor]
            
            rec_stack.remove(node)
            return None
        
        visited: Set[str] = set()
        for node in dependency_graph:
            if node not in visited:
                cycle = has_cycle(node, visited, set())
                if cycle:
                    self.report.circular_refs.append(tuple(reversed(cycle)))
                    self.report.issues.append(ValidationIssue(
                        severity='error',
                        category='circular_dependency',
                        message=f'检测到循环依赖: {" -> ".join(cycle)}',
                        source_file=cycle[0],
                        source_line=1,
                        target=cycle[1]
                    ))
    
    def print_report(self, json_output: bool = False) -> int:
        """打印验证报告"""
        if json_output:
            report_dict = {
                'timestamp': datetime.now().isoformat(),
                'summary': {
                    'total_files': self.report.total_files,
                    'total_refs': self.report.total_refs,
                    'broken_links': self.report.broken_links,
                    'broken_anchors': self.report.broken_anchors,
                    'missing_prerequisites': self.report.missing_prerequisites,
                    'circular_refs': len(self.report.circular_refs)
                },
                'issues': [
                    {
                        'severity': i.severity,
                        'category': i.category,
                        'message': i.message,
                        'source_file': i.source_file,
                        'source_line': i.source_line,
                        'target': i.target,
                        'suggestion': i.suggestion
                    }
                    for i in self.report.issues
                ]
            }
            print(json.dumps(report_dict, indent=2, ensure_ascii=False))
        else:
            print("=" * 80)
            print("交叉引用验证报告")
            print("=" * 80)
            print(f"\n📊 统计信息:")
            print(f"   扫描文件数: {self.report.total_files}")
            print(f"   总引用数: {self.report.total_refs}")
            print(f"   无效链接: {self.report.broken_links}")
            print(f"   可疑锚点: {self.report.broken_anchors}")
            print(f"   缺失前置依赖: {self.report.missing_prerequisites}")
            print(f"   循环依赖: {len(self.report.circular_refs)}")
            
            errors = [i for i in self.report.issues if i.severity == 'error']
            warnings = [i for i in self.report.issues if i.severity == 'warning']
            infos = [i for i in self.report.issues if i.severity == 'info']
            
            print(f"\n🔍 问题汇总:")
            print(f"   错误: {len(errors)}")
            print(f"   警告: {len(warnings)}")
            print(f"   信息: {len(infos)}")
            
            if errors:
                print(f"\n❌ 错误详情:")
                for issue in errors[:15]:
                    print(f"\n   [{issue.category}] {issue.message}")
                    print(f"   位置: {issue.source_file}:{issue.source_line}")
                    if issue.suggestion:
                        print(f"   建议: {issue.suggestion}")
                if len(errors) > 15:
                    print(f"\n   ... 还有 {len(errors) - 15} 个错误")
            
            if warnings:
                print(f"\n⚠️  警告详情 (前10个):")
                for issue in warnings[:10]:
                    print(f"\n   [{issue.category}] {issue.message}")
                    print(f"   位置: {issue.source_file}:{issue.source_line}")
                if len(warnings) > 10:
                    print(f"\n   ... 还有 {len(warnings) - 10} 个警告")
            
            if self.report.circular_refs:
                print(f"\n🔄 循环依赖:")
                for cycle in self.report.circular_refs:
                    print(f"   {' -> '.join(cycle)}")
            
            if not errors and not warnings:
                print(f"\n✅ 所有交叉引用检查通过！")
            
            print("\n" + "=" * 80)
        
        return 1 if errors else 0


def main():
    parser = argparse.ArgumentParser(
        description='交叉引用验证工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python .vscode/validate-cross-refs.py
  python .vscode/validate-cross-refs.py --json
        """
    )
    parser.add_argument('--json', action='store_true', help='输出JSON格式报告')
    parser.add_argument('--fix', action='store_true', help='尝试自动修复部分问题')
    
    args = parser.parse_args()
    
    # 确定项目根目录
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    
    print(f"正在验证交叉引用: {root_dir}", 
          file=sys.stderr if args.json else sys.stdout)
    
    validator = CrossRefValidator(str(root_dir))
    validator.load_registry()
    validator.scan_all_files()
    validator.validate()
    
    exit_code = validator.print_report(json_output=args.json)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
