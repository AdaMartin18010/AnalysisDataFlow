# 实时智慧草原管理案例研究

> 所属阶段: Knowledge/ Flink/ | 前置依赖: [算子全景分类](../01-concept-atlas/operator-deep-dive/01.06-single-input-operators.md) | [IoT流处理](../06-frontier/operator-iot-stream-processing.md) | 形式化等级: L4

## 1. 概念定义 (Definitions)

### Def-GRA-01-01: 智慧草原管理系统 (Smart Grassland Management System)

智慧草原管理系统是通过卫星遥感、地面监测、放牧数据和流计算平台，实现草畜平衡、生态监测与火灾预警的集成系统。

$$\mathcal{G} = (S, G, H, F)$$

其中 $S$ 为卫星遥感流，$G$ 为地面监测流，$H$ 为放牧数据流，$F$ 为流计算处理拓扑。

### Def-GRA-01-02: 草畜平衡指数 (Grass-Livestock Balance Index)

$$GLBI = \frac{Grass_{available}}{Livestock_{need}}$$

$GLBI < 0.8$ 提示超载，需调整放牧量。

### Def-GRA-01-03: 植被覆盖度 (Vegetation Coverage)

$$VC = \frac{A_{vegetation}}{A_{total}} \cdot 100\%$$

目标：$VC \geq 60\%$。

## 2. 实例验证 (Examples)

### 2.1 放牧监测

```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

DataStream<GrazingData> grazing = env
    .addSource(new KafkaSource<>("grassland.grazing"))
    .map(new GrazingParser());

DataStream<OverloadAlert> overloads = grazing
    .keyBy(g -> g.getPastureId())
    .window(TumblingEventTimeWindows.of(Time.days(1)))
    .aggregate(new BalanceAggregate() {
        @Override
        public void aggregate(GrazingData data, Accumulator acc) {
            acc.addLivestock(data.getLivestockCount());
            acc.addGrass(data.getGrassArea());
            double glbi = acc.getGrass() / (acc.getLivestock() * NEED_PER_HEAD);
            if (glbi < 0.8) {
                out.collect(new OverloadAlert(data.getPastureId(), glbi));
            }
        }
    });

overloads.addSink(new AlertSink());
```

### 2.2 火灾监测

```java
DataStream<SatelliteData> satellites = env
    .addSource(new KafkaSource<>("grassland.satellite"))
    .map(new SatelliteParser());

DataStream<FireAlert> fires = satellites
    .keyBy(s -> s.getGridId())
    .process(new FireDetectionFunction() {
        @Override
        public void processElement(SatelliteData data, Context ctx,
                                   Collector<FireAlert> out) {
            if (data.getTemperature() > 50 && data.getNdvi() < 0.2) {
                out.collect(new FireAlert(data.getGridId(),
                    data.getTemperature()));
            }
        }
    });

fires.addSink(new EmergencySink());
```

## 3. 引用参考 (References)

[^1]: 农业农村部, "全国草原监测报告", 2023.
[^2]: FAO, "Grassland and Pasture Management", 2021.
