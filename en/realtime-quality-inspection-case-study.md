# Real-Time Smart Quality Inspection Automation Case Study

> **Stage**: Knowledge/ Flink/ | **Prerequisites**: [Stream Operator Panoramic Taxonomy](operator-taxonomy.md) | [AI/ML Integration](operator-ai-ml-integration.md) | **Formalization Level**: L4

## 1. Definitions

### Def-QIC-01-01: Smart Quality Inspection System (智慧质检系统)

A Smart Quality Inspection System (智慧质检系统) is an integrated system that leverages industrial cameras, sensor data, AI vision models, and stream computing platforms to achieve real-time product defect detection, quality trend analysis, and production line automatic control.

$$\mathcal{Q} = (I, S, M, C, F)$$

Where $I$ denotes the visual image stream, $S$ the sensor data stream, $M$ the AI model inference stream, $C$ the control command stream, and $F$ the stream computing processing topology.

### Def-QIC-01-02: Defect Detection Rate (缺陷检出率)

$$DDR = \frac{N_{detected}}{N_{actual}} \cdot 100\%$$

Requirements: $DDR \geq 99.5\%$ (critical defects), $DDR \geq 95\%$ (general defects).

### Def-QIC-01-03: False Positive Rate (误检率)

$$FPR = \frac{N_{false\_positive}}{N_{total\_inspected}} \cdot 100\%$$

Requirement: $FPR \leq 2\%$.

## 2. Examples

### 2.1 Visual Defect Detection

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

### 2.2 Quality Trend Analysis

```java
DataStream<DefectResult> defectStream = defects
    .keyBy(d -> d.getLineId())
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .aggregate(new QualityTrendAggregate());

defectStream.addSink(new DashboardSink());
```

## 3. References

[^1]: ISO 9001:2015, "Quality Management Systems", 2015.
[^2]: JIS Z 9015-1, "Sampling Inspection Procedures", 2006.
