# 业务模式: 游戏实时分析 (business-pattern: gaming-analytics)

> **所属阶段**: knowledge/03-business-patterns | **前置依赖**: [pattern-event-time-processing](../02-design-patterns/pattern-event-time-processing.md), [pattern-windowed-aggregation](../02-design-patterns/pattern-windowed-aggregation.md), [pattern-side-output](../02-design-patterns/pattern-side-output.md) | **形式化等级**: l4-l5
>
> 本模式解决游戏行业中**游戏事件采集**、**实时 dau 计算**、**异常行为检测**与**充值流水分析**的核心需求，提供基于 flink + pulsar + actor 模型的完整解决方案。

---

## 目录

- [业务模式: 游戏实时分析 (business-pattern: gaming-analytics)](#业务模式-游戏实时分析-business-pattern-gaming-analytics)
  - [目录](#目录)
  - [1. 概念定义 (definitions)](#1-概念定义-definitions)
    - [def-k-03-07: 游戏事件 (game-event)](#def-k-03-07-游戏事件-game-event)
    - [def-k-03-08: 日活跃用户 (dau)](#def-k-03-08-日活跃用户-dau)
    - [def-k-03-09: 异常行为模式 (abnormal-behavior-pattern)](#def-k-03-09-异常行为模式-abnormal-behavior-pattern)
  - [2. 属性推导 (properties)](#2-属性推导-properties)
    - [prop-k-03-07: dau 计算单调性](#prop-k-03-07-dau-计算单调性)
    - [prop-k-03-08: 异常检测实时性边界](#prop-k-03-08-异常检测实时性边界)
    - [prop-k-03-09: 充值分析一致性](#prop-k-03-09-充值分析一致性)
  - [3. 关系建立 (relations)](#3-关系建立-relations)
    - [3.1 与核心设计模式的关系](#31-与核心设计模式的关系)
    - [3.2 技术栈组件映射](#32-技术栈组件映射)
    - [3.3 与 actor 模型的集成](#33-与-actor-模型的集成)
  - [4. 论证过程 (argumentation)](#4-论证过程-argumentation)
    - [4.1 业务场景特点分析](#41-业务场景特点分析)
    - [4.2 异常行为检测策略](#42-异常行为检测策略)
    - [4.3 实时 vs 离线分析权衡](#43-实时-vs-离线分析权衡)
  - [5. 工程论证 (engineering-argument)](#5-工程论证-engineering-argument)
    - [5.1 架构设计决策](#51-架构设计决策)
    - [5.2 性能基准](#52-性能基准)
  - [6. 实例验证 (examples)](#6-实例验证-examples)
    - [6.1 实时 dau 计算](#61-实时-dau-计算)
    - [6.2 异常行为检测 (cep)](#62-异常行为检测-cep)
    - [6.3 充值流水实时分析](#63-充值流水实时分析)
    - [6.4 游戏会话分析](#64-游戏会话分析)
  - [7. 可视化 (visualizations)](#7-可视化-visualizations)
    - [7.1 游戏数据流架构](#71-游戏数据流架构)
    - [7.2 实时指标计算](#72-实时指标计算)
  - [8. 引用参考 (references)](#8-引用参考-references)

---

## 1. 概念定义 (definitions)

### def-k-03-07: 游戏事件 (game-event)

设玩家集合为 $P = \{p_1, p_2, \ldots, p_n\}$，游戏世界状态为 $\mathcal{W}$，事件类型集合为 $E = \{\text{login}, \text{logout}, \text{levelup}, \text{battle}, \text{payment}, \ldots\}$。

**游戏事件**定义为六元组：

$$
g = (p, e, a, w, s, t) \in P \times E \times \mathcal{A} \times \mathcal{W} \times S \times \mathbb{T}
$$

其中：

- $p \in P$ 为玩家标识
- $e \in E$ 为事件类型
- $a \in \mathcal{A}$ 为事件属性（如战斗结果、充值金额）
- $w \in \mathcal{W}$ 为世界状态快照
- $s \in S$ 为服务器/分区标识
- $t \in \mathbb{T}$ 为事件时间戳

### def-k-03-08: 日活跃用户 (dau)

dau 是游戏核心运营指标，定义为：

$$
\text{dau}(t) = |\{ p \in P \mid \exists g \in G(p, [t-24h, t]) \}|
$$

其中 $G(p, \Delta)$ 表示玩家 $p$ 在时间区间 $\Delta$ 内产生的事件集合。

### def-k-03-09: 异常行为模式 (abnormal-behavior-pattern)

异常行为由偏离正常统计分布的事件序列定义：

$$
\text{abnormal}(p) \iff \exists f \in \mathcal{F}: \left| \frac{f(p) - \mu_f}{\sigma_f} \right| > \theta_{\text{threshold}}
$$

其中：

- $\mathcal{F}$ 为行为特征集合（如登录频率、操作速度、资源获取速率）
- $\mu_f, \sigma_f$ 为特征 $f$ 的均值和标准差
- $\theta_{\text{threshold}}$ 为异常判定阈值（通常 3-5 个标准差）

---

## 2. 属性推导 (properties)

### prop-k-03-07: dau 计算单调性

**命题**: 若使用事件时间处理，dau 计算结果具有单调不减性（在窗口内）。

**证明**:
设时间窗口为 $[t_0, t_1]$，在时刻 $\tau$ 观测到的 dau 为：

$$
\text{dau}(\tau) = |\{ p \mid \exists g: t_g \in [t_0, \min(\tau, t_1)] \}|
$$

对于 $\tau_1 < \tau_2$：

$$
\{ p \mid \exists g: t_g \in [t_0, \min(\tau_1, t_1)] \} \subseteq \{ p \mid \exists g: t_g \in [t_0, \min(\tau_2, t_1)] \}
$$

因此 $\text{dau}(\tau_1) \leq \text{dau}(\tau_2)$，即 dau 在窗口内单调不减。

### prop-k-03-08: 异常检测实时性边界

**命题**: 异常检测的实时性受限于窗口大小和 watermark 延迟。

**证明**:
设滑动窗口大小为 $\Delta_w$，滑动间隔为 $\Delta_s$，watermark 延迟为 $\delta_w$。

事件 $g$ 到达后，异常检测的最快触发时间为：

$$
t_{\text{alert}} \leq t_g + \delta_w + \Delta_s
$$

对于会话内实时异常检测，使用 processing time 可将延迟降至：

$$
t_{\text{alert}} \leq t_g + \delta_{\text{proc}}
$$

其中 $\delta_{\text{proc}}$ 为纯处理延迟（通常 < 100ms）。

### prop-k-03-09: 充值分析一致性

**命题**: 在 exactly-once 语义下，充值金额统计不会重复或丢失。

**证明要点**:

1. 充值事件由 pulsar 持久化存储
2. flink 通过 checkpoint 记录消费 offset
3. 故障恢复时从 checkpoint offset 重放
4. idempotent sink 确保重复事件只生效一次

因此充值统计满足一致性：

$$
\sum \text{payment}(p) = \sum_{\text{exactly-once}} \text{amount}(g_{\text{payment}})
$$

---

## 3. 关系建立 (relations)

### 3.1 与核心设计模式的关系

| 模式 | 关系类型 | 说明 |
|------|----------|------|
| **p01: event-time-processing** | 强依赖 | dau 等运营指标必须基于事件时间保证准确性 [^1] |
| **p02: windowed-aggregation** | 强依赖 | 实时指标计算依赖窗口聚合 [^2] |
| **p06: side-output** | 强依赖 | 异常事件通过侧输出分流处理 [^3] |
| **p05: state-management** | 配合 | 玩家会话状态维护 |
| **p07: checkpoint-recovery** | 配合 | 充值分析需要 exactly-once 保证 |

### 3.2 技术栈组件映射

```
┌─────────────────────────────────────────────────────────────────┐
│                    游戏实时分析技术栈映射                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   游戏服务器层                                                   │
│   ├── actor 模型: 游戏逻辑处理 (akka/pekko)                      │
│   ├── 事件采集: 游戏内事件实时上报                               │
│   └── 批量发送: 10s 批量发送到消息队列                            │
│                                                                 │
│   消息队列层 (pulsar)                                            │
│   ├── 多租户: 不同游戏/分区隔离                                  │
│   ├── 持久化: 事件不丢失                                         │
│   ├── geo-replication: 多数据中心同步                            │
│   └── 分区策略: player-id 哈希保证顺序                            │
│                                                                 │
│   流处理层 (flink)                                               │
│   ├── 事件解析: 反序列化、字段提取                                │
│   ├── 窗口聚合: 滑动窗口计算 dau/收入                             │
│   ├── 异常检测: cep 模式匹配外挂行为                              │
│   ├── 侧输出: 异常事件分流                                        │
│   └── 多维分析: 服务器/渠道/版本分组                              │
│                                                                 │
│   存储层                                                         │
│   ├── clickhouse: 明细事件存储                                    │
│   ├── druid/pinot: 实时 olap 查询                                 │
│   ├── redis: 实时指标缓存                                         │
│   └── mysql: 维度表                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 与 actor 模型的集成

游戏服务器通常采用 actor 模型处理并发，与 flink 的集成点：

```
游戏服务器 (actor)
  │
  ├─ 游戏事件 actor
  │     ├─ 处理游戏逻辑
  │     └─ 生成事件 → event collector actor
  │
  └─ event collector actor
        ├─ 批量缓冲 (10s/1000 事件)
        └─ 发送到 pulsar

pulsar
  │
  └─ topic: game-events-{server-id}

flink
  │
  └─ source: 消费 game-events 分区
```

---

## 4. 论证过程 (argumentation)

### 4.1 业务场景特点分析

**场景 1: mmo 大型多人在线游戏**

| 特点 | 技术挑战 | 解决方案 |
|------|----------|----------|
| 同屏人数多 (100+) | 高频事件爆发 | 服务器本地聚合 + 批量发送 |
| 实时战斗同步 | 延迟敏感 | actor 模型本地处理，旁路分析 |
| 跨服玩法 | 数据分散 | 统一事件格式，中心聚合 |
| 充值实时到账 | 一致性要求高 | exactly-once 处理 |

**场景 2: 休闲竞技游戏**

| 特点 | 技术挑战 | 解决方案 |
|------|----------|----------|
| 单局时长短 (3-5min) | 会话窗口频繁开关 | 动态会话 gap 配置 |
| 匹配算法依赖 | 实时匹配质量分析 | 滑动窗口统计匹配指标 |
| 外挂检测急迫 | 实时异常检测 | processing time 快速路径 |
| 留存敏感 | 流失预警 | 行为模式偏离检测 |

**场景 3: 卡牌/策略游戏**

| 特点 | 技术挑战 | 解决方案 |
|------|----------|----------|
| 付费点设计复杂 | 付费漏斗分析 | 事件归因链路追踪 |
| 养成周期长 | 长期价值预测 | 特征工程 + 滚动窗口 |
| 运营活动频繁 | 活动效果实时评估 | 对比窗口分析 |

### 4.2 异常行为检测策略

**策略 1: 基于统计阈值**

```
特征: 每分钟操作次数
阈值: μ + 3σ (正常玩家均值 + 3 倍标准差)
判定: 超过阈值标记为可疑
```

**策略 2: 基于 cep 模式**

```
模式: 速度异常
- 5 秒内移动距离 > 正常速度上限
- 连续击败 10 个玩家无死亡
- 资源获取速率 > 理论上限
```

**策略 3: 基于机器学习**

```
输入: 玩家行为序列
模型: lstm/autoencoder
输出: 异常分数
判定: 分数 > 阈值，人工复核
```

### 4.3 实时 vs 离线分析权衡

| 指标类型 | 实时需求 | 延迟容忍 | 实现方式 |
|----------|----------|----------|----------|
| dau/mau | 高 (运营看板) | < 1min | flink 滑动窗口 |
| 在线人数 | 高 (服务器扩容) | < 10s | 全局窗口 + 定时触发 |
| 充值金额 | 高 (财务监控) | < 1min | tumbling window |
| 留存率 | 低 | t+1d | 离线计算 |
| arpu/ltv | 低 | t+1d | 离线计算 |
| 外挂检测 | 高 | < 1min | cep + 侧输出 |

---

## 5. 工程论证 (engineering-argument)

### 5.1 架构设计决策

**决策 1: 为什么使用 pulsar 而非 kafka**

| 维度 | pulsar | kafka |
|------|--------|-------|
| 多租户 | 原生支持 | 需额外隔离 |
| geo-replication | 内置 | mirror-maker |
| 存储分离 | 计算存储分离 | 紧耦合 |
| 游戏适用性 | **推荐** | 可用 |

mmo 游戏需要多区服数据汇聚和异地容灾，pulsar 更合适。

**决策 2: 游戏服务器与 flink 的耦合策略**

| 策略 | 描述 | 适用场景 |
|------|------|----------|
| 旁路分析 | 游戏逻辑与 analytics 解耦 | **推荐**，不影响游戏性能 |
| 嵌入式 | flink 嵌入游戏进程 | 小规模，需要 colocation |
| 混合式 | 关键路径嵌入式，旁路批量 | 复杂场景 |

选择旁路分析，保证游戏核心性能。

**决策 3: 状态后端选择**

| 场景 | 推荐后端 | 原因 |
|------|----------|------|
| dau 计算 | heap | 状态小，恢复快 |
| 玩家会话 | rocksdb | 状态大，需持久化 |
| 充值分析 | rocksdb | exactly-once 要求 |

### 5.2 性能基准

| 指标 | 目标值 | 测试条件 |
|------|--------|----------|
| 事件吞吐 | 100万 tps | 1kb 事件 |
| dau 更新延迟 | < 30s | 滑动窗口 1min |
| 异常检测延迟 | < 10s | cep 模式匹配 |
| 充值统计延迟 | < 1min | tumbling window 1min |
| 数据保留 | 90 天 | pulsar 持久化 |

---

## 6. 实例验证 (examples)

### 6.1 实时 dau 计算

**场景**: 计算游戏实时日活跃用户。

```scala
import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.api.windowing.assigners.tumblingeventtimewindows
import org.apache.flink.streaming.api.windowing.time.time

// 定义游戏登录事件
case class loginevent(playerid: string, serverid: string, channel: string, timestamp: long)

// 实时 dau 计算
val daustream = loginevents
  .assign timestampsandwatermarks(
    watermarkstrategy
      .forboundedoutoforderness[loginevent](duration.ofseconds(10))
      .withtimestampassigner((event, _) => event.timestamp)
  )
  .keyby(_.serverid)  // 按服务器分组
  .window(tumblingeventtimewindows.of(time.minutes(1)))  // 1 分钟窗口
  .aggregate(new dauaggregate())

// dau 聚合函数
class dauaggregate extends aggregatefunction[loginevent, mutable.set[string], dauresult] {
  override def createaccumulator(): mutable.set[string] = mutable.set.empty

  override def add(event: loginevent, acc: mutable.set[string]): mutable.set[string] = {
    acc += event.playerid
    acc
  }

  override def getresult(acc: mutable.set[string]): dauresult = dauresult(
    windowtime = 0,  // 在 window function 中填充
    uniqueplayers = acc.size,
    playerids = acc.toset  // 可选：输出玩家列表
  )

  override def merge(a: mutable.set[string], b: mutable.set[string]): mutable.set[string] = {
    a ++= b
    a
  }
}

// 多维度 dau 统计
val multidimdaustream = loginevents
  .map(event => (event.serverid, event.channel, event.playerid, event.timestamp))
  .keyby(t => (t._1, t._2))  // 按服务器+渠道分组
  .window(tumblingeventtimewindows.of(time.minutes(1)))
  .process(new multidimdaufunction())
```

### 6.2 异常行为检测 (cep)

**场景**: 检测外挂加速行为。

```scala
import org.apache.flink.cep.scala.cep
import org.apache.flink.cep.scala.pattern.pattern

// 定义移动事件
case class moveevent(playerid: string, position: (double, double), timestamp: long)

// 定义速度异常模式：短时间内移动距离过大
val speedcheatpattern = pattern
  .begin[moveevent]("first")
  .where(_.position != null)
  .next("second")
  .where { (event, ctx) =>
    val firstevent = ctx.geteventsforpattern("first").head
    val timediff = event.timestamp - firstevent.timestamp
    val distancediff = calculatedistance(firstevent.position, event.position)
    val speed = distancediff / (timediff / 1000.0)  // 米/秒

    // 速度超过游戏设定上限 (如 50m/s)
    speed > 50.0 && timediff < 5000  // 5 秒内
  }
  .next("third")
  .where { (event, ctx) =>
    val secondevent = ctx.geteventsforpattern("second").head
    val timediff = event.timestamp - secondevent.timestamp
    val distancediff = calculatedistance(secondevent.position, event.position)
    val speed = distancediff / (timediff / 1000.0)

    // 连续异常加速
    speed > 50.0 && timediff < 5000
  }
  .within(time.seconds(10))

// 应用模式匹配
val cheatstream = cep.pattern(moveevents.keyby(_.playerid), speedcheatpattern)
  .process(new patternhandler[moveevent, cheatalert]() {
    override def processmatch(
      matchmap: map[string, list[moveevent]],
      ctx: context,
      out: collector[cheatalert]
    ): unit = {
      val playerid = matchmap("first").head.playerid
      val positions = matchmap.values.flatten.map(_.position).tolist

      out.collect(cheatalert(
        playerid = playerid,
        alerttype = "speed_cheat",
        description = s"玩家 $playerid 检测到异常加速",
        positions = positions,
        timestamp = ctx.timestamp()
      ))
    }
  })

// 异常事件侧输出到专门处理流
cheatstream.addsink(new cheatauditsink())
```

### 6.3 充值流水实时分析

**场景**: 实时监控充值金额，检测异常充值模式。

```scala
// 定义充值事件
case class paymentevent(
  playerid: string,
  orderid: string,
  amount: double,
  currency: string,
  channel: string,
  timestamp: long
)

// 充值金额实时统计
val paymentstream = paymentevents
  .assign timestampsandwatermarks(
    watermarkstrategy
      .forboundedoutoforderness[paymentevent](duration.ofseconds(5))
      .withtimestampassigner((event, _) => event.timestamp)
  )
  .keyby(_.channel)  // 按支付渠道分组
  .window(tumblingeventtimewindows.of(time.minutes(1)))  // 每分钟统计
  .aggregate(new paymentaggregate())

// 充值聚合结果
case class paymentstats(
  windowstart: long,
  channel: string,
  totalamount: double,
  ordercount: int,
  uniqueplayers: int,
  avgamount: double,
  maxamount: double
)

// 异常充值检测 (侧输出)
val latepaymenttag = outputtag[paymentevent]("suspicious-payment")

val validatedpayments = paymentevents
  .process(new paymentvalidationfunction(latepaymenttag))

// 处理可疑充值
val suspiciouspayments: datastream[paymentevent] = validatedpayments.getsideoutput(latepaymenttag)
suspiciouspayments.addsink(new fraudalertsink())

// 充值验证函数
class paymentvalidationfunction(lateoutputtag: outputtag[paymentevent])
  extends processfunction[paymentevent, paymentevent] {

  private var playerhistory: mapstate[string, list[paymentevent]] = _

  override def open(parameters: configuration): unit = {
    playerhistory = getruntimecontext.getmapstate(
      new mapstatedescriptor[string, list[paymentevent]]("payment-history", classof[string], classof[list[paymentevent]])
    )
  }

  override def processelement(
    event: paymentevent,
    ctx: context,
    out: collector[paymentevent]
  ): unit = {
    val history = option(playerhistory.get(event.playerid)).getorelse(list.empty)
    val recentamount = history.filter(_.timestamp > event.timestamp - 3600000).map(_.amount).sum  // 过去 1 小时

    // 检测异常：1 小时内累计充值超过阈值
    if (recentamount + event.amount > 10000.0) {
      ctx.output(lateoutputtag, event)  // 侧输出可疑交易
    }

    // 更新历史
    val updatedhistory = (event :: history).take(100)  // 保留最近 100 笔
    playerhistory.put(event.playerid, updatedhistory)

    out.collect(event)  // 正常输出
  }
}
```

### 6.4 游戏会话分析

**场景**: 分析玩家游戏会话时长和活跃度。

```scala
// 游戏事件
case class gameevent(playerid: string, eventtype: string, timestamp: long)

// 会话窗口分析
val sessionstream = gameevents
  .assign timestampsandwatermarks(
    watermarkstrategy
      .forboundedoutoforderness[gameevent](duration.ofseconds(15))
      .withtimestampassigner((event, _) => event.timestamp)
  )
  .keyby(_.playerid)
  .window(events timesessionwindows.withgap(time.minutes(5)))  // 5 分钟无事件视为会话结束
  .allowedlateness(time.seconds(30))
  .process(new sessionanalyzer())

// 会话分析结果
case class playersession(
  playerid: string,
  sessionstart: long,
  sessionend: long,
  duration: long,
  eventcount: int,
  loginlogout: int  // 登录登出次数
)

class sessionanalyzer extends processwindowfunction[gameevent, playersession, string, sessionwindow] {
  override def process(
    playerid: string,
    context: context,
    events: iterable[gameevent],
    out: collector[playersession]
  ): unit = {
    val sortedevents = events.tolist.sortby(_.timestamp)
    val starttime = sortedevents.head.timestamp
    val endtime = sortedevents.last.timestamp
    val duration = endtime - starttime

    val logincount = sortedevents.count(_.eventtype == "login")
    val logoutcount = sortedevents.count(_.eventtype == "logout")

    out.collect(playersession(
      playerid = playerid,
      sessionstart = starttime,
      sessionend = endtime,
      duration = duration,
      eventcount = sortedevents.size,
      loginlogout = logincount + logoutcount
    ))
  }
}
```

---

## 7. 可视化 (visualizations)

### 7.1 游戏数据流架构

```mermaid
graph tb
    subgraph "游戏服务器 (actor 模型)"
        gs1[游戏服 1<br/>akka cluster]
        gs2[游戏服 2<br/>akka cluster]
        gs3[游戏服 n<br/>akka cluster]
        actor[event collector actor]
    end

    subgraph "消息队列 (pulsar)"
        p1[topic: game-events]
        p2[topic: payment-events]
        p3[topic: login-events]
    end

    subgraph "flink 实时计算"
        src[source]
        wm[watermark]

        subgraph "指标计算"
            dau[dau 计算<br/>tumbling window]
            online[在线人数<br/>global window]
            revenue[收入统计<br/>tumbling window]
        end

        subgraph "异常检测"
            cep[cep 模式<br/>外挂检测]
            side[侧输出<br/>可疑事件]
        end

        subgraph "会话分析"
            sw[session window<br/>玩家会话]
            sa[会话聚合]
        end
    end

    subgraph "存储与展示"
        redis[(redis<br/>实时指标)]
        clickhouse[(clickhouse<br/>明细存储)]
        druid[(druid<br/>olap 查询)]
        grafana[grafana 看板]
    end

    gs1 --> actor --> p1
    gs2 --> actor --> p2
    gs3 --> actor --> p3

    p1 --> src --> wm
    p2 --> src
    p3 --> src

    wm --> dau --> redis
    wm --> online --> redis
    wm --> revenue --> redis
    wm --> cep --> side --> clickhouse
    wm --> sw --> sa --> druid

    redis --> grafana
    clickhouse --> grafana
    druid --> grafana
```

### 7.2 实时指标计算

```mermaid
flowchart lr
    a[游戏事件] --> b[event time 提取]
    b --> c[keyby 维度]
    c --> d[窗口分配]
    d -->|dau| e[tumbling 1min<br/>去重计数]
    d -->|在线| f[global window<br/>定时触发]
    d -->|收入| g[tumbling 1min<br/>金额求和]
    d -->|会话| h[session window<br/>5min gap]
    e --> i[实时看板]
    f --> i
    g --> i
    h --> j[留存分析]
```

---

## 8. 引用参考 (references)

[^1]: apache flink documentation, "event time and watermarks," 2025. <https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/>

[^2]: apache flink documentation, "windowing," 2025. <https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/operators/windows/>

[^3]: apache flink documentation, "side outputs," 2025. <https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/operators/side_output/>





---

*文档版本: v1.0 | 更新日期: 2026-04-02 | 状态: 已完成*
