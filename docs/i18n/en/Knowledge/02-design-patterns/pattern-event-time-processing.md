# Design Pattern: Event Time Processing

> **Pattern ID**: 01/7 | **Series**: Knowledge/02-design-patterns | **Formalization Level**: L4-L5
>
> This pattern addresses the core conflict between **out-of-order data**, **late data**, and **result determinism** in distributed stream processing, providing a Watermark-based progress tracking mechanism.

---

## Table of Contents

- [Design Pattern: Event Time Processing](#design-pattern-event-time-processing)
  - [Table of Contents](#table-of-contents)
  - [1. Problem / Context](#1-problem--context)
    - [1.1 Temporal Challenges in Distributed Stream Processing](#11-temporal-challenges-in-distributed-stream-processing)
    - [1.2 Time Semantics Selection Dilemma](#12-time-semantics-selection-dilemma)
    - [1.3 Specific Manifestations in Business Scenarios](#13-specific-manifestations-in-business-scenarios)
  - [2. Solution](#2-solution)
    - [2.1 Core Concept Definitions](#21-core-concept-definitions)
    - [2.2 Watermark Mechanism Principles](#22-watermark-mechanism-principles)
    - [2.3 Late Data Handling Strategies](#23-late-data-handling-strategies)
    - [2.4 Pattern Structure Diagram](#24-pattern-structure-diagram)
  - [3. Implementation](#3-implementation)
    - [3.1 Flink Watermark Generation Strategies](#31-flink-watermark-generation-strategies)
    - [3.2 Window Aggregation and Late Data Handling](#32-window-aggregation-and-late-data-handling)
    - [3.3 Watermark Propagation for Multi-Input Operators](#33-watermark-propagation-for-multi-input-operators)
    - [3.4 Idle Source Handling](#34-idle-source-handling)
  - [4. When to Use](#4-when-to-use)
    - [4.1 Recommended Scenarios](#41-recommended-scenarios)
    - [4.2 Not Recommended Scenarios](#42-not-recommended-scenarios)
  - [5. Related Patterns](#5-related-patterns)
  - [6. Formal Guarantees](#6-formal-guarantees)
    - [6.1 Dependent Formal Definitions](#61-dependent-formal-definitions)
    - [6.2 Satisfied Formal Properties](#62-satisfied-formal-properties)
    - [6.3 Property Preservation During Pattern Composition](#63-property-preservation-during-pattern-composition)
    - [6.4 Boundary Conditions and Constraints](#64-boundary-conditions-and-constraints)
    - [6.5 Correspondence Between Engineering Implementation and Theory](#65-correspondence-between-engineering-implementation-and-theory)
  - [7. References](#7-references)

---

## 1. Problem / Context

### 1.1 Temporal Challenges in Distributed Stream Processing

In distributed stream processing systems, there is an essential inconsistency between the **physical arrival order** of data records and their **business occurrence order (event time)**. This inconsistency stems from the following factors [^1][^2]:

| Factor | Description | Typical Latency Range |
|--------|-------------|----------------------|
| **Network Latency** | Network delay from data generation to transmission to processing node | 10ms - seconds |
| **Backpressure** | Downstream processing slowness causing upstream data accumulation | seconds - minutes |
| **Retransmission Mechanism** | Data retransmission after network packet loss | seconds - tens of seconds |
| **Clock Skew** | Inconsistency in system clocks among distributed nodes | milliseconds - seconds |
| **Batch Transmission** | Batch reporting by edge gateways to save bandwidth | seconds - minutes |

**Formal Description** [^3]:

Let $t_e(r)$ be the event time of record $r$, and $t_a(r)$ be its arrival time at the processing system. Then for any two records $r_1, r_2$:

$$
t_e(r_1) < t_e(r_2) \nRightarrow t_a(r_1) < t_a(r_2)
$$

That is, the partial order relation of event time **does not maintain isomorphism** with the partial order relation of arrival time. This out-of-order characteristic makes window aggregation based on arrival order potentially produce **non-deterministic results**.

### 1.2 Time Semantics Selection Dilemma

Stream processing systems typically provide three time semantics, each with its applicable boundaries [^2][^4]:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Time Semantics Selection Matrix                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Event Time                                                             │
│   ├── Definition: Business timestamp when data is generated              │
│   ├── Characteristic: Decoupled from arrival order, guarantees result    │
│   │   determinism                                                        │
│   ├── Cost: Requires Watermark management and late data handling         │
│   └── Applicable: Financial transactions, user behavior analysis, IoT    │
│       monitoring, etc. requiring correctness                             │
│                                                                         │
│   Processing Time                                                        │
│   ├── Definition: Local system time when operator processes              │
│   ├── Characteristic: Lowest latency, no state overhead                  │
│   ├── Cost: Results depend on execution moment, non-deterministic        │
│   └── Applicable: Real-time monitoring, approximate statistics,          │
│       alerting systems                                                   │
│                                                                         │
│   Ingestion Time                                                         │
│   ├── Definition: System time when data enters Source                    │
│   ├── Characteristic: Monotonically increasing, no user Watermark        │
│   │   configuration needed                                               │
│   ├── Cost: Cannot handle disorder at Source                             │
│   └── Applicable: Log analysis, simple ETL, etc. without clock source    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Correctness Guarantee Hierarchy** [^4]:

$$
\text{Processing Time} \subset \text{Ingestion Time} \subset \text{Event Time}
$$

Any Processing Time computation can be simulated by Event Time (by treating processing time as pseudo event time), but not vice versa. Therefore, in the correctness dimension, Event Time is a superset of the other two semantics.

### 1.3 Specific Manifestations in Business Scenarios

**Scenario 1: Out-of-order Transactions in Financial Risk Control** [^5]

In real-time risk control systems, multiple transactions from the same user may arrive out of order due to different network paths:

```
Timeline:
─────────────────────────────────────────────────────────────►

t=10:00:05  Transaction A ($100) ──────┐
                                      │ Network latency difference
                                      ▼
t=10:00:03  Transaction B ($5000) ───►[Processing Node]──── Arrival order: B, A
                                      ▲
t=10:00:01  Transaction C ($50) ──────┘

Event time order: C (10:00:01) → B (10:00:03) → A (10:00:05)
Arrival order:     C → B → A (fortunately consistent)

Another possibility:
t=10:00:05  Transaction A ───────────►┐
                                      │ A takes slower path
                                      ▼
t=10:00:03  Transaction B ───────────►[Processing Node]──── Arrival order: B, A
                                      ▲
t=10:00:01  Transaction C ───────────►┘

Arrival order: B (10:00:03) → A (10:00:05) → C (10:00:01)?
        (C is late, smallest event time but arrives last)
```

If Processing Time is used for 10:00:00-10:00:10 window aggregation, late event C would be incorrectly assigned to the next window, causing risk control rule misses.

**Scenario 2: IoT Sensor Data Out-of-Order** [^6]

In smart manufacturing scenarios, edge gateways batch-report sensor data:

| Sensor | Event Time | Edge Cache Time | Arrival Time | Disorder Delay |
|--------|------------|-----------------|--------------|----------------|
| Temperature-01 | 10:00:00 | 10:00:10 | 10:00:10 | 0s |
| Temperature-02 | 10:00:02 | 10:00:10 | 10:00:10 | 0s |
| Vibration-01 | 10:00:01 | 10:00:15 | 10:00:15 | +13s (relative to Temperature-02) |
| Pressure-01 | 10:00:03 | 10:00:12 | 10:00:12 | -2s (arrives early) |

Vibration-01's event time is between Temperature-01 and Temperature-02, but arrives 15 seconds late due to gateway batching strategy. If the window triggers at 10:00:10, Vibration-01 will be missed, causing incorrect device status judgment.

**Scenario 3: CDC Data Synchronization Timing Issues** [^7]

In database CDC (Change Data Capture) scenarios, multiple change events for the same row must be processed in transaction commit order:

```
Database Transaction Log:  UPDATE row_1 (ts=100) → UPDATE row_1 (ts=105) → DELETE row_1 (ts=110)
                    │
                    ▼ (Network partition)
Kafka Partition:    [UPDATE ts=100] [DELETE ts=110] [UPDATE ts=105] ← Out of order!
                    │
                    ▼ (Flink processing)
If processed by arrival order:  DELETE first then UPDATE → Wrong state (appears after deletion)
```

Therefore, CDC scenarios must use Event Time to ensure correct change order.

---

## 2. Solution

### 2.1 Core Concept Definitions

**Definition 1: Event Time** [^3][^4]

Let $\text{Record}$ be the set of all possible records in the stream, and $\mathbb{T} = \mathbb{R}_{\geq 0}$ be the time domain. Event time is a mapping from records to the time domain:

$$
t_e: \text{Record} \to \mathbb{T}
$$

For any record $r \in \text{Record}$, $t_e(r)$ represents the timestamp of when the record was generated in business logic, attached by the data source when generating the record, and **cannot be modified by the stream processing system** in subsequent processing.

**Definition 2: Watermark** [^3][^4]

Watermark is a special progress beacon injected by the stream processing system into the data stream, formalized as a monotonic function from data stream to time domain:

$$
wm: \text{Stream} \to \mathbb{T} \cup \{+\infty\}
$$

Let the currently observed watermark value be $w$, its semantic assertion is:

$$
\forall r \in \text{Stream}_{\text{future}}. \; t_e(r) \geq w \lor \text{Late}(r, w)
$$

That is: All records with event time strictly less than $w$ have either already arrived and been processed, or have been deemed "late" by the system and will no longer be accepted by the target window.

**Definition 3: Late Data** [^3][^4]

Given a configured allowed latency parameter $L \geq 0$ (allowed lateness), the "late" determination predicate for record $r$ relative to current watermark $w$ is defined as:

$$
\text{Late}(r, w) \iff t_e(r) \leq w - L
$$

When $L = 0$, the condition simplifies to $t_e(r) \leq w$. When $L > 0$, the system retains a grace period after the watermark passes the window end time.

### 2.2 Watermark Mechanism Principles

**Periodic Generation Strategy** [^4]:

At the Source side, the most common Watermark generation strategy is based on maximum observed event time minus a fixed delay:

$$
w(t) = \max_{r \in \text{Observed}(t)} t_e(r) - \delta
$$

Where $\delta \geq 0$ is the maximum out-of-order boundary tolerated by the system.

**Watermark Propagation Rules** [^3]:

| Operator Type | Propagation Rule | Description |
|---------------|------------------|-------------|
| **Single Input Single Output** (Map/Filter/FlatMap) | $w_{\text{out}} = w_{\text{in}} - d_{\text{proc}}$ | Direct pass-through, can add fixed processing delay |
| **Multi Input Single Output** (Join/Union/CoGroup) | $w_{\text{out}} = \min_i w_{\text{in}_i}$ | Take minimum of all inputs, ensuring safety |
| **Multi Output** (Side Output) | Each output inherits input Watermark | Maintain consistency |

**Watermark Monotonicity Theorem** [^3]:

> **Thm-S-09-01**: Let $\mathcal{G} = (V, E, P, \Sigma, \mathbb{T})$ be a Dataflow DAG using event time semantics. For any operator $v \in V$ in the graph, its output Watermark sequence satisfies monotonic non-decrease:
>
> $$
> \forall v \in V, \; \forall t_1 \leq t_2: \quad w_v(t_1) \leq w_v(t_2)
> $$

This theorem guarantees the **uniqueness** of window trigger timing, preventing the same window from triggering repeatedly due to Watermark regression.

### 2.3 Late Data Handling Strategies

Flink provides three levels of late data handling mechanisms [^4][^6]:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Late Data Handling Strategy Hierarchy               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Level 1: Within Watermark Boundary (Default)                            │
│  ─────────────────────────────────                                      │
│  Condition: t_e(r) > current_watermark                                  │
│  Behavior: Normal inclusion in window calculation                        │
│  Configuration: WatermarkStrategy.forBoundedOutOfOrderness(Duration.ofSeconds(5))│
│                                                                         │
│  Level 2: Allowed Lateness                                               │
│  ───────────────────────────────────                                    │
│  Condition: window_end_time ≤ t_e(r) ≤ window_end_time + L              │
│  Behavior: Triggers window update, may output corrected results           │
│  Configuration: .allowedLateness(Time.minutes(10))                      │
│  Note: State is retained longer, increasing storage cost                 │
│                                                                         │
│  Level 3: Side Output                                                    │
│  ─────────────────────────────                                          │
│  Condition: t_e(r) < current_watermark - L (completely late)            │
│  Behavior: Routed to side output stream for audit/offline backfill       │
│  Configuration: .sideOutputLateData(lateDataTag)                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Exactly-Once Semantic Guarantee** [^4]:

Under Flink's Checkpoint mechanism, introducing Allowed Lateness does not break Exactly-Once semantics:

1. Window triggers first time and outputs result $v_1$
2. During Allowed Lateness period, late data arrives triggering window update, outputting corrected results $v_2, v_3, ...$
3. These subsequent outputs are "updated results" rather than "duplicate outputs", usually with timestamps or version identifiers
4. Checkpoint guarantees consistency of state recovery, confirmed results will not be output repeatedly

### 2.4 Pattern Structure Diagram

```mermaid
graph TB
    subgraph "Source Layer"
        S1[Data Source A<br/>Event Time: t_e]
        S2[Data Source B<br/>Event Time: t_e]
    end

    subgraph "Timestamp Assignment"
        TA1[Timestamp Assigner<br/>extract t_e from record]
        TA2[Timestamp Assigner<br/>extract t_e from record]
    end

    subgraph "Watermark Generation"
        WG1[Watermark Generator<br/>wm = max(t_e) - δ]
        WG2[Watermark Generator<br/>wm = max(t_e) - δ]
    end

    subgraph "Stream Processing"
        SP1[Map/Filter<br/>Pass-through]
        SP2[Join/Union<br/>wm_out = min(wm_in)]
        SP3[Window Operator<br/>Trigger: wm ≥ window_end]
    end

    subgraph "Output Handling"
        OH1[Main Output<br/>On-time Results]
        OH2[Side Output<br/>Late Data]
        OH3[State Backend<br/>RocksDB]
    end

    S1 --> TA1 --> WG1 --> SP1
    S2 --> TA2 --> WG2 --> SP2
    SP1 --> SP2 --> SP3
    SP3 --> OH1
    SP3 -.->|Late Data| OH2
    SP3 -.->|State| OH3

    style WG1 fill:#fff9c4,stroke:#f57f17
    style WG2 fill:#fff9c4,stroke:#f57f17
    style SP3 fill:#c8e6c9,stroke:#2e7d32
    style OH2 fill:#ffcdd2,stroke:#c62828
```

**Component Responsibility Description**:

| Component | Responsibility | Key Configuration |
|-----------|---------------|-------------------|
| Timestamp Assigner | Extract event timestamp from records | `SerializableTimestampAssigner` |
| Watermark Generator | Periodically generate Watermark | `forBoundedOutOfOrderness()`, `withIdleness()` |
| Window Operator | Trigger windows based on Watermark | `allowedLateness()`, `sideOutputLateData()` |
| Side Output | Capture completely late data | `OutputTag<>` |

---

## 3. Implementation

### 3.1 Flink Watermark Generation Strategies

**Strategy 1: Ordered Stream** [^4][^6]

Applicable to Kafka single partition, ordered logs, and similar scenarios:

```scala
import org.apache.flink.api.common.eventtime.{SerializableTimestampAssigner, WatermarkStrategy}
import java.time.Duration

// Ordered stream: No disorder, Watermark equals current max event time
val orderedWatermarkStrategy: WatermarkStrategy[SensorReading] =
  WatermarkStrategy
    .forMonotonousTimestamps[SensorReading]()
    .withTimestampAssigner(new SerializableTimestampAssigner[SensorReading] {
      override def extractTimestamp(element: SensorReading, recordTimestamp: Long): Long =
        element.timestamp
    })
    // Idle source handling: No data for 2 minutes considered idle
    .withIdleness(Duration.ofMinutes(2))
```

**Strategy 2: Bounded Out-of-Orderness** [^4][^5][^6]

The most commonly used strategy, applicable to network transmission disorder scenarios:

```scala
// Out-of-order transaction stream: Tolerate maximum 10 seconds disorder
val boundedWatermarkStrategy: WatermarkStrategy[Transaction] =
  WatermarkStrategy
    .forBoundedOutOfOrderness[Transaction](Duration.ofSeconds(10))
    .withTimestampAssigner((txn, _) => txn.timestamp)
    .withIdleness(Duration.ofMinutes(1))

// Apply to DataStream
val streamWithWatermark: DataStream[Transaction] = env
  .fromSource(kafkaSource, boundedWatermarkStrategy, "Transaction Source")
```

**Strategy 3: Custom Generator** [^4]

Applicable to scenarios where data carries special punctuation (such as heartbeat packets):

```scala
import org.apache.flink.api.common.eventtime._

// Punctuation-based Watermark generator
class PunctuatedWatermarkGenerator extends WatermarkGenerator[SensorReading] {
  private var maxTimestamp = Long.MinValue

  override def onEvent(
    event: SensorReading,
    eventTimestamp: Long,
    output: WatermarkOutput
  ): Unit = {
    maxTimestamp = math.max(maxTimestamp, eventTimestamp)

    // Special marker packet triggers Watermark advance
    if (event.isHeartbeatPacket) {
      output.emitWatermark(new Watermark(maxTimestamp))
    }
  }

  override def onPeriodicEmit(output: WatermarkOutput): Unit = {
    // Periodic emission to ensure progress is not blocked
    if (maxTimestamp > Long.MinValue) {
      output.emitWatermark(new Watermark(maxTimestamp - 1))
    }
  }
}
```

### 3.2 Window Aggregation and Late Data Handling

**Complete Example: IoT Sensor Session Window** [^6]

```scala
import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.api.windowing.assigners.SessionWindows
import org.apache.flink.streaming.api.windowing.time.Time
import org.apache.flink.streaming.api.scala.function.ProcessWindowFunction
import org.apache.flink.util.Collector

// Define side output tag
val lateDataTag = OutputTag[SensorReading]("late-data")

// Session window with late data handling
val sessionStream = sensorStream
  // 1. Assign timestamps and Watermark
  .assignTimestampsAndWatermarks(
    WatermarkStrategy
      .forBoundedOutOfOrderness[SensorReading](Duration.ofSeconds(15))
      .withTimestampAssigner((reading, _) => reading.timestamp)
      .withIdleness(Duration.ofMinutes(2))
  )

  // 2. Partition by device ID
  .keyBy(_.deviceId)

  // 3. Define session window (closes after 10 minutes of inactivity)
  .window(EventTimeSessionWindows.withGap(Time.minutes(10)))

  // 4. Allow 30 seconds latency (can still update after Watermark passes)
  .allowedLateness(Time.seconds(30))

  // 5. Side output captures completely late data
  .sideOutputLateData(lateDataTag)

  // 6. Window processing function
  .process(new DeviceSessionAggregateFunction())

// Process main output
sessionStream.addSink(new InfluxDBSink())

// Process late data
val lateDataStream: DataStream[SensorReading] = sessionStream.getSideOutput(lateDataTag)
lateDataStream.addSink(new LateDataAuditSink())
```

**Window Aggregation Function Implementation** [^6]:

```scala
class DeviceSessionAggregateFunction
  extends ProcessWindowFunction[SensorReading, DeviceSession, String, SessionWindow] {

  private var deviceState: ValueState[DeviceState] = _

  override def open(parameters: Configuration): Unit = {
    deviceState = getRuntimeContext.getState(
      new ValueStateDescriptor("device-state", classOf[DeviceState])
    )
  }

  override def process(
    deviceId: String,
    context: Context,
    readings: Iterable[SensorReading],
    out: Collector[DeviceSession]
  ): Unit = {
    // Sort by event time for processing (handles out-of-order arrival)
    val sortedReadings = readings.toVector.sortBy(_.timestamp)

    // Calculate session statistics
    val statistics = calculateStatistics(sortedReadings)

    // Detect anomalies
    val anomalies = detectAnomalies(sortedReadings)

    // Build session result
    val session = DeviceSession(
      deviceId = deviceId,
      sessionStart = context.window.getStart,
      sessionEnd = context.window.getEnd,
      readings = sortedReadings,
      statistics = statistics,
      anomalies = anomalies
    )

    out.collect(session)
  }
}
```

### 3.3 Watermark Propagation for Multi-Input Operators

**Join Operation Watermark Handling** [^3][^4]:

```scala
// Two-stream Join: Watermark takes minimum value
val joinedStream = transactionStream
  .join(userProfileStream)
  .where(_.userId)
  .equalTo(_.userId)
  .window(TumblingEventTimeWindows.of(Time.minutes(5)))
  .apply(new TransactionEnrichmentFunction())
```

In the above Join, the output Watermark is:

$$
w_{\text{out}} = \min(w_{\text{transaction}}, w_{\text{profile}})
$$

This means that if userProfileStream progresses slowly, it will block the entire Join window trigger.

**Multi-source Union Idle Source Handling** [^4][^6]:

```scala
// Multi-data source Union scenario
val sourceA = env.fromSource(kafkaSourceA,
  WatermarkStrategy.forBoundedOutOfOrderness[Event](Duration.ofSeconds(5)),
  "Source A"
)

val sourceB = env.fromSource(kafkaSourceB,
  WatermarkStrategy.forBoundedOutOfOrderness[Event](Duration.ofSeconds(10))
    .withIdleness(Duration.ofMinutes(5)),  // Key: Idle source handling
  "Source B"
)

val unionedStream = sourceA.union(sourceB)
```

The `withIdleness()` configuration ensures that when Source B has no data for 5 minutes, the system marks it as idle and no longer includes it in Watermark minimum calculations, preventing global progress blocking.

### 3.4 Idle Source Handling

**Problem Description**: In multi-input operators, if one input source has no data for a long time (such as a payment system with no transactions at night), its stagnant Watermark will block the entire DAG's progress through minimum value propagation.

**Solution** [^4][^6]:

```scala
// Idle source detection configuration
WatermarkStrategy
  .forBoundedOutOfOrderness[Event](Duration.ofSeconds(10))
  .withIdleness(Duration.ofMinutes(5))  // No data for 5 minutes considered idle
```

**Implementation Principle**:

```
Normal case:
Source A wm=15 ──┐
                 ├─► min(15, 10) = 10 ──► Window triggers
Source B wm=10 ──┘

After Source B becomes idle (5 minutes no data):
Source A wm=25 ──┐
                 ├─► Source B marked as idle, only consider Source A
Source B wm=10 ──┘ (idle)

Output wm=25 ──► Window triggers normally
```

---

## 4. When to Use

### 4.1 Recommended Scenarios

| Scenario | Reason | Typical Watermark Configuration |
|----------|--------|--------------------------------|
| **Financial Transaction Risk Control** [^5] | Requires precise aggregation by transaction time, reproducible | `forBoundedOutOfOrderness(500ms)` |
| **User Behavior Analysis** [^5] | Out-of-order click streams need correct attribution | `forBoundedOutOfOrderness(10s)` |
| **IoT Sensor Monitoring** [^6] | Network latency causes data disorder, edge gateways batch report | `forBoundedOutOfOrderness(15s) + withIdleness(2min)` |
| **CDC Data Synchronization** [^7] | Ensures correct change order, avoids state errors | `forBoundedOutOfOrderness(1s)` |
| **Real-time Recommendation System** [^5] | Feature freshness depends on correct event time windows | `forBoundedOutOfOrderness(5s)` |
| **Log Analysis** | Multi-server log aggregation, clock skew | `forBoundedOutOfOrderness(30s)` |

### 4.2 Not Recommended Scenarios

| Scenario | Reason | Alternative |
|----------|--------|-------------|
| **Real-time Monitoring Alerts** | Latency priority, approximation is sufficient | Processing Time |
| **Simple ETL (No Clock Source)** | Data source has no reliable timestamp | Ingestion Time |
| **Ultra-low Latency Requirements (<100ms)** | Watermark delay increases end-to-end latency | Processing Time + Post-correction |
| **Strictly Ordered Streams** | Additional Watermark overhead with no benefit | `forMonotonousTimestamps()` |
| **Debug/Development Phase** | Simplify problems, rapid iteration | Processing Time |

**Decision Flow Chart**:

```
Need cross-run result consistency?
├── No ──► Processing Time (Lowest latency)
└── Yes ──► Does data source carry reliable timestamp?
            ├── No ──► Ingestion Time (Simplified configuration)
            └── Yes ──► Degree of disorder?
                        ├── No disorder ──► forMonotonousTimestamps()
                        ├── Light (<1s) ──► forBoundedOutOfOrderness(1s)
                        ├── Medium (1-30s) ──► forBoundedOutOfOrderness(10-30s)
                        └── Heavy (>30s) ──► forBoundedOutOfOrderness(60s+) + Side Output
```

---

## 5. Related Patterns

| Pattern | Relation | Description |
|---------|----------|-------------|
| **Pattern 02: Windowed Aggregation** | Depends | Event time is the foundation of window aggregation, this pattern provides the time baseline [^4][^6] |
| **Pattern 03: Complex Event Processing (CEP)** | Depends | CEP pattern matching requires event time to define sequence order and time windows [^8] |
| **Pattern 04: Async I/O Enrichment** | Cooperates | When querying external services asynchronously, Watermark mechanism ensures correct handling of out-of-order responses [^5][^6] |
| **Pattern 05: State Management** | Cooperates | Keyed State combined with Event Time enables cross-session state accumulation [^6] |
| **Pattern 06: Side Output Pattern** | Cooperates | Late data is separated and processed through Side Output [^4][^6] |
| **Pattern 07: Checkpoint & Recovery** | Depends | Checkpoint persists Watermark state, ensuring monotonicity after fault recovery [^3][^4] |

**Relation to Dataflow Model** [^1][^4]:

Flink's Event Time processing mechanism is an engineering implementation of the Google Dataflow model:

- The three core concepts proposed by the Dataflow model: event time, Watermark, and window triggers, are fully implemented in Flink through APIs such as `TimeCharacteristic`, `WatermarkStrategy`, and `Trigger`
- Flink adds `Allowed Lateness` mechanism and Side Output functionality on top of the Dataflow model
- Watermark Monotonicity Theorem (Thm-S-09-01) provides the formal foundation for the Dataflow model's determinism guarantee [^3]

---

## 6. Formal Guarantees

This section establishes the formal connection between Event Time Processing pattern and the Struct/ theory layer, clarifying the theorems, definitions this pattern depends on, and the semantic guarantees it provides.

### 6.1 Dependent Formal Definitions

| Definition ID | Name | Source | Role in This Pattern |
|---------------|------|--------|---------------------|
| **Def-S-04-04** | Watermark Semantics | Struct/01.04 | Defines Watermark as a monotonic non-decreasing progress indicator ω(t) ≤ t, the core abstraction of this pattern |
| **Def-S-09-02** | Watermark Progress Semantics | Struct/02.03 | Formalizes Watermark advancement rules and late data determination conditions |
| **Def-S-07-01** | Deterministic Stream Computing System | Struct/02.01 | Event time is a component of the six-tuple for deterministic processing |
| **Def-S-08-04** | Exactly-Once Semantics | Struct/02.02 | Late data handling does not break end-to-end consistency |

### 6.2 Satisfied Formal Properties

| Theorem/Lemma ID | Name | Source | Guarantee |
|------------------|------|--------|-----------|
| **Thm-S-09-01** | Watermark Monotonicity Theorem | Struct/02.03 | Guarantees uniqueness of window trigger timing, preventing the same window from triggering repeatedly |
| **Lemma-S-04-02** | Watermark Monotonicity Lemma | Struct/01.04 | Watermark propagation maintains monotonic non-decrease in Dataflow graph |
| **Thm-S-07-01** | Stream Computing Determinism Theorem | Struct/02.01 | Pure function + FIFO + Event Time → Deterministic output |
| **Prop-S-08-01** | End-to-End Exactly-Once Decomposition | Struct/02.02 | Source ∧ Checkpoint ∧ Sink three-element conjunction |

### 6.3 Property Preservation During Pattern Composition

**Event Time + Windowed Aggregation Composition**:

- Watermark monotonicity (Thm-S-09-01) guarantees idempotence of window triggers
- Allowed Lateness mechanism introduces corrected outputs that still maintain Exactly-Once semantics

**Event Time + Checkpoint Composition**:

- Checkpoint persists Watermark state, ensuring monotonicity continuation after fault recovery
- Recovered Watermark continues advancing from checkpointed value, satisfying Lemma-S-04-02

### 6.4 Boundary Conditions and Constraints

| Constraint Condition | Formal Description | Violation Consequence |
|---------------------|-------------------|----------------------|
| Disorder Boundary L ≥ D_actual | Watermark delay parameter must be greater than or equal to actual disorder degree | Data loss or incomplete results |
| Monotonicity Preservation | ∀t₁ ≤ t₂: w(t₁) ≤ w(t₂) | Window triggers repeatedly, wrong results |
| Idle Source Handling | withIdleness(T) configuration | Stagnant Watermark blocks global progress |

### 6.5 Correspondence Between Engineering Implementation and Theory

| Theoretical Concept | Flink API | Formal Foundation |
|--------------------|-----------|------------------|
| Watermark Generation | `WatermarkStrategy.forBoundedOutOfOrderness()` | Def-S-04-04 |
| Late Data Handling | `.allowedLateness()` + `.sideOutputLateData()` | Def-S-09-02 |
| Idle Source Handling | `.withIdleness()` | Thm-S-09-01 extension |
| Event Time Extraction | `SerializableTimestampAssigner` | Def-S-07-01 |

---

## 7. References

[^1]: T. Akidau et al., "The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing," *PVLDB*, 8(12), 2015. <https://doi.org/10.14778/2824032.2824076>

[^2]: Apache Flink Documentation, "Event Time and Watermarks," 2025. <https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/>

[^3]: Watermark Monotonicity Theorem, see [Struct/02-properties/02.03-watermark-monotonicity.md](../../Struct/02-properties/02.03-watermark-monotonicity.md)

[^4]: Flink Time Semantics and Watermark, see [Flink/02-core/time-semantics-and-watermark.md](../../Flink/02-core/time-semantics-and-watermark.md)

[^5]: Financial Risk Control Real-time Fraud Detection Case, see [Flink/07-case-studies/case-financial-realtime-risk-control.md](../../Flink/09-practices/09.01-case-studies/case-financial-realtime-risk-control.md)

[^6]: IoT Stream Processing Industrial Case, see [Flink/07-case-studies/case-iot-stream-processing.md](../../Flink/09-practices/09.01-case-studies/case-iot-stream-processing.md)

[^7]: Real-time ETL Deep Analysis, see [Flink/07-case-studies/case-realtime-analytics.md](../../Flink/09-practices/09.01-case-studies/case-realtime-analytics.md)

[^8]: CEP Complex Event Processing Pattern, see [Flink/03-api-patterns/flink-cep-deep-dive.md](../../Flink/03-api/03.02-table-sql-api/flink-sql-window-functions-deep-dive.md)

---

*Document Version: v1.0 | Last Updated: 2026-04-02 | Status: Complete*

