# Flink IoT 项目骨架

> **文档编号**: F-SKELETON-MAIN
> **形式化等级**: L4 (生产级配置)
> **创建时间**: 2026-04-05
> **技术栈**: Flink SQL, Kafka, EMQX, InfluxDB, Grafana, Docker

## 快速开始

### 1. 一键启动

```bash
# 进入项目目录
cd Flink-IoT-Authority-Alignment/Phase-1-Architecture/project-skeleton

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```

### 2. 访问服务

| 服务 | URL | 默认凭据 |
|------|-----|---------|
| Flink Web UI | <http://localhost:8081> | - |
| Grafana | <http://localhost:3000> | admin / flink-iot-grafana |
| EMQX Dashboard | <http://localhost:18083> | admin / public |
| Prometheus | <http://localhost:9090> | - |
| InfluxDB | <http://localhost:8086> | admin / flink-iot-2024 |

### 3. 停止服务

```bash
# 停止所有服务
docker-compose down

# 停止并删除数据卷
docker-compose down -v
```

---

## 项目结构

```
project-skeleton/
├── docker-compose.yml          # 核心: 一键启动所有服务
├── flink-sql/                  # Flink SQL 脚本
│   ├── 01-create-tables.sql    # 建表语句 (Source/Sink)
│   ├── 02-ingestion.sql        # 数据摄取逻辑
│   ├── 03-watermark.sql        # 时间语义配置 (30s延迟)
│   └── 04-queries.sql          # 7个查询示例
├── mock-data/                  # 模拟数据生成
│   ├── sensor-generator.py     # Python数据生成器
│   └── device-registry.json    # 100台设备注册表
├── prometheus/                 # 监控配置
│   ├── prometheus.yml          # Prometheus配置
│   ├── grafana-datasources.yml # Grafana数据源
│   ├── grafana-dashboards.yml  # Grafana仪表板配置
│   ├── flink-dashboard.json    # Flink集群监控
│   └── iot-dashboard.json      # IoT传感器监控
└── README.md                   # 本文件
```

---

## 服务架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        Data Sources                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Sensors  │  │  MQTT    │  │  Kafka   │  │  Batch   │        │
│  │(Mock Gen)│  │  (EMQX)  │  │ (Broker) │  │ (Hist.)  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
└───────┼─────────────┼─────────────┼─────────────┼───────────────┘
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Apache Flink                               │
│  ┌─────────────────┐    ┌─────────────────┐                    │
│  │   JobManager    │◄──►│  TaskManager    │                    │
│  │  (调度/协调)     │    │  (数据处理)      │                    │
│  └─────────────────┘    └─────────────────┘                    │
│         │                        │                              │
│         ▼                        ▼                              │
│  ┌──────────────────────────────────────────────┐              │
│  │           Flink SQL Processing               │              │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐     │              │
│  │  │  清洗    │ │  窗口    │ │  关联    │     │              │
│  │  │  转换    │ │  聚合    │ │  告警    │     │              │
│  │  └──────────┘ └──────────┘ └──────────┘     │              │
│  └──────────────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   InfluxDB   │    │    Kafka     │    │    EMQX      │
│  (时序存储)   │    │  (告警Topic)  │    │ (实时通知)   │
└──────┬───────┘    └──────────────┘    └──────────────┘
       │
       ▼
┌──────────────┐    ┌──────────────┐
│   Grafana    │◄──►│  Prometheus  │
│  (可视化)     │    │   (指标)     │
└──────────────┘    └──────────────┘
```

---

## 使用指南

### 1. 启动数据生成器

数据生成器会自动随docker-compose启动，也可单独运行：

```bash
# 实时模式 (默认)
docker-compose up -d mock-data-generator

# 批量模式 (生成24小时历史数据)
docker-compose run -e BATCH_MODE=true mock-data-generator
```

### 2. 执行Flink SQL

```bash
# 进入Flink SQL客户端
docker-compose exec flink-jobmanager ./bin/sql-client.sh

# 在SQL客户端中执行脚本
SOURCE /opt/flink/sql-scripts/01-create-tables.sql;
SOURCE /opt/flink/sql-scripts/02-ingestion.sql;
SOURCE /opt/flink/sql-scripts/03-watermark.sql;
SOURCE /opt/flink/sql-scripts/04-queries.sql;
```

### 3. 查看Kafka数据

```bash
# 进入Kafka容器
docker-compose exec kafka bash

# 消费传感器数据
kafka-console-consumer --bootstrap-server localhost:9092 \
  --topic sensor-readings --from-beginning

# 查看Topic列表
kafka-topics --bootstrap-server localhost:9092 --list
```

### 4. 查询InfluxDB

```bash
# 进入InfluxDB容器
docker-compose exec influxdb bash

# 使用InfluxQL查询
influx -database sensor-data -username admin -password flink-iot-2024

# 或使用Flux查询
influx query 'from(bucket: "sensor-data") |> range(start: -1h)'
```

---

## Flink SQL 查询示例

### 示例1: 实时温度监控

```sql
-- 检测超过阈值的温度读数
SELECT
    device_id,
    location,
    temperature,
    event_time
