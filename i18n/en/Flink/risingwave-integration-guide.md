---
title: "[EN] Risingwave Integration Guide"
translation_status: "ai_translated"
source_file: "Flink/risingwave-integration-guide.md"
source_version: "c9cbd1b6"
translator: "AI"
reviewer: null
translated_at: "2026-04-08T15:15:06.364112"
reviewed_at: null
quality_score: null
terminology_verified: false
---


<!-- AI Translation Template - Replace <!-- TRANSLATE --> markers with actual translation -->

<!-- TRANSLATE: # RisingWave 与 Flink 深度集成指南 -->

<!-- TRANSLATE: > **所属阶段**: Flink/ | **前置依赖**: [Flink vs RisingWave 对比](../../../Knowledge/04-technology-selection/flink-vs-risingwave.md) | **形式化等级**: L5 -->


<!-- TRANSLATE: ## 2. 属性推导 (Properties) -->

<!-- TRANSLATE: ### Lemma-F-RW-01: 端到端延迟上界 -->

<!-- TRANSLATE: **引理**: RisingWave + Flink 集成系统的端到端延迟满足： -->

```
Latency_total ≤ Latency_Flink + Latency_RisingWave + Latency_network + Latency_sync
```

<!-- TRANSLATE: **证明概要**: 延迟是各组件延迟的串联累加，网络传输和同步开销为额外变量。 -->

<!-- TRANSLATE: ### Lemma-F-RW-02: 一致性传递 -->

<!-- TRANSLATE: **引理**: 若 Flink 提供 Exactly-Once 保证，且 RisingWave 提供 At-Least-Once 摄入，则集成系统提供 At-Least-Once 保证。 -->


<!-- TRANSLATE: ## 4. 论证过程 (Argumentation) -->

<!-- TRANSLATE: ### 场景分析：实时数仓分层 -->

<!-- TRANSLATE: **场景**: 使用 Flink 进行数据清洗和转换，RisingWave 进行实时聚合和即席查询。 -->

```
原始数据 → Flink (清洗/转换) → Kafka → RisingWave (聚合) → 应用查询
```

<!-- TRANSLATE: **论证**: -->

<!-- TRANSLATE: 1. **职责分离**: Flink 擅长复杂转换，RisingWave 擅长实时聚合 -->
<!-- TRANSLATE: 2. **存储优化**: RisingWave 的物化视图避免重复计算 -->
<!-- TRANSLATE: 3. **查询灵活性**: RisingWave 支持标准 SQL 即席查询 -->
<!-- TRANSLATE: 4. **运维简化**: 各系统专注擅长领域 -->


<!-- TRANSLATE: ## 6. 实例验证 (Examples) -->

<!-- TRANSLATE: ### 示例 1: Flink → RisingWave Kafka 集成 -->

```java
// Flink Kafka Producer 配置
FlinkKafkaProducer<String> kafkaProducer = new FlinkKafkaProducer<>(
    "processed-events",
    new JsonSerializer(),
    kafkaProperties,
    FlinkKafkaProducer.Semantic.EXACTLY_ONCE
);

stream.addSink(kafkaProducer);
```

```sql
-- RisingWave 消费 Kafka
CREATE SOURCE processed_events (
    user_id VARCHAR,
    event_type VARCHAR,
    amount DECIMAL,
    event_time TIMESTAMP
) WITH (
    connector = 'kafka',
    topic = 'processed-events',
    properties.bootstrap.server = 'kafka:9092'
);

-- 创建物化视图
CREATE MATERIALIZED VIEW hourly_stats AS
SELECT
    window_start,
    event_type,
    COUNT(*) as event_count,
    SUM(amount) as total_amount
FROM TUMBLE(processed_events, event_time, INTERVAL '1 HOUR')
GROUP BY window_start, event_type;
```

<!-- TRANSLATE: ### 示例 2: RisingWave → Flink CDC 集成 -->

```sql
-- RisingWave 创建 CDC Source
CREATE SOURCE user_changes (
    user_id INT PRIMARY KEY,
    user_name VARCHAR,
    updated_at TIMESTAMP
) WITH (
    connector = 'postgres-cdc',
    hostname = 'postgres',
    port = '5432',
    username = 'user',
    password = 'password',
    database.name = 'mydb',
    schema.name = 'public',
    table.name = 'users'
);
```

```java
// Flink CDC 消费 RisingWave (通过 Debezium)
DebeziumSourceFunction<String> source = DebeziumSourceFunction.<String>builder()
    .setBootstrapServers("kafka:9092")
    .setGroupId("flink-rw-cdc")
    .setTopicList("rw.user_changes")
    .build();
```

<!-- TRANSLATE: ### 示例 3: Flink 查询 RisingWave 维表 -->

```java
// Flink JDBC Lookup Join
Table result = tableEnv.sqlQuery(
    "SELECT " +
    "  o.order_id, " +
    "  o.user_id, " +
    "  u.user_name, " +
    "  o.amount " +
    "FROM orders AS o " +
    "LEFT JOIN rw_users FOR SYSTEM_TIME AS OF o.proc_time AS u " +
    "ON o.user_id = u.user_id"
);
```


<!-- TRANSLATE: ## 8. 引用参考 (References) -->
