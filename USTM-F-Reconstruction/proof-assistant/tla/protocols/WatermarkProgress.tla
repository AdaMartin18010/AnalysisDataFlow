------------------------------ MODULE WatermarkProgress ------------------------------
(*
 * WatermarkProgress - Flink Watermark进展性TLA+规约
 * 版本: 1.0.0
 *)

EXTENDS Integers, Sequences, FiniteSets, Naturals, TLC

CONSTANTS
    Sources,
    Tasks,
    MaxTimestamp,
    IdleTimeout

ASSUME
    /\ Sources # {}
    /\ IsFiniteSet(Sources)
    /\ Tasks # {}
    /\ IsFiniteSet(Tasks)
    /\ MaxTimestamp \in Nat /\ MaxTimestamp > 0
    /\ IdleTimeout \in Nat /\ IdleTimeout > 0

Source == Sources
Task == Tasks
Timestamp == 0..MaxTimestamp
EventTimestamp == 1..MaxTimestamp
WatermarkValue == -1..MaxTimestamp

VARIABLES
    sourceTimestamps,
    sourceWatermarks,
    sourceActive,
    sourceLastActivity,
    taskInputWatermarks,
    taskOutputWatermarks,
    taskPendingEvents,
    globalWatermark,
    watermarkHistory,
    processedEvents,
    globalClock

MinWatermark(wmarks) ==
    LET ActiveMarks == {wmarks[s] : s \in DOMAIN wmarks /\ wmarks[s] # -1}
    IN IF ActiveMarks = {} THEN MaxTimestamp
       ELSE CHOOSE w \in ActiveMarks : \A w2 \in ActiveMarks : w <= w2

IsSourceIdle(s) ==
    sourceActive[s] = FALSE \/ globalClock - sourceLastActivity[s] > IdleTimeout

IsMonotonic(history) ==
    \A i, j \in 1..Len(history) : i < j => history[i] <= history[j]

TaskInputWatermark(task) ==
    MinWatermark(taskInputWatermarks[task])

CanProcessEvent(task, eventTime) ==
    eventTime <= taskOutputWatermarks[task]

Init ==
    /\ sourceTimestamps = [s \in Source |-> 0]
    /\ sourceWatermarks = [s \in Source |-> 0]
    /\ sourceActive = [s \in Source |-> TRUE]
    /\ sourceLastActivity = [s \in Source |-> 0]
    /\ taskInputWatermarks = [t \in Task |-> [s \in Source |-> -1]]
    /\ taskOutputWatermarks = [t \in Task |-> -1]
    /\ taskPendingEvents = [t \in Task |-> <<>>]
    /\ globalWatermark = -1
    /\ watermarkHistory = <<>>
    /\ processedEvents = {}
    /\ globalClock = 0

SourceGenerateEvent(s, ts) ==
    /\ s \in Source
    /\ ts \in EventTimestamp
    /\ ts > sourceTimestamps[s]
    /\ sourceActive[s] = TRUE
    /\ sourceTimestamps' = [sourceTimestamps EXCEPT ![s] = ts]
    /\ sourceLastActivity' = [sourceLastActivity EXCEPT ![s] = globalClock]
    /\ UNCHANGED <<sourceWatermarks, sourceActive, taskInputWatermarks,
                   taskOutputWatermarks, taskPendingEvents, globalWatermark,
                   watermarkHistory, processedEvents, globalClock>>

SourceEmitWatermark(s, wm) ==
    /\ s \in Source
    /\ wm \in WatermarkValue
    /\ wm >= sourceWatermarks[s]
    /\ wm <= sourceTimestamps[s]
    /\ sourceActive[s] = TRUE
    /\ sourceWatermarks' = [sourceWatermarks EXCEPT ![s] = wm]
    /\ sourceLastActivity' = [sourceLastActivity EXCEPT ![s] = globalClock]
    /\ UNCHANGED <<sourceTimestamps, sourceActive, taskInputWatermarks,
                   taskOutputWatermarks, taskPendingEvents, globalWatermark,
                   watermarkHistory, processedEvents, globalClock>>

SourceBecomeIdle(s) ==
    /\ s \in Source
    /\ globalClock - sourceLastActivity[s] > IdleTimeout
    /\ sourceActive' = [sourceActive EXCEPT ![s] = FALSE]
    /\ sourceWatermarks' = [sourceWatermarks EXCEPT ![s] = MaxTimestamp]
    /\ UNCHANGED <<sourceTimestamps, sourceLastActivity, taskInputWatermarks,
                   taskOutputWatermarks, taskPendingEvents, globalWatermark,
                   watermarkHistory, processedEvents, globalClock>>

SourceReactivate(s) ==
    /\ s \in Source
    /\ sourceActive[s] = FALSE
    /\ sourceActive' = [sourceActive EXCEPT ![s] = TRUE]
    /\ sourceWatermarks' = [sourceWatermarks EXCEPT ![s] = 0]
    /\ sourceLastActivity' = [sourceLastActivity EXCEPT ![s] = globalClock]
    /\ UNCHANGED <<sourceTimestamps, taskInputWatermarks,
                   taskOutputWatermarks, taskPendingEvents, globalWatermark,
                   watermarkHistory, processedEvents, globalClock>>

TaskReceiveWatermark(t, s, wm) ==
    /\ t \in Task
    /\ s \in Source
    /\ wm \in WatermarkValue
    /\ taskInputWatermarks[t][s] <= wm
    /\ taskInputWatermarks' = [taskInputWatermarks EXCEPT ![t] = 
                              [@ EXCEPT ![s] = wm]]
    /\ UNCHANGED <<sourceTimestamps, sourceWatermarks, sourceActive,
                   sourceLastActivity, taskOutputWatermarks, taskPendingEvents,
                   globalWatermark, watermarkHistory, processedEvents, globalClock>>

