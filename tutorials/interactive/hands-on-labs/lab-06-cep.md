# Lab 6: CEP 模式匹配

> 所属阶段: Flink/Hands-on | 前置依赖: [Lab 5](./lab-05-checkpoint.md) | 预计时间: 90分钟 | 形式化等级: L4

## 实验目标

- [x] 理解 Flink CEP (Complex Event Processing) 概念
- [x] 掌握模式定义语法
- [x] 学会检测复杂事件序列
- [x] 掌握 CEP 的时间约束和条件

## 前置知识

- Lab 5 的 Checkpoint 机制
- 正则表达式基础
- 事件序列分析概念

## CEP 核心概念

```
CEP = 模式(Pattern) + 匹配(Match) + 复杂事件(Complex Event)
```

| 概念 | 说明 |
|------|------|
| Pattern | 定义要匹配的事件序列规则 |
| Quantifier | 量词（next, followedBy, times, etc.） |
| Condition | 事件匹配条件 |
| Time Constraint | 时间窗口约束 |
| Select Function | 从匹配中提取结果 |

## 实验步骤

### 步骤 1: 基础模式匹配

```java
package com.example;

import org.apache.flink.cep.CEP;
import org.apache.flink.cep.PatternStream;
import org.apache.flink.cep.pattern.Pattern;
import org.apache.flink.cep.pattern.conditions.SimpleCondition;
import org.apache.flink.streaming.api.datastream.DataStream;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.time.Time;


public class BasicCEPExample {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        // 输入事件流
        DataStream<LoginEvent> loginEvents = env
            .addSource(new LoginEventSource())
            .assignTimestampsAndWatermarks(...);

        // 定义模式:连续3次登录失败
        Pattern<LoginEvent, ?> loginFailPattern = Pattern
            .<LoginEvent>begin("first")      // 第一个事件
            .where(new SimpleCondition<LoginEvent>() {
                @Override
                public boolean filter(LoginEvent event) {
                    return event.status.equals("FAIL");
                }
            })
            .next("second")                   // 紧接着第二个
            .where(new SimpleCondition<LoginEvent>() {
                @Override
                public boolean filter(LoginEvent event) {
                    return event.status.equals("FAIL");
                }
            })
            .next("third")                    // 紧接着第三个
            .where(new SimpleCondition<LoginEvent>() {
                @Override
                public boolean filter(LoginEvent event) {
                    return event.status.equals("FAIL");
                }
            })
            .within(Time.seconds(10));        // 10秒内完成

        // 应用模式
        PatternStream<LoginEvent> patternStream = CEP.pattern(
            loginEvents.keyBy(LoginEvent::getUserId),
            loginFailPattern
        );

        // 处理匹配结果
        patternStream
            .process(new PatternProcessFunction<LoginEvent, Alert>() {
                @Override
                public void processMatch(
                        Map<String, List<LoginEvent>> match,
                        Context ctx,
                        Collector<Alert> out) {

                    LoginEvent first = match.get("first").get(0);
                    LoginEvent second = match.get("second").get(0);
                    LoginEvent third = match.get("third").get(0);

                    out.collect(new Alert(
                        first.userId,
                        "BRUTE_FORCE_ATTACK",
                        String.format("3 failed logins within 10s: %s, %s, %s",
                            first.ip, second.ip, third.ip),
                        ctx.timestamp()
                    ));
                }
            })
            .print();

        env.execute("Basic CEP Example");
    }
}
```

### 步骤 2: 量词使用

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.windowing.time.Time;

// 使用量词简化模式定义
Pattern<LoginEvent, ?> loginFailPattern = Pattern
    .<LoginEvent>begin("fail")
    .where(new SimpleCondition<LoginEvent>() {
        @Override
        public boolean filter(LoginEvent event) {
            return event.status.equals("FAIL");
        }
    })
    .times(3)                    // 精确3次
    .within(Time.seconds(10));

// 其他量词示例
Pattern<Transaction, ?> fraudPattern = Pattern
    // 至少2次
    .<Transaction>begin("small").where(t -> t.amount < 100).timesOrMore(2)
    // 后跟1-3次大额交易
    .next("large").where(t -> t.amount > 10000).times(1, 3)
    .within(Time.minutes(5));

// 可选事件
Pattern<Event, ?> optionalPattern = Pattern
    .<Event>begin("start")
    .next("middle").optional()    // 可选
    .next("end")
    .within(Time.minutes(1));

// 贪婪匹配
Pattern<Event, ?> greedyPattern = Pattern
    .<Event>begin("start")
    .where(e -> e.type.equals("A"))
    .oneOrMore().greedy()         // 贪婪匹配尽可能多的A
    .next("end")
    .where(e -> e.type.equals("B"));
