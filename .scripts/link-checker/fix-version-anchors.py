#!/usr/bin/env python3
"""
修复版本号锚点问题
将 flink-2-0 转换为 flink-20
将 flink-1-17 转换为 flink-117
"""

import re
from pathlib import Path

def fix_version_in_anchor(anchor):
    """修复锚点中的版本号格式"""
    # 修复 flink-x-y 格式为 flink-xy
    anchor = re.sub(r'flink-(\d+)-(\d+)', r'flink-\1\2', anchor)
    return anchor

def main():
    root_dir = Path("E:\\_src\\AnalysisDataFlow")
    quick_index_file = root_dir / "GLOSSARY-QUICK-INDEX.md"
    
    # 读取文件
    with open(quick_index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    fixes = []
    
    # 查找所有指向GLOSSARY.md的链接
    pattern = re.compile(r'\[([^\]]+)\]\(GLOSSARY\.md#([^)]+)\)')
    
    for match in pattern.finditer(original_content):
        link_text = match.group(1)
        current_anchor = match.group(2)
        
        # 修复版本号
        fixed_anchor = fix_version_in_anchor(current_anchor)
        
        if fixed_anchor != current_anchor:
            old_link = f"](GLOSSARY.md#{current_anchor})"
            new_link = f"](GLOSSARY.md#{fixed_anchor})"
            
            if old_link in content:
                content = content.replace(old_link, new_link)
                fixes.append({
                    'old': current_anchor,
                    'new': fixed_anchor,
                    'text': link_text
                })
    
    # 保存修复后的文件
    if content != original_content:
        with open(quick_index_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"修复了 {len(fixes)} 个链接:")
        for fix in fixes:
            print(f"  #{fix['old']} -> #{fix['new']}")
    else:
        print("无需修复")
    
    return len(fixes)

if __name__ == "__main__":
    count = main()
    print(f"\n总计修复: {count} 个链接")
