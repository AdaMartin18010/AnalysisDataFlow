#!/usr/bin/env python3
"""
文档新鲜度检查器 (Document Freshness Checker)
扫描项目中 Markdown 文档的更新日期，标记过期内容和前瞻内容。

用法:
    python .scripts/doc-freshness-checker.py
    python .scripts/doc-freshness-checker.py --output FRESHNESS-REPORT.md
"""

import argparse
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple

# 核心目录（需要检查新鲜度）
CORE_DIRS = ["Struct", "Knowledge", "Flink", "en", "formal-methods"]
# 跳过目录
SKIP_DIRS = [".git", ".github", ".scripts", "release", "archive", "reports", "benchmark-results", ".tasks", ".templates", ".vscode", "node_modules"]
# 前瞻关键词
FICTIONAL_KEYWORDS = ["前瞻", "🔮", "预计发布", "预计", "风险等级: 高", "不代表官方", "fictional", "preview"]
# 日期解析正则
DATE_PATTERNS = [
    re.compile(r">\s*\*\*最后更新\*\*:\s*(\d{4}-\d{2}-\d{2})"),
    re.compile(r">\s*\*\*最后核实日期\*\*:\s*(\d{4}-\d{2}-\d{2})"),
    re.compile(r">\s*\*\*生效日期\*\*:\s*(\d{4}-\d{2}-\d{2})"),
    re.compile(r">\s*\*\*发布日期\*\*:\s*(\d{4}-\d{2}-\d{2})"),
    re.compile(r"\*\*最后更新\*\*:\s*(\d{4}-\d{2}-\d{2})"),
]
# 预计发布日期正则
TARGET_DATE_PATTERNS = [
    re.compile(r"目标发布[:：]\s*(\d{4})\s*[年Q](\d+)"),
    re.compile(r"预计发布时间[:：]\s*(\d{4})\s*[年Q](\d+)"),
    re.compile(r"Release goal[:：]\s*(\d{4}-\d{2}-\d{2})"),
]


class FreshnessIssue:
    def __init__(self, file_path: str, issue_type: str, detail: str, severity: str):
        self.file_path = file_path
        self.issue_type = issue_type
        self.detail = detail
        self.severity = severity  # 🔴 P0 / 🟠 P1 / 🟡 P2


def parse_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d")


def extract_date_from_content(content: str) -> Tuple[datetime, str]:
    """从文档内容中提取最后更新日期"""
    for pattern in DATE_PATTERNS:
        match = pattern.search(content)
        if match:
            try:
                return parse_date(match.group(1)), match.group(0)
            except ValueError:
                continue
    return None, ""


def extract_target_date(content: str) -> Tuple[str, str]:
    """提取预计发布日期"""
    for pattern in TARGET_DATE_PATTERNS:
        match = pattern.search(content)
        if match:
            if match.lastindex >= 2:
                year, quarter = match.group(1), match.group(2)
                return f"{year} Q{quarter}", match.group(0)
            else:
                return match.group(1), match.group(0)
    return None, ""


def is_fictional_content(content: str) -> bool:
    """检测是否为前瞻/虚构内容"""
    content_upper = content[:2000]  # 只检查前2000字符
    return any(kw in content_upper for kw in FICTIONAL_KEYWORDS)


def check_file(file_path: Path, now: datetime) -> List[FreshnessIssue]:
    issues = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return issues

    rel_path = str(file_path).replace("\\", "/")

    # 检查最后更新日期
    last_date, matched_line = extract_date_from_content(content)
    if last_date:
        age_days = (now - last_date).days
        if age_days > 365:
            issues.append(FreshnessIssue(
                rel_path, "长期未更新",
                f"最后更新: {last_date.date()} ({age_days} 天前)",
                "🔴 P0" if age_days > 730 else "🟠 P1"
            ))
        elif age_days > 180:
            issues.append(FreshnessIssue(
                rel_path, "中期未更新",
                f"最后更新: {last_date.date()} ({age_days} 天前)",
                "🟡 P2"
            ))
    else:
        # 核心目录缺少更新日期标记
        issues.append(FreshnessIssue(
            rel_path, "缺少更新日期标记",
            "文档未包含 '最后更新' 或 '最后核实日期' 字段",
            "🟡 P2"
        ))

    # 检查前瞻内容的预计发布日期是否已过期
    if is_fictional_content(content):
        target_date, matched = extract_target_date(content)
        if target_date:
            # 简单解析 Q 季度
            q_match = re.match(r"(\d{4}) Q(\d+)", target_date)
            if q_match:
                year, quarter = int(q_match.group(1)), int(q_match.group(2))
                # 季度末月份
                quarter_end_month = quarter * 3
                target = datetime(year, quarter_end_month, 1) + timedelta(days=31)
                target = target.replace(day=1) - timedelta(days=1)
                if now > target:
                    issues.append(FreshnessIssue(
                        rel_path, "前瞻日期已过期",
                        f"预计发布时间 {target_date} 已过期，需核实最新状态",
                        "🟠 P1"
                    ))
            else:
                try:
                    target = parse_date(target_date)
                    if now > target:
                        issues.append(FreshnessIssue(
                            rel_path, "前瞻日期已过期",
                            f"预计发布时间 {target_date} 已过期，需核实最新状态",
                            "🟠 P1"
                        ))
                except ValueError:
                    pass

    return issues


