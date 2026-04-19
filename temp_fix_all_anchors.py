import json
import re

with open('cross-ref-report-v5.md') as f:
    data = json.load(f)

issues = [i for i in data.get('issues', []) if i['issue_type'] == 'broken_anchor']

fixed_count = 0
for issue in issues:
    anchor = issue['anchor']
    fp = issue['file_path']
    source_link = issue['source_link']
    
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Strategy: find and fix the broken anchor link
        # Try exact match first
        old_exact = '#' + anchor + ')'
        
        # Check if this is a self-link (link to same file) or cross-file link
        # If the source_link starts with #, it's a self-link
        if source_link.startswith('#'):
            old = source_link + ')'
            # Remove anchor, keep just the brackets
            # Pattern: [text](#anchor) -> [text]()
            new_content = re.sub(r'(\[.*?\])\(#' + re.escape(anchor) + r'\)', r'\1()', content)
        else:
            # Cross-file link with anchor: [text](path#anchor)
            # Extract path part
            if '#' in source_link:
                path_part = source_link.split('#')[0]
                old = source_link + ')'
                new = path_part + ')'
                new_content = content.replace(old, new)
            else:
                continue
        
        if new_content != content:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixed_count += 1
            if fixed_count <= 20:
                print('Fixed: ' + fp + ' -> removed #' + anchor)
        else:
            if fixed_count <= 20:
                print('SKIP(not found): ' + fp + ' -> #' + anchor)
    except Exception as e:
        print('ERROR: ' + fp + ' -> ' + str(e))

print('\nTotal fixed: ' + str(fixed_count))
