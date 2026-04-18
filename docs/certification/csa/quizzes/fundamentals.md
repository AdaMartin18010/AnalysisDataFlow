# CSA 基础概念练习题

> **章节**: 流计算基础概念 | **题目数**: 60 | **建议用时**: 45分钟

## 单选题 (40题)

### 批处理与流处理

**1. 以下哪项最准确地描述了批处理和流处理的主要区别？**

A. 批处理使用 Hadoop，流处理使用 Flink
B. 批处理处理有界数据，流处理处理无界数据
C. 批处理比流处理更快
D. 批处理只能处理结构化数据

<details>
<summary>答案与解析</summary>

**答案: B**

解析: 批处理和流处理的根本区别在于数据的有界性。批处理处理有限、有界的数据集，而流处理处理持续产生的无限数据流。选项A过于局限，C和D都不准确。
</details>

---

**2. 在流处理系统中，"低延迟"通常指的是？**

A. 数据存储延迟低
B. 从数据产生到结果被消费的时间短
C. 网络传输速度快
D. CPU 使用率低

<details>
<summary>答案与解析</summary>

**答案: B**

解析: 低延迟在流处理语境下指的是端到端的处理延迟，即数据从产生到结果可用的时间间隔。
</details>

---

**3. 以下哪个场景最适合使用流处理而非批处理？**

A. 月度财务报表生成
B. 实时欺诈检测
C. 年度数据归档
D. 历史数据批量迁移

<details>
<summary>答案与解析</summary>

**答案: B**

解析: 实时欺诈检测需要低延迟处理，必须在交易发生时立即做出判断，这是流处理的典型场景。其他三个场景对延迟要求不高，更适合批处理。
</details>

### 时间语义

**4. 在 Flink 中，Event Time 是指？**

A. 数据到达 Flink 的时间
B. 数据在 Flink 中被处理的时间
C. 数据产生时记录的时间戳
D. 数据写入外部系统的时间

<details>
<summary>答案与解析</summary>

**答案: C**

解析: Event Time 是事件实际发生的时间，即数据在源端产生时记录的时间戳。这是业务上最准确的时间语义。
</details>

---

**5. 当使用 Processing Time 进行窗口计算时，以下哪种情况可能导致结果不准确？**

A. 数据乱序到达
B. 系统负载变化
C. 网络延迟波动
D. 以上所有

<details>
<summary>答案与解析</summary>

**答案: D**

解析: Processing Time 以处理机器的时间为准，任何影响处理速度的因素（系统负载、网络延迟、数据乱序）都会导致结果不准确，无法反映真实的业务时间分布。
</details>

---

**6. 关于 Ingestion Time，以下说法正确的是？**

A. 它是数据产生的时间
B. 它是数据进入 Flink Source 的时间
C. 它比 Event Time 更准确
D. 它不需要 Watermark 机制

<details>
<summary>答案与解析</summary>

**答案: B**

解析: Ingestion Time 是数据进入 Flink 数据流的时间（即到达 Source 算子的时间）。它介于 Event Time 和 Processing Time 之间，既不需要依赖数据本身的时间戳，又相对 Processing Time 更稳定。
</details>

---

**7. 在处理乱序数据时，应该使用哪种时间语义？**

A. Processing Time
B. Ingestion Time
C. Event Time
D. 以上都可以

<details>
<summary>答案与解析</summary>

**答案: C**

解析: Event Time 配合 Watermark 机制可以正确处理乱序数据。Processing Time 和 Ingestion Time 都无法处理数据乱序问题。
</details>

### 窗口类型

**8. Tumbling Window 的特点是？**

A. 窗口之间可以重叠
B. 窗口之间无缝连接，不重叠
C. 窗口大小不固定
D. 窗口只在数据到达时创建

<details>
<summary>答案与解析</summary>

**答案: B**

解析: Tumbling Window（滚动窗口）将数据流分割成固定大小、不重叠的时间区间。每个数据只属于一个窗口。
</details>

---

**9. 需要计算每 5 分钟内的指标，且每分钟输出一次结果，应该使用？**

A. Tumbling Window of 5 minutes
B. Tumbling Window of 1 minute
C. Sliding Window with size 5 min and slide 1 min
D. Session Window

<details>
<summary>答案与解析</summary>

**答案: C**

解析: 这是典型的滑动窗口场景。Window size = 5 分钟（计算范围），slide = 1 分钟（输出频率）。滑动窗口允许窗口之间重叠。
</details>

---

**10. Session Window 适用于哪种场景？**

A. 固定时间段的统计
B. 用户行为分析，需要检测会话边界
C. 每分钟定时输出
D. 全量数据统计

<details>
<summary>答案与解析</summary>

**答案: B**

解析: Session Window（会话窗口）根据活动间隙动态划分窗口，非常适合分析用户会话行为，能够自动检测会话的开始和结束。
</details>

---

**11. Global Window 的触发条件是？**

A. 时间到达
B. 数据量达到阈值
C. 需要自定义触发器
D. 以上都是

<details>
<summary>答案与解析</summary>

