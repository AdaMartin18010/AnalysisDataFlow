# Real-Time Patient Monitoring and Alert System: ICU Vital Signs Stream Processing Practice

> **Stage**: Knowledge/10-case-studies/healthcare | **Prerequisites**: [../Knowledge/02-design-patterns/pattern-event-time-processing.md](../Knowledge/02-design-patterns/pattern-event-time-processing.md), [../Knowledge/03-business-patterns/iot-stream-processing.md](../Knowledge/03-business-patterns/iot-stream-processing.md) | **Formalization Level**: L3-L4 | **Industry**: Healthcare / IoT

---

> **Case Nature**: 🔬 Proof-of-Concept Architecture | **Validation Status**: Based on theoretical derivation and architectural design; not independently validated by third-party production deployment
>
> This case describes an ideal architecture derived from the project's theoretical framework, including hypothetical performance metrics. Actual production deployment may yield different results due to environmental variations.

---

## 1. Concept Definitions (Definitions)

### Def-K-10-07-01: Vital Signs Data Model (生命体征数据模型)

The **Vital Signs Data Model** (生命体征数据模型) is a formalized data structure describing real-time physiological parameters of ICU patients, defined as an octuple:

$$
\gamma = \langle \text{patientId}, \text{deviceId}, \text{timestamp}, \text{hr}, \text{bp}_{sys}, \text{bp}_{dia}, \text{spo}_2, \text{temp} \rangle
$$

| Field | Type | Unit | Normal Range |
|-------|------|------|-------------|
| $\text{patientId}$ | String | — | — |
| $\text{deviceId}$ | String | — | — |
| $\text{timestamp}$ | long | ms | — |
| $\text{hr}$ | int | bpm | 60–100 |
| $\text{bp}_{sys}$ | int | mmHg | 90–140 |
| $\text{bp}_{dia}$ | int | mmHg | 60–90 |
| $\text{spo}_2$ | float | % | 95–100 |
| $\text{temp}$ | float | °C | 36.0–37.5 |

Sampling frequency: routine monitoring $f_{normal} = 1\text{ Hz}$; critical monitoring $f_{critical} = 10\text{ Hz}$. For 50 ICU beds, the peak data generation rate is approximately $32\text{ KB/s}$, accumulating about $2.8\text{ GB}$ per day.

---

### Def-K-10-07-02: Alert Level (预警等级)

The **Alert Level** (预警等级) is a discrete classification system defined based on the degree and urgency of deviation of a patient's vital signs from normal ranges:

$$
\mathcal{L} = \{ \text{LEVEL\_0}, \text{LEVEL\_1}, \text{LEVEL\_2}, \text{LEVEL\_3}, \text{LEVEL\_4} \}
$$

| Level | Name | Trigger Condition | Response Time Requirement |
|-------|------|-------------------|--------------------------|
| LEVEL_0 | Normal | All indicators within normal range | — |
| LEVEL_1 | Notification | Single indicator mildly deviated | < 60 s |
| LEVEL_2 | Warning | Single indicator moderately deviated or two indicators mildly deviated | < 30 s |
| LEVEL_3 | Critical | Single indicator severely deviated or composite indicators abnormal | < 10 s |
| LEVEL_4 | Rescue | Vital signs absent or extremely severely abnormal | < 5 s |

Composite alert pattern example (shock alert):

$$
\text{SHOCK}(\gamma_t, \gamma_{t-\Delta t}) \triangleq \text{hr}_t < 60 \land \text{bp}_{sys,t} < 90 \land (\text{hr}_t - \text{hr}_{t-\Delta t}) < -10 \land (\text{bp}_{sys,t} - \text{bp}_{sys,t-\Delta t}) < -15
$$

---

### Def-K-10-07-03: Privacy De-sanitization Operator (隐私脱敏算子)

The **Privacy De-sanitization Operator** (隐私脱敏算子) $\mathcal{D}$ is a family of functions that transform patient privacy identifiers and sensitive information during data stream processing:

$$
\mathcal{D}: \gamma_{raw} \times \mathcal{P} \to \gamma_{safe}
$$

