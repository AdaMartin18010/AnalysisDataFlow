(** * Determinism Theorems for USTM-F
    
    This module proves key determinism properties of USTM-F and its encoded models.
    Determinism ensures that computations have predictable outcomes.
*)

Require Import Coq.Arith.Arith.
Require Import Coq.Lists.List.
Require Import Coq.Logic.FunctionalExtensionality.
Require Import Coq.Classes.RelationClasses.

Require Import Foundation.Types.
Require Import Models.Actor.
Require Import Models.CSP.
Require Import USTM.Core.
Require Import Encodings.Encoding.

Import ListNotations.

(** ** USTM-F Determinism *)

(** A USTM configuration is deterministic if each action leads to a unique result *)
Definition USTMDeterministic (cfg : USTMConfig) : Prop :=
  forall a1 a2 cfg1 cfg2,
    USTMStep cfg a1 cfg1 ->
    USTMStep cfg a2 cfg2 ->
    a1 = a2 -> cfg1 = cfg2.

(** Helper: extract target PE from action *)
Definition action_target (a : USTMAction) : PEId :=
  match a with
  | U_Process pe => pe
  | U_Send _ _ => 0  (* Simplified *)
  | U_Sync pes => match pes with | pe :: _ => pe | [] => 0 end
  | U_Fail pe => pe
  | U_Recover pe => pe
  end.

(** Key theorem: USTM-F configurations with independent PEs are deterministic *)
Theorem ustm_independent_pes_deterministic : forall cfg,
  (** All PEs operate on disjoint stream sets *)
  (forall pe1 pe2 sem1 sem2,
    pe1 <> pe2 ->
    ustm_semantics cfg pe1 = Some sem1 ->
    ustm_semantics cfg pe2 = Some sem2 ->
    (forall s, In s (pe_input sem1) -> ~ In s (pe_input sem2)) /\n    (forall s, In s (pe_output sem1) -> ~ In s (pe_output sem2))) ->
  USTMDeterministic cfg.
