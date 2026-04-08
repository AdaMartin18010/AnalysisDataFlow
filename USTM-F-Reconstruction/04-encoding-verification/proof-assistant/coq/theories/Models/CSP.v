(* USTM CSP Process Algebra Formalization *)

Require Import Foundation.Types.
Require Import List.
Import ListNotations.

(* CSP Event *)
Inductive Event : Type :=
  | EComm : ChannelId -> Value -> Event
  | ETau : Event.

(* CSP Process *)
Inductive Process : Type :=
  | PStop : Process
  | PSkip : Process
  | PPrefix : Event -> Process -> Process
  | PExternal : Process -> Process -> Process
  | PInternal : Process -> Process -> Process
  | PInterleave : Process -> Process -> Process
  | PParallel : Process -> ChannelId -> Process -> Process
  | PHide : Process -> ChannelId -> Process
  | PSeq : Process -> Process -> Process
  | PIf : bool -> Process -> Process -> Process
  | PRec : (Process -> Process) -> Process.

(* CSP Operational Semantics *)
Inductive CSPStep : Process -> Event -> Process -> Prop :=
  | CSP_Prefix : forall e p,
      CSPStep (PPrefix e p) e p
  
  | CSP_ExtL : forall p1 p2 e p1',
      CSPStep p1 e p1' ->
      CSPStep (PExternal p1 p2) e (PExternal p1' p2)
  
  | CSP_ExtR : forall p1 p2 e p2',
      CSPStep p2 e p2' ->
      CSPStep (PExternal p1 p2) e (PExternal p1 p2')
  
  | CSP_ParSync : forall p1 p2 ch v p1' p2',
      CSPStep p1 (EComm ch v) p1' ->
      CSPStep p2 (EComm ch v) p2' ->
      CSPStep (PParallel p1 ch p2) ETau (PParallel p1' ch p2')
  
  | CSP_ParL : forall p1 p2 ch e p1',
      CSPStep p1 e p1' ->
      (forall v, e <> EComm ch v) ->
      CSPStep (PParallel p1 ch p2) e (PParallel p1' ch p2)
  
  | CSP_ParR : forall p1 p2 ch e p2',
      CSPStep p2 e p2' ->
      (forall v, e <> EComm ch v) ->
      CSPStep (PParallel p1 ch p2) e (PParallel p1 ch p2').

(* CSP Trace *)
Definition CSPTrace := list Event.

(* Weak trace: filter out internal events *)
Fixpoint WeakTrace (tr : CSPTrace) : CSPTrace :=
  match tr with
  | [] => []
  | ETau :: rest => WeakTrace rest
  | e :: rest => e :: WeakTrace rest
  end.

(* Weak bisimulation *)
CoInductive WeakBisim : Process -> Process -> Prop :=
  | WB_intro : forall p1 p2,
      (forall e p1',
        CSPStep p1 e p1' ->
        exists p2',
          CSPStep p2 e p2' /\
          WeakBisim p1' p2') ->
      (forall e p2',
        CSPStep p2 e p2' ->
        exists p1',
          CSPStep p1 e p1' /\
          WeakBisim p1' p2') ->
      WeakBisim p1 p2.
