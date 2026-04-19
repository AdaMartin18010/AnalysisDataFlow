import json
import re

with open('cross-ref-report-v3.md') as f:
    data = json.load(f)

issues = [i for i in data.get('issues', []) if i['issue_type'] == 'broken_anchor']

# Fix pattern: anchor = "5" (simple #5)
# If file does NOT have a section starting with "## 5", remove the anchor
fixed_count = 0
for issue in issues:
    anchor = issue['anchor']
    fp = issue['file_path']
    source_link = issue['source_link']
    
    if anchor == '5':
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if file has ## 5 section
            has_section5 = bool(re.search(r'^##\s*5[\.\s]', content, re.MULTILINE))
            
            if not has_section5:
                # Remove the #5 anchor from links, keep just the file path
                # Match patterns like [text](#5) or [text](path#5)
                # We need to be careful to only replace the anchor part
                old = '#5'
                # Find all occurrences of #5 that are part of a markdown link
                new_content = content
                # Pattern: ](...#5) -> ](...)
                new_content = re.sub(r'(\]\([^)#]*)#5\)', r'\1)', new_content)
                # Pattern: standalone [text](#5) -> [text]()
                new_content = re.sub(r'(\[.*?\])\(#5\)', r'\1()', new_content)
                
                if new_content != content:
                    with open(fp, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    fixed_count += 1
                    print('Fixed (no section 5): ' + fp)
                else:
                    print('SKIP(pattern not found): ' + fp)
            else:
                print('OK(has section 5): ' + fp)
        except Exception as e:
            print('ERROR: ' + fp + ' -> ' + str(e))

print('\nTotal fixed (#5 -> removed): ' + str(fixed_count))
