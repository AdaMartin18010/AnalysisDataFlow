# TECH-STACK: 流计算 × PostgreSQL 18 × Temporal × Kratos × Docker

> **状态**: ✅ 已完成 | **风险等级**: 中 | **最后更新**: 2026-04-22
>
> 此技术栈梳理已 100% 完成。PostgreSQL 18 于 2025-09-25 正式发布，Temporal/Kratos 持续演进中。

## 技术栈定位

本目录系统梳理 **流计算 (Apache Flink/Kafka) × PostgreSQL 18 × Temporal × Kratos × Docker/K8s** 五技术组合的：

1. **系统性组合架构**（System Composition）— 数据流、控制流、耦合矩阵
2. **组件深度解析**（Component Deep Dive）— 各组件独立架构与机制
3. **跨组件集成模式**（Integration Patterns）— Outbox/Saga/CQRS/Aggregator
4. **组合弹性论证**（Compositional Resilience）— 故障传播、容错证明、混沌工程
5. **部署与生产实践**（Deployment & Practice）— Docker/K8s/性能基准

## 目录结构

```
TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/
├── 00-meta/                    # 元数据、索引、术语表
├── 01-system-composition/      # 系统性组合架构（核心）
│   ├── 01.01-composite-architecture-overview.md
│   ├── 01.02-data-flow-control-flow-analysis.md
│   ├── 01.03-dependency-coupling-matrix.md
│   └── 01.04-aggregation-patterns.md
├── 02-component-deep-dive/     # 各组件独立架构深度解析
│   ├── 02.01-postgresql-18-cdc-deep-dive.md
│   ├── 02.02-temporal-workflow-engine-guide.md
│   ├── 02.03-kratos-microservices-framework.md
│   ├── 02.04-flink-streaming-resilience.md
│   └── 02.05-docker-kubernetes-deployment-base.md
├── 03-integration/             # 跨组件集成模式与最佳实践
│   ├── 03.01-pg18-cdc-kafka-flink-pipeline.md
│   ├── 03.02-temporal-kratos-worker-integration.md
│   ├── 03.03-outbox-pattern-pg18-kratos.md
│   ├── 03.04-saga-pattern-temporal-kratos.md
│   └── 03.05-cqrs-streaming-read-model.md
├── 04-resilience/              # 组合弹性分析论证（核心）
│   ├── 04.01-resilience-evaluation-framework.md
│   ├── 04.02-circuit-breaker-backpressure-analysis.md
│   ├── 04.03-bulkhead-retry-isolation-patterns.md
│   ├── 04.04-fault-tolerance-composition-proof.md
│   └── 04.05-chaos-engineering-practice.md
├── 05-deployment/              # Docker / K8s / Helm 部署
├── 06-practice/                # 端到端案例与性能调优
└── 07-frontier/                # 前沿趋势与版本跟踪
```

## PostgreSQL 18 核心特性速览（权威来源）

