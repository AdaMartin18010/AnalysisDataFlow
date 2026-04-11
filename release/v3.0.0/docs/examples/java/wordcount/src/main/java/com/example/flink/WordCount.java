package com.example.flink;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.util.Collector;

/**
 * Flink WordCount 示例程序
 * 
 * 功能：从socket或内置数据流读取文本，统计单词频次
 * 
 * 运行方式：
 * 1. 本地运行: mvn compile exec:java -Dexec.mainClass="com.example.flink.WordCount" -Plocal
 * 2. 打包提交: mvn clean package -Plocal && flink run target/flink-wordcount-1.0.0.jar
 * 
 * @author AnalysisDataFlow Project
 * @version 1.0.0
 */
public class WordCount {

    public static void main(String[] args) throws Exception {
        // 创建执行环境
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        
        // 设置并行度
        env.setParallelism(2);
        
        // 创建数据源 - 使用内置数据流便于测试
        DataStream<String> source;
        
        if (args.length > 0 && "socket".equals(args[0])) {
            // 从socket读取 (需要先运行: nc -lk 9999)
            String hostname = args.length > 1 ? args[1] : "localhost";
            int port = args.length > 2 ? Integer.parseInt(args[2]) : 9999;
            System.out.println("从Socket读取数据: " + hostname + ":" + port);
            System.out.println("请先运行: nc -lk " + port);
            source = env.socketTextStream(hostname, port);
        } else {
            // 使用内置数据流进行演示
            System.out.println("使用内置数据流进行演示");
            System.out.println("如需从Socket读取，请运行: java -jar target/flink-wordcount-1.0.0.jar socket localhost 9999");
            source = env.fromData(
                "Hello Flink",
                "Hello World",
                "Flink is awesome",
                "Stream processing with Flink",
                "Hello Flink World",
                "Real-time analytics",
                "Flink rocks",
                "Hello again"
            );
        }

        // 数据流处理链
        DataStream<Tuple2<String, Integer>> wordCounts = source
            // 1. 分词处理
            .flatMap(new Tokenizer())
            // 2. 分配水印（允许2秒延迟）
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<Tuple2<String, Integer>>forMonotonousTimestamps()
                    .withIdleness(java.time.Duration.ofSeconds(2))
            )
            // 3. 按单词分组
            .keyBy(value -> value.f0)
            // 4. 5秒滚动窗口
            .window(TumblingProcessingTimeWindows.of(Time.seconds(5)))
            // 5. 求和
            .sum(1);

        // 输出结果到控制台
        wordCounts.print().setParallelism(1);

        // 执行程序
        System.out.println("=================================");
        System.out.println("WordCount程序已启动");
        System.out.println("=================================");
        env.execute("Flink WordCount Example");
    }

    /**
     * 分词器：将文本行拆分为单词
     */
    public static class Tokenizer implements FlatMapFunction<String, Tuple2<String, Integer>> {
        
        @Override
        public void flatMap(String value, Collector<Tuple2<String, Integer>> out) {
            // 转换为小写并按非单词字符分割
            String[] words = value.toLowerCase().split("\\W+");
            
            for (String word : words) {
                if (word.length() > 0) {
                    out.collect(new Tuple2<>(word, 1));
                }
            }
        }
    }
}
