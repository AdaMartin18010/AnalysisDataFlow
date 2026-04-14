---
title: "Message Queue Connector Evolution Feature Tracking"
translation_status: ai_translated_reviewed
source_version: v4.1
last_sync: "2026-04-15"
---

# Message Queue Connector Evolution Feature Tracking

> Stage: Flink/connectors/evolution | Prerequisites: [MQ Connectors][^1] | Formalization Level: L3

## 1. Definitions

### Def-F-Conn-MQ-01: Message Queue

Message Queue:
$$
\text{MQ} : \text{Producer} \to \text{Queue} \to \text{Consumer}
$$

### Def-F-Conn-MQ-02: Pub/Sub

Publish/Subscribe:
$$
\text{PubSub} : \text{Publisher} \to \{\text{Subscriber}_i\}
$$

## 2. Properties

### Prop-F-Conn-MQ-01: Ordering Guarantee

Ordering Guarantee:
$$
\text{Partition} \implies \text{Ordering}
$$

## 3. Relations

### MQ Evolution

| Version | Feature | Status |
|---------|---------|--------|
| 2.4 | Pulsar Support | GA |
| 2.4 | Kinesis EFO | GA |
| 2.5 | More MQ | GA |
| 3.0 | Unified MQ API | In Design |

## 4. Argumentation

### 4.1 Supported MQ

| MQ | Source | Sink | Status |
|----|--------|------|--------|
| RabbitMQ | ✅ | ✅ | GA |
| Pulsar | ✅ | ✅ | GA |
| Kinesis | ✅ | ✅ | GA |
| Pub/Sub | ✅ | ✅ | GA |
| RocketMQ | ✅ | ✅ | GA |

## 5. Formal Proof / Engineering Argument

### 5.1 Pulsar Source

```java
PulsarSource<String> source = PulsarSource.builder()
    .setServiceUrl("pulsar://localhost:6650")
    .setAdminUrl("http://localhost:8080")
    .setTopics("persistent://public/default/topic")
    .setDeserializationSchema(new SimpleStringSchema())
    .setSubscriptionName("flink-sub")
    .setSubscriptionType(SubscriptionType.Exclusive)
    .build();
```

## 6. Examples

### 6.1 RabbitMQ Sink

```java
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

## 7. Visualizations

```mermaid
graph LR
    A[Producer] --> B[MQ Broker]
    B --> C[Flink Source]
    C --> D[Processing]
    D --> E[Flink Sink]
    E --> F[MQ Broker]
    F --> G[Consumer]
```

## 8. References

[^1]: Flink MQ Connector Documentation

---

## Tracking Information

| Property | Value |
|----------|-------|
| Version | 2.4-3.0 |
| Current Status | Evolving |
