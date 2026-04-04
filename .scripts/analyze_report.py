#!/usr/bin/env python3
import json

with open('.stats/cross_ref_report_v2.json', 'r', encoding='utf-8') as f:
    report = json.load(f)

# 按错误类型分组
file_errors = report['errors_by_category']['file_not_found']
anchor_errors = report['errors_by_category']['anchor_not_found']

# 分析文件错误模式
print('=== 文件不存在错误的常见模式 ===')
patterns = {}
for err in file_errors:
    path = err['resolved']
    # 提取路径模式
    if '/' in path:
        prefix = path.split('/')[0]
    else:
        prefix = 'root'
    patterns[prefix] = patterns.get(prefix, 0) + 1

for prefix, count in sorted(patterns.items(), key=lambda x: -x[1])[:15]:
    print(f'{prefix}: {count}')

# 列出一些具体的无效链接示例
print('\n=== 具体的无效链接示例 ===')
for err in file_errors[:20]:
    print(f"{err['source']} -> {err['url']}")

# 分析锚点错误
print('\n=== 锚点错误的常见模式 ===')
for err in anchor_errors[:15]:
    print(f"{err['source']}:{err['line']} -> #{err['anchor']}")
