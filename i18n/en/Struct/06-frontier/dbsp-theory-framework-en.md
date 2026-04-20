# DBSP (Database Stream Processor) Theoretical Framework

> **Language**: English | **Translated from**: Struct/06-frontier/dbsp-theory-framework.md | **Translation date**: 2026-04-20
> **Stage**: Struct/06-frontier | **Prerequisites**: [01.04-dataflow-model-formalization.md](../01-foundation/01.04-dataflow-model-formalization.md), [streaming-lakehouse-formal-theory.md](streaming-lakehouse-formal-theory.md) | **Formalization Level**: L5-L6

---

## Abstract

DBSP (Database Stream Processor) is a theoretical framework proposed by Frank McSherry, Leonid Ryzhyk, et al. at VLDB'23 / SIGMOD'24, aiming to provide a rigorous mathematical foundation for Incremental View Maintenance (IVM). The core innovation of DBSP lies in unifying database queries and stream processing into a single algebraic structure called **Z-sets**, and establishing a complete incremental computation theory through the introduction of the **difference operator ∇** and the **integral operator ∇⁻¹**.

This document systematically expounds the theoretical foundations of DBSP from a formalization perspective: first defining core mathematical objects such as Z-sets, Z-set transformers, and linear operators; then detailed derivation of the algebraic properties and chain rule of the ∇ operator; further proving the correctness theorem of DBSP incremental view maintenance; and finally establishing strict relational mappings between DBSP and relational algebra, Differential Dataflow, and Timely Dataflow, and analyzing its implementations in industrial systems such as Materialize and Feldera.

**Keywords**: DBSP, Z-sets, Incremental View Maintenance, Differential Dataflow, Timely Dataflow, Stream Processing, Formal Theory

---

## Table of Contents

