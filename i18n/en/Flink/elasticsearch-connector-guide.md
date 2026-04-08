---
title: "[EN] Elasticsearch Connector Guide"
translation_status: "ai_translated"
source_file: "Flink/elasticsearch-connector-guide.md"
source_version: "b53b2253"
translator: "AI"
reviewer: null
translated_at: "2026-04-08T15:15:06.344998"
reviewed_at: null
quality_score: null
terminology_verified: false
---


<!-- AI Translation Template - Replace <!-- TRANSLATE --> markers with actual translation -->

<!-- TRANSLATE: # Elasticsearch Connector 详细指南 -->

<!-- TRANSLATE: > 所属阶段: Flink | 前置依赖: [data-types-complete-reference.md](./data-types-complete-reference.md) | 形式化等级: L4 -->


<!-- TRANSLATE: ## 2. 属性推导 (Properties) -->

<!-- TRANSLATE: ### Lemma-F-ES-01: 批量大小与延迟权衡 -->

<!-- TRANSLATE: **引理**: 增大 `bulk.flush.max.actions` 可提高吞吐但增加延迟： -->

$$
<!-- TRANSLATE: \text{Latency} \approx \frac{N_{actions}}{\lambda_{arrival}} + RTT_{network} + T_{processing} -->
$$

$$
<!-- TRANSLATE: \text{Throughput} \approx \frac{N_{actions}}{\text{Latency}} -->
$$

<!-- TRANSLATE: 其中： -->

- $\lambda_{arrival}$: 记录到达率
- $RTT_{network}$: 网络往返延迟
- $T_{processing}$: ES 处理时间

<!-- TRANSLATE: ### Lemma-F-ES-02: 写入性能边界 -->

<!-- TRANSLATE: **引理**: ES Sink 的最大吞吐量受以下因素约束： -->

$$
<!-- TRANSLATE: T_{max} = \min(T_{bulk}, T_{es}, T_{network}) -->
$$

<!-- TRANSLATE: 其中： -->

- $T_{bulk}$: Bulk API 吞吐
- $T_{es}$: ES 集群索引能力（分片数 × 单分片吞吐）
- $T_{network}$: 网络带宽 / 平均文档大小

<!-- TRANSLATE: ### Prop-F-ES-01: 版本冲突处理 -->

<!-- TRANSLATE: **命题**: 当多个并发写入同一文档时： -->

$$
<!-- TRANSLATE: \text{if } (v_{provided} = v_{current}) \lor (v_{provided} > v_{current}) \Rightarrow \text{update succeeds} -->
$$

$$
<!-- TRANSLATE: \text{if } v_{provided} < v_{current} \Rightarrow \text{VersionConflictException} -->
$$


<!-- TRANSLATE: ## 4. 论证过程 (Argumentation) -->

<!-- TRANSLATE: ### 4.1 索引名称动态化策略 -->

<!-- TRANSLATE: **策略对比**： -->

<!-- TRANSLATE: | 策略 | 实现方式 | 适用场景 | -->
<!-- TRANSLATE: |------|----------|----------| -->
<!-- TRANSLATE: | 静态索引 | 固定索引名 | 小规模数据 | -->
<!-- TRANSLATE: | 时间轮转 | `logs-{date}` | 日志场景 | -->
<!-- TRANSLATE: | 字段路由 | 基于记录字段 | 多租户场景 | -->

<!-- TRANSLATE: ### 4.2 失败处理策略 -->

<!-- TRANSLATE: | 策略 | 行为 | 数据保证 | -->
<!-- TRANSLATE: |------|------|----------| -->
<!-- TRANSLATE: | Ignore | 忽略失败 | 可能丢数据 | -->
<!-- TRANSLATE: | Fail | 作业失败 | 严格一致性 | -->
<!-- TRANSLATE: | Retry | 指数退避重试 | 最终一致性 | -->
<!-- TRANSLATE: | DLQ | 写入死信队列 | 可审计恢复 | -->


