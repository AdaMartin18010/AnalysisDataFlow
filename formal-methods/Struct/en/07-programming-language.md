# Programming Language Theory (Type Theory)

> **Wikipedia Standard Definition**: In mathematics, logic, and computer science, a type theory is the formal presentation of a specific type system. Type theory is the academic study of type systems.
>
> **Source**: <https://en.wikipedia.org/wiki/Type_theory>
>
> **Formalization Level**: L4-L6

---

## 1. Wikipedia Standard Definition

### English Original
>
> "In mathematics, logic, and computer science, a type theory is the formal presentation of a specific type system. Type theory is the academic study of type systems. Some type theories serve as alternatives to set theory as a foundation of mathematics. Two well-known type theories that can serve as foundations are Alonzo Church's typed λ-calculus and Per Martin-Löf's intuitionistic type theory."

---

## 2. Formal Expression

### 2.1 Simply Typed Lambda Calculus (λ→)

**Def-S-98-01** (Type Syntax). Simple types:

$$\tau, \sigma ::= \iota \mid \tau \rightarrow \sigma$$

Where $\iota$ is a base type (e.g., Bool, Nat).

**Def-S-98-02** (Term Syntax). Typed lambda terms:

$$t, u ::= x \mid \lambda x:\tau.t \mid t\,u \mid c$$

**Def-S-98-03** (Typing Judgment). In context $\Gamma$, term $t$ has type $\tau$:

$$\Gamma \vdash t : \tau$$

**Def-S-98-04** (Typing Rules).

$$
\text{(VAR)} \quad \frac{x:\tau \in \Gamma}{\Gamma \vdash x : \tau}
$$

$$
\text{(ABS)} \quad \frac{\Gamma, x:\tau \vdash t : \sigma}{\Gamma \vdash \lambda x:\tau.t : \tau \rightarrow \sigma}
$$

$$
\text{(APP)} \quad \frac{\Gamma \vdash t : \tau \rightarrow \sigma, \quad \Gamma \vdash u : \tau}{\Gamma \vdash t\,u : \sigma}
$$

### 2.2 System F (Polymorphic Lambda Calculus)

**Def-S-98-05** (System F Syntax). Extended types with type variables and universal quantifiers:

$$\tau ::= \alpha \mid \tau \rightarrow \tau \mid \forall\alpha.\tau$$

**Def-S-98-06** (Type Abstraction and Application).

$$
\text{(TABS)} \quad \frac{\Gamma \vdash t : \tau, \quad \alpha \notin \text{FTV}(\Gamma)}{\Gamma \vdash \Lambda\alpha.t : \forall\alpha.\tau}
$$

$$
\text{(TAPP)} \quad \frac{\Gamma \vdash t : \forall\alpha.\tau}{\Gamma \vdash t[\sigma] : \tau\{\sigma/\alpha\}}
$$

### 2.3 Martin-Löf Type Theory (MLTT)

**Def-S-98-07** (Judgment Forms). MLTT has four forms of judgments:

1. $\Gamma \vdash A\,\text{type}$ — $A$ is a well-formed type
2. $\Gamma \vdash A \equiv B\,\text{type}$ — $A$ and $B$ are equal types
3. $\Gamma \vdash a : A$ — $a$ is a term of type $A$
4. $\Gamma \vdash a \equiv b : A$ — $a$ and $b$ are equal in type $A$

**Def-S-98-08** (Inductive Types). Inductive types are defined by constructors:

$$
\frac{\Gamma \vdash a : A \quad \Gamma \vdash b : B(a)}{\Gamma \vdash (a, b) : \Sigma x:A.B(x)} \quad (\Sigma\text{-INTRO})
$$

$$
\frac{\Gamma \vdash p : \Sigma x:A.B(x)}{\Gamma \vdash \pi_1(p) : A} \quad (\Sigma\text{-ELIM}_1)
$$

---

## 3. Properties

### 3.1 Curry-Howard Isomorphism

**Def-S-98-09** (Curry-Howard-Lambek Correspondence). Three-domain isomorphism:

| Logic | Type Theory | Category Theory |
|-------|-------------|-----------------|
| Proposition $P$ | Type $P$ | Object $P$ |
| Proof $p: P$ | Term $p : P$ | Morphism $p: 1 \rightarrow P$ |
| $P \Rightarrow Q$ | Function type $P \rightarrow Q$ | Exponential object $Q^P$ |
| $P \land Q$ | Product type $P \times Q$ | Product $P \times Q$ |
| $P \lor Q$ | Sum type $P + Q$ | Coproduct $P + Q$ |
| $\forall x.P(x)$ | Dependent product $\Pi x:A.P(x)$ | Right adjoint $\Pi$ |
| $\exists x.P(x)$ | Dependent sum $\Sigma x:A.P(x)$ | Left adjoint $\Sigma$ |
| True | Unit type $\top$ | Terminal object $1$ |
| False | Empty type $\bot$ | Initial object $0$ |

