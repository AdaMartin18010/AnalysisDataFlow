# Challenge 2: 恶意登录检测

> 难度: 中级 | 预计时间: 3小时 | 主题: CEP、Pattern

## 需求描述

实现一个实时安全检测系统，使用 Flink CEP 检测异常登录行为。

### 功能需求

1. **暴力破解检测**
   - 5分钟内连续3次登录失败，触发告警
   - 10分钟内连续5次登录失败，封禁账户

2. **异地登录检测**
   - 短时间内在不同地理位置登录
   - IP地址变化超过一定范围

3. **异常时间检测**
   - 非常规时间登录（如凌晨）
   - 首次从新设备登录

### 数据结构

```java
public class LoginEvent {
    public String userId;        // 用户ID
    public String ipAddress;     // IP地址
    public String status;        // SUCCESS / FAIL
    public String location;      // 地理位置
    public String device;        // 设备信息
    public long timestamp;       // 时间戳
}

public class SecurityAlert {
    public String alertType;     // BRUTE_FORCE / GEO_ANOMALY / TIME_ANOMALY
    public String userId;
    public String message;
    public long timestamp;
    public int severity;         // 1-5
}
```

## 技术要点

### CEP 模式设计

```
暴力破解模式: FAIL -> FAIL -> FAIL (within 5min)
             FAIL x 5 (within 10min)

异地登录模式: LOGIN(loc=A) -> LOGIN(loc!=A) (within 30min)
```

## 实现步骤

### Step 1: 基础 CEP 模式

```java
public class SecurityRules {

    // 模式1: 3次登录失败（5分钟内）
    public static Pattern<LoginEvent, ?> bruteForcePattern3 = Pattern
        .<LoginEvent>begin("fail")
        .where(evt -> evt.status.equals("FAIL"))
        .times(3)
        .within(Time.minutes(5));

    // 模式2: 5次登录失败（10分钟内）- 严重
    public static Pattern<LoginEvent, ?> bruteForcePattern5 = Pattern
        .<LoginEvent>begin("fail")
        .where(evt -> evt.status.equals("FAIL"))
        .timesOrMore(5)
        .within(Time.minutes(10));

    // 模式3: 异地登录检测
    public static Pattern<LoginEvent, ?> geoAnomalyPattern = Pattern
        .<LoginEvent>begin("first")
        .where(evt -> evt.status.equals("SUCCESS"))
        .next("second")
        .where(new IterativeCondition<LoginEvent>() {
            @Override
            public boolean filter(LoginEvent event, Context<LoginEvent> ctx) {
                if (!event.status.equals("SUCCESS")) {
                    return false;
                }

                // 获取第一个事件的位置
                for (LoginEvent first : ctx.getEventsForPattern("first")) {
                    if (!first.location.equals(event.location)) {
                        // 检查时间间隔
                        long timeDiff = event.timestamp - first.timestamp;
                        return timeDiff < Time.minutes(30).toMilliseconds();
                    }
                }
                return false;
            }
        })
        .within(Time.hours(1));
}
```

### Step 2: 告警处理

```java
public class AlertHandler extends
    PatternProcessFunction<LoginEvent, SecurityAlert> {

    @Override
    public void processMatch(
            Map<String, List<LoginEvent>> match,
            Context ctx,
            Collector<SecurityAlert> out) {

        List<LoginEvent> events = match.get("fail");
        if (events != null) {
            // 暴力破解告警
            int failCount = events.size();
            LoginEvent lastEvent = events.get(events.size() - 1);

            SecurityAlert alert = new SecurityAlert();
            alert.alertType = failCount >= 5 ? "BRUTE_FORCE_CRITICAL" : "BRUTE_FORCE_WARNING";
            alert.userId = lastEvent.userId;
            alert.message = String.format(
                "%d failed login attempts from IP %s",
                failCount, lastEvent.ipAddress
            );
            alert.timestamp = ctx.timestamp();
            alert.severity = failCount >= 5 ? 5 : 3;

            out.collect(alert);
        }

        // 处理异地登录
        List<LoginEvent> firstList = match.get("first");
        List<LoginEvent> secondList = match.get("second");

        if (firstList != null && secondList != null) {
            LoginEvent first = firstList.get(0);
            LoginEvent second = secondList.get(0);

            SecurityAlert alert = new SecurityAlert();
            alert.alertType = "GEO_ANOMALY";
            alert.userId = first.userId;
            alert.message = String.format(
                "Login from different locations: %s -> %s",
                first.location, second.location
            );
            alert.timestamp = ctx.timestamp();
            alert.severity = 4;

            out.collect(alert);
        }
    }
}
```

### Step 3: 账户封禁状态管理

