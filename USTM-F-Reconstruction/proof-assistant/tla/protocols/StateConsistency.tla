------------------------------ MODULE StateConsistency ------------------------------
(*
 * StateConsistency - Flink状态一致性TLA+规约
 * 版本: 1.0.0
 *)

EXTENDS Integers, Sequences, FiniteSets, Naturals, TLC

CONSTANTS
    Operators,
    StateKeys,
    StateValues,
    Checkpoints,
    MaxOperations

ASSUME
    /\ Operators # {}
    /\ IsFiniteSet(Operators)
    /\ StateKeys # {}
    /\ IsFiniteSet(StateKeys)
    /\ StateValues \subseteq Nat
    /\ IsFiniteSet(StateValues)
    /\ Checkpoints \subseteq Nat
    /\ IsFiniteSet(Checkpoints)
    /\ MaxOperations \in Nat /\ MaxOperations > 0

Operator == Operators
Key == StateKeys
Value == StateValues
Checkpoint == Checkpoints

OpType == {"READ", "WRITE", "CLEAR", "SNAPSHOT", "RESTORE"}

VARIABLES
    currentState,
    stateVersions,
    stateBackend,
    pendingWrites,
    checkpointSnapshots,
    lastCheckpointId,
    operationLog,
    snapshotLog,
    isFailed,
    recoveryCheckpoint,
    operationCount,
    committedWrites,
    abortedWrites

GetState(op, key) ==
    IF key \in DOMAIN currentState[op] 
    THEN currentState[op][key]
    ELSE 0

GetVersion(op, key) ==
    IF key \in DOMAIN stateVersions[op]
    THEN stateVersions[op][key]
    ELSE 0

StateExists(op, key) ==
    key \in DOMAIN currentState[op]

CreateSnapshot(op, cp) ==
    [key \in DOMAIN currentState[op] |-> 
        [value |-> currentState[op][key],
         version |-> stateVersions[op][key]]]

Init ==
    /\ currentState = [op \in Operator |-> [k \in {} |-> 0]]
    /\ stateVersions = [op \in Operator |-> [k \in {} |-> 0]]
    /\ stateBackend = [op \in Operator |-> [k \in {} |-> [value |-> 0, version |-> 0]]]
    /\ pendingWrites = [op \in Operator |-> <<>>]
    /\ checkpointSnapshots = [cp \in Checkpoint |-> [op \in Operator |-> [k \in {} |-> 0]]]
    /\ lastCheckpointId = 0
    /\ operationLog = <<>>
    /\ snapshotLog = <<>>
    /\ isFailed = FALSE
    /\ recoveryCheckpoint = 0
    /\ operationCount = 0
    /\ committedWrites = {}
    /\ abortedWrites = {}

ReadState(op, key) ==
    /\ op \in Operator
    /\ key \in Key
    /\ isFailed = FALSE
    /\ operationCount < MaxOperations
    /\ operationLog' = Append(operationLog,
                            [type |-> "READ",
                             op |-> op,
                             key |-> key,
                             value |-> GetState(op, key),
                             version |-> GetVersion(op, key),
                             success |-> TRUE])
    /\ operationCount' = operationCount + 1
    /\ UNCHANGED <<currentState, stateVersions, stateBackend, pendingWrites,
                   checkpointSnapshots, lastCheckpointId, snapshotLog, isFailed,
                   recoveryCheckpoint, committedWrites, abortedWrites>>

WriteState(op, key, value) ==
    /\ op \in Operator
    /\ key \in Key
    /\ value \in Value
    /\ isFailed = FALSE
    /\ operationCount < MaxOperations
    /\ LET newVersion == GetVersion(op, key) + 1
       IN /\ currentState' = [currentState EXCEPT ![op] = 
                             [@ EXCEPT ![key] = value]]
          /\ stateVersions' = [stateVersions EXCEPT ![op] = 
                              [@ EXCEPT ![key] = newVersion]]
    /\ operationLog' = Append(operationLog,
                            [type |-> "WRITE",
                             op |-> op,
                             key |-> key,
                             value |-> value,
                             version |-> stateVersions'[op][key],
                             success |-> TRUE])
    /\ committedWrites' = committedWrites \union {[op |-> op, key |-> key, value |-> value]}
    /\ operationCount' = operationCount + 1
    /\ UNCHANGED <<stateBackend, pendingWrites, checkpointSnapshots,
                   lastCheckpointId, snapshotLog, isFailed, recoveryCheckpoint,
                   abortedWrites>>

