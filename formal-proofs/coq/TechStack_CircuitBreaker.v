(* ============================================================================ *)
(* TECH-STACK - Circuit Breaker Effectiveness in Preventing Cascading Failures *)
(* ============================================================================ *)
(* 形式化等级: L6 (机械化验证)                                                  *)
(* 源文档: TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/                       *)
(*         04-resilience/04.02-circuit-breaker-backpressure-analysis.md         *)
(* 定理注册 ID: Thm-TS-04-02-01                                                 *)
(* 作者: AnalysisDataFlow Formalization Agent                                   *)
(* 日期: 2026-04-22                                                             *)
(* ============================================================================ *)
(* 编译要求: Coq >= 8.17                                                        *)
(* 依赖: Coq标准库 (Lists, Arith, Classical)                                    *)
(* ============================================================================ *)

Require Import Coq.Lists.List.
Require Import Coq.Arith.PeanoNat.
Require Import Coq.Logic.Classical_Prop.

Import ListNotations.

(* ---------------------------------------------------------------------------- *)
(* Section 1: 基础定义                                                          *)
(* ---------------------------------------------------------------------------- *)

Section CircuitBreaker_Definitions.

(* ---------------------------------------------------------------------------- *)
(* 1.1 组件定义 (Component)                                                     *)
(* ---------------------------------------------------------------------------- *)

(* 组件: 以自然数标识的分布式系统组件 *)
Record Component : Type := mkComponent {
  comp_id : nat
}.

(* 组件相等性判定: 基于 comp_id 的判定过程 *)
Definition comp_eqb (c1 c2 : Component) : bool :=
  Nat.eqb (comp_id c1) (comp_id c2).

Lemma comp_eqb_eq : forall c1 c2, comp_eqb c1 c2 = true <-> c1 = c2.
Proof.
  intros c1 c2. unfold comp_eqb.
  destruct c1 as [id1], c2 as [id2]. simpl.
  split; intro H.
  - apply Nat.eqb_eq in H. subst. reflexivity.
  - inversion H. apply Nat.eqb_eq. reflexivity.
Qed.

Lemma comp_eqb_neq : forall c1 c2, comp_eqb c1 c2 = false <-> c1 <> c2.
Proof.
  intros c1 c2. unfold comp_eqb.
  destruct c1 as [id1], c2 as [id2]. simpl.
  split; intro H.
  - intro Heq. inversion Heq. apply Nat.eqb_neq in H. contradiction.
  - apply Nat.eqb_neq. intro Heq. apply H. subst. reflexivity.
Qed.

Lemma comp_eq_dec : forall c1 c2 : Component, {c1 = c2} + {c1 <> c2}.
Proof.
  intros c1 c2.
  destruct (comp_eqb c1 c2) eqn:Heq.
  - left. apply comp_eqb_eq. assumption.
  - right. apply comp_eqb_neq. assumption.
Defined.

(* 边: 组件之间的有向依赖关系 *)
Definition Edge := (Component * Component)%type.

(* 依赖图: 边的有限列表 *)
Definition DependencyGraph := list Edge.

(* 图中是否包含某条边 *)
Definition has_edge (G : DependencyGraph) (e : Edge) : Prop :=
  In e G.

(* ---------------------------------------------------------------------------- *)
(* 1.2 有向无环图 (DAG) 谓词                                                   *)
(* ---------------------------------------------------------------------------- *)

(* 标准图可达性关系 (不考虑断路器) *)
Inductive reachable (G : DependencyGraph) : Component -> Component -> Prop :=
  | Reach_Refl : forall v, reachable G v v
  | Reach_Step : forall u v w,
      In (u, v) G ->
      reachable G v w ->
      reachable G u w.

(* DAG: 不存在从自身到自身的非平凡路径 (无环) *)
Definition DAG (G : DependencyGraph) : Prop :=
  forall v, ~ reachable G v v.

(* ---------------------------------------------------------------------------- *)
(* 1.3 断路器配置 (CircuitBreakerConfig)                                        *)
(* ---------------------------------------------------------------------------- *)

(* 断路器配置: 配置了断路器的边的集合 (以边列表表示) *)
Definition CircuitBreakerConfig := list Edge.

(* 某条边是否配置了断路器 *)
Definition has_cb (cb : CircuitBreakerConfig) (e : Edge) : Prop :=
  In e cb.

(* 所有边均配置断路器 *)
Definition all_edges_have_cb (G : DependencyGraph) (cb : CircuitBreakerConfig) : Prop :=
  forall u v, In (u, v) G -> has_cb cb (u, v).

(* ---------------------------------------------------------------------------- *)
(* 1.4 故障传播作用域 (Fault Propagation Scope)                                 *)
(* ---------------------------------------------------------------------------- *)

(* 故障单步传播: 从 u 到 v 的故障传播当且仅当存在依赖边 (u,v) 且该边无断路器 *)
Definition fault_step (G : DependencyGraph) (cb : CircuitBreakerConfig)
  (u v : Component) : Prop :=
  In (u, v) G /\ ~ has_cb cb (u, v).

