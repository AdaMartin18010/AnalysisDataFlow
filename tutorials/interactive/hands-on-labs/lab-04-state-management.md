# Lab 4: 状态管理

> 所属阶段: Flink/Hands-on | 前置依赖: [Lab 3](./lab-03-window-aggregation.md) | 预计时间: 90分钟 | 形式化等级: L4

## 实验目标

- [x] 理解 Flink 状态类型：ValueState、ListState、MapState、ReducingState
- [x] 掌握状态的生命周期管理
- [x] 学会使用 State TTL 配置
- [x] 理解 Keyed State 和 Operator State 的区别

## 前置知识

- Lab 3 的窗口操作
- 键值对数据处理基础
- 状态后端概念

## 状态类型概览

| 状态类型 | 适用场景 | 特点 |
|---------|---------|------|
| ValueState | 单值状态（计数器、最新值） | 每个key一个值 |
| ListState | 列表状态（事件历史） | 支持添加、获取列表 |
| MapState | 映射状态（键值对集合） | 类似HashMap |
| ReducingState | 归约状态（聚合） | 自动应用归约函数 |
| AggregatingState | 聚合状态 | 支持复杂聚合逻辑 |

## 实验步骤

### 步骤 1: ValueState 示例 - 检测温度异常

```java
package com.example;

import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.api.common.time.Time;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.util.Collector;

public class TemperatureAlertFunction extends
    KeyedProcessFunction<String, SensorReading, Alert> {

    // 状态声明
    private ValueState<Double> lastTemperatureState;
    private ValueState<Long> lastAlertTimeState;

    @Override
    public void open(Configuration parameters) {
        // 状态描述符
        ValueStateDescriptor<Double> tempDescriptor =
            new ValueStateDescriptor<>("lastTemperature", Double.class);

        ValueStateDescriptor<Long> alertDescriptor =
            new ValueStateDescriptor<>("lastAlertTime", Long.class);

        // 获取状态
        lastTemperatureState = getRuntimeContext().getState(tempDescriptor);
        lastAlertTimeState = getRuntimeContext().getState(alertDescriptor);
    }

    @Override
    public void processElement(
            SensorReading reading,
            Context ctx,
            Collector<Alert> out) throws Exception {

        Double lastTemp = lastTemperatureState.value();
        Long lastAlertTime = lastAlertTimeState.value();

        // 检测温度跳变
        if (lastTemp != null) {
            double diff = Math.abs(reading.temperature - lastTemp);

            if (diff > 10.0) {
                // 检查是否已经发送过告警（10秒内只发送一次）
                long currentTime = ctx.timestamp();
                if (lastAlertTime == null ||
                    (currentTime - lastAlertTime) > 10000) {

                    out.collect(new Alert(
                        reading.sensorId,
                        "TEMPERATURE_SPIKE",
                        String.format("Temperature changed from %.1f to %.1f",
                            lastTemp, reading.temperature),
                        currentTime
                    ));

                    lastAlertTimeState.update(currentTime);
                }
            }
        }

        // 更新状态
        lastTemperatureState.update(reading.temperature);
    }
}
```

### 步骤 2: ListState 示例 - 会话事件收集

```java
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;

import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;


public class SessionEventCollector extends
    KeyedProcessFunction<String, UserEvent, SessionSummary> {

    // ListState 存储会话中的所有事件
    private ListState<UserEvent> sessionEventsState;
    private ValueState<Long> sessionStartTimeState;

    @Override
    public void open(Configuration parameters) {
        sessionEventsState = getRuntimeContext().getListState(
            new ListStateDescriptor<>("sessionEvents", UserEvent.class)
        );
        sessionStartTimeState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("sessionStart", Long.class)
        );
    }

    @Override
    public void processElement(
            UserEvent event,
            Context ctx,
            Collector<SessionSummary> out) throws Exception {

        // 添加事件到列表
        sessionEventsState.add(event);

        // 初始化会话开始时间
        if (sessionStartTimeState.value() == null) {
            sessionStartTimeState.update(event.timestamp);

            // 注册5分钟后检查会话超时的定时器
            ctx.timerService().registerEventTimeTimer(
                event.timestamp + 300000  // 5分钟
            );
        }
    }

    @Override
    public void onTimer(
            long timestamp,
            OnTimerContext ctx,
            Collector<SessionSummary> out) throws Exception {

        // 会话结束，生成摘要
        List<UserEvent> events = new ArrayList<>();
        sessionEventsState.get().forEach(events::add);

        SessionSummary summary = new SessionSummary();
        summary.userId = ctx.getCurrentKey();
        summary.eventCount = events.size();
        summary.sessionDuration = timestamp - sessionStartTimeState.value();
        summary.events = events;

        out.collect(summary);

        // 清空状态
        sessionEventsState.clear();
        sessionStartTimeState.clear();
    }
}
```