```

### 步骤 3: 时间约束与模式

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.windowing.time.Time;

// 严格连续 (next): 事件必须紧邻
Pattern<Event, ?> strictPattern = Pattern
    .<Event>begin("first")
    .next("second")  // 严格连续,中间不能有其他事件
    .next("third");

// 宽松连续 (followedBy): 中间可以有其他事件
Pattern<Event, ?> relaxedPattern = Pattern
    .<Event>begin("first")
    .followedBy("second")  // first和second之间可以有其他事件
    .followedBy("third");

// 非确定性宽松 (followedByAny)
Pattern<Event, ?> nonDetPattern = Pattern
    .<Event>begin("first")
    .followedByAny("second")  // 匹配所有可能的组合
    .followedByAny("third");

// 非连续 (notNext, notFollowedBy)
Pattern<Event, ?> absencePattern = Pattern
    .<Event>begin("start")
    .notFollowedBy("cancel")   // start后不能有cancel
    .followedBy("complete")
    .within(Time.hours(1));
```

### 步骤 4: 迭代条件

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.windowing.time.Time;

// 使用迭代条件检测上升趋势
Pattern<StockPrice, ?> risingPattern = Pattern
    .<StockPrice>begin("start")
    .where(new IterativeCondition<StockPrice>() {
        @Override
        public boolean filter(StockPrice price, Context<StockPrice> ctx) {
            return price.change > 0;  // 初始条件
        }
    })
    .next("middle")
    .oneOrMore()
    .where(new IterativeCondition<StockPrice>() {
        @Override
        public boolean filter(StockPrice price, Context<StockPrice> ctx) {
            // 访问之前匹配的事件
            for (StockPrice p : ctx.getEventsForPattern("middle")) {
                if (price.price <= p.price) {
                    return false;  // 价格必须持续上涨
                }
            }
            // 与start比较
            for (StockPrice p : ctx.getEventsForPattern("start")) {
                if (price.price <= p.price) {
                    return false;
                }
            }
            return true;
        }
    })
    .next("peak")
    .where(new SimpleCondition<StockPrice>() {
        @Override
        public boolean filter(StockPrice price) {
            return price.change < 0;  // 上涨结束
        }
    })
    .within(Time.minutes(30));
```

### 步骤 5: 处理超时和旁路输出

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

// 定义超时标签
OutputTag<TimeoutEvent> timeoutTag = new OutputTag<TimeoutEvent>("timeout"){};

Pattern<Event, ?> pattern = Pattern
    .<Event>begin("start")
    .next("middle")
    .optional()
    .next("end")
    .within(Time.seconds(5));  // 5秒超时

PatternStream<Event> patternStream = CEP.pattern(input, pattern);

// 使用 PatternTimeoutFunction 处理超时
SingleOutputStreamOperator<Result> result = patternStream
    .process(new PatternProcessFunction<Event, Result>() {
        @Override
        public void processMatch(
                Map<String, List<Event>> match,
                Context ctx,
                Collector<Result> out) {
            // 处理正常匹配
            out.collect(new Result(match, false));
        }
    })
    .timeout(new PatternTimeoutFunction<Event, TimeoutResult>() {
        @Override
        public TimeoutResult timeout(
                Map<String, List<Event>> partialMatch,
                long timeoutTimestamp) {
            // 处理超时
            return new TimeoutResult(partialMatch, timeoutTimestamp);
        }
    }, timeoutTag);

// 获取超时输出
DataStream<TimeoutResult> timeoutStream = result.getSideOutput(timeoutTag);
```

### 步骤 6: 复杂场景 - 订单欺诈检测

```java

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

public class FraudDetectionCEP {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        DataStream<Transaction> transactions = env
            .addSource(new TransactionSource())
            .assignTimestampsAndWatermarks(...);

        // 模式1: 短时间内多地大额交易
        Pattern<Transaction, ?> multiLocationPattern = Pattern
            .<Transaction>begin("first")
            .where(t -> t.amount > 1000)
            .next("second")
            .where(t -> t.amount > 1000)
            .where(new IterativeCondition<Transaction>() {
                @Override
                public boolean filter(Transaction t, Context<Transaction> ctx) {
                    // 检查地点不同
                    Collection<Transaction> first =
                        ctx.getEventsForPattern("first");
                    for (Transaction f : first) {
                        if (!f.location.equals(t.location) &&
                            Math.abs(t.timestamp - f.timestamp) < 300000) { // 5分钟内
                            return true;
                        }
                    }
                    return false;
                }
            })
            .within(Time.minutes(10));

        // 模式2: 小额测试后大额交易
        Pattern<Transaction, ?> testThenLargePattern = Pattern
            .<Transaction>begin("test")
            .where(t -> t.amount < 10)  // 小额测试
            .next("wait")
            .where(t -> t.amount > 5000)  // 大额交易
            .within(Time.hours(1));

        // 应用多个模式
        PatternStream<Transaction> patternStream = CEP.pattern(
            transactions.keyBy(t -> t.userId),
            Pattern.<Transaction>begin("fraud")
                .or(multiLocationPattern)
                .or(testThenLargePattern)
        );

        patternStream
            .process(new FraudAlertHandler())
            .addSink(new AlertSink());

        env.execute("Fraud Detection CEP");
    }
}
```

