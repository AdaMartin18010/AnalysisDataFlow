# Finance Industry Case Study: Transaction Monitoring and Compliance System (交易监控与合规系统)

> **Stage**: Knowledge/10-case-studies/finance | **Prerequisites**: [./pattern-windowed-aggregation.md](./pattern-windowed-aggregation.md) | **Formalization Level**: L4

---

> **Case Nature**: 🔬 Proof-of-Concept Architecture | **Validation Status**: Based on theoretical derivation and architectural design; not independently validated by third-party production environments.
>
> This case study describes an ideal architecture derived from the project's theoretical framework, including hypothetical performance metrics and theoretical cost models.
> Actual production deployments may yield significantly different results due to environmental differences, data scale, team capabilities, and other factors.
> It is recommended to use this as an architectural design reference rather than a direct copy-paste production blueprint.

## Table of Contents

- [Finance Industry Case Study: Transaction Monitoring and Compliance System (交易监控与合规系统)](#finance-industry-case-study-transaction-monitoring-and-compliance-system-交易监控与合规系统)
  - [Table of Contents](#table-of-contents)
  - [1. Definitions](#1-definitions)
    - [1.1 Transaction Monitoring System Definition](#11-transaction-monitoring-system-definition)
    - [1.2 Suspicious Transaction Types](#12-suspicious-transaction-types)
    - [1.3 Regulatory Time Constraints](#13-regulatory-time-constraints)
  - [2. Properties](#2-properties)
    - [2.1 Data Integrity Guarantee](#21-data-integrity-guarantee)
    - [2.2 Latency Bound Guarantee](#22-latency-bound-guarantee)
  - [3. Relations](#3-relations)
    - [3.1 Relationship with Regulatory Systems](#31-relationship-with-regulatory-systems)
    - [3.2 Relationship with Data Lake](#32-relationship-with-data-lake)
  - [4. Argumentation](#4-argumentation)
    - [4.1 Real-Time vs. Batch Processing Compliance](#41-real-time-vs-batch-processing-compliance)
    - [4.2 Technology Selection](#42-technology-selection)
  - [5. Formal Proof / Engineering Argument](#5-formal-proof--engineering-argument)
    - [5.1 Layered Processing Architecture](#51-layered-processing-architecture)
    - [5.2 Large-State Window Management](#52-large-state-window-management)
  - [6. Examples](#6-examples)
    - [6.1 Case Background](#61-case-background)
    - [6.2 Flink SQL Implementation](#62-flink-sql-implementation)
    - [6.3 Wash Trade Detection Java Code](#63-wash-trade-detection-java-code)
    - [6.4 Performance Metrics](#64-performance-metrics)
  - [7. Visualizations](#7-visualizations)
    - [7.1 System Architecture Diagram](#71-system-architecture-diagram)
    - [7.2 Wash Trade Detection Flow](#72-wash-trade-detection-flow)
  - [8. References](#8-references)

---

## 1. Definitions

### 1.1 Transaction Monitoring System Definition

**Def-K-10-02-01** (Transaction Monitoring System / 交易监控系统): A transaction monitoring system is a sextuple $\mathcal{T} = (E, R, W, \mathcal{A}, \mathcal{O}, \tau)$, where:

- $E$: Trade event stream, $E = \{e_1, e_2, ..., e_n\}$
- $R$: Regulatory rule set, $R = \{r_1, r_2, ..., r_m\}$
- $W$: Time window set, $W = \{w_1, w_2, ..., w_k\}$
- $\mathcal{A}$: Alert action set
- $\mathcal{O}$: Report output format
- $\tau$: Compliance latency upper bound (regulatory requirement, typically $\leq 5$ minutes)

### 1.2 Suspicious Transaction Types

**Def-K-10-02-02** (Suspicious Transaction Classification / 可疑交易分类): According to regulatory requirements, suspicious transactions are classified as:

| Type | Definition | Regulatory Basis |
|------|------------|------------------|
| **Large-Value Transaction** | Single transaction or daily cumulative amount exceeding threshold | Anti-Money Laundering (AML) Law (反洗钱法) |
| **Anomalous Pattern** | Significant deviation from customer's historical behavior | Suspicious Transaction Reporting (STR) System (可疑交易报告制度) |
| **Structuring Transaction** | Deliberate splitting to evade regulatory thresholds | Large Transaction Reporting System (大额交易报告制度) |
| **Cross-Border Anomaly** | Involving high-risk countries/regions | FATF Recommendations (FATF建议) |

### 1.3 Regulatory Time Constraints

**Def-K-10-02-03** (Regulatory Time Window / 监管时间窗口): Let $t_{detect}$ be the suspicious transaction detection time and $t_{report}$ be the reporting time, then:

$$
t_{report} - t_{detect} \leq T_{regulatory}
$$

where $T_{regulatory} = 5$ minutes (China Securities Regulatory Commission (CSRC / 中国证监会) requirement).

---

## 2. Properties

### 2.1 Data Integrity Guarantee

**Lemma-K-10-02-01** (Exactly-Once Guarantee): The transaction monitoring system uses a two-phase commit (2PC / 两阶段提交) Sink to ensure:

$$
\forall e \in E: \quad count_{processed}(e) = 1
$$

**Proof Sketch**:

1. Kafka source uses replayable offsets.
2. Flink checkpoint periodically snapshots state.
3. Sink uses two-phase commit protocol.
4. Upon failure recovery, restarts from checkpoint, guaranteeing no data loss and no duplicates.

### 2.2 Latency Bound Guarantee

**Lemma-K-10-02-02** (End-to-End Latency / 端到端延迟): The latency $L_{compliance}$ from trade occurrence to regulatory reporting is:

$$
L_{compliance} = L_{trading} + L_{settlement} + L_{processing} + L_{reporting}
$$

Typical values of each component:

- $L_{trading} \leq 1$s (trade execution / 交易执行)
- $L_{settlement} \leq 3$s (settlement confirmation / 清算确认)
- $L_{processing} \leq 30$s (Flink processing / Flink处理)
- $L_{reporting} \leq 10$s (report generation / 报告生成)

**Thm-K-10-02-01**: $L_{compliance} \leq 44$s $<$ 5 minutes (satisfies regulatory requirements).

---

## 3. Relations

### 3.1 Relationship with Regulatory Systems

```
Exchange Market Data ──► Flink Stream Processing ──► Anomaly Detection ──► Regulatory Reporting Platform
                              │                           │
                              ▼                           ▼
                        Data Lake Storage          Manual Review System
```

### 3.2 Relationship with Data Lake

| Data Flow | Purpose | Storage Format |
|-----------|---------|----------------|
| Real-time Stream → Data Lake | Historical backtracking, model training | Delta Lake |
| Data Lake → Real-time Stream | Historical feature lookup | External Table Lookup |
| Real-time Stream → Regulatory DB | Compliance reporting | Parquet |

---

## 4. Argumentation

### 4.1 Real-Time vs. Batch Processing Compliance

| Dimension | Real-Time Processing | Batch Processing |
|-----------|----------------------|------------------|
| Detection Latency | Second-level | Hour-level |
| Regulatory Compliance | Meets 5-minute requirement | Potential delayed reporting |
| Manual Review | Immediate trigger | Deferred review |
| Computation Cost | Higher | Lower |

### 4.2 Technology Selection

Reasons for choosing Apache Flink over Spark Streaming (Spark Streaming / Spark流处理):

1. **Lower Latency**: Second-level vs. minute-level.
2. **Window Semantics**: Event Time windows are more accurate.
3. **CEP Support**: Complex Event Processing (CEP / 复杂事件处理) for pattern matching.
4. **State Management**: Efficient handling of large-window state.

---

## 5. Formal Proof / Engineering Argument

### 5.1 Layered Processing Architecture

```
L0 Raw Layer: Kafka Raw Topic (retained for 7 days)
    │
    ▼
L1 Cleansing Layer: Flink ETL (data validation, standardization)
    │
    ▼
L2 Analytics Layer: Window Aggregation + CEP Pattern Matching
    │
    ▼
L3 Storage Layer: Iceberg (historical) + ClickHouse (querying) + Regulatory Reporting
```

### 5.2 Large-State Window Management

For 30-day sliding window aggregation:

- Number of windows: $30 \times 24 \times 12 = 8640$ (5-minute granularity)
- State per window: approximately 50KB
- Total state: approximately 400MB per partition

Optimization Strategies:

1. **Incremental Aggregation**: Store only incremental values, not raw data.
2. **State Partitioning**: Partition by stock code.
3. **TTL Cleanup**: Automatic expiration of 30-day windows.

---

## 6. Examples

### 6.1 Case Background

> 🔮 **Estimated Data** | Basis: Derived from industry reference values and theoretical analysis; not obtained from actual test environments.

**Institution**: A leading securities firm

| Metric | Value |
|--------|-------|
| Daily Average Transaction Volume | 10 million transactions |
| Market Coverage | Full market coverage of Shanghai-Shenzhen-Hong Kong Stock Connect (沪深港通全市场) |
| Regulatory Requirement | Report suspicious transactions within 5 minutes |
| Historical Data | 10+ years |

**Challenges**:

1. Data format differences between Shanghai and Shenzhen markets.
2. Complex and diverse anomalous transaction patterns.
3. Frequent regulatory rule updates.
4. Historical backtracking query performance requirements.

### 6.2 Flink SQL Implementation

```sql
-- Create trade table
CREATE TABLE stock_trades (
    trade_id STRING,
    stock_code STRING,
    user_id STRING,
    trade_type STRING,  -- 'BUY' or 'SELL'
    price DECIMAL(10,2),
    volume INT,
    trade_time TIMESTAMP(3),
    market STRING,      -- 'SH' or 'SZ'
    WATERMARK FOR trade_time AS trade_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'stock.trades',
    'properties.bootstrap.servers' = 'kafka:9092',
    'format' = 'json'
);

-- 1. Large-value trade monitoring (single transaction > 1M or daily cumulative > 5M)
CREATE TABLE large_trades_alert AS
SELECT
    user_id,
    stock_code,
    trade_type,
    price * volume as trade_amount,
    trade_time,
    'LARGE_TRADE' as alert_type
FROM stock_trades
WHERE price * volume > 1000000;

-- 2. Wash trade detection (same user, same stock, same price and volume, opposite direction)
CREATE TABLE wash_trades_alert AS
SELECT
    t1.user_id,
    t1.stock_code,
    t1.trade_time as first_time,
    t2.trade_time as second_time,
    t1.volume,
    t1.price,
    'WASH_TRADE' as alert_type
FROM stock_trades t1
JOIN stock_trades t2 ON t1.user_id = t2.user_id
    AND t1.stock_code = t2.stock_code
    AND t1.volume = t2.volume
    AND t1.price = t2.price
    AND t1.trade_type <> t2.trade_type
WHERE t2.trade_time BETWEEN t1.trade_time
    AND t1.trade_time + INTERVAL '1' MINUTE;

-- 3. Anomalous volatility monitoring (price fluctuation > 10% within 5 minutes)
CREATE TABLE price_volatility_alert AS
SELECT
    stock_code,
    window_start,
    window_end,
    MIN(price) as min_price,
    MAX(price) as max_price,
    (MAX(price) - MIN(price)) / MIN(price) as volatility,
    'PRICE_VOLATILITY' as alert_type
FROM TABLE(
    TUMBLE(TABLE stock_trades, DESCRIPTOR(trade_time), INTERVAL '5' MINUTE)
)
GROUP BY stock_code, window_start, window_end
HAVING (MAX(price) - MIN(price)) / MIN(price) > 0.1;

-- 4. Concentration monitoring (abnormal position ratio for single account and single stock)
CREATE TABLE concentration_alert AS
WITH user_stock_volume AS (
    SELECT
        user_id,
        stock_code,
        SUM(CASE WHEN trade_type = 'BUY' THEN volume ELSE -volume END)
            OVER (PARTITION BY user_id, stock_code
                  ORDER BY trade_time
                  RANGE BETWEEN INTERVAL '1' DAY PRECEDING AND CURRENT ROW)
            as net_position
    FROM stock_trades
)
SELECT
    user_id,
    stock_code,
    net_position,
    'HIGH_CONCENTRATION' as alert_type
FROM user_stock_volume
WHERE ABS(net_position) > 1000000;  -- Position exceeds 1 million shares
```

### 6.3 Wash Trade Detection Java Code

```java
/**
 * Wash Trade Detection - Using Interval Join
 */

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

public class WashTradeDetector {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        // Source
        DataStream<Trade> trades = env
            .fromSource(createKafkaSource(), createWatermarkStrategy(), "Trades")
            .setParallelism(64);

        // Wash trade detection: opposite trades within 1 minute, same price and volume
        DataStream<WashTradeAlert> washTrades = trades
            .keyBy(Trade::getUserId)
            .intervalJoin(trades.keyBy(Trade::getUserId))
            .between(Time.seconds(0), Time.minutes(1))
            .process(new WashTradeJoinFunction())
            .name("Wash Trade Detection")
            .setParallelism(128);

        // Output to regulatory platform
        washTrades.addSink(new RegulatoryReportSink())
            .name("Regulatory Sink");

        env.execute("Transaction Monitoring");
    }

    static class WashTradeJoinFunction extends ProcessJoinFunction<Trade, Trade, WashTradeAlert> {
        @Override
        public void processElement(Trade first, Trade second, Context ctx, Collector<WashTradeAlert> out) {
            // Check if it is an opposite trade
            if (!first.getTradeType().equals(second.getTradeType()) &&
                first.getStockCode().equals(second.getStockCode()) &&
                first.getPrice().equals(second.getPrice()) &&
                first.getVolume() == second.getVolume() &&
                !first.getTradeId().equals(second.getTradeId())) {

                out.collect(new WashTradeAlert(
                    first.getUserId(),
                    first.getStockCode(),
                    first.getTradeTime(),
                    second.getTradeTime(),
                    first.getPrice(),
                    first.getVolume(),
                    ctx.getLeftTimestamp()
                ));
            }
        }
    }
}
```

### 6.4 Performance Metrics
>
> 🔮 **Estimated Data** | Basis: Design target values; actual achievement may vary depending on environment.

| Metric | Target | Actual |
|--------|--------|--------|
| Processing Latency (P99) | < 30s | 18s |
| Daily Processing Volume | 10 million transactions | 12 million transactions |
| Suspicious Transaction Detection Rate | > 99% | 99.8% |
| Data Integrity | 100% | 100% |
| System Availability | 99.99% | 99.995% |

---

## 7. Visualizations

### 7.1 System Architecture Diagram

```mermaid
graph TB
    subgraph "Exchange Data Sources"
        SH[Shanghai Stock Exchange]
        SZ[Shenzhen Stock Exchange]
        HK[Hong Kong Stock Exchange]
    end

    subgraph "Data Ingestion Layer"
        KAFKA[Kafka Cluster<br/>Multi-Topic Partitioning]
        SCHEMA[Schema Registry<br/>Data Contract]
    end

    subgraph "Flink Processing Layer"
        ETL[Data Cleansing ETL]
        VALID[Data Validation]

        subgraph "Monitoring Rules"
            R1[Large-Value Trade Monitoring]
            R2[Wash Trade Detection]
            R3[Price Volatility Monitoring]
            R4[Concentration Monitoring]
        end

        AGG[Window Aggregation]
    end

    subgraph "Storage Layer"
        ICE[Iceberg<br/>Historical Data]
        CH[ClickHouse<br/>Real-Time Query]
        REG[Regulatory Reporting]
    end

    SH & SZ & HK --> KAFKA --> SCHEMA --> ETL --> VALID
    VALID --> R1 & R2 & R3 & R4 --> AGG
    AGG --> ICE & CH & REG

    style R2 fill:#ffcdd2,stroke:#c62828
    style KAFKA fill:#c8e6c9,stroke:#2e7d32
```

### 7.2 Wash Trade Detection Flow

```mermaid
sequenceDiagram
    participant T1 as Trade A (BUY)
    participant Flink as Flink Join
    participant T2 as Trade B (SELL)
    participant Alert as Alert System

    T1->>Flink: User=U1, Stock=000001<br/>Price=10.5, Volume=10000
    Note over Flink: 1-minute window wait

    T2->>Flink: User=U1, Stock=000001<br/>Price=10.5, Volume=10000

    Flink->>Flink: Matching condition check<br/>- Same user<br/>- Same stock<br/>- Same price and volume<br/>- Opposite direction

    Flink->>Alert: Generate wash trade alert<br/>Wash Trade Detected
    Alert->>Alert: Report to regulator within 5 minutes
```

---

## 8. References

*No external references are cited in this document. Readers may refer to the official Apache Flink documentation, relevant anti-money laundering (AML) regulatory guidelines, and securities exchange reporting requirements for additional context.*

---

*Document Version: v1.0 | Last Updated: 2026-04-04*

---

*Document Version: v1.0 | Created: 2026-04-20*
