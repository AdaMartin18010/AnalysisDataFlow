#!/usr/bin/env python3
"""
Script to update THEOREM-REGISTRY.md with Dependencies column
Simple approach: process line by line with straightforward replacements
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
    'header_modified': 0,
    'separator_modified': 0,
    'data_rows': 0,
    'deps_added': 0
}

output_lines = []
expect_separator = False
expect_data = False
table_type = None

for idx, line in enumerate(lines):
    original_line = line
    modified = False
    
    # Check for table headers with formality level and status
    if '| 编号 |' in line and '形式化等级' in line and '状态' in line:
        # This is a header line - add Dependencies column
        if ' 状态 |' in line:
            line = line.replace(' 状态 |', ' **依赖元素** | 状态 |')
            stats['header_modified'] += 1
            modified = True
            expect_separator = True
            
            # Determine table type
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
    
    # Check for separator line
    elif expect_separator and '|' in line and '---' in line:
        # Add separator for new column
        parts = line.split('|')
        if len(parts) >= 6:
            # Insert after the "形式化等级" separator (index 4)
            new_parts = parts[:5] + ['-------------|'] + parts[5:]
            line = '|'.join(new_parts)
            # Fix any double pipes
            line = line.replace('||', '|')
            stats['separator_modified'] += 1
            modified = True
            expect_separator = False
            expect_data = True
    
    # Check for data rows
    elif expect_data and line.strip().startswith('|'):
        # Check if this is still a data row or end of table
        if not line.strip().startswith('|---') and ' 编号 ' not in line:
            # This is a data row
            parts = line.split('|')
            if len(parts) >= 3:
                elem_num = parts[1].strip()
                # Try to match element ID
                match = re.search(r'(Thm|Def|Lemma|Prop|Cor)-[SKF]-\d{2}[a-z]?-\d{2,3}[a-z]?', elem_num)
                if match:
                    elem_id = match.group(0)
                    dep = dependencies.get(elem_id, '-')
                    
                    # Insert dependency before status (second to last column)
                    if len(parts) >= 6:
                        new_parts = parts[:-2] + [f' {dep} ', parts[-2]] + parts[-1:]
                        line = '|'.join(new_parts)
                        stats['data_rows'] += 1
                        if dep != '-':
                            stats['deps_added'] += 1
                        modified = True
        else:
            # End of table
            expect_data = False
            table_type = None
    
    # Check for end of table (non-empty, non-table line)
    elif expect_data and line.strip() and not line.strip().startswith('|') and not line.strip().startswith('**'):
        expect_data = False
        table_type = None
    
    output_lines.append(line)

# Write the updated file
with open('THEOREM-REGISTRY.md', 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print("THEOREM-REGISTRY.md updated successfully!")
print(f"\nStatistics:")
print(f"  Headers modified: {stats['header_modified']}")
print(f"  Separators modified: {stats['separator_modified']}")
print(f"  Data rows modified: {stats['data_rows']}")
print(f"  Non-empty dependencies added: {stats['deps_added']}")
