(* USTM Actor Model Formalization *)

Require Import Foundation.Types.
Require Import List.
Import ListNotations.

(* Actor Behavior *)
Inductive Behavior : Type :=
  | BSend : ActorId -> Value -> Behavior -> Behavior
  | BReceive : (Message -> option Behavior) -> Behavior
  | BBecome : Behavior -> Behavior
  | BSpawn : Behavior -> (ActorId -> Behavior) -> Behavior
  | BSelf : (ActorId -> Behavior) -> Behavior
  | BStop : Behavior.

(* Actor Configuration *)
Record ActorConfig : Type := {
  actors : list ActorId;
  mailboxes : ActorId -> list Message;
  behaviors : ActorId -> Behavior;
  addresses : ActorId -> ActorId;
  supervision : list (ActorId * ActorId)
}.

(* Actor Transition *)
Inductive ActorStep : ActorConfig -> ActorConfig -> Prop :=
  | StepSend : forall cfg from to val beh,
      behaviors cfg from = BSend to val beh ->
      ActorStep cfg 
        {| actors := actors cfg;
           mailboxes := fun a => 
             if Nat.eqb a to 
             then mkMessage val (mkTimestamp 0 0) :: (mailboxes cfg to)
             else mailboxes cfg a;
           behaviors := fun a => 
             if Nat.eqb a from then beh else behaviors cfg a;
           addresses := addresses cfg;
           supervision := supervision cfg |}
  
  | StepReceive : forall cfg actor msg matcher cont msgs,
      mailboxes cfg actor = msg :: msgs ->
      behaviors cfg actor = BReceive matcher ->
      matcher msg = Some cont ->
      ActorStep cfg
        {| actors := actors cfg;
           mailboxes := fun a => 
             if Nat.eqb a actor then msgs else mailboxes cfg a;
           behaviors := fun a => 
             if Nat.eqb a actor then cont else behaviors cfg a;
           addresses := addresses cfg;
           supervision := supervision cfg |}.

(* Reflexive transitive closure *)
Inductive ActorStepStar : ActorConfig -> ActorConfig -> Prop :=
  | AS_Refl : forall cfg, ActorStepStar cfg cfg
  | AS_Trans : forall cfg1 cfg2 cfg3,
      ActorStep cfg1 cfg2 ->
      ActorStepStar cfg2 cfg3 ->
      ActorStepStar cfg1 cfg3.

(* Restricted Actor: No dynamic address passing *)
Definition RestrictedActor (cfg : ActorConfig) : Prop :=
  forall actor msg,
    In actor (actors cfg) ->
    In msg (mailboxes cfg actor) ->
    match msg_value msg with
    | VAddress _ => False
    | _ => True
    end.

(* Actor Trace *)
Inductive ActorTrace : ActorConfig -> list EventId -> Prop :=
  | TNil : forall cfg, ActorTrace cfg []
  | TCons : forall cfg1 cfg2 tr ev,
      ActorStep cfg1 cfg2 ->
      ActorTrace cfg2 tr ->
      ActorTrace cfg1 (ev :: tr).
