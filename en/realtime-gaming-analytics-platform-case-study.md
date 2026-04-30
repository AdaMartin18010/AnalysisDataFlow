# Real-Time Gaming Analytics Platform Case Study

> Stage: Knowledge | Prerequisites: [Related Documents] | Formalization Level: L3

> **Case ID**: 10.5.3
> **Industry**: Gaming/Entertainment
> **Scenario**: Real-time player behavior analytics, anti-cheat, real-time operations
> **Scale**: 1 million concurrent players, 100 million events/minute
> **Completion Date**: 2026-04-09
> **Document Version**: v1.0

---

> **Case Nature**: 🔬 Proof-of-Concept Architecture | **Validation Status**: Based on theoretical derivation and architectural design, not independently verified in production by a third party
>
> This case study describes an ideal architecture derived from the project's theoretical framework, including hypothetical performance metrics and a theoretical cost model.
> Actual production deployment may yield significantly different results due to environmental differences, data scale, team capabilities, and other factors.
> It is recommended to use this as an architectural design reference rather than a copy-paste production blueprint.
>

## Executive Summary

### Business Background

A leading gaming company built a real-time analytics platform:

- 1 million simultaneous online players, 50 million DAU (Daily Active Users)
- Need real-time understanding of player behavior to optimize gaming experience
- Combat外挂 (cheating tools) and cheating behavior
- Support real-time adjustment of operational campaigns

### Technical Challenges
>
> 🔮 **Estimated Data** | Basis: Derived from industry reference values and theoretical analysis, not from actual test environments


| Challenge | Description | Impact |
|-----------|-------------|--------|
| Ultra-High Concurrency | 100 million events/minute, peak 200 million | System throughput |
| Real-Time Requirements | Dashboard latency < 1s | Operational decision-making |
| Complex Analytics | Player behavior pattern recognition | Anti-cheat accuracy |
| Data Diversity | Client + Server + Third-party | Data integration |

### Solution Overview

Adopted a **Flink + Kafka + ClickHouse + Superset** technology stack:

- Unified collection of client埋点 (tracking points) and server-side logs
- Flink real-time ETL and feature engineering
- ClickHouse for time-series data storage
- Superset for visualized analytics
- Latency reduced from 5s to 500ms

---

## 1. Business Scenario Analysis

### 1.1 Business Process

```mermaid
flowchart TB
    subgraph DataSources[Data Sources]
        C1[Client Tracking]
        S1[Server Logs]
        T1[Third-Party Data]
    end

    subgraph IngestionLayer[Ingestion Layer]
        SDK[Game SDK]
        BEACON[Beacon Service]
        LOG[Log Collection]
    end

    subgraph ProcessingLayer[Real-Time Processing Layer]
        ETL[Flink ETL]
        AGG[Real-Time Aggregation]
        ML[Feature Engineering]
    end

    subgraph StorageLayer[Storage Layer]
        CH[ClickHouse]
        ES[Elasticsearch]
        Redis[Redis]
    end

    subgraph ApplicationLayer[Application Layer]
        BI[Superset BI]
        AC[Anti-Cheat System]
        OP[Operations Platform]
    end

    C1 --> SDK --> BEACON
    S1 --> LOG
    T1 --> BEACON
    BEACON --> Kafka
    LOG --> Kafka
    Kafka --> ETL --> AGG --> ML
    AGG --> CH
    ML --> ES
    ML --> Redis
    CH --> BI
    ES --> AC
    Redis --> OP
```

### 1.2 Data Scale
>
> 🔮 **Estimated Data** | Basis: Derived from industry reference values and theoretical analysis, not from actual test environments


| Metric | Value | Description |
|--------|-------|-------------|
| DAU (Daily Active Users) | 50 million | Daily active users |
| Concurrent Online | 1 million | Peak 1.5 million |
| Event Types | 200+ | Click, movement, combat, etc. |
| Daily Event Volume | 100 billion | Client + server |
| Real-Time Stream | 100 million/minute | Peak 200 million/minute |
| Data Size | 500 TB/day | Raw data |

