# Flink Exactly-Once Semantics Deep Dive

> **Stage**: Flink/02-core | **Prerequisites**: [Checkpoint Mechanism](flink-checkpoint-mechanism.md) | **Formalization Level**: L5
> **Translation Date**: 2026-04-21

## Abstract

Exactly-Once processing semantics guarantee each input event produces exactly one persistent output, even across failures.

---

## 1. Definitions

### Def-F-02-91 (Exactly-Once Semantics)

For system $S = (I, O, T, \Sigma)$:

$$\forall e \in I: \quad |\{ o \in O \mid o = T(e) \land \text{committed}(o) \}| = 1$$

### Def-F-02-92 (End-to-End Exactly-Once)

Requires three components:

1. **Replayable Source**: $\exists \text{replay}: \text{Offset} \times \text{Timestamp} \rightarrow I_{\geq \text{offset}}$
2. **Engine Exactly-Once**: As defined in Def-F-02-91
3. **Transactional Sink**: $\forall B: \text{commit}(B) \iff \text{checkpoint}(C_k) \land B \in C_k$

---

## 2. Consistency Levels

| Semantics | Guarantee | Formalization |
|-----------|-----------|---------------|
| At-Most-Once | May lose, never duplicate | $\forall e: |O_e| \leq 1$ |
| At-Least-Once | Never lose, may duplicate | $\forall e: |O_e| \geq 1$ |
| Exactly-Once | Neither lose nor duplicate | $\forall e: |O_e| = 1$ |

---

## 3. Two-Phase Commit

```java
// TwoPhaseCommitSinkFunction for end-to-end exactly-once
public class KafkaTransactionalSink
    extends TwoPhaseCommitSinkFunction<Event, KafkaTransactionState, KafkaTransactionContext> {

    @Override
    protected void beginTransaction() { /* start Kafka transaction */ }

    @Override
    protected void preCommit(KafkaTransactionState transaction) { /* flush */ }

    @Override
    protected void commit(KafkaTransactionState transaction) { /* commit Kafka tx */ }

    @Override
    protected void abort(KafkaTransactionState transaction) { /* rollback */ }
}
```

---

## 4. References
