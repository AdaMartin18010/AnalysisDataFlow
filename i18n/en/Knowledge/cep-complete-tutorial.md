---
title: "[EN] Cep Complete Tutorial"
translation_status: "ai_translated"
source_file: "Knowledge/cep-complete-tutorial.md"
source_version: "8e8f8f15"
translator: "AI"
reviewer: null
translated_at: "2026-04-08T15:15:06.334005"
reviewed_at: null
quality_score: null
terminology_verified: false
---


<!-- AI Translation Template - Replace <!-- TRANSLATE --> markers with actual translation -->

<!-- TRANSLATE: # CEP (Complex Event Processing) 完整教程 -->

<!-- TRANSLATE: > 所属阶段: Knowledge | 前置依赖: [Flink/time-semantics-and-watermark.md](../../../Flink/02-core/time-semantics-and-watermark.md) | 形式化等级: L4 -->


<!-- TRANSLATE: ## 2. 属性推导 (Properties) -->

<!-- TRANSLATE: ### Lemma-K-CEP-01: 模式匹配完备性 -->

**引理**: 给定模式 $P$ 和事件流 $E$，CEP 引擎可找到所有满足 $P$ 的事件子序列。

<!-- TRANSLATE: **证明概要**： -->

<!-- TRANSLATE: 1. 使用 NFA（非确定性有限自动机）建模模式 -->
<!-- TRANSLATE: 2. 每个事件驱动状态转换 -->
<!-- TRANSLATE: 3. 到达接受状态时输出匹配 -->
<!-- TRANSLATE: 4. 回溯机制保证不遗漏任何可能匹配 -->

<!-- TRANSLATE: ### Lemma-K-CEP-02: 时间窗口约束 -->

**引理**: 时间窗口 $T$ 限制了模式匹配的时间跨度：

$$
<!-- TRANSLATE: \text{Match}(S, P) \Rightarrow t_{last} - t_{first} \leq T_{window} -->
$$

<!-- TRANSLATE: **超时处理**： -->

<!-- TRANSLATE: - 部分匹配在窗口超时时被丢弃 -->
<!-- TRANSLATE: - 超时事件可触发超时告警（通过 `within` 和 `timeout` 标签） -->

<!-- TRANSLATE: ### Prop-K-CEP-01: 状态空间复杂度 -->

<!-- TRANSLATE: **命题**: 模式匹配的状态空间与模式长度和事件类型数成线性关系。 -->

$$
<!-- TRANSLATE: \text{Space} = O(|P| \times |E_{types}|) -->
$$

<!-- TRANSLATE: 其中： -->

- $|P|$: 模式阶段数
- $|E_{types}|$: 事件类型数


<!-- TRANSLATE: ## 4. 论证过程 (Argumentation) -->

<!-- TRANSLATE: ### 4.1 连续性策略选择 -->

<!-- TRANSLATE: **决策矩阵**： -->

<!-- TRANSLATE: | 策略 | 优点 | 缺点 | 适用场景 | -->
<!-- TRANSLATE: |------|------|------|----------| -->
<!-- TRANSLATE: | next | 精确匹配，性能高 | 容易漏匹配 | 严格顺序要求 | -->
<!-- TRANSLATE: | followedBy | 灵活，容错性高 | 可能匹配过多 | 一般业务流程 | -->
<!-- TRANSLATE: | followedByAny | 捕获所有可能 | 状态爆炸风险 | 需要全部匹配 | -->

<!-- TRANSLATE: ### 4.2 时间窗口设计 -->

<!-- TRANSLATE: **窗口大小权衡**： -->

<!-- TRANSLATE: | 窗口大小 | 优点 | 缺点 | -->
<!-- TRANSLATE: |----------|------|------| -->
<!-- TRANSLATE: | 小（秒级） | 低延迟，少误报 | 可能漏慢速攻击 | -->
<!-- TRANSLATE: | 中（分钟级） | 平衡 | 中等状态开销 | -->
<!-- TRANSLATE: | 大（小时级） | 捕获长期模式 | 高状态开销，延迟高 | -->


<!-- TRANSLATE: ## 6. 实例验证 (Examples) -->

<!-- TRANSLATE: ### 6.1 Maven 依赖 -->

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-cep</artifactId>
    <version>1.17.0</version>
</dependency>
```

<!-- TRANSLATE: ### 6.2 欺诈检测模式示例 -->

```java
import org.apache.flink.cep.Pattern;
import org.apache.flink.cep.CEP;
import org.apache.flink.cep.pattern.conditions.SimpleCondition;

import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;


