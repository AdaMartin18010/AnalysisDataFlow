#!/usr/bin/env python3
"""
质量检查器 - 翻译质量验证与术语一致性检查

功能:
1. 术语一致性检查
2. Markdown格式验证
3. 链接有效性检查
4. 代码块语法检查
5. Mermaid图表验证

作者: AnalysisDataFlow i18n Team
版本: 4.0-prep
"""

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class CheckResult:
    """检查结果"""
    rule_id: str
    severity: str  # error, warning, suggestion
    message: str
    line: Optional[int] = None
    column: Optional[int] = None
    suggestion: Optional[str] = None


@dataclass
class FileReport:
    """文件检查报告"""
    file_path: str
    passed: bool = True
    issues: List[CheckResult] = field(default_factory=list)
    stats: Dict = field(default_factory=dict)


class QualityChecker:
    """翻译质量检查器"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.terminology: Dict = {}
        self.verification_rules: Dict = {}
        self.reports: List[FileReport] = []
        
        self.load_terminology()
        self.load_verification_rules()
    
    def load_terminology(self) -> None:
        """加载术语库"""
        # 加载核心术语
        core_terms_path = self.project_root / "i18n/terminology/core-terms.json"
        if core_terms_path.exists():
            with open(core_terms_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for term in data.get("terms", []):
                    self.terminology[term["term"]] = term
        
        # 加载Flink术语
        flink_terms_path = self.project_root / "i18n/terminology/flink-terms.json"
        if flink_terms_path.exists():
            with open(flink_terms_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for term in data.get("terms", []):
                    self.terminology[term["term"]] = term
    
    def load_verification_rules(self) -> None:
        """加载验证规则"""
        rules_path = self.project_root / "i18n/terminology/verification-rules.json"
        if rules_path.exists():
            with open(rules_path, 'r', encoding='utf-8') as f:
                self.verification_rules = json.load(f)
    
    def check_term_consistency(self, content: str, file_path: str) -> List[CheckResult]:
        """检查术语一致性"""
        issues = []
        
        for term_id, term_info in self.terminology.items():
            chinese_term = term_info["term"]
            english_term = term_info["en"]
            forbidden = term_info.get("forbidden_variants", [])
            
            # 检查禁止变体
            for variant in forbidden:
                pattern = r'\b' + re.escape(variant) + r'\b'
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    issues.append(CheckResult(
                        rule_id="TERM-002",
                        severity="warning",
                        message=f"检测到术语禁止变体: '{variant}'",
                        line=content[:match.start()].count('\n') + 1,
                        suggestion=f"使用标准术语: '{english_term}'"
                    ))
            
            # 检查中文术语是否被正确翻译
            # 这里简化处理，实际应更复杂
            if chinese_term in content and term_info.get("verified"):
                # 在英文文档中不应出现中文术语
                if "/en/" in file_path:
                    for match in re.finditer(re.escape(chinese_term), content):
                        issues.append(CheckResult(
                            rule_id="TERM-001",
                            severity="error",
                            message=f"英文文档中出现中文术语: '{chinese_term}'",
                            line=content[:match.start()].count('\n') + 1,
                            suggestion=f"使用英文术语: '{english_term}'"
                        ))
        
        return issues
    
    def check_markdown_format(self, content: str) -> List[CheckResult]:
        """检查Markdown格式"""
        issues = []
        lines = content.split('\n')
        
        # 检查标题层级
        header_levels = []
        for i, line in enumerate(lines, 1):
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                header_levels.append((i, level))
        
        # 检查标题层级跳跃
        for i in range(1, len(header_levels)):
            prev_level = header_levels[i-1][1]
            curr_level = header_levels[i][1]
            if curr_level > prev_level + 1:
                issues.append(CheckResult(
                    rule_id="FMT-002",
                    severity="error",
                    message=f"标题层级跳跃: H{prev_level} -> H{curr_level}",
                    line=header_levels[i][0],
                    suggestion="标题层级应连续，不要跳跃"
                ))
        
        # 检查代码块
        code_block_pattern = r'```(\w*)'
        for match in re.finditer(code_block_pattern, content):
            lang = match.group(1)
            line_num = content[:match.start()].count('\n') + 1
            
            # 检查语言标签
            if not lang:
                issues.append(CheckResult(
                    rule_id="FMT-003",
                    severity="warning",
                    message="代码块缺少语言标签",
                    line=line_num,
                    suggestion="添加语言标签，如 ```java, ```python"
                ))
        
        # 检查未闭合的代码块
        code_block_starts = len(re.findall(r'```\w*\n', content))
        code_block_ends = len(re.findall(r'\n```\s*$', content, re.MULTILINE)) + \
                         len(re.findall(r'\n```\s*\n', content))
        
        if code_block_starts != code_block_ends:
            issues.append(CheckResult(
                rule_id="FMT-001",
                severity="error",
                message=f"代码块未正确闭合: {code_block_starts} 开始, {code_block_ends} 结束",
                suggestion="检查代码块的 ``` 标记是否配对"
            ))
        
        return issues
    
    def check_links(self, content: str, file_path: str) -> List[CheckResult]:
        """检查链接有效性"""
        issues = []
        
        # 查找Markdown链接
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        
        for match in re.finditer(link_pattern, content):
            link_text = match.group(1)
            link_url = match.group(2)
            line_num = content[:match.start()].count('\n') + 1
            
            # 检查内部链接
            if not link_url.startswith(('http://', 'https://', '#', 'mailto:')):
                # 解析相对路径
                base_dir = Path(file_path).parent
                target_path = base_dir / link_url.split('#')[0]
                
                if not target_path.exists():
                    issues.append(CheckResult(
                        rule_id="FMT-005",
                        severity="warning",
                        message=f"内部链接可能无效: '{link_url}'",
                        line=line_num,
                        suggestion="检查链接目标文件是否存在"
                    ))
        
        return issues
    
    def check_mermaid_syntax(self, content: str) -> List[CheckResult]:
        """检查Mermaid图表语法"""
        issues = []
        
        # 提取Mermaid代码块
        mermaid_pattern = r'```mermaid\n(.*?)```'
        
        for match in re.finditer(mermaid_pattern, content, re.DOTALL):
            mermaid_code = match.group(1)
            line_num = content[:match.start()].count('\n') + 1
            
            # 基本语法检查
            # 检查图表类型
            valid_types = ['graph', 'flowchart', 'sequenceDiagram', 'classDiagram', 
                          'stateDiagram', 'gantt', 'pie', 'erDiagram', 'journey']
            
            first_line = mermaid_code.strip().split('\n')[0].lower()
            
            if not any(first_line.startswith(t) for t in valid_types):
                issues.append(CheckResult(
                    rule_id="CNT-001",
                    severity="warning",
                    message=f"未知的Mermaid图表类型: '{first_line}'",
                    line=line_num,
                    suggestion=f"使用有效的图表类型: {', '.join(valid_types)}"
                ))
            
            # 检查基本语法错误
            if '-->' in mermaid_code and not any(x in first_line for x in ['graph', 'flowchart']):
                # 在其他图表类型中可能有问题
                pass
        
        return issues
    
    def check_frontmatter(self, content: str) -> List[CheckResult]:
        """检查Frontmatter完整性"""
        issues = []
        
        # 检查是否有frontmatter
        if not content.startswith('---'):
            issues.append(CheckResult(
                rule_id="FMT-004",
                severity="error",
                message="文档缺少frontmatter",
                suggestion="添加必要的frontmatter字段"
            ))
            return issues
        
        # 解析frontmatter
        try:
            end_marker = content.find('---', 3)
            if end_marker == -1:
                issues.append(CheckResult(
                    rule_id="FMT-004",
                    severity="error",
                    message="frontmatter未正确闭合",
                    suggestion="确保frontmatter以 --- 结束"
                ))
                return issues
            
            frontmatter = content[3:end_marker].strip()
            
            # 检查必需字段
            required_fields = self.verification_rules.get("format_validation", {}).get("rules", [])
            frontmatter_rules = [r for r in required_fields if r.get("id") == "FMT-004"]
            
            if frontmatter_rules:
                for field in frontmatter_rules[0].get("required_fields", []):
                    if field not in frontmatter:
                        issues.append(CheckResult(
                            rule_id="FMT-004",
                            severity="error",
                            message=f"frontmatter缺少必需字段: '{field}'",
                            suggestion=f"添加 {field}: value"
                        ))
        
        except Exception as e:
            issues.append(CheckResult(
                rule_id="FMT-004",
                severity="error",
                message=f"解析frontmatter时出错: {e}",
                suggestion="检查frontmatter格式是否正确"
            ))
        
        return issues
    
    def check_prohibited_terms(self, content: str) -> List[CheckResult]:
        """检查禁止翻译的术语"""
        issues = []
        
        prohibited = self.verification_rules.get("prohibited_translation", {}).get("categories", {})
        
        # 检查产品名是否被翻译
        for category, config in prohibited.items():
            if category in ["products", "programming_languages"]:
                terms = config.get("terms", [])
                for term in terms:
                    # 简单检查：如果术语被翻译为中文形式
                    # 实际应更复杂，考虑上下文
                    pass
        
        return issues
    
    def check_file(self, file_path: str) -> FileReport:
        """检查单个文件"""
        report = FileReport(file_path=file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            report.issues.append(CheckResult(
                rule_id="FILE-001",
                severity="error",
                message=f"无法读取文件: {e}"
            ))
            report.passed = False
            return report
        
        # 执行各项检查
        report.issues.extend(self.check_term_consistency(content, file_path))
        report.issues.extend(self.check_markdown_format(content))
        report.issues.extend(self.check_links(content, file_path))
        report.issues.extend(self.check_mermaid_syntax(content))
        report.issues.extend(self.check_frontmatter(content))
        report.issues.extend(self.check_prohibited_terms(content))
        
        # 统计
        error_count = sum(1 for i in report.issues if i.severity == "error")
        warning_count = sum(1 for i in report.issues if i.severity == "warning")
        
        report.stats = {
            "total_issues": len(report.issues),
            "errors": error_count,
            "warnings": warning_count,
            "line_count": content.count('\n') + 1,
            "word_count": len(content.split())
        }
        
        report.passed = error_count == 0
        
        return report
    
    def check_all(self, target_dir: str = "i18n/en") -> List[FileReport]:
        """检查所有翻译文件"""
        target_path = self.project_root / target_dir
        
        if not target_path.exists():
            print(f"⚠️  目标目录不存在: {target_dir}")
            return []
        
        reports = []
        
        for md_file in target_path.rglob("*.md"):
            print(f"🔍 检查: {md_file.relative_to(self.project_root)}")
            report = self.check_file(str(md_file))
            reports.append(report)
        
        self.reports = reports
        return reports
    
    def generate_report(self) -> str:
        """生成质量检查报告"""
        total_files = len(self.reports)
        passed_files = sum(1 for r in self.reports if r.passed)
        total_issues = sum(len(r.issues) for r in self.reports)
        total_errors = sum(r.stats.get("errors", 0) for r in self.reports)
        total_warnings = sum(r.stats.get("warnings", 0) for r in self.reports)
        
        report_lines = [
            "# 翻译质量检查报告",
            "",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**版本**: v4.0-prep",
            "",
            "## 摘要",
            "",
            f"| 指标 | 数值 |",
            f"|------|------|",
            f"| 检查文件数 | {total_files} |",
            f"| 通过文件数 | {passed_files} |",
            f"| 失败文件数 | {total_files - passed_files} |",
            f"| 总问题数 | {total_issues} |",
            f"| 错误数 | {total_errors} |",
            f"| 警告数 | {total_warnings} |",
            f"| 通过率 | {(passed_files/total_files*100) if total_files else 0:.1f}% |",
            "",
            "## 问题汇总",
            ""
        ]
        
        # 按文件列出问题
        for report in self.reports:
            if report.issues:
                rel_path = Path(report.file_path).relative_to(self.project_root)
                status = "✅" if report.passed else "❌"
                
                report_lines.extend([
                    f"### {status} {rel_path}",
                    "",
                    "| 行 | 严重级别 | 规则 | 问题 | 建议 |",
                    "|----|----------|------|------|------|"
                ])
                
                for issue in report.issues:
                    line = issue.line or "-"
                    suggestion = issue.suggestion or "-"
                    report_lines.append(
                        f"| {line} | {issue.severity} | {issue.rule_id} | {issue.message} | {suggestion} |"
                    )
                
                report_lines.append("")
        
        # 添加建议
        report_lines.extend([
            "## 修复建议",
            "",
            "1. **术语一致性问题**: 参考 `i18n/terminology/core-terms.json` 使用标准术语",
            "2. **格式问题**: 确保Markdown语法正确，标题层级连续",
            "3. **链接问题**: 验证所有内部链接指向有效文件",
            "4. **Mermaid图表**: 使用有效的图表类型和语法",
            ""
        ])
        
        return '\n'.join(report_lines)
    
    def save_report(self, report: str) -> None:
        """保存报告"""
        report_path = self.project_root / "i18n/translation-workflow/reports/quality-report.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 报告已保存: {report_path}")
    
    def run(self, target: str = "all") -> None:
        """运行质量检查"""
        print("🔍 开始翻译质量检查...")
        print(f"📚 已加载 {len(self.terminology)} 个术语")
        
        if target == "all":
            self.check_all()
        else:
            report = self.check_file(target)
            self.reports = [report]
        
        # 生成并保存报告
        report = self.generate_report()
        self.save_report(report)
        
        # 打印摘要
        total_files = len(self.reports)
        passed_files = sum(1 for r in self.reports if r.passed)
        
        print(f"\n📊 检查结果:")
        print(f"   检查文件: {total_files}")
        print(f"   通过: {passed_files}")
        print(f"   失败: {total_files - passed_files}")
        
        if passed_files == total_files:
            print("\n✅ 所有文件通过质量检查!")
        else:
            print(f"\n⚠️  {total_files - passed_files} 个文件需要修复")


def main():
    """主入口"""
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    target = sys.argv[2] if len(sys.argv) > 2 else "all"
    
    checker = QualityChecker(project_root)
    checker.run(target)


if __name__ == "__main__":
    main()
