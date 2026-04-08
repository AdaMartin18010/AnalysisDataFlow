------------------------------- MODULE ExactlyOnce -------------------------------
(*
 * ExactlyOnce - Flink两阶段提交(2PC)精确一次语义TLA+规约
 * 版本: 2.0.0
 * 描述: 形式化定义分布式事务的两阶段提交协议
 *)

EXTENDS Integers, Sequences, FiniteSets, Naturals, TLC

CONSTANTS
    Participants,
    Transactions,
    MaxRetries,
    CoordinatorId

ASSUME
    /\ Participants # {}
    /\ IsFiniteSet(Participants)
    /\ Transactions # {}
    /\ IsFiniteSet(Transactions)
    /\ MaxRetries \in Nat /\ MaxRetries >= 0
    /\ CoordinatorId \notin Participants

Participant == Participants
Transaction == Transactions
Attempt == 0..MaxRetries

TxState == {
    "ACTIVE",
    "PREPARING",
    "PREPARED",
    "COMMITTING",
    "COMMITTED",
    "ABORTING",
    "ABORTED",
    "HEURISTIC"
}

Vote == {"YES", "NO", "TIMEOUT"}

VARIABLES
    coordState,
    coordVotes,
    coordDecisions,
    participantState,
    participantVotes,
    participantLogs,
    txData,
    txParticipants,
    prepareChannel,
    voteChannel,
    decisionChannel,
    ackChannel,
    committedTxns,
    abortedTxns,
    globalClock,
    outputLog

AllParticipantsVoted(tx) ==
    DOMAIN coordVotes[tx] = txParticipants[tx]

AllYesVotes(tx) ==
    \A p \in txParticipants[tx] : coordVotes[tx][p] = "YES"

HasNoVote(tx) ==
    \E p \in txParticipants[tx] : coordVotes[tx][p] = "NO"

IsTxCompleted(tx) ==
    coordState[tx] \in {"COMMITTED", "ABORTED", "HEURISTIC"}

CanDecide(tx) ==
    /\ coordState[tx] = "PREPARING"
    /\ AllParticipantsVoted(tx)

Remove(seq, idx) ==
    [i \in 1..(Len(seq)-1) |-> IF i < idx THEN seq[i] ELSE seq[i+1]]

Init ==
    /\ coordState = [tx \in Transaction |-> "ACTIVE"]
    /\ coordVotes = [tx \in Transaction |-> [p \in Participant |-> "TIMEOUT"]]
    /\ coordDecisions = [tx \in Transaction |-> "UNDECIDED"]
    /\ participantState = [p \in Participant |-> [tx \in Transaction |-> "ACTIVE"]]
    /\ participantVotes = [p \in Participant |-> [tx \in Transaction |-> "TIMEOUT"]]
    /\ participantLogs = [p \in Participant |-> [tx \in Transaction |-> <<>>]]
    /\ txData = [tx \in Transaction |-> 0]
    /\ txParticipants = [tx \in Transaction |-> Participants]
    /\ prepareChannel = <<>>
    /\ voteChannel = <<>>
    /\ decisionChannel = <<>>
    /\ ackChannel = <<>>
    /\ committedTxns = {}
    /\ abortedTxns = {}
    /\ globalClock = 0
    /\ outputLog = <<>>

SendPrepare(tx) ==
    /\ tx \in Transaction
    /\ coordState[tx] = "ACTIVE"
    /\ coordState' = [coordState EXCEPT ![tx] = "PREPARING"]
    /\ prepareChannel' = Append(prepareChannel,
                               [type |-> "PREPARE",
                                tx |-> tx,
                                timestamp |-> globalClock,
                                participants |-> txParticipants[tx]])
    /\ UNCHANGED <<coordVotes, coordDecisions, participantState, 
                   participantVotes, participantLogs, txData, txParticipants,
                   voteChannel, decisionChannel, ackChannel, committedTxns,
                   abortedTxns, globalClock, outputLog>>

