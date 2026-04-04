#!/usr/bin/env python3
"""批量修复 Markdown 锚点引用"""

import re
import json

def slugify(text):
    """将文本转换为 GitHub 风格的锚点"""
    # 移除特殊符号但保留中文字符、字母、数字和空格
    text = re.sub(r'[`~!@#$%^&*()+=\[\]{}\\|;:\'",.<>/?！？。，、；：""''（）【】《》]', '', text)
    # 将空格替换为 -
    text = text.replace(' ', '-')
    # 移除连续的 -
    text = re.sub(r'-+', '-', text)
    # 移除首尾的 -
    text = text.strip('-')
    return text.lower()

def fix_anchor_in_file(filepath, wrong_anchor, correct_anchor):
    """修复文件中的锚点引用"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找并替换锚点
        original = content
        content = content.replace(f'](#{wrong_anchor})', f'](#{correct_anchor})')
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

# 加载错误报告
with open('.stats/cross_ref_report_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

anchors = data['errors_by_category']['anchor_not_found']

# 统计修复情况
fixed_count = 0
failed_count = 0

for error in anchors:
    source = error['source']
    anchor = error['anchor']
    text = error.get('text', '')
    
    # 生成正确的锚点
    if text:
        correct_anchor = slugify(text)
        if correct_anchor != anchor.lower():
            if fix_anchor_in_file(source, anchor, correct_anchor):
                fixed_count += 1
                print(f"Fixed: {source} - {anchor} -> {correct_anchor}")
            else:
                failed_count += 1

print(f"\nTotal: Fixed {fixed_count}, Failed {failed_count}")