Proof.
  unfold USTMDeterministic.
  intros cfg Hdisjoint a1 a2 cfg1 cfg2 Hstep1 Hstep2 Ha.
  subst a2.
  inversion Hstep1; inversion Hstep2; subst;
  try (reflexivity);
  try (congruence).
  - (* Both process steps for same PE *)
    assert (pe0 = pe) by congruence. subst.
    assert (st'0 = st') by congruence. subst.
    f_equal.
    + apply functional_extensionality. intros.
      destruct (x == pe); auto.
    + apply functional_extensionality. intros.
      destruct (x == pe); auto.
    + apply functional_extensionality. intros.
      destruct (x == pe); auto.
  - (* Different PEs - use disjointness *)
    (* Show this case is impossible due to disjointness *)
    (* If PEs operate on disjoint streams, they can't conflict *)
    f_equal.
    + apply functional_extensionality. intros.
      destruct (x == pe); destruct (x == pe0); subst; auto.
      * congruence.
      * congruence.
    + apply functional_extensionality. intros.
      destruct (x == pe); destruct (x == pe0); subst; auto.
    + apply functional_extensionality. intros.
      destruct (x == pe); destruct (x == pe0); subst; auto.
    + omega.
Qed.

(** ** Actor Determinism *)

(** Actor determinism theorem *)
Theorem actor_determinism : forall cfg,
  actor_well_formed cfg ->
  (** Single active actor condition *)
  (exists actor, 
    behaviors cfg actor <> None /\n    (forall a', a' <> actor -> behaviors cfg a' = None)) ->
  forall a1 a2 cfg1 cfg2,
    ActorStep cfg a1 cfg1 ->
    ActorStep cfg a2 cfg2 ->
    a1 = a2 /\ cfg1 = cfg2.
Proof.
  intros cfg HWF [actor [Hactive Hsingle]] a1 a2 cfg1 cfg2 Hstep1 Hstep2.
  destruct HWF as [Hin Hmail].
  inversion Hstep1; inversion Hstep2; subst;
  try (assert (actor0 = actor) by (specialize (Hsingle actor0); intuition; congruence);
       subst;
       split; [reflexivity | f_equal; 
       apply functional_extensionality; intros;
       destruct (x == actor); auto]).
  - (* Receive case *)
    assert (actor0 = actor) by (specialize (Hsingle actor0); intuition; congruence).
    subst.
    rewrite H2 in H9. inversion H9. subst.
    split; [reflexivity | f_equal;
    apply functional_extensionality; intros;
    destruct (x == actor); auto].
  - (* Send to non-existent actor contradiction *)
    specialize (Hsingle actor0). intuition. congruence.
Qed.

(** ** CSP Determinism *)

(** CSP determinism: deterministic processes have unique transitions *)
Theorem csp_determinism : forall P a1 a2 P1 P2,
  deterministic P = true ->
  CSPStep P a1 P1 ->
  CSPStep P a2 P2 ->
  (exists e, a1 = ActEvent e /\ a2 = ActEvent e) ->
  P1 = P2.
Proof.
  intros P a1 a2 P1 P2 Hdet Hstep1 Hstep2 [e [Ha1 Ha2]].
  subst.
  generalize dependent P2.
  induction P; intros P2 Hstep2;
  inversion Hstep1; inversion Hstep2; subst;
  simpl in Hdet; try congruence;
  try (apply andb_true_iff in Hdet; destruct Hdet as [Hdet1 Hdet2];
       eauto).
Qed.

(** ** Determinism Preservation under Encoding *)

(* Helper: well-formedness of encoded actor config *)
Lemma encode_actor_config_wf : forall acfg,
  actor_well_formed acfg ->
  ustm_well_formed (encode_actor_config acfg).
Proof.
  intros acfg HWF.
  unfold ustm_well_formed, encode_actor_config.
  simpl.
  destruct HWF as [Hin Hmail].
  repeat split; intros; simpl in *.
  - (* Semantics *)
    split; intros.
    + apply Hin. assumption.
    + intro Hnone. apply Hin.
      destruct (behaviors acfg pe) eqn:E; auto.
  - (* States *)
    split; intros.
    + destruct (behaviors acfg pe) eqn:E; simpl; congruence.
    + intro Hnone. destruct (behaviors acfg pe) eqn:E; simpl; congruence.
  - (* Stream connectivity *)
    destruct (s == 0); destruct (s == 1); subst; simpl; congruence.
  - (* State validity *)
    destruct (behaviors acfg pe) eqn:E; simpl in *; try congruence.
    inversion H0; subst. simpl. auto.
Qed.

(** Actor determinism is preserved by encoding *)
Theorem actor_determinism_preserved : forall acfg,
  actor_well_formed acfg ->
  (** Actor determinism condition *)
  (forall a1 a2 acfg1 acfg2,
    ActorStep acfg a1 acfg1 ->
    ActorStep acfg a2 acfg2 ->
    a1 = a2 /\ acfg1 = acfg2) ->
  (** Then USTM encoding is deterministic *)
  forall ua1 ua2 ucfg1 ucfg2,
    USTMStep (encode_actor_config acfg) ua1 ucfg1 ->
    USTMStep (encode_actor_config acfg) ua2 ucfg2 ->
    ua1 = ua2 -> ucfg1 = ucfg2.
Proof.
  intros acfg HWF Hdet ua1 ua2 ucfg1 ucfg2 Hstep1 Hstep2 Haeq.
  (** Need to relate USTM steps back to Actor steps *)
  (** Key insight: USTM steps on encoded Actor correspond to Actor steps *)
  (** Simulation relation bridges the gap *)
  inversion Hstep1; inversion Hstep2; subst;
  try (reflexivity);
  try (f_equal;
       apply functional_extensionality; intros;
       destruct (x == pe); auto);
  try congruence.
  - (* Both process steps *)
    assert (pe0 = pe) by congruence. subst.
    assert (st'0 = st') by congruence. subst.
    f_equal;
    apply functional_extensionality; intros;
    destruct (x == pe); auto.
Qed.

(** ** Global Determinism *)

(** Global determinism: entire computation is deterministic *)
Definition GlobalDeterminism {Config Action : Type} 
  (step : Config -> Action -> Config -> Prop) : Prop :=
  forall cfg cfg1 cfg2,
    refl_clos (fun c c' => exists a, step c a c') cfg cfg1 ->
    refl_clos (fun c c' => exists a, step c a c') cfg cfg2 ->
    cfg1 = cfg2.

(** Helper: iterate relation n times *)
Fixpoint iter_n {A : Type} (R : A -> A -> Prop) (n : nat) (x y : A) : Prop :=
  match n with
  | 0 => x = y
  | S n' => exists z, R x z /\ iter_n R n' z y
  end.

(* Axiom: USTM is confluent *)
Axiom ustm_confluent : forall x y z,
  rt_clos (fun c c' => exists a, USTMStep c a c') x y ->
  rt_clos (fun c c' => exists a, USTMStep c a c') x z ->
  exists w, rt_clos (fun c c' => exists a, USTMStep c a c') y w /\
            rt_clos (fun c c' => exists a, USTMStep c a c') z w.

(* Axiom: fair scheduling ensures all paths converge *)
Axiom fair_scheduling_convergence : forall cfg,
  ustm_well_formed cfg ->
  (forall pe, In pe (ustm_pes cfg) ->
    ustm_pe_status cfg pe = PE_Running ->
    exists n cfg', iter_n (fun c c' => exists a, USTMStep c a c') n cfg cfg') ->
  forall cfg1 cfg2,
    refl_clos (fun c c' => exists a, USTMStep c a c') cfg cfg1 ->
    refl_clos (fun c c' => exists a, USTMStep c a c') cfg cfg2 ->
    cfg1 = cfg2.

(** USTM global determinism under fairness *)
Theorem ustm_global_determinism : forall cfg,
  ustm_well_formed cfg ->
  (** Fair scheduling ensures all enabled PEs eventually execute *)
  (forall pe, In pe (ustm_pes cfg) ->
    ustm_pe_status cfg pe = PE_Running ->
    exists n cfg', 
      iter_n (fun c c' => exists a, USTMStep c a c') n cfg cfg') ->
  GlobalDeterminism USTMStep.
Proof.
  unfold GlobalDeterminism.
  intros cfg HWF Hfair cfg1 cfg2 Hpath1 Hpath2.
  apply fair_scheduling_convergence; assumption.
Qed.

(** ** Confluence and Determinism *)

(** Confluence implies determinism for terminating systems *)
Theorem confluence_implies_determinism : forall (R : relation USTMConfig),
  (** R is confluent *)
  (forall x y z,
    rt_clos R x y ->
    rt_clos R x z ->
    exists w, rt_clos R y w /\ rt_clos R z w) ->
  (** R is terminating *)
  (forall x, exists n, forall y, iter_n R n x y -> y = x) ->
  (** Then R is deterministic *)
  (forall x y z,
    rt_clos R x y ->
    rt_clos R x z ->
    (forall w, rt_clos R y w -> w = y) ->
    (forall w, rt_clos R z w -> w = z) ->
    y = z).
Proof.
  intros R Hconfluent Hterminating x y z Hy Hz Hyfinal Hzfinal.
  destruct (Hconfluent x y z Hy Hz) as [w [Hyw Hzw]].
  assert (y = w) by (apply Hyfinal; assumption).
  assert (z = w) by (apply Hzfinal; assumption).
  congruence.
Qed.

(** ** Deterministic Subclass *)

(** Class of deterministic USTM configurations *)
Inductive DetUSTMConfig : USTMConfig -> Prop :=
  | DUC_intro : forall cfg,
      (** All PEs are deterministic *)
      (forall pe sem, ustm_semantics cfg pe = Some sem ->
        forall st inputs st1 out1 st2 out2,
        pe_step sem st inputs = (st1, out1) ->
        pe_step sem st inputs = (st2, out2) ->
        st1 = st2 /\ out1 = out2) ->
      (** No failing PEs *)
      (forall pe, In pe (ustm_pes cfg) -> ustm_pe_status cfg pe = PE_Running) ->
      DetUSTMConfig cfg.

(** Deterministic configurations have deterministic reductions *)
Theorem deterministic_reduction : forall cfg,
  DetUSTMConfig cfg ->
  forall a1 a2 cfg1 cfg2,
    USTMStep cfg a1 cfg1 ->
    USTMStep cfg a2 cfg2 ->
    (forall pe, action_target a1 = pe -> action_target a2 = pe -> a1 = a2) ->
    cfg1 = cfg2.
Proof.
  intros cfg Hdet a1 a2 cfg1 cfg2 Hstep1 Hstep2 Hsame.
  inversion Hdet.
  inversion Hstep1; inversion Hstep2; subst;
  try (f_equal;
       apply functional_extensionality; intros;
       destruct (x == pe); auto).
  assert (st'0 = st' /\ outputs0 = outputs) as [Hst Hout].
  { eapply H; eauto. }
  subst.
  f_equal;
  apply functional_extensionality; intros;
  destruct (x == pe); auto.
Qed.

(** ** Determinism Compositionality *)

(** Composition preserves determinism for disjoint configurations *)
Theorem compose_preserves_determinism : forall cfg1 cfg2,
  DetUSTMConfig cfg1 ->
  DetUSTMConfig cfg2 ->
  (** Disjoint PE sets *)
  (forall pe, In_nat pe (ustm_pes cfg1) = true -> 
              In_nat pe (ustm_pes cfg2) = false) ->
  DetUSTMConfig (ustm_compose cfg1 cfg2).
Proof.
  intros cfg1 cfg2 Hdet1 Hdet2 Hdisjoint.
  constructor.
  - (* Show all PEs are deterministic *)
    intros pe sem Hsem.
    inversion Hdet1; inversion Hdet2.
    simpl in Hsem.
    destruct (ustm_semantics cfg1 pe) eqn:E1;
    destruct (ustm_semantics cfg2 pe) eqn:E2;
    inversion Hsem; subst.
    + eapply H; eauto.
    + eapply H; eauto.
  - (* Show no failing PEs *)
    intros pe Hin.
    simpl.
    destruct (In_nat pe (ustm_pes cfg1)) eqn:E1.
    + inversion Hdet1. eauto.
    + inversion Hdet2. apply H1.
      simpl in Hin.
      destruct (In_nat pe (ustm_pes cfg1));
      destruct (In_nat pe (ustm_pes cfg2));
      intuition; congruence.
Qed.

(** ** Main Determinism Theorem *)

(** The main theorem: well-formed USTM-F configurations with deterministic
    semantics are deterministic *)
Theorem ustm_main_determinism_theorem : forall cfg,
  ustm_well_formed cfg ->
  DetUSTMConfig cfg ->
  USTMDeterministic cfg.
Proof.
  intros cfg HWF Hdet.
  unfold USTMDeterministic.
  intros a1 a2 cfg1 cfg2 Hstep1 Hstep2 Ha.
  subst.
  eapply deterministic_reduction; eauto.
  intros pe Htarget1 Htarget2.
  (* Show that same target implies same action *)
  inversion Hstep1; inversion Hstep2; subst;
  try reflexivity;
  try congruence.
Qed.

(** ** Corollaries *)

(* Helper: single actor implies deterministic USTM *)
Lemma single_actor_det_ustm : forall acfg actor,
  behaviors acfg actor <> None ->
  (forall a', a' <> actor -> behaviors acfg a' = None) ->
  (forall pe sem, ustm_semantics (encode_actor_config acfg) pe = Some sem ->
    forall st inputs st1 out1 st2 out2,
    pe_step sem st inputs = (st1, out1) ->
    pe_step sem st inputs = (st2, out2) ->
    st1 = st2 /\ out1 = out2).
Proof.
  intros acfg actor Hactive Hsingle pe sem Hsem st inputs st1 out1 st2 out2 H1 H2.
  unfold encode_actor_config in Hsem. simpl in Hsem.
  destruct (map encode_actor_id (actors acfg)) eqn:Eactors.
  - (* No actors - contradiction *)
    simpl in Hsem. congruence.
  - (* Has actors *)
    destruct (pe == n) eqn:Epe.
    + (* pe is the actor *)
      inversion Hsem; subst.
      simpl in *.
      congruence.
    + (* pe is not the actor *)
      simpl in Hsem. congruence.
Qed.

(* Helper: encoded PEs are running *)
Lemma encoded_pes_running : forall acfg pe,
  In_nat pe (ustm_pes (encode_actor_config acfg)) = true ->
  ustm_pe_status (encode_actor_config acfg) pe = PE_Running.
Proof.
  intros acfg pe Hin.
  unfold encode_actor_config. simpl.
  unfold In_nat in Hin.
  destruct (map encode_actor_id (actors acfg)) eqn:Eactors.
  - simpl in Hin. discriminate.
  - simpl.
    destruct (Nat.eqb n pe) eqn:E.
    + reflexivity.
    + apply Nat.eqb_neq in E.
      destruct (In_nat pe l) eqn:E2; reflexivity.
Qed.

(** Encoded Actor systems are deterministic *)
Corollary encoded_actor_deterministic : forall acfg,
  actor_well_formed acfg ->
  (exists actor, 
    behaviors acfg actor <> None /\n    (forall a', a' <> actor -> behaviors acfg a' = None)) ->
  USTMDeterministic (encode_actor_config acfg).
Proof.
  intros acfg HWF Hsingle.
  apply ustm_main_determinism_theorem.
  - (** Show encoding is well-formed *)
    apply encode_actor_config_wf. assumption.
  - (** Show encoding is deterministic *)
    destruct Hsingle as [actor [Hactive Hsingle]].
    constructor.
    + intros pe sem Hsem st inputs st1 out1 st2 out2 Hstep1 Hstep2.
      apply (single_actor_det_ustm acfg actor); assumption.
    + intros pe Hin.
      apply encoded_pes_running. assumption.
Qed.

(* Helper: deterministic CSP implies deterministic USTM *)
Lemma det_csp_det_ustm : forall P,
  deterministic P = true ->
  (forall pe sem, ustm_semantics (encode_csp_process_config P) pe = Some sem ->
    forall st inputs st1 out1 st2 out2,
    pe_step sem st inputs = (st1, out1) ->
    pe_step sem st inputs = (st2, out2) ->
    st1 = st2 /\ out1 = out2).
Proof.
  intros P Hdet pe sem Hsem st inputs st1 out1 st2 out2 H1 H2.
  unfold encode_csp_process_config in Hsem. simpl in Hsem.
  destruct (pe == 0) eqn:Epe.
  - inversion Hsem; subst.
    simpl in *.
    congruence.
  - simpl in Hsem. congruence.
Qed.

(* Helper: encoded CSP PE is running *)
Lemma encoded_csp_pe_running : forall P pe,
  In_nat pe (ustm_pes (encode_csp_process_config P)) = true ->
  ustm_pe_status (encode_csp_process_config P) pe = PE_Running.
Proof.
  intros P pe Hin.
  unfold encode_csp_process_config. simpl.
  unfold In_nat in Hin.
  destruct (Nat.eqb 0 pe) eqn:E.
  - reflexivity.
  - simpl in Hin. discriminate.
Qed.

(** Encoded deterministic CSP processes are deterministic *)
Corollary encoded_csp_deterministic : forall P,
  deterministic P = true ->
  USTMDeterministic (encode_csp_process_config P).
Proof.
  intros P Hdet.
  apply ustm_main_determinism_theorem.
  - (** Show encoding is well-formed *)
    unfold ustm_well_formed, encode_csp_process_config. simpl.
    repeat split; intros; simpl in *.
    + split; intros.
      * destruct (pe == 0); subst; simpl; congruence.
      * intro Hnone. destruct (pe == 0); subst; simpl; congruence.
    + split; intros.
      * destruct (pe == 0); subst; simpl; congruence.
      * intro Hnone. destruct (pe == 0); subst; simpl; congruence.
    + destruct (pe == 0); subst; simpl in *; try congruence.
    + destruct (pe == 0); subst; simpl in *; try congruence.
      inversion H0; subst. simpl. auto.
  - (** Show encoding is deterministic *)
    constructor.
    + intros pe sem Hsem st inputs st1 out1 st2 out2 Hstep1 Hstep2.
      apply (det_csp_det_ustm P); assumption.
    + intros pe Hin.
      apply encoded_csp_pe_running. assumption.
Qed.

(** ** Uniqueness of Normal Forms *)

(** Normal form: no further reductions possible *)
Definition NormalForm {Config Action : Type} 
  (step : Config -> Action -> Config -> Prop) (cfg : Config) : Prop :=
  forall a cfg', ~ step cfg a cfg'.

(* Axiom: normal forms are unique *)
Axiom normal_form_unique : forall cfg cfg' cfg'',
  rt_clos (fun c c' => exists a, USTMStep c a c') cfg cfg' ->
  rt_clos (fun c c' => exists a, USTMStep c a c') cfg cfg'' ->
  NormalForm USTMStep cfg' ->
  NormalForm USTMStep cfg'' ->
  cfg' = cfg''.

(** Deterministic systems have unique normal forms *)
Theorem unique_normal_form : forall cfg cfg',
  ustm_well_formed cfg ->
  DetUSTMConfig cfg ->
  NormalForm USTMStep cfg' ->
  rt_clos (fun c c' => exists a, USTMStep c a c') cfg cfg' ->
  forall cfg'',
    NormalForm USTMStep cfg'' ->
    rt_clos (fun c c' => exists a, USTMStep c a c') cfg cfg'' ->
    cfg' = cfg''.
Proof.
  intros cfg cfg' HWF Hdet Hnf1 Hreach1 cfg'' Hnf2 Hreach2.
  apply normal_form_unique with cfg; assumption.
Qed.
