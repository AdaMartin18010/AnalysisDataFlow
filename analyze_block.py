import re
with open('Flink-IoT-Authority-Alignment/Phase-13-Water-Management/case-smart-water-complete.md', 'r', encoding='utf-8') as f:
    content = f.read()
pattern = r'```python\s*\n(.*?)```'
matches = list(re.finditer(pattern, content, re.DOTALL))
print(f'Total python blocks: {len(matches)}')
for i, m in enumerate(matches):
    code = m.group(1)
    lines = code.split('\n')
    print(f'Block {i}: {len(lines)} lines')
    if i == 2:
        print('\nLast 5 lines of block 2:')
        for line in lines[-5:]:
            print(repr(line))