### 步骤 3: MapState 示例 - 用户行为计数

```java
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;

public class UserBehaviorCounter extends
    KeyedProcessFunction<String, UserEvent, BehaviorReport> {

    // MapState: 行为类型 -> 计数
    private MapState<String, Long> behaviorCountState;

    @Override
    public void open(Configuration parameters) {
        behaviorCountState = getRuntimeContext().getMapState(
            new MapStateDescriptor<>("behaviorCounts", String.class, Long.class)
        );
    }

    @Override
    public void processElement(
            UserEvent event,
            Context ctx,
            Collector<BehaviorReport> out) throws Exception {

        String behavior = event.eventType;

        // 获取当前计数，不存在则为0
        Long currentCount = behaviorCountState.get(behavior);
        if (currentCount == null) {
            currentCount = 0L;
        }

        // 更新计数
        behaviorCountState.put(behavior, currentCount + 1);

        // 每100个事件输出一次报告
        long totalCount = 0;
        for (Long count : behaviorCountState.values()) {
            totalCount += count;
        }

        if (totalCount % 100 == 0) {
            BehaviorReport report = new BehaviorReport();
            report.userId = ctx.getCurrentKey();
            report.behaviorCounts = new HashMap<>();
            behaviorCountState.entries().forEach(entry ->
                report.behaviorCounts.put(entry.getKey(), entry.getValue())
            );
            out.collect(report);
        }
    }
}
```

### 步骤 4: ReducingState 示例 - 实时平均值

```java
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;

public class RunningAverageFunction extends
    KeyedProcessFunction<String, SensorReading, AverageResult> {

    // ReducingState: 自动应用归约函数
    private ReducingState<CountSum> countSumState;

    @Override
    public void open(Configuration parameters) {
        countSumState = getRuntimeContext().getReducingState(
            new ReducingStateDescriptor<>("countSum",
                (a, b) -> new CountSum(a.count + b.count, a.sum + b.sum),
                CountSum.class)
        );
    }

    @Override
    public void processElement(
            SensorReading reading,
            Context ctx,
            Collector<AverageResult> out) throws Exception {

        // 添加新值（自动归约）
        countSumState.add(new CountSum(1, reading.temperature));

        // 计算并输出平均值
        CountSum current = countSumState.get();
        out.collect(new AverageResult(
            reading.sensorId,
            current.sum / current.count,
            current.count,
            ctx.timestamp()
        ));
    }

    public static class CountSum {
        public long count;
        public double sum;

        public CountSum() {}

        public CountSum(long count, double sum) {
            this.count = count;
            this.sum = sum;
        }
    }
}
```

### 步骤 5: State TTL 配置

```java
import org.apache.flink.api.common.state.StateTtlConfig;
import org.apache.flink.api.common.time.Time;

import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.streaming.api.windowing.time.Time;


public class StatefulFunctionWithTTL extends KeyedProcessFunction<...> {

    private ValueState<UserSession> sessionState;

    @Override
    public void open(Configuration parameters) {
        // 配置 TTL
        StateTtlConfig ttlConfig = StateTtlConfig
            .newBuilder(Time.minutes(30))  // 30分钟过期
            .setUpdateType(StateTtlConfig.UpdateType.OnCreateAndWrite)
            .setStateVisibility(StateTtlConfig.StateVisibility.NeverReturnExpired)
            .cleanupIncrementally(10, true)  // 增量清理
            .build();

        ValueStateDescriptor<UserSession> descriptor =
            new ValueStateDescriptor<>("session", UserSession.class);

        descriptor.enableTimeToLive(ttlConfig);
        sessionState = getRuntimeContext().getState(descriptor);
    }
}
```

### 步骤 6: Operator State 示例 - 自定义 Source

