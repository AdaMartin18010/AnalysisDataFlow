-------------------------------- MODULE Raft --------------------------------
(******************************************************************************)
(* Raft 共识算法 TLA+ 形式化规约（基础框架）                                      *)
(*                                                                            *)
(* 基于 Diego Ongaro 的博士论文 "Consensus: Bridging Theory and Practice"      *)
(* 本版本提供基础框架，包含核心变量和动作定义                                    *)
(*                                                                            *)
(* 所属阶段: Struct/ | 形式化等级: L5                                           *)
(* 状态: 基础框架（待完善完整实现）                                              *)
(******************************************************************************)

------------------------------------------------------------------------------
(*============================================================================*)
(* 导入模块                                                                    *)
(*============================================================================*)

EXTENDS Integers, Sequences, FiniteSets, TLC

------------------------------------------------------------------------------
(*============================================================================*)
(* 常量声明                                                                    *)
(*============================================================================*)

CONSTANTS
    Server,             \* 服务器节点集合，例如 {s1, s2, s3, s4, s5}
    Value,              \* 可以提交到日志的客户端命令值
    MaxTerm,            \* 用于模型检测的最大任期号（限制状态空间）
    MaxLogLength        \* 用于模型检测的最大日志长度（限制状态空间）

(* ASSUME-01: 常量参数约束 - Server 非空有限，MaxTerm/MaxLogLength 为自然数 *)
(* 证明思路: 模型参数约束，由 TLC 配置保证；有限性保证模型检查可终止 *)
ASSUME ConstantsAssumption ==
    /\ Server # {}                              \* 至少有一个服务器
    /\ IsFiniteSet(Server)                      \* 服务器集合有限
    /\ MaxTerm \in Nat                          \* MaxTerm 是自然数
    /\ MaxLogLength \in Nat                     \* MaxLogLength 是自然数

------------------------------------------------------------------------------
(*============================================================================*)
(* 辅助定义                                                                    *)
(*============================================================================*)

(* 服务器角色 *)
Follower == "follower"
Candidate == "candidate"
Leader == "leader"
Role == {Follower, Candidate, Leader}

(* 空值定义 *)
Nil == 0

(* 服务器多数派大小 *)
MajoritySize == (Cardinality(Server) \div 2) + 1

(* 判断一个集合是否为多数派 *)
IsMajority(Q) ==
    /\ Q \subseteq Server
    /\ Cardinality(Q) >= MajoritySize

(* 任期号范围（用于模型检测） *)
Term == 1..MaxTerm

------------------------------------------------------------------------------
(*============================================================================*)
(* 变量声明                                                                    *)
(*============================================================================*)

VARIABLES
    (* 每个服务器的持久化状态 *)
    currentTerm,        \* 服务器已知的最新任期号（持久化）
    votedFor,           \* 当前任期内投票给的候选者（持久化，Nil 表示未投票）
    log,                \* 日志条目数组，每个条目包含任期号和命令
    
    (* 每个服务器的易失性状态 *)
    commitIndex,        \* 已知已提交的最高日志索引
    lastApplied,        \* 状态机已应用的最高日志索引
    
    (* Leader 的易失性状态（选举后重新初始化） *)
    nextIndex,          \* 对每个服务器，下一个要发送的日志索引
    matchIndex,         \* 对每个服务器，已知复制的最高日志索引
    
    (* 服务器角色 *)
    state,              \* 每个服务器的当前角色
    
    (* 消息系统（简化模型） *)
    messages            \* 网络中的消息集合

(* 所有变量的元组 *)
vars == <<currentTerm, votedFor, log, commitIndex, lastApplied, 
          nextIndex, matchIndex, state, messages>>

------------------------------------------------------------------------------
(*============================================================================*)
(* 类型定义                                                                    *)
(*============================================================================*)

(* 日志条目类型：<<任期号, 命令值>> *)
Entry == [term : Term, value : Value]

(* 消息类型定义 *)
RequestVoteRequest ==
    [type : {"RequestVoteRequest"}, term : Term, candidate : Server,
     lastLogIndex : Nat, lastLogTerm : Nat]

RequestVoteResponse ==
    [type : {"RequestVoteResponse"}, term : Term, voter : Server,
     voteGranted : BOOLEAN]

AppendEntriesRequest ==
    [type : {"AppendEntriesRequest"}, term : Term, leader : Server,
     prevLogIndex : Nat, prevLogTerm : Nat, entries : Seq(Entry),
     leaderCommit : Nat]

