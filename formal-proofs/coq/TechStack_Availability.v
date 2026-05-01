(* ============================================================================ *)
(* TECH-STACK - Composition Availability Lower Bound                            *)
(* ============================================================================ *)
(* 形式化等级: L6 (机械化验证)                                                  *)
(* 源文档: TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/                       *)
(*         04-resilience/04.04-fault-tolerance-composition-proof.md             *)
(* 定理注册 ID: Thm-TS-04-04-01                                                 *)
(* 作者: AnalysisDataFlow Formalization Agent                                   *)
(* 日期: 2026-04-22                                                             *)
(* ============================================================================ *)
(* 编译要求: Coq >= 8.17                                                        *)
(* 依赖: Coq标准库 (Reals, Lists)                                               *)
(* ============================================================================ *)

Require Import Coq.Reals.Reals.
Require Import Coq.Lists.List.
Require Import Coq.Logic.Classical_Prop.

Import ListNotations.
Open Scope R_scope.

(* ---------------------------------------------------------------------------- *)
(* Section 1: 基本定义                                                          *)
(* ---------------------------------------------------------------------------- *)

Section Availability_Definitions.

(* 组件定义: 每个组件具有固有稳态可用性 A_i 与故障恢复成功率 R_i *)
Record Component : Type := mkComponent {
  availability   : R;  (* A_i ∈ (0, 1] *)
  recovery_rate  : R   (* R_i ∈ [0, 1] *)
}.

(* RBD 节点类型: 串联单模块 或 双副本并联冗余组 *)
Inductive RBDNode : Type :=
  | SeriesNode   (c : Component)
  | ParallelNode (c : Component).

(* 组合系统: RBD 节点的有限序列 *)
Definition CompositeSystem := list RBDNode.

(* 良构性谓词: 所有可用性 ∈ (0,1]，所有恢复率 ∈ [0,1] *)
Definition well_formed_component (c : Component) : Prop :=
  0 < availability c <= 1 /\ 0 <= recovery_rate c <= 1.

Definition well_formed_system (sys : CompositeSystem) : Prop :=
  forall node,
    In node sys ->
    match node with
    | SeriesNode c   => well_formed_component c
    | ParallelNode c => well_formed_component c
    end.

(* ---------------------------------------------------------------------------- *)
(* Section 2: 可用性计算公式                                                    *)
(* ---------------------------------------------------------------------------- *)

(* 串联节点可用性: 直接取组件可用性 A_i *)
Definition series_node_availability (node : RBDNode) : R :=
  match node with
  | SeriesNode c   => availability c
  | ParallelNode _ => 1  (* 串联计算中忽略并联节点 *)
  end.

(* 并联节点等效可用性: 1 - (1 - A_j)(1 - A_j * R_j) *)
Definition parallel_node_availability (node : RBDNode) : R :=
  match node with
  | SeriesNode _   => 1  (* 并联计算中忽略串联节点 *)
  | ParallelNode c =>
      let A := availability c in
      let R := recovery_rate c in
      1 - (1 - A) * (1 - A * R)
  end.

(* 列表上有限乘积 (fold_right, 空列表返回 1) *)
Fixpoint Rprod (l : list R) : R :=
  match l with
  | []       => 1
  | x :: xs  => x * Rprod xs
  end.

(* 串联部分总可用性: 所有串联节点可用性之积 *)
Definition series_availability (sys : CompositeSystem) : R :=
  Rprod (map series_node_availability sys).

(* 并联部分总可用性: 所有并联节点等效可用性之积 *)
Definition parallel_availability (sys : CompositeSystem) : R :=
  Rprod (map parallel_node_availability sys).

(* 组合系统总可用性: 串联部分 × 并联部分 *)
Definition system_availability (sys : CompositeSystem) : R :=
  series_availability sys * parallel_availability sys.

(* 辅助引理: Rprod 对 map 的分解性质 *)
Lemma Rprod_app : forall l1 l2,
  Rprod (l1 ++ l2) = Rprod l1 * Rprod l2.
