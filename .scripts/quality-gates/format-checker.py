#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
格式检查器 (Format Checker)

功能：
    - 检查Markdown格式规范
    - 验证代码块语法高亮
    - 检查表格格式完整性
    - 验证列表格式一致性
    - 检查标题层级连续性
    - 验证中英文标点使用

使用方式：
    python format-checker.py [文件或目录路径]
    python format-checker.py --config config.json [路径]
    python format-checker.py --fix [路径]  # 尝试自动修复

退出码：
    0 - 所有检查通过
    1 - 发现格式错误
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
    FORMAT_ERROR = 1
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


class FormatChecker:
    """
    Markdown格式检查器
    
    检查项：
    1. 代码块语法高亮
    2. 表格格式完整性
    3. 列表格式一致性
    4. 标题层级连续性
    5. 中英文标点规范
    6. 空格和空行规范
    """
    
    # 支持的代码块语言（根据项目类型）
    SUPPORTED_LANGUAGES = {
        # 通用
        'text', 'txt', 'markdown', 'md',
        # 编程语言
        'python', 'py', 'java', 'scala', 'rust', 'go', 'javascript', 'js', 'typescript', 'ts',
        'c', 'cpp', 'c++', 'csharp', 'cs', 'ruby', 'rb', 'php', 'kotlin', 'swift',
        'r', 'matlab', 'shell', 'bash', 'sh', 'powershell', 'ps1',
        # 数据格式
        'json', 'yaml', 'yml', 'xml', 'toml', 'sql', 'csv',
        # 配置和标记
        'dockerfile', 'makefile', 'regex', 'http', 'diff', 'git',
        # 特殊（Mermaid）
        'mermaid', 'mmd',
    }
    
    # 需要特定语言的代码块（避免无高亮）
    CODE_BLOCKS_NEED_LANG = re.compile(
        r'^```\s*$', 
        re.MULTILINE
    )
    
    # 代码块匹配
    CODE_BLOCK_PATTERN = re.compile(
        r'^```(\w*)\s*\n(.*?)^```\s*$',
        re.MULTILINE | re.DOTALL
    )
    
    # 表格行匹配
    TABLE_ROW_PATTERN = re.compile(r'^\|.*\|$', re.MULTILINE)
    
    # 标题匹配
    HEADER_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    
    # 列表项匹配
    LIST_ITEM_PATTERN = re.compile(
        r'^(\s*)([-*+]|\d+\.)\s+(.+)$',
        re.MULTILINE
    )
    
    # 中英文标点检查（混合使用检测）
    MIXED_PUNCTUATION = re.compile(
        r'[\u4e00-\u9fff][.,!?;:]'  # 中文后跟英文标点
        r'|'                        # 或
        r'[.,!?;:][\u4e00-\u9fff]'  # 英文标点后跟中文
    )
    
    # 行尾空格
    TRAILING_WHITESPACE = re.compile(r' +$')
    
    # Tab字符
    TAB_CHARACTER = re.compile(r'\t')
    
    # 连续空行（超过3行）
    MULTIPLE_BLANK_LINES = re.compile(r'\n{4,}')
    
    # 内联代码中的空格
    INLINE_CODE_PATTERN = re.compile(r'`([^`]+)`')
    
    def __init__(self, config: Optional[Dict] = None):
        """初始化格式检查器"""
        self.config = config or {}
        self.results: List[ValidationResult] = []
        
        # 从配置加载规则
        self.check_code_blocks = self.config.get('check_code_blocks', True)
        self.check_tables = self.config.get('check_tables', True)
        self.check_lists = self.config.get('check_lists', True)
        self.check_headers = self.config.get('check_headers', True)
        self.check_punctuation = self.config.get('check_punctuation', False)
        self.check_whitespace = self.config.get('check_whitespace', True)
        self.max_line_length = self.config.get('max_line_length', 120)
        
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
        
        # 逐行检查
        if self.check_whitespace:
            self._check_whitespace(lines, result)
        
        # 代码块检查
        if self.check_code_blocks:
            self._check_code_blocks(content, lines, result)
        
        # 表格检查
        if self.check_tables:
            self._check_tables(content, lines, result)
        
        # 列表检查
        if self.check_lists:
            self._check_lists(content, lines, result)
        
        # 标题层级检查
        if self.check_headers:
            self._check_headers(content, lines, result)
        
        # 标点检查
        if self.check_punctuation:
            self._check_punctuation(content, lines, result)
        
        # 行长度检查
        self._check_line_length(lines, result)
        
        return result
    
    def _check_whitespace(self, lines: List[str], result: ValidationResult):
        """检查空格和格式问题"""
        for line_num, line in enumerate(lines, 1):
            # 行尾空格
            if self.TRAILING_WHITESPACE.search(line):
                result.add_issue(
                    line=line_num,
                    severity=Severity.WARNING,
                    code="SPACE-001",
                    message="行尾存在多余空格",
                    suggestion="删除行尾空格"
                )
            
            # Tab字符（应使用空格）
            if self.TAB_CHARACTER.search(line):
                result.add_issue(
                    line=line_num,
                    severity=Severity.WARNING,
                    code="SPACE-002",
                    message="使用Tab字符缩进",
                    suggestion="将Tab替换为4个空格"
                )
        
        # 连续空行
        content = '\n'.join(lines)
        for match in self.MULTIPLE_BLANK_LINES.finditer(content):
            result.add_issue(
                line=content[:match.start()].count('\n') + 1,
                severity=Severity.INFO,
                code="SPACE-003",
                message="存在超过3行的连续空行",
                suggestion="最多保留2-3行空行"
            )
    
    def _check_code_blocks(self, content: str, lines: List[str], 
                           result: ValidationResult):
        """检查代码块格式"""
        # 查找所有代码块
        code_block_starts = list(re.finditer(r'^```(\w*)\s*$', content, re.MULTILINE))
        
        # 检查未闭合的代码块
        if len(code_block_starts) % 2 != 0:
            # 找到未匹配的开启标签
            result.add_issue(
                line=self._find_line_number(content, code_block_starts[-1].start(), lines),
                severity=Severity.ERROR,
                code="CODE-001",
                message="代码块未正确闭合",
                suggestion="添加 ``` 闭合代码块"
            )
        
        # 检查代码块语言
        for i, match in enumerate(code_block_starts):
            if i % 2 == 0:  # 只检查开启标签
                lang = match.group(1).lower()
                line_num = self._find_line_number(content, match.start(), lines)
                
                if not lang:
                    # 检查是否是文本块（可以无语言）
                    # 获取代码块内容
                    if i + 1 < len(code_block_starts):
                        block_end = code_block_starts[i + 1].start()
                        block_content = content[match.end():block_end]
                        
                        # 如果内容看起来像代码，建议添加语言
                        if self._looks_like_code(block_content):
                            result.add_issue(
                                line=line_num,
                                severity=Severity.WARNING,
                                code="CODE-002",
                                message="代码块缺少语言标识",
                                suggestion=f"建议使用: {self._suggest_language(block_content)}"
                            )
                elif lang not in self.SUPPORTED_LANGUAGES:
                    # 检查是否是支持的语言
                    result.add_issue(
                        line=line_num,
                        severity=Severity.INFO,
                        code="CODE-003",
                        message=f"未知的代码块语言: '{lang}'",
                        suggestion=f"使用标准语言标识，如: python, java, scala, mermaid"
                    )
                
                # 检查Mermaid代码块语法
                if lang in ('mermaid', 'mmd'):
                    self._check_mermaid_syntax(
                        content[match.end():code_block_starts[i+1].start() if i+1 < len(code_block_starts) else len(content)],
                        line_num,
                        result
                    )
    
    def _looks_like_code(self, content: str) -> bool:
        """判断内容是否像代码"""
        code_indicators = [
            r'^(def|class|function|const|let|var|import|from|package)\s',
            r'[{};]$',
            r'^(if|for|while|return|try|catch)\s',
            r'^(SELECT|INSERT|UPDATE|DELETE)\s',
        ]
        lines = content.strip().split('\n')
        if not lines:
            return False
        
        code_like_count = 0
        for line in lines[:10]:  # 检查前10行
            for pattern in code_indicators:
                if re.search(pattern, line, re.IGNORECASE):
                    code_like_count += 1
                    break
        
        return code_like_count >= 2 or len(lines) > 5
    
    def _suggest_language(self, content: str) -> str:
        """根据内容建议语言"""
        content_lower = content.lower()
        
        if re.search(r'^(def|class|import|from)\s', content, re.MULTILINE):
            return "python"
        elif re.search(r'^(public\s+class|private|protected)', content, re.MULTILINE):
            return "java"
        elif re.search(r'^(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP)\s', content, re.MULTILINE | re.IGNORECASE):
            return "sql"
        elif re.search(r'^(function|const|let|var)\s', content, re.MULTILINE):
            return "javascript"
        elif 'graph' in content_lower or 'flowchart' in content_lower or 'sequenceDiagram' in content:
            return "mermaid"
        elif re.search(r'^\s*[{\[]', content):
            return "json"
        
        return "text 或其他适合的语言"
    
    def _check_mermaid_syntax(self, content: str, start_line: int, 
                              result: ValidationResult):
        """检查Mermaid图表语法"""
        content_stripped = content.strip()
        
        # 检查图表类型
        valid_types = ['graph', 'flowchart', 'sequenceDiagram', 'classDiagram', 
                      'stateDiagram', 'gantt', 'pie', 'erDiagram', 'journey',
                      'gitGraph', 'mindmap', 'timeline', 'quadrantChart']
        
        first_line = content_stripped.split('\n')[0] if content_stripped else ""
        
        if not any(first_line.startswith(t) for t in valid_types):
            result.add_issue(
                line=start_line,
                severity=Severity.WARNING,
                code="MERMAID-001",
                message=f"Mermaid图表类型可能不正确: '{first_line[:30]}...'",
                suggestion=f"使用有效的图表类型: {', '.join(valid_types[:5])}..."
            )
        
        # 检查常见语法错误
        if '-->' in content and not re.search(r'\w+\s*-->', content):
            result.add_issue(
                line=start_line,
                severity=Severity.INFO,
                code="MERMAID-002",
                message="Mermaid箭头语法可能有问题",
                suggestion="确保节点名称后有箭头: A --> B"
            )
    
    def _check_tables(self, content: str, lines: List[str], 
                      result: ValidationResult):
        """检查表格格式"""
        table_rows = list(self.TABLE_ROW_PATTERN.finditer(content))
        
        if not table_rows:
            return
        
        # 分组连续的行作为表格
        tables = []
        current_table = [table_rows[0]]
        
        for i in range(1, len(table_rows)):
            prev_end = table_rows[i-1].end()
            curr_start = table_rows[i].start()
            
            # 检查是否连续（中间只有空白或空行）
            between = content[prev_end:curr_start]
            if '\n' in between and all(c in ' \n' for c in between):
                current_table.append(table_rows[i])
            else:
                tables.append(current_table)
                current_table = [table_rows[i]]
        
        if current_table:
            tables.append(current_table)
        
        # 检查每个表格
        for table in tables:
            if len(table) < 2:
                continue  # 不是有效表格
            
            # 获取列数
            first_row_cols = table[0].group().count('|') - 1
            
            # 检查分隔行（第二行应该是 ---|---|--- 格式）
            if len(table) >= 2:
                separator = table[1].group()
                if not re.match(r'^\|[-:|\s]+\|$', separator):
                    result.add_issue(
                        line=self._find_line_number(content, table[1].start(), lines),
                        severity=Severity.ERROR,
                        code="TABLE-001",
                        message="表格缺少正确的分隔行",
                        suggestion="添加分隔行: |---|---|"
                    )
            
            # 检查列数一致性
            for row_match in table:
                row_cols = row_match.group().count('|') - 1
                if row_cols != first_row_cols:
                    result.add_issue(
                        line=self._find_line_number(content, row_match.start(), lines),
                        severity=Severity.ERROR,
                        code="TABLE-002",
                        message=f"表格列数不一致: 期望 {first_row_cols}, 实际 {row_cols}",
                        suggestion="确保每行的 | 数量一致"
                    )
    
    def _check_lists(self, content: str, lines: List[str], 
                     result: ValidationResult):
        """检查列表格式"""
        list_items = list(self.LIST_ITEM_PATTERN.finditer(content))
        
        if not list_items:
            return
        
        # 检查缩进一致性
        prev_indent = None
        prev_is_ordered = None
        
        for match in list_items:
            indent = len(match.group(1))
            marker = match.group(2)
            is_ordered = marker[0].isdigit()
            line_num = self._find_line_number(content, match.start(), lines)
            
            # 检查混合列表类型
            if prev_is_ordered is not None and is_ordered != prev_is_ordered:
                if indent == prev_indent:
                    result.add_issue(
                        line=line_num,
                        severity=Severity.WARNING,
                        code="LIST-001",
                        message="同级列表混合使用有序和无序列表",
                        suggestion="保持列表类型一致，或使用不同缩进级别"
                    )
            
            # 检查缩进增量
            if prev_indent is not None and indent > prev_indent:
                if (indent - prev_indent) % 2 != 0 and (indent - prev_indent) % 4 != 0:
                    result.add_issue(
                        line=line_num,
                        severity=Severity.INFO,
                        code="LIST-002",
                        message=f"列表缩进不标准: {indent} 空格",
                        suggestion="使用 2 或 4 空格的倍数缩进"
                    )
            
            prev_indent = indent
            prev_is_ordered = is_ordered
    
    def _check_headers(self, content: str, lines: List[str], 
                       result: ValidationResult):
        """检查标题层级"""
        headers = list(self.HEADER_PATTERN.finditer(content))
        
        if not headers:
            return
        
        prev_level = 0
        
        for match in headers:
            level = len(match.group(1))
            title = match.group(2)
            line_num = self._find_line_number(content, match.start(), lines)
            
            # 检查标题层级跳跃
            if level > prev_level + 1 and prev_level > 0:
                result.add_issue(
                    line=line_num,
                    severity=Severity.WARNING,
                    code="HEADER-001",
                    message=f"标题层级跳跃: H{prev_level} 后直接 H{level}",
                    suggestion=f"考虑添加 H{prev_level + 1} 标题"
                )
            
            # 检查标题末尾标点
            if title.rstrip()[-1] in '。，！？：；':
                result.add_issue(
                    line=line_num,
                    severity=Severity.INFO,
                    code="HEADER-002",
                    message="标题末尾包含标点符号",
                    suggestion="删除标题末尾的标点"
                )
            
            # 检查空标题
            if not title.strip():
                result.add_issue(
                    line=line_num,
                    severity=Severity.ERROR,
                    code="HEADER-003",
                    message="标题内容为空",
                    suggestion="添加标题内容"
                )
            
            prev_level = level
    
    def _check_punctuation(self, content: str, lines: List[str], 
                           result: ValidationResult):
        """检查中英文标点"""
        for match in self.MIXED_PUNCTUATION.finditer(content):
            line_num = self._find_line_number(content, match.start(), lines)
            result.add_issue(
                line=line_num,
                severity=Severity.INFO,
                code="PUNC-001",
                message=f"中英文标点混用: '{match.group()}'",
                suggestion="中文内容使用中文标点，英文内容使用英文标点"
            )
    
    def _check_line_length(self, lines: List[str], result: ValidationResult):
        """检查行长度"""
        for line_num, line in enumerate(lines, 1):
            # 排除表格行（通常较长）
            if line.strip().startswith('|') and line.strip().endswith('|'):
                continue
            
            # 排除代码块中的行
            # 这里简化处理，实际应跟踪代码块状态
            
            if len(line) > self.max_line_length:
                result.add_issue(
                    line=line_num,
                    severity=Severity.INFO,
                    code="LENGTH-001",
                    message=f"行长度超过 {self.max_line_length} 字符",
                    suggestion="考虑换行或简化内容"
                )
    
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
        
        # 排除某些目录
        exclude_patterns = ['.git', 'node_modules', '.venv', '__pycache__']
        md_files = [
            f for f in md_files 
            if not any(p in str(f) for p in exclude_patterns)
        ]
        
        print(f"找到 {len(md_files)} 个Markdown文件待检查...")
        
        for file_path in md_files:
            result = self.check_file(file_path)
            results.append(result)
        
        return results
    
    def print_report(self, results: List[ValidationResult], ci_mode: bool = False):
        """打印检查报告"""
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
            print(f"::group::Format Check Results")
            print(f"Total files: {total_files}")
            print(f"Passed: {passed_files}")
            print(f"Errors: {error_count}")
            print(f"Warnings: {warning_count}")
            
            for result in results:
                for issue in result.issues:
                    if issue.severity == Severity.ERROR:
                        print(f"::error file={issue.file},line={issue.line}::{issue.code}: {issue.message}")
                    elif issue.severity == Severity.WARNING:
                        print(f"::warning file={issue.file},line={issue.line}::{issue.code}: {issue.message}")
            print(f"::endgroup::")
        else:
            print("\n" + "=" * 80)
            print("格式检查报告")
            print("=" * 80)
            print(f"检查文件数: {total_files}")
            print(f"通过: {passed_files} | 失败: {total_files - passed_files}")
            print(f"问题总计: {total_issues} (错误: {error_count}, 警告: {warning_count})")
            print("=" * 80)
            
            failed_results = [r for r in results if not r.passed or r.issues]
            if failed_results:
                print("\n⚠️ 存在格式问题的文件:")
                for result in failed_results[:10]:  # 最多显示10个
                    issue_count = len([i for i in result.issues if i.severity == Severity.ERROR])
                    warning_count = len([i for i in result.issues if i.severity == Severity.WARNING])
                    print(f"\n📄 {result.file_path} (错误:{issue_count}, 警告:{warning_count})")
                    for issue in result.issues[:5]:  # 每文件最多显示5个问题
                        severity_icon = "🔴" if issue.severity == Severity.ERROR else "🟡" if issue.severity == Severity.WARNING else "🔵"
                        print(f"   {severity_icon} 行{issue.line}: [{issue.code}] {issue.message}")
                    if len(result.issues) > 5:
                        print(f"   ... 还有 {len(result.issues) - 5} 个问题")
                
                if len(failed_results) > 10:
                    print(f"\n... 还有 {len(failed_results) - 10} 个文件")
            
            print("\n" + "=" * 80)
            if error_count == 0:
                print("✅ 格式检查完成，无严重错误")
            else:
                print(f"❌ 发现 {error_count} 个格式错误")
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
        description="格式检查器 - 检查Markdown格式规范",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s document.md
  %(prog)s --config config.json docs/
  %(prog)s --ci .
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
        '--ci',
        action='store_true',
        help='CI模式：简洁输出，适合CI环境'
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
    
    # 创建检查器
    checker = FormatChecker(config)
    
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
    sys.exit(ExitCode.FORMAT_ERROR if has_errors else ExitCode.SUCCESS)


if __name__ == '__main__':
    main()