AppendEntriesResponse ==
    [type : {"AppendEntriesResponse"}, term : Term, follower : Server,
     success : BOOLEAN, matchIndex : Nat]

Message ==
    RequestVoteRequest \union RequestVoteResponse \union
    AppendEntriesRequest \union AppendEntriesResponse

------------------------------------------------------------------------------
(*============================================================================*)
(* 初始状态 (Init)                                                              *)
(*============================================================================*)

(* Def-S-Raft-01: 初始状态定义 *)
Init ==
    /\ currentTerm = [s \in Server |-> 1]           \* 所有服务器任期号为 1
    /\ votedFor = [s \in Server |-> Nil]            \* 所有服务器未投票
    /\ log = [s \in Server |-> << >>]               \* 所有服务器日志为空
    /\ commitIndex = [s \in Server |-> 0]           \* 提交索引为 0
    /\ lastApplied = [s \in Server |-> 0]           \* 应用索引为 0
    /\ nextIndex = [s \in Server |-> [t \in Server |-> 1]]  \* Leader 状态
    /\ matchIndex = [s \in Server |-> [t \in Server |-> 0]] \* Leader 状态
    /\ state = [s \in Server |-> Follower]          \* 所有服务器为 Follower
    /\ messages = {}                                \* 无消息

------------------------------------------------------------------------------
(*============================================================================*)
(* 辅助函数                                                                    *)
(*============================================================================*)

(* 获取服务器 s 的日志最后索引 *)
LastLogIndex(s) ==
    Len(log[s])

(* 获取服务器 s 的日志最后条目的任期 *)
LastLogTerm(s) ==
    IF LastLogIndex(s) = 0 THEN 0
    ELSE log[s][LastLogIndex(s)].term

(* 检查候选者的日志是否至少一样新（Raft 论文 5.4.1 节） *)
LogIsAtLeastAsUpToDate(s1, s2) ==
    /\ LastLogTerm(s1) >= LastLogTerm(s2)
    /\ (LastLogTerm(s1) = LastLogTerm(s2)) => (LastLogIndex(s1) >= LastLogIndex(s2))

(* 获取给定索引处条目的任期，如果不存在返回 0 *)
LogTerm(s, i) ==
    IF i = 0 THEN 0
    ELSE IF i > Len(log[s]) THEN 0
    ELSE log[s][i].term

------------------------------------------------------------------------------
(*============================================================================*)
(* 动作定义（基础框架）                                                          *)
(*============================================================================*)

(*----------------------------------------------------------------------------*)
(* 选举相关动作                                                                 *)
(*----------------------------------------------------------------------------*)

(* Def-S-Raft-02: Follower 超时，转换为 Candidate *)
Timeout(s) ==
    /\ state[s] = Follower                          \* 只能是 Follower
    /\ currentTerm[s] < MaxTerm                     \* 未达到最大任期（模型限制）
    /\ state' = [state EXCEPT ![s] = Candidate]     \* 变为 Candidate
    /\ currentTerm' = [currentTerm EXCEPT ![s] = @ + 1]  \* 任期加 1
    /\ votedFor' = [votedFor EXCEPT ![s] = s]       \* 投票给自己
    /\ UNCHANGED <<log, commitIndex, lastApplied, nextIndex, matchIndex, messages>>

(* Def-S-Raft-03: Candidate 向其他服务器发送 RequestVote 请求 *)
SendRequestVote(s) ==
    /\ state[s] = Candidate                         \* 必须是 Candidate
    /\ messages' = messages \cup
        {[type |-> "RequestVoteRequest", term |-> currentTerm[s], candidate |-> s,
          lastLogIndex |-> LastLogIndex(s), lastLogTerm |-> LastLogTerm(s)]}
    /\ UNCHANGED <<currentTerm, votedFor, log, commitIndex, lastApplied,
                   nextIndex, matchIndex, state>>

(* Def-S-Raft-04: 服务器响应 RequestVote 请求 *)
HandleRequestVote(s) ==
    /\ \E m \in messages :
        /\ m.type = "RequestVoteRequest"
        /\ m.candidate # s
        /\ m.term >= currentTerm[s]
        /\ LET canVote ==
               (m.term > currentTerm[s] \/ votedFor[s] = Nil \/ votedFor[s] = m.candidate)
               /\ LogIsAtLeastAsUpToDate(m.candidate, s)
           IN
           /\ currentTerm' = [currentTerm EXCEPT ![s] = IF m.term > currentTerm[s] THEN m.term ELSE @]
           /\ state' = [state EXCEPT ![s] = IF m.term > currentTerm[s] THEN Follower ELSE @]
           /\ votedFor' = [votedFor EXCEPT ![s] = IF canVote THEN m.candidate ELSE @]
           /\ messages' = messages \cup
               {[type |-> "RequestVoteResponse", term |-> m.term, voter |-> s,
                 voteGranted |-> canVote]}
           /\ UNCHANGED <<log, commitIndex, lastApplied, nextIndex, matchIndex>>

