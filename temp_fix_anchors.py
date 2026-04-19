import json
import re

with open('cross-ref-report.md') as f:
    data = json.load(f)

issues = [i for i in data.get('issues', []) if i['issue_type'] == 'broken_anchor']

# Pattern 1: #5-形式证明--工程论证-proof--engineering-argument
# Replace with just #5 (which should match most documents' 5th section)
pattern1_files = set()
for issue in issues:
    if issue['anchor'] in ['5-形式证明--工程论证-proof--engineering-argument', '5-形式证明--工程论证']:
        fp = issue['file_path']
        pattern1_files.add(fp)

print('Pattern 1 files to fix: ' + str(len(pattern1_files)))
for fp in sorted(pattern1_files)[:10]:
    print('  ' + fp)

# Check if these files actually have a section 5
import os
for fp in sorted(pattern1_files)[:5]:
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        has_section5 = bool(re.search(r'^##\s*5[\.\s]', content, re.MULTILINE))
        print(fp + ' has_section5=' + str(has_section5))
    except Exception as e:
        print('Error reading ' + fp + ': ' + str(e))
