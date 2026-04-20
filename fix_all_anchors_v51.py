import os, re

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    
    def fix_anchor(match):
        anchor = match.group(1)
        # Replace double dashes in anchors only
        while '--' in anchor:
            anchor = anchor.replace('--', '-')
        return f'](#{anchor})'
    
    # Fix markdown link anchors
    content = re.sub(r'\]\(#{1,2}([^)]+)\)', fix_anchor, content)
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

target_files = [
    'Flink/08-roadmap/08.01-flink-24/flink-2.1-frontier-tracking.md',
    'Struct/06-frontier/flink-2x-async-state-formalization.md',
    'Knowledge/06-frontier/llm-assisted-stream-processing-optimization.md',
    'Knowledge/10-case-studies/iot/case-edge-llm-streaming-production.md',
    'Flink/08-roadmap/08.01-flink-24/flink-version-evolution-complete-guide.md',
    'Knowledge/06-frontier/veil-framework-production-assessment.md',
    'Knowledge/06-frontier/streaming-vector-db-frontier-2026.md',
    'Struct/06-frontier/iris-coq-state-safety-verification.md',
    'Struct/06-frontier/tla-vs-lean4-expressiveness.md',
    'Knowledge/06-frontier/formal-verification-toolchain-matrix.md',
]

fixed = []
for path in target_files:
    if os.path.exists(path):
        if fix_file(path):
            fixed.append(path)
            print(f'Fixed: {path}')
    else:
        print(f'Not found: {path}')

# Scan all markdown for remaining double-dash anchors
for root, dirs, files in os.walk('i18n/en'):
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f)
            if path not in target_files and fix_file(path):
                fixed.append(path)

for root, dirs, files in os.walk('Flink'):
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f)
            if path not in target_files and fix_file(path):
                fixed.append(path)

for root, dirs, files in os.walk('Struct'):
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f)
            if path not in target_files and fix_file(path):
                fixed.append(path)

for root, dirs, files in os.walk('Knowledge'):
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f)
            if path not in target_files and fix_file(path):
                fixed.append(path)

print(f'\nTotal fixed: {len(fixed)} files')
