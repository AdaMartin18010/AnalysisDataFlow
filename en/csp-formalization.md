# CSP Formalization

> **Stage**: Struct/01-foundation | **Prerequisites**: [Process Calculus Primer](process-calculus-primer.md) | **Formalization Level**: L3
> **Translation Date**: 2026-04-21

## Abstract

Formal semantics of Communicating Sequential Processes (CSP) and its relationship to Go channels.

---

## 1. Definitions

### Def-S-05-01 (CSP Core Syntax)

$$
\begin{aligned}
P ::= &\ \text{STOP} \mid \text{SKIP} \\
    |&\ a \rightarrow P \quad \text{(prefix)} \\
    |&\ P \sqcap Q \quad \text{(internal choice)} \\
    |&\ P \sqsubset Q \quad \text{(external choice)} \\
    |&\ P \parallel_A Q \quad \text{(parallel)} \\
    |&\ P \setminus A \quad \text{(hiding)} \\
    |&\ P \llbracket f \rrbracket \quad \text{(renaming)}
\end{aligned}
$$

### Def-S-05-03 (CSP Semantics Hierarchy)

| Level | Semantics | Equivalence |
|-------|-----------|-------------|
| Traces | $\text{traces}(P) \subseteq \Sigma^*$ | Weakest |
| Failures | $(s, X) \in \text{failures}(P)$ | Intermediate |
| Failures-Divergences | Includes divergence set | Strongest |

---

## 2. Properties

### Property 1 (Trace Prefix Closure)

$$s \cdot \langle a \rangle \in \text{traces}(a \rightarrow P) \Rightarrow s \in \text{traces}(P)$$

### Property 2 (Interleaving Associativity/Commutativity)

$$P \parallel_\emptyset Q = Q \parallel_\emptyset P$$
$$(P \parallel_\emptyset Q) \parallel_\emptyset R = P \parallel_\emptyset (Q \parallel_\emptyset R)$$

---

## 3. Key Theorem

### Thm-S-05-01 (Go-CS-sync to CSP Encoding Preserves Trace Equivalence)

Unbuffered Go channel programs can be encoded into CSP preserving trace semantics.

---

## 4. References
