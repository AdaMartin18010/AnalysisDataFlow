# 认证准备：自定义考核

> **所属阶段**: 认证准备 | **难度等级**: L1-L6 | **预计时长**: 自定

---

## 考核体系概述

### 自定义考核目的

- **内部评估**: 评估团队流计算能力
- **技能认证**: 建立内部技能等级
- **晋升依据**: 作为晋升考核标准
- **培训效果**: 验证培训成果

### 能力等级定义

| 等级 | 名称 | 能力要求 | 对应学习路径 |
|------|------|----------|--------------|
| L1 | 入门级 | 理解基本概念，能运行示例 | 零基础入门 |
| L2 | 初级 | 能开发简单作业 | 有基础入门 |
| L3 | 中级 | 能独立完成项目 | DataStream专家/SQL专家 |
| L4 | 高级 | 能解决复杂问题 | 状态管理专家 |
| L5 | 专家级 | 能进行性能调优 | 性能调优专家 |
| L6 | 架构级 | 能设计平台架构 | 架构师路径 |

---

## 考核形式

### 1. 理论考核

#### 选择题（40%）

```markdown
【单选题】以下关于 Checkpoint 的说法正确的是：

A. Checkpoint 间隔越短越好
B. Checkpoint 可以保证端到端 Exactly-Once
C. Checkpoint 主要用于故障恢复
D. Checkpoint 会增加数据处理延迟

【正确答案】C

【解析】
A - 错误，间隔太短会影响性能
B - 错误，端到端一致性需要配合两阶段提交
C - 正确，Checkpoint 主要用于故障恢复
D - 不完全正确，对齐 Checkpoint 会阻塞处理，非对齐影响较小
```

#### 判断题（20%）

```markdown
【判断题】Flink SQL 的流处理结果和批处理结果一定相同。

【答案】错误

【解析】由于流处理需要考虑时间语义、Watermark 等因素，
在某些场景下结果可能与批处理不同。例如乱序数据处理。
```

#### 简答题（40%）

```markdown
【简答题】请解释 Flink 的 Watermark 机制及其作用。

【参考答案】
1. 概念：Watermark 是一种特殊的事件，用于表示事件时间的推进
2. 作用：处理乱序数据，触发窗口计算
3. 生成方式：
   - Punctuated：基于事件生成
   - Periodic：周期性生成
4. 配置考虑：
   - 最大乱序时间
   - 业务延迟容忍度
```

### 2. 编程考核

#### 基础编程题（L1-L2）

```java
/**
 * 题目：实现 WordCount
 * 要求：
 * 1. 从 Socket 读取数据
 * 2. 统计每个单词出现次数
 * 3. 每秒输出一次结果
 *
 * 时间：30分钟
 */
public class WordCountExercise {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        // 完整实现：WordCount

        // 1. 从Socket读取数据
        DataStream<String> source = env.socketTextStream("localhost", 9999);

        // 2. 分词并转换为(word, 1)格式
        DataStream<Tuple2<String, Integer>> words = source
            .flatMap(new FlatMapFunction<String, Tuple2<String, Integer>>() {
                @Override
                public void flatMap(String value, Collector<Tuple2<String, Integer>> out) {
                    // 分割句子为单词，过滤空字符串
                    for (String word : value.toLowerCase().split("\\s+")) {
                        if (word.length() > 0 && word.matches("[a-z0-9]+")) {
                            out.collect(new Tuple2<>(word, 1));
                        }
                    }
                }
            });

        // 3. 按单词分组，每秒统计一次（使用Processing Time窗口）
        DataStream<Tuple2<String, Integer>> wordCounts = words
            .keyBy(value -> value.f0)
            .window(TumblingProcessingTimeWindows.of(Time.seconds(1)))
            .sum(1);

        // 4. 输出结果到控制台
        wordCounts.print();

        env.execute("WordCount");
    }
}

// **参考答案**：WordCount完整实现
/*
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.util.Collector;

public class WordCountExercise {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(1);

        // 1. 从Socket读取数据
        DataStream<String> source = env.socketTextStream("localhost", 9999);

        // 2. 分词并转换为(word, count)格式
        DataStream<Tuple2<String, Integer>> words = source
            .flatMap(new FlatMapFunction<String, Tuple2<String, Integer>>() {
                @Override
                public void flatMap(String value, Collector<Tuple2<String, Integer>> out) {
                    for (String word : value.toLowerCase().split("\\s+")) {
                        if (word.length() > 0) {
                            out.collect(new Tuple2<>(word, 1));
                        }
                    }
                }
            });

        // 3. 按单词分组，每秒统计一次
        DataStream<Tuple2<String, Integer>> wordCounts = words
            .keyBy(value -> value.f0)
            .window(TumblingProcessingTimeWindows.of(Time.seconds(1)))
            .sum(1);

        // 4. 输出结果
        wordCounts.print();

        env.execute("WordCount");
    }
}
*/
```

