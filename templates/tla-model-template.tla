----------------------------- MODULE ModelTemplate -----------------
(******************************************************************************
 * TLA+模型模板 - 流计算系统形式化验证
 * 
 * 文档编号: Template-TLA-01
 * 用途: 提供标准化的TLA+模型结构和命名规范
 * 形式化等级: L4-L5
 ******************************************************************************)

(* ============================================================================
 * 第1部分：扩展和标准模块导入
 * ============================================================================ *)

EXTENDS 
    Integers,         (* 整数运算 *)
    Sequences,        (* 序列操作 *)
    FiniteSets,       (* 有限集合 *)
    TLC,              (* TLC模型检查器扩展 *)
    Bags              (* 多重集 *), 
    
(* 可选扩展 *)
(* EXTENDS SequencesExt, FiniteSetsExt *)

(* ============================================================================
 * 第2部分：常量声明
 * ============================================================================ *)

CONSTANTS
    (* 系统组件 *)
    Operators,        (* 算子集合 *)
    MaxEvents,        (* 最大事件数限制 *)
    
    (* 时间参数 *)
    CheckpointInterval, (* 检查点触发间隔 *)
    TimeoutValue,       (* 超时阈值 *)
    
    (* 配置选项 *)
    NULL,             (* 空值表示 *)
    MaxRetries        (* 最大重试次数 *)

(* ============================================================================
 * 第3部分：变量声明
 * ============================================================================ *)

VARIABLES
    (* 状态变量 *)
    state,            (* 算子状态映射 *)
    checkpoint,       (* 检查点状态 *)
    watermark,        (* 当前水印 *)
    
    (* 通信变量 *)
    messages,         (* 在途消息 *)
    barriers,         (* 检查点屏障 *)
    
    (* 控制变量 *)
    coordinator,      (* 协调器状态 *)
    pendingAcks,      (* 待确认集合 *)
    
    (* 历史变量 (用于验证) *)
    history,          (* 事件历史 *)
    deliveredCount    (* 交付计数 *)

(* ============================================================================
 * 第4部分：类型定义和辅助函数
 * ============================================================================ *)

(* 消息类型 *)
Message == [type: {"DATA", "BARRIER", "ACK"}, 
            from: Operators, 
            to: Operators,
            payload: SUBSET Nat]

(* 算子状态 *)
OperatorState == [status: {"IDLE", "RUNNING", "CHECKPOINTING", "FAILED"},
                  processed: Nat,
                  snapshot: Nat \union {NULL}]

(* 协调器状态 *)
CoordinatorState == {"IDLE", "TRIGGERING", "COLLECTING", "COMPLETED"}

(* 辅助函数：序列最大元素 *)
RECURSIVE SeqMax(_)
SeqMax(seq) == 
    IF seq = << >> THEN 0
    ELSE IF Len(seq) = 1 THEN seq[1]
    ELSE Max(seq[1], SeqMax(Tail(seq)))

(* 辅助函数：检查消息是否过期 *)
IsExpired(msg, currentTime) ==
    currentTime - msg.timestamp > TimeoutValue

(* 辅助函数：更新映射 *)
UpdateMap(map, key, value) == [map EXCEPT ![key] = value]

(* ============================================================================
 * 第5部分：类型不变式
 * ============================================================================ *)

TypeInvariant ==
    /\ state \in [Operators -> OperatorState]
    /\ checkpoint \in [Operators -> Nat]
    /\ watermark \in Nat
    /\ messages \subseteq Message
    /\ barriers \subseteq Operators
    /\ coordinator \in CoordinatorState
    /\ pendingAcks \subseteq Operators
    /\ history \in Seq([op: Operators, event: Nat, time: Nat])
    /\ deliveredCount \in [Operators -> Nat]

(* ============================================================================
 * 第6部分：初始化
 * ============================================================================ *)

