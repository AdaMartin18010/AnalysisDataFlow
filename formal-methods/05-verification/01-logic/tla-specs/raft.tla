(*
 * Raft Consensus Protocol - TLA+ Specification
 * ============================================
 *
 * 本规约描述 Raft 共识算法的完整行为，包括：
 * - 领导选举 (Leader Election)
 * - 日志复制 (Log Replication)
 * - 安全性保证 (Safety Properties)
 *
 * Raft 设计原则：可理解性优先，通过分离关注点
 * （领导者选举、日志复制、安全性）简化分布式共识。
 *
 * 与 Paxos 的关系：
 * - Raft 与 Multi-Paxos 等价
 * - 提供了更强的领导者概念和更清晰的日志结构
 * - 安全性属性与 Paxos 相同
 *
 * 作者: AnalysisDataFlow Project
 * 版本: 1.0
 *)

------------------------------- MODULE raft -------------------------------

EXTENDS Naturals, FiniteSets, Sequences, TLC

(*
 * =====================================================================
 * 常量声明
 * =====================================================================
 *)
CONSTANTS
    Server,             \* 服务器集合
    Value,              \* 客户端请求的值的集合
    MaxTerm,            \* 最大任期数（用于模型检查）
    MaxLogLen           \* 最大日志长度（用于模型检查）

(*
 * =====================================================================
 * 辅助定义
 * =====================================================================
 *)
Quorum == {Q \in SUBSET Server : Cardinality(Q) * 2 > Cardinality(Server)}

Majority(Q) == Cardinality(Q) * 2 > Cardinality(Server)

Term == 0..MaxTerm

Index == 1..MaxLogLen

Nil == CHOOSE v : v \notin Server

(*
 * =====================================================================
 * 变量声明
 * =====================================================================
 *)
VARIABLES
    (* 持久化状态 - 所有服务器 *)
    currentTerm,        \* 服务器知道的最新任期
    votedFor,           \* 当前任期内投票给的候选者
    log,                \* 日志条目: [index |-> i, term |-> t, value |-> v]
    
    (* 易失性状态 - 所有服务器 *)
    commitIndex,        \* 已知已提交的最高日志索引
    lastApplied,        \* 已应用到状态机的最高日志索引
    
    (* 易失性状态 - 仅领导者 *)
    nextIndex,          \* 对每个服务器，下一个要发送的日志索引
    matchIndex,         \* 对每个服务器，已知复制的最高日志索引
    
    (* 角色 *)
    state,              \* {Follower, Candidate, Leader}
    
    (* 消息 *)
    msgs                \* 网络中的消息

(*
 * =====================================================================
 * 类型定义
 * =====================================================================
 *)
Entry == [index : Index, term : Term, value : Value]

Message ==
    [type : {"RequestVoteRequest"}, from : Server, to : Server, 
     term : Term, lastLogIndex : Nat, lastLogTerm : Term]
    \cup
    [type : {"RequestVoteResponse"}, from : Server, to : Server,
     term : Term, voteGranted : BOOLEAN]
    \cup
    [type : {"AppendEntriesRequest"}, from : Server, to : Server,
     term : Term, prevLogIndex : Nat, prevLogTerm : Term,
     entries : Seq(Entry), leaderCommit : Nat]
    \cup
    [type : {"AppendEntriesResponse"}, from : Server, to : Server,
     term : Term, success : BOOLEAN, matchIndex : Nat]

(*
 * =====================================================================
 * 类型不变式
 * =====================================================================
 *)
TypeOK ==
    /\ currentTerm \in [Server -> Term]
    /\ votedFor \in [Server -> Server \cup {Nil}]
    /\ log \in [Server -> Seq([index : Index, term : Term, value : Value])]
    /\ commitIndex \in [Server -> Nat]
    /\ lastApplied \in [Server -> Nat]
    /\ nextIndex \in [Server -> [Server -> Nat]]
    /\ matchIndex \in [Server -> [Server -> Nat]]
    /\ state \in [Server -> {"Follower", "Candidate", "Leader"}]
    /\ msgs \subseteq Message