#### 中级编程题（L3）

```java
/**
 * 题目：实时订单超时检测
 * 场景：
 * - 订单创建后 30 分钟内未支付视为超时
 * - 超时订单需要输出告警
 *
 * 输入：订单事件流（创建、支付）
 * 输出：超时订单
 *
 * 时间：60分钟
 */
public class OrderTimeoutDetection extends KeyedProcessFunction<String,
    OrderEvent, OrderTimeoutAlert> {

    // 状态声明：保存订单创建时间
    private ValueState<Long> createTimeState;
    // 状态声明：保存定时器时间戳
    private ValueState<Long> timerState;

    @Override
    public void open(Configuration parameters) {
        // 初始化状态
        createTimeState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("createTime", Long.class));
        timerState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("timer", Long.class));
    }

    @Override
    public void processElement(OrderEvent event, Context ctx,
                               Collector<OrderTimeoutAlert> out) throws Exception {

        if ("CREATE".equals(event.eventType)) {
            // 订单创建事件：设置30分钟后的超时检测定时器
            long delay = 30 * 60 * 1000; // 30分钟（毫秒）
            long timerTimestamp = ctx.timerService().currentProcessingTime() + delay;

            // 注册Processing Time定时器
            ctx.timerService().registerProcessingTimeTimer(timerTimestamp);

            // 保存状态
            createTimeState.update(event.timestamp);
            timerState.update(timerTimestamp);

            System.out.println("订单 " + event.orderId + " 创建，设置超时检测定时器");

        } else if ("PAY".equals(event.eventType)) {
            // 订单支付事件：取消定时器
            Long timer = timerState.value();
            if (timer != null) {
                ctx.timerService().deleteProcessingTimeTimer(timer);
                createTimeState.clear();
                timerState.clear();
                System.out.println("订单 " + event.orderId + " 已支付，取消超时检测");
            }
        }
    }

    @Override
    public void onTimer(long timestamp, OnTimerContext ctx,
                        Collector<OrderTimeoutAlert> out) throws Exception {
        // 定时器触发，订单超时
        Long createTime = createTimeState.value();
        String orderId = ctx.getCurrentKey();

        out.collect(new OrderTimeoutAlert(orderId, createTime, "订单超时未支付"));

        // 清理状态
        createTimeState.clear();
        timerState.clear();
    }
}

// **参考答案**：订单超时检测实现
/*
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.util.Collector;

// 订单事件类
class OrderEvent {
    String orderId;
    String eventType;  // "CREATE" 或 "PAY"
    long timestamp;

    public OrderEvent(String orderId, String eventType, long timestamp) {
        this.orderId = orderId;
        this.eventType = eventType;
        this.timestamp = timestamp;
    }
}

// 超时告警类
class OrderTimeoutAlert {
    String orderId;
    long createTime;
    String message;

    public OrderTimeoutAlert(String orderId, long createTime, String message) {
        this.orderId = orderId;
        this.createTime = createTime;
        this.message = message;
    }

    @Override
    public String toString() {
        return "OrderTimeoutAlert{" +
               "orderId='" + orderId + '\'' +
               ", createTime=" + createTime +
               ", message='" + message + '\'' +
               '}';
    }
}

public class OrderTimeoutDetection extends KeyedProcessFunction<String, OrderEvent, OrderTimeoutAlert> {

    // 保存订单创建时间的状态
    private ValueState<Long> createTimeState;
    // 保存定时器时间戳的状态
    private ValueState<Long> timerState;

    @Override
    public void open(Configuration parameters) {
        createTimeState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("createTime", Long.class));
        timerState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("timer", Long.class));
    }

    @Override
    public void processElement(OrderEvent event, Context ctx, Collector<OrderTimeoutAlert> out)
            throws Exception {

        if ("CREATE".equals(event.eventType)) {
            // 订单创建事件：设置30分钟后的定时器
            long delay = 30 * 60 * 1000; // 30分钟（毫秒）
            long timerTimestamp = ctx.timerService().currentProcessingTime() + delay;

            ctx.timerService().registerProcessingTimeTimer(timerTimestamp);

            // 保存状态
            createTimeState.update(event.timestamp);
            timerState.update(timerTimestamp);

            System.out.println("订单 " + event.orderId + " 创建，设置超时检测定时器");

        } else if ("PAY".equals(event.eventType)) {
            // 订单支付事件：取消定时器
            Long timer = timerState.value();
            if (timer != null) {
                ctx.timerService().deleteProcessingTimeTimer(timer);
                createTimeState.clear();
                timerState.clear();
                System.out.println("订单 " + event.orderId + " 已支付，取消超时检测");
            }
        }
    }

    @Override
    public void onTimer(long timestamp, OnTimerContext ctx, Collector<OrderTimeoutAlert> out)
            throws Exception {
        // 定时器触发，订单超时
        Long createTime = createTimeState.value();
        String orderId = ctx.getCurrentKey();

        out.collect(new OrderTimeoutAlert(orderId, createTime, "订单超时未支付"));

        // 清理状态
        createTimeState.clear();
        timerState.clear();
    }
}

// 使用示例：
/*
DataStream<OrderEvent> orderStream = env.fromElements(
    new OrderEvent("order1", "CREATE", System.currentTimeMillis()),
    new OrderEvent("order2", "CREATE", System.currentTimeMillis()),
    new OrderEvent("order1", "PAY", System.currentTimeMillis())
);

orderStream.keyBy(event -> event.orderId)
    .process(new OrderTimeoutDetection())
    .print("超时订单");
*/
*/
```

