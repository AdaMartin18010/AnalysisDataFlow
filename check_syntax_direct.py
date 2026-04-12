import re
import py_compile
import tempfile
import os

with open('Flink-IoT-Authority-Alignment/Phase-13-Water-Management/case-smart-water-complete.md', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'```python\s*\n(.*?)```'
matches = list(re.finditer(pattern, content, re.DOTALL))

# Check block 2
block_idx = 2
code = matches[block_idx].group(1)
lines = code.split('\n')

print(f"Block {block_idx} has {len(lines)} lines")
print("\nLines 15-30:")
for i in range(14, min(30, len(lines))):
    print(f"{i+1}: {repr(lines[i])}")

# Write to temp file
with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
    f.write(code)
    temp_file = f.name

try:
    py_compile.compile(temp_file, doraise=True)
    print("\nSyntax OK!")
except py_compile.PyCompileError as e:
    print(f"\nSyntax Error: {e}")
finally:
    os.unlink(temp_file)
