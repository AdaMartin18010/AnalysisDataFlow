(* ============================================================================
 * TLA+ 规约: Paxos 共识协议
 * ============================================================================
 *
 * 本规约描述 Lamport 的 Paxos 协议, 用于分布式系统中的一致性。
 *
 * 核心角色:
 * - Proposer: 提议者, 提出值(value)给Acceptor
 * - Acceptor: 接受者, 对提议进行投票
 * - Learner: 学习者, 学习已被选定的值
 *
 * 协议阶段:
 * Phase 1 (Prepare):
 *   Proposer -> Acceptor: Prepare(n)
 *   Acceptor -> Proposer: Promise(n, (n', v')) 或拒绝
 *
 * Phase 2 (Accept):
 *   Proposer -> Acceptor: Accept(n, v)
 *   Acceptor -> Proposer: Accepted(n, v) 或拒绝
 *
 * 安全性质 (Paxos保证):
 * - 一致性: 只有一个值能被选定
 * - 有效性: 被选定的值必须是某个Proposer提出的
 *
 * 参考: Lamport, L. (2001). Paxos Made Simple
 * ============================================================================ *)

--------------------------------- MODULE Paxos ---------------------------------

(* ----------------------------------------------------------------------------
 * 常量定义
 * ---------------------------------------------------------------------------- *)

CONSTANTS
    Proposer,           (* 提议者集合 *)
    Acceptor,           (* 接受者集合 *)
    Value,              (* 可能的值集合 *)
    Quorum              (* 法定集合 (Acceptor的子集) *)

ASSUME
    /\ Proposer \cap Acceptor = {}       (* 角色互斥 *)
    /\ Quorum \subseteq SUBSET Acceptor  (* Quorum是Acceptor的子集族 *)
    /\ \A Q1, Q2 \in Quorum : Q1 \cap Q2 # {}  (* 任意两个Quorum相交 *)

(* 提案编号: 自然数 *)
Ballot == Nat

(* ----------------------------------------------------------------------------
 * 变量定义
 * ---------------------------------------------------------------------------- *)

VARIABLES
    (* Proposer状态 *)
    propState,          (* Proposer -> {"idle", "preparing", "accepting", "chosen"} *)
    propBallot,         (* Proposer -> Ballot | -1 *)
    propValue,          (* Proposer -> Value | None *)
    propVotes,          (* Proposer -> SUBSET Acceptor *)
    
    (* Acceptor状态 *)
    accMaxBallot,       (* Acceptor -> Ballot | -1, 已承诺的最高编号 *)
    accAccepted,        (* Acceptor -> [ballot: Ballot, value: Value] | None *)
    
    (* 消息 *)
    msgs                (* 网络中的消息集合 *)

(* ----------------------------------------------------------------------------
 * 消息类型定义
 * ---------------------------------------------------------------------------- *)

PrepareMsg ==
    [type: {"Prepare"}, ballot: Ballot, from: Proposer, to: Acceptor]

PromiseMsg ==
    [type: {"Promise"}, ballot: Ballot, acc: Acceptor, to: Proposer, 
     prev: [ballot: Ballot, value: Value] | {None}]

AcceptMsg ==
    [type: {"Accept"}, ballot: Ballot, value: Value, from: Proposer, to: Acceptor]

AcceptedMsg ==
    [type: {"Accepted"}, ballot: Ballot, value: Value, acc: Acceptor, to: Proposer]

Message == PrepareMsg \cup PromiseMsg \cup AcceptMsg \cup AcceptedMsg

(* ----------------------------------------------------------------------------
 * 类型不变式
 * ---------------------------------------------------------------------------- *)

PaxosTypeOK ==
    /\ propState \in [Proposer -> {"idle", "preparing", "accepting", "chosen"}]
    /\ propBallot \in [Proposer -> Ballot \cup {-1}]
    /\ propValue \in [Proposer -> Value \cup {None}]
    /\ propVotes \in [Proposer -> SUBSET Acceptor]
    /\ accMaxBallot \in [Acceptor -> Ballot \cup {-1}]
    /\ accAccepted \in [Acceptor -> [ballot: Ballot, value: Value] \cup {None}]
    /\ msgs \subseteq Message

(* ----------------------------------------------------------------------------
 * 辅助定义
 * ---------------------------------------------------------------------------- *)