### 3.2 Type System Properties

| Property | Definition | Importance |
|----------|------------|------------|
| **Type Safety** | Progress + Preservation | ⭐⭐⭐⭐⭐ |
| **Strong Normalization** | All well-typed terms terminate | ⭐⭐⭐⭐⭐ |
| **Consistency** | Cannot prove False | ⭐⭐⭐⭐⭐ |
| **Expressiveness** | Can express complex mathematical structures | ⭐⭐⭐⭐ |
| **Decidability** | Type checking is decidable | ⭐⭐⭐⭐ |

---

## 4. Relations

### 4.1 Type Theory Spectrum

```mermaid
graph TB
    subgraph "Simple Types"
        ST[λ→<br/>Church 1940]
    end

    subgraph "Polymorphism"
        F[System F<br/>Girard 1972]
        Fw[System Fω<br/>Girard 1972]
    end

    subgraph "Dependent Types"
        LF[LF<br/>Harper 1987]
        MLTT[MLTT<br/>Martin-Löf 1984]
        CIC[CIC<br/>Coquand 1985]
    end

    subgraph "Modern Systems"
        COQ[Coq<br/>CIC+Induction]
        LEAN[Lean<br/>CIC+Universe]
        AGDA[Agda<br/>MLTT]
        Idris[Idris<br/>Dependent+Haskell]
    end

    subgraph "Homotopy Type Theory"
        HOTT[HoTT<br/>2013]
        CUBICAL[Cubical TT<br/>Cohen 2016]
    end

    ST --> F
    F --> Fw
    F --> LF
    LF --> MLTT
    MLTT --> CIC
    MLTT --> AGDA
    CIC --> COQ
    CIC --> LEAN
    MLTT --> Idris
    MLTT --> HOTT
    HOTT --> CUBICAL
```

### 4.2 Relations with Core Concepts

| Concept | Relation | Description |
|---------|----------|-------------|
| **Set Theory** | Alternative Foundation | Two choices for mathematical foundation |
| **Logic** | Curry-Howard | Propositions as Types, Proofs as Programs |
| **Category Theory** | Semantics | CCC Cartesian Closed Categories correspond to λ-calculus |
| **Proof Assistants** | Implementation | Coq, Lean based on type theory |
| **Programming Languages** | Application | Foundation for type system design |

---

## 5. Historical Context

### 5.1 Development Timeline

```mermaid
timeline
    title Type Theory Development History
    section 1908
        Russell : Origin of Type Theory
                : Avoiding Russell's Paradox
    section 1940
        Church : Simply Typed Lambda Calculus
               : Logical Foundation
    section 1972
        Girard : System F
               : Discovery of Polymorphism
    section 1973
        PerMartinLöf : Intuitionistic Type Theory
                     : Constructive Mathematics
    section 1985
        CoC : Calculus of Constructions
            : Foundation of Coq
    section 2006
        DT : Renaissance of Dependent Types
             : Practical Programming Applications
    section 2013
        HoTT : Homotopy Type Theory
             : New Foundations
```

### 5.2 Milestones

| Year | Figure | Contribution |
|------|--------|--------------|
| 1908 | Bertrand Russell | Type theory to avoid paradox |
| 1940 | Alonzo Church | Simply typed lambda calculus |
| 1972 | Jean-Yves Girard | Discovery of System F |
| 1973 | Per Martin-Löf | Intuitionistic type theory |
| 1985 | Thierry Coquand | Calculus of Constructions (CoC) |
| 1991 | Thierry Coquand | Calculus of Inductive Constructions (CIC) |
| 2013 | Voevodsky et al. | Homotopy Type Theory (HoTT) |

---

## 6. Formal Proofs

### 6.1 Type Safety Theorem

**Thm-S-98-01** (Type Safety). Well-typed programs cannot get stuck (no type errors):

$$\Gamma \vdash t : \tau \Rightarrow \text{Progress}(t) \land \text{Preservation}(t, \tau)$$

Where:

- **Progress**: $t$ is a value or can continue to reduce
- **Preservation**: If $t \rightarrow t'$, then $\Gamma \vdash t' : \tau$

*Proof*: By structural induction on derivation ∎

### 6.2 Strong Normalization Theorem

