# Formal Methods

> **Wikipedia Standard Definition**: Formal methods are mathematically based techniques for the specification, development, and analysis of software and hardware systems.
>
> **Source**: <https://en.wikipedia.org/wiki/Formal_methods>
>
> **Formalization Level**: L1 (Basic Concepts)

---

## 1. Wikipedia Standard Definition

### English Original
>
> "Formal methods are mathematically based techniques for the specification, development, and analysis of software and hardware systems. The use of formal methods is motivated by the expectation that, as in other engineering disciplines, performing appropriate mathematical analysis can contribute to the reliability and robustness of a design."

### Chinese Standard Translation
>
> **Formal Methods** are mathematically based techniques for the specification, development, and analysis of software and hardware systems. The motivation for using formal methods is the expectation that, as in other engineering disciplines, performing appropriate mathematical analysis can improve the reliability and robustness of a design.

---

## 2. Formal Expressions

### 2.1 Formal Definition of Formal Methods

**Def-S-98-01** (Formal Methods System). A formal method is a quintuple:

$$\mathcal{FM} = \langle \mathcal{L}_{\text{spec}}, \mathcal{L}_{\text{impl}}, \mathcal{R}_{\text{refine}}, \mathcal{V}_{\text{verify}}, \mathcal{T}_{\text{transform}} \rangle$$

where:

- $\mathcal{L}_{\text{spec}}$: Specification language (e.g., Z, VDM, TLA+)
- $\mathcal{L}_{\text{impl}}$: Implementation language (e.g., programming languages, hardware description languages)
- $\mathcal{R}_{\text{refine}}$: Refinement relation, $\mathcal{L}_{\text{spec}} \times \mathcal{L}_{\text{impl}} \rightarrow \{\text{true}, \text{false}\}$
- $\mathcal{V}_{\text{verify}}$: Verification methods (model checking, theorem proving, etc.)
- $\mathcal{T}_{\text{transform}}$: Transformation tool set

### 2.2 Formal Correctness

**Def-S-98-02** (Formal Correctness). System $S$ is formally correct with respect to specification $Spec$ if and only if:

$$S \models_{\mathcal{L}} Spec \Leftrightarrow \mathcal{V}(S, Spec) = \text{VALID}$$

where $\mathcal{V}$ is the verifier, $\models_{\mathcal{L}}$ is the satisfaction relation in language $\mathcal{L}$.

---

## 3. Properties and Characteristics

### 3.1 Core Properties

| Property | Definition | Importance |
|----------|------------|------------|
| **Precision** | Using mathematical notation to eliminate natural language ambiguity | ⭐⭐⭐⭐⭐ |
| **Verifiability** | Support for automated or semi-automated correctness proofs | ⭐⭐⭐⭐⭐ |
| **Abstraction Levels** | Step-by-step refinement from high-level specifications to concrete implementations | ⭐⭐⭐⭐ |
| **Completeness** | Coverage of all possible behaviors of the system | ⭐⭐⭐⭐ |
| **Composability** | Support for modular analysis and verification | ⭐⭐⭐⭐ |

### 3.2 Formal Methods Spectrum

```mermaid
mindmap
  root((Formal Methods))
    Specification Methods
      Axiomatic Specification
        Z Language
        VDM
        B Method
      Model-based Specification
        TLA+
        Alloy
        Event-B
      Algebraic Specification
        CASL
        OBJ
    Verification Methods
      Model Checking
        Explicit State
        Symbolic Model Checking
        Bounded Model Checking
      Theorem Proving
        Automated Theorem Proving
        Interactive Theorem Proving
        Satisfiability Modulo Theories
      Abstract Interpretation
        Static Analysis
        Program Verification
        Type Systems
    Development Methods
      Refinement Calculus
        Stepwise Refinement
        Program Extraction
      Transformation Systems
        Compiler Verification
        Optimization Verification
```

---

## 4. Relation Network

### 4.1 Conceptual Hierarchy