(* 故障传播作用域: 从故障源 v0 出发，沿无断路器边可达的所有组件 *)
(* 即 fault_step 的自反传递闭包 *)
Inductive in_fault_scope (G : DependencyGraph) (cb : CircuitBreakerConfig)
  : Component -> Component -> Prop :=
  | FS_Refl : forall v0, in_fault_scope G cb v0 v0
  | FS_Step : forall v0 u v,
      in_fault_scope G cb v0 u ->
      fault_step G cb u v ->
      in_fault_scope G cb v0 v.

End CircuitBreaker_Definitions.

(* ---------------------------------------------------------------------------- *)
(* Section 2: 基本引理                                                          *)
(* ---------------------------------------------------------------------------- *)

Section CircuitBreaker_Lemmas.

(* 故障传播作用域的传递性 *)
Lemma fault_scope_trans :
  forall G cb v0 u v,
    in_fault_scope G cb v0 u ->
    in_fault_scope G cb u v ->
    in_fault_scope G cb v0 v.
Proof.
  intros G cb v0 u v H1 H2.
  induction H2 as [| u' v' Hscope IH Hstep].
  - (* v = u *)
    assumption.
  - (* v = v', Hscope: in_fault_scope G cb u u', Hstep: fault_step G cb u' v' *)
    apply IH in H1.
    apply FS_Step with u'; assumption.
Qed.

(* 故障传播作用域蕴含标准图可达性 *)
Lemma fault_scope_implies_reachable :
  forall G cb v0 v,
    in_fault_scope G cb v0 v ->
    reachable G v0 v.
Proof.
  intros G cb v0 v Hscope.
  induction Hscope as [v0 | v0 u v Hscope IH Hstep].
  - (* FS_Refl *)
    apply Reach_Refl.
  - (* FS_Step *)
    apply Reach_Step with u.
    + unfold fault_step in Hstep. destruct Hstep as [Hin _]. exact Hin.
    + exact IH.
Qed.

(* DAG 中故障传播不可能形成环 *)
Lemma dag_no_fault_cycles :
  forall G cb v,
    DAG G ->
    ~ in_fault_scope G cb v v.
Proof.
  intros G cb v Hdag Hcontra.
  apply fault_scope_implies_reachable in Hcontra.
  apply (Hdag v). exact Hcontra.
Qed.

(* 若 v ≠ v0 且在故障作用域中，则存在前驱节点 u 也在作用域中 *)
Lemma fault_scope_has_predecessor :
  forall G cb v0 v,
    in_fault_scope G cb v0 v ->
    v <> v0 ->
    exists u, in_fault_scope G cb v0 u /\ fault_step G cb u v.
Proof.
  intros G cb v0 v Hscope Hneq.
  inversion Hscope; subst.
  - (* v = v0 *)
    exfalso. apply Hneq. reflexivity.
  - (* FS_Step *)
    exists u. split; assumption.
Qed.

End CircuitBreaker_Lemmas.

(* ---------------------------------------------------------------------------- *)
(* Section 3: 核心定理 (Thm-TS-04-02-01)                                         *)
(* ---------------------------------------------------------------------------- *)

Section CircuitBreaker_Theorem.

(* ---------------------------------------------------------------------------- *)
(* Lemma-TS-04-02-03: 断路器缩减故障传播作用域                                   *)
(* ---------------------------------------------------------------------------- *)
(*
   引理陈述: 对于任意 DAG G、断路器配置 cb、故障源 v0，
   若边 (u,v) 配置了断路器，且 u 已在故障作用域中，
   并且 u 是 v 在作用域内的唯一上游前驱，
   则 v 不在故障作用域中 (除非 v = v0)。

   证明策略:
   1. 反设 v 在故障作用域中且 v ≠ v0。
   2. 由 fault_scope_has_predecessor，存在前驱 w 在作用域中使得 fault_step w v。
   3. 由唯一性假设，w = u。
   4. 故 fault_step u v，即 In (u,v) G 且 ~ has_cb cb (u,v)。
   5. 与假设 has_cb cb (u,v) 矛盾。
*)
Lemma cb_reduces_scope :
  forall G cb v0 u v,
    DAG G ->
    In (u, v) G ->
    has_cb cb (u, v) ->
    in_fault_scope G cb v0 u ->
    (forall w, In (w, v) G -> in_fault_scope G cb v0 w -> w = u) ->
    v <> v0 ->
    ~ in_fault_scope G cb v0 v.
Proof.
  intros G cb v0 u v Hdag Hedge Hcb Hu Hunique Hneq Hcontra.
  (* 反设: v 在故障作用域中且 v <> v0 *)
  apply fault_scope_has_predecessor in Hcontra as [w [Hwscope Hstep]]; auto.
  (* 由唯一性假设，w = u *)
  assert (Hw_eq : w = u). {
    unfold fault_step in Hstep. destruct Hstep as [Hwin _].
    apply Hunique; auto.
  }
  subst w.
  (* 故 fault_step u v，即 ~ has_cb cb (u, v) *)
  unfold fault_step in Hstep. destruct Hstep as [_ Hnocb].
  (* 矛盾: has_cb cb (u,v) 且 ~ has_cb cb (u,v) *)
  contradiction.
