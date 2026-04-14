---
title: "Streaming Anti-Patterns Quick Reference Card"
translation_status: ai_translated_reviewed
source_version: v4.1
last_sync: "2026-04-15"
---

# Streaming Anti-Patterns Quick Reference Card

> **Quick Reference**: Symptoms, root causes, and solutions for 10 common anti-patterns
>
> **Full Documentation**: [streaming-anti-patterns.md](../09-anti-patterns/streaming-anti-patterns.md)

---

## 🚨 Severity Level Reference

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Severity Pyramid                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  P0 - Catastrophic ▲                                                    │
│            /██\    System cascading failure, data loss, service outage  │
│           /████\   AP-02 Ignoring Backpressure Signals                  │
│          /██████\  AP-10 Insufficient Monitoring                        │
│         ▔▔▔▔▔▔▔▔▔                                                │
│                                                                         │
│  P1 - High Risk   ▲                                                     │
│            /██\    Severe performance degradation, OOM, recovery failure│
│           /████\   AP-03 No State TTL      AP-05 Data Skew              │
│          /██████\  AP-06 Global Window Abuse   AP-07 Ignoring Late Data │
│         /████████\ AP-04 Incorrect Checkpoint Configuration             │
│        ▔▔▔▔▔▔▔▔▔▔▔                                             │
│                                                                         │
│  P2 - Medium   ▲                                                        │
│            /██\    Inaccurate results, resource waste, sporadic errors  │
│           /████\   AP-01 Over-reliance on Processing Time   AP-08 Improper Parallelism│
│          /██████\  AP-09 Lack of Idempotency                            │
│         ▔▔▔▔▔▔▔▔▔                                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Top 10 Anti-Patterns Cheat Sheet

### AP-01: Over-Reliance on Processing Time (P2)

| Item | Content |
|------|------|
| **Symptom** | Different results across reruns; incorrect window assignment; sensitive to out-of-order |
| **Root Cause** | Using `ProcessingTime` instead of `EventTime` as the time basis |
| **Solution** | Use `EventTime` + `WatermarkStrategy` + `allowedLateness` |

```scala
// ❌ Wrong
.window(TumblingProcessingTimeWindows.of(Time.minutes(5)))

// ✅ Correct
.assignTimestampsAndWatermarks(
  WatermarkStrategy.forBoundedOutOfOrderness(Duration.ofSeconds(30))
)
.window(TumblingEventTimeWindows.of(Time.minutes(5)))
.allowedLateness(Time.minutes(2))
.sideOutputLateData(lateDataTag)
```

---

### AP-02: Ignoring Backpressure Signals (P0) ⚠️

| Item | Content |
|------|------|
| **Symptom** | Checkpoint timeouts; OOM; Kafka Lag keeps growing; data loss |
| **Root Cause** | Ignoring Flink backpressure signals and continuing to increase input load |
| **Solution** | Monitor backpressure metrics; auto-scaling; source throttling |

```scala
// ✅ Monitor metrics
// backPressuredTimeMsPerSecond > 0 indicates backpressure exists

// ✅ Auto-scaling (Flink Kubernetes Operator)
spec:
  autoScaler:
    enabled: true
    targetUtilization: 0.7

// ✅ Source throttling
kafkaSource.setProperty("max.poll.records", "500")
```

---

### AP-03: Unbounded State Growth without TTL (P1)

| Item | Content |
|------|------|
| **Symptom** | Continuous state growth; increasing Checkpoint time; eventual OOM |
| **Root Cause** | `StateTtlConfig` not configured for state |
| **Solution** | Configure TTL + cleanup strategy |

```scala
// ✅ Configure TTL
val ttlConfig = StateTtlConfig
  .newBuilder(Time.minutes(30))
  .setUpdateType(OnCreateAndWrite)
  .setStateVisibility(NeverReturnExpired)
  .cleanupFullSnapshot()
  .build()

descriptor.enableTimeToLive(ttlConfig)
```

**Recommended TTL Values**:

| State Type | Recommended TTL |
|----------|---------|
| User Session | 30 minutes of inactivity |
| Deduplication State | 24 hours |
| Temporary Computation | 1 hour |
| Aggregation Cache | Window size + grace period |

---

### AP-04: Incorrect Checkpoint Configuration (P1)

