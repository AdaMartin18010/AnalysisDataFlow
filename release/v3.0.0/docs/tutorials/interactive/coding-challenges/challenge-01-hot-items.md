# Challenge 1: 实时热门商品统计

> 难度: 初级 | 预计时间: 2小时 | 主题: Window、Aggregate

## 需求描述

实现一个实时热门商品统计系统，实时分析用户行为数据，统计最近一段时间内的热门商品。

### 功能需求

1. **实时统计**
   - 统计最近1小时内各商品的浏览次数
   - 每5分钟输出一次Top 10热门商品排行榜
   - 输出格式：排名、商品ID、浏览次数、窗口时间

2. **数据输入**
   - 商品浏览事件：`(userId, itemId, category, timestamp)`
   - 支持 Event Time 处理
   - 允许数据乱序（Watermark 处理）

3. **数据输出**
   - 控制台输出
   - 支持写入 Kafka/Redis

### 示例输入

```
user_001, item_100, electronics, 2024-01-15T10:00:00Z
user_002, item_100, electronics, 2024-01-15T10:01:00Z
user_003, item_101, clothing, 2024-01-15T10:02:00Z
user_001, item_102, electronics, 2024-01-15T10:03:00Z
...
```

### 示例输出

```
=== Top 10 Hot Items [10:00:00 - 10:05:00] ===
Rank 1: item_100 (Category: electronics) - 125 views
Rank 2: item_205 (Category: clothing) - 98 views
Rank 3: item_156 (Category: electronics) - 87 views
...
```

## 技术要点

### 核心概念

| 概念 | 说明 | 使用场景 |
|------|------|---------|
| Sliding Window | 滑动窗口 | 每5分钟输出最近1小时统计 |
| AggregateFunction | 增量聚合函数 | 高效计算商品浏览计数 |
| ProcessWindowFunction | 全量窗口函数 | 获取Top N排序结果 |

### 窗口设计

```
时间线:
[0:00]----[0:05]----[0:10]----[0:15]----[0:20]---->
 |___________|         滑动窗口 (size=1h, slide=5m)
      |___________|
           |___________|
```

## 实现步骤

### Step 1: 定义数据模型

```java
public class UserBehavior {
    public String userId;
    public String itemId;
    public String category;
    public long timestamp;

    // 构造方法、getter、setter
}

public class ItemViewCount {
    public String itemId;
    public String category;
    public long count;
    public long windowStart;
    public long windowEnd;

    // 构造方法、toString
}
```

### Step 2: 实现自定义 Source

```java
public class UserBehaviorSource implements SourceFunction<UserBehavior> {
    private volatile boolean isRunning = true;
    private Random random = new Random();

    private String[] users = {"user_001", "user_002", "user_003", ...};
    private String[] items = {"item_100", "item_101", "item_102", ...};
    private String[] categories = {"electronics", "clothing", "food", ...};

    @Override
    public void run(SourceContext<UserBehavior> ctx) throws Exception {
        while (isRunning) {
            UserBehavior behavior = new UserBehavior(
                users[random.nextInt(users.length)],
                items[random.nextInt(items.length)],
                categories[random.nextInt(categories.length)],
                System.currentTimeMillis()
            );

            ctx.collectWithTimestamp(behavior, behavior.timestamp);
            ctx.emitWatermark(new Watermark(behavior.timestamp - 5000));

            Thread.sleep(random.nextInt(100)); // 随机间隔
        }
    }

    @Override
    public void cancel() {
        isRunning = false;
    }
}
```

### Step 3: 实现计数聚合

```java
public class CountAggregate implements
    AggregateFunction<UserBehavior, Long, Long> {

    @Override
    public Long createAccumulator() {
        return 0L;
    }

    @Override
    public Long add(UserBehavior value, Long accumulator) {
        return accumulator + 1;
    }

    @Override
    public Long getResult(Long accumulator) {
        return accumulator;
    }

    @Override
    public Long merge(Long a, Long b) {
        return a + b;
    }
}
```

### Step 4: 实现 Top N 计算

```java
public class TopNItems extends ProcessWindowFunction<
    Long,                    // 输入类型 (AggregateFunction的输出)
    List<ItemViewCount>,     // 输出类型
    String,                  // Key 类型 (itemId)
    TimeWindow               // 窗口类型
> {

    private int topSize;

    public TopNItems(int topSize) {
        this.topSize = topSize;
    }

    @Override
    public void process(
            String itemId,
            Context context,
            Iterable<Long> elements,
            Collector<List<ItemViewCount>> out) {

        // 这里我们收集所有item的计数，然后排序
        // 注意：实际应该在keyBy之前做全局Top N
    }
}

// 更好的方式：使用 KeyedProcessFunction 实现全局 Top N
public class GlobalTopN extends KeyedProcessFunction<
    String,                  // Key (使用固定key如"top10")
    ItemViewCount,           // 输入
    String                   // 输出 (格式化的排行榜)
> {

    private int topSize;
    private ListState<ItemViewCount> itemState;

    @Override
    public void open(Configuration parameters) {
        itemState = getRuntimeContext().getListState(
            new ListStateDescriptor<>("items", ItemViewCount.class)
        );
    }

    @Override
    public void processElement(
            ItemViewCount value,
            Context ctx,
            Collector<String> out) throws Exception {
        itemState.add(value);

        // 注册定时器，在窗口结束时计算Top N
        ctx.timerService().registerEventTimeTimer(value.windowEnd + 1);
    }

    @Override
    public void onTimer(
            long timestamp,
            OnTimerContext ctx,
            Collector<String> out) throws Exception {

        List<ItemViewCount> allItems = new ArrayList<>();
        itemState.get().forEach(allItems::add);

        // 排序取Top N
        allItems.sort(Comparator.comparingLong(ItemViewCount::getCount).reversed());
        List<ItemViewCount> topN = allItems.subList(0, Math.min(topSize, allItems.size()));

        // 格式化输出
        StringBuilder result = new StringBuilder();
        result.append("\n=== Top ").append(topSize).append(" Hot Items ===\n");
        for (int i = 0; i < topN.size(); i++) {
            ItemViewCount item = topN.get(i);
            result.append(String.format(
                "Rank %d: %s (Category: %s) - %d views\n",
                i + 1, item.itemId, item.category, item.count
            ));
        }

        out.collect(result.toString());
        itemState.clear();
    }
}
```