#### 高级编程题（L4-L5）

```java
/**
 * 题目：实现动态规则风控引擎
 * 要求：
 * 1. 支持动态规则更新（Broadcast State）
 * 2. 支持多种规则类型（金额、频率、地域）
 * 3. 满足延迟 < 100ms
 * 4. 保证 Exactly-Once
 *
 * 时间：120分钟
 */
public class DynamicRiskControlEngine
    extends KeyedBroadcastProcessFunction<String, TransactionEvent, RiskRule, RiskResult> {

    // Broadcast State描述器（存储动态规则，所有并行实例共享）
    public static final MapStateDescriptor<String, RiskRule> ruleStateDescriptor =
        new MapStateDescriptor<>("rules", String.class, RiskRule.class);

    // Keyed State：用户交易计数（用于频率检测）
    private ValueState<Integer> transactionCountState;
    // Keyed State：用户累计金额（用于金额检测）
    private ValueState<Double> totalAmountState;
    // Keyed State：上次交易时间（用于窗口清理）
    private ValueState<Long> lastTimestampState;

    @Override
    public void open(Configuration parameters) {
        // 初始化Keyed State
        transactionCountState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("count", Integer.class));
        totalAmountState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("amount", Double.class));
        lastTimestampState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("lastTime", Long.class));
    }

    @Override
    public void processElement(TransactionEvent event, ReadOnlyContext ctx,
                               Collector<RiskResult> out) throws Exception {

        // 获取所有广播的规则
        ReadOnlyBroadcastState<String, RiskRule> rules =
            ctx.getBroadcastState(ruleStateDescriptor);

        // 检查每条启用的规则
        for (Map.Entry<String, RiskRule> entry : rules.immutableEntries()) {
            RiskRule rule = entry.getValue();
            if (!rule.enabled) continue;

            switch (rule.ruleType) {
                case "AMOUNT":
                    checkAmountRule(event, rule, out);
                    break;
                case "FREQUENCY":
                    checkFrequencyRule(event, rule, out);
                    break;
                case "REGION":
                    checkRegionRule(event, rule, out);
                    break;
            }
        }

        // 更新用户状态
        updateState(event);
    }

    // 金额规则检查
    private void checkAmountRule(TransactionEvent event, RiskRule rule,
                                  Collector<RiskResult> out) {
        if (event.amount > rule.threshold) {
            out.collect(new RiskResult(
                event.userId, rule.ruleId, "AMOUNT",
                event.amount, rule.threshold, true));
        }
    }

    // 频率规则检查
    private void checkFrequencyRule(TransactionEvent event, RiskRule rule,
                                     Collector<RiskResult> out) throws Exception {
        Integer count = transactionCountState.value();
        if (count == null) count = 0;

        // 简单的频率检查（实际应用需要滑动窗口）
        if (count + 1 > rule.threshold) {
            out.collect(new RiskResult(
                event.userId, rule.ruleId, "FREQUENCY",
                count + 1, rule.threshold, true));
        }
        transactionCountState.update(count + 1);
    }

    // 地域规则检查（示例）
    private void checkRegionRule(TransactionEvent event, RiskRule rule,
                                  Collector<RiskResult> out) {
        // 简化示例：高风险地域列表检查
        String[] highRiskRegions = {"region_a", "region_b"};
        for (String region : highRiskRegions) {
            if (region.equals(event.region)) {
                out.collect(new RiskResult(
                    event.userId, rule.ruleId, "REGION",
                    0, 0, true));
                break;
            }
        }
    }

    // 更新用户状态
    private void updateState(TransactionEvent event) throws Exception {
        Double total = totalAmountState.value();
        if (total == null) total = 0.0;
        totalAmountState.update(total + event.amount);
        lastTimestampState.update(event.timestamp);
    }

    @Override
    public void processBroadcastElement(RiskRule rule, Context ctx,
                                       Collector<RiskResult> out) throws Exception {
        // 更新规则（动态广播）
        BroadcastState<String, RiskRule> broadcastState =
            ctx.getBroadcastState(ruleStateDescriptor);
        broadcastState.put(rule.ruleId, rule);
        System.out.println("规则更新: " + rule.ruleId + " 类型: " + rule.ruleType);
    }
}

// **参考答案**：动态规则风控引擎实现
/*
import org.apache.flink.api.common.state.*;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.datastream.BroadcastStream;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.co.KeyedBroadcastProcessFunction;
import org.apache.flink.util.Collector;

import java.util.Map;

// 交易事件
class TransactionEvent {
    String userId;
    double amount;
    String region;
    long timestamp;

    public TransactionEvent(String userId, double amount, String region, long timestamp) {
        this.userId = userId;
        this.amount = amount;
        this.region = region;
        this.timestamp = timestamp;
    }
}

// 风控规则
class RiskRule {
    String ruleId;
    String ruleType;  // "AMOUNT", "FREQUENCY", "REGION"
    double threshold;
    long timeWindow;  // 毫秒
    boolean enabled;

    public RiskRule(String ruleId, String ruleType, double threshold, long timeWindow) {
        this.ruleId = ruleId;
        this.ruleType = ruleType;
        this.threshold = threshold;
        this.timeWindow = timeWindow;
        this.enabled = true;
    }
}

// 风控结果
class RiskResult {
    String userId;
    String ruleId;
    String ruleType;
    double currentValue;
    double threshold;
    boolean isRisk;
    long timestamp;

    public RiskResult(String userId, String ruleId, String ruleType,
                     double currentValue, double threshold, boolean isRisk) {
        this.userId = userId;
        this.ruleId = ruleId;
        this.ruleType = ruleType;
        this.currentValue = currentValue;
        this.threshold = threshold;
        this.isRisk = isRisk;
        this.timestamp = System.currentTimeMillis();
    }
}

public class DynamicRiskControlEngine extends KeyedBroadcastProcessFunction<
    String, TransactionEvent, RiskRule, RiskResult> {

    // Broadcast State描述器（存储动态规则）
    private static final MapStateDescriptor<String, RiskRule> ruleStateDescriptor =
        new MapStateDescriptor<>("rules", String.class, RiskRule.class);

    // Keyed State：用户交易计数（用于频率检测）
    private ValueState<Integer> transactionCountState;
    // Keyed State：用户累计金额（用于金额检测）
    private ValueState<Double> totalAmountState;
    // Keyed State：上次交易时间（用于窗口清理）
    private ValueState<Long> lastTimestampState;

    @Override
    public void open(Configuration parameters) {
        transactionCountState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("count", Integer.class));
        totalAmountState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("amount", Double.class));
        lastTimestampState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("lastTime", Long.class));
    }

    @Override
    public void processElement(TransactionEvent event, ReadOnlyContext ctx,
                               Collector<RiskResult> out) throws Exception {

        // 获取所有广播的规则
        ReadOnlyBroadcastState<String, RiskRule> rules = ctx.getBroadcastState(ruleStateDescriptor);

        // 检查每条启用的规则
        for (Map.Entry<String, RiskRule> entry : rules.immutableEntries()) {
            RiskRule rule = entry.getValue();
            if (!rule.enabled) continue;

            switch (rule.ruleType) {
                case "AMOUNT":
                    checkAmountRule(event, rule, out);
                    break;
                case "FREQUENCY":
                    checkFrequencyRule(event, rule, out);
                    break;
                case "REGION":
                    checkRegionRule(event, rule, out);
                    break;
            }
        }

        // 更新状态
        updateState(event);
    }

    // 金额规则检查
    private void checkAmountRule(TransactionEvent event, RiskRule rule,
                                  Collector<RiskResult> out) {
        if (event.amount > rule.threshold) {
            out.collect(new RiskResult(
                event.userId, rule.ruleId, "AMOUNT",
                event.amount, rule.threshold, true));
        }
    }

    // 频率规则检查
    private void checkFrequencyRule(TransactionEvent event, RiskRule rule,
                                     Collector<RiskResult> out) throws Exception {
        Integer count = transactionCountState.value();
        if (count == null) count = 0;

        // 简单的频率检查（实际应用需要滑动窗口）
        if (count + 1 > rule.threshold) {
            out.collect(new RiskResult(
                event.userId, rule.ruleId, "FREQUENCY",
                count + 1, rule.threshold, true));
        }
        transactionCountState.update(count + 1);
    }

    // 地域规则检查（示例）
    private void checkRegionRule(TransactionEvent event, RiskRule rule,
                                  Collector<RiskResult> out) {
        // 简化示例：高风险地域列表检查
        String[] highRiskRegions = {"region_a", "region_b"};
        for (String region : highRiskRegions) {
            if (region.equals(event.region)) {
                out.collect(new RiskResult(
                    event.userId, rule.ruleId, "REGION",
                    0, 0, true));
                break;
            }
        }
    }

    private void updateState(TransactionEvent event) throws Exception {
        Double total = totalAmountState.value();
        if (total == null) total = 0.0;
        totalAmountState.update(total + event.amount);
        lastTimestampState.update(event.timestamp);
    }

    @Override
    public void processBroadcastElement(RiskRule rule, Context ctx,
                                       Collector<RiskResult> out) throws Exception {
        // 更新规则（动态广播）
        BroadcastState<String, RiskRule> broadcastState = ctx.getBroadcastState(ruleStateDescriptor);
        broadcastState.put(rule.ruleId, rule);
        System.out.println("规则更新: " + rule.ruleId + " 类型: " + rule.ruleType);
    }
}

// 使用示例：
/*
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// 交易流
DataStream<TransactionEvent> transactionStream = env
    .addSource(new TransactionSource())
    .keyBy(event -> event.userId);

// 规则流（模拟动态规则更新）
DataStream<RiskRule> ruleStream = env
    .fromElements(
        new RiskRule("rule1", "AMOUNT", 10000, 60000),
        new RiskRule("rule2", "FREQUENCY", 5, 60000)
    )
    .broadcast(DynamicRiskControlEngine.ruleStateDescriptor);

// 连接两个流
transactionStream
    .connect(ruleStream)
    .process(new DynamicRiskControlEngine())
    .print("风险告警");

env.execute("Dynamic Risk Control");
*/

// 设计要点说明：
// 1. Broadcast State：用于存储动态规则，所有并行实例共享
// 2. Keyed State：每个用户独立的状态，用于频率/金额累计
// 3. Exactly-Once：Flink的Checkpoint机制保证状态一致性
// 4. 延迟优化：使用异步IO可进一步优化外部查询延迟
*/
```

