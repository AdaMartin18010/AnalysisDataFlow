# Kafka连接器演进 特性跟踪

> 所属阶段: Flink/connectors/evolution | 前置依赖: [Kafka Connector][^1] | 形式化等级: L3

## 1. 概念定义 (Definitions)

### Def-F-Conn-Kafka-01: Source Connector

Kafka Source：
$$
\text{KafkaSource} : \text{Topic} \times \text{Partition} \to \text{Stream}
$$

### Def-F-Conn-Kafka-02: Sink Connector

Kafka Sink：
$$
\text{KafkaSink} : \text{Stream} \to \text{Topic}
$$

## 2. 属性推导 (Properties)

### Prop-F-Conn-Kafka-01: Exactly-Once

Exactly-Once语义：
$$
\text{KafkaSink} + \text{Transactions} \implies \text{Exactly-Once}
$$

## 3. 关系建立 (Relations)

### Kafka连接器演进

| 版本 | 特性 | 状态 |
|------|------|------|
| 2.3 | 旧API | 废弃 |
| 2.4 | FLIP-27 Source | GA |
| 2.5 | 增强Sink | GA |
| 3.0 | 统一API | 设计中 |

## 4. 论证过程 (Argumentation)

### 4.1 Source vs Sink

| 特性 | Source | Sink |
|------|--------|------|
| 分区发现 | 动态 | 静态 |
| 偏移提交 | 自动 | - |
| 事务 | - | 支持 |

## 5. 形式证明 / 工程论证

### 5.1 Kafka Source

```java
KafkaSource<String> source = KafkaSource.<String>builder()
    .setBootstrapServers("kafka:9092")
    .setTopics("input-topic")
    .setGroupId("flink-group")
    .setStartingOffsets(OffsetsInitializer.earliest())
    .setValueOnlyDeserializer(new SimpleStringSchema())
    .build();
```

## 6. 实例验证 (Examples)

### 6.1 Exactly-Once Sink

```java
KafkaSink<String> sink = KafkaSink.<String>builder()
    .setBootstrapServers("kafka:9092")
    .setRecordSerializer(KafkaRecordSerializationSchema.builder()
        .setTopic("output-topic")
        .setValueSerializationSchema(new SimpleStringSchema())
        .build())
    .setDeliveryGuarantee(DeliveryGuarantee.EXACTLY_ONCE)
    .build();
```

## 7. 可视化 (Visualizations)

```mermaid
graph LR
    A[Kafka Topic] --> B[Flink Source]
    B --> C[处理]
    C --> D[Flink Sink]
    D --> E[Kafka Topic]
```

## 8. 引用参考 (References)

[^1]: Flink Kafka Connector Documentation

---

## 跟踪信息

| 属性 | 值 |
|------|-----|
| 版本 | 2.4-3.0 |
| 当前状态 | 演进中 |
