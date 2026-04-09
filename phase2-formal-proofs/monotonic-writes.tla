------------------------- MODULE MonotonicWrites -------------------------
EXTENDS Naturals
VARIABLES writes
MonotonicWrites == \A w1, w2 \in writes : w1 -> w2 => w1.timestamp <= w2.timestamp
=============================================================================
