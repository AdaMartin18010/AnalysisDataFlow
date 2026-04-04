#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
引用验证器 (Reference Validator)

功能：
    - 验证交叉引用有效性（文档间链接）
    - 检查定理/定义编号全局唯一性
    - 验证内部链接可达性
    - 检查引用格式一致性
    - 生成定理注册表对比报告

使用方式：
    python reference-validator.py [文件或目录路径]
    python reference-validator.py --registry THEOREM-REGISTRY.md [路径]
    python reference-validator.py --ci [路径]

退出码：
    0 - 所有检查通过
    1 - 发现引用错误
    2 - 配置错误
"""

import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Tuple
from enum import IntEnum
from collections import defaultdict
import urllib.parse


class ExitCode(IntEnum):
    """退出码定义"""
    SUCCESS = 0
    REFERENCE_ERROR = 1
    CONFIG_ERROR = 2
    FILE_ERROR = 3


class Severity(IntEnum):
    """问题严重级别"""
    ERROR = 3
    WARNING = 2
    INFO = 1


@dataclass
class Issue:
    """问题记录"""
    file: str
    line: int
    severity: Severity
    code: str
    message: str
    suggestion: str = ""


@dataclass
class ValidationResult:
    """验证结果"""
    file_path: str
    issues: List[Issue] = field(default_factory=list)
    passed: bool = True
    
    def add_issue(self, line: int, severity: Severity, code: str,
                  message: str, suggestion: str = ""):
        self.issues.append(Issue(
            file=self.file_path,
            line=line,
            severity=severity,
            code=code,
            message=message,
            suggestion=suggestion
        ))
        if severity == Severity.ERROR:
            self.passed = False


@dataclass
class Reference:
    """引用信息"""
    ref_type: str          # theorem, definition, link, citation
    target: str            # 引用目标
    source_file: str       # 源文件
    line: int              # 行号
    context: str           # 上下文


class ReferenceValidator:
    """
    引用验证器
    
    验证内容：
    1. 文档内部链接（锚点）
    2. 文档间链接
    3. 定理/定义编号全局唯一性
    4. 引用格式一致性
    5. 与THEOREM-REGISTRY.md对比
    """
    
    # 定理编号模式
    THEOREM_PATTERN = re.compile(
        r'`?(Thm|Lemma|Def|Prop|Cor)-([SKF])-(\d{2})-(\d{2})`?'
    )
    
    # 内部链接: [text](./path/to/file.md), [text](#anchor)
    INTERNAL_LINK_PATTERN = re.compile(
        r'\[([^\]]+)\]\(([^)]+)\)'
    )
    
    # 引用标注: [^1], [^n]
    CITATION_PATTERN = re.compile(r'\[\^(\d+)\]')
    
    # 引用定义: [^1]: content
    CITATION_DEF_PATTERN = re.compile(
        r'^\[(\^\d+)\]:\s*(.+)$',
        re.MULTILINE
    )
    
    # 锚点定义: ## Header {#anchor} 或 <a name="anchor">
    ANCHOR_PATTERN = re.compile(
        r'^(#{1,6})\s+.+?\{#([^}]+)\}'  # 标题锚点
        r'|<a\s+name=["\']([^"\']+)["\']',  # HTML锚点
        re.MULTILINE
    )
    
    def __init__(self, config: Optional[Dict] = None, 
                 root_dir: Optional[Path] = None):
        """
        初始化验证器
        
        Args:
            config: 配置字典
            root_dir: 项目根目录
        """
        self.config = config or {}
        self.root_dir = root_dir or Path.cwd()
        self.results: List[ValidationResult] = []
        
        # 全局引用数据库
        self.all_theorems: Dict[str, Dict] = {}  # 定理ID -> 定义信息
        self.all_files: Set[str] = set()  # 存在的文件
        self.all_anchors: Dict[str, Set[str]] = defaultdict(set)  # 文件 -> 锚点集合
        self.all_citations: Dict[str, Dict[str, str]] = defaultdict(dict)  # 文件 -> 引用定义
        
        # 从配置加载
        self.registry_file = self.config.get('registry_file', 'THEOREM-REGISTRY.md')
        self.check_external_links = self.config.get('check_external_links', False)
        
    def build_reference_database(self, directory: Path):
        """
        构建引用数据库
        
        扫描目录中的所有Markdown文件，收集：
        - 定理/定义编号
        - 文件路径
        - 锚点定义
        - 引用定义
        """
        print(f"构建引用数据库: {directory}")
        
        md_files = list(directory.rglob("*.md"))
        exclude_patterns = ['.git', 'node_modules', '.venv', '__pycache__']
        md_files = [
            f for f in md_files 
            if not any(p in str(f) for p in exclude_patterns)
        ]
        
        for file_path in md_files:
            relative_path = str(file_path.relative_to(self.root_dir))
            self.all_files.add(relative_path)
            
            try:
                content = file_path.read_text(encoding='utf-8')
            except Exception:
                continue
            
            # 收集定理编号
            self._collect_theorems(content, relative_path)
            
            # 收集锚点
            self._collect_anchors(content, relative_path)
            
            # 收集引用定义
            self._collect_citations(content, relative_path)
        
        print(f"  - 发现 {len(self.all_files)} 个文件")
        print(f"  - 发现 {len(self.all_theorems)} 个定理/定义")
        print(f"  - 发现 {sum(len(a) for a in self.all_anchors.values())} 个锚点")
    
    def _collect_theorems(self, content: str, file_path: str):
        """收集定理编号"""
        for match in self.THEOREM_PATTERN.finditer(content):
            theorem_type = match.group(1)
            stage = match.group(2)
            doc_num = match.group(3)
            seq_num = match.group(4)
            
            theorem_id = f"{theorem_type}-{stage}-{doc_num}-{seq_num}"
            
            # 计算行号
            line_num = content[:match.start()].count('\n') + 1
            
            if theorem_id in self.all_theorems:
                # 记录重复
                if 'duplicates' not in self.all_theorems[theorem_id]:
                    self.all_theorems[theorem_id]['duplicates'] = []
                self.all_theorems[theorem_id]['duplicates'].append({
                    'file': file_path,
                    'line': line_num
                })
            else:
                self.all_theorems[theorem_id] = {
                    'type': theorem_type,
                    'stage': stage,
                    'doc_num': doc_num,
                    'seq_num': seq_num,
                    'file': file_path,
                    'line': line_num,
                    'duplicates': []
                }
    
    def _collect_anchors(self, content: str, file_path: str):
        """收集锚点定义"""
        # 从标题自动生成锚点
        header_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        for match in header_pattern.finditer(content):
            header_text = match.group(2).strip()
            # GitHub风格的锚点：小写，空格变-，去除特殊字符
            anchor = re.sub(r'[^\w\s-]', '', header_text).lower().replace(' ', '-')
            self.all_anchors[file_path].add(anchor)
        
        # 显式锚点 {#anchor}
        explicit_anchor = re.compile(r'\{#([^}]+)\}')
        for match in explicit_anchor.finditer(content):
            self.all_anchors[file_path].add(match.group(1))
        
        # HTML锚点 <a name="...">
        html_anchor = re.compile(r'<a\s+name=["\']([^"\']+)["\']')
        for match in html_anchor.finditer(content):
            self.all_anchors[file_path].add(match.group(1))
    
    def _collect_citations(self, content: str, file_path: str):
        """收集引用定义"""
        for match in self.CITATION_DEF_PATTERN.finditer(content):
            ref_id = match.group(1)
            ref_content = match.group(2).strip()
            self.all_citations[file_path][ref_id] = ref_content
    
    def validate_file(self, file_path: Path) -> ValidationResult:
        """验证单个文件"""
        result = ValidationResult(file_path=str(file_path))
        relative_path = str(file_path.relative_to(self.root_dir))
        
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
        except Exception as e:
            result.add_issue(
                line=0,
                severity=Severity.ERROR,
                code="FILE-001",
                message=f"无法读取文件: {e}",
                suggestion="检查文件编码和权限"
            )
            return result
        
        # 1. 验证定理编号（检查是否与全局数据库一致）
        self._validate_theorems_in_file(content, lines, result, relative_path)
        
        # 2. 验证链接
        self._validate_links(content, lines, result, relative_path)
        
        # 3. 验证引用
        self._validate_citations(content, lines, result, relative_path)
        
        return result
    
    def _validate_theorems_in_file(self, content: str, lines: List[str],
                                   result: ValidationResult, file_path: str):
        """验证文件中的定理编号"""
        for match in self.THEOREM_PATTERN.finditer(content):
            theorem_id = f"{match.group(1)}-{match.group(2)}-{match.group(3)}-{match.group(4)}"
            line_num = self._find_line_number(content, match.start(), lines)
            
            theorem_info = self.all_theorems.get(theorem_id)
            if theorem_info:
                # 检查是否有重复
                if len(theorem_info.get('duplicates', [])) > 0:
                    # 这是重复的定义
                    result.add_issue(
                        line=line_num,
                        severity=Severity.ERROR,
                        code="REF-001",
                        message=f"定理编号重复: {theorem_id}",
                        suggestion=f"已在 {theorem_info['file']}:{theorem_info['line']} 定义，请使用新编号"
                    )
                elif theorem_info['file'] != file_path:
                    # 这可能是引用（在其他文件定义是正常的）
                    pass
    
    def _validate_links(self, content: str, lines: List[str],
                        result: ValidationResult, file_path: str):
        """验证链接"""
        for match in self.INTERNAL_LINK_PATTERN.finditer(content):
            link_text = match.group(1)
            link_target = match.group(2)
            line_num = self._find_line_number(content, match.start(), lines)
            
            # 跳过外部链接
            if link_target.startswith(('http://', 'https://', 'mailto:')):
                if self.check_external_links:
                    # 可选：检查外部链接可达性
                    pass
                continue
            
            # 解析链接
            parsed = urllib.parse.urlparse(link_target)
            target_path = parsed.path
            target_anchor = parsed.fragment
            
            if target_path:
                # 文件链接
                # 解析相对路径
                if target_path.startswith('/'):
                    # 绝对路径（相对于项目根）
                    full_target = target_path.lstrip('/')
                else:
                    # 相对路径
                    current_dir = Path(file_path).parent
                    full_target = str(current_dir / target_path)
                
                # 规范化路径
                full_target = str(Path(full_target)).replace('\\', '/')
                
                # 检查文件是否存在
                if full_target not in self.all_files:
                    # 尝试添加.md后缀
                    full_target_md = full_target + '.md'
                    if full_target_md not in self.all_files:
                        result.add_issue(
                            line=line_num,
                            severity=Severity.ERROR,
                            code="LINK-001",
                            message=f"链接指向的文件不存在: {link_target}",
                            suggestion="检查文件路径是否正确，或添加.md后缀"
                        )
                    else:
                        full_target = full_target_md
                
                # 检查锚点
                if target_anchor:
                    if target_anchor not in self.all_anchors.get(full_target, set()):
                        result.add_issue(
                            line=line_num,
                            severity=Severity.WARNING,
                            code="LINK-002",
                            message=f"链接指向的锚点可能不存在: #{target_anchor}",
                            suggestion="检查锚点名称是否正确，或添加显式锚点"
                        )
            else:
                # 纯锚点链接
                if target_anchor:
                    if target_anchor not in self.all_anchors.get(file_path, set()):
                        result.add_issue(
                            line=line_num,
                            severity=Severity.WARNING,
                            code="LINK-003",
                            message=f"内部锚点可能不存在: #{target_anchor}",
                            suggestion=f"确保标题 '{target_anchor}' 存在，或使用 {{#{target_anchor}}} 显式定义"
                        )
    
    def _validate_citations(self, content: str, lines: List[str],
                           result: ValidationResult, file_path: str):
        """验证引用标注"""
        used_citations = set()
        for match in self.CITATION_PATTERN.finditer(content):
            ref_id = f"^{match.group(1)}"
            used_citations.add(ref_id)
        
        # 检查是否有定义
        defined_citations = set(self.all_citations.get(file_path, {}).keys())
        
        # 未定义的引用
        for ref_id in used_citations - defined_citations:
            # 查找引用位置
            for match in self.CITATION_PATTERN.finditer(content):
                if f"^{match.group(1)}" == ref_id:
                    line_num = self._find_line_number(content, match.start(), lines)
                    result.add_issue(
                        line=line_num,
                        severity=Severity.ERROR,
                        code="CITE-001",
                        message=f"引用未定义: [{ref_id}]",
                        suggestion=f"在文档末尾添加: [{ref_id}]: 引用内容"
                    )
                    break
        
        # 未使用的引用定义
        for ref_id in defined_citations - used_citations:
            result.add_issue(
                line=0,
                severity=Severity.INFO,
                code="CITE-002",
                message=f"引用已定义但未使用: [{ref_id}]",
                suggestion="删除未使用的引用定义"
            )
    
    def validate_registry(self, registry_path: Path) -> List[Issue]:
        """
        验证定理注册表
        
        检查：
        1. 注册表中的定理是否都有定义
        2. 定义的定理是否都在注册表中
        3. 编号格式是否一致
        """
        issues = []
        
        if not registry_path.exists():
            return [Issue(
                file=str(registry_path),
                line=0,
                severity=Severity.WARNING,
                code="REG-001",
                message=f"定理注册表不存在: {registry_path}",
                suggestion="创建 THEOREM-REGISTRY.md 或更新配置"
            )]
        
        try:
            content = registry_path.read_text(encoding='utf-8')
        except Exception as e:
            return [Issue(
                file=str(registry_path),
                line=0,
                severity=Severity.ERROR,
                code="REG-002",
                message=f"无法读取注册表: {e}",
                suggestion="检查文件权限"
            )]
        
        # 从注册表提取定理
        registry_theorems = set()
        for match in self.THEOREM_PATTERN.finditer(content):
            theorem_id = f"{match.group(1)}-{match.group(2)}-{match.group(3)}-{match.group(4)}"
            registry_theorems.add(theorem_id)
        
        # 检查差异
        defined_theorems = set(self.all_theorems.keys())
        
        # 在文档中定义但不在注册表中
        for theorem_id in defined_theorems - registry_theorems:
            info = self.all_theorems[theorem_id]
            issues.append(Issue(
                file=info['file'],
                line=info['line'],
                severity=Severity.WARNING,
                code="REG-003",
                message=f"定理 {theorem_id} 未在注册表中登记",
                suggestion=f"在 {registry_path} 中添加该定理"
            ))
        
        # 在注册表中但不在文档中
        for theorem_id in registry_theorems - defined_theorems:
            issues.append(Issue(
                file=str(registry_path),
                line=0,
                severity=Severity.INFO,
                code="REG-004",
                message=f"注册表中的定理 {theorem_id} 在文档中未找到",
                suggestion="检查定理编号是否正确，或删除注册表中的条目"
            ))
        
        return issues
    
    def _find_line_number(self, content: str, position: int, 
                          lines: List[str]) -> int:
        """根据字符位置查找行号"""
        line_num = 1
        current_pos = 0
        for line in lines:
            if current_pos + len(line) + 1 > position:
                return line_num
            current_pos += len(line) + 1
            line_num += 1
        return line_num
    
    def validate_directory(self, directory: Path) -> List[ValidationResult]:
        """验证整个目录"""
        # 首先构建引用数据库
        self.build_reference_database(directory)
        
        results = []
        md_files = list(directory.rglob("*.md"))
        exclude_patterns = ['.git', 'node_modules', '.venv', '__pycache__']
        md_files = [
            f for f in md_files 
            if not any(p in str(f) for p in exclude_patterns)
        ]
        
        print(f"\n验证 {len(md_files)} 个文件的引用...")
        
        for file_path in md_files:
            result = self.validate_file(file_path)
            results.append(result)
        
        # 验证注册表
        registry_path = self.root_dir / self.registry_file
        registry_issues = self.validate_registry(registry_path)
        
        # 将注册表问题添加到结果
        if registry_issues:
            registry_result = ValidationResult(file_path=str(registry_path))
            registry_result.issues = registry_issues
            registry_result.passed = not any(i.severity == Severity.ERROR for i in registry_issues)
            results.append(registry_result)
        
        return results
    
    def print_report(self, results: List[ValidationResult], ci_mode: bool = False):
        """打印验证报告"""
        total_files = len(results)
        passed_files = sum(1 for r in results if r.passed)
        total_issues = sum(len(r.issues) for r in results)
        error_count = sum(
            1 for r in results for i in r.issues if i.severity == Severity.ERROR
        )
        warning_count = sum(
            1 for r in results for i in r.issues if i.severity == Severity.WARNING
        )
        
        # 统计重复定理
        duplicate_theorems = [
            (tid, info) for tid, info in self.all_theorems.items()
            if len(info.get('duplicates', [])) > 0
        ]
        
        if ci_mode:
            print(f"::group::Reference Validation Results")
            print(f"Total files: {total_files}")
            print(f"Passed: {passed_files}")
            print(f"Errors: {error_count}")
            print(f"Warnings: {warning_count}")
            print(f"Duplicate theorems: {len(duplicate_theorems)}")
            
            for result in results:
                for issue in result.issues:
                    if issue.severity == Severity.ERROR:
                        print(f"::error file={issue.file},line={issue.line}::{issue.code}: {issue.message}")
                    elif issue.severity == Severity.WARNING:
                        print(f"::warning file={issue.file},line={issue.line}::{issue.code}: {issue.message}")
            print(f"::endgroup::")
        else:
            print("\n" + "=" * 80)
            print("引用验证报告")
            print("=" * 80)
            print(f"验证文件数: {total_files}")
            print(f"通过: {passed_files} | 失败: {total_files - passed_files}")
            print(f"问题总计: {total_issues} (错误: {error_count}, 警告: {warning_count})")
            print(f"重复定理: {len(duplicate_theorems)}")
            print("=" * 80)
            
            # 显示重复定理
            if duplicate_theorems:
                print("\n🔄 重复的定理编号:")
                for theorem_id, info in duplicate_theorems[:10]:
                    print(f"\n  {theorem_id}:")
                    print(f"    - {info['file']}:{info['line']}")
                    for dup in info['duplicates']:
                        print(f"    - {dup['file']}:{dup['line']}")
            
            # 显示问题文件
            failed_results = [r for r in results if not r.passed]
            if failed_results:
                print("\n❌ 存在引用问题的文件:")
                for result in failed_results[:10]:
                    print(f"\n📄 {result.file_path}")
                    for issue in result.issues[:5]:
                        severity_icon = "🔴" if issue.severity == Severity.ERROR else "🟡"
                        print(f"   {severity_icon} [{issue.code}] 行{issue.line}: {issue.message}")
                        if issue.suggestion:
                            print(f"      💡 {issue.suggestion}")
            
            print("\n" + "=" * 80)
            if error_count == 0:
                print("✅ 引用验证通过！")
            else:
                print(f"❌ 发现 {error_count} 个引用错误")
            print("=" * 80)


def load_config(config_path: Path) -> Dict:
    """加载配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"错误: 无法加载配置文件: {e}", file=sys.stderr)
        sys.exit(ExitCode.CONFIG_ERROR)


