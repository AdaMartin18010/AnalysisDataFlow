#!/usr/bin/env python3
"""
修复GLOSSARY-QUICK-INDEX.md中的锚点链接
"""

import re
from pathlib import Path
from urllib.parse import unquote

def github_anchor(text):
    """GitHub风格的锚点生成"""
    anchor = text.strip().lower()
    # 移除HTML标签
    anchor = re.sub(r'<[^>]+>', '', anchor)
    # 移除Markdown标记
    anchor = re.sub(r'[*_`#\[\]]+', '', anchor)
    # 替换空格为连字符
    anchor = re.sub(r'\s+', '-', anchor)
    # 移除特殊字符，但保留连字符和中文字符
    anchor = re.sub(r'[^\w\u4e00-\u9fff\-]', '-', anchor)
    # 移除多余连字符
    anchor = re.sub(r'-+', '-', anchor)
    anchor = anchor.strip('-')
    return anchor

def extract_glossary_headings(content):
    """提取GLOSSARY.md中的所有三级标题（术语定义）"""
    headings = {}
    pattern = re.compile(r'^###\s+(.+)$', re.MULTILINE)
    for match in pattern.finditer(content):
        title = match.group(1).strip()
        anchor = github_anchor(title)
        headings[anchor.lower()] = title
        
        # 也提取英文部分作为可能的锚点
        # 例如 "Watermark (水印)" -> "watermark"
        english_match = re.match(r'^([A-Za-z\s\-]+)', title)
        if english_match:
            english_title = english_match.group(1).strip()
            english_anchor = github_anchor(english_title)
            if english_anchor and english_anchor != anchor:
                headings[english_anchor.lower()] = title
    
    return headings

def find_best_anchor(target_anchor, available_headings):
    """找到最匹配的锚点"""
    target_lower = target_anchor.lower()
    
    # 1. 精确匹配
    if target_lower in available_headings:
        return github_anchor(available_headings[target_lower])
    
    # 2. 尝试找到包含关系的
    for key, title in available_headings.items():
        if target_lower in key or key in target_lower:
            return github_anchor(title)
    
    # 3. 移除连字符后匹配
    target_clean = target_lower.replace('-', '')
    for key, title in available_headings.items():
        if target_clean == key.replace('-', ''):
            return github_anchor(title)
    
    return None

def main():
    root_dir = Path("E:\\_src\\AnalysisDataFlow")
    glossary_file = root_dir / "GLOSSARY.md"
    quick_index_file = root_dir / "GLOSSARY-QUICK-INDEX.md"
    
    # 读取GLOSSARY.md提取所有术语锚点
    with open(glossary_file, 'r', encoding='utf-8') as f:
        glossary_content = f.read()
    
    glossary_headings = extract_glossary_headings(glossary_content)
    print(f"发现 {len(glossary_headings)} 个术语定义")
    
    # 读取GLOSSARY-QUICK-INDEX.md
    with open(quick_index_file, 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    original_content = index_content
    fixes = []
    
    # 查找所有指向GLOSSARY.md的链接
    pattern = re.compile(r'\[([^\]]+)\]\(GLOSSARY\.md#([^)]+)\)')
    
    for match in pattern.finditer(index_content):
        link_text = match.group(1)
        current_anchor = match.group(2)
        full_match = match.group(0)
        
        # 查找正确的锚点
        correct_anchor = find_best_anchor(current_anchor, glossary_headings)
        
        if correct_anchor and correct_anchor != current_anchor:
            # 需要修复
            old_link = f"](GLOSSARY.md#{current_anchor})"
            new_link = f"](GLOSSARY.md#{correct_anchor})"
            
            if old_link in index_content:
                index_content = index_content.replace(old_link, new_link)
                fixes.append({
                    'old': current_anchor,
                    'new': correct_anchor,
                    'text': link_text
                })
        elif not correct_anchor:
            # 尝试字母锚点
            first_char = current_anchor[0].lower() if current_anchor else ''
            if first_char.isalpha():
                old_link = f"](GLOSSARY.md#{current_anchor})"
                new_link = f"](GLOSSARY.md#{first_char})"
                
                if old_link in index_content:
                    index_content = index_content.replace(old_link, new_link)
                    fixes.append({
                        'old': current_anchor,
                        'new': first_char,
                        'text': link_text,
                        'note': '字母分类'
                    })
    
    # 保存修复后的文件
    if index_content != original_content:
        with open(quick_index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        print(f"\n修复了 {len(fixes)} 个链接:")
        for fix in fixes[:20]:
            note = f" ({fix.get('note', '')})" if 'note' in fix else ''
            print(f"  #{fix['old']} -> #{fix['new']}{note}")
        if len(fixes) > 20:
            print(f"  ... 还有 {len(fixes) - 20} 个")
    else:
        print("\n无需修复")
    
    return len(fixes)

if __name__ == "__main__":
    count = main()
    print(f"\n总计修复: {count} 个链接")
