import json

with open('translation-selection-wave3-50.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

items = data['a_layer']
for i in range(5):
    batch = items[i*10:(i+1)*10]
    print(f'Batch {i+1} ({len(batch)} docs):')
    for j, item in enumerate(batch, 1):
        print(f'{j}. {item["Path"]}')
    print()