def scan_project(root_dir: Path) -> Tuple[List[FreshnessIssue], int, int]:
    now = datetime.now()
    all_issues = []
    total_files = 0
    checked_files = 0

    for dir_name in CORE_DIRS:
        target_dir = root_dir / dir_name
        if not target_dir.exists():
            continue
        for md_file in target_dir.rglob("*.md"):
            total_files += 1
            # 检查是否在跳过目录中
            parts = md_file.parts
            if any(skip in parts for skip in SKIP_DIRS):
                continue
            checked_files += 1
            issues = check_file(md_file, now)
            all_issues.extend(issues)

    return all_issues, total_files, checked_files


def generate_report(issues: List[FreshnessIssue], total_files: int, checked_files: int) -> str:
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# 文档新鲜度检查报告 (Document Freshness Report)",
        "",
        f"> **生成时间**: {now_str}",
        f"> **扫描范围**: Struct/ Knowledge/ Flink/ en/ formal-methods/",
        f"> **扫描文件数**: {checked_files} / {total_files} (核心目录)",
        f"> **发现问题数**: {len(issues)}",
        "",
        "## 统计概览",
        "",
        "| 严重等级 | 数量 | 说明 |",
        "|:--------:|:----:|------|",
    ]

    severity_counts = {"🔴 P0": 0, "🟠 P1": 0, "🟡 P2": 0}
    for issue in issues:
        severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1

    for sev, count in severity_counts.items():
        desc = {"🔴 P0": "严重：超过2年未更新或前瞻性日期严重过期", "🟠 P1": "重要：超过1年未更新或前瞻性日期过期", "🟡 P2": "一般：超过6个月未更新或缺少日期标记"}.get(sev, "")
        lines.append(f"| {sev} | {count} | {desc} |")

    lines.extend([
        "",
        "## 问题清单",
        "",
        "| 文件路径 | 问题类型 | 详情 | 等级 |",
        "|----------|----------|------|:----:|",
    ])

    # 按严重等级排序
    sorted_issues = sorted(issues, key=lambda x: ({"🔴 P0": 0, "🟠 P1": 1, "🟡 P2": 2}.get(x.severity, 3)))
    for issue in sorted_issues:
        lines.append(f"| `{issue.file_path}` | {issue.issue_type} | {issue.detail} | {issue.severity} |")

    lines.extend([
        "",
        "## 维护建议",
        "",
        "1. **🔴 P0 问题**：优先处理，建议 7 天内更新或归档",
        "2. **🟠 P1 问题**：计划处理，建议 30 天内核实并更新",
        "3. **🟡 P2 问题**：定期巡检，建议下次内容迭代时处理",
        "4. 所有更新完成后，请在文档顶部更新 `> **最后更新**: YYYY-MM-DD` 字段",
        "",
        "---",
        "*本报告由 doc-freshness-checker.py 自动生成*",
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="文档新鲜度检查器")
    parser.add_argument("--root", default=".", help="项目根目录")
    parser.add_argument("--output", default="FRESHNESS-REPORT.md", help="输出报告路径")
    args = parser.parse_args()

    root_dir = Path(args.root).resolve()
    if not root_dir.exists():
        print(f"错误: 根目录不存在: {root_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"开始扫描: {root_dir}")
    issues, total_files, checked_files = scan_project(root_dir)
    print(f"扫描完成: {checked_files} 个文件，发现 {len(issues)} 个问题")

    report = generate_report(issues, total_files, checked_files)
    output_path = root_dir / args.output
    output_path.write_text(report, encoding="utf-8")
    print(f"报告已生成: {output_path}")

    # 如果有 P0 问题，返回非零退出码（用于 CI）
    p0_count = sum(1 for i in issues if i.severity == "🔴 P0")
    if p0_count > 0:
        print(f"警告: 存在 {p0_count} 个 P0 级别问题", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
