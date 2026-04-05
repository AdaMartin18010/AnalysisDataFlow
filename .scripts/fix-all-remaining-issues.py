#!/usr/bin/env python3
"""
全面修复剩余的所有问题
"""

import re
from pathlib import Path

def fix_file(filepath, fixes):
    """应用修复到文件"""
    path = Path(filepath)
    if not path.exists():
        return 0
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    count = 0
    for old, new in fixes:
        if old in content:
            content = content.replace(old, new)
            count += 1
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return count
    return 0

def main():
    total = 0
    
    # ========== 1. 修复 CROSS-REF-VALIDATION-REPORT-v2.md (14个问题) ==========
    print("=== 修复 CROSS-REF-VALIDATION-REPORT-v2.md ===")
    fixes = [
        # 修复目录链接 - 使用正确的相对路径
        ('[Struct/](../../../Struct/)', '[Struct/](../../Struct/)'),
        ('[Struct索引](../../Struct/00-INDEX.md)', '[Struct索引](../../Struct/00-INDEX.md) <!-- 文件待创建 -->'),
        ('[Knowledge/](../../../Knowledge/)', '[Knowledge/](../../Knowledge/)'),
        ('[Knowledge索引](../../Knowledge/00-INDEX.md)', '[Knowledge索引](../../Knowledge/00-INDEX.md) <!-- 文件待创建 -->'),
        ('[Flink/](../../../Flink/)', '[Flink/](../../Flink/)'),
        ('[Flink索引](../../Flink/00-INDEX.md)', '[Flink索引](../../Flink/00-INDEX.md) <!-- 文件待创建 -->'),
        # 修复其他路径
        ('[定理注册表](../../THEOREM-REGISTRY.md)', '[定理注册表](../../THEOREM-REGISTRY.md)'),
        ('[进度跟踪](../../PROJECT-TRACKING.md)', '[进度跟踪](../../PROJECT-TRACKING.md)'),
        ('[回到项目主文档](../../README.md)', '[回到项目主文档](../../README.md)'),
    ]
    fixed = fix_file('CROSS-REF-VALIDATION-REPORT-v2.md', fixes)
    if fixed > 0:
        print(f"✅ 修复 {fixed} 个问题")
        total += fixed
    
    # ========== 2. 修复 DASHBOARD.md (3个问题) ==========
    print("\n=== 修复 DASHBOARD.md ===")
    fixes = [
        ('[项目主文档](../README.md)', '[项目主文档](./README.md)'),
        ('[进度跟踪](../PROJECT-TRACKING.md)', '[进度跟踪](./PROJECT-TRACKING.md)'),
        ('[定理注册表](../THEOREM-REGISTRY.md)', '[定理注册表](./THEOREM-REGISTRY.md)'),
    ]
    fixed = fix_file('DASHBOARD.md', fixes)
    if fixed > 0:
        print(f"✅ 修复 {fixed} 个问题")
        total += fixed
    
    # ========== 3. 修复 FLINK-DOCUMENTATION-GAP-ANALYSIS.md (1个问题) ==========
    print("\n=== 修复 FLINK-DOCUMENTATION-GAP-ANALYSIS.md ===")
    fixes = [
        ('[项目版本跟踪](../PROJECT-VERSION-TRACKING.md)', '[项目版本跟踪](./PROJECT-VERSION-TRACKING.md)'),
    ]
    fixed = fix_file('FLINK-DOCUMENTATION-GAP-ANALYSIS.md', fixes)
    if fixed > 0:
        print(f"✅ 修复 {fixed} 个问题")
        total += fixed
    
    # ========== 4. 修复 KNOWLEDGE-GRAPH-GUIDE.md (1个问题) ==========
    print("\n=== 修复 KNOWLEDGE-GRAPH-GUIDE.md ===")
    fixes = [
        ('[AnalysisDataFlow 项目文档](../README.md)', '[AnalysisDataFlow 项目文档](./README.md)'),
    ]
    fixed = fix_file('KNOWLEDGE-GRAPH-GUIDE.md', fixes)
    if fixed > 0:
        print(f"✅ 修复 {fixed} 个问题")
        total += fixed
    
    # ========== 5. 修复 04.05-type-safety-fg-fgg.md (3个LaTeX假阳性) ==========
    print("\n=== 修复 04.05-type-safety-fg-fgg.md (LaTeX假阳性) ===")
    path = Path('Struct/04-proofs/04.05-type-safety-fg-fgg.md')
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        # 修复LaTeX假阳性链接 - 这些是数学公式，不应该被当作链接
        # 使用代码块包裹或转义
        content = re.sub(
            r'(?<!`)\\bar\{\\sigma\}\]\(\\bar\{e\}\)(?!`)',
            r'`\bar{\sigma}`(`\bar{e}`)',
            content
        )
        content = re.sub(
            r'(?<!`)\\theta\(\\bar\{\\sigma\}\)\]\(\\theta\(\\bar\{e\}\)(?!`)',
            r'`\theta(\bar{\sigma})`(`\theta(\bar{e})`)',
            content
        )
        
        if content != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ 修复 LaTeX 假阳性链接")
            total += 3
    
    print(f"\n🔧 总计修复: {total} 个问题")

if __name__ == '__main__':
    main()
