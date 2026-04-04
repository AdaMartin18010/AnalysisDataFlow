import json

with open('.stats/cross_ref_report_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

targets = [
    'Flink/09-language-foundations/05-datastream-v2-api.md',
    'Flink/09-language-foundations/03.01-migration-guide.md',
    'Flink/09-language-foundations/01.03-scala3-type-system-formalization.md',
    'Flink/09-language-foundations/02.01-java-api-from-scala.md',
    'Flink/09-language-foundations/flink-datastream-api-complete-guide.md',
    'Flink/09-language-foundations/flink-language-support-complete-guide.md',
]

for t in targets:
    errs = data['errors_by_source'].get(t, [])
    print(f'\n=== {t} ({len(errs)} errors) ===')
    for err in errs:
        url = err.get('url', '')
        if '.md' in url or '#' in url:
            print(f'  line {err.get("line", "?")}: [{err.get("text", "")}]({url}) type={err.get("type", "")}')
        else:
            print(f'  line {err.get("line", "?")}: [{err.get("text", "")}]({url}) type={err.get("type", "")} [NON-MD]')
