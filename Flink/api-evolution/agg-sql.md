# 聚合函数 SQL 演进 特性跟踪

> 所属阶段: Flink/api-evolution | 前置依赖: [Aggregation Functions][^1] | 形式化等级: L3

## 1. 概念定义 (Definitions)

### Def-F-Agg-01: Aggregate Function

聚合函数：
$$
\text{AggFunc} : \text{Multiset}<T> \to R
$$

### Def-F-Agg-02: Distinct Aggregation

去重聚合：
$$
\text{Distinct} : \text{AggFunc}(\text{SET}(x)) \neq \text{AggFunc}(\text{MULTISET}(x))
$$

## 2. 属性推导 (Properties)

### Prop-F-Agg-01: Incremental Computation

增量计算：
$$
\text{Agg}(S \cup \{x\}) = \text{Update}(\text{Agg}(S), x)
$$

## 3. 关系建立 (Relations)

### 聚合演进

| 版本 | 特性 | 状态 |
|------|------|------|
| 2.4 | 标准聚合 | GA |
| 2.4 | JSON聚合 | GA |
| 2.5 | 近似聚合 | GA |
| 2.5 | 自定义聚合 | GA |

## 4. 论证过程 (Argumentation)

### 4.1 聚合类型

| 类型 | 描述 |
|------|------|
| 标准 | SUM, AVG, COUNT, MIN, MAX |
| JSON | JSON_OBJECTAGG, JSON_ARRAYAGG |
| 近似 | APPROX_COUNT_DISTINCT |

## 5. 形式证明 / 工程论证

### 5.1 JSON聚合

```sql
SELECT
    department,
    JSON_OBJECTAGG(name, salary) AS salaries,
    JSON_ARRAYAGG(name ORDER BY salary DESC) AS employees
FROM staff
GROUP BY department;
```

## 6. 实例验证 (Examples)

### 6.1 近似去重

```sql
SELECT
    date,
    APPROX_COUNT_DISTINCT(user_id) AS unique_users
FROM events
GROUP BY date;
```

## 7. 可视化 (Visualizations)

```mermaid
graph LR
    A[输入] --> B[分组]
    B --> C[聚合计算]
    C --> D[结果]
```

## 8. 引用参考 (References)

[^1]: Flink Aggregation Documentation

---

## 跟踪信息

| 属性 | 值 |
|------|-----|
| 版本 | 2.4-3.0 |
| 当前状态 | 演进中 |
