---
title: "Flink Connectors Ecosystem Complete Guide"
lang: en
source: "Flink/05-ecosystem/05.01-connectors/flink-connectors-ecosystem-complete-guide.md"
---

# Flink Connectors Ecosystem Complete Guide

> **Stage**: Flink/04-connectors | **Prerequisites**: [kafka-integration-patterns.md](./kafka-integration-patterns.md), [flink-iceberg-integration.md](./flink-iceberg-integration.md), [flink-cdc-3.0-data-integration.md](./flink-cdc-3.0-data-integration.md) | **Formalization Level**: L4 | **Coverage**: Message Queue / File System / Database / Lakehouse / CDC

---

## Table of Contents

- [Flink Connectors Ecosystem Complete Guide](#flink-connectors-ecosystem-complete-guide)
  - [Table of Contents](#table-of-contents)
  - [1. Definitions](#1-definitions)
    - [Def-F-04-100 (Flink Connector Formal Definition)](#def-f-04-100-flink-connector-formal-definition)
    - [Def-F-04-101 (Connector Delivery Guarantee Semantics)](#def-f-04-101-connector-delivery-guarantee-semantics)
    - [Def-F-04-102 (Source Connector Interface Contract)](#def-f-04-102-source-connector-interface-contract)
    - [Def-F-04-103 (Sink Connector Interface Contract)](#def-f-04-103-sink-connector-interface-contract)
    - [Def-F-04-104 (Connector Ecosystem Layered Model)](#def-f-04-104-connector-ecosystem-layered-model)
  - [2. Properties](#2-properties)
    - [Lemma-F-04-100 (Connector Composition Closure)](#lemma-f-04-100-connector-composition-closure)
    - [Lemma-F-04-101 (Delivery Guarantee Transitivity)](#lemma-f-04-101-delivery-guarantee-transitivity)
    - [Prop-F-04-100 (End-to-End Consistency Constraints)](#prop-f-04-100-end-to-end-consistency-constraints)
    - [Prop-F-04-101 (Connector Parallelism Scalability)](#prop-f-04-101-connector-parallelism-scalability)
  - [3. Relations](#3-relations)
    - [3.1 Connector Classification](#31-connector-classification)
    - [3.2 Connector-to-Storage Mapping](#32-connector-to-storage-mapping)
    - [3.3 Connector Version Compatibility Matrix](#33-connector-version-compatibility-matrix)
  - [4. Argumentation](#4-argumentation)
    - [4.1 Connector Selection Decision Framework](#41-connector-selection-decision-framework)
    - [4.2 Performance Trade-off Analysis](#42-performance-trade-off-analysis)
    - [4.3 Failure Scenarios \& Recovery Strategies](#43-failure-scenarios--recovery-strategies)
  - [5. Proof / Engineering Argument](#5-proof--engineering-argument)
    - [Thm-F-04-100 (Connector Ecosystem Completeness Theorem)](#thm-f-04-100-connector-ecosystem-completeness-theorem)
    - [Thm-F-04-101 (Multi-Connector Composition Consistency Theorem)](#thm-f-04-101-multi-connector-composition-consistency-theorem)
  - [6. Examples](#6-examples)
    - [6.1 Message Queue Connectors](#61-message-queue-connectors)
      - [6.1.1 Kafka Connector](#611-kafka-connector)
      - [6.1.2 Apache Pulsar Connector](#612-apache-pulsar-connector)
      - [6.1.3 RabbitMQ Connector](#613-rabbitmq-connector)
      - [6.1.4 Amazon Kinesis Connector](#614-amazon-kinesis-connector)
      - [6.1.5 Google Cloud Pub/Sub Connector](#615-google-cloud-pubsub-connector)
      - [6.1.6 MQTT Connector](#616-mqtt-connector)
    - [6.2 File System Connectors](#62-file-system-connectors)
      - [6.2.1 General File System Configuration](#621-general-file-system-configuration)
      - [6.2.2 File Source (Bulk Format)](#622-file-source-bulk-format)
      - [6.2.3 File Sink (Streaming)](#623-file-sink-streaming)
    - [6.3 Database Connectors](#63-database-connectors)
      - [6.3.1 JDBC Connector](#631-jdbc-connector)
      - [6.3.2 Apache Cassandra Connector](#632-apache-cassandra-connector)
      - [6.3.3 Apache HBase Connector](#633-apache-hbase-connector)
      - [6.3.4 Elasticsearch Connector](#634-elasticsearch-connector)
      - [6.3.5 MongoDB Connector](#635-mongodb-connector)
      - [6.3.6 Redis Connector](#636-redis-connector)
      - [6.3.7 InfluxDB Connector](#637-influxdb-connector)
    - [6.4 Lakehouse Connectors](#64-lakehouse-connectors)
      - [6.4.1 Apache Iceberg Connector](#641-apache-iceberg-connector)
      - [6.4.2 Apache Hudi Connector](#642-apache-hudi-connector)
      - [6.4.3 Apache Paimon Connector](#643-apache-paimon-connector)
      - [6.4.4 Delta Lake Connector](#644-delta-lake-connector)
      - [6.4.5 Apache Fluss Connector](#645-apache-fluss-connector)
    - [6.5 CDC Connectors](#65-cdc-connectors)
      - [6.5.1 Flink CDC 3.0 Basic Configuration](#651-flink-cdc-30-basic-configuration)
      - [6.5.2 CDC Pipeline YAML Configuration](#652-cdc-pipeline-yaml-configuration)
      - [6.5.3 CDC to Lakehouse](#653-cdc-to-lakehouse)
  - [7. Visualizations](#7-visualizations)
    - [7.1 Connector Ecosystem Panorama](#71-connector-ecosystem-panorama)
    - [7.2 Connector Selection Decision Tree](#72-connector-selection-decision-tree)
    - [7.3 Data Flow Integration Architecture](#73-data-flow-integration-architecture)
    - [7.4 Connector State Machine](#74-connector-state-machine)
  - [8. Configuration \& Performance](#8-configuration--performance)
    - [8.1 Global Configuration Best Practices](#81-global-configuration-best-practices)
    - [8.2 Connector Performance Comparison Matrix](#82-connector-performance-comparison-matrix)
    - [8.3 Common Issues Troubleshooting Guide](#83-common-issues-troubleshooting-guide)
  - [9. References](#9-references)

---

## 1. Definitions

### Def-F-04-100 (Flink Connector Formal Definition)

**Definition**: A Flink connector is a bridge connecting the Flink compute engine with external data systems, implementing unified data read/write interfaces and supporting both batch and stream processing modes.

**Formal Structure**:

```
FlinkConnector = ⟨Type, Interface, Semantics, Config, Compatibility⟩

Where:
- Type: {Source, Sink, Lookup, Scan}
- Interface: DataStream API | Table API | SQL
- Semantics: {EXACTLY_ONCE, AT_LEAST_ONCE, AT_MOST_ONCE}
- Config: Configuration parameter space ⟨name, type, default, constraint⟩
- Compatibility: Version compatibility ⟨FlinkVersion, ExternalSystemVersion⟩
```

**Connector Type Classification**:

| Type | Direction | Function | Typical Scenario |
|------|-----------|----------|------------------|
| **Source** | Input | Read data from external systems | Kafka consumption, database query |
| **Sink** | Output | Write data to external systems | Data persistence, result output |
| **Lookup** | Dimension table | Point query external systems | Dimension table join, data enrichment |
| **Scan** | Batch read | Batch scan external data | Offline analysis, full sync |

---

### Def-F-04-101 (Connector Delivery Guarantee Semantics)

**Definition**: Connector delivery guarantee defines the reliability level of data during transmission, divided into three levels:

**Formal Definition**:

```
Let:
- E: Event set
- Src: Records produced by Source connector
- Sink: Records written by Sink connector
- Ideal case: ∀e ∈ Src, ∃! s ∈ Sink: e ~ s (one-to-one correspondence)

Delivery guarantees:
┌─────────────────────────────────────────────────────────────┐
│ EXACTLY_ONCE:                                               │
│   ∀e ∈ Src: |{s ∈ Sink | s ~ e}| = 1                       │
│   Each event is processed exactly once, no loss, no dup    │
├─────────────────────────────────────────────────────────────┤
│ AT_LEAST_ONCE:                                              │
│   ∀e ∈ Src: |{s ∈ Sink | s ~ e}| ≥ 1                       │
│   Each event is processed at least once, duplicates allowed │
├─────────────────────────────────────────────────────────────┤
│ AT_MOST_ONCE:                                               │
│   ∀e ∈ Src: |{s ∈ Sink | s ~ e}| ≤ 1                       │
│   Each event is processed at most once, loss allowed        │
└─────────────────────────────────────────────────────────────┘
```

**Connector Delivery Guarantee Capabilities**:

| Connector | Source Guarantee | Sink Guarantee | Implementation Mechanism |
|-----------|------------------|----------------|--------------------------|
| Kafka | EXACTLY_ONCE | EXACTLY_ONCE | Offset + Transaction |
| Pulsar | EXACTLY_ONCE | EXACTLY_ONCE | Cursor + Transaction |
| JDBC | AT_LEAST_ONCE | EXACTLY_ONCE | Checkpoint + XA |
| Iceberg | EXACTLY_ONCE | EXACTLY_ONCE | Snapshot isolation + 2PC |
| Files | EXACTLY_ONCE | EXACTLY_ONCE | File atomic rename |
| Redis | AT_LEAST_ONCE | AT_LEAST_ONCE | Async write |

---

### Def-F-04-102 (Source Connector Interface Contract)

**Definition**: A Source connector must implement the `Source` interface, supporting split enumeration, reader creation, and offset management.

**Formal Contract**:

```java
// [Pseudo-code snippet - not directly runnable] Core logic only
interface Source<T, SplitT extends SourceSplit, EnumChkT>
    extends SourceReaderFactory<T, SplitT> {

    // Create split enumerator, responsible for discovering and assigning data splits
    SplitEnumerator<SplitT, EnumChkT> createEnumerator();

    // Restore split enumerator from checkpoint
    SplitEnumerator<SplitT, EnumChkT> restoreEnumerator(EnumChkT checkpoint);

    // Create SourceReader factory
    SourceReader<T, SplitT> createReader(SourceReaderContext context);

    // Serialize/deserialize splits
    SimpleVersionedSerializer<SplitT> getSplitSerializer();
    SimpleVersionedSerializer<EnumChkT> getEnumeratorCheckpointSerializer();
}
```

**Source Read Semantics**:

| Semantics | Definition | Applicable Scenario |
|-----------|------------|---------------------|
| **Bounded** | Finite dataset, ends after read completion | Batch processing, historical data |
| **Unbounded** | Infinite data stream, continuous read | Stream processing, real-time data |
| **Snapshot** | Point-in-time snapshot read | Consistent backup, time travel |
| **Incremental** | Incremental read of changed data | CDC, incremental sync |

---

### Def-F-04-103 (Sink Connector Interface Contract)

**Definition**: A Sink connector must implement the `Sink` interface, supporting two-phase commit for write operations to guarantee Exactly-Once semantics.

**Formal Contract**:

```java
// [Pseudo-code snippet - not directly runnable] Core logic only
interface Sink<InputT> {
    // Create SinkWriter, responsible for actual writing
    SinkWriter<InputT> createWriter(InitContext context);

    // Create committer (for two-phase commit)
    Optional<Committer<?>> createCommitter();

    // Create global committer (for global coordination)
    Optional<GlobalCommitter<?, ?>> createGlobalCommitter();
}

// Two-phase commit interface
interface TwoPhaseCommitSinkFunction<IN, TXN, CONTEXT> {
    void beginTransaction();                    // Start transaction
    void preCommit(TXN transaction);           // Pre-commit
    void commit(TXN transaction);              // Commit transaction
    void abort(TXN transaction);               // Abort transaction
}
```

**Sink Write Modes**:

| Mode | Latency | Throughput | Consistency |
|------|---------|------------|-------------|
| **Append** | Low | High | Eventual consistency |
| **Upsert** | Medium | Medium | Deduplication by primary key |
| **Batch** | High | Highest | Checkpoint boundary |
| **Streaming** | Low | High | Transaction guarantee |

---

### Def-F-04-104 (Connector Ecosystem Layered Model)

**Definition**: The Flink connector ecosystem adopts a layered architecture, forming a complete integration system from underlying storage to upper-layer applications.

**Layered Structure**:

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 5: Application Layer                                   │
│  - CDC data sync, real-time data warehouse, streaming ETL,  │
│    AI/ML feature engineering                                 │
├─────────────────────────────────────────────────────────────┤
│ Layer 4: Processing Layer                                    │
│  - Flink SQL/DataStream API, window computation, state       │
│    processing                                                │
├─────────────────────────────────────────────────────────────┤
│ Layer 3: Connector Layer                                     │
│  - Source/Sink Connectors, Format serialization              │
├─────────────────────────────────────────────────────────────┤
│ Layer 2: Protocol Layer                                      │
│  - Kafka Protocol, JDBC, HTTP/REST, File Format              │
├─────────────────────────────────────────────────────────────┤
│ Layer 1: Storage Layer                                       │
│  - Message queues, databases, file systems, object storage   │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Properties

### Lemma-F-04-100 (Connector Composition Closure)

**Lemma**: When multiple Flink connectors are used in combination, the semantics of the entire data flow remain closed under specific conditions.

**Proof Sketch**:

```
Let:
- C₁, C₂, ..., Cₙ be a set of connectors
- Semantic function of each connector: fᵢ: Input → Output
- Composed semantics: F = fₙ ∘ fₙ₋₁ ∘ ... ∘ f₁

Closure conditions:
1. Type compatibility: ∀i: Output(fᵢ) ⊆ Input(fᵢ₊₁)
2. Serialization consistency: Adjacent connectors use the same serialization format
3. Semantic compatibility: Upstream delivery guarantee ≥ downstream requirement

If the above conditions are satisfied, the combined data flow maintains deterministic semantics.
```

**Examples**:

| Composition | Closed? | Reason |
|-------------|---------|--------|
| Kafka Source → Iceberg Sink | ✅ | Both support EXACTLY_ONCE |
| JDBC Source → Kafka Sink | ✅ | JDBC AT_LEAST_ONCE + Kafka EOS |
| Files Source → Redis Sink | ✅ | Eventual consistency acceptable |
| Kafka Source → JDBC Sink (no XA) | ⚠️ | JDBC Sink requires extra config for consistency |

---

### Lemma-F-04-101 (Delivery Guarantee Transitivity)

**Lemma**: End-to-end delivery guarantee is determined by the weakest connector in the data flow.

**Formal Statement**:

```
Let the data flow contain n connectors with delivery guarantees g₁, g₂, ..., gₙ
where guarantee level ordering: AT_MOST_ONCE < AT_LEAST_ONCE < EXACTLY_ONCE

End-to-end guarantee: G_end_to_end = min(g₁, g₂, ..., gₙ)

Examples:
- Kafka Source (EXACTLY_ONCE) → Processing → JDBC Sink (AT_LEAST_ONCE)
- Result: End-to-end guarantee is AT_LEAST_ONCE
```

**Improvement Strategies**:

| Scenario | Strategy | Result |
|----------|----------|--------|
| Source is AT_LEAST_ONCE | Enable idempotent Sink | Equivalent EXACTLY_ONCE |
| Sink is AT_LEAST_ONCE | Use transactional Sink (e.g., Kafka) | Upgrade to EXACTLY_ONCE |
| Intermediate operators | Enable Checkpoint | Maintain upstream guarantee |

---

### Prop-F-04-100 (End-to-End Consistency Constraints)

**Proposition**: Achieving end-to-end Exactly-Once requires satisfying three necessary conditions:

1. **Replayable Source**: Supports re-reading from a specific position
2. **Engine Consistency**: Flink Checkpoint guarantees internal state consistency
3. **Transactional Sink**: Supports two-phase commit or idempotent write

**Formal Derivation**:

```
ExactlyOnce(Source, Engine, Sink) ⟺
    Replayable(Source) ∧
    ConsistentCheckpoint(Engine) ∧
    (Transactional(Sink) ∨ Idempotent(Sink))
```

**Connector Satisfaction Levels**:

| Connector | Replayable | Transactional | Idempotent | EO Support |
|-----------|------------|---------------|------------|------------|
| Kafka | ✅ Offset | ✅ 2PC | ✅ Idempotent producer | ✅ |
| Pulsar | ✅ Cursor | ✅ Transaction | ✅ | ✅ |
| Iceberg | ✅ Snapshot | ✅ 2PC | ✅ | ✅ |
| JDBC | ❌ Query-dependent | ⚠️ XA limited | ❌ | ⚠️ |
| Redis | ❌ | ❌ | ✅ Idempotent ops | ⚠️ |
| Files | ✅ File position | ✅ Atomic rename | ✅ | ✅ |

---

### Prop-F-04-101 (Connector Parallelism Scalability)

**Proposition**: Connector parallelism is limited by the external system's sharding/partitioning capability.

**Formal Analysis**:

```
Let:
- P_Flink: Flink parallelism
- P_External: External system partition count

Optimal parallelism: P_optimal = min(P_Flink, P_External)

If P_Flink > P_External:
  - Some subtasks idle, resource waste

If P_Flink < P_External:
  - Single subtask processes multiple partitions
  - Potential data skew
```

**Connector Parallelism Constraints**:

| Connector | Partition Basis | Max Parallelism | Dynamic Scaling |
|-----------|-----------------|-----------------|-----------------|
| Kafka | Topic Partition | Partition count | ✅ Supported |
| Pulsar | Partition | Partition count | ✅ Supported |
| JDBC | Chunk/Shard | DB connection limit | ⚠️ Limited |
| Iceberg | File Split | File count | ✅ Supported |
| Files | Block/File | File count | ✅ Supported |
| Elasticsearch | Shard | Shard count | ⚠️ Limited |

---

## 3. Relations

### 3.1 Connector Classification

**Message Queue Connectors**:

```mermaid
graph TD
    MQ[Message Queue Connectors] --> KAFKA[Apache Kafka]
    MQ --> PULSAR[Apache Pulsar]
    MQ --> RABBIT[RabbitMQ]
    MQ --> KINESIS[Amazon Kinesis]
    MQ --> PUBSUB[Google Cloud Pub/Sub]
    MQ --> MQTT[MQTT Broker]

    KAFKA --> K_SOURCE[Kafka Source<br/>Offset Management]
    KAFKA --> K_SINK[Kafka Sink<br/>Transaction Support]

    PULSAR --> P_SOURCE[Pulsar Source<br/>Cursor Management]
    PULSAR --> P_SINK[Pulsar Sink<br/>Transaction Support]
```

**File System Connectors**:

```mermaid
graph TD
    FS[File System Connectors] --> LOCAL[Local File System]
    FS --> HDFS[HDFS]
    FS --> S3[Amazon S3]
    FS --> GCS[Google Cloud Storage]
    FS --> AZURE[Azure Blob Storage]
    FS --> OSS[Alibaba OSS]

    S3 --> S3_PARQUET[Parquet Format]
    S3 --> S3_ORC[ORC Format]
    S3 --> S3_CSV[CSV Format]
    S3 --> S3_JSON[JSON Format]

    HDFS --> HIVE_PARTITION[Hive Partitioning]
    HDFS --> BUCKETING[Bucketed Storage]
```

**Database Connectors**:

```mermaid
graph TD
    DB[Database Connectors] --> JDBC[JDBC Connector]
    DB --> CASSANDRA[Apache Cassandra]
    DB --> HBASE[Apache HBase]
    DB --> ES[Elasticsearch]
    DB --> MONGODB[MongoDB]
    DB --> REDIS[Redis]
    DB --> INFLUX[InfluxDB]

    JDBC --> MYSQL[MySQL]
    JDBC --> PG[PostgreSQL]
    JDBC --> ORACLE[Oracle]
    JDBC --> SQLSERVER[SQL Server]
    JDBC --> DB2[DB2]
```

**Lakehouse Connectors**:

```mermaid
graph TD
    LAKE[Lakehouse Connectors] --> ICEBERG[Apache Iceberg]
    LAKE --> HUDI[Apache Hudi]
    LAKE --> PAIMON[Apache Paimon]
    LAKE --> DELTA[Delta Lake]
    LAKE --> FLUSS[Apache Fluss]

    ICEBERG --> ICE_SOURCE[Source<br/>Snapshot Read]
    ICEBERG --> ICE_SINK[Sink<br/>UPSERT/Append]
    ICEBERG --> ICE_CATALOG[Catalog<br/>Metadata Management]
```

---

### 3.2 Connector-to-Storage Mapping

**Feature Mapping Matrix**:

| Storage System | Source | Sink | Lookup | CDC Source | Transaction | Unified Batch/Stream |
|----------------|--------|------|--------|------------|-------------|----------------------|
| **Kafka** | ✅ | ✅ | ❌ | ✅ (CDC) | ✅ | ✅ |
| **Pulsar** | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| **RabbitMQ** | ✅ | ✅ | ❌ | ❌ | ❌ | ⚠️ |
| **Kinesis** | ✅ | ✅ | ❌ | ❌ | ⚠️ | ✅ |
| **JDBC** | ✅ | ✅ | ✅ | ⚠️ (needs CDC) | ⚠️ (XA) | ✅ |
| **Cassandra** | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| **HBase** | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| **Elasticsearch** | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| **MongoDB** | ✅ | ✅ | ✅ | ✅ (CDC) | ⚠️ | ✅ |
| **Redis** | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| **Iceberg** | ✅ | ✅ | ❌ | ✅ (CDC) | ✅ | ✅ |
| **Hudi** | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| **Paimon** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

### 3.3 Connector Version Compatibility Matrix

**Flink Version to Connector Version Mapping**:

| Connector | Flink 1.14 | Flink 1.15 | Flink 1.16 | Flink 1.17 | Flink 1.18 | Flink 1.19+ |
|-----------|------------|------------|------------|------------|------------|-------------|
| **Kafka** | 1.14.x | 1.15.x | 1.16.x | 3.0.x | 3.1.x | 3.2.x |
| **Pulsar** | 2.7.x | 2.8.x | 2.9.x | 3.0.x | 4.0.x | 4.1.x |
| **JDBC** | 1.14.x | 1.15.x | 1.16.x | 3.1.x | 3.1.x | 3.2.x |
| **Iceberg** | 0.13.x | 0.14.x | 1.0.x | 1.3.x | 1.4.x | 1.5.x+ |
| **Hudi** | 0.10.x | 0.11.x | 0.12.x | 0.13.x | 0.14.x | 0.15.x+ |
| **Paimon** | N/A | N/A | 0.4.x | 0.6.x | 0.8.x | 0.9.x+ |
| **Flink CDC** | 2.2.x | 2.3.x | 2.4.x | 3.0.x | 3.0.x | 3.1.x+ |

**External System Version Compatibility**:

| Connector | Min Version | Recommended Version | Max Tested Version |
|-----------|-------------|---------------------|--------------------|
| **Kafka** | 0.11 | 2.8+ / 3.5+ | 3.7 |
| **Pulsar** | 2.8 | 2.11+ / 3.0+ | 3.3 |
| **MySQL** | 5.6 | 8.0+ | 8.4 |
| **PostgreSQL** | 9.6 | 14+ | 16 |
| **Elasticsearch** | 6.8 | 7.17+ / 8.11+ | 8.14 |
| **MongoDB** | 3.6 | 5.0+ / 6.0+ | 7.0 |
| **Redis** | 3.0 | 6.2+ / 7.0+ | 7.2 |
| **Iceberg** | 0.13 | 1.4+ | 1.6 |

---

## 4. Argumentation

### 4.1 Connector Selection Decision Framework

**Decision Dimension Analysis**:

```
Connector selection requires comprehensive consideration of the following dimensions:

┌─────────────────────────────────────────────────────────────┐
│ 1. Functional Requirements                                   │
│    - Which capabilities are needed: Source/Sink/Lookup/CDC? │
│    - Is Exactly-Once semantics required?                    │
│    - Latency requirements (millisecond/second/minute level)?│
├─────────────────────────────────────────────────────────────┤
│ 2. Performance Requirements                                  │
│    - Throughput requirements (10K/100K/1M+ records/s)?      │
│    - Is horizontal scaling needed?                          │
│    - Data skew tolerance?                                   │
├─────────────────────────────────────────────────────────────┤
│ 3. Operational Requirements                                  │
│    - Connector maturity and community activity              │
│    - Version upgrade compatibility                          │
│    - Monitoring metrics richness                            │
├─────────────────────────────────────────────────────────────┤
│ 4. Cost Constraints                                          │
│    - External system licensing costs                        │
│    - Infrastructure costs                                   │
│    - Operations manpower costs                              │
└─────────────────────────────────────────────────────────────┘
```

**Message Queue Selection Comparison**:

| Dimension | Kafka | Pulsar | RabbitMQ | Kinesis | Pub/Sub |
|-----------|-------|--------|----------|---------|---------|
| **Throughput** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Latency** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Scalability** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Cost** | Low | Medium | Low | High (AWS) | Medium (GCP) |
| **Ecosystem** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Multi-tenant** | ❌ | ✅ | ❌ | ✅ | ✅ |
| **Geo-replication** | ⚠️ | ✅ | ❌ | ✅ | ✅ |

---

### 4.2 Performance Trade-off Analysis

**Throughput vs Latency Trade-off**:

```
The core of Flink connector performance tuning is balancing throughput and latency:

High-throughput config:
┌─────────────────────────────────────────────────────────────┐
│  - Increase batch.size (Kafka: 32768, JDBC: 5000)          │
│  - Increase buffer.memory (Kafka: 64MB+)                   │
│  - Increase Checkpoint interval (5-10 min)                 │
│  - Enable compression (lz4/snappy)                         │
│  - Result: High throughput, higher latency (second-level)  │
└─────────────────────────────────────────────────────────────┘

Low-latency config:
┌─────────────────────────────────────────────────────────────┐
│  - Decrease batch.size (Kafka: 16384)                      │
│  - Decrease linger.ms (Kafka: 0-5ms)                       │
│  - Decrease Checkpoint interval (1-5s)                     │
│  - Disable compression or lower compression level          │
│  - Result: Low latency (ms-level), lower throughput        │
└─────────────────────────────────────────────────────────────┘
```

**File Format Performance Comparison**:

| Format | Compression Ratio | Read Speed | Write Speed | Columnar | Schema Evolution |
|--------|-------------------|------------|-------------|----------|------------------|
| **Parquet** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ✅ |
| **ORC** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ⚠️ |
| **Avro** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ | ✅ |
| **JSON** | ⭐⭐ | ⭐⭐ | ⭐⭐ | ❌ | ⚠️ |
| **CSV** | ⭐ | ⭐ | ⭐⭐ | ❌ | ❌ |

---

### 4.3 Failure Scenarios & Recovery Strategies

**Common Failure Scenarios**:

| Failure Type | Impact | Recovery Strategy | Prevention |
|--------------|--------|-------------------|------------|
| **Network partition** | Connection interrupted | Auto-reconnect + exponential backoff | Multi-AZ deployment |
| **External system overload** | Write failure | Backpressure + retry queue | Rate limiting + scaling |
| **Checkpoint failure** | State inconsistency | Recover from last successful point | Tune Checkpoint parameters |
| **Schema change** | Serialization failure | Schema Registry + compatibility check | Validate schema in advance |
| **Data skew** | Some subtasks backlogged | Repartition + load balancing | Choose partition key wisely |

**Source Failure Recovery**:

```
Scenario: Kafka Source consumption lag too high

Diagnosis steps:
1. Check consumption lag metric: records-lag-max
2. Check Flink backpressure metric: backPressuredTimeMsPerSecond
3. Check Kafka partition distribution: Is there data skew?

Resolution strategies:
┌─────────────────────────────────────────────────────────────┐
│ If partitions < parallelism:                                 │
│   - Increase Kafka partition count                           │
│   - Adjust Flink parallelism to match partition count        │
│                                                             │
│ If data skew exists:                                         │
│   - Check key distribution, consider salting                 │
│   - Adjust partition strategy                                │
│                                                             │
│ If processing logic is complex:                              │
│   - Optimize processing operators                            │
│   - Increase parallelism                                     │
└─────────────────────────────────────────────────────────────┘
```

**Sink Failure Recovery**:

```
Scenario: JDBC Sink connection timeout

Diagnosis steps:
1. Check database connection pool status
2. Check network latency and stability
3. Check database load

Resolution strategies:
┌─────────────────────────────────────────────────────────────┐
│ Connection timeout:                                          │
│   - Increase connection.timeout                              │
│   - Configure connection pool max connections                │
│                                                             │
│ Write timeout:                                               │
│   - Decrease batch.size                                      │
│   - Increase write timeout                                   │
│                                                             │
│ Primary key conflict:                                        │
│   - Enable UPSERT mode                                       │
│   - Check data uniqueness                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Proof / Engineering Argument

### Thm-F-04-100 (Connector Ecosystem Completeness Theorem)

**Theorem**: The Flink connector ecosystem covers mainstream data storage systems and can satisfy enterprise-level data integration requirements.

**Proof**:

**Premises**:

- P1: Enterprise data storage can be divided into four categories: message queues, file systems, databases, and data lakes
- P2: Each category has industry mainstream implementations
- P3: Flink provides official or community connectors for each mainstream implementation

**Categorical Argumentation**:

```
Message Queue Category (Streaming Data Ingestion):
┌─────────────────────────────────────────────────────────────┐
│ Mainstream systems: Kafka, Pulsar, RabbitMQ, Kinesis,      │
│   Pub/Sub                                                  │
│ Flink support: ✅ Official connectors cover all mainstream │
│   systems                                                  │
│ Semantic guarantee: ✅ Source/Sink both support            │
│   EXACTLY_ONCE                                             │
└─────────────────────────────────────────────────────────────┘

File System Category (Batch Data Storage):
┌─────────────────────────────────────────────────────────────┐
│ Mainstream systems: HDFS, S3, GCS, Azure Blob, OSS         │
│ Flink support: ✅ Unified FileSystem abstraction, supports │
│   all mainstream object storage                            │
│ Format support: ✅ Parquet/ORC/Avro/JSON/CSV              │
└─────────────────────────────────────────────────────────────┘

Database Category (Structured Data Storage):
┌─────────────────────────────────────────────────────────────┐
│ Relational: MySQL, PostgreSQL, Oracle, SQL Server, DB2     │
│ NoSQL: Cassandra, MongoDB, HBase, Elasticsearch, Redis     │
│ Flink support: ✅ JDBC generic + dedicated connectors      │
│ Query capability: ✅ Source/Sink/Lookup support            │
└─────────────────────────────────────────────────────────────┘

Data Lake Category (Lakehouse Storage):
┌─────────────────────────────────────────────────────────────┐
│ Mainstream formats: Iceberg, Hudi, Paimon, Delta Lake,     │
│   Fluss                                                    │
│ Flink support: ✅ Deep integration with all mainstream     │
│   formats                                                  │
│ Unified batch/stream: ✅ Supports streaming write and      │
│   batch query                                              │
└─────────────────────────────────────────────────────────────┘

In summary, the Flink connector ecosystem has complete coverage across all four storage categories. Completeness proved. ∎
```

---

### Thm-F-04-101 (Multi-Connector Composition Consistency Theorem)

**Theorem**: In Flink, when multiple connectors are used in combination, end-to-end consistency can be guaranteed through the Checkpoint mechanism.

**Proof**:

**System Model**:

```
Let the data flow be: Source → [Operators] → Sink

Definitions:
- S: Source connector, producing record sequence ⟨e₁, e₂, ..., eₙ⟩
- O: Operator set, processing records and maintaining state
- K: Sink connector, outputting records to external system
- C: Checkpoint coordinator, periodically triggering consistent snapshots
```

**Two-Phase Commit Flow**:

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: Checkpoint Trigger                                 │
│ ─────────────────────────────────────────────────────────  │
│ 1. CheckpointCoordinator sends Checkpoint Barrier to all   │
│    operators                                               │
│ 2. Source: Save current read position to StateBackend      │
│ 3. Operators: Save computation state to StateBackend       │
│ 4. Sink: Execute preCommit(), prepare transaction          │
│                                                             │
│ Invariant I1: Before all preCommits complete, Sink output  │
│   is not visible                                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Phase 2: Checkpoint Complete                                │
│ ─────────────────────────────────────────────────────────  │
│ Trigger condition: All operators complete snapshotState    │
│                                                             │
│ Actions:                                                    │
│ 1. CheckpointCoordinator confirms global snapshot success  │
│ 2. Source: Optionally commit offset to external system     │
│ 3. Sink: Execute commit(), transaction committed, output   │
│    visible                                                 │
│                                                             │
│ Invariant I2: After Checkpoint success, Sink output is     │
│   permanently visible                                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Failure Recovery Scenarios                                  │
│ ─────────────────────────────────────────────────────────  │
│ Scenario 1: Checkpoint fails during execution              │
│   - Trigger notifyCheckpointAborted()                      │
│   - Sink executes abort(), rollback transaction            │
│   - Recover from last successful Checkpoint                │
│   - Result: No data loss, no duplicates                    │
│                                                             │
│ Scenario 2: Sink fails before commit after Checkpoint      │
│   success                                                  │
│   - New Sink instance recovers from Checkpoint             │
│   - Re-execute commit() (idempotent)                       │
│   - Result: No data duplication                            │
│                                                             │
│ Scenario 3: Source failure                                 │
│   - Recover read position from StateBackend                │
│   - Re-consume unacknowledged data                         │
│   - Result: At-Least-Once, with idempotent Sink achieves   │
│     Exactly-Once                                           │
└─────────────────────────────────────────────────────────────┘
```

**Consistency Guarantee**:

| Condition | Guarantee | Dependency |
|-----------|-----------|------------|
| Source replayable | No loss | Offset/snapshot persistence |
| Checkpoint success | State consistent | Barrier alignment |
| Sink transaction commit | Output not duplicated | 2PC/idempotent mechanism |
| All three combined | Exactly-Once | System coordination |

In summary, multi-connector composition consistency is proved. ∎

---

## 6. Examples

### 6.1 Message Queue Connectors

#### 6.1.1 Kafka Connector

**Maven Dependency**:

```xml
<!-- Kafka Connector -->
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-kafka</artifactId>
    <version>3.2.0-1.19</version>
</dependency>
```

**Source Configuration**:

```java

// [Pseudo-code snippet - not directly runnable] Core logic only
import org.apache.flink.streaming.api.datastream.DataStream;

// Kafka Source (Flink 1.14+ new API)
KafkaSource<String> source = KafkaSource.<String>builder()
    .setBootstrapServers("kafka-1:9092,kafka-2:9092")
    .setTopics("input-topic")
    .setGroupId("flink-consumer-group")
    .setStartingOffsets(OffsetsInitializer.earliest())
    .setValueOnlyDeserializer(new SimpleStringSchema())
    .setProperty("partition.discovery.interval.ms", "10000")
    .setProperty("isolation.level", "read_committed")
    .build();

DataStream<String> stream = env.fromSource(
    source,
    WatermarkStrategy.forBoundedOutOfOrderness(Duration.ofSeconds(5)),
    "Kafka Source"
);
```

**Sink Configuration**:

```java
// [Pseudo-code snippet - not directly runnable] Core logic only
// Kafka Sink with Exactly-Once
KafkaSink<String> sink = KafkaSink.<String>builder()
    .setBootstrapServers("kafka-1:9092,kafka-2:9092")
    .setRecordSerializer(KafkaRecordSerializationSchema.builder()
        .setTopic("output-topic")
        .setValueSerializationSchema(new SimpleStringSchema())
        .build())
    .setDeliveryGuarantee(DeliveryGuarantee.EXACTLY_ONCE)
    .setProperty("transaction.timeout.ms", "900000")
    .setProperty("enable.idempotence", "true")
    .setTransactionalIdPrefix("flink-job-")
    .build();

stream.sinkTo(sink);
```

**Key Configuration Parameters**:

| Parameter | Source/Sink | Default | Description |
|-----------|-------------|---------|-------------|
| `bootstrap.servers` | Both | Required | Kafka cluster address |
| `group.id` | Source | Required | Consumer group ID |
| `auto.offset.reset` | Source | latest | Starting offset strategy |
| `isolation.level` | Source | read_uncommitted | Isolation level |
| `enable.idempotence` | Sink | true | Idempotent producer |
| `transaction.timeout.ms` | Sink | 60000 | Transaction timeout |
| `delivery.guarantee` | Sink | AT_LEAST_ONCE | Delivery guarantee |

---

#### 6.1.2 Apache Pulsar Connector

**Maven Dependency**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-pulsar</artifactId>
    <version>4.1.0-1.19</version>
</dependency>
```

**Source Configuration**:

```java

// [Pseudo-code snippet - not directly runnable] Core logic only
import org.apache.flink.streaming.api.datastream.DataStream;

// Pulsar Source
PulsarSource<String> source = PulsarSource.builder()
    .setServiceUrl("pulsar://pulsar-broker:6650")
    .setAdminUrl("http://pulsar-admin:8080")
    .setTopics("persistent://public/default/input-topic")
    .setDeserializationSchema(new SimpleStringSchema())
    .setSubscriptionName("flink-subscription")
    .setSubscriptionType(SubscriptionType.Exclusive)
    .setStartCursor(StartCursor.earliest())
    .setBoundedStopCursor(StopCursor.never())
    .build();

DataStream<String> stream = env.fromSource(
    source,
    WatermarkStrategy.noWatermarks(),
    "Pulsar Source"
);
```

**Sink Configuration**:

```java
// [Pseudo-code snippet - not directly runnable] Core logic only
// Pulsar Sink
PulsarSink<String> sink = PulsarSink.builder()
    .setServiceUrl("pulsar://pulsar-broker:6650")
    .setAdminUrl("http://pulsar-admin:8080")
    .setTopics("persistent://public/default/output-topic")
    .setSerializationSchema(new SimpleStringSchema())
    .setDeliveryGuarantee(DeliveryGuarantee.EXACTLY_ONCE)
    .setConfig(PulsarOptions.PULSAR_TRANSACTION_TIMEOUT_MILLIS, 600000L)
    .build();

stream.sinkTo(sink);
```

---

#### 6.1.3 RabbitMQ Connector

**Maven Dependency**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-rabbitmq</artifactId>
    <version>3.0.1-1.17</version>
</dependency>
```

**Source/Sink Configuration**:

```java

// [Pseudo-code snippet - not directly runnable] Core logic only
import org.apache.flink.streaming.api.datastream.DataStream;

// RabbitMQ Connection Config
RMQConnectionConfig connectionConfig = new RMQConnectionConfig.Builder()
    .setHost("rabbitmq-host")
    .setPort(5672)
    .setUserName("user")
    .setPassword("password")
    .setVirtualHost("/")
    .build();

// RabbitMQ Source
DataStream<String> stream = env.addSource(
    new RMQSource<>(
        connectionConfig,
        "input-queue",
        true,  // useCorrelationId
        new SimpleStringSchema()
    )
).setParallelism(1);

// RabbitMQ Sink
RMQSink<String> sink = new RMQSink<>(
    connectionConfig,
    "output-queue",
    new SimpleStringSchema()
);

stream.addSink(sink);
```

---

#### 6.1.4 Amazon Kinesis Connector

**Maven Dependency**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-aws-kinesis-streams</artifactId>
    <version>4.3.0-1.19</version>
</dependency>
```

**Source Configuration**:

```java

// [Pseudo-code snippet - not directly runnable] Core logic only
import org.apache.flink.streaming.api.datastream.DataStream;

// Kinesis Source
Properties consumerConfig = new Properties();
consumerConfig.put(AWSConfigConstants.AWS_REGION, "us-east-1");
consumerConfig.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "access-key");
consumerConfig.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "secret-key");

KinesisSource<String> source = KinesisSource.<String>builder()
    .setKinesisStreamName("input-stream")
    .setConsumerConfig(consumerConfig)
    .setDeserializationSchema(new SimpleStringSchema())
    .setInitialPosition(StreamPosition.LATEST)
    .build();

DataStream<String> stream = env.fromSource(
    source,
    WatermarkStrategy.forBoundedOutOfOrderness(Duration.ofSeconds(5)),
    "Kinesis Source"
);
```

**Sink Configuration**:

```java
// [Pseudo-code snippet - not directly runnable] Core logic only
// Kinesis Sink
Properties producerConfig = new Properties();
producerConfig.put(AWSConfigConstants.AWS_REGION, "us-east-1");

KinesisStreamsSink<String> sink = KinesisStreamsSink.<String>builder()
    .setKinesisClientProperties(producerConfig)
    .setSerializationSchema(new SimpleStringSchema())
    .setPartitionKeyGenerator(element -> String.valueOf(element.hashCode()))
    .setStreamName("output-stream")
    .setFailOnError(false)
    .setMaxBatchSize(500)
    .setMaxInFlightRequests(50)
    .setMaxBufferedRequests(10000)
    .setMaxBatchSizeInBytes(5 * 1024 * 1024)
    .setMaxTimeInBufferMS(5000)
    .build();

stream.sinkTo(sink);
```

---

#### 6.1.5 Google Cloud Pub/Sub Connector

**Maven Dependency**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-gcp-pubsub</artifactId>
    <version>3.0.1-1.17</version>
</dependency>
```

**Source/Sink Configuration**:

```java

// [Pseudo-code snippet - not directly runnable] Core logic only
import org.apache.flink.streaming.api.datastream.DataStream;

// Pub/Sub Source
DeserializationSchema<String> deserializer = new SimpleStringSchema();

PubSubSource<String> source = PubSubSource.newBuilder()
    .withDeserializationSchema(deserializer)
    .withProjectName("my-project")
    .withSubscriptionName("my-subscription")
    .withCredentials(GoogleCredentials.fromStream(new FileInputStream("key.json")))
    .build();

DataStream<String> stream = env.addSource(source);

// Pub/Sub Sink
PubSubSink<String> sink = PubSubSink.newBuilder()
    .withSerializationSchema(new SimpleStringSchema())
    .withProjectName("my-project")
    .withTopicName("my-topic")
    .withCredentials(GoogleCredentials.fromStream(new FileInputStream("key.json")))
    .build();

stream.addSink(sink);
```

---

#### 6.1.6 MQTT Connector

**Maven Dependency**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-mqtt</artifactId>
    <version>3.0.0-1.17</version>
</dependency>
```

**Source/Sink Configuration**:

```java

// [Pseudo-code snippet - not directly runnable] Core logic only
import org.apache.flink.streaming.api.datastream.DataStream;

// MQTT Source
MQTTSource<String> source = MQTTSource.<String>builder()
    .setBrokerUrl("tcp://mqtt-broker:1883")
    .setTopics(Arrays.asList("sensor/temperature", "sensor/humidity"))
    .setClientIdPrefix("flink-mqtt-client")
    .setDeserializationSchema(new SimpleStringSchema())
    .setQoS(1)
    .setAutomaticReconnect(true)
    .setCleanSession(false)
    .build();

DataStream<String> stream = env.fromSource(
    source,
    WatermarkStrategy.noWatermarks(),
    "MQTT Source"
);

// MQTT Sink
MQTTSink<String> sink = MQTTSink.<String>builder()
    .setBrokerUrl("tcp://mqtt-broker:1883")
    .setTopic("output/topic")
    .setClientId("flink-mqtt-sink")
    .setSerializationSchema(new SimpleStringSchema())
    .setQoS(1)
    .setRetained(false)
    .build();

stream.sinkTo(sink);
```

---

### 6.2 File System Connectors

#### 6.2.1 General File System Configuration

**Supported File Systems**:

| File System | Scheme | Dependency | Description |
|-------------|--------|------------|-------------|
| Local file | `file://` | Built-in | Local testing |
| HDFS | `hdfs://` | hadoop-client | Distributed file system |
| S3 | `s3://` | flink-s3-fs | AWS object storage |
| GCS | `gs://` | flink-gs-fs | Google object storage |
| Azure | `wasb://` | flink-azure-fs | Azure Blob |
| OSS | `oss://` | flink-oss-fs | Alibaba Cloud object storage |

**File System Configuration Example**:

```java
// [Pseudo-code snippet - not directly runnable] Core logic only
// Create FileSystem instance
FileSystem fs = FileSystem.get(new URI("s3://my-bucket/data"));

// S3 configuration
Configuration conf = new Configuration();
conf.setString("s3.access-key", "AKIA...");
conf.setString("s3.secret-key", "...");
conf.setString("s3.endpoint", "s3.amazonaws.com");

// Register file system
FileSystem.initialize(conf, null);
```

---

#### 6.2.2 File Source (Bulk Format)

**Parquet File Read**:

```java

// [Pseudo-code snippet - not directly runnable] Core logic only
import org.apache.flink.streaming.api.datastream.DataStream;

// Parquet Source
FileSource<Row> source = FileSource.forRecordStreamFormat(
    new ParquetRecordFormat(),
    new Path("s3://bucket/data/")
).build();

DataStream<Row> stream = env.fromSource(
    source,
    WatermarkStrategy.noWatermarks(),
    "Parquet File Source"
);
```

**Avro File Read**:

```java
// [Pseudo-code snippet - not directly runnable] Core logic only
// Avro Source with Schema
Schema schema = new Schema.Parser().parse(
    new File("user.avsc")
);

FileSource<GenericRecord> source = FileSource.forRecordStreamFormat(
    new AvroRecordFormat<>(schema),
    new Path("hdfs://namenode/data/")
).build();
```

---

#### 6.2.3 File Sink (Streaming)

**Parquet File Write**:

```java
// [Pseudo-code snippet - not directly runnable] Core logic only
// Streaming File Sink with Parquet
final StreamingFileSink<Row> sink = StreamingFileSink
    .forBulkFormat(
        new Path("s3://bucket/output/"),
        ParquetRowFormat.forRowType(
            rowType,
            HadoopCompressionCodecName.SNAPPY
        )
    )
    .withBucketAssigner(new DateTimeBucketAssigner<>("yyyy-MM-dd--HH"))
    .withRollingPolicy(
        OnCheckpointRollingPolicy.build()
    )
    .build();

stream.addSink(sink);
```

**Flink 1.14+ FileSink API**:

```java
// [Pseudo-code snippet - not directly runnable] Core logic only
// New FileSink API (Recommended)
FileSink<Row> sink = FileSink.forBulkFormat(
    new Path("s3://bucket/output/"),
    ParquetAvroWriters.forSpecificRecord(User.class)
)
.withBucketAssigner(new DateTimeBucketAssigner<>())
.withRollingPolicy(
    DefaultRollingPolicy.builder()
        .withRolloverInterval(Duration.ofMinutes(15))
        .withInactivityInterval(Duration.ofMinutes(5))
        .withMaxPartSize(MemorySize.ofMebiBytes(128))
        .build()
)
.withBucketCheckInterval(Duration.ofSeconds(10))
.build();

stream.sinkTo(sink);
```

---

### 6.3 Database Connectors

#### 6.3.1 JDBC Connector

**Maven Dependency**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-jdbc</artifactId>
    <version>3.2.0-1.19</version>
</dependency>
<!-- Database driver -->
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.33</version>
</dependency>
```

**JDBC Source**:

```java

// [Pseudo-code snippet - not directly runnable] Core logic only
import org.apache.flink.streaming.api.datastream.DataStream;

// JDBC Source (Bounded)
JdbcSource<Row> source = JdbcSource.<Row>builder()
    .setUrl("jdbc:mysql://localhost:3306/mydb")
    .setDriverName("com.mysql.cj.jdbc.Driver")
    .setUsername("user")
    .setPassword("password")
    .setQuery("SELECT id, name, amount FROM orders WHERE create_time > ?")
    .setRowTypeInfo(rowTypeInfo)
    .setFetchSize(1000)
    .build();

DataStream<Row> stream = env.fromSource(
    source,
    WatermarkStrategy.noWatermarks(),
    "JDBC Source"
);
```

**JDBC Sink**:

```java
// [Pseudo-code snippet - not directly runnable] Core logic only
// JDBC Sink with Exactly-Once (XA)
JdbcExactlyOnceSink<Row> sink = JdbcExactlyOnceSink.sink(
    "INSERT INTO orders (id, name, amount) VALUES (?, ?, ?) " +
    "ON DUPLICATE KEY UPDATE amount = VALUES(amount)",
    (ps, row) -> {
        ps.setLong(1, row.getField(0));
        ps.setString(2, row.getField(1));
        ps.setBigDecimal(3, row.getField(2));
    },
    JdbcExecutionOptions.builder()
        .withBatchSize(1000)
        .withBatchIntervalMs(200)
        .withMaxRetries(3)
        .build(),
    JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
        .withUrl("jdbc:mysql://localhost:3306/mydb")
        .withDriverName("com.mysql.cj.jdbc.Driver")
        .withUsername("user")
        .withPassword("password")
        .build()
);

stream.addSink(sink);
```

**JDBC Lookup Join**:

```sql
-- Flink SQL Lookup Join
CREATE TABLE orders (
    order_id STRING,
    user_id STRING,
    amount DECIMAL(10, 2),
    proctime AS PROCTIME()
) WITH (
    'connector' = 'kafka',
    ...
);

CREATE TABLE users (
    user_id STRING,
    user_name STRING,
    age INT,
    PRIMARY KEY (user_id) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:mysql://localhost:3306/mydb',
    'table-name' = 'users',
    'username' = 'user',
    'password' = 'password',
    'lookup.cache.max-rows' = '5000',
    'lookup.cache.ttl' = '10 min'
);

-- Lookup Join
SELECT o.order_id, o.amount, u.user_name
FROM orders AS o
LEFT JOIN users FOR SYSTEM_TIME AS OF o.proctime AS u
ON o.user_id = u.user_id;
```

---

#### 6.3.2 Apache Cassandra Connector

**Maven Dependency**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-cassandra_2.12</artifactId>
    <version>3.1.0-1.17</version>
</dependency>
```

**Cassandra Sink**:

```java
// [Pseudo-code snippet - not directly runnable] Core logic only
// Cassandra Sink
ClusterBuilder clusterBuilder = new ClusterBuilder() {
    @Override
    protected Cluster buildCluster(Cluster.Builder builder) {
        return builder.addContactPoint("cassandra-host")
            .withPort(9042)
            .withCredentials("username", "password")
            .build();
    }
};

CassandraSink.addSink(stream)
    .setQuery("INSERT INTO mykeyspace.orders (id, name, amount) VALUES (?, ?, ?)")
    .setClusterBuilder(clusterBuilder)
    .setFailureHandler(new CassandraFailureHandler() {
        @Override
        public void onFailure(Throwable throwable) {
            // Handle write failure
        }
    })
    .build();
```

---

#### 6.3.3 Apache HBase Connector

**Maven Dependency**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-hbase-2.2</artifactId>
    <version>3.0.0-1.17</version>
</dependency>
```

**HBase Source/Sink**:

```java
// [Pseudo-code snippet - not directly runnable] Core logic only
// HBase Source
HBaseSourceFunction<Row> source = new HBaseSourceFunction<>(
    "mytable",
    new HBaseConfiguration(),
    rowTypeInfo,
    row -> {
        // Transform HBase Result to Row
    }
);

// HBase Sink
HBaseSinkFunction<Row> sink = new HBaseSinkFunction<>(
    "mytable",
    new HBaseConfiguration(),
    row -> {
        // Transform Row to Put
        return new Put(Bytes.toBytes(row.getField(0).toString()))
            .addColumn(Bytes.toBytes("cf"), Bytes.toBytes("col"),
                      Bytes.toBytes(row.getField(1).toString()));
    }
);

stream.addSink(sink);
```

---

#### 6.3.4 Elasticsearch Connector

**Maven Dependency**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-elasticsearch8</artifactId>
    <version>3.0.1-1.17</version>
</dependency>
```

**Elasticsearch Sink**:

```java
// [Pseudo-code snippet - not directly runnable] Core logic only
// Elasticsearch Sink
List<HttpHost> httpHosts = Arrays.asList(
    new HttpHost("es-host-1", 9200),
    new HttpHost("es-host-2", 9200)
);

ElasticsearchSink.Builder<String> builder = new ElasticsearchSink.Builder<>(
    httpHosts,
    new ElasticsearchSinkFunction<String>() {
        @Override
        public void process(String element, RuntimeContext ctx,
                           RequestIndexer indexer) {
            indexer.add(new IndexRequest("my-index")
                .id(element.getId())
                .source(element, XContentType.JSON));
        }
    }
);

builder.setBulkFlushMaxActions(1000);
builder.setBulkFlushInterval(5000);
builder.setFailureHandler(new RetryRejectedExecutionFailureHandler());

stream.addSink(builder.build());
```

---

#### 6.3.5 MongoDB Connector

**Maven Dependency**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-mongodb</artifactId>
    <version>1.2.0</version>
</dependency>
```

**MongoDB Source/Sink**:

```java

// [Pseudo-code snippet - not directly runnable] Core logic only
import org.apache.flink.streaming.api.datastream.DataStream;

// MongoDB Source
MongoSource<String> source = MongoSource.<String>builder()
    .setUri("mongodb://user:password@mongodb:27017")
    .setDatabase("mydb")
    .setCollection("events")
    .setDeserializationSchema(new JsonDeserializationSchema())
    .setFetchSize(1000)
    .build();

DataStream<String> stream = env.fromSource(
    source,
    WatermarkStrategy.noWatermarks(),
    "MongoDB Source"
);

// MongoDB Sink
MongoSink<Document> sink = MongoSink.<Document>builder()
    .setUri("mongodb://user:password@mongodb:27017")
    .setDatabase("mydb")
    .setCollection("output")
    .setSerializationSchema(
        (doc, ctx) -> new InsertOneModel<>(doc)
    )
    .build();

stream.map(Json::parse).map(Document::parse).sinkTo(sink);
```

---

#### 6.3.6 Redis Connector

**Maven Dependency** (Community connector):

```xml
<dependency>
    <groupId>io.github.leefige</groupId>
    <artifactId>flink-connector-redis</artifactId>
    <version>1.3.0</version>
</dependency>
```

**Redis Sink**:

```java
// [Pseudo-code snippet - not directly runnable] Core logic only
// Redis Sink Configuration
FlinkJedisPoolConfig conf = new FlinkJedisPoolConfig.Builder()
    .setHost("redis-host")
    .setPort(6379)
    .setPassword("password")
    .setDatabase(0)
    .setMaxTotal(100)
    .setMaxIdle(50)
    .setMinIdle(10)
    .build();

// Redis Sink
RedisSink<Tuple2<String, String>> redisSink = new RedisSink<>(
    conf,
    new RedisMapper<Tuple2<String, String>>() {
        @Override
        public RedisCommandDescription getCommandDescription() {
            return new RedisCommandDescription(RedisCommand.HSET, "myhash");
        }

        @Override
        public String getKeyFromData(Tuple2<String, String> data) {
            return data.f0;
        }

        @Override
        public String getValueFromData(Tuple2<String, String> data) {
            return data.f1;
        }
    }
);

stream.addSink(redisSink);
```

---

#### 6.3.7 InfluxDB Connector

**Maven Dependency** (Community connector):

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-influxdb</artifactId>
    <version>1.0.0</version>
</dependency>
```

**InfluxDB Sink**:

```java
// [Pseudo-code snippet - not directly runnable] Core logic only
// InfluxDB Sink
InfluxDBSink<String> sink = InfluxDBSink.builder()
    .setInfluxDBUrl("http://influxdb:8086")
    .setInfluxDBUsername("user")
    .setInfluxDBPassword("password")
    .setDatabase("metrics")
    .setMeasurement("events")
    .setSerializationSchema((element, ctx) -> {
        return Point.measurement("events")
            .time(System.currentTimeMillis(), TimeUnit.MILLISECONDS)
            .tag("type", "click")
            .addField("value", element)
            .build();
    })
    .setWriteBufferSize(1000)
    .setFlushInterval(1000)
    .build();

stream.sinkTo(sink);
```

---

### 6.4 Lakehouse Connectors

#### 6.4.1 Apache Iceberg Connector

**Maven Dependency**:

```xml
<dependency>
    <groupId>org.apache.iceberg</groupId>
    <artifactId>iceberg-flink-runtime-1.19</artifactId>
    <version>1.5.0</version>
</dependency>
```

**Iceberg Catalog Configuration**:

```java
// [Pseudo-code snippet - not directly runnable] Core logic only
// Hive Catalog
CatalogLoader catalogLoader = CatalogLoader.hive(
    "hive_catalog",
    new Configuration(),
    ImmutableMap.of(
        "uri", "thrift://hive-metastore:9083",
        "warehouse", "s3://bucket/warehouse",
        "io-impl", "org.apache.iceberg.aws.s3.S3FileIO"
    )
);

Catalog catalog = catalogLoader.loadCatalog();
```

**Iceberg SQL Integration**:

```sql
-- Create Iceberg Catalog
CREATE CATALOG iceberg_catalog WITH (
    'type' = 'iceberg',
    'catalog-type' = 'hive',
    'uri' = 'thrift://hive-metastore:9083',
    'warehouse' = 's3://bucket/warehouse',
    'io-impl' = 'org.apache.iceberg.aws.s3.S3FileIO'
);

USE CATALOG iceberg_catalog;

-- Create Iceberg table
CREATE TABLE user_events (
    user_id STRING,
    event_type STRING,
    event_time TIMESTAMP(3),
    properties MAP<STRING, STRING>
) PARTITIONED BY (
    days(event_time)
) WITH (
    'write.format.default' = 'parquet',
    'write.parquet.compression-codec' = 'zstd',
    'write.target-file-size-bytes' = '134217728',
    'read.streaming.enabled' = 'true',
    'read.streaming.start-mode' = 'earliest'
);

-- Streaming write
INSERT INTO user_events
SELECT user_id, event_type, event_time, properties
FROM kafka_source;
```

**Iceberg Source (Streaming Read)**:

```java

// [Pseudo-code snippet - not directly runnable] Core logic only
import org.apache.flink.streaming.api.datastream.DataStream;

// Iceberg Streaming Source
Table table = catalog.loadTable(TableIdentifier.of("db", "user_events"));

IcebergSource<Row> source = IcebergSource.forRowData()
    .tableLoader(() -> table)
    .streaming(true)
    .monitorInterval(Duration.ofSeconds(10))
    .startSnapshotId(table.currentSnapshot().snapshotId())
    .build();

DataStream<Row> stream = env.fromSource(
    source,
    WatermarkStrategy.forBoundedOutOfOrderness(Duration.ofSeconds(5)),
    "Iceberg Source"
);
```

---

#### 6.4.2 Apache Hudi Connector

**Maven Dependency**:

```xml
<dependency>
    <groupId>org.apache.hudi</groupId>
    <artifactId>hudi-flink1.19-bundle</artifactId>
    <version>0.14.0</version>
</dependency>
```

**Hudi SQL Integration**:

```sql
-- Create Hudi table
CREATE TABLE hudi_users (
    id STRING PRIMARY KEY NOT ENFORCED,
    name STRING,
    age INT,
    ts TIMESTAMP(3)
) WITH (
    'connector' = 'hudi',
    'path' = 's3://bucket/hudi/users',
    'table.type' = 'MERGE_ON_READ',
    'write.operation' = 'upsert',
    'write.precombine.field' = 'ts',
    'write.tasks' = '4',
    'compaction.tasks' = '4',
    'compaction.schedule.enabled' = 'true',
    'compaction.delta_commits' = '5'
);

-- UPSERT write
INSERT INTO hudi_users
SELECT id, name, age, ts FROM kafka_users;
```

---

#### 6.4.3 Apache Paimon Connector

**Maven Dependency**:

```xml
<dependency>
    <groupId>org.apache.paimon</groupId>
    <artifactId>paimon-flink-1.19</artifactId>
    <version>0.8.0</version>
</dependency>
```

**Paimon SQL Integration**:

```sql
-- Create Paimon Catalog
CREATE CATALOG paimon_catalog WITH (
    'type' = 'paimon',
    'warehouse' = 's3://bucket/paimon',
    's3.endpoint' = 's3.amazonaws.com'
);

USE CATALOG paimon_catalog;

-- Create Paimon table
CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY NOT ENFORCED,
    user_id STRING,
    product_id STRING,
    amount DECIMAL(10, 2),
    order_time TIMESTAMP(3)
) WITH (
    'bucket' = '8',
    'bucket-key' = 'order_id',
    'changelog-producer' = 'input',
    'merge-engine' = 'deduplicate',
    'sequence.field' = 'order_time'
);

-- Streaming write
INSERT INTO orders
SELECT * FROM kafka_orders;
```

---

#### 6.4.4 Delta Lake Connector

**Maven Dependency**:

```xml
<dependency>
    <groupId>io.delta</groupId>
    <artifactId>delta-flink</artifactId>
    <version>3.2.0</version>
</dependency>
```

**Delta Lake Sink**:

```java
// [Pseudo-code snippet - not directly runnable] Core logic only
// Delta Lake Sink
DeltaSink<Row> deltaSink = DeltaSink
    .forRowData(
        new Path("s3://bucket/delta-table/"),
        new Configuration(),
        rowType
    )
    .withPartitionColumns("date")
    .build();

stream.sinkTo(deltaSink);
```

---

#### 6.4.5 Apache Fluss Connector

**Maven Dependency**:

```xml
<dependency>
    <groupId>org.apache.fluss</groupId>
    <artifactId>fluss-flink-connector</artifactId>
    <version>0.5.0</version>
</dependency>
```

**Fluss SQL Integration**:

```sql
-- Create Fluss Catalog
CREATE CATALOG fluss_catalog WITH (
    'type' = 'fluss',
    'bootstrap.servers' = 'fluss-server:9123'
);

USE CATALOG fluss_catalog;

-- Create Fluss table (Streaming Lakehouse)
CREATE TABLE realtime_events (
    event_id STRING PRIMARY KEY NOT ENFORCED,
    user_id STRING,
    event_data STRING,
    event_time TIMESTAMP(3),
    WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
) WITH (
    'kafka.retention.time' = '7d',
    'lakehouse.trigger.interval' = '1h'
);
```

---

### 6.5 CDC Connectors

#### 6.5.1 Flink CDC 3.0 Basic Configuration

**Maven Dependency**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-cdc-dist</artifactId>
    <version>3.0.1</version>
</dependency>
```

**MySQL CDC Source**:

```java
// [Pseudo-code snippet - not directly runnable] Core logic only
// MySQL CDC Source
MySqlSource<String> mySqlSource = MySqlSource.<String>builder()
    .hostname("mysql-host")
    .port(3306)
    .databaseList("inventory")
    .tableList("inventory.products", "inventory.orders")
    .username("cdc_user")
    .password("password")
    .deserializer(new JsonDebeziumDeserializationSchema())
    .startupOptions(StartupOptions.initial())
    .build();

env.fromSource(mySqlSource, WatermarkStrategy.noWatermarks(), "MySQL CDC")
    .print();
```

**Flink SQL CDC**:

```sql
-- MySQL CDC Table
CREATE TABLE mysql_products (
    id INT PRIMARY KEY NOT ENFORCED,
    name STRING,
    description STRING,
    weight DECIMAL(10, 3)
) WITH (
    'connector' = 'mysql-cdc',
    'hostname' = 'mysql-host',
    'port' = '3306',
    'username' = 'cdc_user',
    'password' = 'password',
    'database-name' = 'inventory',
    'table-name' = 'products',
    'scan.startup.mode' = 'initial',
    'server-id' = '5400-5404'
);

-- PostgreSQL CDC Table
CREATE TABLE pg_users (
    id INT PRIMARY KEY NOT ENFORCED,
    name STRING,
    email STRING
) WITH (
    'connector' = 'postgres-cdc',
    'hostname' = 'postgres-host',
    'port' = '5432',
    'username' = 'cdc_user',
    'password' = 'password',
    'database-name' = 'mydb',
    'schema-name' = 'public',
    'table-name' = 'users',
    'decoding.plugin.name' = 'pgoutput',
    'slot.name' = 'flink_slot'
);
```

---

#### 6.5.2 CDC Pipeline YAML Configuration

**MySQL → Doris Sync**:

```yaml
# pipeline.yaml pipeline:
  name: mysql-to-doris-pipeline
  parallelism: 4

source:
  type: mysql
  hostname: mysql-host
  port: 3306
  username: ${MYSQL_USER}
  password: ${MYSQL_PASSWORD}
  database-list: inventory,orders
  table-list: inventory\..*,orders\..*

  # Lock-free read config
  scan.incremental.snapshot.enabled: true
  scan.snapshot.fetch.size: 1024
  scan.incremental.snapshot.chunk.size: 8096
  scan.startup.mode: initial

  # Schema change capture
  include.schema.changes: true

sink:
  type: doris
  fenodes: doris-fe:8030
  username: ${DORIS_USER}
  password: ${DORIS_PASSWORD}
  database: ods

  # Write config
  sink.enable.batch-mode: true
  sink.buffer-flush.interval: 10s
  sink.buffer-flush.max-rows: 50000
  sink.max-retries: 3

  # Table creation options
  table.create.properties.replication_num: 3
  table.create.properties.storage_format: MOR

# Data transform (optional)
transform:
  - source-table: inventory\.customers
    projection: id, name, email, region
    filter: region = 'APAC'
    description: "Filter APAC customers"

# Routing rules (optional)
route:
  - source-table: orders\.order_\d+
    sink-table: ods.orders_all
    description: "Merge all order shards"
```

---

#### 6.5.3 CDC to Lakehouse

**MySQL CDC → Iceberg**:

```sql
-- 1. Create CDC Source table
CREATE TABLE mysql_orders_cdc (
    order_id BIGINT,
    user_id STRING,
    amount DECIMAL(10, 2),
    status STRING,
    create_time TIMESTAMP(3),
    PRIMARY KEY (order_id) NOT ENFORCED
) WITH (
    'connector' = 'mysql-cdc',
    'hostname' = 'mysql-host',
    'port' = '3306',
    'username' = 'cdc_user',
    'password' = 'password',
    'database-name' = 'mydb',
    'table-name' = 'orders'
);

-- 2. Create Iceberg Sink table
CREATE TABLE iceberg_orders (
    order_id BIGINT,
    user_id STRING,
    amount DECIMAL(10, 2),
    status STRING,
    create_time TIMESTAMP(3),
    PRIMARY KEY (order_id) NOT ENFORCED
) WITH (
    'connector' = 'iceberg',
    'catalog-type' = 'hive',
    'catalog-database' = 'default',
    'catalog-table' = 'orders',
    'write.upsert.enabled' = 'true',
    'write.parquet.compression-codec' = 'zstd'
);

-- 3. Start CDC sync
INSERT INTO iceberg_orders
SELECT * FROM mysql_orders_cdc;
```

**CDC to Paimon (Recommended)**:

```sql
-- Paimon CDC sync
CREATE TABLE paimon_orders (
    order_id BIGINT PRIMARY KEY NOT ENFORCED,
    user_id STRING,
    amount DECIMAL(10, 2),
    status STRING,
    create_time TIMESTAMP(3)
) WITH (
    'connector' = 'paimon',
    'path' = 's3://bucket/paimon/orders',
    'bucket' = '8',
    'merge-engine' = 'deduplicate',
    'changelog-producer' = 'input',
    'sequence.field' = 'create_time'
);

-- Sync job
INSERT INTO paimon_orders
SELECT * FROM mysql_orders_cdc;
```

---

## 7. Visualizations

### 7.1 Connector Ecosystem Panorama

```mermaid
graph TB
    subgraph "Flink Connector Ecosystem"
        subgraph "Message Queue Layer"
            K[Kafka]
            P[Pulsar]
            R[RabbitMQ]
            KIN[Amazon Kinesis]
            PS[Google Pub/Sub]
            M[MQTT]
        end

        subgraph "File System Layer"
            H[HDFS]
            S3[Amazon S3]
            GCS[Google Cloud Storage]
            AZ[Azure Blob Storage]
            OSS[Alibaba OSS]
        end

        subgraph "Database Layer"
            JDBC[JDBC<br/>MySQL/PG/Oracle]
            C[Cassandra]
            HB[HBase]
            ES[Elasticsearch]
            MG[MongoDB]
            RD[Redis]
            INF[InfluxDB]
        end

        subgraph "Lakehouse Layer"
            ICE[Apache Iceberg]
            HUD[Apache Hudi]
            PAI[Apache Paimon]
            DL[Delta Lake]
            FL[Apache Fluss]
        end

        subgraph "CDC Layer"
            CDC_M[MySQL CDC]
            CDC_P[PostgreSQL CDC]
            CDC_O[Oracle CDC]
            CDC_MG[MongoDB CDC]
            CDC_S[SQL Server CDC]
        end
    end

    subgraph "Flink Compute Engine"
        FS[Flink Streaming]
        FB[Flink Batch]
        SQL[Flink SQL]
    end

    K --> FS
    P --> FS
    R --> FS
    KIN --> FS
    PS --> FS
    M --> FS

    H --> FB
    S3 --> FB
    GCS --> FB
    AZ --> FB
    OSS --> FB

    JDBC --> FS
    C --> FS
    HB --> FS
    ES --> FS
    MG --> FS
    RD --> FS
    INF --> FS

    ICE --> FS
    ICE --> FB
    HUD --> FS
    HUD --> FB
    PAI --> FS
    DL --> FB
    FL --> FS

    CDC_M --> FS
    CDC_P --> FS
    CDC_O --> FS
    CDC_MG --> FS
    CDC_S --> FS

    FS --> K
    FS --> P
    FB --> S3
    FB --> H
    FS --> JDBC
    FS --> ES
    FS --> ICE
    FS --> HUD
    FS --> PAI
```

---

### 7.2 Connector Selection Decision Tree

```mermaid
flowchart TD
    A[Data Source/Target Type] --> B{Real-time Stream Processing Required?}

    B -->|Yes| C{Message Type?}
    B -->|No| D{Batch Processing Data?}

    C -->|Log/Event| E[Choose Kafka/Pulsar]
    C -->|IoT/MQTT| F[Choose MQTT Broker]
    C -->|Cloud Service| G{Cloud Platform?}

    G -->|AWS| H[Choose Kinesis]
    G -->|GCP| I[Choose Pub/Sub]
    G -->|Azure| J[Choose Event Hubs]

    D -->|File Data| K{Storage Location?}
    D -->|Structured Data| L{Data Scale?}

    K -->|Local/HDFS| M[Choose FileSystem Connector]
    K -->|Cloud Object Storage| N{Cloud Provider?}
    N -->|AWS| O[Choose S3 Connector]
    N -->|GCP| P[Choose GCS Connector]
    N -->|Azure| Q[Choose Azure Blob Connector]
    N -->|Alibaba Cloud| R[Choose OSS Connector]

    L -->|TB-level+| S{Analysis Requirement?}
    L -->|GB-level| T[Choose JDBC Connector]

    S -->|Real-time Analysis| U[Choose Lakehouse<br/>Iceberg/Hudi/Paimon]
    S -->|Offline Analysis| V[Choose Data Lake Format<br/>Parquet/ORC on S3]

    T --> W{Database Type?}
    W -->|Relational| X[MySQL/PostgreSQL/Oracle]
    W -->|NoSQL| Y{Access Pattern?}

    Y -->|Key-Value| Z[Choose Redis/HBase]
    Y -->|Document| AA[Choose MongoDB]
    Y -->|Search| AB[Choose Elasticsearch]
    Y -->|Wide Column| AC[Choose Cassandra]

    E --> AD{Exactly-Once Required?}
    AD -->|Yes| AE[Enable Kafka Transactions]
    AD -->|No| AF[At-Least-Once Mode]
```

---

### 7.3 Data Flow Integration Architecture

```mermaid
graph TB
    subgraph "Data Source Layer"
        DB1[(MySQL)]
        DB2[(PostgreSQL)]
        KAFKA[Kafka Cluster]
        FILES[Data Files<br/>S3/HDFS]
    end

    subgraph "CDC & Ingestion Layer"
        CDC[Flink CDC 3.0]
        K_SOURCE[Kafka Source]
        F_SOURCE[File Source]
    end

    subgraph "Flink Processing Layer"
        subgraph "Stream Processing"
            STREAM[DataStream API]
            SQL[Flink SQL]
        end
        subgraph "State Management"
            STATE[Keyed State]
            WINDOW[Window State]
        end
        subgraph "Processing Logic"
            JOIN[Stream Join]
            AGG[Aggregation]
            FILTER[Filter/Map]
        end
    end

    subgraph "Data Target Layer"
        ICE[(Iceberg<br/>Lakehouse)]
        HUD[(Hudi)]
        PAI[(Paimon)]
        DW[(Doris<br/>StarRocks)]
        ES2[(Elasticsearch)]
        K_SINK[Kafka Output]
    end

    DB1 --> CDC
    DB2 --> CDC
    KAFKA --> K_SOURCE
    FILES --> F_SOURCE

    CDC --> STREAM
    K_SOURCE --> STREAM
    F_SOURCE --> STREAM

    STREAM --> SQL
    SQL --> JOIN
    JOIN --> AGG
    AGG --> STATE
    AGG --> WINDOW
    WINDOW --> FILTER

    FILTER --> ICE
    FILTER --> HUD
    FILTER --> PAI
    FILTER --> DW
    FILTER --> ES2
    FILTER --> K_SINK
```

---

### 7.4 Connector State Machine

```mermaid
stateDiagram-v2
    [*] --> CREATED: Create Connector
    CREATED --> INITIALIZING: Initialize Config

    INITIALIZING --> RUNNING: Start Success
    INITIALIZING --> FAILED: Config Error

    RUNNING --> CHECKPOINTING: Checkpoint Trigger
    CHECKPOINTING --> RUNNING: Checkpoint Success
    CHECKPOINTING --> FAILED: Checkpoint Failure

    RUNNING --> RECOVERING: Failure Detected
    RECOVERING --> RUNNING: Recovery Success
    RECOVERING --> FAILED: Recovery Failure

    RUNNING --> SUSPENDED: Suspend Job
    SUSPENDED --> RUNNING: Resume Job
    SUSPENDED --> CANCELLED: Cancel Job

    RUNNING --> CANCELLED: Normal Shutdown
    FAILED --> CANCELLED: Cleanup Resources

    CANCELLED --> [*]

    note right of CHECKPOINTING
        Source: Save read position
        Sink: preCommit
        State: Persist state
    end note

    note right of RECOVERING
        Recover from Checkpoint
        Source: seek to saved position
        Sink: Clean up pending transactions
    end note
```

---

## 8. Configuration & Performance

### 8.1 Global Configuration Best Practices

**Checkpoint Configuration**:

```java

// [Pseudo-code snippet - not directly runnable] Core logic only
import org.apache.flink.streaming.api.CheckpointingMode;

// Checkpoint configuration
env.enableCheckpointing(60000, CheckpointingMode.EXACTLY_ONCE);
env.getCheckpointConfig().setCheckpointTimeout(600000);
env.getCheckpointConfig().setMinPauseBetweenCheckpoints(30000);
env.getCheckpointConfig().setMaxConcurrentCheckpoints(1);
env.getCheckpointConfig().setExternalizedCheckpointCleanup(
    CheckpointConfig.ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION);

// State backend configuration
env.setStateBackend(new EmbeddedRocksDBStateBackend(true));
env.getCheckpointConfig().setCheckpointStorage("s3://bucket/checkpoints");
```

**Network & Serialization Configuration**:

```java
// [Pseudo-code snippet - not directly runnable] Core logic only
// Network buffer configuration
Configuration conf = new Configuration();
conf.setInteger("taskmanager.memory.network.max", 256 << 20); // 256MB
conf.setInteger("taskmanager.memory.network.min", 128 << 20); // 128MB

// Serialization configuration
env.getConfig().setAutoTypeRegistrationWithKryo(true);
env.getConfig().addDefaultKryoSerializer(MyClass.class, MySerializer.class);
```

**Source General Configuration**:

| Parameter | Recommended Value | Description |
|-----------|-------------------|-------------|
| `source.parallelism` | Match external partition count | Avoid resource waste |
| `source.watermark-interval` | 200ms | Watermark generation interval |
| `source.idle-timeout` | 30s | Idle source detection |

**Sink General Configuration**:

| Parameter | Recommended Value | Description |
|-----------|-------------------|-------------|
| `sink.buffer-flush.max-rows` | 1000-5000 | Batch write size |
| `sink.buffer-flush.interval` | 1-5s | Batch flush interval |
| `sink.max-retries` | 3-10 | Max retry count |
| `sink.retry-interval` | 1-5s | Retry interval |

---

### 8.2 Connector Performance Comparison Matrix

**Source Performance Comparison**:

| Connector | Throughput (records/s) | Latency | Scalability | CPU Usage | Memory Usage |
|-----------|------------------------|---------|-------------|-----------|--------------|
| **Kafka** | 500K-2M | Low (ms) | ⭐⭐⭐⭐⭐ | Medium | Medium |
| **Pulsar** | 400K-1.5M | Low (ms) | ⭐⭐⭐⭐⭐ | Medium | Medium |
| **Kinesis** | 200K-500K | Medium (100ms) | ⭐⭐⭐⭐ | Medium | Medium |
| **JDBC** | 10K-50K | High (100ms+) | ⭐⭐⭐ | Low | Low |
| **Iceberg** | 100K-500K | High (second-level) | ⭐⭐⭐⭐⭐ | Medium | High |
| **Files** | 50K-200K | High (second-level) | ⭐⭐⭐⭐ | Low | Low |

**Sink Performance Comparison**:

| Connector | Throughput (records/s) | Latency | Exactly-Once Overhead | Recommended Scenario |
|-----------|------------------------|---------|-----------------------|----------------------|
| **Kafka** | 300K-1M | Low | 20-30% | Real-time pipeline |
| **Pulsar** | 250K-800K | Low | 20-30% | Real-time pipeline |
| **Iceberg** | 50K-200K | Medium | 10-20% | Data lake |
| **Hudi** | 30K-100K | Medium | 15-25% | Incremental update |
| **Paimon** | 50K-150K | Low | 10-15% | Unified batch/stream |
| **JDBC** | 5K-20K | High | 30-50% | Relational storage |
| **Elasticsearch** | 20K-50K | Low | None | Full-text search |
| **Redis** | 100K-300K | Very low | None | Cache |

**End-to-End Latency Comparison** (Source → Flink → Sink):

| Pipeline Combination | Typical Latency | Applicable Scenario |
|----------------------|-----------------|---------------------|
| Kafka → Flink → Kafka | 50-200ms | Real-time stream processing |
| Kafka → Flink → Iceberg | 5-30s | Real-time lake ingestion |
| MySQL CDC → Flink → Doris | 100ms-2s | Real-time data warehouse |
| Files → Flink → S3 | Minute-level | Offline batch processing |
| Kinesis → Flink → Kinesis | 100-500ms | AWS real-time processing |

---

### 8.3 Common Issues Troubleshooting Guide

**Issue 1: Kafka Source Consumption Lag**

```
Symptom: records-lag-max keeps increasing

Diagnosis:
1. Check Flink backpressure: backPressuredTimeMsPerSecond
2. Check if parallelism matches Kafka partition count
3. Check data skew: processing rate of each subtask

Resolution:
- Increase Flink parallelism = Kafka partition count
- Optimize downstream processing logic
- Scale out Kafka partition count
```

**Issue 2: JDBC Sink Connection Timeout**

```
Symptom: Connection timeout / Connection pool exhausted

Diagnosis:
1. Check database connection count limit
2. Check network stability
3. Check Checkpoint interval vs transaction timeout

Resolution:
- Increase connection.max-retry-timeout
- Decrease batch.size and increase flush.interval
- Use connection pool (HikariCP)
- Increase database connection count limit
```

**Issue 3: Iceberg Sink Too Many Small Files**

```
Symptom: Metadata file bloat, query performance degradation

Diagnosis:
1. Check if Checkpoint interval is too short
2. Check data volume to file size ratio

Resolution:
- Increase Checkpoint interval (recommended 1-5 min)
- Configure Compaction jobs
- Adjust write.target-file-size-bytes (recommended 128MB+)
```

**Issue 4: CDC Sync Data Inconsistency**

```
Symptom: Target data inconsistent with source

Diagnosis:
1. Check if schema change is synchronized
2. Check primary key conflict handling
3. Check timestamp field configuration

Resolution:
- Enable include.schema.changes
- Configure correct merge-engine
- Verify primary key uniqueness
```

**Issue 5: Checkpoint Timeout**

```
Symptom: Checkpoint frequently times out and fails

Diagnosis:
1. Check State size
2. Check if Sink side is blocking
3. Check network bandwidth

Resolution:
- Increase Checkpoint timeout
- Enable incremental Checkpoint
- Optimize State TTL
- Check external system health
```

---

## 9. References


---

*Document version: v1.0 | Created: 2026-04-04 | Last updated: 2026-04-04 | Connectors covered: 30+ | Formal elements: 10+ (5 definitions + 2 lemmas + 2 propositions + 2 theorems)*

---

*Document version: v1.0 | Created: 2026-04-19*
