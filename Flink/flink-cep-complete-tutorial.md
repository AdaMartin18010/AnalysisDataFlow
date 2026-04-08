# Flink CEP 完整教程 (Complete Tutorial)

> **所属阶段**: Flink/03-sql-table-api | **前置依赖**: [flink-cep-complete-guide.md](Flink/03-api/03.02-table-sql-api/flink-cep-complete-guide.md), [time-semantics-and-watermark.md](Flink/02-core/time-semantics-and-watermark.md) | **形式化等级**: L3-L4
> **版本**: Flink 1.13-2.2+ | **难度**: 中级-高级 | **预计阅读时间**: 90分钟

---

## 1. 概念定义 (Definitions)

### Def-F-CEP-Tutorial-01: CEP 核心概念

**复杂事件处理 (Complex Event Processing, CEP)** 是从事件流中检测复杂模式的技术：

$$
\text{CEP} = (E, P, \mathcal{M}, \mathcal{A})
$$

| 组件 | 说明 | Flink 实现 |
|------|------|-----------|
| $E$ | 事件流 | `DataStream<Event>` |
| $P$ | 模式定义 | `Pattern<T, ?>` |
| $\mathcal{M}$ | 匹配引擎 | NFA (非确定性有限自动机) |
| $\mathcal{A}$ | 匹配后动作 | `PatternSelectFunction` |

**CEP 处理流程**:

```
输入事件流 → Pattern API定义 → NFA状态机 → 匹配结果 → 业务动作
     ↓              ↓              ↓           ↓          ↓
  原始事件      模式规则       状态转换      复杂事件    告警/处理
```

### Def-F-CEP-Tutorial-02: Pattern API 核心元素

**Pattern API** 是 Flink CEP 的声明式模式定义接口：

```
Pattern<T, ?> = begin(name)
    → [where|subtype]
    → [next|followedBy|followedByAny]
    → [times|oneOrMore|optional]
    → [within]
```

**核心元素定义**:

| 元素 | 方法 | 语义 |
|------|------|------|
| **起始** | `begin(name)` | 模式起点，创建初始状态 |
| **条件** | `where(condition)` | 事件过滤条件 |
| **连续性** | `next()` / `followedBy()` | 事件间关系约束 |
| **量词** | `times(n,m)` | 循环匹配次数 |
| **时间** | `within(time)` | 模式时间窗口 |

### Def-F-CEP-Tutorial-03: NFA 模式匹配

**非确定性有限自动机 (NFA)** 是 CEP 的底层执行模型：

```
NFA = (Q, Σ, δ, q₀, F)
```

- $Q$: 状态集合（对应模式阶段）
- $Σ$: 输入字母表（事件类型）
- $δ$: 转移函数（事件驱动状态转换）
- $q₀$: 初始状态
- $F$: 接受状态（模式匹配完成）

**NFA 执行示例**:

```
Pattern: A → B → C

状态转换图:
    [Start] --A--> [State_A] --B--> [State_B] --C--> [Accept]
                      ↑_______|            ↑_________|
                      (循环等待)             (循环等待)
```

---

## 2. 属性推导 (Properties)

### Lemma-F-CEP-Tutorial-01: Pattern API 的闭包性质

**引理**: Pattern API 在组合操作下保持闭包性质。

**证明概要**:

1. **顺序组合**: `P1.next(P2)` 仍是有效 Pattern
2. **选择组合**: `P1.or(P2)` 仍是有效 Pattern
3. **循环组合**: `P1.times(n,m)` 仍是有效 Pattern

$$
\forall P_1, P_2 \in \text{Pattern}: P_1 \oplus P_2 \in \text{Pattern}
$$

### Lemma-F-CEP-Tutorial-02: 时间窗口的状态剪枝

**引理**: 时间窗口约束 `within(T)` 将 NFA 的活跃状态数上限从 $O(|E|)$ 降为 $O(T/\bar{\delta})$。

**推导**:

```
无时间窗口:
  每个事件可能启动新匹配
  活跃状态数 ∝ 事件总数 |E|

有时间窗口 T:
  只保留窗口内的事件
  活跃状态数 ∝ T / 平均事件间隔
```

### Prop-F-CEP-Tutorial-01: 连续性策略的匹配集合关系

**命题**: 三种连续性策略的匹配集合满足包含关系：

$$
\text{Matches}_{\text{next}} \subseteq \text{Matches}_{\text{followedBy}} \subseteq \text{Matches}_{\text{followedByAny}}
$$

**示例验证**:

```
事件流: [A, X, A, B, B, C]

Pattern: A → B → C

next():            无匹配 (A后无紧邻B)
followedBy():      匹配 [A(3), B(4), C(6)]
followedByAny():   匹配 [A(3), B(4), C(6)] 和 [A(3), B(5), C(6)]
```

---

## 3. 关系建立 (Relations)

### 3.1 CEP 与 SQL MATCH_RECOGNIZE 对比

