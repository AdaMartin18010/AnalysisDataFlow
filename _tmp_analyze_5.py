import json

with open('cross-ref-report-v2.json', 'r', encoding='utf-8') as f:
    report = json.load(f)

for issue in report['issues']:
    if issue['issue_type'] == 'broken_anchor' and issue['anchor'] == '5':
        print(f"{issue['file_path']}:{issue['line_number']} -> {issue['target_path']}#{issue['anchor']}")
        print(f"  source_link: {issue['source_link']}")
