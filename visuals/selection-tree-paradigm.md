# 并发范式选型决策树

> **所属阶段**: Visuals | **前置依赖**: [../Knowledge/01-concept-atlas/concurrency-paradigms-matrix.md](../Knowledge/01-concept-atlas/concurrency-paradigms-matrix.md), [../Struct/01-foundation/](../Struct/01-foundation/) | **形式化等级**: L3-L6

---

## 1. 决策树概述

本文档提供交互式并发范式选型决策树，帮助架构师根据系统需求特征选择合适的并发计算范式。决策树基于五大关键维度：水平扩展需求、时间语义重要性、容错要求、状态复杂度和网络拓扑动态性。

### 1.1 判定性层级与范式映射

| 判定性层级 | 对应范式 | 形式化特征 |
|-----------|---------|-----------|
| L3 可判定 | CSP (有限状态) | PSPACE-完全，静态通道命名 |
| L4 半可判定 | Actor, Dataflow | 动态拓扑，移动性，消息可达性 |
| L6 图灵完备 | Shared Memory, STM | 不可判定，表达能力最强 |

---

## 2. 交互式决策树

```mermaid
flowchart TD
    %% 根节点
    START([开始选型<br/>START]) --> Q1{需要水平扩展?<br/>Horizontal Scaling}

    %% 第一层：水平扩展
    Q1 -->|是 Yes| Q2{时间语义重要?<br/>Time Semantics Critical}
    Q1 -->|否 No| Q3{单机性能关键?<br/>Single-Node Performance}

    %% 分支A：分布式路径
    Q2 -->|是 Yes| Q4{批流统一处理?<br/>Batch-Stream Unified}
    Q2 -->|否 No| Q5{容错要求高?<br/>Fault Tolerance Level}

    Q4 -->|是 Yes| DATAFLOW[Dataflow<br/>Apache Flink/Beam]
    Q4 -->|否 No| Q6{网络拓扑动态?<br/>Dynamic Topology}

    Q6 -->|是 Yes| ACTOR1[Actor Model<br/>Akka/Erlang]
    Q6 -->|否 No| CSP_DIST[CSP+<br/>Go+Service Discovery]

    Q5 -->|高 High| ACTOR2[Actor Model<br/>Erlang/OTP]
    Q5 -->|中/低 Medium/Low| Q7{同步/异步偏好?<br/>Sync/Async Preference}

    Q7 -->|同步 Sync| CSP_DIST2[CSP<br/>Go Channels]
    Q7 -->|异步 Async| ACTOR3[Actor Model<br/>Akka/Pekko]

    %% 分支B：单机路径
    Q3 -->|是 Yes| Q8{共享数据复杂度?<br/>Shared Data Complexity}
    Q3 -->|否 No| SEQ[顺序模型<br/>单线程/协程]

    Q8 -->|高 High| Q9{需要事务语义?<br/>Transactional Semantics}
    Q8 -->|低 Low| Q10{控制流复杂度?<br/>Control Flow Complexity}

    Q9 -->|是 Yes| STM[STM<br/>Haskell/Clojure]
    Q9 -->|否 No| Q11{死锁风险容忍度?<br/>Deadlock Risk Tolerance}

    Q11 -->|低 Low| ACTOR4[Actor Model<br/>Type-safe Actor]
    Q11 -->|高 High| CSP_LOCAL[CSP<br/>Go Channels]

    Q10 -->|高 High| CSP_LOCAL2[CSP<br/>Go Channels]
    Q10 -->|低 Low| SHARED[Shared Memory<br/>Locks/Mutex]

    %% 范式详情节点
    DATAFLOW --> DF_INFO["**Dataflow模型**<br/><br/>判定性: L4 半可判定<br/>适用场景:<br/>• 实时ETL/流分析<br/>• 事件驱动处理<br/>• 窗口聚合<br/>• CEP复杂事件处理<br/><br/>代表技术:<br/>• Apache Flink<br/>• Apache Beam<br/>• Kafka Streams<br/>• RisingWave"]

    ACTOR1 --> ACTOR_INFO["**Actor模型**<br/><br/>判定性: L4 半可判定<br/>适用场景:<br/>• 分布式微服务<br/>• 高容错消息系统<br/>• 游戏服务器<br/>• IoT设备管理<br/><br/>代表技术:<br/>• Erlang/OTP<br/>• Akka (Scala/Java)<br/>• Pekko<br/>• Orleans (.NET)"]

    ACTOR2 --> ACTOR_INFO2["**Actor模型(高容错)**<br/><br/>判定性: L4 半可判定<br/>容错等级: 原生支持<br/>适用场景:<br/>• 电信核心网<br/>• 金融核心系统<br/>• 高可用服务<br/>• 监督树架构<br/><br/>代表技术:<br/>• Erlang/OTP<br/>• Elixir/Phoenix<br/>• Akka Cluster"]

    CSP_LOCAL --> CSP_INFO["**CSP模型**<br/><br/>判定性: L3 可判定(PSPACE)<br/>适用场景:<br/>• 系统编程<br/>• 高并发网络服务<br/>• 容器编排<br/>• 中间件开发<br/><br/>代表技术:<br/>• Go Channels<br/>• Rust (crossbeam)<br/>• Occam<br/>• Clojure core.async"]

    CSP_DIST --> CSP_DIST_INFO["**CSP分布式扩展**<br/><br/>判定性: L3→L4<br/>适用场景:<br/>• 服务网格<br/>• API网关<br/>• 分布式协调<br/><br/>代表技术:<br/>• Go + etcd/consul<br/>• NATS<br/>• gRPC Stream"]

    STM --> STM_INFO["**STM事务内存**<br/><br/>判定性: L6 图灵完备<br/>适用场景:<br/>• 并发数据结构<br/>• 业务事务处理<br/>• 函数式编程<br/><br/>代表技术:<br/>• Haskell STM<br/>• Clojure refs<br/>• Scala STM<br/>• GCC libitm"]

    SHARED --> SHARED_INFO["**Shared Memory**<br/><br/>判定性: L6 图灵完备<br/>适用场景:<br/>• 数值计算<br/>• 图像/信号处理<br/>• 低延迟系统<br/>• 嵌入式实时<br/><br/>代表技术:<br/>• Pthreads<br/>• Java synchronized<br/>• C++ std::mutex<br/>• OpenMP"]

    SEQ --> SEQ_INFO["**顺序模型**<br/><br/>判定性: L1-L2 高效可判定<br/>适用场景:<br/>• 嵌入式控制<br/>• 确定性执行<br/>• 简单脚本任务<br/><br/>代表技术:<br/>• 单线程协程<br/>• Lua/Python generator<br/>• RTOS任务"]

    %% 样式定义
    style START fill:#e3f2fd,stroke:#1565c0,stroke-width:3px

    style Q1 fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style Q2 fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style Q3 fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style Q4 fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style Q5 fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style Q6 fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style Q7 fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style Q8 fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style Q9 fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style Q10 fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style Q11 fill:#fff3e0,stroke:#ef6c00,stroke-width:2px

    style DATAFLOW fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style ACTOR1 fill:#e1bee7,stroke:#6a1b9a,stroke-width:3px
    style ACTOR2 fill:#e1bee7,stroke:#6a1b9a,stroke-width:3px
    style ACTOR3 fill:#e1bee7,stroke:#6a1b9a,stroke-width:2px
    style ACTOR4 fill:#e1bee7,stroke:#6a1b9a,stroke-width:2px
    style CSP_LOCAL fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    style CSP_LOCAL2 fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style CSP_DIST fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style CSP_DIST2 fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style STM fill:#bbdefb,stroke:#1565c0,stroke-width:3px
    style SHARED fill:#ffcdd2,stroke:#c62828,stroke-width:3px
    style SEQ fill:#f5f5f5,stroke:#616161,stroke-width:2px

    style DF_INFO fill:#fffde7,stroke:#f9a825
    style ACTOR_INFO fill:#f3e5f5,stroke:#8e24aa
    style ACTOR_INFO2 fill:#f3e5f5,stroke:#8e24aa
    style CSP_INFO fill:#e8f5e9,stroke:#43a047
    style CSP_DIST_INFO fill:#e8f5e9,stroke:#43a047
    style STM_INFO fill:#e3f2fd,stroke:#1e88e5
    style SHARED_INFO fill:#ffebee,stroke:#e53935
    style SEQ_INFO fill:#fafafa,stroke:#757575
```

