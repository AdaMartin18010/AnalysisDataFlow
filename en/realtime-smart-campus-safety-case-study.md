# Real-Time Smart Campus Safety Monitoring Case Study

> **Stage**: Knowledge/ Flink/ | **Prerequisites**: [Operator Panorama Classification](../Knowledge/01-concept-atlas/operator-deep-dive/01.06-single-input-operators.md) | [CEP Pattern](pattern-cep-complex-event.md) | **Formal Level**: L4

## 1. Definitions

### Def-SCS-01-01: Smart Campus Safety System (智慧校园安全系统)

Smart Campus Safety System is an integrated system that leverages access control data, video surveillance, dormitory entry/exit records, cafeteria consumption data, and a stream processing platform to achieve campus personnel trajectory tracking, abnormal behavior detection, and emergency response.

$$\mathcal{S} = (A, V, D, C, F)$$

where $A$ is the access control entry/exit stream, $V$ is the video analytics stream, $D$ is the dormitory status stream, $C$ is the consumption data stream, and $F$ is the stream processing topology.

### Def-SCS-01-02: Abnormal Gathering Index (异常聚集指数)

$$AGI = \frac{N_{actual}}{N_{normal}} \cdot \frac{1}{1 + e^{-(t - t_{threshold})}}$$

where $N_{actual}$ is the real-time headcount, $N_{normal}$ is the normal headcount, and $t$ is the dwell time. $AGI > 3$ triggers a gathering alert.

### Def-SCS-01-03: Student Safety Status (学生安全状态)

$$Status = \begin{cases}
SAFE & \text{On campus and in normal area} \\
WARNING & \text{Not returned to dormitory or in abnormal area} \\
DANGER & \text{Left campus or emergency event}
\end{cases}$$

## 2. Examples

### 2.1 Dormitory Absence Detection

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

### 2.2 Abnormal Gathering Detection

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

## 3. References

[^1]: Ministry of Education of the People's Republic of China, "Smart Campus Overall Framework", 2018.
[^2]: GB/T 36342-2018, "Smart Campus Overall Framework", 2018.
