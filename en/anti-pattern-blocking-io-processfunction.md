# Anti-Pattern AP-05: Blocking I/O in ProcessFunction

> **Stage**: Knowledge/09-anti-patterns | **Prerequisites**: [Async I/O Pattern](pattern-async-io-enrichment.md) | **Formalization Level**: L3
> **Translation Date**: 2026-04-21

## Abstract

Executing synchronous blocking I/O calls (database queries, HTTP requests) inside `ProcessFunction` blocks the subtask thread, dramatically reducing throughput. This anti-pattern formalizes the throughput impact and provides async alternatives.

---

## 1. Definition

### Def-K-09-05 (Blocking I/O in ProcessFunction)

**Blocking I/O in ProcessFunction** means calling blocking external services (database, cache, HTTP API, RPC) inside synchronous methods like `processElement` or `onTimer`, causing the subtask thread to suspend and wait.

**Throughput impact**:

$$\text{Throughput} = \frac{1}{T_{proc}} = \frac{1}{T_{compute} + T_{io}}$$

When $T_{io} \gg T_{compute}$, throughput collapses.

**Example**: If $T_{compute} = 1\mu s$ and $T_{io} = 10ms$, throughput drops from 1M records/s to 100 records/s—a **10,000x degradation**.

---

## 2. Symptoms

- Subtask `backPressuredTimeMsPerSecond` is high
- Low throughput despite low CPU utilization
- Time spent in `processElement` is dominated by I/O wait
- Thread dumps show threads stuck in socket read/write

## 3. Negative Impacts

### 3.1 Throughput Impact

| $T_{io}$ | Throughput (records/s) | Degradation |
|----------|------------------------|-------------|
| 0 (no I/O) | 1,000,000 | Baseline |
| 1ms | 1,000 | 1000x |
| 10ms | 100 | 10,000x |
| 100ms | 10 | 100,000x |

### 3.2 Cascade Impact

Blocking one subtask creates backpressure upstream, eventually stalling the entire pipeline.

---

## 4. Solution

### 4.1 Use AsyncFunction

```java
// Async lookup to external database
class AsyncDatabaseLookup extends RichAsyncFunction<Row, Row> {
    private transient AsyncDatabaseClient client;
    
    @Override
    public void open(Configuration parameters) {
        client = new AsyncDatabaseClient(...);
    }
    
    @Override
    public void asyncInvoke(Row input, ResultFuture<Row> resultFuture) {
        client.queryAsync(input.getKey())
            .thenAccept(result -> resultFuture.complete(
                Collections.singletonList(join(input, result))
            ));
    }
}

// Apply async function
DataStream<Row> enriched = AsyncDataStream.unorderedWait(
    inputStream,
    new AsyncDatabaseLookup(),
    1000,  // timeout
    TimeUnit.MILLISECONDS,
    100    // capacity
);
```

### 4.2 Use Lookup Join (Table API)

```sql
-- SQL lookup join (automatically async)
SELECT o.*, d.description
FROM orders AS o
LEFT JOIN dimension_table FOR SYSTEM_TIME AS OF o.proctime AS d
ON o.product_id = d.id
```

---

## 5. References

[^1]: Apache Flink Documentation, "Async I/O", 2025.
[^2]: Apache Flink Documentation, "Lookup Joins", 2025.
[^3]: Netflix Tech Blog, "Asynchronous I/O for Stream Processing", 2019.
