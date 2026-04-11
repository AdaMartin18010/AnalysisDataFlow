# Flink 2.5 迁移指南

> 所属阶段: Flink/08-roadmap | 前置依赖: [Flink 2.4 发布](../08.01-flink-24/flink-2.4-tracking.md) | 形式化等级: L3

---

## 1. 迁移概览

### 1.1 版本兼容性

| 组件 | 兼容性 | 迁移工作量 | 说明 |
|------|--------|------------|------|
| SQL/Table API | ✅ 完全兼容 | 无 | 无需修改 |
| DataStream API | ✅ 源码兼容 | 低 | 重新编译即可 |
| 连接器 | ✅ 兼容 | 无 | 无需修改 |
| 状态后端 | ⚠️ 配置变更 | 低 | 配置项更新 |
| Checkpoint | ✅ 兼容 | 无 | 自动兼容 |
| 部署配置 | ⚠️ 配置变更 | 低 | 新增 Serverless 选项 |

### 1.2 迁移 checklist

```markdown
□ 备份现有作业 (Savepoint)
□ 检查弃用 API 使用情况
□ 更新 Flink 版本依赖
□ 更新配置文件
□ 测试作业功能
□ 性能基准对比
□ 生产环境灰度发布
```

---

## 2. 依赖更新

### 2.1 Maven 依赖

```xml
<!-- Flink 2.5 依赖 -->
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

    <!-- 连接器 -->
    <dependency>
        <groupId>org.apache.flink</groupId>
        <artifactId>flink-connector-kafka</artifactId>
        <version>3.5.0-2.5</version>
    </dependency>
</dependencies>
```

### 2.2 Gradle 依赖

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

## 3. 配置迁移

### 3.1 状态后端配置

**Flink 2.4 配置**:

```yaml
# 2.4 配置
state.backend: rocksdb
state.backend.incremental: true
state.checkpoint-storage: filesystem
state.checkpoints.dir: s3://flink-checkpoints
```

**Flink 2.5 等效配置**:

```yaml
# 2.5 配置 (推荐)
state.backend: forst                    # ForSt 成为推荐后端
state.backend.forst.remote.path: s3://flink-state/{job-id}
state.backend.incremental: true
state.checkpoint-storage: filesystem
state.checkpoints.dir: s3://flink-checkpoints

# 可选：分层存储配置
state.backend.forst.cache.path: /tmp/flink-cache
state.backend.forst.cache.capacity: 10GB
```

### 3.2 Serverless 配置 (新增)

```yaml
# 启用 Serverless 模式
execution.mode: serverless

# 自动扩缩容
kubernetes.operator.job.autoscaler.enabled: true
kubernetes.operator.job.autoscaler.scale-to-zero.enabled: true
kubernetes.operator.job.autoscaler.scale-to-zero.grace-period: 300s

# 快速冷启动
serverless.cold-start.mode: warmup-pool
serverless.cold-start.warmup-pool-size: 2
```

### 3.3 执行模式配置

```yaml
# Flink 2.5 新增自适应执行模式
execution.runtime-mode: adaptive        # 新增选项
# 或保持原有设置
execution.runtime-mode: streaming
execution.runtime-mode: batch
```

---

## 4. API 迁移

### 4.1 DataStream API

**无需修改**，完全兼容：

```java
// Flink 2.4 代码在 2.5 中无需修改
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

**完全兼容**，无需修改。

**2.5 新增功能**（可选使用）：

```java
// 启用自适应执行模式（可选）
TableEnvironment tEnv = TableEnvironment.create(settings);
tEnv.getConfig().set("execution.runtime-mode", "adaptive");

// 物化表 GA（如使用）
tEnv.executeSql("""
    CREATE MATERIALIZED TABLE user_stats
    WITH (
        'refresh-mode' = 'incremental',
        'refresh-interval' = '5 minutes'
    )
    AS SELECT ...
""");
```

### 4.3 弃用 API 替换

| 弃用 API (2.4) | 替换方案 (2.5) |
|----------------|----------------|
| `DataSet API` | 已移除，使用 Table API 或 DataStream |
| `FlinkKafkaConsumer` | `KafkaSource` |
| `FlinkKafkaProducer` | `KafkaSink` |
| `RocksDBStateBackend` | `ForStStateBackend` |

---

## 5. 状态迁移

### 5.1 从 Checkpoint 恢复

```bash
# 使用 2.4 的 Checkpoint 在 2.5 中恢复
flink run \
    -Dexecution.runtime-mode=streaming \
    -s s3://flink-checkpoints/2.4-job/checkpoint-xxxxx \
    ./my-job-2.5.jar
```

### 5.2 状态兼容性

| 状态后端 | 2.4 → 2.5 兼容性 | 说明 |
|----------|------------------|------|
| HashMapStateBackend | ✅ 兼容 | 自动迁移 |
| RocksDBStateBackend | ✅ 兼容 | 自动迁移 |
| ForStStateBackend | ✅ 兼容 | 推荐后端 |

### 5.3 Savepoint 迁移

```bash
# 1. 从 2.4 作业创建 Savepoint
flink savepoint <job-id> s3://flink-savepoints/migration

