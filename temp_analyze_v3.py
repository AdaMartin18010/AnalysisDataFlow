import json
from collections import Counter

with open('cross-ref-report-v3.md') as f:
    data = json.load(f)

issues = data.get('issues', [])
anchors = [i for i in issues if i['issue_type'] == 'broken_anchor']

print('Total broken anchors: ' + str(len(anchors)))
print()

anchor_texts = [a['anchor'] for a in anchors]
print('=== TOP ANCHOR PATTERNS ===')
for text, cnt in Counter(anchor_texts).most_common(30):
    print('  ' + str(cnt).rjust(3) + '  ' + text)

print()
files = [a['file_path'] for a in anchors]
print('=== TOP FILES ===')
for fp, cnt in Counter(files).most_common(30):
    print('  ' + str(cnt).rjust(3) + '  ' + fp)
