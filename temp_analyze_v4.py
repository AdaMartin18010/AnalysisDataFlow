import json
from collections import Counter

with open('cross-ref-report-v4.md') as f:
    data = json.load(f)

issues = data.get('issues', [])
anchors = [i for i in issues if i['issue_type'] == 'broken_anchor']

print('Total broken anchors: ' + str(len(anchors)))
print()

anchor_texts = [a['anchor'] for a in anchors]
print('=== TOP ANCHOR PATTERNS ===')
for text, cnt in Counter(anchor_texts).most_common(30):
    print('  ' + str(cnt).rjust(3) + '  ' + text)
