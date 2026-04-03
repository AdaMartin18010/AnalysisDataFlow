# Challenge 3: 订单超时处理

> 难度: 中级 | 预计时间: 3小时 | 主题: Timer、State

## 需求描述

实现一个电商订单处理系统，处理订单生命周期中的超时取消逻辑。

### 功能需求

1. **订单创建**
   - 接收订单创建事件
   - 设置15分钟支付超时定时器
   - 保存订单状态

2. **订单支付**
   - 接收支付成功/失败事件
   - 取消超时定时器
   - 更新订单状态

3. **订单超时处理**
   - 15分钟内未支付自动取消
   - 释放库存
   - 发送通知

4. **状态查询**
   - 支持查询订单当前状态
   - 统计各状态订单数量

### 订单状态机

```
CREATED -> [支付] -> PAID -> [发货] -> SHIPPED -> [签收] -> DELIVERED
   |
   | [15分钟超时]
   v
CANCELLED
```

## 数据结构

```java
public class OrderEvent {
    public String orderId;
    public String userId;
    public String eventType;  // CREATE / PAY / CANCEL / SHIP / DELIVER
    public double amount;
    public long timestamp;
    public Map<String, String> properties;
}

public class OrderState {
    public String orderId;
    public String status;     // CREATED / PAID / CANCELLED / SHIPPED / DELIVERED
    public double amount;
    public long createTime;
    public Long payTime;
    public Long cancelTime;
    public String cancelReason;
}

public class OrderResult {
    public String orderId;
    public String result;     // SUCCESS / TIMEOUT / CANCELLED
    public String message;
    public long timestamp;
}
```

## 实现步骤

### Step 1: 订单状态机实现

```java
public class OrderProcessor extends
    KeyedProcessFunction<String, OrderEvent, OrderResult> {

    // 状态声明
    private ValueState<OrderState> orderState;
    private ValueState<Long> timeoutTimerState;

    // 超时时间：15分钟
    private static final long TIMEOUT_MS = 15 * 60 * 1000;

    @Override
    public void open(Configuration parameters) {
        StateTtlConfig ttlConfig = StateTtlConfig
            .newBuilder(Time.hours(24))
            .setUpdateType(StateTtlConfig.UpdateType.OnCreateAndWrite)
            .setStateVisibility(StateTtlConfig.StateVisibility.NeverReturnExpired)
            .cleanupIncrementally(10, true)
            .build();

        ValueStateDescriptor<OrderState> stateDescriptor =
            new ValueStateDescriptor<>("orderState", OrderState.class);
        stateDescriptor.enableTimeToLive(ttlConfig);

        orderState = getRuntimeContext().getState(stateDescriptor);
        timeoutTimerState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("timeoutTimer", Long.class)
        );
    }

    @Override
    public void processElement(
            OrderEvent event,
            Context ctx,
            Collector<OrderResult> out) throws Exception {

        OrderState currentState = orderState.value();

        switch (event.eventType) {
            case "CREATE":
                handleCreate(event, ctx, out);
                break;
            case "PAY":
                handlePay(event, currentState, ctx, out);
                break;
            case "CANCEL":
                handleCancel(event, currentState, ctx, out);
                break;
            case "QUERY":
                handleQuery(event, currentState, out);
                break;
            default:
                out.collect(new OrderResult(
                    event.orderId, "ERROR", "Unknown event type", ctx.timestamp()
                ));
        }
    }

    private void handleCreate(
            OrderEvent event,
            Context ctx,
            Collector<OrderResult> out) throws Exception {

        OrderState newOrder = new OrderState();
        newOrder.orderId = event.orderId;
        newOrder.status = "CREATED";
        newOrder.amount = event.amount;
        newOrder.createTime = event.timestamp;

        orderState.update(newOrder);

        // 注册超时定时器
        long timeoutTime = event.timestamp + TIMEOUT_MS;
        ctx.timerService().registerEventTimeTimer(timeoutTime);
        timeoutTimerState.update(timeoutTime);

        out.collect(new OrderResult(
            event.orderId, "SUCCESS", "Order created, payment pending", ctx.timestamp()
        ));
    }

    private void handlePay(
            OrderEvent event,
            OrderState currentState,
            Context ctx,
            Collector<OrderResult> out) throws Exception {

        if (currentState == null) {
            out.collect(new OrderResult(
                event.orderId, "ERROR", "Order not found", ctx.timestamp()
            ));
            return;
        }

        if (!currentState.status.equals("CREATED")) {
            out.collect(new OrderResult(
                event.orderId, "ERROR",
                "Invalid status for payment: " + currentState.status,
                ctx.timestamp()
            ));
            return;
        }

        // 更新状态
        currentState.status = "PAID";
        currentState.payTime = event.timestamp;
        orderState.update(currentState);

        // 取消超时定时器
        Long timeoutTime = timeoutTimerState.value();
        if (timeoutTime != null) {
            ctx.timerService().deleteEventTimeTimer(timeoutTime);
            timeoutTimerState.clear();
        }

        out.collect(new OrderResult(
            event.orderId, "SUCCESS", "Payment successful", ctx.timestamp()
        ));
    }

    private void handleCancel(
            OrderEvent event,
            OrderState currentState,
            Context ctx,
            Collector<OrderResult> out) throws Exception {

        if (currentState == null || !currentState.status.equals("CREATED")) {
            out.collect(new OrderResult(
                event.orderId, "ERROR", "Cannot cancel order", ctx.timestamp()
            ));
            return;
        }

        currentState.status = "CANCELLED";
        currentState.cancelTime = event.timestamp;
        currentState.cancelReason = event.properties.get("reason");
        orderState.update(currentState);

        // 取消超时定时器
        Long timeoutTime = timeoutTimerState.value();
        if (timeoutTime != null) {
            ctx.timerService().deleteEventTimeTimer(timeoutTime);
            timeoutTimerState.clear();
        }

        out.collect(new OrderResult(
            event.orderId, "SUCCESS", "Order cancelled", ctx.timestamp()
        ));
    }

    private void handleQuery(
            OrderEvent event,
            OrderState currentState,
            Collector<OrderResult> out) {

        String status = currentState != null ? currentState.status : "NOT_FOUND";
        out.collect(new OrderResult(
            event.orderId, "INFO", "Status: " + status, System.currentTimeMillis()
        ));
    }

    @Override
    public void onTimer(
            long timestamp,
            OnTimerContext ctx,
            Collector<OrderResult> out) throws Exception {

        OrderState currentState = orderState.value();

        if (currentState != null && currentState.status.equals("CREATED")) {
            // 超时，自动取消
            currentState.status = "CANCELLED";
            currentState.cancelTime = timestamp;
            currentState.cancelReason = "TIMEOUT";
            orderState.update(currentState);

            timeoutTimerState.clear();

            out.collect(new OrderResult(
                ctx.getCurrentKey(),
                "TIMEOUT",
                "Order cancelled due to payment timeout",
                timestamp
            ));

            // TODO: 发送通知、释放库存等
        }
    }
}
```

