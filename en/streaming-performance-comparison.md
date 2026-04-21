# Streaming Engine Performance Comparison

> **Language**: English | **Source**: [Knowledge/04-technology-selection/streaming-performance-comparison-xchart.md](../Knowledge/04-technology-selection/streaming-performance-comparison-xchart.md) | **Last Updated**: 2026-04-21

---

## 1. Definitions

### Def-K-04-EN-20: Throughput

Throughput $\mathcal{T}$ is the number of events successfully processed per unit time:

$$
\mathcal{T} = \frac{|E_{processed}|}{\Delta t} \quad [events/sec]
$$

### Def-K-04-EN-21: Latency

End-to-end latency $\mathcal{L}$ is the time interval from event entry to output:

$$
\mathcal{L}(e) = t_{output}(e) - t_{input}(e) \quad [ms]
$$

### Def-K-04-EN-22: State Size Efficiency

State size efficiency $\eta_{state}$ is the state storage required per million events:

$$
\eta_{state} = \frac{|State|}{|E_{processed}| / 10^6} \quad [MB/M\ events]
$$

## 2. Properties

### Prop-K-04-EN-15: Throughput-Latency Tradeoff

Under resource constraints, throughput and latency trade off:

$$
\mathcal{T} \cdot \mathcal{L} \leq C_{resource}
$$

where $C_{resource}$ is the system resource capacity constant.

### Prop-K-04-EN-16: State Backend Impact

State backend selection affects efficiency as:

$$
\eta_{state}^{RocksDB} < \eta_{state}^{HashMap} < \eta_{state}^{Remote}
$$

RocksDB on-disk storage is most efficient; remote storage is least.

## 3. Engine Comparison

| Engine | Peak Throughput (K eps) | Median Latency (ms) | State Efficiency (MB/M) | Checkpoint Overhead |
|--------|------------------------|---------------------|------------------------|---------------------|
| Flink | 5,000+ | 10-100 | 50 (RocksDB) | < 5% |
| Spark Streaming | 2,000+ | 100-1000 | 200 (in-memory) | < 10% |
| Kafka Streams | 1,000+ | 10-50 | 100 (RocksDB) | < 3% |
| RisingWave | 3,000+ | 1-10 | 30 (columnar) | Incremental |
| Materialize | 500+ | 1-10 | 40 (differential) | Incremental |

## 4. Workload-to-Engine Mapping

| Workload Characteristic | Recommended Engine | Rationale |
|------------------------|-------------------|-----------|
| High throughput + tolerable second-level latency | Spark Streaming | Batch processing optimized |
| Low latency + moderate throughput | Kafka Streams | Lightweight, embedded |
| Complex stateful + exactly-once | Flink | Mature checkpointing, rich API |
| SQL-first + materialized views | RisingWave | PostgreSQL protocol, auto-scaling |
| Strong consistency + differential updates | Materialize | Differential dataflow, correctness |

## References
