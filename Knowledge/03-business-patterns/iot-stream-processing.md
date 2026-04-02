# 业务模式: iot物联网流处理 (business-pattern: iot-stream-processing)

> **所属阶段**: knowledge/03-business-patterns | **前置依赖**: [pattern-event-time-processing](../02-design-patterns/pattern-event-time-processing.md), [pattern-state-management](../02-design-patterns/pattern-state-management.md), [pattern-checkpoint-recovery](../02-design-patterns/pattern-checkpoint-recovery.md) | **形式化等级**: l4-l5
>
> 本模式解决物联网场景下**百万级设备接入**、**乱序数据处理**、**设备状态维护**与**会话窗口管理**的核心需求，提供基于 flink + mqtt + 时序数据库的完整解决方案。

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

### def-k-03-01: iot数据流 (iot-data-stream)

设设备集合为 $D = \{d_1, d_2, \ldots, d_n\}$，每个设备 $d_i$ 产生的事件序列构成数据流：

$$
S_i = \{(e_{i1}, t_{i1}), (e_{i2}, t_{i2}), \ldots\}
$$

其中 $e_{ij}$ 表示第 $i$ 个设备的第 $j$ 个事件，$t_{ij} \in \mathbb{T}$ 为事件时间戳。

**iot数据流**定义为所有设备流的并集：

$$
S_{\text{iot}} = \bigcup_{i=1}^{n} S_i
$$

### def-k-03-02: 设备会话 (device-session)

设备会话是单个设备在活跃时间段内产生的事件集合，定义为：

$$
\text{Session}(d_i) = \{ (e, t) \in S_i \mid t_{\text{start}} \leq t \leq t_{\text{end}} \}
$$

其中会话边界满足**不活跃间隙条件**：

$$
gap(t_{\text{end}}, t_{\text{next}}) > \theta_{\text{session}}
$$

$\theta_{\text{session}}$ 为会话超时阈值，通常配置为 5-30 分钟。

### def-k-03-03: 乱序容忍度 (out-of-order-tolerance)

设事件 $e$ 的事件时间为 $t_e$，到达时间为 $t_a$，乱序延迟定义为：

$$
\delta(e) = t_a - t_e
$$

系统的乱序容忍度 $\delta_{\max}$ 满足：

$$
\forall e \in S_{\text{iot}}: \delta(e) \leq \delta_{\max} \Rightarrow e \text{ 被正确处理}
$$

典型物联网场景下，$\delta_{\max} \in [10s, 60s]$。

---

## 2. 属性推导 (properties)

### prop-k-03-01: 设备状态一致性

**命题**: 在 checkpoint 机制下，设备状态在故障恢复后保持一致。

**证明要点**:

1. 设 checkpoint 周期为 $\tau_c$，状态快照为 $\Sigma_k$ 在时间 $t_k$
2. 故障发生在 $t_f \in (t_k, t_{k+1})$
3. 从 $\Sigma_k$ 恢复后，source 从 offset $o_k$ 重放
4. 由于 exactly-once 语义，每个事件 $e$ 的副作用只应用一次
5. 因此设备状态 $\sigma(d_i)$ 在恢复后与故障前一致

### prop-k-03-02: 会话窗口完整性

**命题**: 使用 event time 会话窗口时，乱序事件不会导致会话分裂。

**证明要点**:
设事件 $e_1, e_2$ 属于同一设备，事件时间满足 $t_1 < t_2$ 且 $t_2 - t_1 < \theta_{\text{session}}$。

即使到达顺序为 $e_2$ 先于 $e_1$，只要：

$$
t_1 > w_{\text{current}} - \delta_{\max}
$$

其中 $w_{\text{current}}$ 为当前 watermark，则 $e_1$ 仍被纳入会话窗口，保证会话完整性。

### prop-k-03-03: 状态空间上界

**命题**: 使用 ttl 管理的 keyed state，状态空间复杂度为 $O(|D| \cdot s_{\max})$。

其中 $|D|$ 为活跃设备数，$s_{\max}$ 为单设备最大状态大小。

**证明**: 每个设备的状态在超时后被清理，因此状态只与当前活跃设备数成正比，而非历史累计设备数。

---

## 3. 关系建立 (relations)

### 3.1 与核心设计模式的关系

| 模式 | 关系类型 | 说明 |
|------|----------|------|
| **p01: event-time-processing** | 强依赖 | iot 场景必须使用事件时间处理边缘网关批量上报导致的乱序 [^1] |
| **p05: state-management** | 强依赖 | 设备状态维护依赖 keyed state 和 ttl 管理 [^2] |
| **p07: checkpoint-recovery** | 强依赖 | 设备状态持久化依赖 checkpoint 机制保证容错 [^3] |
| **p02: windowed-aggregation** | 配合 | 会话窗口用于设备活跃期分析 |
| **p06: side-output** | 配合 | 迟到数据通过侧输出进行离线补录 |

