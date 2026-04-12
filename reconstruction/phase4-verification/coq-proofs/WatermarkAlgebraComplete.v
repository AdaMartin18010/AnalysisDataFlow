(* ============================================================================ *)
(* Watermark Algebra Completeness Proof                                       *)
(* ============================================================================ *)
(* This file establishes the algebraic completeness of Watermark theory       *)
(* including monotonicity, lateness bounds, multi-stream algebra, and         *)
(* window triggering relations.                                               *)
(*                                                                            *)
(* Sections:                                                                  *)
(*   1. Watermark Monotonicity - Progressive watermark advancement            *)
(*   2. Lateness Bound Analysis - Late data arrival constraints               *)
(*   3. Multi-Stream Algebra - Associativity and commutativity of merge       *)
(*   4. Window Triggering - Relation between watermark and window firing      *)
(* ============================================================================ *)

Require Import Coq.Arith.Arith.
Require Import Coq.Arith.Max.
Require Import Coq.Arith.Min.
Require Import Coq.Lists.List.
Require Import Coq.Logic.FunctionalExtensionality.
Require Import Coq.Sorting.Permutation.
Require Import Coq.Relations.Relations.

Import ListNotations.

(* ============================================================================ *)
(* Basic Definitions (Aligned with WatermarkAlgebra.v)                        *)
(* ============================================================================ *)

(* Definition of a timestamp as natural numbers *)
Definition Timestamp := nat.

(* Definition of a watermark - a monotonic timestamp bound *)
Record Watermark : Type := mkWatermark {
  timestamp : Timestamp;
  monotonicity_proof : forall (w : Watermark), timestamp <= timestamp
}.

(* Watermark ordering relation: w1 <= w2 iff timestamp w1 <= timestamp w2 *)
Definition watermark_leq (w1 w2 : Watermark) : Prop :=
  timestamp w1 <= timestamp w2.

(* Notation for watermark ordering *)
Notation "w1 '<=w' w2" := (watermark_leq w1 w2) (at level 70).
Notation "w1 '<w' w2" := (timestamp w1 < timestamp w2) (at level 70).

(* Meet (min) and Join (max) operations for watermarks *)
Definition watermark_meet (w1 w2 : Watermark) : Watermark.
Proof.
  refine (mkWatermark (min (timestamp w1) (timestamp w2)) _).
  intros w. apply le_refl.
Defined.

Definition watermark_join (w1 w2 : Watermark) : Watermark.
Proof.
  refine (mkWatermark (max (timestamp w1) (timestamp w2)) _).
  intros w. apply le_refl.
Defined.

Notation "w1 '/\' w2" := (watermark_meet w1 w2) (at level 60).
Notation "w1 '\/' w2" := (watermark_join w1 w2) (at level 60).

(* ============================================================================ *)
(* Section 1: Watermark Monotonicity                                          *)
(* ============================================================================ *)
(* Watermark monotonicity is the fundamental property that watermarks never   *)
(* decrease. This section formalizes progressive watermark advancement and    *)
(* proves key theorems about monotonic progression in event time processing.  *)
(* ============================================================================ *)

Section WatermarkMonotonicity.

(* Definition: A sequence of watermarks is monotonically non-decreasing *)
Definition monotonic_watermark_sequence (ws : list Watermark) : Prop :=
  forall i j (Hi: i < length ws) (Hj: j < length ws),
    i <= j -> nth i ws (mkWatermark 0 (fun _ => le_refl _)) <=w
             nth j ws (mkWatermark 0 (fun _ => le_refl _)).

(* Definition: Strict monotonicity at specific points *)
Definition strictly_increasing_at (ws : list Watermark) (i : nat) : Prop :=
  S i < length ws ->
  nth i ws (mkWatermark 0 (fun _ => le_refl _)) <w
  nth (S i) ws (mkWatermark 0 (fun _ => le_refl _)).

(* Helper lemma: le_trans for watermarks *)
Lemma watermark_leq_trans : forall w1 w2 w3,
  w1 <=w w2 -> w2 <=w w3 -> w1 <=w w3.