(*
 * =====================================================================
 * 辅助函数
 * =====================================================================
 *)

(* 获取服务器的最后日志索引 *)
LastLogIndex(s) == Len(log[s])

(* 获取服务器的最后日志任期 *)
LastLogTerm(s) ==
    IF LastLogIndex(s) = 0 THEN 0
    ELSE log[s][LastLogIndex(s)].term

(* 获取日志条目任期 *)
LogTerm(s, i) ==
    IF i = 0 THEN 0
    ELSE IF i > Len(log[s]) THEN 0
    ELSE log[s][i].term

(* 获取日志条目值 *)
LogValue(s, i) ==
    IF i > Len(log[s]) THEN Nil
    ELSE log[s][i].value

(* 比较日志：谁的日志更新 *)
IsLogUpToDate(s1, s2) ==
    LET lastTerm1 == LastLogTerm(s1)
        lastTerm2 == LastLogTerm(s2)
        lastIndex1 == LastLogIndex(s1)
        lastIndex2 == LastLogIndex(s2)
    IN (lastTerm1 > lastTerm2)
       \/ ((lastTerm1 = lastTerm2) /\ (lastIndex1 >= lastIndex2))

(*
 * =====================================================================
 * 初始状态
 * =====================================================================
 *)
Init ==
    /\ currentTerm = [s \in Server |-> 0]
    /\ votedFor = [s \in Server |-> Nil]
    /\ log = [s \in Server |-> <<>>]
    /\ commitIndex = [s \in Server |-> 0]
    /\ lastApplied = [s \in Server |-> 0]
    /\ nextIndex = [s \in Server |-> [t \in Server |-> 1]]
    /\ matchIndex = [s \in Server |-> [t \in Server |-> 0]]
    /\ state = [s \in Server |-> "Follower"]
    /\ msgs = {}

(*
 * =====================================================================
 * 消息发送
 * =====================================================================
 *)
Send(m) == msgs' = msgs \cup {m}

Reply(m, old_m) == msgs' = (msgs \ {old_m}) \cup {m}

(*
 * =====================================================================
 * 服务器行为：Follower
 * =====================================================================
 *)

(* Follower 超时并开始新的选举 *)
StartElection(s) ==
    /\ state[s] \in {"Follower", "Candidate"}
    /\ state' = [state EXCEPT ![s] = "Candidate"]
    /\ currentTerm' = [currentTerm EXCEPT ![s] = @ + 1]
    /\ votedFor' = [votedFor EXCEPT ![s] = s]
    /\ \E Q \in Quorum : TRUE  \* 提示 TLC 存在多数派
    /\ Send([type |-> "RequestVoteRequest",
            from |-> s,
            to |-> Nil,  \* 广播
            term |-> currentTerm[s] + 1,
            lastLogIndex |-> LastLogIndex(s),
            lastLogTerm |-> LastLogTerm(s)])
    /\ UNCHANGED <<log, commitIndex, lastApplied, nextIndex, matchIndex>>

(* Follower 处理投票请求 *)
HandleVoteRequest(s) ==
    \E m \in msgs :
        /\ m.type = "RequestVoteRequest"
        /\ m.to = s
        /\ m.term > currentTerm[s]
        /\ currentTerm' = [currentTerm EXCEPT ![s] = m.term]
        /\ state' = [state EXCEPT ![s] = "Follower"]
        /\ LET canVote == 
               (votedFor[s] = Nil \/ votedFor[s] = m.from)
               /\ IsLogUpToDate(m.from, s)
           IN 
           /\ votedFor' = [votedFor EXCEPT ![s] = 
                IF canVote THEN m.from ELSE Nil]
           /\ Reply([type |-> "RequestVoteResponse",
                    from |-> s,
                    to |-> m.from,
                    term |-> m.term,
                    voteGranted |-> canVote], m)
        /\ UNCHANGED <<log, commitIndex, lastApplied, nextIndex, matchIndex>>

