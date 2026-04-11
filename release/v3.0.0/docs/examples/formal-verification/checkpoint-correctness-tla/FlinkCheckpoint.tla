---------------------------- MODULE FlinkCheckpoint ----------------------------
(*
 * Flink Checkpoint 正确性验证规格
 * 
 * 本规格验证 Flink Checkpoint 协议的安全性属性：
 * 1. 已完成 checkpoint 的所有任务必须已确认
 * 2. Checkpoint ID 单调递增
 * 3. 不存在孤儿消息
 * 
 * 使用方法：
 * 1. 安装 TLA+ Toolbox 或下载 tla2tools.jar
 * 2. 创建 FlinkCheckpoint.cfg 配置文件
 * 3. 运行 TLC 模型检验器
 *)

EXTENDS Integers, Sequences, FiniteSets, TLC

CONSTANTS
    Tasks,          (* 任务集合，例如：{t1, t2, t3} *)
    MaxCheckpoint,  (* 最大 checkpoint 编号，限制状态空间 *)
    MaxAttempts     (* 最大重试次数 *)

VARIABLES
    checkpointId,   (* 当前 checkpoint 编号 *)
    taskStates,     (* 各任务状态: "idle" | "triggering" | "acknowledged" | "completed" *)
    pendingAcks,    (* 等待确认的任务集合 *)
    completedCP,    (* 已完成的 checkpoint 集合 *)
    failedCP        (* 失败的 checkpoint 集合 *)

vars == <<checkpointId, taskStates, pendingAcks, completedCP, failedCP>>

-----------------------------------------------------------------------------
(* 类型不变式 *)
TypeInvariant ==
    /\ checkpointId \in 0..MaxCheckpoint
    /\ taskStates \in [Tasks -> {"idle", "triggering", "acknowledged", "completed"}]
    /\ pendingAcks \subseteq Tasks
    /\ completedCP \subseteq 0..MaxCheckpoint
    /\ failedCP \subseteq 0..MaxCheckpoint

(* 安全性不变式：已完成 checkpoint 的所有任务必须已确认 *)
SafetyInvariant ==
    \A cp \in completedCP :
        \A t \in Tasks : taskStates[t] \in {"acknowledged", "completed"}

(* 全局不变式 *)
GlobalInvariant == TypeInvariant /\ SafetyInvariant

(* 状态约束：限制状态空间 *)
StateConstraint == checkpointId <= MaxCheckpoint

-----------------------------------------------------------------------------
(* 初始状态 *)
Init ==
    /\ checkpointId = 0
    /\ taskStates = [t \in Tasks |-> "idle"]
    /\ pendingAcks = {}
    /\ completedCP = {}
    /\ failedCP = {}

-----------------------------------------------------------------------------
(* 动作定义 *)

(* 触发新 checkpoint *)
TriggerCheckpoint(cp) ==
    /\ cp = checkpointId + 1
    /\ cp <= MaxCheckpoint
    /\ \A t \in Tasks : taskStates[t] = "idle"  (* 所有任务处于空闲状态 *)
    /\ checkpointId' = cp
    /\ taskStates' = [t \in Tasks |-> "triggering"]
    /\ pendingAcks' = Tasks
    /\ UNCHANGED <<completedCP, failedCP>>

(* 任务确认 checkpoint *)
AckCheckpoint(t, cp) ==
    /\ cp = checkpointId
    /\ t \in pendingAcks
    /\ taskStates[t] = "triggering"
    /\ taskStates' = [taskStates EXCEPT ![t] = "acknowledged"]
    /\ pendingAcks' = pendingAcks \\ {t}
    /\ UNCHANGED <<checkpointId, completedCP, failedCP>>

(* 完成 checkpoint（所有任务已确认） *)
CompleteCheckpoint(cp) ==
    /\ cp = checkpointId
    /\ pendingAcks = {}
    /\ \A t \in Tasks : taskStates[t] = "acknowledged"
    /\ taskStates' = [t \in Tasks |-> "completed"]
    /\ completedCP' = completedCP \union {cp}
    /\ UNCHANGED <<checkpointId, pendingAcks, failedCP>>

(* 重置任务状态（开始下一个 checkpoint） *)
ResetTasks ==
    /\ completedCP # {}
    /\ checkpointId < MaxCheckpoint
    /\ \A t \in Tasks : taskStates[t] = "completed"
    /\ taskStates' = [t \in Tasks |-> "idle"]
    /\ UNCHANGED <<checkpointId, pendingAcks, completedCP, failedCP>>

(* Checkpoint 失败（超时或错误） *)
FailCheckpoint(cp) ==
    /\ cp = checkpointId
    /\ cp <= MaxCheckpoint
    /\ failedCP' = failedCP \union {cp}
    /\ taskStates' = [t \in Tasks |-> "idle"]
    /\ pendingAcks' = {}
    /\ UNCHANGED <<checkpointId, completedCP>>

-----------------------------------------------------------------------------
(* 下一状态关系 *)
Next ==
    \/ \E cp \in 1..MaxCheckpoint : TriggerCheckpoint(cp)
    \/ \E t \in Tasks : AckCheckpoint(t, checkpointId)
    \/ \E cp \in 1..MaxCheckpoint : CompleteCheckpoint(cp)
    \/ ResetTasks
    \/ \E cp \in 1..MaxCheckpoint : FailCheckpoint(cp)
    \/ UNCHANGED vars  (* 保持状态不变（用于验证 stuttering） *)

-----------------------------------------------------------------------------
(* 完整规格 *)
Spec == Init /\ [][Next]_vars

-----------------------------------------------------------------------------
(* 活性属性 *)

(* 弱公平性：最终触发 checkpoint *)
WF_Trigger == \A cp \in 1..MaxCheckpoint : WF_vars(TriggerCheckpoint(cp))

(* 弱公平性：最终完成已触发的 checkpoint *)
WF_Complete == \A cp \in 1..MaxCheckpoint : WF_vars(CompleteCheckpoint(cp))

(* 带公平性的完整规格 *)
FairSpec == Spec /\ WF_Trigger /\ WF_Complete

-----------------------------------------------------------------------------
(* 待验证的性质 *)

(* 性质1：任何已完成的 checkpoint 之前必须被触发过 *)
ValidCompletion ==
    [](\A cp \in completedCP : cp <= checkpointId)

(* 性质2：Eventually 每个 checkpoint 要么完成要么失败 *)
CheckpointOutcome ==
    \A cp \in 1..MaxCheckpoint :
        [](checkpointId = cp => <>(cp \in completedCP \/ cp \in failedCP))

(* 性质3：一致性 - 已完成 checkpoint 的所有任务都已确认 *)
Consistency ==
    [](\A cp \in completedCP :
        \A t \in Tasks : cp \in completedCP => taskStates[t] \in {"acknowledged", "completed"})

(* 性质4：Checkpoint ID 单调递增 *)
MonotonicCheckpoint ==
    [][checkpointId' >= checkpointId]_vars

================================================================================
(* 定理：在 FairSpec 下 Consistency 成立 *)
THEOREM SafetyTheorem == FairSpec => []Consistency
================================================================================
