# JDBC连接器演进 特性跟踪

> 所属阶段: Flink/connectors/evolution | 前置依赖: [JDBC Connector][^1] | 形式化等级: L3

## 1. 概念定义 (Definitions)

### Def-F-Conn-JDBC-01: JDBC Source

JDBC Source：
$$
\text{JDBCSource} : \text{SQL} \to \text{Stream}
$$

### Def-F-Conn-JDBC-02: JDBC Sink

JDBC Sink：
$$
\text{JDBCSink} : \text{Stream} \xrightarrow{\text{batch}} \text{Database}
$$

## 2. 属性推导 (Properties)

### Prop-F-Conn-JDBC-01: Batch Optimization

批量优化：
$$
\text{Throughput} \propto \text{BatchSize}
$$

## 3. 关系建立 (Relations)

### JDBC演进

| 版本 | 特性 | 状态 |
|------|------|------|
| 2.3 | 基础JDBC | GA |
| 2.4 | 分片读取 | GA |
| 2.5 | 异步写入 | GA |
| 3.0 | 连接池优化 | 设计中 |

## 4. 论证过程 (Argumentation)

### 4.1 数据库支持

| 数据库 | Source | Sink |
|--------|--------|------|
| MySQL | ✅ | ✅ |
| PostgreSQL | ✅ | ✅ |
| Oracle | ✅ | ✅ |
| SQL Server | ✅ | ✅ |

## 5. 形式证明 / 工程论证

### 5.1 JDBC Source

```java
// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
JdbcSourceBuilder<Row> builder = JdbcSourceBuilder.<Row>builder()
    .setDriverName("com.mysql.cj.jdbc.Driver")
    .setUrl("jdbc:mysql://localhost:3306/mydb")
    .setQuery("SELECT * FROM orders WHERE order_time > ?")
    .setResultConverter(rowConverter);
```

## 6. 实例验证 (Examples)

### 6.1 JDBC Sink

```java
// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
JdbcSink.sink(
    "INSERT INTO orders (id, amount) VALUES (?, ?)",
    (ps, order) -> {
        ps.setString(1, order.getId());
        ps.setDouble(2, order.getAmount());
    },
    JdbcExecutionOptions.builder()
        .withBatchSize(1000)
        .withBatchIntervalMs(200)
        .build(),
    new JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
        .withUrl("jdbc:mysql://localhost:3306/mydb")
        .build()
);
```

## 7. 可视化 (Visualizations)

### 7.1 JDBC连接器数据流概览

```mermaid
graph LR
    A[Database] --> B[JDBC Source]
    B --> C[Flink处理]
    C --> D[JDBC Sink]
    D --> E[Database]
```

### 7.2 JDBC连接器演进思维导图

以下思维导图以"JDBC连接器演进"为中心，从 Source 演进、Sink 演进、Lookup Join、连接管理、数据库适配五个维度放射展开。

```mermaid
mindmap
  root((JDBC连接器演进))
    Source演进
      简单查询
      分区读取
      并行Source
      增量读取
    Sink演进
      逐条插入
      批量插入
      Upsert
      两阶段提交
    Lookup Join
      同步查询
      异步查询
      缓存优化
      超时控制
    连接管理
      连接池
      超时配置
      重试策略
      故障恢复
    数据库适配
      MySQL
      PostgreSQL
      Oracle
      SQL Server
      TiDB
```

### 7.3 JDBC操作-配置参数-性能影响多维关联树

以下关联树展示 JDBC 操作 → 关键配置参数 → 性能影响之间的映射关系。

```mermaid
graph TB
    subgraph JDBC操作
        O1[Source读取]
        O2[Sink写入]
        O3[Lookup查询]
        O4[连接建立]
    end

    subgraph 配置参数
        P1[scan.partition.column<br/>scan.partition.num]
        P2[sink.buffer-flush.max-rows<br/>sink.buffer-flush.interval]
        P3[lookup.cache.max-rows<br/>lookup.cache.ttl]
        P4[connection.max-retry-timeout<br/>connection.check-timeout-seconds]
        P5[driverClassName<br/>url]
    end

    subgraph 性能影响
        I1[读取并行度↑
吞吐量↑]
        I2[写入延迟↓
吞吐量↑]
        I3[查询延迟↓
数据库压力↓]
        I4[连接稳定性↑
故障恢复时间↓]
        I5[兼容性
驱动版本差异]
    end

    O1 --> P1
    O2 --> P2
    O3 --> P3
    O4 --> P4
    O4 --> P5

    P1 --> I1
    P2 --> I2
    P3 --> I3
    P4 --> I4
    P5 --> I5
```

### 7.4 JDBC连接器选型决策树

以下决策树指导在不同场景下选择合适的 JDBC 连接器模式与配套方案。

```mermaid
flowchart TD
    Start([开始选型]) --> Q1{数据流向?}

    Q1 -->|批量写入| A1[JDBC Sink]
    A1 --> A1a[配置批大小调优
sink.buffer-flush.max-rows]
    A1 --> A1b[配置批刷新间隔
sink.buffer-flush.interval]

    Q1 -->|实时Upsert| A2[JDBC Upsert Sink]
    A2 --> A2a[配置主键冲突处理策略
sink.semantic = upsert]
    A2 --> A2b[开启幂等写入
确保at-least-once语义]

    Q1 -->|维表Join| A3[JDBC Lookup Join]
    A3 --> A3a[开启缓存优化
lookup.cache.max-rows / ttl]
    A3 --> A3b[启用异步查询
lookup.async = true]
    A3 --> A3c[配置超时控制
lookup.max-retries / retry-interval]

    Q1 -->|CDC同步| A4[Change Data Capture]
    A4 --> A4a[Debezium采集变更]
    A4a --> A4b[Kafka持久化变更流]
    A4b --> A4c[Flink消费处理]
    A4c --> A4d[JDBC Sink写入目标库]

    style Start fill:#e1f5fe
    style A1 fill:#fff3e0
    style A2 fill:#fff3e0
    style A3 fill:#fff3e0
    style A4 fill:#fff3e0
```

## 8. 引用参考 (References)

[^1]: Flink JDBC Connector Documentation
[^2]: Apache Flink Documentation, "JDBC Connector", 2025. https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/table/jdbc/
[^3]: MySQL Connector/J Documentation, "Batch Insert and Connection Properties", 2025. https://dev.mysql.com/doc/connector-j/en/connector-j-reference-configuration-properties.html
[^4]: PostgreSQL JDBC Driver Documentation, "ReWriteBatchedInserts Optimization", 2025. https://jdbc.postgresql.org/documentation/use/
[^5]: TiDB Documentation, "Flink TiDB Connector", 2025. https://docs.pingcap.com/tidb/stable/dev-guide-sample-application-java-flink

---

## 跟踪信息

| 属性 | 值 |
|------|-----|
| 版本 | 2.4-3.0 |
| 当前状态 | 演进中 |

---

*文档版本: v1.0 | 创建日期: 2026-04-19*
