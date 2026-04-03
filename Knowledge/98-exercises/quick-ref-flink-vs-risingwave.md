# Flink vs RisingWave 快速参考卡片

> **快速查阅**: 流处理引擎选型决策、性能对比、功能矩阵
>
> **完整文档**: [flink-vs-risingwave.md](../04-technology-selection/flink-vs-risingwave.md)

---

## 🎯 选型决策速查

### 30秒决策法

```
┌─────────────────────────────────────────────────────────────┐
│                    核心决策路径                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 延迟要求 < 50ms? ──YES──► 选 Flink                       │
│                            │                                │
│                            NO                               │
│                            ▼                                │
│  2. 需要 CEP / 复杂事件匹配? ──YES──► 选 Flink                │
│                                   │                         │
│                                   NO                        │
│                                   ▼                         │
│  3. 需要自定义算子 (非SQL逻辑)? ──YES──► 选 Flink             │
│                                        │                    │
│                                        NO                   │
│                                        ▼                    │
│  4. 状态规模 > 10TB? ──YES──► 选 RisingWave                  │
│                            │                                │
│                            NO                               │
│                            ▼                                │
│  5. 团队熟悉 PostgreSQL? ──YES──► 选 RisingWave              │
│                                │                            │
│                                NO                           │
│                                ▼                            │
│  6. 需要低运维成本? ──YES──► 选 RisingWave                    │
│                         │                                   │
│                         NO                                  │
│                         ▼                                   │
│                    两者皆可，按团队经验                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 场景匹配速查表

| 应用场景 | 首选 | 理由 |
|----------|------|------|
| **实时数仓/CDC同步** | RisingWave | 原生CDC+物化视图，无需Kafka |
| **实时推荐（低延迟）** | Flink | 毫秒级延迟优势 |
| **金融风控CEP** | Flink | RisingWave不支持MATCH_RECOGNIZE |
| **IoT数据分析** | RisingWave | 无限状态支持 |
| **实时报表/仪表盘** | RisingWave | 即席查询友好，PostgreSQL协议 |
| **复杂ETL管道** | Flink | 连接器生态更丰富 |
| **边缘流处理** | Flink | 资源受限环境支持更好 |

---

## ⚡ 性能对比速查表

### Nexmark基准测试

| 查询 | 描述 | RisingWave | Flink | 差异 |
|------|------|------------|-------|------|
| q0-q3 | 简单吞吐 | ~893k r/s | ~800k r/s | RW +12% |
| q4 | 窗口聚合 | 84.3k r/s | 70k r/s | RW +20% |
| q7 | 复杂状态 | **219k r/s** | ~3.5k r/s | **RW 62x** |
| q7-优化 | 重写版本 | **770k r/s** | - | **RW 220x** |

### 关键性能指标

| 指标 | Flink 1.18 | RisingWave | 胜出方 |
|------|------------|------------|--------|
| **最小延迟** | ~5ms | ~50ms | Flink |
| **典型延迟** | 10-100ms | 100ms-1s | Flink |
| **Checkpoint时间** | 30s-分钟级 | **1s** | RisingWave |
| **故障恢复** | 分钟级 | **秒级** | RisingWave |
| **复杂Join吞吐** | 3.5k r/s | **219k r/s** | RisingWave |
| **内存效率** | 中 | **高** | RisingWave |
| **CPU利用率** | 中 | **高** | RisingWave |

### 架构对比

```
┌─────────────────────────────────────────────────────────────┐
│  Apache Flink                    RisingWave                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐                ┌──────────────┐          │
│  │  JobManager  │                │   Meta Node  │          │
│  │  (调度协调)   │                │  (调度协调)   │          │
│  └──────┬───────┘                └──────┬───────┘          │
│         │                               │                   │
│  ┌──────▼──────────────────┐   ┌────────▼────────┐         │
│  │    TaskManager Pool     │   │  Compute Nodes  │         │
│  │  ┌─────┐ ┌─────┐ ┌────┐ │   │  (Stateless)    │         │
│  │  │Slot │ │Slot │ │Slot│ │   └────────┬────────┘         │
│  │  │+    │ │+    │ │+   │ │            │                   │
│  │  │Rock│ │Rock│ │Rock│ │   ┌─────────▼─────────┐         │
│  │  │sDB │ │sDB │ │sDB │ │   │  Hummock Layer    │         │
│  │  └─────┘ └─────┘ └────┘ │   │  (LSM-Tree)       │         │
│  │   ↑本地状态存储           │   └─────────┬─────────┘         │
│  │   ↓异步快照              │             │                   │
│  │  ┌─────────────────────┐ │   ┌─────────▼─────────┐         │
│  └──┤  S3/HDFS Checkpoint │─┘   │  S3/GCS/Azure Blob│         │
│     └─────────────────────┘     │  (Primary Storage)│         │
│                                 └───────────────────┘         │
│                                                             │
│  计算-存储紧耦合                计算-存储分离                  │
│  状态本地访问 (低延迟)          状态远程访问 (可扩展)           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 功能特性对比矩阵

### 核心功能

