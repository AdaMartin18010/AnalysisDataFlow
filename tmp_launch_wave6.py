import json

with open('translation-selection-wave6-100.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

items = data['docs']
for i in range(4):
    batch = items[i*25:(i+1)*25]
    print(f'Group {i+1} ({len(batch)} docs):')
    for j, item in enumerate(batch, 1):
        print(f'{j}. {item["Path"]} ({item["SizeKB"]} KB)')
    print()
