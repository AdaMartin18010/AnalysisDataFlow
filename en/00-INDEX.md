# AnalysisDataFlow — English Document Index

> **Language**: English | **Last Updated**: 2026-04-22
> **Total Documents**: 153 | **New This Round**: 25 (TECH-STACK)

---

## Core Translated Documents

### Struct / Formal Theory

| Document | Source | Description | Formality |
|----------|--------|-------------|-----------|
| [struct-unified-streaming-theory.md](./struct-unified-streaming-theory.md) | [Struct/01-foundation/01.01-unified-streaming-theory.md](../Struct/01-foundation/01.01-unified-streaming-theory.md) | Unified Streaming Meta-Model (USTM) | L6 |
| [process-calculus-primer.md](./process-calculus-primer.md) | [Struct/01-foundation/01.02-process-calculus-primer.md](../Struct/01-foundation/01.02-process-calculus-primer.md) | CCS, CSP, π-Calculus, Session Types | L3-L4 |
| [csp-formalization.md](./csp-formalization.md) | [Struct/01-foundation/01.05-csp-formalization.md](../Struct/01-foundation/01.05-csp-formalization.md) | CSP Semantics & Go Channel Encoding | L3 |
| [actor-to-csp-encoding.md](./actor-to-csp-encoding.md) | [Struct/03-relationships/03.01-actor-to-csp-encoding.md](../Struct/03-relationships/03.01-actor-to-csp-encoding.md) | Actor-to-CSP Formal Encoding | L3 |
| [flink-to-process-calculus.md](./flink-to-process-calculus.md) | [Struct/03-relationships/03.02-flink-to-process-calculus.md](../Struct/03-relationships/03.02-flink-to-process-calculus.md) | Flink Dataflow to π-Calculus | L5 |
| [time-semantics.md](./time-semantics.md) | [Knowledge/01-concept-atlas/01.02-time-semantics.md](../Knowledge/01-concept-atlas/01.02-time-semantics.md) | Event/Processing/Ingestion Time | L3-L4 |
| [state-management-concepts.md](./state-management-concepts.md) | [Knowledge/01-concept-atlas/01.04-state-management-concepts.md](../Knowledge/01-concept-atlas/01.04-state-management-concepts.md) | State Types & Backends | L3-L4 |
| [consistency-hierarchy.md](./consistency-hierarchy.md) | [Struct/02-properties/02.02-consistency-hierarchy.md](../Struct/02-properties/02.02-consistency-hierarchy.md) | Consistency Levels | L5 |
| [watermark-monotonicity-theorem.md](./watermark-monotonicity-theorem.md) | [Struct/02-properties/02.03-watermark-monotonicity.md](../Struct/02-properties/02.03-watermark-monotonicity.md) | Watermark Monotonicity | L5 |
| [liveness-and-safety.md](./liveness-and-safety.md) | [Struct/02-properties/02.04-liveness-and-safety.md](../Struct/02-properties/02.04-liveness-and-safety.md) | Liveness & Safety | L3-L5 |
| [chandy-lamport-snapshot-proof.md](./chandy-lamport-snapshot-proof.md) | [Struct/04-proofs/04.03-chandy-lamport-consistency.md](../Struct/04-proofs/04.03-chandy-lamport-consistency.md) | Snapshot Consistency Proof | L5 |
| [struct-to-flink-mapping.md](./struct-to-flink-mapping.md) | [Knowledge/05-mapping-guides/struct-to-flink-mapping.md](../Knowledge/05-mapping-guides/struct-to-flink-mapping.md) | Theory-to-Implementation Map | L4-L5 |
| [iot-stream-processing-pattern.md](./iot-stream-processing-pattern.md) | [Knowledge/03-business-patterns/iot-stream-processing.md](../Knowledge/03-business-patterns/iot-stream-processing.md) | IoT Stream Processing | L4-L5 |
| [petri-net-formalization.md](./petri-net-formalization.md) | [Struct/01-foundation/01.06-petri-net-formalization.md](../Struct/01-foundation/01.06-petri-net-formalization.md) | Petri Nets | L2-L4 |
| [streaming-database-formalization.md](./streaming-database-formalization.md) | [Struct/01-foundation/01.08-streaming-database-formalization.md](../Struct/01-foundation/01.08-streaming-database-formalization.md) | Streaming Database Model | L5 |
| [edge-streaming-semantics.md](./edge-streaming-semantics.md) | [Struct/01-foundation/01.09-edge-streaming-semantics.md](../Struct/01-foundation/01.09-edge-streaming-semantics.md) | Edge Stream Processing | L5 |
| [schema-evolution-formalization.md](./schema-evolution-formalization.md) | [Struct/01-foundation/01.10-schema-evolution-formalization.md](../Struct/01-foundation/01.10-schema-evolution-formalization.md) | Schema Evolution | L5 |
| [dbsp-differential-dataflow.md](./dbsp-differential-dataflow.md) | [Struct/01-foundation/01.11-dbsp-differential-dataflow.md](../Struct/01-foundation/01.11-dbsp-differential-dataflow.md) | DBSP Theory | L5-L6 |
| [minimal-session-types-theory.md](./minimal-session-types-theory.md) | [Struct/01-foundation/minimal-session-types-theory.md](../Struct/01-foundation/minimal-session-types-theory.md) | Minimal Session Types | L5-L6 |
| [stream-processing-semantics-formalization.md](./stream-processing-semantics-formalization.md) | [Struct/01-foundation/stream-processing-semantics-formalization.md](../Struct/01-foundation/stream-processing-semantics-formalization.md) | Stream Semantics | L5-L6 |
| [streaming-axiomatic-system.md](./streaming-axiomatic-system.md) | [Struct/01-foundation/streaming-axiomatic-system.md](../Struct/01-foundation/streaming-axiomatic-system.md) | Axiomatic System | L6 |
| [streaming-database-formal-definition.md](./streaming-database-formal-definition.md) | [Struct/01-foundation/streaming-database-formal-definition.md](../Struct/01-foundation/streaming-database-formal-definition.md) | SDB Formal Definition | L5-L6 |
| [expressiveness-hierarchy.md](./expressiveness-hierarchy.md) | [Struct/03-relationships/03.03-expressiveness-hierarchy.md](../Struct/03-relationships/03.03-expressiveness-hierarchy.md) | Expressiveness Hierarchy | L3-L6 |
| [bisimulation-equivalences.md](./bisimulation-equivalences.md) | [Struct/03-relationships/03.04-bisimulation-equivalences.md](../Struct/03-relationships/03.04-bisimulation-equivalences.md) | Bisimulation | L3-L4 |
| [cross-model-mappings.md](./cross-model-mappings.md) | [Struct/03-relationships/03.05-cross-model-mappings.md](../Struct/03-relationships/03.05-cross-model-mappings.md) | Cross-Model Mappings | L5-L6 |
| [flink-distributed-architecture.md](./flink-distributed-architecture.md) | [Struct/03-relationships/03.06-flink-distributed-architecture.md](../Struct/03-relationships/03.06-flink-distributed-architecture.md) | Flink Architecture | L5-L6 |
| [three-layer-relationship.md](./three-layer-relationship.md) | [Struct/03-relationships/03.07-three-layer-relationship-comprehensive.md](../Struct/03-relationships/03.07-three-layer-relationship-comprehensive.md) | Three-Layer Relationship | L3-L5 |
| [expressiveness-hierarchy-supplement.md](./expressiveness-hierarchy-supplement.md) | [Struct/03-relationships/03.03-expressiveness-hierarchy-supplement.md](../Struct/03-relationships/03.03-expressiveness-hierarchy-supplement.md) | Hierarchy Supplement | L3-L5 |
| [theorem-dependency-proof-tree.md](./theorem-dependency-proof-tree.md) | [Struct/03-relationships/03.08-theorem-dependency-proof-tree.md](../Struct/03-relationships/03.08-theorem-dependency-proof-tree.md) | Theorem Dependency Graph | L5-L6 |
| [flink-checkpoint-correctness-proof.md](./flink-checkpoint-correctness-proof.md) | [Struct/04-proofs/04.01-flink-checkpoint-correctness.md](../Struct/04-proofs/04.01-flink-checkpoint-correctness.md) | Checkpoint Correctness | L5 |
| [flink-exactly-once-correctness-proof.md](./flink-exactly-once-correctness-proof.md) | [Struct/04-proofs/04.02-flink-exactly-once-correctness.md](../Struct/04-proofs/04.02-flink-exactly-once-correctness.md) | Exactly-Once Correctness | L5 |
| [watermark-algebra-proof.md](./watermark-algebra-proof.md) | [Struct/04-proofs/04.04-watermark-algebra-formal-proof.md](../Struct/04-proofs/04.04-watermark-algebra-formal-proof.md) | Watermark Algebra | L5 |
| [fg-fgg-type-safety-proof.md](./fg-fgg-type-safety-proof.md) | [Struct/04-proofs/04.05-type-safety-fg-fgg.md](../Struct/04-proofs/04.05-type-safety-fg-fgg.md) | FG/FGG Type Safety | L5 |
| [dot-subtyping-completeness.md](./dot-subtyping-completeness.md) | [Struct/04-proofs/04.06-dot-subtyping-completeness.md](../Struct/04-proofs/04.06-dot-subtyping-completeness.md) | DOT Subtyping | L5-L6 |
| [choreographic-deadlock-freedom.md](./choreographic-deadlock-freedom.md) | [Struct/04-proofs/04.07-deadlock-freedom-choreographic.md](../Struct/04-proofs/04.07-deadlock-freedom-choreographic.md) | Choreographic Deadlock Freedom | L5 |
| [open-problems-streaming-verification.md](./open-problems-streaming-verification.md) | [Struct/06-frontier/06.01-open-problems-streaming-verification.md](../Struct/06-frontier/06.01-open-problems-streaming-verification.md) | Open Problems | L4-L6 |
| [ai-agent-session-types.md](./ai-agent-session-types.md) | [Struct/06-frontier/06.03-ai-agent-session-types.md](../Struct/06-frontier/06.03-ai-agent-session-types.md) | AI Agent Session Types | L5 |
| [dbsp-theory-framework.md](./dbsp-theory-framework.md) | [Struct/06-frontier/dbsp-theory-framework.md](../Struct/06-frontier/dbsp-theory-framework.md) | DBSP Framework | L5-L6 |
| [llm-guided-formal-proof-automation.md](./llm-guided-formal-proof-automation.md) | [Struct/06-frontier/llm-guided-formal-proof-automation.md](../Struct/06-frontier/llm-guided-formal-proof-automation.md) | LLM Proof Automation | L5-L6 |