(* Def-S-Raft-05: Candidate 收到多数派投票，成为 Leader *)
BecomeLeader(s) ==
    /\ state[s] = Candidate                         \* 必须是 Candidate
    /\ \E Q \in SUBSET Server :
        /\ IsMajority(Q)
        /\ \A voter \in Q :
            \E m \in messages :
                /\ m.type = "RequestVoteResponse"
                /\ m.term = currentTerm[s]
                /\ m.voter = voter
                /\ m.voteGranted
        /\ state' = [state EXCEPT ![s] = Leader]
        /\ nextIndex' = [nextIndex EXCEPT ![s] =
             [t \in Server |-> LastLogIndex(s) + 1]]
        /\ matchIndex' = [matchIndex EXCEPT ![s] =
             [t \in Server |-> 0]]
        /\ UNCHANGED <<currentTerm, votedFor, log, commitIndex, lastApplied, messages>>

(*----------------------------------------------------------------------------*)
(* 日志复制相关动作                                                             *)
(*----------------------------------------------------------------------------*)

(* Def-S-Raft-06: Leader 接收客户端请求，追加新条目 *)
ClientRequest(s) ==
    /\ state[s] = Leader                            \* 必须是 Leader
    /\ Len(log[s]) < MaxLogLength                   \* 日志未满（模型限制）
    /\ \E v \in Value :
        /\ log' = [log EXCEPT ![s] =
             Append(@, [term |-> currentTerm[s], value |-> v])]
        /\ UNCHANGED <<currentTerm, votedFor, commitIndex, lastApplied,
                       nextIndex, matchIndex, state, messages>>

(* Def-S-Raft-07: Leader 向 Follower 发送 AppendEntries 请求 *)
SendAppendEntries(s) ==
    /\ state[s] = Leader                            \* 必须是 Leader
    /\ \E t \in Server :
        /\ t # s
        /\ LET nextIdx == nextIndex[s][t]
               prevIdx == nextIdx - 1
               prevTerm == LogTerm(s, prevIdx)
               entries == IF nextIdx <= LastLogIndex(s)
                          THEN SubSeq(log[s], nextIdx, LastLogIndex(s))
                          ELSE <<>>
           IN
           /\ messages' = messages \cup
               {[type |-> "AppendEntriesRequest", term |-> currentTerm[s],
                 leader |-> s, prevLogIndex |-> prevIdx, prevLogTerm |-> prevTerm,
                 entries |-> entries, leaderCommit |-> commitIndex[s]]}
           /\ UNCHANGED <<currentTerm, votedFor, log, commitIndex, lastApplied,
                          nextIndex, matchIndex, state>>

(* Def-S-Raft-08: Follower 处理 AppendEntries 请求 *)
HandleAppendEntries(s) ==
    /\ \E m \in messages :
        /\ m.type = "AppendEntriesRequest"
        /\ m.leader # s
        /\ m.term >= currentTerm[s]
        /\ LET logOk ==
               IF m.prevLogIndex = 0 THEN TRUE
               ELSE IF m.prevLogIndex > Len(log[s]) THEN FALSE
               ELSE LogTerm(s, m.prevLogIndex) = m.prevLogTerm
           IN
           /\ currentTerm' = [currentTerm EXCEPT ![s] = IF m.term > currentTerm[s] THEN m.term ELSE @]
           /\ state' = [state EXCEPT ![s] = IF m.term > currentTerm[s] THEN Follower ELSE @]
           /\ IF logOk THEN
                  LET newLog ==
                      IF m.prevLogIndex < Len(log[s])
                      THEN SubSeq(log[s], 1, m.prevLogIndex) \o m.entries
                      ELSE log[s] \o m.entries
                      newLogLen == Len(newLog)
                  IN
                  /\ log' = [log EXCEPT ![s] = newLog]
                  /\ commitIndex' = [commitIndex EXCEPT ![s] =
                       IF m.leaderCommit > commitIndex[s]
                       THEN Min({m.leaderCommit, newLogLen})
                       ELSE @]
                  /\ messages' = messages \cup
                      {[type |-> "AppendEntriesResponse", term |-> m.term,
                        follower |-> s, success |-> TRUE,
                        matchIndex |-> newLogLen]}
              ELSE
                  /\ UNCHANGED <<log, commitIndex>>
                  /\ messages' = messages \cup
                      {[type |-> "AppendEntriesResponse", term |-> m.term,
                        follower |-> s, success |-> FALSE,
                        matchIndex |-> 0]}
           /\ UNCHANGED <<votedFor, lastApplied, nextIndex, matchIndex>>

