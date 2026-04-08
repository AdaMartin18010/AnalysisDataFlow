(* USTM Foundation: Basic Types *)

Require Import Coq.Strings.String.

(* Identifier types *)
Definition ActorId := nat.
Definition ChannelId := nat.
Definition EventId := nat.
Definition VertexId := nat.

(* Value type *)
Inductive Value : Type :=
  | VUnit : Value
  | VNat : nat -> Value
  | VBool : bool -> Value
  | VString : string -> Value
  | VPair : Value -> Value -> Value
  | VAddress : ActorId -> Value.

(* Timestamp *)
Record Timestamp : Type := {
  event_time : nat;
  ingest_time : nat
}.

Definition mkTimestamp (et it : nat) : Timestamp :=
  {| event_time := et; ingest_time := it |}.

(* Message type *)
Record Message : Type := {
  msg_value : Value;
  msg_timestamp : Timestamp
}.

Definition mkMessage (v : Value) (t : Timestamp) : Message :=
  {| msg_value := v; msg_timestamp := t |}.

(* Finite set representation *)
Definition FinSet (A : Type) := list A.

(* Trace type *)
Definition Trace := list EventId.

(* Stream element for Dataflow *)
Record StreamElement : Type := {
  elem_value : Value;
  elem_timestamp : Timestamp;
  elem_key : nat
}.
