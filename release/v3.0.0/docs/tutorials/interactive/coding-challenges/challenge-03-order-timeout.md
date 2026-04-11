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
    public String userId;     // 用户ID，用于发送通知
    public String status;     // CREATED / PAID / CANCELLED / SHIPPED / DELIVERED
    public double amount;
    public long createTime;
    public Long payTime;
    public Long cancelTime;
    public String cancelReason;
    public Map<String, Integer> items;  // 商品ID -> 数量，用于库存管理
}

public class OrderResult {
    public String orderId;
    public String result;     // SUCCESS / TIMEOUT / CANCELLED
    public String message;
    public long timestamp;
}

/**
 * 通知消息 - 用于订单状态变更通知
 */
public class NotificationMessage {
    public String orderId;
    public String userId;
    public String type;       // ORDER_TIMEOUT / ORDER_PAID / ORDER_CANCELLED
    public String content;
    public long timestamp;
    public String channel;    // SMS / EMAIL / PUSH
}

/**
 * 库存释放事件 - 用于超时后释放预占库存
 */
public class InventoryReleaseEvent {
    public String orderId;
    public String reason;     // TIMEOUT_CANCEL / USER_CANCEL / SYSTEM_CANCEL
    public long timestamp;
    public Map<String, Integer> items;  // 商品ID -> 数量
}
```

## 实现步骤

### Step 0: 理解Side Output机制

在实现订单超时处理之前，需要理解Flink的**Side Output**机制。Side Output允许从一个主流中分离出多个旁路输出流，适用于以下场景：
- 异常数据分流
- 多路输出（如同时输出结果和日志）
- 延迟数据处理

```java
// 定义Side Output Tag
public static final OutputTag<NotificationMessage> NOTIFICATION_TAG =
    new OutputTag<NotificationMessage>("notifications") {};

// 在processElement中输出到Side Output
ctx.output(NOTIFICATION_TAG, notificationMessage);

// 在主程序中获取Side Output流
DataStream<NotificationMessage> notifications = results
    .getSideOutput(OrderProcessor.NOTIFICATION_TAG);
