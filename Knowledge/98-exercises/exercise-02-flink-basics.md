# 练习 02: Flink 基础编程

> 所属阶段: Knowledge | 前置依赖: [Flink/01-architecture-overview.md](../Flink/01-architecture-overview.md) | 形式化等级: L3

---

## 1. 学习目标

完成本练习后，你将能够：

- **Def-K-02-01**: 掌握 DataStream API 的核心操作（Transformation, Sink）
- **Def-K-02-02**: 理解 Flink 的并行度与分区策略
- **Def-K-02-03**: 能够设计简单的流处理拓扑
- **Def-K-02-04**: 掌握 Flink 本地开发与调试技巧

---

## 2. 预备知识

### 2.1 环境要求

- JDK 11 或更高版本
- Maven 3.8+ 或 Gradle 7+
- Flink 1.18+ (本地模式)
- 可选：Docker (用于 Flink 集群)

### 2.2 核心概念

| 概念 | 说明 | 常用API |
|------|------|---------|
| DataStream | 数据流抽象 | `env.fromElements()`, `env.fromSource()` |
| Transformation | 数据转换操作 | `map()`, `filter()`, `keyBy()`, `window()` |
| KeyedStream | 按键分区的流 | `keyBy(KeySelector)` |
| Window | 窗口操作 | `window(WindowAssigner)`, `aggregate()` |
| Sink | 数据输出 | `addSink(SinkFunction)` |

### 2.3 初始项目模板

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-streaming-java</artifactId>
    <version>1.18.0</version>
</dependency>
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-clients</artifactId>
    <version>1.18.0</version>
</dependency>
```

---

## 3. 练习题

### 3.1 理论题 (30分)

#### 题目 2.1: 并行度与分区 (10分)

**难度**: L3

给定以下 Flink 程序：

```java
DataStream<Event> stream = env
    .fromSource(kafkaSource, WatermarkStrategy.noWatermarks(), "Kafka")
    .setParallelism(4)
    .map(new DeserializeFunction())
    .setParallelism(4)
    .keyBy(Event::getUserId)
    .window(TumblingProcessingTimeWindows.of(Time.minutes(1)))
    .aggregate(new CountAggregate())
    .setParallelism(2);
```

请回答：

1. 各算子的并行度分别是多少？(2分)
2. `keyBy` 后数据如何在并行实例间分配？(3分)
3. 描述数据在该拓扑中的流转路径 (3分)
4. 为什么 aggregate 的并行度可以设为 2？(2分)

---

#### 题目 2.2: 窗口类型对比 (10分)

**难度**: L3

比较以下窗口类型，说明适用场景：

| 窗口类型 | 触发条件 | 适用场景 | 潜在问题 |
|----------|----------|----------|----------|
| Tumbling Window | | | |
| Sliding Window | | | |
| Session Window | | | |
| Global Window | | | |

请补充上表，并针对实时广告点击率统计场景，推荐最适合的窗口类型。

---

#### 题目 2.3: 状态类型选择 (10分)

**难度**: L3

Flink 提供了 ValueState, ListState, MapState, ReducingState, AggregatingState 等多种状态类型。

请回答：

1. 每种状态类型的适用场景 (5分)
2. 为以下场景选择最合适的状态类型 (5分)：
   - a) 统计每个用户的访问次数
   - b) 保存最近100条消息用于去重
   - c) 聚合每个设备的传感器数据
   - d) 维护用户购物车内容

---

### 3.2 编程题 (70分)

#### 题目 2.4: 实时词频统计 (15分)

**难度**: L3

实现一个从 Socket 读取文本、实时统计词频的 Flink 程序。

**要求**：

- 从 localhost:9999 读取文本流 (3分)
- 分词后统计每个单词的出现次数 (5分)
- 使用滚动窗口，每5秒输出一次统计结果 (4分)
- 结果打印到控制台 (3分)

**参考代码**：

```java
public class WordCount {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        // TODO: 实现数据源、转换、窗口和输出