(*
 * =====================================================================
 * 服务器行为：Candidate
 * =====================================================================
 *)

(* Candidate 收集投票 *)
CollectVote(s) ==
    \E m \in msgs :
        /\ m.type = "RequestVoteResponse"
        /\ m.to = s
        /\ m.term = currentTerm[s]
        /\ m.voteGranted
        /\ LET votes == {mv \in msgs : 
                mv.type = "RequestVoteResponse"
                /\ mv.to = s
                /\ mv.term = currentTerm[s]
                /\ mv.voteGranted}
           IN \E Q \in Quorum :
               /\ Q \subseteq {mv.from : mv \in votes}
               /\ state' = [state EXCEPT ![s] = "Leader"]
               /\ nextIndex' = [nextIndex EXCEPT ![s] = 
                    [t \in Server |-> LastLogIndex(s) + 1]]
               /\ matchIndex' = [matchIndex EXCEPT ![s] = 
                    [t \in Server |-> 0]]
        /\ UNCHANGED <<currentTerm, votedFor, log, commitIndex, 
                       lastApplied, msgs>>

(*
 * =====================================================================
 * 服务器行为：Leader
 * =====================================================================
 *)

(* Leader 复制日志到 Follower *)
ReplicateLog(leader, follower) ==
    /\ state[leader] = "Leader"
    /\ LET nextIdx == nextIndex[leader][follower]
           prevIdx == nextIdx - 1
           prevTerm == LogTerm(leader, prevIdx)
           entries == IF nextIdx <= LastLogIndex(leader)
                      THEN SubSeq(log[leader], nextIdx, LastLogIndex(leader))
                      ELSE <<>>
       IN Send([type |-> "AppendEntriesRequest",
                from |-> leader,
                to |-> follower,
                term |-> currentTerm[leader],
                prevLogIndex |-> prevIdx,
                prevLogTerm |-> prevTerm,
                entries |-> entries,
                leaderCommit |-> commitIndex[leader]])
    /\ UNCHANGED <<currentTerm, votedFor, log, commitIndex, lastApplied,
                   state, nextIndex, matchIndex>>

(* Leader 接收客户端请求（简化：直接选择一个值） *)
ClientRequest(leader) ==
    /\ state[leader] = "Leader"
    /\ \E v \in Value :
        /\ LastLogIndex(leader) < MaxLogLen
        /\ log' = [log EXCEPT ![leader] = 
            Append(@, [index |-> LastLogIndex(leader) + 1,
                      term |-> currentTerm[leader],
                      value |-> v])]
    /\ UNCHANGED <<currentTerm, votedFor, commitIndex, lastApplied,
                   state, nextIndex, matchIndex, msgs>>

(* Leader 更新 commitIndex *)
AdvanceCommitIndex(leader) ==
    /\ state[leader] = "Leader"
    /\ \E n \in (commitIndex[leader] + 1)..LastLogIndex(leader) :
        /\ log[leader][n].term = currentTerm[leader]
        /\ \E Q \in Quorum :
            /\ leader \in Q
            /\ \A s \in Q : 
                s = leader \/ matchIndex[leader][s] >= n
        /\ commitIndex' = [commitIndex EXCEPT ![leader] = n]
    /\ UNCHANGED <<currentTerm, votedFor, log, lastApplied, state,
                   nextIndex, matchIndex, msgs>>

(*
 * =====================================================================
 * Follower 处理 AppendEntries
 * =====================================================================
 *)