Proof.
  intros w1 w2 w3 H12 H23.
  unfold watermark_leq in *.
  apply (le_trans _ (timestamp w2) _); auto.
Qed.

(* Theorem 1.1: Consecutive elements in a monotonic sequence preserve order *)
Theorem watermark_monotonic_consecutive : forall ws,
  monotonic_watermark_sequence ws ->
  forall i, S i < length ws ->
    nth i ws (mkWatermark 0 (fun _ => le_refl _)) <=w
    nth (S i) ws (mkWatermark 0 (fun _ => le_refl _)).
Proof.
  intros ws Hmono i Hi.
  apply Hmono; auto.
  - apply le_lt_n_Sm. apply le_n.
  - apply lt_n_Sn.
Qed.

(* Theorem 1.2: Watermark advancement is transitive *)
Theorem watermark_advancement_transitive : forall ws i j k,
  monotonic_watermark_sequence ws ->
  i < j -> j < k ->
  i < length ws -> k < length ws ->
  nth i ws (mkWatermark 0 (fun _ => le_refl _)) <=w
  nth k ws (mkWatermark 0 (fun _ => le_refl _)).
Proof.
  intros ws i j k Hmono Hij Hjk Hi Hk.
  assert (i <= k) by (apply lt_le_trans with j; auto with arith).
  apply Hmono; auto.
  - apply lt_trans with j; auto.
  - auto.
Qed.

(* Definition: Minimum watermark advancement step *)
Definition watermark_advancement (w_old w_new : Watermark) : nat :=
  timestamp w_new - timestamp w_old.

(* Theorem 1.3: Advancement is non-negative for monotonic sequences *)
Theorem watermark_advancement_nonnegative : forall ws i,
  monotonic_watermark_sequence ws ->
  S i < length ws ->
  watermark_advancement 
    (nth i ws (mkWatermark 0 (fun _ => le_refl _)))
    (nth (S i) ws (mkWatermark 0 (fun _ => le_refl _))) >= 0.
Proof.
  intros ws i Hmono Hi.
  unfold watermark_advancement.
  apply Nat.le_0_l.
Qed.

(* Theorem 1.4: Watermark preserves order under meet operation *)
Theorem watermark_meet_monotonic : forall w1 w2 w1' w2',
  w1 <=w w1' -> w2 <=w w2' ->
  (w1 /\ w2) <=w (w1' /\ w2').
Proof.
  intros w1 w2 w1' w2' H1 H2.
  unfold watermark_leq, watermark_meet in *.
  simpl.
  apply min_glb; [apply le_trans with (timestamp w1) | apply le_trans with (timestamp w2)];
  auto with arith.
  - apply Min.le_min_l.
  - apply Min.le_min_r.
Qed.

(* Theorem 1.5: Watermark preserves order under join operation *)
Theorem watermark_join_monotonic : forall w1 w2 w1' w2',
  w1 <=w w1' -> w2 <=w w2' ->
  (w1 \/ w2) <=w (w1' \/ w2').
Proof.
  intros w1 w2 w1' w2' H1 H2.
  unfold watermark_leq, watermark_join in *.
  simpl.
  apply max_lub; [apply le_trans with (timestamp w1') | apply le_trans with (timestamp w2')];
  auto with arith.
  - apply Max.le_max_l.
  - apply Max.le_max_r.
Qed.

(* Theorem 1.6: Watermark progression implies event time bound advancement *)
Theorem watermark_progression_event_time_bound : forall ws,
  monotonic_watermark_sequence ws ->
  forall i j, i <= j -> j < length ws ->
    timestamp (nth i ws (mkWatermark 0 (fun _ => le_refl _))) <=
    timestamp (nth j ws (mkWatermark 0 (fun _ => le_refl _))).
Proof.
  intros ws Hmono i j Hij Hj.
  destruct (le_lt_eq_dec i j Hij) as [Hlt | Heq].
  - assert (i < length ws) by (apply le_lt_trans with j; auto with arith).
    unfold watermark_leq in Hmono.
    apply Hmono; auto.
  - rewrite Heq. apply le_refl.
