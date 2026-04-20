(* ============================================================================
 * TLA+ 规约: 两阶段提交协议 (Two-Phase Commit)
 * ============================================================================
 *
 * 本规约描述分布式事务的两阶段提交协议 (2PC)。
 * 
 * 核心概念:
 * - Coordinator (协调者): 管理事务提交流程
 * - Participants (参与者): 执行事务操作的服务
 * - Phases: 投票阶段(Vote) + 提交阶段(Commit/Abort)
 *
 * 协议流程:
 * Phase 1 (投票):
 *   1. Coordinator 发送 VOTE-REQ 给所有 Participants
 *   2. 每个 Participant 投票 YES/NO
 *   3. Participant 写本地日志后回复
 *
 * Phase 2 (决定):
 *   4. Coordinator 收集所有投票
 *   5. 如果全部 YES, 决定 COMMIT; 否则 ABORT
 *   6. Coordinator 发送决定给所有 Participants
 *   7. Participants 执行决定并确认
 *
 * 安全性质:
 * - Agreement: 所有正确进程对事务结果达成一致
 * - Validity: 只有当所有参与者投票YES时才提交
 * - Termination: 非故障参与者最终做出决定
 *
 * 参考: Gray, J. (1978). Notes on Data Base Operating Systems
 * ============================================================================ *)

------------------------------ MODULE TwoPhaseCommit ------------------------------

(* ----------------------------------------------------------------------------
 * 常量定义
 * ---------------------------------------------------------------------------- *)

CONSTANTS
    Participant,           (* 参与者集合, e.g., {p1, p2, p3} *)
    Coordinator,           (* 协调者, e.g., c1 *)
    
    (* 消息类型 *)
    VoteRequest,           (* 投票请求 *)
    VoteYes,               (* 赞成票 *)
    VoteNo,                (* 反对票 *)
    Commit,                (* 提交命令 *)
    Abort,                 (* 中止命令 *)
    Ack                    (* 确认 *)

(* ASSUME-01: 角色分离假设 - Coordinator 不能是 Participant *)
(* 证明思路: 角色分离确保协调者独立决策，避免投票和决策的角色冲突 *)
(* ASSUME-02: 非空假设 - 至少有一个参与者 *)
(* 证明思路: 空参与者集合使协议无意义；这是模型配置约束 *)
ASSUME ConstantsAssumption ==
    /\ Coordinator \notin Participant     (* 协调者不是参与者 *)
    /\ Participant \neq {}                (* 至少有一个参与者 *)

(* ----------------------------------------------------------------------------
 * 变量定义
 * ---------------------------------------------------------------------------- *)

VARIABLES
    (* 协调者状态 *)
    coordinatorState,      (* "init", "waiting", "committed", "aborted" *)
    votes,                 (* 收到的投票集合 *)
    
    (* 参与者状态 *)
    participantState,      (* Participant -> "init", "ready", "committed", "aborted" *)
    participantVote,       (* Participant -> "yes", "no", "none" *)
    
    (* 通信 *)
    msgs                   (* 消息集合 *)

(* ----------------------------------------------------------------------------
 * 类型不变式
 * ---------------------------------------------------------------------------- *)

TwoPCTypeOK ==
    /\ coordinatorState \in {"init", "waiting", "committed", "aborted"}
    /\ votes \subseteq Participant
    /\ participantState \in [Participant -> {"init", "ready", "committed", "aborted"}]
    /\ participantVote \in [Participant -> {"yes", "no", "none"}]
    /\ msgs \subseteq 
        [type: {VoteRequest}, coord: {Coordinator}, part: Participant]
        \cup [type: {VoteYes, VoteNo}, part: Participant, coord: {Coordinator}]
        \cup [type: {Commit, Abort}, coord: {Coordinator}, part: Participant]
        \cup [type: {Ack}, part: Participant, coord: {Coordinator}]

(* ----------------------------------------------------------------------------
 * 辅助定义
 * ---------------------------------------------------------------------------- *)

(* 所有参与者都已投票 *)
AllVotesCollected == votes = Participant

(* 是否存在NO投票 *)
HasNoVote == 
    \E p \in Participant : participantVote[p] = "no"

