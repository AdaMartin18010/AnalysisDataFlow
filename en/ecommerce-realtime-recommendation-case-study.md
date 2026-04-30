# E-commerce Real-time Recommendation System Case Study

> Stage: Knowledge | Prerequisites: [Related Documents] | Formalization Level: L3

> **Case ID**: 10.2.4
> **Industry**: E-commerce
> **Scenario**: Real-time Personalized Recommendation, Real-time Feature Engineering
> **Scale**: 10 million DAU (Daily Active Users, 日活跃用户), 1 billion events/day
> **Completion Date**: 2026-04-09
> **Document Version**: v1.0

---

> **Case Nature**: 🔬 Proof-of-Concept Architecture | **Validation Status**: Based on theoretical derivation and architectural design; not independently validated by third-party production verification
>
> This case describes an ideal architecture derived from the project's theoretical framework, including hypothetical performance metrics and theoretical cost models.
> Actual production deployment may yield significantly different results due to environmental differences, data scale, team capabilities, and other factors.
> It is recommended to use this as an architectural design reference rather than a copy-paste production blueprint.

## Executive Summary

### Business Background

A leading e-commerce platform faces real-time challenges in its recommendation system:

- User behavior changes rapidly; offline models cannot timely capture interest drift
- During sales events (大促), traffic surges 10x, requiring elastic system scaling
- Recommendation latency directly impacts conversion rate and GMV (Gross Merchandise Volume, 商品交易总额)

### Technical Challenges

| Challenge | Description | Impact |
|-----------|-------------|--------|
| Low Latency Requirement | Recommendation results must return within 100ms | Directly impacts user experience |
| Feature Real-time | Real-time user behavior must reflect in recommendations within seconds | Impacts recommendation accuracy |
| High Concurrency Processing | Peak QPS (Queries Per Second, 每秒查询量) reaches 500,000 | System stability risk |
| A/B Testing | Must support multi-model parallel experiments | Engineering complexity |

### Solution Overview

Adopts **Flink + Redis + TensorFlow Serving** architecture:

- Flink processes user behavior streams in real time, updating user profiles (用户画像)
- Redis stores real-time features, supporting millisecond-level queries
- TensorFlow Serving deploys models with GPU-accelerated inference
- Recommendation latency reduced from 500ms to 50ms, conversion rate improved by 15%

---

## 1. Business Scenario Analysis

### 1.1 Business Process

The following diagram illustrates the end-to-end business flow from user actions through data collection, real-time processing, recommendation service, and storage layers.

```mermaid
flowchart TB
    subgraph UserClient[User Client]
        A[Browse Products]
        B[Click Product]
        C[Add to Cart]
        D[Place Order & Pay]
    end

    subgraph DataCollection[Data Collection Layer]
        E[Tracking SDK]
        F[Log Collection]
        G[Kafka Message Queue]
    end

    subgraph RealtimeProcessing[Real-time Processing Layer]
        H[Flink Stream Processing]
        I[Feature Computation]
        J[User Profile Update]
    end

    subgraph RecService[Recommendation Service Layer]
        K[Feature Query]
        L[Model Inference]
        M[Result Ranking]
    end

    subgraph StorageLayer[Storage Layer]
        N[Redis Real-time Features]
        O[Feature Store]
        P[Model Repository]
    end

    A --> E --> F --> G
    B --> E --> F --> G
    C --> E --> F --> G
    D --> E --> F --> G
    G --> H --> I --> J
    I --> N
    J --> O
    A --> K --> N --> L --> M
    L --> P
```

### 1.2 Data Scale
>
> 🔮 **Estimated Data** | Basis: Derived from industry reference values and theoretical analysis; not from actual test environments


| Metric | Value | Description |
|--------|-------|-------------|
| DAU (Daily Active Users) | 10 million | Peak: 15 million |
| Daily Event Volume | 1 billion | Clicks, views, favorites, etc. |
| Peak QPS | 500,000 | During sales events |
| Product SKU | 50 million | Including historical products |
| User Profile Dimensions | 200+ | Basic attributes + behavioral features |
| Real-time Feature Count | 1,000+ | Real-time computed features |

### 1.3 SLA Requirements
>
> 🔮 **Estimated Data** | Basis: Derived from industry reference values and theoretical analysis; not from actual test environments


