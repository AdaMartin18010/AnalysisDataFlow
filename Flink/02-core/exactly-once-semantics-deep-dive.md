# Exactly-Once语义深度解析

> 所属阶段: Flink Stage 2 | 前置依赖: [checkpoint-mechanism-deep-dive.md](./checkpoint-mechanism-deep-dive.md), [flink-state-management-complete-guide.md](./flink-state-management-complete-guide.md) | 形式化等级: L5

## 1. 概念定义 (Definitions)

### 1.1 一致性语义的形式化定义

**定义 Def-F-02-91 (Exactly-Once语义)**

给定流处理系统 $S = (I, O, T, \Sigma)$，其中 $I$ 为输入事件流，$O$ 为输出事件流，$T$ 为转换算子集合，$\Sigma$ 为状态空间。系统在事件 $e$ 上满足 **Exactly-Once处理语义** 当且仅当：

$$\forall e \in I: \quad |\{ o \in O \mid o = T(e) \land \text{committed}(o) \}| = 1$$

其中 $\text{committed}(o)$ 表示输出 $o$ 已被持久化确认。即每个输入事件在故障恢复后**恰好产生一次**持久化输出。

**定义 Def-F-02-92 (端到端Exactly-Once)**

端到端Exactly-Once要求处理链路满足三要素：

1. **Source可重放性 (Replayable Source)**:
   $$\exists \text{replay}: \text{Offset} \times \text{Timestamp} \rightarrow I_{\geq \text{offset}}$$

2. **引擎Exactly-Once (Engine Exactly-Once)**: 如 Def-F-02-91 所定义

3. **Sink事务性 (Transactional Sink)**:
   $$\forall B \in \text{Batches}: \quad \text{commit}(B) \iff \text{checkpoint}(C_k) \land B \in C_k$$

**定义 Def-F-02-93 (一致性语义分类)**

| 语义级别 | 形式化定义 | 输出保证 |
|---------|-----------|---------|
| **At-Most-Once** | $\forall e: |O_e| \leq 1$ | 可能丢失，绝不重复 |
| **At-Least-Once** | $\forall e: |O_e| \geq 1$ | 绝不丢失，可能重复 |
| **Exactly-Once** | $\forall e: |O_e| = 1$ | 既不丢失，也不重复 |

其中 $O_e = \{ o \in O \mid o \text{ derived from } e \}$ 表示事件 $e$ 产生的输出集合。

**定义 Def-F-02-94 (屏障对齐与非对齐)**

- **对齐Checkpoint (Aligned Checkpoint)**:
  $$\forall \text{channel } c: \quad \text{barrier}_b^c \text{ received} \Rightarrow \text{block inputs until all barriers}_b \text{ received}$$

- **非对齐Checkpoint (Unaligned Checkpoint)**:
  $$\text{barrier}_b \text{ injected} \Rightarrow \text{snapshot in-flight data immediately without blocking}$$

### 1.2 两阶段提交协议形式化

**定义 Def-F-02-95 (2PC协议状态机)**

两阶段提交协议状态转移系统 $M_{2PC} = (S, S_0, \Sigma, \delta)$，其中：

- 状态集 $S = \{\text{INIT}, \text{PREPARING}, \text{PREPARED}, \text{COMMITTING}, \text{COMMITTED}, \text{ABORTING}, \text{ABORTED}\}$
- 初始状态 $S_0 = \text{INIT}$
- 事件集 $\Sigma = \{\text{prepare}, \text{ack}, \text{commit}, \text{abort}, \text{timeout}\}$
- 转移函数 $\delta: S \times \Sigma \rightarrow S$

```
INIT --(prepare)--> PREPARING --(ack)--> PREPARED --(commit)--> COMMITTING --> COMMITTED
                                           |
                                           v
                                         (abort) --> ABORTING --> ABORTED
```

## 2. 属性推导 (Properties)

### 2.1 一致性保证的基本性质

**引理 Lemma-F-02-71 (屏障对齐保证因果一致性)**

若 Flink 作业使用对齐Checkpoint且Checkpoint间隔为 $\Delta$，则：

$$\forall e_i, e_j: \quad e_i \rightarrow e_j \Rightarrow \text{checkpoint}(e_i) \leq \text{checkpoint}(e_j)$$

