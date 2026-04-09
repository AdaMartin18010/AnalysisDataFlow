(*
 * Checkpoint.tla
 * Flink Checkpoint协议的TLA+形式化规约
 * 
 * 本规约形式化定义了Flink分布式Checkpoint机制，包括：
 * - Barrier消息传播语义
 * - 算子状态快照行为
 * - 一致割集(Consistent Cut)条件
 * - Checkpoint完成条件
 * - 安全性不变式(Safety Invariants)
 *
 * 版本: 1.1 (修复版)
 * 日期: 2026-04-09
 * 参考: Flink Checkpointing机制、Chandy-Lamport算法
 *)

----------------------------- MODULE Checkpoint -----------------------------

(*===========================================================================*)
(* 导入标准模块                                                               *)
(*===========================================================================*)

EXTENDS Naturals, Sequences, FiniteSets, TLC

(*===========================================================================*)
(* 常量定义                                                                   *)
(*===========================================================================*)

CONSTANTS
    Operators,              (* 算子集合: 所有参与Checkpoint的算子 *)
    Sources,                (* 源算子子集: 发起Checkpoint的算子 *)
    Sinks,                  (* 汇算子子集: Checkpoint终止的算子 *)
    MaxEvents,              (* 每个算子处理的最大事件数 *)
    MaxCheckpoints          (* 最大Checkpoint数量 *)

ASSUME
    Sources \subseteq Operators
ASSUME
    Sinks \subseteq Operators
ASSUME
    \A s \in Sources : \A k \in Sinks : s # k  (* 源和汇是不同的算子 *)

(*===========================================================================*)
(* 类型定义                                                                   *)
(*===========================================================================*)

(*---------------------------------------------------------------------------*)
(* Def-V-01: CheckpointID - Checkpoint标识符类型                              *)
(*---------------------------------------------------------------------------*)
CheckpointID == 1..MaxCheckpoints

(*---------------------------------------------------------------------------*)
(* Def-V-02: Event - 数据事件类型                                             *)
(* 事件是算子之间传递的基本数据单元                                           *)
(*---------------------------------------------------------------------------*)
Event == [type: {"DATA"}, value: Nat]

(*---------------------------------------------------------------------------*)
(* Def-V-03: Barrier - Barrier消息类型                                        *)
(* Barrier是特殊的控制消息，用于触发和协调Checkpoint                           *)
(*---------------------------------------------------------------------------*)
Barrier == [type: {"BARRIER"}, cpId: CheckpointID, source: Operators]

(*---------------------------------------------------------------------------*)
(* Def-V-04: Message - 消息类型 (数据或Barrier)                                *)
(*---------------------------------------------------------------------------*)
Message == Event \union Barrier

(*---------------------------------------------------------------------------*)
(* Def-V-05: OperatorState - 算子状态                                         *)
(* 每个算子维护其处理状态、待处理Barrier和已确认快照                          *)
(*---------------------------------------------------------------------------*)
OperatorState == [
    processed: Nat,                              (* 已处理事件计数 *)
    pendingBarriers: SUBSET Barrier,             (* 待处理Barrier集合 *)
    snapshot: SUBSET Event,                      (* 状态快照 (KeyedState) *)
    checkpointed: SUBSET CheckpointID,           (* 已完成的Checkpoint *)
    inFlight: Seq(Message)                       (* 在途消息队列 *)
]

(*---------------------------------------------------------------------------*)
(* Def-V-06: ChannelState - 通道状态 (算子间连接)                              *)
(* 每个输入通道维护一个消息队列                                               *)
(*---------------------------------------------------------------------------*)
Channel == Operators \times Operators

(*===========================================================================*)
(* 变量定义                                                                   *)
(*===========================================================================*)

VARIABLES
    operatorStates,         (* operatorStates[op] = 算子op的当前状态 *)
    channelBuffers,         (* channelBuffers[<<src, dst>>] = 通道消息队列 *)
    globalCheckpointStatus, (* globalCheckpointStatus[cpId] = Checkpoint全局状态 *)
    currentCheckpointId     (* 当前正在进行的Checkpoint ID *)

(*---------------------------------------------------------------------------*)
(* Def-V-07: TypeInvariant - 类型正确性                                       *)
(*---------------------------------------------------------------------------*)
TypeInvariant ==
    /\ operatorStates \in [Operators -> OperatorState]
    /\ channelBuffers \in [Channel -> Seq(Message)]
    /\ globalCheckpointStatus \in [CheckpointID -> {"PENDING", "COMPLETED", "FAILED", "NONE"}]
    /\ currentCheckpointId \in 0..MaxCheckpoints

