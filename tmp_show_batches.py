import json
with open('translation-selection-next-50.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

items = data['a_layer']
for i in range(5):
    batch = items[i*10:(i+1)*10]
    print(f'Batch {i+1} ({len(batch)} docs):')
    for item in batch:
        print(f"  {item['Path']}")
    print()
