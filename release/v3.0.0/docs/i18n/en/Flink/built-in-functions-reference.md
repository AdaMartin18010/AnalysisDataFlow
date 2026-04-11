---
title: "[EN] Built In Functions Reference"
translation_status: "ai_translated"
source_file: "Flink/built-in-functions-reference.md"
source_version: "a29c2d33"
translator: "AI"
reviewer: null
translated_at: "2026-04-08T15:15:06.343364"
reviewed_at: null
quality_score: null
terminology_verified: false
---


<!-- AI Translation Template - Replace <!-- TRANSLATE --> markers with actual translation -->

<!-- TRANSLATE: # Flink Built-in Functions 完整参考 -->

<!-- TRANSLATE: > 所属阶段: Flink | 前置依赖: [data-types-complete-reference.md](./data-types-complete-reference.md) | 形式化等级: L4 -->


<!-- TRANSLATE: ## 2. 属性推导 (Properties) -->

<!-- TRANSLATE: ### Lemma-F-Func-01: 函数确定性分类 -->

<!-- TRANSLATE: **引理**: 内置函数按确定性分为三类： -->

$$
<!-- TRANSLATE: \Delta(f) = \begin{cases} -->
<!-- TRANSLATE: \text{DETERMINISTIC} & \text{if } f(x) = f(x) \text{ 恒成立} \\ -->
<!-- TRANSLATE: \text{NON-DETERMINISTIC} & \text{if } f(x) \text{ 可能变化} \\ -->
<!-- TRANSLATE: \text{DYNAMIC} & \text{if } f(x) \text{ 依赖上下文} -->
<!-- TRANSLATE: \end{cases} -->
$$

<!-- TRANSLATE: **分类示例**： -->

<!-- TRANSLATE: | 确定性 | 函数示例 | 说明 | -->
<!-- TRANSLATE: |--------|----------|------| -->
<!-- TRANSLATE: | 确定性 | ABS, UPPER, CONCAT | 相同输入必产生相同输出 | -->
<!-- TRANSLATE: | 非确定性 | RAND(), CURRENT_TIMESTAMP | 每次调用可能产生不同结果 | -->
<!-- TRANSLATE: | 动态 | SESSION_USER, CURRENT_DATABASE | 依赖执行上下文 | -->

<!-- TRANSLATE: ### Lemma-F-Func-02: 空值传播规则 -->

<!-- TRANSLATE: **引理**: 大多数内置函数遵循 **NULL 输入 → NULL 输出** 原则： -->

$$
<!-- TRANSLATE: f(\text{NULL}) = \text{NULL}, \quad \forall f \in F_{scalar} \setminus F_{null\_handling} -->
$$

<!-- TRANSLATE: **例外函数**（显式处理 NULL）： -->

<!-- TRANSLATE: - `COALESCE(a, b, ...)` - 返回第一个非 NULL 值 -->
<!-- TRANSLATE: - `NULLIF(a, b)` - 若 a=b 返回 NULL，否则返回 a -->
<!-- TRANSLATE: - `IFNULL(a, b)` - 若 a 为 NULL 返回 b -->
<!-- TRANSLATE: - `IS NULL` / `IS NOT NULL` - NULL 判断 -->

<!-- TRANSLATE: ### Prop-F-Func-01: 类型推导完备性 -->

<!-- TRANSLATE: **命题**: 类型系统可推导出任意合法函数表达式的结果类型。 -->

```
输入类型 → 类型检查 → 隐式转换 → 函数执行 → 输出类型
    ↑___________________________|
          (类型兼容性验证)
```


<!-- TRANSLATE: ## 4. 论证过程 (Argumentation) -->

<!-- TRANSLATE: ### 4.1 TRY_CAST 设计决策 -->

<!-- TRANSLATE: **问题**: 为什么需要 `TRY_CAST`？ -->

<!-- TRANSLATE: **论证**: -->

<!-- TRANSLATE: - **问题**: `CAST` 在转换失败时抛出异常，中断查询执行 -->
<!-- TRANSLATE: - **方案**: `TRY_CAST` 返回 NULL 而非异常 -->
<!-- TRANSLATE: - **权衡**: 性能略低（需要异常捕获），但提升容错性 -->

<!-- TRANSLATE: **使用场景对比**： -->

```sql
-- 严格模式：失败即报错
SELECT CAST('invalid' AS INT);  -- 抛出异常

-- 容错模式：失败返回 NULL
SELECT TRY_CAST('invalid' AS INT);  -- 返回 NULL
```

<!-- TRANSLATE: ### 4.2 窗口函数 vs 分组聚合 -->

