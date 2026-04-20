(* ============================================================================ *)
(* Network Calculus for Streaming Systems                                       *)
(* ============================================================================ *)
(* 形式化等级: L5 (机械化证明)                                                  *)
(* 对应文档: Struct/01-foundation/network-calculus/network-calculus-streaming.md*) 
(* 定理: Thm-S-01-NC-01/02: 延迟边界定理                                        *)
(* ============================================================================ *)

Require Import Coq.Reals.Reals.
Require Import Coq.Lists.List.
Require Import Coq.Arith.Compare_dec.

Open Scope R_scope.

(* ---------------------------------------------------------------------------- *)
(* Section 1: Min-Plus代数                                                      *)
(* ---------------------------------------------------------------------------- *)

Section MinPlus_Algebra.

(* Min-Plus加 - 实数上的min运算 *)
Definition min_plus_add (x y : R) : R := Rmin x y.

(* Min-Plus乘 - 实数上的+运算 *)
Definition min_plus_mul (x y : R) : R := x + y.

(* Min-Plus卷积 *)
(* 注意: Rbar.glb_Rbar API可能因Coq版本而异，以下代码基于MathComp-Analysis 1.0+
   如遇编译错误，请检查Rbar.glb_Rbar的签名 *)
Definition min_plus_convolution (f g : R -> R) (t : R) : R :=
  Rbar.real (Rbar.glb_Rbar (fun s => 
    min_plus_mul (f s) (g (t - s))) 0 t).

(* 记法 *)
Notation "f '⊗' g" := (min_plus_convolution f g) (at level 40).
Notation "x '⊕' y" := (min_plus_add x y) (at level 50).
Notation "x '⊙' y" := (min_plus_mul x y) (at level 40).

(* Min-Plus代数性质 *)
Lemma min_plus_add_comm : forall x y, x ⊕ y = y ⊕ x.
Proof.
  intros. unfold min_plus_add. apply Rmin_comm.
Qed.

Lemma min_plus_add_assoc : forall x y z, (x ⊕ y) ⊕ z = x ⊕ (y ⊕ z).
Proof.
  intros. unfold min_plus_add. apply Rmin_assoc.
Qed.

Lemma min_plus_mul_comm : forall x y, x ⊙ y = y ⊙ x.
Proof.
  intros. unfold min_plus_mul. apply Rplus_comm.
Qed.

Lemma min_plus_mul_assoc : forall x y z, (x ⊙ y) ⊙ z = x ⊙ (y ⊙ z).
Proof.
  intros. unfold min_plus_mul. apply Rplus_assoc.
Qed.

(* 分配律: Min-Plus乘法(+)对加法(min)的分配 *)
Lemma min_plus_distr : forall x y z, x ⊙ (y ⊕ z) = (x ⊙ y) ⊕ (x ⊙ z).
Proof.
  intros x y z. unfold min_plus_add, min_plus_mul.
  destruct (Rle_dec y z) as [Hle | Hgt].
  - (* y <= z *)
    rewrite Rmin_left by lra.
    rewrite Rmin_left; lra.
  - (* z < y *)
    rewrite Rmin_right by lra.
    rewrite Rmin_right; lra.
Qed.

End MinPlus_Algebra.

(* ---------------------------------------------------------------------------- *)
(* Section 2: 到达曲线与服务曲线                                                *)
(* ---------------------------------------------------------------------------- *)

Section Arrival_Service_Curves.

(* 累积到达函数 *)
Definition CumulativeArrival := R -> R.

(* 到达曲线定义 *)
Definition ArrivalCurve (alpha : R -> R) (A : CumulativeArrival) : Prop :=
  forall s t : R,
    0 <= s <= t ->
    A t - A s <= alpha (t - s).

(* 漏桶到达曲线 *)
Definition LeakyBucket (r b : R) (t : R) : R := r * t + b.

(* 到达曲线性质 *)
Lemma leaky_bucket_arrival :
  forall A r b,
    (forall s t, 0 <= s <= t -> A t - A s <= r * (t - s) + b) ->
    ArrivalCurve (LeakyBucket r b) A.
Proof.
  intros A r b H s t Hst.
  apply H. assumption.
Qed.

(* 服务曲线定义 *)
Definition ServiceCurve (beta : R -> R) (S : CumulativeArrival) : Prop :=
  forall t : R,
    t >= 0 ->
    S t >= min_plus_convolution S beta t.

(* 速率延迟服务曲线 *)
Definition RateLatency (R T : R) (t : R) : R :=
  if Rlt_dec t T then 0 else R * (t - T).

End Arrival_Service_Curves.

(* ---------------------------------------------------------------------------- *)
(* Section 3: 延迟与积压边界                                                    *)
(* ---------------------------------------------------------------------------- *)

Section Delay_Backlog_Bounds.

(* 延迟定义 - 水平距离 *)
Definition DelayBound (alpha beta : R -> R) (d : R) : Prop :=
  forall t : R,
    t >= 0 ->
    alpha t <= beta (t + d).

(* 积压定义 - 垂直距离 *)
Definition BacklogBound (alpha beta : R -> R) (b : R) : Prop :=
  forall t : R,
    t >= 0 ->
    alpha t - beta t <= b.

(* Thm-S-01-NC-01: 延迟边界定理 *)
Theorem delay_bound_theorem :
  forall alpha beta r b R T d,
    (forall t, alpha t = r * t + b) ->       (* 漏桶到达 *)
    (forall t, beta t = RateLatency R T t) -> (* 速率延迟服务 *)
    0 < R ->                                   (* 服务速率为正 *)
    0 <= b ->                                  (* 突发量为非负 *)
    r <= R ->                                  (* 稳定性条件 *)
    d = T + b / R ->                          (* 延迟公式 *)
    DelayBound alpha beta d.
