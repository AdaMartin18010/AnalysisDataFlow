#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

with open('formal-element-check-result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 60)
print("形式化元素检查结果分析")
print("=" * 60)
print()

print("=== 统计信息 ===")
print(f"总元素数: {data['statistics']['total']}")
print(f"按类型: {data['statistics']['by_type']}")
print(f"按阶段: {data['statistics']['by_stage']}")
print()

print("=== 格式不规范元素 ===")
if data['invalid_formats']:
    for item in data['invalid_formats'][:20]:
        print(f"  {item['full_id']}: {item['issues']}")
else:
    print("  无")
print()

print("=== 连续性/重复问题样本 (前40) ===")
if data['continuity_issues']:
    for item in data['continuity_issues'][:40]:
        print(f"  {item['message']}")
else:
    print("  无")
print()

# 分析重复编号的真实情况
print("=== 重复编号分析 ===")
duplicates = data['duplicates']
if duplicates:
    print(f"发现 {len(duplicates)} 个重复编号")
    
    # 统计重复次数分布
    count_dist = {}
    for elem_id, elems in duplicates.items():
        cnt = len(elems)
        count_dist[cnt] = count_dist.get(cnt, 0) + 1
    
    print("重复次数分布:")
    for cnt in sorted(count_dist.keys()):
        print(f"  出现 {cnt} 次的编号: {count_dist[cnt]} 个")
else:
    print("无重复编号")
print()

# 检查实际唯一元素数
all_elements = data['all_elements']
unique_ids = set(e['full_id'] for e in all_elements)
print(f"=== 唯一编号统计 ===")
print(f"总出现次数: {len(all_elements)}")
print(f"唯一编号数: {len(unique_ids)}")
print(f"重复出现次数: {len(all_elements) - len(unique_ids)}")
