------------------------- MODULE ReadYourWrites -------------------------
EXTENDS Naturals
VARIABLES writes, reads
ReadYourWrites == \A w \in writes, r \in reads : SameClient(w, r) => r.sees(w)
=============================================================================
