# Real-Time Smart Satellite Navigation Augmentation Case Study

> Stage: Knowledge/ Flink/ | Prerequisites: [Operator Panoramic Classification](../Knowledge/01-concept-atlas/operator-deep-dive/01.06-single-input-operators.md) | [IoT Stream Processing](operator-iot-stream-processing.md) | Formalization Level: L4

## 1. Definitions

### Def-SAT-01-01: Smart Satellite Navigation System (智慧卫星导航系统)

A Smart Satellite Navigation System (智慧卫星导航系统) is an integrated system that achieves real-time differential positioning, ionospheric monitoring, and accuracy augmentation through GNSS observation data, reference station networks, ionospheric models, and stream computing platforms.

$$\mathcal{N} = (G, B, I, F)$$

Where $G$ is the GNSS observation stream, $B$ is the reference station data stream, $I$ is the ionospheric parameter stream, and $F$ is the stream computing processing topology.

### Def-SAT-01-02: Real-Time Kinematic Accuracy (实时动态精度)

$$RTK_{accuracy} = \sqrt{\sigma_{N}^2 + \sigma_{E}^2 + \sigma_{U}^2}$$

Requirement: horizontal accuracy $< 2$ cm, vertical accuracy $< 5$ cm.

### Def-SAT-01-03: Ionospheric Delay Correction (电离层延迟改正)

$$I_{delay} = \frac{40.3 \cdot TEC}{f^2}$$

Where $TEC$ is the Total Electron Content, and $f$ is the carrier frequency.

## 2. Examples

### 2.1 Differential Positioning Solution

```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

DataStream<GNSSData> gnss = env
    .addSource(new KafkaSource<>("gnss.observations"))
    .map(new GNSSParser());

DataStream<RTKResult> rtk = gnss
    .keyBy(g -> g.getStationId())
    .process(new RTKFunction() {
        @Override
        public void processElement(GNSSData data, Context ctx,
                                   Collector<RTKResult> out) {
            double[] correction = calculateCorrection(data);
            out.collect(new RTKResult(data.getStationId(),
                data.getPosition(), correction, ctx.timestamp()));
        }
    });

rtk.addSink(new CorrectionSink());
```

### 2.2 Ionospheric Monitoring

```java
DataStream<IonosphereData> iono = env
    .addSource(new KafkaSource<>("gnss.ionosphere"))
    .map(new IonosphereParser());

DataStream<IonosphereAlert> alerts = iono
    .keyBy(i -> i.getRegionId())
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .aggregate(new IonosphereAggregate());

alerts.addSink(new AlertSink());
```

## 3. References

[^1]: IGS, "Real-Time Service (RTS) Product", 2023.
[^2]: RTCA, "Minimum Operational Performance Standards for GPS", DO-229D, 2020.