其中 $e_i \rightarrow e_j$ 表示 Lamport Happens-Before 关系。

**证明概要**: 屏障 $b_k$ 在时刻 $t_k = k \cdot \Delta$ 被注入Source，由于对齐机制确保下游算子仅在收到全部上游屏障后才进行Checkpoint，因此因果关系得以保持。∎

**引理 Lemma-F-02-72 (非对齐Checkpoint的有界一致性)**

非对齐Checkpoint保证：

$$\forall e: \quad \text{in-flight}(e) \in C_k \Rightarrow e \text{ will be reprocessed at most once}$$

其中 in-flight 数据指已发送但尚未被下游确认的事件。

### 2.2 Exactly-Once的充分必要条件

**定理 Thm-F-02-71 (端到端Exactly-Once充分条件)**

流处理系统实现端到端Exactly-Once当且仅当满足：

$$\text{Exactly-Once}_{\text{e2e}} \iff R_{\text{source}} \land E_{\text{engine}} \land T_{\text{sink}}$$

其中：

- $R_{\text{source}}$: Source支持可重放 (如Kafka offset管理)
- $E_{\text{engine}}$: 引擎保证内部Exactly-Once (Checkpoint机制)
- $T_{\text{sink}}$: Sink支持事务或幂等写入

**证明**:

- $(\Rightarrow)$: 若任一条件不满足，存在故障场景导致重复或丢失。
- $(\Leftarrow)$: 三个条件同时满足时，故障恢复后：Source重放至一致偏移，引擎恢复至一致状态，Sink去重或事务提交确保输出唯一。∎

**定理 Thm-F-02-72 (2PC原子性保证)**

给定事务协调者 $C$ 和参与者集合 $P = \{p_1, ..., p_n\}$，2PC协议保证：

$$\forall p_i, p_j \in P: \quad \text{outcome}(p_i) = \text{outcome}(p_j) \in \{\text{COMMITTED}, \text{ABORTED}\}$$

**证明**:

- Phase 1: 协调者收集所有参与者的PREPARE投票
- 若所有参与者投票YES，协调者决定COMMIT；否则决定ABORT
- Phase 2: 协调者广播决定，参与者必须执行
- 协议确保所有参与者最终状态一致 ∎

### 2.3 延迟与一致性权衡

**引理 Lemma-F-02-73 (对齐Checkpoint延迟上界)**

对齐Checkpoint引入的额外延迟 $\delta_{\text{align}}$ 满足：

$$\delta_{align} \leq \max_{\text{paths } P_i} \left( \sum_{e \in P_i} \text{latency}(e) \right) + \text{barrier}_{\text{processing}}$$

在反压场景下，该延迟可能无界增长。

**引理 Lemma-F-02-74 (事务超时与一致性)**

事务超时时间 $T_{\text{timeout}}$ 必须满足：

$$T_{\text{timeout}} > 2 \times \max(T_{\text{network}}, T_{\text{process}}) + \sigma$$

其中 $\sigma$ 为时钟偏差容忍度。否则可能出现不一致提交。

## 3. 关系建立 (Relations)

### 3.1 Exactly-Once与Checkpoint机制的关系

