# 一致性级别选择决策树

> 所属阶段: formal-methods/03-model-taxonomy/04-consistency/ | 前置依赖: [01-consistency-spectrum.md](01-consistency-spectrum.md), [02-cap-theorem.md](02-cap-theorem.md) | 形式化等级: L4

## 1. 概念定义 (Definitions)

### 1.1 一致性选择决策树

**定义 Def-M-04-CDT-01**: 一致性级别选择决策树是分布式存储系统一致性模型选择的层次化决策框架，基于 CAP 定理、PACELC 模型和延迟-可用性权衡，指导工程师从系统需求出发选择合适的一致性保证。

**形式化表示**:

$$\mathcal{T}_{cons} = (N, E, \mathcal{C}, n_0, \delta)$$

其中：

- $N$: 决策节点集合
- $E \subseteq N \times N$: 决策分支关系
- $\mathcal{C} = \{\text{强一致}, \text{最终一致}, \text{因果一致}, \text{会话一致}\}$: 一致性级别
- $n_0$: 根节点（一致性需求分析）
- $\delta: N \rightarrow \mathcal{P}(ConsistencyModel)$: 节点到一致性模型集合的映射

### 1.2 选择维度

**定义 Def-M-04-CDT-02**: 一致性选择的三大核心维度：

| 维度 | 决策问题 | 典型选项 |
|------|---------|---------|
| **CAP 权衡** | 分区容忍性下的选择 | CP vs AP |
| **延迟需求** | 可接受的读写延迟 | 强一致延迟 vs 最终一致延迟 |
| **可用性需求** | 可接受的不可用时间 | 100% 可用 vs 可容忍故障 |

### 1.3 一致性级别层次

**定义 Def-M-04-CDT-03**: 一致性强度层次（从强到弱）：

$$\text{线性一致} \succ \text{顺序一致} \succ \text{因果一致} \succ \text{PRAM} \succ \text{读己写} \succ \text{单调读} \succ \text{最终一致}$$

**形式化定义**: 基于 [01-consistency-spectrum.md](01-consistency-spectrum.md) 中的形式化语义。

## 2. 属性推导 (Properties)

### 2.1 一致性选择的完备性

**引理 Lemma-M-04-CDT-01** [选择维度完备性]:
CAP 权衡、延迟需求和可用性需求三个维度覆盖了分布式系统一致性选择的主要决策因素。

**证明概要**:
根据 Gilbert 和 Lynch 的 CAP 定理[^1]，分布式系统必须在一致性(C)、可用性(A)和分区容忍性(P)中选择。延迟和可用性是 CAP 的工程细化：

- 延迟需求：强一致性通常需要同步通信，增加延迟
- 可用性需求：强一致性在分区期间可能需要拒绝服务

因此三个维度构成完备的决策空间。∎

### 2.2 一致性级别特征

**引理 Lemma-M-04-CDT-02** [一致性级别延迟特征]:

| 一致性级别 | 读延迟 | 写延迟 | 分区行为 |
|-----------|-------|-------|---------|
| 线性一致 | 高 | 高 | 不可用 |
| 因果一致 | 中 | 中 | 降级可用 |
| 最终一致 | 低 | 低 | 完全可用 |

## 3. 关系建立 (Relations)

### 3.1 一致性级别到应用场景的映射

| 一致性级别 | 典型应用 | 代表系统 |
|-----------|---------|---------|
| 线性一致 | 金融交易、库存管理 | etcd, ZooKeeper, Spanner |
| 顺序一致 | 分布式锁、配置管理 | ZooKeeper, etcd |
| 因果一致 | 社交网络、协作编辑 | COPS, AntidoteDB |
| 读己写 | 用户会话、购物车 | Dynamo, Cassandra |
| 最终一致 | 日志、监控、推荐 | Cassandra, DynamoDB |

### 3.2 PACELC 扩展关系

PACELC 模型[^2]扩展了 CAP，引入延迟与一致性的权衡：

- **PA**: 分区时选择可用性（AP 系统）
- **PC**: 分区时选择一致性（CP 系统）
- **EL**: 正常时选择低延迟
- **EC**: 正常时选择一致性

决策树整合了 PACELC 的四种组合：

- **PA/EL**: Dynamo, Cassandra（最终一致，低延迟）
- **PA/EC**: PNUTS（因果一致，中等延迟）
- **PC/EL**: MongoDB（可调一致性）
- **PC/EC**: Spanner, etcd（强一致，高延迟）

## 4. 论证过程 (Argumentation)

### 4.1 决策路径设计原则

**原则 1: 从业务需求出发**

- 首先确定是否需要强一致性（如金融交易）
- 其次确定延迟容忍度（如实时性要求）
- 最后确定可用性要求（如 SLA 承诺）