<!-- TRANSLATE: | 特性 | 分组聚合 | 窗口函数 | -->
<!-- TRANSLATE: |------|----------|----------| -->
<!-- TRANSLATE: | 输出行数 | ≤ 输入行数 | = 输入行数 | -->
<!-- TRANSLATE: | 语义 | 数据压缩 | 附加计算列 | -->
<!-- TRANSLATE: | 使用位置 | SELECT + GROUP BY | SELECT 子句 | -->
<!-- TRANSLATE: | 典型应用 | 统计汇总 | 排名、趋势分析 | -->


<!-- TRANSLATE: ## 6. 实例验证 (Examples) -->

<!-- TRANSLATE: ### 6.1 数学函数示例 -->

```sql
-- 数学函数使用
SELECT
    order_id,
    amount,
    ABS(amount) AS abs_amount,
    ROUND(amount, 2) AS rounded,
    POWER(amount, 2) AS squared,
    SQRT(ABS(amount)) AS root,
    LN(amount + 1) AS log_natural,
    MOD(order_id, 100) AS bucket
FROM orders;
```

<!-- TRANSLATE: ### 6.2 字符串函数示例 -->

```sql
-- 字符串处理
SELECT
    email,
    UPPER(email) AS email_upper,
    LOWER(SUBSTRING(email, 1, POSITION('@' IN email) - 1)) AS username,
    TRIM(BOTH ' ' FROM email) AS trimmed,
    REPLACE(email, '@', '[at]') AS obfuscated,
    CONCAT(first_name, ' ', last_name) AS full_name,
    LENGTH(email) AS email_length
FROM users;
```

<!-- TRANSLATE: ### 6.3 日期时间函数示例 -->

```sql
-- 日期时间处理
SELECT
    event_time,
    CURRENT_DATE AS today,
    DATE_FORMAT(event_time, 'yyyy-MM-dd HH:mm:ss') AS formatted,
    EXTRACT(YEAR FROM event_time) AS year,
    EXTRACT(MONTH FROM event_time) AS month,
    DATEDIFF(CURRENT_DATE, DATE(event_time)) AS days_ago,
    DATE_ADD(DATE(event_time), 7) AS next_week,
    TIMESTAMPADD(HOUR, 8, event_time) AS beijing_time
FROM events;
```

<!-- TRANSLATE: ### 6.4 聚合函数示例 -->

```sql
-- 聚合分析
SELECT
    category,
    COUNT(*) AS total_orders,
    COUNT(DISTINCT user_id) AS unique_users,
    SUM(amount) AS total_amount,
    AVG(amount) AS avg_amount,
    MIN(amount) AS min_amount,
    MAX(amount) AS max_amount,
    STDDEV(amount) AS std_amount,
    PERCENTILE(amount, 0.95) AS p95_amount
FROM orders
GROUP BY category;
```

<!-- TRANSLATE: ### 6.5 窗口函数示例 -->

```sql
-- 窗口分析
SELECT
    user_id,
    order_time,
    amount,

    -- 排序函数
    ROW_NUMBER() OVER (ORDER BY amount DESC) AS row_num,
    RANK() OVER (ORDER BY amount DESC) AS rank_num,
    DENSE_RANK() OVER (ORDER BY amount DESC) AS dense_rank,

    -- 分区排序
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_time) AS user_order_seq,

    -- 取值函数
    FIRST_VALUE(amount) OVER (PARTITION BY user_id ORDER BY order_time) AS first_order,
    LAST_VALUE(amount) OVER (PARTITION BY user_id ORDER BY order_time) AS last_order,
    LAG(amount, 1, 0) OVER (PARTITION BY user_id ORDER BY order_time) AS prev_order,
    LEAD(amount, 1, 0) OVER (PARTITION BY user_id ORDER BY order_time) AS next_order,

    -- 分布函数
    PERCENT_RANK() OVER (ORDER BY amount) AS pct_rank,
    CUME_DIST() OVER (ORDER BY amount) AS cum_dist
FROM orders;
```

<!-- TRANSLATE: ### 6.6 条件与空值处理 -->

```sql
-- 条件表达式
SELECT
    user_id,
    amount,

    -- CASE 表达式
    CASE
        WHEN amount < 100 THEN 'small'
        WHEN amount < 1000 THEN 'medium'
        ELSE 'large'
    END AS order_size,

    -- 简化条件
    IF(amount > 1000, 'VIP', 'Regular') AS customer_type,

    -- 空值处理
    COALESCE(phone, email, 'N/A') AS contact,
    NULLIF(status, 'deleted') AS active_status,
    IFNULL(discount, 0) AS final_discount
FROM orders;
```


<!-- TRANSLATE: ## 8. 引用参考 (References) -->