### Step 5: 主程序

```java
public class HotItemsJob {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(1);

        // 创建数据流
        DataStream<UserBehavior> behaviorStream = env
            .addSource(new UserBehaviorSource())
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<UserBehavior>forBoundedOutOfOrderness(
                        Duration.ofSeconds(5))
                    .withTimestampAssigner((event, ts) -> event.timestamp)
            );

        // 统计窗口内各商品浏览量
        DataStream<ItemViewCount> windowedCounts = behaviorStream
            .keyBy(behavior -> behavior.itemId)
            .window(SlidingEventTimeWindows.of(
                Time.hours(1),   // 窗口大小
                Time.minutes(5)  // 滑动间隔
            ))
            .aggregate(
                new CountAggregate(),
                new WindowResultFunction()  // 添加窗口信息
            );

        // 全局Top N（使用固定key）
        windowedCounts
            .keyBy(count -> "top10")  // 所有数据到一个key
            .process(new GlobalTopN(10))
            .print();

        env.execute("Hot Items Statistics");
    }
}
```

## 验证方法

### 测试用例

```java
@Test
public void testHotItems() throws Exception {
    // 创建测试数据
    List<UserBehavior> testData = Arrays.asList(
        new UserBehavior("u1", "item_100", "elec", 1000L),
        new UserBehavior("u2", "item_100", "elec", 2000L),
        new UserBehavior("u3", "item_100", "elec", 3000L),
        new UserBehavior("u1", "item_101", "cloth", 4000L),
        new UserBehavior("u2", "item_101", "cloth", 5000L)
    );

    // 执行统计
    // 验证 item_100 排名高于 item_101
}
```

### 运行验证

```bash
# 1. 启动 Flink Playground
cd tutorials/interactive/flink-playground
docker-compose up -d

# 2. 编译打包
cd challenge-01-hot-items
mvn clean package

# 3. 提交作业
docker-compose exec jobmanager flink run \
  -c com.example.HotItemsJob \
  /jobs/challenge-01-hot-items-1.0.jar

# 4. 查看输出
docker-compose logs -f jobmanager
```

## 评分标准

| 维度 | 权重 | 要求 |
|------|------|------|
| 功能正确性 | 40% | 正确统计热门商品，输出Top 10 |
| 窗口使用 | 25% | 正确使用 Sliding Window |
| 代码质量 | 20% | 清晰的结构、注释、命名 |
| 测试 | 15% | 包含单元测试 |

## 扩展练习

### 扩展 1: 按类别统计

```java
// 每个类别输出独立的Top 10
behaviorStream
    .keyBy(behavior -> behavior.category)  // 按类别分组
    .window(...)
    .aggregate(...)
    .keyBy(count -> count.category)  // 每个类别一个key
    .process(new CategoryTopN(10));
```

### 扩展 2: 输出到 Redis

```java
// 使用 Flink-Redis Connector 或自定义 Sink
windowedCounts.addSink(new RedisSink<>(
    new FlinkJedisPoolConfig.Builder().setHost("redis").build(),
    new RedisMapper<ItemViewCount>() {
        @Override
        public String getKeyFromData(ItemViewCount data) {
            return "hot_items:" + data.windowStart;
        }

        @Override
        public String getValueFromData(ItemViewCount data) {
            return data.itemId + ":" + data.count;
        }

        @Override
        public RedisCommandDescription getCommandDescription() {
            return new RedisCommandDescription(RedisCommand.ZADD);
        }
    }
));
```

### 扩展 3: 历史趋势对比

```java
// 将当前窗口结果与上一窗口对比，输出增长最快的商品
public class TrendingItems extends CoProcessFunction<
    ItemViewCount,    // 当前窗口
    ItemViewCount,    // 上一窗口
    TrendResult
> {
    private ValueState<ItemViewCount> lastWindowState;

    @Override
    public void processElement1(
            ItemViewCount current,
            Context ctx,
            Collector<TrendResult> out) {

        ItemViewCount last = lastWindowState.value();
        if (last != null) {
            double growthRate = (double)(current.count - last.count) / last.count;
            out.collect(new TrendResult(current.itemId, growthRate));
        }
        lastWindowState.update(current);
    }

    // ...
}
```

## 参考解答

完整参考实现位于 `reference/challenge-01-hot-items/` 目录。

## 下一步

- [Challenge 2: 恶意登录检测](./challenge-02-login-detection.md)
