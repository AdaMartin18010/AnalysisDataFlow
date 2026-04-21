# Business Pattern: IoT Stream Processing

> **Stage**: Knowledge/03-business-patterns | **Prerequisites**: [Event Time](pattern-event-time-processing.md), [Stateful Computation](pattern-stateful-computation.md) | **Complexity**: ★★★★☆ | **Latency**: < 2s
> **Translation Date**: 2026-04-21

## Abstract

Handling millions of device connections, out-of-order data, device state maintenance, and session window management in IoT scenarios.

---

## 1. Definitions

### Def-K-03-01 (IoT Data Stream)

$$D_{IoT} = \{ (deviceId, timestamp, metric, value) \mid deviceId \in \text{UUID} \}$$

### Def-K-03-02 (Device Session)

A session is a maximal sequence of events from one device with gap $< g$:

$$\text{Session}(d) = [t_{first}, t_{last}] \quad \text{where} \quad t_{i+1} - t_i < g$$

### Def-K-03-03 (Out-of-Order Tolerance)

Maximum event time delay accepted: $\delta_{max} = 30s$ (typical).

---

## 2. Architecture

```
Device → MQTT Broker → Flink Source → Window/Session → Alert/Analytics
                ↓
         Actor-based Device Manager
```

---

## 3. Flink Implementation

```java
// Session windows for device activity
stream
    .keyBy(e -> e.deviceId)
    .window(EventTimeSessionWindows.withDynamicGap(
        (e) -> Time.minutes(5)))
    .aggregate(new DeviceSessionAggregator());

// Temperature alert with state
stream
    .keyBy(e -> e.deviceId)
    .process(new TemperatureAlertFunction());
```

---

## 4. Key Challenges

| Challenge | Solution |
|-----------|----------|
| Million-scale devices | KeyBy(deviceId) for parallelization |
| Out-of-order data | Watermark with 30s tolerance |
| Device state | KeyedState with TTL |
| Session management | EventTimeSessionWindows |

---

## 5. References
