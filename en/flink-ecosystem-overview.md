# Flink Ecosystem Overview

> **Language**: English | **Source**: [Flink/05-ecosystem/README.md](../Flink/05-ecosystem/README.md) | **Last Updated**: 2026-04-21

---

## Ecosystem Boundary

Flink ecosystem defines the **complete interface set** for stream processing engine interaction with the external world:

```
┌─────────────────────────────────────────────────────────────┐
│                     Flink Ecosystem                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Connectors  │  │  Lakehouse  │  │  WASM UDF           │ │
│  │ Kafka/Pulsar│  │  Iceberg    │  │  User-defined funcs │ │
│  │ JDBC/ES/S3  │  │  Paimon     │  │  Polyglot runtime   │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  Graph      │  │  ML         │  │  Third-party        │ │
│  │  Gelly      │  │  Flink ML   │  │  RisingWave         │ │
│  │  Streaming  │  │  TensorFlow │  │  Confluent          │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Connectors

| Connector | Source | Sink | Exactly-Once | Use Case |
|-----------|--------|------|--------------|----------|
| **Kafka** | ✅ | ✅ | ✅ (EOS) | Event streaming |
| **Pulsar** | ✅ | ✅ | ✅ | Multi-tenant messaging |
| **JDBC** | ✅ | ✅ | ⚠️ (idempotent) | Database sync |
| **Elasticsearch** | ❌ | ✅ | ⚠️ (idempotent) | Search index |
| **S3/MinIO** | ✅ | ✅ | ✅ | File sink |
| **Iceberg** | ✅ | ✅ | ✅ | Lakehouse |

## Lakehouse Integration

| Format | Streaming Read | Streaming Write | Time Travel | Flink Version |
|--------|---------------|-----------------|-------------|---------------|
| **Iceberg** | ✅ V2 format | ✅ | ✅ | 1.14+ |
| **Paimon** | ✅ LSM tree | ✅ | ✅ | 1.17+ |
| **Hudi** | ✅ MOR table | ✅ | ⚠️ | 1.12+ |
| **Delta Lake** | ✅ | ✅ | ✅ | 1.13+ |

## WASM UDF

WebAssembly UDFs enable polyglot user-defined functions:

| Language | WASM Target | Performance | Maturity |
|----------|------------|-------------|----------|
| Rust | ✅ Native | ~90% of Java | Beta |
| C/C++ | ✅ Emscripten | ~85% of Java | Alpha |
| Go | ⚠️ TinyGo | ~70% of Java | Experimental |

## Graph Processing

| Library | Model | Scale | Status |
|---------|-------|-------|--------|
| **Gelly** | Batch/Sreaming | Medium | Deprecated |
| **Flink Graph API** | Streaming | Large | Preview |

## References

[^1]: Apache Flink Documentation, "Connectors", 2025.
[^2]: Apache Flink Documentation, "Lakehouse Integration", 2025.
