# Streaming Processing Best Practices

> **Language**: English | **Source**: [Knowledge/07-best-practices/](../Knowledge/07-best-practices/) | **Last Updated**: 2026-04-21

---

## 1. Production Checklist

### Pre-Launch Verification

| Category | Item | Priority | Verification Method |
|----------|------|----------|---------------------|
| **State Management** | State backend selection aligned with access pattern | P0 | Review state backend comparison matrix |
| **Checkpointing** | Checkpoint interval < maximum tolerable replay | P0 | Validate against business SLA |
| **Watermark** | Watermark strategy matches data arrival pattern | P0 | Test with production data sample |
| **Parallelism** | Key distribution analyzed for skew | P0 | Run representative workload |
| **Monitoring** | Latency/throughput/backpressure metrics configured | P0 | Dashboard verification |
| **Failure Recovery** | Savepoint taken before deployment | P0 | Manual savepoint + restore test |

### Post-Launch Monitoring

| Metric | Warning Threshold | Critical Threshold | Action |
|--------|-------------------|-------------------|--------|
| Checkpoint Duration | > 50% of interval | > 80% of interval | Tune state backend or increase interval |
| Backpressure Ratio | > 20% | > 50% | Scale out or optimize operator |
| Watermark Lag | > 5 minutes | > 15 minutes | Investigate source delay |
| JVM Heap Usage | > 70% | > 85% | Tune GC or increase memory |
| Record Latency (p99) | > 2× SLA | > 5× SLA | Optimize or scale |

## 2. Performance Tuning Patterns

### Def-K-07-EN-01: Backpressure Mitigation Pattern

A backpressure mitigation strategy is a tuple $(D, B, S)$ where:

- $D$: Detection mechanism (task backpressure ratio > threshold)
- $B$: Buffer strategy (increase network buffer, enable buffer debloating)
- $S$: Scale action (auto-scaling trigger or manual parallelism adjustment)

**Theorem**: If backpressure ratio $r > \theta_{critical}$ and scaling factor $\lambda > \frac{r}{\theta_{target}}$, then backpressure resolves within $O(\log_{\lambda} \frac{r}{\theta_{target}})$ scaling iterations.

### Def-K-07-EN-02: Serialization Optimization

Serialization overhead reduction follows the hierarchy:

$$
\text{TypeInformation} \succ \text{Avro} \succ \text{Kryo} \succ \text{Java Serialization}
$$

**Recommendation**: Register custom types with TypeInformation; avoid Java Serialization in hot paths.

## 3. Cost Optimization

| Dimension | Low-Cost Strategy | Trade-off |
|-----------|-------------------|-----------|
| Compute | Spot instances for non-critical pipelines | Possible interruption |
| Storage | Incremental checkpoints + local recovery | Longer recovery on failover |
| Network | Co-location of source and processing | Reduced flexibility |
| State | RocksDB with SSD tiering | Higher latency vs heap state |

## 4. Security Hardening

- **Authentication**: Enable Kerberos or mTLS for inter-task communication
- **Authorization**: Use ACLs on state backends and checkpoint storage
- **Encryption**: Enable TLS for data in transit; encrypt checkpoints at rest
- **Audit**: Log all configuration changes and manual savepoint operations

## 5. References