```
┌─────────────────────────────────────────────────────────────┐
│                    Exactly-Once 实现层次                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Source层   │  │  引擎层      │  │  Sink层             │  │
│  │  可重放性    │  │  Checkpoint │  │  事务/幂等          │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         │                │                    │             │
│         └────────────────┼────────────────────┘             │
│                          ▼                                  │
│              ┌─────────────────────┐                        │
│              │   端到端Exactly-Once │                        │
│              └─────────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Flink Exactly-Once与分布式事务的关系

| 特性 | Flink 2PC | 传统分布式事务 (XA) |
|-----|-----------|-------------------|
| 协调者 | JobManager | 独立TM服务 |
| 参与者 | Operators | 数据库/资源管理器 |
| 隔离级别 | 读已提交 | 可串行化 |
| 超时处理 | 事务中止 | 启发式决策 |
| 持久化 | StateBackend | WAL/Redo Log |

### 3.3 Source-Sink一致性矩阵

| Source \ Sink | 事务型Sink | 幂等型Sink | 非幂等Sink |
|--------------|-----------|-----------|-----------|
| **可重放Source** | ✅ Exactly-Once | ✅ Exactly-Once | ⚠️ At-Least-Once |
| **不可重放Source** | ⚠️ At-Least-Once | ⚠️ At-Least-Once | ❌ At-Most-Once |

## 4. 论证过程 (Argumentation)

### 4.1 Exactly-Once必要性的业务论证

**场景1: 金融交易系统**

- 重复扣款: 同一笔交易处理两次导致客户资金损失
- 丢失交易: 交易未记录导致账务不平
- 合规要求: 监管机构要求精确一次处理

**场景2: 实时报表统计**

- 重复计数: 活跃用户数统计偏高
- 丢失事件: GMV计算偏低
- 决策影响: 基于不准确数据的业务决策

### 4.2 屏障对齐的边界分析

**反例: 不对齐导致的重复输出**

考虑双流Join场景：

```
Stream A: [a1] ──barrier── [a2]
                ↓
Stream B: [b1] ─────────── [b2, barrier]
```

若不对齐，算子可能在收到A的barrier后立即Checkpoint，此时：

- a1已处理，a2未处理
- b1和b2都已处理（因为B的barrier还未到）

故障恢复后重放：a1和a2都将与b1、b2再次Join，导致重复输出。

### 4.3 事务ID设计的幂等性分析

**事务ID冲突场景**：

- 若事务ID仅由 jobID + checkpointID 组成
- Job重启后checkpointID从0开始
- 与已提交的历史事务ID冲突
- 结果: 新事务被视为已提交，数据丢失

**解决方案**：

- 事务ID = `jobID` + `checkpointID` + `operatorID` + `attemptID`
- 或使用 Kafka 的 `transactional.id` 自动生成机制

## 5. 工程论证 / 生产最佳实践

### 5.1 Source配置要求

**Kafka Source 可重放配置**：

```java
// 启用自动提交偏移量到Kafka (仅作为参考)
properties.setProperty("enable.auto.commit", "false");

// Flink管理偏移量
FlinkKafkaConsumer<String> source = new FlinkKafkaConsumer<>(
    "topic",
    new SimpleStringSchema(),
    properties
);

// 从最新Checkpoint恢复
source.setStartFromGroupOffsets();
```

**偏移量管理策略对比**：

| 策略 | 配置 | 适用场景 |
|-----|------|---------|
| Group Offsets | `setStartFromGroupOffsets()` | 首次启动或消费者组变更 |
| Earliest | `setStartFromEarliest()` | 数据完整性优先 |
| Latest | `setStartFromLatest()` | 实时性优先 |
| Specific | `setStartFromSpecificOffsets()` | 精确恢复点 |

### 5.2 Sink事务配置

**Kafka Sink 两阶段提交配置**：

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("transaction.timeout.ms", "900000"); // 15分钟
props.put("transactional.id", "flink-sink-" + jobId);

FlinkKafkaProducer<String> sink = new FlinkKafkaProducer<>(
    "output-topic",
    new SimpleStringSchema(),
    props,
    FlinkKafkaProducer.Semantic.EXACTLY_ONCE  // 启用Exactly-Once
);
```

**事务ID前缀管理最佳实践**：

```java
// 方案1: JobID作为前缀
String transactionalIdPrefix = jobId + "-" + operatorId;

// 方案2: 时间戳+随机数
String transactionalIdPrefix =
    "flink-" + System.currentTimeMillis() + "-" + UUID.randomUUID();

// 方案3: 配置指定+序号
String transactionalIdPrefix = config.getString("transaction.id.prefix") + subtaskIndex;
```

### 5.3 Checkpoint调优策略

**间隔与延迟权衡**：

| Checkpoint间隔 | 恢复时间 | 处理延迟 | 存储开销 | 适用场景 |
|--------------|---------|---------|---------|---------|
| 1秒 | 短 | 高 | 高 | 低延迟金融 |
| 10秒 | 中 | 中 | 中 | 通用实时 |
| 60秒 | 长 | 低 | 低 | 高吞吐ETL |
| 10分钟 | 很长 | 很低 | 很低 | 批流一体 |

**推荐配置**：