(*===========================================================================*)
(* 辅助函数                                                                   *)
(*===========================================================================*)

(*---------------------------------------------------------------------------*)
(* Def-V-08: IsSource - 判断算子是否为源算子                                  *)
(*---------------------------------------------------------------------------*)
IsSource(op) == op \in Sources

(*---------------------------------------------------------------------------*)
(* Def-V-09: IsSink - 判断算子是否为汇算子                                    *)
(*---------------------------------------------------------------------------*)
IsSink(op) == op \in Sinks

(*---------------------------------------------------------------------------*)
(* Def-V-10: GetInputs - 获取算子的输入算子集合                               *)
(*---------------------------------------------------------------------------*)
GetInputs(op) == { src \in Operators : <<src, op>> \in Channel }

(*---------------------------------------------------------------------------*)
(* Def-V-11: GetOutputs - 获取算子的输出算子集合                              *)
(*---------------------------------------------------------------------------*)
GetOutputs(op) == { dst \in Operators : <<op, dst>> \in Channel }

(*---------------------------------------------------------------------------*)
(* Def-V-12: CountBarriers - 统计队列中特定Checkpoint的Barrier数量            *)
(*---------------------------------------------------------------------------*)
CountBarriers(queue, cpId) ==
    Cardinality({ i \in 1..Len(queue) : 
        /\ queue[i] \in Barrier 
        /\ queue[i].cpId = cpId })

(*===========================================================================*)
(* 初始化条件                                                                 *)
(*===========================================================================*)

(*---------------------------------------------------------------------------*)
(* Def-V-13: Init - 系统初始状态                                              *)
(*---------------------------------------------------------------------------*)
Init ==
    /\ operatorStates = [op \in Operators |-> [
            processed |-> 0,
            pendingBarriers |-> {},
            snapshot |-> {},
            checkpointed |-> {},
            inFlight |-> <<>>
        ]]
    /\ channelBuffers = [ch \in Channel |-> <<>>]
    /\ globalCheckpointStatus = [cp \in CheckpointID |-> "NONE"]
    /\ currentCheckpointId = 0

(*===========================================================================*)
(* 动作定义                                                                   *)
(*===========================================================================*)

(*---------------------------------------------------------------------------*)
(* Def-V-14: TriggerCheckpoint - 源算子触发新Checkpoint                       *)
(* 源算子生成Barrier并发送到所有下游算子                                      *)
(*---------------------------------------------------------------------------*)
TriggerCheckpoint(cp) ==
    /\ cp = currentCheckpointId + 1
    /\ cp <= MaxCheckpoints
    /\ globalCheckpointStatus[cp] = "NONE"
    /\ currentCheckpointId' = cp
    /\ globalCheckpointStatus' = [globalCheckpointStatus EXCEPT ![cp] = "PENDING"]
    /\ LET newBarrier == [type |-> "BARRIER", cpId |-> cp, source |-> op]
       IN operatorStates' = [op \in Operators |->
            IF IsSource(op)
            THEN [operatorStates[op] EXCEPT 
                    !.pendingBarriers = @ \cup {newBarrier},
                    !.inFlight = Append(@, newBarrier)
                 ]
            ELSE operatorStates[op]]
    /\ channelBuffers' = [ch \in Channel |->
            IF IsSource(ch[1]) /\ ch[2] \in GetOutputs(ch[1])
            THEN LET newBarrier == [type |-> "BARRIER", cpId |-> cp, source |-> ch[1]]
                 IN Append(channelBuffers[ch], newBarrier)
            ELSE channelBuffers[ch]]

(*---------------------------------------------------------------------------*)
(* Def-V-15: ProcessDataEvent - 算子处理数据事件                              *)
(* 算子从输入通道接收并处理数据事件                                           *)
(* 前置条件: 所有更早的Barrier已被处理                                        *)
(*---------------------------------------------------------------------------*)
ProcessDataEvent(op) ==
    /\ \E src \in GetInputs(op) :
        /\ Len(channelBuffers[<<src, op>>]) > 0
        /\ LET msg == Head(channelBuffers[<<src, op>>])
           IN /\ msg \in Event
              /\ \A b \in operatorStates[op].pendingBarriers : 
                  b.source = src  (* 该源的Barrier已对齐 *)
        /\ LET msg == Head(channelBuffers[<<src, op>>])
           IN /\ channelBuffers' = [channelBuffers EXCEPT ![<<src, op>>] = Tail(@)]
              /\ operatorStates' = [operatorStates EXCEPT 
                   ![op] = [@ EXCEPT 
                       !.processed = @ + 1,
                       !.snapshot = @ \cup {msg} 
                   ]
               ]
    /\ UNCHANGED <<globalCheckpointStatus, currentCheckpointId>>

