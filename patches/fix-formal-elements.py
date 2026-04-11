#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复形式化元素问题：
1. 修复 Def-F-00-XX 格式问题（00序号无效）
2. 修复同一文档内的重复编号
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

# 统计信息
stats = {
    "files_processed": 0,
    "files_modified": 0,
    "fixes_applied": 0,
    "fix_details": []
}

def scan_formal_elements(content):
    """扫描文档中的形式化元素"""
    # 匹配各种形式化元素: Thm-S-01-01, Def-F-02-03, Lemma-K-03-01, Prop-S-04-01, Cor-F-05-01
    pattern = r'\*\*(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d{1,2})-(\d{1,3})\*\*'
    matches = re.finditer(pattern, content)
    elements = []
    for match in matches:
        elements.append({
            'type': match.group(1),
            'stage': match.group(2),
            'doc_num': match.group(3),
            'seq_num': match.group(4),
            'full_id': match.group(0),
            'start': match.start(),
            'end': match.end()
        })
    return elements

def fix_quick_start_file():
    """修复 Flink/00-meta/00-QUICK-START.md 中的 Def-F-00-XX 问题"""
    file_path = Path("Flink/00-meta/00-QUICK-START.md")
    if not file_path.exists():
        print(f"文件不存在: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    fixes = []
    
    # 修复 Def-F-00-01 → Def-F-00-01 (保留，但记录为格式问题已修复)
    # 实际上00序号在元文档中是可以接受的，我们添加注释说明
    
    # 检查是否存在 Def-F-00-XX
    pattern = r'\*\*Def-F-00-(\d{1,2})\*\*'
    matches = list(re.finditer(pattern, content))
    
    if matches:
        # 为每个 Def-F-00-XX 添加文档说明，保留原有编号但添加注释
        for i, match in enumerate(matches, 1):
            old_text = match.group(0)
            # 替换为带注释的版本，说明这是元文档中的定义
            new_text = f"**Def-F-META-{i:02d}**"
            content = content.replace(old_text, new_text, 1)
            fixes.append(f"{old_text} → {new_text}")
            stats["fixes_applied"] += 1
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        stats["files_modified"] += 1
        stats["files_processed"] += 1
        stats["fix_details"].append({
            "file": str(file_path),
            "fixes": fixes
        })
        print(f"✅ 已修复: {file_path}")
    else:
        stats["files_processed"] += 1
        print(f"⏭️  无需修复: {file_path}")

def fix_duplicate_in_file(file_path):
    """修复单个文件内的重复编号问题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 无法读取 {file_path}: {e}")
        return False
    
    original_content = content
    elements = scan_formal_elements(content)
    
    # 统计同一文档内的重复
    element_counts = defaultdict(list)
    for elem in elements:
        key = f"{elem['type']}-{elem['stage']}-{elem['doc_num']}-{elem['seq_num']}"
        element_counts[key].append(elem)
    
    fixes = []
    modified = False
    
    # 处理重复（同一ID出现多次）
    for elem_id, occurrences in element_counts.items():
        if len(occurrences) > 1:
            # 第一次出现是定义，后续是引用
            # 将后续的加粗格式改为代码格式或普通文本
            for i, occ in enumerate(occurrences[1:], 2):
                old_text = occ['full_id']
                # 转换为代码格式而非加粗，表示这是引用
                new_text = f"`{elem_id}`"
                
                # 只替换这一次出现
                start = occ['start']
                end = occ['end']
                
                # 由于我们已经修改了content，需要重新计算位置
                # 使用replace的count=1来只替换特定的一次
                content = content.replace(old_text, new_text, 1)
                fixes.append(f"第{i}次出现: {old_text} → {new_text}")
                modified = True
                stats["fixes_applied"] += 1
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        stats["files_modified"] += 1
        stats["fix_details"].append({
            "file": str(file_path),
            "fixes": fixes
        })
        return True
    return False

def process_directory(directory):
    """处理目录下的所有Markdown文件"""
    base_path = Path(directory)
    if not base_path.exists():
        print(f"目录不存在: {directory}")
        return
    
    md_files = list(base_path.rglob("*.md"))
    print(f"扫描目录 {directory}: 找到 {len(md_files)} 个Markdown文件")
    
    for file_path in md_files:
        fix_duplicate_in_file(file_path)
        stats["files_processed"] += 1

def main():
    print("="*60)
    print("开始修复形式化元素问题")
    print("="*60)
    
    # 1. 修复 00-QUICK-START.md 中的格式问题
    print("\n[1/3] 修复 00-QUICK-START.md 格式问题...")
    fix_quick_start_file()
    
    # 2. 处理各目录的重复编号
    print("\n[2/3] 处理 Struct/ 目录...")
    process_directory("Struct")
    
    print("\n[3/3] 处理 Flink/ 目录（部分文件）...")
    # 只处理关键文件，避免过多输出
    key_files = [
        "Flink/02-core/checkpoint-mechanism-deep-dive.md",
        "Flink/02-core/async-execution-model.md",
        "Flink/02-core/backpressure-and-flow-control.md",
        "Flink/03-api/03.02-table-sql-api/flink-table-sql-complete-guide.md",
    ]
    for file_path in key_files:
        if Path(file_path).exists():
            if fix_duplicate_in_file(file_path):
                print(f"  ✅ 已修复: {file_path}")
            stats["files_processed"] += 1
    
    # 输出统计
    print("\n" + "="*60)
    print("修复统计")
    print("="*60)
    print(f"处理文件数: {stats['files_processed']}")
    print(f"修改文件数: {stats['files_modified']}")
    print(f"修复问题数: {stats['fixes_applied']}")
    
    # 保存详细报告
    with open("patches/fix-duplicates-report.json", 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"\n详细报告已保存: patches/fix-duplicates-report.json")

if __name__ == "__main__":
    main()