```java
env.enableCheckpointing(60000); // 60秒
env.getCheckpointConfig().setCheckpointingMode(
    CheckpointingMode.EXACTLY_ONCE
);
env.getCheckpointConfig().setMinPauseBetweenCheckpoints(30000);
env.getCheckpointConfig().setCheckpointTimeout(600000);
env.getCheckpointConfig().setMaxConcurrentCheckpoints(1);
env.getCheckpointConfig().enableExternalizedCheckpoints(
    ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION
);
```

### 5.4 故障恢复场景处理

**场景1: JobManager故障**

- HA模式下，Standby JobManager接管
- 从最新Checkpoint恢复
- 事务协调者状态恢复，未完成事务可继续或回滚

**场景2: TaskManager故障**

- 受影响Task重启
- 从Checkpoint恢复状态
- Source从记录的偏移重放

**场景3: 网络分区**

- 检测到超时后触发Checkpoint失败
- 旧Checkpoint用于恢复
- 可能触发事务超时回滚

### 5.5 消费者read_committed配置

```java
Properties consumerProps = new Properties();
consumerProps.put("bootstrap.servers", "localhost:9092");
consumerProps.put("group.id", "my-consumer-group");

// 关键配置：只读取已提交事务的消息
consumerProps.put("isolation.level", "read_committed");

// 可选：调整poll等待时间
consumerProps.put("max.poll.records", "500");
```

## 6. 实例验证 (Examples)

### 6.1 完整Exactly-Once作业配置

```java
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.CheckpointingMode;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaProducer;
import org.apache.flink.streaming.util.serialization.SimpleStringSchema;
import org.apache.flink.runtime.state.filesystem.FsStateBackend;
import org.apache.flink.streaming.api.datastream.DataStream;

import java.util.Properties;

public class ExactlyOnceExample {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        // ========================================
        // 1. Checkpoint配置 (引擎层Exactly-Once)
        // ========================================
        env.enableCheckpointing(60000); // 60秒间隔
        env.getCheckpointConfig().setCheckpointingMode(
            CheckpointingMode.EXACTLY_ONCE
        );
        env.getCheckpointConfig().setMinPauseBetweenCheckpoints(30000);
        env.getCheckpointConfig().setCheckpointTimeout(600000);
        env.getCheckpointConfig().setMaxConcurrentCheckpoints(1);
        env.getCheckpointConfig().enableExternalizedCheckpoints(
            ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION
        );

        // 状态后端配置
        env.setStateBackend(new FsStateBackend("hdfs://namenode:8020/flink/checkpoints"));

        // ========================================
        // 2. Kafka Source配置 (可重放Source)
        // ========================================
        Properties sourceProps = new Properties();
        sourceProps.put("bootstrap.servers", "kafka:9092");
        sourceProps.put("group.id", "exactly-once-consumer");
        sourceProps.put("auto.offset.reset", "earliest");
        // Flink管理偏移量，禁用自动提交
        sourceProps.put("enable.auto.commit", "false");

        FlinkKafkaConsumer<String> source = new FlinkKafkaConsumer<>(
            "input-topic",
            new SimpleStringSchema(),
            sourceProps
        );

        // ========================================
        // 3. 业务处理逻辑
        // ========================================
        DataStream<String> stream = env.addSource(source);

        DataStream<String> processed = stream
            .map(value -> transform(value))
            .keyBy(value -> extractKey(value))
            .window(TumblingEventTimeWindows.of(Time.minutes(5)))
            .aggregate(new MyAggregateFunction());

        // ========================================
        // 4. Kafka Sink配置 (事务型Sink)
        // ========================================
        String jobId = env.getJobID().toString();
        Properties sinkProps = new Properties();
        sinkProps.put("bootstrap.servers", "kafka:9092");
        // 事务超时必须大于Checkpoint间隔
        sinkProps.put("transaction.timeout.ms", "900000"); // 15分钟
        // 事务ID前缀，确保唯一性
        sinkProps.put("transactional.id", "flink-producer-" + jobId);

        FlinkKafkaProducer<String> sink = new FlinkKafkaProducer<>(
            "output-topic",
            new SimpleStringSchema(),
            sinkProps,
            FlinkKafkaProducer.Semantic.EXACTLY_ONCE
        );

        processed.addSink(sink);

        env.execute("Exactly-Once Processing Job");
    }

    private static String transform(String value) {
        // 业务转换逻辑
        return value.toUpperCase();
    }

    private static String extractKey(String value) {
        // 提取Key用于分区
        return value.split(",")[0];
    }
}
```

