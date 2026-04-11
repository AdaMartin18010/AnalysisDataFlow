---
title: "[EN] Flink Built In Functions Reference"
translation_status: "ai_translated"
source_file: "Flink/flink-built-in-functions-reference.md"
source_version: "4c419ac3"
translator: "AI"
reviewer: null
translated_at: "2026-04-08T15:15:06.347290"
reviewed_at: null
quality_score: null
terminology_verified: false
---


<!-- AI Translation Template - Replace <!-- TRANSLATE --> markers with actual translation -->

<!-- TRANSLATE: # Flink Built-in Functions 完整参考 -->

<!-- TRANSLATE: > 所属阶段: Flink | 前置依赖: [flink-data-types-reference.md](./flink-data-types-reference.md) | 形式化等级: L4 -->


<!-- TRANSLATE: ## 2. 属性推导 (Properties) -->

<!-- TRANSLATE: ### Lemma-F-02-01: 函数确定性分类 -->

<!-- TRANSLATE: **引理**: 内置函数按确定性分为三类： -->

$$
<!-- TRANSLATE: \Delta(f) = \begin{cases} -->
<!-- TRANSLATE: \text{DETERMINISTIC} & \text{if } f(x) = f(x) \text{ 恒成立} \\ -->
<!-- TRANSLATE: \text{NON-DETERMINISTIC} & \text{if } f(x) \text{ 每次调用可能变化} \\ -->
<!-- TRANSLATE: \text{DYNAMIC} & \text{if } f(x) \text{ 依赖执行上下文} -->
<!-- TRANSLATE: \end{cases} -->
$$

<!-- TRANSLATE: **确定性分类表**： -->

<!-- TRANSLATE: | 确定性 | 函数示例 | 说明 | -->
<!-- TRANSLATE: |--------|----------|------| -->
<!-- TRANSLATE: | **确定性** | `ABS`, `UPPER`, `CONCAT`, `DATE_ADD` | 相同输入必产生相同输出 | -->
<!-- TRANSLATE: | **非确定性** | `RAND()`, `CURRENT_TIMESTAMP`, `UUID()` | 每次调用可能产生不同结果 | -->
<!-- TRANSLATE: | **动态** | `SESSION_USER`, `CURRENT_DATABASE`, `CURRENT_SCHEMA` | 依赖执行上下文 | -->

<!-- TRANSLATE: ### Lemma-F-02-02: 空值传播规则 -->

<!-- TRANSLATE: **引理**: 大多数内置函数遵循 **NULL 输入 → NULL 输出** 原则： -->

$$
<!-- TRANSLATE: f(\text{NULL}) = \text{NULL}, \quad \forall f \in F_{scalar} \setminus F_{null\_handling} -->
$$

<!-- TRANSLATE: **例外函数表**（显式处理 NULL）： -->

<!-- TRANSLATE: | 函数 | 语法 | 行为 | 示例 | -->
<!-- TRANSLATE: |------|------|------|------| -->
<!-- TRANSLATE: | `COALESCE` | `COALESCE(a, b, ...)` | 返回第一个非 NULL 值 | `COALESCE(NULL, 1, 2)` → 1 | -->
<!-- TRANSLATE: | `NULLIF` | `NULLIF(a, b)` | 若 a=b 返回 NULL，否则返回 a | `NULLIF(5, 5)` → NULL | -->
<!-- TRANSLATE: | `IFNULL` | `IFNULL(a, b)` | 若 a 为 NULL 返回 b | `IFNULL(NULL, 'default')` → 'default' | -->
<!-- TRANSLATE: | `IS NULL` | `a IS NULL` | 判断是否为 NULL | `NULL IS NULL` → TRUE | -->
<!-- TRANSLATE: | `IS NOT NULL` | `a IS NOT NULL` | 判断是否非 NULL | `5 IS NOT NULL` → TRUE | -->
<!-- TRANSLATE: | `NVL` | `NVL(a, b)` | 同 IFNULL | `NVL(NULL, 0)` → 0 | -->