---

## 3. 决策维度详解

### 3.1 维度一：水平扩展需求

| 需求 | 描述 | 推荐范式 |
|------|------|---------|
| **需要水平扩展** | 数据量/负载需要跨多台机器分布 | Actor, Dataflow |
| **单机多核** | 任务可在单台高性能服务器完成 | CSP, Shared Memory, STM |

**判定性影响**：水平扩展引入网络分区，将问题从可判定域(L3)推向半可判定域(L4)或不可判定域(FLP不可能性)。

### 3.2 维度二：时间语义重要性

| 重要性 | 描述 | 推荐范式 |
|--------|------|---------|
| **时间语义关键** | 依赖事件时间顺序、窗口计算、乱序处理 | Dataflow |
| **时间语义次要** | 处理时间足够，或顺序无关 | Actor, CSP |

**判定性影响**：时间语义要求引入Watermark机制，将无限流的半可判定问题转化为有限窗口的准可判定问题。

### 3.3 维度三：容错要求

| 容错等级 | 描述 | 推荐范式 |
|---------|------|---------|
| **高** | 电信级(99.999%)、故障自动恢复 | Actor (监督树原生支持) |
| **中** | 商业级(99.9%)、Checkpoint恢复 | Dataflow, STM |
| **低** | 开发级、允许服务重启 | Shared Memory, CSP |

