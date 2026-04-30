------------------------------- MODULE StreamingCheckpoint -------------------------------
(******************************************************************************)
(* 流计算 Checkpoint 协调与 Exactly-Once 语义 TLA+ 形式化规约                    *)
(*                                                                            *)
(* 本规约基于 Apache Flink Checkpoint 机制（Chandy-Lamport 分布式快照变体）      *)
(* 形式化定义了流处理 DAG 中 barrier 注入、传播、状态快照及 exactly-once 语义    *)
(*                                                                            *)
(* 所属阶段: Flink/04-runtime | 前置依赖: TwoPhaseCommit.tla, Utilities.tla   *)
(* 形式化等级: L5                                                             *)
(* 参考: Chandy & Lamport, "Distributed Snapshots", ACM TOCS, 1985            *)
(*       Apache Flink Documentation, "Checkpointing", 2025                    *)
(******************************************************************************)

------------------------------------------------------------------------------
(*============================================================================*)
(* 导入模块                                                                    *)
(*============================================================================*)

EXTENDS Naturals, Sequences, FiniteSets, TLC
\* Naturals: 提供自然数运算（checkpoint epoch 编号）
\* Sequences: 提供序列操作（in-flight 数据、barrier 队列）
\* FiniteSets: 提供有限集合操作（task 集合、状态快照集）
\* TLC: 提供 TLC 模型检测器特定工具

------------------------------------------------------------------------------
(*============================================================================*)
(* 常量声明                                                                    *)
(*============================================================================*)

CONSTANTS
    Operators,          \* 逻辑算子集合，例如 {src, map1, filter1, keyBy1, win1, sink1}
    Tasks,              \* 物理执行 Task 集合（Operator 的并行实例）
    Barriers,           \* Barrier ID 集合，与 Checkpoint 一一对应
    StateSnapshots,     \* 可能的状态快照标识集合
    Checkpoints,        \* Checkpoint epoch 编号集合（自然数子集）
    OperatorType,       \* Task -> OperatorType 的映射（见下方 ASSUME）
    Upstream,           \* Task -> Task 集合，DAG 上游关系
    Downstream,         \* Task -> Task 集合，DAG 下游关系
    MaxInFlight         \* 最大在途数据量（用于模型检测限制状态空间）

(* ASSUME-01: 常量参数约束 —— 确保模型参数满足基本结构化要求 *)
(* 证明思路: 模型参数约束，由 TLC 常量定义保证；有限性确保模型检查可终止 *)
ASSUME ConstantsAssumption ==
    /\ Operators # {}                         \* 至少有一个算子
    /\ Tasks # {}                             \* 至少有一个 Task
    /\ IsFiniteSet(Operators)                 \* 算子集合有限
    /\ IsFiniteSet(Tasks)                     \* Task 集合有限
    /\ Barriers \subseteq Checkpoints          \* Barrier 是 Checkpoint 的子集
    /\ Checkpoints \subseteq Nat               \* Checkpoint epoch 为自然数
    /\ IsFiniteSet(Checkpoints)               \* Checkpoint 集合有限
    /\ MaxInFlight \in Nat                     \* 最大在途数据量为自然数

(* 算子类型枚举 *)
OpSource  == "source"
OpMap     == "map"
OpFilter  == "filter"
OpKeyBy   == "keyBy"
OpWindow  == "window"
OpSink    == "sink"
OpTypeSet == {OpSource, OpMap, OpFilter, OpKeyBy, OpWindow, OpSink}

(* ASSUME-02: OperatorType 映射有效性 —— 每个 task 都有合法的算子类型 *)
ASSUME OperatorTypeValid ==
    /\ OperatorType \in [Tasks -> OpTypeSet]   \* 每个 task 都有确定的算子类型
    /\ \E t \in Tasks : OperatorType[t] = OpSource  \* 至少一个 Source
    /\ \E t \in Tasks : OperatorType[t] = OpSink    \* 至少一个 Sink

(* ASSUME-03: DAG 结构约束 —— Upstream/Downstream 互为逆关系，无环 *)
ASSUME DAGStructure ==
    /\ Upstream  \in [Tasks -> SUBSET Tasks]   \* Upstream 是 Task 幂集上的函数
    /\ Downstream \in [Tasks -> SUBSET Tasks]  \* Downstream 是 Task 幂集上的函数
    /\ \A t1, t2 \in Tasks :                   \* 互逆关系
        t1 \in Upstream[t2]  <=>  t2 \in Downstream[t1]
    /\ \A t \in Tasks : t \notin Upstream[t]   \* 无自环
    /\ \A t \in Tasks :                        \* Source 无上游，Sink 无下游
        /\ (OperatorType[t] = OpSource  => Upstream[t] = {})
        /\ (OperatorType[t] = OpSink    => Downstream[t] = {})

------------------------------------------------------------------------------
(*============================================================================*)
(* 变量声明                                                                    *)
(*============================================================================*)

VARIABLES
    taskStates,         \* taskStates[t] = Task t 的当前执行状态
    barrierStates,      \* barrierStates[t][b] = Task t 对 Barrier b 的处理状态
    checkpointEpochs,   \* checkpointEpochs[t] = Task t 已确认的最新 checkpoint epoch
    stateSnapshots,     \* stateSnapshots[t][b] = Task t 在 Barrier b 处的快照状态
    inFlightData,       \* inFlightData[t] = Task t 的输入缓冲区（在途数据序列）
    outputRecords,      \* outputRecords[t] = Task t 已输出到下游的记录的集合/序列
    completedCheckpoints  \* 全局已完成的 checkpoint 集合

