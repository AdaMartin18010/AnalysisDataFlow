# 流计算技术迁移建议

> 所属阶段: Knowledge | 前置依赖: [技术雷达](./README.md), [决策树](./decision-tree.md) | 形式化等级: L3

## 1. 迁移策略总览

### 1.1 迁移路线图

```mermaid
gantt
    title 流计算技术迁移路线图
    dateFormat  YYYY-MM
    section 评估阶段
    现状分析           :a1, 2026-04, 2w
    技术选型           :a2, after a1, 2w
    POC验证            :a3, after a2, 4w
    section 准备阶段
    基础设施搭建       :b1, after a3, 3w
    团队培训           :b2, after a3, 4w
    监控体系           :b3, after b1, 2w
    section 迁移阶段
    影子模式运行       :c1, after b2, 4w
    灰度切换           :c2, after c1, 6w
    全量切换           :c3, after c2, 2w
    section 优化阶段
    性能调优           :d1, after c3, 4w
    成本优化           :d2, after d1, 2w
```

### 1.2 迁移模式选择

| 模式 | 适用场景 | 风险等级 | 时间周期 |
|------|----------|----------|----------|
| **大爆炸** | 小型系统、停机可接受 | 高 | 1-2周 |
**金丝雀** | 关键业务、需验证 | 中 | 4-8周 |
| **蓝绿** | 高可用要求 | 低 | 6-12周 |
| **影子** | 复杂系统、需对比 | 低 | 8-16周 |
| **绞杀者** | 单体拆分 | 中 | 3-6月 |

## 2. 具体迁移路径

### 2.1 Spark Streaming → Apache Flink

**适用场景:**

- 需要更低延迟处理
- 复杂事件处理需求
- 精确一次语义要求

**迁移步骤:**

```mermaid
flowchart TD
    A[Spark Streaming作业] --> B[代码分析]
    B --> C{DStream?}
    C -->|是| D[重构为DataStream API]
    C -->|否| E[直接迁移Structured Streaming]
    D --> F[状态迁移]
    E --> F
    F --> G[Checkpoint适配]
    G --> H[Sink连接器替换]
    H --> I[性能验证]
    I --> J[生产切换]
```

**代码映射示例:**

| Spark | Flink | 注意点 |
|-------|-------|--------|
| `DStream` | `DataStream` | 语义等价 |
| `updateStateByKey` | `KeyedProcessFunction` | 需手动状态管理 |
| `window()` | `window()` + `WindowFunction` | 时间语义差异 |
| `StreamingContext` | `StreamExecutionEnvironment` | 配置方式不同 |
| `KafkaUtils` | `FlinkKafkaConsumer` | 参数映射 |

**详细迁移指南:** [05.1-spark-streaming-to-flink-migration.md](../Knowledge/05-mapping-guides/migration-guides/05.1-spark-streaming-to-flink-migration.md)

### 2.2 Kafka Streams → Apache Flink

**适用场景:**

- 跨Kafka集群处理
- 复杂状态计算
- 多源数据融合

**关键差异:**

```mermaid
graph LR
    subgraph Kafka Streams
        KS1[Kafka Topic] --> KS2[Streams App] --> KS3[Kafka Topic]
        KS2 -.->|状态存储| KS4[RocksDB/Changelog]
    end

    subgraph Apache Flink
        F1[多数据源] --> F2[Flink Job] --> F3[多数据汇]
        F2 -.->|状态| F4[Checkpoint/Savepoint]
    end
```

**迁移检查清单:**

- [ ] Kafka Consumer Group ID重新规划
- [ ] 状态存储从RocksDB → Flink State Backend
- [ ] 拓扑从KStream DSL → DataStream API
- [ ] 窗口语义对齐（Kafka vs Flink时间定义）
- [ ] Exactly-Once配置迁移

**详细迁移指南:** [05.2-kafka-streams-to-flink-migration.md](../Knowledge/05-mapping-guides/migration-guides/05.2-kafka-streams-to-flink-migration.md)

### 2.3 Storm → Apache Flink

