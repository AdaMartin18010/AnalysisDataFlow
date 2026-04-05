#!/usr/bin/env python3
"""
批量锚点修复脚本 - 第2批: Struct/02-properties 及其他
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

def add_anchor_to_header(filepath, header_pattern, anchor_text):
    """在标题后添加自定义锚点"""
    path = Path(filepath)
    if not path.exists():
        return 0
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    pattern = r'^(#{1,6}\s+' + re.escape(header_pattern) + r')$'
    replacement = r'\1 {' + anchor_text + '}'
    content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return 1
    return 0

def main():
    total_fixed = 0
    
    print("=== 修复 Struct/02-properties ===")
    
    # 02.01-determinism-in-streaming.md
    fixed = fix_file("Struct/02-properties/02.01-determinism-in-streaming.md", [
        ('[关系 3: 可观测确定性 `⊂` 语义确定性 {#关系-3-可观测确定性--语义确定性}](#关系-3-可观测确定性-语义确定性)',
         '[关系 3: 可观测确定性 `⊂` 语义确定性](#关系-3-可观测确定性--语义确定性)'),
        ('[5. 形式证明 / 工程论证 (Proof / Engineering Argument)](#5-形式证明--工程论证)',
         '[5. 形式证明 / 工程论证 (Proof / Engineering Argument)](#5-形式证明--工程论证-proof--engineering-argument)'),
    ])
    if fixed > 0:
        print(f"✅ 02.01-determinism-in-streaming.md: 修复 {fixed} 个问题")
        total_fixed += fixed
    
    fixed = add_anchor_to_header("Struct/02-properties/02.01-determinism-in-streaming.md",
                                  "5. 形式证明 / 工程论证 (Proof / Engineering Argument)",
                                  "{#5-形式证明--工程论证-proof--engineering-argument}")
    if fixed > 0:
        print(f"✅ 02.01-determinism-in-streaming.md: 添加锚点")
        total_fixed += fixed
    
    # 02.02-consistency-hierarchy.md
    fixed = fix_file("Struct/02-properties/02.02-consistency-hierarchy.md", [
        ('[关系 1: Dataflow 确定性定理与一致性层级的联系](#关系-1-dataflow-确定性定理)',
         '[关系 1: Dataflow 确定性定理与一致性层级的联系](#关系-1-dataflow-确定性定理与一致性层级的联系)'),
    ])
    if fixed > 0:
        print(f"✅ 02.02-consistency-hierarchy.md: 修复 {fixed} 个问题")
        total_fixed += fixed
    
    # 02.04-liveness-and-safety.md
    fixed = add_anchor_to_header("Struct/02-properties/02.04-liveness-and-safety.md",
                                  "6. 实例与反例 (Examples \\& Counter-examples)",
                                  "{#6-实例与反例-examples--counter-examples}")
    if fixed > 0:
        print(f"✅ 02.04-liveness-and-safety.md: 添加锚点")
        total_fixed += fixed
    
    # 02.05-type-safety-derivation.md
    fixed = add_anchor_to_header("Struct/02-properties/02.05-type-safety-derivation.md",
                                  "6. 实例与反例 (Examples \\& Counter-examples)",
                                  "{#6-实例与反例-examples--counter-examples}")
    if fixed > 0:
        print(f"✅ 02.05-type-safety-derivation.md: 添加锚点")
        total_fixed += fixed
    
    print("\n=== 修复 Struct/03-relationships ===")
    
    # 03.01-actor-to-csp-encoding.md
    fixed = add_anchor_to_header("Struct/03-relationships/03.01-actor-to-csp-encoding.md",
                                  "6. 实例与反例 (Examples \\& Counter-examples)",
                                  "{#6-实例与反例-examples--counter-examples}")
    if fixed > 0:
        print(f"✅ 03.01-actor-to-csp-encoding.md: 添加锚点")
        total_fixed += fixed
    
    # 03.02-flink-to-process-calculus.md
    fixed = fix_file("Struct/03-relationships/03.02-flink-to-process-calculus.md", [
        ('[Flink 到进程演算编码 (Flink-to-Process Calculus Encoding)](#flink-到进程演算编码)',
         '[Flink 到进程演算编码 (Flink-to-Process Calculus Encoding)](#flink-到进程演算编码-flink-to-process-calculus-encoding)'),
    ])
    if fixed > 0:
        print(f"✅ 03.02-flink-to-process-calculus.md: 修复 {fixed} 个问题")
        total_fixed += fixed
    
    # 03.04-bisimulation-equivalences.md
    fixed = fix_file("Struct/03-relationships/03.04-bisimulation-equivalences.md", [
        ('[Def-S-15-02. 弱互模拟与分支互模拟 (Weak \\& Branching Bisimulation)](#def-s-15-02-弱互模拟与分支互模拟-weak--branching-bisimulation)',
         '[Def-S-15-02. 弱互模拟与分支互模拟 (Weak \\& Branching Bisimulation)](#def-s-15-02-弱互模拟与分支互模拟)'),
    ])
    if fixed > 0:
        print(f"✅ 03.04-bisimulation-equivalences.md: 修复 {fixed} 个问题")
        total_fixed += fixed
    
    # 03.05-cross-model-mappings.md
    fixed = add_anchor_to_header("Struct/03-relationships/03.05-cross-model-mappings.md",
                                  "5. 形式证明 / 工程论证 (Proof / Engineering Argument)",
                                  "{#5-形式证明--工程论证-proof--engineering-argument}")
    if fixed > 0:
        print(f"✅ 03.05-cross-model-mappings.md: 添加锚点")
        total_fixed += fixed
    
    print(f"\n🔧 本批次总计修复: {total_fixed} 个问题")

if __name__ == '__main__':
    main()
