------------------------- MODULE Linearizability -------------------------
EXTENDS Naturals
VARIABLES operations
Linearizability == \E linearizationPoint : ConsistentWithRealTime(operations, linearizationPoint)
=============================================================================
