# Gaming Case Study: Real-Time Battle Data Processing System

> **Stage**: Knowledge/10-case-studies/gaming | **Prerequisites**: [pattern-windowed-aggregation.md](pattern-windowed-aggregation.md) | **Formalization Level**: L4

---

> **Case Nature**: 🔬 Concept Validation Architecture | **Validation Status**: Based on theoretical derivation and architectural design; not independently verified in production
>
> This case study describes an ideal architecture derived from the project's theoretical framework, including hypothetical performance metrics and theoretical cost models.
> Actual production deployments may vary significantly due to environmental differences, data scale, team capabilities, and other factors.
> It is recommended to use this as an architectural design reference rather than a direct copy-and-paste production blueprint.

## Table of Contents

- [Gaming Case Study: Real-Time Battle Data Processing System](#gaming-case-study-real-time-battle-data-processing-system)
  - [Table of Contents](#table-of-contents)
  - [1. Definitions](#1-definitions)
    - [1.1 Real-Time Battle System Definition](#11-real-time-battle-system-definition)
    - [1.2 Game Event Types](#12-game-event-types)
    - [1.3 Real-Time Levels](#13-real-time-levels)
  - [2. Properties](#2-properties)
    - [2.1 Event Order Consistency](#21-event-order-consistency)
    - [2.2 Throughput Guarantee](#22-throughput-guarantee)
  - [3. Relations](#3-relations)
    - [3.1 Data Processing Pipeline](#31-data-processing-pipeline)
    - [3.2 Analysis Types](#32-analysis-types)
  - [4. Argumentation](#4-argumentation)
    - [4.1 Necessity of Real-Time Processing](#41-necessity-of-real-time-processing)
    - [4.2 Technical Challenges](#42-technical-challenges)
  - [5. Proof / Engineering Argument](#5-proof--engineering-argument)
    - [5.1 Real-Time Battle Statistics](#51-real-time-battle-statistics)
    - [5.2 Anti-Cheat Detection](#52-anti-cheat-detection)
  - [6. Examples](#6-examples)
    - [6.1 Case Background](#61-case-background)
    - [6.2 Performance Metrics](#62-performance-metrics)
  - [7. Visualizations](#7-visualizations)
    - [7.1 Game Data Processing Architecture](#71-game-data-processing-architecture)
    - [7.2 Anti-Cheat Detection Flow](#72-anti-cheat-detection-flow)
  - [8. References](#8-references)

---

## 1. Definitions

### 1.1 Real-Time Battle System Definition

**Def-K-10-07-01** (Real-Time Battle Data Processing System, 实时对战数据处理系统): A real-time battle system is a septuple $\mathcal{G} = (M, P, E, S, C, A, \tau)$:

- $M$: Match set, $M = \{m_1, m_2, ..., m_n\}$
- $P$: Player set, each match $m$ has $k$ players
- $E$: Event stream, $E = \{e | e = (t, m, p, action, params)\}$
- $S$: Game state
- $C$: Computation logic
- $A$: Analysis output
- $\tau$: Latency upper bound (typically $\leq 50$ms)

### 1.2 Game Event Types

**Def-K-10-07-02** (Game Event Classification, 游戏事件分类):

| Event Type | Definition | Examples |
|-----------|------------|----------|
| **Movement Event** (移动事件) | Position state change | Hero movement, skill displacement |
| **Combat Event** (战斗事件) | Damage/healing occurrence | Attack, spell casting, being hit |
| **Interaction Event** (交互事件) | Interaction with environment | Buy equipment, use items |
| **State Event** (状态事件) | Game state change | Game start/end, victory/defeat |

### 1.3 Real-Time Levels

> 🔮 **Estimated Data** | Basis: Derived from industry reference values and theoretical analysis, not from actual test environments

**Def-K-10-07-03** (Latency Levels, 延迟等级): Game data processing is divided into:

| Level | Latency Requirement | Application Scenario |
|-------|--------------------|---------------------|
| Hard Real-Time (硬实时) | < 16ms | Game state synchronization |
| Soft Real-Time (软实时) | < 100ms | Battle replay, real-time spectating |
| Near Real-Time (近实时) | < 1s | Data statistics, leaderboard |

---

## 2. Properties

### 2.1 Event Order Consistency

**Lemma-K-10-07-01**: For the event sequence of the same match, causal consistency must be guaranteed:

$$
\forall e_i, e_j \in E_m: \quad e_i \rightarrow e_j \Rightarrow t_i < t_j
$$

### 2.2 Throughput Guarantee

**Lemma-K-10-07-02**: Let the event rate of a single match be $r$, the number of concurrent matches be $N$, then the total throughput is:

$$
Throughput = r \times N \times k
$$

where $k$ is the number of players per match.

**Thm-K-10-07-01**: For million-level concurrent matches, the system throughput must be $>$ 10 million events/second.

---

## 3. Relations

### 3.1 Data Processing Pipeline

```
Game Client ──► Game Server ──► Kafka ──► Flink ──► Analytics/Storage
                │                            │
                └────────► Real-time Sync ◄─────────┘
```

### 3.2 Analysis Types

> 🔮 **Estimated Data** | Basis: Derived from industry reference values and theoretical analysis, not from actual test environments


| Analysis Type | Latency Requirement | Technical Solution |
|--------------|--------------------|-------------------|
| Real-Time Battle Statistics (实时战斗统计) | < 1s | Flink Window Aggregation |
| Real-Time Leaderboard (实时排行榜) | < 5s | Redis + Flink |
| Battle Replay (战斗回放) | < 100ms | Event Stream Replay |
| Anti-Cheat Detection (反作弊检测) | < 1s | CEP Pattern Matching |

---

## 4. Argumentation

### 4.1 Necessity of Real-Time Processing

Special requirements for game data processing:

1. **State Synchronization Latency** (状态同步延迟): Affects player experience
2. **Real-Time Spectating** (实时观战): Requires low-latency data streams
3. **Real-Time Leaderboard** (实时排行榜): Motivates player competition
4. **Instant Feedback** (即时反馈): Real-time display of battle statistics

### 4.2 Technical Challenges

| Challenge | Description | Solution |
|-----------|-------------|----------|
| High Concurrency (高并发) | Million-level concurrent online users | Partitioned parallel processing |
| Out-of-Order Data (乱序数据) | Network latency variation | Event Time + Watermark |
| Large State (大状态) | Player session state | RocksDB + TTL |
| Fault Recovery (故障恢复) | No game data loss | Checkpoint |

---

## 5. Proof / Engineering Argument

### 5.1 Real-Time Battle Statistics

```java
/**
 * Real-Time Battle Statistics
 */

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.streaming.api.windowing.time.Time;

public class RealtimeBattleAnalytics {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.enableCheckpointing(10000);
        env.setParallelism(256);

        // 1. Game event stream
        DataStream<GameEvent> events = env
            .fromSource(createKafkaSource(),
                WatermarkStrategy.<GameEvent>forBoundedOutOfOrderness(Duration.ofMillis(100))
                    .withIdleness(Duration.ofSeconds(30)),
                "Game Events")
            .setParallelism(128);

        // 2. Real-time player statistics
        DataStream<PlayerStats> playerStats = events
            .keyBy(GameEvent::getPlayerId)
            .window(TumblingEventTimeWindows.of(Time.minutes(1)))
            .aggregate(new PlayerStatsAggregate())
            .name("Player Stats")
            .setParallelism(256);

        // 3. Match-level statistics
        DataStream<MatchStats> matchStats = events
            .keyBy(GameEvent::getMatchId)
            .window(TumblingEventTimeWindows.of(Time.minutes(5)))
            .aggregate(new MatchStatsAggregate())
            .name("Match Stats")
            .setParallelism(256);

        // 4. Real-time leaderboard
        DataStream<LeaderboardEntry> leaderboard = playerStats
            .windowAll(TumblingProcessingTimeWindows.of(Time.seconds(10)))
            .process(new LeaderboardCalculator(100))
            .name("Leaderboard")
            .setParallelism(1);

        // 5. Output
        playerStats.addSink(new RedisSink<>("player_stats"));
        matchStats.addSink(new ClickHouseSink<>("match_stats"));
        leaderboard.addSink(new RedisSink<>("leaderboard"));

        env.execute("Realtime Battle Analytics");
    }
}

/**
 * Player statistics aggregation
 */
class PlayerStatsAggregate implements AggregateFunction<GameEvent, PlayerAccumulator, PlayerStats> {

    @Override
    public PlayerAccumulator createAccumulator() {
        return new PlayerAccumulator();
    }

    @Override
    public PlayerAccumulator add(GameEvent event, PlayerAccumulator acc) {
        acc.playerId = event.getPlayerId();
        acc.matchId = event.getMatchId();

        switch (event.getEventType()) {
            case "DAMAGE_DEALT" -> {
                acc.totalDamage += event.getIntParam("amount");
                acc.damageEvents++;
            }
            case "KILL" -> acc.kills++;
            case "DEATH" -> acc.deaths++;
            case "ASSIST" -> acc.assists++;
            case "HEAL" -> acc.totalHeal += event.getIntParam("amount");
        }

        return acc;
    }

    @Override
    public PlayerStats getResult(PlayerAccumulator acc) {
        return PlayerStats.builder()
            .playerId(acc.playerId)
            .matchId(acc.matchId)
            .kills(acc.kills)
            .deaths(acc.deaths)
            .assists(acc.assists)
            .kda(calculateKDA(acc.kills, acc.deaths, acc.assists))
            .totalDamage(acc.totalDamage)
            .avgDamagePerHit(acc.damageEvents > 0 ? acc.totalDamage / acc.damageEvents : 0)
            .build();
    }

    @Override
    public PlayerAccumulator merge(PlayerAccumulator a, PlayerAccumulator b) {
        a.kills += b.kills;
        a.deaths += b.deaths;
        a.assists += b.assists;
        a.totalDamage += b.totalDamage;
        a.totalHeal += b.totalHeal;
        a.damageEvents += b.damageEvents;
        return a;
    }

    private double calculateKDA(int k, int d, int a) {
        return d == 0 ? (k + a) : (double) (k + a) / d;
    }
}
```

### 5.2 Anti-Cheat Detection

```java
/**
 * Game anti-cheat detection (CEP)
 */

import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.streaming.api.windowing.time.Time;

public class AntiCheatDetection {

    public static DataStream<CheatAlert> detectAimbot(DataStream<GameEvent> events) {
        // Pattern: Multiple headshots in short time
        Pattern<GameEvent, ?> aimbotPattern = Pattern
            .<GameEvent>begin("headshot1")
            .where(evt -> "HEADSHOT_KILL".equals(evt.getEventType()))
            .next("headshot2")
            .where(evt -> "HEADSHOT_KILL".equals(evt.getEventType()))
            .next("headshot3")
            .where(evt -> "HEADSHOT_KILL".equals(evt.getEventType()))
            .next("headshot4")
            .where(evt -> "HEADSHOT_KILL".equals(evt.getEventType()))
            .next("headshot5")
            .where(evt -> "HEADSHOT_KILL".equals(evt.getEventType()))
            .within(Time.seconds(10));

        return CEP.pattern(events.keyBy(GameEvent::getPlayerId), aimbotPattern)
            .process(new PatternProcessFunction<GameEvent, CheatAlert>() {
                @Override
                public void processMatch(Map<String, List<GameEvent>> match,
                                        Context ctx, Collector<CheatAlert> out) {
                    String playerId = match.get("headshot1").get(0).getPlayerId();
                    long timeSpan = match.get("headshot5").get(0).getTimestamp()
                                  - match.get("headshot1").get(0).getTimestamp();

                    if (timeSpan < 5000) {  // 5 headshots within 5 seconds
                        out.collect(new CheatAlert(
                            playerId,
                            "AIMBOT_SUSPECTED",
                            "5 headshots in " + timeSpan + "ms",
                            ctx.timestamp()
                        ));
                    }
                }
            });
    }

    public static DataStream<CheatAlert> detectSpeedHack(DataStream<GameEvent> events) {
        // Pattern: Abnormal movement speed
        return events
            .keyBy(GameEvent::getPlayerId)
            .process(new SpeedCheckFunction());
    }
}

/**
 * Speed detection function
 */
class SpeedCheckFunction extends KeyedProcessFunction<String, GameEvent, CheatAlert> {

    private ValueState<PositionState> lastPositionState;
    private static final double MAX_SPEED = 500.0;  // Maximum reasonable speed units/s

    @Override
    public void open(Configuration parameters) {
        lastPositionState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("last_position", PositionState.class));
    }

    @Override
    public void processElement(GameEvent event, Context ctx, Collector<CheatAlert> out)
            throws Exception {
        if (!"MOVE".equals(event.getEventType())) return;

        PositionState last = lastPositionState.value();
        PositionState current = new PositionState(
            event.getTimestamp(),
            event.getFloatParam("x"),
            event.getFloatParam("y"),
            event.getFloatParam("z")
        );

        if (last != null) {
            double distance = calculateDistance(last, current);
            double timeDelta = (current.timestamp - last.timestamp) / 1000.0;
            double speed = distance / timeDelta;

            if (speed > MAX_SPEED * 2) {  // Exceeds 2x maximum speed
                out.collect(new CheatAlert(
                    event.getPlayerId(),
                    "SPEED_HACK",
                    String.format("Speed: %.2f (max: %.2f)", speed, MAX_SPEED),
                    ctx.timestamp()
                ));
            }
        }

        lastPositionState.update(current);
    }

    private double calculateDistance(PositionState a, PositionState b) {
        return Math.sqrt(
            Math.pow(a.x - b.x, 2) +
            Math.pow(a.y - b.y, 2) +
            Math.pow(a.z - b.z, 2)
        );
    }
}
```

---

## 6. Examples

### 6.1 Case Background

> 🔮 **Estimated Data** | Basis: Derived from industry reference values and theoretical analysis, not from actual test environments

**Game**: A MOBA (Multiplayer Online Battle Arena, MOBA竞技手游) competitive mobile game

| Metric | Value |
|--------|-------|
| DAU (Daily Active Users, 日活跃用户) | 50 million |
| Daily Matches (日均对局) | 30 million |
| Concurrent Online Matches (同时在线对局) | 2 million |
| Event Peak (事件峰值) | 50 million/second |

**Challenges**:

1. Large volume of real-time battle data
2. Anti-cheat detection requires low latency
3. Real-time leaderboard updates
4. Battle replay storage

### 6.2 Performance Metrics

> 🔮 **Estimated Data** | Basis: Design target values; actual achievement may vary depending on environment


| Metric | Target | Actual |
|--------|--------|--------|
| Statistics Latency (P99) (统计延迟) | < 1s | 0.5s |
| Leaderboard Update (排行榜更新) | < 5s | 3s |
| Anti-Cheat Detection (反作弊检测) | < 5s | 2s |
| Event Processing Throughput (事件处理吞吐) | 50 million/s | 80 million/s |
| Data Completeness (数据完整性) | 100% | 100% |

---

## 7. Visualizations

### 7.1 Game Data Processing Architecture

The following diagram illustrates the overall architecture of the game data processing system, covering data ingestion from game servers, real-time processing via Flink, and multi-tier storage.

```mermaid
graph TB
    subgraph "Game Server Cluster"
        GS1[Game Server-1]
        GS2[Game Server-2]
        GS3[Game Server-N]
    end

    subgraph "Data Ingestion"
        KAFKA[Kafka<br/>game-events topic]
    end

    subgraph "Flink Real-Time Processing"
        STATS[Real-Time Statistics<br/>Window Aggregation]
        LB[Leaderboard Calculation<br/>Top-N]
        CHEAT[Anti-Cheat Detection<br/>CEP]
        REPLAY[Battle Replay<br/>Event Storage]
    end

    subgraph "Storage"
        REDIS[(Redis<br/>Real-Time Data)]
        CH[(ClickHouse<br/>Historical Analytics)]
        S3[(S3<br/>Replay Files)]
    end

    subgraph "Applications"
        DASH[Real-Time Dashboard]
        RANK[In-Game Leaderboard]
        AC[Anti-Cheat System]
    end

    GS1 & GS2 & GS3 --> KAFKA
    KAFKA --> STATS & LB & CHEAT & REPLAY
    STATS --> REDIS & CH
    LB --> REDIS
    CHEAT --> AC
    REPLAY --> S3
    REDIS --> DASH & RANK

    style CHEAT fill:#ffcdd2,stroke:#c62828
    style LB fill:#c8e6c9,stroke:#2e7d32
    style KAFKA fill:#bbdefb,stroke:#1565c0
```

### 7.2 Anti-Cheat Detection Flow

The following diagram shows the anti-cheat detection workflow, including event type classification, multi-dimensional cheat pattern matching, and manual review processing.

```mermaid
graph TD
    A[Game Event] --> B{Event Type}
    B -->|Move| C[Speed Check]
    B -->|Kill| D[Headshot Rate Check]
    B -->|Damage| E[Damage Anomaly Check]

    C -->|Speed > Threshold| F[Speed Cheat Alert]
    D -->|Headshot Rate > Threshold| G[Aim Assist Alert]
    E -->|Damage > Threshold| H[Damage Cheat Alert]

    F & G & H --> I[Anti-Cheat Queue]
    I --> J[Manual Review]
    J -->|Confirmed| K[Ban Processing]
    J -->|False Positive| L[Clear]

    style F fill:#ffcdd2,stroke:#c62828
    style G fill:#ffcdd2,stroke:#c62828
    style H fill:#ffcdd2,stroke:#c62828
    style K fill:#ffcdd2,stroke:#c62828
```

---

## 8. References


---

*Document Version: v1.0 | Last Updated: 2026-04-04*

---

*Document Version: v1.0 | Created Date: 2026-04-20*
