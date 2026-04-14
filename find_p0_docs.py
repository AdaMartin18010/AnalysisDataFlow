import os
import re
from pathlib import Path

# 六段式核心章节（支持多种变体）
SECTION_PATTERNS = {
    'definitions': re.compile(r'^##\s+1\.\s*.*概念定义|Definitions.*', re.I),
    'properties': re.compile(r'^##\s+2\.\s*.*属性推导|Properties.*', re.I),
    'relations': re.compile(r'^##\s+3\.\s*.*关系建立|Relations.*', re.I),
    'argumentation': re.compile(r'^##\s+4\.\s*.*论证过程|Argumentation.*', re.I),
    'proof': re.compile(r'^##\s+5\.\s*.*形式证明|Proof|Engineering Argument.*', re.I),
    'examples': re.compile(r'^##\s+6\.\s*.*实例验证|Examples.*', re.I),
    'visualizations': re.compile(r'^##\s+7\.\s*.*可视化|Visualizations.*', re.I),
    'references': re.compile(r'^##\s+8\.\s*.*引用参考|References.*', re.I),
}

EXEMPT_PATTERNS = [
    r'00-INDEX\.md$',
    r'README\.md$',
    r'CASE-STUDIES-INDEX\.md$',
    r'PROJECT-TRACKING\.md$',
    r'AGENTS\.md$',
    r'CHANGELOG\.md$',
    r'-REPORT\.md$',
    r'-TRACKING\.md$',
    r'PROGRESS-TRACKING\.md$',
    r'TASK-ASSIGNMENTS\.md$',
    r'-cheatsheet\.md$',
    r'-checklist\.md$',
    r'quick-ref-.*\.md$',
    r'exercise-.*\.md$',
    r'-template\.md$',
    r'CODE-RUNNABILITY-NOTES\.md$',
    r'PERFORMANCE-DATA-NOTES\.md$',
    r'.*-comparison\.md$',
    r'.*-tracking\.md$',
    r'.*roadmap.*\.md$',
    r'.*preview\.md$',
    r'.*migration-guide\.md$',
    r'QUARTERLY-REVIEWS/',
    r'release/',
    r'archive/',
    r'\.improvement-tracking/',
    r'\.tasks/',
    r'\.github/',
    r'\.scripts/',
    r'\.templates/',
    r'\.vscode/',
    r'advisory-board/',
    r'badges/',
    r'benchmark-',
    r'case-studies/',
    r'COMMUNITY/',
    r'docker/',
    r'docs/',
    r'en/',
    r'examples/',
    r'i18n/',
    r'LEARNING-PATHS/',
    r'TECH-RADAR/',
    r'USTM-F-Reconstruction/',
    r'FORMAL-TO-CODE-MAPPING',
    r'glossary\.md$',
    r'COMPLETION-REPORT',
    r'PROGRESS-TRACKING',
    r'TASK-ASSIGNMENTS',
    r'in-progress',
    r'_in-progress',
    r'arroyo-update',
    r'agent-d-',
    r'formal-methods/',
    r'formal-proofs/',
    r'KNOWLEDGE-GRAPH/',
    r'Flink-IoT-Authority-Alignment/',
]

def is_exempt(path):
    p = path.replace('\\', '/')
    for pat in EXEMPT_PATTERNS:
        if re.search(pat, p, re.I):
            return True
    return False

def check_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return None
    
    # Skip very short files
    if len(content.strip()) < 500:
        return None
    
    lines = content.split('\n')
    found = {k: False for k in SECTION_PATTERNS}
    for line in lines:
        for key, pat in SECTION_PATTERNS.items():
            if pat.match(line.strip()):
                found[key] = True
    
    missing = [k for k, v in found.items() if not v]
    return missing

# Scan
scan_dirs = ['Struct', 'Knowledge', 'Flink']
p0_docs = []

for scan_dir in scan_dirs:
    if not os.path.exists(scan_dir):
        continue
    for root, _, files in os.walk(scan_dir):
        for fname in files:
            if not fname.endswith('.md'):
                continue
            path = os.path.join(root, fname)
            if is_exempt(path):
                continue
            missing = check_file(path)
            if missing and len(missing) >= 3:
                p0_docs.append((path, missing))

# Sort by missing count desc
p0_docs.sort(key=lambda x: -len(x[1]))

print(f"Found {len(p0_docs)} non-exempt docs missing >=3 sections")
print("\nTop P0 candidates:")
for path, missing in p0_docs[:20]:
    print(f"  {path}: missing {len(missing)} -> {', '.join(missing)}")