(* ----------------------------------------------------------------------------
 * 初始状态
 * ---------------------------------------------------------------------------- *)

Init ==
    /\ coordinatorState = "init"
    /\ votes = {}
    /\ participantState = [p \in Participant |-> "init"]
    /\ participantVote = [p \in Participant |-> "none"]
    /\ msgs = {}

(* ----------------------------------------------------------------------------
 * 协调者动作
 * ---------------------------------------------------------------------------- *)

(* 协调者发起投票请求 - Phase 1 开始 *)
CoordinatorStart ==
    /\ coordinatorState = "init"
    /\ coordinatorState' = "waiting"
    /\ msgs' = msgs \cup 
        {[type |-> VoteRequest, coord |-> Coordinator, part |-> p] : p \in Participant}
    /\ UNCHANGED <<votes, participantState, participantVote>>

(* 协调者收集投票 *)
CoordinatorCollectVote(p) ==
    /\ coordinatorState = "waiting"
    /\ p \in Participant
    /\ p \notin votes
    /\ \E voteMsg \in msgs :
        /\ voteMsg.type \in {VoteYes, VoteNo}
        /\ voteMsg.part = p
        /\ voteMsg.coord = Coordinator
    /\ votes' = votes \cup {p}
    /\ UNCHANGED <<coordinatorState, participantState, participantVote, msgs>>

(* 协调者决定提交 - Phase 2 开始 *)
CoordinatorDecideCommit ==
    /\ coordinatorState = "waiting"
    /\ AllVotesCollected
    /\ ~HasNoVote           (* 全部投YES *)
    /\ coordinatorState' = "committed"
    /\ msgs' = msgs \cup 
        {[type |-> Commit, coord |-> Coordinator, part |-> p] : p \in Participant}
    /\ UNCHANGED <<votes, participantState, participantVote>>

(* 协调者决定中止 *)
CoordinatorDecideAbort ==
    /\ coordinatorState = "waiting"
    /\ AllVotesCollected
    /\ HasNoVote            (* 有NO投票 *)
    /\ coordinatorState' = "aborted"
    /\ msgs' = msgs \cup 
        {[type |-> Abort, coord |-> Coordinator, part |-> p] : p \in Participant}
    /\ UNCHANGED <<votes, participantState, participantVote>>

(* ----------------------------------------------------------------------------
 * 参与者动作
 * ---------------------------------------------------------------------------- *)

(* 参与者接收投票请求并投票YES *)
ParticipantVoteYes(p) ==
    /\ participantState[p] = "init"
    /\ \E req \in msgs :
        /\ req.type = VoteRequest
        /\ req.part = p
        /\ req.coord = Coordinator
    /\ participantState' = [participantState EXCEPT ![p] = "ready"]
    /\ participantVote' = [participantVote EXCEPT ![p] = "yes"]
    /\ msgs' = msgs \cup {[type |-> VoteYes, part |-> p, coord |-> Coordinator]}
    /\ UNCHANGED <<coordinatorState, votes>>

(* 参与者接收投票请求并投票NO *)
ParticipantVoteNo(p) ==
    /\ participantState[p] = "init"
    /\ \E req \in msgs :
        /\ req.type = VoteRequest
        /\ req.part = p
        /\ req.coord = Coordinator
    /\ participantState' = [participantState EXCEPT ![p] = "ready"]
    /\ participantVote' = [participantVote EXCEPT ![p] = "no"]
    /\ msgs' = msgs \cup {[type |-> VoteNo, part |-> p, coord |-> Coordinator]}
    /\ UNCHANGED <<coordinatorState, votes>>

(* 参与者执行提交 *)
ParticipantCommit(p) ==
    /\ participantState[p] = "ready"
    /\ \E decision \in msgs :
        /\ decision.type = Commit
        /\ decision.part = p
        /\ decision.coord = Coordinator
    /\ participantState' = [participantState EXCEPT ![p] = "committed"]
    /\ msgs' = msgs \cup {[type |-> Ack, part |-> p, coord |-> Coordinator]}
    /\ UNCHANGED <<coordinatorState, votes, participantVote>>

