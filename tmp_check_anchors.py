import sys, re
sys.path.insert(0, '.scripts')
from validate_cross_refs_v2 import CrossRefValidator

v = CrossRefValidator('.')

targets = [
    'Flink/09-language-foundations/05-datastream-v2-api.md',
    'Flink/09-language-foundations/03.01-migration-guide.md',
    'Flink/09-language-foundations/01.03-scala3-type-system-formalization.md',
    'Flink/09-language-foundations/flink-datastream-api-complete-guide.md',
]

for t in targets:
    with open(t, 'r', encoding='utf-8') as f:
        content = f.read()
    v.anchors.clear()
    v.extract_anchors(content, t)
    print(f'\n=== {t} ===')
    for anchor in sorted(v.anchors.get(t, set())):
        print(f'  {anchor}')
