# IoT Case Study: Connected Vehicle Data Processing System

> **Stage**: en/realtime-connected-vehicles-case-study | **Prerequisites**: [./pattern-event-time-processing.md](./pattern-event-time-processing.md) | **Formalization Level**: L4

---

> **Case Nature**: 🔬 Concept Verification Architecture | **Validation Status**: Based on theoretical derivation and architectural design; not independently verified by third-party production deployment.
>
> This case study describes an ideal architecture derived from the project's theoretical framework, including hypothetical performance metrics and theoretical cost models. Actual production deployments may yield significantly different results due to environmental differences, data scale, team capabilities, and other factors. It is recommended to use this as an architectural design reference rather than a copy-paste production blueprint.

## Table of Contents

- [IoT Case Study: Connected Vehicle Data Processing System](#iot-case-study-connected-vehicle-data-processing-system)
  - [Table of Contents](#table-of-contents)
  - [1. Concept Definitions](#1-concept-definitions)
    - [1.1 Connected Vehicle System Definition](#11-connected-vehicle-system-definition)
    - [1.2 Vehicle Event Types](#12-vehicle-event-types)
  - [2. Example Verification](#2-example-verification)
    - [2.1 Case Background](#21-case-background)
    - [2.2 Driving Behavior Scoring](#22-driving-behavior-scoring)
    - [2.3 Performance Metrics](#23-performance-metrics)

## 1. Concept Definitions

### 1.1 Connected Vehicle System Definition

**Def-K-10-09-01** (Connected Vehicle Data Processing System, 车联网数据处理系统): A connected vehicle system is a sextuple $\mathcal{V} = (C, S, D, N, A, \tau)$:

- $C$: Set of vehicles
- $S$: Set of sensors (GPS, speed, engine, battery, etc.)
- $D$: Data stream, $D = \{d \mid d = (t, v, s, \text{location})\}$
- $N$: Network type (5G/4G)
- $A$: Analytics applications (navigation, insurance, maintenance)
- $\tau$: Latency requirements (navigation < 100ms, diagnostics < 1s)

### 1.2 Vehicle Event Types

| Event Type | Frequency | Data Volume | Purpose |
|-----------|-----------|-------------|---------|
| GPS Location | 1Hz | Low | Navigation, trajectory |
| Driving Behavior | 10Hz | Medium | Insurance scoring |
| Vehicle Status | 1Hz | Medium | Remote diagnostics |
| Alert Events | Triggered | Low | Emergency response |
| Video Stream | 30fps | High | ADAS (Advanced Driver Assistance Systems, 高级驾驶辅助系统) |

---

## 2. Example Verification

### 2.1 Case Background

**Enterprise**: A new energy vehicle manufacturer (新能源汽车厂商)

| Metric | Value |
|--------|-------|
| Connected Vehicles | 2 million |
| Daily Data Volume | 2 PB |
| Data Upload Frequency | 1-10 Hz |
| Service Scenarios | Navigation / Insurance / Maintenance / OTA |

### 2.2 Driving Behavior Scoring

```java
/**
 * Real-time driving behavior scoring
 */

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

public class DrivingBehaviorScoring {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        DataStream<VehicleEvent> events = env
            .fromSource(createKafkaSource(),
                WatermarkStrategy.<VehicleEvent>forBoundedOutOfOrderness(Duration.ofSeconds(5))
                    .withIdleness(Duration.ofMinutes(1)),
                "Vehicle Events")
            .setParallelism(128);

        // Driving behavior analysis (5-minute window)
        DataStream<DrivingScore> scores = events
            .keyBy(VehicleEvent::getVehicleId)
            .window(TumblingEventTimeWindows.of(Time.minutes(5)))
            .process(new DrivingBehaviorAnalyzer())
            .name("Driving Score")
            .setParallelism(256);

        // Write to insurance platform
        scores.addSink(new InsurancePlatformSink());

        env.execute("Driving Behavior Scoring");
    }
}

/**
 * Driving behavior analysis
 */
class DrivingBehaviorAnalyzer extends ProcessWindowFunction<VehicleEvent, DrivingScore, String, TimeWindow> {

    @Override
    public void process(String vehicleId, Context ctx, Iterable<VehicleEvent> events,
                       Collector<DrivingScore> out) {
        int harshBraking = 0;
        int harshAcceleration = 0;
        int sharpTurn = 0;
        int speeding = 0;
        double totalDistance = 0;
        long totalDrivingTime = 0;

        VehicleEvent lastEvent = null;

        for (VehicleEvent event : events) {
            // Harsh braking detection
            if (event.getAcceleration() < -3.0) {  // m/s²
                harshBraking++;
            }

            // Harsh acceleration detection
            if (event.getAcceleration() > 3.0) {
                harshAcceleration++;
            }

            // Sharp turn detection
            if (Math.abs(event.getGyroZ()) > 0.5) {  // rad/s
                sharpTurn++;
            }

            // Speeding detection
            if (event.getSpeed() > event.getSpeedLimit() * 1.2) {
                speeding++;
            }

            // Calculate distance
            if (lastEvent != null) {
                totalDistance += GeoUtils.distance(lastEvent.getLocation(), event.getLocation());
            }

            lastEvent = event;
        }

        // Calculate score (0-100)
        double score = 100;
        score -= harshBraking * 2;
        score -= harshAcceleration * 2;
        score -= sharpTurn * 1.5;
        score -= speeding * 3;
        score = Math.max(0, score);

        out.collect(new DrivingScore(
            vehicleId,
            ctx.window().getStart(),
            score,
            harshBraking,
            harshAcceleration,
            sharpTurn,
            speeding,
            totalDistance
        ));
    }
}
```

### 2.3 Performance Metrics
>
> 🔮 **Estimated Data** | Basis: Design target values; actual achievement may vary depending on environment.

| Metric | Target | Actual |
|--------|--------|--------|
| Data Processing Latency | < 5s | 2s |
| Daily Processed Events | 20 billion | 25 billion |
| Location Accuracy | 10m | 5m |
| System Availability | 99.99% | 99.995% |

---

*Document Version: v1.0 | Last Updated: 2026-04-04*

---

*Document Version: v1.0 | Created: 2026-04-19*
