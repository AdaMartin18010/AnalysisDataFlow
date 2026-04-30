# Real-time Smart Earthquake Warning Case Study

> **Stage**: Knowledge/ Flink/ | **Prerequisites**: [Operator Panoramic Classification (算子全景分类)](./01-concept-atlas/operator-deep-dive/01.06-single-input-operators.md) | [IoT Stream Processing (IoT流处理)](./06-frontier/operator-iot-stream-processing.md) | **Formalization Level**: L4

## 1. Definitions

### Def-EQW-01-01: Smart Earthquake Warning System (智慧地震预警系统)

The **Smart Earthquake Warning System** (智慧地震预警系统) is an integrated system that achieves early earthquake warning, rapid intensity reporting, and emergency response through seismic station networks, P-wave detection, S-wave prediction, and stream computing platforms.

$$\mathcal{E} = (P, S, M, F)$$

Where $P$ is the P-wave detection stream, $S$ is the S-wave analysis stream, $M$ is the station network data stream, and $F$ is the stream computing processing topology.

### Def-EQW-01-02: Warning Lead Time (预警时间窗口)

$$T_{lead} = \frac{D_{epicenter} - D_{station}}{V_S} - T_{process}$$

Where $V_S$ is the S-wave velocity (~3.5 km/s), and $T_{process}$ is the processing latency.

### Def-EQW-01-03: Warning Miss Rate (预警漏报率)

$$MissRate = \frac{N_{missed}}{N_{total}} \cdot 100\%$$

Requirement: $MissRate < 5\%$, false alarm rate $< 10\%$.

## 2. Examples

### 2.1 P-wave Detection

```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

DataStream<SeismicData> seismic = env
    .addSource(new KafkaSource<>("seismic.data"))
    .map(new SeismicParser());

DataStream<PWaveAlert> pWaves = seismic
    .keyBy(s -> s.getStationId())
    .process(new PWaveDetectionFunction() {
        @Override
        public void processElement(SeismicData data, Context ctx,
                                   Collector<PWaveAlert> out) {
            if (data.getAmplitude() > P_THRESHOLD &&
                data.getFrequency() > F_THRESHOLD) {
                out.collect(new PWaveAlert(data.getStationId(),
                    data.getAmplitude(), ctx.timestamp()));
            }
        }
    });

pWaves.addSink(new WarningSink());
```

### 2.2 Epicenter Location

```java
DataStream<PWaveAlert> pWaveAlerts = env.addSource(...);

DataStream<Epicenter> epicenters = pWaveAlerts
    .keyBy(a -> a.getEventId())
    .window(TumblingEventTimeWindows.of(Time.seconds(3)))
    .aggregate(new EpicenterLocationAggregate());

epicenters.addSink(new AlertSink());
```

## 3. References
