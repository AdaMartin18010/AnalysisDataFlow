# Streaming SLO/SLI Definition and Reliability Engineering

> **Stage**: Knowledge | **Prerequisites**: [05-ecosystem/streaming-quality-assurance.md](../07-best-practices/07.01-flink-production-checklist.md) | **Formalization Level**: L3

---

## Table of Contents

- [Streaming SLO/SLI Definition and Reliability Engineering](#streaming-slosli-definition-and-reliability-engineering)
  - [Table of Contents](#table-of-contents)
  - [1. Definitions](#1-definitions)
    - [Def-K-06-19: Service Level Indicator (SLI)](#def-k-06-19-service-level-indicator-sli)
    - [Def-K-06-20: Service Level Objective (SLO)](#def-k-06-20-service-level-objective-slo)
    - [Def-K-06-21: Error Budget](#def-k-06-21-error-budget)
    - [Def-K-06-22: Availability Calculation](#def-k-06-22-availability-calculation)
  - [2. Properties](#2-properties)
    - [Prop-K-06-01: SLI Selection Criteria](#prop-k-06-01-sli-selection-criteria)
    - [Prop-K-06-02: SLO Hierarchical Structure](#prop-k-06-02-slo-hierarchical-structure)
    - [Lemma-K-06-01: Error Budget Exhaustion Theorem](#lemma-k-06-01-error-budget-exhaustion-theorem)
  - [3. Relations](#3-relations)
    - [3.1 Mapping SLO to Engineering Practice](#31-mapping-slo-to-engineering-practice)
    - [3.2 Relationship with the Dataflow Model](#32-relationship-with-the-dataflow-model)
    - [3.3 Mapping to Flink Mechanisms](#33-mapping-to-flink-mechanisms)
  - [4. Argumentation](#4-argumentation)
    - [4.1 Why Do Streaming Systems Need Special SLOs?](#41-why-do-streaming-systems-need-special-slos)
    - [4.2 Common Pitfalls in SLO Setting](#42-common-pitfalls-in-slo-setting)
  - [5. Engineering Argument](#5-engineering-argument)
    - [5.1 Streaming-Specific SLO System](#51-streaming-specific-slo-system)
    - [5.2 SLO Setting Process](#52-slo-setting-process)
    - [5.3 Error Budget Policy](#53-error-budget-policy)
  - [6. Examples](#6-examples)
    - [6.1 E-Commerce Platform Real-Time Recommendation System SLO](#61-e-commerce-platform-real-time-recommendation-system-slo)
    - [6.2 Financial Risk Control System SLO](#62-financial-risk-control-system-slo)
  - [7. Visualizations](#7-visualizations)
    - [7.1 SLO/SLI System Hierarchy Diagram](#71-slosli-system-hierarchy-diagram)
    - [7.2 SLO Setting Flowchart](#72-slo-setting-flowchart)
    - [7.3 Error Budget Consumption Tracking Chart](#73-error-budget-consumption-tracking-chart)
  - [8. References](#8-references)

## 1. Definitions

### Def-K-06-19: Service Level Indicator (SLI)

**Formal Definition**: Let the service system be $S$ and the observation time window be $T$. Then SLI is the mapping:

$$\text{SLI}_S: T \times \Omega \to \mathbb{R}^+$$

Where $\Omega$ is the observation sample space, and the output is a quantitative measure of service quality.

**SLI in Streaming Context**:

- **Availability SLI**: $A = \frac{\text{Service Uptime}}{\text{Total Observation Time}}$
- **Latency SLI**: $L_p = p\text{-th percentile processing latency}$
- **Throughput SLI**: $T = \frac{\text{Actual Records/Second}}{\text{Target Throughput}}$
- **Freshness SLI**: $F = t_{\text{now}} - t_{\text{last\_event}}$

**Intuitive Explanation**: SLI is the "thermometer" of service quality — it answers the question "how is the service performing?" A good SLI should be measurable, actionable, representative, and understandable.

---

### Def-K-06-20: Service Level Objective (SLO)

**Formal Definition**: SLO is a tuple $(\text{SLI}, \theta)$, where:

$$\text{SLO} = \{ (s, c) \mid s \in \text{SLI}, c \in C, P(s \text{ satisfies } c) \geq 1 - \epsilon \}$$

- $C$ is the set of target conditions (e.g., $\geq 99.9\%$, $< 1s$)
- $\epsilon$ is the allowed violation probability threshold
- $1 - \epsilon$ is called the **confidence level**

**SLO Compliance Determination**:
Within observation period $T$, if the proportion of samples satisfying the condition is $r$, then:

$$\text{Compliance}(\text{SLO}) = \mathbb{1}_{[r \geq \theta]} \in \{0, 1\}$$

**Intuitive Explanation**: SLO is the "passing grade" of service quality — it binds SLI to business expectations and defines "what counts as good."

---

### Def-K-06-21: Error Budget

**Formal Definition**: Given SLO target $\theta$ and time window $T$, error budget $E$ is defined as:

$$E = (1 - \theta) \times |T|$$

Where $|T|$ is the total number of requests/events in the window.

**Budget Consumption Rate**:
Let $e(t)$ be the budget consumed up to current time $t$. Then:

$$\text{Consumption Rate} = \frac{e(t)}{E \times \frac{t}{|T|}}$$

| Consumption Range | Status | Recommended Action |
|-------------------|--------|-------------------|
| $< 50\%$ | Healthy | Normal iteration |
| $50\% - 80\%$ | Caution | Assess risk |
| $80\% - 100\%$ | Danger | Freeze new feature releases |
| $> 100\%$ | Breach | Launch reliability campaign |

**Intuitive Explanation**: Error budget is the "monetized" expression of SLO — it converts abstract percentages into actionable time/count units, balancing reliability and innovation velocity.

---

### Def-K-06-22: Availability Calculation

**Formal Definition**: Availability $A$ is the proportion of time the system is in a serviceable state:

$$A = \frac{MTBF}{MTBF + MTTR}$$

Where:

- $MTBF$ (Mean Time Between Failures): average time between failures
- $MTTR$ (Mean Time To Recovery): average recovery time

**Nines Correspondence**:

| Availability Target | Annual Allowed Downtime | Monthly Allowed Downtime | Applicable Scenario |
|---------------------|------------------------|--------------------------|---------------------|
| 99% (2 nines) | 3.65 days | 7.3 hours | Internal tools |
| 99.9% (3 nines) | 8.76 hours | 43.8 minutes | Standard business |
| 99.99% (4 nines) | 52.6 minutes | 4.4 minutes | Critical business |
| 99.999% (5 nines) | 5.26 minutes | 26.3 seconds | Financial core |

**Streaming Availability Extension**:
For long-running (Always-On) streaming jobs, availability calculation must consider:

$$A_{\text{streaming}} = \frac{\sum_{i} (t_{i}^{\text{end}} - t_{i}^{\text{start}})}{T_{\text{total}}}$$

Where $\{(t_{i}^{\text{start}}, t_{i}^{\text{end}})\}$ is the set of all normal operation intervals.

---

## 2. Properties

### Prop-K-06-01: SLI Selection Criteria

**Proposition**: Effective streaming SLIs should satisfy the following properties:

1. **End-to-End Observability**: SLI should cover the complete path actually perceived by users.
   $$\text{SLI}_{\text{e2e}} = f(\text{SLI}_{\text{ingest}}, \text{SLI}_{\text{process}}, \text{SLI}_{\text{sink}})$$

2. **Causal Explainability**: If SLO is violated, it should be possible to locate the specific component.
   $$\text{Violation}(\text{SLO}) \implies \exists c \in \text{Components}: \text{RootCause}(c)$$

3. **Statistical Stability**: SLI should converge within a reasonable time window.
   $$\text{Var}(\text{SLI}_T) < \delta, \quad \forall T \geq T_{\min}$$

---

### Prop-K-06-02: SLO Hierarchical Structure

**Proposition**: Streaming system SLOs have a natural hierarchy:

$$
\text{SLO}_{\text{org}} \supseteq \text{SLO}_{\text{service}} \supseteq \text{SLO}_{\text{pipeline}} \supseteq \text{SLO}_{\text{operator}}
$$

And satisfy the error allocation constraint:

$$1 - \theta_{\text{org}} \geq \sum_{i} (1 - \theta_{i})$$

**Engineering Significance**: Organization-level SLO must be looser than lower-level SLOs, reserving error margin for each layer.

---

### Lemma-K-06-01: Error Budget Exhaustion Theorem

**Lemma**: If the error budget is exhausted within time window $\tau < T$, then:

$$P(\text{SLO}_{\text{next}} \text{ satisfied}) \leq \frac{T - \tau}{T} \times \theta$$

**Proof Sketch**:
Remaining available error share is 0; any subsequent failure will cause SLO breach. The only remaining strategy is to ensure 100% success going forward, which has extremely low probability in complex streaming systems.

---

## 3. Relations

### 3.1 Mapping SLO to Engineering Practice

```
┌─────────────────────────────────────────────────────────────┐
│                   Reliability Engineering System              │
├─────────────────────────────────────────────────────────────┤
│  SLO (Target)  ←──────→  SLI (Indicator)  ←──────→  SLI Collection System │
│     ↑                                            ↓          │
│  Error Budget  ←──────→  Release Policy  ←──────→  Monitoring/Alert System │
│     ↑                                            ↓          │
│  Reliability Campaign  ←────→  Incident Review  ←──────→  Observability Platform │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Relationship with the Dataflow Model

| Dataflow Concept | SLO/SLI Correspondence |
|-----------------|------------------------|
| Watermark delay | Freshness SLI |
| Processing-time delay | Latency SLI |
| Exactly-Once guarantee | Correctness SLO |
| Window trigger timeliness | Availability/Latency SLO |

### 3.3 Mapping to Flink Mechanisms

| Flink Mechanism | Related SLO | Monitoring Entry Point |
|----------------|-------------|----------------------|
| Checkpoint | Recovery time SLO | checkpointDuration, failedCheckpoints |
| Watermark | Freshness SLO | currentOutputWatermark |
| Backpressure | Latency/Throughput SLO | backPressuredTimeMsPerSecond |
| Savepoint | Release window SLO | Coordinate checkpoint triggering |

---

## 4. Argumentation

### 4.1 Why Do Streaming Systems Need Special SLOs?

**Traditional Batch Processing vs. Streaming**:

| Dimension | Batch Processing | Streaming |
|-----------|-----------------|-----------|
| Time Model | Discrete batches | Continuous time |
| Failure Impact | Single job | Continuous accumulation |
| Recovery Requirement | Hour-level acceptable | Second/minute-level expected |
| Measurement Frequency | Per-batch completion | Continuous sampling |

**Core Difference**: Streaming job failures have a **continuous accumulation effect** — every minute of downtime may mean millions of events lost or delayed, rather than just affecting a single batch as in batch processing.

### 4.2 Common Pitfalls in SLO Setting

1. **Over-optimizing availability while neglecting latency**
   - Anti-pattern: System shows 99.99% availability, but P99 latency reaches 30 seconds.
   - Consequence: Poor actual user experience, business logic timeouts.

2. **SLI metrics disconnected from user experience**
   - Anti-pattern: Monitoring Kafka Consumer Lag instead of end-to-end latency.
   - Consequence: Lag appears normal but Sink is blocked, so users still perceive delays.

3. **Overly aggressive SLO leading to runaway costs**
   - Anti-pattern: Pursuing 5 nines availability when failure rate is only 0.001%.
   - Consequence: Redundancy costs may exceed business benefits.

---

## 5. Engineering Argument

### 5.1 Streaming-Specific SLO System

Based on industry practice, streaming systems should define the following SLO categories:

| Category | SLI Definition | Typical SLO | Measurement Method |
|----------|---------------|-------------|-------------------|
| **Availability** | Job runtime proportion | 99.9% | (Runtime/Total Time) × 100% |
| **Latency** | P99 processing delay | < 1s | P99 of `now() - event_timestamp` |
| **Correctness** | Exactly-Once success rate | 99.99% | Successful EOS transactions / Total transactions |
| **Freshness** | Data arrival delay | < 5s | `now() - max(event_time in window)` |
| **Throughput** | Actual/Target throughput ratio | > 80% | Actual RPS / Target RPS |
| **Recoverability** | Failure recovery time | < 3min | Failure detected → Fully recovered |

**SLO Priority Recommendations**:

```
P0 (Critical): Availability > Correctness > Recoverability
P1 (Important): Latency > Freshness
P2 (Optimization): Throughput
```

### 5.2 SLO Setting Process

**Step 1: Identify Critical User Journeys (CUJ)**

```
Example CUJ: Real-Time Risk Control Decision
├── Data Ingestion (Kafka → Flink)
├── Rule Computation (CEP Window Processing)
├── Decision Output (Flink → Redis)
└── Result Query (API Service)
```

**Step 2: Define SLIs**

For each CUJ step, define quantifiable SLIs:

- Data ingestion latency: `kafka_consumer_lag × avg_event_size / throughput`
- Processing latency: `output_watermark - input_watermark`
- End-to-end latency: `api_response_time - event_timestamp`

**Step 3: Set SLO Targets**

Adopt a **progressive tightening** strategy:

1. Initial target = Current baseline × 0.9
2. Evaluate actual achievement after 4 weeks
3. If consistently achieved, tighten the target; if frequently breached, relax the target

**Step 4: Implement Monitoring**

```java
// [Pseudocode snippet - not directly runnable] Core logic only
// Prometheus metrics example
Counter slo_violations_total = Counter.build()
    .name("streaming_slo_violations_total")
    .labelNames("slo_type", "pipeline_name")
    .help("Total SLO violations")
    .register();

Histogram event_latency = Histogram.build()
    .name("event_processing_latency_seconds")
    .buckets(0.01, 0.1, 0.5, 1, 5, 10)
    .help("End-to-end event processing latency")
    .register();
```

**Step 5: Continuous Improvement**

- Weekly SLO review meetings
- Monthly error budget consumption analysis
- Quarterly SLO target adjustments

### 5.3 Error Budget Policy

**Budget Allocation Model**:

```
Total Error Budget (100%)
├── Planned Maintenance: 20%
├── Known Risks: 30%
├── New Feature Releases: 30%
└── Unknown Failure Buffer: 20%
```

**Budget Consumption Alerts**:

| Alert Level | Trigger Condition | Response Action |
|-------------|-------------------|-----------------|
| INFO | Consumption > 50% | Notify team to monitor |
| WARNING | Consumption > 80% | Freeze non-urgent releases |
| CRITICAL | Consumption > 95% | Launch reliability campaign, block releases |
| PAGE | Consumption > 100% | All hands on deck, immediate damage control |

**Release Policy Association**:

```
Error Budget Status → Release Policy
─────────────────────────────────
Green (< 50%)  → Standard release process
Yellow (50-80%) → Add manual approval
Red (> 80%)  → Emergency fixes only
Exhausted (> 100%) → Freeze all changes
```

---

## 6. Examples

### 6.1 E-Commerce Platform Real-Time Recommendation System SLO

**Business Scenario**: Product recommendation stream processing based on real-time user behavior

| CUJ | SLI | SLO | Monitoring Implementation |
|-----|-----|-----|--------------------------|
| Click event processing | P99 latency | < 500ms | Flink metrics reporter |
| Recommendation result generation | Throughput | > 10K TPS | Kafka consumer metrics |
| Feature update | Freshness | < 10s | Watermark lag monitor |
| System availability | Job runtime | 99.95% | JobManager REST API |

**Error Budget Calculation**:

- Annual allowed downtime = (1 - 0.9995) × 365 × 24 = 4.38 hours
- Monthly budget = 4.38 / 12 = 21.9 minutes

### 6.2 Financial Risk Control System SLO

**Business Scenario**: Real-time transaction anti-fraud detection

| Level | SLO | Notes |
|-------|-----|-------|
| Organization-level | 99.99% | Regulatory requirement |
| Service-level | 99.995% | Multi-AZ deployment |
| Job-level | 99.999% | Critical path jobs |

**SLI Calculation Example**:

```python
# Latency SLI calculation
def calculate_latency_sli(events: List[Event], slo_threshold_ms: int) -> float:
    """Calculate the proportion of events satisfying latency SLO"""
    compliant = sum(1 for e in events
                   if e.processed_at - e.event_time <= slo_threshold_ms)
    return compliant / len(events)

# Availability SLI calculation
def calculate_availability_sli(
    job_uptime_ms: int,
    total_time_ms: int
) -> float:
    """Calculate job availability"""
    return job_uptime_ms / total_time_ms
```

---

## 7. Visualizations

### 7.1 SLO/SLI System Hierarchy Diagram

```mermaid
graph TB
    subgraph "Business Layer"
        B1[Business Goals<br/>User Satisfaction]
    end

    subgraph "SLO Layer"
        S1[Organization-Level SLO<br/>99.9%]
        S2[Service-Level SLO<br/>99.95%]
        S3[Job-Level SLO<br/>99.99%]
    end

    subgraph "SLI Layer"
        I1[Availability SLI<br/>Runtime Proportion]
        I2[Latency SLI<br/>P99 Processing Time]
        I3[Throughput SLI<br/>Records/Second]
        I4[Correctness SLI<br/>EOS Success Rate]
    end

    subgraph "Monitoring Layer"
        M1[Prometheus Metrics]
        M2[Grafana Dashboard]
        M3[Alert Rules]
    end

    B1 --> S1
    S1 --> S2
    S2 --> S3
    S3 --> I1
    S3 --> I2
    S3 --> I3
    S3 --> I4
    I1 --> M1
    I2 --> M1
    I3 --> M1
    I4 --> M1
    M1 --> M2
    M2 --> M3
```

### 7.2 SLO Setting Flowchart

```mermaid
flowchart TD
    Start([Start]) --> Identify[Identify Critical User Journeys]
    Identify --> DefineSLI[Define SLI Metrics]
    DefineSLI --> Baseline[Collect Baseline Data]
    Baseline --> SetSLO[Set SLO Targets]
    SetSLO --> Implement[Implement Monitoring]
    Implement --> Monitor[Continuous Monitoring]
    Monitor --> Review{Quarterly Review}
    Review -->|Achieved| Tighten[Tighten Targets]
    Review -->|Not Achieved| Loosen[Relax Targets]
    Review -->|Achieved| Maintain[Maintain Current]
    Tighten --> Monitor
    Loosen --> Monitor
    Maintain --> Monitor
```

### 7.3 Error Budget Consumption Tracking Chart

```mermaid
xychart-beta
    title "Error Budget Consumption Trend (Monthly)"
    x-axis [Week1, Week2, Week3, Week4]
    y-axis "Consumption Percentage %" 0 --> 100
    line "Actual Consumption" [12, 35, 58, 85]
    line "Linear Expectation" [25, 50, 75, 100]
    line "80% Warning Line" [80, 80, 80, 80]
```

---

## 8. References

---

*Document Version: v1.0 | Created: 2026-04-20*