ReceivePrepare(p, tx) ==
    /\ p \in Participant
    /\ tx \in Transaction
    /\ p \in txParticipants[tx]
    /\ participantState[p][tx] = "ACTIVE"
    /\ \E i \in 1..Len(prepareChannel) :
        /\ prepareChannel[i].type = "PREPARE"
        /\ prepareChannel[i].tx = tx
        /\ p \in prepareChannel[i].participants
        /\ participantState' = [participantState EXCEPT ![p] = 
                              [@ EXCEPT ![tx] = "PREPARING"]]
        /\ participantLogs' = [participantLogs EXCEPT ![p] = 
                              [@ EXCEPT ![tx] = Append(@, 
                                  [type |-> "PREPARE", 
                                   timestamp |-> globalClock])]]
        /\ prepareChannel' = Remove(prepareChannel, i)
    /\ UNCHANGED <<coordState, coordVotes, coordDecisions, participantVotes,
                   txData, txParticipants, voteChannel, decisionChannel,
                   ackChannel, committedTxns, abortedTxns, globalClock, outputLog>>

VoteYes(p, tx) ==
    /\ p \in Participant
    /\ tx \in Transaction
    /\ participantState[p][tx] = "PREPARING"
    /\ participantVotes' = [participantVotes EXCEPT ![p] = 
                          [@ EXCEPT ![tx] = "YES"]]
    /\ participantState' = [participantState EXCEPT ![p] = 
                          [@ EXCEPT ![tx] = "PREPARED"]]
    /\ participantLogs' = [participantLogs EXCEPT ![p] = 
                          [@ EXCEPT ![tx] = Append(@,
                              [type |-> "VOTE_YES",
                               timestamp |-> globalClock])]]
    /\ voteChannel' = Append(voteChannel,
                            [type |-> "VOTE",
                             tx |-> tx,
                             participant |-> p,
                             vote |-> "YES",
                             timestamp |-> globalClock])
    /\ UNCHANGED <<coordState, coordVotes, coordDecisions, txData,
                   txParticipants, prepareChannel, decisionChannel, ackChannel,
                   committedTxns, abortedTxns, globalClock, outputLog>>

VoteNo(p, tx) ==
    /\ p \in Participant
    /\ tx \in Transaction
    /\ participantState[p][tx] = "PREPARING"
    /\ participantVotes' = [participantVotes EXCEPT ![p] = 
                          [@ EXCEPT ![tx] = "NO"]]
    /\ participantState' = [participantState EXCEPT ![p] = 
                          [@ EXCEPT ![tx] = "ABORTED"]]
    /\ participantLogs' = [participantLogs EXCEPT ![p] = 
                          [@ EXCEPT ![tx] = Append(@,
                              [type |-> "VOTE_NO",
                               timestamp |-> globalClock])]]
    /\ voteChannel' = Append(voteChannel,
                            [type |-> "VOTE",
                             tx |-> tx,
                             participant |-> p,
                             vote |-> "NO",
                             timestamp |-> globalClock])
    /\ UNCHANGED <<coordState, coordVotes, coordDecisions, txData,
                   txParticipants, prepareChannel, decisionChannel, ackChannel,
                   committedTxns, abortedTxns, globalClock, outputLog>>

ReceiveVote(tx) ==
    /\ tx \in Transaction
    /\ coordState[tx] = "PREPARING"
    /\ \E i \in 1..Len(voteChannel) :
        /\ voteChannel[i].type = "VOTE"
        /\ voteChannel[i].tx = tx
        /\ voteChannel[i].participant \notin DOMAIN coordVotes[tx]
        /\ coordVotes' = [coordVotes EXCEPT ![tx] = 
                         @ @@ (voteChannel[i].participant :> voteChannel[i].vote)]
        /\ voteChannel' = Remove(voteChannel, i)
    /\ UNCHANGED <<coordState, coordDecisions, participantState, 
                   participantVotes, participantLogs, txData, txParticipants,
                   prepareChannel, decisionChannel, ackChannel, committedTxns,
                   abortedTxns, globalClock, outputLog>>

DecideCommit(tx) ==
    /\ tx \in Transaction
    /\ CanDecide(tx)
    /\ AllYesVotes(tx)
    /\ coordState' = [coordState EXCEPT ![tx] = "COMMITTING"]
    /\ coordDecisions' = [coordDecisions EXCEPT ![tx] = "COMMIT"]
    /\ decisionChannel' = Append(decisionChannel,
                                [type |-> "DECISION",
                                 tx |-> tx,
                                 decision |-> "COMMIT",
                                 timestamp |-> globalClock,
                                 participants |-> txParticipants[tx]])
    /\ UNCHANGED <<coordVotes, participantState, participantVotes, 
                   participantLogs, txData, txParticipants, prepareChannel,
                   voteChannel, ackChannel, committedTxns, abortedTxns,
                   globalClock, outputLog>>

