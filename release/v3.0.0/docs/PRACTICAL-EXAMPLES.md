# 流处理实践示例

> **Practical Examples for Stream Processing**

## 示例1: 实时WordCount

```java

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;

public class StreamingWordCount {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        // 从Socket读取数据
        DataStream<String> text = env.socketTextStream("localhost", 9999);

        // 分词并统计
        DataStream<Tuple2<String, Integer>> wordCounts = text
            .flatMap(new Tokenizer())
            .keyBy(0)
            .sum(1);

        wordCounts.print();
        env.execute("Streaming WordCount");
    }

    static class Tokenizer implements FlatMapFunction<String, Tuple2<String, Integer>> {
        @Override
        public void flatMap(String value, Collector<Tuple2<String, Integer>> out) {
            for (String word : value.split(" ")) {
                out.collect(new Tuple2<>(word, 1));
            }
        }
    }
}
```

## 示例2: 窗口聚合统计

```java

import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

// 每5分钟统计各品类销售额
DataStream<SalesRecord> sales = ...;

DataStream<CategoryStats> stats = sales
    .keyBy(SalesRecord::getCategory)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .aggregate(new SalesAggregator());
```

## 示例3: 双流Join

```java

import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

// 订单流与支付流Join
DataStream<Order> orders = ...;
DataStream<Payment> payments = ...;

DataStream<EnrichedOrder> enriched = orders
    .keyBy(Order::getOrderId)
    .intervalJoin(payments.keyBy(Payment::getOrderId))
    .between(Time.minutes(-5), Time.minutes(5))
    .process(new OrderPaymentJoin());
```

## 示例4: 模式检测（CEP）

```java

import org.apache.flink.streaming.api.windowing.time.Time;

// 检测登录异常：5分钟内3次失败登录
Pattern<LoginEvent, ?> loginFailPattern = Pattern
    .<LoginEvent>begin("first")
    .where(evt -> evt.getStatus().equals("FAIL"))
    .next("second")
    .where(evt -> evt.getStatus().equals("FAIL"))
    .next("third")
    .where(evt -> evt.getStatus().equals("FAIL"))
    .within(Time.minutes(5));

PatternStream<LoginEvent> patternStream = CEP.pattern(
    loginEvents.keyBy(LoginEvent::getUserId),
    loginFailPattern);
```

---

*Practical Examples - Phase 2*