### Step 2: 订单统计

```java
public class OrderStatistics extends
    ProcessAllWindowFunction<OrderResult, Statistics, TimeWindow> {

    @Override
    public void process(
            Context context,
            Iterable<OrderResult> elements,
            Collector<Statistics> out) {

        Map<String, Long> statusCounts = new HashMap<>();
        long totalOrders = 0;
        long timeoutOrders = 0;

        for (OrderResult result : elements) {
            totalOrders++;

            if (result.result.equals("TIMEOUT")) {
                timeoutOrders++;
            }

            statusCounts.merge(result.result, 1L, Long::sum);
        }

        Statistics stats = new Statistics();
        stats.windowStart = context.window().getStart();
        stats.windowEnd = context.window().getEnd();
        stats.totalOrders = totalOrders;
        stats.timeoutOrders = timeoutOrders;
        stats.timeoutRate = totalOrders > 0 ?
            (double) timeoutOrders / totalOrders : 0.0;
        stats.statusDistribution = statusCounts;

        out.collect(stats);
    }
}
```

### Step 3: 主程序

```java
public class OrderTimeoutJob {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(4);

        // 订单事件流
        DataStream<OrderEvent> orderEvents = env
            .addSource(new OrderEventSource())
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<OrderEvent>forBoundedOutOfOrderness(
                        Duration.ofSeconds(5))
                    .withTimestampAssigner((event, ts) -> event.timestamp)
            );

        // 处理订单
        DataStream<OrderResult> results = orderEvents
            .keyBy(event -> event.orderId)
            .process(new OrderProcessor());

        // 输出结果
        results.print("ORDER_RESULT");

        // 统计窗口
        results
            .windowAll(TumblingEventTimeWindows.of(Time.minutes(5)))
            .process(new OrderStatistics())
            .print("STATISTICS");

        // 超时订单特殊处理
        results
            .filter(r -> r.result.equals("TIMEOUT"))
            .addSink(new TimeoutNotificationSink());

        env.execute("Order Timeout Management");
    }
}
```

