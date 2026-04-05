#!/usr/bin/env python3
"""
新建文档质量门禁检查

分析DataFlow项目文档质量检查脚本
功能：检查新建文档是否符合六段式模板、形式化元素、Mermaid图表等标准

用法：
    python doc-quality-gate.py [文件路径1] [文件路径2] ...
    python doc-quality-gate.py --check-all  # 检查所有Markdown文件
    python doc-quality-gate.py --pr-mode    # PR模式：只检查变更的文件

退出码：
    0 - 所有检查通过
    1 - 发现质量问题
"""

import re
import sys
import os
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
import argparse


@dataclass
class CheckResult:
    """检查结果"""
    passed: bool
    message: str
    details: List[str] = field(default_factory=list)
    score: int = 0  # 0-100


@dataclass
class QualityReport:
    """质量检查报告"""
    file_path: str
    file_name_valid: bool
    sections_check: CheckResult
    formal_elements_check: CheckResult
    mermaid_check: CheckResult
    citations_check: CheckResult
    code_examples_check: CheckResult
    overall_score: int
    passed: bool


# =============================================================================
# 常量定义
# =============================================================================

# 六段式模板必需的章节
REQUIRED_SECTIONS = [
    ('概念定义', ['概念定义', 'Definitions', 'Definition']),
    ('属性推导', ['属性推导', 'Properties', 'Property']),
    ('关系建立', ['关系建立', 'Relations', 'Relationships']),
    ('论证过程', ['论证过程', 'Argumentation', '论证']),
    ('形式证明', ['形式证明', 'Proof', '证明', '工程论证', 'Engineering Argument']),
    ('实例验证', ['实例验证', 'Examples', '实例', '验证']),
]

# 可选章节（用于完整度评分）
OPTIONAL_SECTIONS = [
    ('可视化', ['可视化', 'Visualizations', 'Mermaid']),
    ('引用参考', ['引用参考', 'References', '引用']),
]

# 形式化元素正则模式
FORMAL_ELEMENT_PATTERNS = {
    'Def': re.compile(r'Def-[SKF]-\d{2}-\d{2,3}'),
    'Thm': re.compile(r'Thm-[SKF]-\d{2}-\d{2,3}'),
    'Lemma': re.compile(r'Lemma-[SKF]-\d{2}-\d{2,3}'),
    'Prop': re.compile(r'Prop-[SKF]-\d{2}-\d{2,3}'),
    'Cor': re.compile(r'Cor-[SKF]-\d{2}-\d{2,3}'),
}

# 文件名命名规范
FILENAME_PATTERN = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*\.md$')

# 引用格式模式
CITATION_PATTERN = re.compile(r'\[\^\d+\]')

# Mermaid图表模式
MERMAID_PATTERN = re.compile(r'```mermaid\s*\n', re.IGNORECASE)

# 代码块模式
CODE_BLOCK_PATTERN = re.compile(r'```(\w+)?\s*\n')


# =============================================================================
# 核心检查函数
# =============================================================================

def check_file_name(file_path: Path) -> Tuple[bool, str]:
    """
    检查文件名是否符合命名规范
    
    规范：
    - 全部小写
    - 使用连字符分隔
    - 以.md结尾
    """
    file_name = file_path.name
    
    # 特殊文件豁免（如README.md, CHANGELOG.md等）
    exempt_files = ['README.md', 'CHANGELOG.md', 'CONTRIBUTING.md', 'LICENSE.md', 
                    'AGENTS.md', 'CODE_OF_CONDUCT.md', 'SECURITY.md']
    if file_name in exempt_files:
        return True, f"特殊文件 {file_name} 豁免检查"
    
    if FILENAME_PATTERN.match(file_name):
        return True, f"文件名 '{file_name}' 符合规范"
    else:
        return False, f"文件名 '{file_name}' 不符合规范：应使用小写字母、数字和连字符"