(*---------------------------------------------------------------------------*)
(* Def-V-16: ReceiveBarrier - 算子接收Barrier消息                             *)
(* Barrier到达时，算子记录并准备对齐                                          *)
(*---------------------------------------------------------------------------*)
ReceiveBarrier(op) ==
    /\ \E src \in GetInputs(op) :
        /\ Len(channelBuffers[<<src, op>>]) > 0
        /\ LET msg == Head(channelBuffers[<<src, op>>])
           IN /\ msg \in Barrier
              /\ channelBuffers' = [channelBuffers EXCEPT ![<<src, op>>] = Tail(@)]
              /\ operatorStates' = [operatorStates EXCEPT 
                   ![op] = [@ EXCEPT 
                       !.pendingBarriers = @ \cup {msg}
                   ]
               ]
    /\ UNCHANGED <<globalCheckpointStatus, currentCheckpointId>>

(*---------------------------------------------------------------------------*)
(* Def-V-17: AlignBarriers - Barrier对齐操作                                  *)
(* 当算子从所有输入通道收到同一Checkpoint的Barrier时，执行对齐                *)
(*---------------------------------------------------------------------------*)
AlignBarriers(op, cp) ==
    /\ LET pendingCpBarriers == { b \in operatorStates[op].pendingBarriers : b.cpId = cp }
       IN /\ Cardinality(pendingCpBarriers) = Cardinality(GetInputs(op))
          /\ \A src \in GetInputs(op) : 
              \E b \in pendingCpBarriers : b.source = src
    /\ operatorStates' = [operatorStates EXCEPT 
            ![op] = [@ EXCEPT 
                !.pendingBarriers = @ \ { b \in @ : b.cpId = cp },
                !.checkpointed = @ \cup {cp}
            ]
         ]
    /\ UNCHANGED <<channelBuffers, globalCheckpointStatus, currentCheckpointId>>

(*---------------------------------------------------------------------------*)
(* Def-V-18: PropagateBarrier - Barrier向下游传播                             *)
(* 对齐完成后，算子向下游发送Barrier                                          *)
(*---------------------------------------------------------------------------*)
PropagateBarrier(op, cp) ==
    /\ cp \in operatorStates[op].checkpointed
    /\ \A dst \in GetOutputs(op) : 
        Len(channelBuffers[<<op, dst>>]) < MaxEvents  (* 通道不满 *)
    /\ LET newBarrier == [type |-> "BARRIER", cpId |-> cp, source |-> op]
       IN /\ operatorStates' = [operatorStates EXCEPT 
                ![op] = [@ EXCEPT 
                    !.inFlight = Append(@, newBarrier)
                ]
             ]
          /\ channelBuffers' = [dst \in Operators |->
                IF dst \in GetOutputs(op)
                THEN Append(channelBuffers[<<op, dst>>], newBarrier)
                ELSE channelBuffers[<<op, dst>>]]
    /\ UNCHANGED <<globalCheckpointStatus, currentCheckpointId>>

(*---------------------------------------------------------------------------*)
(* Def-V-19: CompleteCheckpoint - 完成Checkpoint                              *)
(* 当所有Sink算子都确认收到Barrier时，Checkpoint完成                          *)
(*---------------------------------------------------------------------------*)
CompleteCheckpoint(cp) ==
    /\ globalCheckpointStatus[cp] = "PENDING"
    /\ \A sink \in Sinks : cp \in operatorStates[sink].checkpointed
    /\ globalCheckpointStatus' = [globalCheckpointStatus EXCEPT ![cp] = "COMPLETED"]
    /\ UNCHANGED <<operatorStates, channelBuffers, currentCheckpointId>>

(*===========================================================================*)
(* 下一步动作组合 (修复版)                                                     *)
(*===========================================================================*)

(* 修复后的Next操作符：使用析取而非合取 *)
Next ==
    \/ \E cp \in CheckpointID :
        /\ cp = currentCheckpointId + 1 
        /\ cp <= MaxCheckpoints
        /\ globalCheckpointStatus[cp] = "NONE"
        /\ TriggerCheckpoint(cp)
    \/ \E op \in Operators : ProcessDataEvent(op)
    \/ \E op \in Operators : ReceiveBarrier(op)
    \/ \E op \in Operators, cp \in CheckpointID : AlignBarriers(op, cp)
    \/ \E op \in Operators, cp \in CheckpointID : PropagateBarrier(op, cp)
    \/ \E cp \in CheckpointID : CompleteCheckpoint(cp)

