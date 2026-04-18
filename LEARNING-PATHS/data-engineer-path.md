# 数据工程师学习路径

> **难度级别**: 中级 | **预计时长**: 8-12周 | **目标受众**: 数据工程师、ETL开发者、数据平台工程师

---

## 路径概览

### 学习目标

- 掌握流处理核心概念和架构
- 熟练使用Flink进行数据处理
- 理解Checkpoint和Exactly-Once语义
- 具备生产环境调优和故障排查能力

### 前置知识要求

- 熟悉SQL和至少一种编程语言(Java/Python/Scala)
- 了解基础的数据库概念
- 有批处理数据处理经验

### 完成标准

完成所有阶段学习，通过自测检查点，并独立完成至少一个综合项目

---

## 阶段划分

### 阶段1: 基础概念阶段

**时间安排**: 第1-2周

**学习主题**:

- 流处理基础概念与批处理的区别
- 时间语义（Event Time / Processing Time / Ingestion Time）
- Window机制与触发器
- Flink架构概览

**推荐文档**:

- [Knowledge/01-concept-atlas/streaming-models-mindmap.md](../Knowledge/01-concept-atlas/streaming-models-mindmap.md)
- [Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md](../Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md)
- [Flink/01-architecture/deployment-architectures.md](../Flink/01-concepts/deployment-architectures.md)
- [Flink/02-core/time-semantics-and-watermark.md](../Flink/02-core/time-semantics-and-watermark.md)

**实践任务**:

1. 搭建本地Flink开发环境
2. 运行官方WordCount示例
3. 修改示例，使用Event Time处理

---

### 阶段2: Flink核心机制

**时间安排**: 第3-5周

**学习主题**:

- Checkpoint机制原理与配置
- Exactly-Once语义实现
- 状态管理与状态后端
- Watermark传播与迟到数据处理

**推荐文档**:

- [Flink/02-core/checkpoint-mechanism-deep-dive.md](../Flink/02-core/checkpoint-mechanism-deep-dive.md)
- [Flink/02-core/exactly-once-semantics-deep-dive.md](../Flink/02-core/exactly-once-semantics-deep-dive.md)
- [状态后端选择](../Flink/02-core/state-backends-deep-comparison.md)
- [Struct/02-properties/02.02-consistency-hierarchy.md](../Struct/02-properties/02.02-consistency-hierarchy.md)
- [Struct/02-properties/02.03-watermark-monotonicity.md](../Struct/02-properties/02.03-watermark-monotonicity.md)

**实践任务**:

1. 配置并观察Checkpoint过程
2. 对比不同状态后端的性能
3. 实现一个有状态计算作业

---

### 阶段3: 实践应用阶段

**时间安排**: 第6-8周

**学习主题**:

- Flink SQL与Table API
- 连接器（Kafka、CDC、文件系统）
- 部署与运维（Kubernetes）
- 设计模式与最佳实践

**推荐文档**:

- [Flink/03-sql-table-api/flink-sql-window-functions-deep-dive.md](../Flink/03-api/03.02-table-sql-api/flink-sql-window-functions-deep-dive.md)
- [Flink/03-sql-table-api/materialized-tables.md](../Flink/03-api/03.02-table-sql-api/materialized-tables.md)
- [Flink/04-connectors/kafka-integration-patterns.md](../Flink/05-ecosystem/05.01-connectors/kafka-integration-patterns.md)
- [Flink/04-connectors/flink-cdc-3.0-data-integration.md](../Flink/05-ecosystem/05.01-connectors/flink-cdc-3.0-data-integration.md)
- [Flink/05-ecosystem/flink-dynamic-iceberg-sink-guide.md](../Flink/05-ecosystem/flink-dynamic-iceberg-sink-guide.md)
- [Flink/05-ecosystem/05.01-connectors/fluss-integration.md](../Flink/05-ecosystem/05.01-connectors/fluss-integration.md)
- [Flink/05-ecosystem/05.02-lakehouse/flink-paimon-integration.md](../Flink/05-ecosystem/05.02-lakehouse/flink-paimon-integration.md)
- [Flink/10-deployment/kubernetes-deployment.md](../Flink/04-runtime/04.01-deployment/kubernetes-deployment.md)
- [Knowledge/02-design-patterns/pattern-event-time-processing.md](../Knowledge/02-design-patterns/pattern-event-time-processing.md)
- [Knowledge/02-design-patterns/pattern-windowed-aggregation.md](../Knowledge/02-design-patterns/pattern-windowed-aggregation.md)
- [Knowledge/09-anti-patterns/anti-pattern-checklist.md](../Knowledge/09-anti-patterns/anti-pattern-checklist.md)

**实践任务**:

1. 使用Flink SQL实现复杂查询
2. 搭建CDC数据同步Pipeline
3. 在Kubernetes上部署Flink作业

---

### 阶段4: 高级优化阶段

**时间安排**: 第9-12周

**学习主题**:

- 性能调优与反压处理
- 生产环境实践案例
- 监控与告警
- 技术选型决策

**推荐文档**:

