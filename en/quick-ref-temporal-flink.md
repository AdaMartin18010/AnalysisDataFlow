# Temporal + Flink Layered Architecture Quick Reference

> **Language**: English | **Source**: [Knowledge/98-exercises/quick-ref-temporal-flink.md](../Knowledge/98-exercises/quick-ref-temporal-flink.md) | **Last Updated**: 2026-04-21

---

## Four-Layer Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 4: Business Orchestration (Temporal)   ← Quasi-Decidable │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ Saga Pattern│  │ Human Task  │  │ Cross-Service Tx Coord  │  │
│  │ Compensation│  │ External Sig│  │ Long-Running Process    │  │
│  └──────┬──────┘  └──────┬──────┘  └────────────┬────────────┘  │
│         └─────────────────┼──────────────────────┘               │
│                           │ Trigger Events                       │
│  Decidability: Quasi-Decidable                                   │
│  Latency: Seconds / Minutes / Days                               │
├───────────────────────────┼──────────────────────────────────────┤
│  Layer 3: Stream Processing (Flink)        ← Semi-Decidable     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ Window Agg  │  │ CEP Detect  │  │ Real-time Features      │  │
│  │ Time Windows│  │ Patterns    │  │ Metrics                 │  │
│  └──────┬──────┘  └──────┬──────┘  └────────────┬────────────┘  │
│  Decidability: Semi-Decidable                                    │
│  Latency: Milliseconds (event-level)                             │
├───────────────────────────┼──────────────────────────────────────┤
│  Layer 2: Message Queue (Kafka/Pulsar)                           │
│  Role: Event storage, ordering guarantee, stream multiplexing    │
├───────────────────────────┼──────────────────────────────────────┤
│  Layer 1: Data Sources                                           │
│  IoT Sensors │ Trading Systems │ User Logs │ External APIs       │
└─────────────────────────────────────────────────────────────────┘
```

## Decidability Spectrum

```
Decidability Strength ↑
           │
Decidable │  Batch Processing (Flink Bounded Stream)
           │  Sequential Computation
           │
Quasi-Dec  │  ●──────────────────────────────────────●
           │  │ Temporal Workflow (Deterministic SM)  │
           │  │  • Event history replay               │
           │  │  • Saga compensation sequences        │
           │  │  • Human approval / external waits    │
           │  ●──────────────────────────────────────●
           │
Semi-Dec   │  ●──────────────────────────────────────●
           │  │ Flink Stream Processing               │
           │  │  • CEP pattern detection (unbounded)  │
           │  │  • Window aggregation (watermark)     │
           │  │  • High-throughput real-time compute  │
           │  ●──────────────────────────────────────●
           │
Undecidable│  General distributed consensus (FLP)
           │  LLM Agent emergent behavior
           └──────────────────────────────────────────────→ Complexity
```

## Scenario Matching

| Scenario | Flink Role | Temporal Role | Integration |
|----------|------------|---------------|-------------|
| **IoT Maintenance** | Anomaly detection (window agg) | Create ticket → Engineer confirm → Complete | One-way trigger |
| **Financial Risk** | Suspicious pattern detection (CEP) | Investigation → Manual review → Risk rating | One-way trigger |
| **E-commerce Order** | Real-time inventory check | Order fulfillment → Payment → Ship → Deliver | Bi-directional |
| **Device Alert** | Multi-sensor aggregation | Tiered response (CRITICAL/WARNING) | One-way trigger |
| **Real-time Recommend** | User behavior features | A/B test orchestration | Bi-directional |

## Configuration Quick Reference

| Scenario | Flink Config | Temporal Config | E2E Latency |
|----------|-------------|-----------------|-------------|
| **IoT Maintenance** | 5-min window + 60s checkpoint | 24h human confirmation timeout | < 6 min |
| **Real-time Risk** | 1-min window + 30s checkpoint | 1h investigation timeout | < 2 min |
| **Order Processing** | Direct trigger (no window) | 7-day fulfillment timeout | < 1 sec |

## Key Integration Pattern

```java
// Flink Temporal Sink - Idempotent workflow trigger
public class TemporalWorkflowSink
    extends TwoPhaseCommitSinkFunction<AlertEvent, TemporalTransaction, Void> {

    private transient TemporalClient temporalClient;

    @Override
    protected void commit(TemporalTransaction transaction) {
        for (AlertEvent alert : transaction.getPendingWorkflows()) {
            String workflowId = generateWorkflowId(alert);
            try {
                temporalClient.startWorkflow(
                    "DeviceMaintenanceWorkflow", workflowId, alert);
            } catch (WorkflowExecutionAlreadyStarted e) {
                log.info("Workflow {} already exists, skipping", workflowId);
            }
        }
    }

    private String generateWorkflowId(AlertEvent alert) {
        // Idempotency: same device + time window → same ID
        return String.format("maintenance-%s-%d",
            alert.getDeviceId(),
            alert.getWindowStart() / 3600000);
    }
}
```

## References
