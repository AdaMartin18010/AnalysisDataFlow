import json
import re
import os

with open('cross-ref-report.md') as f:
    data = json.load(f)

issues = [i for i in data.get('issues', []) if i['issue_type'] == 'broken_anchor']

# Fix pattern: #5-形式证明--工程论证-proof--engineering-argument -> #5
# And #5-形式证明--工程论证 -> #5
fixed_count = 0
for issue in issues:
    anchor = issue['anchor']
    fp = issue['file_path']
    source_link = issue['source_link']
    
    if anchor in ['5-形式证明--工程论证-proof--engineering-argument', '5-形式证明--工程论证']:
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace the broken anchor link with simple #5
            old_link = source_link
            new_link = '#5'
            
            # Only replace if old_link exists in content
            if old_link in content:
                content = content.replace(old_link, new_link)
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_count += 1
                print('Fixed: ' + fp + ' -> ' + old_link + ' to ' + new_link)
            else:
                # Try with just the anchor part
                old_anchor = '#' + anchor
                if old_anchor in content:
                    content = content.replace(old_anchor, '#5')
                    with open(fp, 'w', encoding='utf-8') as f:
                        f.write(content)
                    fixed_count += 1
                    print('Fixed: ' + fp + ' -> ' + old_anchor + ' to #5')
                else:
                    print('SKIP(not found): ' + fp + ' -> ' + source_link)
        except Exception as e:
            print('ERROR: ' + fp + ' -> ' + str(e))

print('\nTotal fixed (pattern #5): ' + str(fixed_count))
