#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flink Table API Python示例

演示Flink SQL和Table API的使用，包括：
1. 批处理查询
2. 流处理查询
3. 窗口聚合
4. 表连接

运行方式：
    python table_api_example.py [batch|stream|window|join]

依赖安装：
    pip install -r requirements.txt

作者: AnalysisDataFlow Project
版本: 1.0.0
"""

import argparse
import logging
from datetime import datetime

from pyflink.table import (
    EnvironmentSettings, 
    TableEnvironment,
    TableDescriptor,
    Schema,
    DataTypes
)
from pyflink.table.expressions import lit, col
from pyflink.table.window import Tumble

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_table_env(mode: str = "streaming") -> TableEnvironment:
    """
    创建TableEnvironment
    
    Args:
        mode: "streaming" 或 "batch"
    
    Returns:
        TableEnvironment实例
    """
    if mode == "batch":
        settings = EnvironmentSettings.in_batch_mode()
    else:
        settings = EnvironmentSettings.in_streaming_mode()
    
    return TableEnvironment.create(settings)


def batch_processing_example():
    """
    批处理示例：订单数据分析
    """
    logger.info("=" * 50)
    logger.info("Table API - 批处理示例")
    logger.info("=" * 50)
    
    # 创建批处理环境
    t_env = create_table_env("batch")
    
    # 创建源表 - 使用Values
    t_env.execute_sql("""
        CREATE TABLE orders (
            order_id STRING,
            user_id STRING,
            product STRING,
            amount DOUBLE,
            order_time TIMESTAMP(3)
        ) WITH (
            'connector' = 'values'
        )
    """)
    
    # 插入数据
    t_env.execute_sql("""
        INSERT INTO orders VALUES
            ('O001', 'U001', 'iPhone', 5999.0, TIMESTAMP '2024-01-01 10:00:00'),
            ('O002', 'U002', 'MacBook', 12999.0, TIMESTAMP '2024-01-01 10:05:00'),
            ('O003', 'U001', 'AirPods', 1299.0, TIMESTAMP '2024-01-01 10:10:00'),
            ('O004', 'U003', 'iPad', 4999.0, TIMESTAMP '2024-01-01 10:15:00'),
            ('O005', 'U002', 'iPhone', 5999.0, TIMESTAMP '2024-01-01 10:20:00'),
            ('O006', 'U001', 'MacBook', 12999.0, TIMESTAMP '2024-01-01 10:25:00')
    """)
    
    # 查询1: 按用户统计订单金额
    logger.info("\n【查询1】按用户统计订单金额")
    result1 = t_env.sql_query("""
        SELECT 
            user_id,
            COUNT(*) as order_count,
            SUM(amount) as total_amount,
            AVG(amount) as avg_amount
        FROM orders
        GROUP BY user_id
        ORDER BY total_amount DESC
    """)
    result1.execute().print()
    
    # 查询2: 按商品统计销量
    logger.info("\n【查询2】按商品统计销量")
    result2 = t_env.sql_query("""
        SELECT 
            product,
            COUNT(*) as sales_count,
            SUM(amount) as revenue
        FROM orders
        GROUP BY product
        ORDER BY sales_count DESC
    """)
    result2.execute().print()


def stream_processing_example():
    """
    流处理示例：实时数据过滤和转换
    """
    logger.info("=" * 50)
    logger.info("Table API - 流处理示例")
    logger.info("=" * 50)
    
    t_env = create_table_env("streaming")
    
    # 创建Datagen源表 (自动生成测试数据)
    t_env.execute_sql("""
        CREATE TABLE events (
            user_id STRING,
            event_type STRING,
            event_time TIMESTAMP(3),
            amount DOUBLE,
            WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'datagen',
            'rows-per-second' = '5',
            'fields.user_id.length' = '5',
            'fields.event_type.length' = '8',
            'fields.amount.min' = '1',
            'fields.amount.max' = '1000'
        )
    """)
    
    # 创建Print结果表
    t_env.execute_sql("""
        CREATE TABLE high_value_events (
            user_id STRING,
            event_type STRING,
            amount DOUBLE,
            event_time TIMESTAMP(3)
        ) WITH (
            'connector' = 'print'
        )
    """)
    
    # 执行过滤并插入
    logger.info("\n【实时过滤】金额大于500的事件")
    t_env.execute_sql("""
        INSERT INTO high_value_events
        SELECT user_id, event_type, amount, event_time
        FROM events
        WHERE amount > 500
    """)
    
    logger.info("流处理正在运行，按Ctrl+C停止...")


def window_aggregation_example():
    """
    窗口聚合示例：10秒滚动窗口统计
    """
    logger.info("=" * 50)
    logger.info("Table API - 窗口聚合示例")
    logger.info("=" * 50)
    
    t_env = create_table_env("streaming")
    
    # 创建Datagen源表
    t_env.execute_sql("""
        CREATE TABLE sensor_readings (
            sensor_id STRING,
            temperature DOUBLE,
            event_time TIMESTAMP(3),
            WATERMARK FOR event_time AS event_time - INTERVAL '2' SECOND
        ) WITH (
            'connector' = 'datagen',
            'rows-per-second' = '2',
            'fields.sensor_id.length' = '8',
            'fields.temperature.min' = '20',
            'fields.temperature.max' = '40'
        )
    """)
    
    # 创建Print结果表
    t_env.execute_sql("""
        CREATE TABLE window_stats (
            sensor_id STRING,
            window_start TIMESTAMP(3),
            window_end TIMESTAMP(3),
            avg_temp DOUBLE,
            max_temp DOUBLE,
            min_temp DOUBLE,
            reading_count BIGINT
        ) WITH (
            'connector' = 'print'
        )
    """)
    
    # 执行窗口聚合
    logger.info("\n【窗口聚合】10秒滚动窗口温度统计")
    t_env.execute_sql("""
        INSERT INTO window_stats
        SELECT 
            sensor_id,
            window_start,
            window_end,
            AVG(temperature) as avg_temp,
            MAX(temperature) as max_temp,
            MIN(temperature) as min_temp,
            COUNT(*) as reading_count
        FROM TABLE(
            TUMBLE(TABLE sensor_readings, DESCRIPTOR(event_time), INTERVAL '10' SECONDS)
        )
        GROUP BY sensor_id, window_start, window_end
    """)
    
    logger.info("窗口聚合正在运行，按Ctrl+C停止...")


def table_join_example():
    """
    表连接示例：订单与用户表关联
    """
    logger.info("=" * 50)
    logger.info("Table API - 表连接示例")
    logger.info("=" * 50)
    
    t_env = create_table_env("batch")
    
    # 创建订单表
    t_env.execute_sql("""
        CREATE TABLE orders (
            order_id STRING,
            user_id STRING,
            product STRING,
            amount DOUBLE
        ) WITH (
            'connector' = 'values'
        )
    """)
    
    # 创建用户表
    t_env.execute_sql("""
        CREATE TABLE users (
            user_id STRING,
            user_name STRING,
            city STRING
        ) WITH (
            'connector' = 'values'
        )
    """)
    
    # 插入订单数据
    t_env.execute_sql("""
        INSERT INTO orders VALUES
            ('O001', 'U001', 'iPhone', 5999.0),
            ('O002', 'U002', 'MacBook', 12999.0),
            ('O003', 'U001', 'AirPods', 1299.0),
            ('O004', 'U003', 'iPad', 4999.0),
            ('O005', 'U004', 'iPhone', 5999.0)
    """)
    
    # 插入用户数据
    t_env.execute_sql("""
        INSERT INTO users VALUES
            ('U001', '张三', '北京'),
            ('U002', '李四', '上海'),
            ('U003', '王五', '深圳'),
            ('U004', '赵六', '杭州')
    """)
    
    # 执行内连接
    logger.info("\n【内连接】订单与用户关联")
    result = t_env.sql_query("""
        SELECT 
            o.order_id,
            u.user_name,
            u.city,
            o.product,
            o.amount
        FROM orders o
        INNER JOIN users u ON o.user_id = u.user_id
    """)
    result.execute().print()
    
    # 按城市统计销售额
    logger.info("\n【分组聚合】按城市统计销售额")
    result2 = t_env.sql_query("""
        SELECT 
            u.city,
            COUNT(*) as order_count,
            SUM(o.amount) as total_sales
        FROM orders o
        INNER JOIN users u ON o.user_id = u.user_id
        GROUP BY u.city
        ORDER BY total_sales DESC
    """)
    result2.execute().print()


def main():
    """主入口"""
    parser = argparse.ArgumentParser(description='Flink Table API Python Examples')
    parser.add_argument(
        'example',
        choices=['batch', 'stream', 'window', 'join', 'all'],
        default='batch',
        nargs='?',
        help='选择要运行的示例 (默认: batch)'
    )
    
    args = parser.parse_args()
    
    try:
        if args.example == 'batch' or args.example == 'all':
            batch_processing_example()
        
        if args.example == 'stream' or args.example == 'all':
            stream_processing_example()
        
        if args.example == 'window' or args.example == 'all':
            window_aggregation_example()
        
        if args.example == 'join' or args.example == 'all':
            table_join_example()
            
    except KeyboardInterrupt:
        logger.info("用户中断执行")
    except Exception as e:
        logger.error(f"执行出错: {e}")
        raise


if __name__ == '__main__':
    main()
