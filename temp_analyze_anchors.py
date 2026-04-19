import json
from collections import Counter

with open('cross-ref-report.md') as f:
    data = json.load(f)

issues = data.get('issues', [])
anchors = [i for i in issues if i['issue_type'] == 'broken_anchor']

print(f'Total broken anchors: {len(anchors)}')
print()

# Group by anchor text
anchor_texts = [a['anchor'] for a in anchors]
print('=== TOP ANCHOR PATTERNS ===')
for text, cnt in Counter(anchor_texts).most_common(30):
    print(f'  {cnt:3d}  {text}')

print()

# Group by file
files = [a['file_path'] for a in anchors]
print('=== TOP FILES ===')
for fp, cnt in Counter(files).most_common(30):
    print(f'  {cnt:3d}  {fp}')