## 验证方法

### 测试用例

```java
@Test
public void testOrderTimeout() throws Exception {
    // 创建测试 harness
    KeyedProcessFunctionTestHarness<String, OrderEvent, OrderResult> harness =
        new KeyedProcessFunctionTestHarness<>(
            new OrderProcessor(),
            OrderEvent::getOrderId,
            TypeInformation.of(String.class)
        );

    harness.open();

    String orderId = "ORDER_001";
    long baseTime = 1000000L;

    // 创建订单
    harness.processElement(
        new OrderEvent(orderId, "USER_001", "CREATE", 100.0, baseTime),
        baseTime
    );

    // 验证定时器注册
    assertEquals(1, harness.numEventTimeTimers());

    // 触发超时
    harness.setCurrentWatermark(baseTime + 16 * 60 * 1000);

    // 验证超时结果
    List<OrderResult> results = harness.extractOutputValues();
    assertTrue(results.stream().anyMatch(r -> r.result.equals("TIMEOUT")));
}

@Test
public void testOrderPay() throws Exception {
    // 创建订单后支付，验证定时器被取消
    harness.processElement(
        new OrderEvent(orderId, "USER_001", "CREATE", 100.0, baseTime),
        baseTime
    );

    harness.processElement(
        new OrderEvent(orderId, "USER_001", "PAY", 100.0, baseTime + 60000),
        baseTime + 60000
    );

    // 验证定时器已取消
    assertEquals(0, harness.numEventTimeTimers());
}
```

## 评分标准

| 维度 | 权重 | 要求 |
|------|------|------|
| 状态机 | 30% | 正确实现订单状态转换 |
| 定时器 | 30% | 正确注册和取消超时定时器 |
| 状态管理 | 25% | 正确使用 State TTL |
| 代码质量 | 15% | 结构清晰，有测试 |

## 扩展练习

### 扩展 1: 多级超时

```java
// 15分钟未支付 -> 发送提醒
// 30分钟未支付 -> 自动取消
public class MultiLevelTimeout extends KeyedProcessFunction<...> {

    private static final long REMINDER_MS = 15 * 60 * 1000;
    private static final long CANCEL_MS = 30 * 60 * 1000;

    @Override
    public void processElement(...) {
        if (event.eventType.equals("CREATE")) {
            // 注册提醒定时器
            ctx.timerService().registerEventTimeTimer(
                event.timestamp + REMINDER_MS
            );
            // 注册取消定时器
            ctx.timerService().registerEventTimeTimer(
                event.timestamp + CANCEL_MS
            );
        }
    }

    @Override
    public void onTimer(long timestamp, ...) {
        OrderState state = orderState.value();
        if (state == null || !state.status.equals("CREATED")) {
            return;
        }

        long createTime = state.createTime;
        if (timestamp == createTime + REMINDER_MS) {
            // 发送提醒
            out.collect(new OrderResult(..., "REMINDER", ...));
        } else if (timestamp == createTime + CANCEL_MS) {
            // 自动取消
            out.collect(new OrderResult(..., "TIMEOUT", ...));
        }
    }
}
```

### 扩展 2: 库存管理

```java
// 与库存系统联动
public class OrderWithInventory extends KeyedProcessFunction<...> {

    private ValueState<Integer> inventoryState;

    @Override
    public void processElement(OrderEvent event, ...) {
        if (event.eventType.equals("CREATE")) {
            // 预占库存
            int current = inventoryState.value();
            if (current >= event.quantity) {
                inventoryState.update(current - event.quantity);
                // 创建订单
            } else {
                out.collect(new OrderResult(..., "OUT_OF_STOCK", ...));
            }
        } else if (event.eventType.equals("PAY")) {
            // 确认扣减库存
        } else if (event.eventType.equals("CANCEL") ||
                   event.result.equals("TIMEOUT")) {
            // 释放库存
            int current = inventoryState.value();
            inventoryState.update(current + order.quantity);
        }
    }
}
```

## 参考解答

完整参考实现位于 `reference/challenge-03-order-timeout/` 目录。

## 下一步

- [Challenge 4: 实时推荐系统](./challenge-04-recommendation.md)
