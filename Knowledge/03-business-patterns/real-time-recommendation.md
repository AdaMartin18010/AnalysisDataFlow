# 业务模式: 实时推荐系统 (business-pattern: real-time-recommendation)

> **所属阶段**: knowledge/03-business-patterns | **前置依赖**: [pattern-windowed-aggregation](../02-design-patterns/pattern-windowed-aggregation.md), [pattern-async-io-enrichment](../02-design-patterns/pattern-async-io-enrichment.md), [pattern-state-management](../02-design-patterns/pattern-state-management.md) | **形式化等级**: l4-l5
>
> 本模式解决推荐系统中**点击流实时处理**、**用户特征计算**、**异步画像查询**与**top-k 推荐**的核心需求，提供基于 flink + redis + 特征服务的完整解决方案。

---

## 目录

- [1. 概念定义 (definitions)](#1-概念定义-definitions)
- [2. 属性推导 (properties)](#2-属性推导-properties)
- [3. 关系建立 (relations)](#3-关系建立-relations)
- [4. 论证过程 (argumentation)](#4-论证过程-argumentation)
- [5. 工程论证 (engineering-argument)](#5-工程论证-engineering-argument)
- [6. 实例验证 (examples)](#6-实例验证-examples)
- [7. 可视化 (visualizations)](#7-可视化-visualizations)
- [8. 引用参考 (references)](#8-引用参考-references)

---

## 1. 概念定义 (definitions)

### def-k-03-04: 用户行为事件 (user-behavior-event)

设用户集合为 $U = \{u_1, u_2, \ldots, u_m\}$，物品集合为 $I = \{i_1, i_2, \ldots, i_n\}$，行为类型集合为 $A = \{\text{click}, \text{view}, \text{cart}, \text{order}, \ldots\}$。

**用户行为事件**定义为五元组：

$$
e = (u, i, a, w, t) \in U \times I \times A \times \mathbb{R}_{\geq 0} \times \mathbb{T}
$$

其中 $w$ 为行为权重（如订单金额），$t$ 为事件时间戳。

### def-k-03-05: 实时用户画像 (real-time-user-profile)

用户 $u$ 的实时画像定义为时间窗口内的行为聚合向量：

$$
\text{profile}(u, t, \Delta) = \bigoplus_{e \in E(u, t, \Delta)} \phi(e)
$$

其中：

- $E(u, t, \Delta) = \{ e = (u, i, a, w, t_e) \mid t - \Delta \leq t_e \leq t \}$ 为时间窗口 $\Delta$ 内的事件集合
- $\phi(e)$ 为事件特征提取函数
- $\bigoplus$ 为聚合算子（如求和、计数、去重计数）

### def-k-03-06: 推荐候选集 (recommendation-candidates)

对于用户 $u$ 在时刻 $t$，推荐候选集为：

$$
\text{candidates}(u, t) = \{ i \in I \mid \text{score}(u, i, t) \geq \theta_{\text{min}} \}
$$

其中 $\text{score}(u, i, t)$ 为评分函数，$\theta_{\text{min}}$ 为最低相关性阈值。

top-k 推荐结果为：

$$
\text{topk}(u, t) = \underset{i \in \text{candidates}(u, t)}{\text{argmax}_k} \text{score}(u, i, t)
$$

---

## 2. 属性推导 (properties)

### prop-k-03-04: 特征新鲜度边界

**命题**: 实时特征计算的特征新鲜度上界为窗口触发延迟。

**证明**:
设事件到达时间为 $t_a$，窗口触发时间为 $t_t$，则特征新鲜度：

$$
\text{freshness} = t_t - t_a \leq \delta_{\text{window}} + \delta_{\text{watermark}}
$$

其中 $\delta_{\text{window}}$ 为窗口大小，$\delta_{\text{watermark}}$ 为 watermark 延迟。对于滑动窗口，特征更新间隔为 slide 间隔 $\delta_{\text{slide}}$。

### prop-k-03-05: 异步 i/o 并发度上界

**命题**: 异步 i/o 的并发度存在最优值，过高会导致下游压力过大。

**证明**:
设：

- 特征服务 qps 上限为 $q$
- flink 并行度为 $p$
- 每个算子实例并发度为 $c$

则总并发请求数为 $p \cdot c$。为避免压垮特征服务：

$$
p \cdot c \leq \alpha \cdot q
$$

其中 $\alpha \in (0, 1)$ 为安全因子（通常 0.8）。因此并发度上界为：

$$
c_{\max} = \frac{\alpha \cdot q}{p}
$$

### prop-k-03-06: 推荐结果一致性

**命题**: 在 exactly-once 语义下，同一用户同一时刻的推荐结果具有确定性。

**证明要点**:

1. 用户行为流按 user-id 分区，保证同一用户的事件顺序处理
2. keyed state 维护用户特征，checkpoint 保证状态一致性
3. 异步查询使用事件时间作为查询时间点，保证时序一致
4. top-k 计算基于确定性排序算法

因此，给定相同的事件历史和模型版本，推荐结果确定。

---

## 3. 关系建立 (relations)

### 3.1 与核心设计模式的关系

| 模式 | 关系类型 | 说明 |
|------|----------|------|
| **p02: windowed-aggregation** | 强依赖 | 用户行为统计依赖滑动窗口实时聚合 [^1] |
| **p04: async-i/o-enrichment** | 强依赖 | 用户画像、物品特征查询需要异步 i/o [^2] |
| **p05: state-management** | 强依赖 | 用户实时特征维护依赖 keyed state [^3] |
| **p01: event-time-processing** | 配合 | 确保行为时序正确性 |
| **p06: side-output** | 配合 | 特征缺失数据侧输出补全 |

### 3.2 技术栈组件映射

```
┌─────────────────────────────────────────────────────────────────┐
│                  实时推荐系统技术栈映射                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   数据采集层                                                     │
│   ├── 客户端 sdk: 埋点采集点击、曝光、转化                        │
│   ├── 日志收集: flume/filebeat → kafka                           │
│   └── 实时流: kafka topic (user-behavior)                        │
│                                                                 │
│   流处理层 (flink)                                               │
│   ├── 行为解析: 数据清洗、格式标准化                              │
│   ├── 窗口聚合: 滑动窗口统计用户行为特征                          │
│   ├── 异步查询: async i/o 查询用户/物品画像                       │
│   ├── 特征拼接: 实时特征 + 画像特征                               │
│   └── 模型推理: 特征向量 → 推荐评分                               │
│                                                                 │
│   特征服务层                                                     │
│   ├── redis: 热特征缓存 (用户近实时特征)                          │
│   ├── feature service: 特征计算与查询 api                         │
│   └── model serving: 模型推理服务 (tensorflow serving)            │
│                                                                 │
│   推荐结果层                                                     │
│   ├── 候选生成: 多路召回 (协同过滤、向量召回)                      │
│   ├── 精排服务: 深度模型排序                                      │
│   └── 结果缓存: redis 缓存推荐结果                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 特征计算时序关系

实时推荐系统的特征计算具有明确的时序依赖：

$$
\text{raw-events} \xrightarrow{\text{window-agg}} \text{realtime-features} \xrightarrow{\text{async-join}} \text{user-profile} \xrightarrow{\text{model-inference}} \text{recommendations}
$$

**特征分层**:

- **实时特征 (t+0)**: 过去 5 分钟内的行为统计
- **近实时特征 (t+5min)**: 过去 1 小时的行为统计
- **离线特征 (t+1h)**: 历史长期画像

---

## 4. 论证过程 (argumentation)

### 4.1 业务场景特点分析

**场景 1: 电商实时个性化推荐**

| 特点 | 技术挑战 | 解决方案 |
|------|----------|----------|
| 用户行为密集 | 高并发特征更新 | redis 热缓存 + 本地状态 |
| 兴趣漂移快 | 特征过期策略 | 滑动窗口 + ttl |
| 多样性需求 | 避免过度个性化 | exploration 机制 |
| 冷启动问题 | 新用户无历史 | 基于内容的默认推荐 |

**场景 2: 内容 feed 流推荐**

| 特点 | 技术挑战 | 解决方案 |
|------|----------|----------|
| 内容时效性强 | 实时内容发现 | 流式内容索引更新 |
| 用户停留时长 | 长短期兴趣平衡 | 多时间尺度特征 |
| 刷新频率高 | 推荐延迟敏感 | 预计算 + 实时修正 |

**场景 3: 广告实时竞价 (rtb)**

| 特点 | 技术挑战 | 解决方案 |
|------|----------|----------|
| 延迟极敏感 | < 50ms 响应 | 边缘计算 + 缓存 |
| 点击率预估 | 实时 ctr 特征 | 流式特征工程 |
| 预算控制 | 实时花费监控 | 滑动窗口统计 |

### 4.2 实时 vs 离线特征权衡

| 维度 | 实时特征 | 离线特征 |
|------|----------|----------|
| 延迟 | < 1s | t+1h ~ t+1d |
| 准确性 | 反映即时意图 | 反映长期兴趣 |
| 计算成本 | 高 | 低 |
| 稳定性 | 波动大 | 平滑稳定 |
| 适用场景 | 即时个性化、会话内推荐 | 基础画像、稳定性需求 |

**混合策略**:

$$
\text{final-score} = \alpha \cdot \text{realtime-score} + (1-\alpha) \cdot \text{offline-score}
$$

$\alpha$ 根据业务场景动态调整（通常 0.3-0.5）。

### 4.3 异步 i/o 超时处理策略

**问题**: 特征服务超时导致推荐延迟。

**策略 1: 快速失败 + 默认值**

```scala
async i/o with timeout = 50ms
  |- success → use returned features
  |- timeout → use default features (population average)
```

**策略 2: 降级缓存**

```scala
async i/o with timeout = 50ms
  |- success → update local cache, return features
  |- timeout → return stale features from local cache
```

**策略 3: 特征补齐**

```scala
partial features from async i/o
  + default values for missing dimensions
  → complete feature vector
```

---

## 5. 工程论证 (engineering-argument)

### 5.1 架构设计决策

**决策 1: 为什么使用滑动窗口而非滚动窗口**

| 维度 | sliding window | tumbling window |
|------|----------------|-----------------|
| 特征连续性 | 高（平滑过渡） | 低（跳跃式更新） |
| 计算成本 | 高（重复计算） | 低 |
| 实时性 | 高（更频繁更新） | 中 |
| 推荐适用性 | **推荐** | 低频场景 |

推荐系统需要平滑的用户兴趣变化感知，因此选择滑动窗口。

**决策 2: 状态后端与缓存策略**

| 存储 | 用途 | 配置 |
|------|------|------|
| flink keyed state | 窗口内聚合状态 | rocksdb，ttl=24h |
| redis | 用户特征缓存 | cluster 模式，过期策略 |
| local cache (caffeine) | 热点特征本地缓存 | lru，ttl=5min |

**多级缓存命中率**:

- l1 (local): 80%
- l2 (redis): 15%
- l3 (feature service): 5%

### 5.2 性能基准

| 指标 | 目标值 | 测试条件 |
|------|--------|----------|
| p99 延迟 | < 100ms | 含异步查询 |
| 吞吐 | 50万 tps | 100字节事件 |
| 特征服务查询 | < 20ms p99 | redis 命中 |
| 模型推理 | < 30ms p99 | 轻量级模型 |
| 特征新鲜度 | < 1min | 滑动窗口 5min slide 1min |

---

## 6. 实例验证 (examples)

### 6.1 用户行为实时特征计算

**场景**: 计算用户过去 5 分钟内的点击、收藏、加购统计。

```scala
import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.api.windowing.assigners.slidingeventtimewindows
import org.apache.flink.streaming.api.windowing.time.time

// 定义行为事件
case class behaviorevent(userid: string, itemid: string, action: string, timestamp: long)

// 定义用户特征
case class userfeatures(
  userid: string,
  windowstart: long,
  clickcount: int,
  cartcount: int,
  ordercount: int,
  totalamount: double
)

// 滑动窗口聚合：5 分钟窗口，1 分钟滑动
val userfeaturestream = behaviorevents
  .assign timestampsandwatermarks(
    watermarkstrategy
      .forboundedoutoforderness[behaviorevent](duration.ofseconds(5))
      .withtimestampassigner((event, _) => event.timestamp)
  )
  .keyby(_.userid)
  .window(slidingeventtimewindows.of(time.minutes(5), time.minutes(1)))
  .aggregate(new userbehavioraggregate())

// 聚合函数实现
class userbehavioraggregate extends aggregatefunction[behaviorevent, featureacc, userfeatures] {
  override def createaccumulator(): featureacc = featureacc(0, 0, 0, 0.0)

  override def add(event: behaviorevent, acc: featureacc): featureacc = event.action match {
    case "click" => acc.copy(clicks = acc.clicks + 1)
    case "cart" => acc.copy(carts = acc.carts + 1)
    case "order" => acc.copy(
      orders = acc.orders + 1,
      amount = acc.amount + event.value.getorelse(0.0)
    )
    case _ => acc
  }

  override def getresult(acc: featureacc): userfeatures = userfeatures(
    userid = "",  // 在 window function 中填充
    windowstart = 0,
    clickcount = acc.clicks,
    cartcount = acc.carts,
    ordercount = acc.orders,
    totalamount = acc.amount
  )

  override def merge(a: featureacc, b: featureacc): featureacc = featureacc(
    a.clicks + b.clicks,
    a.carts + b.carts,
    a.orders + b.orders,
    a.amount + b.amount
  )
}
```

### 6.2 异步查询用户画像

**场景**: 实时特征与离线画像拼接。

```scala
import org.apache.flink.streaming.api.scala.async.asyncfunction
import scala.concurrent.{executioncontext, future}

class asyncuserenrichment extends asyncfunction[userfeatures, enricheduser] {

  @transient private var featureservice: userfeatureclient = _

  override def open(parameters: configuration): unit = {
    featureservice = new userfeatureclient(redishost, redisport)
  }

  override def asyncinvoke(
    features: userfeatures,
    resultfuture: resultfuture[enricheduser]
  ): unit = {
    implicit val ec: executioncontext = executioncontext.global

    future {
      // 异步查询 redis 用户画像
      val userprofile = featureservice.getprofile(features.userid)
      val itemhistory = featureservice.getrecentitems(features.userid, 10)

      enricheduser(
        userid = features.userid,
        realtimefeatures = features,
        agegroup = userprofile.agegroup,
        gender = userprofile.gender,
        interests = userprofile.interesttags,
        recentitems = itemhistory
      )
    }.oncomplete {
      case scala.util.success(result) => resultfuture.complete(collections.singleton(result))
      case scala.util.failure(ex) =>
        // 超时或异常，使用默认值
        resultfuture.complete(collections.singleton(
          enricheduser.withdefaults(features.userid, features)
        ))
    }
  }

  override def timeout(
    features: userfeatures,
    resultfuture: resultfuture[enricheduser]
  ): unit = {
    // 超时处理：返回带默认值的结果
    resultfuture.complete(collections.singleton(
      enricheduser.withdefaults(features.userid, features)
    ))
  }
}

// 应用异步 i/o
val enrichedstream = userfeaturestream
  .keyby(_.userid)
  .process(new asyncwaitfunction(new asyncuserenrichment(), timeout = 50, capacity = 100))
```

### 6.3 top-k 推荐生成

**场景**: 基于实时特征生成 top-10 推荐。

```scala
// 候选物品召回
class candidategeneration extends processfunction[enricheduser, recommendationrequest] {

  @transient private var candidateservice: candidateserviceclient = _

  override def open(parameters: configuration): unit = {
    candidateservice = new candidateserviceclient()
  }

  override def processelement(
    user: enricheduser,
    ctx: context,
    out: collector[recommendationrequest]
  ): unit = {
    // 多路召回
    val cfitems = candidateservice.collaborativefiltering(user.userid, 100)
    val contentitems = candidateservice.contentbased(user.interests, 100)
    val trenditems = candidateservice.trending(50)

    // 合并候选集并去重
    val candidates = (cfitems ++ contentitems ++ trenditems).distinct.take(200)

    out.collect(recommendationrequest(
      userid = user.userid,
      userfeatures = user,
      candidates = candidates,
      timestamp = ctx.timestamp()
    ))
  }
}

// 精排与 top-k 选择
class rankingandselection extends processfunction[recommendationrequest, recommendation] {

  @transient private var modelservice: modelinferenceservice = _

  override def open(parameters: configuration): unit = {
    modelservice = new modelinferenceservice(tf servinghost)
  }

  override def processelement(
    request: recommendationrequest,
    ctx: context,
    out: collector[recommendation]
  ): unit = {
    // 批量推理评分
    val scores = modelservice.predictbatch(
      request.candidates.map(item =>
        featurevector(request.userfeatures, item)
      )
    )

    // 组合候选与评分
    val scoreditems = request.candidates.zip(scores)

    // 选择 top-k
    val topk = scoreditems
      .sortby(-_._2)  // 按评分降序
      .take(10)
      .map { case (item, score) => scoreditem(item.itemid, score) }

    out.collect(recommendation(
      userid = request.userid,
      items = topk,
      timestamp = ctx.timestamp(),
      requestid = uuid.randomuuid().tostring
    ))
  }
}
```

### 6.4 特征缺失处理

**场景**: 新用户或特征服务异常时的降级策略。

```scala
// 带降级策略的推荐流程
val recommendationstream = enrichedstream
  .process(new safeenrichmentfunction())

class safeenrichmentfunction
  extends processfunction[userfeatures, recommendation] {

  private var featurecache: mapstate[string, userprofile] = _
  private var errorcount: valuestate[int] = _

  override def open(parameters: configuration): unit = {
    featurecache = getruntimecontext.getmapstate(
      new mapstatedescriptor[string, userprofile]("profile-cache", classof[string], classof[userprofile])
    )
    errorcount = getruntimecontext.getstate(
      new valuestatedescriptor[int]("error-count", classof[int])
    )
  }

  override def processelement(
    features: userfeatures,
    ctx: context,
    out: collector[recommendation]
  ): unit = {
    val profile = try {
      // 尝试查询特征服务
      queryfeatureservice(features.userid)
    } catch {
      case _: timeoutexception =>
        // 超时，使用缓存
        featurecache.get(features.userid)
      case _: exception =>
        // 其他异常，使用默认画像
        userprofile.default
    }

    // 生成推荐
    val recs = if (profile != null) {
      generaterecommendations(features, profile)
    } else {
      // 完全缺失时使用热门兜底
      gettrendingrecommendations(10)
    }

    out.collect(recs)
  }
}
```

---

## 7. 可视化 (visualizations)

### 7.1 推荐架构图

```mermaid
graph tb
    subgraph "数据采集"
        app[移动 app/web]
        sdk[sdk 埋点]
        kafka1[kafka<br/>behavior-events]
    end

    subgraph "flink 实时计算"
        src[source]
        wm[watermark 5s]

        subgraph "特征计算"
            k[keyby userid]
            sw[sliding window<br/>5min/1min]
            agg[aggregate<br/>行为统计]
        end

        subgraph "特征增强"
            async[async i/o<br/>画像查询]
            redis[(redis<br/>用户画像)]
        end

        subgraph "推荐生成"
            recall[候选召回<br/>cf/cb/热门]
            rank[精排模型<br/>tensorflow serving]
            topk[top-10 选择]
        end
    end

    subgraph "存储层"
        redis2[(redis<br/>推荐结果)]
        hbase[(hbase<br/>历史记录)]
    end

    subgraph "服务层"
        api[推荐 api]
        cache[结果缓存]
    end

    app --> sdk --> kafka1 --> src --> wm --> k --> sw --> agg --> async
    redis -.-> async --> recall --> rank --> topk
    topk --> redis2 --> api --> cache --> app
    topk -.-> hbase
```

### 7.2 特征计算流程

```mermaid
flowchart lr
    a[点击事件] --> b[event time 提取]
    b --> c[keyby user]
    c --> d[滑动窗口<br/>5min window<br/>1min slide]
    d --> e[聚合计算<br/>click/cart/order]
    e --> f[async 查询画像]
    f -->|命中| g[特征拼接]
    f -->|超时| h[使用缓存/默认]
    g --> i[特征向量]
    h --> i
    i --> j[模型推理]
    j --> k[top-k 排序]
```

### 7.3 模型推理集成

```mermaid
graph tb
    subgraph "特征工程"
        f1[实时特征<br/>滑动窗口]
        f2[离线特征<br/>用户画像]
        f3[上下文特征<br/>时间/位置]
    end

    subgraph "特征拼接"
        join[特征向量拼接<br/>vector assembly]
    end

    subgraph "模型推理"
        m1[召回模型<br/>双塔模型/ann]
        m2[粗排模型<br/>轻量级 gbdt]
        m3[精排模型<br/>深度网络]
    end

    subgraph "后处理"
        p1[多样性控制<br/>mmr/dpp]
        p2[业务规则<br/>过滤/加权]
        p3[结果缓存<br/>redis]
    end

    f1 --> join
    f2 --> join
    f3 --> join
    join --> m1 --> m2 --> m3
    m3 --> p1 --> p2 --> p3
```

---

## 8. 引用参考 (references)

[^1]: apache flink documentation, "windowing," 2025. <https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/operators/windows/>

[^2]: apache flink documentation, "async i/o," 2025. <https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/operators/asyncio/>

[^3]: apache flink documentation, "working with state," 2025. <https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/state/state/>




---

*文档版本: v1.0 | 更新日期: 2026-04-02 | 状态: 已完成*