// 定义欺诈检测模式：小额测试后大额交易
Pattern<Transaction, ?> fraudPattern = Pattern
    .<Transaction>begin("small-amount")
    .where(new SimpleCondition<Transaction>() {
        @Override
        public boolean filter(Transaction tx) {
            return tx.getAmount() < 10.0;  // 小额测试
        }
    })
    .followedBy("large-amount")
    .where(new SimpleCondition<Transaction>() {
        @Override
        public boolean filter(Transaction tx) {
            return tx.getAmount() > 1000.0;  // 大额交易
        }
    })
    // 同一用户，10分钟内
    .where(new SimpleCondition<Transaction>() {
        @Override
        public boolean filter(Transaction tx) {
            return tx.getUserId().equals(
                ctx.getEventsForPattern("small-amount")
                   .get(0).getUserId()
            );
        }
    })
    .within(Time.minutes(10));

// 应用到流
DataStream<Transaction> txStream = ...;
PatternStream<Transaction> patternStream = CEP.pattern(txStream, fraudPattern);

// 处理匹配结果
DataStream<Alert> alerts = patternStream
    .select(new PatternSelectFunction<Transaction, Alert>() {
        @Override
        public Alert select(Map<String, List<Transaction>> pattern) {
            Transaction small = pattern.get("small-amount").get(0);
            Transaction large = pattern.get("large-amount").get(0);
            return new Alert(small.getUserId(), "FRAUD_PATTERN",
                "Small: " + small.getAmount() + ", Large: " + large.getAmount());
        }
    });
```

<!-- TRANSLATE: ### 6.3 异常登录检测模式 -->

```java

import org.apache.flink.streaming.api.windowing.time.Time;

// 3分钟内 5 次失败登录后 1 次成功登录
Pattern<LoginEvent, ?> suspiciousLogin = Pattern
    .<LoginEvent>begin("failed-logins")
    .where(new SimpleCondition<LoginEvent>() {
        @Override
        public boolean filter(LoginEvent event) {
            return !event.isSuccess();
        }
    })
    .timesOrMore(5)
    .greedy()
    .followedBy("success-login")
    .where(new SimpleCondition<LoginEvent>() {
        @Override
        public boolean filter(LoginEvent event) {
            return event.isSuccess();
        }
    })
    .within(Time.minutes(3));

// 处理超时（未出现成功登录）
patternStream
    .process(new PatternProcessFunction<LoginEvent, Alert>() {
        @Override
        public void processMatch(Map<String, List<LoginEvent>> match,
                                 Context ctx, Collector<Alert> out) {
            // 处理匹配
        }

        @Override
        public void processTimedOutMatch(Map<String, List<LoginEvent>> match,
                                         Context ctx, Collector<Alert> out) {
            // 超时处理：多次失败登录但未成功
            out.collect(new Alert(match.get("failed-logins").get(0).getUserId(),
                "BRUTE_FORCE_ATTEMPT", "Multiple failed logins without success"));
        }
    });
```

<!-- TRANSLATE: ### 6.4 设备故障预测模式 -->

```java

import org.apache.flink.streaming.api.windowing.time.Time;

// 温度持续上升趋势后超过阈值
Pattern<SensorReading, ?> overheatingPattern = Pattern
    .<SensorReading>begin("first")
    .where(new SimpleCondition<SensorReading>() {
        @Override
        public boolean filter(SensorReading reading) {
            return reading.getTemperature() > 80;
        }
    })
    .next("second")
    .where(new IterativeCondition<SensorReading>() {
        @Override
        public boolean filter(SensorReading reading, Context<SensorReading> ctx) {
            double firstTemp = ctx.getEventsForPattern("first")
                .get(0).getTemperature();
            return reading.getTemperature() > firstTemp + 5;
        }
    })
    .next("third")
    .where(new IterativeCondition<SensorReading>() {
        @Override
        public boolean filter(SensorReading reading, Context<SensorReading> ctx) {
            double secondTemp = ctx.getEventsForPattern("second")
                .get(0).getTemperature();
            return reading.getTemperature() > secondTemp + 5;
        }
    })
    .within(Time.seconds(30));
```

<!-- TRANSLATE: ### 6.5 SQL MATCH_RECOGNIZE 等价写法 -->

```sql
-- 使用 SQL 模式识别（Flink SQL）
SELECT *
FROM transactions
MATCH_RECOGNIZE (
    PARTITION BY user_id
    ORDER BY event_time
    MEASURES
        A.amount AS small_amount,
        B.amount AS large_amount,
        A.event_time AS start_time
    ONE ROW PER MATCH
    PATTERN (A B)
    DEFINE
        A AS amount < 10,
        B AS amount > 1000
) MR;
```


<!-- TRANSLATE: ## 8. 引用参考 (References) -->