def check_six_section_template(content: str) -> CheckResult:
    """
    检查六段式模板
    
    必需章节：
    1. 概念定义
    2. 属性推导
    3. 关系建立
    4. 论证过程
    5. 形式证明/工程论证
    6. 实例验证
    """
    found_sections = []
    missing_sections = []
    details = []
    
    for section_name, aliases in REQUIRED_SECTIONS:
        found = False
        for alias in aliases:
            # 匹配 ## 1. 标题 或 ## 标题 格式
            patterns = [
                rf'##\s*\d+\.\s*{re.escape(alias)}',
                rf'##\s*{re.escape(alias)}',
            ]
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    found = True
                    break
            if found:
                break
        
        if found:
            found_sections.append(section_name)
        else:
            missing_sections.append(section_name)
    
    # 检查可选章节
    optional_found = 0
    for section_name, aliases in OPTIONAL_SECTIONS:
        for alias in aliases:
            patterns = [
                rf'##\s*\d+\.\s*{re.escape(alias)}',
                rf'##\s*{re.escape(alias)}',
            ]
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    optional_found += 1
                    break
    
    # 计算得分
    required_score = len(found_sections) / len(REQUIRED_SECTIONS) * 70
    optional_score = optional_found / len(OPTIONAL_SECTIONS) * 30
    total_score = int(required_score + optional_score)
    
    if missing_sections:
        details.append(f"❌ 缺少必需章节: {', '.join(missing_sections)}")
    if found_sections:
        details.append(f"✅ 已包含章节: {', '.join(found_sections)}")
    
    passed = len(missing_sections) == 0
    message = f"六段式模板检查: {'通过' if passed else '未通过'} ({len(found_sections)}/{len(REQUIRED_SECTIONS)}必需章节)"
    
    return CheckResult(passed=passed, message=message, details=details, score=total_score)


def check_formal_elements(content: str) -> CheckResult:
    """
    检查形式化元素（Def/Thm/Lemma/Prop/Cor）
    
    要求：至少3个形式化元素
    只检测章节标题中的声明（行首的 ### X-X-X-X: 格式）
    """
    counts = {}
    details = []
    all_elements = []
    
    # 只匹配章节标题中的形式化元素（行首的 ### X-X-X-X:）
    for elem_type, pattern in FORMAL_ELEMENT_PATTERNS.items():
        # 匹配行首的 ### Type-Stage-Doc-Seq: 格式
        declaration_pattern = re.compile(
            rf'^###\s+({pattern.pattern}):',
            re.MULTILINE
        )
        matches = declaration_pattern.findall(content)
        counts[elem_type] = len(matches)
        all_elements.extend(matches)
    
    total_count = len(all_elements)
    unique_count = len(set(all_elements))
    
    # 检查重复（仅检查声明的编号）
    duplicates = []
    seen = set()
    for elem in all_elements:
        if elem in seen:
            duplicates.append(elem)
        seen.add(elem)
    
    # 计算得分
    if total_count >= 3:
        score = 100
    elif total_count >= 2:
        score = 70
    elif total_count >= 1:
        score = 40
    else:
        score = 0
    
    if duplicates:
        details.append(f"⚠️ 发现重复的编号: {', '.join(set(duplicates))}")
    
    for elem_type, count in sorted(counts.items()):
        if count > 0:
            details.append(f"  - {elem_type}: {count}个")
    
    passed = total_count >= 3
    message = f"形式化元素检查: 发现 {total_count} 个元素（要求≥3个）"
    
    return CheckResult(passed=passed, message=message, details=details, score=score)


def check_mermaid_diagrams(content: str) -> CheckResult:
    """
    检查Mermaid图表
    
    要求：至少1个Mermaid图表
    """
    matches = MERMAID_PATTERN.findall(content)
    count = len(matches)
    
    details = []
    if count > 0:
        details.append(f"✅ 发现 {count} 个Mermaid图表")
    else:
        details.append("❌ 未发现Mermaid图表")
    
    # 检查图表类型
    diagram_types = []
    if 'graph TD' in content or 'graph TB' in content or 'graph LR' in content:
        diagram_types.append("graph")
    if 'flowchart' in content:
        diagram_types.append("flowchart")
    if 'sequenceDiagram' in content:
        diagram_types.append("sequence")
    if 'classDiagram' in content:
        diagram_types.append("class")
    if 'stateDiagram' in content:
        diagram_types.append("state")
    if 'gantt' in content:
        diagram_types.append("gantt")
    
    if diagram_types:
        details.append(f"  图表类型: {', '.join(diagram_types)}")
    
    score = 100 if count >= 1 else 0
    passed = count >= 1
    message = f"Mermaid图表检查: 发现 {count} 个图表（要求≥1个）"
    
    return CheckResult(passed=passed, message=message, details=details, score=score)