**适用场景:**

- Storm项目维护困难
- 需要更好的状态管理
- 精确一次处理需求

**迁移要点:**

```java
// Storm Bolt
public class WordCountBolt extends BaseRichBolt {
    private Map<String, Integer> counts = new HashMap<>();

    @Override
    public void execute(Tuple tuple) {
        String word = tuple.getStringByField("word");
        counts.put(word, counts.getOrDefault(word, 0) + 1);
        collector.emit(new Values(word, counts.get(word)));
    }
}

// Flink 等效实现
DataStream<Tuple2<String, Integer>> wordCounts =
    words.keyBy(word -> word.f0)
         .process(new KeyedProcessFunction<String, String, Tuple2<String, Integer>>() {
             private ValueState<Integer> countState;

             @Override
             public void open(Configuration parameters) {
                 countState = getRuntimeContext()
                     .getState(new ValueStateDescriptor<>("count", Types.INT));
             }

             @Override
             public void processElement(String word, Context ctx,
                                       Collector<Tuple2<String, Integer>> out) throws Exception {
                 int current = countState.value() != null ? countState.value() : 0;
                 countState.update(current + 1);
                 out.collect(new Tuple2<>(word, current + 1));
             }
         });
```

**详细迁移指南:** [05.3-storm-to-flink-migration.md](../Knowledge/05-mapping-guides/migration-guides/05.3-storm-to-flink-migration.md)

### 2.4 Flink 1.x → Flink 2.x

**主要变化:**

- DataStream API V2
- 新的状态后端架构
- 移除Scala 2.11支持

**迁移路径:**

```mermaid
flowchart TD
    Start[Flink 1.18] --> V1[升级到1.19]
    V1 --> V2[升级到1.20]
    V2 --> Check{检查兼容性}
    Check -->|通过| V3[升级到2.0]
    Check -->|不通过| Fix[修复不兼容代码]
    Fix --> V2
    V3 --> State[状态迁移]
    State --> Config[配置更新]
    Config --> Test[测试验证]
```

**关键变更点:**

| Flink 1.x | Flink 2.x | 迁移操作 |
|-----------|-----------|----------|
| `DataStreamSource` | `DataStreamSource` | API兼容 |
| `StateTtlConfig` | 新增`cleanupIncrementally` | 检查清理策略 |
| `RocksDBStateBackend` | `EmbeddedRocksDBStateBackend` | 类名变更 |
| `FsStateBackend` | `HashMapStateBackend` | 类名变更 |
| Scala 2.11 | 移除 | 升级到Scala 2.12/2.13 |

**详细迁移指南:** [05.4-flink-1x-to-2x-migration.md](../Knowledge/05-mapping-guides/migration-guides/05.4-flink-1x-to-2x-migration.md)

### 2.5 批处理 → 流处理架构迁移

**绞杀者模式实施:**

```mermaid
graph TB
    subgraph Phase1[阶段1: 批流共存]
        B1[批处理ETL] --> D1[数据仓库]
        S1[流处理试点] -.-> D1
    end

    subgraph Phase2[阶段2: 关键路径迁移]
        B2[剩余批处理] --> D2[数仓历史数据]
        S2[流处理主链] --> D3[实时数仓]
        D3 -.->|同步| D2
    end

    subgraph Phase3[阶段3: 统一流处理]
        S3[统一流处理] --> D4[湖仓一体]
    end

    Phase1 --> Phase2 --> Phase3
```

**详细迁移指南:** [05.5-batch-to-streaming-migration.md](../Knowledge/05-mapping-guides/migration-guides/05.5-batch-to-streaming-migration.md)

## 3. 状态迁移策略

### 3.1 Savepoint兼容性矩阵

| 源版本 | 目标版本 | 兼容性 | 操作 |
|--------|----------|--------|------|
| 1.18 | 1.19 | ✓ 完全兼容 | 直接恢复 |
| 1.18 | 2.0 | △ 部分兼容 | 检查变更 |
| 1.15 | 2.0 | ✗ 不兼容 | 重新消费 |

