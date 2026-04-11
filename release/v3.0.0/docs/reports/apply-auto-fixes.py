#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动生成的依赖修复脚本
生成时间: 2026-04-11T20:30:38

此脚本应用高置信度的自动修复:
- Def-S-13-05 -> Def-S-13-04 (文档13只有4个定义)
- Def-S-14-04 -> Def-S-13-04 (文档14没有Def-14-04)
- Def-K-05-12 -> Def-K-05-11 (文档05只有11个定义)
"""

import re
from pathlib import Path

# 修复映射表: (文件路径, 原依赖ID, 新依赖ID)
FIXES = [
    # Proof-Chains-Relationships-Complete.md 中的修复
    ("Struct/Proof-Chains-Relationships-Complete.md", "Def-S-13-05", "Def-S-13-04"),
    ("Struct/Proof-Chains-Relationships-Complete.md", "Def-S-14-04", "Def-S-13-04"),
    # COMPLETION-REPORT.md 中的修复
    ("Knowledge/Flink-Scala-Rust-Comprehensive/05-architecture-patterns/COMPLETION-REPORT.md", "Def-K-05-12", "Def-K-05-11"),
]

def apply_fixes():
    fixed_count = 0
    error_count = 0
    
    for file_path, old_id, new_id in FIXES:
        # 尝试相对路径和绝对路径
        paths_to_try = [
            Path(file_path),
            Path(".") / file_path,
            Path("e:/_src/AnalysisDataFlow") / file_path,
        ]
        
        path = None
        for p in paths_to_try:
            if p.exists():
                path = p
                break
        
        if not path:
            print(f'❌ 文件不存在: {file_path}')
            error_count += 1
            continue
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含要替换的内容
            if old_id not in content:
                print(f'⚠️  {path} 中未找到 {old_id}')
                continue
            
            # 替换依赖引用
            new_content = re.sub(rf'\b{re.escape(old_id)}\b', new_id, content)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # 计算替换次数
            replace_count = content.count(old_id)
            print(f'✅ 已修复: {path} - {old_id} -> {new_id} ({replace_count} 处)')
            fixed_count += replace_count
            
        except Exception as e:
            print(f'❌ 修复失败 {path}: {e}')
            error_count += 1
    
    print(f"\n{'='*60}")
    print(f"修复完成: {fixed_count} 处修复, {error_count} 个错误")
    print(f"{'='*60}")
    return fixed_count, error_count

if __name__ == '__main__':
    apply_fixes()
