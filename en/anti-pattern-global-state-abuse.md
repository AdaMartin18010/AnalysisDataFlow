# Anti-Pattern AP-01: Global State Abuse

> **Stage**: Knowledge/09-anti-patterns | **Category**: State Management | **Severity**: P2 | **Detection**: Easy
> **Translation Date**: 2026-04-21

## Abstract

Using global mutable state in operators that should be stateless leads to concurrency issues, recovery difficulties, and non-deterministic results.

---

## 1. Definition

**Anti-Pattern**: Storing state in non-managed variables (instance fields, static variables) instead of Flink's managed state APIs.

---

## 2. Symptoms

| Symptom | Indicator |
|---------|-----------|
| Runtime | Non-deterministic results across restarts |
| Code Review | `private int count = 0;` in `ProcessFunction` |
| Metrics | Checkpoint size much smaller than expected state |

---

## 3. Solutions

### Use KeyedState (Recommended)

```java
// Wrong: Global counter
private int globalCounter = 0;

// Correct: KeyedState counter
private ValueState<Integer> counterState;

@Override
public void open(Configuration parameters) {
    counterState = getRuntimeContext().getState(
        new ValueStateDescriptor<>("counter", Types.INT));
}
```

### Use OperatorState

For non-keyed state that needs to be checkpointed.

### Use Broadcast State

For configuration/state that should be identical across all subtasks.

---

## 4. References
