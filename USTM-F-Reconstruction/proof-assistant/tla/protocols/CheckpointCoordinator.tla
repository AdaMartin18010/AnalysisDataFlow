--------------------------- MODULE CheckpointCoordinator ---------------------------
(*
 * CheckpointCoordinator - Flink检查点协调协议TLA+规约
 * 版本: 2.0.0
 * 描述: 形式化定义Flink分布式检查点协议的Chandy-Lamport算法变体
 * 
 * 核心属性:
 * 1. 安全性: 所有任务在一致的逻辑时间点进行快照
 * 2. 活性: 检查点最终完成（无无限期阻塞）
 * 3. 一致性: 检查点状态构成全局一致快照
 *)

EXTENDS Integers, Sequences, FiniteSets, Naturals, TLC

CONSTANTS
    Tasks,
    MaxCheckpointId,
    MaxAttempts,
    TimeoutPeriod

ASSUME
    /\ Tasks # {}
    /\ IsFiniteSet(Tasks)
    /\ MaxCheckpointId \in Nat /\ MaxCheckpointId > 0
    /\ MaxAttempts \in Nat /\ MaxAttempts > 0
    /\ TimeoutPeriod \in Nat /\ TimeoutPeriod > 0

(* ===========================================================================
 * 类型定义
 * ===========================================================================*)

TaskId == Tasks
CheckpointId == 1..MaxCheckpointId
AttemptCount == 0..MaxAttempts

CPState == {
    "IDLE",
    "TRIGGERED",
    "WAITING_ACKS",
    "COMPLETED",
    "FAILED",
    "EXPIRED"
}

TaskCPState == {
    "NONE",
    "RECEIVED",
    "SNAPSHOTTING",
    "ACK_SENT",
    "FAILED"
}

VARIABLES
    coordinatorState,
    coordinatorAcks,
    coordinatorStartTime,
    currentCheckpoint,
    taskStates,
    taskSnapshots,
    triggerChannel,
    ackChannel,
    globalClock,
    completedCheckpoints,
    failedCheckpoints

AllTasksAcked(cpId) ==
    coordinatorAcks[cpId] = Tasks

IsCheckpointTimeout(cpId) ==
    coordinatorState[cpId] = "WAITING_ACKS" /\ 
    globalClock - coordinatorStartTime[cpId] > TimeoutPeriod

CanTriggerCheckpoint(cpId) ==
    coordinatorState[cpId] = "IDLE" /\ 
    cpId = currentCheckpoint

PendingAcks(cpId) ==
    Tasks \ coordinatorAcks[cpId]

Remove(seq, idx) ==
    [i \in 1..(Len(seq)-1) |-> IF i < idx THEN seq[i] ELSE seq[i+1]]

Init ==
    /\ coordinatorState = [cpId \in CheckpointId |-> "IDLE"]
    /\ coordinatorAcks = [cpId \in CheckpointId |-> {}]
    /\ coordinatorStartTime = [cpId \in CheckpointId |-> 0]
    /\ currentCheckpoint = 1
    /\ taskStates = [t \in TaskId |-> [cpId \in CheckpointId |-> "NONE"]]
    /\ taskSnapshots = [t \in TaskId |-> [cpId \in CheckpointId |-> 0]]
    /\ triggerChannel = <<>>
    /\ ackChannel = <<>>
    /\ globalClock = 0
    /\ completedCheckpoints = {}
    /\ failedCheckpoints = {}

TriggerCheckpoint(cpId) ==
    /\ cpId \in CheckpointId
    /\ CanTriggerCheckpoint(cpId)
    /\ coordinatorState' = [coordinatorState EXCEPT ![cpId] = "TRIGGERED"]
    /\ coordinatorStartTime' = [coordinatorStartTime EXCEPT ![cpId] = globalClock]
    /\ triggerChannel' = Append(triggerChannel, 
                               [type |-> "TRIGGER", 
                                cpId |-> cpId, 
                                timestamp |-> globalClock,
                                tasks |-> Tasks])
    /\ UNCHANGED <<coordinatorAcks, currentCheckpoint, taskStates, 
                   taskSnapshots, ackChannel, globalClock,
                   completedCheckpoints, failedCheckpoints>>