- [Flink/02-core/backpressure-and-flow-control.md](../Flink/02-core/backpressure-and-flow-control.md)
- [Flink/06-engineering/performance-tuning-guide.md](../Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md)
- [Flink/07-case-studies/case-realtime-analytics.md](../Flink/09-practices/09.01-case-studies/case-realtime-analytics.md)
- [Flink/07-case-studies/case-ecommerce-realtime-recommendation.md](../Flink/09-practices/09.01-case-studies/case-ecommerce-realtime-recommendation.md)
- [Knowledge/03-business-patterns/iot-stream-processing.md](../Knowledge/03-business-patterns/iot-stream-processing.md)
- [Knowledge/04-technology-selection/engine-selection-guide.md](../Knowledge/04-technology-selection/engine-selection-guide.md)

**实践任务**:

1. 分析并解决一个反压问题
2. 完成一次性能调优实践
3. 编写技术选型报告

---

## 学习资源索引

### 核心理论 (Struct/)

| 文档 | 主题 | 难度 | 预计时间 |
|------|------|------|----------|
| `02.02-consistency-hierarchy.md` | 一致性层次结构 | L3 | 2h |
| `02.03-watermark-monotonicity.md` | Watermark单调性 | L3 | 2h |
| `04.01-flink-checkpoint-correctness.md` | Checkpoint正确性 | L4 | 4h |
| `04.02-flink-exactly-once-correctness.md` | Exactly-Once正确性 | L4 | 4h |

### 工程知识 (Knowledge/)

| 文档 | 主题 | 难度 | 预计时间 |
|------|------|------|----------|
| `01-concept-atlas/streaming-models-mindmap.md` | 流处理模型思维导图 | L2 | 2h |
| `02-design-patterns/pattern-event-time-processing.md` | 事件时间处理 | L3 | 3h |
| `02-design-patterns/pattern-windowed-aggregation.md` | 窗口聚合 | L2 | 2h |
| `09-anti-patterns/anti-pattern-checklist.md` | 反模式检查清单 | L2 | 2h |

### Flink 实践 (Flink/)

| 文档 | 主题 | 难度 | 预计时间 |
|------|------|------|----------|
| `02-core-mechanisms/checkpoint-mechanism-deep-dive.md` | Checkpoint机制 | L3 | 4h |
| `02-core-mechanisms/exactly-once-semantics-deep-dive.md` | Exactly-Once语义 | L3 | 4h |
| `03-sql-table-api/flink-sql-window-functions-deep-dive.md` | SQL窗口函数 | L3 | 3h |
| `04-connectors/flink-cdc-3.0-data-integration.md` | CDC数据集成 | L3 | 4h |
| `05-ecosystem/flink-dynamic-iceberg-sink-guide.md` | Dynamic Iceberg Sink | L3 | 4h |
| `05-ecosystem/05.01-connectors/fluss-integration.md` | Fluss流存储集成 | L3 | 3h |
| `05-ecosystem/05.02-lakehouse/flink-paimon-integration.md` | Paimon湖仓集成 | L3 | 3h |

---

## 实践项目

### 项目1: 实时日志分析Pipeline

**项目描述**: 构建一个实时日志收集、分析和可视化系统

**技术要求**:

- 使用Flink CDC从多个数据源收集日志
- 实时统计错误率、响应时间等指标
- 支持按服务、时间段等维度聚合
- 输出到存储并支持查询

**产出物**:

- 完整的Flink作业代码
- 部署配置文档
- 监控Dashboard配置

---

### 项目2: 用户行为实时分析Dashboard

**项目描述**: 实时分析用户行为数据，提供实时指标

**技术要求**:

- 使用Flink SQL进行复杂分析
- 实现会话窗口分析用户行为序列
- 支持实时推荐触发
- 低延迟（<1秒）输出

**产出物**:

- SQL脚本集合
- 数据处理流程图
- 性能测试报告

---

### 项目3: 电商实时推荐流

**项目描述**: 基于实时用户行为生成个性化推荐

**技术要求**:

- 实时特征工程（用户画像、商品特征）
- 与机器学习模型集成
- A/B测试框架支持
- 高可用设计

**产出物**:

- 架构设计文档
- 完整代码实现
- 上线运行报告

---

## 自测检查点

- [ ] **检查点1**: 能够解释Event Time和Processing Time的区别，并说明各自适用场景
- [ ] **检查点2**: 能够设计合理的Checkpoint策略（间隔、超时、并发数）
- [ ] **检查点3**: 能够诊断和解决反压问题，理解反压传播机制
- [ ] **检查点4**: 能够完成生产环境的部署配置，包括HA设置
- [ ] **检查点5**: 能够识别常见的反模式并给出改进方案
- [ ] **检查点6**: 能够进行技术选型分析，比较不同方案的优劣

---

## 延伸阅读

- Apache Flink官方文档: <https://nightlies.apache.org/flink/>
- Kleppmann《Designing Data-Intensive Applications》第11章
- Akidau《Streaming Systems》全书
- Flink Forward演讲视频

---

*此学习路径为AnalysisDataFlow项目预定义路径*
