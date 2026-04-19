import json
from collections import Counter

with open('cross-ref-report-v5.md') as f:
    data = json.load(f)

issues = [i for i in data.get('issues', []) if i['issue_type'] == 'broken_anchor']

print('Total broken anchors: ' + str(len(issues)))
print()

anchor_texts = [a['anchor'] for a in issues]
print('=== TOP ANCHOR PATTERNS ===')
for text, cnt in Counter(anchor_texts).most_common(40):
    print('  ' + str(cnt).rjust(3) + '  ' + text)
