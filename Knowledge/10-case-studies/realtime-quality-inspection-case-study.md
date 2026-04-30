# 实时智慧质检自动化案例研究

> 所属阶段: Knowledge/ Flink/ | 前置依赖: [算子全景分类](../01-concept-atlas/operator-deep-dive/01.06-single-input-operators.md) | [AI/ML集成](../06-frontier/operator-ai-ml-integration.md) | 形式化等级: L4

## 1. 概念定义 (Definitions)

### Def-QIC-01-01: 智慧质检系统 (Smart Quality Inspection System)

智慧质检系统是通过工业相机、传感器数据、AI视觉模型和流计算平台，实现产品缺陷实时检测、质量趋势分析与产线自动控制的集成系统。

$$\mathcal{Q} = (I, S, M, C, F)$$

其中 $I$ 为视觉图像流，$S$ 为传感器数据流，$M$ 为AI模型推理流，$C$ 为控制指令流，$F$ 为流计算处理拓扑。

### Def-QIC-01-02: 缺陷检出率 (Defect Detection Rate)

$$DDR = \frac{N_{detected}}{N_{actual}} \cdot 100\%$$

要求：$DDR \geq 99.5\%$（关键缺陷），$DDR \geq 95\%$（一般缺陷）。

### Def-QIC-01-03: 误检率 (False Positive Rate)

$$FPR = \frac{N_{false\_positive}}{N_{total\_inspected}} \cdot 100\%$$

要求：$FPR \leq 2\%$。

## 2. 实例验证 (Examples)

### 2.1 视觉缺陷检测

```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

DataStream<ImageData> images = env
    .addSource(new CameraSource("inspection/camera"))
    .map(new ImageParser());

// AI inference
DataStream<DefectResult> defects = images
    .map(new AIInferenceFunction() {
        @Override
        public DefectResult map(ImageData image) {
            float[] features = extractFeatures(image);
            float score = model.predict(features);
            return new DefectResult(image.getProductId(),
                score > THRESHOLD ? "DEFECT" : "PASS", score);
        }
    });

// Alert on critical defects
defects
    .filter(d -> d.getType().equals("DEFECT") && d.getScore() > 0.9)
    .addSink(new RejectSink());
```

### 2.2 质量趋势分析

```java
DataStream<DefectResult> defectStream = defects
    .keyBy(d -> d.getLineId())
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .aggregate(new QualityTrendAggregate());

defectStream.addSink(new DashboardSink());
```

## 3. 引用参考 (References)