```mermaid
graph TB
    subgraph "Mathematical Foundations"
        LOGIC[Logic]
        SET[Set Theory]
        CAT[Category Theory]
    end

    subgraph "Formal Methods"
        SPEC[Specification Methods]
        VERIF[Verification Methods]
        DEV[Development Methods]
    end

    subgraph "Application Domains"
        HW[Hardware Verification]
        SW[Software Verification]
        PROTO[Protocol Verification]
        SEC[Security Analysis]
    end

    LOGIC --> SPEC
    LOGIC --> VERIF
    SET --> SPEC
    CAT --> VERIF

    SPEC --> HW
    SPEC --> SW
    VERIF --> PROTO
    VERIF --> SEC
    DEV --> SW
```

### 4.2 Relations with Other Core Concepts

| Concept | Relation Type | Description |
|---------|---------------|-------------|
| **Logic** | Foundation | Formal methods are based on mathematical logic |
| **Model Checking** | Instance | An automated technique for formal verification |
| **Theorem Proving** | Instance | A deductive technique for formal verification |
| **Type Theory** | Foundation | Curry-Howard correspondence connects programs and proofs |
| **Abstract Interpretation** | Instance | Theoretical foundation for formal static analysis |

---

## 5. Historical Background

### 5.1 Development History

```mermaid
timeline
    title History of Formal Methods Development
    section 1960s-1970s
        Foundation : Floyd-Hoare Logic
                   : Dijkstra Weakest Precondition
                   : Program Correctness Theory Established
    section 1980s-1990s
        Language Development : Z, VDM, CSP Emergence
                             : Birth of Model Checking
                             : Process Calculus Matured
    section 2000s-2010s
        Tool Maturity : TLA+ Industrial Application
                      : Coq/Isabelle Large-scale Proofs
                      : SMT Solver Revolution
    section 2020s
        AI Integration : Neural Theorem Proving
                       : LLM-assisted Formalization
                       : Automation Level Improvement
```

### 5.2 Milestone Events

| Year | Event | Contributor |
|------|-------|-------------|
| 1967 | Floyd Assignment Axioms | Robert W. Floyd |
| 1969 | Hoare Logic | C.A.R. Hoare |
| 1975 | Weakest Precondition | Edsger W. Dijkstra |
| 1980 | CCS Process Calculus | Robin Milner |
| 1985 | CTL Model Checking | Clarke & Emerson |
| 1989 | π-calculus | Robin Milner |
| 1999 | TLA+ Release | Leslie Lamport |
| 2009 | seL4 Verification Complete | Klein et al. |
| 2024 | AlphaProof IMO Silver Medal | DeepMind |

---

## 6. Formal Proofs

### 6.1 Soundness Theorem of Formal Methods

**Thm-S-98-01** (Soundness of Formal Verification). If formal verifier $\mathcal{V}$ proves that system $S$ satisfies specification $Spec$, then under formal semantics $S$ indeed satisfies $Spec$:

$$\mathcal{V}(S, Spec) = \text{VALID} \Rightarrow S \models Spec$$

*Proof*:

1. Let $\mathcal{V}$ be based on formal semantics $\llbracket \cdot \rrbracket$
2. Verification process computes $\llbracket S \rrbracket \subseteq \llbracket Spec \rrbracket$
3. By semantic definition, $\llbracket S \rrbracket \subseteq \llbracket Spec \rrbracket \Leftrightarrow S \models Spec$
4. Therefore successful verification implies satisfaction relation ∎

### 6.2 Completeness Limitations

**Thm-S-98-02** (Incompleteness of Formal Verification). For Turing-complete languages, formal verification is not complete:

$$\exists S, Spec: S \models Spec \land \mathcal{V}(S, Spec) = \text{UNKNOWN}$$

*Proof Sketch*:

1. From undecidability of the halting problem
2. Program correctness implies halting (total correctness)
3. Therefore program correctness is also undecidable
4. Any verifier must necessarily have cases returning UNKNOWN ∎

---

## 7. Eight-Dimensional Characterization

### 7.1 Mind Map

```mermaid
mindmap
  root((Formal Methods))
    Mathematical Foundations
      Logic
        Propositional Logic
        First-order Logic
        Modal Logic
        Temporal Logic
      Set Theory
        ZFC Axioms
        Relations
        Functions
      Type Theory
        Simple Types
        Dependent Types
        Polymorphic Types
    Specification Techniques
      State Machines
      Algebraic Specification
      Logical Specification
    Verification Techniques
      Model Checking
      Theorem Proving
      Abstract Interpretation
      Type Checking
    Application Domains
      Hardware
      Software
      Protocols
      Security
```

