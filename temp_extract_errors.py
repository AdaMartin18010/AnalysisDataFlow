import json

with open('cross-ref-report.md') as f:
    data = json.load(f)

print('=== BROKEN LINKS (28) ===')
for i, item in enumerate(data.get('broken_links', []), 1):
    print(f"{i}. {item['file_path']} -> {item['source_link']}")

print()
print('=== BROKEN ANCHORS SAMPLE (first 50 of 202) ===')
for i, item in enumerate(data.get('broken_anchors', [])[:50], 1):
    print(f"{i}. {item['file_path']} -> #{item['anchor']}")

print()
print('=== BROKEN ANCHORS BY FILE ===')
from collections import Counter
files = [item['file_path'] for item in data.get('broken_anchors', [])]
for fp, cnt in Counter(files).most_common(30):
    print(f"  {cnt:3d} {fp}")