| Metric | Target | Actual Achievement |
|--------|--------|--------------------|
| Recommendation Latency (P99) | < 100ms | 50ms |
| Feature Freshness | < 1s | 500ms |
| System Availability | 99.99% | 99.995% |
| Recommendation Accuracy | > 15% | 18% (CTR) |
| Throughput | 500K QPS | 600K QPS |

---

## 2. Architecture Design

### 2.1 System Architecture Diagram

The following diagram shows the overall system architecture encompassing data sources, real-time computation, feature storage, model service, and recommendation API layers.

```mermaid
graph TB
    subgraph DataSource[Data Source]
        KAFKA[Kafka Cluster<br/>10 Nodes / 3 Replicas]
    end

    subgraph RealtimeCompute[Real-time Computation Layer]
        FLINK[Flink Cluster<br/>100 TaskManagers]
        subgraph FlinkJobs[Flink Jobs]
            JOB1[User Behavior Parsing]
            JOB2[Real-time Feature Computation]
            JOB3[User Profile Update]
            JOB4[Product Popularity Computation]
        end
    end

    subgraph FeatureStorage[Feature Storage Layer]
        REDIS[Redis Cluster<br/>20 Masters / 40 Slaves]
        FEAST[Feast Feature Store]
    end

    subgraph ModelService[Model Service Layer]
        TFS[TensorFlow Serving<br/>GPU Cluster]
        subgraph Models[Recommendation Models]
            M1[Deep Interest Network (DIN)]
            M2[Sequence Model (Transformer)]
            M3[Recall Model (Embedding)]
        end
    end

    subgraph RecAPI[Recommendation API Layer]
        GATEWAY[API Gateway]
        RECSVC[Recommendation Service]
    end

    KAFKA --> FLINK
    FLINK --> JOB1 --> JOB2 --> JOB3
    FLINK --> JOB4
    JOB2 --> REDIS
    JOB3 --> FEAST
    JOB4 --> REDIS
    GATEWAY --> RECSVC
    RECSVC --> REDIS
    RECSVC --> FEAST
    RECSVC --> TFS
    TFS --> M1
    TFS --> M2
    TFS --> M3
```

### 2.2 Component Selection

| Component | Selection | Rationale |
|-----------|-----------|-----------|
| Stream Processing Engine | Apache Flink 2.1 | Low latency, Exactly-Once semantics, mature ecosystem |
| Message Queue | Kafka 3.5 | High throughput, persistence, horizontal scaling |
| Feature Storage | Redis Cluster 7.0 | Millisecond-level queries, high concurrency, rich data structures |
| Model Serving | TensorFlow Serving 2.13 | GPU support, batch inference, A/B testing |
| Feature Store | Feast 0.34 | Feature reuse, version management, offline-online consistency |

### 2.3 Deployment Topology

The following diagram illustrates the cross-Availability Zone deployment topology for Flink JobManagers, TaskManagers, and Redis clusters.

```mermaid
graph LR
    subgraph AZ1[Availability Zone 1]
        F1[Flink JobManager]
        T1[TaskManager x30]
        R1[Redis Master x10]
    end

    subgraph AZ2[Availability Zone 2]
        F2[Flink JobManager-Standby]
        T2[TaskManager x30]
        R2[Redis Master x10]
    end

    subgraph AZ3[Availability Zone 3]
        T3[TaskManager x40]
        R3[Redis Slave x20]
    end

    F1 -.-> F2
    T1 -.-> T2
    T2 -.-> T3
    R1 -.-> R3
    R2 -.-> R3
```

---

## 3. Technical Implementation

### 3.1 Flink Real-time Feature Computation

