# 流处理反模式快速参考卡片

> **快速查阅**: 10大常见反模式的症状、原因与解决方案
>
> **完整文档**: [streaming-anti-patterns.md](../09-anti-patterns/anti-pattern-checklist.md)

---

## 🚨 严重程度分级参考

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      严重程度金字塔                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  P0 - 灾难性 ▲                                                          │
│            /██\    系统级联故障、数据丢失、服务中断                       │
│           /████\   AP-02 忽略背压信号                                    │
│          /██████\  AP-10 监控不足                                        │
│         ▔▔▔▔▔▔▔▔▔                                                │
│                                                                         │
│  P1 - 高危   ▲                                                          │
│            /██\    性能严重退化、OOM、恢复失败                           │
│           /████\   AP-03 状态无TTL      AP-05 数据倾斜                   │
│          /██████\  AP-06 全局窗口滥用   AP-07 忽略迟到数据               │
│         /████████\ AP-04 错误Checkpoint配置                              │
│        ▔▔▔▔▔▔▔▔▔▔▔                                             │
│                                                                         │
│  P2 - 中等   ▲                                                          │
│            /██\    结果不准确、资源浪费、偶发错误                        │
│           /████\   AP-01 过度依赖处理时间   AP-08 并行度不当             │
│          /██████\  AP-09 缺乏幂等性                                      │
│         ▔▔▔▔▔▔▔▔▔                                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 10大反模式速查表

### AP-01: 过度依赖处理时间 (P2)

| 项目 | 内容 |
|------|------|
| **症状** | 相同数据多次运行结果不同；窗口归属错误；乱序敏感 |
| **根本原因** | 使用 `ProcessingTime` 而非 `EventTime` 作为时间基准 |
| **解决方案** | 使用 `EventTime` + `WatermarkStrategy` + `allowedLateness` |

```scala
// ❌ 错误
.window(TumblingProcessingTimeWindows.of(Time.minutes(5)))

// ✅ 正确
.assignTimestampsAndWatermarks(
  WatermarkStrategy.forBoundedOutOfOrderness(Duration.ofSeconds(30))
)
.window(TumblingEventTimeWindows.of(Time.minutes(5)))
.allowedLateness(Time.minutes(2))
.sideOutputLateData(lateDataTag)
```

---

### AP-02: 忽略背压信号 (P0) ⚠️

| 项目 | 内容 |
|------|------|
| **症状** | Checkpoint超时；OOM；Kafka Lag持续增长；数据丢失 |
| **根本原因** | 无视Flink背压信号，继续增加输入负载 |
| **解决方案** | 监控背压指标；自动扩缩容；Source限流 |

```scala
// ✅ 监控指标
// backPressuredTimeMsPerSecond > 0 表示存在背压

// ✅ 自动扩缩容 (Flink Kubernetes Operator)
spec:
  autoScaler:
    enabled: true
    targetUtilization: 0.7

// ✅ Source限流
kafkaSource.setProperty("max.poll.records", "500")
```

---

### AP-03: 状态无限增长无TTL (P1)

| 项目 | 内容 |
|------|------|
| **症状** | 状态持续增长；Checkpoint时间增长；最终OOM |
| **根本原因** | 未为状态配置 `StateTtlConfig` |
| **解决方案** | 配置TTL + 清理策略 |

```scala
// ✅ 配置TTL
val ttlConfig = StateTtlConfig
  .newBuilder(Time.minutes(30))
  .setUpdateType(OnCreateAndWrite)
  .setStateVisibility(NeverReturnExpired)
  .cleanupFullSnapshot()
  .build()

descriptor.enableTimeToLive(ttlConfig)
```

**TTL推荐值**:

| 状态类型 | 推荐TTL |
|----------|---------|
| 用户会话 | 30分钟无活动 |
| 去重状态 | 24小时 |
| 临时计算 | 1小时 |
| 聚合缓存 | 窗口大小+宽限期 |

---

### AP-04: 错误的Checkpoint配置 (P1)

| 项目 | 内容 |
|------|------|
| **症状** | Checkpoint频繁失败；恢复时间过长；状态损坏 |
| **根本原因** | 间隔/超时/存储配置不合理 |
| **解决方案** | 根据恢复SLA配置参数 |