| Item | Content |
|------|------|
| **Symptom** | Frequent Checkpoint failures; excessive recovery time; state corruption |
| **Root Cause** | Unreasonable interval/timeout/storage configuration |
| **Solution** | Configure parameters based on recovery SLA |

```scala
// ✅ Recommended configuration
env.enableCheckpointing(120000)  // 2-minute interval
env.getCheckpointConfig.setCheckpointTimeout(600000)  // 10-minute timeout
env.setStateBackend(new EmbeddedRocksDBStateBackend(true))  // Incremental Checkpoint
env.getCheckpointConfig.setCheckpointStorage("hdfs:///flink-checkpoints")
```

**Configuration Decision Table**:

| Scenario | Recommended Interval | Recommended Timeout | Incremental |
|------|----------|----------|------|
| Small state (<100MB) | 30s-1min | 2min | Optional |
| Medium state (100MB-10GB) | 1-2min | 5min | Recommended |
| Large state (>10GB) | 3-5min | 10min+ | Required |
| Financial trading | 10-30s | 1min | Recommended |

---

### AP-05: Unhandled Data Skew (P1)

| Item | Content |
|------|------|
| **Symptom** | Some tasks at 95%+ load while others idle; overall throughput drops |
| **Root Cause** | Uneven key distribution causing hot keys |
| **Solution** | Two-phase aggregation; custom partitioner; local cache |

```scala
// ✅ Two-phase aggregation
.map(txn => (s"${txn.merchantId}_${Random.nextInt(10)}", txn.amount))  // Add random prefix
.keyBy(_._1).window(TumblingEventTimeWindows.of(Time.seconds(10)))
.aggregate(new PreAggregate())  // First-phase local aggregation

.map { case (key, amount) => (key.split("_")(0), amount) }  // Remove prefix
.keyBy(_._1).window(TumblingEventTimeWindows.of(Time.minutes(1)))
.aggregate(new FinalAggregate())  // Second-phase global aggregation
```

---

### AP-06: Abusing Global Windows (P1)

| Item | Content |
|------|------|
| **Symptom** | Continuous state growth; no output or uncontrollable latency |
| **Root Cause** | Using `GlobalWindows` without configuring trigger and cleanup strategy |
| **Solution** | Configure explicit trigger and Evictor |

```scala
// ❌ Wrong
.window(GlobalWindows.create())  // Never closes!
.aggregate(new CountAggregate())

// ✅ Correct
.window(GlobalWindows.create())
.trigger(CountTrigger.of(1000))  // Trigger every 1000 records
.evictor(CountEvictor.of(1000))  // Clean up after trigger
.aggregate(new CountAggregate())
```

---

### AP-07: Ignoring Late Data (P1)

| Item | Content |
|------|------|
| **Symptom** | Statistics lower than actual; data loss cannot be audited |
| **Root Cause** | `allowedLateness` and `sideOutputLateData` not configured |
| **Solution** | Complete late data handling mechanism |

```scala
// ✅ Full configuration
val lateDataTag = OutputTag[Event]("late-data")

val result = stream
  .assignTimestampsAndWatermarks(
    WatermarkStrategy.forBoundedOutOfOrderness[Event](Duration.ofSeconds(10))
  )
  .keyBy(_.userId)
  .window(TumblingEventTimeWindows.of(Time.minutes(5)))
  .allowedLateness(Time.minutes(2))       // ✅ Allow 2-minute lateness
  .sideOutputLateData(lateDataTag)        // ✅ Side output for fully late data
  .aggregate(new CountAggregate())

// Handle fully late data
val lateData = result.getSideOutput(lateDataTag)
lateData.addSink(new LateDataAuditSink())  // Audit or offline backfill
```

---

### AP-08: Improper Parallelism Settings (P2)

| Item | Content |
|------|------|
| **Symptom** | Resource waste or insufficient processing capacity; some operators become bottlenecks |
| **Root Cause** | Parallelism does not match data volume/resources |
| **Solution** | Set parallelism according to scenario |

```scala
// ✅ Recommended configuration
kafkaSource.setParallelism(10)  // = Kafka partition count

stream
  .map(parseJson).setParallelism(10)  // Lightweight transformation
  .keyBy(_.userId)
  .window(TumblingEventTimeWindows.of(Time.minutes(1)))
  .aggregate(complexAggregation).setParallelism(20)  // Heavy computation
  .addSink(elasticsearchSink).setParallelism(5)  // Based on downstream capacity
```

