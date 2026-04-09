------------------------- MODULE PricingConsistency -------------------------
EXTENDS Naturals
VARIABLES prices
PricingConsistency == \A p1, p2 \in prices : SameProduct(p1, p2) => p1.value = p2.value
=============================================================================
