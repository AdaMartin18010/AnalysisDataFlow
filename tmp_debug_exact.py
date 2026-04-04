import re
from pathlib import Path

base_dir = Path('.')
file_path = 'Flink/09-language-foundations/05-datastream-v2-api.md'
full_path = base_dir / file_path

with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Exact copy of validator's _get_code_ranges
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

inline_pattern = r'`[^`]*`'
inline_ranges = []
for match in re.finditer(inline_pattern, content):
    start, end = match.start(), match.end()
    if any(rs <= start and end <= re for rs, re in ranges):
        continue
    inline_ranges.append((start, end))

all_ranges = ranges + inline_ranges

# Exact copy of validator's extract_links
link_pattern = r'\[([^\]]*?)\]\(([^)]+)\)'
found_links = []
for match in re.finditer(link_pattern, content):
    in_range = any(rs <= match.start() and match.end() <= re for rs, re in all_ranges)
    if in_range:
        continue
    
    link_text = match.group(1)
    link_url = match.group(2)
    
    if '\n' in link_text and 'classOf' in link_url:
        continue
    if 'classOf' in link_url or 'Duration.of' in link_url:
        continue
    if link_url.startswith('#'):
        continue
    if link_url.startswith('http://') or link_url.startswith('https://'):
        continue
    
    line_num = content[:match.start()].count('\n') + 1
    found_links.append((line_num, link_text, link_url, match.group(0)))

print(f'Found {len(found_links)} non-code internal links:')
for line, text, url, full in found_links:
    print(f'  line {line}: [{text}]({url})')