```

### Step 1: 订单状态机实现

```java
public class OrderProcessor extends
    KeyedProcessFunction<String, OrderEvent, OrderResult> {

    // Side Output Tag 定义
    public static final OutputTag<NotificationMessage> NOTIFICATION_TAG =
        new OutputTag<NotificationMessage>("notifications") {};
    public static final OutputTag<InventoryReleaseEvent> INVENTORY_RELEASE_TAG =
        new OutputTag<InventoryReleaseEvent>("inventory-release") {};

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
        newOrder.userId = event.userId;
        newOrder.status = "CREATED";
        newOrder.amount = event.amount;
        newOrder.createTime = event.timestamp;
        newOrder.items = event.properties != null ?
            parseItems(event.properties.get("items")) : new HashMap<>();

        orderState.update(newOrder);

        // 注册超时定时器
        long timeoutTime = event.timestamp + TIMEOUT_MS;
        ctx.timerService().registerEventTimeTimer(timeoutTime);
        timeoutTimerState.update(timeoutTime);

        out.collect(new OrderResult(
            event.orderId, "SUCCESS", "Order created, payment pending", ctx.timestamp()
        ));

        // 发送订单创建通知
        NotificationMessage notification = new NotificationMessage();
        notification.orderId = event.orderId;
        notification.userId = event.userId;
        notification.type = "ORDER_CREATED";
        notification.content = String.format(
            "订单已创建，请在15分钟内完成支付，金额: %.2f", event.amount
        );
        notification.timestamp = ctx.timestamp();
        ctx.output(NOTIFICATION_TAG, notification);
    }

    /**
     * 解析商品信息字符串为Map
     * 格式: "SKU001:2,SKU002:1"
     */
    private Map<String, Integer> parseItems(String itemsStr) {
        Map<String, Integer> items = new HashMap<>();
        if (itemsStr == null || itemsStr.isEmpty()) {
            return items;
        }
        String[] pairs = itemsStr.split(",");
        for (String pair : pairs) {
            String[] parts = pair.split(":");
            if (parts.length == 2) {
                items.put(parts[0].trim(), Integer.parseInt(parts[1].trim()));
            }
        }
        return items;
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

            // 发送超时通知到Side Output
            NotificationMessage notification = new NotificationMessage();
            notification.orderId = ctx.getCurrentKey();
            notification.userId = currentState.userId;
            notification.type = "ORDER_TIMEOUT";
            notification.content = String.format(
                "您的订单 %s 因超时未支付已自动取消，金额: %.2f",
                currentState.orderId, currentState.amount
            );
            notification.timestamp = timestamp;
            ctx.output(NOTIFICATION_TAG, notification);

            // 发送库存释放事件到Side Output
            InventoryReleaseEvent releaseEvent = new InventoryReleaseEvent();
            releaseEvent.orderId = ctx.getCurrentKey();
            releaseEvent.reason = "TIMEOUT_CANCEL";
            releaseEvent.timestamp = timestamp;
            ctx.output(INVENTORY_RELEASE_TAG, releaseEvent);

            // 记录超时审计日志
            logTimeoutAudit(currentState, timestamp);
        }
    }

    /**
     * 记录订单超时审计日志
     */
    private void logTimeoutAudit(OrderState state, long timestamp) {
        System.out.printf("[AUDIT] Order timeout: orderId=%s, userId=%s, " +
            "amount=%.2f, createTime=%d, timeoutAt=%d%n",
            state.orderId, state.userId, state.amount,
            state.createTime, timestamp);
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

### Step 3: 主程序（含Side Output处理）

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
        SingleOutputStreamOperator<OrderResult> results = orderEvents
            .keyBy(event -> event.orderId)
            .process(new OrderProcessor());

        // 输出主结果
        results.print("ORDER_RESULT");

        // ========== Side Output: 通知消息处理 ==========
        DataStream<NotificationMessage> notifications = results
            .getSideOutput(OrderProcessor.NOTIFICATION_TAG);

        // 通知可以发送到多个渠道
        notifications
            .filter(n -> n.type.equals("ORDER_TIMEOUT"))
            .addSink(new NotificationSink("SMS"));      // 短信通知

        notifications
            .filter(n -> n.type.equals("ORDER_CREATED"))
            .addSink(new NotificationSink("PUSH"));     // App推送

        // ========== Side Output: 库存释放事件处理 ==========
        DataStream<InventoryReleaseEvent> inventoryReleases = results
            .getSideOutput(OrderProcessor.INVENTORY_RELEASE_TAG);

        inventoryReleases
            .keyBy(event -> event.orderId)
            .process(new InventoryReleaseHandler())
            .name("Inventory Release Handler");

        // ========== 统计窗口 ==========
        results
            .windowAll(TumblingEventTimeWindows.of(Time.minutes(5)))
            .process(new OrderStatistics())
            .print("STATISTICS");

        env.execute("Order Timeout Management");
    }
}
```

### Step 4: 通知发送Sink实现

```java
/**
 * 通知发送Sink - 支持多渠道通知
 */
public class NotificationSink implements SinkFunction<NotificationMessage> {

    private final String channel;
    private transient NotificationClient client;

    public NotificationSink(String channel) {
        this.channel = channel;
    }

    @Override
    public void open(Configuration parameters) throws Exception {
        // 初始化通知客户端
        client = new NotificationClient(channel);
        client.connect();
    }

    @Override
    public void invoke(NotificationMessage message, Context context) {
        try {
            // 根据消息类型和渠道发送通知
            switch (message.type) {
                case "ORDER_TIMEOUT":
                    client.sendTimeoutNotification(message);
                    break;
                case "ORDER_CREATED":
                    client.sendReminder(message);
                    break;
                case "ORDER_PAID":
                    client.sendConfirmation(message);
                    break;
                default:
                    client.sendGeneric(message);
            }
            System.out.printf("[NOTIFY-%s] Sent to user %s: %s%n",
                channel, message.userId, message.content);
        } catch (Exception e) {
            System.err.printf("[NOTIFY-ERROR] Failed to send: %s, error: %s%n",
                message.orderId, e.getMessage());
        }
    }

    @Override
    public void close() throws Exception {
        if (client != null) {
            client.disconnect();
        }
    }
}
```

### Step 5: 库存释放处理器实现

```java
/**
 * 库存释放处理器 - 处理超时订单的库存回滚
 */