**原则 2: 渐进降级**
推荐路径：强一致 → 因果一致 → 最终一致
只在必要时降级，避免过早优化。

**原则 3: 混合策略**
对于复杂系统，不同数据子集可采用不同一致性级别：

- 关键数据：线性一致
- 用户数据：因果一致
- 日志数据：最终一致

### 4.2 反例分析

**反例 1**: 电商库存系统

- 直觉选择: 线性一致（避免超卖）
- 问题: 高峰期延迟过高，用户体验差
- 实际方案:
  - 下单时：预留库存（线性一致）
  - 查询时：缓存库存（最终一致）
  - 支付时：确认库存（线性一致）
- 教训: 不同操作采用不同一致性级别

**反例 2**: 全球分布式数据库

- 场景: 跨大洲数据复制
- 问题: 强一致性导致写入延迟 > 200ms
- 解决方案: 采用因果一致 + 向量时钟
- 验证: 业务逻辑无因果关系依赖，因果一致足够

## 5. 形式证明 / 工程论证 (Proof / Engineering Argument)

### 5.1 CAP 决策定理

**定理 Thm-M-04-CDT-01** [CAP 不可兼得]:
在异步网络模型中，不存在同时满足以下三个性质的分布式数据存储：

1. **一致性 (C)**: 所有节点看到相同的数据视图
2. **可用性 (A)**: 每个请求都收到非错误响应
3. **分区容忍性 (P)**: 系统在任意网络分区下继续运行

**证明概要**:
假设存在满足 CAP 的系统。考虑两节点网络分区场景：

- 节点1接收写请求
- 节点2接收读请求
- 网络分区使两节点无法通信

为保持一致性，节点2必须等待节点1的写操作（或拒绝服务）。

- 如果等待 → 违反可用性
- 如果拒绝 → 违反可用性
- 如果返回旧值 → 违反一致性

矛盾。∎

### 5.2 一致性级别蕴含关系

**定理 Thm-M-04-CDT-02** [一致性层级蕴含]:
一致性级别满足以下蕴含关系：

$$\text{Linearizable} \Rightarrow \text{Sequential} \Rightarrow \text{Causal} \Rightarrow \text{PRAM} \Rightarrow \text{Read-Your-Writes}$$

**工程论证**: 更强的保证蕴含更弱的保证，但代价是更高的延迟和更低的可用性。决策树通过引导用户在需求-代价权衡中找到最优平衡点。

### 5.3 延迟下界定理

**定理 Thm-M-04-CDT-03** [一致性延迟下界]:
在网络延迟为 $d$ 的分布式系统中，实现线性一致的读写操作至少需要 $2d$ 的延迟。

**证明概要**:
读操作必须确认没有并发的写操作，需要与多数副本通信。写操作必须确认持久化到多数副本。最少需要两次网络往返。∎

## 6. 实例验证 (Examples)

### 6.1 金融交易系统选型

**需求分析**:

- 数据类型: 账户余额、交易记录
- 一致性要求: 绝对精确，不允许不一致
- 延迟要求: < 1s（可接受）
- 可用性要求: 99.99%（可容忍短暂不可用）

**决策路径**:

```
分区容忍性: 必须（分布式系统）
└── CAP选择: 一致性优先（CP）
    └── 延迟可接受 → 线性一致
        └── 系统选择: Spanner / CockroachDB
```

**验证**: 使用 Jepsen 测试验证线性一致性[^3]。

### 6.2 社交网络动态流选型

**需求分析**:

- 数据类型: 用户动态、点赞、评论
- 一致性要求: 用户看到自己的操作即可
- 延迟要求: < 100ms（严格）
- 可用性要求: 100%（不接受不可用）

**决策路径**:

```
分区容忍性: 必须
└── CAP选择: 可用性优先（AP）
    └── 低延迟要求 → 最终一致
        └── 增强: 会话一致（Read-Your-Writes）
            └── 系统选择: Cassandra / DynamoDB
```

**验证**: 使用向量时钟验证因果一致性。

### 6.3 协作编辑器选型

**需求分析**:

- 数据类型: 文档操作（CRDT）
- 一致性要求: 操作因果关系保持
- 延迟要求: < 50ms（实时协作）
- 可用性要求: 离线可用

**决策路径**:

```
分区容忍性: 必须（支持离线）
└── CAP选择: 可用性优先（AP）
    └── 因果要求 → 因果一致
        └── 实现: CRDT + 向量时钟
            └── 系统选择: Yjs / Automerge
```

## 7. 可视化 (Visualizations)

### 7.1 一致性选择决策树（主决策树）

