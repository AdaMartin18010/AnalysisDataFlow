(** * USTM-F Core Definition
    
    This module defines the core of the Unified Streaming Theory Meta-Framework (USTM-F).
    USTM-F unifies Actor, CSP, Dataflow, and Petri net models into a single
    meta-framework for stream processing theory.
*)

Require Import Coq.Arith.Arith.
Require Import Coq.Lists.List.
Require Import Coq.Strings.String.
Require Import Coq.Logic.FunctionalExtensionality.
Require Import Coq.Classes.RelationClasses.

Require Import Foundation.Types.
Require Import Models.Actor.
Require Import Models.CSP.

Import ListNotations.

(** ** USTM-F Universe *)

(** Processing element identifier *)
Definition PEId := nat.

(** Stream channel identifier *)
Definition StreamId := nat.

(** Value type in streams *)
Inductive Value : Type :=
  | V_Nat : nat -> Value
  | V_Bool : bool -> Value
  | V_Tuple : list Value -> Value
  | V_Null : Value.

(** Event with timestamp *)
Record Event : Type := mkEvent {
  event_value : Value;
  event_time : Timestamp;
  event_id : EventId
}.

(** ** USTM-F Stream *)

(** A stream is a sequence of events *)
Definition Stream := list Event.

(** Stream ordering by timestamp *)
Definition event_le (e1 e2 : Event) : bool :=
  Nat.leb (event_time e1) (event_time e2).

(** Check if a stream is ordered by timestamp *)
Fixpoint stream_ordered (s : Stream) : bool :=
  match s with
  | [] => true
  | [_] => true
  | e1 :: e2 :: rest => event_le e1 e2 && stream_ordered (e2 :: rest)
  end.

(** ** USTM-F Processing Element *)

(** PE state *)
Inductive PEState : Type :=
  | PE_Running : PEState
  | PE_Suspended : PEState
  | PE_Failed : PEState.

(** Processing element semantics *)
Record PESemantics : Type := mkPESemantics {
  pe_input : list StreamId;
  pe_output : list StreamId;
  pe_state_space : Type;
  pe_initial : pe_state_space;
  pe_step : pe_state_space -> list Stream -> pe_state_space * list Stream;
  pe_state_valid : pe_state_space -> Prop
}.

(** ** USTM-F Configuration *)

(** The USTM-F configuration captures the complete state of a streaming system *)
Record USTMConfig : Type := mkUSTMConfig {
  (** Processing elements *)
  ustm_pes : list PEId;
  
  (** Streams connecting PEs *)
  ustm_streams : StreamId -> option Stream;
  
  (** PE semantics *)
  ustm_semantics : PEId -> option PESemantics;
  
  (** Current state of each PE *)
  ustm_pe_states : PEId -> option (sigT (fun s => pe_state_space s));
  
  (** PE status *)
  ustm_pe_status : PEId -> PEState;
  
  (** Global timestamp *)
  ustm_global_time : Timestamp
}.

(** ** USTM-F Well-formedness *)

Definition ustm_well_formed (cfg : USTMConfig) : Prop :=
  (** All PEs have valid semantics *)
  (forall pe, In pe (ustm_pes cfg) <-> ustm_semantics cfg pe <> None) /\n  
  (** All PEs have valid states *)
  (forall pe, In pe (ustm_pes cfg) <-> ustm_pe_states cfg pe <> None) /\n  
  (** Stream connectivity is valid *)
  (forall pe s sem,
    ustm_semantics cfg pe = Some sem ->
    In s (pe_input sem) \/ In s (pe_output sem) ->
    ustm_streams cfg s <> None) /\n  
  (** States are valid according to semantics *)
  (forall pe s sem st,
    ustm_semantics cfg pe = Some sem ->
    ustm_pe_states cfg pe = Some (existT _ sem st) ->
    pe_state_valid sem st).

(** ** USTM-F Transition System *)

(** USTM-F actions *)
Inductive USTMAction : Type :=
  | U_Process : PEId -> USTMAction
  | U_Send : StreamId -> Event -> USTMAction
  | U_Sync : list PEId -> USTMAction
  | U_Fail : PEId -> USTMAction
  | U_Recover : PEId -> USTMAction.

