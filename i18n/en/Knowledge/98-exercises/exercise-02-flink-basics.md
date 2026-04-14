---
title: "Exercise 02: Flink Basic Programming"
translation_status: ai_translated_reviewed
source_version: v4.1
last_sync: "2026-04-15"
---

# Exercise 02: Flink Basic Programming

> Stage: Knowledge | Prerequisites: [Deployment Architecture](../../Flink/01-concepts/deployment-architectures.md) | Formalization Level: L3

---

## Table of Contents

- [Exercise 02: Flink Basic Programming](#exercise-02-flink-basic-programming)
  - [Table of Contents](#table-of-contents)
  - [1. Learning Objectives](#1-learning-objectives)
  - [2. Prerequisites](#2-prerequisites)
    - [2.1 Environment Requirements](#21-environment-requirements)
    - [2.2 Core Concepts](#22-core-concepts)
    - [2.3 Initial Project Template](#23-initial-project-template)
  - [3. Exercises](#3-exercises)
    - [3.1 Theory Questions (30 points)](#31-theory-questions-30-points)
      - [Question 2.1: Parallelism and Partitioning (10 points)](#question-21-parallelism-and-partitioning-10-points)
      - [Question 2.2: Window Type Comparison (10 points)](#question-22-window-type-comparison-10-points)
      - [Question 2.3: State Type Selection (10 points)](#question-23-state-type-selection-10-points)
    - [3.2 Programming Questions (70 points)](#32-programming-questions-70-points)
      - [Question 2.4: Real-time Word Count (15 points)](#question-24-real-time-word-count-15-points)
      - [Question 2.5: User Behavior Analysis (25 points)](#question-25-user-behavior-analysis-25-points)
      - [Question 2.6: Temperature Monitoring Alert System (20 points)](#question-26-temperature-monitoring-alert-system-20-points)
      - [Question 2.7: Data Skew Analysis and Optimization (10 points)](#question-27-data-skew-analysis-and-optimization-10-points)
  - [4. Answer Key Links](#4-answer-key-links)
  - [5. Grading Criteria](#5-grading-criteria)
    - [Score Distribution](#score-distribution)
    - [Programming Question Grading Rubric](#programming-question-grading-rubric)
    - [Code Style Requirements](#code-style-requirements)
  - [6. Advanced Challenge (Bonus)](#6-advanced-challenge-bonus)
  - [7. Reference Resources](#7-reference-resources)
  - [8. Visualizations](#8-visualizations)
    - [Flink Dataflow Topology Example](#flink-dataflow-topology-example)

## 1. Learning Objectives

After completing this exercise, you will be able to:

- **Def-K-02-01**: Master core DataStream API operations (Transformation, Sink)
- **Def-K-02-02**: Understand Flink's parallelism and partitioning strategies
- **Def-K-02-03**: Design simple stream processing topologies
- **Def-K-02-04**: Master Flink local development and debugging techniques

---

## 2. Prerequisites

### 2.1 Environment Requirements

- JDK 11 or higher
- Maven 3.8+ or Gradle 7+
- Flink 1.18+ (local mode)
- Optional: Docker (for Flink cluster)

### 2.2 Core Concepts

| Concept | Description | Common APIs |
|---------|-------------|-------------|
| DataStream | Data stream abstraction | `env.fromElements()`, `env.fromSource()` |
| Transformation | Data transformation operations | `map()`, `filter()`, `keyBy()`, `window()` |
| KeyedStream | Key-partitioned stream | `keyBy(KeySelector)` |
| Window | Window operations | `window(WindowAssigner)`, `aggregate()` |
| Sink | Data output | `addSink(SinkFunction)` |

### 2.3 Initial Project Template

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

## 3. Exercises

### 3.1 Theory Questions (30 points)

#### Question 2.1: Parallelism and Partitioning (10 points)

**Difficulty**: L3

Given the following Flink program:

```java

import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

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

Please answer:

1. What is the parallelism of each operator? (2 points)
2. How is data distributed among parallel instances after `keyBy`? (3 points)
3. Describe the data flow path in this topology (3 points)
4. Why can the parallelism of aggregate be set to 2? (2 points)

---

#### Question 2.2: Window Type Comparison (10 points)

**Difficulty**: L3

Compare the following window types and explain applicable scenarios:

| Window Type | Trigger Condition | Applicable Scenario | Potential Issue |
|-------------|-------------------|---------------------|-----------------|
| Tumbling Window | | | |
| Sliding Window | | | |
| Session Window | | | |
| Global Window | | | |

Please complete the above table, and for a real-time ad click-through rate statistics scenario, recommend the most suitable window type.

---

#### Question 2.3: State Type Selection (10 points)

**Difficulty**: L3

Flink provides multiple state types: ValueState, ListState, MapState, ReducingState, AggregatingState.

Please answer:

1. Applicable scenarios for each state type (5 points)
2. Select the most appropriate state type for the following scenarios (5 points):
   - a) Counting each user's visit count
   - b) Saving the most recent 100 messages for deduplication
   - c) Aggregating sensor data for each device
   - d) Maintaining user shopping cart contents

---

### 3.2 Programming Questions (70 points)

#### Question 2.4: Real-time Word Count (15 points)

**Difficulty**: L3

Implement a Flink program that reads text from a Socket and counts word frequencies in real time.

**Requirements**:

- Read text stream from localhost:9999 (3 points)
- Tokenize and count the occurrences of each word (5 points)
- Use tumbling window, output statistics every 5 seconds (4 points)
- Print results to console (3 points)

**Reference Code**:

```java
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.util.Collector;

/**
 * Real-time word count program
 *
 * Function: Read text stream from Socket, tokenize and count each word's occurrences,
 *           output statistics every 5 seconds
 *
 * Run steps:
 * 1. Open terminal and run: nc -lk 9999
 * 2. Start WordCount program
 * 3. Input text in nc terminal, e.g.: hello world hello flink
 * 4. Word frequency statistics will be printed to console every 5 seconds
 */
public class WordCount {
    public static void main(String[] args) throws Exception {
        // Create Flink stream processing execution environment
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        // Set parallelism to 1 for local testing, adjust according to cluster in production
        env.setParallelism(1);

        // ========== 1. Data Source: Read text stream from Socket ==========
        // Parameter description:
        // - "localhost": Socket server hostname
        // - 9999: Socket server port
        // Start command: nc -lk 9999 (Linux/Mac) or nc -l -p 9999 (Windows)
        DataStream<String> source = env.socketTextStream("localhost", 9999);

        // ========== 2. Data Transformation: Tokenize and convert to (word, 1) tuples ==========
        DataStream<Tuple2<String, Integer>> wordStream = source
            // Use FlatMap for tokenization: one line input may produce multiple word outputs
            .flatMap(new Tokenizer())
            // Name operator for easy identification in Web UI
            .name("Tokenizer: Split Words");

        // ========== 3. KeyBy and windowed statistics ==========
        DataStream<Tuple2<String, Integer>> windowed = wordStream
            // keyBy: Group by word, same words are assigned to the same parallel instance
            .keyBy(value -> value.f0)
            // window: Use tumbling window, windows do not overlap
            // A new window is created every 5 seconds, counting word frequency within that window
            .window(TumblingProcessingTimeWindows.of(Time.seconds(5)))
            // sum: Sum the second field of Tuple2 (count)
            .sum(1)
            .name("Windowed Word Count");

        // ========== 4. Output to console ==========
        // print() outputs results to stdout, can be replaced with other Sinks in production
        windowed.print().name("Print Sink");

        // Execute Flink job
        env.execute("Socket WordCount");
    }

    /**
     * Custom FlatMapFunction: Split input line into words
     *
     * FlatMapFunction<T, O>:
     * - T: Input type (String - one line of text)
     * - O: Output type (Tuple2<String, Integer> - (word, 1))
     */
    public static class Tokenizer implements FlatMapFunction<String, Tuple2<String, Integer>> {

        @Override
        public void flatMap(String value, Collector<Tuple2<String, Integer>> out) {
            // Split input line by non-word characters (regex: \\W+)
            // Convert to lowercase for case-insensitive counting
            String[] words = value.toLowerCase().split("\\W+");

            for (String word : words) {
                // Filter empty strings
                if (word.length() > 0) {
                    // Output (word, 1) tuple
                    out.collect(new Tuple2<>(word, 1));
                }
            }
        }
    }
}

// ==================== Maven Dependencies (pom.xml) ====================
/*
<dependencies>
    <!-- Flink Streaming API -->
    <dependency>
        <groupId>org.apache.flink</groupId>
        <artifactId>flink-streaming-java</artifactId>
        <version>1.18.0</version>
    </dependency>
    <!-- Flink Client (required for local execution) -->
    <dependency>
        <groupId>org.apache.flink</groupId>
        <artifactId>flink-clients</artifactId>
        <version>1.18.0</version>
    </dependency>
</dependencies>
*/

// ==================== Run Example ====================
/*
// Step 1: Start Socket server (Terminal 1)
$ nc -lk 9999

// Step 2: Run WordCount program (Terminal 2)
$ mvn exec:java -Dexec.mainClass="WordCount"

// Step 3: Input text in Socket server
hello world
hello flink
apache flink is great

// Step 4: Observe WordCount output (printed every 5 seconds)
4> (hello, 2)
4> (world, 1)
4> (flink, 1)
...
4> (apache, 1)
4> (flink, 2)
4> (is, 1)
4> (great, 1)
*/

// **Answer Key**: Complete WordCount implementation
/*
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.util.Collector;

public class WordCount {
    public static void main(String[] args) throws Exception {
        // Create execution environment
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(1); // Set to 1 for local testing, adjust for production

        // 1. Data Source: Read from Socket
        // Start command: nc -lk 9999
        DataStream<String> source = env.socketTextStream("localhost", 9999);

        // 2. Data Transformation: Tokenize and convert to (word, 1) tuples
        DataStream<Tuple2<String, Integer>> wordStream = source
            .flatMap(new Tokenizer())
            .name("tokenizer");

        // 3. KeyBy and window
        DataStream<Tuple2<String, Integer>> windowed = wordStream
            .keyBy(value -> value.f0)                    // Group by word
            .window(TumblingProcessingTimeWindows.of(Time.seconds(5))) // 5s tumbling window
            .sum(1)                                      // Sum second field
            .name("windowed-sum");

        // 4. Output to console
        windowed.print().name("print-sink");

        // Execute job
        env.execute("Socket WordCount");
    }

    // Custom FlatMapFunction: Tokenization
    public static class Tokenizer implements FlatMapFunction<String, Tuple2<String, Integer>> {
        @Override
        public void flatMap(String value, Collector<Tuple2<String, Integer>> out) {
            // Split input line by whitespace, filter empty strings
            for (String word : value.toLowerCase().split("\\s+")) {
                if (word.length() > 0) {
                    out.collect(new Tuple2<>(word, 1));
                }
            }
        }
    }
}

// Maven Dependencies (pom.xml):
/*
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
*/

// Run steps:
// 1. Open terminal and run: nc -lk 9999
// 2. Start WordCount program
// 3. Input text in nc terminal, e.g.: hello world hello flink
// 4. Word frequency statistics will be printed to console every 5 seconds
*/
```

---

#### Question 2.5: User Behavior Analysis (25 points)

**Difficulty**: L4

Implement an e-commerce user behavior analysis program that processes user clickstream data.

**Input Data Format**:

```json
{
  "userId": "u12345",
  "itemId": "i987",
  "category": "electronics",
  "action": "click",
  "timestamp": 1712345678000
}
```

**Functional Requirements**:

1. Use Kafka as the data source (5 points)
2. Real-time statistics of clicks per product category per minute (7 points)
3. Identify "hot items" (clicks > 100 within 1 minute) (7 points)
4. Write results to different Kafka topics (6 points)

**Extended Requirements**:

- Use ProcessFunction to implement custom logic
- Add Watermark to handle out-of-order data

---

#### Question 2.6: Temperature Monitoring Alert System (20 points)

**Difficulty**: L4

Implement an IoT temperature monitoring system.

**Requirements**:

- Monitor temperature readings from multiple sensors
- Detect continuous anomalies (3 consecutive readings > threshold)
- Alert deduplication (only one alert per sensor within 1 minute)
- Use SideOutput to output alerts

**Hints**:

- Use `ProcessFunction` to maintain state
- Use `Context.output()` to output to side stream
- Consider using `TimerService` to implement alert deduplication

---

#### Question 2.7: Data Skew Analysis and Optimization (10 points)

**Difficulty**: L4

Given the following problematic code:

```java

import org.apache.flink.streaming.api.windowing.time.Time;

dataStream
    .keyBy(Event::getCategory)  // Assume category distribution is extremely uneven
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .aggregate(new CountAggregate())
    .addSink(new MySink());
```

**Tasks**:

1. Analyze potential data skew issues (3 points)
2. Optimize the code using two-phase aggregation (4 points)
3. Explain the optimization principle (3 points)

---

## 4. Answer Key Links

| Question | Answer Location | Supplementary Notes |
|----------|-----------------|---------------------|
| 2.1 | **answers/02-flink-basics.md** (answer to be added) | Includes diagram explanation |
| 2.2 | **answers/02-flink-basics.md** (answer to be added) | Scenario analysis table |
| 2.3 | **answers/02-flink-basics.md** (answer to be added) | State type comparison |
| 2.4 | **answers/02-code/WordCount.java** (code example to be added) | Complete implementation |
| 2.5 | **answers/02-code/UserBehaviorAnalysis.java** (code example to be added) | Includes Kafka config |
| 2.6 | **answers/02-code/TemperatureMonitor.java** (code example to be added) | Includes test data generation |
| 2.7 | **answers/02-code/SkewOptimization.java** (code example to be added) | Two-phase aggregation example |

---

## 5. Grading Criteria

### Score Distribution

| Grade | Score Range | Requirement |
|-------|-------------|-------------|
| S | 95-100 | All completed, code is well-formatted, has optimization design |
| A | 85-94 | Functionally complete, no obvious bugs |
| B | 70-84 | Main functions implemented, minor issues |
| C | 60-69 | Basic functions implemented |
| F | <60 | Cannot run or missing functions |

### Programming Question Grading Rubric

| Question | Points | Grading Criteria |
|----------|--------|------------------|
| 2.4 | 15 | Runs correctly, outputs expected results |
| 2.5 | 25 | Complete functions + code style + extended implementation |
| 2.6 | 20 | Correct state management + correct side output usage |
| 2.7 | 10 | Correct optimization idea + code implementation |

### Code Style Requirements

- Naming conventions (PascalCase for class names, camelCase for variables)
- Key logic has comments
- Exception handling is complete
- Use try-with-resources or properly close resources

---

## 6. Advanced Challenge (Bonus)

Complete any one of the following tasks to earn an extra 10 points:

1. **Performance Test**: Compare throughput and latency under different parallelism configurations
2. **Custom Source**: Implement a custom SourceFunction that simulates sensor data
3. **Complex Event Processing**: Use the CEP library to implement order timeout detection

---

## 7. Reference Resources


---

## 8. Visualizations

### Flink Dataflow Topology Example

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

*Last updated: 2026-04-02*