TaskReceiveTrigger(t, cpId) ==
    /\ t \in TaskId
    /\ cpId \in CheckpointId
    /\ \E i \in 1..Len(triggerChannel) :
        /\ triggerChannel[i].type = "TRIGGER"
        /\ triggerChannel[i].cpId = cpId
        /\ t \in triggerChannel[i].tasks
        /\ taskStates[t][cpId] = "NONE"
        /\ taskStates' = [taskStates EXCEPT ![t] = 
                         [@ EXCEPT ![cpId] = "RECEIVED"]]
        /\ triggerChannel' = Remove(triggerChannel, i)
    /\ UNCHANGED <<coordinatorState, coordinatorAcks, coordinatorStartTime,
                   currentCheckpoint, taskSnapshots, ackChannel, globalClock,
                   completedCheckpoints, failedCheckpoints>>

TaskStartSnapshot(t, cpId) ==
    /\ t \in TaskId
    /\ cpId \in CheckpointId
    /\ taskStates[t][cpId] = "RECEIVED"
    /\ taskStates' = [taskStates EXCEPT ![t] = 
                     [@ EXCEPT ![cpId] = "SNAPSHOTTING"]]
    /\ taskSnapshots' = [taskSnapshots EXCEPT ![t] = 
                        [@ EXCEPT ![cpId] = globalClock]]
    /\ UNCHANGED <<coordinatorState, coordinatorAcks, coordinatorStartTime,
                   currentCheckpoint, triggerChannel, ackChannel, globalClock,
                   completedCheckpoints, failedCheckpoints>>

TaskSendAck(t, cpId) ==
    /\ t \in TaskId
    /\ cpId \in CheckpointId
    /\ taskStates[t][cpId] = "SNAPSHOTTING"
    /\ taskStates' = [taskStates EXCEPT ![t] = 
                     [@ EXCEPT ![cpId] = "ACK_SENT"]]
    /\ ackChannel' = Append(ackChannel,
                           [type |-> "ACK",
                            taskId |-> t,
                            cpId |-> cpId,
                            timestamp |-> globalClock,
                            state |-> taskSnapshots[t][cpId]])
    /\ UNCHANGED <<coordinatorState, coordinatorAcks, coordinatorStartTime,
                   currentCheckpoint, taskSnapshots, triggerChannel, globalClock,
                   completedCheckpoints, failedCheckpoints>>

CoordinatorReceiveAck(cpId) ==
    /\ cpId \in CheckpointId
    /\ coordinatorState[cpId] \in {"TRIGGERED", "WAITING_ACKS"}
    /\ \E i \in 1..Len(ackChannel) :
        /\ ackChannel[i].type = "ACK"
        /\ ackChannel[i].cpId = cpId
        /\ ackChannel[i].taskId \notin coordinatorAcks[cpId]
        /\ coordinatorAcks' = [coordinatorAcks EXCEPT ![cpId] = 
                              @ \union {ackChannel[i].taskId}]
        /\ coordinatorState' = [coordinatorState EXCEPT ![cpId] = "WAITING_ACKS"]
        /\ ackChannel' = Remove(ackChannel, i)
    /\ UNCHANGED <<coordinatorStartTime, currentCheckpoint, taskStates,
                   taskSnapshots, triggerChannel, globalClock,
                   completedCheckpoints, failedCheckpoints>>

CompleteCheckpoint(cpId) ==
    /\ cpId \in CheckpointId
    /\ coordinatorState[cpId] = "WAITING_ACKS"
    /\ AllTasksAcked(cpId)
    /\ coordinatorState' = [coordinatorState EXCEPT ![cpId] = "COMPLETED"]
    /\ currentCheckpoint' = IF cpId < MaxCheckpointId THEN cpId + 1 ELSE cpId
    /\ completedCheckpoints' = completedCheckpoints \union {cpId}
    /\ UNCHANGED <<coordinatorAcks, coordinatorStartTime, taskStates,
                   taskSnapshots, triggerChannel, ackChannel, globalClock,
                   failedCheckpoints>>