public class InventoryReleaseHandler extends
    KeyedProcessFunction<String, InventoryReleaseEvent, InventoryReleaseResult> {

    // 库存状态（实际项目中可能连接外部库存系统）
    private ValueState<Map<String, Integer>> inventoryState;

    @Override
    public void open(Configuration parameters) {
        inventoryState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("inventory", Types.MAP(Types.STRING, Types.INT))
        );
    }

    @Override
    public void processElement(
            InventoryReleaseEvent event,
            Context ctx,
            Collector<InventoryReleaseResult> out) throws Exception {

        // 从事件中获取商品信息并释放库存
        // 实际项目中这里会调用库存服务的API

        InventoryReleaseResult result = new InventoryReleaseResult();
        result.orderId = event.orderId;
        result.success = true;
        result.releaseTime = ctx.timestamp();
        result.reason = event.reason;

        // 模拟库存释放操作
        releaseInventory(event.orderId, event.items);

        out.collect(result);

        System.out.printf("[INVENTORY] Released for order %s, reason: %s%n",
            event.orderId, event.reason);
    }

    private void releaseInventory(String orderId, Map<String, Integer> items) {
        // 实际实现：
        // 1. 调用库存服务API
        // 2. 更新数据库
        // 3. 发送消息到库存消息队列
        if (items != null) {
            items.forEach((sku, quantity) -> {
                System.out.printf("  - SKU: %s, Quantity: %d%n", sku, quantity);
            });
        }
    }
}

public class InventoryReleaseResult {
    public String orderId;
    public boolean success;
    public long releaseTime;
    public String reason;
}
```

### Step 6: 完整的超时处理流程说明

订单超时处理的完整流程如下：

```
┌─────────────────┐
│   订单创建事件   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 保存订单状态    │──────┐
│ 注册15分钟定时器│      │
└────────┬────────┘      │
         │               │
         ▼               │ Side Output
┌─────────────────┐      │
│ 发送创建通知    │◄─────┘
└─────────────────┘
         │
    15分钟内?
    /        \
  是          否(超时)
  /            \
支付成功      ┌─────────────────┐
  │           │ 更新状态为CANCELLED│
  ▼           │ 清除定时器状态   │
┌─────────────────┐  │
│ 更新状态为PAID  │  │
│ 取消定时器      │  │
│ 发送支付成功通知│  │
└─────────────────┘  │ Side Output
                     ▼
            ┌─────────────────┐
            │ 发送超时通知     │
            │ 发送库存释放事件 │
            │ 记录审计日志     │
            └─────────────────┘
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

### 完整参考答案概览

以下是订单超时处理的完整参考实现核心逻辑：

#### 1. 核心状态机处理器（完整版）

