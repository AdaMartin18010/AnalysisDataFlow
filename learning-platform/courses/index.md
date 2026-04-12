# 课程目录

## 概述

本学习平台提供三门系统化课程，涵盖 Apache Flink 从入门到精通的完整知识体系。

---

## 课程列表

### 课程1: Flink基础速成 (5节课)

| 课节 | 标题 | 时长 | 关键概念 |
|------|------|------|----------|
| 1.1 | Flink简介与安装 | 30min | 架构概览、环境搭建 |
| 1.2 | DataStream API基础 | 40min | Source、Transformation、Sink |
| 1.3 | 第一个流处理应用 | 35min | WordCount、执行模式 |
| 1.4 | 时间与Watermark | 45min | Event Time、Processing Time |
| 1.5 | 基础窗口操作 | 40min | Tumbling、Sliding Window |

**前置要求**: Java/Scala 基础、基础分布式概念

---

### 课程2: 流处理设计模式 (4节课)

| 课节 | 标题 | 时长 | 关键概念 |
|------|------|------|----------|
| 2.1 | 窗口高级特性 | 50min | Session Window、Custom Trigger |
| 2.2 | 状态管理基础 | 55min | Keyed State、Operator State |
| 2.3 | 复杂事件处理(CEP) | 60min | Pattern API、时间约束 |
| 2.4 | 连接器与集成 | 45min | Kafka、JDBC、File System |

**前置要求**: 完成课程1

---

### 课程3: 高级主题与调优 (4节课)

| 课节 | 标题 | 时长 | 关键概念 |
|------|------|------|----------|
| 3.1 | Checkpoint与容错 | 60min | Barrier、Exactly-Once |
| 3.2 | 背压与流量控制 | 50min | Credit-based Flow Control |
| 3.3 | 性能调优实践 | 55min | 并行度、状态后端选型 |
| 3.4 | 生产环境部署 | 45min | HA配置、监控告警 |

**前置要求**: 完成课程2

---

## 学习建议

1. **循序渐进**: 按顺序完成课程，不要跳过基础
2. **动手实践**: 每节课后完成配套练习
3. **交互实验**: 结合实验加深理解
4. **编程挑战**: 通过挑战检验学习成果

---

## 参考文档

- [Flink 官方文档](https://nightlies.apache.org/flink/flink-docs-stable/)
- [项目 Struct 目录](../../Struct/)
- [项目 Knowledge 目录](../../Knowledge/)
- [项目 Flink 目录](../../Flink/)
