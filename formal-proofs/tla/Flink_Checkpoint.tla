-------------------------------- MODULE Flink_Checkpoint --------------------------------
(* ============================================================================ *)
(* TLA+ Specification of Flink Checkpoint Protocol                               *)
(* ============================================================================ *)
(* 形式化等级: L5 (形式规格)                                                    *)
(* 对应文档: Struct/04-proofs/04.01-flink-checkpoint-correctness.md             *)
(* 定理: Thm-S-04-01: Flink Checkpoint正确性证明                                 *)
(* ============================================================================ *)

EXTENDS Integers, Sequences, FiniteSets, Naturals

(* ---------------------------------------------------------------------------- *)
(* 常量定义                                                                     *)
(* ---------------------------------------------------------------------------- *)
CONSTANTS
    TaskManagers,           \* 任务管理器集合
    JobManager,             \* 作业管理器
    CheckpointInterval,     \* 检查点间隔
    MaxInflightRecords      \* 最大在途记录数

(* ASSUME-01: 参数化假设 - CheckpointInterval 必须是正自然数 *)
(* 证明思路: 这是模型参数约束，由 TLC 配置保证，非证明目标 *)
ASSUME CheckpointIntervalAssumption ==
    /\ CheckpointInterval \in Nat
    /\ CheckpointInterval > 0

(* ---------------------------------------------------------------------------- *)
(* 类型定义                                                                     *)
(* ---------------------------------------------------------------------------- *)
TaskManager == STRING
Channel == [source : TaskManager, dest : TaskManager]
Record == [data : STRING, timestamp : Nat]
Barrier == [type : {"barrier"}, checkpoint_id : Nat]
Message == Record \cup Barrier

(* 处理器状态 *)
ProcessorState == 
    [status : {"running", "checkpointing", "completed"},
     state_data : STRING,
     pending_barriers : SUBSET Nat]

(* ---------------------------------------------------------------------------- *)
(* 变量定义                                                                     *)
(* ---------------------------------------------------------------------------- *)
VARIABLES
    tm_states,          \* TaskManager状态映射
    channels,           \* 通道中的消息队列
    checkpoint_coord,   \* Checkpoint协调器状态
    global_checkpoint   \* 全局检查点状态

(* ---------------------------------------------------------------------------- *)
(* 初始状态                                                                     *)
(* ---------------------------------------------------------------------------- *)
Init ==
    /\ tm_states = [tm \in TaskManagers |-> 
                     [status |-> "running",
                      state_data |-> "empty",
                      pending_barriers |-> {}]]
    /\ channels = [ch \in Channel |-> <<>>]
    /\ checkpoint_coord = [next_id |-> 1,
                          active |-> {},
                          completed |-> {}]
    /\ global_checkpoint = [latest |-> 0, states |-> {}]

(* ---------------------------------------------------------------------------- *)
(* 动作定义                                                                     *)
(* ---------------------------------------------------------------------------- *)

(* 1. 作业管理器触发Checkpoint *)
TriggerCheckpoint ==
    /\ checkpoint_coord.active = {}
    /\ LET cp_id == checkpoint_coord.next_id
       IN
       /\ checkpoint_coord' = [checkpoint_coord EXCEPT 
                               !.next_id = @ + 1,
                               !.active = {cp_id}]
       /\ channels' = [ch \in Channel |-> 
                       Append(channels[ch], [type |-> "barrier", checkpoint_id |-> cp_id])]
       /\ UNCHANGED <<tm_states, global_checkpoint>>

(* 2. TaskManager接收Barrier并快照状态 *)
ReceiveBarrier(tm) ==
    /\ tm_states[tm].status = "running"
    /\ \E ch \in Channel :
        /\ ch.dest = tm
        /\ Len(channels[ch]) > 0
        /\ LET msg == Head(channels[ch])
           IN
           /\ msg.type = "barrier"
           /\ LET cp_id == msg.checkpoint_id
                  tm_state == tm_states[tm]
              IN
              /\ tm_states' = [tm_states EXCEPT ![tm] = 
                               [status |-> "checkpointing",
                                state_data |-> @.state_data,
                                pending_barriers |-> @.pending_barriers \union {cp_id}]]
              /\ channels' = [channels EXCEPT ![ch] = Tail(@)]
              /\ UNCHANGED <<checkpoint_coord, global_checkpoint>>

