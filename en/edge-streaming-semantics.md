# Formal Semantics of Edge Stream Processing

> **Stage**: Struct/ | **Prerequisites**: [01.04-dataflow-model-formalization.md](01.04-dataflow-model-formalization.md), [01.06-petri-net-formalization.md](01.06-petri-net-formalization.md) | **Formalization Level**: L5

## 1. Definitions

Edge Stream Processing sinks stream computing capabilities to network edge devices, enabling local data processing and cloud collaboration in intermittently connected environments.
This section establishes the core formal model of edge stream processing.

### 1.1 Intermittent Connection Model

**Definition Def-S-01-91: Intermittent Connection Model**

Let the set of edge nodes be $\mathcal{E} = \{e_1, e_2, \ldots, e_n\}$, and the cloud node be $c$. The connection state function $\gamma: \mathcal{E} \times \mathbb{T} \rightarrow \{0, 1\}$ is defined as:

$$
\gamma(e, t) = \begin{cases}
1 & \text{if } e \text{ is connected to the cloud at time } t \\
0 & \text{otherwise}
\end{cases}
$$

where $\mathbb{T}$ is the discrete time domain. The intermittent connection period is defined as:

$$
\mathcal{I}(e) = \{ [t_i^{\text{on}}, t_i^{\text{off}}) \}_{i=1}^{k}
$$

satisfying $\forall t \in [t_i^{\text{on}}, t_i^{\text{off}}): \gamma(e, t) = 1$, and the connection availability metric:

$$
\text{Avail}(e) = \frac{\sum_{i=1}^{k} (t_i^{\text{off}} - t_i^{\text{on}})}{t_{\text{now}} - t_0}
$$

> **Intuitive Explanation**: The connection between edge devices and the cloud is not continuously stable; instead, it exhibits an intermittent, pulse-like pattern. The availability metric quantifies the proportion of time an edge device spends in the online state. In typical industrial scenarios, $\text{Avail}(e) \in [0.3, 0.9]$.

### 1.2 Local Buffer Semantics

**Definition Def-S-01-92: Local Buffer Semantics**

The local buffer $B_e$ of edge node $e$ is a finite-capacity priority queue:

$$
B_e = \langle Q_e, \preceq_e, C_e \rangle
$$

where:

- $Q_e \subseteq \mathcal{M} \times \mathbb{T}$ is the timestamped message queue
- $\preceq_e$ is the event-time-based partial order relation
- $C_e \in \mathbb{N}^+$ is the buffer capacity limit

Buffer operations are defined as:

$$
\begin{aligned}
\text{enq}(B_e, m, t) &= \begin{cases}
B_e \oplus \langle m, t \rangle & \text{if } |Q_e| < C_e \\
B_e \oplus \langle m, t \rangle \ominus \min_{\preceq_e}(Q_e) & \text{otherwise (LRU replacement)}
\end{cases} \\
\text{deq}(B_e) &= \langle m, t \rangle \text{ where } \langle m, t \rangle = \min_{\preceq_e}(Q_e)
\end{aligned}
$$

> **Intuitive Explanation**: The local buffer serves as a "temporary storage warehouse" for edge devices. When the network is disconnected, data is first stored here; when the network recovers, it is uploaded in batches. The finite capacity means strategies are needed to decide which data to retain or discard.

### 1.3 Batch Sync Protocol

**Definition Def-S-01-93: Batch Sync Protocol**

The batch sync protocol $\mathcal{P}_{\text{sync}}$ is a quintuple:

$$
\mathcal{P}_{\text{sync}} = \langle \mathcal{S}, \Sigma, \delta, s_0, F \rangle
$$

where:

- $\mathcal{S} = \{\text{IDLE}, \text{COLLECT}, \text{COMPRESS}, \text{TRANSMIT}, \text{ACK}\}$ is the set of protocol states
- $\Sigma = \{\text{conn\_up}, \text{conn\_down}, \text{buffer\_full}, \text{timeout}, \text{ack\_recv}\}$ is the event alphabet
- $\delta: \mathcal{S} \times \Sigma \rightarrow \mathcal{S}$ is the state transition function
- $s_0 = \text{IDLE}$ is the initial state
- $F = \{\text{IDLE}\}$ is the set of accepting states

