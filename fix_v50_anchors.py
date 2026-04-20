import os, re

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    
    def fix_anchor_dashes(match):
        anchor = match.group(1)
        fixed = re.sub(r'-+', '-', anchor)
        return f'](#{fixed})'
    
    content = re.sub(r'\]\(#{1,2}([^)]+)\)', fix_anchor_dashes, content)
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Fix all markdown files in i18n/en/ that might have broken anchors
for root, dirs, files in os.walk('i18n/en'):
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f)
            if fix_file(path):
                print(f'Fixed: {path}')

# Also fix known problematic files
target_files = [
    'Knowledge/06-frontier/veil-framework-production-assessment.md',
    'Struct/06-frontier/iris-coq-state-safety-verification.md',
    'Struct/06-frontier/tla-vs-lean4-expressiveness.md',
    'Knowledge/10-case-studies/iot/case-edge-llm-streaming-production.md',
    'Struct/06-frontier/formal-verification-toolchain-matrix.md',
]

for path in target_files:
    if os.path.exists(path):
        if fix_file(path):
            print(f'Fixed: {path}')