### 1.3 Analytics Scenarios
>
> 🔮 **Estimated Data** | Basis: Derived from industry reference values and theoretical analysis, not from actual test environments


| Scenario | Description | Latency Requirement |
|----------|-------------|---------------------|
| Real-Time Dashboard | Online users, revenue, retention | < 1s |
| Anti-Cheat Detection | 外挂 (cheat tool) identification, abnormal behavior | < 200ms |
| Operational Campaigns | Real-time campaign effectiveness monitoring | < 5s |
| Player Profile | Real-time tag updates | < 10s |

---

## 2. Architecture Design

### 2.1 System Architecture Diagram

```mermaid
graph TB
    subgraph Client[Game Client]
        Unity[Unity SDK]
        UE[UE SDK]
        Mobile[Mobile SDK]
    end

    subgraph Ingestion[Data Ingestion Layer]
        LB[Load Balancer]
        Beacon[Beacon Service Cluster<br/>100 instances]
        KafkaIn[Kafka<br/>100 partitions]
    end

    subgraph Processing[Real-Time Processing Layer]
        subgraph FlinkCluster[Flink Cluster]
            JM[JobManager]
            TM1[TM: ETL]
            TM2[TM: Aggregation]
            TM3[TM: ML Features]
            TM4[TM: Anti-Cheat]
        end
    end

    subgraph Storage[Storage Layer]
        CH[ClickHouse<br/>10 shards]
        ES[Elasticsearch<br/>20 nodes]
        Redis[Redis Cluster<br/>50 nodes]
        S3[S3<br/>Cold Storage]
    end

    subgraph Analytics[Analytics Layer]
        Superset[Superset BI]
        Grafana[Grafana Monitoring]
        Jupyter[Jupyter Analytics]
    end

    Unity --> LB --> Beacon --> KafkaIn
    UE --> LB
    Mobile --> LB
    KafkaIn --> FlinkCluster
    TM1 --> CH
    TM2 --> CH
    TM3 --> ES --> Redis
    TM4 --> Redis
    CH --> Superset
    CH --> Grafana
    ES --> Jupyter
```

### 2.2 Component Selection

| Component | Selection | Rationale |
|-----------|-----------|-----------|
| Data Collection | In-house SDK | Customization, performance optimization |
| Message Queue | Kafka 3.5 | High throughput, low latency |
| Stream Processing | Flink 2.1 | Complex processing, low latency |
| Time-Series Storage | ClickHouse 23.x | High-performance OLAP |
| Search | ES 8.x | Log retrieval, anti-cheat |
| Cache | Redis 7.0 | Real-time feature queries |
| BI | Superset 3.0 | Open source, customizable |

### 2.3 Data Flow Design

```mermaid
graph LR
    subgraph RawData[Raw Data]
        E1[Client Events]
        E2[Server Logs]
        E3[Payment Data]
    end

    subgraph CleanData[Clean Data]
        C1[Standardized Events]
        C2[Session Data]
        C3[User Attributes]
    end

    subgraph FeatureData[Feature Data]
        F1[Real-Time Features]
        F2[Aggregated Metrics]
        F3[Behavior Tags]
    end

    subgraph AppData[Application Data]
        A1[Dashboard]
        A2[Anti-Cheat]
        A3[Operations]
    end

    E1 -->|SDK| C1 -->|Flink| F1 -->|Redis| A1
    E2 -->|Log| C2 -->|Flink| F2 -->|ClickHouse| A2
    E3 -->|API| C3 -->|Flink| F3 -->|ES| A3
```

---

## 3. Technical Implementation

### 3.1 Game Event Collection