The batch window is defined as:

$$
W_{\text{batch}} = \langle N_{\max}, T_{\max}, S_{\max} \rangle
$$

Trigger condition:

$$
\text{trigger}(B_e) = (|Q_e| \geq N_{\max}) \lor (t - t_{\text{last}} \geq T_{\max}) \lor (\text{size}(Q_e) \geq S_{\max})
$$

> **Intuitive Explanation**: The batch sync protocol defines the rules of "when to package, how to transmit, and how to acknowledge." Edge devices do not send every message immediately (too resource-intensive); instead, they accumulate a batch and transmit it uniformly, similar to the logic of "fill a truck before dispatching."

### 1.4 Offline Execution Semantics

**Definition Def-S-01-94: Offline Execution**

The offline execution model $\mathcal{X}_{\text{offline}}$ is defined as a triple:

$$
\mathcal{X}_{\text{offline}} = \langle \mathcal{G}_e, \mathcal{D}_e, \mathcal{R}_e \rangle
$$

where:

- $\mathcal{G}_e = \langle V_e, E_e, \lambda_e \rangle$ is the operator graph deployed at the edge, with $V_e \subseteq \mathcal{V}$ (a subset of the global operator set)
- $\mathcal{D}_e: V_e \rightarrow 2^{\mathcal{K}}$ is the mapping from operators to local data shards, where $\mathcal{K}$ is the key space
- $\mathcal{R}_e: E_e \rightarrow \{\text{LOCAL}, \text{REMOTE}\}$ is the mapping from edges to routing strategies

Offline execution capability function:

$$
\text{Cap}(e) = \{ \text{op} \in \mathcal{V} \mid \text{op can execute on } e \text{ with } \gamma(e, t) = 0 \}
$$

Offline state consistency definition:

