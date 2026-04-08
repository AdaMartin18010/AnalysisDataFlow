------------------------------- MODULE ExactlyOnceMC -------------------------------
(*
 * ExactlyOnceMC - ExactlyOnce模型检验实例
 * 用于TLC模型检验器验证两阶段提交协议
 *)

EXTENDS ExactlyOnce

CONSTANTS
    p1, p2
    tx1, tx2

MC_Participants == {p1, p2}
MC_Transactions == {tx1, tx2}
MC_MaxRetries == 1
MC_CoordinatorId == "coord"

MC_Init ==
    /\ coordState = [tx \in MC_Transactions |-> "ACTIVE"]
    /\ coordVotes = [tx \in MC_Transactions |-> [p \in MC_Participants |-> "TIMEOUT"]]
    /\ coordDecisions = [tx \in MC_Transactions |-> "UNDECIDED"]
    /\ participantState = [p \in MC_Participants |-> [tx \in MC_Transactions |-> "ACTIVE"]]
    /\ participantVotes = [p \in MC_Participants |-> [tx \in MC_Transactions |-> "TIMEOUT"]]
    /\ participantLogs = [p \in MC_Participants |-> [tx \in MC_Transactions |-> <<>>]]
    /\ txData = [tx \in MC_Transactions |-> 0]
    /\ txParticipants = [tx \in MC_Transactions |-> MC_Participants]
    /\ prepareChannel = <<>>
    /\ voteChannel = <<>>
    /\ decisionChannel = <<>>
    /\ ackChannel = <<>>
    /\ committedTxns = {}
    /\ abortedTxns = {}
    /\ globalClock = 0
    /\ outputLog = <<>>

MC_Next ==
    \/ \E tx \in MC_Transactions : 
        /\ coordState[tx] = "ACTIVE"
        /\ coordState' = [coordState EXCEPT ![tx] = "PREPARING"]
        /\ prepareChannel' = Append(prepareChannel,
                                   [type |-> "PREPARE",
                                    tx |-> tx,
                                    timestamp |-> globalClock,
                                    participants |-> MC_Participants])
        /\ UNCHANGED <<coordVotes, coordDecisions, participantState, 
                       participantVotes, participantLogs, txData, txParticipants,
                       voteChannel, decisionChannel, ackChannel, committedTxns,
                       abortedTxns, globalClock, outputLog>>
    \/ \E p \in MC_Participants, tx \in MC_Transactions : 
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
    \/ \E p \in MC_Participants, tx \in MC_Transactions : 
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
    \/ \E tx \in MC_Transactions : 
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
    \/ \E tx \in MC_Transactions : 
        /\ coordState[tx] = "PREPARING"
        /\ DOMAIN coordVotes[tx] = txParticipants[tx]
        /\ \A p \in txParticipants[tx] : coordVotes[tx][p] = "YES"
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
    \/ \E p \in MC_Participants, tx \in MC_Transactions : 
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
    \/ \E tx \in MC_Transactions : 
        /\ coordState[tx] = "COMMITTING"
        /\ coordState' = [coordState EXCEPT ![tx] = "COMMITTED"]
        /\ committedTxns' = committedTxns \union {tx}
        /\ outputLog' = Append(outputLog, [tx |-> tx, status |-> "COMMITTED", time |-> globalClock])
        /\ UNCHANGED <<coordVotes, coordDecisions, participantState, participantVotes,
                       participantLogs, txData, txParticipants, prepareChannel,
                       voteChannel, decisionChannel, ackChannel, abortedTxns,
                       globalClock>>
    \/ /\ globalClock' = globalClock + 1
       /\ UNCHANGED <<coordState, coordVotes, coordDecisions, participantState,
                      participantVotes, participantLogs, txData, txParticipants,
                      prepareChannel, voteChannel, decisionChannel, ackChannel,
                      committedTxns, abortedTxns, outputLog>>

MC_Spec == MC_Init /\ [][MC_Next]_vars

MC_TypeInvariant ==
    /\ coordState \in [MC_Transactions -> TxState]
    /\ participantState \in [MC_Participants -> [MC_Transactions -> TxState]]
    /\ committedTxns \subseteq MC_Transactions
    /\ abortedTxns \subseteq MC_Transactions

MC_Atomicity ==
    [] (committedTxns \intersect abortedTxns = {})

MC_EventuallyCommits ==
    <> (tx1 \in committedTxns)

================================================================================