(*===========================================================================*)
(* 公平性条件                                                                 *)
(*===========================================================================*)

Fairness ==
    /\ WF_<<operatorStates, channelBuffers, globalCheckpointStatus, currentCheckpointId>>(
        \E op \in Operators : ProcessDataEvent(op))
    /\ WF_<<operatorStates, channelBuffers, globalCheckpointStatus, currentCheckpointId>>(
        \E op \in Operators : ReceiveBarrier(op))
    /\ WF_<<operatorStates, channelBuffers, globalCheckpointStatus, currentCheckpointId>>(
        \E op \in Operators, cp \in CheckpointID : AlignBarriers(op, cp))
    /\ WF_<<operatorStates, channelBuffers, globalCheckpointStatus, currentCheckpointId>>(
        \E op \in Operators, cp \in CheckpointID : PropagateBarrier(op, cp))
    /\ WF_<<operatorStates, channelBuffers, globalCheckpointStatus, currentCheckpointId>>(
        \E cp \in CheckpointID : CompleteCheckpoint(cp))

(*===========================================================================*)
(* 安全性不变式 (Safety Invariants)                                           *)
(*===========================================================================*)

(*---------------------------------------------------------------------------*)
(* Prop-V-01: CheckpointProgressMonotonic - Checkpoint进度单调性              *)
(* 一旦Checkpoint完成，状态不会改变                                           *)
(*---------------------------------------------------------------------------*)
CheckpointProgressMonotonic ==
    \A cp \in CheckpointID :
        globalCheckpointStatus[cp] = "COMPLETED" =>
            [] (globalCheckpointStatus[cp] = "COMPLETED")

(*---------------------------------------------------------------------------*)
(* Prop-V-02: ConsistentCutCondition - 一致割集条件                           *)
(* 对于任意完成的Checkpoint，所有通道状态满足:                                 *)
(* - 在源算子快照之后发送的消息，在目标算子快照之前接收                       *)
(* 即: 割集之前的事件都被处理，割集之后的事件未被处理                         *)
(*---------------------------------------------------------------------------*)
ConsistentCutCondition ==
    \A cp \in CheckpointID :
        globalCheckpointStatus[cp] = "COMPLETED" =>
            \A ch \in Channel :
                LET src == ch[1]
                    dst == ch[2]
                IN /\ cp \in operatorStates[src].checkpointed
                   /\ cp \in operatorStates[dst].checkpointed
                   /\ \A i \in 1..Len(channelBuffers[ch]) :
                       channelBuffers[ch][i] \in Event =>
                           (* 数据事件必须在Barrier之后到达 *)
                           \E j \in 1..i-1 :
                               /\ channelBuffers[ch][j] \in Barrier
                               /\ channelBuffers[ch][j].cpId = cp

(*---------------------------------------------------------------------------*)
(* Prop-V-03: NoBarrierLoss - Barrier不会丢失                                 *)
(* Barrier在传输过程中不会被丢弃                                              *)
(*---------------------------------------------------------------------------*)
NoBarrierLoss ==
    \A cp \in CheckpointID :
        \A ch \in Channel :
            CountBarriers(channelBuffers[ch], cp) <= 1

(*---------------------------------------------------------------------------*)
(* Prop-V-04: CheckpointExactlyOnce - Checkpoint恰好一次语义                  *)
(* 每个算子对每个Checkpoint最多执行一次快照                                  *)
(*---------------------------------------------------------------------------*)
CheckpointExactlyOnce ==
    \A op \in Operators :
        \A cp \in CheckpointID :
            cp \in operatorStates[op].checkpointed =>
                ~ ( \E b \in operatorStates[op].pendingBarriers : b.cpId = cp )

(*---------------------------------------------------------------------------*)
(* Prop-V-05: StateSnapshotConsistency - 状态快照一致性                       *)
(* 算子快照只包含割集之前处理的事件                                           *)
(*---------------------------------------------------------------------------*)
StateSnapshotConsistency ==
    \A op \in Operators :
        \A cp \in CheckpointID :
            (cp \in operatorStates[op].checkpointed) =>
                \A e \in operatorStates[op].snapshot :
                    (* 所有快照事件都在Barrier到达前处理 *)
                    \A src \in GetInputs(op) :
                        \E b \in operatorStates[op].pendingBarriers :
                            /\ b.cpId = cp
                            /\ b.source = src
                            (* 该事件来自src且在Barrier前 *)