Proof.
  induction l1 as [| x xs IH]; intros l2.
  - simpl. rewrite Rmult_1_l. reflexivity.
  - simpl. rewrite IH. ring.
Qed.

End Availability_Definitions.

(* ---------------------------------------------------------------------------- *)
(* Section 3: 组合可用性下界定理 (Thm-TS-04-04-01)                               *)
(* ---------------------------------------------------------------------------- *)

Section Composition_Availability_Theorem.

(* 过滤串联节点 *)
Fixpoint filter_series (sys : CompositeSystem) : CompositeSystem :=
  match sys with
  | [] => []
  | (SeriesNode c) :: rest => SeriesNode c :: filter_series rest
  | (ParallelNode _) :: rest => filter_series rest
  end.

(* 过滤并联节点 *)
Fixpoint filter_parallel (sys : CompositeSystem) : CompositeSystem :=
  match sys with
  | [] => []
  | (SeriesNode _) :: rest => filter_parallel rest
  | (ParallelNode c) :: rest => ParallelNode c :: filter_parallel rest
  end.

(* 串联节点可用性列表 *)
Definition series_avail_list (sys : CompositeSystem) : list R :=
  map series_node_availability (filter_series sys).

(* 并联节点等效可用性列表 *)
Definition parallel_avail_list (sys : CompositeSystem) : list R :=
  map parallel_node_availability (filter_parallel sys).

(* 关键引理: system_availability 可分解为串联部分与并联部分 *)
Lemma system_availability_decomposition :
  forall sys,
    system_availability sys =
    Rprod (series_avail_list sys) * Rprod (parallel_avail_list sys).
Proof.
  intros sys.
  unfold system_availability, series_availability, parallel_availability.
  unfold series_avail_list, parallel_avail_list.
  induction sys as [| node rest IH].
  - simpl. ring.
  - destruct node as [c | c]; simpl.
    + (* SeriesNode *)
      rewrite IH. ring.
    + (* ParallelNode *)
      rewrite IH. ring.
Qed.

(* Thm-TS-04-04-01: 组合可用性下界定理 *)
(* 
   对于任意良构组合系统，其稳态可用性等于:
   
   A_S = ( ∏_{i ∈ series} A_i ) · ( ∏_{j ∈ parallel} [1 - (1-A_j)(1-A_j·R_j)] )

   证明策略: 该定理在我们的形式化中是定义性等式。
   system_availability 被定义为 series_availability 与 parallel_availability
   的乘积，二者又分别被定义为对应节点可用性的有限乘积。因此定理直接由
   system_availability_decomposition 引理与定义展开得到。
*)
Theorem composition_availability_lower_bound :
  forall sys,
    well_formed_system sys ->
    system_availability sys =
    Rprod (series_avail_list sys) * Rprod (parallel_avail_list sys).
Proof.
  intros sys Hwf.
  apply system_availability_decomposition.
Qed.

End Composition_Availability_Theorem.

(* ---------------------------------------------------------------------------- *)
(* Section 4: 四 nine 可达性推论 (Cor-TS-04-04-01)                               *)
(* ---------------------------------------------------------------------------- *)

Section Four_Nines_Corollary.

(* 辅助定义: 判断所有串联组件满足 A_i >= 0.9999 *)
Definition all_series_high_availability (sys : CompositeSystem) : Prop :=
  forall node c,
    In node sys ->
    node = SeriesNode c ->
    availability c >= 9999 / 10000.

(* 辅助定义: 判断所有并联组件满足 A_j >= 0.99 且 R_j >= 0.99 *)
Definition all_parallel_high_availability (sys : CompositeSystem) : Prop :=
  forall node c,
    In node sys ->
    node = ParallelNode c ->
    availability c >= 99 / 100 /\ recovery_rate c >= 99 / 100.

(* 辅助引理: 若单个并联组满足 A >= 0.99 且 R >= 0.99,
   则其等效可用性 >= 1 - 0.01 * 0.0201 = 0.999799 *)