### 3. 架构设计考核

#### 架构设计题（L6）

```markdown
【设计题】设计一个支撑日活 1 亿的实时推荐系统

背景：
- 日活用户 1 亿
- 日均 PV 10 亿
- 推荐延迟 < 50ms
- 支持 A/B 测试

要求：
1. 绘制系统架构图
2. 说明关键技术选型
3. 描述数据流
4. 说明扩展性设计

时间：180分钟
```

### 4. 故障排查考核

#### 故障排查题

```markdown
【故障排查】作业频繁重启，Checkpoint 超时

症状：
- 作业每 10 分钟重启一次
- Checkpoint 耗时 > 5 分钟
- TaskManager OOM

日志：
```

2026-04-04 10:00:01 ERROR Checkpoint failure
java.util.concurrent.TimeoutException: Checkpoint expired
...
2026-04-04 10:05:00 ERROR OutOfMemoryError: Java heap space

```

请分析原因并给出解决方案。

时间：30分钟
```

---

## 考核题库建设

### 题库分类

```
题库/
├── 基础理论/
│   ├── 概念理解/
│   ├── 架构原理/
│   └── API使用/
├── 编程实践/
│   ├── DataStream/
│   ├── SQL/
│   └── 综合项目/
├── 架构设计/
│   ├── 系统设计/
│   ├── 性能优化/
│   └── 故障排查/
└── 场景应用/
    ├── 金融/
    ├── 电商/
    └── IoT/
```

