---
title: "[EN] Flink Data Types Reference"
translation_status: "ai_translated"
source_file: "Flink/flink-data-types-reference.md"
source_version: "1d332d93"
translator: "AI"
reviewer: null
translated_at: "2026-04-08T15:15:06.350160"
reviewed_at: null
quality_score: null
terminology_verified: false
---


<!-- AI Translation Template - Replace <!-- TRANSLATE --> markers with actual translation -->

<!-- TRANSLATE: # Flink Data Types 完整参考 -->

<!-- TRANSLATE: > 所属阶段: Flink | 前置依赖: [Flink/00-QUICK-START.md](../../../Flink/00-meta/00-QUICK-START.md) | 形式化等级: L4 -->


<!-- TRANSLATE: ## 2. 属性推导 (Properties) -->

<!-- TRANSLATE: ### Lemma-F-01-01: 类型完备性 -->

<!-- TRANSLATE: **引理**: Flink SQL 类型系统对标准 SQL:2016 数据模型是类型完备的。 -->

<!-- TRANSLATE: **证明要点**: -->

<!-- TRANSLATE: 1. **原子类型覆盖**: 所有标准 SQL 原子类型均有对应实现 -->
<!-- TRANSLATE: 2. **复合类型封闭性**: ARRAY/MAP/ROW 支持递归嵌套，形成代数数据类型 -->
<!-- TRANSLATE: 3. **空值处理**: 所有类型均支持 NULL 值，满足三值逻辑 -->
<!-- TRANSLATE: 4. **时间扩展**: 在 SQL 标准基础上扩展 TIMESTAMP_LTZ 适应流计算 -->

<!-- TRANSLATE: ### Lemma-F-01-02: 类型转换单调性 -->

**引理**: 类型转换关系 $\prec$ 构成偏序集，满足传递性：

$$
<!-- TRANSLATE: \forall T_1, T_2, T_3 \in \mathcal{T}: T_1 \prec T_2 \land T_2 \prec T_3 \Rightarrow T_1 \prec T_3 -->
$$

<!-- TRANSLATE: **证明**: 由转换链的定义直接可得，每对相邻类型间的转换都是单射函数，复合仍为单射。 -->

<!-- TRANSLATE: ### Prop-F-01-01: 类型安全保证 -->

<!-- TRANSLATE: **命题**: 在编译期可检测所有类型不匹配错误。 -->

$$
<!-- TRANSLATE: \forall Q \in SQL: \text{TypeCheck}(Q) = \bot \Rightarrow \nexists E: \text{Execute}(Q, E) \neq \text{Error} -->
$$


<!-- TRANSLATE: ## 4. 论证过程 (Argumentation) -->

<!-- TRANSLATE: ### 4.1 DECIMAL vs FLOAT 选择决策 -->

<!-- TRANSLATE: **问题**: 为什么选择 DECIMAL 而非 FLOAT 作为精确数值计算类型？ -->

<!-- TRANSLATE: **论证**: -->

<!-- TRANSLATE: | 维度 | DECIMAL | FLOAT/DOUBLE | -->
<!-- TRANSLATE: |------|---------|--------------| -->
<!-- TRANSLATE: | 精度 | 精确表示，无舍入误差 | IEEE 754 近似表示 | -->
<!-- TRANSLATE: | 范围 | 有限（1~38位） | 极大（约10³⁰⁸） | -->
<!-- TRANSLATE: | 性能 | 较慢（软件实现） | 快（硬件加速） | -->
<!-- TRANSLATE: | 存储 | 变长，较大 | 固定 4/8 字节 | -->
<!-- TRANSLATE: | 适用 | 金融、货币计算 | 科学计算、近似分析 | -->

<!-- TRANSLATE: **决策**: 金融场景必须使用 DECIMAL(p,s)，推荐 DECIMAL(19,4) 满足大多数货币计算需求。 -->

<!-- TRANSLATE: ### 4.2 TIMESTAMP vs TIMESTAMP_LTZ 选择矩阵 -->

<!-- TRANSLATE: | 应用场景 | 推荐类型 | 理由 | -->
<!-- TRANSLATE: |----------|----------|------| -->
<!-- TRANSLATE: | 单时区应用 | `TIMESTAMP` | 简单直观，无时区概念负担 | -->
<!-- TRANSLATE: | 多时区应用 | `TIMESTAMP_LTZ` | 统一 UTC 存储，前端本地化显示 | -->
<!-- TRANSLATE: | 与 Kafka 集成 | `TIMESTAMP_LTZ` | Kafka 使用 UTC epoch millis | -->
<!-- TRANSLATE: | 审计日志 | `TIMESTAMP_LTZ` | 保证全球时间一致性 | -->
<!-- TRANSLATE: | 业务事件时间 | `TIMESTAMP` | 业务语义通常为本地时间 | -->


<!-- TRANSLATE: ## 6. 实例验证 (Examples) -->

<!-- TRANSLATE: ### 6.1 DDL 类型定义完整示例 -->