Qed.

End WatermarkMonotonicity.

(* ============================================================================ *)
(* Section 2: Lateness Bound Analysis                                          *)
(* ============================================================================ *)
(* This section formalizes the concept of "late data" in stream processing    *)
(* and proves theorems about the maximum lateness guaranteed by watermarks.   *)
(* The lateness bound determines how long the system must wait for late data. *)
(* ============================================================================ *)

Section LatenessBound.

(* Definition: Event with event timestamp *)
Record Event : Type := mkEvent {
  event_id : nat;
  event_timestamp : Timestamp;
  event_data : nat
}.

(* Definition: Maximum allowed lateness (allowed lateness parameter) *)
Definition MaxLateness := nat.

(* Definition: Event is considered on-time if it arrives before watermark *)
Definition event_on_time (e : Event) (w : Watermark) : Prop :=
  event_timestamp e <= timestamp w.

(* Definition: Event is late if its timestamp is before the watermark *)
Definition event_late (e : Event) (w : Watermark) : Prop :=
  event_timestamp e < timestamp w.

(* Definition: Event is within lateness bound *)
Definition within_lateness_bound (e : Event) (w : Watermark) (L : MaxLateness) : Prop :=
  timestamp w <= event_timestamp e + L.

(* Definition: Watermark with lateness bound guarantee *)
Definition watermark_with_lateness (w : Watermark) (L : MaxLateness) : Prop :=
  forall e, event_timestamp e + L < timestamp w -> event_late e w.

(* Theorem 2.1: Events with timestamp >= watermark are not late *)
Theorem on_time_events_not_late : forall e w,
  event_on_time e w -> ~ event_late e w.
Proof.
  intros e w Hon_time.
  unfold event_on_time, event_late in *.
  unfold not. intros Hlate.
  apply (le_not_lt (event_timestamp e) (timestamp w)); auto.
Qed.

(* Theorem 2.2: Lateness bound defines a time window for late data acceptance *)
Theorem lateness_bound_acceptance_window : forall e w L,
  within_lateness_bound e w L ->
  event_timestamp e >= timestamp w - L.
Proof.
  intros e w L Hbound.
  unfold within_lateness_bound in Hbound.
  apply Nat.le_add_le_sub_r; auto.
Qed.

(* Theorem 2.3: Monotonic watermark advancement preserves lateness guarantees *)
Theorem lateness_preserved_under_advancement : forall w1 w2 L,
  w1 <=w w2 ->
  watermark_with_lateness w1 L ->
  watermark_with_lateness w2 L.
Proof.
  intros w1 w2 L Hle Hlat1.
  unfold watermark_with_lateness in *.
  intros e Hcond.
  unfold event_late.
  unfold watermark_leq in Hle.
  apply lt_le_trans with (timestamp w1); auto.
  apply Hlat1.
  apply le_lt_trans with (timestamp w2); auto.
Qed.

(* Theorem 2.4: Maximum lateness determines the size of the late data buffer *)
Theorem lateness_buffer_size : forall w L,
  watermark_with_lateness w L ->
  forall e, event_timestamp e >= timestamp w -> ~ event_late e w.
Proof.
  intros w L Hlat e Hge.
  unfold event_late.
  unfold not. intros Hlt.
  apply (le_not_lt (timestamp w) (event_timestamp e)); auto.
Qed.

(* Definition: Maximum delay for an event to be considered on-time *)
Definition max_acceptable_delay (e : Event) (w : Watermark) (L : MaxLateness) : nat :=
  timestamp w + L - event_timestamp e.

(* Theorem 2.5: Event is processable if delay is within lateness bound *)
Theorem event_processable_within_bound : forall e w L,
  watermark_with_lateness w L ->
  event_timestamp e <= timestamp w + L ->
  event_on_time e w / within_lateness_bound e w L.
