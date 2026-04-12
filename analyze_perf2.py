import re
with open('Flink/09-practices/09.02-benchmarking/performance-benchmark-suite.md', 'r', encoding='utf-8') as f:
    content = f.read()
pattern = r'```python\s*\n(.*?)```'
matches = list(re.finditer(pattern, content, re.DOTALL))
code = matches[1].group(1)
lines = code.split('\n')
print(f'Block 1: {len(lines)} lines')
print('Lines around 185-195:')
for j in range(184, min(195, len(lines))):
    print(f'{j+1}: {repr(lines[j])}')