---

### AP-09: Lack of Idempotency Consideration (P2)

| Item | Content |
|------|------|
| **Symptom** | Data duplication after failure recovery; incorrect statistics |
| **Root Cause** | Sink does not implement idempotent writes |
| **Solution** | UPSERT semantics; Two-Phase Commit (2PC); unique key constraints |

```scala
// ✅ Idempotent write (UPSERT)
val stmt = connection.prepareStatement(
  """INSERT INTO results (id, value, checkpoint_id)
     VALUES (?, ?, ?)
     ON CONFLICT (id) DO UPDATE SET
     value = EXCLUDED.value,
     checkpoint_id = EXCLUDED.checkpoint_id
     WHERE results.checkpoint_id < EXCLUDED.checkpoint_id
  """.stripMargin
)
stmt.setLong(3, context.getCurrentCheckpointId)  // Carry Checkpoint ID

// ✅ Or implement TwoPhaseCommitSinkFunction
class TwoPhaseCommitKafkaSink extends TwoPhaseCommitSinkFunction[...] { ... }
```

---

### AP-10: Insufficient Monitoring and Observability (P0) ⚠️

| Item | Content |
|------|------|
| **Symptom** | Delayed failure discovery; difficult troubleshooting; inability to predict issues |
| **Root Cause** | Lack of key metric monitoring and alerting |
| **Solution** | Complete monitoring system; key metric alerts; distributed tracing |

**Must-Monitor Metrics**:

| Category | Key Metric | Alert Threshold |
|------|----------|----------|
| **Latency** | End-to-end latency (p50/p99) | p99 > SLA |
| **Throughput** | recordsInPerSecond | Below expected |
| **Backpressure** | backPressuredTimeMsPerSecond | > 0 |
| **Checkpoint** | checkpointDuration | > 80% of timeout |
| **State** | stateSize | Growing too fast |
| **Kafka** | records-lag-max | > threshold |

---

## 🔍 Anti-Pattern Correlation Graph

```
┌─────────────────────────────────────────────────────────────────┐
│                      Anti-Pattern Causality                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  AP-02 Ignore Backpressure ────► AP-04 Checkpoint Timeout ────► Recovery Failure│
│       │                                             │           │
│       ▼                                             ▼           │
│  AP-10 Insufficient Monitoring ◄───────────────────────────── Data Loss        │
│       ▲                                             ▲           │
│       │                                             │           │
│  AP-05 Data Skew ────► Processing Capacity Drop ────► Backpressure Aggravation │
│       │                                                         │
│       └──► Hot Task OOM ◄──── AP-03 Unbounded State Growth     │
│                                                                 │
│  AP-01 Processing Time ────► AP-07 Late Data ────► Inaccurate Results         │
│       │                                                         │
│       └──► Window Assignment Error ◄──── AP-06 Global Window Abuse           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Further Reading

| Anti-Pattern | Full Documentation |
|--------|----------|
| AP-01 | [anti-pattern-02-watermark-misconfiguration.md](../09-anti-patterns/anti-pattern-02-watermark-misconfiguration.md) |
| AP-02 | [anti-pattern-08-ignoring-backpressure.md](../09-anti-patterns/anti-pattern-08-ignoring-backpressure.md) |
| AP-03 | [anti-pattern-01-global-state-abuse.md](../09-anti-patterns/anti-pattern-01-global-state-abuse.md) |
| AP-04 | [anti-pattern-03-checkpoint-interval-misconfig.md](../09-anti-patterns/anti-pattern-03-checkpoint-interval-misconfig.md) |
| AP-05 | [anti-pattern-04-hot-key-skew.md](../09-anti-patterns/anti-pattern-04-hot-key-skew.md) |
| AP-06 | [anti-pattern-07-window-state-explosion.md](../09-anti-patterns/anti-pattern-07-window-state-explosion.md) |
| AP-09 | [anti-pattern-05-blocking-io-processfunction.md](../09-anti-patterns/anti-pattern-05-blocking-io-processfunction.md) |
| AP-10 | [anti-pattern-10-resource-estimation-oom.md](../09-anti-patterns/anti-pattern-10-resource-estimation-oom.md) |
| Comprehensive | [streaming-anti-patterns.md](../09-anti-patterns/streaming-anti-patterns.md) |

---

*Quick Reference Card v1.0 | Last Updated: 2026-04-03*
