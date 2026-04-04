#!/usr/bin/env python3
"""
修复wasi-0.3-async-preview.md中的锚点链接
"""

import re
from pathlib import Path

def slugify(text):
    """GitHub风格锚点生成"""
    text = text.strip().lower()
    text = re.sub(r'[*_`#\[\]]+', '', text)
    text = re.sub(r'<[^>]+>', '', text)  # 移除尖括号内容
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^\w\u4e00-\u9fff\-]', '-', text)  # 特殊字符转为连字符
    text = re.sub(r'-+', '-', text)
    text = text.strip('-')
    return text

def extract_headings(content):
    """提取所有标题及其锚点"""
    headings = {}
    pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    for match in pattern.finditer(content):
        level = len(match.group(1))
        title = match.group(2).strip()
        anchor = slugify(title)
        if anchor:
            headings[title] = anchor
    return headings

def main():
    file_path = Path("E:\\_src\\AnalysisDataFlow\\Flink\\13-wasm\\wasi-0.3-async-preview.md")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 提取所有标题
    headings = extract_headings(content)
    
    # 查找所有锚点链接
    link_pattern = re.compile(r'\[([^\]]+)\]\(#([^)]+)\)')
    
    fixes = []
    for match in link_pattern.finditer(original_content):
        link_text = match.group(1)
        current_anchor = match.group(2)
        
        # 查找匹配的标题
        for title, correct_anchor in headings.items():
            if link_text.strip().lower() == title.strip().lower():
                if current_anchor != correct_anchor:
                    old_link = f"[{link_text}](#{current_anchor})"
                    new_link = f"[{link_text}](#{correct_anchor})"
                    if old_link in content:
                        content = content.replace(old_link, new_link)
                        fixes.append({
                            'text': link_text[:50],
                            'old': current_anchor,
                            'new': correct_anchor
                        })
                break
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"修复了 {len(fixes)} 个链接:")
        for fix in fixes[:20]:
            print(f"  {fix['text']}: #{fix['old']} -> #{fix['new']}")
        if len(fixes) > 20:
            print(f"  ... 还有 {len(fixes) - 20} 个")
    else:
        print("无需修复")
    
    return len(fixes)

if __name__ == "__main__":
    count = main()
    print(f"\n总计修复: {count} 个链接")