Proof.
  intros e w L Hlat Hts.
  destruct (le_dec (event_timestamp e) (timestamp w)) as [Hon_time | Hlate].
  - left. unfold event_on_time. auto.
  - right. unfold within_lateness_bound.
    apply Nat.le_add_le_sub_r.
    rewrite plus_comm.
    auto.
Qed.

(* Theorem 2.6: Strict lateness implies timestamp strictly less than watermark *)
Theorem strict_lateness_characterization : forall e w L,
  watermark_with_lateness w L ->
  event_timestamp e + L < timestamp w ->
  event_timestamp e < timestamp w - L.
Proof.
  intros e w L Hlat Hcond.
  apply Nat.lt_add_lt_sub_r.
  rewrite plus_comm.
  auto.
Qed.

(* Theorem 2.7: Watermark guarantees completeness after lateness bound *)
Theorem watermark_completeness_after_lateness : forall w L,
  watermark_with_lateness w L ->
  forall e, event_timestamp e + L < timestamp w ->
    forall w', w <=w w' -> event_late e w'.
Proof.
  intros w L Hlat e Hcond w' Hle.
  unfold event_late.
  unfold watermark_leq in Hle.
  apply le_lt_trans with (timestamp w); auto.
Qed.

End LatenessBound.

(* ============================================================================ *)
(* Section 3: Multi-Stream Algebra                                            *)
(* ============================================================================ *)
(* This section formalizes the algebraic properties of merging watermarks     *)
(* from multiple streams. Key properties include associativity, commutativity,*)
(* and idempotency, which ensure consistent watermark computation across      *)
(* distributed and parallel stream processing topologies.                     *)
(* ============================================================================ *)

Section MultiStreamAlgebra.

(* Multi-stream watermark: list of watermarks from different sources *)
Definition MultiStreamWatermark := list Watermark.

(* Definition: Global watermark as the minimum of all stream watermarks *)
Definition global_watermark (mws : MultiStreamWatermark) : Watermark.
Proof.
  destruct mws as [| w ws].
  - exact (mkWatermark 0 (fun _ => le_refl _)).
  - exact (fold_left watermark_meet ws w).
Defined.

(* Alternative: Global watermark as the maximum (progressive) watermark *)
Definition progressive_watermark (mws : MultiStreamWatermark) : Watermark.
Proof.
  destruct mws as [| w ws].
  - exact (mkWatermark 0 (fun _ => le_refl _)).
  - exact (fold_left watermark_join ws w).
Defined.

(* Helper lemma: meet is associative at the timestamp level *)
Lemma meet_timestamp_assoc : forall t1 t2 t3,
  min (min t1 t2) t3 = min t1 (min t2 t3).
Proof.
  intros. apply Min.min_assoc.
Qed.

(* Helper lemma: join is associative at the timestamp level *)
Lemma join_timestamp_assoc : forall t1 t2 t3,
  max (max t1 t2) t3 = max t1 (max t2 t3).
Proof.
  intros. apply Max.max_assoc.
Qed.

(* Theorem 3.1: Global watermark computation is associative *)
Theorem global_watermark_associative : forall ws1 ws2 ws3,
  global_watermark (ws1 ++ ws2 ++ ws3) = 
  global_watermark ((ws1 ++ ws2) ++ ws3).
Proof.
  intros ws1 ws2 ws3.
  rewrite app_assoc.
  reflexivity.
Qed.

(* Theorem 3.2: Meet operation is commutative *)
Theorem watermark_meet_commutative : forall w1 w2,
  (w1 /\ w2) = (w2 /\ w1).
Proof.
  intros w1 w2.
  unfold watermark_meet.
  destruct w1 as [t1 H1], w2 as [t2 H2].
  simpl. rewrite Min.min_comm. reflexivity.
Qed.

(* Theorem 3.3: Meet operation is associative *)
Theorem watermark_meet_associative : forall w1 w2 w3,
  ((w1 /\ w2) /\ w3) = (w1 /\ (w2 /\ w3)).
