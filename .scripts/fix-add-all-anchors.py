#!/usr/bin/env python3
"""
为所有缺失的锚点添加自定义锚点到标题
"""

import re
from pathlib import Path

def add_anchor_to_header(filepath, header_text, anchor_text):
    """在指定标题后添加自定义锚点"""
    path = Path(filepath)
    if not path.exists():
        return 0
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 尝试多种匹配模式
    patterns = [
        # 模式1: 标题后没有锚点
        (r'^(#{1,6}\s+' + re.escape(header_text) + r')$', r'\1 {' + anchor_text + '}'),
        # 模式2: 标题后可能有空格
        (r'^(#{1,6}\s+' + re.escape(header_text) + r')\s*$', r'\1 {' + anchor_text + '}'),
    ]
    
    for pattern, replacement in patterns:
        content_new = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        if content_new != content:
            content = content_new
            break
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return 1
    return 0

def main():
    total = 0
    
    # 根据错误报告，添加所有缺失的锚点
    anchors_to_add = [
        # CASE-STUDIES.md
        ("CASE-STUDIES.md", "🆕 新增详细案例（Knowledge/10-case-studies/）", "{#新增详细案例}"),
        
        # Knowledge/06-frontier/wasm-dataflow-patterns.md
        ("Knowledge/06-frontier/wasm-dataflow-patterns.md", 
         "WebAssembly 数据流模式：浏览器-边缘-云统一执行模型",
         "{#webassembly-数据流模式浏览器-边缘-云统一执行模型-wasm-dataflow-patterns}"),
        
        # Struct/01-foundation/01.04-dataflow-model-formalization.md
        ("Struct/01-foundation/01.04-dataflow-model-formalization.md",
         "关系 1: Dataflow Model `⊃` Kahn 进程网络 (KPN)",
         "{#关系-1-dataflow-model--kahn-进程网络-kpn}"),
        ("Struct/01-foundation/01.04-dataflow-model-formalization.md",
         "关系 2: 同步数据流 (SDF) `⊂` 动态数据流 (DDF) `≈` Dataflow Model",
         "{#关系-2-同步数据流-sdf--动态数据流-ddf--dataflow-model}"),
        ("Struct/01-foundation/01.04-dataflow-model-formalization.md",
         "关系 3: Dataflow 理论模型 `↦` Flink Runtime 实现",
         "{#关系-3-dataflow-理论模型--flink-runtime-实现}"),
        
        # Struct/01-foundation/01.05-csp-formalization.md
        ("Struct/01-foundation/01.05-csp-formalization.md",
         "基础情形 ($Q = 0$)",
         "{#基础情形-q--0}"),
        ("Struct/01-foundation/01.05-csp-formalization.md",
         "6. 实例验证 (Examples \\& Verification)",
         "{#6-实例验证-examples--verification}"),
        
        # Struct/01-foundation/01.06-petri-net-formalization.md
        ("Struct/01-foundation/01.06-petri-net-formalization.md",
         "Petri 网形式化 (Petri Net Formalization)",
         "{#petri-网形式化-petri-net-formalization}"),
        ("Struct/01-foundation/01.06-petri-net-formalization.md",
         "图 1-1: Petri 网结构示例",
         "{#图-1-1-petri-网结构示例}"),
        ("Struct/01-foundation/01.06-petri-net-formalization.md",
         "6. 实例验证 (Examples \\& Verification)",
         "{#6-实例验证-examples--verification}"),
        
        # Struct/01-foundation/01.07-session-types.md
        ("Struct/01-foundation/01.07-session-types.md",
         "5. 形式证明 / 工程论证 (Proof)",
         "{#5-形式证明--工程论证-proof}"),
        
        # Struct/02-properties/02.01-determinism-in-streaming.md
        ("Struct/02-properties/02.01-determinism-in-streaming.md",
         "5. 形式证明 / 工程论证 (Proof / Engineering Argument)",
         "{#5-形式证明--工程论证-proof--engineering-argument}"),
        
        # Struct/02-properties/02.02-consistency-hierarchy.md
        ("Struct/02-properties/02.02-consistency-hierarchy.md",
         "关系 1: Dataflow 确定性定理与一致性层级的联系",
         "{#关系-1-dataflow-确定性定理与一致性层级的联系}"),
        
        # Struct/03-relationships/03.02-flink-to-process-calculus.md
        ("Struct/03-relationships/03.02-flink-to-process-calculus.md",
         "Flink 到进程演算编码 (Flink-to-Process Calculus Encoding)",
         "{#flink-到进程演算编码-flink-to-process-calculus-encoding}"),
        
        # Struct/03-relationships/03.04-bisimulation-equivalences.md
        ("Struct/03-relationships/03.04-bisimulation-equivalences.md",
         "Def-S-15-02. 弱互模拟与分支互模拟 (Weak \\& Branching Bisimulation)",
         "{#def-s-15-02-弱互模拟与分支互模拟}"),
        
        # Struct/04-proofs/04.05-type-safety-fg-fgg.md
        ("Struct/04-proofs/04.05-type-safety-fg-fgg.md",
         "6. 实例与反例 (Examples \\& Counter-examples)",
         "{#6-实例验证-examples--counter-examples}"),
        
        # Struct/04-proofs/04.07-deadlock-freedom-choreographic.md
        ("Struct/04-proofs/04.07-deadlock-freedom-choreographic.md",
         "Def-S-23-02. Global Types (全局类型)",
         "{#def-s-23-02-global-types}"),
        ("Struct/04-proofs/04.07-deadlock-freedom-choreographic.md",
         "Lemma-S-23-01. EPP 保持通信结构",
         "{#lemma-s-23-01-epp-保持通信结构-lemma-s-23-01-epp-preservation}"),
        ("Struct/04-proofs/04.07-deadlock-freedom-choreographic.md",
         "Prop-S-23-01. Choreography 的合流性",
         "{#prop-s-23-01-choreography-的合流性-prop-s-23-01-choreography-confluence}"),
    ]
    
    for filepath, header, anchor in anchors_to_add:
        result = add_anchor_to_header(filepath, header, anchor)
        if result > 0:
            print(f"✅ {filepath}: 添加锚点 {anchor}")
            total += result
        else:
            # 尝试查找并打印实际标题
            path = Path(filepath)
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # 查找类似标题
                similar = re.findall(rf'^#{1,6}\s+.*{re.escape(header[:20])}.*$', content, re.MULTILINE)
                if similar:
                    print(f"⚠️  {filepath}: 未找到 '{header[:40]}...'，类似标题: {similar[0][:60]}")
                else:
                    print(f"⚠️  {filepath}: 未找到 '{header[:40]}...'")
    
    print(f"\n🔧 总计添加: {total} 个锚点")

if __name__ == '__main__':
    main()
