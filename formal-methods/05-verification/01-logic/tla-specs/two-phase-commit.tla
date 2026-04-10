(*
 * Two-Phase Commit Protocol - TLA+ Specification
 * ==============================================
 *
 * 本规约描述经典的两阶段提交（2PC）协议，用于实现分布式事务的原子性。
 *
 * 协议角色：
 * - Coordinator（协调者）：管理事务提交或中止
 * - Participants（参与者）：执行事务操作，投票决定提交/中止
 *
 * 协议阶段：
 * Phase 1 (Voting): Coordinator 询问所有参与者是否可以提交
 * Phase 2 (Decision): 根据投票结果决定提交或中止
 *
 * 安全性保证：
 * - 原子性：所有参与者最终要么都提交，要么都中止
 * - 一致性：不存在部分提交的情况
 *
 * 已知问题：
 * - 阻塞问题：如果 Coordinator 在第二阶段崩溃，参与者可能阻塞等待
 *
 * 作者: AnalysisDataFlow Project
 * 版本: 1.0
 *)

------------------------------- MODULE two-phase-commit -------------------------------

EXTENDS Naturals, FiniteSets, Sequences, TLC

(*
 * =====================================================================
 * 常量声明
 * =====================================================================
 *)
CONSTANTS
    Participant,        \* 参与者集合
    Value,              \* 事务值的集合
    Coordinator         \* 协调者（单一节点）

ASSUME CoordinatorAssumption == 
    Coordinator \notin Participant

(*
 * =====================================================================
 * 变量声明
 * =====================================================================
 *)
VARIABLES
    (* Coordinator 状态 *)
    c_state,            \* Coordinator 的状态
    c_votes,            \* 收集到的投票
    c_decision,         \* 最终决策
    
    (* Participant 状态 *)
    p_state,            \* 每个参与者的状态
    p_vote,             \* 每个参与者的投票
    p_decision,         \* 每个参与者收到的决策
    
    (* 事务数据 *)
    tx_value,           \* 当前事务值
    
    (* 消息 *)
    msgs,               \* 网络消息
    
    (* 故障模拟 *)
    c_alive,            \* Coordinator 是否存活
    p_alive             \* 每个参与者是否存活

(*
 * =====================================================================
 * 辅助定义
 * =====================================================================
 *)
Node == Participant \cup {Coordinator}

(* 消息类型 *)
Message ==
    [type : {"prepare"}, from : {Coordinator}, to : Participant]
    \cup
    [type : {"vote"}, from : Participant, to : {Coordinator}, 
     vote : {"yes", "no"}]
    \cup
    [type : {"commit"}, from : {Coordinator}, to : Participant]
    \cup
    [type : {"abort"}, from : {Coordinator}, to : Participant]
    \cup
    [type : {"ack"}, from : Participant, to : {Coordinator}]

(* Coordinator 状态 *)
CoordinatorState == {
    "init",         \* 初始状态
    "waiting",      \* 等待投票
    "committed",    \* 已决定提交
    "aborted"       \* 已决定中止
}

(* Participant 状态 *)
ParticipantState == {
    "working",      \* 执行事务
    "prepared",     \* 已准备（投票 yes 后）
    "committed",    \* 已提交
    "aborted"      \* 已中止
}

(*
 * =====================================================================
 * 类型不变式
 * =====================================================================
 *)
TypeOK ==
    /\ c_state \in CoordinatorState
    /\ c_votes \in [Participant -> {"yes", "no", "none"}]
    /\ c_decision \in {"none", "commit", "abort"}
    /\ p_state \in [Participant -> ParticipantState]
    /\ p_vote \in [Participant -> {"yes", "no", "none"}]
    /\ p_decision \in [Participant -> {"none", "commit", "abort"}]
    /\ tx_value \in Value \cup {None}
    /\ msgs \subseteq Message
    /\ c_alive \in BOOLEAN
    /\ p_alive \in [Participant -> BOOLEAN]

None == CHOOSE v : v \notin Value

(*
 * =====================================================================
 * 初始状态
 * =====================================================================
 *)
Init ==
    /\ c_state = "init"
    /\ c_votes = [p \in Participant |-> "none"]
    /\ c_decision = "none"
    /\ p_state = [p \in Participant |-> "working"]
    /\ p_vote = [p \in Participant |-> "none"]
    /\ p_decision = [p \in Participant |-> "none"]
    /\ tx_value \in Value
    /\ msgs = {}
    /\ c_alive = TRUE
    /\ p_alive = [p \in Participant |-> TRUE]

(*
 * =====================================================================
 * 辅助操作
 * =====================================================================
 *)
Send(m) == msgs' = msgs \cup {m}

Broadcast(from, type_msg) ==
    msgs' = msgs \cup {[type |-> type_msg, from |-> from, to |-> p] : p \in Participant}

AllVoted ==
    \A p \in Participant : c_votes[p] # "none"

