---
title: "Temporal + Flink Layered Architecture Quick Reference Card"
translation_status: ai_translated_reviewed
source_version: v4.1
last_sync: "2026-04-15"
---

# Temporal + Flink Layered Architecture Quick Reference Card

> **Quick Reference**: Layered architecture, typical scenarios, and code templates for Temporal and Flink integration
>
> **Full Document**: [temporal-flink-layered-architecture.md](../06-frontier/temporal-flink-layered-architecture.md)

---

## 🏗️ Layered Architecture Quick-Reference Diagram

### Four-Layer Architecture Model

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 4: Business Orchestration (Temporal)    ← Quasi-Decidable│
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ Saga Pattern│  │ Manual      │  │ Cross-Service           │  │
│  │ Compensation│  │ Approval    │  │ Transaction Coordination│  │
│  │ Transaction │  │ External    │  │ Long-Running Process    │  │
│  └──────┬──────┘  └──────┬──────┘  └────────────┬────────────┘  │
│         │                │                      │               │
│         └────────────────┼──────────────────────┘               │
│                          │ Trigger Events                       │
│  Decidability: Quasi-Decidable (Quasi-Decidable)                │
│  Latency: Seconds / Minutes / Days                              │
├──────────────────────────┼──────────────────────────────────────┤
│  Layer 3: Stream Processing (Flink)         ← Semi-Decidable    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ Window      │  │ CEP         │  │ Real-Time Feature       │  │
│  │ Aggregation │  │ Detection   │  │ Computation             │  │
│  │ Time Windows│  │ Complex     │  │ Metric Statistics       │  │
│  └──────┬──────┘  └──────┬──────┘  └────────────┬────────────┘  │
│         │                │                      │               │
│  Decidability: Semi-Decidable (Semi-Decidable)                  │
│  Latency: Milliseconds (event-level)                            │
├──────────────────────────┼──────────────────────────────────────┤
│  Layer 2: Message Queue (Kafka/Pulsar)                          │
│  Responsibilities: Event storage, ordering guarantee, stream    │
│  multiplexing                                                   │
├─────────────────────────────────────────────────────────────────┤
│  Layer 1: Data Source Layer                                     │
│  IoT Sensors │ Trading Systems │ User Behavior Logs │ External  │
│  API                                                            │
└─────────────────────────────────────────────────────────────────┘
```

### Decidability Spectrum Positioning

```
Decidability Strength ↑
           │
Decidable  │  Batch Processing (Flink Bounded Stream)
           │  Sequential Computation
           │
Quasi-     │  ●──────────────────────────────────────●
Decidable  │  │ Temporal Workflow (Deterministic    │
           │  │   State Machine)                     │
           │  │  • Event History Replay              │
           │  │  • Saga Compensation Sequence        │
           │  │  • Manual Approval / External Event  │
           │  │    Wait                              │
           │  ●──────────────────────────────────────●
           │
Semi-      │  ●──────────────────────────────────────●
Decidable  │  │ Flink Stream Processing              │
           │  │  • CEP Pattern Detection (Infinite   │
           │  │    Stream)                           │
           │  │  • Window Aggregation (Watermark     │
           │  │    Approximation)                    │
           │  │  • High-Throughput Real-Time         │
           │  │    Computation                       │
           │  ●──────────────────────────────────────●
           │
Undecidable│  General Distributed Consensus (FLP    │
           │  Impossibility)                        │
           │  LLM Agent Emergent Behavior           │
           │
           └──────────────────────────────────────────────→ Complexity
```

---

## 📊 Typical Scenario Matching Table

| Scenario | Flink Responsibility | Temporal Responsibility | Integration Mode |
|----------|----------------------|-------------------------|------------------|
| **IoT Device Maintenance** | Temperature anomaly detection (window aggregation) | Create ticket → Engineer confirmation → Complete maintenance | One-way Trigger |
| **Financial Risk Control** | Suspicious transaction pattern detection (CEP) | Investigation process → Manual review → Risk classification | One-way Trigger |
| **E-Commerce Order** | Real-time inventory check | Order fulfillment → Payment → Shipping → Delivery | Bidirectional Sync |
| **Device Alert** | Multi-sensor aggregation judgment | Tiered response (CRITICAL / WARNING) | One-way Trigger |
| **Real-Time Recommendation** | Real-time user behavior features | A/B test experiment orchestration | Bidirectional Sync |
| **Anomaly Detection** | Real-time ML model inference | Alert escalation → Expert intervention | One-way Trigger |

### Scenario Detailed Configuration Quick Reference

| Scenario | Flink Config | Temporal Config | End-to-End Latency |
|----------|--------------|-----------------|--------------------|
| **IoT Maintenance** | 5-min window + 60s Checkpoint | 24-hour manual confirmation timeout | < 6 minutes |
| **Real-Time Risk Control** | 1-min window + 30s Checkpoint | 1-hour investigation timeout | < 2 minutes |
| **Order Processing** | Direct trigger, no window | 7-day fulfillment timeout | < 1 second |

---

## 💻 Code Template Quick Reference

### Flink Temporal Sink (Java)

```java
/**
 * Flink Temporal Sink - Transactional Workflow Trigger
 */
