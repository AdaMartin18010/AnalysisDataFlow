---
title: "Cross-Reference Index"
translation_status: ai_translated_reviewed
source_version: v4.1
last_sync: "2026-04-15"
---

# Cross-Reference Index

> **Stage**: Knowledge/Flink-Scala-Rust-Comprehensive/99-appendix | Version: v1.0 | Coverage: 28+ documents

---

## Table of Contents

- [Cross-Reference Index](#cross-reference-index)
  - [Table of Contents](#table-of-contents)
  - [1. Document Navigation](#1-document-navigation)
    - [1.1 By Chapter](#11-by-chapter)
      - [01 - Scala Streaming Ecosystem](#01---scala-streaming-ecosystem)
      - [02 - Flink Technical System](#02---flink-technical-system)
      - [03 - Scala ↔ Rust Interoperability](#03---scala--rust-interoperability)
      - [04 - Rust Stream Processing Engines](#04---rust-stream-processing-engines)
      - [05 - Architecture Patterns](#05---architecture-patterns)
      - [06 - 2026 Trends](#06---2026-trends)
      - [99 - Appendix](#99---appendix)
    - [1.2 By Role](#12-by-role)
    - [1.3 By Technology Stack](#13-by-technology-stack)
  - [2. Formal Definition Index](#2-formal-definition-index)
    - [2.1 Definition Type Statistics](#21-definition-type-statistics)
    - [2.2 By Category](#22-by-category)
      - [Scala Type System (Def-K-01-*, Def-K-SC-*)](#scala-type-system-def-k-01--def-k-sc-)
      - [Flink Architecture (Def-K-02-\*)](#flink-architecture-def-k-02-)
      - [WASM/WASI (Def-K-WSI-\*)](#wasmwasi-def-k-wsi-)
      - [Rust Engines (Def-RUST-*, Def-RW-*, Def-MZ-\*)](#rust-engines-def-rust--def-rw--def-mz-)
    - [2.3 Theorem and Proof Index](#23-theorem-and-proof-index)
    - [2.4 Lemma Index](#24-lemma-index)
  - [3. Code Example Index](#3-code-example-index)
    - [3.1 By Language](#31-by-language)
      - [Scala Code Examples](#scala-code-examples)
      - [Rust Code Examples](#rust-code-examples)
      - [Java Code Examples](#java-code-examples)
      - [SQL Code Examples](#sql-code-examples)
      - [Configuration Examples](#configuration-examples)
    - [3.2 By Topic](#32-by-topic)
  - [4. Diagram Index](#4-diagram-index)
    - [4.1 Mermaid Diagram Statistics](#41-mermaid-diagram-statistics)
    - [4.2 Key Architecture Diagram Index](#42-key-architecture-diagram-index)
    - [4.3 Flowchart Index](#43-flowchart-index)
    - [4.4 Sequence Diagram Index](#44-sequence-diagram-index)
  - [5. Topic Quick Lookup](#5-topic-quick-lookup)
    - [5.1 Core Concept Lookup Table](#51-core-concept-lookup-table)
    - [5.2 FAQ Index](#52-faq-index)
    - [5.3 Performance Optimization Guide Index](#53-performance-optimization-guide-index)
  - [6. Dependency Graph](#6-dependency-graph)
    - [6.1 Document Dependencies](#61-document-dependencies)
    - [6.2 Prerequisite Matrix](#62-prerequisite-matrix)
  - [Appendix: Index Usage Guide](#appendix-index-usage-guide)
    - [Quick Lookup Tips](#quick-lookup-tips)
    - [Cross-Reference Format](#cross-reference-format)

---

## 1. Document Navigation

### 1.1 By Chapter

#### 01 - Scala Streaming Ecosystem

| Doc ID | Document Name | Key Topics | Formal Level |
|----------|----------|----------|------------|
| 01.01 | [scala-streaming-landscape](../01-scala-ecosystem/01.01-scala-streaming-landscape.md) | Scala streaming ecosystem, fs2, Pekko Streams, ZIO | L4 |
| 01.02 | [flink-scala-api-analysis](../01-scala-ecosystem/01.02-flink-scala-api-analysis.md) | Flink Scala API, type safety, interoperability | L4 |
| 01.03 | [scala-java-api-interop](../01-scala-ecosystem/01.03-scala-java-api-interop.md) | Scala/Java interoperability, API compatibility | L3 |
| 01.04 | [fs2-pekko-streams](../01-scala-ecosystem/01.04-fs2-pekko-streams.md) | fs2, Pekko Streams comparison, integration | L4 |
| 01.05 | [scala-type-system-streaming](../01-scala-ecosystem/01.05-scala-type-system-streaming.md) | HKT, Type Class, macro programming | L5 |

#### 02 - Flink Technical System

| Doc ID | Document Name | Key Topics | Formal Level |
|----------|----------|----------|------------|
| 02.01 | [flink-2x-architecture](../02-flink-system/02.01-flink-2x-architecture.md) | Flink 2.x, disaggregated storage/compute, Adaptive Scheduler | L5 |
| 02.02 | [flink-runtime-deep-dive](../02-flink-system/02.02-flink-runtime-deep-dive.md) | Runtime, Checkpoint, network stack | L4 |
| 02.03 | [flink-state-backends](../02-flink-system/02.03-flink-state-backends.md) | State Backend, ForSt, RocksDB | L4 |
| 02.04 | [flink-sql-table-api](../02-flink-system/02.04-flink-sql-table-api.md) | SQL, Table API, Streaming SQL | L4 |
| 02.05 | [flink-cloud-native](../02-flink-system/02.05-flink-cloud-native.md) | K8s, Operator, cloud-native deployment | L3 |

#### 03 - Scala ↔ Rust Interoperability

| Doc ID | Document Name | Key Topics | Formal Level |
|----------|----------|----------|------------|
| 03.01 | [wasm-interop](../03-scala-rust-interop/03.01-wasm-interop.md) | WASM, WASI 0.3, component model | L4 |
| 03.02 | [jni-bridge](../03-scala-rust-interop/03.02-jni-bridge.md) | JNI, unsafe, FFI performance | L4 |
| 03.03 | [grpc-service](../03-scala-rust-interop/03.03-grpc-service.md) | gRPC, service mesh, distributed | L3 |
| 03.04 | [iron-functions-guide](../03-scala-rust-interop/03.04-iron-functions-guide.md) | Iron Functions, WASM UDF | L3 |
| 03.05 | [interop-comparison](../03-scala-rust-interop/03.05-interop-comparison.md) | Interoperability comparison, selection decisions | L3 |

#### 04 - Rust Stream Processing Engines

| Doc ID | Document Name | Key Topics | Formal Level |
|----------|----------|----------|------------|
| 04.01 | [rust-engines-comparison](../04-rust-engines/04.01-rust-engines-comparison.md) | Engine comparison, selection decisions | L4 |
| 04.02 | [risingwave-deep-dive](../04-rust-engines/04.02-risingwave-deep-dive.md) | RisingWave, Hummock, materialized views | L4 |
| 04.03 | [materialize-analysis](../04-rust-engines/04.03-materialize-analysis.md) | Materialize, Differential Dataflow | L4 |
| 04.04 | [arroyo-cloudflare](../04-rust-engines/04.04-arroyo-cloudflare.md) | Arroyo, Cloudflare, edge computing | L3 |
| 04.05 | [vectorization-simd](../04-rust-engines/04.05-vectorization-simd.md) | SIMD, vectorization, performance optimization | L4 |

#### 05 - Architecture Patterns

| Doc ID | Document Name | Key Topics | Formal Level |
|----------|----------|----------|------------|
| 05.01 | [hybrid-architecture-patterns](../05-architecture-patterns/05.01-hybrid-architecture-patterns.md) | Hybrid architecture, layered design | L3 |
| 05.02 | [migration-strategies](../05-architecture-patterns/05.02-migration-strategies.md) | Migration strategies, incremental transformation | L3 |
| 05.03 | [cloud-deployment](../05-architecture-patterns/05.03-cloud-deployment.md) | Multi-cloud deployment, K8s best practices | L3 |
| 05.04 | [edge-computing](../05-architecture-patterns/05.04-edge-computing.md) | Edge computing, low-latency architecture | L3 |

#### 06 - 2026 Trends

| Doc ID | Document Name | Key Topics | Formal Level |
|----------|----------|----------|------------|
| 06.01 | [2026-trends](../06-trends-2026/06.01-2026-trends.md) | Technology trends, evolution predictions | L2 |
| 06.02 | [adoption-roadmap](../06-trends-2026/06.02-adoption-roadmap.md) | Adoption roadmap, decision framework | L2 |

#### 99 - Appendix

| Doc ID | Document Name | Key Topics | Formal Level |
|----------|----------|----------|------------|
| 99.01 | [glossary](99.01-glossary.md) | Glossary, definition index | L1 |
| 99.02 | [references](99.02-references.md) | References, resource index | L1 |
| 99.03 | [cross-reference-index](cross-reference-index.md) | Cross-references, quick lookup | L1 |

---

### 1.2 By Role

| Role | Recommended Document Path |
|------|-------------|
| **Architect** | 05.01 → 05.03 → 05.04 → 06.01 → 06.02 |
| **Scala Developer** | 01.01 → 01.02 → 01.04 → 01.05 → 03.02 |
| **Rust Developer** | 04.01 → 04.02 → 03.01 → 04.05 |
| **Flink User** | 02.01 → 02.02 → 02.03 → 01.02 → 02.04 |
| **DevOps Engineer** | 02.05 → 05.03 → 05.04 → 02.01 |
| **Performance Engineer** | 04.05 → 02.03 → 04.02 → 02.02 |
| **Decision Maker** | 04.01 → 06.01 → 06.02 → 05.01 |

---

### 1.3 By Technology Stack

| Technology Domain | Core Documents | Extended Reading |
|----------|----------|----------|
| **Scala Streaming** | 01.01, 01.04, 01.05 | 01.02, 01.03 |
| **Flink Core** | 02.01, 02.02, 02.03 | 02.04, 02.05 |
| **Rust Stream Engines** | 04.01, 04.02, 04.03 | 04.04, 04.05 |
| **WASM Interoperability** | 03.01, 03.04 | 03.05 |
| **Cloud-Native Deployment** | 02.05, 05.03 | 05.01, 05.04 |
| **Architecture Design** | 05.01, 05.02, 06.01 | 06.02 |

---

## 2. Formal Definition Index

### 2.1 Definition Type Statistics

| Type | Prefix | Count | Description |
|------|------|------|------|
| Definition | Def-K-* | 45+ | Knowledge layer formal definitions |
| Lemma | Lemma-K-* | 25+ | Properties derived from definitions |
| Proposition | Prop-K-* | 20+ | Statements requiring proof |
| Theorem | Thm-K-* | 15+ | Major formal results |
| Corollary | Cor-K-* | 5+ | Directly derived from theorems |

### 2.2 By Category

#### Scala Type System (Def-K-01-*, Def-K-SC-*)

| ID | Name | Location | Description |
|------|------|------|------|
| Def-K-01-01 | Scala Streaming Ecosystem | 01.01 | Quintuple formal definition |
| Def-K-01-02 | Functional Stream Processing | 01.01 | Referential transparency and lazy evaluation |
| Def-K-01-03 | Stream Type Constructor | 01.01 | HKT formalization |
| Def-K-SC-01 | Type Class Model | 01.05 | Type class formalization |
| Def-K-SC-02 | Higher-Kinded Types | 01.05 | Higher-kinded type constructors |

#### Flink Architecture (Def-K-02-*)

| ID | Name | Location | Description |
|------|------|------|------|
| Def-K-02-01 | Disaggregated Storage/Compute Architecture | 02.01 | DisaggregatedArch quintuple |
| Def-K-02-02 | Unified Scheduler | 02.01 | Adaptive Scheduler definition |
| Def-K-02-03 | Async Checkpoint Enhancement | 02.01 | Checkpoint O(1) complexity |
| Def-K-02-04 | Async Execution Model | 02.01 | Non-blocking state access |
| Def-K-02-05 | ForSt State Backend | 02.03 | Cloud-native state backend |

#### WASM/WASI (Def-K-WSI-*)

| ID | Name | Location | Description |
|------|------|------|------|
| Def-K-WSI-01 | WASI System Interface | 03.01 | Quadruple formalization |
| Def-K-WSI-02 | WASI 0.3 Async I/O Model | 03.01 | AsyncWASI definition |
| Def-K-WSI-03 | WASM Component Model | 03.01 | Component definition |

#### Rust Engines (Def-RUST-*, Def-RW-*, Def-MZ-*)

| ID | Name | Location | Description |
|------|------|------|------|
| Def-RUST-01 | Rust Native Stream Processing Engine | 04.01 | Quadruple definition |
| Def-RUST-02 | Consistency Model Hierarchy | 04.01 | Consistency partial order |
| Def-RUST-03 | Stream Processing Engine Taxonomy | 04.01 | Taxonomy definition |
| Def-RW-01 | Stream Processing Database | 04.02 | StreamingDB definition |
| Def-RW-02 | Compute-Storage Disaggregated Architecture | 04.02 | SepArch definition |
| Def-RW-03 | Hummock Tiered Storage Engine | 04.02 | Three-layer storage definition |

### 2.3 Theorem and Proof Index

| ID | Name | Location | Type | Description |
|------|------|------|------|------|
| Thm-K-01-01 | Categorical Unification of Scala Stream Libraries | 01.01 | Theorem | Monad unification abstraction |
| Thm-K-02-01 | Exactly-Once under Disaggregated Storage | 02.01 | Theorem | Semantic preservation with disaggregated storage |
| Thm-K-02-02 | Adaptive Scheduler Convergence | 02.01 | Theorem | Scheduler convergence proof |
| Thm-K-WSI-01 | Async UDF Throughput Theorem | 03.01 | Theorem | WASI performance advantage |
| Thm-K-WSI-02 | Type Safety Formal Argument | 03.01 | Proof | WIT type consistency |
| Thm-RUST-01 | Selection Decision Theorem | 04.01 | Theorem | Optimal selection formula |
| Thm-RW-01 | RisingWave Exactly-Once | 04.02 | Proof | Epoch-based guarantee |
| Thm-RW-02 | Rust UDF Execution Performance Theorem | 04.02 | Theorem | Native UDF advantage |

### 2.4 Lemma Index

| ID | Name | Location | Description |
|------|------|------|------|
| Lemma-K-01-01 | Composability of Scala Stream Libraries | 01.01 | Adapter pattern composition |
| Lemma-K-01-02 | Determinism of Pure Function Stream Transformations | 01.01 | Output determinism guarantee |
| Lemma-K-02-01 | Scaling Flexibility of Disaggregated Storage/Compute | 02.01 | O(1) scaling complexity |
| Lemma-K-02-02 | Resource Utilization of Async Model | 02.01 | CPU utilization improvement |
| Lemma-RW-01 | Statelessness of Compute Nodes | 04.02 | Stateless proof |
| Lemma-RW-02 | Horizontal Scaling Linear Speedup | 04.02 | Scaling efficiency formula |

---

## 3. Code Example Index

### 3.1 By Language

#### Scala Code Examples

| Document | Example Name | Description |
|------|----------|------|
| 01.01 | fs2 basic stream operations | Stream, map, filter, fold |
| 01.01 | Pekko Streams graph construction | Source, Flow, Sink, GraphDSL |
| 01.01 | ZIO Streams effect integration | ZStream, resource safety, backpressure |
| 01.02 | Flink Scala API | DataStream, type safety |
| 01.04 | Cross-library interoperability | fs2↔Pekko↔ZIO conversion |
| 03.01 | Scala WASM host wrapper | WasiProcessor implementation |
| 03.02 | JNI binding code | Scala↔Rust JNI calls |

#### Rust Code Examples

| Document | Example Name | Description |
|------|----------|------|
| 03.01 | Rust WASM module development | WIT, async, WASI 0.3 |
| 03.02 | JNI native method implementation | unsafe, FFI, JNI exports |
| 04.02 | Rust UDF development | #[udf] macro, SIMD optimization |
| 04.05 | SIMD vectorization | AVX2, auto-vectorization |

#### Java Code Examples

| Document | Example Name | Description |
|------|----------|------|
| 02.01 | Async State API | Async state access Java API |
| 02.02 | ProcessFunction | Low-level stream processing |
| 03.01 | Flink WASM UDF integration | FlinkWasiUdfJob |

#### SQL Code Examples

| Document | Example Name | Description |
|------|----------|------|
| 02.04 | Flink SQL window queries | TUMBLE, HOP, SESSION |
| 04.01 | Engine SQL comparison | RisingWave/Materialize/Arroyo |
| 04.02 | RisingWave materialized views | CREATE MATERIALIZED VIEW |

#### Configuration Examples

| Document | Example Name | Description |
|------|----------|------|
| 02.01 | Flink 2.x YAML configuration | Disaggregated storage/compute, Adaptive Scheduler |
| 02.05 | K8s Deployment | FlinkDeployment CRD |
| 04.02 | RisingWave K8s deployment | Compute/Meta/Compactor |
| 05.03 | Multi-cloud deployment configuration | AWS/Azure/GCP |

### 3.2 By Topic

| Topic | Related Code Examples | Main Documents |
|------|-------------|----------|
| **Stream Fundamentals** | map/filter/fold/window | 01.01, 01.04 |
| **Type Safety** | Type Class, HKT | 01.05 |
| **State Management** | State Backend, Checkpoint | 02.03 |
| **Async Programming** | async/await, Future | 03.01 |
| **Interoperability** | WASM, JNI, gRPC | 03.01-03.05 |
| **Performance Optimization** | SIMD, vectorization | 04.05 |
| **Deployment Configuration** | YAML, K8s, Helm | 02.05, 05.03 |

---

## 4. Diagram Index

### 4.1 Mermaid Diagram Statistics

| Type | Count | Main Use |
|------|------|----------|
| graph TB/TD | 25+ | Architecture diagrams, hierarchies |
| flowchart | 15+ | Decision trees, flowcharts |
| sequenceDiagram | 8+ | Sequence diagrams, call chains |
| classDiagram | 3+ | Type structures |
| stateDiagram | 2+ | State machines |
| quadrantChart | 2+ | Comparison matrices |
| radar | 1+ | Capability radar charts |

### 4.2 Key Architecture Diagram Index

| Diagram Name | Location | Description |
|--------|------|------|
| Scala Streaming Ecosystem Panorama | 01.01 | fs2/Pekko/ZIO/Flink relationships |
| Flink 1.x vs 2.x Architecture Comparison | 02.01 | Disaggregated evolution |
| Adaptive Scheduler Decision Flow | 02.01 | Auto-scaling decisions |
| WASI 0.3 Async Execution Model | 03.01 | Scala↔Rust async calls |
| RisingWave Overall Architecture | 04.02 | Tiered storage architecture |
| Flink vs RisingWave Architecture Comparison | 04.02 | Architectural differences |
| Rust Engine Capability Radar | 04.01 | RisingWave/Materialize/Arroyo |
| Technology Selection Decision Tree | 04.01 | Engine selection guide |

### 4.3 Flowchart Index

| Diagram Name | Location | Description |
|--------|------|------|
| WASI 0.2 vs 0.3 Selection Decision | 03.01 | Async I/O selection |
| Stream Library Selection Decision Matrix | 01.01 | fs2/Pekko/ZIO selection |
| Interoperability Scheme Comparison Matrix | 03.05 | WASM/JNI/gRPC selection |
| Engine Selection Decision Tree | 04.01 | Engine selection flow |
| Migration Strategy Flow | 05.02 | Incremental migration |

### 4.4 Sequence Diagram Index

| Diagram Name | Location | Description |
|--------|------|------|
| WASI 0.3 Async Execution Model | 03.01 | Scala→WASM→I/O call chain |
| Rust UDF Execution Flow | 04.02 | Register→Compile→Execute flow |
| Flink Checkpoint Coordination | 02.02 | JM→TM coordination flow |
| gRPC Service Call Chain | 03.03 | Scala↔Rust gRPC calls |

---

## 5. Topic Quick Lookup

### 5.1 Core Concept Lookup Table

| Concept | Definition Location | Implementation Example | Related Theorem |
|------|----------|----------|----------|
| **Disaggregated Storage/Compute** | 02.01 (Def-K-02-01) | ForSt configuration | Thm-K-02-01 |
| **Async State Access** | 02.01 (Def-K-02-04) | AsyncValueState | Lemma-K-02-02 |
| **WASI 0.3** | 03.01 (Def-K-WSI-02) | Rust WASM module | Thm-K-WSI-01 |
| **Materialized View** | 04.02 (Def-RW-01) | CREATE MATERIALIZED VIEW | Thm-RW-01 |
| **Hummock** | 04.02 (Def-RW-03) | Three-layer storage configuration | Lemma-RW-03 |
| **Type Class** | 01.05 | Functor/Monad implementation | Thm-K-01-01 |

### 5.2 FAQ Index

| Question | Answer Location |
|------|----------|
| What are the new features in Flink 2.x? | 02.01 Sections 1-2 |
| How to choose a Scala stream library? | 01.01 Section 5, 01.04 Section 6 |
| WASI 0.3 vs 0.2: how to choose? | 03.01 Section 4.2 |
| What is the difference between RisingWave and Flink? | 04.02 Section 3 |
| How to apply SIMD in stream processing? | 04.05 Section 5 |
| How to deploy Flink 2.x on K8s? | 02.05 Section 6 |
| How to implement Scala↔Rust interoperability? | 03.01-03.05 |
| How to select a stream processing engine? | 04.01 Section 5, 06.02 |

### 5.3 Performance Optimization Guide Index

| Optimization Direction | Related Documents | Key Technologies |
|----------|----------|----------|
| **State Access** | 02.03, 04.02 | ForSt, Hummock caching |
| **Vectorization** | 04.05 | SIMD, AVX2 |
| **Async I/O** | 02.01, 03.01 | async/await, WASI 0.3 |
| **Parallelism Tuning** | 02.01, 02.02 | Adaptive Scheduler |
| **Memory Management** | 04.01, 04.05 | Rust ownership, Arrow |

---

## 6. Dependency Graph

### 6.1 Document Dependencies

```
00-MASTER-INDEX
    │
    ├── 01-scala-ecosystem/
    │       ├── 01.01 (fundamentals) ──┬──► 01.02 ──┬──► 01.04
    │       │                          │            │
    │       └── 01.05 (types) ◄─┘            └──► 01.03
    │
    ├── 02-flink-system/
    │       ├── 02.01 (architecture) ──┬──► 02.02 ──┬──► 02.03
    │       │                          │            │
    │       └── 02.05 ◄────────┴──► 02.04 ◄─┘
    │
    ├── 03-scala-rust-interop/
    │       ├── 03.01 (WASM) ──┬──► 03.04
    │       ├── 03.02 (JNI) ◄──┤
    │       ├── 03.03 (gRPC) ◄─┤
    │       └── 03.05 (comparison) ◄─┘
    │
    ├── 04-rust-engines/
    │       ├── 04.01 (comparison) ──┬──► 04.02
    │       │                        ├──► 04.03
    │       │                        ├──► 04.04
    │       │                        └──► 04.05
    │
    ├── 05-architecture-patterns/
    │       └── 05.01 → 05.02 → 05.03 → 05.04
    │
    ├── 06-trends-2026/
    │       └── 06.01 → 06.02
    │
    └── 99-appendix/
            └── 99.01, 99.02, cross-reference-index
```

### 6.2 Prerequisite Matrix

| Document | Strong Dependencies | Weak Dependencies |
|------|--------|--------|
| 01.02 | 01.01 | Flink fundamentals |
| 01.03 | 01.02 | JVM fundamentals |
| 01.04 | 01.01 | Reactive Streams |
| 01.05 | 01.01 | Category theory fundamentals |
| 02.02 | 02.01 | Networking fundamentals |
| 02.03 | 02.01, 02.02 | Storage fundamentals |
| 02.04 | 02.01 | SQL fundamentals |
| 02.05 | 02.01 | K8s fundamentals |
| 03.01 | - | WASM/WASI fundamentals |
| 03.02 | 03.01 | JNI fundamentals |
| 03.03 | - | gRPC fundamentals |
| 03.04 | 03.01 | Serverless fundamentals |
| 03.05 | 03.01-03.04 | - |
| 04.01 | - | Stream processing fundamentals |
| 04.02 | 04.01 | Database fundamentals |
| 04.03 | 04.01 | Consistency model fundamentals |
| 04.04 | 04.01 | Edge computing fundamentals |
| 04.05 | 04.01 | SIMD fundamentals |
| 05.01 | 02.01, 04.01 | Architecture design fundamentals |
| 05.02 | 05.01 | Migration experience |
| 05.03 | 02.05, 05.01 | Cloud platform experience |
| 05.04 | 05.03 | Edge deployment experience |
| 06.01 | All | Industry insights |
| 06.02 | 06.01, All | Decision frameworks |

---

## Appendix: Index Usage Guide

### Quick Lookup Tips

1. **Look up term definitions**: Browse [99.01-glossary.md](99.01-glossary.md) by category
2. **Look up references**: Use the category index in [99.02-references.md](99.02-references.md)
3. **Look up formal definitions**: Use the definition index table in Section 2 of this document
4. **Look up code examples**: Use the categorized index in Section 3 of this document
5. **Look up diagrams**: Use the diagram index in Section 4 of this document

### Cross-Reference Format

- Document reference: `[chapter.doc_id-name](#)`
- Definition reference: `Def-K-{doc_id}-{seq}`
- Theorem reference: `Thm-K-{doc_id}-{seq}`
- Lemma reference: `Lemma-K-{doc_id}-{seq}`
- Citation reference: `[^{n}]`

---

*Document Version: v1.0 | Created: 2026-04-07 | Coverage: 28 documents | Total index entries: 300+*
