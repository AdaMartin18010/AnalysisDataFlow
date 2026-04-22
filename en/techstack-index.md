# TECH-STACK: Streaming × PostgreSQL 18 × Temporal × Kratos × Docker

> **Stage**: TECH-STACK | **Prerequisites**: [Chinese source](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/00-meta/00-INDEX.md) | **Formalization Level**: L3-L4 | **Last Updated**: 2026-04-22

## Tech Stack Positioning

This directory systematically organizes the **Streaming (Apache Flink/Kafka) × PostgreSQL 18 × Temporal × Kratos × Docker/K8s** five-technology combination:

1. **System Composition** — Data flow, control flow, coupling matrix
2. **Component Deep Dive** — Independent architecture and mechanisms of each component
3. **Cross-Component Integration Patterns** — Outbox/Saga/CQRS/Aggregator
4. **Compositional Resilience** — Fault propagation, fault-tolerance proofs, chaos engineering
5. **Deployment & Production Practice** — Docker/K8s/performance benchmarks

## Directory Structure

```
TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/
├── 00-meta/                    # Metadata, index, glossary
├── 01-system-composition/      # System composition architecture (core)
│   ├── 01.01-composite-architecture-overview.md
│   ├── 01.02-data-flow-control-flow-analysis.md
│   ├── 01.03-dependency-coupling-matrix.md
│   └── 01.04-aggregation-patterns.md
├── 02-component-deep-dive/     # Deep dive into each component's architecture
│   ├── 02.01-postgresql-18-cdc-deep-dive.md
│   ├── 02.02-temporal-workflow-engine-guide.md
│   ├── 02.03-kratos-microservices-framework.md
│   ├── 02.04-flink-streaming-resilience.md
│   └── 02.05-docker-kubernetes-deployment-base.md
├── 03-integration/             # Cross-component integration patterns
│   ├── 03.01-pg18-cdc-kafka-flink-pipeline.md
│   ├── 03.02-temporal-kratos-worker-integration.md
│   ├── 03.03-outbox-pattern-pg18-kratos.md
│   ├── 03.04-saga-pattern-temporal-kratos.md
│   └── 03.05-cqrs-streaming-read-model.md
├── 04-resilience/              # Compositional resilience analysis (core)
│   ├── 04.01-resilience-evaluation-framework.md
│   ├── 04.02-circuit-breaker-backpressure-analysis.md
│   ├── 04.03-bulkhead-retry-isolation-patterns.md
│   ├── 04.04-fault-tolerance-composition-proof.md
│   └── 04.05-chaos-engineering-practice.md
├── 05-deployment/              # Docker / K8s / Helm deployment
├── 06-practice/                # End-to-end cases and performance tuning
└── 07-frontier/                # Frontier trends and version tracking
```

## PostgreSQL 18 Core Features Overview (Authoritative Sources)