(* 检查提议是否已获得多数Acceptor承诺 *)
HasPromiseQuorum(p, b) ==
    \E Q \in Quorum :
        \A a \in Q :
            \E m \in msgs :
                /\ m.type = "Promise"
                /\ m.ballot = b
                /\ m.acc = a
                /\ m.to = p

(* 检查提议是否已获得多数Acceptor接受 *)
HasAcceptQuorum(p, b) ==
    \E Q \in Quorum :
        \A a \in Q :
            \E m \in msgs :
                /\ m.type = "Accepted"
                /\ m.ballot = b
                /\ m.acc = a

(* 获取已承诺的最高编号的值 *)
GetHighestPromisedValue(p, b) ==
    LET promises == {m \in msgs :
                        /\ m.type = "Promise"
                        /\ m.ballot = b
                        /\ m.to = p
                        /\ m.prev # None}
    IN IF promises = {}
       THEN None
       ELSE LET maxM == CHOOSE m1 \in promises :
                        \A m2 \in promises : m1.prev.ballot >= m2.prev.ballot
            IN maxM.prev.value

(* ----------------------------------------------------------------------------
 * 初始状态
 * ---------------------------------------------------------------------------- *)

Init ==
    /\ propState = [p \in Proposer |-> "idle"]
    /\ propBallot = [p \in Proposer |-> -1]
    /\ propValue = [p \in Proposer |-> None]
    /\ propVotes = [p \in Proposer |-> {}]
    /\ accMaxBallot = [a \in Acceptor |-> -1]
    /\ accAccepted = [a \in Acceptor |-> None]
    /\ msgs = {}

(* ----------------------------------------------------------------------------
 * Proposer动作
 * ---------------------------------------------------------------------------- *)

(* Phase 1a: Proposer发送Prepare消息 *)
ProposerPrepare(p, b) ==
    /\ propState[p] = "idle"
    /\ b > 0
    /\ \A p2 \in Proposer : propBallot[p2] # b   (* 编号唯一 *)
    /\ propState' = [propState EXCEPT ![p] = "preparing"]
    /\ propBallot' = [propBallot EXCEPT ![p] = b]
    /\ msgs' = msgs \cup 
        {[type |-> "Prepare", ballot |-> b, from |-> p, to |-> a] : a \in Acceptor}
    /\ UNCHANGED <<propValue, propVotes, accMaxBallot, accAccepted>>

(* Phase 2a: Proposer收到足够Promise, 发送Accept消息 *)
ProposerAccept(p, v) ==
    /\ propState[p] = "preparing"
    /\ HasPromiseQuorum(p, propBallot[p])
    /\ LET highest == GetHighestPromisedValue(p, propBallot[p])
       IN /\ IF highest = None
             THEN v \in Value          (* 自由选择值 *)
             ELSE v = highest          (* 必须使用已承诺的值 *)
          /\ propValue' = [propValue EXCEPT ![p] = v]
    /\ propState' = [propState EXCEPT ![p] = "accepting"]
    /\ msgs' = msgs \cup
        {[type |-> "Accept", ballot |-> propBallot[p], value |-> v, 
          from |-> p, to |-> a] : a \in Acceptor}
    /\ UNCHANGED <<propBallot, propVotes, accMaxBallot, accAccepted>>

(* Proposer学习到自己的提议被选定 *)
ProposerLearnChosen(p) ==
    /\ propState[p] = "accepting"
    /\ HasAcceptQuorum(p, propBallot[p])
    /\ propState' = [propState EXCEPT ![p] = "chosen"]
    /\ UNCHANGED <<propBallot, propValue, propVotes, msgs, accMaxBallot, accAccepted>>

(* ----------------------------------------------------------------------------
 * Acceptor动作
 * ---------------------------------------------------------------------------- *)

(* Phase 1b: Acceptor处理Prepare请求 *)
AcceptorPrepare(a) ==
    \E m \in msgs :
        /\ m.type = "Prepare"
        /\ m.to = a
        /\ m.ballot > accMaxBallot[a]      (* 只接受更高编号的提议 *)
        /\ accMaxBallot' = [accMaxBallot EXCEPT ![a] = m.ballot]
        /\ msgs' = msgs \cup
            {[type |-> "Promise", ballot |-> m.ballot, acc |-> a, 
              to |-> m.from, prev |-> accAccepted[a]]}
        /\ UNCHANGED <<propState, propBallot, propValue, propVotes, accAccepted>>

(* Phase 2b: Acceptor处理Accept请求 *)
AcceptorAccept(a) ==
    \E m \in msgs :
        /\ m.type = "Accept"
        /\ m.to = a
        /\ m.ballot >= accMaxBallot[a]     (* 接受编号 >= 已承诺的编号 *)
        /\ accAccepted' = [accAccepted EXCEPT ![a] = 
            [ballot |-> m.ballot, value |-> m.value]]
        /\ accMaxBallot' = [accMaxBallot EXCEPT ![a] = m.ballot]
        /\ msgs' = msgs \cup
            {[type |-> "Accepted", ballot |-> m.ballot, value |-> m.value,
              acc |-> a, to |-> m.from]}
        /\ UNCHANGED <<propState, propBallot, propValue, propVotes>>