def main():
    """主入口函数"""
    parser = argparse.ArgumentParser(
        description="引用验证器 - 验证交叉引用和定理编号",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s document.md
  %(prog)s --registry THEOREM-REGISTRY.md .
  %(prog)s --ci Struct/ Knowledge/ Flink/
        """
    )
    
    parser.add_argument(
        'paths',
        nargs='+',
        help='要验证的文件或目录路径'
    )
    parser.add_argument(
        '--config', '-c',
        type=Path,
        help='配置文件路径 (JSON格式)'
    )
    parser.add_argument(
        '--registry', '-r',
        type=Path,
        default='THEOREM-REGISTRY.md',
        help='定理注册表文件路径'
    )
    parser.add_argument(
        '--ci',
        action='store_true',
        help='CI模式：简洁输出'
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='输出报告到文件 (JSON格式)'
    )
    
    args = parser.parse_args()
    
    # 加载配置
    config = {}
    if args.config:
        config = load_config(args.config)
    if args.registry:
        config['registry_file'] = str(args.registry)
    
    # 创建验证器
    validator = ReferenceValidator(config)
    
    # 验证所有路径
    all_results = []
    for path_str in args.paths:
        path = Path(path_str)
        if not path.exists():
            print(f"错误: 路径不存在: {path}", file=sys.stderr)
            sys.exit(ExitCode.FILE_ERROR)
        
        if path.is_file():
            # 单个文件：也需要先构建数据库
            validator.build_reference_database(path.parent)
            result = validator.validate_file(path)
            all_results.append(result)
        elif path.is_dir():
            results = validator.validate_directory(path)
            all_results.extend(results)
    
    # 打印报告
    validator.print_report(all_results, ci_mode=args.ci)
    
    # 保存报告
    if args.output:
        report_data = {
            'results': [
                {
                    'file': r.file_path,
                    'passed': r.passed,
                    'issues': [
                        {
                            'line': i.line,
                            'severity': i.severity.name,
                            'code': i.code,
                            'message': i.message,
                            'suggestion': i.suggestion
                        }
                        for i in r.issues
                    ]
                }
                for r in all_results
            ],
            'theorem_summary': {
                'total_defined': len(validator.all_theorems),
                'duplicates': [
                    {
                        'id': tid,
                        'locations': [
                            {'file': info['file'], 'line': info['line']}
                        ] + info.get('duplicates', [])
                    }
                    for tid, info in validator.all_theorems.items()
                    if info.get('duplicates')
                ]
            },
            'summary': {
                'total_files': len(all_results),
                'passed_files': sum(1 for r in all_results if r.passed),
                'total_issues': sum(len(r.issues) for r in all_results),
                'error_count': sum(
                    1 for r in all_results 
                    for i in r.issues if i.severity == Severity.ERROR
                ),
                'warning_count': sum(
                    1 for r in all_results 
                    for i in r.issues if i.severity == Severity.WARNING
                )
            }
        }
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        print(f"\n报告已保存到: {args.output}")
    
    # 返回退出码
    has_errors = any(
        i.severity == Severity.ERROR 
        for r in all_results for i in r.issues
    )
    sys.exit(ExitCode.REFERENCE_ERROR if has_errors else ExitCode.SUCCESS)


if __name__ == '__main__':
    main()