## 验证方法

### 检查清单

- [ ] 理解 next/followedBy/followedByAny 的区别
- [ ] 掌握 times/oneOrMore/optional 等量词
- [ ] 能够使用 IterativeCondition 访问历史事件
- [ ] 理解 within 时间约束
- [ ] 能够处理超时和部分匹配

### 测试用例

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.windowing.time.Time;

@Test
public void testLoginFailurePattern() throws Exception {
    // 创建测试数据
    List<LoginEvent> events = Arrays.asList(
        new LoginEvent("user1", "FAIL", 1000L),
        new LoginEvent("user1", "FAIL", 2000L),
        new LoginEvent("user1", "FAIL", 3000L),  // 应该匹配
        new LoginEvent("user1", "SUCCESS", 4000L)
    );

    // 创建模式
    Pattern<LoginEvent, ?> pattern = Pattern
        .<LoginEvent>begin("fail").where(e -> e.status.equals("FAIL"))
        .times(3)
        .within(Time.seconds(10));

    // 测试匹配
    PatternProcessFunction<LoginEvent, Alert> processFunction =
        new LoginFailureHandler();

    // 验证输出包含告警
    // ...
}
```

## 扩展练习

### 练习 1: 实时营销场景

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.windowing.time.Time;

// 购物车放弃检测
Pattern<UserAction, ?> cartAbandonmentPattern = Pattern
    .<UserAction>begin("add")
    .where(a -> a.action.equals("ADD_TO_CART"))
    .followedBy("browse")
    .where(a -> a.action.equals("BROWSE"))
    .oneOrMore()
    .notFollowedBy("checkout")   // 没有结账
    .within(Time.hours(2));

// 优惠卷使用模式
Pattern<UserAction, ?> couponPattern = Pattern
    .<UserAction>begin("view")
    .where(a -> a.action.equals("VIEW_PRODUCT"))
    .timesOrMore(3)
    .followedBy("coupon")
    .where(a -> a.action.equals("APPLY_COUPON"))
    .within(Time.minutes(30));
```

### 练习 2: IoT 设备异常检测

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.windowing.time.Time;

// 设备故障模式:温度持续上升后突然停止报告
Pattern<SensorReading, ?> failurePattern = Pattern
    .<SensorReading>begin("rising")
    .where(r -> r.temperature > 50)
    .oneOrMore()
    .where(new IterativeCondition<SensorReading>() {
        @Override
        public boolean filter(SensorReading r, Context<SensorReading> ctx) {
            // 温度持续上升
            for (SensorReading prev : ctx.getEventsForPattern("rising")) {
                if (r.temperature <= prev.temperature) {
                    return false;
                }
            }
            return true;
        }
    })
    .notFollowedBy("report")
    .where(r -> r.timestamp - getLastTimestamp(ctx) < 60000)
    .within(Time.minutes(5));
```

## 最佳实践

1. **尽早过滤**: 在 Pattern 前使用 filter 减少数据量
2. **合理设置时间窗口**: 窗口太大导致状态膨胀，太小可能错过匹配
3. **使用 keyed stream**: CEP 必须在 keyed stream 上使用
4. **注意状态清理**: 长时间未完成的模式会占用内存
5. **避免过于复杂的模式**: 复杂模式影响性能，可拆分为多个简单模式

## 性能考虑

| 因素 | 建议 |
|------|------|
| 模式复杂度 | 保持简单，避免过多迭代条件 |
| 时间窗口 | 根据业务需求设置合理值 |
| Key 选择 | 选择高基数字段作为 key |
| 状态大小 | 监控 CEP 状态大小，必要时调优 |

## 下一步

- [测验：综合测试](../quizzes/comprehensive-test.md)
- [编程挑战](../coding-challenges/README.md)

## 引用参考