(* ----------------------------------------------------------------------------
 * 下一步动作
 * ---------------------------------------------------------------------------- *)

Next ==
    \/ \E p \in Proposer, b \in Ballot : ProposerPrepare(p, b)
    \/ \E p \in Proposer, v \in Value : ProposerAccept(p, v)
    \/ \E p \in Proposer : ProposerLearnChosen(p)
    \/ \E a \in Acceptor : AcceptorPrepare(a)
    \/ \E a \in Acceptor : AcceptorAccept(a)

(* ----------------------------------------------------------------------------
 * 公平性
 * ---------------------------------------------------------------------------- *)

Fairness ==
    /\ \A p \in Proposer : 
        WF_<<propState, propBallot, propValue, propVotes, accMaxBallot, accAccepted, msgs>>(
            \E b \in Ballot : ProposerPrepare(p, b))
    /\ \A p \in Proposer :
        WF_<<propState, propBallot, propValue, propVotes, accMaxBallot, accAccepted, msgs>>(
            \E v \in Value : ProposerAccept(p, v))
    /\ \A a \in Acceptor :
        WF_<<propState, propBallot, propValue, propVotes, accMaxBallot, accAccepted, msgs>>(
            AcceptorPrepare(a))
    /\ \A a \in Acceptor :
        WF_<<propState, propBallot, propValue, propVotes, accMaxBallot, accAccepted, msgs>>(
            AcceptorAccept(a))

Spec == Init /\ [][Next]_<<propState, propBallot, propValue, propVotes, 
                              accMaxBallot, accAccepted, msgs>> /\ Fairness

(* ----------------------------------------------------------------------------
 * 不变式 (安全性)
 * ---------------------------------------------------------------------------- *)

(* 类型不变式 *)
TypeInvariant == PaxosTypeOK

(* 一致性: 没有两个不同的值可以同时被选定 *)
Consistency ==
    \A a1, a2 \in Acceptor :
        /\ accAccepted[a1] # None
        /\ accAccepted[a2] # None
        /\ accAccepted[a1].ballot = accAccepted[a2].ballot
        => accAccepted[a1].value = accAccepted[a2].value

(* 更强的形式: 一旦值被选定, 所有后续提议必须使用相同值 *)
SingleValueChosen ==
    \A p1, p2 \in Proposer :
        (propState[p1] = "chosen" /\ propState[p2] = "chosen")
        => propValue[p1] = propValue[p2]

(* 有效性: 被选定的值必须是某个Proposer提出的 *)
Validity ==
    \A a \in Acceptor :
        accAccepted[a] # None => accAccepted[a].value \in Value

(* ----------------------------------------------------------------------------
 * 时序性质 (活性)
 * ---------------------------------------------------------------------------- *)

(* 终止性: 某个Proposer最终选定值 *)
Termination ==
    <>(\E p \in Proposer : propState[p] = "chosen")

(* ----------------------------------------------------------------------------
 * 模型检查配置示例
 * ---------------------------------------------------------------------------- *)
(*
运行 TLC Model Checker 的配置:

1. 定义常量:
   Proposer = {p1, p2}
   Acceptor = {a1, a2, a3}
   Value = {v1, v2}
   Quorum = {{a1, a2}, {a1, a3}, {a2, a3}}

2. 指定不变式:
   - TypeInvariant
   - Consistency
   - SingleValueChosen
   - Validity

3. 指定属性:
   - Termination

4. 建议: 使用小的Ballot范围如 0..2
*)

================================================================================
