import json
d=json.load(open('code-validation-python-result.json', encoding='utf-8'))
errors = d['p0_errors']
# 过滤掉release目录
errors = [e for e in errors if 'release\\v3.0.0' not in e['file'] and 'release/v3.0.0' not in e['file']]
print(f"Remaining non-release errors: {len(errors)}\n")
for i, e in enumerate(errors, 1):
    print(f"{i}. {e['file']} (Block #{e['block_index']})")
    print(f"   Error: {e['error'][:120]}")