### 7.2 Multi-dimensional Comparison Matrix

| Dimension | Formal Methods | Traditional Testing | Advantage Ratio |
|-----------|---------------|---------------------|-----------------|
| Coverage | 100% | Sampling | 100:1 |
| Reliability | Mathematical Guarantee | Statistical Guarantee | 10:1 |
| Cost | High | Low | 1:10 |
| Automation | Medium | High | 1:2 |
| Maintainability | Medium | High | 1:1 |
| Learning Curve | Steep | Gentle | 1:5 |

### 7.3 Axiom-Theorem Tree

```mermaid
graph TD
    A1[Axiom: Law of Excluded Middle] --> L1[Logical Foundation]
    A2[Axiom: ZFC Set Theory] --> L2[Mathematical Foundation]

    L1 --> T1[Theorem: Propositional Logic Completeness]
    L1 --> T2[Theorem: First-order Logic Incompleteness]
    L2 --> T3[Theorem: Mathematical Induction Validity]

    T1 --> T4[Theorem: Hoare Logic Relative Completeness]
    T2 --> T5[Theorem: Program Verification Undecidability]
    T3 --> T6[Theorem: Type System Soundness]

    T4 --> C1[Corollary: Partial Programs Verifiable]
    T5 --> C2[Corollary: Approximation Methods Needed]
    T6 --> C3[Corollary: Well-typed Programs Have No Runtime Errors]

    style A1 fill:#ffcccc
    style A2 fill:#ffcccc
    style T4 fill:#ccffcc
    style T6 fill:#ccffcc
    style C1 fill:#ccffff
    style C3 fill:#ccffff
```

### 7.4 State Transition Diagram

```mermaid
stateDiagram-v2
    [*] --> Requirements Analysis
    Requirements Analysis --> Formal Specification: Using Specification Language
    Formal Specification --> Model Checking: Finite State Systems
    Formal Specification --> Theorem Proving: Infinite State Systems
    Formal Specification --> Abstract Interpretation: Static Analysis

    Model Checking --> Verification Passed: Property Holds
    Model Checking --> Counterexample Generated: Property Violated
    Theorem Proving --> Verification Passed: Proof Complete
    Theorem Proving --> Proof Obligations: Assistance Needed
    Abstract Interpretation --> Verification Passed: Safe
    Abstract Interpretation --> False Positive: Too Conservative

    Counterexample Generated --> Specification Correction: Correct Specification
    Proof Obligations --> Specification Correction: Strengthen Invariant
    False Positive --> Refine Abstraction: More Precise Domain

    Specification Correction --> Formal Specification
    Refine Abstraction --> Abstract Interpretation

    Verification Passed --> [*]
```

### 7.5 Dependency Relation Graph

```mermaid
graph BT
    subgraph "Prerequisite Knowledge"
        A[Discrete Mathematics]
        B[Mathematical Logic]
        C[Set Theory]
    end

    subgraph "Basic Formalization"
        D[Formal Specification]
        E[Operational Semantics]
        F[Type Systems]
    end

    subgraph "Verification Techniques"
        G[Model Checking]
        H[Theorem Proving]
        I[Abstract Interpretation]
    end

    subgraph "Advanced Applications"
        J[Program Verification]
        K[Protocol Verification]
        L[System Verification]
    end

    A --> D
    B --> D
    B --> E
    C --> E
    D --> F
    E --> F
    F --> G
    F --> H
    E --> I
    G --> J
    H --> J
    I --> J
    G --> K
    H --> K
    J --> L
    K --> L
```

### 7.6 Evolution Timeline

