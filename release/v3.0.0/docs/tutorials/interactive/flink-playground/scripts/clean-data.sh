#!/bin/bash
# 清理实验数据

echo "Cleaning up Flink data..."

# 停止服务
docker-compose down

# 清理卷数据
docker volume rm flink-playground_kafka-data 2>/dev/null || true
docker volume rm flink-playground_postgres-data 2>/dev/null || true
docker volume rm flink-playground_redis-data 2>/dev/null || true
docker volume rm flink-playground_minio-data 2>/dev/null || true

echo "Data cleaned. Run 'docker-compose up -d' to restart fresh."
