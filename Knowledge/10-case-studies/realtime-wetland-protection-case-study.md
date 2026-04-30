# 实时智慧湿地保护案例研究

> 所属阶段: Knowledge/ Flink/ | 前置依赖: [算子全景分类](../01-concept-atlas/operator-deep-dive/01.06-single-input-operators.md) | [IoT流处理](../06-frontier/operator-iot-stream-processing.md) | 形式化等级: L4

## 1. 概念定义 (Definitions)

### Def-WET-01-01: 智慧湿地保护系统 (Smart Wetland Protection System)

智慧湿地保护系统是通过水质监测、鸟类追踪、生态相机和流计算平台，实现水质预警、物种监测与生态评估的集成系统。

$$\mathcal{W} = (Q, B, C, F)$$

其中 $Q$ 为水质数据流，$B$ 为鸟类追踪流，$C$ 为生态相机流，$F$ 为流计算处理拓扑。

### Def-WET-01-02: 湿地健康指数 (Wetland Health Index)

$$WHI = \omega_1 \cdot WQI + \omega_2 \cdot Biodiversity + \omega_3 \cdot Hydrology$$

$WHI > 0.8$ 表示健康，$WHI < 0.5$ 表示退化。

### Def-WET-01-03: 鸟类多样性指数 (Bird Diversity Index)

$$BDI = -\sum_{i=1}^{n} p_i \cdot \ln(p_i)$$

其中 $p_i$ 为第 $i$ 种鸟类的比例。

## 2. 实例验证 (Examples)

### 2.1 水质监测

```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

DataStream<WaterQuality> quality = env
    .addSource(new KafkaSource<>("wetland.quality"))
    .map(new QualityParser());

DataStream<QualityAlert> alerts = quality
    .keyBy(q -> q.getStationId())
    .process(new QualityMonitorFunction() {
        @Override
        public void processElement(WaterQuality data, Context ctx,
                                   Collector<QualityAlert> out) {
            if (data.getCod() > 30 || data.getAmmonia() > 2) {
                out.collect(new QualityAlert(data.getStationId(),
                    data.getCod(), data.getAmmonia()));
            }
        }
    });

alerts.addSink(new AlertSink());
```

### 2.2 鸟类追踪

```java
DataStream<BirdData> birds = env
    .addSource(new KafkaSource<>("wetland.birds"))
    .map(new BirdParser());

DataStream<BirdReport> reports = birds
    .keyBy(b -> b.getWetlandId())
    .window(TumblingEventTimeWindows.of(Time.days(1)))
    .aggregate(new BirdAggregate());

reports.addSink(new DashboardSink());
```

## 3. 引用参考 (References)
