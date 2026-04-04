with open('Flink/09-language-foundations/05-datastream-v2-api.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_code = False
for i, line in enumerate(lines, 1):
    stripped = line.lstrip()
    if stripped.startswith('```'):
        was = in_code
        in_code = not in_code
        print(f'{i}: in_code={in_code} (was {was}) | {repr(line.rstrip())}')

print(f'Final in_code={in_code}')