### Knowledge / Design Patterns

| Document | Source | Description |
|----------|--------|-------------|
| [pattern-realtime-feature-engineering.md](./pattern-realtime-feature-engineering.md) | [Knowledge/02-design-patterns/pattern-realtime-feature-engineering.md](../Knowledge/02-design-patterns/pattern-realtime-feature-engineering.md) | Real-time Feature Engineering |
| [pattern-stateful-computation.md](./pattern-stateful-computation.md) | [Knowledge/02-design-patterns/pattern-stateful-computation.md](../Knowledge/02-design-patterns/pattern-stateful-computation.md) | Stateful Computation Pattern |
| [pattern-event-time-processing.md](./pattern-event-time-processing.md) | [Knowledge/02-design-patterns/pattern-event-time-processing.md](../Knowledge/02-design-patterns/pattern-event-time-processing.md) | Event Time Processing |
| [pattern-windowed-aggregation.md](./pattern-windowed-aggregation.md) | [Knowledge/02-design-patterns/pattern-windowed-aggregation.md](../Knowledge/02-design-patterns/pattern-windowed-aggregation.md) | Windowed Aggregation |

### Knowledge / Business Patterns

| Document | Source | Description |
|----------|--------|-------------|
| [fintech-realtime-risk-control.md](./fintech-realtime-risk-control.md) | [Knowledge/03-business-patterns/fintech-realtime-risk-control.md](../Knowledge/03-business-patterns/fintech-realtime-risk-control.md) | FinTech Real-time Risk Control |

