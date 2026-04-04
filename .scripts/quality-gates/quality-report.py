#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
质量报告生成器 (Quality Report Generator)

功能：
    - 整合所有质量门禁的检查结果
    - 生成综合质量评分
    - 分类汇总问题
    - 提供修复建议
    - 支持多种输出格式（JSON、Markdown、HTML）
    - CI/CD集成支持

使用方式：
    python quality-report.py [检查结果文件...]
    python quality-report.py --run-all [项目目录]
    python quality-report.py --format markdown --output report.md

退出码：
    0 - 质量检查通过
    1 - 发现质量问题
"""

import re
import sys
import json
import subprocess
import argparse
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Set, Optional, Tuple, Any
from enum import IntEnum
from datetime import datetime
from collections import defaultdict


class ExitCode(IntEnum):
    """退出码定义"""
    SUCCESS = 0
    QUALITY_ERROR = 1
    CONFIG_ERROR = 2


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
    category: str = ""  # 问题分类


@dataclass
class CheckResult:
    """单个检查工具的结果"""
    tool: str
    file_path: str
    passed: bool
    issues: List[Issue] = field(default_factory=list)
    metrics: Dict = field(default_factory=dict)


@dataclass
class QualityReport:
    """综合质量报告"""
    timestamp: str
    project_path: str
    results: List[CheckResult] = field(default_factory=list)
    summary: Dict = field(default_factory=dict)
    
    def add_result(self, result: CheckResult):
        self.results.append(result)


class QualityReportGenerator:
    """
    质量报告生成器
    
    功能：
    1. 运行所有质量门禁检查
    2. 整合检查结果
    3. 生成综合报告
    4. 提供修复建议
    """
    
    # 问题分类规则
    CATEGORY_RULES = {
        'structure': ['STRUCT', 'META', 'THEOREM', 'HEADER'],
        'format': ['SPACE', 'CODE', 'TABLE', 'LIST', 'PUNC', 'LENGTH'],
        'reference': ['REF', 'LINK', 'CITE', 'REG'],
        'content': ['COMPLETE', 'VIZ', 'TERM', 'QUALITY', 'CODE'],
        'file': ['FILE'],
    }
    
    # 严重程度权重
    SEVERITY_WEIGHTS = {
        Severity.ERROR: 10,
        Severity.WARNING: 5,
        Severity.INFO: 1,
    }
    
    def __init__(self, config: Optional[Dict] = None, 
                 root_dir: Optional[Path] = None):
        """初始化报告生成器"""
        self.config = config or {}
        self.root_dir = root_dir or Path.cwd()
        self.scripts_dir = Path(__file__).parent
        
        # 配置参数
        self.quality_threshold = self.config.get('quality_threshold', 70)
        self.max_errors = self.config.get('max_errors', 0)
        self.max_warnings = self.config.get('max_warnings', 100)
        
    def run_all_checks(self, target_path: Path) -> QualityReport:
        """
        运行所有质量检查
        
        执行顺序：
        1. structure-validator.py - 结构验证
        2. format-checker.py - 格式检查
        3. reference-validator.py - 引用验证
        4. content-quality-checker.py - 内容质量
        """
        report = QualityReport(
            timestamp=datetime.now().isoformat(),
            project_path=str(target_path)
        )
        
        tools = [
            ('structure-validator', '结构验证'),
            ('format-checker', '格式检查'),
            ('reference-validator', '引用验证'),
            ('content-quality-checker', '内容质量'),
        ]
        
        for tool_name, tool_desc in tools:
            print(f"\n{'='*60}")
            print(f"运行 {tool_desc}...")
            print('='*60)
            
            result = self._run_single_tool(tool_name, target_path)
            report.add_result(result)
        
        # 生成汇总
        report.summary = self._generate_summary(report.results)
        
        return report
    
    def _run_single_tool(self, tool_name: str, target_path: Path) -> CheckResult:
        """运行单个检查工具"""
        script_path = self.scripts_dir / f"{tool_name}.py"
        
        if not script_path.exists():
            return CheckResult(
                tool=tool_name,
                file_path=str(target_path),
                passed=False,
                issues=[Issue(
                    file=str(script_path),
                    line=0,
                    severity=Severity.ERROR,
                    code="TOOL-001",
                    message=f"检查工具不存在: {script_path}",
                    suggestion="确保所有质量门禁脚本已安装"
                )]
            )
        
        # 运行脚本并捕获输出
        output_file = self.root_dir / f".quality-{tool_name}.json"
        
        try:
            cmd = [
                sys.executable,
                str(script_path),
                str(target_path),
                '--output', str(output_file)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            # 读取输出文件
            if output_file.exists():
                with open(output_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                output_file.unlink()  # 删除临时文件
                
                return self._parse_tool_output(tool_name, data)
            else:
                return CheckResult(
                    tool=tool_name,
                    file_path=str(target_path),
                    passed=result.returncode == 0,
                    issues=[]
                )
                
        except subprocess.TimeoutExpired:
            return CheckResult(
                tool=tool_name,
                file_path=str(target_path),
                passed=False,
                issues=[Issue(
                    file=str(script_path),
                    line=0,
                    severity=Severity.ERROR,
                    code="TOOL-002",
                    message=f"检查工具超时: {tool_name}",
                    suggestion="检查文件数量或增加超时时间"
                )]
            )
        except Exception as e:
            return CheckResult(
                tool=tool_name,
                file_path=str(target_path),
                passed=False,
                issues=[Issue(
                    file=str(script_path),
                    line=0,
                    severity=Severity.ERROR,
                    code="TOOL-003",
                    message=f"运行检查工具失败: {e}",
                    suggestion="检查Python环境和依赖"
                )]
            )
    
    def _parse_tool_output(self, tool_name: str, data: Dict) -> CheckResult:
        """解析工具输出"""
        issues = []
        
        for result_data in data.get('results', []):
            for issue_data in result_data.get('issues', []):
                severity = Severity[issue_data.get('severity', 'WARNING')]
                issue = Issue(
                    file=result_data.get('file', ''),
                    line=issue_data.get('line', 0),
                    severity=severity,
                    code=issue_data.get('code', 'UNKNOWN'),
                    message=issue_data.get('message', ''),
                    suggestion=issue_data.get('suggestion', ''),
                    category=self._categorize_issue(issue_data.get('code', ''))
                )
                issues.append(issue)
        
        return CheckResult(
            tool=tool_name,
            file_path=data.get('results', [{}])[0].get('file', '') if data.get('results') else '',
            passed=all(r.get('passed', True) for r in data.get('results', [])),
            issues=issues,
            metrics=data.get('summary', {})
        )
    
    def _categorize_issue(self, code: str) -> str:
        """根据问题代码分类"""
        code_prefix = code.split('-')[0] if '-' in code else code
        
        for category, prefixes in self.CATEGORY_RULES.items():
            if code_prefix in prefixes:
                return category
        
        return 'other'
    
    def _generate_summary(self, results: List[CheckResult]) -> Dict:
        """生成汇总统计"""
        summary = {
            'total_tools': len(results),
            'passed_tools': sum(1 for r in results if r.passed),
            'total_issues': sum(len(r.issues) for r in results),
            'error_count': sum(
                1 for r in results for i in r.issues if i.severity == Severity.ERROR
            ),
            'warning_count': sum(
                1 for r in results for i in r.issues if i.severity == Severity.WARNING
            ),
            'info_count': sum(
                1 for r in results for i in r.issues if i.severity == Severity.INFO
            ),
            'by_category': defaultdict(lambda: {'error': 0, 'warning': 0, 'info': 0}),
            'by_tool': {},
            'quality_score': 0,
        }
        
        # 按分类统计
        for result in results:
            tool_stats = {'error': 0, 'warning': 0, 'info': 0, 'passed': result.passed}
            
            for issue in result.issues:
                severity_name = issue.severity.name.lower()
                summary['by_category'][issue.category][severity_name] += 1
                tool_stats[severity_name] += 1
            
            summary['by_tool'][result.tool] = tool_stats
        
        # 计算质量分数
        base_score = 100
        for result in results:
            for issue in result.issues:
                weight = self.SEVERITY_WEIGHTS.get(issue.severity, 1)
                base_score -= weight
        
        summary['quality_score'] = max(0, base_score)
        summary['passed'] = (
            summary['error_count'] <= self.max_errors and
            summary['warning_count'] <= self.max_warnings and
            summary['quality_score'] >= self.quality_threshold
        )
        
        return dict(summary)
    
    def generate_markdown_report(self, report: QualityReport) -> str:
        """生成Markdown格式报告"""
        lines = []
        
        # 标题
        lines.append("# 文档质量检查报告")
        lines.append("")
        lines.append(f"**生成时间**: {report.timestamp}")
        lines.append(f"**项目路径**: {report.project_path}")
        lines.append("")
        
        # 汇总
        summary = report.summary
        lines.append("## 📊 质量概览")
        lines.append("")
        
        # 质量徽章
        if summary.get('passed'):
            lines.append("![质量状态](https://img.shields.io/badge/质量检查-通过-brightgreen)")
        else:
            lines.append("![质量状态](https://img.shields.io/badge/质量检查-失败-red)")
        lines.append(f"![质量分数](https://img.shields.io/badge/质量分数-{summary.get('quality_score', 0):.0f}/100-blue)")
        lines.append("")
        
        # 统计表格
        lines.append("| 指标 | 数值 |")
        lines.append("|------|------|")
        lines.append(f"| 检查工具 | {summary.get('total_tools', 0)} 个 |")
        lines.append(f"| 通过 | {summary.get('passed_tools', 0)} 个 |")
        lines.append(f"| 问题总计 | {summary.get('total_issues', 0)} 个 |")
        lines.append(f"| 🔴 错误 | {summary.get('error_count', 0)} 个 |")
        lines.append(f"| 🟡 警告 | {summary.get('warning_count', 0)} 个 |")
        lines.append(f"| 🔵 信息 | {summary.get('info_count', 0)} 个 |")
        lines.append("")
        
        # 按分类统计
        lines.append("### 问题分类")
        lines.append("")
        lines.append("| 分类 | 错误 | 警告 | 信息 |")
        lines.append("|------|------|------|------|")
        
        category_names = {
            'structure': '结构',
            'format': '格式',
            'reference': '引用',
            'content': '内容',
            'file': '文件',
            'other': '其他'
        }
        
        for category, stats in summary.get('by_category', {}).items():
            name = category_names.get(category, category)
            lines.append(f"| {name} | {stats.get('error', 0)} | {stats.get('warning', 0)} | {stats.get('info', 0)} |")
        
        lines.append("")
        
        # 各工具详细结果
        lines.append("## 🔍 详细结果")
        lines.append("")
        
        for result in report.results:
            tool_name = result.tool.replace('-', ' ').title()
            status = "✅ 通过" if result.passed else "❌ 失败"
            
            lines.append(f"### {tool_name} - {status}")
            lines.append("")
            
            # 工具指标
            if result.metrics:
                lines.append("**指标**:")
                for key, value in result.metrics.items():
                    lines.append(f"- {key}: {value}")
                lines.append("")
            
            # 问题列表
            if result.issues:
                lines.append("**发现问题**:")
                lines.append("")
                
                # 按严重程度分组
                errors = [i for i in result.issues if i.severity == Severity.ERROR]
                warnings = [i for i in result.issues if i.severity == Severity.WARNING]
                
                if errors:
                    lines.append("🔴 **错误**:")
                    for issue in errors[:10]:
                        lines.append(f"- `{issue.code}` 行{issue.line}: {issue.message}")
                        if issue.suggestion:
                            lines.append(f"  - 💡 {issue.suggestion}")
                    if len(errors) > 10:
                        lines.append(f"- ... 还有 {len(errors) - 10} 个错误")
                    lines.append("")
                
                if warnings:
                    lines.append("🟡 **警告**:")
                    for issue in warnings[:10]:
                        lines.append(f"- `{issue.code}` 行{issue.line}: {issue.message}")
                    if len(warnings) > 10:
                        lines.append(f"- ... 还有 {len(warnings) - 10} 个警告")
                    lines.append("")
        
        # 修复建议
        lines.append("## 💡 修复建议")
        lines.append("")
        
        # 按分类汇总建议
        category_suggestions = self._generate_suggestions(report)
        for category, suggestions in category_suggestions.items():
            if suggestions:
                lines.append(f"### {category_names.get(category, category)}")
                lines.append("")
                for suggestion in suggestions[:5]:
                    lines.append(f"- {suggestion}")
                lines.append("")
        
        return '\n'.join(lines)
    
    def _generate_suggestions(self, report: QualityReport) -> Dict[str, List[str]]:
        """生成修复建议"""
        suggestions = defaultdict(list)
        
        for result in report.results:
            for issue in result.issues:
                if issue.severity == Severity.ERROR and issue.suggestion:
                    suggestions[issue.category].append(issue.suggestion)
        
        # 去重
        for category in suggestions:
            suggestions[category] = list(set(suggestions[category]))
        
        return dict(suggestions)
    
    def generate_html_report(self, report: QualityReport) -> str:
        """生成HTML格式报告"""
        summary = report.summary
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文档质量检查报告</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            margin: 0 0 10px 0;
            color: #333;
        }}
        .meta {{
            color: #666;
            font-size: 14px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stat-card .number {{
            font-size: 36px;
            font-weight: bold;
            margin: 10px 0;
        }}
        .stat-card .label {{
            color: #666;
            font-size: 14px;
        }}
        .stat-card.error {{ border-top: 4px solid #dc3545; }}
        .stat-card.warning {{ border-top: 4px solid #ffc107; }}
        .stat-card.success {{ border-top: 4px solid #28a745; }}
        .stat-card.info {{ border-top: 4px solid #17a2b8; }}
        .stat-card.error .number {{ color: #dc3545; }}
        .stat-card.warning .number {{ color: #ffc107; }}
        .stat-card.success .number {{ color: #28a745; }}
        .stat-card.info .number {{ color: #17a2b8; }}
        .section {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            margin-top: 0;
            color: #333;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}
        th {{
            background: #f8f9fa;
            font-weight: 600;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }}
        .badge-error {{ background: #dc3545; color: white; }}
        .badge-warning {{ background: #ffc107; color: #333; }}
        .badge-info {{ background: #17a2b8; color: white; }}
        .badge-success {{ background: #28a745; color: white; }}
        .tool-result {{
            margin-bottom: 20px;
            padding: 15px;
            border-radius: 6px;
            background: #f8f9fa;
        }}
        .tool-result.passed {{ border-left: 4px solid #28a745; }}
        .tool-result.failed {{ border-left: 4px solid #dc3545; }}
        .tool-name {{
            font-weight: 600;
            margin-bottom: 10px;
        }}
        .issue-list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        .issue-item {{
            padding: 8px;
            margin: 5px 0;
            border-radius: 4px;
            font-size: 14px;
        }}
        .issue-error {{ background: #f8d7da; }}
        .issue-warning {{ background: #fff3cd; }}
        .issue-info {{ background: #d1ecf1; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📋 文档质量检查报告</h1>
        <div class="meta">
            生成时间: {report.timestamp}<br>
            项目路径: {report.project_path}
        </div>
    </div>
    
    <div class="summary">
        <div class="stat-card {'success' if summary.get('passed') else 'error'}">
            <div class="label">质量状态</div>
            <div class="number">{'✓' if summary.get('passed') else '✗'}</div>
        </div>
        <div class="stat-card info">
            <div class="label">质量分数</div>
            <div class="number">{summary.get('quality_score', 0):.0f}</div>
        </div>
        <div class="stat-card error">
            <div class="label">错误</div>
            <div class="number">{summary.get('error_count', 0)}</div>
        </div>
        <div class="stat-card warning">
            <div class="label">警告</div>
            <div class="number">{summary.get('warning_count', 0)}</div>
        </div>
    </div>
"""
        
        # 添加详细结果
        html += """
    <div class="section">
        <h2>🔍 详细结果</h2>
"""
        
        for result in report.results:
            status_class = 'passed' if result.passed else 'failed'
            status_text = '✅ 通过' if result.passed else '❌ 失败'
            
            html += f"""
        <div class="tool-result {status_class}">
            <div class="tool-name">{result.tool.replace('-', ' ').title()} - {status_text}</div>
"""
            
            if result.issues:
                html += '<ul class="issue-list">'
                for issue in result.issues[:10]:
                    severity_class = f"issue-{issue.severity.name.lower()}"
                    html += f"""
                <li class="issue-item {severity_class}">
                    <span class="badge badge-{issue.severity.name.lower()}">{issue.severity.name}</span>
                    <code>{issue.code}</code> 行{issue.line}: {issue.message}
                </li>
"""
                if len(result.issues) > 10:
                    html += f'<li class="issue-item">... 还有 {len(result.issues) - 10} 个问题</li>'
                html += '</ul>'
            
            html += '</div>'
        
        html += """
    </div>
</body>
</html>
"""
        
        return html
    
    def print_console_report(self, report: QualityReport, ci_mode: bool = False):
        """打印控制台报告"""
        summary = report.summary
        
        if ci_mode:
            print(f"::group::Quality Report")
            print(f"Quality Score: {summary.get('quality_score', 0):.1f}")
            print(f"Errors: {summary.get('error_count', 0)}")
            print(f"Warnings: {summary.get('warning_count', 0)}")
            print(f"Passed: {summary.get('passed', False)}")
            
            for result in report.results:
                for issue in result.issues:
                    if issue.severity == Severity.ERROR:
                        print(f"::error file={issue.file},line={issue.line}::{issue.code}: {issue.message}")
            print(f"::endgroup::")
        else:
            print("\n" + "=" * 80)
            print("📋 文档质量检查报告")
            print("=" * 80)
            print(f"生成时间: {report.timestamp}")
            print(f"项目路径: {report.project_path}")
            print("-" * 80)
            
            # 质量状态
            if summary.get('passed'):
                print("✅ 质量检查通过")
            else:
                print("❌ 质量检查失败")
            
            print(f"\n质量分数: {summary.get('quality_score', 0):.1f}/100")
            print(f"检查工具: {summary.get('passed_tools', 0)}/{summary.get('total_tools', 0)} 通过")
            print(f"问题统计: 🔴 {summary.get('error_count', 0)} 错误, "
                  f"🟡 {summary.get('warning_count', 0)} 警告, "
                  f"🔵 {summary.get('info_count', 0)} 信息")
            
            # 按分类统计
            print("\n问题分类:")
            for category, stats in summary.get('by_category', {}).items():
                total = stats.get('error', 0) + stats.get('warning', 0) + stats.get('info', 0)
                if total > 0:
                    print(f"  - {category}: {stats.get('error', 0)} 错误, "
                          f"{stats.get('warning', 0)} 警告, {stats.get('info', 0)} 信息")
            
            print("\n" + "=" * 80)


