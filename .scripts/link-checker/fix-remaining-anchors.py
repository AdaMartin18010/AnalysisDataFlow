#!/usr/bin/env python3
"""
修复剩余的特殊锚点问题
"""

import re
from pathlib import Path

def slugify(text):
    """GitHub风格锚点生成"""
    text = text.strip().lower()
    text = re.sub(r'[*_`#\[\]]+', '', text)
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^\w\u4e00-\u9fff\-]', '-', text)
    text = re.sub(r'-+', '-', text)
    text = text.strip('-')
    return text

def fix_wasm_dataflow_patterns():
    """修复wasm-dataflow-patterns.md"""
    file_path = Path("E:\\_src\\AnalysisDataFlow\\Knowledge\\06-frontier\\wasm-dataflow-patterns.md")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 获取文件中的第一个标题（主标题）
    first_heading_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if not first_heading_match:
        return 0
    
    first_heading = first_heading_match.group(1).strip()
    correct_anchor = slugify(first_heading)
    
    # 查找目录中的链接
    toc_pattern = re.compile(r'^\s*-\s*\[([^\]]+)\]\(#([^)]+)\)', re.MULTILINE)
    
    fixes = 0
    for match in toc_pattern.finditer(content):
        link_text = match.group(1)
        current_anchor = match.group(2)
        
        # 如果这个链接指向主标题但锚点不正确
        if link_text == first_heading and current_anchor != correct_anchor:
            old_link = f"[{link_text}](#{current_anchor})"
            new_link = f"[{link_text}](#{correct_anchor})"
            content = content.replace(old_link, new_link)
            fixes += 1
    
    if fixes > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"修复了 {file_path.name} 中的 {fixes} 个链接")
    
    return fixes

def fix_wasi_async_preview():
    """修复wasi-0.3-async-preview.md"""
    file_path = Path("E:\\_src\\AnalysisDataFlow\\Flink\\13-wasm\\wasi-0.3-async-preview.md")
    
    if not file_path.exists():
        return 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 修复特定链接
    fixes = [
        ('#def-f-13-12-stream-类型', '#def-f-13-12-stream-类型'),
        ('#def-f-13-13-future-类型', '#def-f-13-13-future-类型'),
        ('#72-stream-生命周期状态机', '#72-stream-生命周期状态机'),
    ]
    
    # 这些链接可能已经是正确的，但需要检查
    # 实际上，这些链接可能是格式问题（如Def-F-13-12 vs def-f-13-12）
    
    count = 0
    for old, new in fixes:
        if old in content and old != new:
            content = content.replace(old, new)
            count += 1
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"修复了 {file_path.name} 中的 {count} 个链接")
    
    return count

def fix_cron_schedule():
    """修复cron-schedule.md"""
    file_path = Path("E:\\_src\\AnalysisDataFlow\\.scripts\\flink-version-tracking\\cron-schedule.md")
    
    if not file_path.exists():
        return 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找标题
    headings = []
    for match in re.finditer(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE):
        level = len(match.group(1))
        title = match.group(2).strip()
        anchor = slugify(title)
        headings.append((title, anchor))
    
    # 查找指向#linux-cron-配置的链接
    if '#linux-cron-配置' in content:
        # 找到实际的Linux Cron配置标题
        for title, anchor in headings:
            if 'linux' in title.lower() and 'cron' in title.lower():
                if anchor != 'linux-cron-配置':
                    content = content.replace('#linux-cron-配置', f'#{anchor}')
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"修复了 {file_path.name}: #linux-cron-配置 -> #{anchor}")
                    return 1
    
    return 0

def fix_glossary_quick_index():
    """修复GLOSSARY-QUICK-INDEX.md中的Z链接"""
    file_path = Path("E:\\_src\\AnalysisDataFlow\\GLOSSARY-QUICK-INDEX.md")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找 [Z](#z) 并修复
    if '[Z](#z)' in content:
        content = content.replace('[Z](#z)', '[Z](GLOSSARY.md#z)')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"修复了 {file_path.name}: [Z](#z) -> [Z](GLOSSARY.md#z)")
        return 1
    
    return 0

def main():
    total = 0
    
    total += fix_wasm_dataflow_patterns()
    total += fix_wasi_async_preview()
    total += fix_cron_schedule()
    total += fix_glossary_quick_index()
    
    print(f"\n总计修复: {total} 个链接")
    return total

if __name__ == "__main__":
    main()