| 特性 | Pattern API | SQL MATCH_RECOGNIZE |
|------|-------------|---------------------|
| **表达能力** | 图灵完备 | 正则类 |
| **使用方式** | Java/Scala API | SQL 声明式 |
| **动态模式** | 支持 | 不支持 |
| **匹配后处理** | 灵活（任意代码） | 受限（SQL投影） |
| **适用场景** | 复杂业务逻辑 | 简单模式识别 |

### 3.2 CEP 与流处理算子对比

```mermaid
graph TB
    subgraph "流处理算子"
        A[Filter] --> B[Map] --> C[Window] --> D[Aggregate]
    end

    subgraph "CEP 模式匹配"
        E[Event Stream] --> F[NFA Engine]
        F --> G[Pattern Match]
        G --> H[Complex Event]
    end

    subgraph "能力对比"
        D -->|聚合计算| I[统计结果]
        H -->|时序识别| J[业务事件]
    end

    style F fill:#e1f5fe
    style G fill:#fff3e0
```

### 3.3 Pattern API 与正则表达式映射

| 正则表达式 | Pattern API | 说明 |
|-----------|-------------|------|
| `a+` | `A.oneOrMore()` | 一次或多次 |
| `a?` | `A.optional()` | 零次或一次 |
| `a{n,m}` | `A.times(n, m)` | n 到 m 次 |
| `a\|b` | `A.or(B)` | 选择 |
| `ab` | `A.next(B)` | 紧邻序列 |
| `a.*b` | `A.followedBy(B)` | 宽松序列 |

---

## 4. 论证过程 (Argumentation)

### 4.1 连续性策略选择决策树

```mermaid
flowchart TD
    START([选择连续性策略])

    START --> Q1{事件必须紧邻?}
    Q1 -->|是| Q2{允许其他事件插入?}
    Q1 -->|否| Q3{需要所有匹配?}

    Q2 -->|否| NEXT[next<br/>严格连续]
    Q2 -->|是| Q4{多个后续事件?}

    Q3 -->|是| FBA[followedByAny<br/>非确定性宽松]
    Q3 -->|否| FB[followedBy<br/>宽松连续]

    Q4 -->|是| FBA
    Q4 -->|否| FB

    style NEXT fill:#ffebee
    style FB fill:#e8f5e9
    style FBA fill:#e3f2fd
```

### 4.2 时间窗口设计权衡

| 窗口大小 | 优点 | 缺点 | 适用场景 |
|----------|------|------|----------|
| **小 (<1分钟)** | 低延迟、少误报、低状态 | 可能漏慢速攻击 | 高频交易、实时风控 |
| **中 (1-10分钟)** | 平衡延迟与覆盖率 | 中等状态开销 | 常规业务监控 |
| **大 (>10分钟)** | 捕获长期模式 | 高状态、高延迟 | 业务流程分析 |

### 4.3 消耗策略选择指南

| 策略 | 输出匹配数 | 适用场景 |
|------|-----------|----------|
| `NO_SKIP` | 最多 | 需要所有可能匹配 |
| `SKIP_TO_NEXT` | 中等 | 从下一个起始事件开始 |
| `SKIP_PAST_LAST_EVENT` | 最少 | 避免重叠匹配 |
| `SKIP_TO_FIRST` | 可控 | 跳转到指定模式起点 |

---

## 5. 形式证明 / 工程论证 (Proof / Engineering Argument)

### Thm-F-CEP-Tutorial-01: CEP Exactly-Once 语义

**定理**: 在 Flink Checkpoint 机制下，CEP 模式匹配满足 Exactly-Once 语义。

**证明**:

1. **状态包含**: Checkpoint 保存 NFA 的完整状态
   - 活跃的状态实例
   - 部分匹配的事件序列
   - 时间窗口边界

2. **恢复一致性**: 从 Checkpoint 恢复后
   - NFA 状态与故障前一致
   - 已处理事件不会重放（Flink 保证）
   - 部分匹配从断点继续

3. **输出一致性**: 匹配结果只输出一次
   - 已输出的匹配在状态中标记
   - 恢复后不会重复输出

$$
\text{Output}_{\text{before_failure}} = \text{Output}_{\text{after_recovery}}
$$

### Thm-F-CEP-Tutorial-02: 模式匹配的时间复杂度

**定理**: 对于长度为 $n$ 的模式和事件流，CEP 匹配的时间复杂度为 $O(|E| \cdot n \cdot k)$，其中 $k$ 为最大并发匹配数。

**工程优化**:

1. **索引优化**: 按事件类型建立索引
2. **窗口剪枝**: 超时匹配自动清理
3. **状态压缩**: 相似匹配合并存储

---

## 6. 实例验证 (Examples)

### 6.1 Maven 依赖配置

```xml
<!-- Flink CEP 依赖 -->
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-cep</artifactId>
    <version>1.17.0</version>
</dependency>

<!-- Scala API (可选) -->
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-cep-scala_2.12</artifactId>
    <version>1.17.0</version>
</dependency>
```

### 6.2 基础 Pattern API 详解

#### 6.2.1 Java API 完整示例