AllYesVotes ==
    \A p \in Participant : c_votes[p] = "yes"

(*
 * =====================================================================
 * Phase 1: 投票阶段
 * =====================================================================
 *)

(* 步骤 1: Coordinator 发送 prepare 请求 *)
CoordinatorSendPrepare ==
    /\ c_alive
    /\ c_state = "init"
    /\ c_state' = "waiting"
    /\ Broadcast(Coordinator, "prepare")
    /\ UNCHANGED <<c_votes, c_decision, p_state, p_vote, p_decision, 
                   tx_value, c_alive, p_alive>>

(* 步骤 2: Participant 接收 prepare 并投票 *)
ParticipantReceivePrepare(p) ==
    /\ p_alive[p]
    /\ p_state[p] = "working"
    /\ \E m \in msgs :
        /\ m.type = "prepare"
        /\ m.to = p
        /\ \E v \in {"yes", "no"} :
            (* 简化：参与者随机投票 yes 或 no *)
            /\ p_vote' = [p_vote EXCEPT ![p] = v]
            /\ IF v = "yes"
               THEN p_state' = [p_state EXCEPT ![p] = "prepared"]
               ELSE p_state' = [p_state EXCEPT ![p] = "aborted"]
            /\ Send([type |-> "vote", from |-> p, to |-> Coordinator, vote |-> v])
    /\ UNCHANGED <<c_state, c_votes, c_decision, p_decision, 
                   tx_value, c_alive, p_alive>>

(* 步骤 3: Coordinator 收集投票 *)
CoordinatorCollectVote ==
    /\ c_alive
    /\ c_state = "waiting"
    /\ \E m \in msgs :
        /\ m.type = "vote"
        /\ m.to = Coordinator
        /\ c_votes[m.from] = "none"
        /\ c_votes' = [c_votes EXCEPT ![m.from] = m.vote]
    /\ UNCHANGED <<c_state, c_decision, p_state, p_vote, p_decision,
                   tx_value, msgs, c_alive, p_alive>>

(*
 * =====================================================================
 * Phase 2: 决策阶段
 * =====================================================================
 *)

(* 步骤 4: Coordinator 做出决策并广播 *)
CoordinatorDecide ==
    /\ c_alive
    /\ c_state = "waiting"
    /\ AllVoted
    /\ IF AllYesVotes
       THEN 
           /\ c_state' = "committed"
           /\ c_decision' = "commit"
           /\ Broadcast(Coordinator, "commit")
       ELSE 
           /\ c_state' = "aborted"
           /\ c_decision' = "abort"
           /\ Broadcast(Coordinator, "abort")
    /\ UNCHANGED <<c_votes, p_state, p_vote, p_decision, 
                   tx_value, c_alive, p_alive>>

(* 步骤 5: Participant 接收决策 *)
ParticipantReceiveDecision(p) ==
    /\ p_alive[p]
    /\ p_decision[p] = "none"
    /\ \E m \in msgs :
        /\ (m.type = "commit" \/ m.type = "abort")
        /\ m.to = p
        /\ IF m.type = "commit"
           THEN 
               /\ p_state' = [p_state EXCEPT ![p] = "committed"]
               /\ p_decision' = [p_decision EXCEPT ![p] = "commit"]
           ELSE 
               /\ p_state' = [p_state EXCEPT ![p] = "aborted"]
               /\ p_decision' = [p_decision EXCEPT ![p] = "abort"]
        /\ Send([type |-> "ack", from |-> p, to |-> Coordinator])
    /\ UNCHANGED <<c_state, c_votes, c_decision, p_vote,
                   tx_value, c_alive, p_alive>>

(* 步骤 6: Coordinator 收集确认 *)
CoordinatorCollectAck ==
    /\ c_alive
    /\ (c_state = "committed" \/ c_state = "aborted")
    /\ \E m \in msgs :
        /\ m.type = "ack"
        /\ m.to = Coordinator
    /\ UNCHANGED <<c_state, c_votes, c_decision, p_state, p_vote, p_decision,
                   tx_value, msgs, c_alive, p_alive>>

(*
 * =====================================================================
 * 故障处理（用于分析阻塞问题）
 * =====================================================================
 *)

(* Coordinator 崩溃 *)
CoordinatorCrash ==
    /\ c_alive
    /\ c_alive' = FALSE
    /\ UNCHANGED <<c_state, c_votes, c_decision, p_state, p_vote, p_decision,
                   tx_value, msgs, p_alive>>

(* Participant 崩溃 *)
ParticipantCrash(p) ==
    /\ p_alive[p]
    /\ p_alive' = [p_alive EXCEPT ![p] = FALSE]
    /\ UNCHANGED <<c_state, c_votes, c_decision, p_state, p_vote, p_decision,
                   tx_value, msgs, c_alive>>

