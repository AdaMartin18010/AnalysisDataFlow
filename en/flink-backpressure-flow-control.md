# Flink Backpressure and Flow Control

> **Stage**: Flink/02-core | **Prerequisites**: [Deployment Architectures](flink-deployment-architectures.md) | **Formalization Level**: L3-L4
> **Translation Date**: 2026-04-21

## Abstract

Credit-based flow control (CBFC) mechanism in Flink for handling downstream overload without data loss or OOM.

---

## 1. Definitions

### Def-F-02-01 (Backpressure)

Backpressure occurs when downstream operators cannot process data as fast as upstream produces it, propagating flow control signals upstream.

### Def-F-02-02 (Credit-Based Flow Control)

CBFC uses explicit credit messages from downstream to upstream, controlling buffer consumption per channel:

$$\text{Send} \iff \text{credit}_{receiver} > 0$$

### Def-F-02-05 (Buffer Debloating)

Dynamically reduces network buffer sizes to minimize checkpoint barrier propagation time.

---

## 2. Key Properties

### Prop-F-02-01 (CBFC Deadlock Freedom)

CBFC guarantees no deadlock: credit release is monotonic and bounded.

### Prop-F-02-05 (Credit System Prevents Receiver Overflow)

$$\text{buffer}_{used} \leq \text{buffer}_{total} - \text{credit}_{pending}$$

---

## 3. Backpressure Types

| Type | Scope | Mechanism | Flink Version |
|------|-------|-----------|---------------|
| TCP Backpressure | End-to-end | TCP window | < 1.5 |
| Credit-Based | Local per channel | Explicit credits | ≥ 1.5 |
| Buffer Debloating | Global tuning | Dynamic sizing | ≥ 1.14 |

---

## 4. Configuration

```java
// Enable buffer debloating
env.getConfiguration().setString(
    "taskmanager.network.memory.buffer-debloat.enabled", "true");

// Target time for buffer consumption (affects debloat aggressiveness)
env.getConfiguration().setString(
    "taskmanager.network.memory.buffer-debloat.target", "500");
```

---

## 5. References