```java
import org.apache.flink.cep.CEP;
import org.apache.flink.cep.PatternStream;
import org.apache.flink.cep.pattern.Pattern;
import org.apache.flink.cep.pattern.conditions.SimpleCondition;
import org.apache.flink.cep.pattern.conditions.IterativeCondition;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

public class CEPCompleteTutorial {

    // ========== 1. 基础模式定义 ==========

    /**
     * 示例 1: 简单序列模式
     * 检测：登录后 5 分钟内完成支付
     */
    public static Pattern<LoginEvent, ?> loginThenPayPattern() {
        return Pattern.<LoginEvent>begin("login")
            .where(new SimpleCondition<LoginEvent>() {
                @Override
                public boolean filter(LoginEvent event) {
                    return event.getType().equals("LOGIN");
                }
            })
            .followedBy("payment")
            .where(new SimpleCondition<LoginEvent>() {
                @Override
                public boolean filter(LoginEvent event) {
                    return event.getType().equals("PAYMENT");
                }
            })
            .within(Time.minutes(5));
    }

    /**
     * 示例 2: 循环模式
     * 检测：5 分钟内 3 次以上失败登录
     */
    public static Pattern<LoginEvent, ?> bruteForcePattern() {
        return Pattern.<LoginEvent>begin("failed")
            .where(new SimpleCondition<LoginEvent>() {
                @Override
                public boolean filter(LoginEvent event) {
                    return event.getType().equals("LOGIN") && !event.isSuccess();
                }
            })
            .timesOrMore(3)  // 3次或更多
            .greedy()        // 贪婪模式，尽可能多匹配
            .within(Time.minutes(5));
    }

    /**
     * 示例 3: 否定模式
     * 检测：下单后 30 分钟内未支付
     */
    public static Pattern<OrderEvent, ?> orderNotPaidPattern() {
        return Pattern.<OrderEvent>begin("order")
            .where(new SimpleCondition<OrderEvent>() {
                @Override
                public boolean filter(OrderEvent event) {
                    return event.getType().equals("ORDER_CREATED");
                }
            })
            .notFollowedBy("payment")
            .where(new SimpleCondition<OrderEvent>() {
                @Override
                public boolean filter(OrderEvent event) {
                    return event.getType().equals("PAYMENT");
                }
            })
            .within(Time.minutes(30));
    }

    // ========== 2. 复杂条件模式 ==========

    /**
     * 示例 4: 迭代条件（访问前面匹配的事件）
     * 检测：温度持续上升超过阈值
     */
    public static Pattern<SensorReading, ?> temperatureRisingPattern() {
        return Pattern.<SensorReading>begin("first")
            .where(new SimpleCondition<SensorReading>() {
                @Override
                public boolean filter(SensorReading reading) {
                    return reading.getTemperature() > 80.0;
                }
            })
            .next("second")
            .where(new IterativeCondition<SensorReading>() {
                @Override
                public boolean filter(SensorReading reading, Context<SensorReading> ctx) {
                    // 访问前面匹配的事件
                    double firstTemp = ctx.getEventsForPattern("first")
                        .get(0).getTemperature();
                    return reading.getTemperature() > firstTemp + 5.0;
                }
            })
            .next("third")
            .where(new IterativeCondition<SensorReading>() {
                @Override
                public boolean filter(SensorReading reading, Context<SensorReading> ctx) {
                    double secondTemp = ctx.getEventsForPattern("second")
                        .get(0).getTemperature();
                    return reading.getTemperature() > secondTemp + 5.0;
                }
            })
            .within(Time.minutes(10));
    }

    // ========== 3. 组合模式 ==========

    /**
     * 示例 5: 或组合模式
     * 检测：VIP用户的高额交易 或 普通用户的异常交易
     */
    public static Pattern<Transaction, ?> fraudPattern() {
        Pattern<Transaction, ?> vipPattern = Pattern.<Transaction>begin("vip")
            .where(new SimpleCondition<Transaction>() {
                @Override
                public boolean filter(Transaction tx) {
                    return tx.getUserType().equals("VIP") && tx.getAmount() > 50000;
                }
            });

        Pattern<Transaction, ?> normalPattern = Pattern.<Transaction>begin("normal")
            .where(new SimpleCondition<Transaction>() {
                @Override
                public boolean filter(Transaction tx) {
                    return tx.getUserType().equals("NORMAL") && tx.getAmount() > 10000;
                }
            });

        return Pattern.<Transaction>begin("start")
            .where(new SimpleCondition<Transaction>() {
                @Override
                public boolean filter(Transaction tx) {
                    return tx.getAmount() < 10;  // 小额试探
                }
            })
            .next("suspicious")
            .where(new SimpleCondition<Transaction>() {
                @Override
                public boolean filter(Transaction tx) {
                    return tx.getAmount() > 5000;
                }
            })
            .or(vipPattern)  // 或组合
            .within(Time.minutes(10));
    }
}
```

#### 6.2.2 Scala API 完整示例

