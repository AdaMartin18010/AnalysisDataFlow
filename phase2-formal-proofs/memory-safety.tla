------------------------- MODULE MemorySafety -------------------------
(* Memory Safety Guarantees - Task 1-22 *)
EXTENDS Naturals
CONSTANTS MaxMemory
VARIABLES memoryUsage, allocations
MemorySafe == memoryUsage <= MaxMemory
=============================================================================
