import json

with open('cross-ref-report.md') as f:
    data = json.load(f)

issues = data.get('issues', [])
blinks = [i for i in issues if i['issue_type'] == 'broken_link']
banchors = [i for i in issues if i['issue_type'] == 'broken_anchor']

print(f'BROKEN LINKS: {len(blinks)}')
for i, item in enumerate(blinks, 1):
    print(f"{i}. {item['file_path']} -> {item['source_link']}")

print()
print(f'BROKEN ANCHORS: {len(banchors)}')
for i, item in enumerate(banchors[:60], 1):
    print(f"{i}. {item['file_path']} -> #{item['anchor']}")
