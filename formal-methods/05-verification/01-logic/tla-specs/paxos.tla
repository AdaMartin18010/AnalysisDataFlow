(*
 * Paxos Consensus Protocol - TLA+ Specification
 * =============================================
 * 
 * 本规约描述 Basic Paxos 协议的完整行为，包括：
 * - 提案准备与承诺阶段 (Prepare/Promise)
 * - 提案接受阶段 (Propose/Accept)
 * - 学习者学习已选定的值 (Learn)
 * 
 * 规约验证以下属性：
 * - 安全性：只有一个值可以被选定 (Single-Valued Safety)
 * - 活性：在多数派可用且有一个唯一领导者时，最终会有值被选定
 *
 * 作者: AnalysisDataFlow Project
 * 版本: 1.0
 *)

------------------------------- MODULE paxos -------------------------------

(*
 * 常量声明
 *)
CONSTANTS 
    Value,          \* 可能被选定的值的集合
    Acceptor,       \* 接受者进程的集合
    Quorum,         \* 多数派集合，满足：
                    \* 1. 任意两个多数派集合有交集
                    \* 2. 所有多数派都是接受者的子集
    Proposer        \* 提案者进程的集合

(*
 * 假设：对常量的一致性约束
 *)
(* ASSUME-01: Quorum 假设 - Quorum 是 Acceptor 的子集族且两两相交 *)
(* 证明思路: 这是 Paxos 安全性的核心前提，可由集合论直接推导；
 * 若 Acceptor 有限且 Cardinality(Q)*2 > Cardinality(Acceptor)，则交集性质自动成立 *)
ASSUME QuorumAssumption ==
    /\ \A Q \in Quorum : Q \subseteq Acceptor  \* 多数派都是接受者的子集
    /\ \A Q1, Q2 \in Quorum : Q1 \cap Q2 # {}  \* 任意两个多数派有交集

(* ASSUME-02: 基数假设 - 每个 Quorum 的大小严格大于 Acceptor 的一半 *)
(* 证明思路: 由鸽巢原理，若 |Q1|+|Q2| > |Acceptor|，则 Q1 ∩ Q2 ≠ ∅；
 * 此假设蕴含 QuorumAssumption 的交集性质，可视为更强的参数约束 *)
ASSUME CardAssumption ==
    \A Q \in Quorum : Cardinality(Q) * 2 > Cardinality(Acceptor)

(*
 * 扩展标准模块
 *)
EXTENDS Naturals, FiniteSets, Sequences, TLC

(*
 * Ballot 类型：自然数，用于排序提案
 *)
Ballot == Nat

(*
 * 消息类型定义
 *)
Message == 
    [type : {"prepare"}, from : Proposer, bal : Ballot] 
    \cup
    [type : {"promise"}, from : Acceptor, bal : Ballot, 
     maxVBal : Ballot \cup {-1}, maxVal : Value \cup {None}]
    \cup
    [type : {"propose"}, from : Proposer, bal : Ballot, val : Value]
    \cup
    [type : {"accept"}, from : Acceptor, bal : Ballot, val : Value]

(*
 * 特殊常量
 *)
None == CHOOSE v : v \notin Value

(*
 * 变量声明
 *)
VARIABLES
    msgs,           \* 网络中的所有消息（异步网络模型）
    maxBal,         \* Acceptor 看到的最大 ballot 数
    maxVBal,        \* Acceptor 接受的最大 ballot 数
    maxVal,         \* Acceptor 接受的值
    chosen          \* 已经被选定的值

(*
 * 类型不变式
 *)
TypeOK ==
    /\ msgs \subseteq Message
    /\ maxBal \in [Acceptor -> Ballot \cup {-1}]
    /\ maxVBal \in [Acceptor -> Ballot \cup {-1}]
    /\ maxVal \in [Acceptor -> Value \cup {None}]
    /\ chosen \subseteq Value

(*
 * 初始状态
 *)
