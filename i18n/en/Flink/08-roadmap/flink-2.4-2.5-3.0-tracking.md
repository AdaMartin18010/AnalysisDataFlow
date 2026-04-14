---
title: "Flink Version Tracking Report (2.0-3.0)"
translation_status: ai_translated_reviewed
source_version: v4.1
last_sync: "2026-04-15"
---

<!-- Version status marker: status=tracking, target=2026 -->
> **Status**: Forward-looking | **Estimated Release**: Starting 2026-Q3 | **Last Updated**: 2026-04-12
>
> ⚠️ Features described in this document are in early discussion stages and have not been officially released. Implementation details may change.

> **Version Tracking Notes**
>
> **This document is compiled based on official Apache Flink releases and community discussions**
>
> | Attribute | Status |
> |-----------|--------|
> | **Flink 2.0-2.2** | Released - Based on official release notes |
> | **Flink 2.4/2.5/3.0** | Forward-looking planning - Based on community discussions and trend analysis |
> | **Document Nature** | Version tracking / Roadmap analysis / Impact assessment |
> | **Last Updated** | 2026-04-09 |
>
> **Reference Sources**:
>
> - Apache Flink Official Releases: <https://flink.apache.org/downloads/>
> - Flink Official Roadmap: <https://flink.apache.org/what-is-flink/roadmap/>
> - Flink JIRA: <https://issues.apache.org/jira/browse/FLINK>

---

# Flink Version Tracking Report (2.0-3.0)

> **Stage**: Flink/08-roadmap | **Prerequisites**: Flink 2.x Roadmap | **Formality Level**: L3

---

## Executive Summary

| Version | Status | Release Date | Major Features | Project Documentation Status |
|---------|--------|--------------|----------------|------------------------------|
| Flink 2.0 | Released | 2025-03-24 | Disaggregated state storage, async execution, ForSt DB | Updated |
| Flink 2.1 | Released | 2025-07-31 | Materialized table enhancements, performance optimizations | Updated |
| Flink 2.2 | Released | 2025-12-04 | Continuous improvements, stability enhancements | Updated |
| Flink 2.3 | In planning | Estimated 2026 Q2 | AI Agent integration preview | Needs update |
| Flink 2.4 | In planning | Estimated 2026 Q4 | AI Agent GA, Serverless Beta | Needs update |
| Flink 2.5 | Forward-looking | Estimated 2027 Q1 | Deeper batch-stream unification | In planning |
| Flink 3.0 | Vision | Estimated 2027+ | Major architectural refactoring | Concept stage |

---

## Part 1: Released Versions (Officially Confirmed)

### Flink 2.0 (Released 2025-03-24)

#### New Feature 1: Disaggregated State Storage and Management

- **Description**: Introduces a disaggregated state storage architecture using remote storage (e.g., S3, HDFS) as the primary state store, decoupling compute and storage resources
- **Technical Implementation**:
  - ForSt DB: A state backend designed specifically for disaggregated storage
  - Async execution model: Eliminates state access blocking
  - Tiered caching: A hybrid architecture of local cache + remote storage
- **Impact**:
  - Supports larger state scales (hundreds of TB)
  - Faster scaling and failure recovery
  - Better suited for cloud-native deployments
- **Project Documentation Status**: Updated
  - See: Flink/02-core/flink-2.0-forst-state-backend.md
  - See: Flink/02-core/flink-2.0-async-execution-model.md

#### New Feature 2: Materialized Table

- **Description**: A unified batch-stream data processing abstraction that automatically maintains query result freshness
- **Technical Implementation**:
  - Declarative data freshness configuration
  - Automatic stream/batch execution mode selection
  - Incremental refresh optimization
- **Impact**:
  - Simplifies ETL pipeline development
  - Unified batch-stream development experience
  - Reduces user cognitive burden
- **Project Documentation Status**: Updated
  - See: Flink/03-api/03.02-table-sql-api/flink-materialized-table-deep-dive.md
  - See: Flink/03-api/03.02-table-sql-api/materialized-tables.md

#### New Feature 3: API Cleanup and Modernization

- **Description**: Removes long-deprecated APIs and simplifies the architecture
- **Change List**:
  - Removes DataSet API
  - Removes Scala API (moved to community maintenance)
  - Removes SinkFunction V1
  - Removes TableSource/TableSink API
  - Unifies Sink API V2 as the standard
- **Impact**:
  - Requires migration of old code
  - Simplifies maintenance burden
  - Clearer API hierarchy
- **Project Documentation Status**: Updated
  - See: Flink/01-concepts/flink-1.x-vs-2.0-comparison.md

#### New Feature 4: Java Version Requirement Upgrade

- **Description**: Minimum Java version upgraded from 8 to 11
- **Impact**:
  - Requires JDK version upgrade
  - Can leverage Java 11+ new features
  - Better performance and security
- **Project Documentation Status**: Updated
  - See: Flink/09-practices/09.03-performance-tuning/jdk-11-migration-guide.md

