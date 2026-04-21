# Business Pattern: FinTech Real-Time Risk Control

> **Stage**: Knowledge | **Prerequisites**: [CEP Pattern](../pattern-cep-complex-event.md) | **Formal Level**: L4-L5
>
> **Domain**: FinTech | **Complexity**: ★★★★★ | **Latency**: < 100ms | **Accuracy**: False Positive < 5%, False Negative < 0.1%
>
> Real-time fraud detection, credit risk assessment, and anti-money laundering using CEP + Flink.

---

## 1. Problem Context

**Core Challenges**:

| Dimension | Problem | Impact | Requirement |
|-----------|---------|--------|-------------|
| Latency | Transactions must complete risk assessment in milliseconds | User churn or failure | P99 < 100ms |
| Accuracy | False positives hurt UX, false negatives cause losses | Financial + reputational | FP < 5%, FN < 0.1% |
| Temporal Complexity | Fraud exhibits complex temporal patterns | Simple rules insufficient | CEP engine |
| Consistency | No transaction loss or duplication | Regulatory + financial | Exactly-Once |
| Compliance | Complete audit trail required | Regulatory penalty | Immutable logs |

---

## 2. Solution Architecture

**CEP + Flink Pipeline**:

```
Kafka (transaction events)
  → KeyBy(account_id)
  → CEP Pattern Matching (fraud patterns)
  → Feature Enrichment (user profile, device)
  → ML Model Scoring
  → Rule Engine (policy overlay)
  → Decision Sink (approve/block/review)
```

---

## 3. Implementation

**Key Performance Metrics**:

- Throughput: 500K+ TPS
- P99 latency: < 80ms
- Checkpoint interval: 30s
- State size: 2TB (RocksDB)

**Flink Code Example**:

```java
// Fraud pattern: 3+ failed logins followed by large transfer
Pattern<LoginEvent, ?> fraudPattern = Pattern
    .<LoginEvent>begin("failed_logins")
    .where(evt -> evt.getStatus().equals("FAILED"))
    .timesOrMore(3)
    .within(Time.minutes(10))
    .next("large_transfer")
    .where(evt -> evt.getAmount() > 10000);
```

---

## 4. When to Use

**Recommended**:

- Real-time payment fraud detection
- Credit card transaction scoring
- Anti-money laundering monitoring

**Not Recommended**:

- Offline batch risk modeling
- Non-time-sensitive compliance reporting

---

## 5. Related Patterns

- [CEP Pattern](../pattern-cep-complex-event.md)
- [Stateful Computation](../pattern-stateful-computation.md)
- [Exactly-Once](../flink-exactly-once-end-to-end.md)

---

## 6. References
