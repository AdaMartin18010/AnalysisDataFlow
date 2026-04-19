import json
import re

with open('cross-ref-report-v3.md') as f:
    data = json.load(f)

issues = [i for i in data.get('issues', []) if i['issue_type'] == 'broken_anchor']

# Fix all broken anchors by reverting #5 back to full anchor
# OR removing anchor if no matching section exists
fixed_count = 0
for issue in issues:
    anchor = issue['anchor']
    fp = issue['file_path']
    source_link = issue['source_link']
    
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all h2 sections
        h2_sections = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
        
        # Generate anchors from sections (GitHub style)
        def gen_anchor(text):
            # Remove markdown formatting
            t = text.strip()
            # Convert to lowercase-ish (keep Chinese chars)
            # Replace spaces and slashes with -
            t = re.sub(r'[\s/]+', '-', t)
            # Remove parentheses content
            t = re.sub(r'[()]', '', t)
            return t.lower()
        
        anchors = [gen_anchor(s) for s in h2_sections]
        
        if anchor == '5':
            # Check if any generated anchor starts with '5'
            matching = [a for a in anchors if a.startswith('5')]
            if matching:
                target = matching[0]
                # Replace #5 with #target
                new_content = content.replace('#5)', '#' + target + ')')
                new_content = new_content.replace('#5]', '#' + target + ']')
                if new_content != content:
                    with open(fp, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    fixed_count += 1
                    print('Fixed #5 -> #' + target + ' in ' + fp)
                else:
                    print('SKIP(pattern not found in content): ' + fp)
            else:
                print('No section 5 found in: ' + fp)
        elif '形式证明' in anchor or '工程论证' in anchor:
            # Try to find matching section
            matching = [a for a in anchors if '形式证明' in a or '工程论证' in a]
            if matching:
                target = matching[0]
                old = '#' + anchor
                new = '#' + target
                if old in content:
                    new_content = content.replace(old, new)
                    with open(fp, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    fixed_count += 1
                    print('Fixed ' + old + ' -> ' + new + ' in ' + fp)
                else:
                    print('SKIP(not found): ' + fp + ' ' + old)
            else:
                print('No matching section in: ' + fp)
        else:
            # For other anchors, just print for manual inspection
            pass
    except Exception as e:
        print('ERROR: ' + fp + ' -> ' + str(e))

print('\nTotal fixed: ' + str(fixed_count))
