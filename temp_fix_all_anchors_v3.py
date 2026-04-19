import json
import re

with open('cross-ref-report-v7.md') as f:
    data = json.load(f)

issues = [i for i in data.get('issues', []) if i['issue_type'] == 'broken_anchor']

fixed_count = 0
for issue in issues:
    anchor = issue['anchor']
    fp = issue['file_path']
    line_num = issue['line_number']
    
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if line_num > len(lines):
            continue
        
        line = lines[line_num - 1]
        old_line = line
        
        # Pattern: [text](#anchor) -> [text]()
        line = re.sub(r'(\[.*?\])\(#' + re.escape(anchor) + r'\)', r'\1()', line)
        
        if line != old_line:
            lines[line_num - 1] = line
            with open(fp, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            fixed_count += 1
            if fixed_count <= 30:
                print('Fixed: ' + fp + ' line ' + str(line_num))
        else:
            # Try alternative: the anchor might be part of a larger link
            # e.g. [text](path#anchor)
            line2 = re.sub(r'(\[.*?\]\([^)#]*)#' + re.escape(anchor) + r'\)', r'\1)', line)
            if line2 != line:
                lines[line_num - 1] = line2
                with open(fp, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                fixed_count += 1
                if fixed_count <= 30:
                    print('Fixed(cross-link): ' + fp + ' line ' + str(line_num))
            else:
                if fixed_count <= 10:
                    print('SKIP: ' + fp + ' line ' + str(line_num) + ' -> #' + anchor)
                    print('  ' + old_line.strip()[:100])
    except Exception as e:
        print('ERROR: ' + fp + ' -> ' + str(e))

print('\nTotal fixed: ' + str(fixed_count))