### 题目模板

```yaml
题目ID: Q001
类型: 单选题
难度: L2
知识点:
  - Checkpoint
  - 容错机制
题干: |
  以下关于 Checkpoint 的说法正确的是：
选项:
  A: Checkpoint 间隔越短越好
  B: Checkpoint 可以保证端到端 Exactly-Once
  C: Checkpoint 主要用于故障恢复
  D: Checkpoint 会增加数据处理延迟
答案: C
解析: |
  A - 错误，间隔太短会影响性能
  B - 错误，端到端一致性需要配合两阶段提交
  C - 正确，Checkpoint 主要用于故障恢复
  D - 不完全正确，对齐 Checkpoint 会阻塞处理
```

---

## 考核实施流程

### 1. 考前准备

```
阶段1：制定考核方案
├── 确定考核目标
├── 确定考核形式
├── 确定考核范围
└── 制定评分标准

阶段2：准备考核材料
├── 编写试题
├── 准备编程环境
├── 准备评分标准
└── 通知参考人员

阶段3：环境检查
├── 检查考试环境
├── 测试编程环境
├── 验证试题
└── 培训监考人员
```

### 2. 考核执行

```
理论考核：
├── 发布试题
├── 监控考试
├── 收回答卷
└── 密封处理

编程考核：
├── 发布题目
├── 提供环境
├── 监控进度
└── 收集代码

架构考核：
├── 发布题目
├── 提供画图工具
├── 收集方案
└── 组织答辩
```

