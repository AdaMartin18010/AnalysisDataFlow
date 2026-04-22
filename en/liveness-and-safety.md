# Liveness and Safety Properties

> **Stage**: Struct/02-properties | **Prerequisites**: [Actor Model](actor-model-formalization.md) | **Formalization Level**: L3-L5
> **Translation Date**: 2026-04-21

## Abstract

Formal classification of temporal properties: safety ("nothing bad happens") and liveness ("something good eventually happens").

---

## 1. Definitions

### Safety Property

$$\text{Safety}(P) \iff \forall \sigma \in \Sigma^\omega: \sigma \models P \Rightarrow \forall i: \sigma[..i] \not\models \neg P$$

"Nothing bad ever happens." Violations are finitely observable.

### Liveness Property

$$\text{Liveness}(P) \iff \forall \sigma \in \Sigma^\omega: \exists i: \sigma[i..] \models P$$

"Something good eventually happens." Requires infinite trace analysis.

---

## 2. Properties

### Property 2.1 (Safety Closed under Union/Intersection)

Safety properties form a complete lattice under inclusion.

### Property 2.2 (Liveness Closed under Union, Not Intersection)

$$\text{Liveness}(P) \land \text{Liveness}(Q) \not\Rightarrow \text{Liveness}(P \land Q)$$

### Property 2.3 (Alpern-Schneider Decomposition)

Every property can be decomposed into safety + liveness components.

---

## 3. Verification Methods

| Property Type | Verification Method | Complexity |
|---------------|---------------------|------------|
| Safety | Runtime monitoring | Polynomial |
| Liveness | Model checking | PSPACE-complete (LTL) |
| Both | TLA+ / CTL | Varies |

---

## 4. References
