import json
from collections import Counter

d=json.load(open('code-validation-python-result.json', encoding='utf-8'))
errors = d['p0_errors']

print(f"Remaining errors: {len(errors)}\n")

# 按文件统计
c = Counter(e['file'] for e in errors)
print("Files with most errors:")
for f, n in c.most_common(20):
    print(f"  {f}: {n}")

print("\n\nError types:")
for i, e in enumerate(errors[:30], 1):
    print(f"{i}. {e['file']}")
    print(f"   Line {e.get('line_number', 'N/A')}: {e['error'][:100]}...")
