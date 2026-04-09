(* ============================================================================ *)
(* CEP Pattern Matching Correctness Specification - Phase 2 Task 1-5          *)
(* ============================================================================ *)
(* This TLA+ specification models the correctness of Complex Event Processing *)
(* pattern matching in stream processing systems.                             *)
(* ============================================================================ *)

---------------------------- MODULE CEPPatternMatching ------------------------

EXTENDS Naturals, Sequences, FiniteSets, TLC

(* ============================================================================ *)
(* Type Definitions                                                           *)
(* ============================================================================ *)

(* Event types *)
EventType == {"ORDER", "PAYMENT", "SHIPMENT", "DELIVERY", "CANCEL"}

(* Event record *)
Event == [type: EventType, timestamp: Nat, orderId: Nat, amount: Nat]

(* Pattern operators *)
PatternOp == {"SEQUENCE", "AND", "OR", "NOT", "TIMES", "FOLLOWED_BY"}

(* Pattern definition *)
Pattern == [
    op: PatternOp,
    events: SUBSET EventType,
    times: Nat,          (* For TIMES operator *)
    within: Nat          (* Time window in seconds *)
]

(* Match result *)
MatchResult == [matched: BOOLEAN, events: SUBSET Event, timestamp: Nat]

(* ============================================================================ *)
(* State Variables                                                            *)
(* ============================================================================ *)

VARIABLES 
    eventStream,      (* Incoming event stream *)
    patternDef,       (* Current pattern definition *)
    buffer,           (* Event buffer for pattern matching *)
    matches,          (* Successful pattern matches *)
    clock             (* System clock *)

(* ============================================================================ *)
(* Initial State                                                              *)
(* ============================================================================ *)

Init ==
    /\ eventStream = <<>>
    /\ patternDef = [op |-> "SEQUENCE", events |-> {"ORDER", "PAYMENT"}, times |-> 1, within |-> 3600]
    /\ buffer = {}
    /\ matches = {}
    /\ clock = 0

(* ============================================================================ *)
(* Helper Operators                                                           *)
(* ============================================================================ *)

(* Check if event matches pattern element *)
MatchesEvent(e, eventType) == e.type = eventType

(* Check if all events in buffer match pattern within time window *)
CheckSequencePattern(buff, pattern) ==
    LET ordered == SelectSeq(SortSeq(buff, LAMBDA e1, e2: e1.timestamp < e2.timestamp),
                            LAMBDA e: e.type \in pattern.events)
    IN 
        /\ Len(ordered) = Cardinality(pattern.events)
        /\ \A i \in 1..Len(ordered)-1: ordered[i].timestamp <= ordered[i+1].timestamp
        /\ (ordered[Len(ordered)].timestamp - ordered[1].timestamp) <= pattern.within

(* Check AND pattern - all event types present *)
CheckAndPattern(buff, pattern) ==
    /\ Cardinality(buff) = Cardinality(pattern.events)
    /\ {e.type: e \in buff} = pattern.events
    /\ \E minTs, maxTs \in Nat:
        /\ minTs = Min({e.timestamp: e \in buff})
        /\ maxTs = Max({e.timestamp: e \in buff})
        /\ maxTs - minTs <= pattern.within

(* Check TIMES pattern - same event type repeats N times *)
CheckTimesPattern(buff, pattern) ==
    /\ Cardinality(buff) = pattern.times
    /\ \A e1, e2 \in buff: e1.type = e2.type
    /\ \E minTs, maxTs \in Nat:
        /\ minTs = Min({e.timestamp: e \in buff})
        /\ maxTs = Max({e.timestamp: e \in buff})
        /\ maxTs - minTs <= pattern.within

(* Generic pattern check *)
CheckPattern(buff, pattern) ==
    CASE pattern.op = "SEQUENCE" -> CheckSequencePattern(buff, pattern)
    [] pattern.op = "AND" -> CheckAndPattern(buff, pattern)
    [] pattern.op = "TIMES" -> CheckTimesPattern(buff, pattern)
    [] OTHER -> FALSE

