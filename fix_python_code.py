#!/usr/bin/env python3
"""
修复Python代码示例中的语法错误
"""

import json
import re
import os

# 加载错误数据
with open('code-validation-python-result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

errors = data['p0_errors']

# 按文件分组错误
errors_by_file = {}
for err in errors:
    file = err['file']
    if file not in errors_by_file:
        errors_by_file[file] = []
    errors_by_file[file].append(err)

print(f"需要修复 {len(errors_by_file)} 个文件中的 {len(errors)} 个错误")

# 修复统计
fixed_count = 0
skipped_count = 0

# 修复函数
def fix_file(file_path, file_errors):
    global fixed_count, skipped_count
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"  无法读取文件 {file_path}: {e}")
        return False
    
    original_content = content
    
    # 按block_index降序排序，以便从后向前替换
    file_errors.sort(key=lambda x: x['block_index'], reverse=True)
    
    for err in file_errors:
        block_idx = err['block_index']
        error_msg = err['error']
        
        # 提取代码块
        pattern = r'```python\s*\n(.*?)```'
        matches = list(re.finditer(pattern, content, re.DOTALL))
        
        if block_idx >= len(matches):
            pattern2 = r'```py\s*\n(.*?)```'
            matches2 = list(re.finditer(pattern2, content, re.DOTALL))
            matches.extend(matches2)
        
        if block_idx >= len(matches):
            print(f"  无法找到代码块 #{block_idx} in {file_path}")
            skipped_count += 1
            continue
        
        match = matches[block_idx]
        code = match.group(1)
        start, end = match.start(), match.end()
        
        # 判断错误类型并修复
        fixed = False
        new_block = None
        
        # 类型1: 伪代码/说明性文字（包含明显非Python语法）
        if any(kw in code for kw in ['Day 1-2:', 'Day 5-7:', '✅', '⊕', 'apply H to', ':=', '1MB', '1mm', '5s', 'apache-flink==']):
            # 改为text标记
            new_block = f'```text\n{code}```'
            fixed = True
            print(f"  [{file_path}] Block #{block_idx}: 伪代码 → text")
        
        # 类型2: 缩进错误
        elif 'IndentationError' in error_msg:
            # 尝试修复缩进
            lines = code.split('\n')
            if len(lines) > 1:
                # 找到第一个非空行的缩进
                base_indent = None
                for line in lines:
                    if line.strip():
                        base_indent = len(line) - len(line.lstrip())
                        break
                
                if base_indent and base_indent > 0:
                    # 移除公共缩进
                    fixed_lines = []
                    for line in lines:
                        if line.strip():
                            if line.startswith(' ' * base_indent):
                                fixed_lines.append(line[base_indent:])
                            else:
                                fixed_lines.append(line)
                        else:
                            fixed_lines.append(line)
                    new_code = '\n'.join(fixed_lines)
                    new_block = f'```python\n{new_code}```'
                    fixed = True
                    print(f"  [{file_path}] Block #{block_idx}: 修复缩进")
        
        # 类型3: 函数定义不完整 (def func(:)
        elif 'def __init__(:' in code or 'def fuse_inventory(:' in code or 'def combine_evidence(:' in code:
            # 这些是故意截断的示例，改为text
            new_block = f'```text\n{code}```'
            fixed = True
            print(f"  [{file_path}] Block #{block_idx}: 不完整函数定义 → text")
        
        # 类型4: session types 语法
        elif 'Channel[!int.?bool' in code or '├' in code:
            new_block = f'```text\n{code}```'
            fixed = True
            print(f"  [{file_path}] Block #{block_idx}: session types → text")
        
        # 类型5: list comprehension 不完整
        elif code.count('[') != code.count(']'):
            # 尝试补全
            if code.rstrip().endswith(','):
                new_code = code.rstrip()[:-1] + ']'
                new_block = f'```python\n{new_code}```'
                fixed = True
                print(f"  [{file_path}] Block #{block_idx}: 补全列表推导式")
        
        # 类型6: 中文标点符号
        elif '，' in code or '（' in code or '）' in code:
            # 替换中文标点
            new_code = code.replace('，', ',').replace('（', '(').replace('）', ')').replace('：', ':')
            new_block = f'```python\n{new_code}```'
            fixed = True
            print(f"  [{file_path}] Block #{block_idx}: 中文标点 → 英文标点")
        
        # 类型7: 缺少 else 的 conditional expression
        elif 'if' in code and 'else' not in code and 'invalid syntax' in error_msg:
            # 可能是伪代码
            new_block = f'```text\n{code}```'
            fixed = True
            print(f"  [{file_path}] Block #{block_idx}: 不完整条件表达式 → text")
        
        # 类型8: YAML格式误标为Python
        elif 'labels:' in code and 'Response:' in code:
            new_block = f'```yaml\n{code}```'
            fixed = True
            print(f"  [{file_path}] Block #{block_idx}: YAML → yaml")
        
        # 应用修复
        if fixed and new_block:
            content = content[:start] + new_block + content[end:]
            fixed_count += 1
        else:
            print(f"  [{file_path}] Block #{block_idx}: 未修复 (未知错误类型)")
            skipped_count += 1
    
    # 写回文件
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# 处理每个文件
modified_files = []
for file_path in sorted(errors_by_file.keys()):
    # 跳过 release 目录（归档版本不需要修复）
    if 'release\\v3.0.0' in file_path or 'release/v3.0.0' in file_path:
        print(f"跳过归档文件: {file_path}")
        continue
    
    print(f"处理: {file_path}")
    if fix_file(file_path, errors_by_file[file_path]):
        modified_files.append(file_path)

print(f"\n修复完成!")
print(f"  修复错误: {fixed_count}")
print(f"  跳过错误: {skipped_count}")
print(f"  修改文件: {len(modified_files)}")

# 保存修改的文件列表
with open('fixed_python_files.txt', 'w', encoding='utf-8') as f:
    for fp in modified_files:
        f.write(fp + '\n')
print(f"修改文件列表已保存: fixed_python_files.txt")