```scala
// ✅ 推荐配置
env.enableCheckpointing(120000)  // 2分钟间隔
env.getCheckpointConfig.setCheckpointTimeout(600000)  // 10分钟超时
env.setStateBackend(new EmbeddedRocksDBStateBackend(true))  // 增量Checkpoint
env.getCheckpointConfig.setCheckpointStorage("hdfs:///flink-checkpoints")
```

**配置决策表**:

| 场景 | 推荐间隔 | 推荐超时 | 增量 |
|------|----------|----------|------|
| 小状态 (<100MB) | 30s-1min | 2min | 可选 |
| 中状态 (100MB-10GB) | 1-2min | 5min | 建议 |
| 大状态 (>10GB) | 3-5min | 10min+ | 必须 |
| 金融交易 | 10-30s | 1min | 建议 |

---

### AP-05: 数据倾斜未处理 (P1)

| 项目 | 内容 |
|------|------|
| **症状** | 部分Task负载95%+，其他Task空闲；整体吞吐量下降 |
| **根本原因** | Key分布不均，热点Key导致 |
| **解决方案** | 两阶段聚合；自定义分区器；本地缓存 |

```scala
// ✅ 两阶段聚合
.map(txn => (s"${txn.merchantId}_${Random.nextInt(10)}", txn.amount))  // 加随机前缀
.keyBy(_._1).window(TumblingEventTimeWindows.of(Time.seconds(10)))
.aggregate(new PreAggregate())  // 第一阶段局部聚合

.map { case (key, amount) => (key.split("_")(0), amount) }  // 去掉前缀
.keyBy(_._1).window(TumblingEventTimeWindows.of(Time.minutes(1)))
.aggregate(new FinalAggregate())  // 第二阶段全局聚合
```

---

### AP-06: 滥用全局窗口 (P1)

| 项目 | 内容 |
|------|------|
| **症状** | 状态持续增长；无输出或延迟不可控 |
| **根本原因** | 使用 `GlobalWindows` 但未配置触发器和清理策略 |
| **解决方案** | 配置明确的触发器和Evictor |

```scala
// ❌ 错误
.window(GlobalWindows.create())  // 永不关闭！
.aggregate(new CountAggregate())

// ✅ 正确
.window(GlobalWindows.create())
.trigger(CountTrigger.of(1000))  // 每1000条触发
.evictor(CountEvictor.of(1000))  // 触发后清理
.aggregate(new CountAggregate())
```

---

### AP-07: 忽略迟到数据 (P1)

| 项目 | 内容 |
|------|------|
| **症状** | 统计数据比实际少；数据丢失无法审计 |
| **根本原因** | 未配置 `allowedLateness` 和 `sideOutputLateData` |
| **解决方案** | 完整迟到数据处理机制 |

```scala
// ✅ 完整配置
val lateDataTag = OutputTag[Event]("late-data")

val result = stream
  .assignTimestampsAndWatermarks(
    WatermarkStrategy.forBoundedOutOfOrderness[Event](Duration.ofSeconds(10))
  )
  .keyBy(_.userId)
  .window(TumblingEventTimeWindows.of(Time.minutes(5)))
  .allowedLateness(Time.minutes(2))       // ✅ 允许2分钟延迟
  .sideOutputLateData(lateDataTag)        // ✅ 完全迟到的数据侧输出
  .aggregate(new CountAggregate())

// 处理完全迟到的数据
val lateData = result.getSideOutput(lateDataTag)
lateData.addSink(new LateDataAuditSink())  // 审计或离线补录
```

---

### AP-08: 不恰当的并行度设置 (P2)

| 项目 | 内容 |
|------|------|
| **症状** | 资源浪费或处理能力不足；某些算子成为瓶颈 |
| **根本原因** | 并行度与数据量/资源不匹配 |
| **解决方案** | 根据场景设置并行度 |

```scala
// ✅ 推荐配置
kafkaSource.setParallelism(10)  // = Kafka分区数

stream
  .map(parseJson).setParallelism(10)  // 轻量转换
  .keyBy(_.userId)
  .window(TumblingEventTimeWindows.of(Time.minutes(1)))
  .aggregate(complexAggregation).setParallelism(20)  // 重计算
  .addSink(elasticsearchSink).setParallelism(5)  // 根据下游能力
```