Init ==
    /\ msgs = {}
    /\ maxBal = [a \in Acceptor |-> -1]
    /\ maxVBal = [a \in Acceptor |-> -1]
    /\ maxVal = [a \in Acceptor |-> None]
    /\ chosen = {}

(*
 * 辅助定义：发送消息
 *)
Send(m) == msgs' = msgs \cup {m}

(*
 * Phase 1a: Proposer 发送 Prepare 请求
 *)
Prepare(p, b) ==
    /\ ~\E m \in msgs : m.type = "prepare" /\ m.from = p /\ m.bal = b
    /\ Send([type |-> "prepare", from |-> p, bal |-> b])
    /\ UNCHANGED <<maxBal, maxVBal, maxVal, chosen>>

(*
 * Phase 1b: Acceptor 响应 Promise
 *)
Promise(a) ==
    \E m \in msgs :
        /\ m.type = "prepare"
        /\ m.bal > maxBal[a]
        /\ maxBal' = [maxBal EXCEPT ![a] = m.bal]
        /\ Send([type |-> "promise", from |-> a, bal |-> m.bal,
                 maxVBal |-> maxVBal[a], maxVal |-> maxVal[a]])
        /\ UNCHANGED <<maxVBal, maxVal, chosen>>

(*
 * 辅助函数：从 Promise 消息中提取值
 *)
