> **状态**: 🔮 前瞻内容 | **风险等级**: 高 | **最后更新**: 2026-04
> 
> 此文档描述的内容处于早期规划阶段，可能与最终实现不符。请以 Apache Flink 官方发布为准。
# TECH-RADAR 目录索引

> AnalysisDataFlow 项目 - 流计算技术雷达

## 目录结构

```
TECH-RADAR/
├── 00-INDEX.md              # 本索引文件
├── README.md                # 技术雷达主文档
├── evolution-timeline.md    # 技术演进时间线
├── decision-tree.md         # 选型决策树
├── migration-recommendations.md  # 迁移建议
├── risk-assessment.md       # 风险评估
└── visuals/                 # 可视化资源
    ├── radar-chart.svg      # 静态SVG雷达图
    └── interactive-radar.html  # 交互式雷达图
```

## 快速导航

### 技术评估

- [技术雷达总览](./README.md) - 四象限技术分类与清单
- [演进时间线](./evolution-timeline.md) - 技术发展历程与趋势预测

### 决策支持

- [选型决策树](./decision-tree.md) - 系统化选型流程与对比矩阵
- [迁移建议](./migration-recommendations.md) - 各技术栈迁移路径指南
- [风险评估](./risk-assessment.md) - 多维度风险分析与缓解策略

### 可视化

- [静态雷达图](./visuals/radar-chart.svg) - SVG格式技术分布图
- [交互式雷达图](./visuals/interactive-radar.html) - D3.js交互式探索工具

## 技术象限速查

### ADOPT (采用) - 28项

生产就绪、广泛采用的技术

**语言与框架:**

- Apache Flink 2.0+, Flink SQL/Table API, Java 21, Scala 2.13, Kafka Client 3.7+

**存储与数据:**

- Apache Kafka 3.7+, Apache Paimon 0.9+, Apache Iceberg 1.6+, RocksDB, PostgreSQL 16+

**基础设施:**

- Kubernetes 1.29+, Flink Kubernetes Operator 1.9+, Prometheus + Grafana, OpenTelemetry, Istio/Envoy

**工具与平台:**

- Debezium 2.7+, dbt 1.8+, Apache Airflow 2.9+, Schema Registry, DataHub

### TRIAL (试用) - 20项

有前景的技术，建议非核心场景试点

**语言与框架:**

- PyFlink 2.0+, Rust Native Streaming, RisingWave 2.0+, Timely Dataflow, Flink CDC 3.2+

**存储与数据:**

- Delta Lake 3.2+, Apache Hudi 0.15+, ForSt State Backend, Fluss

**基础设施:**

- Serverless Flink, eBPF, Cilium, GPUs for Inference, Confidential Computing

**工具与平台:**

- Temporal, Flink SQL Gateway, Great Expectations, Soda Core

### ASSESS (评估) - 20项

新兴技术，值得研究和POC验证

**语言与框架:**

- Flink + AI Agent (FLIP-531), Wasm UDF (WASI 0.3), Gleam, Kotlin Flow, Zig

**存储与数据:**

- Apache Ozone, Ceph, Tiered Storage, Vector DB (PGVector)

**基础设施:**

- WebAssembly Runtime (WASI 0.3), Unikernels, DPU/IPU, Quantum-safe Crypto

**工具与平台:**

- MCP Protocol, A2A Protocol, LangChain/LangGraph, DuckDB, Materialize

### HOLD (暂缓) - 12项

技术债务或替代方案更优

- Apache Storm, Samza, Flink Scala 2.11 (语言框架)
- HDFS, Cassandra老版本, Redis Cluster大规模, Elasticsearch 7.x (存储)
- YARN, Mesos, Docker Swarm (基础设施)
- Apache Nifi, Logstash (工具)

## 版本信息

- **当前版本:** v2026.2
- **发布时间:** 2026-04-04
- **更新周期:** 每月发布
- **下次更新:** 2026-05-15

## 使用建议

1. **技术选型**: 参考 [decision-tree.md](./decision-tree.md) 进行系统化评估
2. **风险评估**: 使用 [risk-assessment.md](./risk-assessment.md) 评估技术风险
3. **迁移规划**: 查阅 [migration-recommendations.md](./migration-recommendations.md) 获取迁移指导
4. **趋势跟踪**: 关注 [evolution-timeline.md](./evolution-timeline.md) 了解技术演进

## 贡献指南

欢迎通过以下方式贡献：

- 提交技术评估建议
- 报告过时技术信息
- 分享生产实践经验
- 改进可视化效果

请遵循项目 [CONTRIBUTING.md](../CONTRIBUTING.md) 规范。

---

*AnalysisDataFlow Project | 2026 Q2*
