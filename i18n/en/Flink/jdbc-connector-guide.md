---
title: "[EN] Jdbc Connector Guide"
translation_status: "ai_translated"
source_file: "Flink/jdbc-connector-guide.md"
source_version: "c0f38e72"
translator: "AI"
reviewer: null
translated_at: "2026-04-08T15:15:06.359760"
reviewed_at: null
quality_score: null
terminology_verified: false
---


<!-- AI Translation Template - Replace <!-- TRANSLATE --> markers with actual translation -->

<!-- TRANSLATE: # JDBC Connector 详细指南 -->

<!-- TRANSLATE: > 所属阶段: Flink | 前置依赖: [data-types-complete-reference.md](./data-types-complete-reference.md) | 形式化等级: L4 -->


<!-- TRANSLATE: ## 2. 属性推导 (Properties) -->

<!-- TRANSLATE: ### Lemma-F-JDBC-01: 批量写入吞吐量边界 -->

<!-- TRANSLATE: **引理**: JDBC Sink 的最大吞吐量受以下因素约束： -->

$$
<!-- TRANSLATE: T_{max} = \min\left( \frac{B_{size}}{B_{interval}}, \frac{C_{pool} \times R_{db}}{L_{network}} \right) -->
$$

<!-- TRANSLATE: 其中： -->

- $B_{size}$: 批量大小
- $B_{interval}$: 批量间隔
- $C_{pool}$: 连接池大小
- $R_{db}$: 数据库写入速率
- $L_{network}$: 网络延迟

<!-- TRANSLATE: ### Lemma-F-JDBC-02: 连接池无死锁 -->

**引理**: 当 $N_{max} \geq P_{parallelism}$ 时，连接池不会发生死锁。

<!-- TRANSLATE: **证明**： -->

<!-- TRANSLATE: 1. 每个并行子任务最多需要一个连接 -->
1. 最大并发需求 = 并行度 $P$
2. 若 $N_{max} \geq P$，则总有可用连接
<!-- TRANSLATE: 4. 无循环等待，满足死锁避免条件 -->

<!-- TRANSLATE: ### Prop-F-JDBC-01: 幂等写入条件 -->

<!-- TRANSLATE: **命题**: 在以下条件下，JDBC Sink 可实现 Exactly-Once 语义： -->

<!-- TRANSLATE: 1. **主键存在**: 目标表有唯一主键约束 -->
<!-- TRANSLATE: 2. **幂等语句**: 使用 UPSERT/REPLACE 语义 -->
<!-- TRANSLATE: 3. **事务支持**: 数据库支持 XA 事务（可选） -->


<!-- TRANSLATE: ## 4. 论证过程 (Argumentation) -->

<!-- TRANSLATE: ### 4.1 分区读取策略选择 -->

<!-- TRANSLATE: **策略对比**： -->

<!-- TRANSLATE: | 策略 | 优点 | 缺点 | 适用场景 | -->
<!-- TRANSLATE: |------|------|------|----------| -->
<!-- TRANSLATE: | 主键范围 | 均匀分布，无数据倾斜 | 要求主键是数值/可排序 | 大表全量读取 | -->
<!-- TRANSLATE: | 分区列 | 利用数据库分区 | 需要预定义分区列 | 已分区表 | -->
<!-- TRANSLATE: | 无分区 | 简单，无需额外配置 | 单线程，性能受限 | 小表读取 | -->

<!-- TRANSLATE: ### 4.2 XA 事务 vs 幂等写入 -->

<!-- TRANSLATE: | 特性 | XA 事务 | 幂等写入 | -->
<!-- TRANSLATE: |------|---------|----------| -->
<!-- TRANSLATE: | 一致性 | 强一致性 | 最终一致性 | -->
<!-- TRANSLATE: | 性能 | 较低（两阶段提交） | 较高 | -->
<!-- TRANSLATE: | 数据库要求 | 需支持 XA | 需支持 UPSERT | -->
<!-- TRANSLATE: | 复杂度 | 高 | 低 | -->
<!-- TRANSLATE: | 推荐场景 | 金融交易 | 日志同步 | -->