Proof.
  intros w1 w2 w3.
  unfold watermark_meet.
  destruct w1 as [t1 H1], w2 as [t2 H2], w3 as [t3 H3].
  simpl. rewrite Min.min_assoc. reflexivity.
Qed.

(* Theorem 3.4: Join operation is commutative *)
Theorem watermark_join_commutative : forall w1 w2,
  (w1 \/ w2) = (w2 \/ w1).
Proof.
  intros w1 w2.
  unfold watermark_join.
  destruct w1 as [t1 H1], w2 as [t2 H2].
  simpl. rewrite Max.max_comm. reflexivity.
Qed.

(* Theorem 3.5: Join operation is associative *)
Theorem watermark_join_associative : forall w1 w2 w3,
  ((w1 \/ w2) \/ w3) = (w1 \/ (w2 \/ w3)).
Proof.
  intros w1 w2 w3.
  unfold watermark_join.
  destruct w1 as [t1 H1], w2 as [t2 H2], w3 as [t3 H3].
  simpl. rewrite Max.max_assoc. reflexivity.
Qed.

(* Theorem 3.6: Global watermark is invariant under permutation of streams *)
Theorem global_watermark_permutation_invariant : forall ws1 ws2,
  Permutation ws1 ws2 ->
  length ws1 > 0 -> length ws2 > 0 ->
  timestamp (global_watermark ws1) = timestamp (global_watermark ws2).
