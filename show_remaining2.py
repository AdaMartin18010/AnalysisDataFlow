import json
d=json.load(open('code-validation-python-result.json', encoding='utf-8'))
errors = d['p0_errors']
errors = [e for e in errors if 'release\\v3.0.0' not in e['file'] and 'release/v3.0.0' not in e['file']]
print(f"Remaining errors: {len(errors)}\n")
for e in errors:
    print(f"File: {e['file']}")
    print(f"Block: {e['block_index']}, Line: {e.get('line_number', 'N/A')}")
    print(f"Error: {e['error']}")
