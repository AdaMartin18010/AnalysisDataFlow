# Lab 2: Event Time 处理

> 所属阶段: Flink/Hands-on | 前置依赖: [Lab 1](./lab-01-first-flink-program.md) | 预计时间: 60分钟 | 形式化等级: L4

## 实验目标

- [x] 理解三种时间语义：Event Time、Processing Time、Ingestion Time
- [x] 掌握 Watermark 的工作原理
- [x] 学会处理乱序数据
- [x] 实现基于 Event Time 的窗口计算

## 前置知识

- Lab 1 的基本 Flink 程序结构
- 时间戳和时区基础
- 窗口的基本概念

## 环境准备

确保 Flink Playground 运行中：

```bash
cd tutorials/interactive/flink-playground
docker-compose ps
```

## 核心概念

### 三种时间语义

| 时间类型 | 定义 | 特点 | 适用场景 |
|---------|------|------|---------|
| Event Time | 事件实际发生时间 | 处理乱序数据，结果确定 | 日志分析、金融交易 |
| Processing Time | 数据被处理的时间 | 低延迟，不确定 | 实时监控、近似计算 |
| Ingestion Time | 数据进入Flink的时间 | 介于两者之间 | 需要一定顺序保证 |

### Watermark 机制

Watermark 是 Flink 处理乱序数据的核心机制，表示"所有时间戳小于等于该值的事件都已到达"。

## 实验步骤

### 步骤 1: 创建 Event Time 作业

```java
package com.example;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import java.time.Duration;

public class EventTimeExample {

    public static void main(String[] args) throws Exception {
        final StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(1);

        // 创建带有事件时间戳的数据源
        DataStream<SensorReading> readings = env
            .addSource(new SensorSource())
            // 分配时间戳和水印
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<SensorReading>forBoundedOutOfOrderness(
                        Duration.ofSeconds(5))  // 允许5秒乱序
                    .withTimestampAssigner((event, timestamp) -> event.timestamp)
            );

        // 按传感器ID分组,使用Event Time窗口
        DataStream<SensorResult> results = readings
            .keyBy(r -> r.sensorId)
            .window(TumblingEventTimeWindows.of(Time.minutes(1)))
            .aggregate(new AverageAggregate());

        results.print();
        env.execute("Event Time Example");
    }
}
```

### 步骤 2: 实现自定义数据源（带乱序数据）

```java
public static class SensorSource implements SourceFunction<SensorReading> {
    private volatile boolean isRunning = true;
    private volatile long currentTime = System.currentTimeMillis();

    @Override
    public void run(SourceContext<SensorReading> ctx) throws Exception {
        int i = 0;
        while (isRunning && i < 20) {
            long eventTime = currentTime + (i * 5000);

            // 模拟乱序:第5个数据延迟10秒
            if (i == 5) {
                eventTime -= 10000;
                System.out.println(">>> 生成延迟数据: event_time - 10s");
            }

            SensorReading reading = new SensorReading(
                "sensor_1",
                20 + Math.random() * 10,
                eventTime
            );

            System.out.println("生成: " + reading);
            ctx.collectWithTimestamp(reading, eventTime);

            // 发送水印
            ctx.emitWatermark(new org.apache.flink.api.common.eventtime.Watermark(
                eventTime - 5000
            ));

            Thread.sleep(1000);
            i++;
        }
    }

    @Override
    public void cancel() {
        isRunning = false;
    }
}
```

### 步骤 3: 处理延迟数据（侧输出）

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

// 定义侧输出标签
private static final OutputTag<SensorReading> lateDataTag =
    new OutputTag<SensorReading>("late-data"){};

// 主输出:正常窗口计算
SingleOutputStreamOperator<SensorResult> mainResult = readings
    .keyBy(r -> r.sensorId)
    .window(TumblingEventTimeWindows.of(Time.seconds(10)))
    .allowedLateness(Time.seconds(5))  // 允许5秒延迟
    .sideOutputLateData(lateDataTag)   // 超期数据输出到侧流
    .aggregate(new AverageAggregate());

// 获取延迟数据侧流
DataStream<SensorReading> lateData = mainResult.getSideOutput(lateDataTag);
lateData.print("LATE");
```

## 验证方法

- [ ] 理解 Event Time 和 Processing Time 的区别
- [ ] 能够解释 Watermark 的作用
- [ ] 作业正确处理了乱序数据
- [ ] 延迟数据被正确路由到侧输出

## 下一步

- [Lab 3: Window 聚合](./lab-03-window-aggregation.md)
- [Lab 4: 状态管理](./lab-04-state-management.md)

## 引用参考