| 特性 | Flink | RisingWave | 说明 |
|------|-------|------------|------|
| **SQL方言** | Flink SQL | PostgreSQL | RW兼容psql生态 |
| **物化视图** | ⚠️ 有限 | ✅ 原生核心 | RW增量维护 |
| **即席查询** | ❌ 需外部DB | ✅ 内置 | RW支持点查 |
| **CDC源** | Flink CDC | 原生直连 | RW免Kafka中间件 |
| **CEP支持** | ✅ MATCH_RECOGNIZE | ❌ 不支持 | Flink优势场景 |
| **窗口类型** | 丰富 | 标准 | Flink更灵活 |
| **自定义算子** | ✅ DataStream API | ❌ SQL only | Flink可扩展性强 |
| **UDF支持** | Java/Python/Scala | Python/Java/Rust | 相当 |
| **连接器数** | 50+ | 50+ | 相当 |
| **数据湖Sink** | Paimon/Iceberg | Iceberg/Delta | 相当 |
| **向量检索** | ❌ | ✅ v2.6+ | RW领先 |

### 架构特性

| 特性 | Flink 1.x | Flink 2.0 | RisingWave |
|------|-----------|-----------|------------|
| **计算-存储** | 紧耦合 | 松耦合 (ForSt) | 完全分离 |
| **状态位置** | 本地RocksDB | 本地+S3 | S3主存储 |
| **状态访问延迟** | ~10μs | ~10μs-10ms | ~10ms(可缓存) |
| **计算节点** | 有状态 | 混合 | 无状态 |
| **扩容操作** | 停止→重分配→启动 | 渐进式重平衡 | 热扩容 |
| **编程语言** | Java/Scala | Java/Scala | Rust |
| **运行时** | JVM | JVM | 原生二进制 |

---

## 💰 运维成本对比

| 成本项 | Flink | RisingWave | 胜出 |
|--------|-------|------------|------|
| **基础设施成本** | 高（大内存+SSD） | 低（S3+小内存） | RW |
| **运维人力** | 高（集群管理） | 低（托管服务化） | RW |
| **状态调优** | 需RocksDB专家 | 无需调优 | RW |
| **扩容操作** | 停机重分配 | 热扩容 | RW |
| **学习曲线** | 陡峭（多概念） | 平缓（SQL即可） | RW |
| **云服务成熟度** | 高（Ververica等） | 中（发展中） | Flink |
| **社区规模** | 大（Apache顶级） | 中（快速成长） | Flink |

---

## ✅ 选型Checklist

### 选择Flink如果满足任一条件

- [ ] 端到端延迟要求 < 50ms
- [ ] 需要复杂事件处理 (CEP / MATCH_RECOGNIZE)
- [ ] 需要自定义算子（非SQL可表达逻辑）
- [ ] 需要 DataStream API 进行细粒度控制
- [ ] 有专职流处理团队，愿意投入学习成本
- [ ] 已有 Flink 基础设施和运维经验
- [ ] 需要与特定生态（如Paimon）深度集成

### 选择RisingWave如果满足任一条件

- [ ] 团队熟悉 PostgreSQL，希望SQL-first开发
- [ ] 状态规模预期超过 10TB 或不可预测
- [ ] 需要内置物化视图和即席查询能力
- [ ] 希望简化CDC管道（直连MySQL/PostgreSQL）
- [ ] 希望降低运维复杂度（单二进制部署）
- [ ] 希望降低存储成本（S3替代SSD）
- [ ] 需要快速故障恢复（秒级RTO）
- [ ] 弹性扩缩容需求频繁（云原生环境）

### 考虑混合架构如果

- [ ] 既有低延迟场景，又有SQL分析需求
- [ ] 已有Flink集群，但希望简化部分SQL pipeline
- [ ] 数据量极大，需要分层处理（实时层+分析层）

---

## 🔄 迁移建议速查

| 迁移路径 | 难度 | 风险 | 建议 |
|----------|------|------|------|
| Flink SQL → RisingWave | 低 | 低 | SQL语义兼容，可直接迁移 |
| Flink DataStream → RisingWave | 高 | 高 | 需重写为SQL，评估可行性 |
| Spark Streaming → RisingWave | 中 | 中 | SQL层迁移较平滑 |
| ksqlDB → RisingWave | 低 | 低 | RisingWave完全覆盖ksqlDB能力 |
| RisingWave → Flink | 中 | 中 | 如需CEP或更低延迟 |

---

## 📚 延伸阅读

| 文档 | 内容 |
|------|------|
| [flink-vs-risingwave.md](../04-technology-selection/flink-vs-risingwave.md) | 完整深度对比分析 |
| [risingwave-deep-dive.md](../06-frontier/risingwave-deep-dive.md) | RisingWave深度解析 |
| [engine-selection-guide.md](../04-technology-selection/engine-selection-guide.md) | 流处理引擎通用选型指南 |
| [streaming-database-guide.md](../04-technology-selection/streaming-database-guide.md) | 流数据库选型指南 |

---

*快速参考卡片 v1.0 | 最后更新: 2026-04-03*