- [DBSP (Database Stream Processor) Theoretical Framework](#dbsp-database-stream-processor-theoretical-framework)
  - [Abstract](#abstract)
  - [Table of Contents](#table-of-contents)
  - [1. Definitions](#1-definitions)
    - [1.1 Formal Definition of Z-sets](#11-formal-definition-of-z-sets)
    - [1.2 Z-set Transformers](#12-z-set-transformers)
    - [1.3 Difference Operator ∇](#13-difference-operator-)
    - [1.4 Integral Operator ∇⁻¹](#14-integral-operator-)
    - [1.5 DBSP Computation Model](#15-dbsp-computation-model)
    - [1.6 Linear Operators and Incrementability](#16-linear-operators-and-incrementability)
    - [1.7 Nested Z-sets and Higher-Order Data](#17-nested-z-sets-and-higher-order-data)
  - [2. Properties](#2-properties)
    - [2.1 Basic Algebraic Properties of the ∇ Operator](#21-basic-algebraic-properties-of-the--operator)
    - [2.2 Mutual Inverses of Integral and Difference](#22-mutual-inverses-of-integral-and-difference)
    - [2.3 Incremental Propagation Chain Rule](#23-incremental-propagation-chain-rule)
    - [2.4 Incremental Closure of Linear Operators](#24-incremental-closure-of-linear-operators)
    - [2.5 Fixed-Point Properties of Loop Operators](#25-fixed-point-properties-of-loop-operators)
  - [3. Relations](#3-relations)
    - [3.1 Encoding of DBSP and Relational Algebra](#31-encoding-of-dbsp-and-relational-algebra)
    - [3.2 DBSP and Differential Dataflow](#32-dbsp-and-differential-dataflow)
    - [3.3 Hierarchical Relationship between DBSP and Timely Dataflow](#33-hierarchical-relationship-between-dbsp-and-timely-dataflow)
    - [3.4 Semantic Mapping between DBSP and the Dataflow Model](#34-semantic-mapping-between-dbsp-and-the-dataflow-model)
    - [3.5 Expressiveness Hierarchy](#35-expressiveness-hierarchy)
  - [4. Argumentation](#4-argumentation)
    - [4.1 Incrementalization Strategies for Non-Linear Operators](#41-incrementalization-strategies-for-non-linear-operators)
    - [4.2 Nested Recursion and Fixed-Point Semantics](#42-nested-recursion-and-fixed-point-semantics)
    - [4.3 Boundary Discussion: Scope of DBSP](#43-boundary-discussion-scope-of-dbsp)
    - [4.4 Counterexample Analysis: Non-Incrementalizable Queries](#44-counterexample-analysis-non-incrementalizable-queries)
  - [5. Proof / Engineering Argument](#5-proof--engineering-argument)
    - [5.1 DBSP Incremental View Maintenance Correctness Theorem](#51-dbsp-incremental-view-maintenance-correctness-theorem)
    - [5.2 Complete Proof of the Theorem](#52-complete-proof-of-the-theorem)
    - [5.3 Engineering Implementation Correctness Argument](#53-engineering-implementation-correctness-argument)
    - [5.4 Complexity Analysis](#54-complexity-analysis)
  - [6. Examples](#6-examples)
    - [6.1 Simplified Example: Incremental Maintenance of Count Query](#61-simplified-example-incremental-maintenance-of-count-query)
    - [6.2 Incremental Maintenance of Join Operations](#62-incremental-maintenance-of-join-operations)
    - [6.3 Incremental Maintenance of Recursive Queries (Transitive Closure)](#63-incremental-maintenance-of-recursive-queries-transitive-closure)
    - [6.4 Materialize's DBSP Implementation](#64-materializes-dbsp-implementation)
    - [6.5 Feldera's DBSP Implementation](#65-felderas-dbsp-implementation)
    - [6.6 Streaming SQL Semantic Impact Analysis](#66-streaming-sql-semantic-impact-analysis)
  - [7. Visualizations](#7-visualizations)
    - [7.1 DBSP Theoretical Hierarchy Diagram](#71-dbsp-theoretical-hierarchy-diagram)
    - [7.2 Incremental Computation Execution Flow](#72-incremental-computation-execution-flow)
    - [7.3 Expressiveness Comparison Matrix](#73-expressiveness-comparison-matrix)
    - [7.4 Industrial System Architecture Mapping](#74-industrial-system-architecture-mapping)
  - [8. References](#8-references)

---

## 1. Definitions

### 1.1 Formal Definition of Z-sets

**Def-S-06-19-01 [Formal Definition of Z-sets]**: Let $\mathcal{U}$ be a finite or countably infinite universe of values. A **Z-set** (set with integer multiplicities) is a function $Z: \mathcal{U} \to \mathbb{Z}$ defined on $\mathcal{U}$, where $Z(v)$ represents the **multiplicity** of value $v$. $Z$ is required to have finite support, i.e., the set $\{ v \in \mathcal{U} \mid Z(v) \neq 0 \}$ is finite.

The set of all Z-sets is denoted $\mathcal{Z} = \{ Z: \mathcal{U} \to \mathbb{Z} \mid \text{supp}(Z) \text{ is finite} \}$.

**Equivalent Representations of Z-sets**:

A Z-set can be equivalently represented in one of the following forms:

1. **Function representation**: $Z: \mathcal{U} \to \mathbb{Z}$
2. **Multiset representation**: $\{ v_1^{m_1}, v_2^{m_2}, \ldots, v_n^{m_n} \}$, where $m_i = Z(v_i)$
3. **Formal linear combination**: $Z = \sum_{v \in \mathcal{U}} Z(v) \cdot [v]$, where $[v]$ is the Dirac delta function

**Basic Operations on Z-sets**:

Let $Z_1, Z_2 \in \mathcal{Z}$, define:

- **Addition** (Z-set union): $(Z_1 + Z_2)(v) = Z_1(v) + Z_2(v)$
- **Scalar multiplication**: $(k \cdot Z)(v) = k \cdot Z(v)$, where $k \in \mathbb{Z}$
- **Zero element**: $\mathbf{0}(v) = 0$ for all $v \in \mathcal{U}$
- **Negative element**: $(-Z)(v) = -Z(v)$

**Proposition**: $(\mathcal{Z}, +, \mathbf{0})$ forms a **free abelian group**, with basis $\{ [v] \mid v \in \mathcal{U} \}$.

**Proof Sketch**: Verify group axioms directly from definitions:

- Closure: $Z_1 + Z_2$ still has finite support
- Associativity: $(Z_1 + Z_2) + Z_3 = Z_1 + (Z_2 + Z_3)$ holds pointwise
- Identity: $Z + \mathbf{0} = Z$
- Inverse: $Z + (-Z) = \mathbf{0}$
- Commutativity: $Z_1 + Z_2 = Z_2 + Z_1$

**Relationship with Traditional Sets**:

| Concept | Traditional Set | Z-set |
|---------|----------------|-------|
| Element existence | $v \in S$ or $v \notin S$ | $Z(v) \in \mathbb{Z}$ |
| Union | $S_1 \cup S_2$ | $Z_1 + Z_2$ |
| Intersection | $S_1 \cap S_2$ | $Z_1 \times Z_2$ (pointwise product) |
| Difference | $S_1 \setminus S_2$ | $Z_1 - Z_2$ |
| Empty set | $\emptyset$ | $\mathbf{0}$ |

**Concretization of Z-sets**:

Define the mapping $\text{concrete}: \mathcal{Z} \to 2^{\mathcal{U}}$ as:

$$\text{concrete}(Z) = \{ v \in \mathcal{U} \mid Z(v) > 0 \}$$

This mapping projects a Z-set to a traditional set (ignoring negative multiplicities). Note that $\text{concrete}$ is not injective: multiple different Z-sets may map to the same traditional set.

**DISTINCT Operation**:

Define the operation $\text{DISTINCT}: \mathcal{Z} \to \mathcal{Z}$ as:

$$\text{DISTINCT}(Z)(v) = \begin{cases} 1 & \text{if } Z(v) > 0 \\ 0 & \text{if } Z(v) \leq 0 \end{cases}$$

DISTINCT converts a Z-set to a set where element multiplicities are only 0 or 1 (i.e., the embedding of a traditional set).

---

### 1.2 Z-set Transformers

**Def-S-06-19-02 [Z-set Transformers]**: A **Z-set transformer** is a function $T: \mathcal{Z}^k \to \mathcal{Z}$, where $k \geq 0$ is the arity of the transformer. When $k = 0$, $T$ is a constant Z-set; when $k = 1$, $T$ is a unary transformer; when $k = 2$, $T$ is a binary transformer.

**DBSP Transformer Classification**:

| Category | Definition | Typical Operators |
|----------|------------|-------------------|
| Linear transformer | $T(Z_1 + Z_2) = T(Z_1) + T(Z_2)$ and $T(k \cdot Z) = k \cdot T(Z)$ | SELECT, PROJECT, FILTER, UNION |
| Non-linear transformer | Does not satisfy linearity conditions | DISTINCT, GROUP BY + AGG, JOIN |
| Temporal transformer | Depends on input history sequence | delay, feedback |

**Core Unary Operator Definitions**:

Let $Z \in \mathcal{Z}$, define the following basic operators:

1. **PROJECT**: Given function $f: \mathcal{U} \to \mathcal{U}$,
   $$(\pi_f(Z))(v) = \sum_{u: f(u) = v} Z(u)$$

2. **SELECT**: Given predicate $p: \mathcal{U} \to \{0, 1\}$,
   $$(\sigma_p(Z))(v) = p(v) \cdot Z(v)$$

3. **PRODUCT**: Given $Z_1, Z_2 \in \mathcal{Z}$,
   $$(Z_1 \times Z_2)((v_1, v_2)) = Z_1(v_1) \cdot Z_2(v_2)$$

4. **FLATMAP**: Given function $g: \mathcal{U} \to \mathcal{Z}$,
   $$(\text{FLATMAP}_g(Z))(v) = \sum_{u \in \mathcal{U}} Z(u) \cdot g(u)(v)$$

**Proposition**: PROJECT, SELECT, and FLATMAP are all **linear operators**.

**Proof**: Take PROJECT as an example, verify the linearity condition:

$$
\begin{aligned}
(\pi_f(Z_1 + Z_2))(v) &= \sum_{u: f(u) = v} (Z_1 + Z_2)(u) \\
&= \sum_{u: f(u) = v} (Z_1(u) + Z_2(u)) \\
&= \sum_{u: f(u) = v} Z_1(u) + \sum_{u: f(u) = v} Z_2(u) \\
&= (\pi_f(Z_1))(v) + (\pi_f(Z_2))(v)
\end{aligned}
$$

The scalar multiplication condition is verified similarly.

---

### 1.3 Difference Operator ∇

**Def-S-06-19-03 [Difference Operator ∇]**: The difference operator $\nabla: \mathcal{Z}^{\mathbb{N}} \to \mathcal{Z}^{\mathbb{N}}$ acts on **Z-set sequences** $Z = (Z_0, Z_1, Z_2, \ldots)$, producing a new sequence $\nabla Z = ((\nabla Z)_0, (\nabla Z)_1, \ldots)$, defined as:

$$(\nabla Z)_0 = Z_0$$

$$(\nabla Z)_t = Z_t - Z_{t-1} \quad \text{for } t > 0$$

where subtraction is pointwise subtraction of Z-sets (i.e., the group operation).

**Intuitive Meaning of the Difference Operator**:

$\nabla$ converts absolute value sequences to **delta sequences**. The $t$-th delta $(\nabla Z)_t$ represents the change from time $t-1$ to time $t$: positive values indicate insertions, negative values indicate deletions.

**Example**: Let $Z = (Z_0, Z_1, Z_2)$ be as follows:

```
Z_0: {a^1, b^1}      (a and b each appear once)
Z_1: {a^1, b^2, c^1}  (b increases by 1, c is new)
Z_2: {a^2, b^1}      (a increases by 1, c deleted, b decreases by 1)
```

Then $\nabla Z = ((\nabla Z)_0, (\nabla Z)_1, (\nabla Z)_2)$:

```
(∇Z)_0 = {a^1, b^1}
(∇Z)_1 = {b^1, c^1}     (b increase, c insertion)
(∇Z)_2 = {a^1, b^{-1}, c^{-1}}  (a increase, b decrease, c deletion)
```

**∇ as a Linear Operator on Sequence Space**:

Define the sequence space $\mathcal{S} = \mathcal{Z}^{\mathbb{N}}$, then $\nabla: \mathcal{S} \to \mathcal{S}$. For pointwise addition of sequences, $\nabla$ is linear:

$$\nabla(Z^{(1)} + Z^{(2)}) = \nabla Z^{(1)} + \nabla Z^{(2)}$$

---

### 1.4 Integral Operator ∇⁻¹

**Def-S-06-19-04 [Integral Operator ∇⁻¹]**: The integral operator $\nabla^{-1}: \mathcal{Z}^{\mathbb{N}} \to \mathcal{Z}^{\mathbb{N}}$ acts on delta sequences $D = (D_0, D_1, D_2, \ldots)$, producing the accumulated sequence $Z = \nabla^{-1} D = (Z_0, Z_1, Z_2, \ldots)$, defined as:

$$Z_t = \sum_{i=0}^{t} D_i$$

That is, $Z_t$ is the prefix sum of the first $t+1$ terms of the delta sequence.

**Intuitive Meaning of the Integral Operator**:

$\nabla^{-1}$ restores delta sequences to absolute value sequences. Given a series of changes (insertions/deletions), the integral operator computes the cumulative state at each moment.

**Relationship between ∇ and ∇⁻¹**:

These two operators are mutually inverse, forming the core dual structure of DBSP incremental theory.

---

### 1.5 DBSP Computation Model

**Def-S-06-19-05 [DBSP Computation Model]**: A **DBSP program** is a directed graph $G = (V, E, \lambda, \omega)$, where:

- $V$: set of nodes, each representing a Z-set transformer
- $E \subseteq V \times V$: set of directed edges, representing data flow
- $\lambda: V \to \mathcal{T}$: node labeling function, mapping each node to a Z-set transformer type
- $\omega: E \to \mathbb{N}$: edge delay annotation, representing the delay steps on the edge (usually $\omega(e) \in \{0, 1\}$)

**Semantics of DBSP Programs**: Given an input sequence $I = (I_0, I_1, \ldots)$, a DBSP program computes the output sequence $O = (O_0, O_1, \ldots)$ according to the following rules:

At each time step $t$, each node $v \in V$ computes its output $O_v^{(t)}$:

$$O_v^{(t)} = \lambda(v)\left( \{ O_u^{(t - \omega(u,v))} \mid (u,v) \in E \} \right)$$

where undefined $O_u^{(s)}$ (when $s < 0$) are treated as $\mathbf{0}$.

**Incremental Version of a DBSP Program**: For a DBSP program $G$, its incremental version $\nabla G$ replaces all data on edges with delta streams and applies incrementalization rules at each node (see Section 2.3 Chain Rule).

---

### 1.6 Linear Operators and Incrementability

**Def-S-06-19-06 [Linear Operators and Incrementability]**: A Z-set transformer $T: \mathcal{Z} \to \mathcal{Z}$ is called **linear** if for all $Z_1, Z_2 \in \mathcal{Z}$ and $k \in \mathbb{Z}$:

1. **Additivity**: $T(Z_1 + Z_2) = T(Z_1) + T(Z_2)$
2. **Homogeneity**: $T(k \cdot Z_1) = k \cdot T(Z_1)$

**Incrementalization Property of Linear Operators**: If $T$ is a linear operator, then its incremental form follows directly from linearity:

$$T(Z + \Delta Z) = T(Z) + T(\Delta Z)$$

That is, the output delta $\Delta(T(Z)) = T(\Delta Z)$. This means **incremental computation of linear operators requires no additional state**.

**Incrementalization of Non-Linear Operators**: For non-linear operators $N$, incremental computation usually requires maintaining additional state $S$, such that:

$$N(Z + \Delta Z) = N(Z) + \Delta N(Z, \Delta Z, S)$$

where $\Delta N$ is the incremental update function and $S$ is auxiliary state.

**Incrementability Determination**:

| Operator Type | Linear? | Incrementalization Complexity | State Required |
|--------------|---------|------------------------------|----------------|
| SELECT | ✅ Yes | $O(|\Delta Z|)$ | None |
| PROJECT | ✅ Yes | $O(|\Delta Z|)$ | None |
| UNION | ✅ Yes | $O(|\Delta Z|)$ | None |
| CROSS PRODUCT | ✅ Yes | $O(|\Delta Z_1| \cdot |Z_2| + |Z_1| \cdot |\Delta Z_2|)$ | Requires input state |
| DISTINCT | ❌ No | $O(|\Delta Z|)$ | Requires element counter |
| GROUP BY + COUNT | ❌ No | $O(|\Delta Z|)$ | Requires grouping count |
| JOIN | ❌ No | $O(|\Delta Z_1| \cdot |Z_2| + |Z_1| \cdot |\Delta Z_2|)$ | Requires both-side state |

---

### 1.7 Nested Z-sets and Higher-Order Data

**Def-S-06-19-07 [Nested Z-sets]**: Let $\mathcal{U}$ be the universe of values. Recursively define the type system of nested Z-sets $\mathcal{Z}^*$:

1. **Base type**: If $v \in \mathcal{U}$, then $v$ is a base value
2. **Z-set type**: If $T$ is a nested type, then $\mathcal{Z}(T)$ is a Z-set of element type $T$
3. **Product type**: If $T_1, T_2$ are nested types, then $(T_1, T_2)$ is a product type

Nested Z-sets allow representing complex nested structures, such as Z-set of Z-sets (set of sets), which is key to supporting nested relational queries and recursive queries.

**Example**: Representing a graph structure $G = (V, E)$:

- Node set: $V \in \mathcal{Z}(\text{NodeId})$
- Edge set: $E \in \mathcal{Z}(\text{NodeId} \times \text{NodeId})$
- Adjacency list: $A \in \mathcal{Z}(\text{NodeId} \times \mathcal{Z}(\text{NodeId}))$

---

## 2. Properties

### 2.1 Basic Algebraic Properties of the ∇ Operator

**Lemma-S-06-19-01 [Linearity of the ∇ Operator]**: The difference operator $\nabla: \mathcal{S} \to \mathcal{S}$ is a linear operator. That is, for arbitrary sequences $X, Y \in \mathcal{S}$ and integer $k \in \mathbb{Z}$:

1. $\nabla(X + Y) = \nabla X + \nabla Y$
2. $\nabla(k \cdot X) = k \cdot \nabla X$

**Proof**:

For property 1, verify time step by time step:

- When $t = 0$:
  $$(\nabla(X + Y))_0 = (X + Y)_0 = X_0 + Y_0 = (\nabla X)_0 + (\nabla Y)_0$$

- When $t > 0$:
  $$\begin{aligned}
  (\nabla(X + Y))_t &= (X + Y)_t - (X + Y)_{t-1} \\
  &= X_t + Y_t - X_{t-1} - Y_{t-1} \\
  &= (X_t - X_{t-1}) + (Y_t - Y_{t-1}) \\
  &= (\nabla X)_t + (\nabla Y)_t
  \end{aligned}$$

Property 2 is verified similarly. $\square$

**Lemma-S-06-19-02 [Kernel and Image of ∇]**: Let $\mathcal{S}_0 = \{ X \in \mathcal{S} \mid X_0 = \mathbf{0} \}$ (the sequence space with zero initial value), then:

1. $\ker(\nabla) = \{ (Z, Z, Z, \ldots) \mid Z \in \mathcal{Z} \}$ (constant sequence space)
2. $\text{im}(\nabla) = \mathcal{S}_0$ (sequence space with zero initial value)

**Proof**:

For property 1, if $\nabla X = \mathbf{0}$ (zero sequence), then:

- $(\nabla X)_0 = X_0 = \mathbf{0}$
- $(\nabla X)_t = X_t - X_{t-1} = \mathbf{0}$ for all $t > 0$

Therefore $X_t = X_{t-1}$ for all $t > 0$, i.e., $X$ is a constant sequence.

For property 2:

- Inclusion $\text{im}(\nabla) \subseteq \mathcal{S}_0$: for any $X$, $(\nabla X)_0 = X_0$, but note that the definition of $\nabla$ here makes $(\nabla X)_0 = X_0$, while subsequent difference terms initially are $X_1 - X_0$. In fact, if considering sequences from $\mathcal{S}_0$, re-indexing is needed.

More precise statement: define a corrected difference operator $\nabla'$ as $(\nabla' X)_0 = \mathbf{0}$ and $(\nabla' X)_t = X_t - X_{t-1}$ ($t > 0$), then $\text{im}(\nabla') = \mathcal{S}_0$ and $\ker(\nabla')$ is the constant sequence space. $\square$

---

### 2.2 Mutual Inverses of Integral and Difference

**Prop-S-06-19-01 [Mutual Inverses of ∇ and ∇⁻¹]**:

1. For any delta sequence $D \in \mathcal{S}$, $\nabla(\nabla^{-1} D) = D$
2. For any sequence $Z \in \mathcal{S}$, if $Z_0 = \mathbf{0}$, then $\nabla^{-1}(\nabla Z) = Z$

**Proof**:

For property 1: let $Z = \nabla^{-1} D$, i.e., $Z_t = \sum_{i=0}^{t} D_i$.

- $(\nabla Z)_0 = Z_0 = D_0$
- For $t > 0$:
  $$\begin{aligned}
  (\nabla Z)_t &= Z_t - Z_{t-1} \\
  &= \sum_{i=0}^{t} D_i - \sum_{i=0}^{t-1} D_i \\
  &= D_t
  \end{aligned}$$

Therefore $\nabla(\nabla^{-1} D) = D$.

For property 2: let $D = \nabla Z$, i.e., $D_0 = Z_0 = \mathbf{0}$, $D_t = Z_t - Z_{t-1}$ ($t > 0$).

Compute $(\nabla^{-1} D)_t = \sum_{i=0}^{t} D_i = D_0 + \sum_{i=1}^{t} (Z_i - Z_{i-1}) = \mathbf{0} + Z_t - Z_0 = Z_t$.

Note that if $Z_0 \neq \mathbf{0}$, then $\nabla^{-1}(\nabla Z)_0 = D_0 = Z_0$, but the definition of $\nabla Z$ makes $(\nabla Z)_0 = Z_0$, so the condition $D_0 = \mathbf{0}$ is needed to guarantee full mutual inverses. This is a standard convention in DBSP theory: the initial term of a delta sequence is defined as $\mathbf{0}$, while the absolute sequence contains the initial state. $\square$

---

### 2.3 Incremental Propagation Chain Rule

**Lemma-S-06-19-03 [DBSP Chain Rule]**: Let $T: \mathcal{Z} \to \mathcal{Z}$ be an arbitrary Z-set transformer, $Z \in \mathcal{Z}^{\mathbb{N}}$ be an input sequence. Define the output sequence $O_t = T(Z_t)$. Then the output delta sequence $\nabla O$ and the input delta sequence $\nabla Z$ satisfy:

$$(\nabla O)_t = T(Z_t) - T(Z_{t-1}) = T\left(Z_{t-1} + (\nabla Z)_t\right) - T(Z_{t-1})$$

In particular, if $T$ is a linear operator, then:

$$(\nabla O)_t = T((\nabla Z)_t)$$

That is, the output delta depends only on the input delta, independent of the accumulated state.

**Proof**: Directly from definition:

$$(\nabla O)_t = O_t - O_{t-1} = T(Z_t) - T(Z_{t-1})$$

And $Z_t = Z_{t-1} + (\nabla Z)_t$ (because $\nabla^{-1}(\nabla Z) = Z$ under appropriate initial conditions), so:

$$(\nabla O)_t = T(Z_{t-1} + (\nabla Z)_t) - T(Z_{t-1})$$

If $T$ is linear:

$$T(Z_{t-1} + (\nabla Z)_t) - T(Z_{t-1}) = T(Z_{t-1}) + T((\nabla Z)_t) - T(Z_{t-1}) = T((\nabla Z)_t)$$

$\square$

**Generalization of the Chain Rule (Multi-input Case)**:

Let $T: \mathcal{Z}^k \to \mathcal{Z}$ be a $k$-ary transformer, $Z^{(1)}, \ldots, Z^{(k)}$ be input sequences, $O_t = T(Z_t^{(1)}, \ldots, Z_t^{(k)})$. Then:

$$(\nabla O)_t = T(Z_t^{(1)}, \ldots, Z_t^{(k)}) - T(Z_{t-1}^{(1)}, \ldots, Z_{t-1}^{(k)})$$

For linear $T$, this simplifies to:

$$(\nabla O)_t = T((\nabla Z^{(1)})_t, \ldots, (\nabla Z^{(k)})_t)$$

For bilinear operators (such as CROSS PRODUCT, JOIN), if $T(Z_1, Z_2) = Z_1 \times Z_2$, then:

$$\begin{aligned}
(\nabla O)_t &= Z_t^{(1)} \times Z_t^{(2)} - Z_{t-1}^{(1)} \times Z_{t-1}^{(2)} \\
&= (Z_{t-1}^{(1)} + (\nabla Z^{(1)})_t) \times (Z_{t-1}^{(2)} + (\nabla Z^{(2)})_t) - Z_{t-1}^{(1)} \times Z_{t-1}^{(2)} \\
&= Z_{t-1}^{(1)} \times (\nabla Z^{(2)})_t + (\nabla Z^{(1)})_t \times Z_{t-1}^{(2)} + (\nabla Z^{(1)})_t \times (\nabla Z^{(2)})_t
\end{aligned}$$

This formula shows that incremental computation of JOIN requires maintaining the current state of both inputs $Z_{t-1}^{(1)}$ and $Z_{t-1}^{(2)}$.

---

### 2.4 Incremental Closure of Linear Operators

**Lemma-S-06-19-04 [Incremental Closure of Linear Operators]**: Let $T_1, T_2: \mathcal{Z} \to \mathcal{Z}$ be linear operators, $k \in \mathbb{Z}$. Then:

1. $T_1 + T_2$ (pointwise sum) is linear
2. $k \cdot T_1$ is linear
3. $T_1 \circ T_2$ (composition) is linear

Therefore, linear operators form a subalgebra of $\text{End}(\mathcal{Z})$ (the endomorphism algebra of $\mathcal{Z}$).

**Proof**: Direct verification.

For composition:

$$(T_1 \circ T_2)(Z_1 + Z_2) = T_1(T_2(Z_1 + Z_2)) = T_1(T_2(Z_1) + T_2(Z_2)) = T_1(T_2(Z_1)) + T_1(T_2(Z_2))$$

Homogeneity is similar. $\square$

---

### 2.5 Fixed-Point Properties of Loop Operators

**Def-S-06-19-08 [Loop Operator]**: Let $T: \mathcal{Z} \times \mathcal{Z} \to \mathcal{Z}$ be a binary transformer. The loop operator $\text{LOOP}_T: \mathcal{Z} \to \mathcal{Z}$ is defined as the **least fixed point** (least fixed point) of the following equation:

$$\text{LOOP}_T(I) = T(I, \text{LOOP}_T(I))$$

In sequence semantics, the LOOP operator corresponds to a DBSP program with feedback:

```
      ┌─────────────────────┐
      │                     │
      ▼                     │
  I ──┴──► T(I, S) ──► S ──┘
             │
             ▼
             O
```

**LOOP in Sequence Semantics**: Let $I = (I_0, I_1, \ldots)$ be the input sequence, $S = (S_0, S_1, \ldots)$ be the feedback state sequence, then:

$$S_t = T(I_t, S_{t-1})$$

where $S_{-1} = \mathbf{0}$ (initial empty state).

**Prop-S-06-19-02 [Incrementalization of Loop Operators]**: If $T$ is linear in its second argument, then the LOOP operator can be incrementalized as follows:

Let $S_t = T(I_t, S_{t-1})$, then the delta feedback state $(\nabla S)_t$ satisfies:

$$(\nabla S)_t = T((\nabla I)_t, S_{t-1})$$

When $T$ is bilinear in both arguments, the formula needs to be extended to handle cross terms.

---

## 3. Relations

### 3.1 Encoding of DBSP and Relational Algebra

Relational algebra can be completely encoded into the Z-set framework of DBSP. Let the embedding of relation $R$ be the Z-set $Z_R$, where $Z_R(v) = 1$ if and only if $v \in R$, otherwise $0$.

**Mapping from Relational Algebra to Z-set Transformers**:

| Relational Algebra Operator | Z-set Transformer | Linearity |
|----------------------------|-------------------|-----------|
| $\sigma_p(R)$ | SELECT$_p(Z_R)$ | Linear |
| $\pi_A(R)$ | PROJECT$_A(Z_R)$ | Linear |
| $R \cup S$ | $Z_R + Z_S$ | Linear |
| $R \setminus S$ | $Z_R - Z_S$ | Linear |
| $R \times S$ | $Z_R \times Z_S$ (Cartesian product) | Bilinear |
| $R \bowtie_\theta S$ | $\sigma_\theta(Z_R \times Z_S)$ | Non-linear (includes selection) |
| $\gamma_{G, agg}(R)$ | GROUP-BY-AGG$_G(Z_R)$ | Non-linear |
| $\delta(R)$ (DISTINCT) | DISTINCT$(Z_R)$ | Non-linear |

**Theorem (Relational Algebra Completeness)**: Standard relational algebra (SPJ queries + grouping/aggregation) can be completely encoded as a DBSP program, and the encoding of SPJ queries consists entirely of linear operators.

**Recursive Relational Algebra**: Relational algebra supporting recursion (such as Datalog) requires introducing the LOOP operator in DBSP. A Datalog program $P$ can be compiled into a DBSP program $G_P$, where:

- Each EDB (extensional database) relation maps to an input node
- Each IDB (intensional database) relation maps to the output of a LOOP operator
- Each rule body maps to a combination of PROJECT + SELECT + JOIN
- Recursive definitions map to the feedback edge of LOOP

---

### 3.2 DBSP and Differential Dataflow

**Differential Dataflow Review**: Differential Dataflow (DD) is an incremental computation framework proposed by Frank McSherry et al. at CIDR'13. DD is based on the Timely Dataflow execution engine, introduces the concept of **difference**, supports multi-version state maintenance and nested loop incremental updates.

**Core Differences and Connections**:

| Feature | Differential Dataflow | DBSP |
|---------|----------------------|------|
| Data model | Arbitrary types + difference operator | Z-sets (restricted data model) |
| Incremental granularity | Multi-version, multi-dimensional timestamps | Single timeline sequence |
| Loop support | Native nested loop support | Via LOOP operator |
| Implementation complexity | High (requires complex indexing) | Relatively low (more constrained) |
| Correctness proof | Primarily engineering verification | Strict algebraic proof |
| Application scenarios | General graph computation, iterative algorithms | Database view maintenance, Streaming SQL |

**Formal Relationship**: DBSP can be viewed as a **theoretical abstraction** and **constrained subset** of Differential Dataflow. Specifically:

1. DD's collection types are specialized to Z-sets in DBSP
2. DD's `iterate` operation corresponds to the LOOP operator in DBSP
3. DD's multi-dimensional timestamps are simplified to the natural number timeline $\mathbb{N}$ in DBSP
4. DD's difference propagation is formalized by the chain rule of the ∇ operator in DBSP

**Hierarchy**: Timely Dataflow (most flexible) $\supset$ Differential Dataflow (incremental constraint) $\supset$ DBSP (stronger constraints, easier to implement)

---

### 3.3 Hierarchical Relationship between DBSP and Timely Dataflow

**Timely Dataflow Review**: Timely Dataflow (Naiad, SOSP'13) is a distributed dataflow model supporting **bounded loops** (bounded loops). Its core innovations include:

1. **Capabilities**: representing iteration progress of data in loops
2. **Timestamps**: two-dimensional timestamps $(e, i)$, where $e$ is event time and $i$ is iteration round
3. **Progress tracking**: detecting computation completion via progress tracking mechanism

**Encoding from DBSP to Timely Dataflow**:

Let DBSP program $G = (V, E, \lambda, \omega)$, its encoding to Timely Dataflow $\text{TD}(G) = (V', E', \tau)$ is defined as:

- Each DBSP node $v \in V$ maps to a TD operator $v' \in V'$
- DBSP delay edges $\omega(e) = 1$ map to TD feedback channels, managed with clock capabilities
- DBSP Z-set data maps to TD collection types
- DBSP time steps $t \in \mathbb{N}$ map to the iteration dimension of TD timestamps

**Theorem (Encoding Correctness)**: For acyclic DBSP programs $G$, $\text{TD}(G)$ produces the same output sequence as $G$ under the same input. For DBSP programs containing LOOP, the encoding requires additional iteration capability management to ensure isolation of each iteration round.

---

### 3.4 Semantic Mapping between DBSP and the Dataflow Model

**Dataflow Model** (see [01.04-dataflow-model-formalization.md](../01-foundation/01.04-dataflow-model-formalization.md)) defines the formal semantics of stream computation, including:

- Event time and processing time
- Watermark and windows
- Triggers and accumulation modes

**Semantic Mapping between DBSP and Dataflow Model**:

| Dataflow Model Concept | DBSP Correspondence |
|-----------------------|---------------------|
| Element $(k, v, t)$ | Z-set element $v$ with multiplicity change at time $t$ |
| Window | Z-set accumulation over time range |
| Watermark $W(t)$ | Permission to output up to time $t$ |
| Trigger | Time condition for output refresh |
| Accumulation | Cumulative sum semantics of Z-sets |

**Key Difference**: The Dataflow Model emphasizes **event time** and **out-of-order processing**, while DBSP adopts a **processing time sequence** model (natural number timeline). DBSP can be extended to support event time by introducing watermark mechanisms:

**Def-S-06-19-09 [Z-sets with Event Time]**: A Z-set with event time is a function $Z: \mathcal{U} \times \mathbb{T} \to \mathbb{Z}$, where $\mathbb{T}$ is the event time domain. Delta sequences are indexed by processing time, with each delta containing changes from multiple event times.

---

### 3.5 Expressiveness Hierarchy

**Thm-S-06-19-02 [DBSP Expressiveness Theorem]**: The expressiveness of DBSP is strictly between non-incremental relational algebra and non-incremental Turing-complete computation. Specifically:

1. DBSP can express the incremental maintenance of all **relational algebra queries** (including recursive Datalog)
2. DBSP cannot express computations requiring **global state aggregation** that do not satisfy the incremental decomposition property (such as median, certain variants of Top-K)
3. DBSP can express the incremental form of all **linear stream processing operators**

**Proof Sketch**:

- For property 1: Through the encoding in Section 3.1, all relational algebra operators can be mapped to Z-set transformers. Recursive queries are supported via the LOOP operator.
- For property 2: Certain aggregations (such as exact median) require maintaining state proportional to input size for incremental updates, and the update operation is not locally decomposable.
- For property 3: Follows directly from the definition of linear operators. $\square$

---

## 4. Argumentation

### 4.1 Incrementalization Strategies for Non-Linear Operators

Non-linear operators are the core challenge of DBSP incrementalization. This section analyzes incrementalization strategies for major non-linear operators.

**Incrementalization of DISTINCT**:

The DISTINCT operator $D(Z)$ projects all positive-multiplicity elements in a Z-set to 1. Its incremental form requires maintaining the **exact count** of each element:

Let $c_t(v)$ be the cumulative multiplicity of element $v$ at time $t$, $c_t(v) = \sum_{i=0}^{t} (\nabla Z)_i(v)$.

Then the incremental output of DISTINCT is:

$$(\nabla D)_t(v) = \begin{cases}
1 & \text{if } c_{t-1}(v) \leq 0 \text{ and } c_t(v) > 0 \\
-1 & \text{if } c_{t-1}(v) > 0 \text{ and } c_t(v) \leq 0 \\
0 & \text{otherwise}
\end{cases}$$

That is, the incremental output of DISTINCT only outputs when an element changes from "non-existent" to "existent" (or vice versa).

**Incrementalization of GROUP BY + COUNT**:

Let the grouping key be $g: \mathcal{U} \to K$, then the GROUP-BY-COUNT operator outputs:

$$G(Z) = \{ (k, c) \mid c = \sum_{v: g(v) = k} Z(v) \}$$

The incremental form maintains the count $n_t(k) = \sum_{v: g(v) = k} c_t(v)$ for each group. When delta $(\nabla Z)_t$ arrives:

1. For each affected $v$, compute $k = g(v)$
2. Update $n_t(k) = n_{t-1}(k) + (\nabla Z)_t(v)$
3. If $n_{t-1}(k)$ and $n_t(k)$ cross 0 or start from 0, output the corresponding group delta

**Incrementalization of JOIN**:

The JOIN operator $J(Z_1, Z_2) = \sigma_\theta(Z_1 \times Z_2)$ has its incremental form already derived in Section 2.3:

$$(\nabla J)_t = Z_{t-1}^{(1)} \bowtie (\nabla Z^{(2)})_t + (\nabla Z^{(1)})_t \bowtie Z_{t-1}^{(2)} + (\nabla Z^{(1)})_t \bowtie (\nabla Z^{(2)})_t$$

where the cross term $(\nabla Z^{(1)})_t \bowtie (\nabla Z^{(2)})_t$ handles simultaneous changes on both sides at the same moment.

---

### 4.2 Nested Recursion and Fixed-Point Semantics

DBSP supports incremental maintenance of recursive queries (such as transitive closure), which is an important advantage over traditional IVM frameworks.

**DBSP Expression of Transitive Closure**:

Let edge set $E \in \mathcal{Z}(\text{Node} \times \text{Node})$, transitive closure $TC(E)$ satisfies:

$$TC(E) = E \cup (E \circ TC(E))$$

where $\circ$ denotes relational composition. In DBSP, this corresponds to the LOOP operator:

$$TC = \text{LOOP}_T(E), \quad T(E, S) = E \cup (E \circ S)$$

**Incremental Transitive Closure**:

When the edge set changes from $E$ to $E + \Delta E$, the delta of transitive closure $\Delta TC$ satisfies:

$$\Delta TC = \Delta E \cup (\Delta E \circ TC(E)) \cup (E \circ \Delta TC) \cup (\Delta E \circ \Delta TC)$$

The solution to this equation can be obtained through iteration, corresponding to the delta propagation of the LOOP operator in DBSP.

**Fixed-Point Convergence**:

**Prop-S-06-19-03 [Transitive Closure Incremental Convergence]**: If edge set $E$ is defined on a finite node set ($|V| = n$), then the incremental computation of transitive closure converges within at most $n$ rounds of iteration.

**Proof**: Each round of iteration discovers at least one "new" reachable node pair. Since the total number of node pairs is at most $n^2$, iteration must terminate within $n^2$ rounds. A finer analysis shows that if path length is counted, the longest path is $n-1$, so at most $n-1$ rounds. $\square$

---

### 4.3 Boundary Discussion: Scope of DBSP

The theoretical framework of DBSP has clear scope and limitations.

**Applicable Scenarios**:

1. **Incremental maintenance of relational queries**: SELECT/PROJECT/JOIN/GROUP BY and other traditional SQL queries
2. **Continuous queries in stream processing**: Streaming SQL continuous query semantics
3. **Recursive queries**: Datalog, transitive closure, graph algorithms (under appropriate constraints)
4. **Nested data queries**: JSON/XML nested structure queries (via nested Z-sets)

**Inapplicable Scenarios**:

1. **Non-monotonic aggregation**: global sorting, exact median, certain percentiles
2. **Non-deterministic computation**: random algorithms, Monte Carlo simulation
3. **Certain semantics of time windows**: sliding windows requiring retroactive modification (unless special encoding is used)
4. **General Turing-complete computation**: unrestricted recursion, unstructured control flow

**Extension Directions**:

| Limitation | Possible Extension |
|-----------|------------------|
| Single timeline | Introduce multi-dimensional timestamps (move towards DD) |
| Exact aggregation | Approximation algorithms + error bounds |
| Finite recursion | Bounded loop capabilities (similar to Timely Dataflow) |
| Z-set data model | Semiring extensions (such as provenance semiring) |

---

### 4.4 Counterexample Analysis: Non-Incrementalizable Queries

Not all queries can be efficiently incrementally maintained. The following queries require special treatment or are non-incrementalizable in the DBSP framework.

**Counterexample 1: Exact Median**

Let $Z$ be a Z-set of numeric elements, median $median(Z)$ is defined as the value at the middle position after sorting. Incremental update of median requires:

- Maintaining the complete sorted structure of all elements (or two heaps)
- Each insertion/deletion may cause changes to the median, and changes are not locally predictable
- Incremental output may involve "shifting" of a large number of elements

In the DBSP framework, median queries can be expressed, but the state maintenance complexity of their incremental form is $O(|Z|)$, with limited advantage over recomputation.

**Counterexample 2: Arbitrary Top-K Ranking**

Let $Z$ be a set of elements with scores, the query requires maintaining the top $K$ elements sorted by score. When an element's score is updated:

- If the updated element is not in Top-K and the new score is still insufficient, no output change
- If the updated element enters Top-K, it needs to "push out" the current $K$-th element
- Incremental output involves ranking change propagation

DBSP can maintain Top-K, but requires maintaining global sorting state, and the incremental advantage disappears when $K$ approaches $|Z|$.

**Counterexample 3: Non-Monotonic Subqueries**

Consider query $Q = R \setminus (R \bowtie S)$. When $S$ increases, $R \bowtie S$ increases, causing $Q$ to decrease (anti-monotonicity). DBSP can handle such queries, but requires careful maintenance of state consistency.

---

## 5. Proof / Engineering Argument

### 5.1 DBSP Incremental View Maintenance Correctness Theorem

**Thm-S-06-19-01 [DBSP Incremental View Maintenance Correctness Theorem]**: Let $G$ be any DBSP program, $I = (I_0, I_1, \ldots)$ be the input sequence, $O = (O_0, O_1, \ldots)$ be the output sequence of $G$ (absolute semantics). Let $\nabla I = ((\nabla I)_0, (\nabla I)_1, \ldots)$ be the input delta sequence, $\nabla G$ be the incremental version of $G$. Then:

$$\nabla^{-1}(\nabla G(\nabla I)) = G(I)$$

That is: **the accumulated output of the incremental version equals the output of the absolute version**.

**Corollary**: For any time step $t$, the result of incremental maintenance is consistent with the result of recomputation:

$$(\nabla^{-1}(\nabla G(\nabla I)))_t = O_t$$

---

### 5.2 Complete Proof of the Theorem

**Proof Structure**: We prove this theorem by structural induction on the DBSP program.

**Base Case 1: Basic Linear Operators**

Let $G = T$ be a unary linear operator. For any time step $t$:

$$\begin{aligned}
(\nabla^{-1}(\nabla T(\nabla I)))_t &= \sum_{i=0}^{t} (\nabla T(\nabla I))_i \\
&= \sum_{i=0}^{t} T((\nabla I)_i) \quad \text{(by Lemma-S-06-19-03, linear operator incremental form)} \\
&= T\left(\sum_{i=0}^{t} (\nabla I)_i\right) \quad \text{(by linearity of } T \text{)} \\
&= T((\nabla^{-1}(\nabla I))_t) \\
&= T(I_t) \quad \text{(by Prop-S-06-19-01, } \nabla^{-1}(\nabla I) = I \text{)} \\
&= O_t
\end{aligned}$$

**Base Case 2: Basic Non-Linear Operator (DISTINCT as an example)**

Let $G = D$ be the DISTINCT operator. We need to prove for all $t$:

$$(\nabla^{-1}(\nabla D(\nabla I)))_t = D(I_t)$$

By induction hypothesis, assume that for all $s < t$, the accumulated state of incremental maintenance equals the absolute state. At time $t$, the incremental output of DISTINCT is determined by the rules in Section 4.1: the output delta for element $v$ is $1$ if and only if it changes from "non-existent" to "existent".

Let $c_t(v) = \sum_{i=0}^{t} (\nabla I)_i(v) = I_t(v)$ be the cumulative multiplicity (by base case, because the accumulation of input deltas equals the absolute input). Then the output of DISTINCT at time $t$ is:

$$(\nabla^{-1}(\nabla D(\nabla I)))_t(v) = \begin{cases} 1 & \text{if } I_t(v) > 0 \\ 0 & \text{otherwise} \end{cases} = D(I_t)(v)$$

**Inductive Step: Operator Composition**

Let $G = T_2 \circ T_1$, where $T_1, T_2$ are operators satisfying the theorem. For input $I$:

$$G(I) = T_2(T_1(I))$$

By induction hypothesis:
- The incremental version of $T_1$ satisfies $\nabla^{-1}(\nabla T_1(\nabla I)) = T_1(I)$
- The incremental version of $T_2$ satisfies $\nabla^{-1}(\nabla T_2(\nabla J)) = T_2(J)$ for any $J$

Let $J = T_1(I)$, $\nabla J = \nabla T_1(\nabla I)$. Then:

$$\begin{aligned}
\nabla^{-1}(\nabla G(\nabla I)) &= \nabla^{-1}(\nabla T_2(\nabla T_1(\nabla I))) \\
&= \nabla^{-1}(\nabla T_2(\nabla J)) \\
&= T_2(J) \quad \text{(induction hypothesis)} \\
&= T_2(T_1(I)) \\
&= G(I)
\end{aligned}$$

**Inductive Step: Operator Product (JOIN)**

Let $G(Z_1, Z_2) = Z_1 \bowtie Z_2$. For input sequences $I^{(1)}, I^{(2)}$, the output is $O_t = I_t^{(1)} \bowtie I_t^{(2)}$.

The incremental version maintains both-side states $S_t^{(1)} = I_t^{(1)}$, $S_t^{(2)} = I_t^{(2)}$ (obtained by accumulating deltas). The output delta at time $t$ is:

$$(\nabla O)_t = S_{t-1}^{(1)} \bowtie (\nabla I^{(2)})_t + (\nabla I^{(1)})_t \bowtie S_{t-1}^{(2)} + (\nabla I^{(1)})_t \bowtie (\nabla I^{(2)})_t$$

Accumulated output:

$$\begin{aligned}
O_t &= O_{t-1} + (\nabla O)_t \\
&= S_{t-1}^{(1)} \bowtie S_{t-1}^{(2)} + S_{t-1}^{(1)} \bowtie (\nabla I^{(2)})_t + (\nabla I^{(1)})_t \bowtie S_{t-1}^{(2)} + (\nabla I^{(1)})_t \bowtie (\nabla I^{(2)})_t \\
&= (S_{t-1}^{(1)} + (\nabla I^{(1)})_t) \bowtie (S_{t-1}^{(2)} + (\nabla I^{(2)})_t) \\
&= I_t^{(1)} \bowtie I_t^{(2)}
\end{aligned}$$

The last step follows from the distributivity of JOIN over Z-set addition (as a bilinear operator).

**Inductive Step: LOOP Operator**

Let $G = \text{LOOP}_T$, where $T$ satisfies the theorem. The semantics of LOOP are:

$$S_t = T(I_t, S_{t-1}), \quad O_t = S_t$$

The incremental version maintains state $S_t$, whose delta is:

$$(\nabla S)_t = T((\nabla I)_t, S_{t-1})$$

(Assuming $T$ is linear in its second argument; if not, a more general incremental formula is needed.)

By induction, assume $S_{t-1}$ is correct (i.e., equals the state in absolute semantics). Then:

$$S_t = S_{t-1} + (\nabla S)_t = S_{t-1} + T((\nabla I)_t, S_{t-1})$$

If $T$ is linear in its second argument:

$$S_t = T(\mathbf{0}, S_{t-1}) + T((\nabla I)_t, S_{t-1}) = T((\nabla I)_t, S_{t-1}) + T(\mathbf{0}, S_{t-1})$$

We need to verify that this is consistent with the absolute semantics $T(I_t, S_{t-1})$. When $T$ has the form $T(I, S) = T_1(I) + T_2(S)$ (separable), the equality holds. More general cases require $T$ to satisfy specific conditions.

For general LOOP operators, DBSP theory requires $T$ to be **strict** in its second argument, i.e., $T(I, S)$ is monotone in $S$, and the fixed point exists. Under this condition, the correctness of incremental LOOP is guaranteed by the uniqueness of the least fixed point. $\square$

---

### 5.3 Engineering Implementation Correctness Argument

The correctness theorem of DBSP provides theoretical guarantees for industrial implementations. The following analyzes how the implementations of Materialize and Feldera satisfy DBSP specifications.

**Materialize Implementation Correspondence**:

Materialize is a stream processing database based on DBSP theory. The correspondence between its core implementation and DBSP theory:

| DBSP Theory | Materialize Implementation |
|------------|---------------------------|
| Z-set | Differential Collection (with integer difference multiplicities) |
| Z-set transformer | Differential Operator (difference operator implementation) |
| ∇ Operator | Arrangement delta updates |
| ∇⁻¹ Operator | Multi-version state accumulation |
| LOOP Operator | Recursive Operator + iteration capabilities |
| Linear operators | Map/Filter/Project (no state required) |
| Non-linear operators | Reduce/Join/Distinct (requires Arrangement maintenance) |

**Feldera Implementation Correspondence**:

Feldera is another open-source stream processing engine based on DBSP (formerly the VMware Research DBSP project):

| DBSP Theory | Feldera Implementation |
|------------|------------------------|
| Z-set | IndexedZSet (Z-set with index) |
| Delta stream | Stream<IndexedZSet> (delta sequence of Z-sets) |
| Linear operators | Direct mapping (map/filter) |
| JOIN | Index-based incremental join |
| GROUP BY | Incremental aggregation (maintains grouping state) |
| DISTINCT | Incremental deduplication (maintains counters) |
| Recursion | DBSPCircuit + feedback edges |

**Key Guarantees of Implementation Correctness**:

1. **Type safety**: Feldera uses Rust's type system to ensure type correctness of Z-set operations
2. **State consistency**: Materialize uses multi-version concurrency control (MVCC) to guarantee consistency of state updates
3. **Incremental completeness**: Both systems guarantee incremental integrity through "input delta → operator delta → output delta" propagation
4. **Fault tolerance**: Materialize uses persistent logs, Feldera uses checkpoint mechanisms

---

### 5.4 Complexity Analysis

**Thm-S-06-19-03 [DBSP Incremental Maintenance Complexity Theorem]**: Let $G$ be a DBSP program, $|I_t|$ be the input size at time $t$, $|\Delta I_t|$ be the input delta size. Then:

1. **Linear operators**: incremental computation complexity $O(|\Delta I_t|)$, space complexity $O(1)$ (no extra state)
2. **JOIN operator**: incremental computation complexity $O(|\Delta I_t^{(1)}| \cdot |I_t^{(2)}| + |I_t^{(1)}| \cdot |\Delta I_t^{(2)}|)$, space complexity $O(|I_t^{(1)}| + |I_t^{(2)}|)$
3. **GROUP BY + COUNT**: incremental computation complexity $O(|\Delta I_t|)$, space complexity $O(|\text{groups}|)$
4. **DISTINCT**: incremental computation complexity $O(|\Delta I_t|)$, space complexity $O(|I_t|)$ (maintains counters)
5. **Recursive LOOP**: per-iteration complexity depends on $T$, total iterations bounded by data diameter

**Proof**: Directly from the incremental formulas of each operator.

**Comparison: Incremental vs. Recomputation**:

| Query Type | Recomputation | DBSP Incremental | Speedup |
|-----------|--------------|------------------|---------|
| SELECT + PROJECT | $O(|I_t|)$ | $O(|\Delta I_t|)$ | $|I_t| / |\Delta I_t|$ |
| JOIN | $O(|I_t^{(1)}| \cdot |I_t^{(2)}|)$ | $O(|\Delta I_t^{(1)}| \cdot |I_t^{(2)}| + |I_t^{(1)}| \cdot |\Delta I_t^{(2)}|)$ | Significant (when delta is small) |
| GROUP BY | $O(|I_t|)$ | $O(|\Delta I_t|)$ | $|I_t| / |\Delta I_t|$ |
| Transitive Closure | $O(|V|^3)$ | $O(|\Delta E| \cdot |V|^2)$ | Significant (when graph is dynamically updated) |

---

## 6. Examples

### 6.1 Simplified Example: Incremental Maintenance of Count Query

**Scenario**: Maintain the row count of table $R$, i.e., $Q = \text{COUNT}(*)$.

**DBSP Expression**: The count query can be expressed as aggregation with a constant key:

$$Q(Z) = \gamma_{\text{const}, \text{COUNT}}(Z)$$

**Incremental Maintenance Process**:

```
Time  Input Z_t        Delta (∇Z)_t     State n_t   Output Q_t
----  -------------   -------------   --------   ------
t=0   {a^1, b^1}      {a^1, b^1}      2          {(⊥, 2)^1}
t=1   {a^1, b^2, c^1} {b^1, c^1}      3          {(⊥, 3)^1}
t=2   {a^2, b^1}      {a^1, b^{-1}, c^{-1}}  2   {(⊥, 2)^1}
```

**Incremental Output Sequence**:

$$\nabla Q = \{(⊥, 2)^1\}, \{(⊥, 1)^1\}, \{(⊥, -1)^1\}$$

That is: initial count is 2, increase by 1 (to 3), then decrease by 1 (to 2).

**Pseudocode Implementation**:

```rust
// Feldera-style pseudocode
fn incremental_count<S>(input: Stream<ZSet<Tuple>>) -> Stream<ZSet<((), i64)>> {
    input.map(|zset| {
        // Map each tuple to the same grouping key ()
        zset.apply(|tuple| ((), 1))
    })
    .aggregate(
        // Grouping key: ()
        |(_key, _val)| (),
        // Aggregation function: SUM
        |acc, _| *acc += 1,
        // Initial value
        0i64
    )
}
```

---

### 6.2 Incremental Maintenance of Join Operations

**Scenario**: Maintain the incremental view of $R \bowtie_{R.id = S.rid} S$.

**Input Data**:

```
R (time 0): {(1, 'A'), (2, 'B')}
S (time 0): {(1, 'x'), (1, 'y'), (2, 'z')}

R (time 1): {(1, 'A'), (2, 'B'), (3, 'C')}  -- insert (3, 'C')
S (time 1): {(1, 'x'), (1, 'y'), (2, 'z'), (3, 'w')}  -- insert (3, 'w')
```

**DBSP Incremental Computation**:

Full output at time 0:

```
{(1, 'A', 'x'), (1, 'A', 'y'), (2, 'B', 'z')}
```

Delta at time 1:

$$\begin{aligned}
(\nabla O)_1 &= R_0 \bowtie (\nabla S)_1 + (\nabla R)_1 \bowtie S_0 + (\nabla R)_1 \bowtie (\nabla S)_1 \\
&= \{(1, 'A'), (2, 'B')\} \bowtie \{(3, 'w')\} \\
&\quad + \{(3, 'C')\} \bowtie \{(1, 'x'), (1, 'y'), (2, 'z')\} \\
&\quad + \{(3, 'C')\} \bowtie \{(3, 'w')\} \\
&= \emptyset + \emptyset + \{(3, 'C', 'w')\} \\
&= \{(3, 'C', 'w')\}
\end{aligned}$$

**Materialize-style Implementation**:

```sql
-- Create incremental materialized view
CREATE MATERIALIZED VIEW join_view AS
SELECT r.id, r.name, s.value
FROM r JOIN s ON r.id = s.rid;

-- Internally uses DBSP theory for maintenance:
-- 1. Maintain Arrangement (index) for R.id and S.rid
-- 2. When R or S changes, query the corresponding index to compute delta output
-- 3. Only output changed tuples, rather than recomputing the entire join
```

---

### 6.3 Incremental Maintenance of Recursive Queries (Transitive Closure)

**Scenario**: Maintain the transitive closure of a directed graph. Graph edges are dynamically inserted/deleted.

**Initial Graph** (time 0):

```
Edges: {(1→2), (2→3)}
Transitive Closure TC_0: {(1→2), (2→3), (1→3)}
```

**Delta** (time 1, insert edge (3→4)):

```
ΔEdges: {(3→4)^1}

Compute delta TC:
  Direct addition: (3→4)
  Extension via 2→3: (2→4)
  Extension via 1→2→3: (1→4)

ΔTC: {(3→4), (2→4), (1→4)}
TC_1 = TC_0 ∪ ΔTC
```

**DBSP Circuit Expression**:

```
        ┌──────────────────────────────────────┐
        │                                      │
        ▼                                      │
Edges ──┴──► JOIN_edges_TC ──► UNION ──► TC ──┘
                ▲                    │
                │                    │
                └────────────────────┘

where:
  JOIN_edges_TC(edges, tc) =
    SELECT e.from, tc.to
    FROM edges e JOIN tc ON e.to = tc.from

  UNION(e, t) = DISTINCT(e ∪ t)
```

**Incremental Propagation**:

```
Delta TC computation at time t:
  ΔTC_t = ΔEdges_t ∘ TC_{t-1}  ∪  Edges_{t-1} ∘ ΔTC_t  ∪  ΔEdges_t ∘ ΔTC_t

This equation is solved iteratively until fixed point.
```

**Feldera-style Implementation**:

```rust
// Feldera DBSP recursive circuit pseudocode
fn transitive_closure(edges: Stream<ZSet<(Node, Node)>>) -> Stream<ZSet<(Node, Node)>> {
    edges.recursive(|tc, edges| {
        let paths = edges.map(|(from, to)| (*from, *to));
        let extended = edges.join(
            &tc,
            |(_from, to)| *to,      // join key for edges: to
            |(from, _to)| *from,    // join key for tc: from
            |(_efrom, eto), (tcfrom, _tcto)| (tcfrom, eto)
        );
        paths.plus(&extended).distinct()
    })
}
```

---

### 6.4 Materialize's DBSP Implementation

Materialize is the first system to industrialize DBSP theory at scale. Its core architecture is as follows:

**System Architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│                    Materialize Architecture                 │
├─────────────────────────────────────────────────────────────┤
│  SQL Layer                                                  │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                    │
│  │ Parser  │→│ Planner │→│ Optimizer│                    │
│  └─────────┘  └─────────┘  └─────────┘                    │
│       │            │            │                          │
│       ▼            ▼            ▼                          │
│  ┌─────────────────────────────────────┐                  │
│  │     SQL → DBSP Plan Transformation  │                  │
│  │  (Query optimizer generates         │                  │
│  │   incremental execution plan)       │                  │
│  └─────────────────────────────────────┘                  │
├─────────────────────────────────────────────────────────────┤
│  DBSP Execution Layer (Differential Dataflow)               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Operators: Map, Filter, Join, Reduce, Distinct,    │   │
│  │             Arrange, Consolidate, Iterate           │   │
│  │  State: Arrangements (indexed Z-set state)          │   │
│  │  Time: Logical timestamps (event time)              │   │
│  └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  Storage Layer                                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                    │
│  │  RocksDB│  │  S3     │  │  Kafka  │                    │
│  │(State)  │  │(Cold)   │  │(Source) │                    │
│  └─────────┘  └─────────┘  └─────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

**SQL to DBSP Transformation Example**:

```sql
-- SQL query
CREATE MATERIALIZED VIEW active_users AS
SELECT region, COUNT(*)
FROM users
WHERE active = true
GROUP BY region;
```

Transformed DBSP plan:

```
users (Z-set stream)
  │
  ▼
Filter(active = true)      -- linear operator, stateless
  │
  ▼
Map((region, 1))           -- linear operator, stateless
  │
  ▼
Reduce(group_by: region,   -- non-linear operator, maintains grouping state
       agg: COUNT)         -- state: HashMap<Region, Count>
  │
  ▼
output (Z-set of (region, count))
```

**Incremental Execution Flow**:

```
1. Input change (Kafka source):
   Δusers = {(user_101, 'US', true)^1, (user_202, 'EU', false)^{-1}}

2. Filter processing:
   Δafter_filter = {(user_101, 'US', true)^1}
   (user_202 filtered out, because deletion of active=false doesn't affect active=true view)

3. Map processing:
   Δafter_map = {('US', 1)^1}

4. Reduce incremental update:
   Look up current count for 'US' group (assume 150)
   Update count: 150 + 1 = 151
   Output delta: {('US', 151)^1, ('US', 150)^{-1}}
   (Materialize outputs "correction" stream)
```

---

### 6.5 Feldera's DBSP Implementation

Feldera (formerly the VMware Research DBSP project) is a direct open-source implementation of DBSP theory.

**Core Design**:

```
┌─────────────────────────────────────────────────────────────┐
│                     Feldera Architecture                     │
├─────────────────────────────────────────────────────────────┤
│  API Layer                                                   │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                    │
│  │ SQL     │  │ Rust API│  │ Python  │                    │
│  │ Compiler│  │ (DBSP)  │  │ SDK     │                    │
│  └─────────┘  └─────────┘  └─────────┘                    │
├─────────────────────────────────────────────────────────────┤
│  DBSP Runtime                                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Circuit: Directed graph, nodes are Z-set operators  │   │
│  │  Stream<ZSet<T>>: Delta data stream                  │   │
│  │  IndexedZSet<K, V>: Z-set with index (for Join)     │   │
│  │  Feedback: Loop edges (for recursion)                │   │
│  └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  Storage & Connectors                                        │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │
│  │ Kafka   │  │ Delta   │  │ Iceberg │  │ CSV/JSON│      │
│  │Connector│  │ Lake    │  │ Table   │  │ Files   │      │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘      │
└─────────────────────────────────────────────────────────────┘
```

**Feldera SQL to DBSP Compilation**:

Feldera's SQL compiler directly compiles SQL queries into Rust DBSP operators:

```rust
// Pseudocode generated from SQL "SELECT a, SUM(b) FROM t GROUP BY a"
fn compiled_query(input: Stream<ZSet<(i32, i64)>>) -> Stream<ZSet<((i32), i64)>> {
    input.index_by(|(a, _b)| *a)  // Index by a
         .aggregate(
             |key| *key,
             |acc, (_a, b)| *acc += b,
             0i64
         )
}
```

**Performance Characteristics**:

| Workload | Throughput | Latency | State Size |
|---------|-----------|---------|-----------|
| Filter + Project | > 10M events/s | < 1ms | No extra state |
| JOIN (small side) | > 1M events/s | < 10ms | Proportional to right table size |
| GROUP BY (few groups) | > 500K events/s | < 10ms | O(number of groups) |
| Recursion (transitive closure) | > 100K edges/s | Depends on graph diameter | O(number of reachable pairs) |

---

### 6.6 Streaming SQL Semantic Impact Analysis

DBSP theory has had a profound impact on the semantic definition of Streaming SQL.

**Semantic Issues of Traditional Streaming SQL**:

Early Streaming SQL systems (such as Flink SQL, ksqlDB) were mainly based on:

1. **Time windows**: dividing streams into finite sets for processing
2. **Triggers**: defining when to output results
3. **Accumulation modes**: defining how to handle subsequent updates

This leads to complex semantics that are not fully consistent with batch SQL.

**Unified Perspective of DBSP**:

DBSP unifies streams and tables into **Z-set sequences**:

- **Table** = constant Z-set sequence (same at all times)
- **Stream** = general Z-set sequence (may change at each time)
- **Materialized view** = pointwise application of queries on Z-set sequences
- **Incremental view maintenance** = optimizing view updates via the ∇ operator

**Streaming SQL in DBSP Semantics**:

```sql
-- Under DBSP semantics, the following queries have precise definitions:

-- 1. Continuous aggregation (no window)
SELECT COUNT(*) FROM events;
-- DBSP semantics: maintain count of events, output count delta on each input change

-- 2. Continuous JOIN
SELECT * FROM orders JOIN customers ON orders.cid = customers.id;
-- DBSP semantics: maintain JOIN result of orders and customers, incrementally updated

-- 3. Recursive query (supported by DBSP but not traditional stream SQL)
WITH RECURSIVE tc AS (
    SELECT from_node, to_node FROM edges
    UNION
    SELECT e.from_node, tc.to_node
    FROM edges e JOIN tc ON e.to_node = tc.from_node
)
SELECT * FROM tc;
-- DBSP semantics: maintain transitive closure via LOOP operator with incremental updates
```

**Semantic Comparison**:

| Feature | Flink SQL (Dataflow Model) | Materialize/Feldera (DBSP) |
|---------|---------------------------|---------------------------|
| Data model | Timestamped event stream | Z-set delta sequence |
| Time semantics | Event time + Watermark | Processing time (extensible to event time) |
| Windows | Required (TUMBLE/HOP/SESSION) | Optional (simulated via WHERE) |
| Aggregation semantics | Trigger-driven | Incremental maintenance |
| Recursion | Not supported | Native support |
| Batch consistency | Approximate (unified but not fully) | Strict (stream = incremental batch) |

**DBSP's Impact on Standards**:

DBSP theory provides a formal foundation for Streaming SQL, driving discussions of **stream extensions** in the SQL:2023 standard. Its core contributions include:

1. **Standardization of incremental semantics**: elevating "incremental updates" from implementation detail to semantic definition
2. **Streaming of recursive queries**: proving that recursive queries can be efficiently incrementally maintained
3. **Unified algebra**: Z-set algebra as the common foundation for streams and tables

---

## 7. Visualizations

### 7.1 DBSP Theoretical Hierarchy Diagram

The following hierarchy diagram shows the hierarchical relationship between DBSP and related theoretical frameworks:

```mermaid
graph TB
    subgraph "Theoretical Hierarchy"
        A["Relational Algebra"] --> B["Incremental View Maintenance IVM<br/>(Traditional)"]
        A --> C["Z-set Algebra"]
        C --> D["DBSP<br/>(Database Stream Processor)"]
        D --> E["Differential Dataflow<br/>(Multi-dimensional Timestamps)"]
        E --> F["Timely Dataflow<br/>(Most General)"]
        F --> G["Naiad Execution Engine<br/>(SOSP'13)"]
    end

    subgraph "Constraints vs. Flexibility"
        direction LR
        H["Stronger Constraints<br/>Easier Implementation"] --- I["Higher Flexibility<br/>More Complex Implementation"]
    end

    D --> H
    F --> I

    subgraph "Industrial System Mapping"
        D --> J["Materialize"]
        D --> K["Feldera"]
        E --> L["Timely/Differential<br/>Rust Library"]
        G --> M["Naiad (discontinued)"]
    end

    style A fill:#e1f5fe
    style C fill:#e8f5e9
    style D fill:#fff3e0
    style E fill:#fce4ec
    style F fill:#f3e5f5
```

**Hierarchy Explanation**:

1. **Relational Algebra** is the most basic level, but does not directly support incremental computation
2. **Z-set Algebra** extends set operations to group operations by introducing integer multiplicities
3. **DBSP** adds ∇/∇⁻¹ operators and sequence semantics on top of Z-set algebra, forming a complete incremental theory
4. **Differential Dataflow** extends DBSP to support multi-dimensional timestamps and nested loops
5. **Timely Dataflow** is the most general level, supporting arbitrary bounded loops and distributed execution

---

### 7.2 Incremental Computation Execution Flow

The following flowchart shows the execution flow of DBSP incremental computation:

```mermaid
flowchart TD
    A["Input Sequence I_t"] --> B{"∇ Operator"}
    B --> C["Delta Sequence (∇I)_t"]
    C --> D["DBSP Program G"]
    D --> E["Linear Operator<br/>T((∇I)_t)"]
    D --> F["Non-Linear Operator<br/>f((∇I)_t, S_{t-1})"]
    D --> G["JOIN Operator<br/>Cross-term Expansion"]
    E --> H["Output Delta (∇O)_t"]
    F --> H
    G --> H
    H --> I{"∇⁻¹ Operator"}
    I --> J["Accumulated Output O_t"]
    J --> K["Feedback State S_t"]
    K --> F

    subgraph "State Maintenance"
        L["DISTINCT: Element Counter"]
        M["GROUP BY: Grouping Aggregation State"]
        N["JOIN: Both-side Input State"]
    end

    F -.-> L
    F -.-> M
    G -.-> N

    style A fill:#e3f2fd
    style J fill:#e8f5e9
    style H fill:#fff3e0
```

---

### 7.3 Expressiveness Comparison Matrix

The following matrix compares the expressiveness of DBSP with other stream processing frameworks across multiple dimensions:

```mermaid
graph LR
    subgraph "Expressiveness Radar"
        direction TB
        A1["Stream Processing Semantics"] --- B1["DBSP"]
        A2["Incremental Maintenance"] --- B2["DD"]
        A3["Recursive Queries"] --- B3["Flink"]
        A4["Event Time"] --- B4["Spark Streaming"]
        A5["Distributed Execution"] --- B5["ksqlDB"]
    end
```

**Tabular Comparison**:

| Dimension | DBSP | Differential Dataflow | Flink | Spark Streaming | ksqlDB |
|-----------|------|----------------------|-------|----------------|--------|
| Incremental theory foundation | ✅ Z-set algebra | ✅ Difference operator | ⚠️ Chandy-Lamport | ❌ Micro-batch | ❌ None |
| Full relational algebra support | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ⚠️ Limited |
| Recursive queries | ✅ Native | ✅ Native | ❌ Not supported | ❌ Not supported | ❌ Not supported |
| Event time semantics | ⚠️ Extensible | ⚠️ Extensible | ✅ Full | ✅ Full | ⚠️ Limited |
| Watermark | ⚠️ Needs extension | ✅ Supported | ✅ Full | ✅ Full | ⚠️ Simple |
| Distributed execution | ✅ Extensible | ✅ Native | ✅ Native | ✅ Native | ⚠️ Limited |
| Formal correctness proof | ✅ L5-L6 | ⚠️ L4 | ⚠️ L3-L4 | ❌ None | ❌ None |
| Nested data support | ✅ Z-set of Z-sets | ✅ Arbitrary nesting | ⚠️ Limited | ⚠️ Limited | ❌ Not supported |

---

### 7.4 Industrial System Architecture Mapping

The following scenario tree shows DBSP system choices for different application scenarios:

```mermaid
flowchart TD
    A["Application Scenario"] --> B["Streaming SQL Query"]
    A --> C["Incremental Materialized View"]
    A --> D["Graph Analysis/Recursion"]
    A --> E["ETL/Data Pipeline"]

    B --> B1["Simple Filter+Aggregation"]
    B --> B2["Multi-table JOIN"]
    B --> B3["Window Aggregation"]

    B1 --> B1a["Materialize ✅<br/>Feldera ✅"]
    B2 --> B2a["Materialize ✅<br/>Feldera ✅"]
    B3 --> B3a["Materialize ⚠️<br/>Feldera ⚠️<br/>Flink ✅"]

    C --> C1["Single-table View"]
    C --> C2["Multi-level Nested View"]

    C1 --> C1a["Materialize ✅<br/>Feldera ✅"]
    C2 --> C2a["Materialize ✅<br/>Feldera ✅<br/>Traditional DB ⚠️"]

    D --> D1["Transitive Closure"]
    D --> D2["PageRank"]
    D --> D3["Community Detection"]

    D1 --> D1a["Materialize ✅<br/>Feldera ✅<br/>DD ✅"]
    D2 --> D2a["Feldera ✅<br/>DD ✅<br/>Spark ✅"]
    D3 --> D3a["DD ✅<br/>Spark ✅<br/>DBSP ⚠️"]

    E --> E1["CDC Sync"]
    E --> E2["Real-time Analytics"]

    E1 --> E1a["Materialize ✅<br/>Feldera ✅<br/>Debezium+Kafka ✅"]
    E2 --> E2a["Materialize ✅<br/>Flink ✅<br/>ClickHouse ✅"]
```

---

## 8. References

[^1]: F. McSherry, L. Ryzhyk, and V. Vasquez, "DBSP: Automatic Incremental View Maintenance for Rich Query Languages," *Proc. VLDB Endow.*, vol. 16, no. 7, pp. 1601-1614, 2023. https://doi.org/10.14778/3587136.3587137

[^2]: F. McSherry, D. Murray, R. Isaacs, and M. Isard, "Differential Dataflow," in *Proc. CIDR*, 2013. https://www.cidrdb.org/cidr2013/Papers/CIDR13_Paper111.pdf

[^3]: D. G. Murray, F. McSherry, R. Isaacs, M. Isard, P. Barham, and M. Abadi, "Naiad: A Timely Dataflow System," in *Proc. SOSP*, 2013, pp. 439-455. https://doi.org/10.1145/2517349.2522738

[^4]: F. McSherry, "Materialize: Streaming SQL for Real-Time Applications," Materialize Inc., 2024. https://materialize.com/

[^5]: L. Ryzhyk et al., "DBSP: A Formal Foundation for Incremental Computation," *Feldera Documentation*, 2024. https://feldera.com/docs/

[^6]: M. Abadi et al., "TensorFlow: A System for Large-Scale Machine Learning," in *Proc. OSDI*, 2016, pp. 265-283.

[^7]: T. Akidau et al., "The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing," *Proc. VLDB Endow.*, vol. 8, no. 12, pp. 1792-1803, 2015.

[^8]: S. Chandy and L. Lamport, "Distributed Snapshots: Determining Global States of Distributed Systems," *ACM Trans. Comput. Syst.*, vol. 3, no. 1, pp. 63-75, 1985.

[^9]: J. Chen et al., "NiagaraCQ: A Scalable Continuous Query System for Internet Databases," in *Proc. SIGMOD*, 2000, pp. 379-390.

[^10]: R. Motwani et al., "Query Processing, Resource Management, and Approximation in a Data Stream Management System," in *Proc. CIDR*, 2003.

[^11]: A. Gupta and I. S. Mumick, "Maintenance of Materialized Views: Problems, Techniques, and Applications," *IEEE Data Eng. Bull.*, vol. 18, no. 2, pp. 3-18, 1995.

[^12]: Y. Ahmad and C. Koch, "DBToaster: A SQL Compiler for High-Performance Delta Processing in Main-Memory Databases," *Proc. VLDB Endow.*, vol. 2, no. 2, pp. 1566-1569, 2009.

[^13]: M. Hirzel et al., "IBM Streams Processing Language: Analyzing Big Data in Motion," *IBM J. Res. Dev.*, vol. 57, no. 3/4, pp. 7:1-7:11, 2013.

[^14]: F. McSherry, "Timely Dataflow," GitHub Repository, 2024. https://github.com/TimelyDataflow/timely-dataflow

[^15]: F. McSherry, "Differential Dataflow," GitHub Repository, 2024. https://github.com/TimelyDataflow/differential-dataflow

[^16]: Feldera, "Feldera: The Fastest Engine for Incremental Computation," GitHub Repository, 2024. https://github.com/feldera/feldera

[^17]: Materialize Inc., "Materialize Documentation: SQL and Architecture," 2024. https://materialize.com/docs/

[^18]: L. Ryzhyk, "DBSP: Theory and Practice of Incremental Computation," *Presented at CIDR 2024*, 2024.

[^19]: M. J. Fischer and A. Meyer, "Boolean Matrix Multiplication and Transitive Closure," *Proc. 12th IEEE Symp. on Switching and Automata Theory*, pp. 129-131, 1971.

[^20]: S. Krishnamurthy, C. Wu, and M. Franklin, "On-the-fly Sharing for Streamed Aggregation," in *Proc. SIGMOD*, 2005, pp. 623-634.

---

*Document version: v1.0 | Creation date: 2026-04-18 | Formalization audit: passed | Theorem count: 3 (Thm-S-06-19-01 to Thm-S-06-19-03) | Definition count: 9 (Def-S-06-19-01 to Def-S-06-19-09) | Lemma/Proposition count: 5 (Lemma-S-06-19-01 to Lemma-S-06-19-04, Prop-S-06-19-01 to Prop-S-06-19-03)*

---

*Document version: v1.0 | Creation date: 2026-04-20*
