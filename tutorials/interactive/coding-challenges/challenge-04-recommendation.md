# Challenge 4: 实时推荐系统

> 难度: 高级 | 预计时间: 4小时 | 主题: Async IO、Join

## 需求描述

实现一个实时个性化推荐系统，根据用户实时行为结合用户画像生成推荐。

### 功能需求

1. **实时行为处理**
   - 收集用户点击、浏览、购买行为
   - 实时更新用户兴趣向量

2. **用户画像查询**
   - 异步查询用户历史偏好
   - 异步查询商品特征

3. **推荐生成**
   - 协同过滤推荐
   - 内容相似度推荐
   - 混合推荐排序

4. **推荐反馈**
   - 记录推荐展示和点击
   - A/B测试支持

## 数据结构

```java
public class UserBehavior {
    public String userId;
    public String itemId;
    public String behavior;   // VIEW / CLICK / BUY / RATE
    public double score;      // 评分或权重
    public long timestamp;
}

public class UserProfile {
    public String userId;
    public Map<String, Double> interests;  // 兴趣标签权重
    public List<String> recentItems;       // 最近交互商品
    public double[] embedding;             // 用户向量
}

public class ItemFeature {
    public String itemId;
    public String category;
    public List<String> tags;
    public double[] embedding;             // 商品向量
    public double price;
}

public class Recommendation {
    public String userId;
    public List<ScoredItem> items;
    public String algorithm;   // CF / CONTENT / HYBRID
    public long timestamp;
    public String abTestGroup;
}

public class ScoredItem {
    public String itemId;
    public double score;
    public String reason;      // 推荐理由
}
```

## 实现步骤

### Step 1: 异步查询用户画像

```java
import org.apache.flink.streaming.api.functions.async.AsyncFunction;

public class AsyncProfileRequest extends
    AsyncFunction<UserBehavior, EnrichedBehavior> {

    private transient UserProfileService profileService;

    @Override
    public void open(Configuration parameters) {
        profileService = new UserProfileService(
            "redis://localhost:6379"
        );
    }

    @Override
    public void asyncInvoke(
            UserBehavior behavior,
            ResultFuture<EnrichedBehavior> resultFuture) {

        CompletableFuture<UserProfile> profileFuture =
            profileService.getProfileAsync(behavior.userId);

        profileFuture.thenAccept(profile -> {
            EnrichedBehavior enriched = new EnrichedBehavior();
            enriched.behavior = behavior;
            enriched.profile = profile;
            resultFuture.complete(Collections.singletonList(enriched));
        }).exceptionally(throwable -> {
            // 失败时使用空画像
            EnrichedBehavior enriched = new EnrichedBehavior();
            enriched.behavior = behavior;
            enriched.profile = UserProfile.empty(behavior.userId);
            resultFuture.complete(Collections.singletonList(enriched));
            return null;
        });
    }

    @Override
    public void timeout(
            UserBehavior input,
            ResultFuture<EnrichedBehavior> resultFuture) {
        // 超时处理
        EnrichedBehavior enriched = new EnrichedBehavior();
        enriched.behavior = input;
        enriched.profile = UserProfile.empty(input.userId);
        resultFuture.complete(Collections.singletonList(enriched));
    }
}
```

### Step 2: 用户兴趣实时更新

```java
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;

import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;


public class InterestUpdater extends
    KeyedProcessFunction<String, EnrichedBehavior, UserProfile> {

    private ValueState<UserProfile> profileState;
    private ListState<String> recentItemsState;

    @Override
    public void open(Configuration parameters) {
        profileState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("profile", UserProfile.class)
        );
        recentItemsState = getRuntimeContext().getListState(
            new ListStateDescriptor<>("recentItems", String.class)
        );
    }

    @Override
    public void processElement(
            EnrichedBehavior enriched,
            Context ctx,
            Collector<UserProfile> out) throws Exception {

        UserProfile profile = profileState.value();
        if (profile == null) {
            profile = enriched.profile != null ? enriched.profile :
                new UserProfile(enriched.behavior.userId);
        }

        UserBehavior behavior = enriched.behavior;

        // 更新兴趣权重(基于行为类型)
        double weight = getBehaviorWeight(behavior.behavior);

        // 假设能从商品ID获取类别
        String category = getCategoryFromItem(behavior.itemId);
        if (category != null) {
            profile.interests.merge(category, weight * behavior.score, Double::sum);
        }

        // 更新最近交互
        recentItemsState.add(behavior.itemId);

        // 保持最近50个
        List<String> recent = new ArrayList<>();
        recentItemsState.get().forEach(recent::add);
        if (recent.size() > 50) {
            recent = recent.subList(recent.size() - 50, recent.size());
            recentItemsState.update(recent);
        }
        profile.recentItems = recent;

        // 更新用户向量(简化示例)
        updateUserEmbedding(profile);

        profileState.update(profile);
        out.collect(profile);
    }

    private double getBehaviorWeight(String behavior) {
        switch (behavior) {
            case "BUY": return 5.0;
            case "RATE": return 4.0;
            case "CART": return 3.0;
            case "CLICK": return 2.0;
            case "VIEW": return 1.0;
            default: return 0.5;
        }
    }
}
```