**答案: C**

解析: Global Window 将所有数据放在一个窗口中，默认不会触发计算。必须配合自定义 Trigger 才能触发结果输出。
</details>

---

**12. 以下哪种窗口类型会根据数据动态调整窗口大小？**

A. Tumbling Window
B. Sliding Window
C. Session Window
D. Fixed Window

<details>
<summary>答案与解析</summary>

**答案: C**

解析: Session Window 的大小由数据本身决定，当在指定的 gap 时间内没有新数据到达时，窗口才会关闭。其他窗口的大小都是固定的。
</details>

## 多选题 (15题)

**13. 流处理系统相比批处理系统的优势包括？（选择所有适用的）**

A. 更低的处理延迟
B. 能够处理无限数据流
C. 更高的资源利用率
D. 更简单的编程模型
E. 实时响应能力

<details>
<summary>答案与解析</summary>

**答案: A, B, E**

解析: 流处理的核心优势是低延迟(A)、处理无界数据(B)和实时响应(E)。资源利用率(C)取决于具体实现，编程模型(D)通常比批处理更复杂。
</details>

---

**14. 以下哪些是 Event Time 处理乱序数据的常用机制？**

A. Watermark
B. Allowed Lateness
C. Side Output
D. Checkpoint
E. State Backend

<details>
<summary>答案与解析</summary>

**答案: A, B, C**

解析: Watermark 用于声明时间进度，Allowed Lateness 允许延迟数据参与计算，Side Output 用于收集延迟过长的数据。Checkpoint 和 State Backend 是容错机制，与乱序处理无关。
</details>

---

**15. 选择时间语义时需要考虑的因素包括？**

A. 数据是否包含时间戳
B. 对结果准确性的要求
C. 系统负载情况
D. 延迟要求
E. 数据是否可能乱序

<details>
<summary>答案与解析</summary>

**答案: A, B, D, E**

解析: 选择时间语义需要考虑：数据是否有时间戳(A)、准确性要求(B)、延迟要求(D)、数据是否乱序(E)。系统负载(C)影响性能但不直接决定时间语义选择。
</details>

---

**16. 以下关于窗口的说法正确的有？**

A. Tumbling Window 可以按时间或计数定义
B. Sliding Window 的 slide 必须小于 size
C. Session Window 需要指定 gap 时间
D. Global Window 通常需要自定义触发器
E. 所有窗口类型都支持 Event Time

<details>
<summary>答案与解析</summary>

**答案: A, C, D, E**

解析: Tumbling Window 支持时间和计数两种定义(A)。Session Window 必须指定 gap(C)。Global Window 默认不触发，需要自定义 Trigger(D)。所有窗口都支持三种时间语义(E)。Sliding Window 的 slide 可以等于 size（此时等同于 Tumbling Window），所以 B 错误。
</details>

## 判断题 (5题)

**17. Processing Time 窗口的结果在数据乱序时也是准确的。**

A. 正确  B. 错误

<details>
<summary>答案与解析</summary>

**答案: B（错误）**

解析: Processing Time 以机器处理时间为准，完全不受数据时间戳影响。数据乱序会导致处理顺序与事件发生顺序不一致，因此结果可能不准确。
</details>

---

**18. Watermark 机制只能与 Event Time 一起使用。**

A. 正确  B. 错误

<details>
<summary>答案与解析</summary>

**答案: A（正确）**

解析: Watermark 用于处理 Event Time 语义下的乱序问题，是 Event Time 特有的机制。Processing Time 和 Ingestion Time 不需要 Watermark。
</details>

---

**19. Session Window 的结束时间是在窗口创建时就确定的。**

A. 正确  B. 错误

<details>
<summary>答案与解析</summary>

**答案: B（错误）**

解析: Session Window 是动态窗口，其结束时间取决于数据到达情况。只有当 gap 时间内没有新数据到达时，窗口才会关闭。因此结束时间无法预先确定。
</details>

---

**20. 在 Flink 中，一个数据可以同时属于多个 Sliding Window。**

A. 正确  B. 错误

<details>
<summary>答案与解析</summary>

**答案: A（正确）**

解析: Sliding Window 允许重叠，因此一个数据点可能落入多个窗口。例如，窗口大小 10 分钟、滑动步长 5 分钟时，一个数据会同时属于当前窗口和下一个窗口。
</details>

---

*[共60题，此处展示前20题作为示例。完整题库包含：单选题40道、多选题15道、判断题5道]*

## 答案速查表

| 题号 | 答案 | 题号 | 答案 | 题号 | 答案 | 题号 | 答案 |
|------|------|------|------|------|------|------|------|
| 1 | B | 6 | B | 11 | C | 16 | ACDE |
| 2 | B | 7 | C | 12 | C | 17 | B |
| 3 | B | 8 | B | 13 | ABE | 18 | A |
| 4 | C | 9 | C | 14 | ABC | 19 | B |
| 5 | D | 10 | B | 15 | ABDE | 20 | A |

---

[返回题库首页 →](./README.md) | [下一章: Flink API →]
