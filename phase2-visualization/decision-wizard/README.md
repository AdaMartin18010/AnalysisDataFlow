# 决策向导 (Decision Wizard)

> **模块**: Phase 2 - 可视化平台 - 模块3
> **功能**: 交互式技术选型决策工具
> **状态**: 初稿

---

## 功能概述

决策向导帮助用户根据业务场景选择合适的技术方案：

1. **流处理框架选择** - Flink vs Spark Streaming vs Kafka Streams
2. **状态后端选择** - RocksDB vs Heap vs FsStateBackend
3. **部署模式选择** - Standalone vs YARN vs Kubernetes
4. **窗口类型选择** - Tumbling vs Sliding vs Session vs Global

---

## 决策流程

```mermaid
flowchart TD
    Start([开始]) --> Q1{数据延迟要求?}
    Q1 -->|秒级| Q2{数据规模?}
    Q1 -->|分钟级| Q3{已有生态?}

    Q2 -->|TB级/天| A1[Flink]
    Q2 -->|PB级/天| A1
    Q2 -->|GB级/天| A2[Kafka Streams]

    Q3 -->|Spark生态| A3[Spark Streaming]
    Q3 -->|Kafka生态| A2
    Q3 -->|无偏好| A1

    A1 --> Q4{状态大小?}
    A2 --> Q5{部署环境?}
    A3 --> Q3

    Q4 -->|大状态| B1[RocksDB StateBackend]
    Q4 -->|小状态| B2[Heap StateBackend]
    Q4 -->|仅恢复| B3[FsStateBackend]

    Q5 -->|容器化| C1[Kubernetes]
    Q5 -->|Hadoop| C2[YARN]
    Q5 -->|独立部署| C3[Standalone]

    B1 --> End([完成])
    B2 --> End
    B3 --> End
    C1 --> End
    C2 --> End
    C3 --> End
```

---

## 实现计划

### Phase 1: 基础框架

- [ ] 决策树数据结构定义
- [ ] 基础UI组件
- [ ] 结果展示页面

### Phase 2: 内容填充

- [ ] 流处理框架决策树
- [ ] 状态后端决策树
- [ ] 部署模式决策树

### Phase 3: 增强功能

- [ ] 用户历史记录
- [ ] 推荐解释说明
- [ ] 导出决策报告

---

*Phase 2 - 任务线4-3: 决策向导设计*