| Operator | Symbol | Definition |
|----------|--------|------------|
| Identifier Hashing | $\mathcal{D}_{hash}$ | $\text{patientId}' = \text{SHA256}(\text{patientId} \| \text{salt})$ |
| Time Perturbation | $\mathcal{D}_{time}$ | $\text{timestamp}' = \text{timestamp} + \delta, \delta \sim U(-\Delta, +\Delta)$ |
| Value Generalization | $\mathcal{D}_{gen}$ | $\text{bp}' = \lfloor \text{bp} / k \rfloor \times k$ |
| Field Masking | $\mathcal{D}_{mask}$ | $\text{name}' = \text{***}$ |

HIPAA de-identification Safe Harbor rule mapping[^1]: 18 categories of identifiers must be processed via $\mathcal{D}_{hash}$ or $\mathcal{D}_{mask}$.

---

## 2. Property Derivation (Properties)

### Prop-K-10-07-01: Data Collection Frequency and Throughput Boundary

Let $N$ be the number of ICU beds, $f_{max} = 10\text{ Hz}$, $S_{payload} \approx 64\text{ bytes}$, and Avro compression ratio $R_{batch} \approx 0.3$; then the edge-to-cloud network throughput is:

$$
\lambda_{edge\to cloud} = N \times f_{max} \times S_{payload} \times R_{batch}
$$

For $N = 50$: $\lambda_{edge\to cloud} = 50 \times 10 \times 64 \times 0.3 = 9,600\text{ bytes/s} = 9.6\text{ KB/s}$.

**Conclusion**: The data volume of a single-hospital ICU is far below the typical throughput capacity of Kafka/Flink; **the bottleneck lies in latency rather than throughput**.

---

### Prop-K-10-07-02: Out-of-Order Data Tolerance and Watermark Sufficiency

Let network latency $L_{network} \sim \mathcal{N}(\mu=20\text{ms}, \sigma=10\text{ms})$, edge-to-cloud latency $L_{edge\to cloud} \sim \mathcal{N}(\mu=50\text{ms}, \sigma=30\text{ms})$; the Watermark boundary is:

$$
\delta_{max} \geq P_{99}(L_{network} + L_{edge\to cloud}) \approx 144\text{ ms}
$$

Taking $\delta_{max} = 2\text{s}$, the effective alert latency $T_{effective} = T_{process} + \delta_{max} < 2.5\text{s} \ll T_{alert} = 10\text{s}$. Watermark waiting will not cause alert timeout.

---

## 3. Relation Establishment (Relations)

### 3.1 Medical IoT to Flink Component Mapping

| Medical System Component | Flink Primitive | State Type |
|-------------------------|-----------------|------------|
| Bedside Monitor | KafkaSource / MQTT Source | Stateless |
| Edge Gateway Preprocessing | ProcessFunction + Filter | ValueState |
| Patient-Level Real-Time Analysis | KeyedProcessFunction | ValueState, ListState |
| CEP Composite Alert Detection | CEP.pattern + PatternSelect | NFA State Machine |
| Multi-Stream Join | IntervalJoin / TemporalTableJoin | Time-Window State |
| Privacy De-sanitization Processing | ProcessFunction | Stateless |
| Alert Notification | SinkFunction | Stateless |

### 3.2 CEP Pattern to Clinical Rule Mapping

| Clinical Rule | CEP Pattern Definition | Alert Level |
|---------------|------------------------|-------------|
| HR > 120 for 5 minutes | `Pattern.begin("tachycardia").where(v -> v.hr > 120).timesOrMore(300)` | LEVEL_2 |
| Systolic BP < 90 and HR > 100 | `Pattern.begin("hypotension").where(v -> v.bpSys < 90).next("tachycardia").where(v -> v.hr > 100).within(Time.minutes(1))` | LEVEL_3 |
| SpO2 < 90% for 30 seconds | `Pattern.begin("hypoxia").where(v -> v.spo2 < 90).timesOrMore(30).within(Time.seconds(30))` | LEVEL_3 |
| HR drop > 20% + BP drop > 15% | See Section 6 shock alert pattern | LEVEL_3 |

### 3.3 Multi-Stream Join to Patient Panoramic View Mapping

$$
\text{PatientView}_t = \text{VitalSigns}_t \bowtie_{\text{patientId}} \text{PatientInfo} \bowtie_{[t-1h, t]} \text{Medication}_t
$$

