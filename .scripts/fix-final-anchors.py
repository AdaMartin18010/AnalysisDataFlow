#!/usr/bin/env python3
"""
最终锚点修复 - 解决剩余的31个问题
"""

import re
from pathlib import Path

def fix_links_in_file(file_path, replacements):
    """修复文件中的链接"""
    path = Path(file_path)
    if not path.exists():
        return 0
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for old, new in replacements:
        content = content.replace(old, new)
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return len(replacements)
    return 0

def main():
    fixes = {
        # Knowledge
        "Knowledge/01-concept-atlas/streaming-models-mindmap.md": [
            ("](#关系-1-dataflow--actor图灵完备等价-关系-1-dataflow-actor-图灵完备等价)", "](#关系-1-dataflow-actor-图灵完备等价)"),
            ("](#关系-2-dataflow--csp异步-vs-同步的连续统-关系-2-dataflow-csp-异步-vs-同步的连续统)", "](#关系-2-dataflow-csp-异步-vs-同步的连续统)"),
            ("](#关系-3-pubsub--actor解耦是地址匿名化的特例-关系-3-pubsub-actor-解耦是地址匿名化的特例)", "](#关系-3-pubsub-actor-解耦是地址匿名化的特例)"),
            ("](#关系-4-cep--dataflow模式匹配是有状态算子的语法糖-关系-4-cep-dataflow-模式匹配是有状态算子的语法糖)", "](#关系-4-cep-dataflow-模式匹配是有状态算子的语法糖)"),
            ("](#5-形式证明--工程论证-proof--engineering-argument)", "](#5-形式证明--工程论证)"),
        ],
        "Knowledge/02-design-patterns/pattern-log-analysis.md": [
            ("](#关系-log-analysis--windowed-aggregation-关系-log-analysis--windowed-aggregation)", "](#关系-log-analysis--windowed-aggregation)"),
            ("](#关系-log-analysis--cep-pattern-关系-log-analysis--cep-pattern)", "](#关系-log-analysis--cep-pattern)"),
            ("](#5-形式证明--工程论证)", "](#5-形式证明--工程论证)"),
        ],
        "Knowledge/02-design-patterns/pattern-windowed-aggregation.md": [
            ("](#关系-windowed-aggregation--def-s-04-05-关系-windowed-aggregation--def-s-04-05)", "](#关系-windowed-aggregation--def-s-04-05)"),
            ("](#5-形式证明--工程论证)", "](#5-形式证明--工程论证)"),
        ],
        
        # Struct foundation
        "Struct/01-foundation/01.03-actor-model-formalization.md": [
            ("](#关系-1classic-actor--erlang-actor-关系-1-classic-actor--erlang-actor)", "](#关系-1-classic-actor--erlang-actor)"),
            ("](#关系-2actor-模型--异步-π-演算-关系-2-actor-模型--异步-π-演算)", "](#关系-2-actor-模型--异步-π-演算)"),
            ("](#关系-3erlangotp--akka-actor核心语义双模拟等价-关系-3-erlangotp--akka-actor核心语义双模拟等价)", "](#关系-3-erlangotp--akka-actor核心语义双模拟等价)"),
            ("](#关系-4actor-模型--dataflow-模型图灵完备等价-关系-4-actor-模型--dataflow-模型图灵完备等价)", "](#关系-4-actor-模型--dataflow-模型图灵完备等价)"),
        ],
        
        # Struct properties
        "Struct/02-properties/02.03-watermark-monotonicity.md": [
            ("](#watermark-单调性定理)", "](#watermark-单调性定理-watermark-monotonicity-theorem)"),
            ("](#5-形式证明--工程论证)", "](#5-形式证明--工程论证-proof--engineering-argument)"),
        ],
        "Struct/02-properties/02.04-liveness-and-safety.md": [
            ("](#关系-4-safety--运行时监控-liveness--模型检测-关系-4-safety--运行时监控-liveness--模型检测)", "](#关系-4-safety--运行时监控-liveness--模型检测)"),
            ("](#6-实例与反例)", "](#6-实例与反例-examples--counter-examples)"),
        ],
        
        # Struct proofs
        "Struct/04-proofs/04.01-flink-checkpoint-correctness.md": [
            ("](#flink-checkpoint-正确性证明)", "](#flink-checkpoint-正确性证明-flink-checkpoint-correctness-proof)"),
            ("](#反例-42)", "](#反例-42-异步快照失败导致-checkpoint-不完整)"),
        ],
        "Struct/04-proofs/04.03-chandy-lamport-consistency.md": [
            ("](#def-s-19-02-一致割集--consistent-cut)", "](#def-s-19-02-一致割集--consistent-cut)"),
            ("](#lemma-s-19-02-一致割集引理--consistent-cut-lemma)", "](#lemma-s-19-02-一致割集引理--consistent-cut-lemma)"),
            ("](#示例-62)", "](#示例-62-环形拓扑中的-marker-传播)"),
        ],
        "Struct/04-proofs/04.04-watermark-algebra-formal-proof.md": [
            ("](#lemma-s-20-02-交换律)", "](#lemma-s-20-02-交换律-lemma-s-20-02--交换律)"),
            ("](#lemma-s-20-03-幂等律)", "](#lemma-s-20-03-幂等律-lemma-s-20-03--幂等律)"),
        ],
        
        # Struct frontier
        "Struct/06-frontier/06.02-choreographic-streaming-programming.md": [
            ("](#关系-1-choreographic--传统数据流-关系-1-choreographic-传统数据流)", "](#关系-1-choreographic--传统数据流)"),
        ],
        "Struct/06-frontier/06.03-ai-agent-session-types.md": [
            ("](#关系-2-llm-agent-protocol--choreography-关系-2-llm-agent-protocol--choreography)", "](#关系-2-llm-agent-protocol--choreography)"),
        ],
        "Struct/06-frontier/06.04-pdot-path-dependent-types.md": [
            ("](#41-pdot-引入的动机)", "](#41-pdot-引入的动机分析)"),
            ("](#5-形式证明--工程论证)", "](#5-形式证明--工程论证-proof--engineering-argument)"),
            ("](#示例-63)", "](#示例-63-dataflow-算子链的类型追踪)"),
        ],
    }
    
    total = 0
    for file_path, replacements in fixes.items():
        fixed = fix_links_in_file(file_path, replacements)
        if fixed > 0:
            print(f"✅ {file_path}: 修复 {fixed} 个问题")
            total += fixed
    
    print(f"\n🔧 总计修复: {total} 个问题")

if __name__ == '__main__':
    main()
