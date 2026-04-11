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
    content = f.read()

lines = content.split('\n')

# Track changes
stats = {
    'header_modified': 0,
    'separator_modified': 0,
    'data_rows': 0,
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
            if ' 状态 |' in line:
                line = line.replace(' 状态 |', ' **依赖元素** | 状态 |')
                stats['header_modified'] += 1
            header_line_idx = idx
    
    # Modify separator line after header (typically line with |-----|)
    elif in_table and header_line_idx is not None and idx == header_line_idx + 1:
        if '|' in line and ('---' in line or ':-:' in line):
            # Count columns in separator
            parts = line.split('|')
            # Insert separator for new column
            if parts:
                # Find where to insert (before status separator)
                new_parts = []
                for i, p in enumerate(parts):
                    new_parts.append(p)
                    # After the 4th column separator (position 4), insert new one
                    if i == 4 and '---' in p:
                        new_parts.append('-------------')
                line = '|'.join(new_parts)
                stats['separator_modified'] += 1
    
    # Modify data rows
    elif in_table and table_type and '|' in line:
        line_stripped = line.strip()
        # Skip separator lines and header continuation lines
        if line_stripped.startswith('|') and not line_stripped.startswith('|---') and not line_stripped.startswith('| **'):
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
                    # Find position of last | which is before status
                    cells = line.split('|')
                    # Insert before the status cell (second to last non-empty cell)
                    new_cells = []
                    status_cell = None
                    for i, c in enumerate(cells):
                        if i == len(cells) - 2:  # Before the last cell (which is empty or status)
                            new_cells.append(f' {dep} ')
                        new_cells.append(c)
                    line = '|'.join(new_cells)
                    
                    stats['data_rows'] += 1
                    if dep != '-':
                        stats['deps_added'] += 1
    
    # Detect end of table (empty line or non-table line)
    elif in_table and header_line_idx is not None and line.strip() and not line.strip().startswith('|') and not line.strip().startswith('**'):
        if idx > header_line_idx + 2:  # Make sure we're past header and separator
            in_table = False
            table_type = None
            header_line_idx = None
    
    output_lines.append(line)

# Write the updated file
with open('THEOREM-REGISTRY.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print("THEOREM-REGISTRY.md updated successfully!")
print(f"\nStatistics:")
print(f"  Headers modified: {stats['header_modified']}")
print(f"  Separators modified: {stats['separator_modified']}")
print(f"  Data rows modified: {stats['data_rows']}")
print(f"  Non-empty dependencies added: {stats['deps_added']}")
