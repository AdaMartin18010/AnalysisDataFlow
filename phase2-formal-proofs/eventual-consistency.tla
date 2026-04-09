------------------------- MODULE EventualConsistency -------------------------
EXTENDS Naturals
VARIABLES replicas
EventualConsistency == <> (\A r1, r2 \in replicas : r1.state = r2.state)
=============================================================================