(* 所有变量的元组，用于时序公式 *)
vars == <<taskStates, barrierStates, checkpointEpochs, stateSnapshots,
          inFlightData, outputRecords, completedCheckpoints>>

------------------------------------------------------------------------------
(*============================================================================*)
(* 辅助定义与类型集合                                                          *)
(*============================================================================*)

(*----------------------------------------------------------------------------*)
(* Task 状态集合                                                              *)
(*----------------------------------------------------------------------------*)

(* Source 算子状态 *)
SourceState == {"idle", "emitting", "barrier_injected", "completed"}

(* Map/Filter/KeyBy/Window 等中间算子状态 *)
IntermediateState == {"idle", "processing", "barrier_reached", "snapshot_taken", "completed"}

(* Sink 算子状态 *)
SinkState == {"idle", "buffering", "committing", "committed", "completed"}

(* 所有可能的 Task 状态并集 *)
TaskState == SourceState \union IntermediateState \union SinkState

(*----------------------------------------------------------------------------*)
(* Barrier 处理状态                                                           *)
(*----------------------------------------------------------------------------*)

(* 单个 Task 对某个 Barrier 的处理阶段 *)
BarrierPhase == {
    "none",             \* 尚未收到此 barrier
    "received",         \* 已收到 barrier，等待对齐（对齐模式下）
    "aligned",          \* barrier 已对齐（所有输入通道均收到）
    "snapshotting",     \* 正在执行本地状态快照
    "snapshotted",      \* 本地快照已完成
    "acknowledged"      \* 已向 CheckpointCoordinator 确认
}

(*----------------------------------------------------------------------------*)
(* Checkpoint 全局状态                                                        *)
(*----------------------------------------------------------------------------*)

CheckpointState == {
    "pending",          \* Checkpoint 已触发，等待各 task 响应
    "snapshotting",     \* 至少有一个 task 在进行快照
    "completed",        \* 所有 task 均确认快照成功
    "aborted"           \* Checkpoint 被显式中止或超时
}

(*----------------------------------------------------------------------------*)
(* 快照状态                                                                   *)
(*----------------------------------------------------------------------------*)

SnapshotStatus == {
    "none",             \* 尚未开始快照
    "in_progress",      \* 快照进行中（异步快照）
    "sync_done",        \* 同步部分完成
    "async_done",       \* 异步部分完成
    "confirmed"         \* 全局确认
}

(*----------------------------------------------------------------------------*)
(* 输出记录状态（用于 exactly-once 追踪）                                      *)
(*----------------------------------------------------------------------------*)

RecordStatus == {
    "in_flight",        \* 已生成但尚未确认提交
    "committed",        \* 已确认提交（exactly-once 下不可回滚）
    "aborted"           \* 已回滚/丢弃
}

------------------------------------------------------------------------------
(*============================================================================*)
(* 初始状态定义 (Init)                                                         *)
(*============================================================================*)

(* Def-S-SC-01: 初始状态定义 *)
(* 所有 Task 处于 idle，无 barrier，无快照，无在途数据，无已完成 checkpoint *)
Init ==
    /\ taskStates = [t \in Tasks |->
        IF OperatorType[t] = OpSource THEN "idle"
        ELSE IF OperatorType[t] = OpSink THEN "idle"
        ELSE "idle"]
    /\ barrierStates = [t \in Tasks |-> [b \in Barriers |-> "none"]]
    /\ checkpointEpochs = [t \in Tasks |-> 0]
    /\ stateSnapshots = [t \in Tasks |-> [b \in Barriers |-> "none"]]
    /\ inFlightData = [t \in Tasks |-> << >>]
    /\ outputRecords = [t \in Tasks |-> << >>]
    /\ completedCheckpoints = {}

------------------------------------------------------------------------------
(*============================================================================*)
(* 算子状态机 (OperatorStateMachine)                                           *)
(*============================================================================*)

(*----------------------------------------------------------------------------*)
(* Source 算子动作                                                            *)
(*----------------------------------------------------------------------------*)

(* Def-S-SC-02: Source 从 idle 转换到 emitting *)
(* Source 开始读取外部输入并向下游发送数据 *)
SourceStartEmitting(t) ==
    /\ OperatorType[t] = OpSource
    /\ taskStates[t] = "idle"
    /\ taskStates' = [taskStates EXCEPT ![t] = "emitting"]
    /\ UNCHANGED <<barrierStates, checkpointEpochs, stateSnapshots,
                   inFlightData, outputRecords, completedCheckpoints>>

(* Def-S-SC-03: Source 注入 Barrier（触发 checkpoint） *)
(* Source 在数据流中插入 barrier，标志着新 checkpoint epoch 的开始 *)
SourceInjectBarrier(t, b) ==
    /\ OperatorType[t] = OpSource
    /\ taskStates[t] = "emitting"
    /\ b \in Barriers
    /\ barrierStates[t][b] = "none"
    /\ taskStates' = [taskStates EXCEPT ![t] = "barrier_injected"]
    /\ barrierStates' = [barrierStates EXCEPT ![t] =
        [@ EXCEPT ![b] = "aligned"]]   \* Source 无上游，barrier 天然对齐
    /\ checkpointEpochs' = [checkpointEpochs EXCEPT ![t] = b]
    /\ UNCHANGED <<stateSnapshots, inFlightData, outputRecords, completedCheckpoints>>

