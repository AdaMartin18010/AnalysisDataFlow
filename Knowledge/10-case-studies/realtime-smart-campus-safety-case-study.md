# 实时智慧校园安全监测案例研究

> 所属阶段: Knowledge/ Flink/ | 前置依赖: [算子全景分类](../01-concept-atlas/operator-deep-dive/01.06-single-input-operators.md) | [CEP模式](../02-design-patterns/pattern-cep-complex-event.md) | 形式化等级: L4

## 1. 概念定义 (Definitions)

### Def-SCS-01-01: 智慧校园安全系统 (Smart Campus Safety System)

智慧校园安全系统是通过门禁数据、视频监控、宿舍出入、食堂消费和流计算平台，实现校园人员轨迹追踪、异常行为检测与应急响应的集成系统。

$$\mathcal{S} = (A, V, D, C, F)$$

其中 $A$ 为门禁出入流，$V$ 为视频分析流，$D$ 为宿舍状态流，$C$ 为消费数据流，$F$ 为流计算处理拓扑。

### Def-SCS-01-02: 异常聚集指数 (Abnormal Gathering Index)

$$AGI = \frac{N_{actual}}{N_{normal}} \cdot \frac{1}{1 + e^{-(t - t_{threshold})}}$$

其中 $N_{actual}$ 为实时人数，$N_{normal}$ 为正常人数，$t$ 为停留时间。$AGI > 3$ 触发聚集预警。

### Def-SCS-01-03: 学生安全状态 (Student Safety Status)

$$Status = \begin{cases}
SAFE & \text{在校且在正常区域} \\
WARNING & \text{未归寝或异常区域} \\
DANGER & \text{离校或紧急事件}
\end{cases}$$

## 2. 实例验证 (Examples)

### 2.1 未归寝检测

```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

DataStream<DormEntry> dormEntries = env
    .addSource(new KafkaSource<>("campus.dorm.entry"))
    .map(new DormParser());

// Detect students not returned by curfew (23:00)
DataStream<AbsenceAlert> absences = dormEntries
    .keyBy(e -> e.getStudentId())
    .window(TumblingEventTimeWindows.of(Time.days(1)))
    .aggregate(new AbsenceAggregate());

absences.addSink(new AlertSink());
```

### 2.2 异常聚集检测

```java
DataStream<Location> locations = env
    .addSource(new KafkaSource<>("campus.location"))
    .map(new LocationParser());

DataStream<GatheringAlert> gatherings = locations
    .keyBy(l -> l.getZoneId())
    .window(SlidingEventTimeWindows.of(Time.minutes(5), Time.minutes(1)))
    .aggregate(new GatheringAggregate() {
        @Override
        public void aggregate(Location loc, Accumulator acc) {
            acc.add(loc.getStudentId());
            if (acc.getCount() > THRESHOLD) {
                out.collect(new GatheringAlert(loc.getZoneId(),
                    acc.getCount(), ctx.window().getEnd()));
            }
        }
    });

gatherings.addSink(new SecuritySink());
```

## 3. 引用参考 (References)

[^1]: 教育部, "智慧校园总体框架", 2018.
[^2]: GB/T 36342-2018, "智慧校园总体框架", 2018.
