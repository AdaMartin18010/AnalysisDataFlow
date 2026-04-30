import re

path = 'formal-methods/formal-code/lean4/FormalMethods/Logic/Propositional.lean'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the notation definition first
content = content.replace('notation "｢" φ "｣" σ => eval σ φ\n', '')
content = content.replace('notation "｢" φ "｣" σ => eval σ φ', '')

# Replace ｢expr｣ var with eval var expr
# Use a loop to handle overlapping matches
pattern = re.compile(r'｢([^｢｣]*)｣\s*(\w+)')

def replacer(m):
    expr = m.group(1).strip()
    var = m.group(2).strip()
    return f'eval {var} {expr}'

# Keep replacing until no more matches
prev = None
while prev != content:
    prev = content
    content = pattern.sub(replacer, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