TaskUpdateOutputWatermark(t) ==
    /\ t \in Task
    /\ LET newWm == TaskInputWatermark(t)
       IN /\ newWm # -1
          /\ newWm >= taskOutputWatermarks[t]
          /\ taskOutputWatermarks' = [taskOutputWatermarks EXCEPT ![t] = newWm]
    /\ UNCHANGED <<sourceTimestamps, sourceWatermarks, sourceActive,
                   sourceLastActivity, taskInputWatermarks, taskPendingEvents,
                   globalWatermark, watermarkHistory, processedEvents, globalClock>>

TaskReceiveEvent(t, event) ==
    /\ t \in Task
    /\ event \in [timestamp: EventTimestamp, data: Nat]
    /\ taskPendingEvents' = [taskPendingEvents EXCEPT ![t] = 
                            Append(@, event)]
    /\ UNCHANGED <<sourceTimestamps, sourceWatermarks, sourceActive,
                   sourceLastActivity, taskInputWatermarks, taskOutputWatermarks,
                   globalWatermark, watermarkHistory, processedEvents, globalClock>>

TaskProcessEvent(t) ==
    /\ t \in Task
    /\ Len(taskPendingEvents[t]) > 0
    /\ LET event == taskPendingEvents[t][1]
       IN /\ CanProcessEvent(t, event.timestamp)
          /\ processedEvents' = processedEvents \union {event}
          /\ taskPendingEvents' = [taskPendingEvents EXCEPT ![t] = 
                                  [i \in 1..(Len(@)-1) |-> @[i+1]]]
    /\ UNCHANGED <<sourceTimestamps, sourceWatermarks, sourceActive,
                   sourceLastActivity, taskInputWatermarks, taskOutputWatermarks,
                   globalWatermark, watermarkHistory, globalClock>>

