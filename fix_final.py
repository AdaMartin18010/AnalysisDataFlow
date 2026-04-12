with open('Flink/09-practices/09.02-benchmarking/performance-benchmark-suite.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the remaining error
content = content.replace(
    'for result in sorted(self.data["checkpoint",:\n                            key=lambda x: x.get("state_size_mb", 0)):',
    'for result in sorted(self.data["checkpoint"],\n                            key=lambda x: x.get("state_size_mb", 0)):')

with open('Flink/09-practices/09.02-benchmarking/performance-benchmark-suite.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed!")
