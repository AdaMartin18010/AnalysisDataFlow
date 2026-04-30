# Real-Time Smart Firefighting Early Warning Case Study

> Stage: Knowledge/ Flink/ | Prerequisites: [Operator Panorama Classification](../Knowledge/01-concept-atlas/operator-deep-dive/01.06-single-input-operators.md) | [IoT Stream Processing](../Knowledge/06-frontier/operator-iot-stream-processing.md) | Formalization Level: L4

## 1. Definitions

### Def-FIR-01-01: Smart Firefighting System (智慧消防系统)

A Smart Firefighting System is an integrated system that achieves early fire detection, situation assessment, coordinated control, and evacuation command through smoke sensors, temperature sensors, water pressure monitoring devices, and a stream computing platform.

$$\mathcal{F} = (S, T, W, V, C)$$

Where $S$ is the smoke concentration stream, $T$ is the temperature stream, $W$ is the firefighting water pressure stream, $V$ is the video surveillance stream, and $C$ is the stream computing processing topology.

### Def-FIR-01-02: Fire Risk Index (火灾风险指数)

$$FRI = \omega_1 \cdot \frac{S_{actual}}{S_{threshold}} + \omega_2 \cdot \frac{T_{actual}}{T_{threshold}} + \omega_3 \cdot \frac{dT}{dt}$$

Where $\omega_1 + \omega_2 + \omega_3 = 1$, $FRI > 1$ triggers an alarm, and $FRI > 2$ activates the automatic sprinkler system.

### Def-FIR-01-03: Evacuation Time Window (疏散时间窗口)

Available Safe Egress Time:

$$ASET = t_{detect} + t_{response} + t_{travel}$$

Requirement: $ASET < RSET$ (Required Safe Egress Time).

## 2. Examples

### 2.1 Early Fire Detection

```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

DataStream<SensorData> sensors = env
    .addSource(new MqttSource("firefighting/sensor/+/data"))
    .map(new SensorParser());

DataStream<FireAlert> fireAlerts = sensors
    .keyBy(s -> s.getZoneId())
    .process(new FireDetectionFunction() {
        @Override
        public void processElement(SensorData data, Context ctx,
                                   Collector<FireAlert> out) {
            double fri = calculateFRI(data);
            if (fri > 1.0) {
                out.collect(new FireAlert(data.getZoneId(), fri,
                    fri > 2.0 ? "CRITICAL" : "WARNING", ctx.timestamp()));
            }
        }
    });

fireAlerts.addSink(new EmergencySink());
```

### 2.2 Firefighting Water Pressure Monitoring

```java
DataStream<WaterPressure> waterPressure = env
    .addSource(new MqttSource("firefighting/water/pressure"))
    .map(new PressureParser());

DataStream<PressureAlert> pressureAlerts = waterPressure
    .keyBy(p -> p.getZoneId())
    .process(new PressureMonitorFunction() {
        @Override
        public void processElement(WaterPressure pressure, Context ctx,
                                   Collector<PressureAlert> out) {
            if (pressure.getPressure() < 0.1) {
                out.collect(new PressureAlert(pressure.getZoneId(),
                    "LOW_PRESSURE", ctx.timestamp()));
            }
        }
    });

pressureAlerts.addSink(new MaintenanceSink());
```

## 3. References