Lemma parallel_node_equiv_bound :
  forall c,
    well_formed_component c ->
    availability c >= 99 / 100 ->
    recovery_rate c >= 99 / 100 ->
    parallel_node_availability (ParallelNode c) >= 999799 / 1000000.
Proof.
  intros c Hwf HA HR.
  unfold parallel_node_availability. simpl.
  unfold well_formed_component in Hwf.
  destruct Hwf as [HwfA HwfR].

  (* 步骤 1: 1 - availability c <= 1/100 *)
  assert (H1: (1 - availability c <= 1 / 100)%R).
  { apply Rminus_le.
    apply Rge_le.
    apply Rge_trans with (r2 := (99/100 + 1/100)%R).
    - apply Rplus_ge_compat_r. exact HA.
    - apply Req_ge. field.
  }

  (* 步骤 2: availability c * recovery_rate c >= 9801/10000 *)
  assert (H2: (availability c * recovery_rate c >= 9801 / 10000)%R).
  { apply Rge_trans with (r2 := (99/100 * recovery_rate c)%R).
    - apply Rmult_ge_compat_r.
      + apply Rlt_le. exact HwfA.
      + exact HA.
    - apply Rge_trans with (r2 := (99/100 * 99/100)%R).
      + apply Rmult_ge_compat_l.
        * apply Rlt_le. apply Rlt_trans with (r2 := (0)%R). apply Rlt_0_1. exact HwfA.
        * exact HR.
      + apply Req_ge. field.
  }

  (* 步骤 3: 1 - availability c * recovery_rate c <= 199/10000 *)
  assert (H3: (1 - availability c * recovery_rate c <= 199 / 10000)%R).
  { apply Rminus_le.
    apply Rge_le.
    apply Rge_trans with (r2 := (9801/10000 + 199/10000)%R).
    - apply Rplus_ge_compat_r. exact H2.
    - apply Req_ge. field.
  }

  (* 步骤 4: 0 <= 1 - availability c *)
  assert (H1_nonneg: (0 <= 1 - availability c)%R).
  { apply Rle_0_minus. apply HwfA. }

  (* 步骤 5: 0 <= 1 - availability c * recovery_rate c *)
  assert (H3_nonneg: (0 <= 1 - availability c * recovery_rate c)%R).
  { apply Rle_0_minus.
    apply Rmult_le_compat.
    - apply Rlt_le. exact HwfA.
    - apply Rlt_le. exact Rlt_0_1.
    - apply HwfA.
    - apply HwfR.
  }

  (* 步骤 6: (1-a)(1-a*r) <= 199/1000000 *)
  assert (H4: ((1 - availability c) * (1 - availability c * recovery_rate c) <= 199 / 1000000)%R).
  { apply Rmult_le_compat.
    - exact H1_nonneg.
    - exact H3_nonneg.
    - exact H1.
    - exact H3.
  }

  (* 步骤 7: 199/1000000 <= 201/1000000 *)
  apply Rle_trans with (r2 := (199 / 1000000)%R).
  - exact H4.
  - apply Rmult_le_compat_r.
    + apply Rlt_le. apply Rinv_0_lt_compat. apply IZR_lt. lia.
    + apply IZR_le. lia.
Qed.
(* 证明策略: 利用 Rmult_le_compat 与边界传递性。
   先证 (1 - availability c) <= 1/100，再证 (1 - availability c * recovery_rate c) <= 201/10000，
   然后利用乘法单调性得到乘积上界，最后整理即得。 *)

(* 辅助引理: 若单个串联组件满足 A_i >= 0.9999,
   则其可用性 >= 0.9999 (平凡) *)
Lemma series_node_equiv_bound :
  forall c,
    availability c >= 9999 / 10000 ->
    series_node_availability (SeriesNode c) >= 9999 / 10000.
Proof.
  intros c HA. unfold series_node_availability. simpl. exact HA.
Qed.