```java
// Game tracking SDK (埋点SDK)
public class GameAnalyticsSDK {

    private static GameAnalyticsSDK instance;
    private EventQueue eventQueue;
    private AnalyticsConfig config;

    // Singleton pattern
    public static synchronized GameAnalyticsSDK getInstance() {
        if (instance == null) {
            instance = new GameAnalyticsSDK();
        }
        return instance;
    }

    // Initialization
    public void init(Context context, String appKey) {
        this.config = new AnalyticsConfig(appKey);
        this.eventQueue = new EventQueue(config.getQueueSize());

        // Start the send thread
        startFlushTimer();

        // Register lifecycle listeners
        registerLifecycleCallbacks(context);
    }

    // Track event
    public void trackEvent(String eventName, Map<String, Object> properties) {
        GameEvent event = new GameEvent.Builder()
            .setEventName(eventName)
            .setProperties(properties)
            .setTimestamp(System.currentTimeMillis())
            .setUserId(getUserId())
            .setSessionId(getSessionId())
            .setDeviceInfo(getDeviceInfo())
            .build();

        eventQueue.enqueue(event);

        // Flush critical events immediately
        if (isCriticalEvent(eventName)) {
            flushImmediately();
        }
    }

    // Track level start
    public void trackLevelStart(String levelId, int difficulty) {
        Map<String, Object> props = new HashMap<>();
        props.put("level_id", levelId);
        props.put("difficulty", difficulty);
        props.put("player_level", getPlayerLevel());
        trackEvent("level_start", props);
    }

    // Track level completion
    public void trackLevelComplete(String levelId, int score, int stars,
                                   long durationMs) {
        Map<String, Object> props = new HashMap<>();
        props.put("level_id", levelId);
        props.put("score", score);
        props.put("stars", stars);
        props.put("duration_ms", durationMs);
        props.put("attempt_count", getAttemptCount(levelId));
        trackEvent("level_complete", props);
    }

    // Track purchase
    public void trackPurchase(String productId, double price, String currency) {
        Map<String, Object> props = new HashMap<>();
        props.put("product_id", productId);
        props.put("price", price);
        props.put("currency", currency);
        props.put("payment_method", getPaymentMethod());
        trackEvent("purchase", props);
    }

    // Batch send
    private void flush() {
        List<GameEvent> events = eventQueue.drain();
        if (events.isEmpty()) return;

        // Compress
        byte[] compressed = compress(events);

        // Send
        sendToServer(compressed);
    }

    private boolean isCriticalEvent(String eventName) {
        return eventName.equals("purchase") ||
               eventName.equals("cheat_detected") ||
               eventName.equals("account_banned");
    }
}
```

### 3.2 Real-Time Anti-Cheat Detection

