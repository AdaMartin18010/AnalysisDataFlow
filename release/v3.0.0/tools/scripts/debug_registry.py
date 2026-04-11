#!/usr/bin/env python3
"""Debug script to check THEOREM-REGISTRY.md format"""

with open('THEOREM-REGISTRY.md', 'r', encoding='utf-8') as f:
    content = f.read()
    
lines = content.split('\n')
for idx, line in enumerate(lines):
    if '| 编号 |' in line and '形式化等级' in line:
        print(f'Line {idx+1}: Header match found')
        print(f'  Contains [ 状态 |]: {" 状态 |" in line}')
        print(f'  Contains [状态 |]: {"状态 |" in line}')
        print(f'  Line content: {repr(line)}')
        # Check next line
        if idx+1 < len(lines):
            print(f'  Next line: {repr(lines[idx+1][:80])}')
        break
