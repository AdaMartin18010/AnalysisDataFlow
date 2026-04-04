#!/usr/bin/env python3
"""
修复GLOSSARY-QUICK-INDEX.md中的锚点链接 v2
使用更精确的匹配算法
"""

import re
from pathlib import Path
from urllib.parse import unquote

def github_anchor(text):
    """GitHub风格的锚点生成"""
    anchor = text.strip().lower()
    anchor = re.sub(r'<[^>]+>', '', anchor)
    anchor = re.sub(r'[*_`#\[\]]+', '', anchor)
    anchor = re.sub(r'\s+', '-', anchor)
    anchor = re.sub(r'[^\w\u4e00-\u9fff\-]', '-', anchor)
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
        
        # 存储原始标题和生成的锚点
        headings[anchor.lower()] = {
            'title': title,
            'anchor': anchor
        }
        
        # 提取英文部分作为别名
        # 例如 "Watermark (水印)" -> "watermark"
        english_match = re.match(r'^([A-Za-z0-9\s\-/\.]+)', title)
        if english_match:
            english_title = english_match.group(1).strip()
            english_anchor = github_anchor(english_title)
            if english_anchor and english_anchor != anchor:
                headings[english_anchor.lower()] = {
                    'title': title,
                    'anchor': anchor,
                    'alias': english_title
                }
    
    return headings

def find_best_anchor(target_anchor, available_headings):
    """找到最匹配的锚点"""
    target_lower = target_anchor.lower().strip('-')
    
    # 1. 精确匹配
    if target_lower in available_headings:
        return available_headings[target_lower]['anchor']
    
    # 2. 检查是否是中文术语的直接链接（如 #watermark）
    # 尝试在标题中查找
    for key, info in available_headings.items():
        title_lower = info['title'].lower()
        # 检查target是否在标题中
        if target_lower in title_lower:
            return info['anchor']
        # 检查标题是否在target中
        if title_lower.replace(' ', '-').replace('（', '-').replace('）', '') in target_lower:
            return info['anchor']
    
    # 3. 移除连字符后匹配
    target_clean = target_lower.replace('-', '')
    for key, info in available_headings.items():
        key_clean = key.replace('-', '')
        if target_clean == key_clean:
            return info['anchor']
        # 检查标题的clean版本
        title_clean = info['title'].lower().replace(' ', '').replace('-', '').replace('（', '').replace('）', '')
        if target_clean == title_clean:
            return info['anchor']
    
    return None

def main():
    root_dir = Path("E:\\_src\\AnalysisDataFlow")
    glossary_file = root_dir / "GLOSSARY.md"
    quick_index_file = root_dir / "GLOSSARY-QUICK-INDEX.md"
    
    # 读取GLOSSARY.md提取所有术语锚点
    with open(glossary_file, 'r', encoding='utf-8') as f:
        glossary_content = f.read()
    
    glossary_headings = extract_glossary_headings(glossary_content)
    print(f"发现 {len(glossary_headings)} 个术语定义映射")
    
    # 读取GLOSSARY-QUICK-INDEX.md
    with open(quick_index_file, 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    original_content = index_content
    fixes = []
    not_found = []
    
    # 查找所有指向GLOSSARY.md的链接
    pattern = re.compile(r'\[([^\]]+)\]\(GLOSSARY\.md#([^)]+)\)')
    
    for match in pattern.finditer(original_content):
        link_text = match.group(1)
        current_anchor = match.group(2)
        
        # 解码URL编码
        decoded_anchor = unquote(current_anchor)
        
        # 查找正确的锚点
        correct_anchor = find_best_anchor(decoded_anchor, glossary_headings)
        
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
            not_found.append({
                'anchor': decoded_anchor,
                'text': link_text
            })
    
    # 保存修复后的文件
    if index_content != original_content:
        with open(quick_index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        print(f"\n修复了 {len(fixes)} 个链接:")
        for fix in fixes:
            print(f"  #{fix['old']} -> #{fix['new']}")
    else:
        print("\n无需修复")
    
    if not_found:
        print(f"\n未找到匹配的锚点 ({len(not_found)} 个):")
        for nf in not_found[:10]:
            print(f"  #{nf['anchor']} ({nf['text']})")
        if len(not_found) > 10:
            print(f"  ... 还有 {len(not_found) - 10} 个")
    
    return len(fixes)

if __name__ == "__main__":
    count = main()
    print(f"\n总计修复: {count} 个链接")
