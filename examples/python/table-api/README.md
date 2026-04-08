# Flink Table API Python示例

## 项目简介

演示PyFlink Table API和SQL的使用，包含批处理、流处理、窗口聚合和表连接。

## 功能特性

- **批处理 (Batch)**: 静态数据查询分析
- **流处理 (Stream)**: 实时数据过滤转换
- **窗口聚合 (Window)**: 时间窗口统计
- **表连接 (Join)**: 多表关联查询

## 快速开始

### 安装依赖

```bash
cd examples/python/table-api
pip install -r requirements.txt
```

### 运行示例

```bash
# 批处理示例
python table_api_example.py batch

# 流处理示例
python table_api_example.py stream

# 窗口聚合示例
python table_api_example.py window

# 表连接示例
python table_api_example.py join

# 运行所有示例
python table_api_example.py all
```

## 示例详解

### 1. 批处理示例 (batch)

演示静态数据分析：
```sql
SELECT 
    user_id,
    COUNT(*) as order_count,
    SUM(amount) as total_amount
FROM orders
GROUP BY user_id
```

**输出**:
```
+-------+-------------+-------------+
|user_id|  order_count| total_amount|
+-------+-------------+-------------+
|   U001|            3|      20297.0|
|   U002|            2|      18998.0|
|   U003|            1|       4999.0|
+-------+-------------+-------------+
```

### 2. 流处理示例 (stream)

使用Datagen连接器生成实时数据流。

### 3. 窗口聚合示例 (window)

10秒滚动窗口温度统计：
```sql
SELECT 
    sensor_id,
    window_start,
    window_end,
    AVG(temperature) as avg_temp,
    MAX(temperature) as max_temp
FROM TABLE(
    TUMBLE(TABLE sensor_readings, DESCRIPTOR(event_time), INTERVAL '10' SECONDS)
)
GROUP BY sensor_id, window_start, window_end
```

### 4. 表连接示例 (join)

订单表与用户表关联：
```sql
SELECT 
    o.order_id,
    u.user_name,
    u.city,
    o.product,
    o.amount
FROM orders o
INNER JOIN users u ON o.user_id = u.user_id
```

## 连接器说明

| 连接器 | 用途 | 配置 |
|-------|------|------|
| values | 批处理测试数据 | `'connector' = 'values'` |
| datagen | 流处理测试数据 | `'connector' = 'datagen'` |
| print | 输出到控制台 | `'connector' = 'print'` |

## 高级用法

### 使用TableDescriptor
```python
from pyflink.table import TableDescriptor, Schema, DataTypes

t_env.create_table(
    "my_table",
    TableDescriptor.for_connector("filesystem")
        .schema(Schema.new_builder()
            .column("id", DataTypes.STRING())
            .column("value", DataTypes.DOUBLE())
            .build())
        .option("path", "/path/to/file")
        .format("csv")
        .build()
)
```

### 使用表达式API
```python
from pyflink.table.expressions import col, lit

table.select(col("name"), col("age") + lit(1).alias("age_next_year"))
```
