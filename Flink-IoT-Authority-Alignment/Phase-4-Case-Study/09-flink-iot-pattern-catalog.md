# Flink IoT 模式目录 - 快速参考手册

> 所属阶段: Flink-IoT-Authority-Alignment/Phase-4-Case-Study | 前置依赖: [01-flink-iot-architecture-patterns.md](./01-flink-iot-architecture-patterns.md) | 形式化等级: L3-L4 | 文档类型: 快速参考手册

---

## 目录

- [Flink IoT 模式目录 - 快速参考手册](#flink-iot-模式目录---快速参考手册)
  - [目录](#目录)
  - [1. 架构模式速查](#1-架构模式速查)
    - [1.1 架构模式对比表](#11-架构模式对比表)
    - [1.2 边缘-云架构决策树](#12-边缘-云架构决策树)
    - [1.3 架构模式代码模板](#13-架构模式代码模板)
  - [2. 摄取模式速查](#2-摄取模式速查)
    - [2.1 数据源对比表](#21-数据源对比表)
    - [2.2 MQTT摄取模式](#22-mqtt摄取模式)
    - [2.3 Kafka摄取模式](#23-kafka摄取模式)
    - [2.4 HTTP摄取模式](#24-http摄取模式)
  - [3. 处理模式速查](#3-处理模式速查)
    - [3.1 Window模式速查表](#31-window模式速查表)
    - [3.2 Window处理代码模板](#32-window处理代码模板)
    - [3.3 Join模式速查表](#33-join模式速查表)
    - [3.4 Join处理代码模板](#34-join处理代码模板)
    - [3.5 CEP模式匹配速查表](#35-cep模式匹配速查表)
    - [3.6 CEP处理代码模板](#36-cep处理代码模板)
  - [4. 存储模式速查](#4-存储模式速查)
    - [4.1 存储类型对比表](#41-存储类型对比表)
    - [4.2 时序数据库写入模式](#42-时序数据库写入模式)
    - [4.3 数据湖写入模式](#43-数据湖写入模式)
    - [4.4 OLAP写入模式](#44-olap写入模式)
  - [5. 监控模式速查](#5-监控模式速查)
    - [5.1 监控维度对比表](#51-监控维度对比表)
    - [5.2 Metrics配置模板](#52-metrics配置模板)
    - [5.3 日志监控配置](#53-日志监控配置)
    - [5.4 分布式追踪配置](#54-分布式追踪配置)
  - [6. SQL速查表](#6-sql速查表)
    - [6.1 Window函数速查](#61-window函数速查)
    - [6.2 常用SQL模板](#62-常用sql模板)
  - [7. 配置速查表](#7-配置速查表)
    - [7.1 并行度与资源配置](#71-并行度与资源配置)
    - [7.2 Checkpoint配置](#72-checkpoint配置)
    - [7.3 Watermark与事件时间配置](#73-watermark与事件时间配置)
    - [7.4 网络与反压配置](#74-网络与反压配置)
    - [7.5 RocksDB状态后端配置](#75-rocksdb状态后端配置)
    - [7.6 安全配置](#76-安全配置)
  - [8. 问题排查速查](#8-问题排查速查)
    - [8.1 常见问题速查表](#81-常见问题速查表)
    - [8.2 反压诊断流程](#82-反压诊断流程)
    - [8.3 Checkpoint故障排查](#83-checkpoint故障排查)
    - [8.4 数据倾斜解决方案](#84-数据倾斜解决方案)
    - [8.5 内存问题排查](#85-内存问题排查)
  - [9. 性能速查表](#9-性能速查表)
    - [9.1 性能指标参考值](#91-性能指标参考值)
    - [9.2 硬件配置参考](#92-硬件配置参考)
    - [9.3 调优检查清单](#93-调优检查清单)
  - [10. 工具推荐](#10-工具推荐)
    - [10.1 工具分类速查表](#101-工具分类速查表)
    - [10.2 工具选择决策树](#102-工具选择决策树)
    - [10.3 推荐技术栈组合](#103-推荐技术栈组合)
  - [引用参考](#引用参考)

## 1. 架构模式速查

### 1.1 架构模式对比表

| 模式 | 适用场景 | 核心特点 | 优点 | 缺点 | 复杂度 |
|------|---------|---------|------|------|--------|
| **边缘-云分层** | 超低延迟场景(<50ms) | 边缘预处理+云端聚合 | 极低延迟、带宽节省 | 部署复杂、运维困难 | ⭐⭐⭐⭐⭐ |
| **Lambda架构** | 批流一体、准确性要求高 | 批处理层+速度层+服务层 | 准确性高、容错强 | 代码重复、维护成本高 | ⭐⭐⭐⭐ |
| **Kappa架构** | 纯实时场景 | 流处理统一 | 架构简单、一致性强 | 重处理成本高、近似结果 | ⭐⭐⭐ |
| **云原生微服务** | 弹性伸缩场景 | 容器化部署 | 弹性好、可扩展 | 网络开销、复杂度高 | ⭐⭐⭐⭐ |
| **混合边缘架构** | 地理分布广、带宽受限 | 边缘推理+云端训练 | 离线可用、隐私保护 | 同步困难、版本管理 | ⭐⭐⭐⭐ |

### 1.2 边缘-云架构决策树

```
延迟要求 < 100ms?
├── 是 → 边缘-云分层架构
│        ├── 设备数据 < 1000条/秒 → 单机Flink Edge
│        └── 设备数据 >= 1000条/秒 → Flink Cluster on Edge
└── 否 → 云端集中处理
         ├── 需要批流一体 → Lambda架构
         └── 纯实时场景 → Kappa架构
```

### 1.3 架构模式代码模板

**边缘-云分层 - 边缘端代码:**

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

// 边缘端: 数据过滤与聚合
DataStream<SensorData> filtered = env
    .addSource(new MqttSource("tcp://edge-mqtt:1883", "sensors/+"))
    .filter(data -> data.temperature > 0 && data.temperature < 100)
    .keyBy(data -> data.sensorId)
    .window(TumblingProcessingTimeWindows.of(Time.seconds(10)))
    .aggregate(new AvgTemperatureAggregate());

// 压缩后发送到云端
filtered.addSink(new MqttSink("tcp://cloud-mqtt:1883", "aggregated/"));
```

**Lambda架构 - 批处理层 (历史数据):**

```java
// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
// 批处理层: 每日全量计算
ExecutionEnvironment batchEnv = ExecutionEnvironment.getExecutionEnvironment();
DataSet<HourlyStats> dailyStats = batchEnv
    .readTextFile("hdfs://data/history/" + date)
    .map(new ParseSensorData())
    .groupBy("sensorId")
    .reduceGroup(new ComputeDailyAggregate());
dailyStats.writeAsText("hdfs://results/daily/" + date);
```

**Lambda架构 - 速度层 (实时数据):**

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

// 速度层: 实时增量计算
DataStream<HourlyStats> realtimeStats = streamEnv
    .addSource(new KafkaSource<>("realtime-topic"))
    .keyBy(data -> data.sensorId)
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .aggregate(new RealtimeAggregate());
realtimeStats.addSink(new RedisSink<>("realtime-view"));
```

**Kappa架构 - 统一流处理:**

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

// Kappa: 所有数据通过流处理
DataStream<SensorData> allData = env
    .addSource(new KafkaSource<>("all-sensor-data"))
    .assignTimestampsAndWatermarks(
        WatermarkStrategy.<SensorData>forBoundedOutOfOrderness(Duration.ofSeconds(30))
            .withTimestampAssigner((event, timestamp) -> event.eventTime)
    );

// 实时视图
allData.keyBy(d -> d.sensorId)
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .aggregate(new SensorAggregate())
    .addSink(new PinotSink<>("realtime-table"));

// 重放历史数据时调整watermark
allData.filter(d -> d.isHistorical())
    .keyBy(d -> d.sensorId)
    .window(TumblingEventTimeWindows.of(Time.days(1)))
    .aggregate(new HistoricalAggregate())
    .addSink(new PinotSink<>("batch-table"));
```

---

## 2. 摄取模式速查

### 2.1 数据源对比表

| 数据源 | 协议/接口 | 吞吐量 | 延迟 | 适用场景 | 可靠性 |
|--------|----------|--------|------|---------|--------|
| **MQTT** | TCP/1883, TLS/8883 | 中等(10K-100K msg/s) | 低(<10ms) | 设备直连、边缘网关 | QoS 0/1/2 |
| **Kafka** | TCP/9092 | 高(百万级 msg/s) | 低(<5ms) | 大规模数据集成 | 高(多副本) |
| **HTTP REST** | HTTP/80, HTTPS/443 | 中等 | 中(50-200ms) | 移动应用、第三方集成 | 应用层保证 |
| **CoAP** | UDP/5683 | 低 | 极低(<5ms) | 受限设备、NB-IoT | 可选确认 |
| **File/S3** | HDFS/S3 API | 高(批量) | 高(分钟级) | 历史数据、日志归档 | 持久化存储 |
| **Database CDC** | Debezium/Canal | 中等 | 低(<100ms) | 业务数据同步 | 事务日志 |

### 2.2 MQTT摄取模式

**基础MQTT Source配置:**

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.datastream.DataStream;

Properties mqttProps = new Properties();
mqttProps.setProperty("brokerUrl", "tcp://mqtt.broker:1883");
mqttProps.setProperty("topic", "sensors/+/temperature");
mqttProps.setProperty("qos", "1");  // 至少一次
mqttProps.setProperty("clientId", "flink-mqtt-source-" + UUID.randomUUID());

DataStream<SensorReading> mqttStream = env
    .addSource(new FlinkMqttConsumer<>(
        mqttProps,
        new SensorDeserializationSchema()
    ))
    .name("MQTT Source")
    .uid("mqtt-source");
```

**MQTT Source - 多主题订阅:**

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.datastream.DataStream;

// 同时订阅多个主题
List<String> topics = Arrays.asList(
    "sensors/+/temperature",
    "sensors/+/humidity",
    "sensors/+/pressure",
    "alarms/+/critical"
);

DataStream<SensorReading> multiTopicStream = env
    .addSource(new FlinkMqttConsumer<>(
        "tcp://mqtt.broker:1883",
        topics,
        new SensorDeserializationSchema()
    ));

// 按主题路由
dataStream
    .process(new ProcessFunction<SensorReading, SensorReading>() {
        @Override
        public void processElement(SensorReading value, Context ctx,
                                   Collector<SensorReading> out) {
            String topic = value.getTopic();
            if (topic.contains("alarm")) {
                ctx.output(alarmsTag, value);
            } else {
                out.collect(value);
            }
        }
    });
```

**MQTT连接池与故障恢复:**

```java
// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
// 生产级MQTT配置
Properties prodMqttProps = new Properties();
prodMqttProps.setProperty("brokerUrl", "ssl://mqtt.secure:8883");
prodMqttProps.setProperty("connectionTimeout", "30");
prodMqttProps.setProperty("keepAliveInterval", "60");
prodMqttProps.setProperty("cleanSession", "false");  // 持久会话
prodMqttProps.setProperty("automaticReconnect", "true");
prodMqttProps.setProperty("maxInflight", "1000");
prodMqttProps.setProperty("ssl.protocol", "TLSv1.2");

// 证书配置
prodMqttProps.setProperty("ssl.ca.path", "/certs/ca.crt");
prodMqttProps.setProperty("ssl.cert.path", "/certs/client.crt");
prodMqttProps.setProperty("ssl.key.path", "/certs/client.key");
```

### 2.3 Kafka摄取模式

**基础Kafka Source (新API):**

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.datastream.DataStream;

KafkaSource<SensorReading> kafkaSource = KafkaSource.<SensorReading>builder()
    .setBootstrapServers("kafka:9092")
    .setTopics("sensor-data", "device-events")
    .setGroupId("flink-iot-consumer")
    .setStartingOffsets(OffsetsInitializer.earliest())
    .setValueOnlyDeserializer(new SensorDeserializationSchema())
    .build();

DataStream<SensorReading> kafkaStream = env.fromSource(
    kafkaSource,
    WatermarkStrategy.forBoundedOutOfOrderness(Duration.ofSeconds(30)),
    "Kafka Source"
);
```

**Kafka Source - 精确一次消费:**

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.CheckpointingMode;

KafkaSource<SensorReading> exactlyOnceSource = KafkaSource.<SensorReading>builder()
    .setBootstrapServers("kafka:9092")
    .setTopics("sensor-data")
    .setGroupId("flink-exactly-once")
    .setProperty("isolation.level", "read_committed")
    .setProperty("enable.idempotence", "true")
    .setStartingOffsets(OffsetsInitializer.committedOffsets(OffsetResetStrategy.EARLIEST))
    .setValueOnlyDeserializer(new SensorDeserializationSchema())
    .build();

// 启用检查点保证精确一次
checkpointConfig.enableExternalizedCheckpoints(
    ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION
);
env.enableCheckpointing(60000, CheckpointingMode.EXACTLY_ONCE);
```

**Kafka多分区处理:**

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.streaming.api.windowing.time.Time;

// 基于设备ID分区，保证同一设备数据顺序处理
DataStream<SensorReading> partitionedStream = kafkaStream
    .keyBy(reading -> reading.getDeviceId())
    .map(new RichMapFunction<SensorReading, SensorReading>() {
        private transient ValueState<DeviceStats> state;

        @Override
        public void open(Configuration parameters) {
            StateTtlConfig ttlConfig = StateTtlConfig
                .newBuilder(Time.hours(24))
                .setUpdateType(StateTtlConfig.UpdateType.OnCreateAndWrite)
                .setStateVisibility(StateTtlConfig.StateVisibility.NeverReturnExpired)
                .build();

            ValueStateDescriptor<DeviceStats> descriptor =
                new ValueStateDescriptor<>("device-stats", DeviceStats.class);
            descriptor.enableTimeToLive(ttlConfig);
            state = getRuntimeContext().getState(descriptor);
        }

        @Override
        public SensorReading map(SensorReading value) throws Exception {
            DeviceStats stats = state.value();
            if (stats == null) {
                stats = new DeviceStats();
            }
            stats.update(value);
            state.update(stats);
            return value;
        }
    });
```

### 2.4 HTTP摄取模式

**HTTP Source (Async I/O):**

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

// 使用AsyncFunction批量获取外部API数据
DataStream<DeviceConfig> deviceConfigs = sensorStream
    .keyBy(SensorReading::getDeviceId)
    .asyncWaitFor(
        new AsyncFunction<String, DeviceConfig>() {
            private transient AsyncHttpClient httpClient;

            @Override
            public void open(Configuration parameters) {
                httpClient = Dsl.asyncHttpClient(
                    Dsl.config()
                        .setMaxConnections(100)
                        .setMaxConnectionsPerHost(20)
                );
            }

            @Override
            public void asyncInvoke(String deviceId,
                                   ResultFuture<DeviceConfig> resultFuture) {
                httpClient.prepareGet("http://device-api/config/" + deviceId)
                    .execute(new AsyncCompletionHandler<Response>() {
                        @Override
                        public Response onCompleted(Response response) {
                            DeviceConfig config = parseConfig(response);
                            resultFuture.complete(Collections.singletonList(config));
                            return response;
                        }

                        @Override
                        public void onThrowable(Throwable t) {
                            resultFuture.completeExceptionally(t);
                        }
                    });
            }
        },
        Time.seconds(5),    // 超时
        100                 // 并发数
    );
```

**WebSocket Source (实时推送):**

```java
// 使用自定义SourceFunction接收WebSocket数据
public class WebSocketSource extends RichSourceFunction<SensorReading>
    implements CheckpointListener {

    private transient WebSocketClient wsClient;
    private volatile boolean isRunning = true;

    @Override
    public void run(SourceContext<SensorReading> ctx) throws Exception {
        wsClient = new WebSocketClient(new URI("wss://iot-api/stream")) {
            @Override
            public void onMessage(String message) {
                synchronized (ctx.getCheckpointLock()) {
                    ctx.collect(parseMessage(message));
                }
            }
        };
        wsClient.connect();

        while (isRunning) {
            Thread.sleep(100);
        }
    }

    @Override
    public void cancel() {
        isRunning = false;
        if (wsClient != null) {
            wsClient.close();
        }
    }
}
```

---

## 3. 处理模式速查

### 3.1 Window模式速查表

| Window类型 | 适用场景 | 触发条件 | 特点 | 代码示例 |
|------------|---------|---------|------|---------|
| **滚动窗口** | 固定时间统计 | 时间到达 | 不重叠、等大小 | `TUMBLE(event_time, INTERVAL '1' HOUR)` |
| **滑动窗口** | 平滑趋势分析 | 时间到达 | 可重叠、滑动步长 | `HOP(event_time, INTERVAL '5' MIN, INTERVAL '1' HOUR)` |
| **会话窗口** | 用户行为分析 | 活动间隙 | 动态大小、Gap触发 | `SESSION(event_time, INTERVAL '30' MINUTE)` |
| **计数窗口** | 批量处理 | 数量到达 | 按元素计数 | `countWindow(1000)` |
| **全局窗口** | 自定义触发 | 自定义 | 需要Trigger | `windowAll(GlobalWindows.create())` |
| **增量聚合** | 实时更新 | 每元素 | 内存高效 | `aggregate(new IncrementalAggregate())` |

### 3.2 Window处理代码模板

**滚动窗口 - 温度平均值:**

```java

import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.streaming.api.windowing.time.Time;

DataStream<AvgTemperature> avgTemp = sensorStream
    .keyBy(SensorReading::getSensorId)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .aggregate(new AverageAggregate())
    .name("5min-avg-temperature");

// AggregateFunction实现
public static class AverageAggregate implements
    AggregateFunction<SensorReading, TemperatureAcc, AvgTemperature> {

    @Override
    public TemperatureAcc createAccumulator() {
        return new TemperatureAcc(0.0, 0);
    }

    @Override
    public TemperatureAcc add(SensorReading value, TemperatureAcc accumulator) {
        return new TemperatureAcc(
            accumulator.sum + value.getTemperature(),
            accumulator.count + 1
        );
    }

    @Override
    public AvgTemperature getResult(TemperatureAcc acc) {
        return new AvgTemperature(acc.sum / acc.count, acc.count);
    }

    @Override
    public TemperatureAcc merge(TemperatureAcc a, TemperatureAcc b) {
        return new TemperatureAcc(a.sum + b.sum, a.count + b.count);
    }
}
```

**滑动窗口 - 移动平均:**

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

// 每小时计算过去24小时的移动平均
DataStream<MovingAverage> movingAvg = sensorStream
    .keyBy(SensorReading::getSensorId)
    .window(SlidingEventTimeWindows.of(Time.hours(24), Time.hours(1)))
    .aggregate(new MovingAverageAggregate());

// SQL版本
String sql = "SELECT " +
    "  sensor_id, " +
    "  HOP_START(event_time, INTERVAL '1' HOUR, INTERVAL '24' HOUR) as window_start, " +
    "  AVG(temperature) as avg_temp, " +
    "  COUNT(*) as sample_count " +
    "FROM sensor_readings " +
    "GROUP BY HOP(event_time, INTERVAL '1' HOUR, INTERVAL '24' HOUR), sensor_id";
tableEnv.executeSql(sql);
```

**会话窗口 - 设备活动分析:**

```java

import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

// 检测设备会话（30分钟无活动视为会话结束）
DataStream<DeviceSession> sessions = sensorStream
    .keyBy(SensorReading::getDeviceId)
    .window(EventTimeSessionWindows.withDynamicGap(
        (element) -> Time.minutes(30)
    ))
    .allowedLateness(Time.minutes(10))
    .sideOutputLateData(lateDataTag)
    .process(new SessionProcessFunction());

// ProcessWindowFunction获取完整窗口信息
public static class SessionProcessFunction extends
    ProcessWindowFunction<SensorReading, DeviceSession, String, TimeWindow> {

    @Override
    public void process(String deviceId, Context context,
                       Iterable<SensorReading> elements,
                       Collector<DeviceSession> out) {
        long start = context.window().getStart();
        long end = context.window().getEnd();

        double sum = 0;
        int count = 0;
        for (SensorReading r : elements) {
            sum += r.getTemperature();
            count++;
        }

        out.collect(new DeviceSession(
            deviceId,
            new Date(start),
            new Date(end),
            sum / count,
            count
        ));
    }
}
```

### 3.3 Join模式速查表

| Join类型 | 语义 | 适用场景 | 延迟容忍 | 代码模式 |
|----------|------|---------|---------|---------|
| **Interval Join** | 时间区间匹配 | 传感器校准、设备配对 | 有界 | `between(Time.minutes(-5), Time.minutes(5))` |
| **Window Join** | 同一窗口内匹配 | 批量关联 | 窗口边界 | `join(other).where().equalTo().window()` |
| **Temporal Join** | 版本表关联 | 设备信息补全 | 无限制 | `FOR SYSTEM_TIME AS OF` |
| **Lookup Join** | 维表查询 | 实时维度关联 | 网络延迟 | `lookupJoin()` |
| **Async Lookup** | 异步维表 | 高并发查询 | 超时控制 | `asyncLookup()` |

### 3.4 Join处理代码模板

**Interval Join - 传感器配对分析:**

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

// 匹配5分钟内发生的相关事件
DataStream<EnrichedReading> enriched = tempStream
    .keyBy(SensorReading::getLocationId)
    .intervalJoin(humidityStream.keyBy(SensorReading::getLocationId))
    .between(Time.minutes(-5), Time.minutes(5))
    .lowerBoundExclusive()
    .upperBoundExclusive()
    .process(new ProcessJoinFunction<SensorReading, SensorReading, EnrichedReading>() {
        @Override
        public void processElement(SensorReading temp, SensorReading humidity,
                                  Context ctx, Collector<EnrichedReading> out) {
            double heatIndex = calculateHeatIndex(
                temp.getValue(),
                humidity.getValue()
            );
            out.collect(new EnrichedReading(
                temp.getLocationId(),
                temp.getTimestamp(),
                heatIndex
            ));
        }
    });
```

**Temporal Join - 设备信息版本关联:**

```sql
-- 创建版本表 (设备信息历史版本)
CREATE TABLE device_info (
    device_id STRING,
    firmware_version STRING,
    location STRING,
    installation_date TIMESTAMP(3),
    PRIMARY KEY (device_id) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://db:5432/iot',
    'table-name' = 'device_versions'
);

-- Temporal Join: 关联读取时刻的设备版本
SELECT
    s.sensor_id,
    s.reading_value,
    d.firmware_version,
    d.location
FROM sensor_readings s
JOIN device_info FOR SYSTEM_TIME AS OF s.event_time d
ON s.sensor_id = d.device_id;
```

**Lookup Join - 实时维度补全:**

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

// 异步查找设备元数据
DataStream<EnrichedEvent> enriched = eventStream
    .asyncWaitFor(
        new AsyncFunction<SensorEvent, EnrichedEvent>() {
            private transient Cache<String, DeviceMetadata> cache;

            @Override
            public void open(Configuration parameters) {
                cache = Caffeine.newBuilder()
                    .maximumSize(10000)
                    .expireAfterWrite(Duration.ofMinutes(5))
                    .build();
            }

            @Override
            public void asyncInvoke(SensorEvent event,
                                   ResultFuture<EnrichedEvent> resultFuture) {
                DeviceMetadata metadata = cache.getIfPresent(event.getDeviceId());
                if (metadata != null) {
                    resultFuture.complete(Collections.singletonList(
                        new EnrichedEvent(event, metadata)
                    ));
                } else {
                    // 异步查询数据库
                    queryMetadataAsync(event.getDeviceId())
                        .thenAccept(m -> {
                            cache.put(event.getDeviceId(), m);
                            resultFuture.complete(Collections.singletonList(
                                new EnrichedEvent(event, m)
                            ));
                        });
                }
            }
        },
        Time.milliseconds(100),  // 超时时间
        100                      // 并发度
    );
```

### 3.5 CEP模式匹配速查表

| 模式类型 | 描述 | 使用场景 | 复杂度 |
|----------|------|---------|--------|
| **Sequence** | 严格顺序匹配 | 流程监控、状态机 | 低 |
| **FollowedBy** | 宽松跟随 | 事件依赖分析 | 低 |
| **Next** | 紧邻匹配 | 紧密关联事件 | 低 |
| **Within** | 时间限制 | 超时检测 | 低 |
| **OneOrMore** | 重复匹配 | 频繁事件检测 | 中 |
| **Times** | 指定次数 | 精确计数 | 中 |
| **Optional** | 可选模式 | 条件分支 | 中 |
| **Negation** | 否定模式 | 缺失事件检测 | 高 |

### 3.6 CEP处理代码模板

**温度异常模式检测:**

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

// 定义模式: 温度持续升高后骤降(可能设备故障)
Pattern<SensorReading, ?> tempAnomalyPattern = Pattern
    .<SensorReading>begin("rising")
    .where(new SimpleCondition<SensorReading>() {
        @Override
        public boolean filter(SensorReading r) {
            return r.getTemperature() > 50;
        }
    })
    .next("rising_more")
    .where(new SimpleCondition<SensorReading>() {
        @Override
        public boolean filter(SensorReading r) {
            return r.getTemperature() > 60;
        }
    })
    .within(Time.minutes(10))
    .next("sudden_drop")
    .where(new SimpleCondition<SensorReading>() {
        @Override
        public boolean filter(SensorReading r) {
            return r.getTemperature() < 30;
        }
    })
    .within(Time.minutes(5));

// 应用模式
PatternStream<SensorReading> patternStream = CEP.pattern(
    sensorStream.keyBy(SensorReading::getSensorId),
    tempAnomalyPattern
);

// 处理匹配结果
DataStream<Alert> alerts = patternStream
    .process(new PatternProcessFunction<SensorReading, Alert>() {
        @Override
        public void processMatch(
            Map<String, List<SensorReading>> match,
            Context ctx,
            Collector<Alert> out) {

            SensorReading first = match.get("rising").get(0);
            SensorReading last = match.get("sudden_drop").get(0);

            out.collect(new Alert(
                "TEMP_ANOMALY",
                first.getSensorId(),
                "Temperature anomaly detected: " +
                first.getTemperature() + " -> " + last.getTemperature(),
                ctx.timestamp()
            ));
        }
    });
```

**设备心跳缺失检测:**

```java
// 检测设备失联: 15分钟内没有心跳
Pattern<DeviceEvent, ?> offlinePattern = Pattern
    .<DeviceEvent>begin("last_heartbeat")
    .where(evt -> evt.getType().equals("HEARTBEAT"))
    .notFollowedBy("next_heartbeat")
    .where(evt -> evt.getType().equals("HEARTBEAT"))
    .within(Time.minutes(15));

// 超时检测需要特殊处理 - 使用ProcessFunction + Timer

import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.streaming.api.windowing.time.Time;

public class HeartbeatMonitor extends KeyedProcessFunction<String, DeviceEvent, Alert> {
    private ValueState<Long> lastHeartbeatState;

    @Override
    public void open(Configuration parameters) {
        lastHeartbeatState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("last-heartbeat", Long.class)
        );
    }

    @Override
    public void processElement(DeviceEvent event, Context ctx,
                              Collector<Alert> out) throws Exception {
        if (event.getType().equals("HEARTBEAT")) {
            lastHeartbeatState.update(ctx.timestamp());
            // 注册15分钟后的超时检测
            ctx.timerService().registerEventTimeTimer(
                ctx.timestamp() + TimeUnit.MINUTES.toMillis(15)
            );
        }
    }

    @Override
    public void onTimer(long timestamp, OnTimerContext ctx,
                       Collector<Alert> out) throws Exception {
        Long lastHeartbeat = lastHeartbeatState.value();
        if (lastHeartbeat != null &&
            timestamp - lastHeartbeat >= TimeUnit.MINUTES.toMillis(15)) {
            out.collect(new Alert(
                "DEVICE_OFFLINE",
                ctx.getCurrentKey(),
                "Device offline for > 15 minutes",
                timestamp
            ));
        }
    }
}
```

---

## 4. 存储模式速查

### 4.1 存储类型对比表

| 存储类型 | 代表产品 | 适用场景 | 查询模式 | 数据保留 | 吞吐量 |
|----------|---------|---------|---------|---------|--------|
| **时序数据库** | InfluxDB, TDengine | 传感器数据、指标 | 时间范围、降采样 | 可配置TTL | 极高 |
| **数据湖** | Iceberg, Hudi, Delta | 原始数据、归档 | 全表扫描、分析 | 永久 | 高 |
| **OLAP** | ClickHouse, Pinot | 实时分析、报表 | 复杂聚合、过滤 | 长期 | 高 |
| **键值存储** | Redis, HBase | 最新状态、缓存 | 点查 | 内存限制 | 极高 |
| **搜索引擎** | Elasticsearch | 日志、文本 | 全文检索 | 可配置 | 高 |
| **关系数据库** | PostgreSQL | 配置、元数据 | 事务查询 | 永久 | 中 |

### 4.2 时序数据库写入模式

**InfluxDB写入:**

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.datastream.DataStream;

// InfluxDB 2.x Sink
InfluxDBConfig influxConfig = InfluxDBConfig.builder()
    .url("http://influxdb:8086")
    .token("my-token")
    .org("my-org")
    .bucket("iot-bucket")
    .build();

DataStream<Point> points = sensorStream.map(reading ->
    Point.measurement("temperature")
        .addTag("sensor_id", reading.getSensorId())
        .addTag("location", reading.getLocation())
        .addField("value", reading.getTemperature())
        .time(reading.getTimestamp(), WritePrecision.MS)
);

points.addSink(new InfluxDBSink<>(influxConfig,
    (point, context) -> point,
    1000,   // 批量大小
    5000,   // 刷新间隔(ms)
    3       // 重试次数
));
```

**TDengine写入:**

```java
// TDengine批量写入
public class TDengineSink extends RichSinkFunction<SensorReading> {
    private Connection conn;
    private PreparedStatement pstmt;
    private List<SensorReading> buffer = new ArrayList<>();
    private static final int BATCH_SIZE = 1000;

    @Override
    public void open(Configuration parameters) throws Exception {
        Class.forName("com.taosdata.jdbc.TSDBDriver");
        conn = DriverManager.getConnection(
            "jdbc:TAOS://tdengine:6030/iot_db",
            "root",
            "taosdata"
        );
        pstmt = conn.prepareStatement(
            "INSERT INTO sensor_data VALUES (?, ?, ?, ?)"
        );
    }

    @Override
    public void invoke(SensorReading value, Context context) throws Exception {
        buffer.add(value);
        if (buffer.size() >= BATCH_SIZE) {
            flush();
        }
    }

    private void flush() throws SQLException {
        for (SensorReading r : buffer) {
            pstmt.setTimestamp(1, new Timestamp(r.getTimestamp()));
            pstmt.setString(2, r.getSensorId());
            pstmt.setDouble(3, r.getTemperature());
            pstmt.addBatch();
        }
        pstmt.executeBatch();
        buffer.clear();
    }
}
```

### 4.3 数据湖写入模式

**Apache Iceberg写入:**

```java
// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
// Flink SQL写入Iceberg
String createCatalog = "CREATE CATALOG iceberg_catalog WITH (" +
    "'type'='iceberg'," +
    "'catalog-type'='hive'," +
    "'uri'='thrift://hive-metastore:9083'," +
    "'warehouse'='s3://data-lake/warehouse/'" +
    ")";
tableEnv.executeSql(createCatalog);

String createTable = "CREATE TABLE iceberg_catalog.iot.sensor_data (" +
    "  sensor_id STRING," +
    "  event_time TIMESTAMP(3)," +
    "  temperature DOUBLE," +
    "  humidity DOUBLE," +
    "  WATERMARK FOR event_time AS event_time - INTERVAL '30' SECOND" +
    ") PARTITIONED BY (days(event_time))" +
    "WITH ('write_compression'='ZSTD')";
tableEnv.executeSql(createTable);

// 流式写入
tableEnv.executeSql("INSERT INTO iceberg_catalog.iot.sensor_data " +
    "SELECT * FROM kafka_sensor_stream");
```

**Apache Hudi写入 (带Compaction):**

```java
// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
// Hudi表配置
Map<String, String> hudiOptions = new HashMap<>();
hudiOptions.put(FlinkOptions.PATH.key(), "hdfs://data-lake/hudi/sensor_data");
hudiOptions.put(FlinkOptions.TABLE_TYPE.key(), "MERGE_ON_READ");
hudiOptions.put(FlinkOptions.OPERATION.key(), "upsert");
hudiOptions.put(FlinkOptions.PRECOMBINE_FIELD.key(), "event_time");
hudiOptions.put(FlinkOptions.RECORD_KEY_FIELD.key(), "sensor_id");
hudiOptions.put(FlinkOptions.PARTITION_PATH_FIELD.key(), "dt");
hudiOptions.put(FlinkOptions.COMPACTION_SCHEDULE_ENABLED.key(), "true");
hudiOptions.put(FlinkOptions.COMPACTION_DELTA_COMMITS.key(), "5");
hudiOptions.put(FlinkOptions.COMPACTION_TASKS.key(), "4");

// 写入
stream.createTemporaryTable("hudi_sensor",
    new HudiTableFactory().createHudiTable(hudiOptions));
tableEnv.executeSql("INSERT INTO hudi_sensor SELECT * FROM sensor_stream");
```

### 4.4 OLAP写入模式

**Apache Pinot写入:**

```java
// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
// Pinot实时摄取
PinotSinkFunction<GenericRow> pinotSink = new PinotSinkFunction<>(
    "sensor_data",
    new Schema.Parser().parse(pinotSchemaJson),
    new TableConfig.Builder(TableType.REALTIME)
        .setTimeColumnName("event_time")
        .setTimeType(TimeUnit.MILLISECONDS)
        .setSegmentPushType("APPEND")
        .setStreamConfigs(ImmutableMap.of(
            "streamType", "kafka",
            "stream.kafka.topic.name", "sensor-data",
            "stream.kafka.broker.list", "kafka:9092"
        ))
        .build(),
    PinotControllerConf.builder()
        .controllerHost("pinot-controller")
        .controllerPort("9000")
        .build()
);

sensorStream.map(r -> {
    GenericRow row = new GenericRow();
    row.putValue("sensor_id", r.getSensorId());
    row.putValue("event_time", r.getTimestamp());
    row.putValue("temperature", r.getTemperature());
    return row;
}).addSink(pinotSink);
```

**ClickHouse写入:**

```java
// ClickHouse JDBC批量写入
public class ClickHouseBatchSink extends RichSinkFunction<SensorReading> {
    private ClickHouseDataSource dataSource;
    private List<SensorReading> batch = new ArrayList<>();

    @Override
    public void open(Configuration parameters) {
        ClickHouseConfig config = new ClickHouseConfig();
        config.setHost("clickhouse");
        config.setPort(8123);
        config.setDatabase("iot");
        dataSource = new ClickHouseDataSource(config);
    }

    @Override
    public void invoke(SensorReading value, Context context) {
        batch.add(value);
        if (batch.size() >= 10000) {
            insertBatch();
        }
    }

    private void insertBatch() {
        String sql = "INSERT INTO sensor_data (event_time, sensor_id, temperature) " +
                    "VALUES (?, ?, ?)";
        try (Connection conn = dataSource.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            for (SensorReading r : batch) {
                stmt.setTimestamp(1, new Timestamp(r.getTimestamp()));
                stmt.setString(2, r.getSensorId());
                stmt.setDouble(3, r.getTemperature());
                stmt.addBatch();
            }
            stmt.executeBatch();
            batch.clear();
        } catch (SQLException e) {
            throw new RuntimeException("ClickHouse insert failed", e);
        }
    }
}
```

---

## 5. 监控模式速查

### 5.1 监控维度对比表

| 监控类型 | 数据来源 | 采集方式 | 存储 | 告警延迟 | 典型指标 |
|----------|---------|---------|------|---------|---------|
| **Metrics** | Flink Metric System | Push/Pull | Prometheus/InfluxDB | <30s | 吞吐量、延迟、水位线 |
| **Logs** | Flink + App Logs | Filebeat/Fluentd | ELK/Loki | 分钟级 | 错误日志、异常堆栈 |
| **Traces** | OpenTelemetry | Agent收集 | Jaeger/Zipkin | 秒级 | 端到端延迟、调用链 |
| **Health Checks** | REST Endpoint | 主动探测 | Prometheus Blackbox | <10s | 存活状态、响应时间 |

### 5.2 Metrics配置模板

**自定义Metrics:**

```java
public class MonitoredFunction extends RichMapFunction<SensorReading, SensorReading> {
    private transient Counter eventCounter;
    private transient Histogram processingTimeHist;
    private transient Gauge currentWatermarkGauge;
    private transient Meter throughputMeter;

    @Override
    public void open(Configuration parameters) {
        eventCounter = getRuntimeContext()
            .getMetricGroup()
            .counter("eventsProcessed");

        processingTimeHist = getRuntimeContext()
            .getMetricGroup()
            .histogram("processingTimeMs", new DropwizardHistogramWrapper(
                new com.codahale.metrics.Histogram(
                    new SlidingWindowReservoir(500)
                )
            ));

        currentWatermarkGauge = getRuntimeContext()
            .getMetricGroup()
            .gauge("currentWatermarkMs", new Gauge<Long>() {
                @Override
                public Long getValue() {
                    return currentWatermark;
                }
            });

        throughputMeter = getRuntimeContext()
            .getMetricGroup()
            .meter("throughputPerSecond");
    }

    @Override
    public SensorReading map(SensorReading value) {
        long startTime = System.currentTimeMillis();

        // 处理逻辑...

        eventCounter.inc();
        processingTimeHist.update(System.currentTimeMillis() - startTime);
        throughputMeter.markEvent();

        return value;
    }
}
```

**Prometheus Reporter配置:**

```yaml
# flink-conf.yaml
metrics.reporters: prom
metrics.reporter.prom.class: org.apache.flink.metrics.prometheus.PrometheusReporter
metrics.reporter.prom.port: 9249

# 关键指标暴露
metrics.scope.jm: "flink.jobmanager"
metrics.scope.tm: "flink.taskmanager"
metrics.scope.task: "flink.task"
```

**关键监控指标速查表:**

| 指标名称 | 类型 | 告警阈值 | 说明 |
|----------|------|---------|------|
| `records_in_per_second` | Meter | < 预期的80% | 输入吞吐量下降 |
| `records_out_per_second` | Meter | < records_in | 输出阻塞 |
| `checkpoint_duration` | Histogram | > 60s | 检查点耗时过长 |
| `checkpoint_size` | Gauge | > 1GB | 状态过大 |
| `numRecordsInBuffers` | Gauge | 持续增长 | 反压指示 |
| `currentOutputWatermark` | Gauge | 落后当前时间 > 5min | 数据延迟 |
| `numRestarts` | Counter | > 3次/小时 | 频繁重启 |
| `heap_used` | Gauge | > 80% | 内存不足 |

### 5.3 日志监控配置

**结构化日志输出:**

```java
// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
// Log4j2 JSON格式配置
// log4j2.properties
appender.json.type = RollingFile
appender.json.name = JsonFile
appender.json.fileName = ${sys:log.file}
appender.json.filePattern = ${sys:log.file}.%i
appender.json.layout.type = JsonTemplateLayout
appender.json.layout.eventTemplateUri = classpath:LogstashJsonEventLayoutV1.json
```

**Flink日志关联:**

```java
// 添加trace_id到MDC
public class TraceEnrichFunction extends RichMapFunction<Event, Event> {
    @Override
    public Event map(Event event) {
        MDC.put("trace_id", event.getTraceId());
        MDC.put("sensor_id", event.getSensorId());
        MDC.put("job_id", getRuntimeContext().getJobId().toString());

        logger.info("Processing event: {}", event.getEventId());

        MDC.clear();
        return event;
    }
}
```

### 5.4 分布式追踪配置

**OpenTelemetry集成:**

```java
// 初始化Tracer
OpenTelemetry openTelemetry = OpenTelemetrySdk.builder()
    .setTracerProvider(
        SdkTracerProvider.builder()
            .addSpanProcessor(
                BatchSpanProcessor.builder(
                    JaegerGrpcSpanExporter.builder()
                        .setEndpoint("http://jaeger:14250")
                        .build()
                ).build()
            )
            .build()
    )
    .build();

Tracer tracer = openTelemetry.getTracer("flink-iot-job");

// 在Flink算子中使用
public class TracedFunction extends RichMapFunction<Event, Event> {
    private transient Tracer tracer;

    @Override
    public void open(Configuration parameters) {
        tracer = getRuntimeContext().getDistributedTracingTracer();
    }

    @Override
    public Event map(Event event) {
        Span span = tracer.spanBuilder("process_event")
            .setAttribute("sensor.id", event.getSensorId())
            .setAttribute("event.type", event.getType())
            .startSpan();

        try (Scope scope = span.makeCurrent()) {
            // 处理逻辑
            return process(event);
        } catch (Exception e) {
            span.recordException(e);
            throw e;
        } finally {
            span.end();
        }
    }
}
```

---

## 6. SQL速查表

### 6.1 Window函数速查

| 操作 | SQL语法 | 说明 |
|------|---------|------|
| **滚动窗口** | `TUMBLE(event_time, INTERVAL '1' HOUR)` | 固定1小时窗口 |
| **滑动窗口** | `HOP(event_time, INTERVAL '5' MIN, INTERVAL '1' HOUR)` | 每小时窗口，每5分钟滑动 |
| **会话窗口** | `SESSION(event_time, INTERVAL '30' MINUTE)` | 30分钟间隙的会话 |
| **累积窗口** | `CUMULATE(event_time, INTERVAL '10' SECOND, INTERVAL '1' HOUR)` | 逐步累积窗口 |
| **Watermark** | `WATERMARK FOR event_time AS event_time - INTERVAL '30' SECOND` | 30秒延迟水位线 |

### 6.2 常用SQL模板

**滚动窗口聚合:**

```sql
-- 每小时传感器平均值
SELECT
    sensor_id,
    TUMBLE_START(event_time, INTERVAL '1' HOUR) as window_start,
    TUMBLE_END(event_time, INTERVAL '1' HOUR) as window_end,
    AVG(temperature) as avg_temp,
    MAX(temperature) as max_temp,
    MIN(temperature) as min_temp,
    COUNT(*) as sample_count
FROM sensor_readings
GROUP BY
    sensor_id,
    TUMBLE(event_time, INTERVAL '1' HOUR);
```

**滑动窗口趋势:**

```sql
-- 5分钟滑动窗口，1分钟步长 - 计算移动平均
SELECT
    sensor_id,
    HOP_START(event_time, INTERVAL '1' MINUTE, INTERVAL '5' MINUTE) as window_start,
    AVG(temperature) as moving_avg,
    STDDEV(temperature) as temp_stddev
FROM sensor_readings
GROUP BY
    sensor_id,
    HOP(event_time, INTERVAL '1' MINUTE, INTERVAL '5' MINUTE);
```

**Top-N per Group:**

```sql
-- 每个区域温度最高的3个传感器
SELECT sensor_id, location, avg_temp, rank_num
FROM (
    SELECT
        sensor_id,
        location,
        AVG(temperature) as avg_temp,
        ROW_NUMBER() OVER (PARTITION BY location ORDER BY AVG(temperature) DESC) as rank_num
    FROM sensor_readings
    GROUP BY sensor_id, location, TUMBLE(event_time, INTERVAL '1' HOUR)
)
WHERE rank_num <= 3;
```

**Stream Join:**

```sql
-- 传感器数据与设备元数据关联
SELECT
    s.sensor_id,
    s.temperature,
    d.location,
    d.firmware_version,
    d.installation_date
FROM sensor_readings s
JOIN device_metadata d
    ON s.sensor_id = d.sensor_id;
```

**Temporal Join (版本关联):**

```sql
-- 关联历史版本的设备信息
SELECT
    s.sensor_id,
    s.temperature,
    d.location,
    d.firmware_version
FROM sensor_readings s
JOIN device_metadata FOR SYSTEM_TIME AS OF s.event_time d
    ON s.sensor_id = d.sensor_id;
```

**Interval Join:**

```sql
-- 匹配时间接近的温湿度读数
SELECT
    t.sensor_id,
    t.temperature,
    h.humidity,
    t.event_time as temp_time,
    h.event_time as humidity_time
FROM temperature_stream t
JOIN humidity_stream h
    ON t.sensor_id = h.sensor_id
    AND t.event_time BETWEEN h.event_time - INTERVAL '5' MINUTE
                         AND h.event_time + INTERVAL '5' MINUTE;
```

**Pattern Match (CEP in SQL):**

```sql
-- SQL中的模式匹配 (需要启用MATCH_RECOGNIZE)
SELECT *
FROM sensor_readings
MATCH_RECOGNIZE (
    PARTITION BY sensor_id
    ORDER BY event_time
    MEASURES
        A.event_time as start_time,
        LAST(B.event_time) as end_time,
        A.temperature as start_temp,
        LAST(B.temperature) as end_temp
    ONE ROW PER MATCH
    PATTERN (A B+ C)
    DEFINE
        A AS temperature > 50,
        B AS temperature > A.temperature,
        C AS temperature < 30
) MR;
```

**迟到数据处理:**

```sql
-- 创建表时配置迟到数据处理
CREATE TABLE sensor_readings (
    sensor_id STRING,
    temperature DOUBLE,
    event_time TIMESTAMP(3),
    WATERMARK FOR event_time AS event_time - INTERVAL '30' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'sensor-data',
    'properties.group.id' = 'flink-sql-consumer',
    'late-data-throwable' = 'false',  -- 不丢弃迟到数据
    'late-data-table' = 'sensor_late_data'  -- 侧输出到单独表
);
```

---

## 7. 配置速查表

### 7.1 并行度与资源配置

| 参数 | 说明 | 推荐值 | 备注 |
|------|------|--------|------|
| `parallelism.default` | 默认并行度 | 8-16 | 根据TaskManager数量调整 |
| `taskmanager.numberOfTaskSlots` | 每个TM的槽位数 | 4-8 | 通常与CPU核数相同 |
| `jobmanager.memory.process.size` | JobManager内存 | 2048mb | 小规模作业 |
| `taskmanager.memory.process.size` | TaskManager内存 | 8192mb-32768mb | 根据状态大小调整 |
| `taskmanager.memory.managed.size` | 托管内存(RocksDB) | 40% of TM内存 | 状态大时增加 |
| `taskmanager.memory.network.max` | 网络缓冲区 | 256mb-512mb | 高吞吐时增加 |

### 7.2 Checkpoint配置

| 参数 | 说明 | 推荐值 | 备注 |
|------|------|--------|------|
| `execution.checkpointing.interval` | 检查点间隔 | 30s-1min | 平衡恢复时间与开销 |
| `execution.checkpointing.timeout` | 检查点超时 | 10min | 应大于interval |
| `execution.checkpointing.min-pause` | 最小间隔 | 30s | 防止连续checkpoint |
| `execution.checkpointing.max-concurrent` | 并发检查点 | 1 | 通常设为1 |
| `state.backend.incremental` | 增量checkpoint | true | 大状态时必需 |
| `state.checkpoints.num-retained` | 保留数量 | 10-20 | 根据存储成本调整 |
| `state.backend.local-recovery` | 本地恢复 | true | 加速恢复 |

### 7.3 Watermark与事件时间配置

| 参数 | 说明 | 推荐值 | 备注 |
|------|------|--------|------|
| `pipeline.auto-watermark-interval` | Watermark生成间隔 | 1s-5s | 影响延迟检测精度 |
| `execution.checkpointing.align-max-size` | 对齐超时阈值 | 1MB | 非对齐checkpoint时调整 |
| `table.exec.emit.early-fire.enabled` | 早期触发 | false | 需要低延迟时开启 |
| `table.exec.emit.late-fire.enabled` | 晚期触发 | true | 允许迟到数据更新 |
| `table.exec.state.ttl` | 状态TTL | 1h-24h | 根据业务需求 |

### 7.4 网络与反压配置

| 参数 | 说明 | 推荐值 | 备注 |
|------|------|--------|------|
| `taskmanager.memory.network.min` | 网络缓冲最小值 | 128mb | 低吞吐 |
| `taskmanager.memory.network.max` | 网络缓冲最大值 | 512mb | 高吞吐 |
| `web.backpressure.refresh-interval` | 反压检测间隔 | 60000 | 毫秒 |
| `taskmanager.network.memory.buffer-debloat.enabled` | 自动缓冲调整 | true | Flink 1.14+ |
| `taskmanager.network.memory.buffer-debloat.threshold-percentages` | 调整阈值 | 50,100 | 百分比 |

### 7.5 RocksDB状态后端配置

| 参数 | 说明 | 推荐值 | 备注 |
|------|------|--------|------|
| `state.backend.rocksdb.memory.managed` | 托管内存模式 | true | 自动管理 |
| `state.backend.rocksdb.predefined-options` | 预设配置 | FLASH_SSD_OPTIMIZED | SSD优化 |
| `state.backend.rocksdb.threads.threads-number` | 后台线程数 | 4-8 | 与CPU核数相关 |
| `state.backend.rocksdb.compaction.style` | 压缩策略 | LEVEL | 空间效率 |
| `state.backend.rocksdb.block.cache-size` | 块缓存大小 | 512mb | 读密集型增加 |
| `state.backend.incremental` | 增量快照 | true | 推荐开启 |

### 7.6 安全配置

| 参数 | 说明 | 推荐值 | 备注 |
|------|------|--------|------|
| `security.ssl.internal.enabled` | 内部通信加密 | true | 生产环境必需 |
| `security.ssl.rest.enabled` | REST API加密 | true | 生产环境必需 |
| `security.kerberos.login.keytab` | Kerberos Keytab | /path/to/keytab | Kerberos认证 |
| `security.kerberos.login.principal` | Kerberos主体 | <flink@EXAMPLE.COM> | Kerberos认证 |

---

## 8. 问题排查速查

### 8.1 常见问题速查表

| 问题现象 | 可能原因 | 诊断命令 | 解决方案 |
|----------|---------|---------|---------|
| **延迟高** | 反压、GC、网络慢 | `flink info`, GC日志 | 增加并行度、优化GC、扩容网络 |
| **Checkpoint失败** | 状态过大、超时、存储不可用 | Checkpoint详情页 | 增量checkpoint、增加超时、检查存储 |
| **OOM** | 状态过大、内存泄漏 | Heap Dump分析 | 使用RocksDB、调优JVM参数 |
| **数据丢失** | 未启用checkpoint、Kafka偏移 | Checkpoint配置 | 启用checkpoint、检查offset提交 |
| **重复数据** | 精确一次未配置、Source重放 | Sink配置 | 启用exactly-once、幂等写入 |
| **数据倾斜** | Key分布不均 | Web UI Subtasks | 加盐、重新分区、两阶段聚合 |
| **CPU过高** | 复杂计算、序列化开销 | Flame Graph | 优化算法、使用Avro/Protobuf |
| **网络超时** | 缓冲区不足、远程存储慢 | 网络监控 | 增加网络缓冲、检查存储性能 |
| **Kafka消费滞后** | 消费能力不足、分区不均 | Consumer Lag监控 | 增加消费者、检查分区分配 |
| **状态恢复慢** | 状态过大、网络慢 | 恢复日志 | 增量checkpoint、本地恢复 |

### 8.2 反压诊断流程

```
发现延迟高
    ↓
查看Web UI Backpressure → 红色(High)?
    ↓ 是
确定反压源 → 找第一个OK的算子,前一个即为瓶颈
    ↓
检查该算子的:
├── 并行度是否足够? → 增加parallelism
├── GC是否正常? → 查看GC日志,调优JVM
├── 是否有外部调用? → 使用Async I/O
├── 状态是否过大? → 使用RocksDB,调优状态访问
└── 数据是否倾斜? → 加盐重新分区
```

### 8.3 Checkpoint故障排查

**Checkpoint超时诊断:**

```bash
# 1. 查看Checkpoint详情
# Flink Web UI → Job → Checkpoints → History

# 2. 检查状态大小增长趋势
curl http://jobmanager:8081/jobs/<job-id>/checkpoints

# 3. 查看TaskManager日志
grep "Checkpoint" flink-taskmanager-*.log | tail -100
```

**解决方案代码:**

```java
// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
// 增加Checkpoint超时
env.enableCheckpointing(60000);
env.getCheckpointConfig().setCheckpointTimeout(600000);  // 10分钟

// 启用非对齐Checkpoint (减少反压时超时)
env.getCheckpointConfig().enableUnalignedCheckpoints();
env.getCheckpointConfig().setAlignmentTimeout(Duration.ofSeconds(30));

// 增量Checkpoint
env.setStateBackend(new EmbeddedRocksDBStateBackend(true));

// 本地恢复加速
configuration.setBoolean(StateBackendOptions.LOCAL_RECOVERY, true);
```

### 8.4 数据倾斜解决方案

**加盐两阶段聚合:**

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

// 第一阶段: 加盐打散
DataStream<AggregatedResult> phase1 = dataStream
    .map(new RichMapFunction<SensorReading, Tuple2<String, Double>>() {
        private Random random;

        @Override
        public void open(Configuration parameters) {
            random = new Random();
        }

        @Override
        public Tuple2<String, Double> map(SensorReading r) {
            String saltedKey = r.getSensorId() + "_" + random.nextInt(100);
            return Tuple2.of(saltedKey, r.getValue());
        }
    })
    .keyBy(t -> t.f0)
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .aggregate(new PartialAggregate());

// 第二阶段: 去盐聚合
DataStream<AggregatedResult> phase2 = phase1
    .map(t -> {
        String originalKey = t.f0.split("_")[0];
        return Tuple2.of(originalKey, t.f1);
    })
    .keyBy(t -> t.f0)
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .aggregate(new FinalAggregate());
```

### 8.5 内存问题排查

**JVM参数模板:**

```bash
# flink-conf.yaml
env.java.opts.taskmanager: >
  -Xms8g -Xmx8g
  -XX:+UseG1GC
  -XX:MaxGCPauseMillis=100
  -XX:+UnlockDiagnosticVMOptions
  -XX:+DebugNonSafepoints
  -XX:+PrintGCDetails
  -XX:+PrintGCDateStamps
  -Xloggc:/var/log/flink/gc.log
  -XX:+HeapDumpOnOutOfMemoryError
  -XX:HeapDumpPath=/var/log/flink/heapdump.hprof
```

**内存诊断命令:**

```bash
# 查看TaskManager内存使用
jmap -heap <taskmanager-pid>

# 生成Heap Dump
jmap -dump:live,format=b,file=heap.hprof <taskmanager-pid>

# 分析大对象
jhat -J-Xmx2g heap.hprof
# 或使用Eclipse MAT分析
```

---

## 9. 性能速查表

### 9.1 性能指标参考值

| 指标 | 良好 | 一般 | 差 | 优化建议 |
|------|------|------|----|---------|
| **吞吐量(单并行度)** | > 100K records/s | 50K-100K | < 50K | 检查序列化、减少状态访问 |
| **端到端延迟** | < 1s | 1-5s | > 5s | 减小缓冲区、调整watermark |
| **Checkpoint时长** | < 30s | 30s-2min | > 2min | 增量checkpoint、减少状态 |
| **GC暂停时间** | < 100ms | 100-500ms | > 500ms | 使用G1/ZGC、调优堆大小 |
| **CPU利用率** | 60-80% | 80-90% | > 90% | 增加并行度、优化计算 |
| **内存利用率** | 60-70% | 70-80% | > 80% | 增加内存、使用RocksDB |
| **反压频率** | 0% | < 5% | > 5% | 扩容、优化瓶颈算子 |
| **Kafka Lag** | 0 | < 1000 | > 1000 | 增加消费者、提高吞吐 |

### 9.2 硬件配置参考

| 规模 | TM数量 | TM规格 | JM规格 | 适用场景 |
|------|--------|--------|--------|---------|
| **小型** | 2-3 | 4核8GB | 2核4GB | 开发测试、<1000设备 |
| **中型** | 5-10 | 8核16GB | 4核8GB | 生产环境、<10K设备 |
| **大型** | 20-50 | 16核32GB | 8核16GB | 大规模、<100K设备 |
| **超大型** | 100+ | 32核64GB | 16核32GB | 海量数据、>100K设备 |

### 9.3 调优检查清单

**部署前检查:**

- [ ] 并行度 = TaskManager数量 × slots × 利用率(0.8)
- [ ] Checkpoint间隔 ≥ 处理延迟 × 2
- [ ] RocksDB内存 ≥ 状态大小 × 1.5
- [ ] 网络缓冲 ≥ 期望吞吐 × 平均记录大小 × 2
- [ ] Kafka分区数 ≥ Source并行度

**运行中监控:**

- [ ] 无持续反压(Backpressure = OK)
- [ ] Checkpoint成功率 > 95%
- [ ] GC暂停 < 200ms/次
- [ ] 内存利用率 < 80%
- [ ] CPU利用率 60-80%
- [ ] Kafka Lag 不持续增长

---

## 10. 工具推荐

### 10.1 工具分类速查表

| 类别 | 工具 | 用途 | 推荐场景 |
|------|------|------|---------|
| **MQTT Broker** | EMQX | 企业级MQTT | 大规模部署 |
| **MQTT Broker** | Mosquitto | 轻量级MQTT | 开发测试、边缘 |
| **MQTT Broker** | HiveMQ | 商业MQTT | 企业支持需求 |
| **消息队列** | Kafka | 流数据总线 | 大数据场景 |
| **消息队列** | Pulsar | 云原生MQ | 多租户、GEO复制 |
| **消息队列** | RabbitMQ | 通用消息 | 复杂路由需求 |
| **时序DB** | InfluxDB | 指标存储 | 监控数据 |
| **时序DB** | TimescaleDB | SQL时序 | 熟悉PostgreSQL |
| **时序DB** | TDengine | 国产时序 | 高性能写入 |
| **时序DB** | IoTDB | 物联网专用 | 设备管理一体 |
| **OLAP** | ClickHouse | 实时分析 | 海量数据查询 |
| **OLAP** | Apache Pinot | 实时OLAP | 低延迟查询 |
| **OLAP** | Apache Druid | 实时分析 | 复杂聚合 |
| **数据湖** | Apache Iceberg | 开放表格式 | Schema演进 |
| **数据湖** | Apache Hudi | 流式数据湖 | CDC场景 |
| **数据湖** | Delta Lake | ACID数据湖 | Databricks生态 |
| **监控** | Prometheus | 指标采集 | 云原生标配 |
| **监控** | Grafana | 可视化 | 仪表盘 |
| **监控** | Datadog | 商业监控 | 全托管需求 |
| **日志** | ELK Stack | 日志分析 | 全文检索 |
| **日志** | Loki | 轻量级日志 | 资源受限环境 |
| **追踪** | Jaeger | 分布式追踪 | OpenTelemetry |
| **追踪** | Zipkin | 分布式追踪 | 轻量级部署 |

### 10.2 工具选择决策树

```
MQTT Broker选择:
├── 设备数量 < 1000 → Mosquitto
├── 需要企业支持 → HiveMQ
├── 需要规则引擎 → EMQX
└── 需要集群高可用 → EMQX / HiveMQ

消息队列选择:
├── 需要极高吞吐 → Kafka
├── 需要多租户 → Pulsar
├── 需要复杂路由 → RabbitMQ
└── 需要云原生 → Pulsar

时序数据库选择:
├── 熟悉SQL → TimescaleDB
├── 需要极致写入 → TDengine
├── 需要云托管 → InfluxDB Cloud
└── 需要边缘部署 → InfluxDB Edge

OLAP选择:
├── 需要SQL兼容 → ClickHouse
├── 需要实时更新 → Pinot
├── 需要复杂分析 → Druid
└── 需要与Flink集成 → Pinot / Druid
```

### 10.3 推荐技术栈组合

**方案A: 开源全栈 (成本优化)**

- MQTT: EMQX Community
- 消息队列: Kafka
- 计算: Flink
- 时序DB: InfluxDB OSS / TDengine
- 数据湖: Iceberg on MinIO
- 监控: Prometheus + Grafana
- 日志: Loki + Grafana
- 追踪: Jaeger

**方案B: 企业级 (性能优化)**

- MQTT: HiveMQ / EMQX Enterprise
- 消息队列: Kafka / Pulsar
- 计算: Flink on K8s
- 时序DB: TimescaleDB / InfluxDB Enterprise
- 数据湖: Delta Lake on S3
- 监控: Datadog / New Relic
- 日志: Splunk / ELK Enterprise
- 追踪: Honeycomb

**方案C: 云原生 (运维简化)**

- MQTT: AWS IoT Core / Azure IoT Hub
- 消息队列: Confluent Cloud / AWS MSK
- 计算: Flink on managed K8s
- 时序DB: InfluxDB Cloud / AWS Timestream
- 数据湖: AWS Glue / Azure Synapse
- 监控: CloudWatch / Azure Monitor
- 日志: CloudWatch Logs / Azure Log Analytics
- 追踪: AWS X-Ray / Azure Application Insights

---

## 引用参考











---

*文档版本: 1.0 | 最后更新: 2026-04-05 | 形式化等级: L3-L4*
