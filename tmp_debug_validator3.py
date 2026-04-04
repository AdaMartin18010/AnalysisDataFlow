import sys, json
sys.path.insert(0, '.scripts')
from validate_cross_refs_v2 import CrossRefValidator

v = CrossRefValidator('.')
v.collect_files()
v.scan_all_files()
v.validate_links()
v.identify_fixable_errors()

# Build the report the same way
errors_by_source = {}
for err in v.errors:
    src = err['source']
    if src not in errors_by_source:
        errors_by_source[src] = []
    errors_by_source[src].append(err)

t = 'Flink/09-language-foundations/05-datastream-v2-api.md'
print(f'Errors in v.errors for {t}: {len([e for e in v.errors if e["source"] == t])}')
print(f'Errors in errors_by_source for {t}: {len(errors_by_source.get(t, []))}')
for e in errors_by_source.get(t, []):
    print(f"  line {e['line']}: type={e['type']} url={e.get('url','')}")
