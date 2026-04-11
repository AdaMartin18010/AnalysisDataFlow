#!/usr/bin/env python3
"""
质量评分计算器 - 计算文档质量分数

用法:
    python quality-score-calculator.py --reports-dir reports --output score-report.md
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


def calculate_score(report_data: Dict[str, Any], weights: Dict[str, float]) -> float:
    """计算加权分数"""
    score = 100.0
    
    for metric, weight in weights.items():
        if metric in report_data:
            value = report_data[metric]
            if isinstance(value, (int, float)):
                # 扣分制
                score -= value * weight
    
    return max(0, min(100, score))


def load_report(report_path: Path) -> Dict[str, Any]:
    """加载报告文件"""
    try:
        if report_path.suffix == '.json':
            return json.loads(report_path.read_text())
    except Exception as e:
        print(f"Error loading {report_path}: {e}")
    return {}


def generate_score_report(reports_dir: Path, output_path: Path):
    """生成质量评分报告"""
    
    scores = {}
    
    # 定义评分权重
    weights = {
        'cross-ref': {
            'broken_refs': 2.0,
            'missing_refs': 1.5
        },
        'template': {
            'missing_sections': 0.5
        },
        'mermaid': {
            'syntax_errors': 1.0
        },
        'links': {
            'broken_links': 2.0
        },
        'theorems': {
            'duplicates': 5.0
        }
    }
    
    # 加载各个报告
    reports = {
        'cross-ref': reports_dir / 'cross-ref-validation.json',
        'template': reports_dir / 'template-validation.json',
        'mermaid': reports_dir / 'mermaid-syntax-report.json',
        'links': reports_dir / 'internal-link-report.json',
        'theorems': reports_dir / 'theorem-uniqueness-report.json'
    }
    
    total_score = 100.0
    details = []
    
    for name, path in reports.items():
        if path.exists():
            data = load_report(path)
            summary = data.get('summary', data)
            
            # 计算子分数
            sub_score = calculate_score(summary, weights.get(name, {}))
            scores[name] = sub_score
            
            details.append({
                'name': name,
                'score': sub_score,
                'summary': summary
            })
            
            # 更新总分
            total_score = min(total_score, sub_score)
    
    # 生成报告
    grade = 'A' if total_score >= 90 else 'B' if total_score >= 80 else 'C' if total_score >= 70 else 'D'
    
    report_lines = [
        f"# Quality Score Report",
        f"",
        f"**Generated**: {datetime.now().isoformat()}",
        f"",
        f"## Overall Score",
        f"",
        f"```",
        f"Score: {total_score:.1f}/100",
        f"Grade: {grade}",
        f"```",
        f"",
        f"## Component Scores",
        f"",
        "| Component | Score | Status |",
        "|-----------|-------|--------|",
    ]
    
    for detail in details:
        status = '✅' if detail['score'] >= 90 else '⚠️' if detail['score'] >= 70 else '❌'
        report_lines.append(f"| {detail['name']} | {detail['score']:.1f} | {status} |")
    
    report_lines.extend([
        f"",
        f"## Score Criteria",
        f"",
        f"- **A (90-100)**: Excellent quality",
        f"- **B (80-89)**: Good quality",
        f"- **C (70-79)**: Acceptable quality",
        f"- **D (<70)**: Needs improvement",
        f"",
    ])
    
    output_path.write_text('\n'.join(report_lines))
    print(f"Quality score report generated: {output_path}")
    print(f"Overall score: {total_score:.1f} ({grade})")


def main():
    parser = argparse.ArgumentParser(description='Calculate quality scores from reports')
    parser.add_argument('--reports-dir', type=Path, default=Path('reports'),
                       help='Directory containing report files')
    parser.add_argument('--output', type=Path, default=Path('reports/quality-score-report.md'),
                       help='Output path for score report')
    
    args = parser.parse_args()
    
    generate_score_report(args.reports_dir, args.output)


if __name__ == '__main__':
    main()
