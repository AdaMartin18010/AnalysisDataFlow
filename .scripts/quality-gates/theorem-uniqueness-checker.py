#!/usr/bin/env python3
"""
定理编号唯一性检查器
检查项目中所有定理/定义/引理/命题/推论编号的唯一性

用法:
    python theorem-uniqueness-checker.py [--strict] [--fix]

选项:
    --strict  严格模式，发现重复时报错退出
    --fix     尝试自动修复（添加后缀区分重复项）
"""

import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime


# 定理编号模式（根据AGENTS.md规范）
THEOREM_PATTERNS = {
    'Thm': re.compile(r'Thm-[SKF]-\d{2}-\d{2}'),
    'Def': re.compile(r'Def-[SKF]-\d{2}-\d{2}'),
    'Lemma': re.compile(r'Lemma-[SKF]-\d{2}-\d{2}'),
    'Prop': re.compile(r'Prop-[SKF]-\d{2}-\d{2}'),
    'Cor': re.compile(r'Cor-[SKF]-\d{2}-\d{2}')
}


def scan_document(file_path: Path) -> dict:
    """扫描单个文档中的所有定理编号"""
    results = defaultdict(list)
    
    try:
        content = file_path.read_text(encoding='utf-8')
        rel_path = str(file_path.relative_to('.')).replace('\\', '/')
        
        for thm_type, pattern in THEOREM_PATTERNS.items():
            matches = pattern.findall(content)
            for match in matches:
                results[match].append({
                    'file': rel_path,
                    'type': thm_type,
                    'context': extract_context(content, match)
                })
    except Exception as e:
        print(f"Warning: Could not process {file_path}: {e}", file=sys.stderr)
    
    return results


def extract_context(content: str, theorem_id: str, context_lines: int = 2) -> str:
    """提取定理编号周围的上下文"""
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if theorem_id in line:
            start = max(0, i - context_lines)
            end = min(len(lines), i + context_lines + 1)
            return '\n'.join(lines[start:end])
    return ""


def find_duplicates(all_theorems: dict) -> list:
    """查找重复的定理编号"""
    duplicates = []
    
    for theorem_id, occurrences in all_theorems.items():
        if len(occurrences) > 1:
            duplicates.append({
                'id': theorem_id,
                'count': len(occurrences),
                'occurrences': occurrences
            })
    
    return duplicates


def check_sequential_gaps(all_theorems: dict) -> list:
    """检查序号是否有跳号"""
    gaps = []
    
    # 按类型和阶段分组
    grouped = defaultdict(lambda: defaultdict(list))
    for theorem_id in all_theorems.keys():
        parts = theorem_id.split('-')
        if len(parts) >= 3:
            thm_type = parts[0]
            stage = parts[1]
            doc_num = int(parts[2])
            seq_num = int(parts[3]) if len(parts) > 3 else 0
            grouped[thm_type][(stage, doc_num)].append(seq_num)
    
    # 检查每组是否有跳号
    for thm_type, docs in grouped.items():
        for (stage, doc_num), seq_nums in docs.items():
            seq_nums = sorted(set(seq_nums))
            if len(seq_nums) > 1:
                for i in range(len(seq_nums) - 1):
                    if seq_nums[i + 1] - seq_nums[i] > 1:
                        gaps.append({
                            'type': thm_type,
                            'stage': stage,
                            'doc': doc_num,
                            'gap': f"{seq_nums[i]} -> {seq_nums[i + 1]}"
                        })
    
    return gaps


