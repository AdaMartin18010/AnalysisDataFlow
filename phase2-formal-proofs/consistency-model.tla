------------------------- MODULE ConsistencyModel -------------------------
EXTENDS Naturals
CONSTANTS Operations
VARIABLES operationOrder
Consistency == \A o1, o2 \in Operations : o1 -> o2 => OrderPreserved(o1, o2)
=============================================================================