<!-- TRANSLATE: ### Prop-F-02-01: 类型推导完备性 -->

<!-- TRANSLATE: **命题**: 类型系统可推导出任意合法函数表达式的结果类型。 -->

```
输入类型 → 类型检查 → 隐式转换 → 函数执行 → 输出类型
    ↑___________________________|
          (类型兼容性验证)
```


<!-- TRANSLATE: ## 4. 论证过程 (Argumentation) -->

<!-- TRANSLATE: ### 4.1 TRY_CAST vs CAST 设计决策 -->

<!-- TRANSLATE: **问题**: 为什么需要 `TRY_CAST`？ -->

<!-- TRANSLATE: **论证**: -->

<!-- TRANSLATE: | 特性 | CAST | TRY_CAST | -->
<!-- TRANSLATE: |------|------|----------| -->
<!-- TRANSLATE: | 失败行为 | 抛出异常 | 返回 NULL | -->
<!-- TRANSLATE: | 性能 | 较高 | 略低（异常捕获） | -->
<!-- TRANSLATE: | 容错性 | 低 | 高 | -->
<!-- TRANSLATE: | 适用场景 | 严格数据验证 | 容错数据处理 | -->

<!-- TRANSLATE: **使用场景对比**： -->

```sql
-- 严格模式：失败即报错
SELECT CAST('invalid' AS INT);  -- 抛出异常，查询中断

-- 容错模式：失败返回 NULL
SELECT TRY_CAST('invalid' AS INT);  -- 返回 NULL，继续执行
```

<!-- TRANSLATE: ### 4.2 窗口函数 vs 分组聚合对比 -->

<!-- TRANSLATE: | 特性 | 分组聚合 | 窗口函数 | -->
<!-- TRANSLATE: |------|----------|----------| -->
<!-- TRANSLATE: | 输出行数 | ≤ 输入行数 | = 输入行数 | -->
<!-- TRANSLATE: | 语义 | 数据压缩/汇总 | 附加计算列 | -->
<!-- TRANSLATE: | 使用位置 | SELECT + GROUP BY | SELECT 子句 | -->
<!-- TRANSLATE: | 典型应用 | 统计汇总 | 排名、趋势分析、行间计算 | -->
<!-- TRANSLATE: | 状态需求 | 分组状态 | 窗口缓冲区 | -->


<!-- TRANSLATE: ## 6. 实例验证 (Examples) -->

<!-- TRANSLATE: ### 6.1 数学函数完整示例 -->

```sql
-- 数学函数使用
SELECT
    order_id,
    amount,

    -- 基本运算
    ABS(amount) AS abs_amount,
    ROUND(amount, 2) AS rounded,
    CEIL(amount) AS ceiling,
    FLOOR(amount) AS flooring,

    -- 幂运算与根
    POWER(amount, 2) AS squared,
    SQRT(ABS(amount)) AS square_root,
    CBRT(amount) AS cube_root,

    -- 对数运算
    LN(amount + 1) AS natural_log,
    LOG10(amount + 1) AS log_base_10,
    LOG(2, amount + 1) AS log_base_2,
    EXP(amount) AS exponential,

    -- 三角函数
    SIN(amount) AS sine,
    COS(amount) AS cosine,
    TAN(amount) AS tangent,

    -- 取模与符号
    MOD(order_id, 100) AS bucket,
    SIGN(amount) AS sign_value,
    PI() AS pi_constant,

    -- 边界限制
    GREATEST(amount, 100) AS at_least_100,
    LEAST(amount, 10000) AS at_most_10000
FROM orders;
```

<!-- TRANSLATE: ### 6.2 字符串函数完整示例 -->

