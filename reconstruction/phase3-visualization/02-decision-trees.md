# 核心决策树可视化

> 所属阶段: Knowledge | 前置依赖: [流处理基础概念](../struct/01-stream-processing-basics.md) | 形式化等级: L3

## 1. 概念定义 (Definitions)

**Def-K-VIZ-02-01: 决策树 (Decision Tree)**
决策树是一种分层决策支持工具，通过一系列是非判断或特征选择，将复杂决策过程分解为可执行的推理路径。在流处理系统选型中，决策树将技术需求映射为具体的组件配置。

**Def-K-VIZ-02-02: 引擎选型维度 (Engine Selection Dimension)**
引擎选型的核心维度包括：延迟敏感度（Latency Sensitivity）、一致性保证级别（Consistency Level）、状态规模（State Scale）、吞吐量要求（Throughput Requirement）、以及生态兼容性（Ecosystem Compatibility）。

**Def-K-VIZ-02-03: 部署模式谱系 (Deployment Mode Spectrum)**
部署模式按照基础设施抽象层级分为：Standalone（进程级）、YARN（资源管理器级）、Kubernetes（容器编排级）、Serverless（函数级），各模式在运维复杂度与弹性能力之间存在权衡。

---

## 2. 属性推导 (Properties)

**Lemma-K-VIZ-02-01: 决策树完备性**
对于任意流处理需求，若其在五个维度（延迟、一致性、状态、窗口、部署）上的取值都在预定义范围内，则至少存在一条决策路径通向明确的技术选型推荐。

**Lemma-K-VIZ-02-02: 一致性级别蕴含关系**
Exactly-Once 语义在工程实现上蕴含 At-Least-Once 能力，但反之不成立。形式化表述为：

```
∀s ∈ StreamProcessor: ExactlyOnce(s) → AtLeastOnce(s)
∃s ∈ StreamProcessor: AtLeastOnce(s) ∧ ¬ExactlyOnce(s)
```

**Lemma-K-VIZ-02-03: 状态后端选择边界**
状态后端的选择遵循内存-性能权衡定律：HashMap 提供最优访问延迟但受限于堆内存；RocksDB/ForSt 支持TB级状态但引入序列化开销和磁盘I/O延迟。

---

## 3. 关系建立 (Relations)

### 3.1 决策维度与引擎能力映射

| 决策维度 | Flink | RisingWave | Kafka Streams |
|---------|-------|------------|---------------|
| 延迟要求(<100ms) | 支持 | 支持 | 支持 |
| 延迟要求(<10ms) | 有限支持 | 支持 | 有限支持 |
| Exactly-Once | 原生支持 | 原生支持 | 需外部协调 |
| TB级状态 | RocksDB/ForSt | 内置存储 | 需外部存储 |
| SQL支持 | Table API/SQL | 原生SQL | KSQL |

### 3.2 部署模式与弹性能力关系

```
Standalone → 手动扩缩容 → 低运维复杂度，低弹性
YARN       → 资源级弹性 → 中等运维，中等弹性
Kubernetes → 容器级弹性 → 较高运维，高弹性
Serverless → 函数级弹性 → 低运维，自动弹性
```

---

## 4. 论证过程 (Argumentation)

### 4.1 引擎选型决策的边界条件

**反例分析**: 当需求同时要求亚毫秒级延迟（<1ms）和TB级状态时，当前主流流处理引擎均无法单一满足。此类场景需采用分层架构：

- 热路径：专用低延迟引擎（如 Aeron, Disruptor）
- 冷路径：标准流处理引擎处理状态管理

### 4.2 窗口策略与时间语义耦合

窗口策略的选择与时间语义（Processing Time vs Event Time）存在强耦合：

- **Processing Time**: 适合 Tumbling/Sliding 窗口，简单但无法处理乱序
- **Event Time**: 必须配合 Watermark 机制，Session 窗口在此模式下才有意义

---

## 5. 形式证明 / 工程论证 (Proof / Engineering Argument)

### 5.1 状态后端选择的工程论证

**场景假设**: 状态规模 S，访问频率 F，可用内存 M

**决策规则**:

1. 若 S ≤ 0.3M 且 F > 10⁴ ops/s → 选择 HashMapStateBackend
2. 若 S > M 或需增量 Checkpoint → 选择 RocksDBStateBackend/ForStStateBackend
3. 若 S > 10TB 或需远程恢复 → 选择 ForStStateBackend（云原生优化）

