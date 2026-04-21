# AnalysisDataFlow — English Document Index

> **Language**: English | **Last Updated**: 2026-04-21
> **Total Documents**: 128 | **New This Round**: 18

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
Total Core: 35 / 102  (34%+)
Total Files: 129
```

> **Goal**: Reach 100% coverage of core documents (60+ priority translations).

---

*This index is updated as new translations are completed.*
