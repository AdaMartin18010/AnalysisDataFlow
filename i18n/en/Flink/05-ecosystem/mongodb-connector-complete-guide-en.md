# MongoDB Connector Complete Guide

> **Language**: English | **Translated from**: Flink/05-ecosystem/05.01-connectors/mongodb-connector-complete-guide.md | **Translation date**: 2026-04-20
>
> **Stage**: Flink/04-connectors | **Prerequisites**: [flink-connectors-ecosystem-complete-guide.md](flink-connectors-ecosystem-complete-guide.md), [../../Flink/02-core/exactly-once-end-to-end.md](../../02-core/exactly-once-end-to-end.md) | **Formalization Level**: L4

---

## Table of Contents

- [MongoDB Connector Complete Guide](#mongodb-connector-complete-guide)
  - [Table of Contents](#table-of-contents)
  - [1. Definitions](#1-definitions)
    - [Def-F-04-06 (MongoDB Source Definition)](#def-f-04-06-mongodb-source-definition)
    - [Def-F-04-07 (MongoDB Sink Definition)](#def-f-04-07-mongodb-sink-definition)
    - [Def-F-04-08 (Collection/Document Model)](#def-f-04-08-collectiondocument-model)
    - [Def-F-04-09 (Change Streams CDC)](#def-f-04-09-change-streams-cdc)
    - [Def-F-04-10 (MongoDB Idempotent Write Semantics)](#def-f-04-10-mongodb-idempotent-write-semantics)
  - [2. Properties](#2-properties)
    - [Lemma-F-04-03 (Change Streams Ordering Guarantee)](#lemma-f-04-03-change-streams-ordering-guarantee)
    - [Lemma-F-04-04 (Bulk Write Atomicity Boundary)](#lemma-f-04-04-bulk-write-atomicity-boundary)
    - [Prop-F-04-02 (MongoDB Sink Idempotency Conditions)](#prop-f-04-02-mongodb-sink-idempotency-conditions)
  - [3. Relations](#3-relations)
    - [Relation 1: MongoDB Replica Set to Flink Checkpoint Mapping](#relation-1-mongodb-replica-set-to-flink-checkpoint-mapping)
    - [Relation 2: Change Stream Resume Token to Flink State Backend](#relation-2-change-stream-resume-token-to-flink-state-backend)
    - [Relation 3: BSON Type System to Flink SQL Type Encoding](#relation-3-bson-type-system-to-flink-sql-type-encoding)
  - [4. Argumentation](#4-argumentation)
    - [4.1 Change Stream Event Ordering and Timing Analysis](#41-change-stream-event-ordering-and-timing-analysis)
    - [4.2 Partition Strategy and Parallelism Matching Analysis](#42-partition-strategy-and-parallelism-matching-analysis)
    - [4.3 Idempotent Write and Duplicate Data Processing Boundary](#43-idempotent-write-and-duplicate-data-processing-boundary)
    - [4.4 Connection Pool Configuration and Resource Management Trade-offs](#44-connection-pool-configuration-and-resource-management-trade-offs)
  - [5. Proof / Engineering Argument](#5-proof--engineering-argument)
    - [Thm-F-04-03 (Change Streams Source Exactly-Once Correctness)](#thm-f-04-03-change-streams-source-exactly-once-correctness)
    - [Thm-F-04-04 (MongoDB Sink Idempotent Write Guarantee)](#thm-f-04-04-mongodb-sink-idempotent-write-guarantee)
  - [6. Examples](#6-examples)
    - [6.1 Dependency Configuration](#61-dependency-configuration)
    - [6.2 MongoDB Source Basic Configuration](#62-mongodb-source-basic-configuration)
    - [6.3 Change Streams CDC Mode](#63-change-streams-cdc-mode)
    - [6.4 MongoDB Sink Basic Configuration](#64-mongodb-sink-basic-configuration)
    - [6.5 End-to-End CDC Sync Example](#65-end-to-end-cdc-sync-example)
  - [7. Visualizations](#7-visualizations)
    - [7.1 MongoDB-Flink Integration Architecture](#71-mongodb-flink-integration-architecture)
    - [7.2 Change Streams Event Flow Sequence Diagram](#72-change-streams-event-flow-sequence-diagram)
    - [7.3 Bulk Write Flowchart](#73-bulk-write-flowchart)
    - [7.4 Data Type Mapping Matrix](#74-data-type-mapping-matrix)
  - [8. Configuration Reference](#8-configuration-reference)
    - [8.1 MongoDB Source Configuration Options](#81-mongodb-source-configuration-options)
    - [8.2 MongoDB Sink Configuration Options](#82-mongodb-sink-configuration-options)
    - [8.3 Connection URI Parameters](#83-connection-uri-parameters)
  - [9. References](#9-references)

---

## 1. Definitions

### Def-F-04-06 (MongoDB Source Definition)

MongoDB Source is a Flink Source connector that reads data from MongoDB collections. Let $M = (D, C, Q)$ be a MongoDB data source, where $D$ is the database instance, $C$ is the target collection, and $Q$ is the query filter:

$$\text{MongoSource}(M) = \{ d \mid d \in C \land Q(d) = \text{true} \}$$

**Source Operation Modes**:

| Mode | Description | Applicable Scenarios |
|------|-------------|---------------------|
| **Batch Query Mode** | One-time collection scan with filter projection | Initial loading, offline analysis |
| **Change Streams CDC** | Listen to change streams, capture data changes in real-time | Real-time sync, event-driven processing |
| **Hybrid Mode** | Batch load first, then switch to CDC | Full + incremental sync |

**Intuitive Explanation**: MongoDB Source provides two data ingestion methods. Batch mode is suitable for historical data loading, CDC mode is suitable for real-time change capture. Hybrid mode combines both advantages, supporting incremental sync from any point in time[^1][^3].

### Def-F-04-07 (MongoDB Sink Definition)

MongoDB Sink is an output connector that writes Flink data streams to MongoDB collections. Let $S = (D, C, W, U)$ be a MongoDB Sink, where $D$ is the target database, $C$ is the target collection, $W$ is the write mode, and $U$ is the update strategy:

$$\text{MongoSink}(S, \{r_1, r_2, \dots, r_n\}) = \bigcup_{i=1}^{n} \text{Write}(C, r_i, W, U)$$

**Write Modes**:

| Mode | Semantics | Idempotency |
|------|-----------|-------------|
| **INSERT** | Direct insert, duplicate key error | No |
| **REPLACE** | Replace entire document (upsert) | Yes (with _id) |
| **UPDATE** | Partial field update (upsert) | Yes (with _id) |
| **BULK_WRITE** | Batch mixed operations | Depends on operation type |

**Intuitive Explanation**: The Sink's write mode determines how data maps to MongoDB documents. REPLACE mode is suitable for full sync scenarios, UPDATE mode is suitable for incremental updates. Using the `_id` field to achieve idempotency is the key to ensuring Exactly-Once semantics[^1][^2].

### Def-F-04-08 (Collection/Document Model)

MongoDB adopts a document-oriented data model. Core concepts include:

- **Database**: Physically independent storage unit, corresponding to a namespace in the MongoDB instance
- **Collection**: Logical grouping of documents, no pre-defined Schema required, analogous to a table in relational databases
- **Document**: BSON format data record, key-value pair structure, supports nested documents and arrays

**BSON Document Structure**:

```bson
{
  "_id": ObjectId("..."),           // Unique identifier
  "field1": "string value",         // String type
  "field2": 123,                    // Numeric type
  "nested": {                       // Nested document
    "subField": true
  },
  "tags": ["tag1", "tag2"],         // Array
  "createdAt": ISODate("...")       // Date type
}
```

**Mapping to Relational Model**:

| Relational Database | MongoDB | Flink SQL |
|---------------------|---------|-----------|
| Table | Collection | Table |
| Row | Document | Row |
| Column | Field | Field |
| Primary Key | _id | PRIMARY KEY |
| Index | Index | - |
| Foreign Key | Reference/Embedded | - |

### Def-F-04-09 (Change Streams CDC)

Change Streams is a Change Data Capture (CDC) mechanism provided by MongoDB 3.6+. Let $\mathcal{E}$ be the change event stream, $t$ be the timestamp, and $op$ be the operation type:

$$\text{ChangeStream}(C) = \{ (t_i, op_i, doc_i, fullDoc_i, token_i) \mid t_i \in \mathbb{T}, op_i \in \{\text{insert}, \text{update}, \text{delete}, \text{replace}\} \}$$

**Change Event Structure**:

| Field | Type | Description |
|-------|------|-------------|
| `_id` | Document | Event unique identifier (contains resume token) |
| `operationType` | String | Operation type: insert/update/delete/replace |
| `ns` | Document | Namespace { db, coll } |
| `documentKey` | Document | _id of the modified document |
| `fullDocument` | Document | Full document content (configurable) |
| `updateDescription` | Document | Updated field description (update only) |
| `clusterTime` | Timestamp | Operation timestamp |

**Resume Token Mechanism**:

Resume Token is the position identifier of Change Stream, supporting consumption resumption from any point:

$$\text{Resume}(token_k) \Rightarrow \text{Stream from event } e_{k+1}$$

**Intuitive Explanation**: Change Streams is based on MongoDB oplog (operation log), providing the same strong consistency guarantee as master-slave replication. After persisting the Resume Token to the Flink state backend, precise recovery upon failure can be achieved[^1][^4].

### Def-F-04-10 (MongoDB Idempotent Write Semantics)

Idempotent write guarantees that executing the same operation multiple times produces consistent results. Let $w$ be a write operation and $s$ be the document state:

$$\text{Idempotent}(w) \iff w(w(s)) = w(s)$$

**MongoDB Idempotent Write Implementation**:

| Mechanism | Implementation | Guarantee Level |
|-----------|----------------|-----------------|
| **_id uniqueness** | Document primary key constraint | Single document level |
| **ReplaceOne upsert** | Replace if exists, insert if not | Document level |
| **UpdateOne upsert** | Partial update based on operators | Field level |
| **Transaction (Multi-doc)** | Multi-document ACID transaction | Transaction level |

**Intuitive Explanation**: By mapping Flink data's unique key to the MongoDB `_id` field and combining with upsert semantics, idempotent write at the Sink side can be achieved. This prevents duplicate data when Flink tasks fail and retry[^2][^5].

---

## 2. Properties

### Lemma-F-04-03 (Change Streams Ordering Guarantee)

**Statement**: Events in a single Change Stream are strictly ordered according to the sequence in which operations occurred.

**Formal Statement**: Let $\mathcal{E} = (e_1, e_2, \dots, e_n)$ be the Change Stream event sequence and $t(e)$ be the event timestamp:

$$\forall i, j. \; i < j \Rightarrow t(e_i) \leq t(e_j)$$

**Proof**:

1. Change Stream is based on MongoDB oplog
2. Oplog is a capped collection on the MongoDB primary node, recording all write operations
3. MongoDB guarantees oplog entries are appended in the order operations occurred
4. Change Stream reads oplog in order and generates events
5. Therefore, Change Stream event order is consistent with original operation order

Note: This guarantee is limited to **single collection** Change Streams. In cross-collection or multi-shard scenarios, event order may produce relative disorder due to network latency and other factors[^4]. ∎

### Lemma-F-04-04 (Bulk Write Atomicity Boundary)

**Statement**: The atomicity boundary of MongoDB bulk write operations (BulkWrite) is a single batch, not a single document.

**Formal Statement**: Let $B = \{w_1, w_2, \dots, w_n\}$ be a bulk write batch:

$$\text{Atomic}(B) \iff \forall w \in B. \; \text{Success}(w) \lor \forall w \in B. \; \text{Fail}(w)$$

**Proof**:

1. MongoDB `bulkWrite` operation uses `ordered: true` mode by default
2. In ordered mode, any operation failure aborts subsequent operations
3. Successfully completed operations are not rolled back (without transaction support)
4. When using multi-document transactions, the entire batch is committed as an atomic unit
5. Flink MongoDB Connector's bulk write does not enforce transactions, so the atomicity boundary is at the batch level

Therefore, in abnormal scenarios, bulk write may result in partial success and requires idempotency mechanisms to ensure data consistency[^2]. ∎

### Prop-F-04-02 (MongoDB Sink Idempotency Conditions)

**Statement**: The necessary and sufficient conditions for MongoDB Sink to achieve end-to-end Exactly-Once are: (1) each record has a unique identifier, (2) writes use upsert semantics, (3) Flink Checkpoint is enabled.

**Formal Statement**:

$$
\text{ExactlyOnce}(Sink) \iff \begin{cases}
\exists key(r). \; \forall r. \; \text{unique}(key(r)) \\
\text{WriteMode} \in \{REPLACE, UPDATE\} \land \text{upsert} = \text{true} \\
\text{CheckpointingEnabled} = \text{true}
\end{cases}
$$

**Engineering Argument**:

1. **Unique identifier**: Mapping Flink record's unique key to `_id` ensures repeated writes of the same record target the same document
2. **Upsert semantics**: REPLACE/UPDATE mode with upsert=true achieves "update if exists, insert if not"
3. **Checkpoint mechanism**: Flink two-phase commit guarantees "at least once" writing, and idempotency guarantees "at most once", combining to achieve Exactly-Once

Therefore, when the above three conditions are met, duplicate data will not be generated even if Flink tasks fail and restart[^5]. ∎

---

## 3. Relations

### Relation 1: MongoDB Replica Set to Flink Checkpoint Mapping

MongoDB replica sets provide the high-availability foundation for Change Streams, complementing Flink Checkpoint:

```
┌─────────────────────────────────────────────────────────────┐
│                    MongoDB Replica Set                       │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐             │
│  │ Primary  │────▶│ Secondary│     │ Secondary│             │
│  │ (oplog)  │     │ (sync)   │     │ (sync)   │             │
│  └────┬─────┘     └──────────┘     └──────────┘             │
│       │                                                      │
│       │ Change Stream                                        │
│       ▼                                                      │
│  ┌──────────┐                                                │
│  │  Events  │──────────────┐                                 │
│  └──────────┘              │                                 │
└────────────────────────────┼─────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    Flink Source Operator                     │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐             │
│  │  Event 1 │────▶│  Event 2 │────▶│  Event 3 │             │
│  └────┬─────┘     └────┬─────┘     └────┬─────┘             │
│       │                │                │                   │
│       └────────────────┴────────────────┘                   │
│                     │                                       │
│                     ▼ Checkpoint Barrier                    │
│              ┌──────────────┐                               │
│              │ Resume Token │───▶ State Backend            │
│              │   (offset)   │                               │
│              └──────────────┘                               │
└─────────────────────────────────────────────────────────────┘
```

**Mapping Relations**:

| MongoDB Concept | Flink Concept | Role |
|----------------|---------------|------|
| Primary oplog | Event Source | Change data source |
| Resume Token | Offset / State | Consumption position identifier |
| Secondary election | Failover | High-availability switching |
| Read Concern | Consistency Level | Consistency level |

### Relation 2: Change Stream Resume Token to Flink State Backend

Persistence of the Resume Token is key to fault tolerance for Change Stream Source:

$$\text{State}(checkpoint_k) = \{ token_k, ts_k, \text{pendingEvents}_k \}$$

**State Recovery Flow**:

1. **Checkpoint triggered**: Source writes current Resume Token to state snapshot
2. **Failure occurs**: Flink recovers from the most recent successful Checkpoint
3. **State recovery**: Source reads Resume Token and rebuilds Change Stream cursor
4. **Data replay**: Consumption continues from Resume Token position, may produce duplicate events
5. **Deduplication**: Downstream operators eliminate duplicates through state or Sink idempotency

### Relation 3: BSON Type System to Flink SQL Type Encoding

Mapping from BSON to Flink types is the foundation for data interoperability:

$$\text{Encode}: \text{BSON} \rightarrow \text{Flink SQL Type}$$

| BSON Type | Flink SQL Type | Note |
|-----------|----------------|------|
| ObjectId | STRING | 24-character hexadecimal string |
| String | STRING | Direct mapping |
| Int32 | INT | 32-bit signed integer |
| Int64 | BIGINT | 64-bit signed integer |
| Double | DOUBLE | Double-precision floating point |
| Decimal128 | DECIMAL | High-precision decimal |
| Boolean | BOOLEAN | Boolean value |
| Date | TIMESTAMP | Date and time |
| Array | ARRAY<T> | Element types must be consistent |
| Document | ROW | Nested structure |
| Null | NULL | Null value |

---

## 4. Argumentation

### 4.1 Change Stream Event Ordering and Timing Analysis

**Question**: Can Change Stream guarantee global ordering?

**Analysis**:

1. **Single collection ordering**: Events in a single collection's Change Stream are strictly arranged in oplog order, i.e., the causal order in which operations occurred
2. **Cross-collection disorder**: When multiple Change Streams are consumed concurrently, due to network latency and processing time differences, event arrival order may differ from occurrence order
3. **Sharded cluster**: In sharded clusters, Change Streams need to aggregate oplogs from multiple shards, and disorder may be introduced during aggregation

**Solutions**:

| Scenario | Strategy | Description |
|----------|----------|-------------|
| Strict ordering | Single-partition Source | Sacrifice parallelism for ordering |
| Eventual consistency | Event time + Watermark | Allow brief disorder, process by event time |
| Causal consistency | Business timestamp | Sort using business time fields in documents |

### 4.2 Partition Strategy and Parallelism Matching Analysis

MongoDB Source partition strategy affects read performance:

| Partition Strategy | Principle | Applicable Scenarios |
|--------------------|-----------|---------------------|
| **SplitVector** | Even splitting based on data distribution | Large collections, uniform data distribution |
| **Sample** | Random sampling to estimate boundaries | Unknown data distribution |
| **_id range** | Based on ObjectId time range | Time-series data |
| **Custom** | User-specified partition key | Known optimal partition key |

**Parallelism Matching**:

```
Parallelism = min(partition count, available slot count)
```

- Partition count > parallelism: Some slots process multiple partitions
- Partition count < parallelism: Some slots idle
- Optimal: partition count = parallelism, achieving load balancing

### 4.3 Idempotent Write and Duplicate Data Processing Boundary

**Duplicate Data Sources**:

1. **Source replay**: After Change Stream recovers from Resume Token, previously processed events may be resent
2. **Operator recomputation**: After Flink failure recovery, some operators need to reprocess data
3. **Sink retry**: Write retries due to network timeout

**Idempotent Write Boundary**:

| Idempotency Level | Implementation | Boundary Condition |
|-------------------|----------------|-------------------|
| Document-level | _id + upsert | Duplicate write of same _id |
| Batch-level | Transaction + unique key | Duplicate commit of entire batch |
| Job-level | Job ID + version | Repeated execution of same job instance |

### 4.4 Connection Pool Configuration and Resource Management Trade-offs

MongoDB Java Driver connection pool parameters affect resource usage:

| Parameter | Effect | Trade-off |
|-----------|--------|-----------|
| `maxPoolSize` | Maximum connections | Too large: resource waste; Too small: connection waiting |
| `minPoolSize` | Minimum connections | Too large: idle connections; Too small: frequent creation |
| `maxConnectionLifeTime` | Connection max lifetime | Too long: connection aging; Too short: frequent rebuilding |
| `waitQueueTimeout` | Connection wait timeout | Too long: blocking; Too short: timeout exception |

**Recommended Configuration** (based on Flink parallelism):

```
maxPoolSize = Flink parallelism × 2 + 1
minPoolSize = Flink parallelism
```

---

## 5. Proof / Engineering Argument

### Thm-F-04-03 (Change Streams Source Exactly-Once Correctness)

**Theorem**: When the following conditions are met, MongoDB Change Streams Source combined with Flink Checkpoint can achieve Exactly-Once semantics:

1. Resume Token is persisted to the state backend
2. Change Stream uses `fullDocument: updateLookup` or equivalent option
3. Downstream operators have idempotency or deduplication capability

**Proof**:

**Lemma 1** (Resume Token Monotonicity): MongoDB Resume Token has monotonically increasing characteristics — the token of a new event is always greater than that of an old event.

**Lemma 2** (State Snapshot Consistency): Flink Checkpoint mechanism guarantees atomicity of state snapshots, and Resume Token persistence is synchronized with Checkpoint success.

**Main Proof**:

Let $E = (e_1, e_2, \dots, e_n)$ be the Change Stream event sequence and $C_k$ be the $k$-th Checkpoint.

1. **Normal flow**:
   - Source consumes event $e_i$, advancing Resume Token $token_i$
   - Trigger Checkpoint $C_k$, persist $token_m$ ($m$ is the last event before $C_k$)
   - Checkpoint succeeds, processed events $e_1$ to $e_m$'s Resume Token is saved

2. **Failure recovery**:
   - After failure, Flink recovers from Checkpoint $C_k$
   - Source reads saved $token_m$, rebuilds Change Stream cursor
   - By Lemma 1, new cursor starts consuming from $e_{m+1}$

3. **Boundary analysis**:
   - $e_m$ may have been sent downstream but not confirmed (in-flight)
   - Downstream operators may reprocess $e_m$
   - By condition 3, downstream idempotency or deduplication eliminates duplicates

4. **Exactly-Once guarantee**:
   - No data loss: Resume Token guarantees continuation from $e_{m+1}$
   - No duplicate data: Downstream idempotency eliminates duplicates
   - Therefore Exactly-Once is achieved

∎

### Thm-F-04-04 (MongoDB Sink Idempotent Write Guarantee)

**Theorem**: When using the `_id` field as the unique key combined with upsert semantics, MongoDB Sink achieves idempotent writes.

**Proof**:

Let $d$ be the document to write, $C$ be the target collection, and $s$ be the current collection state.

**Case 1**: Document does not exist (first write)

$$C' = C \cup \{d\} \quad \text{where } d._id \notin \{c._id \mid c \in C\}$$

**Case 2**: Document already exists (duplicate write)

$$\text{Replace}(C, d) = (C \setminus \{c \mid c._id = d._id\}) \cup \{d\}$$

**Idempotency Verification**:

$$\text{Replace}(\text{Replace}(C, d), d) = \text{Replace}(C, d)$$

Two Replace operations result in the same collection state as one Replace, therefore idempotent.

**Extension to Flink Scenario**:

Let $r$ be a Flink record and $f$ be the mapping function $r \rightarrow d$:

$$\text{Idempotent}(Sink) \iff \exists f. \; \forall r. \; f(r)._id = \text{unique}(r)$$

Therefore, as long as:

1. The mapping function generates the same _id for the same record
2. Upsert semantics are used

Sink achieves idempotent writes. ∎

---

## 6. Examples

### 6.1 Dependency Configuration

**Maven Dependencies**:

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-mongodb</artifactId>
    <version>1.2.0</version>
</dependency>

<!-- MongoDB Java Driver (if not included by connector) -->
<dependency>
    <groupId>org.mongodb</groupId>
    <artifactId>mongodb-driver-sync</artifactId>
    <version>4.11.1</version>
</dependency>
```

**Gradle Dependencies**:

```groovy
dependencies {
    implementation 'org.apache.flink:flink-connector-mongodb:1.2.0'
    implementation 'org.mongodb:mongodb-driver-sync:4.11.1'
}
```

### 6.2 MongoDB Source Basic Configuration

**Java API Example** (batch query mode):

```java
import org.apache.flink.connector.mongodb.source.MongoSource;
import org.apache.flink.connector.mongodb.source.config.MongoReadOptions;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

public class MongoDBSourceExample {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(2);

        // Configure MongoDB Source
        MongoSource<Document> mongoSource = MongoSource.<Document>builder()
            .setUri("mongodb://user:password@localhost:27017")
            .setDatabase("mydb")
            .setCollection("users")
            // Query filter - only read documents with age >= 18
            .setFilter(BsonDocument.parse("{ \"age\": { \"$gte\": 18 } }"))
            // Projection optimization - only read needed fields
            .setProjection(BsonDocument.parse("{ \"name\": 1, \"email\": 1, \"_id\": 1 }"))
            // Partition strategy
            .setPartitionStrategy(PartitionStrategy.SAMPLE)
            .setSampleSize(1000)
            // Read options
            .setFetchSize(1000)
            .setLimit(10000L)
            .build();

        DataStream<Document> stream = env.fromSource(
            mongoSource,
            WatermarkStrategy.noWatermarks(),
            "MongoDB Source"
        );

        stream.print();
        env.execute("MongoDB Source Example");
    }
}
```

**SQL API Example**:

```sql
-- Create MongoDB table
CREATE TABLE users (
    _id STRING,
    name STRING,
    email STRING,
    age INT,
    created_at TIMESTAMP(3),
    PRIMARY KEY (_id) NOT ENFORCED
) WITH (
    'connector' = 'mongodb',
    'uri' = 'mongodb://user:password@localhost:27017',
    'database' = 'mydb',
    'collection' = 'users',
    'filter' = '{"age": {"$gte": 18}}',
    'projection' = '{"name": 1, "email": 1, "_id": 1}',
    'partitionStrategy' = 'SAMPLE',
    'fetchSize' = '1000'
);

-- Query data
SELECT name, email, age
FROM users
WHERE age >= 18;
```

### 6.3 Change Streams CDC Mode

**Java API Example** (CDC mode):

```java
import org.apache.flink.connector.mongodb.source.MongoSource;
import org.apache.flink.connector.mongodb.source.config.MongoChangeStreamOptions;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;


public class MongoDBCDCExample {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.enableCheckpointing(60000); // 60 second Checkpoint

        // Configure Change Stream Source
        MongoSource<ChangeStreamDocument<Document>> cdcSource = MongoSource
            .<ChangeStreamDocument<Document>>builder()
            .setUri("mongodb://user:password@localhost:27017/?replicaSet=rs0")
            .setDatabase("mydb")
            .setCollection("orders")
            // Enable Change Streams
            .setChangeStreamOptions(
                MongoChangeStreamOptions.builder()
                    // Full document query - includes complete document after change
                    .setFullDocument(FullDocument.UPDATE_LOOKUP)
                    // Listen operation types
                    .setOperationTypes(
                        OperationType.INSERT,
                        OperationType.UPDATE,
                        OperationType.REPLACE
                    )
                    // Start from current time
                    .setStartAtOperationTime(Instant.now())
                    .build()
            )
            .build();

        DataStream<ChangeStreamDocument<Document>> changeStream = env.fromSource(
            cdcSource,
            WatermarkStrategy.forBoundedOutOfOrderness(
                Duration.ofSeconds(5)
            ),
            "MongoDB CDC Source"
        );

        // Process change events
        changeStream.map(event -> {
            String operation = event.getOperationType().getValue();
            Document fullDoc = event.getFullDocument();
            BsonDocument key = event.getDocumentKey();

            System.out.printf("Operation: %s, Key: %s, Doc: %s%n",
                operation, key, fullDoc);
            return event;
        });

        env.execute("MongoDB CDC Example");
    }
}
```

**Processing Change Events**:

```java
import org.apache.flink.api.common.functions.MapFunction;

// Convert Change Stream events to standard format
public class ChangeStreamProcessor
    implements MapFunction<ChangeStreamDocument<Document>, Row> {

    @Override
    public Row map(ChangeStreamDocument<Document> event) {
        Row row = new Row(5);

        // Operation type: INSERT/UPDATE/DELETE
        row.setField(0, event.getOperationType().getValue());

        // Document primary key
        row.setField(1, event.getDocumentKey().getObjectId("_id").toString());

        // Change timestamp
        row.setField(2, event.getClusterTime());

        // Full document (UPDATE_LOOKUP mode)
        Document fullDoc = event.getFullDocument();
        row.setField(3, fullDoc != null ? fullDoc.toJson() : null);

        // Update description (UPDATE operation only)
        UpdateDescription updateDesc = event.getUpdateDescription();
        row.setField(4, updateDesc != null ? updateDesc.toString() : null);

        return row;
    }
}
```

### 6.4 MongoDB Sink Basic Configuration

**Java API Example** (Replace mode):

```java
import org.apache.flink.connector.mongodb.sink.MongoSink;
import org.apache.flink.connector.mongodb.sink.config.MongoWriteOptions;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;


public class MongoDBSinkExample {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.enableCheckpointing(60000);

        // Input data stream
        DataStream<Document> input = env.fromElements(
            new Document()
                .append("_id", new ObjectId())
                .append("user_id", "U001")
                .append("amount", 100.50)
                .append("status", "completed")
                .append("created_at", new Date())
        );

        // Configure MongoDB Sink
        MongoSink<Document> mongoSink = MongoSink.<Document>builder()
            .setUri("mongodb://user:password@localhost:27017")
            .setDatabase("mydb")
            .setCollection("transactions")
            // Write mode: REPLACE (upsert)
            .setWriteMode(WriteMode.REPLACE)
            // Batch configuration
            .setBatchSize(1000)
            .setBatchIntervalMs(1000)
            // Retry configuration
            .setMaxRetries(3)
            .setRetryIntervalMs(1000)
            // Connection options
            .setMaxConnectionIdleTime(60000)
            .build();

        input.sinkTo(mongoSink);
        env.execute("MongoDB Sink Example");
    }
}
```

**Update Mode Example**:

```java
// [Pseudo-code snippet - not directly runnable] Core logic only
// Configure as Update mode - only update specified fields
MongoSink<Document> updateSink = MongoSink.<Document>builder()
    .setUri("mongodb://user:password@localhost:27017")
    .setDatabase("mydb")
    .setCollection("users")
    .setWriteMode(WriteMode.UPDATE)
    // Update key - for locating document
    .setUpdateKey("_id")
    // Allow upsert
    .setUpsert(true)
    .setBatchSize(500)
    .build();

// Data needs to contain update operators
Document updateDoc = new Document()
    .append("_id", "user001")
    .append("$set", new Document()
        .append("last_login", new Date())
        .append("login_count", 1)
    )
    .append("$inc", new Document()
        .append("visit_count", 1)
    );
```

**SQL API Example**:

```sql
-- Create target table
CREATE TABLE transactions_sink (
    _id STRING,
    user_id STRING,
    amount DECIMAL(10, 2),
    status STRING,
    created_at TIMESTAMP(3),
    PRIMARY KEY (_id) NOT ENFORCED
) WITH (
    'connector' = 'mongodb',
    'uri' = 'mongodb://user:password@localhost:27017',
    'database' = 'mydb',
    'collection' = 'transactions',
    'writeMode' = 'REPLACE',
    'batch.size' = '1000',
    'batch.intervalMs' = '1000',
    'maxRetries' = '3'
);

-- Insert data
INSERT INTO transactions_sink
SELECT
    CAST(user_id AS STRING) as _id,
    user_id,
    amount,
    status,
    created_at
FROM orders
WHERE status = 'completed';
```

### 6.5 End-to-End CDC Sync Example

**Complete CDC Sync Pipeline**:

```java
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.TableEnvironment;


public class MongoDBCDCtoSinkExample {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.enableCheckpointing(60000);

        StreamTableEnvironment tEnv = StreamTableEnvironment.create(env);

        // ========== 1. Configure CDC Source ==========
        MongoSource<ChangeStreamDocument<Document>> cdcSource = MongoSource
            .<ChangeStreamDocument<Document>>builder()
            .setUri("mongodb://srcUser:srcPass@srcHost:27017/?replicaSet=rs0")
            .setDatabase("source_db")
            .setCollection("orders")
            .setChangeStreamOptions(
                MongoChangeStreamOptions.builder()
                    .setFullDocument(FullDocument.UPDATE_LOOKUP)
                    .setOperationTypes(
                        OperationType.INSERT,
                        OperationType.UPDATE,
                        OperationType.REPLACE,
                        OperationType.DELETE
                    )
                    .build()
            )
            .build();

        DataStream<ChangeStreamDocument<Document>> cdcStream = env.fromSource(
            cdcSource,
            WatermarkStrategy.forMonotonousTimestamps(),
            "MongoDB CDC"
        );

        // ========== 2. Process CDC events ==========
        DataStream<Document> processedStream = cdcStream
            .map(new CDCEventTransformer())
            .filter(Objects::nonNull);

        // ========== 3. Configure target Sink ==========
        MongoSink<Document> targetSink = MongoSink.<Document>builder()
            .setUri("mongodb://tgtUser:tgtPass@tgtHost:27017/?replicaSet=rs1")
            .setDatabase("target_db")
            .setCollection("orders_replica")
            .setWriteMode(WriteMode.REPLACE)
            .setUpsert(true)
            .setBatchSize(1000)
            .build();

        // ========== 4. Execute sync ==========
        processedStream.sinkTo(targetSink);
        env.execute("MongoDB CDC Sync");
    }
}

// CDC event transformer
class CDCEventTransformer
    implements MapFunction<ChangeStreamDocument<Document>, Document> {

    @Override
    public Document map(ChangeStreamDocument<Document> event) {
        OperationType opType = event.getOperationType();

        switch (opType) {
            case INSERT:
            case REPLACE:
                // Write full document directly
                return event.getFullDocument();

            case UPDATE:
                // Merge update to full document
                Document fullDoc = event.getFullDocument();
                if (fullDoc != null) {
                    // Add sync marker
                    fullDoc.append("_sync_time", new Date());
                    return fullDoc;
                }
                return null;

            case DELETE:
                // Send delete marker or execute deletion
                BsonDocument key = event.getDocumentKey();
                return new Document()
                    .append("_id", key.getObjectId("_id").getValue())
                    .append("_deleted", true)
                    .append("_deleted_at", new Date());

            default:
                return null;
        }
    }
}
```

---

## 7. Visualizations

### 7.1 MongoDB-Flink Integration Architecture

```mermaid
graph TB
    subgraph MongoDB_Cluster["MongoDB Cluster"]
        RS1["Primary (oplog)"]
        RS2["Secondary"]
        RS3["Secondary"]
        Collection[(Collection)]

        RS1 -->|"replicate"| RS2
        RS1 -->|"replicate"| RS3
        RS1 -->|"read/write"| Collection
    end

    subgraph Flink_Cluster["Flink Cluster"]
        subgraph Source_Operators["Source Operators"]
            S1["MongoSource<br/>Parallelism=2"]
            S2["ChangeStreamSource<br/>Parallelism=1"]
        end

        subgraph Processing["Processing"]
            P1["Map/Filter"]
            P2["Window/Aggregate"]
        end

        subgraph Sink_Operators["Sink Operators"]
            SK1["MongoSink<br/>Replace Mode"]
            SK2["MongoSink<br/>Update Mode"]
        end
    end

    subgraph State_Backend["State Backend"]
        Checkpoint[(Checkpoint)]
        ResumeToken["Resume Token"]
    end

    Collection -->|"Batch Query"| S1
    RS1 -->|"Change Stream"| S2
    S1 --> P1
    S2 --> P1
    P1 --> P2
    P2 --> SK1
    P2 --> SK2
    S2 -.->|"persist"| ResumeToken
    ResumeToken -.->|"snapshot"| Checkpoint
```

### 7.2 Change Streams Event Flow Sequence Diagram

```mermaid
sequenceDiagram
    participant App as Application
    participant FS as Flink Source
    participant MC as MongoDB Client
    participant MP as MongoDB Primary
    participant OP as Oplog

    App->>FS: Create Change Stream
    FS->>MC: watch(collection)
    MC->>MP: Establish cursor
    MP->>OP: Read oplog entries
    OP-->>MC: Stream changes
    MC-->>FS: ChangeStreamDocument
    FS->>FS: Deserialize to Row
    FS->>App: Emit record

    Note over FS,Checkpoint: Checkpoint Triggered
    FS->>FS: snapshotState()
    FS->>Checkpoint: Save Resume Token
    Checkpoint-->>FS: Confirm
    FS->>App: notifyCheckpointComplete()

    Note over App,MP: Failure & Recovery
    MP--xFS: Connection lost
    App->>FS: Restore from checkpoint
    FS->>Checkpoint: Get Resume Token
    FS->>MC: watch() with resumeAfter
    MC->>MP: Resume from token
    MP->>OP: Continue reading
```

### 7.3 Bulk Write Flowchart

```mermaid
flowchart TD
    A["Flink Record Stream"] --> B{"Buffer Records"}
    B -->|"Batch Size >= N"| C["Flush Batch"]
    B -->|"Interval >= T"| C
    C --> D["Create BulkWrite"]
    D --> E["Group by Operation Type"]
    E --> F["Send to MongoDB"]
    F --> G{"Success?"}
    G -->|"Yes"| H["Clear Buffer"]
    G -->|"No"| I{"Retry < Max?"}
    I -->|"Yes"| J["Wait Interval"]
    J --> F
    I -->|"No"| K["Throw Exception"]
    K --> L["Trigger Failover"]
    H --> M["Commit Checkpoint"]
```

### 7.4 Data Type Mapping Matrix

```mermaid
graph LR
    subgraph BSON["BSON Types"]
        B1[ObjectId]
        B2[String]
        B3[Int32]
        B4[Int64]
        B5[Double]
        B6[Decimal128]
        B7[Boolean]
        B8[Date]
        B9[Array]
        B10[Document]
        B11[Null]
    end

    subgraph Flink["Flink SQL Types"]
        F1[STRING]
        F2[STRING]
        F3[INT]
        F4[BIGINT]
        F5[DOUBLE]
        F6[DECIMAL]
        F7[BOOLEAN]
        F8[TIMESTAMP]
        F9[ARRAY<T>]
        F10[ROW]
        F11[NULL]
    end

    B1 -->|"toHexString"| F1
    B2 -->|"direct"| F2
    B3 -->|"intValue"| F3
    B4 -->|"longValue"| F4
    B5 -->|"doubleValue"| F5
    B6 -->|"bigDecimalValue"| F6
    B7 -->|"booleanValue"| F7
    B8 -->|"toInstant"| F8
    B9 -->|"toList"| F9
    B10 -->|"toRow"| F10
    B11 -->|"null"| F11
```

---

## 8. Configuration Reference

### 8.1 MongoDB Source Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `uri` | String | Required | MongoDB connection URI |
| `database` | String | Required | Database name |
| `collection` | String | Required | Collection name |
| `filter` | String | null | Query filter (JSON) |
| `projection` | String | null | Projection fields (JSON) |
| `partitionStrategy` | Enum | `SAMPLE` | Partition strategy: `SAMPLE`, `SPLIT_VECTOR`, `ID_RANGE` |
| `splitSize` | Integer | 64MB | Partition size (bytes) |
| `fetchSize` | Integer | 1000 | Documents per batch |
| `limit` | Long | null | Maximum documents to read |
| `noCursorTimeout` | Boolean | true | Cursor never times out |
| `readPreference` | String | `primary` | Read preference: `primary`, `secondary`, `nearest` |
| `readConcern` | String | `majority` | Read concern level |

**CDC-specific Configuration**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `changeStreamFullDocument` | Enum | `UPDATE_LOOKUP` | Full document mode: `DEFAULT`, `UPDATE_LOOKUP`, `REQUIRED` |
| `changeStreamOperationTypes` | List | all | Operation types to listen |
| `changeStreamStartAt` | String | `now` | Starting point: `now`, `timestamp` |
| `changeStreamResumeAfter` | String | null | Resume from specified Resume Token |

### 8.2 MongoDB Sink Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `uri` | String | Required | MongoDB connection URI |
| `database` | String | Required | Database name |
| `collection` | String | Required | Collection name |
| `writeMode` | Enum | `INSERT` | Write mode: `INSERT`, `REPLACE`, `UPDATE` |
| `upsert` | Boolean | true | Allow upsert (REPLACE/UPDATE) |
| `updateKey` | String | `_id` | Update key field |
| `batchSize` | Integer | 1000 | Batch write size |
| `batchIntervalMs` | Integer | 1000 | Batch interval (milliseconds) |
| `maxRetries` | Integer | 3 | Maximum retry attempts |
| `retryIntervalMs` | Integer | 1000 | Retry interval (milliseconds) |
| `writeConcern` | String | `acknowledged` | Write concern: `w1`, `wmajority`, `jtrue` |

### 8.3 Connection URI Parameters

**Standard URI Format**:

```
mongodb://[username:password@]host1[:port1][,host2[:port2],...[/[database][?options]]
```

**Common Connection Parameters**:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `replicaSet` | Replica set name | `replicaSet=rs0` |
| `authSource` | Authentication database | `authSource=admin` |
| `ssl` | Enable SSL | `ssl=true` |
| `connectTimeoutMS` | Connection timeout | `connectTimeoutMS=10000` |
| `socketTimeoutMS` | Socket timeout | `socketTimeoutMS=0` |
| `maxPoolSize` | Max connection pool | `maxPoolSize=50` |
| `minPoolSize` | Min connection pool | `minPoolSize=10` |
| `maxConnectionLifeTimeMS` | Connection max lifetime | `maxConnectionLifeTimeMS=0` |
| `waitQueueTimeoutMS` | Wait queue timeout | `waitQueueTimeoutMS=5000` |
| `readPreference` | Read preference | `readPreference=secondaryPreferred` |
| `readConcernLevel` | Read concern | `readConcernLevel=majority` |
| `w` | Write concern | `w=majority` |
| `journal` | Journal commit | `journal=true` |

**Complete Example**:

```
mongodb://user:pass@host1:27017,host2:27017,host3:27017/mydb?replicaSet=rs0&authSource=admin&maxPoolSize=50&w=majority&readPreference=secondaryPreferred
```

---

## 9. References

[^1]: Apache Flink Documentation, "MongoDB Connector", 2024. <https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/mongodb/>

[^2]: MongoDB Documentation, "MongoDB Connector for Apache Flink", 2024. <https://www.mongodb.com/docs/kafka-connector/current/>

[^3]: MongoDB Documentation, "Change Streams", 2024. <https://www.mongodb.com/docs/manual/changeStreams/>

[^4]: MongoDB Documentation, "Change Events", 2024. <https://www.mongodb.com/docs/manual/reference/change-events/>

[^5]: Apache Flink Documentation, "Exactly Once Semantics", 2024. <https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/streaming_analytics/>

---

*Document version: v1.0 | Created: 2026-04-19*