```mermaid
timeline
    title Evolution of Formal Methods Tools and Theory
    section 1960s
        Floyd : Foundation of Program Verification
              : Flowchart Semantics
    section 1970s
        Hoare : Hoare Logic
              : Axiomatic Semantics
        Dijkstra : Weakest Precondition
                 : Structured Programming
    section 1980s
        CCS/CSP : Concurrency Theory
                : Process Calculus
        ModelChecking : Clarke/Emerson
                      : Birth of Automatic Verification
    section 1990s
        TLA+ : Lamport
             : Temporal Logic of Actions
        BMethod : Abrial
                : Refinement Calculus
    section 2000s
        Coq/Isabelle : Proof Assistants Matured
                     : Large-scale Proofs
        SLAM/BLAST : Microsoft Projects
                   : Software Model Checking
    section 2010s
        SMT : Z3/CVC4
            : Solver Revolution
        Dafny/Ironclad : Verification Languages
                       : Verifiable Systems
    section 2020s
        AlphaProof : Neural Theorem Proving
                   : AI Integration
        Lean4/mathlib : Mathematical Formalization
                      : Community Collaboration
```

### 7.7 Hierarchical Architecture

```mermaid
graph TB
    subgraph "Application Layer"
        A1[System Verification]
        A2[Program Analysis]
        A3[Protocol Checking]
    end

    subgraph "Method Layer"
        M1[Model Checking]
        M2[Theorem Proving]
        M3[Abstract Interpretation]
        M4[Type Systems]
    end

    subgraph "Logic Layer"
        L1[Propositional/First-order Logic]
        L2[Temporal Logic]
        L3[Modal Logic]
        L4[Hoare Logic]
    end

    subgraph "Mathematics Layer"
        MA1[Set Theory]
        MA2[Category Theory]
        MA3[Domain Theory]
        MA4[Type Theory]
    end

    A1 --> M1
    A1 --> M2
    A2 --> M3
    A2 --> M4
    A3 --> M1
    A3 --> M2

    M1 --> L2
    M2 --> L1
    M2 --> L3
    M3 --> L4
    M4 --> L1

    L1 --> MA1
    L2 --> MA1
    L3 --> MA2
    L4 --> MA4
    MA4 --> MA3
```

### 7.8 Proof Search Tree

```mermaid
graph TD
    A[Proof Goal: Γ ⊢ P] --> B{Form of P?}

    B -->|Atomic Proposition| C[Assumption Lookup]
    B -->|Conjunction P∧Q| D[Prove P and Q Separately]
    B -->|Disjunction P∨Q| E[Choose to Prove P or Q]
    B -->|Implication P→Q| F[Assume P, Prove Q]
    B -->|Universal ∀x.P| G[Take arbitrary c, Prove P[c/x]]
    B -->|Existential ∃x.P| H[Construct t, Prove P[t/x]]

    C --> I{P∈Γ?}
    I -->|Yes| J[Proof Complete]
    I -->|No| K[Try Resolution]

    D --> L[Subgoal 1: Γ ⊢ P]
    D --> M[Subgoal 2: Γ ⊢ Q]

    E --> N[Subgoal: Γ ⊢ P]
    E --> O[Subgoal: Γ ⊢ Q]

    F --> P[Extend Environment: Γ,P ⊢ Q]

    G --> Q[Skolem Constant]

    H --> R{Term t?}
    R -->|Known| S[Substitute]
    R -->|Unknown| T[Synthesize/Search]

    style J fill:#ccffcc
    style K fill:#ffcccc
```

---

## 8. References

### Wikipedia Original References



### Classic Literature





---

## 9. Related Concepts

- [Model Checking](../../98-appendices/wikipedia-concepts/en/02-model-checking.md)
- [Theorem Proving](../../98-appendices/wikipedia-concepts/en/03-theorem-proving.md)
- [Process Calculus](../../98-appendices/wikipedia-concepts/en/04-process-calculus.md)
- [Temporal Logic](../../98-appendices/wikipedia-concepts/en/05-temporal-logic.md)
- [Hoare Logic](../../98-appendices/wikipedia-concepts/en/06-hoare-logic.md)
- [Type Theory](../../98-appendices/wikipedia-concepts/en/07-type-theory.md)

---

> **Concept Tags**: #FormalMethods #BasicConcepts #MathematicalFoundations #SoftwareEngineering #HardwareVerification
>
> **Learning Difficulty**: ⭐⭐⭐ (Intermediate)
>
> **Prerequisites**: Mathematical Logic, Set Theory
>
> **Follow-up Concepts**: Model Checking, Theorem Proving, Process Calculus
