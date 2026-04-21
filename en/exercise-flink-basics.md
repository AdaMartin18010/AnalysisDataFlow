# Exercise: Flink Basics

> **Language**: English | **Source**: [Knowledge/98-exercises/exercise-02-flink-basics.md](../Knowledge/98-exercises/exercise-02-flink-basics.md) | **Last Updated**: 2026-04-21

---

## Learning Objectives

After completing this exercise, you will be able to:

- **Def-K-02-EN-01**: Master core DataStream API operations (Transformation, Sink)
- **Def-K-02-EN-02**: Understand Flink parallelism and partitioning strategies
- **Def-K-02-EN-03**: Design simple stream processing topologies
- **Def-K-02-EN-04**: Use local development and debugging techniques

## Prerequisites

- JDK 11+
- Maven 3.8+ or Gradle 7+
- Flink 1.18+ (local mode)
- Optional: Docker (for Flink cluster)

## Core Concepts

| Concept | Description | Common API |
|---------|-------------|------------|
| DataStream | Stream abstraction | `env.fromElements()`, `env.fromSource()` |
| Transformation | Stream operation | `.map()`, `.filter()`, `.keyBy()`, `.window()` |
| Sink | Output destination | `.print()`, `.addSink()`, `.writeAsText()` |
| Parallelism | Concurrent task count | `env.setParallelism(n)` |
| Checkpoint | Fault-tolerant snapshot | `env.enableCheckpointing(interval)` |

## Window Types

| Window | Trigger | Use Case |
|--------|---------|----------|
| **Tumbling** | Fixed time, non-overlapping | Periodic metrics (every 1 min) |
| **Sliding** | Fixed time, overlapping | Moving average (last 5 min, every 1 min) |
| **Session** | Activity gap | User sessions (gap > 30 min) |
| **Global** | Manual / never | Batch-over-stream pattern |

## Exercise 1: Word Count (15 min)

```java
StreamExecutionEnvironment env =
    StreamExecutionEnvironment.getExecutionEnvironment();

DataStream<String> source = env.fromData(
    "hello flink", "hello world", "flink streaming");

source
    .flatMap((String value, Collector<String> out) -> {
        for (String word : value.split(" ")) {
            out.collect(word);
        }
    })
    .map(word -> Tuple2.of(word, 1))
    .keyBy(tuple -> tuple.f0)
    .window(TumblingEventTimeWindows.of(Time.seconds(5)))
    .sum(1)
    .print();

env.execute("WordCount");
```

## Exercise 2: User Behavior Analysis

**Task**: Count page views per user in 1-minute tumbling windows.

**Input**: `UserEvent{userId, pageId, timestamp}`

**Expected Output**: `(userId, viewCount)` per minute

```java
stream
    .keyBy(event -> event.userId)
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .aggregate(new CountAggregate())
    .print();
```

## Exercise 3: Temperature Alert System

**Task**: Alert when temperature exceeds threshold for 3 consecutive readings.

**Hint**: Use `KeyedProcessFunction` with state.

```java
class TemperatureAlert extends KeyedProcessFunction<String, SensorReading, Alert> {
    private ValueState<Integer> consecutiveHighState;

    @Override
    public void open(Configuration parameters) {
        consecutiveHighState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("consecutive", Types.INT));
    }

    @Override
    public void processElement(SensorReading reading, Context ctx, Collector<Alert> out)
            throws Exception {
        int count = consecutiveHighState.value() != null ?
            consecutiveHighState.value() : 0;

        if (reading.temperature > THRESHOLD) {
            count++;
            if (count >= 3) {
                out.collect(new Alert(reading.sensorId, reading.temperature));
            }
        } else {
            count = 0;
        }
        consecutiveHighState.update(count);
    }
}
```

## Key Partitioning Strategies

| Strategy | When to Use |
|----------|-------------|
| `keyBy()` | Stateful operations, aggregations per key |
| `broadcast()` | Small lookup tables, configuration |
| `rebalance()` | Data skew mitigation |
| `shuffle()` | Random distribution for load balancing |

## Debugging Tips

```bash
# Local execution with Web UI
flink run -d -p 2 my-job.jar
# Open http://localhost:8081

# Check backpressure
# Flink UI -> Job -> Backpressure tab

# Enable logging
log4j.logger.org.apache.flink=DEBUG
```

## References
