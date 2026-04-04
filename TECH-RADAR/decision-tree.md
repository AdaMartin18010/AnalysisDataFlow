# 流计算技术选型决策树

> 所属阶段: Knowledge | 前置依赖: [技术雷达](./README.md) | 形式化等级: L3

## 1. 概述

本决策树帮助技术团队在面对流计算技术选型时，系统化地评估各种因素，做出最适合业务场景的决策。

## 2. 核心决策流程

```mermaid
flowchart TD
    Start([开始选型]) --> Q1{是否需要<br/>Exactly-Once语义?}

    Q1 -->|是| Q2{延迟要求<br/>亚秒级?}
    Q1 -->|否| Q3{批处理为主<br/>偶尔流处理?}

    Q2 -->|是| Q4{状态复杂度<br/>高?}
    Q2 -->|否| Q5{秒级延迟<br/>可接受?}

    Q4 -->|是| A1[Apache Flink]
    Q4 -->|否| A2[Kafka Streams]

    Q5 -->|是| Q6{已有Spark生态?}
    Q5 -->|否| A1

    Q6 -->|是| A3[Spark Structured Streaming]
    Q6 -->|否| A1

    Q3 -->|是| A4[Spark Batch + 微批]
    Q3 -->|否| Q7{SQL优先<br/>无代码?}

    Q7 -->|是| Q8{需要物化视图?}
    Q7 -->|否| Q9{云原生优先?}

    Q8 -->|是| A5[RisingWave/Materialize]
    Q8 -->|否| A6[ksqlDB/Flink SQL]

    Q9 -->|是| Q10{多租户SaaS?}
    Q9 -->|否| Q11{团队Java能力?}

    Q10 -->|是| A7[Confluent/Upstash Kafka]
    Q10 -->|否| A8[托管Flink服务]

    Q11 -->|强| A1
    Q11 -->|一般| Q12{Python生态?}

    Q12 -->|是| A9[PyFlink/Faust]
    Q12 -->|否| A10[Go/Rust原生方案]
```

## 3. 场景化决策矩阵

### 3.1 实时数据处理场景

| 场景特征 | 推荐技术 | 备选方案 | 关键考量 |
|----------|----------|----------|----------|
| **金融风控** (毫秒级延迟) | Apache Flink | Redpanda + Flink | 状态一致性、Checkpoint |
| **电商实时推荐** | Flink + Redis | RisingWave | 特征实时性、低延迟 |
| **IoT设备监控** | Flink/Mqtt | Kafka Streams | 高吞吐、乱序处理 |
| **日志分析** | Flink + ES | ClickHouse | 海量数据、Schema灵活 |
| **CDC数据同步** | Flink CDC | Debezium + Kafka | 多源支持、Schema变更 |

### 3.2 技术栈匹配

```mermaid
graph TB
    subgraph 现有技术栈评估
        Java[Java团队] --> F1[Apache Flink]
        Scala[Scala团队] --> F1
        Python[Python/ML团队] --> F2[PyFlink/Bytewax]
        Go[Go团队] --> F3[Benthos/Vector]
        Rust[Rust团队] --> F4[RisingWave/Timely]
    end

    subgraph 基础设施现状
        K8s[Kubernetes] --> D1[Operator部署]
        Cloud[公有云] --> D2[托管服务]
        VM[虚拟机] --> D3[Standalone/YARN]
    end

    subgraph 数据源类型
        Kafka[已有Kafka] --> S1[原生集成]
        Pg[PostgreSQL CDC] --> S2[Flink CDC]
        Files[文件/对象存储] --> S3[批流统一]
    end
```

## 4. 详细决策路径

### 4.1 延迟需求决策

```mermaid
flowchart LR
    subgraph 延迟层级
        L1[< 10ms] --> T1[专用硬件/FPGA]
        L2[10ms-100ms] --> T2[Flink低延迟模式]
        L3[100ms-1s] --> T3[标准Flink/KStreams]
        L4[1s-10s] --> T4[Spark Streaming]
        L5[> 10s] --> T5[微批/定时任务]
    end
```

**决策要点:**

| 延迟要求 | 技术选择 | 配置重点 |
|----------|----------|----------|
| < 50ms | Flink + RocksDB本地状态 | 禁用远程状态、优化序列化 |
| 50-200ms | Flink标准配置 | 调整Checkpoint间隔 |
| 200ms-1s | Flink/Kafka Streams | 平衡延迟与吞吐量 |
| > 1s | Spark/Flink均可 | 优先考虑开发效率 |

### 4.2 状态管理决策

```mermaid
flowchart TD
    StateQ{状态类型?} -->|无状态| NS[任意引擎]
    StateQ -->|键值状态| KS{状态大小?}
    StateQ -->|窗口聚合| WA{窗口类型?}

    KS -->|< 1GB| KS1[RocksDB本地]
    KS -->|1-100GB| KS2[RocksDB + 增量Checkpoint]
    KS -->|> 100GB| KS3[ForSt远程状态]

    WA -->|滚动/滑动| WA1[Flink标准窗口]
    WA -->|会话| WA2[Flink会话窗口]
    WA -->|自定义| WA3[ProcessFunction]
```