```sql
-- 创建包含完整类型系统的表
CREATE TABLE user_events (
    -- 原子类型 - 标识与状态
    user_id BIGINT NOT NULL,
    username VARCHAR(128) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    user_type CHAR(1) DEFAULT 'R',  -- R: Regular, V: VIP

    -- 数值类型 - 业务指标
    score DECIMAL(10, 4),           -- 精确分数
    temperature FLOAT,              -- 传感器读数（近似）

    -- 二进制类型
    avatar_hash VARBINARY(64),
    raw_payload BYTES,

    -- 时间类型 - 流计算核心
    birth_date DATE,
    preferred_time TIME(3),
    event_ts TIMESTAMP(3),          -- 事件时间（本地）
    event_ts_utc TIMESTAMP_LTZ(3),  -- 事件时间（UTC）

    -- 复合类型 - 结构化数据
    tags ARRAY<VARCHAR(50)>,
    properties MAP<STRING, STRING>,
    address ROW<
        street STRING,
        city STRING,
        country STRING DEFAULT 'CN',
        coordinates ROW<
            lat DOUBLE,
            lon DOUBLE
        >
    >,

    -- 元数据列
    proc_time AS PROCTIME(),

    -- 水位线定义
    WATERMARK FOR event_ts AS event_ts - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'user-events',
    'format' = 'json',
    'json.fail-on-missing-field' = 'false',
    'json.ignore-parse-errors' = 'true'
);
```

<!-- TRANSLATE: ### 6.2 类型转换示例 -->

```sql
-- 隐式转换（自动进行）
SELECT
    user_id + 1.5 AS user_id_double,           -- BIGINT → DOUBLE
    CONCAT('ID:', CAST(user_id AS STRING)) AS user_id_str
FROM user_events;

-- 显式转换（CAST）
SELECT
    CAST(event_ts AS DATE) AS event_date,
    CAST(event_ts AS STRING) AS ts_string,
    CAST(score AS INT) AS score_int,           -- 截断小数
    CAST(score AS BIGINT) AS score_bigint
FROM user_events;

-- 安全转换（TRY_CAST）
SELECT
    TRY_CAST(username AS INT) AS username_num, -- 失败返回 NULL
    TRY_CAST('2024-01-15' AS DATE) AS valid_date,
    TRY_CAST('invalid' AS DATE) AS null_date   -- 返回 NULL
FROM user_events;
```

<!-- TRANSLATE: ### 6.3 Java API 类型编程 -->

```java
import org.apache.flink.table.api.DataTypes;
import org.apache.flink.table.api.Schema;
import org.apache.flink.table.api.Table;
import org.apache.flink.table.api.TableDescriptor;

import org.apache.flink.api.common.typeinfo.Types;


public class DataTypeExample {

    // 编程方式定义 Schema
    public Schema createUserSchema() {
        return Schema.newBuilder()
            .column("user_id", DataTypes.BIGINT().notNull())
            .column("username", DataTypes.VARCHAR(128))
            .column("is_active", DataTypes.BOOLEAN().defaultValue(true))
            .column("score", DataTypes.DECIMAL(10, 4))
            .column("tags", DataTypes.ARRAY(DataTypes.VARCHAR(50)))
            .column("properties", DataTypes.MAP(
                DataTypes.STRING(),
                DataTypes.STRING()
            ))
            .column("address", DataTypes.ROW(
                DataTypes.FIELD("street", DataTypes.STRING()),
                DataTypes.FIELD("city", DataTypes.STRING()),
                DataTypes.FIELD("zipcode", DataTypes.CHAR(6))
            ))
            .column("event_ts", DataTypes.TIMESTAMP(3))
            .columnByExpression("proc_time", "PROCTIME()")
            .watermark("event_ts", "SOURCE_WATERMARK()")
            .build();
    }

    // 使用 TableDescriptor 定义
    public TableDescriptor createKafkaDescriptor() {
        return TableDescriptor.forConnector("kafka")
            .schema(createUserSchema())
            .option("topic", "user-events")
            .option("properties.bootstrap.servers", "localhost:9092")
            .format("json")
            .build();
    }
}
```

<!-- TRANSLATE: ### 6.4 Python Table API 类型使用 -->

```python
from pyflink.table import DataTypes, Schema, TableDescriptor
from pyflink.table.table_environment import StreamTableEnvironment

# 定义 Schema
schema = Schema.new_builder() \
    .column("user_id", DataTypes.BIGINT().not_null()) \
    .column("username", DataTypes.STRING()) \
    .column("score", DataTypes.DECIMAL(10, 4)) \
    .column("tags", DataTypes.ARRAY(DataTypes.STRING())) \
    .column("metadata", DataTypes.MAP(
        DataTypes.STRING(),
        DataTypes.STRING()
    )) \
    .column("event_time", DataTypes.TIMESTAMP(3)) \
    .column_by_expression("proc_time", "PROCTIME()") \
    .watermark("event_time", "SOURCE_WATERMARK()") \
    .build()

# 创建表
descriptor = TableDescriptor.for_connector("kafka") \
    .schema(schema) \
    .option("topic", "events") \
    .option("properties.bootstrap.servers", "kafka:9092") \
    .format("json") \
    .build()
```


<!-- TRANSLATE: ## 8. 引用参考 (References) -->
