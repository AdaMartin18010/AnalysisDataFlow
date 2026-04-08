# 实验 1.1: 理解不同时间语义

> **所属模块**: 模块 1 - 流计算基础概念
> **预计用时**: 45分钟
> **难度等级**: ★★☆☆☆

## 实验目标

1. 理解 Event Time、Processing Time 和 Ingestion Time 的区别
2. 观察不同时间语义下窗口计算结果的差异
3. 掌握如何在 Flink 中配置时间语义

## 前置要求

- 已完成环境搭建（Java 8+, Flink 1.18+）
- 了解基本 DataStream API 操作

## 实验环境

```xml
<!-- pom.xml 依赖 -->
<dependencies>
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
</dependencies>
```

## 实验内容

### 任务 1: Processing Time 窗口

**目标**: 使用 Processing Time 进行 5 秒滚动窗口统计

**代码框架**:

```java
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;

public class ProcessingTimeExample {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        // 使用 Processing Time（默认）
        env.setStreamTimeCharacteristic(TimeCharacteristic.ProcessingTime);

        // 创建模拟数据流
        DataStream<String> stream = env.socketTextStream("localhost", 9999);

        // TODO: 实现数据处理逻辑
        // 1. 将输入转换为 (word, 1) 格式
        // 2. 按 word 分组
        // 3. 使用 5 秒 Processing Time 窗口
        // 4. 统计每个单词出现次数

        env.execute("Processing Time Example");
    }
}
```

**实现提示**:

```java
stream
    .map(new MapFunction<String, Tuple2<String, Integer>>() {
        @Override
        public Tuple2<String, Integer> map(String value) {
            return Tuple2.of(value, 1);
        }
    })
    .keyBy(value -> value.f0)
    .window(TumblingProcessingTimeWindows.of(Time.seconds(5)))
    .sum(1)
    .print();
```

**测试步骤**:

1. 启动 netcat 模拟数据源:

   ```bash
   nc -lk 9999
   ```

2. 运行程序

3. 在 netcat 中输入单词（快速连续输入相同单词，然后等待 5 秒）

4. 观察输出结果

**思考问题**:

- 如果在 5 秒窗口内连续输入 "hello" 5 次，输出是什么？
- 如果停顿 5 秒后再输入，窗口如何变化？

---

### 任务 2: Event Time 窗口

**目标**: 使用 Event Time 进行窗口统计，理解 Watermark 的作用

**代码框架**:

```java
import org.apache.flink.streaming.api.TimeCharacteristic;
import org.apache.flink.streaming.api.functions.timestamps.BoundedOutOfOrdernessTimestampExtractor;
import org.apache.flink.streaming.api.windowing.time.Time;

public class EventTimeExample {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        // 设置为 Event Time
        env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime);

        DataStream<String> stream = env.socketTextStream("localhost", 9999);

        // TODO: 实现 Event Time 处理
        // 1. 解析输入，提取时间戳（格式: word,timestamp）
        // 2. 分配 Watermark（允许 2 秒乱序）
        // 3. 使用 5 秒 Event Time 窗口
        // 4. 观察乱序数据的处理

        env.execute("Event Time Example");
    }
}
```

**输入数据格式**:

```
hello,1000
world,2000
hello,1500  // 乱序数据
flink,6000
```

**实现提示**:

```java
stream
    .map(line -> {
        String[] parts = line.split(",");
        return Tuple3.of(parts[0], Long.parseLong(parts[1]), 1);
    })
    .assignTimestampsAndWatermarks(
        new BoundedOutOfOrdernessTimestampExtractor<
            Tuple3<String, Long, Integer>>(Time.seconds(2)) {
            @Override
            public long extractTimestamp(Tuple3<String, Long, Integer> element) {
                return element.f1;
            }
        }
    )
    .keyBy(value -> value.f0)
    .window(TumblingEventTimeWindows.of(Time.seconds(5)))
    .sum(2)
    .print();
```

**测试场景**:

1. 输入以下数据（模拟 0-5 秒窗口的乱序数据）:

   ```
   a,1000
   b,2000
   a,4000
   b,1000  // 乱序到达
   ```

2. 输入 Watermark 推进数据（时间戳 >= 5000）触发窗口计算:

   ```
   c,5000
   ```

**思考问题**:

- 乱序的 b,1000 是否被正确统计？
- 如果延迟超过 2 秒（Watermark 边界）会怎样？

---

### 任务 3: 对比分析

**目标**: 对比三种时间语义的结果差异

**实验设计**:

准备以下测试数据（相同输入，三种时间语义）:

```
输入序列（按输入顺序）:
1. "hello" (业务时间: 00:00:01)
2. "hello" (业务时间: 00:00:03)
3. "world" (业务时间: 00:00:02)
4. "hello" (业务时间: 00:00:01)  // 延迟到达
5. "world" (业务时间: 00:00:06)
```

**预期结果对比**:

| 时间语义 | hello 计数 | world 计数 | 说明 |
|----------|------------|------------|------|
| Processing Time | ? | ? | 按输入顺序统计 |
| Ingestion Time | ? | ? | 按到达 Flink 顺序 |
| Event Time | 3 | 1 | 按业务时间，延迟数据被正确处理 |

**任务**:

1. 分别实现三种时间语义的版本
2. 记录并对比输出结果
3. 分析差异原因

## 实验报告模板

```markdown
# 实验 1.1 报告

## 基本信息
- 姓名: ______
- 日期: ______
- 用时: ______

## 任务 1 结果
- 代码是否运行成功: [是/否]
- 5 秒窗口内输入 5 次 "hello" 的输出: ______
- 思考回答: ______

## 任务 2 结果
- Event Time 配置是否成功: [是/否]
- 乱序数据 b,1000 是否被统计: [是/否]
- 原因分析: ______

## 任务 3 结果

### Processing Time 输出
```

[粘贴输出]

```

### Event Time 输出
```

[粘贴输出]

```

### 差异分析
1. 差异点: ______
2. 原因: ______
3. 适用场景: ______

## 总结
- 时间语义选择建议: ______
- 遇到的问题及解决: ______
```

## 参考答案

### 任务 1 思考回答

- 连续输入 5 次 "hello" 后输出: `(hello, 5)`
- 停顿 5 秒后，之前的窗口关闭，新窗口开始

### 任务 2 思考回答

- 乱序的 b,1000 会被正确统计，因为 Watermark 允许 2 秒乱序
- 如果延迟超过 2 秒，数据会被丢弃或发送到侧输出流

### 任务 3 差异分析

- **Processing Time**: hello=2, world=1（延迟到达的数据计入新窗口）
- **Event Time**: hello=3, world=1（按业务时间归到正确窗口）

## 扩展思考

1. 在金融交易场景中，应该使用哪种时间语义？为什么？
2. 如果数据完全没有时间戳，如何统计每 100 条数据的聚合？
3. Watermark 设置过大或过小会有什么影响？

---

[返回课程大纲 →](../syllabus-csa.md) | [下一实验: 窗口计算实践 →](./lab-02-window-basics.md)