```java
public class AccountBlocker extends KeyedProcessFunction<String, SecurityAlert, BlockedAccount> {

    private ValueState<Boolean> blockedState;
    private ValueState<Long> unblockTimeState;

    @Override
    public void open(Configuration parameters) {
        blockedState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("blocked", Boolean.class)
        );
        unblockTimeState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("unblockTime", Long.class)
        );
    }

    @Override
    public void processElement(
            SecurityAlert alert,
            Context ctx,
            Collector<BlockedAccount> out) throws Exception {

        // 严重告警，封禁账户
        if (alert.severity >= 4 && (blockedState.value() == null || !blockedState.value())) {
            long blockDuration = alert.severity == 5 ?
                Time.hours(24).toMilliseconds() : Time.hours(1).toMilliseconds();

            long unblockTime = ctx.timestamp() + blockDuration;

            blockedState.update(true);
            unblockTimeState.update(unblockTime);

            // 注册解封定时器
            ctx.timerService().registerEventTimeTimer(unblockTime);

            out.collect(new BlockedAccount(
                alert.userId,
                ctx.timestamp(),
                unblockTime,
                alert.message
            ));
        }
    }

    @Override
    public void onTimer(
            long timestamp,
            OnTimerContext ctx,
            Collector<BlockedAccount> out) throws Exception {

        // 解封账户
        blockedState.update(false);
        unblockTimeState.clear();

        out.collect(new BlockedAccount(
            ctx.getCurrentKey(),
            timestamp,
            0,
            "Account unblocked"
        ));
    }
}
```

### Step 4: 主程序

```java
public class SecurityDetectionJob {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(2);

        // 登录事件流
        DataStream<LoginEvent> loginStream = env
            .addSource(new LoginEventSource())
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<LoginEvent>forBoundedOutOfOrderness(
                        Duration.ofSeconds(10))
                    .withTimestampAssigner((event, ts) -> event.timestamp)
            );

        // 应用 CEP 模式
        Pattern<LoginEvent, ?> pattern = Pattern
            .<LoginEvent>begin("brute3").where(evt -> evt.status.equals("FAIL")).times(3)
            .or(Pattern.<LoginEvent>begin("brute5").where(evt -> evt.status.equals("FAIL")).timesOrMore(5))
            .or(Pattern.<LoginEvent>begin("geo").where(evt -> evt.status.equals("SUCCESS"))
                .next("geo2").where(new GeoCondition()))
            .within(Time.minutes(10));

        PatternStream<LoginEvent> patternStream = CEP.pattern(
            loginStream.keyBy(evt -> evt.userId),
            pattern
        );

        // 处理匹配结果
        DataStream<SecurityAlert> alerts = patternStream
            .process(new AlertHandler());

        // 输出告警
        alerts.print("ALERT");

        // 封禁严重违规账户
        alerts
            .keyBy(alert -> alert.userId)
            .process(new AccountBlocker())
            .print("BLOCKED");

        env.execute("Security Detection");
    }
}
```

## 验证方法

### 测试数据生成器

```java
public class LoginEventSource implements SourceFunction<LoginEvent> {

    @Override
    public void run(SourceContext<LoginEvent> ctx) throws Exception {
        // 模拟暴力破解
        String targetUser = "victim_user";
        String attackerIp = "192.168.1.100";

        for (int i = 0; i < 5; i++) {
            ctx.collect(new LoginEvent(
                targetUser,
                attackerIp,
                "FAIL",
                "Beijing",
                "Unknown",
                System.currentTimeMillis() + i * 60000
            ));
        }

        // 模拟异地登录
        ctx.collect(new LoginEvent(
            "user_001", "10.0.0.1", "SUCCESS", "Beijing", "Chrome",
            System.currentTimeMillis()
        ));
        ctx.collect(new LoginEvent(
            "user_001", "10.0.0.2", "SUCCESS", "Shanghai", "Chrome",
            System.currentTimeMillis() + 600000
        ));
    }
}
```

## 评分标准

| 维度 | 权重 | 要求 |
|------|------|------|
| CEP 模式 | 30% | 正确定义暴力破解和异地登录模式 |
| 告警生成 | 25% | 正确生成不同类型的告警 |
| 状态管理 | 25% | 正确管理封禁状态和解封逻辑 |
| 代码质量 | 20% | 结构清晰，有适当注释和测试 |

## 扩展练习

### 扩展 1: 更复杂的地理检测

```java
// 使用 GeoIP 库检测不可能的旅行速度
public class GeoCondition extends IterativeCondition<LoginEvent> {

    private static final double MAX_SPEED_KMH = 900; // 飞机速度

    @Override
    public boolean filter(LoginEvent event, Context<LoginEvent> ctx) {
        for (LoginEvent prev : ctx.getEventsForPattern("first")) {
            double distance = calculateDistance(prev.location, event.location);
            double timeHours = (event.timestamp - prev.timestamp) / 3600000.0;
            double speed = distance / timeHours;

            if (speed > MAX_SPEED_KMH) {
                return true; // 不可能的速度，异常
            }
        }
        return false;
    }

    private double calculateDistance(String loc1, String loc2) {
        // 解析经纬度，计算距离
        return GeoUtils.distance(loc1, loc2);
    }
}
```

### 扩展 2: 机器学习集成

```java
// 使用模型评分登录风险
public class MLScoringFunction extends RichMapFunction<LoginEvent, ScoredLogin> {

    private transient RiskModel model;

    @Override
    public void open(Configuration parameters) {
        // 加载预训练的风险评估模型
        model = RiskModel.load("hdfs://models/login-risk-model");
    }

    @Override
    public ScoredLogin map(LoginEvent event) {
        double riskScore = model.predict(event);
        return new ScoredLogin(event, riskScore);
    }
}
```

## 参考解答

完整参考实现位于 `reference/challenge-02-login-detection/` 目录。

## 下一步

- [Challenge 3: 订单超时处理](./challenge-03-order-timeout.md)
