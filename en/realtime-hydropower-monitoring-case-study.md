# Operators and Real-Time Hydropower Monitoring

> **Stage**: Knowledge/10-case-studies | **Prerequisites**: [01.06-single-input-operators.md](../Knowledge/01-concept-atlas/operator-deep-dive/01.06-single-input-operators.md), [operator-energy-grid-monitoring.md](../Knowledge/06-frontier/operator-energy-grid-monitoring.md) | **Formalization Level**: L3
> **Document Positioning**: Operator fingerprints and Pipeline design for stream processing operators in real-time hydropower station operation monitoring, flood control dispatch, and equipment health diagnosis
> **Version**: 2026.04

---

## Table of Contents

- [1. Concept Definitions (Definitions)](#1-concept-definitions-definitions)
- [2. Property Derivation (Properties)](#2-property-derivation-properties)
- [3. Relationship Establishment (Relations)](#3-relationship-establishment-relations)
- [4. Argumentation Process (Argumentation)](#4-argumentation-process-argumentation)
- [5. Formal Proof / Engineering Argument (Proof / Engineering Argument)](#5-formal-proof--engineering-argument-proof--engineering-argument)
- [6. Example Verification (Examples)](#6-example-verification-examples)
- [7. Visualizations (Visualizations)](#7-visualizations-visualizations)
- [8. References (References)](#8-references-references)

---

## 1. Concept Definitions (Definitions)

### Def-HYD-01-01: Hydropower Real-time Monitoring System (水电站实时监测系统)

A hydropower real-time monitoring system is a comprehensive surveillance system for hydraulic structures, electromechanical equipment, and operating conditions:

$$\text{HydroMonitor} = (\text{Dam}_t, \text{Turbine}_t, \text{Generator}_t, \text{Transformer}_t, \text{WaterSystem}_t)$$

### Def-HYD-01-02: Reservoir Operation Chart (水库调度图)

The reservoir operation chart is a zoned rule guiding reservoir operations:

$$\text{Zone}(V_t, Q_{in,t}) \in \{\text{Normal}, \text{FloodControl}, \text{Conservation}, \text{Dead}\}$$

### Def-HYD-01-03: Vibration Severity (机组振动烈度)

Vibration severity is a comprehensive indicator measuring the operating state of rotating machinery:

$$V_s = \sqrt{\sum_{i} (a_i \cdot w_i)^2}$$

Where $a_i$ is the vibration acceleration in the $i$-th frequency band, and $w_i$ is the weight. Per ISO 10816 standard: $V_s < 2.8$ mm/s is excellent, $2.8-7.1$ is good, and $> 7.1$ is abnormal.

### Def-HYD-01-04: Turbine Efficiency (水轮机效率)

$$\eta = \frac{P_{out}}{\rho g Q H}$$

Where $P_{out}$ is the output power, $Q$ is the flow rate, and $H$ is the water head.

### Def-HYD-01-05: Flood Control Level (防洪限制水位)

The flood control level is the maximum allowable storage water level during the flood season:

$$Z_{flood} = Z_{normal} - \Delta Z_{safety}$$

---

## 2. Property Derivation (Properties)

### Lemma-HYD-01-01: Reservoir Water Balance

$$\frac{dV}{dt} = Q_{in} - Q_{out} - Q_{loss}$$

**Proof**: Directly derived from the continuity equation. ∎

### Lemma-HYD-01-02: Turbine Affinity Laws

$$\frac{Q_1}{Q_2} = \left(\frac{D_1}{D_2}\right)^3 \cdot \frac{n_1}{n_2}, \quad \frac{H_1}{H_2} = \left(\frac{D_1}{D_2}\right)^2 \cdot \left(\frac{n_1}{n_2}\right)^2$$

### Prop-HYD-01-01: Characteristic Frequencies of Vibration Spectrum

| Fault Type | Characteristic Frequency | Diagnostic Basis |
|-----------|------------------------|-----------------|
| Unbalance | 1× rotation frequency | 1× amplitude dominates |
| Misalignment | 2× rotation frequency | 2× amplitude significant |
| Oil whirl | 0.42-0.48× rotation frequency | Half-frequency component |
| Blade pass | Blade count × rotation frequency | High-frequency periodic |

### Prop-HYD-01-02: Water Level - Power Generation Relationship

$$P = \eta \cdot \rho g \cdot Q \cdot (Z_{up} - Z_{down})$$

---

## 3. Relationship Establishment (Relations)

### 3.1 Hydropower Station Monitoring Pipeline Operator Mapping

| Application Scenario | Operator Combination | Data Source | Latency Requirement |
|---------|---------|--------|---------|
| **Hydrological monitoring** | Source + map | Water level / rainfall sensors | < 1 min |
| **Vibration analysis** | AsyncFunction + window | Acceleration sensors | < 5 min |
| **Efficiency calculation** | map | Flow rate / power | < 1 min |
| **Flood control dispatch** | Broadcast + ProcessFunction | Dispatch instructions | < 10 min |
| **Equipment diagnosis** | Async ML | Multi-sensor | < 15 min |

### 3.2 Operator Fingerprint

| Dimension | Hydropower Monitoring Characteristics |
|------|------------|
| **Core operators** | ProcessFunction (equipment state machine), AsyncFunction (spectrum analysis), BroadcastProcessFunction (dispatch instructions), window+aggregate (statistics) |
| **State types** | ValueState (equipment health index), MapState (sensor calibration), BroadcastState (dispatch rules) |
| **Time semantics** | Event time (sensor timestamps) |
| **Data characteristics** | Periodicity (day/night/season), spatial correlation (upstream/downstream), strong causality |
| **State scale** | Keyed by unit; large hydropower stations may have dozens of units |
| **Performance bottleneck** | Spectrum analysis computation, external weather API |

---

## 4. Argumentation Process (Argumentation)

### 4.1 Why Hydropower Stations Need Stream Processing Instead of Traditional SCADA

Problems with traditional SCADA (Supervisory Control and Data Acquisition, 数据采集与监视控制系统):

- Second-level refresh: unable to capture high-frequency vibration signals
- Manual interpretation: fault discovery lags
- Offline analysis: health trends cannot be tracked in real time

Advantages of stream processing:

- Millisecond-level sampling: high-frequency vibration real-time analysis
- Automatic diagnosis: AI models identify fault patterns in real time
- Predictive maintenance: schedule maintenance ahead of time based on trends

### 4.2 Real-Time Decision Making for Flood Control Dispatch

**Scenario**: Upstream heavy rain causes a surge in inflow.

**Stream processing solution**:

1. Real-time rainfall → flood forecasting model → inflow prediction
2. Current reservoir capacity → comparison with flood control limit → discharge decision
3. Downstream safety → flow control → automatic gate adjustment

### 4.3 Early Warning for Unit Vibration

**Problem**: Initial vibration changes from turbine runner cracks are subtle and difficult for humans to detect.

**Solution**: Stream processing real-time spectrum analysis → characteristic frequency energy change detection → trend early warning.

---

## 5. Formal Proof / Engineering Argument (Proof / Engineering Argument)

### 5.1 Real-Time Vibration Monitoring

```java
// Vibration sensor stream
DataStream<VibrationData> vibration = env.addSource(new AccelerometerSource());

// Spectrum analysis
vibration.keyBy(VibrationData::getUnitId)
    .window(TumblingProcessingTimeWindows.of(Time.minutes(5)))
    .process(new ProcessFunction<Iterable<VibrationData>, VibrationSpectrum>() {
        @Override
        public void process(Iterable<VibrationData> values, Context ctx, Collector<VibrationSpectrum> out) {
            List<Double> samples = new ArrayList<>();
            values.forEach(v -> samples.add(v.getAcceleration()));

            // FFT spectrum analysis
            Complex[] fftResult = FFT.fft(samples.stream().mapToDouble(Double::doubleValue).toArray());

            double[] magnitudes = new double[fftResult.length / 2];
            for (int i = 0; i < magnitudes.length; i++) {
                magnitudes[i] = fftResult[i].abs();
            }

            // Extract characteristic frequencies
            double rotationFreq = 50.0 / 60.0;  // 50Hz = 3000rpm
            double[] featureFreqs = {1, 2, 0.45};

            Map<String, Double> features = new HashMap<>();
            for (double f : featureFreqs) {
                int idx = (int)(f * rotationFreq * samples.size() / 200.0);
                features.put(f + "x", magnitudes[idx]);
            }

            out.collect(new VibrationSpectrum(ctx.getCurrentKey(), features, ctx.timestamp()));
        }
    })
    .addSink(new DiagnosticSink());
```

### 5.2 Reservoir Flood Control Dispatch

```java
// Inflow stream
DataStream<InflowData> inflow = env.addSource(new HydrologicalSource());

// Real-time dispatch decision
inflow.keyBy(InflowData::getReservoirId)
    .connect(dispatchRulesBroadcast)
    .process(new BroadcastProcessFunction<InflowData, DispatchRule, FloodControlCommand>() {
        @Override
        public void processElement(InflowData data, ReadOnlyContext ctx, Collector<FloodControlCommand> out) {
            ReadOnlyBroadcastState<String, DispatchRule> rules = ctx.getBroadcastState(RULE_DESCRIPTOR);
            DispatchRule rule = rules.get(data.getReservoirId());

            if (rule == null) return;

            // Calculate current reservoir capacity status
            double currentLevel = data.getCurrentLevel();
            double floodLimit = rule.getFloodControlLevel();
            double inflowRate = data.getInflowRate();

            if (currentLevel > floodLimit && inflowRate > rule.getMaxInflow()) {
                double releaseRate = calculateRelease(currentLevel, floodLimit, inflowRate);
                out.collect(new FloodControlCommand(data.getReservoirId(), releaseRate, "FLOOD_RELEASE", ctx.timestamp()));
            }
        }

        @Override
        public void processBroadcastElement(DispatchRule rule, Context ctx, Collector<FloodControlCommand> out) {
            ctx.getBroadcastState(RULE_DESCRIPTOR).put(rule.getReservoirId(), rule);
        }
    })
    .addSink(new GateControlSink());
```

---

## 6. Example Verification (Examples)

### 6.1 Real-World Case: Large Hydropower Station Intelligent Monitoring

```java
// 1. Multi-sensor data ingestion
DataStream<VibrationData> vibration = env.addSource(new AccelerometerSource());
DataStream<InflowData> inflow = env.addSource(new HydrologicalSource());
DataStream<PowerData> power = env.addSource(new GeneratorSource());

// 2. Vibration diagnosis
vibration.keyBy(VibrationData::getUnitId)
    .window(TumblingProcessingTimeWindows.of(Time.minutes(5)))
    .process(new VibrationDiagnosticFunction())
    .addSink(new MaintenanceAlertSink());

// 3. Efficiency monitoring
power.connect(inflow.keyBy(InflowData::getReservoirId))
    .process(new CoProcessFunction<PowerData, InflowData, EfficiencyReport>() {
        private ValueState<InflowData> lastInflow;

        @Override
        public void processElement1(PowerData p, Context ctx, Collector<EfficiencyReport> out) {
            InflowData inf = lastInflow.value();
            if (inf == null) return;

            double efficiency = p.getPower() / (9.81 * inf.getFlowRate() * inf.getHead());
            out.collect(new EfficiencyReport(p.getUnitId(), efficiency, ctx.timestamp()));
        }

        @Override
        public void processElement2(InflowData inf, Context ctx, Collector<EfficiencyReport> out) {
            lastInflow.update(inf);
        }
    })
    .addSink(new EfficiencyDashboardSink());

// 4. Flood control dispatch
inflow.connect(dispatchRulesBroadcast)
    .process(new FloodControlFunction())
    .addSink(new GateControlSink());
```

---

## 7. Visualizations (Visualizations)

### Hydropower Station Monitoring Pipeline

```mermaid
graph TB
    subgraph Perception Layer
        S1[Water Level Gauge]
        S2[Vibration Sensor]
        S3[Power Transmitter]
        S4[Rainfall Station]
    end

    subgraph Analysis Layer
        A1[Hydrological Analysis]
        A2[Vibration Spectrum]
        A3[Efficiency Calculation]
        A4[Flood Control Dispatch]
    end

    subgraph Execution Layer
        E1[Dispatch Dashboard]
        E2[Maintenance Work Order]
        E3[Gate Control]
    end

    S1 --> A1 --> A4 --> E3
    S2 --> A2 --> E2
    S3 --> A3 --> E1
    S4 --> A1
```

---

## 8. References (References)






---

*Related Documents*: [01.06-single-input-operators.md](../Knowledge/01-concept-atlas/operator-deep-dive/01.06-single-input-operators.md) | [operator-energy-grid-monitoring.md](../Knowledge/06-frontier/operator-energy-grid-monitoring.md) | [realtime-energy-trading-case-study.md](../Knowledge/10-case-studies/realtime-energy-trading-case-study.md)
