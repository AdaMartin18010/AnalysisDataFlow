---
title: "Flink 2.5 Features Detailed Preview"
translation_status: ai_translated_reviewed
source_version: v4.1
last_sync: "2026-04-15"
---

# Flink 2.5 Features Detailed Preview

> **Status**: Forward-looking | **Estimated Release**: 2026-Q3 | **Last Updated**: 2026-04-12
>
> ⚠️ The features described in this document are in early discussion stages and have not been officially released. Implementation details may change.

> Stage: Flink/08-roadmap | **Prerequisites**: [Flink 2.5 Roadmap](./flink-25-roadmap.md) | **Formalization Level**: L3

---

## 1. Unified Streaming-Batch Execution Engine (FLIP-435)

### 1.1 Core Concepts

Flink 2.5 introduces a true unified streaming-batch execution engine, eliminating runtime-level differences between stream processing and batch processing.

```
┌─────────────────────────────────────────────────────────────┐
│                    Unified Optimizer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ SQL Parser   │  │ Table API    │  │ DataStream API   │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘  │
│         └─────────────────┴───────────────────┘             │
│                           │                                 │
│                    Unified Logical Plan                     │
│                           │                                 │
│         ┌─────────────────┼─────────────────┐               │
│         ▼                 ▼                 ▼               │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐          │
│  │  Streaming │   │   Batch    │   │  Hybrid    │          │
│  │   Mode     │   │   Mode     │   │   Mode     │          │
│  └────────────┘   └────────────┘   └────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Adaptive Execution Mode

```java

import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

// Automatically select the optimal execution mode
ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();

// Configure adaptive execution
env.getConfig().set("execution.runtime-mode", "ADAPTIVE");
env.getConfig().set("execution.adaptive.latency-threshold", "100ms");

// Unified processing logic, runtime automatically selects execution mode
DataStream<Event> stream = env.fromSource(kafkaSource, ...);
stream
    .keyBy(Event::getUserId)
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .aggregate(new CountAggregate())
    .sinkTo(sink);
```

### 1.3 Hybrid Execution Example

```sql
-- Streaming-batch hybrid query: real-time stream JOIN historical batch data
SELECT
    s.user_id,
    s.event_type,
    s.amount as realtime_amount,
    h.total_amount as historical_total
FROM real_time_events s  -- Stream data source (Kafka)
LEFT JOIN user_history h   -- Batch data source (Iceberg)
    ON s.user_id = h.user_id
    AND h.dt >= CURRENT_DATE - INTERVAL '30' DAY
WHERE s.event_type = 'PURCHASE';
```

---

## 2. Serverless Flink GA (FLIP-442)

### 2.1 Scale-to-Zero

```yaml
# flink-conf.yaml
kubernetes.operator.job.autoscaler.enabled: true
kubernetes.operator.job.autoscaler.scale-to-zero.enabled: true
kubernetes.operator.job.autoscaler.scale-to-zero.grace-period: 300s
kubernetes.operator.job.autoscaler.scale-to-zero.idle-timeout: 600s
```

**Behavior Description**:

1. When a job has no traffic for more than `idle-timeout` (10 minutes), trigger Scale-to-Zero
2. Save the final Checkpoint to remote storage
3. Release all TaskManager resources
4. When new data arrives, quickly recover from Checkpoint

### 2.2 Fast Cold Start

```yaml
# Fast cold start optimization configuration
serverless.cold-start:
  mode: warmup-pool          # Warm-up pool mode
  warmup-pool-size: 2        # Keep 2 warm-up instances
  max-concurrent-startups: 10
  startup-timeout: 30s

  # Image optimization
  image:
    preloaded-jars:          # Pre-loaded JAR packages
      - flink-connector-kafka
      - flink-connector-jdbc
    jvm-warmup: true         # JVM warm-up
```

### 2.3 Predictive Auto-Scaling

```yaml
serverless.auto-scaling:
  enabled: true
  mode: predictive           # Predictive auto-scaling

  prediction:
    window-size: 5m          # Prediction window
    algorithm: lstm          # LSTM prediction model
    lookahead: 2m            # Predict 2 minutes ahead

  scaling:
    min-replicas: 0
    max-replicas: 100
    target-latency: 100ms    # Target processing latency
    scale-up-threshold: 0.8  # Scale-up threshold
    scale-down-threshold: 0.3 # Scale-down threshold
```

---

## 3. AI/ML Inference Optimization

### 3.1 Dynamic Batching

```java

import org.apache.flink.streaming.api.datastream.DataStream;

// Dynamic batching configuration
ModelInferenceConfig config = ModelInferenceConfig.builder()
    .withBatching(true)
    .withMaxBatchSize(32)
    .withMaxLatencyMs(50)    // Maximum wait time
    .withAdaptiveBatching(true)  // Adjust batch size based on load
    .build();

// Automatic batch inference
DataStream<Prediction> predictions = events
    .keyBy(Event::getModelId)
    .process(new BatchedModelInferenceFunction(config));
```

### 3.2 KV-Cache Sharing

```java
// Enable cross-request KV-Cache sharing
InferenceConfig config = InferenceConfig.builder()
    .withKvCacheSharing(true)
    .withPrefixCaching(true)      // Prefix caching
    .withMaxCacheSizeMB(2048)
    .withCacheEvictionPolicy("lru")
    .build();