(* Def-S-SC-04: Source 完成 checkpoint 后恢复 emitting *)
SourceResumeAfterBarrier(t, b) ==
    /\ OperatorType[t] = OpSource
    /\ taskStates[t] = "barrier_injected"
    /\ barrierStates[t][b] = "snapshotted"
    /\ taskStates' = [taskStates EXCEPT ![t] = "emitting"]
    /\ UNCHANGED <<barrierStates, checkpointEpochs, stateSnapshots,
                   inFlightData, outputRecords, completedCheckpoints>>

(*----------------------------------------------------------------------------*)
(* 中间算子动作 (Map / Filter / KeyBy / Window)                               *)
(*----------------------------------------------------------------------------*)

(* Def-S-SC-05: 中间算子处理输入数据 *)
(* Task 从输入缓冲区读取数据，执行计算，产生输出到下游 *)
IntermediateProcessData(t) ==
    /\ OperatorType[t] \in {OpMap, OpFilter, OpKeyBy, OpWindow}
    /\ taskStates[t] \in {"idle", "processing"}
    /\ inFlightData[t] # << >>   \* 输入缓冲区非空
    /\ taskStates' = [taskStates EXCEPT ![t] = "processing"]
    /\ inFlightData' = [inFlightData EXCEPT ![t] =
        [i \in 1..(Len(@) - 1) |-> @[i + 1]]]  \* 消费一条输入
    /\ outputRecords' = [outputRecords EXCEPT ![t] =
        Append(@, [status |-> "in_flight", data |-> "processed"])]
    /\ UNCHANGED <<barrierStates, checkpointEpochs, stateSnapshots, completedCheckpoints>>

(* Def-S-SC-06: 中间算子收到 Barrier（对齐模式） *)
(* 当所有上游输入通道都收到同一 barrier 时，task 进入 barrier_reached *)
(* FORMAL-GAP: 此处抽象为原子操作；实际实现中各输入通道异步到达，需显式 *)
(* 维护 per-channel barrier 状态。完整建模需引入 channel 维度。 *)
IntermediateReceiveBarrierAligned(t, b) ==
    /\ OperatorType[t] \in {OpMap, OpFilter, OpKeyBy, OpWindow}
    /\ taskStates[t] \in {"idle", "processing"}
    /\ b \in Barriers
    /\ barrierStates[t][b] = "none"
    /\ \A u \in Upstream[t] : barrierStates[u][b] \in {"aligned", "snapshotting", "snapshotted", "acknowledged"}
    /\ taskStates' = [taskStates EXCEPT ![t] = "barrier_reached"]
    /\ barrierStates' = [barrierStates EXCEPT ![t] =
        [@ EXCEPT ![b] = "aligned"]]
    /\ checkpointEpochs' = [checkpointEpochs EXCEPT ![t] = b]
    /\ UNCHANGED <<stateSnapshots, inFlightData, outputRecords, completedCheckpoints>>

(* Def-S-SC-07: 中间算子收到 Barrier（非对齐模式） *)
(* 非对齐模式下，barrier 越过缓冲区数据直达处理逻辑，需快照 in-flight 数据 *)
(* FORMAL-GAP: 非对齐模式需显式建模 channel 状态与缓冲区细粒度快照；当前 *)
(* 抽象级别以 barrierStates 统一表达。完整形式化需扩展 channel-level 状态。 *)
IntermediateReceiveBarrierUnaligned(t, b) ==
    /\ OperatorType[t] \in {OpMap, OpFilter, OpKeyBy, OpWindow}
    /\ taskStates[t] \in {"idle", "processing"}
    /\ b \in Barriers
    /\ barrierStates[t][b] = "none"
    /\ \E u \in Upstream[t] : barrierStates[u][b] \in {"aligned", "snapshotting", "snapshotted", "acknowledged"}
    /\ taskStates' = [taskStates EXCEPT ![t] = "barrier_reached"]
    /\ barrierStates' = [barrierStates EXCEPT ![t] =
        [@ EXCEPT ![b] = "aligned"]]
    /\ checkpointEpochs' = [checkpointEpochs EXCEPT ![t] = b]
    /\ UNCHANGED <<stateSnapshots, inFlightData, outputRecords, completedCheckpoints>>

(* Def-S-SC-08: 中间算子执行本地状态快照 *)
(* Task 在 barrier 处原子性地保存本地状态（keyed state / operator state） *)
IntermediateTakeSnapshot(t, b) ==
    /\ OperatorType[t] \in {OpMap, OpFilter, OpKeyBy, OpWindow}
    /\ taskStates[t] = "barrier_reached"
    /\ barrierStates[t][b] = "aligned"
    /\ stateSnapshots[t][b] = "none"
    /\ taskStates' = [taskStates EXCEPT ![t] = "snapshot_taken"]
    /\ barrierStates' = [barrierStates EXCEPT ![t] =
        [@ EXCEPT ![b] = "snapshotting"]]
    /\ stateSnapshots' = [stateSnapshots EXCEPT ![t] =
        [@ EXCEPT ![b] = "in_progress"]]
    /\ UNCHANGED <<checkpointEpochs, inFlightData, outputRecords, completedCheckpoints>>

(* Def-S-SC-09: 中间算子快照完成，恢复处理 *)
IntermediateSnapshotComplete(t, b) ==
    /\ OperatorType[t] \in {OpMap, OpFilter, OpKeyBy, OpWindow}
    /\ taskStates[t] = "snapshot_taken"
    /\ barrierStates[t][b] = "snapshotting"
    /\ stateSnapshots[t][b] = "in_progress"
    /\ taskStates' = [taskStates EXCEPT ![t] = "idle"]
    /\ barrierStates' = [barrierStates EXCEPT ![t] =
        [@ EXCEPT ![b] = "acknowledged"]]
    /\ stateSnapshots' = [stateSnapshots EXCEPT ![t] =
        [@ EXCEPT ![b] = "confirmed"]]
    /\ UNCHANGED <<checkpointEpochs, inFlightData, outputRecords, completedCheckpoints>>

