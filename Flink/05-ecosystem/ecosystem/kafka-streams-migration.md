> **状态**: 📦 已归档 | **归档日期**: 2026-04-20
>
> 本文档内容已整合至主文档，此处保留为重定向入口。
> **主文档**: [Knowledge\05-mapping-guides\migration-guides\05.2-kafka-streams-to-flink-migration.md](../../../Knowledge/05-mapping-guides/migration-guides/05.2-kafka-streams-to-flink-migration.md)
> **归档位置**: [../../../archive/content-deduplication/2026-04/Flink/05-ecosystem/ecosystem/kafka-streams-migration.md](../../../archive/content-deduplication/2026-04/Flink/05-ecosystem/ecosystem/kafka-streams-migration.md)

---

## 思维表征补充

以下思维表征为迁移实践提供可视化导航。

### 思维导图：Kafka Streams 迁移到 Flink

迁移全景以 Kafka Streams 迁移到 Flink 为核心，从五大维度放射展开。

```mermaid
mindmap
  root((Kafka Streams<br/>迁移到 Flink))
    动机分析
      更丰富的算子
        KeyBy / Window / ProcessFunction
        SQL / Table API 声明式表达
      更好的状态管理
        Queryable State
        Incremental Checkpoint
        State TTL 细粒度控制
      更强的容错
        Exactly-Once 端到端
        自动 Barrier 对齐
        快速 Failover
      SQL支持
        Flink SQL 统一批流
        Hive / JDBC Catalog 集成
    概念映射
      KStream → DataStream
        无界流抽象等价
        Event Time / Processing Time 语义增强
      KTable → Table
        Changelog Stream 转 Dynamic Table
        Retraction 语义支持
      Topology → JobGraph
        Processor API → Transformation
        物理执行计划透明化
    状态迁移
      RocksDB状态
        复用 RocksDBStateBackend
        SST 文件格式兼容性评估
      Checkpoint格式
        Kafka Streams State Dir ≠ Flink Checkpoint
        自定义 State Processor API 导入
      状态大小评估
        全量 Checkpoint 耗时测算
        增量快照与历史状态清理
    代码迁移
      DSL转换
        stream() → env.fromSource()
        groupByKey() → keyBy()
        aggregate() → window().aggregate()
      ProcessFunction
        Processor → KeyedProcessFunction
        Punctuator → TimerService
      窗口语义
        Tumbling / Sliding / Session 窗口重映射
        Allowed Lateness 与 Watermark 对齐
      Join策略
        Stream-Stream Join → Interval Join / Window Join
        Stream-Table Join → Temporal Join
    验证上线
      并行运行
        双写 Kafka Topic
        影子流量旁路对比
      结果对比
        输出一致性校验
        延迟 / 吞吐指标对齐
      性能基准
        Nexmark / 自定义压测
        Backpressure 与 Checkpoint 调优
      灰度切换
        金丝雀发布
        流量权重渐进切流
```

### 多维关联树：特性映射与迁移注意点

展示 Kafka Streams 特性、Flink 等价能力与迁移注意点之间的映射关系。

```mermaid
graph TB
    subgraph KS[Kafka Streams 特性]
        A1[KStream DSL]
        A2[KTable 物化视图]
        A3[Processor API]
        A4[Interactive Queries]
        A5[Exactly-Once 生产]
        A6[Windowed Operations]
        A7[Standby Replicas]
    end

    subgraph FL[Flink 等价能力]
        B1[DataStream / Table API]
        B2[Dynamic Table / SQL]
        B3[ProcessFunction / AsyncFunction]
        B4[Queryable State / Lookup Join]
        B5[Two-Phase Commit / Kafka EOS]
        B6[Window / Interval Join]
        B7[Regional Recovery / HA 配置]
    end

    subgraph NOTE[迁移注意点]
        C1[算子语义差异: aggregate 触发时机]
        C2[Changelog 格式: +I/-U/-D 需适配]
        C3[状态访问模式: 从本地读取改为分布式]
        C4[查询接口变化: REST → 自定义 Lookup]
        C5[事务 ID 隔离: Flink 需配置 transactional.id.prefix]
        C6[窗口对齐: Event Time Watermark 需显式声明]
        C7[副本策略: Standby → Checkpoint + Savepoint]
    end

    A1 --> B1 --> C1
    A2 --> B2 --> C2
    A3 --> B3 --> C3
    A4 --> B4 --> C4
    A5 --> B5 --> C5
    A6 --> B6 --> C6
    A7 --> B7 --> C7
```

### 决策树：迁移策略选择

根据现有 Kafka Streams 应用复杂度选择适配的迁移路径。

```mermaid
flowchart TD
    Start([开始评估迁移]) --> Q1{拓扑复杂度?}
    Q1 -->|简单拓扑<br/>过滤/映射/聚合| S1[直接 DSL 映射]
    S1 --> S1A[快速迁移<br/>1-2 周交付]
    S1A --> End1([上线完成])

    Q1 -->|复杂状态<br/>大量本地状态存储| S2[状态导出 + Flink 恢复]
    S2 --> S2A[使用 State Processor API<br/>导入历史状态]
    S2A --> S2B[双跑验证<br/>结果一致性校验]
    S2B --> End2([灰度上线])

    Q1 -->|混合架构<br/>部分模块稳定| S3[Kafka Streams 遗留 + Flink 新功能并行]
    S3 --> S3A[边界清晰划分<br/>Topic 契约约定]
    S3A --> S3B[新需求走 Flink<br/>旧模块维持]
    S3B --> End3([渐进演进])

    Q1 -->|全面替换<br/>技术债务重| S4[渐进迁移 + 金丝雀 + 监控对比]
    S4 --> S4A[模块拆分<br/>按业务域逐批迁移]
    S4A --> S4B[金丝雀发布<br/>5% → 50% → 100%]
    S4B --> S4C[监控对比<br/>延迟/吞吐/错误率]
    S4C --> End4([全面切换])
```

## 引用参考