```mermaid
flowchart TD
    Root["分布式系统一致性选择"]

    Root --> Q1{网络分区容忍?}
    Q1 -->|否| SingleNode["单机系统<br/>无需CAP权衡"]
    Q1 -->|是| CAPChoice["CAP定理适用"]

    CAPChoice --> Q2{分区时选择?}
    Q2 -->|一致性| CPSystem["CP系统"]
    Q2 -->|可用性| APSystem["AP系统"]

    CPSystem --> Q3{延迟需求?}
    Q3 -->|可接受高延迟| CPLatencyHigh["高延迟CP"]
    CPLatencyHigh --> CP1["线性一致<br/>Linearizable"]
    CP1 --> Sys1[Spanner<br/>CockroachDB<br/>etcd]

    Q3 -->|需要低延迟| CPLatencyLow["低延迟CP"]
    CPLatencyLow --> CP2["顺序一致<br/>Sequential"]
    CP2 --> Sys2["ZooKeeper<br/>etcd - 读优化"]

    APSystem --> Q4{一致性需求?}
    Q4 -->|强因果| APCausal["因果一致"]
    APCausal --> AP1[Causal Consistency]
    AP1 --> Sys3[COPS<br/>AntidoteDB<br/>Riak]

    Q4 -->|会话保证| APSession["会话一致"]
    APSession --> AP2[Read-Your-Writes<br/>Monotonic Reads]
    AP2 --> Sys4[Cassandra<br/>DynamoDB<br/>Voldemort]

    Q4 -->|最终即可| APEventual["最终一致"]
    APEventual --> AP3[Eventual Consistency]
    AP3 --> Sys5[Cassandra<br/>Dynamo<br/>Couchbase]

    SingleNode --> SingleRec["强一致默认<br/>无需分布式协议"]

    style Root fill:#e3f2fd
    style CPSystem fill:#f8d7da
    style APSystem fill:#d4edda
    style CP1 fill:#fff3cd
    style AP1 fill:#fff3cd
    style AP2 fill:#fff3cd
    style AP3 fill:#fff3cd
```

### 7.2 PACELC 扩展决策树

```mermaid
flowchart TD
    Start["PACELC一致性选择"]

    Start --> Q1{正常情况?}
    Q1 -->|是| NormalCase["正常情况决策"]
    Q1 -->|否| PartitionCase["分区情况决策"]

    NormalCase --> Q2{延迟 vs 一致性?}
    Q2 -->|低延迟优先| EL["EL - 延迟优先"]
    Q2 -->|一致性优先| EC["EC - 一致优先"]

    EL --> EL1["正常: 异步复制<br/>低延迟"]
    EC --> EC1["正常: 同步复制<br/>强一致"]

    PartitionCase --> Q3{可用性 vs 一致性?}
    Q3 -->|可用性优先| PA["PA - 可用优先"]
    Q3 -->|一致性优先| PC["PC - 一致优先"]

    PA --> PA1["分区: 继续服务<br/>可能不一致"]
    PC --> PC1["分区: 拒绝服务<br/>保持一致"]

    %% 组合结果
    EL --> Combo1{分区时?}
    Combo1 -->|PA| PA_EL["PA/EL<br/>Dynamo模式"]
    PA_EL --> Sys1["Dynamo<br/>Cassandra<br/>最终一致"]

    Combo1 -->|PC| PC_EL["PC/EL<br/>可调一致"]
    PC_EL --> Sys2["MongoDB<br/>可调一致性"]

    EC --> Combo2{分区时?}
    Combo2 -->|PA| PA_EC["PA/EC<br/>因果一致"]
    PA_EC --> Sys3["PNUTS<br/>Causal一致"]

    Combo2 -->|PC| PC_EC["PC/EC<br/>强一致"]
    PC_EC --> Sys4["Spanner<br/>etcd<br/>线性一致"]

    style Start fill:#e3f2fd
    style PA_EL fill:#d4edda
    style PC_EC fill:#f8d7da
```

### 7.3 应用场景快速决策图

```mermaid
flowchart TD
    Root["应用场景一致性选择"]

    Root --> App1["金融/交易"]
    Root --> App2["社交网络"]
    Root --> App3["电商/库存"]
    Root --> App4["日志/监控"]
    Root --> App5["协作编辑"]
    Root --> App6["配置管理"]

    App1 --> App1_1["需求: 绝对一致<br/>可接受延迟"]
    App1_1 --> App1_Rec["线性一致<br/>Spanner/Paxos"]

    App2 --> App2_1["需求: 低延迟<br/>高可用"]
    App2_1 --> App2_Rec["最终一致+会话<br/>Cassandra"]

    App3 --> App3_1["需求: 混合<br/>不同操作不同要求"]
    App3_1 --> App3_Rec["下单: 线性一致<br/>查询: 最终一致"]

    App4 --> App4_1["需求: 高吞吐<br/>顺序不重要"]
    App4_1 --> App4_Rec["最终一致<br/>Kafka/Cassandra"]

    App5 --> App5_1["需求: 因果关系<br/>离线可用"]
    App5_1 --> App5_Rec["因果一致<br/>CRDT/Yjs"]

    App6 --> App6_1["需求: 强一致<br/>低并发"]
    App6_1 --> App6_Rec["顺序一致<br/>ZooKeeper/etcd"]

    style Root fill:#e3f2fd
    style App1_Rec fill:#f8d7da
    style App2_Rec fill:#d4edda
    style App3_Rec fill:#fff3cd
```

