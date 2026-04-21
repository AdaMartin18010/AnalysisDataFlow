# Process Calculus Primer

> **Stage**: Struct/01-foundation | **Prerequisites**: None | **Formalization Level**: L3-L4
> **Translation Date**: 2026-04-21

## Abstract

Foundational process algebras for modeling concurrent and distributed systems: CCS, CSP, π-calculus, and Session Types.

---

## 1. Definitions

### Def-S-02-01. CCS (Calculus of Communicating Systems)

Milner's 1980 CCS syntax:

$$
\begin{aligned}
P, Q ::= &\ 0 \quad \text{(nil)} \\
        |&\ a.P \quad \text{(prefix)} \\
        |&\ P + Q \quad \text{(choice)} \\
        |&\ P \mid Q \quad \text{(parallel)} \\
        |&\ P\backslash a \quad \text{(restriction)} \\
        |&\ P[f] \quad \text{(relabelling)}
\end{aligned}
$$

### Def-S-02-02. CSP (Communicating Sequential Processes)

Hoare's CSP with trace/failures/divergences semantics.

### Def-S-02-03. π-Calculus

Mobile processes with channel passing:

$$
P ::= 0 \mid a(x).P \mid \bar{a}\langle y \rangle.P \mid P \mid Q \mid (\nu x)P \mid !P
$$

### Def-S-02-04. Binary Session Types

Type discipline for structured communication protocols.

---

## 2. Properties

### Lemma-S-02-01 (Static Channel Topology Invariance)

CCS/CSP channels are statically scoped; topology does not change at runtime.

### Lemma-S-02-02 (Dynamic Channel Turing Completeness)

π-calculus with channel mobility is Turing-complete.

### Prop-S-02-01 (Duality Implies Compatibility)

Dual session types guarantee communication compatibility.

---

## 3. Relations

| Relation | Expression | Meaning |
|----------|-----------|---------|
| CSP ⊥ CCS | Semantically incomparable | Different equivalence relations |
| CCS ⊂ π | Strict inclusion | π extends CCS with mobility |
| Session Types ⊂ π | Typed subset | Disciplined communication |

---

## 4. References