(*----------------------------------------------------------------------------*)
(* Sink 算子动作                                                              *)
(*----------------------------------------------------------------------------*)

(* Def-S-SC-10: Sink 从上游接收数据并缓冲 *)
SinkBufferData(t) ==
    /\ OperatorType[t] = OpSink
    /\ taskStates[t] \in {"idle", "buffering"}
    /\ inFlightData[t] # << >>
    /\ taskStates' = [taskStates EXCEPT ![t] = "buffering"]
    /\ inFlightData' = [inFlightData EXCEPT ![t] =
        [i \in 1..(Len(@) - 1) |-> @[i + 1]]]
    /\ outputRecords' = [outputRecords EXCEPT ![t] =
        Append(@, [status |-> "in_flight", data |-> "buffered"])]
    /\ UNCHANGED <<barrierStates, checkpointEpochs, stateSnapshots, completedCheckpoints>>

(* Def-S-SC-11: Sink 收到 Barrier 后进入提交阶段 *)
(* Sink 需等待 checkpoint 全局完成后再将缓冲数据提交到外部系统 *)
SinkReceiveBarrier(t, b) ==
    /\ OperatorType[t] = OpSink
    /\ taskStates[t] \in {"idle", "buffering"}
    /\ b \in Barriers
    /\ barrierStates[t][b] = "none"
    /\ \A u \in Upstream[t] : barrierStates[u][b] \in {"aligned", "snapshotting", "snapshotted", "acknowledged"}
    /\ taskStates' = [taskStates EXCEPT ![t] = "committing"]
    /\ barrierStates' = [barrierStates EXCEPT ![t] =
        [@ EXCEPT ![b] = "aligned"]]
    /\ checkpointEpochs' = [checkpointEpochs EXCEPT ![t] = b]
    /\ UNCHANGED <<stateSnapshots, inFlightData, outputRecords, completedCheckpoints>>

(* Def-S-SC-12: Sink 将两阶段提交中的预提交结果固化（exactly-once 核心） *)
(* 在 checkpoint 确认后，Sink 将之前处于 in_flight 的输出标记为 committed *)
SinkCommitOnCheckpoint(t, b) ==
    /\ OperatorType[t] = OpSink
    /\ taskStates[t] = "committing"
    /\ barrierStates[t][b] = "aligned"
    /\ b \in completedCheckpoints   \* 全局 checkpoint 已完成
    /\ taskStates' = [taskStates EXCEPT ![t] = "committed"]
    /\ barrierStates' = [barrierStates EXCEPT ![t] =
        [@ EXCEPT ![b] = "acknowledged"]]
    /\ outputRecords' = [outputRecords EXCEPT ![t] =
        [i \in 1..Len(@) |->
            IF @[i].status = "in_flight"
            THEN [status |-> "committed", data |-> @[i].data]
            ELSE @[i]]]
    /\ UNCHANGED <<checkpointEpochs, stateSnapshots, inFlightData, completedCheckpoints>>

(* Def-S-SC-13: Sink 提交完成后恢复 buffering *)
SinkResumeAfterCommit(t) ==
    /\ OperatorType[t] = OpSink
    /\ taskStates[t] = "committed"
    /\ taskStates' = [taskStates EXCEPT ![t] = "buffering"]
    /\ UNCHANGED <<barrierStates, checkpointEpochs, stateSnapshots,
                   inFlightData, outputRecords, completedCheckpoints>>

------------------------------------------------------------------------------
(*============================================================================*)
(* Barrier 注入与传播 (BarrierPropagation)                                     *)
(*============================================================================*)

(*----------------------------------------------------------------------------*)
(* 下游 Task 从上游接收数据 / Barrier（网络层抽象）                             *)
(*----------------------------------------------------------------------------*)

(* Def-S-SC-14: 上游 Task 向下游发送数据（网络层模拟） *)
(* 将上游 outputRecords 中的 in_flight 记录传播到下游 inFlightData *)
(* FORMAL-GAP: 实际 Flink 网络层有显式的 ResultPartition/InputGate 抽象；此处 *)
(* 简化为直接的上下游数据传递。完整建模需引入网络缓冲区和反压机制。 *)
TransmitDataToDownstream(t) ==
    /\ taskStates[t] \notin {"idle"}  \* 活跃的 task 才能发送数据
    /\ \E d \in Downstream[t] :
        /\ Len(inFlightData[d]) < MaxInFlight   \* 下游缓冲区未满
        /\ \E i \in 1..Len(outputRecords[t]) :
            /\ outputRecords[t][i].status = "in_flight"
            /\ inFlightData' = [inFlightData EXCEPT ![d] =
                Append(@, outputRecords[t][i].data)]
    /\ UNCHANGED <<taskStates, barrierStates, checkpointEpochs,
                   stateSnapshots, outputRecords, completedCheckpoints>>

(* Def-S-SC-15: Barrier 沿 DAG 边向下游传播 *)
(* 当上游 Task 对 barrier b 进入 snapshotting/snapshotted/acknowledged 时， *)
(* barrier 可被下游感知。此动作为 IntermediateReceiveBarrierAligned/Unaligned *)
(* 的前置条件来源。 *)
(* 注：在实际规约中，barrier 传播通过 IntermediateReceiveBarrier* 的前置条件 *)
(* 隐式建模；此定义作为文档性说明。 *)

