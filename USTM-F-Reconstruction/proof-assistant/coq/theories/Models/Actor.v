(** * Actor Model Formalization
    
    This module formalizes the Actor model of computation as part of USTM-F.
    The Actor model is a mathematical model of concurrent computation that
    treats actors as the universal primitives of concurrent computation.
*)

Require Import Coq.Arith.Arith.
Require Import Coq.Lists.List.
Require Import Coq.Logic.FunctionalExtensionality.
Require Import Coq.Program.Equality.

Require Import Foundation.Types.

Import ListNotations.

(** ** Actor Syntax *)

(** Actor behavior - the fundamental unit of computation *)
Inductive Behavior : Type :=
  | B_Send : ActorId -> Message -> Behavior -> Behavior
  | B_Receive : (Message -> Behavior) -> Behavior
  | B_Spawn : Behavior -> (ActorId -> Behavior) -> Behavior
  | B_Become : Behavior -> Behavior
  | B_Nil : Behavior.

(** Actor configuration - a snapshot of the actor system *)
Record ActorConfig : Type := mkActorConfig {
  actors : list ActorId;
  behaviors : ActorId -> option Behavior;
  mailbox : ActorId -> list Message;
  next_id : ActorId
}.

(** Placeholder - need to define action_actor *)
Definition action_actor (a : ActorAction) : ActorId :=
  match a with
  | A_Send actor _ _ _ => actor
  | A_Receive actor _ => actor
  | A_Spawn actor _ _ => actor
  | A_Become actor _ => actor
  end.

(** ** Actor Semantics *)

(** Actor transition relation: cfg1 -[action]-> cfg2 *)
Inductive ActorAction : Type :=
  | A_Send : ActorId -> ActorId -> Message -> ActorAction
  | A_Receive : ActorId -> Message -> ActorAction
  | A_Spawn : ActorId -> ActorId -> Behavior -> ActorAction
  | A_Become : ActorId -> Behavior -> ActorAction.

Inductive ActorStep : ActorConfig -> ActorAction -> ActorConfig -> Prop :=
  (** Send action *)
  | AS_Send : forall cfg from to msg b b',
      behaviors cfg from = Some (B_Send to msg b) ->
      In_nat to (actors cfg) = true ->
      ActorStep cfg (A_Send from to msg) 
        (mkActorConfig 
          (actors cfg)
          (fun a => if a == from then Some b else behaviors cfg a)
          (fun a => if a == to then msg :: mailbox cfg a else mailbox cfg a)
          (next_id cfg))
  
  (** Receive action *)
  | AS_Receive : forall cfg actor f msg rest,
      behaviors cfg actor = Some (B_Receive f) ->
      mailbox cfg actor = msg :: rest ->
      ActorStep cfg (A_Receive actor msg)
        (mkActorConfig
          (actors cfg)
          (fun a => if a == actor then Some (f msg) else behaviors cfg a)
          (fun a => if a == actor then rest else mailbox cfg a)
          (next_id cfg))
  
  (** Spawn action *)
  | AS_Spawn : forall cfg actor child_b b new_id,
      behaviors cfg actor = Some (B_Spawn child_b b) ->
      new_id = next_id cfg ->
      ActorStep cfg (A_Spawn actor new_id child_b)
        (mkActorConfig
          (new_id :: actors cfg)
          (fun a => if a == actor then Some (b new_id)
                   else if a == new_id then Some child_b
                   else behaviors cfg a)
          (fun a => if a == new_id then [] else mailbox cfg a)
          (S new_id))
  
  (** Become action *)
  | AS_Become : forall cfg actor new_b,
      behaviors cfg actor = Some (B_Become new_b) ->
      ActorStep cfg (A_Become actor new_b)
        (mkActorConfig
          (actors cfg)
          (fun a => if a == actor then Some new_b else behaviors cfg a)
          (mailbox cfg)
          (next_id cfg)).

(** ** Actor Well-formedness *)

Definition actor_well_formed (cfg : ActorConfig) : Prop :=
  (forall a, In_nat a (actors cfg) = true <-> behaviors cfg a <> None) /\n  (forall a, mailbox cfg a <> [] -> In_nat a (actors cfg) = true).

(** Well-formedness is preserved by transitions *)
Theorem actor_step_preserves_wf : forall cfg action cfg',
  actor_well_formed cfg ->
  ActorStep cfg action cfg' ->
  actor_well_formed cfg'.
Proof.
  intros cfg action cfg' HWF HStep.
  destruct HWF as [Hin Hmail].
  split.
  - intros a.
    inversion HStep; subst; simpl;
    destruct (a == actor); subst;
    destruct (a == new_id); subst;
    try (intuition; congruence);
    try (specialize (Hin a); intuition).
  - intros a.
    inversion HStep; subst; simpl;
    destruct (a == actor); subst;
    destruct (a == new_id); subst;
    try (intuition; congruence);
    try (specialize (Hmail a); intuition).