def main():
    """主入口函数"""
    parser = argparse.ArgumentParser(
        description="质量报告生成器 - 整合所有质量门禁检查结果",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --run-all .
  %(prog)s --run-all . --format markdown --output report.md
  %(prog)s --run-all . --format html --output report.html
  %(prog)s .quality-*.json --format markdown
        """
    )
    
    parser.add_argument(
        'input',
        nargs='?',
        help='输入路径（项目目录或检查结果文件）'
    )
    parser.add_argument(
        '--run-all',
        action='store_true',
        help='运行所有检查工具'
    )
    parser.add_argument(
        '--format', '-f',
        choices=['json', 'markdown', 'html'],
        default='json',
        help='输出格式 (默认: json)'
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='输出文件路径'
    )
    parser.add_argument(
        '--ci',
        action='store_true',
        help='CI模式：简洁输出'
    )
    parser.add_argument(
        '--threshold', '-t',
        type=float,
        default=70,
        help='质量分数阈值 (默认: 70)'
    )
    
    args = parser.parse_args()
    
    if not args.input and not args.run_all:
        parser.print_help()
        sys.exit(ExitCode.CONFIG_ERROR)
    
    # 创建报告生成器
    config = {'quality_threshold': args.threshold}
    generator = QualityReportGenerator(config)
    
    # 生成报告
    if args.run_all:
        target_path = Path(args.input or '.')
        report = generator.run_all_checks(target_path)
    else:
        # 从现有检查结果加载
        print("从检查结果文件加载暂不支持，请使用 --run-all")
        sys.exit(ExitCode.CONFIG_ERROR)
    
    # 打印控制台报告
    generator.print_console_report(report, ci_mode=args.ci)
    
    # 生成输出文件
    if args.output:
        if args.format == 'json':
            output_data = {
                'timestamp': report.timestamp,
                'project_path': report.project_path,
                'summary': report.summary,
                'results': [
                    {
                        'tool': r.tool,
                        'file_path': r.file_path,
                        'passed': r.passed,
                        'metrics': r.metrics,
                        'issues': [
                            {
                                'file': i.file,
                                'line': i.line,
                                'severity': i.severity.name,
                                'code': i.code,
                                'message': i.message,
                                'suggestion': i.suggestion,
                                'category': i.category
                            }
                            for i in r.issues
                        ]
                    }
                    for r in report.results
                ]
            }
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
                
        elif args.format == 'markdown':
            markdown = generator.generate_markdown_report(report)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(markdown)
                
        elif args.format == 'html':
            html = generator.generate_html_report(report)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(html)
        
        print(f"\n报告已保存到: {args.output}")
    
    # 返回退出码
    sys.exit(ExitCode.SUCCESS if report.summary.get('passed', False) else ExitCode.QUALITY_ERROR)


if __name__ == '__main__':
    main()