### 6.2 自定义两阶段提交Sink

```java
import org.apache.flink.streaming.api.functions.sink.TwoPhaseCommitSinkFunction;

/**
 * 自定义两阶段提交Sink实现
 *
 * 实现原理：
 * 1. invoke(): 预写入数据到临时存储
 * 2. snapshotState(): 准备事务
 * 3. notifyCheckpointComplete(): 提交事务
 * 4. recoverAndCommit(): 恢复时提交未完成事务
 * 5. recoverAndAbort(): 恢复时中止未完成事务
 */
public class CustomTwoPhaseCommitSink
    extends TwoPhaseCommitSinkFunction<String, Transaction, Context> {

    public CustomTwoPhaseCommitSink() {
        super(
            TypeInformation.of(String.class).createSerializer(new ExecutionConfig()),
            TypeInformation.of(Transaction.class).createSerializer(new ExecutionConfig())
        );
    }

    @Override
    protected void invoke(Transaction transaction, String value, Context context) {
        // 将数据写入事务缓冲区
        transaction.buffer(value);
    }

    @Override
    protected Transaction beginTransaction() {
        // 开启新事务
        return new Transaction(generateTransactionId());
    }

    @Override
    protected void preCommit(Transaction transaction) {
        // 预提交：刷写到临时位置
        transaction.flushToTemporary();
    }

    @Override
    protected void commit(Transaction transaction) {
        // 正式提交：确认写入
        transaction.commitToPermanent();
    }

    @Override
    protected void abort(Transaction transaction) {
        // 中止事务：清理临时数据
        transaction.rollback();
    }
}

class Transaction {
    private final String txId;
    private final List<String> buffer;

    public Transaction(String txId) {
        this.txId = txId;
        this.buffer = new ArrayList<>();
    }

    public void buffer(String value) {
        buffer.add(value);
    }

    public void flushToTemporary() {
        // 写入临时存储
    }

    public void commitToPermanent() {
        // 原子性移动到最终位置
    }

    public void rollback() {
        // 清理临时数据
    }
}
```

### 6.3 非对齐Checkpoint配置

```java
// Flink 1.11+ 支持非对齐Checkpoint
env.getCheckpointConfig().enableUnalignedCheckpoints(true);

// 配置对齐超时时间
// 超过此时间后自动切换为非对齐模式
env.getCheckpointConfig().setAlignmentTimeout(Duration.ofSeconds(30));

// 或完全禁用对齐（Flink 1.13+）
env.getCheckpointConfig().enableUnalignedCheckpoints();
```

## 7. 可视化 (Visualizations)

### 7.1 端到端Exactly-Once架构图

以下Mermaid图展示了Flink实现端到端Exactly-Once的完整架构，包含Source、引擎、Sink三层：

```mermaid
graph TB
    subgraph Source层[Source层 - 可重放性保证]
        K1[Kafka Partition 1<br/>offset=100]
        K2[Kafka Partition 2<br/>offset=200]
        K3[Kafka Partition N<br/>offset=150]
    end

    subgraph 引擎层[引擎层 - Checkpoint机制]
        JM[JobManager<br/>协调者]
        TM1[TaskManager 1]
        TM2[TaskManager 2]

        subgraph Checkpoint流程
            B1[Barrier注入]
            B2[状态快照]
            B3[确认完成]
        end
    end

    subgraph Sink层[Sink层 - 事务保证]
        TX[事务协调]
        KP[Kafka Producer<br/>事务ID: flink-tx-001]
    end

    K1 --> TM1
    K2 --> TM1
    K3 --> TM2

    TM1 --> TX
    TM2 --> TX
    TX --> KP

    JM -.->|协调| B1
    B1 -.->|触发| TM1
    B1 -.->|触发| TM2
    TM1 -.->|上报| B3
    TM2 -.->|上报| B3
    B3 -.->|通知提交| TX

    style Source层 fill:#e1f5fe
    style 引擎层 fill:#fff3e0
    style Sink层 fill:#e8f5e9
```

