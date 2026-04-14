---
title: "MongoDB Connector Detailed Guide"
translation_status: "ai_translated_reviewed"
source_version: "v4.1"
last_sync: "2026-04-15"
---

# MongoDB Connector Detailed Guide

> Stage: Flink | Prerequisites: [data-types-complete-reference.md](./data-types-complete-reference.md) | Formalization Level: L4

---

## 1. Definitions

### Def-F-Mongo-01: MongoDB Source Definition

**Definition**: MongoDB Source is the connector that reads data from a MongoDB collection:

$$
\text{MongoSource} = \langle D, C, Q, M, R \rangle
$$

Where:

- $D$: Database connection configuration $\langle uri, database, collection \rangle$
- $C$: Collection name
- $Q$: Query filter
- $M$: Read mode $\{Batch, ChangeStream, Hybrid\}$
- $R$: Resume Token storage (for CDC)

**Read Mode Semantics**:

| Mode | Description | Applicable Scenario |
|------|-------------|---------------------|
| **Batch** | One-time collection scan | Full sync, offline analysis |
| **ChangeStream** | Listen to change stream | Real-time CDC |
| **Hybrid** | Batch first, then ChangeStream | Full + incremental |

### Def-F-Mongo-02: MongoDB Sink Definition

**Definition**: MongoDB Sink is the connector that writes stream data into MongoDB:

$$
\text{MongoSink} = \langle D, C, W, U, B \rangle
$$

Where:

- $D$: Database connection configuration
- $C$: Target collection
- $W$: Write mode $\{INSERT, REPLACE, UPDATE, BULK\}$
- $U$: Update strategy
- $B$: Batch configuration

**Write Modes**:

| Mode | Semantics | Idempotency |
|------|-----------|-------------|
| INSERT | `insertOne/insertMany` | ❌ No |
| REPLACE | `replaceOne` (upsert) | ✅ Yes (with `_id`) |
| UPDATE | `updateOne` (upsert) | ✅ Yes (with `_id`) |
| BULK | Bulk mixed operations | Depends on specific operation |

### Def-F-Mongo-03: Change Streams Mechanism

**Definition**: Change Streams is MongoDB's CDC mechanism, implemented based on oplog:

$$
\text{ChangeStream} = \langle O, T, F, ResumeToken \rangle
$$

Where:

- $O$: Operation type $\{insert, update, replace, delete, invalidate\}$
- $T$: Timestamp (cluster time)
- $F$: Full document option
- $ResumeToken$: Resume token

**Event Format**:

```json
{
  "_id": {"_data": "<resume_token>"},
  "operationType": "insert",
  "fullDocument": { ... },
  "ns": {"db": "mydb", "coll": "users"},
  "documentKey": {"_id": ObjectId("...")},
  "clusterTime": Timestamp(1234567890, 1)
}
```

---

## 2. Properties

### Lemma-F-Mongo-01: Change Streams Ordering

**Lemma**: Change Streams guarantee ordering within each shard, and causal consistency across shards via `clusterTime`.

**Proof**:

1. MongoDB replication is based on oplog, which is ordered
2. Change Streams read oplog while preserving order
3. In a sharded cluster, `clusterTime` acts as a logical clock ensuring causal order

### Lemma-F-Mongo-02: Bulk Write Atomicity Boundary

**Lemma**: MongoDB bulk write atomicity boundary is at the document level, not the batch level.

**Explanation**:

- `insertMany` is non-atomic: partial failures result in partial success
- Transactions support multi-document atomicity, but with large performance overhead
- Idempotent writes (upsert) can guarantee eventual consistency

### Prop-F-Mongo-01: Resume Token Persistence

**Proposition**: After persisting the Resume Token to the Flink state backend, the job can resume from the checkpoint after recovery.

$$
\text{Resume}(token_{checkpoint}) \Rightarrow \text{No duplicate}, \text{No missing}
$$

---

## 3. Relations

### 3.1 Replica Set and Checkpoint Mapping

```mermaid
graph TB
    subgraph MongoDB ReplicaSet
        P[Primary]
        S1[Secondary 1]
        S2[Secondary 2]
    end

    subgraph Flink Job
        F[MongoSource]
        C[Checkpoint]
    end

    P -->|oplog| S1
    P -->|oplog| S2
    P -->|ChangeStream| F
    F -->|ResumeToken| C

    style P fill:#e8f5e9
    style F fill:#e1f5fe
    style C fill:#fff3e0
```

