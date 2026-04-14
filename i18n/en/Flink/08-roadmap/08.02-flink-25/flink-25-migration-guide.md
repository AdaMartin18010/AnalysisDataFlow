---
title: "Flink 2.5 Migration Guide"
translation_status: ai_translated_reviewed
source_version: v4.1
last_sync: "2026-04-15"
---

# Flink 2.5 Migration Guide

> **Status**: Preview | **Estimated Release**: 2026-Q3 | **Last Updated**: 2026-04-12
>
> ⚠️ The features described in this document are in early discussion stages and have not been officially released. Implementation details may change.

> Stage: Flink/08-roadmap | Prerequisites: [Flink 2.4 Release](../08.01-flink-24/flink-2.4-tracking.md) | Formalization Level: L3

---

## 1. Migration Overview

### 1.1 Version Compatibility

| Component | Compatibility | Migration Effort | Notes |
|------|--------|------------|------|
| SQL/Table API | ✅ Fully Compatible | None | No changes needed |
| DataStream API | ✅ Source Compatible | Low | Recompile only |
| Connectors | ✅ Compatible | None | No changes needed |
| State Backend | ⚠️ Configuration Changes | Low | Configuration items updated |
| Checkpoint | ✅ Compatible | None | Automatic compatibility |
| Deployment Configuration | ⚠️ Configuration Changes | Low | New Serverless options added |

### 1.2 Migration Checklist

```markdown
□ Backup existing jobs (Savepoint)
□ Check deprecated API usage
□ Update Flink version dependencies
□ Update configuration files
□ Test job functionality
□ Performance benchmark comparison
□ Production environment canary release
```

---

## 2. Dependency Updates

### 2.1 Maven Dependencies

```xml
<!-- Flink 2.5 Dependencies -->
<properties>
    <flink.version>2.5.0</flink.version>
</properties>

<dependencies>
    <!-- Core -->
    <dependency>
        <groupId>org.apache.flink</groupId>
        <artifactId>flink-streaming-java</artifactId>
        <version>${flink.version}</version>
    </dependency>

    <!-- Table API -->
    <dependency>
        <groupId>org.apache.flink</groupId>
        <artifactId>flink-table-api-java</artifactId>
        <version>${flink.version}</version>
    </dependency>

    <!-- Connectors -->
    <dependency>
        <groupId>org.apache.flink</groupId>
        <artifactId>flink-connector-kafka</artifactId>
        <version>3.5.0-2.5</version>
    </dependency>
</dependencies>
```

### 2.2 Gradle Dependencies

```groovy
ext {
    flinkVersion = '2.5.0'
}

dependencies {
    implementation "org.apache.flink:flink-streaming-java:${flinkVersion}"
    implementation "org.apache.flink:flink-table-api-java:${flinkVersion}"
    implementation "org.apache.flink:flink-connector-kafka:3.5.0-2.5"
}
```

---

## 3. Configuration Migration

### 3.1 State Backend Configuration

**Flink 2.4 Configuration**:

```yaml
# 2.4 Configuration
state.backend: rocksdb
state.backend.incremental: true
state.checkpoint-storage: filesystem
state.checkpoints.dir: s3://flink-checkpoints
```

**Flink 2.5 Equivalent Configuration**:

```yaml
# 2.5 Configuration (Recommended)
state.backend: forst                    # ForSt becomes the recommended backend
state.backend.forst.remote.path: s3://flink-state/{job-id}
state.backend.incremental: true
state.checkpoint-storage: filesystem
state.checkpoints.dir: s3://flink-checkpoints

# Optional: Tiered storage configuration
state.backend.forst.cache.path: /tmp/flink-cache
state.backend.forst.cache.capacity: 10GB
```

### 3.2 Serverless Configuration (New)

```yaml
# Enable Serverless mode
execution.mode: serverless

# Auto-scaling
kubernetes.operator.job.autoscaler.enabled: true
kubernetes.operator.job.autoscaler.scale-to-zero.enabled: true
kubernetes.operator.job.autoscaler.scale-to-zero.grace-period: 300s

# Fast cold start
serverless.cold-start.mode: warmup-pool
serverless.cold-start.warmup-pool-size: 2
```