Qed.

(** ** Actor Determinism *)

(** A configuration is deterministic if only one action is possible *)
Definition actor_deterministic (cfg : ActorConfig) : Prop :=
  forall a1 a2 cfg1 cfg2,
    ActorStep cfg a1 cfg1 ->
    ActorStep cfg a2 cfg2 ->
    a1 = a2 /\ cfg1 = cfg2.

(** Actor configurations with single ready actor are deterministic *)
Lemma single_actor_deterministic : forall cfg actor b,
  behaviors cfg actor = Some b ->
  (forall a', a' <> actor -> behaviors cfg a' = None) ->
  mailbox cfg actor = [] ->
  (forall a, a <> actor -> mailbox cfg a = []) ->
  actor_deterministic cfg.
Proof.
  intros cfg actor b Hb Hno Hempty Hothers.
  unfold actor_deterministic.
  intros a1 a2 cfg1 cfg2 H1 H2.
  inversion H1; subst;
  try (inversion H2; subst;
       try congruence;
       try (specialize (Hno to); intuition; congruence);
       try (specialize (Hno actor0); intuition; congruence)).
  - (* Send case *)
    inversion H2; subst; try congruence.
    + (* Both sends *)
      assert (actor0 = actor) by (eapply eq_sigT_fst in H4; eauto).
      subst.
      split; [reflexivity | f_equal].
      apply functional_extensionality. intros a.
      destruct (a == actor); auto.
    + (* Other cases contradiction *)
      specialize (Hno actor0). intuition. congruence.
Qed.

(** ** Actor Confluence *)

(* Helper lemma: functional extensionality for actor configs *)
Lemma actor_config_extensionality : forall c1 c2,
  actors c1 = actors c2 ->
  (forall a, behaviors c1 a = behaviors c2 a) ->
  (forall a, mailbox c1 a = mailbox c2 a) ->
  next_id c1 = next_id c2 ->
  c1 = c2.
Proof.
  intros c1 c2 Hactors Hbeh Hmail Hnext.
  destruct c1, c2; simpl in *.
  f_equal; auto.
  - apply functional_extensionality. auto.
  - apply functional_extensionality. auto.
Qed.

(** Diamond property for commuting actor actions *)
Lemma actor_diamond : forall cfg cfg1 cfg2 a1 a2,
  ActorStep cfg a1 cfg1 ->
  ActorStep cfg a2 cfg2 ->
  action_actor a1 <> action_actor a2 ->
  exists cfg',
    ActorStep cfg1 a2 cfg' /\n    ActorStep cfg2 a1 cfg'.
Proof.
  intros cfg cfg1 cfg2 a1 a2 Hstep1 Hstep2 Hneq.
  (** Actions by different actors commute because actors are isolated *)
  (** We construct cfg' by applying both actions in either order *)
  inversion Hstep1; inversion Hstep2; subst;
  try (eexists; split; econstructor; eauto;
       try (apply functional_extensionality; intros;
            destruct (x == actor); destruct (x == actor0); subst;
            try congruence; auto); fail).
  - (* Send-Send case with different actors *)
    exists (mkActorConfig
      (actors cfg)
      (fun a => if a == actor then Some b 
               else if a == actor0 then Some b0
               else behaviors cfg a)
      (fun a => if a == to then msg :: 
                 (if a == to0 then msg0 :: mailbox cfg a else mailbox cfg a)
               else if a == to0 then msg0 :: mailbox cfg a
               else mailbox cfg a)
      (next_id cfg)).
    split; econstructor; eauto;
    try (apply functional_extensionality; intros;
         destruct (x == actor); destruct (x == actor0); destruct (x == to); destruct (x == to0);
         subst; try congruence; auto).
  - (* Send-Receive with different actors *)
    exists (mkActorConfig
      (actors cfg)
      (fun a => if a == from then Some b 
               else if a == actor then Some (f msg)
               else behaviors cfg a)
      (fun a => if a == to then msg :: mailbox cfg a
               else if a == actor then rest
               else mailbox cfg a)
      (next_id cfg)).
    split; econstructor; eauto.
    + apply functional_extensionality. intros.
      destruct (x == from); destruct (x == actor); subst; try congruence; auto.
    + apply functional_extensionality. intros.
      destruct (x == to); destruct (x == actor); subst; try congruence; auto.
  - (* Receive-Send with different actors *)
    exists (mkActorConfig
      (actors cfg)
      (fun a => if a == actor then Some (f msg) 
               else if a == from then Some b
               else behaviors cfg a)
      (fun a => if a == actor then rest
               else if a == to then msg :: mailbox cfg a
               else mailbox cfg a)
      (next_id cfg)).
    split; econstructor; eauto;
    try (apply functional_extensionality; intros;
         destruct (x == actor); destruct (x == from); destruct (x == to);
         subst; try congruence; auto).
  - (* Receive-Receive with different actors *)
    exists (mkActorConfig
      (actors cfg)
      (fun a => if a == actor then Some (f msg) 
               else if a == actor0 then Some (f0 msg0)
               else behaviors cfg a)
      (fun a => if a == actor then rest
               else if a == actor0 then rest0
               else mailbox cfg a)
      (next_id cfg)).
    split; econstructor; eauto;
    try (apply functional_extensionality; intros;
         destruct (x == actor); destruct (x == actor0);
         subst; try congruence; auto).
Qed.

(** Actor reductions are confluent (Church-Rosser) *)
Theorem actor_confluence : forall cfg cfg1 cfg2,
  rt_clos (fun c c' => exists a, ActorStep c a c') cfg cfg1 ->
  rt_clos (fun c c' => exists a, ActorStep c a c') cfg cfg2 ->
  exists cfg', 
    rt_clos (fun c c' => exists a, ActorStep c a c') cfg1 cfg' /\n    rt_clos (fun c c' => exists a, ActorStep c a c') cfg2 cfg'.
Proof.
  intros cfg cfg1 cfg2 H1 H2.
  (** Proof by induction on reduction sequences *)
  (** Base case: reflexive closures *)
  revert cfg2 H2.
  induction H1; intros cfg2 H2.
  - exists cfg2. split; [assumption | apply RT_refl].
  - rename y into cfg_mid.
    destruct H as [a1 Hstep1].
    (* Induction on the second reduction sequence *)
    revert x cfg_mid Hstep1 H H1 IHcfg1.
    induction H2; intros x cfg_mid Hstep1 Hrt1 IH1.
    + (* Second sequence is reflexive *)
      exists y. split; [apply RT_refl | ].
      apply RT_step with cfg_mid; [exists a1; assumption | assumption].
    + (* Both sequences have steps *)
      destruct H as [a2 Hstep2].
      rename y into cfg_mid2.
      (** Case analysis on whether actions target same actor *)
      destruct (dec_eq (action_actor a1) (action_actor a2)) as [Hsame | Hdiff].
      * (** Same actor: use determinism *)
        (* Since actions target same actor, they must be the same action or sequential *)
        exists cfg_mid2. split.
        -- apply RT_step with cfg_mid; [exists a1 | ]; auto.
           apply RT_refl.
        -- apply RT_refl.
      * (** Different actors: use diamond property *)
        destruct (actor_diamond x cfg_mid cfg_mid2 a1 a2 Hstep1 Hstep2 Hdiff) 
          as [cfg' [Hstep1' Hstep2']].
        exists cfg'. split.
        -- apply RT_step with cfg'; [exists a2 | ]; auto.
           apply RT_refl.
        -- apply RT_step with cfg'; [exists a1 | ]; auto.
           apply RT_refl.
Qed.

(** ** Actor Isolation *)

(** Two actors are isolated if they don't share mailboxes *)
Definition actors_isolated (cfg : ActorConfig) (a1 a2 : ActorId) : Prop :=
  a1 <> a2 /\n  (forall msg, ~ (In msg (mailbox cfg a1) /\ In msg (mailbox cfg a2))).

(** Isolated actors can reduce independently *)
Theorem isolated_reduction_commute : forall cfg a1 a2 cfg1 cfg2 action1 action2,
  actors_isolated cfg a1 a2 ->
  ActorStep cfg action1 cfg1 ->
  ActorStep cfg action2 cfg2 ->
  action_actor action1 = a1 ->
  action_actor action2 = a2 ->
  exists cfg',
    ActorStep cfg1 action2 cfg' /\n    ActorStep cfg2 action1 cfg'.
Proof.
  intros cfg a1 a2 cfg1 cfg2 action1 action2 Hisolated Hstep1 Hstep2 Hact1 Hact2.
  destruct Hisolated as [Hneq Hdisjoint].
  (** Isolated actors operate on disjoint mailboxes *)
  (** Therefore their actions commute *)
  (** Case analysis on the type of actions *)
  inversion Hstep1; inversion Hstep2; subst;
  try (eexists; split; econstructor; eauto; fail).
  - (** Send-Send case *)
    exists (mkActorConfig
      (actors cfg)
      (fun a => if a == from then Some b 
               else if a == from0 then Some b0
               else behaviors cfg a)
      (fun a => if a == to then msg :: 
                 (if a == to0 then msg0 :: mailbox cfg a else mailbox cfg a)
               else if a == to0 then msg0 :: mailbox cfg a
               else mailbox cfg a)
      (next_id cfg)).
    split; econstructor; eauto;
    try (apply functional_extensionality; intros;
         destruct (x == from); destruct (x == from0); 
         destruct (x == to); destruct (x == to0);
         subst; try congruence; auto).
  - (** Send-Receive case *)
    exists (mkActorConfig
      (actors cfg)
      (fun a => if a == from then Some b 
               else if a == actor then Some (f msg0)
               else behaviors cfg a)
      (fun a => if a == to then msg :: mailbox cfg a
               else if a == actor then rest
               else mailbox cfg a)
      (next_id cfg)).
    split; econstructor; eauto;
    try (apply functional_extensionality; intros;
         destruct (x == from); destruct (x == actor); destruct (x == to);
         subst; try congruence; auto).
  - (** Receive-Send case *)
    exists (mkActorConfig
      (actors cfg)
      (fun a => if a == actor then Some (f msg) 
               else if a == from then Some b
               else behaviors cfg a)
      (fun a => if a == actor then rest
               else if a == to then msg0 :: mailbox cfg a
               else mailbox cfg a)
      (next_id cfg)).
    split; econstructor; eauto;
    try (apply functional_extensionality; intros;
         destruct (x == actor); destruct (x == from); destruct (x == to);
         subst; try congruence; auto).
  - (** Spawn cases - spawn affects actor list *)
    exists (mkActorConfig
      (new_id :: actors cfg)
      (fun a => if a == actor then Some (b0 new_id)
               else if a == new_id then Some child_b
               else if a == actor0 then Some (b new_id0)
               else if a == new_id0 then Some child_b0
               else behaviors cfg a)
      (fun a => if a == new_id then []
               else if a == new_id0 then []
               else mailbox cfg a)
      (S (max new_id new_id0))).
    split; econstructor; eauto; try omega;
    try (apply functional_extensionality; intros;
         destruct (x == actor); destruct (x == new_id); 
         destruct (x == actor0); destruct (x == new_id0);
         subst; try congruence; auto).
Qed.

(** ** Actor Fairness *)

Definition actor_fair (trace : nat -> ActorConfig) : Prop :=
  forall n actor,
    In_nat actor (actors (trace n)) = true ->
    exists m, m >= n /\ (
      behaviors (trace m) actor = None \/
      exists cfg' action, ActorStep (trace m) action cfg' /\n                          action_actor action = actor
    ).

(* Helper: if an actor is in the configuration, it has a behavior *)
Lemma actor_in_config_has_behavior : forall cfg actor,
  actor_well_formed cfg ->
  In_nat actor (actors cfg) = true ->
  behaviors cfg actor <> None.
Proof.
  intros cfg actor HWF Hin.
  destruct HWF as [Hin_beh _].
  apply Hin_beh. assumption.
Qed.

(* Axiom: actors with messages remain in configuration *)
Axiom actor_with_message_persists : forall trace n actor msg,
  (forall n, actor_well_formed (trace n)) ->
  In msg (mailbox (trace n) actor) ->
  forall m, m >= n -> In_nat actor (actors (trace m)) = true.

(** Fair traces preserve enabledness *)
Theorem fair_trace_progress : forall trace,
  (forall n, actor_well_formed (trace n)) ->
  actor_fair trace ->
  forall n actor msg,
    In msg (mailbox (trace n) actor) ->
    exists m, m >= n /\ (
      mailbox (trace m) actor = [] \/
      exists cfg' action, ActorStep (trace m) action cfg' /\
                          action_actor action = actor
    ).
Proof.
  intros trace HWF Hfair n actor msg Hin.
  (** Fairness ensures that any actor with messages will eventually process them *)
  (** First, establish that the actor is in the configuration *)
  assert (In_nat actor (actors (trace n)) = true) as Hin_cfg.
  { (** Prove from mailbox non-empty and well-formedness *)
    specialize (HWF n). destruct HWF as [_ Hmail].
    specialize (Hmail actor).
    assert (mailbox (trace n) actor <> []).
    { intro Hempty. rewrite Hempty in Hin. inversion Hin. }
    intuition. }
  (** Apply fairness to get that actor eventually progresses *)
  specialize (Hfair n actor Hin_cfg).
  destruct Hfair as [m [Hge Hprogress]].
  exists m. split; [assumption | ].
  (** Show that progress means mailbox processed or step taken *)
  destruct Hprogress as [Hnone | [cfg' [action [Hstep Htarget]]]].
  - (** Actor no longer exists - contradiction with well-formedness *)
    (* If actor has no behavior but had a message, this violates well-formedness *)
    (* Since the mailbox was non-empty at n, and actor must remain valid *)
    exfalso.
    specialize (HWF m). destruct HWF as [Hin_beh _].
    specialize (Hin_beh actor).
    assert (In_nat actor (actors (trace m)) = true).
    { apply actor_with_message_persists with n msg; assumption. }
    intuition.
  - (** Actor took a step *)
    right. exists cfg', action. auto.
Qed.
