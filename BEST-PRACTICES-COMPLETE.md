# 流处理完全最佳实践

> **Complete Best Practices for Stream Processing**

## 1. 设计最佳实践

### 状态管理

- **推荐**: 使用RocksDB状态后端处理大状态
- **避免**: 在Heap状态后端存储大量数据
- **原因**: Heap受限于JVM内存，RocksDB可使用磁盘

### 时间语义

- **事件时间**: 用于需要准确时间顺序的场景
- **处理时间**: 用于低延迟要求的场景
- **摄取时间**: 简单场景，不推荐生产使用

### 并行度设置

```
推荐公式: 并行度 = max(可用CPU核心数, Kafka分区数)
```

## 2. 开发最佳实践

### 算子链优化

```java
// 允许算子链（默认）
env.disableOperatorChaining(); // 仅调试时使用

// 自定义算子链
stream.map(...).startNewChain().filter(...);
```

### 序列化优化

- 使用Avro或Protobuf替代JSON
- 启用Kryo序列化
- 自定义TypeInformation

### 资源管理

```java
// 配置网络缓冲区
env.getConfig().setAutoWatermarkInterval(200);

// 配置Checkpoint超时
env.getCheckpointConfig().setCheckpointTimeout(600000);
```

## 3. 运维最佳实践

### 监控指标

| 指标 | 告警阈值 | 说明 |
|------|----------|------|
| 延迟 | > 5s | 数据处理延迟 |
| 吞吐量 | 下降30% | 每秒处理记录数 |
| Checkpoint时间 | > 60s | Checkpoint耗时 |
| 失败率 | > 1% | 任务失败频率 |

### 故障恢复

```bash
# 从Checkpoint恢复
./bin/flink run -s checkpoint_path job.jar

# 手动触发Savepoint
./bin/flink savepoint job_id
```

## 4. 安全最佳实践

### 认证授权

- 启用Kerberos认证
- 配置RBAC权限
- 敏感数据加密

### 网络安全

- 启用SSL/TLS
- 配置防火墙规则
- 限制访问IP

---

*Best Practices Complete - Phase 2*