### 3.3 Execution Mode Configuration

```yaml
# Flink 2.5 adds adaptive execution mode
execution.runtime-mode: adaptive        # New option
# Or keep existing settings
execution.runtime-mode: streaming
execution.runtime-mode: batch
```

---

## 4. API Migration

### 4.1 DataStream API

**No changes needed**, fully compatible:

```java

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

// Flink 2.4 code works without modification in 2.5
StreamExecutionEnvironment env =
    StreamExecutionEnvironment.getExecutionEnvironment();

DataStream<Event> stream = env
    .fromSource(kafkaSource, watermarkStrategy, "Kafka Source");

stream
    .keyBy(Event::getUserId)
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .aggregate(new CountAggregate())
    .sinkTo(sink);

env.execute("My Job");
```

### 4.2 Table API / SQL

**Fully compatible**, no changes needed.

**New in 2.5** (Optional usage):

```java

import org.apache.flink.table.api.TableEnvironment;

// Enable adaptive execution mode (optional)
TableEnvironment tEnv = TableEnvironment.create(settings);
tEnv.getConfig().set("execution.runtime-mode", "adaptive");

// Materialized table GA (if used)
tEnv.executeSql("""
    CREATE MATERIALIZED TABLE user_stats
    WITH (
        'refresh-mode' = 'incremental',
        'refresh-interval' = '5 minutes'
    )
    AS SELECT ...
""");
```

### 4.3 Deprecated API Replacements

| Deprecated API (2.4) | Replacement (2.5) |
|----------------|----------------|
| `DataSet API` | Removed, use Table API or DataStream |
| `FlinkKafkaConsumer` | `KafkaSource` |
| `FlinkKafkaProducer` | `KafkaSink` |
| `RocksDBStateBackend` | `ForStStateBackend` |

---

## 5. State Migration

### 5.1 Recovering from Checkpoint

```bash
# Use 2.4 Checkpoint to recover in 2.5
flink run \
    -Dexecution.runtime-mode=streaming \
    -s s3://flink-checkpoints/2.4-job/checkpoint-xxxxx \
    ./my-job-2.5.jar
```

### 5.2 State Compatibility

| State Backend | 2.4 → 2.5 Compatibility | Notes |
|----------|------------------|------|
| HashMapStateBackend | ✅ Compatible | Automatic migration |
| RocksDBStateBackend | ✅ Compatible | Automatic migration |
| ForStStateBackend | ✅ Compatible | Recommended backend |

### 5.3 Savepoint Migration

```bash
# 1. Create Savepoint from 2.4 job
flink savepoint <job-id> s3://flink-savepoints/migration

# 2. Start 2.5 job using Savepoint
flink run \
    -Dstate.backend=forst \
    -s s3://flink-savepoints/migration/savepoint-xxxxx \
    ./my-job-2.5.jar
```

---

## 6. Serverless Migration

### 6.1 Traditional Deployment → Serverless

**Traditional Deployment (2.4)**:

```yaml
# flink-conf.yaml (2.4)
jobmanager.memory.process.size: 2gb
taskmanager.memory.process.size: 8gb
taskmanager.numberOfTaskSlots: 4
parallelism.default: 4
```

**Serverless Deployment (2.5)**:

```yaml
# flink-conf.yaml (2.5)
execution.mode: serverless

# Resource configuration changed to ranges
kubernetes.operator.job.autoscaler:
  enabled: true
  min-parallelism: 1
  max-parallelism: 100

# TaskManager resource configuration
taskmanager.memory.process.size: 4gb
taskmanager.numberOfTaskSlots: 2

# Serverless-specific configuration
serverless.cold-start.mode: warmup-pool
serverless.cold-start.warmup-pool-size: 2
```

### 6.2 Kubernetes Deployment Update