**判定性影响**：容错机制通过状态隔离（Actor）或快照（Checkpoint）在半可判定环境中构造确定性恢复点。

### 3.4 维度四：状态复杂度

| 复杂度 | 描述 | 推荐范式 |
|--------|------|---------|
| **简单** | 无状态或简单局部状态 | Shared Memory, CSP |
| **中等** | 需要键控分区状态 | Dataflow |
| **复杂** | 分布式事务、嵌套状态机 | Actor, STM |

### 3.5 维度五：网络拓扑动态性

| 动态性 | 描述 | 推荐范式 |
|--------|------|---------|
| **静态** | 拓扑预定义，运行时不变 | CSP (静态通道) |
| **动态** | 运行时创建/销毁连接 | Actor (动态地址传递) |

**判定性影响**：动态拓扑表达能力等价于π-演算，从L3可判定进入L4半可判定。

---

## 4. 范式详细对比

### 4.1 核心特征矩阵

| 特征 | Dataflow | Actor | CSP | Shared Memory | STM |
|------|----------|-------|-----|---------------|-----|
| **通信风格** | 数据驱动 | 异步消息 | 同步通道 | 直接内存访问 | 事务边界 |
| **状态隔离** | 按键分区 | 完全隔离 | 完全隔离 | 完全共享 | 事务边界共享 |
| **判定性层级** | L4 半可判定 | L4 半可判定 | L3 可判定 | L6 图灵完备 | L6 图灵完备 |
| **容错机制** | Checkpoint | 监督树 | 需应用层实现 | 需应用层实现 | 事务回滚 |
| **水平扩展** | 原生支持 | 原生支持 | 需框架扩展 | 需DSM系统 | 分布式STM不成熟 |
| **代表技术** | Flink, Beam | Erlang, Akka | Go Channels | Pthreads, Java锁 | Haskell STM |

### 4.2 适用场景矩阵

| 场景特征 | 首选范式 | 次选方案 | 避免使用 |
|---------|---------|---------|---------|
| 大规模流处理 | **Dataflow** | Actor | Shared Memory |
| 高容错分布式系统 | **Actor** | Dataflow | Shared Memory |
| 高性能网络服务 | **CSP** | Shared Memory | Actor |
| 并发数据结构 | **STM** | Shared Memory + Locks | Actor |
| 实时控制系统 | **CSP** | Shared Memory | Actor |
| 复杂事务处理 | **STM** | Actor + Saga | Shared Memory |
| 嵌入式实时系统 | **Shared Memory** | CSP | Actor |

---

## 5. 判定性谱系与选型

```mermaid
graph TB
    subgraph "判定性层级与范式映射"
        L3["L3: 可判定<br/>PSPACE-Complete"]
        L4["L4: 半可判定<br/>Turing-recognizable"]
        L6["L6: 图灵完备<br/>Undecidable"]

        L3 -->|表达能力编码| L4
        L4 -->|实现于| L6
    end

    CSP_MODEL["CSP<br/>静态通道命名"]
    ACTOR_MODEL["Actor<br/>动态地址传递"]
    DF_MODEL["Dataflow<br/>数据驱动"]
    SM_MODEL["Shared Memory<br/>显式锁"]
    STM_MODEL["STM<br/>乐观并发"]

    L3 -.->|映射| CSP_MODEL
    L4 -.->|映射| ACTOR_MODEL
    L4 -.->|映射| DF_MODEL
    L6 -.->|映射| SM_MODEL
    L6 -.->|映射| STM_MODEL

    style L3 fill:#c8e6c9,stroke:#2e7d32
    style L4 fill:#fff9c4,stroke:#f57f17
    style L6 fill:#ffcdd2,stroke:#c62828
    style CSP_MODEL fill:#c8e6c9,stroke:#2e7d32
    style ACTOR_MODEL fill:#e1bee7,stroke:#6a1b9a
    style DF_MODEL fill:#fff9c4,stroke:#f57f17
    style SM_MODEL fill:#ffcdd2,stroke:#c62828
    style STM_MODEL fill:#bbdefb,stroke:#1565c0
```

### 5.1 判定性与工程权衡