def check_citations(content: str) -> CheckResult:
    """
    检查引用格式
    
    要求：使用[^n]格式引用
    """
    matches = CITATION_PATTERN.findall(content)
    count = len(matches)
    
    details = []
    
    # 检查引用定义
    ref_definitions = re.findall(r'\[\^(\d+)\]:', content)
    defined_refs = set(ref_definitions)
    used_refs = set(re.findall(r'\[\^(\d+)\]', content))
    
    undefined_refs = used_refs - defined_refs
    unused_refs = defined_refs - used_refs
    
    if undefined_refs:
        details.append(f"⚠️ 引用了但未定义的引用: {', '.join(sorted(undefined_refs, key=int))}")
    if unused_refs:
        details.append(f"⚠️ 已定义但未使用的引用: {', '.join(sorted(unused_refs, key=int))}")
    
    # 计算得分
    if count >= 2:
        score = 100
    elif count == 1:
        score = 60
    else:
        score = 30
    
    if count > 0:
        details.append(f"✅ 发现 {count} 处引用")
    
    passed = len(undefined_refs) == 0
    message = f"引用格式检查: 发现 {count} 处引用"
    
    return CheckResult(passed=passed, message=message, details=details, score=score)


def check_code_examples(content: str) -> CheckResult:
    """
    检查代码示例
    
    检测代码块，评估代码示例质量
    """
    code_blocks = list(CODE_BLOCK_PATTERN.finditer(content))
    count = len(code_blocks)
    
    details = []
    languages = defaultdict(int)
    
    for match in code_blocks:
        lang = match.group(1) if match.group(1) else '无语言标记'
        languages[lang] += 1
    
    # 排除mermaid代码块
    mermaid_count = len(MERMAID_PATTERN.findall(content))
    code_count = count - mermaid_count
    
    if code_count > 0:
        details.append(f"✅ 发现 {code_count} 个代码示例")
        for lang, cnt in sorted(languages.items()):
            if lang != 'mermaid' and lang != '无语言标记':
                details.append(f"  - {lang}: {cnt}个")
    else:
        details.append("⚠️ 未发现代码示例（可选）")
    
    # 检查是否有代码说明
    has_explanations = bool(re.search(r'```\w+\s*\n[\s\S]*?```\s*\n[^`]{10,}', content))
    if has_explanations:
        details.append("✅ 代码示例带有说明")
    
    # 计算得分（代码示例是可选的）
    if code_count >= 2:
        score = 100
    elif code_count >= 1:
        score = 80
    else:
        score = 60
    
    passed = True  # 代码示例是可选的
    message = f"代码示例检查: 发现 {code_count} 个代码块"
    
    return CheckResult(passed=passed, message=message, details=details, score=score)


def check_document_header(content: str) -> CheckResult:
    """
    检查文档头部信息
    
    格式：
    > 所属阶段: [Struct|Knowledge|Flink] | 前置依赖: [链接] | 形式化等级: L[1-6]
    """
    details = []
    score = 0
    
    # 匹配文档头部信息行（支持带粗体的格式）
    header_patterns = [
        # 标准格式: > 所属阶段: X | 前置依赖: Y | 形式化等级: L3
        r'^>\s*所属阶段:\s*(\w+)\s*\|\s*前置依赖:\s*([^|]*)\|\s*形式化等级:\s*L?([1-6])',
        # 粗体格式: > **所属阶段**: X | **前置依赖**: Y | **形式化等级**: L3
        r'^>\s*\*\*所属阶段\*\*:\s*(\w+)\s*\|\s*\*\*前置依赖\*\*:\s*([^|]*)\|\s*\*\*形式化等级\*\*:\s*L?([1-6])',
    ]
    
    match = None
    for pattern in header_patterns:
        match = re.search(pattern, content, re.MULTILINE)
        if match:
            break
    
    if match:
        stage = match.group(1)
        dependencies = match.group(2).strip()
        level = match.group(3)
        
        valid_stages = ['Struct', 'Knowledge', 'Flink']
        
        details.append(f"✅ 文档头部信息完整")
        details.append(f"  - 所属阶段: {stage}")
        details.append(f"  - 前置依赖: {dependencies[:50]}{'...' if len(dependencies) > 50 else ''}")
        details.append(f"  - 形式化等级: L{level}")
        
        if stage in valid_stages:
            score += 40
        else:
            details.append(f"⚠️ 阶段 '{stage}' 不是标准值（应为Struct/Knowledge/Flink之一）")
        
        if dependencies and dependencies != '[]':
            score += 30
        
        if level:
            score += 30
        
        passed = stage in valid_stages
    else:
        details.append("❌ 缺少标准文档头部信息")
        details.append("  格式应为: > 所属阶段: [Struct|Knowledge|Flink] | 前置依赖: [链接] | 形式化等级: L[1-6]")
        passed = False
        score = 0
    
    message = "文档头部信息检查: " + ("通过" if passed else "未通过")
    return CheckResult(passed=passed, message=message, details=details, score=score)


# =============================================================================
# 主检查流程
# =============================================================================