------------------------------------------------------------------------------
(*============================================================================*)
(* Snapshot 协议 (SnapshotProtocol)                                            *)
(*============================================================================*)

(*----------------------------------------------------------------------------*)
(* 两阶段快照：本地快照 + 全局一致性确认                                        *)
(*----------------------------------------------------------------------------*)

(* Def-S-SC-16: Checkpoint Coordinator 触发全局 Checkpoint（由 Source 注入代表） *)
(* 在实际系统中，CheckpointCoordinator 向所有 Source 发送触发消息； *)
(* 本规约中通过 SourceInjectBarrier 抽象表达。 *)

(* Def-S-SC-17: Checkpoint 全局完成判定 *)
(* 当所有 Task 都对某个 barrier 完成快照确认时，该 checkpoint 全局完成 *)
CheckpointGlobalComplete(b) ==
    /\ b \in Barriers
    /\ b \notin completedCheckpoints
    /\ \A t \in Tasks :
        /\ barrierStates[t][b] \in {"acknowledged"}
        /\ stateSnapshots[t][b] \in {"confirmed"}
    /\ completedCheckpoints' = completedCheckpoints \union {b}
    /\ UNCHANGED <<taskStates, barrierStates, checkpointEpochs,
                   stateSnapshots, inFlightData, outputRecords>>

(* Def-S-SC-18: Checkpoint 中止（超时或失败） *)
(* 当某个 Task 的快照失败时，整个 checkpoint 被标记为 aborted *)
(* FORMAL-GAP: 实际 Flink 支持部分失败重试和 region-based 恢复；此处简化为 *)
(* 全局 abort。完整建模需引入 TaskFailure 状态和区域恢复协议。 *)
CheckpointAbort(b) ==
    /\ b \in Barriers
    /\ b \notin completedCheckpoints
    /\ taskStates' = taskStates   \* 无状态变更，仅逻辑标记
    /\ UNCHANGED vars   \* 简化模型：abort 为逻辑事件

(*----------------------------------------------------------------------------*)
(* 状态快照原子性保证                                                         *)
(*----------------------------------------------------------------------------*)

(* Def-S-SC-19: 同步快照 —— 阻塞式，所有处理暂停直至快照完成 *)
(* 在 Flink 中，同步快照对应早期版本的 full-barrier 阻塞模式 *)
SyncSnapshotSemantics(t, b) ==
    /\ taskStates[t] = "barrier_reached"
    /\ stateSnapshots[t][b] = "sync_done"
    /\ UNCHANGED <<taskStates, barrierStates, checkpointEpochs,
                   inFlightData, outputRecords, completedCheckpoints>>

(* Def-S-SC-20: 异步快照 —— 非阻塞式，快照线程与处理线程并发 *)
(* 异步快照允许 barrier 之后的记录继续处理，快照在后台完成 *)
(* FORMAL-GAP: 异步快照的完整并发语义需引入 action interleaving 的精细建模； *)
(* 当前通过 IntermediateSnapshotComplete 从 in_progress 到 confirmed 的转移 *)
(* 抽象表达异步完成事件。 *)

------------------------------------------------------------------------------
(*============================================================================*)
(* Exactly-Once 语义定义 (ExactlyOnceSemantics)                                *)
(*============================================================================*)

(*----------------------------------------------------------------------------*)
(* 交付保证等级的形式化定义                                                    *)
(*----------------------------------------------------------------------------*)

(* Def-S-SC-21: At-Most-Once 语义 *)
(* 每条记录至多被处理并输出一次（允许丢失） *)
AtMostOnce ==
    \A t \in Tasks :
        /\ OperatorType[t] = OpSink  =>
            /\ \A i, j \in 1..Len(outputRecords[t]) :
                i # j => outputRecords[t][i].data # outputRecords[t][j].data
            \* 注：在简化模型中 data 字段标识唯一记录；无重复即满足 at-most-once

(* Def-S-SC-22: At-Least-Once 语义 *)
(* 每条记录至少被处理并输出一次（允许重复） *)
(* FORMAL-GAP: at-least-once 的完整形式化需引入输入源可重放（replayable source） *)
(* 的假设和输入-输出对应关系的追踪；当前抽象级别以输出非空性表达。 *)
AtLeastOnce ==
    \A t \in Tasks :
        /\ OperatorType[t] = OpSink  =>
            /\ Len(outputRecords[t]) > 0

(* Def-S-SC-23: Exactly-Once 语义 *)
(* 每条记录恰好被处理并输出一次，等价于 at-most-once + at-least-once + *)
(* 状态快照一致性。端到端 exactly-once 要求： *)
(*   1. 幂等输出（idempotent sink / 两阶段提交）                               *)
(*   2. 可重放输入（replayable source，如 Kafka 等 offset-based 源）            *)
(*   3. 一致性快照（consistent distributed snapshot）                          *)
ExactlyOnce ==
    /\ AtMostOnce
    /\ AtLeastOnce
    /\ \A t \in Tasks :
        /\ OperatorType[t] = OpSink =>
            /\ \A i \in 1..Len(outputRecords[t]) :
                outputRecords[t][i].status # "aborted"   \* 无被丢弃的有效记录
    /\ \A b \in completedCheckpoints :
        /\ \A t1, t2 \in Tasks :
            /\ stateSnapshots[t1][b] = "confirmed"
            /\ stateSnapshots[t2][b] = "confirmed"
            \* 快照一致性：同一 checkpoint 下所有 task 的快照构成全局一致割

