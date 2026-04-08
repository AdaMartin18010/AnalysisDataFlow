---- MODULE CheckpointCoordinator ----

EXTENDS Naturals, Sequences, FiniteSets, TLC

CONSTANTS Tasks, 
          MaxCheckpointId

VARIABLES checkpointId,
          pendingCheckpoints,
          completedCheckpoints,
          taskAcks

CheckpointStatus == {"TRIGGERED", "ACKS_PENDING", "COMPLETED", "FAILED"}

Init ==
  /\ checkpointId = 0
  /\ pendingCheckpoints = {}
  /\ completedCheckpoints = {}
  /\ taskAcks = [t \in Tasks |-> 0]

TriggerCheckpoint ==
  /\ checkpointId < MaxCheckpointId
  /\ checkpointId' = checkpointId + 1
  /\ pendingCheckpoints' = pendingCheckpoints \union
      {[id |-> checkpointId + 1,
        status |-> "TRIGGERED",
        acks |-> {}]}
  /\ UNCHANGED <<completedCheckpoints, taskAcks>>

ReceiveAck(task, cpId) ==
  /\ \E cp \in pendingCheckpoints :
       /\ cp.id = cpId
       /\ cp.status \in {"TRIGGERED", "ACKS_PENDING"}
  /\ taskAcks' = [taskAcks EXCEPT ![task] = cpId]
  /\ pendingCheckpoints' = 
       {IF cp.id = cpId
        THEN [cp EXCEPT !.acks = cp.acks \union {task},
                        !.status = IF cp.acks \union {task} = Tasks
                                   THEN "COMPLETED"
                                   ELSE "ACKS_PENDING"]
        ELSE cp : cp \in pendingCheckpoints}
  /\ UNCHANGED <<checkpointId, completedCheckpoints>>

CompleteCheckpoint(cpId) ==
  /\ \E cp \in pendingCheckpoints :
       /\ cp.id = cpId
       /\ cp.status = "COMPLETED"
  /\ completedCheckpoints' = completedCheckpoints \union {cpId}
  /\ pendingCheckpoints' = pendingCheckpoints \\n       {cp \in pendingCheckpoints : cp.id = cpId}
  /\ UNCHANGED <<checkpointId, taskAcks>>

Next ==
  /\ TriggerCheckpoint
  /\ \E t \in Tasks, cid \in 1..MaxCheckpointId : ReceiveAck(t, cid)
  /\ \E cid \in 1..MaxCheckpointId : CompleteCheckpoint(cid)

Spec == Init /\ [][Next]_<<checkpointId, pendingCheckpoints, 
                                 completedCheckpoints, taskAcks>>

====
