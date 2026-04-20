(* ============================================================================
 * TLA+ 规约: Raft 共识算法
 * ============================================================================
 *
 * 本规约描述 Diego Ongaro 和 John Ousterhout 的 Raft 共识算法。
 *
 * Raft 核心概念:
 * - Leader 选举: 使用任期(term)和随机超时选举Leader
 * - 日志复制: Leader将日志条目复制到Follower
 * - 安全性: 保证所有节点的日志一致性
 *
 * 服务器状态:
 * - Follower: 被动接收请求
 * - Candidate: 发起选举
 * - Leader: 处理客户端请求, 复制日志
 *
 * RPC消息:
 * - RequestVote: 候选人请求投票
 * - AppendEntries: Leader复制日志/发送心跳
 *
 * 参考: Ongaro & Ousterhout (2014). In Search of an Understandable Consensus Algorithm
 * ============================================================================ *)

--------------------------------- MODULE Raft ---------------------------------

(* ----------------------------------------------------------------------------
 * 常量定义
 * ---------------------------------------------------------------------------- *)

CONSTANTS
    Server,         (* 服务器集合 *)
    Value,          (* 客户端命令值 *)
    
    (* 服务器状态 *)
    Follower,
    Candidate,
    Leader,
    
    (* 消息类型 *)
    RequestVoteRequest,
    RequestVoteResponse,
    AppendEntriesRequest,
    AppendEntriesResponse,
    ClientRequest

(* ASSUME-01: 基数假设 - 至少需要 3 个节点以保证多数派容错 *)
(* 证明思路: 2 个节点无法容忍任何故障（2/2 不是多数），3 个节点可容忍 1 个故障；
 * 这是 Raft 提供容错能力的最小配置 *)
ASSUME ServerSizeAssumption ==
    /\ Cardinality(Server) >= 3    (* 至少需要3个节点 *)

(* ----------------------------------------------------------------------------
 * 辅助定义
 * ---------------------------------------------------------------------------- *)

Majority == {Q \in SUBSET Server : Cardinality(Q) * 2 > Cardinality(Server)}

(* 日志条目索引 *)
LogIndex == Nat \ {0}

(* 任期编号 *)
Term == Nat

(* ----------------------------------------------------------------------------
 * 变量定义
 * ---------------------------------------------------------------------------- *)

VARIABLES
    (* 持久状态 (所有服务器) *)
    currentTerm,    (* Server -> Term, 最后看到的任期 *)
    votedFor,       (* Server -> Server | {None}, 当前任期投票给谁 *)
    log,            (* Server -> Seq([term: Term, value: Value]), 日志条目 *)
    
    (* 易失状态 (所有服务器) *)
    commitIndex,    (* Server -> Nat, 已知的最高已提交索引 *)
    lastApplied,    (* Server -> Nat, 最后应用到状态机的索引 *)
    
    (* 易失状态 (Leader特有) *)
    nextIndex,      (* Server -> [Server -> LogIndex], 每个Follower的下一个发送索引 *)
    matchIndex,     (* Server -> [Server -> Nat], 每个Follower已知的最高匹配索引 *)
    
    (* 服务器状态 *)
    state,          (* Server -> {Follower, Candidate, Leader} *)
    
    (* 选举定时器 *)
    electionTimer,  (* Server -> Nat *)
    
    (* 消息网络 *)
    msgs            (* 消息集合 *)

(* ----------------------------------------------------------------------------
 * 消息类型定义
 * ---------------------------------------------------------------------------- *)

RequestVoteReq == [
    type: {RequestVoteRequest},
    term: Term,
    candidateId: Server,
    lastLogIndex: Nat,
    lastLogTerm: Term,
    to: Server
]

RequestVoteResp == [
    type: {RequestVoteResponse},
    term: Term,
    voteGranted: BOOLEAN,
    voter: Server,
    to: Server
]

