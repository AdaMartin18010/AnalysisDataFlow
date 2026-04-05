#!/usr/bin/env python3
"""
修复最后4个锚点问题
"""

from pathlib import Path

def fix_file(filepath, fixes):
    """应用修复到文件"""
    path = Path(filepath)
    if not path.exists():
        return 0
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for old, new in fixes:
        content = content.replace(old, new)
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return len(fixes)
    return 0

def main():
    # 修复最后4个问题
    all_fixes = {
        "Knowledge/01-concept-atlas/streaming-models-mindmap.md": [
            # 在示例 6.4 标题后添加锚点
            ("### 示例 6.4 CEP + Pub/Sub 混合实例：金融风控实时告警\n",
             "### 示例 6.4 CEP + Pub/Sub 混合实例：金融风控实时告警 {#示例-64-cep--pubsub-混合实例金融风控实时告警}\n"),
        ],
        "Struct/02-properties/02.03-watermark-monotonicity.md": [
            # 给主标题添加额外的锚点
            ("# Watermark 单调性定理 (Watermark Monotonicity Theorem) {#步骤-1-基例--source-算子的-watermark-单调性}",
             "# Watermark 单调性定理 (Watermark Monotonicity Theorem) {#watermark-单调性定理-watermark-monotonicity-theorem}"),
        ],
        "Struct/04-proofs/04.04-watermark-algebra-formal-proof.md": [
            # 删除重复的锚点
            ("### Lemma-S-20-02 (⊔ 交换律) {#lemma-s-20-02--交换律} {#lemma-s-20-02--交换律}",
             "### Lemma-S-20-02 (⊔ 交换律) {#lemma-s-20-02--交换律}"),
            ("### Lemma-S-20-03 (⊔ 幂等律) {#lemma-s-20-03--幂等律} {#lemma-s-20-03--幂等律}",
             "### Lemma-S-20-03 (⊔ 幂等律) {#lemma-s-20-03--幂等律}"),
        ],
    }
    
    total = 0
    for filepath, fixes in all_fixes.items():
        fixed = fix_file(filepath, fixes)
        if fixed > 0:
            print(f"✅ {filepath}: 修复 {fixed} 个问题")
            total += fixed
    
    print(f"\n🔧 总计修复: {total} 个问题")

if __name__ == '__main__':
    main()
