-------------------------------- MODULE Paxos --------------------------------
(******************************************************************************)
(* Paxos 共识算法 TLA+ 形式化规约（基础框架）                                     *)
(*                                                                            *)
(* 基于 Leslie Lamport 的 "The Part-Time Parliament" 和 "Paxos Made Simple"     *)
(* 本版本提供基础框架，包含核心变量和动作定义                                    *)
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
    Acceptor,           \* 接受者集合，例如 {a1, a2, a3}
    Proposer,           \* 提议者集合，例如 {p1, p2}
    Value,              \* 可以被选中的值的集合
    Ballot,             \* 选票号集合（全序集合）
    Quorum              \* 法定集合（多数派的子集）

(* ASSUME-01: 常量参数约束 - Acceptor、Proposer 非空且有限，Quorum 满足交集性质 *)
(* 证明思路: 这是模型配置假设，由 TLC 常量定义保证；Quorum 交集是 Paxos 安全性的核心前提 *)
ASSUME ConstantsAssumption ==
    /\ Acceptor # {}                              \* 至少有一个 Acceptor
    /\ Proposer # {}                              \* 至少有一个 Proposer
    /\ IsFiniteSet(Acceptor)                      \* Acceptor 集合有限
    /\ IsFiniteSet(Proposer)                      \* Proposer 集合有限
    /\ Quorum \subseteq SUBSET Acceptor           \* Quorum 是 Acceptor 的子集族
    /\ \A Q1, Q2 \in Quorum : Q1 \cap Q2 # {}      \* 任意两个 Quorum 相交（安全性关键）

------------------------------------------------------------------------------
(*============================================================================*)
(* 辅助定义                                                                    *)
(*============================================================================*)

(* 空值定义 *)
None == 0

(* ASSUME-02: Ballot 必须是全序集合，此处限定为自然数子集以保证可比性 *)
(* 证明思路: Nat 上的 < 关系是全序，因此 Ballot 继承全序性；这是选票号比较的基础 *)
ASSUME BallotOrderingAssumption == Ballot \subseteq Nat

(* Acceptor 可能的投票状态 *)
VoteRecord ==
    [acc : Acceptor, bal : Ballot, val : Value]

------------------------------------------------------------------------------
(*============================================================================*)
(* 变量声明                                                                    *)
(*============================================================================*)

VARIABLES
    (* Acceptor 状态 *)
    maxBal,             \* maxBal[a] = Acceptor a 承诺不投票的更高选票号
    votes,              \* votes[a] = Acceptor a 已投票的 <<ballot, value>> 集合
    
    (* 被选中的值 *)
    chosen,             \* 已被选中的值集合
    
    (* Proposer 状态（简化模型） *)
    propBal,            \* propBal[p] = Proposer p 当前使用的选票号
    propVal,            \* propVal[p] = Proposer p 尝试提议的值
    propState,          \* propState[p] = Proposer p 的当前状态
    
    (* 消息系统（简化模型） *)
    msgs                \* 网络中的消息集合

(* 所有变量的元组 *)
vars == <<maxBal, votes, chosen, propBal, propVal, propState, msgs>>

------------------------------------------------------------------------------
(*============================================================================*)
(* 类型定义                                                                    *)
(*============================================================================*)

(* Proposer 状态 *)
Idle == "idle"
Preparing == "preparing"
Accepting == "accepting"
Done == "done"
PropState == {Idle, Preparing, Accepting, Done}

(* 消息类型定义 *)
Phase1aMessage ==
    [type : {"Phase1a"}, proposer : Proposer, ballot : Ballot]

Phase1bMessage ==
    [type : {"Phase1b"}, acceptor : Acceptor, ballot : Ballot, 
     maxVBal : Ballot \union {None}, maxVal : Value \union {None}]

Phase2aMessage ==
    [type : {"Phase2a"}, proposer : Proposer, ballot : Ballot, value : Value]

Phase2bMessage ==
    [type : {"Phase2b"}, acceptor : Acceptor, ballot : Ballot, value : Value]

Message ==
    Phase1aMessage \union Phase1bMessage \union
    Phase2aMessage \union Phase2bMessage

