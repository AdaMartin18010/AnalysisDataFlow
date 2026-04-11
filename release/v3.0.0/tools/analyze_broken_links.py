import json
import os

with open('broken_links_full.json', 'r', encoding='utf-8') as f:
    links = json.load(f)

# 分类断链
code_false_positives = []
file_not_found = []
possible_moves = []

for link in links:
    url = link['url']
    # 检测代码片段误报 - 这些是在Markdown表格或代码块中的误解析
    if any(c in url for c in ['`', '\n', 'classOf', '=>', 'StateDeclaration', 'StreamKey', '|']):
        code_false_positives.append(link)
    elif url.startswith('./') or url.startswith('../') or (not url.startswith(('http', '#', 'mailto')) and '.md' in url.lower()):
        file_not_found.append(link)
    else:
        possible_moves.append(link)

print('=== 断链分析统计 ===')
print(f'代码片段误报（可忽略）: {len(code_false_positives)}')
print(f'真实文件缺失: {len(file_not_found)}')
print(f'其他: {len(possible_moves)}')
print()

# 分析真实文件缺失的模式 - 按源文件分组
by_source = {}
for link in file_not_found:
    src = link['source']
    if src not in by_source:
        by_source[src] = []
    by_source[src].append(link)

print(f'=== 涉及 {len(by_source)} 个源文件的断链 ===')
for src, links in sorted(by_source.items(), key=lambda x: -len(x[1]))[:20]:
    print(f'{src}: {len(links)} 个断链')
print()

# 分析常见的断链目标模式
print('=== 常见的断链目标 ===')
target_counts = {}
for link in file_not_found:
    target = link['url']
    target_counts[target] = target_counts.get(target, 0) + 1

for target, count in sorted(target_counts.items(), key=lambda x: -x[1])[:20]:
    print(f'{count}x: {target}')
print()

# 保存真实需要修复的链接
with open('broken_links_real.json', 'w', encoding='utf-8') as f:
    json.dump(file_not_found, f, ensure_ascii=False, indent=2)
print(f'真实断链已保存到 broken_links_real.json ({len(file_not_found)} 个)')