(* Coordinator 恢复 - 简化：从持久化存储恢复状态 *)
CoordinatorRecover ==
    /\ ~c_alive
    /\ c_alive' = TRUE
    /\ UNCHANGED <<c_state, c_votes, c_decision, p_state, p_vote, p_decision,
                   tx_value, msgs, p_alive>>

(*
 * =====================================================================
 * 下一步动作
 * =====================================================================
 *)
Next ==
    CoordinatorSendPrepare
    \/ CoordinatorCollectVote
    \/ CoordinatorDecide
    \/ CoordinatorCollectAck
    \/ \E p \in Participant : 
        ParticipantReceivePrepare(p) 
        \/ ParticipantReceiveDecision(p)
    (* 可选：启用故障模拟用于分析阻塞问题 *)
    (* \/ CoordinatorCrash *)
    (* \/ \E p \in Participant : ParticipantCrash(p) *)
    (* \/ CoordinatorRecover *)

(*
 * =====================================================================
 * 完整规约
 * =====================================================================
 *)
Spec == Init /\ [][Next]_<<c_state, c_votes, c_decision, p_state, p_vote, 
                          p_decision, tx_value, msgs, c_alive, p_alive>>

(*
 * =====================================================================
 * 安全性不变式 (Safety Properties)
 * =====================================================================
 *)

(*
 * Thm-2PC-01: Atomicity
 * 不可能出现部分参与者提交、部分中止的情况
 *)
Atomicity ==
    ~\E p1, p2 \in Participant :
        p_state[p1] = "committed" /\ p_state[p2] = "aborted"

(*
 * Thm-2PC-02: Consistent Decision
 * 所有最终决策必须一致
 *)
ConsistentDecision ==
    \A p \in Participant :
        (p_decision[p] = "commit" 
         => \A p2 \in Participant : p_decision[p2] # "abort")
    /\
    \A p \in Participant :
        (p_decision[p] = "abort"
         => \A p2 \in Participant : p_decision[p2] # "commit")

(*
 * Thm-2PC-03: Commit Validity
 * 只有所有参与者都投票 yes 时才能提交
 *)
CommitValidity ==
    (c_decision = "commit")
    => \A p \in Participant : c_votes[p] = "yes"

(*
 * Thm-2PC-04: State Transition Validity
 * 参与者状态必须按正确顺序转换
 *)
StateTransitionValidity ==
    [][\A p \in Participant :
        (* working -> prepared -> committed *)
        (* working -> aborted *)
        (* prepared -> committed *)
        (* prepared -> aborted *)
        (p_state[p] = "working" => 
            p_state'[p] \in {"working", "prepared", "aborted"})
        /\ (p_state[p] = "prepared" =>
            p_state'[p] \in {"prepared", "committed", "aborted"})
        /\ (p_state[p] = "committed" => p_state'[p] = "committed")
        /\ (p_state[p] = "aborted" => p_state'[p] = "aborted")
    ]_<<p_state>>

(*
 * =====================================================================
 * 阻塞问题分析 (Blocking Analysis)
 * =====================================================================
 *)

(*
 * Thm-2PC-05: Blocking Scenario
 * 当 Coordinator 在第二阶段崩溃时，处于 prepared 状态的参与者会阻塞
 *
 * 引理：存在一种执行，其中某个参与者永远处于 prepared 状态
 * 除非 Coordinator 恢复或人工干预
 *)
BlockingScenario ==
    \E p \in Participant :
        <>[](p_state[p] = "prepared" /\ ~c_alive)

(*
 * Thm-2PC-06: Non-Blocking Condition
 * 如果 Coordinator 存活且网络可靠，协议不会阻塞
 *)
NonBlockingCondition ==
    (c_alive /\ \A p \in Participant : p_alive[p])
    => <>(\A p \in Participant : p_state[p] \in {"committed", "aborted"})

(*
 * =====================================================================
 * 三阶段提交对比 (3PC Comparison)
 * =====================================================================
 *
 * 3PC 解决了 2PC 的阻塞问题，通过引入额外的 "pre-commit" 阶段：
 *
 * Phase 1: CanCommit? (Coordinator -> Participants)
 * Phase 2: PreCommit (Coordinator -> Participants)  
 * Phase 3: DoCommit (Coordinator -> Participants)
 *
 * 关键区别：
 * - 在 PreCommit 阶段后，参与者知道其他参与者也都准备好了
 * - 即使 Coordinator 崩溃，参与者可以通过询问其他参与者决定提交/中止
 *
 * 代价：
 * - 多一次网络往返
 * * 更复杂的实现
 *)

(*
 * =====================================================================
 * TLC 配置
 * =====================================================================
 *
 * CONSTANTS:
 *   Participant = {p1, p2, p3}
 *   Value = {v1}
 *   Coordinator = c
 *
 * 不变式:
 *   TypeOK
 *   Atomicity
 *   ConsistentDecision
 *   CommitValidity
 *)

=============================================================================