def check_document(file_path: Path) -> QualityReport:
    """检查单个文档"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return QualityReport(
            file_path=str(file_path),
            file_name_valid=False,
            sections_check=CheckResult(False, f"无法读取文件: {e}", [], 0),
            formal_elements_check=CheckResult(False, "", [], 0),
            mermaid_check=CheckResult(False, "", [], 0),
            citations_check=CheckResult(False, "", [], 0),
            code_examples_check=CheckResult(False, "", [], 0),
            overall_score=0,
            passed=False
        )
    
    # 执行各项检查
    file_name_valid, _ = check_file_name(file_path)
    header_check = check_document_header(content)
    sections_check = check_six_section_template(content)
    formal_check = check_formal_elements(content)
    mermaid_check = check_mermaid_diagrams(content)
    citation_check = check_citations(content)
    code_check = check_code_examples(content)
    
    # 计算总体得分（限制每项最高100分）
    weights = {
        'header': 0.15,
        'sections': 0.25,
        'formal': 0.25,
        'mermaid': 0.15,
        'citation': 0.10,
        'code': 0.10,
    }
    
    overall_score = int(
        min(header_check.score, 100) * weights['header'] +
        min(sections_check.score, 100) * weights['sections'] +
        min(formal_check.score, 100) * weights['formal'] +
        min(mermaid_check.score, 100) * weights['mermaid'] +
        min(citation_check.score, 100) * weights['citation'] +
        min(code_check.score, 100) * weights['code']
    )
    
    # 判断是否通过
    passed = (
        file_name_valid and
        header_check.passed and
        sections_check.passed and
        formal_check.passed and
        mermaid_check.passed
    )
    
    return QualityReport(
        file_path=str(file_path),
        file_name_valid=file_name_valid,
        sections_check=sections_check,
        formal_elements_check=formal_check,
        mermaid_check=mermaid_check,
        citations_check=citation_check,
        code_examples_check=code_check,
        overall_score=overall_score,
        passed=passed
    )


def print_report(report: QualityReport, verbose: bool = False):
    """打印检查报告"""
    print(f"\n{'='*70}")
    print(f"📄 文件: {report.file_path}")
    print(f"{'='*70}")
    
    # 文件名检查
    status = "✅" if report.file_name_valid else "❌"
    print(f"\n{status} 文件名规范")
    
    # 各项检查结果（注意：需要重新获取header_check，这里使用简化处理）
    # 由于QualityReport中没有存储header_check，我们简化输出
    checks = [
        ("六段式模板", report.sections_check),
        ("形式化元素", report.formal_elements_check),
        ("Mermaid图表", report.mermaid_check),
        ("引用格式", report.citations_check),
        ("代码示例", report.code_examples_check),
    ]
    
    for name, check in checks:
        status = "✅" if check.passed else "❌"
        print(f"\n{status} {check.message} (得分: {check.score})")
        if verbose or not check.passed:
            for detail in check.details:
                print(f"   {detail}")
    
    # 总体评分
    print(f"\n{'-'*70}")
    status = "✅ 通过" if report.passed else "❌ 未通过"
    print(f"总体评分: {report.overall_score}/100 - {status}")
    print(f"{'='*70}\n")


def print_summary(reports: List[QualityReport]):
    """打印总结报告"""
    total = len(reports)
    passed = sum(1 for r in reports if r.passed)
    failed = total - passed
    avg_score = sum(r.overall_score for r in reports) / total if total > 0 else 0
    
    print(f"\n{'='*70}")
    print("📊 质量门禁检查总结")
    print(f"{'='*70}")
    print(f"\n总计检查: {total} 个文件")
    print(f"✅ 通过: {passed} 个")
    print(f"❌ 未通过: {failed} 个")
    print(f"📈 平均得分: {avg_score:.1f}/100")
    
    if failed > 0:
        print(f"\n❌ 未通过的文件:")
        for report in reports:
            if not report.passed:
                print(f"  - {report.file_path} (得分: {report.overall_score})")
    
    print(f"\n{'='*70}\n")
    
    return failed == 0


def get_changed_files() -> List[Path]:
    """获取PR中变更的Markdown文件"""
    # 从环境变量获取变更文件列表
    changed = os.environ.get('CHANGED_FILES', '')
    if changed:
        files = [f.strip() for f in changed.split('\n') if f.strip().endswith('.md')]
        return [Path(f) for f in files if Path(f).exists()]
    return []


def get_all_markdown_files() -> List[Path]:
    """获取所有Markdown文件"""
    md_files = list(Path('.').rglob('*.md'))
    # 排除隐藏目录和依赖目录
    md_files = [f for f in md_files if not any(
        part.startswith('.') or part in ['node_modules', '__pycache__', '.git', 'vendor']
        for part in f.parts
    )]
    return md_files


def generate_github_actions_output(reports: List[QualityReport]):
    """生成GitHub Actions输出"""
    summary_file = os.environ.get('GITHUB_STEP_SUMMARY')
    if not summary_file:
        return
    
    total = len(reports)
    passed = sum(1 for r in reports if r.passed)
    failed = total - passed
    avg_score = sum(r.overall_score for r in reports) / total if total > 0 else 0
    
    with open(summary_file, 'a', encoding='utf-8') as f:
        f.write("\n## 📋 文档质量门禁检查\n\n")
        f.write(f"| 指标 | 数值 |\n")
        f.write(f"|------|------|\n")
        f.write(f"| 检查文件数 | {total} |\n")
        f.write(f"| 通过 | {passed} ✅ |\n")
        f.write(f"| 未通过 | {failed} {'❌' if failed > 0 else ''} |\n")
        f.write(f"| 平均得分 | {avg_score:.1f}/100 |\n")
        f.write("\n")
        
        if failed > 0:
            f.write("### ❌ 未通过的文件\n\n")
            f.write("| 文件 | 得分 | 问题 |\n")
            f.write("|------|------|------|\n")
            for report in reports:
                if not report.passed:
                    issues = []
                    if not report.sections_check.passed:
                        issues.append("六段式")
                    if not report.formal_elements_check.passed:
                        issues.append("形式化元素")
                    if not report.mermaid_check.passed:
                        issues.append("Mermaid图表")
                    f.write(f"| {report.file_path} | {report.overall_score} | {', '.join(issues)} |\n")
            f.write("\n")


def main():
    parser = argparse.ArgumentParser(
        description='分析DataFlow文档质量门禁检查',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s file1.md file2.md          # 检查指定文件
  %(prog)s --check-all                 # 检查所有Markdown文件
  %(prog)s --pr-mode                   # PR模式：检查变更文件
  %(prog)s --verbose file.md           # 详细输出
        """
    )
    parser.add_argument('files', nargs='*', help='要检查的文件路径')
    parser.add_argument('--check-all', action='store_true', help='检查所有Markdown文件')
    parser.add_argument('--pr-mode', action='store_true', help='PR模式：检查变更的文件')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    parser.add_argument('--json', action='store_true', help='以JSON格式输出结果')
    
    args = parser.parse_args()
    
    # 确定要检查的文件
    if args.pr_mode:
        files_to_check = get_changed_files()
        print(f"PR模式: 检查 {len(files_to_check)} 个变更的Markdown文件")
    elif args.check_all:
        files_to_check = get_all_markdown_files()
        print(f"检查所有 {len(files_to_check)} 个Markdown文件")
    elif args.files:
        files_to_check = [Path(f) for f in args.files]
    else:
        # 默认检查当前目录下新增的文件
        files_to_check = get_changed_files()
        if not files_to_check:
            parser.print_help()
            print("\n❌ 错误: 未指定文件且未检测到变更文件")
            sys.exit(1)
    
    if not files_to_check:
        print("✅ 没有需要检查的Markdown文件")
        sys.exit(0)
    
    # 执行检查
    reports = []
    for file_path in files_to_check:
        if not file_path.exists():
            print(f"⚠️ 跳过不存在的文件: {file_path}")
            continue
        report = check_document(file_path)
        reports.append(report)
        if not args.json:
            print_report(report, args.verbose)
    
    # JSON输出
    if args.json:
        output = {
            'summary': {
                'total': len(reports),
                'passed': sum(1 for r in reports if r.passed),
                'failed': sum(1 for r in reports if not r.passed),
                'average_score': sum(r.overall_score for r in reports) / len(reports) if reports else 0,
            },
            'reports': [
                {
                    'file': r.file_path,
                    'passed': r.passed,
                    'score': r.overall_score,
                    'checks': {
                        'file_name': r.file_name_valid,
                        'sections': {
                            'passed': r.sections_check.passed,
                            'score': r.sections_check.score,
                            'details': r.sections_check.details,
                        },
                        'formal_elements': {
                            'passed': r.formal_elements_check.passed,
                            'score': r.formal_elements_check.score,
                            'details': r.formal_elements_check.details,
                        },
                        'mermaid': {
                            'passed': r.mermaid_check.passed,
                            'score': r.mermaid_check.score,
                            'details': r.mermaid_check.details,
                        },
                    }
                }
                for r in reports
            ]
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        # 打印总结
        all_passed = print_summary(reports)
        
        # 生成GitHub Actions输出
        generate_github_actions_output(reports)
        
        # 返回退出码
        sys.exit(0 if all_passed else 1)


if __name__ == '__main__':
    main()