        env.execute("Socket WordCount");
    }
}
```

---

#### 题目 2.5: 用户行为分析 (25分)

**难度**: L4

实现一个电商用户行为分析程序，处理用户点击流数据。

**输入数据格式**：

```json
{
  "userId": "u12345",
  "itemId": "i987",
  "category": "electronics",
  "action": "click",
  "timestamp": 1712345678000
}
```

**功能要求**：

1. 使用 Kafka 作为数据源 (5分)
2. 实时统计每分钟的各类别商品点击量 (7分)
3. 识别"热门商品"（1分钟内点击量 > 100）(7分)
4. 将结果写入 Kafka 不同 Topic (6分)

**扩展要求**：

- 使用 ProcessFunction 实现自定义逻辑
- 添加 Watermark 处理乱序数据

---

#### 题目 2.6: 温度监控告警系统 (20分)

**难度**: L4

实现一个 IoT 温度监控系统。

**需求**：

- 监控多个传感器的温度读数
- 检测连续异常（连续3次读数 > 阈值）
- 告警去重（同一传感器1分钟内只告警一次）
- 使用侧输出流 (SideOutput) 输出告警

**提示**：

- 使用 `ProcessFunction` 维护状态
- 使用 `Context.output()` 输出到侧流
- 考虑使用 `TimerService` 实现告警去重

---

#### 题目 2.7: 数据倾斜分析与优化 (10分)

**难度**: L4

给定以下问题代码：

```java
dataStream
    .keyBy(Event::getCategory)  // 假设 category 分布极不均匀
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .aggregate(new CountAggregate())
    .addSink(new MySink());
```

**任务**：

1. 分析潜在的数据倾斜问题 (3分)
2. 使用两阶段聚合优化该代码 (4分)
3. 解释优化原理 (3分)

---

## 4. 参考答案链接

| 题目 | 答案位置 | 补充说明 |
|------|----------|----------|
| 2.1 | [answers/02-flink-basics.md](./answers/02-flink-basics.md#21) | 含图示说明 |
| 2.2 | [answers/02-flink-basics.md](./answers/02-flink-basics.md#22) | 场景分析表 |
| 2.3 | [answers/02-flink-basics.md](./answers/02-flink-basics.md#23) | 状态类型对比 |
| 2.4 | [answers/02-code/WordCount.java](./answers/02-code/WordCount.java) | 完整实现 |
| 2.5 | [answers/02-code/UserBehaviorAnalysis.java](./answers/02-code/UserBehaviorAnalysis.java) | 含Kafka配置 |
| 2.6 | [answers/02-code/TemperatureMonitor.java](./answers/02-code/TemperatureMonitor.java) | 含测试数据生成 |
| 2.7 | [answers/02-code/SkewOptimization.java](./answers/02-code/SkewOptimization.java) | 两阶段聚合示例 |

---

## 5. 评分标准

### 总分分布

| 等级 | 分数区间 | 要求 |
|------|----------|------|
| S | 95-100 | 全部完成，代码规范，有优化设计 |
| A | 85-94 | 功能完整，无明显bug |
| B | 70-84 | 主要功能实现，少量问题 |
| C | 60-69 | 基本功能实现 |
| F | <60 | 无法运行或功能缺失 |

### 编程题评分细则

| 题目 | 分值 | 评分标准 |
|------|------|----------|
| 2.4 | 15 | 能正确运行，输出预期结果 |
| 2.5 | 25 | 功能完整 + 代码规范 + 扩展实现 |
| 2.6 | 20 | 状态管理正确 + 侧输出使用正确 |
| 2.7 | 10 | 优化思路正确 + 代码实现 |

### 代码规范要求

- 命名规范（类名大驼峰，变量小驼峰）
- 关键逻辑有注释
- 异常处理完善
- 使用 try-with-resources 或正确关闭资源

---

## 6. 进阶挑战 (Bonus)

完成以下任一任务可获得额外 10 分：

1. **性能测试**：对比不同并行度配置下的吞吐量和延迟
2. **自定义 Source**：实现一个模拟传感器数据的自定义 SourceFunction
3. **复杂事件处理**：使用 CEP 库实现订单超时检测

---

## 7. 参考资源


---

## 8. 可视化

### Flink 数据流拓扑示例

```mermaid
graph LR
    subgraph "Source"
        S1[Socket Source<br/>Parallelism: 1]
    end

    subgraph "Transformation"
        T1[FlatMap<br/>Split Words]
        T2[Map<br/>Word->(Word,1)]
        T3[KeyBy<br/>Word]
        T4[Window<br/>Tumbling 5s]
        T5[Sum<br/>Count]
    end

    subgraph "Sink"
        SK1[Print Sink]
    end

    S1 --> T1 --> T2 --> T3 --> T4 --> T5 --> SK1
```

---

*最后更新: 2026-04-02*