<!-- TRANSLATE: ## 6. 实例验证 (Examples) -->

<!-- TRANSLATE: ### 6.1 Maven 依赖 -->

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-jdbc</artifactId>
    <version>3.1.2-1.17</version>
</dependency>

<!-- MySQL 驱动 -->
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.33</version>
</dependency>

<!-- PostgreSQL 驱动 -->
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <version>42.6.0</version>
</dependency>
```

<!-- TRANSLATE: ### 6.2 DataStream API 示例 -->

```java
import org.apache.flink.connector.jdbc.JdbcConnectionOptions;
import org.apache.flink.connector.jdbc.JdbcExecutionOptions;
import org.apache.flink.connector.jdbc.JdbcSink;
import org.apache.flink.connector.jdbc.JdbcStatementBuilder;

import org.apache.flink.streaming.api.datastream.DataStream;


// JDBC Sink 配置
DataStream<Order> orderStream = ...;

orderStream.addSink(JdbcSink.sink(
    "INSERT INTO orders (id, user_id, amount, create_time) VALUES (?, ?, ?, ?) " +
    "ON CONFLICT (id) DO UPDATE SET amount = EXCLUDED.amount",
    (JdbcStatementBuilder<Order>) (ps, order) -> {
        ps.setLong(1, order.getId());
        ps.setLong(2, order.getUserId());
        ps.setBigDecimal(3, order.getAmount());
        ps.setTimestamp(4, Timestamp.from(order.getCreateTime()));
    },
    JdbcExecutionOptions.builder()
        .withBatchSize(1000)
        .withBatchIntervalMs(200)
        .withMaxRetries(3)
        .build(),
    new JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
        .withUrl("jdbc:postgresql://localhost:5432/mydb")
        .withDriverName("org.postgresql.Driver")
        .withUsername("user")
        .withPassword("password")
        .build()
));
```

<!-- TRANSLATE: ### 6.3 Table API / SQL 示例 -->

```sql
-- 创建 JDBC 表
CREATE TABLE products (
    id BIGINT PRIMARY KEY,
    name STRING,
    price DECIMAL(10, 2),
    update_time TIMESTAMP
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:mysql://localhost:3306/mydb',
    'table-name' = 'products',
    'username' = 'user',
    'password' = 'password',
    'driver' = 'com.mysql.cj.jdbc.Driver',
    -- 批量配置
    'sink.buffer-flush.max-rows' = '1000',
    'sink.buffer-flush.interval' = '1s',
    'sink.max-retries' = '3'
);

-- 从 Kafka 读取并写入 JDBC
INSERT INTO products
SELECT
    id,
    name,
    price,
    CURRENT_TIMESTAMP AS update_time
FROM kafka_source;
```

<!-- TRANSLATE: ### 6.4 JDBC Source 示例 -->

```java
import org.apache.flink.connector.jdbc.JdbcInputFormat;
import org.apache.flink.api.common.typeinfo.BasicTypeInfo;
import org.apache.flink.api.java.DataSet;
import org.apache.flink.api.java.ExecutionEnvironment;

DataSet<Row> dbData = env.createInput(
    JdbcInputFormat.buildJdbcInputFormat()
        .setDrivername("com.mysql.cj.jdbc.Driver")
        .setDBUrl("jdbc:mysql://localhost/mydb")
        .setUsername("user")
        .setPassword("password")
        .setQuery("SELECT id, name, price FROM products WHERE price > ?")
        .setRowTypeInfo(new RowTypeInfo(
            BasicTypeInfo.LONG_TYPE_INFO,
            BasicTypeInfo.STRING_TYPE_INFO,
            BasicTypeInfo.BIG_DEC_TYPE_INFO
        ))
        .setParametersProvider(new Serializable[][]{
            new Serializable[]{new BigDecimal("100.00")}
        })
        .finish()
);
```


<!-- TRANSLATE: ## 8. 引用参考 (References) -->
