------------------------- MODULE SequentialConsistency -------------------------
EXTENDS Naturals
VARIABLES operations
SequentialConsistency == \E seq : IsSequential(seq) /\ Equivalent(operations, seq)
=============================================================================
