# CSP 练习题库

> **版本**: v1.0 | **题目总数**: 500+ | **难度**: ★★★☆☆

## 题库结构

```
quizzes/
├── README.md                    # 本文件
├── runtime-architecture.md      # 运行时架构 (60题)
├── checkpoint-state.md          # Checkpoint与状态 (80题)
├── exactly-once.md              # Exactly-Once语义 (60题)
├── time-watermark.md            # 时间语义高级 (50题)
├── state-management.md          # 状态管理高级 (50题)
├── table-api-sql.md             # Table API与SQL (60题)
├── cep.md                       # CEP复杂事件 (40题)
├── deployment-ops.md            # 部署与运维 (50题)
├── performance-tuning.md        # 性能调优 (50题)
└── mock-exams/                  # 模拟考试
    ├── mock-01.md
    ├── mock-02.md
    └── mock-03.md
```

## 快速导航

| 章节 | 题目数 | 难度 | 考点 |
|------|--------|------|------|
| [运行时架构](./runtime-architecture.md) | 60 | ★★★☆☆ | JobGraph、调度、网络栈 |
| [Checkpoint与状态](./checkpoint-state.md) | 80 | ★★★★☆ | Barrier、状态后端、增量 |
| [Exactly-Once](./exactly-once.md) | 60 | ★★★★☆ | 2PC、幂等性、事务 |
| [时间语义高级](./time-watermark.md) | 50 | ★★★☆☆ | Watermark策略、延迟处理 |
| [状态管理高级](./state-management.md) | 50 | ★★★★☆ | 大状态优化、Broadcast |
| [Table API/SQL](./table-api-sql.md) | 60 | ★★★☆☆ | SQL优化、CDC |
| [CEP](./cep.md) | 40 | ★★★★☆ | 模式匹配、超时处理 |
| [部署运维](./deployment-ops.md) | 50 | ★★★☆☆ | K8s部署、监控告警 |
| [性能调优](./performance-tuning.md) | 50 | ★★★★☆ | 背压、数据倾斜、GC |

## 备考建议

### 阶段一：模块学习期

每个模块学习完成后，完成对应章节练习题：

- 目标正确率: 70%+
- 错题记录到错题本
- 理解解析而非死记答案

### 阶段二：专项突破期

针对薄弱环节进行专项练习：

- 使用错题本复习
- 重新做错误题目直到全对
- 重点关注概念辨析题

### 阶段三：模拟考试期

完成 3 套模拟考试：

- 模拟真实考试环境（3小时限时）
- 目标分数: 80+
- 分析失分点，查漏补缺

## 题目难度标识

| 标识 | 难度 | 说明 |
|------|------|------|
| ★☆☆☆☆ | 基础 | 直接概念题 |
| ★★☆☆☆ | 简单 | 简单应用 |
| ★★★☆☆ | 中等 | 需要理解 |
| ★★★★☆ | 困难 | 综合应用 |
| ★★★★★ | 专家 | 深度分析 |

## 样题示例

### 单选题

**【Checkpoint】★★★★☆**

在 Flink 中，Unaligned Checkpoint 的主要优势是什么？

A. 减少状态存储大小
B. 降低 Checkpoint 对业务延迟的影响
C. 提高状态恢复速度
D. 支持更大规模的状态

<details>
<summary>答案与解析</summary>

**答案: B**

解析: Unaligned Checkpoint 不需要等待 Barrier 对齐，可以在数据流中快速传播 Barrier，从而减少对业务处理延迟的影响（尤其是在反压场景下）。它不直接减少存储大小或提高恢复速度。
</details>

### 多选题

**【Exactly-Once】★★★★☆**

实现端到端 Exactly-Once 输出到 Kafka，需要满足哪些条件？

A. Flink 启用 Checkpoint
B. Kafka Producer 配置事务 ID
C. Sink 实现 TwoPhaseCommitSinkFunction
D. Kafka 版本 >= 0.11
E. Checkpoint 间隔小于事务超时时间

<details>
<summary>答案与解析</summary>

**答案: A, B, C, D, E**

解析: 实现端到端 Exactly-Once 需要：

- Flink Checkpoint 保证内部状态一致性(A)
- Kafka 事务支持(B, D)
- 两阶段提交协议(C)
- 事务必须在超时前完成提交(E)

</details>

### 简答题

**【性能调优】★★★★★**

某 Flink 作业出现严重数据倾斜，导致部分 Task 处理缓慢。请列举至少 3 种诊断方法和 3 种解决方案。

<details>
<summary>参考答案</summary>

**诊断方法**:

1. 查看 Web UI SubTask 指标，观察记录数/字节数分布
2. 检查火焰图，定位热点方法
3. 分析 keyBy 字段分布，统计各 key 出现频率

**解决方案**:

1. 两阶段聚合：先局部预聚合，再全局聚合
2. Key 加盐：为热点 key 添加随机前缀分散处理
3. 自定义分区器：根据数据特征优化分区策略

</details>

## 学习资源

- [课程大纲](../syllabus-csp.md) - 对应模块学习
- [实验指导](../labs/) - 动手实践
- [Flink 官方文档](https://nightlies.apache.org/flink/) - 权威参考

---

[返回课程大纲 →](../syllabus-csp.md) | [开始练习: 运行时架构 →](./runtime-architecture.md)