public class TemporalWorkflowSink
    extends TwoPhaseCommitSinkFunction<AlertEvent,
                                       TemporalTransaction,
                                       Void> {

    private transient TemporalClient temporalClient;

    @Override
    protected void invoke(TemporalTransaction transaction,
                          AlertEvent value,
                          Context context) {
        transaction.addPendingWorkflow(value);
    }

    @Override
    protected void commit(TemporalTransaction transaction) {
        for (AlertEvent alert : transaction.getPendingWorkflows()) {
            String workflowId = generateWorkflowId(alert);
            try {
                temporalClient.startWorkflow(
                    "DeviceMaintenanceWorkflow",
                    workflowId,
                    alert
                );
            } catch (WorkflowExecutionAlreadyStarted e) {
                // Idempotent handling: ignore already-existing workflow
                log.info("Workflow {} already exists, skipping", workflowId);
            }
        }
    }

    private String generateWorkflowId(AlertEvent alert) {
        // Idempotency guarantee: same device + time window generates same ID
        return String.format("maintenance-%s-%d",
            alert.getDeviceId(),
            alert.getWindowStart() / 3600000); // hourly window
    }
}
```

### Temporal Workflow (Go)

```go
package maintenance

import (
    "time"
    "go.temporal.io/sdk/workflow"
)

// DeviceAlert represents a device alert event
type DeviceAlert struct {
    DeviceID    string
    SensorType  string
    AlertLevel  string // WARNING, CRITICAL
    Temperature float64
    Timestamp   time.Time
}

// DeviceMaintenanceWorkflow is the device maintenance workflow
func DeviceMaintenanceWorkflow(
    ctx workflow.Context,
    alert DeviceAlert
) (*MaintenanceResult, error) {
    logger := workflow.GetLogger(ctx)

    // Define activity options
    ao := workflow.ActivityOptions{
        StartToCloseTimeout: 10 * time.Minute,
        RetryPolicy: &temporal.RetryPolicy{
            InitialInterval:    time.Second,
            BackoffCoefficient: 2.0,
            MaximumInterval:    time.Minute,
            MaximumAttempts:    3,
        },
    }
    ctx = workflow.WithActivityOptions(ctx, ao)

    // Step 1: Create maintenance ticket (idempotent operation)
    var ticketID string
    err := workflow.ExecuteActivity(
        ctx, CreateMaintenanceTicket, alert
    ).Get(ctx, &ticketID)
    if err != nil {
        return nil, err
    }

    // Step 2: Branch processing based on alert level
    if alert.AlertLevel == "CRITICAL" {
        // CRITICAL: immediate notification, wait 1 hour for acknowledgment
        err = workflow.ExecuteActivity(
            ctx, SendUrgentNotification, alert, ticketID
        ).Get(ctx, nil)

        selector := workflow.NewSelector(ctx)
        var ack EngineerAcknowledgment

        selector.AddReceive(
            workflow.GetSignalChannel(ctx, "EngineerAcknowledged"),
            func(c workflow.ReceiveChannel, more bool) {
                c.Receive(ctx, &ack)
            },
        )

        // Set timeout
        timer := workflow.NewTimer(ctx, time.Hour)
        selector.AddFuture(timer, func(f workflow.Future) {
            _ = workflow.ExecuteActivity(
                ctx, EscalateToManager, ticketID
            ).Get(ctx, nil)
        })

        selector.Select(ctx)
    } else {
        // WARNING: normal process, wait 24 hours
        // ...
    }

    return result, nil
}
```

### IoT Temperature Monitor Flink Job

```java
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.CheckpointingMode;
import org.apache.flink.streaming.api.windowing.time.Time;


public class TemperatureMonitorJob {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        // Configure Checkpoint
        env.enableCheckpointing(60000); // 60 seconds
        env.getCheckpointConfig().setCheckpointingMode(
            CheckpointingMode.EXACTLY_ONCE);