```java
// User real-time behavior feature computation

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.streaming.api.CheckpointingMode;

public class UserRealtimeFeatureJob {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        // Configure Checkpoint
        env.enableCheckpointing(60000);
        env.getCheckpointConfig().setCheckpointingMode(
            CheckpointingMode.EXACTLY_ONCE);

        // Read user behavior stream
        DataStream<UserEvent> userEvents = env
            .addSource(new FlinkKafkaConsumer<>("user-events",
                new UserEventDeserializationSchema(), kafkaProps))
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<UserEvent>forBoundedOutOfOrderness(
                    Duration.ofSeconds(5))
                .withTimestampAssigner((event, timestamp) ->
                    event.getEventTime())
            );

        // Compute real-time features
        DataStream<UserFeature> features = userEvents
            .keyBy(UserEvent::getUserId)
            .process(new RealtimeFeatureFunction());

        // Write to Redis
        features.addSink(new RedisFeatureSink());

        env.execute("User Realtime Feature Computation");
    }
}

// Real-time feature computation function
public class RealtimeFeatureFunction extends
    KeyedProcessFunction<String, UserEvent, UserFeature> {

    private ValueState<UserSession> sessionState;
    private ListState<ProductView> viewHistory;

    @Override
    public void open(Configuration parameters) {
        sessionState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("session", UserSession.class));
        viewHistory = getRuntimeContext().getListState(
            new ListStateDescriptor<>("views", ProductView.class));
    }

    @Override
    public void processElement(UserEvent event, Context ctx,
            Collector<UserFeature> out) throws Exception {

        UserSession session = sessionState.value();
        if (session == null) {
            session = new UserSession(event.getUserId());
        }

        // Update session statistics
        session.update(event);

        // Maintain recent browsing history (sliding window)
        if (event.getEventType() == EventType.VIEW) {
            viewHistory.add(new ProductView(
                event.getProductId(),
                event.getEventTime()));

            // Clean expired records (keep latest 100)
            trimViewHistory(100);
        }

        // Generate real-time features
        UserFeature feature = new UserFeature();
        feature.setUserId(event.getUserId());
        feature.setSessionDuration(session.getDuration());
        feature.setClickCount(session.getClickCount());
        feature.setCategoryDistribution(
            calculateCategoryDistribution());
        feature.setRecentViews(getRecentViews(10));
        feature.setTimestamp(System.currentTimeMillis());

        out.collect(feature);
        sessionState.update(session);
    }

    private Map<String, Double> calculateCategoryDistribution()
            throws Exception {
        Map<String, Integer> counts = new HashMap<>();
        int total = 0;

        for (ProductView view : viewHistory.get()) {
            String category = view.getCategory();
            counts.merge(category, 1, Integer::sum);
            total++;
        }

        Map<String, Double> distribution = new HashMap<>();
        for (Map.Entry<String, Integer> entry : counts.entrySet()) {
            distribution.put(entry.getKey(),
                entry.getValue() / (double) total);
        }

        return distribution;
    }
}
```

### 3.2 Recommendation Service Implementation

```python
# Recommendation service main logic
class RecommendationService:
    def __init__(self):
        self.redis_client = RedisCluster(
            startup_nodes=REDIS_NODES,
            decode_responses=True
        )
        self.feature_store = FeastFeatureStore(
            repo_path="/opt/feast/feature_repo"
        )
        self.tf_serving = TFServingClient(
            host="tf-serving.internal",
            port=8501
        )

    async def get_recommendations(
        self,
        user_id: str,
        context: RequestContext
    ) -> RecommendationResponse:
        start_time = time.time()

        # 1. Query real-time features (Redis) - target < 5ms
        realtime_features = await self._get_realtime_features(user_id)

        # 2. Query batch features (Feature Store) - target < 10ms
        batch_features = await self._get_batch_features(user_id)

        # 3. Recall stage - target < 20ms
        recall_items = await self._recall_stage(
            user_id,
            realtime_features
        )

        # 4. Ranking stage (model inference) - target < 50ms
        ranked_items = await self._rank_stage(
            recall_items,
            {**realtime_features, **batch_features},
            context
        )

        # 5. Re-ranking stage - target < 10ms
        final_items = await self._rerank_stage(
            ranked_items,
            context
        )

        latency = (time.time() - start_time) * 1000

        return RecommendationResponse(
            items=final_items[:50],
            latency_ms=latency,
            trace_id=context.trace_id
        )

    async def _get_realtime_features(self, user_id: str) -> Dict:
        """Get real-time features from Redis - critical path"""
        pipe = self.redis_client.pipeline()

        # Query multiple features in parallel
        pipe.hgetall(f"user:{user_id}:realtime")
        pipe.get(f"user:{user_id}:session_duration")
        pipe.lrange(f"user:{user_id}:recent_views", 0, 9)
        pipe.hgetall(f"user:{user_id}:category_dist")

        results = pipe.execute()

        return {
            'realtime_profile': results[0],
            'session_duration': float(results[1] or 0),
            'recent_views': results[2],
            'category_distribution': results[3]
        }

    async def _rank_stage(
        self,
        items: List[Item],
        features: Dict,
        context: RequestContext
    ) -> List[RankedItem]:
        """Model inference ranking stage"""

        # Construct model inputs
        model_inputs = []
        for item in items:
            feature_vector = self._construct_feature_vector(
                item,
                features,
                context
            )
            model_inputs.append(feature_vector)

        # Batch inference optimization
        batch_size = 100
        scores = []

        for i in range(0, len(model_inputs), batch_size):
            batch = model_inputs[i:i + batch_size]
            batch_scores = await self.tf_serving.predict(
                model_name="din_recommendation",
                inputs=np.array(batch)
            )
            scores.extend(batch_scores)

        # Sort
        ranked = [
            RankedItem(item=item, score=score)
            for item, score in zip(items, scores)
        ]
        ranked.sort(key=lambda x: x.score, reverse=True)

        return ranked
```

