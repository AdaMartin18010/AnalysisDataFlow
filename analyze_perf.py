import re
with open('Flink/09-practices/09.02-benchmarking/performance-benchmark-suite.md', 'r', encoding='utf-8') as f:
    content = f.read()
pattern = r'```python\s*\n(.*?)```'
matches = list(re.finditer(pattern, content, re.DOTALL))
print(f'Total python blocks: {len(matches)}')
for i in [0, 1]:
    code = matches[i].group(1)
    lines = code.split('\n')
    print(f'\nBlock {i}: {len(lines)} lines')
    print('Lines around error:')
    for j in range(19, min(25, len(lines))):
        print(f'{j+1}: {repr(lines[j])}')
