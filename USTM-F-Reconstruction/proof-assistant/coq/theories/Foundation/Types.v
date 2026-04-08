(** * Foundation Types for USTM-F
    
    This module defines the foundational types and utilities used throughout
    the USTM-F (Unified Streaming Theory Meta-Framework) formalization.
*)

Require Import Coq.Arith.Arith.
Require Import Coq.Lists.List.
Require Import Coq.Strings.String.
Require Import Coq.Logic.FunctionalExtensionality.
Require Import Coq.Program.Equality.

Import ListNotations.

(** ** Basic Type Definitions *)

(** Actor identifier *)
Definition ActorId := nat.

(** Channel identifier *)
Definition ChannelId := nat.

(** Message type - can be extended with more variants *)
Inductive Message : Type :=
  | M_Nat : nat -> Message
  | M_Bool : bool -> Message
  | M_Pair : Message -> Message -> Message
  | M_Nil : Message.

(** Event timestamp *)
Definition Timestamp := nat.

(** Event identifier *)
Definition EventId := nat.

(** ** Utility Functions *)

(** Boolean equality for messages *)
Fixpoint message_eq (m1 m2 : Message) : bool :=
  match m1, m2 with
  | M_Nat n1, M_Nat n2 => Nat.eqb n1 n2
  | M_Bool b1, M_Bool b2 => Bool.eqb b1 b2
  | M_Pair a1 b1, M_Pair a2 b2 => message_eq a1 a2 && message_eq b1 b2
  | M_Nil, M_Nil => true
  | _, _ => false
  end.

(** Message equality is reflexive *)
Lemma message_eq_refl : forall m, message_eq m m = true.
Proof.
  induction m; simpl;
  try reflexivity;
  try (apply Nat.eqb_refl);
  try (rewrite IHm1, IHm2; reflexivity).
Qed.

(** ** Finite Set Utilities *)

(** Check if an element is in a list *)
Fixpoint In_nat (n : nat) (l : list nat) : bool :=
  match l with
  | [] => false
  | x :: xs => if Nat.eqb x n then true else In_nat n xs
  end.

(** Remove duplicates from a list of naturals *)
Fixpoint remove_dups (l : list nat) : list nat :=
  match l with
  | [] => []
  | x :: xs => if In_nat x xs then remove_dups xs else x :: remove_dups xs
  end.

(** List union *)
Fixpoint list_union (l1 l2 : list nat) : list nat :=
  match l1 with
  | [] => l2
  | x :: xs => if In_nat x l2 then list_union xs l2 else x :: list_union xs l2
  end.

(** ** Option Monad Utilities *)

Definition bind_option {A B : Type} (x : option A) (f : A -> option B) : option B :=
  match x with
  | Some a => f a
  | None => None
  end.

Notation "x >>= f" := (bind_option x f) (at level 50, left associativity).

Definition pure_option {A : Type} (x : A) : option A := Some x.

(** ** Result Type for Error Handling *)

Inductive Result (A E : Type) : Type :=
  | Ok : A -> Result A E
  | Err : E -> Result A E.

Arguments Ok {A E} _.
Arguments Err {A E} _.

(** ** Relation Definitions *)

Definition relation (A : Type) := A -> A -> Prop.

(** Reflexive closure *)
Inductive refl_clos {A : Type} (R : relation A) : relation A :=
  | R_step : forall x y, R x y -> refl_clos R x y
  | R_refl : forall x, refl_clos R x x.

(** Transitive closure *)
Inductive trans_clos {A : Type} (R : relation A) : relation A :=
  | T_step : forall x y, R x y -> trans_clos R x y
  | T_trans : forall x y z, R x y -> trans_clos R y z -> trans_clos R x z.

(** Reflexive-transitive closure *)
Inductive rt_clos {A : Type} (R : relation A) : relation A :=
  | RT_refl : forall x, rt_clos R x x
  | RT_step : forall x y z, R x y -> rt_clos R y z -> rt_clos R x z.

(** ** Decidable Equality Typeclass *)

Class DecidableEq (A : Type) := {
  dec_eq : forall x y : A, {x = y} + {x <> y}
}.

Instance DecidableEq_nat : DecidableEq nat := {
  dec_eq := Nat.eq_dec
}.

Instance DecidableEq_bool : DecidableEq bool := {
  dec_eq := bool_dec
}.

(** ** Basic Properties *)

Lemma rt_clos_trans : forall {A} (R : relation A) x y z,
  rt_clos R x y -> rt_clos R y z -> rt_clos R x z.
Proof.
  intros A R x y z Hxy Hyz.
  induction Hxy.
  - assumption.
  - apply RT_step with y0; auto.
Qed.

Lemma trans_clos_implies_rt_clos : forall {A} (R : relation A) x y,
  trans_clos R x y -> rt_clos R x y.
Proof.
  intros A R x y H.
  induction H.
  - apply RT_step with y; [assumption | apply RT_refl].
  - eapply rt_clos_trans; eauto.
    apply RT_step with y; [assumption | apply RT_refl].
Qed.

(** ** Notations *)

Notation "x == y" := (dec_eq x y) (at level 70).
Notation "[ 'list' ]" := (@nil _) (format "[ 'list' ]") : list_scope.
