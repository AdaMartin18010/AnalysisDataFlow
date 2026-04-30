# 实时智慧水务管理案例研究

> 所属阶段: Knowledge/ Flink/ | 前置依赖: [算子全景分类](../01-concept-atlas/operator-deep-dive/01.06-single-input-operators.md) | [IoT流处理](../06-frontier/operator-iot-stream-processing.md) | 形式化等级: L4

## 1. 概念定义 (Definitions)

### Def-WAT-01-01: 智慧水务管理系统 (Smart Water Utility System)

智慧水务管理系统是通过管网传感器、水表数据、水质监测和流计算平台，实现漏损检测、水压优化与水质监控的集成系统。

$$\mathcal{W} = (P, M, Q, F)$$

其中 $P$ 为管网压力流，$M$ 为水表数据流，$Q$ 为水质监测流，$F$ 为流计算处理拓扑。

### Def-WAT-01-02: 漏损指数 (Leakage Index)

$$LI = \frac{Flow_{in} - Flow_{out}}{Flow_{in}} \cdot 100\%$$

目标：$LI < 10\%$（国内先进水平）。

### Def-WAT-01-03: 水质综合指数 (Water Quality Index)

$$WQI = \sum_{i=1}^{n} \omega_i \cdot \frac{C_i}{S_i}$$

其中 $C_i$ 为实测浓度，$S_i$ 为标准限值，$\omega_i$ 为权重。

## 2. 实例验证 (Examples)

### 2.1 漏损检测

```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

DataStream<FlowData> flows = env
    .addSource(new KafkaSource<>("water.flow"))
    .map(new FlowParser());

DataStream<LeakAlert> leaks = flows
    .keyBy(f -> f.getZoneId())
    .window(TumblingEventTimeWindows.of(Time.hours(1)))
    .aggregate(new LeakDetectionAggregate() {
        @Override
        public void aggregate(FlowData flow, Accumulator acc) {
            acc.addIn(flow.getInflow());
            acc.addOut(flow.getOutflow());
            double li = (acc.getIn() - acc.getOut()) / acc.getIn();
            if (li > LEAK_THRESHOLD) {
                out.collect(new LeakAlert(flow.getZoneId(), li));
            }
        }
    });

leaks.addSink(new MaintenanceSink());
```

### 2.2 水质监控

```java
DataStream<QualityData> quality = env
    .addSource(new KafkaSource<>("water.quality"))
    .map(new QualityParser());

DataStream<QualityAlert> alerts = quality
    .keyBy(q -> q.getStationId())
    .process(new QualityMonitorFunction() {
        @Override
        public void processElement(QualityData data, Context ctx,
                                   Collector<QualityAlert> out) {
            double wqi = calculateWQI(data);
            if (wqi > WQI_THRESHOLD) {
                out.collect(new QualityAlert(data.getStationId(), wqi));
            }
        }
    });

alerts.addSink(new AlertSink());
```

## 3. 引用参考 (References)