DecideAbort(tx) ==
    /\ tx \in Transaction
    /\ CanDecide(tx)
    /\ ~AllYesVotes(tx)
    /\ coordState' = [coordState EXCEPT ![tx] = "ABORTING"]
    /\ coordDecisions' = [coordDecisions EXCEPT ![tx] = "ABORT"]
    /\ decisionChannel' = Append(decisionChannel,
                                [type |-> "DECISION",
                                 tx |-> tx,
                                 decision |-> "ABORT",
                                 timestamp |-> globalClock,
                                 participants |-> txParticipants[tx]])
    /\ UNCHANGED <<coordVotes, participantState, participantVotes, 
                   participantLogs, txData, txParticipants, prepareChannel,
                   voteChannel, ackChannel, committedTxns, abortedTxns,
                   globalClock, outputLog>>

ReceiveCommitDecision(p, tx) ==
    /\ p \in Participant
    /\ tx \in Transaction
    /\ participantState[p][tx] = "PREPARED"
    /\ \E i \in 1..Len(decisionChannel) :
        /\ decisionChannel[i].type = "DECISION"
        /\ decisionChannel[i].tx = tx
        /\ decisionChannel[i].decision = "COMMIT"
        /\ p \in decisionChannel[i].participants
        /\ participantState' = [participantState EXCEPT ![p] = 
                              [@ EXCEPT ![tx] = "COMMITTED"]]
        /\ participantLogs' = [participantLogs EXCEPT ![p] = 
                              [@ EXCEPT ![tx] = Append(@,
                                  [type |-> "COMMIT",
                                   timestamp |-> globalClock])]]
        /\ decisionChannel' = Remove(decisionChannel, i)
    /\ UNCHANGED <<coordState, coordVotes, coordDecisions, participantVotes,
                   txData, txParticipants, prepareChannel, voteChannel,
                   ackChannel, committedTxns, abortedTxns, globalClock, outputLog>>

ReceiveAbortDecision(p, tx) ==
    /\ p \in Participant
    /\ tx \in Transaction
    /\ participantState[p][tx] \in {"PREPARING", "PREPARED"}
    /\ \E i \in 1..Len(decisionChannel) :
        /\ decisionChannel[i].type = "DECISION"
        /\ decisionChannel[i].tx = tx
        /\ decisionChannel[i].decision = "ABORT"
        /\ p \in decisionChannel[i].participants
        /\ participantState' = [participantState EXCEPT ![p] = 
                              [@ EXCEPT ![tx] = "ABORTED"]]
        /\ participantLogs' = [participantLogs EXCEPT ![p] = 
                              [@ EXCEPT ![tx] = Append(@,
                                  [type |-> "ABORT",
                                   timestamp |-> globalClock])]]
        /\ decisionChannel' = Remove(decisionChannel, i)
    /\ UNCHANGED <<coordState, coordVotes, coordDecisions, participantVotes,
                   txData, txParticipants, prepareChannel, voteChannel,
                   ackChannel, committedTxns, abortedTxns, globalClock, outputLog>>

CompleteCommit(tx) ==
    /\ tx \in Transaction
    /\ coordState[tx] = "COMMITTING"
    /\ coordState' = [coordState EXCEPT ![tx] = "COMMITTED"]
    /\ committedTxns' = committedTxns \union {tx}
    /\ outputLog' = Append(outputLog, [tx |-> tx, status |-> "COMMITTED", time |-> globalClock])
    /\ UNCHANGED <<coordVotes, coordDecisions, participantState, participantVotes,
                   participantLogs, txData, txParticipants, prepareChannel,
                   voteChannel, decisionChannel, ackChannel, abortedTxns,
                   globalClock>>

