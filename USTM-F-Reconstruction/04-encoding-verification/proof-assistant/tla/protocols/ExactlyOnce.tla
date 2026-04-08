---- MODULE ExactlyOnce ----

EXTENDS Naturals, Sequences, FiniteSets

CONSTANTS Transactions, Participants, Coordinator

VARIABLES txState,
          participantState,
          decisions,
          prePrepared

TxStatus == {"ACTIVE", "PREPARING", "PREPARED", "COMMITTING", 
             "COMMITTED", "ABORTING", "ABORTED"}

ParticipantStatus == {"IDLE", "PREPARED", "COMMITTED", "ABORTED"}

Init ==
  /\ txState = [t \in Transactions |-> "ACTIVE"]
  /\ participantState = [t \in Transactions, p \in Participants |-> "IDLE"]
  /\ decisions = [t \in Transactions |-> NULL]
  /\ prePrepared = [t \in Transactions |-> {}]

Prepare(tx, p) ==
  /\ txState[tx] = "PREPARING"
  /\ participantState[tx, p] = "IDLE"
  /\ participantState' = [participantState EXCEPT ![tx, p] = "PREPARED"]
  /\ prePrepared' = [prePrepared EXCEPT ![tx] = @ \union {p}]
  /\ UNCHANGED <<txState, decisions>>

CollectVotes(tx) ==
  /\ txState[tx] = "PREPARING"
  /\ prePrepared[tx] = Participants
  /\ txState' = [txState EXCEPT ![tx] = "PREPARED"]
  /\ UNCHANGED <<participantState, decisions, prePrepared>>

DecideCommit(tx) ==
  /\ txState[tx] = "PREPARED"
  /\ decisions' = [decisions EXCEPT ![tx] = "COMMIT"]
  /\ txState' = [txState EXCEPT ![tx] = "COMMITTING"]
  /\ UNCHANGED <<participantState, prePrepared>>

DecideAbort(tx) ==
  /\ txState[tx] \in {"PREPARING", "PREPARED"}
  /\ decisions' = [decisions EXCEPT ![tx] = "ABORT"]
  /\ txState' = [txState EXCEPT ![tx] = "ABORTING"]
  /\ UNCHANGED <<participantState, prePrepared>>

Commit(tx, p) ==
  /\ txState[tx] = "COMMITTING"
  /\ participantState[tx, p] = "PREPARED"
  /\ participantState' = [participantState EXCEPT ![tx, p] = "COMMITTED"]
  /\ UNCHANGED <<txState, decisions, prePrepared>>

Next ==
  /\ \E tx \in Transactions, p \in Participants : Prepare(tx, p)
  /\ \E tx \in Transactions : CollectVotes(tx)
  /\ \E tx \in Transactions : DecideCommit(tx)
  /\ \E tx \in Transactions : DecideAbort(tx)
  /\ \E tx \in Transactions, p \in Participants : Commit(tx, p)

Spec == Init /\ [][Next]_<<txState, participantState, decisions, prePrepared>>

====
