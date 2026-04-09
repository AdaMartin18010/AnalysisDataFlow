------------------------- MODULE TypeSafety -------------------------
(* Type Safety in Stream Processing - Task 1-21 *)
EXTENDS Naturals, Sequences
CONSTANTS Types, Values
VARIABLES typeEnv, dataFlow
TypeSafe == \A d \in dataFlow : d.type \in Types
=============================================================================
