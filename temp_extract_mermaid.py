import json

with open('mermaid-report.md') as f:
    data = json.load(f)

errors = [d for d in data.get('diagrams', []) if d.get('has_syntax_error')]
print(f'=== MERMAID SYNTAX ERRORS ({len(errors)}) ===')
for i, e in enumerate(errors, 1):
    print(f"{i}. {e['file_path']}:{e['line_start']} - {e['error_message']}")

print()
print('=== FILES WITH ERRORS ===')
files = [e['file_path'] for e in errors]
from collections import Counter
for fp, cnt in Counter(files).most_common(30):
    print(f"  {cnt} {fp}")
