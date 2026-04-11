---
title: "[EN] Mongodb Connector Guide"
translation_status: "ai_translated"
source_file: "Flink/mongodb-connector-guide.md"
source_version: "b232efac"
translator: "AI"
reviewer: null
translated_at: "2026-04-08T15:15:06.361353"
reviewed_at: null
quality_score: null
terminology_verified: false
---


<!-- AI Translation Template - Replace <!-- TRANSLATE --> markers with actual translation -->

<!-- TRANSLATE: # MongoDB Connector 详细指南 -->

<!-- TRANSLATE: > 所属阶段: Flink | 前置依赖: [data-types-complete-reference.md](./data-types-complete-reference.md) | 形式化等级: L4 -->


<!-- TRANSLATE: ## 2. 属性推导 (Properties) -->

<!-- TRANSLATE: ### Lemma-F-Mongo-01: Change Streams 有序性 -->

<!-- TRANSLATE: **引理**: Change Streams 保证每个分片内的有序性，分片间通过 `clusterTime` 保证因果一致性。 -->

<!-- TRANSLATE: **证明**： -->

<!-- TRANSLATE: 1. MongoDB 复制基于 oplog，oplog 是有序的 -->
<!-- TRANSLATE: 2. Change Streams 读取 oplog，保持顺序 -->
<!-- TRANSLATE: 3. 分片集群中，`clusterTime` 作为逻辑时钟，保证因果序 -->

<!-- TRANSLATE: ### Lemma-F-Mongo-02: 批量写入原子性边界 -->

<!-- TRANSLATE: **引理**: MongoDB 批量写入的原子性边界为文档级别，而非批量级别。 -->

<!-- TRANSLATE: **说明**： -->

<!-- TRANSLATE: - `insertMany` 非原子性：部分失败时部分成功 -->
<!-- TRANSLATE: - 事务支持多文档原子性，但性能开销大 -->
<!-- TRANSLATE: - 幂等写入（upsert）可保证最终一致性 -->

<!-- TRANSLATE: ### Prop-F-Mongo-01: Resume Token 持久化 -->

<!-- TRANSLATE: **命题**: Resume Token 持久化到 Flink 状态后端后，作业恢复后可从断点续传。 -->

$$
<!-- TRANSLATE: \text{Resume}(token_{checkpoint}) \Rightarrow \text{No duplicate}, \text{No missing} -->
$$


<!-- TRANSLATE: ## 4. 论证过程 (Argumentation) -->

<!-- TRANSLATE: ### 4.1 Change Stream 事件排序 -->

<!-- TRANSLATE: **问题**: 分片集群中如何保证全局有序？ -->

<!-- TRANSLATE: **分析**： -->

<!-- TRANSLATE: 1. **分片内有序**: 每个分片的 oplog 是有序的 -->
<!-- TRANSLATE: 2. **分片间无序**: 不同分片的变更无全局顺序 -->
<!-- TRANSLATE: 3. **因果一致性**: 通过 `clusterTime` 保证因果关系 -->
<!-- TRANSLATE: 4. **Flink 处理**: Watermark 对齐 + Event Time 处理 -->

<!-- TRANSLATE: ### 4.2 幂等写入策略选择 -->

<!-- TRANSLATE: | 策略 | 实现 | 适用场景 | -->
<!-- TRANSLATE: |------|------|----------| -->
<!-- TRANSLATE: | _id 覆盖 | `replaceOne({_id}, doc, {upsert:true})` | 完整文档替换 | -->
| 字段更新 | `updateOne({_id}, {$set: fields})` | 增量更新 |
<!-- TRANSLATE: | 业务键 | `updateOne({bizKey}, doc, {upsert:true})` | 有业务主键 | -->


<!-- TRANSLATE: ## 6. 实例验证 (Examples) -->

<!-- TRANSLATE: ### 6.1 Maven 依赖 -->

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-mongodb</artifactId>
    <version>1.0.1-1.17</version>
</dependency>

<!-- MongoDB Java Driver -->
<dependency>
    <groupId>org.mongodb</groupId>
    <artifactId>mongodb-driver-sync</artifactId>
    <version>4.11.1</version>