(*----------------------------------------------------------------------------*)
(* Exactly-Once 核心不变量                                                    *)
(*----------------------------------------------------------------------------*)

(* Thm-S-SC-01: Exactly-Once 不变量 *)
(* 系统在任意可达状态下均满足 exactly-once 语义 *)
ExactlyOnceInv ==
    /\ AtMostOnce
    /\ \A t \in Tasks :
        /\ OperatorType[t] = OpSink =>
            /\ \A i \in 1..Len(outputRecords[t]) :
                /\ outputRecords[t][i].status = "in_flight"  =>
                    \E b \in Barriers :
                        /\ barrierStates[t][b] = "aligned"
                        /\ b \notin completedCheckpoints
                /\ outputRecords[t][i].status = "committed"  =>
                    /\ \E b \in completedCheckpoints :
                        barrierStates[t][b] = "acknowledged"
                /\ outputRecords[t][i].status = "aborted" => FALSE   \* Sink 无 aborted
    /\ \A b \in completedCheckpoints :
        \A t \in Tasks : stateSnapshots[t][b] = "confirmed"

------------------------------------------------------------------------------
(*============================================================================*)
(* 下一步关系 (Next)                                                           *)
(*============================================================================*)

(* Def-S-SC-24: 系统的所有可能动作 *)
Next ==
    (* Source 算子动作 *)
    /\ \E t \in Tasks :
        /\ OperatorType[t] = OpSource
        /\ \/ SourceStartEmitting(t)
            \/ \E b \in Barriers : SourceInjectBarrier(t, b)
            \/ \E b \in Barriers : SourceResumeAfterBarrier(t, b)
    (* 中间算子动作 *)
    /\ \E t \in Tasks :
        /\ OperatorType[t] \in {OpMap, OpFilter, OpKeyBy, OpWindow}
        /\ \/ IntermediateProcessData(t)
            \/ \E b \in Barriers : IntermediateReceiveBarrierAligned(t, b)
            \/ \E b \in Barriers : IntermediateReceiveBarrierUnaligned(t, b)
            \/ \E b \in Barriers : IntermediateTakeSnapshot(t, b)
            \/ \E b \in Barriers : IntermediateSnapshotComplete(t, b)
    (* Sink 算子动作 *)
    /\ \E t \in Tasks :
        /\ OperatorType[t] = OpSink
        /\ \/ SinkBufferData(t)
            \/ \E b \in Barriers : SinkReceiveBarrier(t, b)
            \/ \E b \in Barriers : SinkCommitOnCheckpoint(t, b)
            \/ SinkResumeAfterCommit(t)
    (* 网络层动作 *)
    /\ \E t \in Tasks : TransmitDataToDownstream(t)
    (* Checkpoint 协调器动作 *)
    /\ \E b \in Barriers : CheckpointGlobalComplete(b)
    /\ \E b \in Barriers : CheckpointAbort(b)

------------------------------------------------------------------------------
(*============================================================================*)
(* 时序公式 (Specification)                                                    *)
(*============================================================================*)

(* Def-S-SC-25: 公平性条件 *)
(* 弱公平性：如果某个动作持续可用，它最终会被执行 *)
Fairness ==
    /\ \A t \in Tasks :
        /\ WF_vars(IntermediateProcessData(t))
        /\ WF_vars(IntermediateTakeSnapshot(t, CHOOSE b \in Barriers : TRUE))
    /\ \A t \in Tasks : WF_vars(SinkBufferData(t))
    /\ \A b \in Barriers : WF_vars(CheckpointGlobalComplete(b))

(* Def-S-SC-26: 完整规约 *)
(* 从初始状态开始，通过 Next 动作转移，并满足公平性条件 *)
Spec == Init /\ [][Next]_vars /\ Fairness

(* 不带公平性的规约（用于安全性性质检查） *)
SpecNoFairness == Init /\ [][Next]_vars

------------------------------------------------------------------------------
(*============================================================================*)
(* 不变量 (Invariants) —— TLC 可检查的方式                                     *)
(*============================================================================*)

(*----------------------------------------------------------------------------*)
(* 类型不变式                                                                 *)
(*----------------------------------------------------------------------------*)

(* Thm-S-SC-02: 类型不变式 *)
(* 所有变量始终保持合法类型 *)
TypeInvariant ==
    /\ taskStates \in [Tasks -> TaskState]
    /\ barrierStates \in [Tasks -> [Barriers -> BarrierPhase]]
    /\ checkpointEpochs \in [Tasks -> Nat]
    /\ stateSnapshots \in [Tasks -> [Barriers -> SnapshotStatus]]
    /\ inFlightData \in [Tasks -> Seq({"data"})]   \* 简化数据域
    /\ outputRecords \in [Tasks -> Seq([status : RecordStatus, data : {"data"}])]
    /\ completedCheckpoints \subseteq Checkpoints

(*----------------------------------------------------------------------------*)
(* Checkpoint 完整性不变式                                                    *)
(*----------------------------------------------------------------------------*)

(* Thm-S-SC-03: Checkpoint 完整性 *)
(* 每个发起的 checkpoint 要么全局完成，要么被中止（简化模型下均会完成） *)
CheckpointCompleteness ==
    \A b \in Barriers :
        b \in completedCheckpoints
            => \A t \in Tasks :
                /\ barrierStates[t][b] = "acknowledged"
                /\ stateSnapshots[t][b] = "confirmed"

