#!/usr/bin/env python3
"""
最终批次 - 修复剩余的锚点格式问题
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

def fix_regex(filepath, patterns):
    """使用正则表达式修复"""
    path = Path(filepath)
    if not path.exists():
        return 0
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    total = 0
    for pattern, replacement in patterns:
        content_new = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        if content_new != content:
            content = content_new
            total += 1
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    return total

def main():
    total = 0
    
    # 1. 修复 01.04-dataflow-model-formalization.md - 删除重复锚点
    print("=== 修复 01.04-dataflow-model-formalization.md ===")
    fixed = fix_regex("Struct/01-foundation/01.04-dataflow-model-formalization.md", [
        # 删除重复的锚点 (关系 1)
        (r'({#关系-1-dataflow-model--kahn-进程网络-kpn}) {#关系-1-dataflow-model--kahn-进程网络-kpn-[^}]+}',
         r'\1'),
        # 删除重复的锚点 (关系 2)
        (r'({#关系-2-同步数据流-sdf--动态数据流-ddf--dataflow-model}) {#关系-2-同步数据流-sdf--动态数据流-ddf--dataflow-model-[^}]+}',
         r'\1'),
        # 删除重复的锚点 (关系 3)
        (r'({#关系-3-dataflow-理论模型--flink-runtime-实现}) {#关系-3-dataflow-理论模型--flink-runtime-实现-[^}]+}',
         r'\1'),
    ])
    if fixed > 0:
        print(f"✅ 删除 {fixed} 个重复锚点")
        total += fixed
    
    # 2. 修复 01.05-csp-formalization.md - 转换 {{#...}} 为 {#...}
    print("\n=== 修复 01.05-csp-formalization.md ===")
    fixed = fix_regex("Struct/01-foundation/01.05-csp-formalization.md", [
        # 转换 {{#...}} 为 {#...}
        (r'\{\{#([^}]+)\}\}', r'{#\1}'),
    ])
    if fixed > 0:
        print(f"✅ 转换 {fixed} 个锚点格式")
        total += fixed
    
    # 3. 修复 01.06-petri-net-formalization.md - 转换 {{#...}} 并添加缺失锚点
    print("\n=== 修复 01.06-petri-net-formalization.md ===")
    fixed = fix_regex("Struct/01-foundation/01.06-petri-net-formalization.md", [
        (r'\{\{#([^}]+)\}\}', r'{#\1}'),
    ])
    if fixed > 0:
        print(f"✅ 转换 {fixed} 个锚点格式")
        total += fixed
    
    # 4. 修复 wasm-dataflow-patterns.md - 添加完整的锚点
    print("\n=== 修复 wasm-dataflow-patterns.md ===")
    fixed = fix_file("Knowledge/06-frontier/wasm-dataflow-patterns.md", [
        ('{#webassembly-数据流模式浏览器-边缘-云统一执行模型}',
         '{#webassembly-数据流模式浏览器-边缘-云统一执行模型-wasm-dataflow-patterns}'),
    ])
    if fixed > 0:
        print(f"✅ 修复标题锚点")
        total += fixed
    
    # 5. 修复 01.07-session-types.md - 添加锚点
    print("\n=== 修复 01.07-session-types.md ===")
    fixed = fix_regex("Struct/01-foundation/01.07-session-types.md", [
        (r'^(#{1,6}\s+5\. 形式证明 / 工程论证 \(Proof\))$', 
         r'\1 {#5-形式证明--工程论证-proof}'),
    ])
    if fixed > 0:
        print(f"✅ 添加锚点")
        total += 1
    
    # 6. 修复 02.01-determinism-in-streaming.md - 添加锚点
    print("\n=== 修复 02.01-determinism-in-streaming.md ===")
    fixed = fix_regex("Struct/02-properties/02.01-determinism-in-streaming.md", [
        (r'^(#{1,6}\s+5\. 形式证明 / 工程论证 \(Proof / Engineering Argument\))$', 
         r'\1 {#5-形式证明--工程论证-proof--engineering-argument}'),
    ])
    if fixed > 0:
        print(f"✅ 添加锚点")
        total += 1
    
    # 7. 修复 02.02-consistency-hierarchy.md - 添加锚点
    print("\n=== 修复 02.02-consistency-hierarchy.md ===")
    fixed = fix_regex("Struct/02-properties/02.02-consistency-hierarchy.md", [
        (r'^(#{1,6}\s+关系 1: Dataflow 确定性定理与一致性层级的联系)$', 
         r'\1 {#关系-1-dataflow-确定性定理与一致性层级的联系}'),
    ])
    if fixed > 0:
        print(f"✅ 添加锚点")
        total += 1
    
    # 8. 修复 03.02-flink-to-process-calculus.md - 添加锚点
    print("\n=== 修复 03.02-flink-to-process-calculus.md ===")
    fixed = fix_regex("Struct/03-relationships/03.02-flink-to-process-calculus.md", [
        (r'^(#{1,6}\s+Flink 到进程演算编码 \(Flink-to-Process Calculus Encoding\))$', 
         r'\1 {#flink-到进程演算编码-flink-to-process-calculus-encoding}'),
    ])
    if fixed > 0:
        print(f"✅ 添加锚点")
        total += 1
    
    # 9. 修复 03.04-bisimulation-equivalences.md - 添加锚点
    print("\n=== 修复 03.04-bisimulation-equivalences.md ===")
    fixed = fix_regex("Struct/03-relationships/03.04-bisimulation-equivalences.md", [
        (r'^(#{1,6}\s+Def-S-15-02\. 弱互模拟与分支互模拟 \(Weak \\& Branching Bisimulation\))$', 
         r'\1 {#def-s-15-02-弱互模拟与分支互模拟}'),
    ])
    if fixed > 0:
        print(f"✅ 添加锚点")
        total += 1
    
    # 10. 修复 04.05-type-safety-fg-fgg.md - 添加锚点
    print("\n=== 修复 04.05-type-safety-fg-fgg.md ===")
    fixed = fix_regex("Struct/04-proofs/04.05-type-safety-fg-fgg.md", [
        (r'^(#{1,6}\s+6\. 实例与反例 \(Examples \\& Counter-examples\))$', 
         r'\1 {#6-实例验证-examples--counter-examples}'),
    ])
    if fixed > 0:
        print(f"✅ 添加锚点")
        total += 1
    
    # 11. 修复 04.07-deadlock-freedom-choreographic.md - 添加锚点
    print("\n=== 修复 04.07-deadlock-freedom-choreographic.md ===")
    fixed = fix_regex("Struct/04-proofs/04.07-deadlock-freedom-choreographic.md", [
        (r'^(#{1,6}\s+Def-S-23-02\. Global Types \(全局类型\))$', 
         r'\1 {#def-s-23-02-global-types}'),
        (r'^(#{1,6}\s+Lemma-S-23-01\. EPP 保持通信结构)$', 
         r'\1 {#lemma-s-23-01-epp-保持通信结构-lemma-s-23-01-epp-preservation}'),
        (r'^(#{1,6}\s+Prop-S-23-01\. Choreography 的合流性)$', 
         r'\1 {#prop-s-23-01-choreography-的合流性-prop-s-23-01-choreography-confluence}'),
    ])
    if fixed > 0:
        print(f"✅ 添加 {fixed} 个锚点")
        total += fixed
    
    # 12. 修复 06.01-open-problems-streaming-verification.md - 添加锚点
    print("\n=== 修复 06.01-open-problems-streaming-verification.md ===")
    fixed = fix_regex("Struct/06-frontier/06.01-open-problems-streaming-verification.md", [
        (r'^(#{1,6}\s+5\. 形式证明 / 工程论证 \(Proof / Engineering Argument\))$', 
         r'\1 {#5-形式证明--工程论证-proof--engineering-argument}'),
    ])
    if fixed > 0:
        print(f"✅ 添加锚点")
        total += 1
    
    print(f"\n🔧 总计修复: {total} 个问题")

if __name__ == '__main__':
    main()
