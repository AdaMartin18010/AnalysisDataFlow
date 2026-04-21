# Flink Ecosystem Overview

> **Status**: Stable | **Last Updated**: 2026-04-20
> **Stage**: Flink/05-ecosystem | **Prerequisites**: [Flink API Layer](../03-api/) | **Formalization Level**: L3
> **Translation Date**: 2026-04-21

## Abstract

This document serves as the authoritative navigation center for the Flink ecosystem, covering connectors, lakehouse integration, WASM UDF extensions, graph computing, and machine learning.

---

## 1. Ecosystem Structure

```
05-ecosystem/
├── Connectors/              # Data source/sink connectors
│   ├── Kafka, Pulsar, JDBC
│   ├── CDC (Change Data Capture)
│   └── File systems (S3, HDFS)
├── Lakehouse/               # Lakehouse storage integration
│   ├── Iceberg
│   ├── Paimon
│   └── Delta Lake
├── WASM UDF/                # WebAssembly UDF extensions
│   ├── Wasmtime runtime
│   └── WASI async preview
├── Graph Processing/        # Graph computing
│   ├── Gelly (batch)
│   └── Gelly Streaming
└── Third-party/             # External system integration
    ├── RisingWave
    ├── Materialize
    └── Confluent
```

---

## 2. Key Integration Patterns

### 2.1 Connector Ecosystem

| Connector | Source | Sink | Exactly-Once |
|-----------|--------|------|--------------|
| Kafka | ✅ | ✅ | ✅ (transactional) |
| Pulsar | ✅ | ✅ | ✅ |
| JDBC | ✅ | ✅ | ⚠️ (idempotent) |
| Elasticsearch | ❌ | ✅ | ⚠️ (idempotent) |
| Iceberg | ✅ | ✅ | ✅ |

### 2.2 Lakehouse Integration

| Format | Streaming Read | Streaming Write | Time Travel |
|--------|---------------|-----------------|-------------|
| Iceberg | ✅ | ✅ | ✅ |
| Paimon | ✅ | ✅ | ✅ |
| Delta Lake | ✅ | ✅ | ✅ |

### 2.3 WASM UDF

WebAssembly UDFs enable polyglot user-defined functions with sandboxed execution:

```sql
-- Call WASM UDF in Flink SQL
SELECT wasm_udf(input_column) FROM my_table;
```

---

## 3. References
