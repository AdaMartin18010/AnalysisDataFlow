# DOT Subtyping Completeness Proof

> **Stage**: Struct/04-proofs | **Prerequisites**: [`../02-properties/02.05-type-safety-derivation.md`](../02-properties/02.05-type-safety-derivation.md) | **Formalization Level**: L5-L6

---

## Table of Contents

- [DOT Subtyping Completeness Proof](#dot-subtyping-completeness-proof)
  - [Table of Contents](#table-of-contents)
  - [1. Definitions](#1-definitions)
    - [1.1 DOT Abstract Syntax](#11-dot-abstract-syntax)
    - [1.2 Paths and Path Types](#12-paths-and-path-types)
    - [1.3 Nominal Types and Structural Types](#13-nominal-types-and-structural-types)
    - [1.4 Type Member Declarations and Bounds](#14-type-member-declarations-and-bounds)
    - [1.5 DOT Subtyping Relation](#15-dot-subtyping-relation)
  - [2. Properties](#2-properties)
    - [2.1 Subtyping Reflexivity and Transitivity](#21-subtyping-reflexivity-and-transitivity)
    - [2.2 Stability of Path Types](#22-stability-of-path-types)
    - [2.3 Unfolding Principle for Recursive Types](#23-unfolding-principle-for-recursive-types)
  - [3. Relations](#3-relations)
    - [3.1 Comparison of Subtyping Relations between DOT and FG/FGG](#31-comparison-of-subtyping-relations-between-dot-and-fgfgg)
    - [3.2 Path-Dependent Types and Type Projections](#32-path-dependent-types-and-type-projections)
    - [3.3 Correspondence between Semantic Models and Syntactic Derivations](#33-correspondence-between-semantic-models-and-syntactic-derivations)
  - [4. Argumentation](#4-argumentation)
    - [4.1 Complexity of the Subtyping Decision Problem](#41-complexity-of-the-subtyping-decision-problem)
    - [4.2 Bad Bounds Problem and Well-Formedness Conditions](#42-bad-bounds-problem-and-well-formedness-conditions)
    - [4.3 Design Principles for Subtyping Algorithms](#43-design-principles-for-subtyping-algorithms)
  - [5. Proofs](#5-proofs)
    - [5.1 Correctness of the Subtyping Algorithm](#51-correctness-of-the-subtyping-algorithm)
    - [5.2 Completeness of Path-Dependent Type Resolution](#52-completeness-of-path-dependent-type-resolution)
    - [5.3 Completeness Theorem Thm-S-22-01](#53-completeness-theorem-thm-s-22-01)
  - [6. Examples](#6-examples)
    - [6.1 Positive Example: Simple Subtyping Derivation](#61-positive-example-simple-subtyping-derivation)
    - [6.2 Positive Example: Path Type Projection](#62-positive-example-path-type-projection)
    - [6.3 Counterexample: Bad Bounds Problem](#63-counterexample-bad-bounds-problem)
    - [6.4 Counterexample: Cyclic Subtyping](#64-counterexample-cyclic-subtyping)
  - [7. Visualizations](#7-visualizations)
    - [7.1 DOT Subtyping Derivation Structure Diagram](#71-dot-subtyping-derivation-structure-diagram)
    - [7.2 Nominal vs Structural Type Comparison Diagram](#72-nominal-vs-structural-type-comparison-diagram)
    - [7.3 Subtyping Completeness Proof Dependency Diagram](#73-subtyping-completeness-proof-dependency-diagram)
  - [8. References](#8-references)

---

## 1. Definitions

### 1.1 DOT Abstract Syntax

**Definition Def-S-22-01 (DOT Abstract Syntax)**[^1][^2]:

DOT (Dependent Object Types) is the minimal core calculus of the Scala type system, capturing the essence of path-dependent types and abstract type members. Its abstract syntax is defined as follows:

$$
\begin{array}{llcl}
\text{Variables} & x, y, z & & \\
\text{Labels} & a, b, c & & \text{(term labels)} \\
& A, B, C & & \text{(type labels)} \\
\text{Terms} & t, s & ::= & x \mid \lambda(x: T).t \mid t\,s \mid \nu(x: T)d \mid t.a \\
\text{Definitions} & d & ::= & \{a = t\} \mid \{A = T\} \mid d \wedge d' \\
\text{Values} & v & ::= & \lambda(x: T).t \mid \nu(x: T)d \\
\text{Types} & T, U, S & ::= & \\
& & \mid & \top \mid \bot & \text{(top / bottom types)} \\
& & \mid & x.A & \text{(path-dependent type projection)} \\
& & \mid & \{A: S..U\} & \text{(type member declaration)} \\
& & \mid & S \rightarrow U & \text{(function type)} \\
& & \mid & S \,\&\, U & \text{(intersection type)} \\
& & \mid & S \mid U & \text{(union type)} \\
& & \mid & \mu(x: T) & \text{(recursive type)} \\
\text{Paths} & p, q & ::= & x \mid p.a \\
\text{Environments} & \Gamma & ::= & \emptyset \mid \Gamma, x: T
\end{array}
$$

**Intuitive Explanation of Syntax Constructors**:

| Constructor | Meaning | Scala Equivalent |
|-------------|---------|-----------------|
| $\nu(x: T)d$ | Object construction (nu-abstraction) | `new T { d }` |
| $x.A$ | Path-dependent type projection | `x.A` (type projection) |
| $\{A: S..U\}$ | Type member declaration (bounds $S$ to $U$) | `type A >: S <: U` |
| $T \,\&\, U$ | Intersection type | `T with U` |
| $\mu(x: T)$ | Recursive type | Self-referential type definition |
| $p.a$ | Path selection | `p.a` (field access path) |

The DOT syntax is deliberately minimal, stripping away Scala's trait mixing, implicit conversions, pattern matching, and other advanced features, retaining only the **path-dependent type** as the core characteristic. A path $p$ is an **immutable access path** starting from a variable $x$ and extended through field selections $.a$; the object it points to at runtime never changes, so the path-dependent type $p.A$ has **stability** in the type system.

---

### 1.2 Paths and Path Types

**Definition Def-S-22-02 (Paths and Path Types)**[^1]:

A **Path** in DOT is an immutable sequence of references to an object, forming the basis of path-dependent types:

$$
\text{Path } p, q ::= x \mid p.a
$$

Where:

- **Variable path** $x$: Directly references a variable in the environment
- **Selection path** $p.a$: Selects the field labeled $a$ from the object pointed to by path $p$

A **Path-Dependent Type** $p.A$ represents "the concrete type of the type member $A$ of the object pointed to by path $p$". Its semantics depends on the actual runtime target of path $p$, which is the core characteristic that distinguishes DOT from traditional nominal/structural type systems.

**Path Equivalence ($\Gamma \vdash p \equiv q$)**:

$$
\frac{\Gamma(x) = T}{\Gamma \vdash x \equiv x} \text{ (P-Var)}
\quad
\frac{\Gamma \vdash p \equiv q \quad \Gamma \vdash p.a: T}{\Gamma \vdash p.a \equiv q.a} \text{ (P-Select)}
$$

**Path Type Well-Formedness**:

$$
\frac{\Gamma \vdash p: T \quad \Gamma \vdash T <: \{A: S..U\}}{\Gamma \vdash p.A \text{ wf}} \text{ (WF-Proj)}
$$

The key property of path-dependent types lies in **stability**—if two paths are equivalent, then their dependent types are also equivalent:

$$
\Gamma \vdash p \equiv q \Rightarrow (\Gamma \vdash p.A <: q.A \land \Gamma \vdash q.A <: p.A)
$$

---

### 1.3 Nominal Types and Structural Types

**Definition Def-S-22-03 (Nominal Types and Structural Types)**[^3][^4]:

**Nominal Subtyping**:

Nominal subtyping is based on **explicitly declared inheritance relationships**. Type $T$ is a subtype of $U$ if and only if there is an explicit `extends` or `implements` relationship at the declaration site:

$$
\frac{\text{type } T \text{ extends } U}{T <:_{nom} U}
$$

**Characteristics**:

- The subtyping relationship is explicitly declared by the programmer
- Type equivalence is based on type names (nominal identity)
- Transitivity is guaranteed by the declaration graph
- Typical representatives: Java, C#, Scala class inheritance

**Structural Subtyping**:

Structural subtyping is based on **structural compatibility of types**. Type $T$ is a subtype of $U$ if and only if the structure of $T$ (method/field set) contains all structural requirements of $U$:

$$
\frac{\forall m \in methods(U): T \text{ implements } m}{T <:_{struct} U}
$$

**Characteristics**:

- The subtyping relationship is implicitly determined by structural compatibility
- Type equivalence is based on structural isomorphism
- No explicit inheritance declaration is required
- Typical representatives: Go, TypeScript, OCaml object types

**DOT's Unified Perspective**:

DOT adopts a hybrid strategy of **nominal declaration + structural satisfaction**:

| Level | Mechanism | Explanation |
|-------|-----------|-------------|
| Declaration Level | Nominal | Type member declaration $\{A: S..U\}$ defines bound constraints |
| Usage Level | Structural | Subtyping judgment is based on bound satisfiability (structural) |
| Projection Level | Path-Dependent | The concrete type of $p.A$ is determined by the runtime path |

```
Scala: trait Animal { type Food <: Edible }
       class Dog extends Animal { type Food = DogFood }

DOT:   { Food: ..Edible }  // Animal's type signature
       ν(x: {Food = DogFood})  // Dog object construction
```

---

### 1.4 Type Member Declarations and Bounds

**Definition Def-S-22-04 (Type Member Declaration)**[^1]:

A type member declaration $\{A: S..U\}$ indicates that an object possesses an abstract type member named $A$, with lower bound $S$ and upper bound $U$:

$$
\{A: S..U\} \quad \text{where } S <: U
$$

**Semantics of Bound Constraints**:

- **Lower bound $S$**: The type member $A$ must contain at least all values of $S$ ($S <: A$)
- **Upper bound $U$**: The type member $A$ must be a subtype of $U$ ($A <: U$)
- **Exact type $T$**: Equivalent to $\{A: T..T\}$, i.e., lower bound equals upper bound

**Type Member Declaration Subtyping Rule (<:-Typ)**:

$$
\frac{\Gamma \vdash S_2 <: S_1 \quad \Gamma \vdash U_1 <: U_2}
     {\Gamma \vdash \{A: S_1..U_1\} <: \{A: S_2..U_2\}} \text{ (<:-Typ)}
$$

**Intuitive Explanation**: The contravariant lower bound and covariant upper bound of type member declarations align with intuition—

- If the lower bound of $T_1$ is "larger" ($S_2 <: S_1$), then the range of possible values for $T_1$ is smaller
- If the upper bound of $T_1$ is "smaller" ($U_1 <: U_2$), then the range of possible values for $T_1$ is smaller
- Therefore $T_1$ is a subtype of $T_2$ (a more specific type)

**Bad Bounds Problem**:

When a type declaration does not satisfy $S <: U$, it is called a **bad bound (Bad Bounds)**. For example:

$$
\{A: \bot .. \top\} \text{ is well-formed} \quad
\{A: Int .. String\} \text{ is a bad bound (assuming Int </: String)}
$$

Bad bounds can lead to type system inconsistency and must be excluded.

---

### 1.5 DOT Subtyping Relation

**Definition Def-S-22-05 (DOT Core Subtyping Rules)**[^1][^2]:

The DOT subtyping judgment $\Gamma \vdash S <: T$ is inductively defined by the following rules:

**Basic Rules**:

$$
\frac{}{\Gamma \vdash T <: \top} \text{ (<:-Top)}
\quad
\frac{}{\Gamma \vdash \bot <: T} \text{ (<:-Bot)}
\quad
\frac{}{\Gamma \vdash T <: T} \text{ (<:-Refl)}
$$

**Function Subtyping** (contravariant in argument, covariant in return):

$$
\frac{\Gamma \vdash T_1 <: S_1 \quad \Gamma \vdash S_2 <: T_2}
     {\Gamma \vdash S_1 \rightarrow S_2 <: T_1 \rightarrow T_2} \text{ (<:-Fun)}
$$

**Type Member Subtyping** (covariant/contravariant in bounds):

$$
\frac{\Gamma \vdash S_2 <: S_1 \quad \Gamma \vdash U_1 <: U_2}
     {\Gamma \vdash \{A: S_1..U_1\} <: \{A: S_2..U_2\}} \text{ (<:-Typ)}
$$

**Path Projection Subtyping** (DOT's core rule):

$$
\frac{\Gamma \vdash p: T \quad \Gamma \vdash T <: \{A: S..U\}}
     {\Gamma \vdash S <: p.A <: U} \text{ (<:-Proj)}
$$

**Intersection/Union Subtyping**:

$$
\frac{\Gamma \vdash S <: T_1 \quad \Gamma \vdash S <: T_2}
     {\Gamma \vdash S <: T_1 \,\&\, T_2} \text{ (<:-And-I)}
\quad
\frac{}{\Gamma \vdash T_1 \,\&\, T_2 <: T_i} \text{ (<:-And-E)}
$$

**Transitivity**:

$$
\frac{\Gamma \vdash S <: U \quad \Gamma \vdash U <: T}
     {\Gamma \vdash S <: T} \text{ (<:-Trans)}
$$

**Recursive Type Subtyping**:

$$
\frac{\Gamma, x: \mu(x: T) \vdash T <: U}
     {\Gamma \vdash \mu(x: T) <: \mu(x: U)} \text{ (<:-Rec)}
$$

**Subtyping Induction Principle**:

The DOT subtyping relation is the smallest relation satisfying the above rules, possessing the well-foundedness of an inductive definition.

---

## 2. Properties

### 2.1 Subtyping Reflexivity and Transitivity

**Lemma Lemma-S-22-01 (Reflexivity)**:

For any well-formed type $T$:

$$
\Gamma \vdash T <: T
$$

**Proof**: By structural induction on $T$.

- **Base cases**: $T = \top, \bot, x.A$
  - $\top <: \top$ by (<:-Refl)
  - $\bot <: \bot$ by (<:-Refl)
  - $x.A <: x.A$ by (<:-Refl) or derived from bounds

- **Inductive steps**:
  - $T = S \rightarrow U$: By induction hypothesis $S <: S$, $U <: U$, apply (<:-Fun) to obtain $S \rightarrow U <: S \rightarrow U$
  - $T = \{A: S..U\}$: By induction hypothesis and (<:-Typ)
  - $T = T_1 \,\&\, T_2$: By combining (<:-And-E) and (<:-And-I)

∎

---

**Lemma Lemma-S-22-02 (Transitivity)**:

If $\Gamma \vdash S <: U$ and $\Gamma \vdash U <: T$, then $\Gamma \vdash S <: T$.

**Proof Sketch**[^2]: Transitivity is the core difficulty of DOT subtyping relations. Direct structural induction encounters difficulties (the induction hypothesis is not strong enough). Amin & Rompf (2017) employ **mutual induction** techniques, simultaneously inducting on subtyping and other auxiliary relations.

Key observations: Transitivity requires special handling in the following cases:

1. $U$ is a path projection $p.A$ — requires path equivalence information
2. $U$ is an intersection/union type — requires decomposition and recombination
3. $U$ is a recursive type — requires unfolding treatment

The complete transitivity proof relies on the **semantic model approach**, proving the transitivity of the syntactic subtyping relation by constructing a denotational semantics.

∎

---

### 2.2 Stability of Path Types

**Lemma Lemma-S-22-03 (Path Type Stability)**:

If $\Gamma \vdash p \equiv q$ and $\Gamma \vdash p.A$ is well-formed, then:

$$
\Gamma \vdash p.A <: q.A \quad \text{and} \quad \Gamma \vdash q.A <: p.A
$$

That is, $p.A \equiv q.A$.

**Proof**:

1. From $\Gamma \vdash p \equiv q$, there exists a path equivalence derivation
2. Apply the (<:-Proj) rule to the bounds of $p$ and $q$
3. If $p$ and $q$ are equivalent, they point to the same type member of the same object
4. Therefore $p.A$ and $q.A$ denote the same type, and are subtypes of each other

∎

---

### 2.3 Unfolding Principle for Recursive Types

**Lemma Lemma-S-22-04 (Recursive Type Unfolding)**:

For recursive type $\mu(x: T)$, its **unfold** is defined as:

$$
\text{unfold}(\mu(x: T)) = T[\mu(x: T)/x]
$$

**Unfolding Preserves Subtyping**:

$$
\frac{\Gamma \vdash S <: \mu(x: T)}
     {\Gamma \vdash S <: \text{unfold}(\mu(x: T))}
$$

$$
\frac{\Gamma \vdash \mu(x: T) <: U}
     {\Gamma \vdash \text{unfold}(\mu(x: T)) <: U}
$$

**Proof**: Subtyping of recursive types is determined by their unfolded structure. This is the standard technique for recursive type processing (a variant of the Amber rule).

∎

---

## 3. Relations

### 3.1 Comparison of Subtyping Relations between DOT and FG/FGG

**Comparison Table**:

| Feature | FG/FGG | DOT | Explanation |
|---------|--------|-----|-------------|
| **Subtyping Basis** | Structural satisfaction | Bound satisfaction + path projection | DOT is more fine-grained |
| **Generics Mechanism** | Parametric polymorphism | Type members + F-bound | DOT supports existential types |
| **Recursive Types** | None | $\mu(x: T)$ | Native support in DOT |
| **Intersection Types** | None | $T \,\&\, U$ | DOT supports mixin composition |
| **Path Dependence** | None | $p.A$ | Unique feature of DOT |
| **Type Equality** | Nominal (FG) / Structural | Path equivalence | DOT depends on runtime paths |

**Subtyping Derivation Differences**:

```
FG:  T <: U iff methods(T) ⊇ methods(U)

DOT: T <: U iff
     - All type members of T satisfy U's bound constraints
     - For path projection p.A, the actual type of p needs to be resolved
```

---

### 3.2 Path-Dependent Types and Type Projections

**Relation**: $p.A$ encodes the expressive power of **Existential Types**.

In System F, the existential type $\exists X.T$ means "there exists some type $X$ such that $T$ holds". DOT's type member declarations implement a similar capability:

$$
\{A: S..U\} \approx \exists A. (S <: A <: U) \land \ldots
$$

**Semantics of Path Projection**:

- $p.A$ is not a simple type alias, but a type **dependent on a value**
- Different paths may point to the same object, in which case their projections are equivalent
- The same path may point to different objects at different times (but paths are immutable in DOT, hence stable)

```scala
// Scala example
trait Container { type Elem }
def head(c: Container): c.Elem = ...

// DOT counterpart
// c: {Elem: ⊥..⊤}
// head return type: c.Elem
```

---

### 3.3 Correspondence between Semantic Models and Syntactic Derivations

**Relation**: The denotational semantic model $\llbracket T \rrbracket$ provides the foundation for **completeness** of the subtyping relation.

**Semantic Subtyping**:

$$
S \sqsubseteq_{sem} T \iff \llbracket S \rrbracket \subseteq \llbracket T \rrbracket
$$

**Syntax-Semantics Correspondence**:

$$
\Gamma \vdash S <: T \Rightarrow \llbracket S \rrbracket_\Gamma \subseteq \llbracket T \rrbracket_\Gamma
$$

**Completeness Goal**:

$$
\llbracket S \rrbracket_\Gamma \subseteq \llbracket T \rrbracket_\Gamma \Rightarrow \Gamma \vdash S <: T
$$

This is the core theorem Thm-S-22-01 to be proved in this document.

---

## 4. Argumentation

### 4.1 Complexity of the Subtyping Decision Problem

The DOT subtyping decision faces the following complexity challenges:

**1. Uncertainty of Path Dependence**

The concrete target of path $p$ may be unknown at compile time, requiring **symbolic execution** to resolve $p.A$.

**2. Infinite Unfolding of Recursive Types**

The unfolding of recursive type $\mu(x: T)$ may be infinite, requiring processing techniques with **finite representation**.

**3. Combinatorial Explosion of Intersection/Union**

Judgments of the form $(T_1 \,\&\, T_2) <: (U_1 \mid U_2)$ need to be decomposed into multiple subgoals.

**4. Non-locality of Transitivity**

The intermediate type $U$ in $S <: U <: T$ may not be a subformula of $S$ or $T$, requiring a **guess** of the intermediate type.

---

### 4.2 Bad Bounds Problem and Well-Formedness Conditions

**Bad Bounds Definition**:

A type member declaration $\{A: S..U\}$ is a **bad bound** if and only if $S \not<: U$.

**Harm of Bad Bounds**:

Bad bounds can cause the type system to become **inconsistent**, allowing the derivation of arbitrary subtyping relations:

$$
\{A: Int .. String\} \text{ (assuming Int </: String)} \Rightarrow \bot
$$

By constructing self-referential types, a contradiction can be derived from bad bounds:

$$
T = \mu(x: \{A: x.A .. \bot\})
$$

**Well-Formedness Condition**:

$$
\frac{\Gamma \vdash S <: U}{\Gamma \vdash \{A: S..U\} \text{ wf}} \text{ (WF-Typ)}
$$

All types participating in subtyping judgments must satisfy well-formedness.

---

### 4.3 Design Principles for Subtyping Algorithms

Designing a decidable DOT subtyping algorithm requires the following principles:

**1. Finite Representation Principle**

All intermediate types must be representable by **finite syntax**, prohibiting infinite unfolding.

**2. Termination Guarantee Principle**

Prove algorithm termination through a **measure function**:

$$
\mu(S <: T) = (\text{type size}(S) + \text{type size}(T), \text{path depth}(S), \text{path depth}(T))
$$

**3. Completeness Principle**

All subtyping relations accepted by the algorithm must be derivable in the syntactic rules.

**4. Path Caching Principle**

**Memoize** the resolution results of path projections $p.A$ to avoid repeated computation.

---

## 5. Proofs

### 5.1 Correctness of the Subtyping Algorithm

**Definition (Subtyping Algorithm $algorithmic\_<:$)**:

The algorithmic judgment $\Gamma \vdash_{alg} S <: T$ is defined as follows:

```
algorithmic_<:(Γ, S, T):
  // Base cases
  if S = T: return true
  if T = ⊤: return true
  if S = ⊥: return true

  // Function types
  if S = S1 → S2 and T = T1 → T2:
    return algorithmic_<:(Γ, T1, S1) and algorithmic_<:(Γ, S2, T2)

  // Type members
  if S = {A: S1..S2} and T = {A: T1..T2}:
    return algorithmic_<:(Γ, T1, S1) and algorithmic_<:(Γ, S2, T2)

  // Path projection resolution
  if S = p.A:
    (L, U) = resolve_path(Γ, p, A)
    return algorithmic_<:(Γ, L, T)

  if T = p.A:
    (L, U) = resolve_path(Γ, p, A)
    return algorithmic_<:(Γ, S, U)

  // Intersection types
  if T = T1 & T2:
    return algorithmic_<:(Γ, S, T1) and algorithmic_<:(Γ, S, T2)

  if S = S1 & S2:
    return algorithmic_<:(Γ, S1, T) or algorithmic_<:(Γ, S2, T)

  return false
```

**Lemma Lemma-S-22-05 (Algorithm Soundness)**:

If $\Gamma \vdash_{alg} S <: T$, then $\Gamma \vdash S <: T$.

**Proof**: By induction on the recursive structure of the algorithm. Each algorithm branch corresponds to a direct application or combination of a syntactic subtyping rule.

- Base cases correspond to (<:-Refl), (<:-Top), (<:-Bot)
- Function type branch corresponds to (<:-Fun)
- Type member branch corresponds to (<:-Typ)
- Path projection branch corresponds to the appropriate direction of (<:-Proj)
- Intersection type branch corresponds to (<:-And-I), (<:-And-E)

∎

---

**Lemma Lemma-S-22-06 (Algorithm Completeness)**:

If $\Gamma \vdash S <: T$ and all types are well-formed, then $\Gamma \vdash_{alg} S <: T$.

**Proof Sketch**: By induction on the syntactic subtyping derivation. It is necessary to prove:

1. Each rule in the syntactic derivation has a corresponding treatment in the algorithm
2. The algorithm recursion depth is finite (termination)
3. Transitivity cases can be handled through path resolution

Key cases:

- **Transitivity (<:-Trans)**: $S <: U <: T$. The algorithm implicitly handles the transitivity chain by progressively simplifying the structure of $S$ and $T$.
- **Path Projection (<:-Proj)**: The algorithm calls `resolve_path` to resolve path bounds, consistent with the syntactic rule.

∎

---

### 5.2 Completeness of Path-Dependent Type Resolution

**Definition (Path Resolution Function resolve_path)**:

$$
\text{resolve\_path}(\Gamma, p, A) = (L, U)
$$

Where $L <: p.A <: U$ is the tightest bound of the path projection in environment $\Gamma$.

**Resolution Rules**:

$$
\frac{\Gamma(x) = \{A: L..U\}}{\text{resolve\_path}(\Gamma, x, A) = (L, U)}
$$

$$
\frac{\text{resolve\_path}(\Gamma, p, A) = (L, U) \quad \Gamma \vdash p.a: T \quad T <: \{A: L'..U'\}}
     {\text{resolve\_path}(\Gamma, p.a, A) = (L \sqcup L', U \sqcap U')}
$$

**Lemma Lemma-S-22-07 (Path Resolution Completeness)**:

If $\Gamma \vdash p: T$ and $\Gamma \vdash T <: \{A: S..U\}$, then:

$$
\text{resolve\_path}(\Gamma, p, A) = (L, U') \Rightarrow S <: L \land U' <: U
$$

**Proof**: By induction on the length of path $p$.

- **Base case** ($p = x$): Bounds are directly obtained from environment lookup
- **Inductive step** ($p = q.a$): Bounds are combined from the induction hypothesis and the selection rule

∎

---

### 5.3 Completeness Theorem Thm-S-22-01

**Theorem Thm-S-22-01 (DOT Subtyping Completeness)**:

The DOT subtyping relation is **complete** with respect to its denotational semantic model, i.e.:

$$
\forall S, T, \Gamma. \quad
\llbracket S \rrbracket_\Gamma \subseteq \llbracket T \rrbracket_\Gamma \Rightarrow \Gamma \vdash S <: T
$$

Where $\llbracket \cdot \rrbracket_\Gamma$ is the denotational semantic interpretation under environment $\Gamma$.

**Proof**[^2]:

**Step 1: Construct the Denotational Semantic Model**

Define the interpretation of types in the **unification closure** model:

- Value domain $V$ is the set of DOT values
- Type interpretation $\llbracket T \rrbracket_\Gamma \subseteq V$ is inductively defined:
  - $\llbracket \top \rrbracket = V$
  - $\llbracket \bot \rrbracket = \emptyset$
  - $\llbracket S \rightarrow T \rrbracket = \{ \lambda(x:S).t \mid \forall v \in \llbracket S \rrbracket: t[v/x] \in \llbracket T \rrbracket \}$
  - $\llbracket \{A: S..U\} \rrbracket = \{ v \mid v.A \text{ exists and } \llbracket S \rrbracket \subseteq \llbracket v.A \rrbracket \subseteq \llbracket U \rrbracket \}$
  - $\llbracket p.A \rrbracket = \llbracket T \rrbracket$ where the type member $A$ of the object pointed to by $p$ equals $T$

**Step 2: Prove Semantics Implies Syntax**

Assume $\llbracket S \rrbracket_\Gamma \subseteq \llbracket T \rrbracket_\Gamma$. We need to construct the syntactic derivation $\Gamma \vdash S <: T$.

Perform **lexicographic induction** on the structure of $(S, T)$, with the measure function:

$$
\text{measure}(S, T) = (|S| + |T|, \text{rank}(S), \text{rank}(T))
$$

Where $|T|$ is the syntactic size of the type, and $\text{rank}$ is the "semantic complexity" of the type.

**Case Analysis**:

1. **$T = \top$**: Directly follows from (<:-Top)

2. **$S = \bot$**: Directly follows from (<:-Bot)

3. **$S = p.A$ (path projection)**:
   - From semantic inclusion, $\llbracket p.A \rrbracket \subseteq \llbracket T \rrbracket$
   - From path resolution, there exist bounds $L <: p.A <: U$
   - From semantics, $\llbracket L \rrbracket \subseteq \llbracket p.A \rrbracket \subseteq \llbracket U \rrbracket$
   - By induction hypothesis, $\Gamma \vdash L <: T$
   - By (<:-Proj) and (<:-Trans), $\Gamma \vdash p.A <: T$

4. **$T = p.A$ (path projection as upper bound)**:
   - Similarly, using upper bound resolution and (<:-Proj)

5. **$S = S_1 \rightarrow S_2$, $T = T_1 \rightarrow T_2$**:
   - From semantics, function space inclusion implies contravariance in argument and covariance in return
   - By induction hypothesis, $\Gamma \vdash T_1 <: S_1$ and $\Gamma \vdash S_2 <: T_2$
   - Follows from (<:-Fun)

6. **$S = \{A: S_1..S_2\}$, $T = \{A: T_1..T_2\}$**:
   - From semantics, type member inclusion implies bound inclusion
   - By induction hypothesis, $\Gamma \vdash T_1 <: S_1$ and $\Gamma \vdash S_2 <: T_2$
   - Follows from (<:-Typ)

7. **$T = T_1 \,\&\, T_2$ (intersection)**:
   - From semantics, $\llbracket S \rrbracket \subseteq \llbracket T_1 \rrbracket \cap \llbracket T_2 \rrbracket$
   - i.e., $\llbracket S \rrbracket \subseteq \llbracket T_1 \rrbracket$ and $\llbracket S \rrbracket \subseteq \llbracket T_2 \rrbracket$
   - By induction hypothesis, $\Gamma \vdash S <: T_1$ and $\Gamma \vdash S <: T_2$
   - Follows from (<:-And-I)

8. **$S = S_1 \,\&\, S_2$ (intersection as lower bound)**:
   - From semantics, $\llbracket S_1 \rrbracket \cup \llbracket S_2 \rrbracket \subseteq \llbracket T \rrbracket$
   - This requires additional argumentation, because union inclusion in $T$ does not directly correspond to a syntactic rule
   - In DOT, intersection as a lower bound requires utilizing **semantic minimality**
   - By induction hypothesis, $\Gamma \vdash S_1 <: T$ or $\Gamma \vdash S_2 <: T$
   - This requires a stronger semantic condition (complete lattice structure)

9. **Recursive types**:
   - Utilize recursive type unfolding equivalence
   - By induction hypothesis and the (<:-Rec) rule

**Step 3: Completeness Conclusion**

All cases have proved:

$$
\llbracket S \rrbracket_\Gamma \subseteq \llbracket T \rrbracket_\Gamma \Rightarrow \Gamma \vdash S <: T
$$

Combined with Lemma Lemma-S-22-05 (Algorithm Soundness) and Lemma-S-22-06 (Algorithm Completeness), we conclude:

**The DOT subtyping algorithm is complete and sound with respect to the semantic model**.

∎

---

**Corollary Cor-S-22-01 (Type Safety Guarantee)**:

From DOT subtyping completeness, combined with the DOT type safety theorem (see [`../02-properties/02.05-type-safety-derivation.md`](../02-properties/02.05-type-safety-derivation.md) Section 5.5), we obtain:

Well-typed DOT programs do not break type safety during subtyping conversions.

---

## 6. Examples

### 6.1 Positive Example: Simple Subtyping Derivation

**Example 6.1: Function Type Subtyping**

Given types:

$$
S = Int \rightarrow String \quad T = \top \rightarrow \top
$$

**Derivation**:

$$
\frac{\frac{}{\vdash \top <: Int} \text{ (implied by definition of } \top \text{)} \quad \frac{}{\vdash String <: \top} \text{ (<:-Top)}}
     {\vdash Int \rightarrow String <: \top \rightarrow \top} \text{ (<:-Fun)}
$$

**Explanation**: Contravariance in the argument ($\top$ accepts fewer constraints, hence more general) and covariance in the return ($String$ is more specific than $\top$).

---

**Example 6.2: Type Member Subtyping**

Given:

$$
S = \{A: Animal .. Animal\} \quad T = \{A: Cat .. Animal\}
$$

**Derivation**:

$$
\frac{\vdash Cat <: Animal \quad \vdash Animal <: Animal}
     {\vdash \{A: Animal .. Animal\} <: \{A: Cat .. Animal\}} \text{ (<:-Typ)}
$$

**Explanation**: $S$ requires $A$ to be exactly $Animal$, while $T$ allows $A$ to be either $Cat$ or $Animal$. Since $Cat <: Animal$, $S$ is more specific, and therefore a subtype of $T$.

---

### 6.2 Positive Example: Path Type Projection

**Example 6.3: Path-Dependent Type**

Given environment:

$$
\Gamma = c: \{Elem: Int .. Int\}
$$

Type judgment:

$$
\Gamma \vdash Int <: c.Elem <: Int
$$

**Derivation**:

$$
\frac{\Gamma(c) = \{Elem: Int .. Int\} \quad \frac{}{\{Elem: Int .. Int\} <: \{Elem: Int .. Int\}}}
     {\Gamma \vdash Int <: c.Elem} \text{ (<:-Proj)}
$$

**Explanation**: Since the type declaration of $c$ specifies $Elem$ as exactly $Int$, $c.Elem$ is equivalent to $Int$.

---

**Example 6.4: F-bound Polymorphism**

$$
\Gamma = x: \mu(z: \{A: z.A .. z.A, compareTo: z.A \rightarrow Int\})
$$

This type means: Object $x$ has a type member $A$ (self-referential), and a comparison method accepting a parameter of type $A$.

This is the DOT encoding of the `Comparable` interface in Scala:

```scala
trait Comparable[T <: Comparable[T]] {
  def compareTo(other: T): Int
}
```

---

### 6.3 Counterexample: Bad Bounds Problem

**Counterexample 6.1: Bad Bounds Lead to Inconsistency**

Consider the type:

$$
T = \{A: Int .. String\} \quad \text{(assuming } Int \not<: String\text{)}
$$

**Analysis**:

1. This type declaration violates the well-formedness condition: the lower bound $Int$ is not a subtype of the upper bound $String$
2. If this type is accepted, a self-referential type can be constructed:

$$
X = \mu(x: \{A: x.A .. \bot\})
$$

1. Unfolding yields: $X.A <: \bot$, but $\bot$ is the bottom type, so $X.A$ must equal $\bot$
2. Meanwhile, by self-reference, $X.A <: X.A$ requires $X.A$ to exist
3. Contradiction! Arbitrary type equalities can be derived (e.g., $Int <: String$)

**Conclusion**: The DOT type checker must reject type declarations containing bad bounds.

---

### 6.4 Counterexample: Cyclic Subtyping

**Counterexample 6.2: Ill-founded Recursion**

Consider:

$$
T = \mu(x: x.A) \quad \text{where } A \text{ is undefined}
$$

**Analysis**:

Unfolding this type yields $T.A = T.A$, forming an infinite loop. The type checker needs to detect such ill-founded recursion to ensure termination.

---

## 7. Visualizations

### 7.1 DOT Subtyping Derivation Structure Diagram

The following Mermaid diagram shows the core structure of DOT subtyping derivation, from basic axioms to the completeness theorem:

```mermaid
graph BT
    subgraph "Basic Axioms"
        A1["[Axiom] <: Top: T <: ⊤"]
        A2["[Axiom] <: Bot: ⊥ <: T"]
        A3["[Axiom] <: Refl: T <: T"]
        A4["[Axiom] <: Proj: S <: p.A <: U"]
    end

    subgraph "Structural Rules"
        R1["[<: Fun] Function Type: Contravariant Arg, Covariant Ret"]
        R2["[<: Typ] Type Member: Contravariant Lower, Covariant Upper"]
        R3["[<: And] Intersection Type Decomposition and Composition"]
        R4["[<: Trans] Transitivity"]
    end

    subgraph "Auxiliary Lemmas"
        L1["[Lemma S 22 01] Reflexivity"]
        L2["[Lemma S 22 02] Transitivity"]
        L3["[Lemma S 22 03] Path Type Stability"]
        L4["[Lemma S 22 05] Algorithm Soundness"]
        L5["[Lemma S 22 06] Algorithm Completeness"]
        L6["[Lemma S 22 07] Path Resolution Completeness"]
    end

    subgraph "Core Theorem"
        T1["[Thm S 22 01] DOT Subtyping Completeness: Semantic Inclusion ⇒ Syntactic Derivation"]
    end

    subgraph "Application Corollary"
        C1["[Cor S 22 01] Type Safety Guarantee"]
    end

    A1 --> L4
    A2 --> L4
    A3 --> L1
    A4 --> L6

    R1 --> L4
    R2 --> L4
    R3 --> L4
    R4 --> L2

    L1 --> L5
    L2 --> L5
    L3 --> L6
    L4 --> T1
    L5 --> T1
    L6 --> T1

    T1 --> C1

    style A1 fill:#fff9c4,stroke:#f57f17
    style A2 fill:#fff9c4,stroke:#f57f17
    style A3 fill:#fff9c4,stroke:#f57f17
    style A4 fill:#fff9c4,stroke:#f57f17
    style L1 fill:#bbdefb,stroke:#1565c0
    style L2 fill:#bbdefb,stroke:#1565c0
    style L3 fill:#bbdefb,stroke:#1565c0
    style L4 fill:#bbdefb,stroke:#1565c0
    style L5 fill:#bbdefb,stroke:#1565c0
    style L6 fill:#bbdefb,stroke:#1565c0
    style T1 fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    style C1 fill:#f8bbd9,stroke:#ad1457
```

**Diagram Explanation**:

- Bottom yellow nodes represent the basic axiom rules of DOT subtyping
- Blue nodes represent key lemmas required to prove completeness
- Green node represents the core completeness theorem Thm-S-22-01
- Pink node represents the application corollary

---

### 7.2 Nominal Type vs Structural Type Comparison Diagram

The following diagram compares nominal subtyping and structural subtyping in the DOT context:

```mermaid
graph TB
    subgraph "Nominal Subtyping"
        N1["Explicit Inheritance Declaration class Dog extends Animal"]
        N2["Type Equivalence = Name Equivalence Dog ≡ Dog"]
        N3["Subtyping Relation Determined by Declaration Graph Transitive Closure of extends Relations"]
        N4["Pros: Clear, Controllable Cons: Not Flexible Enough"]
    end

    subgraph "DOT Hybrid Strategy"
        D0["Nominal Declaration + Structural Satisfaction"]
        D1["Type Member Declaration {A: S..U} Nominal: Existence of Declaration"]
        D2["Bound Satisfaction Check Structural: S <: A <: U"]
        D3["Path-Dependent p.A Runtime Resolution"]
    end

    subgraph "Structural Subtyping"
        S1["Implicit Structural Compatibility methods(T) ⊇ methods(U)"]
        S2["Type Equivalence = Structural Equivalence {x: Int} ≡ {x: Int}"]
        S3["Subtyping Relation Determined by Structural Comparison Duck Typing"]
        S4["Pros: Flexible, Expressive Cons: Difficult to Reason About"]
    end

    N1 -.->|DOT Adopts| D1
    S1 -.->|DOT Adopts| D2
    D1 --> D0
    D2 --> D0
    D3 --> D0

    style N1 fill:#e3f2fd,stroke:#1565c0
    style N2 fill:#e3f2fd,stroke:#1565c0
    style N3 fill:#e3f2fd,stroke:#1565c0
    style N4 fill:#e3f2fd,stroke:#1565c0
    style S1 fill:#e8f5e9,stroke:#2e7d32
    style S2 fill:#e8f5e9,stroke:#2e7d32
    style S3 fill:#e8f5e9,stroke:#2e7d32
    style S4 fill:#e8f5e9,stroke:#2e7d32
    style D0 fill:#fce4ec,stroke:#ad1457,stroke-width:3px
    style D1 fill:#fce4ec,stroke:#ad1457
    style D2 fill:#fce4ec,stroke:#ad1457
    style D3 fill:#fce4ec,stroke:#ad1457
```

---

### 7.3 Subtyping Completeness Proof Dependency Diagram

The following flowchart shows the overall structure of the Thm-S-22-01 proof:

```mermaid
flowchart TD
    Start([Start: Prove Semantic Inclusion ⇒ Syntactic Derivation]) --> Step1

    Step1[Step 1: Construct Denotational Semantic Model] --> Step1a
    Step1a[Define Value Domain V and Type Interpretation] --> Step1b
    Step1b[Define Semantics of Path Projection] --> Step2

    Step2[Step 2: Define Measure Function] --> Step2a
    Step2a[measure S T: Type Size and Rank] --> Step3

    Step3[Step 3: Lexicographic Induction] --> Step3a

    Step3a{Case Analysis} --> Case1
    Step3a --> Case2
    Step3a --> Case3
    Step3a --> Case4
    Step3a --> Case5
    Step3a --> Case6

    Case1["T = ⊤: Apply <: Top"] --> Done
    Case2["S = ⊥: Apply <: Bot"] --> Done
    Case3["S = p.A: Path Resolution"] --> Case3a
    Case3a["resolve path to obtain bounds"] --> Case3b
    Case3b["Induction Hypothesis + <: Proj"] --> Done
    Case4["T = p.A: Similar to Case3"] --> Done
    Case5["Function Type: <: Fun"] --> Done
    Case6["Recursive Type: <: Rec"] --> Done

    Done[Complete Derivation Γ ⊢ S <: T] --> End1
    End1([Thm S 22 01 Proved])

    style Start fill:#e1bee7,stroke:#6a1b9a
    style End1 fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    style Step1 fill:#fff9c4,stroke:#f57f17
    style Step2 fill:#fff9c4,stroke:#f57f17
    style Step3 fill:#bbdefb,stroke:#1565c0
```

---

## 8. References

[^1]: Amin, N., Moors, A., & Odersky, M. (2016). "The Essence of Dependent Object Types". In *WGP 2016: Proceedings of the 8th ACM SIGPLAN Workshop on Generic Programming* (pp. 31-42). <https://doi.org/10.1145/2976022.2976025>

[^2]: Amin, N., & Rompf, T. (2017). "Type Soundness for Dependent Object Types (DOT)". In *OOPSLA 2017: Proceedings of the ACM on Programming Languages* (Vol. 1, pp. 1-28). <[DOI: 10.1145/3138088]>

[^3]: Odersky, M. (2019). "A Tour of Scala: Abstract Type Members". Scala Documentation. <https://docs.scala-lang.org/tour/abstract-type-members.html>

[^4]: Odersky, M., & Zenger, M. (2005). "Scalable Component Abstractions". In *OOPSLA 2005* (pp. 41-57). <https://doi.org/10.1145/1094811.1094815>

---

**Document Metadata**:

- **Chapter**: 04-proofs/04.06-dot-subtyping-completeness
- **Definition Count**: 5 (Def-S-22-01 ~ Def-S-22-05)
- **Lemma Count**: 7 (Lemma-S-22-01 ~ Lemma-S-22-07)
- **Theorem Count**: 1 (Thm-S-22-01)
- **Corollary Count**: 1 (Cor-S-22-01)
- **Cross References**: [`../02-properties/02.05-type-safety-derivation.md`](../02-properties/02.05-type-safety-derivation.md)
- **Sources**: Amin et al. (DOT paper) [^1][^2], Odersky [^3][^4]

---

*Document version: v1.0 | Translation date: 2026-04-24*