---

### Flink 2.1 (Released 2025-07-31)

#### New Feature 1: Materialized Table Enhancements

- **Description**: Materialized table functionality upgraded from MVP to production-ready
- **Enhancements**:
  - Automatic refresh scheduling optimization
  - Incremental update performance improvement
  - Deep integration with lakehouse storage (Iceberg/Paimon)
- **Project Documentation Status**: Updated

#### New Feature 2: SQL Performance Optimization

- **Description**: Query optimizer improvements
- **Enhancements**:
  - CBO (Cost-Based Optimization) enhancements
  - Runtime Filter support
  - Dynamic Partition Pruning optimization
- **Project Documentation Status**: Updated

---

### Flink 2.2 (Released 2025-12-04)

#### New Feature 1: Stability Enhancements

- **Description**: Bug fixes and stability improvements
- **Content**: 51 bug fixes, security vulnerability patches
- **Project Documentation Status**: Updated

#### New Feature 2: Performance Optimization

- **Description**: Continuous performance optimization
- **Project Documentation Status**: Updated

---

## Part 2: Forward-Looking Planned Versions (Based on Community Discussions)

> **The following content is forward-looking analysis based on community discussions, not official commitments**

### Flink 2.3 (In planning, Estimated 2026 Q2)

#### Planned Feature 1: AI Agent Integration Preview (FLIP-531 Preview)

- **Description**: Preview version of Flink AI Agents, supporting building and running AI Agents in Flink
- **Planned Features**:
  - Event-driven Agent runtime
  - MCP (Model Context Protocol) protocol support
  - State management as Agent memory
  - Full replayability
- **Impact Assessment**:
  - Provides infrastructure for real-time AI applications
  - Combines stream processing and LLM inference
  - New application scenarios (intelligent customer service, real-time decision-making, etc.)
- **Project Documentation Status**: Needs update
  - To be added: Flink/06-ai-ml/flink-agents-flip-531.md

#### Planned Feature 2: Vector Search Enhancements

- **Description**: Native vector search support improvements
- **Planned Features**:
  - VECTOR_SEARCH SQL function optimization
  - Enhanced integration with vector databases
  - RAG (Retrieval-Augmented Generation) support
- **Project Documentation Status**: Needs update

---

### Flink 2.4 (Forward-looking, Estimated 2026 Q4)

#### Planned Feature 1: AI Agent GA (FLIP-531 GA)

- **Description**: AI Agent functionality upgraded from preview to general availability
- **Planned Features**:
  - Multi-Agent coordination framework
  - Agent version management and canary releases
  - Production-grade monitoring and observability
  - Agent marketplace/registry
- **Project Documentation Status**: Needs update

#### Planned Feature 2: Serverless Flink Beta

- **Description**: True serverless stream processing capabilities
- **Planned Features**:
  - Scale-to-Zero (zero cost when no traffic)
  - Millisecond-level cold start
  - Load-based intelligent auto-scaling
  - Billed by actual data processed
- **Impact Assessment**:
  - Greatly reduces idle costs
  - Better suited for event-driven scenarios
  - Simplifies operations
- **Project Documentation Status**: Needs update
  - See: Flink/04-runtime/04.01-deployment/serverless-flink-ga-guide.md

#### Planned Feature 3: Adaptive Execution Engine v2

- **Description**: ML-driven dynamic optimization
- **Planned Features**:
  - ML model predicts optimal configuration
  - Real-time execution plan rewriting
  - Workload-aware optimization
  - Historical execution learning
- **Project Documentation Status**: In planning

---

### Flink 2.5 (Forward-looking, Estimated 2027 Q1)

#### Planned Feature 1: Unified Batch-Stream Execution Engine (FLIP-435)

- **Description**: A truly unified execution engine that eliminates the batch-stream boundary
- **Planned Features**:
  - Unified execution plan generator
  - Adaptive execution mode selection
  - Unified state management
  - Unified fault tolerance mechanism
  - Mixed execution (streaming operators and batch operators coexisting in the same job)
- **Impact Assessment**:
  - Completely unified development experience
  - Automatic runtime optimization
  - Reduced architectural complexity
- **Project Documentation Status**: Needs update
  - See: Flink/08-roadmap/08.02-flink-25/flink-25-roadmap.md

#### Planned Feature 2: Serverless Flink GA

- **Description**: Serverless functionality upgraded from Beta to GA
- **Planned Features**:
  - Cold start < 500ms
  - Predictive auto-scaling
  - Cost optimization reports
  - Fully managed experience
- **Project Documentation Status**: Needs update

#### Planned Feature 3: WebAssembly UDF GA

- **Description**: WASM UDF production-ready
- **Planned Features**:
  - WASI Preview 2 support
  - Multi-language UDF (Rust/Go/C++/Zig)
  - UDF marketplace/registry
  - Zero-copy data transfer
- **Project Documentation Status**: Needs update
  - See: Flink/03-api/09-language-foundations/flink-25-wasm-udf-ga.md

