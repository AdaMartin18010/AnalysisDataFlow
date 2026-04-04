#!/usr/bin/env python3
"""
调试锚点问题
"""

import re
from pathlib import Path
from urllib.parse import unquote

def slugify(text):
    """将标题转换为GitHub风格的锚点ID"""
    text = text.strip()
    text = text.lower()
    text = re.sub(r'[*_`#\[\]]+', '', text)
    text = re.sub(r'<[^>]+>', '', text)  # 移除HTML标签
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^\w\u4e00-\u9fff\-]', '-', text)
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
            headings[anchor.lower()] = {
                'level': level,
                'title': title,
                'anchor': anchor
            }
    return headings

def main():
    file_path = Path("E:\\_src\\AnalysisDataFlow\\Flink\\13-wasm\\wasi-0.3-async-preview.md")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    headings = extract_headings(content)
    
    print(f"文件: {file_path.name}")
    print(f"找到 {len(headings)} 个标题:\n")
    
    # 查找包含 stream 的标题
    for key, info in headings.items():
        if 'stream' in key or 'future' in key:
            print(f"  Anchor: #{info['anchor']}")
            print(f"  Title:  {info['title']}")
            print()
    
    # 检查特定锚点
    target = 'def-f-13-12-stream-类型'
    if target in headings:
        print(f"✓ 找到锚点: #{target}")
    else:
        print(f"✗ 未找到锚点: #{target}")
        print("\n相近的锚点:")
        for key in headings.keys():
            if 'def-f-13-12' in key:
                print(f"  #{key}")

if __name__ == "__main__":
    main()