ClearState(op, key) ==
    /\ op \in Operator
    /\ key \in Key
    /\ isFailed = FALSE
    /\ operationCount < MaxOperations
    /\ currentState' = [currentState EXCEPT ![op] = 
                     [k \in DOMAIN @ \ {key} |-> @[k]]]
    /\ stateVersions' = [stateVersions EXCEPT ![op] = 
                        [k \in DOMAIN @ \ {key} |-> @[k]]]
    /\ operationLog' = Append(operationLog,
                            [type |-> "CLEAR",
                             op |-> op,
                             key |-> key,
                             value |-> 0,
                             version |-> 0,
                             success |-> TRUE])
    /\ operationCount' = operationCount + 1
    /\ UNCHANGED <<stateBackend, pendingWrites, checkpointSnapshots,
                   lastCheckpointId, snapshotLog, isFailed, recoveryCheckpoint,
                   committedWrites, abortedWrites>>

CreateCheckpoint(cp) ==
    /\ cp \in Checkpoint
    /\ cp > lastCheckpointId
    /\ isFailed = FALSE
    /\ checkpointSnapshots' = [checkpointSnapshots EXCEPT ![cp] = 
                            [op \in Operator |-> CreateSnapshot(op, cp)]]
    /\ lastCheckpointId' = cp
    /\ snapshotLog' = Append(snapshotLog,
                            [type |-> "SNAPSHOT",
                             cp |-> cp,
                             timestamp |-> operationCount,
                             ops |-> Operators])
    /\ UNCHANGED <<currentState, stateVersions, stateBackend, pendingWrites,
                   operationLog, isFailed, recoveryCheckpoint, operationCount,
                   committedWrites, abortedWrites>>

InjectFailure ==
    /\ isFailed = FALSE
    /\ isFailed' = TRUE
    /\ UNCHANGED <<currentState, stateVersions, stateBackend, pendingWrites,
                   checkpointSnapshots, lastCheckpointId, operationLog,
                   snapshotLog, recoveryCheckpoint, operationCount,
                   committedWrites, abortedWrites>>

RecoverFromCheckpoint(cp) ==
    /\ cp \in Checkpoint
    /\ isFailed = TRUE
    /\ cp <= lastCheckpointId
    /\ checkpointSnapshots[cp] # [op \in Operator |-> [k \in {} |-> 0]]
    /\ currentState' = [op \in Operator |-> 
                       [k \in DOMAIN checkpointSnapshots[cp][op] |-> 
                           checkpointSnapshots[cp][op][k].value]]
    /\ stateVersions' = [op \in Operator |-> 
                        [k \in DOMAIN checkpointSnapshots[cp][op] |-> 
                            checkpointSnapshots[cp][op][k].version]]
    /\ isFailed' = FALSE
    /\ recoveryCheckpoint' = cp
    /\ operationLog' = Append(operationLog,
                            [type |-> "RECOVER",
                             cp |-> cp,
                             timestamp |-> operationCount])
    /\ UNCHANGED <<stateBackend, pendingWrites, checkpointSnapshots,
                   lastCheckpointId, snapshotLog, operationCount,
                   committedWrites, abortedWrites>>

SyncToBackend(op, key) ==
    /\ op \in Operator
    /\ key \in DOMAIN currentState[op]
    /\ stateBackend' = [stateBackend EXCEPT ![op] = 
                      [@ EXCEPT ![key] = 
                          [value |-> currentState[op][key],
                           version |-> stateVersions[op][key]]]]
    /\ UNCHANGED <<currentState, stateVersions, pendingWrites,
                   checkpointSnapshots, lastCheckpointId, operationLog,
                   snapshotLog, isFailed, recoveryCheckpoint, operationCount,
                   committedWrites, abortedWrites>>