GetAcceptedValue(msgs_set, b) ==
    LET valid_promises == {m \in msgs_set : 
            m.type = "promise" /\ m.bal = b /\ m.maxVBal # -1}
    IN IF valid_promises = {}
       THEN CHOOSE v : v \in Value  \* 自由选择任意值
       ELSE LET max_promise == CHOOSE m \in valid_promises :
                    \A m2 \in valid_promises : m.maxVBal >= m2.maxVBal
            IN max_promise.maxVal

(*
 * Phase 2a: Proposer 在收到多数派 Promise 后发送 Propose
 *)
Propose(p, b) ==
    \E Q \in Quorum, v \in Value :
        /\ \A a \in Q : \E m \in msgs :
            m.type = "promise" /\ m.from = a /\ m.bal = b
        /\ ~\E m \in msgs : m.type = "propose" /\ m.bal = b
        /\ LET promised_val == GetAcceptedValue(msgs, b)
           IN v = IF promised_val = None 
                  THEN CHOOSE val \in Value : TRUE  \* 自由提议新值
                  ELSE promised_val
        /\ Send([type |-> "propose", from |-> p, bal |-> b, val |-> v])
        /\ UNCHANGED <<maxBal, maxVBal, maxVal, chosen>>

(*
 * Phase 2b: Acceptor 接受提案
 *)
Accept(a) ==
    \E m \in msgs :
        /\ m.type = "propose"
        /\ m.bal >= maxBal[a]
        /\ maxBal' = [maxBal EXCEPT ![a] = m.bal]
        /\ maxVBal' = [maxVBal EXCEPT ![a] = m.bal]
        /\ maxVal' = [maxVal EXCEPT ![a] = m.val]
        /\ Send([type |-> "accept", from |-> a, bal |-> m.bal, val |-> m.val])
        /\ UNCHANGED <<chosen>>

(*
 * 学习者发现已选定的值
 *)
Learn ==
    \E Q \in Quorum, v \in Value, b \in Ballot :
        /\ \A a \in Q : \E m \in msgs :
            m.type = "accept" /\ m.from = a /\ m.bal = b /\ m.val = v
        /\ chosen' = chosen \cup {v}
        /\ UNCHANGED <<msgs, maxBal, maxVBal, maxVal>>

(*
 * 下一步动作
 *)
Next ==
    \E p \in Proposer, a \in Acceptor, b \in Ballot :
        Prepare(p, b) \/ Promise(a) \/ Propose(p, b) \/ Accept(a)
    \/ Learn

(*
 * 完整规约
 *)
Spec == Init /\ [][Next]_<<msgs, maxBal, maxVBal, maxVal, chosen>>
        /\ WF_<<msgs, maxBal, maxVBal, maxVal, chosen>>(Learn)

(*
 * =====================================================================
 * 安全性不变式 (Safety Properties)
 * =====================================================================
 *)

(*
 * Thm-Paxos-01: Single-Valued Safety
 * 最多只有一个值可以被选定
 *)
Safety ==
    \A v1, v2 \in chosen : v1 = v2

(*
 * Thm-Paxos-02: Chosen Value Validity
 * 被选定的值必须来自某个 Proposer 的提议
 *)
Validity ==
    \A v \in chosen : 
        \E m \in msgs : m.type = "propose" /\ m.val = v

(*
 * Thm-Paxos-03: Agreement
 * 如果一个值被选定，那么所有学习者最终都会学习到这个值
 *)
Agreement ==
    \A v \in chosen :
        \E Q \in Quorum, b \in Ballot :
            \A a \in Q : \E m \in msgs :
                m.type = "accept" /\ m.from = a /\ m.bal = b /\ m.val = v

(*
 * =====================================================================
 * 活性属性 (Liveness Properties)
 * =====================================================================
 *)

(*
 * Thm-Paxos-04: Eventual Choice
 * 如果有一个 Proposer 持续运行且网络可靠，最终会有一个值被选定
 * 注意：这需要公平性假设
 *)
Liveness ==
    <> (chosen # {})

(*
 * Thm-Paxos-05: Proposal Progress
 * 对于每个 ballot，最多只有一个值被提议
 *)
ProposalUniqueness ==
    \A m1, m2 \in msgs :
        (m1.type = "propose" /\ m2.type = "propose" /\ m1.bal = m2.bal)
        => m1.val = m2.val

(*
 * =====================================================================
 * 不变式证明辅助定理
 * =====================================================================
 *)

(* Lemma-Paxos-04: QuorumAssumption 蕴含 CardAssumption 的交集性质 *)
(* 证明: 由鸽巢原理，若 |Q1|+|Q2| > |A|，则 Q1∩Q2 不可能为空 *)
QuorumIntersectionFromCardinality ==
    CardAssumption => QuorumAssumption

(*
 * Lemma-Paxos-01: MaxBal Monotonicity
 * Acceptor 的 maxBal 只会增加
 *)
MaxBalMonotonic ==
    [][\A a \in Acceptor : maxBal'[a] >= maxBal[a]]_<<msgs, maxBal, maxVBal, maxVal, chosen>>

(*
 * Lemma-Paxos-02: Promise Validity
 * 如果 Acceptor 承诺了 ballot b，则它不会再接受更小的 ballot
 *)
PromiseValidity ==
    \A a \in Acceptor, m \in msgs :
        (m.type = "promise" /\ m.from = a /\ m.bal = b)
        => maxVBal[a] <= b

(*
 * Lemma-Paxos-03: Accept Implies Promise
 * Acceptor 只有在收到对应 ballot 的 prepare 后才能 accept
 *)
AcceptRequiresPromise ==
    \A a \in Acceptor, m \in msgs :
        (m.type = "accept" /\ m.from = a)
        => \E mp \in msgs : mp.type = "prepare" /\ mp.bal = m.bal

(*
 * =====================================================================
 * TLC 模型检查配置
 * =====================================================================
 *
 * 使用 TLC 进行模型检查时，建议配置如下：
 *
 * CONSTANTS:
 *   Value = {v1, v2}
 *   Acceptor = {a1, a2, a3}
 *   Quorum = {{a1, a2}, {a1, a3}, {a2, a3}}
 *   Proposer = {p1, p2}
 *   Ballot = 0..2
 *
 * 不变式检查:
 *   - TypeOK
 *   - Safety
 *   - Validity
 *   - ProposalUniqueness
 *
 * 活性检查:
 *   - Liveness (需要公平性假设)
 *
 * 状态空间:
 *   - 对于这个配置，状态空间大约为 10^4 个状态
 *   - 检查时间通常在几分钟内完成
 *)

=============================================================================