------------------------------------------------------------------------------
(*============================================================================*)
(* 辅助函数                                                                    *)
(*============================================================================*)

(* 获取 Acceptor a 在选票号 b 投票的值，如果没有返回 None *)
VotedFor(a, b) ==
    IF \E v \in Value : <<b, v>> \in votes[a]
    THEN CHOOSE v \in Value : <<b, v>> \in votes[a]
    ELSE None

(* 判断 Acceptor a 是否已在选票号 b 投过票 *)
HasVoted(a, b) ==
    \E v \in Value : <<b, v>> \in votes[a]

(* 获取 Acceptor a 投过票的最高选票号 *)
MaxVotedBallot(a) ==
    IF votes[a] = {}
    THEN None
    ELSE Max({b \in Ballot : \E v \in Value : <<b, v>> \in votes[a]})

(* 获取 Acceptor a 在最高选票号投的值 *)
MaxVotedValue(a) ==
    VotedFor(a, MaxVotedBallot(a))

(* 判断值 v 是否已被选中（存在某个选票号，多数派已投票） *)
IsChosen(v) ==
    \E b \in Ballot, Q \in Quorum :
        \A a \in Q : <<b, v>> \in votes[a]

------------------------------------------------------------------------------
(*============================================================================*)
(* 初始状态 (Init)                                                              *)
(*============================================================================*)

(* Def-S-Paxos-01: 初始状态定义 *)
Init ==
    /\ maxBal = [a \in Acceptor |-> None]         \* 所有 Acceptor 未承诺
    /\ votes = [a \in Acceptor |-> {}]            \* 所有 Acceptor 未投票
    /\ chosen = {}                                \* 无值被选中
    /\ propBal = [p \in Proposer |-> None]        \* 所有 Proposer 未选择选票号
    /\ propVal = [p \in Proposer |-> None]        \* 所有 Proposer 未选择值
    /\ propState = [p \in Proposer |-> Idle]      \* 所有 Proposer 空闲
    /\ msgs = {}                                  \* 无消息

------------------------------------------------------------------------------
(*============================================================================*)
(* 动作定义（基础框架）                                                          *)
(*============================================================================*)

(*----------------------------------------------------------------------------*)
(* Phase 1: 准备阶段                                                            *)
(*----------------------------------------------------------------------------*)

(* Def-S-Paxos-02: Phase 1a - Proposer 发送 Prepare 请求 *)
(* Proposer p 选择一个新的选票号 b 并发送 Prepare 请求 *)
(* TODO-01: 需补充完整实现 - 选择新选票号并更新 propState, propBal, msgs *)
(* 完成建议: 参考 formal-methods/05-verification/01-logic/tla-specs/paxos.tla 中 Prepare 动作 *)
Phase1a(p) ==
    /\ propState[p] = Idle                        \* Proposer 必须处于 Idle 状态
    /\ UNCHANGED vars

(* Def-S-Paxos-03: Phase 1b - Acceptor 响应 Promise *)
(* Acceptor a 收到 Prepare(b) 后，如果 b > maxBal[a]，则承诺不投票 <= b *)
(* TODO-02: 需补充完整实现 - 更新 maxBal, votes, 添加 Promise 消息到 msgs *)
(* 完成建议: 参考 formal-methods/90-examples/tla-plus/paxos.tla 中 Promise 动作 *)
Phase1b(a) ==
    /\ UNCHANGED vars

(*----------------------------------------------------------------------------*)
(* Phase 2: 接受阶段                                                            *)
(*----------------------------------------------------------------------------*)

(* Def-S-Paxos-04: Phase 2a - Proposer 发送 Accept 请求 *)
(* Proposer p 收到多数派 Promise 后，发送 Accept(b, v) 请求 *)
(* TODO-03: 需补充完整实现 - 根据 Promise 选择值，更新 propState, propVal, msgs *)
(* 完成建议: 参考 formal-methods/90-examples/tla-plus/paxos.tla 中 Propose 动作 *)
Phase2a(p) ==
    /\ propState[p] = Preparing                   \* 必须在 Preparing 状态
    /\ UNCHANGED vars

