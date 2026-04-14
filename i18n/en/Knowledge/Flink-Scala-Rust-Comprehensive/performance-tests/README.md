---
title: "Stream Computing Performance Test Suite"
translation_status: "ai_translated_reviewed"
source_version: "v4.1"
last_sync: "2026-04-15"
---

# Stream Computing Performance Test Suite

This directory contains a complete stream computing performance testing framework for evaluating the performance of stream processing engines such as Flink, RisingWave, and Materialize.

## Directory Structure

```
performance-tests/
├── nexmark-benchmark-suite.md      # Nexmark benchmark documentation
├── simd-vectorization-benchmark.md # SIMD vectorization performance tests
├── wasm-udf-overhead-analysis.md   # WASM UDF overhead analysis
├── performance-test-framework.md   # Performance test framework documentation
├── README.md                       # This file
│
├── nexmark/                        # Nexmark test implementations
│   ├── flink/                      # Flink Scala implementation
│   │   ├── pom.xml
│   │   └── src/main/scala/nexmark/
│   ├── risingwave/                 # RisingWave SQL
│   └── materialize/                # Materialize SQL
│
├── simd/                           # SIMD vectorization tests
│   ├── rust/                       # Rust SIMD implementation
│   │   ├── Cargo.toml
│   │   ├── src/
│   │   └── benches/
│   └── java/                       # Java Vector API
│       └── VectorizedOperations.java
│
└── wasm/                           # WASM UDF tests
    ├── rust/                       # Rust WASM implementation
    ├── java/                       # JNI comparison
    └── scala/                      # Flink WASM integration
```

## Quick Start

### 1. Environment Requirements

- JDK 11+
- Scala 2.12
- Rust 1.75+
- Apache Flink 1.18+
- Python 3.9+ (for report generation)

### 2. Running Nexmark Tests

```bash
cd nexmark/flink
mvn clean package

# Run Q5 test
flink run -p 4 target/nexmark-flink-1.0-SNAPSHOT.jar \
  --query Q5 \
  --parallelism 4 \
  --max-events 10000000 \
  --events-per-second 100000
```

### 3. Running SIMD Tests

```bash
cd simd/rust
cargo bench

# View report
target/criterion/report/index.html
```

### 4. Running WASM Tests

```bash
cd wasm/rust
# Compile WASM
cargo build --target wasm32-unknown-unknown --release

# Run benchmark
cargo bench
```

## Key Findings

| Test Type | Key Finding |
|---------|---------|
| Nexmark | RisingWave is 1.5-2x faster than Flink on complex joins |
| SIMD | AVX-512 achieves 6-7x speedup; selectivity has minor impact |
| WASM | Invocation overhead is 10-50x; suitable for complex business logic rather than simple computation |

## Document Checklist

1. **nexmark-benchmark-suite.md** (40,002 bytes)
   - Complete Nexmark query set definition (Q0-Q12)
   - Flink/RisingWave/Materialize implementations
   - Performance comparison results and charts

2. **simd-vectorization-benchmark.md** (15,162 bytes)
   - SIMD test design methodology
   - Rust AVX2/AVX-512/NEON implementations
   - Java Vector API implementation

3. **wasm-udf-overhead-analysis.md** (17,554 bytes)
   - WASM vs JNI vs Native comparison
   - Function call/data transfer overhead tests
   - Selection decision tree

4. **performance-test-framework.md** (21,144 bytes)
   - Test framework architecture design
   - JMH + Criterion integration
   - Statistical analysis and visualization

**Total Document Size**: ~94KB
**Total Lines of Code**: 2000+ lines