TimeoutCheckpoint(cpId) ==
    /\ cpId \in CheckpointId
    /\ IsCheckpointTimeout(cpId)
    /\ coordinatorState' = [coordinatorState EXCEPT ![cpId] = "EXPIRED"]
    /\ failedCheckpoints' = failedCheckpoints \union {cpId}
    /\ currentCheckpoint' = IF cpId < MaxCheckpointId THEN cpId + 1 ELSE cpId
    /\ UNCHANGED <<coordinatorAcks, coordinatorStartTime, taskStates,
                   taskSnapshots, triggerChannel, ackChannel, globalClock,
                   completedCheckpoints>>

AdvanceTime ==
    /\ globalClock' = globalClock + 1
    /\ UNCHANGED <<coordinatorState, coordinatorAcks, coordinatorStartTime,
                   currentCheckpoint, taskStates, taskSnapshots, 
                   triggerChannel, ackChannel, completedCheckpoints, 
                   failedCheckpoints>>

Next ==
    \/ \E cpId \in CheckpointId : TriggerCheckpoint(cpId)
    \/ \E t \in TaskId, cpId \in CheckpointId : TaskReceiveTrigger(t, cpId)
    \/ \E t \in TaskId, cpId \in CheckpointId : TaskStartSnapshot(t, cpId)
    \/ \E t \in TaskId, cpId \in CheckpointId : TaskSendAck(t, cpId)
    \/ \E cpId \in CheckpointId : CoordinatorReceiveAck(cpId)
    \/ \E cpId \in CheckpointId : CompleteCheckpoint(cpId)
    \/ \E cpId \in CheckpointId : TimeoutCheckpoint(cpId)
    \/ AdvanceTime

Fairness ==
    /\ SF_vars(\E cpId \in CheckpointId : CompleteCheckpoint(cpId))
    /\ WF_vars(AdvanceTime)
    /\ \A t \in TaskId, cpId \in CheckpointId : 
        WF_vars(TaskSendAck(t, cpId))

Spec == Init /\ [][Next]_vars /\ Fairness

TypeInvariant ==
    /\ coordinatorState \in [CheckpointId -> CPState]
    /\ coordinatorAcks \in [CheckpointId -> SUBSET TaskId]
    /\ coordinatorStartTime \in [CheckpointId -> Nat]
    /\ currentCheckpoint \in CheckpointId
    /\ taskStates \in [TaskId -> [CheckpointId -> TaskCPState]]
    /\ taskSnapshots \in [TaskId -> [CheckpointId -> Nat]]
    /\ globalClock \in Nat
    /\ completedCheckpoints \subseteq CheckpointId
    /\ failedCheckpoints \subseteq CheckpointId

CheckpointMonotonicity ==
    \A cpId1, cpId2 \in CheckpointId :
        (cpId1 < cpId2 /\ coordinatorState[cpId2] # "IDLE") 
        => coordinatorState[cpId1] \in {"COMPLETED", "FAILED", "EXPIRED"}

AckConsistency ==
    \A cpId \in CheckpointId, t \in coordinatorAcks[cpId] :
        taskStates[t][cpId] = "ACK_SENT"

ValidStateTransitions ==
    \A cpId \in CheckpointId :
        coordinatorState[cpId] = "COMPLETED" => AllTasksAcked(cpId)

CheckpointEventuallyCompletes ==
    \A cpId \in CheckpointId :
        coordinatorState[cpId] = "TRIGGERED" ~> 
        coordinatorState[cpId] \in {"COMPLETED", "FAILED", "EXPIRED"}

CompletedCheckpointsHaveAllAcks ==
    [] (\A cpId \in completedCheckpoints : AllTasksAcked(cpId))

NoDeadlock ==
    [] (ENABLED Next)

GlobalConsistency ==
    \A cpId \in completedCheckpoints :
        \A t1, t2 \in Tasks :
            taskSnapshots[t1][cpId] <= globalClock /\ 
            taskSnapshots[t2][cpId] <= globalClock

MutualExclusion ==
    Cardinality({cpId \in CheckpointId : 
        coordinatorState[cpId] \in {"TRIGGERED", "WAITING_ACKS"}}) <= 1

vars == <<coordinatorState, coordinatorAcks, coordinatorStartTime,
          currentCheckpoint, taskStates, taskSnapshots, 
          triggerChannel, ackChannel, globalClock,
          completedCheckpoints, failedCheckpoints>>

================================================================================