### Knowledge / Best Practices

| Document | Source | Description |
|----------|--------|-------------|
| [flink-production-checklist.md](./flink-production-checklist.md) | [Knowledge/07-best-practices/07.01-flink-production-checklist.md](../Knowledge/07-best-practices/07.01-flink-production-checklist.md) | Production Deployment Checklist |
| [performance-tuning-patterns.md](./performance-tuning-patterns.md) | [Knowledge/07-best-practices/07.02-performance-tuning-patterns.md](../Knowledge/07-best-practices/07.02-performance-tuning-patterns.md) | Performance Tuning Patterns |

### Knowledge / Anti-Patterns

| Document | Source | Description |
|----------|--------|-------------|
| [anti-pattern-global-state-abuse.md](./anti-pattern-global-state-abuse.md) | [Knowledge/09-anti-patterns/anti-pattern-01-global-state-abuse.md](../Knowledge/09-anti-patterns/anti-pattern-01-global-state-abuse.md) | Global State Abuse |
| [anti-pattern-hot-key-skew.md](./anti-pattern-hot-key-skew.md) | [Knowledge/09-anti-patterns/anti-pattern-04-hot-key-skew.md](../Knowledge/09-anti-patterns/anti-pattern-04-hot-key-skew.md) | Hot Key Skew |

