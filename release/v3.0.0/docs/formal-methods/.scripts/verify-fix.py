#!/usr/bin/env python3
"""验证修复效果"""
import re
from pathlib import Path

priority_files = [
    'formal-methods/99-probabilistic-programming.md',
    'formal-methods/99-homotopy-type-theory.md',
    'formal-methods/99-game-semantics.md',
    'formal-methods/99-kubernetes-scheduler.md',
    'formal-methods/99-raft-consensus.md',
    'formal-methods/99-llvm-ir-semantics.md',
]

total_remaining = 0
print('剩余问题扫描:')
print('='*60)

for file_path in priority_files:
    p = Path(file_path)
    if not p.exists():
        continue
    
    content = p.read_text(encoding='utf-8')
    lines = content.split('\n')
    in_mermaid = False
    file_errors = []
    
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('```mermaid'):
            in_mermaid = True
            continue
        elif line.strip() == '```' and in_mermaid:
            in_mermaid = False
            continue
        
        if in_mermaid:
            # 检查箭头中的空格
            if re.search(r'--\s+>', line) or re.search(r'-\s+->', line):
                file_errors.append((i, '箭头空格', line.strip()[:60]))
            # 检查引号
            if line.count('"') % 2 == 1 and '"' in line:
                file_errors.append((i, '引号', line.strip()[:60]))
    
    if file_errors:
        print(f'\n{file_path}: {len(file_errors)}处')
        for ln, err_type, content in file_errors[:5]:
            print(f'  行{ln} [{err_type}]: {content}...')
        if len(file_errors) > 5:
            print(f'  ... 还有 {len(file_errors) - 5} 处')
        total_remaining += len(file_errors)
    else:
        print(f'{file_path}: ✓ 无问题')

print(f'\n总计剩余问题: {total_remaining}')