### 3. 评分与反馈

```
评分流程：
├── 制定评分细则
├── 组织阅卷
├── 交叉验证
├── 汇总成绩
└── 生成报告

反馈内容：
├── 总体评价
├── 分项得分
├── 优势分析
├── 改进建议
└── 学习路径推荐
```

---

## 评分标准

### 等级评定

| 分数 | 等级 | 评价 |
|------|------|------|
| 90-100 | 优秀 | 完全掌握，可指导他人 |
| 80-89 | 良好 | 扎实掌握，可独立工作 |
| 70-79 | 合格 | 基本掌握，需少量指导 |
| 60-69 | 待提升 | 部分掌握，需要培训 |
| <60 | 不合格 | 需要系统学习 |

### 分项权重

```
L1-L2 考核：
- 理论：50%
- 编程：50%

L3-L4 考核：
- 理论：30%
- 编程：50%
- 故障排查：20%

L5-L6 考核：
- 理论：20%
- 编程：40%
- 架构设计：30%
- 故障排查：10%
```

---

## 考核工具

### 在线考试系统

```markdown
推荐工具：
1. 问卷星 - 简单选择题考试
2. 考试酷 - 支持多种题型
3. 自建系统 - 深度定制

功能需求：
- 随机抽题
- 限时考试
- 自动阅卷
- 成绩统计
```

### 编程考核环境

```markdown
推荐方案：
1. Jupyter + Flink Kernel
2. 在线 IDE（如 CodeSandbox）
3. 自建评测系统

环境要求：
- Flink 1.17+
- JDK 11+
- Maven 3.6+
- 预置示例数据
```

---

## 持续改进

### 题库维护

```
定期更新：
- 每季度更新 20% 题目
- 移除过时题目
- 添加新知识点

质量评估：
- 分析通过率
- 收集反馈意见
- 优化题目难度
```

### 考核效果评估

```
评估指标：
- 通过率
- 成绩分布
- 与实际能力匹配度
- 培训效果相关性

改进措施：
- 调整题目难度
- 优化考核形式
- 完善评分标准
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-04-04 | 初始版本，自定义考核体系 |