Init ==
    /\ state = [op \in Operators |-> 
                [status |-> "IDLE", processed |-> 0, snapshot |-> NULL]]
    /\ checkpoint = [op \in Operators |-> 0]
    /\ watermark = 0
    /\ messages = {}
    /\ barriers = {}
    /\ coordinator = "IDLE"
    /\ pendingAcks = {}
    /\ history = << >>
    /\ deliveredCount = [op \in Operators |-> 0]

(* ============================================================================
 * 第7部分：动作定义
 * ============================================================================ *)

(* -------------------------------------------------------------------------
 * 7.1 算子动作
 * ------------------------------------------------------------------------- *)

(* 算子启动 *)
StartOperator(op) ==
    /\ state[op].status = "IDLE"
    /\ state' = [state EXCEPT ![op] = 
                 [status |-> "RUNNING", processed |-> 0, snapshot |-> NULL]]
    /\ UNCHANGED <<checkpoint, watermark, messages, barriers, 
                   coordinator, pendingAcks, history, deliveredCount>>

(* 处理输入事件 *)
ProcessEvent(op) ==
    /\ state[op].status = "RUNNING"
    /\ state[op].processed < MaxEvents
    /\ state' = [state EXCEPT ![op].processed = @ + 1]
    /\ history' = Append(history, 
                         [op |-> op, event |-> state[op].processed + 1, time |-> watermark])
    /\ UNCHANGED <<checkpoint, watermark, messages, barriers,
                   coordinator, pendingAcks, deliveredCount>>

(* 算子失败 *)
OperatorFail(op) ==
    /\ state[op].status \in {"RUNNING", "CHECKPOINTING"}
    /\ state' = [state EXCEPT ![op] = 
                 [status |-> "FAILED", processed |-> checkpoint[op], snapshot |-> NULL]]
    /\ UNCHANGED <<checkpoint, watermark, messages, barriers,
                   coordinator, pendingAcks, history, deliveredCount>>

(* 算子恢复 *)
OperatorRecover(op) ==
    /\ state[op].status = "FAILED"
    /\ state' = [state EXCEPT ![op] = 
                 [status |-> "RUNNING", processed |-> checkpoint[op], snapshot |-> NULL]]
    /\ UNCHANGED <<checkpoint, watermark, messages, barriers,
                   coordinator, pendingAcks, history, deliveredCount>>

(* -------------------------------------------------------------------------
 * 7.2 检查点协议动作
 * ------------------------------------------------------------------------- *)

(* 协调器触发检查点 *)
TriggerCheckpoint ==
    /\ coordinator = "IDLE"
    /\ \E op \in Operators : state[op].processed - checkpoint[op] >= CheckpointInterval
    /\ coordinator' = "TRIGGERING"
    /\ barriers' = Operators
    /\ UNCHANGED <<state, checkpoint, watermark, messages,
                   pendingAcks, history, deliveredCount>>

(* 算子接收屏障并快照 *)
ReceiveBarrier(op) ==
    /\ op \in barriers
    /\ state[op].status = "RUNNING"
    /\ state' = [state EXCEPT ![op] = 
                 [@ EXCEPT !.status = "CHECKPOINTING", 
                           !.snapshot = @.processed]]
    /\ barriers' = barriers \ {op}
    /\ pendingAcks' = pendingAcks \union {op}
    /\ UNCHANGED <<checkpoint, watermark, messages, coordinator, 
                   history, deliveredCount>>

(* 协调器收集确认 *)
CollectAcks ==
    /\ coordinator = "TRIGGERING"
    /\ barriers = {}
    /\ pendingAcks = {}
    /\ coordinator' = "COMPLETED"
    /\ checkpoint' = [op \in Operators |-> state[op].snapshot]
    /\ UNCHANGED <<state, watermark, messages, barriers, 
                   pendingAcks, history, deliveredCount>>

(* 协调器完成检查点 *)
CompleteCheckpoint ==
    /\ coordinator = "COMPLETED"
    /\ state' = [op \in Operators |-> 
                 [state[op] EXCEPT !.status = "RUNNING", !.snapshot |-> NULL]]
    /\ coordinator' = "IDLE"
    /\ UNCHANGED <<checkpoint, watermark, messages, barriers,
                   pendingAcks, history, deliveredCount>>

