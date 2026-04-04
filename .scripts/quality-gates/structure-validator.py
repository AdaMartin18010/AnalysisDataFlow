#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档结构验证器 (Structure Validator)

功能：
    - 验证文档六段式模板完整性
    - 检查必要章节是否存在
    - 验证文档元信息（所属阶段、前置依赖、形式化等级）
    - 检查定理/定义编号体系

使用方式：
    python structure-validator.py [文件或目录路径]
    python structure-validator.py --config config.json [路径]
    python structure-validator.py --ci [路径]  # CI/CD模式

退出码：
    0 - 所有检查通过
    1 - 发现结构错误
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


class ExitCode(IntEnum):
    """退出码定义"""
    SUCCESS = 0
    STRUCTURE_ERROR = 1
    CONFIG_ERROR = 2
    FILE_ERROR = 3


class Severity(IntEnum):
    """问题严重级别"""
    ERROR = 3      # 严重错误，必须修复
    WARNING = 2    # 警告，建议修复
    INFO = 1       # 信息提示


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
        """添加问题记录"""
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


class StructureValidator:
    """
    文档结构验证器
    
    根据 AGENTS.md 规范验证：
    1. 六段式模板完整性
    2. 文档元信息
    3. 定理/定义编号体系
    """
    
    # 六段式必需章节（中英文标题均可）
    REQUIRED_SECTIONS = [
        ("概念定义", "Definitions"),
        ("属性推导", "Properties"),
        ("关系建立", "Relations"),
        ("论证过程", "Argumentation"),
        ("形式证明", "Proof"),
        ("工程论证", "Engineering Argument"),
        ("实例验证", "Examples"),
        ("可视化", "Visualizations"),
        ("引用参考", "References"),
    ]
    
    # 必需章节的最小数量（至少有6个主要章节）
    MIN_REQUIRED_SECTIONS = 6
    
    # 文档元信息正则
    META_PATTERN = re.compile(
        r'>\s*所属阶段:\s*(\S+).*?\|'
        r'.*?前置依赖:\s*([^|]+)\|'
        r'.*?形式化等级:\s*(L[1-6])',
        re.DOTALL | re.IGNORECASE
    )
    
    # 定理编号正则: Thm-S-01-01, Lemma-K-02-03, Def-F-01-01 等
    THEOREM_PATTERN = re.compile(
        r'`?(Thm|Lemma|Def|Prop|Cor)-([SKF])-(\d{2})-(\d{2})`?'
    )
    
    # 章节标题正则
    SECTION_PATTERN = re.compile(r'^(#{1,3})\s+(.+)$', re.MULTILINE)
    
    # 引用格式正则: [^1], [^n]
    CITATION_PATTERN = re.compile(r'\[\^(\d+)\]')
    
    # 有效阶段
    VALID_STAGES = {"Struct", "Knowledge", "Flink", "Struct/", "Knowledge/", "Flink/"}
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化验证器
        
        Args:
            config: 配置字典，可覆盖默认规则
        """
        self.config = config or {}
        self.results: List[ValidationResult] = []
        self.global_theorems: Set[str] = set()  # 全局定理编号集合
        self.duplicate_theorems: Dict[str, List[str]] = {}  # 重复定理
        
        # 从配置加载规则
        self.min_sections = self.config.get('min_sections', self.MIN_REQUIRED_SECTIONS)
        self.required_sections = self.config.get('required_sections', self.REQUIRED_SECTIONS)
        self.strict_mode = self.config.get('strict_mode', False)
        
    def validate_file(self, file_path: Path) -> ValidationResult:
        """
        验证单个文件
        
        Args:
            file_path: Markdown文件路径
            
        Returns:
            ValidationResult: 验证结果
        """
        result = ValidationResult(file_path=str(file_path))
        
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
        
        # 1. 验证文档元信息
        self._validate_meta_info(content, lines, result)
        
        # 2. 验证六段式结构
        self._validate_six_section_structure(content, lines, result)
        
        # 3. 验证定理编号
        self._validate_theorem_numbering(content, lines, result, file_path)
        
        # 4. 验证引用格式
        self._validate_citations(content, lines, result)
        
        return result
    
    def _validate_meta_info(self, content: str, lines: List[str], 
                           result: ValidationResult):
        """验证文档元信息"""
        # 查找元信息行（通常在文档开头）
        meta_match = self.META_PATTERN.search(content)
        
        if not meta_match:
            # 尝试查找简化版元信息
            if not re.search(r'>\s*所属阶段:', content):
                result.add_issue(
                    line=1,
                    severity=Severity.ERROR,
                    code="META-001",
                    message="缺少文档元信息（所属阶段、前置依赖、形式化等级）",
                    suggestion="在标题后添加: > 所属阶段: Struct | 前置依赖: [] | 形式化等级: L1"
                )
            return
        
        stage = meta_match.group(1).strip()
        dependencies = meta_match.group(2).strip()
        level = meta_match.group(3)
        
        # 验证阶段
        if stage not in self.VALID_STAGES:
            result.add_issue(
                line=self._find_line_number(content, meta_match.start(), lines),
                severity=Severity.WARNING,
                code="META-002",
                message=f"未知的阶段: '{stage}'",
                suggestion=f"使用有效阶段: {', '.join(self.VALID_STAGES)}"
            )
        
        # 验证形式化等级
        if level not in {f"L{i}" for i in range(1, 7)}:
            result.add_issue(
                line=self._find_line_number(content, meta_match.start(), lines),
                severity=Severity.WARNING,
                code="META-003",
                message=f"无效的形式化等级: '{level}'",
                suggestion="使用 L1-L6 表示形式化等级"
            )
    
    def _validate_six_section_structure(self, content: str, lines: List[str],
                                        result: ValidationResult):
        """验证六段式模板结构"""
        sections = self.SECTION_PATTERN.findall(content)
        
        if not sections:
            result.add_issue(
                line=1,
                severity=Severity.ERROR,
                code="STRUCT-001",
                message="文档没有任何章节标题",
                suggestion="使用 ## 或 ### 添加章节标题"
            )
            return
        
        # 提取所有章节标题（去除#符号）
        section_titles = [s[1].strip() for s in sections]
        
        # 检查必需章节
        found_required = 0
        missing_sections = []
        
        for chinese, english in self.required_sections:
            found = any(
                chinese in title or english in title 
                for title in section_titles
            )
            if found:
                found_required += 1
            else:
                missing_sections.append(f"{chinese}/{english}")
        
        # 检查章节数量
        if found_required < self.min_sections:
            result.add_issue(
                line=self._find_line_number(content, content.find(sections[0][1]), lines),
                severity=Severity.ERROR if self.strict_mode else Severity.WARNING,
                code="STRUCT-002",
                message=f"必需章节不足: 找到 {found_required} 个，至少需要 {self.min_sections} 个",
                suggestion=f"添加缺失的章节: {', '.join(missing_sections[:3])}..."
            )
        
        # 检查一级标题（只能有一个）
        h1_count = sum(1 for s in sections if s[0] == '#')
        if h1_count == 0:
            result.add_issue(
                line=1,
                severity=Severity.ERROR,
                code="STRUCT-003",
                message="缺少文档主标题（一级标题 #）",
                suggestion="在文档开头添加: # 文档标题"
            )
        elif h1_count > 1:
            result.add_issue(
                line=1,
                severity=Severity.WARNING,
                code="STRUCT-004",
                message=f"文档有多个一级标题 ({h1_count} 个)",
                suggestion="只保留一个主标题，其他使用二级标题 ##"
            )
        
        # 检查章节顺序（可选：可以添加顺序检查）
        self._check_section_order(content, lines, section_titles, result)
    
    def _check_section_order(self, content: str, lines: List[str], 
                             section_titles: List[str], 
                             result: ValidationResult):
        """检查章节顺序是否合理"""
        # 定义推荐顺序
        recommended_order = [
            ("概念定义", "Definitions"),
            ("属性推导", "Properties"),
            ("关系建立", "Relations"),
            ("论证过程", "Argumentation"),
            ("形式证明", "Proof"),
            ("工程论证", "Engineering Argument"),
            ("实例验证", "Examples"),
            ("可视化", "Visualizations"),
            ("引用参考", "References"),
        ]
        
        # 找到实际出现的章节索引
        found_indices = []
        for title in section_titles:
            for idx, (ch, en) in enumerate(recommended_order):
                if ch in title or en in title:
                    found_indices.append(idx)
                    break
        
        # 检查是否基本有序（允许部分章节缺失）
        for i in range(1, len(found_indices)):
            if found_indices[i] < found_indices[i-1]:
                result.add_issue(
                    line=1,
                    severity=Severity.INFO,
                    code="STRUCT-005",
                    message="章节顺序可能与推荐顺序不符",
                    suggestion=f"推荐顺序: {' → '.join([c for c, e in recommended_order])}"
                )
                break
    
    def _validate_theorem_numbering(self, content: str, lines: List[str],
                                    result: ValidationResult, file_path: Path):
        """验证定理/定义编号体系"""
        theorems = self.THEOREM_PATTERN.findall(content)
        
        if not theorems:
            # 如果文档应该有定理但没有，给出警告
            if "Struct/" in str(file_path) or "struct" in str(file_path).lower():
                result.add_issue(
                    line=1,
                    severity=Severity.WARNING,
                    code="THEOREM-001",
                    message="Struct/ 目录文档未发现定理/定义编号",
                    suggestion="根据规范，Struct/ 文档必须包含至少一个 Def-* 或 Thm-* 编号"
                )
            return
        
        # 检查每个定理编号
        for match in self.THEOREM_PATTERN.finditer(content):
            theorem_type = match.group(1)  # Thm, Lemma, Def, etc.
            stage = match.group(2)         # S, K, F
            doc_num = match.group(3)       # 01
            seq_num = match.group(4)       # 01
            
            full_id = f"{theorem_type}-{stage}-{doc_num}-{seq_num}"
            
            # 检查全局唯一性
            if full_id in self.global_theorems:
                if full_id not in self.duplicate_theorems:
                    self.duplicate_theorems[full_id] = []
                self.duplicate_theorems[full_id].append(str(file_path))
                
                result.add_issue(
                    line=self._find_line_number(content, match.start(), lines),
                    severity=Severity.ERROR,
                    code="THEOREM-002",
                    message=f"定理编号重复: {full_id}",
                    suggestion="使用全局唯一的编号，参考 THEOREM-REGISTRY.md"
                )
            else:
                self.global_theorems.add(full_id)
            
            # 验证阶段一致性
            expected_stage = self._get_expected_stage(file_path)
            if expected_stage and stage != expected_stage:
                result.add_issue(
                    line=self._find_line_number(content, match.start(), lines),
                    severity=Severity.WARNING,
                    code="THEOREM-003",
                    message=f"定理阶段标记不一致: 使用 '{stage}' 但文档在 '{expected_stage}' 目录",
                    suggestion=f"使用正确的阶段标记: {expected_stage}"
                )
    
    def _validate_citations(self, content: str, lines: List[str],
                           result: ValidationResult):
        """验证引用格式"""
        citations = self.CITATION_PATTERN.findall(content)
        
        if not citations:
            # 检查是否有引用章节但没有引用
            if "引用参考" in content or "References" in content:
                # 检查引用列表
                ref_section_match = re.search(
                    r'(?:##\s+(?:\d+\.\s+)?(?:引用参考|References).*?\n)(.*?)(?=##|\Z)',
                    content,
                    re.DOTALL | re.IGNORECASE
                )
                if ref_section_match:
                    ref_content = ref_section_match.group(1)
                    if not re.search(r'\[\^\d+\]:', ref_content):
                        result.add_issue(
                            line=self._find_line_number(content, ref_section_match.start(), lines),
                            severity=Severity.WARNING,
                            code="CITE-001",
                            message="引用参考章节为空或格式不正确",
                            suggestion="使用格式: [^1]: 引用内容"
                        )
    
    def _get_expected_stage(self, file_path: Path) -> Optional[str]:
        """根据文件路径推断应有的阶段标记"""
        path_str = str(file_path).replace('\\', '/')
        if '/Struct/' in path_str or path_str.startswith('Struct/'):
            return 'S'
        elif '/Knowledge/' in path_str or path_str.startswith('Knowledge/'):
            return 'K'
        elif '/Flink/' in path_str or path_str.startswith('Flink/'):
            return 'F'
        return None
    
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
        """
        验证整个目录
        
        Args:
            directory: 要验证的目录
            
        Returns:
            List[ValidationResult]: 所有文件的验证结果
        """
        results = []
        
        # 查找所有Markdown文件
        md_files = list(directory.rglob("*.md"))
        
        # 排除某些目录
        exclude_patterns = ['.git', 'node_modules', '.venv', '__pycache__']
        md_files = [
            f for f in md_files 
            if not any(p in str(f) for p in exclude_patterns)
        ]
        
        print(f"找到 {len(md_files)} 个Markdown文件待验证...")
        
        for file_path in md_files:
            result = self.validate_file(file_path)
            results.append(result)
        
        # 检查全局重复
        self._check_global_duplicates(results)
        
        return results
    
    def _check_global_duplicates(self, results: List[ValidationResult]):
        """检查全局重复的定理编号"""
        for theorem_id, files in self.duplicate_theorems.items():
            if len(files) > 1:
                # 已经在每个文件中添加了错误，这里可以添加汇总信息
                pass
    
    def print_report(self, results: List[ValidationResult], ci_mode: bool = False):
        """
        打印验证报告
        
        Args:
            results: 验证结果列表
            ci_mode: 是否为CI模式（简洁输出）
        """
        total_files = len(results)
        passed_files = sum(1 for r in results if r.passed)
        total_issues = sum(len(r.issues) for r in results)
        error_count = sum(
            1 for r in results for i in r.issues if i.severity == Severity.ERROR
        )
        warning_count = sum(
            1 for r in results for i in r.issues if i.severity == Severity.WARNING
        )
        
        if ci_mode:
            # CI模式：简洁输出
            print(f"::group::Structure Validation Results")
            print(f"Total files: {total_files}")
            print(f"Passed: {passed_files}")
            print(f"Failed: {total_files - passed_files}")
            print(f"Errors: {error_count}")
            print(f"Warnings: {warning_count}")
            
            for result in results:
                if not result.passed:
                    for issue in result.issues:
                        if issue.severity == Severity.ERROR:
                            print(f"::error file={issue.file},line={issue.line}::{issue.code}: {issue.message}")
                        elif issue.severity == Severity.WARNING:
                            print(f"::warning file={issue.file},line={issue.line}::{issue.code}: {issue.message}")
            print(f"::endgroup::")
        else:
            # 正常模式：详细输出
            print("\n" + "=" * 80)
            print("文档结构验证报告")
            print("=" * 80)
            print(f"验证文件数: {total_files}")
            print(f"通过: {passed_files} | 失败: {total_files - passed_files}")
            print(f"问题总计: {total_issues} (错误: {error_count}, 警告: {warning_count})")
            print("=" * 80)
            
            # 显示失败的文件
            failed_results = [r for r in results if not r.passed]
            if failed_results:
                print("\n❌ 存在问题的文件:")
                for result in failed_results:
                    print(f"\n📄 {result.file_path}")
                    for issue in result.issues:
                        severity_icon = "🔴" if issue.severity == Severity.ERROR else "🟡"
                        print(f"   {severity_icon} [{issue.code}] 行{issue.line}: {issue.message}")
                        if issue.suggestion:
                            print(f"      💡 {issue.suggestion}")
            
            # 显示统计
            print("\n" + "=" * 80)
            if error_count == 0:
                print("✅ 所有文件结构验证通过！")
            else:
                print(f"❌ 发现 {error_count} 个错误，需要修复")
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
        description="文档结构验证器 - 验证六段式模板和文档结构",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s document.md
  %(prog)s --config config.json docs/
  %(prog)s --ci Struct/ Knowledge/
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
        '--ci',
        action='store_true',
        help='CI模式：简洁输出，适合GitHub Actions等CI环境'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='严格模式：警告视为错误'
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
    if args.strict:
        config['strict_mode'] = True
    
    # 创建验证器
    validator = StructureValidator(config)
    
    # 验证所有路径
    all_results = []
    for path_str in args.paths:
        path = Path(path_str)
        if not path.exists():
            print(f"错误: 路径不存在: {path}", file=sys.stderr)
            sys.exit(ExitCode.FILE_ERROR)
        
        if path.is_file():
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
    sys.exit(ExitCode.STRUCTURE_ERROR if has_errors else ExitCode.SUCCESS)


if __name__ == '__main__':
    main()