(* 参与者执行中止 *)
ParticipantAbort(p) ==
    /\ participantState[p] = "ready"
    /\ \E decision \in msgs :
        /\ decision.type = Abort
        /\ decision.part = p
        /\ decision.coord = Coordinator
    /\ participantState' = [participantState EXCEPT ![p] = "aborted"]
    /\ msgs' = msgs \cup {[type |-> Ack, part |-> p, coord |-> Coordinator]}
    /\ UNCHANGED <<coordinatorState, votes, participantVote>>

(* ----------------------------------------------------------------------------
 * 下一步动作 (状态转移)
 * ---------------------------------------------------------------------------- *)

Next ==
    \/ CoordinatorStart
    \/ \E p \in Participant : CoordinatorCollectVote(p)
    \/ CoordinatorDecideCommit
    \/ CoordinatorDecideAbort
    \/ \E p \in Participant : ParticipantVoteYes(p)
    \/ \E p \in Participant : ParticipantVoteNo(p)
    \/ \E p \in Participant : ParticipantCommit(p)
    \/ \E p \in Participant : ParticipantAbort(p)

(* ----------------------------------------------------------------------------
 * 公平性约束 (确保进展)
 * ---------------------------------------------------------------------------- *)

Fairness ==
    /\ WF_<<coordinatorState, votes, participantState, participantVote, msgs>>(CoordinatorStart)
    /\ \A p \in Participant :
        WF_<<coordinatorState, votes, participantState, participantVote, msgs>>(CoordinatorCollectVote(p))
    /\ WF_<<coordinatorState, votes, participantState, participantVote, msgs>>(CoordinatorDecideCommit)
    /\ WF_<<coordinatorState, votes, participantState, participantVote, msgs>>(CoordinatorDecideAbort)
    /\ \A p \in Participant :
        WF_<<coordinatorState, votes, participantState, participantVote, msgs>>(ParticipantVoteYes(p))
    /\ \A p \in Participant :
        WF_<<coordinatorState, votes, participantState, participantVote, msgs>>(ParticipantCommit(p))

Spec == Init /\ [][Next]_<<coordinatorState, votes, participantState, participantVote, msgs>> /\ Fairness

(* ----------------------------------------------------------------------------
 * 不变式 (安全性性质)
 * ---------------------------------------------------------------------------- *)

(* 类型不变式 *)
TypeInvariant == TwoPCTypeOK

(* 协议一致性: 不可能同时有参与者提交和中止 *)
Consistency ==
    ~(\E p1, p2 \in Participant :
        /\ participantState[p1] = "committed"
        /\ participantState[p2] = "aborted")

(* 协调者决定与参与者状态的一致性 *)
CoordinatorConsistency ==
    (coordinatorState = "committed" => 
        \A p \in Participant : participantState[p] \in {"ready", "committed"})
    /\ (coordinatorState = "aborted" =>
        \A p \in Participant : participantState[p] \in {"ready", "aborted"})

(* 有效性: 只有当没有NO投票时才能提交 *)
Validity ==
    coordinatorState = "committed" => 
        \A p \in Participant : participantVote[p] = "yes"

(* ----------------------------------------------------------------------------
 * 时序性质 (活性性质)
 * ---------------------------------------------------------------------------- *)

(* 终止性: 如果协调者决定提交, 所有非故障参与者最终提交 *)
Termination ==
    coordinatorState = "committed" ~> 
        (\A p \in Participant : participantState[p] = "committed")

(* 所有参与者最终达到终止状态 *)
AllParticipantsDecide ==
    <>(\A p \in Participant : participantState[p] \in {"committed", "aborted"})

(* ----------------------------------------------------------------------------
 * 模型检查配置示例
 * ---------------------------------------------------------------------------- *)
(*
运行 TLC Model Checker 的配置:

1. 创建新模型
2. 定义常量:
   Participant = {p1, p2}
   Coordinator = c1
   VoteRequest = VoteRequest
   VoteYes = VoteYes
   VoteNo = VoteNo
   Commit = Commit
   Abort = Abort
   Ack = Ack

3. 指定不变式检查:
   - TypeInvariant
   - Consistency
   - CoordinatorConsistency
   - Validity

4. 指定属性检查:
   - Termination
   - AllParticipantsDecide

5. 启动模型检查
*)

================================================================================