</dependency>
```

<!-- TRANSLATE: ### 6.2 DataStream API - Source 示例 -->

```java
import org.apache.flink.connector.mongodb.source.MongoSource;
import org.apache.flink.connector.mongodb.source.reader.deserializer.MongoDeserializationSchema;
import org.bson.BsonDocument;
import org.bson.Document;

// MongoDB Source 配置
MongoSource<Document> mongoSource = MongoSource.<Document>builder()
    .setUri("mongodb://user:password@localhost:27017")
    .setDatabase("mydb")
    .setCollection("events")
    // 查询过滤
    .setProjection(BsonDocument.parse("{user_id: 1, event_type: 1, _id: 0}"))
    // 分页读取配置
    .setFetchSize(1000)
    .setNoCursorTimeout(true)
    // 反序列化
    .setDeserializationSchema(new MongoDeserializationSchema<Document>() {
        @Override
        public Document deserialize(BsonDocument document) {
            return Document.parse(document.toJson());
        }

        @Override
        public TypeInformation<Document> getProducedType() {
            return TypeInformation.of(Document.class);
        }
    })
    .build();

env.fromSource(mongoSource, WatermarkStrategy.noWatermarks(), "MongoDB Source")
    .print();
```

<!-- TRANSLATE: ### 6.3 DataStream API - Change Streams 示例 -->

```java
import org.apache.flink.connector.mongodb.source.MongoSource;
import org.apache.flink.connector.mongodb.source.enumerator.splitter.MongoSplitters;

// Change Stream Source 配置
MongoSource<ChangeStreamDocument<Document>> changeStreamSource =
    MongoSource.<ChangeStreamDocument<Document>>builder()
        .setUri("mongodb://user:password@localhost:27017")
        .setDatabase("mydb")
        .setCollection("events")
        // 启用 Change Stream
        .setChangeStream(true)
        // 全文档选项
        .setFullDocument(FullDocument.UPDATE_LOOKUP)
        // 恢复令牌（从指定位置开始）
        .setResumeToken(resumeToken)
        .build();

env.fromSource(
    changeStreamSource,
    WatermarkStrategy.forMonotonousTimestamps(),
    "MongoDB Change Stream"
).map(doc -> {
    // 处理变更事件
    String opType = doc.getOperationType().getValue();
    Document fullDoc = doc.getFullDocument();
    // ... 业务处理
    return fullDoc;
});
```

<!-- TRANSLATE: ### 6.4 DataStream API - Sink 示例 -->

```java
import org.apache.flink.connector.mongodb.sink.MongoSink;
import org.apache.flink.connector.mongodb.sink.writer.context.MongoSinkContext;
import org.bson.Document;

// MongoDB Sink 配置
MongoSink<Document> mongoSink = MongoSink.<Document>builder()
    .setUri("mongodb://user:password@localhost:27017")
    .setDatabase("mydb")
    .setCollection("processed_events")
    // 批量配置
    .setBatchSize(1000)
    .setBatchIntervalMs(1000)
    // 文档构建
    .setSerializationSchema((element, context) -> {
        return new Document()
            .append("_id", element.getEventId())  // 幂等键
            .append("user_id", element.getUserId())
            .append("event_type", element.getEventType())
            .append("processed_time", new Date())
            .append("data", element.getData());
    })
    // 写入模式：UPSERT
    .setWriteMode(WriteMode.UPSERT)
    .build();

stream.sinkTo(mongoSink);
```

<!-- TRANSLATE: ### 6.5 Table API / SQL 示例 -->

```sql
-- 创建 MongoDB 表
CREATE TABLE user_events (
    _id STRING,  -- MongoDB 文档 ID
    user_id STRING,
    event_type STRING,
    event_time TIMESTAMP,
    properties MAP<STRING, STRING>
) WITH (
    'connector' = 'mongodb',
    'uri' = 'mongodb://localhost:27017',
    'database' = 'mydb',
    'collection' = 'events',
    -- 读取模式
    'scan.fetch-size' = '1000',
    -- 写入模式
    'sink.batch.size' = '1000',
    'sink.max-retries' = '3'
);

-- 从 Kafka 读取并写入 MongoDB
INSERT INTO user_events
SELECT
    CAST(user_id AS STRING) || '_' || CAST(event_time AS STRING) AS _id,
    user_id,
    event_type,
    event_time,
    properties
FROM kafka_source;
```


<!-- TRANSLATE: ## 8. 引用参考 (References) -->
