# Theory-to-Implementation Static-Dynamic Mapping

> **Stage**: Knowledge/05-mapping-guides | **Prerequisites**: [Struct-to-Flink Mapping](struct-to-flink-mapping.md) | **Formalization Level**: L4-L5
> **Translation Date**: 2026-04-21

## Abstract

This document formalizes the mapping from theoretical constructs to implementation mechanisms, distinguishing static (compile-time) and dynamic (runtime) aspects of stream processing systems.

---

## 1. Definitions

### Def-K-05-15 (Static Mechanism)

**Static mechanisms** $M_{static}$ are determined at compile/configuration time:

- Type system constraints
- Operator chain topology
- Partitioning strategy
- State backend selection
- Checkpoint configuration

### Def-K-05-16 (Dynamic Mechanism)

**Dynamic mechanisms** $M_{dynamic}$ adapt at runtime:

- Backpressure control
- Dynamic resource allocation
- Adaptive checkpoint interval
- Watermark generation strategy
- Fault recovery rescheduling

### Def-K-05-17 (Static-Dynamic Mapping)

The **static-dynamic mapping** function:

$$\Psi: M_{static} \times \Sigma_{runtime} \to M_{dynamic}$$

maps static configuration and runtime state to dynamic behavior.

---

## 2. Properties

### Prop-K-05-11 (Static-Dynamic Consistency)

For any job $J$, dynamic behavior $B_J$ stays within static configuration's feasible region:

$$\forall t, B_J(t) \in \text{Feasible}(C_J)$$

### Prop-K-05-12 (Dynamic Adaptation Gain)

Adaptive mechanisms improve throughput:

$$\text{Throughput}_{adaptive} \geq \text{Throughput}_{static} \cdot (1 + \delta)$$

where $\delta \in [0.15, 0.35]$ is typical.

---

## 3. Mapping Examples

| Theoretical Concept | Static Mapping | Dynamic Mapping |
|--------------------|---------------|-----------------|
| Dataflow Graph | JobGraph (compile) | ExecutionGraph (runtime) |
| Watermark | Strategy config | Progress metric |
| State | Backend choice | Snapshot/restore |
| Parallelism | Max parallelism | Auto-scaling |
| Fault Tolerance | Checkpoint interval | Recovery trigger |

---

## 4. References
