import os
import re

files = [
    'phase2-case-studies/banking/11.37.1-realtime-payment.md',
    'phase2-case-studies/manufacturing/11.14.1-predictive-maintenance.md',
    'phase2-case-studies/media/11.20.1-livestreaming.md',
    'phase2-case-studies/retail/11.17.1-realtime-pricing.md',
    'phase2-case-studies/insurance/11.18.1-claims-processing.md',
    'phase2-case-studies/education/11.22.1-online-learning.md',
    'phase2-case-studies/realestate/11.21.1-smart-building.md',
    'phase2-case-studies/telecom/11.9.1-network-traffic.md',
    'phase2-case-studies/petrochemical/11.8.1-pipeline-leak.md',
    'phase2-case-studies/autonomous-driving/11.6.1-sensor-fusion.md',
    'phase2-case-studies/aerospace/11.7.1-flight-data.md',
]

results = []
for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    size = len(content.encode('utf-8'))
    # word count: count Chinese chars + English words
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
    english_words = len(re.findall(r'[a-zA-Z]+', content))
    words = chinese_chars + english_words
    mermaid_blocks = len(re.findall(r'```mermaid', content))
    tables = len(re.findall(r'\n\|[^\n]+\|\n\|[-:]+\|', content))
    code_blocks = len(re.findall(r'```(?:java|python|yaml|sql|json|scala|go|cpp|c\+\+)', content))
    results.append({
        'file': os.path.basename(path),
        'size_kb': round(size/1024, 1),
        'words': words,
        'mermaid': mermaid_blocks,
        'tables': tables,
        'code_blocks': code_blocks,
    })

print(f"{'File':<50} {'Size(KB)':>10} {'Words':>10} {'Mermaid':>8} {'Tables':>8} {'Code':>8}")
for r in results:
    print(f"{r['file']:<50} {r['size_kb']:>10} {r['words']:>10} {r['mermaid']:>8} {r['tables']:>8} {r['code_blocks']:>8}")
