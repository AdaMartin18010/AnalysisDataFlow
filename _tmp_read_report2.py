import json
with open('cross-ref-report-v2.json', 'r', encoding='utf-8') as f:
    report = json.load(f)
for issue in report['issues']:
    if issue['issue_type'] == 'broken_anchor' and 'watermark' in issue['file_path'].lower():
        print(f"source_link: {issue['source_link']}")
        print(f"file_path: {issue['file_path']}")
        print(f"target_path: {issue['target_path']}")
        print(f"anchor: {issue['anchor']}")
