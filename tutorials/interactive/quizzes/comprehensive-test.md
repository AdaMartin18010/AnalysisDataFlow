# 综合测试

> 所属阶段: 测验 | 前置依赖: 完成所有实验和测验 | 预计时间: 45分钟

## 说明

本测试综合考察流计算的理论知识和 Flink 实践能力。共 30 题，包括单选、多选和简答。

---

## 第一部分：单选题 (共15题，每题2分)

### 问题 1

**Flink 的流批统一核心是什么？**

- [ ] A. 统一的 SQL 引擎
- [ ] B. DataStream API 既可以处理有界流也可以处理无界流
- [ ] C. 统一的存储格式
- [ ] D. 统一的部署方式

<details>
<summary>答案</summary>

**答案：B**

Flink 通过 DataStream API 实现流批统一：无界数据流是流处理，有界数据流（如文件）可以当作批处理优化执行。
</details>

### 问题 2

**以下哪种 Window Assigner 会导致窗口重叠？**

- [ ] A. TumblingEventTimeWindows
- [ ] B. SlidingEventTimeWindows (slide < size)
- [ ] C. EventTimeSessionWindows
- [ ] D. GlobalWindows

<details>
<summary>答案</summary>

**答案：B**

Sliding Window 当滑动间隔小于窗口大小时，窗口会重叠，一个事件可能属于多个窗口。
</details>

### 问题 3

**Flink Checkpoint 的 barriers 是？**

- [ ] A. 网络屏障
- [ ] B. 数据流中的特殊记录，标记快照边界
- [ ] C. 内存屏障
- [ ] D. 安全屏障

<details>
<summary>答案</summary>

**答案：B**

Barriers 是 Flink Checkpoint 机制的核心，周期性地插入数据流，作为快照边界，确保一致性快照。
</details>

### 问题 4

**在 Flink SQL 中，`EMIT WITH DELAY '1' MINUTE` 表示？**

- [ ] A. 延迟读取数据
- [ ] B. 延迟输出结果，允许更多迟到数据
- [ ] C. 延迟启动作业
- [ ] D. 延迟 Checkpoint

<details>
<summary>答案</summary>

**答案：B**

EMIT WITH DELAY 允许窗口触发后继续等待一段时间，收集更多迟到数据，提高结果准确性。
</details>

### 问题 5

**Flink 中 `keyBy()` 后以下哪个操作是合法的？**

- [ ] A. `map()`
- [ ] B. `filter()`
- [ ] C. `window()` 或 `process()`
- [ ] D. 以上所有

<details>
<summary>答案</summary>

**答案：D**

keyBy() 后可以使用任何转换操作，包括 map、filter、window、process 等。KeyedStream 继承自 DataStream。
</details>

### 问题 6

**RocksDB StateBackend 的增量 Checkpoint 是指？**

- [ ] A. 只保存新增的状态
- [ ] B. 只保存相对于上次 Checkpoint 发生变化的状态
- [ ] C. 减少 Checkpoint 频率
- [ ] D. 减少状态大小

<details>
<summary>答案</summary>

**答案：B**

增量 Checkpoint 只保存 SST 文件的变化部分，减少 Checkpoint 时间和存储空间，适合大状态场景。
</details>

### 问题 7

**Flink CEP 中的 `followedBy()` 与 `next()` 的区别是？**

- [ ] A. 没有区别
- [ ] B. `followedBy()` 允许中间有其他事件，`next()` 不允许
- [ ] C. `next()` 允许中间有其他事件
- [ ] D. 时间约束不同

<details>
<summary>答案</summary>

**答案：B**

`next()` 要求事件严格连续，`followedBy()` 允许中间有其他事件（宽松连续）。

**参考**: [Lab 6: CEP 模式匹配](../hands-on-labs/lab-06-cep.md)
</details>

### 问题 8

**在流处理系统中，以下哪种情况最适合使用 Processing Time？**

- [ ] A. 需要精确结果的历史数据分析
- [ ] B. 对延迟敏感、可以容忍近似结果的实时监控
- [ ] C. 金融交易对账
- [ ] D. 日志回放分析

<details>
<summary>答案</summary>

**答案：B**

Processing Time 提供最低延迟，适合实时监控等场景。需要精确结果的场景应该使用 Event Time。
</details>

### 问题 9

**Flink 的 Side Output 主要用于？**

- [ ] A. 提高吞吐量
- [ ] B. 分流处理，如分离迟到数据
- [ ] C. 减少延迟
- [ ] D. 状态管理

<details>
<summary>答案</summary>

**答案：B**

Side Output 允许将数据分流到旁路输出，常用于处理迟到数据、异常数据分离等场景。
</details>

### 问题 10

**以下哪个不是 Flink 支持的 Restart Strategy？**

- [ ] A. fixed-delay
- [ ] B. failure-rate
- [ ] C. exponential-delay
- [ ] D. checkpoint-restart

<details>
<summary>答案</summary>

**答案：D**

Flink 支持 fixed-delay、failure-rate、exponential-delay 和 no-restart，没有 checkpoint-restart 策略。
</details>