### Step 3: 协同过滤推荐

```java
public class CollaborativeFiltering extends
    BroadcastProcessFunction<UserProfile, ItemFeature, Recommendation> {

    // 广播状态存储所有商品特征
    private BroadcastState<String, ItemFeature> itemState;

    @Override
    public void open(Configuration parameters) {
        // 初始化
    }

    @Override
    public void processElement(
            UserProfile profile,
            ReadOnlyContext ctx,
            Collector<Recommendation> out) throws Exception {

        List<ScoredItem> recommendations = new ArrayList<>();

        // 遍历所有商品,计算相似度
        for (Map.Entry<String, ItemFeature> entry :
                ctx.getBroadcastState(...).immutableEntries()) {

            ItemFeature item = entry.getValue();

            // 跳过用户已交互的商品
            if (profile.recentItems.contains(item.itemId)) {
                continue;
            }

            // 计算向量相似度
            double similarity = cosineSimilarity(
                profile.embedding,
                item.embedding
            );

            if (similarity > 0.5) {  // 阈值
                recommendations.add(new ScoredItem(
                    item.itemId,
                    similarity,
                    "Collaborative Filtering"
                ));
            }
        }

        // 排序取Top N
        recommendations.sort(Comparator.comparingDouble(s -> -s.score));
        List<ScoredItem> topN = recommendations.subList(
            0, Math.min(10, recommendations.size())
        );

        Recommendation rec = new Recommendation();
        rec.userId = profile.userId;
        rec.items = topN;
        rec.algorithm = "CF";
        rec.timestamp = System.currentTimeMillis();

        out.collect(rec);
    }

    @Override
    public void processBroadcastElement(
            ItemFeature item,
            Context ctx,
            Collector<Recommendation> out) throws Exception {
        // 更新商品特征
        ctx.getBroadcastState(...).put(item.itemId, item);
    }
}
```

### Step 4: 内容推荐 + 混合排序

```java

import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;

public class HybridRecommender extends CoProcessFunction<
    Recommendation,      // CF 推荐
    Recommendation,      // Content 推荐
    Recommendation       // 混合结果
> {

    private ValueState<List<ScoredItem>> cfState;
    private ValueState<List<ScoredItem>> contentState;

    @Override
    public void open(Configuration parameters) {
        cfState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("cfRecs", List.class)
        );
        contentState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("contentRecs", List.class)
        );
    }

    @Override
    public void processElement1(
            Recommendation cfRec,
            Context ctx,
            Collector<Recommendation> out) throws Exception {
        cfState.update(cfRec.items);
        tryMergeAndOutput(ctx, out);
    }

    @Override
    public void processElement2(
            Recommendation contentRec,
            Context ctx,
            Collector<Recommendation> out) throws Exception {
        contentState.update(contentRec.items);
        tryMergeAndOutput(ctx, out);
    }

    private void tryMergeAndOutput(Context ctx, Collector<Recommendation> out)
            throws Exception {

        List<ScoredItem> cf = cfState.value();
        List<ScoredItem> content = contentState.value();

        if (cf == null || content == null) {
            return;  // 等待两者都到达
        }

        // 融合排序(加权)
        Map<String, Double> mergedScores = new HashMap<>();
        Map<String, String> mergedReasons = new HashMap<>();

        // CF 结果权重 0.6
        for (ScoredItem item : cf) {
            mergedScores.merge(item.itemId, item.score * 0.6, Double::sum);
            mergedReasons.put(item.itemId, "CF:" + item.reason);
        }

        // Content 结果权重 0.4
        for (ScoredItem item : content) {
            mergedScores.merge(item.itemId, item.score * 0.4, Double::sum);
            mergedReasons.merge(item.itemId, "+Content", String::concat);
        }

        // 排序输出
        List<ScoredItem> hybrid = mergedScores.entrySet().stream()
            .map(e -> new ScoredItem(
                e.getKey(),
                e.getValue(),
                mergedReasons.get(e.getKey())
            ))
            .sorted(Comparator.comparingDouble(s -> -s.score))
            .limit(10)
            .collect(Collectors.toList());

        Recommendation result = new Recommendation();
        result.userId = ctx.getCurrentKey();
        result.items = hybrid;
        result.algorithm = "HYBRID";
        result.timestamp = ctx.timestamp();

        out.collect(result);

        // 清空状态
        cfState.clear();
        contentState.clear();
    }
}
```

