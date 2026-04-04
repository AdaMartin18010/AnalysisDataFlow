import sys
sys.path.insert(0, '.scripts')
from validate_cross_refs_v2 import CrossRefValidator

v = CrossRefValidator('.')
v.collect_files()

# Monkey-patch extract_links to print all found links before filtering
orig_extract_links = v.extract_links
captured_links = []

def patched_extract_links(content, file_path):
    import re
    link_pattern = r'\[([^\]]*?)\]\(([^)]+)\)'
    code_ranges = v._get_code_ranges(content)
    for match in re.finditer(link_pattern, content):
        in_range = any(rs <= match.start() and match.end() <= re for rs, re in code_ranges)
        line = content[:match.start()].count('\n') + 1
        if file_path == 'Flink/09-language-foundations/05-datastream-v2-api.md' and line in [75, 91, 171]:
            captured_links.append({
                'line': line,
                'text': match.group(1),
                'url': match.group(2),
                'in_code': in_range,
                'raw': match.group(0)
            })
    orig_extract_links(content, file_path)

v.extract_links = patched_extract_links
v.scan_all_files()
v.validate_links()

print('Captured links for 05-datastream-v2-api.md lines 75, 91, 171:')
for link in captured_links:
    print(link)

print(f'\nTotal errors for target: {len([e for e in v.errors if e["source"] == "Flink/09-language-foundations/05-datastream-v2-api.md"])}')
for e in v.errors:
    if e['source'] == 'Flink/09-language-foundations/05-datastream-v2-api.md':
        print(f"  line {e['line']}: type={e['type']} url={e.get('url','')}")
