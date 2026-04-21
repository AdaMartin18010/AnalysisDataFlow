# Petri Net Formalization

> **Stage**: Struct/01-foundation | **Prerequisites**: [Process Calculus](process-calculus-primer.md) | **Formalization Level**: L2-L4
> **Translation Date**: 2026-04-21

## Abstract

Formal foundations of Place/Transition nets, reachability, and their relationship to process calculi.

---

## 1. Definitions

### Def-S-06-01 (Place/Transition Net)

A P/T net is a tuple $N = (P, T, F, W, M_0)$ where:

- $P$: finite set of places
- $T$: finite set of transitions
- $F \subseteq (P \times T) \cup (T \times P)$: flow relation
- $W: F \to \mathbb{N}^+$: arc weights
- $M_0: P \to \mathbb{N}$: initial marking

### Def-S-06-02 (Firing Rule)

Transition $t \in T$ is **enabled** at marking $M$ if:

$$\forall p \in P: M(p) \geq W(p, t)$$

Firing produces new marking $M'$:

$$M'(p) = M(p) - W(p, t) + W(t, p)$$

---

## 2. Properties

### Property 1 (Boundedness Implies Finite State Space)

If $N$ is $k$-bounded, the reachability set has at most $(k+1)^{|P|}$ states.

### Property 4 (Liveness Implies No Dead Transitions)

$$\text{Liveness}(N) \Rightarrow \forall t \in T: \exists M: t \text{ enabled at } M$$

---

## 3. Relations

| Relation | Result |
|----------|--------|
| Petri nets vs π-calculus | Expressively incomparable |
| Bounded Petri nets vs CSP | Trace-equivalent to finite-state CSP subset |
| CPN vs Petri nets | CPN reduces to ordinary Petri nets |

---

## 4. Key Theorem

### Thm-S-06-01 (Liveness and Boundedness Decidable via Reachability Graph)

For bounded P/T nets, liveness and boundedness are decidable by reachability graph analysis.

---

## 5. References