<!-- TRANSLATE: ## 6. 实例验证 (Examples) -->

<!-- TRANSLATE: ### 6.1 Maven 依赖 -->

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-elasticsearch7</artifactId>
    <version>3.0.1-1.17</version>
</dependency>

<!-- 或使用 Elasticsearch 8 -->
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-elasticsearch8</artifactId>
    <version>3.0.1-1.17</version>
</dependency>
```

<!-- TRANSLATE: ### 6.2 DataStream API 示例 -->

```java
import org.apache.flink.connector.elasticsearch.sink.Elasticsearch7SinkBuilder;
import org.apache.flink.connector.elasticsearch.sink.ElasticsearchEmitter;
import org.apache.http.HttpHost;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.client.Requests;

import java.util.HashMap;
import java.util.Map;

// 创建 ES Sink
ElasticsearchSink<Event> esSink = new Elasticsearch7SinkBuilder<Event>()
    .setBulkFlushMaxActions(1000)
    .setBulkFlushInterval(5000)
    .setHosts(new HttpHost("localhost", 9200))
    // 认证配置（如果需要）
    .setRestClientFactory(
        restClientBuilder -> {
            restClientBuilder.setDefaultHeaders(
                new Header[]{new BasicHeader("Authorization", "ApiKey xxx")}
            );
        }
    )
    // 文档构建
    .setEmitter((element, context, indexer) -> {
        Map<String, Object> json = new HashMap<>();
        json.put("user_id", element.getUserId());
        json.put("event_type", element.getEventType());
        json.put("timestamp", element.getTimestamp());
        json.put("data", element.getData());

        IndexRequest request = Requests.indexRequest()
            .index("events-" + element.getDate())
            .id(element.getEventId())  // 设置 _id 实现幂等
            .source(json);

        indexer.add(request);
    })
    .build();

// 添加到流
stream.sinkTo(esSink);
```

<!-- TRANSLATE: ### 6.3 Table API / SQL 示例 -->

```sql
-- 创建 Elasticsearch 表
CREATE TABLE user_events (
    user_id STRING,
    event_type STRING,
    event_time TIMESTAMP,
    properties MAP<STRING, STRING>,
    -- 元数据列
    INDEX VARCHAR METADATA FROM 'index'
) WITH (
    'connector' = 'elasticsearch-7',
    'hosts' = 'http://localhost:9200',
    'index' = 'user-events-{event_time|yyyy.MM.dd}',
    'document-id' = 'user_id-event_time',
    'bulk-flush.max-actions' = '1000',
    'bulk-flush.interval' = '5000',
    'format' = 'json'
);

-- 写入数据
INSERT INTO user_events
SELECT
    user_id,
    event_type,
    event_time,
    properties
FROM kafka_source;
```

<!-- TRANSLATE: ### 6.4 配置模板 -->

```java
// 高级配置示例
ElasticsearchSink<Event> esSink = new Elasticsearch7SinkBuilder<Event>()
    // 批量配置
    .setBulkFlushMaxActions(1000)
    .setBulkFlushMaxSizeMb(5)
    .setBulkFlushInterval(5000)

    // 重试配置
    .setBulkFlushBackoffStrategy(
        ElasticsearchSinkBase.FlushBackoffType.EXPONENTIAL,
        8,    // 最大重试次数
        1000  // 初始重试间隔(ms)
    )

    // 连接配置
    .setHosts(
        new HttpHost("es-node1", 9200),
        new HttpHost("es-node2", 9200),
        new HttpHost("es-node3", 9200)
    )

    // 失败处理
    .setFailureHandler(new RetryRejectedExecutionFailureHandler())

    // 文档构建器
    .setEmitter(new MyElasticsearchEmitter())
    .build();
```


<!-- TRANSLATE: ## 8. 引用参考 (References) -->