### 3.2 技术栈组件映射

```
┌─────────────────────────────────────────────────────────────────┐
│                    iot 流处理技术栈映射                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   数据采集层                                                     │
│   ├── mqtt broker (emqx/mosquitto): 百万级设备连接              │
│   ├── mqtt 协议: qos 0/1/2 分级可靠性                           │
│   └── 边缘网关: 本地聚合、协议转换、离线缓存                       │
│                                                                 │
│   消息缓冲层                                                     │
│   ├── kafka: 高吞吐事件流缓冲                                    │
│   ├── 分区策略: device-id 哈希保证顺序                           │
│   └── 保留策略: 7 天用于故障恢复                                 │
│                                                                 │
│   流处理层 (flink)                                               │
│   ├── event time processing: 乱序数据重排                        │
│   ├── keyed state: 设备级状态维护                                │
│   ├── session windows: 设备会话分析                              │
│   └── checkpoint: 状态持久化与容错                               │
│                                                                 │
│   存储层                                                         │
│   ├── 时序数据库 (influxdb/tdengine): 指标存储                   │
│   ├── hbase/cassandra: 设备画像与元数据                          │
│   └── redis: 热状态缓存                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 数据流时序关系

iot 数据流的特殊时序特性：

$$
t_{\text{event}} < t_{\text{gateway}} < t_{\text{ingestion}} < t_{\text{processing}}
$$

其中：

- $t_{\text{event}}$: 传感器采样时间
- $t_{\text{gateway}}$: 边缘网关聚合时间
- $t_{\text{ingestion}}$: 进入 kafka 时间
- $t_{\text{processing}}$: flink 处理时间

乱序主要来源于边缘网关的批量上报策略。

---

## 4. 论证过程 (argumentation)

### 4.1 业务场景特点分析

**场景 1: 智能制造设备监控**

| 特点 | 技术挑战 | 解决方案 |
|------|----------|----------|
| 传感器高频采样 (1-10hz) | 数据量大，需边缘聚合 | 边缘网关 10s 批量上报 |
| 网络不稳定 (4g/wifi) | 数据丢失与乱序 | mqtt qos 1 + 事件时间窗口 |
| 设备状态实时告警 | 低延迟要求 | 滚动窗口 (5s) + 侧输出 |
| 历史趋势分析 | 长期存储 | 时序数据库自动降采样 |

**场景 2: 车联网 telematics**

| 特点 | 技术挑战 | 解决方案 |
|------|----------|----------|
| 车辆移动导致网络切换 | 连接不稳定 | 车辆级 keyed state 持久化 |
| 地理位置相关计算 | 需要地理围栏 | cep 模式匹配 |
| 驾驶行为分析 | 会话内聚合 | 会话窗口 (5min gap) |
| 事故实时检测 | 极低延迟 | 旁路规则引擎 |

**场景 3: 智能家居**

| 特点 | 技术挑战 | 解决方案 |
|------|----------|----------|
| 设备数量巨大 (>1000万) | 水平扩展 | kafka 分区 + flink 并行度 |
| 设备唤醒/休眠频繁 | 会话管理 | 动态会话窗口 |
| 用户场景联动 | 跨设备关联 | 异步 i/o 查询用户配置 |

### 4.2 mqtt 消息可靠性级别选择

**qos 0 (at most once)**:

- 适用: 高频传感器数据，丢失可容忍
- 延迟: 最低
- 带宽: 最小

**qos 1 (at least once)**:

- 适用: 设备状态变更、告警事件
- 延迟: 中等
- 注意: flink 需幂等处理重复消息

**qos 2 (exactly once)**:

- 适用: 控制指令、固件升级指令
- 延迟: 最高
- 成本: 4 次握手

### 4.3 边缘计算与中心计算的分界

```
边缘层 (边缘网关)              中心层 (flink 集群)
┌─────────────────┐           ┌─────────────────┐
│ 数据预处理       │           │ 复杂事件处理    │
│ - 数据清洗      │           │ - 跨设备关联    │
│ - 单位转换      │──────────►│ - 历史趋势分析  │
│ - 简单聚合      │           │ - 机器学习推理  │
│ - 本地缓存      │           │ - 全局状态管理  │
└─────────────────┘           └─────────────────┘
      10s-60s 批量上报
