# Operator Best Practices Quick Reference

> **Stage**: Knowledge/07-best-practices | **Prerequisites**: All v7.1 operator system documents | **Formalization Level**: L2
> **Document Positioning**: Quick reference handbook for stream processing operator selection, configuration, tuning, and troubleshooting
> **Version**: 2026.04

---

## Table of Contents

- [Operator Best Practices Quick Reference](#operator-best-practices-quick-reference)
  - [Table of Contents](#table-of-contents)
  - [1. Operator Selection Quick Reference](#1-operator-selection-quick-reference)
    - [1.1 Selection by Business Scenario](#11-selection-by-business-scenario)
    - [1.2 Selection by Data Characteristics](#12-selection-by-data-characteristics)
  - [2. Parameter Configuration Quick Reference](#2-parameter-configuration-quick-reference)
    - [2.1 Global Configuration](#21-global-configuration)
    - [2.2 Operator-level Configuration](#22-operator-level-configuration)
  - [3. Performance Tuning Quick Reference](#3-performance-tuning-quick-reference)
    - [3.1 Latency Optimization Checklist](#31-latency-optimization-checklist)
    - [3.2 Throughput Optimization Checklist](#32-throughput-optimization-checklist)
    - [3.3 Resource Optimization Checklist](#33-resource-optimization-checklist)
  - [4. Troubleshooting Quick Reference](#4-troubleshooting-quick-reference)
    - [4.1 Exception Quick Reference](#41-exception-quick-reference)
    - [4.2 Key Metrics Thresholds](#42-key-metrics-thresholds)
  - [5. Code Template Quick Reference](#5-code-template-quick-reference)
    - [5.1 Standard ProcessFunction Template](#51-standard-processfunction-template)
    - [5.2 AsyncFunction Template](#52-asyncfunction-template)
    - [5.3 Two-Stage Aggregation (Anti-Skew) Template](#53-two-stage-aggregation-anti-skew-template)
    - [5.4 Side Output Exception Handling Template](#54-side-output-exception-handling-template)
  - [6. Security Checklist](#6-security-checklist)
    - [6.1 Pre-Release Checklist](#61-pre-release-checklist)
    - [6.2 Runtime Monitoring Checklist](#62-runtime-monitoring-checklist)

---

## 1. Operator Selection Quick Reference

### 1.1 Selection by Business Scenario

| Business Requirement | Recommended Operators | Avoid | Key Parameters |
|---------|---------|------|---------|
| Data cleansing/transformation | `map` / `filter` / `flatMap` | `ProcessFunction` (overkill) | None |
| Key-grouped statistics | `keyBy` + `reduce` / `aggregate` | `windowAll` | `TTL`, `stateBackend` |
| Time window aggregation | `window` + `aggregate` | Global `process` simulating windows | `size`, `slide`, `allowedLateness` |
| Dual-stream join | `intervalJoin` / `coGroup` | `join` (Tumbling only) | `lowerBound`, `upperBound` |
| Async I/O | `AsyncFunction` | Synchronous calls in `map` | `timeout`, `capacity` |
| Complex event recognition | `CEP` | Handwritten `ProcessFunction` | `within`, `next/followedBy` |
| Dynamic rule updates | `BroadcastStream` + `connect` | Hard-coded rules | `MapStateDescriptor` |
| Data splitting | `SideOutput` | Multiple `filter` with duplicate processing | `OutputTag` |
| Ordering guarantee | `keyBy` then single-partition processing | Global sorting | `parallelism=1` (sorting stage only) |
| Late data handling | `allowedLateness` + `sideOutput` | Dropping all late data | `allowedLateness`, `sideOutputTag` |

### 1.2 Selection by Data Characteristics

| Data Characteristic | Recommended Pattern | Operator Combination |
|---------|---------|---------|
| High throughput (>1M/s) | Stateless + pre-aggregation | `filter` → `map` → `keyBy` → `reduce` |
| High latency tolerance (>1min) | Large window batch processing | `window` (hour-level) → `aggregate` |
| Strict low latency (<100ms) | Per-event processing | `process` / `AsyncFunction` |
| Severe data skew | Salting + two-stage aggregation | `map` (salting) → `keyBy` → `reduce` → `keyBy` (desalting) → `reduce` |
| Severe out-of-order | Event time + watermarks | `assignTimestamps` → `watermark` → `window` |
| Very large state (>10GB) | RocksDB + incremental Checkpoint | `keyBy` + `RocksDBStateBackend` |
| Exactly-once requirement | Transactional Sink | `TwoPhaseCommitSinkFunction` |

---

## 2. Parameter Configuration Quick Reference

### 2.1 Global Configuration

```properties
# Checkpoint configuration
execution.checkpointing.interval=30s
execution.checkpointing.min-pause-between-checkpoints=30s
execution.checkpointing.timeout=10min
execution.checkpointing.max-concurrent-checkpoints=1
state.backend=rocksdb
state.backend.incremental=true
state.checkpoints.dir=s3://bucket/checkpoints

# Network configuration
taskmanager.memory.network.fraction=0.15
taskmanager.memory.network.min=128mb
taskmanager.memory.network.max=256mb

# State configuration
state.backend.rocksdb.memory.managed=true
state.backend.rocksdb.predefined-options=SPINNING_DISK_OPTIMIZED_HIGH_MEM
```

### 2.2 Operator-level Configuration

| Operator | Key Parameters | Recommended Value | Description |
|------|---------|--------|------|
| **Kafka Source** | `fetch.min.bytes` | 1-10KB | Reduce empty polling |
| | `max.poll.records` | 500-2000 | Balance latency and throughput |
| | `consumer.auto.offset.reset` | `latest`/`earliest` | Choose based on business needs |
| **AsyncFunction** | `timeout` | p99 latency × 1.5 | Cover绝大多数 requests |
| | `capacity` | ⌈p99/p50⌉ × P | P is parallelism |
| **Window** | `allowedLateness` | Max out-of-order time | Usually 5 seconds to 5 minutes |
| | `sideOutputLateData` | Must configure | Late data not lost |
| **Join** | `lowerBound` | -window size | Left stream waits for right stream |
| | `upperBound` | +window size | Right stream waits for left stream |
| **Timer** | Clean old timers | Must implement | Avoid timer leaks |
| **State TTL** | `updateType` | `OnCreateAndWrite` | Refresh TTL on each update |
| | `stateVisibility` | `NeverReturnExpired` | Do not return expired state |

---

## 3. Performance Tuning Quick Reference

### 3.1 Latency Optimization Checklist

- [ ] Source parallelism = Kafka partition count (avoid idle tasks)
- [ ] Network buffer sufficient (`taskmanager.memory.network.fraction ≥ 0.1`)
- [ ] Serializer optimization (prefer Avro/Protobuf, avoid Kryo generics)
- [ ] Async I/O替代 synchronous I/O (AsyncFunction vs HTTP calls in map)
- [ ] State access locality (RocksDB block cache tuning)
- [ ] GC optimization (G1GC, -XX:MaxGCPauseMillis=100)
- [ ] Object reuse (reuse output objects in ProcessFunction)

### 3.2 Throughput Optimization Checklist

- [ ] Backpressure定位 (find bottleneck operator, not盲目 scaling)
- [ ] Data skew detection (SkewIndex > 5 needs handling)
- [ ] Small file management (lakehouse Sink periodic compaction)
- [ ] Batch writes (Sink端 batch commit, reduce IO次数)
- [ ] Compression algorithm selection (LZ4/Snappy balance CPU and compression ratio)
- [ ] Reasonable parallelism (CPU utilization 60-70% is optimal)
- [ ] Partition strategy optimization (avoid cross-network shuffle)

### 3.3 Resource Optimization Checklist

- [ ] Reserved instances (7×24 jobs use Reserved Instances to save 30-55%)
- [ ] State TTL (prevent unbounded state growth)
- [ ] Auto scaling (for peak-valley明显 scenarios)
- [ ] Spot instances (stateless tasks can use Spot to save 60-80%)
- [ ] Memory vs disk tradeoff (state >1GB must use RocksDB)
- [ ] Checkpoint interval tradeoff (30 seconds to 1 minute is optimal balance)

---

## 4. Troubleshooting Quick Reference

### 4.1 Exception Quick Reference

| Exception/Symptom | Quick Diagnosis | Quick Fix |
|----------|---------|---------|
| `NullPointerException` | Check input data null values | Pre-filter or Optional handling |
| `OutOfMemoryError` | Check stateSize and Timer count | Enable TTL or reduce windows |
| `Checkpoint expired` | Check checkpointDuration | Increase timeout or optimize state |
| `BackPressure` | Locate backpressure source operator | Scale up or optimize bottleneck operator |
| `Watermarks lagging` | Check Source Lag | Increase Source parallelism or adjust Watermark |
| `Connection refused` | Check external service health | Add retry and circuit breaker |
| `ClassCastException` | Check TypeInformation | Explicitly specify type or serializer |
| `Too many open files` | Check file handle limits | ulimit -n 65536 |

### 4.2 Key Metrics Thresholds

| Metric | Normal Range | Warning Threshold | Critical Threshold |
|------|---------|---------|---------|
| CPU utilization | 40-70% | >80% | >95% |
| Memory utilization | 50-70% | >80% | >95% |
| GC time ratio | <5% | >10% | >30% |
| Backpressure ratio | <0.1 | >0.5 | >0.8 |
| Checkpoint duration | <30s | >60s | >timeout |
| Source Lag | <1000 | >10000 | >100000 |
| Watermark lag | <event time window | >2×window size | >10×window size |
| State size | <1GB/parallelism | >5GB/parallelism | >10GB/parallelism |

---

## 5. Code Template Quick Reference

### 5.1 Standard ProcessFunction Template

```java
public class SafeProcessFunction extends KeyedProcessFunction<String, Event, Result> {
    private ValueState<StateData> state;
    private ValueState<Long> timerState;

    @Override
    public void open(Configuration parameters) {
        StateTtlConfig ttl = StateTtlConfig
            .newBuilder(Time.hours(24))
            .setUpdateType(OnCreateAndWrite)
            .setStateVisibility(NeverReturnExpired)
            .build();
        ValueStateDescriptor<StateData> descriptor =
            new ValueStateDescriptor<>("state", StateData.class);
        descriptor.enableTimeToLive(ttl);
        state = getRuntimeContext().getState(descriptor);

        ValueStateDescriptor<Long> timerDescriptor =
            new ValueStateDescriptor<>("timer", Types.LONG);
        timerState = getRuntimeContext().getState(timerDescriptor);
    }

    @Override
    public void processElement(Event event, Context ctx, Collector<Result> out) {
        // 1. Clean old timer
        Long oldTimer = timerState.value();
        if (oldTimer != null) {
            ctx.timerService().deleteEventTimeTimer(oldTimer);
        }

        // 2. Processing logic
        StateData current = state.value();
        if (current == null) current = new StateData();
        current.update(event);
        state.update(current);

        // 3. Register new timer
        long newTimer = ctx.timestamp() + Time.minutes(5).toMilliseconds();
        ctx.timerService().registerEventTimeTimer(newTimer);
        timerState.update(newTimer);

        // 4. Output
        out.collect(current.toResult());
    }

    @Override
    public void onTimer(long timestamp, OnTimerContext ctx, Collector<Result> out) {
        // Clean up state
        timerState.clear();
        StateData current = state.value();
        if (current != null && current.isExpired(timestamp)) {
            state.clear();
        }
    }
}
```

### 5.2 AsyncFunction Template

```java
public class SafeAsyncFunction extends AsyncFunction<Event, EnrichedEvent> {
    private transient AsyncHttpClient client;

    @Override
    public void open(Configuration parameters) {
        client = AsyncHttpClient.builder()
            .setRequestTimeout(Duration.ofMillis(100))
            .setMaxConnections(100)
            .build();
    }

    @Override
    public void asyncInvoke(Event event, ResultFuture<EnrichedEvent> resultFuture) {
        client.call(event.getId())
            .whenComplete((result, exception) -> {
                if (exception != null) {
                    resultFuture.completeExceptionally(exception);
                } else {
                    resultFuture.complete(Collections.singletonList(
                        new EnrichedEvent(event, result)
                    ));
                }
            });
    }

    @Override
    public void timeout(Event event, ResultFuture<EnrichedEvent> resultFuture) {
        resultFuture.complete(Collections.singletonList(
            new EnrichedEvent(event, null)  // Degradation handling
        ));
    }
}
```

### 5.3 Two-Stage Aggregation (Anti-Skew) Template

```java
// Step 1: Salting pre-aggregation
stream.map(event -> {
    event.setSaltedKey(event.getKey() + "_" + ThreadLocalRandom.current().nextInt(10));
    return event;
})
.keyBy(Event::getSaltedKey)
.aggregate(new PartialAggregate())
// Step 2: Desalting final aggregation
.map(result -> {
    result.setKey(result.getSaltedKey().split("_")[0]);
    return result;
})
.keyBy(Result::getKey)
.aggregate(new FinalAggregate());
```

### 5.4 Side Output Exception Handling Template

```java
OutputTag<Event> lateTag = new OutputTag<Event>("late"){};
OutputTag<Event> errorTag = new OutputTag<Event>("error"){};

SingleOutputStreamOperator<Result> main = stream
    .keyBy(Event::getKey)
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .allowedLateness(Time.seconds(30))
    .sideOutputLateData(lateTag)
    .process(new SafeWindowFunction(errorTag));

// Handle late data
main.getSideOutput(lateTag).addSink(new LateDataSink());
// Handle exception data
main.getSideOutput(errorTag).addSink(new ErrorDataSink());
```

---

## 6. Security Checklist

### 6.1 Pre-Release Checklist

- [ ] Are operator UIDs stable? (Savepoint compatibility)
- [ ] Has state type changed? (Schema compatibility)
- [ ] Is keyBy key distribution uniform? (Data skew)
- [ ] Are all states configured with TTL? (Prevent OOM)
- [ ] Are timers cleaned up? (Prevent leaks)
- [ ] Do external calls have timeouts? (Prevent blocking)
- [ ] Is Sink idempotent or transactional? (Prevent duplicates)
- [ ] Is sensitive data desensitized? (Privacy compliance)
- [ ] Is parallelism reasonable? (Source ≤ Kafka partition count)
- [ ] Does Checkpoint pass? (Recovery capability)

### 6.2 Runtime Monitoring Checklist

- [ ] Backpressure ratio < 0.5?
- [ ] CPU utilization 40-70%?
- [ ] GC time < 5%?
- [ ] Checkpoint duration < 60 seconds?
- [ ] Source Lag < 10000?
- [ ] State size growth trend stable?
- [ ] No exception log flooding?
- [ ] Watermark advancing normally?

---

*Related Documents*: [operator-testing-and-verification-guide.md](operator-testing-and-verification-guide.md) | [operator-performance-benchmark-tuning.md](operator-performance-benchmark-tuning.md) | [operator-anti-patterns.md](operator-anti-patterns.md)
