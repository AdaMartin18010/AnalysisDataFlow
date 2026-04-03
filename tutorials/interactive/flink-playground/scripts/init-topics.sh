#!/bin/bash
# 初始化 Kafka Topics

echo "Creating Kafka topics..."

# 传感器数据
docker-compose exec kafka kafka-topics \
  --create --bootstrap-server kafka:9092 \
  --replication-factor 1 \
  --partitions 4 \
  --topic sensor-data \
  --if-not-exists

# 用户行为
docker-compose exec kafka kafka-topics \
  --create --bootstrap-server kafka:9092 \
  --replication-factor 1 \
  --partitions 4 \
  --topic user-events \
  --if-not-exists

# 订单事件
docker-compose exec kafka kafka-topics \
  --create --bootstrap-server kafka:9092 \
  --replication-factor 1 \
  --partitions 4 \
  --topic orders \
  --if-not-exists

# 登录事件
docker-compose exec kafka kafka-topics \
  --create --bootstrap-server kafka:9092 \
  --replication-factor 1 \
  --partitions 4 \
  --topic login-events \
  --if-not-exists

# 清洗后数据
docker-compose exec kafka kafka-topics \
  --create --bootstrap-server kafka:9092 \
  --replication-factor 1 \
  --partitions 4 \
  --topic cleansed-data \
  --if-not-exists

# 死信队列
docker-compose exec kafka kafka-topics \
  --create --bootstrap-server kafka:9092 \
  --replication-factor 1 \
  --partitions 1 \
  --topic dead-letter-queue \
  --if-not-exists

echo "Topics created successfully!"
docker-compose exec kafka kafka-topics --bootstrap-server kafka:9092 --list