Next ==
    \/ \E op \in Operator, key \in Key : ReadState(op, key)
    \/ \E op \in Operator, key \in Key, value \in Value : WriteState(op, key, value)
    \/ \E op \in Operator, key \in Key : ClearState(op, key)
    \/ \E cp \in Checkpoint : CreateCheckpoint(cp)
    \/ InjectFailure
    \/ \E cp \in Checkpoint : RecoverFromCheckpoint(cp)
    \/ \E op \in Operator, key \in Key : SyncToBackend(op, key)

Fairness ==
    /\ WF_vars(InjectFailure)
    /\ \A cp \in Checkpoint : WF_vars(RecoverFromCheckpoint(cp))
    /\ \A op \in Operator, key \in Key : WF_vars(SyncToBackend(op, key))

Spec == Init /\ [][Next]_vars /\ Fairness

TypeInvariant ==
    /\ currentState \in [Operator -> [Key -> Value]]
    /\ stateVersions \in [Operator -> [Key -> Nat]]
    /\ isFailed \in BOOLEAN
    /\ lastCheckpointId \in Nat

VersionMonotonicity ==
    \A op \in Operator, key \in Key :
        stateVersions[op][key] >= 0

CheckpointSnapshotValidity ==
    \A cp \in Checkpoint, op \in Operator :
        cp <= lastCheckpointId =>
            \A key \in DOMAIN checkpointSnapshots[cp][op] :
                checkpointSnapshots[cp][op][key].version <= stateVersions[op][key]

StateConsistencyInvariant ==
    \A op \in Operator, key \in DOMAIN currentState[op] :
        stateBackend[op][key].value = currentState[op][key] \/ 
        stateBackend[op][key].version < stateVersions[op][key]

FailureRequiresRecovery ==
    isFailed = TRUE => recoveryCheckpoint <= lastCheckpointId

ReadYourWrites ==
    \A i, j \in 1..Len(operationLog) :
        /\ i < j
        /\ operationLog[i].type = "WRITE"
        /\ operationLog[j].type = "READ"
        /\ operationLog[i].op = operationLog[j].op
        /\ operationLog[i].key = operationLog[j].key
        /\ (~ \E k \in i+1..j-1 :
                operationLog[k].type = "WRITE" /\ 
                operationLog[k].op = operationLog[i].op /\ 
                operationLog[k].key = operationLog[i].key)
        => operationLog[j].value = operationLog[i].value

MonotonicReads ==
    \A i, j \in 1..Len(operationLog) :
        /\ i < j
        /\ operationLog[i].type = "READ"
        /\ operationLog[j].type = "READ"
        /\ operationLog[i].op = operationLog[j].op
        /\ operationLog[i].key = operationLog[j].key
        => operationLog[j].version >= operationLog[i].version

RecoveryConsistency ==
    \A i \in 1..Len(operationLog) :
        operationLog[i].type = "RECOVER" =>
            LET cp == operationLog[i].cp
            IN \A op \in Operator, key \in Key :
                GetState(op, key) = 
                    IF key \in DOMAIN checkpointSnapshots[cp][op]
                    THEN checkpointSnapshots[cp][op][key].value
                    ELSE 0

WriteAtomicity ==
    \A w \in committedWrites :
        \E i \in 1..Len(operationLog) :
            operationLog[i].type = "WRITE" /\ 
            operationLog[i].op = w.op /\ 
            operationLog[i].key = w.key /\ 
            operationLog[i].value = w.value /\ 
            operationLog[i].success = TRUE

Isolation ==
    \A cp \in Checkpoint, op \in Operator, key \in Key :
        cp <= lastCheckpointId /\ key \in DOMAIN checkpointSnapshots[cp][op] =>
            checkpointSnapshots[cp][op][key] = 
                checkpointSnapshots[cp][op][key]

EventuallyVisible ==
    \A w \in committedWrites :
        <> (\E op \in Operator, key \in Key :
                currentState[op][key] = w.value)

EventualRecovery ==
    isFailed = TRUE ~> isFailed = FALSE

EventualCheckpoint ==
    []<> (lastCheckpointId > 0)

vars == <<currentState, stateVersions, stateBackend, pendingWrites,
          checkpointSnapshots, lastCheckpointId, operationLog, snapshotLog,
          isFailed, recoveryCheckpoint, operationCount, committedWrites,
          abortedWrites>>

================================================================================
