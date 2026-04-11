package com.example.flink;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.*;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;

import java.time.Duration;
import java.time.Instant;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;

/**
 * Flink 窗口操作示例程序
 * 
 * 演示三种主要窗口类型：
 * 1. Tumbling Window (滚动窗口) - 固定大小，不重叠
 * 2. Sliding Window (滑动窗口) - 固定大小，可重叠
 * 3. Session Window (会话窗口) - 动态大小，由活动间隙决定
 * 
 * 运行方式：
 * 1. 本地运行: mvn compile exec:java -Dexec.mainClass="com.example.flink.WindowingExample" -Plocal
 * 2. 指定窗口类型: java -jar target/flink-windowing-1.0.0.jar [tumbling|sliding|session]
 * 
 * @author AnalysisDataFlow Project
 * @version 1.0.0
 */
public class WindowingExample {

    // 时间格式化器
    private static final DateTimeFormatter FORMATTER = 
        DateTimeFormatter.ofPattern("HH:mm:ss").withZone(ZoneId.systemDefault());

    public static void main(String[] args) throws Exception {
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(1); // 单并行度便于观察输出顺序

        // 解析窗口类型参数
        String windowType = args.length > 0 ? args[0].toLowerCase() : "tumbling";
        
        System.out.println("=================================");
        System.out.println("Flink窗口操作示例 - " + getWindowTypeName(windowType));
        System.out.println("=================================");

        // 创建模拟数据源 (温度传感器数据)
        DataStream<SensorReading> source = env.fromData(
            new SensorReading("sensor_1", Instant.now().toEpochMilli(), 25.5),
            new SensorReading("sensor_1", Instant.now().plusMillis(1000).toEpochMilli(), 26.0),
            new SensorReading("sensor_2", Instant.now().plusMillis(2000).toEpochMilli(), 30.0),
            new SensorReading("sensor_1", Instant.now().plusMillis(3000).toEpochMilli(), 26.5),
            new SensorReading("sensor_2", Instant.now().plusMillis(4000).toEpochMilli(), 31.0),
            new SensorReading("sensor_1", Instant.now().plusMillis(5000).toEpochMilli(), 27.0),
            new SensorReading("sensor_2", Instant.now().plusMillis(6000).toEpochMilli(), 29.5),
            new SensorReading("sensor_1", Instant.now().plusMillis(7000).toEpochMilli(), 27.5),
            new SensorReading("sensor_2", Instant.now().plusMillis(8000).toEpochMilli(), 30.5),
            new SensorReading("sensor_1", Instant.now().plusMillis(12000).toEpochMilli(), 28.0)
        );

        // 分配水印
        DataStream<SensorReading> withTimestamps = source.assignTimestampsAndWatermarks(
            WatermarkStrategy.<SensorReading>forBoundedOutOfOrderness(Duration.ofSeconds(2))
                .withTimestampAssigner((event, timestamp) -> event.timestamp)
                .withIdleness(Duration.ofSeconds(5))
        );

        // 根据窗口类型选择不同的窗口策略
        DataStream<Tuple2<String, Double>> result;
        
        switch (windowType) {
            case "sliding":
                result = applySlidingWindow(withTimestamps);
                break;
            case "session":
                result = applySessionWindow(withTimestamps);
                break;
            case "tumbling":
            default:
                result = applyTumblingWindow(withTimestamps);
                break;
        }

        // 输出结果
        result.print();

        env.execute("Flink Windowing Example - " + windowType);
    }

    /**
     * 应用滚动窗口：每5秒计算一次平均温度
     */
    private static DataStream<Tuple2<String, Double>> applyTumblingWindow(DataStream<SensorReading> stream) {
        System.out.println("使用 TumblingWindow: 窗口大小=5秒");
        System.out.println("每个窗口独立计算，窗口间不重叠");
        System.out.println();

        return stream
            .keyBy(reading -> reading.sensorId)
            .window(TumblingEventTimeWindows.of(Time.seconds(5)))
            .aggregate(new AverageAggregate());
    }

    /**
     * 应用滑动窗口：每2秒计算过去5秒的平均温度
     */
    private static DataStream<Tuple2<String, Double>> applySlidingWindow(DataStream<SensorReading> stream) {
        System.out.println("使用 SlidingWindow: 窗口大小=5秒, 滑动间隔=2秒");
        System.out.println("窗口之间会有重叠，用于计算移动平均");
        System.out.println();

        return stream
            .keyBy(reading -> reading.sensorId)
            .window(SlidingEventTimeWindows.of(Time.seconds(5), Time.seconds(2)))
            .aggregate(new AverageAggregate());
    }

    /**
     * 应用会话窗口：当3秒内没有新数据时触发计算
     */
    private static DataStream<Tuple2<String, Double>> applySessionWindow(DataStream<SensorReading> stream) {
        System.out.println("使用 SessionWindow: 会话间隔=3秒");
        System.out.println("动态窗口大小，由活动间隙决定");
        System.out.println();

        return stream
            .keyBy(reading -> reading.sensorId)
            .window(EventTimeSessionWindows.withGap(Time.seconds(3)))
            .aggregate(new AverageAggregate());
    }

    private static String getWindowTypeName(String type) {
        switch (type) {
            case "sliding": return "滑动窗口 (Sliding Window)";
            case "session": return "会话窗口 (Session Window)";
            default: return "滚动窗口 (Tumbling Window)";
        }
    }

    /**
     * 传感器读数数据类
     */
    public static class SensorReading {
        public String sensorId;
        public long timestamp;
        public double temperature;

        public SensorReading() {}

        public SensorReading(String sensorId, long timestamp, double temperature) {
            this.sensorId = sensorId;
            this.timestamp = timestamp;
            this.temperature = temperature;
        }

        @Override
        public String toString() {
            return String.format("SensorReading{%s, %s, %.1f°C}",
                sensorId,
                FORMATTER.format(java.time.Instant.ofEpochMilli(timestamp)),
                temperature);
        }
    }

    /**
     * 平均值聚合函数
     */
    public static class AverageAggregate implements AggregateFunction<SensorReading, AverageAggregate.Acc, Tuple2<String, Double>> {

        @Override
        public Acc createAccumulator() {
            return new Acc();
        }

        @Override
        public Acc add(SensorReading value, Acc accumulator) {
            accumulator.sensorId = value.sensorId;
            accumulator.sum += value.temperature;
            accumulator.count++;
            return accumulator;
        }

        @Override
        public Tuple2<String, Double> getResult(Acc accumulator) {
            double avg = accumulator.count == 0 ? 0.0 : accumulator.sum / accumulator.count;
            return new Tuple2<>(accumulator.sensorId, avg);
        }

        @Override
        public Acc merge(Acc a, Acc b) {
            a.sum += b.sum;
            a.count += b.count;
            return a;
        }

        public static class Acc {
            public String sensorId;
            public double sum = 0.0;
            public int count = 0;
        }
    }
}
