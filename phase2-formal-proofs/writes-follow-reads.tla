------------------------- MODULE WritesFollowReads -------------------------
EXTENDS Naturals
VARIABLES writes, reads
WritesFollowReads == \A r \in reads, w \in writes : r -> w => w.sees(r)
=============================================================================
