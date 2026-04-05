#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AnalysisDataFlow 虚构内容检测审计脚本

功能:
1. 扫描所有Markdown文件
2. 检测潜在的虚构内容模式
3. 生成审计报告，列出可疑内容及其位置
4. 分类: SQL语法 / 配置参数 / Maven依赖 / 时间线预测

作者: AnalysisDataFlow Project
版本: 1.0
日期: 2026-04-05
"""

import os
import re
import sys
import yaml
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from collections import defaultdict
import fnmatch


@dataclass
class Finding:
    """检测结果数据类"""
    file_path: str
    line_number: int
    line_content: str
    category: str
    rule_id: str
    rule_name: str
    matched_text: str
    severity: str
    note: str
    context_before: List[str] = field(default_factory=list)
    context_after: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            'file_path': self.file_path,
            'line_number': self.line_number,
            'line_content': self.line_content.strip(),
            'category': self.category,
            'rule_id': self.rule_id,
            'rule_name': self.rule_name,
            'matched_text': self.matched_text,
            'severity': self.severity,
            'note': self.note,
            'context': {
                'before': self.context_before,
                'after': self.context_after
            }
        }


class FictionalContentAuditor:
    """虚构内容检测审计器"""
    
    def __init__(self, config_path: str, project_root: str):
        self.config = self._load_config(config_path)
        self.project_root = Path(project_root)
        self.findings: List[Finding] = []
        self.stats = defaultdict(int)
        
        # 编译正则表达式
        self.patterns = self._compile_patterns()
        self.exclusion_patterns = self._compile_exclusions()
        
    def _load_config(self, config_path: str) -> Dict:
        """加载YAML配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"错误: 无法加载配置文件 {config_path}: {e}")
            sys.exit(1)
            
    def _compile_patterns(self) -> List[Dict]:
        """编译检测规则为正则表达式"""
        compiled = []
        
        categories = [
            ('sql_syntax', 'SQL语法'),
            ('config_params', '配置参数'),
            ('maven_deps', 'Maven依赖'),
            ('timeline_predictions', '时间线预测'),
            ('flips', 'FLIP提案')
        ]
        
        for cat_key, cat_name in categories:
            if cat_key not in self.config:
                continue
                
            cat_config = self.config[cat_key]
            severity = cat_config.get('severity', 'medium')
            
            for pattern_def in cat_config.get('patterns', []):
                try:
                    compiled.append({
                        'category': cat_name,
                        'rule_id': pattern_def['id'],
                        'rule_name': pattern_def['name'],
                        'pattern': re.compile(pattern_def['pattern'], re.IGNORECASE),
                        'example': pattern_def.get('example', ''),
                        'note': pattern_def.get('note', ''),
                        'severity': severity
                    })
                except re.error as e:
                    print(f"警告: 正则表达式编译失败 {pattern_def.get('id', 'unknown')}: {e}")
                    
        return compiled
        
    def _compile_exclusions(self) -> Dict:
        """编译排除规则"""
        exclusions = self.config.get('exclusions', {})
        compiled = {
            'files': exclusions.get('files', []),
            'lines': [],
            'code_comments': []
        }
        
        # 编译行排除规则
        for pattern in exclusions.get('lines', []):
            try:
                compiled['lines'].append(re.compile(pattern, re.IGNORECASE))
            except re.error:
                pass
                
        # 编译代码注释排除规则
        for pattern in exclusions.get('code_comments', []):
            try:
                compiled['code_comments'].append(re.compile(pattern, re.IGNORECASE))
            except re.error:
                pass
                
        return compiled
        
    def _should_exclude_file(self, file_path: str) -> bool:
        """检查文件是否应该被排除"""
        rel_path = os.path.relpath(file_path, self.project_root)
        
        for pattern in self.exclusion_patterns['files']:
            # 转换glob模式
            pattern_clean = pattern.replace('**/', '').replace('*/', '')
            if pattern_clean in rel_path:
                return True
            if fnmatch.fnmatch(rel_path, pattern):
                return True
                
        return False
        
    def _should_exclude_line(self, line: str) -> bool:
        """检查行是否应该被排除"""
        for pattern in self.exclusion_patterns['lines']:
            if pattern.search(line):
                return True
        return False
        
    def _get_context(self, lines: List[str], current_idx: int, context_lines: int = 2) -> Tuple[List[str], List[str]]:
        """获取上下文行"""
        before = []
        after = []
        
        # 获取前文
        start = max(0, current_idx - context_lines)
        for i in range(start, current_idx):
            before.append(f"{i+1}: {lines[i].rstrip()}")
            
        # 获取后文
        end = min(len(lines), current_idx + context_lines + 1)
        for i in range(current_idx + 1, end):
            after.append(f"{i+1}: {lines[i].rstrip()}")
            
        return before, after
        
    def scan_file(self, file_path: str) -> List[Finding]:
        """扫描单个文件"""
        findings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"警告: 无法读取文件 {file_path}: {e}")
            return findings
            
        for line_idx, line in enumerate(lines):
            # 检查行排除规则
            if self._should_exclude_line(line):
                continue
                
            # 检测每个模式
            for rule in self.patterns:
                matches = rule['pattern'].finditer(line)
                
                for match in matches:
                    # 获取上下文
                    before, after = self._get_context(lines, line_idx)
                    
                    finding = Finding(
                        file_path=file_path,
                        line_number=line_idx + 1,
                        line_content=line,
                        category=rule['category'],
                        rule_id=rule['rule_id'],
                        rule_name=rule['rule_name'],
                        matched_text=match.group(),
                        severity=rule['severity'],
                        note=rule['note'],
                        context_before=before,
                        context_after=after
                    )
                    findings.append(finding)
                    
        return findings
        
    def scan_project(self) -> None:
        """扫描整个项目"""
        print(f"开始扫描项目: {self.project_root}")
        print("-" * 60)
        
        # 查找所有Markdown文件
        md_files = list(self.project_root.rglob("*.md"))
        total_files = len(md_files)
        
        print(f"找到 {total_files} 个Markdown文件")
        
        scanned = 0
        skipped = 0
        
        for md_file in md_files:
            file_path = str(md_file)
            
            # 检查文件排除规则
            if self._should_exclude_file(file_path):
                skipped += 1
                continue
                
            scanned += 1
            file_findings = self.scan_file(file_path)
            self.findings.extend(file_findings)
            
            # 更新统计
            for finding in file_findings:
                self.stats[finding.category] += 1
                self.stats[f"severity_{finding.severity}"] += 1
                
            # 进度显示
            if scanned % 50 == 0:
                print(f"  已扫描 {scanned}/{total_files - skipped} 个文件...")
                
        print("-" * 60)
        print(f"扫描完成: {scanned} 个文件已扫描, {skipped} 个文件已跳过")
        print(f"发现 {len(self.findings)} 个潜在虚构内容")
        
    def generate_report(self, output_path: str) -> None:
        """生成审计报告"""
        report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 按类别和严重级别分组
        findings_by_category = defaultdict(list)
        for finding in self.findings:
            findings_by_category[finding.category].append(finding)
            
        # 生成Markdown报告
        report_lines = [
            "# AnalysisDataFlow 虚构内容审计报告",
            "",
            f"> **报告生成时间**: {report_date}",
            f"> **扫描文件数**: {self.stats.get('scanned', 0)}",
            f"> **发现问题数**: {len(self.findings)}",
            "> **审计工具版本**: 1.0",
            "",
            "---",
            "",
            "## 执行摘要",
            "",
            "### 统计概览",
            "",
            "| 类别 | 发现数量 | 严重级别分布 |",
            "|------|----------|--------------|"
        ]
        
        # 统计表格
        categories = ['SQL语法', '配置参数', 'Maven依赖', '时间线预测', 'FLIP提案']
        for cat in categories:
            count = len(findings_by_category.get(cat, []))
            if count > 0:
                severities = defaultdict(int)
                for f in findings_by_category[cat]:
                    severities[f.severity] += 1
                sev_str = ", ".join([f"{k}:{v}" for k, v in severities.items()])
                report_lines.append(f"| {cat} | {count} | {sev_str} |")
                
        # 严重级别汇总
        report_lines.extend([
            "",
            "### 严重级别分布",
            "",
            "| 级别 | 数量 | 说明 |",
            "|------|------|------|",
            f"| 🔴 High | {self.stats.get('severity_high', 0)} | 高度可能的虚构内容，需要立即处理 |",
            f"| 🟡 Medium | {self.stats.get('severity_medium', 0)} | 中等可能性，建议审查 |",
            f"| 🟢 Low | {self.stats.get('severity_low', 0)} | 低可能性，可作为参考 |",
            "",
            "---",
            "",
        ])
        
        # 详细发现列表
        report_lines.extend([
            "## 详细发现列表",
            "",
            "按类别分组的详细检测结果：",
            ""
        ])
        
        severity_icons = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
        
        for cat in categories:
            findings = findings_by_category.get(cat, [])
            if not findings:
                continue
                
            report_lines.extend([
                f"### {cat}",
                "",
                f"共发现 {len(findings)} 个问题：",
                ""
            ])
            
            # 按文件分组
            by_file = defaultdict(list)
            for f in findings:
                by_file[f.file_path].append(f)
                
            for file_path, file_findings in sorted(by_file.items()):
                rel_path = os.path.relpath(file_path, self.project_root)
                report_lines.extend([
                    f"#### {rel_path}",
                    ""
                ])
                
                for finding in sorted(file_findings, key=lambda x: x.line_number):
                    icon = severity_icons.get(finding.severity, '⚪')
                    report_lines.extend([
                        f"**{icon} [{finding.rule_id}] {finding.rule_name}**",
                        "",
                        f"- **位置**: 第 {finding.line_number} 行",
                        f"- **匹配内容**: `{finding.matched_text}`",
                        f"- **说明**: {finding.note}",
                        "",
                        "**代码片段**：",
                        "",
                        "```markdown"
                    ])
                    
                    # 添加上下文
                    for ctx in finding.context_before:
                        report_lines.append(ctx)
                    report_lines.append(f">>> {finding.line_number}: {finding.line_content.rstrip()}")
                    for ctx in finding.context_after:
                        report_lines.append(ctx)
                        
                    report_lines.extend([
                        "```",
                        ""
                    ])
                    
        # 标记规范建议
        report_lines.extend([
            "---",
            "",
            "## 标记规范建议",
            "",
            "对于检测到的虚构内容，建议使用以下标记方式：",
            "",
            "### 1. 删除线标记",
            "",
            "适用于文本中的虚构API或配置：",
            "",
            "```markdown",
            "~~虚构内容~~ <!-- 概念设计阶段，非实际API -->",
            "```",
            "",
            "### 2. 代码块注释标记",
            "",
            "适用于代码示例中的虚构内容：",
            "",
            "```sql",
            "-- 概念设计阶段，非实际API",
            "-- CREATE AGENT example_agent",
            "```",
            "",
            "### 3. 表格内标记",
            "",
            "适用于表格中的虚构依赖或配置：",
            "",
            "```markdown",
            "| 依赖 | 说明 |",
            "|------|------|",
            "| flink-ai-agent <!-- 设计阶段，尚未发布 --> | AI Agent支持 |",
            "```",
            "",
            "### 4. 时间线预测标记",
            "",
            "```markdown",
            "<!-- 预测时间线，以Apache Flink官方发布为准 -->",
            "预计 2026 Q1 发布",
            "```",
            "",
            "---",
            "",
            "## 附录",
            "",
            "### A. 检测规则配置",
            "",
            "检测规则配置文件位于: `scripts/config/fictional-patterns.yaml`",
            "",
            "### B. 误报处理",
            "",
            "如果某些检测结果为误报，可以通过以下方式处理：",
            "",
            "1. **行级排除**: 在内容所在行添加 `<!-- 已验证: 实际API -->`",
            "2. **文件级排除**: 在配置文件的 `exclusions.files` 中添加文件模式",
            "3. **规则调整**: 修改规则的正则表达式以提高精度",
            "",
            "---",
            "",
            f"*报告生成时间: {report_date}*",
            ""
        ])
        
        # 写入报告
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
            
        print(f"\n审计报告已生成: {output_path}")
        
    def generate_summary_json(self, output_path: str) -> None:
        """生成JSON格式的摘要报告"""
        import json
        
        summary = {
            'scan_date': datetime.now().isoformat(),
            'total_findings': len(self.findings),
            'statistics': dict(self.stats),
            'findings_by_category': {}
        }
        
        for finding in self.findings:
            cat = finding.category
            if cat not in summary['findings_by_category']:
                summary['findings_by_category'][cat] = []
            summary['findings_by_category'][cat].append(finding.to_dict())
            
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"JSON摘要报告已生成: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='AnalysisDataFlow 虚构内容检测审计工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python audit-fictional-content.py
  python audit-fictional-content.py --config custom-config.yaml
  python audit-fictional-content.py --output-dir ./reports
        """
    )
    
    parser.add_argument(
        '--project-root',
        default='e:\\_src\\AnalysisDataFlow',
        help='项目根目录路径 (默认: e:\\_src\\AnalysisDataFlow)'
    )
    
    parser.add_argument(
        '--config',
        default='e:\\_src\\AnalysisDataFlow\\scripts\\config\\fictional-patterns.yaml',
        help='检测规则配置文件路径'
    )
    
    parser.add_argument(
        '--output-dir',
        default='e:\\_src\\AnalysisDataFlow\\reports',
        help='报告输出目录'
    )
    
    parser.add_argument(
        '--format',
        choices=['markdown', 'json', 'both'],
        default='both',
        help='报告格式 (默认: both)'
    )
    
    args = parser.parse_args()
    
    # 确保输出目录存在
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 创建审计器
    auditor = FictionalContentAuditor(args.config, args.project_root)
    
    # 执行扫描
    auditor.scan_project()
    
    # 生成报告
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if args.format in ['markdown', 'both']:
        md_output = os.path.join(args.output_dir, f'fictional-content-audit-{timestamp}.md')
        auditor.generate_report(md_output)
        
    if args.format in ['json', 'both']:
        json_output = os.path.join(args.output_dir, f'fictional-content-audit-{timestamp}.json')
        auditor.generate_summary_json(json_output)
        
    print("\n" + "=" * 60)
    print("审计完成!")
    print(f"发现问题: {len(auditor.findings)} 个")
    print(f"报告目录: {args.output_dir}")
    print("=" * 60)


if __name__ == '__main__':
    main()
