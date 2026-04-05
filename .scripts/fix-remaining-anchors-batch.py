#!/usr/bin/env python3
"""
修复剩余的29个锚点问题
"""

import re
from pathlib import Path

def add_anchor(filepath, header_pattern, anchor_text):
    """在标题后添加锚点"""
    path = Path(filepath)
    if not path.exists():
        return 0
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    # 匹配标题行（后面没有锚点）
    pattern = r'^(#{1,6}\s+' + re.escape(header_pattern) + r')$'
    replacement = r'\1 {' + anchor_text + '}'
    content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return 1
    return 0

def fix_link(filepath, old_link, new_link):
    """修复链接"""
    path = Path(filepath)
    if not path.exists():
        return 0
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_link in content:
        content = content.replace(old_link, new_link)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return 1
    return 0

def main():
    total = 0
    
    # Struct/01-foundation
    print("=== Struct/01-foundation ===")
    anchors = [
        ("Struct/01-foundation/01.06-petri-net-formalization.md", 
         "Petri 网形式化 (Petri Net Formalization)", "{#petri-网形式化-petri-net-formalization}"),
        ("Struct/01-foundation/01.06-petri-net-formalization.md", 
         "图 1-1: Petri 网结构示例", "{#图-1-1-petri-网结构示例}"),
        ("Struct/01-foundation/01.06-petri-net-formalization.md", 
         "6. 实例验证 (Examples \\& Verification)", "{#6-实例验证-examples--verification}"),
        ("Struct/01-foundation/01.07-session-types.md", 
         "5. 形式证明 / 工程论证 (Proof)", "{#5-形式证明--工程论证-proof}"),
    ]
    for filepath, header, anchor in anchors:
        if add_anchor(filepath, header, anchor):
            print(f"✅ {filepath}: {anchor}")
            total += 1
    
    # Struct/02-properties
    print("\n=== Struct/02-properties ===")
    anchors = [
        ("Struct/02-properties/02.01-determinism-in-streaming.md", 
         "5. 形式证明 / 工程论证 (Proof / Engineering Argument)", "{#5-形式证明--工程论证-proof--engineering-argument}"),
        ("Struct/02-properties/02.02-consistency-hierarchy.md", 
         "关系 1: Dataflow 确定性定理与一致性层级的联系", "{#关系-1-dataflow-确定性定理与一致性层级的联系}"),
        ("Struct/02-properties/02.04-liveness-and-safety.md", 
         "6. 实例与反例 (Examples \\& Counter-examples)", "{#6-实例与反例-examples--counter-examples}"),
        ("Struct/02-properties/02.05-type-safety-derivation.md", 
         "6. 实例与反例 (Examples \\& Counter-examples)", "{#6-实例与反例-examples--counter-examples}"),
    ]
    for filepath, header, anchor in anchors:
        if add_anchor(filepath, header, anchor):
            print(f"✅ {filepath}: {anchor}")
            total += 1
    
    # Struct/03-relationships
    print("\n=== Struct/03-relationships ===")
    anchors = [
        ("Struct/03-relationships/03.01-actor-to-csp-encoding.md", 
         "6. 实例与反例 (Examples \\& Counter-examples)", "{#6-实例与反例-examples--counter-examples}"),
        ("Struct/03-relationships/03.02-flink-to-process-calculus.md", 
         "Flink 到进程演算编码 (Flink-to-Process Calculus Encoding)", "{#flink-到进程演算编码-flink-to-process-calculus-encoding}"),
        ("Struct/03-relationships/03.04-bisimulation-equivalences.md", 
         "Def-S-15-02. 弱互模拟与分支互模拟 (Weak \\& Branching Bisimulation)", "{#def-s-15-02-弱互模拟与分支互模拟}"),
        ("Struct/03-relationships/03.05-cross-model-mappings.md", 
         "5. 形式证明 / 工程论证 (Proof / Engineering Argument)", "{#5-形式证明--工程论证-proof--engineering-argument}"),
    ]
    for filepath, header, anchor in anchors:
        if add_anchor(filepath, header, anchor):
            print(f"✅ {filepath}: {anchor}")
            total += 1
    
    # Struct/04-proofs
    print("\n=== Struct/04-proofs ===")
    anchors = [
        ("Struct/04-proofs/04.01-flink-checkpoint-correctness.md", 
         "Flink Checkpoint 正确性证明 (Flink Checkpoint Correctness Proof)", "{#flink-checkpoint-正确性证明-flink-checkpoint-correctness-proof}"),
        ("Struct/04-proofs/04.02-flink-exactly-once-correctness.md", 
         "8. 实例与反例 (Examples \\& Counter-examples)", "{#8-实例与反例-examples--counter-examples}"),
        ("Struct/04-proofs/04.05-type-safety-fg-fgg.md", 
         "6. 实例与反例 (Examples \\& Counter-examples)", "{#6-实例验证-examples--counter-examples}"),
        ("Struct/04-proofs/04.07-deadlock-freedom-choreographic.md", 
         "Def-S-23-02. Global Types (全局类型)", "{#def-s-23-02-global-types}"),
        ("Struct/04-proofs/04.07-deadlock-freedom-choreographic.md", 
         "Lemma-S-23-01. EPP 保持通信结构", "{#lemma-s-23-01-epp-保持通信结构-lemma-s-23-01-epp-preservation}"),
        ("Struct/04-proofs/04.07-deadlock-freedom-choreographic.md", 
         "Prop-S-23-01. Choreography 的合流性", "{#prop-s-23-01-choreography-的合流性-prop-s-23-01-choreography-confluence}"),
    ]
    for filepath, header, anchor in anchors:
        if add_anchor(filepath, header, anchor):
            print(f"✅ {filepath}: {anchor}")
            total += 1
    
    # Struct/05-06
    print("\n=== Struct/05-06 ===")
    anchors = [
        ("Struct/05-comparative-analysis/05.01-go-vs-scala-expressiveness.md", 
         "6. 实例与反例 (Examples \\& Counter-examples)", "{#6-实例与反例-examples--counter-examples}"),
        ("Struct/06-frontier/06.01-open-problems-streaming-verification.md", 
         "5. 形式证明 / 工程论证 (Proof / Engineering Argument)", "{#5-形式证明--工程论证-proof--engineering-argument}"),
    ]
    for filepath, header, anchor in anchors:
        if add_anchor(filepath, header, anchor):
            print(f"✅ {filepath}: {anchor}")
            total += 1
    
    # Knowledge
    print("\n=== Knowledge ===")
    if add_anchor("Knowledge/06-frontier/wasm-dataflow-patterns.md",
                  "WebAssembly 数据流模式：浏览器-边缘-云统一执行模型",
                  "{#webassembly-数据流模式浏览器-边缘-云统一执行模型-wasm-dataflow-patterns}"):
        print(f"✅ wasm-dataflow-patterns.md")
        total += 1
    
    print(f"\n🔧 总计添加: {total} 个锚点")

if __name__ == '__main__':
    main()
