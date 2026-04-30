# Core Stream Computing Terminology Disambiguation Matrix

> Stage: Struct/01-foundation | Prerequisites: [unified-streaming-theory](unified-streaming-theory.md), [dataflow-model-formalization](dataflow-model-formalization.md) | Formalization Level: L4 | Updated: 2026-04-30

---

## Table of Contents

- [Core Stream Computing Terminology Disambiguation Matrix](#core-stream-computing-terminology-disambiguation-matrix)
  - [Table of Contents](#table-of-contents)
  - [1. Definitions](#1-definitions)
    - [Def-T-01-01: Terminology Disambiguation Framework](#def-t-01-01-terminology-disambiguation-framework)
    - [Def-T-01-02: Stream Computing (流计算)](#def-t-01-02-stream-computing-流计算)
    - [Def-T-01-03: Stream Processing (流处理)](#def-t-01-03-stream-processing-流处理)
    - [Def-T-01-04: Real-time Computing (实时计算)](#def-t-01-04-real-time-computing-实时计算)
    - [Def-T-01-05: Event-driven (事件驱动)](#def-t-01-05-event-driven-事件驱动)
    - [Def-T-01-06: Dataflow Model (Abstract Model)](#def-t-01-06-dataflow-model-abstract-model)
    - [Def-T-01-07: Dataflow System (Google Product)](#def-t-01-07-dataflow-system-google-product)
    - [Def-T-01-08: Dataflow Engine (Execution Engine)](#def-t-01-08-dataflow-engine-execution-engine)
    - [Def-T-01-09: Operator](#def-t-01-09-operator)
    - [Def-T-01-10: Transformation](#def-t-01-10-transformation)
    - [Def-T-01-11: Function](#def-t-01-11-function)
    - [Def-T-01-12: UDF (User-Defined Function)](#def-t-01-12-udf-user-defined-function)
    - [Def-T-01-13: Stream vs Flow vs Event Sequence vs Log](#def-t-01-13-stream-vs-flow-vs-event-sequence-vs-log)
    - [Def-T-01-14: Latency vs Throughput vs Freshness](#def-t-01-14-latency-vs-throughput-vs-freshness)
    - [Def-T-01-15: Deterministic vs Exactly-once vs Idempotent](#def-t-01-15-deterministic-vs-exactly-once-vs-idempotent)
  - [2. Properties](#2-properties)
    - [Lemma-T-01-01: Inclusion Relation between Stream Computing and Stream Processing](#lemma-t-01-01-inclusion-relation-between-stream-computing-and-stream-processing)
    - [Lemma-T-01-02: Orthogonality of Real-time Computing and Stream Processing](#lemma-t-01-02-orthogonality-of-real-time-computing-and-stream-processing)
    - [Lemma-T-01-03: Intersection Characteristics of Event-driven and Stream Processing](#lemma-t-01-03-intersection-characteristics-of-event-driven-and-stream-processing)
    - [Lemma-T-01-04: Strict Separation between Dataflow Model and Dataflow System](#lemma-t-01-04-strict-separation-between-dataflow-model-and-dataflow-system)
    - [Lemma-T-01-05: Hierarchical Relation Operator ⊂ Transformation](#lemma-t-01-05-hierarchical-relation-operator--transformation)
    - [Lemma-T-01-06: Formal Expression of Latency-Throughput Trade-off](#lemma-t-01-06-formal-expression-of-latency-throughput-trade-off)
    - [Lemma-T-01-07: Non-equivalence of Exactly-once Implementation Paths](#lemma-t-01-07-non-equivalence-of-exactly-once-implementation-paths)
  - [3. Relations](#3-relations)
    - [3.1 Four-Dimensional Terminology Space Mapping](#31-four-dimensional-terminology-space-mapping)
    - [3.2 Terminology Dependency Graph](#32-terminology-dependency-graph)
  - [4. Argumentation](#4-argumentation)
    - [4.1 Historical Causes of Terminology Confusion](#41-historical-causes-of-terminology-confusion)
    - [4.2 Typical Misuse Case Analysis](#42-typical-misuse-case-analysis)
  - [5. Proof / Engineering Argument](#5-proof--engineering-argument)
    - [Thm-T-01-01: Formal Completeness of Terminology Selection Decision Tree](#thm-t-01-01-formal-completeness-of-terminology-selection-decision-tree)
    - [Thm-T-01-02: Non-interchangeability of Stream vs Flow vs Event Sequence vs Log](#thm-t-01-02-non-interchangeability-of-stream-vs-flow-vs-event-sequence-vs-log)
    - [Thm-T-01-03: End-to-End Impossibility of Exactly-once (without Cooperation)](#thm-t-01-03-end-to-end-impossibility-of-exactly-once-without-cooperation)
  - [6. Examples](#6-examples)
    - [6.1 Example: Precise Terminology Usage in Flink Jobs](#61-example-precise-terminology-usage-in-flink-jobs)
    - [6.2 Example: Technical Document Terminology Correction](#62-example-technical-document-terminology-correction)
  - [7. Visualizations](#7-visualizations)
    - [7.1 Terminology × Dimension Concept Matrix](#71-terminology--dimension-concept-matrix)
    - [7.2 Boundary Decision Tree: "Which Term Should I Use for My Scenario?"](#72-boundary-decision-tree-which-term-should-i-use-for-my-scenario)
    - [7.3 Radar Chart for Six Groups of Confusable Concepts](#73-radar-chart-for-six-groups-of-confusable-concepts)
  - [8. References](#8-references)
  - [Appendix A: Project Internal Unified Usage Recommendations](#appendix-a-project-internal-unified-usage-recommendations)
  - [Appendix B: Quick Reference Tables for Six Term Groups](#appendix-b-quick-reference-tables-for-six-term-groups)
    - [Group 1: Stream Computing vs Stream Processing vs Real-time Computing vs Event-driven](#group-1-stream-computing-vs-stream-processing-vs-real-time-computing-vs-event-driven)
    - [Group 2: Dataflow Model vs Dataflow System vs Dataflow Engine](#group-2-dataflow-model-vs-dataflow-system-vs-dataflow-engine)
    - [Group 3: Operator vs Transformation vs Function vs UDF](#group-3-operator-vs-transformation-vs-function-vs-udf)
    - [Group 4: Stream vs Flow vs Event Sequence vs Log](#group-4-stream-vs-flow-vs-event-sequence-vs-log)
    - [Group 5: Latency vs Throughput vs Freshness](#group-5-latency-vs-throughput-vs-freshness)
    - [Group 6: Deterministic vs Exactly-once vs Idempotent](#group-6-deterministic-vs-exactly-once-vs-idempotent)

## 1. Definitions

This document provides rigorous disambiguation of six groups of the most easily confused core terminologies in the stream computing field, establishing formal differentiation criteria and unified internal project usage.

### Def-T-01-01: Terminology Disambiguation Framework

Let the terminology space be $\mathcal{T}$, where each term $t \in \mathcal{T}$ is characterized by a quadruple:

$$t \triangleq \langle \text{AbstractionLevel}, \text{TimeConstraint}, \text{StateRequirement}, \text{SemanticGuarantee} \rangle$$

Where:

- $\text{AbstractionLevel} \in \{L_1(\text{Physical}), L_2(\text{Logical}), L_3(\text{Mathematical}), L_4(\text{Business})\}$
- $\text{TimeConstraint} \in \{\text{Hard}, \text{Firm}, \text{Soft}, \text{None}\}$
- $\text{StateRequirement} \in \{\text{Stateless}, \text{Stateful}(\text{Bounded}), \text{Stateful}(\text{Unbounded})\}$
- $\text{SemanticGuarantee} \in \{\text{At-most-once}, \text{At-least-once}, \text{Exactly-once}, \text{Deterministic}\}$

### Def-T-01-02: Stream Computing (流计算)

**Wikipedia Definition Reference**[^1]: "Stream processing is a computer programming paradigm, equivalent to dataflow programming, event stream processing, and reactive programming, that allows some applications to more easily exploit a limited form of parallel processing."

**Critical Analysis**: Wikipedia conflates stream processing with stream computing, but industry practice maintains a subtle distinction. Stream Computing (流计算) emphasizes the **computational paradigm** itself—the continuous computation model where data triggers computation upon arrival; while Stream Processing (流处理) leans more toward **engineering implementation**—the concrete process of performing filtering, transformation, aggregation, and other operations on data streams.

Formal Definition:

$$\text{StreamComputing} \triangleq \langle S, \to, \mathcal{C} \rangle$$

Where $S$ is the set of infinite streams, $\to$ is the data-driven trigger relation, and $\mathcal{C}$ is the family of continuous computation functions.

### Def-T-01-03: Stream Processing (流处理)

**Wikipedia Definition Reference**[^1]: "Stream processing is a data processing technique to analyze and process continuous streams of data in real-time or near-real-time."

Formal Definition:

$$\text{StreamProcessing} \triangleq \lambda s \in S.\ \text{process}(s) : S \to O \times S'$$

Where $O$ is the output set and $S'$ is the updated state. Stream Processing emphasizes the **operation execution** level, containing explicit input-output mapping and state transitions.

### Def-T-01-04: Real-time Computing (实时计算)

**Wikipedia Definition Reference**[^2]: "Real-time computing (RTC) describes hardware and software systems subject to a 'real-time constraint' — for example from event to system response. Real-time programs must guarantee response within specified time constraints, often referred to as 'deadlines'."

**Critical Analysis**: Wikipedia clearly distinguishes hard/soft/firm real-time, but Chinese technical communities often generalize "real-time" (实时) to mean "fast", leading to severe conceptual degradation.

Formal Definition:

$$\text{RealTimeComputing} \triangleq \langle \mathcal{T}, \delta, \prec \rangle$$

Where $\mathcal{T}$ is the task set, $\delta: \mathcal{T} \to \mathbb{R}^+$ is the deadline assignment function, and $\prec$ is the priority partial order. Correctness depends not only on logical results but also on the timing of result production.

### Def-T-01-05: Event-driven (事件驱动)

**Wikipedia Definition Reference**[^3]: "Event-driven architecture (EDA) is a software architecture paradigm revolving around the production, detection, consumption of, and reaction to events."

Formal Definition:

$$\text{EventDriven} \triangleq \langle E, H, \text{dispatch} \rangle$$

Where $E$ is the event space, $H: E \to \text{Action}$ is the set of event handlers, and $\text{dispatch}: E \times H \to \text{Response}$ is the dispatch function.

### Def-T-01-06: Dataflow Model (Abstract Model)

**Google Dataflow Paper Definition**[^4]: "The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing."

Formal Definition (Akidau et al., VLDB 2015):

$$\text{DataflowModel} \triangleq \langle \text{What}, \text{Where}, \text{When}, \text{How} \rangle$$

- **What**: What results are computed (transformation logic)
- **Where**: In which window of event time to compute
- **When**: At what point in processing time to trigger output
- **How**: How results are refined over time (accumulation mode)

### Def-T-01-07: Dataflow System (Google Product)

**Google Cloud Official Definition**[^5]: "Google Cloud Dataflow is a fully managed service for executing Apache Beam pipelines within the Google Cloud Platform ecosystem."

Formal Distinction:

$$\text{DataflowSystem} \triangleq \text{ManagedService}(\text{DataflowModel}, \text{ApacheBeam}, \text{GCP})$$

It is the **commercial implementation** of the Dataflow Model, not the model itself.

### Def-T-01-08: Dataflow Engine (Execution Engine)

Formal Definition:

$$\text{DataflowEngine} \triangleq \langle G, \mathcal{E}, \text{sched} \rangle$$

Where $G = (V, E)$ is the operator graph (DAG), $\mathcal{E}$ is the execution environment, and $\text{sched}: V \to \text{Resource}$ is the scheduling function. Flink's JobManager/TaskManager and Spark's DAGScheduler all fall into this category.

### Def-T-01-09: Operator

**Flink Official Documentation Definition**[^6]: "An Operator is a node in the logical or physical execution graph that performs a specific computation on one or more input streams and produces one or more output streams."

Formal Definition:

$$\text{Operator} \triangleq \langle I, O, f, \Sigma \rangle$$

Where $I$ is the input port set, $O$ is the output port set, $f: I \times \Sigma \to O \times \Sigma$ is the stateful computation function, and $\Sigma$ is the operator state space.

### Def-T-01-10: Transformation

Formal Definition:

$$\text{Transformation} \triangleq \text{Operator} \cup \text{GraphRewrite}$$

Transformation is a broader concept, encompassing both atomic operators (e.g., `map`, `filter`) and graph-level rewrites (e.g., data redistribution triggered by `keyBy`).

### Def-T-01-11: Function

Formal Definition:

$$\text{Function} \triangleq f: D \to R$$

Function is a pure mathematical concept, stateless and side-effect-free, decoupled from execution context.

### Def-T-01-12: UDF (User-Defined Function)

**Flink Official Documentation Definition**[^6]: "User-defined functions (UDFs) are extension points to call frequently used logic or custom logic that cannot be expressed otherwise in queries."

Formal Definition:

$$\text{UDF} \triangleq \text{Function} \times \text{RuntimeContext}$$

UDF is a user-provided function instance managed by the system at runtime, with access to state, metrics, distributed cache, and other runtime capabilities.

### Def-T-01-13: Stream vs Flow vs Event Sequence vs Log

**Wikipedia Definition Reference**[^1][^7]:

- Stream: "A sequence of data elements made available over time."
- Flow: "In computing, dataflow is a broad concept that can refer to data in motion or the flow of data through a system."

Formal Distinction:

| Term | Formal Signature | Core Characteristic |
|------|-----------------|---------------------|
| **Stream** | $S: \mathbb{T} \to \mathcal{P}(D)$ | Time-indexed sequence of data elements, emphasizing **continuity** |
| **Flow** | $F: \langle D, \text{rate}, \text{path} \rangle$ | Data **flowing** through network/system, emphasizing topological path |
| **Event Sequence** | $ES: \mathbb{N} \to E$ | Discrete events in **causal order**, emphasizing event semantics |
| **Log** | $L: \mathbb{N} \to \text{Record}$ | Immutable **persistent record sequence**, emphasizing fault tolerance and replayability |

### Def-T-01-14: Latency vs Throughput vs Freshness

Formal Definitions:

$$\text{Latency}(e) \triangleq t_{\text{output}}(e) - t_{\text{event}}(e)$$

$$\text{Throughput} \triangleq \lim_{T \to \infty} \frac{|\{e : t_{\text{output}}(e) \leq T\}|}{T}$$

$$\text{Freshness}(q) \triangleq t_{\text{now}} - t_{\text{latest_event_in_result}}(q)$$

**Critical Analysis**: Latency measures the interval for a **single record** from production to processing; Throughput measures **system capacity**; Freshness measures **result timeliness** (the time span of the latest data reflected in the result). The three are often confused but can actually be optimized independently.

### Def-T-01-15: Deterministic vs Exactly-once vs Idempotent

Formal Definitions:

$$\text{Deterministic}(f) \triangleq \forall x.\ f(x) \text{ is uniquely determined} \Leftrightarrow f \text{ is a pure function}$$

$$\text{ExactlyOnce}(S) \triangleq \forall e \in S.\ \text{effect}(e) \text{ is applied exactly once}$$

$$\text{Idempotent}(g) \triangleq \forall x.\ g(g(x)) = g(x)$$

**Key Distinction**: Deterministic describes **function property**; Exactly-once describes **system semantics**; Idempotent describes **operation idempotency**. Exactly-once can be achieved through the combination of Deterministic + Idempotent, but the three are not equivalent.

---

## 2. Properties

### Lemma-T-01-01: Inclusion Relation between Stream Computing and Stream Processing

$$\text{StreamProcessing} \subseteq \text{StreamComputing}$$

**Proof**: Stream Processing is a concrete implementation instance of the Stream Computing paradigm. All Stream Processing systems follow the pattern of computing upon data arrival, hence belong to Stream Computing; conversely, theoretical Stream Computing models (such as certain pure dataflow languages) may not correspond to any actual Stream Processing system.

### Lemma-T-01-02: Orthogonality of Real-time Computing and Stream Processing

$$\text{StreamProcessing} \not\subseteq \text{RealTimeComputing} \land \text{RealTimeComputing} \not\subseteq \text{StreamProcessing}$$

**Proof**:

- Stream Processing is not necessarily Real-time: Batch micro-batch processing, though processing stream data, can have latency of seconds or even minutes, failing to satisfy real-time constraints.
- Real-time Computing is not necessarily Stream Processing: Hard real-time control systems (such as automotive ABS) process periodic control signals rather than data streams, belonging to real-time computing but not stream processing.

### Lemma-T-01-03: Intersection Characteristics of Event-driven and Stream Processing

$$\text{StreamProcessing} \cap \text{EventDriven} \neq \emptyset$$

$$|\text{StreamProcessing} \cup \text{EventDriven}| > \max(|\text{StreamProcessing}|, |\text{EventDriven}|)$$

**Proof**: Modern stream processing systems (Flink, Kafka Streams) are all implemented using event-driven architecture; but EDA is also widely used in non-streaming scenarios (such as GUI programming, microservice event buses).

### Lemma-T-01-04: Strict Separation between Dataflow Model and Dataflow System

$$\text{DataflowModel} \cap \text{DataflowSystem} = \emptyset \quad (\text{conceptual level})$$

**Proof**: Dataflow Model is a mathematical abstraction (What/Where/When/How); Dataflow System (Google Cloud Dataflow) is a specific engineering implementation of that model. Confusing the two is equivalent to conflating "relational algebra" with "Oracle Database".

### Lemma-T-01-05: Hierarchical Relation Operator ⊂ Transformation

$$\forall o \in \text{Operator}.\ o \in \text{Transformation}$$

$$\exists t \in \text{Transformation}.\ t \notin \text{Operator}$$

**Proof**: `keyBy` in Flink is a Transformation, but it does not perform data computation—it only defines data partitioning strategy, and does not constitute an independent Operator.

### Lemma-T-01-06: Formal Expression of Latency-Throughput Trade-off

$$\forall S.\ \text{Latency}(S) \cdot \text{Throughput}(S) \leq C(S) \quad (\text{system-dependent constant})$$

**Proof**: For fixed resources, reducing per-record processing time (low latency) usually requires reducing batching/buffering, leading to decreased processing volume per unit time (low throughput). Conversely, increasing buffering improves throughput but increases latency. This inequality is a corollary of Little's Law in stream systems.

### Lemma-T-01-07: Non-equivalence of Exactly-once Implementation Paths

$$\text{ExactlyOnce} \Rightarrow (\text{Deterministic} \lor \text{Idempotent})$$

$$\text{Deterministic} \land \text{Idempotent} \Rightarrow \text{ExactlyOnce} \text{ (in fault-tolerant restart scenarios)}$$

**Proof**: Flink's Exactly-once is achieved through Deterministic (replayable state snapshots) + transactional Sink; Kafka's Exactly-once is achieved through idempotent producer + transaction API. Different paths, equivalent effect.

---

## 3. Relations

### 3.1 Four-Dimensional Terminology Space Mapping

The following concept matrix shows the distribution of six groups of core terminologies across four dimensions:

```mermaid
quadrantChart
    title 流计算核心术语四维度定位矩阵
    x-axis 低抽象层 --> 高抽象层
    y-axis 弱时间约束 --> 强时间约束
    quadrant-1 商业概念层
    quadrant-2 实时系统层
    quadrant-3 基础组件层
    quadrant-4 抽象模型层
    "Stream Computing": [0.7, 0.5]
    "Stream Processing": [0.5, 0.6]
    "Real-time Computing": [0.4, 0.9]
    "Event-driven": [0.6, 0.7]
    "Dataflow Model": [0.9, 0.4]
    "Dataflow System": [0.3, 0.5]
    "Dataflow Engine": [0.2, 0.6]
    "Operator": [0.1, 0.5]
    "Transformation": [0.3, 0.4]
    "Function": [0.5, 0.2]
    "UDF": [0.4, 0.3]
    "Stream": [0.6, 0.5]
    "Flow": [0.4, 0.4]
    "Event Sequence": [0.7, 0.6]
    "Log": [0.2, 0.3]
    "Latency": [0.3, 0.8]
    "Throughput": [0.3, 0.2]
    "Freshness": [0.7, 0.7]
    "Deterministic": [0.8, 0.3]
    "Exactly-once": [0.5, 0.7]
    "Idempotent": [0.6, 0.4]
```

### 3.2 Terminology Dependency Graph

```mermaid
graph TB
    subgraph "计算范式层"
        SC[Stream Computing]
        RT[Real-time Computing]
        ED[Event-driven]
    end

    subgraph "处理实现层"
        SP[Stream Processing]
        DM[Dataflow Model]
    end

    subgraph "系统产品层"
        DS[Dataflow System]
        DE[Dataflow Engine]
        Flink[Apache Flink]
    end

    subgraph "编程抽象层"
        OP[Operator]
        TR[Transformation]
        FN[Function]
        UDF[UDF]
    end

    subgraph "数据对象层"
        ST[Stream]
        FL[Flow]
        ES[Event Sequence]
        LG[Log]
    end

    subgraph "语义保证层"
        DET[Deterministic]
        EO[Exactly-once]
        IDP[Idempotent]
    end

    SC -->|实现为| SP
    ED -->|实现为| SP
    RT -.->|可独立存在| RT
    SP -->|基于| DM
    DM -->|产品化| DS
    DM -->|引擎化| DE
    DE -->|实例| Flink
    SP -->|由...构成| OP
    OP -->|属于| TR
    TR -->|使用| FN
    FN -->|扩展为| UDF
    SP -->|处理| ST
    ST -->|网络中表现为| FL
    ST -->|语义化为| ES
    ST -->|持久化为| LG
    SP -->|需要保证| EO
    EO -->|可通过| DET
    EO -->|可通过| IDP
```

---

## 4. Argumentation

### 4.1 Historical Causes of Terminology Confusion

The chaos in stream computing terminology stems from three historical intersections:

1. **Collision between Database and Systems Communities**: Database researchers use "stream" to refer to infinite relations over relational algebra (Arasu et al., CQL); systems researchers use "stream" to refer to byte stream transmission (TCP stream).

2. **Conflict between Industrial Marketing and Academic Precision**: Google named its product "Cloud Dataflow", causing the community to use "Dataflow" to simultaneously refer to the model, the product, and the general concept.

3. **Semantic Loss in Chinese Translation**: "Real-time" is translated as "实时" (shí shí), where in everyday Chinese "实时" is equivalent to "timely", dissolving the strict distinction between hard/soft real-time.

### 4.2 Typical Misuse Case Analysis

**Case 1: "Our system supports real-time computing" (Concept Degradation)**

- **Scenario**: An e-commerce company refers to Flink batch processing (Processing Time window, 5-minute trigger) as "real-time computing" (实时计算).
- **Problem**: A 5-minute delay falls into the Soft Real-time or even non-real-time category. The Wikipedia definition of real-time requires "guarantee response within specified time constraints"—it must provide **deadline guarantees**, not simply "relatively fast".
- **Correct Phrasing**: "Our system supports low-latency stream processing (latency target < 5 minutes) and is not a hard real-time system."

**Case 2: "Dataflow is Google's stream computing system" (Model vs Implementation Confusion)**

- **Scenario**: Technical blogs conflate "Dataflow Model" with "Google Cloud Dataflow".
- **Problem**: Dataflow Model (VLDB 2015 paper) is an abstract computation model; Google Cloud Dataflow is the managed service implementation of that model; Apache Beam is the open-source SDK for the model. The three operate at different levels.
- **Correct Phrasing**: "Google Cloud Dataflow is a commercial implementation of the Dataflow Model, defining jobs through the Apache Beam SDK."

**Case 3: "A UDF is just a Function" (Ignoring Runtime Context)**

- **Scenario**: Developers register pure functions directly as Flink UDFs, expecting to access state but receiving NullPointerException.
- **Problem**: UDF (Def-T-01-12) is the product type of Function and RuntimeContext. Pure Function is stateless; UDF, under system management, can access state, metrics, and distributed cache.
- **Correct Phrasing**: "UDF is a wrapped instance of user functions in the stream processing runtime, containing lifecycle management and runtime context injection."

**Case 4: "Exactly-once equals deterministic execution" (Confusing Semantic Guarantee with Function Property)**

- **Scenario**: Believing that as long as operators are deterministic functions, the system naturally provides exactly-once.
- **Problem**: Deterministic describes that a function produces unique output given the same input; Exactly-once describes that the system does not repeatedly apply side effects after fault recovery. Deterministic functions do produce identical output when re-executed, but if the Sink writes to external systems twice, exactly-once is still violated.
- **Correct Phrasing**: "Exactly-once requires end-to-end coordination (replayable source + deterministic computation + transactional/idempotent sink) and cannot be guaranteed by deterministic functions alone."

**Case 5: "Low Latency equals High Freshness" (Confusing Single-record Latency with Result Timeliness)**

- **Scenario**: System latency is 10ms, but Watermark lags 10 minutes, so query results are still based on data from 10 minutes ago.
- **Problem**: Latency measures the interval from record production to processing; Freshness measures the gap between the timestamp of the latest data reflected in query results and the current time. High Watermark lag leads to poor Freshness even when single-record Latency is low.
- **Correct Phrasing**: "The system has single-record processing latency of 10ms, but due to event-time watermark lag of 10 minutes, result freshness is 10 minutes."


---

## 5. Proof / Engineering Argument

### Thm-T-01-01: Formal Completeness of Terminology Selection Decision Tree

**Theorem**: For any stream computing scenario $C$, there exists a unique terminology subset $T_C \subseteq \mathcal{T}$ such that $T_C$ precisely describes the technical characteristics of $C$, and $\forall t_1, t_2 \in T_C$, $t_1$ and $t_2$ are non-redundant.

**Proof Framework**:

1. **Abstraction Level Determination**: If $C$ discusses architecture design, use $L_3$ and above terminologies (Model, Paradigm); if $C$ discusses code implementation, use $L_2$ terminologies (Operator, UDF).

2. **Time Constraint Determination**: If $C$ requires deadline guarantees, use Real-time Computing and its subclasses (Hard/Firm/Soft); if only low latency is required, use Stream Processing.

3. **State Requirement Determination**: If $C$ involves infinite-state aggregation, use Stateful Stream Processing; if only per-record filtering is needed, use Stateless.

4. **Semantic Guarantee Determination**: If $C$ requires end-to-end non-duplication, use Exactly-once; if only internal determinism is required, use Deterministic.

The following Mermaid decision tree implements this determination process:

```mermaid
flowchart TD
    A[开始: 描述流计算场景] --> B{讨论抽象层级?}
    B -->|架构/模型/论文| C[使用 Stream Computing / Dataflow Model]
    B -->|工程/实现/代码| D[使用 Stream Processing / Operator]
    B -->|商业/产品/服务| E[使用 Dataflow System / 实时分析产品]

    C --> F{有时间约束要求?}
    F -->|有严格 Deadline| G[使用 Real-time Computing]
    G --> H{Deadline 类型?}
    H -->|错过即灾难| I[Hard Real-time]
    H -->|偶尔错过可容忍| J[Firm Real-time]
    H -->|仅性能降级| K[Soft Real-time]
    F -->|无 Deadline，仅低延迟| L[使用 Stream Processing]

    D --> M{需要状态?}
    M -->|无状态/逐条处理| N[使用 Stateless Operator / Function]
    M -->|有状态/窗口聚合| O[使用 Stateful Operator / Transformation]

    O --> P{数据来源与去向?}
    P -->|内部数据流| Q[使用 Stream / Flow]
    P -->|外部事件触发| R[使用 Event Sequence / Event-driven]
    P -->|持久化重放| S[使用 Log / Kafka]

    N --> T{自定义逻辑?}
    T -->|使用内置算子| U[使用 Operator: map/filter/flatMap]
    T -->|用户自定义| V[使用 UDF / UDAF / UDTF]

    L --> W{优化目标?}
    W -->|单条快| X[优化 Latency]
    W -->|总量大| Y[优化 Throughput]
    W -->|结果新| Z[优化 Freshness / Watermark]

    W --> AA{容错语义?}
    AA -->|内部不重复| AB[使用 Deterministic + Checkpoint]
    AA -->|端到端不重复| AC[使用 Exactly-once = Deterministic + 事务Sink]
    AA -->|Sink可重复写| AD[使用 Idempotent Sink]
```

### Thm-T-01-02: Non-interchangeability of Stream vs Flow vs Event Sequence vs Log

**Theorem**: There exists a system property $\phi$ such that:

$$\text{Stream} \models \phi \land \text{Flow} \not\models \phi \land \text{EventSequence} \not\models \phi \land \text{Log} \not\models \phi$$

**Proof**:

Let $\phi =$ "supports out-of-order data reordering".

- Stream: The Flink DataStream API explicitly supports Event Time and Watermark mechanisms, capable of handling out-of-order data, thus $\text{Stream} \models \phi$.
- Flow: Network flows (such as TCP flow) are ordered transmission abstractions of bytes, providing no cross-partition out-of-order reordering semantics, thus $\text{Flow} \not\models \phi$.
- Event Sequence: Event sequences in CEP (Complex Event Processing) typically require processing by causal order or pattern order, not natively supporting out-of-order handling, thus $\text{EventSequence} \not\models \phi$.
- Log: Kafka Log is a persistent sequence that is ordered within partitions but unordered across partitions; consumers must handle out-of-order themselves, thus $\text{Log} \not\models \phi$.

Therefore, the four terms are not interchangeable.

### Thm-T-01-03: End-to-End Impossibility of Exactly-once (without Cooperation)

**Theorem**: If the Sink lacks idempotency or transactional capabilities, end-to-end exactly-once cannot be achieved solely through the stream processing engine's internal exactly-once guarantee.

**Proof**:

Assume the engine internally guarantees exactly-once (through checkpoint and recovery). Consider the fault scenario:

1. The engine successfully processes event $e$, generating output $o = f(e)$.
2. The Sink writes $o$ to an external database, but the write acknowledgment is lost before returning to the engine.
3. The engine rolls back to the checkpoint due to not receiving the acknowledgment, reprocesses $e$, and generates $o$ again.
4. The Sink writes $o$ again, causing duplication in the external system.

Unless the Sink possesses:

- Idempotency: $g(o) = g(g(o))$, where repeated writes produce no additional side effects; or
- Transactionality: writes are bound to checkpoints, and unacknowledged writes are rolled back externally.

Otherwise, end-to-end exactly-once cannot hold. QED.

---

## 6. Examples

### 6.1 Example: Precise Terminology Usage in Flink Jobs

```java
// Correct terminology mapping example
StreamExecutionEnvironment env =
    StreamExecutionEnvironment.getExecutionEnvironment();

// DataStream = Stream（无限数据序列）
DataStream<Event> stream = env.addSource(new KafkaSource<>());

// keyBy = Transformation（图级重写，定义分区策略）
// window = Operator（带状态的计算节点）
DataStream<Result> result = stream
    .keyBy(Event::getUserId)                    // Transformation
    .window(TumblingEventTimeWindows.of(
        Time.minutes(5)))                       // Window Operator
    .aggregate(new CountAggregate());           // UDAF（UDF 的一种）

// 精确一次语义配置
env.enableCheckpointing(60000);
env.getCheckpointConfig().setCheckpointingMode(
    CheckpointingMode.EXACTLY_ONCE);            // Exactly-once 系统语义
```

**Terminology Mapping Verification**:

- `DataStream` → Stream (Def-T-01-13)
- `keyBy` → Transformation (Def-T-01-10), not Operator (Lemma-T-01-05)
- `window + aggregate` → Stateful Operator (Def-T-01-09)
- `CountAggregate` → UDAF (Def-T-01-12)
- `EXACTLY_ONCE` → System-level semantics (Def-T-01-15)

### 6.2 Example: Technical Document Terminology Correction

**Original Text (with Confusion)**: "Our real-time data stream system is based on the Dataflow model, uses the Google Dataflow engine, achieves exactly-once deterministic computing through custom Functions, and guarantees low latency and high freshness."

**Problem Diagnosis**:

1. "Real-time" does not distinguish hard/soft/firm.
2. "Dataflow model" and "Dataflow engine" are confused.
3. "Function" should be "UDF" (if accessing runtime state).
4. "exactly-once" and "deterministic computing" are juxtaposed, implying equivalence (Thm-T-01-03 has proven they are not).
5. "latency" and "freshness" are conflated.

**Corrected Version**: "Our low-latency stream processing system (soft real-time, latency target P99 < 2s) adopts the Dataflow Model (Akidau et al., 2015) as the computational abstraction, running on a self-hosted Flink Dataflow Engine. Business logic is implemented via Java UDFs, with exactly-once semantics configured at the engine layer (based on checkpoint + transactional Kafka Sink), and deterministic execution guaranteed at the operator layer. The system has a single-record processing latency averaging 50ms, while result freshness depends on watermark progress (typically lagging 10~30s)."

---

## 7. Visualizations

### 7.1 Terminology × Dimension Concept Matrix

```mermaid
graph TB
    subgraph "维度: 抽象层"
        direction LR
        A1[L1 物理] --- A2[L2 逻辑] --- A3[L3 数学] --- A4[L4 商业]
    end

    subgraph "维度: 时间要求"
        direction LR
        T1[None] --- T2[Soft] --- T3[Firm] --- T4[Hard]
    end

    subgraph "维度: 状态"
        direction LR
        S1[Stateless] --- S2[Bounded] --- S3[Unbounded]
    end

    subgraph "维度: 语义保证"
        direction LR
        G1[At-most-once] --- G2[At-least-once] --- G3[Exactly-once] --- G4[Deterministic]
    end

    subgraph "术语定位"
        direction TB
        SC["Stream Computing<br/>[L3, Soft, Unbounded, -]"]
        SP["Stream Processing<br/>[L2, Soft, Stateful, ALO/EO]"]
        RT["Real-time Computing<br/>[L3, Hard/Firm, -, -]"]
        ED["Event-driven<br/>[L2, Soft, Stateless, -]"]
        DM["Dataflow Model<br/>[L3, -, -, Deterministic]"]
        DS["Dataflow System<br/>[L4, Soft, Stateful, EO]"]
        DE["Dataflow Engine<br/>[L1, Soft, Stateful, EO]"]
        OP["Operator<br/>[L2, -, Stateful, -]"]
        TR["Transformation<br/>[L2, -, -, -]"]
        FN["Function<br/>[L3, -, Stateless, Deterministic]"]
        UDF["UDF<br/>[L2, -, Stateful*, -]"]
        ST["Stream<br/>[L3, -, -, -]"]
        FL["Flow<br/>[L2, -, -, -]"]
        ES["Event Sequence<br/>[L3, -, -, -]"]
        LG["Log<br/>[L1, -, -, -]"]
        LA["Latency<br/>[L1, Hard/Soft, -, -]"]
        TH["Throughput<br/>[L1, -, -, -]"]
        FR["Freshness<br/>[L2, Soft, -, -]"]
        DET["Deterministic<br/>[L3, -, -, Det]"]
        EO["Exactly-once<br/>[L2, -, Stateful, EO]"]
        IDP["Idempotent<br/>[L2, -, -, -]"]
    end
```

### 7.2 Boundary Decision Tree: "Which Term Should I Use for My Scenario?"

```mermaid
flowchart TD
    ROOT["场景: 我需要描述一个数据处理系统"] --> Q1["Q1: 数据是连续到达的吗？"]
    Q1 -->|否| B1["使用 Batch Processing<br/>术语集: Job/Task/Stage"]
    Q1 -->|是| Q2["Q2: 强调计算范式还是具体实现？"]

    Q2 -->|范式/理论| Q3["Q3: 是否强调时间约束保证？"]
    Q3 -->|是| Q4["Q4: 错过 deadline 的后果？"]
    Q4 -->|灾难性| RT1["术语: Hard Real-time Computing<br/>例: 飞控系统、医疗设备"]
    Q4 -->|可丢弃| RT2["术语: Firm Real-time Computing<br/>例: 视频会议帧"]
    Q4 -->|仅降级| RT3["术语: Soft Real-time Computing<br/>例: 推荐系统、监控告警"]
    Q3 -->|否| SC1["术语: Stream Computing<br/>强调持续计算范式"]

    Q2 -->|实现/工程| Q5["Q5: 使用什么编程模型？"]
    Q5 -->|Dataflow/Beam| DM1["术语: Stream Processing on Dataflow Model<br/>子术语: Window/Trigger/Watermark"]
    Q5 -->|Actor/Reactive| ED1["术语: Event-driven Processing<br/>子术语: Event Handler/Event Loop"]
    Q5 -->|未确定| SP1["术语: Stream Processing<br/>通用实现层术语"]

    SP1 --> Q6["Q6: 讨论代码还是架构？"]
    Q6 -->|代码| Q7["Q7: 逻辑是内置还是自定义？"]
    Q7 -->|内置| OP1["术语: Operator<br/>map/filter/aggregate/window"]
    Q7 -->|自定义| UDF1["术语: UDF / UDAF / UDTF<br/>含 RuntimeContext 的用户函数"]
    Q6 -->|架构| Q8["Q8: 讨论运行环境还是商业产品？"]
    Q8 -->|运行环境| DE1["术语: Dataflow Engine / Stream Processor<br/>例: Flink JobManager/TaskManager"]
    Q8 -->|商业产品| DS1["术语: Dataflow System / Managed Service<br/>例: Google Cloud Dataflow"]

    Q6 -->|数据对象| Q9["Q9: 数据的本质特征？"]
    Q9 -->|连续时间序列| ST1["术语: Stream<br/>强调时间连续性"]
    Q9 -->|网络路径| FL1["术语: Flow / Dataflow<br/>强调拓扑与传输"]
    Q9 -->|因果事件链| ES1["术语: Event Sequence<br/>强调事件语义与模式"]
    Q9 -->|持久化记录| LG1["术语: Log / Topic<br/>强调不可变与可重放"]

    Q6 -->|性能指标| Q10["Q10: 关注哪类指标？"]
    Q10 -->|单条快慢| LA1["术语: Latency<br/>事件产生到处理完成的间隔"]
    Q10 -->|总量多大| TH1["术语: Throughput<br/>单位时间处理记录数"]
    Q10 -->|结果多新| FR1["术语: Freshness<br/>结果反映的最新事件时间"]

    Q6 -->|语义保证| Q11["Q11: 容错场景下需要什么保证？"]
    Q11 -->|输出唯一确定| DET1["术语: Deterministic<br/>相同输入必得相同输出"]
    Q11 -->|不丢不重| EO1["术语: Exactly-once<br/>端到端恰好一次生效"]
    Q11 -->|重复无害| IDP1["术语: Idempotent<br/>重复执行结果不变"]
```

### 7.3 Radar Chart for Six Groups of Confusable Concepts

```mermaid
radarChart
    title 六组术语辨析雷达（相似度 0-10，0=完全区分，10=完全等同）
    axis StreamComputing, StreamProcessing, RealTimeComputing, EventDriven
    axis DataflowModel, DataflowSystem, DataflowEngine
    axis Operator, Transformation, Function, UDF
    axis Stream, Flow, EventSequence, Log
    axis Latency, Throughput, Freshness
    axis Deterministic, ExactlyOnce, Idempotent

    "组1: 计算范式": [2, 2, 7, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    "组2: Dataflow": [0, 0, 0, 0, 2, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    "组3: 编程抽象": [0, 0, 0, 0, 0, 0, 0, 3, 2, 4, 0, 0, 0, 0, 0, 0, 0, 0]
    "组4: 数据对象": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 3, 0, 0, 0, 0, 0]
    "组5: 性能指标": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 3, 0, 0]
    "组6: 语义保证": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 4, 3]
```

---

## 8. References

[^1]: Wikipedia, "Stream processing", <https://en.wikipedia.org/wiki/Stream_processing>. "Stream processing is a computer programming paradigm, equivalent to dataflow programming, event stream processing, and reactive programming..."

[^2]: Wikipedia, "Real-time computing", <https://en.wikipedia.org/wiki/Real-time_computing>. "Real-time computing describes hardware and software systems subject to a 'real-time constraint'... The correctness of these types of systems depends on their temporal aspects as well as their functional aspects."

[^3]: Wikipedia, "Event-driven architecture", <https://en.wikipedia.org/wiki/Event-driven_architecture>. "Event-driven architecture is a software architecture paradigm revolving around the production, detection, consumption of, and reaction to events."

[^4]: T. Akidau et al., "The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing", PVLDB, 8(12), 2015.

[^5]: Google Cloud, "What is Dataflow?", <https://cloud.google.com/dataflow/docs/concepts>. "Dataflow is a fully managed streaming analytics service that minimizes latency..."

[^6]: Apache Flink Documentation, "User-defined Functions", <https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/functions/udfs/>. "User-defined functions (UDFs) are extension points to call frequently used logic or custom logic..."

[^7]: Wikipedia, "Dataflow", <https://en.wikipedia.org/wiki/Dataflow>. "Dataflow is a broad concept that can refer to data in motion or the flow of data through a system."

---

## Appendix A: Project Internal Unified Usage Recommendations

| Scenario | Recommended Term | Avoid Using | Rationale |
|----------|-----------------|-------------|-----------|
| Describing Flink/Spark continuous computing capabilities | Stream Processing | Real-time Computing | Avoid the deadline implication of "real-time" |
| Describing the Dataflow paper abstraction | Dataflow Model | Dataflow | Distinguish model from implementation |
| Describing Google Cloud managed service | Google Cloud Dataflow | Dataflow | Precisely point to the product |
| Describing Flink execution layer | Dataflow Engine / Stream Processor | Dataflow | Avoid confusion with the model |
| Describing computation nodes in code | Operator | Function | Operator includes state and port semantics |
| Describing graph operations at API layer | Transformation | Operator | Transformation includes graph rewriting |
| Describing user-defined logic | UDF / UDAF / UDTF | Function | Emphasize runtime context |
| Describing pure mathematical logic | Function | UDF | Stateless, no runtime dependency |
| Describing Kafka data carrier | Log / Topic | Stream | Log emphasizes immutability and replay |
| Describing Flink DataStream | Stream | Flow | Stream emphasizes temporal continuity |
| Describing network transmission path | Flow | Stream | Flow emphasizes topological path |
| Describing CEP input | Event Sequence | Stream | Emphasizes event semantics and patterns |
| Describing single-record processing speed | Latency | Latency (alone) | Clarify the metric definition |
| Describing system capacity | Throughput | QPS/TPS (mixed usage) | Unify using throughput |
| Describing result timeliness | Freshness | Real-time-ness | Avoid confusion with real-time |
| Describing function property | Deterministic | Exactly-once | Distinguish function property from system semantics |
| Describing system non-duplication guarantee | Exactly-once | No-loss-no-duplicate | Use standard terminology |
| Describing operation idempotency | Idempotent | Repeatable execution | Use mathematical standard terminology |

---

## Appendix B: Quick Reference Tables for Six Term Groups

### Group 1: Stream Computing vs Stream Processing vs Real-time Computing vs Event-driven

| Dimension | Stream Computing | Stream Processing | Real-time Computing | Event-driven |
|-----------|-----------------|-------------------|---------------------|--------------|
| **Wikipedia Definition** | Paradigm where data is computed upon arrival[^1] | Technique for real-time analysis of continuous data[^1] | Systems subject to time constraints[^2] | Architecture around event production-consumption-reaction[^3] |
| **Abstraction Level** | L3 (Paradigm) | L2 (Implementation) | L3 (System Classification) | L2 (Architecture Pattern) |
| **Time Requirement** | Soft/None | Soft | Hard/Firm/Soft | Soft |
| **State** | Optional | Usually Stateful | Usually Stateful | Usually Stateless |
| **Typical Systems** | Theoretical models | Flink, Kafka Streams | RTOS, VxWorks | Node.js, GUI frameworks |
| **Chinese Misuse** | Conflated with "stream processing" | Conflated with "real-time computing" | Generalized as "fast" | Generalized as "asynchronous" |

### Group 2: Dataflow Model vs Dataflow System vs Dataflow Engine

| Dimension | Dataflow Model | Dataflow System | Dataflow Engine |
|-----------|---------------|-----------------|-----------------|
| **Definition Source** | Akidau et al., VLDB 2015[^4] | Google Cloud product documentation[^5] | General systems architecture concept |
| **Essence** | Mathematical abstraction (What/Where/When/How) | Managed cloud service | Execution runtime |
| **Open-source Equivalent** | Apache Beam SDK | Google Cloud Dataflow | Flink Runtime, Spark DAGScheduler |
| **Confusion Consequence** | Limiting the model to a Google product | Generalizing the product as a universal concept | Equating the runtime with the programming model |

### Group 3: Operator vs Transformation vs Function vs UDF

| Dimension | Operator | Transformation | Function | UDF |
|-----------|----------|---------------|----------|-----|
| **Existence Level** | Execution graph / physical plan | Logical plan / API | Mathematics / pure logic | SQL / Table API extension |
| **State** | Usually Stateful | Optional | Stateless | Can access Runtime State |
| **Side Effects** | May include I/O | Usually none | None | Controllable (via Runtime) |
| **Flink Example** | `WindowOperator` | `keyBy`, `window` | `MapFunction.apply` | `ScalarFunction.eval` |
| **Invocation Frequency** | Per record | Defines graph structure | Per record | Per record (with context) |

### Group 4: Stream vs Flow vs Event Sequence vs Log

| Dimension | Stream | Flow | Event Sequence | Log |
|-----------|--------|------|---------------|-----|
| **Core Characteristic** | Temporal continuity | Topological path | Causal/pattern order | Immutable persistence |
| **Out-of-order Support** | Native (Watermark) | None | Limited (CEP) | None across partitions |
| **Persistence** | Optional | None | Optional | Core characteristic |
| **Replay Capability** | Depends on Source | None | Depends on storage | Native |
| **Typical Technology** | Flink DataStream | SDN Flow, TCP Flow | Esper CEP | Kafka Log |

### Group 5: Latency vs Throughput vs Freshness

| Dimension | Latency | Throughput | Freshness |
|-----------|---------|-----------|-----------|
| **Definition** | Single-record: event time → processing complete | System: records / time unit | Result: current time - latest event time |
| **Optimization Means** | Reduce buffering, locality | Increase buffering, batching | Shorten watermark lag |
| **Unit** | ms / s | records/s, MB/s | s / min |
| **Relationship to Delay** | Direct measurement | Indirect influence | Can be independent of single-record latency |
| **Typical Pitfall** | Low latency ≠ high freshness | High throughput ≠ low latency | High freshness requires tolerating latency |

### Group 6: Deterministic vs Exactly-once vs Idempotent

| Dimension | Deterministic | Exactly-once | Idempotent |
|-----------|--------------|--------------|------------|
| **Definition Domain** | Function property | System semantics | Operation property |
| **Formalization** | $f(x)$ is unique | effect(e) applied exactly once | $g(g(x)) = g(x)$ |
| **Implementation Layer** | User code | Engine + Sink coordination | Sink / external system |
| **Independent Guarantee** | Cannot guarantee EO alone | Requires Deterministic or Idempotent | Cannot cover intermediate state duplication |
| **Flink Implementation** | Stateful operator deterministic replay | Checkpoint + transactional Sink | Idempotent Kafka Producer |

---

*Document Version: v1.0 | Last Updated: 2026-04-30 | Quality Gates: Six-section ✓ | Mermaid Diagrams 3/3 ✓ | Formal Elements 15+ ✓*

---

## 5. Proof / Engineering Argument

### Thm-T-01-01: Formal Completeness of Terminology Selection Decision Tree

**Theorem**: For any stream computing scenario $C$, there exists a unique terminology subset $T_C \subseteq \mathcal{T}$, such that $T_C$ precisely describes the technical characteristics of $C$, and $\forall t_1, t_2 \in T_C$, $t_1$ and $t_2$ are not redundant.

**Proof Framework**:

1. **Abstraction Level Determination**: If $C$ discusses architecture design, use $L_3$ and above terminologies (Model, Paradigm); if $C$ discusses code implementation, use $L_2$ terminologies (Operator, UDF).

2. **Time Constraint Determination**: If $C$ requires deadline guarantee, use Real-time Computing and its subclasses (Hard/Firm/Soft); if only low latency is required, use Stream Processing.

3. **State Requirement Determination**: If $C$ involves infinite state aggregation, use Stateful Stream Processing; if only per-record filtering, use Stateless.

4. **Semantic Guarantee Determination**: If $C$ requires end-to-end no-duplicates, use Exactly-once; if only internal determinism is required, use Deterministic.

The following Mermaid decision tree implements this determination process:

```mermaid
flowchart TD
    A[开始: 描述流计算场景] --> B{讨论抽象层级?}
    B -->|架构/模型/论文| C[使用 Stream Computing / Dataflow Model]
    B -->|工程/实现/代码| D[使用 Stream Processing / Operator]
    B -->|商业/产品/服务| E[使用 Dataflow System / 实时分析产品]

    C --> F{有时间约束要求?}
    F -->|有严格 Deadline| G[使用 Real-time Computing]
    G --> H{Deadline 类型?}
    H -->|错过即灾难| I[Hard Real-time]
    H -->|偶尔错过可容忍| J[Firm Real-time]
    H -->|仅性能降级| K[Soft Real-time]
    F -->|无 Deadline，仅低延迟| L[使用 Stream Processing]

    D --> M{需要状态?}
    M -->|无状态/逐条处理| N[使用 Stateless Operator / Function]
    M -->|有状态/窗口聚合| O[使用 Stateful Operator / Transformation]

    O --> P{数据来源与去向?}
    P -->|内部数据流| Q[使用 Stream / Flow]
    P -->|外部事件触发| R[使用 Event Sequence / Event-driven]
    P -->|持久化重放| S[使用 Log / Kafka]

    N --> T{自定义逻辑?}
    T -->|使用内置算子| U[使用 Operator: map/filter/flatMap]
    T -->|用户自定义| V[使用 UDF / UDAF / UDTF]

    L --> W{优化目标?}
    W -->|单条快| X[优化 Latency]
    W -->|总量大| Y[优化 Throughput]
    W -->|结果新| Z[优化 Freshness / Watermark]

    W --> AA{容错语义?}
    AA -->|内部不重复| AB[使用 Deterministic + Checkpoint]
    AA -->|端到端不重复| AC[使用 Exactly-once = Deterministic + 事务Sink]
    AA -->|Sink可重复写| AD[使用 Idempotent Sink]
```

### Thm-T-01-02: Non-interchangeability of Stream vs Flow vs Event Sequence vs Log

**Theorem**: There exists a system property $\phi$ such that:

$$\text{Stream} \models \phi \land \text{Flow} \not\models \phi \land \text{EventSequence} \not\models \phi \land \text{Log} \not\models \phi$$

**Proof**:

Let $\phi =$ "supports out-of-order data reordering".

- Stream: Flink DataStream API explicitly supports Event Time and Watermark mechanisms, capable of handling out-of-order data, hence $\text{Stream} \models \phi$.
- Flow: Network flows (such as TCP flow) are ordered transmission abstractions of bytes, providing no cross-partition out-of-order reordering semantics, hence $\text{Flow} \not\models \phi$.
- Event Sequence: Event sequences in CEP (Complex Event Processing) typically require processing by causal order or pattern order, not naturally supporting out-of-order handling, hence $\text{EventSequence} \not\models \phi$.
- Log: Kafka Log is a persistent sequence that is ordered within partitions and unordered across partitions; consumers must handle out-of-order themselves, hence $\text{Log} \not\models \phi$.

Therefore the four terminologies are not interchangeable.

### Thm-T-01-03: End-to-end Impossibility of Exactly-once (without Cooperation)

**Theorem**: If the Sink does not possess idempotency or transactional capability, then end-to-end exactly-once cannot be achieved solely through internal exactly-once guarantees of the stream processing engine.

**Proof**:

Assume the engine internally guarantees exactly-once (through checkpoint and recovery). Consider the fault scenario:

1. The engine successfully processes event $e$, generating output $o = f(e)$.
2. The Sink writes $o$ to the external database, but the write acknowledgment is lost before returning to the engine.
3. The engine rolls back to checkpoint due to not receiving acknowledgment, reprocesses $e$, and generates $o$ again.
4. The Sink writes $o$ again, causing duplicates in the external system.

Unless the Sink possesses:

- Idempotency: $g(o) = g(g(o))$, repeated writes have no additional side effects; or
- Transactionality: writes are bound to checkpoints, unacknowledged writes are rolled back externally.

Otherwise end-to-end exactly-once cannot hold. QED.

---

## 6. Examples

### 6.1 Example: Precise Terminology Usage in Flink Jobs

```java
// Correct terminology mapping example
StreamExecutionEnvironment env =
    StreamExecutionEnvironment.getExecutionEnvironment();

// DataStream = Stream (infinite data sequence)
DataStream<Event> stream = env.addSource(new KafkaSource<>());

// keyBy = Transformation (graph-level rewrite, defines partitioning strategy)
// window = Operator (stateful computation node)
DataStream<Result> result = stream
    .keyBy(Event::getUserId)                    // Transformation
    .window(TumblingEventTimeWindows.of(
        Time.minutes(5)))                       // Window Operator
    .aggregate(new CountAggregate());           // UDAF (a type of UDF)

// Exactly-once semantics configuration
env.enableCheckpointing(60000);
env.getCheckpointConfig().setCheckpointingMode(
    CheckpointingMode.EXACTLY_ONCE);            // Exactly-once system semantics
```

**Terminology Mapping Verification**:

- `DataStream` → Stream (Def-T-01-13)
- `keyBy` → Transformation (Def-T-01-10), not Operator (Lemma-T-01-05)
- `window + aggregate` → Stateful Operator (Def-T-01-09)
- `CountAggregate` → UDAF (Def-T-01-12)
- `EXACTLY_ONCE` → System-level semantics (Def-T-01-15)

### 6.2 Example: Technical Document Terminology Correction

**Original Text (with confusion)**: "Our real-time data stream system is based on the Dataflow model, uses the Google Dataflow engine, achieves exactly-once deterministic computing through custom Functions, guaranteeing low latency and high freshness."

**Problem Diagnosis**:

1. "Real-time" does not distinguish hard/soft/firm.
2. "Dataflow model" and "Dataflow engine" are confused.
3. "Function" should be "UDF" (if accessing runtime state).
4. "exactly-once" and "deterministic computing" are juxtaposed, implying equivalence (Thm-T-01-03 has proven they are not).
5. "latency" and "freshness" are conflated.

**Corrected Version**: "Our low-latency stream processing system (soft real-time, latency target P99 < 2s) adopts the Dataflow Model (Akidau et al., 2015) as its computational abstraction, running on a self-hosted Flink Dataflow Engine. Business logic is implemented through Java UDFs; the engine layer is configured with exactly-once semantics (based on checkpoint + transactional Kafka Sink); the operator layer guarantees deterministic execution. The system has mean single-record processing latency of 50ms; result freshness depends on watermark progress (typically lagging 10~30s)."

---

## 7. Visualizations

### 7.1 Terminology × Dimension Concept Matrix

```mermaid
graph TB
    subgraph "维度: 抽象层"
        direction LR
        A1[L1 物理] --- A2[L2 逻辑] --- A3[L3 数学] --- A4[L4 商业]
    end

    subgraph "维度: 时间要求"
        direction LR
        T1[None] --- T2[Soft] --- T3[Firm] --- T4[Hard]
    end

    subgraph "维度: 状态"
        direction LR
        S1[Stateless] --- S2[Bounded] --- S3[Unbounded]
    end

    subgraph "维度: 语义保证"
        direction LR
        G1[At-most-once] --- G2[At-least-once] --- G3[Exactly-once] --- G4[Deterministic]
    end

    subgraph "术语定位"
        direction TB
        SC["Stream Computing<br/>[L3, Soft, Unbounded, -]"]
        SP["Stream Processing<br/>[L2, Soft, Stateful, ALO/EO]"]
        RT["Real-time Computing<br/>[L3, Hard/Firm, -, -]"]
        ED["Event-driven<br/>[L2, Soft, Stateless, -]"]
        DM["Dataflow Model<br/>[L3, -, -, Deterministic]"]
        DS["Dataflow System<br/>[L4, Soft, Stateful, EO]"]
        DE["Dataflow Engine<br/>[L1, Soft, Stateful, EO]"]
        OP["Operator<br/>[L2, -, Stateful, -]"]
        TR["Transformation<br/>[L2, -, -, -]"]
        FN["Function<br/>[L3, -, Stateless, Deterministic]"]
        UDF["UDF<br/>[L2, -, Stateful*, -]"]
        ST["Stream<br/>[L3, -, -, -]"]
        FL["Flow<br/>[L2, -, -, -]"]
        ES["Event Sequence<br/>[L3, -, -, -]"]
        LG["Log<br/>[L1, -, -, -]"]
        LA["Latency<br/>[L1, Hard/Soft, -, -]"]
        TH["Throughput<br/>[L1, -, -, -]"]
        FR["Freshness<br/>[L2, Soft, -, -]"]
        DET["Deterministic<br/>[L3, -, -, Det]"]
        EO["Exactly-once<br/>[L2, -, Stateful, EO]"]
        IDP["Idempotent<br/>[L2, -, -, -]"]
    end
```

### 7.2 Boundary Decision Tree: "Which Term Should I Use for My Scenario?"

```mermaid
flowchart TD
    ROOT["场景: 我需要描述一个数据处理系统"] --> Q1["Q1: 数据是连续到达的吗？"]
    Q1 -->|否| B1["使用 Batch Processing<br/>术语集: Job/Task/Stage"]
    Q1 -->|是| Q2["Q2: 强调计算范式还是具体实现？"]

    Q2 -->|范式/理论| Q3["Q3: 是否强调时间约束保证？"]
    Q3 -->|是| Q4["Q4: 错过 deadline 的后果？"]
    Q4 -->|灾难性| RT1["术语: Hard Real-time Computing<br/>例: 飞控系统、医疗设备"]
    Q4 -->|可丢弃| RT2["术语: Firm Real-time Computing<br/>例: 视频会议帧"]
    Q4 -->|仅降级| RT3["术语: Soft Real-time Computing<br/>例: 推荐系统、监控告警"]
    Q3 -->|否| SC1["术语: Stream Computing<br/>强调持续计算范式"]

    Q2 -->|实现/工程| Q5["Q5: 使用什么编程模型？"]
    Q5 -->|Dataflow/Beam| DM1["术语: Stream Processing on Dataflow Model<br/>子术语: Window/Trigger/Watermark"]
    Q5 -->|Actor/Reactive| ED1["术语: Event-driven Processing<br/>子术语: Event Handler/Event Loop"]
    Q5 -->|未确定| SP1["术语: Stream Processing<br/>通用实现层术语"]

    SP1 --> Q6["Q6: 讨论代码还是架构？"]
    Q6 -->|代码| Q7["Q7: 逻辑是内置还是自定义？"]
    Q7 -->|内置| OP1["术语: Operator<br/>map/filter/aggregate/window"]
    Q7 -->|自定义| UDF1["术语: UDF / UDAF / UDTF<br/>含 RuntimeContext 的用户函数"]
    Q6 -->|架构| Q8["Q8: 讨论运行环境还是商业产品？"]
    Q8 -->|运行环境| DE1["术语: Dataflow Engine / Stream Processor<br/>例: Flink JobManager/TaskManager"]
    Q8 -->|商业产品| DS1["术语: Dataflow System / Managed Service<br/>例: Google Cloud Dataflow"]

    Q6 -->|数据对象| Q9["Q9: 数据的本质特征？"]
    Q9 -->|连续时间序列| ST1["术语: Stream<br/>强调时间连续性"]
    Q9 -->|网络路径| FL1["术语: Flow / Dataflow<br/>强调拓扑与传输"]
    Q9 -->|因果事件链| ES1["术语: Event Sequence<br/>强调事件语义与模式"]
    Q9 -->|持久化记录| LG1["术语: Log / Topic<br/>强调不可变与可重放"]

    Q6 -->|性能指标| Q10["Q10: 关注哪类指标？"]
    Q10 -->|单条快慢| LA1["术语: Latency<br/>事件产生到处理完成的间隔"]
    Q10 -->|总量多大| TH1["术语: Throughput<br/>单位时间处理记录数"]
    Q10 -->|结果多新| FR1["术语: Freshness<br/>结果反映的最新事件时间"]

    Q6 -->|语义保证| Q11["Q11: 容错场景下需要什么保证？"]
    Q11 -->|输出唯一确定| DET1["术语: Deterministic<br/>相同输入必得相同输出"]
    Q11 -->|不丢不重| EO1["术语: Exactly-once<br/>端到端恰好一次生效"]
    Q11 -->|重复无害| IDP1["术语: Idempotent<br/>重复执行结果不变"]
```

### 7.3 Radar Chart for Six Groups of Confusable Concepts

```mermaid
radarChart
    title 六组术语辨析雷达（相似度 0-10，0=完全区分，10=完全等同）
    axis StreamComputing, StreamProcessing, RealTimeComputing, EventDriven
    axis DataflowModel, DataflowSystem, DataflowEngine
    axis Operator, Transformation, Function, UDF
    axis Stream, Flow, EventSequence, Log
    axis Latency, Throughput, Freshness
    axis Deterministic, ExactlyOnce, Idempotent

    "组1: 计算范式": [2, 2, 7, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    "组2: Dataflow": [0, 0, 0, 0, 2, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    "组3: 编程抽象": [0, 0, 0, 0, 0, 0, 0, 3, 2, 4, 0, 0, 0, 0, 0, 0, 0, 0]
    "组4: 数据对象": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 3, 0, 0, 0, 0, 0]
    "组5: 性能指标": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 3, 0, 0]
    "组6: 语义保证": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 4, 3]
```

---

## 8. References

[^1]: Wikipedia, "Stream processing", <https://en.wikipedia.org/wiki/Stream_processing>. "Stream processing is a computer programming paradigm, equivalent to dataflow programming, event stream processing, and reactive programming..."

[^2]: Wikipedia, "Real-time computing", <https://en.wikipedia.org/wiki/Real-time_computing>. "Real-time computing describes hardware and software systems subject to a 'real-time constraint'... The correctness of these types of systems depends on their temporal aspects as well as their functional aspects."

[^3]: Wikipedia, "Event-driven architecture", <https://en.wikipedia.org/wiki/Event-driven_architecture>. "Event-driven architecture is a software architecture paradigm revolving around the production, detection, consumption of, and reaction to events."

[^4]: T. Akidau et al., "The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing", PVLDB, 8(12), 2015.

[^5]: Google Cloud, "What is Dataflow?", <https://cloud.google.com/dataflow/docs/concepts>. "Dataflow is a fully managed streaming analytics service that minimizes latency..."

[^6]: Apache Flink Documentation, "User-defined Functions", <https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/functions/udfs/>. "User-defined functions (UDFs) are extension points to call frequently used logic or custom logic..."

[^7]: Wikipedia, "Dataflow", <https://en.wikipedia.org/wiki/Dataflow>. "Dataflow is a broad concept that can refer to data in motion or the flow of data through a system."

---

## Appendix A: Project Internal Unified Usage Recommendations

| Scenario | Recommended Term | Avoid Using | Reason |
|----------|-----------------|-------------|--------|
| Describing Flink/Spark continuous computing capability | Stream Processing | Real-time Computing | Avoid the deadline implication of "real-time" |
| Describing Dataflow paper abstraction | Dataflow Model | Dataflow | Distinguish model from implementation |
| Describing Google Cloud managed service | Google Cloud Dataflow | Dataflow | Precisely point to the product |
| Describing Flink execution layer | Dataflow Engine / Stream Processor | Dataflow | Avoid confusion with the model |
| Describing computation nodes in code | Operator | Function | Operator includes state and port semantics |
| Describing API-level graph operations | Transformation | Operator | Transformation includes graph rewrites |
| Describing user-customized logic | UDF / UDAF / UDTF | Function | Emphasizes runtime context |
| Describing pure mathematical logic | Function | UDF | Stateless, no runtime dependency |
| Describing Kafka data carrier | Log / Topic | Stream | Log emphasizes immutability and replay |
| Describing Flink DataStream | Stream | Flow | Stream emphasizes temporal continuity |
| Describing network transmission path | Flow | Stream | Flow emphasizes topological path |
| Describing CEP input | Event Sequence | Stream | Emphasizes event semantics and patterns |
| Describing single-record processing speed | Latency | Delay (used alone) | Clear metric definition |
| Describing system capacity | Throughput | QPS/TPS (mixed usage) | Unified use of throughput |
| Describing result timeliness | Freshness | Real-time-ness | Avoid confusion with real-time |
| Describing function property | Deterministic | Exactly-once | Distinguish function property from system semantics |
| Describing system no-duplicate guarantee | Exactly-once | No-loss-no-duplicate | Use standard terminology |
| Describing operation idempotency | Idempotent | Repeatable execution | Use mathematical standard terminology |

---

## Appendix B: Quick Reference for Six Groups of Terminology

### Group 1: Stream Computing vs Stream Processing vs Real-time Computing vs Event-driven

| Dimension | Stream Computing | Stream Processing | Real-time Computing | Event-driven |
|-----------|-----------------|-------------------|---------------------|--------------|
| **Wikipedia Definition** | Paradigm where data triggers computation upon arrival[^1] | Technique for real-time analysis of continuous data[^1] | Systems subject to time constraints[^2] | Architecture revolving around event production-consumption-reaction[^3] |
| **Abstraction Level** | L3 (Paradigm) | L2 (Implementation) | L3 (System Classification) | L2 (Architecture Pattern) |
| **Time Requirement** | Soft/None | Soft | Hard/Firm/Soft | Soft |
| **State** | Optional | Usually Stateful | Usually Stateful | Usually Stateless |
| **Typical Systems** | Theoretical models | Flink, Kafka Streams | RTOS, VxWorks | Node.js, GUI frameworks |
| **Chinese Misuse** | Conflated with "stream processing" | Conflated with "real-time computing" | Generalized to "fast" | Generalized to "asynchronous" |

### Group 2: Dataflow Model vs Dataflow System vs Dataflow Engine

| Dimension | Dataflow Model | Dataflow System | Dataflow Engine |
|-----------|---------------|-----------------|-----------------|
| **Definition Source** | Akidau et al., VLDB 2015[^4] | Google Cloud product documentation[^5] | General system architecture concept |
| **Essence** | Mathematical abstraction (What/Where/When/How) | Managed cloud service | Execution runtime |
| **Open-source Equivalent** | Apache Beam SDK | Google Cloud Dataflow | Flink Runtime, Spark DAGScheduler |
| **Confusion Consequence** | Limiting the model to a Google product | Generalizing the product to a universal concept | Equating runtime with programming model |

### Group 3: Operator vs Transformation vs Function vs UDF

| Dimension | Operator | Transformation | Function | UDF |
|-----------|---------|---------------|----------|-----|
| **Existence Level** | Execution graph / physical plan | Logical plan / API | Mathematics / pure logic | SQL / Table API extension |
| **State** | Usually Stateful | Optional | Stateless | Can access Runtime State |
| **Side Effects** | May contain I/O | Usually none | None | Controllable (through Runtime) |
| **Flink Example** | `WindowOperator` | `keyBy`, `window` | `MapFunction.apply` | `ScalarFunction.eval` |
| **Invocation Frequency** | Per record | Defines graph structure | Per record | Per record (with context) |

### Group 4: Stream vs Flow vs Event Sequence vs Log

| Dimension | Stream | Flow | Event Sequence | Log |
|-----------|--------|------|---------------|-----|
| **Core Characteristic** | Temporal continuity | Topological path | Causal/pattern order | Immutable persistence |
| **Out-of-order Support** | Native (Watermark) | None | Limited (CEP) | None across partitions |
| **Persistence** | Optional | None | Optional | Core characteristic |
| **Replay Capability** | Depends on Source | None | Depends on storage | Native |
| **Typical Technology** | Flink DataStream | SDN Flow, TCP Flow | Esper CEP | Kafka Log |

### Group 5: Latency vs Throughput vs Freshness

| Dimension | Latency | Throughput | Freshness |
|-----------|---------|-----------|-----------|
| **Definition** | Single record: event time → processing completion | System: record count / time unit | Result: current time - latest event time |
| **Optimization Means** | Reduce buffering, locality | Increase buffering, batch processing | Shorten Watermark lag |
| **Unit** | ms / s | records/s, MB/s | s / min |
| **Relation to Delay** | Direct measurement | Indirect influence | Can be independent of single-record latency |
| **Typical Pitfall** | Low latency ≠ high freshness | High throughput ≠ low latency | High freshness requires latency tolerance |

### Group 6: Deterministic vs Exactly-once vs Idempotent

| Dimension | Deterministic | Exactly-once | Idempotent |
|-----------|--------------|--------------|------------|
| **Definition Domain** | Function property | System semantics | Operation property |
| **Formalization** | $f(x)$ is unique | effect(e) exactly once | $g(g(x)) = g(x)$ |
| **Implementation Layer** | User code | Engine + Sink coordination | Sink / external system |
| **Independent Guarantee** | Cannot alone guarantee EO | Depends on Deterministic or Idempotent | Cannot cover intermediate state duplicates |
| **Flink Implementation** | Stateful operator deterministic replay | Checkpoint + transactional Sink | Idempotent Kafka Producer |

---

*Document Version: v1.0 | Last Updated: 2026-04-30 | Quality Gates: Six-section ✓ | Mermaid Diagrams 3/3 ✓ | Formal Elements 15+ ✓*