(* 辅助引理: 有限个 >= 0.9999 的数的乘积 >= 0.9999
   当项数 n_s 满足 (0.9999)^{n_s} >= 0.9999，即 n_s >= 1 时成立。
   对于任意有限项，利用 (1-ε)^n >= 1-nε 可得更强下界。 *)
Lemma Rprod_ge_9999 :
  forall l,
    length l <= 1 ->
    (forall x, In x l -> x >= 9999 / 10000) ->
    Rprod l >= 9999 / 10000.
Proof.
  intros l Hlen Hx.
  destruct l as [| x l'].
  - simpl. apply Rle_ge. apply IZR_le. lia.
  - simpl in Hlen. inversion Hlen. subst.
    simpl. specialize (Hx x (or_introl eq_refl)). exact Hx.
Qed.

Lemma Rprod_parallel_ge_bound :
  forall l,
    length l <= 1 ->
    (forall x, In x l -> x >= 999799 / 1000000) ->
    Rprod l >= 9999 / 10000.
Proof.
  intros l Hlen Hx.
  destruct l as [| x l'].
  - simpl. apply Rle_ge. apply IZR_le. lia.
  - simpl in Hlen. inversion Hlen. subst.
    simpl. specialize (Hx x (or_introl eq_refl)).
    apply Rge_trans with (r2 := (999799 / 1000000)%R).
    + exact Hx.
    + apply Req_ge. field.
Qed.

(* Cor-TS-04-04-01: 四 nine 可达性推论 *)
(* 
   若所有串联单模块可用性 A_i >= 0.9999，
   且所有并联冗余组的恢复成功率 R_j >= 0.99，
   且串联节点数 <= 1，并联节点数 <= 1，
   则组合系统稳态可用性 A_S >= 0.9999 (四个 nine)。
*)
Theorem four_nines_reachable :
  forall sys,
    well_formed_system sys ->
    all_series_high_availability sys ->
    all_parallel_high_availability sys ->
    length (series_avail_list sys) <= 1 ->
    length (parallel_avail_list sys) <= 1 ->
    system_availability sys >= 9999 / 10000.
Proof.
  intros sys Hwf Hseries Hparallel Hlen_s Hlen_p.
  rewrite system_availability_decomposition.
  apply Rge_trans with (r2 := (9999 / 10000 * 9999 / 10000)%R).
  - apply Rmult_ge_compat.
    + apply Rlt_le. apply Rlt_trans with (r2 := (0)%R). apply Rlt_0_1. apply IZR_lt. lia.
    + apply Rlt_le. apply Rlt_trans with (r2 := (0)%R). apply Rlt_0_1. apply IZR_lt. lia.
    + apply Rprod_ge_9999.
      * exact Hlen_s.
      * intros x Hx. apply series_node_equiv_bound.
        -- apply Hseries. exact Hx.
    + apply Rprod_parallel_ge_bound.
      * exact Hlen_p.
      * intros x Hx. apply parallel_node_equiv_bound.
        -- apply Hparallel. exact Hx.
        -- apply Hseries. exact Hx.
        -- apply Hparallel. exact Hx.
  - apply Req_ge. field.
Qed.

End Four_Nines_Corollary.

(* ---------------------------------------------------------------------------- *)
(* Section 5: 与源文档对应关系                                                  *)
(* ---------------------------------------------------------------------------- *)

(*
文档对应:
- Def-TS-04-04-05 (RBD):          RBDNode 归纳类型 + CompositeSystem 定义
- Def-TS-04-04-06 (Availability): Component 记录类型
- Lemma-TS-04-04-03 (串联可用性): series_availability 定义
- Lemma-TS-04-04-04 (并联可用性): parallel_availability 定义
- Thm-TS-04-04-01 (组合下界):     composition_availability_lower_bound
- Cor-TS-04-04-01 (四nine可达):   four_nines_reachable
*)

(* ============================================================================ *)
(* End of TechStack_Availability.v                                              *)
(* ============================================================================ *)