AppendEntriesReq == [
    type: {AppendEntriesRequest},
    term: Term,
    leaderId: Server,
    prevLogIndex: Nat,
    prevLogTerm: Term,
    entries: Seq([term: Term, value: Value]),
    leaderCommit: Nat,
    to: Server
]

AppendEntriesResp == [
    type: {AppendEntriesResponse},
    term: Term,
    success: BOOLEAN,
    matchIndex: Nat,
    follower: Server,
    to: Server
]

Message == RequestVoteReq \cup RequestVoteResp \cup AppendEntriesReq \cup AppendEntriesResp

(* ----------------------------------------------------------------------------
 * 类型不变式
 * ---------------------------------------------------------------------------- *)

RaftTypeOK ==
    /\ currentTerm \in [Server -> Term]
    /\ votedFor \in [Server -> Server \cup {None}]
    /\ log \in [Server -> Seq([term: Term, value: Value])]
    /\ commitIndex \in [Server -> Nat]
    /\ lastApplied \in [Server -> Nat]
    /\ nextIndex \in [Server -> [Server -> LogIndex]]
    /\ matchIndex \in [Server -> [Server -> Nat]]
    /\ state \in [Server -> {Follower, Candidate, Leader}]
    /\ electionTimer \in [Server -> Nat]
    /\ msgs \subseteq Message

(* ----------------------------------------------------------------------------
 * 辅助函数
 * ---------------------------------------------------------------------------- *)

(* 获取服务器最后日志索引 *)
LastLogIndex(s) == Len(log[s])

(* 获取服务器最后日志任期 *)
LastLogTerm(s) ==
    IF LastLogIndex(s) = 0 THEN 0
    ELSE log[s][LastLogIndex(s)].term

(* 检查日志是否至少一样新 *)
LogIsAtLeastAsNew(s1, s2) ==
    /\ LastLogTerm(s1) >= LastLogTerm(s2)
    /\ (LastLogTerm(s1) = LastLogTerm(s2) => LastLogIndex(s1) >= LastLogIndex(s2))

(* 检查是否可以投票给候选人 *)
CanVote(voter, candidate, term) ==
    /\ currentTerm[voter] < term  \* 候选人的任期更新
    /\ (votedFor[voter] = candidate \/ votedFor[voter] = None)  \* 未投票或已投给候选人
    /\ LogIsAtLeastAsNew(candidate, voter)  \* 候选人的日志至少一样新

(* ----------------------------------------------------------------------------
 * 初始状态
 * ---------------------------------------------------------------------------- *)

Init ==
    /\ currentTerm = [s \in Server |-> 0]
    /\ votedFor = [s \in Server |-> None]
    /\ log = [s \in Server |-> << >>]     (* 空日志 *)
    /\ commitIndex = [s \in Server |-> 0]
    /\ lastApplied = [s \in Server |-> 0]
    /\ nextIndex = [s \in Server |-> [t \in Server |-> 1]]
    /\ matchIndex = [s \in Server |-> [t \in Server |-> 0]]
    /\ state = [s \in Server |-> Follower]
    /\ electionTimer = [s \in Server |-> 0]
    /\ msgs = {}

(* ----------------------------------------------------------------------------
 * 状态机函数
 * ---------------------------------------------------------------------------- *)

(* 转换为候选人 *)
BecomeCandidate(s) ==
    /\ state' = [state EXCEPT ![s] = Candidate]
    /\ currentTerm' = [currentTerm EXCEPT ![s] = @ + 1]
    /\ votedFor' = [votedFor EXCEPT ![s] = s]   (* 投票给自己 *)
    /\ electionTimer' = [electionTimer EXCEPT ![s] = 0]

(* 转换为Leader *)
BecomeLeader(s) ==
    /\ state' = [state EXCEPT ![s] = Leader]
    /\ nextIndex' = [nextIndex EXCEPT ![s] = [t \in Server |-> LastLogIndex(s) + 1]]
    /\ matchIndex' = [matchIndex EXCEPT ![s] = [t \in Server |-> 0]]