### 问题 11

**在 Flink 中，AsyncFunction 的主要作用是？**

- [ ] A. 同步处理数据
- [ ] B. 异步访问外部系统，提高吞吐量
- [ ] C. 并行处理
- [ ] D. 状态管理

<details>
<summary>答案</summary>

**答案：B**

AsyncFunction 支持异步 IO，在等待外部系统响应时不阻塞数据流，显著提高与外部系统交互的吞吐量。
</details>

### 问题 12

**Flink SQL 的 `TUMBLE` 窗口与 `HOP` 窗口的主要区别是？**

- [ ] A. 时间精度不同
- [ ] B. TUMBLE 窗口不重叠，HOP 窗口可以重叠
- [ ] C. HOP 只能用于批处理
- [ ] D. TUMBLE 只能用于流处理

<details>
<summary>答案</summary>

**答案：B**

TUMBLE（滚动）窗口之间不重叠；HOP（滑动）窗口有滑动步长，可以重叠。
</details>

### 问题 13

**在分布式流处理中，Backpressure 是指？**

- [ ] A. 网络压力
- [ ] B. 下游向上游传递的处理压力信号
- [ ] C. 存储压力
- [ ] D. CPU 压力

<details>
<summary>答案</summary>

**答案：B**

Backpressure 是流系统的流量控制机制，当下游处理不过来时向上游传递压力信号，减慢数据产生速度。
</details>

### 问题 14

**Flink 的 Broadcast State 主要用于？**

- [ ] A. 广播数据到所有 Task
- [ ] B. 小量配置数据广播给所有 subtask，与数据流连接
- [ ] C. 提高并行度
- [ ] D. 状态备份

<details>
<summary>答案</summary>

**答案：B**

Broadcast State 用于将小量配置/规则数据广播到所有并行实例，与主流数据连接处理（如动态规则更新）。
</details>

### 问题 15

**以下哪种 Sink 连接器实现 Exactly-Once 最复杂？**

- [ ] A. Print Sink
- [ ] B. Kafka Sink (with transactions)
- [ ] C. Socket Sink
- [ ] D. Collection Sink

<details>
<summary>答案</summary>

**答案：B**

Kafka Sink 使用事务实现 Exactly-Once 最复杂，需要协调两阶段提交、事务超时管理等。
</details>

---

## 第二部分：多选题 (共5题，每题4分，漏选得2分，错选不得分)

### 问题 16

**Flink 中实现 Exactly-Once 语义需要哪些条件？**

- [ ] A. 可重放的数据源（如 Kafka）
- [ ] B. 定期 Checkpoint 保存状态
- [ ] C. 事务性或幂等性 Sink
- [ ] D. 增加并行度

<details>
<summary>答案</summary>

**答案：A, B, C**

Exactly-Once 需要：可重放数据源（故障后重新消费）、Checkpoint（保存处理状态）、事务/幂等 Sink（保证输出不重复）。并行度与 Exactly-Once 无关。
</details>

### 问题 17

**以下哪些是 Flink 支持的 State 类型？**

- [ ] A. ValueState
- [ ] B. ListState
- [ ] C. MapState
- [ ] D. ReducingState

<details>
<summary>答案</summary>

**答案：A, B, C, D**

Flink 支持 ValueState、ListState、MapState、ReducingState 和 AggregatingState 等Keyed State 类型。

**参考**: [Lab 4: 状态管理](../hands-on-labs/lab-04-state-management.md)
</details>

### 问题 18

**Watermark 生成策略包括？**

- [ ] A. forMonotonousTimestamps
- [ ] B. forBoundedOutOfOrderness
- [ ] C. forAscendingTimestamps
- [ ] D. 自定义 WatermarkGenerator

<details>
<summary>答案</summary>

**答案：A, B, D**

Flink 提供 forMonotonousTimestamps（无乱序）、forBoundedOutOfOrderness（固定延迟）以及自定义 WatermarkGenerator。forAscendingTimestamps 不是标准 API。
</details>

### 问题 19

**以下哪些是 Flink 部署模式？**

- [ ] A. Local
- [ ] B. Standalone Cluster
- [ ] C. YARN
- [ ] D. Kubernetes

<details>
<summary>答案</summary>

**答案：A, B, C, D**

Flink 支持 Local（本地）、Standalone（独立集群）、YARN 和 Kubernetes 多种部署模式。
</details>

### 问题 20

**CEP 模式中的量词包括？**

- [ ] A. times(n)
- [ ] B. oneOrMore()
- [ ] C. optional()
- [ ] D. timesOrMore(n)

<details>
<summary>答案</summary>

**答案：A, B, C, D**

Flink CEP 支持 times(n)（精确n次）、oneOrMore()（一次或多次）、optional()（可选）、timesOrMore(n)（至少n次）等量词。

**参考**: [Lab 6: CEP 模式匹配](../hands-on-labs/lab-06-cep.md)
</details>

---

## 第三部分：简答题 (共5题，每题6分)

### 问题 21

**描述 Flink Checkpoint 的完整流程，以及它是如何保证 Exactly-Once 语义的。**

