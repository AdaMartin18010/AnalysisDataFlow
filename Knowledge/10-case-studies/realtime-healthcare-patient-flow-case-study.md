# 实时智慧医疗患者流管理案例研究

> 所属阶段: Knowledge/ Flink/ | 前置依赖: [算子全景分类](../01-concept-atlas/operator-deep-dive/01.06-single-input-operators.md) | [CEP模式](../02-design-patterns/pattern-cep-complex-event.md) | 形式化等级: L4

## 1. 概念定义 (Definitions)

### Def-HPF-01-01: 智慧患者流系统 (Smart Patient Flow System)

智慧患者流系统是通过挂号数据、分诊评级、候诊队列、床位状态和流计算平台，实现患者全就诊流程实时监控与资源优化的集成系统。

$$\mathcal{P} = (R, T, Q, B, F)$$

其中 $R$ 为挂号数据流，$T$ 为分诊评级流，$Q$ 为候诊队列流，$B$ 为床位状态流，$F$ 为流计算处理拓扑。

### Def-HPF-01-02: 急诊分诊优先级 (Emergency Triage Priority)

采用五级分诊标准：

$$Priority = \begin{cases}
1 & \text{濒危 (Resuscitation)} \\
2 & \text{危重 (Emergent)} \\
3 & \text{急症 (Urgent)} \\
4 & \text{次急 (Less Urgent)} \\
5 & \text{非急 (Non-urgent)}
\end{cases}$$

### Def-HPF-01-03: 候诊时间预警阈值 (Waiting Time Alert Threshold)

$$Alert_{wait} = \alpha \cdot T_{target} \cdot Priority$$

其中 $T_{target}$ 为基准候诊时间，$\alpha = 1.5$ 为放大系数，$Priority$ 为优先级权重（值越小权重越大）。

## 2. 实例验证 (Examples)

### 2.1 实时候诊监控

```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

DataStream<Registration> registrations = env
    .addSource(new KafkaSource<>("hospital.registration"))
    .map(new RegistrationParser());

DataStream<TriageResult> triage = env
    .addSource(new KafkaSource<>("hospital.triage"))
    .map(new TriageParser());

// Merge streams and calculate waiting time
DataStream<PatientStatus> patientStatus = registrations
    .keyBy(r -> r.getPatientId())
    .connect(triage.keyBy(t -> t.getPatientId()))
    .process(new PatientFlowFunction() {
        @Override
        public void processElement1(Registration reg, Context ctx,
                                   Collector<PatientStatus> out) {
            out.collect(new PatientStatus(reg.getPatientId(),
                reg.getDepartment(), "REGISTERED", ctx.timestamp()));
        }

        @Override
        public void processElement2(TriageResult triage, Context ctx,
                                   Collector<PatientStatus> out) {
            out.collect(new PatientStatus(triage.getPatientId(),
                triage.getDepartment(), "TRIAGED_" + triage.getLevel(),
                ctx.timestamp()));
        }
    });

// Alert on long wait times
DataStream<WaitAlert> alerts = patientStatus
    .keyBy(s -> s.getDepartment())
    .process(new WaitTimeMonitorFunction() {
        @Override
        public void processElement(PatientStatus status, Context ctx,
                                   Collector<WaitAlert> out) {
            long waitTime = ctx.timestamp() - status.getRegistrationTime();
            long threshold = getThreshold(status.getPriority());
            if (waitTime > threshold) {
                out.collect(new WaitAlert(status.getPatientId(),
                    waitTime, threshold, ctx.timestamp()));
            }
        }
    });

alerts.addSink(new AlertSink());
```

### 2.2 床位实时管理

```java
DataStream<BedStatus> bedStatus = env
    .addSource(new KafkaSource<>("hospital.bed"))
    .map(new BedParser());

DataStream<BedAvailability> availability = bedStatus
    .keyBy(b -> b.getWardId())
    .window(TumblingProcessingTimeWindows.of(Time.minutes(1)))
    .aggregate(new BedAvailabilityAggregate());

availability.addSink(new DashboardSink());
```

## 3. 引用参考 (References)

[^1]: 国家卫健委, "急诊病人病情分级试点指导原则", 2011.
[^2]: Hwang, U. et al., "Emergency Department Crowding", Annals of Emergency Medicine, 2011.
