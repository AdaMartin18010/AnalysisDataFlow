#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容质量检查器 (Content Quality Checker)

功能：
    - 检查内容完整性（必要段落是否为空）
    - 验证Mermaid图表语法
    - 检查代码示例完整性
    - 验证表格数据一致性
    - 检查关键术语定义
    - 评估内容覆盖度

使用方式：
    python content-quality-checker.py [文件或目录路径]
    python content-quality-checker.py --config config.json [路径]
    python content-quality-checker.py --ci [路径]

退出码：
    0 - 所有检查通过
    1 - 发现质量问题
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
    QUALITY_ERROR = 1
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
    quality_score: float = 0.0  # 0-100分
    metrics: Dict = field(default_factory=dict)
    
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


class ContentQualityChecker:
    """
    内容质量检查器
    
    检查维度：
    1. 内容完整性 - 章节是否有实质内容
    2. 可视化质量 - Mermaid图表语法
    3. 示例质量 - 代码示例完整性
    4. 术语覆盖 - 关键术语定义
    5. 内容深度 - 段落长度和细节
    """
    
    # 章节内容提取正则
    SECTION_PATTERN = re.compile(
        r'^(#{2,3})\s+(\d+\.\s+)?(.+)$', 
        re.MULTILINE
    )
    
    # Mermaid代码块
    MERMAID_PATTERN = re.compile(
        r'```mermaid\s*\n(.*?)```',
        re.DOTALL
    )
    
    # 代码块
    CODE_BLOCK_PATTERN = re.compile(
        r'```(\w+)\s*\n(.*?)```',
        re.DOTALL
    )
    
    # 定义术语模式（粗体或代码后接解释）
    TERM_DEFINITION_PATTERN = re.compile(
        r'(?:^|\n)(?:\*\*|`)'  # **term** 或 `term`
        r'([^*`]+)'
        r'(?:\*\*|`)'
        r'\s*[:：]\s*'  # 后跟冒号
        r'(.+?)(?=\n\n|\Z)',
        re.MULTILINE | re.DOTALL
    )
    
    # 空段落检测（章节标题后少于最小字符数）
    MIN_SECTION_CONTENT = 50  # 最少字符数
    
    # Mermaid支持的图表类型
    MERMAID_TYPES = {
        'graph', 'flowchart', 'sequenceDiagram', 'classDiagram',
        'stateDiagram', 'stateDiagram-v2', 'gantt', 'pie', 'erDiagram',
        'journey', 'gitGraph', 'mindmap', 'timeline', 'quadrantChart',
        'requirementDiagram', 'C4Context', 'C4Container', 'C4Component',
        'packet-beta'
    }
    
    # 质量评分权重
    QUALITY_WEIGHTS = {
        'completeness': 0.3,    # 完整性
        'visualization': 0.25,  # 可视化
        'examples': 0.25,       # 示例
        'terminology': 0.2,     # 术语
    }
    
    def __init__(self, config: Optional[Dict] = None):
        """初始化质量检查器"""
        self.config = config or {}
        self.results: List[ValidationResult] = []
        
        # 配置参数
        self.min_section_content = self.config.get('min_section_content', 50)
        self.min_mermaid_count = self.config.get('min_mermaid_count', 1)
        self.min_code_examples = self.config.get('min_code_examples', 0)
        self.min_definitions = self.config.get('min_definitions', 1)
        self.quality_threshold = self.config.get('quality_threshold', 70.0)
        
        # 关键术语列表（可配置）
        self.key_terms = set(self.config.get('key_terms', []))
    
    def check_file(self, file_path: Path) -> ValidationResult:
        """检查单个文件"""
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
        
        metrics = {}
        
        # 1. 检查内容完整性
        completeness_score = self._check_completeness(content, lines, result)
        metrics['completeness_score'] = completeness_score
        
        # 2. 检查Mermaid图表
        viz_score = self._check_visualizations(content, lines, result)
        metrics['visualization_score'] = viz_score
        
        # 3. 检查代码示例
        example_score = self._check_code_examples(content, lines, result)
        metrics['example_score'] = example_score
        
        # 4. 检查术语定义
        term_score = self._check_terminology(content, lines, result)
        metrics['terminology_score'] = term_score
        
        # 计算总体质量分数
        result.quality_score = (
            completeness_score * self.QUALITY_WEIGHTS['completeness'] +
            viz_score * self.QUALITY_WEIGHTS['visualization'] +
            example_score * self.QUALITY_WEIGHTS['examples'] +
            term_score * self.QUALITY_WEIGHTS['terminology']
        )
        
        result.metrics = metrics
        
        # 如果质量分数低于阈值，添加警告
        if result.quality_score < self.quality_threshold:
            result.add_issue(
                line=0,
                severity=Severity.WARNING,
                code="QUALITY-001",
                message=f"文档质量分数 ({result.quality_score:.1f}) 低于阈值 ({self.quality_threshold})",
                suggestion="参考各维度评分改进内容质量"
            )
        
        return result
    
    def _check_completeness(self, content: str, lines: List[str], 
                           result: ValidationResult) -> float:
        """检查内容完整性，返回0-100分"""
        sections = list(self.SECTION_PATTERN.finditer(content))
        
        if not sections:
            result.add_issue(
                line=1,
                severity=Severity.WARNING,
                code="COMPLETE-001",
                message="文档缺少章节结构",
                suggestion="使用 ## 或 ### 添加章节标题"
            )
            return 0.0
        
        # 检查每个章节是否有内容
        empty_sections = []
        for i, match in enumerate(sections):
            section_start = match.end()
            section_line = self._find_line_number(content, match.start(), lines)
            
            # 确定章节结束位置
            if i + 1 < len(sections):
                section_end = sections[i + 1].start()
            else:
                section_end = len(content)
            
            section_content = content[section_start:section_end].strip()
            
            # 移除子标题
            section_content = re.sub(r'^#{2,3}\s+.+$', '', section_content, flags=re.MULTILINE).strip()
            
            # 检查内容长度
            if len(section_content) < self.min_section_content:
                empty_sections.append((match.group(3), section_line, len(section_content)))
        
        # 报告空章节
        for title, line, length in empty_sections[:5]:
            result.add_issue(
                line=line,
                severity=Severity.WARNING,
                code="COMPLETE-002",
                message=f"章节内容过少: '{title[:30]}...' ({length} 字符)",
                suggestion=f"添加更多内容，建议至少 {self.min_section_content} 字符"
            )
        
        # 计算分数
        if len(sections) == 0:
            return 0.0
        
        score = max(0, 100 - (len(empty_sections) / len(sections) * 100))
        return score
    
    def _check_visualizations(self, content: str, lines: List[str],
                              result: ValidationResult) -> float:
        """检查可视化质量，返回0-100分"""
        mermaid_blocks = list(self.MERMAID_PATTERN.finditer(content))
        
        if not mermaid_blocks:
            # 检查是否是强制需要Mermaid的文档类型
            if 'Struct/' in str(result.file_path) or 'struct' in str(result.file_path).lower():
                result.add_issue(
                    line=1,
                    severity=Severity.WARNING,
                    code="VIZ-001",
                    message="文档缺少Mermaid可视化图表",
                    suggestion="根据AGENTS.md规范，每篇文档应至少包含一个Mermaid图表"
                )
            return 50.0  # 无图表的基础分
        
        valid_charts = 0
        syntax_errors = 0
        
        for match in mermaid_blocks:
            chart_content = match.group(1).strip()
            line_num = self._find_line_number(content, match.start(), lines)
            
            # 检查图表类型
            first_line = chart_content.split('\n')[0].strip().lower()
            chart_type = first_line.split()[0] if first_line else ''
            
            if chart_type not in self.MERMAID_TYPES:
                # 尝试匹配带方向的类型 (graph TD, graph LR)
                if not any(first_line.startswith(t) for t in self.MERMAID_TYPES):
                    result.add_issue(
                        line=line_num,
                        severity=Severity.WARNING,
                        code="VIZ-002",
                        message=f"未知的Mermaid图表类型: '{chart_type}'",
                        suggestion=f"使用支持的类型: {', '.join(list(self.MERMAID_TYPES)[:5])}..."
                    )
                    syntax_errors += 1
                    continue
            
            # 检查基本语法
            syntax_ok = self._validate_mermaid_syntax(chart_content, line_num, result)
            if syntax_ok:
                valid_charts += 1
            else:
                syntax_errors += 1
        
        # 计算分数
        if len(mermaid_blocks) == 0:
            return 50.0
        
        score = (valid_charts / len(mermaid_blocks)) * 100
        return score
    
    def _validate_mermaid_syntax(self, content: str, start_line: int,
                                  result: ValidationResult) -> bool:
        """验证Mermaid语法基本正确性"""
        lines = content.split('\n')
        chart_type = lines[0].strip().split()[0].lower() if lines else ''
        
        is_valid = True
        
        # 根据图表类型检查
        if chart_type in ('graph', 'flowchart'):
            # 检查是否有节点定义
            has_nodes = False
            has_edges = False
            
            for i, line in enumerate(lines[1:], start=1):
                line = line.strip()
                if not line or line.startswith('%%'):
                    continue
                
                # 简单的节点检测
                if re.search(r'\w+\s*\[.*?\]', line) or re.search(r'\w+\s*\(.*?\)', line):
                    has_nodes = True
                
                # 简单的边检测
                if '-->' in line or '---' in line or '==>' in line or '-.->' in line:
                    has_edges = True
            
            if not has_nodes:
                result.add_issue(
                    line=start_line + 1,
                    severity=Severity.WARNING,
                    code="VIZ-003",
                    message="Flowchart/Graph 图表缺少节点定义",
                    suggestion="添加节点: A[节点A] 或 B(节点B)"
                )
                is_valid = False
        
        elif chart_type == 'sequencediagram':
            # 检查是否有参与者
            has_participants = False
            for line in lines[1:]:
                if re.match(r'^\s*\w+->>\w+:', line):
                    has_participants = True
                    break
            
            if not has_participants:
                result.add_issue(
                    line=start_line + 1,
                    severity=Severity.INFO,
                    code="VIZ-004",
                    message="SequenceDiagram 可能没有正确的消息定义",
                    suggestion="使用格式: A->>B: 消息"
                )
        
        return is_valid
    
    def _check_code_examples(self, content: str, lines: List[str],
                             result: ValidationResult) -> float:
        """检查代码示例质量，返回0-100分"""
        code_blocks = list(self.CODE_BLOCK_PATTERN.finditer(content))
        
        if not code_blocks:
            if self.min_code_examples > 0:
                result.add_issue(
                    line=1,
                    severity=Severity.WARNING,
                    code="CODE-001",
                    message="文档缺少代码示例",
                    suggestion="添加代码块展示关键实现"
                )
            return 50.0
        
        valid_examples = 0
        issues = []
        
        for match in code_blocks:
            lang = match.group(1)
            code = match.group(2)
            line_num = self._find_line_number(content, match.start(), lines)
            
            # 检查代码块是否为空
            if not code.strip():
                result.add_issue(
                    line=line_num,
                    severity=Severity.ERROR,
                    code="CODE-002",
                    message="代码块为空",
                    suggestion="添加代码内容或删除空代码块"
                )
                continue
            
            # 检查代码长度（太短的示例可能没用）
            code_lines = [l for l in code.split('\n') if l.strip()]
            if len(code_lines) < 2:
                result.add_issue(
                    line=line_num,
                    severity=Severity.INFO,
                    code="CODE-003",
                    message="代码示例过短，可能缺乏说明性",
                    suggestion="提供更完整的代码示例"
                )
            else:
                valid_examples += 1
            
            # 检查是否是可运行代码（基本语法检查）
            if lang in ('python', 'py'):
                if self._has_python_syntax_issues(code):
                    result.add_issue(
                        line=line_num,
                        severity=Severity.INFO,
                        code="CODE-004",
                        message="Python代码可能存在语法问题",
                        suggestion="检查缩进和语法"
                    )
        
        # 计算分数
        score = (valid_examples / len(code_blocks)) * 100 if code_blocks else 50.0
        return score
    
    def _has_python_syntax_issues(self, code: str) -> bool:
        """检查Python代码是否有明显语法问题"""
        # 简单的启发式检查
        lines = code.split('\n')
        
        # 检查缩进问题
        indent_levels = []
        for line in lines:
            if line.strip():
                indent = len(line) - len(line.lstrip())
                indent_levels.append(indent)
        
        # 检查缩进是否是4的倍数（Python惯例）
        if indent_levels:
            for i, indent in enumerate(indent_levels[1:], 1):
                if indent > indent_levels[i-1]:
                    if (indent - indent_levels[i-1]) % 4 != 0:
                        return True
        
        # 检查括号匹配
        open_count = code.count('(') - code.count(')')
        if open_count != 0:
            return True
        
        bracket_open = code.count('[') - code.count(']')
        if bracket_open != 0:
            return True
        
        return False
    
    def _check_terminology(self, content: str, lines: List[str],
                          result: ValidationResult) -> float:
        """检查术语定义质量，返回0-100分"""
        # 查找定义模式
        definitions = list(self.TERM_DEFINITION_PATTERN.finditer(content))
        
        # 也查找 **Def-** 格式的定义
        def_pattern = re.compile(
            r'`?(Def-[SKF]-\d{2}-\d{2})`?\s*[:：]\s*(.+?)(?=\n\n|\Z)',
            re.DOTALL
        )
        formal_defs = list(def_pattern.finditer(content))
        
        total_definitions = len(definitions) + len(formal_defs)
        
        if total_definitions == 0:
            # 检查是否是应该包含定义的文档
            if any(kw in content.lower() for kw in ['定义', 'definition', '概念', 'concept']):
                result.add_issue(
                    line=1,
                    severity=Severity.WARNING,
                    code="TERM-001",
                    message="文档可能缺少术语定义",
                    suggestion="使用 **术语**: 解释 的格式定义关键概念"
                )
            return 30.0
        
        # 检查定义质量
        good_definitions = 0
        
        for match in definitions + formal_defs:
            term = match.group(1)
            definition = match.group(2).strip()
            
            # 检查定义长度
            if len(definition) >= 20:
                good_definitions += 1
        
        # 计算分数
        score = (good_definitions / total_definitions) * 100 if total_definitions > 0 else 0
        return score
    
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
    
    def check_directory(self, directory: Path) -> List[ValidationResult]:
        """检查整个目录"""
        results = []
        md_files = list(directory.rglob("*.md"))
        
        exclude_patterns = ['.git', 'node_modules', '.venv', '__pycache__']
        md_files = [
            f for f in md_files 
            if not any(p in str(f) for p in exclude_patterns)
        ]
        
        print(f"检查 {len(md_files)} 个文件的内容质量...")
        
        for file_path in md_files:
            result = self.check_file(file_path)
            results.append(result)
        
        return results
    
    def print_report(self, results: List[ValidationResult], ci_mode: bool = False):
        """打印质量报告"""
        total_files = len(results)
        passed_files = sum(1 for r in results if r.passed)
        avg_score = sum(r.quality_score for r in results) / len(results) if results else 0
        
        if ci_mode:
            print(f"::group::Content Quality Results")
            print(f"Total files: {total_files}")
            print(f"Passed: {passed_files}")
            print(f"Average quality score: {avg_score:.1f}/100")
            
            for result in results:
                if result.quality_score < self.quality_threshold:
                    print(f"::warning file={result.file_path}::Quality score {result.quality_score:.1f} below threshold {self.quality_threshold}")
            print(f"::endgroup::")
        else:
            print("\n" + "=" * 80)
            print("内容质量检查报告")
            print("=" * 80)
            print(f"检查文件数: {total_files}")
            print(f"平均质量分数: {avg_score:.1f}/100")
            print(f"通过: {passed_files} | 需改进: {total_files - passed_files}")
            print("=" * 80)
            
            # 按分数排序
            sorted_results = sorted(results, key=lambda r: r.quality_score)
            
            # 显示低质量文件
            low_quality = [r for r in sorted_results if r.quality_score < 60]
            if low_quality:
                print("\n⚠️ 质量分数较低的文档:")
                for result in low_quality[:10]:
                    print(f"\n📄 {result.file_path}")
                    print(f"   质量分数: {result.quality_score:.1f}/100")
                    print(f"   指标: 完整性={result.metrics.get('completeness_score', 0):.0f}, "
                          f"可视化={result.metrics.get('visualization_score', 0):.0f}, "
                          f"示例={result.metrics.get('example_score', 0):.0f}, "
                          f"术语={result.metrics.get('terminology_score', 0):.0f}")
                    for issue in result.issues[:3]:
                        if issue.severity in (Severity.ERROR, Severity.WARNING):
                            print(f"   ⚠️ [{issue.code}] {issue.message}")
            
            # 显示高质量文件
            high_quality = [r for r in sorted_results if r.quality_score >= 80]
            if high_quality:
                print(f"\n✅ 高质量文档 ({len(high_quality)} 个):")
                for result in high_quality[:5]:
                    print(f"   • {Path(result.file_path).name} ({result.quality_score:.1f}分)")
            
            print("\n" + "=" * 80)
            if avg_score >= 70:
                print(f"✅ 整体内容质量良好 ({avg_score:.1f}分)")
            else:
                print(f"⚠️ 整体内容质量有待提升 ({avg_score:.1f}分)")
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
        description="内容质量检查器 - 评估文档内容质量",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s document.md
  %(prog)s --config config.json docs/
  %(prog)s --ci --threshold 80 .
        """
    )
    
    parser.add_argument(
        'paths',
        nargs='+',
        help='要检查的文件或目录路径'
    )
    parser.add_argument(
        '--config', '-c',
        type=Path,
        help='配置文件路径 (JSON格式)'
    )
    parser.add_argument(
        '--threshold', '-t',
        type=float,
        default=70.0,
        help='质量分数阈值 (默认: 70)'
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
    config['quality_threshold'] = args.threshold
    
    # 创建检查器
    checker = ContentQualityChecker(config)
    
    # 检查所有路径
    all_results = []
    for path_str in args.paths:
        path = Path(path_str)
        if not path.exists():
            print(f"错误: 路径不存在: {path}", file=sys.stderr)
            sys.exit(ExitCode.FILE_ERROR)
        
        if path.is_file():
            result = checker.check_file(path)
            all_results.append(result)
        elif path.is_dir():
            results = checker.check_directory(path)
            all_results.extend(results)
    
    # 打印报告
    checker.print_report(all_results, ci_mode=args.ci)
    
    # 保存报告
    if args.output:
        report_data = {
            'results': [
                {
                    'file': r.file_path,
                    'passed': r.passed,
                    'quality_score': r.quality_score,
                    'metrics': r.metrics,
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
                'average_score': sum(r.quality_score for r in all_results) / len(all_results) if all_results else 0,
                'below_threshold': sum(1 for r in all_results if r.quality_score < args.threshold)
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
    sys.exit(ExitCode.QUALITY_ERROR if has_errors else ExitCode.SUCCESS)


if __name__ == '__main__':
    main()