```sql
-- 字符串处理
SELECT
    email,

    -- 大小写转换
    UPPER(email) AS email_upper,
    LOWER(email) AS email_lower,
    INITCAP(email) AS email_title_case,

    -- 子串提取
    SUBSTRING(email, 1, 5) AS first_5_chars,
    SUBSTRING(email FROM 1 FOR 5) AS first_5_alt,
    LEFT(email, 3) AS left_3,
    RIGHT(email, 4) AS domain_suffix,

    -- 位置查找
    POSITION('@' IN email) AS at_position,
    STRPOS(email, '@') AS at_position_alt,

    -- 子串提取（基于位置）
    SUBSTRING(email, 1, POSITION('@' IN email) - 1) AS username,
    SUBSTRING(email, POSITION('@' IN email) + 1) AS domain,

    -- 空白处理
    TRIM(BOTH ' ' FROM email) AS trimmed,
    TRIM(LEADING ' ' FROM email) AS ltrimmed,
    TRIM(TRAILING ' ' FROM email) AS rtrimmed,

    -- 替换操作
    REPLACE(email, '@', '[at]') AS obfuscated,
    REGEXP_REPLACE(email, '@.*', '') AS regex_username,

    -- 连接操作
    CONCAT(first_name, ' ', last_name) AS full_name,
    first_name || ' ' || last_name AS full_name_alt,
    CONCAT_WS(' - ', first_name, last_name, email) AS joined,

    -- 长度与填充
    LENGTH(email) AS email_length,
    CHAR_LENGTH(email) AS char_length,
    OCTET_LENGTH(email) AS byte_length,
    LPAD(order_id::STRING, 10, '0') AS padded_id,
    RPAD(status, 10, '_') AS r_padded_status,

    -- 重复与反转
    REPEAT('*', LENGTH(password)) AS masked_password,
    REVERSE(email) AS reversed_email,

    -- 包含判断
    email LIKE '%@gmail.com' AS is_gmail,
    email ILIKE '%@GMAIL.COM' AS is_gmail_case_insensitive,
    email SIMILAR TO '[a-z]+@[a-z]+\.[a-z]+' AS valid_pattern,

    -- 分割
    SPLIT_INDEX(email, '@', 0) AS split_username,
    SPLIT_INDEX(email, '@', 1) AS split_domain
FROM users;
```

<!-- TRANSLATE: ### 6.3 日期时间函数完整示例 -->

```sql
-- 日期时间处理
SELECT
    event_time,

    -- 当前时间函数
    CURRENT_DATE AS today,
    CURRENT_TIME AS current_time,
    CURRENT_TIMESTAMP AS now,
    LOCALTIME AS local_time,
    LOCALTIMESTAMP AS local_timestamp,
    NOW() AS now_alt,

    -- 格式化
    DATE_FORMAT(event_time, 'yyyy-MM-dd HH:mm:ss') AS formatted,
    DATE_FORMAT(event_time, 'yyyy年MM月dd日') AS chinese_format,

    -- 提取组件
    EXTRACT(YEAR FROM event_time) AS year,
    EXTRACT(MONTH FROM event_time) AS month,
    EXTRACT(DAY FROM event_time) AS day,
    EXTRACT(HOUR FROM event_time) AS hour,
    EXTRACT(MINUTE FROM event_time) AS minute,
    EXTRACT(SECOND FROM event_time) AS second,
    EXTRACT(WEEK FROM event_time) AS week_of_year,
    EXTRACT(DOW FROM event_time) AS day_of_week,
    EXTRACT(DOY FROM event_time) AS day_of_year,
    EXTRACT(QUARTER FROM event_time) AS quarter,

    -- 便捷提取函数
    YEAR(event_time) AS year_alt,
    MONTH(event_time) AS month_alt,
    DAYOFMONTH(event_time) AS day_alt,
    DAYOFWEEK(event_time) AS dayofweek_alt,
    DAYOFYEAR(event_time) AS dayofyear_alt,
    HOUR(event_time) AS hour_alt,
    MINUTE(event_time) AS minute_alt,
    SECOND(event_time) AS second_alt,

    -- 日期计算
    DATE(event_time) AS date_only,
    TIME(event_time) AS time_only,
    DATEDIFF(CURRENT_DATE, DATE(event_time)) AS days_ago,
    DATEDIFF(event_time, TIMESTAMP '2024-01-01') AS days_since_year_start,

    -- 日期加减
    DATE_ADD(DATE(event_time), 7) AS next_week,
    DATE_SUB(DATE(event_time), 30) AS month_ago,
    event_time + INTERVAL '1' DAY AS tomorrow_same_time,
    event_time - INTERVAL '2' HOUR AS two_hours_ago,
    TIMESTAMPADD(HOUR, 8, event_time) AS beijing_time,
    TIMESTAMPDIFF(DAY, TIMESTAMP '2024-01-01', event_time) AS day_diff,

    -- 月初月末
    DATE_TRUNC('MONTH', event_time) AS month_start,
    LAST_DAY(event_time) AS month_end,

    -- 时区转换
    CONVERT_TZ(event_time, 'UTC', 'Asia/Shanghai') AS shanghai_time,
    TO_TIMESTAMP_LTZ(UNIX_TIMESTAMP(event_time) * 1000, 3) AS as_ltz,

    -- 其他
    UNIX_TIMESTAMP(event_time) AS unix_seconds,
    UNIX_TIMESTAMP(event_time) * 1000 AS unix_millis,
    FROM_UNIXTIME(UNIX_TIMESTAMP(event_time)) AS from_unix
FROM events;
```