```

### 3.3 Model Serving Configuration

```yaml
# AI inference service configuration
ai.inference:
  enabled: true

  models:
    - id: text-generation-v1
      path: s3://models/llama-2-7b
      framework: vllm
      device: GPU
      replicas: 2

      # Inference optimization
      optimization:
        batching: true
        speculative-decoding: true
        kv-cache-sharing: true

      # Auto-scaling
      autoscaling:
        min-replicas: 1
        max-replicas: 10
        target-qps: 100
```

---

## 4. Materialized Table GA (FLIP-516)

### 4.1 Auto-Refresh Configuration

```sql
-- Create materialized table with auto-refresh
CREATE MATERIALIZED TABLE user_stats
WITH (
    'format' = 'parquet',
    'partition.fields' = 'dt',
    'refresh-mode' = 'incremental',      -- Incremental refresh
    'refresh-interval' = '5 minutes',     -- Refresh interval
    'refresh-trigger' = 'watermark'       -- Triggered by Watermark
)
AS SELECT
    user_id,
    COUNT(*) as event_count,
    SUM(amount) as total_amount,
    DATE_FORMAT(event_time, 'yyyy-MM-dd') as dt
FROM user_events
GROUP BY user_id, DATE_FORMAT(event_time, 'yyyy-MM-dd');
```

### 4.2 Lakehouse Integration

```sql
-- Iceberg materialized table
CREATE MATERIALIZED TABLE iceberg_user_stats
WITH (
    'connector' = 'iceberg',
    'catalog' = 'iceberg_catalog',
    'database' = 'analytics',
    'table' = 'user_stats',
    'write-mode' = 'merge-on-read',      -- MOR mode
    'compaction.enabled' = 'true'
)
AS SELECT ...;
```

---

## 5. WebAssembly UDF GA (FLIP-448)

### 5.1 Multi-Language UDF Support

```rust
// Rust-written WASM UDF
#[no_mangle]
pub extern "C" fn sentiment_score(text: &str) -> f64 {
    // Sentiment analysis logic
    analyze_sentiment(text)
}
```

```go
// Go-written WASM UDF
//export geo_distance
func geo_distance(lat1, lon1, lat2, lon2 float64) float64 {
    // Distance calculation logic
    return calculateDistance(lat1, lon1, lat2, lon2)
}
```

### 5.2 Flink Registration and Usage

```java

import org.apache.flink.table.api.TableEnvironment;

// Register multi-language WASM UDF
TableEnvironment tEnv = TableEnvironment.create(...);

// Rust UDF
tEnv.createTemporarySystemFunction(
    "sentiment_score",
    WasmScalarFunction.builder()
        .withWasmModule("sentiment.wasm")
        .withFunctionName("sentiment_score")
        .withLanguage(WasmLanguage.RUST)
        .withSandbox(WasmSandbox.STRICT)
        .build()
);

// Go UDF
tEnv.createTemporarySystemFunction(
    "geo_distance",
    WasmScalarFunction.builder()
        .withWasmModule("geo.wasm")
        .withFunctionName("geo_distance")
        .withLanguage(WasmLanguage.GO)
        .withSandbox(WasmSandbox.STRICT)
        .build()
);

// SQL usage
String sql = """
    SELECT
        review_id,
        sentiment_score(review_text) as sentiment,
        geo_distance(user_lat, user_lon, store_lat, store_lon) as distance_km
    FROM reviews
    WHERE sentiment_score(review_text) > 0.5
""";
```

---

## 6. Performance Benchmarks

### 6.1 Unified Streaming-Batch Performance

| Scenario | Flink 2.4 | Flink 2.5 Target | Improvement |
|----------|-----------|------------------|-------------|
| Stream processing throughput | 100K events/s | 120K events/s | +20% |
| Batch processing throughput | 500MB/s | 650MB/s | +30% |
| Hybrid query latency | 500ms | 200ms | 2.5x |

### 6.2 Serverless Performance

| Metric | Flink 2.4 Beta | Flink 2.5 GA |
|--------|----------------|--------------|
| Cold start time | 2s | 500ms |
| Auto-scaling latency | 30s | 10s |
| Scale-to-Zero | 60s | 10s |

### 6.3 AI Inference Performance

| Metric | Flink 2.4 | Flink 2.5 |
|--------|-----------|-----------|
| Inference latency (P99) | 2s | 500ms |
| Throughput | 100 req/s | 500 req/s |
| GPU utilization | 40% | 80% |

---

## 7. Configuration Reference

### 7.1 Complete Configuration Example

```yaml
# flink-conf.yaml - Flink 2.5 complete configuration

# ==========================================
# Execution engine configuration
# ==========================================
execution.mode: adaptive
execution.adaptive.optimizer: unified
execution.adaptive.mode-detection: auto

# ==========================================
# Serverless configuration
# ==========================================
kubernetes.operator.job.autoscaler.enabled: true
kubernetes.operator.job.autoscaler.scale-to-zero.enabled: true
serverless.cold-start.mode: warmup-pool
serverless.cold-start.warmup-pool-size: 2

# ==========================================
# State backend configuration
# ==========================================
state.backend: forst
state.backend.forst.remote.path: s3://flink-state/{job-id}
state.backend.forst.cache.capacity: 10GB

# ==========================================
# AI inference configuration
# ==========================================
ai.inference.enabled: true
ai.inference.optimization.batching: true
ai.inference.optimization.kv-cache-sharing: true

# ==========================================
# WASM UDF configuration
# ==========================================
wasm.udf.enabled: true
wasm.udf.wasi-version: preview2
wasm.udf.sandbox: strict
```

---

*Last Updated: 2026-04-08*
