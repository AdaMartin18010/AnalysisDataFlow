# Business Pattern: FinTech Real-time Risk Control

> **Stage**: Knowledge/03-business-patterns | **Prerequisites**: [CEP Pattern](pattern-complex-event-processing.md) | **Complexity**: ★★★★★ | **Latency**: < 100ms
> **Translation Date**: 2026-04-21

## Abstract

Real-time fraud detection, credit risk assessment, and AML using CEP + Flink with sub-100ms latency.

---

## 1. Problem Context

| Dimension | Challenge | Requirement |
|-----------|-----------|-------------|
| Latency | Transaction must complete risk check in milliseconds | P99 < 100ms |
| Accuracy | False positives < 5%, false negatives < 0.1% | Complex feature engineering + ML |
| Temporal | Fraud exhibits complex temporal patterns | CEP pattern matching |
| Consistency | Transactions must not be lost or duplicated | Exactly-Once semantics |
| Compliance | Full audit trail required | Immutable log + reproducible computation |

---

## 2. Solution Architecture

### 2.1 CEP + Flink Pipeline

```
Event Source → Enrichment → CEP Pattern Match → Risk Scoring → Decision → Action
                ↓                ↓                    ↓
          Feature Store    Rule Engine          ML Model
```

### 2.2 Risk Score Formula

$$\text{RiskScore}(t) = \sum_{i} w_i \cdot f_i(t) + \text{Model}(t)$$

---

## 3. Flink Implementation

```java
Pattern<Transaction, ?> fraudPattern = Pattern
    .<Transaction>begin("small")
    .where(t -> t.amount < 100)
    .next("large")
    .where(t -> t.amount > 10000)
    .within(Time.seconds(60));

CEP.pattern(stream, fraudPattern)
    .process(new FraudAlertHandler());
```

---

## 4. References