<!-- TRANSLATE: ### 6.4 聚合函数完整示例 -->

```sql
-- 聚合分析
SELECT
    category,

    -- 基本计数
    COUNT(*) AS total_orders,
    COUNT(order_id) AS count_order_id,
    COUNT(DISTINCT user_id) AS unique_users,
    COUNT(DISTINCT DATE(event_time)) AS active_days,

    -- 求和与平均
    SUM(amount) AS total_amount,
    AVG(amount) AS avg_amount,
    SUM(amount) / COUNT(*) AS manual_avg,

    -- 最值
    MIN(amount) AS min_amount,
    MAX(amount) AS max_amount,
    MIN(event_time) AS first_order_time,
    MAX(event_time) AS last_order_time,

    -- 范围统计
    MAX(amount) - MIN(amount) AS amount_range,

    -- 统计函数
    STDDEV(amount) AS std_amount,
    STDDEV_SAMP(amount) AS std_sample,
    STDDEV_POP(amount) AS std_population,
    VARIANCE(amount) AS variance_amount,
    VAR_SAMP(amount) AS var_sample,
    VAR_POP(amount) AS var_population,

    -- 百分位数
    PERCENTILE(amount, 0.5) AS median,
    PERCENTILE(amount, 0.95) AS p95,
    PERCENTILE(amount, 0.99) AS p99,

    -- 集合聚合
    COLLECT(user_id) AS user_list,
    COLLECT(DISTINCT user_id) AS unique_user_list,

    -- 字符串聚合
    LISTAGG(product_name, ', ') AS product_list,
    LISTAGG(DISTINCT category, ' | ') AS category_list,

    -- 首末值
    FIRST_VALUE(amount) AS first_amount,
    LAST_VALUE(amount) AS last_amount,

    -- 条件聚合
    COUNT(*) FILTER (WHERE amount > 1000) AS high_value_count,
    SUM(amount) FILTER (WHERE status = 'completed') AS completed_amount,
    AVG(amount) FILTER (WHERE payment_method = 'credit_card') AS cc_avg
FROM orders
GROUP BY category;
```

<!-- TRANSLATE: ### 6.5 窗口函数完整示例 -->