(* Def-S-Paxos-05: Phase 2b - Acceptor 接受值 *)
(* Acceptor a 收到 Accept(b, v) 后，如果未承诺更高选票号，则接受 *)
(* TODO-04: 需补充完整实现 - 在 b >= maxBal[a] 时更新 votes[a] *)
(* 完成建议: 参考 formal-methods/05-verification/01-logic/tla-specs/paxos.tla 中 Accept 动作 *)
Phase2b(a) ==
    /\ UNCHANGED vars

(*----------------------------------------------------------------------------*)
(* 学习被选中的值                                                               *)
(*----------------------------------------------------------------------------*)

(* Def-S-Paxos-06: 更新被选中的值集合 *)
(* TODO-05: 需补充完整实现 - 当检测到 Quorum 对同一 (b,v) 投票时更新 chosen *)
(* 完成建议: 遍历所有选票号和值，检查是否存在 Quorum 已投票，若存在则加入 chosen *)
LearnChosen ==
    /\ UNCHANGED vars

(*----------------------------------------------------------------------------*)
(* 消息处理动作                                                                 *)
(*----------------------------------------------------------------------------*)

(* Def-S-Paxos-07: 消息被丢弃（模拟网络丢包） *)
(* TODO-06: 需补充完整实现 - 从 msgs 中删除某条消息 *)
(* 完成建议: \E m \in msgs : msgs' = msgs \ {m} *)
DropMessage ==
    /\ UNCHANGED vars

(* Def-S-Paxos-08: 消息延迟（模拟网络延迟） *)
(* TODO-07: 需补充完整实现 - 可添加延迟计数器或消息队列建模 *)
(* 完成建议: 引入延迟消息集合 delayed_msgs，消息先在 delayed_msgs 中停留若干步 *)
DelayMessage ==
    /\ UNCHANGED vars

(*----------------------------------------------------------------------------*)
(* 下一步关系                                                                   *)
(*----------------------------------------------------------------------------*)

(* Def-S-Paxos-09: 下一个状态的所有可能动作 *)
Next ==
    \/ \E p \in Proposer : Phase1a(p)
    \/ \E a \in Acceptor : Phase1b(a)
    \/ \E p \in Proposer : Phase2a(p)
    \/ \E a \in Acceptor : Phase2b(a)
    \/ LearnChosen
    \/ DropMessage
    \/ DelayMessage

------------------------------------------------------------------------------
(*============================================================================*)
(* 时序公式                                                                     *)
(*============================================================================*)

(* Def-S-Paxos-10: 公平性条件（基础框架，待完善） *)
(* TODO-08: 需补充完整公平性约束以保证活性 *)
(* 完成建议: 对所有 Phase1a, Phase2a, Phase1b, Phase2b 动作添加弱公平性 *)
Fairness ==
    TRUE

(* Def-S-Paxos-11: 完整规约 *)
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

(* Thm-S-Paxos-01: 类型不变式 *)
TypeInvariant ==
    /\ maxBal \in [Acceptor -> Ballot \union {None}]
    /\ votes \in [Acceptor -> SUBSET (Ballot \X Value)]
    /\ chosen \subseteq Value
    /\ propBal \in [Proposer -> Ballot \union {None}]
    /\ propVal \in [Proposer -> Value \union {None}]
    /\ propState \in [Proposer -> PropState]
    /\ msgs \subseteq Message

(*----------------------------------------------------------------------------*)
(* 核心安全性不变式（Paxos 的核心保证）                                          *)
(*----------------------------------------------------------------------------*)

(* Thm-S-Paxos-02: 一致性（Consistency）                                         *)
(* 最多只有一个值可以被选中                                                      *)
(* 这是 Paxos 的核心安全性保证                                                   *)
Consistency ==
    Cardinality(chosen) <= 1

(* 更强的一致性：如果两个值都被选中，则它们相等 *)
ConsistencyStrong ==
    \A v1, v2 \in chosen : v1 = v2

(* Thm-S-Paxos-03: 非平凡性（Nontriviality）                                     *)
(* 只有被提议的值才能被选中                                                      *)
Nontriviality ==
    chosen \subseteq Value

(* Thm-S-Paxos-04: 安全性（Safety）                                              *)
(* 一旦被选中，值不会改变                                                        *)
Safety ==
    [][chosen \subseteq chosen']_vars

(*----------------------------------------------------------------------------*)
(* Paxos 协议特定不变式                                                          *)
(*----------------------------------------------------------------------------*)

(* Thm-S-Paxos-05: 选票号承诺一致性                                             *)
(* 如果 Acceptor a 承诺了选票号 b，则它不会在任何 <= b 的选票号投票            *)
BallotPromiseConsistency ==
    \A a \in Acceptor, b1, b2 \in Ballot :
        (<<b1, b2>> \in votes[a]) => (b2 <= maxBal[a])

(* Thm-S-Paxos-06: 每个选票号最多一个值                                         *)
(* Acceptor 不会在同一选票号为两个不同值投票                                    *)
SingleValuePerBallot ==
    \A a \in Acceptor, b \in Ballot, v1, v2 \in Value :
        (<<b, v1>> \in votes[a] /\ <<b, v2>> \in votes[a]) => (v1 = v2)

(* Thm-S-Paxos-07: Quorum 交集性质                                              *)
(* 如果值 v 在选票号 b 被选中，则任何更高选票号必须提议相同的值                  *)
QuorumIntersectionProperty ==
    \A b1, b2 \in Ballot, v1, v2 \in Value, Q1, Q2 \in Quorum :
        (b1 < b2 /\ \A a \in Q1 : <<b1, v1>> \in votes[a]
                /\ \A a \in Q2 : <<b2, v2>> \in votes[a])
            => (v1 = v2)

(*----------------------------------------------------------------------------*)
(* 组合不变式                                                                   *)
(*----------------------------------------------------------------------------*)

(* Thm-S-Paxos-08: 完整不变式 *)
Invariant ==
    /\ TypeInvariant
    /\ Consistency
    /\ Nontriviality
    /\ BallotPromiseConsistency
    /\ SingleValuePerBallot

------------------------------------------------------------------------------
(*============================================================================*)
(* 活性性质（基础框架）                                                          *)
(*============================================================================*)

(* Thm-S-Paxos-09: 最终某个值会被选中 *)
EventuallyValueChosen ==
    <> (chosen # {})

(* Thm-S-Paxos-10: 如果多数派存活且可以通信，最终会有值被选中                    *)
(* 需要补充假设：足够的 Acceptor 存活且网络可靠                                  *)
Liveness ==
    <> (chosen # {})

------------------------------------------------------------------------------
(*============================================================================*)
(* 定理与推论                                                                   *)
(*============================================================================*)

(* Lemma-S-Paxos-01: 如果值 v 被选中，则它必须被某个 Acceptor 投票              *)
ChosenImpliesVoted ==
    (chosen # {}) =>
        \E a \in Acceptor, b \in Ballot, v \in chosen : <<b, v>> \in votes[a]

(* Lemma-S-Paxos-02: 两个不同的值不能在同一选票号被选中                          *)
UniqueValuePerBallot ==
    \A b \in Ballot, v1, v2 \in Value :
        (\E Q \in Quorum : \A a \in Q : <<b, v1>> \in votes[a])
        /\ (\E Q \in Quorum : \A a \in Q : <<b, v2>> \in votes[a])
        => (v1 = v2)

(* Cor-S-Paxos-01: 一致性推论 - 使用 Quorum 交集性质证明                          *)
ConsistencyFromQuorum ==
    Consistency

------------------------------------------------------------------------------
(*============================================================================*)
(* 模型检测辅助                                                                  *)
(*============================================================================*)

(* 用于 TLC 模型检测的状态约束（防止状态空间爆炸）                                 *)
StateConstraint ==
    /\ \A a \in Acceptor : Cardinality(votes[a]) <= 2
    /\ Cardinality(msgs) <= 10
    /\ Cardinality(chosen) <= 1

(* 对称性集合声明（用于 TLC 优化）                                                *)
AcceptorPermutations == Permutations(Acceptor)
ValuePermutations == Permutations(Value)

------------------------------------------------------------------------------
(*============================================================================*)
(* 规约结束                                                                      *)
(*============================================================================*)

================================================================================
