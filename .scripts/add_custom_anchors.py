#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为文档中的关系标题添加自定义锚点
解决特殊字符导致的锚点不匹配问题
"""

import os
import re
from pathlib import Path

class CustomAnchorAdder:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.fixes_applied = []
        
    def read_file(self, filepath):
        """读取文件内容"""
        full_path = self.base_dir / filepath
        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            print(f"读取文件 {filepath} 失败: {e}")
            return None
    
    def write_file(self, filepath, content):
        """写入文件内容"""
        full_path = self.base_dir / filepath
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"写入文件 {filepath} 失败: {e}")
            return False

    def _slugify(self, text):
        """将标题转换为GitHub风格的锚点"""
        # 移除markdown标记
        text = re.sub(r'\*\*', '', text)
        text = re.sub(r'`', '', text)
        text = re.sub(r'<[^>]+>', '', text)
        # 转换为小写
        text = text.lower()
        # 替换特殊字符为连字符
        text = re.sub(r'[^\w\s\u4e00-\u9fff-]', '-', text)
        text = re.sub(r'[\s]+', '-', text)
        # 移除首尾连字符
        text = text.strip('-')
        return text

    def add_custom_anchors_to_file(self, filepath, title_patterns):
        """为文档中的特定标题添加自定义锚点"""
        content = self.read_file(filepath)
        if not content:
            return False
        
        modified = False
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            new_line = line
            for pattern, anchor in title_patterns.items():
                # 匹配标题行
                if re.match(rf'^###\s+{re.escape(pattern)}\s*$', line):
                    # 检查是否已有自定义锚点
                    if '{#' not in line:
                        new_line = f"{line} {{#{anchor}}}"
                        modified = True
                        self.fixes_applied.append({
                            'file': filepath,
                            'line': line,
                            'anchor': anchor
                        })
                    break
            new_lines.append(new_line)
        
        if modified:
            content = '\n'.join(new_lines)
            if self.write_file(filepath, content):
                print(f"✓ 添加自定义锚点: {filepath}")
                return True
        return False

    def run_all_fixes(self):
        """运行所有修复"""
        print("="*70)
        print("添加自定义锚点")
        print("="*70)
        
        # 修复 Struct/01-foundation/01.03-actor-model-formalization.md
        self.add_custom_anchors_to_file("Struct/01-foundation/01.03-actor-model-formalization.md", {
            "关系 1：Classic Actor `⊂` Erlang Actor": "关系-1-classic-actor--erlang-actor",
            "关系 2：Actor 模型 `⊂` 异步 π-演算": "关系-2-actor-模型--异步-π-演算",
            "关系 3：Erlang/OTP `≈` Akka Actor（核心语义双模拟等价）": "关系-3-erlangotp-akka-actor核心语义双模拟等价",
            "关系 4：Actor 模型 `↔` Dataflow 模型（图灵完备等价）": "关系-4-actor-模型--dataflow-模型图灵完备等价",
        })
        
        # 修复 Struct/01-foundation/01.04-dataflow-model-formalization.md
        self.add_custom_anchors_to_file("Struct/01-foundation/01.04-dataflow-model-formalization.md", {
            "关系 1: Dataflow Model `⊃` Kahn 进程网络 (KPN)": "关系-1-dataflow-model--kahn-进程网络-kpn",
            "关系 2: 同步数据流 (SDF) `⊂` 动态数据流 (DDF) `≈` Dataflow Model": "关系-2-同步数据流-sdf--动态数据流-ddf--dataflow-model",
            "关系 3: Dataflow 理论模型 `↦` Flink Runtime 实现": "关系-3-dataflow-理论模型--flink-runtime-实现",
        })
        
        # 修复 Struct/02-properties/02.01-determinism-in-streaming.md
        self.add_custom_anchors_to_file("Struct/02-properties/02.01-determinism-in-streaming.md", {
            "关系 1: 确定性流处理 `≃` Kahn 网络确定性": "关系-1-确定性流处理--kahn-网络确定性",
            "关系 2: 汇合归约 `⇒` Dataflow 确定性": "关系-2-汇合归约--dataflow-确定性",
            "关系 3: 可观测确定性 `⊂` 语义确定性": "关系-3-可观测确定性--语义确定性",
        })
        
        # 修复 Struct/02-properties/02.02-consistency-hierarchy.md
        self.add_custom_anchors_to_file("Struct/02-properties/02.02-consistency-hierarchy.md", {
            "关系 2: 内部一致性 `≈` Chandy-Lamport 分布式快照": "关系-2-内部一致性--chandy-lamport-分布式快照",
            "反例 4.1 (内部一致 ≠ 端到端一致)": "反例-41-内部一致--端到端一致",
        })
        
        # 修复 Struct/02-properties/02.03-watermark-monotonicity.md
        self.add_custom_anchors_to_file("Struct/02-properties/02.03-watermark-monotonicity.md", {
            "步骤 1：基例 — Source 算子的 Watermark 单调性": "步骤-1-基例--source-算子的-watermark-单调性",
            "步骤 3：归纳步骤 — 第 $k$ 个算子的单调性保持": "步骤-3-归纳步骤--第-k-个算子的单调性保持",
        })
        
        # 修复 Struct/02-properties/02.04-liveness-and-safety.md
        self.add_custom_anchors_to_file("Struct/02-properties/02.04-liveness-and-safety.md", {
            "关系 1: 安全性 `⊂` 闭集 (Borel拓扑)": "关系-1-安全性--闭集-borel拓扑",
            "关系 2: 活性 `≈` 稠密集": "关系-2-活性--稠密集",
            "关系 3: Actor模型 `⊆` 活性验证需公平性": "关系-3-actor模型--活性验证需公平性",
            "关系 4: Safety `↦` 运行时监控, Liveness `↦` 模型检测": "关系-4-safety--运行时监控-liveness--模型检测",
        })
        
        # 修复 Struct/03-relationships/03.02-flink-to-process-calculus.md
        self.add_custom_anchors_to_file("Struct/03-relationships/03.02-flink-to-process-calculus.md", {
            "关系 1: Flink Dataflow 图 `↦` π-演算进程网络": "关系-1-flink-dataflow-图--π-演算进程网络",
            "关系 2: Checkpoint 屏障协议 `≈` Chandy-Lamport 快照算法": "关系-2-checkpoint-屏障协议--chandy-lamport-快照算法",
            "关系 3: Flink Exactly-Once `↦` π-演算幂等进程组合": "关系-3-flink-exactly-once--π-演算幂等进程组合",
        })
        
        # 修复 Struct/04-proofs/04.01-flink-checkpoint-correctness.md
        self.add_custom_anchors_to_file("Struct/04-proofs/04.01-flink-checkpoint-correctness.md", {
            "关系 1: Flink Checkpoint `↦` Chandy-Lamport 分布式快照": "关系-1-flink-checkpoint--chandy-lamport-分布式快照",
            "关系 2: Checkpoint 对齐 `⟹` Consistent Cut": "关系-2-checkpoint-对齐--consistent-cut",
            "关系 3: 异步快照 `≈` 同步快照（语义等价）": "关系-3-异步快照--同步快照语义等价",
        })
        
        # 修复 Struct/04-proofs/04.03-chandy-lamport-consistency.md
        self.add_custom_anchors_to_file("Struct/04-proofs/04.03-chandy-lamport-consistency.md", {
            "关系 1: Marker 接收 `↦` 状态记录触发": "关系-1-marker-接收--状态记录触发",
            "关系 2: 通道记录规则 `⟹` 无消息丢失或重复": "关系-2-通道记录规则--无消息丢失或重复",
            "关系 3: Chandy-Lamport `≈` Flink Checkpoint (语义等价)": "关系-3-chandy-lamport--flink-checkpoint-语义等价",
        })
        
        # 修复 Struct/04-proofs/04.04-watermark-algebra-formal-proof.md
        self.add_custom_anchors_to_file("Struct/04-proofs/04.04-watermark-algebra-formal-proof.md", {
            "Lemma-S-20-01 (⊔ 结合律)": "lemma-s-20-01--结合律",
            "Lemma-S-20-02 (⊔ 交换律)": "lemma-s-20-02--交换律",
            "Lemma-S-20-03 (⊔ 幂等律)": "lemma-s-20-03--幂等律",
            "Lemma-S-20-04 (⊔ 吸收律与单位元)": "lemma-s-20-04--吸收律与单位元",
            "关系 1: Watermark 格 `↦` 完备格理论": "关系-1-watermark-格--完备格理论",
            "关系 2: Watermark 合并 `⟹` 单调性保持": "关系-2-watermark-合并--单调性保持",
            "关系 3: Watermark 传播 `≈` 最小上界计算": "关系-3-watermark-传播--最小上界计算",
            "反例 4.2 (缺失 ⊥ 元素的格不完备性)": "反例-42-缺失--元素的格不完备性",
        })
        
        # 修复 Struct/04-proofs/04.07-deadlock-freedom-choreographic.md
        self.add_custom_anchors_to_file("Struct/04-proofs/04.07-deadlock-freedom-choreographic.md", {
            "关系 1: Global Types `↔` Session Types": "关系-1-global-types--session-types",
            "关系 2: EPP `≈` Bisimulation (互模拟等价)": "关系-2-epp--bisimulation-互模拟等价",
            "关系 3: Choreography `↦` Process Calculus": "关系-3-choreography--process-calculus",
        })

        print("\n" + "="*70)
        print("修复完成统计")
        print("="*70)
        print(f"总修复数: {len(self.fixes_applied)}")

def main():
    base_dir = Path(__file__).parent.parent
    adder = CustomAnchorAdder(base_dir)
    adder.run_all_fixes()
    print("\n自定义锚点添加完成!")
    return 0

if __name__ == '__main__':
    exit(main())
