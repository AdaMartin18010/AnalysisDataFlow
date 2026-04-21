# DBSP Theory Framework

> **Stage**: Struct/06-frontier | **Prerequisites**: [Dataflow Model](dataflow-model-formalization.md) | **Formalization Level**: L5-L6
> **Translation Date**: 2026-04-21

## Abstract

Database Stream Processor (DBSP): unified theory for incremental view maintenance via Z-sets and differential operators.

---

## 1. Definitions

### Z-sets

$$Z\langle A \rangle = A \to \mathbb{Z}$$

Generalized multisets with negative multiplicities.

### Differential Operator

$$\nabla f(x) = f(x) - f(x-1)$$

### Integral Operator

$$\nabla^{-1}(\Delta y) = \sum_{i} \Delta y_i$$

---

## 2. Key Properties

| Property | Statement |
|----------|-----------|
| Linearity | $\nabla(f + g) = \nabla f + \nabla g$ |
| Chain Rule | $\nabla(g \circ f) = \nabla g \circ \nabla f$ |
| Inverse | $\nabla^{-1}(\nabla f) = f$ |

---

## 3. Relations

| System | Relation |
|--------|----------|
| SQL | DBSP encodes relational algebra |
| Differential Dataflow | DBSP generalizes to nested recursion |
| Timely Dataflow | DBSP is the theoretical foundation |

---

## 4. References
