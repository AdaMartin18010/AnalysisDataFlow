path = 'formal-methods/formal-code/lean4/FormalMethods/Logic/Propositional.lean'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('notation "⟦" φ "⟧" σ => eval σ φ', 'notation "｢" φ "｣" σ => eval σ φ')
content = content.replace('⟦', '｢')
content = content.replace('⟧', '｣')
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
