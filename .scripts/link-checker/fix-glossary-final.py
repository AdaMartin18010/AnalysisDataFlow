#!/usr/bin/env python3
"""
最终修复GLOSSARY-QUICK-INDEX.md中的锚点链接
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
        
        # 提取英文部分（如果存在）
        english_match = re.match(r'^([A-Za-z0-9\s\-/\.]+)', title)
        english_name = None
        if english_match:
            english_name = english_match.group(1).strip()
        
        headings[anchor.lower()] = {
            'title': title,
            'anchor': anchor,
            'english_name': english_name
        }
    
    return headings

def find_correct_anchor(term_name, glossary_headings):
    """根据术语名称找到正确的锚点"""
    term_lower = term_name.lower().strip()
    
    # 1. 直接匹配标题
    for key, info in glossary_headings.items():
        if info['title'].lower() == term_lower:
            return info['anchor']
    
    # 2. 匹配英文名称
    for key, info in glossary_headings.items():
        if info['english_name'] and info['english_name'].lower() == term_lower:
            return info['anchor']
    
    # 3. 部分匹配
    for key, info in glossary_headings.items():
        if term_lower in info['title'].lower():
            return info['anchor']
        if info['english_name'] and term_lower in info['english_name'].lower():
            return info['anchor']
    
    # 4. 清理后匹配
    term_clean = term_lower.replace('-', '').replace(' ', '')
    for key, info in glossary_headings.items():
        title_clean = info['title'].lower().replace('-', '').replace(' ', '').replace('（', '').replace('）', '')
        if term_clean == title_clean:
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
    print(f"发现 {len(glossary_headings)} 个术语定义")
    
    # 读取GLOSSARY-QUICK-INDEX.md
    with open(quick_index_file, 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    original_content = index_content
    fixes = []
    
    # 查找表格中的行，提取术语和链接
    # 格式: | 中文名 | 英文名 | 分类 | [详细定义](GLOSSARY.md#锚点) |
    table_pattern = re.compile(r'^\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*\[([^\]]+)\]\(GLOSSARY\.md#([^)]+)\)\s*\|$', re.MULTILINE)
    
    for match in table_pattern.finditer(original_content):
        chinese_name = match.group(1).strip()
        english_name = match.group(2).strip()
        category = match.group(3).strip()
        link_text = match.group(4).strip()
        current_anchor = match.group(5).strip()
        
        # 尝试用英文名查找
        correct_anchor = find_correct_anchor(english_name, glossary_headings)
        
        # 如果没找到，尝试用中文名
        if not correct_anchor:
            correct_anchor = find_correct_anchor(chinese_name, glossary_headings)
        
        if correct_anchor and correct_anchor != current_anchor:
            old_link = f"](GLOSSARY.md#{current_anchor})"
            new_link = f"](GLOSSARY.md#{correct_anchor})"
            
            if old_link in index_content:
                index_content = index_content.replace(old_link, new_link)
                fixes.append({
                    'term': english_name or chinese_name,
                    'old': current_anchor,
                    'new': correct_anchor
                })
    
    # 保存修复后的文件
    if index_content != original_content:
        with open(quick_index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        print(f"\n修复了 {len(fixes)} 个链接:")
        for fix in fixes[:30]:
            print(f"  {fix['term']}: #{fix['old']} -> #{fix['new']}")
        if len(fixes) > 30:
            print(f"  ... 还有 {len(fixes) - 30} 个")
    else:
        print("\n无需修复")
    
    return len(fixes)

if __name__ == "__main__":
    count = main()
    print(f"\n总计修复: {count} 个链接")