### Knowledge / Technology Selection

| Document | Source | Description |
|----------|--------|-------------|
| [engine-selection-guide.md](./engine-selection-guide.md) | [Knowledge/04-technology-selection/engine-selection-guide.md](../Knowledge/04-technology-selection/engine-selection-guide.md) | Engine Selection Guide |
| [flink-vs-spark-comparison.md](./flink-vs-spark-comparison.md) | [Knowledge/04-technology-selection/flink-vs-spark-structured-streaming-2026.md](../Knowledge/04-technology-selection/flink-vs-spark-structured-streaming-2026.md) | Flink vs Spark 2026 |

### Flink / Core Concepts

| Document | Source | Description |
|----------|--------|-------------|
| [flink-five-mental-models.md](./flink-five-mental-models.md) | [Flink/01-concepts/flink-five-mental-models-complete-guide.md](../Flink/01-concepts/flink-five-mental-models-complete-guide.md) | Five Mental Models |
| [flink-checkpoint-mechanism.md](./flink-checkpoint-mechanism.md) | [Flink/02-core/checkpoint-mechanism-deep-dive.md](../Flink/02-core/checkpoint-mechanism-deep-dive.md) | Checkpoint Mechanism |
| [flink-exactly-once-semantics.md](./flink-exactly-once-semantics.md) | [Flink/02-core/exactly-once-semantics-deep-dive.md](../Flink/02-core/exactly-once-semantics-deep-dive.md) | Exactly-Once Semantics |

### TECH-STACK / Streaming + Postgres + Temporal + Kratos