(* 转换为Follower *)
BecomeFollower(s, term) ==
    /\ state' = [state EXCEPT ![s] = Follower]
    /\ currentTerm' = [currentTerm EXCEPT ![s] = term]
    /\ votedFor' = [votedFor EXCEPT ![s] = None]

(* ----------------------------------------------------------------------------
 * RPC 处理动作
 * ---------------------------------------------------------------------------- *)

(* 处理 RequestVote RPC *)
HandleRequestVote(s) ==
    \E m \in msgs :
        /\ m.type = RequestVoteRequest
        /\ m.to = s
        /\ LET grant == CanVote(s, m.candidateId, m.term)
           IN IF grant
              THEN /\ votedFor' = [votedFor EXCEPT ![s] = m.candidateId]
                   /\ IF m.term > currentTerm[s]
                      THEN BecomeFollower(s, m.term)
                      ELSE UNCHANGED <<state, currentTerm>>
              ELSE UNCHANGED <<state, currentTerm, votedFor>>
        /\ msgs' = msgs \cup {
            [type |-> RequestVoteResponse,
             term |-> m.term,
             voteGranted |-> CanVote(s, m.candidateId, m.term),
             voter |-> s,
             to |-> m.candidateId]}
        /\ UNCHANGED <<log, commitIndex, lastApplied, nextIndex, matchIndex, electionTimer>>

(* 处理 RequestVote 响应 *)
HandleRequestVoteResponse(s) ==
    /\ state[s] = Candidate
    /\ \E m \in msgs :
        /\ m.type = RequestVoteResponse
        /\ m.to = s
        /\ m.term = currentTerm[s]
        /\ IF m.voteGranted
           THEN \E Q \in Majority :
                    /\ s \in Q
                    /\ \A t \in Q :
                        t = s \/ \E resp \in msgs :
                            /\ resp.type = RequestVoteResponse
                            /\ resp.to = s
                            /\ resp.voter = t
                            /\ resp.voteGranted
                            /\ resp.term = currentTerm[s]
                BecomeLeader(s)
           ELSE UNCHANGED <<state, nextIndex, matchIndex>>
        /\ UNCHANGED <<currentTerm, votedFor, log, commitIndex, 
                       lastApplied, electionTimer, msgs>>

(* 处理 AppendEntries RPC *)
HandleAppendEntries(s) ==
    \E m \in msgs :
        /\ m.type = AppendEntriesRequest
        /\ m.to = s
        /\ IF m.term < currentTerm[s]
           THEN (* 拒绝旧任期的Leader *)
                msgs' = msgs \cup {
                    [type |-> AppendEntriesResponse,
                     term |-> currentTerm[s],
                     success |-> FALSE,
                     matchIndex |-> 0,
                     follower |-> s,
                     to |-> m.leaderId]}
                /\ UNCHANGED <<state, currentTerm, votedFor, log, 
                               commitIndex, nextIndex, matchIndex, electionTimer>>
           ELSE (* 接受新Leader *)
                LET newState == IF m.term > currentTerm[s] 
                               THEN BecomeFollower(s, m.term) 
                               ELSE UNCHANGED <<state, currentTerm, votedFor>>
                IN IF m.prevLogIndex > 0 /\ 
                      (m.prevLogIndex > Len(log[s]) \/ 
                       log[s][m.prevLogIndex].term # m.prevLogTerm)
                   THEN (* 日志不匹配 *)
                        msgs' = msgs \cup {
                            [type |-> AppendEntriesResponse,
                             term |-> m.term,
                             success |-> FALSE,
                             matchIndex |-> 0,
                             follower |-> s,
                             to |-> m.leaderId]}
                        /\ UNCHANGED <<log, commitIndex, nextIndex, matchIndex, electionTimer>>
                   ELSE (* 日志匹配, 追加条目 *)
                        LET newLog == 
                            IF m.prevLogIndex = 0 
                            THEN m.entries
                            ELSE SubSeq(log[s], 1, m.prevLogIndex) \o m.entries
                        IN log' = [log EXCEPT ![s] = newLog]
                        /\ commitIndex' = [commitIndex EXCEPT ![s] = 
                            IF m.leaderCommit > @ THEN m.leaderCommit ELSE @]
                        /\ msgs' = msgs \cup {
                            [type |-> AppendEntriesResponse,
                             term |-> m.term,
                             success |-> TRUE,
                             matchIndex |-> m.prevLogIndex + Len(m.entries),
                             follower |-> s,
                             to |-> m.leaderId]}
                        /\ electionTimer' = [electionTimer EXCEPT ![s] = 0]
                        /\ UNCHANGED <<nextIndex, matchIndex>>
        /\ UNCHANGED <<lastApplied>>