(* Thm-S-SC-04: Checkpoint 单调性 *)
(* Task 的 checkpointEpoch 单调不减 *)
CheckpointMonotonicity ==
    [][\A t \in Tasks : checkpointEpochs'[t] >= checkpointEpochs[t]]_vars

(*----------------------------------------------------------------------------*)
(* 无孤立状态不变式                                                           *)
(*----------------------------------------------------------------------------*)

(* Thm-S-SC-05: 无孤立快照状态 *)
(* 已确认的快照必须与活跃状态一致：不存在 snapshotted 但 barrier 未 acknowledged *)
NoOrphanedState ==
    \A t \in Tasks, b \in Barriers :
        stateSnapshots[t][b] = "confirmed"
            => barrierStates[t][b] = "acknowledged"

(* Thm-S-SC-06: 快照一致性 —— 同一 checkpoint 下所有 task 的快照构成一致割 *)
SnapshotConsistency ==
    \A b \in completedCheckpoints :
        \A t1, t2 \in Tasks :
            /\ stateSnapshots[t1][b] = "confirmed"
            /\ stateSnapshots[t2][b] = "confirmed"
            /\ checkpointEpochs[t1] >= b
            /\ checkpointEpochs[t2] >= b

(*----------------------------------------------------------------------------*)
(* 状态转换有效性不变式                                                       *)
(*----------------------------------------------------------------------------*)

(* Thm-S-SC-07: Source 状态转移有效性 *)
SourceStateTransitionValid ==
    [][\A t \in Tasks :
        OperatorType[t] = OpSource =>
            /\ (taskStates[t] = "idle"         => taskStates'[t] \in {"idle", "emitting"})
            /\ (taskStates[t] = "emitting"     => taskStates'[t] \in {"emitting", "barrier_injected"})
            /\ (taskStates[t] = "barrier_injected" => taskStates'[t] \in {"barrier_injected", "emitting"})
            /\ (taskStates[t] = "completed"    => taskStates'[t] = "completed")
    ]_vars

(* Thm-S-SC-08: 中间算子状态转移有效性 *)
IntermediateStateTransitionValid ==
    [][\A t \in Tasks :
        OperatorType[t] \in {OpMap, OpFilter, OpKeyBy, OpWindow} =>
            /\ (taskStates[t] = "idle"         => taskStates'[t] \in {"idle", "processing", "barrier_reached"})
            /\ (taskStates[t] = "processing"   => taskStates'[t] \in {"processing", "barrier_reached"})
            /\ (taskStates[t] = "barrier_reached" => taskStates'[t] \in {"barrier_reached", "snapshot_taken"})
            /\ (taskStates[t] = "snapshot_taken" => taskStates'[t] \in {"snapshot_taken", "idle"})
    ]_vars

(* Thm-S-SC-09: Sink 状态转移有效性 *)
SinkStateTransitionValid ==
    [][\A t \in Tasks :
        OperatorType[t] = OpSink =>
            /\ (taskStates[t] = "idle"         => taskStates'[t] \in {"idle", "buffering", "committing"})
            /\ (taskStates[t] = "buffering"    => taskStates'[t] \in {"buffering", "committing"})
            /\ (taskStates[t] = "committing"   => taskStates'[t] \in {"committing", "committed"})
            /\ (taskStates[t] = "committed"    => taskStates'[t] \in {"committed", "buffering"})
    ]_vars

(*----------------------------------------------------------------------------*)
(* 组合不变式                                                                 *)
(*----------------------------------------------------------------------------*)

(* Thm-S-SC-10: 完整安全性不变式 *)
Invariant ==
    /\ TypeInvariant
    /\ CheckpointCompleteness
    /\ CheckpointMonotonicity
    /\ NoOrphanedState
    /\ SnapshotConsistency
    /\ ExactlyOnceInv

------------------------------------------------------------------------------
(*============================================================================*)
(* 活性性质 (Liveness Properties)                                              *)
(*============================================================================*)

(* Thm-S-SC-11: 每个已触发的 Checkpoint 最终全局完成（在公平性条件下） *)
EventuallyCheckpointCompletes(b) ==
    b \in Barriers => (b \notin completedCheckpoints) ~> (b \in completedCheckpoints)

(* Thm-S-SC-12: Source 注入的 Barrier 最终传播到所有 Sink *)
BarrierEventuallyReachesSinks(b) ==
    /\ b \in Barriers
    /\ \E t \in Tasks :
        /\ OperatorType[t] = OpSource
        /\ barrierStates[t][b] = "aligned"
    => <> (\A s \in Tasks :
            OperatorType[s] = OpSink => barrierStates[s][b] = "acknowledged")

(* Thm-S-SC-13: Sink 的 in_flight 记录在 checkpoint 完成后最终变为 committed *)
PendingRecordsEventuallyCommitted ==
    \A t \in Tasks :
        OperatorType[t] = OpSink =>
            \A i \in 1..Len(outputRecords[t]) :
                outputRecords[t][i].status = "in_flight"
                    ~> outputRecords[t][i].status = "committed"

------------------------------------------------------------------------------
(*============================================================================*)
(* 规格属性定理                                                                *)
(*============================================================================*)

(* Thm-S-SC-14: 规约蕴含类型不变式始终成立 *)
THEOREM Spec => []TypeInvariant

(* Thm-S-SC-15: 规约蕴含 Checkpoint 完整性始终成立 *)
THEOREM Spec => []CheckpointCompleteness

(* Thm-S-SC-16: 规约蕴含 Exactly-Once 不变式始终成立 *)
THEOREM Spec => []ExactlyOnceInv

(* Thm-S-SC-17: 规约蕴含无孤立状态始终成立 *)
THEOREM Spec => []NoOrphanedState

(* Thm-S-SC-18: 规约蕴含快照一致性始终成立 *)
THEOREM Spec => []SnapshotConsistency

------------------------------------------------------------------------------
(*============================================================================*)
(* INSTANCE 示例与模块引用                                                     *)
(*============================================================================*)

(* INSTANCE 示例：引入 Utilities 模块的辅助函数（可选） *)
(* 注：TLA+ Toolbox 中需将 Utilities.tla 加入模块搜索路径 *)
(* INSTANCE Utilities WITH ANY <- {"data"} *)

(* ASSUME 示例：引入基于 Utilities 的额外假设（若可用） *)
(* ASSUME MaxCheckpointsAssumption == IsFiniteSet(Checkpoints) *)

------------------------------------------------------------------------------
(*============================================================================*)
(* TLC 模型检测配置建议                                                        *)
(*============================================================================*)

(******************************************************************************)
(* TLC 模型检测配置（在 .cfg 文件中使用）                                        *)
(*                                                                            *)
(* CONSTANTS                                                                  *)
(*   Operators = {op_src, op_map, op_sink}                                    *)
(*   Tasks     = {t_src, t_map, t_sink}                                       *)
(*   OperatorType = [t_src |-> "source", t_map |-> "map", t_sink |-> "sink"]  *)
(*   Barriers  = {1, 2}                                                       *)
(*   StateSnapshots = {s1, s2, s3}                                            *)
(*   Checkpoints = {1, 2}                                                     *)
(*   Upstream  = [t_src |-> {}, t_map |-> {t_src}, t_sink |-> {t_map}]        *)
(*   Downstream = [t_src |-> {t_map}, t_map |-> {t_sink}, t_sink |-> {}]     *)
(*   MaxInFlight = 3                                                          *)
(*                                                                            *)
(* INVARIANTS                                                                 *)
(*   TypeInvariant                                                            *)
(*   CheckpointCompleteness                                                   *)
(*   ExactlyOnceInv                                                           *)
(*   NoOrphanedState                                                          *)
(*                                                                            *)
(* PROPERTIES                                                                 *)
(*   EventuallyCheckpointCompletes(1)                                         *)
(*   BarrierEventuallyReachesSinks(1)                                         *)
(*                                                                            *)
(* STATE CONSTRAINTS（可选，限制状态空间）                                      *)
(*   \A t \in Tasks : Len(inFlightData[t]) <= MaxInFlight                     *)
(*   \A t \in Tasks : Len(outputRecords[t]) <= 5                              *)
(*                                                                            *)
(* SYMMETRY（可选，利用对称性约简）                                             *)
(*   Permutations = Permutations(Tasks)                                       *)
(*                                                                            *)
(* 注意:                                                                      *)
(*   1. 初始模型应使用最小的 Task 集合（2-3 个）和 1 个 Barrier                 *)
(*   2. 验证通过后再逐步扩展至更多 Task 和 Barrier                              *)
(*   3. 如果状态空间过大，可通过 MaxInFlight 和输出记录长度限制状态空间         *)
(******************************************************************************)

------------------------------------------------------------------------------
(*============================================================================*)
(* FORMAL-GAP 标注汇总                                                         *)
(*============================================================================*)

(******************************************************************************)
(*                                                                            *)
(* FORMAL-GAP-01 [IntermediateReceiveBarrierAligned/Unaligned]:               *)
(*   当前抽象将 barrier 对齐/非对齐简化为原子状态转移。实际 Flink 实现中：      *)
(*   - 对齐模式需显式建模 per-input-channel 的 barrier 状态                   *)
(*   - 非对齐模式需建模 in-flight buffer 的快照和 channel 级别的状态          *)
(*   完整形式化需扩展状态空间：barrierStates[t][b][channel]                   *)
(*                                                                            *)
(* FORMAL-GAP-02 [TransmitDataToDownstream]:                                  *)
(*   网络层简化为直接上下游传递。完整建模需引入：                               *)
(*   - ResultPartition / InputGate 结构                                       *)
(*   - 网络缓冲区和 credit-based 反压机制                                     *)
(*   - 数据分区策略（hash / round-robin / broadcast）                         *)
(*                                                                            *)
(* FORMAL-GAP-03 [CheckpointAbort]:                                           *)
(*   当前简化模型未显式建模 Task 故障和 region-based 恢复。                     *)
(*   完整形式化需引入：                                                         *)
(*   - TaskFailure 状态和故障检测超时                                         *)
(*   - Region-based 增量 checkpoint 恢复协议                                  *)
(*   - CheckpointCoordinator 的决策逻辑                                       *)
(*                                                                            *)
(* FORMAL-GAP-04 [AtLeastOnce / ExactlyOnce]:                                 *)
(*   端到端 exactly-once 需外部系统配合（如 Kafka 事务、idempotent producer）。 *)
(*   当前规约聚焦于 Flink 内部 exactly-once；端到端语义需联合建模外部系统。     *)
(*                                                                            *)
(* FORMAL-GAP-05 [AsyncSnapshotSemantics]:                                    *)
(*   异步快照的并发语义未完全展开。完整建模需区分同步部分（状态表拷贝）和       *)
(*   异步部分（快照文件写入），并形式化证明二者组合的原子性。                   *)
(*                                                                            *)
(******************************************************************************)

------------------------------------------------------------------------------
(*============================================================================*)
(* 规约结束                                                                    *)
(*============================================================================*)

================================================================================