# 2. 使用 Savepoint 启动 2.5 作业
flink run \
    -Dstate.backend=forst \
    -s s3://flink-savepoints/migration/savepoint-xxxxx \
    ./my-job-2.5.jar
```

---

## 6. Serverless 迁移

### 6.1 传统部署 → Serverless

**传统部署 (2.4)**:

```yaml
# flink-conf.yaml (2.4)
jobmanager.memory.process.size: 2gb
taskmanager.memory.process.size: 8gb
taskmanager.numberOfTaskSlots: 4
parallelism.default: 4
```

**Serverless 部署 (2.5)**:

```yaml
# flink-conf.yaml (2.5)
execution.mode: serverless

# 资源配置改为范围
kubernetes.operator.job.autoscaler:
  enabled: true
  min-parallelism: 1
  max-parallelism: 100

# TaskManager 资源配置
taskmanager.memory.process.size: 4gb
taskmanager.numberOfTaskSlots: 2

# Serverless 特定配置
serverless.cold-start.mode: warmup-pool
serverless.cold-start.warmup-pool-size: 2
```

### 6.2 Kubernetes 部署更新

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
    # Serverless 配置 (新增)
    serverless:
      enabled: true
      scale-to-zero:
        enabled: true
        idle-timeout: 10m
```

---

## 7. 常见问题

### 7.1 启动失败

**问题**: 作业启动时报告配置错误

```
Caused by: IllegalArgumentException: Unknown configuration key: state.backend.rocksdb.memory.managed
```

**解决**: 更新配置键名

```yaml
# 旧配置
state.backend.rocksdb.memory.managed: true

# 新配置
state.backend.forst.memory.managed: true
```

### 7.2 性能下降

**问题**: 迁移后作业吞吐量下降

**排查步骤**:

1. 检查状态后端配置是否正确
2. 验证 Checkpoint 配置
3. 对比 GC 日志
4. 检查网络缓冲区配置

**解决**:

```yaml
# 调优网络缓冲区
taskmanager.memory.network.min: 256mb
taskmanager.memory.network.max: 512mb

# 调优 Checkpoint
execution.checkpointing.interval: 30s
execution.checkpointing.max-concurrent-checkpoints: 1
```

### 7.3 Serverless 冷启动慢

**问题**: Scale-from-Zero 后恢复慢

**解决**:

```yaml
# 启用预热池
serverless.cold-start.mode: warmup-pool
serverless.cold-start.warmup-pool-size: 2

# 优化状态恢复
state.backend.forst.incremental-recovery: true
state.backend.forst.restore.parallelism: 10
```

---

## 8. 回滚方案

### 8.1 回滚到 2.4

```bash
# 1. 创建 2.5 作业的 Savepoint
flink savepoint <2.5-job-id> s3://flink-savepoints/rollback

# 2. 使用 2.4 镜像重新部署
flink run \
    -Dstate.backend=rocksdb \
    -s s3://flink-savepoints/rollback/savepoint-xxxxx \
    ./my-job-2.4.jar
```

**注意**:

- 2.5 新增特性 (如 Serverless) 在回滚后将不可用
- 确保 2.4 配置与 2.5 兼容

---

## 9. 最佳实践

### 9.1 迁移策略

```
建议迁移流程:

Week 1: 开发环境验证
  - 更新依赖和配置
  - 功能测试
  - 性能基准测试

Week 2: 预发布环境验证
  - 集成测试
  - 长时间稳定性测试
  - Checkpoint/恢复测试

Week 3: 生产灰度发布
  - 5% 流量验证
  - 监控指标对比
  - 逐步扩大流量

Week 4: 全量迁移
  - 100% 流量切换
  - 保留 2.4 回滚能力
  - 监控和优化
```

### 9.2 配置模板

```yaml
# flink-conf.yaml - Flink 2.5 推荐配置模板

# 执行模式
execution.mode: adaptive
execution.runtime-mode: streaming

# 状态后端 (推荐 ForSt)
state.backend: forst
state.backend.forst.remote.path: s3://flink-state/{job-id}
state.backend.forst.cache.capacity: 10GB

# Checkpoint
execution.checkpointing.interval: 30s
execution.checkpointing.mode: EXACTLY_ONCE
state.checkpoint-storage: filesystem
state.checkpoints.dir: s3://flink-checkpoints/{job-id}

# Serverless (可选)
kubernetes.operator.job.autoscaler.enabled: true
kubernetes.operator.job.autoscaler.scale-to-zero.enabled: false  # 谨慎启用

# 网络
taskmanager.memory.network.min: 256mb
taskmanager.memory.network.max: 512mb

# 重启策略
restart-strategy: fixed-delay
restart-strategy.fixed-delay.attempts: 10
restart-strategy.fixed-delay.delay: 10s
```

---

*最后更新: 2026-04-08*