```

---

## 5. 工程论证 (engineering-argument)

### 5.1 架构设计决策

**决策 1: 为什么使用 event time 而非 processing time**

| 维度 | event time | processing time |
|------|------------|-----------------|
| 正确性 | 高（结果可复现） | 低（依赖到达顺序） |
| 延迟 | 中（+watermark 延迟） | 低 |
| 状态复杂度 | 高（需管理乱序） | 低 |
| iot 适用性 | **推荐** | 仅用于近似监控 |

iot 场景需要准确的设备会话分析和告警，必须保证结果确定性，因此选择 event time。

**决策 2: 状态后端选择**

| 维度 | rocksdb | heap |
|------|---------|------|
| 状态大小 | 大（tb 级） | 小（内存限制） |
| 性能 | 中（磁盘 io） | 高 |
| 恢复速度 | 慢（需加载 sst） | 快 |
| iot 推荐 | **推荐**（设备数多） | 小规模部署 |

**决策 3: 窗口类型选择**

| 场景 | 窗口类型 | 配置 |
|------|----------|------|
| 实时告警 | tumbling window | 10s |
| 设备会话分析 | session window | 5min gap |
| 趋势分析 | sliding window | 1h window / 1min slide |
| 日级统计 | tumbling window | 1d |

### 5.2 性能基准

| 指标 | 目标值 | 测试条件 |
|------|--------|----------|
| 峰值吞吐 | 100万 tps | 100字节消息 |
| 端到端延迟 (p99) | < 2s | 含 30s watermark 延迟 |
| flink 处理延迟 | < 100ms | 纯计算时间 |
| 状态恢复时间 | < 2min | 100gb 状态 |
| checkpoint 间隔 | 30s | 平衡性能与恢复 |

---

## 6. 实例验证 (examples)

### 6.1 设备温度监控告警

**场景**: 工业锅炉温度传感器监控，超过阈值触发告警。

```scala
import org.apache.flink.streaming.api.scala._
import org.apache.flink.api.common.eventtime.watermarkstrategy
import org.apache.flink.streaming.api.windowing.assigners.tumblingeventtimewindows
import org.apache.flink.streaming.api.windowing.time.time

// 定义温度事件
case class temperatureevent(deviceid: string, temperature: double, timestamp: long)

// watermark 策略：容忍 15 秒乱序
val watermarkstrategy = watermarkstrategy
  .forboundedoutoforderness[temperatureevent](duration.ofseconds(15))
  .withtimestampassigner((event, _) => event.timestamp)
  .withidleness(duration.ofminutes(2))

// 温度告警流
val alertstream = env
  .fromsource(mqttsource, watermarkstrategy, "mqtt sensor source")
  .keyby(_.deviceid)
  .window(tumblingeventtimewindows.of(time.seconds(10)))
  .aggregate(new temperaturealertaggregate())
  .filter(_.maxtemperature > 100.0)  // 阈值告警
```

### 6.2 设备会话分析

**场景**: 分析设备活跃会话，统计会话内事件数。

```scala
// 会话窗口：5 分钟无数据视为会话结束
val sessionstream = sensorevents
  .keyby(_.deviceid)
  .window(events timesessionwindows.withdynamicgap((event: sensorevent) => {
    // 根据设备类型动态调整会话超时
    if (event.devicetype == "mobile") time.minutes(5)
    else time.minutes(30)
  }))
  .allowedlateness(time.seconds(30))
  .process(new devicehandler())

// 处理函数
class devicehandler extends processwindowfunction[sensorevent, devicesession, string, sessionwindow] {
  override def process(
    deviceid: string,
    context: context,
    events: iterable[sensorevent],
    out: collector[devicesession]
  ): unit = {
    val eventlist = events.tolist.sortby(_.timestamp)
    val starttime = eventlist.head.timestamp
    val endtime = eventlist.last.timestamp
    val eventcount = eventlist.size

    out.collect(devicesession(
      deviceid = deviceid,
      sessionstart = starttime,
      sessionend = endtime,
      eventcount = eventcount,
      avgtemperature = eventlist.map(_.temperature).sum / eventcount
    ))
  }
}
```

### 6.3 乱序数据处理

**场景**: 边缘网关批量上报导致的乱序。

```scala
// 侧输出标签定义迟到数据
val latedatatag = outputtag[sensorevent]("late-data")

// 带侧输出的窗口聚合
val aggregated = sensorevents
  .assign timestampsandwatermarks(
    watermarkstrategy
      .forboundedoutoforderness[sensorevent](duration.ofseconds(30))
      .withtimestampassigner((event, _) => event.timestamp)
  )
  .keyby(_.deviceid)
  .window(tumblingeventtimewindows.of(time.minutes(1)))
  .allowedlateness(time.seconds(60))  // 允许 60 秒延迟
  .sideoutputlatedata(latedatatag)
  .aggregate(new sensormetrics())

// 处理迟到数据
val latedata: datastream[sensorevent] = aggregated.getsideoutput(latedatatag)
latedata.addsink(new latedataauditsink())
```

### 6.4 设备状态机管理

**场景**: 维护设备在线/离线状态。

```scala
class devicestatefunction extends keyedprocessfunction[string, sensorevent, devicestatus] {

