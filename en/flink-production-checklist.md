# Flink Production Deployment Checklist

> **Stage**: Knowledge/07-best-practices | **Prerequisites**: [Anti-patterns](anti-pattern-checklist.md) | **Formalization Level**: L3
> **Translation Date**: 2026-04-21

## Abstract

Systematic checklist for deploying Flink jobs to production with stability, reliability, security, and performance guarantees.

---

## 1. Configuration Checklist

### Checkpoint

| Item | Recommendation | Criticality |
|------|---------------|-------------|
| Interval | 1-10 minutes | High |
| Timeout | > interval | High |
| Mode | EXACTLY_ONCE for correctness | High |
| Unaligned | Enable if backpressure > 30s | Medium |

### Watermark

| Item | Recommendation | Criticality |
|------|---------------|-------------|
| Strategy | BoundedOutOfOrderness | High |
| Max delay | 2x observed max delay | High |
| Idleness | Enable for multi-source | Medium |

### Resources

| Item | Recommendation | Criticality |
|------|---------------|-------------|
| Parallelism | Match Kafka partitions | High |
| Heap/Managed memory | 40%/40% split | High |
| Network memory | min 64MB per slot | Medium |

---

## 2. Monitoring Checklist

- [ ] JobManager/TaskManager JVM metrics
- [ ] Checkpoint duration and failures
- [ ] Backpressure ratio per operator
- [ ] Watermark lag per source
- [ ] Records in/out per second
- [ ] State size growth rate

---

## 3. Security Checklist

- [ ] Kerberos authentication enabled
- [ ] TLS for network communication
- [ ] RBAC for Flink Web UI
- [ ] Audit logging enabled
- [ ] Sensitive data encryption at rest

---

## 4. Performance Validation

- [ ] Throughput meets SLA
- [ ] P99 latency < 100ms (or requirement)
- [ ] No backpressure under peak load
- [ ] Recovery time < 2 minutes

---

## 5. References
