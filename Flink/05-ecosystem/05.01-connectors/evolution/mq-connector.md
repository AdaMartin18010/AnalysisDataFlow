# 消息队列连接器演进 特性跟踪

> 所属阶段: Flink/connectors/evolution | 前置依赖: [MQ Connectors][^1] | 形式化等级: L3

## 1. 概念定义 (Definitions)

### Def-F-Conn-MQ-01: Message Queue

消息队列：
$$
\text{MQ} : \text{Producer} \to \text{Queue} \to \text{Consumer}
$$

### Def-F-Conn-MQ-02: Pub/Sub

发布订阅：
$$
\text{PubSub} : \text{Publisher} \to \{\text{Subscriber}_i\}
$$

## 2. 属性推导 (Properties)

### Prop-F-Conn-MQ-01: Ordering Guarantee

顺序保证：
$$
\text{Partition} \implies \text{Ordering}
$$

## 3. 关系建立 (Relations)

### MQ演进

| 版本 | 特性 | 状态 |
|------|------|------|
| 2.4 | Pulsar支持 | GA |
| 2.4 | Kinesis EFO | GA |
| 2.5 | 更多MQ | GA |
| 3.0 | 统一MQ API | 设计中 |

## 4. 论证过程 (Argumentation)

### 4.1 支持的MQ

| MQ | Source | Sink | 状态 |
|----|--------|------|------|
| RabbitMQ | ✅ | ✅ | GA |
| Pulsar | ✅ | ✅ | GA |
| Kinesis | ✅ | ✅ | GA |
| Pub/Sub | ✅ | ✅ | GA |
| RocketMQ | ✅ | ✅ | GA |

## 5. 形式证明 / 工程论证

### 5.1 Pulsar Source

```java
// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
PulsarSource<String> source = PulsarSource.builder()
    .setServiceUrl("pulsar://localhost:6650")
    .setAdminUrl("http://localhost:8080")
    .setTopics("persistent://public/default/topic")
    .setDeserializationSchema(new SimpleStringSchema())
    .setSubscriptionName("flink-sub")
    .setSubscriptionType(SubscriptionType.Exclusive)
    .build();
```

## 6. 实例验证 (Examples)

### 6.1 RabbitMQ Sink

```java
// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
RMQSink<String> sink = new RMQSink<>(
    new RMQConnectionConfig.Builder()
        .setHost("localhost")
        .setPort(5672)
        .setVirtualHost("/")
        .build(),
    "queue-name",
    new SimpleStringSchema()
);
```

## 7. 可视化 (Visualizations)

```mermaid
graph LR
    A[Producer] --> B[MQ Broker]
    B --> C[Flink Source]
    C --> D[处理]
    D --> E[Flink Sink]
    E --> F[MQ Broker]
    F --> G[Consumer]
```

### 7.1 思维导图：消息队列连接器演进全景

```mermaid
mindmap
  root((消息队列连接器演进))
    Kafka连接器
      0.9至3.x
      Consumer API
      事务生产者
      Exactly-Once
    Pulsar连接器
      分区发现
      Cursor管理
      多租户
      Geo复制
    RabbitMQ连接器
      AMQP
      路由
      队列
      QoS
      死信
    其他MQ
      Kinesis
      RocketMQ
      ActiveMQ
      Pub/Sub
    统一抽象
      Source API统一
      Sink API统一
      配置标准化
```

### 7.2 多维关联树：MQ特性→连接器能力→应用场景

```mermaid
graph TB
    subgraph MQ核心特性
        A1[高吞吐持久化]
        A2[多租户隔离]
        A3[灵活路由]
        A4[云托管弹性]
        A5[顺序保证]
    end

    subgraph 连接器核心能力
        B1[Exactly-Once语义]
        B2[分区动态发现]
        B3[事务生产者]
        B4[Cursor自动管理]
        B5[QoS流控]
        B6[死信队列]
    end

    subgraph 典型应用场景
        C1[实时ETL]
        C2[事件溯源]
        C3[日志聚合]
        C4[流式ML推理]
        C5[跨地域复制]
    end

    A1 --> B1
    A1 --> B3
    A2 --> B2
    A2 --> B4
    A3 --> B5
    A3 --> B6
    A4 --> B2
    A5 --> B1
    B1 --> C1
    B2 --> C4
    B3 --> C2
    B4 --> C5
    B5 --> C3
    B6 --> C1
```

