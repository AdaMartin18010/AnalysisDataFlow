# Liveness and Safety Properties

> **Stage**: Struct/02-properties | **Prerequisites**: [Actor Model Formalization](actor-model-formalization.md) | **Formalization Level**: L3-L5
> **Translation Date**: 2026-04-21

## Abstract

Safety and liveness are the two fundamental classes of temporal properties. Safety states that "nothing bad ever happens"; liveness states that "something good eventually happens."

---

## 1. Definitions

### 1.1 Traces and Properties

A **trace** $\sigma$ is an infinite sequence of states or events.

A **property** $P$ is a set of traces.

### Safety Property

$P$ is a **safety property** if:

$$\sigma \notin P \Rightarrow \exists \text{ finite prefix } \sigma': \forall \sigma'': \sigma'\sigma'' \notin P$$

(Any violation has a finite witness)

### Liveness Property

$P$ is a **liveness property** if:

$$\forall \text{ finite prefix } \sigma': \exists \sigma'': \sigma'\sigma'' \in P$$

(Any finite prefix can be extended to satisfy $P$)

---

## 2. Properties

### Property 2.1 (Safety is Algebraically Closed)

Safety properties are closed under union and intersection.

### Property 2.2 (Liveness is Closed Under Union)

Liveness properties are closed under union but not intersection.

### Property 2.3 (Alpern-Schneider Decomposition)

Every property can be expressed as the intersection of a safety and a liveness property.

### Property 2.4 (Fairness Hierarchy)

| Fairness | Condition | Guarantees |
|----------|-----------|------------|
| Unconditional | Every process gets infinitely many turns | Strong liveness |
| Weak | Enabled process eventually executes | Basic liveness |
| Strong | Continuously enabled process eventually executes | Stronger liveness |

---

## 3. Relations

### Relation 1: Safety $\subset$ Closed Sets (Borel Topology)

Safety properties correspond to closed sets in the trace topology.

### Relation 2: Liveness $\approx$ Dense Sets

Liveness properties correspond to dense sets.

### Relation 3: Actor Model $\subseteq$ Liveness Requires Fairness

Actor systems require fairness assumptions to guarantee liveness.

### Relation 4: Safety $\mapsto$ Runtime Monitoring, Liveness $\mapsto$ Model Checking

- Safety: can be checked at runtime (finite witnesses)
- Liveness: requires model checking or proof (infinite witnesses)

---

## 4. Theorem

### Thm-S-05-01 (Actor System Safety and Liveness Compositionality)

If actor $A$ satisfies safety property $S_A$ and actor $B$ satisfies $S_B$, then $A \parallel B$ satisfies $S_A \land S_B$.

If $A$ and $B$ satisfy liveness properties with fair scheduling, $A \parallel B$ satisfies both.

---

## 5. References

[^1]: B. Alpern & F. B. Schneider, "Defining Liveness", Information Processing Letters, 1985.
[^2]: E. A. Emerson, "Temporal and Modal Logic", Handbook of Theoretical Computer Science, 1990.
[^3]: G. A. Agha, "Actors: A Model of Concurrent Computation", MIT Press, 1986.
