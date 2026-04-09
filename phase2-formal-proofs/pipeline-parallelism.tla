------------------------- MODULE PipelineParallelism -------------------------
EXTENDS Naturals
VARIABLES pipelineStages
PipelineParallelism == \A s1, s2 \in pipelineStages : CanExecuteInParallel(s1, s2) => OutputCorrect
=============================================================================