### 3.3 Key Configuration Parameters

```yaml
# Flink configuration
flink:
  parallelism:
    default: 100
    feature-computation: 50
    user-profile: 30
  checkpoint:
    interval: 60s
    mode: EXACTLY_ONCE
    timeout: 10m
    min-pause: 30s
  state:
    backend: rocksdb
    incremental-checkpoints: true
    local-recovery: true
  network:
    memory:
      fraction: 0.15
      min: 2gb
      max: 8gb

# Redis configuration
redis:
  cluster:
    nodes: 20
    replicas-per-master: 2
  memory:
    max: 64gb-per-node
    policy: allkeys-lru
  timeout: 100ms
  tcp-keepalive: 300

# TensorFlow Serving configuration
tf_serving:
  model:
    name: din_recommendation
    version: 20240409
    batching:
      max_batch_size: 100
      batch_timeout_micros: 5000
      num_batch_threads: 16
  resources:
    gpu:
      count: 4
      memory_fraction: 0.9
    cpu: 16
    memory: 64gb
```

---

## 4. Performance Metrics

### 4.1 Latency Analysis
>
> 🔮 **Estimated Data** | Basis: Derived from industry reference values and theoretical analysis; not from actual test environments


| Stage | P50 | P99 | Target | Status |
|-------|-----|-----|--------|--------|
| Real-time Feature Query | 3ms | 8ms | < 10ms | ✅ |
| Batch Feature Query | 8ms | 15ms | < 20ms | ✅ |
| Recall Stage | 12ms | 25ms | < 30ms | ✅ |
| Model Inference | 30ms | 50ms | < 60ms | ✅ |
| Re-ranking Stage | 5ms | 10ms | < 15ms | ✅ |
| **Total Latency** | **58ms** | **108ms** | **< 120ms** | ✅ |

### 4.2 Throughput Data

The following diagram illustrates QPS progression from normal traffic to peak sales traffic to stress-test limits.

```mermaid
graph LR
    subgraph Normal[Normal Traffic]
        D1[200K QPS]
    end

    subgraph Peak[Peak Traffic (Sales Event)]
        P1[600K QPS]
    end

    subgraph Stress[Stress Test]
        L1[1M QPS]
    end

    D1 --> P1 --> L1
```

>
> 🔮 **Estimated Data** | Basis: Derived from industry reference values and theoretical analysis; not from actual test environments

| Scenario | QPS | Latency P99 | CPU Usage | Memory Usage |
|----------|-----|-------------|-----------|--------------|
| Normal | 200K | 80ms | 45% | 60% |
| Sales Event | 600K | 108ms | 75% | 80% |
| Stress Test | 1M | 200ms | 95% | 95% |

### 4.3 Business Impact
>
> 🔮 **Estimated Data** | Basis: Derived from industry reference values and case analogy analysis


| Metric | Before Optimization | After Optimization | Improvement |
|--------|--------------------|--------------------|-------------|
| Recommendation Latency (P99) | 500ms | 108ms | **78%** ↓ |
| CTR (Click-Through Rate, 点击率) | 12% | 18% | **50%** ↑ |
| CVR (Conversion Rate, 转化率) | 3% | 4.5% | **50%** ↑ |
| GMV Contribution | Baseline | +15% | **15%** ↑ |
| User Dwell Time | Baseline | +20% | **20%** ↑ |

---

## 5. Lessons Learned

