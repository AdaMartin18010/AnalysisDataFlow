---
title: "Pattern: Event Time Processing"
translation_status: ai_translated_pending_expert_review
source_version: v4.1
last_sync: "2026-04-15"
---

# Pattern: Event Time Processing

> **Pattern ID**: 01/7 | **Series**: Knowledge/02-design-patterns | **Formalization Level**: L4-L5
>
> This pattern resolves the core tension between **out-of-order data**, **late data**, and **result determinism** in distributed stream processing, providing a Watermark-based progress tracking mechanism.

---

## Table of Contents

- [Pattern: Event Time Processing](#pattern-event-time-processing)
  - [Table of Contents](#table-of-contents)
  - [1. Definitions](#1-definitions)
    - [Def-K-02-01 (Event Time)](#def-k-02-01-event-time)
    - [Def-K-02-02 (Watermark)](#def-k-02-02-watermark)
    - [Def-K-02-03 (Late Data)](#def-k-02-03-late-data)
  - [2. Properties](#2-properties)
    - [Prop-K-02-01 (Watermark Monotonicity Propagation)](#prop-k-02-01-watermark-monotonicity-propagation)
    - [Prop-K-02-02 (Late Data Processing Semantics)](#prop-k-02-02-late-data-processing-semantics)
  - [3. Relations](#3-relations)
    - [Relation to Windowed Aggregation](#relation-to-windowed-aggregation)
    - [Relation to CEP Pattern Matching](#relation-to-cep-pattern-matching)
    - [Relation to Checkpoint Mechanism](#relation-to-checkpoint-mechanism)
  - [4. Argumentation](#4-argumentation)
    - [4.1 Temporal Challenges in Distributed Stream Processing](#41-temporal-challenges-in-distributed-stream-processing)
    - [4.2 Time Semantics Selection Argumentation](#42-time-semantics-selection-argumentation)
    - [4.3 Applicability Analysis](#43-applicability-analysis)
  - [8. Formal Guarantees](#8-formal-guarantees)
    - [8.1 Dependent Formal Definitions](#81-dependent-formal-definitions)
    - [8.2 Satisfied Formal Properties](#82-satisfied-formal-properties)
    - [8.3 Property Preservation under Pattern Composition](#83-property-preservation-under-pattern-composition)
    - [8.4 Boundary Conditions and Constraints](#84-boundary-conditions-and-constraints)
    - [8.5 Engineering Implementation and Theory Correspondence](#85-engineering-implementation-and-theory-correspondence)
  - [5. Proof / Engineering Argument](#5-proof--engineering-argument)
    - [5.1 Watermark Monotonicity Guarantee](#51-watermark-monotonicity-guarantee)
    - [5.2 Late Data Processing Exactly-Once Compatibility](#52-late-data-processing-exactly-once-compatibility)
    - [5.3 Idle Source Handling Engineering Argument](#53-idle-source-handling-engineering-argument)
  - [6. Examples](#6-examples)
    - [6.1 Flink Watermark Generation Strategies](#61-flink-watermark-generation-strategies)
    - [6.2 Window Aggregation and Late Data Handling](#62-window-aggregation-and-late-data-handling)
    - [6.3 Watermark Propagation in Multi-Input Operators](#63-watermark-propagation-in-multi-input-operators)
    - [6.4 Idle Source Handling](#64-idle-source-handling)
  - [7. Visualizations](#7-visualizations)
    - [7.1 Event Time Processing Architecture](#71-event-time-processing-architecture)
    - [7.2 Time Semantics Decision Tree](#72-time-semantics-decision-tree)
  - [9. References](#9-references)

---

## 1. Definitions

### Def-K-02-01 (Event Time)

**Definition**: Let $\text{Record}$ be the set of all possible records in a stream, and $\mathbb{T} = \mathbb{R}_{\geq 0}$ be the time domain. Event time is a mapping from records to the time domain:

$$
t_e: \text{Record} \to \mathbb{T}
$$

For any record $r \in \text{Record}$, $t_e(r)$ denotes the timestamp at which the record was generated in business logic, attached by the data source when the record is created, and **must not be modified by the stream processing system** in subsequent processing [^1][^2].

---

### Def-K-02-02 (Watermark)

**Definition**: Watermark is a special progress beacon injected by the stream processing system into the data stream, formalized as a monotonic function from the data stream to the time domain (see **Def-S-04-04**) [^3][^4]:

$$
wm: \text{Stream} \to \mathbb{T} \cup \{+\infty\}
$$

Let the currently observed watermark value be $w$. Its semantic assertion is:

$$
\forall r \in \text{Stream}_{\text{future}}. \; t_e(r) \geq w \lor \text{Late}(r, w)
$$

That is: all records with event time strictly less than $w$ have either arrived and been processed, or have been judged as "late" by the system and are no longer accepted by the target window.

---

### Def-K-02-03 (Late Data)

**Definition**: Given a configured allowed lateness parameter $L \geq 0$ (allowed lateness), the "late" judgment predicate for a record $r$ relative to the current watermark $w$ is defined as (see **Def-S-09-02**) [^3][^4]:

$$
\text{Late}(r, w) \iff t_e(r) \leq w - L
$$

When $L = 0$, the condition simplifies to $t_e(r) \leq w$. When $L > 0$, the system retains a grace period after the watermark passes the window end time.

---

## 2. Properties

### Prop-K-02-01 (Watermark Monotonicity Propagation)

**Proposition**: In a Dataflow DAG using event time semantics, the output Watermark sequence of any operator satisfies monotonic non-decreasing (**Thm-S-09-01**).

For any operator $v \in V$ in the graph:

$$
\forall t_1 \leq t_2: \quad w_v(t_1) \leq w_v(t_2)
$$

**Derivation**:

1. Source-side Watermark generation is based on the maximum observed event time minus a fixed delay, naturally monotonic
2. Single-input operators pass through the Watermark directly, preserving monotonicity (**Lemma-S-04-02**)
3. Multi-input operators take the minimum of all input Watermarks; the minimum function preserves the monotonicity of each input
4. Therefore Watermark never regresses throughout the entire DAG

**Engineering significance**: This property guarantees the **uniqueness** of window trigger moments, preventing the same window from being triggered repeatedly due to Watermark regression.

---

### Prop-K-02-02 (Late Data Processing Semantics)

**Proposition**: Under Flink's Checkpoint mechanism, introducing Allowed Lateness does not break end-to-end ExactlyOnce semantics (**Prop-S-08-01**).

**Derivation**:

1. When the window triggers for the first time, it outputs result $v_1$
2. During the Allowed Lateness period, late data arrives and triggers window updates, outputting corrected results $v_2, v_3, ...$
3. These subsequent outputs are "updated results" rather than "duplicate outputs", typically carrying timestamps or version identifiers
4. Checkpoint guarantees consistent state recovery; confirmed results will not be output again (**Thm-S-18-01**)

**Constraint**: Allowed Lateness increases state retention time; a trade-off between storage cost and result completeness is required.

---

## 3. Relations

### Relation to Windowed Aggregation

Event time is the fundamental time basis for windowed aggregation [^4][^6]:

- **Tumbling Window**, **Sliding Window**, and **Session Window** boundaries are all defined based on event time
- Watermark monotonicity (**Thm-S-09-01**) guarantees the idempotence of window triggering
- Window aggregation results can serve as atomic event inputs for downstream CEP or stateful computation

### Relation to CEP Pattern Matching

CEP pattern matching relies on event time to define sequence order and time windows [^8]:

- The `.within(Time)` constraint in patterns requires event time as the measurement baseline
- Late events may break the integrity of sequence detection and must be isolated via side outputs
- Watermark advancement drives the timeout cleanup mechanism in CEP

### Relation to Checkpoint Mechanism

Checkpoint is the fault-tolerance guarantee for the correctness of event time semantics [^3][^4]:

- Checkpoint persists Watermark state, ensuring monotonicity continuity after failure recovery
- The recovered Watermark continues advancing from the checkpointed value, satisfying **Lemma-S-04-02**
- End-to-end ExactlyOnce requires the conjunction of replayable Source, Checkpoint consistency, and transactional Sink (**Thm-S-18-01**)

---

## 4. Argumentation

### 4.1 Temporal Challenges in Distributed Stream Processing

In distributed stream processing systems, the **physical arrival order** of data records is fundamentally inconsistent with their **business occurrence order (event time)**. This inconsistency stems from the following factors [^1][^2]:

| Factor | Description | Typical Delay Range |
|--------|-------------|---------------------|
| **Network latency** | Network delay from data generation to transmission to processing nodes | 10ms - seconds |
| **Backpressure** | Slow downstream processing causing upstream data backlog | Seconds - minutes |
| **Retransmission** | Data retransmission after network packet loss | Seconds - tens of seconds |
| **Clock skew** | Inconsistency of system clocks among distributed nodes | Milliseconds - seconds |
| **Batch transmission** | Bulk reporting by edge gateways to save bandwidth | Seconds - minutes |

**Formal Description** [^3]:

Let the event time of record $r$ be $t_e(r)$, and its arrival time at the processing system be $t_a(r)$. Then for any two records $r_1, r_2$:

$$
t_e(r_1) < t_e(r_2) \nRightarrow t_a(r_1) < t_a(r_2)
$$

That is, the partial order relation of event time **does not preserve isomorphism** with the partial order relation of arrival time. This out-of-order characteristic makes window aggregation based on arrival order potentially produce **non-deterministic results**.

**Business Scenario Manifestations**:

- **Financial risk control**: Multiple transactions of the same user may arrive out of order due to different network paths. If Processing Time windows are used, late events will be incorrectly assigned to the next window, causing risk rule misses [^5]
- **IoT monitoring**: Edge gateways batch-reporting cause sensor data to arrive out of order. If windows trigger before the Watermark, critical data will be omitted [^6]
- **CDC synchronization**: Multiple change events for the same row must be processed in transaction commit order. Out-of-order DELETE/UPDATE will lead to state errors [^7]

---

### 4.2 Time Semantics Selection Argumentation

Stream processing systems typically provide three time semantics, each with its applicable boundary [^2][^4]:

| Semantics | Definition | Characteristics | Cost | Applicable Scenarios |
|-----------|------------|-----------------|------|----------------------|
| **Event Time** | Business timestamp when data is generated | Decoupled from arrival order, guarantees result determinism | Requires Watermark management and late data handling | Financial transactions, user behavior analysis, IoT monitoring |
| **Processing Time** | Local system time when the operator processes | Lowest latency, no state overhead | Results depend on execution moment, non-deterministic | Real-time monitoring, approximate statistics, alerting systems |
| **Ingestion Time** | System time when data enters the Source | Monotonically increasing, no user-configured Watermark needed | Cannot handle out-of-order at the Source | Log analysis, simple ETL |

**Correctness Guarantee Hierarchy** [^4]:

$$
\text{Processing Time} \subset \text{Ingestion Time} \subset \text{Event Time}
$$

Any Processing Time computation can be simulated by Event Time (by treating processing time as pseudo event time), but not vice versa. Therefore, in the correctness dimension, Event Time is a superset of the other two semantics.

---

### 4.3 Applicability Analysis

**Recommended Scenarios** [^5][^6]:

| Scenario | Rationale | Typical Watermark Configuration |
|----------|-----------|--------------------------------|
| **Financial transaction risk control** | Requires precise aggregation by transaction time, reproducible results | `forBoundedOutOfOrderness(500ms)` |
| **User behavior analysis** | Out-of-order click streams need correct attribution | `forBoundedOutOfOrderness(10s)` |
| **IoT sensor monitoring** | Network latency causes out-of-order data, edge gateways batch-report | `forBoundedOutOfOrderness(15s) + withIdleness(2min)` |
| **CDC data synchronization** | Ensures correct change order, prevents state errors | `forBoundedOutOfOrderness(1s)` |
| **Real-time recommendation system** | Feature freshness depends on correct event time windows | `forBoundedOutOfOrderness(5s)` |

**Not Recommended Scenarios** [^4]:

| Scenario | Rationale | Alternative |
|----------|-----------|-------------|
| **Real-time monitoring alerts** | Latency priority, approximation is sufficient | Processing Time |
| **Simple ETL (no clock source)** | Data source lacks reliable timestamp | Ingestion Time |
| **Ultra-low latency requirement (<100ms)** | Watermark delay increases end-to-end latency | Processing Time + post-hoc correction |

---

## 8. Formal Guarantees

This section establishes the formal connection between the Event Time Processing pattern and the Struct/ theoretical layer, clarifying the theorems, definitions this pattern depends on, and the semantic guarantees it provides.

### 8.1 Dependent Formal Definitions

| Definition ID | Name | Source | Role in This Pattern |
|---------------|------|--------|----------------------|
| **Def-S-04-04** | Watermark semantics | Struct/01.04 | Defines Watermark as a monotonic non-decreasing progress indicator $\omega(t) \leq t$; core abstraction of this pattern |
| **Def-S-09-02** | Watermark progress semantics | Struct/02.03 | Formalizes Watermark advancement rules and late data judgment conditions |
| **Def-S-07-01** | Deterministic streaming system | Struct/02.01 | Event time is a component of the sextuple for achieving deterministic processing |
| **Def-S-08-04** | ExactlyOnce semantics | Struct/02.02 | Late data handling does not break end-to-end consistency |

### 8.2 Satisfied Formal Properties

| Theorem/Lemma ID | Name | Source | Guarantee |
|------------------|------|--------|-----------|
| **Thm-S-09-01** | Watermark monotonicity theorem | Struct/02.03 | Guarantees uniqueness of window trigger moments, preventing the same window from being triggered repeatedly |
| **Lemma-S-04-02** | Watermark monotonicity lemma | Struct/01.04 | Watermark propagation in Dataflow graphs preserves monotonic non-decreasing |
| **Thm-S-07-01** | Streaming determinism theorem | Struct/02.01 | Pure function + FIFO + event time $\to$ deterministic output |
| **Prop-S-08-01** | End-to-end ExactlyOnce decomposition | Struct/02.02 | Source $\land$ Checkpoint $\land$ Sink three-factor conjunction |

### 8.3 Property Preservation under Pattern Composition

**Event Time + Windowed Aggregation Composition**:

- Watermark monotonicity (**Thm-S-09-01**) guarantees idempotence of window triggering
- The corrected outputs introduced by the Allowed Lateness mechanism still maintain ExactlyOnce semantics

**Event Time + Checkpoint Composition**:

- Checkpoint persists Watermark state, ensuring monotonicity continuity after failure recovery
- The recovered Watermark continues advancing from the checkpointed value, satisfying **Lemma-S-04-02**

### 8.4 Boundary Conditions and Constraints

| Constraint | Formal Description | Violation Consequence |
|------------|--------------------|-----------------------|
| Out-of-order boundary $L \geq D_{\text{actual}}$ | Watermark delay parameter must be greater than or equal to actual out-of-order degree | Data loss or incomplete results |
| Monotonicity preservation | $\forall t_1 \leq t_2: w(t_1) \leq w(t_2)$ | Window repeated triggering, incorrect results |
| Idle source handling | `withIdleness(T)` configuration | Stalled Watermark blocks global progress |

### 8.5 Engineering Implementation and Theory Correspondence

| Theoretical Concept | Flink API | Formal Foundation |
|---------------------|-----------|-------------------|
| Watermark generation | `WatermarkStrategy.forBoundedOutOfOrderness()` | **Def-S-04-04** |
| Late data handling | `.allowedLateness()` + `.sideOutputLateData()` | **Def-S-09-02** |
| Idle source handling | `.withIdleness()` | **Thm-S-09-01** extension |
| Event time extraction | `SerializableTimestampAssigner` | **Def-S-07-01** |

---

## 5. Proof / Engineering Argument

### 5.1 Watermark Monotonicity Guarantee

**Theorem Statement** (citing **Thm-S-09-01**) [^3]:

> Let $\mathcal{G} = (V, E, P, \Sigma, \mathbb{T})$ be a Dataflow DAG using event time semantics. For any operator $v \in V$ in the graph, its output Watermark sequence satisfies monotonic non-decreasing:
> $$\forall v \in V, \; \forall t_1 \leq t_2: \quad w_v(t_1) \leq w_v(t_2)$$

**Engineering Argumentation**:

1. **Source side**: Watermark generation strategy is based on $\max(t_e) - \delta$. Since $\max(t_e)$ is monotonic non-decreasing, the generated Watermark is also monotonic non-decreasing
2. **Single-input operator** (Map/Filter): $w_{\text{out}} = w_{\text{in}} - d_{\text{proc}}$, direct pass-through preserves monotonicity
3. **Multi-input operator** (Join/Union): $w_{\text{out}} = \min_i w_{\text{in}_i}$, the minimum function preserves monotonicity given each input is monotonic
4. Therefore, there is no path in the dataflow graph where Watermark regresses

This theorem guarantees the **uniqueness** of window trigger moments, preventing the same window from being triggered repeatedly due to Watermark regression, and is the theoretical foundation of event time semantics correctness.

---

### 5.2 Late Data Processing ExactlyOnce Compatibility

**Engineering Argumentation Goal**: Prove that Flink jobs can still maintain end-to-end ExactlyOnce semantics when Allowed Lateness and Side Output are enabled.

**Argumentation Structure**:

1. **State consistency**: Window state (including not-yet-triggered windows and windows within the allowed lateness period) is persisted through the Checkpoint mechanism (**Thm-S-17-01**)
2. **Output determinism**: Multiple triggers of the same window (first trigger + late updates) are deterministic, because trigger conditions depend only on Watermark advancement and event time (**Thm-S-07-01**)
3. **No duplicate output**: If the Sink uses transactional two-phase commit (2PC), only outputs after a successful Checkpoint are committed; after failure recovery, uncommitted transactions are rolled back and recomputed (**Thm-S-18-01**)
4. **No data loss**: The Source replays from the offset recorded in the Checkpoint, ensuring all data is processed at least once (**Lemma-S-18-01**)

In summary, the combination of Event Time + Allowed Lateness + Checkpoint + Transactional Sink satisfies end-to-end ExactlyOnce.

---

### 5.3 Idle Source Handling Engineering Argument

**Problem**: In multi-input operators, if one input source has no data for a long time, its stalled Watermark will propagate through the minimum value and block the progress of the entire DAG.

**Engineering correctness of the solution**:

Flink's `withIdleness(Duration)` mechanism introduces idle detection at the Source side:

1. When a Source produces no records for the configured duration $T$, it is marked as `IDLE`
2. The idle Source no longer participates in downstream Watermark minimum calculations
3. When the Source resumes data production, its Watermark rejoins the calculation starting from the latest event time

**Correctness guarantee**: This mechanism does not affect result correctness, because:

- During the idle period, there is indeed no new data being produced, so there is no need to wait for its Watermark advancement to trigger windows
- The recovered Watermark is generated from the actual event time of the data, and will not introduce false time progress
- If an idle Source resumes with event times earlier than the current global Watermark, the data is correctly judged as late and handled through side output

---

## 6. Examples

### 6.1 Flink Watermark Generation Strategies

**Strategy 1: Ordered Stream** [^4][^6]

Applicable to Kafka single partitions, ordered logs, and similar scenarios:

```scala
import org.apache.flink.api.common.eventtime.{SerializableTimestampAssigner, WatermarkStrategy}
import java.time.Duration

// Ordered stream: no out-of-order, Watermark equals current max event time
val orderedWatermarkStrategy: WatermarkStrategy[SensorReading] =
  WatermarkStrategy
    .forMonotonousTimestamps[SensorReading]()
    .withTimestampAssigner(new SerializableTimestampAssigner[SensorReading] {
      override def extractTimestamp(element: SensorReading, recordTimestamp: Long): Long =
        element.timestamp
    })
    // Idle source handling: no data within 2 minutes is considered idle
    .withIdleness(Duration.ofMinutes(2))
```

**Strategy 2: Bounded Out-of-Orderness** [^4][^5][^6]

The most commonly used strategy, applicable to out-of-order scenarios caused by network transmission:

```scala
// Out-of-order transaction stream: tolerate up to 10 seconds of out-of-orderness
val boundedWatermarkStrategy: WatermarkStrategy[Transaction] =
  WatermarkStrategy
    .forBoundedOutOfOrderness[Transaction](Duration.ofSeconds(10))
    .withTimestampAssigner((txn, _) => txn.timestamp)
    .withIdleness(Duration.ofMinutes(1))

// Applied to DataStream
val streamWithWatermark: DataStream[Transaction] = env
  .fromSource(kafkaSource, boundedWatermarkStrategy, "Transaction Source")
```

**Strategy 3: Custom Generator** [^4]

Applicable to scenarios where data carries special punctuation (e.g., heartbeat packets):

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

    // Special marker packet triggers Watermark advancement
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

---

### 6.2 Window Aggregation and Late Data Handling

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

  // 3. Define session window (close after 10 minutes of inactivity)
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

**Window Aggregate Function Implementation** [^6]:

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

    // Compute session statistics
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

---

### 6.3 Watermark Propagation in Multi-Input Operators

**Join Operation Watermark Handling** [^3][^4]:

```scala
// Two-stream Join: Watermark takes the minimum
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

This means that if the userProfileStream progresses slowly, it will block the window triggering of the entire Join.

**Multi-Source Union Idle Source Handling** [^4][^6]:

```scala
// Multi-data-source Union scenario
val sourceA = env.fromSource(kafkaSourceA,
  WatermarkStrategy.forBoundedOutOfOrderness[Event](Duration.ofSeconds(5)),
  "Source A"
)

val sourceB = env.fromSource(kafkaSourceB,
  WatermarkStrategy.forBoundedOutOfOrderness[Event](Duration.ofSeconds(10))
    .withIdleness(Duration.ofMinutes(5)),  // Key: idle source handling
  "Source B"
)

val unionedStream = sourceA.union(sourceB)
```

The `withIdleness()` configuration ensures that when Source B has no data for 5 minutes, the system marks it as idle and no longer includes it in Watermark minimum calculations, preventing global progress from being blocked.

---

### 6.4 Idle Source Handling

**Problem Description**: In multi-input operators, if one input source has no data for a long time (e.g., a payment system with no transactions at night), its stalled Watermark will propagate through the minimum value and block the progress of the entire DAG.

**Solution** [^4][^6]:

```scala
// Idle source detection configuration
WatermarkStrategy
  .forBoundedOutOfOrderness[Event](Duration.ofSeconds(10))
  .withIdleness(Duration.ofMinutes(5))  // No data for 5 minutes is considered idle
```

**Implementation Principle**:

```
Normal case:
Source A wm=15 ──┐
                 ├─► min(15, 10) = 10 ──► Window triggers
Source B wm=10 ──┘

After Source B becomes idle (no data for 5 minutes):
Source A wm=25 ──┐
                 ├─► Source B is marked idle, only Source A is considered
Source B wm=10 ──┘ (idle)

Output wm=25 ──► Window triggers normally
```

---

## 7. Visualizations

### 7.1 Event Time Processing Architecture

The following Mermaid diagram shows the core components and data flow of the event time processing pattern:

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
|-----------|----------------|-------------------|
| Timestamp Assigner | Extract event timestamp from records | `SerializableTimestampAssigner` |
| Watermark Generator | Periodically generate Watermark | `forBoundedOutOfOrderness()`, `withIdleness()` |
| Window Operator | Trigger windows based on Watermark | `allowedLateness()`, `sideOutputLateData()` |
| Side Output | Capture completely late data | `OutputTag<>` |

---

### 7.2 Time Semantics Decision Tree

The following decision tree helps select the appropriate time semantics for different scenarios:

```mermaid
flowchart TD
    A[Start Evaluation] --> B{Need cross-run<br/>result consistency?}
    B -->|No| C[Processing Time<br/>Lowest latency]
    B -->|Yes| D{Data source carries<br/>reliable timestamp?}
    D -->|No| E[Ingestion Time<br/>Simplified configuration]
    D -->|Yes| F{How severe is out-of-order?}
    F -->|None| G[forMonotonous<br/>Timestamps]
    F -->|Mild <1s| H[forBoundedOutOf<br/>Orderness 1s]
    F -->|Moderate 1-30s| I[forBoundedOutOf<br/>Orderness 10-30s]
    F -->|Severe >30s| J[forBoundedOutOf<br/>Orderness 60s+]<br/>+ Side Output]

    style C fill:#ffcdd2,stroke:#c62828
    style E fill:#fff9c4,stroke:#f57f17
    style G fill:#c8e6c9,stroke:#2e7d32
    style H fill:#c8e6c9,stroke:#2e7d32
    style I fill:#c8e6c9,stroke:#2e7d32
    style J fill:#e1bee7,stroke:#6a1b9a
```

---

## 9. References

[^1]: T. Akidau et al., "The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing," *PVLDB*, 8(12), 2015. <https://doi.org/10.14778/2824032.2824076>

[^2]: Apache Flink Documentation, "Event Time and Watermarks," 2025. <https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/>

[^3]: Watermark Monotonicity Theorem, see [Struct/02-properties/02.03-watermark-monotonicity.md](../../Struct/02-properties/02.03-watermark-monotonicity.md)

[^4]: Flink Time Semantics and Watermark, see [Flink/02-core/time-semantics-and-watermark.md](../../Flink/02-core/time-semantics-and-watermark.md)

[^5]: Financial Risk Control Real-time Fraud Detection Case, see [Flink/09-practices/09.01-case-studies/case-financial-realtime-risk-control.md](../../Flink/09-practices/09.01-case-studies/case-financial-realtime-risk-control.md)

[^6]: IoT Stream Processing Industrial Case, see [Flink/09-practices/09.01-case-studies/case-iot-stream-processing.md](../../Flink/09-practices/09.01-case-studies/case-iot-stream-processing.md)

[^7]: Real-time ETL Deep Dive, see [Flink/09-practices/09.01-case-studies/case-realtime-analytics.md](../../Flink/09-practices/09.01-case-studies/case-realtime-analytics.md)

[^8]: CEP Complex Event Processing Pattern, see [Flink/03-api-patterns/flink-cep-deep-dive.md](../../Flink/03-api/03.02-table-sql-api/flink-sql-window-functions-deep-dive.md)

---

*Document Version: v1.0 | Update Date: 2026-04-02 | Status: Completed*
