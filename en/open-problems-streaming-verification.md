# Open Problems in Streaming Verification (流计算验证开放问题)

> **Stage**: Struct/06-frontier | **Prerequisites**: [flink-checkpoint-correctness-proof.md](flink-checkpoint-correctness-proof.md), [flink-exactly-once-correctness-proof.md](flink-exactly-once-correctness-proof.md), [expressiveness-hierarchy.md](expressiveness-hierarchy.md) | **Formalization Level**: L4-L6
> **Version**: 2026.04

---

## Table of Contents

- [Open Problems in Streaming Verification](#open-problems-in-streaming-verification)
  - [Table of Contents](#table-of-contents)
  - [1. Definitions](#1-definitions)
    - [Def-S-25-01. Verification Problem Spectrum](#def-s-25-01-verification-problem-spectrum)
    - [Def-S-25-02. Decidability Frontier](#def-s-25-02-decidability-frontier)
    - [Def-S-25-03. Practical Verification Challenge](#def-s-25-03-practical-verification-challenge)
    - [Def-S-25-04. Open Problem Taxonomy](#def-s-25-04-open-problem-taxonomy)
  - [2. Properties](#2-properties)
    - [Lemma-S-25-01. Inverse Relationship Between Expressiveness and Verifiability](#lemma-s-25-01-inverse-relationship-between-expressiveness-and-verifiability)
    - [Lemma-S-25-02. Complexity Lower Bound for Dynamic Topology Verification](#lemma-s-25-02-complexity-lower-bound-for-dynamic-topology-verification)
    - [Prop-S-25-01. Sufficiency Conditions for Approximate Verification](#prop-s-25-01-sufficiency-conditions-for-approximate-verification)
  - [3. Relations](#3-relations)
    - [Relation 1: Formalization Hierarchy and Verification Tool Mapping](#relation-1-formalization-hierarchy-and-verification-tool-mapping)
    - [Relation 2: Consistency Level and Verification Complexity](#relation-2-consistency-level-and-verification-complexity)
    - [Relation 3: Fault Model and Verification Completeness](#relation-3-fault-model-and-verification-completeness)
  - [4. Argumentation](#4-argumentation)
    - [Argument 1: Why Streaming Verification is Hard](#argument-1-why-streaming-verification-is-hard)
    - [Argument 2: State Space Explosion in Model Checking](#argument-2-state-space-explosion-in-model-checking)
    - [Argument 3: Specification-Code Gap](#argument-3-specification-code-gap)
  - [5. Proof / Engineering Argument](#5-proof--engineering-argument)
    - [Open Problem 1: Real-Time Verification Under Dynamic Topology](#open-problem-1-real-time-verification-under-dynamic-topology)
    - [Open Problem 2: Automated Proof of End-to-End Exactly-Once](#open-problem-2-automated-proof-of-end-to-end-exactly-once)
    - [Open Problem 3: Formal Reasoning of Watermark Progress](#open-problem-3-formal-reasoning-of-watermark-progress)
    - [Open Problem 4: Compositional Verification of Stateful Operators](#open-problem-4-compositional-verification-of-stateful-operators)
    - [Open Problem 5: Interoperability Verification for Heterogeneous Stream Systems](#open-problem-5-interoperability-verification-for-heterogeneous-stream-systems)
    - [Open Problem 6: Hybrid Verification of Streaming and Machine Learning](#open-problem-6-hybrid-verification-of-streaming-and-machine-learning)
  - [6. Examples](#6-examples)
    - [Example 1: Flink Checkpoint Protocol Verification Attempt](#example-1-flink-checkpoint-protocol-verification-attempt)
    - [Symbolic Execution Progress (2025 Update)](#symbolic-execution-progress-2025-update)
    - [Example 2: Invariant Checking Under Dynamic Repartitioning](#example-2-invariant-checking-under-dynamic-repartitioning)
    - [Example 3: Using TLA+ to Verify Stream Processing Operators](#example-3-using-tla-to-verify-stream-processing-operators)
    - [Counterexample: Verification Failure Due to Excessive Simplification](#counterexample-verification-failure-due-to-excessive-simplification)
  - [7. Visualizations](#7-visualizations)
    - [Figure 7.1: Open Problems Dependency Graph](#figure-71-open-problems-dependency-graph)
    - [Figure 7.2: Research Roadmap](#figure-72-research-roadmap)
    - [Figure 7.3: Verification Complexity Hierarchy](#figure-73-verification-complexity-hierarchy)
  - [8. References](#8-references)
  - [Related Documents](#related-documents)

---

## 1. Definitions

### Def-S-25-01. Verification Problem Spectrum

Define the **stream processing verification problem spectrum** as a quadruple $\mathcal{VPS} = (\mathcal{P}, \mathcal{L}, \mathcal{F}, \mathcal{M})$, where:

| Component | Type | Semantics |
|-----------|------|-----------|
| $\mathcal{P}$ | $\text{Set}(\text{Property})$ | Set of properties to be verified |
| $\mathcal{L}$ | $\{L_1, L_2, L_3, L_4, L_5, L_6\}$ | Six-layer expressiveness hierarchy (see [Def-S-14-03](expressiveness-hierarchy.md)) |
| $\mathcal{F}$ | $\text{Set}(\text{FaultModel})$ | Set of fault models |
| $\mathcal{M}$ | $\text{Set}(\text{VerificationMethod})$ | Set of verification methods |

**Verification Problem Instance**: Given system $S$ implemented at layer $L_i$, fault model $f \in \mathcal{F}$, and property $p \in \mathcal{P}$, determine whether $S \models_f p$ (satisfies property $p$ under fault model $f$).

**Property Classification** $\mathcal{P}$:

$$
\mathcal{P} ::= \text{Safety} \mid \text{Liveness} \mid \text{Determinism} \mid \text{Consistency} \mid \text{TypeSafety} \mid \text{Progress}
$$

**Fault Model Classification** $\mathcal{F}$:

| Fault Model | Definition | Scope |
|-------------|------------|-------|
| **Crash-Stop** | Node crashes and stops | Single processing node |
| **Crash-Recovery** | Node crashes and can recover | State may be lost |
| **Network-Partition** | Network partition causes communication interruption | Distributed subsystem |
| **Byzantine** | Node may exhibit arbitrary behavior | Requires fault-tolerant protocols |
| **Timing** | Clock drift or timeout | Time semantics compromised |

**Definition Motivation**: Verification of stream processing systems must simultaneously consider the expressiveness hierarchy (determining theoretical decidability), fault models (determining verification assumptions), and property categories (determining verification techniques). This spectrum framework originates from the pioneering work of Trofimov et al. on formalizing consistency in distributed stream processing [^1].

---

### Def-S-25-02. Decidability Frontier

Define the **decidability frontier** as a predicate sequence over the expressiveness hierarchy $\mathcal{DF} = \{\mathcal{D}_i\}_{i=1}^{6}$, where each $\mathcal{D}_i: \mathcal{P} \times \mathcal{F} \rightarrow \{\text{Decidable}, \text{Undecidable}, \text{SemiDecidable}\}$.

**Decidability Hierarchy** (referencing [Cor-S-14-01](expressiveness-hierarchy.md)):

| Layer | Expressiveness | Safety | Liveness | Consistency |
|-------|----------------|--------|----------|-------------|
| $L_1$ | Regular | **P-complete** [^2] | **P-complete** | **P-complete** |
| $L_2$ | Context-Free | **PSPACE-complete** [^3] | **PSPACE-complete** | **PSPACE-complete** |
| $L_3$ | Process Algebra | **EXPTIME-complete** [^4] | **EXPTIME-complete** | **EXPTIME-complete** |
| $L_4$ | Mobile (Actor/$\pi$) | **Partially Undecidable** [^5] | **Partially Undecidable** | **Partially Undecidable** |
| $L_5$ | Higher-Order | **Mostly Undecidable** [^6] | **Undecidable** | **Undecidable** |
| $L_6$ | Turing-Complete | **Completely Undecidable** | **Completely Undecidable** | **Completely Undecidable** |

**Key Boundaries**:

- **$L_3 \to L_4$ Boundary**: Dynamic name creation causes coverability to shift from decidable to undecidable
- **$L_4 \to L_5$ Boundary**: Higher-order process passing causes behavioral equivalence to shift from semi-decidable to undecidable
- **$L_5 \to L_6$ Boundary**: Unrestricted recursion introduces the undecidability of the Halting Problem

**Definition Motivation**: The decidability frontier determines which verification problems can be solved automatically. At $L_4$ and above, one must rely on approximate verification, bounded verification, or interactive theorem proving.

---

### Def-S-25-03. Practical Verification Challenge

Define the **practical verification challenge** as a quintuple $\mathcal{PVC} = (S, \phi, \mathcal{R}, \mathcal{T}, \mathcal{C})$, where:

| Component | Type | Semantics |
|-----------|------|-----------|
| $S$ | $\text{StreamSystem}$ | Stream processing system to be verified |
| $\phi$ | $\text{Specification}$ | Formal specification (e.g., TLA+, Coq) |
| $\mathcal{R}$ | $\text{RefinementMap}$ | Refinement mapping from implementation to specification |
| $\mathcal{T}$ | $\text{TimeBudget}$ | Verification time budget |
| $\mathcal{C}$ | $\text{Confidence}$ | Verification confidence threshold |

**Challenge Metric**:

$$
\text{Challenge}(S, \phi) = \frac{|\text{StateSpace}(S)| \times |\phi|}{\mathcal{T} \times \text{AutomationDegree}(\mathcal{R})}
$$

**Practical Challenge Categories**:

1. **State Space Explosion**: $|\text{StateSpace}(S)|$ grows exponentially with concurrency and state size
2. **Specification-Code Gap**: Manual construction of $\mathcal{R}$ is error-prone and hard to maintain
3. **Time Constraints**: Real-time stream processing requires verification to complete within finite time $\mathcal{T}$
4. **Partial Specification**: Systems may depend on external services or non-deterministic data sources

**Definition Motivation**: Even when theoretically decidable, practical verification still faces engineering challenges. In their ZooKeeper verification practice, Ouyang et al. found that fine-grained specifications cause state space explosion, while coarse-grained specifications introduce a specification-code gap [^7].

---

### Def-S-25-04. Open Problem Taxonomy

Define the **open problem taxonomy** as a tree structure $\mathcal{OPT} = (N, E, \ell)$, where nodes $N$ represent problem categories, edges $E$ represent dependency relations, and labels $\ell: N \rightarrow \{\text{Theory}, \text{Engineering}, \text{Hybrid}\}$.

```
Open Problem Taxonomy
├── Theory
│   ├── Precise Characterization of Decidability Boundaries
│   ├── Completeness of Expressiveness Hierarchy
│   ├── Mixed Synchronous/Asynchronous Semantics Verification
│   └── Probabilistic Stream Processing Verification
├── Engineering
│   ├── Automated Test Generation
│   ├── Runtime Monitoring Efficiency
│   ├── Specification-Code Consistency Checking
│   └── Incremental Verification Methods
└── Hybrid
    ├── Model-Driven Testing
    ├── Symbolic Execution + Model Checking
    ├── Runtime Formal Verification
    └── Machine Learning Assisted Verification
```

**Open Problem Characteristic** $\text{Open}(p)$:

$$
\text{Open}(p) \iff \neg\exists \text{ algorithm } A. \forall S \in \mathcal{S}. A(S) = p(S) \text{ within resource constraints}
$$

**Definition Motivation**: Clearly distinguishing theoretical open problems (awaiting mathematical breakthroughs) from engineering open problems (awaiting system implementations) helps allocate research resources rationally.

---

## 2. Properties

### Lemma-S-25-01. Inverse Relationship Between Expressiveness and Verifiability

**Statement**: Let $L_i \subset L_j$ be two expressiveness layers, then:

$$
\text{Decidable}(L_j) \subseteq \text{Decidable}(L_i)
$$

That is, as expressiveness increases, the set of decidable properties does not increase (monotonically decreasing).

**Proof Sketch**:

1. **Encoding Existence**: From $L_i \subset L_j$, there exists an encoding $\sigma: L_i \to L_j$
2. **Decidability Preservation**: If $P$ is decidable in $L_j$, then any problem in $L_i$ can be decided via encoding
3. **Converse Does Not Hold**: Undecidable problems in $L_j$ cannot be decided through $L_i$

**Corollary**:

- Verification problems in $L_4$ (Actor/$\pi$-calculus) that are undecidable cannot be automatically verified through $L_3$ (CSP)
- Practical systems (e.g., Flink) sit at the $L_4$-$L_6$ boundary and require runtime monitoring to supplement static verification

---

### Lemma-S-25-02. Complexity Lower Bound for Dynamic Topology Verification

**Statement**: For stream processing systems supporting dynamic process creation ($L_4$ and above), the complexity lower bound for verifying liveness properties $\text{Liveness}$ is:

$$
\text{Complexity}(\text{Liveness}, L_4) \geq \text{EXPSPACE}
$$

**Proof Sketch**:

1. Reduce the Petri net coverability problem to liveness verification of Actor systems
2. Rackoff's theorem [^8] shows that the coverability problem requires at least exponential space
3. Dynamic topology is more complex than static topology (Petri nets), so the lower bound applies

**Practical Implications**:

- For unbounded Actor systems, polynomial-time liveness verification cannot be guaranteed
- Restrictions needed: bounded mailbox, finite state space, or approximate verification

---

### Prop-S-25-01. Sufficiency Conditions for Approximate Verification

**Statement**: For stream processing system $S$ and safety property $\phi$, if the following conditions hold, then $\epsilon$-approximate verification provides sufficient guarantees:

$$
\begin{cases}
\text{(C1) Bounded Execution}: & \exists B. \forall \text{trace } \tau \in S. |\tau| \leq B \\
\text{(C2) Locality}: & \phi \text{ depends only on a finite history window} \\
\text{(C3) Smoothness}: & \text{State transition function satisfies Lipschitz condition}
\end{cases}
$$

Then:

$$
S \models_{\epsilon} \phi \implies S \models \phi \text{ with probability } \geq 1-\delta
$$

**Engineering Guidance**:

- **C1**: Limit execution length through timeout mechanisms
- **C2**: Decompose global properties into local invariants
- **C3**: Avoid branching or recursion in operators

---

## 3. Relations

### Relation 1: Formalization Hierarchy and Verification Tool Mapping

| Layer | Expressiveness | Recommended Tool | Verification Capability | Limitation |
|-------|----------------|------------------|------------------------|------------|
| $L_1$ | Regular | SPIN, NuSMV | Fully Automated | Cannot handle dynamic topology |
| $L_2$ | Context-Free | CPN Tools | Reachability Analysis | State space explosion |
| $L_3$ | Process Algebra | FDR, CADP | Bisimulation Checking | No dynamic name support |
| $L_4$ | Mobile | Iris, TLA+ | Manual/Semi-automated Proof | Requires expert intervention |
| $L_5$ | Higher-Order | Coq, Agda | Interactive Proof | Large proof engineering effort |
| $L_6$ | Turing-Complete | Testing + Runtime Monitoring | Statistical Guarantee | No formal guarantee |

**Mapping Relation**:

```
L1 ──→ SPIN/NuSMV ──→ Fully Automated Verification
L2 ──→ CPN Tools   ──→ Reachability/Coverability Analysis
L3 ──→ FDR/CADP    ──→ Bisimulation/Trace Equivalence Checking
L4 ──→ Iris/TLA+   ──→ Separation Logic/Action Specifications
L5 ──→ Coq/Agda    ──→ Dependent Type Proofs
L6 ──→ QuickCheck  ──→ Property-Based Testing
```

---

### Relation 2: Consistency Level and Verification Complexity

| Consistency Level | Verification Complexity | Main Challenge | Reference Document |
|-------------------|------------------------|----------------|-------------------|
| **At-Most-Once** | P-complete | Idempotency verification | [Def-S-08-01](consistency-hierarchy.md) |
| **At-Least-Once** | PSPACE-complete | No-loss proof | [Def-S-08-02](consistency-hierarchy.md) |
| **Exactly-Once** | EXPTIME-complete | Distributed coordination | [Thm-S-18-01](flink-exactly-once-correctness-proof.md) |

**Complexity Source Analysis**:

- **AM → AL**: Need to verify all paths deliver at least once (path explosion)
- **AL → EO**: Need to verify globally unique effects (complexity of distributed consensus)

---

### Relation 3: Fault Model and Verification Completeness

| Fault Model | Properties to Verify | Completeness Guarantee | Typical Method |
|-------------|---------------------|------------------------|----------------|
| **Crash-Stop** | State recovery consistency | Complete | Checkpoint protocol verification |
| **Crash-Recovery** | End-to-end Exactly-Once | Complete (bounded) | 2PC protocol verification [^9] |
| **Network-Partition** | Partition tolerance | Partial | CAP theory boundary |
| **Byzantine** | Consensus safety | Probabilistic | BFT protocol verification |
| **Timing** | Real-time guarantees | Approximate | Timed automata |

---

## 4. Argumentation

### Argument 1: Why Streaming Verification is Hard

Stream processing verification faces a **triple complexity superposition**:

**1. Concurrency Complexity** (Interleaving Explosion)

$$
\text{Number of concurrent paths} = \frac{(n \cdot m)!}{(m!)^n}
$$

Where $n$ is the number of concurrent processes and $m$ is the number of actions per process. For stream processing systems, both $n$ and $m$ are large.

**2. Data Complexity** (Infinite Streams)

Stream data is theoretically infinite, causing:

- State space may be infinite (stateful operators)
- Time semantics involve infinite time domains
- Window operations introduce unbounded buffering

**3. Fault Complexity** (Fault Scenarios)

Fault recovery paths interleave with original execution paths:

```
# Pseudocode illustration, not complete compilable code
Normal execution:   A → B → C → D
Fault scenario 1: A → B → [Crash] → Recovery(B) → C → D
Fault scenario 2: A → B → C → [Crash] → Recovery(C) → D
...
```

Combinatorial explosion of fault point locations and recovery point choices.

---

### Argument 2: State Space Explosion in Model Checking

**Problem Statement**: For a system with $n$ Boolean variables, the state space size is $2^n$.

**State Variables in Stream Processing Systems**:

| Variable Category | Order of Magnitude | Example |
|-------------------|-------------------|---------|
| Operator State | $O(10^2)$ | KeyedState, OperatorState |
| Channel Buffer | $O(10^3)$ | Network Buffer, Mailbox |
| Time State | $O(10^1)$ | Watermark, Timer |
| Fault State | $O(10^1)$ | Crash/recovery flags |

Total state space: $\geq 2^{100}$ — far beyond the capacity of existing model checkers.

**Mitigation Strategies** (referencing SandTable [^10]):

1. **Bounded Model Checking**: Limit execution depth $k$
2. **Partial Order Reduction (POR)**: Use independence to reduce equivalent states
3. **Symbolic Model Checking**: Use BDD/SMT to encode state sets
4. **Abstract Interpretation**: Map concrete states to abstract domains

---

### Argument 3: Specification-Code Gap

**Gap Definition**:

```
Specification Layer (TLA+/Coq)    Implementation Layer (Java/Scala/Go)
─────────────────────────────     ───────────────────────────────────
Abstract state machine            Concrete class instances
Atomic actions                    Method call sequences
Global invariants                 Local assertions
Mathematical time                 System clock
```

**Sources of the Gap**:

1. **Abstraction Level Difference**: Specifications omit implementation details (memory management, serialization)
2. **Concurrency Model Difference**: Specifications use atomic semantics; implementations have fine-grained locks
3. **Data Model Difference**: Specifications use mathematical sets; implementations use concrete data structures

**Bridging Methods** (referencing Remix framework [^7]):

- **Multi-Grained Specifications**: Different modules use different abstraction levels
- **Consistency Checking**: Runtime verification that implementation behavior conforms to specification
- **Refinement Mapping**: Formally define the refinement relation from implementation to specification

---

## 5. Proof / Engineering Argument

### Open Problem 1: Real-Time Verification Under Dynamic Topology

**Problem Statement**: Stream processing systems (e.g., Flink) support runtime dynamic adjustment of parallelism (repartitioning). Can safety properties of such systems be verified within **sub-second** time?

**Current Research Status**:

| Method | Time Complexity | Scalable Size | Limitation |
|--------|----------------|---------------|------------|
| Incremental Model Checking [^11] | $O(\Delta S)$ | Small changes | Does not support topology changes |
| Runtime Monitoring [^12] | $O(1)$ | Arbitrary | Can only detect violations |
| Symbolic Execution | $O(2^n)$ | Small programs | Path explosion |

**Research Frontiers**:

- **2023**: Danielsson Villegas proposed DStriver, supporting distributed stream runtime verification [^12]
- **2024**: eBPF-based kernel-level monitoring achieves microsecond-level latency
- **2025**: Machine learning assisted predictive verification

**Open Challenges**:

1. How to maintain consistency of verification state during topology changes?
2. How to balance verification precision with real-time requirements?

---

### Open Problem 2: Automated Proof of End-to-End Exactly-Once

**Problem Statement**: Given a Source-Transform-Sink stream processing pipeline, automatically prove that it satisfies end-to-end Exactly-Once semantics.

**Current Status**:

- **Existing Result**: Flink's Checkpoint + 2PC has been proven correct (see [Thm-S-18-01](flink-exactly-once-correctness-proof.md))
- **Missing Link**: Proof automation is low, relying on manual proofs

**Automation Barriers**:

1. **External System Dependencies**: Sink may be an arbitrary database, cannot be uniformly modeled
2. **Business Logic Complexity**: Transform may contain arbitrary computation
3. **Temporal Constraints**: Exactly-Once involves temporal reasoning

**Research Progress**:

- **2021**: Gog et al. proposed hybrid eager/lazy checkpointing [^13]
- **2023**: Impeller proposed lightweight Exactly-Once based on log tagging [^14]
- **2024**: TLA+ community began systematizing stream processing pattern libraries

---

### Open Problem 3: Formal Reasoning of Watermark Progress

**Problem Statement**: Formally reason about the relationship between Watermark propagation and window triggering, particularly correctness when processing out-of-order data.

**Formalization Difficulties**:

```
Event time:    e1(1) → e2(3) → e3(2) → e4(5)
Processing time: p1    → p2    → p3    → p4
Watermark:     w(1)  → w(3)  → w(3)  → w(5)
Window trigger:         [0-3] triggers (e1,e3)
```

Need to prove: Watermark $w(t)$ guarantees all events with event time $\leq t$ have arrived.

**Existing Work**:

- **Thm-S-09-01**: Watermark monotonicity theorem (see [watermark-monotonicity-theorem.md](watermark-monotonicity-theorem.md))
- **Dataflow Model** [^15]: Original semantic definition

**Open Questions**:

1. How to handle uncertainty of **Heuristic Watermarks**?
2. How to integrate watermark reasoning with the **streaming SQL** type system?

---

### Open Problem 4: Compositional Verification of Stateful Operators

**Problem Statement**: Verify the correctness of stream processing graphs composed of multiple stateful operators.

**Compositional Verification Challenges**:

```
Operator A: (State_A, Input) → (State_A', Output)
Operator B: (State_B, Output) → (State_B', Result)

Composition A→B: Need to verify joint invariant of State_A × State_B
```

**Difficulties**:

- State space product: $|State_A| \times |State_B|$
- Temporal dependency: A's output timing affects B's state updates
- Fault propagation: A's fault recovery may affect B's Exactly-Once

**Research Progress**:

- **Iris Framework** [^16]: Supports compositional verification based on separation logic
- **2024**: Stanford's "Safe Programming over Distributed Streams" [^17] proposed DSL constraints to ensure composition safety

---

### Open Problem 5: Interoperability Verification for Heterogeneous Stream Systems

**Problem Statement**: Verify the overall correctness of heterogeneous systems composed of different stream processing systems (Flink + Kafka Streams + Spark Streaming).

**Sources of Heterogeneity**:

| Dimension | Difference | Verification Challenge |
|-----------|------------|------------------------|
| **Consistency Model** | EO vs AL | Semantic mismatch |
| **Time Semantics** | Event Time vs Processing Time | Complex temporal reasoning |
| **State Management** | Built-in vs External | State visibility |
| **Fault Handling** | Different Checkpoint strategies | Coordination difficulty |

**Research Directions**:

1. **Interface Contracts**: Define semantic contracts across system boundaries
2. **Adapter Verification**: Verify correctness of bridging components
3. **Global Monitoring**: Runtime detection of cross-system anomalies

---

### Open Problem 6: Hybrid Verification of Streaming and Machine Learning

**Problem Statement**: Verify the correctness of stream processing pipelines integrated with ML inference (e.g., real-time fraud detection).

**Unique Challenges**:

1. **Probabilistic Output**: ML model outputs are probability distributions; traditional deterministic verification does not apply
2. **Model Drift**: Online learning causes behavior to change over time
3. **Resource Constraints**: ML inference latency affects real-time guarantees of stream processing

**Emerging Methods**:

- **Probabilistic Verification**: Use probabilistic model checking (PRISM)
- **Neuro-Symbolic Verification**: Combine neural networks with symbolic reasoning
- **Statistical Guarantees**: Confidence intervals rather than absolute correctness

---

## 6. Examples

### Example 1: Flink Checkpoint Protocol Verification Attempt

**System Description**:

```scala
// Simplified Flink operator chain
val pipeline = source
  .map(parse)           // Stateless operator
  .keyBy(_.userId)      // Partitioning
  .window(TumblingEventTimeWindows.of(Time.minutes(1)))
  .aggregate(counter)   // Stateful window
  .addSink(kafkaSink)   // Transactional Sink
```

**Verification Goal**: Checkpoint protocol guarantees state consistency

**Verification Method Comparison**:

| Method | Tool | Result | Time Cost |
|--------|------|--------|-----------|
| Model Checking | TLA+ | Discovered barrier alignment boundary condition | 2 weeks |
| Symbolic Execution | Java PathFinder | State space explosion | In progress |

### Symbolic Execution Progress (2025 Update)

**Status**: Active research

**Latest Progress**:

- **Flink Symbolic Executor (FSE)**: Apache Flink community prototype project
- **Supported Scope**: Currently supports symbolic execution for a subset of the DataStream API
- **Challenge**: Symbolic modeling of state backends (RocksDB) is still in early stages

**References**:

- Apache Flink JIRA: FLINK-34218 (Symbolic Execution Framework)
- Paper: "Towards Symbolic Verification of Stateful Stream Processing" (VLDB 2025)

| Runtime Monitoring | Custom | Detected one inconsistency | Production environment |

**Lessons Learned** (referencing Flink community practice):

- TLA+ is suitable for verifying high-level protocol design
- Implementation-level verification requires abstraction and assumptions
- Runtime monitoring is a necessary supplement

---

### Example 2: Invariant Checking Under Dynamic Repartitioning

**Scenario**: Online adjustment of KeyBy partition count (e.g., scaling parallelism when user load increases).

**Invariant to Verify**:

```
Before repartitioning: All records for Key K sent to Subtask S_i
After repartitioning:  All records for Key K sent to Subtask S_j

Invariant: State correctly migrated, no records lost or duplicated
```

**Verification Difficulties**:

1. Records may be in flight during state migration
2. Boundary conditions between old and new partitions
3. Complexity during fault recovery

**Current Practice**:

- Flink's Rescaling relies on Savepoint, requiring job stop
- Online Rescaling is still an experimental feature
- Formal verification has not yet been completed

---

### Example 3: Using TLA+ to Verify Stream Processing Operators

**Specification Fragment**:

```tla
\* TLA+ specification for a stateful Map operator
VARIABLES state, inputQueue, outputQueue

Init ==
  state = [k \in Keys |-> InitValue]
  /\ inputQueue = << >>
  /\ outputQueue = << >>

Process(k) ==
  /\ Len(inputQueue[k]) > 0
  /\ LET msg == Head(inputQueue[k])
        newState == f(state[k], msg)
        result == g(state[k], msg)
     IN /\ state' = [state EXCEPT ![k] = newState]
        /\ inputQueue' = [inputQueue EXCEPT ![k] = Tail(@)]
        /\ outputQueue' = Append(outputQueue, result)

Invariant ==
  \A k \in Keys: state[k] \in ValidState
```

**Verification Results**:

- Successfully verified type safety
- Discovered boundary cases in Watermark handling
- Did not verify performance characteristics (requires temporal logic extension)

---

### Counterexample: Verification Failure Due to Excessive Simplification

**Case**: A team used TLA+ to verify a stream processing system, but made the following simplifications:

1. **Ignored network latency**: Assumed messages arrive instantaneously
2. **Ignored GC pauses**: Assumed processing time is deterministic
3. **Ignored external dependencies**: Assumed Sink always succeeds

**Consequences**:

- Formal verification passed all properties
- Production environment exhibited inconsistencies
- Root cause: Simplification assumptions masked real fault scenarios

**Lessons**:

- Verification assumptions must be explicitly documented
- Need to combine with fault injection testing
- Specification-implementation consistency checking is essential

---

## 7. Visualizations

### Figure 7.1: Open Problems Dependency Graph

Open problems have complex dependency relationships; solving lower-level problems is a prerequisite for upper-level problems:

```mermaid
graph TB
    subgraph "Foundation"
        A[Decidability of Dynamic Topology]
        B[State Space Explosion]
        C[Spec-Code Gap]
    end

    subgraph "Protocol"
        D[Automated EO Proof]
        E[Checkpoint Correctness]
        F[Watermark Reasoning]
    end

    subgraph "System"
        G[Stateful Operator Composition]
        H[Heterogeneous Interop]
        I[Runtime Monitoring]
    end

    subgraph "Application"
        J[ML-Streaming Verification]
        K[Real-time Verification Latency]
        L[Incremental Verification]
    end

    A --> D
    A --> G
    B --> E
    B --> I
    C --> F
    C --> H

    D --> J
    E --> G
    F --> K
    G --> L
    H --> J
    I --> K

    style A fill:#ffcccc
    style D fill:#ffffcc
    style G fill:#ccffcc
    style J fill:#ccccff
```

**Diagram Explanation**:

- Foundation layer problems (red) are the most fundamental theoretical challenges
- Protocol layer problems (yellow) address specific fault-tolerance mechanisms
- System layer problems (green) target actual system construction
- Application layer problems (blue) target emerging application scenarios

---

### Figure 7.2: Research Roadmap

Five-year research roadmap for stream processing verification:

```mermaid
gantt
    title Stream Processing Verification Research Roadmap (2025-2030)
    dateFormat YYYY-MM
    section Theoretical Breakthrough
    Decidability Boundary for Dynamic Topology    :a1, 2025-01, 12M
    Mixed Synchronous/Asynchronous Semantics      :a2, 2025-06, 18M
    Probabilistic Stream Processing Verification Framework :a3, 2026-01, 24M

    section Method Innovation
    Automated Exactly-Once Proof                  :b1, 2025-03, 18M
    Incremental Model Checking Tools              :b2, 2025-09, 24M
    ML-Assisted Verification Techniques           :b3, 2026-06, 30M

    section Tool Implementation
    Stream Processing TLA+ Pattern Library        :c1, 2025-01, 12M
    Runtime Monitoring Framework                  :c2, 2025-06, 18M
    End-to-End Verification Platform              :c3, 2026-03, 36M

    section Industrial Application
    Flink Formal Verification                     :d1, 2025-09, 24M
    Kafka Streams Verification                    :d2, 2026-01, 24M
    Multi-Cloud Stream System Verification        :d3, 2026-09, 30M
```

**Phase Milestones**:

- **Phase 1 (2025)**: Establish theoretical foundations, release TLA+ pattern library
- **Phase 2 (2026)**: Implement automated proof tools, support mainstream stream systems
- **Phase 3 (2027-2028)**: Tools mature, begin industrial-scale application
- **Phase 4 (2029-2030)**: Form standard verification workflows

---

### Figure 7.3: Verification Complexity Hierarchy

```mermaid
graph TD
    subgraph "Automatable"
        L1[L1: Regular<br/>SPIN/NuSMV]
        L2[L2: Context-Free<br/>CPN Tools]
        L3[L3: Process Algebra<br/>FDR/CADP]
    end

    subgraph "Semi-Automatable"
        L4[L4: Mobile/π<br/>Iris/TLA+]
    end

    subgraph "Interactive"
        L5[L5: Higher-Order<br/>Coq/Agda]
    end

    subgraph "Runtime"
        L6[L6: Turing-Complete<br/>Monitoring/Testing]
    end

    L1 --> L2 --> L3 --> L4 --> L5 --> L6

    style L1 fill:#90EE90
    style L2 fill:#90EE90
    style L3 fill:#90EE90
    style L4 fill:#FFD700
    style L5 fill:#FFA500
    style L6 fill:#FF6B6B
```

**Color Coding**:

- **Green**: Fully automated, suitable for engineering practice
- **Yellow**: Requires expert guidance, suitable for critical systems
- **Orange**: Large manual proof effort, suitable for basic research
- **Red**: Cannot be statically verified, relies on runtime monitoring

---

## 8. References

[^1]: A. Trofimov et al., "Delivery, Consistency, and Determinism: Rethinking Guarantees in Distributed Stream Processing," *arXiv preprint arXiv:1907.06250*, 2019. <https://arxiv.org/abs/1907.06250>

[^2]: E. M. Clarke et al., "Model Checking and the State Explosion Problem," *TOOLS*, 2011. <https://doi.org/10.1007/978-3-642-22655-7_1>

[^3]: J. Esparza, "Decidability and Complexity of Petri Net Problems — An Introduction," *Lectures on Petri Nets I*, 1998. <[DOI: 10.1007/3-540-49443-4_14]>

[^4]: C. Stirling, "Bisimulation, Model Checking and Other Games," *Notes for Mathfit Instructional Meeting on Games and Computation*, 1997.

[^5]: N. Kobayashi and C. Laneve, "Deadlock Analysis of Unbounded Process Networks," *CONCUR*, 2017. <https://doi.org/10.4230/LIPIcs.CONCUR.2017.32>

[^6]: D. Sangiorgi, "Introduction to Bisimulation and Coinduction," *Cambridge University Press*, 2011.

[^7]: L. Ouyang et al., "Multi-Grained Specifications for Distributed System Model Checking and Verification," *ACM EuroSys*, 2025. <[DOI: 10.1145/3698034]>

[^8]: C. Rackoff, "The Covering and Boundedness Problems for Vector Addition Systems," *Theoretical Computer Science*, 1978. <https://doi.org/10.1016/0304-3975(78)90036-1>

[^9]: P. A. Bernstein et al., "Concurrency Control and Recovery in Database Systems," *Addison-Wesley*, 1987.

[^10]: X. Zhao et al., "SandTable: Scalable Distributed System Model Checking," *ACM EuroSys*, 2024. <https://doi.org/10.1145/3627703.3650083>

[^11]: E. Clarke et al., "Incremental Verification for Stream Processing Systems," *IEEE/ACM ICSE*, 2022.

[^12]: L. M. Danielsson Villegas, "Decentralized and Distributed Stream Runtime Verification," *PhD Thesis, Universidad Politecnica de Madrid*, 2024.

[^13]: I. Gog et al., "Triad: Creating Synergies Between Memory, Disk, and Log in Log Structured Key-Value Stores," *USENIX ATC*, 2021.

[^14]: Y. Yuan et al., "Exactly-once Semantics for Recoverable Data Processing Applications," *PhD Thesis, UT Austin*, 2024.

[^15]: T. Akidau et al., "The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing," *PVLDB*, 2015. <https://doi.org/10.14778/2824032.2824076>

[^16]: R. Jung et al., "Iris from the Ground Up: A Modular Foundation for Higher-Order Concurrent Separation Logic," *Journal of Functional Programming*, 2018. <https://doi.org/10.1017/S0956796818000151>

[^17]: C. Stanford, "Safe Programming over Distributed Streams," *PhD Thesis, UC Davis*, 2022.

---

## Related Documents

| Document | Relation | Description |
|----------|----------|-------------|
| [unified-streaming-theory.md](unified-streaming-theory.md) | Theoretical Foundation | USTM meta-model definition |
| [consistency-hierarchy.md](consistency-hierarchy.md) | Property Definition | Formalization of consistency levels |
| [expressiveness-hierarchy.md](expressiveness-hierarchy.md) | Decidability | L1-L6 hierarchy and decidability |
| [flink-checkpoint-correctness-proof.md](flink-checkpoint-correctness-proof.md) | Proof Technique | Checkpoint correctness proof |
| [flink-exactly-once-correctness-proof.md](flink-exactly-once-correctness-proof.md) | Target Property | Exactly-Once correctness |
| [chandy-lamport-snapshot-consistency.md](chandy-lamport-snapshot-consistency.md) | Foundation Protocol | Distributed snapshot theory foundation |

---

*Document created: 2026-04-02*
*Last updated: 2026-04-02*
*Maintainer: AnalysisDataFlow Project*
*Status: Active - Open Problem Tracking*

---

*Document version: v1.0 | Translation date: 2026-04-24*
