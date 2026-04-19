import json
with open('cross-ref-report.md') as f:
    data = json.load(f)
issues = [i for i in data.get('issues', []) if i['issue_type'] == 'broken_anchor' and i['anchor'] == '5-形式证明--工程论证-proof--engineering-argument']
print('Files with broken anchor #5:')
for i in issues[:20]:
    print('  ' + i['file_path'] + ' -> ' + i['source_link'])
print('Total: ' + str(len(issues)))
