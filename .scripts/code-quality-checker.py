#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码质量自动化检查脚本
=======================

检查项目代码的格式一致性、命名规范、注释完整性和异常处理。

用法:
    python code-quality-checker.py [options]

选项:
    --fix           自动修复可修复的问题
    --output        指定输出报告路径
    --format        指定报告格式 (json|markdown|html)
"""

import argparse
import ast
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from datetime import datetime


@dataclass
class QualityIssue:
    """代码质量问题"""
    file_path: str
    line_number: int
    issue_type: str
    severity: str  # error, warning, info
    message: str
    suggestion: str = ""


@dataclass
class FileQualityReport:
    """单个文件的质量报告"""
    file_path: str
    file_type: str  # python, yaml, sql, java
    total_lines: int = 0
    code_lines: int = 0
    comment_lines: int = 0
    blank_lines: int = 0
    issues: List[QualityIssue] = field(default_factory=list)
    score: float = 100.0


@dataclass
class QualitySummary:
    """质量汇总报告"""
    total_files: int = 0
    python_files: int = 0
    yaml_files: int = 0
    sql_files: int = 0
    java_files: int = 0
    total_issues: int = 0
    errors: int = 0
    warnings: int = 0
    infos: int = 0
    avg_score: float = 100.0
    files_with_issues: int = 0


class CodeQualityChecker:
    """代码质量检查器"""

    # PEP 8 命名规范正则
    SNAKE_CASE_PATTERN = re.compile(r'^[a-z][a-z0-9_]*$')
    CAMEL_CASE_PATTERN = re.compile(r'^[a-z][a-zA-Z0-9]*$')
    PASCAL_CASE_PATTERN = re.compile(r'^[A-Z][a-zA-Z0-9]*$')
    UPPER_SNAKE_CASE_PATTERN = re.compile(r'^[A-Z][A-Z0-9_]*$')

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.reports: List[FileQualityReport] = []
        self.summary = QualitySummary()

    def scan_project(self) -> List[Path]:
        """扫描项目中的所有代码文件"""
        files = []
        
        # Python文件
        files.extend(self.project_root.rglob("*.py"))
        
        # YAML文件
        files.extend(self.project_root.rglob("*.yml"))
        files.extend(self.project_root.rglob("*.yaml"))
        
        # SQL文件
        files.extend(self.project_root.rglob("*.sql"))
        
        # Java文件
        files.extend(self.project_root.rglob("*.java"))
        
        # 排除特定目录
        exclude_dirs = {'.git', '.github', 'node_modules', '__pycache__', 
                       '.vscode', '.idea', 'venv', '.venv', 'env'}
        
        filtered_files = [
            f for f in files 
            if not any(excluded in f.parts for excluded in exclude_dirs)
        ]
        
        return sorted(filtered_files)

    def check_python_file(self, file_path: Path) -> FileQualityReport:
        """检查Python文件质量"""
        report = FileQualityReport(
            file_path=str(file_path),
            file_type="python"
        )

        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            report.total_lines = len(lines)
            
            # 统计行数
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    report.blank_lines += 1
                elif stripped.startswith('#'):
                    report.comment_lines += 1
                else:
                    report.code_lines += 1

            # 解析AST
            try:
                tree = ast.parse(content)
            except SyntaxError as e:
                report.issues.append(QualityIssue(
                    file_path=str(file_path),
                    line_number=e.lineno or 1,
                    issue_type="syntax_error",
                    severity="error",
                    message=f"语法错误: {e.msg}",
                    suggestion="修复语法错误"
                ))
                return report

            # 检查文件头
            self._check_python_header(content, file_path, report)
            
            # 检查导入排序
            self._check_import_order(tree, file_path, report)
            
            # 检查命名规范
            self._check_naming_conventions(tree, file_path, report)
            
            # 检查类型提示
            self._check_type_hints(tree, file_path, report)
            
            # 检查文档字符串
            self._check_docstrings(tree, file_path, report)
            
            # 检查异常处理
            self._check_exception_handling(tree, file_path, report)
            
            # 检查代码复杂度
            self._check_complexity(tree, file_path, report)

        except Exception as e:
            report.issues.append(QualityIssue(
                file_path=str(file_path),
                line_number=1,
                issue_type="read_error",
                severity="error",
                message=f"读取文件失败: {str(e)}",
                suggestion="检查文件权限和编码"
            ))

        # 计算分数
        self._calculate_score(report)
        return report

    def _check_python_header(self, content: str, file_path: Path, report: FileQualityReport):
        """检查Python文件头"""
        lines = content.split('\n')[:3]
        
        # 检查shebang
        if not any('#!/usr/bin/env python' in line for line in lines):
            report.issues.append(QualityIssue(
                file_path=str(file_path),
                line_number=1,
                issue_type="missing_shebang",
                severity="info",
                message="缺少shebang (#!/usr/bin/env python3)",
                suggestion="在文件第一行添加shebang"
            ))
        
        # 检查编码声明
        if not any('# -*- coding: utf-8 -*-' in line for line in lines):
            report.issues.append(QualityIssue(
                file_path=str(file_path),
                line_number=1,
                issue_type="missing_encoding",
                severity="info",
                message="缺少编码声明 (# -*- coding: utf-8 -*-)",
                suggestion="在shebang后添加编码声明"
            ))

    def _check_import_order(self, tree: ast.AST, file_path: Path, report: FileQualityReport):
        """检查导入排序"""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append((node.lineno, alias.name))
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                imports.append((node.lineno, module))

        # 简单检查：标准库导入应该在第三方库之前
        stdlib_modules = {'os', 'sys', 'json', 're', 'pathlib', 'typing', 'datetime', 
                         'collections', 'itertools', 'functools', 'dataclasses'}
        
        prev_is_stdlib = None
        for lineno, name in imports:
            is_stdlib = name.split('.')[0] in stdlib_modules
            if prev_is_stdlib is False and is_stdlib:
                report.issues.append(QualityIssue(
                    file_path=str(file_path),
                    line_number=lineno,
                    issue_type="import_order",
                    severity="warning",
                    message=f"导入顺序问题: {name}",
                    suggestion="标准库导入应该放在第三方库之前"
                ))
            prev_is_stdlib = is_stdlib

    def _check_naming_conventions(self, tree: ast.AST, file_path: Path, report: FileQualityReport):
        """检查命名规范"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # 函数名应该是snake_case
                if not self.SNAKE_CASE_PATTERN.match(node.name):
                    if not (node.name.startswith('__') and node.name.endswith('__')):
                        report.issues.append(QualityIssue(
                            file_path=str(file_path),
                            line_number=node.lineno,
                            issue_type="naming_convention",
                            severity="warning",
                            message=f"函数名 '{node.name}' 不符合snake_case规范",
                            suggestion="使用小写字母和下划线命名函数"
                        ))
            
            elif isinstance(node, ast.ClassDef):
                # 类名应该是PascalCase
                if not self.PASCAL_CASE_PATTERN.match(node.name):
                    report.issues.append(QualityIssue(
                        file_path=str(file_path),
                        line_number=node.lineno,
                        issue_type="naming_convention",
                        severity="warning",
                        message=f"类名 '{node.name}' 不符合PascalCase规范",
                        suggestion="使用首字母大写的驼峰命名法"
                    ))
            
            elif isinstance(node, ast.NameConstant):
                # 检查是否是全局常量
                pass  # 简化处理

    def _check_type_hints(self, tree: ast.AST, file_path: Path, report: FileQualityReport):
        """检查类型提示"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # 检查函数参数类型提示
                args_with_annotations = sum(
                    1 for arg in node.args.args 
                    if arg.annotation is not None
                )
                total_args = len(node.args.args)
                
                if total_args > 0 and args_with_annotations < total_args:
                    missing_args = total_args - args_with_annotations
                    # 排除self/cls
                    if missing_args > 1 or (missing_args == 1 and 
                        not any(arg.arg in ('self', 'cls') for arg in node.args.args 
                               if arg.annotation is None)):
                        report.issues.append(QualityIssue(
                            file_path=str(file_path),
                            line_number=node.lineno,
                            issue_type="missing_type_hints",
                            severity="info",
                            message=f"函数 '{node.name}' 缺少参数类型提示",
                            suggestion="为函数参数添加类型注解"
                        ))
                
                # 检查返回值类型提示
                if node.returns is None and node.name != '__init__':
                    report.issues.append(QualityIssue(
                        file_path=str(file_path),
                        line_number=node.lineno,
                        issue_type="missing_return_type",
                        severity="info",
                        message=f"函数 '{node.name}' 缺少返回值类型提示",
                        suggestion="为函数添加 -> 返回类型"
                    ))

    def _check_docstrings(self, tree: ast.AST, file_path: Path, report: FileQualityReport):
        """检查文档字符串"""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                docstring = ast.get_docstring(node)
                
                if docstring is None:
                    report.issues.append(QualityIssue(
                        file_path=str(file_path),
                        line_number=node.lineno,
                        issue_type="missing_docstring",
                        severity="info",
                        message=f"{node.__class__.__name__} '{node.name}' 缺少文档字符串",
                        suggestion="添加描述性的文档字符串"
                    ))
                elif len(docstring.strip()) < 10:
                    report.issues.append(QualityIssue(
                        file_path=str(file_path),
                        line_number=node.lineno,
                        issue_type="short_docstring",
                        severity="info",
                        message=f"'{node.name}' 的文档字符串过短",
                        suggestion="提供更详细的文档说明"
                    ))

    def _check_exception_handling(self, tree: ast.AST, file_path: Path, report: FileQualityReport):
        """检查异常处理"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                # 检查是否有空的except块
                for handler in node.handlers:
                    if handler.type is None:
                        report.issues.append(QualityIssue(
                            file_path=str(file_path),
                            line_number=handler.lineno,
                            issue_type="bare_except",
                            severity="warning",
                            message="使用裸except:捕获所有异常",
                            suggestion="指定具体的异常类型"
                        ))
                    
                    # 检查except块是否为空或只包含pass
                    if handler.body and len(handler.body) == 1:
                        if isinstance(handler.body[0], ast.Pass):
                            report.issues.append(QualityIssue(
                                file_path=str(file_path),
                                line_number=handler.lineno,
                                issue_type="empty_except",
                                severity="warning",
                                message="空的异常处理块",
                                suggestion="处理异常或记录日志"
                            ))

    def _check_complexity(self, tree: ast.AST, file_path: Path, report: FileQualityReport):
        """检查代码复杂度"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # 简单计算函数行数
                if hasattr(node, 'end_lineno') and node.end_lineno:
                    func_lines = node.end_lineno - node.lineno
                    if func_lines > 50:
                        report.issues.append(QualityIssue(
                            file_path=str(file_path),
                            line_number=node.lineno,
                            issue_type="high_complexity",
                            severity="warning",
                            message=f"函数 '{node.name}' 过长 ({func_lines}行)",
                            suggestion="考虑拆分函数"
                        ))

    def _calculate_score(self, report: FileQualityReport):
        """计算质量分数"""
        score = 100.0
        
        for issue in report.issues:
            if issue.severity == "error":
                score -= 10
            elif issue.severity == "warning":
                score -= 5
            elif issue.severity == "info":
                score -= 2
        
        report.score = max(0, score)

    def check_yaml_file(self, file_path: Path) -> FileQualityReport:
        """检查YAML文件质量"""
        report = FileQualityReport(
            file_path=str(file_path),
            file_type="yaml"
        )

        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            report.total_lines = len(lines)

            # 基本语法检查
            try:
                import yaml
                yaml.safe_load(content)
            except ImportError:
                pass  # 没有yaml库时跳过
            except yaml.YAMLError as e:
                report.issues.append(QualityIssue(
                    file_path=str(file_path),
                    line_number=1,
                    issue_type="yaml_syntax",
                    severity="error",
                    message=f"YAML语法错误: {str(e)}",
                    suggestion="检查YAML缩进和语法"
                ))

            # 检查缩进（应该是2个空格）
            for i, line in enumerate(lines, 1):
                if line.strip() and not line.startswith('#'):
                    leading_spaces = len(line) - len(line.lstrip())
                    if leading_spaces % 2 != 0 and leading_spaces > 0:
                        report.issues.append(QualityIssue(
                            file_path=str(file_path),
                            line_number=i,
                            issue_type="indentation",
                            severity="warning",
                            message=f"缩进应为2的倍数 (当前{leading_spaces}个空格)",
                            suggestion="使用2个空格作为缩进"
                        ))

            # 检查是否有注释说明
            has_comment = any(line.strip().startswith('#') for line in lines[:5])
            if not has_comment:
                report.issues.append(QualityIssue(
                    file_path=str(file_path),
                    line_number=1,
                    issue_type="missing_header_comment",
                    severity="info",
                    message="缺少文件头注释",
                    suggestion="在文件开头添加描述性注释"
                ))

        except Exception as e:
            report.issues.append(QualityIssue(
                file_path=str(file_path),
                line_number=1,
                issue_type="read_error",
                severity="error",
                message=f"读取文件失败: {str(e)}",
                suggestion="检查文件权限和编码"
            ))

        self._calculate_score(report)
        return report

    def check_sql_file(self, file_path: Path) -> FileQualityReport:
        """检查SQL文件质量"""
        report = FileQualityReport(
            file_path=str(file_path),
            file_type="sql"
        )

        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            report.total_lines = len(lines)

            # 检查是否有注释
            has_comment = any(
                line.strip().startswith(('--', '/*')) for line in lines[:10]
            )
            if not has_comment:
                report.issues.append(QualityIssue(
                    file_path=str(file_path),
                    line_number=1,
                    issue_type="missing_sql_comment",
                    severity="info",
                    message="SQL文件缺少注释说明",
                    suggestion="添加查询目的和参数说明"
                ))

            # 检查SELECT *
            if re.search(r'SELECT\s+\*', content, re.IGNORECASE):
                report.issues.append(QualityIssue(
                    file_path=str(file_path),
                    line_number=1,
                    issue_type="select_star",
                    severity="warning",
                    message="使用SELECT *",
                    suggestion="显式指定需要的列"
                ))

            # 检查缺少WHERE的DELETE/UPDATE
            for match in re.finditer(
                r'(DELETE\s+FROM|UPDATE)\s+\w+\s*(?!WHERE)', 
                content, 
                re.IGNORECASE
            ):
                report.issues.append(QualityIssue(
                    file_path=str(file_path),
                    line_number=content[:match.start()].count('\n') + 1,
                    issue_type="missing_where",
                    severity="error",
                    message="DELETE/UPDATE语句缺少WHERE条件",
                    suggestion="添加WHERE条件以防止意外操作"
                ))

        except Exception as e:
            report.issues.append(QualityIssue(
                file_path=str(file_path),
                line_number=1,
                issue_type="read_error",
                severity="error",
                message=f"读取文件失败: {str(e)}",
                suggestion="检查文件权限和编码"
            ))

        self._calculate_score(report)
        return report

    def run_checks(self) -> Tuple[List[FileQualityReport], QualitySummary]:
        """运行所有检查"""
        files = self.scan_project()
        
        print(f"扫描到 {len(files)} 个代码文件")
        print("=" * 60)

        for i, file_path in enumerate(files, 1):
            suffix = file_path.suffix.lower()
            
            if suffix == '.py':
                report = self.check_python_file(file_path)
                self.summary.python_files += 1
            elif suffix in ('.yml', '.yaml'):
                report = self.check_yaml_file(file_path)
                self.summary.yaml_files += 1
            elif suffix == '.sql':
                report = self.check_sql_file(file_path)
                self.summary.sql_files += 1
            else:
                continue

            self.reports.append(report)
            self.summary.total_files += 1
            
            if report.issues:
                self.summary.files_with_issues += 1
                self.summary.total_issues += len(report.issues)
                
                for issue in report.issues:
                    if issue.severity == "error":
                        self.summary.errors += 1
                    elif issue.severity == "warning":
                        self.summary.warnings += 1
                    else:
                        self.summary.infos += 1

            print(f"[{i}/{len(files)}] {file_path} - 分数: {report.score:.1f}")

        # 计算平均分
        if self.reports:
            self.summary.avg_score = sum(r.score for r in self.reports) / len(self.reports)

        return self.reports, self.summary

    def generate_markdown_report(self, output_path: str):
        """生成Markdown格式的报告"""
        lines = [
            "# 代码质量检查报告\n",
            f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            "\n## 汇总统计\n",
            f"- **总文件数**: {self.summary.total_files}\n",
            f"- **Python文件**: {self.summary.python_files}\n",
            f"- **YAML文件**: {self.summary.yaml_files}\n",
            f"- **SQL文件**: {self.summary.sql_files}\n",
            f"- **问题文件数**: {self.summary.files_with_issues}\n",
            f"- **平均分数**: {self.summary.avg_score:.1f}/100\n",
            "\n## 问题统计\n",
            f"- **错误**: {self.summary.errors}\n",
            f"- **警告**: {self.summary.warnings}\n",
            f"- **建议**: {self.summary.infos}\n",
            f"- **总计**: {self.summary.total_issues}\n",
            "\n## 详细结果\n",
        ]

        # 按分数排序
        sorted_reports = sorted(self.reports, key=lambda r: r.score)
        
        for report in sorted_reports:
            status = "✅" if report.score >= 90 else "⚠️" if report.score >= 70 else "❌"
            lines.append(f"\n### {status} {report.file_path}\n")
            lines.append(f"- **文件类型**: {report.file_type}\n")
            lines.append(f"- **总行数**: {report.total_lines}\n")
            lines.append(f"- **代码行**: {report.code_lines}\n")
            lines.append(f"- **注释行**: {report.comment_lines}\n")
            lines.append(f"- **质量分数**: {report.score:.1f}/100\n")
            
            if report.issues:
                lines.append("\n**问题列表**:\n")
                for issue in report.issues:
                    severity_emoji = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}
                    emoji = severity_emoji.get(issue.severity, "•")
                    lines.append(f"- {emoji} **{issue.issue_type}** (第{issue.line_number}行): {issue.message}\n")
                    if issue.suggestion:
                        lines.append(f"  - 建议: {issue.suggestion}\n")

        # 添加改进建议
        lines.extend([
            "\n## 改进建议\n",
            "\n### 高优先级\n",
        ])
        
        if self.summary.errors > 0:
            lines.append(f"1. 修复 {self.summary.errors} 个错误级别问题\n")
        if self.summary.warnings > 0:
            lines.append(f"2. 处理 {self.summary.warnings} 个警告级别问题\n")
        
        lines.extend([
            "\n### 代码风格\n",
            "1. 确保所有Python文件包含shebang和编码声明\n",
            "2. 为所有公共函数和类添加文档字符串\n",
            "3. 使用类型提示提高代码可读性\n",
            "4. 遵循PEP 8命名规范\n",
            "\n### 配置文件\n",
            "1. YAML文件使用2个空格缩进\n",
            "2. 添加描述性注释说明配置用途\n",
            "3. SQL文件显式指定查询列\n",
        ])

        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        print(f"\n报告已保存到: {output_path}")

    def generate_json_report(self, output_path: str):
        """生成JSON格式的报告"""
        data = {
            "summary": asdict(self.summary),
            "reports": [
                {
                    **asdict(report),
                    "issues": [asdict(issue) for issue in report.issues]
                }
                for report in self.reports
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"JSON报告已保存到: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="代码质量自动化检查工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python code-quality-checker.py
  python code-quality-checker.py --format markdown --output report.md
  python code-quality-checker.py --format json --output report.json
        """
    )
    
    parser.add_argument(
        "--output", "-o",
        default="code-quality-report.md",
        help="输出报告路径 (默认: code-quality-report.md)"
    )
    
    parser.add_argument(
        "--format", "-f",
        choices=["markdown", "json"],
        default="markdown",
        help="报告格式 (默认: markdown)"
    )
    
    parser.add_argument(
        "--project-root", "-p",
        default=".",
        help="项目根目录 (默认: 当前目录)"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("代码质量检查工具")
    print("=" * 60)

    checker = CodeQualityChecker(args.project_root)
    reports, summary = checker.run_checks()

    print("\n" + "=" * 60)
    print("检查完成")
    print(f"总文件数: {summary.total_files}")
    print(f"问题文件: {summary.files_with_issues}")
    print(f"错误: {summary.errors}, 警告: {summary.warnings}, 建议: {summary.infos}")
    print(f"平均质量分数: {summary.avg_score:.1f}/100")
    print("=" * 60)

    # 生成报告
    if args.format == "json":
        checker.generate_json_report(args.output)
    else:
        checker.generate_markdown_report(args.output)

    return 0 if summary.errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