```java
public class OrderProcessor extends
    KeyedProcessFunction<String, OrderEvent, OrderResult> {

    // Side Output Tags
    public static final OutputTag<NotificationMessage> NOTIFICATION_TAG =
        new OutputTag<NotificationMessage>("notifications") {};
    public static final OutputTag<InventoryReleaseEvent> INVENTORY_RELEASE_TAG =
        new OutputTag<InventoryReleaseEvent>("inventory-release") {};

    // 状态和配置
    private ValueState<OrderState> orderState;
    private ValueState<Long> timeoutTimerState;
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
    public void processElement(OrderEvent event, Context ctx, Collector<OrderResult> out)
            throws Exception {
        switch (event.eventType) {
            case "CREATE":
                handleCreate(event, ctx, out);
                break;
            case "PAY":
                handlePay(event, ctx, out);
                break;
            case "CANCEL":
                handleCancel(event, ctx, out);
                break;
            default:
                out.collect(new OrderResult(event.orderId, "ERROR", 
                    "Unknown type", ctx.timestamp()));
        }
    }

    private void handleCreate(OrderEvent event, Context ctx, Collector<OrderResult> out)
            throws Exception {
        // 初始化订单状态
        OrderState state = new OrderState();
        state.orderId = event.orderId;
        state.userId = event.userId;
        state.status = "CREATED";
        state.amount = event.amount;
        state.createTime = event.timestamp;
        state.items = parseItems(event.properties.get("items"));
        orderState.update(state);

        // 注册超时定时器
        long timeoutTime = event.timestamp + TIMEOUT_MS;
        ctx.timerService().registerEventTimeTimer(timeoutTime);
        timeoutTimerState.update(timeoutTime);

        out.collect(new OrderResult(event.orderId, "SUCCESS", 
            "Order created", ctx.timestamp()));

        // Side Output: 发送创建通知
        ctx.output(NOTIFICATION_TAG, buildNotification(event, "ORDER_CREATED",
            String.format("订单已创建，请在15分钟内支付 %.2f 元", event.amount)));
    }

    private void handlePay(OrderEvent event, Context ctx, Collector<OrderResult> out)
            throws Exception {
        OrderState state = orderState.value();
        if (state == null || !state.status.equals("CREATED")) {
            out.collect(new OrderResult(event.orderId, "ERROR", 
                "Invalid state for payment", ctx.timestamp()));
            return;
        }

        // 更新状态
        state.status = "PAID";
        state.payTime = event.timestamp;
        orderState.update(state);

        // 取消超时定时器
        Long timer = timeoutTimerState.value();
        if (timer != null) {
            ctx.timerService().deleteEventTimeTimer(timer);
            timeoutTimerState.clear();
        }

        out.collect(new OrderResult(event.orderId, "SUCCESS", 
            "Payment successful", ctx.timestamp()));

        // Side Output: 发送支付成功通知
        ctx.output(NOTIFICATION_TAG, buildNotification(event, "ORDER_PAID",
            String.format("订单支付成功，金额: %.2f 元", event.amount)));
    }

    @Override
    public void onTimer(long timestamp, OnTimerContext ctx, Collector<OrderResult> out)
            throws Exception {
        OrderState state = orderState.value();
        if (state != null && state.status.equals("CREATED")) {
            // 超时处理
            state.status = "CANCELLED";
            state.cancelTime = timestamp;
            state.cancelReason = "TIMEOUT";
            orderState.update(state);
            timeoutTimerState.clear();

            out.collect(new OrderResult(ctx.getCurrentKey(), "TIMEOUT", 
                "Order cancelled due to timeout", timestamp));

            // Side Output: 发送超时通知
            ctx.output(NOTIFICATION_TAG, buildNotification(
                state.orderId, state.userId, "ORDER_TIMEOUT",
                String.format("订单 %s 因超时未支付已自动取消", state.orderId)));

            // Side Output: 发送库存释放事件
            ctx.output(INVENTORY_RELEASE_TAG, buildInventoryRelease(state));
        }
    }

    private NotificationMessage buildNotification(OrderEvent event, String type, 
            String content) {
        NotificationMessage msg = new NotificationMessage();
        msg.orderId = event.orderId;
        msg.userId = event.userId;
        msg.type = type;
        msg.content = content;
        msg.timestamp = event.timestamp;
        return msg;
    }

    private NotificationMessage buildNotification(String orderId, String userId,
            String type, String content) {
        NotificationMessage msg = new NotificationMessage();
        msg.orderId = orderId;
        msg.userId = userId;
        msg.type = type;
        msg.content = content;
        msg.timestamp = System.currentTimeMillis();
        return msg;
    }

    private InventoryReleaseEvent buildInventoryRelease(OrderState state) {
        InventoryReleaseEvent event = new InventoryReleaseEvent();
        event.orderId = state.orderId;
        event.reason = "TIMEOUT_CANCEL";
        event.timestamp = state.cancelTime;
        event.items = state.items;
        return event;
    }
}
```

#### 2. 数据类定义

```java
// 订单事件
public class OrderEvent {
    public String orderId;
    public String userId;
    public String eventType;
    public double amount;
    public long timestamp;
    public Map<String, String> properties;
}

// 订单状态
public class OrderState {
    public String orderId;
    public String userId;
    public String status;
    public double amount;
    public long createTime;
    public Long payTime;
    public Long cancelTime;
    public String cancelReason;
    public Map<String, Integer> items;
}

// 订单结果
public class OrderResult {
    public String orderId;
    public String result;
    public String message;
    public long timestamp;
}

// 通知消息
public class NotificationMessage {
    public String orderId;
    public String userId;
    public String type;
    public String content;
    public long timestamp;
}

// 库存释放事件
public class InventoryReleaseEvent {
    public String orderId;
    public String reason;
    public long timestamp;
    public Map<String, Integer> items;
}
```

完整参考实现位于 `reference/challenge-03-order-timeout/` 目录。

## 下一步

- [Challenge 4: 实时推荐系统](./challenge-04-recommendation.md)
