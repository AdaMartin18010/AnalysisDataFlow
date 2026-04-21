# Exercise: TLA+ Practice

> **Language**: English | **Source**: [Knowledge/98-exercises/exercise-06-tla-practice.md](../Knowledge/98-exercises/exercise-06-tla-practice.md) | **Last Updated**: 2026-04-21

---

## Learning Objectives

After completing this exercise, you will be able to:

- **Def-K-06-EN-01**: Master basic TLA+ specification syntax
- **Def-K-06-EN-02**: Model concurrent systems with TLA+
- **Def-K-06-EN-03**: Verify system properties with TLC model checker
- **Def-K-06-EN-04**: Use TLAPS for formal proofs

## TLA+ Core Syntax

| TLA+ Notation | Meaning | Example |
|--------------|---------|---------|
| `[]P` | Always P | `[]x >= 0` (x always non-negative) |
| `<>P` | Eventually P | `<>Terminated` (will terminate) |
| `P ~> Q` | P leads to Q | `Request ~> Response` |
| `WF_vars(A)` | Weak fairness | `WF_chan(Send)` |
| `SF_vars(A)` | Strong fairness | `SF_proc(Schedule)` |

## PlusCal Template

```tla
(*--algorithm Example
variables x = 0;

process Proc \in {1, 2}
begin
L1: x := x + 1;
L2: assert x <= 2;
end process;

end algorithm;*)
```

## Exercise 1: Two-Phase Commit (TPC)

Model a simplified TPC with one coordinator and two participants:

```tla
MODULE TwoPhaseCommit

CONSTANTS Participants

VARIABLES
  coordState,    (* "init", "prepare", "commit", "abort" *)
  participantState,  (* [p \in Participants |-> "working"] *)
  votes            (* [p \in Participants |-> "none"] *)

Init ==
  /\ coordState = "init"
  /\ participantState = [p \in Participants |-> "working"]
  /\ votes = [p \in Participants |-> "none"]

Prepare ==
  /\ coordState = "init"
  /\ coordState' = "prepare"
  /\ UNCHANGED <<participantState, votes>>

Vote(p) ==
  /\ coordState = "prepare"
  /\ participantState[p] = "working"
  /\ votes' = [votes EXCEPT ![p] = "yes"]
  /\ participantState' = [participantState EXCEPT ![p] = "prepared"]
  /\ UNCHANGED coordState

Commit ==
  /\ coordState = "prepare"
  /\ \A p \in Participants : votes[p] = "yes"
  /\ coordState' = "commit"
  /\ participantState' = [p \in Participants |-> "committed"]
  /\ UNCHANGED votes

Next == Prepare \/ \E p \in Participants : Vote(p) \/ Commit

Spec == Init /\ [][Next]_vars /\ WF_vars(Next)

Consistency ==
  [](coordState = "commit" =>
     \A p \in Participants : participantState[p] = "committed")
```

## Exercise 2: Flink Checkpoint Modeling

Key aspects to model:

- Barrier injection and alignment
- State snapshotting
- Recovery from checkpoint

```tla
MODULE FlinkCheckpoint

VARIABLES
  barriers,      (* set of injected barriers *)
  operatorState, (* map of operator -> state *)
  checkpointId   (* current checkpoint ID *)

InjectBarrier ==
  /\ checkpointId' = checkpointId + 1
  /\ barriers' = barriers \union {checkpointId'}
  /\ UNCHANGED operatorState

AlignAndSnapshot ==
  /\ \E b \in barriers :
      /\ operatorState' = [operatorState EXCEPT !["op1"] = @ + 1]
      /\ barriers' = barriers \\ {b}
  /\ UNCHANGED checkpointId

Spec == Init /\ [][InjectBarrier \/ AlignAndSnapshot]_vars
```

## TLC Model Checker Usage

```bash
# 1. Translate PlusCal to TLA+
java -cp tla2tools.jar pcal.trans MySpec.tla

# 2. Run TLC
java -cp tla2tools.jar tlc2.TLC MySpec.tla

# 3. Check specific invariant
java -cp tla2tools.jar tlc2.TLC -config MySpec.cfg MySpec.tla
```

## References
