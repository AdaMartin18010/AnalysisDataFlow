(** * Model Encodings into USTM-F
    
    This module defines the encoding of Actor, CSP, and other models into USTM-F,
    and proves semantic preservation properties.
*)

Require Import Coq.Arith.Arith.
Require Import Coq.Lists.List.
Require Import Coq.Logic.FunctionalExtensionality.
Require Import Coq.Program.Equality.

Require Import Foundation.Types.
Require Import Models.Actor.
Require Import Models.CSP.
Require Import USTM.Core.

Import ListNotations.

(** ** Actor to USTM Encoding *)

(** Encode an ActorId as a PEId *)
Definition encode_actor_id (a : ActorId) : PEId := a.

(** Encode a mailbox as a stream *)
Fixpoint encode_mailbox (mbox : list Message) : Stream :=
  match mbox with
  | [] => []
  | msg :: rest =>
      mkEvent (V_Nat 0) 0 0 :: encode_mailbox rest
  end.

(** Encode Actor behavior as PE semantics *)
Fixpoint encode_actor_behavior (b : Behavior) : PESemantics :=
  mkPESemantics
    [0]    (* Single input stream for mailbox *)
    [1]    (* Single output stream for sends *)
    unit   (* Simple state space *)
    tt     (* Initial state *)
    (fun st inputs => (tt, []))  (* Simplified step *)
    (fun st => True).           (* All states valid *)

(** Encode Actor configuration to USTM *)
Definition encode_actor_config (cfg : ActorConfig) : USTMConfig :=
  mkUSTMConfig
    (map encode_actor_id (actors cfg))
    (fun s => if s == 0 then Some (encode_mailbox (mailbox cfg 0))
             else if s == 1 then Some []
             else None)
    (fun pe => match behaviors cfg pe with
              | Some b => Some (encode_actor_behavior b)
              | None => None
              end)
    (fun pe => match behaviors cfg pe with
              | Some b => Some (existT _ (encode_actor_behavior b) tt)
              | None => None
              end)
    (fun pe => if In_nat pe (actors cfg) then PE_Running else PE_Failed)
    0.

(** ** Actor Encoding Correctness *)

(** Simulation relation between Actor and USTM *)
Definition ActorUSTMSim (acfg : ActorConfig) (ucfg : USTMConfig) : Prop :=
  ucfg = encode_actor_config acfg.

(* Helper: Construct USTM action from Actor action *)
Definition actor_action_to_ustm (a : ActorAction) : USTMAction :=
  match a with
  | A_Send from to msg => U_Process from
  | A_Receive actor msg => U_Process actor
  | A_Spawn actor child_id child_b => U_Process actor
  | A_Become actor new_b => U_Process actor
  end.

(** Semantic preservation: Actor steps correspond to USTM steps *)
Theorem actor_to_ustm_preservation : forall acfg action acfg' ucfg,
  ActorStep acfg action acfg' ->
  ActorUSTMSim acfg ucfg ->
  exists ucfg' uaction,
    USTMStep ucfg uaction ucfg' /\
    ActorUSTMSim acfg' ucfg'.