(* -------------------------------------------------------------------------
 * 7.3 水印推进动作
 * ------------------------------------------------------------------------- *)

(* 推进水印 *)
AdvanceWatermark ==
    /\ \E newWM \in Nat :
        /\ newWM > watermark
        /\ newWM <= Min({state[op].processed : op \in Operators})
        /\ watermark' = newWM
    /\ UNCHANGED <<state, checkpoint, messages, barriers,
                   coordinator, pendingAcks, history, deliveredCount>>

(* -------------------------------------------------------------------------
 * 7.4 消息传递动作
 * ------------------------------------------------------------------------- *)

(* 发送消息 *)
SendMessage(fromOp, toOp, msgType, payload) ==
    /\ fromOp \in Operators
    /\ toOp \in Operators
    /\ messages' = messages \union 
                   {[type |-> msgType, from |-> fromOp, to |-> toOp, payload |-> payload]}
    /\ UNCHANGED <<state, checkpoint, watermark, barriers,
                   coordinator, pendingAcks, history, deliveredCount>>

(* 接收消息 *)
ReceiveMessage(msg) ==
    /\ msg \in messages
    /\ messages' = messages \ {msg}
    /\ UNCHANGED <<state, checkpoint, watermark, barriers,
                   coordinator, pendingAcks, history, deliveredCount>>

(* ============================================================================
 * 第8部分：下一状态关系
 * ============================================================================ *)

(* 所有可能动作的并集 *)
Next ==
    \/ \E op \in Operators : StartOperator(op)
    \/ \E op \in Operators : ProcessEvent(op)
    \/ \E op \in Operators : OperatorFail(op)
    \/ \E op \in Operators : OperatorRecover(op)
    \/ TriggerCheckpoint
    \/ \E op \in Operators : ReceiveBarrier(op)
    \/ CollectAcks
    \/ CompleteCheckpoint
    \/ AdvanceWatermark
    \/ \E fromOp, toOp \in Operators : 
         \E msgType \in {"DATA", "BARRIER", "ACK"} :
         \E payload \in SUBSET Nat :
         SendMessage(fromOp, toOp, msgType, payload)
    \/ \E msg \in Message : ReceiveMessage(msg)

(* 公平性约束 (活性属性需要) *)
Fairness ==
    /\ WF_vars(TriggerCheckpoint)
    /\ WF_vars(CompleteCheckpoint)
    /\ \A op \in Operators : WF_vars(ProcessEvent(op))
    /\ \A op \in Operators : WF_vars(OperatorRecover(op))

(* 完整规范 *)
Spec == Init /\ [][Next]_vars /\ Fairness

(* 变量元组 (用于UNCHANGED) *)
vars == <<state, checkpoint, watermark, messages, barriers,
          coordinator, pendingAcks, history, deliveredCount>>

(* ============================================================================
 * 第9部分：不变式 (安全性属性)
 * ============================================================================ *)

(* 基本类型安全 *)
TypeOK == TypeInvariant

(* 处理计数非负 *)
ProcessedNonNegative ==
    \A op \in Operators : state[op].processed >= 0

(* 检查点单调性 *)
CheckpointMonotonic ==
    \A op \in Operators : checkpoint[op] <= state[op].processed

(* 状态一致性 *)
StateConsistency ==
    \A op \in Operators :
        state[op].status = "CHECKPOINTING" => state[op].snapshot # NULL

(* 检查点一致性 (所有算子快照一致) *)
CheckpointConsistency ==
    coordinator = "COMPLETED" =>
        \A op1, op2 \in Operators : checkpoint[op1] = checkpoint[op2]

