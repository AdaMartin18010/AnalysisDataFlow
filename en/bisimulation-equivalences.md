# Bisimulation Equivalences

> **Stage**: Struct/03-relationships | **Prerequisites**: [Process Calculus](process-calculus-primer.md) | **Formalization Level**: L3-L4
> **Translation Date**: 2026-04-21

## Abstract

Strong, weak, and branching bisimulation: definitions, properties, and the spectrum of process equivalences.

---

## 1. Definitions

### Def-S-15-01 (Strong Bisimulation)

Relation $R$ is a strong bisimulation if:

$$P \ R \ Q \Rightarrow \forall a: (P \xrightarrow{a} P' \Rightarrow \exists Q': Q \xrightarrow{a} Q' \land P' \ R \ Q')$$

### Def-S-15-02 (Weak Bisimulation)

As strong, but allows $\tau$-transitions: $\xrightarrow{a}$ becomes $\xrightarrow{a}^*$ (including $\tau$ sequences).

---

## 2. Equivalence Spectrum

$$
\text{Bisimulation} \subset \text{Branching Bisim} \subset \text{Weak Bisim} \subset \text{Trace Equiv}$$

| Equivalence | Preserves | Complexity |
|-------------|-----------|------------|
| Strong Bisim | All behavior | P-complete |
| Weak Bisim | Observable behavior | P-complete |
| Trace Equiv | Sequences only | PSPACE |

---

## 3. Key Theorem

### Thm-S-15-01 (Bisimulation Congruence)

Strong bisimulation is a congruence for all CCS operators.

---

## 4. References

[^1]: R. Milner, "Communication and Concurrency", Prentice Hall, 1989.
[^2]: D. Park, "Concurrency and Automata on Infinite Sequences", LNCS, 1981.