**论证**: HashMap 提供 O(1) 访问复杂度，但受限于 JVM 堆内存和 GC 压力。RocksDB 通过 LSM-Tree 结构实现写优化，牺牲部分读性能换取水平扩展能力。ForSt 针对云存储（S3/OSS）优化，通过分层存储实现成本-性能平衡。

---

## 6. 实例验证 (Examples)

### 6.1 实时风控系统选型案例

**需求特征**:

- 延迟要求: <500ms
- 一致性: Exactly-Once（资金相关）
- 状态规模: 用户行为画像，约 100GB
- 窗口: 5分钟滑动窗口检测异常模式

**决策路径**:

1. 延迟 < 1s → 进入流处理引擎对比
2. Exactly-Once → Flink/RisingWave
3. 状态 100GB → RocksDB 后端
4. 滑动窗口 + 模式触发 → Flink CEP

**结论**: Apache Flink + RocksDB State Backend

### 6.2 日志聚合分析选型案例

**需求特征**:

- 延迟要求: <30s 可接受
- 一致性: At-Least-Once（允许少量重复）
- 状态规模: 无状态聚合
- 部署: 已有 K8s 集群

**决策路径**:

1. 延迟 > 1s → 批处理或轻量流处理均可
2. At-Least-Once → Kafka Streams 可选
3. K8s 部署 → Flink on K8s 或 Kafka Streams

**结论**: Kafka Streams（简化运维）或 Flink（未来扩展性）

---

## 7. 可视化 (Visualizations)

### 7.1 流处理引擎选型决策树

流处理引擎选型需要综合评估延迟、一致性、状态规模和SQL需求四个核心维度。

```mermaid
flowchart TD
    Start([开始选型]) --> Latency{延迟要求}

    Latency -->|亚毫秒级<br/><1ms| Specialized[专用低延迟引擎<br/>Aeron/Disruptor]
    Latency -->|毫秒级<br/>1-100ms| Consistency{一致性要求}
    Latency -->|秒级<br/>>1s| Throughput{吞吐量优先?}

    Consistency -->|Exactly-Once| StateSize{状态规模}
    Consistency -->|At-Least-Once| KStreams[Kafka Streams<br/>轻量级嵌入]

    StateSize -->|小状态<br/><10GB| FlinkLight[Flink<br/>HashMap后端]
    StateSize -->|中等状态<br/>10GB-1TB| FlinkRocks[Flink<br/>RocksDB后端]
    StateSize -->|大状态<br/>>1TB或SQL优先| RisingWave[RisingWave<br/>物化视图优先]

    Throughput -->|是| FlinkScale[Flink<br/>高吞吐集群]
    Throughput -->|否| Simple[Kafka Streams<br/>或Flink轻量模式]

    Specialized --> End1([选择专用引擎])
    KStreams --> End2([Kafka Streams])
    FlinkLight --> End3([Flink + HashMap])
    FlinkRocks --> End4([Flink + RocksDB])
    RisingWave --> End5([RisingWave])
    FlinkScale --> End6([Flink集群部署])
    Simple --> End7([轻量级方案])

    style Start fill:#e1f5fe
    style End1 fill:#c8e6c9
    style End2 fill:#c8e6c9
    style End3 fill:#c8e6c9
    style End4 fill:#c8e6c9
    style End5 fill:#c8e6c9
    style End6 fill:#c8e6c9
    style End7 fill:#c8e6c9
    style RisingWave fill:#fff3e0
```

---

### 7.2 一致性模型选型决策树

一致性模型的选择取决于业务对重复处理和数据丢失的容忍度。

```mermaid
flowchart TD
    Start([选择一致性模型]) --> TolerateDup{允许重复处理?}

    TolerateDup -->|否| TolerateLoss{允许数据丢失?}
    TolerateDup -->|是| AtLeastOnce[At-Least-Once
    至少一次语义
    保证不丢但可能重]

    TolerateLoss -->|否| ExactlyOnce[Exactly-Once
    精确一次语义
    通过幂等/事务实现]
    TolerateLoss -->|是| AtMostOnce[At-Most-Once
    至多一次语义
    可能丢失但不重]

    ExactlyOnce --> ImplMethod{实现方式}
    AtLeastOnce --> AckStrategy{确认策略}
    AtMostOnce --> FireForget[发送即忘
    无确认机制]

    ImplMethod -->|两阶段提交| TwoPhase[2PC事务
    外部系统支持]
    ImplMethod -->|幂等写入| Idempotent[幂等Producer
    基于ID去重]

    AckStrategy -->|批量确认| BatchAck[批量ACK
    吞吐优先]
    AckStrategy -->|单条确认| SingleAck[单条ACK
    延迟敏感]

    TwoPhase --> End1([Exactly-Once + 2PC])
    Idempotent --> End2([Exactly-Once + 幂等])
    BatchAck --> End3([At-Least-Once 批量])
    SingleAck --> End4([At-Least-Once 单条])
    FireForget --> End5([At-Most-Once])

    style Start fill:#e1f5fe
    style ExactlyOnce fill:#ffebee
    style AtLeastOnce fill:#fff3e0
    style AtMostOnce fill:#e8f5e9
    style End1 fill:#c8e6c9
    style End2 fill:#c8e6c9
    style End3 fill:#c8e6c9
    style End4 fill:#c8e6c9
    style End5 fill:#c8e6c9
```