```scala
import org.apache.flink.cep.scala.CEP
import org.apache.flink.cep.scala.pattern.Pattern
import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.api.windowing.time.Time

object CEPScalaTutorial {

  // 示例 1: 简单模式
  val loginPattern = Pattern.begin[LoginEvent]("login")
    .where(_.eventType == "LOGIN")
    .followedBy("payment")
    .where(_.eventType == "PAYMENT")
    .within(Time.minutes(5))

  // 示例 2: 循环模式
  val bruteForcePattern = Pattern.begin[LoginEvent]("failed")
    .where(evt => evt.eventType == "LOGIN" && !evt.success)
    .timesOrMore(3)
    .greedy()
    .within(Time.minutes(5))

  // 示例 3: 迭代条件
  val temperatureRisingPattern = Pattern.begin[SensorReading]("first")
    .where(_.temperature > 80.0)
    .next("second")
    .where((reading, ctx) => {
      val firstTemp = ctx.getEventsForPattern("first").head.temperature
      reading.temperature > firstTemp + 5.0
    })
    .next("third")
    .where((reading, ctx) => {
      val secondTemp = ctx.getEventsForPattern("second").head.temperature
      reading.temperature > secondTemp + 5.0
    })
    .within(Time.minutes(10))

  // 应用到流
  def applyPattern[T](stream: DataStream[T], pattern: Pattern[T, _]): Unit = {
    val patternStream = CEP.pattern(stream, pattern)

    patternStream.select(pattern => {
      // 处理匹配结果
      pattern.toString
    })
  }
}
```

### 6.3 实际案例详解

#### 6.3.1 欺诈检测完整实现

```java
/**
 * 案例：信用卡欺诈检测
 * 模式：小额测试 → 大额交易（5分钟内）
 */
public class FraudDetectionCEP {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(4);

        // 1. 创建事件流
        DataStream<Transaction> transactions = env
            .addSource(new TransactionSource())
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<Transaction>forBoundedOutOfOrderness(
                    Duration.ofSeconds(5))
                    .withIdleness(Duration.ofMinutes(1))
            );

        // 2. 定义欺诈检测模式
        Pattern<Transaction, ?> fraudPattern = Pattern
            .<Transaction>begin("small-amount")
            .where(new SimpleCondition<Transaction>() {
                @Override
                public boolean filter(Transaction tx) {
                    // 小额试探交易
                    return tx.getAmount() > 0 && tx.getAmount() < 10.0;
                }
            })
            .followedBy("large-amount")
            .where(new IterativeCondition<Transaction>() {
                @Override
                public boolean filter(Transaction tx, Context<Transaction> ctx) {
                    // 大额交易（大于5000）
                    if (tx.getAmount() <= 5000.0) {
                        return false;
                    }

                    // 同一用户
                    String userId = ctx.getEventsForPattern("small-amount")
                        .get(0).getUserId();
                    return tx.getUserId().equals(userId);
                }
            })
            .within(Time.minutes(5));

        // 3. 应用模式到流
        PatternStream<Transaction> patternStream = CEP.pattern(
            transactions.keyBy(Transaction::getUserId),  // 按用户分区
            fraudPattern
        );

        // 4. 处理匹配结果
        DataStream<Alert> alerts = patternStream
            .select(new PatternSelectFunction<Transaction, Alert>() {
                @Override
                public Alert select(Map<String, List<Transaction>> pattern) {
                    Transaction small = pattern.get("small-amount").get(0);
                    Transaction large = pattern.get("large-amount").get(0);

                    return new Alert(
                        small.getUserId(),
                        "FRAUD_PATTERN_DETECTED",
                        String.format("Small: $%.2f at %s, Large: $%.2f at %s",
                            small.getAmount(), small.getTimestamp(),
                            large.getAmount(), large.getTimestamp()),
                        System.currentTimeMillis()
                    );
                }
            });

        // 5. 输出告警
        alerts.addSink(new AlertSink());

        env.execute("Fraud Detection with CEP");
    }
}
```

#### 6.3.2 登录异常检测

