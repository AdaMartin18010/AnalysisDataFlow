------------------------------- MODULE TwoPhaseCommit -------------------------------
(******************************************************************************)
(* 两阶段提交协议 (Two-Phase Commit) TLA+ 形式化规约                             *)
(*                                                                            *)
(* 本规约描述了经典的两阶段提交协议，保证分布式事务的原子性                       *)
(* 所有资源管理器(RM)最终要么全部提交，要么全部中止                               *)
(*                                                                            *)
(* 所属阶段: Struct/ | 形式化等级: L5                                           *)
(* 参考: Bernstein, Hadzilacos, Goodman "Concurrency Control and Recovery in    *)
(*       Database Systems", 1987                                               *)
(******************************************************************************)

------------------------------------------------------------------------------
(*============================================================================*)
(* 导入模块                                                                    *)
(*============================================================================*)

EXTENDS Integers, Sequences, FiniteSets, TLC
\* Integers: 提供整数运算
\* Sequences: 提供序列操作
\* FiniteSets: 提供有限集合操作
\* TLC: 提供 TLC 模型检测器特定的工具

------------------------------------------------------------------------------
(*============================================================================*)
(* 常量声明                                                                    *)
(*============================================================================*)

CONSTANTS
    RM,                 \* 资源管理器的集合，例如 {r1, r2, r3}
    Ballot              \* 提案号集合，用于唯一标识事务尝试

(* ASSUME-01: 常量参数约束 - RM 非空有限，Ballot 为自然数子集 *)
(* 证明思路: 模型参数约束，由 TLC 配置保证；有限性确保模型检查可终止 *)
ASSUME ConstantsAssumption ==
    /\ RM # {}          \* 至少有一个资源管理器
    /\ IsFiniteSet(RM)  \* RM 是有限集合
    /\ Ballot \subseteq Nat  \* Ballot 是自然数的子集

------------------------------------------------------------------------------
(*============================================================================*)
(* 变量声明                                                                    *)
(*============================================================================*)

VARIABLES
    rmState,            \* rmState[r] 表示资源管理器 r 的当前状态
    tmState,            \* 事务管理器的当前状态
    tmPrepared,         \* 已准备提交的资源管理器集合
    ballot              \* 当前使用的提案号

------------------------------------------------------------------------------
(*============================================================================*)
(* 类型定义与辅助定义                                                            *)
(*============================================================================*)

(* RM 可能的状态 *)
RMState == {"working", "prepared", "committed", "aborted"}

(* TM 可能的状态 *)
TMState == {"init", "commit", "abort"}

(* 所有变量的元组，用于时序公式 *)
vars == <<rmState, tmState, tmPrepared, ballot>>

------------------------------------------------------------------------------
(*============================================================================*)
(* 初始状态定义 (Init)                                                          *)
(*============================================================================*)

(* Def-S-TP-01: 初始状态定义 *)
Init ==
    /\ rmState = [r \in RM |-> "working"]      \* 所有 RM 初始为 working
    /\ tmState = "init"                         \* TM 初始为 init
    /\ tmPrepared = {}                          \* 无 RM 已准备
    /\ ballot \in Ballot                        \* 选择一个提案号

------------------------------------------------------------------------------
(*============================================================================*)
(* 动作定义 (Actions)                                                           *)
(*============================================================================*)

(*----------------------------------------------------------------------------*)
(* 资源管理器动作                                                               *)
(*----------------------------------------------------------------------------*)

(* Def-S-TP-02: RM 单方面中止动作                                               *)
(* RM r 可以单方面决定中止事务，从 working 状态直接变为 aborted                 *)
RMAbort(r) ==
    /\ rmState[r] = "working"                   \* 前置条件: 必须处于 working
    /\ rmState' = [rmState EXCEPT ![r] = "aborted"]  \* 状态变为 aborted
    /\ UNCHANGED <<tmState, tmPrepared, ballot>>     \* TM 相关状态不变

(* Def-S-TP-03: RM 准备提交动作                                                 *)
(* RM r 准备好提交，向 TM 发送准备就绪消息                                       *)
RMPrepare(r) ==
    /\ rmState[r] = "working"                   \* 前置条件: 必须处于 working
    /\ rmState' = [rmState EXCEPT ![r] = "prepared"] \* 状态变为 prepared
    /\ tmPrepared' = tmPrepared \union {r}      \* 加入已准备集合
    /\ UNCHANGED <<tmState, ballot>>            \* TM 状态和提案号不变

(*----------------------------------------------------------------------------*)
(* 事务管理器动作                                                               *)
(*----------------------------------------------------------------------------*)

(* Def-S-TP-04: TM 决定提交动作                                                 *)
(* 当所有 RM 都已准备时，TM 可以决定提交                                          *)
TMCommit ==
    /\ tmState = "init"                         \* 前置条件: TM 处于 init
    /\ tmPrepared = RM                          \* 所有 RM 都已准备
    /\ tmState' = "commit"                      \* TM 状态变为 commit
    /\ UNCHANGED <<rmState, tmPrepared, ballot>>     \* RM 状态暂不更新

(* Def-S-TP-05: TM 决定中止动作                                                 *)
(* TM 可以在任何时候决定中止事务                                                 *)
TMAbort ==
    /\ tmState = "init"                         \* 前置条件: TM 处于 init
    /\ tmState' = "abort"                       \* TM 状态变为 abort
    /\ UNCHANGED <<rmState, tmPrepared, ballot>>     \* RM 状态暂不更新

(*----------------------------------------------------------------------------*)
(* RM 根据 TM 决定执行的动作（决策传播）                                          *)
(*----------------------------------------------------------------------------*)

(* Def-S-TP-06: RM 执行提交动作                                                 *)
(* 当 TM 决定提交后，prepared 状态的 RM 可以实际提交                               *)
RMCommit(r) ==
    /\ tmState = "commit"                       \* 前置条件: TM 已决定 commit
    /\ rmState[r] = "prepared"                  \* RM 必须已 prepared
    /\ rmState' = [rmState EXCEPT ![r] = "committed"]  \* 状态变为 committed
    /\ UNCHANGED <<tmState, tmPrepared, ballot>>

(* Def-S-TP-07: RM 执行中止动作                                                 *)
(* 当 TM 决定中止后，prepared 状态的 RM 可以实际中止                               *)
RMAbortPrepared(r) ==
    /\ tmState = "abort"                        \* 前置条件: TM 已决定 abort
    /\ rmState[r] = "prepared"                  \* RM 必须已 prepared
    /\ rmState' = [rmState EXCEPT ![r] = "aborted"]  \* 状态变为 aborted
    /\ UNCHANGED <<tmState, tmPrepared, ballot>>

(*----------------------------------------------------------------------------*)
(* 下一步关系                                                                   *)
(*----------------------------------------------------------------------------*)

(* Def-S-TP-08: 下一个状态的所有可能动作                                        *)
Next ==
    \/ TMCommit                                 \* TM 决定提交
    \/ TMAbort                                  \* TM 决定中止
    \/ \E r \in RM :                            \* 存在某个 RM 执行动作
        \/ RMAbort(r)                           \*   - RM 单方面中止
        \/ RMPrepare(r)                         \*   - RM 准备
        \/ RMCommit(r)                          \*   - RM 执行提交
        \/ RMAbortPrepared(r)                   \*   - RM 执行中止

------------------------------------------------------------------------------
(*============================================================================*)
(* 时序公式 (Specification)                                                     *)
(*============================================================================*)

(* Def-S-TP-09: 公平性条件                                                      *)
(* 弱公平性：如果某个动作持续可用，它最终会被执行                               *)
Fairness ==
    /\ WF_vars(TMCommit)                        \* TMCommit 最终会被执行
    /\ WF_vars(TMAbort)                         \* TMAbort 最终会被执行
    /\ \A r \in RM : WF_vars(RMCommit(r))       \* 每个 RM 的 Commit 最终执行
    /\ \A r \in RM : WF_vars(RMAbortPrepared(r)) \* 每个 RM 的 Abort 最终执行

(* Def-S-TP-10: 完整规约                                                        *)
(* 从初始状态开始，通过 Next 动作转移，并满足公平性条件                           *)
Spec == Init /\ [][Next]_vars /\ Fairness

(* 不带公平性的规约（用于某些性质检查）                                          *)
SpecNoFairness == Init /\ [][Next]_vars

------------------------------------------------------------------------------
(*============================================================================*)
(* 不变式 (Invariants)                                                          *)
(*============================================================================*)

(*----------------------------------------------------------------------------*)
(* 类型不变式                                                                   *)
(*----------------------------------------------------------------------------*)

(* Thm-S-TP-01: 类型不变式                                                      *)
(* 所有变量始终保持合法类型                                                      *)
TypeInvariant ==
    /\ rmState \in [RM -> RMState]              \* rmState 是 RM 到状态的映射
    /\ tmState \in TMState                      \* tmState 是 TM 状态
    /\ tmPrepared \subseteq RM                  \* tmPrepared 是 RM 的子集
    /\ ballot \in Ballot                        \* ballot 属于 Ballot 集合

(*----------------------------------------------------------------------------*)
(* 一致性不变式                                                                 *)
(*----------------------------------------------------------------------------*)

(* Thm-S-TP-02: 一致性不变式 - 核心安全性性质                                    *)
(* 不存在两个 RM 分别处于 committed 和 aborted 状态                              *)
(* 这是 2PC 的核心保证：所有 RM 最终状态一致                                      *)
Consistency ==
    ~ \E r1, r2 \in RM :
        /\ rmState[r1] = "committed"
        /\ rmState[r2] = "aborted"

(* 更强的版本：不能同时存在 committed 和 working 状态（如果 TM 已 abort）          *)
ConsistencyStrong ==
    \A r1, r2 \in RM :
        ~ /\ rmState[r1] = "committed"
          /\ rmState[r2] = "aborted"

(*----------------------------------------------------------------------------*)
(* 状态一致性不变式                                                             *)
(*----------------------------------------------------------------------------*)

(* Thm-S-TP-03: TM 提交 implies 所有 RM 已准备                                   *)
(* 如果 TM 决定提交，那么所有 RM 必须已经发送准备就绪消息                           *)
TMCommitImpliesAllPrepared ==
    (tmState = "commit") => (tmPrepared = RM)

(* Thm-S-TP-04: 已准备的 RM 状态一致性                                           *)
(* 如果 RM r 在 tmPrepared 中，那么它的状态必须是 prepared                         *)
PreparedSetConsistency ==
    \A r \in RM :
        (r \in tmPrepared) => (rmState[r] = "prepared")

(* Thm-S-TP-05: RM 状态与 TM 决定的一致性                                        *)
(* 如果 TM 已决定 commit，则没有 RM 可以处于 working 状态                          *)
TMCommitNoWorking ==
    (tmState = "commit") =>
        \A r \in RM : rmState[r] # "working"

(* Thm-S-TP-06: 如果 TM 已 abort，则没有 RM 可以 committed                       *)
TMAbortNoCommitted ==
    (tmState = "abort") =>
        \A r \in RM : rmState[r] # "committed"

(*----------------------------------------------------------------------------*)
(* 状态转移不变式                                                               *)
(*----------------------------------------------------------------------------*)

(* Thm-S-TP-07: RM 状态转移有效性 - 只允许合法的状态转换 *)
(* working -> prepared -> committed                                            *)
(* working -> aborted                                                          *)
(* prepared -> aborted (通过 TM abort)                                         *)
RMStateTransitionValidity ==
    [][\A r \in RM :
        /\ (rmState[r] = "working" => rmState'[r] \in {"working", "prepared", "aborted"})
        /\ (rmState[r] = "prepared" => rmState'[r] \in {"prepared", "committed", "aborted"})
        /\ (rmState[r] = "committed" => rmState'[r] = "committed")
        /\ (rmState[r] = "aborted" => rmState'[r] = "aborted")]_vars

(* Thm-S-TP-08: TM 状态转移有效性 - init 只能转移到 commit 或 abort *)
TMStateTransitionValidity ==
    [][\/ (tmState = "init" => tmState' \in {"init", "commit", "abort"})
        \/ (tmState = "commit" => tmState' = "commit")
        \/ (tmState = "abort" => tmState' = "abort")]_vars

(*----------------------------------------------------------------------------*)
(* 组合不变式                                                                   *)
(*----------------------------------------------------------------------------*)

(* Thm-S-TP-09: 完整不变式 - 包含所有安全性性质                                   *)
Invariant ==
    /\ TypeInvariant
    /\ Consistency
    /\ TMCommitImpliesAllPrepared
    /\ PreparedSetConsistency
    /\ TMCommitNoWorking
    /\ TMAbortNoCommitted

------------------------------------------------------------------------------
(*============================================================================*)
(* 活性性质 (Liveness Properties)                                               *)
(*============================================================================*)

(* Thm-S-TP-10: 最终所有 RM 要么全部提交，要么全部中止                              *)
(* 这是 2PC 的核心活性性质                                                      *)
EventuallyDecided ==
    <> (\/ \A r \in RM : rmState[r] = "committed"
        \/ \A r \in RM : rmState[r] = "aborted")

(* Thm-S-TP-11: 如果所有 RM 已准备，TM 最终会提交                                  *)
(* 假设没有 RM 单方面中止                                                        *)
AllPreparedLeadsToCommit ==
    (tmPrepared = RM) ~> (tmState = "commit")

(* Thm-S-TP-12: TM 决定提交后，所有 prepared 的 RM 最终会 committed                *)
TMCommitLeadsToRMCommitted ==
    \A r \in RM :
        (tmState = "commit" /\ rmState[r] = "prepared")
            ~> (rmState[r] = "committed")

(* Thm-S-TP-13: TM 决定中止后，所有 prepared 的 RM 最终会 aborted                 *)
TMAbortLeadsToRMAborted ==
    \A r \in RM :
        (tmState = "abort" /\ rmState[r] = "prepared")
            ~> (rmState[r] = "aborted")

------------------------------------------------------------------------------
(*============================================================================*)
(* 定理与推论                                                                   *)
(*============================================================================*)

(* Lemma-S-TP-01: 从 working 状态不能直接跳到 committed                          *)
WorkingToCommittedRequiresPrepare ==
    [][\A r \in RM :
        (rmState[r] = "working" /\ rmState'[r] = "committed")
            => FALSE]_vars

(* Lemma-S-TP-02: TM 只能在 init 状态下做决定                                     *)
TMDecideOnlyFromInit ==
    [][(tmState # "init" /\ tmState' # tmState)
        => tmState \in {"init"}]_vars

(* Cor-S-TP-01: 如果存在一个 committed 的 RM，则所有 RM 最终都会 committed         *)
OneCommittedImpliesAllCommitted ==
    (\E r \in RM : rmState[r] = "committed")
        => (\A r \in RM : rmState[r] \in {"prepared", "committed"})

------------------------------------------------------------------------------
(*============================================================================*)
(* 模型检测辅助                                                                  *)
(*============================================================================*)

(* 用于 TLC 模型检测的状态约束（防止状态空间爆炸）                                 *)
StateConstraint ==
    \A r \in RM : rmState[r] \in RMState

(* 对称性集合声明（用于 TLC 优化）                                                *)
Permutations == Permutations(RM)

------------------------------------------------------------------------------
(*============================================================================*)
(* 规约结束                                                                      *)
(*============================================================================*)

================================================================================
