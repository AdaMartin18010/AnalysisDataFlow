import json
d=json.load(open('code-validation-python-result.json', encoding='utf-8'))
for e in d['p0_errors']:
    if 'case-smart-water-complete' in e['file'] and e['block_index'] == 2:
        print(f"File: {e['file']}")
        print(f"Block: {e['block_index']}, Line: {e.get('line_number', 'N/A')}")
        print(f"Error: {e['error']}")
        print("Code preview:")
        print(e['code_preview'])
        print("\n" + "="*50 + "\n")
