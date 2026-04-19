import json
import re

with open('cross-ref-report-v4.md') as f:
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
        
        # Find all h2 sections
        h2_sections = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
        
        def gen_anchor(text):
            t = text.strip().lower()
            t = re.sub(r'[^\w\s-]', '', t)
            t = re.sub(r'[-\s]+', '-', t)
            t = t.strip('-')
            return t
        
        anchors = [gen_anchor(s) for s in h2_sections]
        
        # Try to find closest match
        target = None
        if anchor.startswith('5.'):
            # My previous fix added a dot incorrectly
            # Find section 5
            for s in h2_sections:
                if re.match(r'^5[\.\s]', s):
                    target = gen_anchor(s)
                    break
        elif anchor.startswith('5-'):
            # Also try to match section 5
            for s in h2_sections:
                if re.match(r'^5[\.\s]', s):
                    a = gen_anchor(s)
                    if a != anchor:
                        target = a
                    break
        
        if target and target != anchor:
            old = '#' + anchor
            new = '#' + target
            if old in content:
                new_content = content.replace(old, new)
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                fixed_count += 1
                print('Fixed ' + old + ' -> ' + new + ' in ' + fp)
            else:
                # Try with regex to handle parentheses variations
                pass
        else:
            # For non-#5 anchors, just check if exact match exists
            pass
    except Exception as e:
        print('ERROR: ' + fp + ' -> ' + str(e))

print('\nTotal fixed: ' + str(fixed_count))