### 3.2 BSON to Flink Type Mapping

| BSON Type | Flink SQL Type | Description |
|-----------|----------------|-------------|
| ObjectId | STRING | 24-character hexadecimal string |
| String | STRING | UTF-8 string |
| Int32 | INT | 32-bit integer |
| Int64 | BIGINT | 64-bit integer |
| Double | DOUBLE | Double-precision floating point |
| Decimal128 | DECIMAL(38,18) | High-precision decimal |
| Date | TIMESTAMP_LTZ(3) | UTC timestamp |
| Timestamp | TIMESTAMP_LTZ(0) | Internal timestamp |
| Boolean | BOOLEAN | Boolean value |
| Binary | BYTES | Binary data |
| Array | ARRAY | Array type |
| Document | ROW / MAP | Nested document |
| Null | NULL | Null value |

### 3.3 End-to-End Consistency Guarantees

| Combination | Source Guarantee | Sink Guarantee | End-to-End |
|-------------|------------------|----------------|------------|
| ChangeStream + Upsert | At-Least-Once | At-Least-Once | At-Least-Once |
| ChangeStream + Upsert + Checkpoint | At-Least-Once | Exactly-Once | At-Least-Once |
| Transactional Source + Transactional Sink | Exactly-Once | Exactly-Once | Exactly-Once |

---

## 4. Argumentation

### 4.1 Change Stream Event Ordering

**Question**: How to guarantee global ordering in a sharded cluster?

**Analysis**:

1. **Intra-shard ordered**: Each shard's oplog is ordered
2. **Inter-shard unordered**: Changes across different shards have no global order
3. **Causal consistency**: Causal relationships are guaranteed via `clusterTime`
4. **Flink processing**: Watermark alignment + Event Time processing

### 4.2 Idempotent Write Strategy Selection

| Strategy | Implementation | Applicable Scenario |
|----------|----------------|---------------------|
| _id overwrite | `replaceOne({_id}, doc, {upsert:true})` | Full document replacement |
| Field update | `updateOne({_id}, {$set: fields})` | Incremental update |
| Business key | `updateOne({bizKey}, doc, {upsert:true})` | Has business primary key |

---

## 5. Proof / Engineering Argument

### Thm-F-Mongo-01: Change Streams Source Exactly-Once

**Theorem**: With Checkpoint enabled and Resume Token persisted, MongoDB Source provides Exactly-Once semantics.

**Proof Sketch**:

1. **Initial state**: Start reading from the specified Resume Token
2. **At Checkpoint**: Save the current Resume Token
3. **At recovery**: Resume from the saved Resume Token
4. **Idempotency**: MongoDB oplog is idempotent, replaying has no side effects

### Thm-F-Mongo-02: MongoDB Sink Idempotent Writes

**Theorem**: Using REPLACE/UPDATE mode with `_id` specified, the Sink provides idempotent writes.

**Proof**:

- `replaceOne({_id: X}, doc, {upsert: true})` execution result:
  - Document exists → replaced with doc
  - Document does not exist → inserted as doc
- Multiple executions yield the same result
- Therefore it is idempotent

---

## 6. Examples

### 6.1 Maven Dependencies

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

### 6.2 DataStream API - Source Example

```java
import org.apache.flink.connector.mongodb.source.MongoSource;
import org.apache.flink.connector.mongodb.source.reader.deserializer.MongoDeserializationSchema;
import org.bson.BsonDocument;
import org.bson.Document;

// MongoDB Source configuration
MongoSource<Document> mongoSource = MongoSource.<Document>builder()
    .setUri("mongodb://user:password@localhost:27017")
    .setDatabase("mydb")
    .setCollection("events")
    // Query projection
    .setProjection(BsonDocument.parse("{user_id: 1, event_type: 1, _id: 0}"))
    // Paging read configuration
    .setFetchSize(1000)
    .setNoCursorTimeout(true)
    // Deserialization
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

### 6.3 DataStream API - Change Streams Example

```java
import org.apache.flink.connector.mongodb.source.MongoSource;
import org.apache.flink.connector.mongodb.source.enumerator.splitter.MongoSplitters;

// Change Stream Source configuration
MongoSource<ChangeStreamDocument<Document>> changeStreamSource =
    MongoSource.<ChangeStreamDocument<Document>>builder()
        .setUri("mongodb://user:password@localhost:27017")
        .setDatabase("mydb")
        .setCollection("events")
        // Enable Change Stream
        .setChangeStream(true)
        // Full document option
        .setFullDocument(FullDocument.UPDATE_LOOKUP)
        // Resume token (start from specified position)
        .setResumeToken(resumeToken)
        .build();

