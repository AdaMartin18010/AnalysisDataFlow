#!/usr/bin/env python3
"""
批量锚点修复脚本 - 第3批: Struct/04-proofs, 05, 06 及其他
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
    
    print("=== 修复 Struct/04-proofs ===")
    
    # 04.01-flink-checkpoint-correctness.md
    fixed = add_anchor_to_header("Struct/04-proofs/04.01-flink-checkpoint-correctness.md",
                                  "Flink Checkpoint 正确性证明 (Flink Checkpoint Correctness Proof)",
                                  "{#flink-checkpoint-正确性证明-flink-checkpoint-correctness-proof}")
    if fixed > 0:
        print(f"✅ 04.01-flink-checkpoint-correctness.md: 添加锚点")
        total_fixed += fixed
    
    # 04.02-flink-exactly-once-correctness.md
    fixed = add_anchor_to_header("Struct/04-proofs/04.02-flink-exactly-once-correctness.md",
                                  "8. 实例与反例 (Examples \\& Counter-examples)",
                                  "{#8-实例与反例-examples--counter-examples}")
    if fixed > 0:
        print(f"✅ 04.02-flink-exactly-once-correctness.md: 添加锚点")
        total_fixed += fixed
    
    # 04.05-type-safety-fg-fgg.md - 需要修复LaTeX链接和锚点
    fixed = fix_file("Struct/04-proofs/04.05-type-safety-fg-fgg.md", [
        # 这些LaTeX链接可能是误报，但先修复锚点问题
        ('[6. 实例与反例 (Examples \\& Counter-examples)](#6-实例与反例-examples--counter-examples)',
         '[6. 实例与反例 (Examples \\& Counter-examples)](#6-实例验证-examples--counter-examples)'),
    ])
    if fixed > 0:
        print(f"✅ 04.05-type-safety-fg-fgg.md: 修复 {fixed} 个问题")
        total_fixed += fixed
    
    # 04.07-deadlock-freedom-choreographic.md
    fixed = fix_file("Struct/04-proofs/04.07-deadlock-freedom-choreographic.md", [
        ('[Def-S-23-02. Global Types (全局类型)](#def-s-23-02-global-types-全局类型)',
         '[Def-S-23-02. Global Types (全局类型)](#def-s-23-02-global-types)'),
        ('[Lemma-S-23-01. EPP 保持通信结构](#lemma-s-23-01-epp-保持通信结构)',
         '[Lemma-S-23-01. EPP 保持通信结构](#lemma-s-23-01-epp-保持通信结构-lemma-s-23-01-epp-preservation)'),
        ('[Prop-S-23-01. Choreography 的合流性](#prop-s-23-01-choreography-的合流性)',
         '[Prop-S-23-01. Choreography 的合流性](#prop-s-23-01-choreography-的合流性-prop-s-23-01-choreography-confluence)'),
    ])
    if fixed > 0:
        print(f"✅ 04.07-deadlock-freedom-choreographic.md: 修复 {fixed} 个问题")
        total_fixed += fixed
    
    print("\n=== 修复 Struct/05, 06 及其他 ===")
    
    # 05.01-go-vs-scala-expressiveness.md
    fixed = add_anchor_to_header("Struct/05-comparative-analysis/05.01-go-vs-scala-expressiveness.md",
                                  "6. 实例与反例 (Examples \\& Counter-examples)",
                                  "{#6-实例与反例-examples--counter-examples}")
    if fixed > 0:
        print(f"✅ 05.01-go-vs-scala-expressiveness.md: 添加锚点")
        total_fixed += fixed
    
    # 06.01-open-problems-streaming-verification.md
    fixed = add_anchor_to_header("Struct/06-frontier/06.01-open-problems-streaming-verification.md",
                                  "5. 形式证明 / 工程论证 (Proof / Engineering Argument)",
                                  "{#5-形式证明--工程论证-proof--engineering-argument}")
    if fixed > 0:
        print(f"✅ 06.01-open-problems-streaming-verification.md: 添加锚点")
        total_fixed += fixed
    
    # Knowledge/06-frontier/wasm-dataflow-patterns.md
    fixed = fix_file("Knowledge/06-frontier/wasm-dataflow-patterns.md", [
        ('[WebAssembly 数据流模式：浏览器-边缘-云统一执行模型](#webassembly-数据流模式浏览器-边缘-云统一执行模型)',
         '[WebAssembly 数据流模式：浏览器-边缘-云统一执行模型](#webassembly-数据流模式浏览器-边缘-云统一执行模型-wasm-dataflow-patterns)'),
    ])
    if fixed > 0:
        print(f"✅ wasm-dataflow-patterns.md: 修复 {fixed} 个问题")
        total_fixed += fixed
    
    # visuals/ 目录
    print("\n=== 修复 visuals/ 目录 ===")
    
    fixed = fix_file("visuals/knowledge-pattern-relations.md", [
        ('[3.1 领域 × 模式矩阵](#31-领域--模式矩阵)',
         '[3.1 领域 × 模式矩阵](#31-领域-模式矩阵)'),
    ])
    if fixed > 0:
        print(f"✅ knowledge-pattern-relations.md: 修复 {fixed} 个问题")
        total_fixed += fixed
    
    fixed = fix_file("visuals/matrix-patterns.md", [
        ('[2.1 核心业务需求 × 设计模式矩阵](#21-核心业务需求--设计模式矩阵)',
         '[2.1 核心业务需求 × 设计模式矩阵](#21-核心业务需求-设计模式矩阵)'),
    ])
    if fixed > 0:
        print(f"✅ matrix-patterns.md: 修复 {fixed} 个问题")
        total_fixed += fixed
    
    fixed = fix_file("visuals/matrix-scenarios.md", [
        ('[完整业务场景 × 技术要素矩阵](#完整业务场景--技术要素矩阵)',
         '[完整业务场景 × 技术要素矩阵](#完整业务场景-技术要素矩阵)'),
    ])
    if fixed > 0:
        print(f"✅ matrix-scenarios.md: 修复 {fixed} 个问题")
        total_fixed += fixed
    
    print(f"\n🔧 本批次总计修复: {total_fixed} 个问题")

if __name__ == '__main__':
    main()