| Data Stream | Update Frequency | Join Strategy | State TTL |
|-------------|-----------------|---------------|-----------|
| $\text{VitalSigns}_t$ | 1–10 Hz | Primary Driving Stream | — |
| $\text{PatientInfo}$ | Quasi-static | Broadcast / Temporal Table | 24 h |
| $\text{Medication}_t$ | Event-triggered | Interval Join | 2 h |

---

## 4. Argumentation (Argumentation)

### 4.1 Why Stream Processing is Essential for ICU Monitoring

Traditional batch ETL (hour-level) cannot provide timely alerts during acute conditions such as cardiac arrest or respiratory failure; batch window boundaries may split critical event sequences across boundaries, destroying CEP pattern detection integrity.

Studies indicate that approximately $15\%$ of cardiac arrest events in the ICU exhibit detectable physiological deterioration signs $6$–$8$ hours before occurrence[^3]. Stream processing can trigger alerts at the first moment such signs appear, and intervention $5$–$10$ minutes earlier can reduce ICU mortality by approximately $6\%$.

### 4.2 Necessity of Edge Gateway Preprocessing

1. **Data Dimensionality Reduction**: Raw ECG waveform at $500\text{ Hz}$ generates $>2\text{ GB}$ per bed per day. Edge extraction of derived indicators, uploading only aggregated metrics, achieves $>1000:1$ compression.
2. **Local Emergency Response**: LEVEL_4 must be processed locally at the edge (< 1 s); bedside alarms must remain functional during network interruption.
3. **Network Interruption Tolerance**: Edge gateways are configured with local RocksDB storage to continue monitoring during interruptions, retransmitting in event-time order after recovery.

### 4.3 Complexity Analysis of Multi-Patient Correlated Alerts

**Cross-Infection Risk Monitoring**:

$$
\text{OUTBREAK}(p_i, p_j, t) \triangleq \text{pathogen}(p_i, t) = \text{pathogen}(p_j, t) \land \text{room}(p_i) = \text{room}(p_j) \land |t_i - t_j| < 72h
$$

Implementation: `keyBy(roomId)` + Windowed Aggregation, aggregating pathogen detection results at the ward dimension.

**Equipment Resource Conflicts**: There are 8 ventilators in total; when 3 LEVEL_3 respiratory failure alerts occur simultaneously, standby equipment must be scheduled in advance. Implementation: `keyBy(icuUnit)` + ProcessFunction maintaining resource pool state.

### 4.4 HIPAA and MLPS 2.0 Compliance Technical Measures

| HIPAA Requirement[^1] | Technical Implementation |
|-----------------------|--------------------------|
| Access Control | RBAC + Fine-Grained Permissions |
| Audit Control | Tamper-Proof Audit Logs |
| Transmission Security | TLS 1.3 End-to-End Encryption |
| De-identification | De-sanitization Operator $\mathcal{D}$ |

MLPS 2.0 (等保2.0) Level-3 Key Points[^2]: Two-factor authentication; principle of least privilege; audit records retained for $>6$ months; AES-256-GCM encryption for storage.

---

## 5. Formal Proof / Engineering Argument (Proof / Engineering Argument)

### Lemma-K-10-07-01: Alert Latency Boundary

**Lemma Statement**: In the described architecture, the total latency upper bound from physiological anomaly occurrence to medical staff receiving a LEVEL_3 alert satisfies clinical requirements:

$$
L_{total} \leq L_{sample} + L_{edge} + L_{transmit} + L_{watermark} + L_{cep} + L_{join} + L_{notify} < 10\text{ s}
$$

**Proof**:

- **Step 1** ($L_{sample}$): The monitor samples at $10\text{ Hz}$; in the worst case the anomaly occurs at the midpoint of a sampling interval: $L_{sample} = \frac{1}{2 \times 10} = 50\text{ ms}$.
- **Step 2** ($L_{edge}$): Data validation and cleansing $< 5\text{ ms}$, local threshold detection $< 5\text{ ms}$, serialization and batching $< 10\text{ ms}$. $L_{edge} \leq 20\text{ ms}$.
- **Step 3** ($L_{transmit}$): Device → edge gateway approximately $10\text{ ms}$, edge → cloud Kafka approximately $50\text{ ms}$. $L_{transmit} = 60\text{ ms}$.
- **Step 4** ($L_{watermark}$): Taking $\delta_{max} = 2\text{ s}$ (sufficiency proven in Prop-K-10-07-02).
- **Step 5** ($L_{cep}$): The shock alert pattern requires 3 consecutive events to match (event interval $100\text{ ms}$), NFA state transition $< 5\text{ ms}$ per event. Shortest detection $215\text{ ms}$; worst case $\approx 2.2\text{ s}$. Take $L_{cep} = 2.2\text{ s}$.
- **Step 6** ($L_{join}$): Broadcast Join $< 5\text{ ms}$; Interval Join for medication events usually already arrived, $< 10\text{ ms}$. $L_{join} \leq 15\text{ ms}$.
- **Step 7** ($L_{notify}$): Flink Sink → Kafka $< 10\text{ ms}$; Kafka → notification service $< 200\text{ ms}$; mobile network to PDA $< 500\text{ ms}$. $L_{notify} \leq 710\text{ ms}$.