| 判定性层级 | 理论限制 | 工程策略 | 适用范式 |
|-----------|---------|---------|---------|
| **高效可判定(P)** | 表达能力受限 | 追求最优算法 | 顺序计算 |
| **可判定但难处理** | NP/PSPACE复杂度 | 近似算法、启发式 | CSP有限状态验证 |
| **半可判定** | 不可判定终止性 | 水印/窗口/超时 | Actor, Dataflow |
| **图灵完备** | 停机问题不可解 | 测试、监控、熔断 | Shared Memory, STM |

---

## 6. 使用说明

### 6.1 快速选型指南

**场景1：实时数据分析平台**

```
水平扩展: 是 → 时间语义: 是 → 批流统一: 是 → Dataflow (Flink)
```

**场景2：微服务订单系统**

```
水平扩展: 是 → 时间语义: 否 → 容错要求高: 是 → Actor (Akka/Erlang)
```

**场景3：API网关**

```
水平扩展: 是 → 时间语义: 否 → 容错要求中 → 同步偏好 → CSP (Go)
```

**场景4：金融风控核心**

```
水平扩展: 否 → 单机性能: 是 → 共享数据复杂: 高 → 事务语义: 是 → STM
```

**场景5：图像处理服务**

```
水平扩展: 否 → 单机性能: 是 → 共享数据复杂: 低 → 控制流简单 → Shared Memory
```

### 6.2 混合范式策略

现代复杂系统通常采用分层混合范式：

```mermaid
graph TB
    subgraph "混合范式架构示例"
        API[API Gateway<br/>CSP/Go]
        MS[Microservices<br/>Actor/Akka]
        STREAM[Stream Processing<br/>Dataflow/Flink]
        STORE[State Store<br/>STM/Clojure]

        CLIENT[客户端] -->|HTTP/gRPC| API
        API -->|异步事件| MS
        MS -->|数据流| STREAM
        MS -->|共享状态| STORE
        STREAM -->|分析结果| API
    end

    style API fill:#c8e6c9,stroke:#2e7d32
    style MS fill:#e1bee7,stroke:#6a1b9a
    style STREAM fill:#fff9c4,stroke:#f57f17
    style STORE fill:#bbdefb,stroke:#1565c0
```

### 6.3 选型检查清单

- [ ] **规模评估**：数据量是TB级(PB级)还是GB级?
- [ ] **延迟要求**：需要毫秒级还是秒级响应?
- [ ] **容错需求**：能否接受服务重启，还是需要热故障转移?
- [ ] **团队技能**：团队熟悉函数式编程还是命令式编程?
- [ ] **生态成熟度**：目标语言/平台的库支持是否完善?
- [ ] **部署环境**：云原生(K8s)还是嵌入式/边缘设备?

---

## 7. 反模式警示

### 7.1 常见选型错误

| 反模式 | 错误描述 | 后果 | 正确选择 |
|--------|---------|------|---------|
| **Actor误用于流处理** | 用Akka实现实时窗口聚合 | 缺乏时间语义、Watermark机制 | Dataflow (Flink) |
| **Shared Memory误用于分布式** | 用Java锁实现跨服务协调 | 死锁、性能瓶颈、无法水平扩展 | Actor (Akka) |
| **CSP误用于长事务** | 用Go Channel实现Saga | 缺乏故障恢复、状态管理复杂 | Actor + Saga 或 Temporal |
| **Dataflow误用于RPC** | 用Flink实现请求-响应 | 高延迟、资源浪费 | CSP (gRPC) 或 Actor |

---

## 8. 关联文档

### 8.1 上游依赖

- [../Knowledge/01-concept-atlas/concurrency-paradigms-matrix.md](../Knowledge/01-concept-atlas/concurrency-paradigms-matrix.md) — 并发范式完整对比矩阵
- [../Struct/01-foundation/01.01-unified-streaming-theory.md](../Struct/01-foundation/01.01-unified-streaming-theory.md) — 统一流计算理论与六层表达能力层次
- [../Struct/01-foundation/01.03-actor-model-formalization.md](../Struct/01-foundation/01.03-actor-model-formalization.md) — Actor模型严格形式化
- [../Struct/01-foundation/01.04-dataflow-model-formalization.md](../Struct/01-foundation/01.04-dataflow-model-formalization.md) — Dataflow模型严格形式化
- [../Struct/01-foundation/01.05-csp-formalization.md](../Struct/01-foundation/01.05-csp-formalization.md) — CSP严格形式化

### 8.2 下游应用

- [../Flink/](../Flink/) — Flink专项知识库
- [../Knowledge/](../Knowledge/) — 工程实践与设计模式

---

## 9. 引用参考


---

*文档版本: 2026.04 | 形式化等级: L3-L6 | 状态: 可视化文档*
*关联矩阵: 5个决策维度 | 判定性层级: 3层 | 推荐范式: 5种*
