import json
import re

with open('cross-ref-report-v6.md') as f:
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
            print('SKIP(line out of range): ' + fp + ' line ' + str(line_num))
            continue
        
        line = lines[line_num - 1]
        old_line = line
        
        # Find markdown link with this anchor and remove the anchor part
        # Pattern: [text](#anchor) -> [text]()
        line = re.sub(r'(\[.*?\])\(#' + re.escape(anchor) + r'\)', r'\1()', line)
        
        if line != old_line:
            lines[line_num - 1] = line
            with open(fp, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            fixed_count += 1
            print('Fixed: ' + fp + ' line ' + str(line_num) + ' -> removed #' + anchor)
        else:
            print('SKIP(pattern not found on line): ' + fp + ' line ' + str(line_num) + ' -> #' + anchor)
            print('  Content: ' + old_line.strip()[:80])
    except Exception as e:
        print('ERROR: ' + fp + ' -> ' + str(e))

print('\nTotal fixed: ' + str(fixed_count))
