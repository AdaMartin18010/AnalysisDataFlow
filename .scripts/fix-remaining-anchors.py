#!/usr/bin/env python3
"""
修复剩余锚点问题
================
处理最后101个问题
"""

import re
from pathlib import Path

def fix_struct_files():
    """修复Struct目录的锚点问题"""
    
    fixes = {
        "Struct/01-foundation/01.03-actor-model-formalization.md": [
            ("#关系-1classic-actor--erlang-actor-关系-1-classic-actor--erlang-actor", "#关系-1-classic-actor--erlang-actor"),
            ("#关系-2actor-模型--异步-π-演算-关系-2-actor-模型--异步-π-演算", "#关系-2-actor-模型--异步-π-演算"),
            ("#关系-3erlangotp--akka-actor核心语义双模拟等价-关系-3-erlangotp-akka-actor核心语义双模拟等价", "#关系-3-erlangotp--akka-actor核心语义双模拟等价"),
            ("#关系-4actor-模型--dataflow-模型图灵完备等价-关系-4-actor-模型--dataflow-模型图灵完备等价", "#关系-4-actor-模型--dataflow-模型图灵完备等价"),
        ],
        "Struct/01-foundation/01.06-petri-net-formalization.md": [
            ("#def-s-06-01-placetransition-net---pt-网", "#def-s-06-01-place-transition-net---pt-网"),
            ("#def-s-06-02-变迁触发规则---firing-rule", "#def-s-06-02-变迁触发规则--firing-rule"),
            ("#def-s-06-03-可达性与可达图---reachability-graph", "#def-s-06-03-可达性与可达图--reachability-graph"),
            ("#def-s-06-04-着色-petri-网---colored-petri-net-cpn", "#def-s-06-04-着色-petri-网--colored-petri-net-cpn"),
            ("#def-s-06-05-时间-petri-网---timed-petri-net-tpn", "#def-s-06-05-时间-petri-网--timed-petri-net-tpn"),
            ("#petri-网形式化-petri-net-formalization", "#petri-网形式化"),
            ("#图-1-1-petri-网结构示例", "#图-1-petri-网结构示例"),
            ("#6-实例验证-examples--verification", "#6-实例验证"),
        ],
        "Struct/02-properties/02.01-determinism-in-streaming.md": [
            ("#关系-1-确定性流处理--kahn-网络确定性-关系-1-确定性流处理--kahn-网络确定性", "#关系-1-确定性流处理--kahn-网络确定性"),
            ("#关系-2-汇合归约--dataflow-确定性-关系-2-汇合归约--dataflow-确定性", "#关系-2-汇合归约--dataflow-确定性"),
            ("#关系-3-可观测确定性--语义确定性-关系-3-可观测确定性--语义确定性", "#关系-3-可观测确定性--语义确定性"),
            ("#5-形式证明--工程论证-proof--engineering-argument", "#5-形式证明--工程论证"),
        ],
        "Struct/02-properties/02.02-consistency-hierarchy.md": [
            ("#关系-2-内部一致性--chandy-lamport-分布式快照-关系-2-内部一致性--chandy-lamport-分布式快照", "#关系-2-内部一致性--chandy-lamport-分布式快照"),
            ("#反例-41-内部一致--端到端一致-反例-41-内部一致--端到端一致", "#反例-41-内部一致--端到端一致"),
            ("#关系-1-dataflow-确定性定理与一致性层级的联系", "#关系-1-dataflow-确定性定理"),
        ],
        "Struct/02-properties/02.03-watermark-monotonicity.md": [
            ("#5-形式证明--工程论证-proof--engineering-argument", "#5-形式证明--工程论证"),
            ("#步骤-1基例--source-算子的-watermark-单调性-步骤-1-基例--source-算子的-watermark-单调性", "#步骤-1-基例--source-算子的-watermark-单调性"),
            ("#步骤-2归纳假设", "#步骤-2-归纳假设"),
            ("#步骤-3归纳步骤--第-k-个算子的单调性保持-步骤-3-归纳步骤--第-k-个算子的单调性保持", "#步骤-3-归纳步骤--第-k-个算子的单调性保持"),
            ("#watermark-单调性定理-watermark-monotonicity-theorem", "#watermark-单调性定理"),
        ],
        "Struct/02-properties/02.04-liveness-and-safety.md": [
            ("#活性与安全性形式化-liveness-and-safety-properties", "#活性与安全性形式化"),
            ("#关系-1-安全性--闭集-borel拓扑-关系-1-安全性--闭集-borel拓扑", "#关系-1-安全性--闭集-borel拓扑"),
            ("#关系-2-活性--稠密集-关系-2-活性--稠密集", "#关系-2-活性--稠密集"),
            ("#关系-3-actor模型--活性验证需公平性-关系-3-actor模型--活性验证需公平性", "#关系-3-actor模型--活性验证需公平性"),
            ("#6-实例与反例-examples--counter-examples", "#6-实例与反例"),
        ],
        "Struct/03-relationships/03.02-flink-to-process-calculus.md": [
            ("#flink-到进程演算编码-flink-to-process-calculus-encoding", "#flink-到进程演算编码"),
            ("#关系-2-checkpoint-屏障协议--chandy-lamport-快照算法-关系-2-checkpoint-屏障协议--chandy-lamport-快照算法", "#关系-2-checkpoint-屏障协议--chandy-lamport-快照算法"),
            ("#关系-3-flink-exactly-once--π-演算幂等进程组合-关系-3-flink-exactly-once--π-演算幂等进程组合", "#关系-3-flink-exactly-once--π-演算幂等进程组合"),
        ],
        "Struct/03-relationships/03.05-cross-model-mappings.md": [
            ("#5-形式证明--工程论证-proof--engineering-argument", "#5-形式证明--工程论证"),
        ],
        "Struct/04-proofs/04.01-flink-checkpoint-correctness.md": [
            ("#flink-checkpoint-正确性证明-flink-checkpoint-correctness-proof", "#flink-checkpoint-正确性证明"),
            ("#关系-1-flink-checkpoint--chandy-lamport-分布式快照-关系-1-flink-checkpoint--chandy-lamport-分布式快照", "#关系-1-flink-checkpoint--chandy-lamport-分布式快照"),
            ("#关系-2-checkpoint-对齐--consistent-cut-关系-2-checkpoint-对齐--consistent-cut", "#关系-2-checkpoint-对齐--consistent-cut"),
            ("#关系-3-异步快照-同步快照语义等价", "#关系-3-异步快照--同步快照语义等价"),
            ("#反例-42-异步快照失败导致-checkpoint-不完整", "#反例-42"),
        ],
        "Struct/04-proofs/04.02-flink-exactly-once-correctness.md": [
            ("#def-s-18-03-两阶段提交协议-2pc---two-phase-commit", "#def-s-18-03-两阶段提交协议-2pc--two-phase-commit"),
            ("#8-实例与反例-examples--counter-examples", "#8-实例与反例"),
        ],
        "Struct/04-proofs/04.03-chandy-lamport-consistency.md": [
            ("#def-s-19-02-一致割集--consistent-cut", "#def-s-19-02-一致割集--consistent-cut"),
            ("#lemma-s-19-02-一致割集引理--consistent-cut-lemma", "#lemma-s-19-02-一致割集引理--consistent-cut-lemma"),
            ("#关系-1-marker-接收--状态记录触发-关系-1-marker-接收--状态记录触发", "#关系-1-marker-接收--状态记录触发"),
            ("#关系-2-通道记录规则--无消息丢失或重复-关系-2-通道记录规则--无消息丢失或重复", "#关系-2-通道记录规则--无消息丢失或重复"),
            ("#关系-3-chandy-lamport--flink-checkpoint-语义等价-关系-3-chandy-lamport--flink-checkpoint-语义等价", "#关系-3-chandy-lamport--flink-checkpoint-语义等价"),
            ("#示例-62-环形拓扑中的-marker-传播", "#示例-62"),
        ],
        "Struct/04-proofs/04.04-watermark-algebra-formal-proof.md": [
            ("#watermark-代数形式证明-watermark-algebra-formal-proof", "#watermark-代数形式证明"),
            ("#def-s-20-02-watermark-合并算子-", "#def-s-20-02-watermark-合并算子"),
            ("#def-s-20-03-watermark-偏序关系-", "#def-s-20-03-watermark-偏序关系"),
            ("#lemma-s-20-02-交换律", "#lemma-s-20-02-交换律"),
            ("#lemma-s-20-03-幂等律", "#lemma-s-20-03-幂等律"),
        ],
        "Struct/04-proofs/04.07-deadlock-freedom-choreographic.md": [
            ("#def-s-23-02-global-types-全局类型", "#def-s-23-02-global-types-全局类型"),
            ("#lemma-s-23-01-epp-保持通信结构", "#lemma-s-23-01-epp-保持通信结构"),
            ("#prop-s-23-01-choreography-的合流性", "#prop-s-23-01-choreography-的合流性"),
        ],
        "Struct/06-frontier/06.02-choreographic-streaming-programming.md": [
            ("#choreographic-流编程前沿-choreographic-streaming-programming-frontier", "#choreographic-流编程前沿"),
            ("#关系-2-mpst--session-types-关系-2-mpst--session-types", "#关系-2-mpst--session-types"),
            ("#关系-3-全局类型-死锁自由", "#关系-3-全局类型--死锁自由"),
        ],
        "Struct/06-frontier/06.03-ai-agent-session-types.md": [
            ("#ai-agent-与会话类型-ai-agent-and-session-types", "#ai-agent-与会话类型"),
            ("#关系-3-type-safe-agent-communication--deadlock-freedom-关系-3-type-safe-agent-communication--deadlock-freedom", "#关系-3-type-safe-agent-communication--deadlock-freedom"),
        ],
        "Struct/06-frontier/06.04-pdot-path-dependent-types.md": [
            ("#pdot-完全路径依赖类型dot演算扩展", "#pdot-完全路径依赖类型"),
            ("#41-pdot-引入的动机分析", "#41-pdot-引入的动机"),
            ("#5-形式证明--工程论证-proof--engineering-argument", "#5-形式证明--工程论证"),
            ("#示例-63-dataflow-算子链的类型追踪", "#示例-63"),
        ],
        "Knowledge/01-concept-atlas/streaming-models-mindmap.md": [
            ("#关系-1-dataflow-actor图灵完备等价", "#关系-1-dataflow-actor-图灵完备等价"),
            ("#关系-2-dataflow-csp异步-vs-同步的连续统", "#关系-2-dataflow-csp-异步-vs-同步的连续统"),
            ("#关系-3-pubsub-actor解耦是地址匿名化的特例", "#关系-3-pubsub-actor-解耦是地址匿名化的特例"),
            ("#关系-4-cep-dataflow模式匹配是有状态算子的语法糖", "#关系-4-cep-dataflow-模式匹配是有状态算子的语法糖"),
        ],
        "Knowledge/02-design-patterns/pattern-log-analysis.md": [
            ("#设计模式-实时日志分析-pattern-real-time-log-analysis", "#设计模式-实时日志分析"),
        ],
        "Knowledge/02-design-patterns/pattern-windowed-aggregation.md": [
            ("#设计模式-窗口聚合-pattern-windowed-aggregation", "#设计模式-窗口聚合"),
        ],
        "Knowledge/06-frontier/streaming-access-control.md": [
            ("#def-k-06-18-数据血缘与策略传播-data-lineage--policy-propagation-def-k-06-18-数据血缘与策略传播-data-lineage--policy-propagation", "#def-k-06-18-数据血缘与策略传播-data-lineage--policy-propagation"),
        ],
    }
    
    total_fixed = 0
    
    for file_path, replacements in fixes.items():
        path = Path(file_path)
        if not path.exists():
            print(f"❌ 文件不存在: {file_path}")
            continue
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        for old, new in replacements:
            content = content.replace(old, new)
        
        if content != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed = len(replacements)
            total_fixed += fixed
            print(f"✅ {file_path}: 修复 {fixed} 个问题")
    
    return total_fixed


def main():
    print("🔧 修复剩余锚点问题...")
    print("=" * 70)
    
    total = fix_struct_files()
    
    print("=" * 70)
    print(f"✅ 修复完成！共修复 {total} 个问题")


if __name__ == '__main__':
    main()
