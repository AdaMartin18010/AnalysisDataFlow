------------------------- MODULE MonotonicReads -------------------------
EXTENDS Naturals
VARIABLES reads
MonotonicReads == \A r1, r2 \in reads : r1 -> r2 => r1.value <= r2.value
=============================================================================