```java
// Anti-cheat detection - Flink CEP

import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.streaming.api.windowing.time.Time;

public class AntiCheatDetection {

    // Detect bot behavior (regular operation patterns)
    public static void detectBotBehavior(DataStream<GameEvent> events) {

        Pattern<GameEvent, ?> botPattern = Pattern
            .<GameEvent>begin("regular-actions")
            .where(new IterativeCondition<GameEvent>() {
                @Override
                public boolean filter(GameEvent event, Context<GameEvent> ctx) {
                    // Detect if operation intervals are too regular
                    return event.getEventName().equals("player_action");
                }
            })
            .timesOrMore(20)
            .within(Time.minutes(5));

        CEP.pattern(events.keyBy(GameEvent::getUserId), botPattern)
            .process(new PatternProcessFunction<GameEvent, CheatAlert>() {
                @Override
                public void processMatch(Map<String, List<GameEvent>> match,
                        Context ctx, Collector<CheatAlert> out) {

                    List<GameEvent> actions = match.get("regular-actions");

                    // Calculate standard deviation of operation intervals
                    List<Long> intervals = calculateIntervals(actions);
                    double stdDev = calculateStdDev(intervals);

                    // If standard deviation is small, the operation pattern is too regular
                    if (stdDev < 50) { // Less than 50ms
                        CheatAlert alert = new CheatAlert(
                            actions.get(0).getUserId(),
                            "BOT_BEHAVIOR",
                            "Regular action pattern detected",
                            stdDev,
                            System.currentTimeMillis()
                        );
                        out.collect(alert);
                    }
                }
            })
            .addSink(new CheatAlertSink());
    }

    // Detect speed hack (abnormal movement speed)
    public static void detectSpeedHack(DataStream<MovementEvent> movements) {

        movements
            .keyBy(MovementEvent::getPlayerId)
            .process(new KeyedProcessFunction<String, MovementEvent, CheatAlert>() {

                private ValueState<Position> lastPositionState;
                private ValueState<Long> lastTimeState;

                @Override
                public void open(Configuration parameters) {
                    lastPositionState = getRuntimeContext().getState(
                        new ValueStateDescriptor<>("lastPos", Position.class));
                    lastTimeState = getRuntimeContext().getState(
                        new ValueStateDescriptor<>("lastTime", Long.class));
                }

                @Override
                public void processElement(MovementEvent event, Context ctx,
                        Collector<CheatAlert> out) throws Exception {

                    Position lastPos = lastPositionState.value();
                    Long lastTime = lastTimeState.value();

                    if (lastPos != null && lastTime != null) {
                        double distance = calculateDistance(lastPos, event.getPosition());
                        long timeDiff = event.getTimestamp() - lastTime;

                        if (timeDiff > 0) {
                            double speed = distance / timeDiff * 1000; // m/s

                            // If speed exceeds the game-defined maximum
                            double maxSpeed = getMaxPlayerSpeed(event.getPlayerType());
                            if (speed > maxSpeed * 1.5) {
                                CheatAlert alert = new CheatAlert(
                                    event.getPlayerId(),
                                    "SPEED_HACK",
                                    String.format("Speed %.2f m/s exceeds limit %.2f m/s",
                                        speed, maxSpeed),
                                    speed,
                                    event.getTimestamp()
                                );
                                out.collect(alert);
                            }
                        }
                    }

                    lastPositionState.update(event.getPosition());
                    lastTimeState.update(event.getTimestamp());
                }
            });
    }

    // Detect wall hack (seeing what should not be seen)
    public static void detectWallHack(DataStream<PlayerViewEvent> views) {

        views
            .filter(event -> event.getTargetType().equals("ENEMY"))
            .filter(event -> !event.isTargetVisible())
            .filter(event -> event.getHitRate() > 0.8)  // High hit rate
            .addSink(new SinkFunction<PlayerViewEvent>() {
                @Override
                public void invoke(PlayerViewEvent event, Context context) {
                    // Record suspicious behavior, accumulate evidence
                    CheatEvidence evidence = new CheatEvidence(
                        event.getPlayerId(),
                        "WALL_HACK",
                        "High hit rate on invisible targets",
                        event.getHitRate(),
                        event.getTimestamp()
                    );

                    // Trigger alert if evidence is sufficient
                    if (accumulateEvidence(evidence) > THRESHOLD) {
                        triggerBan(event.getPlayerId(), "WALL_HACK");
                    }
                }
            });
    }
}
```

### 3.3 Real-Time Metrics Calculation

