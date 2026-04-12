import json
d=json.load(open('code-validation-python-result.json', encoding='utf-8'))
errors = d['p0_errors']
print(f"Total errors: {len(errors)}\n")
for i, e in enumerate(errors, 1):
    print(f"{i}. {e['file']} (Block #{e['block_index']}, Line {e.get('line_number', 'N/A')})")
    print(f"   Error: {e['error'][:150]}")
    print()
