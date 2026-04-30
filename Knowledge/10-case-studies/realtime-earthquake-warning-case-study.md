# 实时智慧地震预警案例研究

> 所属阶段: Knowledge/ Flink/ | 前置依赖: [算子全景分类](../01-concept-atlas/operator-deep-dive/01.06-single-input-operators.md) | [IoT流处理](../06-frontier/operator-iot-stream-processing.md) | 形式化等级: L4

## 1. 概念定义 (Definitions)

### Def-EQW-01-01: 智慧地震预警系统 (Smart Earthquake Warning System)

智慧地震预警系统是通过地震台网、P波检测、S波预测和流计算平台，实现地震早期预警、烈度速报与应急响应的集成系统。

$$\mathcal{E} = (P, S, M, F)$$

其中 $P$ 为P波检测流，$S$ 为S波分析流，$M$ 为台网数据流，$F$ 为流计算处理拓扑。

### Def-EQW-01-02: 预警时间窗口 (Warning Lead Time)

$$T_{lead} = \frac{D_{epicenter} - D_{station}}{V_S} - T_{process}$$

其中 $V_S$ 为S波速度（~3.5 km/s），$T_{process}$ 为处理延迟。

### Def-EQW-01-03: 预警漏报率 (Warning Miss Rate)

$$MissRate = \frac{N_{missed}}{N_{total}} \cdot 100\%$$

要求：$MissRate < 5\%$，误报率 $< 10\%$。

## 2. 实例验证 (Examples)

### 2.1 P波检测

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

### 2.2 震源定位

```java
DataStream<PWaveAlert> pWaveAlerts = env.addSource(...);

DataStream<Epicenter> epicenters = pWaveAlerts
    .keyBy(a -> a.getEventId())
    .window(TumblingEventTimeWindows.of(Time.seconds(3)))
    .aggregate(new EpicenterLocationAggregate());

epicenters.addSink(new AlertSink());
```

## 3. 引用参考 (References)