CompleteAbort(tx) ==
    /\ tx \in Transaction
    /\ coordState[tx] = "ABORTING"
    /\ coordState' = [coordState EXCEPT ![tx] = "ABORTED"]
    /\ abortedTxns' = abortedTxns \union {tx}
    /\ outputLog' = Append(outputLog, [tx |-> tx, status |-> "ABORTED", time |-> globalClock])
    /\ UNCHANGED <<coordVotes, coordDecisions, participantState, participantVotes,
                   participantLogs, txData, txParticipants, prepareChannel,
                   voteChannel, decisionChannel, ackChannel, committedTxns,
                   globalClock>>

AdvanceTime ==
    /\ globalClock' = globalClock + 1
    /\ UNCHANGED <<coordState, coordVotes, coordDecisions, participantState,
                   participantVotes, participantLogs, txData, txParticipants,
                   prepareChannel, voteChannel, decisionChannel, ackChannel,
                   committedTxns, abortedTxns, outputLog>>

Next ==
    \/ \E tx \in Transaction : SendPrepare(tx)
    \/ \E p \in Participant, tx \in Transaction : ReceivePrepare(p, tx)
    \/ \E p \in Participant, tx \in Transaction : VoteYes(p, tx)
    \/ \E p \in Participant, tx \in Transaction : VoteNo(p, tx)
    \/ \E tx \in Transaction : ReceiveVote(tx)
    \/ \E tx \in Transaction : DecideCommit(tx)
    \/ \E tx \in Transaction : DecideAbort(tx)
    \/ \E p \in Participant, tx \in Transaction : ReceiveCommitDecision(p, tx)
    \/ \E p \in Participant, tx \in Transaction : ReceiveAbortDecision(p, tx)
    \/ \E tx \in Transaction : CompleteCommit(tx)
    \/ \E tx \in Transaction : CompleteAbort(tx)
    \/ AdvanceTime

Fairness ==
    /\ \A tx \in Transaction : 
        SF_vars(CompleteCommit(tx) \/ CompleteAbort(tx))
    /\ WF_vars(AdvanceTime)
    /\ \A p \in Participant, tx \in Transaction :
        WF_vars(VoteYes(p, tx) \/ VoteNo(p, tx))

Spec == Init /\ [][Next]_vars /\ Fairness

TypeInvariant ==
    /\ coordState \in [Transaction -> TxState]
    /\ participantState \in [Participant -> [Transaction -> TxState]]
    /\ committedTxns \subseteq Transaction
    /\ abortedTxns \subseteq Transaction
    /\ committedTxns \intersect abortedTxns = {}

StateConsistency ==
    \A tx \in Transaction :
        (coordState[tx] = "COMMITTED" => tx \in committedTxns) /\ 
        (coordState[tx] = "ABORTED" => tx \in abortedTxns)

DecisionConsistency ==
    \A tx \in Transaction :
        coordDecisions[tx] = "COMMIT" => AllYesVotes(tx)

ParticipantCoordinatorConsistency ==
    \A tx \in Transaction, p \in txParticipants[tx] :
        (coordState[tx] = "COMMITTED" => 
            participantState[p][tx] \in {"PREPARED", "COMMITTED"}) /\ 
        (coordState[tx] = "ABORTED" => 
            participantState[p][tx] \in {"PREPARING", "PREPARED", "ABORTED"})

Atomicity ==
    \A tx \in committedTxns :
        \A p \in txParticipants[tx] :
            participantState[p][tx] = "COMMITTED"

MutualExclusion ==
    [] (committedTxns \intersect abortedTxns = {})

Serializability ==
    \A i, j \in 1..Len(outputLog) :
        i < j => outputLog[i].time <= outputLog[j].time

EventuallyDecides ==
    \A tx \in Transaction :
        coordState[tx] = "PREPARING" ~> 
        coordState[tx] \in {"COMMITTED", "ABORTED", "HEURISTIC"}

ExactlyOnce ==
    \A tx \in committedTxns :
        Cardinality({i \in 1..Len(outputLog) : outputLog[i].tx = tx}) = 1

vars == <<coordState, coordVotes, coordDecisions, participantState,
          participantVotes, participantLogs, txData, txParticipants,
          prepareChannel, voteChannel, decisionChannel, ackChannel,
          committedTxns, abortedTxns, globalClock, outputLog>>

================================================================================