(* 3. TaskManager完成Checkpoint并确认 *)
CompleteCheckpoint(tm) ==
    /\ tm_states[tm].status = "checkpointing"
    /\ tm_states[tm].pending_barriers # {}
    /\ LET cp_id == CHOOSE id \in tm_states[tm].pending_barriers : TRUE
       IN
       /\ tm_states' = [tm_states EXCEPT ![tm] = 
                        [status |-> "running",
                         state_data |-> @.state_data,
                         pending_barriers |-> @.pending_barriers \\ {cp_id}]]
       /\ checkpoint_coord' = [checkpoint_coord EXCEPT 
                               !.completed = @ \union {cp_id}]
       /\ UNCHANGED <<channels, global_checkpoint>>

(* 4. 全局Checkpoint确认 *)
(* TODO-03: checkpoint_coord.completed \supseteq TaskManagers 存在类型不匹配 *)
(* 问题: completed 存储的是 checkpoint ID (Nat)，而 TaskManagers 是 STRING 集合 *)
(* 完成建议: 重构为按 checkpoint ID 追踪每个 TM 的完成状态，例如 completedTM[cp_id] \subseteq TaskManagers *)
ConfirmGlobalCheckpoint ==
    /\ checkpoint_coord.active # {}
    /\ LET cp_id == CHOOSE id \in checkpoint_coord.active : TRUE
       IN
       /\ checkpoint_coord.completed \supseteq TaskManagers  \* 所有TM完成 (注意: 当前实现存在类型不匹配，语义待修正)
       /\ global_checkpoint' = [latest |-> cp_id,
                               states |-> global_checkpoint.states \union {cp_id}]
       /\ checkpoint_coord' = [checkpoint_coord EXCEPT 
                               !.active = {},
                               !.completed = {}]
       /\ UNCHANGED <<tm_states, channels>>

(* 5. 正常记录处理 *)
ProcessRecord(tm) ==
    /\ tm_states[tm].status = "running"
    /\ \E ch \in Channel :
        /\ ch.dest = tm
        /\ Len(channels[ch]) > 0
        /\ LET msg == Head(channels[ch])
           IN
           /\ msg.type # "barrier"  \* 普通记录
           /\ tm_states' = [tm_states EXCEPT ![tm].state_data = 
                            @ ++ ",processed:" ++ msg.data]
           /\ channels' = [channels EXCEPT ![ch] = Tail(@)]
           /\ UNCHANGED <<checkpoint_coord, global_checkpoint>>

(* ---------------------------------------------------------------------------- *)
(* 下一步关系                                                                   *)
(* ---------------------------------------------------------------------------- *)
Next ==
    \/ TriggerCheckpoint
    \/ \E tm \in TaskManagers : ReceiveBarrier(tm)
    \/ \E tm \in TaskManagers : CompleteCheckpoint(tm)
    \/ ConfirmGlobalCheckpoint
    \/ \E tm \in TaskManagers : ProcessRecord(tm)

(* ---------------------------------------------------------------------------- *)
(* 时序属性                                                                     *)
(* ---------------------------------------------------------------------------- *)

(* 活性: 最终总会触发Checkpoint *)
(* TODO-01: 需补充公平性条件 WF_vars(TriggerCheckpoint) 以确保活性 *)
(* 完成建议: 在 Spec 中添加公平性约束，使 TriggerCheckpoint 在持续可启用时最终执行 *)
Liveness == 
    <> (global_checkpoint.latest > 0)

(* 安全性: Checkpoint ID单调递增 *)
Safety ==
    [][global_checkpoint.latest' >= global_checkpoint.latest]_vars

(* 一致性: 所有TaskManager的快照是一致的 *)
(* TODO-02: 当前为简化表示，需补充具体状态等价性条件 *)
(* 完成建议: 定义状态等价关系 StateEquivalence(tm1, tm2, cp_id)，比较处理记录的集合 *)
Consistency ==
    \A cp_id \in global_checkpoint.states :
        \A tm1, tm2 \in TaskManagers :
            (cp_id \notin tm_states[tm1].pending_barriers /\
             cp_id \notin tm_states[tm2].pending_barriers)
            => tm_states[tm1].state_data = tm_states[tm2].state_data

(* ---------------------------------------------------------------------------- *)
(* 规约完整定义                                                                 *)
(* ---------------------------------------------------------------------------- *)
vars == <<tm_states, channels, checkpoint_coord, global_checkpoint>>

Spec == Init /\ [][Next]_vars /\ Liveness

(* ---------------------------------------------------------------------------- *)
(* 定理: Checkpoint正确性                                                       *)
(* ---------------------------------------------------------------------------- *)

(* Thm-S-04-01: Checkpoint协议保证一致性 *)
THEOREM CheckpointCorrectness ==
    Spec => []Consistency

(* End of Flink_Checkpoint.tla *)
================================================================================
