#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
形式化元素高级检查脚本 - 区分定义和引用
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

# 定义模式（行首是**元素编号**或**Def-XX**）
DEFINITION_PATTERN = re.compile(
    r'^\s*\*\*(Def)-([SKF])-(\d{2})-(\d{2,3})\*\*|^\s*###\s+\*\*(Def)-([SKF])-(\d{2})-(\d{2,3})\*\*'
)

# 元素类型映射
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
    """从文件中提取所有形式化元素，区分定义和引用"""
    definitions = []
    references = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                # 检查是否是定义（行首有**元素编号**格式）
                is_definition = False
                if line.strip().startswith('**') and '**' in line.strip()[2:]:
                    # 检查是否是定义行
                    if re.search(r'^\s*\*\*(Thm|Def|Lemma|Prop|Cor)-[SKF]-\d{2}-\d{2,3}\*\*', line):
                        is_definition = True
                
                # 查找所有匹配的形式化元素
                matches = FORMAL_ELEMENT_PATTERN.findall(line)
                for match in matches:
                    elem_type, stage, doc_num, seq_num = match
                    elem_info = {
                        'type': elem_type,
                        'stage': stage,
                        'doc_num': doc_num,
                        'seq_num': seq_num,
                        'full_id': f"{elem_type}-{stage}-{doc_num}-{seq_num}",
                        'file': os.path.relpath(file_path, PROJECT_ROOT),
                        'line': line_num,
                        'context': line.strip()[:150]
                    }
                    
                    if is_definition:
                        definitions.append(elem_info)
                    else:
                        references.append(elem_info)
    except Exception as e:
        print(f"  警告: 无法读取文件 {file_path}: {e}")
    
    return definitions, references


