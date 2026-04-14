import os
import re

SECTION_KEYWORDS = {
    'definitions': ['概念定义', 'Definitions'],
    'properties': ['属性推导', 'Properties'],
    'relations': ['关系建立', 'Relations'],
    'argumentation': ['论证过程', 'Argumentation'],
    'proof': ['形式证明', 'Proof / Engineering', 'Engineering Argument'],
    'examples': ['实例验证', 'Examples'],
    'visualizations': ['可视化', 'Visualizations'],
    'references': ['引用参考', 'References', '参考文献'],
}

EXEMPT_PATTERNS = [
    r'00-INDEX\.md$', r'README\.md$', r'CASE-STUDIES-INDEX\.md$',
    r'PROJECT-TRACKING\.md$', r'AGENTS\.md$', r'CHANGELOG\.md$',
    r'-REPORT\.md$', r'-TRACKING\.md$', r'PROGRESS-TRACKING\.md$',
    r'TASK-ASSIGNMENTS\.md$', r'-cheatsheet\.md$', r'-checklist\.md$',
    r'quick-ref-.*\.md$', r'exercise-.*\.md$', r'-template\.md$',
    r'CODE-RUNNABILITY-NOTES\.md$', r'PERFORMANCE-DATA-NOTES\.md$',
    r'.*-comparison\.md$', r'.*-tracking\.md$', r'.*roadmap.*\.md$',
    r'.*preview\.md$', r'.*migration-guide\.md$',
    r'QUARTERLY-REVIEWS/', r'release/', r'archive/',
    r'\.improvement-tracking/', r'\.tasks/', r'\.github/', r'\.scripts/',
    r'\.templates/', r'\.vscode/', r'advisory-board/', r'badges/',
    r'benchmark-', r'case-studies/', r'COMMUNITY/', r'docker/',
    r'docs/', r'en/', r'examples/', r'i18n/', r'LEARNING-PATHS/',
    r'TECH-RADAR/', r'USTM-F-Reconstruction/',
    r'FORMAL-TO-CODE-MAPPING', r'glossary\.md$',
    r'COMPLETION-REPORT', r'PROGRESS-TRACKING', r'TASK-ASSIGNMENTS',
    r'in-progress', r'_in-progress', r'arroyo-update', r'agent-d-',
    r'formal-methods/', r'formal-proofs/', r'KNOWLEDGE-GRAPH/',
    r'Flink-IoT-Authority-Alignment/',
    r'Proof-Chains-', r'PROOF-CHAINS-INDEX',
    r'00-MASTER-INDEX',
    r'project-supplementation-plan',
    r'research-trends-analysis',
    r'academic-frontier',
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
    if len(content.strip()) < 500:
        return None
    lines = content.split('\n')
    found = {k: False for k in SECTION_KEYWORDS}
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped.startswith('##'):
            continue
        for key, keywords in SECTION_KEYWORDS.items():
            for kw in keywords:
                if kw in line_stripped:
                    found[key] = True
                    break
    missing = [k for k, v in found.items() if not v]
    return missing

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

p0_docs.sort(key=lambda x: -len(x[1]))
print(f"Found {len(p0_docs)} non-exempt docs missing >=3 sections")
print("\nTop P0 candidates:")
for path, missing in p0_docs[:30]:
    print(f"  {path}: missing {len(missing)}")