```yaml
# flink-deployment-2.5.yaml
apiVersion: flink.apache.org/v1beta1
kind: FlinkDeployment
metadata:
  name: my-job
spec:
  image: flink:2.5.0
  flinkVersion: v2.5

  jobManager:
    resource:
      memory: 2Gi
      cpu: 1

  taskManager:
    resource:
      memory: 4Gi
      cpu: 2
    # Serverless configuration (new)
    serverless:
      enabled: true
      scale-to-zero:
        enabled: true
        idle-timeout: 10m
```

---

## 7. FAQ

### 7.1 Startup Failure

**Problem**: Job reports configuration error at startup

```
Caused by: IllegalArgumentException: Unknown configuration key: state.backend.rocksdb.memory.managed
```

**Solution**: Update configuration key name

```yaml
# Old configuration
state.backend.rocksdb.memory.managed: true

# New configuration
state.backend.forst.memory.managed: true
```

### 7.2 Performance Degradation

**Problem**: Job throughput decreases after migration

**Troubleshooting Steps**:

1. Check if state backend configuration is correct
2. Verify Checkpoint configuration
3. Compare GC logs
4. Check network buffer configuration

**Solution**:

```yaml
# Tune network buffers
taskmanager.memory.network.min: 256mb
taskmanager.memory.network.max: 512mb

# Tune Checkpoint
execution.checkpointing.interval: 30s
execution.checkpointing.max-concurrent-checkpoints: 1
```

### 7.3 Serverless Cold Start Slow

**Problem**: Slow recovery after scale-from-zero

**Solution**:

```yaml
# Enable warmup pool
serverless.cold-start.mode: warmup-pool
serverless.cold-start.warmup-pool-size: 2

# Optimize state recovery
state.backend.forst.incremental-recovery: true
state.backend.forst.restore.parallelism: 10
```

---

## 8. Rollback Plan

### 8.1 Rolling Back to 2.4

```bash
# 1. Create Savepoint of 2.5 job
flink savepoint <2.5-job-id> s3://flink-savepoints/rollback

# 2. Redeploy using 2.4 image
flink run \
    -Dstate.backend=rocksdb \
    -s s3://flink-savepoints/rollback/savepoint-xxxxx \
    ./my-job-2.4.jar
```

**Note**:

- 2.5 new features (e.g., Serverless) will be unavailable after rollback
- Ensure 2.4 configuration is compatible with 2.5

---

## 9. Best Practices

### 9.1 Migration Strategy

```
Suggested Migration Process:

Week 1: Development Environment Verification
  - Update dependencies and configuration
  - Functional testing
  - Performance benchmark testing

Week 2: Pre-production Environment Verification
  - Integration testing
  - Long-term stability testing
  - Checkpoint/recovery testing

Week 3: Production Canary Release
  - 5% traffic verification
  - Monitoring metric comparison
  - Gradually expand traffic

Week 4: Full Migration
  - 100% traffic switch
  - Retain 2.4 rollback capability
  - Monitoring and optimization
```

### 9.2 Configuration Template

```yaml
# flink-conf.yaml - Flink 2.5 Recommended Configuration Template

# Execution mode
execution.mode: adaptive
execution.runtime-mode: streaming

# State backend (ForSt recommended)
state.backend: forst
state.backend.forst.remote.path: s3://flink-state/{job-id}
state.backend.forst.cache.capacity: 10GB

# Checkpoint
execution.checkpointing.interval: 30s
execution.checkpointing.mode: EXACTLY_ONCE
state.checkpoint-storage: filesystem
state.checkpoints.dir: s3://flink-checkpoints/{job-id}

# Serverless (optional)
kubernetes.operator.job.autoscaler.enabled: true
kubernetes.operator.job.autoscaler.scale-to-zero.enabled: false  # Enable with caution

# Network
taskmanager.memory.network.min: 256mb
taskmanager.memory.network.max: 512mb

# Restart strategy
restart-strategy: fixed-delay
restart-strategy.fixed-delay.attempts: 10
restart-strategy.fixed-delay.delay: 10s
```

---

*Last Updated: 2026-04-08*