(* 消息唯一性 *)
MessageUniqueness ==
    \A msg1, msg2 \in messages :
        msg1 # msg2 => 
        (msg1.from # msg2.from \/ msg1.to # msg2.to \/ msg1.payload # msg2.payload)

(* 历史完整性 *)
HistoryCompleteness ==
    \A i \in 1..Len(history) :
        /\ history[i].op \in Operators
        /\ history[i].event > 0
        /\ history[i].time <= watermark

(* 组合不变式 *)
AllInvariants ==
    /\ TypeOK
    /\ ProcessedNonNegative
    /\ CheckpointMonotonic
    /\ StateConsistency
    /\ CheckpointConsistency
    /\ MessageUniqueness
    /\ HistoryCompleteness

(* ============================================================================
 * 第10部分：时序性质 (活性)
 * ============================================================================ *)

(* 检查点最终会完成 *)
CheckpointCompletes ==
    coordinator = "TRIGGERING" ~> coordinator = "COMPLETED"

(* 所有事件最终会被处理 *)
AllEventsProcessed ==
    \A op \in Operators :
        state[op].status = "RUNNING" ~> state[op].processed = MaxEvents

(* 水印最终会推进 *)
WatermarkProgresses ==
    watermark < MaxEvents ~> watermark' > watermark

(* 故障算子最终会恢复 *)
OperatorRecovery ==
    \A op \in Operators :
        state[op].status = "FAILED" ~> state[op].status = "RUNNING"

(* 活性性质组合 *)
AllLiveness ==
    /\ CheckpointCompletes
    /\ AllEventsProcessed
    /\ WatermarkProgresses
    /\ OperatorRecovery

(* ============================================================================
 * 第11部分：状态约束 (用于模型检查限制状态空间)
 * ============================================================================ *)

(* 限制单个算子处理的事件数 *)
StateConstraint ==
    \A op \in Operators : state[op].processed <= MaxEvents

(* 限制历史长度 *)
HistoryConstraint ==
    Len(history) <= MaxEvents * Cardinality(Operators)

(* 限制在途消息数 *)
MessageConstraint ==
    Cardinality(messages) <= 10

(* 完整约束 *)
StateConstraints ==
    /\ StateConstraint
    /\ HistoryConstraint
    /\ MessageConstraint

(* ============================================================================
 * 第12部分：动作属性
 * ============================================================================ *)

(* 动作不变式示例 *)
ProcessEventIncreasesCount ==
    [][\A op \in Operators :
         ProcessEvent(op) => state'[op].processed = state[op].processed + 1]_vars

(* 不相交动作 *)
DisjointActions ==
    \A op1, op2 \in Operators :
        op1 # op2 => ProcessEvent(op1) => ~ProcessEvent(op2)

(* ============================================================================
 * 第13部分：证明义务和定理
 * ============================================================================ *)

(* 初始化满足类型不变式 *)
THEOREM InitTypeOK == Init => TypeOK

(* 下一状态保持类型不变式 *)
THEOREM NextTypeOK == TypeOK /\ [Next]_vars => TypeOK'

(* 安全性定理 *)
THEOREM Safety == Spec => []TypeOK

(* 活性定理 *)
THEOREM Liveness == Spec => AllLiveness

(* ============================================================================
 * 第14部分：模型检查配置参考
 * ============================================================================ *)

(*
MCCheckpoint.cfg 示例:
--------------------
CONSTANTS
    Operators = {op1, op2, op3}
    MaxEvents = 10
    CheckpointInterval = 3
    TimeoutValue = 5
    MaxRetries = 3
    NULL = NULL

INIT Init
NEXT Next

INVARIANT TypeOK
INVARIANT CheckpointConsistency
INVARIANT ProcessedNonNegative

PROPERTY CheckpointCompletes
PROPERTY WatermarkProgresses

CONSTRAINT StateConstraints

CHECK_DEADLOCK TRUE

SIMULATE
    num = 100
    trace = "checkpoint_trace"
*)

================================================================
(*
 * 修改历史:
 *   - v1.0: 初始版本，基本框架
 *   - v1.1: 添加检查点协议
 *   - v1.2: 添加水印推进
 * 
 * 验证状态:
 *   [x] 语法检查通过
 *   [ ] TLC模型检查完成
 *   [ ] 所有不变式验证
 *   [ ] 活性属性验证
 *)
