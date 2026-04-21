# Performance Tuning Patterns

> **Stage**: Knowledge/07-best-practices | **Prerequisites**: [Anti-patterns](anti-pattern-serialization-overhead.md) | **Formalization Level**: L3
> **Translation Date**: 2026-04-21

## Abstract

Systematic optimization patterns for Flink jobs covering serialization, networking, state access, and JVM tuning.

---

## 1. Key Performance Metrics

| Metric | Definition | Measurement | Goal |
|--------|-----------|-------------|------|
| Throughput | Records processed per second | `numRecordsInPerSecond` | Maximize |
| Latency | Input to output time | `currentOutputWatermark - inputTimestamp` | Minimize |
| Backpressure | Upstream blocking time | `backPressuredTimeMsPerSecond` | Minimize |
| Checkpoint time | Snapshot duration | `checkpointDuration` | Minimize |
| CPU utilization | Effective compute ratio | `cpuTime` / wallTime | Maximize |

---

## 2. Serialization Optimization

```java
// Use POJOs with public fields (fastest)
public class Event {
    public long timestamp;
    public String key;
    public double value;
}

// Avoid generic types when possible
// Use TypeInformation explicitly
TypeInformation<Event> typeInfo = TypeInformation.of(Event.class);
```

| Serializer | Speed | Compatibility |
|------------|-------|---------------|
| POJO (public fields) | ★★★★★ | ★★★★☆ |
| POJO (getters/setters) | ★★★★☆ | ★★★★★ |
| Avro | ★★★★☆ | ★★★★★ |
| Kryo | ★★★☆☆ | ★★★★☆ |
| Generic (TypeExtractor) | ★★☆☆☆ | ★★★★★ |

---

## 3. State Access Optimization

| Pattern | Impact | When to Use |
|---------|--------|-------------|
| ValueState | Lowest overhead | Single value per key |
| MapState | Efficient for maps | Key-value collections |
| ListState | Sequential access | Ordered collections |
| State TTL | Automatic cleanup | Time-bound state |

---

## 4. JVM Optimization

```java
// Recommended JVM options
env.getConfiguration().setString("env.java.opts",
    "-XX:+UseG1GC " +
    "-XX:MaxGCPauseMillis=100 " +
    "-XX:+UnlockExperimentalVMOptions " +
    "-XX:+UseContainerSupport"
);
```

---

## 5. References
