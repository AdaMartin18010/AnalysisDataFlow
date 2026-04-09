------------------------- MODULE SessionConsistency -------------------------
EXTENDS Naturals
VARIABLES sessionOps
SessionConsistency == \A s1, s2 \in sessionOps : SameSession(s1, s2) => OrderPreserved(s1, s2)
=============================================================================