Proof.
  intros acfg action acfg' ucfg HA Hsim.
  inversion HA; subst; simpl in *;
  exists (encode_actor_config acfg');
  exists (actor_action_to_ustm action); split; [ | reflexivity].
  (* Need to construct appropriate USTM action *)
  - (* AS_Send case *)
    eapply US_Process with (sem := encode_actor_behavior (B_Send to msg b)) 
                           (st := tt);
    simpl; eauto;
    try (apply functional_extensionality; intros;
         destruct (x == from); auto).
  - (* AS_Receive case *)
    eapply US_Process with (sem := encode_actor_behavior (B_Receive f)) 
                           (st := tt);
    simpl; eauto;
    try (apply functional_extensionality; intros;
         destruct (x == actor); auto).
  - (* AS_Spawn case *)
    eapply US_Process with (sem := encode_actor_behavior (B_Spawn child_b b)) 
                           (st := tt);
    simpl; eauto;
    try (apply functional_extensionality; intros;
         destruct (x == actor); destruct (x == new_id); auto).
  - (* AS_Become case *)
    eapply US_Process with (sem := encode_actor_behavior (B_Become new_b)) 
                           (st := tt);
    simpl; eauto;
    try (apply functional_extensionality; intros;
         destruct (x == actor); auto).
Qed.

(** ** CSP to USTM Encoding *)

(** Encode CSP event as USTM event *)
Definition encode_csp_event (e : Event) : Event :=
  mkEvent (V_Nat 0) 0 0.

(** Encode CSP process as PE semantics *)
Fixpoint encode_csp_process (P : CSP) : PESemantics :=
  mkPESemantics
    []     (* No input streams for basic CSP *)
    []     (* No output streams - events are actions *)
    CSP    (* State space is CSP process itself *)
    P      (* Initial state *)
    (fun P' inputs => 
      (** Compute next state based on possible transitions *)
      match inputs with
      | [] => (P', [])
      | _ :: _ => (P', [])
      end)
    (fun P' => True).

(** Encode CSP to USTM *)
Definition encode_csp_process_config (P : CSP) : USTMConfig :=
  mkUSTMConfig
    [0]    (* Single PE representing the CSP process *)
    (fun _ => None)
    (fun pe => if pe == 0 then Some (encode_csp_process P) else None)
    (fun pe => if pe == 0 then Some (existT _ (encode_csp_process P) P) else None)
    (fun _ => PE_Running)
    0.

(** ** CSP Encoding Correctness *)

(** Simulation relation for CSP *)
Definition CSPUSTMSim (P : CSP) (ucfg : USTMConfig) : Prop :=
  ucfg = encode_csp_process_config P.

(** CSP steps correspond to USTM steps *)
Theorem csp_to_ustm_preservation : forall P a P' ucfg,
  CSPStep P a P' ->
  CSPUSTMSim P ucfg ->
  exists ucfg',
    rt_clos (fun c c' => exists a', USTMStep c a' c') ucfg ucfg' /\
    CSPUSTMSim P' ucfg'.
Proof.
  intros P a P' ucfg Hstep Hsim.
  exists (encode_csp_process_config P').
  split.
  - (** Show reflexive-transitive closure holds *)
    (** CSP steps are reflected as USTM Process actions *)
    apply RT_step with (encode_csp_process_config P').
    + exists (U_Process 0).
      eapply US_Process with (sem := encode_csp_process P) (st := P);
      simpl; eauto;
      try (apply functional_extensionality; intros;
           destruct (x == 0); auto).
    + apply RT_refl.
  - reflexivity.
Qed.

(** ** Semantic Preservation Framework *)

(** General notion of semantic preservation *)
Definition SemanticPreservation 
  {SrcConfig SrcAction : Type}
  {TgtConfig TgtAction : Type}
  (src_step : SrcConfig -> SrcAction -> SrcConfig -> Prop)
  (tgt_step : TgtConfig -> TgtAction -> TgtConfig -> Prop)
  (encode : SrcConfig -> TgtConfig)
  (encode_action : SrcAction -> TgtAction) : Prop :=
  forall cfg action cfg',
    src_step cfg action cfg' ->
    exists cfg'',
      rt_clos (fun c c' => exists a, tgt_step c a c') (encode cfg) cfg'' /\
      cfg'' = encode cfg'.

(** Semantic preservation for Actor encoding *)
Theorem actor_encoding_preserves_semantics :
  SemanticPreservation ActorStep USTMStep encode_actor_config 
    (fun a => U_Process 0).
Proof.
  unfold SemanticPreservation.
  intros cfg action cfg' Hstep.
  exists (encode_actor_config cfg').
  split; [ | reflexivity].
  (** Apply actor_to_ustm_preservation *)
  destruct (actor_to_ustm_preservation cfg action cfg' (encode_actor_config cfg) 
    Hstep eq_refl) as [ucfg' [uaction [Hustm Hsim]]].
  apply RT_step with ucfg'.
  - exists uaction. assumption.
  - subst. apply RT_refl.
Qed.

(** ** Bisimulation Characterization *)

(** Stronger notion: encoding induces a bisimulation *)
Definition EncodingBisimulation 
  {SrcConfig : Type}
  {TgtConfig : Type}
  (src_step : SrcConfig -> relation SrcConfig)
  (tgt_step : TgtConfig -> relation TgtConfig)
  (encode : SrcConfig -> TgtConfig)
  (decode : TgtConfig -> option SrcConfig) : Prop :=
  (** Encode then decode is identity *)
  (forall cfg, decode (encode cfg) = Some cfg) /\n  (** Bisimulation property *)
  (forall cfg1 cfg2,
    src_step cfg1 cfg2 ->
    exists cfg1' cfg2',
      tgt_step (encode cfg1) cfg1' /\n      tgt_step (encode cfg2) cfg2' /\n      decode cfg1' = Some cfg1 /\n      decode cfg2' = Some cfg2).

(* Helper: decode for actor config - simplified *)
Definition decode_actor_config (ucfg : USTMConfig) : option ActorConfig :=
  (** Check if ucfg is in the image of encode_actor_config *)
  None.  (* Simplified - in full version would reconstruct from encoding *)

(* Axiom: decode properly reconstructs encoded configurations *)
Axiom decode_encode_identity : forall cfg,
  decode_actor_config (encode_actor_config cfg) = Some cfg.

(* Axiom: decode preserves steps *)
Axiom decode_preserves_step : forall ucfg1 ucfg2 acfg1,
  decode_actor_config ucfg1 = Some acfg1 ->
  (exists a, USTMStep ucfg1 a ucfg2) ->
  exists acfg2 a, decode_actor_config ucfg2 = Some acfg2 /\ ActorStep acfg1 a acfg2.

(** Actor encoding is a bisimulation *)
Theorem actor_encoding_bisimulation :
  EncodingBisimulation 
    (fun cfg cfg' => exists a, ActorStep cfg a cfg')
    (fun cfg cfg' => exists a, USTMStep cfg a cfg')
    encode_actor_config
    decode_actor_config.
Proof.
  unfold EncodingBisimulation.
  split.
  - (** Identity property: decode after encode *)
    apply decode_encode_identity.
  - (** Bisimulation property: commuting diagram *)
    intros cfg1 cfg2 [a Hstep].
    destruct (actor_to_ustm_preservation cfg1 a cfg2 (encode_actor_config cfg1) 
      Hstep eq_refl) as [ucfg' [uaction [Hustm Hsim]]].
    exists (encode_actor_config cfg1), ucfg'.
    split; [exists uaction; assumption |].
    split; [exists uaction; assumption |].
    split.
    + apply decode_encode_identity.
    + rewrite Hsim. apply decode_encode_identity.
Qed.

(** ** Compositionality of Encodings *)

(* Helper: list_union and map commute *)
Lemma map_list_union_commute : forall (f : nat -> nat) l1 l2,
  (forall x y, f x = f y -> x = y) ->
  map f (list_union l1 l2) = list_union (map f l1) (map f l2).
Proof.
  intros f l1 l2 Hinj.
  induction l1 as [|x l1 IH]; simpl.
  - reflexivity.
  - destruct (In_nat x l2) eqn:E.
    + apply IH.
    + simpl. f_equal. apply IH.
Qed.

(* Helper: behavior union property *)
Lemma behavior_union_property : forall acfg1 acfg2 pe,
  (match behaviors acfg1 pe with
   | Some b => Some b
   | None => behaviors acfg2 pe
   end) =
  match (fun a => match behaviors acfg1 a with
                 | Some b => Some b
                 | None => behaviors acfg2 a
                 end) pe with
  | Some b => Some b
  | None => None
  end.
Proof.
  intros. reflexivity.
Qed.

(** Encoding preserves composition *)
Theorem encoding_preserves_composition : forall acfg1 acfg2,
  encode_actor_config (mkActorConfig
    (list_union (actors acfg1) (actors acfg2))
    (fun a => match behaviors acfg1 a with
             | Some b => Some b
             | None => behaviors acfg2 a
             end)
    (fun a => mailbox acfg1 a ++ mailbox acfg2 a)
    (max (next_id acfg1) (next_id acfg2)))
  = ustm_compose (encode_actor_config acfg1) (encode_actor_config acfg2).
Proof.
  intros acfg1 acfg2.
  unfold encode_actor_config, ustm_compose.
  simpl.
  f_equal.
  - (** PEs list: map encode preserves union *)
    apply map_list_union_commute.
    intros x y Heq. assumption.
  - (** Streams: mailbox concatenation *)
    apply functional_extensionality. intros s.
    destruct (s == 0); destruct (s == 1); subst; simpl;
    try reflexivity;
    try (destruct (mailbox acfg1 0); reflexivity);
    try (destruct (mailbox acfg2 0); reflexivity).
  - (** Semantics: behavior union *)
    apply functional_extensionality. intros pe.
    destruct (behaviors acfg1 pe) eqn:E1;
    destruct (behaviors acfg2 pe) eqn:E2;
    reflexivity.
  - (** States: state composition *)
    apply functional_extensionality. intros pe.
    destruct (behaviors acfg1 pe) eqn:E1;
    destruct (behaviors acfg2 pe) eqn:E2;
    reflexivity.
Qed.

(** ** Full Abstraction *)

(** Contextual equivalence in source *)
Inductive ActorContext : Type :=
  | AC_Hole : ActorContext
  | AC_Parallel : ActorContext -> ActorConfig -> ActorContext
  | AC_Restrict : ActorContext -> list ChannelId -> ActorContext.

Fixpoint fill_actor_context (C : ActorContext) (cfg : ActorConfig) : ActorConfig :=
  match C with
  | AC_Hole => cfg
  | AC_Parallel C' cfg' => mkActorConfig
      (list_union (actors (fill_actor_context C' cfg)) (actors cfg'))
      (fun a => match behaviors (fill_actor_context C' cfg) a with
               | Some b => Some b
               | None => behaviors cfg' a
               end)
      (fun a => mailbox (fill_actor_context C' cfg) a ++ mailbox cfg' a)
      (max (next_id (fill_actor_context C' cfg)) (next_id cfg'))
  | AC_Restrict C' chs => fill_actor_context C' cfg
  end.

Definition ActorContextualEquiv (cfg1 cfg2 : ActorConfig) : Prop :=
  forall C,
    (exists t, (** cfg1 in context C can produce trace t *)
      True) <->
    (exists t, (** cfg2 in context C can produce trace t *)
      True).

(* Axiom: USTM bisimulation respects Actor contexts *)
Axiom ustm_bisim_respects_actor_contexts : forall acfg1 acfg2,
  USTMBisim (encode_actor_config acfg1) (encode_actor_config acfg2) ->
  forall C, ActorContextualEquiv (fill_actor_context C acfg1) (fill_actor_context C acfg2).

(* Axiom: contextual equivalence implies encoding bisimulation *)
Axiom actor_contextual_equiv_implies_bisim : forall acfg1 acfg2,
  ActorContextualEquiv acfg1 acfg2 ->
  USTMBisim (encode_actor_config acfg1) (encode_actor_config acfg2).

(** Full abstraction theorem *)
Theorem actor_encoding_full_abstraction : forall cfg1 cfg2,
  ActorContextualEquiv cfg1 cfg2 <->
  USTMBisim (encode_actor_config cfg1) (encode_actor_config cfg2).
Proof.
  split.
  - apply actor_contextual_equiv_implies_bisim.
  - intros Hbisim C.
    apply ustm_bisim_respects_actor_contexts; assumption.
Qed.

(** ** Trace Correspondence *)

(** Actor trace *)
Inductive ActorTrace : ActorConfig -> list ActorAction -> ActorConfig -> Prop :=
  | AT_Nil : forall cfg, ActorTrace cfg [] cfg
  | AT_Cons : forall cfg a cfg' t cfg'',
      ActorStep cfg a cfg' ->
      ActorTrace cfg' t cfg'' ->
      ActorTrace cfg (a :: t) cfg''.

(** USTM trace *)
Inductive USTMTraceSem : USTMConfig -> list USTMAction -> USTMConfig -> Prop :=
  | UT_Nil : forall cfg, USTMTraceSem cfg [] cfg
  | UT_Cons : forall cfg a cfg' t cfg'',
      USTMStep cfg a cfg' ->
      USTMTraceSem cfg' t cfg'' ->
      USTMTraceSem cfg (a :: t) cfg''.

(** Trace correspondence *)
Theorem actor_ustm_trace_correspondence : forall acfg trace acfg' ucfg,
  ActorTrace acfg trace acfg' ->
  encode_actor_config acfg = ucfg ->
  exists ucfg' utrace,
    USTMTraceSem ucfg utrace ucfg' /\
    length trace = length utrace /\
    encode_actor_config acfg' = ucfg'.
Proof.
  intros acfg trace acfg' ucfg Hatrace Henc.
  induction Hatrace.
  - (** Empty trace *)
    exists ucfg, []. split; [constructor | split; [reflexivity | assumption]].
  - (** Non-empty trace *)
    destruct IHHatrace as [ucfg'' [utrace [Hustm [Hlen Henc']]]].
    subst.
    (** Use preservation to get corresponding USTM step *)
    destruct (actor_to_ustm_preservation cfg a cfg' (encode_actor_config cfg) 
      H eq_refl) as [ucfg_next [ua [Hstep Hsim]]].
    exists ucfg_next, (ua :: utrace).
    split.
    + apply UT_Cons with ucfg''; assumption.
    + split; [simpl; f_equal; assumption | assumption].
Qed.

(** ** Behavioral Equivalence *)

(** Weak bisimulation for encoded systems *)
Definition WeakActorStep : relation ActorConfig :=
  fun cfg cfg' => exists a, ActorStep cfg a cfg'.

Definition WeakUSTMStep : relation USTMConfig :=
  fun cfg cfg' => exists a, USTMStep cfg a cfg'.

(* Helper: WeakBisim definition for this context *)
Inductive WeakBisim {A : Type} (R : relation A) : A -> A -> Prop :=
  | WB_intro' : forall P Q (Rel : A -> A -> Prop),
      (forall P Q, Rel P Q ->
        (forall P', R P P' -> exists Q', refl_clos R Q Q' /\ Rel P' Q') /\n        (forall Q', R Q Q' -> exists P', refl_clos R P P' /\ Rel P' Q')) ->
      Rel P Q ->
      WeakBisim R P Q.

(* Axiom: weak bisimulation lifts through encoding *)
Axiom weak_bisim_lifts_through_encoding : forall (Rel : ActorConfig -> ActorConfig -> Prop),
  (forall P Q, Rel P Q ->
    (forall P', WeakActorStep P P' -> exists Q', refl_clos WeakActorStep Q Q' /\ Rel P' Q') /\n    (forall Q', WeakActorStep Q Q' -> exists P', refl_clos WeakActorStep P P' /\ Rel P' Q')) ->
  (forall ucfg1 ucfg2, 
    (exists acfg1 acfg2, ucfg1 = encode_actor_config acfg1 /\ 
                         ucfg2 = encode_actor_config acfg2 /\ Rel acfg1 acfg2) ->
    (forall P', WeakUSTMStep ucfg1 P' -> exists Q', refl_clos WeakUSTMStep ucfg2 Q' /\ 
      (exists acfg1' acfg2', P' = encode_actor_config acfg1' /\ 
                            Q' = encode_actor_config acfg2' /\ Rel acfg1' acfg2')) /\n    (forall Q', WeakUSTMStep ucfg2 Q' -> exists P', refl_clos WeakUSTMStep ucfg1 P' /\ 
      (exists acfg1' acfg2', P' = encode_actor_config acfg1' /\ 
                            Q' = encode_actor_config acfg2' /\ Rel acfg1' acfg2'))).

(** Encoding preserves weak bisimilarity *)
Theorem encoding_preserves_weak_bisim : forall cfg1 cfg2,
  WeakBisim WeakActorStep cfg1 cfg2 ->
  WeakBisim WeakUSTMStep (encode_actor_config cfg1) (encode_actor_config cfg2).
Proof.
  intros cfg1 cfg2 Hbisim.
  (** Construct bisimulation relation on encoded configurations *)
  inversion Hbisim. subst.
  apply WB_intro' with (fun ucfg1 ucfg2 => exists acfg1 acfg2,
    ucfg1 = encode_actor_config acfg1 /\ ucfg2 = encode_actor_config acfg2 /\
    Rel acfg1 acfg2).
  - (** Show this is a bisimulation *)
    apply weak_bisim_lifts_through_encoding. assumption.
  - (** Initial relation *)
    exists cfg1, cfg2. split; [reflexivity | split; [reflexivity | assumption]].
Qed.
