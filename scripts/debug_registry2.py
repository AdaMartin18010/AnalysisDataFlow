#!/usr/bin/env python3
"""Debug script to check THEOREM-REGISTRY.md format"""

with open('THEOREM-REGISTRY.md', 'r', encoding='utf-8') as f:
    content = f.read()
    
lines = content.split('\n')
for idx, line in enumerate(lines):
    if '| 编号 |' in line and '形式化等级' in line and '状态' in line:
        print(f'Line {idx+1}: Header match found')
        original = line
        
        # Try the replacement
        if ' 状态 |' in line:
            new_line = line.replace(' 状态 |', ' **依赖元素** | 状态 |')
            print(f'  Original: {repr(original)}')
            print(f'  New:      {repr(new_line)}')
        break
