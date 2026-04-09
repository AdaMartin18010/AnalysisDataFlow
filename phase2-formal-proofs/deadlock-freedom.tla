------------------------- MODULE DeadlockFreedom -------------------------
(* Deadlock Freedom Proof - Task 1-23 *)
EXTENDS Naturals, FiniteSets
CONSTANTS Processes
VARIABLES processStates
NoDeadlock == \E p \in Processes : processStates[p] = "RUNNING"
=============================================================================
