# Flink示例 - Docker Compose环境

## 快速开始

```bash
# 进入docker目录
cd examples/docker

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f jobmanager
```

## 访问地址

| 服务 | 地址 | 说明 |
|-----|------|------|
| Flink Web UI | http://localhost:8081 | 作业管理界面 |
| Kafka UI | http://localhost:8082 | Kafka管理界面 |

## 提交作业

### 提交Python作业

```bash
# WordCount示例
docker-compose exec jobmanager flink run -py /opt/flink/examples/python/wordcount/wordcount.py

# Table API示例
docker-compose exec jobmanager flink run -py /opt/flink/examples/python/table-api/table_api_example.py -- batch
```

### 提交Java作业

```bash
# 先确保Java项目已打包
cd ../java/wordcount && mvn clean package -DskipTests

# 提交到Flink
docker-compose exec jobmanager flink run /opt/flink/examples/java/flink-wordcount-1.0.0.jar
```

## 常用命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 停止并删除数据卷
docker-compose down -v

# 查看Flink日志
docker-compose logs -f jobmanager
docker-compose logs -f taskmanager

# 进入Flink容器
docker-compose exec jobmanager bash

# 启动数据生成器
docker-compose --profile datagen up datagen

# 创建Kafka Topic
docker-compose exec kafka kafka-topics --create --topic my-topic --bootstrap-server localhost:9092

# 查看Kafka消息
docker-compose exec kafka kafka-console-consumer --topic sensor-data --from-beginning --bootstrap-server localhost:9092
```

## 架构图

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Flink Web UI  │────▶│    JobManager   │◀────│  SQL Client     │
│   (localhost:8081)    │   (调度中心)    │     │  (交互式SQL)    │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
           ┌────────────┐ ┌────────────┐ ┌────────────┐
           │ TaskManager│ │ TaskManager│ │ TaskManager│
           │  (Slot x4) │ │  (Slot x4) │ │  (Slot x4) │
           └────────────┘ └────────────┘ └────────────┘
                    │            │            │
                    └────────────┼────────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
           ┌────────────┐ ┌────────────┐ ┌────────────┐
           │   Kafka    │ │ Zookeeper  │ │  DataGen   │
           │  (消息队列) │ │(协调服务)  │ │ (数据生成) │
           └────────────┘ └────────────┘ └────────────┘
```

## 配置说明

### JobManager配置
- 内存: 1024m
- Heap: 512m
- Web UI端口: 8081

### TaskManager配置
- 内存: 2048m
- Slot数量: 4
- 副本数: 2

## 故障排查

### 服务无法启动
```bash
# 检查端口占用
netstat -tlnp | grep 8081

# 清理重启
docker-compose down -v
docker-compose up -d
```

### 作业提交失败
```bash
# 检查JobManager是否就绪
curl http://localhost:8081/overview

# 查看TaskManager连接状态
docker-compose logs taskmanager | grep "Registering TaskManager"
```

### 内存不足
编辑 `docker-compose.yml` 调整内存配置：
```yaml
environment:
  - FLINK_PROPERTIES=
      jobmanager.memory.process.size: 512m
      taskmanager.memory.process.size: 1024m
```
