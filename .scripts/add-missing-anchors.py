#!/usr/bin/env python3
"""
添加缺失的锚点到标题
"""

import re
from pathlib import Path

def add_anchors_to_file(file_path, anchors_to_add):
    """在指定标题后添加自定义锚点"""
    path = Path(file_path)
    if not path.exists():
        return 0
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for header_pattern, anchor_text in anchors_to_add:
        # 匹配标题行（确保标题后面没有已有锚点）
        pattern = r'^(#{1,6}\s+' + re.escape(header_pattern) + r')$'
        replacement = r'\1 {#%%ANCHOR%%}'
        content_new = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        if content_new != content:
            content = content_new.replace('{#%%ANCHOR%%}', anchor_text)
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return len(anchors_to_add)
    return 0

def main():
    fixes = {
        # Knowledge
        "Knowledge/01-concept-atlas/streaming-models-mindmap.md": [
            ("5. 形式证明 / 工程论证 (Proof / Engineering Argument)", "{#5-形式证明--工程论证}"),
            ("示例 6.4: CEP + Pub/Sub 混合实例：金融风控实时告警", "{#示例-64-cep--pubsub-混合实例金融风控实时告警}"),
        ],
        "Knowledge/02-design-patterns/pattern-log-analysis.md": [
            ("5. 形式证明 / 工程论证", "{#5-形式证明--工程论证}"),
        ],
        "Knowledge/02-design-patterns/pattern-windowed-aggregation.md": [
            ("5. 形式证明 / 工程论证", "{#5-形式证明--工程论证}"),
        ],
        
        # Struct properties
        "Struct/02-properties/02.03-watermark-monotonicity.md": [
            ("Watermark 单调性定理 (Watermark Monotonicity Theorem)", "{#watermark-单调性定理-watermark-monotonicity-theorem}"),
            ("5. 形式证明 / 工程论证 (Proof / Engineering Argument)", "{#5-形式证明--工程论证-proof--engineering-argument}"),
        ],
        "Struct/02-properties/02.04-liveness-and-safety.md": [
            ("6. 实例与反例 (Examples \\& Counter-examples)", "{#6-实例与反例-examples--counter-examples}"),
        ],
        
        # Struct proofs
        "Struct/04-proofs/04.01-flink-checkpoint-correctness.md": [
            ("Flink Checkpoint 正确性证明 (Flink Checkpoint Correctness Proof)", "{#flink-checkpoint-正确性证明-flink-checkpoint-correctness-proof}"),
        ],
        "Struct/04-proofs/04.03-chandy-lamport-consistency.md": [
            ("Def-S-19-02 (一致割集 / Consistent Cut)", "{#def-s-19-02-一致割集--consistent-cut}"),
            ("Lemma-S-19-02 (一致割集引理 / Consistent Cut Lemma)", "{#lemma-s-19-02-一致割集引理--consistent-cut-lemma}"),
        ],
        "Struct/04-proofs/04.04-watermark-algebra-formal-proof.md": [
            ("Lemma-S-20-02 (⊔ 交换律) {#lemma-s-20-02--交换律}", "{#lemma-s-20-02--交换律}"),
            ("Lemma-S-20-03 (⊔ 幂等律) {#lemma-s-20-03--幂等律}", "{#lemma-s-20-03--幂等律}"),
        ],
        
        # Struct frontier
        "Struct/06-frontier/06.02-choreographic-streaming-programming.md": [
            ("关系 1: Choreographic ⊃ 传统数据流 {#关系-1-choreographic-传统数据流}", "{#关系-1-choreographic--传统数据流}"),
        ],
        "Struct/06-frontier/06.04-pdot-path-dependent-types.md": [
            ("5. 形式证明 / 工程论证 (Proof / Engineering Argument)", "{#5-形式证明--工程论证-proof--engineering-argument}"),
        ],
    }
    
    total = 0
    for file_path, anchors in fixes.items():
        fixed = add_anchors_to_file(file_path, anchors)
        if fixed > 0:
            print(f"✅ {file_path}: 添加 {fixed} 个锚点")
            total += fixed
    
    print(f"\n🔧 总计添加: {total} 个锚点")

if __name__ == '__main__':
    main()
