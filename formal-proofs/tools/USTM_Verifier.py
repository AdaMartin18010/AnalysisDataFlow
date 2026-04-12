#!/usr/bin/env python3
"""
USTM模型检查器原型
形式化等级: L5 (工具实现)
对应文档: Struct/01-foundation/01.01-unified-streaming-theory.md

功能:
1. 解析流处理拓扑描述
2. 转换为USTM模型
3. 执行基本正确性检查
4. 生成TLA+规格
"""

import json
import sys
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class ProcessorType(Enum):
    """处理器类型"""
    SOURCE = "source"
    MAP = "map"
    FILTER = "filter"
    KEYED_PROCESS = "keyed_process"
    WINDOW = "window"
    SINK = "sink"


@dataclass
class Processor:
    """处理器定义"""
    id: str
    type: ProcessorType
    parallelism: int = 1
    stateful: bool = False
    inputs: List[str] = None
    outputs: List[str] = None
    
    def __post_init__(self):
        if self.inputs is None:
            self.inputs = []
        if self.outputs is None:
            self.outputs = []


@dataclass
class Channel:
    """通道定义"""
    id: str
    source: str
    destination: str
    buffer_size: int = 1000


@dataclass
class USTMModel:
    """USTM系统模型"""
    name: str
    processors: List[Processor]
    channels: List[Channel]
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "processors": [
                {
                    "id": p.id,
                    "type": p.type.value,
                    "parallelism": p.parallelism,
                    "stateful": p.stateful,
                    "inputs": p.inputs,
                    "outputs": p.outputs
                }
                for p in self.processors
            ],
            "channels": [
                {
                    "id": c.id,
                    "source": c.source,
                    "destination": c.destination,
                    "buffer_size": c.buffer_size
                }
                for c in self.channels
            ]
        }


class USTMVerifier:
    """USTM模型检查器"""
    
    def __init__(self, model: USTMModel):
        self.model = model
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def verify_topology(self) -> bool:
        """验证拓扑结构"""
        valid = True
        
        # 检查1: 所有通道引用的处理器存在
        processor_ids = {p.id for p in self.model.processors}
        for ch in self.model.channels:
            if ch.source not in processor_ids:
                self.errors.append(f"通道 {ch.id}: 源处理器 {ch.source} 不存在")
                valid = False
            if ch.destination not in processor_ids:
                self.errors.append(f"通道 {ch.id}: 目标处理器 {ch.destination} 不存在")
                valid = False
        
        # 检查2: 无环性 (简化DFS)
        if not self._check_acyclic():
            self.errors.append("拓扑中存在环，可能导致死锁")
            valid = False
        
        # 检查3: Source和Sink存在
        sources = [p for p in self.model.processors if p.type == ProcessorType.SOURCE]
        sinks = [p for p in self.model.processors if p.type == ProcessorType.SINK]
        
        if not sources:
            self.errors.append("缺少Source处理器")
            valid = False
        if not sinks:
            self.errors.append("缺少Sink处理器")
            valid = False
        
        # 警告1: 孤立处理器
        connected = set()
        for ch in self.model.channels:
            connected.add(ch.source)
            connected.add(ch.destination)
        
        for p in self.model.processors:
            if p.id not in connected and p.type not in [ProcessorType.SOURCE, ProcessorType.SINK]:
                self.warnings.append(f"处理器 {p.id} 未连接")
        
        return valid
    
    def _check_acyclic(self) -> bool:
        """检查无环性 (简化实现)"""
        # 构建邻接表
        graph: Dict[str, List[str]] = {p.id: [] for p in self.model.processors}
        for ch in self.model.channels:
            graph[ch.source].append(ch.destination)
        
        # DFS检测环
        visited = set()
        rec_stack = set()
        
        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in graph:
            if node not in visited:
                if dfs(node):
                    return False
        
        return True
    
    def verify_consistency(self) -> bool:
        """验证一致性属性"""
        valid = True
        
        # 检查: 状态处理器必须有状态后端
        for p in self.model.processors:
            if p.stateful and p.type not in [ProcessorType.KEYED_PROCESS, ProcessorType.WINDOW]:
                self.warnings.append(f"处理器 {p.id} 标记为有状态但类型为 {p.type.value}")
        
        # 检查: 并行度合理性
        for p in self.model.processors:
            if p.parallelism < 1:
                self.errors.append(f"处理器 {p.id}: 并行度必须 >= 1")
                valid = False
            if p.parallelism > 1000:
                self.warnings.append(f"处理器 {p.id}: 并行度 {p.parallelism} 过大")
        
        return valid
    
    def generate_tla_spec(self) -> str:
        """生成TLA+规格"""
        tla = f"""-------------------------------- MODULE {self.model.name} --------------------------------
(* Auto-generated TLA+ specification from USTM model *)

EXTENDS Integers, Sequences, FiniteSets

CONSTANTS
    {", ".join([f"{p.id.upper()}_PAR" for p in self.model.processors])}

(* Processor definitions *)
Processors == {{
    {", ".join([f'"{p.id}"' for p in self.model.processors])}
}}

(* Type definitions *)
ProcessorState == [status: {{"idle", "running", "failed"}}, data: STRING]

VARIABLES
    processor_states,
    channel_buffers

(* Initial state *)
Init ==
    /\\ processor_states = [p \\in Processors |-> [status |-> "idle", data |-> ""]]
    /\\ channel_buffers = {{}}

(* Next state relation *)
Process(p) ==
    /\\ processor_states[p].status = "idle"
    /\\ processor_states' = [processor_states EXCEPT ![p].status = "running"]
    /\\ UNCHANGED channel_buffers

Next ==
    \\E p \\in Processors : Process(p)

Spec == Init /\\ [][Next]_<<processor_states, channel_buffers>>

================================================================================
"""
        return tla
    
    def generate_report(self) -> dict:
        """生成验证报告"""
        topology_valid = self.verify_topology()
        consistency_valid = self.verify_consistency()
        
        return {
            "model_name": self.model.name,
            "verification_status": "PASSED" if (topology_valid and consistency_valid) else "FAILED",
            "topology_valid": topology_valid,
            "consistency_valid": consistency_valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "statistics": {
                "num_processors": len(self.model.processors),
                "num_channels": len(self.model.channels),
                "num_sources": len([p for p in self.model.processors if p.type == ProcessorType.SOURCE]),
                "num_sinks": len([p for p in self.model.processors if p.type == ProcessorType.SINK])
            }
        }


def example_usage():
    """使用示例"""
    # 创建示例Flink拓扑
    model = USTMModel(
        name="SimpleETL",
        processors=[
            Processor("source_1", ProcessorType.SOURCE, outputs=["ch1"]),
            Processor("map_1", ProcessorType.MAP, inputs=["ch1"], outputs=["ch2"]),
            Processor("filter_1", ProcessorType.FILTER, inputs=["ch2"], outputs=["ch3"]),
            Processor("sink_1", ProcessorType.SINK, inputs=["ch3"])
        ],
        channels=[
            Channel("ch1", "source_1", "map_1"),
            Channel("ch2", "map_1", "filter_1"),
            Channel("ch3", "filter_1", "sink_1")
        ]
    )
    
    # 创建验证器并运行
    verifier = USTMVerifier(model)
    report = verifier.generate_report()
    
    # 输出报告
    print(json.dumps(report, indent=2))
    
    # 生成TLA+规格
    tla_spec = verifier.generate_tla_spec()
    print("\n--- Generated TLA+ Spec ---")
    print(tla_spec)


if __name__ == "__main__":
    example_usage()
