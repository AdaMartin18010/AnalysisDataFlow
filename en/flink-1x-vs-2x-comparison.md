# Flink 1.x vs 2.0 Architecture Comparison

> **Language**: English | **Source**: [Flink/01-concepts/flink-1.x-vs-2.0-comparison.md](../Flink/01-concepts/flink-1.x-vs-2.0-comparison.md) | **Last Updated**: 2026-04-21

---

## Executive Summary

Apache Flink 2.0 introduces **Disaggregated State Storage** and **Async Execution Model**. This document formally compares the core architectural differences between Flink 1.x and 2.0.

| Dimension | Flink 1.x | Flink 2.0 | Impact |
|-----------|-----------|-----------|--------|
| **State storage** | TM-local binding | Disaggregated remote | Recovery: minutes → seconds |
| **Fault recovery** | Full state migration | Location-independent scheduling | Complexity: O(n) → O(1) |
| **Scaling** | Key Group redistribution | Instant scaling | Simplified topology changes |
| **Consistency** | Checkpoint barrier sync | Async snapshot + incremental sync | New formalization needed |

## Architecture Overview

### Flink 1.x: Embedded State

```
┌─────────────────────────────────────┐
│  JobManager (Control Plane)         │
└─────────────┬───────────────────────┘
              │
┌─────────────▼─────────────┐
│  TaskManager (Data Plane) │
│  ┌─────────┐ ┌─────────┐ │
│  │ Task    │ │ State   │ │  ← Tightly coupled
│  │ Slot 1  │ │ Backend │ │
│  └─────────┘ └─────────┘ │
│  ┌─────────┐ ┌─────────┐ │
│  │ Task    │ │ Local   │ │
│  │ Slot 2  │ │ RocksDB │ │
│  └─────────┘ └─────────┘ │
└───────────────────────────┘
```

### Flink 2.0: Disaggregated State

```
┌─────────────────────────────────────┐
│  JobManager (Control Plane)         │
└─────────────┬───────────────────────┘
              │
┌─────────────▼─────────────┐    ┌─────────────────┐
│  Stateless TaskManagers   │◄──►│  Remote State   │
│  ┌─────────┐ ┌─────────┐  │    │  Service        │
│  │ Task    │ │ Cache   │  │    │  (S3/GCS/OSS)   │
│  │ Slot 1  │ │ L1/L2   │  │    └─────────────────┘
│  └─────────┘ └─────────┘  │
│  ┌─────────┐ ┌─────────┐  │
│  │ Task    │ │ Cache   │  │
│  │ Slot 2  │ │ L1/L2   │  │
│  └─────────┘ └─────────┘  │
└───────────────────────────┘
```

## Detailed Comparison

| Feature | Flink 1.x | Flink 2.0 |
|---------|-----------|-----------|
| **State backend** | Memory / FS / RocksDB (local) | ForStateBackend (remote) |
| **State access** | Blocking synchronous | Async non-blocking |
| **Max state size** | TM disk capacity | Unlimited (cloud storage) |
| **Recovery time** | ∝ state size | Near-instant |
| **Rescaling** | Key group redistribution | Stateless TM migration |
| **API** | DataStream V1 | DataStream V2 (async) |
| **Backpressure** | Reactive (downstream signal) | Proactive (credit-based) |
| **Deployment** | Stateful pods | Stateless pods + remote state |

## API Migration

| V1 API | V2 API | Change |
|--------|--------|--------|
| `ValueState<T>` | `AsyncState<T>` | Blocking → Async |
| `getRuntimeContext().getState(...)` | `@State` annotation | Imperative → Declarative |
| `processElement(...)` | `processElement(...)` with futures | Sync → Async composition |
| `KeyedProcessFunction` | `KeyedProcessFunctionV2` | Enhanced type safety |

## Migration Strategy

| Phase | Action | Risk |
|-------|--------|------|
| **1. Assess** | Identify stateful operators, measure state size | Low |
| **2. Test** | Run V2 API in staging with representative workload | Medium |
| **3. Migrate** | Convert operators incrementally; run V1+V2 hybrid | Medium |
| **4. Cutover** | Switch to V2 runtime; enable disaggregated state | High |
| **5. Optimize** | Tune cache policy, sync strategy | Low |

## References
