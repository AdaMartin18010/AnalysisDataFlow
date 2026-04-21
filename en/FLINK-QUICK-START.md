# Flink Quick Start

> **Language**: English | **Source**: [Flink/01-concepts/FLINK-QUICK-START.md](../Flink/01-concepts/FLINK-QUICK-START.md) | **Last Updated**: 2026-04-21

---

## Prerequisites

- Java 11 or 17
- Maven or Gradle
- Docker (optional, for local cluster)

## 1. Create a Project

```bash
mvn archetype:generate \
  -DarchetypeGroupId=org.apache.flink \
  -DarchetypeArtifactId=flink-quickstart-java \
  -DarchetypeVersion=1.18.0 \
  -DgroupId=com.example \
  -DartifactId=streaming-job \
  -Dversion=1.0 \
  -Dpackage=com.example \
  -DinteractiveMode=false
```

## 2. Write Your First Job

```java
package com.example;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;

public class WordCount {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        DataStream<String> source = env
            .fromData("hello flink", "hello world", "flink streaming")
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<String>forMonotonousTimestamps()
            );

        source
            .flatMap((String value, Collector<String> out) -> {
                for (String word : value.split(" ")) {
                    out.collect(word);
                }
            })
            .map(word -> new Tuple2<>(word, 1))
            .keyBy(tuple -> tuple.f0)
            .window(TumblingEventTimeWindows.of(Time.seconds(5)))
            .sum(1)
            .print();

        env.execute("WordCount");
    }
}
```

## 3. Run Locally

```bash
# From project root
mvn clean package
flink run target/streaming-job-1.0.jar
```

## 4. Run with Docker

```bash
docker run -p 8081:8081 flink:1.18.0 standalone-job \
  --job-classname com.example.WordCount
```

## Next Steps

- [Checkpointing Deep Dive](flink-checkpoint-deep-dive.md)
- [State Backends](flink-state-backends.md)
- [Deployment Architectures](flink-deployment-architectures.md)

## References