```java
/**
 * 案例：异常登录检测
 * 模式1: 5分钟内 3 次失败登录 → 成功登录（暴力破解）
 * 模式2: 异地登录（地理位置突变）
 */
public class LoginAnomalyDetection {

    // 模式 1: 暴力破解检测
    public static Pattern<LoginEvent, ?> bruteForcePattern() {
        return Pattern.<LoginEvent>begin("failed-logins")
            .where(new SimpleCondition<LoginEvent>() {
                @Override
                public boolean filter(LoginEvent event) {
                    return !event.isSuccess();
                }
            })
            .timesOrMore(3)
            .greedy()
            .followedBy("success-login")
            .where(new SimpleCondition<LoginEvent>() {
                @Override
                public boolean filter(LoginEvent event) {
                    return event.isSuccess();
                }
            })
            .within(Time.minutes(5));
    }

    // 模式 2: 异地登录检测
    public static Pattern<LoginEvent, ?> geoAnomalyPattern() {
        return Pattern.<LoginEvent>begin("first-login")
            .where(new SimpleCondition<LoginEvent>() {
                @Override
                public boolean filter(LoginEvent event) {
                    return event.isSuccess();
                }
            })
            .next("second-login")
            .where(new IterativeCondition<LoginEvent>() {
                @Override
                public boolean filter(LoginEvent event, Context<LoginEvent> ctx) {
                    if (!event.isSuccess()) return false;

                    LoginEvent first = ctx.getEventsForPattern("first-login").get(0);

                    // 同一用户，不同城市，时间间隔小于 2 小时
                    return event.getUserId().equals(first.getUserId())
                        && !event.getCity().equals(first.getCity())
                        && (event.getTimestamp() - first.getTimestamp()) < Time.hours(2).toMilliseconds();
                }
            })
            .within(Time.hours(2));
    }

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        DataStream<LoginEvent> logins = env
            .addSource(new LoginEventSource())
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<LoginEvent>forBoundedOutOfOrderness(
                    Duration.ofSeconds(10))
            );

        // 应用多个模式
        Pattern<LoginEvent, ?> pattern = bruteForcePattern();

        PatternStream<LoginEvent> patternStream = CEP.pattern(
            logins.keyBy(LoginEvent::getUserId),
            pattern
        );

        // 处理匹配和超时
        DataStream<Alert> alerts = patternStream
            .process(new PatternProcessFunction<LoginEvent, Alert>() {
                @Override
                public void processMatch(
                        Map<String, List<LoginEvent>> match,
                        Context ctx,
                        Collector<Alert> out) {

                    // 正常匹配处理：暴力破解成功
                    List<LoginEvent> failed = match.get("failed-logins");
                    LoginEvent success = match.get("success-login").get(0);

                    out.collect(new Alert(
                        success.getUserId(),
                        "BRUTE_FORCE_SUCCESS",
                        String.format("%d failed attempts followed by success", failed.size()),
                        success.getTimestamp()
                    ));
                }

                @Override
                public void processTimedOutMatch(
                        Map<String, List<LoginEvent>> match,
                        Context ctx,
                        Collector<Alert> out) {

                    // 超时处理：多次失败但未成功（仍在尝试）
                    List<LoginEvent> failed = match.get("failed-logins");

                    out.collect(new Alert(
                        failed.get(0).getUserId(),
                        "BRUTE_FORCE_ATTEMPT",
                        String.format("%d failed attempts without success", failed.size()),
                        System.currentTimeMillis()
                    ));
                }
            });

        alerts.print();
        env.execute("Login Anomaly Detection");
    }
}
```

#### 6.3.3 业务流程监控

```java
/**
 * 案例：业务流程超时监控
 * 监控订单流程：创建 → 支付 → 发货 → 签收
 * 检测各环节超时
 */
public class BusinessProcessMonitor {

    // 完整订单流程监控
    public static Pattern<OrderEvent, ?> orderProcessPattern() {
        return Pattern.<OrderEvent>begin("created")
            .where(evt -> evt.getType().equals("ORDER_CREATED"))
            .followedBy("paid")
            .where(evt -> evt.getType().equals("ORDER_PAID"))
            .followedBy("shipped")
            .where(evt -> evt.getType().equals("ORDER_SHIPPED"))
            .followedBy("delivered")
            .where(evt -> evt.getType().equals("ORDER_DELIVERED"))
            .within(Time.hours(72));  // 72小时完整流程
    }

    // 支付超时检测
    public static Pattern<OrderEvent, ?> paymentTimeoutPattern() {
        return Pattern.<OrderEvent>begin("created")
            .where(evt -> evt.getType().equals("ORDER_CREATED"))
            .notFollowedBy("paid")
            .where(evt -> evt.getType().equals("ORDER_PAID"))
            .within(Time.minutes(30));  // 30分钟未支付
    }

    // 发货超时检测
    public static Pattern<OrderEvent, ?> shippingTimeoutPattern() {
        return Pattern.<OrderEvent>begin("paid")
            .where(evt -> evt.getType().equals("ORDER_PAID"))
            .notFollowedBy("shipped")
            .where(evt -> evt.getType().equals("ORDER_SHIPPED"))
            .within(Time.hours(24));  // 24小时未发货
    }

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        DataStream<OrderEvent> orders = env
            .addSource(new OrderEventSource())
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<OrderEvent>forBoundedOutOfOrderness(
                    Duration.ofSeconds(30))
            );

        // 检测支付超时
        PatternStream<OrderEvent> timeoutStream = CEP.pattern(
            orders.keyBy(OrderEvent::getOrderId),
            paymentTimeoutPattern()
        );

        DataStream<TimeoutAlert> alerts = timeoutStream
            .process(new PatternProcessFunction<OrderEvent, TimeoutAlert>() {
                @Override
                public void processMatch(
                        Map<String, List<OrderEvent>> match,
                        Context ctx,
                        Collector<TimeoutAlert> out) {
                    // 正常匹配不会触发（notFollowedBy）
                }

                @Override
                public void processTimedOutMatch(
                        Map<String, List<OrderEvent>> match,
                        Context ctx,
                        Collector<TimeoutAlert> out) {

                    OrderEvent created = match.get("created").get(0);
                    long elapsed = System.currentTimeMillis() - created.getTimestamp();

                    out.collect(new TimeoutAlert(
                        created.getOrderId(),
                        "PAYMENT_TIMEOUT",
                        String.format("Order not paid within %d minutes", elapsed / 60000),
                        created.getTimestamp()
                    ));
                }
            });

        alerts.addSink(new AlertSink());
        env.execute("Business Process Monitor");
    }
}
```