### 7.2 两阶段提交流程图

以下序列图展示了2PC协议在Flink中的执行流程：

```mermaid
sequenceDiagram
    participant JM as JobManager<br/>协调者
    participant OP as Operator<br/>参与者
    participant KS as Kafka Sink<br/>事务执行者
    participant K as Kafka Broker

    Note over JM,K: Checkpoint N 触发

    JM->>OP: 注入Barrier
    OP->>OP: 异步快照状态
    OP->>JM: 确认快照完成

    Note over JM,K: Phase 1: 准备阶段

    JM->>KS: preCommit()
    KS->>KS: flush() 刷写缓冲区
    KS->>KS: prepareTransaction()
    KS->>K: send(prepare)
    K-->>KS: ack
    KS-->>JM: PREPARED

    Note over JM,K: Phase 2: 提交阶段

    JM->>JM: 所有参与者确认
    JM->>KS: commit()
    KS->>K: commitTransaction()
    K-->>KS: committed
    KS-->>JM: COMMITTED

    Note over JM,K: 故障恢复场景

    alt 协调者故障恢复
        JM->>KS: recoverAndCommit(txId)
        KS->>K: checkTransaction(txId)
        K-->>KS: PREPARED状态
        KS->>K: commitTransaction(txId)
    else 参与者故障
        JM->>KS: recoverAndAbort(txId)
        KS->>K: abortTransaction(txId)
    end
```

### 7.3 Exactly-Once配置决策树

以下决策树帮助用户选择适合其场景的Exactly-Once配置策略：

```mermaid
flowchart TD
    A[需要Exactly-Once?] -->|是| B{Source类型?}
    A -->|否| Z1[使用At-Least-Once<br/>性能最优]

    B -->|可重放<br/>Kafka/Pulsar| C{Sink类型?}
    B -->|不可重放<br/>Socket/HTTP| Z2[无法实现Exactly-Once<br/>使用At-Least-Once]

    C -->|Kafka| D{延迟要求?}
    C -->|JDBC| E{幂等性?}
    C -->|ES/HBase| F[幂等写入配置]

    D -->|低延迟<br/><100ms| G[非对齐Checkpoint<br/>增量Checkpoint]
    D -->|高吞吐优先| H[对齐Checkpoint<br/>RocksDB增量]

    E -->|有主键| I[幂等INSERT<br/>ON CONFLICT UPDATE]
    E -->|无幂等支持| J[自定义2PC Sink<br/>本地事务表]

    F --> K{是否需要即时可见?}
    K -->|是| L[配置refresh_interval<br/>权衡一致性可见性]
    K -->|否| M[批量写入+幂等ID]

    G --> N[配置检查清单]
    H --> N
    I --> N
    J --> N
    L --> N
    M --> N

    N --> O[事务超时 > Checkpoint间隔 × 2]
    N --> P[read_committed消费者]
    N --> Q[唯一transactional.id]

    style Z1 fill:#ffebee
    style Z2 fill:#ffebee
    style N fill:#e8f5e9
```

### 7.4 屏障对齐 vs 非对齐对比矩阵

```mermaid
graph LR
    subgraph 对齐Checkpoint[对齐Checkpoint]
        A1[Barrier到达] --> A2[阻塞输入]
        A2 --> A3[等待所有Barrier]
        A3 --> A4[同步快照]
        A4 --> A5[恢复输入]
    end

    subgraph 非对齐Checkpoint[非对齐Checkpoint]
        U1[Barrier到达] --> U2[立即快照]
        U2 --> U3[快照in-flight数据]
        U3 --> U4[异步持久化]
        U4 --> U5[无阻塞继续]
    end

    A5 -.->|延迟| L1[反压场景<br/>延迟增加]
    U5 -.->|吞吐| L2[稳定吞吐<br/>状态大小增加]

    style 对齐Checkpoint fill:#fff3e0
    style 非对齐Checkpoint fill:#e1f5fe
```

## 8. 引用参考 (References)











---

*文档版本: v1.0 | 最后更新: 2026-04-03 | 状态: 完成*