**Total Latency**:

$$
L_{total} = 50 + 20 + 60 + 2000 + 2200 + 15 + 710 = 5055\text{ ms} = 5.1\text{ s}
$$

Worst case with 20% system jitter margin: $L_{total}^{proven} = 5.1 \times 1.2 = 6.1\text{ s} < 10\text{ s}$. The alert latency upper bound satisfies clinical requirements. ∎

---

## 6. Example Verification (Examples)

### 6.1 Flink CEP Pattern: Shock Alert

```java
import org.apache.flink.cep.CEP;
import org.apache.flink.cep.pattern.Pattern;
import org.apache.flink.cep.pattern.conditions.IterativeCondition;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.time.Time;
import java.util.List;
import java.util.Map;

public class ShockAlertCEP {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.enableCheckpointing(5000);
        env.getCheckpointConfig().setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE);

        DataStream<VitalSigns> vitals = env
            .fromSource(createKafkaSource("icu-vitals"),
                WatermarkStrategy.<VitalSigns>forBoundedOutOfOrderness(Duration.ofSeconds(2))
                    .withIdleness(Duration.ofSeconds(30)), "Vital Signs")
            .keyBy(VitalSigns::getPatientId);

        Pattern<VitalSigns, ?> shockPattern = Pattern
            .<VitalSigns>begin("hypotension").where(v -> v.getBpSys() < 90)
            .next("bradycardia")
            .where(new IterativeCondition<VitalSigns>() {
                @Override
                public boolean filter(VitalSigns v, Context<VitalSigns> ctx) {
                    List<VitalSigns> hypo = ctx.getEventsForPattern("hypotension");
                    if (hypo.isEmpty()) return false;
                    VitalSigns first = hypo.get(0);
                    return v.getHr() < 60 && (v.getHr() - first.getHr()) < -10
                        && (v.getBpSys() - first.getBpSys()) < -15;
                }
            }).within(Time.minutes(2));

        CEP.pattern(vitals, shockPattern).process(
            new PatternProcessFunction<VitalSigns, AlertEvent>() {
                @Override
                public void processMatch(Map<String, List<VitalSigns>> match,
                        Context ctx, Collector<AlertEvent> out) {
                    VitalSigns h = match.get("hypotension").get(0);
                    VitalSigns b = match.get("bradycardia").get(0);
                    out.collect(new AlertEvent(h.getPatientId(), AlertLevel.LEVEL_3,
                        AlertType.SHOCK, String.format("Shock Alert: BP %d->%d, HR %d->%d",
                            h.getBpSys(), b.getBpSys(), h.getHr(), b.getHr()),
                        ctx.timestamp()));
                }
            }).addSink(new AlertNotificationSink());

        env.execute("ICU Shock Alert Detection");
    }
}

class VitalSigns {
    private String patientId, deviceId; private long timestamp;
    private int hr, bpSys, bpDia; private float spo2, temp;
    public String getPatientId() { return patientId; }
    public int getHr() { return hr; }
    public int getBpSys() { return bpSys; }
}
class AlertEvent {
    private String patientId; private AlertLevel level; private AlertType type;
    private String message; private long alertTimestamp;
    public AlertEvent(String pid, AlertLevel lv, AlertType ty, String msg, long ts) {
        this.patientId = pid; this.level = lv; this.type = ty;
        this.message = msg; this.alertTimestamp = ts;
    }
}
enum AlertLevel { LEVEL_0, LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4 }
enum AlertType { SHOCK, CARDIAC_ARREST, RESPIRATORY_FAILURE, SEPSIS, ARRHYTHMIA }
```