### 6.4 时间处理详解

#### 6.4.1 Event Time vs Processing Time

```java
/**
 * CEP 时间语义详解
 */
public class CEPTimeSemantics {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        DataStream<Event> stream = env.addSource(new EventSource());

        // ========== Event Time 处理（推荐用于生产） ==========
        DataStream<Event> eventTimeStream = stream
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<Event>forBoundedOutOfOrderness(
                    Duration.ofSeconds(30))  // 允许30秒乱序
                    .withIdleness(Duration.ofMinutes(5))  // 5分钟无数据标记为空闲
            );

        // Event Time 模式下，within() 使用事件时间戳
        Pattern<Event, ?> pattern = Pattern.<Event>begin("start")
            .where(evt -> evt.getType().equals("A"))
            .followedBy("end")
            .where(evt -> evt.getType().equals("B"))
            .within(Time.minutes(5));  // 基于 Event Time 的 5 分钟窗口

        // ========== Processing Time 处理（低延迟场景） ==========
        // Processing Time 模式下，within() 使用机器时间
        // 适用于：实时性要求高，可容忍少数迟到事件丢失

        PatternStream<Event> patternStream = CEP.pattern(
            eventTimeStream.keyBy(Event::getKey),
            pattern
        );

        // 处理结果
        patternStream.select(match -> {
            // 匹配处理
            return match;
        });
    }
}
```

#### 6.4.2 Watermark 与迟到事件处理

```java
/**
 * CEP 中 Watermark 策略配置
 */
public class CEPWatermarkConfig {

    /**
     * 推荐配置：Bounded Out Of Orderness
     * 适用于：大多数生产场景
     */
    public static WatermarkStrategy<Event> boundedOutOfOrdernessStrategy() {
        return WatermarkStrategy.<Event>forBoundedOutOfOrderness(
                Duration.ofSeconds(30))
            .withTimestampAssigner((event, timestamp) -> event.getEventTime())
            .withIdleness(Duration.ofMinutes(1));
    }

    /**
     * 严格有序场景
     * 适用于：数据源本身有序（如 Kafka 单分区）
     */
    public static WatermarkStrategy<Event> monotonousStrategy() {
        return WatermarkStrategy.<Event>forMonotonousTimestamps()
            .withTimestampAssigner((event, timestamp) -> event.getEventTime());
    }

    /**
     * 自定义 Watermark 生成
     * 适用于：特殊乱序场景
     */
    public static WatermarkStrategy<Event> customWatermarkStrategy() {
        return new WatermarkStrategy<Event>() {
            @Override
            public WatermarkGenerator<Event> createWatermarkGenerator(
                    WatermarkGeneratorSupplier.Context context) {
                return new WatermarkGenerator<Event>() {
                    private long maxTimestamp = Long.MIN_VALUE;
                    private final long outOfOrdernessMillis = 30000;  // 30秒

                    @Override
                    public void onEvent(Event event, long eventTimestamp, WatermarkOutput output) {
                        maxTimestamp = Math.max(maxTimestamp, eventTimestamp);
                    }

                    @Override
                    public void onPeriodicEmit(WatermarkOutput output) {
                        output.emitWatermark(
                            new Watermark(maxTimestamp - outOfOrdernessMillis - 1));
                    }
                };
            }
        }.withTimestampAssigner((event, timestamp) -> event.getEventTime());
    }
}
```

### 6.5 高级模式技巧

#### 6.5.1 动态模式生成

```java
/**
 * 基于配置动态生成 CEP 模式
 */
public class DynamicPatternBuilder {

    public static <T> Pattern<T, ?> buildPatternFromConfig(
            PatternConfig config,
            Class<T> eventClass) {

        Pattern<T, ?> pattern = Pattern.begin(config.getStartName());

        // 添加起始条件
        pattern = pattern.where(createCondition(config.getStartCondition()));

        // 添加后续模式阶段
        for (PatternStage stage : config.getStages()) {
            switch (stage.getContiguity()) {
                case NEXT:
                    pattern = pattern.next(stage.getName());
                    break;
                case FOLLOWED_BY:
                    pattern = pattern.followedBy(stage.getName());
                    break;
                case FOLLOWED_BY_ANY:
                    pattern = pattern.followedByAny(stage.getName());
                    break;
            }

            pattern = pattern.where(createCondition(stage.getCondition()));

            // 添加量词
            if (stage.getMinTimes() > 1 || stage.getMaxTimes() != null) {
                pattern = pattern.times(stage.getMinTimes(), stage.getMaxTimes());
            }

            if (stage.isOptional()) {
                pattern = pattern.optional();
            }
        }

        // 添加时间窗口
        pattern = pattern.within(Time.milliseconds(config.getWindowMillis()));

        return pattern;
    }

    private static <T> SimpleCondition<T> createCondition(ConditionConfig config) {
        return new SimpleCondition<T>() {
            @Override
            public boolean filter(T event) {
                // 根据配置解析条件
                return evaluateCondition(event, config);
            }
        };
    }
}
```

