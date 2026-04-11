(** * CSP (Communicating Sequential Processes) Formalization
    
    This module formalizes Hoare's CSP calculus as part of USTM-F.
    CSP is a process algebra for describing patterns of interaction
    in concurrent systems.
*)

Require Import Coq.Arith.Arith.
Require Import Coq.Lists.List.
Require Import Coq.Strings.String.
Require Import Coq.Logic.FunctionalExtensionality.
Require Import Coq.Setoids.Setoid.

Require Import Foundation.Types.

Import ListNotations.

(** ** CSP Syntax *)

(** Event/channel names *)
Definition Event := string.

(** CSP Process syntax *)
Inductive CSP : Type :=
  | STOP : CSP                          (** Deadlock *)
  | SKIP : CSP                          (** Successful termination *)
  | Prefix : Event -> CSP -> CSP        (** e -> P *)
  | ExtChoice : CSP -> CSP -> CSP       (** P [] Q - external choice *)
  | IntChoice : CSP -> CSP -> CSP       (** P |~| Q - internal choice *)
  | Parallel : CSP -> list Event -> CSP -> CSP  (** P [| A |] Q - parallel *)
  | Hide : CSP -> list Event -> CSP     (** P \ A - hiding *)
  | Rename : CSP -> (Event -> Event) -> CSP.    (** P[[f]] - renaming *)

Notation "e '-->' P" := (Prefix e P) (at level 60, right associativity).
Notation "P '[]' Q" := (ExtChoice P Q) (at level 50, left associativity).
Notation "P '|~|' Q" := (IntChoice P Q) (at level 50, left associativity).
Notation "P '[|' A '|]' Q" := (Parallel P A Q) (at level 50, left associativity).
Notation "P '\\' A" := (Hide P A) (at level 50, left associativity).

(** ** CSP Operational Semantics *)

(** Observable actions *)
Inductive Action : Type :=
  | ActEvent : Event -> Action
  | ActTau : Action           (** Internal action *)
  | ActTick : Action.         (** Termination signal *)

