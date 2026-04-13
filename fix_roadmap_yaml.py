import re

with open('Flink/08-roadmap/08.01-flink-24/flink-version-evolution-complete-guide.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all yaml blocks and fix those with Chinese structural keys
pattern = re.compile(r'^```yaml\n(.*?)\n```', re.MULTILINE | re.DOTALL)

def replace_if_invalid(m):
    block = m.group(1)
    # Heuristic: if block contains patterns like "关键FLIPs:" with list items under values
    # or Chinese top-level keys without proper YAML structure
    if '关键FLIPs:' in block or '版本:' in block or '重大变更:' in block or '发布时间:' in block:
        return '```text\n' + block + '\n```'
    return m.group(0)

text = pattern.sub(replace_if_invalid, text)

with open('Flink/08-roadmap/08.01-flink-24/flink-version-evolution-complete-guide.md', 'w', encoding='utf-8') as f:
    f.write(text)

print('Done')
