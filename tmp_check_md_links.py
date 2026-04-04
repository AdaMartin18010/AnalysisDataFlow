import os
import re

targets = [
    'Flink/09-language-foundations/05-datastream-v2-api.md',
    'Flink/09-language-foundations/03.01-migration-guide.md',
    'Flink/09-language-foundations/01.03-scala3-type-system-formalization.md',
    'Flink/09-language-foundations/02.01-java-api-from-scala.md',
    'Flink/09-language-foundations/flink-datastream-api-complete-guide.md',
    'Flink/09-language-foundations/flink-language-support-complete-guide.md',
]

link_pattern = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')

for t in targets:
    if not os.path.exists(t):
        print(f'FILE NOT FOUND: {t}')
        continue
    with open(t, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f'\n=== {t} ===')
    for i, line in enumerate(lines, 1):
        for match in link_pattern.finditer(line):
            text, url = match.groups()
            if '.md' in url and not url.startswith('http'):
                # Resolve relative path
                src_dir = os.path.dirname(t)
                target_path = os.path.normpath(os.path.join(src_dir, url.split('#')[0]))
                if not os.path.exists(target_path):
                    print(f'  line {i}: [{text}]({url}) -> MISSING: {target_path}')
