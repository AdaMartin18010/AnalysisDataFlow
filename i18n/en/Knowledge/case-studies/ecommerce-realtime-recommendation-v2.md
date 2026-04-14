---
title: "E-Commerce Real-Time Recommendation System Case Study"
translation_status: ai_translated_reviewed
source_version: v4.1
last_sync: "2026-04-15"
---

# E-Commerce Real-Time Recommendation System Case Study

> **Stage**: Knowledge/case-studies/ecommerce | **Prerequisites**: [Knowledge/00-INDEX.md](../../Knowledge/00-INDEX.md) | **Formalization Level**: L5
> **Case ID**: CS-E-02 | **Completion Date**: 2026-04-11 | **Version**: v2.0

---

## Table of Contents

- [E-Commerce Real-Time Recommendation System Case Study](#e-commerce-real-time-recommendation-system-case-study)
  - [Table of Contents](#table-of-contents)
  - [1. Definitions](#1-definitions)
    - [1.1 Real-Time Recommendation System Definition](#11-real-time-recommendation-system-definition)
    - [1.2 User Behavior Characteristics](#12-user-behavior-characteristics)
    - [1.3 Recommendation Quality Metrics](#13-recommendation-quality-metrics)
  - [2. Properties](#2-properties)
    - [2.1 Real-Time Constraints](#21-real-time-constraints)
    - [2.2 Scalability Guarantees](#22-scalability-guarantees)
  - [3. Relations](#3-relations)
    - [3.1 Data Flow Architecture Relationship](#31-data-flow-architecture-relationship)
    - [3.2 Model Service Relationship](#32-model-service-relationship)
  - [4. Argumentation](#4-argumentation)
    - [4.1 Real-Time vs Offline Recommendation](#41-real-time-vs-offline-recommendation)
    - [4.2 Cold Start Problem Analysis](#42-cold-start-problem-analysis)
  - [5. Proof / Engineering Argument](#5-proof--engineering-argument)
    - [5.1 Feature Engineering Pipeline](#51-feature-engineering-pipeline)
    - [5.2 Model Inference Optimization](#52-model-inference-optimization)
  - [6. Examples](#6-examples)
    - [6.1 Case Background](#61-case-background)
    - [6.2 Implementation Results](#62-implementation-results)
    - [6.3 Technical Architecture](#63-technical-architecture)
    - [6.4 Production Environment Checklist](#64-production-environment-checklist)
  - [7. Visualizations](#7-visualizations)
    - [7.1 Real-Time Recommendation Data Flow Architecture](#71-real-time-recommendation-data-flow-architecture)
    - [7.2 Feature Engineering Pipeline](#72-feature-engineering-pipeline)
    - [7.3 Model Inference Service Architecture](#73-model-inference-service-architecture)
    - [7.4 System Deployment Topology](#74-system-deployment-topology)
  - [8. References](#8-references)

---

## 1. Definitions

### 1.1 Real-Time Recommendation System Definition

**Def-K-10-201** (Real-Time Recommendation System): A real-time recommendation system is a nonuple $\mathcal{R} = (U, I, C, B, F, M, S, P, W)$:

- $U$: set of users, $|U| = N_u$, typically at the $10^8$ scale
- $I$: set of items, $|I| = N_i$, typically at the $10^7$ scale
- $C$: set of contexts (time, location, device)
- $B$: set of user behavior sequences
- $F$: set of feature engineering functions
- $M$: set of recommendation models (recall + ranking + reranking)
- $S$: candidate generation strategy
- $P$: personalization function
- $W$: feedback learning mechanism

**Recommendation response definition**:

$$
Recommendation(u, c, t) = TopK\left(\{score(u, i, c) : i \in CandidateSet(u, t)\}\right)
$$

Where $score(u, i, c)$ is the predicted score of user $u$ for item $i$ in context $c$.

### 1.2 User Behavior Characteristics

**Def-K-10-202** (User Real-Time Profile): The real-time profile of user $u$ at time $t$ is defined as:

$$
Profile(u, t) = (D_u, H_u^{(t)}, R_u^{(t)}, S_u^{(t)})
$$

Where:

- $D_u$: user demographic features (age, gender, region)
- $H_u^{(t)} = \{(i, \tau, action) : \tau \in [t-T, t]\}$: recent behavior history
- $R_u^{(t)}$: real-time intent vector (inferred from session behavior)
- $S_u^{(t)}$: current session state

**Def-K-10-203** (Real-Time Feature Vector): Feature engineering output:

$$
F(u, i, c) = concat(F_{user}(u), F_{item}(i), F_{context}(c), F_{interaction}(u,i))
$$

### 1.3 Recommendation Quality Metrics

**Def-K-10-204** (Recommendation Effect Metrics):

| Metric | Definition | Target |
|--------|------------|--------|
| CTR | Click-through rate = clicks / impressions | > 5% |
| CVR | Conversion rate = orders / clicks | > 3% |
| GMV | Gross merchandise value | Daily > 100M |
| Diversity | Category coverage | > 80% |
| Novelty | Long-tail item proportion | > 30% |

**Def-K-10-205** (Latency Constraint):

$$
L_{total} = L_{feature} + L_{recall} + L_{rank} + L_{rerank} + L_{network} \leq 100ms
$$

---

## 2. Properties

### 2.1 Real-Time Constraints

**Lemma-K-10-201**: Let feature query latency be $L_f$, recall stage latency be $L_r$, and ranking stage latency be $L_s$, then the total latency satisfies:

$$
L_{total} = L_f + \max(L_r^{(1)}, L_r^{(2)}, ..., L_r^{(k)}) + L_s + L_{rerank} \leq L_{SLA}
$$

For e-commerce recommendation scenarios, $L_{SLA} = 100$ms (P99).

**Thm-K-10-201** (Throughput Scalability): Let single-node throughput be $TPS_{single}$, number of nodes be $N$, and linear scaling coefficient be $\alpha$ (typically $\alpha \in [0.8, 0.95]$), then the total system throughput is:

$$
TPS_{total} = \alpha \cdot N \cdot TPS_{single}
$$

To reach 1 million TPS, assuming 50K TPS per node and $\alpha = 0.9$:

$$
N \geq \frac{10^6}{0.9 \times 5 \times 10^4} \approx 23 \text{ nodes}
$$

### 2.2 Scalability Guarantees

**Lemma-K-10-202** (Feature Storage Capacity): Let the number of users be $N_u$, feature dimension per user be $d$, single feature size be $s$ bytes, and number of Redis cluster shards be $S$, then storage per shard is:

$$
Storage_{per\_shard} = \frac{N_u \cdot d \cdot s}{S}
$$

For 1 billion users, 1000-dimensional features, 4 bytes per dimension, and 100 shards:

$$
Storage = \frac{10^9 \times 1000 \times 4}{100} = 40GB/shard
$$

---

## 3. Relations

### 3.1 Data Flow Architecture Relationship

```mermaid
flowchart TB
    subgraph Data Collection Layer
        A1[Click Stream]
        A2[Impression Logs]
        A3[Order Events]
        A4[User Behavior]
    end

    subgraph Flink Real-Time Processing
        B1[Behavior Parsing]
        B2[Session Window]
        B3[Feature Aggregation]
        B4[Real-Time Profile]
    end

    subgraph Feature Store
        C1[Redis User Profile]
        C2[HBase Historical Features]
        C3[Flink State Session Features]
    end

    subgraph Recall Layer
        D1[i2i Collaborative Filtering]
        D2[Vector Recall]
        D3[Trending Rankings]
        D4[Operational Intervention]
    end

    subgraph Ranking Layer
        E1[Deep Model]
        E2[GBDT Model]
        E3[Rule Reranking]
    end

    A1 --> B1 --> B2 --> B3 --> B4
    A2 --> B1
    A3 --> B1
    A4 --> B1

    B4 --> C1
    B3 --> C2
    B2 --> C3

    C1 --> D1 --> E1
    C2 --> D2 --> E2
    C3 --> D3 --> E3
```

### 3.2 Model Service Relationship

| Stage | Model Type | Latency Requirement | Candidate Count | Core Metric |
|-------|------------|---------------------|-----------------|-------------|
| Recall | Vector retrieval | < 10ms | Tens of thousands | Recall rate |
| Coarse ranking | Lightweight model | < 20ms | Thousands | Relevance |
| Fine ranking | Deep model | < 50ms | Hundreds | CTR/CVR |
| Reranking | Rules / policies | < 10ms | Tens | Diversity |

---

## 4. Argumentation

### 4.1 Real-Time vs Offline Recommendation

| Dimension | Real-Time Recommendation | Offline Recommendation | Hybrid Strategy |
|-----------|--------------------------|------------------------|-----------------|
| Latency | < 100ms | Hour-level | Real-time recall + offline features |
| Personalization | Based on current session | Based on historical behavior | Fuse both |
| Cold start | Rapid response | Cannot handle | Real-time learning |
| Computation cost | High | Low | Tiered optimization |
| Applicable scenario | Homepage Feed | Email push | Full-scenario coverage |

**Hybrid architecture advantage**: Real-time capture of user instant intent, while leveraging rich offline features to ensure recommendation quality.

### 4.2 Cold Start Problem Analysis

**Def-K-10-206** (Cold Start Classification):

| Type | Description | Solution Strategy |
|------|-------------|-------------------|
| User cold start | New user has no history | Popular recommendations, based on device/location |
| Item cold start | New item has no interactions | Content similarity, exploration-exploitation |
| System cold start | Brand-new system | Expert rules, rapid iteration |

**Exploration-Exploitation Balance**:

$$
Score_{explore}(i) = \hat{r}_{ui} + \beta \cdot \sqrt{\frac{\ln N}{n_i}}
$$

Where $N$ is the total number of impressions, $n_i$ is the number of impressions of item $i$, and $\beta$ is the exploration coefficient.

---

## 5. Proof / Engineering Argument

### 5.1 Feature Engineering Pipeline

**Thm-K-10-202** (Feature Consistency): The Flink feature engineering pipeline guarantees Exactly-Once semantics, ensuring training/inference feature consistency.

**Flink feature engineering implementation**:

```java

import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.streaming.api.windowing.time.Time;

// User behavior feature computation
DataStream<UserFeature> userFeatures = clickStream
    .keyBy(ClickEvent::getUserId)
    .window(SlidingEventTimeWindows.of(Time.minutes(30), Time.seconds(10)))
    .aggregate(new UserFeatureAggregator())
    .name("user-feature-calculation");

// Item statistical features
DataStream<ItemFeature> itemFeatures = eventStream
    .keyBy(Event::getItemId)
    .window(SlidingEventTimeWindows.of(Time.hours(1), Time.minutes(5)))
    .aggregate(new ItemFeatureAggregator());

// Session-level real-time intent recognition
DataStream<SessionIntent> sessionIntents = behaviorStream
    .keyBy(BehaviorEvent::getSessionId)
    .process(new KeyedProcessFunction<String, BehaviorEvent, SessionIntent>() {
        private ValueState<SessionState> sessionState;
        private static final long SESSION_TIMEOUT = 30 * 60 * 1000; // 30min

        @Override
        public void open(Configuration parameters) {
            sessionState = getRuntimeContext().getState(
                new ValueStateDescriptor<>("session", SessionState.class));
        }

        @Override
        public void processElement(BehaviorEvent event, Context ctx,
                                   Collector<SessionIntent> out) throws Exception {
            SessionState state = sessionState.value();
            if (state == null || ctx.timestamp() - state.getLastTime() > SESSION_TIMEOUT) {
                state = new SessionState(event.getUserId(), ctx.timestamp());
            }
            state.addEvent(event);
            sessionState.update(state);

            // Output intent every 5 events or at session end
            if (state.getEventCount() % 5 == 0 || event.getType() == EventType.PURCHASE) {
                out.collect(state.extractIntent());
            }
        }
    });

// Real-time features written to Redis
userFeatures.addSink(new RedisSink<>(
    new FlinkJedisPoolConfig.Builder()
        .setHost("redis-cluster")
        .setPort(6379)
        .build(),
    new UserFeatureRedisMapper()
));
```

### 5.2 Model Inference Optimization

**TensorFlow Serving integration**:

```java
// Asynchronous model inference

import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

public class AsyncModelInference extends
    RichAsyncFunction<FeatureVector, Prediction> {

    private transient TensorFlowServingClient tfClient;
    private static final String MODEL_NAME = "recommendation_ranking";
    private static final int MODEL_VERSION = 1;

    @Override
    public void open(Configuration parameters) {
        tfClient = TensorFlowServingClient.create("tf-serving:8501");
    }

    @Override
    public void asyncInvoke(FeatureVector features,
                            ResultFuture<Prediction> resultFuture) {
        ListenableFuture<PredictResponse> responseFuture = tfClient.predict(
            MODEL_NAME, MODEL_VERSION,
            features.toTensorProto()
        );

        Futures.addCallback(responseFuture, new FutureCallback<>() {
            @Override
            public void onSuccess(PredictResponse response) {
                float score = response.getOutputsOrThrow("score")
                    .getFloatVal(0);
                resultFuture.complete(Collections.singletonList(
                    new Prediction(features.getItemId(), score)
                ));
            }

            @Override
            public void onFailure(Throwable t) {
                resultFuture.complete(Collections.singletonList(
                    new Prediction(features.getItemId(), 0.0f, t)
                ));
            }
        }, Executors.newCachedThreadPool());
    }
}

// Applied to DataStream
DataStream<Prediction> predictions = featureStream
    .map(FeatureVector::fromUserItemContext)
    .flatMap(new CandidateGenerator()) // Generate candidate set
    .asyncWaitFor(
        new AsyncModelInference(),
        Time.milliseconds(50), // 50ms timeout
        100 // Concurrency
    );
```

**Cache optimization strategy**:

```java
// Multi-level cache: local Caffeine + Redis Cluster
public class MultiLevelFeatureCache {
    private final Cache<String, UserFeature> localCache;
    private final RedisClusterAsyncCommands<String, String> redisClient;

    public UserFeature getUserFeature(String userId) {
        // L1: local cache
        UserFeature feature = localCache.getIfPresent(userId);
        if (feature != null) return feature;

        // L2: Redis
        feature = fetchFromRedis(userId);
        if (feature != null) {
            localCache.put(userId, feature);
            return feature;
        }

        // L3: real-time computation (degradation)
        feature = computeInRealTime(userId);
        return feature;
    }
}
```

---

## 6. Examples

### 6.1 Case Background

**Real-time recommendation system upgrade project for a leading e-commerce platform**

- **Business scale**: 200M DAU, 10B daily PVs, 50M+ SKUs
- **Recommendation scenarios**: Homepage Feed, "Guess You Like" on product detail pages, cart recommendations
- **Historical issues**: Offline recommendation had high latency and could not capture real-time user interest changes

**Technical challenges**:

| Challenge | Description | Quantified Metric |
|-----------|-------------|-------------------|
| Ultra-low latency | Recommendation API P99 < 100ms | Original system 500ms+ |
| Ultra-high throughput | Peak 1M TPS | Daily processing of hundreds of billions of events |
| Real-time personalization | Real-time user intent learning | Minute-level profile updates |
| Multi-objective optimization | CTR/CVR/GMV balance | Multi-objective modeling |

### 6.2 Implementation Results

**Performance data** (12 months post-launch):

| Metric | Before Optimization | After Optimization | Improvement |
|--------|---------------------|--------------------|-------------|
| Recommendation API P99 latency | 450ms | 85ms | -81% |
| System throughput | 200K TPS | 1.2M TPS | +500% |
| Homepage CTR | 3.2% | 5.8% | +81% |
| Conversion rate (CVR) | 2.1% | 3.6% | +71% |
| GMV per capita | ¥125 | ¥198 | +58% |
| Long-tail item impressions | 15% | 35% | +133% |
| Real-time profile updates | Hour-level | Second-level | 3600x |

**Business value**:

- Annual GMV increment: 5B+
- User experience improvement: bounce rate reduced by 12%
- Long-tail item sales: niche category GMV growth of 200%

### 6.3 Technical Architecture

**Core technology stack**:

- **Stream processing**: Apache Flink 1.18 (100-node cluster)
- **Message queue**: Apache Kafka (200 partitions, 3 replicas)
- **Feature store**: Redis Cluster (200 nodes, 40TB) + HBase
- **Model serving**: TensorFlow Serving + NVIDIA Triton
- **Vector retrieval**: Milvus (1B vectors, recall rate > 95%)
- **Monitoring**: Prometheus + Grafana + self-developed A/B platform

**Flink cluster configuration**:

```yaml
# flink-conf.yaml
jobmanager.memory.process.size: 8192m
taskmanager.memory.process.size: 32768m
taskmanager.numberOfTaskSlots: 8
parallelism.default: 400

# Checkpoint configuration
state.backend: rocksdb
state.checkpoints.dir: hdfs:///checkpoints/recommendation
execution.checkpointing.interval: 30s
execution.checkpointing.max-concurrent-checkpoints: 1
```

### 6.4 Production Environment Checklist

**Pre-deployment checks**:

| Check Item | Requirement | Verification Method |
|------------|-------------|---------------------|
| Redis cluster | 200 nodes, 40TB capacity | `redis-cli cluster info` |
| Kafka throughput | 2M records/second | Producer stress test |
| TF Serving GPU | A100 x 20 | `nvidia-smi` |
| Network bandwidth | 10Gbps NIC, <1ms latency | `iperf3` |

**Runtime monitoring**:

| Metric | Alert Threshold | Handling Plan |
|--------|-----------------|---------------|
| Recommendation latency P99 | > 150ms | Scale out / degrade |
| Redis hit rate | < 95% | Adjust cache strategy |
| TF Serving QPS | > 80% capacity | Horizontal scale out |
| Flink Checkpoint | Failures > 3 | Tune RocksDB |
| Model AUC | Drop > 5% | Rollback model |

**Fault degradation strategy**:

```java
// Multi-level degradation strategy
public class DegradationStrategy {
    // Level 1: Disable complex feature computation
    public void level1Degrade() {
        featureConfig.setComputeComplexFeatures(false);
    }

    // Level 2: Use simplified model
    public void level2Degrade() {
        modelRouter.routeTo("light_model");
    }

    // Level 3: Return trending rankings
    public void level3Degrade() {
        recommendationCache.getHotItems();
    }
}
```

---

## 7. Visualizations

### 7.1 Real-Time Recommendation Data Flow Architecture

```mermaid
graph TB
    subgraph User Side
        A1[APP/PC/H5]
        A2[Embedded SDK]
    end

    subgraph Access Layer
        B1[Nginx Gateway]
        B2[Kafka Producer]
    end

    subgraph Real-Time Computation Layer
        C1[Flink Event Parsing]
        C2[User Profile Update]
        C3[Item Statistics Update]
        C4[Real-Time Feature Computation]
    end

    subgraph Storage Layer
        D1[Redis User Profile]
        D2[HBase Historical Features]
        D3[Milvus Vector Store]
        D4[ClickHouse Reports]
    end

    subgraph Recommendation Service Layer
        E1[Recall Service]
        E2[Ranking Service]
        E3[Reranking Service]
        E4[TF Serving]
    end

    subgraph Output Layer
        F1[Recommendation Results]
        F2[Real-Time Reports]
    end

    A1 --> A2 --> B1 --> B2
    B2 --> C1 --> C2 --> D1
    C1 --> C3 --> D2
    C1 --> C4 --> D3

    D1 --> E1 --> E2 --> E3 --> F1
    D2 --> E2
    D3 --> E1
    E2 --> E4

    C4 --> D4 --> F2
```

### 7.2 Feature Engineering Pipeline

```mermaid
flowchart LR
    subgraph Raw Data
        A1[Click Stream]
        A2[Impression Stream]
        A3[Order Stream]
    end

    subgraph Flink Processing
        B1[Data Cleansing]
        B2[Session Recognition]
        B3[Window Aggregation]
        B4[Feature Computation]
    end

    subgraph Feature Types
        C1[User Features<br/>1000-dim]
        C2[Item Features<br/>500-dim]
        C3[Cross Features<br/>200-dim]
        C4[Real-Time Features<br/>300-dim]
    end

    subgraph Storage
        D1[Redis<br/>TTL=1h]
        D2[HBase<br/>Permanent]
        D3[Flink State<br/>Session-level]
    end

    A1 --> B1 --> B2 --> B3 --> B4
    A2 --> B1
    A3 --> B1

    B4 --> C1 --> D1
    B4 --> C2 --> D2
    B4 --> C3 --> D1
    B4 --> C4 --> D3
```

### 7.3 Model Inference Service Architecture

```mermaid
graph TB
    subgraph Request Entry
        A1[API Gateway]
        A2[Load Balancer]
    end

    subgraph Recall Layer
        B1[i2i Recall<br/>Milvus]
        B2[Vector Recall<br/>Faiss]
        B3[Trending Recall<br/>Redis]
        B4[Operational Recall<br/>Config Center]
    end

    subgraph Ranking Layer
        C1[Coarse Ranking<br/>LightGBM]
        C2[Fine Ranking<br/>DeepFM]
        C3[TF Serving Cluster]
    end

    subgraph Reranking Layer
        D1[Diversity Control]
        D2[Novelty Boost]
        D3[Business Rules]
    end

    subgraph Output
        E1[Top50 Results]
        E2[CTR Prediction]
        E3[CVR Prediction]
    end

    A1 --> A2 --> B1 & B2 & B3 & B4
    B1 --> C1
    B2 --> C1
    B3 --> C1
    B4 --> C1

    C1 --> C2 --> C3 --> D1 --> E1
    C3 --> E2
    C3 --> E3
    D2 --> E1
    D3 --> E1
```

### 7.4 System Deployment Topology

```mermaid
graph TB
    subgraph Alibaba Cloud Region East China 1
        subgraph Availability Zone A
            A1[Flink JM x3]
            A2[Flink TM x50]
            A3[Kafka Broker x6]
        end

        subgraph Availability Zone B
            B1[Flink TM x50]
            B2[Redis Master x50]
            B3[TF Serving x10]
        end

        subgraph Availability Zone C
            C1[Flink TM x50]
            C2[Redis Slave x50]
            C3[Milvus x10]
        end
    end

    subgraph Cross-Region Disaster Recovery
        D1[Region North China 2<br/>Read-Only Replica]
    end

    A1 --> A2
    A2 --> A3
    A2 -.-> B1
    B1 --> B2
    B1 -.-> C1
    C1 --> C2
    C2 -.-> D1
    B3 --> C3
```

---

## 8. References

---

*This document follows the AnalysisDataFlow project six-section template specification | Last Updated: 2026-04-11*
