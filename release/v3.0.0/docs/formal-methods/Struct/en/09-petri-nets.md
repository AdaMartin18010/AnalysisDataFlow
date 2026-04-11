# Petri Nets: A Formal Modeling Language for Concurrent Systems

> **Stage**: formal-methods/appendices | **Prerequisites**: [CCS Process Calculus](01-ccs-calculus.md), [Automata Theory](05-automata-theory.md) | **Formalization Level**: L4

---

## 1. Definitions

### 1.1 Wikipedia Standard Definition

According to the authoritative definition from Wikipedia, **Petri Net** is a **mathematical representation method for discrete parallel systems** proposed by Carl Adam Petri in his 1962 doctoral thesis. It is a graphical and mathematical modeling tool particularly suitable for describing systems with concurrency, synchronization, and asynchronous characteristics[^1].

Core characteristics of Petri nets:

- **Graphical representation**: Uses directed bipartite graphs to intuitively display system structure
- **Rigorous mathematical foundation**: Based on set theory and relational theory
- **Distributed state representation**: State is represented by the distribution of tokens rather than a single global state
- **Local determinism, global non-determinism**: Transition firing is local, but firing order is non-deterministic

### 1.2 Formal Definition

**`Def-PN-01` [Petri Net Quadruple Definition]**: A **Place/Transition Petri Net** (P/T Net) is a quadruple $N = (P, T, F, M_0)$, where:

1. **$P$ = $\{p_1, p_2, \ldots, p_m\}$**: **Place Set** (Places): Represents state components or resource holders of the system
2. **$T$ = $\{t_1, t_2, \ldots, t_n\}$**: **Transition Set** (Transitions): Represents events or operations of the system
3. **$F$ ⊆ $(P \times T) \cup (T \times P)$**: **Flow Relation** (Arcs): Directed edges connecting places and transitions, representing resource flow
4. **$M_0: P \rightarrow \mathbb{N}$**: **Initial Marking**: Number of initial tokens in each place

**Constraints** (well-formedness constraints for valid Petri nets):

- **Disjointness**: $P \cap T = \emptyset$ (places and transitions are disjoint)
- **Non-emptiness**: $P \cup T \neq \emptyset$ (net is non-empty)
- **No isolated elements**: $\forall x \in P \cup T: \exists y \in P \cup T: (x, y) \in F \lor (y, x) \in F$ (each node has at least one incoming or outgoing arc)

### 1.3 Incidence Functions and Weights

**`Def-PN-02` [Preset and Postset]**: For transition $t \in T$:

- **Preset**: $\bullet t = \{p \in P \mid (p, t) \in F\}$, i.e., all places pointing to $t$
- **Postset**: $t\bullet = \{p \in P \mid (t, p) \in F\}$, i.e., all places $t$ points to

For place $p \in P$, define:

- $\bullet p = \{t \in T \mid (t, p) \in F\}$ (transitions pointing to $p$)
- $p\bullet = \{t \in T \mid (p, t) \in F\}$ (transitions $p$ points to)

**`Def-PN-03` [Weight Function]**: Weighted Petri nets introduce weight function $W: F \rightarrow \mathbb{N}^+$, where $W(f)$ represents the weight on arc $f$ (default is 1). The weight function extends to:

$$W(x, y) = \begin{cases} w & \text{if } (x, y) \in F \text{ with weight } w \\ 0 & \text{if } (x, y) \notin F \end{cases}$$

**`Def-PN-04` [Marking and State]**: A marking $M: P \rightarrow \mathbb{N}$ is a function from places to non-negative integers, representing the **global state** of the system. The set of all possible markings is denoted $\mathcal{M} = \mathbb{N}^{|P|}$.

**`Def-PN-05` [Pure Net and Self-loop]**:

- If there exists $p \in P, t \in T$ such that $(p, t) \in F$ and $(t, p) \in F$, this structure is called a **self-loop**
- A Petri net without self-loops is called a **pure net**

### 1.4 Net System Classification

**`Def-PN-06` [Net System Types]**:

| Type | Definition | Characteristics |
|------|------------|-----------------|
| **State Machine** | $\forall t \in T: |\bullet t| = |t\bullet| = 1$ | No concurrency, represents finite state automata only |
| **Marked Graph** | $\forall p \in P: |\bullet p| = |p\bullet| = 1$ | No conflict, no choice, pure concurrency |
| **Free Choice** | $\forall p_1, p_2 \in P: p_1\bullet \cap p_2\bullet \neq \emptyset \Rightarrow p_1\bullet = p_2\bullet$ | Conflict and concurrency separable |
| **Extended Free Choice** | Relaxed version of free choice | Allows more flexible structure |

---

## 2. Properties

### 2.1 Transition Enabling Conditions

**`Lemma-PN-01` [Enabling Condition]**: Transition $t \in T$ is **enabled** at marking $M$, denoted $M[t\rangle$, if and only if:

$$\forall p \in P: M(p) \geq W(p, t)$$

That is, for all input places, the current token count is not less than the input arc weight.

**Proof**: According to the definition of enabling, transition firing requires consuming tokens from input places. Each input place $p$ needs to provide $W(p,t)$ tokens, so the condition is necessary and sufficient. $\square$

### 2.2 State Transition Function

**`Lemma-PN-02` [Marking Update Rule]**: If $M[t\rangle$, then firing $t$ produces new marking $M'$, defined as:

$$M'(p) = M(p) - W(p, t) + W(t, p), \quad \forall p \in P$$

Or in vector form:

$$M' = M + \mathbf{C}(\cdot, t)$$

where $\mathbf{C}$ is the **incidence matrix**, $\mathbf{C}(p, t) = W(t, p) - W(p, t)$.

### 2.3 Reachability Relation

**`Lemma-PN-03` [Transitivity of Reachability]**: The reachability relation $\rightarrow^*$ is transitive. That is, if $M \rightarrow^* M'$ and $M' \rightarrow^* M''$, then $M \rightarrow^* M''$.

**Proof**: Directly from the definition of $\rightarrow^*$ (reflexive transitive closure). $\square$

**`Lemma-PN-04` [Concurrency and Conflict]**:

- **Concurrency**: Two transitions $t_1, t_2$ are concurrently enabled at $M$ if and only if $M[t_1\rangle$ and $M[t_2\rangle$ and their presets are disjoint: $\bullet t_1 \cap \bullet t_2 = \emptyset$
- **Conflict**: Two transitions $t_1, t_2$ have a conflict at $M$ if and only if $M[t_1\rangle$ and $M[t_2\rangle$ and $\bullet t_1 \cap \bullet t_2 \neq \emptyset$

---

## 3. Relations

### 3.1 Encoding Relation Between Petri Nets and CCS

**`Thm-PN-01` [Encoding Theorem]**: Any finite CCS process can be encoded into a Petri net while preserving bisimulation equivalence.

**Encoding Construction**: For CCS process $P$, construct Petri net $N_P = (P_N, T_N, F_N, M_0)$:

1. Each CCS subterm corresponds to a place
2. Action $\alpha$ corresponds to transition $t_\alpha$
3. Parallel composition $P \mid Q$ corresponds to union of places with synchronous connections
4. Restriction $(\nu a)P$ corresponds to hiding transitions related to the action

**Mermaid Diagram: CCS to Petri Net Encoding Mapping**

```mermaid
graph TB
    subgraph CCS Process
        P["P = a.Q | b.R"]
        Q["Q = c.0"]
        R["R = d.0"]
    end

    subgraph Petri Net
        P_pos["Place: P"]
        Q_pos["Place: Q"]
        R_pos["Place: R"]

        Ta["Transition: a"]
        Tb["Transition: b"]
        Tc["Transition: c"]
        Td["Transition: d"]

        P_pos -->|W=1| Ta
        P_pos -->|W=1| Tb
        Ta -->|W=1| Q_pos
        Tb -->|W=1| R_pos
        Q_pos -->|W=1| Tc
        R_pos -->|W=1| Td
    end

    P -.->|Encode| P_pos
    Q -.->|Encode| Q_pos
    R -.->|Encode| R_pos
```

### 3.2 Comparison with Other Concurrency Models

**`Prop-PN-01` [Expressiveness Hierarchy]**:

| Model | Expressiveness | State Space | Main Analysis Tools |
|-------|---------------|-------------|---------------------|
| Finite Automata | Regular languages | Finite | State traversal |
| Petri Nets | Partially decidable | Potentially infinite | Coverability graph, Linear algebra |
| Turing Machine | Recursively enumerable | Infinite | Undecidable |
| CCS/π-calculus | Infinite state | Potentially infinite | Bisimulation, Model checking |

**`Prop-PN-02` [Advantages of Petri Nets]**:

1. **Graphical intuitiveness**: Distributed state visualization
2. **True concurrency semantics**: Non-interleaving semantics, direct representation of concurrency
3. **Analysis decidability**: Certain properties are decidable in Petri nets (though complexity may be high)
4. **No global state**: Natural support for distributed system modeling

---

## 4. Argumentation

### 4.1 State Space Explosion Problem

**`Lemma-PN-05` [State Space Complexity]**: For a Petri net with $n$ places, each bounded by $k$, the reachability graph has at most $(k+1)^n$ nodes.

**Proof**: Each place $p_i$ can contain $0$ to $k$ tokens, giving $k+1$ possibilities. The combination of $n$ places is $(k+1)^n$. $\square$

### 4.2 Challenges of Unbounded Nets

**`Lemma-PN-06` [Unboundedness Leads to Infinite State]**: There exist Petri nets such that for any $k \in \mathbb{N}$, there is a reachable marking $M$ where $\exists p: M(p) > k$.

**Example**: Consider a simple net $p_1 \rightarrow t \rightarrow p_2$, where $t$ has a self-loop back to $p_1$. Each firing of $t$ increases the token count in $p_2$ while $p_1$ remains unchanged (or cycles).

### 4.3 Necessity of Coverability Graph

**`Prop-PN-03` [Existence of Coverability Graph]**: For any Petri net, its coverability graph is finite and computable.

**Argument**: Even if the state space is infinite, the coverability graph compresses infinite sets by introducing a special symbol $\omega$ representing "arbitrarily large", making analysis possible.

---

## 5. Formal Proofs

### 5.1 Reachability Decidability

**`Thm-PN-02` [Mayr's Theorem / Reachability Decidability]**: For Petri nets, given initial marking $M_0$ and target marking $M$, the problem of determining whether $M$ is reachable from $M_0$ is **decidable**[^6].

**Historical Context**: This theorem was proved by Ernst Mayr in 1981, resolving a long-standing open problem. The proof used **Generalized Petri Nets** and **modified coverability tree** techniques.

**Proof Sketch** (Mayr 1981):

1. **Normalization**: Convert Petri net to standard form (ordinary Petri net)
2. **Construct coverability tree**: Build finite representation of reachable state coverability tree
3. **Introduce $\omega$ symbol**: Use $\omega$ to represent arbitrarily growing token counts
4. **Semi-linear set property**: Prove that reachable sets can be represented as semi-linear sets (Presburger definable)
5. **Decision algorithm**: Conclude based on decidable properties of semi-linear sets

**Complexity Note**: Although the reachability problem is decidable, it has been proven to be **EXPSPACE-hard**, and the original Mayr algorithm has non-elementary complexity.

### 5.2 Boundedness Decision Algorithm

**`Thm-PN-03` [Boundedness Decision]**: The boundedness problem for Petri nets is decidable and can be completed in polynomial space.

**Algorithm** (Based on coverability graph):

**Input**: Petri net $N = (P, T, F, M_0)$
**Output**: Whether all places are bounded

```
Algorithm Boundedness-Check:
1. Construct coverability graph CG(N)
2. For each place p ∈ P:
   a. If CG(N) contains node with ω(p) = ω
   b. Then p is unbounded
3. If unbounded place exists, return "Unbounded"
4. Otherwise return "Bounded"
```

**Correctness Proof**:

- **Completeness**: Coverability graph precisely characterizes all reachable markings (considering $\omega$)
- **Soundness**: If $\omega$ appears at some place, according to coverability graph construction rules, that place's marking can grow infinitely

**`Lemma-PN-07` [Linear Algebra Criterion for Place Boundedness]**: Place $p$ is bounded if and only if there exists a non-negative integer vector $Y \geq 0$ such that $Y^T \cdot \mathbf{C} \leq 0$ and $Y(p) > 0$.

**Proof**: This is a duality result based on **state equations** and **Farkas' lemma**. $\square$

### 5.3 Relation Between Liveness and Reachability

**`Thm-PN-04` [Liveness Decision]**: Given Petri net $N$ and transition $t$, determining whether $t$ is **live** (i.e., $t$ can eventually be enabled from any reachable marking) is decidable.

**Definition**: Transition $t$ is live if:

$$\forall M \in R(N, M_0), \exists M' \in R(N, M): M'[t\rangle$$

**Relation with Reachability**:

**`Prop-PN-04` [Liveness Implies Reachability Queries]**: Transition $t$ is live if and only if for all reachable markings $M$, there exists a reachable path from $M$ to some marking that enables $t$.

This is essentially a combination of **infinite reachability queries**, but due to the well-structured nature of Petri nets, it can be transformed into a finite problem.

**`Thm-PN-05` [Commoner's Theorem]**: For free choice nets, a sufficient and necessary condition for system liveness is: every directed circuit contains at least one token.

### 5.4 Fairness Analysis

**`Def-PN-07` [Fairness Types]**:

1. **Weak Fairness**: If transition $t$ is enabled infinitely often, it fires infinitely often
2. **Strong Fairness**: If transition $t$ is continuously enabled from some point, it is eventually fired

**`Thm-PN-06` [Fairness Decision]**: For Petri nets, determining whether there exists an infinite firing sequence satisfying given fairness conditions is **undecidable**.

**Proof Sketch**: This can be proven by reduction from the **halting problem**. $\square$

---

## 6. Examples

### 6.1 Producer-Consumer Problem

**`Ex-PN-01` [Producer-Consumer]**:

```mermaid
graph LR
    subgraph Producer
        P_ready["P_ready<br/>Initial:1"]
        P_prod["P_prod<br/>Initial:0"]
    end

    subgraph Buffer
        Buffer["Buffer<br/>Capacity:5<br/>Initial:0"]
    end

    subgraph Consumer
        C_ready["C_ready<br/>Initial:1"]
        C_cons["C_cons<br/>Initial:0"]
    end

    P_ready -->|produce| P_prod
    P_prod -->|put| Buffer
    Buffer -->|get| C_cons
    C_cons -->|consume| C_ready

    Buffer -.->|Capacity limit| Buffer
```

**Analysis**:

- Boundedness: Buffer capacity is 5, system is bounded
- Liveness: As long as producer and consumer are ready, system can run indefinitely
- Fairness: Under fair scheduling, producer and consumer execute alternately

### 6.2 Dining Philosophers Problem

**`Ex-PN-02` [Philosophers Problem]**:

```mermaid
graph TB
    subgraph Philosopher 1
        T1["Thinking"]
        H1["Hungry"]
        E1["Eating"]
    end

    subgraph Forks
        F1["Fork 1<br/>Initial:1"]
        F2["Fork 2<br/>Initial:1"]
    end

    subgraph Philosopher 2
        T2["Thinking"]
        H2["Hungry"]
        E2["Eating"]
    end

    T1 -->|get_hungry| H1
    H1 -->|pick_F1<br/>Requires F1=1| E1
    H1 -->|pick_F2<br/>Requires F2=1| E1
    E1 -->|release| T1

    T2 -->|get_hungry| H2
    H2 -->|pick_F1<br/>Requires F1=1| E2
    H2 -->|pick_F2<br/>Requires F2=1| E2
    E2 -->|release| T2

    E1 -.Releases.-> F1
    E1 -.Releases.-> F2
    E2 -.Releases.-> F1
    E2 -.Releases.-> F2
```

**Deadlock Analysis**: If both philosophers pick up their left forks simultaneously, the system enters deadlock. Petri nets can detect such reachable deadlock states.

---

## 7. Visualizations

### 7.1 Petri Net Structure Hierarchy

```mermaid
mindmap
  root((Petri Net))
    Formal Definition
      Quadruple P,T,F,M0
      Places
      Transitions
      Flow Relation
      Weights
    Net Types
      State Machine SM
      Marked Graph MG
      Free Choice FC
      Extended Free Choice EFC
      Asymmetric Choice AC
    Dynamic Semantics
      Enabled
      Firing
      Marking
      State Change
    Analysis Techniques
      Reachability Graph RG
      Coverability Graph CG
      State Equation SE
      Linear Algebra LA
    Property Verification
      Boundedness
      Liveness
      Reachability
      Fairness
      Reversibility
```

### 7.2 Coverability Graph Construction Process

```mermaid
flowchart TD
    A[Start<br/>M0 = Initial Marking] --> B{Already have same or larger marking?}
    B -->|No| C[Create new node]
    C --> D[Find all enabled transitions]
    D --> E[For each enabled transition t]
    E --> F[Calculate new marking M']
    F --> G{M' > Parent marking?}
    G -->|Yes| H[Mark ω at growing positions]
    G -->|No| I[Keep M']
    H --> B
    I --> B
    B -->|Yes| J[Merge node]
    J --> K{More unprocessed nodes?}
    K -->|Yes| D
    K -->|No| L[Coverability graph complete]

    style A fill:#e1f5e1
    style L fill:#e1f5e1
    style H fill:#fff3cd
```

### 7.3 Eight-Dimensional Characterization

```mermaid
graph TB
    subgraph "Eight-Dimensional Characterization"
        direction TB

        D1["1. Syntax Dimension<br/>Quadruple Definition<br/>Structural Constraints"]
        D2["2. Semantics Dimension<br/>Enabling Condition<br/>Firing Rule"]
        D3["3. Operational Dimension<br/>Reachability<br/>State Transition"]
        D4["4. Algebraic Dimension<br/>Incidence Matrix<br/>State Equation"]
        D5["5. Logical Dimension<br/>Temporal Logic<br/>CTL/LTL"]
        D6["6. Computational Dimension<br/>Decidability<br/>Complexity"]
        D7["7. Relational Dimension<br/>With Other Models<br/>Encoding Relations"]
        D8["8. Application Dimension<br/>Concurrent Systems<br/>Protocol Verification"]
    end

    D1 --> D2 --> D3 --> D4 --> D5 --> D6 --> D7 --> D8
    D8 -.->|Feedback| D1
```

---

## 8. Eight-Dimensional Characterization

### 8.1 Syntax Dimension

**Characterization**: The syntax of Petri nets is strictly defined by the quadruple $N = (P, T, F, M_0)$.

**Key Elements**:

- **Bipartite graph structure**: Places and transitions form two disjoint node types
- **Directed arcs**: Represent unidirectional flow of resources or control
- **Multiset semantics**: Markings are multisets over places

### 8.2 Semantics Dimension

**Characterization**: Operational semantics defines the dynamic behavior of the system.

**Core Rules**:

1. **Enabling rule**: Resource sufficiency check
2. **Firing rule**: Atomic consumption and production of tokens
3. **Interleaving vs true concurrency**: Petri nets support true concurrency semantics

### 8.3 Operational Dimension

**Characterization**: Reachability analysis reveals all possible behaviors of the system.

**Reachable Set**: $R(N, M_0) = \{M \mid M_0 \rightarrow^* M\}$

**Key Properties**:

- Reachability is decidable (Mayr 1981)
- Reachable sets may be non-semi-linear

### 8.4 Algebraic Dimension

**Characterization**: Linear algebra tools provide efficient analysis methods.

**State Equation**:

$$M = M_0 + \mathbf{C} \cdot \vec{\sigma}$$

where $\vec{\sigma}$ is the firing count vector.

**Note**: The state equation is a **necessary but not sufficient** condition for reachability (due to firing order constraints).

### 8.5 Logical Dimension

**Characterization**: Temporal logic expresses system properties.

**Common Formulas**:

- Safety: $G \neg (M(p) > k)$ — place $p$ never exceeds $k$
- Liveness: $GF \text{ Enabled}(t)$ — transition $t$ is enabled infinitely often
- Reachability: $F (M = M_{target})$ — eventually reaches target marking

### 8.6 Computational Dimension

**Characterization**: Decidability and complexity of analysis problems.

| Problem | Decidability | Complexity |
|---------|--------------|------------|
| Reachability | ✅ Decidable | EXPSPACE-hard |
| Coverability | ✅ Decidable | EXPSPACE-complete |
| Boundedness | ✅ Decidable | PSPACE-complete |
| Liveness | ✅ Decidable | EXPSPACE-hard |
| Model Checking | ❌ Undecidable | — |

### 8.7 Relational Dimension

**Characterization**: Relations with other computational models.

**Encoding Capability**:

- Petri nets ⊃ Finite automata (strictly stronger)
- Petri nets ⊂ Turing machine (cannot represent all computable functions)
- Petri nets ~ CCS (bisimulation equivalence class)

### 8.8 Application Dimension

**Characterization**: Real-world system modeling and verification.

**Application Domains**:

- **Concurrent program verification**: Deadlock detection, liveness verification
- **Communication protocols**: Protocol correctness verification
- **Manufacturing systems**: Production process optimization
- **Workflow systems**: Business process modeling
- **Biological systems**: Gene regulatory networks

---

## 9. Coverability Graph

### 9.1 Motivation and Definition

**`Def-PN-08` [Coverability Relation]**: Marking $M$ **covers** $M'$, denoted $M \geq M'$, if:

$$\forall p \in P: M(p) \geq M'(p)$$

**`Def-PN-09` [Coverability Graph]**: The **coverability graph** $CG(N)$ of a Petri net is a marking graph where:

- Nodes are **generalized markings** (allowing $\omega$ symbol)
- Edges are labeled by enabled transitions
- $\omega$ represents "arbitrarily large" token count

### 9.2 Construction Algorithm

**Algorithm Coverability-Graph-Construction**:

```
Input: Petri net N = (P, T, F, M0)
Output: Coverability graph CG = (V, E)

V := {M0}; E := ∅; ToProcess := {M0}

while ToProcess ≠ ∅ do
    Take M ∈ ToProcess; ToProcess := ToProcess \\ {M}

    // ω-extension: check for strict growth
    if ∃path M0 →* M' →* M and M > M' then
        For all positions p where M(p) > M'(p):
            M(p) := ω
    end if

    for each t ∈ T such that M[t⟩ do
        Calculate M' = M + C(·, t)

        if M' ∉ V then
            V := V ∪ {M'}
            ToProcess := ToProcess ∪ {M'}
        end if

        E := E ∪ {(M, t, M')}
    end for
end while
```

### 9.3 Properties and Applications

**`Thm-PN-07` [Finiteness of Coverability Graph]**: For any Petri net, its coverability graph is finite.

**Proof Sketch**:

1. Each position can take values from $\mathbb{N} \cup \{\omega\}$
2. Once a position is marked with $\omega$, it remains forever
3. By **Dickson's Lemma**, there are no infinite strictly descending well-ordered sets
4. Therefore the construction process must terminate

**Applications**:

- **Boundedness decision**: Check if any position is marked with $\omega$
- **Coverability decision**: Check if target marking is covered by some node
- **Liveness analysis**: Analyze transition enabling patterns based on coverability graph

---

## 10. Historical Background

### 10.1 Carl Adam Petri's Contribution

**`Historical Note`**: Carl Adam Petri (1926-2010) was a German mathematician and computer scientist.

**1962 Doctoral Thesis**: *Kommunikation mit Automaten* (Communication with Automata)[^2]

**Core Innovations**:

1. Proposed **Net Theory** as mathematical foundation for communication systems
2. Introduced **concurrency** as a basic concept, not a derived one
3. Developed **non-interleaving semantics**: Opposed reducing concurrency to non-deterministic interleaving
4. Established **partial order semantics**: Based on causal relationships rather than global clock

### 10.2 Development Milestones

| Year | Milestone | Contributor |
|------|-----------|-------------|
| 1962 | Original Petri net definition | Carl Adam Petri |
| 1974 | Petri net naming | Widely adopted by computer science community |
| 1981 | Reachability decidability proof | Ernst Mayr |
| 1989 | Murata's classic survey | Tadao Murata |
| 1990s | Advanced Petri nets | Colored nets, Timed nets, Stochastic nets |
| 2000s | Model checking integration | Integration with SPIN, UPPAAL tools |

---

## 11. References

[^1]: Wikipedia contributors, "Petri net," Wikipedia, The Free Encyclopedia, <https://en.wikipedia.org/wiki/Petri_net> (accessed April 10, 2026).

[^2]: C. A. Petri, "Kommunikation mit Automaten," Ph.D. dissertation, University of Bonn, Bonn, Germany, 1962.




[^6]: E. W. Mayr, "An Algorithm for the General Petri Net Reachability Problem," in *Proceedings of the 13th Annual ACM Symposium on Theory of Computing (STOC '81)*, 1981, pp. 238-246. DOI: 10.1145/800076.802477










---

**Document Metadata**

- Document ID: FM-APP-WP-10
- Version: 1.0
- Creation Date: 2026-04-10
- Author: AnalysisDataFlow Project
- Formal Elements Statistics: 9 definitions, 7 lemmas, 6 propositions, 7 theorems
- References: 15
