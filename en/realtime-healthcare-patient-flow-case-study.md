# Real-Time Smart Healthcare Patient Flow Management Case Study

> Stage: Knowledge/ Flink/ | Prerequisites: [Operator Panorama Classification](../Knowledge/01-concept-atlas/operator-deep-dive/01.06-single-input-operators.md) | [CEP Patterns](../Knowledge/02-design-patterns/pattern-cep-complex-event.md) | Formalization Level: L4

## 1. Definitions

### Def-HPF-01-01: Smart Patient Flow System (智慧患者流系统)

A Smart Patient Flow System (智慧患者流系统) is an integrated system that leverages registration data, triage ratings, waiting queues, bed status, and a stream computing platform to achieve real-time monitoring and resource optimization across the entire patient visit workflow.

$$\mathcal{P} = (R, T, Q, B, F)$$

Where $R$ is the registration data stream, $T$ is the triage rating stream, $Q$ is the waiting queue stream, $B$ is the bed status stream, and $F$ is the stream computing processing topology.

### Def-HPF-01-02: Emergency Triage Priority (急诊分诊优先级)

A five-level triage standard is adopted:

$$Priority = \begin{cases}
1 & \text{濒危 (Resuscitation)} \\
2 & \text{危重 (Emergent)} \\
3 & \text{急症 (Urgent)} \\
4 & \text{次急 (Less Urgent)} \\
5 & \text{非急 (Non-urgent)}
\end{cases}$$

### Def-HPF-01-03: Waiting Time Alert Threshold (候诊时间预警阈值)

$$Alert_{wait} = \alpha \cdot T_{target} \cdot Priority$$

Where $T_{target}$ is the baseline waiting time, $\alpha = 1.5$ is the amplification coefficient, and $Priority$ is the priority weight (smaller values indicate higher weights).

## 2. Examples

### 2.1 Real-Time Waiting Monitoring

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

### 2.2 Real-Time Bed Management

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

## 3. References

[^1]: National Health Commission of China, "Pilot Guidelines for Emergency Patient Triage Classification", 2011.
[^2]: Hwang, U. et al., "Emergency Department Crowding", Annals of Emergency Medicine, 2011.
