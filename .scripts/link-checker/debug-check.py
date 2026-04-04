#!/usr/bin/env python3
"""
模拟锚点检查逻辑
"""

import re
from pathlib import Path
from urllib.parse import unquote

def slugify(text):
    text = text.strip().lower()
    text = re.sub(r'[*_`#\[\]]+', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^\w\u4e00-\u9fff\-]', '-', text)
    text = re.sub(r'-+', '-', text)
    text = text.strip('-')
    return text

def extract_headings(content):
    headings = {}
    pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    for match in pattern.finditer(content):
        level = len(match.group(1))
        title = match.group(2).strip()
        anchor = slugify(title)
        if anchor:
            headings[anchor.lower()] = {
                'level': level,
                'title': title,
                'anchor': anchor
            }
    return headings

def extract_anchor_links(content):
    links = []
    pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    for match in pattern.finditer(content):
        link_text = match.group(1)
        link_target = match.group(2)
        if link_target.startswith(('http://', 'https://', 'mailto:', 'tel:')):
            continue
        if '#' in link_target:
            parts = link_target.split('#', 1)
            file_path_part = parts[0]
            anchor = parts[1]
            links.append({
                'text': link_text,
                'target': link_target,
                'file': file_path_part,
                'anchor': anchor
            })
    return links

def normalize_anchor(anchor):
    decoded = unquote(anchor)
    decoded = decoded.lower()
    decoded = decoded.replace(' ', '-')
    decoded = re.sub(r'-+', '-', decoded)
    decoded = decoded.strip('-')
    return decoded

def main():
    file_path = Path("E:\\_src\\AnalysisDataFlow\\Flink\\13-wasm\\wasi-0.3-async-preview.md")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    headings = extract_headings(content)
    links = extract_anchor_links(content)
    
    print(f"文件: {file_path.name}")
    print(f"找到 {len(headings)} 个标题, {len(links)} 个锚点链接\n")
    
    # 检查每个内部链接
    for link in links:
        if link['file']:  # 跳过外部文件链接
            continue
        
        anchor = link['anchor']
        normalized = normalize_anchor(anchor)
        
        # 检查是否存在
        found = normalized in headings
        
        if not found:
            # 尝试其他匹配方式
            for key in headings.keys():
                if key == normalized or key == anchor.lower():
                    found = True
                    break
        
        status = "✓" if found else "✗"
        if not found:
            print(f"{status} [#{anchor}]")
            print(f"   文本: {link['text']}")
            print(f"   规范化: #{normalized}")
            
            # 查找相似的锚点
            for key in headings.keys():
                if 'stream' in key and 'def-f-13-12' in key:
                    print(f"   可用: #{key}")
            print()

if __name__ == "__main__":
    main()
