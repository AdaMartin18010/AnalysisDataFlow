# CSP 学习资源

> **中级认证学习资料汇总**

## 核心理论文档

### Checkpoint 与状态

| 文档 | 难度 | 预计时间 | 重点 |
|------|------|----------|------|
| [Checkpoint 机制深度解析](../../../../Flink/02-core/checkpoint-mechanism-deep-dive.md) | ★★★★☆ | 2h | Barrier、对齐、增量 |
| [Exactly-Once 语义深度解析](../../../../Flink/02-core/exactly-once-semantics-deep-dive.md) | ★★★★☆ | 2h | 2PC、幂等性 |
| 状态后端配置指南 | ★★★☆☆ | 1h | RocksDB 调优 |
| Exactly-Once 形式化语义 | ★★★★★ | 2h | 形式化定义 |

### 运行时架构

| 文档 | 难度 | 预计时间 | 重点 |
|------|------|----------|------|
| 作业提交流程 | ★★★☆☆ | 1.5h | 图转换、调度 |
| 网络栈深度解析 | ★★★★☆ | 2h | Netty、信用值 |
| [背压与流控](../../../../Flink/02-core/backpressure-and-flow-control.md) | ★★★☆☆ | 1h | 背压传播 |

### 时间语义

| 文档 | 难度 | 预计时间 | 重点 |
|------|------|----------|------|
| [时间语义与 Watermark](../../../../Flink/02-core/time-semantics-and-watermark.md) | ★★★☆☆ | 1.5h | Watermark 生成 |
| [Watermark 单调性](../../../../Struct/02-properties/02.03-watermark-monotonicity.md) | ★★★★☆ | 1h | 形式化性质 |

## 工程实践文档

### 设计模式

- [Knowledge/02-design-patterns/](../../../../Knowledge/02-design-patterns/)
  - pattern-stateful-computation.md
  - pattern-exactly-once-sink.md
  - pattern-late-data-handling.md
  - pattern-broadcast-state.md
  - pattern-async-io.md

### 反模式

- [Knowledge/09-anti-patterns/](../../../../Knowledge/09-anti-patterns/)
  - anti-state-access-in-richfunction.md
  - anti-processfunction-timer-usage.md
  - anti-data-skew.md

### 案例研究

- Flink/07-case-studies/
  - case-fraud-detection.md
  - case-realtime-ml-feature.md

## 运维与调优

- [生产检查清单](../../../../Knowledge/production-checklist.md)
- [性能调优指南](../../../../Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md)
- 监控配置指南
- [部署架构指南](../../../../DEPLOYMENT-ARCHITECTURES.md)

## 推荐书籍

### 必读

1. **《Streaming Systems》** - Tyler Akidau et al.
   - 全书：流计算系统深度解析
   - 重点章节: 5-8章（时间、窗口、一致性）

2. **《Apache Flink实战》** - 崔星灿
   - 第 6-12 章：高级特性、运维调优

3. **《Designing Data-Intensive Applications》** - Martin Kleppmann
   - 第 11 章：流处理
   - 第 8-9 章：分布式系统一致性

### 进阶参考

1. **《The Dataflow Model》** - VLDB 2015 (Paper)
2. **《Apache Flink: Stream and Batch Processing in a Single Engine》** - IEEE 2015

## 实验环境

### K8s 实验平台

- 申请地址: <https://labs.analysisdataflow.org/csp>
- 包含: Flink Operator、Kafka、监控套件

### 本地 Docker 环境

```yaml
# 伪代码示意，非完整可执行配置
# docker-compose.yml 包含
version: '3'
services:
  flink-jobmanager:
    image: flink:1.18
    # ...
  flink-taskmanager:
    image: flink:1.18
    # ...
  kafka:
    image: confluentinc/cp-kafka:latest
    # ...
  mysql:
    image: mysql:8.0
    # ...
  prometheus:
    image: prom/prometheus
    # ...
  grafana:
    image: grafana/grafana
    # ...
```

## 练习题库

- [CSP 练习题库](../quizzes/README.md) - 500+ 题目
- [设计模式测验](../../../../tutorials/interactive/quizzes/design-patterns.md)
- [综合测试](../../../../tutorials/interactive/quizzes/comprehensive-test.md)

## 认证准备清单

### 知识检查

- [ ] 能详细解释 Checkpoint 完整流程
- [ ] 理解 Exactly-Once 实现原理
- [ ] 掌握三种状态后端的选型
- [ ] 能诊断和解决背压问题
- [ ] 熟练使用 SQL/Table API
- [ ] 掌握 CEP 模式定义
- [ ] 能部署 K8s 上的 Flink 集群
- [ ] 能进行性能调优

### 技能检查

- [ ] 能实现端到端 Exactly-Once
- [ ] 能处理数据倾斜
- [ ] 能设计合理的 Checkpoint 策略
- [ ] 能配置生产级监控系统

---

[返回课程大纲 →](../syllabus-csp.md)