HandleAppendEntries(s) ==
    \E m \in msgs :
        /\ m.type = "AppendEntriesRequest"
        /\ m.to = s
        /\ m.term >= currentTerm[s]
        /\ currentTerm' = [currentTerm EXCEPT ![s] = m.term]
        /\ state' = [state EXCEPT ![s] = "Follower"]
        /\ LET success ==
               (m.prevLogIndex = 0)
               \/ ((m.prevLogIndex <= LastLogIndex(s))
                   /\ (LogTerm(s, m.prevLogIndex) = m.prevLogTerm))
           IN 
           /\ IF success
              THEN 
                  (* 删除冲突条目并追加新条目 *)
                  LET newLog ==
                      IF m.prevLogIndex = 0
                      THEN m.entries
                      ELSE IF m.prevLogIndex >= Len(log[s])
                      THEN log[s]  \* 不应该发生
                      ELSE Concatenate(
                            SubSeq(log[s], 1, m.prevLogIndex),
                            m.entries)
                  IN log' = [log EXCEPT ![s] = newLog]
              ELSE log' = log
           /\ commitIndex' = [commitIndex EXCEPT ![s] =
                IF success /\ m.leaderCommit > commitIndex[s]
                THEN Min(m.leaderCommit, LastLogIndex(s))
                ELSE commitIndex[s]]
           /\ Reply([type |-> "AppendEntriesResponse",
                    from |-> s,
                    to |-> m.from,
                    term |-> m.term,
                    success |-> success,
                    matchIndex |-> IF success THEN m.prevLogIndex + Len(m.entries)
                                             ELSE 0], m)
        /\ UNCHANGED <<votedFor, lastApplied, nextIndex, matchIndex>>

(* Leader 处理 AppendEntries 响应 *)
HandleAppendEntriesResponse(leader) ==
    \E m \in msgs :
        /\ m.type = "AppendEntriesResponse"
        /\ m.to = leader
        /\ state[leader] = "Leader"
        /\ m.term = currentTerm[leader]
        /\ IF m.success
           THEN 
               /\ matchIndex' = [matchIndex EXCEPT ![leader] = 
                    [matchIndex[leader] EXCEPT ![m.from] = 
                        Max(@, m.matchIndex)]]
               /\ nextIndex' = [nextIndex EXCEPT ![leader] =
                    [nextIndex[leader] EXCEPT ![m.from] = 
                        Max(@, m.matchIndex + 1)]]
           ELSE 
               /\ nextIndex' = [nextIndex EXCEPT ![leader] =
                    [nextIndex[leader] EXCEPT ![m.from] = 
                        Max(1, nextIndex[leader][m.from] - 1)]]
               /\ matchIndex' = matchIndex
        /\ UNCHANGED <<currentTerm, votedFor, log, commitIndex, 
                       lastApplied, state, msgs>>

(*
 * =====================================================================
 * 下一步动作
 * =====================================================================
 *)
Next ==
    \E s \in Server :
        StartElection(s) \/ HandleVoteRequest(s) \/ CollectVote(s)
        \/ ClientRequest(s) \/ AdvanceCommitIndex(s)
        \/ HandleAppendEntries(s) \/ HandleAppendEntriesResponse(s)
        \/ \E t \in Server \\ {s} : ReplicateLog(s, t)

(*
 * =====================================================================
 * 完整规约
 * =====================================================================
 *)
Spec == Init /\ [][Next]_<<currentTerm, votedFor, log, commitIndex, 
                          lastApplied, state, nextIndex, matchIndex, msgs>>

(*
 * =====================================================================
 * 安全性不变式 (Safety Properties)
 * =====================================================================
 *)

(*
 * Thm-Raft-01: Election Safety
 * 每个任期最多只有一个领导者
 *)
ElectionSafety ==
    \A s1, s2 \in Server :
        (state[s1] = "Leader" /\ state[s2] = "Leader"
         /\ currentTerm[s1] = currentTerm[s2])
        => s1 = s2

(*
 * Thm-Raft-02: Leader Append-Only
 * 领导者从不删除或覆盖日志条目，只追加
 *)