```sql
-- 窗口分析
SELECT
    user_id,
    order_time,
    amount,
    category,

    -- 排序函数（全局）
    ROW_NUMBER() OVER (ORDER BY amount DESC) AS overall_rank,
    RANK() OVER (ORDER BY amount DESC) AS overall_rank_with_ties,
    DENSE_RANK() OVER (ORDER BY amount DESC) AS overall_dense_rank,

    -- 排序函数（分区）
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY amount DESC) AS category_rank,
    RANK() OVER (PARTITION BY category ORDER BY amount DESC) AS category_rank_ties,
    DENSE_RANK() OVER (PARTITION BY category ORDER BY amount DESC) AS category_dense_rank,
    NTILE(4) OVER (ORDER BY amount) AS quartile,

    -- 分区排序
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_time) AS user_order_seq,

    -- 取值函数
    FIRST_VALUE(amount) OVER (PARTITION BY user_id ORDER BY order_time) AS first_order,
    LAST_VALUE(amount) OVER (
        PARTITION BY user_id
        ORDER BY order_time
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS last_order,
    NTH_VALUE(amount, 2) OVER (PARTITION BY user_id ORDER BY order_time) AS second_order,

    -- 偏移函数
    LAG(amount, 1, 0) OVER (PARTITION BY user_id ORDER BY order_time) AS prev_order,
    LAG(amount, 2, 0) OVER (PARTITION BY user_id ORDER BY order_time) AS prev_2_order,
    LEAD(amount, 1, 0) OVER (PARTITION BY user_id ORDER BY order_time) AS next_order,
    LEAD(amount, 3, 0) OVER (PARTITION BY user_id ORDER BY order_time) AS next_3_order,

    -- 变化量计算
    amount - LAG(amount, 1, 0) OVER (PARTITION BY user_id ORDER BY order_time) AS amount_change,
    (amount - LAG(amount, 1, amount) OVER (PARTITION BY user_id ORDER BY order_time))
        / LAG(amount, 1, amount) OVER (PARTITION BY user_id ORDER BY order_time) * 100 AS pct_change,

    -- 分布函数
    PERCENT_RANK() OVER (ORDER BY amount) AS pct_rank,
    CUME_DIST() OVER (ORDER BY amount) AS cum_dist,

    -- 移动平均
    AVG(amount) OVER (
        PARTITION BY user_id
        ORDER BY order_time
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3,

    -- 累计求和
    SUM(amount) OVER (
        PARTITION BY user_id
        ORDER BY order_time
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total,

    -- 窗口总计百分比
    amount / SUM(amount) OVER (PARTITION BY user_id) * 100 AS pct_of_user_total,
    amount / SUM(amount) OVER () * 100 AS pct_of_grand_total

FROM orders;
```

<!-- TRANSLATE: ### 6.6 条件与空值处理完整示例 -->

```sql
-- 条件表达式
SELECT
    user_id,
    amount,
    status,
    discount,
    phone,
    email,

    -- CASE 表达式（完整形式）
    CASE
        WHEN amount < 100 THEN 'small'
        WHEN amount < 1000 THEN 'medium'
        WHEN amount < 10000 THEN 'large'
        ELSE 'enterprise'
    END AS order_size,

    -- CASE 表达式（简单形式）
    CASE status
        WHEN 'pending' THEN '待处理'
        WHEN 'processing' THEN '处理中'
        WHEN 'completed' THEN '已完成'
        WHEN 'cancelled' THEN '已取消'
        ELSE '未知状态'
    END AS status_cn,

    -- 简化条件函数
    IF(amount > 1000, 'VIP', 'Regular') AS customer_type,
    IF(status = 'completed', amount, 0) AS completed_amount,

    -- 空值处理
    COALESCE(phone, email, 'N/A') AS primary_contact,
    COALESCE(discount, 0) AS safe_discount,
    COALESCE(discount, 0, amount * 0.1) AS discount_or_default,

    -- NULL 条件判断
    NULLIF(status, 'deleted') AS active_status,
    IFNULL(discount, 0) AS final_discount,
    NVL(discount, 0) AS nvl_discount,

    -- 存在性判断
    phone IS NULL AS has_no_phone,
    email IS NOT NULL AS has_email,
    COALESCE(phone, email) IS NOT NULL AS has_contact,

    -- 条件聚合（窗口函数内）
    COUNT(*) FILTER (WHERE status = 'completed') OVER () AS total_completed,

    -- NULL 安全比较
    NULLIF(amount, 0) AS safe_divisor,
    amount / NULLIF(discount, 0) AS risky_division_safe
FROM orders;
```


<!-- TRANSLATE: ## 8. 引用参考 (References) -->
