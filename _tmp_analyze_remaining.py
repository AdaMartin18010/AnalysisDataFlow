import json
from collections import Counter

with open('cross-ref-report-v2.json', 'r', encoding='utf-8') as f:
    report = json.load(f)

broken = [i for i in report['issues'] if i['issue_type'] == 'broken_anchor']
anchors = Counter(i['anchor'] for i in broken)

print(f"Total broken anchors: {len(broken)}")
print(f"Unique broken anchors: {len(anchors)}")
print("\nTop 30 broken anchors:")
for anchor, count in anchors.most_common(30):
    print(f"  {count:3d}  #{anchor}")