---

### 7.3 窗口策略选型决策树

窗口策略的选择取决于时间特征、触发模式和业务语义需求。

```mermaid
flowchart TD
    Start([选择窗口策略]) --> TimeChar{时间特征}

    TimeChar -->|固定时间段| Fixed{时间重叠?}
    TimeChar -->|活动会话| SessionWindow[Session窗口
    动态边界
    超时触发]
    TimeChar -->|全局视图| GlobalWindow[全局窗口
    单窗口
    自定义触发]

    Fixed -->|无重叠| Tumbling[Tumbling窗口
    翻滚窗口
    固定大小不重叠]
    Fixed -->|有重叠| Sliding[Sliding窗口
    滑动窗口
    滑动步长<窗口大小]

    Tumbling --> Trigger1{触发模式}
    Sliding --> Trigger2{触发模式}
    SessionWindow --> Trigger3{触发模式}

    Trigger1 -->|时间触发| TimeTrigger1[时间触发
    窗口结束触发]
    Trigger1 -->|计数触发| CountTrigger1[计数触发
    达到N条触发]

    Trigger2 -->|时间触发| TimeTrigger2[时间触发
    增量计算]
    Trigger2 -->|计数触发| CountTrigger2[计数触发
    滑动内累计]

    Trigger3 -->|超时触发| TimeoutTrigger[超时触发
    无新数据触发]
    Trigger3 -->|间隙触发| GapTrigger[间隙触发
    活动间隙超时]

    TimeTrigger1 --> End1([Tumbling + Time])
    CountTrigger1 --> End2([Tumbling + Count])
    TimeTrigger2 --> End3([Sliding + Time])
    CountTrigger2 --> End4([Sliding + Count])
    TimeoutTrigger --> End5([Session + Timeout])
    GapTrigger --> End6([Session + Gap])
    GlobalWindow --> End7([Global + Custom])

    style Start fill:#e1f5fe
    style Tumbling fill:#e3f2fd
    style Sliding fill:#e8f5e9
    style SessionWindow fill:#fff3e0
    style GlobalWindow fill:#f3e5f5
    style End1 fill:#c8e6c9
    style End2 fill:#c8e6c9
    style End3 fill:#c8e6c9
    style End4 fill:#c8e6c9
    style End5 fill:#c8e6c9
    style End6 fill:#c8e6c9
    style End7 fill:#c8e6c9
```

---

### 7.4 状态后端选型决策树

状态后端的选择取决于状态规模、访问模式和恢复速度要求。

```mermaid
flowchart TD
    Start([选择状态后端]) --> StateSize{状态规模}

    StateSize -->|小状态<br/><100MB| HashMap[HashMapStateBackend
    内存存储
    JNI Off-Heap可选]
    StateSize -->|中等状态<br/>100MB-100GB| RocksDB[RocksDBStateBackend
    本地磁盘存储
    LSM-Tree结构]
    StateSize -->|大状态<br/>>100GB或云原生| ForSt[ForStStateBackend
    云原生优化
    分层存储]

    StateSize -->|超大规模<br/>TB级+远程| Remote[RemoteStateBackend
    外部存储
    Redis/RocksDB-Cloud]

    HashMap --> RecoverySpeed1{恢复速度要求}
    RocksDB --> RecoverySpeed2{恢复速度要求}
    ForSt --> RecoverySpeed3{恢复速度要求}

    RecoverySpeed1 -->|快速恢复| HashMapSync[同步Checkpoint
    全量快照]
    RecoverySpeed1 -->|标准恢复| HashMapAsync[异步Checkpoint
    后台持久化]

    RecoverySpeed2 -->|快速恢复| RocksDBInc[增量Checkpoint
    SST文件差异]
    RecoverySpeed2 -->|标准恢复| RocksDBFull[全量Checkpoint
    完整状态快照]

    RecoverySpeed3 -->|快速恢复| ForStTier[分层Checkpoint
    本地+远程混合]
    RecoverySpeed3 -->|成本优先| ForStRemote[远程优先
    S3/OSS存储]

    HashMapSync --> End1([HashMap + 同步])
    HashMapAsync --> End2([HashMap + 异步])
    RocksDBInc --> End3([RocksDB + 增量])
    RocksDBFull --> End4([RocksDB + 全量])
    ForStTier --> End5([ForSt + 分层])
    ForStRemote --> End6([ForSt + 远程])
    Remote --> End7([Remote Backend])

    style Start fill:#e1f5fe
    style HashMap fill:#e8f5e9
    style RocksDB fill:#fff3e0
    style ForSt fill:#ffebee
    style Remote fill:#f3e5f5
    style End1 fill:#c8e6c9
    style End2 fill:#c8e6c9
    style End3 fill:#c8e6c9
    style End4 fill:#c8e6c9
    style End5 fill:#c8e6c9
    style End6 fill:#c8e6c9
    style End7 fill:#c8e6c9
```