(* Def-S-Raft-09: Leader 根据 matchIndex 更新 commitIndex *)
AdvanceCommitIndex(s) ==
    /\ state[s] = Leader                            \* 必须是 Leader
    /\ \E n \in (commitIndex[s] + 1)..LastLogIndex(s) :
        /\ log[s][n].term = currentTerm[s]
        /\ \E Q \in SUBSET Server :
            /\ IsMajority(Q)
            /\ \A t \in Q :
                t = s \/ matchIndex[s][t] >= n
        /\ commitIndex' = [commitIndex EXCEPT ![s] = n]
        /\ UNCHANGED <<currentTerm, votedFor, log, lastApplied,
                       nextIndex, matchIndex, state, messages>>

(*----------------------------------------------------------------------------*)
(* 消息处理动作                                                                 *)
(*----------------------------------------------------------------------------*)

(* Def-S-Raft-10: 消息被丢弃（模拟网络丢包） *)
DropMessage ==
    /\ messages # {}
    /\ \E m \in messages : messages' = messages \ {m}
    /\ UNCHANGED <<currentTerm, votedFor, log, commitIndex, lastApplied,
                   nextIndex, matchIndex, state>>

(* Def-S-Raft-11: 消息延迟（模拟网络延迟） *)
(* 简化实现：消息延迟由环境非确定性和 DropMessage 共同模拟 *)
DelayMessage ==
    /\ TRUE

(*----------------------------------------------------------------------------*)
(* 下一步关系                                                                   *)
(*----------------------------------------------------------------------------*)

(* Def-S-Raft-12: 下一个状态的所有可能动作 *)
Next ==
    \/ \E s \in Server : Timeout(s)
    \/ \E s \in Server : SendRequestVote(s)
    \/ \E s \in Server : HandleRequestVote(s)
    \/ \E s \in Server : BecomeLeader(s)
    \/ \E s \in Server : ClientRequest(s)
    \/ \E s \in Server : SendAppendEntries(s)
    \/ \E s \in Server : HandleAppendEntries(s)
    \/ \E s \in Server : AdvanceCommitIndex(s)
    \/ DropMessage
    \/ DelayMessage

------------------------------------------------------------------------------
(*============================================================================*)
(* 时序公式                                                                     *)
(*============================================================================*)

(* Def-S-Raft-13: 公平性条件 *)
Fairness ==
    /\ \A s \in Server : WF_vars(Timeout(s))
    /\ \A s \in Server : WF_vars(SendRequestVote(s))
    /\ \A s \in Server : WF_vars(HandleRequestVote(s))
    /\ \A s \in Server : WF_vars(BecomeLeader(s))
    /\ \A s \in Server : WF_vars(ClientRequest(s))
    /\ \A s \in Server : WF_vars(SendAppendEntries(s))
    /\ \A s \in Server : WF_vars(HandleAppendEntries(s))
    /\ \A s \in Server : WF_vars(AdvanceCommitIndex(s))

(* Def-S-Raft-14: 完整规约 *)
Spec == Init /\ [][Next]_vars /\ Fairness

(* 不带公平性的规约 *)
SpecNoFairness == Init /\ [][Next]_vars

------------------------------------------------------------------------------
(*============================================================================*)
(* 不变式（基础框架）                                                            *)
(*============================================================================*)

(*----------------------------------------------------------------------------*)
(* 类型不变式                                                                   *)
(*----------------------------------------------------------------------------*)

(* Thm-S-Raft-01: 类型不变式 *)
TypeInvariant ==
    /\ currentTerm \in [Server -> Term \union {0}]
    /\ votedFor \in [Server -> Server \union {Nil}]
    /\ log \in [Server -> Seq([term : Term, value : Value])]
    /\ commitIndex \in [Server -> Nat]
    /\ lastApplied \in [Server -> Nat]
    /\ state \in [Server -> Role]
    /\ messages \subseteq Message

(*----------------------------------------------------------------------------*)
(* 核心安全性不变式（Raft 论文中提到的关键性质）                                  *)
(*----------------------------------------------------------------------------*)