        // Data source: MQTT/Kafka
        DataStream<SensorReading> readings = env
            .addSource(new FlinkKafkaConsumer<>(
                "sensor-readings",
                new SensorReadingDeserializationSchema(),
                kafkaProps))
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<SensorReading>forBoundedOutOfOrderness(
                    Duration.ofSeconds(30))
                .withTimestampAssigner((event, ts) -> event.getTimestamp())
            );

        // Window aggregation: group by device ID, 1-hour tumbling window
        DataStream<DeviceAlert> alerts = readings
            .keyBy(SensorReading::getDeviceId)
            .window(TumblingEventTimeWindows.of(Time.hours(1)))
            .aggregate(new AverageTemperatureAggregate())
            .filter(avg -> avg.getAverageTemp() > 80.0)
            .map(avg -> new DeviceAlert(
                avg.getDeviceId(),
                "TEMPERATURE",
                avg.getAverageTemp() > 90.0 ? "CRITICAL" : "WARNING",
                avg.getAverageTemp(),
                avg.getWindowStart()
            ));

        // Write to Temporal to trigger workflow
        alerts.addSink(new TemporalWorkflowSink(
            "temporal:7233",
            "iot-maintenance"
        ));

        env.execute("IoT Temperature Monitor");
    }
}
```

### Saga Pattern Implementation

```go
// MaintenanceSaga manages the maintenance saga
type MaintenanceSaga struct {
    compensations []func() error
}

func (s *MaintenanceSaga) addCompensation(fn func() error) {
    s.compensations = append(s.compensations, fn)
}

func (s *MaintenanceSaga) compensate(ctx workflow.Context) error {
    // Execute compensations in reverse order
    for i := len(s.compensations) - 1; i >= 0; i-- {
        if err := s.compensations[i](); err != nil {
            workflow.GetLogger(ctx).Error(
                "Compensation failed",
                "Index", i,
                "Error", err,
            )
        }
    }
    return nil
}

func DeviceMaintenanceWorkflowWithSaga(
    ctx workflow.Context,
    alert DeviceAlert
) error {
    saga := &MaintenanceSaga{}

    // Step 1: Reserve spare part
    var reservationID string
    err := workflow.ExecuteActivity(
        ctx, ReserveSparePart, alert.DeviceID
    ).Get(ctx, &reservationID)
    if err != nil {
        return err
    }
    saga.addCompensation(func() error {
        return workflow.ExecuteActivity(
            ctx, ReleaseSparePart, reservationID
        ).Get(ctx, nil)
    })

    // Step 2: Disable device
    err = workflow.ExecuteActivity(
        ctx, DisableDevice, alert.DeviceID
    ).Get(ctx, nil)
    if err != nil {
        saga.compensate(ctx)
        return err
    }
    saga.addCompensation(func() error {
        return workflow.ExecuteActivity(
            ctx, EnableDevice, alert.DeviceID
        ).Get(ctx, nil)
    })

    // Step 3: Perform maintenance
    // ...

    return nil
}
```

---

## 🔄 State Synchronization Strategies

### Mode 1: Unidirectional Flow (Flink → Temporal)

```
Flink                    Kafka                    Temporal
  │                       │                         │
  │── Detect Anomaly ────►│                         │
  │                       │─── Trigger Workflow ───►│
  │                       │                         │── Start Workflow
  │                       │                         │── Process
  │                       │◄── Status Update ───────┤
  │◄── Update State ──────│                         │
```

**Applicable Scenarios**: Flink detects anomalies, Temporal handles subsequent processes

### Mode 2: Bidirectional Sync (Flink ↔ Temporal)

```java
// Temporal Query Handler
@QueryMethod
public WorkflowState getWorkflowState() {
    return new WorkflowState(
        this.currentStatus,
        this.processedEvents.size(),
        this.pendingActivities
    );
}

// Flink AsyncFunction
public class TemporalStateLookup extends AsyncFunction<AlertEvent, EnrichedAlert> {
    @Override
    public void asyncInvoke(AlertEvent event, ResultFuture<EnrichedAlert> resultFuture) {
        CompletableFuture<WorkflowState> stateFuture = client.queryWorkflow(
            event.getDeviceId(),
            "getWorkflowState",
            WorkflowState.class
        );

        stateFuture.thenAccept(state -> {
            resultFuture.complete(Collections.singletonList(
                new EnrichedAlert(event, state)
            ));
        });
    }
}
```

**Applicable Scenarios**: Complex scenarios requiring state feedback

---

## ⚖️ Error Handling Comparison

| Error Type | Flink Handling | Temporal Handling |
|------------|----------------|-------------------|
| **Transient Fault** | Auto-retry (Task restart) | Activity auto-retry (exponential backoff) |
| **State Loss** | Recover from Checkpoint | Replay from Event History |
| **External API Failure** | Requires Sink-side handling | Saga compensation transaction |
| **Logic Error** | Code fix and restart required | Workflow version upgrade + patch |
| **Timeout** | Window timeout trigger | Workflow / Activity timeout config |

---

## 📚 Further Reading

| Document | Content |
|----------|---------|
| [temporal-flink-layered-architecture.md](../06-frontier/temporal-flink-layered-architecture.md) | Complete architecture guide |
| [streaming-slo-definition.md](../06-frontier/streaming-slo-definition.md) | Streaming SLO definitions |
| [realtime-data-mesh-practice.md](../06-frontier/realtime-data-mesh-practice.md) | Real-time data mesh practice |

---

*Quick Reference Card v1.0 | Last Updated: 2026-04-03*