**Thm-S-98-02** (Strong Normalization). All well-typed terms in simply typed lambda calculus are strongly normalizing:

$$\Gamma \vdash t : \tau \Rightarrow \exists n \in \mathbb{N}, \forall \text{reduction sequences}: |\text{sequence}| \leq n$$

*Proof* (Tait Reducibility Method):

1. Define reducible term set $\text{RED}_\tau$ for type $\tau$
2. Prove all reducible terms are strongly normalizing
3. Prove all well-typed terms are reducible
4. Therefore all well-typed terms are strongly normalizing ∎

### 6.3 Curry-Howard Isomorphism Theorem

**Thm-S-98-03** (Curry-Howard). Intuitionistic propositional logic and natural deduction are isomorphic to simply typed lambda calculus:

$$\Gamma \vdash_{\text{IPL}} \varphi \quad \Leftrightarrow \quad \Gamma^* \vdash_{\lambda\rightarrow} t : \varphi^*$$

Where $^*$ is the standard translation.

*Proof*: Show one-to-one correspondence of rules ∎

---

## 7. Visualizations

### 7.1 Type Theory Concept Hierarchy

```mermaid
mindmap
  root((Type Theory))
    Simple Types
      Simply Typed λ-Calculus
      Church 1940
      Base Types
      Function Types
    Polymorphism
      System F
      Girard 1972
      Type Variables
      Universal Quantification
    Dependent Types
      Martin-Löf Type Theory
      Dependent Products Π
      Dependent Sums Σ
      Inductive Types
    Modern Proof Assistants
      Coq
      Lean
      Agda
      Idris
    Homotopy Type Theory
      Univalence Axiom
      Higher Inductive Types
      Cubical Type Theory
```

### 7.2 Curry-Howard Correspondence Diagram

```mermaid
graph TB
    subgraph "Logic"
        L1[Proposition P]
        L2[Proof p: P]
        L3[Implication P → Q]
        L4[Conjunction P ∧ Q]
    end

    subgraph "Type Theory"
        T1[Type P]
        T2[Term p : P]
        T3[Function Type P → Q]
        T4[Product Type P × Q]
    end

    subgraph "Category Theory"
        C1[Object P]
        C2[Morphism p: 1 → P]
        C3[Exponential Q^P]
        C4[Product P × Q]
    end

    L1 -.->|Propositions as Types| T1
    L2 -.->|Proofs as Terms| T2
    L3 -.->|Function Types| T3
    L4 -.->|Product Types| T4

    T1 -.->|Types as Objects| C1
    T2 -.->|Terms as Morphisms| C2
    T3 -.->|Function Objects| C3
    T4 -.->|Categorical Products| C4
```

### 7.3 Type System Evolution Tree

```mermaid
graph TD
    A[Type Theory Origins<br/>Russell 1908] --> B[Simple Types<br/>Church 1940]
    B --> C[System F<br/>Girard 1972]
    B --> D[ML Type System<br/>Milner 1978]

    C --> E[Dependent Types<br/>Martin-Löf 1973]
    C --> F[Higher-order Types<br/>Girard 1972]

    E --> G[Calculus of Constructions<br/>Coquand 1985]
    G --> H[Coq<br/>INRIA 1989]
    G --> I[Lean<br/>Microsoft 2013]

    E --> J[Agda<br/>Chalmers 1999]
    E --> K[Idris<br/>Brady 2013]

    E --> L[Homotopy Type Theory<br/>Voevodsky 2013]
    L --> M[Cubical TT<br/>Cohen 2016]

    D --> N[Hindley-Milner<br/>1978]
    N --> O[Haskell<br/>1990]
    N --> P[ML Family<br/>1973-]
    N --> Q[TypeScript<br/>2012]

    style H fill:#f9f
    style I fill:#f9f
    style O fill:#bbf
```

### 7.4 Type Checking Algorithm Flow

```mermaid
flowchart TD
    Start([Input Term]) --> Parse[Parse Term]
    Parse --> Context{Check Context}

    Context -->|Variable| VarRule{VAR Rule}
    VarRule -->|In Context| Type1[Return Type]
    VarRule -->|Not Found| Error1[Type Error]

    Context -->|Lambda| AbsRule{ABS Rule}
    AbsRule --> Extend[Extend Context]
    Extend --> CheckBody[Check Body]
    CheckBody --> BuildArrow[Build Arrow Type]

    Context -->|Application| AppRule{APP Rule}
    AppRule --> CheckFun[Check Function]
    CheckFun --> CheckArg[Check Argument]
    CheckArg --> Unify{Unify Types}
    Unify -->|Success| Type2[Return Result Type]
    Unify -->|Fail| Error2[Type Error]

    Context -->|Constant| Const[Return Constant Type]

    Type1 --> End([End])
    Type2 --> End
    BuildArrow --> End
    Const --> End
    Error1 --> End
    Error2 --> End
```

