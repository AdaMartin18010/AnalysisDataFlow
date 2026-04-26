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
// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
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
// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
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

### 7.1 思维导图：Kafka连接器演进全景

以下思维导图以"Kafka连接器演进"为中心，系统展示Source演进、Sink演进、格式支持、高级特性与性能优化五大维度。

```mermaid
mindmap
  root((Kafka连接器演进))
    Source演进
      Consumer API
      新Source API
      分区发现
      动态扩展
    Sink演进
      Producer API
      新Sink API
      事务
      Exactly-Once
      幂等
    格式支持
      JSON
      Avro
      Protobuf
      Schema Registry集成
    高级特性
      Watermark集成
      空闲Source
      Regex订阅
      动态Topic
    性能优化
      批量处理
      压缩
      并行度
      背压协调
```

### 7.2 多维关联树：Kafka版本→连接器特性→Flink收益

以下层次图展示Kafka版本演进如何映射到连接器特性，并转化为Flink应用的工程收益。

```mermaid
graph TB
    subgraph Kafka版本
        K23[Kafka 2.3]
        K24[Kafka 2.4]
        K25[Kafka 2.5]
        K30[Kafka 3.0]
    end

    subgraph 连接器特性
        C23[旧Consumer API<br/>静态分区分配]
        C24[FLIP-27 Source API<br/>动态分区发现<br/>空闲Source]
        C25[新Sink API<br/>事务支持<br/>Exactly-Once]
        C30[统一API<br/>Watermark集成<br/>Regex订阅]
    end

    subgraph Flink收益
        F23[基础吞吐]
        F24[弹性扩展<br/>动态发现]
        F25[端到端Exactly-Once<br/>幂等写入]
        F30[完整流处理语义<br/>Schema进化]
    end

    K23 --> C23 --> F23
    K24 --> C24 --> F24
    K25 --> C25 --> F25
    K30 --> C30 --> F30
```

### 7.3 决策树：Kafka连接器配置选型

以下决策树针对四类典型场景给出配置策略与关键参数建议。

```mermaid
flowchart TD
    Start([开始配置Kafka连接器]) --> Q1{场景需求?}

    Q1 -->|低延迟| A1[小批量<br/>频繁Flush<br/>低Watermark]
    Q1 -->|高吞吐| A2[大批量<br/>压缩<br/>并行度优化]
    Q1 -->|高可靠| A3[Exactly-Once<br/>事务<br/>Checkpoint]
    Q1 -->|灵活消费| A4[动态发现<br/>Regex订阅<br/>Schema进化]

    A1 --> B1[配置参数:<br/>linger.ms=0<br/>batch.size=small]
    A2 --> B2[配置参数:<br/>compression.type=lz4<br/>parallelism=分区数]
    A3 --> B3[配置参数:<br/>delivery.guarantee=EXACTLY_ONCE<br/>transactional.id.prefix=flink]
    A4 --> B4[配置参数:<br/>topic-pattern=regex<br/>properties.auto.offset.reset=earliest]
```

## 8. 引用参考 (References)

[^1]: Flink Kafka Connector Documentation
[^2]: Apache Flink Documentation, "Kafka Source", https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/kafka/
[^3]: Apache Flink Documentation, "Kafka Connector - Exactly Once", https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/kafka/#exactly-once
[^4]: Apache Kafka Documentation, "Apache Kafka 官方文档", https://kafka.apache.org/documentation/
[^5]: Confluent, "Kafka Schema Registry 指南", https://docs.confluent.io/platform/current/schema-registry/index.html

---

## 跟踪信息

| 属性 | 值 |
|------|-----|
| 版本 | 2.4-3.0 |
| 当前状态 | 演进中 |

---

*文档版本: v1.0 | 创建日期: 2026-04-19*