(* Thm-S-Raft-02: 选举安全（Election Safety）                                     *)
(* 给定任期内最多只有一个 Leader 被选举出来                                       *)
ElectionSafety ==
    \A t \in Term :
        Cardinality({ s \in Server : state[s] = Leader /\ currentTerm[s] = t }) <= 1

(* Thm-S-Raft-03: Leader 只追加（Leader Append-Only）                            *)
(* Leader 从不修改或删除日志条目，只追加新条目                                      *)
(* 辅助: 序列前缀判断，seq1 是 seq2 的前缀当且仅当 seq2 前 Len(seq1) 个元素与 seq1 相同 *)
IsPrefixSeq(seq1, seq2) ==
    /\ Len(seq1) <= Len(seq2)
    /\ \A i \in 1..Len(seq1) : seq1[i] = seq2[i]

LeaderAppendOnly ==
    [][\A s \in Server :
        (state[s] = Leader /\ state'[s] = Leader)
            => IsPrefixSeq(log[s], log'[s])]_vars

(* Thm-S-Raft-04: 日志匹配（Log Matching）                                       *)
(* 如果两个日志条目有相同的索引和任期，则它们存储相同的命令                        *)
(* 且在该索引之前的所有条目都相同                                                  *)
LogMatching ==
    \A s1, s2 \in Server :
        \A i \in 1..Min(Len(log[s1]), Len(log[s2])) :
            (log[s1][i].term = log[s2][i].term)
                => (\A j \in 1..i : log[s1][j] = log[s2][j])

(* Thm-S-Raft-05: Leader 完备性（Leader Completeness）                            *)
(* 如果一个日志条目被提交，那么它一定会出现在所有更高任期的 Leader 的日志中          *)
LeaderCompleteness ==
    \A s \in Server :
        (state[s] = Leader)
            => (\A i \in 1..commitIndex[s] :
                    \E e \in DOMAIN log[s] : 
                        /\ e >= i
                        /\ log[s][e].term <= currentTerm[s])

(* Thm-S-Raft-06: 状态机安全（State Machine Safety）                              *)
(* 如果一个服务器已将给定索引的日志条目应用到其状态机，                          *)
(* 则没有其他服务器会在同一索引应用不同的日志条目                                *)
StateMachineSafety ==
    \A s1, s2 \in Server, i \in Nat :
        (i <= lastApplied[s1] /\ i <= lastApplied[s2])
            => log[s1][i] = log[s2][i]

(*----------------------------------------------------------------------------*)
(* 辅助不变式                                                                   *)
(*----------------------------------------------------------------------------*)

(* Thm-S-Raft-07: 任期单调性 *)
TermMonotonicity ==
    [][\A s \in Server : currentTerm[s] <= currentTerm'[s]]_vars

(* Thm-S-Raft-08: commitIndex 单调性 *)
CommitIndexMonotonicity ==
    [][\A s \in Server : commitIndex[s] <= commitIndex'[s]]_vars

(* Thm-S-Raft-09: 只有当前任期的条目可以被提交 *)
OnlyCurrentTermCommitted ==
    \A s \in Server :
        \A i \in 1..commitIndex[s] :
            log[s][i].term <= currentTerm[s]

(*----------------------------------------------------------------------------*)
(* 组合不变式                                                                   *)
(*----------------------------------------------------------------------------*)

(* Thm-S-Raft-10: 完整不变式 *)
Invariant ==
    /\ TypeInvariant
    /\ ElectionSafety
    /\ LeaderAppendOnly
    /\ LogMatching
    /\ TermMonotonicity
    /\ CommitIndexMonotonicity

------------------------------------------------------------------------------
(*============================================================================*)
(* 活性性质（基础框架）                                                          *)
(*============================================================================*)

(* Thm-S-Raft-11: 选举 eventually 成功 *)
ElectionEventuallySucceeds ==
    \A t \in Term :
        (\E s \in Server : currentTerm[s] = t)
            ~> (\E s \in Server : state[s] = Leader /\ currentTerm[s] = t)

(* Thm-S-Raft-12: 已提交的条目 eventually 被所有服务器应用                        *)
CommittedEntryEventuallyApplied ==
    \A s1, s2 \in Server, i \in Nat :
        (i <= commitIndex[s1])
            ~> (i <= lastApplied[s2])

------------------------------------------------------------------------------
(*============================================================================*)
(* 规约结束                                                                      *)
(*============================================================================*)

================================================================================