| Document | Source | Description | Formality |
|----------|--------|-------------|-----------|
| [techstack-index.md](./techstack-index.md) | [TECH-STACK/00-meta/00-INDEX.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/00-meta/00-INDEX.md) | Module Index & PG18 Feature Matrix | L2 |
| [techstack-five-technology-complementarity.md](./techstack-five-technology-complementarity.md) | [TECH-STACK/01-system-composition/01.01-five-technology-complementarity.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/01-system-composition/01.01-five-technology-complementarity.md) | Five-Technology Complementarity Theorem | L3 |
| [techstack-end-to-end-data-control-flow.md](./techstack-end-to-end-data-control-flow.md) | [TECH-STACK/01-system-composition/01.02-end-to-end-data-control-flow.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/01-system-composition/01.02-end-to-end-data-control-flow.md) | E2E Data & Control Flow Analysis | L3 |
| [techstack-dependency-coupling-matrix.md](./techstack-dependency-coupling-matrix.md) | [TECH-STACK/01-system-composition/01.03-dependency-coupling-matrix.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/01-system-composition/01.03-dependency-coupling-matrix.md) | Dependency Structure Matrix & Coupling | L3 |
| [techstack-aggregation-patterns.md](./techstack-aggregation-patterns.md) | [TECH-STACK/01-system-composition/01.04-aggregation-patterns.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/01-system-composition/01.04-aggregation-patterns.md) | Aggregator & Composite Patterns | L3 |
| [techstack-postgresql-18-cdc-resilience.md](./techstack-postgresql-18-cdc-resilience.md) | [TECH-STACK/02-component-deep-dive/02.01-postgresql-18-cdc-resilience.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/02-component-deep-dive/02.01-postgresql-18-cdc-resilience.md) | PG18 CDC & Resilience Deep Dive | L3 |
| [techstack-temporal-workflow-orchestration.md](./techstack-temporal-workflow-orchestration.md) | [TECH-STACK/02-component-deep-dive/02.02-temporal-workflow-orchestration.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/02-component-deep-dive/02.02-temporal-workflow-orchestration.md) | Temporal Workflow Orchestration | L3 |
| [techstack-kratos-microservices-framework.md](./techstack-kratos-microservices-framework.md) | [TECH-STACK/02-component-deep-dive/02.03-kratos-microservices-framework.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/02-component-deep-dive/02.03-kratos-microservices-framework.md) | Kratos Microservices Framework | L3 |
| [techstack-flink-stream-processing-core.md](./techstack-flink-stream-processing-core.md) | [TECH-STACK/02-component-deep-dive/02.04-flink-stream-processing-core.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/02-component-deep-dive/02.04-flink-stream-processing-core.md) | Flink Stream Processing Core | L3 |
| [techstack-docker-kubernetes-runtime.md](./techstack-docker-kubernetes-runtime.md) | [TECH-STACK/02-component-deep-dive/02.05-docker-kubernetes-runtime.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/02-component-deep-dive/02.05-docker-kubernetes-runtime.md) | Docker & Kubernetes Runtime | L2 |
| [techstack-pg18-cdc-kafka-flink-pipeline.md](./techstack-pg18-cdc-kafka-flink-pipeline.md) | [TECH-STACK/03-integration/03.01-pg18-cdc-kafka-flink-pipeline.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/03-integration/03.01-pg18-cdc-kafka-flink-pipeline.md) | PG18 → Debezium → Kafka → Flink Pipeline | L4 |
| [techstack-temporal-kratos-worker-hosting.md](./techstack-temporal-kratos-worker-hosting.md) | [TECH-STACK/03-integration/03.02-temporal-kratos-worker-hosting.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/03-integration/03.02-temporal-kratos-worker-hosting.md) | Temporal Worker Hosted in Kratos | L3 |
| [techstack-outbox-pattern-pg18-kratos.md](./techstack-outbox-pattern-pg18-kratos.md) | [TECH-STACK/03-integration/03.03-outbox-pattern-pg18-kratos.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/03-integration/03.03-outbox-pattern-pg18-kratos.md) | Outbox Pattern with PG18 & Kratos | L3 |
| [techstack-saga-pattern-temporal-orchestration.md](./techstack-saga-pattern-temporal-orchestration.md) | [TECH-STACK/03-integration/03.04-saga-pattern-temporal-orchestration.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/03-integration/03.04-saga-pattern-temporal-orchestration.md) | Saga Pattern Orchestration | L3 |
| [techstack-cqrs-streaming-read-model.md](./techstack-cqrs-streaming-read-model.md) | [TECH-STACK/03-integration/03.05-cqrs-streaming-read-model.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/03-integration/03.05-cqrs-streaming-read-model.md) | CQRS Streaming Read Model | L3 |
| [techstack-resilience-evaluation-framework.md](./techstack-resilience-evaluation-framework.md) | [TECH-STACK/04-resilience/04.01-resilience-evaluation-framework.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/04-resilience/04.01-resilience-evaluation-framework.md) | RES/RML Resilience Evaluation Framework | L4 |
| [techstack-circuit-breaker-backpressure-analysis.md](./techstack-circuit-breaker-backpressure-analysis.md) | [TECH-STACK/04-resilience/04.02-circuit-breaker-backpressure-analysis.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/04-resilience/04.02-circuit-breaker-backpressure-analysis.md) | Circuit Breaker & Backpressure Analysis | L4 |
| [techstack-bulkhead-retry-isolation.md](./techstack-bulkhead-retry-isolation.md) | [TECH-STACK/04-resilience/04.03-bulkhead-retry-isolation.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/04-resilience/04.03-bulkhead-retry-isolation.md) | Bulkhead Isolation & Retry Storm Prevention | L3 |
| [techstack-fault-tolerance-composition-proof.md](./techstack-fault-tolerance-composition-proof.md) | [TECH-STACK/04-resilience/04.04-fault-tolerance-composition-proof.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/04-resilience/04.04-fault-tolerance-composition-proof.md) | Fault Tolerance Composition Proof | L5 |
| [techstack-chaos-engineering-practice.md](./techstack-chaos-engineering-practice.md) | [TECH-STACK/04-resilience/04.05-chaos-engineering-practice.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/04-resilience/04.05-chaos-engineering-practice.md) | Chaos Engineering Practice | L3 |
| [techstack-docker-compose-fullstack.md](./techstack-docker-compose-fullstack.md) | [TECH-STACK/05-deployment/05.01-docker-compose-fullstack.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/05-deployment/05.01-docker-compose-fullstack.md) | Docker Compose Full-Stack Deployment | L2 |
| [techstack-kubernetes-helm-deployment.md](./techstack-kubernetes-helm-deployment.md) | [TECH-STACK/05-deployment/05.02-kubernetes-helm-deployment.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/05-deployment/05.02-kubernetes-helm-deployment.md) | Kubernetes Helm Deployment | L2 |
| [techstack-production-checklist.md](./techstack-production-checklist.md) | [TECH-STACK/05-deployment/05.03-production-checklist.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/05-deployment/05.03-production-checklist.md) | Production Deployment Checklist | L2 |
| [techstack-end-to-end-order-processing-example.md](./techstack-end-to-end-order-processing-example.md) | [TECH-STACK/06-practice/06.01-end-to-end-order-processing-example.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/06-practice/06.01-end-to-end-order-processing-example.md) | End-to-End Order Processing Example | L3 |
| [techstack-performance-benchmark-guide.md](./techstack-performance-benchmark-guide.md) | [TECH-STACK/06-practice/06.02-performance-benchmark-guide.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/06-practice/06.02-performance-benchmark-guide.md) | Performance Benchmark Guide | L2 |
| [techstack-future-trends-ai-agent-streaming.md](./techstack-future-trends-ai-agent-streaming.md) | [TECH-STACK/07-frontier/07.01-future-trends-ai-agent-streaming.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/07-frontier/07.01-future-trends-ai-agent-streaming.md) | Future Trends: AI Agent & Streaming | L2 |

