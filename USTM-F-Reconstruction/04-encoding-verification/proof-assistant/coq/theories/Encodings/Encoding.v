(* USTM Encoding Theory *)

Require Import Models.Actor.
Require Import Models.CSP.

(* Encoding function type *)
Definition Encoding (S T : Type) := S -> T.

(* Syntax preservation *)
Definition SyntaxPreserving {S T : Type} 
  (WF_S : S -> Prop) (WF_T : T -> Prop)
  (encode : Encoding S T) : Prop :=
  forall s, WF_S s -> WF_T (encode s).

(* Semantics preservation *)
Definition SemanticsPreserving 
  {S T Trace_S Trace_T : Type}
  (sem_S : S -> Trace_S -> Prop)
  (sem_T : T -> Trace_T -> Prop)
  (trace_map : Trace_S -> Trace_T)
  (encode : Encoding S T) : Prop :=
  forall s tr_S,
    sem_S s tr_S ->
    sem_T (encode s) (trace_map tr_S).

(* Compositionality *)
Definition Compositional {S T Comp_S Comp_T : Type}
  (compose_S : Comp_S -> Comp_S -> S)
  (compose_T : Comp_T -> Comp_T -> T)
  (ctx : T -> T -> T)
  (encode : Encoding S T)
  (encode_comp : Encoding Comp_S Comp_T) : Prop :=
  forall c1 c2,
    encode (compose_S c1 c2) = 
    ctx (encode_comp c1) (encode_comp c2).

(* Valid encoding record *)
Record ValidEncoding {S T : Type} := {
  encode : Encoding S T;
  WF_S : S -> Prop;
  WF_T : T -> Prop;
  syntax_preserving : SyntaxPreserving WF_S WF_T encode
}.