def generate_report(stats: dict, duplicates: list, gaps: list, output_path: Path = None):
    """生成检查报告"""
    lines = [
        "# Theorem Uniqueness Check Report",
        "",
        f"**Generated**: {datetime.now().isoformat()}",
        "",
        "## Summary",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Total Theorems | {stats['total']} |",
        f"| Unique IDs | {stats['unique']} |",
        f"| Duplicates | {len(duplicates)} |",
        f"| Sequential Gaps | {len(gaps)} |",
        ""
    ]
    
    if duplicates:
        lines.extend([
            "## ❌ Duplicate Theorem IDs",
            "",
            "| ID | Count | Files |",
            "|----|-------|-------|"
        ])
        
        for dup in sorted(duplicates, key=lambda x: x['id']):
            files = ', '.join(set(occ['file'] for occ in dup['occurrences']))
            lines.append(f"| `{dup['id']}` | {dup['count']} | {files} |")
        
        lines.append("")
        
        # 详细上下文
        lines.extend([
            "### Detailed Context",
            ""
        ])
        
        for dup in sorted(duplicates, key=lambda x: x['id']):
            lines.extend([
                f"#### `{dup['id']}`",
                ""
            ])
            for occ in dup['occurrences']:
                lines.extend([
                    f"**File**: `{occ['file']}`",
                    "",
                    "```markdown",
                    occ['context'],
                    "```",
                    ""
                ])
    
    if gaps:
        lines.extend([
            "## ⚠️ Sequential Gaps",
            "",
            "| Type | Stage | Doc | Gap |",
            "|------|-------|-----|-----|"
        ])
        
        for gap in gaps:
            lines.append(
                f"| {gap['type']} | {gap['stage']} | {gap['doc']} | {gap['gap']} |"
            )
        
        lines.append("")
    
    lines.extend([
        "## Recommendations",
        ""
    ])
    
    if duplicates:
        lines.extend([
            "### High Priority",
            "",
            f"1. Resolve {len(duplicates)} duplicate theorem IDs",
            "2. Ensure each theorem ID is unique across the project",
            "3. Update THEOREM-REGISTRY.md to reflect correct assignments",
            ""
        ])
    else:
        lines.append("✅ All theorem IDs are unique!")
        lines.append("")
    
    if gaps:
        lines.extend([
            "### Medium Priority",
            "",
            f"1. Review {len(gaps)} sequential gaps",
            "2. Consider renumbering to maintain sequential order",
            ""
        ])
    
    lines.append("---")
    lines.append("")
    lines.append("*This report was generated by theorem-uniqueness-checker.py*")
    
    report = '\n'.join(lines)
    
    if output_path:
        output_path.write_text(report, encoding='utf-8')
    
    return report


def main():
    parser = argparse.ArgumentParser(
        description='Check theorem ID uniqueness across the project'
    )
    parser.add_argument(
        '--strict', action='store_true',
        help='Exit with error code if duplicates found'
    )
    parser.add_argument(
        '--fix', action='store_true',
        help='Attempt to auto-fix duplicates (not implemented)'
    )
    parser.add_argument(
        '--output', '-o', type=str,
        default='reports/theorem-uniqueness-report.md',
        help='Output report path'
    )
    parser.add_argument(
        '--dirs', nargs='+',
        default=['Struct', 'Knowledge', 'Flink'],
        help='Directories to scan'
    )
    
    args = parser.parse_args()
    
    print("🔍 Scanning for theorem ID uniqueness...")
    
    # 收集所有定理
    all_theorems = defaultdict(list)
    files_scanned = 0
    
    for directory in args.dirs:
        dir_path = Path(directory)
        if not dir_path.exists():
            print(f"Warning: Directory {directory} not found, skipping")
            continue
        
        for md_file in dir_path.rglob('*.md'):
            results = scan_document(md_file)
            for theorem_id, occurrences in results.items():
                all_theorems[theorem_id].extend(occurrences)
            files_scanned += 1
    
    # 统计
    stats = {
        'total': sum(len(occ) for occ in all_theorems.values()),
        'unique': len(all_theorems)
    }
    
    print(f"   Scanned {files_scanned} files")
    print(f"   Found {stats['total']} theorem references ({stats['unique']} unique IDs)")
    
    # 查找重复
    duplicates = find_duplicates(all_theorems)
    
    if duplicates:
        print(f"\n❌ Found {len(duplicates)} duplicate theorem IDs:")
        for dup in duplicates:
            print(f"   - {dup['id']}: {dup['count']} occurrences")
    else:
        print("\n✅ All theorem IDs are unique")
    
    # 检查跳号
    gaps = check_sequential_gaps(all_theorems)
    
    if gaps:
        print(f"\n⚠️ Found {len(gaps)} sequential gaps")
    
    # 生成报告
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    report = generate_report(stats, duplicates, gaps, output_path)
    print(f"\n📄 Report saved to: {output_path}")
    
    # 严格模式退出
    if args.strict and duplicates:
        sys.exit(1)
    
    sys.exit(0)


if __name__ == '__main__':
    main()