LeaderAppendOnly ==
    [][\A s \in Server :
        state[s] = "Leader" => Len(log'[s]) >= Len(log[s])]_vars

(*
 * Thm-Raft-03: Log Matching Property
 * 如果两个日志在相同索引处有相同任期，则它们在该索引之前的所有条目都相同
 *)
LogMatching ==
    \A s1, s2 \in Server, i \in Index :
        (i <= Len(log[s1]) /\ i <= Len(log[s2])
         /\ log[s1][i].term = log[s2][i].term)
        => \A j \in 1..i : log[s1][j] = log[s2][j]

(*
 * Thm-Raft-04: Leader Completeness
 * 如果一个日志条目在某个任期被提交，则它会在所有更高任期的领导者的日志中
 *)
LeaderCompleteness ==
    \A s \in Server, t \in Term, i \in Index :
        (state[s] = "Leader" /\ currentTerm[s] = t)
        => \A t2 \in 0..(t-1), i2 \in Index :
            (\E Q \in Quorum : \A s2 \in Q : 
                commitIndex[s2] >= i2 /\ LogTerm(s2, i2) = t2)
            => (i2 <= Len(log[s]) /\ LogTerm(s, i2) = t2)

(*
 * Thm-Raft-05: State Machine Safety
 * 如果服务器应用了某个索引的日志到状态机，则没有其他服务器会在相同索引应用不同的日志
 *)
StateMachineSafety ==
    \A s1, s2 \in Server :
        (lastApplied[s1] > 0 /\ lastApplied[s2] > 0)
        => \A i \in 1..Min(lastApplied[s1], lastApplied[s2]) :
            LogValue(s1, i) = LogValue(s2, i)

(*
 * =====================================================================
 * 活性属性 (Liveness Properties)
 * =====================================================================
 *)

(*
 * Thm-Raft-06: Leader Election
 * 最终会有一个领导者被选出
 *)
LeaderElection ==
    <>(\E s \in Server : state[s] = "Leader")

(*
 * Thm-Raft-07: Log Replication Progress
 * 一旦领导者被选出，日志最终会被复制到多数派
 *)
LogReplication ==
    \A s \in Server :
        (state[s] = "Leader" 
         /\ commitIndex[s] < LastLogIndex(s))
        => <>(commitIndex[s] >= LastLogIndex(s))

(*
 * =====================================================================
 * 与 Paxos 的等价性讨论
 * =====================================================================
 *
 * Thm-Raft-Paxos-Equiv: Raft 与 Paxos 的对应关系
 *
 * Raft 的组件映射到 Paxos：
 * - Raft Term      <=> Paxos Ballot
 * - Raft Leader    <=> Paxos Proposer (活跃时)
 * - Raft Follower  <=> Paxos Acceptor + Learner
 * - Raft Log Entry <=> Paxos Instance
 *
 * 关键等价性：
 * 1. 领导者选举 (Raft) <=> 准备阶段 (Paxos Phase 1)
 *    - Raft 的 RequestVote 对应 Paxos 的 Prepare
 *    - RequestVote 中的 lastLogTerm/lastLogIndex 确保 Leader Completeness
 *
 * 2. 日志复制 (Raft) <=> 接受阶段 (Paxos Phase 2)
 *    - AppendEntries 对应 Accept 消息
 *    - 日志索引对应 Paxos 的 instance 编号
 *
 * 3. 安全性保证
 *    - Election Safety (Raft) <=> Leader Uniqueness (Paxos)
 *    - State Machine Safety (Raft) <=> Agreement (Paxos)
 *
 * Raft 的优势：
 * - 更强的领导者概念，简化客户端交互
 * - 顺序日志结构，便于实现和验证
 * - 通过日志匹配属性保证一致性
 *
 * Paxos 的优势：
 * - 更灵活的多领导者支持
 * - 单条决策的原子性更好
 *)

(*
 * =====================================================================
 * TLC 配置
 * =====================================================================
 *
 * CONSTANTS:
 *   Server = {s1, s2, s3}
 *   Value = {v1, v2}
 *   MaxTerm = 3
 *   MaxLogLen = 5
 *
 * 不变式:
 *   TypeOK
 *   ElectionSafety
 *   LogMatching
 *   LeaderCompleteness
 *   StateMachineSafety
 *)

=============================================================================