### 3.2 状态迁移工具链

```bash
# 1. 创建Savepoint
flink savepoint <jobId> <savepointPath>

# 2. 状态分析
flink-state-analyzer analyze <savepointPath> --output report.json

# 3. 状态转换（如有必要）
flink-state-migrate transform \
    --from <oldSavepoint> \
    --to <newSavepoint> \
    --mapping state-mapping.yaml

# 4. 验证
flink-state-analyzer verify <newSavepoint>
```

## 4. 风险缓解策略

### 4.1 回滚方案

```mermaid
flowchart LR
    subgraph 回滚准备
        A[双版本部署] --> B[数据双写]
        B --> C[流量分割]
    end

    subgraph 回滚触发
        D{异常检测} -->|SLA违反| E[自动回滚]
        D -->|人工判断| F[手动回滚]
    end

    subgraph 回滚执行
        E --> G[切回原系统]
        F --> G
        G --> H[状态恢复]
        H --> I[验证确认]
    end
```

### 4.2 数据一致性保证

| 场景 | 策略 | 工具 |
|------|------|------|
| 并行运行期 | 双写比对 | Apache Griffin |
| 切换时刻 | 断点续传 | Kafka Offset管理 |
| 异常恢复 | 幂等写入 | Sink幂等设计 |
| 长期校验 | 审计日志 | Flink CDC + 比对 |

## 5. 性能基线建立

### 5.1 迁移前基准测试

```yaml
# benchmark-config.yaml
baseline:
  throughput:
    target: 100000  # events/sec
    duration: 10min
  latency:
    p50: < 50ms
    p99: < 200ms
  resource:
    cpu: < 4 cores
    memory: < 8GB

workloads:
  - name: simple-map
    complexity: low
  - name: keyed-aggregation
    complexity: medium
  - name: window-join
    complexity: high
```

### 5.2 迁移后验证

```python
# 自动化验证脚本示例
class MigrationValidator:
    def validate_latency(self, baseline, current):
        """验证延迟指标"""
        assert current.p50 <= baseline.p50 * 1.1
        assert current.p99 <= baseline.p99 * 1.2

    def validate_throughput(self, baseline, current):
        """验证吞吐量"""
        assert current >= baseline * 0.95

    def validate_correctness(self, expected, actual):
        """验证结果正确性"""
        diff = compare_datasets(expected, actual)
        assert diff.error_rate < 0.001
```

## 6. 团队能力建设

### 6.1 培训计划

| 阶段 | 内容 | 时长 | 目标 |
|------|------|------|------|
| **基础** | Flink核心概念 | 2天 | 理解API和语义 |
| **进阶** | 状态管理与容错 | 2天 | 掌握高级特性 |
| **实战** | 项目实战演练 | 1周 | 独立开发能力 |
| **专家** | 源码与调优 | 持续 | 性能优化能力 |

### 6.2 知识转移检查清单

- [ ] 架构设计文档更新
- [ ] 运维手册编写
- [ ] 故障处理Playbook
- [ ] 代码Review指南
- [ ] 性能调优手册

## 7. 成本效益分析模板

### 7.1 ROI计算

```
迁移ROI = (收益 - 成本) / 成本 × 100%

收益组成:
- 延迟降低带来的业务价值
- 运维效率提升节省人力
- 资源利用率优化节省成本
- 故障减少避免的损失

成本组成:
- 迁移开发人力成本
- 双系统并行运行成本
- 培训与文档成本
- 风险准备金
```

### 7.2 迁移决策评分卡

| 维度 | 权重 | 评分(1-5) | 加权分 |
|------|------|-----------|--------|
| 技术必要性 | 25% | | |
| 业务价值 | 25% | | |
| 团队就绪度 | 20% | | |
| 资源可用性 | 15% | | |
| 风险可控性 | 15% | | |
| **总计** | 100% | | **/5** |

评分≥3.5: 建议迁移
评分2.5-3.5: 评估后决定
评分<2.5: 暂缓迁移

## 8. 引用参考


---

*最后更新: 2026-04-04*