### 6.2 Implementation Results and Hypothetical Data

> 🔮 **Estimated Data** | Basis: Derived from industry reference values and theoretical analysis; not obtained from actual test environments

**Case Background**: A tertiary hospital ICU with 50 beds, admitting 35–40 critically ill patients daily on average.

| Metric | Value |
|--------|-------|
| ICU Beds | 50 |
| Networked Monitors | 200 (average 4 per bed) |
| Data Collection Frequency | 10 Hz (critical monitoring mode) |
| Peak Concurrent Data Streams | 2,000 records/s |
| Edge Gateway Count | 5 (1 per 10 beds, redundant deployment) |
| Cloud Flink Parallelism | 32 (8 TaskManager × 4 slots) |

**Implementation Effect Comparison**:

| Metric | Before (Traditional Polling) | After (Stream Processing System) | Improvement |
|--------|------------------------------|----------------------------------|-------------|
| Anomaly Detection Latency | 5–15 min | **< 500 ms** | ↓99% |
| Alert Notification Latency | 2–5 min | **< 3 s** | ↓95% |
| Shock Alert Accuracy | ~78% | **96.5%** | ↑24% |
| False Positive Rate | ~15% | **< 2%** | ↓87% |
| Nurse Response Time | Avg 4.2 min | **Avg 28 s** | ↓89% |
| Unplanned Rescue Events | 12/month | **4/month** | ↓67% |
| Avg ICU Length of Stay | 8.5 days | **7.2 days** | ↓15% |

**System Performance Benchmark**:

| Performance Metric | Target | Hypothetical Actual |
|--------------------|--------|---------------------|
| End-to-End Latency (p99) | < 5 s | **2.8 s** |
| CEP Pattern Detection Latency | < 3 s | **1.2 s** |
| Multi-Stream Join Latency | < 1 s | **350 ms** |
| Flink Checkpoint Duration | < 30 s | **12 s** |
| System Availability | 99.9% | **99.95%** |
| Data Integrity | 100% | **100%** |

---

## 7. Visualizations (Visualizations)

### 7.1 Overall Architecture of Real-Time Medical Monitoring

```mermaid
graph TB
    subgraph "Bedside Layer (床旁设备层)"
        ECG1[ECG Monitor<br/>(心电监护仪 ECG 500Hz)]
        BP1[Invasive BP Sensor<br/>(有创血压传感器 BP 100Hz)]
        SPO1[Pulse Oximeter<br/>(脉搏血氧仪 SpO2 10Hz)]
        TEMP1[Temperature Probe<br/>(体温探头 Temp 1Hz)]
        PUMP1[Infusion Pump<br/>(输液泵 Medication Events)]
    end

    subgraph "Edge Layer (边缘网关层)"
        GW1[Edge Gateway-1<br/>Flink Embedded]
        GW2[Edge Gateway-2<br/>Flink Embedded]
        GW3[Edge Gateway-N<br/>Flink Embedded]

        subgraph "Edge Processing"
            E_VAL[Data Validation<br/>(数据验证)]
            E_LOC[Local Emergency Detection<br/>(本地紧急检测 LEVEL_3/4)]
            E_AGG[10s Aggregation & Downsampling<br/>(10秒聚合降采样)]
        end
    end

    subgraph "Network Layer"
        MQTT[MQTT Broker]
        KAFKA[Kafka Cluster<br/>SSL/TLS]
    end

    subgraph "Cloud Flink Layer"
        SRC[Kafka Source]
        DES[Privacy De-sanitization<br/>(隐私脱敏)]
        KEY[keyBy patientId]
        CEP[CEP Engine<br/>(CEP引擎)]
        JOIN[Multi-Stream Join<br/>(多流Join)]
        SQL[SQL Window Aggregation<br/>(SQL窗口聚合)]
        AUDIT[Audit Log Sink<br/>(审计日志Sink)]
    end

    subgraph "Storage & Notification"
        REDIS[(Redis<br/>Real-Time Dashboard)]
        INFLUX[(InfluxDB<br/>Time-Series History)]
        OLAP[(OLAP Warehouse)]
        WS[WebSocket<br/>Nurse Station Dashboard]
        PDA[Nurse PDA]
        PAGE[Physician Pager]
    end

    ECG1 & BP1 & SPO1 & TEMP1 & PUMP1 --> MQTT
    MQTT --> GW1 & GW2 & GW3
    GW1 --> E_VAL --> E_LOC --> E_AGG
    E_LOC -.->|LEVEL_4 Local Alarm| BED_ALERT[Bedside Alarm]
    E_AGG --> KAFKA
    KAFKA --> SRC --> DES --> KEY
    KEY --> CEP & JOIN & SQL
    CEP --> PAGE & PDA
    JOIN --> AUDIT
    SQL --> REDIS --> WS
    SQL --> INFLUX
    AUDIT --> OLAP

    style E_LOC fill:#ffcdd2,stroke:#c62828
    style CEP fill:#fff9c4,stroke:#f57f17
    style DES fill:#e1bee7,stroke:#6a1b9a
    style PAGE fill:#ffcdd2,stroke:#c62828
    style BED_ALERT fill:#ff8a80,stroke:#b71c1c
```