UpdateGlobalWatermark ==
    /\ LET allOutputWms == {taskOutputWatermarks[t] : t \in Task /\ taskOutputWatermarks[t] # -1}
       IN /\ allOutputWms # {}
          /\ LET newGlobal == CHOOSE w \in allOutputWms : 
                             \A w2 \in allOutputWms : w <= w2
             IN /\ newGlobal >= globalWatermark
                /\ globalWatermark' = newGlobal
                /\ watermarkHistory' = Append(watermarkHistory, newGlobal)
    /\ UNCHANGED <<sourceTimestamps, sourceWatermarks, sourceActive,
                   sourceLastActivity, taskInputWatermarks, taskOutputWatermarks,
                   taskPendingEvents, processedEvents, globalClock>>

AdvanceTime ==
    /\ globalClock' = globalClock + 1
    /\ UNCHANGED <<sourceTimestamps, sourceWatermarks, sourceActive,
                   sourceLastActivity, taskInputWatermarks, taskOutputWatermarks,
                   taskPendingEvents, globalWatermark, watermarkHistory,
                   processedEvents>>

Next ==
    \/ \E s \in Source, ts \in EventTimestamp : SourceGenerateEvent(s, ts)
    \/ \E s \in Source, wm \in WatermarkValue : SourceEmitWatermark(s, wm)
    \/ \E s \in Source : SourceBecomeIdle(s)
    \/ \E s \in Source : SourceReactivate(s)
    \/ \E t \in Task, s \in Source, wm \in WatermarkValue : 
        TaskReceiveWatermark(t, s, wm)
    \/ \E t \in Task : TaskUpdateOutputWatermark(t)
    \/ \E t \in Task : \E event \in [timestamp: EventTimestamp, data: Nat] :
        TaskReceiveEvent(t, event)
    \/ \E t \in Task : TaskProcessEvent(t)
    \/ UpdateGlobalWatermark
    \/ AdvanceTime

Fairness ==
    /\ WF_vars(AdvanceTime)
    /\ \A t \in Task : WF_vars(TaskUpdateOutputWatermark(t))
    /\ WF_vars(UpdateGlobalWatermark)
    /\ \A s \in Source : WF_vars(SourceEmitWatermark(s, MaxTimestamp))

Spec == Init /\ [][Next]_vars /\ Fairness

TypeInvariant ==
    /\ sourceTimestamps \in [Source -> Nat]
    /\ sourceWatermarks \in [Source -> WatermarkValue]
    /\ sourceActive \in [Source -> BOOLEAN]
    /\ taskOutputWatermarks \in [Task -> WatermarkValue]
    /\ globalWatermark \in WatermarkValue
    /\ watermarkHistory \in Seq(Nat)

SourceWatermarkMonotonicity ==
    \A s \in Source :
        \A i, j \in 1..Len(watermarkHistory) :
            i < j => sourceWatermarks[s] >= 0 => TRUE

TaskWatermarkMonotonicity ==
    \A t \in Task, s \in Source :
        taskInputWatermarks[t][s] <= taskOutputWatermarks[t] \/ 
        taskOutputWatermarks[t] = -1

GlobalWatermarkIsMinimum ==
    globalWatermark = -1 \/ 
    (globalWatermark = MinWatermark(taskOutputWatermarks))

EventTimeIntegrity ==
    \A t \in Task, i \in 1..Len(taskPendingEvents[t]) :
        taskOutputWatermarks[t] <= taskPendingEvents[t][i].timestamp \/ 
        taskPendingEvents[t][i] \in processedEvents

IdleSourceSendsMaxTimestamp ==
    \A s \in Source :
        sourceActive[s] = FALSE => sourceWatermarks[s] = MaxTimestamp

GlobalMonotonicity ==
    IsMonotonic(watermarkHistory)

CorrectEventProcessing ==
    \A e \in processedEvents :
        \E t \in Task :
            e.timestamp <= taskOutputWatermarks[t]

NoPrematureProcessing ==
    \A t \in Task, i \in 1..Len(taskPendingEvents[t]) :
        taskPendingEvents[t][i] \notin processedEvents => 
            taskPendingEvents[t][i].timestamp > taskOutputWatermarks[t]

WatermarkProgress ==
    (\E s \in Source : sourceActive[s] = TRUE /\ sourceTimestamps[s] > 0) ~>
    <> (globalWatermark > 0)

EventualEventProcessing ==
    \A t \in Task, i \in 1..Len(taskPendingEvents[t]) :
        taskPendingEvents[t][i].timestamp <= taskOutputWatermarks[t] ~>
        <> (taskPendingEvents[t][i] \in processedEvents)

IdleSourcesEventuallyMarked ==
    \A s \in Source :
        [] (globalClock - sourceLastActivity[s] > IdleTimeout => 
            <> (sourceActive[s] = FALSE))

vars == <<sourceTimestamps, sourceWatermarks, sourceActive, sourceLastActivity,
          taskInputWatermarks, taskOutputWatermarks, taskPendingEvents,
          globalWatermark, watermarkHistory, processedEvents, globalClock>>

================================================================================