$$
\mathcal{C}_{\text{offline}}(e, t) = \{ s \in \mathcal{S}_e \mid \forall t' < t: \gamma(e, t') = 0 \Rightarrow \text{state}_e(t') \models \Phi_{\text{local}} \}
$$

where $\Phi_{\text{local}}$ is the local consistency constraint.

> **Intuitive Explanation**: Offline execution semantics answers the question "what can edge devices do when disconnected." By sinking some operators to the edge, devices can still process data and update local states independently even when disconnected from the cloud, synchronizing differences after network recovery.

---

## 2. Properties

### 2.1 Connection State Lemma

**Lemma Lemma-S-01-01: Connection State Transition**

For any edge node $e \in \mathcal{E}$, its connection state $\gamma(e, t)$ satisfies:

$$
\forall t_1 < t_2 < t_3: \gamma(e, t_1) = \gamma(e, t_3) = 1 \land \gamma(e, t_2) = 0 \Rightarrow \exists t_{\text{up}}, t_{\text{down}} \in (t_1, t_3)
$$

such that the connection state completes at least one full transition $1 \rightarrow 0 \rightarrow 1$ within $(t_1, t_3)$.

**Proof Sketch**: By Definition Def-S-01-91, $\gamma$ is a binary function on the discrete time domain. According to the discrete version of the intermediate value principle, state changes must occur through explicit transitions. If $\gamma(e, t_1) = 1$ and $\gamma(e, t_2) = 0$, then there exists $t_{\text{down}} \in (t_1, t_2]$ where the connection breaks; similarly, there exists $t_{\text{up}} \in [t_2, t_3)$ where the connection recovers. $\square$

### 2.2 Buffer Saturation Lemma

**Lemma Lemma-S-01-02: Buffer Saturation**

Let the buffer capacity of edge node $e$ be $C_e$, the input rate be $\lambda_{\text{in}}(t)$, and the output (sync) rate be $\lambda_{\text{out}}(t)$. If:

$$
\exists T > 0: \int_{t_0}^{t_0+T} (\lambda_{\text{in}}(\tau) - \lambda_{\text{out}}(\tau)) \cdot \gamma(e, \tau) \, d\tau > C_e
$$

then within the time interval $[t_0, t_0+T]$, the buffer $B_e$ necessarily experiences at least one capacity overflow event.

**Proof Sketch**: Consider the worst case---the entire interval $[t_0, t_0+T]$ has $\gamma(e, t) = 0$ (fully offline). At this time $\lambda_{\text{out}}(t) = 0$, and the cumulative arrival is $\int_{t_0}^{t_0+T} \lambda_{\text{in}}(\tau) \, d\tau$. By the condition, this value exceeds $C_e$. According to the LRU replacement policy in Def-S-01-92, when $|Q_e| = C_e$, newly arrived messages trigger replacement, i.e., an "overflow" (in the generalized sense). If there are online periods within the interval, the conclusion still holds due to the net accumulation effect of $\lambda_{\text{in}} > \lambda_{\text{out}}$. $\square$

---

## 3. Relations

### 3.1 Edge-Cloud Computing Model Mapping

Edge stream processing and centralized stream processing have the following formal mapping relationships:

| Dimension | Centralized Stream Processing | Edge Stream Processing | Mapping Relation |
|-----------|------------------------------|------------------------|------------------|
| Compute Node | Cloud cluster $\mathcal{C}$ | Edge device $\mathcal{E}$ | $\mathcal{E} \prec \mathcal{C}$ (resource-constrained) |
| Connectivity Assumption | Always connected $\gamma \equiv 1$ | Intermittent connection Def-S-01-91 | $\gamma \in \{0, 1\}$ |
| State Storage | Distributed state backend | Local buffer Def-S-01-92 | $B_e \subset \mathcal{S}_{\text{global}}$ |
| Fault Tolerance Mechanism | Checkpoint to distributed storage | Local persistence + batch sync Def-S-01-93 | $\mathcal{P}_{\text{sync}}$ extends Checkpoint |
| Consistency Level | Exactly-Once / At-Least-Once | Edge eventual consistency | $\mathcal{C}_{\text{offline}} \leadsto \text{Eventual}$ |

### 3.2 Correspondence with the Actor Model

Edge node $e$ can be viewed as an Actor in the Actor model:

- **State**: Local buffer $B_e$ + operator state $\mathcal{S}_e$
- **Behavior**: Offline execution capability $\text{Cap}(e)$
- **Message**: Sensor data stream $m \in \mathcal{M}$
- **Mailbox**: Buffer queue $Q_e$

Edge-cloud interaction corresponds to message passing between Actors, while intermittent connection manifests as "messages being persisted to storage when the mailbox is full."

### 3.3 Integration with the Dataflow Model

Edge stream processing is a specialization of the Dataflow model in resource-constrained, intermittently connected environments:

$$
\text{Edge-Dataflow} = \text{Dataflow} \times \text{Intermittent}(\mathcal{E}) \times \text{LocalBuffer}(B_e)
$$

where $\text{Intermittent}(\mathcal{E})$ and $\text{LocalBuffer}(B_e)$ are defined by Def-S-01-91 and Def-S-01-92, respectively.

---

## 4. Argumentation

### 4.1 Necessity Argument for Edge Computing

**Scenario Assumption**: Industrial IoT scenario with $n=1000$ sensor nodes, each producing $1KB$ of data per second, with a cloud analytics latency requirement of $< 100ms$.

**Pure Cloud Solution**:

- Total bandwidth requirement: $1000 \times 1KB/s = 1MB/s$
- Network transmission latency (assuming 50ms RTT) + cloud processing latency (50ms) = 100ms (critical)
- Completely fails when disconnected

**Edge-Cloud Collaborative Solution**:

- Edge preprocessing (filtering, aggregation): data compression rate 90%
- Effective upload: $100KB/s$
- Local response latency: $< 10ms$ (no network required)
- Core functionality maintained when disconnected

**Conclusion**: In scenarios with limited bandwidth, latency sensitivity, and high reliability requirements, edge stream processing is not an "option" but a "must-have."

### 4.2 Batch Sync Strategy Trade-offs

| Strategy | Latency | Bandwidth Efficiency | Fault Tolerance | Applicable Scenario |
|----------|---------|---------------------|-----------------|---------------------|
| Per-message send | Lowest | Lowest | High (per-message ACK) | High-frequency control commands |
| Time window (Def-S-01-93) | Medium | Medium | Medium | General telemetry data |
| Capacity window (Def-S-01-93) | Variable | Highest | Low (batch loss risk) | Large-volume logs |
| Hybrid trigger (Def-S-01-93) | Adaptive | Adaptive | Medium | Complex industrial scenarios |

---

## 5. Proof / Engineering Argument

### 5.1 Edge Eventual Consistency Theorem

**Theorem Thm-S-01-09: Edge Eventual Consistency**

Let the edge-cloud stream processing system satisfy the following conditions:

1. All edge nodes $e \in \mathcal{E}$ satisfy Def-S-01-91 and $\text{Avail}(e) > 0$
2. Use the batch sync protocol Def-S-01-93 for edge-cloud data synchronization
3. Cloud state updates are monotonic: $s_c(t_1) \sqsubseteq s_c(t_2)$ for $t_1 < t_2$

Then the system satisfies **edge eventual consistency**:

$$
\forall e \in \mathcal{E}: \lim_{t \to \infty} \gamma(e, t) = 1 \Rightarrow \lim_{t \to \infty} s_c(t) = \bigsqcup_{e \in \mathcal{E}} s_e(t)
$$

That is: if an edge node eventually recovers persistent connection, the cloud state will converge to the union of all edge node states.

**Formal Proof**:

**Step 1**: Define edge node state evolution.

By Def-S-01-94, the state evolution equation of edge node $e$ is:

$$
s_e(t+1) = \begin{cases}
f_e(s_e(t), m_t) & \text{if } \gamma(e, t) = 0 \text{ (offline local processing)} \\
g_e(s_e(t), m_t, s_c(t)) & \text{if } \gamma(e, t) = 1 \text{ (online collaborative processing)}
\end{cases}
$$

where $f_e$ is the local operator function and $g_e$ is the collaborative operator function.

**Step 2**: Analyze the batch sync process.

Let $\tau_i$ be the time of the $i$-th successful synchronization. By Def-S-01-93, the sync process satisfies:

$$
\forall i: s_c(\tau_i^+) = s_c(\tau_i^-) \sqcup \Delta s_e(\tau_i)
$$

where $\Delta s_e(\tau_i) = s_e(\tau_i) - s_e(\tau_{i-1})$ is the state increment of the edge node during $[\tau_{i-1}, \tau_i]$.

**Step 3**: Prove monotonic convergence of the cloud state.

By condition 3, $s_c$ is monotonically increasing (in the lattice $\langle \mathcal{S}, \sqsubseteq \rangle$). By Step 2, each sync merges the edge increment into the cloud:

$$
s_c(t) = s_c(t_0) \sqcup \bigsqcup_{\tau_i \leq t} \Delta s_e(\tau_i)
$$

**Step 4**: Utilize the connection availability condition.

By condition 1 and the limit condition $\lim_{t \to \infty} \gamma(e, t) = 1$, there exists $T$ such that $\forall t > T: \gamma(e, t) = 1$.

This means:

- For $t > T$, the edge node no longer produces "unsyncable" state increments
- All state changes for $t > T$ will be synchronized to the cloud via $\mathcal{P}_{\text{sync}}$

**Step 5**: Convergence conclusion.

Consider any time $t > T$:

$$
\begin{aligned}
s_c(t) &= s_c(T) \sqcup \bigsqcup_{\tau_i \in (T, t]} \Delta s_e(\tau_i) \\
&= s_c(t_0) \sqcup \bigsqcup_{\tau_i \leq T} \Delta s_e(\tau_i) \sqcup \bigsqcup_{\tau_i \in (T, t]} \Delta s_e(\tau_i) \\
&= s_c(t_0) \sqcup \bigsqcup_{\tau_i \leq t} \Delta s_e(\tau_i)
\end{aligned}
$$

As $t \to \infty$, the right-hand side will include the accumulation of all edge state changes:

$$
\lim_{t \to \infty} s_c(t) = s_c(t_0) \sqcup \bigsqcup_{i=1}^{\infty} \Delta s_e(\tau_i) = \bigsqcup_{e \in \mathcal{E}} s_e(\infty)
$$

where $s_e(\infty) = \lim_{t \to \infty} s_e(t)$ (assuming edge state convergence).

**Conclusion**: Under the given conditions, the edge-cloud system satisfies eventual consistency. $\square$

### 5.2 Engineering Implementation Argument

**AWS IoT Greengrass Implementation Mapping**:

| Formal Concept | Greengrass Component |
|----------------|----------------------|
| Def-S-01-91 (Intermittent Connection) | `ConnectionManager` + offline shadow mechanism |
| Def-S-01-92 (Local Buffer) | `StreamManager` (local storage queue) |
| Def-S-01-93 (Batch Sync) | `ExportDefinition` (batch export configuration) |
| Def-S-01-94 (Offline Execution) | `Lambda` functions + `LocalShadow` |

**Azure IoT Edge Implementation Mapping**:

| Formal Concept | IoT Edge Component |
|----------------|--------------------|
| Def-S-01-91 (Intermittent Connection) | `IoT Edge Hub` connection state management |
| Def-S-01-92 (Local Buffer) | `Edge Hub` local message storage |
| Def-S-01-93 (Batch Sync) | `StoreAndForward` configuration (TTL + batch size) |
| Def-S-01-94 (Offline Execution) | `Edge Modules` + local routing |

---

## 6. Examples

### 6.1 Smart Factory Edge Stream Processing Example

**Scenario**: An automobile assembly line has 50 workstations, each equipped with sensors and an edge gateway.

```
Workstation Sensor → Edge Gateway (Local Preprocessing) → [Intermittent Connection] → Cloud Analytics Platform
               ↓
         Local Alert (Latency < 50ms)
         Local Dashboard
```

**Configuration Example (AWS IoT Greengrass)**:

```yaml
# Greengrass batch sync configuration
telemetry_config:
  batch_size: 100          # N_max = 100 messages
  batch_interval_ms: 5000  # T_max = 5 seconds
  max_payload_size: 128000 # S_max = 128KB

  # Intermittent connection handling
  offline_policy:
    local_storage_limit: "1GB"
    priority_queue: true
    eviction_policy: "LRU"
```

**Configuration Example (Azure IoT Edge)**:

```json
{
  "storeAndForwardConfiguration": {
    "timeToLiveSecs": 7200,
    "batchSize": 100,
    "maxConcurrentSends": 10
  },
  "routes": {
    "sensorToLocal": "FROM /messages/modules/sensor/* INTO $upstream",
    "localProcessing": "FROM /messages/modules/processor/* INTO BrokeredEndpoint('/modules/localStorage/inputs/input1')"
  }
}
```

### 6.2 Offline Execution State Consistency Verification

Assume edge node $e$ executes a sliding window count operator with window size $W = 60$ seconds.

**Online State** (synchronized with cloud):

```
t=0s:  count = 0
t=30s: count = 150 (cloud sync: 150)
t=60s: count = 300 (cloud sync: 300)
```

**Offline State** (disconnected at t=60s):

```
t=60s:  count = 300 (local state)
t=90s:  count = 450 (local update only)
t=120s: count = 600 (local update only, cloud still shows 300)
```

**Recovery Sync** (reconnected at t=150s):

```
Edge delta: Δ = 600 - 300 = 300
Cloud update: 300 + 300 = 600
Eventual consistency achieved ✓
```

---

## 7. Visualizations

### 7.1 Edge-Cloud Stream Processing Architecture Diagram

The following Mermaid diagram shows the hierarchical architecture of edge-cloud collaborative stream processing:

```mermaid
graph TB
    subgraph Cloud["☁️ Cloud Layer"]
        CA[Central Analytics<br/>Engine]
        CS[Cloud Storage<br/>Persistent Storage]
        CDB[(State Backend)]
        CM[Coordination Manager]
    end

    subgraph Network["🌐 Network Layer"]
        IC{{Intermittent Connection<br/>Def-S-01-91}}
    end

    subgraph Edge["🔷 Edge Layer"]
        subgraph EdgeNode1["Edge Node e₁"]
            LP1[Local Processing]
            LB1[(Local Buffer<br/>Def-S-01-92)]
            BSP1[Batch Sync Protocol<br/>Def-S-01-93]
            OE1[Offline Execution<br/>Def-S-01-94]
        end

        subgraph EdgeNode2["Edge Node e₂"]
            LP2[Local Processing]
            LB2[(Local Buffer)]
            BSP2[Batch Sync Protocol]
            OE2[Offline Execution]
        end

        subgraph EdgeNodeN["Edge Node eₙ"]
            LPn[Local Processing]
            LBn[(Local Buffer)]
            BSPn[Batch Sync Protocol]
            OEn[Offline Execution]
        end
    end

    subgraph Device["📟 Device Layer"]
        S1[Sensor 1]
        S2[Sensor 2]
        Sn[Sensor n]
    end

    %% Data flow
    S1 -->|Stream| LP1
    S2 -->|Stream| LP2
    Sn -->|Stream| LPn

    %% Edge internal flow
    LP1 --> LB1
    LP2 --> LB2
    LPn --> LBn

    LB1 --> BSP1
    LB2 --> BSP2
    LBn --> BSPn

    BSP1 -.->|Sync| OE1
    BSP2 -.->|Sync| OE2
    BSPn -.->|Sync| OEn

    %% Edge-cloud connection
    BSP1 -.->|Batch Upload| IC
    BSP2 -.->|Batch Upload| IC
    BSPn -.->|Batch Upload| IC

    IC -.->|When Connected| CA

    %% Cloud internal
    CA --> CS
    CA --> CDB
    CM --> CA

    %% Control flow
    CM -.->|Deploy Operators| OE1
    CM -.->|Deploy Operators| OE2
    CM -.->|Deploy Operators| OEn

    %% Styles
    style Cloud fill:#e1f5ff,stroke:#01579b,stroke-width:3px
    style Edge fill:#fff3e0,stroke:#e65100,stroke-width:3px
    style Device fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    style Network fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,stroke-dasharray: 5 5
    style IC fill:#ffebee,stroke:#b71c1c,stroke-width:2px
```

### 7.2 Batch Sync Protocol State Machine

```mermaid
stateDiagram-v2
    [*] --> IDLE

    IDLE --> COLLECT : conn_up / buffer
    COLLECT --> COLLECT : data_arrival
    COLLECT --> COMPRESS : trigger(W_batch)

    COMPRESS --> TRANSMIT : compressed
    COMPRESS --> IDLE : compress_fail / retry

    TRANSMIT --> ACK : data_sent
    TRANSMIT --> COLLECT : conn_down / requeue

    ACK --> IDLE : ack_recv
    ACK --> COLLECT : ack_timeout / retry

    note right of IDLE
        Waiting for data or connection recovery
        Def-S-01-93 initial state
    end note

    note right of COLLECT
        Accumulating batch data
        |Q_e| < N_max
        t - t_last < T_max
    end note

    note right of COMPRESS
        Compressing to reduce
        transmission overhead
    end note

    note right of TRANSMIT
        Batch upload via intermittent connection
        Def-S-01-91
    end note

    note right of ACK
        Waiting for cloud acknowledgment
        Ensuring reliable transmission
    end note
```

### 7.3 Offline Execution Capability Hierarchy Diagram

```mermaid
graph TD
    A[Offline Execution Capability Hierarchy<br/>Def-S-01-94] --> B[Level 3: Complex Analytics]
    A --> C[Level 2: Aggregation Computing]
    A --> D[Level 1: Simple Filtering]

    B --> B1[Sliding Window Aggregation]
    B --> B2[Pattern Matching]
    B --> B3[Anomaly Detection ML]

    C --> C1[Group Statistics]
    C --> C2[Time Window Counting]
    C --> C3[Deduplication]

    D --> D1[Threshold Filtering]
    D --> D2[Field Projection]
    D --> D3[Format Conversion]

    B1 -.->|Requires| E[(Local State Storage)]
    B2 -.->|Requires| E
    C1 -.->|Requires| E
    C2 -.->|Requires| E

    style A fill:#e3f2fd,stroke:#1565c0,stroke-width:3px
    style E fill:#fff8e1,stroke:#ff6f00,stroke-width:2px
```

---

## 8. References

[^1]: Apache Flink Documentation, "Checkpointing", 2025. https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/checkpointing/
[^2]: T. Akidau et al., "The Dataflow Model", PVLDB, 8(12), 2015.
[^3]: L. Lamport, "Time, Clocks, and the Ordering of Events in a Distributed System", CACM, 21(7), 1978.

---

*Document version: v1.0 | Translation date: 2026-04-24*