**Legend**: Red = Local emergency detection and alarm; Yellow = CEP composite pattern detection; Purple = Privacy de-sanitization processing.

---

### 7.2 CEP Shock Alert Detection Flow

```mermaid
flowchart TD
    START([Vital Signs Data Inflow<br/>(生命体征数据流入 按patientId分区)]) --> INGEST[Event-Time Ordering<br/>(事件时间排序 Watermark delta=2s)]
    INGEST --> BUFFER[NFA State Machine Buffer<br/>(NFA状态机缓冲区)]
    BUFFER --> CHECK1{Systolic BP < 90?<br/>(收缩压 < 90?)}
    CHECK1 -->|No| BUFFER
    CHECK1 -->|Yes| STATE1[Create hypotension State<br/>(创建hypotension状态 记录hr0, bp0)]
    STATE1 --> CHECK2{Within 2 Minutes<br/>(2分钟内 下一事件?)}
    CHECK2 -->|No| TIMEOUT[Pattern Timeout<br/>(模式超时)]
    CHECK2 -->|Yes| CHECK3{HR < 60<br/>and hr < hr0-10<br/>and bp < bp0-15?<br/>(心率 < 60 且hr < hr0-10 且bp < bp0-15?)}
    CHECK3 -->|No| CHECK2
    CHECK3 -->|Yes| MATCH[Pattern Match<br/>(模式匹配 LEVEL_3预警)]
    MATCH --> ENRICH[Multi-Stream Join Enriching<br/>(多流Join enriching)]
    ENRICH --> NOTIFY[Push Notification<br/>(推送通知)]
    NOTIFY --> AUDIT[Audit Log<br/>(审计日志)]
    TIMEOUT --> CLEAN[Clean NFA State<br/>(清理NFA状态)]

    style START fill:#bbdefb,stroke:#1565c0
    style MATCH fill:#ffcdd2,stroke:#c62828
    style NOTIFY fill:#ff8a80,stroke:#b71c1c
    style TIMEOUT fill:#e0e0e0,stroke:#616161
    style CHECK1 fill:#fff9c4,stroke:#f57f17
    style CHECK3 fill:#fff9c4,stroke:#f57f17
```

**Legend**: Blue = Data ingestion; Yellow = CEP condition evaluation; Red = Alert generation and notification; Gray = Timeout cleanup.

---

## 8. References (References)

[^1]: U.S. Department of Health and Human Services, "Health Insurance Portability and Accountability Act (HIPAA) Security Rule", 45 CFR Part 160 and Subparts A and C of Part 164, 2013. <https://www.hhs.gov/hipaa/for-professionals/security/index.html>

[^2]: State Administration for Market Regulation, Standardization Administration of the People's Republic of China, "Information Security Technology — Baseline for Classified Protection of Cybersecurity" (GB/T 22239-2019, MLPS 2.0 / 等保2.0), 2019. <https://www.tc260.org.cn/>

[^3]: Churpek, M.M., Yuen, T.C., Huber, M.T., Park, S.Y., Hall, J.B. and Edelson, D.P., "Predicting Cardiac Arrest on the Wards: A Nested Case-Control Study", *Chest*, 141(5), pp.1170-1176, 2012. DOI: 10.1378/chest.11-1466

---

*Document Version: v2.0 | Created: 2026-04-21 | Last Updated: 2026-04-21 | Status: Complete*
