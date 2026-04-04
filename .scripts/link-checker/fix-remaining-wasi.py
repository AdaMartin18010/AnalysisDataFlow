#!/usr/bin/env python3
"""
修复wasi-0.3-async-preview.md中剩余的锚点链接
主要处理 #8-1 格式改为 #81 格式
"""

import re
from pathlib import Path

def main():
    file_path = Path("E:\\_src\\AnalysisDataFlow\\Flink\\13-wasm\\wasi-0.3-async-preview.md")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    fixes = []
    
    # 查找所有形如 #8-1-xxx 的链接，改为 #81-xxx
    pattern = re.compile(r'\[([^\]]+)\]\(#(\d)-(\d)([^)]*)\)')
    
    for match in pattern.finditer(original_content):
        link_text = match.group(1)
        first = match.group(2)
        second = match.group(3)
        rest = match.group(4)
        
        old_anchor = f"#{first}-{second}{rest}"
        new_anchor = f"#{first}{second}{rest}"
        
        old_link = f"[{link_text}]({old_anchor})"
        new_link = f"[{link_text}]({new_anchor})"
        
        if old_link in content:
            content = content.replace(old_link, new_link)
            fixes.append({
                'text': link_text[:40],
                'old': old_anchor,
                'new': new_anchor
            })
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"修复了 {len(fixes)} 个链接:")
        for fix in fixes[:20]:
            print(f"  {fix['text']}: {fix['old']} -> {fix['new']}")
        if len(fixes) > 20:
            print(f"  ... 还有 {len(fixes) - 20} 个")
    else:
        print("无需修复")
    
    return len(fixes)

if __name__ == "__main__":
    count = main()
    print(f"\n总计修复: {count} 个链接")