<details>
<summary>参考答案</summary>

**Checkpoint 流程：**

1. Checkpoint Coordinator 周期性向所有 Source 发送 barrier
2. Source 收到 barrier 后保存自己的状态，向下游广播 barrier
3. 算子收到所有输入流的 barrier 后，保存当前状态，向下游转发 barrier
4. 当所有算子确认状态保存完成，Checkpoint Coordinator 收到确认
5. Checkpoint 完成，通知所有算子

**Exactly-Once 保证：**

- 故障时从最新 Checkpoint 恢复状态
- 数据源从 Checkpoint 记录的 offset 重新消费
- 确保每条数据在故障恢复后的效果等价于恰好处理一次

</details>

### 问题 22

**比较 Tumbling Window、Sliding Window 和 Session Window 的适用场景。**

<details>
<summary>参考答案</summary>

| 窗口类型 | 特点 | 适用场景 |
|---------|------|---------|
| Tumbling | 固定大小，不重叠 | 固定周期统计，如每分钟PV |
| Sliding | 滑动步长，可重叠 | 移动平均，如最近5分钟每10秒统计 |
| Session | 动态大小，活动间隙触发 | 用户行为分析，如会话时长 |

**选择原则：**

- 固定时间周期用 Tumbling
- 需要平滑趋势用 Sliding
- 用户/会话驱动用 Session

</details>

### 问题 23

**解释 Event Time 和 Processing Time 的区别，以及在什么情况下应该使用哪种时间语义。**

<details>
<summary>参考答案</summary>

**区别：**

- Event Time：事件实际发生时间，嵌入数据本身
- Processing Time：数据被处理时的机器时间

**选择依据：**

- **Event Time**：需要精确、可重现的结果，能处理乱序数据
  - 适用：金融交易、日志分析、报表统计
- **Processing Time**：低延迟优先，可容忍近似结果
  - 适用：实时监控、告警系统、近似计算

</details>

### 问题 24

**描述如何使用 Flink CEP 检测"用户在短时间内连续多次登录失败"的安全事件。**

<details>
<summary>参考答案</summary>

```java

// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
import org.apache.flink.streaming.api.windowing.time.Time;

Pattern<LoginEvent, ?> pattern = Pattern
    .<LoginEvent>begin("fail")
    .where(e -> e.status.equals("FAIL"))
    .timesOrMore(3)  // 3次或更多
    .within(Time.minutes(5));  // 5分钟内

CEP.pattern(stream.keyBy(LoginEvent::getUserId), pattern)
    .process(new PatternProcessFunction<LoginEvent, Alert>() {
        @Override
        public void processMatch(Map<String, List<LoginEvent>> match,
                                Context ctx, Collector<Alert> out) {
            List<LoginEvent> fails = match.get("fail");
            out.collect(new Alert(
                fails.get(0).userId,
                "BRUTE_FORCE_ATTACK",
                fails.size() + " failed logins"
            ));
        }
    });
```

</details>

### 问题 25

**解释 Backpressure 机制，以及如何在 Flink 中监控和处理反压。**

<details>
<summary>参考答案</summary>

**Backpressure 机制：**

- 当下游 Task 处理速度 < 上游发送速度时，数据在缓冲区堆积
- 当缓冲区满，下游停止读取，上游网络发送阻塞
- 反压信号向上游传播，直到数据源减慢发送

**监控：**

- Flink Web UI 中的 Backpressure 标签页
- 颜色标识：OK/Low/High（绿色/黄色/红色）
- Task Metrics: `backPressuredTimeMsPerSecond`

**处理：**

- 优化慢速算子（代码优化、并行度调整）
- 增加资源（CPU/内存）
- 减少数据量（过滤、采样）
- 异步化阻塞操作（AsyncFunction）

</details>

---

## 成绩统计

| 部分 | 题数 | 分值 | 得分 |
|------|------|------|------|
| 单选题 | 15 | 30 | ___ |
| 多选题 | 5 | 20 | ___ |
| 简答题 | 5 | 30 | ___ |
| **总计** | **25** | **80** | **___** |

### 评分标准

- 70-80 分：优秀，完全掌握流处理和 Flink
- 60-69 分：良好，能够独立完成大部分开发任务
- 45-59 分：及格，需要继续加强实践
- <45 分：建议重新学习理论和实验

## 完成证书

完成本测试后，您已获得：

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║           AnalysisDataFlow 流计算学习认证                     ║
║                                                               ║
║    完成者: ______________________                             ║
║    完成日期: ___________________                              ║
║    综合测试得分: _______________                              ║
║                                                               ║
║    已掌握技能:                                                ║
║    □ Flink DataStream API                                    ║
║    □ Event Time 与 Watermark                                 ║
║    □ Window 聚合操作                                          ║
║    □ 状态管理                                                 ║
║    □ Checkpoint 与 Exactly-Once                              ║
║    □ CEP 模式匹配                                             ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

## 下一步

- [编程挑战](../coding-challenges/README.md) - 实战练习
- [Flink Playground](../flink-playground/README.md) - 自由实验
