# Flink Delta Join: Large-State Stream Join Optimization

> **Language**: English | **Source**: [Flink/02-core/delta-join.md](../Flink/02-core/delta-join.md) | **Last Updated**: 2026-04-21

---

## 1. Definitions

### Def-F-02-EN-20: Delta Join Operator

An execution operator optimized for large-state stream joins, using **incremental lookup** instead of **materialized intermediate results**.

Given streams $S_1$ and $S_2$ associated with external stores $T_1$ and $T_2$, Delta Join operator $\mathcal{D}$ is defined as:

$$
\mathcal{D}(s_1, T_2, T_1) : S_1 \times \mathcal{P}(T_2) \times \mathcal{P}(T_1) \rightarrow \{(r_1, r_2) \mid r_1 \in s_1 \land r_2 \in T_2 \land \theta(r_1, r_2)\}
$$

where $s_1 \subseteq S_1$ is the input delta, $\theta$ is the join condition. **Key constraint**: $\mathcal{D}$ does not maintain materialized join intermediate state.

**Insight**: Traditional Stream Join maintains buffered state for both inputs (Hash Table or RocksDB), growing with data. Delta Join caches only one side (usually the smaller/dimension table), and performs point lookups when the other stream arrives, reducing join state from $O(|S_1| + |S_2|)$ to $O(|T|)$.

### Def-F-02-EN-21: Bi-Directional Lookup Join

An extension of Delta Join allowing both streams to join via external lookup without any intermediate state materialization:

$$
\text{BiLookup}(s_1, s_2, T) = \{(r_1, r_2) \mid (r_1 \in s_1 \land \text{lookup}_T(r_1) = r_2) \lor (r_2 \in s_2 \land \text{lookup}_T(r_2) = r_1)\}
$$

Requires external store $T$ to support efficient point lookup:

- JDBC dimension tables (MySQL, PostgreSQL)
- KV stores (HBase, Redis)
- Lakehouse tables (Iceberg, Paimon)

### Def-F-02-EN-22: Zero Intermediate State Policy

Core execution principle of Delta Join:

$$
\forall t \in \text{ExecutionTime}, \nexists M_t : M_t = \{(r_i, r_j) \mid r_i \in S_1 \land r_j \in S_2 \land \theta(r_i, r_j)\}
$$

Trade-offs and optimizations:

- **Local cache**: LRU cache for hot join keys
- **Batch lookup**: Coalesce multiple point lookups
- **Async I/O**: Non-blocking stream processing

## 2. Properties

### Prop-F-02-EN-15: State Complexity Upper Bound

Delta Join state complexity is $O(|T|_{cache} + |W|)$, where $|T|_{cache}$ is external store cache size and $|W|$ is async I/O wait queue length.

### Prop-F-02-EN-16: Lookup Amortization

With batch size $b$, amortized lookup cost per record:

$$
C_{avg} = \frac{C_{batch}}{b} + C_{cache\_hit} \cdot p_{hit}
$$

## 3. When to Use Delta Join

| Scenario | Traditional Join | Delta Join |
|----------|-----------------|------------|
| Both streams large | Required | Not suitable |
| One stream + one dimension table | Works | **Optimal** |
| State size > TM memory | RocksDB spill | **External lookup** |
| Join key highly skewed | Hot key OOM | **Cache + batch** |
| Low-latency requirement | State access latency | **Async I/O** |

## 4. Configuration

```sql
-- Flink SQL Delta Join hint
SELECT /*+ LOOKUP('table'='customers', 'retry'='fixed-delay') */ *
FROM orders o
LEFT JOIN customers FOR SYSTEM_TIME AS OF o.proc_time c
ON o.customer_id = c.id;
```

```java
// Async I/O for Delta Join
AsyncDataStream.unorderedWait(
    inputStream,
    new AsyncCustomerLookup(),
    1000,  // timeout ms
    TimeUnit.MILLISECONDS,
    100    // capacity
);
```

## References