FROM sensor_readings
WHERE temperature > 50 OR temperature < -20;
```

### 示例2: 5分钟窗口聚合

```sql
-- 每5分钟统计各区域平均温度
SELECT
    location,
    TUMBLE_START(event_time, INTERVAL '5' MINUTE) as window_start,
    AVG(temperature) as avg_temp,
    COUNT(*) as reading_count
FROM sensor_readings
GROUP BY location, TUMBLE(event_time, INTERVAL '5' MINUTE);
```

### 示例3: 设备健康检查

```sql
-- 检测设备离线（10分钟无数据）
SELECT
    device_id,
    MAX(event_time) as last_seen,
    TIMESTAMPDIFF(MINUTE, MAX(event_time), NOW()) as minutes_offline
FROM sensor_readings
GROUP BY device_id
HAVING TIMESTAMPDIFF(MINUTE, MAX(event_time), NOW()) > 10;
```

---

## 配置说明

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DEVICE_COUNT` | 模拟设备数量 | 100 |
| `MESSAGE_RATE` | 每秒消息数 | 10 |
| `OUT_OF_ORDER_PROBABILITY` | 乱序数据概率 | 0.05 |
| `BATCH_MODE` | 批量模式开关 | false |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka地址 | kafka:9092 |
| `MQTT_BROKER` | MQTT Broker地址 | emqx |

### 端口映射

| 端口 | 服务 | 说明 |
|------|------|------|
| 2181 | Zookeeper | 协调服务 |
| 9092, 29092 | Kafka | 消息队列 |
| 8081 | Flink JobManager | Flink Web UI |
| 6123 | Flink JobManager | RPC端口 |
| 1883 | EMQX | MQTT协议 |
| 18083 | EMQX | Dashboard |
| 8086 | InfluxDB | HTTP API |
| 3000 | Grafana | 可视化 |
| 9090 | Prometheus | 指标收集 |

---

## 监控与告警

### Grafana 仪表板

1. **Flink集群监控** (`flink-dashboard.json`)
   - JobManager/TaskManager状态
   - Checkpoint统计
   - 内存和CPU使用
   - Backpressure检测

2. **IoT传感器监控** (`iot-dashboard.json`)
   - 实时温度/压力/湿度
   - 设备在线状态
   - 告警历史
   - Kafka消费延迟

### Prometheus 指标

```bash
# 查看Flink指标
curl http://localhost:9249

# 查询Prometheus
curl 'http://localhost:9090/api/v1/query?query=flink_jobmanager_uptime_timeSeconds'
```

---

## 故障排查

### 常见问题

#### 1. Flink JobManager无法启动

```bash
# 检查日志
docker-compose logs flink-jobmanager

# 检查资源
docker stats flink-jobmanager
```

#### 2. Kafka连接失败

```bash
# 检查Kafka状态
docker-compose exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092

# 重新创建Topic
docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 \
  --create --if-not-exists --topic sensor-readings --partitions 3 --replication-factor 1
```

#### 3. 数据生成器不发送数据

```bash
# 检查日志
docker-compose logs -f mock-data-generator

# 手动运行测试
pip install kafka-python paho-mqtt
python mock-data/sensor-generator.py
```

### 健康检查

```bash
# 检查所有服务状态
docker-compose ps

# 检查健康状态
docker-compose exec flink-jobmanager curl -f http://localhost:8081/overview
docker-compose exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092
docker-compose exec influxdb curl -f http://localhost:8086/health
```

---

## 扩展开发

### 添加新的SQL查询

在 `flink-sql/` 目录下创建新的 `.sql` 文件：

```sql
-- 05-custom-analysis.sql
CREATE TEMPORARY VIEW my_analysis AS
SELECT ...;
```

### 自定义数据生成器

修改 `mock-data/sensor-generator.py`：

```python
# 添加新的传感器类型
SENSOR_PROFILES['MY_SENSOR'] = {
    'base_value': 100.0,
    'variation': 10.0
}
```

### 添加新的仪表板面板

编辑 `prometheus/iot-dashboard.json`，在 `panels` 数组中添加新面板配置。

---

## 技术规格

| 组件 | 版本 | 说明 |
|------|------|------|
| Apache Flink | 1.18 | 流处理引擎 |
| Apache Kafka | 7.5.0 | 消息队列 (Confluent) |
| EMQX | 5.4.0 | MQTT Broker |
| InfluxDB | 2.7 | 时序数据库 |
| Grafana | 10.2.0 | 可视化平台 |
| Prometheus | 2.48.0 | 指标收集 |

---

## 许可证

本项目属于 AnalysisDataFlow 项目的一部分，遵循项目统一许可证。

---

## 参考文档

- [Apache Flink 文档](https://nightlies.apache.org/flink/flink-docs-stable/)
- [Flink SQL 参考](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/sql/)
- [Kafka 文档](https://kafka.apache.org/documentation/)
- [EMQX 文档](https://www.emqx.io/docs/)
- [InfluxDB 文档](https://docs.influxdata.com/)

---

*Generated by Flink IoT Project Generator v1.0.0*