---

### AP-09: 缺乏幂等性考虑 (P2)

| 项目 | 内容 |
|------|------|
| **症状** | 故障恢复后数据重复；统计结果错误 |
| **根本原因** | Sink未实现幂等写入 |
| **解决方案** | UPSERT语义；两阶段提交 (2PC)；唯一键约束 |

```scala
// ✅ 幂等写入 (UPSERT)
val stmt = connection.prepareStatement(
  """INSERT INTO results (id, value, checkpoint_id)
     VALUES (?, ?, ?)
     ON CONFLICT (id) DO UPDATE SET
     value = EXCLUDED.value,
     checkpoint_id = EXCLUDED.checkpoint_id
     WHERE results.checkpoint_id < EXCLUDED.checkpoint_id
  """.stripMargin
)
stmt.setLong(3, context.getCurrentCheckpointId)  // 携带Checkpoint ID

// ✅ 或实现TwoPhaseCommitSinkFunction
class TwoPhaseCommitKafkaSink extends TwoPhaseCommitSinkFunction[...] { ... }
```

---

### AP-10: 监控和可观测性不足 (P0) ⚠️

| 项目 | 内容 |
|------|------|
| **症状** | 故障发现延迟；定位困难；无法预判问题 |
| **根本原因** | 缺乏关键指标监控和告警 |
| **解决方案** | 完整监控体系；关键指标告警；链路追踪 |

**必须监控的指标**:

| 类别 | 关键指标 | 告警阈值 |
|------|----------|----------|
| **延迟** | 端到端延迟 (p50/p99) | p99 > SLA |
| **吞吐** | recordsInPerSecond | 低于预期 |
| **背压** | backPressuredTimeMsPerSecond | > 0 |
| **Checkpoint** | checkpointDuration | > 超时80% |
| **状态** | stateSize | 增长过快 |
| **Kafka** | records-lag-max | > 阈值 |

---

## 🔍 反模式关联图

```
┌─────────────────────────────────────────────────────────────────┐
│                      反模式因果关系                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  AP-02 忽略背压 ────► AP-04 Checkpoint超时 ────► 恢复失败      │
│       │                                             │           │
│       ▼                                             ▼           │
│  AP-10 监控不足 ◄───────────────────────────── 数据丢失        │
│       ▲                                             ▲           │
│       │                                             │           │
│  AP-05 数据倾斜 ────► 处理能力下降 ────► 背压加剧              │
│       │                                                         │
│       └──► 热点Task OOM ◄──── AP-03 状态无限增长               │
│                                                                 │
│  AP-01 处理时间 ────► AP-07 迟到数据 ────► 结果不准确          │
│       │                                                         │
│       └──► 窗口归属错误 ◄──── AP-06 全局窗口滥用               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 延伸阅读

| 反模式 | 完整文档 |
|--------|----------|
| AP-01 | [anti-pattern-02-watermark-misconfiguration.md](../09-anti-patterns/anti-pattern-02-watermark-misconfiguration.md) |
| AP-02 | [anti-pattern-08-ignoring-backpressure.md](../09-anti-patterns/anti-pattern-08-ignoring-backpressure.md) |
| AP-03 | [anti-pattern-01-global-state-abuse.md](../09-anti-patterns/anti-pattern-01-global-state-abuse.md) |
| AP-04 | [anti-pattern-03-checkpoint-interval-misconfig.md](../09-anti-patterns/anti-pattern-03-checkpoint-interval-misconfig.md) |
| AP-05 | [anti-pattern-04-hot-key-skew.md](../09-anti-patterns/anti-pattern-04-hot-key-skew.md) |
| AP-06 | [anti-pattern-07-window-state-explosion.md](../09-anti-patterns/anti-pattern-07-window-state-explosion.md) |
| AP-09 | [anti-pattern-05-blocking-io-processfunction.md](../09-anti-patterns/anti-pattern-05-blocking-io-processfunction.md) |
| AP-10 | [anti-pattern-10-resource-estimation-oom.md](../09-anti-patterns/anti-pattern-10-resource-estimation-oom.md) |
| 综合 | [streaming-anti-patterns.md](../09-anti-patterns/anti-pattern-checklist.md) |

---

*快速参考卡片 v1.0 | 最后更新: 2026-04-03*