---

### Flink 3.0 (Vision, Estimated 2027+)

#### Planned Direction 1: Unified Execution Layer

- **Description**: A completely unified execution engine
- **Planned Content**:
  - Unified runtime for streaming, batch, and interactive queries
  - Adaptive execution strategy selection
  - Global optimizer
- **Project Documentation Status**: Concept stage
  - See: Flink/08-roadmap/08.03-flink-30/flink-30-architecture-redesign.md

#### Planned Direction 2: Next-Generation State Management

- **Description**: Tiered storage architecture
- **Planned Content**:
  - L1: Local memory (NVM/DRAM)
  - L2: Local SSD
  - L3: Remote high-performance storage
  - L4: Object storage
  - Intelligent caching strategies
- **Project Documentation Status**: Concept stage

#### Planned Direction 3: Cloud-Native Architecture 2.0

- **Description**: Deep cloud-native support
- **Planned Content**:
  - Fully elastic scheduling
  - Multi-cloud native support
  - FinOps integration
  - Enhanced spot instance support
- **Project Documentation Status**: Concept stage

---

## Part 3: Document Update Checklist

### High Priority Updates

| Document Path | Update Reason | Estimated Effort |
|---------------|---------------|------------------|
| Flink/06-ai-ml/flink-agents-flip-531.md | FLIP-531 actual release status tracking | 2 hours |
| Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md | Update to actual roadmap | 1 hour |
| Flink/08-roadmap/08.02-flink-25/flink-25-roadmap.md | Update release timeline | 1 hour |
| Flink/02-core/forst-state-backend.md | Supplement 2.0 GA features | 1 hour |

### Medium Priority Updates

| Document Path | Update Reason | Estimated Effort |
|---------------|---------------|------------------|
| Flink/03-api/03.02-table-sql-api/materialized-tables.md | Supplement 2.1 enhancement features | 1 hour |
| Flink/04-runtime/04.01-deployment/serverless-flink-ga-guide.md | Distinguish Beta/GA stages | 1 hour |
| Flink/01-concepts/flink-architecture-evolution-1x-to-2x.md | Supplement 2.0-2.2 evolution | 2 hours |

### Low Priority Updates

| Document Path | Update Reason | Estimated Effort |
|---------------|---------------|------------------|
| Flink/08-roadmap/08.03-flink-30/flink-30-architecture-redesign.md | Update 3.0 planning status | 1 hour |
| Flink/00-meta/version-tracking.md | Sync version info | 0.5 hours |

---

## Part 4: New Feature Impact Assessment

### Impact on Existing Users

| Version | Impact Type | Impact Level | Recommended Action |
|---------|-------------|--------------|--------------------|
| Flink 2.0 | API changes | High | Migrate DataSet code, upgrade JDK |
| Flink 2.0 | State backend | Medium | Evaluate ForSt DB migration |
| Flink 2.1 | Materialized tables | Low | Optional adoption of new features |
| Flink 2.2 | Stability | Low | Recommended upgrade |
| Flink 2.3+ | AI features | Medium | Watch preview versions, evaluate use cases |

### Impact Matrix on Project Documentation

```
Impact Level:
                    High Impact
                       |
    AI Agent features  |       Requires new/major document updates
                       |
    Serverless arch    |       Requires deployment doc updates
                       |
    Batch-stream unification |   Requires unified concept docs
                       |
    Materialized tables |       Requires example supplements
                       |
    Disaggregated state storage | Requires core concept updates
                       |
                    Low Impact
```

### Recommended Document Update Order

1. **Immediate updates** (1-2 weeks)
   - Version tracking documents
   - 2.0 release notes Chinese compilation
   - Migration guides

2. **Short-term updates** (within 1 month)
   - AI Agent related documents
   - Serverless deployment guides
   - Materialized table usage guides

3. **Medium-term updates** (within 3 months)
   - Batch-stream unified documentation
   - Performance optimization guides
   - Best practices updates

---

## Part 5: Reference Resources

### Official Resources

- Apache Flink Official Downloads: <https://flink.apache.org/downloads/>
- Flink 2.0.0 Release Notes: <https://flink.apache.org/2025/03/24/apache-flink-2.0.0-a-new-era-of-real-time-data-processing/>
- Flink Official Roadmap: <https://flink.apache.org/what-is-flink/roadmap/>
- FLIP Proposal List: <https://github.com/apache/flink/tree/main/flink-docs/docs/flips/>

### Community Resources

- Flink Forward 2024 Talks
- Flink User Mailing List: <https://flink.apache.org/community/>
- Flink JIRA: <https://issues.apache.org/jira/browse/FLINK>

---

## Version History

| Date | Version | Changes | Updated By |
|------|---------|---------|------------|
| 2026-04-09 | v1.0 | Initial version, integrating official release info and forward-looking plans | Agent |

---

*Document Version: v1.0 | Formality Level: L3 | Last Updated: 2026-04-09*