---

### 7.5 部署模式选型决策树

部署模式的选择取决于基础设施现状、弹性需求和运维能力。

```mermaid
flowchart TD
    Start([选择部署模式]) --> Infra{基础设施现状}

    Infra -->|已有K8s集群| K8s{弹性需求}
    Infra -->|已有Hadoop生态| YARN{资源需求}
    Infra -->|裸机/VM| Standalone{规模}
    Infra -->|无基础设施| Cloud{云厂商}

    K8s -->|自动弹性| K8sNative[Flink Native on K8s
    Operator管理
    自动扩缩容]
    K8s -->|静态资源| K8sSession[K8s Session模式
    多Job共享
    资源隔离]

    YARN -->|大规模集群| YARNProd[YARN生产模式
    高可用配置
    资源队列]
    YARN -->|开发测试| YARNPerJob[YARN Per-Job
    单Job独立
    快速迭代]

    Standalone -->|单机/小集群| StandaloneLocal[Standalone Local
    单节点部署
    开发调试]
    Standalone -->|多机集群| StandaloneCluster[Standalone Cluster
    手动配置HA
    固定资源]

    Cloud -->|AWS| AWSServerless[EMR Serverless
    或Kinesis]
    Cloud -->|阿里云| AliServerless[Serverless Flink
    全托管服务]
    Cloud -->|GCP| GCPDataflow[Dataflow
    或GKE托管]
    Cloud -->|Azure| AzureStream[Azure Stream Analytics
    或AKS托管]

    K8sNative --> HA1{高可用?}
    K8sSession --> HA2{高可用?}

    HA1 -->|是| K8sHA[K8s HA模式
    多JM副本
    K8s原生HA]
    HA1 -->|否| K8sSingle[K8s单点
    快速启动]

    HA2 -->|是| SessionHA[Session HA
    ZooKeeper/K8s HA]
    HA2 -->|否| SessionSingle[单Session
    简单部署]

    K8sHA --> End1([K8s Native HA])
    K8sSingle --> End2([K8s Native 单点])
    SessionHA --> End3([K8s Session HA])
    SessionSingle --> End4([K8s Session 单点])
    YARNProd --> End5([YARN 生产模式])
    YARNPerJob --> End6([YARN Per-Job])
    StandaloneLocal --> End7([Standalone Local])
    StandaloneCluster --> End8([Standalone Cluster])
    AWSServerless --> End9([AWS Serverless])
    AliServerless --> End10([阿里云 Serverless])
    GCPDataflow --> End11([GCP Dataflow])
    AzureStream --> End12([Azure Stream Analytics])

    style Start fill:#e1f5fe
    style K8sNative fill:#e3f2fd
    style YARNProd fill:#fff3e0
    style StandaloneCluster fill:#e8f5e9
    style AliServerless fill:#ffebee
    style End1 fill:#c8e6c9
    style End2 fill:#c8e6c9
    style End3 fill:#c8e6c9
    style End4 fill:#c8e6c9
    style End5 fill:#c8e6c9
    style End6 fill:#c8e6c9
    style End7 fill:#c8e6c9
    style End8 fill:#c8e6c9
    style End9 fill:#c8e6c9
    style End10 fill:#c8e6c9
    style End11 fill:#c8e6c9
    style End12 fill:#c8e6c9
```

---

## 8. 引用参考 (References)