```java
import org.apache.flink.streaming.api.checkpoint.CheckpointedFunction;
import org.apache.flink.runtime.state.FunctionInitializationContext;
import org.apache.flink.runtime.state.FunctionSnapshotContext;

public class CheckpointedCounterSource implements
    SourceFunction<Long>, CheckpointedFunction {

    private volatile boolean isRunning = true;
    private long count = 0L;

    // Operator State
    private ListState<Long> checkpointedCount;

    @Override
    public void run(SourceContext<Long> ctx) throws Exception {
        while (isRunning) {
            synchronized (ctx.getCheckpointLock()) {
                ctx.collect(count++);
            }
            Thread.sleep(1000);
        }
    }

    @Override
    public void snapshotState(FunctionSnapshotContext context) throws Exception {
        // Checkpoint 时保存状态
        checkpointedCount.clear();
        checkpointedCount.add(count);
    }

    @Override
    public void initializeState(FunctionInitializationContext context) throws Exception {
        // 初始化状态
        ListStateDescriptor<Long> descriptor =
            new ListStateDescriptor<>("counter", Long.class);

        checkpointedCount = context.getOperatorStateStore().getListState(descriptor);

        // 从 Checkpoint 恢复
        if (context.isRestored()) {
            for (Long c : checkpointedCount.get()) {
                count = c;
            }
        }
    }

    @Override
    public void cancel() {
        isRunning = false;
    }
}
```

## 验证方法

### 检查清单

- [ ] 理解 Keyed State 和 Operator State 的区别
- [ ] 能够选择合适的 State 类型
- [ ] 掌握 State TTL 配置方法
- [ ] 理解状态清理策略
- [ ] 能够通过 Checkpoint 恢复状态

### 测试用例

```java
@Test
public void testTemperatureAlert() throws Exception {
    // 创建测试 harness
    KeyedProcessFunctionTestHarness<String, SensorReading, Alert> harness =
        new KeyedProcessFunctionTestHarness<>(
            new TemperatureAlertFunction(),
            SensorReading::getSensorId,
            TypeInformation.of(String.class)
        );

    harness.open();

    // 发送正常温度
    harness.processElement(new SensorReading("s1", 20.0, 0L), 0L);
    harness.processElement(new SensorReading("s1", 21.0, 1000L), 1000L);

    // 发送跳变温度（应触发告警）
    harness.processElement(new SensorReading("s1", 35.0, 2000L), 2000L);

    // 验证输出
    assertEquals(1, harness.extractOutputValues().size());
}
```

## 扩展练习

### 练习 1: 实现复杂状态机

使用状态实现订单生命周期管理：

```java
// 订单状态机: CREATED -> PAID -> SHIPPED -> DELIVERED

import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.streaming.api.windowing.time.Time;

public class OrderStateMachine extends KeyedProcessFunction<String, OrderEvent, Order> {

    private ValueState<OrderStatus> orderStatusState;
    private ValueState<Long> statusUpdateTimeState;

    @Override
    public void processElement(OrderEvent event, Context ctx, Collector<Order> out) {
        OrderStatus currentStatus = orderStatusState.value();
        OrderStatus newStatus = calculateNewStatus(currentStatus, event);

        if (isValidTransition(currentStatus, newStatus)) {
            orderStatusState.update(newStatus);
            statusUpdateTimeState.update(ctx.timestamp());

            // 超时检查：如果PAID后30分钟未SHIP，发送提醒
            if (newStatus == OrderStatus.PAID) {
                ctx.timerService().registerEventTimeTimer(
                    ctx.timestamp() + Time.minutes(30).toMilliseconds()
                );
            }
        }
    }
}
```

### 练习 2: 状态查询（Queryable State）

配置可查询状态用于外部监控：

```java

import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;

// 启用状态查询
ValueStateDescriptor<Long> descriptor =
    new ValueStateDescriptor<>("counter", Long.class);
descriptor.setQueryable("queryable-counter");

// 外部客户端查询
QueryableStateClient client = new QueryableStateClient(tmHostname, proxyPort);
CompletableFuture<ValueState<Long>> future = client.getKvState(
    jobId,
    "queryable-counter",
    key,
    BasicTypeInfo.STRING_TYPE_INFO,
    descriptor
);
```

## 最佳实践

1. **选择合适的状态类型**：简单值用 ValueState，列表用 ListState，键值对用 MapState
2. **配置 TTL**：为临时状态配置过期时间，避免无限增长
3. **及时清理**：用完状态后调用 clear() 清理
4. **避免大状态**：ListState 和 MapState 可能无限增长，需要限制大小

## 下一步

- [Lab 5: Checkpoint与恢复](./lab-05-checkpoint.md)
- [Lab 6: CEP模式匹配](./lab-06-cep.md)

## 引用参考