#### 6.5.2 多模式并行检测

```java
/**
 * 同时检测多个 CEP 模式
 */
public class MultiPatternDetection {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        DataStream<Transaction> transactions = env.addSource(new TransactionSource());

        // 定义多个检测模式
        Pattern<Transaction, ?> fraudPattern1 = Pattern.<Transaction>begin("small")
            .where(tx -> tx.getAmount() < 10)
            .followedBy("large")
            .where(tx -> tx.getAmount() > 10000)
            .within(Time.minutes(5));

        Pattern<Transaction, ?> fraudPattern2 = Pattern.<Transaction>begin("rapid")
            .where(tx -> tx.getAmount() > 1000)
            .timesOrMore(3)
            .within(Time.minutes(1));

        // 并行应用多个模式
        DataStream<Alert> alerts1 = CEP.pattern(transactions, fraudPattern1)
            .select(match -> new Alert("FRAUD_PATTERN_1", match));

        DataStream<Alert> alerts2 = CEP.pattern(transactions, fraudPattern2)
            .select(match -> new Alert("FRAUD_PATTERN_2", match));

        // 合并告警流
        DataStream<Alert> allAlerts = alerts1.union(alerts2);

        allAlerts.addSink(new AlertSink());
        env.execute("Multi-Pattern Detection");
    }
}
```

---

## 7. 性能优化

### 7.1 状态优化策略

| 优化策略 | 说明 | 效果 |
|---------|------|------|
| **时间窗口限制** | 使用合理的 `within()` | 减少状态存储 |
| **消耗策略** | 选择合适的 `SkipStrategy` | 减少重复匹配 |
| **KeyBy 分区** | 合理选择分区键 | 减少跨分区状态 |
| **条件过滤前置** | 在 Pattern 前预过滤 | 减少无效事件进入 CEP |

### 7.2 代码优化示例

```java
/**
 * CEP 性能优化示例
 */
public class CEPPerformanceOptimization {

    /**
     * 优化 1: 合理的 KeyBy 分区
     * 避免热点，确保数据均匀分布
     */
    public static void optimizedKeyBy(DataStream<Event> stream) {
        // 不推荐：用户ID可能导致热点
        // stream.keyBy(Event::getUserId)

        // 推荐：使用复合键或哈希
        stream.keyBy(event ->
            (event.getUserId().hashCode() % 100) + "_" + event.getRegion()
        );
    }

    /**
     * 优化 2: 前置过滤
     * 减少进入 CEP 的事件数量
     */
    public static DataStream<Event> preFilter(DataStream<Event> stream) {
        return stream.filter(event ->
            // 只让可能匹配的事件进入 CEP
            event.getType().equals("LOGIN") ||
            event.getType().equals("PAYMENT")
        );
    }

    /**
     * 优化 3: 选择高效的连续性策略
     */
    public static Pattern<Event, ?> optimizedPattern() {
        // next() 比 followedByAny() 性能更好
        // 只在需要时使用 followedByAny()
        return Pattern.<Event>begin("start")
            .where(evt -> evt.getType().equals("A"))
            .next("end")  // 优先使用 next()
            .where(evt -> evt.getType().equals("B"))
            .within(Time.minutes(1));
    }

    /**
     * 优化 4: 合理设置时间窗口
     */
    public static Pattern<Event, ?> optimizedWindow() {
        // 窗口越小，状态越少
        // 根据业务场景选择最小可行窗口
        return Pattern.<Event>begin("start")
            .where(evt -> evt.getType().equals("A"))
            .followedBy("end")
            .where(evt -> evt.getType().equals("B"))
            .within(Time.minutes(5));  // 避免使用过大的窗口
    }
}
```

### 7.3 监控指标

```java
/**
 * CEP 监控指标收集
 */
public class CEPMetrics {

    public static void collectMetrics(PatternStream<Event> patternStream) {
        patternStream.select(new PatternSelectFunction<Event, Result>() {
            private transient Counter matchCounter;
            private transient Histogram matchLatency;

            @Override
            public void open(Configuration parameters) {
                matchCounter = getRuntimeContext()
                    .getMetricGroup()
                    .counter("cep.matches");
                matchLatency = getRuntimeContext()
                    .getMetricGroup()
                    .histogram("cep.matchLatency", new DropwizardHistogramWrapper(
                        new com.codahale.metrics.Histogram(
                            new SlidingWindowReservoir(500))));
            }

            @Override
            public Result select(Map<String, List<Event>> pattern) {
                matchCounter.inc();

                // 计算匹配延迟
                long startTime = pattern.get("start").get(0).getTimestamp();
                long latency = System.currentTimeMillis() - startTime;
                matchLatency.update(latency);

                return new Result(pattern);
            }
        });
    }
}
```