### 5.1 Best Practices

1. **Hierarchical Feature Design**
   - Real-time features: User's most recent behavior, millisecond-level updates
   - Near real-time features: 5-minute aggregation, minute-level updates
   - Offline features: User profile, hourly updates
   - Cold-start features: Global statistics, daily updates

2. **Model Serving Optimization**
   - Batch inference: Reduce RPC call count
   - Model warm-up: Avoid cold-start latency
   - Multi-version deployment: Support canary releases
   - GPU sharing: Improve resource utilization

3. **Caching Strategy**
   - Multi-level cache: Local cache + Redis cluster
   - Cache warm-up: Pre-load hot data before sales events
   - Cache invalidation: Event-based precise invalidation

### 5.2 Pitfalls

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| Redis Hot Key | Certain user features accessed at high frequency | Local cache + Key sharding |
| Flink Checkpoint Timeout | State too large, RocksDB slow | Incremental Checkpoint + Local recovery |
| Model Inference Latency Jitter | Uneven GPU batch processing | Dynamic batching + Timeout mechanism |
| Feature Inconsistency | Online-offline feature computation logic differs | Unified feature definitions via Feast |

### 5.3 Optimization Recommendations

1. **Short-term Optimization**
   - Introduce JVM profiling to optimize GC
   - Optimize feature storage structure to reduce memory usage
   - Implement adaptive batch processing size

2. **Mid-term Planning**
   - Explore model quantization to reduce inference latency
   - Introduce GNN (Graph Neural Network, 图神经网络) to model user-item relationships
   - Implement multi-objective optimization (CTR + CVR + dwell time)

3. **Long-term Vision**
   - End-to-end real-time training (Online Learning, 在线学习)
   - Reinforcement learning for recommendation strategy optimization
   - Cross-domain recommendation (products + content + ads)

---

## 6. Appendix

### 6.1 Complete Configuration

```properties
# application.properties

# Flink configuration
flink.job-manager.memory.process.size=4096m
flink.task-manager.memory.process.size=16384m
flink.task-manager.memory.managed.fraction=0.4
flink.task-manager.memory.network.fraction=0.15
flink.state.backend.incremental=true
flink.state.checkpoints.dir=hdfs:///checkpoints/recommendation

# Redis configuration
redis.cluster.nodes=redis-1:6379,redis-2:6379,redis-3:6379
redis.connection.timeout=100
redis.socket.timeout=100
redis.max-redirects=3
redis.max-total=1000
redis.max-idle=500
redis.min-idle=100

# TensorFlow Serving configuration
TF_SERVING_HOST=tf-serving.internal
TF_SERVING_PORT=8501
TF_SERVING_MODEL_NAME=din_recommendation
TF_SERVING_BATCH_SIZE=100
TF_SERVING_BATCH_TIMEOUT=5
```

### 6.2 Monitoring Metrics
>
> 🔮 **Estimated Data** | Basis: Derived from industry reference values and theoretical analysis; not from actual test environments


| Metric Category | Specific Metric | Alert Threshold |
|-----------------|-----------------|-----------------|
| Latency | Recommendation API P99 | > 150ms |
| Latency | Feature Query P99 | > 20ms |
| Availability | Recommendation Service Success Rate | < 99.9% |
| Resources | Flink TaskManager CPU | > 85% |
| Resources | Redis Memory Usage | > 85% |
| Business | Recommendation CTR | Drop 20% MoM |

### 6.3 Incident Response

**Scenario 1: Redis Cluster Failure**

```
Symptom: Massive feature query timeouts
Response:
1. Automatic degradation to local cache
2. Trigger Redis master-slave failover
3. Rate-limiting to protect downstream services
4. Manual intervention for repair
```

**Scenario 2: Flink Job Failure**

```
Symptom: Real-time feature updates stop
Response:
1. Automatic job restart (up to 3 times)
2. Recover from the latest Checkpoint
3. Notify operations team
4. Monitor data lag recovery
```

**Scenario 3: Model Inference Timeout**

```
Symptom: Recommendation API latency spikes
Response:
1. Timeout circuit breaker, return fallback results
2. Dynamically reduce batch processing size
3. Trigger model warm-up
4. Check GPU resources
```

---

## References


---

*This case study was compiled by the AnalysisDataFlow project and is intended for educational and exchange purposes only.*