Qed.

(* ---------------------------------------------------------------------------- *)
(* 辅助引理: 若所有边均配置断路器，则不存在故障单步传播 *)
(* ---------------------------------------------------------------------------- *)
Lemma all_cb_no_fault_step :
  forall G cb u v,
    all_edges_have_cb G cb ->
    ~ fault_step G cb u v.
Proof.
  intros G cb u v Hall Hstep.
  unfold fault_step in Hstep. destruct Hstep as [Hin Hnocb].
  unfold all_edges_have_cb in Hall.
  unfold has_cb in *.
  apply Hnocb. apply Hall. exact Hin.
Qed.

(* ---------------------------------------------------------------------------- *)
(* Thm-TS-04-02-01: 全边断路器配置下单跳隔离定理                               *)
(* ---------------------------------------------------------------------------- *)
(*
   定理陈述: 若依赖图 G 为 DAG，且所有边均配置了断路器，
   则从任意故障源 v0 出发的故障传播作用域恰好为单点集合 {v0}。

   形式化: all_edges_have_cb G cb ->
           forall v, in_fault_scope G cb v0 v <-> v = v0

   证明策略:
   1. (->): 设 v 在故障作用域中。
      - 若 v = v0，结论成立。
      - 若 v <> v0，由 fault_scope_has_predecessor，存在 u 使得
        in_fault_scope G cb v0 u 且 fault_step G cb u v。
      - 但 all_cb_no_fault_step 表明在全边 CB 配置下 fault_step 永假。
      - 矛盾。故 v = v0。
   2. (<-): 由 FS_Refl，v0 总在自身作用域中。故 {v0} ⊆ scope(v0)。
   3. 综上，scope(v0) = {v0} (集合意义下)。

   工程解释: 当每条依赖边均配置断路器时，故障在传播的第一跳即被阻断。
   任何下游组件都不会因上游故障而失效，实现了理想的故障隔离。
*)
Theorem cb_all_single_hop :
  forall G cb v0,
    DAG G ->
    all_edges_have_cb G cb ->
    forall v, in_fault_scope G cb v0 v <-> v = v0.
Proof.
  intros G cb v0 Hdag Hall v. split.
  - (* 正向: in_fault_scope -> v = v0 *)
    intro Hscope.
    destruct (comp_eq_dec v v0) as [Heq | Hneq].
    + (* v = v0 *)
      exact Heq.
    + (* v <> v0, 导出矛盾 *)
      apply fault_scope_has_predecessor in Hscope as [u [Hu Hstep]]; auto.
      (* 全边 CB 配置下不存在 fault_step *)
      apply (all_cb_no_fault_step G cb u v Hall).
      exact Hstep.
  - (* 反向: v = v0 -> in_fault_scope *)
    intro Heq. subst v. apply FS_Refl.
Qed.

(* 推论: 故障作用域的基数为 1 *)
Corollary cb_all_scope_cardinality_one :
  forall G cb v0,
    DAG G ->
    all_edges_have_cb G cb ->
    (forall v, in_fault_scope G cb v0 v -> v = v0) /\
    in_fault_scope G cb v0 v0.
Proof.
  intros G cb v0 Hdag Hall.
  split.
  - (* 作用域中任意元素等于 v0 *)
    intro v. apply cb_all_single_hop; auto.
  - (* v0 自身在作用域中 *)
    apply FS_Refl.
Qed.

End CircuitBreaker_Theorem.

(* ---------------------------------------------------------------------------- *)
(* Section 4: 与源文档对应关系                                                  *)
(* ---------------------------------------------------------------------------- *)

(*
文档对应:
- Def-TS-04-02-01 (断路器):         has_cb / CircuitBreakerConfig 定义
- Def-TS-04-02-05 (级联故障):       in_fault_scope 归纳定义
- Def-TS-04-02-01 状态转移:         工程层面见源文档，此处抽象为布尔配置
- Lemma-TS-04-02-03 (CB缩减作用域): cb_reduces_scope
- Thm-TS-04-02-01 (单跳隔离):       cb_all_single_hop
- Cor-TS-04-02-01 (基数推论):       cb_all_scope_cardinality_one

形式化抽象:
- 将断路器的三态状态机 (Closed/Open/Half-Open) 抽象为边上的二元配置
- 将故障检测时间 T_detect 与过载时间 T_overload 抽象为传播/阻断的定性区分
- 将降级模式抽象为"不沿该边传播故障"
- DAG 假设排除了分布式系统中循环依赖的退化情况
*)

(* ============================================================================ *)
(* End of TechStack_CircuitBreaker.v                                            *)
(* ============================================================================ *)
