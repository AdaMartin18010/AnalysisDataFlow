# 算子最佳实践速查表

> **所属阶段**: Knowledge/07-best-practices | **前置依赖**: 全部v7.1算子体系文档 | **形式化等级**: L2
> **文档定位**: 流处理算子选型、配置、调优、排障的快速参考手册
> **版本**: 2026.04

---

## 目录

- [算子最佳实践速查表](#算子最佳实践速查表)
  - [目录](#目录)
  - [1. 算子选型速查](#1-算子选型速查)
    - [1.1 按业务场景选型](#11-按业务场景选型)
    - [1.2 按数据特征选型](#12-按数据特征选型)
  - [2. 参数配置速查](#2-参数配置速查)
    - [2.1 全局配置](#21-全局配置)
    - [2.2 算子级配置](#22-算子级配置)
  - [3. 性能调优速查](#3-性能调优速查)
    - [3.1 延迟优化检查清单](#31-延迟优化检查清单)
    - [3.2 吞吐优化检查清单](#32-吞吐优化检查清单)
    - [3.3 资源优化检查清单](#33-资源优化检查清单)
  - [4. 故障排查速查](#4-故障排查速查)
    - [4.1 异常速查](#41-异常速查)
    - [4.2 Metrics关键阈值](#42-metrics关键阈值)
  - [5. 代码模板速查](#5-代码模板速查)
    - [5.1 标准ProcessFunction模板](#51-标准processfunction模板)
    - [5.2 AsyncFunction模板](#52-asyncfunction模板)
    - [5.3 两阶段聚合（防倾斜）模板](#53-两阶段聚合防倾斜模板)
    - [5.4 Side Output异常处理模板](#54-side-output异常处理模板)
  - [6. 安全检查清单](#6-安全检查清单)
    - [6.1 发布前检查清单](#61-发布前检查清单)
    - [6.2 运行时监控检查清单](#62-运行时监控检查清单)

---

## 1. 算子选型速查

### 1.1 按业务场景选型

| 业务需求 | 推荐算子 | 避免 | 关键参数 |
|---------|---------|------|---------|
| 数据清洗/转换 | `map` / `filter` / `flatMap` | `ProcessFunction`（过度） | 无 |
| 按Key分组统计 | `keyBy` + `reduce` / `aggregate` | `windowAll` | `TTL`, `stateBackend` |
| 时间窗口聚合 | `window` + `aggregate` | 全局`process`模拟窗口 | `size`, `slide`, `allowedLateness` |
| 双流关联 | `intervalJoin` / `coGroup` | `join`（仅支持Tumbling） | `lowerBound`, `upperBound` |
| 异步IO | `AsyncFunction` | `map`中同步调用 | `timeout`, `capacity` |
| 复杂事件识别 | `CEP` | 手写`ProcessFunction` | `within`, `next/followedBy` |
| 规则动态更新 | `BroadcastStream` + `connect` | 硬编码规则 | `MapStateDescriptor` |
| 数据分流 | `SideOutput` | 多个`filter`重复处理 | `OutputTag` |
| 顺序保证 | `keyBy`后单分区处理 | 全局排序 | `parallelism=1`（仅排序阶段） |
| 延迟数据处理 | `allowedLateness` + `sideOutput` | 丢弃所有延迟数据 | `allowedLateness`, `sideOutputTag` |

### 1.2 按数据特征选型

| 数据特征 | 推荐模式 | 算子组合 |
|---------|---------|---------|
| 高吞吐（>100万/s） | 无状态 + 预聚合 | `filter` → `map` → `keyBy` → `reduce` |
| 高延迟容忍（>1分钟） | 大窗口批处理 | `window`（小时级）→ `aggregate` |
| 严格低延迟（<100ms） | 逐事件处理 | `process` / `AsyncFunction` |
| 数据倾斜严重 | 加盐 + 两阶段聚合 | `map`（加盐）→ `keyBy` → `reduce` → `keyBy`（去盐）→ `reduce` |
| 乱序严重 | 事件时间 + 水位线 | `assignTimestamps` → `watermark` → `window` |
| 状态极大（>10GB） | RocksDB + 增量Checkpoint | `keyBy` + `RocksDBStateBackend` |
|  exactly-once要求 | 事务Sink | `TwoPhaseCommitSinkFunction` |

---

## 2. 参数配置速查

### 2.1 全局配置

```properties
# Checkpoint配置
execution.checkpointing.interval=30s
execution.checkpointing.min-pause-between-checkpoints=30s
execution.checkpointing.timeout=10min
execution.checkpointing.max-concurrent-checkpoints=1
state.backend=rocksdb
state.backend.incremental=true
state.checkpoints.dir=s3://bucket/checkpoints

# 网络配置
taskmanager.memory.network.fraction=0.15
taskmanager.memory.network.min=128mb
taskmanager.memory.network.max=256mb

# 状态配置
state.backend.rocksdb.memory.managed=true
state.backend.rocksdb.predefined-options=SPINNING_DISK_OPTIMIZED_HIGH_MEM
```

### 2.2 算子级配置

| 算子 | 关键参数 | 推荐值 | 说明 |
|------|---------|--------|------|
| **Kafka Source** | `fetch.min.bytes` | 1-10KB | 减少空轮询 |
| | `max.poll.records` | 500-2000 | 平衡延迟与吞吐 |
| | `consumer.auto.offset.reset` | `latest`/`earliest` | 根据业务选择 |
| **AsyncFunction** | `timeout` | p99延迟 × 1.5 | 覆盖绝大多数请求 |
| | `capacity` | ⌈p99/p50⌉ × P | P为并行度 |
| **Window** | `allowedLateness` | 最大乱序时间 | 通常5秒-5分钟 |
| | `sideOutputLateData` | 必须配置 | 延迟数据不丢失 |
| **Join** | `lowerBound` | -窗口大小 | 左流等待右流 |
| | `upperBound` | +窗口大小 | 右流等待左流 |
| **Timer** | 清理旧Timer | 必须实现 | 避免Timer泄漏 |
| **State TTL** | `updateType` | `OnCreateAndWrite` | 每次更新刷新TTL |
| | `stateVisibility` | `NeverReturnExpired` | 不返回过期状态 |

---

## 3. 性能调优速查

### 3.1 延迟优化检查清单

- [ ] Source并行度 = Kafka分区数（避免空跑Task）
- [ ] 网络缓冲区足够（`taskmanager.memory.network.fraction ≥ 0.1`）
- [ ] 序列化器优化（优先使用Avro/Protobuf，避免Kryo泛型）
- [ ] 异步IO替代同步IO（AsyncFunction vs map中的HTTP调用）
- [ ] 状态访问本地化（RocksDB block cache调优）
- [ ] GC优化（G1GC，-XX:MaxGCPauseMillis=100）
- [ ] 对象复用（在ProcessFunction中复用输出对象）

### 3.2 吞吐优化检查清单

- [ ] 背压定位（找到瓶颈算子，而非盲目扩容）
- [ ] 数据倾斜检测（SkewIndex > 5 需处理）
- [ ] 小文件管理（湖仓Sink定期compaction）
- [ ] Batch写入（Sink端批量提交，减少IO次数）
- [ ] 压缩算法选择（LZ4/Snappy平衡CPU与压缩率）
- [ ] 并行度合理（CPU利用率60-70%为最佳）
- [ ] 分区策略优化（避免跨网络shuffle）

### 3.3 资源优化检查清单

- [ ] 预留实例（7×24作业用Reserved Instances节省30-55%）
- [ ] 状态TTL（防止状态无限增长）
- [ ] 自动扩缩容（峰谷明显场景）
- [ ] Spot实例（无状态Task可用Spot节省60-80%）
- [ ] 内存与磁盘权衡（状态>1GB必须用RocksDB）
- [ ] Checkpoint间隔权衡（30秒-1分钟为最佳平衡点）

---

## 4. 故障排查速查

### 4.1 异常速查

| 异常/症状 | 快速诊断 | 快速修复 |
|----------|---------|---------|
| `NullPointerException` | 检查输入数据空值 | 前置filter或Optional处理 |
| `OutOfMemoryError` | 检查stateSize和Timer数量 | 启用TTL或减少窗口 |
| `Checkpoint expired` | 检查checkpointDuration | 增大timeout或优化状态 |
| `BackPressure` | 定位背压源算子 | 扩容或优化瓶颈算子 |
| `Watermarks lagging` | 检查Source Lag | 增加Source并行度或调整Watermark |
| `Connection refused` | 检查外部服务健康 | 添加重试和熔断 |
| `ClassCastException` | 检查TypeInformation | 显式指定类型或序列化器 |
| `Too many open files` | 检查文件句柄限制 | ulimit -n 65536 |

### 4.2 Metrics关键阈值

| 指标 | 正常范围 | 警告阈值 | 严重阈值 |
|------|---------|---------|---------|
| CPU利用率 | 40-70% | >80% | >95% |
| 内存利用率 | 50-70% | >80% | >95% |
| GC时间占比 | <5% | >10% | >30% |
| 背压比 | <0.1 | >0.5 | >0.8 |
| Checkpoint持续时间 | <30s | >60s | >超时 |
| Source Lag | <1000 | >10000 | >100000 |
| Watermark滞后 | <事件时间窗口 | >2×窗口大小 | >10×窗口大小 |
| 状态大小 | <1GB/并行度 | >5GB/并行度 | >10GB/并行度 |

---

## 5. 代码模板速查

### 5.1 标准ProcessFunction模板

```java
public class SafeProcessFunction extends KeyedProcessFunction<String, Event, Result> {
    private ValueState<StateData> state;
    private ValueState<Long> timerState;

    @Override
    public void open(Configuration parameters) {
        StateTtlConfig ttl = StateTtlConfig
            .newBuilder(Time.hours(24))
            .setUpdateType(OnCreateAndWrite)
            .setStateVisibility(NeverReturnExpired)
            .build();
        ValueStateDescriptor<StateData> descriptor =
            new ValueStateDescriptor<>("state", StateData.class);
        descriptor.enableTimeToLive(ttl);
        state = getRuntimeContext().getState(descriptor);

        ValueStateDescriptor<Long> timerDescriptor =
            new ValueStateDescriptor<>("timer", Types.LONG);
        timerState = getRuntimeContext().getState(timerDescriptor);
    }

    @Override
    public void processElement(Event event, Context ctx, Collector<Result> out) {
        // 1. 清理旧Timer
        Long oldTimer = timerState.value();
        if (oldTimer != null) {
            ctx.timerService().deleteEventTimeTimer(oldTimer);
        }

        // 2. 处理逻辑
        StateData current = state.value();
        if (current == null) current = new StateData();
        current.update(event);
        state.update(current);

        // 3. 注册新Timer
        long newTimer = ctx.timestamp() + Time.minutes(5).toMilliseconds();
        ctx.timerService().registerEventTimeTimer(newTimer);
        timerState.update(newTimer);

        // 4. 输出
        out.collect(current.toResult());
    }

    @Override
    public void onTimer(long timestamp, OnTimerContext ctx, Collector<Result> out) {
        // 清理状态
        timerState.clear();
        StateData current = state.value();
        if (current != null && current.isExpired(timestamp)) {
            state.clear();
        }
    }
}
```

### 5.2 AsyncFunction模板

```java
public class SafeAsyncFunction extends AsyncFunction<Event, EnrichedEvent> {
    private transient AsyncHttpClient client;

    @Override
    public void open(Configuration parameters) {
        client = AsyncHttpClient.builder()
            .setRequestTimeout(Duration.ofMillis(100))
            .setMaxConnections(100)
            .build();
    }

    @Override
    public void asyncInvoke(Event event, ResultFuture<EnrichedEvent> resultFuture) {
        client.call(event.getId())
            .whenComplete((result, exception) -> {
                if (exception != null) {
                    resultFuture.completeExceptionally(exception);
                } else {
                    resultFuture.complete(Collections.singletonList(
                        new EnrichedEvent(event, result)
                    ));
                }
            });
    }

    @Override
    public void timeout(Event event, ResultFuture<EnrichedEvent> resultFuture) {
        resultFuture.complete(Collections.singletonList(
            new EnrichedEvent(event, null)  // 降级处理
        ));
    }
}
```

### 5.3 两阶段聚合（防倾斜）模板

```java
// Step 1: 加盐预聚合
stream.map(event -> {
    event.setSaltedKey(event.getKey() + "_" + ThreadLocalRandom.current().nextInt(10));
    return event;
})
.keyBy(Event::getSaltedKey)
.aggregate(new PartialAggregate())
// Step 2: 去盐最终聚合
.map(result -> {
    result.setKey(result.getSaltedKey().split("_")[0]);
    return result;
})
.keyBy(Result::getKey)
.aggregate(new FinalAggregate());
```

### 5.4 Side Output异常处理模板

```java
OutputTag<Event> lateTag = new OutputTag<Event>("late"){};
OutputTag<Event> errorTag = new OutputTag<Event>("error"){};

SingleOutputStreamOperator<Result> main = stream
    .keyBy(Event::getKey)
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .allowedLateness(Time.seconds(30))
    .sideOutputLateData(lateTag)
    .process(new SafeWindowFunction(errorTag));

// 处理延迟数据
main.getSideOutput(lateTag).addSink(new LateDataSink());
// 处理异常数据
main.getSideOutput(errorTag).addSink(new ErrorDataSink());
```

---

## 6. 安全检查清单

### 6.1 发布前检查清单

- [ ] 算子UID是否稳定？（Savepoint兼容性）
- [ ] 状态类型是否变更？（Schema兼容性）
- [ ] keyBy键分布是否均匀？（数据倾斜）
- [ ] 所有状态是否配置了TTL？（防OOM）
- [ ] Timer是否清理？（防泄漏）
- [ ] 外部调用是否有超时？（防阻塞）
- [ ] Sink是否幂等或事务性？（防重复）
- [ ] 敏感数据是否脱敏？（隐私合规）
- [ ] 并行度是否合理？（Source ≤ Kafka分区数）
- [ ] Checkpoint是否通过？（恢复能力）

### 6.2 运行时监控检查清单

- [ ] 背压比 < 0.5？
- [ ] CPU利用率 40-70%？
- [ ] GC时间 < 5%？
- [ ] Checkpoint持续时间 < 60秒？
- [ ] Source Lag < 10000？
- [ ] 状态大小增长趋势平稳？
- [ ] 无异常日志洪水？
- [ ] Watermark正常推进？

---

*关联文档*: [operator-best-practices-quick-reference.md] 汇总了v7.1算子体系全部26篇文档的核心要点。详细内容请参阅各专题文档。
