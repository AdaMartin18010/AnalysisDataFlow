#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复剩余的锚点问题
"""

import os
import re
from pathlib import Path

class RemainingAnchorFixer:
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
                # 匹配标题行 (支持 ### 或 ## 级别)
                if re.match(rf'^(##|###)\s+{re.escape(pattern)}\s*$', line):
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
        """运行所有修复"""
        print("="*70)
        print("修复剩余锚点问题")
        print("="*70)
        
        # 修复 BENCHMARK-REPORT.md 和 TROUBLESHOOTING-COMPLETE.md
        # 这些文档的 "5. 形式证明 / 工程论证" 锚点问题需要检查
        # 暂时跳过，因为需要查看实际的文档结构
        
        # 修复 Struct/05-comparative-analysis/05.02-expressiveness-vs-decidability.md
        self.add_custom_anchors_to_file("Struct/05-comparative-analysis/05.02-expressiveness-vs-decidability.md", {
            "表 7.1: 模型 × 性质 × 可判定性矩阵": "表-71-模型-性质-可判定性矩阵",
        })
        
        # 修复 Struct/06-frontier/06.02-choreographic-streaming-programming.md
        self.add_custom_anchors_to_file("Struct/06-frontier/06.02-choreographic-streaming-programming.md", {
            "关系 1: Choreographic ⊃ 传统数据流": "关系-1-choreographic-传统数据流",
            "关系 2: MPST ↔ Session Types": "关系-2-mpst--session-types",
            "关系 3: 全局类型 ⟹ 死锁自由": "关系-3-全局类型--死锁自由",
        })
        
        # 修复 Struct/06-frontier/06.03-ai-agent-session-types.md
        self.add_custom_anchors_to_file("Struct/06-frontier/06.03-ai-agent-session-types.md", {
            "关系 1: MAST ↔ 传统 MPST": "关系-1-mast--传统-mpst",
            "关系 2: LLM-Agent Protocol ↦ Choreography": "关系-2-llm-agent-protocol--choreography",
            "关系 3: Type-safe Agent Communication ↦ Deadlock Freedom": "关系-3-type-safe-agent-communication--deadlock-freedom",
        })
        
        # 修复 Struct/06-frontier/06.04-pdot-path-dependent-types.md
        self.add_custom_anchors_to_file("Struct/06-frontier/06.04-pdot-path-dependent-types.md", {
            "关系 1: DOT `⊂` pDOT (表达能力严格扩展)": "关系-1-dot--pdot-表达能力严格扩展",
            "关系 2: pDOT `↦` Scala 3 类型系统": "关系-2-pdot--scala-3-类型系统",
            "关系 3: 路径依赖类型 `↔` Dataflow 状态追踪": "关系-3-路径依赖类型--dataflow-状态追踪",
        })
        
        # 修复 Knowledge/01-concept-atlas/streaming-models-mindmap.md
        self.add_custom_anchors_to_file("Knowledge/01-concept-atlas/streaming-models-mindmap.md", {
            "关系 1: Dataflow `≈` Actor（图灵完备等价）": "关系-1-dataflow--actor图灵完备等价",
            "关系 2: Dataflow `↦` CSP（异步 vs 同步的连续统）": "关系-2-dataflow--csp异步-vs-同步的连续统",
            "关系 3: Pub/Sub `⊂` Actor（解耦是地址匿名化的特例）": "关系-3-pubsub--actor解耦是地址匿名化的特例",
            "关系 4: CEP `⊂` Dataflow（模式匹配是有状态算子的语法糖）": "关系-4-cep--dataflow模式匹配是有状态算子的语法糖",
        })
        
        # 修复 Knowledge/02-design-patterns/pattern-log-analysis.md
        self.add_custom_anchors_to_file("Knowledge/02-design-patterns/pattern-log-analysis.md", {
            "关系: Log Analysis `↦` Windowed Aggregation": "关系-log-analysis--windowed-aggregation",
            "关系: Log Analysis `↦` CEP Pattern": "关系-log-analysis--cep-pattern",
        })
        
        # 修复 Knowledge/02-design-patterns/pattern-windowed-aggregation.md
        self.add_custom_anchors_to_file("Knowledge/02-design-patterns/pattern-windowed-aggregation.md", {
            "关系: Windowed Aggregation `↦` Def-S-04-05": "关系-windowed-aggregation--def-s-04-05",
        })
        
        # 修复 Knowledge/03-business-patterns/iot-stream-processing.md
        self.add_custom_anchors_to_file("Knowledge/03-business-patterns/iot-stream-processing.md", {
            "7.2 Actor + Dataflow 双层架构": "72-actor--dataflow-双层架构",
        })
        
        # 修复 Knowledge/03-business-patterns/log-monitoring.md
        self.add_custom_anchors_to_file("Knowledge/03-business-patterns/log-monitoring.md", {
            "业务模式: 日志分析与监控 (Business Pattern: Log Analysis & Monitoring)": "业务模式-日志分析与监控-business-pattern-log-analysis--monitoring",
        })
        
        # 修复 Knowledge/05-mapping-guides/struct-to-flink-mapping.md
        self.add_custom_anchors_to_file("Knowledge/05-mapping-guides/struct-to-flink-mapping.md", {
            "映射 1: Dataflow 图 → Flink DataStream API": "映射-1-dataflow-图--flink-datastream-api",
            "映射 2: Watermark 单调性 → Flink WatermarkStrategy": "映射-2-watermark-单调性--flink-watermarkstrategy",
            "映射 3: Checkpoint Barrier → Flink CheckpointCoordinator": "映射-3-checkpoint-barrier--flink-checkpointcoordinator",
            "映射 4: 一致割集 → Flink 全局状态快照": "映射-4-一致割集--flink-全局状态快照",
            "映射 5: Exactly-Once 语义 → Flink 2PC + 可重放 Source": "映射-5-exactly-once-语义--flink-2pc--可重放-source",
            "映射 6: Actor 模型 → Flink Actor 运行时": "映射-6-actor-模型--flink-actor-运行时",
            "映射 7: 类型安全 → Flink TypeInformation 系统": "映射-7-类型安全--flink-typeinformation-系统",
        })
        
        # 修复 Knowledge/06-frontier/edge-llm-realtime-inference.md
        self.add_custom_anchors_to_file("Knowledge/06-frontier/edge-llm-realtime-inference.md", {
            "Def-K-06-64: 模型量化与压缩 (Model Quantization & Compression)": "def-k-06-64-模型量化与压缩-model-quantization--compression",
        })
        
        # 修复 Knowledge/06-frontier/materialize-comparison-guide.md
        self.add_custom_anchors_to_file("Knowledge/06-frontier/materialize-comparison-guide.md", {
            "6.4 混合架构：Flink + Materialize": "64-混合架构flink--materialize",
        })
        
        # 修复 Knowledge/06-frontier/risingwave-integration-guide.md
        self.add_custom_anchors_to_file("Knowledge/06-frontier/risingwave-integration-guide.md", {
            "4.1 为什么需要 RisingWave + Flink 混合架构": "41-为什么需要-risingwave--flink-混合架构",
        })
        
        # 修复 Knowledge/06-frontier/serverless-streaming-cost-optimization.md
        self.add_custom_anchors_to_file("Knowledge/06-frontier/serverless-streaming-cost-optimization.md", {
            "AWS Lambda + MSK Serverless": "aws-lambda--msk-serverless",
            "Azure Functions + Event Hubs": "azure-functions--event-hubs",
            "GCP Cloud Functions + Pub/Sub": "gcp-cloud-functions--pubsub",
            "示例 6.1: AWS Lambda + MSK 成本优化": "示例61-aws-lambda--msk成本优化",
            "示例 6.2: Azure Functions + Event Hubs 成本对比": "示例62-azure-functions--event-hubs成本对比",
        })
        
        # 修复 Knowledge/06-frontier/streaming-access-control.md
        self.add_custom_anchors_to_file("Knowledge/06-frontier/streaming-access-control.md", {
            "Def-K-06-18: 数据血缘与策略传播 (Data Lineage & Policy Propagation)": "def-k-06-18-数据血缘与策略传播-data-lineage--policy-propagation",
        })
        
        # 修复 Knowledge/06-frontier/wasm-dataflow-patterns.md
        self.add_custom_anchors_to_file("Knowledge/06-frontier/wasm-dataflow-patterns.md", {
            "WebAssembly 数据流模式：浏览器-边缘-云统一执行模型": "webassembly-数据流模式-浏览器-边缘-云统一执行模型",
        })

        print("\n" + "="*70)
        print("修复完成统计")
        print("="*70)
        print(f"总修复数: {len(self.fixes_applied)}")

def main():
    base_dir = Path(__file__).parent.parent
    fixer = RemainingAnchorFixer(base_dir)
    fixer.run_all_fixes()
    print("\n剩余锚点修复完成!")
    return 0

if __name__ == '__main__':
    exit(main())