### 7.5 Dependent Type Example: Vector Length

```mermaid
graph LR
    subgraph "Dependent Type Vector"
        V0[Vec A 0]
        V1[Vec A 1]
        V2[Vec A 2]
        VN[Vec A n]
    end

    subgraph "Operations"
        Cons[cons : A → Vec A n → Vec A (n+1)]
        Head[head : Vec A (n+1) → A]
        Tail[tail : Vec A (n+1) → Vec A n]
    end

    V0 --> Cons
    Cons --> V1
    V1 --> Cons
    Cons --> V2
    V2 -.->|...| VN

    V1 --> Head
    V2 --> Head
    VN --> Head

    V1 --> Tail
    V2 --> Tail
    VN --> Tail
```

### 7.6 Type Theory Applications

```mermaid
mindmap
  root((Type Theory Applications))
    Programming Languages
      Static Type Systems
      Type Inference
      Generic Programming
      Dependent Types in Practice
    Formal Verification
      Proof Assistants
      Program Verification
      Certified Compilation
      Protocol Verification
    Mathematical Foundations
      Alternative to Set Theory
      Constructive Mathematics
      Formalized Mathematics
      Univalent Foundations
    Computer Science Theory
      Semantics of Programming Languages
      Category Theory Connections
      Computational Complexity
      Logic and Computability
```

### 7.7 Comparison: Type Theory vs Set Theory

```mermaid
graph TB
    subgraph "Type Theory"
        TT1[Construction Rules]
        TT2[Computational Content]
        TT3[Curry-Howard Correspondence]
        TT4[Constructive Logic]
        TT5[Type Checking]
    end

    subgraph "Set Theory"
        ST1[Membership Relation]
        ST2[Extensional Equality]
        ST3[Classical Logic]
        ST4[Non-computational]
        ST5[Set Membership Test]
    end

    subgraph "Common Goals"
        CG1[Mathematical Foundation]
        CG2[Formal Reasoning]
        CG3[Defining Mathematical Objects]
    end

    TT1 --> CG1
    TT2 --> CG2
    TT5 --> CG3
    ST1 --> CG1
    ST3 --> CG2
    ST5 --> CG3
```

### 7.8 Modern Type Systems Landscape

```mermaid
graph TB
    subgraph "Academic Research"
        A1[Homotopy Type Theory]
        A2[Cubical Type Theory]
        A3[Linear Type Systems]
        A4[Session Types]
    end

    subgraph "Industrial Applications"
        I1[Rust Ownership Types]
        I2[Swift Protocol Types]
        I3[Scala DOT Calculus]
        I4[TypeScript Gradual Types]
    end

    subgraph "Proof Assistants"
        P1[Coq - Mathematical Proofs]
        P2[Lean - Mathlib]
        P3[Agda - Type Theory Research]
        P4[Isabelle - Verification]
    end

    subgraph "Foundations"
        F1[Simply Typed λ-Calculus]
        F2[System F]
        F3[Dependent Type Theory]
        F4[MLTT / CIC]
    end

    F1 --> F2
    F1 --> F3
    F2 --> F4
    F3 --> F4

    F4 --> A1
    F4 --> A2
    F3 --> A3
    F3 --> A4

    F2 --> I3
    F3 --> I1
    F1 --> I4
    F2 --> I4

    F4 --> P1
    F4 --> P2
    F3 --> P3
    F1 --> P4
```

---

## 8. References

### Classic Literature









---

## 9. Related Concepts

- [Type Theory Foundations](../../01-foundations/05-type-theory.md) - More in-depth type theory formalization content
- [Curry-Howard Correspondence](08-curry-howard.md)
- [Set Theory](22-set-theory.md)
- [Category Theory](24-category-theory.md)
- [Theorem Proving](03-theorem-proving.md)

---

> **Concept Tags**: #TypeTheory #CurryHoward #ProgrammingLanguages #FormalVerification #MathematicalLogic
>
> **Learning Difficulty**: ⭐⭐⭐⭐⭐ (Expert)
>
> **Prerequisites**: Lambda Calculus, Propositional Logic, Basic Category Theory
>
> **Follow-up Concepts**: Dependent Types, Proof Assistants, Homotopy Type Theory

---

*Document Version: v1.0 | Creation Date: 2026-04-10 | Last Updated: 2026-04-10*