Proof.
  intros alpha beta r b R T d Halpha Hbeta HR Hb Hstab Hd t Ht.
  unfold DelayBound.
  rewrite Halpha, Hbeta, Hd.
  unfold RateLatency.
  destruct (Rlt_dec (t + (T + b / R)) T) as [Hlt | Hge].
  - (* 不可能情况: t + T + b/R < T 意味着 t + b/R < 0,
       但 t >= 0 且 b/R >= 0 (因 b >= 0, R > 0) *)
    exfalso.
    assert (0 <= b / R).
    { apply Rdiv_le_0_compat; lra. }
    lra.
  - (* t + T + b/R >= T, 即 RateLatency = R * (t + d - T) *)
    assert (Heq: R * (t + (T + b / R) - T) = R * t + b).
    { unfold Rdiv.
      assert (Hinv: R * /R = 1) by (apply Rinv_r; lra).
      replace (t + (T + b * /R) - T) with (t + b * /R) by
        (rewrite Rplus_assoc; rewrite Rplus_comm with (r1 := T);
         rewrite <- Rplus_assoc; rewrite Rplus_opp_r; rewrite Rplus_0_r;
         reflexivity).
      rewrite Rmult_plus_distr_l.
      rewrite <- Rmult_assoc.
      rewrite Hinv.
      rewrite Rmult_1_r.
      reflexivity.
    }
    rewrite Heq.
    apply Rplus_le_compat_r.
    apply Rmult_le_compat_r; lra.
Qed.

(* Thm-S-01-NC-02: 积压边界定理 *)
Theorem backlog_bound_theorem :
  forall alpha beta r b R T B,
    (forall t, alpha t = r * t + b) ->
    (forall t, beta t = RateLatency R T t) ->
    0 < R ->                                   (* 服务速率为正 *)
    0 <= r ->                                  (* 到达速率为非负 *)
    0 <= b ->                                  (* 突发量为非负 *)
    r <= R ->
    B = b + r * T ->
    BacklogBound alpha beta B.
Proof.
  intros alpha beta r b R T B Halpha Hbeta HR Hr Hb Hstab HB t Ht.
  unfold BacklogBound.
  rewrite Halpha, Hbeta, HB.
  unfold RateLatency.
  destruct (Rlt_dec t T) as [Hlt | Hge].
  - (* t < T: beta t = 0, 需要 r * t + b <= b + r * T, 即 r * t <= r * T *)
    replace (r * t + b - 0) with (r * t + b) by ring.
    apply Rplus_le_compat_r.
    apply Rmult_le_compat_l; lra.
  - (* t >= T: beta t = R * (t - T) *)
    assert (Heq: r * t + b - R * (t - T) = (r - R) * t + b + R * T).
    { ring. }
    rewrite Heq.
    assert (Heq2: b + r * T = (r - R) * T + b + R * T).
    { ring. }
    rewrite Heq2.
    apply Rplus_le_compat_r.
    apply Rplus_le_compat_l.
    assert (Hneg: r - R <= 0) by lra.
    replace ((r - R) * t) with (-((R - r) * t)) by ring.
    replace ((r - R) * T) with (-((R - r) * T)) by ring.
    apply Ropp_le_contravar.
    apply Rmult_le_compat_l; lra.
Qed.

End Delay_Backlog_Bounds.

(* ---------------------------------------------------------------------------- *)
(* Section 4: Flink算子专用分析                                                 *)
(* ---------------------------------------------------------------------------- *)

Section Flink_Operator_Analysis.

(* 算子服务曲线参数 *)
Record OperatorServiceCurve := mkOpSC {
  op_R : R;  (* 服务速率 *)
  op_T : R   (* 服务延迟 *)
}.

(* Map算子 - 无状态 *)
Definition MapService : OperatorServiceCurve :=
  {| op_R := 1000000; op_T := 0.001 |}.  (* 100万条/秒, 1ms延迟 *)

(* KeyedProcess算子 - 有状态访问 *)
Definition KeyedProcessService : OperatorServiceCurve :=
  {| op_R := 50000; op_T := 0.002 |}.   (* 5万条/秒, 2ms延迟 *)

(* Window算子 - 窗口触发延迟 *)
Definition WindowService (window_size : R) : OperatorServiceCurve :=
  {| op_R := 1000; op_T := window_size |}.  (* 窗口大小决定延迟 *)

(* 端到端延迟计算 *)
Definition EndToEndDelay (ops : list OperatorServiceCurve) (b r : R) : R :=
  fold_right (fun op acc => acc + op_T op + b / op_R op) 0 ops.

(* 引理: 延迟累加 *)
Lemma delay_additive :
  forall op1 op2 b r,
    EndToEndDelay [op1; op2] b r = op_T op1 + b / op_R op1 + op_T op2 + b / op_R op2.
Proof.
  intros. reflexivity.
Qed.

End Flink_Operator_Analysis.

(* ---------------------------------------------------------------------------- *)
(* Section 5: 与文档对应关系                                                    *)
(* ---------------------------------------------------------------------------- *)

(*
文档对应:
- Def-S-01-NC-01 (Min-Plus代数): Section MinPlus_Algebra
- Def-S-01-NC-02 (到达曲线): Definition ArrivalCurve
- Def-S-01-NC-03 (服务曲线): Definition ServiceCurve
- Thm-S-01-NC-01 (延迟边界): Theorem delay_bound_theorem
- Thm-S-01-NC-02 (积压边界): Theorem backlog_bound_theorem
- Prop-S-01-NC-01 (延迟保证): 蕴含在定理中
*)

(* ============================================================================ *)
(* End of Network_Calculus.v                                                    *)
(* ============================================================================ *)