> 来源: [PostgreSQL 18 Release Notes](https://www.postgresql.org/docs/release/18.0/) (2025-09-25)

| 特性 | 说明 | 与流计算关联 |
|------|------|-------------|
| **异步 I/O (AIO)** | `io_uring` 非阻塞读取，存储扫描性能提升最高 3 倍 | CDC 读取 WAL 更高效 |
| **UUIDv7** | 时间排序 UUID，改善 B-tree 索引局部性 | 事件表主键，减少索引分裂 |
| **虚拟生成列** | 默认虚拟列，查询时计算，不占用存储 | 派生事件字段，简化 schema |
| **B-Tree Skip Scan** | 多列索引跳过前导列也能使用 | 复合查询优化 |
| **逻辑复制增强** | 并行流、冲突报告、生成列复制 | Debezium/Flink CDC 更可靠 |
| **Temporal WITHOUT OVERLAPS** | 时态表约束原生支持 | 与 Temporal 工作流引擎语义呼应 |
| **RETURNING OLD/NEW** | 单语句获取更新前后值 | CDC 事件 enrich 简化 |
| **并行 COPY** | 批量加载并行化 | 初始 snapshot 加速 |

## 文档清单与快速导航

| 编号 | 文档 | 主题 | 规模 |
|------|------|------|------|
| **C1** | [01.01-composite-architecture-overview.md](../01-system-composition/01.01-composite-architecture-overview.md) | 五技术组合架构总览 | ~27KB |
| **C2** | [01.02-data-flow-control-flow-analysis.md](../01-system-composition/01.02-data-flow-control-flow-analysis.md) | 数据流与控制流分析 | ~21KB |
| **C3** | [01.03-dependency-coupling-matrix.md](../01-system-composition/01.03-dependency-coupling-matrix.md) | 依赖耦合矩阵 | ~35KB |
| **C4** | [01.04-aggregation-patterns.md](../01-system-composition/01.04-aggregation-patterns.md) | 聚合模式 | ~38KB |
| **D1** | [02.01-postgresql-18-cdc-deep-dive.md](../02-component-deep-dive/02.01-postgresql-18-cdc-deep-dive.md) | PG18 CDC 深度解析 | ~23KB |
| **D2** | [02.02-temporal-workflow-engine-guide.md](../02-component-deep-dive/02.02-temporal-workflow-engine-guide.md) | Temporal 工作流引擎 | ~29KB |
| **D3** | [02.03-kratos-microservices-framework.md](../02-component-deep-dive/02.03-kratos-microservices-framework.md) | Kratos 微服务框架 | ~24KB |
| **D4** | [02.04-flink-streaming-resilience.md](../02-component-deep-dive/02.04-flink-streaming-resilience.md) | Flink 流处理弹性 | ~17KB |
| **D5** | [02.05-docker-kubernetes-deployment-base.md](../02-component-deep-dive/02.05-docker-kubernetes-deployment-base.md) | Docker/K8s 部署底座 | ~29KB |
| **I1** | [03.01-pg18-cdc-kafka-flink-pipeline.md](../03-integration/03.01-pg18-cdc-kafka-flink-pipeline.md) | CDC-Kafka-Flink 管道 | ~15KB |
| **I2** | [03.02-temporal-kratos-worker-integration.md](../03-integration/03.02-temporal-kratos-worker-integration.md) | Temporal-Kratos Worker | ~12KB |
| **I3** | [03.03-outbox-pattern-pg18-kratos.md](../03-integration/03.03-outbox-pattern-pg18-kratos.md) | Outbox 模式 | ~12KB |
| **I4** | [03.04-saga-pattern-temporal-kratos.md](../03-integration/03.04-saga-pattern-temporal-kratos.md) | Saga 分布式事务 | ~45KB |
| **I5** | [03.05-cqrs-streaming-read-model.md](../03-integration/03.05-cqrs-streaming-read-model.md) | CQRS 流式读模型 | ~12KB |
| **R1** | [04.01-resilience-evaluation-framework.md](../04-resilience/04.01-resilience-evaluation-framework.md) | 弹性评价框架 | ~27KB |
| **R2** | [04.02-circuit-breaker-backpressure-analysis.md](../04-resilience/04.02-circuit-breaker-backpressure-analysis.md) | 断路器与背压分析 | ~16KB |
| **R3** | [04.03-bulkhead-retry-isolation-patterns.md](../04-resilience/04.03-bulkhead-retry-isolation-patterns.md) | 舱壁隔离与重试 | ~14KB |
| **R4** | [04.04-fault-tolerance-composition-proof.md](../04-resilience/04.04-fault-tolerance-composition-proof.md) | 组合容错形式化证明 | ~29KB |
| **R5** | [04.05-chaos-engineering-practice.md](../04-resilience/04.05-chaos-engineering-practice.md) | 混沌工程实践 | ~14KB |
| **P1** | [05.01-docker-compose-fullstack.md](../05-deployment/05.01-docker-compose-fullstack.md) | Docker Compose 全栈 | ~23KB |
| **P2** | [05.02-kubernetes-helm-deployment.md](../05-deployment/05.02-kubernetes-helm-deployment.md) | K8s Helm 部署 | ~29KB |
| **P3** | [05.03-production-checklist.md](../05-deployment/05.03-production-checklist.md) | 生产检查清单 | ~25KB |
| **P4** | [06.01-end-to-end-order-processing-example.md](../06-practice/06.01-end-to-end-order-processing-example.md) | 端到端订单处理案例 | ~40KB |
| **P5** | [06.02-performance-benchmark-guide.md](../06-practice/06.02-performance-benchmark-guide.md) | 性能基准测试 | ~22KB |
| **P6** | [07.01-pg19-roadmap-ai-streaming.md](../07-frontier/07.01-pg19-roadmap-ai-streaming.md) | PG19 前瞻与 AI 流处理 | ~17KB |

## 质量门禁状态

| 检查项 | 状态 |
|--------|------|
| 六段式模板 | ✅ 25/25 (100%) |
| 内部交叉引用 | ✅ 0 broken links |
| Mermaid 语法 | ✅ 48/48 (100%) |
| 形式化元素唯一性 | ✅ 115 个，无冲突 |
| 引用格式 [^n] | ✅ 95+ 条 |

## 弹性架构权威框架引用

> 来源: arXiv 2512.16959v1 (2025-12), *Resilient Microservices: A Systematic Review of Recovery Patterns*

本技术栈弹性论证基于该 PRISMA 对齐系统文献综述，涵盖：

- **Recovery Pattern Taxonomy** — 故障类型→恢复策略映射
- **Resilience Evaluation Score (RES)** — 标准化弹性评估清单
- **Resilience Maturity Model (RML)** — 五级成熟度模型（Ad-hoc → Optimized）
- **九大运维主题 (T1-T9)** — 断路器、Saga、重试、舱壁、背压、混沌测试等