### 7.4 一致性级别能力矩阵

```mermaid
graph TB
    subgraph "一致性级别"
    C1["线性一致<br/>Linearizable"]
    C2["顺序一致<br/>Sequential"]
    C3["因果一致<br/>Causal"]
    C4["会话一致<br/>Session"]
    C5["最终一致<br/>Eventual"]
    end

    subgraph "能力特征"
    F1["实时读最新"]
    F2["全局顺序"]
    F3["因果保持"]
    F4["读己写"]
    F5["高可用"]
    F6["低延迟"]
    end

    C1 -.->|✓| F1
    C1 -.->|✓| F2
    C1 -.->|✓| F3

    C2 -.->|✗| F1
    C2 -.->|✓| F2
    C2 -.->|✓| F3

    C3 -.->|✗| F1
    C3 -.->|✗| F2
    C3 -.->|✓| F3

    C4 -.->|✗| F1
    C4 -.->|✗| F2
    C4 -.->|△| F3
    C4 -.->|✓| F4

    C5 -.->|✗| F1
    C5 -.->|✗| F2
    C5 -.->|✗| F3
    C5 -.->|✓| F5
    C5 -.->|✓| F6

    C1 -.->|✗| F5
    C1 -.->|✗| F6
```

### 7.5 延迟-一致性权衡图

```mermaid
graph LR
    subgraph "延迟 vs 一致性"
    direction TB

    LowCons["最终一致<br/>延迟: <1ms"]
    MedCons["因果一致<br/>延迟: 10-50ms"]
    HighCons["线性一致<br/>延迟: 100-500ms"]

    LowCons --> MedCons --> HighCons
    end

    subgraph "应用场景"
    AppLow["日志/监控<br/>推荐系统"]
    AppMed["社交网络<br/>购物车"]
    AppHigh["金融交易<br/>库存管理"]
    end

    LowCons -.-> AppLow
    MedCons -.-> AppMed
    HighCons -.-> AppHigh
```

### 7.6 一致性选择检查清单

```mermaid
flowchart TD
    Start["一致性选择检查清单"]

    Start --> Check1{是否需要实时看到最新写入?}
    Check1 -->|是| C1_NeedLatest
    Check1 -->|否| C1_EventualOK

    C1_NeedLatest --> Check2{是否需要全局顺序?}
    Check2 -->|是| C2_NeedOrder
    Check2 -->|否| C2_CausalOK

    C2_NeedOrder --> Check3{是否可以接受分区时不可用?}
    Check3 -->|是| C3_CPSystem
    Check3 -->|否| C3_AdjustDesign

    C3_CPSystem --> Rec1["推荐: 线性一致<br/>Spanner/CockroachDB"]

    C2_CausalOK --> Rec2["推荐: 因果一致<br/>COPS/AntidoteDB"]
    C1_EventualOK --> Rec3["推荐: 最终一致<br/>Cassandra/Dynamo"]
    C3_AdjustDesign --> Rec4["建议: 重新设计<br/>或接受数据不一致"]

    Start --> Check4{延迟要求?}
    Check4 -->|<10ms| LatLow["需要本地处理"]
    Check4 -->|<100ms| LatMed["可用因果一致"]
    Check4 -->|>100ms| LatHigh["可用强一致"]

    LatLow --> LatRec["考虑: 边缘缓存<br/>本地优先"]

    Start --> Check5{可用性要求?}
    Check5 -->|100% SLA| AvHigh["必须AP系统"]
    Check5 -->|99.9% SLA| AvMed["可调一致性"]
    Check5 -->|<99% SLA| AvLow["可CP系统"]

    AvHigh --> AvRec["AP + 最终一致"]

    style Start fill:#e3f2fd
    style Rec1 fill:#f8d7da
    style Rec2 fill:#fff3cd
    style Rec3 fill:#d4edda
```

## 8. 引用参考 (References)

[^1]: S. Gilbert and N. Lynch, "Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services", ACM SIGACT News, 2002.
[^2]: D. J. Abadi, "Consistency Tradeoffs in Modern Distributed Database System Design", IEEE Computer, 2012.
[^3]: K. Kingsbury, "Jepsen: Distributed Systems Safety Analysis", <https://jepsen.io>, 2013-2025.