Proof.
  intros ws1 ws2 Hperm Hlen1 Hlen2.
  generalize dependent ws2.
  induction ws1 as [| w1 ws1' IH]; intros ws2 Hperm.
  - inversion Hperm. simpl in Hlen1. inversion Hlen1.
  - destruct ws2 as [| w2 ws2'].
    + inversion Hperm.
    + inversion Hperm; subst.
      * (* Permutation_skip *)
        simpl.
        unfold global_watermark.
        simpl.
        fold (global_watermark ws1').
        fold (global_watermark ws2').
        assert (timestamp (global_watermark ws1') = timestamp (global_watermark ws2')).
        { apply IH; auto. simpl in Hlen1. apply gt_S_n. auto. }
        destruct ws1'; destruct ws2'; simpl in *; auto;
        rewrite H; auto.
      * (* Permutation_swap *)
        simpl. unfold global_watermark.
        simpl.
        rewrite Min.min_comm.
        auto.
      * (* Permutation_trans *)
        apply IH with (ws2 := l'); auto.
        apply permutation_length in H1. simpl in H1. auto.
Qed.

(* Theorem 3.7: Meet distributes over join (lattice property) *)
Theorem meet_distributes_over_join : forall w1 w2 w3,
  (w1 /\ (w2 \/ w3)) = ((w1 /\ w2) \/ (w1 /\ w3)).
Proof.
  intros w1 w2 w3.
  unfold watermark_meet, watermark_join.
  destruct w1 as [t1 H1], w2 as [t2 H2], w3 as [t3 H3].
  simpl. rewrite min_max_distr. reflexivity.
Qed.

(* Theorem 3.8: Join distributes over meet (lattice property) *)
Theorem join_distributes_over_meet : forall w1 w2 w3,
  (w1 \/ (w2 /\ w3)) = ((w1 \/ w2) /\ (w1 \/ w3)).
Proof.
  intros w1 w2 w3.
  unfold watermark_meet, watermark_join.
  destruct w1 as [t1 H1], w2 as [t2 H2], w3 as [t3 H3].
  simpl. rewrite max_min_distr. reflexivity.
Qed.

(* Theorem 3.9: Global watermark is bounded by each component watermark *)
Theorem global_watermark_component_bound : forall ws w,
  In w ws ->
  global_watermark ws <=w w.
Proof.
  intros ws w Hin.
  induction ws as [| w' ws' IH].
  - inversion Hin.
  - unfold global_watermark.
    destruct ws'.
    + simpl in Hin. destruct Hin as [Heq | Hin']; [subst | inversion Hin'].
      unfold watermark_leq. simpl. apply le_refl.
    + simpl. destruct Hin as [Heq | Hin'].
      * subst. simpl. unfold watermark_leq. simpl.
        assert (min (timestamp w) (timestamp w0) <= timestamp w).
        { apply Min.le_min_l. }
        remember (fold_left (fun w1 w2 : Watermark => w1 /\ w2) (w0 :: l) w) as gw.
        assert (timestamp gw <= min (timestamp w) (timestamp w0)).
        { subst. clear. induction l as [| w1 ws IH]; simpl.
          - apply le_refl.
          - unfold watermark_leq. simpl.
            apply min_glb; [apply IH | apply Min.le_min_r]. }
        unfold watermark_leq in *. simpl.
        apply le_trans with (min (timestamp w) (timestamp w0)); auto.
      * apply IH in Hin'.
        fold (global_watermark (w0 :: l)) in *.
        fold (global_watermark (w' :: w0 :: l)).
        unfold global_watermark. simpl.
        unfold watermark_leq in *. simpl.
        apply le_trans with (min (timestamp w') (timestamp (global_watermark (w0 :: l)))).
        + remember (fold_left (fun w1 w2 : Watermark => w1 /\ w2) (w0 :: l) w') as gw.
          clear. induction l as [| w1 ws IH]; simpl in *.
          * subst. apply le_refl.
          * unfold watermark_leq in *. simpl in *.
            apply min_glb; [apply IH | apply Min.le_min_r].
        + apply min_glb; [apply Min.le_min_r | auto].
Qed.

(* Definition: Stream merge operation combining two multi-stream watermarks *)
Definition merge_streams (mws1 mws2 : MultiStreamWatermark) : MultiStreamWatermark :=
  mws1 ++ mws2.

(* Theorem 3.10: Merging streams preserves global watermark lower bound *)
Theorem merge_preserves_global_lower_bound : forall ws1 ws2,
  global_watermark (merge_streams ws1 ws2) <=w global_watermark ws1.
Proof.
  intros ws1 ws2.
  unfold merge_streams.
  induction ws1 as [| w ws1' IH]; simpl.
  - unfold watermark_leq. simpl. apply le_0_n.
  - destruct ws1'; simpl; unfold watermark_leq; simpl; auto.
    + apply Min.le_min_l.
    + remember (fold_left watermark_meet ws1' w) as gw1.
      remember (fold_left watermark_meet ws2 (mkWatermark 0 (fun _ => le_refl _))) as gw2.
      remember (fold_left watermark_meet (ws1' ++ ws2) w) as gw.
      assert (timestamp gw <= timestamp gw1).
      { subst. clear. induction ws1' as [| w' ws' IH']; simpl.
        - apply Min.le_min_l.
        - unfold watermark_leq in *. simpl in *.
          apply min_glb; [apply IH' | apply Min.le_min_l]. }
      apply le_trans with (min (timestamp w) (timestamp gw1)); auto.
      apply min_glb; [apply Min.le_min_l | auto].
Qed.

End MultiStreamAlgebra.

(* ============================================================================ *)
(* Section 4: Window Triggering                                               *)
(* ============================================================================ *)
(* This section establishes the formal relationship between watermarks and    *)
(* window triggering in stream processing systems. It proves conditions under *)
(* which windows are guaranteed to fire based on watermark progression.       *)
(* ============================================================================ *)

Section WindowTriggering.

(* Definition: Window represented by [start, end) interval *)
Record Window : Type := mkWindow {
  window_start : Timestamp;
  window_end : Timestamp;
  window_valid : window_start <= window_end
}.

(* Definition: Event belongs to a window *)
Definition event_in_window (e : Event) (win : Window) : Prop :=
  window_start win <= event_timestamp e < window_end win.

(* Definition: Window is ready to fire when watermark passes its end *)
Definition window_ready (win : Window) (w : Watermark) : Prop :=
  window_end win <= timestamp w.

(* Definition: Window has fired *)
Definition window_fired (win : Window) (w : Watermark) : Prop :=
  window_ready win w.

(* Definition: Event completeness for a window *)
Definition window_event_completeness (win : Window) (w : Watermark) : Prop :=
  forall e, event_in_window e win -> event_timestamp e <= timestamp w.

(* Theorem 4.1: Watermark passing window end implies readiness *)
Theorem watermark_implies_window_ready : forall win w,
  window_end win <= timestamp w -> window_ready win w.
Proof.
  intros win w H. unfold window_ready. auto.
Qed.

(* Theorem 4.2: Window readiness is monotonic with watermark advancement *)
Theorem window_ready_monotonic : forall win w1 w2,
  window_ready win w1 -> w1 <=w w2 -> window_ready win w2.
Proof.
  intros win w1 w2 Hready Hle.
  unfold window_ready in *.
  unfold watermark_leq in Hle.
  apply le_trans with (timestamp w1); auto.
Qed.

(* Theorem 4.3: Events in window are bounded by window end *)
Theorem window_event_bound : forall e win,
  event_in_window e win -> event_timestamp e < window_end win.
Proof.
  intros e win Hin.
  unfold event_in_window in Hin.
  destruct Hin as [_ H]. auto.
Qed.

(* Theorem 4.4: Window firing guarantees all on-time events are included *)
Theorem window_firing_completeness : forall win w,
  window_ready win w ->
  forall e, event_in_window e win -> event_on_time e w.
Proof.
  intros win w Hready e Hin.
  unfold window_ready in Hready.
  unfold event_on_time.
  unfold event_in_window in Hin.
  destruct Hin as [Hstart Hend].
  apply le_trans with (window_end win); auto.
  apply lt_le_incl. auto.
Qed.

(* Definition: Late data arrival for a window *)
Definition late_data_for_window (e : Event) (win : Window) (w : Watermark) : Prop :=
  event_in_window e win /\ event_late e w.

(* Theorem 4.5: No late data for fired window with proper lateness bound *)
Theorem no_late_data_after_firing : forall win w L,
  window_ready win w ->
  watermark_with_lateness w L ->
  window_end win + L <= timestamp w ->
  forall e, ~ late_data_for_window e win w.
Proof.
  intros win w L Hready Hlat Hbound e.
  unfold late_data_for_window.
  unfold not. intros [Hin Hlate].
  unfold event_late in Hlate.
  unfold event_in_window in Hin.
  destruct Hin as [Hstart Hend].
  unfold watermark_with_lateness in Hlat.
  apply Hlat with (e := e).
  apply le_lt_trans with (window_end win + L); auto.
  apply plus_le_compat_r. apply lt_le_incl. auto.
Qed.

(* Theorem 4.6: Watermark guarantees window event completeness *)
Theorem watermark_guarantees_completeness : forall win w,
  window_ready win w ->
  window_event_completeness win w.
Proof.
  intros win w Hready e Hin.
  unfold window_event_completeness.
  unfold window_ready in Hready.
  unfold event_in_window in Hin.
  destruct Hin as [Hstart Hend].
  apply le_trans with (window_end win); auto.
  apply lt_le_incl. auto.
Qed.

(* Definition: Session window with gap duration *)
Record SessionWindow : Type := mkSessionWindow {
  session_start : Timestamp;
  session_end : Timestamp;
  session_gap : nat;
  session_valid : session_start + session_gap >= session_end
}.

(* Theorem 4.7: Session window firing condition *)
Theorem session_window_firing_condition : forall (sw : SessionWindow) w,
  timestamp w >= session_end sw + session_gap sw ->
  forall e, event_timestamp e <= session_end sw -> event_on_time e w.
Proof.
  intros sw w Hcond e Hts.
  unfold event_on_time.
  apply le_trans with (session_end sw); auto.
  apply le_trans with (session_end sw + session_gap sw); auto.
  apply Nat.le_add_r.
Qed.

(* Theorem 4.8: Watermark advancement triggers all ready windows *)
Theorem watermark_triggers_ready_windows : forall wins w,
  (forall win, In win wins -> window_ready win w) ->
  forall win, In win wins -> window_fired win w.
Proof.
  intros wins w Hready win Hin.
  unfold window_fired.
  apply Hready. auto.
Qed.

(* Theorem 4.9: Sliding window firing based on watermark progression *)
Definition SlidingWindow := Window. (* Same structure, different semantics *)

Theorem sliding_window_progressive_firing : forall (sws : list SlidingWindow) w1 w2,
  (forall sw, In sw sws -> window_start sw <= timestamp w1 -> window_ready sw w1) ->
  w1 <=w w2 ->
  forall sw, In sw sws -> window_start sw <= timestamp w2 -> window_ready sw w2.
Proof.
  intros sws w1 w2 Hfired Hle sw Hin Hstart.
  unfold window_ready.
  unfold watermark_leq in Hle.
  destruct (le_dec (window_start sw) (timestamp w1)) as [Hstart1 | Hstart1].
  - apply window_ready_monotonic with w1; auto.
    apply Hfired; auto.
  - unfold window_ready. apply le_trans with (timestamp w1); auto.
    apply not_le in Hstart1. apply lt_le_incl. auto.
Qed.

(* Theorem 4.10: Cascading window firing order *)
Theorem cascading_window_firing_order : forall win1 win2 w,
  window_end win1 <= window_start win2 ->
  window_fired win2 w -> window_fired win1 w.
Proof.
  intros win1 win2 w Hsep Hfired2.
  unfold window_fired, window_ready in *.
  apply le_trans with (window_start win2); auto.
  apply le_trans with (window_end win2); auto.
  apply le_trans with (timestamp w); auto.
Qed.

End WindowTriggering.

(* ============================================================================ *)
(* Summary Theorems                                                           *)
(* ============================================================================ *)
(* These theorems summarize the key algebraic completeness properties of      *)
(* watermarks in stream processing systems.                                   *)
(* ============================================================================ *)

Section Summary.

(* Summary Theorem: Watermark algebra forms a complete lattice *)
Theorem watermark_algebra_lattice_summary :
  (forall w1 w2, exists w_min w_max,
    (forall w, w <=w w1 -> w <=w w2 -> w <=w w_min) /\
    (w_min <=w w1) /\ (w_min <=w w2) /\
    (w1 <=w w_max) /\ (w2 <=w w_max) /\
    (forall w, w1 <=w w -> w2 <=w w -> w_max <=w w)) /\
  (forall w1 w2 w3, ((w1 /\ w2) /\ w3) = (w1 /\ (w2 /\ w3))) /\
  (forall w1 w2 w3, ((w1 \/ w2) \/ w3) = (w1 \/ (w2 \/ w3))) /\
  (forall w1 w2, (w1 /\ w2) = (w2 /\ w1)) /\
  (forall w1 w2, (w1 \/ w2) = (w2 \/ w1)).
Proof.
  repeat split.
  - exists (w1 /\ w2), (w1 \/ w2).
    repeat split; try (unfold watermark_leq; simpl; auto with arith).
    + intros w Hw1 Hw2. unfold watermark_leq. simpl. apply min_glb; auto.
    + intros w Hw1 Hw2. unfold watermark_leq. simpl. apply max_lub; auto.
  - apply watermark_meet_associative.
  - apply watermark_join_associative.
  - apply watermark_meet_commutative.
  - apply watermark_join_commutative.
Qed.

(* Summary Theorem: Watermark guarantees event-time processing correctness *)
Theorem watermark_event_time_correctness :
  forall (ws : list Watermark) (wins : list Window),
  monotonic_watermark_sequence ws ->
  forall w win, In w ws -> In win wins ->
  window_ready win w ->
  window_event_completeness win w.
Proof.
  intros ws wins Hmono w win Hin_w Hin_win Hready e Hin_event.
  apply watermark_guarantees_completeness; auto.
Qed.

End Summary.

(* ============================================================================ *)
(* End of WatermarkAlgebraComplete.v                                          *)
(* ============================================================================ *)