---

## 8. 故障排查

### 8.1 常见问题与解决方案

| 问题 | 症状 | 原因 | 解决方案 |
|------|------|------|----------|
| **状态过大** | OOM、Checkpoint 超时 | 时间窗口过大 | 缩小 `within()` 窗口 |
| **匹配延迟** | 事件匹配不及时 | Watermark 延迟 | 调整 Watermark 策略 |
| **漏匹配** | 预期匹配未触发 | 连续性策略不当 | 检查 `next()` vs `followedBy()` |
| **重复匹配** | 同一事件多次匹配 | 消耗策略配置 | 设置 `SkipStrategy` |
| **性能下降** | 吞吐量降低 | Key 热点 | 优化 KeyBy 策略 |

### 8.2 调试技巧

```java
/**
 * CEP 调试工具
 */
public class CEPDebugging {

    /**
     * 调试 1: 打印所有事件
     */
    public static void debugEvents(DataStream<Event> stream) {
        stream.map(event -> {
            System.out.println("[DEBUG] Event: " + event +
                " @ " + System.currentTimeMillis());
            return event;
        });
    }

    /**
     * 调试 2: 监控 Watermark 进度
     */
    public static void debugWatermarks(DataStream<Event> stream) {
        stream.assignTimestampsAndWatermarks(
            WatermarkStrategy.<Event>forBoundedOutOfOrderness(Duration.ofSeconds(5))
                .withTimestampAssigner((event, ts) -> event.getTimestamp())
        ).map(event -> {
            // 打印当前 Watermark
            return event;
        });
    }

    /**
     * 调试 3: 模式匹配详情
     */
    public static void debugPatternMatches(
            PatternStream<Event> patternStream) {

        patternStream.select(new PatternSelectFunction<Event, String>() {
            @Override
            public String select(Map<String, List<Event>> pattern) {
                StringBuilder sb = new StringBuilder();
                sb.append("=== Pattern Match ===\n");

                for (Map.Entry<String, List<Event>> entry : pattern.entrySet()) {
                    sb.append("Stage: ").append(entry.getKey()).append("\n");
                    for (Event e : entry.getValue()) {
                        sb.append("  - ").append(e).append("\n");
                    }
                }

                System.out.println(sb.toString());
                return sb.toString();
            }
        });
    }
}
```

---

## 9. 可视化 (Visualizations)

### 9.1 CEP 架构流程图

```mermaid
graph TB
    A[Input Event Stream] --> B[KeyBy Partitioning]
    B --> C[CEP Pattern Matcher]
    C --> D{NFA State Machine}
    D -->|Match Found| E[Complex Event]
    D -->|Partial Match| F[State Store]
    D -->|Timeout| G[Cleanup]
    E --> H[Pattern Select Function]
    H --> I[Output Stream]
    F -->|Next Event| D

    style C fill:#e1f5fe
    style D fill:#fff3e0
    style E fill:#e8f5e9
```

### 9.2 模式匹配状态机

```mermaid
stateDiagram-v2
    [*] --> Idle: Initial State
    Idle --> Matching: First Event Matches
    Matching --> PartialMatch: Intermediate Event
    Matching --> CompleteMatch: Final Event
    Matching --> Timeout: Within Expired
    PartialMatch --> PartialMatch: Continue Matching
    PartialMatch --> CompleteMatch: All Events Matched
    PartialMatch --> Timeout: Time Window Expired
    CompleteMatch --> [*]: Emit Result
    Timeout --> [*]: Cleanup State

    state Matching {
        [*] --> Stage1
        Stage1 --> Stage2: next()
        Stage1 --> Stage2: followedBy()
        Stage2 --> Stage3: Event Match
    }
```

### 9.3 连续性策略对比图

```mermaid
flowchart LR
    subgraph next["next() - 严格连续"]
        A1[A] -->|紧邻| B1[B]
        A1 -.->|X 不允许| X1[Other]
    end

    subgraph followedBy["followedBy() - 宽松连续"]
        A2[A] --> X2[Other]
        X2 --> X3[Other]
        X3 --> B2[B]
    end

    subgraph followedByAny["followedByAny() - 非确定性"]
        A3[A] --> B3[B]
        A3 --> B4[B]
        A3 --> X4[Other] --> B5[B]
    end

    style next fill:#ffebee
    style followedBy fill:#e8f5e9
    style followedByAny fill:#e3f2fd
```

### 9.4 CEP 在流处理中的位置

```mermaid
graph TB
    subgraph "Data Ingestion"
        K[Kafka/Source]
    end

    subgraph "Stream Processing"
        F[Filter/Map]
        W[Window Aggregation]
        C[CEP Pattern Matching]
        J[Join/Union]
    end

    subgraph "Output"
        S[(Sink)]
    end

    K --> F
    F --> W
    F --> C
    W --> J
    C --> J
    J --> S

    style C fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

---

## 10. 引用参考 (References)