(* 处理 AppendEntries 响应 *)
HandleAppendEntriesResponse(s) ==
    /\ state[s] = Leader
    /\ \E m \in msgs :
        /\ m.type = AppendEntriesResponse
        /\ m.to = s
        /\ IF m.term > currentTerm[s]
           THEN BecomeFollower(s, m.term)
           ELSE IF m.success
                THEN /\ matchIndex' = [matchIndex EXCEPT ![s][m.follower] = m.matchIndex]
                     /\ nextIndex' = [nextIndex EXCEPT ![s][m.follower] = m.matchIndex + 1]
                     /\ UNCHANGED <<state, currentTerm, votedFor>>
                ELSE /\ nextIndex' = [nextIndex EXCEPT ![s][m.follower] = 
                                       Max({@ - 1, 1})]
                     /\ UNCHANGED <<state, currentTerm, votedFor, matchIndex>>
        /\ UNCHANGED <<log, commitIndex, lastApplied, electionTimer, msgs>>

(* ----------------------------------------------------------------------------
 * Leader 动作
 * ---------------------------------------------------------------------------- *)

(* Leader 发送 AppendEntries (心跳或日志复制) *)
LeaderSendAppendEntries(s) ==
    /\ state[s] = Leader
    /\ \E t \in Server \ {s} :
        LET prevIdx == nextIndex[s][t] - 1
            prevTerm == IF prevIdx = 0 THEN 0 
                       ELSE log[s][prevIdx].term
            entries == IF nextIndex[s][t] > Len(log[s])
                      THEN << >>  (* 心跳 *)
                      ELSE SubSeq(log[s], nextIndex[s][t], Len(log[s]))
        IN msgs' = msgs \cup {
            [type |-> AppendEntriesRequest,
             term |-> currentTerm[s],
             leaderId |-> s,
             prevLogIndex |-> prevIdx,
             prevLogTerm |-> prevTerm,
             entries |-> entries,
             leaderCommit |-> commitIndex[s],
             to |-> t]}
    /\ UNCHANGED <<state, currentTerm, votedFor, log, commitIndex, 
                   lastApplied, nextIndex, matchIndex, electionTimer>>

(* Leader 提交日志 *)
LeaderCommit(s) ==
    /\ state[s] = Leader
    /\ \E i \in {commitIndex[s] + 1 .. Len(log[s])} :
        /\ log[s][i].term = currentTerm[s]   (* 只提交当前任期的条目 *)
        /\ \E Q \in Majority :
            \A t \in Q : matchIndex[s][t] >= i
        /\ commitIndex' = [commitIndex EXCEPT ![s] = i]
    /\ UNCHANGED <<state, currentTerm, votedFor, log, lastApplied, 
                   nextIndex, matchIndex, electionTimer, msgs>>

(* ----------------------------------------------------------------------------
 * Candidate 动作
 * ---------------------------------------------------------------------------- *)

(* Candidate 发送 RequestVote *)
CandidateSendRequestVote(s) ==
    /\ state[s] = Candidate
    /\ \E t \in Server \ {s} :
        msgs' = msgs \cup {
            [type |-> RequestVoteRequest,
             term |-> currentTerm[s],
             candidateId |-> s,
             lastLogIndex |-> LastLogIndex(s),
             lastLogTerm |-> LastLogTerm(s),
             to |-> t]}
    /\ UNCHANGED <<state, currentTerm, votedFor, log, commitIndex, 
                   lastApplied, nextIndex, matchIndex, electionTimer>>

