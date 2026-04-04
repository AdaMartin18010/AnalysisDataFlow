#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复锚点问题
主要修复特殊字符在锚点中的处理问题
"""

import os
import re
from pathlib import Path

class AnchorFixer:
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

    def fix_document_anchors(self, filepath, anchor_mappings):
        """修复文档中的锚点链接"""
        content = self.read_file(filepath)
        if not content:
            return False
        
        modified = False
        for old_anchor, new_anchor in anchor_mappings.items():
            if old_anchor in content:
                content = content.replace(old_anchor, new_anchor)
                modified = True
                self.fixes_applied.append({
                    'file': filepath,
                    'old': old_anchor,
                    'new': new_anchor
                })
        
        if modified:
            if self.write_file(filepath, content):
                print(f"✓ 修复锚点: {filepath}")
                return True
        return False

    def run_all_fixes(self):
        """运行所有锚点修复"""
        print("="*70)
        print("批量修复锚点问题")
        print("="*70)
        
        # 修复 BENCHMARK-REPORT.md
        self.fix_document_anchors("BENCHMARK-REPORT.md", {
            "#5-形式证明--工程论证-proof--engineering-argument-proof--engineering-argument": "#5-形式证明--工程论证",
        })
        
        # 修复 TROUBLESHOOTING-COMPLETE.md
        self.fix_document_anchors("TROUBLESHOOTING-COMPLETE.md", {
            "#5-形式证明--工程论证-proof--engineering-argument": "#5-形式证明--工程论证",
            "#关系-1-问题症状--根因映射": "#关系-1",
            "#关系-2-排查流程--故障恢复": "#关系-2",
        })
        
        # 修复 Struct/01-foundation/01.03-actor-model-formalization.md
        self.fix_document_anchors("Struct/01-foundation/01.03-actor-model-formalization.md", {
            "#关系-1classic-actor-⊂-erlang-actor": "#关系-1-classic-actor--erlang-actor",
            "#关系-2actor-模型-⊂-异步-π-演算": "#关系-2-actor-模型--异步-π-演算",
            "#关系-3erlangotp-≈-akka-actor核心语义双模拟等价": "#关系-3-erlangotp-akka-actor核心语义双模拟等价",
            "#关系-4actor-模型-↔-dataflow-模型图灵完备等价": "#关系-4-actor-模型--dataflow-模型图灵完备等价",
        })
        
        # 修复 Struct/01-foundation/01.04-dataflow-model-formalization.md
        self.fix_document_anchors("Struct/01-foundation/01.04-dataflow-model-formalization.md", {
            "#关系-1-dataflow-model-⊃-kahn-进程网络-kpn": "#关系-1-dataflow-model--kahn-进程网络-kpn",
            "#关系-2-同步数据流-sdf-⊂-动态数据流-ddf-≈-dataflow-model": "#关系-2-同步数据流-sdf--动态数据流-ddf--dataflow-model",
            "#关系-3-dataflow-理论模型-↦-flink-runtime-实现": "#关系-3-dataflow-理论模型--flink-runtime-实现",
        })
        
        # 修复 Struct/02-properties/02.01-determinism-in-streaming.md
        self.fix_document_anchors("Struct/02-properties/02.01-determinism-in-streaming.md", {
            "#关系-1-确定性流处理-≃-kahn-网络确定性": "#关系-1-确定性流处理--kahn-网络确定性",
            "#关系-2-汇合归约-⇒-dataflow-确定性": "#关系-2-汇合归约--dataflow-确定性",
            "#关系-3-可观测确定性-⊂-语义确定性": "#关系-3-可观测确定性--语义确定性",
        })
        
        # 修复 Struct/02-properties/02.02-consistency-hierarchy.md
        self.fix_document_anchors("Struct/02-properties/02.02-consistency-hierarchy.md", {
            "#关系-2-内部一致性-≈-chandy-lamport-分布式快照": "#关系-2-内部一致性--chandy-lamport-分布式快照",
            "#反例-41-内部一致-≠-端到端一致": "#反例-41-内部一致--端到端一致",
        })
        
        # 修复 Struct/02-properties/02.03-watermark-monotonicity.md
        self.fix_document_anchors("Struct/02-properties/02.03-watermark-monotonicity.md", {
            "#步骤-1基例-—-source-算子的-watermark-单调性": "#步骤-1-基例--source-算子的-watermark-单调性",
            "#步骤-3归纳步骤-—-第-k-个算子的单调性保持": "#步骤-3-归纳步骤--第-k-个算子的单调性保持",
        })
        
        # 修复 Struct/02-properties/02.04-liveness-and-safety.md
        self.fix_document_anchors("Struct/02-properties/02.04-liveness-and-safety.md", {
            "#关系-1-安全性-⊂-闭集-borel拓扑": "#关系-1-安全性--闭集-borel拓扑",
            "#关系-2-活性-≈-稠密集": "#关系-2-活性--稠密集",
            "#关系-3-actor模型-⊆-活性验证需公平性": "#关系-3-actor模型--活性验证需公平性",
            "#关系-4-safety-↦-运行时监控-liveness-↦-模型检测": "#关系-4-safety--运行时监控-liveness--模型检测",
        })
        
        # 修复 Struct/03-relationships/03.02-flink-to-process-calculus.md
        self.fix_document_anchors("Struct/03-relationships/03.02-flink-to-process-calculus.md", {
            "#关系-1-flink-dataflow-图-↦-π-演算进程网络": "#关系-1-flink-dataflow-图--π-演算进程网络",
            "#关系-2-checkpoint-屏障协议-≈-chandy-lamport-快照算法": "#关系-2-checkpoint-屏障协议--chandy-lamport-快照算法",
            "#关系-3-flink-exactly-once-↦-π-演算幂等进程组合": "#关系-3-flink-exactly-once--π-演算幂等进程组合",
        })
        
        # 修复 Struct/04-proofs/04.01-flink-checkpoint-correctness.md
        self.fix_document_anchors("Struct/04-proofs/04.01-flink-checkpoint-correctness.md", {
            "#关系-1-flink-checkpoint-↦-chandy-lamport-分布式快照": "#关系-1-flink-checkpoint--chandy-lamport-分布式快照",
            "#关系-2-checkpoint-对齐-⟹-consistent-cut": "#关系-2-checkpoint-对齐--consistent-cut",
            "#关系-3-异步快照-≈-同步快照语义等价": "#关系-3-异步快照--同步快照语义等价",
        })
        
        # 修复 Struct/04-proofs/04.03-chandy-lamport-consistency.md
        self.fix_document_anchors("Struct/04-proofs/04.03-chandy-lamport-consistency.md", {
            "#关系-1-marker-接收-↦-状态记录触发": "#关系-1-marker-接收--状态记录触发",
            "#关系-2-通道记录规则-⟹-无消息丢失或重复": "#关系-2-通道记录规则--无消息丢失或重复",
            "#关系-3-chandy-lamport-≈-flink-checkpoint-语义等价": "#关系-3-chandy-lamport--flink-checkpoint-语义等价",
        })
        
        # 修复 Struct/04-proofs/04.04-watermark-algebra-formal-proof.md
        self.fix_document_anchors("Struct/04-proofs/04.04-watermark-algebra-formal-proof.md", {
            "#lemma-s-20-01-⊔-结合律": "#lemma-s-20-01--结合律",
            "#lemma-s-20-02-⊔-交换律": "#lemma-s-20-02--交换律",
            "#lemma-s-20-03-⊔-幂等律": "#lemma-s-20-03--幂等律",
            "#lemma-s-20-04-⊔-吸收律与单位元": "#lemma-s-20-04--吸收律与单位元",
            "#关系-1-watermark-格-↦-完备格理论": "#关系-1-watermark-格--完备格理论",
            "#关系-2-watermark-合并-⟹-单调性保持": "#关系-2-watermark-合并--单调性保持",
            "#关系-3-watermark-传播-≈-最小上界计算": "#关系-3-watermark-传播--最小上界计算",
            "#反例-42-缺失-⊥-元素的格不完备性": "#反例-42-缺失--元素的格不完备性",
        })
        
        # 修复 Struct/04-proofs/04.07-deadlock-freedom-choreographic.md
        self.fix_document_anchors("Struct/04-proofs/04.07-deadlock-freedom-choreographic.md", {
            "#关系-1-global-types-↔-session-types": "#关系-1-global-types--session-types",
            "#关系-2-epp-≈-bisimulation-互模拟等价": "#关系-2-epp--bisimulation-互模拟等价",
            "#关系-3-choreography-↦-process-calculus": "#关系-3-choreography--process-calculus",
        })
        
        # 修复 Knowledge 文档中的 "5-形式证明--工程论证-proof--engineering-argument" 问题
        knowledge_files_with_proof_anchor = [
            "Knowledge/03-business-patterns/log-monitoring.md",
            "Knowledge/03-business-patterns/netflix-streaming-pipeline.md",
            "Knowledge/03-business-patterns/real-time-recommendation.md",
            "Knowledge/03-business-patterns/spotify-music-recommendation.md",
            "Knowledge/03-business-patterns/stripe-payment-processing.md",
            "Knowledge/03-business-patterns/uber-realtime-platform.md",
            "Knowledge/04-technology-selection/flink-vs-risingwave.md",
            "Knowledge/04-technology-selection/paradigm-selection-guide.md",
            "Knowledge/04-technology-selection/streaming-database-guide.md",
            "Knowledge/05-mapping-guides/struct-to-flink-mapping.md",
            "Knowledge/05-mapping-guides/theory-to-code-patterns.md",
            "Knowledge/06-frontier/edge-llm-realtime-inference.md",
            "Knowledge/06-frontier/edge-streaming-patterns.md",
            "Knowledge/06-frontier/materialize-comparison-guide.md",
            "Knowledge/06-frontier/risingwave-integration-guide.md",
            "Knowledge/06-frontier/streaming-database-ecosystem-comparison.md",
            "Knowledge/06-frontier/streaming-databases.md",
            "Knowledge/07-best-practices/07.02-performance-tuning-patterns.md",
            "Knowledge/07-best-practices/07.03-troubleshooting-guide.md",
            "Knowledge/07-best-practices/07.04-cost-optimization-patterns.md",
        ]
        
        for filepath in knowledge_files_with_proof_anchor:
            self.fix_document_anchors(filepath, {
                "#5-形式证明--工程论证-proof--engineering-argument": "#5-形式证明--工程论证",
            })

        print("\n" + "="*70)
        print("修复完成统计")
        print("="*70)
        print(f"总修复数: {len(self.fixes_applied)}")

def main():
    base_dir = Path(__file__).parent.parent
    fixer = AnchorFixer(base_dir)
    fixer.run_all_fixes()
    print("\n锚点修复完成!")
    return 0

if __name__ == '__main__':
    exit(main())