### 7.3 决策树：MQ连接器选型

```mermaid
flowchart TD
    Start([开始选型]) --> Q1{核心需求?}
    Q1 -->|高吞吐持久化| A[Kafka<br/>首选方案]
    Q1 -->|多租户云原生| B[Pulsar]
    Q1 -->|企业集成ESB| C[RabbitMQ / ActiveMQ]
    Q1 -->|云托管免运维| D[Kinesis / Pub/Sub]
    Q1 -->|低延迟金融级| E[RocketMQ]

    A --> A1[百万级TPS]
    A --> A2[分区水平扩展]
    A --> A3[Exactly-Once]

    B --> B1[分层存储]
    B --> B2[Geo复制]
    B --> B3[Function Mesh]

    C --> C1[AMQP协议兼容]
    C --> C2[灵活路由]
    C --> C3[死信队列]

    D --> D1[Serverless]
    D --> D2[自动扩缩容]
    D --> D3[按需计费]

    E --> E1[毫秒级延迟]
    E --> E2[定时消息]
    E --> E3[严格顺序消息]
```

### 7.4 思维导图：消息队列连接器演进阶段

```mermaid
mindmap
  root((消息队列连接器演进))
    早期API
      SourceFunction
      SinkFunction
      简单轮询
    Kafka优先
      Kafka Connector成熟
      生态丰富
      Exactly-Once语义
    多队列支持
      Pulsar Connector
      RabbitMQ Connector
      RocketMQ Connector
      ActiveMQ Connector
    新Source API
      FLIP-27
      Split机制
      Enumerator
      动态发现
    云原生适配
      托管队列
      Serverless消费
      自动伸缩
```

### 7.5 多维关联树：消息队列→连接器特性→Flink能力

```mermaid
graph TB
    subgraph 消息队列
        MQ1[Apache Kafka]
        MQ2[Apache Pulsar]
        MQ3[RabbitMQ]
        MQ4[RocketMQ]
        MQ5[Amazon Kinesis]
        MQ6[MQTT/NATS]
    end

    subgraph 连接器特性
        F1[分区消费]
        F2[事务生产者]
        F3[Cursor管理]
        F4[AMQP路由]
        F5[Serverless消费]
        F6[动态Split发现]
    end

    subgraph Flink能力
        C1[Exactly-Once处理]
        C2[Checkpoint容错]
        C3[动态扩缩容]
        C4[多租户隔离]
        C5[低延迟流处理]
        C6[边缘计算支持]
    end

    MQ1 --> F1
    MQ1 --> F2
    MQ2 --> F3
    MQ2 --> F6
    MQ3 --> F4
    MQ4 --> F1
    MQ5 --> F5
    MQ6 --> F5

    F1 --> C1
    F1 --> C3
    F2 --> C1
    F2 --> C2
    F3 --> C4
    F4 --> C5
    F5 --> C3
    F5 --> C6
    F6 --> C3
```

### 7.6 决策树：MQ连接器选型（简化版）

```mermaid
flowchart TD
    Start([开始MQ连接器选型]) --> Q1{核心需求是什么?}
    Q1 -->|高吞吐持久化| A[Kafka Connector<br/>首选方案]
    Q1 -->|多租户云原生| B[Pulsar Connector]
    Q1 -->|企业集成| C[RabbitMQ / RocketMQ Connector]
    Q1 -->|轻量/边缘场景| D[MQTT / NATS Connector]

    A --> A1[百万级TPS]
    A --> A2[分区水平扩展]
    A --> A3[Exactly-Once语义]

    B --> B1[分层存储]
    B --> B2[Geo复制]
    B --> B3[Function Mesh]

    C --> C1[AMQP协议兼容]
    C --> C2[灵活路由]
    C --> C3[死信队列]

    D --> D1[极小资源占用]
    D --> D2[边缘部署]
    D --> D3[发布订阅轻量化]
```

## 8. 引用参考 (References)

[^1]: Flink MQ Connector Documentation

---

## 跟踪信息

| 属性 | 值 |
|------|-----|
| 版本 | 2.4-3.0 |
| 当前状态 | 演进中 |

---

*文档版本: v1.1 | 更新日期: 2026-04-26*
