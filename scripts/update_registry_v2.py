#!/usr/bin/env python3
"""
Script to update THEOREM-REGISTRY.md with Dependencies column
"""

import re

# Read dependency mappings
dependencies = {}
with open('scripts/dependency_mappings.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and ':' in line:
            key, val = line.split(':', 1)
            dependencies[key.strip()] = val.strip()

# Read the original file
with open('THEOREM-REGISTRY.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Track changes
stats = {
    'theorem_rows': 0,
    'def_rows': 0,
    'lemma_rows': 0,
    'prop_rows': 0,
    'cor_rows': 0,
    'deps_added': 0
}

output_lines = []
in_table = False
table_type = None
header_line_idx = None

for idx, line in enumerate(lines):
    original_line = line
    
    # Detect table headers - match pattern like "| 编号 | 名称 | 位置 | 形式化等级 | 状态 |"
    if '| 编号 |' in line and '形式化等级' in line and '状态' in line:
        in_table = True
        if '定理' in line or 'Thm' in line:
            table_type = 'theorem'
        elif '定义' in line or 'Def' in line:
            table_type = 'def'
        elif '引理' in line or 'Lemma' in line:
            table_type = 'lemma'
        elif '命题' in line or 'Prop' in line:
            table_type = 'prop'
        elif '推论' in line or 'Cor' in line:
            table_type = 'cor'
        else:
            table_type = None
        
        # Modify header line to add Dependencies column
        if table_type:
            line = line.rstrip('\n')
            # Insert before "状态" or at the end if no "状态"
            if ' 状态 |' in line:
                line = line.replace(' 状态 |', ' **依赖元素** | 状态 |')
            else:
                line = line.rstrip() + ' **依赖元素** |'
            output_lines.append(line + '\n')
            header_line_idx = idx
            continue
    
    # Modify separator line after header (typically line with |-----|)
    if in_table and header_line_idx is not None and idx == header_line_idx + 1:
        if '|' in line and ('---' in line or ':-:' in line):
            line = line.rstrip('\n')
            if ' 状态 |' in line:
                # Find the position to insert
                parts = line.split('|')
                # Insert before the last part (which should be status)
                new_parts = parts[:-2] + ['-------------', parts[-2]] + [parts[-1]]
                line = '|'.join(new_parts)
            else:
                line = line.rstrip() + '|-------------|'
            output_lines.append(line + '\n')
            continue
    
    # Modify data rows
    if in_table and table_type and '|' in line:
        line_stripped = line.strip()
        # Skip separator lines and header continuation lines
        if line_stripped.startswith('|') and not line_stripped.startswith('|---'):
            parts = line_stripped.split('|')
            if len(parts) >= 3:
                elem_num = parts[1].strip()
                # Match patterns like Thm-S-XX-XX, Def-S-XX-XX, etc.
                match = re.search(r'(Thm|Def|Lemma|Prop|Cor)-[SKF]-\d{2}[a-z]?-\d{2,3}[a-z]?', elem_num)
                if not match:
                    # Try alternative patterns
                    match = re.search(r'(Thm|Def|Lemma|Prop|Cor)-[SKF]-\d{2}-\d{2}', elem_num)
                if match:
                    elem_id = match.group(0)
                    dep = dependencies.get(elem_id, '-')
                    
                    # Add dependency column before status
                    line = line.rstrip('\n')
                    if ' |' in line:
                        # Insert before the last column (status)
                        # Find all table cells
                        cells = [c.strip() for c in line.split('|')]
                        # Remove empty cells from start/end
                        while cells and not cells[0]:
                            cells = cells[1:]
                        while cells and not cells[-1]:
                            cells = cells[:-1]
                        
                        # Insert dependency before status (last cell)
                        if len(cells) >= 4:
                            new_cells = cells[:-1] + [dep, cells[-1]]
                            line = '| ' + ' | '.join(new_cells) + ' |'
                    
                    stats[f'{table_type}_rows'] += 1
                    if dep != '-':
                        stats['deps_added'] += 1
    
    # Detect end of table (empty line or non-table line)
    if in_table and header_line_idx is not None and line.strip() and not line.strip().startswith('|') and not line.strip().startswith('**') and not line.strip().startswith('迁移') and not line.strip().startswith('Flink'):
        if idx > header_line_idx + 2:  # Make sure we're past header and separator
            in_table = False
            table_type = None
            header_line_idx = None
    
    output_lines.append(line)

# Write the updated file
with open('THEOREM-REGISTRY.md', 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print("THEOREM-REGISTRY.md updated successfully!")
print(f"\nStatistics:")
print(f"  Theorem rows with deps column: {stats['theorem_rows']}")
print(f"  Definition rows with deps column: {stats['def_rows']}")
print(f"  Lemma rows with deps column: {stats['lemma_rows']}")
print(f"  Proposition rows with deps column: {stats['prop_rows']}")
print(f"  Corollary rows with deps column: {stats['cor_rows']}")
print(f"  Total rows modified: {sum(stats.values()) - stats['deps_added']}")
print(f"  Non-empty dependencies added: {stats['deps_added']}")
