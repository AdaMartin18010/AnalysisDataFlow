#!/usr/bin/env python3
"""
修复GLOSSARY-QUICK-INDEX.md中的字母导航链接
"""

import re
from pathlib import Path

def main():
    quick_index_file = Path("E:\\_src\\AnalysisDataFlow\GLOSSARY-QUICK-INDEX.md")
    
    # 读取文件
    with open(quick_index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 字母列表
    letters = ['h', 'j', 'v', 'z']
    
    fixes = []
    
    # 修复字母导航链接，将它们指向GLOSSARY.md
    for letter in letters:
        # 匹配 [X](#x) 格式的链接，改为 [X](GLOSSARY.md#x)
        old_pattern = f"[{letter.upper()}](#{letter})"
        new_pattern = f"[{letter.upper()}](GLOSSARY.md#{letter})"
        
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            fixes.append({
                'letter': letter.upper(),
                'old': f"#{letter}",
                'new': f"GLOSSARY.md#{letter}"
            })
    
    # 保存修复后的文件
    if content != original_content:
        with open(quick_index_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"修复了 {len(fixes)} 个字母导航链接:")
        for fix in fixes:
            print(f"  [{fix['letter']}] {fix['old']} -> {fix['new']}")
    else:
        print("无需修复")
    
    return len(fixes)

if __name__ == "__main__":
    count = main()
    print(f"\n总计修复: {count} 个链接")