  // 状态声明
  private var lastactivitystate: valuestate[long] = _
  private var onlinestate: valuestate[boolean] = _
  private var timerstate: valuestate[long] = _

  override def open(parameters: configuration): unit = {
    lastactivitystate = getruntimecontext.getstate(
      new valuestatedescriptor[long]("last-activity", classof[long])
    )
    onlinestate = getruntimecontext.getstate(
      new valuestatedescriptor[boolean]("online", classof[boolean])
    )
    timerstate = getruntimecontext.getstate(
      new valuestatedescriptor[long]("timer", classof[long])
    )
  }

  override def processelement(
    event: sensorevent,
    ctx: context,
    out: collector[devicestatus]
  ): unit = {
    val currenttime = ctx.timestamp()
    val wasonline = option(onlinestate.value()).getorelse(false)

    // 更新活动时间
    lastactivitystate.update(currenttime)

    // 如果之前离线，现在转为在线
    if (!wasonline) {
      onlinestate.update(true)
      out.collect(devicestatus(event.deviceid, "online", currenttime))
    }

    // 取消旧定时器，注册新定时器 (5 分钟后检查)
    option(timerstate.value()).foreach(ctx.timerservice().deleteeventtimetimer)
    val timeouttime = currenttime + time.minutes(5).tomilliseconds
    ctx.timerservice().registereventtimetimer(timeouttime)
    timerstate.update(timeouttime)
  }

  override def ontimer(
    timestamp: long,
    ctx: ontimercontext,
    out: collector[devicestatus]
  ): unit = {
    // 定时器触发，设备 5 分钟无活动，标记为离线
    onlinestate.update(false)
    out.collect(devicestatus(ctx.getcurrentkey, "offline", timestamp))
  }
}
```

---

## 7. 可视化 (visualizations)

### 7.1 iot 架构图

```mermaid
graph tb
    subgraph "设备层"
        d1[传感器/设备 a]
        d2[传感器/设备 b]
        d3[传感器/设备 c]
        dg[边缘网关<br/>批量聚合]
    end

    subgraph "接入层"
        mqtt[mqtt broker<br/>emqx]
        lb[负载均衡器]
    end

    subgraph "消息层"
        k1[kafka<br/>设备数据 topic]
        k2[kafka<br/>控制指令 topic]
    end

    subgraph "flink 处理层"
        src[source<br/>kafka consumer]
        wm[watermark<br/>容忍 15s 乱序]

        subgraph "核心处理"
            k1b[keyby deviceid]
            sw[session window<br/>5min gap]
            tw[tumbling window<br/>实时告警]
            state[keyed state<br/>设备状态]
        end

        ck[checkpoint<br/>30s 间隔]
    end

    subgraph "存储层"
        tsdb[(时序数据库<br/>influxdb/tdengine)]
        hbase[(设备画像<br/>hbase)]
        redis[(热状态<br/>redis)]
    end

    subgraph "应用层"
        alert[告警服务]
        dashboard[监控大屏]
        api[设备管理 api]
    end

    d1 --> dg
    d2 --> dg
    d3 --> dg
    dg --> mqtt
    mqtt --> lb --> k1
    k1 --> src --> wm --> k1b
    k1b --> sw --> tsdb
    k1b --> tw --> alert
    k1b --> state --> redis

    sw -.-> hbase
    state -.-> ck
```

### 7.2 数据流图

```mermaid
flowchart lr
    a[传感器采样] --> b[边缘缓存<br/>10s 批量]
    b --> c[mqtt qos 1]
    c --> d[kafka 分区<br/>deviceid 哈希]
    d --> e{乱序检测}
    e -->|在 watermark 内| f[窗口聚合]
    e -->|迟到数据| g[侧输出<br/>离线补录]
    f --> h[状态更新]
    h --> i[时序数据库]
    h --> j[告警触发]
```

### 7.3 设备状态机

```mermaid
statediagram-v2
    [*] --> 离线: 系统初始化

    离线 --> 在线: 收到设备心跳/数据

    在线 --> 活跃: 高频数据上报
    在线 --> 静默: 5 分钟无数据

    活跃 --> 在线: 数据频率降低
    活跃 --> 告警: 异常指标检测

    静默 --> 在线: 收到新数据
    静默 --> 离线: 超时 30 分钟

    告警 --> 活跃: 告警清除
    告警 --> 维护: 人工介入

    维护 --> 离线: 维护完成
    离线 --> [*]
```

---

## 8. 引用参考 (references)

[^1]: apache flink documentation, "event time and watermarks," 2025. <https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/>

[^2]: apache flink documentation, "state backends," 2025. <https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/state_backends/>

[^3]: apache flink documentation, "checkpointing," 2025. <https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/checkpointing/>





---

*文档版本: v1.0 | 更新日期: 2026-04-02 | 状态: 已完成*
