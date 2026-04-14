import csv
import json
from pathlib import Path
import random

with open('all_zh_docs.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    docs = list(reader)

c_layer_patterns = [
    '04-proofs', 'proof', 'bisimulation', 'type-safety', 'correctness-proof',
    'formal-verification', 'dot-subtyping', 'deadlock-freedom', 'chandy-lamport-consistency'
]

b_layer_patterns = [
    'design-patterns', 'concept-atlas', 'best-practices', 'architecture',
    'mechanism-deep-dive', 'exactly-once-semantics', 'checkpoint-mechanism',
    'watermark', 'consistency-hierarchy', 'state-backend', 'fault-tolerance',
    'performance-tuning', 'migration', 'technology-selection'
]

a_layer_patterns = [
    '00-INDEX', 'INDEX', 'README', 'QUICK-START', 'overview', 'guide', 'tutorial',
    'connector', 'cep', 'sql', 'table-api', 'deployment', 'checklist', 'case-study',
    'introduction', 'getting-started', 'roadmap', 'faq', 'glossary', 'comparison',
    'vs-', 'competitor', 'benchmark', 'learning-path', 'recommender'
]

def classify_doc(path):
    p = path.lower()
    if any(pat in p for pat in c_layer_patterns):
        return 'C'
    if any(pat in p for pat in b_layer_patterns):
        return 'B'
    if any(pat in p for pat in a_layer_patterns):
        return 'A'
    if 'Struct/01-foundation' in path or 'Struct/02-properties' in path or 'Struct/03-relationships' in path:
        return 'B'
    if 'Struct/' in path:
        return 'C'
    if 'Knowledge/06-frontier' in path or 'Knowledge/08-standards' in path or 'Knowledge/09-anti-patterns' in path:
        return 'A'
    if 'Flink/01-concepts' in path or 'Flink/02-core' in path:
        return 'B'
    if 'Flink/03-api' in path or 'Flink/04-connectors' in path or 'Flink/06-engineering' in path or 'Flink/07-case-studies' in path:
        return 'A'
    if 'Flink/05-vs-competitors' in path or 'Flink/08-roadmap' in path or 'Flink/10-deployment' in path:
        return 'A'
    return 'A'

categorized = {'A': [], 'B': [], 'C': []}
for d in docs:
    d['layer'] = classify_doc(d['Path'])
    categorized[d['layer']].append(d)

print('A-layer candidates: %d' % len(categorized['A']))
print('B-layer candidates: %d' % len(categorized['B']))
print('C-layer candidates: %d' % len(categorized['C']))

a_candidates = [d for d in categorized['A'] if float(d['SizeKB']) < 50]
a_candidates.sort(key=lambda x: float(x['SizeKB']))

def pick_diverse(docs, count):
    selected = []
    used_dirs = set()
    for d in docs:
        parts = d['Path'].split('/')
        parent = parts[1] if len(parts) > 1 else 'root'
        if parent not in used_dirs and len(selected) < count:
            selected.append(d)
            used_dirs.add(parent)
    for d in docs:
        if d not in selected and len(selected) < count:
            selected.append(d)
    return selected

a_selected = pick_diverse(a_candidates, 50)

b_candidates = [d for d in categorized['B'] if 5 < float(d['SizeKB']) < 80]
b_candidates.sort(key=lambda x: float(x['SizeKB']))
b_selected = pick_diverse(b_candidates, 10)

selection = {
    'generated_at': '2026-04-15',
    'a_layer': a_selected,
    'b_layer': b_selected
}

with open('translation-selection.json', 'w', encoding='utf-8') as f:
    json.dump(selection, f, ensure_ascii=False, indent=2)

print('Selected A-layer: %d' % len(a_selected))
print('Selected B-layer: %d' % len(b_selected))
print('Saved to translation-selection.json')
