#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
形式化元素唯一性检查脚本
验证所有Markdown文件中定理/定义/引理/命题/推论编号的唯一性和格式规范
"""

import os
import re
import json
from collections import defaultdict
from pathlib import Path
from datetime import datetime

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 三大输出目录
TARGET_DIRS = ['Struct', 'Knowledge', 'Flink']

# 形式化元素的正则表达式模式
# 支持格式: Thm-S-01-01, Def-K-12-34, Lemma-F-99-99, Prop-S-01-01, Cor-K-01-01
FORMAL_ELEMENT_PATTERN = re.compile(
    r'\b(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d{2})-(\d{2,3})\b'
)

# 在Markdown表格中引用的模式（如定理注册表中的引用）
TABLE_REF_PATTERN = re.compile(
    r'\|?\s*(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d{2})-(\d{2,3})\s*\|'
)

# 元素类型映射
ELEMENT_TYPES = {
    'Thm': '定理',
    'Def': '定义',
    'Lemma': '引理',
    'Prop': '命题',
    'Cor': '推论'
}

# 阶段映射
STAGE_MAP = {
    'S': 'Struct',
    'K': 'Knowledge',
    'F': 'Flink'
}


def get_all_md_files():
    """获取所有目标目录下的Markdown文件"""
    md_files = []
    for dir_name in TARGET_DIRS:
        dir_path = PROJECT_ROOT / dir_name
        if dir_path.exists():
            for root, _, files in os.walk(dir_path):
                for file in files:
                    if file.endswith('.md'):
                        md_files.append(os.path.join(root, file))
    return md_files


def extract_formal_elements(file_path):
    """从文件中提取所有形式化元素编号"""
    elements = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                # 查找所有匹配的形式化元素
                matches = FORMAL_ELEMENT_PATTERN.findall(line)
                for match in matches:
                    elem_type, stage, doc_num, seq_num = match
                    elements.append({
                        'type': elem_type,
                        'stage': stage,
                        'doc_num': doc_num,
                        'seq_num': seq_num,
                        'full_id': f"{elem_type}-{stage}-{doc_num}-{seq_num}",
                        'file': os.path.relpath(file_path, PROJECT_ROOT),
                        'line': line_num,
                        'context': line.strip()[:200]
                    })
    except Exception as e:
        print(f"  警告: 无法读取文件 {file_path}: {e}")
    
    return elements


def check_uniqueness(all_elements):
    """检查元素编号的唯一性"""
    duplicates = defaultdict(list)
    unique_elements = {}
    
    for elem in all_elements:
        elem_id = elem['full_id']
        if elem_id in unique_elements:
            duplicates[elem_id].append(elem)
            if len(duplicates[elem_id]) == 1:
                duplicates[elem_id].append(unique_elements[elem_id])
        else:
            unique_elements[elem_id] = elem
    
    return duplicates


def check_format_validity(all_elements):
    """检查编号格式规范性"""
    invalid_formats = []
    
    for elem in all_elements:
        issues = []
        
        # 检查文档序号范围 (01-99)
        doc_num = int(elem['doc_num'])
        if doc_num < 1 or doc_num > 99:
            issues.append(f"文档序号{elem['doc_num']}超出范围(01-99)")
        
        # 检查顺序号范围 (01-999)
        seq_num = int(elem['seq_num'])
        if seq_num < 1 or seq_num > 999:
            issues.append(f"顺序号{elem['seq_num']}超出范围(01-999)")
        
        # 检查阶段标识
        if elem['stage'] not in ['S', 'K', 'F']:
            issues.append(f"无效的阶段标识'{elem['stage']}'")
        
        # 检查类型标识
        if elem['type'] not in ELEMENT_TYPES:
            issues.append(f"无效的类型标识'{elem['type']}'")
        
        if issues:
            elem['issues'] = issues
            invalid_formats.append(elem)
    
    return invalid_formats


def check_continuity(elements_by_type_stage):
    """检查编号连续性"""
    continuity_issues = []
    
    for (elem_type, stage), elements in elements_by_type_stage.items():
        # 按文档序号和顺序号排序
        sorted_elems = sorted(elements, key=lambda x: (x['doc_num'], int(x['seq_num'])))
        
        # 按文档分组检查连续性
        by_doc = defaultdict(list)
        for elem in sorted_elems:
            by_doc[elem['doc_num']].append(int(elem['seq_num']))
        
        for doc_num, seq_nums in by_doc.items():
            sorted_seqs = sorted(set(seq_nums))
            if len(sorted_seqs) > 1:
                # 检查是否有空缺
                for i in range(len(sorted_seqs) - 1):
                    if sorted_seqs[i+1] - sorted_seqs[i] > 1:
                        continuity_issues.append({
                            'type': elem_type,
                            'stage': stage,
                            'doc_num': doc_num,
                            'gap_start': sorted_seqs[i],
                            'gap_end': sorted_seqs[i+1],
                            'message': f"{elem_type}-{stage}-{doc_num}: 序号空缺 {sorted_seqs[i]} -> {sorted_seqs[i+1]}"
                        })
            
            # 检查重复
            from collections import Counter
            counts = Counter(seq_nums)
            for seq, count in counts.items():
                if count > 1:
                    continuity_issues.append({
                        'type': elem_type,
                        'stage': stage,
                        'doc_num': doc_num,
                        'seq_num': seq,
                        'count': count,
                        'message': f"{elem_type}-{stage}-{doc_num}-{seq:02d}: 在同一文档中出现{count}次"
                    })
    
    return continuity_issues


def generate_statistics(all_elements):
    """生成统计信息"""
    stats = {
        'total': len(all_elements),
        'by_type': defaultdict(int),
        'by_stage': defaultdict(int),
        'by_doc': defaultdict(int),
        'type_stage_combo': defaultdict(int)
    }
    
    for elem in all_elements:
        stats['by_type'][elem['type']] += 1
        stats['by_stage'][elem['stage']] += 1
        doc_key = f"{elem['type']}-{elem['stage']}-{elem['doc_num']}"
        stats['by_doc'][doc_key] += 1
        combo_key = f"{elem['type']}-{elem['stage']}"
        stats['type_stage_combo'][combo_key] += 1
    
    return stats


def generate_report(all_elements, duplicates, invalid_formats, continuity_issues, stats):
    """生成检查报告"""
    report_lines = []
    report_lines.append("# 形式化元素唯一性检查报告")
    report_lines.append("")
    report_lines.append(f"> **检查时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"> **检查范围**: Struct/ | Knowledge/ | Flink/")
    report_lines.append(f"> **扫描文件**: {len(set(e['file'] for e in all_elements))} 个 Markdown 文件")
    report_lines.append("")
    
    # 执行摘要
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## 执行摘要")
    report_lines.append("")
    
    has_issues = bool(duplicates or invalid_formats or continuity_issues)
    if has_issues:
        report_lines.append("⚠️ **检查发现问题，需要修复**")
    else:
        report_lines.append("✅ **所有形式化元素编号唯一且格式规范**")
    
    report_lines.append("")
    report_lines.append(f"- **总元素数**: {stats['total']}")
    report_lines.append(f"- **重复编号**: {len(duplicates)} 个")
    report_lines.append(f"- **格式不规范**: {len(invalid_formats)} 个")
    report_lines.append(f"- **连续性/重复问题**: {len(continuity_issues)} 个")
    report_lines.append("")
    
    # 按类型统计
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## 1. 各类形式化元素统计")
    report_lines.append("")
    report_lines.append("### 1.1 按类型统计")
    report_lines.append("")
    report_lines.append("| 类型 | 中文名 | 数量 | 占比 |")
    report_lines.append("|------|--------|------|------|")
    
    for type_key, type_name in ELEMENT_TYPES.items():
        count = stats['by_type'].get(type_key, 0)
        percentage = (count / stats['total'] * 100) if stats['total'] > 0 else 0
        report_lines.append(f"| {type_key} | {type_name} | {count} | {percentage:.1f}% |")
    
    report_lines.append("")
    report_lines.append("### 1.2 按阶段统计")
    report_lines.append("")
    report_lines.append("| 阶段 | 目录 | 数量 | 占比 |")
    report_lines.append("|------|------|------|------|")
    
    for stage_key, stage_name in STAGE_MAP.items():
        count = stats['by_stage'].get(stage_key, 0)
        percentage = (count / stats['total'] * 100) if stats['total'] > 0 else 0
        report_lines.append(f"| {stage_key} | {stage_name} | {count} | {percentage:.1f}% |")
    
    report_lines.append("")
    report_lines.append("### 1.3 类型-阶段组合统计")
    report_lines.append("")
    report_lines.append("| 组合 | 数量 | 占比 |")
    report_lines.append("|------|------|------|")
    
    for combo, count in sorted(stats['type_stage_combo'].items()):
        percentage = (count / stats['total'] * 100) if stats['total'] > 0 else 0
        report_lines.append(f"| {combo} | {count} | {percentage:.1f}% |")
    
    # 重复编号列表
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## 2. 重复编号列表")
    report_lines.append("")
    
    if duplicates:
        report_lines.append(f"发现 **{len(duplicates)}** 个重复编号：")
        report_lines.append("")
        report_lines.append("| 重复编号 | 出现次数 | 出现位置 |")
        report_lines.append("|----------|----------|----------|")
        
        for elem_id, elems in sorted(duplicates.items()):
            locations = [f"{e['file']}:{e['line']}" for e in elems]
            report_lines.append(f"| {elem_id} | {len(elems)} | {'<br>'.join(locations[:3])} |")
        
        report_lines.append("")
        report_lines.append("### 重复详情")
        report_lines.append("")
        
        for elem_id, elems in sorted(duplicates.items()):
            report_lines.append(f"#### {elem_id}")
            report_lines.append("")
            for e in elems:
                report_lines.append(f"- 文件: `{e['file']}` (第{e['line']}行)")
                report_lines.append(f"  上下文: `{e['context'][:100]}...`")
            report_lines.append("")
    else:
        report_lines.append("✅ **未发现重复编号**")
    
    # 格式不规范列表
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## 3. 格式不规范列表")
    report_lines.append("")
    
    if invalid_formats:
        report_lines.append(f"发现 **{len(invalid_formats)}** 个格式不规范元素：")
        report_lines.append("")
        report_lines.append("| 编号 | 问题描述 | 文件 | 行号 |")
        report_lines.append("|------|----------|------|------|")
        
        for elem in invalid_formats:
            issues_str = '; '.join(elem['issues'])
            report_lines.append(f"| {elem['full_id']} | {issues_str} | {elem['file']} | {elem['line']} |")
    else:
        report_lines.append("✅ **所有元素格式规范**")
    
    # 连续性问题
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## 4. 编号连续性与重复问题")
    report_lines.append("")
    
    if continuity_issues:
        report_lines.append(f"发现 **{len(continuity_issues)}** 个连续性问题：")
        report_lines.append("")
        report_lines.append("| 问题类型 | 详细信息 |")
        report_lines.append("|----------|----------|")
        
        for issue in continuity_issues:
            report_lines.append(f"| {'空缺' if 'gap' in issue else '重复'} | {issue['message']} |")
    else:
        report_lines.append("✅ **编号连续，无重复**")
    
    # 修复建议
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## 5. 建议修复方案")
    report_lines.append("")
    
    if duplicates:
        report_lines.append("### 5.1 重复编号修复")
        report_lines.append("")
        report_lines.append("对于重复编号，建议：")
        report_lines.append("1. 检查是否为同一元素在不同位置的引用（正常情况，保留）")
        report_lines.append("2. 如果是不同元素使用了相同编号，需要重新分配其中一个的编号")
        report_lines.append("3. 更新 THEOREM-REGISTRY.md 注册表")
        report_lines.append("")
    
    if invalid_formats:
        report_lines.append("### 5.2 格式规范修复")
        report_lines.append("")
        report_lines.append("对于格式不规范的元素：")
        report_lines.append("1. 确保文档序号在 01-99 范围内")
        report_lines.append("2. 确保顺序号在 01-999 范围内")
        report_lines.append("3. 使用正确的阶段标识 (S/K/F)")
        report_lines.append("4. 使用正确的类型标识 (Thm/Def/Lemma/Prop/Cor)")
        report_lines.append("")
    
    if continuity_issues:
        report_lines.append("### 5.3 连续性优化")
        report_lines.append("")
        report_lines.append("对于编号空缺：")
        report_lines.append("1. 检查是否有遗漏的形式化元素未编号")
        report_lines.append("2. 考虑是否需要填补空缺以保持连续性")
        report_lines.append("")
    
    if not has_issues:
        report_lines.append("✅ **无需修复，所有检查通过！**")
    
    # 附录：所有元素列表
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## 附录：完整元素清单")
    report_lines.append("")
    report_lines.append(f"共 {stats['total']} 个形式化元素，按类型-阶段-文档排序：")
    report_lines.append("")
    
    # 排序并显示
    sorted_elements = sorted(all_elements, key=lambda x: (x['type'], x['stage'], x['doc_num'], int(x['seq_num'])))
    
    current_type_stage = None
    for elem in sorted_elements:
        combo = f"{elem['type']}-{elem['stage']}"
        if combo != current_type_stage:
            if current_type_stage:
                report_lines.append("")
            current_type_stage = combo
            type_name = ELEMENT_TYPES.get(elem['type'], elem['type'])
            stage_name = STAGE_MAP.get(elem['stage'], elem['stage'])
            report_lines.append(f"### {type_name} ({stage_name})")
            report_lines.append("")
            report_lines.append("| 编号 | 文件 | 行号 |")
            report_lines.append("|------|------|------|")
        
        report_lines.append(f"| {elem['full_id']} | {elem['file']} | {elem['line']} |")
    
    return '\n'.join(report_lines)


def main():
    """主函数"""
    print("=" * 60)
    print("形式化元素唯一性检查")
    print("=" * 60)
    print()
    
    # 获取所有Markdown文件
    print("[1/6] 扫描Markdown文件...")
    md_files = get_all_md_files()
    print(f"      找到 {len(md_files)} 个Markdown文件")
    
    # 提取所有形式化元素
    print("[2/6] 提取形式化元素...")
    all_elements = []
    for file_path in md_files:
        elements = extract_formal_elements(file_path)
        all_elements.extend(elements)
    print(f"      提取到 {len(all_elements)} 个形式化元素")
    
    # 检查唯一性
    print("[3/6] 检查编号唯一性...")
    duplicates = check_uniqueness(all_elements)
    print(f"      发现 {len(duplicates)} 个重复编号")
    
    # 检查格式
    print("[4/6] 检查格式规范性...")
    invalid_formats = check_format_validity(all_elements)
    print(f"      发现 {len(invalid_formats)} 个格式不规范")
    
    # 检查连续性
    print("[5/6] 检查编号连续性...")
    elements_by_type_stage = defaultdict(list)
    for elem in all_elements:
        key = (elem['type'], elem['stage'])
        elements_by_type_stage[key].append(elem)
    continuity_issues = check_continuity(elements_by_type_stage)
    print(f"      发现 {len(continuity_issues)} 个连续性问题")
    
    # 生成统计
    print("[6/6] 生成统计信息...")
    stats = generate_statistics(all_elements)
    
    # 生成报告
    report = generate_report(all_elements, duplicates, invalid_formats, continuity_issues, stats)
    
    # 保存报告
    report_path = PROJECT_ROOT / 'FORMAL-ELEMENT-UNIQUENESS-REPORT.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print()
    print("=" * 60)
    print("检查完成！")
    print(f"报告已保存至: {report_path}")
    print()
    print(f"统计摘要:")
    print(f"  - 总元素数: {stats['total']}")
    print(f"  - 重复编号: {len(duplicates)} 个")
    print(f"  - 格式问题: {len(invalid_formats)} 个")
    print(f"  - 连续性问题: {len(continuity_issues)} 个")
    print("=" * 60)
    
    # 保存JSON格式的详细数据
    json_data = {
        'timestamp': datetime.now().isoformat(),
        'statistics': {
            'total': stats['total'],
            'by_type': dict(stats['by_type']),
            'by_stage': dict(stats['by_stage']),
        },
        'duplicates': {
            elem_id: [{k: v for k, v in e.items() if k != 'context'} for e in elems]
            for elem_id, elems in duplicates.items()
        },
        'invalid_formats': invalid_formats,
        'continuity_issues': continuity_issues,
        'all_elements': [{k: v for k, v in e.items() if k != 'context'} for e in all_elements]
    }
    
    json_path = PROJECT_ROOT / 'formal-element-check-result.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"JSON数据已保存至: {json_path}")


if __name__ == '__main__':
    main()
