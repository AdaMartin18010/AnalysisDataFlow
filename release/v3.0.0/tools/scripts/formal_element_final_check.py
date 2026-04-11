#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
形式化元素最终检查脚本 - 综合检查唯一性、格式和连续性
"""

import os
import re
import json
from collections import defaultdict
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
TARGET_DIRS = ['Struct', 'Knowledge', 'Flink']

# 形式化元素的正则表达式模式
FORMAL_ELEMENT_PATTERN = re.compile(
    r'\b(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d{2})-(\d{2,3})\b'
)

ELEMENT_TYPES = {
    'Thm': '定理',
    'Def': '定义',
    'Lemma': '引理',
    'Prop': '命题',
    'Cor': '推论'
}

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
    """从文件中提取所有形式化元素"""
    elements = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
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
                        'context': line.strip()[:150]
                    })
    except Exception as e:
        print(f"  警告: 无法读取文件 {file_path}: {e}")
    
    return elements


def analyze_uniqueness(elements):
    """分析唯一性"""
    # 按编号分组
    by_id = defaultdict(list)
    for elem in elements:
        by_id[elem['full_id']].append(elem)
    
    # 找出重复的（出现次数>1）
    duplicates = {k: v for k, v in by_id.items() if len(v) > 1}
    
    return duplicates


def analyze_continuity(elements):
    """分析编号连续性"""
    issues = []
    
    # 按类型-阶段-文档分组
    by_group = defaultdict(list)
    for elem in elements:
        key = (elem['type'], elem['stage'], elem['doc_num'])
        by_group[key].append(int(elem['seq_num']))
    
    for (elem_type, stage, doc_num), seq_nums in by_group.items():
        sorted_seqs = sorted(set(seq_nums))
        
        # 检查连续性
        if len(sorted_seqs) > 1:
            for i in range(len(sorted_seqs) - 1):
                if sorted_seqs[i+1] - sorted_seqs[i] > 1:
                    issues.append({
                        'type': 'gap',
                        'elem_type': elem_type,
                        'stage': stage,
                        'doc_num': doc_num,
                        'from': sorted_seqs[i],
                        'to': sorted_seqs[i+1],
                        'message': f"{elem_type}-{stage}-{doc_num}: 序号空缺 {sorted_seqs[i]} → {sorted_seqs[i+1]}"
                    })
        
        # 检查同一文档内的重复
        from collections import Counter
        counts = Counter(seq_nums)
        for seq, count in counts.items():
            if count > 1:
                issues.append({
                    'type': 'duplicate_in_doc',
                    'elem_type': elem_type,
                    'stage': stage,
                    'doc_num': doc_num,
                    'seq_num': seq,
                    'count': count,
                    'message': f"{elem_type}-{stage}-{doc_num}-{seq:02d}: 在同一文档中出现{count}次"
                })
    
    return issues


def check_format_issues(elements):
    """检查格式问题"""
    issues = []
    
    for elem in elements:
        # 检查文档序号
        doc_num = int(elem['doc_num'])
        if doc_num < 1 or doc_num > 99:
            issues.append({
                'elem_id': elem['full_id'],
                'issue': f"文档序号{elem['doc_num']}超出范围(01-99)",
                'file': elem['file'],
                'line': elem['line']
            })
        
        # 检查顺序号
        seq_num = int(elem['seq_num'])
        if seq_num < 1 or seq_num > 999:
            issues.append({
                'elem_id': elem['full_id'],
                'issue': f"顺序号{elem['seq_num']}超出范围(01-999)",
                'file': elem['file'],
                'line': elem['line']
            })
    
    return issues


def main():
    """主函数"""
    print("=" * 70)
    print("形式化元素唯一性检查 - 最终报告")
    print("=" * 70)
    print()
    
    # 获取所有Markdown文件
    print("[1/5] 扫描Markdown文件...")
    md_files = get_all_md_files()
    print(f"      找到 {len(md_files)} 个Markdown文件")
    
    # 提取所有形式化元素
    print("[2/5] 提取形式化元素...")
    all_elements = []
    for file_path in md_files:
        elements = extract_formal_elements(file_path)
        all_elements.extend(elements)
    
    print(f"      提取到 {len(all_elements)} 个形式化元素引用")
    
    # 统计唯一编号
    print("[3/5] 统计唯一编号...")
    unique_ids = set(e['full_id'] for e in all_elements)
    print(f"      唯一编号数: {len(unique_ids)}")
    
    # 按类型统计
    type_counts = defaultdict(int)
    stage_counts = defaultdict(int)
    for elem_id in unique_ids:
        parts = elem_id.split('-')
        if len(parts) >= 2:
            type_counts[parts[0]] += 1
            stage_counts[parts[1]] += 1
    
    # 分析重复
    print("[4/5] 分析重复编号...")
    duplicates = analyze_uniqueness(all_elements)
    print(f"      发现 {len(duplicates)} 个编号有重复出现")
    
    # 分析连续性
    print("[5/5] 分析编号连续性...")
    continuity_issues = analyze_continuity(all_elements)
    print(f"      发现 {len(continuity_issues)} 个连续性问题")
    
    # 检查格式
    format_issues = check_format_issues(all_elements)
    
    # 生成报告
    print()
    print("=" * 70)
    print("检查结果摘要")
    print("=" * 70)
    print()
    
    # 打印统计表格
    print("【按类型统计】")
    print(f"{'类型':<10} {'中文':<8} {'唯一编号':>10} {'占比':>8}")
    print("-" * 40)
    total = len(unique_ids)
    for type_key in ['Thm', 'Def', 'Lemma', 'Prop', 'Cor']:
        count = type_counts.get(type_key, 0)
        pct = (count / total * 100) if total > 0 else 0
        print(f"{type_key:<10} {ELEMENT_TYPES.get(type_key, type_key):<8} {count:>10} {pct:>7.1f}%")
    print("-" * 40)
    print(f"{'总计':<10} {'':8} {total:>10} {'100.0%':>8}")
    print()
    
    print("【按阶段统计】")
    print(f"{'阶段':<10} {'目录':<15} {'唯一编号':>10} {'占比':>8}")
    print("-" * 50)
    for stage_key in ['S', 'K', 'F']:
        count = stage_counts.get(stage_key, 0)
        pct = (count / total * 100) if total > 0 else 0
        print(f"{stage_key:<10} {STAGE_MAP.get(stage_key, stage_key):<15} {count:>10} {pct:>7.1f}%")
    print("-" * 50)
    print(f"{'总计':<10} {'':15} {total:>10} {'100.0%':>8}")
    print()
    
    # 与注册表对比
    print("【与THEOREM-REGISTRY.md对比】")
    registry_stats = {
        'Thm': 1910,
        'Def': 4564,
        'Lemma': 1568,
        'Prop': 1194,
        'Cor': 121
    }
    total_registry = sum(registry_stats.values())
    
    print(f"{'类型':<10} {'扫描结果':>10} {'注册表':>10} {'差异':>10} {'覆盖率':>10}")
    print("-" * 55)
    for type_key in ['Thm', 'Def', 'Lemma', 'Prop', 'Cor']:
        scanned = type_counts.get(type_key, 0)
        registry = registry_stats[type_key]
        diff = scanned - registry
        coverage = (scanned / registry * 100) if registry > 0 else 0
        print(f"{ELEMENT_TYPES[type_key]:<10} {scanned:>10} {registry:>10} {diff:>+10} {coverage:>9.1f}%")
    print("-" * 55)
    coverage_total = (total / total_registry * 100) if total_registry > 0 else 0
    print(f"{'总计':<10} {total:>10} {total_registry:>10} {total - total_registry:>+10} {coverage_total:>9.1f}%")
    print()
    
    # 问题汇总
    print("【问题汇总】")
    print(f"  ✓ 唯一编号: {len(unique_ids)} 个")
    print(f"  ✓ 总出现次数: {len(all_elements)} 次")
    print(f"  ⚠ 重复出现: {len(duplicates)} 个编号有重复")
    print(f"  ⚠ 格式问题: {len(format_issues)} 个")
    print(f"  ⚠ 连续性问题: {len(continuity_issues)} 个")
    print()
    
    # 重复分析
    if duplicates:
        dup_counts = defaultdict(int)
        for elem_id, elems in duplicates.items():
            dup_counts[len(elems)] += 1
        
        print("【重复次数分布】")
        for count in sorted(dup_counts.keys()):
            print(f"  出现 {count:>2} 次的编号: {dup_counts[count]:>4} 个")
        print()
    
    # 格式问题详情
    if format_issues:
        print("【格式问题详情】")
        for issue in format_issues[:10]:
            print(f"  {issue['elem_id']}: {issue['issue']}")
        if len(format_issues) > 10:
            print(f"  ... 还有 {len(format_issues) - 10} 个")
        print()
    
    # 生成Markdown报告
    report_lines = []
    report_lines.append("# 形式化元素唯一性检查报告")
    report_lines.append("")
    report_lines.append(f"> **检查时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"> **检查范围**: Struct/ | Knowledge/ | Flink/ 三大目录")
    report_lines.append(f"> **扫描文件**: {len(md_files)} 个 Markdown 文件")
    report_lines.append("")
    
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## 执行摘要")
    report_lines.append("")
    
    if duplicates or format_issues or continuity_issues:
        report_lines.append("⚠️ **检查发现以下问题**：")
        report_lines.append("")
        if duplicates:
            report_lines.append(f"- **重复编号**: {len(duplicates)} 个编号在多处出现")
        if format_issues:
            report_lines.append(f"- **格式问题**: {len(format_issues)} 个元素格式不规范")
        if continuity_issues:
            report_lines.append(f"- **连续性问题**: {len(continuity_issues)} 个连续性或重复问题")
    else:
        report_lines.append("✅ **所有形式化元素编号唯一且格式规范**")
    
    report_lines.append("")
    report_lines.append("| 指标 | 数量 |")
    report_lines.append("|------|------|")
    report_lines.append(f"| 扫描文件数 | {len(md_files)} |")
    report_lines.append(f"| 唯一编号数 | {len(unique_ids)} |")
    report_lines.append(f"| 总出现次数 | {len(all_elements)} |")
    report_lines.append(f"| 重复编号 | {len(duplicates)} |")
    report_lines.append(f"| 格式问题 | {len(format_issues)} |")
    report_lines.append("")
    
    # 按类型统计
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## 1. 各类形式化元素统计")
    report_lines.append("")
    report_lines.append("### 1.1 按类型统计")
    report_lines.append("")
    report_lines.append("| 类型 | 中文名 | 唯一编号 | 占比 |")
    report_lines.append("|------|--------|----------|------|")
    for type_key in ['Thm', 'Def', 'Lemma', 'Prop', 'Cor']:
        count = type_counts.get(type_key, 0)
        pct = (count / total * 100) if total > 0 else 0
        report_lines.append(f"| {type_key} | {ELEMENT_TYPES.get(type_key, type_key)} | {count} | {pct:.1f}% |")
    report_lines.append(f"| **总计** | | **{total}** | **100.0%** |")
    
    report_lines.append("")
    report_lines.append("### 1.2 按阶段统计")
    report_lines.append("")
    report_lines.append("| 阶段 | 目录 | 唯一编号 | 占比 |")
    report_lines.append("|------|------|----------|------|")
    for stage_key in ['S', 'K', 'F']:
        count = stage_counts.get(stage_key, 0)
        pct = (count / total * 100) if total > 0 else 0
        report_lines.append(f"| {stage_key} | {STAGE_MAP.get(stage_key, stage_key)} | {count} | {pct:.1f}% |")
    report_lines.append(f"| **总计** | | **{total}** | **100.0%** |")
    
    # 与注册表对比
    report_lines.append("")
    report_lines.append("### 1.3 与THEOREM-REGISTRY.md对比")
    report_lines.append("")
    report_lines.append("| 类型 | 扫描结果 | 注册表 | 差异 | 覆盖率 |")
    report_lines.append("|------|----------|--------|------|--------|")
    for type_key in ['Thm', 'Def', 'Lemma', 'Prop', 'Cor']:
        scanned = type_counts.get(type_key, 0)
        registry = registry_stats[type_key]
        diff = scanned - registry
        coverage = (scanned / registry * 100) if registry > 0 else 0
        report_lines.append(f"| {ELEMENT_TYPES[type_key]} | {scanned} | {registry} | {diff:+,} | {coverage:.1f}% |")
    report_lines.append(f"| **总计** | **{total}** | **{total_registry}** | **{total - total_registry:+,}** | **{coverage_total:.1f}%** |")
    
    report_lines.append("")
    report_lines.append("> **说明**: 注册表统计可能包含规划中的元素或历史版本数据，实际扫描只统计当前文档中存在的元素。")
    
    # 重复编号详情
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## 2. 重复编号列表")
    report_lines.append("")
    
    if duplicates:
        report_lines.append(f"发现 **{len(duplicates)}** 个编号在多处出现（包括定义和引用）：")
        report_lines.append("")
        report_lines.append("| 编号 | 出现次数 | 说明 |")
        report_lines.append("|------|----------|------|")
        
        # 只显示出现次数较多的
        sorted_dups = sorted(duplicates.items(), key=lambda x: -len(x[1]))
        for elem_id, elems in sorted_dups[:100]:
            files = set(e['file'] for e in elems)
            if len(files) > 1:
                report_lines.append(f"| {elem_id} | {len(elems)} | 跨 {len(files)} 个文件 |")
            else:
                report_lines.append(f"| {elem_id} | {len(elems)} | 同一文件内 |")
        
        if len(sorted_dups) > 100:
            report_lines.append(f"| ... | ... | 还有 {len(sorted_dups) - 100} 个 |")
        
        report_lines.append("")
        report_lines.append("> **说明**: 编号在多处出现是正常现象，通常是因为在定义后又在其他位置被引用。")
    else:
        report_lines.append("✅ **未发现重复编号**")
    
    # 格式问题
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## 3. 格式不规范列表")
    report_lines.append("")
    
    if format_issues:
        report_lines.append(f"发现 **{len(format_issues)}** 个格式不规范元素：")
        report_lines.append("")
        report_lines.append("| 编号 | 问题描述 | 文件 | 行号 |")
        report_lines.append("|------|----------|------|------|")
        for issue in format_issues:
            report_lines.append(f"| {issue['elem_id']} | {issue['issue']} | {issue['file']} | {issue['line']} |")
    else:
        report_lines.append("✅ **所有元素格式规范**")
    
    # 连续性问题
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## 4. 编号连续性问题")
    report_lines.append("")
    
    gap_issues = [i for i in continuity_issues if i['type'] == 'gap']
    dup_in_doc = [i for i in continuity_issues if i['type'] == 'duplicate_in_doc']
    
    if gap_issues:
        report_lines.append(f"### 4.1 序号空缺 ({len(gap_issues)}个)")
        report_lines.append("")
        report_lines.append("| 问题描述 |")
        report_lines.append("|----------|")
        for issue in gap_issues[:50]:
            report_lines.append(f"| {issue['message']} |")
        if len(gap_issues) > 50:
            report_lines.append(f"| ... 还有 {len(gap_issues) - 50} 个 |")
        report_lines.append("")
    
    if dup_in_doc:
        report_lines.append(f"### 4.2 同一文档内重复 ({len(dup_in_doc)}个)")
        report_lines.append("")
        report_lines.append("| 问题描述 |")
        report_lines.append("|----------|")
        for issue in dup_in_doc[:50]:
            report_lines.append(f"| {issue['message']} |")
        if len(dup_in_doc) > 50:
            report_lines.append(f"| ... 还有 {len(dup_in_doc) - 50} 个 |")
        report_lines.append("")
    
    if not continuity_issues:
        report_lines.append("✅ **无连续性问题**")
    
    # 建议
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## 5. 建议修复方案")
    report_lines.append("")
    
    if format_issues:
        report_lines.append("### 格式规范修复")
        report_lines.append("")
        report_lines.append("1. 确保文档序号在 01-99 范围内（00无效）")
        report_lines.append("2. 确保顺序号在 01-999 范围内")
        report_lines.append("3. 使用正确的阶段标识：S(Struct)、K(Knowledge)、F(Flink)")
        report_lines.append("4. 使用正确的类型标识：Thm、Def、Lemma、Prop、Cor")
        report_lines.append("")
    
    report_lines.append("### 注册表同步建议")
    report_lines.append("")
    report_lines.append(f"当前扫描覆盖率为 **{coverage_total:.1f}%**，建议：")
    report_lines.append("1. **注册表更新**: 根据实际扫描结果更新THEOREM-REGISTRY.md")
    report_lines.append("2. **补充缺失元素**: 检查注册表中有但文档中缺失的元素")
    report_lines.append("3. **规范引用格式**: 确保所有引用使用标准格式")
    report_lines.append("")
    
    # 保存报告
    report_path = PROJECT_ROOT / 'FORMAL-ELEMENT-UNIQUENESS-CHECK-REPORT.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print("=" * 70)
    print("检查完成！")
    print(f"报告已保存: {report_path}")
    print("=" * 70)
    
    # 保存JSON
    json_data = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'files': len(md_files),
            'unique_elements': len(unique_ids),
            'total_occurrences': len(all_elements),
            'duplicates': len(duplicates),
            'format_issues': len(format_issues),
            'continuity_issues': len(continuity_issues)
        },
        'statistics': {
            'by_type': dict(type_counts),
            'by_stage': dict(stage_counts)
        },
        'format_issues': format_issues,
        'continuity_issues': continuity_issues,
        'duplicates': {
            k: [{**e, 'context': e['context'][:100]} for e in v]
            for k, v in list(duplicates.items())[:100]  # 只保存前100个
        }
    }
    
    json_path = PROJECT_ROOT / 'formal-element-check-summary.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"JSON数据已保存: {json_path}")


if __name__ == '__main__':
    main()