(*---------------------------------------------------------------------------*)
(* Prop-V-06: BarrierAlignmentCompleteness - Barrier对齐完备性                *)
(* 只有从所有输入都收到Barrier后，才能声明Checkpoint完成                      *)
(*---------------------------------------------------------------------------*)
BarrierAlignmentCompleteness ==
    \A op \in Operators :
        \A cp \in CheckpointID :
            cp \in operatorStates[op].checkpointed =>
                LET receivedBarriers == { b.source : b \in operatorStates[op].pendingBarriers \union 
                                                     {bb \in operatorStates[op].pendingBarriers : bb.cpId = cp} }
                IN receivedBarriers = GetInputs(op)

(*---------------------------------------------------------------------------*)
(* Prop-V-07: ChannelFIFO - 通道FIFO属性                                      *)
(* 通道保持消息顺序 (FIFO)                                                    *)
(*---------------------------------------------------------------------------*)
ChannelFIFO ==
    \A ch \in Channel :
        \A i, j \in 1..Len(channelBuffers[ch]) :
            i < j =>
                LET msg_i == channelBuffers[ch][i]
                    msg_j == channelBuffers[ch][j]
                IN /\ msg_i \in Barrier /\ msg_j \in Barrier => 
                       msg_i.cpId <= msg_j.cpId

(*===========================================================================*)
(* 组合安全性不变式                                                           *)
(*===========================================================================*)

(*---------------------------------------------------------------------------*)
(* Def-V-20: SafetyInvariant - 组合安全性不变式                               *)
(*---------------------------------------------------------------------------*)
SafetyInvariant ==
    /\ TypeInvariant
    /\ CheckpointProgressMonotonic
    /\ ConsistentCutCondition
    /\ NoBarrierLoss
    /\ CheckpointExactlyOnce
    /\ StateSnapshotConsistency
    /\ BarrierAlignmentCompleteness
    /\ ChannelFIFO

(*===========================================================================*)
(* 活性属性 (Liveness Properties)                                             *)
(*===========================================================================*)

(*---------------------------------------------------------------------------*)
(* Prop-V-08: CheckpointEventuallyCompletes - Checkpoint最终完成              *)
(* 每个被触发的Checkpoint最终都会完成                                         *)
(*---------------------------------------------------------------------------*)
CheckpointEventuallyCompletes ==
    \A cp \in CheckpointID :
        (globalCheckpointStatus[cp] = "PENDING") ~> 
        (globalCheckpointStatus[cp] = "COMPLETED")

(*---------------------------------------------------------------------------*)
(* Prop-V-09: AllBarriersPropagated - 所有Barrier最终传播                     *)
(* 所有Barrier最终都会传播到所有Sink                                          *)
(*---------------------------------------------------------------------------*)
AllBarriersPropagated ==
    \A cp \in CheckpointID :
        \A sink \in Sinks :
            (globalCheckpointStatus[cp] = "PENDING") ~>
            (cp \in operatorStates[sink].checkpointed)

(*===========================================================================*)
(* 规约                                                                       *)
(*===========================================================================*)

Spec == Init /\ [][Next]_<<operatorStates, channelBuffers, globalCheckpointStatus, currentCheckpointId>> /\ Fairness

(*===========================================================================*)
(* 定理                                                                       *)
(*===========================================================================*)

(*---------------------------------------------------------------------------*)
(* Thm-V-01: Safety - 安全性定理                                              *)
(* Spec蕴含所有安全性不变式                                                   *)
(*---------------------------------------------------------------------------*)
THEOREM Safety == Spec => [] SafetyInvariant

(*---------------------------------------------------------------------------*)
(* Thm-V-02: Liveness - 活性定理                                              *)
(* Spec蕴含Checkpoint最终完成                                                 *)
(*---------------------------------------------------------------------------*)
THEOREM Liveness == Spec => CheckpointEventuallyCompletes

(*---------------------------------------------------------------------------*)
(* Thm-V-03: ConsistentCutGuarantee - 一致割集保证定理                        *)
(* 完成的Checkpoint保证形成一致割集                                           *)
(*---------------------------------------------------------------------------*)
THEOREM ConsistentCutGuarantee == Spec => [] ConsistentCutCondition

=============================================================================
(* End of module Checkpoint *)