### 4.3 一致性级别决策

| 一致性要求 | 推荐方案 | 实现方式 |
|------------|----------|----------|
| **Exactly-Once** | Flink Checkpoint + 幂等Sink | 两阶段提交 |
| **At-Least-Once** | Kafka + 去重 | 幂等生产者 |
| **最终一致** | 异步Sink + 补偿 | 最大努力交付 |

## 5. 技术对比矩阵

### 5.1 流处理引擎对比

| 维度 | Apache Flink | Kafka Streams | Spark Streaming | RisingWave |
|------|-------------|---------------|-----------------|------------|
| **延迟** | 毫秒级 | 毫秒级 | 秒级 | 毫秒级 |
| **语义** | Exactly-Once | Exactly-Once | Exactly-Once | Exactly-Once |
| **状态管理** | ★★★★★ | ★★★☆☆ | ★★★★☆ | ★★★★★ |
| **SQL支持** | ★★★★☆ | ★★☆☆☆ | ★★★★☆ | ★★★★★ |
| **生态集成** | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★☆☆ |
| **学习曲线** | 中等 | 低 | 低 | 低 |
| **云原生** | ★★★★★ | ★★★☆☆ | ★★★★☆ | ★★★★★ |

### 5.2 存储方案对比

| 场景 | 推荐存储 | 优势 | 劣势 |
|------|----------|------|------|
| 实时状态 | RocksDB | 低延迟、嵌入式 | 内存限制 |
| 大状态 | ForSt/S3 | 无限扩展 | 网络延迟 |
| 湖仓一体 | Paimon/Iceberg | 批流统一 | 成熟度 |
| 消息队列 | Kafka | 高吞吐、持久化 | 运维成本 |
| 向量存储 | PGVector/Milvus | AI集成 | 专用场景 |

## 6. 成本效益分析

### 6.1 TCO估算模型

```
总拥有成本(TCO) = 开发成本 + 基础设施成本 + 运维成本 + 机会成本

其中:
- 开发成本 = 学习曲线 × 人天 × 人力成本
- 基础设施成本 = 计算资源 + 存储资源 + 网络流量
- 运维成本 = 监控 + 告警 + 故障处理 + 版本升级
- 机会成本 = 技术债务 + 迁移风险
```

### 6.2 规模适配建议

| 数据规模 | 推荐架构 | 预估成本 |
|----------|----------|----------|
| < 1K TPS | 单机/嵌入式 | $500-2000/月 |
| 1K-10K TPS | 小型集群 | $2000-8000/月 |
| 10K-100K TPS | 中型集群 | $8000-30000/月 |
| > 100K TPS | 大型集群/云原生 | $30000+/月 |

## 7. 风险评估矩阵

| 风险类型 | 低风险 | 中风险 | 高风险 |
|----------|--------|--------|--------|
| **技术成熟度** | Kafka, Flink 2.0 | RisingWave, Paimon | Wasm UDF, AI Agent |
| **社区支持** | Apache顶级项目 | 活跃商业项目 | 新兴小众项目 |
| **人才获取** | Java/Flink | Python/Go | Rust/Scala |
| **供应商锁定** | 开源方案 | 云托管服务 | 专有SaaS |

## 8. 迁移决策检查清单

### 8.1 从批处理迁移到流处理

- [ ] 业务场景是否需要实时洞察？
- [ ] 现有ETL是否可以增量执行？
- [ ] 数据源是否支持CDC？
- [ ] 团队是否具备流处理经验？
- [ ] 基础设施是否支持持续运行？

### 8.2 引擎迁移评估

- [ ] 现有作业的SQL/DataStream代码量
- [ ] 自定义Connector/Format数量
- [ ] 状态数据大小与迁移策略
- [ ] 生产环境的SLA要求
- [ ] 回滚方案是否就绪

## 9. 决策支持工具

### 9.1 交互式决策助手

访问 [decision-helper.html](./visuals/decision-helper.html) 使用交互式决策工具。

### 9.2 快速决策参考卡

```
┌─────────────────────────────────────────────────────────┐
│              流计算技术选型速查卡                         │
├─────────────────────────────────────────────────────────┤
│  低延迟(<100ms)    →  Apache Flink                      │
│  高吞吐(>100K TPS) →  Apache Flink + Kafka              │
│  SQL优先           →  Flink SQL / RisingWave            │
│  云原生            →  托管Flink / Confluent             │
│  Python生态        →  PyFlink / Bytewax                 │
│  无状态简单转换    →  Kafka Streams / Benthos           │
│  AI/ML集成         →  Flink + 模型服务                  │
│  成本敏感          →  开源方案 + K8s自托管              │
└─────────────────────────────────────────────────────────┘
```

## 10. 引用参考


---

*最后更新: 2026-04-04*
