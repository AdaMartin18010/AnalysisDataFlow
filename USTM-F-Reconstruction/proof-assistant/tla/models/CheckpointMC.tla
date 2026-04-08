------------------------------- MODULE CheckpointMC -------------------------------
(*
 * CheckpointMC - CheckpointCoordinator模型检验实例
 * 用于TLC模型检验器验证检查点协议
 *)

EXTENDS CheckpointCoordinator

CONSTANTS
    t1, t2, t3

MC_Tasks == {t1, t2, t3}
MC_MaxCheckpointId == 2
MC_MaxAttempts == 2
MC_TimeoutPeriod == 5

MC_Init ==
    /\ coordinatorState = [cpId \in 1..MC_MaxCheckpointId |-> "IDLE"]
    /\ coordinatorAcks = [cpId \in 1..MC_MaxCheckpointId |-> {}]
    /\ coordinatorStartTime = [cpId \in 1..MC_MaxCheckpointId |-> 0]
    /\ currentCheckpoint = 1
    /\ taskStates = [t \in MC_Tasks |-> [cpId \in 1..MC_MaxCheckpointId |-> "NONE"]]
    /\ taskSnapshots = [t \in MC_Tasks |-> [cpId \in 1..MC_MaxCheckpointId |-> 0]]
    /\ triggerChannel = <<>>
    /\ ackChannel = <<>>
    /\ globalClock = 0
    /\ completedCheckpoints = {}
    /\ failedCheckpoints = {}

MC_Next ==
    \/ \E cpId \in 1..MC_MaxCheckpointId : 
        /\ cpId = currentCheckpoint
        /\ coordinatorState[cpId] = "IDLE"
        /\ coordinatorState' = [coordinatorState EXCEPT ![cpId] = "TRIGGERED"]
        /\ coordinatorStartTime' = [coordinatorStartTime EXCEPT ![cpId] = globalClock]
        /\ triggerChannel' = Append(triggerChannel, 
                                   [type |-> "TRIGGER", 
                                    cpId |-> cpId, 
                                    timestamp |-> globalClock,
                                    tasks |-> MC_Tasks])
        /\ UNCHANGED <<coordinatorAcks, currentCheckpoint, taskStates, 
                       taskSnapshots, ackChannel, globalClock,
                       completedCheckpoints, failedCheckpoints>>
    \/ \E t \in MC_Tasks, cpId \in 1..MC_MaxCheckpointId : 
        /\ taskStates[t][cpId] = "NONE"
        /\ \E i \in 1..Len(triggerChannel) :
            /\ triggerChannel[i].type = "TRIGGER"
            /\ triggerChannel[i].cpId = cpId
            /\ t \in triggerChannel[i].tasks
            /\ taskStates' = [taskStates EXCEPT ![t] = 
                             [@ EXCEPT ![cpId] = "RECEIVED"]]
            /\ triggerChannel' = Remove(triggerChannel, i)
        /\ UNCHANGED <<coordinatorState, coordinatorAcks, coordinatorStartTime,
                       currentCheckpoint, taskSnapshots, ackChannel, globalClock,
                       completedCheckpoints, failedCheckpoints>>
    \/ \E t \in MC_Tasks, cpId \in 1..MC_MaxCheckpointId : 
        /\ taskStates[t][cpId] = "RECEIVED"
        /\ taskStates' = [taskStates EXCEPT ![t] = 
                         [@ EXCEPT ![cpId] = "SNAPSHOTTING"]]
        /\ taskSnapshots' = [taskSnapshots EXCEPT ![t] = 
                            [@ EXCEPT ![cpId] = globalClock]]
        /\ UNCHANGED <<coordinatorState, coordinatorAcks, coordinatorStartTime,
                       currentCheckpoint, triggerChannel, ackChannel, globalClock,
                       completedCheckpoints, failedCheckpoints>>
    \/ \E t \in MC_Tasks, cpId \in 1..MC_MaxCheckpointId : 
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
    \/ \E cpId \in 1..MC_MaxCheckpointId : 
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
    \/ \E cpId \in 1..MC_MaxCheckpointId : 
        /\ coordinatorState[cpId] = "WAITING_ACKS"
        /\ coordinatorAcks[cpId] = MC_Tasks
        /\ coordinatorState' = [coordinatorState EXCEPT ![cpId] = "COMPLETED"]
        /\ currentCheckpoint' = IF cpId < MC_MaxCheckpointId THEN cpId + 1 ELSE cpId
        /\ completedCheckpoints' = completedCheckpoints \union {cpId}
        /\ UNCHANGED <<coordinatorAcks, coordinatorStartTime, taskStates,
                       taskSnapshots, triggerChannel, ackChannel, globalClock,
                       failedCheckpoints>>
    \/ \E cpId \in 1..MC_MaxCheckpointId : 
        /\ coordinatorState[cpId] = "WAITING_ACKS"
        /\ globalClock - coordinatorStartTime[cpId] > MC_TimeoutPeriod
        /\ coordinatorState' = [coordinatorState EXCEPT ![cpId] = "EXPIRED"]
        /\ failedCheckpoints' = failedCheckpoints \union {cpId}
        /\ currentCheckpoint' = IF cpId < MC_MaxCheckpointId THEN cpId + 1 ELSE cpId
        /\ UNCHANGED <<coordinatorAcks, coordinatorStartTime, taskStates,
                       taskSnapshots, triggerChannel, ackChannel, globalClock,
                       completedCheckpoints>>
    \/ /\ globalClock' = globalClock + 1
       /\ UNCHANGED <<coordinatorState, coordinatorAcks, coordinatorStartTime,
                      currentCheckpoint, taskStates, taskSnapshots, 
                      triggerChannel, ackChannel, completedCheckpoints, 
                      failedCheckpoints>>

MC_Spec == MC_Init /\ [][MC_Next]_vars

MC_TypeInvariant ==
    /\ coordinatorState \in [1..MC_MaxCheckpointId -> CPState]
    /\ coordinatorAcks \in [1..MC_MaxCheckpointId -> SUBSET MC_Tasks]
    /\ currentCheckpoint \in 1..MC_MaxCheckpointId
    /\ taskStates \in [MC_Tasks -> [1..MC_MaxCheckpointId -> TaskCPState]]

MC_Completeness ==
    <> (1 \in completedCheckpoints)

MC_NoDeadlock ==
    [] (ENABLED MC_Next)

================================================================================
