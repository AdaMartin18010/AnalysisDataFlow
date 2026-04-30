# Real-Time Smart Streetlight Energy Management Case Study

> Stage: Knowledge/ Flink/ | Prerequisites: [Operator Panorama Classification (算子全景分类)](01.06-single-input-operators.md) | [IoT Stream Processing (IoT流处理)](operator-iot-stream-processing.md) | Formalization Level: L4

## 1. Definitions

### Def-SLG-01-01: Smart Streetlight Management System (智能路灯管理系统)

A Smart Streetlight Management System is an integrated system that utilizes single-lamp controllers, ambient light sensors, and a stream computing platform to realize remote monitoring, adaptive dimming, fault detection, and energy consumption optimization of streetlights.

$$\mathcal{L} = (P, E, F, C, S)$$

Where $P$ is the streetlight power data stream, $E$ is the ambient light stream, $F$ is the fault alert stream, $C$ is the control command stream, and $S$ is the stream computing processing topology.

### Def-SLG-01-02: Adaptive Dimming Factor (自适应调光系数)

Dynamically adjusts streetlight brightness based on traffic volume and ambient light:

$$Dimming = \alpha \cdot \frac{L_{ambient}}{L_{max}} + \beta \cdot \frac{Traffic_{actual}}{Traffic_{max}}$$

Where $\alpha + \beta = 1$, and $L_{ambient}$ is the ambient illuminance.

### Def-SLG-01-03: Streetlight Availability (路灯完好率)

$$Availability = \frac{N_{working}}{N_{total}} \cdot 100\%$$

Municipal requirement: $Availability \geq 98\%$.

## 2. Examples

### 2.1 Real-Time Streetlight Monitoring

```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

DataStream<LightStatus> lightStatus = env
    .addSource(new MqttSource("streetlight/+/status"))
    .map(new LightParser());

// Fault detection
DataStream<FaultAlert> faults = lightStatus
    .keyBy(s -> s.getPoleId())
    .process(new FaultDetectionFunction() {
        @Override
        public void processElement(LightStatus status, Context ctx,
                                   Collector<FaultAlert> out) {
            if (status.getPower() == 0 && status.getSwitchState().equals("ON")) {
                out.collect(new FaultAlert(status.getPoleId(),
                    "LAMP_FAILURE", ctx.timestamp()));
            }
            if (status.getVoltage() > 250 || status.getVoltage() < 180) {
                out.collect(new FaultAlert(status.getPoleId(),
                    "VOLTAGE_ABNORMAL", ctx.timestamp()));
            }
        }
    });

faults.addSink(new MaintenanceSink());
```

### 2.2 Adaptive Dimming

```java
DataStream<AmbientLight> ambientLight = env
    .addSource(new MqttSource("streetlight/ambient"))
    .map(new AmbientParser());

DataStream<TrafficData> traffic = env
    .addSource(new CameraSource("traffic/flow"))
    .map(new TrafficParser());

DataStream<DimmingCommand> dimming = ambientLight
    .keyBy(a -> a.getZoneId())
    .connect(traffic.keyBy(t -> t.getZoneId()))
    .process(new AdaptiveDimmingFunction() {
        @Override
        public void processElement1(AmbientLight light, Context ctx,
                                   Collector<DimmingCommand> out) {
            double dimmingLevel = calculateDimming(light.getLux(), 0);
            out.collect(new DimmingCommand(light.getZoneId(), dimmingLevel));
        }

        @Override
        public void processElement2(TrafficData traffic, Context ctx,
                                   Collector<DimmingCommand> out) {
            // Update dimming based on traffic
        }
    });

dimming.addSink(new LightControlSink());
```

## 3. References
