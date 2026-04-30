# Real-time Construction Site Safety Monitoring Case Study

> **Stage**: Knowledge/ Flink/ | **Prerequisites**: [Stream Operator Panoramic Taxonomy (算子全景分类)](operator-taxonomy.md) | [IoT Stream Processing (IoT流处理)](operator-iot-stream-processing.md) | **Formalization Level**: L4

## 1. Definitions

### Def-CST-01-01: Smart Construction Safety System (智慧工地安全系统)

The Smart Construction Safety System is an integrated system that performs real-time monitoring and risk early warning for personnel, equipment, and environment at construction sites through tower crane sensors, deep foundation pit monitoring, personnel positioning devices, and stream computing platforms.

$$\mathcal{C} = (T, E, P, W, F)$$

where $T$ is the tower crane status stream, $E$ is the deep foundation pit monitoring stream, $P$ is the personnel positioning stream, $W$ is the environmental monitoring stream (dust/noise), and $F$ is the stream computing processing topology.

### Def-CST-01-02: Tower Crane Anti-collision Distance (塔吊防碰撞安全距离)

Minimum safe distance between tower cranes:

$$D_{safe} = D_{brake} + D_{wind} + D_{margin}$$

where $D_{brake}$ is the braking distance, $D_{wind}$ is the wind-induced swing distance, and $D_{margin}$ is the safety margin (typically 2m).

### Def-CST-01-03: Foundation Pit Deformation Rate (深基坑变形速率)

Horizontal displacement rate of the foundation pit enclosure structure:

$$v_{deform} = \frac{\Delta x}{\Delta t}$$

Alert thresholds: $v_{deform} > 2$ mm/day requires early warning; $v_{deform} > 5$ mm/day requires emergency response.

## 2. Examples

### 2.1 Tower Crane Real-time Monitoring

```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

DataStream<CraneStatus> craneStatus = env
    .addSource(new MqttSource("construction/crane/+/status"))
    .map(new CraneParser());

// Anti-collision detection
DataStream<CollisionAlert> collisions = craneStatus
    .keyBy(c -> c.getSiteId())
    .process(new AntiCollisionFunction() {
        @Override
        public void processElement(CraneStatus crane, Context ctx,
                                   Collector<CollisionAlert> out) {
            List<CraneStatus> nearby = getNearbyCranes(crane);
            for (CraneStatus other : nearby) {
                double distance = calculateDistance(crane, other);
                if (distance < SAFE_DISTANCE) {
                    out.collect(new CollisionAlert(
                        crane.getCraneId(), other.getCraneId(),
                        distance, ctx.timestamp()
                    ));
                }
            }
        }
    });

collisions.addSink(new AlertSink());
```

### 2.2 Personnel Positioning and Danger Zone Alert

```java
DataStream<WorkerPosition> workers = env
    .addSource(new UwbSource("construction/uwb"))
    .map(new WorkerParser());

DataStream<DangerAlert> dangerAlerts = workers
    .keyBy(w -> w.getWorkerId())
    .process(new DangerZoneFunction() {
        @Override
        public void processElement(WorkerPosition worker, Context ctx,
                                   Collector<DangerAlert> out) {
            if (isInDangerZone(worker.getPosition())) {
                out.collect(new DangerAlert(
                    worker.getWorkerId(),
                    worker.getPosition(),
                    "ENTERED_DANGER_ZONE",
                    ctx.timestamp()
                ));
            }
        }
    });

dangerAlerts.addSink(new AlertSink());
```

## 3. References