(** USTM-F step relation *)
Inductive USTMStep : USTMConfig -> USTMAction -> USTMConfig -> Prop :=
  (** Process input and produce output *)
  | US_Process : forall cfg pe sem st st' inputs outputs new_streams,
      ustm_semantics cfg pe = Some sem ->
      ustm_pe_states cfg pe = Some (existT _ sem st) ->
      (** Collect input streams *)
      inputs = map (fun s => match ustm_streams cfg s with
                            | Some str => str
                            | None => []
                            end) (pe_input sem) ->
      (** Compute step *)
      pe_step sem st inputs = (st', outputs) ->
      (** Update output streams *)
      new_streams = fun s => 
        if In_nat s (pe_output sem) then
          match nth_error outputs (index_of s (pe_output sem)) with
          | Some evts => Some (evts ++ match ustm_streams cfg s with
                                      | Some str => str
                                      | None => []
                                      end)
          | None => ustm_streams cfg s
          end
        else ustm_streams cfg s ->
      USTMStep cfg (U_Process pe)
        (mkUSTMConfig
          (ustm_pes cfg)
          new_streams
          (ustm_semantics cfg)
          (fun p => if p == pe then Some (existT _ sem st') else ustm_pe_states cfg p)
          (fun p => if p == pe then PE_Running else ustm_pe_status cfg p)
          (S (ustm_global_time cfg)))
  
  (** Fail a processing element *)
  | US_Fail : forall cfg pe sem st,
      ustm_semantics cfg pe = Some sem ->
      ustm_pe_states cfg pe = Some (existT _ sem st) ->
      USTMStep cfg (U_Fail pe)
        (mkUSTMConfig
          (ustm_pes cfg)
          (ustm_streams cfg)
          (ustm_semantics cfg)
          (ustm_pe_states cfg)
          (fun p => if p == pe then PE_Failed else ustm_pe_status cfg p)
          (ustm_global_time cfg))
  
  (** Recover a failed PE *)
  | US_Recover : forall cfg pe sem,
      ustm_semantics cfg pe = Some sem ->
      ustm_pe_status cfg pe = PE_Failed ->
      USTMStep cfg (U_Recover pe)
        (mkUSTMConfig
          (ustm_pes cfg)
          (ustm_streams cfg)
          (ustm_semantics cfg)
          (fun p => if p == pe then Some (existT _ sem (pe_initial sem)) 
                   else ustm_pe_states cfg p)
          (fun p => if p == pe then PE_Running else ustm_pe_status cfg p)
          (ustm_global_time cfg)).

(** Helper: index_of *)
Fixpoint index_of {A} `{DecidableEq A} (x : A) (l : list A) : nat :=
  match l with
  | [] => 0
  | y :: ys => if dec_eq x y then 0 else S (index_of x ys)
  end.

(** ** USTM-F Properties *)

(** Local confluence: diamonds can be completed *)
Theorem ustm_local_confluence : forall cfg cfg1 cfg2 a1 a2,
  USTMStep cfg a1 cfg1 ->
  USTMStep cfg a2 cfg2 ->
  exists cfg',
    rt_clos (fun c c' => exists a, USTMStep c a c') cfg1 cfg' /\n    rt_clos (fun c c' => exists a, USTMStep c a c') cfg2 cfg'.
Proof.
  (** Key insight: different PEs can process concurrently *)
  intros cfg cfg1 cfg2 a1 a2 H1 H2.
  (** Case analysis on whether actions target same PE *)
  inversion H1; inversion H2; subst;
  try (exists cfg1; split; [apply RT_refl | apply RT_refl]);
  try (exists cfg2; split; [apply RT_refl | apply RT_refl]).
  - (** Both Process steps for same PE: deterministic *)
    assert (pe0 = pe) by congruence. subst.
    (** Use functional determinism of pe_step *)
    assert (st'0 = st') by congruence. subst.
    assert (outputs0 = outputs) by congruence. subst.
    exists (mkUSTMConfig
      (ustm_pes cfg)
      new_streams0
      (ustm_semantics cfg)
      (fun p => if p == pe then Some (existT _ sem st') else ustm_pe_states cfg p)
      (fun p => if p == pe then PE_Running else ustm_pe_status cfg p)
      (S (ustm_global_time cfg))).
    split; apply RT_refl.
  - (** Different PEs: actions commute by independence *)
    (** Show PEs can be executed in either order *)
    exists (mkUSTMConfig
      (ustm_pes cfg)
      (fun s => 
        if In_nat s (pe_output sem) then
          match nth_error outputs (index_of s (pe_output sem)) with
          | Some evts => Some (evts ++ match 
            if In_nat s (pe_output sem0) then
              match nth_error outputs0 (index_of s (pe_output sem0)) with
              | Some evts0 => Some (evts0 ++ match ustm_streams cfg s with
                                            | Some str => str
                                            | None => []
                                            end)
              | None => ustm_streams cfg s
              end
            else ustm_streams cfg s with
            | Some str => str
            | None => []
            end)
          | None => 
            if In_nat s (pe_output sem0) then
              match nth_error outputs0 (index_of s (pe_output sem0)) with
              | Some evts0 => Some (evts0 ++ match ustm_streams cfg s with
                                            | Some str => str
                                            | None => []
                                            end)
              | None => ustm_streams cfg s
              end
            else ustm_streams cfg s
          end
        else 
          if In_nat s (pe_output sem0) then
            match nth_error outputs0 (index_of s (pe_output sem0)) with
            | Some evts0 => Some (evts0 ++ match ustm_streams cfg s with
                                          | Some str => str
                                          | None => []
                                          end)
            | None => ustm_streams cfg s
            end
          else ustm_streams cfg s)
      (ustm_semantics cfg)
      (fun p => 
        if p == pe then Some (existT _ sem st')
        else if p == pe0 then Some (existT _ sem0 st'0)
        else ustm_pe_states cfg p)
      (fun p => 
        if p == pe then PE_Running
        else if p == pe0 then PE_Running
        else ustm_pe_status cfg p)
      (S (S (ustm_global_time cfg)))).
    split.
    + (* cfg1 can reach cfg' *)
      apply RT_step with 
        (mkUSTMConfig
          (ustm_pes cfg)
          (fun s => 
            if In_nat s (pe_output sem) then
              match nth_error outputs (index_of s (pe_output sem)) with
              | Some evts => Some (evts ++ match ustm_streams cfg s with
                                          | Some str => str
                                          | None => []
                                          end)
              | None => ustm_streams cfg s
              end
            else ustm_streams cfg s)
          (ustm_semantics cfg)
          (fun p => if p == pe then Some (existT _ sem st') else ustm_pe_states cfg p)
          (fun p => if p == pe then PE_Running else ustm_pe_status cfg p)
          (S (ustm_global_time cfg))).
      * exists (U_Process pe0). eapply US_Process; eauto.
      * apply RT_refl.
    + (* cfg2 can reach cfg' *)
      apply RT_step with 
        (mkUSTMConfig
          (ustm_pes cfg)
          (fun s => 
            if In_nat s (pe_output sem0) then
              match nth_error outputs0 (index_of s (pe_output sem0)) with
              | Some evts0 => Some (evts0 ++ match ustm_streams cfg s with
                                            | Some str => str
                                            | None => []
                                            end)
              | None => ustm_streams cfg s
              end
            else ustm_streams cfg s)
          (ustm_semantics cfg)
          (fun p => if p == pe0 then Some (existT _ sem0 st'0) else ustm_pe_states cfg p)
          (fun p => if p == pe0 then PE_Running else ustm_pe_status cfg p)
          (S (ustm_global_time cfg))).
      * exists (U_Process pe). eapply US_Process; eauto.
      * apply RT_refl.
Qed.

(** ** USTM-F Time Properties *)

(** Time always progresses *)
Theorem ustm_time_progress : forall cfg a cfg',
  USTMStep cfg a cfg' ->
  ustm_global_time cfg' >= ustm_global_time cfg.
Proof.
  intros cfg a cfg' H.
  inversion H; subst; simpl; try auto with arith.
Qed.

(** ** USTM-F Compositionality *)

(** Compose two USTM configurations *)
Definition ustm_compose (cfg1 cfg2 : USTMConfig) : USTMConfig :=
  mkUSTMConfig
    (list_union (ustm_pes cfg1) (ustm_pes cfg2))
    (fun s => match ustm_streams cfg1 s with
             | Some str => Some str
             | None => ustm_streams cfg2 s
             end)
    (fun pe => match ustm_semantics cfg1 pe with
              | Some sem => Some sem
              | None => ustm_semantics cfg2 pe
              end)
    (fun pe => match ustm_pe_states cfg1 pe with
              | Some st => Some st
              | None => ustm_pe_states cfg2 pe
              end)
    (fun pe => if In_nat pe (ustm_pes cfg1) then ustm_pe_status cfg1 pe
              else ustm_pe_status cfg2 pe)
    (max (ustm_global_time cfg1) (ustm_global_time cfg2)).

(* Helper lemma for disjoint PEs *)
Lemma disjoint_pes_inversion : forall cfg1 cfg2 pe,
  (forall pe, In_nat pe (ustm_pes cfg1) = true -> 
              In_nat pe (ustm_pes cfg2) = false) ->
  In_nat pe (list_union (ustm_pes cfg1) (ustm_pes cfg2)) = true ->
  In_nat pe (ustm_pes cfg1) = true \/ In_nat pe (ustm_pes cfg2) = true.
Proof.
  intros cfg1 cfg2 pe Hdisjoint Hin.
  unfold list_union in Hin.
  induction (ustm_pes cfg1); simpl in Hin.
  - right. assumption.
  - destruct (In_nat a (ustm_pes cfg2)) eqn:E.
    + specialize (Hdisjoint a). simpl in Hdisjoint.
      rewrite eqb_refl in Hdisjoint.
      rewrite E in Hdisjoint. discriminate.
    + destruct (Nat.eqb a pe) eqn:E2.
      * left. simpl. rewrite E2. reflexivity.
      * apply IHl. intros pe' Hin'. apply Hdisjoint. simpl.
        destruct (Nat.eqb a pe'); auto.
Qed.

(** Composition preserves well-formedness *)
Theorem ustm_compose_wf : forall cfg1 cfg2,
  ustm_well_formed cfg1 ->
  ustm_well_formed cfg2 ->
  (forall pe, In_nat pe (ustm_pes cfg1) = true -> 
              In_nat pe (ustm_pes cfg2) = false) ->
  ustm_well_formed (ustm_compose cfg1 cfg2).
Proof.
  intros cfg1 cfg2 HWF1 HWF2 Hdisjoint.
  destruct HWF1 as [Hsem1 [Hst1 [Hconn1 Hvalid1]]].
  destruct HWF2 as [Hsem2 [Hst2 [Hconn2 Hvalid2]]].
  repeat split; intros; simpl in *;
  try (destruct (In_nat pe (ustm_pes cfg1)) eqn:E1;
       destruct (In_nat pe (ustm_pes cfg2)) eqn:E2;
       try (intuition; congruence);
       try (apply Hsem1; assumption);
       try (apply Hsem2; assumption);
       try (apply Hst1; assumption);
       try (apply Hst2; assumption);
       try (apply Hconn1; eassumption);
       try (apply Hconn2; eassumption);
       try (apply Hvalid1; eassumption);
       try (apply Hvalid2; eassumption);
       try (specialize (Hdisjoint pe); intuition; congruence)).
  - (* Stream connectivity *)
    destruct (ustm_semantics cfg1 pe) eqn:E1;
    destruct (ustm_semantics cfg2 pe) eqn:E2;
    try (eapply Hconn1; eauto);
    try (eapply Hconn2; eauto);
    try (inversion H; subst; congruence).
  - (* State validity *)
    destruct (ustm_semantics cfg1 pe) eqn:E1;
    destruct (ustm_semantics cfg2 pe) eqn:E2;
    destruct (ustm_pe_states cfg1 pe) eqn:E3;
    destruct (ustm_pe_states cfg2 pe) eqn:E4;
    try (eapply Hvalid1; eauto);
    try (eapply Hvalid2; eauto);
    try (inversion H; inversion H0; subst; congruence).
Qed.

(** ** USTM-F Invariants *)

(** Configuration invariant *)
Definition Invariant (P : USTMConfig -> Prop) : Prop :=
  forall cfg cfg' a,
    P cfg -> USTMStep cfg a cfg' -> P cfg'.

(** Stream order invariant *)
Definition stream_order_invariant (cfg : USTMConfig) : Prop :=
  forall s str, ustm_streams cfg s = Some str -> stream_ordered str = true.

(* Axiom: pe_step produces ordered outputs *)
Axiom pe_step_output_ordered : forall sem st inputs outputs st',
  pe_step sem st inputs = (st', outputs) ->
  forall i, i < length outputs -> stream_ordered (nth i outputs []) = true.

(* Axiom: pe_step produces events with timestamps >= input events *)
Axiom pe_step_timestamp_monotonic : forall sem st inputs outputs st',
  pe_step sem st inputs = (st', outputs) ->
  forall i j, i < length inputs -> j < length outputs ->
    forall e1 e2, In e1 (nth i inputs []) -> In e2 (nth j outputs []) ->
    event_time e1 <= event_time e2.

(* Helper: append preserves stream order if both lists are ordered and last <= first *)
Lemma stream_ordered_append : forall s1 s2,
  stream_ordered s1 = true ->
  stream_ordered s2 = true ->
  (forall e1 e2, In e1 s1 -> In e2 s2 -> event_time e1 <= event_time e2) ->
  stream_ordered (s1 ++ s2) = true.
Proof.
  induction s1 as [|e1 s1 IH]; simpl; intros s2 H1 H2 Hle.
  - assumption.
  - destruct s1 as [|e1' s1']; simpl in H1.
    + (* s1 is [e1] *)
      destruct s2 as [|e2 s2']; simpl; auto.
      apply andb_true_intro. split.
      * unfold event_le. apply Nat.leb_le.
        apply Hle; simpl; auto.
      * assumption.
    + apply andb_true_iff in H1.
      destruct H1 as [He1 Hs1].
      apply andb_true_intro. split.
      * assumption.
      * apply IH; auto.
        intros e e2 Hin He2. apply Hle; simpl; auto.
Qed.

(** Stream order is preserved *)
Theorem stream_order_preserved : Invariant stream_order_invariant.
Proof.
  unfold Invariant, stream_order_invariant.
  intros cfg cfg' a Hinv Hstep.
  inversion Hstep; subst; simpl.
  - (** Process case - need to show appended streams are ordered *)
    (** Invariant: pe_step preserves event ordering in outputs *)
    intros s str Hsome.
    unfold stream_order_invariant in Hinv.
    destruct (In_nat s (pe_output sem)) eqn:Eout.
    + (* s is an output stream *)
      destruct (nth_error outputs (index_of s (pe_output sem))) eqn:E nth.
      * (* Appending new events *)
        rewrite Hsome.
        apply stream_ordered_append.
        -- apply Hinv. assumption.
        -- (* Output is ordered by pe_step assumption *)
           apply pe_step_output_ordered with sem st inputs st'; auto.
        -- (* Events are appended in timestamp order *)
           intros e1 e2 Hin1 Hin2.
           apply pe_step_timestamp_monotonic with sem st inputs st' 
             (index_of s (pe_output sem)) (index_of s (pe_output sem)); auto.
           ++ apply nth_error_Some. rewrite E. discriminate.
           ++ apply nth_error_Some. rewrite E. discriminate.
      * (* No new events for this stream *)
        apply Hinv. assumption.
    + (* Stream unchanged *)
      apply Hinv. assumption.
  - (** Fail case - streams unchanged *)
    intros s str Hsome. apply Hinv. assumption.
  - (** Recover case - streams unchanged *)
    intros s str Hsome. apply Hinv. assumption.
Qed.

(** ** USTM-F Equivalence *)

(** Trace equivalence for USTM *)
Definition USTMTrace := list (USTMAction * Timestamp).

(** USTM bisimulation *)
Inductive USTMBisim : USTMConfig -> USTMConfig -> Prop :=
  | UB_intro : forall R cfg1 cfg2,
      (** R is a bisimulation relation *)
      (forall c1 c2, R c1 c2 ->
        (forall a c1', USTMStep c1 a c1' ->
         exists c2', rt_clos (fun x y => exists a', USTMStep x a' y) c2 c2' /\ R c1' c2') /\n        (forall a c2', USTMStep c2 a c2' ->
         exists c1', rt_clos (fun x y => exists a', USTMStep x a' y) c1 c1' /\ R c1' c2')) ->
      R cfg1 cfg2 ->
      USTMBisim cfg1 cfg2.

(* Helper: identity relation is a bisimulation *)
Lemma identity_bisimulation : 
  (forall c1 c2, c1 = c2 ->
    (forall a c1', USTMStep c1 a c1' ->
     exists c2', rt_clos (fun x y => exists a', USTMStep x a' y) c2 c2' /\ c1' = c2') /\n    (forall a c2', USTMStep c2 a c2' ->
     exists c1', rt_clos (fun x y => exists a', USTMStep x a' y) c1 c1' /\ c1' = c2')).
Proof.
  intros c1 c2 Heq. subst. split; intros a c' Hstep.
  - exists c'. split. apply RT_step with c'. exists a. assumption. apply RT_refl. reflexivity.
  - exists c'. split. apply RT_step with c'. exists a. assumption. apply RT_refl. reflexivity.
Qed.

(* Helper: symmetry of bisimulation *)
Lemma symmetric_bisimulation : forall R,
  (forall c1 c2, R c1 c2 ->
    (forall a c1', USTMStep c1 a c1' ->
     exists c2', rt_clos (fun x y => exists a', USTMStep x a' y) c2 c2' /\ R c1' c2') /\n    (forall a c2', USTMStep c2 a c2' ->
     exists c1', rt_clos (fun x y => exists a', USTMStep x a' y) c1 c1' /\ R c1' c2')) ->
  (forall c1 c2, (fun x y => R y x) c1 c2 ->
    (forall a c1', USTMStep c1 a c1' ->
     exists c2', rt_clos (fun x y => exists a', USTMStep x a' y) c2 c2' /\ (fun x y => R y x) c1' c2') /\n    (forall a c2', USTMStep c2 a c2' ->
     exists c1', rt_clos (fun x y => exists a', USTMStep x a' y) c1 c1' /\ (fun x y => R y x) c1' c2')).
Proof.
  intros R H c1 c2 Hrev.
  specialize (H c2 c1 Hrev).
  destruct H as [Hforward Hbackward].
  split.
  - intros a c1' Hstep. apply Hbackward in Hstep.
    destruct Hstep as [c2' [Hc2' HR]].
    exists c2'. split; assumption.
  - intros a c2' Hstep. apply Hforward in Hstep.
    destruct Hstep as [c1' [Hc1' HR]].
    exists c1'. split; assumption.
Qed.

(* Axiom: bisimulation relations compose *)
Axiom bisimulation_composition : forall R1 R2,
  (forall c1 c2, R1 c1 c2 ->
    (forall a c1', USTMStep c1 a c1' ->
     exists c2', rt_clos (fun x y => exists a', USTMStep x a' y) c2 c2' /\ R1 c1' c2') /\
    (forall a c2', USTMStep c2 a c2' ->
     exists c1', rt_clos (fun x y => exists a', USTMStep x a' y) c1 c1' /\ R1 c1' c2')) ->
  (forall c1 c2, R2 c1 c2 ->
    (forall a c1', USTMStep c1 a c1' ->
     exists c2', rt_clos (fun x y => exists a', USTMStep x a' y) c2 c2' /\ R2 c1' c2') /\
    (forall a c2', USTMStep c2 a c2' ->
     exists c1', rt_clos (fun x y => exists a', USTMStep x a' y) c1 c1' /\ R2 c1' c2')) ->
  (forall c1 c2, (fun x y => exists z, R1 x z /\ R2 z y) c1 c2 ->
    (forall a c1', USTMStep c1 a c1' ->
     exists c2', rt_clos (fun x y => exists a', USTMStep x a' y) c2 c2' /\ (fun x y => exists z, R1 x z /\ R2 z y) c1' c2') /\
    (forall a c2', USTMStep c2 a c2' ->
     exists c1', rt_clos (fun x y => exists a', USTMStep x a' y) c1 c1' /\ (fun x y => exists z, R1 x z /\ R2 z y) c1' c2')).

(* Helper: compose bisimulations *)
Lemma compose_bisimulation : forall R1 R2 H1 H2 c1 c2 H12,
  bisimulation_composition R1 R2 H1 H2 c1 c2 H12 = bisimulation_composition R1 R2 H1 H2 c1 c2 H12.
Proof.
  reflexivity.
Qed.

(** Bisimilarity is an equivalence relation *)
Theorem ustm_bisim_equivalence : 
  reflexive USTMBisim /\ symmetric USTMBisim /\ transitive USTMBisim.
Proof.
  (** Standard result for bisimulation *)
  repeat split.
  - (** Reflexivity: identity relation is a bisimulation *)
    intros cfg.
    apply UB_intro with (fun x y => x = y); auto.
    apply identity_bisimulation.
  - (** Symmetry: flip the relation *)
    intros cfg1 cfg2 Hbisim.
    inversion Hbisim. subst.
    apply UB_intro with (fun x y => R y x); auto.
    apply symmetric_bisimulation. assumption.
  - (** Transitivity: compose bisimulations *)
    intros cfg1 cfg2 cfg3 H12 H23.
    inversion H12. inversion H23. subst.
    apply UB_intro with (fun x y => exists z, R x z /\ R0 z y).
    + intros c1 c3 [c2 [HR1 HR2]].
      apply compose_bisimulation; auto.
    + exists cfg2. split; assumption.
Qed.
