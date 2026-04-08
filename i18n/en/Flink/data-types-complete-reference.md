---
title: "[EN] Data Types Complete Reference"
translation_status: "ai_translated"
source_file: "Flink/data-types-complete-reference.md"
source_version: "a8a1148c"
translator: "AI"
reviewer: null
translated_at: "2026-04-08T15:15:06.344124"
reviewed_at: null
quality_score: null
terminology_verified: false
---


<!-- AI Translation Template - Replace <!-- TRANSLATE --> markers with actual translation -->

<!-- TRANSLATE: # Flink Data Types 完整参考 -->

<!-- TRANSLATE: > 所属阶段: Flink | 前置依赖: [Flink/00-QUICK-START.md](00-meta/00-QUICK-START.md) | 形式化等级: L4 -->


<!-- TRANSLATE: ## 2. 属性推导 (Properties) -->

<!-- TRANSLATE: ### Lemma-F-DataType-01: 类型完备性 -->

<!-- TRANSLATE: **引理**: Flink SQL 类型系统对标准 SQL 数据模型是类型完备的。 -->

<!-- TRANSLATE: **证明要点**: -->

<!-- TRANSLATE: 1. **原子类型覆盖**: 所有标准 SQL 原子类型均有对应实现 -->
<!-- TRANSLATE: 2. **复合类型封闭性**: 复合类型可递归嵌套，形成代数数据类型 -->
<!-- TRANSLATE: 3. **空值处理**: 所有类型均支持 NULL 值，满足三值逻辑 -->

<!-- TRANSLATE: ### Lemma-F-DataType-02: 类型转换单调性 -->

**引理**: 类型转换关系 $\prec$ 构成偏序集，满足：

$$
<!-- TRANSLATE: \forall T_1, T_2, T_3 \in \mathcal{T}: T_1 \prec T_2 \land T_2 \prec T_3 \Rightarrow T_1 \prec T_3 -->
$$

<!-- TRANSLATE: **隐式转换链**: -->

```
TINYINT → SMALLINT → INT → BIGINT → DECIMAL → DOUBLE
CHAR → VARCHAR → STRING
DATE → TIMESTAMP → TIMESTAMP_LTZ
```

<!-- TRANSLATE: ### Prop-F-DataType-01: 类型安全保证 -->

<!-- TRANSLATE: **命题**: 在编译期可检测所有类型不匹配错误。 -->

$$
<!-- TRANSLATE: \forall Q \in SQL: \text{TypeCheck}(Q) = \bot \Rightarrow \nexists E: \text{Execute}(Q, E) \neq \text{Error} -->
$$


<!-- TRANSLATE: ## 4. 论证过程 (Argumentation) -->

<!-- TRANSLATE: ### 4.1 DECIMAL 精度设计决策 -->

<!-- TRANSLATE: **问题**: 为什么选择 DECIMAL 而非 FLOAT 作为精确数值计算类型？ -->

<!-- TRANSLATE: **论证**: -->

<!-- TRANSLATE: - **浮点误差**: FLOAT/DOUBLE 采用 IEEE 754 表示，存在精度损失 -->
<!-- TRANSLATE: - **金融场景**: 货币计算要求精确到分，DECIMAL(19,4) 可满足 -->
<!-- TRANSLATE: - **性能权衡**: DECIMAL 计算慢于 FLOAT，但正确性优先 -->

<!-- TRANSLATE: ### 4.2 TIMESTAMP vs TIMESTAMP_LTZ 选择 -->

<!-- TRANSLATE: **决策矩阵**: -->

<!-- TRANSLATE: | 场景 | 推荐类型 | 理由 | -->
<!-- TRANSLATE: |------|----------|------| -->
<!-- TRANSLATE: | 单时区应用 | TIMESTAMP | 简单直观，无时区概念负担 | -->
<!-- TRANSLATE: | 多时区应用 | TIMESTAMP_LTZ | 统一 UTC 存储，前端本地化显示 | -->
<!-- TRANSLATE: | 与 Kafka 集成 | TIMESTAMP_LTZ | Kafka 使用 UTC epoch millis | -->


<!-- TRANSLATE: ## 6. 实例验证 (Examples) -->

<!-- TRANSLATE: ### 6.1 DDL 类型定义示例 -->

```sql
-- 创建包含完整类型系统的表
CREATE TABLE user_events (
    -- 原子类型
    user_id BIGINT,
    username VARCHAR(128),
    is_active BOOLEAN,
    score DECIMAL(10, 2),
    avatar BINARY(1024),

    -- 时间类型
    birth_date DATE,
    login_time TIME,
    event_ts TIMESTAMP(3),
    event_ts_utc TIMESTAMP_LTZ(3),

    -- 复合类型
    tags ARRAY<STRING>,
    properties MAP<STRING, STRING>,
    address ROW<
        street STRING,
        city STRING,
        zipcode STRING,
        coordinates ROW<lat DOUBLE, lon DOUBLE>
    >,

    -- 水位线定义
    WATERMARK FOR event_ts AS event_ts - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'user-events',
    'format' = 'json'
);
```

<!-- TRANSLATE: ### 6.2 类型转换示例 -->

```sql
-- 隐式转换（自动）
SELECT
    user_id + 1.5 AS user_id_double,  -- BIGINT → DOUBLE
    CONCAT('ID:', CAST(user_id AS STRING)) AS user_id_str
FROM user_events;

-- 显式转换（CAST）
SELECT
    CAST(event_ts AS DATE) AS event_date,
    CAST(score AS INT) AS score_int,  -- 截断小数
    TRY_CAST(username AS INT) AS username_maybe  -- 失败返回 NULL
FROM user_events;
```

<!-- TRANSLATE: ### 6.3 Java API 类型使用 -->

```java
import org.apache.flink.table.api.DataTypes;
import org.apache.flink.table.api.Schema;

// 编程方式定义 Schema
Schema schema = Schema.newBuilder()
    .column("user_id", DataTypes.BIGINT().notNull())
    .column("username", DataTypes.VARCHAR(128))
    .column("tags", DataTypes.ARRAY(DataTypes.STRING()))
    .column("address", DataTypes.ROW(
        DataTypes.FIELD("street", DataTypes.STRING()),
        DataTypes.FIELD("city", DataTypes.STRING())
    ))
    .columnByExpression("event_ts", "PROCTIME()")
    .build();
```


<!-- TRANSLATE: ## 8. 引用参考 (References) -->