```java
import org.apache.flink.streaming.api.datastream.DataStream;

import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.streaming.api.windowing.time.Time;


// Real-time player retention calculation
public class RetentionCalculation {

    public static void calculateRealtimeRetention(
            DataStream<LoginEvent> logins) {

        // Calculate real-time retention rate
        DataStream<RetentionMetric> retention = logins
            .keyBy(LoginEvent::getUserId)
            .window(TumblingEventTimeWindows.of(Time.days(1)))
            .aggregate(new AggregateFunction<LoginEvent, Set<String>, Integer>() {
                @Override
                public Set<String> createAccumulator() {
                    return new HashSet<>();
                }

                @Override
                public Set<String> add(LoginEvent event, Set<String> acc) {
                    acc.add(event.getUserId());
                    return acc;
                }

                @Override
                public Integer getResult(Set<String> acc) {
                    return acc.size();
                }

                @Override
                public Set<String> merge(Set<String> a, Set<String> b) {
                    a.addAll(b);
                    return a;
                }
            })
            .windowAll(TumblingEventTimeWindows.of(Time.minutes(5)))
            .aggregate(new AggregateFunction<Integer, List<Integer>, RetentionMetric>() {
                @Override
                public List<Integer> createAccumulator() {
                    return new ArrayList<>();
                }

                @Override
                public List<Integer> add(Integer count, List<Integer> acc) {
                    acc.add(count);
                    return acc;
                }

                @Override
                public RetentionMetric getResult(List<Integer> acc) {
                    if (acc.isEmpty()) return new RetentionMetric(0, 0);

                    int today = acc.get(acc.size() - 1);
                    int yesterday = acc.size() > 1 ? acc.get(acc.size() - 2) : today;

                    double retentionRate = yesterday > 0 ?
                        (double) today / yesterday * 100 : 0;

                    return new RetentionMetric(today, retentionRate);
                }

                @Override
                public List<Integer> merge(List<Integer> a, List<Integer> b) {
                    a.addAll(b);
                    return a;
                }
            });

        retention.addSink(new RetentionMetricSink());
    }

    // Real-time LTV calculation
    public static void calculateRealtimeLTV(
            DataStream<PurchaseEvent> purchases) {

        purchases
            .keyBy(PurchaseEvent::getUserId)
            .window(TumblingEventTimeWindows.of(Time.days(7)))
            .aggregate(new AggregateFunction<PurchaseEvent, Double, Double>() {
                @Override
                public Double createAccumulator() {
                    return 0.0;
                }

                @Override
                public Double add(PurchaseEvent event, Double acc) {
                    return acc + event.getAmount();
                }

                @Override
                public Double getResult(Double acc) {
                    return acc;
                }

                @Override
                public Double merge(Double a, Double b) {
                    return a + b;
                }
            })
            .windowAll(TumblingEventTimeWindows.of(Time.hours(1)))
            .process(new ProcessAllWindowFunction<Double, LTVMetric, TimeWindow>() {
                @Override
                public void process(Context context, Iterable<Double> elements,
                        Collector<LTVMetric> out) {

                    double totalRevenue = 0;
                    int payingUsers = 0;

                    for (Double ltv : elements) {
                        totalRevenue += ltv;
                        if (ltv > 0) payingUsers++;
                    }

                    double arpu = payingUsers > 0 ? totalRevenue / payingUsers : 0;

                    out.collect(new LTVMetric(
                        totalRevenue,
                        payingUsers,
                        arpu,
                        context.window().getEnd()
                    ));
                }
            })
            .addSink(new LTVMetricSink());
    }
}
```

### 3.4 Key Configurations

```yaml
# Flink configuration
flink:
  parallelism:
    default: 200
    source: 100
    process: 150
    sink: 50

  checkpoint:
    interval: 30s
    mode: AT_LEAST_ONCE  # Game logs can tolerate minor duplicates

  state:
    backend: rocksdb
    incremental: true

  network:
    memory:
      fraction: 0.25

# ClickHouse configuration
clickhouse:
  cluster:
    shards: 10
    replicas: 2

  tables:
    events:
      engine: MergeTree
      partition: toYYYYMMDD(event_time)
      order: (game_id, event_name, event_time)
      ttl: event_time + INTERVAL 90 DAY

# Game SDK configuration
sdk:
  queue:
    size: 10000
    flush_interval: 30s
    batch_size: 100

  network:
    timeout: 10s
    retry_count: 3
    compression: true
```

---

## 4. Performance Metrics

### 4.1 Latency Analysis
>
> 🔮 **Estimated Data** | Basis: Derived from industry reference values and theoretical analysis, not from actual test environments


| Stage | P50 | P99 | Target | Status |
|-------|-----|-----|--------|--------|
| Client Collection | 10ms | 50ms | < 100ms | ✅ |
| Network Transfer | 50ms | 200ms | < 300ms | ✅ |
| Flink Processing | 100ms | 500ms | < 1s | ✅ |
| Storage Write | 50ms | 200ms | < 300ms | ✅ |
| Dashboard | 200ms | 800ms | < 1s | ✅ |
| **End-to-End** | **410ms** | **1750ms** | **< 2s** | ✅ |

