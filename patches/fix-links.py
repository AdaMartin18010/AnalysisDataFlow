#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复无效链接问题：
1. 02-core-mechanisms → 02-core
2. 修复其他路径变更导致的链接断裂
"""

import os
import re
import json
from pathlib import Path

# 统计信息
stats = {
    "files_processed": 0,
    "files_modified": 0,
    "links_fixed": 0,
    "fix_details": []
}

# 路径映射表
PATH_MAPPINGS = {
    # 旧路径 → 新路径
    "Flink/02-core-mechanisms/": "Flink/02-core/",
    "Flink/06-engineering/": "Flink/09-practices/09.03-performance-tuning/",
    "Flink/07-case-studies/": "Flink/09-practices/09.01-case-studies/",
}

def fix_links_in_file(file_path):
    """修复单个文件中的链接"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, str(e)
    
    original_content = content
    fixes = []
    
    # 应用路径映射
    for old_path, new_path in PATH_MAPPINGS.items():
        # 处理不同格式的链接
        patterns = [
            (rf'\(\.\./{re.escape(old_path)}([^)]+)\)', f'(../{new_path}$1)'),
            (rf'\(\./{re.escape(old_path)}([^)]+)\)', f'(./{new_path}$1)'),
            (rf'\({re.escape(old_path)}([^)]+)\)', f'({new_path}$1)'),
            (rf'"{re.escape(old_path)}([^"]+)"', f'"{new_path}$1"'),
        ]
        
        for pattern, replacement in patterns:
            matches = re.findall(pattern, content)
            if matches:
                content = re.sub(pattern, replacement, content)
                for match in matches:
                    fixes.append(f"{old_path}{match} → {new_path}{match}")
                    stats["links_fixed"] += 1
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, fixes
    return False, []

def process_directory(directory):
    """处理目录下的所有Markdown文件"""
    base_path = Path(directory)
    if not base_path.exists():
        return
    
    md_files = list(base_path.rglob("*.md"))
    
    for file_path in md_files:
        modified, result = fix_links_in_file(file_path)
        stats["files_processed"] += 1
        if modified:
            stats["files_modified"] += 1
            stats["fix_details"].append({
                "file": str(file_path),
                "fixes": result
            })

def main():
    print("="*60)
    print("开始修复链接问题")
    print("="*60)
    
    # 处理根目录下的报告文件
    print("\n[1/4] 处理根目录报告文件...")
    root_files = [
        "DESIGN-PRINCIPLES.md",
        "cross-ref-error-analysis.md",
        "FLINK_REVISION_REPORT.md",
        "BENCHMARK-REPORT.md",
        "CHANGELOG.md",
        "CASE-STUDIES.md",
        "BROKEN-LINK-FIX-REPORT.md",
    ]
    for file_name in root_files:
        file_path = Path(file_name)
        if file_path.exists():
            modified, result = fix_links_in_file(file_path)
            stats["files_processed"] += 1
            if modified:
                stats["files_modified"] += 1
                print(f"  ✅ 已修复: {file_name}")
            else:
                print(f"  ⏭️  无需修复: {file_name}")
    
    # 处理 Struct 目录
    print("\n[2/4] 处理 Struct/ 目录...")
    process_directory("Struct")
    print(f"  处理文件数: {stats['files_processed']}")
    
    # 处理 Flink 目录
    print("\n[3/4] 处理 Flink/ 目录...")
    flink_stats = {"files_processed": 0, "files_modified": 0}
    base_path = Path("Flink")
    if base_path.exists():
        md_files = list(base_path.rglob("*.md"))
        for file_path in md_files:
            modified, result = fix_links_in_file(file_path)
            flink_stats["files_processed"] += 1
            if modified:
                flink_stats["files_modified"] += 1
    print(f"  处理文件数: {flink_stats['files_processed']}, 修改: {flink_stats['files_modified']}")
    
    # 处理 Knowledge 目录
    print("\n[4/4] 处理 Knowledge/ 目录...")
    knowledge_stats = {"files_processed": 0, "files_modified": 0}
    base_path = Path("Knowledge")
    if base_path.exists():
        md_files = list(base_path.rglob("*.md"))
        for file_path in md_files:
            modified, result = fix_links_in_file(file_path)
            knowledge_stats["files_processed"] += 1
            if modified:
                knowledge_stats["files_modified"] += 1
    print(f"  处理文件数: {knowledge_stats['files_processed']}, 修改: {knowledge_stats['files_modified']}")
    
    # 输出统计
    print("\n" + "="*60)
    print("修复统计")
    print("="*60)
    print(f"处理文件数: {stats['files_processed']}")
    print(f"修改文件数: {stats['files_modified']}")
    print(f"修复链接数: {stats['links_fixed']}")
    
    # 保存详细报告
    with open("patches/fix-links-report.json", 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"\n详细报告已保存: patches/fix-links-report.json")

if __name__ == "__main__":
    main()
