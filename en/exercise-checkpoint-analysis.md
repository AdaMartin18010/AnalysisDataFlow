# Exercise: Checkpoint Analysis

> **Language**: English | **Source**: [Knowledge/98-exercises/exercise-03-checkpoint-analysis.md](../Knowledge/98-exercises/exercise-03-checkpoint-analysis.md) | **Last Updated**: 2026-04-21

---

## Learning Objectives

After completing this exercise, you will be able to:

- **Def-K-03-EN-01**: Understand checkpoint trigger mechanisms and execution flow
- **Def-K-03-EN-02**: Diagnose checkpoint timeouts and failures
- **Def-K-03-EN-03**: Configure and optimize checkpoint parameters
- **Def-K-03-EN-04**: Understand Exactly-Once semantics via checkpointing

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Checkpoint Barrier** | Special record separating pre- and post-checkpoint data |
| **Snapshot** | Consistent snapshot of all operator states |
| **Checkpoint Coordinator** | JobManager component that orchestrates checkpoints |
| **State Backend** | Persistent storage for state (Memory/FS/RocksDB) |
| **Incremental Checkpoint** | Only saves delta state changes |

## Key Configuration Parameters

```java
// Checkpointing settings
env.enableCheckpointing(60000);           // Interval: 60s
env.getCheckpointConfig().setTimeout(600000);  // Timeout: 10 min
env.getCheckpointConfig().setMinPauseBetweenCheckpoints(30000);  // 30s min pause
env.getCheckpointConfig().setMaxConcurrentCheckpoints(1);
env.getCheckpointConfig().setCheckpointStorage("file:///checkpoints");

// RocksDB settings
env.setStateBackend(new EmbeddedRocksDBStateBackend(true));  // Incremental
env.getCheckpointConfig().setCheckpointStorage(new FileSystemCheckpointStorage("s3://bucket"));
```

## Checkpoint Execution Flow

```mermaid
sequenceDiagram
    participant JM as JobManager
    participant CC as CheckpointCoordinator
    participant TM1 as TaskManager 1
    participant TM2 as TaskManager 2
    participant S3 as Checkpoint Storage

    JM->>CC: Trigger checkpoint
    CC->>TM1: Inject barrier
    CC->>TM2: Inject barrier
    TM1->>TM1: Align barriers, snapshot state
    TM2->>TM2: Align barriers, snapshot state
    TM1->>S3: Upload state async
    TM2->>S3: Upload state async
    TM1->>CC: Acknowledge
    TM2->>CC: Acknowledge
    CC->>JM: Complete checkpoint
```

## Failure Diagnosis

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `Checkpoint expired` | State too large; slow storage | Enable incremental; use faster storage |
| `Alignment timeout` | Backpressure during checkpoint | Reduce `alignmentTimeout`; enable unaligned |
| `Async phase timeout` | Serialization bottleneck | Use `TypeInformation`; tune buffer size |
| `Checkpoint decline` | TM overloaded | Scale out TMs; reduce task slots per TM |

## Exactly-Once Semantics

```mermaid
graph TB
    subgraph "Pre-Checkpoint"
        A[Records before barrier]
    end
    subgraph "Barrier"
        B[Checkpoint Barrier n]
    end
    subgraph "Post-Checkpoint"
        C[Records after barrier]
    end
    subgraph "Recovery"
        D[Restore from Checkpoint n]
        E[Replay from offset n]
    end
    A --> B --> C
    D --> E --> C
```

**Key insight**: Barriers divide the stream into pre-checkpoint and post-checkpoint regions. On recovery, restore state from checkpoint and replay source from the recorded offset.

## Optimization Checklist

- [ ] Interval < max tolerable replay window
- [ ] Timeout > expected checkpoint duration × 2
- [ ] Incremental enabled for large state (> 1GB)
- [ ] Local recovery enabled for fast failover
- [ ] Unaligned checkpoint enabled for high backpressure scenarios
- [ ] Externalized checkpoint cleanup for savepoint retention

## References