### Project-Level Documents

| Document | Description |
|----------|-------------|
| [README.md](./README.md) | Project Overview |
| [QUICK-START.md](./QUICK-START.md) | Quick Start Guide |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | Architecture Document |
| [KNOWLEDGE-GRAPH-GUIDE.md](./KNOWLEDGE-GRAPH-GUIDE.md) | Knowledge Graph Guide |
| [OBSERVABILITY-GUIDE.md](./OBSERVABILITY-GUIDE.md) | Observability Guide |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Contributing Guide |
| [GLOSSARY.md](./GLOSSARY.md) | Glossary |
| [LEARNING-PATH-GUIDE.md](./LEARNING-PATH-GUIDE.md) | Learning Path Guide |
| [BEST-PRACTICES.md](./BEST-PRACTICES.md) | Best Practices |
| [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) | Troubleshooting Guide |
| [FLINK-INDEX.md](./FLINK-INDEX.md) | Flink Index |
| [FLINK-QUICK-START.md](./FLINK-QUICK-START.md) | Flink Quick Start |
| [KNOWLEDGE-INDEX.md](./KNOWLEDGE-INDEX.md) | Knowledge Index |
| [STRUCT-INDEX.md](./STRUCT-INDEX.md) | Struct Index |

---

## Translation Status

```
English Coverage (Core Documents):
├── Struct/ Core Theory:     5 / 15  (33%)
├── Knowledge/ Patterns:     4 / 20  (20%)
├── Knowledge/ Business:     1 / 10  (10%)
├── Knowledge/ Practices:    2 / 7   (29%)
├── Knowledge/ Anti-Patterns: 2 / 10  (20%)
├── Knowledge/ Selection:    2 / 10  (20%)
├── Flink/ Core Concepts:    3 / 15  (20%)
├── Project Docs:           14 / 15  (93%)
----------------------------------------
Total Core: 88 / 127  (69%+)
Total Files: 181
```

> **Goal**: Reach 100% coverage of core documents (60+ priority translations).

---

*This index is updated as new translations are completed.*
