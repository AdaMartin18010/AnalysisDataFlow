#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复缺失依赖问题：
添加缺失的形式化元素定义引用
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
    "definitions_added": 0,
    "fix_details": []
}

# 已知缺失的定义和应添加的位置
MISSING_DEFINITIONS = {
    # 文件路径: [(元素ID, 建议添加位置, 上下文), ...]
    "Flink/02-core/time-semantics-and-watermark.md": [
        ("Def-F-02-04", "在 Watermark 定义之后", "Watermark时间语义"),
        ("Def-F-02-05", "在 Watermark 定义之后", "Watermark时间语义"),
        ("Def-F-02-06", "在 State Backend 定义之后", "状态后端定义"),
    ],
}

def scan_missing_definitions(file_path, content):
    """扫描文档中引用但未定义的形式化元素"""
    # 找出所有引用的形式化元素
    ref_pattern = r'`(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d{1,2})-(\d{1,3})`'
    refs = set(re.findall(ref_pattern, content))
    
    # 找出所有定义的加粗形式化元素
    def_pattern = r'\*\*(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d{1,2})-(\d{1,3})\*\*'
    defs = set(re.findall(def_pattern, content))
    
    # 找出引用但未在同一文档中定义的
    missing = []
    for ref in refs:
        if ref not in defs:
            missing.append(f"{ref[0]}-{ref[1]}-{ref[2]}-{ref[3]}")
    
    return missing

def add_missing_definitions(file_path, missing_defs):
    """在文档中添加缺失的定义引用"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, str(e)
    
    original_content = content
    fixes = []
    
    # 在文档开头添加引用说明（如果存在缺失的定义）
    if missing_defs:
        # 查找文档头部（第一个标题之后）
        lines = content.split('\n')
        header_end = 0
        for i, line in enumerate(lines):
            if line.startswith('# ') and i > 0:
                header_end = i + 1
                break
        
        # 在头部添加依赖说明
        dep_section = "\n> **形式化元素依赖**: " + ", ".join([f"`{d}`" for d in missing_defs[:5]])
        if len(missing_defs) > 5:
            dep_section += f" 等{len(missing_defs)}个定义"
        dep_section += "\n"
        
        # 插入到第一个标题之后
        lines.insert(header_end, dep_section)
        content = '\n'.join(lines)
        
        for d in missing_defs:
            fixes.append(f"添加依赖引用: {d}")
            stats["definitions_added"] += 1
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, fixes
    return False, []

def process_key_files():
    """处理关键文件"""
    key_files = [
        "Flink/02-core/checkpoint-mechanism-deep-dive.md",
        "Flink/02-core/async-execution-model.md",
        "Flink/02-core/time-semantics-and-watermark.md",
        "Flink/01-concepts/datastream-v2-semantics.md",
        "Struct/01-foundation/01.02-process-calculus-primer.md",
        "Struct/01-foundation/01.03-actor-model-formalization.md",
    ]
    
    for file_path in key_files:
        path = Path(file_path)
        if not path.exists():
            print(f"  ⏭️  文件不存在: {file_path}")
            continue
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"  ❌ 无法读取 {file_path}: {e}")
            continue
        
        stats["files_processed"] += 1
        
        # 扫描缺失的定义
        missing = scan_missing_definitions(file_path, content)
        if missing:
            modified, result = add_missing_definitions(file_path, missing)
            if modified:
                stats["files_modified"] += 1
                stats["fix_details"].append({
                    "file": file_path,
                    "fixes": result
                })
                print(f"  ✅ 已添加 {len(missing)} 个依赖引用: {file_path}")
            else:
                print(f"  ⏭️  无需修改: {file_path}")
        else:
            print(f"  ⏭️  无缺失依赖: {file_path}")

def main():
    print("="*60)
    print("开始修复缺失依赖")
    print("="*60)
    
    print("\n[1/1] 处理关键文件...")
    process_key_files()
    
    # 输出统计
    print("\n" + "="*60)
    print("修复统计")
    print("="*60)
    print(f"处理文件数: {stats['files_processed']}")
    print(f"修改文件数: {stats['files_modified']}")
    print(f"添加依赖数: {stats['definitions_added']}")
    
    # 保存详细报告
    with open("patches/fix-dependencies-report.json", 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"\n详细报告已保存: patches/fix-dependencies-report.json")

if __name__ == "__main__":
    main()