(** Operational semantics transition relation *)
Inductive CSPStep : CSP -> Action -> CSP -> Prop :=
  (** Prefix *)
  | CS_Prefix : forall e P,
      CSPStep (e --> P) (ActEvent e) P
  
  (** External choice - left *)
  | CS_ExtChoiceL : forall P Q a P',
      CSPStep P a P' ->
      (a = ActTau \/ a = ActTick \/ exists e, a = ActEvent e) ->
      CSPStep (P [] Q) a (P' [] Q)
  
  (** External choice - right *)
  | CS_ExtChoiceR : forall P Q a Q',
      CSPStep Q a Q' ->
      (a = ActTau \/ a = ActTick \/ exists e, a = ActEvent e) ->
      CSPStep (P [] Q) a (P [] Q')
  
  (** External choice resolve - left *)
  | CS_ExtChoiceResolveL : forall P Q e P',
      CSPStep P (ActEvent e) P' ->
      CSPStep (P [] Q) (ActEvent e) P'
  
  (** External choice resolve - right *)
  | CS_ExtChoiceResolveR : forall P Q e Q',
      CSPStep Q (ActEvent e) Q' ->
      CSPStep (P [] Q) (ActEvent e) Q'
  
  (** Internal choice - left *)
  | CS_IntChoiceL : forall P Q,
      CSPStep (P |~| Q) ActTau P
  
  (** Internal choice - right *)
  | CS_IntChoiceR : forall P Q,
      CSPStep (P |~| Q) ActTau Q
  
  (** Parallel - left *)
  | CS_ParallelL : forall P Q A a P',
      CSPStep P a P' ->
      (forall e, a = ActEvent e -> ~ In e A) ->
      CSPStep (P [| A |] Q) a (P' [| A |] Q)
  
  (** Parallel - right *)
  | CS_ParallelR : forall P Q A a Q',
      CSPStep Q a Q' ->
      (forall e, a = ActEvent e -> ~ In e A) ->
      CSPStep (P [| A |] Q) a (P [| A |] Q')
  
  (** Parallel - synchronize *)
  | CS_ParallelSync : forall P Q A e P' Q',
      In e A ->
      CSPStep P (ActEvent e) P' ->
      CSPStep Q (ActEvent e) Q' ->
      CSPStep (P [| A |] Q) (ActEvent e) (P' [| A |] Q')
  
  (** Hiding - internalize *)
  | CS_Hide : forall P A e P',
      In e A ->
      CSPStep P (ActEvent e) P' ->
      CSPStep (P \ A) ActTau (P' \ A)
  
  (** Hiding - preserve *)
  | CS_HidePreserve : forall P A a P',
      (forall e, a <> ActEvent e) ->
      CSPStep P a P' ->
      CSPStep (P \ A) a (P' \ A)
  
  (** Renaming *)
  | CS_Rename : forall P f e P',
      CSPStep P (ActEvent e) P' ->
      CSPStep (Rename P f) (ActEvent (f e)) (Rename P' f)
  
  (** Termination *)
  | CS_SKIP : CSPStep SKIP ActTick STOP.

(** ** CSP Traces *)

(** A trace is a sequence of events *)
Definition Trace := list Event.

(** Trace semantics - P after s behaves as Q *)
Inductive After : CSP -> Trace -> CSP -> Prop :=
  | After_Nil : forall P, After P [] P
  | After_Cons : forall P e s P' P'',
      CSPStep P (ActEvent e) P' ->
      After P' s P'' ->
      After P (e :: s) P''.

(** P can perform trace s *)
Definition CanTrace (P : CSP) (s : Trace) : Prop :=
  exists P', After P s P'.

(** ** CSP Refinement *)

(** Trace refinement: P [T= Q if traces(P) ⊇ traces(Q) *)
Definition TraceRefinement (P Q : CSP) : Prop :=
  forall s, CanTrace Q s -> CanTrace P s.

Notation "P '[T=' Q" := (TraceRefinement P Q) (at level 70).

(** Refinement is reflexive *)
Theorem trace_reflexive : forall P, P [T= P.
Proof.
  unfold TraceRefinement. auto.
Qed.

(** Refinement is transitive *)
Theorem trace_transitive : forall P Q R,
  P [T= Q -> Q [T= R -> P [T= R.
Proof.
  unfold TraceRefinement. auto.
Qed.

(** ** CSP Algebraic Laws *)

(** External choice is idempotent *)
Lemma ext_choice_idempotent : forall P,
  (P [] P) [T= P /\ P [T= (P [] P).
Proof.
  intros P. split; unfold TraceRefinement; intros s H.
  - (* P [] P [T= P *)
    induction H. exists x. assumption.
  - (* P [T= P [] P *)
    induction H as [P' | P' e s P'' P''' Hstep Hafter IH].
    + exists (P [] P). apply After_Nil.
    + (* P' can do e to P'' *)
      (* Show (P [] P) can simulate P by using left branch *)
      destruct IH as [Q' HQ'].
      exists Q'.
      eapply After_Cons.
      * apply CS_ExtChoiceResolveL. eassumption.
      * eassumption.
Qed.

(** External choice is commutative *)
Theorem ext_choice_comm : forall P Q,
  (P [] Q) [T= (Q [] P).
Proof.
  unfold TraceRefinement. intros P Q s H.
  induction H as [P' | P' e s P'' P''' Hstep Hafter IH].
  - exists P. apply After_Nil.
  - inversion Hstep; subst;
    try (eexists; apply After_Cons; [
      apply CS_ExtChoiceResolveR; eassumption |
      eassumption]);
    try (eexists; apply After_Cons; [
      apply CS_ExtChoiceResolveL; eassumption |
      eassumption]).
Qed.

(** STOP is unit for external choice *)
Theorem ext_choice_unit : forall P,
  (P [] STOP) [T= P /\ P [T= (P [] STOP).
Proof.
  intros P. split; unfold TraceRefinement; intros s H.
  - (* P [] STOP [T= P *)
    induction H as [P' | P' e s P'' P''' Hstep Hafter IH].
    + exists P. apply After_Nil.
    + inversion Hstep; subst; try congruence.
      * (* Left branch *)
        destruct IH as [Q' HQ'].
        exists Q'. apply After_Cons with P''; assumption.
      * (* Right branch - STOP has no transitions *)
        inversion H5.
  - (* P [T= P [] STOP *)
    induction H as [P' | P' e s P'' P''' Hstep Hafter IH].
    + exists (P [] STOP). apply After_Nil.
    + (** P' can do e to P'' *)
      (** Show (P [] STOP) can simulate P *)
      exists (P'' [] STOP).
      apply After_Cons with (P'' [] STOP).
      * apply CS_ExtChoiceResolveL. assumption.
      * assumption.
Qed.

(** Parallel composition is commutative *)
Theorem parallel_comm : forall P Q A,
  (P [| A |] Q) [T= (Q [| A |] P).
Proof.
  unfold TraceRefinement. intros P Q A s H.
  induction H as [P' | P' e s P'' P''' Hstep Hafter IH].
  - exists (Q [| A |] P). apply After_Nil.
  - inversion Hstep; subst.
    + (* Left *)
      eexists. apply After_Cons. 
      apply CS_ParallelR; eauto. eauto.
    + (* Right *)
      eexists. apply After_Cons.
      apply CS_ParallelL; eauto. eauto.
    + (* Sync *)
      eexists. apply After_Cons.
      apply CS_ParallelSync; eauto. eauto.
Qed.

(** ** CSP Determinism *)

(** A process is deterministic if it has no internal choices *)
Fixpoint deterministic (P : CSP) : bool :=
  match P with
  | STOP => true
  | SKIP => true
  | Prefix _ P' => deterministic P'
  | ExtChoice P Q => deterministic P && deterministic Q
  | IntChoice _ _ => false
  | Parallel P _ Q => deterministic P && deterministic Q
  | Hide P _ => deterministic P
  | Rename P _ => deterministic P
  end.

(** Deterministic processes have at most one transition per event *)
Theorem deterministic_unique : forall P e P1 P2,
  deterministic P = true ->
  CSPStep P (ActEvent e) P1 ->
  CSPStep P (ActEvent e) P2 ->
  P1 = P2.
Proof.
  intros P e P1 P2 Hdet H1 H2.
  induction P; try inversion H1; try inversion H2; subst;
  simpl in Hdet; try congruence;
  try (apply andb_true_iff in Hdet; destruct Hdet as [Hdet1 Hdet2];
       eauto).
Qed.

(** ** CSP Deadlock Freedom *)

(** A process is deadlock-free if it can never reach STOP *)
Definition DeadlockFree (P : CSP) : Prop :=
  forall s P', After P s P' -> P' <> STOP.

(** SKIP is deadlock-free *)
Theorem skip_deadlock_free : DeadlockFree SKIP.
Proof.
  unfold DeadlockFree. intros s P' H.
  inversion H; subst.
  - discriminate.
  - inversion H0.
Qed.

(** Prefix preserves deadlock-freedom *)
Theorem prefix_deadlock_free : forall e P,
  DeadlockFree P -> DeadlockFree (e --> P).
Proof.
  unfold DeadlockFree. intros e P H s P' HA.
  inversion HA; subst.
  - discriminate.
  - inversion H0; subst. eapply H. eassumption.
Qed.

(** ** CSP and Traces Theory *)

(** Initial events of a process *)
Fixpoint initials (P : CSP) : list Event :=
  match P with
  | STOP => []
  | SKIP => []
  | Prefix e _ => [e]
  | ExtChoice P Q => list_union (initials P) (initials Q)
  | IntChoice P Q => list_union (initials P) (initials Q)
  | Parallel P A Q => 
      list_union 
        (filter (fun e => if In_nat e A then true else false) 
                (list_union (initials P) (initials Q)))
        (filter (fun e => negb (In_nat e A)) (initials P))
  | Hide P A => filter (fun e => negb (In_nat e A)) (initials P)
  | Rename P f => map f (initials P)
  end.

(* Helper: string equality is decidable *)
Axiom string_dec : forall s1 s2 : string, {s1 = s2} + {s1 <> s2}.

(** Initials are sound: any initial can be performed *)
Theorem initials_sound : forall P e,
  In e (initials P) ->
  exists P', CSPStep P (ActEvent e) P'.
Proof.
  induction P; simpl; intros e Hin;
  try (destruct Hin; try congruence; eauto).
  - (* ExtChoice *)
    apply in_app_or in Hin. destruct Hin; eauto.
  - (* IntChoice *)
    apply in_app_or in Hin. destruct Hin; eauto.
  - (* Parallel *)
    (* Case analysis: event is in synchronization set or not *)
    apply in_app_or in Hin.
    destruct Hin as [Hin | Hin].
    + (* Event is in synchronization set *)
      apply filter_In in Hin.
      destruct Hin as [Hin_union Hin_in_A].
      apply in_app_or in Hin_union.
      destruct Hin_union as [HinP | HinQ].
      * destruct (IHP1 e HinP) as [P' HP'].
        exists (P' [| l |] P2).
        apply CS_ParallelL; auto.
        intros e' Heq. inversion Heq; subst.
        unfold In_nat in Hin_in_A.
        destruct (In_nat e l); discriminate.
      * destruct (IHP2 e HinQ) as [Q' HQ'].
        exists (P1 [| l |] Q').
        apply CS_ParallelR; auto.
        intros e' Heq. inversion Heq; subst.
        unfold In_nat in Hin_in_A.
        destruct (In_nat e l); discriminate.
    + (* Event not in synchronization set *)
      apply filter_In in Hin.
      destruct Hin as [HinP Hin_not_in_A].
      destruct (IHP1 e HinP) as [P' HP'].
      exists (P' [| l |] P2).
      apply CS_ParallelL; auto.
      intros e' Heq. inversion Heq; subst.
      unfold negb, In_nat in Hin_not_in_A.
      destruct (In_nat e l); discriminate.
  - (* Hide *)
    (* Hidden events are not in initials by definition *)
    apply filter_In in Hin.
    destruct Hin as [HinP Hin_not_in_A].
    destruct (IHP e HinP) as [P' HP'].
    exists (P' \ l).
    apply CS_HidePreserve; auto.
    intros e' Heq. inversion Heq; subst.
    unfold negb, In_nat in Hin_not_in_A.
    destruct (In_nat e l); discriminate.
  - (* Rename *)
    (* Renaming preserves performability *)
    apply in_map_iff in Hin.
    destruct Hin as [e' [Heq Hin']].
    destruct (IHP e' Hin') as [P' HP'].
    exists (Rename P' f).
    subst. apply CS_Rename. assumption.
Qed.

(** ** CSP Weak Bisimulation (Simplified) *)

Inductive WeakCSPStep : CSP -> Action -> CSP -> Prop :=
  | WCS_Direct : forall P a P',
      CSPStep P a P' ->
      WeakCSPStep P a P'
  | WCS_TauSeq : forall P P' P'' a,
      CSPStep P ActTau P' ->
      WeakCSPStep P' a P'' ->
      WeakCSPStep P a P''.

(** Weak bisimulation relation *)
Definition WeakBisimulation (R : CSP -> CSP -> Prop) : Prop :=
  forall P Q,
    R P Q ->
    (forall a P',
      CSPStep P a P' ->
      exists Q',
        WeakCSPStep Q a Q' /\ R P' Q') /\n    (forall a Q',
      CSPStep Q a Q' ->
      exists P',
        WeakCSPStep P a P' /\ R P' Q').

(** Weak bisimilarity *)
Inductive WeakBisim : CSP -> CSP -> Prop :=
  | WB_intro : forall R P Q,
      WeakBisimulation R ->
      R P Q ->
      WeakBisim P Q.
