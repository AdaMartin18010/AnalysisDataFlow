------------------------- MODULE CausalConsistency -------------------------
EXTENDS Naturals
VARIABLES events
CausalConsistency == \A e1, e2 \in events : HappensBefore(e1, e2) => OrderPreserved(e1, e2)
=============================================================================