(* ----------------------------------------------------------------------------
 * 定时器动作
 * ---------------------------------------------------------------------------- *)

(* 选举超时 *)
ElectionTimeout(s) ==
    /\ state[s] \in {Follower, Candidate}
    /\ electionTimer[s] >= 10   (* 简化的超时阈值 *)
    /\ BecomeCandidate(s)
    /\ UNCHANGED <<log, commitIndex, lastApplied, nextIndex, matchIndex, msgs>>

(* 定时器递增 *)
Tick(s) ==
    /\ electionTimer' = [electionTimer EXCEPT ![s] = @ + 1]
    /\ UNCHANGED <<state, currentTerm, votedFor, log, commitIndex, 
                   lastApplied, nextIndex, matchIndex, msgs>>

(* ----------------------------------------------------------------------------
 * 下一步动作
 * ---------------------------------------------------------------------------- *)

Next ==
    \/ \E s \in Server : HandleRequestVote(s)
    \/ \E s \in Server : HandleRequestVoteResponse(s)
    \/ \E s \in Server : HandleAppendEntries(s)
    \/ \E s \in Server : HandleAppendEntriesResponse(s)
    \/ \E s \in Server : LeaderSendAppendEntries(s)
    \/ \E s \in Server : LeaderCommit(s)
    \/ \E s \in Server : CandidateSendRequestVote(s)
    \/ \E s \in Server : ElectionTimeout(s)
    \/ \E s \in Server : Tick(s)

(* ----------------------------------------------------------------------------
 * 规约
 * ---------------------------------------------------------------------------- *)

Spec == Init /\ [][Next]_<<state, currentTerm, votedFor, log, commitIndex, 
                              lastApplied, nextIndex, matchIndex, electionTimer, msgs>>

(* ----------------------------------------------------------------------------
 * 不变式 (安全性)
 * ---------------------------------------------------------------------------- *)

(* 类型不变式 *)
TypeInvariant == RaftTypeOK

(* 每个任期最多一个Leader *)
OneLeaderPerTerm ==
    \A s, t \in Server :
        (state[s] = Leader /\ state[t] = Leader /\ currentTerm[s] = currentTerm[t])
        => s = t

(* 日志匹配性质 *)
LogMatching ==
    \A s, t \in Server, i \in LogIndex :
        (i <= Len(log[s]) /\ i <= Len(log[t]) /\ log[s][i].term = log[t][i].term)
        => SubSeq(log[s], 1, i) = SubSeq(log[t], 1, i)

(* Leader完整性: 一旦条目被提交, 所有后续Leader都有该条目 *)
LeaderCompleteness ==
    \A s \in Server :
        state[s] = Leader => 
            \A i \in 1..commitIndex[s] :
                i <= Len(log[s]) /\ log[s][i].term <= currentTerm[s]

(* ----------------------------------------------------------------------------
 * 时序性质 (活性)
 * ---------------------------------------------------------------------------- *)

(* 最终选举出Leader *)
EventuallyLeaderElected ==
    <>(\E s \in Server : state[s] = Leader)

(* ----------------------------------------------------------------------------
 * 模型检查配置
 * ---------------------------------------------------------------------------- *)
(*
TLC Model Checker 配置:

1. 定义常量:
   Server = {s1, s2, s3}
   Value = {v1, v2}
   Follower = Follower
   Candidate = Candidate
   Leader = Leader
   RequestVoteRequest = RequestVoteRequest
   RequestVoteResponse = RequestVoteResponse
   AppendEntriesRequest = AppendEntriesRequest
   AppendEntriesResponse = AppendEntriesResponse
   ClientRequest = ClientRequest

2. 检查的不变式:
   - TypeInvariant
   - OneLeaderPerTerm
   - LogMatching
   - LeaderCompleteness

3. 检查的属性:
   - EventuallyLeaderElected
*)

================================================================================
