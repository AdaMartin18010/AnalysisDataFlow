# 实时智慧消防预警案例研究

> 所属阶段: Knowledge/ Flink/ | 前置依赖: [算子全景分类](../01-concept-atlas/operator-deep-dive/01.06-single-input-operators.md) | [IoT流处理](../06-frontier/operator-iot-stream-processing.md) | 形式化等级: L4

## 1. 概念定义 (Definitions)

### Def-FIR-01-01: 智慧消防系统 (Smart Firefighting System)

智慧消防系统是通过烟雾传感器、温度传感器、水压监测设备和流计算平台，实现火灾早期探测、态势研判、联动控制和疏散指挥的集成系统。

$$\mathcal{F} = (S, T, W, V, C)$$

其中 $S$ 为烟雾浓度流，$T$ 为温度流，$W$ 为消防水压流，$V$ 为视频监控流，$C$ 为流计算处理拓扑。

### Def-FIR-01-02: 火灾风险指数 (Fire Risk Index)

$$FRI = \omega_1 \cdot \frac{S_{actual}}{S_{threshold}} + \omega_2 \cdot \frac{T_{actual}}{T_{threshold}} + \omega_3 \cdot \frac{dT}{dt}$$

其中 $\omega_1 + \omega_2 + \omega_3 = 1$，$FRI > 1$ 触发告警，$FRI > 2$ 启动自动喷淋。

### Def-FIR-01-03: 疏散时间窗口 (Evacuation Time Window)

可用安全疏散时间：

$$ASET = t_{detect} + t_{response} + t_{travel}$$

要求：$ASET < RSET$（必需安全疏散时间）。

## 2. 实例验证 (Examples)

### 2.1 火灾早期探测

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

### 2.2 消防水压监控

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

## 3. 引用参考 (References)