def main():
    """主函数"""
    print("=" * 60)
    print("形式化元素高级检查（区分定义与引用）")
    print("=" * 60)
    print()
    
    # 获取所有Markdown文件
    print("[1/4] 扫描Markdown文件...")
    md_files = get_all_md_files()
    print(f"      找到 {len(md_files)} 个Markdown文件")
    
    # 提取所有形式化元素
    print("[2/4] 提取形式化元素...")
    all_definitions = []
    all_references = []
    
    for file_path in md_files:
        defs, refs = extract_formal_elements(file_path)
        all_definitions.extend(defs)
        all_references.extend(refs)
    
    print(f"      提取到 {len(all_definitions)} 个定义")
    print(f"      提取到 {len(all_references)} 个引用")
    
    # 统计唯一编号
    print("[3/4] 统计唯一编号...")
    unique_defs = set(e['full_id'] for e in all_definitions)
    unique_refs = set(e['full_id'] for e in all_references)
    all_unique = unique_defs | unique_refs
    
    print(f"      唯一定义: {len(unique_defs)}")
    print(f"      唯一引用: {len(unique_refs)}")
    print(f"      总共唯一: {len(all_unique)}")
    
    # 检查是否有编号只有引用没有定义
    refs_without_defs = unique_refs - unique_defs
    if refs_without_defs:
        print(f"      ⚠️  {len(refs_without_defs)} 个编号只有引用没有定义")
    
    # 按类型统计
    print("[4/4] 按类型统计...")
    type_stats = defaultdict(lambda: {'def': 0, 'ref': 0, 'unique': 0})
    
    for elem_id in all_unique:
        elem_type = elem_id.split('-')[0]
        type_stats[elem_type]['unique'] += 1
    
    for elem in all_definitions:
        type_stats[elem['type']]['def'] += 1
    
    for elem in all_references:
        type_stats[elem['type']]['ref'] += 1
    
    print()
    print("=" * 60)
    print("统计结果")
    print("=" * 60)
    print()
    print(f"{'类型':<10} {'中文':<8} {'唯一定义':>10} {'定义出现':>10} {'引用出现':>10} {'总计':>10}")
    print("-" * 60)
    
    total_def = total_ref = total_unique = 0
    for type_key in ['Thm', 'Def', 'Lemma', 'Prop', 'Cor']:
        if type_key in type_stats:
            stats = type_stats[type_key]
            type_name = ELEMENT_TYPES[type_key]
            print(f"{type_key:<10} {type_name:<8} {stats['unique']:>10} {stats['def']:>10} {stats['ref']:>10} {stats['def']+stats['ref']:>10}")
            total_unique += stats['unique']
            total_def += stats['def']
            total_ref += stats['ref']
    
    print("-" * 60)
    print(f"{'总计':<10} {'':8} {total_unique:>10} {total_def:>10} {total_ref:>10} {total_def+total_ref:>10}")
    print()
    
    # 与注册表对比
    print("=" * 60)
    print("与THEOREM-REGISTRY.md对比")
    print("=" * 60)
    print()
    print("                    扫描结果    注册表      差异")
    print("-" * 50)
    
    registry_stats = {
        'Thm': 1910,
        'Def': 4564,
        'Lemma': 1568,
        'Prop': 1194,
        'Cor': 121
    }
    
    for type_key in ['Thm', 'Def', 'Lemma', 'Prop', 'Cor']:
        scanned = type_stats[type_key]['unique'] if type_key in type_stats else 0
        registry = registry_stats[type_key]
        diff = scanned - registry
        type_name = ELEMENT_TYPES[type_key]
        print(f"{type_name:<8} {scanned:>10} {registry:>10} {diff:>+10}")
    
    print("-" * 50)
    print(f"{'总计':<8} {total_unique:>10} {sum(registry_stats.values()):>10} {total_unique - sum(registry_stats.values()):>+10}")
    print()
    
    # 生成详细报告
    report_lines = []
    report_lines.append("# 形式化元素高级检查报告")
    report_lines.append("")
    report_lines.append(f"> **检查时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"> **检查范围**: Struct/ | Knowledge/ | Flink/")
    report_lines.append(f"> **扫描文件**: {len(md_files)} 个 Markdown 文件")
    report_lines.append("")
    
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## 执行摘要")
    report_lines.append("")
    report_lines.append("### 扫描结果统计")
    report_lines.append("")
    report_lines.append(f"| 指标 | 数量 |")
    report_lines.append(f"|------|------|")
    report_lines.append(f"| Markdown文件数 | {len(md_files)} |")
    report_lines.append(f"| 唯一定义编号 | {len(unique_defs)} |")
    report_lines.append(f"| 唯一定义出现 | {len(all_definitions)} |")
    report_lines.append(f"| 引用出现次数 | {len(all_references)} |")
    report_lines.append(f"| 总唯一编号 | {len(all_unique)} |")
    report_lines.append("")
    
    if refs_without_defs:
        report_lines.append(f"⚠️ **警告**: 发现 {len(refs_without_defs)} 个编号只有引用没有定义")
        report_lines.append("")
        report_lines.append("### 只有引用没有定义的编号（前50）")
        report_lines.append("")
        for elem_id in sorted(list(refs_without_defs))[:50]:
            report_lines.append(f"- `{elem_id}`")
        report_lines.append("")
    
    report_lines.append("### 按类型统计")
    report_lines.append("")
    report_lines.append(f"| 类型 | 中文 | 唯一编号 | 定义出现 | 引用出现 | 总计 |")
    report_lines.append(f"|------|------|----------|----------|----------|------|")
    
    for type_key in ['Thm', 'Def', 'Lemma', 'Prop', 'Cor']:
        if type_key in type_stats:
            stats = type_stats[type_key]
            type_name = ELEMENT_TYPES[type_key]
            report_lines.append(f"| {type_key} | {type_name} | {stats['unique']} | {stats['def']} | {stats['ref']} | {stats['def']+stats['ref']} |")
    
    report_lines.append("")
    report_lines.append("### 与THEOREM-REGISTRY.md对比")
    report_lines.append("")
    report_lines.append("| 类型 | 中文 | 扫描唯一 | 注册表 | 差异 | 覆盖率 |")
    report_lines.append("|------|------|----------|--------|------|--------|")
    
    for type_key in ['Thm', 'Def', 'Lemma', 'Prop', 'Cor']:
        scanned = type_stats[type_key]['unique'] if type_key in type_stats else 0
        registry = registry_stats[type_key]
        diff = scanned - registry
        type_name = ELEMENT_TYPES[type_key]
        coverage = (scanned / registry * 100) if registry > 0 else 0
        report_lines.append(f"| {type_key} | {type_name} | {scanned} | {registry} | {diff:+,} | {coverage:.1f}% |")
    
    total_registry = sum(registry_stats.values())
    total_coverage = (total_unique / total_registry * 100) if total_registry > 0 else 0
    report_lines.append(f"| **总计** | | **{total_unique}** | **{total_registry}** | **{total_unique - total_registry:+,}** | **{total_coverage:.1f}%** |")
    report_lines.append("")
    
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## 问题与建议")
    report_lines.append("")
    
    if total_coverage < 90:
        report_lines.append("### ⚠️ 覆盖率不足")
        report_lines.append("")
        report_lines.append(f"扫描覆盖率仅为 {total_coverage:.1f}%，可能原因：")
        report_lines.append("1. 注册表中列出的部分元素尚未写入实际文档")
        report_lines.append("2. 部分元素编号格式不符合标准，未被正则表达式捕获")
        report_lines.append("3. 部分文档使用了非标准的编号格式")
        report_lines.append("")
    
    if refs_without_defs:
        report_lines.append("### ⚠️ 引用不一致")
        report_lines.append("")
        report_lines.append(f"发现 {len(refs_without_defs)} 个编号在文档中被引用但未找到定义。建议：")
        report_lines.append("1. 检查这些编号是否拼写错误")
        report_lines.append("2. 确认定义是否存在于未扫描的文件中")
        report_lines.append("3. 添加相应的定义或删除无效引用")
        report_lines.append("")
    
    report_lines.append("### 建议修复方案")
    report_lines.append("")
    report_lines.append("1. **格式规范检查**: 确保所有形式化元素使用标准格式 `Type-Stage-Doc-Seq`")
    report_lines.append("2. **定义完整性**: 确保每个被引用的编号都有对应的定义")
    report_lines.append("3. **注册表同步**: 定期更新THEOREM-REGISTRY.md以反映实际文档状态")
    report_lines.append("4. **编号连续性**: 检查编号空缺，考虑是否需要填补")
    report_lines.append("")
    
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## 附录：唯一定义清单（前200）")
    report_lines.append("")
    report_lines.append("| 编号 | 定义文件 | 行号 |")
    report_lines.append("|------|----------|------|")
    
    sorted_defs = sorted(all_definitions, key=lambda x: (x['type'], x['stage'], x['doc_num'], int(x['seq_num'])))
    seen = set()
    for elem in sorted_defs[:200]:
        if elem['full_id'] not in seen:
            seen.add(elem['full_id'])
            report_lines.append(f"| {elem['full_id']} | {elem['file']} | {elem['line']} |")
    
    if len(unique_defs) > 200:
        report_lines.append(f"| ... | ... | ... |")
        report_lines.append(f"| *共 {len(unique_defs)} 个唯一定义* | | |")
    
    # 保存报告
    report_path = PROJECT_ROOT / 'FORMAL-ELEMENT-ADVANCED-REPORT.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print()
    print("=" * 60)
    print("检查完成！")
    print(f"报告已保存至: {report_path}")
    print("=" * 60)
    
    # 保存JSON
    json_data = {
        'timestamp': datetime.now().isoformat(),
        'statistics': {
            'files': len(md_files),
            'unique_definitions': len(unique_defs),
            'definition_occurrences': len(all_definitions),
            'reference_occurrences': len(all_references),
            'total_unique': len(all_unique)
        },
        'type_stats': dict(type_stats),
        'definitions': [{k: v for k, v in e.items() if k != 'context'} for e in all_definitions],
        'references': [{k: v for k, v in e.items() if k != 'context'} for e in all_references],
        'refs_without_defs': sorted(list(refs_without_defs))
    }
    
    json_path = PROJECT_ROOT / 'formal-element-advanced-result.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"JSON数据已保存至: {json_path}")


if __name__ == '__main__':
    main()