(* ============================================================================ *)
(* Actions                                                                    *)
(* ============================================================================ *)

(* Receive new event *)
ReceiveEvent ==
    /\ eventStream' = Append(eventStream, [type |-> "ORDER", timestamp |-> clock, orderId |-> Len(eventStream), amount |-> 100])
    /\ clock' = clock + 1
    /\ UNCHANGED <<patternDef, buffer, matches>>

(* Add event to buffer *)
BufferEvent(e) ==
    /\ buffer' = buffer \cup {e}
    /\ UNCHANGED <<eventStream, patternDef, matches, clock>>

(* Try to match pattern *)
TryMatch ==
    /\ CheckPattern(buffer, patternDef)
    /\ matches' = matches \cup {[events |-> buffer, timestamp |-> clock]}
    /\ buffer' = {}  (* Clear buffer after match *)
    /\ UNCHANGED <<eventStream, patternDef, clock>>

(* Clear old events from buffer *)
ExpireOldEvents ==
    /\ buffer' = {e \in buffer: clock - e.timestamp <= patternDef.within}
    /\ UNCHANGED <<eventStream, patternDef, matches, clock>>

(* Change pattern definition *)
ChangePattern(newPattern) ==
    /\ patternDef' = newPattern
    /\ buffer' = {}  (* Clear buffer when pattern changes *)
    /\ UNCHANGED <<eventStream, matches, clock>>

(* ============================================================================ *)
(* Next State Relation                                                        *)
(* ============================================================================ *)

Next ==
    \/ ReceiveEvent
    \/ \E e \in Event: BufferEvent(e)
    \/ TryMatch
    \/ ExpireOldEvents
    \/ \E newPattern \in Pattern: ChangePattern(newPattern)

(* ============================================================================ *)
(* Specification                                                              *)
(* ============================================================================ *)

Spec == Init /\ [][Next]_<<eventStream, patternDef, buffer, matches, clock>>

(* ============================================================================ *)
(* Invariants                                                                 *)
(* ============================================================================ *)

(* Type invariant *)
TypeInvariant ==
    /\ eventStream \in Seq(Event)
    /\ patternDef \in Pattern
    /\ buffer \in SUBSET Event
    /\ matches \in SUBSET MatchResult
    /\ clock \in Nat

(* Buffer size invariant - should not grow unbounded *)
BufferSizeInvariant ==
    Cardinality(buffer) <= Cardinality(patternDef.events) * 2

(* Match correctness invariant *)
MatchCorrectness ==
    \A match \in matches:
        /\ match.matched = TRUE
        /\ CheckPattern(match.events, patternDef)
        /\ match.timestamp >= Max({e.timestamp: e \in match.events})

(* No duplicate matches invariant *)
NoDuplicateMatches ==
    \A m1, m2 \in matches:
        m1.events = m2.events => m1 = m2

(* ============================================================================ *)
(* Properties                                                                 *)
(* ============================================================================ *)

(* Liveness: If pattern exists in event stream, it will eventually be matched *)
PatternEventuallyMatched ==
    \A possibleMatch \in SUBSET Event:
        CheckPattern(possibleMatch, patternDef) ~>
            \E match \in matches: match.events = possibleMatch

(* Safety: Only valid patterns are matched *)
OnlyValidPatternsMatched ==
    \A match \in matches: CheckPattern(match.events, patternDef)

(* Fairness: Events are eventually processed *)
EventProcessingFairness ==
    \A e \in Event:
        (e \in buffer) ~> (e \in matches.events \/ e \notin buffer)

(* ============================================================================ *)
(* Theorems                                                                   *)
(* ============================================================================ *)

THEOREM TypeCorrectness ==
    Spec => []TypeInvariant

THEOREM BufferBounded ==
    Spec => []BufferSizeInvariant

THEOREM Correctness ==
    Spec => []MatchCorrectness

THEOREM Uniqueness ==
    Spec => []NoDuplicateMatches

================================================================================
(* End of CEPPatternMatching.tla - Phase 2                                    *)
================================================================================
