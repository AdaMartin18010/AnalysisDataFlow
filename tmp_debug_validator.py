import re

with open('Flink/09-language-foundations/05-datastream-v2-api.md', 'r', encoding='utf-8') as f:
    content = f.read()

ranges = []
fence_pattern = r'^```.*?$'
in_code = False
code_start = 0
for match in re.finditer(fence_pattern, content, re.MULTILINE):
    if not in_code:
        code_start = match.start()
        in_code = True
    else:
        ranges.append((code_start, match.end()))
        in_code = False

print(f'Total code ranges: {len(ranges)}')
for rs, re_end in ranges[:10]:
    start_line = content[:rs].count('\n') + 1
    end_line = content[:re_end].count('\n') + 1
    print(f'  Lines {start_line}-{end_line}: ({rs}, {re_end})')

# Check line 75 specifically
line_75_start = content.find('valueState[Long]("counter")')
if line_75_start >= 0:
    in_range = any(rs <= line_75_start and (line_75_start + len('valueState[Long]("counter")')) <= re_end for rs, re_end in ranges)
    print(f'Line 75 link in code range: {in_range}')
    # Find which range it might be in
    for rs, re_end in ranges:
        if rs <= line_75_start <= re_end:
            start_line = content[:rs].count('\n') + 1
            end_line = content[:re_end].count('\n') + 1
            print(f'  Line 75 is in range lines {start_line}-{end_line}')

# Also check the inline code ranges
inline_pattern = r'`[^`]*`'
inline_ranges = []
for match in re.finditer(inline_pattern, content):
    start, end = match.start(), match.end()
    if any(rs <= start and end <= re for rs, re in ranges):
        continue
    inline_ranges.append((start, end))

print(f'Inline code ranges: {len(inline_ranges)}')
