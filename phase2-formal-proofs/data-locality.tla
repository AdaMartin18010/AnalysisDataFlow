------------------------- MODULE DataLocality -------------------------
EXTENDS Naturals
VARIABLES dataPlacement
DataLocality == MinimizeNetworkTransfer(dataPlacement)
=============================================================================
