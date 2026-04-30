# Operators and Real-time Port Logistics

> **Stage**: Knowledge/10-case-studies | **Prerequisites**: [01.07-two-input-operators.md](01.07-two-input-operators.md), [realtime-supply-chain-tracking-case-study.md](realtime-supply-chain-tracking-case-study.md) | **Formalization Level**: L3
> **Document Positioning**: Operator fingerprint and Pipeline design for stream-processing operators in real-time port container dispatching, AGV path optimization, and vessel arrival prediction
> **Version**: 2026.04

---

## Table of Contents

- [1. Definitions](#1-definitions)
- [2. Properties](#2-properties)
- [3. Relations](#3-relations)
- [4. Argumentation](#4-argumentation)
- [5. Proof / Engineering Argument](#5-proof--engineering-argument)
- [6. Examples](#6-examples)
- [7. Visualizations](#7-visualizations)
- [8. References](#8-references)

---

## 1. Definitions

### Def-PRT-01-01: Port Logistics Digital Twin (港口物流数字孪生)

Port Logistics Digital Twin is a real-time virtual mapping of physical port operations:

$$\text{PortTwin}(t) = (\text{Vessels}_t, \text{Containers}_t, \text{AGVs}_t, \text{Cranes}_t, \text{Yard}_t)$$

### Def-PRT-01-02: ETA — Estimated Time of Arrival (船舶到港时间)

ETA is the predicted arrival time based on vessel speed, route, and weather conditions:

$$\text{ETA} = t_{current} + \frac{D_{remaining}}{v_{avg}} + \sum_{i} \Delta t_{delay,i}$$

where $D_{remaining}$ is the remaining voyage distance, $v_{avg}$ is the average vessel speed, and $\Delta t_{delay,i}$ is the $i$-th delay factor (e.g., port congestion, weather).

### Def-PRT-01-03: Yard Optimization (集装箱堆场优化)

Yard Optimization is the decision problem of maximizing space utilization while minimizing container relocation (restow) operations:

$$\min \sum_{c} \text{Relocations}(c) \quad \text{s.t.} \quad \text{SpaceUtilization} < 0.85$$

### Def-PRT-01-04: AGV Scheduling (AGV调度)

AGV Scheduling is the optimization problem of assigning tasks and routes to Automated Guided Vehicles (AGVs, 自动导引车):

$$\min \sum_{v} \left(\alpha \cdot T_{travel,v} + \beta \cdot T_{wait,v} + \gamma \cdot T_{charging,v}\right)$$

### Def-PRT-01-05: Customs Risk Score (海关风险评分)

Customs Risk Score evaluates the inspection probability based on cargo characteristics:

$$\text{Risk} = w_1 \cdot f_{origin} + w_2 \cdot f_{commodity} + w_3 \cdot f_{shipper} + w_4 \cdot f_{history}$$

---

## 2. Properties

### Lemma-PRT-01-01: Port Throughput Queuing Model (港口吞吐的排队论模型)

Port throughput capacity follows the M/M/c queuing model:

$$\rho = \frac{\lambda}{c \cdot \mu}$$

where $\lambda$ is the arrival rate, $\mu$ is the single-berth service rate, and $c$ is the number of berths. As $\rho \to 1$, vessel waiting time tends to infinity.

### Lemma-PRT-01-02: AGV Path Conflict Graph-Theoretic Decision (AGV路径冲突的图论判定)

AGV path conflicts can be modeled as a graph coloring problem:

$$\chi(G) \leq \Delta(G) + 1$$

where $\chi(G)$ is the chromatic number of conflict graph $G$, and $\Delta(G)$ is the maximum degree. Conflict avoidance is equivalent to assigning different time slots to AGVs traversing the same path segment simultaneously.

### Prop-PRT-01-01: Relationship Between Yard Relocation Rate and Stacking Height (堆场翻箱率与堆叠高度的关系)

$$\text{RelocationRate} = 1 - \frac{1}{H_{avg}}$$

where $H_{avg}$ is the average stacking height. Higher stacking leads to higher relocation rates.

### Prop-PRT-01-02: Berth Utilization Improvement from Pre-Arrival Information (预到港信息的泊位利用率提升)

$$\Delta \eta = \eta_{withETA} - \eta_{withoutETA} \approx 15\text{-}25\%$$

---

## 3. Relations

### 3.1 Port Logistics Pipeline Operator Mapping

| Application Scenario | Operator Combination | Data Source | Latency Requirement |
|---------|---------|--------|---------|
| **Vessel Arrival Prediction** | AsyncFunction + map | AIS / Weather | < 15 min |
| **Container Tracking** | KeyedProcessFunction | RFID / GPS | < 1 min |
| **AGV Scheduling** | Broadcast + ProcessFunction | Task Queue | < 5 s |
| **Yard Optimization** | window + aggregate | Yard Status | < 10 min |
| **Customs Risk** | Async ML | Declaration Data | < 30 s |
| **Equipment Monitoring** | ProcessFunction + Timer | Sensors | < 1 min |

### 3.2 Operator Fingerprint

| Dimension | Port Logistics Characteristics |
|------|------------|
| **Core Operators** | BroadcastProcessFunction (AGV Scheduling), KeyedProcessFunction (Container State Machine), AsyncFunction (ETA / Risk Model), window + aggregate (Yard Statistics) |
| **State Types** | ValueState (Container Location), MapState (AGV Status), BroadcastState (Scheduling Policy) |
| **Time Semantics** | Processing-time dominant (scheduling real-time requirements) |
| **Data Characteristics** | Spatially dense (location data), temporally correlated (vessel arrivals), multi-source heterogeneous |
| **State Hotspots** | Popular yard area keys, active AGV keys |
| **Performance Bottlenecks** | AGV conflict resolution, external ETA API |

---

## 4. Argumentation

### 4.1 Why Port Logistics Needs Stream Processing Instead of Traditional Scheduling

Problems with traditional scheduling:

- **Static planning**: Unable to cope with vessel delays or early arrivals
- **Manual dispatching**: Low efficiency, error-prone
- **Information lag**: Container location updates are not timely

Advantages of stream processing:

- **Real-time tracking**: Container locations updated at second-level granularity
- **Dynamic dispatching**: AGV tasks adjusted according to real-time conditions
- **Predictive optimization**: ETA predictions enable proactive berth arrangement

### 4.2 AGV Conflict Avoidance

**Problem**: Multiple AGVs request the same passage at the same time.

**Solution**:

1. **Time-slot allocation**: Assign passage time slots to different AGVs
2. **Priority**: Emergency tasks (reefer containers) take precedence
3. **Path re-planning**: Automatic detour when a conflict is detected

### 4.3 Reefer Container Monitoring

**Scenario**: Temperature of reefer (refrigerated) containers must be kept below -18°C.

**Stream-processing solution**: Real-time temperature monitoring → Anomaly alert → Automatic maintenance notification → Backup container dispatching.

---

## 5. Proof / Engineering Argument

### 5.1 Real-time AGV Scheduling System

```java
public class AGVScheduler extends BroadcastProcessFunction<TaskRequest, SchedulePolicy, AGVAssignment> {
    private MapState<String, AGVState> agvFleet;

    @Override
    public void processElement(TaskRequest task, ReadOnlyContext ctx, Collector<AGVAssignment> out) throws Exception {
        // Retrieve current scheduling policy
        ReadOnlyBroadcastState<String, SchedulePolicy> policyState = ctx.getBroadcastState(POLICY_DESCRIPTOR);
        SchedulePolicy policy = policyState.get("default");

        // Find the best AGV
        String bestAGV = null;
        double bestScore = Double.NEGATIVE_INFINITY;

        for (Map.Entry<String, AGVState> entry : agvFleet.entries()) {
            AGVState agv = entry.getValue();
            if (!agv.isAvailable()) continue;

            double score = policy.calculateScore(agv, task);
            if (score > bestScore) {
                bestScore = score;
                bestAGV = entry.getKey();
            }
        }

        if (bestAGV != null) {
            AGVState assigned = agvFleet.get(bestAGV);
            assigned.assignTask(task);
            agvFleet.put(bestAGV, assigned);

            out.collect(new AGVAssignment(bestAGV, task.getId(), task.getDestination(), ctx.timestamp()));
        }
    }

    @Override
    public void processBroadcastElement(SchedulePolicy policy, Context ctx, Collector<AGVAssignment> out) {
        ctx.getBroadcastState(POLICY_DESCRIPTOR).put("default", policy);
    }
}
```

### 5.2 Container Status Tracking

```java
// Container event stream
DataStream<ContainerEvent> containers = env.addSource(new ContainerRFIDSource());

// Real-time location tracking
containers.keyBy(ContainerEvent::getContainerId)
    .process(new KeyedProcessFunction<String, ContainerEvent, ContainerLocation>() {
        private ValueState<ContainerLocation> locationState;

        @Override
        public void processElement(ContainerEvent event, Context ctx, Collector<ContainerLocation> out) throws Exception {
            ContainerLocation loc = locationState.value();
            if (loc == null) loc = new ContainerLocation(event.getContainerId());

            loc.update(event.getLocation(), event.getTimestamp());
            locationState.update(loc);

            // Check for abnormal dwell time
            if (loc.getDwellTime() > 3600000) {  // Exceeds 1 hour
                out.collect(loc.withAlert("LONG_DWELL"));
            } else {
                out.collect(loc);
            }
        }
    })
    .addSink(new ContainerTrackingSink());
```

### 5.3 Vessel Arrival Prediction

```java
// AIS data stream
DataStream<AISMessage> ais = env.addSource(new AISSource());

// ETA calculation
ais.keyBy(AISMessage::getMmsi)
    .process(new KeyedProcessFunction<String, AISMessage, ETAPrediction>() {
        private ValueState<VesselTrack> trackState;

        @Override
        public void processElement(AISMessage msg, Context ctx, Collector<ETAPrediction> out) throws Exception {
            VesselTrack track = trackState.value();
            if (track == null) track = new VesselTrack(msg.getMmsi());

            track.updatePosition(msg.getLat(), msg.getLon(), msg.getSpeed(), msg.getTimestamp());

            // Calculate ETA
            double distanceToPort = calculateDistance(track.getLastPosition(), PORT_LOCATION);
            double avgSpeed = track.getAverageSpeed(3600000);  // Average over the last 1 hour

            if (avgSpeed > 0) {
                long etaMillis = (long)(distanceToPort / avgSpeed * 3600000);
                Date eta = new Date(ctx.timestamp() + etaMillis);
                out.collect(new ETAPrediction(msg.getMmsi(), eta, distanceToPort, ctx.timestamp()));
            }

            trackState.update(track);
        }
    })
    .addSink(new PortScheduleSink());
```

---

## 6. Examples

### 6.1 Real-world: Intelligent Port Real-time Scheduling

```java
// 1. Vessel arrival prediction
DataStream<ETAPrediction> etas = env.addSource(new AISSource())
    .keyBy(AISMessage::getMmsi)
    .process(new ETACalculationFunction());

// 2. Berth allocation
etas.keyBy(ETAPrediction::getMmsi)
    .connect(berthAvailabilityBroadcast)
    .process(new BerthAllocationFunction())
    .addSink(new BerthScheduleSink());

// 3. Container tracking
DataStream<ContainerEvent> containerEvents = env.addSource(new RFIDSource());
containerEvents.keyBy(ContainerEvent::getContainerId)
    .process(new ContainerTrackingFunction())
    .addSink(new YardManagementSink());

// 4. AGV scheduling
DataStream<TaskRequest> tasks = env.addSource(new TaskQueueSource());
tasks.connect(agvStatusBroadcast)
    .process(new AGVScheduler())
    .addSink(new AGVCommandSink());
```

### 6.2 Real-world: Reefer Container Monitoring

```java
// Reefer container temperature sensors
DataStream<TemperatureReading> temps = env.addSource(new ReeferSensorSource());

// Anomaly detection
temps.keyBy(TemperatureReading::getContainerId)
    .process(new KeyedProcessFunction<String, TemperatureReading, TemperatureAlert>() {
        private ValueState<TemperatureStats> stats;

        @Override
        public void processElement(TemperatureReading reading, Context ctx, Collector<TemperatureAlert> out) throws Exception {
            TemperatureStats s = stats.value();
            if (s == null) s = new TemperatureStats();

            s.update(reading.getTemperature());

            // High-temperature alert
            if (reading.getTemperature() > reading.getMaxAllowed()) {
                out.collect(new TemperatureAlert(reading.getContainerId(), "HIGH_TEMP", reading.getTemperature(), ctx.timestamp()));
            }

            // Trend alert: continuous rise
            if (s.isRising(5) && reading.getTemperature() > reading.getMaxAllowed() - 2) {
                out.collect(new TemperatureAlert(reading.getContainerId(), "RISING_TREND", reading.getTemperature(), ctx.timestamp()));
            }

            stats.update(s);
        }
    })
    .addSink(new MaintenanceAlertSink());
```

---

## 7. Visualizations

### Port Logistics Pipeline

The following diagram illustrates the end-to-end real-time port logistics pipeline, from multi-source data ingestion through stream processing to physical execution.

```mermaid
graph TB
    subgraph Data Sources
        D1[AIS Vessel Data]
        D2[RFID Containers]
        D3[AGV Sensors]
        D4[Yard System]
        D5[Customs Declarations]
    end

    subgraph Stream Processing
        P1[ETA Prediction]
        P2[Berth Allocation]
        P3[Container Tracking]
        P4[AGV Scheduling]
        P5[Yard Optimization]
        P6[Customs Risk]
    end

    subgraph Execution
        A1[Vessel Dispatching]
        A2[Quay Crane]
        A3[AGV]
        A4[Yard Crane]
        A5[Gate]
    end

    D1 --> P1 --> P2 --> A1 --> A2
    D2 --> P3 --> A2
    D3 --> P4 --> A3 --> A4
    D4 --> P5 --> A4
    D5 --> P6 --> A5
```

---

## 8. References

[^1]: Apache Flink Documentation, "Broadcast State Pattern", 2025. https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/broadcast_state/
[^2]: T. Akidau et al., "The Dataflow Model", PVLDB, 8(12), 2015.
[^3]: D. Gross et al., "Fundamentals of Queueing Theory", Wiley, 4th Edition, 2008.

---

*Related Documents*: [01.07-two-input-operators.md](01.07-two-input-operators.md) | [realtime-supply-chain-tracking-case-study.md](realtime-supply-chain-tracking-case-study.md) | [realtime-digital-twin-case-study.md](realtime-digital-twin-case-study.md)