### 4.2 System Capacity
>
> 🔮 **Estimated Data** | Basis: Derived from industry reference values and theoretical analysis, not from actual test environments


| Metric | Design Value | Measured Value | Headroom |
|--------|--------------|----------------|----------|
| Event Throughput | 100 million/minute | 150 million/minute | 50% |
| Concurrent Connections | 1 million | 1.5 million | 50% |
| Query QPS | 1000 | 2000 | 100% |
| Storage Write | 500K/s | 800K/s | 60% |

### 4.3 Business Impact
>
> 🔮 **Estimated Data** | Basis: Derived from industry reference values and theoretical analysis, not from actual test environments


| Metric | Before Optimization | After Optimization | Improvement |
|--------|---------------------|--------------------|-------------|
| Dashboard Latency | 5s | 500ms | **90%** ↓ |
| Anti-Cheat Detection Rate | 70% | 95% | **+36%** |
| Cheat Ban Response Time | Hours | Minutes | **99%** ↓ |
| Operational Decision Efficiency | Days | Hours | **95%** ↓ |

---

## 5. Lessons Learned

### 5.1 Best Practices

1. **Client-Side Optimization**
   - Local caching + batch sending
   - Network-adaptive downsampling
   - Critical events reported in real-time

2. **Server-Side Optimization**
   - Multi-level degradation strategy
   - Hot data pre-aggregation
   - Asynchronous processing for non-critical paths

3. **Cost Control**
   - Hot/cold data tiering
   - Dynamic sampling rate adjustment
   - Elastic scaling of compute resources

### 5.2 Pitfalls

| Issue | Cause | Solution |
|-------|-------|----------|
| Client OOM | Memory cache too large | Disk overflow + compression |
| ClickHouse write bottleneck | Single-shard hotspot | Hash sharding + batching |
| Anti-cheat false positives | Model threshold too high | Manual review + appeals |
| Network congestion | Global players reporting simultaneously | CDN edge nodes |

### 5.3 Optimization Recommendations

1. **Near-Term Optimization**
   - Introduce Apache Pulsar to replace Kafka
   - ClickHouse materialized view optimization
   - Federated learning to protect player privacy

2. **Mid-Term Planning**
   - Real-time digital twin of the game world
   - AI-generated game content (AIGC)
   - Metaverse cross-game data analytics

---

## 6. Appendix

### 6.1 Core Metric Definitions

```sql
-- Daily Active Users (DAU)
SELECT uniqExact(user_id) as dau
FROM events
WHERE event_time >= today()
  AND event_time < today() + 1

-- Retention Rate
SELECT
    first_date,
    countIf(date_diff = 0) as d0,
    countIf(date_diff = 1) as d1,
    countIf(date_diff = 7) as d7,
    round(d1 / d0 * 100, 2) as retention_d1
FROM (
    SELECT
        user_id,
        min(toDate(event_time)) as first_date,
        date_diff('day', first_date, toDate(event_time)) as date_diff
    FROM events
    GROUP BY user_id
)
GROUP BY first_date

-- Average Revenue Per User (ARPU)
SELECT
    toDate(event_time) as date,
    sum(purchase_amount) / uniqExact(user_id) as arpu
FROM events
WHERE event_name = 'purchase'
GROUP BY date
```

### 6.2 Monitoring Alerts

```yaml
alerts:
  - name: HighLatency
    expr: dashboard_latency_p99 > 2
    for: 5m
    severity: warning

  - name: DataLoss
    expr: (events_received - events_processed) / events_received > 0.01
    for: 1m
    severity: critical

  - name: LowRetention
    expr: retention_rate_d1 < 30
    for: 1h
    severity: warning
```

---

*This case study was compiled by the AnalysisDataFlow project for educational and exchange purposes only.*