env.fromSource(
    changeStreamSource,
    WatermarkStrategy.forMonotonousTimestamps(),
    "MongoDB Change Stream"
).map(doc -> {
    // Process change event
    String opType = doc.getOperationType().getValue();
    Document fullDoc = doc.getFullDocument();
    // ... business processing
    return fullDoc;
});
```

### 6.4 DataStream API - Sink Example

```java
import org.apache.flink.connector.mongodb.sink.MongoSink;
import org.apache.flink.connector.mongodb.sink.writer.context.MongoSinkContext;
import org.bson.Document;

// MongoDB Sink configuration
MongoSink<Document> mongoSink = MongoSink.<Document>builder()
    .setUri("mongodb://user:password@localhost:27017")
    .setDatabase("mydb")
    .setCollection("processed_events")
    // Batch configuration
    .setBatchSize(1000)
    .setBatchIntervalMs(1000)
    // Document builder
    .setSerializationSchema((element, context) -> {
        return new Document()
            .append("_id", element.getEventId())  // idempotency key
            .append("user_id", element.getUserId())
            .append("event_type", element.getEventType())
            .append("processed_time", new Date())
            .append("data", element.getData());
    })
    // Write mode: UPSERT
    .setWriteMode(WriteMode.UPSERT)
    .build();

stream.sinkTo(mongoSink);
```

### 6.5 Table API / SQL Example

```sql
-- Create MongoDB table
CREATE TABLE user_events (
    _id STRING,  -- MongoDB document ID
    user_id STRING,
    event_type STRING,
    event_time TIMESTAMP,
    properties MAP<STRING, STRING>
) WITH (
    'connector' = 'mongodb',
    'uri' = 'mongodb://localhost:27017',
    'database' = 'mydb',
    'collection' = 'events',
    -- Read mode
    'scan.fetch-size' = '1000',
    -- Write mode
    'sink.batch.size' = '1000',
    'sink.max-retries' = '3'
);

-- Read from Kafka and write to MongoDB
INSERT INTO user_events
SELECT
    CAST(user_id AS STRING) || '_' || CAST(event_time AS STRING) AS _id,
    user_id,
    event_type,
    event_time,
    properties
FROM kafka_source;
```

---

## 7. Visualizations

### 7.1 MongoDB-Flink Integration Architecture

```mermaid
graph TB
    subgraph MongoDB
        A[Primary Node]
        B[Secondary 1]
        C[Secondary 2]
        D[(Oplog)]
    end

    subgraph Flink
        E[MongoSource] --> F[Transformation]
        F --> G[MongoSink]
    end

    subgraph Modes
        H[Batch Mode] -->|find()| A
        I[ChangeStream Mode] -->|watch()| D
    end

    A --> H
    D --> I
    H -.-> E
    I -.-> E
    G -.->|insert/update| A

    style A fill:#e8f5e9
    style E fill:#e1f5fe
    style G fill:#e1f5fe
```

### 7.2 Change Stream Event Flow

```mermaid
sequenceDiagram
    participant App as Application
    participant Mongo as MongoDB
    participant Flink as Flink Source
    participant State as Flink State

    App->>Mongo: Insert Document
    Mongo->>Mongo: Write Oplog
    Mongo->>Flink: Change Event

    Flink->>Flink: Process Event
    Flink->>State: Update ResumeToken

    opt Checkpoint
        State->>State: Persist ResumeToken
    end

    opt Recovery
        State-->>Flink: Restore ResumeToken
        Flink-->>Mongo: Resume from Token
    end
```

### 7.3 Data Type Mapping Matrix

```mermaid
graph LR
    subgraph BSON
        B1[ObjectId]
        B2[String]
        B3[Int32/Int64]
        B4[Double]
        B5[Date]
        B6[Array]
        B7[Document]
    end

    subgraph Flink SQL
        F1[STRING]
        F2[STRING]
        F3[INT/BIGINT]
        F4[DOUBLE]
        F5[TIMESTAMP_LTZ]
        F6[ARRAY]
        F7[ROW/MAP]
    end

    B1 -->|toHexString| F1
    B2 --> F2
    B3 --> F3
    B4 --> F4
    B5 --> F5
    B6 --> F6
    B7 --> F7
```

---

## 8. References