### Step 5: 主程序

```java

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;

public class RealtimeRecommendationJob {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(4);

        // 用户行为流
        DataStream<UserBehavior> behaviors = env
            .addSource(new UserBehaviorSource())
            .assignTimestampsAndWatermarks(...);

        // 商品特征流(广播)
        BroadcastStream<ItemFeature> itemFeatures = env
            .addSource(new ItemFeatureSource())
            .broadcast(ITEM_STATE_DESCRIPTOR);

        // Step 1: 异步查询画像
        DataStream<EnrichedBehavior> enriched = AsyncDataStream
            .unorderedWait(
                behaviors,
                new AsyncProfileRequest(),
                1000,  // 超时1秒
                TimeUnit.MILLISECONDS,
                100    // 并发请求数
            );

        // Step 2: 更新用户兴趣
        DataStream<UserProfile> profiles = enriched
            .keyBy(e -> e.behavior.userId)
            .process(new InterestUpdater());

        // Step 3: 协同过滤推荐
        DataStream<Recommendation> cfRecs = profiles
            .connect(itemFeatures)
            .process(new CollaborativeFiltering());

        // Step 4: 内容推荐
        DataStream<Recommendation> contentRecs = profiles
            .map(new ContentBasedRecommender());

        // Step 5: 混合排序
        DataStream<Recommendation> hybridRecs = cfRecs
            .keyBy(r -> r.userId)
            .connect(contentRecs.keyBy(r -> r.userId))
            .process(new HybridRecommender());

        // 输出推荐结果
        hybridRecs.addSink(new RecommendationSink());

        env.execute("Realtime Recommendation");
    }
}
```

## 评分标准

| 维度 | 权重 | 要求 |
|------|------|------|
| Async IO | 25% | 正确使用异步查询外部服务 |
| 推荐算法 | 25% | 实现至少两种推荐算法 |
| 融合排序 | 20% | 正确融合多种推荐结果 |
| 性能优化 | 20% | 考虑缓存、并发控制 |
| 代码质量 | 10% | 结构清晰，可测试 |

## 扩展练习

### 扩展 1: 实时模型更新

```java
// 使用 FlinkML 或外部模型服务
public class ModelInference extends RichMapFunction<UserProfile, Recommendation> {

    private transient ModelServer client;

    @Override
    public void open(Configuration parameters) {
        client = ModelServer.connect("tensorflow-serving:8501");
    }

    @Override
    public Recommendation map(UserProfile profile) {
        // 调用深度学习模型
        Prediction pred = client.predict(profile.embedding);
        return toRecommendation(pred);
    }
}
```

### 扩展 2: 在线 A/B 测试

```java
public class ABTestSplit extends ProcessFunction<UserProfile, UserProfile> {

    @Override
    public void processElement(UserProfile profile, Context ctx, ...) {
        // 基于用户ID哈希分配实验组
        int hash = profile.userId.hashCode() % 100;

        if (hash < 50) {
            profile.abTestGroup = "control";
        } else {
            profile.abTestGroup = "treatment";
        }

        out.collect(profile);
    }
}
```

## 参考解答

完整参考实现位于 `reference/challenge-04-recommendation/` 目录。

## 下一步

- [Challenge 5: 实时数据清洗管道](./challenge-05-data-pipeline.md)
