# Flink Production Deployment Checklist

> **Stage**: Knowledge/07-best-practices | **Prerequisites**: [Anti-pattern Checklist](anti-pattern-checklist.md) | **Formalization Level**: L3
> **Translation Date**: 2026-04-21

## Abstract

This checklist provides a systematic verification process for deploying Flink jobs to production, ensuring stability, reliability, security, and performance.

---

## 1. Definitions

### Def-K-07-01 (Production Deployment Checklist)

A **production deployment checklist** is a set of verification steps ensuring Flink jobs meet requirements before production deployment.

---

## 2. Checklist Categories

### 2.1 Configuration Checks

#### Checkpoint Configuration

- [ ] Checkpoint interval: 10s - 10min (typical: 1min)
- [ ] Checkpoint timeout: > interval + network latency
- [ ] Exactly-once semantics enabled (if required)
- [ ] Incremental checkpointing enabled for large state
- [ ] Unaligned checkpoints considered for backpressure scenarios
- [ ] Externalized checkpoint cleanup: RETAIN_ON_CANCELLATION or DELETE_ON_CANCELLATION

#### Watermark Configuration

- [ ] Watermark strategy defined (event time processing)
- [ ] Max out-of-orderness configured based on source characteristics
- [ ] Idle source timeout configured for multi-source jobs
- [ ] Allowed lateness configured for windowed operations

#### Resource Configuration

- [ ] Parallelism matches source partition count (Kafka: 1:1)
- [ ] Task slots per TM: 1-4 (avoid oversubscription)
- [ ] JVM heap size: at least 2GB per slot
- [ ] Managed memory fraction: 0.4 for RocksDB, 0.1 for memory state

### 2.2 Monitoring Checks

#### Basic Monitoring

- [ ] JobManager and TaskManager metrics exposed (Prometheus)
- [ ] Lag metrics for all sources (records behind latest offset)
- [ ] Backpressure monitoring enabled
- [ ] Checkpoint failure alerts configured
- [ ] Restart strategy configured (fixed-delay or exponential-backoff)

#### Log Checks

- [ ] Structured logging (JSON format)
- [ ] Log level: INFO for production, DEBUG for troubleshooting only
- [ ] Log retention policy configured
- [ ] Sensitive data masked in logs

### 2.3 Security Review

#### Authentication & Authorization

- [ ] Kerberos / OAuth enabled for cluster access
- [ ] RBAC configured for Kubernetes deployment
- [ ] Service accounts with least privilege

#### Data Security

- [ ] TLS enabled for network communication
- [ ] Encryption at rest for state backends (if applicable)
- [ ] PII data handling complies with regulations (GDPR, CCPA)

#### Audit Logging

- [ ] Job submission audit trail
- [ ] Configuration change tracking
- [ ] Access logs for state queries

### 2.4 Performance Validation

#### Load Testing

- [ ] Baseline throughput measured
- [ ] Peak load test: 2x expected traffic
- [ ] Recovery test: kill TM, verify automatic restart
- [ ] Backpressure behavior observed and acceptable

---

## 3. Deployment Flow

```mermaid
graph LR
    Dev[Development] --> Review[Code Review]
    Review --> Staging[Staging Deploy]
    Staging --> Check[Checklist Verification]
    Check --> LoadTest[Load Testing]
    LoadTest --> Prod[Production Deploy]
    Prod --> Monitor[Monitoring]
    
    style Check fill:#fff3e0
    style Prod fill:#e8f5e9
```

---

## 4. References

[^1]: Apache Flink Documentation, "Production Readiness", 2025.
[^2]: Apache Flink Documentation, "Configuration", 2025.
[^3]: Apache Flink Documentation, "Monitoring and Metrics", 2025.