> Source: [PostgreSQL 18 Release Notes](https://www.postgresql.org/docs/release/18.0/) (2025-09-25)

| Feature | Description | Streaming Relevance |
|---------|-------------|---------------------|
| **Async I/O (AIO)** | `io_uring` non-blocking reads, up to 3× storage scan performance | More efficient CDC WAL reading |
| **UUIDv7** | Time-sortable UUID, improves B-tree index locality | Event table primary key, reduces index splitting |
| **Virtual Generated Columns** | Virtual columns computed at query time, zero storage overhead | Derived event fields, simplified schema |
| **B-Tree Skip Scan** | Multi-column index usable without leading column | Composite query optimization |
| **Logical Replication Enhancement** | Parallel streams, conflict reporting, generated column replication | More reliable Debezium/Flink CDC |
| **Temporal WITHOUT OVERLAPS** | Native temporal table constraint support | Semantic alignment with Temporal workflow engine |
| **RETURNING OLD/NEW** | Single-statement before/after values | Simplified CDC event enrichment |
| **Parallel COPY** | Parallelized bulk loading | Faster initial snapshot |

## Document List and Quick Navigation

| ID | Document | Topic | Size |
|----|----------|-------|------|
| **C1** | [01.01-composite-architecture-overview.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/01-system-composition/01.01-composite-architecture-overview.md) | Five-Technology Composite Architecture Overview | ~27KB |
| **C2** | [01.02-data-flow-control-flow-analysis.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/01-system-composition/01.02-data-flow-control-flow-analysis.md) | Data Flow and Control Flow Analysis | ~21KB |
| **C3** | [01.03-dependency-coupling-matrix.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/01-system-composition/01.03-dependency-coupling-matrix.md) | Dependency Coupling Matrix | ~35KB |
| **C4** | [01.04-aggregation-patterns.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/01-system-composition/01.04-aggregation-patterns.md) | Aggregation Patterns | ~38KB |
| **D1** | [02.01-postgresql-18-cdc-deep-dive.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/02-component-deep-dive/02.01-postgresql-18-cdc-deep-dive.md) | PG18 CDC Deep Dive | ~23KB |
| **D2** | [02.02-temporal-workflow-engine-guide.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/02-component-deep-dive/02.02-temporal-workflow-engine-guide.md) | Temporal Workflow Engine | ~29KB |
| **D3** | [02.03-kratos-microservices-framework.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/02-component-deep-dive/02.03-kratos-microservices-framework.md) | Kratos Microservices Framework | ~24KB |
| **D4** | [02.04-flink-streaming-resilience.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/02-component-deep-dive/02.04-flink-streaming-resilience.md) | Flink Streaming Resilience | ~17KB |
| **D5** | [02.05-docker-kubernetes-deployment-base.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/02-component-deep-dive/02.05-docker-kubernetes-deployment-base.md) | Docker/K8s Deployment Base | ~29KB |
| **I1** | [03.01-pg18-cdc-kafka-flink-pipeline.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/03-integration/03.01-pg18-cdc-kafka-flink-pipeline.md) | CDC-Kafka-Flink Pipeline | ~15KB |
| **I2** | [03.02-temporal-kratos-worker-integration.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/03-integration/03.02-temporal-kratos-worker-integration.md) | Temporal-Kratos Worker | ~12KB |
| **I3** | [03.03-outbox-pattern-pg18-kratos.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/03-integration/03.03-outbox-pattern-pg18-kratos.md) | Outbox Pattern | ~12KB |
| **I4** | [03.04-saga-pattern-temporal-kratos.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/03-integration/03.04-saga-pattern-temporal-kratos.md) | Saga Distributed Transactions | ~45KB |
| **I5** | [03.05-cqrs-streaming-read-model.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/03-integration/03.05-cqrs-streaming-read-model.md) | CQRS Streaming Read Model | ~12KB |
| **R1** | [04.01-resilience-evaluation-framework.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/04-resilience/04.01-resilience-evaluation-framework.md) | Resilience Evaluation Framework | ~27KB |
| **R2** | [04.02-circuit-breaker-backpressure-analysis.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/04-resilience/04.02-circuit-breaker-backpressure-analysis.md) | Circuit Breaker & Backpressure Analysis | ~16KB |
| **R3** | [04.03-bulkhead-retry-isolation-patterns.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/04-resilience/04.03-bulkhead-retry-isolation-patterns.md) | Bulkhead Isolation & Retry | ~14KB |
| **R4** | [04.04-fault-tolerance-composition-proof.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/04-resilience/04.04-fault-tolerance-composition-proof.md) | Compositional Fault Tolerance Formal Proof | ~29KB |
| **R5** | [04.05-chaos-engineering-practice.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/04-resilience/04.05-chaos-engineering-practice.md) | Chaos Engineering Practice | ~14KB |
| **P1** | [05.01-docker-compose-fullstack.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/05-deployment/05.01-docker-compose-fullstack.md) | Docker Compose Full Stack | ~23KB |
| **P2** | [05.02-kubernetes-helm-deployment.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/05-deployment/05.02-kubernetes-helm-deployment.md) | K8s Helm Deployment | ~29KB |
| **P3** | [05.03-production-checklist.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/05-deployment/05.03-production-checklist.md) | Production Checklist | ~25KB |
| **P4** | [06.01-end-to-end-order-processing-example.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/06-practice/06.01-end-to-end-order-processing-example.md) | End-to-End Order Processing Case | ~40KB |
| **P5** | [06.02-performance-benchmark-guide.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/06-practice/06.02-performance-benchmark-guide.md) | Performance Benchmark Guide | ~22KB |
| **P6** | [07.01-pg19-roadmap-ai-streaming.md](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/07-frontier/07.01-pg19-roadmap-ai-streaming.md) | PG19 Roadmap & AI Streaming | ~17KB |

## Quality Gate Status

| Check Item | Status |
|------------|--------|
| Eight-Section Template | ✅ 25/25 (100%) |
| Internal Cross-References | ✅ 0 broken links |
| Mermaid Syntax | ✅ 48/48 (100%) |
| Formal Element Uniqueness | ✅ 115 elements, no conflicts |
| Citation Format [^n] | ✅ 95+ entries |

## Resilient Architecture Authoritative Framework Reference

> Source: arXiv 2512.16959v1 (2025-12), *Resilient Microservices: A Systematic Review of Recovery Patterns*

This tech stack's resilience argumentation is based on this PRISMA-aligned systematic literature review, covering:

- **Recovery Pattern Taxonomy** — Fault type → recovery strategy mapping
- **Resilience Evaluation Score (RES)** — Standardized resilience assessment checklist
- **Resilience Maturity Model (RML)** — Five-level maturity model (Ad-hoc → Optimized)
- **Nine Operations Topics (T1-T9)** — Circuit breaker, Saga, retry, bulkhead, backpressure, chaos testing, etc.
