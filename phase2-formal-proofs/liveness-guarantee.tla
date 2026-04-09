------------------------- MODULE LivenessGuarantee -------------------------
(* Liveness Guarantees - Task 1-24 *)
EXTENDS Naturals, Sequences
VARIABLES pendingTasks, completedTasks
Liveness == \A t \in pendingTasks : <> (t \in completedTasks)
=============================================================================
