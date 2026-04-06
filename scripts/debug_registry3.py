#!/usr/bin/env python3
"""Debug script to check THEOREM-REGISTRY.md format"""

with open('THEOREM-REGISTRY.md', 'r', encoding='utf-8') as f:
    content = f.read()
    
lines = content.split('\n')
for idx, line in enumerate(lines):
    check1 = '| 编号 |' in line
    check2 = '形式化等级' in line
    check3 = '状态' in line
    
    if check1:
        print(f'Line {idx+1}: check1=True, check2={check2}, check3={check3}')
        print(f'  Line: {repr(line[:80])}')
