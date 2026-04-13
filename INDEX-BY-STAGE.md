> **状态**: 🔮 前瞻内容 | **风险等级**: 高 | **最后更新**: 2026-04
>
> 此文档描述的内容处于早期规划阶段，可能与最终实现不符。请以 Apache Flink 官方发布为准。
>
# AnalysisDataFlow 形式化元素索引 (按层级分类)

> **版本**: v1.0.0 | **生成日期**: 2026-04-11 | **总计**: 2,667 个形式化元素

---

## 目录

- [Struct 层级 (形式理论) - 498个](#struct-层级)
- [Knowledge 层级 (知识结构) - 732个](#knowledge-层级)
- [Flink 层级 (Flink专项) - 1437个](#flink-层级)

## Struct 层级 (形式理论)

总计: 498 个形式化元素

### 按类型统计

| 类型 | 数量 |
|------|------|
| 定理 | 133 |
| 定义 | 205 |
| 引理 | 104 |
| 命题 | 39 |
| 推论 | 17 |

### 完整列表

| 编号 | 名称 | 类型 | 位置 |
|------|------|------|------|
| Thm-S-01-01 | USTM组合性定理 | 定理 |  |
| Thm-S-01-02 | 表达能力层次判定 | 定理 |  |
| Thm-S-01-03 | 会话类型安全性 (Type Safety) | 定理 |  |
| Thm-S-01-04 | 会话类型无死锁性 (Deadlock Freedom) | 定理 |  |
| Thm-S-01-05 | 协议合规性 (Protocol Compliance) | 定理 |  |
| Thm-S-01-12 | IMPACT-REPORT.md | 定理 |  |
| Thm-S-01-30 | 流处理的进程等价性 | 定理 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Thm-S-01-31 | 流处理与Dataflow模型的对应 | 定理 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Thm-S-01-32 | Actor与流处理的语义对应 | 定理 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Thm-S-01-33 | 一致性层级包含关系 | 定理 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Thm-S-01-34 | 流处理系统的CAP权衡 | 定理 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Thm-S-01-35 | 恰好一次语义的充要条件 | 定理 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Thm-S-01-36 | Watermark完整性定理 | 定理 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Thm-S-01-80 | (流数据库一致性等价定理) | 定理 | Struct/01-foundation/01.08-streaming-database-formalization.md |
| Thm-S-01-90 | (Schema演化一致性定理) | 定理 | Struct/01-foundation/01.10-schema-evolution-formalization.md |
| Thm-S-02-01 | 动态通道演算严格包含静态通道演算 | 定理 | Struct/Proof-Chains-Process-Calculus-Foundation.md |
| Thm-S-02-02 | 有限控制静态演算可判定性 | 定理 | Struct/Proof-Chains-Process-Calculus-Foundation.md |
| Thm-S-02-03 | 进程组合保持互模拟 | 定理 | Struct/Proof-Chains-Process-Calculus-Foundation.md |
| Thm-S-02-08 | (CALM定理 — Consistency As Logical Monotonicity): | 定理 | Struct/02-properties/02.06-calm-theorem.md |
| Thm-S-02-09 | 同态计算正确性定理 | 定理 | Struct/02-properties/02.07-encrypted-stream-processing.md |
| Thm-S-02-10 | 流式差分隐私组合性 (Streaming DP Composition) | 定理 | Struct/02-properties/02.08-differential-privacy-streaming.md |
| Thm-S-03-01 | Actor 邮箱串行处理下的局部确定性 | 定理 | Struct/Proof-Chains-Actor-Model.md |
| Thm-S-03-02 | 监督树活性定理 | 定理 | Struct/Proof-Chains-Actor-Model.md |
| Thm-S-04-01 | (Dataflow 确定性定理) | 定理 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Thm-S-04-02 | (算子组合确定性) | 定理 | Struct/Proof-Chains-Dataflow-Foundation.md |
| Thm-S-05-01 | 采用对 $Q \in \text{Go-CS-sync}$ 的结构归纳： | 定理 | Struct/01-foundation/01.05-csp-formalization.md |
| Thm-S-06-01 | 依赖以下关键引理和步骤 | 定理 | Struct/01-foundation/01.06-petri-net-formalization.md |
| Thm-S-06-02 | 投影算法的完备性 | 定理 | Struct/06-frontier/first-person-choreographies.md |
| Thm-S-06-03 | 与Census的互编码 | 定理 | Struct/06-frontier/first-person-choreographies.md |
| Thm-S-07-01 | (流计算确定性定理) | 定理 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Thm-S-07-02 | Checkpoint一致性的形式化证明 | 定理 | Struct/07-tools/coq-mechanization.md |
| Thm-S-07-03 | Stream 类型安全定理 | 定理 | Struct/07-tools/coq-mechanization.md |
| Thm-S-07-04 | Exactly-Once语义的形式化 | 定理 | Struct/07-tools/coq-mechanization.md |
| Thm-S-07-05 | 流计算常见证明模式的自动化 | 定理 | Struct/07-tools/proof-automation-guide.md |
| Thm-S-07-06 | Flink 2.x Generic WAL 规格 | 定理 | Struct/07-tools/tla-for-flink.md |
| Thm-S-07-07 | Smart Casual Verification的有效性定理 | 定理 | Struct/07-tools/smart-casual-verification.md |
| Thm-S-07-08 | CCF共识协议的安全性质规格 | 定理 | Struct/07-tools/smart-casual-verification.md |
| Thm-S-07-09 | Trace Validation搜索优化定理 | 定理 | Struct/07-tools/smart-casual-verification.md |
| Thm-S-08-01 | (Exactly-Once 网络分区必要条件) | 定理 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Thm-S-08-02 | (端到端 Exactly-Once 正确性) | 定理 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Thm-S-08-03 | 统一一致性格定理 | 定理 | Struct/Proof-Chains-Consistency-Hierarchy.md |
| Thm-S-09-01 | (Watermark 单调性定理) | 定理 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Thm-S-10-01 | Actor 安全/活性组合性 | 定理 | Struct/Proof-Chains-Actor-Model.md |
| Thm-S-11-01 | 类型安全(Progress + Preservation) | 定理 |  |
| Thm-S-12-01 | (Actor→CSP 编码保持定理) | 定理 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Thm-S-12-02 | 编码保持弱公平性 | 定理 | Struct/Proof-Chains-Relationships-Complete.md |
| Thm-S-12-03 | 编码保持安全性不变式 | 定理 | Struct/Proof-Chains-Relationships-Complete.md |
| Thm-S-12-04 | 受限Actor系统表达能力等价 | 定理 | Struct/Proof-Chains-Relationships-Complete.md |
| Thm-S-12-05 | 完整Actor系统严格强于CSP | 定理 | Struct/Proof-Chains-Relationships-Complete.md |
| Thm-S-13-01 | (Flink→π Exactly-Once 保持定理) | 定理 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Thm-S-13-02 | 水位线传播保持时间语义 | 定理 | Struct/Proof-Chains-Relationships-Complete.md |
| Thm-S-13-03 | 有状态算子编码保持状态一致性 | 定理 | Struct/Proof-Chains-Relationships-Complete.md |
| Thm-S-13-04 | Checkpoint恢复等价于进程重启 | 定理 | Struct/Proof-Chains-Relationships-Complete.md |
| Thm-S-13-05 | 并行度扩展保持语义 | 定理 | Struct/Proof-Chains-Relationships-Complete.md |
| Thm-S-14-01 | 表达能力严格层次定理 | 定理 | Struct/Proof-Chains-Relationships-Complete.md |
| Thm-S-14-02 | 流计算系统表达能力分类 | 定理 | Struct/Proof-Chains-Relationships-Complete.md |
| Thm-S-14-03 | 判定性递减定理 | 定理 | Struct/Proof-Chains-Relationships-Complete.md |
| Thm-S-14-04 | 模型编码存在性判定 | 定理 | Struct/Proof-Chains-Relationships-Complete.md |
| Thm-S-15-01 | 互模拟同余定理 | 定理 | Struct/Proof-Chains-Process-Calculus-Foundation.md |
| Thm-S-15-02 | 强互模拟是等价关系 | 定理 | Struct/Proof-Chains-Relationships-Complete.md |
| Thm-S-15-03 | 互模拟蕴含迹等价反之不成立 | 定理 | Struct/Proof-Chains-Relationships-Complete.md |
| Thm-S-15-04 | 弱互模拟保持可观察性质 | 定理 | Struct/Proof-Chains-Relationships-Complete.md |
| Thm-S-15-05 | 互模拟游戏完备性 | 定理 | Struct/Proof-Chains-Relationships-Complete.md |
| Thm-S-16-01 | 跨层映射组合定理 | 定理 | Struct/Proof-Chains-Relationships-Complete.md |
| Thm-S-16-02 | Galois连接保序性 | 定理 | Struct/Proof-Chains-Relationships-Complete.md |
| Thm-S-16-03 | 映射复合的Galois连接保持 | 定理 | Struct/Proof-Chains-Relationships-Complete.md |
| Thm-S-16-04 | 精化关系传递性 | 定理 | Struct/Proof-Chains-Relationships-Complete.md |
| Thm-S-16-05 | 形式化到Flink的正确性保持 | 定理 | Struct/Proof-Chains-Relationships-Complete.md |
| Thm-S-17-01 | (Flink Checkpoint 一致性定理) | 定理 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Thm-S-18-01 | (Flink Exactly-Once 正确性) | 定理 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Thm-S-18-02 | 幂等 Sink 等价性定理 | 定理 | Struct/04-proofs/04.02-flink-exactly-once-correctness.md |
| Thm-S-18-03 | visuals/theorem-dependencies.md | 定理 |  |
| Thm-S-19-01 | (Chandy-Lamport 算法记录一致全局状态) | 定理 | Struct/04-proofs/04.03-chandy-lamport-consistency.md |
| Thm-S-20-01 | (Watermark 完全格定理) | 定理 | Struct/04-proofs/04.04-watermark-algebra-formal-proof.md |
| Thm-S-20-02 | 结合律 (Associativity) | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-20-03 | 交换律 (Commutativity) | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-20-04 | 幂等律 (Idempotence) | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-20-05 | 吸收律 (Absorption) | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-20-06 | 算子传播单调性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-20-07 | 全局单调性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-20-08 | 边界保持性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-20-09 | 多源流合并完备性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-20-10 | Watermark 延迟边界 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-21-01 | FG/FGG类型安全定理 | 定理 |  |
| Thm-S-21-03 | 方法集闭包性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-21-04 | 动态分派正确性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-21-05 | 接口实现完备性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-21-06 | 替换与类型保持 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-21-07 | ~ Thm-S-21-10: 辅助引理组 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-22-01 | DOT子类型完备性定理 | 定理 |  |
| Thm-S-22-02 | 路径良构性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-22-03 | 路径等价判定 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-22-04 | 路径类型一致性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-22-05 | 名义子类型判定 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-22-06 | 结构子类型完备性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-22-07 | 混合系统一致性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-22-08 | mu 类型展开等价性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-22-09 | 递归类型终止性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-22-10 | F-有界多态保持 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-23-01 | Choreographic死锁自由定理 | 定理 |  |
| Thm-S-23-02 | EPP 完备性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-23-03 | 投影语义保持 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-23-04 | 合并重构性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-23-05 | 类型合成完备性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-23-06 | 合成唯一性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-23-07 | 合成与投影互逆 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-23-08 | 广播通信安全 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-23-09 | 多路选择完备性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-23-10 | 动态角色创建 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-24-01 | Go与Scala图灵完备等价 | 定理 |  |
| Thm-S-24-02 | 锁与信号量等价 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-24-03 | Channel 表达能力 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-24-04 | Select 非确定性完备性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-24-05 | Context 传播正确性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-24-06 | Happens-Before 传递性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-24-07 | Channel 同步强度 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-24-08 | Mutex 释放-获取序 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-24-09 | WaitGroup 同步点 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-24-10 | Atomic 操作全序 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-24-11 | Go 编译器语义保持 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-24-12 | Scala 类型擦除正确性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-24-13 | JIT 优化保持性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-24-14 | GC 安全点一致性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-24-15 | 内联优化正确性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-24-16 | 逃逸分析正确性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-24-17 | 栈分裂安全 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-24-18 | 写屏障正确性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-24-19 | 闭包转换正确性 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-24-20 | 尾调用优化条件 | 定理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Thm-S-25-01 | Struct/05-comparative-analysis/05.02-expressiveness-vs-decidability.md | 定理 |  |
| Thm-S-26-01 | 编码保持性分解定理 | 定理 | Struct/Proof-Chains-Relationships-Complete.md |
| Thm-S-26-02 | (Actor 到 CSP 编码非完备性) | 定理 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Thm-S-29-01 | PRESENTATION-DECK.md | 定理 |  |
| Def-S-01-01 | USTM 统一流计算元模型 | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-01-02 | 六层表达能力层次 | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-01-03 | Processor 处理器 | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-01-04 | Channel 通道 | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-01-05 | TimeModel 时间模型 | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-01-06 | Consistency Model 一致性模型 | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-01-07 | UCM 统一并发模型 | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-01-08 | 二元会话类型语法 | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-01-09 | 双寡规则 (Duality) | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-01-10 | 全局类型 (Global Types) | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-01-11 | 会话-进程编码 | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-01-50 | 流作为无限序列 | 定义 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Def-S-01-51 | 时间域结构 | 定义 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Def-S-01-52 | 事件时间与处理时间语义 | 定义 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Def-S-01-53 | 流的完整性与有界性 | 定义 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Def-S-01-54 | 窗口类型定义 | 定义 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Def-S-01-55 | 核心算子形式化定义 | 定义 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Def-S-01-56 | Join算子的形式化 | 定义 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Def-S-01-57 | 状态空间定义 | 定义 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Def-S-01-58 | 流到进程演算的编码 | 定义 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Def-S-01-59 | 流处理的π-演算编码 | 定义 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Def-S-01-60 | Dataflow模型形式化 | 定义 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Def-S-01-61 | Actor模型的流编码 | 定义 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Def-S-01-62 | Watermark形式化 | 定义 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Def-S-01-63 | 交付保证层级 | 定义 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Def-S-01-64 | 一致性模型形式化 | 定义 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Def-S-01-80 | (流数据库核心模型) | 定义 | Struct/01-foundation/01.08-streaming-database-formalization.md |
| Def-S-01-81 | (物化视图) | 定义 | Struct/01-foundation/01.08-streaming-database-formalization.md |
| Def-S-01-82 | (增量维护) | 定义 | Struct/01-foundation/01.08-streaming-database-formalization.md |
| Def-S-01-83 | (一致性级别：严格串行化) | 定义 | Struct/01-foundation/01.08-streaming-database-formalization.md |
| Def-S-01-84 | (一致性级别：快照隔离) | 定义 | Struct/01-foundation/01.08-streaming-database-formalization.md |
| Def-S-01-85 | (一致性级别：读已提交) | 定义 | Struct/01-foundation/01.08-streaming-database-formalization.md |
| Def-S-01-86 | (流SQL查询语义) | 定义 | Struct/01-foundation/01.08-streaming-database-formalization.md |
| Def-S-01-96 | (Schema Version) | 定义 | Struct/01-foundation/01.10-schema-evolution-formalization.md |
| Def-S-01-97 | (Compatibility Judgment) | 定义 | Struct/01-foundation/01.10-schema-evolution-formalization.md |
| Def-S-01-98 | (Schema Migration Function) | 定义 | Struct/01-foundation/01.10-schema-evolution-formalization.md |
| Def-S-01-99 | (Type Evolution) | 定义 | Struct/01-foundation/01.10-schema-evolution-formalization.md |
| Def-S-02-01 | (CCS - 通信系统演算) | 定义 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Def-S-02-02 | (CSP - 通信顺序进程) | 定义 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Def-S-02-03 | (π-Calculus - 通道移动性) | 定义 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Def-S-02-04 | 二进制会话类型 (Binary Session Types) | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-02-13 | (分布式问题): 一个分布式问题 $\mathcal{P}$ 是一个映射 $P: \mathcal{I} \to \mathcal{O}$，其中： | 定义 | Struct/02-properties/02.06-calm-theorem.md |
| Def-S-02-14 | (逻辑单调性): 问题 $P$ 是逻辑单调的（Logically Monotone），当且仅当： | 定义 | Struct/02-properties/02.06-calm-theorem.md |
| Def-S-02-15 | (协调): 协调（Coordination）是指在分布式计算中，为了确保正确性而引入的进程间同步机制，包括： | 定义 | Struct/02-properties/02.06-calm-theorem.md |
| Def-S-02-16 | (一致性作为程序结果确定性): 分布式实现 $\mathcal{A}$ 满足一致性，当且仅当对于所有可能的执行轨迹 $\sigma \in \text{Exec}(\mathcal{A})$： | 定义 | Struct/02-properties/02.06-calm-theorem.md |
| Def-S-02-17 | 同态加密 (Homomorphic Encryption, HE) | 定义 | Struct/02-properties/02.07-encrypted-stream-processing.md |
| Def-S-02-18 | 安全多方计算 (Multi-Party Computation, MPC) | 定义 | Struct/02-properties/02.07-encrypted-stream-processing.md |
| Def-S-02-19 | 可信执行环境 (Trusted Execution Environment, TEE) | 定义 | Struct/02-properties/02.07-encrypted-stream-processing.md |
| Def-S-02-20 | 密文计算语义 | 定义 | Struct/02-properties/02.07-encrypted-stream-processing.md |
| Def-S-02-21 | (ε,δ)-差分隐私 ((ε,δ)-Differential Privacy) | 定义 | Struct/02-properties/02.08-differential-privacy-streaming.md |
| Def-S-02-22 | 敏感度 (Sensitivity) | 定义 | Struct/02-properties/02.08-differential-privacy-streaming.md |
| Def-S-02-23 | 隐私预算管理 (Privacy Budget Management) | 定义 | Struct/02-properties/02.08-differential-privacy-streaming.md |
| Def-S-02-24 | 流式噪声机制 (Streaming Noise Mechanisms) | 定义 | Struct/02-properties/02.08-differential-privacy-streaming.md |
| Def-S-03-01 | Actor (经典 Actor 四元组) | 定义 | Struct/Proof-Chains-Actor-Model.md |
| Def-S-03-02 | Behavior (行为) | 定义 | Struct/Proof-Chains-Actor-Model.md |
| Def-S-03-03 | Mailbox (邮箱) | 定义 | Struct/Proof-Chains-Actor-Model.md |
| Def-S-03-04 | ActorRef (Actor 不透明引用) | 定义 | Struct/Proof-Chains-Actor-Model.md |
| Def-S-03-05 | Supervision Tree (监督树) | 定义 | Struct/Proof-Chains-Actor-Model.md |
| Def-S-03-06 | IMPACT-REPORT.md | 定义 |  |
| Def-S-03-07 | IMPACT-REPORT.md | 定义 |  |
| Def-S-03-08 | IMPACT-REPORT.md | 定义 |  |
| Def-S-04-01 | (Dataflow 图) | 定义 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Def-S-04-02 | (算子语义) | 定义 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Def-S-04-03 | (流作为偏序多重集) | 定义 | Struct/Proof-Chains-Dataflow-Foundation.md |
| Def-S-04-04 | (事件时间与 Watermark) | 定义 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Def-S-04-05 | 窗口形式化 (Window) | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-05-01 | CSP 核心语法 | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-05-02 | CSP 结构化操作语义 (SOS) | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-05-03 | CSP 迹/失败/发散语义 | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-05-04 | CSP 通道与同步原语 | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-05-05 | Go-CS-sync 到 CSP 编码 | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-06-01 | P/T 网 (Place/Transition Net) | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-06-02 | 变迁触发规则 (Firing Rule) | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-06-03 | 可达性与可达图 | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-06-04 | 着色 Petri 网 (CPN) | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-06-05 | 时间 Petri 网 (TPN) | 定义 | Struct/Proof-Chains-Foundation-Complete.md |
| Def-S-06-06 | (Petri 网层次结构) | 定义 | Struct/01-foundation/01.06-petri-net-formalization.md |
| Def-S-06-07 | (pDOT Calculus) | 定义 | Struct/06-frontier/06.04-pdot-path-dependent-types.md |
| Def-S-06-08 | (路径依赖类型 - 任意长度路径) | 定义 | Struct/06-frontier/06.04-pdot-path-dependent-types.md |
| Def-S-06-09 | (Singleton 类型 - 路径等价追踪) | 定义 | Struct/06-frontier/06.04-pdot-path-dependent-types.md |
| Def-S-06-10 | (精确对象类型 - Precise Object Typing) | 定义 | Struct/06-frontier/06.04-pdot-path-dependent-types.md |
| Def-S-06-11 | 进程参数化 (Process Parameterisation) | 定义 | Struct/06-frontier/first-person-choreographies.md |
| Def-S-06-12 | Continuation-Passing通信 (CPC) | 定义 | Struct/06-frontier/first-person-choreographies.md |
| Def-S-07-01 | (确定性流处理系统) | 定义 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Def-S-07-02 | 合流规约语义 | 定义 | Struct/Proof-Chains-Consistency-Hierarchy.md |
| Def-S-07-03 | (可观测确定性) | 定义 | Struct/02-properties/02.01-determinism-in-streaming.md |
| Def-S-07-04 | (无竞争条件) | 定义 | Struct/02-properties/02.01-determinism-in-streaming.md |
| Def-S-07-05 | 资源代数 (Resource Algebra) | 定义 | Struct/07-tools/iris-separation-logic.md |
| Def-S-07-06 | 不变式与原子性 | 定义 | Struct/07-tools/iris-separation-logic.md |
| Def-S-07-07 | Coq归纳类型 (Inductive Types) | 定义 | Struct/07-tools/coq-mechanization.md |
| Def-S-07-08 | 依赖类型与规约 (Dependent Types & Specifications) | 定义 | Struct/07-tools/coq-mechanization.md |
| Def-S-07-09 | 策略证明 (Tactics) | 定义 | Struct/07-tools/coq-mechanization.md |
| Def-S-07-10 | Stream 类型形式化定义 | 定义 | Struct/07-tools/coq-mechanization.md |
| Def-S-07-11 | LTL/CTL时序逻辑 | 定义 | Struct/07-tools/model-checking-practice.md |
| Def-S-07-12 | 状态爆炸问题 (State Space Explosion) | 定义 | Struct/07-tools/model-checking-practice.md |
| Def-S-07-13 | 策略反射 (Proof by Reflection) | 定义 | Struct/07-tools/proof-automation-guide.md |
| Def-S-07-14 | Casual Verification（轻量验证） | 定义 | Struct/07-tools/smart-casual-verification.md |
| Def-S-07-15 | Trace-规格一致性检查 | 定义 | Struct/07-tools/smart-casual-verification.md |
| Def-S-07-16 | Consensus Bug模式分类 | 定义 | Struct/07-tools/smart-casual-verification.md |
| Def-S-08-01 | At-Most-Once 语义 | 定义 | Struct/Proof-Chains-Consistency-Hierarchy.md |
| Def-S-08-02 | (At-Most-Once 语义) | 定义 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Def-S-08-03 | (At-Least-Once 语义) | 定义 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Def-S-08-04 | (Exactly-Once 语义) | 定义 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Def-S-08-05 | (端到端一致性) | 定义 | Struct/02-properties/02.02-consistency-hierarchy.md |
| Def-S-08-06 | (内部一致性) | 定义 | Struct/02-properties/02.02-consistency-hierarchy.md |
| Def-S-08-07 | (Strong Consistency) | 定义 | Struct/02-properties/02.02-consistency-hierarchy.md |
| Def-S-08-08 | (Causal Consistency) | 定义 | Struct/02-properties/02.02-consistency-hierarchy.md |
| Def-S-08-09 | (Eventual Consistency) | 定义 | Struct/02-properties/02.02-consistency-hierarchy.md |
| Def-S-09-01 | (事件时间严格定义) | 定义 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Def-S-09-02 | (水印语义) | 定义 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Def-S-10-01 | 安全性(Safety) | 定义 |  |
| Def-S-10-02 | 活性(Liveness) | 定义 |  |
| Def-S-10-03 | Struct/02-properties/02.04-liveness-and-safety.md | 定义 |  |
| Def-S-10-04 | Struct/02-properties/02.04-liveness-and-safety.md | 定义 |  |
| Def-S-10-05 | Struct/02-properties/02.04-liveness-and-safety.md | 定义 |  |
| Def-S-11-01 | NAVIGATION-INDEX.md | 定义 |  |
| Def-S-11-02 | Featherweight Go语法 | 定义 |  |
| Def-S-11-03 | Generic Go语法 | 定义 |  |
| Def-S-11-04 | DOT路径依赖类型 | 定义 |  |
| Def-S-11-05 | Struct/02-properties/02.05-type-safety-derivation.md | 定义 |  |
| Def-S-12-01 | [Actor配置四元组] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-12-02 | [CSP核心语法子集] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-12-03 | Actor→CSP 编码函数 | 定义 | Struct/Proof-Chains-Cross-Model-Encoding.md |
| Def-S-12-04 | 受限Actor系统 | 定义 |  |
| Def-S-12-05 | [Actor监督树结构] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-12-06 | [分布式Actor网络] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-13-01 | (Flink 算子到 π-演算编码) | 定义 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Def-S-13-02 | [Dataflow边→π-演算通道] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-13-03 | (Checkpoint→屏障同步编码) | 定义 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Def-S-13-04 | [状态算子→带状态进程] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-13-06 | [RocksDB状态后端编码] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-13-07 | [Hive状态后端编码] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-14-01 | [表达能力预序] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-14-02 | [互模拟等价] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-14-03 | [六层表达能力层次] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-14-05 | [流SQL表达能力] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-14-06 | [窗口操作层级] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-14-07 | [时间语义影响] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-15-01 | [强互模拟] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-15-02 | [弱互模拟与分支互模拟] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-15-03 | [互模拟游戏] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-15-04 | [同余关系] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-15-05 | [分支互模拟] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-15-06 | [测试等价] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-15-07 | [失败等价] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-15-08 | [概率互模拟] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-15-09 | [时间互模拟] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-16-01 | [四层统一映射框架] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-16-02 | [层间Galois连接] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-16-03 | [跨层组合映射] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-16-04 | [语义保持性与精化关系] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-16-05 | [模型精化链] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-16-06 | [逆向映射] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-16-07 | [多模型融合] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-16-08 | [模型演化映射] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-16-09 | [抽象解释连接] | 定义 | Struct/Proof-Chains-Relationships-Complete.md |
| Def-S-17-01 | (Checkpoint Barrier 语义) | 定义 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Def-S-17-02 | (一致全局状态) | 定义 | Struct/04-proofs/04.01-flink-checkpoint-correctness.md |
| Def-S-17-03 | (Checkpoint 对齐) | 定义 | Struct/04-proofs/04.01-flink-checkpoint-correctness.md |
| Def-S-17-04 | (状态快照原子性) | 定义 | Struct/04-proofs/04.01-flink-checkpoint-correctness.md |
| Def-S-18-01 | (Exactly-Once 语义) | 定义 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Def-S-18-02 | 端到端一致性 (End-to-End Consistency) | 定义 | Struct/04-proofs/04.02-flink-exactly-once-correctness.md |
| Def-S-18-03 | (2PC 协议) | 定义 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Def-S-18-04 | 可重放 Source (Replayable Source) | 定义 | Struct/04-proofs/04.02-flink-exactly-once-correctness.md |
| Def-S-18-05 | 幂等性 (Idempotency) | 定义 | Struct/04-proofs/04.02-flink-exactly-once-correctness.md |
| Def-S-19-01 | (全局状态) | 定义 | Struct/04-proofs/04.03-chandy-lamport-consistency.md |
| Def-S-19-02 | (一致割集 / Consistent Cut) {#def-s-19-02-一致割集--consistent-cut} | 定义 | Struct/04-proofs/04.03-chandy-lamport-consistency.md |
| Def-S-19-03 | (通道状态) | 定义 | Struct/04-proofs/04.03-chandy-lamport-consistency.md |
| Def-S-19-04 | (Marker 消息) | 定义 | Struct/04-proofs/04.03-chandy-lamport-consistency.md |
| Def-S-19-05 | (本地快照) | 定义 | Struct/04-proofs/04.03-chandy-lamport-consistency.md |
| Def-S-20-01 | (Watermark 格元素) | 定义 | Struct/04-proofs/04.04-watermark-algebra-formal-proof.md |
| Def-S-20-02 | (Watermark 合并算子 ⊔) | 定义 | Struct/04-proofs/04.04-watermark-algebra-formal-proof.md |
| Def-S-20-03 | (Watermark 偏序关系 ⊑) | 定义 | Struct/04-proofs/04.04-watermark-algebra-formal-proof.md |
| Def-S-20-04 | (Watermark 传播规则) | 定义 | Struct/04-proofs/04.04-watermark-algebra-formal-proof.md |
| Def-S-20-05 | (Watermark 完全格) | 定义 | Struct/04-proofs/04.04-watermark-algebra-formal-proof.md |
| Def-S-20-06 | (全局类型推断系统) | 定义 | Struct/06-frontier/06.02-choreographic-streaming-programming.md |
| Def-S-21-01 | FG抽象语法 | 定义 |  |
| Def-S-21-02 | FGG泛型扩展 | 定义 |  |
| Def-S-21-03 | 类型替换 | 定义 |  |
| Def-S-21-04 | 方法解析 | 定义 |  |
| Def-S-22-01 | DOT抽象语法 | 定义 |  |
| Def-S-22-02 | 路径与路径类型 | 定义 |  |
| Def-S-22-03 | 名义类型与结构类型 | 定义 |  |
| Def-S-22-04 | 类型成员声明 | 定义 |  |
| Def-S-22-05 | Struct/04-proofs/04.06-dot-subtyping-completeness.md | 定义 |  |
| Def-S-23-01 | Choreographic Programming | 定义 |  |
| Def-S-23-02 | Global Types | 定义 |  |
| Def-S-23-03 | Endpoint Projection | 定义 |  |
| Def-S-23-04 | Deadlock Freedom | 定义 |  |
| Def-S-23-05 | Choral Language | 定义 |  |
| Def-S-23-06 | MultiChor扩展 | 定义 |  |
| Def-S-25-01 | CRITICAL-EVALUATION-REPORT-v1.0.md | 定义 |  |
| Def-S-25-02 | Struct/00-INDEX.md | 定义 |  |
| Def-S-25-03 | Struct/00-INDEX.md | 定义 |  |
| Def-S-25-04 | Struct/00-INDEX.md | 定义 |  |
| Def-S-26-01 | Struct/05-comparative-analysis/05.03-encoding-completeness-analysis.md | 定义 |  |
| Def-S-26-02 | Struct/05-comparative-analysis/05.03-encoding-completeness-analysis.md | 定义 |  |
| Def-S-26-03 | Struct/05-comparative-analysis/05.03-encoding-completeness-analysis.md | 定义 |  |
| Def-S-26-04 | Struct/05-comparative-analysis/05.03-encoding-completeness-analysis.md | 定义 |  |
| Def-S-29-01 | Struct/00-INDEX.md | 定义 |  |
| Def-S-29-02 | Struct/00-INDEX.md | 定义 |  |
| Def-S-29-03 | Struct/00-INDEX.md | 定义 |  |
| Def-S-29-04 | Struct/00-INDEX.md | 定义 |  |
| Def-S-29-05 | Struct/00-INDEX.md | 定义 |  |
| Def-S-29-06 | Struct/00-INDEX.md | 定义 |  |
| Lemma-S-01-01 | 无状态算子的单调性 | 引理 | Struct/01-foundation/stream-processing-semantics-formalization.md |
| Lemma-S-01-02 | AGENTS.md | 引理 |  |
| Lemma-S-01-04 | Struct/01-foundation/01.07-session-types.md | 引理 |  |
| Lemma-S-01-05 | Struct/01-foundation/01.07-session-types.md | 引理 |  |
| Lemma-S-01-06 | Struct/01-foundation/01.07-session-types.md | 引理 |  |
| Lemma-S-01-80 | (物化视图更新单调性) | 引理 | Struct/01-foundation/01.08-streaming-database-formalization.md |
| Lemma-S-01-81 | (增量维护正确性条件) | 引理 | Struct/01-foundation/01.08-streaming-database-formalization.md |
| Lemma-S-01-82 | (一致性级别蕴含关系) | 引理 | Struct/01-foundation/01.08-streaming-database-formalization.md |
| Lemma-S-01-90 | (兼容性传递性) | 引理 | Struct/01-foundation/01.10-schema-evolution-formalization.md |
| Lemma-S-01-91 | (迁移函数合成性) | 引理 | Struct/01-foundation/01.10-schema-evolution-formalization.md |
| Lemma-S-02-01 | 静态通道模型的拓扑不变性 | 引理 | Struct/Proof-Chains-Process-Calculus-Foundation.md |
| Lemma-S-02-02 | 动态通道演算的图灵完备性 | 引理 | Struct/Proof-Chains-Process-Calculus-Foundation.md |
| Lemma-S-02-10 | 同态运算复合封闭性 | 引理 | Struct/02-properties/02.07-encrypted-stream-processing.md |
| Lemma-S-02-11 | 噪声增长边界 | 引理 | Struct/02-properties/02.07-encrypted-stream-processing.md |
| Lemma-S-02-12 | (单调性的集合运算封闭性): 逻辑单调性对以下运算封闭： | 引理 | Struct/02-properties/02.06-calm-theorem.md |
| Lemma-S-02-13 | (非单调操作的不封闭性): 以下操作不保持逻辑单调性： | 引理 | Struct/02-properties/02.06-calm-theorem.md |
| Lemma-S-02-14 | (单调性的网络容忍性): 若问题 $P$ 是逻辑单调的，则对于任意消息延迟函数 $\delta: \mathbb{M} \to \mathbb{R}^+$，存在异步实现 $\mathcal{A}_\delta$ 使得： | 引理 | Struct/02-properties/02.06-calm-theorem.md |
| Lemma-S-03-01 | 邮箱串行处理引理 | 引理 | Struct/Proof-Chains-Actor-Model.md |
| Lemma-S-03-02 | 监督树故障传播有界性 | 引理 | Struct/Proof-Chains-Actor-Model.md |
| Lemma-S-04-01 | (算子局部确定性) | 引理 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Lemma-S-04-02 | (Watermark 单调性) | 引理 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Lemma-S-04-03 | (状态算子幂等性) | 引理 | Struct/Proof-Chains-Dataflow-Foundation.md |
| Lemma-S-04-04 | (算子组合封闭性) | 引理 | Struct/Proof-Chains-Dataflow-Foundation.md |
| Lemma-S-04-05 | IMPACT-REPORT.md | 引理 |  |
| Lemma-S-05-01 | (CSP 外部选择可执行分支集合保持性) | 引理 | Struct/01-foundation/01.05-csp-formalization.md |
| Lemma-S-05-02 | (CSP 同步并行下迹前缀保持性) | 引理 | Struct/01-foundation/01.05-csp-formalization.md |
| Lemma-S-06-01 | (Karp-Miller 树有限性) | 引理 | Struct/01-foundation/01.06-petri-net-formalization.md |
| Lemma-S-06-02 | (Petri 网触发规则的单调性) | 引理 | Struct/01-foundation/01.06-petri-net-formalization.md |
| Lemma-S-06-03 | (路径规范化) | 引理 | Struct/06-frontier/06.04-pdot-path-dependent-types.md |
| Lemma-S-06-04 | (路径等价传递性) | 引理 | Struct/06-frontier/06.04-pdot-path-dependent-types.md |
| Lemma-S-07-01 | 确定性蕴含可重现性 | 引理 | Struct/Proof-Chains-Consistency-Hierarchy.md |
| Lemma-S-07-02 | Watermark 单调性蕴含触发确定性 | 引理 | Struct/Proof-Chains-Consistency-Hierarchy.md |
| Lemma-S-07-03 | 分区哈希的确定性 | 引理 | Struct/Proof-Chains-Properties-Complete.md |
| Lemma-S-07-04 | 汇合系统的全局确定性 | 引理 | Struct/Proof-Chains-Properties-Complete.md |
| Lemma-S-07-05 | 纯函数性 + FIFO + 事件时间 → 可观测确定性 | 引理 | Struct/Proof-Chains-Properties-Complete.md |
| Lemma-S-07-06 | 无竞争条件 ↔ Keyed 分区状态隔离 | 引理 | Struct/Proof-Chains-Properties-Complete.md |
| Lemma-S-07-07 | 结合律聚合函数对重放记录顺序不敏感 | 引理 | Struct/Proof-Chains-Properties-Complete.md |
| Lemma-S-07-08 | TLA+自动转换 | 引理 |  |
| Lemma-S-08-01 | 端到端 Exactly-Once 分解 | 引理 | Struct/Proof-Chains-Consistency-Hierarchy.md |
| Lemma-S-08-02 | 一致性层级蕴含关系 | 引理 | Struct/Proof-Chains-Consistency-Hierarchy.md |
| Lemma-S-08-03 | At-Least-Once 与 At-Most-Once 的误差互补性 | 引理 | Struct/Proof-Chains-Properties-Complete.md |
| Lemma-S-08-04 | Strong Consistency 蕴含 Causal Consistency | 引理 | Struct/Proof-Chains-Properties-Complete.md |
| Lemma-S-08-05 | Causal Consistency 蕴含 Eventual Consistency | 引理 | Struct/Proof-Chains-Properties-Complete.md |
| Lemma-S-09-01 | Watermark 推进保证事件时间进展 | 引理 | Struct/Proof-Chains-Consistency-Hierarchy.md |
| Lemma-S-10-01 | 安全性有限见证 | 引理 | Struct/Proof-Chains-Actor-Model.md |
| Lemma-S-10-02 | 活性无限承诺 | 引理 | Struct/Proof-Chains-Properties-Complete.md |
| Lemma-S-10-03 | Struct/02-properties/02.04-liveness-and-safety.md | 引理 |  |
| Lemma-S-11-01 | 替换引理 | 引理 |  |
| Lemma-S-11-02 | Struct/02-properties/02.05-type-safety-derivation.md | 引理 |  |
| Lemma-S-11-03 | Struct/02-properties/02.05-type-safety-derivation.md | 引理 |  |
| Lemma-S-12-01 | MAILBOX FIFO 不变式 | 引理 | Struct/Proof-Chains-Cross-Model-Encoding.md |
| Lemma-S-12-02 | Actor 进程单线程性 | 引理 | Struct/Proof-Chains-Cross-Model-Encoding.md |
| Lemma-S-12-03 | 状态不可外部访问 | 引理 | Struct/Proof-Chains-Cross-Model-Encoding.md |
| Lemma-S-13-01 | 算子编码保持局部确定性 | 引理 | Struct/Proof-Chains-Cross-Model-Encoding.md |
| Lemma-S-13-02 | Barrier 对齐保证快照一致性 | 引理 | Struct/Proof-Chains-Cross-Model-Encoding.md |
| Lemma-S-13-03 | [异步快照非阻塞性] | 引理 | Struct/Proof-Chains-Relationships-Complete.md |
| Lemma-S-14-01 | [组合性编码状态空间上界] | 引理 | Struct/Proof-Chains-Relationships-Complete.md |
| Lemma-S-14-02 | [动态拓扑不可回归性] | 引理 | Struct/Proof-Chains-Relationships-Complete.md |
| Lemma-S-15-01 | 强互模拟是等价关系 | 引理 | Struct/Proof-Chains-Process-Calculus-Foundation.md |
| Lemma-S-15-02 | 互模拟蕴含迹等价反之不成立 | 引理 | Struct/Proof-Chains-Process-Calculus-Foundation.md |
| Lemma-S-15-03 | 弱互模拟的复合保持性 | 引理 | Struct/Proof-Chains-Process-Calculus-Foundation.md |
| Lemma-S-15-04 | 互模拟关系的最大不动点刻画 | 引理 | Struct/Proof-Chains-Process-Calculus-Foundation.md |
| Lemma-S-16-01 | [Galois连接的保序性] | 引理 | Struct/Proof-Chains-Relationships-Complete.md |
| Lemma-S-16-02 | [映射复合的Galois连接保持] | 引理 | Struct/Proof-Chains-Relationships-Complete.md |
| Lemma-S-17-01 | (Barrier 传播不变式) | 引理 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Lemma-S-17-02 | (状态一致性引理) | 引理 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Lemma-S-17-03 | 对齐点唯一性 | 引理 | Struct/Proof-Chains-Properties-Complete.md |
| Lemma-S-17-04 | 无孤儿消息保证 | 引理 | Struct/Proof-Chains-Properties-Complete.md |
| Lemma-S-18-01 | (Source 可重放引理) | 引理 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Lemma-S-18-02 | (2PC 原子性引理) | 引理 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Lemma-S-18-03 | 状态恢复一致性引理 (State Recovery Consistency Lemma) | 引理 | Struct/04-proofs/04.02-flink-exactly-once-correctness.md |
| Lemma-S-18-04 | 算子确定性引理 (Operator Determinism Lemma) | 引理 | Struct/04-proofs/04.02-flink-exactly-once-correctness.md |
| Lemma-S-19-01 | (Marker 传播不变式) | 引理 | Struct/04-proofs/04.03-chandy-lamport-consistency.md |
| Lemma-S-19-02 | (一致割集引理 / Consistent Cut Lemma) {#lemma-s-19-02-一致割集引理--consistent-cut-lemma} | 引理 | Struct/04-proofs/04.03-chandy-lamport-consistency.md |
| Lemma-S-19-03 | (通道状态完备性) | 引理 | Struct/04-proofs/04.03-chandy-lamport-consistency.md |
| Lemma-S-19-04 | (无孤儿消息保证) | 引理 | Struct/04-proofs/04.03-chandy-lamport-consistency.md |
| Lemma-S-20-01 | (⊔ 结合律) {#lemma-s-20-01--结合律} | 引理 | Struct/04-proofs/04.04-watermark-algebra-formal-proof.md |
| Lemma-S-20-02 | (⊔ 交换律) {#lemma-s-20-02--交换律} | 引理 | Struct/04-proofs/04.04-watermark-algebra-formal-proof.md |
| Lemma-S-20-03 | (⊔ 幂等律) {#lemma-s-20-03--幂等律} | 引理 | Struct/04-proofs/04.04-watermark-algebra-formal-proof.md |
| Lemma-S-20-04 | (⊔ 吸收律与单位元) {#lemma-s-20-04--吸收律与单位元} | 引理 | Struct/04-proofs/04.04-watermark-algebra-formal-proof.md |
| Lemma-S-21-01 | (替换引理): | 引理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Lemma-S-21-02 | (置换引理): | 引理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Lemma-S-21-03 | (结构子类型反身性): | 引理 | Struct/Proof-Chains-Proofs-Remaining.md |
| Lemma-S-21-04 | Struct/04-proofs/04.05-type-safety-fg-fgg.md | 引理 |  |
| Lemma-S-21-05 | Struct/04-proofs/04.05-type-safety-fg-fgg.md | 引理 |  |
| Lemma-S-21-06 | Struct/04-proofs/04.05-type-safety-fg-fgg.md | 引理 |  |
| Lemma-S-22-01 | Struct/04-proofs/04.06-dot-subtyping-completeness.md | 引理 |  |
| Lemma-S-22-02 | Struct/04-proofs/04.06-dot-subtyping-completeness.md | 引理 |  |
| Lemma-S-22-03 | Struct/04-proofs/04.06-dot-subtyping-completeness.md | 引理 |  |
| Lemma-S-22-04 | Struct/04-proofs/04.06-dot-subtyping-completeness.md | 引理 |  |
| Lemma-S-22-05 | Struct/04-proofs/04.06-dot-subtyping-completeness.md | 引理 |  |
| Lemma-S-22-06 | Struct/04-proofs/04.06-dot-subtyping-completeness.md | 引理 |  |
| Lemma-S-22-07 | Struct/04-proofs/04.06-dot-subtyping-completeness.md | 引理 |  |
| Lemma-S-23-01 | EPP保持通信结构 | 引理 |  |
| Lemma-S-23-02 | 投影合成还原 | 引理 |  |
| Lemma-S-23-03 | 类型保持性 | 引理 |  |
| Lemma-S-25-01 | Struct/00-INDEX.md | 引理 |  |
| Lemma-S-25-02 | Struct/00-INDEX.md | 引理 |  |
| Lemma-S-26-01 | Struct/05-comparative-analysis/05.03-encoding-completeness-analysis.md | 引理 |  |
| Lemma-S-26-02 | Struct/05-comparative-analysis/05.03-encoding-completeness-analysis.md | 引理 |  |
| Lemma-S-29-01 | Struct/00-INDEX.md | 引理 |  |
| Lemma-S-29-02 | Struct/00-INDEX.md | 引理 |  |
| Lemma-S-29-03 | Struct/00-INDEX.md | 引理 |  |
| Lemma-S-29-04 | Struct/00-INDEX.md | 引理 |  |
| Prop-S-01-80 | (物化视图可交换性条件) | 命题 | Struct/01-foundation/01.08-streaming-database-formalization.md |
| Prop-S-01-90 | (向后兼容性保持性) | 命题 | Struct/01-foundation/01.10-schema-evolution-formalization.md |
| Prop-S-02-01 | (对偶性蕴含通信兼容) | 命题 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Prop-S-02-02 | (有限控制静态演算的可判定性) | 命题 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Prop-S-02-07 | 时序相关性的隐私放大效应 | 命题 | Struct/02-properties/02.08-differential-privacy-streaming.md |
| Prop-S-02-08 | 密文流处理延迟分解 | 命题 | Struct/02-properties/02.07-encrypted-stream-processing.md |
| Prop-S-03-01 | ActorRef不透明性蕴含位置透明 | 命题 |  |
| Prop-S-04-01 | (状态算子幂等性条件) | 命题 | Struct/01-foundation/01.04-dataflow-model-formalization.md |
| Prop-S-06-01 | 1CP表达力完备性 | 命题 | Struct/06-frontier/first-person-choreographies.md |
| Prop-S-06-02 | (类型良好性保持) | 命题 | Struct/06-frontier/06.04-pdot-path-dependent-types.md |
| Prop-S-07-01 | Iris 编码 Actor 模型 | 命题 | Struct/07-tools/iris-separation-logic.md |
| Prop-S-07-02 | Session Types 的 Iris 嵌入 | 命题 | Struct/07-tools/iris-separation-logic.md |
| Prop-S-07-03 | Coq逻辑一致性 | 命题 | Struct/07-tools/coq-mechanization.md |
| Prop-S-07-04 | Generic WAL 安全性 | 命题 | Struct/07-tools/tla-for-flink.md |
| Prop-S-07-05 | 提取计算正确性 | 命题 | Struct/07-tools/coq-mechanization.md |
| Prop-S-07-06 | 策略组合保持正确性 | 命题 | Struct/07-tools/proof-automation-guide.md |
| Prop-S-08-01 | (端到端一致性分解) | 命题 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Prop-S-08-02 | 时间语义一致性 | 命题 | Struct/08-standards/streaming-sql-standard.md |
| Prop-S-13-01 | (分区策略保持键的局部性) | 命题 | Struct/03-relationships/03.02-flink-to-process-calculus.md |
| Prop-S-14-01 | 可判定性单调递减律 | 命题 |  |
| Prop-S-14-02 | 编码存在性保持不可判定性 | 命题 |  |
| Prop-S-15-01 | 弱互模拟的同余缺陷 | 命题 |  |
| Prop-S-15-02 | 分支互模拟保持发散行为 | 命题 |  |
| Prop-S-16-01 | (理论-语言编码的语义保持性) | 命题 | Struct/03-relationships/03.05-cross-model-mappings.md |
| Prop-S-16-02 | (跨层映射的传递性) | 命题 | Struct/03-relationships/03.05-cross-model-mappings.md |
| Prop-S-16-03 | (精化关系的层间保持) | 命题 | Struct/03-relationships/03.05-cross-model-mappings.md |
| Prop-S-17-01 | (Barrier 对齐与 Exactly-Once 的关系) | 命题 | Struct/04-proofs/04.01-flink-checkpoint-correctness.md |
| Prop-S-18-01 | Checkpoint 与 2PC 的绑定关系 | 命题 | Struct/04-proofs/04.02-flink-exactly-once-correctness.md |
| Prop-S-18-02 | 观察等价性 (Observational Equivalence) | 命题 | Struct/04-proofs/04.02-flink-exactly-once-correctness.md |
| Prop-S-20-01 | (Watermark 单调性与格结构的兼容性) | 命题 | Struct/04-proofs/04.04-watermark-algebra-formal-proof.md |
| Prop-S-23-01 | Choreography的合流性 | 命题 |  |
| Prop-S-23-02 | 投影语义等价性 | 命题 |  |
| Prop-S-25-01 | Struct/00-INDEX.md | 命题 |  |
| Prop-S-25-02 | Struct/05-comparative-analysis/05.02-expressiveness-vs-decidability.md | 命题 |  |
| Prop-S-25-03 | Struct/05-comparative-analysis/05.02-expressiveness-vs-decidability.md | 命题 |  |
| Prop-S-25-04 | Struct/05-comparative-analysis/05.02-expressiveness-vs-decidability.md | 命题 |  |
| Prop-S-26-01 | Struct/05-comparative-analysis/05.03-encoding-completeness-analysis.md | 命题 |  |
| Prop-S-29-01 | Struct/00-INDEX.md | 命题 |  |
| Prop-S-29-02 | Struct/00-INDEX.md | 命题 |  |
| Cor-S-02-01 | 良类型会话进程无死锁 | 推论 |  |
| Cor-S-02-04 | 流计算中，无界聚合操作（如全局SUM、COUNT）必然引入协调开销。 | 推论 | Struct/02-properties/02.06-calm-theorem.md |
| Cor-S-02-05 | 基于事件时间的窗口聚合可以通过Watermark机制延迟协调到窗口边界，而非每条记录都协调。 | 推论 | Struct/02-properties/02.06-calm-theorem.md |
| Cor-S-02-06 | 存在近似算法（如Count-Min Sketch、HyperLogLog）可以将非单调问题转化为单调的近似版本，从而避免协调。 | 推论 | Struct/02-properties/02.06-calm-theorem.md |
| Cor-S-04-01 | KNOWLEDGE-GRAPH-GUIDE.md | 推论 |  |
| Cor-S-04-02 | DESIGN-PRINCIPLES.md | 推论 |  |
| Cor-S-07-01 | (容错一致性)：满足 Thm-S-07-01 条件的流处理系统，在故障恢复后产生的输出与无故障连续执行的输出完全一致。 | 推论 | Struct/02-properties/02.01-determinism-in-streaming.md |
| Cor-S-07-02 | (回溯一致性)：对历史数据的重放（backfill）处理产生与原始处理相同的结果，支持结果版本化。 | 推论 | Struct/02-properties/02.01-determinism-in-streaming.md |
| Cor-S-07-03 | (并行度无关性)：在保持 KeyBy 分区语义的前提下，改变算子并行度（通过 Savepoint 恢复）不改变最终输出。 | 推论 | Struct/02-properties/02.01-determinism-in-streaming.md |
| Cor-S-14-01 | [可判定性递减推论] | 推论 | Struct/Proof-Chains-Relationships-Complete.md |
| Cor-S-15-01 | 互模拟等价类构成商LTS | 推论 |  |
| Cor-S-18-01 | (端到端 Exactly-Once 保证) | 推论 | Struct/00-STRUCT-DERIVATION-CHAIN.md |
| Cor-S-22-01 | Struct/04-proofs/04.06-dot-subtyping-completeness.md | 推论 |  |
| Cor-S-23-01 | Struct/04-proofs/04.07-deadlock-freedom-choreographic.md | 推论 |  |
| Cor-S-25-01 | Struct/05-comparative-analysis/05.02-expressiveness-vs-decidability.md | 推论 |  |
| Cor-S-25-02 | Struct/05-comparative-analysis/05.02-expressiveness-vs-decidability.md | 推论 |  |
| Cor-S-29-01 | Struct/06-frontier/06.03-ai-agent-session-types.md | 推论 |  |


## Knowledge 层级 (知识结构)

总计: 732 个形式化元素

### 按类型统计

| 类型 | 数量 |
|------|------|
| 定理 | 121 |
| 定义 | 344 |
| 引理 | 129 |
| 命题 | 137 |
| 推论 | 1 |

### 完整列表

| 编号 | 名称 | 类型 | 位置 |
|------|------|------|------|
| Thm-K-01-01 | Scala 流库的范畴论统一 | 定理 | Knowledge/Flink-Scala-Rust-Comprehensive/01-scala-ecosystem/01.01-scala-streaming-landscape.md |
| Thm-K-01-20 | Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md | 定理 |  |
| Thm-K-02-01 | (窗口聚合正确性条件) | 定理 | Knowledge/02-design-patterns/pattern-windowed-aggregation.md |
| Thm-K-02-02 | (日志关联完整性条件) | 定理 | Knowledge/02-design-patterns/pattern-log-analysis.md |
| Thm-K-02-03 | Credit-Based 流控安全性 | 定理 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.02-flink-runtime-deep-dive.md |
| Thm-K-02-04 | 反压传播完备性 | 定理 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.02-flink-runtime-deep-dive.md |
| Thm-K-02-05 | State Backend 选型完备性 | 定理 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.03-flink-state-backends.md |
| Thm-K-02-06 | ForSt 一致性保持 | 定理 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.03-flink-state-backends.md |
| Thm-K-02-07 | Table API 语义一致性 | 定理 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.04-flink-sql-table-api.md |
| Thm-K-02-08 | 物化表一致性保证 | 定理 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.04-flink-sql-table-api.md |
| Thm-K-02-09 | K8s 部署的稳定性保证 | 定理 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.05-flink-cloud-native.md |
| Thm-K-02-10 | 自动扩缩容的最优性 | 定理 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.05-flink-cloud-native.md |
| Thm-K-03-01 | 类型安全的互操作性 | 定理 | Knowledge/Flink-Scala-Rust-Comprehensive/01-scala-ecosystem/01.03-scala-java-api-interop.md |
| Thm-K-03-02 | 给定Netflix业务负载特征，Keystone平台满足： | 定理 | Knowledge/03-business-patterns/netflix-streaming-pipeline.md |
| Thm-K-03-03 | 双11实时计算SLA满足性 | 定理 |  |
| Thm-K-03-20 | Knowledge/03-business-patterns/data-mesh-streaming-architecture-2026.md | 定理 |  |
| Thm-K-03-50 | 实时数据最优定价定理 | 定理 | Knowledge/03-business-patterns/streaming-data-product-economics.md |
| Thm-K-03-51 | 数据网络效应价值定理 | 定理 | Knowledge/03-business-patterns/streaming-data-product-economics.md |
| Thm-K-03-52 | 多租户成本分摊定理 | 定理 | Knowledge/03-business-patterns/streaming-data-product-economics.md |
| Thm-K-04-01 | (流数据库vs流引擎选择定理) | 定理 | Knowledge/04-technology-selection/flink-vs-risingwave.md |
| Thm-K-04-02 | (2026流数据库选型定理) | 定理 | Knowledge/04-technology-selection/streaming-databases-2026-comparison.md |
| Thm-K-05-01 | 核心映射语义保持性定理 | 定理 | Knowledge/05-mapping-guides/struct-to-flink-mapping.md |
| Thm-K-05-15 | Streaming ETL工具生态关系定理 | 定理 | Knowledge/05-mapping-guides/streaming-etl-tools-landscape-2026.md |
| Thm-K-05-16 | Flink差异化定位定理 | 定理 | Knowledge/05-mapping-guides/streaming-etl-tools-landscape-2026.md |
| Thm-K-05-17 | 选型决策框架定理 | 定理 | Knowledge/05-mapping-guides/streaming-etl-tools-landscape-2026.md |
| Thm-K-05-21 | Knowledge/05-mapping-guides/streaming-sql-engines-2026-comparison.md | 定理 |  |
| Thm-K-05-24 | Knowledge/05-mapping-guides/streaming-sql-engines-2026-comparison.md | 定理 |  |
| Thm-K-05-26 | Knowledge/05-mapping-guides/streaming-sql-engines-2026-comparison.md | 定理 |  |
| Thm-K-05-31 | Agent编排+流处理混合架构定理 | 定理 | Knowledge/05-mapping-guides/multi-agent-frameworks-2026-comparison.md |
| Thm-K-05-32 | 选型决策定理 | 定理 | Knowledge/05-mapping-guides/multi-agent-frameworks-2026-comparison.md |
| Thm-K-06-01 | (快照一致性). RisingWave 提供的快照一致性保证：对于任意查询 $q$ 在时刻 $t_q$ 发出，系统返回结果 $R$ 满足： | 定理 | Knowledge/06-frontier/risingwave-deep-dive.md |
| Thm-K-06-02 | (RisingWave 快照一致性保证). RisingWave 的查询结果始终对应于某一历史时刻的全局一致状态。 | 定理 | Knowledge/06-frontier/risingwave-deep-dive.md |
| Thm-K-06-03 | (一致性模型蕴含关系). 设： | 定理 | Knowledge/06-frontier/risingwave-deep-dive.md |
| Thm-K-06-04 | 技术债务可持续管理定理 | 定理 | Knowledge/Flink-Scala-Rust-Comprehensive/06-trends-2026/06.02-adoption-roadmap.md |
| Thm-K-06-10 | 流式推理正确性定理 | 定理 | Knowledge/06-frontier/realtime-ai-inference-architecture.md |
| Thm-K-06-100 | (分层验证完备性) | 定理 | Knowledge/06-frontier/realtime-data-quality-validation.md |
| Thm-K-06-101 | (契约兼容性) | 定理 | Knowledge/06-frontier/realtime-data-quality-validation.md |
| Thm-K-06-102 | (DLQ完整性) | 定理 | Knowledge/06-frontier/realtime-data-quality-validation.md |
| Thm-K-06-105 | 主动-主动架构可行性定理 | 定理 |  |
| Thm-K-06-106 | 跨区域复制一致性边界定理 | 定理 |  |
| Thm-K-06-107 | 跨云延迟下界定理 | 定理 |  |
| Thm-K-06-11 | 延迟优化上限定理 | 定理 | Knowledge/06-frontier/realtime-ai-inference-architecture.md |
| Thm-K-06-110 | 流处理端到端安全协议的安全性 | 定理 | Knowledge/06-frontier/streaming-security-compliance.md |
| Thm-K-06-111 | 合规性验证的可判定性 | 定理 | Knowledge/06-frontier/streaming-security-compliance.md |
| Thm-K-06-112 | 密钥轮换期间的业务连续性 | 定理 | Knowledge/06-frontier/streaming-security-compliance.md |
| Thm-K-06-115 | (视图选择NP完全性). 给定查询工作负载 $\mathcal{Q}$ 和物化视图候选集 $\mathcal{C}$，在满足存储约束 $S_{budget}$ 的前提下最大化查询性能提升的视图选择问题是NP完全的。 | 定理 | Knowledge/06-frontier/streaming-materialized-view-architecture.md |
| Thm-K-06-116 | (流式物化视图一致性边界). 采用Barrier检查点机制的流式物化视图系统提供有界一致性： | 定理 | Knowledge/06-frontier/streaming-materialized-view-architecture.md |
| Thm-K-06-117 | (增量计算复杂度下界). 对于聚合查询类，增量维护的时间复杂度下界为： | 定理 | Knowledge/06-frontier/streaming-materialized-view-architecture.md |
| Thm-K-06-12 | 成本效益优化定理 | 定理 | Knowledge/06-frontier/realtime-ai-inference-architecture.md |
| Thm-K-06-120 | 流数据库物化视图的一致性保证 | 定理 | Knowledge/06-frontier/streaming-database-ecosystem-comparison.md |
| Thm-K-06-121 | 计算-存储分离架构的可扩展性定理 | 定理 | Knowledge/06-frontier/streaming-database-ecosystem-comparison.md |
| Thm-K-06-122 | 增量计算复杂度的下界 | 定理 | Knowledge/06-frontier/streaming-database-ecosystem-comparison.md |
| Thm-K-06-125 | [Flink边缘资源优化]: 在资源受限的边缘节点（内存 < 4GB）上，Flink 作业的最优配置满足： | 定理 | Knowledge/06-frontier/edge-streaming-architecture.md |
| Thm-K-06-126 | [断网容错保证]: 边缘流处理系统在网络分区期间的数据不丢失条件： | 定理 | Knowledge/06-frontier/edge-streaming-architecture.md |
| Thm-K-06-127 | [边缘-云数据一致性]: 采用 Delta Sync + CRDT 机制可实现边缘-云数据的最终一致性： | 定理 | Knowledge/06-frontier/edge-streaming-architecture.md |
| Thm-K-06-130 | 实时数据网格的 CAP 权衡 | 定理 | Knowledge/06-frontier/realtime-data-mesh-practice.md |
| Thm-K-06-131 | 数据契约验证的完备性 | 定理 | Knowledge/06-frontier/realtime-data-mesh-practice.md |
| Thm-K-06-132 | 血缘追踪的传递闭包 | 定理 | Knowledge/06-frontier/realtime-data-mesh-practice.md |
| Thm-K-06-140 | 在线-离线一致性保证定理 | 定理 | Knowledge/06-frontier/realtime-feature-store-architecture.md |
| Thm-K-06-141 | 特征服务延迟下界定理 | 定理 | Knowledge/06-frontier/realtime-feature-store-architecture.md |
| Thm-K-06-142 | 特征血缘变更传播定理 | 定理 | Knowledge/06-frontier/realtime-feature-store-architecture.md |
| Thm-K-06-145 | 流式上下文一致性定理 | 定理 | Knowledge/06-frontier/mcp-protocol-agent-streaming.md |
| Thm-K-06-146 | Tool 调用安全性定理 | 定理 | Knowledge/06-frontier/mcp-protocol-agent-streaming.md |
| Thm-K-06-147 | 流式更新完整性定理 | 定理 | Knowledge/06-frontier/mcp-protocol-agent-streaming.md |
| Thm-K-06-150 | A2A 任务完成可靠性定理 | 定理 | Knowledge/06-frontier/a2a-protocol-agent-communication.md |
| Thm-K-06-151 | A2A-MCP 正交性定理 | 定理 | Knowledge/06-frontier/a2a-protocol-agent-communication.md |
| Thm-K-06-152 | 流式 Artifact 完整性定理 | 定理 | Knowledge/06-frontier/a2a-protocol-agent-communication.md |
| Thm-K-06-155 | 多模态同步正确性定理 | 定理 | Knowledge/06-frontier/multimodal-streaming-architecture.md |
| Thm-K-06-156 | 延迟栈压缩效果定理 | 定理 | Knowledge/06-frontier/multimodal-streaming-architecture.md |
| Thm-K-06-157 | Barge-in响应性定理 | 定理 | Knowledge/06-frontier/multimodal-streaming-architecture.md |
| Thm-K-06-160 | 流平台选型决策定理 | 定理 | Knowledge/06-frontier/data-streaming-landscape-2025.md |
| Thm-K-06-161 | 部署模式成本边界定理 | 定理 | Knowledge/06-frontier/data-streaming-landscape-2025.md |
| Thm-K-06-162 | 流处理引擎能力完备性定理 | 定理 | Knowledge/06-frontier/data-streaming-landscape-2025.md |
| Thm-K-06-170 | DEX价格有效性定理 | 定理 | Knowledge/06-frontier/web3-streaming-analytics-defi.md |
| Thm-K-06-171 | 跨链一致性定理 | 定理 | Knowledge/06-frontier/web3-streaming-analytics-defi.md |
| Thm-K-06-172 | MEV检测完备性定理 | 定理 | Knowledge/06-frontier/web3-streaming-analytics-defi.md |
| Thm-K-06-20 | (流处理引擎选择决策定理) | 定理 | Knowledge/06-frontier/materialize-comparison-guide.md |
| Thm-K-06-240 | A2A互操作性定理 | 定理 |  |
| Thm-K-06-241 | A2A+MCP正交完备性定理 | 定理 |  |
| Thm-K-06-242 | 流式Task完整性定理 | 定理 |  |
| Thm-K-06-25 | Scale-to-Zero 延迟权衡定理 | 定理 | Knowledge/06-frontier/ai-agent-database-workloads.md |
| Thm-K-06-250 | A2A 互操作性定理 | 定理 | Knowledge/06-frontier/ai-agent-a2a-protocol.md |
| Thm-K-06-251 | A2A + MCP 正交完备性定理 | 定理 | Knowledge/06-frontier/ai-agent-a2a-protocol.md |
| Thm-K-06-252 | 流式 Task 完整性定理 | 定理 | Knowledge/06-frontier/ai-agent-a2a-protocol.md |
| Thm-K-06-40 | (实时多模态的必要性定理): 在以下应用场景中，多模态处理的延迟约束是刚性需求： | 定理 | Knowledge/06-frontier/multimodal-ai-streaming-architecture.md |
| Thm-K-06-50 | (链上流处理延迟下界): 任何基于区块链的实时处理系统，其端到端延迟 $\tau_{e2e}$ 满足： | 定理 | Knowledge/06-frontier/web3-blockchain-streaming-architecture.md |
| Thm-K-06-51 | (重组风险与一致性权衡): 设链重组概率为 $p_{reorg}$，则系统必须在一致性与延迟之间权衡： | 定理 | Knowledge/06-frontier/web3-blockchain-streaming-architecture.md |
| Thm-K-06-64 | Serverless流处理架构选型定理 | 定理 | Knowledge/06-frontier/serverless-stream-processing-architecture.md |
| Thm-K-06-80 | AI Agent流式响应实时性定理 | 定理 |  |
| Thm-K-06-90 | (流处理Data Mesh技术栈完备性)：一个生产级流处理Data Mesh平台需要满足以下能力矩阵： | 定理 | Knowledge/06-frontier/streaming-data-mesh-architecture.md |
| Thm-K-06-95 | 状态外置的一致性定理 | 定理 | Knowledge/06-frontier/serverless-streaming-architecture.md |
| Thm-K-06-96 | Serverless自动扩缩容响应时间定理 | 定理 | Knowledge/06-frontier/serverless-streaming-architecture.md |
| Thm-K-06-97 | 混合架构最优配置定理 | 定理 | Knowledge/06-frontier/serverless-streaming-architecture.md |
| Thm-K-06-98 | 成本监控预警完备性定理 | 定理 | Knowledge/06-frontier/serverless-streaming-cost-optimization.md |
| Thm-K-07-01 | 对于流处理作业 $J$，测试套件 $S$ 达到完全覆盖当且仅当： | 定理 | Knowledge/07-best-practices/07.07-testing-strategies-complete.md |
| Thm-K-07-02 | GPU TEE完整性定理 | 定理 |  |
| Thm-K-07-03 | GPU TEE远程证明正确性定理 | 定理 |  |
| Thm-K-07-04 | GPU流计算安全执行定理 | 定理 |  |
| Thm-K-08-01 | Lakehouse时间旅行一致性定理 | 定理 |  |
| Thm-K-08-02 | 流批一体ACID隔离性定理 | 定理 |  |
| Thm-K-08-03 | 元数据层一致性保证定理 | 定理 |  |
| Thm-K-08-04 | 增量处理正确性定理 | 定理 |  |
| Thm-K-08-15 | 流数据治理的必要性 | 定理 | Knowledge/08-standards/streaming-data-governance.md |
| Thm-K-08-20 | 实时质量监控的完备性定理 | 定理 | Knowledge/08-standards/streaming-data-governance-quality.md |
| Thm-K-08-21 | 流式 MDM 一致性定理 | 定理 | Knowledge/08-standards/streaming-data-governance-quality.md |
| Thm-K-08-22 | 合规删除的彻底性定理 | 定理 | Knowledge/08-standards/streaming-data-governance-quality.md |
| Thm-K-09-01 | RAG检索正确性定理 | 定理 |  |
| Thm-K-09-02 | RAG流式生成一致性定理 | 定理 |  |
| Thm-K-09-03 | 向量索引实时更新一致性定理 | 定理 |  |
| Thm-K-09-04 | RAG端到端正确性定理 | 定理 |  |
| Thm-K-10-201 | (吞吐量扩展性): 设单节点吞吐量为 $TPS_{single}$，节点数为 $N$，线性扩展系数为 $\alpha$（通常 $\alpha \in | 定理 | Knowledge/case-studies/ecommerce-realtime-recommendation-v2.md |
| Thm-K-10-202 | (特征一致性): Flink特征工程管道保证 Exactly-Once 语义，确保训练/推理特征一致性。 | 定理 | Knowledge/case-studies/ecommerce-realtime-recommendation-v2.md |
| Thm-K-10-211 | (吞吐量与设备数关系): 设每台电表上报频率为 $f$（次/秒），设备总数为 $N_d$，则系统需支持的总吞吐量为： | 定理 | Knowledge/case-studies/iot-smart-grid-case-study.md |
| Thm-K-10-212 | (系统可用性): 设各组件可用性为 $A_i$，则系统整体可用性： | 定理 | Knowledge/case-studies/iot-smart-grid-case-study.md |
| Thm-K-10-213 | (负荷预测准确性): 基于LSTM的短期负荷预测模型在典型场景下 MAPE < 3%。 | 定理 | Knowledge/case-studies/iot-smart-grid-case-study.md |
| Thm-K-10-221 | (延迟分解定理): 设各阶段延迟为 $L_i$，则总延迟满足： | 定理 | Knowledge/case-studies/fraud-detection-production-case.md |
| Thm-K-10-222 | (水平扩展性): 设节点数为 $N$，单节点吞吐为 $t$，则系统总吞吐： | 定理 | Knowledge/case-studies/fraud-detection-production-case.md |
| Thm-K-10-223 | (CEP检测完备性): 对于给定的CEP模式集合 $\mathcal{P}$，Flink CEP引擎能够检测所有满足模式约束的事件序列。 | 定理 | Knowledge/case-studies/fraud-detection-production-case.md |
| Thm-K-10-231 | (吞吐量扩展): 设每玩家每秒产生 $e$ 个事件，DAU为 $N_{DAU}$，在线率为 $\eta$，则事件吞吐需求： | 定理 | Knowledge/case-studies/gaming-analytics-platform-case.md |
| Thm-K-10-232 | (Exactly-Once语义): 通过两阶段提交，Flink + Kafka能够保证： | 定理 | Knowledge/case-studies/gaming-analytics-platform-case.md |
| Thm-K-10-233 | (实时指标准确性): 基于Flink窗口的实时指标计算，在保证Exactly-Once语义下，结果与批处理一致。 | 定理 | Knowledge/case-studies/gaming-analytics-platform-case.md |
| Def-K-01-01 | 流计算模型 (Streaming Computation Model) | 定义 | Knowledge/01-concept-atlas/streaming-models-mindmap.md |
| Def-K-01-02 | Dataflow 模型 | 定义 | Knowledge/01-concept-atlas/streaming-models-mindmap.md |
| Def-K-01-03 | Actor 模型 | 定义 | Knowledge/01-concept-atlas/streaming-models-mindmap.md |
| Def-K-01-04 | CSP (Communicating Sequential Processes) | 定义 | Knowledge/01-concept-atlas/streaming-models-mindmap.md |
| Def-K-01-05 | Pub/Sub (发布-订阅) | 定义 | Knowledge/01-concept-atlas/streaming-models-mindmap.md |
| Def-K-01-06 | CEP (Complex Event Processing) | 定义 | Knowledge/01-concept-atlas/streaming-models-mindmap.md |
| Def-K-01-07 | 微服务流 (Microservices Streaming) | 定义 | Knowledge/01-concept-atlas/streaming-models-mindmap.md |
| Def-K-01-08 | Knowledge/01-concept-atlas/concurrency-paradigms-matrix.md | 定义 |  |
| Def-K-01-09 | Knowledge/01-concept-atlas/concurrency-paradigms-matrix.md | 定义 |  |
| Def-K-01-10 | Knowledge/01-concept-atlas/concurrency-paradigms-matrix.md | 定义 |  |
| Def-K-01-11 | Knowledge/01-concept-atlas/concurrency-paradigms-matrix.md | 定义 |  |
| Def-K-01-40 | FINAL-COMPLETION-REPORT-v4.0.md | 定义 |  |
| Def-K-01-41 | Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md | 定义 |  |
| Def-K-01-42 | Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md | 定义 |  |
| Def-K-01-43 | Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md | 定义 |  |
| Def-K-01-44 | Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md | 定义 |  |
| Def-K-01-45 | Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md | 定义 |  |
| Def-K-01-46 | Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md | 定义 |  |
| Def-K-01-47 | Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md | 定义 |  |
| Def-K-01-48 | Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md | 定义 |  |
| Def-K-01-49 | Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md | 定义 |  |
| Def-K-01-54 | Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md | 定义 |  |
| Def-K-02-01 | (窗口分配器) | 定义 | Knowledge/02-design-patterns/pattern-windowed-aggregation.md |
| Def-K-02-02 | (窗口类型分类) | 定义 | Knowledge/02-design-patterns/pattern-windowed-aggregation.md |
| Def-K-02-03 | (触发器) | 定义 | Knowledge/02-design-patterns/pattern-windowed-aggregation.md |
| Def-K-02-04 | (驱逐器) | 定义 | Knowledge/02-design-patterns/pattern-windowed-aggregation.md |
| Def-K-02-05 | (异步 I/O 富化模式) | 定义 | Knowledge/02-design-patterns/pattern-async-io-enrichment.md |
| Def-K-02-06 | (AsyncFunction 接口) | 定义 | Knowledge/02-design-patterns/pattern-async-io-enrichment.md |
| Def-K-02-07 | (结果缓冲区) | 定义 | Knowledge/02-design-patterns/pattern-async-io-enrichment.md |
| Def-K-02-08 | (超时控制) | 定义 | Knowledge/02-design-patterns/pattern-async-io-enrichment.md |
| Def-K-02-09 | (多路输出拓扑) | 定义 | Knowledge/02-design-patterns/pattern-side-output.md |
| Def-K-02-10 | 特征新鲜度 (Feature Freshness) | 定义 | Knowledge/02-design-patterns/pattern-realtime-feature-engineering.md |
| Def-K-02-11 | 窗口特征聚合 (Windowed Feature Aggregation) | 定义 | Knowledge/02-design-patterns/pattern-realtime-feature-engineering.md |
| Def-K-02-12 | 特征存储 (Feature Store) | 定义 | Knowledge/02-design-patterns/pattern-realtime-feature-engineering.md |
| Def-K-02-13 | (日志流模式) | 定义 | Knowledge/02-design-patterns/pattern-log-analysis.md |
| Def-K-02-14 | (日志结构化) | 定义 | Knowledge/02-design-patterns/pattern-log-analysis.md |
| Def-K-02-15 | (日志聚合与关联) | 定义 | Knowledge/02-design-patterns/pattern-log-analysis.md |
| Def-K-02-16 | Materialized Table (物化表) | 定义 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.04-flink-sql-table-api.md |
| Def-K-02-17 | Model DDL (Flink 2.2) | 定义 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.04-flink-sql-table-api.md |
| Def-K-02-18 | 流批一体语义 | 定义 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.04-flink-sql-table-api.md |
| Def-K-02-19 | Kubernetes Native Integration | 定义 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.05-flink-cloud-native.md |
| Def-K-02-20 | 自动扩缩容 (Autoscaling) | 定义 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.05-flink-cloud-native.md |
| Def-K-02-21 | 云存储集成 | 定义 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.05-flink-cloud-native.md |
| Def-K-02-22 | Serverless 部署模式 | 定义 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.05-flink-cloud-native.md |
| Def-K-03-01 | IoT 数据流 (IoT Data Stream) | 定义 | Knowledge/03-business-patterns/iot-stream-processing.md |
| Def-K-03-02 | 设备会话 (Device Session) | 定义 | Knowledge/03-business-patterns/iot-stream-processing.md |
| Def-K-03-03 | 游戏事件 (Game Event) | 定义 | Knowledge/03-business-patterns/gaming-analytics.md |
| Def-K-03-04 | 实时排行榜 (Real-time Leaderboard) | 定义 | Knowledge/03-business-patterns/gaming-analytics.md |
| Def-K-03-05 | 反作弊检测 (Anti-Cheat Detection) | 定义 | Knowledge/03-business-patterns/gaming-analytics.md |
| Def-K-03-06 | 玩家会话 (Player Session) | 定义 | Knowledge/03-business-patterns/gaming-analytics.md |
| Def-K-03-07 | 动态定价 (Surge Pricing) | 定义 | Knowledge/03-business-patterns/uber-realtime-platform.md |
| Def-K-03-08 | Netflix数据管道 (Netflix Data Pipeline) | 定义 | Knowledge/03-business-patterns/netflix-streaming-pipeline.md |
| Def-K-03-09 | Keystone平台 (Keystone Platform) | 定义 | Knowledge/03-business-patterns/netflix-streaming-pipeline.md |
| Def-K-03-10 | 实时推荐特征 (Real-time Recommendation Features) | 定义 | Knowledge/03-business-patterns/netflix-streaming-pipeline.md |
| Def-K-03-11 | 双11实时计算架构 | 定义 | Knowledge/03-business-patterns/alibaba-double11-flink.md |
| Def-K-03-12 | 每秒40亿+ TPS处理 | 定义 | Knowledge/03-business-patterns/alibaba-double11-flink.md |
| Def-K-03-13 | 全球数据中心协同 | 定义 | Knowledge/03-business-patterns/alibaba-double11-flink.md |
| Def-K-03-14 | Stripe支付事件流 | 定义 | Knowledge/03-business-patterns/stripe-payment-processing.md |
| Def-K-03-15 | 实时风控决策系统 | 定义 | Knowledge/03-business-patterns/stripe-payment-processing.md |
| Def-K-03-16 | 账单实时分析引擎 | 定义 | Knowledge/03-business-patterns/stripe-payment-processing.md |
| Def-K-03-17 | 音乐播放事件流 | 定义 | Knowledge/03-business-patterns/spotify-music-recommendation.md |
| Def-K-03-18 | 实时会话分析引擎 | 定义 | Knowledge/03-business-patterns/spotify-music-recommendation.md |
| Def-K-03-19 | 个性化播放列表生成器 | 定义 | Knowledge/03-business-patterns/spotify-music-recommendation.md |
| Def-K-03-20 | Airbnb双边市场事件流 | 定义 | Knowledge/03-business-patterns/airbnb-marketplace-dynamics.md |
| Def-K-03-21 | 动态定价引擎 | 定义 | Knowledge/03-business-patterns/airbnb-marketplace-dynamics.md |
| Def-K-03-22 | 实时搜索排序系统 | 定义 | Knowledge/03-business-patterns/airbnb-marketplace-dynamics.md |
| Def-K-03-30 | FINAL-COMPLETION-REPORT-v4.0.md | 定义 |  |
| Def-K-03-31 | Knowledge/03-business-patterns/data-mesh-streaming-architecture-2026.md | 定义 |  |
| Def-K-03-32 | Knowledge/03-business-patterns/data-mesh-streaming-architecture-2026.md | 定义 |  |
| Def-K-03-33 | Knowledge/03-business-patterns/data-mesh-streaming-architecture-2026.md | 定义 |  |
| Def-K-03-34 | Knowledge/03-business-patterns/data-mesh-streaming-architecture-2026.md | 定义 |  |
| Def-K-03-35 | Knowledge/03-business-patterns/data-mesh-streaming-architecture-2026.md | 定义 |  |
| Def-K-03-50 | Data Product Economics | 定义 | Knowledge/03-business-patterns/streaming-data-product-economics.md |
| Def-K-03-51 | Data Monetization Models | 定义 | Knowledge/03-business-patterns/streaming-data-product-economics.md |
| Def-K-03-52 | Real-time Data Pricing | 定义 | Knowledge/03-business-patterns/streaming-data-product-economics.md |
| Def-K-03-53 | Data Value Scoring | 定义 | Knowledge/03-business-patterns/streaming-data-product-economics.md |
| Def-K-03-54 | Data Marketplace Mechanics | 定义 | Knowledge/03-business-patterns/streaming-data-product-economics.md |
| Def-K-03-55 | Streaming Data ROI | 定义 | Knowledge/03-business-patterns/streaming-data-product-economics.md |
| Def-K-04-01 | fs2 (Functional Streams for Scala) | 定义 | Knowledge/Flink-Scala-Rust-Comprehensive/01-scala-ecosystem/01.04-fs2-pekko-streams.md |
| Def-K-04-02 | Pekko Streams (Reactive Streams 实现) | 定义 | Knowledge/Flink-Scala-Rust-Comprehensive/01-scala-ecosystem/01.04-fs2-pekko-streams.md |
| Def-K-04-03 | Pull-based vs Push-based 流模型 | 定义 | Knowledge/Flink-Scala-Rust-Comprehensive/01-scala-ecosystem/01.04-fs2-pekko-streams.md |
| Def-K-04-04 | Knowledge/04-technology-selection/engine-selection-guide.md | 定义 |  |
| Def-K-04-05 | Knowledge/04-technology-selection/engine-selection-guide.md | 定义 |  |
| Def-K-04-06 | Knowledge/04-technology-selection/engine-selection-guide.md | 定义 |  |
| Def-K-04-07 | Knowledge/04-technology-selection/engine-selection-guide.md | 定义 |  |
| Def-K-04-08 | Knowledge/04-technology-selection/engine-selection-guide.md | 定义 |  |
| Def-K-04-09 | Knowledge/04-technology-selection/engine-selection-guide.md | 定义 |  |
| Def-K-04-10 | (流处理引擎架构模型) | 定义 | Knowledge/04-technology-selection/flink-vs-risingwave.md |
| Def-K-04-11 | (状态存储架构分类) | 定义 | Knowledge/04-technology-selection/flink-vs-risingwave.md |
| Def-K-04-12 | (流数据库定义) | 定义 | Knowledge/04-technology-selection/flink-vs-risingwave.md |
| Def-K-04-13 | Knowledge/04-technology-selection/streaming-database-guide.md | 定义 |  |
| Def-K-04-14 | Knowledge/04-technology-selection/streaming-database-guide.md | 定义 |  |
| Def-K-04-15 | Knowledge/04-technology-selection/streaming-database-guide.md | 定义 |  |
| Def-K-04-16 | Knowledge/04-technology-selection/streaming-database-guide.md | 定义 |  |
| Def-K-04-17 | Knowledge/04-technology-selection/streaming-database-guide.md | 定义 |  |
| Def-K-04-18 | Knowledge/04-technology-selection/streaming-database-guide.md | 定义 |  |
| Def-K-04-19 | Knowledge/04-technology-selection/streaming-database-guide.md | 定义 |  |
| Def-K-04-20 | (流数据库分类体系) | 定义 | Knowledge/04-technology-selection/streaming-databases-2026-comparison.md |
| Def-K-04-21 | (存算分离架构形式化定义) | 定义 | Knowledge/04-technology-selection/streaming-databases-2026-comparison.md |
| Def-K-04-22 | (物化视图维护机制) | 定义 | Knowledge/04-technology-selection/streaming-databases-2026-comparison.md |
| Def-K-04-23 | (增量计算引擎) | 定义 | Knowledge/04-technology-selection/streaming-databases-2026-comparison.md |
| Def-K-05-01 | 形式化到实现映射 | 定义 | Knowledge/05-mapping-guides/struct-to-flink-mapping.md |
| Def-K-05-02 | 语义保持性 (Semantic Preservation) | 定义 | Knowledge/05-mapping-guides/struct-to-flink-mapping.md |
| Def-K-05-03 | 实现近似性 (Implementation Approximation) | 定义 | Knowledge/05-mapping-guides/struct-to-flink-mapping.md |
| Def-K-05-04 | 验证金字塔 | 定义 | Knowledge/05-mapping-guides/theory-to-code-patterns.md |
| Def-K-05-05 | API 兼容性矩阵 (API Compatibility Matrix) | 定义 | Knowledge/Flink-Scala-Rust-Comprehensive/05-architecture-patterns/05.02-migration-strategies.md |
| Def-K-05-06 | 数据验证契约 (Data Validation Contract) | 定义 | Knowledge/Flink-Scala-Rust-Comprehensive/05-architecture-patterns/05.02-migration-strategies.md |
| Def-K-05-07 | 云原生流处理部署模型 (Cloud-Native Stream Processing Deployment Model) | 定义 | Knowledge/Flink-Scala-Rust-Comprehensive/05-architecture-patterns/05.03-cloud-deployment.md |
| Def-K-05-08 | 自动扩缩容策略 (Auto-scaling Policy) | 定义 | Knowledge/Flink-Scala-Rust-Comprehensive/05-architecture-patterns/05.03-cloud-deployment.md |
| Def-K-05-09 | 多环境部署拓扑 (Multi-Environment Deployment Topology) | 定义 | Knowledge/Flink-Scala-Rust-Comprehensive/05-architecture-patterns/05.03-cloud-deployment.md |
| Def-K-05-10 | 边缘-云协同流处理架构 (Edge-Cloud Collaborative Stream Processing Architecture) | 定义 | Knowledge/Flink-Scala-Rust-Comprehensive/05-architecture-patterns/05.04-edge-computing.md |
| Def-K-05-11 | 资源受限执行环境 (Resource-Constrained Execution Environment) | 定义 | Knowledge/Flink-Scala-Rust-Comprehensive/05-architecture-patterns/05.04-edge-computing.md |
| Def-K-05-12 | 离线容忍度 (Offline Tolerance) | 定义 | Knowledge/Flink-Scala-Rust-Comprehensive/05-architecture-patterns/05.04-edge-computing.md |
| Def-K-05-30 | Streaming ETL形式化定义 | 定义 | Knowledge/05-mapping-guides/streaming-etl-tools-landscape-2026.md |
| Def-K-05-31 | 工具分类学 | 定义 | Knowledge/05-mapping-guides/streaming-etl-tools-landscape-2026.md |
| Def-K-05-32 | 核心指标维度 | 定义 | Knowledge/05-mapping-guides/streaming-etl-tools-landscape-2026.md |
| Def-K-05-40 | FINAL-COMPLETION-REPORT-v4.0.md | 定义 |  |
| Def-K-05-41 | Knowledge/05-mapping-guides/streaming-sql-engines-2026-comparison.md | 定义 |  |
| Def-K-05-42 | Knowledge/05-mapping-guides/streaming-sql-engines-2026-comparison.md | 定义 |  |
| Def-K-05-43 | Knowledge/05-mapping-guides/streaming-sql-engines-2026-comparison.md | 定义 |  |
| Def-K-05-51 | Multi-Agent系统 (MAS) | 定义 | Knowledge/05-mapping-guides/multi-agent-frameworks-2026-comparison.md |
| Def-K-05-52 | Agent编排框架 | 定义 | Knowledge/05-mapping-guides/multi-agent-frameworks-2026-comparison.md |
| Def-K-05-53 | 编排模型分类 | 定义 | Knowledge/05-mapping-guides/multi-agent-frameworks-2026-comparison.md |
| Def-K-05-54 | LangGraph状态机 | 定义 | Knowledge/05-mapping-guides/multi-agent-frameworks-2026-comparison.md |
| Def-K-05-55 | CrewAI核心抽象 | 定义 | Knowledge/05-mapping-guides/multi-agent-frameworks-2026-comparison.md |
| Def-K-05-56 | AutoGen核心抽象 | 定义 | Knowledge/05-mapping-guides/multi-agent-frameworks-2026-comparison.md |
| Def-K-05-57 | 分层架构模式 | 定义 | Knowledge/05-mapping-guides/multi-agent-frameworks-2026-comparison.md |
| Def-K-05-58 | LangGraph研究管道实现 | 定义 | Knowledge/05-mapping-guides/multi-agent-frameworks-2026-comparison.md |
| Def-K-05-59 | CrewAI研究管道实现 | 定义 | Knowledge/05-mapping-guides/multi-agent-frameworks-2026-comparison.md |
| Def-K-05-60 | AutoGen研究管道实现 | 定义 | Knowledge/05-mapping-guides/multi-agent-frameworks-2026-comparison.md |
| Def-K-06-01 | (RisingWave 系统架构). RisingWave 是一个分布式流处理数据库系统，其架构可形式化定义为五元组： | 定义 | Knowledge/06-frontier/risingwave-deep-dive.md |
| Def-K-06-02 | (无状态计算节点). 计算节点 $\mathcal{N}_{compute}$ 被定义为逻辑无状态的，当且仅当： | 定义 | Knowledge/06-frontier/risingwave-deep-dive.md |
| Def-K-06-03 | (有状态存储节点 - Hummock). Hummock 存储引擎是一个基于 LSM-Tree 的云原生键值存储，形式化为： | 定义 | Knowledge/06-frontier/risingwave-deep-dive.md |
| Def-K-06-04 | (增量视图维护). 给定基础表 $B$ 和物化视图定义查询 $Q$，增量维护机制 $\mathcal{I}$ 定义为： | 定义 | Knowledge/06-frontier/risingwave-deep-dive.md |
| Def-K-06-05 | FaaS Dataflow | 定义 | Knowledge/06-frontier/faas-dataflow.md |
| Def-K-06-06 | 云边端连续体 (Cloud-Edge-Device Continuum) | 定义 | Knowledge/06-frontier/faas-dataflow.md |
| Def-K-06-07 | 自适应工作流放置 | 定义 | Knowledge/06-frontier/faas-dataflow.md |
| Def-K-06-08 | Cloud-Edge Continuum (云边端连续体) | 定义 | Knowledge/06-frontier/cloud-edge-continuum.md |
| Def-K-06-09 | 雾计算 (Fog Computing) | 定义 | Knowledge/06-frontier/cloud-edge-continuum.md |
| Def-K-06-10 | 计算卸载 (Computation Offloading) | 定义 | Knowledge/06-frontier/cloud-edge-continuum.md |
| Def-K-06-101 | 实时数据产品 (Real-time Data Product) | 定义 | Knowledge/06-frontier/realtime-data-product-architecture.md |
| Def-K-06-102 | 流式数据产品接口 (Streaming Data Product Interface) | 定义 | Knowledge/06-frontier/realtime-data-product-architecture.md |
| Def-K-06-103 | 领域数据所有权 (Domain Data Ownership) | 定义 | Knowledge/06-frontier/realtime-data-product-architecture.md |
| Def-K-06-104 | 联邦计算治理 (Federated Computational Governance) | 定义 | Knowledge/06-frontier/realtime-data-product-architecture.md |
| Def-K-06-11 | 自适应放置策略 (Adaptive Placement Policy) | 定义 | Knowledge/06-frontier/cloud-edge-continuum.md |
| Def-K-06-110 | AI Agent (人工智能代理) | 定义 | Knowledge/06-frontier/ai-agent-streaming-architecture.md |
| Def-K-06-111 | Agent架构模式 (Agent Architecture Patterns) | 定义 | Knowledge/06-frontier/ai-agent-streaming-architecture.md |
| Def-K-06-112 | Agent记忆系统 (Agent Memory System) | 定义 | Knowledge/06-frontier/ai-agent-streaming-architecture.md |
| Def-K-06-113 | 流式Agent触发 (Streaming Agent Trigger) | 定义 | Knowledge/06-frontier/ai-agent-streaming-architecture.md |
| Def-K-06-114 | 多Agent编排架构 (Multi-Agent Orchestration) | 定义 | Knowledge/06-frontier/ai-agent-streaming-architecture.md |
| Def-K-06-115 | Agent状态机 (Agent State Machine) | 定义 | Knowledge/06-frontier/ai-agent-streaming-architecture.md |
| Def-K-06-116 | 工具调用流编排 (Tool Calling Flow Orchestration) | 定义 | Knowledge/06-frontier/ai-agent-streaming-architecture.md |
| Def-K-06-117 | 记忆流式更新协议 (Memory Streaming Update Protocol) | 定义 | Knowledge/06-frontier/ai-agent-streaming-architecture.md |
| Def-K-06-12 | 边缘计算 (Edge Computing) | 定义 | Knowledge/06-frontier/edge-streaming-patterns.md |
| Def-K-06-120 | (Data Mesh)：Data Mesh是一种去中心化的数据架构范式，将数据视为由独立域团队拥有和运营的产品，通过自服务平台和联邦治理实现大规模数据价值交付。 | 定义 | Knowledge/06-frontier/streaming-data-mesh-architecture.md |
| Def-K-06-121 | (实时数据产品)：实时数据产品是一种特殊的数据产品，其数据新鲜度满足时延约束 $T_{latency} \leq T_{SLO}$，形式化定义为： | 定义 | Knowledge/06-frontier/streaming-data-mesh-architecture.md |
| Def-K-06-122 | (流数据域)：流数据域 $\mathcal{D}_s$ 是围绕业务事件流定义的领域边界，满足： | 定义 | Knowledge/06-frontier/streaming-data-mesh-architecture.md |
| Def-K-06-123 | (Data Contract)：数据契约是流数据产品与其消费者之间的形式化协议： | 定义 | Knowledge/06-frontier/streaming-data-mesh-architecture.md |
| Def-K-06-13 | 边缘流处理延迟层级 (Edge Latency Hierarchy) | 定义 | Knowledge/06-frontier/edge-streaming-patterns.md |
| Def-K-06-130 | Serverless流处理系统 | 定义 | Knowledge/06-frontier/serverless-streaming-architecture.md |
| Def-K-06-131 | 冷启动与热启动 | 定义 | Knowledge/06-frontier/serverless-streaming-architecture.md |
| Def-K-06-132 | 状态外置模式 (Externalized State Pattern) | 定义 | Knowledge/06-frontier/serverless-streaming-architecture.md |
| Def-K-06-133 | 事件驱动函数链 | 定义 | Knowledge/06-frontier/serverless-streaming-architecture.md |
| Def-K-06-134 | Serverless Checkpoint机制 | 定义 | Knowledge/06-frontier/serverless-streaming-architecture.md |
| Def-K-06-135 | 混合架构模型 | 定义 | Knowledge/06-frontier/serverless-streaming-architecture.md |
| Def-K-06-14 | WebAssembly 边缘运行时 (Wasm Edge Runtime) | 定义 | Knowledge/06-frontier/edge-streaming-patterns.md |
| Def-K-06-140 | (数据质量维度) | 定义 | Knowledge/06-frontier/realtime-data-quality-validation.md |
| Def-K-06-141 | (流数据质量损失函数) | 定义 | Knowledge/06-frontier/realtime-data-quality-validation.md |
| Def-K-06-142 | (数据契约) | 定义 | Knowledge/06-frontier/realtime-data-quality-validation.md |
| Def-K-06-143 | (数据可观测性) | 定义 | Knowledge/06-frontier/realtime-data-quality-validation.md |
| Def-K-06-15 | Flink 边缘部署模式 (Flink Edge Deployment) | 定义 | Knowledge/06-frontier/edge-streaming-patterns.md |
| Def-K-06-150 | 多云流处理架构 (Multi-Cloud Streaming Architecture) | 定义 | Knowledge/06-frontier/multi-cloud-streaming-architecture.md |
| Def-K-06-151 | 跨区域复制模式 (Cross-Region Replication Pattern) | 定义 | Knowledge/06-frontier/multi-cloud-streaming-architecture.md |
| Def-K-06-152 | 主动-主动架构 (Active-Active Architecture) | 定义 | Knowledge/06-frontier/multi-cloud-streaming-architecture.md |
| Def-K-06-153 | 主动-被动架构 (Active-Passive Architecture) | 定义 | Knowledge/06-frontier/multi-cloud-streaming-architecture.md |
| Def-K-06-154 | RPO/RTO (Recovery Point/Time Objective) | 定义 | Knowledge/06-frontier/multi-cloud-streaming-architecture.md |
| Def-K-06-155 | 零信任网络 (Zero Trust Network) | 定义 | Knowledge/06-frontier/multi-cloud-streaming-architecture.md |
| Def-K-06-16 | 边缘流处理模式 (Edge Streaming Patterns) | 定义 | Knowledge/06-frontier/edge-streaming-patterns.md |
| Def-K-06-160 | 流处理安全威胁模型 (Streaming Security Threat Model) | 定义 | Knowledge/06-frontier/streaming-security-compliance.md |
| Def-K-06-161 | CIA三元组在流处理中的形式化定义 | 定义 | Knowledge/06-frontier/streaming-security-compliance.md |
| Def-K-06-162 | 传输安全协议栈 (Transport Security Stack) | 定义 | Knowledge/06-frontier/streaming-security-compliance.md |
| Def-K-06-163 | 数据安全生命周期 (Data Security Lifecycle) | 定义 | Knowledge/06-frontier/streaming-security-compliance.md |
| Def-K-06-164 | 访问控制模型 (Access Control Models) | 定义 | Knowledge/06-frontier/streaming-security-compliance.md |
| Def-K-06-165 | 合规框架映射 (Compliance Framework Mapping) | 定义 | Knowledge/06-frontier/streaming-security-compliance.md |
| Def-K-06-17 | 基于关系的访问控制 (ReBAC) | 定义 | Knowledge/06-frontier/streaming-access-control.md |
| Def-K-06-170 | (物化视图). 给定基础表集合 $\mathcal{B} = \{B_1, B_2, ..., B_n\}$ 和视图定义查询 $Q$，物化视图 $V$ 定义为： | 定义 | Knowledge/06-frontier/streaming-materialized-view-architecture.md |
| Def-K-06-171 | (传统物化视图 vs 流式物化视图). 两类物化视图的形式化对比： | 定义 | Knowledge/06-frontier/streaming-materialized-view-architecture.md |
| Def-K-06-172 | (增量视图维护 IVM). 增量视图维护机制 $\mathcal{I}$ 定义为映射函数： | 定义 | Knowledge/06-frontier/streaming-materialized-view-architecture.md |
| Def-K-06-173 | (计算-存储分离架构). 流式物化视图系统架构定义为四元组： | 定义 | Knowledge/06-frontier/streaming-materialized-view-architecture.md |
| Def-K-06-174 | (级联物化视图). 级联物化视图是由视图依赖关系构成的有向无环图 $DAG = (\mathcal{V}, \mathcal{E})$： | 定义 | Knowledge/06-frontier/streaming-materialized-view-architecture.md |
| Def-K-06-175 | (流式一致性模型). 流式物化视图的一致性级别定义： | 定义 | Knowledge/06-frontier/streaming-materialized-view-architecture.md |
| Def-K-06-18 | 数据血缘与策略传播 (Data Lineage & Policy Propagation) {#def-k-06-18-数据血缘与策略传播-data-lineage--policy-propagation} | 定义 | Knowledge/06-frontier/streaming-access-control.md |
| Def-K-06-180 | 流数据库系统 (Streaming Database System) | 定义 | Knowledge/06-frontier/streaming-database-ecosystem-comparison.md |
| Def-K-06-181 | 计算-存储分离架构 (Compute-Storage Separation) | 定义 | Knowledge/06-frontier/streaming-database-ecosystem-comparison.md |
| Def-K-06-182 | 增量计算视图 (Incremental Computed View) | 定义 | Knowledge/06-frontier/streaming-database-ecosystem-comparison.md |
| Def-K-06-183 | 流SQL方言 (Streaming SQL Dialect) | 定义 | Knowledge/06-frontier/streaming-database-ecosystem-comparison.md |
| Def-K-06-184 | CDC源连接器 (CDC Source Connector) | 定义 | Knowledge/06-frontier/streaming-database-ecosystem-comparison.md |
| Def-K-06-185 | 向量化执行引擎 (Vectorized Execution Engine) | 定义 | Knowledge/06-frontier/streaming-database-ecosystem-comparison.md |
| Def-K-06-19 | 服务水平指标 (Service Level Indicator, SLI) | 定义 | Knowledge/06-frontier/streaming-slo-definition.md |
| Def-K-06-190 | [边缘流处理]: 边缘流处理是指在数据源产生地或其邻近的计算节点上，对连续到达的数据流进行实时处理、过滤、聚合和推理的计算范式。形式上，边缘流处理系统可建模为六元组： | 定义 | Knowledge/06-frontier/edge-streaming-architecture.md |
| Def-K-06-191 | [边缘计算延迟模型]: 边缘流处理的端到端延迟由以下组件构成： | 定义 | Knowledge/06-frontier/edge-streaming-architecture.md |
| Def-K-06-192 | [边缘-云协同层级]: | 定义 | Knowledge/06-frontier/edge-streaming-architecture.md |
| Def-K-06-193 | [边缘部署决策函数]: 给定应用特征向量 $\vec{A} = (d_{latency}, v_{data}, c_{compute}, r_{reliability})$，边缘部署决策为： | 定义 | Knowledge/06-frontier/edge-streaming-architecture.md |
| Def-K-06-194 | [离线优先约束]: 离线优先架构必须满足 CAP 变体——在断网场景下优先保证 可用性(A) 和 分区容忍性(P)，通过最终一致性实现数据同步： | 定义 | Knowledge/06-frontier/edge-streaming-architecture.md |
| Def-K-06-195 | [边缘运维自动化]: 边缘运维复杂度随节点数 $N$ 呈亚线性增长： | 定义 | Knowledge/06-frontier/edge-streaming-architecture.md |
| Def-K-06-20 | (Materialize系统架构) | 定义 | Knowledge/06-frontier/materialize-comparison-guide.md |
| Def-K-06-200 | 多Agent流式编排 (Multi-Agent Streaming Orchestration) | 定义 | Knowledge/06-frontier/multi-agent-streaming-orchestration.md |
| Def-K-06-201 | Agent角色类型 (Agent Role Types) | 定义 | Knowledge/06-frontier/multi-agent-streaming-orchestration.md |
| Def-K-06-202 | 协作模式拓扑 (Collaboration Topology Patterns) | 定义 | Knowledge/06-frontier/multi-agent-streaming-orchestration.md |
| Def-K-06-203 | 流式任务调度 (Streaming Task Scheduling) | 定义 | Knowledge/06-frontier/multi-agent-streaming-orchestration.md |
| Def-K-06-204 | Agent能力协商协议 (Agent Capability Negotiation) | 定义 | Knowledge/06-frontier/multi-agent-streaming-orchestration.md |
| Def-K-06-205 | 自服务数据平台 (Self-serve Data Platform) | 定义 | Knowledge/06-frontier/realtime-data-mesh-practice.md |
| Def-K-06-21 | (Differential Dataflow形式化定义) | 定义 | Knowledge/06-frontier/materialize-comparison-guide.md |
| Def-K-06-210 | 特征平台 (Feature Store) | 定义 | Knowledge/06-frontier/realtime-feature-store-architecture.md |
| Def-K-06-211 | 实时特征 vs 离线特征 | 定义 | Knowledge/06-frontier/realtime-feature-store-architecture.md |
| Def-K-06-212 | 在线-离线一致性 (Training-Serving Skew) | 定义 | Knowledge/06-frontier/realtime-feature-store-architecture.md |
| Def-K-06-213 | Point-in-Time 正确性 | 定义 | Knowledge/06-frontier/realtime-feature-store-architecture.md |
| Def-K-06-214 | 特征血缘 (Feature Lineage) | 定义 | Knowledge/06-frontier/realtime-feature-store-architecture.md |
| Def-K-06-215 | 特征服务 API (Feature Service) | 定义 | Knowledge/06-frontier/realtime-feature-store-architecture.md |
| Def-K-06-22 | (严格序列化一致性) | 定义 | Knowledge/06-frontier/materialize-comparison-guide.md |
| Def-K-06-220 | Model Context Protocol (MCP) | 定义 | Knowledge/06-frontier/mcp-protocol-agent-streaming.md |
| Def-K-06-221 | MCP Server | 定义 | Knowledge/06-frontier/mcp-protocol-agent-streaming.md |
| Def-K-06-222 | MCP Client | 定义 | Knowledge/06-frontier/mcp-protocol-agent-streaming.md |
| Def-K-06-223 | Resources 与 Tools | 定义 | Knowledge/06-frontier/mcp-protocol-agent-streaming.md |
| Def-K-06-224 | Streaming Context Flow | 定义 | Knowledge/06-frontier/mcp-protocol-agent-streaming.md |
| Def-K-06-225 | Agent 工作流编排 | 定义 | Knowledge/06-frontier/mcp-protocol-agent-streaming.md |
| Def-K-06-23 | (SQL流处理方言分类) | 定义 | Knowledge/06-frontier/materialize-comparison-guide.md |
| Def-K-06-230 | Agent-to-Agent Protocol (A2A) | 定义 | Knowledge/06-frontier/a2a-protocol-agent-communication.md |
| Def-K-06-231 | Agent Card (能力卡片) | 定义 | Knowledge/06-frontier/a2a-protocol-agent-communication.md |
| Def-K-06-232 | Task 生命周期 | 定义 | Knowledge/06-frontier/a2a-protocol-agent-communication.md |
| Def-K-06-233 | Message 与 Part | 定义 | Knowledge/06-frontier/a2a-protocol-agent-communication.md |
| Def-K-06-234 | Artifact (任务产出) | 定义 | Knowledge/06-frontier/a2a-protocol-agent-communication.md |
| Def-K-06-235 | A2A 与流处理集成模型 | 定义 | Knowledge/06-frontier/a2a-protocol-agent-communication.md |
| Def-K-06-24 | 增量提交与 Changelog | 定义 | Knowledge/06-frontier/streaming-lakehouse-iceberg-delta.md |
| Def-K-06-240 | Agent-to-Agent Protocol (A2A) - 形式化定义 | 定义 | Knowledge/06-frontier/ai-agent-a2a-protocol.md |
| Def-K-06-241 | Agent 拓扑与角色模型 | 定义 | Knowledge/06-frontier/ai-agent-a2a-protocol.md |
| Def-K-06-242 | Task 生命周期状态机 | 定义 | Knowledge/06-frontier/ai-agent-a2a-protocol.md |
| Def-K-06-243 | Agent Card - 能力描述本体 | 定义 | Knowledge/06-frontier/ai-agent-a2a-protocol.md |
| Def-K-06-244 | Artifact - 多模态产出物 | 定义 | Knowledge/06-frontier/ai-agent-a2a-protocol.md |
| Def-K-06-245 | Multimodal Context Window | 定义 | Knowledge/06-frontier/multimodal-streaming-architecture.md |
| Def-K-06-25 | 统一批流存储 | 定义 | Knowledge/06-frontier/streaming-lakehouse-iceberg-delta.md |
| Def-K-06-250 | 数据流平台 (Data Streaming Platform) | 定义 | Knowledge/06-frontier/data-streaming-landscape-2025.md |
| Def-K-06-251 | 流处理语义分类 | 定义 | Knowledge/06-frontier/data-streaming-landscape-2025.md |
| Def-K-06-252 | 部署模式分类 | 定义 | Knowledge/06-frontier/data-streaming-landscape-2025.md |
| Def-K-06-253 | 存算分离架构 (Storage-Compute Separation) | 定义 | Knowledge/06-frontier/data-streaming-landscape-2025.md |
| Def-K-06-254 | 流处理引擎核心指标 | 定义 | Knowledge/06-frontier/data-streaming-landscape-2025.md |
| Def-K-06-255 | Streaming Database | 定义 | Knowledge/06-frontier/data-streaming-landscape-2025.md |
| Def-K-06-26 | RAG管道 (RAG Pipeline) | 定义 | Knowledge/06-frontier/real-time-rag-architecture.md |
| Def-K-06-260 | Web3 Streaming Data | 定义 | Knowledge/06-frontier/web3-streaming-analytics-defi.md |
| Def-K-06-261 | DeFi Streaming Analytics | 定义 | Knowledge/06-frontier/web3-streaming-analytics-defi.md |
| Def-K-06-262 | Blockchain Event Log | 定义 | Knowledge/06-frontier/web3-streaming-analytics-defi.md |
| Def-K-06-263 | Wallet Clustering | 定义 | Knowledge/06-frontier/web3-streaming-analytics-defi.md |
| Def-K-06-264 | MEV (Maximal Extractable Value) | 定义 | Knowledge/06-frontier/web3-streaming-analytics-defi.md |
| Def-K-06-265 | Cross-Chain Analytics | 定义 | Knowledge/06-frontier/web3-streaming-analytics-defi.md |
| Def-K-06-27 | 实时嵌入生成 (Real-time Embedding Generation) | 定义 | Knowledge/06-frontier/real-time-rag-architecture.md |
| Def-K-06-28 | 流式上下文检索 (Streaming Context Retrieval) | 定义 | Knowledge/06-frontier/real-time-rag-architecture.md |
| Def-K-06-29 | 向量存储同步 (Vector Store Synchronization) | 定义 | Knowledge/06-frontier/real-time-rag-architecture.md |
| Def-K-06-30 | AI-Native数据库 (AI-Native Database) | 定义 | Knowledge/06-frontier/vector-search-streaming-convergence.md |
| Def-K-06-31 | 实时RAG架构 (Real-Time RAG Architecture) | 定义 | Knowledge/06-frontier/vector-search-streaming-convergence.md |
| Def-K-06-32 | 向量索引增量更新 (Vector Index Incremental Update) | 定义 | Knowledge/06-frontier/vector-search-streaming-convergence.md |
| Def-K-06-33 | 流式近似最近邻搜索 (Streaming Approximate Nearest Neighbor Search) | 定义 | Knowledge/06-frontier/vector-search-streaming-convergence.md |
| Def-K-06-34 | 混合检索语义 (Hybrid Retrieval Semantics) | 定义 | Knowledge/06-frontier/vector-search-streaming-convergence.md |
| Def-K-06-40 | Streaming AI系统 (Streaming AI System) | 定义 | Knowledge/06-frontier/realtime-ai-streaming-2026.md |
| Def-K-06-41 | 三层核心架构 (Three-Tier Architecture) | 定义 | Knowledge/06-frontier/realtime-ai-streaming-2026.md |
| Def-K-06-42 | 事件级处理 vs 批处理 (Event-Level vs Batch Processing) | 定义 | Knowledge/06-frontier/realtime-ai-streaming-2026.md |
| Def-K-06-43 | 实时RAG架构 (Real-Time RAG) | 定义 | Knowledge/06-frontier/realtime-ai-streaming-2026.md |
| Def-K-06-50 | Agent-Native Database (Agent原生数据库) | 定义 | Knowledge/06-frontier/ai-agent-database-workloads.md |
| Def-K-06-51 | Ephemeral Database Pattern (瞬态数据库模式) | 定义 | Knowledge/06-frontier/ai-agent-database-workloads.md |
| Def-K-06-52 | Self-Driving Database Capability (自治数据库能力) | 定义 | Knowledge/06-frontier/ai-agent-database-workloads.md |
| Def-K-06-53 | 流式RAG (Streaming RAG) | 定义 | Knowledge/06-frontier/realtime-ai-inference-architecture.md |
| Def-K-06-54 | 低延迟推理优化 (Low-Latency Inference Optimization) | 定义 | Knowledge/06-frontier/realtime-ai-inference-architecture.md |
| Def-K-06-55 | GPU加速流处理 (GPU-Accelerated Stream Processing) | 定义 | Knowledge/06-frontier/realtime-ai-inference-architecture.md |
| Def-K-06-60 | 边缘LLM推理 (Edge LLM Inference) | 定义 | Knowledge/06-frontier/edge-llm-realtime-inference.md |
| Def-K-06-61 | 实时推理延迟模型 (Realtime Inference Latency Model) | 定义 | Knowledge/06-frontier/edge-llm-realtime-inference.md |
| Def-K-06-62 | 边缘-云协同推理 (Edge-Cloud Collaborative Inference) | 定义 | Knowledge/06-frontier/edge-llm-realtime-inference.md |
| Def-K-06-63 | 流式Token生成 (Streaming Token Generation) | 定义 | Knowledge/06-frontier/edge-llm-realtime-inference.md |
| Def-K-06-64 | 模型量化与压缩 (Model Quantization & Compression) {#def-k-06-64-模型量化与压缩-model-quantization--compression} | 定义 | Knowledge/06-frontier/edge-llm-realtime-inference.md |
| Def-K-06-70 | (多模态AI): 多模态AI是一个五元组 $\mathcal{M} = \langle \mathcal{M}_T, \mathcal{M}_I, \mathcal{M}_A, \mathcal{M}_V, \mathcal{F} \rangle$，其中： | 定义 | Knowledge/06-frontier/multimodal-ai-streaming-architecture.md |
| Def-K-06-71 | (实时多模态流): 实时多模态流是一个带时序约束的数据序列 $S = \langle (d_1, t_1, m_1), (d_2, t_2, m_2), \ldots \rangle$，其中： | 定义 | Knowledge/06-frontier/multimodal-ai-streaming-architecture.md |
| Def-K-06-72 | (跨模态统一表示): 设 $\phi_i: \mathcal{M}_i \rightarrow \mathbb{R}^d$ 为各模态的编码器，若存在投影矩阵 $W_i$ 使得对于语义等价的数据 $x_i \in \mathcal{M}_i, x_j \in \mathcal{M}_j$ 满足： | 定义 | Knowledge/06-frontier/multimodal-ai-streaming-architecture.md |
| Def-K-06-73 | (时间戳对齐误差): 对于同步采集的多模态数据对 $(x_A, x_V)$（音频-视频），若其采集时间戳分别为 $t_A, t_V$，则对齐误差 $\delta = | 定义 | Knowledge/06-frontier/multimodal-ai-streaming-architecture.md |
| Def-K-06-80 | (Web3 形式化定义): Web3 是一个去中心化的价值互联网协议栈，由三元组 $\mathcal{W}_3 = (\mathcal{L}, \mathcal{C}, \mathcal{T})$ 定义，其中： | 定义 | Knowledge/06-frontier/web3-blockchain-streaming-architecture.md |
| Def-K-06-81 | (区块结构): 区块链中的区块 $B_n$ 定义为： | 定义 | Knowledge/06-frontier/web3-blockchain-streaming-architecture.md |
| Def-K-06-82 | (事件日志): 智能合约事件是状态变更的不可变记录： | 定义 | Knowledge/06-frontier/web3-blockchain-streaming-architecture.md |
| Def-K-06-83 | (区块链事件流): 区块链事件流 $\mathcal{S}_{chain}$ 是一个有序事件序列： | 定义 | Knowledge/06-frontier/web3-blockchain-streaming-architecture.md |
| Def-K-06-84 | (最终性窗口): 对于采用概率最终性的区块链（如 PoW），交易在区块深度 $k$ 后被认为最终确定： | 定义 | Knowledge/06-frontier/web3-blockchain-streaming-architecture.md |
| Def-K-06-91 | Serverless流处理系统 (Serverless Stream Processing System) | 定义 | Knowledge/06-frontier/serverless-stream-processing-architecture.md |
| Def-K-06-92 | 冷启动延迟 (Cold Start Latency) | 定义 | Knowledge/06-frontier/serverless-stream-processing-architecture.md |
| Def-K-06-93 | 并发模型 (Concurrency Model) | 定义 | Knowledge/06-frontier/serverless-stream-processing-architecture.md |
| Def-K-06-94 | 批处理窗口 (Batch Window) | 定义 | Knowledge/06-frontier/serverless-stream-processing-architecture.md |
| Def-K-07-01 | 流处理测试金字塔 | 定义 | Knowledge/07-best-practices/07.07-testing-strategies-complete.md |
| Def-K-07-02 | TestHarness | 定义 | Knowledge/07-best-practices/07.07-testing-strategies-complete.md |
| Def-K-07-03 | 确定性测试 | 定义 | Knowledge/07-best-practices/07.07-testing-strategies-complete.md |
| Def-K-07-04 | MiniCluster | 定义 | Knowledge/07-best-practices/07.07-testing-strategies-complete.md |
| Def-K-07-05 | 内存加密语义 | 定义 |  |
| Def-K-07-06 | Knowledge/07-best-practices/07.06-high-availability-patterns.md | 定义 |  |
| Def-K-08-01 | Lakehouse存储模型 | 定义 |  |
| Def-K-08-02 | 时间旅行查询 | 定义 |  |
| Def-K-08-03 | ACID事务语义 | 定义 |  |
| Def-K-08-04 | 元数据层 | 定义 |  |
| Def-K-08-05 | 增量表格式 | 定义 |  |
| Def-K-08-20 | 流数据治理 (Streaming Data Governance) | 定义 | Knowledge/08-standards/streaming-data-governance.md |
| Def-K-08-21 | 流数据与批处理治理差异 | 定义 | Knowledge/08-standards/streaming-data-governance.md |
| Def-K-08-22 | 三大治理支柱 (Three Pillars) | 定义 | Knowledge/08-standards/streaming-data-governance.md |
| Def-K-08-30 | 实时数据质量管理 (Real-time Data Quality Management) | 定义 | Knowledge/08-standards/streaming-data-governance-quality.md |
| Def-K-08-31 | 数据质量维度 (Data Quality Dimensions) | 定义 | Knowledge/08-standards/streaming-data-governance-quality.md |
| Def-K-08-32 | 流式数据血缘 (Streaming Data Lineage) | 定义 | Knowledge/08-standards/streaming-data-governance-quality.md |
| Def-K-08-33 | 流式主数据管理 (Streaming MDM) | 定义 | Knowledge/08-standards/streaming-data-governance-quality.md |
| Def-K-08-34 | 实时数据剖析 (Streaming Data Profiling) | 定义 | Knowledge/08-standards/streaming-data-governance-quality.md |
| Def-K-08-35 | 流数据治理成熟度模型 (Streaming Governance Maturity) | 定义 | Knowledge/08-standards/streaming-data-governance-quality.md |
| Def-K-09-01 | RAG系统架构 | 定义 |  |
| Def-K-09-02 | 向量嵌入空间 | 定义 |  |
| Def-K-09-03 | 语义检索 | 定义 |  |
| Def-K-09-04 | 流式向量索引 | 定义 |  |
| Def-K-09-05 | 上下文窗口约束 | 定义 |  |
| Def-K-09-06 | 检索-生成一致性 | 定义 |  |
| Def-K-09-07 | Knowledge/09-anti-patterns/anti-pattern-07-window-state-explosion.md | 定义 |  |
| Def-K-09-08 | Knowledge/09-anti-patterns/anti-pattern-08-ignoring-backpressure.md | 定义 |  |
| Def-K-09-09 | Knowledge/09-anti-patterns/anti-pattern-09-multi-stream-join-misalignment.md | 定义 |  |
| Def-K-09-10 | Knowledge/09-anti-patterns/anti-pattern-10-resource-estimation-oom.md | 定义 |  |
| Def-K-10-201 | (实时推荐系统): 实时推荐系统是一个九元组 $\mathcal{R} = (U, I, C, B, F, M, S, P, W)$： | 定义 | Knowledge/case-studies/ecommerce-realtime-recommendation-v2.md |
| Def-K-10-202 | (用户实时画像): 用户 $u$ 在时间 $t$ 的实时画像定义为： | 定义 | Knowledge/case-studies/ecommerce-realtime-recommendation-v2.md |
| Def-K-10-203 | (实时特征向量): 特征工程输出： | 定义 | Knowledge/case-studies/ecommerce-realtime-recommendation-v2.md |
| Def-K-10-204 | (推荐效果指标): | 定义 | Knowledge/case-studies/ecommerce-realtime-recommendation-v2.md |
| Def-K-10-205 | (延迟约束): | 定义 | Knowledge/case-studies/ecommerce-realtime-recommendation-v2.md |
| Def-K-10-206 | (冷启动分类): | 定义 | Knowledge/case-studies/ecommerce-realtime-recommendation-v2.md |
| Def-K-10-211 | (智能电网IoT系统): 智能电网IoT系统是一个十元组 $\mathcal{G} = (D, M, E, C, N, F, P, A, S, R)$： | 定义 | Knowledge/case-studies/iot-smart-grid-case-study.md |
| Def-K-10-212 | (短期负荷预测): 区域 $r$ 在时间 $t+\Delta t$ 的负荷预测： | 定义 | Knowledge/case-studies/iot-smart-grid-case-study.md |
| Def-K-10-213 | (预测误差度量): | 定义 | Knowledge/case-studies/iot-smart-grid-case-study.md |
| Def-K-10-214 | (用电异常评分): | 定义 | Knowledge/case-studies/iot-smart-grid-case-study.md |
| Def-K-10-215 | (设备健康度): | 定义 | Knowledge/case-studies/iot-smart-grid-case-study.md |
| Def-K-10-221 | (高性能反欺诈系统): 高性能反欺诈系统是一个十二元组 $\mathcal{F} = (T, U, D, R, C, G, F, M, E, P, S, A)$： | 定义 | Knowledge/case-studies/fraud-detection-production-case.md |
| Def-K-10-222 | (CEP欺诈模式): 复杂事件模式是一个五元组 $\mathcal{P} = (E_{seq}, \phi, \tau, \omega, \lambda)$： | 定义 | Knowledge/case-studies/fraud-detection-production-case.md |
| Def-K-10-223 | (位置跳跃检测): | 定义 | Knowledge/case-studies/fraud-detection-production-case.md |
| Def-K-10-224 | (交易关系图): 交易图 $G = (V, E, X)$ 其中： | 定义 | Knowledge/case-studies/fraud-detection-production-case.md |
| Def-K-10-225 | (图神经网络风险评分): | 定义 | Knowledge/case-studies/fraud-detection-production-case.md |
| Def-K-10-231 | (游戏实时分析平台): 游戏实时分析平台是一个十元组 $\mathcal{A} = (P, S, E, M, C, F, D, R, V, B)$： | 定义 | Knowledge/case-studies/gaming-analytics-platform-case.md |
| Def-K-10-232 | (实时指标): | 定义 | Knowledge/case-studies/gaming-analytics-platform-case.md |
| Def-K-10-233 | (玩家实时画像): 玩家 $p$ 在时间 $t$ 的实时画像： | 定义 | Knowledge/case-studies/gaming-analytics-platform-case.md |
| Def-K-10-234 | (流失风险模型): | 定义 | Knowledge/case-studies/gaming-analytics-platform-case.md |
| Def-K-10-235 | (A/B测试实验): 实验定义为五元组 $\mathcal{E} = (N, V, A, H, M)$： | 定义 | Knowledge/case-studies/gaming-analytics-platform-case.md |
| Def-K-10-236 | (流量分配): | 定义 | Knowledge/case-studies/gaming-analytics-platform-case.md |
| Def-K-10-237 | (统计显著性): | 定义 | Knowledge/case-studies/gaming-analytics-platform-case.md |
| Def-K-10-238 | (玩家分群): | 定义 | Knowledge/case-studies/gaming-analytics-platform-case.md |
| Lemma-K-01-01 | Scala 流库的组合性 | 引理 | Knowledge/Flink-Scala-Rust-Comprehensive/01-scala-ecosystem/01.01-scala-streaming-landscape.md |
| Lemma-K-01-02 | 纯函数流变换的确定性 | 引理 | Knowledge/Flink-Scala-Rust-Comprehensive/01-scala-ecosystem/01.01-scala-streaming-landscape.md |
| Lemma-K-01-20 | Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md | 引理 |  |
| Lemma-K-01-21 | Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md | 引理 |  |
| Lemma-K-02-01 | 编译时派生的完备性 | 引理 | Knowledge/Flink-Scala-Rust-Comprehensive/01-scala-ecosystem/01.02-flink-scala-api-analysis.md |
| Lemma-K-02-02 | Scala 2.13/3.x 跨版本兼容性 | 引理 | Knowledge/Flink-Scala-Rust-Comprehensive/01-scala-ecosystem/01.02-flink-scala-api-analysis.md |
| Lemma-K-02-03 | Credit-Based 流控无死锁保证 | 引理 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.02-flink-runtime-deep-dive.md |
| Lemma-K-02-04 | 窗口边界事件处理的一致性 | 引理 | Knowledge/02-design-patterns/pattern-realtime-feature-engineering.md |
| Lemma-K-02-05 | 滑动窗口特征计算效率 | 引理 | Knowledge/02-design-patterns/pattern-realtime-feature-engineering.md |
| Lemma-K-02-06 | 特征在线/离线一致性保证 | 引理 | Knowledge/02-design-patterns/pattern-realtime-feature-engineering.md |
| Lemma-K-02-07 | Table API 与 DataStream API 表达能力等价性 | 引理 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.04-flink-sql-table-api.md |
| Lemma-K-02-08 | 物化表新鲜度保证 | 引理 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.04-flink-sql-table-api.md |
| Lemma-K-02-09 | K8s 原生部署的故障隔离性 | 引理 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.05-flink-cloud-native.md |
| Lemma-K-02-10 | 自动扩缩容收敛性 | 引理 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.05-flink-cloud-native.md |
| Lemma-K-03-01 | 供需平衡收敛引理 | 引理 | Knowledge/03-business-patterns/uber-realtime-platform.md |
| Lemma-K-03-02 | 欺诈检测准确率下界 | 引理 | Knowledge/03-business-patterns/stripe-payment-processing.md |
| Lemma-K-03-03 | 排行榜一致性边界 | 引理 | Knowledge/03-business-patterns/gaming-analytics.md |
| Lemma-K-03-04 | 供需匹配效率下界 | 引理 | Knowledge/03-business-patterns/airbnb-marketplace-dynamics.md |
| Lemma-K-03-20 | Knowledge/03-business-patterns/data-mesh-streaming-architecture-2026.md | 引理 |  |
| Lemma-K-03-21 | Knowledge/03-business-patterns/data-mesh-streaming-architecture-2026.md | 引理 |  |
| Lemma-K-03-22 | Knowledge/03-business-patterns/data-mesh-streaming-architecture-2026.md | 引理 |  |
| Lemma-K-03-50 | 数据新鲜度价值衰减 | 引理 | Knowledge/03-business-patterns/streaming-data-product-economics.md |
| Lemma-K-03-51 | 边际成本递减 | 引理 | Knowledge/03-business-patterns/streaming-data-product-economics.md |
| Lemma-K-04-01 | fs2 流的组合性 | 引理 | Knowledge/Flink-Scala-Rust-Comprehensive/01-scala-ecosystem/01.04-fs2-pekko-streams.md |
| Lemma-K-04-02 | Pekko Streams 图的可视化 | 引理 | Knowledge/Flink-Scala-Rust-Comprehensive/01-scala-ecosystem/01.04-fs2-pekko-streams.md |
| Lemma-K-04-03 | (存储分离与恢复时间关系) | 引理 | Knowledge/04-technology-selection/flink-vs-risingwave.md |
| Lemma-K-04-04 | (状态位置与扩展性权衡) | 引理 | Knowledge/04-technology-selection/flink-vs-risingwave.md |
| Lemma-K-04-05 | (存算分离与成本关系) | 引理 | Knowledge/04-technology-selection/streaming-databases-2026-comparison.md |
| Lemma-K-04-06 | (SQL兼容性边界) | 引理 | Knowledge/04-technology-selection/streaming-databases-2026-comparison.md |
| Lemma-K-05-01 | 映射传递性引理 | 引理 | Knowledge/05-mapping-guides/struct-to-flink-mapping.md |
| Lemma-K-05-02 | 理论保持性引理 | 引理 | Knowledge/05-mapping-guides/struct-to-flink-mapping.md |
| Lemma-K-05-03 | 代码等价性保持 | 引理 | Knowledge/05-mapping-guides/theory-to-code-patterns.md |
| Lemma-K-05-04 | Knowledge/05-mapping-guides/migration-guides/05.4-flink-1x-to-2x-migration.md | 引理 |  |
| Lemma-K-05-05 | Knowledge/05-mapping-guides/migration-guides/05.5-batch-to-streaming-migration.md | 引理 |  |
| Lemma-K-05-15 | 事件流平台性能边界 | 引理 | Knowledge/05-mapping-guides/streaming-etl-tools-landscape-2026.md |
| Lemma-K-05-16 | 流处理引擎能力边界 | 引理 | Knowledge/05-mapping-guides/streaming-etl-tools-landscape-2026.md |
| Lemma-K-05-17 | 云原生服务约束 | 引理 | Knowledge/05-mapping-guides/streaming-etl-tools-landscape-2026.md |
| Lemma-K-05-20 | Knowledge/05-mapping-guides/streaming-sql-engines-2026-comparison.md | 引理 |  |
| Lemma-K-05-22 | Knowledge/05-mapping-guides/streaming-sql-engines-2026-comparison.md | 引理 |  |
| Lemma-K-05-23 | Knowledge/05-mapping-guides/streaming-sql-engines-2026-comparison.md | 引理 |  |
| Lemma-K-05-25 | Knowledge/05-mapping-guides/streaming-sql-engines-2026-comparison.md | 引理 |  |
| Lemma-K-05-31 | 控制流显式程度排序 | 引理 | Knowledge/05-mapping-guides/multi-agent-frameworks-2026-comparison.md |
| Lemma-K-05-32 | 开发效率与学习曲线权衡 | 引理 | Knowledge/05-mapping-guides/multi-agent-frameworks-2026-comparison.md |
| Lemma-K-05-33 | 模型依赖性边界 | 引理 | Knowledge/05-mapping-guides/multi-agent-frameworks-2026-comparison.md |
| Lemma-K-06-001 | (验证延迟不等式) | 引理 | Knowledge/06-frontier/realtime-data-quality-validation.md |
| Lemma-K-06-002 | (DLQ完备性条件) | 引理 | Knowledge/06-frontier/realtime-data-quality-validation.md |
| Lemma-K-06-01 | 函数链状态传递引理 | 引理 | Knowledge/06-frontier/faas-dataflow.md |
| Lemma-K-06-02 | (计算弹性). 计算节点可独立扩展： | 引理 | Knowledge/06-frontier/risingwave-deep-dive.md |
| Lemma-K-06-03 | (写路径优化). Hummock 的写放大因子 $\alpha_{write}$ 满足： | 引理 | Knowledge/06-frontier/risingwave-deep-dive.md |
| Lemma-K-06-04 | 卸载决策的阈值特性 | 引理 | Knowledge/06-frontier/cloud-edge-continuum.md |
| Lemma-K-06-05 | Wasm 跨平台执行等价性 | 引理 | Knowledge/06-frontier/edge-streaming-patterns.md |
| Lemma-K-06-06 | (Barrier 一致性). 对于任意执行路径 $p$，Barrier $B(e)$ 保证： | 引理 | Knowledge/06-frontier/risingwave-deep-dive.md |
| Lemma-K-06-07 | 向量一致性引理 | 引理 | Knowledge/06-frontier/real-time-rag-architecture.md |
| Lemma-K-06-08 | 流式嵌入延迟分解 | 引理 | Knowledge/06-frontier/vector-search-streaming-convergence.md |
| Lemma-K-06-10 | 热加载原子性保证 | 引理 | Knowledge/06-frontier/edge-llm-realtime-inference.md |
| Lemma-K-06-100 | 验证延迟不等式 | 引理 |  |
| Lemma-K-06-101 | 验证吞吐量上界 | 引理 |  |
| Lemma-K-06-102 | DLQ完备性条件 | 引理 |  |
| Lemma-K-06-105 | 多云可用性上限 | 引理 |  |
| Lemma-K-06-106 | 跨云延迟下界 | 引理 |  |
| Lemma-K-06-11 | RisingWave 状态重建时间 | 引理 | Knowledge/06-frontier/rust-streaming-ecosystem.md |
| Lemma-K-06-110 | TLS层级的机密性保证 | 引理 | Knowledge/06-frontier/streaming-security-compliance.md |
| Lemma-K-06-111 | RBAC层次化的权限继承 | 引理 | Knowledge/06-frontier/streaming-security-compliance.md |
| Lemma-K-06-112 | 端到端加密的数据独立性 | 引理 | Knowledge/06-frontier/streaming-security-compliance.md |
| Lemma-K-06-115 | (增量计算正确性). 对于任意查询 $Q$ 和基础表变更序列 $\langle \Delta B_1, \Delta B_2, ..., \Delta B_k \rangle$，增量维护机制 $\mathcal{I}$ 满足： | 引理 | Knowledge/06-frontier/streaming-materialized-view-architecture.md |
| Lemma-K-06-116 | (级联更新传播). 在级联物化视图 $DAG$ 中，对于任意节点 $V$，其更新延迟满足： | 引理 | Knowledge/06-frontier/streaming-materialized-view-architecture.md |
| Lemma-K-06-117 | (存储空间优化). 物化视图系统的存储复杂度： | 引理 | Knowledge/06-frontier/streaming-materialized-view-architecture.md |
| Lemma-K-06-12 | Materialize 多副本一致性 | 引理 | Knowledge/06-frontier/rust-streaming-ecosystem.md |
| Lemma-K-06-125 | [边缘计算优势边界]: 对于数据密集型IoT应用，当满足以下条件时，边缘处理优于纯云处理： | 引理 | Knowledge/06-frontier/edge-streaming-architecture.md |
| Lemma-K-06-130 | Serverless成本边界引理 | 引理 |  |
| Lemma-K-06-131 | 冷启动频率成本影响 | 引理 |  |
| Lemma-K-06-132 | 批处理窗口成本效益 | 引理 |  |
| Lemma-K-06-15 | 模型切换延迟引理 | 引理 | Knowledge/06-frontier/realtime-ai-inference-architecture.md |
| Lemma-K-06-16 | 多模态对齐引理 | 引理 | Knowledge/06-frontier/realtime-ai-inference-architecture.md |
| Lemma-K-06-160 | Kafka 协议标准化效应 | 引理 | Knowledge/06-frontier/data-streaming-landscape-2025.md |
| Lemma-K-06-161 | 存算分离的权衡定律 | 引理 | Knowledge/06-frontier/data-streaming-landscape-2025.md |
| Lemma-K-06-162 | 流处理引擎的状态复杂度边界 | 引理 | Knowledge/06-frontier/data-streaming-landscape-2025.md |
| Lemma-K-06-20 | (差分计算复杂度边界) | 引理 | Knowledge/06-frontier/materialize-comparison-guide.md |
| Lemma-K-06-200 | 流式调度一致性引理 | 引理 | Knowledge/06-frontier/multi-agent-streaming-orchestration.md |
| Lemma-K-06-201 | 消息传递有序性引理 | 引理 | Knowledge/06-frontier/multi-agent-streaming-orchestration.md |
| Lemma-K-06-202 | 在线存储容量边界 | 引理 | Knowledge/06-frontier/realtime-feature-store-architecture.md |
| Lemma-K-06-21 | (时间戳传播与一致性关系) | 引理 | Knowledge/06-frontier/materialize-comparison-guide.md |
| Lemma-K-06-210 | MCP 协议延迟边界 | 引理 | Knowledge/06-frontier/mcp-protocol-agent-streaming.md |
| Lemma-K-06-211 | 并发 Tool 调用安全 | 引理 | Knowledge/06-frontier/mcp-protocol-agent-streaming.md |
| Lemma-K-06-220 | A2A 协议延迟分解 | 引理 | Knowledge/06-frontier/a2a-protocol-agent-communication.md |
| Lemma-K-06-221 | Agent Card 缓存有效性 | 引理 | Knowledge/06-frontier/a2a-protocol-agent-communication.md |
| Lemma-K-06-230 | A2A 协议分层延迟分解 | 引理 | Knowledge/06-frontier/ai-agent-a2a-protocol.md |
| Lemma-K-06-231 | Task 并发与隔离性 | 引理 | Knowledge/06-frontier/ai-agent-a2a-protocol.md |
| Lemma-K-06-250 | 同步精度与成本权衡 | 引理 | Knowledge/06-frontier/realtime-digital-twin-streaming.md |
| Lemma-K-06-251 | 边缘-云协同延迟 | 引理 | Knowledge/06-frontier/realtime-digital-twin-streaming.md |
| Lemma-K-06-260 | 区块链最终性延迟 | 引理 | Knowledge/06-frontier/web3-streaming-analytics-defi.md |
| Lemma-K-06-261 | 跨链套利窗口 | 引理 | Knowledge/06-frontier/web3-streaming-analytics-defi.md |
| Lemma-K-06-40 | (多模态流延迟下界): 对于包含 $n$ 个模态的实时流系统，端到端延迟满足： | 引理 | Knowledge/06-frontier/multimodal-ai-streaming-architecture.md |
| Lemma-K-06-41 | (多模态吞吐量上限): 设模型单次推理处理批次大小为 $B$，推理时间为 $T_{inf}$，则系统最大吞吐量： | 引理 | Knowledge/06-frontier/multimodal-ai-streaming-architecture.md |
| Lemma-K-06-50 | (追加不可变性): 区块链事件流 $\mathcal{S}_{chain}$ 满足追加写入语义，历史事件不可变更： | 引理 | Knowledge/06-frontier/web3-blockchain-streaming-architecture.md |
| Lemma-K-06-51 | (最终一致性边界): 设区块链出块间隔为 $\Delta_b$，确认深度为 $k$，则事件可见性延迟满足： | 引理 | Knowledge/06-frontier/web3-blockchain-streaming-architecture.md |
| Lemma-K-06-52 | (事件溯源完备性): 区块链状态 $S_n$ 可完全由其创世状态 $S_0$ 和事件流前缀 $\mathcal{S}_{chain} | 引理 | Knowledge/06-frontier/web3-blockchain-streaming-architecture.md |
| Lemma-K-06-61 | Serverless延迟边界 | 引理 | Knowledge/06-frontier/serverless-stream-processing-architecture.md |
| Lemma-K-06-62 | 成本边界定理 | 引理 | Knowledge/06-frontier/serverless-stream-processing-architecture.md |
| Lemma-K-06-71 | 流式接口的幂等性边界 | 引理 | Knowledge/06-frontier/realtime-data-product-architecture.md |
| Lemma-K-06-72 | Schema演进兼容性传递性 | 引理 | Knowledge/06-frontier/realtime-data-product-architecture.md |
| Lemma-K-06-80 | 上下文窗口效率引理 | 引理 | Knowledge/06-frontier/ai-agent-streaming-architecture.md |
| Lemma-K-06-81 | 记忆一致性引理 | 引理 | Knowledge/06-frontier/ai-agent-streaming-architecture.md |
| Lemma-K-06-90 | (域自治与全局一致性权衡)：在Data Mesh架构中，域自治度 $\alpha$ 与全局一致性 $C$ 满足反比关系： | 引理 | Knowledge/06-frontier/streaming-data-mesh-architecture.md |
| Lemma-K-06-91 | (实时数据产品的网络效应)：设域数量为 $n$，数据产品数量为 $m$，则网格价值 $V_{mesh}$ 满足： | 引理 | Knowledge/06-frontier/streaming-data-mesh-architecture.md |
| Lemma-K-06-92 | (Schema演化兼容性)：设Schema版本序列为 $S_1, S_2, ..., S_n$，向后兼容性要求： | 引理 | Knowledge/06-frontier/streaming-data-mesh-architecture.md |
| Lemma-K-06-96 | 自动扩缩容响应时间引理 | 引理 |  |
| Lemma-K-06-97 | Serverless成本边界 | 引理 | Knowledge/06-frontier/serverless-streaming-cost-optimization.md |
| Lemma-K-06-98 | 批流成本盈亏平衡点 | 引理 | Knowledge/06-frontier/serverless-streaming-cost-optimization.md |
| Lemma-K-07-01 | 测试幂等性 | 引理 | Knowledge/07-best-practices/07.07-testing-strategies-complete.md |
| Lemma-K-07-02 | GPU内存加密原子性 | 引理 |  |
| Lemma-K-07-03 | Knowledge/07-best-practices/07.03-troubleshooting-guide.md | 引理 |  |
| Lemma-K-07-04 | Knowledge/07-best-practices/07.04-cost-optimization-patterns.md | 引理 |  |
| Lemma-K-07-05 | Knowledge/07-best-practices/07.05-security-hardening-guide.md | 引理 |  |
| Lemma-K-07-06 | Knowledge/07-best-practices/07.06-high-availability-patterns.md | 引理 |  |
| Lemma-K-08-01 | 时间戳单调性引理 | 引理 |  |
| Lemma-K-08-02 | 快照隔离一致性 | 引理 |  |
| Lemma-K-08-10 | 审计日志不可篡改性 | 引理 | Knowledge/08-standards/streaming-security-compliance.md |
| Lemma-K-09-01 | 向量相似度保持性 | 引理 |  |
| Lemma-K-09-02 | 上下文窗口边界引理 | 引理 |  |
| Lemma-K-09-03 | 检索-生成组合性 | 引理 |  |
| Lemma-K-10-201 | 设特征查询延迟为 $L_f$，召回阶段延迟为 $L_r$，排序阶段延迟为 $L_s$，则总延迟满足： | 引理 | Knowledge/case-studies/ecommerce-realtime-recommendation-v2.md |
| Lemma-K-10-202 | (特征存储容量): 设用户数为 $N_u$，每用户特征维度为 $d$，单条特征大小为 $s$ 字节，Redis集群分片数为 $S$，则每分片存储： | 引理 | Knowledge/case-studies/ecommerce-realtime-recommendation-v2.md |
| Lemma-K-10-211 | 设边缘聚合延迟为 $L_{edge}$，网络传输延迟为 $L_{net}$，云端处理延迟为 $L_{cloud}$，则端到端延迟： | 引理 | Knowledge/case-studies/iot-smart-grid-case-study.md |
| Lemma-K-10-212 | (数据完整性): 设单条消息丢失概率为 $p$，系统采用 $k$ 重备份，则数据丢失概率： | 引理 | Knowledge/case-studies/iot-smart-grid-case-study.md |
| Lemma-K-10-221 | 在10ms延迟约束下，各阶段时间分配： | 引理 | Knowledge/case-studies/fraud-detection-production-case.md |
| Lemma-K-10-222 | 要达到50万TPS，假设单核处理能力为 $c$ TPS，则需要的最小核数： | 引理 | Knowledge/case-studies/fraud-detection-production-case.md |
| Lemma-K-10-231 | 设事件上报延迟为 $L_{report}$，网络传输延迟为 $L_{network}$，处理延迟为 $L_{process}$，则端到端可见延迟： | 引理 | Knowledge/case-studies/gaming-analytics-platform-case.md |
| Lemma-K-10-232 | 设Kafka分区数为 $P$，Flink并行度为 $F$，要保证全局顺序，需满足： | 引理 | Knowledge/case-studies/gaming-analytics-platform-case.md |
| Prop-K-01-01 | (Dataflow 的确定性保证) | 命题 | Knowledge/01-concept-atlas/streaming-models-mindmap.md |
| Prop-K-01-02 | (Actor 的局部顺序一致性) | 命题 | Knowledge/01-concept-atlas/streaming-models-mindmap.md |
| Prop-K-01-03 | (CSP 的背压内建性) | 命题 | Knowledge/01-concept-atlas/streaming-models-mindmap.md |
| Prop-K-01-04 | (Pub/Sub 的吞吐-延迟权衡) | 命题 | Knowledge/01-concept-atlas/streaming-models-mindmap.md |
| Prop-K-01-05 | (CEP 的表达能力与状态爆炸) | 命题 | Knowledge/01-concept-atlas/streaming-models-mindmap.md |
| Prop-K-01-20 | Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md | 命题 |  |
| Prop-K-01-21 | Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md | 命题 |  |
| Prop-K-01-22 | Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md | 命题 |  |
| Prop-K-02-01 | (异步化吞吐量提升) | 命题 | Knowledge/02-design-patterns/pattern-async-io-enrichment.md |
| Prop-K-02-02 | (并发度与内存权衡) | 命题 | Knowledge/02-design-patterns/pattern-async-io-enrichment.md |
| Prop-K-02-03 | (解析完备性) | 命题 | Knowledge/02-design-patterns/pattern-log-analysis.md |
| Prop-K-02-04 | (关联传递性) | 命题 | Knowledge/02-design-patterns/pattern-log-analysis.md |
| Prop-K-02-05 | 恢复速度与状态大小的关系 | 命题 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.03-flink-state-backends.md |
| Prop-K-02-06 | 成本模型的差异 | 命题 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.03-flink-state-backends.md |
| Prop-K-02-07 | Calcite CBO 最优性 | 命题 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.04-flink-sql-table-api.md |
| Prop-K-02-08 | Model DDL 与 UDF 的性能优势 | 命题 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.04-flink-sql-table-api.md |
| Prop-K-02-09 | 云存储的持久性保证 | 命题 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.05-flink-cloud-native.md |
| Prop-K-02-10 | Serverless 的成本效益 | 命题 | Knowledge/Flink-Scala-Rust-Comprehensive/02-flink-system/02.05-flink-cloud-native.md |
| Prop-K-03-01 | 设备状态一致性 | 命题 | Knowledge/03-business-patterns/iot-stream-processing.md |
| Prop-K-03-02 | 会话窗口完整性 | 命题 | Knowledge/03-business-patterns/iot-stream-processing.md |
| Prop-K-03-03 | 事件乱序容忍度 | 命题 | Knowledge/03-business-patterns/gaming-analytics.md |
| Prop-K-03-04 | 乱序数据收敛性 | 命题 | Knowledge/03-business-patterns/iot-stream-processing.md |
| Prop-K-03-05 | Schema 演进的向后兼容性 | 命题 | Knowledge/03-business-patterns/log-monitoring.md |
| Prop-K-03-06 | 实时推荐延迟边界 | 命题 | Knowledge/03-business-patterns/spotify-music-recommendation.md |
| Prop-K-03-07 | 定价收敛性定理 | 命题 | Knowledge/03-business-patterns/airbnb-marketplace-dynamics.md |
| Prop-K-03-11 | 超大规模流处理特性 | 命题 | Knowledge/03-business-patterns/alibaba-double11-flink.md |
| Prop-K-03-12 | 分离式架构优势 | 命题 | Knowledge/03-business-patterns/alibaba-double11-flink.md |
| Prop-K-03-15 | Knowledge/03-business-patterns/data-mesh-streaming-architecture-2026.md | 命题 |  |
| Prop-K-03-16 | Knowledge/03-business-patterns/data-mesh-streaming-architecture-2026.md | 命题 |  |
| Prop-K-03-50 | 实时数据溢价 | 命题 | Knowledge/03-business-patterns/streaming-data-product-economics.md |
| Prop-K-03-51 | 数据网络效应 | 命题 | Knowledge/03-business-patterns/streaming-data-product-economics.md |
| Prop-K-04-01 | 背压传播保证 | 命题 | Knowledge/Flink-Scala-Rust-Comprehensive/01-scala-ecosystem/01.04-fs2-pekko-streams.md |
| Prop-K-04-02 | Knowledge/04-technology-selection/engine-selection-guide.md | 命题 |  |
| Prop-K-04-03 | (SQL原生性对开发效率的影响) | 命题 | Knowledge/04-technology-selection/flink-vs-risingwave.md |
| Prop-K-04-04 | (生态成熟度与选型权衡) | 命题 | Knowledge/04-technology-selection/streaming-databases-2026-comparison.md |
| Prop-K-04-05 | Knowledge/04-technology-selection/storage-selection-guide.md | 命题 |  |
| Prop-K-05-01 | 语义等价性命题 | 命题 | Knowledge/05-mapping-guides/struct-to-flink-mapping.md |
| Prop-K-05-02 | 跨层数据传输开销上界 | 命题 | Knowledge/Flink-Scala-Rust-Comprehensive/05-architecture-patterns/05.01-hybrid-architecture-patterns.md |
| Prop-K-05-03 | 容错一致性传递 | 命题 | Knowledge/Flink-Scala-Rust-Comprehensive/05-architecture-patterns/05.01-hybrid-architecture-patterns.md |
| Prop-K-05-04 | 迁移风险递减性 | 命题 | Knowledge/Flink-Scala-Rust-Comprehensive/05-architecture-patterns/05.02-migration-strategies.md |
| Prop-K-05-05 | 双写一致性条件 | 命题 | Knowledge/Flink-Scala-Rust-Comprehensive/05-architecture-patterns/05.02-migration-strategies.md |
| Prop-K-05-06 | 回滚可行性 | 命题 | Knowledge/Flink-Scala-Rust-Comprehensive/05-architecture-patterns/05.02-migration-strategies.md |
| Prop-K-05-08 | 声明式部署幂等性 | 命题 | Knowledge/Flink-Scala-Rust-Comprehensive/05-architecture-patterns/05.03-cloud-deployment.md |
| Prop-K-05-09 | 水平扩容线性加速 | 命题 | Knowledge/Flink-Scala-Rust-Comprehensive/05-architecture-patterns/05.03-cloud-deployment.md |
| Prop-K-05-10 | 故障域隔离 | 命题 | Knowledge/Flink-Scala-Rust-Comprehensive/05-architecture-patterns/05.03-cloud-deployment.md |
| Prop-K-05-11 | 边缘处理延迟优势 | 命题 | Knowledge/Flink-Scala-Rust-Comprehensive/05-architecture-patterns/05.04-edge-computing.md |
| Prop-K-05-12 | 边缘计算成本效益 | 命题 | Knowledge/Flink-Scala-Rust-Comprehensive/05-architecture-patterns/05.04-edge-computing.md |
| Prop-K-05-13 | WASM 沙箱安全性 | 命题 | Knowledge/Flink-Scala-Rust-Comprehensive/05-architecture-patterns/05.04-edge-computing.md |
| Prop-K-05-31 | 2026框架功能完备性对比 | 命题 | Knowledge/05-mapping-guides/multi-agent-frameworks-2026-comparison.md |
| Prop-K-05-32 | 性能边界推导 | 命题 | Knowledge/05-mapping-guides/multi-agent-frameworks-2026-comparison.md |
| Prop-K-06-001 | (验证吞吐量上界) | 命题 | Knowledge/06-frontier/realtime-data-quality-validation.md |
| Prop-K-06-01 | 冷启动延迟与并发度的权衡 | 命题 | Knowledge/06-frontier/faas-dataflow.md |
| Prop-K-06-02 | 数据局部性增益边界 | 命题 | Knowledge/06-frontier/faas-dataflow.md |
| Prop-K-06-03 | 混合架构成本优化 | 命题 | Knowledge/06-frontier/risingwave-integration-guide.md |
| Prop-K-06-04 | 流计算与工作流的互补性 | 命题 | Knowledge/06-frontier/temporal-flink-layered-architecture.md |
| Prop-K-06-05 | 延迟分层递减性 | 命题 | Knowledge/06-frontier/cloud-edge-continuum.md |
| Prop-K-06-06 | 资源-精度权衡律 | 命题 | Knowledge/06-frontier/cloud-edge-continuum.md |
| Prop-K-06-07 | 移动性导致状态一致性开销 | 命题 | Knowledge/06-frontier/cloud-edge-continuum.md |
| Prop-K-06-08 | 延迟分层递减性 | 命题 | Knowledge/06-frontier/edge-streaming-patterns.md |
| Prop-K-06-09 | 资源-精度权衡律 | 命题 | Knowledge/06-frontier/edge-streaming-patterns.md |
| Prop-K-06-10 | 离线-在线一致性边界 | 命题 | Knowledge/06-frontier/edge-streaming-patterns.md |
| Prop-K-06-100 | 成本最优部署形态 | 命题 |  |
| Prop-K-06-101 | 状态外置成本临界点 | 命题 |  |
| Prop-K-06-102 | 自动扩缩容成本稳定性 | 命题 |  |
| Prop-K-06-105 | 多云部署的可用性上限 | 命题 | Knowledge/06-frontier/multi-cloud-streaming-architecture.md |
| Prop-K-06-106 | 跨云延迟下界 | 命题 | Knowledge/06-frontier/multi-cloud-streaming-architecture.md |
| Prop-K-06-107 | 数据一致性三角权衡 | 命题 | Knowledge/06-frontier/multi-cloud-streaming-architecture.md |
| Prop-K-06-11 | 检索质量边界 | 命题 | Knowledge/06-frontier/real-time-rag-architecture.md |
| Prop-K-06-110 | 多层安全控制的复合效应 | 命题 | Knowledge/06-frontier/streaming-security-compliance.md |
| Prop-K-06-111 | 最小权限原则的形式化表述 | 命题 | Knowledge/06-frontier/streaming-security-compliance.md |
| Prop-K-06-12 | 向量索引一致性边界 | 命题 | Knowledge/06-frontier/vector-search-streaming-convergence.md |
| Prop-K-06-126 | [数据本地化收益]: 在边缘执行数据预过滤和聚合，可将上传数据量减少 70-95% | 命题 | Knowledge/06-frontier/edge-streaming-architecture.md |
| Prop-K-06-127 | [边缘AI融合]: 到2026年，超过 75% 的企业数据将在边缘产生和处理（2020年仅为10%），主要驱动因素包括： | 命题 | Knowledge/06-frontier/edge-streaming-architecture.md |
| Prop-K-06-13 | 一致性-延迟权衡 | 命题 | Knowledge/06-frontier/rust-streaming-ecosystem.md |
| Prop-K-06-130 | 事件流作为数据产品接口的必要性 | 命题 | Knowledge/06-frontier/realtime-data-mesh-practice.md |
| Prop-K-06-131 | 数据契约的兼容性传播 | 命题 | Knowledge/06-frontier/realtime-data-mesh-practice.md |
| Prop-K-06-132 | 联邦治理边界 | 命题 |  |
| Prop-K-06-14 | 混合查询成本模型 | 命题 | Knowledge/06-frontier/vector-search-streaming-convergence.md |
| Prop-K-06-15 | 边缘推理延迟上界 | 命题 | Knowledge/06-frontier/edge-llm-realtime-inference.md |
| Prop-K-06-16 | 量化精度损失边界 | 命题 | Knowledge/06-frontier/edge-llm-realtime-inference.md |
| Prop-K-06-17 | 流式生成吞吐量守恒 | 命题 | Knowledge/06-frontier/edge-llm-realtime-inference.md |
| Prop-K-06-20 | (SQL完备性与表达能力权衡) | 命题 | Knowledge/06-frontier/materialize-comparison-guide.md |
| Prop-K-06-200 | 编排复杂度边界定理 | 命题 | Knowledge/06-frontier/multi-agent-streaming-orchestration.md |
| Prop-K-06-201 | 容错恢复时间边界 | 命题 | Knowledge/06-frontier/multi-agent-streaming-orchestration.md |
| Prop-K-06-202 | 动态扩展性定理 | 命题 | Knowledge/06-frontier/multi-agent-streaming-orchestration.md |
| Prop-K-06-203 | 特征计算复用率 | 命题 | Knowledge/06-frontier/realtime-feature-store-architecture.md |
| Prop-K-06-21 | 吞吐量-延迟权衡 | 命题 | Knowledge/06-frontier/realtime-ai-inference-architecture.md |
| Prop-K-06-210 | 流式 Resource 新鲜度 | 命题 | Knowledge/06-frontier/mcp-protocol-agent-streaming.md |
| Prop-K-06-211 | Tool 调用幂等性 | 命题 | Knowledge/06-frontier/mcp-protocol-agent-streaming.md |
| Prop-K-06-22 | 小团队能力扩展定理 | 命题 | Knowledge/06-frontier/realtime-ai-streaming-2026.md |
| Prop-K-06-220 | 任务状态一致性 | 命题 | Knowledge/06-frontier/a2a-protocol-agent-communication.md |
| Prop-K-06-221 | 多模态传输容量边界 | 命题 | Knowledge/06-frontier/a2a-protocol-agent-communication.md |
| Prop-K-06-230 | Agent Card 缓存一致性 | 命题 | Knowledge/06-frontier/ai-agent-a2a-protocol.md |
| Prop-K-06-231 | SSE 流式传输可靠性边界 | 命题 | Knowledge/06-frontier/ai-agent-a2a-protocol.md |
| Prop-K-06-25 | Agent 数据库启动延迟边界 | 命题 | Knowledge/06-frontier/ai-agent-database-workloads.md |
| Prop-K-06-250 | 预测准确率边界 | 命题 | Knowledge/06-frontier/realtime-digital-twin-streaming.md |
| Prop-K-06-251 | 数字孪生保真度 | 命题 | Knowledge/06-frontier/realtime-digital-twin-streaming.md |
| Prop-K-06-26 | 并发数据库实例上限 | 命题 | Knowledge/06-frontier/ai-agent-database-workloads.md |
| Prop-K-06-260 | DEX价格发现效率 | 命题 | Knowledge/06-frontier/web3-streaming-analytics-defi.md |
| Prop-K-06-261 | 匿名用户识别精度 | 命题 | Knowledge/06-frontier/web3-streaming-analytics-defi.md |
| Prop-K-06-27 | Scale-to-Zero 成本节约率 | 命题 | Knowledge/06-frontier/ai-agent-database-workloads.md |
| Prop-K-06-40 | (多模态流处理的Flink适配性): Apache Flink的以下特性使其成为多模态流处理的理想基础设施： | 命题 | Knowledge/06-frontier/multimodal-ai-streaming-architecture.md |
| Prop-K-06-41 | (异步推理模式): 为避免模型推理阻塞数据流，采用AsyncFunction模式： | 命题 | Knowledge/06-frontier/multimodal-ai-streaming-architecture.md |
| Prop-K-06-42 | 流数据库一致性级别与延迟的权衡 | 命题 | Knowledge/06-frontier/streaming-database-ecosystem-comparison.md |
| Prop-K-06-43 | 存储分离架构下的状态访问延迟 | 命题 | Knowledge/06-frontier/streaming-database-ecosystem-comparison.md |
| Prop-K-06-50 | 去中心化流处理活性保证 | 命题 |  |
| Prop-K-06-51 | 链上/链下数据一致性 | 命题 |  |
| Prop-K-06-63 | 扩缩容响应时间界限 | 命题 | Knowledge/06-frontier/serverless-stream-processing-architecture.md |
| Prop-K-06-70 | 局部性定理 | 命题 | Knowledge/06-frontier/realtime-graph-streaming-tgnn.md |
| Prop-K-06-71 | 复杂度对比 | 命题 | Knowledge/06-frontier/realtime-graph-streaming-tgnn.md |
| Prop-K-06-72 | 内存占用分析 | 命题 | Knowledge/06-frontier/realtime-graph-streaming-tgnn.md |
| Prop-K-06-73 | 数据产品自洽性条件 | 命题 | Knowledge/06-frontier/realtime-data-product-architecture.md |
| Prop-K-06-80 | Agent响应延迟边界定理 | 命题 | Knowledge/06-frontier/ai-agent-streaming-architecture.md |
| Prop-K-06-81 | 推理-行动循环复杂度边界 | 命题 | Knowledge/06-frontier/ai-agent-streaming-architecture.md |
| Prop-K-06-82 | 多Agent并行效率定理 | 命题 | Knowledge/06-frontier/ai-agent-streaming-architecture.md |
| Prop-K-06-83 | Agent状态机活性定理 | 命题 | Knowledge/06-frontier/ai-agent-streaming-architecture.md |
| Prop-K-06-90 | (血缘传递闭包)：若数据产品 $P_A$ 依赖 $P_B$，$P_B$ 依赖 $P_C$，则血缘图 $\mathcal{G}_{lineage}$ 中存在路径 $P_A \rightarrow P_B \rightarrow P_C$，影响分析的范围为： | 命题 | Knowledge/06-frontier/streaming-data-mesh-architecture.md |
| Prop-K-06-95 | Serverless成本边界 | 命题 | Knowledge/06-frontier/serverless-streaming-architecture.md |
| Prop-K-06-96 | 冷启动对延迟的影响边界 | 命题 | Knowledge/06-frontier/serverless-streaming-architecture.md |
| Prop-K-06-98 | 自动扩缩容成本效益 | 命题 | Knowledge/06-frontier/serverless-streaming-cost-optimization.md |
| Prop-K-07-01 | 测试隔离性 | 命题 | Knowledge/07-best-practices/07.07-testing-strategies-complete.md |
| Prop-K-07-02 | 时间可控性 | 命题 | Knowledge/07-best-practices/07.07-testing-strategies-complete.md |
| Prop-K-07-03 | 状态可验证性 | 命题 | Knowledge/07-best-practices/07.07-testing-strategies-complete.md |
| Prop-K-07-04 | Knowledge/07-best-practices/07.04-cost-optimization-patterns.md | 命题 |  |
| Prop-K-07-05 | Knowledge/07-best-practices/07.05-security-hardening-guide.md | 命题 |  |
| Prop-K-07-06 | Knowledge/07-best-practices/07.06-high-availability-patterns.md | 命题 |  |
| Prop-K-08-01 | Lakehouse读写分离一致性 | 命题 |  |
| Prop-K-08-12 | 治理覆盖率边界 | 命题 | Knowledge/08-standards/streaming-data-governance.md |
| Prop-K-08-13 | Schema兼容性传递性 | 命题 | Knowledge/08-standards/streaming-data-governance.md |
| Prop-K-08-14 | 合规延迟上界 | 命题 | Knowledge/08-standards/streaming-data-governance.md |
| Prop-K-08-15 | 质量维度相关性 | 命题 | Knowledge/08-standards/streaming-data-governance-quality.md |
| Prop-K-08-16 | 血缘传递的封闭性 | 命题 | Knowledge/08-standards/streaming-data-governance-quality.md |
| Prop-K-08-17 | 实时质量监控的延迟边界 | 命题 | Knowledge/08-standards/streaming-data-governance-quality.md |
| Prop-K-08-18 | 实体解析的准确率上界 | 命题 | Knowledge/08-standards/streaming-data-governance-quality.md |
| Prop-K-08-20 | 加密强度与性能权衡 | 命题 | Knowledge/08-standards/streaming-security-compliance.md |
| Prop-K-08-21 | 访问控制决策延迟 | 命题 | Knowledge/08-standards/streaming-security-compliance.md |
| Prop-K-09-01 | RAG延迟-准确性权衡 | 命题 |  |
| Cor-K-06-05 | 智能合约事件驱动活性推论 | 推论 |  |


## Flink 层级 (Flink专项)

总计: 1,437 个形式化元素

### 按类型统计

| 类型 | 数量 |
|------|------|
| 定理 | 258 |
| 定义 | 710 |
| 引理 | 242 |
| 命题 | 217 |
| 推论 | 10 |

### 完整列表

| 编号 | 名称 | 类型 | 位置 |
|------|------|------|------|
| Thm-F-01-01 | 类型一致性保证 | 定理 | Flink/flink-data-types-reference.md |
| Thm-F-01-02 | 类型推断完备性 | 定理 | Flink/flink-data-types-reference.md |
| Thm-F-01-03 | 分离存储下的 Exactly-Once 保持 | 定理 | Flink/01-concepts/flink-architecture-evolution-1x-to-2x.md |
| Thm-F-02-01 | ForSt Checkpoint一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-02 | LazyRestore正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-03 | 异步执行语义保持性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-04 | Checkpoint 效率优化界限定理 | 定理 | Flink/02-core/state-backends-deep-comparison.md |
| Thm-F-02-05 | 状态后端选择完备性 | 定理 | Flink/02-core/state-backend-evolution-analysis.md |
| Thm-F-02-06 | CBFC 安全性 (Safety) | 定理 | Flink/02-core/network-stack-evolution.md |
| Thm-F-02-10 | Debloating加速Checkpoint Barrier传播定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-12 | Delta Join V2缓存有效性定理 | 定理 |  |
| Thm-F-02-13 | VECTOR_SEARCH精度-延迟权衡边界 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-14 | Balanced Scheduling最优性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-30 | Delta Join V2缓存有效性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-31 | 多级缓存最优性定理 | 定理 | Flink/02-core/delta-join-production-guide.md |
| Thm-F-02-32 | Delta Join V2 生产可用性定理 | 定理 | Flink/02-core/delta-join-production-guide.md |
| Thm-F-02-35 | Streaming ETL端到端一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-36 | Schema演化兼容性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-37 | 乱序数据处理正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-40 | 多路Join最优计划选择定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-45 | ForSt状态后端一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-46 | ForSt增量Checkpoint正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-47 | RocksDBStateBackend 一致性定理 | 定理 | Struct/Proof-Chains-Flink-Implementation.md |
| Thm-F-02-50 | 异步算子执行语义保持性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-51 | 异步I/O并发度最优性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-52 | 异步执行顺序一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-53 | 异步超时容错正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-54 | 混合同步异步执行正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-55 | 异步资源池动态分配定理 | 定理 |  |
| Thm-F-02-56 | 自适应执行正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-57 | 数据倾斜处理有效性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-60 | State TTL过期一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-61 | TTL惰性清理正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-62 | TTL状态恢复完整性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-63 | TTL堆内存优化边界定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-64 | TTL增量清理性能定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-71 | 端到端Exactly-Once充分条件定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-72 | 两阶段提交原子性保证定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-90 | State Backend选择最优性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-91 | Checkpoint完备性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-02-92 | State TTL一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-03-01 | 动态表上连续查询的语义完整性 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-03-02 | Exactly-Once语义保证 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-03-03 | SQL Hints的优化有效性 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-03-100 | Flink SQL JSON函数SQL:2023符合性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-03-101 | MATCH_RECOGNIZE流处理完备性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-03-102 | 窗口函数RANGE框架时序正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-03-15 | Python UDF执行正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-03-20 | PTF多态处理正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-03-21 | (谓词下推正确性): 设 $\sigma_{\theta}$ 为选择算子，$\bowtie_{\phi}$ 为连接算子，若 $\theta$ 仅涉及连接左侧 $L$ 的属性，则： | 定理 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Thm-F-03-22 | (投影下推正确性): 设 $\pi_{A}$ 为投影，$\bowtie_{\phi}$ 为连接，若 $\phi$ 涉及的属性集为 $A_{\phi}$，则： | 定理 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Thm-F-03-23 | (CBO最优性边界): 设 $\mathcal{P}$ 为所有等价物理计划集合，$\hat{P}$ 为VolcanoPlanner返回的计划，则： | 定理 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Thm-F-03-24 | (Blink Planner优势): Blink Planner在以下维度严格优于Old Planner： | 定理 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Thm-F-03-25 | (批流语义一致性): 对于无时间属性的SQL查询，批执行和流执行产生逻辑等价结果： | 定理 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Thm-F-03-26 | (Join重排序代价边界): 对于 $n$ 个表的Join，最优执行顺序的代价与最差顺序的代价比值满足： | 定理 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Thm-F-03-27 | (Watermark传播正确性): 算子输出的Watermark是其输入Watermark的单调不减函数。 | 定理 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Thm-F-03-28 | (VolcanoPlanner最优性): 在统计信息准确的前提下，VolcanoPlanner通过动态规划枚举能够找到全局最优或近似最优的物理执行计划。 | 定理 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Thm-F-03-29 | (Changelog规范化正确性): Changelog规范化变换保持流处理结果的最终一致性。 | 定理 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Thm-F-03-50 | 物化表一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-03-51 | 物化表最优分桶定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-03-52 | 新鲜度推断完备性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-03-60 | VECTOR_SEARCH类型安全性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-03-61 | RAG延迟边界定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-03-62 | 混合搜索成本优化定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-03-70 | Broadcast Join可行性条件定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-03-71 | State TTL与结果正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-03-72 | JSON聚合函数内存上界定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-03-92 | SQL Hint优化正确性 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-04-01 | ES Sink 的 At-Least-Once 语义保证 | 定理 | Flink/05-ecosystem/05.01-connectors/elasticsearch-connector-complete-guide.md |
| Thm-F-04-02 | Exactly-Once 通过幂等 ID 实现 | 定理 | Flink/05-ecosystem/05.01-connectors/elasticsearch-connector-complete-guide.md |
| Thm-F-04-03 | (Change Streams Source Exactly-Once 正确性) | 定理 | Flink/05-ecosystem/05.01-connectors/mongodb-connector-complete-guide.md |
| Thm-F-04-04 | (MongoDB Sink 幂等写入保证) | 定理 | Flink/05-ecosystem/05.01-connectors/mongodb-connector-complete-guide.md |
| Thm-F-04-05 | Blue/Green 部署零停机保证 | 定理 | Flink/04-runtime/04.01-deployment/flink-k8s-operator-1.14-guide.md |
| Thm-F-04-06 | 状态一致性切换正确性 | 定理 | Flink/04-runtime/04.01-deployment/flink-k8s-operator-1.14-guide.md |
| Thm-F-04-100 | 连接器生态完备性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-04-101 | 多连接器组合一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-04-15 | (存储成本下界定理) | 定理 | Flink/05-ecosystem/05.01-connectors/diskless-kafka-cloud-native.md |
| Thm-F-04-16 | (弹性扩展边界) | 定理 | Flink/05-ecosystem/05.01-connectors/diskless-kafka-cloud-native.md |
| Thm-F-04-17 | (分层存储可靠性定理) | 定理 | Flink/05-ecosystem/05.01-connectors/diskless-kafka-cloud-native.md |
| Thm-F-04-20 | (CDC Source Exactly-Once正确性) | 定理 | Flink/05-ecosystem/05.01-connectors/04.04-cdc-debezium-integration.md |
| Thm-F-04-200 | Flink 2.4连接器生态完备性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-04-201 | 端到端Exactly-Once扩展性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-04-202 | 连接器性能优化效果量化论证 | 定理 | Flink/05-ecosystem/05.01-connectors/flink-24-connectors-guide.md |
| Thm-F-04-21 | (事务边界保证定理) | 定理 | Flink/05-ecosystem/05.01-connectors/04.04-cdc-debezium-integration.md |
| Thm-F-04-30 | Delta Lake写入一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-04-31 | Flink-Delta事务隔离性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-04-32 | 增量提交原子性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-04-33 | 流批一体存储正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-04-40 | Iceberg快照一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-04-41 | Flink-Iceberg事务隔离性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-04-42 | 隐藏分区正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-04-43 | 模式演化兼容性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-04-50 | Paimon LSM-Tree一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-04-51 | Paimon流批统一正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-04-52 | 变更日志生成正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-04-53 | Paimon合并引擎正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-04-60 | CDC端到端一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-04-61 | Schema变更传播正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-05-01 | (流处理引擎选择决策定理) | 定理 | Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-kafka-streams.md |
| Thm-F-05-02 | Schema Evolution的一致性保证 | 定理 | Flink/05-ecosystem/05.01-connectors/flink-cdc-3.6.0-guide.md |
| Thm-F-06-01 | (最优内存配置定理) | 定理 | Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md |
| Thm-F-06-02 | (并行度扩展效率定理) | 定理 | Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md |
| Thm-F-06-03 | (最优算子链配置定理) | 定理 | Flink/09-practices/09.03-performance-tuning/06.02-performance-optimization-complete.md |
| Thm-F-06-04 | (SQL查询性能下界定理) | 定理 | Flink/09-practices/09.03-performance-tuning/06.02-performance-optimization-complete.md |
| Thm-F-06-10 | Flink LLM管道正确性 | 定理 | Flink/06-ai-ml/flink-llm-realtime-inference-guide.md |
| Thm-F-06-100 | 语义检索准确率保证 | 定理 | Flink/06-ai-ml/flip-531-ai-agents-ga-guide.md |
| Thm-F-06-101 | 异步执行吞吐量下界 | 定理 | Flink/06-ai-ml/flip-531-ai-agents-ga-guide.md |
| Thm-F-06-102 | MCP Server可靠性保证 | 定理 | Flink/06-ai-ml/flip-531-ai-agents-ga-guide.md |
| Thm-F-06-11 | 流式输出等价性 | 定理 | Flink/06-ai-ml/flink-llm-realtime-inference-guide.md |
| Thm-F-06-12 | 成本优化下界 | 定理 | Flink/06-ai-ml/flink-llm-realtime-inference-guide.md |
| Thm-F-06-20 | dbt模型增量编译正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-06-21 | Flink-dbt血缘追踪完整性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-06-30 | 单元测试完备性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-06-31 | 集成测试一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-06-32 | 端到端测试正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-06-40 | 成本优化帕累托前沿定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-06-41 | 自动扩缩容成本最优性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-06-42 | FinOps单位经济学一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-06-50 | 网络层优化组合效果定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-06-51 | 序列化优化帕累托最优定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-06-52 | 分代内存管理最优性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-06-53 | 并行类加载加速定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-06-54 | 信用值流控稳定性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-06-55 | POJO序列化正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-06-56 | 分代内存管理无OOM保证定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-06-57 | ForSt一致性保证定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-06-58 | 自适应Join选择最优性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-06-59 | 升级收益边界定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-07-01 | 实时分析案例正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-07-08 | 物流实时追踪正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-07-09 | 物流异常检测定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-07-10 | 金融实时风控正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-07-11 | 金融反欺诈准确率定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-07-12 | (状态规模可扩展性): 对于状态大小 $S$（GB），系统仍能保持延迟保证的最大吞吐量 $T_{\max}$： | 定理 | Flink/09-practices/09.01-case-studies/case-financial-realtime-risk-control.md |
| Thm-F-07-30 | 智能制造IoT架构正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-07-31 | 工业数字孪生一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-07-32 | 智能制造IoT实时检测正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-07-50 | (预测精度上界定理): 在给定数据质量 $Q_{data}$ 和模型复杂度 $\mathcal{C}_{model}$ 约束下，可达到的最佳预测精度满足： | 定理 | Flink/09-practices/09.01-case-studies/case-smart-grid-energy-management.md |
| Thm-F-07-51 | (实时性保证定理): 在Flink流处理系统中，端到端延迟满足： | 定理 | Flink/09-practices/09.01-case-studies/case-smart-grid-energy-management.md |
| Thm-F-07-52 | (可再生能源渗透率上限): 在给定系统惯性和调节能力下，可再生能源渗透率上限为： | 定理 | Flink/09-practices/09.01-case-studies/case-smart-grid-energy-management.md |
| Thm-F-07-61 | 游戏反作弊检测正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-07-62 | 实时玩家匹配公平性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-07-71 | Clickstream实时分析正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-07-75 | 用户留存计算正确性 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-08-01 | 2026 Q2 任务完成定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-08-02 | Flink 2.1 前沿跟踪定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-08-03 | Flink 2.1 性能目标可达性定理 | 定理 | Flink/08-roadmap/08.01-flink-24/flink-2.1-frontier-tracking.md |
| Thm-F-08-40 | Flink 2.3 Release Scope 定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-08-41 | SSL前向安全性定理 | 定理 | Flink/08-roadmap/08.01-flink-24/flink-2.3-2.4-roadmap.md |
| Thm-F-08-50 | 版本迁移完备性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-08-51 | 版本选择决策完备性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-08-52 | 版本选择完备性定理 | 定理 | Flink/08-roadmap/08.01-flink-24/flink-version-comparison-matrix.md |
| Thm-F-08-53 | 流批一体语义保持定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-08-54 | 自适应执行最优性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-08-55 | 统一容错正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-08-56 | 批处理性能不下降定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-08-60 | 统一执行层语义等价性定理 | 定理 | Flink/08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md |
| Thm-F-08-61 | 新状态管理一致性定理 | 定理 | Flink/08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md |
| Thm-F-08-62 | 云原生弹性保证定理 | 定理 | Flink/08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md |
| Thm-F-08-63 | 向后兼容性保证定理 | 定理 | Flink/08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md |
| Thm-F-08-70 | Serverless Scale-to-Zero Correctness | 定理 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Thm-F-08-71 | Adaptive Engine Convergence | 定理 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Thm-F-08-72 | AI Agent Multi-Coordination Safety | 定理 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Thm-F-09-01 | 最优语言选择定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-09-02 | 跨语言UDF语义等价性 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-09-03 | Flink SQL优化器完备性 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-09-04 | Python UDF性能上界 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-09-10 | V2 API Backward Compatibility | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-09-11 | Scala 3 Type Safety in Flink | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-09-12 | Compile-time Type Preservation | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-09-13 | Hummock Performance Bounds | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-09-14 | Materialized View Consistency | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-09-15 | 向量搜索性能定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-09-16 | WASM Sandbox Isolation | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-09-17 | Component Composability | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-09-20 | 100x性能提升定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-09-21 | REGION优化正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-09-22 | Differential Dataflow内部一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-09-25 | Async API Throughput Scaling Theorem | 定理 | Flink/03-api/09-language-foundations/02.03-python-async-api.md |
| Thm-F-09-30 | 算子链优化定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-09-50 | WASM UDF安全性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-09-57 | ARRANGE算子索引共享定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-10-01 | 最优资源配置定理 | 定理 | Flink/04-runtime/04.01-deployment/cost-optimization-calculator.md |
| Thm-F-10-02 | Spot 实例的成本效益条件 | 定理 | Flink/04-runtime/04.01-deployment/cost-optimization-calculator.md |
| Thm-F-10-03 | 自动扩缩容的成本节约上界 | 定理 | Flink/04-runtime/04.01-deployment/cost-optimization-calculator.md |
| Thm-F-10-10 | K8s部署高可用性证明 | 定理 | Flink/04-runtime/04.01-deployment/kubernetes-deployment-production-guide.md |
| Thm-F-10-11 | 故障恢复正确性 | 定理 | Flink/04-runtime/04.01-deployment/kubernetes-deployment-production-guide.md |
| Thm-F-10-12 | 扩缩容一致性保证 | 定理 | Flink/04-runtime/04.01-deployment/kubernetes-deployment-production-guide.md |
| Thm-F-10-20 | Flink Kubernetes Operator部署一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-10-21 | Operator自动扩缩容正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-10-30 | 自动扩缩容稳定性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-10-31 | 顶点级别扩缩容最优性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-10-32 | 追赶容量完备性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-10-40 | Kubernetes Native部署的容错完备性 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-10-41 | 细粒度资源管理的最优性 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-10-42 | 蓝绿部署的零停机保证 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-10-50 | Serverless Flink GA成本最优性 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-10-51 | 状态恢复原子性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-10-52 | Scale-to-Zero可用性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-12-01 | (在线学习参数收敛性) | 定理 | Flink/06-ai-ml/online-learning-algorithms.md |
| Thm-F-12-02 | 流式推理架构正确性 | 定理 | Flink/06-ai-ml/model-serving-streaming.md |
| Thm-F-12-03 | 持续训练系统收敛性保证 | 定理 | Flink/06-ai-ml/online-learning-production.md |
| Thm-F-12-04 | A/B 测试统计有效性保证 | 定理 | Flink/06-ai-ml/online-learning-production.md |
| Thm-F-12-100 | Agent状态一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-12-101 | A2A消息可靠性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-12-102 | Agent重放等价性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-12-103 | 向量搜索类型安全性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-12-104 | ML_PREDICT容错性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-12-105 | RAG检索-生成一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-12-106 | 流式LLM集成成本下界定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-12-15 | 实时特征一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-12-16 | Feature Store物化视图正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-12-17 | 在线/离线特征一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-12-20 | PROJECT-COMPLETION-FINAL-REPORT.md | 定理 |  |
| Thm-F-12-30 | 异步推理正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-12-31 | 特征一致性约束定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-12-32 | 模型漂移检测统计保证定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-12-35 | LLM推理容错性保证定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-12-36 | RAG一致性约束定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-12-37 | LLM批处理吞吐量下界定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-12-50 | GPU算子正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-12-51 | 异构调度最优性定理 | 定理 | Flink/06-ai-ml/flink-25-gpu-acceleration.md |
| Thm-F-12-52 | GPU内存一致性定理 | 定理 | Flink/06-ai-ml/flink-25-gpu-acceleration.md |
| Thm-F-12-90 | Agent状态一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-12-91 | A2A消息可靠性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-12-92 | Agent重放等价性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-13-01 | async/sync组合正确性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-13-02 | Stream流水线性能保证定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-13-03 | Flink安全配置完备性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-13-04 | 零信任架构正确性 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-13-07 | SPIRE-Flink 集成安全性定理 | 定理 | Flink/09-practices/09.04-security/spiffe-spire-integration-guide.md |
| Thm-F-13-20 | Flink 2.4安全配置完备性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-13-21 | 零信任架构正确性证明 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-14-01 | Rust WASM UDF 性能优势定理 | 定理 | Flink/07-rust-native/flink-rust-ecosystem-trends-2026.md |
| Thm-F-14-02 | WASM-Native 引擎可扩展性定理 | 定理 | Flink/07-rust-native/flink-rust-ecosystem-trends-2026.md |
| Thm-F-14-03 | Time Travel 一致性定理 | 定理 | Flink/05-ecosystem/05.02-lakehouse/flink-iceberg-integration.md |
| Thm-F-14-04 | 统一批流结果一致性定理 | 定理 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-architecture.md |
| Thm-F-14-05 | 湖仓格式端到端 Exactly-Once 语义定理 | 定理 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-architecture.md |
| Thm-F-14-06 | 增量消费完备性定理 | 定理 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-architecture.md |
| Thm-F-14-15 | Streaming-First Lakehouse一致性定理 | 定理 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-deep-dive-2026.md |
| Thm-F-14-16 | 多格式Catalog统一治理定理 | 定理 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-deep-dive-2026.md |
| Thm-F-14-17 | S3 Tables托管服务SLA边界定理 | 定理 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-deep-dive-2026.md |
| Thm-F-14-18 | Table Format选型决策完备性定理 | 定理 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-deep-dive-2026.md |
| Thm-F-14-21 | (流式连通组件算法的正确性). 设边流 $ℰ$ 按时间戳非递减到达，算法在每个时间 $t$ 输出连通组件标识 $C_t(v)$，则： | 定理 | Flink/05-ecosystem/05.04-graph/flink-gelly-streaming-graph-processing.md |
| Thm-F-14-22 | (增量三角形计数的复杂度上界). 设图 $G$ 的最大度数为 $Δ$，流式三角形计数算法处理单条边的时间复杂度为 $O(Δ)$。 | 定理 | Flink/05-ecosystem/05.04-graph/flink-gelly-streaming-graph-processing.md |
| Thm-F-14-23 | (分区策略对局部性的影响). 对于度分布服从幂律的图，度感知分区（DGR）相比哈希分区可减少 $O(\log | 定理 | Flink/05-ecosystem/05.04-graph/flink-gelly-streaming-graph-processing.md |
| Thm-F-15-01 | 流处理可观测性完备性定理 | 定理 | Flink/04-runtime/04.03-observability/opentelemetry-streaming-observability.md |
| Thm-F-15-10 | 实时数据质量监控一致性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-15-11 | 数据质量规则验证完备性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-15-30 | OpenTelemetry集成完备性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-15-31 | 端到端延迟可追踪性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-15-32 | Watermark延迟预警定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-15-35 | SLO满足性监控定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-15-36 | 延迟异常检测定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-15-37 | 资源利用率优化定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-15-50 | 端到端可观测性完备性定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-15-51 | 背压根因定位定理 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Thm-F-15-52 | Checkpoint超时检测完备性 | 定理 | Struct/Proof-Chains-Flink-Complete.md |
| Def-F-00-01 | Flink AI Agent - FLIP-531 引入的原生 Agent 抽象，将 Flink 的流处理能力扩展到自主 AI Agent 领域。 | 定义 | Flink/00-meta/00-QUICK-START.md |
| Def-F-00-02 | Serverless Flink - 按需扩缩容至零实例，Pay-per-use 计费模式。 | 定义 | Flink/00-meta/00-QUICK-START.md |
| Def-F-00-03 | Unified Stream-Batch Execution - Flink 2.5 实现完全统一的执行引擎，消除流批边界。 | 定义 | Flink/00-meta/00-QUICK-START.md |
| Def-F-00-04 | GPU-Accelerated Stream Processing - 利用 GPU 大规模并行计算能力执行流处理算子。 | 定义 | Flink/00-meta/00-QUICK-START.md |
| Def-F-00-05 | Flink 2.5 WASM UDF GA - 基于 WASI 0.2/0.3 标准的多语言 UDF 支持。 | 定义 | Flink/00-meta/00-QUICK-START.md |
| Def-F-01-01 | 数据类型系统 | 定义 | Flink/flink-data-types-reference.md |
| Def-F-01-02 | 原子类型 (Atomic Types) | 定义 | Flink/flink-data-types-reference.md |
| Def-F-01-03 | 数值类型 (Numeric Types) | 定义 | Flink/flink-data-types-reference.md |
| Def-F-01-04 | 复合类型 (Composite Types) | 定义 | Flink/flink-data-types-reference.md |
| Def-F-01-05 | 时间类型 (Temporal Types) | 定义 | Flink/flink-data-types-reference.md |
| Def-F-01-06 | 类型转换关系 | 定义 | Flink/flink-data-types-reference.md |
| Def-F-01-25 | 嵌入式状态架构 (Embedded State Architecture) | 定义 | Flink/01-concepts/flink-architecture-evolution-1x-to-2x.md |
| Def-F-01-26 | 分离状态架构 (Disaggregated State Architecture) | 定义 | Flink/01-concepts/flink-architecture-evolution-1x-to-2x.md |
| Def-F-01-27 | 同步执行模型 (Synchronous Execution Model) | 定义 | Flink/01-concepts/flink-architecture-evolution-1x-to-2x.md |
| Def-F-01-28 | 异步执行模型 (Asynchronous Execution Model) | 定义 | Flink/01-concepts/flink-architecture-evolution-1x-to-2x.md |
| Def-F-02-01 | 内置函数体系 | 定义 | Flink/flink-built-in-functions-reference.md |
| Def-F-02-02 | 标量函数 (Scalar Functions) | 定义 | Flink/flink-built-in-functions-reference.md |
| Def-F-02-03 | 聚合函数 (Aggregate Functions) | 定义 | Flink/flink-built-in-functions-reference.md |
| Def-F-02-04 | 窗口函数 (Window Functions) | 定义 | Flink/flink-built-in-functions-reference.md |
| Def-F-02-05 | 异步执行控制器 (AEC) | 定义 | Flink/02-core/async-execution-model.md |
| Def-F-02-06 | 非阻塞状态访问 | 定义 | Flink/02-core/async-execution-model.md |
| Def-F-02-07 | 按键有序性保持 (Per-key FIFO) | 定义 | Flink/02-core/async-execution-model.md |
| Def-F-02-08 | (Changelog State Backend) → ChangelogStateBackend | 定义 | Flink/Formal-to-Code-Mapping-v2.md |
| Def-F-02-09 | ForSt存储引擎 (ForSt Storage Engine) | 定义 | Flink/02-core/forst-state-backend.md |
| Def-F-02-10 | Unified File System (UFS)层 | 定义 | Flink/02-core/forst-state-backend.md |
| Def-F-02-11 | Active State 与 Remote State | 定义 | Flink/02-core/forst-state-backend.md |
| Def-F-02-110 | 智能检查点 (Smart Checkpointing) | 定义 | Flink/02-core/smart-checkpointing-strategies.md |
| Def-F-02-111 | 自适应检查点间隔 (Adaptive Checkpoint Interval) | 定义 | Flink/02-core/smart-checkpointing-strategies.md |
| Def-F-02-112 | 负载感知调度 (Load-Aware Scheduling) | 定义 | Flink/02-core/smart-checkpointing-strategies.md |
| Def-F-02-113 | 增量检查点优化 (Incremental Checkpoint Optimization) | 定义 | Flink/02-core/smart-checkpointing-strategies.md |
| Def-F-02-114 | 局部检查点 (Partial Checkpoint) | 定义 | Flink/02-core/smart-checkpointing-strategies.md |
| Def-F-02-115 | 检查点并行度 (Checkpoint Parallelism) | 定义 | Flink/02-core/smart-checkpointing-strategies.md |
| Def-F-02-116 | 存储层优化 (Storage Layer Optimization) | 定义 | Flink/02-core/smart-checkpointing-strategies.md |
| Def-F-02-117 | 检查点成本模型 (Checkpoint Cost Model) | 定义 | Flink/02-core/smart-checkpointing-strategies.md |
| Def-F-02-12 | LazyRestore 机制 | 定义 | Flink/02-core/forst-state-backend.md |
| Def-F-02-13 | 远程 Compaction | 定义 | Flink/02-core/forst-state-backend.md |
| Def-F-02-14 | State Backend（状态后端） | 定义 | Flink/02-core/state-backends-deep-comparison.md |
| Def-F-02-15 | MemoryStateBackend（内存状态后端） | 定义 | Flink/02-core/state-backends-deep-comparison.md |
| Def-F-02-16 | FsStateBackend（文件系统状态后端） | 定义 | Flink/02-core/state-backends-deep-comparison.md |
| Def-F-02-17 | HashMapStateBackend（哈希映射状态后端） | 定义 | Flink/02-core/state-backends-deep-comparison.md |
| Def-F-02-18 | RocksDBStateBackend（RocksDB 状态后端） | 定义 | Flink/02-core/state-backends-deep-comparison.md |
| Def-F-02-19 | ForStStateBackend（ForSt 状态后端） | 定义 | Flink/02-core/state-backends-deep-comparison.md |
| Def-F-02-20 | Delta Join算子 | 定义 | Flink/02-core/delta-join.md |
| Def-F-02-21 | 双向查找Join语义 | 定义 | Flink/02-core/delta-join.md |
| Def-F-02-22 | 零中间状态策略 | 定义 | Flink/02-core/delta-join.md |
| Def-F-02-23 | Delta Join V2 - 增强型增量Join算子 | 定义 | Flink/02-core/flink-2.2-frontier-features.md |
| Def-F-02-24 | Delta Join 缓存层级架构 | 定义 | Flink/02-core/flink-2.2-frontier-features.md |
| Def-F-02-25 | VECTOR_SEARCH 向量搜索算子（规划中） | 定义 | Flink/02-core/flink-2.2-frontier-features.md |
| Def-F-02-26 | Materialized Table V2 - 可选FRESHNESS与智能推断 | 定义 | Flink/02-core/flink-2.2-frontier-features.md |
| Def-F-02-27 | MaterializedTableEnricher 扩展接口 | 定义 | Flink/02-core/flink-2.2-frontier-features.md |
| Def-F-02-28 | DISTRIBUTED BY/INTO 分桶语义 | 定义 | Flink/02-core/flink-2.2-frontier-features.md |
| Def-F-02-29 | SinkUpsertMaterializer V2 | 定义 | Flink/02-core/flink-2.2-frontier-features.md |
| Def-F-02-30 | (Netty PooledByteBufAllocator) → NettyBufferPool | 定义 | Flink/Formal-to-Code-Mapping-v2.md |
| Def-F-02-31 | (Credit-based Flow Control) → CreditBasedFlowControl | 定义 | Flink/Formal-to-Code-Mapping-v2.md |
| Def-F-02-32 | Balanced Tasks Scheduling | 定义 | Flink/02-core/flink-2.2-frontier-features.md |
| Def-F-02-33 | Event Reporting 系统 | 定义 | Flink/02-core/flink-2.2-frontier-features.md |
| Def-F-02-34 | Protobuf 4.x 序列化升级 | 定义 | Flink/02-core/flink-2.2-frontier-features.md |
| Def-F-02-40 | Delta Join V2 生产就绪定义 | 定义 | Flink/02-core/delta-join-production-guide.md |
| Def-F-02-41 | CDC 源无DELETE约束 | 定义 | Flink/02-core/delta-join-production-guide.md |
| Def-F-02-42 | 投影/过滤下推语义 | 定义 | Flink/02-core/delta-join-production-guide.md |
| Def-F-02-43 | 多级缓存架构（生产级） | 定义 | Flink/02-core/delta-join-production-guide.md |
| Def-F-02-44 | Delta Join 与 Regular Join 决策边界 | 定义 | Flink/02-core/delta-join-production-guide.md |
| Def-F-02-45 | 数据转换算子 | 定义 |  |
| Def-F-02-46 | 目标系统Sink抽象 | 定义 |  |
| Def-F-02-47 | 数据质量校验 | 定义 |  |
| Def-F-02-48 | 错误处理策略 | 定义 |  |
| Def-F-02-49 | 死信队列 | 定义 |  |
| Def-F-02-50 | (多路Join): 设流集合 $\mathcal{S} = \{S_1, S_2, \ldots, S_n\}$，其中每个流 $S_i$ 包含记录 $(k, v_i, t_i)$，$k$ 为Join Key，$v_i$ 为值，$t_i$ 为事件时间。多路Join操作 $\text{MultiJoin}_{\theta}$ 定义为： | 定义 | Flink/02-core/multi-way-join-optimization.md |
| Def-F-02-51 | (Join链): 二Join的序列组合称为Join链，记为： | 定义 | Flink/02-core/multi-way-join-optimization.md |
| Def-F-02-52 | (状态膨胀因子): 对于Join链，定义状态膨胀因子为： | 定义 | Flink/02-core/multi-way-join-optimization.md |
| Def-F-02-53 | (状态存储复杂度): 对于 $n$ 路Join，传统Join链的状态空间复杂度为： | 定义 | Flink/02-core/multi-way-join-optimization.md |
| Def-F-02-54 | (MultiJoin支持矩阵): | 定义 | Flink/02-core/multi-way-join-optimization.md |
| Def-F-02-55 | 恢复点管理 | 定义 |  |
| Def-F-02-56 | 多路Join查询图 | 定义 |  |
| Def-F-02-57 | Join树结构 | 定义 |  |
| Def-F-02-58 | 代价模型 | 定义 |  |
| Def-F-02-59 | 左深树与浓密树 | 定义 |  |
| Def-F-02-60 | 动态规划优化器 | 定义 |  |
| Def-F-02-61 | ForStStateBackend 是 Flink 2.0 引入的云原生分离式状态后端 | 定义 | Struct/Proof-Chains-Flink-Implementation.md |
| Def-F-02-62 | 统一文件系统层 (UFS - Unified File System) | 定义 | Flink/02-core/flink-2.0-forst-state-backend.md |
| Def-F-02-63 | RocksDBStateBackend 是嵌入式磁盘状态后端的形式化定义 | 定义 | Struct/Proof-Chains-Flink-Implementation.md |
| Def-F-02-64 | 即时恢复机制 (Instant Recovery) | 定义 | Flink/02-core/flink-2.0-forst-state-backend.md |
| Def-F-02-65 | 远程 Compaction 服务 (Remote Compaction Service) | 定义 | Flink/02-core/flink-2.0-forst-state-backend.md |
| Def-F-02-70 | 异步算子接口定义 | 定义 | Struct/Proof-Chains-Flink-Implementation.md |
| Def-F-02-71 | 异步结果未来 | 定义 |  |
| Def-F-02-72 | 并发度配额管理 | 定义 |  |
| Def-F-02-73 | 异步超时语义 | 定义 |  |
| Def-F-02-74 | 顺序保持模式 | 定义 | Struct/Proof-Chains-Flink-Implementation.md |
| Def-F-02-75 | 异步资源池 | 定义 | Struct/Proof-Chains-Flink-Implementation.md |
| Def-F-02-76 | 异步I/O调度器 | 定义 |  |
| Def-F-02-77 | 完成回调机制 | 定义 | Struct/Proof-Chains-Flink-Implementation.md |
| Def-F-02-78 | Watermark 正确性源码验证 | 定义 | Flink/02-core/flink-2.0-async-execution-model.md |
| Def-F-02-79 | 混合执行模式 | 定义 |  |
| Def-F-02-80 | State TTL (Time-To-Live) | 定义 | Flink/02-core/flink-state-ttl-best-practices.md |
| Def-F-02-81 | TTL 更新类型 (Update Type) | 定义 | Flink/02-core/flink-state-ttl-best-practices.md |
| Def-F-02-82 | 状态可见性 (State Visibility) | 定义 | Flink/02-core/flink-state-ttl-best-practices.md |
| Def-F-02-83 | 清理策略 (Cleanup Strategy) | 定义 | Flink/02-core/flink-state-ttl-best-practices.md |
| Def-F-02-84 | 惰性清理策略 | 定义 |  |
| Def-F-02-85 | 增量清理策略 | 定义 |  |
| Def-F-02-86 | RocksDB TTL compaction | 定义 |  |
| Def-F-02-87 | 自适应执行引擎 (Adaptive Execution Engine, AEE) | 定义 | Flink/02-core/adaptive-execution-engine-v2.md |
| Def-F-02-88 | 智能执行计划优化器 (Intelligent Execution Plan Optimizer, IEPO) | 定义 | Flink/02-core/adaptive-execution-engine-v2.md |
| Def-F-02-89 | 运行时自适应调整器 (Runtime Adaptive Adjuster, RAA) | 定义 | Flink/02-core/adaptive-execution-engine-v2.md |
| Def-F-02-90 | 数据倾斜检测器 (Skew Detector, SD) | 定义 | Flink/02-core/adaptive-execution-engine-v2.md |
| Def-F-02-91 | HashMapStateBackend 是内存状态后端的形式化定义 | 定义 | Struct/Proof-Chains-Flink-Implementation.md |
| Def-F-02-92 | Adaptive Scheduler 集成接口 | 定义 | Flink/02-core/adaptive-execution-engine-v2.md |
| Def-F-02-93 | ForStStateBackend (Flink 2.0+) | 定义 | Flink/02-core/flink-state-management-complete-guide.md |
| Def-F-02-94 | Keyed State（键控状态） | 定义 | Flink/02-core/flink-state-management-complete-guide.md |
| Def-F-02-95 | Operator State（算子状态） | 定义 | Flink/02-core/flink-state-management-complete-guide.md |
| Def-F-02-96 | Checkpoint（检查点） | 定义 | Flink/02-core/flink-state-management-complete-guide.md |
| Def-F-02-97 | State TTL（状态生存时间） | 定义 | Flink/02-core/flink-state-management-complete-guide.md |
| Def-F-02-98 | Changelog State Backend (Flink 1.15+) | 定义 | Flink/02-core/flink-state-management-complete-guide.md |
| Def-F-03-01 | 内置函数体系 (Built-in Function System) | 定义 | Flink/03-api/03.02-table-sql-api/built-in-functions-complete-list.md |
| Def-F-03-02 | 函数分类层级 | 定义 | Flink/03-api/03.02-table-sql-api/built-in-functions-complete-list.md |
| Def-F-03-03 | 类型系统层次结构 | 定义 | Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md |
| Def-F-03-04 | STRING | 定义 | Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md |
| Def-F-03-05 | VARCHAR | 定义 | Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md |
| Def-F-03-06 | CHAR | 定义 | Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md |
| Def-F-03-07 | 整数类型族 | 定义 | Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md |
| Def-F-03-08 | DECIMAL/NUMERIC | 定义 | Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md |
| Def-F-03-09 | 浮点类型 | 定义 | Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md |
| Def-F-03-10 | BOOLEAN | 定义 | Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md |
| Def-F-03-100 | ANSI SQL 2023 标准 | 定义 | Flink/03-api/03.02-table-sql-api/ansi-sql-2023-compliance-guide.md |
| Def-F-03-101 | Flink SQL 标准符合性模型 | 定义 | Flink/03-api/03.02-table-sql-api/ansi-sql-2023-compliance-guide.md |
| Def-F-03-102 | SQL/JSON 增强定义 | 定义 | Flink/03-api/03.02-table-sql-api/ansi-sql-2023-compliance-guide.md |
| Def-F-03-103 | 行模式识别 (Row Pattern Recognition) | 定义 | Flink/03-api/03.02-table-sql-api/ansi-sql-2023-compliance-guide.md |
| Def-F-03-104 | 窗口函数框架扩展 | 定义 | Flink/03-api/03.02-table-sql-api/ansi-sql-2023-compliance-guide.md |
| Def-F-03-105 | 多态表函数 (Polymorphic Table Functions) | 定义 | Flink/03-api/03.02-table-sql-api/ansi-sql-2023-compliance-guide.md |
| Def-F-03-11 | 二进制类型族 | 定义 | Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md |
| Def-F-03-12 | ARRAY | 定义 | Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md |
| Def-F-03-13 | MAP | 定义 | Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md |
| Def-F-03-14 | ROW | 定义 | Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md |
| Def-F-03-15 | DATE | 定义 | Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md |
| Def-F-03-16 | TIME | 定义 | Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md |
| Def-F-03-17 | TIMESTAMP | 定义 | Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md |
| Def-F-03-18 | TIMESTAMP WITH LOCAL TIME ZONE | 定义 | Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md |
| Def-F-03-19 | INTERVAL | 定义 | Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md |
| Def-F-03-20 | 隐式类型转换 | 定义 | Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md |
| Def-F-03-21 | CAST表达式 | 定义 | Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md |
| Def-F-03-22 | (UDF执行模型差异): 设 $\mathcal{U}_{java}$ 为Java UDF，$\mathcal{U}_{py}$ 为Python UDF，则两者执行模型差异可定义为： | 定义 | Flink/03-api/03.02-table-sql-api/flink-python-udf.md |
| Def-F-03-30 | Process Table Function (PTF) | 定义 | Flink/03-api/03.02-table-sql-api/flink-process-table-functions.md |
| Def-F-03-31 | 托管状态 (Managed State) | 定义 | Flink/03-api/03.02-table-sql-api/flink-process-table-functions.md |
| Def-F-03-32 | 状态转换函数 (State Transition) | 定义 | Flink/03-api/03.02-table-sql-api/flink-process-table-functions.md |
| Def-F-03-33 | PTF与标准SQL函数对比 | 定义 | Flink/03-api/03.02-table-sql-api/flink-process-table-functions.md |
| Def-F-03-34 | PTF设计目标 | 定义 | Flink/03-api/03.02-table-sql-api/flink-process-table-functions.md |
| Def-F-03-35 | (逻辑计划): 逻辑计划 $LP$ 是与执行引擎无关的关系代数表达式树，满足： | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-36 | (物理计划): 物理计划 $PP$ 是绑定到特定执行引擎的计划，满足： | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-37 | (Flink SQL优化流水线): Flink SQL优化器采用分层架构： | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-38 | (Blink Planner架构): Blink Planner是Flink 1.9+引入的现代化优化器： | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-39 | (语义等价性): 两个关系代数表达式 $E_1$ 和 $E_2$ 语义等价，记作 $E_1 \equiv E_2$，当且仅当： | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-40 | (代价函数): 物理计划 $PP$ 的代价定义为： | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-41 | (SQL-关系代数映射): Flink SQL基于Calcite实现与ISO/IEC 9075 SQL标准的关系代数映射： | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-42 | (批流物理算子映射): | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-43 | (谓词下推): 将过滤条件下推至数据源或更早执行位置，减少中间数据量。 | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-44 | (投影下推): 裁剪不需要的列，减少IO和网络传输。 | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-45 | (分区裁剪): 利用分区列谓词，仅扫描匹配分区。 | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-46 | (两阶段聚合): 将聚合拆分为局部聚合（Local）和全局聚合（Global），减少Shuffle数据量。 | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-47 | (Watermark语义): Watermark $w(t)$ 是事件时间 $t$ 的单调不减下界函数，标记所有时间戳 $\leq w(t)$ 的事件已到达。 | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-48 | (状态算子分类): Flink流SQL算子按状态需求分类： | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-49 | (Changelog语义): Flink流SQL使用Changelog模型处理数据变更 | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-50 | (Retraction机制): 当聚合键值变化时，Flink需要发送撤回消息（-U）再发送新值（+U）。 | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-51 | (视图展开): 将视图定义内联到查询中，为后续优化提供完整上下文。 | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-52 | (子查询去关联化): 将关联子查询转换为非关联形式，提升并行度。 | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-53 | (物化视图匹配): 若物化视图 $MV$ 包含查询 $Q$ 所需数据，可将 $Q$ 重写到 $MV$。 | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-54 | (EXPLAIN模式): Flink提供多级执行计划展示： | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-55 | (SQL Hints): Flink支持通过Hints影响优化器决策 | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-56 | (统计信息类型): Flink CBO依赖的统计信息： | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-57 | (VolcanoPlanner) → FlinkOptimizer | 定义 | Flink/Formal-to-Code-Mapping-v2.md |
| Def-F-03-58 | (MEMO结构): MEMO是VolcanoPlanner内部用于存储等价关系表达式组的数据结构，采用组(Group)和表达式(Expression)两级组织： | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-59 | (RelTraitDef): RelTraitDef定义了物理算子所需满足的物理属性约束： | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-60 | (CostFactory): CostFactory定义多维代价计算模型： | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-61 | (Flink优化规则分类): Flink在Calcite基础规则之上，实现了针对流计算特性的专用优化规则，涵盖Watermark传播、Changelog处理、状态后端选择等维度 | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-62 | (WatermarkPushDownRule): Watermark传播优化规则将Watermark生成算子下推至Source节点，减少中间算子的Watermark处理开销。 | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-63 | (ChangelogNormalizeRule): Changelog规范化规则优化Upsert/Retract流的转换过程，减少不必要的Retraction消息生成。 | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-64 | (StateBackendRewriteRule): 状态后端重写规则根据状态大小、访问模式自动选择HashMapStateBackend或RocksDBStateBackend。 | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-65 | (Flink Join优化规则组): Flink实现针对流/批场景的Join算法选择规则 | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md |
| Def-F-03-70 | 物化表 (Materialized Table) | 定义 | Flink/03-api/03.02-table-sql-api/flink-materialized-table-deep-dive.md |
| Def-F-03-71 | 新鲜度语义 (Freshness Semantics) | 定义 | Flink/03-api/03.02-table-sql-api/flink-materialized-table-deep-dive.md |
| Def-F-03-72 | 物化表与传统物化视图对比 | 定义 | Flink/03-api/03.02-table-sql-api/flink-materialized-table-deep-dive.md |
| Def-F-03-73 | 分桶策略 (Distribution Strategy) | 定义 | Flink/03-api/03.02-table-sql-api/flink-materialized-table-deep-dive.md |
| Def-F-03-80 | 向量搜索 (Vector Search) | 定义 | Flink/03-api/03.02-table-sql-api/flink-vector-search-rag.md |
| Def-F-03-81 | 向量嵌入 (Vector Embeddings) | 定义 | Flink/03-api/03.02-table-sql-api/flink-vector-search-rag.md |
| Def-F-03-82 | 相似度度量 (Similarity Metrics) | 定义 | Flink/03-api/03.02-table-sql-api/flink-vector-search-rag.md |
| Def-F-03-83 | 检索增强生成 (RAG) | 定义 | Flink/03-api/03.02-table-sql-api/flink-vector-search-rag.md |
| Def-F-03-84 | 向量数据库集成 | 定义 | Flink/03-api/03.02-table-sql-api/flink-vector-search-rag.md |
| Def-F-03-85 | 向量索引算法 | 定义 | Flink/03-api/03.02-table-sql-api/flink-vector-search-rag.md |
| Def-F-03-90 | SQL Hint | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-hints-optimization.md |
| Def-F-03-91 | Flink SQL Hint 分类体系 | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-hints-optimization.md |
| Def-F-03-92 | Join Hint 语义 | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-hints-optimization.md |
| Def-F-03-93 | State Hint 语义 | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-hints-optimization.md |
| Def-F-03-94 | JSON函数族（Flink 2.2增强） | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-hints-optimization.md |
| Def-F-03-95 | 执行计划（Execution Plan） | 定义 | Flink/03-api/03.02-table-sql-api/flink-sql-hints-optimization.md |
| Def-F-04-01 | Elasticsearch Sink | 定义 | Flink/05-ecosystem/05.01-connectors/elasticsearch-connector-complete-guide.md |
| Def-F-04-02 | 索引与文档模型 | 定义 | Flink/05-ecosystem/05.01-connectors/elasticsearch-connector-complete-guide.md |
| Def-F-04-03 | 批量写入机制 (Bulk API) | 定义 | Flink/05-ecosystem/05.01-connectors/elasticsearch-connector-complete-guide.md |
| Def-F-04-04 | 幂等写入语义 | 定义 | Flink/05-ecosystem/05.01-connectors/elasticsearch-connector-complete-guide.md |
| Def-F-04-05 | (Schema 兼容性契约) | 定义 | Flink/05-ecosystem/05.01-connectors/kafka-integration-patterns.md |
| Def-F-04-06 | (MongoDB Source 定义) | 定义 | Flink/05-ecosystem/05.01-connectors/mongodb-connector-complete-guide.md |
| Def-F-04-07 | (MongoDB Sink 定义) | 定义 | Flink/05-ecosystem/05.01-connectors/mongodb-connector-complete-guide.md |
| Def-F-04-08 | (集合/文档模型) | 定义 | Flink/05-ecosystem/05.01-connectors/mongodb-connector-complete-guide.md |
| Def-F-04-09 | (Change Streams CDC) | 定义 | Flink/05-ecosystem/05.01-connectors/mongodb-connector-complete-guide.md |
| Def-F-04-10 | Fluss架构 | 定义 | Flink/05-ecosystem/05.01-connectors/fluss-integration.md |
| Def-F-04-100 | (Flink 连接器形式化定义) | 定义 | Flink/05-ecosystem/05.01-connectors/flink-connectors-ecosystem-complete-guide.md |
| Def-F-04-101 | (连接器交付保证语义) | 定义 | Flink/05-ecosystem/05.01-connectors/flink-connectors-ecosystem-complete-guide.md |
| Def-F-04-102 | (Source 连接器接口契约) | 定义 | Flink/05-ecosystem/05.01-connectors/flink-connectors-ecosystem-complete-guide.md |
| Def-F-04-103 | (Sink 连接器接口契约) | 定义 | Flink/05-ecosystem/05.01-connectors/flink-connectors-ecosystem-complete-guide.md |
| Def-F-04-104 | (连接器生态分层模型) | 定义 | Flink/05-ecosystem/05.01-connectors/flink-connectors-ecosystem-complete-guide.md |
| Def-F-04-11 | 流式存储语义 | 定义 | Flink/05-ecosystem/05.01-connectors/fluss-integration.md |
| Def-F-04-12 | 实时分析优化 | 定义 | Flink/05-ecosystem/05.01-connectors/fluss-integration.md |
| Def-F-04-15 | DefaultScheduler | 定义 | Flink/04-runtime/04.01-deployment/evolution/scheduling-evolution.md |
| Def-F-04-16 | LegacyScheduler | 定义 | Flink/04-runtime/04.01-deployment/evolution/scheduling-evolution.md |
| Def-F-04-17 | DeclarativeScheduler | 定义 | Flink/04-runtime/04.01-deployment/evolution/scheduling-evolution.md |
| Def-F-04-18 | AdaptiveScheduler | 定义 | Flink/04-runtime/04.01-deployment/evolution/scheduling-evolution.md |
| Def-F-04-19 | AdaptiveScheduler V2 (Flink 2.0) | 定义 | Flink/04-runtime/04.01-deployment/evolution/scheduling-evolution.md |
| Def-F-04-20 | (CloudEvents 规范) | 定义 | Flink/05-ecosystem/05.01-connectors/cloudevents-integration-guide.md |
| Def-F-04-200 | Flink 2.4 连接器生态定义 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-24-connectors-guide.md |
| Def-F-04-201 | 原生连接器与外部连接器分类 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-24-connectors-guide.md |
| Def-F-04-202 | Kafka 3.x 原生协议支持 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-24-connectors-guide.md |
| Def-F-04-203 | Paimon 连接器增强语义 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-24-connectors-guide.md |
| Def-F-04-204 | Iceberg V2 表格式规范 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-24-connectors-guide.md |
| Def-F-04-205 | Fluss 统一流存储连接器 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-24-connectors-guide.md |
| Def-F-04-206 | CDC 3.0 管道连接器 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-24-connectors-guide.md |
| Def-F-04-207 | 连接器性能分级模型 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-24-connectors-guide.md |
| Def-F-04-21 | (CloudEvents 核心属性) | 定义 | Flink/05-ecosystem/05.01-connectors/cloudevents-integration-guide.md |
| Def-F-04-22 | (CloudEvents 序列化格式) | 定义 | Flink/05-ecosystem/05.01-connectors/cloudevents-integration-guide.md |
| Def-F-04-23 | (事件网格适配器) | 定义 | Flink/05-ecosystem/05.01-connectors/cloudevents-integration-guide.md |
| Def-F-04-24 | 流量切换策略 (Traffic Switching Strategy) | 定义 | Flink/04-runtime/04.01-deployment/flink-k8s-operator-1.14-guide.md |
| Def-F-04-25 | 状态版本兼容性矩阵 | 定义 | Flink/04-runtime/04.01-deployment/flink-k8s-operator-1.14-guide.md |
| Def-F-04-30 | (CDC形式化定义) | 定义 | Flink/05-ecosystem/05.01-connectors/04.04-cdc-debezium-integration.md |
| Def-F-04-31 | (日志型CDC语义) | 定义 | Flink/05-ecosystem/05.01-connectors/04.04-cdc-debezium-integration.md |
| Def-F-04-32 | (Debezium架构形式化) | 定义 | Flink/05-ecosystem/05.01-connectors/04.04-cdc-debezium-integration.md |
| Def-F-04-33 | (CDC事件结构) | 定义 | Flink/05-ecosystem/05.01-connectors/04.04-cdc-debezium-integration.md |
| Def-F-04-34 | (Schema变更事件) | 定义 | Flink/05-ecosystem/05.01-connectors/04.04-cdc-debezium-integration.md |
| Def-F-04-40 | (Delta Lake 表格式形式化) | 定义 | Flink/05-ecosystem/05.01-connectors/flink-delta-lake-integration.md |
| Def-F-04-41 | (Lakehouse 架构定义) | 定义 | Flink/05-ecosystem/05.01-connectors/flink-delta-lake-integration.md |
| Def-F-04-42 | (ACID 事务协议) | 定义 | Flink/05-ecosystem/05.01-connectors/flink-delta-lake-integration.md |
| Def-F-04-43 | (Time Travel 与版本控制) | 定义 | Flink/05-ecosystem/05.01-connectors/flink-delta-lake-integration.md |
| Def-F-04-44 | (Schema 演进机制) | 定义 | Flink/05-ecosystem/05.01-connectors/flink-delta-lake-integration.md |
| Def-F-04-45 | (Flink-Delta Source 语义) | 定义 | Flink/05-ecosystem/05.01-connectors/flink-delta-lake-integration.md |
| Def-F-04-46 | (Flink-Delta Sink 语义) | 定义 | Flink/05-ecosystem/05.01-connectors/flink-delta-lake-integration.md |
| Def-F-04-47 | (CDC Merge 语义) | 定义 | Flink/05-ecosystem/05.01-connectors/flink-delta-lake-integration.md |
| Def-F-04-50 | CDC (Change Data Capture) 形式化定义 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-cdc-3.0-data-integration.md |
| Def-F-04-51 | Flink CDC 3.0 定义 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-cdc-3.0-data-integration.md |
| Def-F-04-52 | Pipeline API 定义 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-cdc-3.0-data-integration.md |
| Def-F-04-53 | Schema Evolution 定义 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-cdc-3.0-data-integration.md |
| Def-F-04-54 | 行级删除 (Row-Level Deletes) 形式化 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-iceberg-integration.md |
| Def-F-04-55 | Flink-Iceberg Source 语义 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-iceberg-integration.md |
| Def-F-04-56 | Flink-Iceberg Sink 语义 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-iceberg-integration.md |
| Def-F-04-57 | 时间旅行 (Time Travel) 形式化 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-iceberg-integration.md |
| Def-F-04-60 | Apache Paimon 形式化定义 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-paimon-integration.md |
| Def-F-04-61 | 流式 Lakehouse 定义 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-paimon-integration.md |
| Def-F-04-62 | LSM-Tree 增量日志模型 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-paimon-integration.md |
| Def-F-04-63 | 湖存储格式 (ORC/Parquet/Avro) | 定义 | Flink/05-ecosystem/05.01-connectors/flink-paimon-integration.md |
| Def-F-04-64 | 增量快照 (Incremental Snapshot) | 定义 | Flink/05-ecosystem/05.01-connectors/flink-paimon-integration.md |
| Def-F-04-65 | Changelog Producer 类型 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-paimon-integration.md |
| Def-F-04-66 | 分区与桶 (Partition & Bucket) | 定义 | Flink/05-ecosystem/05.01-connectors/flink-paimon-integration.md |
| Def-F-04-67 | Compaction 策略 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-paimon-integration.md |
| Def-F-04-70 | CDC变更数据捕获 | 定义 |  |
| Def-F-04-71 | 数据管道同步语义 | 定义 |  |
| Def-F-04-72 | Schema Registry集成 | 定义 |  |
| Def-F-04-73 | 端到端数据一致性 | 定义 |  |
| Def-F-05-01 | (流处理引擎部署架构模型) | 定义 | Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-kafka-streams.md |
| Def-F-05-02 | (嵌入式流处理与独立集群流处理) | 定义 | Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-kafka-streams.md |
| Def-F-05-03 | (Kafka Streams 拓扑与算子) | 定义 | Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-kafka-streams.md |
| Def-F-05-04 | 本地状态与Kafka日志 | 定义 | Flink/09-practices/09.03-performance-tuning/05-vs-competitors/linkedin-samza-deep-dive.md |
| Def-F-05-05 | YARN与Kubernetes部署 | 定义 | Flink/09-practices/09.03-performance-tuning/05-vs-competitors/linkedin-samza-deep-dive.md |
| Def-F-05-06 | Transform VARIANT类型与JSON解析定义 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-cdc-3.6.0-guide.md |
| Def-F-05-07 | 路由配置正则表达式支持定义 | 定义 | Flink/05-ecosystem/05.01-connectors/flink-cdc-3.6.0-guide.md |
| Def-F-06-01 | (性能调优维度空间) | 定义 | Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md |
| Def-F-06-02 | (反压传播系数) | 定义 | Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md |
| Def-F-06-03 | (状态访问局部性) | 定义 | Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md |
| Def-F-06-04 | (检查点同步开销) | 定义 | Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md |
| Def-F-06-05 | (性能基准测试框架) | 定义 | Flink/09-practices/09.03-performance-tuning/06.02-performance-optimization-complete.md |
| Def-F-06-06 | (算子链效率系数) | 定义 | Flink/09-practices/09.03-performance-tuning/06.02-performance-optimization-complete.md |
| Def-F-06-07 | (SQL查询执行效率指标) | 定义 | Flink/09-practices/09.03-performance-tuning/06.02-performance-optimization-complete.md |
| Def-F-06-08 | (连接器吞吐模型) | 定义 | Flink/09-practices/09.03-performance-tuning/06.02-performance-optimization-complete.md |
| Def-F-06-09 | (端到端延迟分解) | 定义 | Flink/09-practices/09.03-performance-tuning/06.02-performance-optimization-complete.md |
| Def-F-06-10 | (总体拥有成本 TCO) | 定义 | Flink/09-practices/09.03-performance-tuning/flink-tco-cost-optimization-guide.md |
| Def-F-06-100 | Flink Agents 0.2.x 版本定义 | 定义 | Flink/06-ai-ml/flip-531-ai-agents-ga-guide.md |
| Def-F-06-101 | Embedding Models 支持 | 定义 | Flink/06-ai-ml/flip-531-ai-agents-ga-guide.md |
| Def-F-06-102 | Vector Stores 集成 | 定义 | Flink/06-ai-ml/flip-531-ai-agents-ga-guide.md |
| Def-F-06-103 | MCP Server 支持 | 定义 | Flink/06-ai-ml/flip-531-ai-agents-ga-guide.md |
| Def-F-06-104 | Java异步执行框架 | 定义 | Flink/06-ai-ml/flip-531-ai-agents-ga-guide.md |
| Def-F-06-105 | AI Agent运行时架构 (0.2.x) | 定义 | Flink/06-ai-ml/flip-531-ai-agents-ga-guide.md |
| Def-F-06-11 | (Flink 成本模型) | 定义 | Flink/09-practices/09.03-performance-tuning/flink-tco-cost-optimization-guide.md |
| Def-F-06-12 | (隐性成本) | 定义 | Flink/09-practices/09.03-performance-tuning/flink-tco-cost-optimization-guide.md |
| Def-F-06-13 | (云资源单位成本) | 定义 | Flink/09-practices/09.03-performance-tuning/flink-tco-cost-optimization-guide.md |
| Def-F-06-14 | (FinOps) | 定义 | Flink/09-practices/09.03-performance-tuning/flink-tco-cost-optimization-guide.md |
| Def-F-06-20 | (dbt 核心抽象) | 定义 | Flink/09-practices/09.03-performance-tuning/flink-dbt-integration.md |
| Def-F-06-21 | (流式 dbt 模型) | 定义 | Flink/09-practices/09.03-performance-tuning/flink-dbt-integration.md |
| Def-F-06-22 | (物化策略语义) | 定义 | Flink/09-practices/09.03-performance-tuning/flink-dbt-integration.md |
| Def-F-06-23 | (dbt-Confluent 适配器架构) | 定义 | Flink/09-practices/09.03-performance-tuning/flink-dbt-integration.md |
| Def-F-06-24 | (增量物化模式) | 定义 | Flink/09-practices/09.03-performance-tuning/flink-dbt-integration.md |
| Def-F-06-30 | (流处理测试复杂度): 流处理系统的测试复杂度 $C_{stream}$ 定义为： | 定义 | Flink/09-practices/09.03-performance-tuning/stream-processing-testing-strategies.md |
| Def-F-06-300 | Flink Agent工作流引擎 | 定义 | Flink/06-ai-ml/flink-agent-workflow-engine.md |
| Def-F-06-301 | Agent工作流定义 (Agent Workflow Definition) | 定义 | Flink/06-ai-ml/flink-agent-workflow-engine.md |
| Def-F-06-302 | Agent节点类型 (Agent Node Types) | 定义 | Flink/06-ai-ml/flink-agent-workflow-engine.md |
| Def-F-06-303 | 状态快照与恢复 (State Snapshot and Recovery) | 定义 | Flink/06-ai-ml/flink-agent-workflow-engine.md |
| Def-F-06-304 | 动态工作流编排 (Dynamic Workflow Orchestration) | 定义 | Flink/06-ai-ml/flink-agent-workflow-engine.md |
| Def-F-06-31 | (测试金字塔 - 流处理版本): 流处理测试金字塔包含三个层次： | 定义 | Flink/09-practices/09.03-performance-tuning/stream-processing-testing-strategies.md |
| Def-F-06-32 | (确定性重放 - Deterministic Replay): 给定相同的输入事件序列 $E = \{e_1, e_2, ..., e_n\}$ 和系统配置 $C$，流处理系统 $S$ 的输出 $O$ 满足： | 定义 | Flink/09-practices/09.03-performance-tuning/stream-processing-testing-strategies.md |
| Def-F-06-33 | (水印边界 - Watermark Boundary): 对于事件时间窗口 $W = | 定义 | Flink/09-practices/09.03-performance-tuning/stream-processing-testing-strategies.md |
| Def-F-06-34 | (状态一致性 - State Consistency): 在检查点 $cp$ 之后，系统状态 $State_{cp}$ 满足： | 定义 | Flink/09-practices/09.03-performance-tuning/stream-processing-testing-strategies.md |
| Def-F-06-35 | (测试数据生成器): 测试数据生成器 $G$ 是一个函数： | 定义 | Flink/09-practices/09.03-performance-tuning/stream-processing-testing-strategies.md |
| Def-F-06-40 | (流处理成本模型) | 定义 | Flink/09-practices/09.03-performance-tuning/stream-processing-cost-optimization.md |
| Def-F-06-41 | (FinOps框架) | 定义 | Flink/09-practices/09.03-performance-tuning/stream-processing-cost-optimization.md |
| Def-F-06-42 | (云成本分摊Unit Economics) | 定义 | Flink/09-practices/09.03-performance-tuning/stream-processing-cost-optimization.md |
| Def-F-06-43 | (自动扩缩容成本函数) | 定义 | Flink/09-practices/09.03-performance-tuning/stream-processing-cost-optimization.md |
| Def-F-06-50 | Flink LLM推理管道 | 定义 | Flink/06-ai-ml/flink-llm-realtime-inference-guide.md |
| Def-F-06-51 | 异步LLM推理算子 | 定义 | Flink/06-ai-ml/flink-llm-realtime-inference-guide.md |
| Def-F-06-52 | 会话状态管理 | 定义 | Flink/06-ai-ml/flink-llm-realtime-inference-guide.md |
| Def-F-06-53 | 模型路由策略 | 定义 | Flink/06-ai-ml/flink-llm-realtime-inference-guide.md |
| Def-F-06-54 | 流式响应处理 | 定义 | Flink/06-ai-ml/flink-llm-realtime-inference-guide.md |
| Def-F-06-55 | 分代内存池 | 定义 |  |
| Def-F-06-56 | ForSt StateBackend | 定义 |  |
| Def-F-07-01 | (实时推荐系统 Real-time Recommendation System): 实时推荐系统是一个五元组 $\mathcal{R} = (\mathcal{U}, \mathcal{I}, \mathcal{C}, \mathcal{F}, \mathcal{P})$，其中： | 定义 | Flink/09-practices/09.01-case-studies/case-ecommerce-realtime-recommendation.md |
| Def-F-07-02 | (实时协同过滤 Real-time Collaborative Filtering): 基于隐语义模型的实时协同过滤定义为： | 定义 | Flink/09-practices/09.01-case-studies/case-ecommerce-realtime-recommendation.md |
| Def-F-07-03 | (域数据产品 Domain Data Product): 在Data Mesh架构中，域数据产品是自包含的数据单元，定义为三元组 $\mathcal{D} = (\mathcal{S}, \mathcal{I}, \mathcal{O})$： | 定义 | Flink/09-practices/09.01-case-studies/case-ecommerce-realtime-recommendation.md |
| Def-F-07-10 | (实时风控系统): 实时风控系统是一个六元组 $\mathcal{R} = (E, S, \mathcal{F}, \mathcal{D}, \mathcal{A}, \tau)$，其中： | 定义 | Flink/09-practices/09.01-case-studies/case-financial-realtime-risk-control.md |
| Def-F-07-11 | (欺诈检测模型): 欺诈检测模型是一个概率分类器： | 定义 | Flink/09-practices/09.01-case-studies/case-financial-realtime-risk-control.md |
| Def-F-07-12 | (域所有权): 在Data Mesh架构中，金融数据域定义为： | 定义 | Flink/09-practices/09.01-case-studies/case-financial-realtime-risk-control.md |
| Def-F-07-211 | (社交媒体事件流 Social Media Event Stream): 社交媒体事件流是用户生成内容的时序序列，定义为六元组 $\mathcal{S} = (\mathcal{U}, \mathcal{P}, \mathcal{C}, \mathcal{I}, \mathcal{T}, \mathcal{R})$，其中： | 定义 | Flink/09-practices/09.01-case-studies/case-social-media-analytics.md |
| Def-F-07-212 | (实时情感分析 Real-time Sentiment Analysis): 实时情感分析是映射函数 $\mathcal{A}: \mathcal{P} \times \mathcal{T} \rightarrow | 定义 | Flink/09-practices/09.01-case-studies/case-social-media-analytics.md |
| Def-F-07-213 | (趋势检测 Trend Detection): 趋势是话题热度随时间变化的显著上升模式。趋势检测定义为二元判定函数： | 定义 | Flink/09-practices/09.01-case-studies/case-social-media-analytics.md |
| Def-F-07-214 | (影响力传播 Influence Propagation): 影响力在用户社交网络中的传播遵循独立级联模型。用户 $u$ 在时间 $t$ 被激活的概率： | 定义 | Flink/09-practices/09.01-case-studies/case-social-media-analytics.md |
| Def-F-07-215 | (动态社交图谱 Dynamic Social Graph): 社交图谱是在线更新的有向图 $\mathcal{G}(t) = (\mathcal{V}(t), \mathcal{E}(t), \mathcal{W}(t))$： | 定义 | Flink/09-practices/09.01-case-studies/case-social-media-analytics.md |
| Def-F-07-221 | (金融交易图 Financial Transaction Graph): 金融交易图是动态异构图 $\mathcal{G}(t) = (\mathcal{V}, \mathcal{E}(t), \mathcal{X}, \mathcal{T})$，其中： | 定义 | Flink/09-practices/09.01-case-studies/case-fraud-detection-advanced.md |
| Def-F-07-222 | (欺诈模式 Fraud Pattern): 欺诈模式是交易序列上的异常子图结构，定义为四元组 $\mathcal{P} = (\mathcal{S}, \phi, \theta, \tau)$： | 定义 | Flink/09-practices/09.01-case-studies/case-fraud-detection-advanced.md |
| Def-F-07-223 | (实时风险评分 Real-time Risk Score): 交易级别的风险评分是多元函数： | 定义 | Flink/09-practices/09.01-case-studies/case-fraud-detection-advanced.md |
| Def-F-07-224 | (欺诈检测CEP模式 Fraud CEP Pattern): CEP模式用于检测时序上的异常行为序列： | 定义 | Flink/09-practices/09.01-case-studies/case-fraud-detection-advanced.md |
| Def-F-07-225 | (实时图嵌入 Real-time Graph Embedding): 图嵌入是映射函数 $f_{GNN}: \mathcal{V} \times \mathcal{G} \rightarrow \mathbb{R}^d$，将节点映射到低维向量空间： | 定义 | Flink/09-practices/09.01-case-studies/case-fraud-detection-advanced.md |
| Def-F-07-231 | (供应链事件流 Supply Chain Event Stream): 供应链事件流是物流、生产、库存状态的时序序列，定义为七元组 $\mathcal{S} = (\mathcal{E}, \mathcal{L}, \mathcal{T}, \mathcal{P}, \mathcal{I}, \mathcal{C}, \mathcal{W})$： | 定义 | Flink/09-practices/09.01-case-studies/case-supply-chain-optimization.md |
| Def-F-07-232 | (实时库存状态 Real-time Inventory State): 位置 $l$ 产品 $p$ 在时刻 $t$ 的库存水平： | 定义 | Flink/09-practices/09.01-case-studies/case-supply-chain-optimization.md |
| Def-F-07-233 | (实时需求预测 Real-time Demand Forecasting): 需求预测是基于历史数据和实时信号的函数： | 定义 | Flink/09-practices/09.01-case-studies/case-supply-chain-optimization.md |
| Def-F-07-234 | (实时路径优化 Real-time Route Optimization): 对于配送请求集合 $\mathcal{R}$，路径优化求解： | 定义 | Flink/09-practices/09.01-case-studies/case-supply-chain-optimization.md |
| Def-F-07-235 | (供应链风险指数 Supply Chain Risk Index): 综合风险评分函数： | 定义 | Flink/09-practices/09.01-case-studies/case-supply-chain-optimization.md |
| Def-F-07-241 | (城市IoT数据空间 Urban IoT Data Space): 城市IoT数据空间是异构数据源的联合空间，定义为八元组 $\mathcal{U} = (\mathcal{S}, \mathcal{L}, \mathcal{T}, \mathcal{M}, \mathcal{V}, \mathcal{E}, \mathcal{C}, \mathcal{R})$： | 定义 | Flink/09-practices/09.01-case-studies/case-smart-city-iot.md |
| Def-F-07-242 | (城市数字孪生 City Digital Twin): 城市数字孪生是物理城市的实时镜像，定义为： | 定义 | Flink/09-practices/09.01-case-studies/case-smart-city-iot.md |
| Def-F-07-243 | (城市治理决策规则 Urban Governance Rules): 决策规则是条件-动作映射： | 定义 | Flink/09-practices/09.01-case-studies/case-smart-city-iot.md |
| Def-F-07-244 | (跨域事件关联 Cross-domain Event Correlation): 跨域关联发现因果或相关关系： | 定义 | Flink/09-practices/09.01-case-studies/case-smart-city-iot.md |
| Def-F-07-245 | (城市健康指数 City Health Index): 综合评估城市运行状态的指标： | 定义 | Flink/09-practices/09.01-case-studies/case-smart-city-iot.md |
| Def-F-07-251 | (患者生理数据流 Patient Physiological Data Stream): 患者生理数据流是连续监测信号的时间序列，定义为五元组 $\mathcal{P} = (\mathcal{V}, \mathcal{M}, \mathcal{T}, \mathcal{F}, \mathcal{C})$： | 定义 | Flink/09-practices/09.01-case-studies/case-healthcare-monitoring.md |
| Def-F-07-252 | (生理异常检测 Physiological Anomaly Detection): 异常检测是分类函数： | 定义 | Flink/09-practices/09.01-case-studies/case-healthcare-monitoring.md |
| Def-F-07-253 | (早期预警评分 Early Warning Score): 综合评分系统量化患者恶化风险： | 定义 | Flink/09-practices/09.01-case-studies/case-healthcare-monitoring.md |
| Def-F-07-254 | (生理趋势分析 Physiological Trend Analysis): 趋势分析检测体征变化方向： | 定义 | Flink/09-practices/09.01-case-studies/case-healthcare-monitoring.md |
| Def-F-07-255 | (患者状态相似度 Patient State Similarity): 基于历史数据的相似患者检索： | 定义 | Flink/09-practices/09.01-case-studies/case-healthcare-monitoring.md |
| Def-F-07-261 | (智能电网数据空间 Smart Grid Data Space): 电网数据空间是电力系统运行数据的联合空间，定义为七元组 $\mathcal{G} = (\mathcal{N}, \mathcal{L}, \mathcal{M}, \mathcal{T}, \mathcal{D}, \mathcal{G}, \mathcal{C})$： | 定义 | Flink/09-practices/09.01-case-studies/case-energy-grid-optimization.md |
| Def-F-07-262 | (多时间尺度负载预测 Multi-timescale Load Forecasting): 负载预测在不同时间尺度上的定义： | 定义 | Flink/09-practices/09.01-case-studies/case-energy-grid-optimization.md |
| Def-F-07-263 | (需求响应优化 Demand Response Optimization): 需求响应是在价格或激励信号引导下调整负载： | 定义 | Flink/09-practices/09.01-case-studies/case-energy-grid-optimization.md |
| Def-F-07-264 | (电能质量指数 Power Quality Index): 综合电能质量评分： | 定义 | Flink/09-practices/09.01-case-studies/case-energy-grid-optimization.md |
| Def-F-07-265 | (DER优化调度 DER Dispatch Optimization): 分布式能源的实时调度： | 定义 | Flink/09-practices/09.01-case-studies/case-energy-grid-optimization.md |
| Def-F-07-30 | (智能制造系统): 智能制造系统是一个八元组 $\mathcal{M} = (P, D, S, F, C, A, \mathcal{T}, \mathcal{O})$，其中： | 定义 | Flink/09-practices/09.01-case-studies/case-smart-manufacturing-iot.md |
| Def-F-07-31 | (OEE - Overall Equipment Effectiveness): OEE是三个效率指标的乘积： | 定义 | Flink/09-practices/09.01-case-studies/case-smart-manufacturing-iot.md |
| Def-F-07-32 | (数字孪生): 数字孪生是物理实体在数字空间的实时映射： | 定义 | Flink/09-practices/09.01-case-studies/case-smart-manufacturing-iot.md |
| Def-F-07-33 | (预测性维护): 预测性维护系统是一个预测模型： | 定义 | Flink/09-practices/09.01-case-studies/case-smart-manufacturing-iot.md |
| Def-F-07-34 | (边缘-云协同模型): 边缘-云协同是一个处理函数分解： | 定义 | Flink/09-practices/09.01-case-studies/case-smart-manufacturing-iot.md |
| Def-F-07-35 | (边缘-云决策函数): 处理函数 $f$ 的执行位置决策： | 定义 | Flink/09-practices/09.01-case-studies/case-smart-manufacturing-iot.md |
| Def-F-07-40 | 包裹追踪事件 (Package Tracking Event) | 定义 | Flink/09-practices/09.01-case-studies/case-logistics-realtime-tracking.md |
| Def-F-07-41 | 运输网络图 (Transportation Network Graph) | 定义 | Flink/09-practices/09.01-case-studies/case-logistics-realtime-tracking.md |
| Def-F-07-42 | 预测性到达时间 ETA (Estimated Time of Arrival) | 定义 | Flink/09-practices/09.01-case-studies/case-logistics-realtime-tracking.md |
| Def-F-07-43 | 地理围栏 (Geofence) | 定义 | Flink/09-practices/09.01-case-studies/case-logistics-realtime-tracking.md |
| Def-F-07-44 | 追踪准确率 (Tracking Accuracy) | 定义 | Flink/09-practices/09.01-case-studies/case-logistics-realtime-tracking.md |
| Def-F-07-45 | 动态路由优化问题 (Dynamic Routing Optimization) | 定义 | Flink/09-practices/09.01-case-studies/case-logistics-realtime-tracking.md |
| Def-F-07-50 | (智能电网系统): 智能电网是一个十元组 $\mathcal{G} = (N, L, G, C, S, D, \mathcal{P}, \mathcal{F}, \mathcal{T}, \mathcal{O})$，其中： | 定义 | Flink/09-practices/09.01-case-studies/case-smart-grid-energy-management.md |
| Def-F-07-51 | (负荷预测): 负荷预测是一个时序回归问题，定义为： | 定义 | Flink/09-practices/09.01-case-studies/case-smart-grid-energy-management.md |
| Def-F-07-52 | (可再生能源出力预测): | 定义 | Flink/09-practices/09.01-case-studies/case-smart-grid-energy-management.md |
| Def-F-07-53 | (预测区间): 预测区间 $ | 定义 | Flink/09-practices/09.01-case-studies/case-smart-grid-energy-management.md |
| Def-F-07-54 | (需求响应): 需求响应是负荷侧弹性资源的调度机制： | 定义 | Flink/09-practices/09.01-case-studies/case-smart-grid-energy-management.md |
| Def-F-07-55 | (电网异常检测): 电网异常检测是一个复杂事件处理 (CEP) 问题： | 定义 | Flink/09-practices/09.01-case-studies/case-smart-grid-energy-management.md |
| Def-F-07-61 | (游戏事件流) | 定义 | Flink/09-practices/09.01-case-studies/case-gaming-realtime-analytics.md |
| Def-F-07-62 | (玩家会话) | 定义 | Flink/09-practices/09.01-case-studies/case-gaming-realtime-analytics.md |
| Def-F-07-63 | (游戏状态空间) | 定义 | Flink/09-practices/09.01-case-studies/case-gaming-realtime-analytics.md |
| Def-F-07-64 | (作弊行为) | 定义 | Flink/09-practices/09.01-case-studies/case-gaming-realtime-analytics.md |
| Def-F-07-65 | (反作弊检测系统) | 定义 | Flink/09-practices/09.01-case-studies/case-gaming-realtime-analytics.md |
| Def-F-07-66 | (实时作弊检测窗口) | 定义 | Flink/09-practices/09.01-case-studies/case-gaming-realtime-analytics.md |
| Def-F-07-67 | (准确率与召回率) | 定义 | Flink/09-practices/09.01-case-studies/case-gaming-realtime-analytics.md |
| Def-F-07-71 | (Clickstream 点击流): 点击流是用户在数字平台上的交互事件序列，定义为四元组 $\mathcal{C} = (\mathcal{E}, \mathcal{T}, \mathcal{A}, \preceq)$，其中： | 定义 | Flink/09-practices/09.01-case-studies/case-clickstream-user-behavior-analytics.md |
| Def-F-07-72 | (用户会话 User Session): 用户会话是会话窗口内的连续交互序列，定义为三元组 $\mathcal{S} = (u, \mathcal{E}_s, \tau)$： | 定义 | Flink/09-practices/09.01-case-studies/case-clickstream-user-behavior-analytics.md |
| Def-F-07-73 | (转化漏斗 Conversion Funnel): 转化漏斗是预定义的用户行为路径，定义为有序列表 $\mathcal{F} = | 定义 | Flink/09-practices/09.01-case-studies/case-clickstream-user-behavior-analytics.md |
| Def-F-07-74 | (实时用户画像 Real-time User Profile): 用户画像是在线更新的用户特征向量，定义为 $\mathcal{P}_u(t) = (\mathbf{d}_u, \mathbf{b}_u(t), \mathbf{r}_u(t))$： | 定义 | Flink/09-practices/09.01-case-studies/case-clickstream-user-behavior-analytics.md |
| Def-F-07-75 | (异常行为检测 Anomaly Detection): Bot/爬虫行为检测定义为分类函数 $\mathcal{D}: \mathcal{E}_s \rightarrow \{0, 1\}$，其中： | 定义 | Flink/09-practices/09.01-case-studies/case-clickstream-user-behavior-analytics.md |
| Def-F-08-01 | Flink 2.0 当前状态 (Flink 2.0 Current State) | 定义 | Flink/08-roadmap/08.01-flink-24/2026-q2-flink-tasks.md |
| Def-F-08-02 | Q2 目标状态 (Q2 Target State) | 定义 | Flink/08-roadmap/08.01-flink-24/2026-q2-flink-tasks.md |
| Def-F-08-03 | 任务优先级级别 (Task Priority Levels) | 定义 | Flink/08-roadmap/08.01-flink-24/2026-q2-flink-tasks.md |
| Def-F-08-04 | Flink 2.1 版本定义 | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.1-frontier-tracking.md |
| Def-F-08-05 | ML Inference Operator | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.1-frontier-tracking.md |
| Def-F-08-06 | Feature Store Connector | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.1-frontier-tracking.md |
| Def-F-08-07 | Auto-Scaling Strategy | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.1-frontier-tracking.md |
| Def-F-08-08 | Multi-Cluster Federation | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.1-frontier-tracking.md |
| Def-F-08-09 | Latency Spectrum (延迟谱) | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.1-frontier-tracking.md |
| Def-F-08-40 | Flink 2.3 Release Scope | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.3-2.4-roadmap.md |
| Def-F-08-41 | FLIP-531 Flink AI Agents | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.3-2.4-roadmap.md |
| Def-F-08-42 | Security SSL Enhancement | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.3-2.4-roadmap.md |
| Def-F-08-43 | Kafka 2PC Integration | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.3-2.4-roadmap.md |
| Def-F-08-44 | Flink 2.4 Preview | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.3-2.4-roadmap.md |
| Def-F-08-45 | 社区健康度指标 (Community Health Metrics) | 定义 | Flink/08-roadmap/08.01-flink-24/community-dynamics-tracking.md |
| Def-F-08-46 | 核心开发者 (Core Committer) | 定义 | Flink/08-roadmap/08.01-flink-24/community-dynamics-tracking.md |
| Def-F-08-47 | FLIP (Flink Improvement Proposal) | 定义 | Flink/08-roadmap/08.01-flink-24/community-dynamics-tracking.md |
| Def-F-08-48 | 竞品对标框架 (Competitive Benchmarking Framework) | 定义 | Flink/08-roadmap/08.01-flink-24/community-dynamics-tracking.md |
| Def-F-08-50 | Flink 2.5 Release Scope | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.5-preview.md |
| Def-F-08-51 | Unified Stream-Batch Execution (FLIP-435) | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.5-preview.md |
| Def-F-08-52 | Serverless Flink GA (FLIP-442) | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.5-preview.md |
| Def-F-08-53 | AI/ML Inference Optimization (FLIP-531 演进) | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.5-preview.md |
| Def-F-08-54 | Materialized Table GA (FLIP-516) | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.5-preview.md |
| Def-F-08-55 | WebAssembly UDF GA (FLIP-448) | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.5-preview.md |
| Def-F-08-56 | Stream-Batch Unification Architecture (流批一体架构) | 定义 | Flink/08-roadmap/08.01-flink-24/flink-25-stream-batch-unification.md |
| Def-F-08-57 | Unified Execution Engine (统一执行引擎) | 定义 | Flink/08-roadmap/08.01-flink-24/flink-25-stream-batch-unification.md |
| Def-F-08-58 | Adaptive Mode Selection (自适应模式选择) | 定义 | Flink/08-roadmap/08.01-flink-24/flink-25-stream-batch-unification.md |
| Def-F-08-59 | Unified Fault Tolerance (统一容错机制) | 定义 | Flink/08-roadmap/08.01-flink-24/flink-25-stream-batch-unification.md |
| Def-F-08-60 | Unified Storage Layer (统一存储层) | 定义 | Flink/08-roadmap/08.01-flink-24/flink-25-stream-batch-unification.md |
| Def-F-08-61 | Stream-Batch Hybrid Execution (流批混合执行) | 定义 | Flink/08-roadmap/08.01-flink-24/flink-25-stream-batch-unification.md |
| Def-F-08-62 | Next-Gen State Management (下一代状态管理) | 定义 | Flink/08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md |
| Def-F-08-63 | Cloud-Native Architecture 2.0 (云原生架构2.0) | 定义 | Flink/08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md |
| Def-F-08-64 | Unified API Layer (统一API层) | 定义 | Flink/08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md |
| Def-F-08-65 | Compatibility Strategy (兼容性策略) | 定义 | Flink/08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md |
| Def-F-08-66 | 版本生命周期状态 (Version Lifecycle State) | 定义 | Flink/08-roadmap/08.01-flink-24/flink-version-comparison-matrix.md |
| Def-F-08-67 | 特性成熟度等级 (Feature Maturity Level) | 定义 | Flink/08-roadmap/08.01-flink-24/flink-version-comparison-matrix.md |
| Def-F-08-68 | 兼容性等级 (Compatibility Level) | 定义 | Flink/08-roadmap/08.01-flink-24/flink-version-comparison-matrix.md |
| Def-F-08-69 | 升级复杂度 (Upgrade Complexity) | 定义 | Flink/08-roadmap/08.01-flink-24/flink-version-comparison-matrix.md |
| Def-F-08-70 | Flink 2.4 Release Scope | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Def-F-08-71 | AI Agent Preview (FLIP-531) | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Def-F-08-72 | Serverless Flink Architecture | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Def-F-08-73 | Adaptive Execution Engine v2 | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Def-F-08-74 | Intelligent Checkpointing Strategy | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Def-F-08-75 | ANSI SQL 2023 Compatibility | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Def-F-08-76 | New Connectors in 2.4 | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Def-F-08-77 | Agent Runtime Core | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Def-F-08-78 | Multi-Agent Coordination Protocol | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Def-F-08-79 | MCP Integration Framework | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Def-F-08-80 | Disaggregated State Architecture | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Def-F-08-81 | Tiered State Storage | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Def-F-08-82 | Dynamic Property Graph | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Def-F-08-83 | Continuous Graph Query | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Def-F-08-84 | Temporal Graph Operator | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Def-F-08-85 | Unified Source Interface | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Def-F-08-86 | Hybrid Scan Strategy | 定义 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Def-F-09-01 | (JDK 兼容性矩阵) | 定义 | Flink/09-practices/09.03-performance-tuning/jdk-11-migration-guide.md |
| Def-F-09-02 | (迁移风险等级) | 定义 | Flink/09-practices/09.03-performance-tuning/jdk-11-migration-guide.md |
| Def-F-09-03 | (回滚窗口期) | 定义 | Flink/09-practices/09.03-performance-tuning/jdk-11-migration-guide.md |
| Def-F-09-04 | (性能回归系数) | 定义 | Flink/09-practices/09.03-performance-tuning/jdk-11-migration-guide.md |
| Def-F-09-05 | Resource Profile Template | 定义 | Flink/09-practices/09.04-deployment/flink-kubernetes-operator-1.14-guide.md |
| Def-F-09-06 | FlinkDeploymentSet CRD | 定义 | Flink/09-practices/09.04-deployment/flink-kubernetes-operator-1.14-guide.md |
| Def-F-09-07 | 向后兼容性 (Backward Compatibility) | 定义 | Flink/09-practices/09.04-deployment/flink-k8s-operator-migration-1.13-to-1.14.md |
| Def-F-09-08 | 配置迁移 (Configuration Migration) | 定义 | Flink/09-practices/09.04-deployment/flink-k8s-operator-migration-1.13-to-1.14.md |
| Def-F-09-09 | CRD 版本升级 | 定义 | Flink/09-practices/09.04-deployment/flink-k8s-operator-migration-1.13-to-1.14.md |
| Def-F-09-10 | 滚动升级策略 | 定义 | Flink/09-practices/09.04-deployment/flink-k8s-operator-migration-1.13-to-1.14.md |
| Def-F-09-11 | 迁移验证点 (Migration Verification Point) | 定义 | Flink/09-practices/09.04-deployment/flink-k8s-operator-migration-1.13-to-1.14.md |
| Def-F-09-12 | Declarative Resource Management | 定义 | Flink/09-practices/09.04-deployment/flink-k8s-operator-new-features-1.14.md |
| Def-F-09-13 | Autoscaling Algorithm V2 | 定义 | Flink/09-practices/09.04-deployment/flink-k8s-operator-new-features-1.14.md |
| Def-F-09-14 | Session Cluster Enhancements | 定义 | Flink/09-practices/09.04-deployment/flink-k8s-operator-new-features-1.14.md |
| Def-F-09-15 | Helm Chart Schema Validation | 定义 | Flink/09-practices/09.04-deployment/flink-k8s-operator-new-features-1.14.md |
| Def-F-09-16 | Blue/Green Deployment CRD | 定义 | Flink/09-practices/09.04-deployment/flink-k8s-operator-new-features-1.14.md |
| Def-F-09-17 | PyFlink 架构 (Python→Java Bridge) | 定义 | Flink/03-api/09-language-foundations/02-python-api.md |
| Def-F-09-18 | UDF 序列化 (PyFlink UDF) | 定义 | Flink/03-api/09-language-foundations/02-python-api.md |
| Def-F-09-19 | Python 环境管理 (Conda/Pip) | 定义 | Flink/03-api/09-language-foundations/02-python-api.md |
| Def-F-09-20 | 性能基准测试框架 (Performance Benchmark Framework) | 定义 | Flink/09-practices/09.02-benchmarking/flink-24-25-benchmark-results.md |
| Def-F-09-21 | 标准化性能指标 (Standardized Performance Metrics) | 定义 | Flink/09-practices/09.02-benchmarking/flink-24-25-benchmark-results.md |
| Def-F-09-22 | 版本对比基线 (Version Comparison Baseline) | 定义 | Flink/09-practices/09.02-benchmarking/flink-24-25-benchmark-results.md |
| Def-F-09-23 | 统计显著性指标 (Statistical Significance Metrics) | 定义 | Flink/09-practices/09.02-benchmarking/flink-24-25-benchmark-results.md |
| Def-F-09-24 | PyFlink UDF 分类 | 定义 | Flink/03-api/09-language-foundations/pyflink-complete-guide.md |
| Def-F-09-25 | PyFlink-Pandas 集成模型 | 定义 | Flink/03-api/09-language-foundations/pyflink-complete-guide.md |
| Def-F-09-26 | PyFlink ML 集成架构 | 定义 | Flink/03-api/09-language-foundations/pyflink-complete-guide.md |
| Def-F-09-27 | PyFlink 部署拓扑 | 定义 | Flink/03-api/09-language-foundations/pyflink-complete-guide.md |
| Def-F-09-28 | PyFlink 性能优化策略 | 定义 | Flink/03-api/09-language-foundations/pyflink-complete-guide.md |
| Def-F-09-30 | Nexmark基准测试框架 | 定义 | Flink/09-practices/09.02-benchmarking/nexmark-2026-benchmark.md |
| Def-F-09-31 | Q0-Q23查询分类体系 | 定义 | Flink/09-practices/09.02-benchmarking/nexmark-2026-benchmark.md |
| Def-F-09-32 | 跨引擎性能指标标准化 | 定义 | Flink/09-practices/09.02-benchmarking/nexmark-2026-benchmark.md |
| Def-F-09-33 | RecordAttributes V2 | 定义 | Flink/03-api/09-language-foundations/05-datastream-v2-api.md |
| Def-F-09-34 | Scala 3 Type System (DOT Calculus Extension) | 定义 | Flink/03-api/09-language-foundations/01.03-scala3-type-system-formalization.md |
| Def-F-09-35 | Path-Dependent Types in Streaming Context | 定义 | Flink/03-api/09-language-foundations/01.03-scala3-type-system-formalization.md |
| Def-F-09-36 | Typeclass Derivation (Using Clauses) | 定义 | Flink/03-api/09-language-foundations/01.03-scala3-type-system-formalization.md |
| Def-F-09-37 | Opaque Types for Domain Modeling | 定义 | Flink/03-api/09-language-foundations/01.03-scala3-type-system-formalization.md |
| Def-F-09-38 | Inline Functions for Zero-cost Abstractions | 定义 | Flink/03-api/09-language-foundations/01.03-scala3-type-system-formalization.md |
| Def-F-09-39 | RisingWave 系统架构 | 定义 | Flink/03-api/09-language-foundations/06-risingwave-deep-dive.md |
| Def-F-09-40 | TCO总拥有成本模型 (Total Cost of Ownership) | 定义 | Flink/09-practices/09.02-benchmarking/tco-analysis-2026.md |
| Def-F-09-41 | 云资源定价模型 | 定义 | Flink/09-practices/09.02-benchmarking/tco-analysis-2026.md |
| Def-F-09-42 | 单位处理成本效率 (Cost Efficiency) | 定义 | Flink/09-practices/09.02-benchmarking/tco-analysis-2026.md |
| Def-F-09-43 | Component Model | 定义 |  |
| Def-F-09-44 | WASM Sandbox Security | 定义 |  |
| Def-F-09-45 | 计算-存储分离架构 | 定义 | Flink/03-api/09-language-foundations/06-risingwave-deep-dive.md |
| Def-F-09-46 | Native CDC 实现 | 定义 | Flink/03-api/09-language-foundations/06-risingwave-deep-dive.md |
| Def-F-09-47 | 向量数据类型与相似度算子 | 定义 | Flink/03-api/09-language-foundations/06-risingwave-deep-dive.md |
| Def-F-09-48 | 向量索引算法 | 定义 | Flink/03-api/09-language-foundations/06-risingwave-deep-dive.md |
| Def-F-09-49 | 实时 RAG 架构 | 定义 | Flink/03-api/09-language-foundations/06-risingwave-deep-dive.md |
| Def-F-09-50 | 统一数据库架构 | 定义 | Flink/03-api/09-language-foundations/06-risingwave-deep-dive.md |
| Def-F-09-51 | Timestamp Capability 语义 | 定义 | Flink/03-api/09-language-foundations/07.01-timely-dataflow-optimization.md |
| Def-F-09-52 | 系统级进度跟踪 | 定义 | Flink/03-api/09-language-foundations/07.01-timely-dataflow-optimization.md |
| Def-F-09-53 | 惰性算子调度策略 | 定义 | Flink/03-api/09-language-foundations/07.01-timely-dataflow-optimization.md |
| Def-F-09-54 | REGION 算子 | 定义 | Flink/03-api/09-language-foundations/07.01-timely-dataflow-optimization.md |
| Def-F-09-55 | Differential Dataflow 更新模型 | 定义 | Flink/03-api/09-language-foundations/07.01-timely-dataflow-optimization.md |
| Def-F-09-56 | ARRANGE 算子双重功能 | 定义 | Flink/03-api/09-language-foundations/07.01-timely-dataflow-optimization.md |
| Def-F-09-57 | ARRANGE算子双重功能 | 定义 |  |
| Def-F-09-60 | AsyncExecutionMode | 定义 | Flink/03-api/09-language-foundations/02.03-python-async-api.md |
| Def-F-09-61 | ConcurrencyLimiter | 定义 | Flink/03-api/09-language-foundations/02.03-python-async-api.md |
| Def-F-09-62 | AsyncRetryStrategy | 定义 | Flink/03-api/09-language-foundations/02.03-python-async-api.md |
| Def-F-09-63 | AsyncRichFunction | 定义 | Flink/03-api/09-language-foundations/02.03-python-async-api.md |
| Def-F-09-64 | ResultFuture | 定义 | Flink/03-api/09-language-foundations/02.03-python-async-api.md |
| Def-F-09-65 | DataStream 类型层次 | 定义 | Flink/03-api/09-language-foundations/flink-datastream-api-complete-guide.md |
| Def-F-09-66 | 转换算子 (Transformations) | 定义 | Flink/03-api/09-language-foundations/flink-datastream-api-complete-guide.md |
| Def-F-09-67 | 键控流 (KeyedStream) | 定义 | Flink/03-api/09-language-foundations/flink-datastream-api-complete-guide.md |
| Def-F-09-68 | 状态原语 (State Primitives) | 定义 | Flink/03-api/09-language-foundations/flink-datastream-api-complete-guide.md |
| Def-F-09-69 | 时间语义 (Time Semantics) | 定义 | Flink/03-api/09-language-foundations/flink-datastream-api-complete-guide.md |
| Def-F-09-70 | Watermark 机制 | 定义 | Flink/03-api/09-language-foundations/flink-datastream-api-complete-guide.md |
| Def-F-09-71 | 异步 I/O | 定义 | Flink/03-api/09-language-foundations/flink-datastream-api-complete-guide.md |
| Def-F-09-72 | ProcessFunction 家族 | 定义 | Flink/03-api/09-language-foundations/flink-datastream-api-complete-guide.md |
| Def-F-09-73 | CEP 复杂事件处理 | 定义 | Flink/03-api/09-language-foundations/flink-datastream-api-complete-guide.md |
| Def-F-09-74 | 广播状态模式 | 定义 | Flink/03-api/09-language-foundations/flink-datastream-api-complete-guide.md |
| Def-F-09-75 | 可查询状态 | 定义 | Flink/03-api/09-language-foundations/flink-datastream-api-complete-guide.md |
| Def-F-10-01 | 流计算总拥有成本 (TCO) | 定义 | Flink/04-runtime/04.01-deployment/cost-optimization-calculator.md |
| Def-F-10-02 | 计算资源单位成本 | 定义 | Flink/04-runtime/04.01-deployment/cost-optimization-calculator.md |
| Def-F-10-03 | 状态存储成本模型 | 定义 | Flink/04-runtime/04.01-deployment/cost-optimization-calculator.md |
| Def-F-10-04 | 成本效率指标 | 定义 | Flink/04-runtime/04.01-deployment/cost-optimization-calculator.md |
| Def-F-10-05 | 容量规划基线 | 定义 | Flink/04-runtime/04.01-deployment/cost-optimization-calculator.md |
| Def-F-10-10 | K8s部署模式形式化 | 定义 | Flink/04-runtime/04.01-deployment/kubernetes-deployment-production-guide.md |
| Def-F-10-11 | Native K8s集成 | 定义 | Flink/04-runtime/04.01-deployment/kubernetes-deployment-production-guide.md |
| Def-F-10-12 | Flink K8s Operator架构 | 定义 | Flink/04-runtime/04.01-deployment/kubernetes-deployment-production-guide.md |
| Def-F-10-13 | 多租户隔离模型 | 定义 | Flink/04-runtime/04.01-deployment/kubernetes-deployment-production-guide.md |
| Def-F-10-20 | Flink Kubernetes Operator | 定义 | Flink/04-runtime/04.01-deployment/flink-kubernetes-operator-deep-dive.md |
| Def-F-10-21 | CRD (Custom Resource Definition) | 定义 | Flink/04-runtime/04.01-deployment/flink-kubernetes-operator-deep-dive.md |
| Def-F-10-22 | 控制循环 (Control Loop) | 定义 | Flink/04-runtime/04.01-deployment/flink-kubernetes-operator-deep-dive.md |
| Def-F-10-23 | 有状态升级 (Stateful Upgrade) | 定义 | Flink/04-runtime/04.01-deployment/flink-kubernetes-operator-deep-dive.md |
| Def-F-10-24 | Application Mode on K8s | 定义 | Flink/04-runtime/04.01-deployment/flink-kubernetes-operator-deep-dive.md |
| Def-F-10-25 | Session Mode on K8s | 定义 | Flink/04-runtime/04.01-deployment/flink-kubernetes-operator-deep-dive.md |
| Def-F-10-30 | Autoscaler 架构定义 | 定义 | Flink/04-runtime/04.01-deployment/flink-kubernetes-autoscaler-deep-dive.md |
| Def-F-10-31 | 背压 (Backpressure) 形式化定义 | 定义 | Flink/04-runtime/04.01-deployment/flink-kubernetes-autoscaler-deep-dive.md |
| Def-F-10-32 | 目标利用率 (Target Utilization) 定义 | 定义 | Flink/04-runtime/04.01-deployment/flink-kubernetes-autoscaler-deep-dive.md |
| Def-F-10-33 | 顶点级别扩缩容 (Vertex-Level Scaling) 定义 | 定义 | Flink/04-runtime/04.01-deployment/flink-kubernetes-autoscaler-deep-dive.md |
| Def-F-10-34 | 追赶容量 (Catch-up Capacity) 定义 | 定义 | Flink/04-runtime/04.01-deployment/flink-kubernetes-autoscaler-deep-dive.md |
| Def-F-10-35 | 稳定窗口 (Stabilization Window) 定义 | 定义 | Flink/04-runtime/04.01-deployment/flink-kubernetes-autoscaler-deep-dive.md |
| Def-F-10-40 | Flink 部署模式分类 | 定义 | Flink/04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md |
| Def-F-10-41 | Slot 与资源分配单元 | 定义 | Flink/04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md |
| Def-F-10-42 | 细粒度资源管理 (Fine-Grained Resource Management) | 定义 | Flink/04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md |
| Def-F-10-43 | 自适应调度器 (Adaptive Scheduler) | 定义 | Flink/04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md |
| Def-F-10-44 | JobManager 高可用性模式 | 定义 | Flink/04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md |
| Def-F-10-45 | 有状态作业升级策略 | 定义 | Flink/04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md |
| Def-F-10-50 | Kubernetes Operator 1.12增强模式 | 定义 | Flink/04-runtime/04.01-deployment/flink-24-deployment-improvements.md |
| Def-F-10-51 | Helm Chart v2语义化部署 | 定义 | Flink/04-runtime/04.01-deployment/flink-24-deployment-improvements.md |
| Def-F-10-52 | 配置热更新 (Hot Configuration Reload) | 定义 | Flink/04-runtime/04.01-deployment/flink-24-deployment-improvements.md |
| Def-F-10-53 | 滚动升级优化 (Optimized Rolling Upgrade) | 定义 | Flink/04-runtime/04.01-deployment/flink-24-deployment-improvements.md |
| Def-F-10-54 | 蓝绿部署 (Blue-Green Deployment) | 定义 | Flink/04-runtime/04.01-deployment/flink-24-deployment-improvements.md |
| Def-F-10-55 | 金丝雀发布 (Canary Release) | 定义 | Flink/04-runtime/04.01-deployment/flink-24-deployment-improvements.md |
| Def-F-10-56 | 多租户隔离 (Multi-Tenant Isolation) | 定义 | Flink/04-runtime/04.01-deployment/flink-24-deployment-improvements.md |
| Def-F-10-57 | 资源配额管理 (Resource Quota Management) | 定义 | Flink/04-runtime/04.01-deployment/flink-24-deployment-improvements.md |
| Def-F-10-58 | 部署安全检查 (Deployment Security Gate) | 定义 | Flink/04-runtime/04.01-deployment/flink-24-deployment-improvements.md |
| Def-F-10-59 | 声明式配置状态 (Desired Configuration State) | 定义 | Flink/04-runtime/04.01-deployment/flink-24-deployment-improvements.md |
| Def-F-11-01 | 基准测试 (Benchmarking) | 定义 | Flink/09-practices/09.02-benchmarking/performance-benchmarking-guide.md |
| Def-F-11-02 | 吞吐量 (Throughput) | 定义 | Flink/09-practices/09.02-benchmarking/performance-benchmarking-guide.md |
| Def-F-11-03 | 端到端延迟 (End-to-End Latency) | 定义 | Flink/09-practices/09.02-benchmarking/performance-benchmarking-guide.md |
| Def-F-11-04 | Nexmark基准测试套件 | 定义 | Flink/09-practices/09.02-benchmarking/performance-benchmark-suite.md |
| Def-F-11-05 | 端到端延迟 (End-to-End Latency) | 定义 | Flink/09-practices/09.02-benchmarking/performance-benchmark-suite.md |
| Def-F-11-06 | 吞吐量-延迟曲线 (Throughput-Latency Curve) | 定义 | Flink/09-practices/09.02-benchmarking/performance-benchmark-suite.md |
| Def-F-11-07 | 状态规模指标 (State Scale Metrics) | 定义 | Flink/09-practices/09.02-benchmarking/performance-benchmark-suite.md |
| Def-F-11-08 | Checkpoint性能指标 | 定义 | Flink/09-practices/09.02-benchmarking/performance-benchmark-suite.md |
| Def-F-12-01 | Flink ML架构 | 定义 | Flink/06-ai-ml/flink-ml-architecture.md |
| Def-F-12-02 | 迭代计算 (Iterations) | 定义 | Flink/06-ai-ml/flink-ml-architecture.md |
| Def-F-12-03 | 参数服务器集成 | 定义 | Flink/06-ai-ml/flink-ml-architecture.md |
| Def-F-12-04 | (在线学习 Online Learning) | 定义 | Flink/06-ai-ml/online-learning-algorithms.md |
| Def-F-12-05 | (随机梯度下降 SGD) | 定义 | Flink/06-ai-ml/online-learning-algorithms.md |
| Def-F-12-06 | (概念漂移 Concept Drift) | 定义 | Flink/06-ai-ml/online-learning-algorithms.md |
| Def-F-12-07 | 模型服务 (Model Serving) | 定义 | Flink/06-ai-ml/model-serving-streaming.md |
| Def-F-12-08 | 实时推理管道 (Real-time Inference Pipeline) | 定义 | Flink/06-ai-ml/model-serving-streaming.md |
| Def-F-12-09 | 模型版本管理 (Model Version Management) | 定义 | Flink/06-ai-ml/model-serving-streaming.md |
| Def-F-12-10 | 在线学习范式 (Online Learning Paradigm) | 定义 | Flink/06-ai-ml/online-learning-production.md |
| Def-F-12-100 | Flink AI/ML 统一架构 | 定义 | Flink/06-ai-ml/flink-ai-ml-integration-complete-guide.md |
| Def-F-12-101 | FLIP-531 Agent运行时架构 | 定义 | Flink/06-ai-ml/flink-ai-ml-integration-complete-guide.md |
| Def-F-12-102 | MCP协议原生集成 | 定义 | Flink/06-ai-ml/flink-ai-ml-integration-complete-guide.md |
| Def-F-12-103 | A2A (Agent-to-Agent) 通信协议 | 定义 | Flink/06-ai-ml/flink-ai-ml-integration-complete-guide.md |
| Def-F-12-104 | 向量搜索语义 (VECTOR_SEARCH) | 定义 | Flink/06-ai-ml/flink-ai-ml-integration-complete-guide.md |
| Def-F-12-105 | ML_PREDICT与Model DDL | 定义 | Flink/06-ai-ml/flink-ai-ml-integration-complete-guide.md |
| Def-F-12-106 | LLM集成抽象层 | 定义 | Flink/06-ai-ml/flink-ai-ml-integration-complete-guide.md |
| Def-F-12-107 | Flink ML Pipeline API | 定义 | Flink/06-ai-ml/flink-ai-ml-integration-complete-guide.md |
| Def-F-12-108 | Agent可重放性保证 | 定义 | Flink/06-ai-ml/flink-ai-ml-integration-complete-guide.md |
| Def-F-12-109 | 向量索引类型 | 定义 | Flink/06-ai-ml/flink-ai-ml-integration-complete-guide.md |
| Def-F-12-11 | 增量学习 vs 批量学习 (Incremental vs Batch Learning) | 定义 | Flink/06-ai-ml/online-learning-production.md |
| Def-F-12-110 | SQL Agent语法扩展 | 定义 | Flink/06-ai-ml/flink-ai-ml-integration-complete-guide.md |
| Def-F-12-12 | 模型持续训练架构 (Continuous Training Architecture) | 定义 | Flink/06-ai-ml/online-learning-production.md |
| Def-F-12-13 | 实时特征-标签关联 (Real-time Feature-Label Join) | 定义 | Flink/06-ai-ml/online-learning-production.md |
| Def-F-12-14 | 模型版本管理与 A/B 测试 (Model Versioning & A/B Testing) | 定义 | Flink/06-ai-ml/online-learning-production.md |
| Def-F-12-15 | 影子模式与渐进发布 (Shadow Mode & Progressive Rollout) | 定义 | Flink/06-ai-ml/online-learning-production.md |
| Def-F-12-16 | PROJECT-COMPLETION-FINAL-REPORT.md | 定义 |  |
| Def-F-12-17 | Flink/12-ai-ml/online-learning-production.md | 定义 |  |
| Def-F-12-18 | Flink/12-ai-ml/online-learning-production.md | 定义 |  |
| Def-F-12-19 | Flink/12-ai-ml/online-learning-production.md | 定义 |  |
| Def-F-12-20 | Streaming RAG Architecture | 定义 | Flink/06-ai-ml/rag-streaming-architecture.md |
| Def-F-12-21 | Streaming Vector Retrieval Mechanism | 定义 | Flink/06-ai-ml/rag-streaming-architecture.md |
| Def-F-12-22 | Real-time Feature Engineering Pipeline | 定义 | Flink/06-ai-ml/rag-streaming-architecture.md |
| Def-F-12-23 | LLM Inference Optimization Patterns | 定义 | Flink/06-ai-ml/rag-streaming-architecture.md |
| Def-F-12-30 | Flink Agent | 定义 | Flink/06-ai-ml/flink-agents-flip-531.md |
| Def-F-12-31 | Agentic Workflow (智能体工作流) | 定义 | Flink/06-ai-ml/flink-agents-flip-531.md |
| Def-F-12-32 | MCP (Model Context Protocol) 集成 | 定义 | Flink/06-ai-ml/flink-agents-flip-531.md |
| Def-F-12-33 | A2A (Agent-to-Agent) 协议 | 定义 | Flink/06-ai-ml/flink-agents-flip-531.md |
| Def-F-12-34 | Agent 记忆管理 | 定义 | Flink/06-ai-ml/flink-agents-flip-531.md |
| Def-F-12-35 | Replayability (可重放性) | 定义 | Flink/06-ai-ml/flink-agents-flip-531.md |
| Def-F-12-40 | 流式 LLM 推理架构 (Streaming LLM Inference Architecture) | 定义 | Flink/06-ai-ml/flink-llm-integration.md |
| Def-F-12-41 | Model DDL (模型定义语言) | 定义 | Flink/06-ai-ml/flink-llm-integration.md |
| Def-F-12-42 | ML_PREDICT 函数 | 定义 | Flink/06-ai-ml/flink-llm-integration.md |
| Def-F-12-43 | RAG 流式架构 (Retrieval-Augmented Generation Streaming) | 定义 | Flink/06-ai-ml/flink-llm-integration.md |
| Def-F-12-44 | OpenAI API 兼容层 | 定义 | Flink/06-ai-ml/flink-llm-integration.md |
| Def-F-12-45 | 令牌预算管理 (Token Budget Management) | 定义 | Flink/06-ai-ml/flink-llm-integration.md |
| Def-F-12-46 | Model Context Protocol (MCP) | 定义 | Flink/06-ai-ml/flink-mcp-protocol-integration.md |
| Def-F-12-47 | MCP 服务器 (MCP Server) | 定义 | Flink/06-ai-ml/flink-mcp-protocol-integration.md |
| Def-F-12-48 | MCP 工具 (MCP Tool) | 定义 | Flink/06-ai-ml/flink-mcp-protocol-integration.md |
| Def-F-12-49 | MCP 资源 (MCP Resource) | 定义 | Flink/06-ai-ml/flink-mcp-protocol-integration.md |
| Def-F-12-50 | GPU加速流处理 (GPU-Accelerated Stream Processing) | 定义 | Flink/06-ai-ml/flink-25-gpu-acceleration.md |
| Def-F-12-51 | Flink-CUDA运行时架构 (Flink-CUDA Runtime Architecture) | 定义 | Flink/06-ai-ml/flink-25-gpu-acceleration.md |
| Def-F-12-52 | GPU算子库 (GPU Operator Library) | 定义 | Flink/06-ai-ml/flink-25-gpu-acceleration.md |
| Def-F-12-53 | 异构计算调度 (Heterogeneous Computing Scheduler) | 定义 | Flink/06-ai-ml/flink-25-gpu-acceleration.md |
| Def-F-12-54 | GPU内存管理模型 (GPU Memory Management Model) | 定义 | Flink/06-ai-ml/flink-25-gpu-acceleration.md |
| Def-F-12-55 | CUDA流与并发 (CUDA Streams and Concurrency) | 定义 | Flink/06-ai-ml/flink-25-gpu-acceleration.md |
| Def-F-12-90 | Flink AI Agent | 定义 | Flink/06-ai-ml/flink-ai-agents-flip-531.md |
| Def-F-12-91 | Agent State as Memory | 定义 | Flink/06-ai-ml/flink-ai-agents-flip-531.md |
| Def-F-12-92 | Agent Tool Definition | 定义 | Flink/06-ai-ml/flink-ai-agents-flip-531.md |
| Def-F-12-93 | A2A Communication | 定义 | Flink/06-ai-ml/flink-ai-agents-flip-531.md |
| Def-F-12-94 | Agent Replayability | 定义 | Flink/06-ai-ml/flink-ai-agents-flip-531.md |
| Def-F-13-01 | 安全加固 (Security Hardening) | 定义 | Flink/09-practices/09.04-security/security-hardening-guide.md |
| Def-F-13-02 | 零信任架构 (Zero Trust Architecture) | 定义 | Flink/09-practices/09.04-security/security-hardening-guide.md |
| Def-F-13-03 | 纵深防御 (Defense in Depth) | 定义 | Flink/09-practices/09.04-security/security-hardening-guide.md |
| Def-F-13-04 | 最小权限原则 (Principle of Least Privilege) | 定义 | Flink/09-practices/09.04-security/security-hardening-guide.md |
| Def-F-13-05 | 飞地 (Enclave) | 定义 | Flink/09-practices/09.04-security/trusted-execution-flink.md |
| Def-F-13-06 | 远程证明 (Remote Attestation) | 定义 | Flink/09-practices/09.04-security/trusted-execution-flink.md |
| Def-F-13-07 | 安全通道建立 (Secure Channel Establishment) | 定义 | Flink/09-practices/09.04-security/trusted-execution-flink.md |
| Def-F-13-08 | GPU TEE (GPU Trusted Execution Environment) | 定义 | Flink/09-practices/09.04-security/gpu-confidential-computing.md |
| Def-F-13-09 | NVIDIA H100 Confidential Computing (CC Mode) | 定义 | Flink/09-practices/09.04-security/gpu-confidential-computing.md |
| Def-F-13-10 | AMD MI300 Infinity Guard | 定义 | Flink/09-practices/09.04-security/gpu-confidential-computing.md |
| Def-F-13-11 | Intel TDX Connect for GPUs | 定义 | Flink/09-practices/09.04-security/gpu-confidential-computing.md |
| Def-F-13-12 | 硬件发展时间线 (2022-2025) | 定义 | Flink/09-practices/09.04-security/gpu-confidential-computing.md |
| Def-F-13-13 | 安全流处理会话 (Secure Stream Processing Session) | 定义 | Flink/09-practices/09.04-security/gpu-confidential-computing.md |
| Def-F-13-14 | Flink 安全模型 (Flink Security Model) | 定义 | Flink/09-practices/09.04-security/flink-security-complete-guide.md |
| Def-F-13-15 | 认证机制 (Authentication Mechanisms) | 定义 | Flink/09-practices/09.04-security/flink-security-complete-guide.md |
| Def-F-13-16 | 授权模型 (Authorization Models) | 定义 | Flink/09-practices/09.04-security/flink-security-complete-guide.md |
| Def-F-13-17 | 数据安全控制 (Data Security Controls) | 定义 | Flink/09-practices/09.04-security/flink-security-complete-guide.md |
| Def-F-13-18 | 可信执行环境 (TEE) | 定义 | Flink/09-practices/09.04-security/flink-security-complete-guide.md |
| Def-F-13-19 | 密钥管理生命周期 (Key Management Lifecycle) | 定义 | Flink/09-practices/09.04-security/flink-security-complete-guide.md |
| Def-F-13-30 | SPIFFE 身份框架 (SPIFFE Identity Framework) | 定义 | Flink/09-practices/09.04-security/spiffe-spire-integration-guide.md |
| Def-F-13-31 | SPIRE 身份控制平面 (SPIRE Control Plane) | 定义 | Flink/09-practices/09.04-security/spiffe-spire-integration-guide.md |
| Def-F-13-32 | SVID (SPIFFE Verifiable Identity Document) | 定义 | Flink/09-practices/09.04-security/spiffe-spire-integration-guide.md |
| Def-F-13-33 | 工作负载证明 (Workload Attestation) | 定义 | Flink/09-practices/09.04-security/spiffe-spire-integration-guide.md |
| Def-F-13-50 | Flink 2.4 安全模型 (Flink 2.4 Security Model) | 定义 | Flink/09-practices/09.04-security/flink-24-security-enhancements.md |
| Def-F-13-51 | TLS 1.3 全栈支持 (TLS 1.3 Full-Stack Support) | 定义 | Flink/09-practices/09.04-security/flink-24-security-enhancements.md |
| Def-F-13-52 | 现代密码套件 (Modern Cipher Suites) | 定义 | Flink/09-practices/09.04-security/flink-24-security-enhancements.md |
| Def-F-13-53 | OAuth 2.1 增强认证 (OAuth 2.1 Enhanced Authentication) | 定义 | Flink/09-practices/09.04-security/flink-24-security-enhancements.md |
| Def-F-13-54 | OIDC 集成改进 (OIDC Integration Improvements) | 定义 | Flink/09-practices/09.04-security/flink-24-security-enhancements.md |
| Def-F-13-55 | 结构化审计日志 (Structured Audit Logging) | 定义 | Flink/09-practices/09.04-security/flink-24-security-enhancements.md |
| Def-F-13-56 | 数据脱敏引擎 (Data Masking Engine) | 定义 | Flink/09-practices/09.04-security/flink-24-security-enhancements.md |
| Def-F-13-57 | 字段级加密 (Field-Level Encryption) | 定义 | Flink/09-practices/09.04-security/flink-24-security-enhancements.md |
| Def-F-13-58 | 声明式安全策略 (Declarative Security Policies) | 定义 | Flink/09-practices/09.04-security/flink-24-security-enhancements.md |
| Def-F-14-01 | WASM-Native Stream Processing (WASM 原生流处理) | 定义 | Flink/07-rust-native/flink-rust-ecosystem-trends-2026.md |
| Def-F-14-02 | Vectorized Execution (向量化执行) | 定义 | Flink/07-rust-native/flink-rust-ecosystem-trends-2026.md |
| Def-F-14-03 | Polyglot UDF Engine (多语言 UDF 引擎) | 定义 | Flink/07-rust-native/flink-rust-ecosystem-trends-2026.md |
| Def-F-14-04 | Time Travel 在流处理中的应用 | 定义 | Flink/05-ecosystem/05.02-lakehouse/flink-iceberg-integration.md |
| Def-F-14-05 | Hidden Partitioning（隐藏分区） | 定义 | Flink/05-ecosystem/05.02-lakehouse/flink-iceberg-integration.md |
| Def-F-14-06 | Snapshot Isolation（快照隔离） | 定义 | Flink/05-ecosystem/05.02-lakehouse/flink-iceberg-integration.md |
| Def-F-14-07 | Apache Paimon LSM-Tree 流批模型 | 定义 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-architecture.md |
| Def-F-14-08 | Delta Lake 流式架构 | 定义 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-architecture.md |
| Def-F-14-09 | 统一批流处理语义 | 定义 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-architecture.md |
| Def-F-14-21 | Streaming-First Lakehouse Architecture (流优先湖仓架构) | 定义 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-deep-dive-2026.md |
| Def-F-14-22 | Open Table Format 2026 Maturity Model (开放表格式成熟度模型) | 定义 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-deep-dive-2026.md |
| Def-F-14-23 | Table Format 存储语义形式化 | 定义 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-deep-dive-2026.md |
| Def-F-14-24 | Catalog 标准化与治理抽象 (Apache Polaris / Unity Catalog / Gravitino) | 定义 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-deep-dive-2026.md |
| Def-F-14-25 | S3 Tables与Storage-First架构 | 定义 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-deep-dive-2026.md |
| Def-F-14-31 | (图流数据模型). 设图流为随时间演化的图序列 $𝒢 = \{G_t\}_{t=0}^{∞}$，其中每个时间点的图状态为： | 定义 | Flink/05-ecosystem/05.04-graph/flink-gelly-streaming-graph-processing.md |
| Def-F-14-32 | (边添加流模型 - Edge Addition Stream). Gelly Streaming 采用边添加流模型，定义图更新操作： | 定义 | Flink/05-ecosystem/05.04-graph/flink-gelly-streaming-graph-processing.md |
| Def-F-14-33 | (GraphStream 抽象). Gelly Streaming 的核心抽象 `GraphStream<K, VV, EV>` 定义为： | 定义 | Flink/05-ecosystem/05.04-graph/flink-gelly-streaming-graph-processing.md |
| Def-F-14-34 | (图窗口切片 - Graph Window Slice). 设时间窗口 $W = | 定义 | Flink/05-ecosystem/05.04-graph/flink-gelly-streaming-graph-processing.md |
| Def-F-14-35 | (分布式图摘要 - Distributed Graph Summarization). 设图 $G=(V,E)$，图摘要为映射函数 $φ: V → V'$ 诱导的压缩图 $G'=(V',E')$，其中： | 定义 | Flink/05-ecosystem/05.04-graph/flink-gelly-streaming-graph-processing.md |
| Def-F-15-01 | 系统指标 (System Metrics) | 定义 | Flink/04-runtime/04.03-observability/metrics-and-monitoring.md |
| Def-F-15-02 | Flink运行时指标 (Runtime Metrics) | 定义 | Flink/04-runtime/04.03-observability/metrics-and-monitoring.md |
| Def-F-15-03 | 业务指标 (Business Metrics) | 定义 | Flink/04-runtime/04.03-observability/metrics-and-monitoring.md |
| Def-F-15-04 | 健康度评分 (Health Score) | 定义 | Flink/04-runtime/04.03-observability/metrics-and-monitoring.md |
| Def-F-15-05 | 分布式追踪 (Distributed Tracing) | 定义 | Flink/04-runtime/04.03-observability/distributed-tracing.md |
| Def-F-15-06 | Span与Trace | 定义 | Flink/04-runtime/04.03-observability/distributed-tracing.md |
| Def-F-15-07 | 上下文传播 (Context Propagation) | 定义 | Flink/04-runtime/04.03-observability/distributed-tracing.md |
| Def-F-15-08 | 采样策略 (Sampling Strategy) | 定义 | Flink/04-runtime/04.03-observability/distributed-tracing.md |
| Def-F-15-09 | Split-level指标 (Split-level Metrics) | 定义 | Flink/04-runtime/04.03-observability/split-level-watermark-metrics.md |
| Def-F-15-10 | OpenTelemetry统一可观测性模型 | 定义 | Flink/04-runtime/04.03-observability/opentelemetry-streaming-observability.md |
| Def-F-15-11 | 可观测性三支柱统一模型 | 定义 | Flink/04-runtime/04.03-observability/opentelemetry-streaming-observability.md |
| Def-F-15-12 | EventReporter 接口 | 定义 | Flink/04-runtime/04.03-observability/event-reporting.md |
| Def-F-15-13 | 内置系统事件 (Built-in System Events) | 定义 | Flink/04-runtime/04.03-observability/event-reporting.md |
| Def-F-15-14 | 自定义事件类型 (Custom Event Types) | 定义 | Flink/04-runtime/04.03-observability/event-reporting.md |
| Def-F-15-15 | Flink/15-observability/opentelemetry-streaming-observability.md | 定义 |  |
| Def-F-15-16 | Flink/15-observability/opentelemetry-streaming-observability.md | 定义 |  |
| Def-F-15-17 | Flink/15-observability/opentelemetry-streaming-observability.md | 定义 |  |
| Def-F-15-20 | 数据质量 (Data Quality) | 定义 | Flink/04-runtime/04.03-observability/realtime-data-quality-monitoring.md |
| Def-F-15-21 | 准确性 (Accuracy) | 定义 | Flink/04-runtime/04.03-observability/realtime-data-quality-monitoring.md |
| Def-F-15-22 | 完整性 (Completeness) | 定义 | Flink/04-runtime/04.03-observability/realtime-data-quality-monitoring.md |
| Def-F-15-23 | 一致性 (Consistency) | 定义 | Flink/04-runtime/04.03-observability/realtime-data-quality-monitoring.md |
| Def-F-15-24 | 及时性 (Timeliness) | 定义 | Flink/04-runtime/04.03-observability/realtime-data-quality-monitoring.md |
| Def-F-15-25 | 有效性 (Validity) | 定义 | Flink/04-runtime/04.03-observability/realtime-data-quality-monitoring.md |
| Def-F-15-26 | 数据剖析 (Data Profiling) | 定义 | Flink/04-runtime/04.03-observability/realtime-data-quality-monitoring.md |
| Def-F-15-27 | 质量检查算子 (Quality Check Operator) | 定义 | Flink/04-runtime/04.03-observability/realtime-data-quality-monitoring.md |
| Def-F-15-28 | 死信队列 (Dead Letter Queue, DLQ) | 定义 | Flink/04-runtime/04.03-observability/realtime-data-quality-monitoring.md |
| Def-F-15-30 | 可观测性三元组 | 定义 | Flink/04-runtime/04.03-observability/flink-opentelemetry-observability.md |
| Def-F-15-31 | OpenTelemetry 数据模型 | 定义 | Flink/04-runtime/04.03-observability/flink-opentelemetry-observability.md |
| Def-F-15-32 | 流处理可观测性维度 | 定义 | Flink/04-runtime/04.03-observability/flink-opentelemetry-observability.md |
| Def-F-15-33 | Flink Metrics 分类体系 | 定义 | Flink/04-runtime/04.03-observability/flink-opentelemetry-observability.md |
| Def-F-15-34 | 分布式追踪语义 | 定义 | Flink/04-runtime/04.03-observability/flink-opentelemetry-observability.md |
| Def-F-15-35 | SLO/SLI 定义 | 定义 | Flink/04-runtime/04.03-observability/flink-opentelemetry-observability.md |
| Def-F-15-40 | 流处理监控特殊性 | 定义 | Flink/04-runtime/04.03-observability/streaming-metrics-monitoring-slo.md |
| Def-F-15-41 | 关键指标分类 | 定义 | Flink/04-runtime/04.03-observability/streaming-metrics-monitoring-slo.md |
| Def-F-15-42 | SLO/SLI 分层模型 | 定义 | Flink/04-runtime/04.03-observability/streaming-metrics-monitoring-slo.md |
| Def-F-15-43 | 监控工具选型空间 | 定义 | Flink/04-runtime/04.03-observability/streaming-metrics-monitoring-slo.md |
| Def-F-15-44 | 背压指标量化 | 定义 | Flink/04-runtime/04.03-observability/streaming-metrics-monitoring-slo.md |
| Def-F-15-45 | 监控仪表板分层 | 定义 | Flink/04-runtime/04.03-observability/streaming-metrics-monitoring-slo.md |
| Def-F-15-50 | 可观测性体系架构 | 定义 | Flink/04-runtime/04.03-observability/flink-observability-complete-guide.md |
| Def-F-15-51 | 指标类型分类体系 | 定义 | Flink/04-runtime/04.03-observability/flink-observability-complete-guide.md |
| Def-F-15-52 | 指标作用域层级 | 定义 | Flink/04-runtime/04.03-observability/flink-observability-complete-guide.md |
| Def-F-15-53 | 日志事件模型 | 定义 | Flink/04-runtime/04.03-observability/flink-observability-complete-guide.md |
| Def-F-15-54 | 分布式追踪语义 | 定义 | Flink/04-runtime/04.03-observability/flink-observability-complete-guide.md |
| Def-F-15-55 | 告警规则模型 | 定义 | Flink/04-runtime/04.03-observability/flink-observability-complete-guide.md |
| Def-F-15-56 | SLO/SLI 形式化定义 | 定义 | Flink/04-runtime/04.03-observability/flink-observability-complete-guide.md |
| Lemma-F-01-01 | 类型完备性 | 引理 | Flink/flink-data-types-reference.md |
| Lemma-F-01-02 | 类型转换单调性 | 引理 | Flink/flink-data-types-reference.md |
| Lemma-F-01-09 | 存算分离带来扩缩容灵活性 | 引理 | Flink/01-concepts/flink-architecture-evolution-1x-to-2x.md |
| Lemma-F-01-10 | 异步模型提升资源利用率 | 引理 | Flink/01-concepts/flink-architecture-evolution-1x-to-2x.md |
| Lemma-F-02-01 | 函数确定性分类 | 引理 | Flink/flink-built-in-functions-reference.md |
| Lemma-F-02-02 | 异步资源配额保持引理 | 引理 | Struct/Proof-Chains-Flink-Implementation.md |
| Lemma-F-02-03 | 按键 FIFO 保持性证明 | 引理 | Flink/02-core/async-execution-model.md |
| Lemma-F-02-04 | 自适应收敛性 | 引理 | Flink/02-core/adaptive-execution-engine-v2.md |
| Lemma-F-02-05 | 倾斜检测完备性 | 引理 | Flink/02-core/adaptive-execution-engine-v2.md |
| Lemma-F-02-06 | 状态后端访问延迟排序 | 引理 | Flink/02-core/state-backends-deep-comparison.md |
| Lemma-F-02-07 | 状态容量扩展性 | 引理 | Flink/02-core/state-backends-deep-comparison.md |
| Lemma-F-02-08 | 状态后端演进规律 | 引理 | Flink/02-core/state-backend-evolution-analysis.md |
| Lemma-F-02-09 | 故障恢复时间演进 | 引理 | Flink/02-core/state-backend-evolution-analysis.md |
| Lemma-F-02-10 | CBFC 粒度优势 | 引理 | Flink/02-core/network-stack-evolution.md |
| Lemma-F-02-11 | 背压传播延迟演进 | 引理 | Flink/02-core/network-stack-evolution.md |
| Lemma-F-02-20 | ETL管道可组合性引理 | 引理 |  |
| Lemma-F-02-21 | Schema演化保持性引理 | 引理 |  |
| Lemma-F-02-23 | Checkpoint Barrier 对齐引理 | 引理 | Struct/Proof-Chains-Flink-Implementation.md |
| Lemma-F-02-40 | (MultiJoin状态上界): 对于 $n$ 路Join，设各流Key空间大小为 $ | 引理 | Flink/02-core/multi-way-join-optimization.md |
| Lemma-F-02-41 | (Join链状态下界): 传统Join链的最小状态条目数满足： | 引理 | Flink/02-core/multi-way-join-optimization.md |
| Lemma-F-02-50 | 自适应间隔收敛性 | 引理 | Flink/02-core/smart-checkpointing-strategies.md |
| Lemma-F-02-51 | 增量检查点存储上界 | 引理 | Flink/02-core/smart-checkpointing-strategies.md |
| Lemma-F-02-52 | 局部检查点一致性保证 | 引理 | Flink/02-core/smart-checkpointing-strategies.md |
| Lemma-F-02-60 | TTL 过期状态的单调性 | 引理 | Flink/02-core/flink-state-ttl-best-practices.md |
| Lemma-F-02-61 | 清理策略的及时性排序 | 引理 | Flink/02-core/flink-state-ttl-best-practices.md |
| Lemma-F-02-62 | 状态可见性与一致性边界 | 引理 | Flink/02-core/flink-state-ttl-best-practices.md |
| Lemma-F-02-70 | 异步快照非阻塞性引理 | 引理 | Struct/Proof-Chains-Flink-Implementation.md |
| Lemma-F-02-71 | State Backend 容量扩展性 | 引理 | Flink/02-core/flink-state-management-complete-guide.md |
| Lemma-F-02-72 | 非对齐Checkpoint有界一致性 | 引理 |  |
| Lemma-F-02-73 | 对齐Checkpoint延迟上界 | 引理 |  |
| Lemma-F-02-74 | 事务超时约束 | 引理 |  |
| Lemma-F-03-01 | 类型完备性 | 引理 | Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md |
| Lemma-F-03-02 | 类型可比较性 | 引理 | Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md |
| Lemma-F-03-03 | 嵌套类型限制 | 引理 | Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md |
| Lemma-F-03-04 | 嵌入模型的 Lipschitz 连续性 | 引理 | Flink/03-api/03.02-table-sql-api/vector-search.md |
| Lemma-F-03-07 | (Python UDF性能上界): 设 $T_{java}$ 为同功能Java UDF执行时间，$T_{py}$ 为Python UDF执行时间，则存在常数 $k > 1$ 使得： | 引理 | Flink/03-api/03.02-table-sql-api/flink-python-udf.md |
| Lemma-F-03-08 | (类型一致性): 对于任意Python UDF $\mathcal{U}_{py}$，若输入类型满足 $\Gamma \vdash e : \tau$，则输出类型满足： | 引理 | Flink/03-api/03.02-table-sql-api/flink-python-udf.md |
| Lemma-F-03-10 | 嵌入向量的 Lipschitz 连续性 | 引理 | Flink/03-api/03.02-table-sql-api/flink-vector-search-rag.md |
| Lemma-F-03-100 | Flink SQL 类型系统兼容性 | 引理 | Flink/03-api/03.02-table-sql-api/ansi-sql-2023-compliance-guide.md |
| Lemma-F-03-101 | 窗口函数代数封闭性 | 引理 | Flink/03-api/03.02-table-sql-api/ansi-sql-2023-compliance-guide.md |
| Lemma-F-03-30 | 物化表的幂等性 | 引理 | Flink/03-api/03.02-table-sql-api/flink-materialized-table-deep-dive.md |
| Lemma-F-03-31 | 分桶数据倾斜边界引理 | 引理 |  |
| Lemma-F-03-70 | Join Hint优先级 | 引理 | Flink/03-api/03.02-table-sql-api/flink-sql-hints-optimization.md |
| Lemma-F-03-71 | State TTL与Checkpoint关系 | 引理 | Flink/03-api/03.02-table-sql-api/flink-sql-hints-optimization.md |
| Lemma-F-03-72 | JSON函数性能特征 | 引理 | Flink/03-api/03.02-table-sql-api/flink-sql-hints-optimization.md |
| Lemma-F-04-01 | (尾部延迟引理) | 引理 | Flink/05-ecosystem/05.01-connectors/diskless-kafka-cloud-native.md |
| Lemma-F-04-02 | (写入延迟不变性) | 引理 | Flink/05-ecosystem/05.01-connectors/diskless-kafka-cloud-native.md |
| Lemma-F-04-03 | (Change Streams 有序性保证) | 引理 | Flink/05-ecosystem/05.01-connectors/mongodb-connector-complete-guide.md |
| Lemma-F-04-04 | (批量写入原子性边界) | 引理 | Flink/05-ecosystem/05.01-connectors/mongodb-connector-complete-guide.md |
| Lemma-F-04-07 | 调度器演进规律 | 引理 | Flink/04-runtime/04.01-deployment/evolution/scheduling-evolution.md |
| Lemma-F-04-08 | 扩缩容速度演进 | 引理 | Flink/04-runtime/04.01-deployment/evolution/scheduling-evolution.md |
| Lemma-F-04-09 | 蓝绿部署状态隔离性 | 引理 | Flink/04-runtime/04.01-deployment/flink-k8s-operator-1.14-guide.md |
| Lemma-F-04-10 | 流量切换原子性 | 引理 | Flink/04-runtime/04.01-deployment/flink-k8s-operator-1.14-guide.md |
| Lemma-F-04-100 | (连接器组合封闭性) | 引理 | Flink/05-ecosystem/05.01-connectors/flink-connectors-ecosystem-complete-guide.md |
| Lemma-F-04-101 | (交付保证传递性) | 引理 | Flink/05-ecosystem/05.01-connectors/flink-connectors-ecosystem-complete-guide.md |
| Lemma-F-04-11 | 回滚时间边界 | 引理 | Flink/04-runtime/04.01-deployment/flink-k8s-operator-1.14-guide.md |
| Lemma-F-04-20 | (CDC延迟边界) | 引理 | Flink/05-ecosystem/05.01-connectors/04.04-cdc-debezium-integration.md |
| Lemma-F-04-200 | 连接器版本向后兼容性 | 引理 | Flink/05-ecosystem/05.01-connectors/flink-24-connectors-guide.md |
| Lemma-F-04-201 | Kafka 3.x Exactly-Once 语义保持 | 引理 | Flink/05-ecosystem/05.01-connectors/flink-24-connectors-guide.md |
| Lemma-F-04-21 | (初始快照一致性) | 引理 | Flink/05-ecosystem/05.01-connectors/04.04-cdc-debezium-integration.md |
| Lemma-F-04-40 | CDC一致性保证 | 引理 | Flink/05-ecosystem/05.01-connectors/flink-cdc-3.0-data-integration.md |
| Lemma-F-04-41 | 延迟边界 | 引理 | Flink/05-ecosystem/05.01-connectors/flink-cdc-3.0-data-integration.md |
| Lemma-F-04-42 | (Z-Ordering 查询优化边界) | 引理 | Flink/05-ecosystem/05.01-connectors/flink-delta-lake-integration.md |
| Lemma-F-04-50 | Iceberg 快照的不可变性与线性历史 | 引理 | Flink/05-ecosystem/05.01-connectors/flink-iceberg-integration.md |
| Lemma-F-04-51 | 隐藏分区的查询透明性 | 引理 | Flink/05-ecosystem/05.01-connectors/flink-iceberg-integration.md |
| Lemma-F-04-52 | 增量消费完备性 | 引理 | Flink/05-ecosystem/05.01-connectors/flink-iceberg-integration.md |
| Lemma-F-04-60 | CDC捕获完整性引理 | 引理 |  |
| Lemma-F-04-61 | 模式变更传播一致性引理 | 引理 |  |
| Lemma-F-05-01 | (嵌入式架构的状态访问延迟上界) | 引理 | Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-kafka-streams.md |
| Lemma-F-05-02 | (集群架构的水平扩展能力) | 引理 | Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-kafka-streams.md |
| Lemma-F-06-01 | (内存配置的约束传播) | 引理 | Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md |
| Lemma-F-06-02 | (并行度与吞吐量的亚线性关系) | 引理 | Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md |
| Lemma-F-06-03 | (检查点间隔与恢复时间的权衡) | 引理 | Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md |
| Lemma-F-06-04 | (序列化开销的比例边界) | 引理 | Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md |
| Lemma-F-06-05 | (算子链合并的收益边界) | 引理 | Flink/09-practices/09.03-performance-tuning/06.02-performance-optimization-complete.md |
| Lemma-F-06-06 | (SQL谓词下推的有效性条件) | 引理 | Flink/09-practices/09.03-performance-tuning/06.02-performance-optimization-complete.md |
| Lemma-F-06-07 | (异步I/O的并行度最优性) | 引理 | Flink/09-practices/09.03-performance-tuning/06.02-performance-optimization-complete.md |
| Lemma-F-06-08 | (批处理大小的吞吐-延迟权衡) | 引理 | Flink/09-practices/09.03-performance-tuning/06.02-performance-optimization-complete.md |
| Lemma-F-06-10 | (规模经济效应) | 引理 | Flink/09-practices/09.03-performance-tuning/flink-tco-cost-optimization-guide.md |
| Lemma-F-06-100 | 0.2.x版本API兼容性 | 引理 | Flink/06-ai-ml/flip-531-ai-agents-ga-guide.md |
| Lemma-F-06-101 | Embedding调用延迟边界 | 引理 | Flink/06-ai-ml/flip-531-ai-agents-ga-guide.md |
| Lemma-F-06-102 | MCP Server连接稳定性 | 引理 | Flink/06-ai-ml/flip-531-ai-agents-ga-guide.md |
| Lemma-F-06-11 | (存算分离的成本边界) | 引理 | Flink/09-practices/09.03-performance-tuning/flink-tco-cost-optimization-guide.md |
| Lemma-F-06-15 | 流式输出延迟引理 | 引理 | Flink/06-ai-ml/flink-llm-realtime-inference-guide.md |
| Lemma-F-06-16 | 批处理最优大小引理 | 引理 | Flink/06-ai-ml/flink-llm-realtime-inference-guide.md |
| Lemma-F-06-20 | (物化策略的延迟边界) | 引理 | Flink/09-practices/09.03-performance-tuning/flink-dbt-integration.md |
| Lemma-F-06-21 | (流式模型幂等性条件) | 引理 | Flink/09-practices/09.03-performance-tuning/flink-dbt-integration.md |
| Lemma-F-06-300 | Checkpoint一致性引理 | 引理 | Flink/06-ai-ml/flink-agent-workflow-engine.md |
| Lemma-F-06-301 | Agent调用幂等性引理 | 引理 | Flink/06-ai-ml/flink-agent-workflow-engine.md |
| Lemma-F-06-40 | (成本边界效应) | 引理 | Flink/09-practices/09.03-performance-tuning/stream-processing-cost-optimization.md |
| Lemma-F-06-41 | (Spot实例成本稳定性) | 引理 | Flink/09-practices/09.03-performance-tuning/stream-processing-cost-optimization.md |
| Lemma-F-06-50 | 信用值流控延迟上界 | 引理 |  |
| Lemma-F-06-51 | 零拷贝带宽利用率 | 引理 |  |
| Lemma-F-06-52 | POJO序列化加速比 | 引理 |  |
| Lemma-F-06-53 | 分代GC停顿时间 | 引理 |  |
| Lemma-F-06-54 | ForSt异步IO吞吐 | 引理 |  |
| Lemma-F-07-01 | (端到端延迟边界): 在Flink实时推荐系统中，从用户行为发生到推荐结果更新的端到端延迟 $L_{total}$ 满足： | 引理 | Flink/09-practices/09.01-case-studies/case-ecommerce-realtime-recommendation.md |
| Lemma-F-07-02 | (实时特征有效性): 设离线批处理特征为 $\phi_{batch}$，实时特征为 $\phi_{rt}$，则推荐准确率损失上界为： | 引理 | Flink/09-practices/09.01-case-studies/case-ecommerce-realtime-recommendation.md |
| Lemma-F-07-08 | 位置更新实时性下界 | 引理 | Flink/09-practices/09.01-case-studies/case-logistics-realtime-tracking.md |
| Lemma-F-07-09 | 地理围栏检测概率 | 引理 | Flink/09-practices/09.01-case-studies/case-logistics-realtime-tracking.md |
| Lemma-F-07-10 | (端到端延迟分解): 实时风控系统的端到端延迟 $L_{\text{total}}$ 可分解为： | 引理 | Flink/09-practices/09.01-case-studies/case-financial-realtime-risk-control.md |
| Lemma-F-07-11 | (实时准确率边界): 设批处理系统准确率为 $A_{\text{batch}}$，实时系统准确率为 $A_{\text{realtime}}$，则： | 引理 | Flink/09-practices/09.01-case-studies/case-financial-realtime-risk-control.md |
| Lemma-F-07-12 | (水平扩展线性度): Flink风控系统的吞吐量 $T$ 与并行度 $p$ 满足： | 引理 | Flink/09-practices/09.01-case-studies/case-financial-realtime-risk-control.md |
| Lemma-F-07-211 | (情感聚合单调性): 对于话题 $T$ 的情感分析，当新内容 $p_{new}$ 的情感极性与当前情感一致时，聚合情感会强化： | 引理 | Flink/09-practices/09.01-case-studies/case-social-media-analytics.md |
| Lemma-F-07-212 | (趋势检测召回率下界): 设真实趋势发生率为 $\rho$，检测窗口为 $W$，则召回率满足： | 引理 | Flink/09-practices/09.01-case-studies/case-social-media-analytics.md |
| Lemma-F-07-213 | (传播覆盖上界): 在独立级联模型下，初始种子集 $\mathcal{S}_0$ 的期望传播覆盖满足： | 引理 | Flink/09-practices/09.01-case-studies/case-social-media-analytics.md |
| Lemma-F-07-221 | (图特征区分度下界): 设欺诈节点集合为 $\mathcal{V}_f$，正常节点为 $\mathcal{V}_n$，图嵌入的区分能力满足： | 引理 | Flink/09-practices/09.01-case-studies/case-fraud-detection-advanced.md |
| Lemma-F-07-222 | (欺诈检测延迟分解): 从交易发生到风险决策的端到端延迟： | 引理 | Flink/09-practices/09.01-case-studies/case-fraud-detection-advanced.md |
| Lemma-F-07-223 | (模型时效性衰减): 设模型训练时刻为 $t_0$，当前时刻为 $t$，模型效果衰减满足： | 引理 | Flink/09-practices/09.01-case-studies/case-fraud-detection-advanced.md |
| Lemma-F-07-231 | (库存状态一致性): 对于任意位置 $l$、产品 $p$ 和时刻 $t$，库存计算满足： | 引理 | Flink/09-practices/09.01-case-studies/case-supply-chain-optimization.md |
| Lemma-F-07-232 | (预测误差上界): 指数平滑预测的MAPE（平均绝对百分比误差）满足： | 引理 | Flink/09-practices/09.01-case-studies/case-supply-chain-optimization.md |
| Lemma-F-07-241 | (多源数据一致性): 对于同一物理量 $m$ 的多个传感器测量 $\{m_1, m_2, \ldots, m_n\}$，融合估计 $\hat{m}$ 的方差满足： | 引理 | Flink/09-practices/09.01-case-studies/case-smart-city-iot.md |
| Lemma-F-07-242 | (城市事件响应延迟): 从事件发生到决策执行的端到端延迟： | 引理 | Flink/09-practices/09.01-case-studies/case-smart-city-iot.md |
| Lemma-F-07-243 | (数字孪生同步误差): 数字孪生状态 $\mathcal{DT}(t)$ 与物理世界状态 $S(t)$ 的同步误差： | 引理 | Flink/09-practices/09.01-case-studies/case-smart-city-iot.md |
| Lemma-F-07-251 | (异常检测响应延迟): 从生理异常发生到告警触发的端到端延迟： | 引理 | Flink/09-practices/09.01-case-studies/case-healthcare-monitoring.md |
| Lemma-F-07-252 | (告警疲劳控制): 通过分层阈值和趋势确认，假阳性率可控制在： | 引理 | Flink/09-practices/09.01-case-studies/case-healthcare-monitoring.md |
| Lemma-F-07-253 | (数据完整性边界): 对于采样频率 $f$，数据完整性要求： | 引理 | Flink/09-practices/09.01-case-studies/case-healthcare-monitoring.md |
| Lemma-F-07-261 | (预测误差下界): 在平稳假设下，最小可达MAPE满足： | 引理 | Flink/09-practices/09.01-case-studies/case-energy-grid-optimization.md |
| Lemma-F-07-262 | (电网控制响应延迟): 从测量采集到控制指令执行的端到端延迟： | 引理 | Flink/09-practices/09.01-case-studies/case-energy-grid-optimization.md |
| Lemma-F-07-263 | (储能投资回收期): 储能系统的投资回收期： | 引理 | Flink/09-practices/09.01-case-studies/case-energy-grid-optimization.md |
| Lemma-F-07-30 | (端到端延迟分解): 智能制造IoT系统的端到端延迟 $L_{total}$ 可分解为： | 引理 | Flink/09-practices/09.01-case-studies/case-smart-manufacturing-iot.md |
| Lemma-F-07-31 | (故障检测准确率边界): 设故障检测系统的真正例率为 $TPR$，假正例率为 $FPR$，则： | 引理 | Flink/09-practices/09.01-case-studies/case-smart-manufacturing-iot.md |
| Lemma-F-07-32 | (水平扩展线性度): Flink智能制造系统的吞吐量 $T$ 与并行度 $p$ 满足： | 引理 | Flink/09-practices/09.01-case-studies/case-smart-manufacturing-iot.md |
| Lemma-F-07-50 | (预测误差下界): 对于任何负荷预测模型，预测误差的理论下界由信号本身的不可预测性决定： | 引理 | Flink/09-practices/09.01-case-studies/case-smart-grid-energy-management.md |
| Lemma-F-07-51 | (预测精度随提前期衰减): 预测精度随预测提前期 $h$ 增加而衰减： | 引理 | Flink/09-practices/09.01-case-studies/case-smart-grid-energy-management.md |
| Lemma-F-07-52 | (端到端延迟分解): 智能电网实时处理系统的端到端延迟 $L_{total}$ 可分解为： | 引理 | Flink/09-practices/09.01-case-studies/case-smart-grid-energy-management.md |
| Lemma-F-07-53 | (功率平衡稳定性条件): 电网频率稳定的必要条件是实时功率平衡： | 引理 | Flink/09-practices/09.01-case-studies/case-smart-grid-energy-management.md |
| Lemma-F-07-61 | (作弊检测准确率上界) | 引理 | Flink/09-practices/09.01-case-studies/case-gaming-realtime-analytics.md |
| Lemma-F-07-62 | (检测延迟与准确率权衡) | 引理 | Flink/09-practices/09.01-case-studies/case-gaming-realtime-analytics.md |
| Lemma-F-07-63 | (端到端延迟分解) | 引理 | Flink/09-practices/09.01-case-studies/case-gaming-realtime-analytics.md |
| Lemma-F-07-64 | (状态访问延迟) | 引理 | Flink/09-practices/09.01-case-studies/case-gaming-realtime-analytics.md |
| Lemma-F-07-71 | (会话边界一致性): 对于有序事件流 $\mathcal{E} = | 引理 | Flink/09-practices/09.01-case-studies/case-clickstream-user-behavior-analytics.md |
| Lemma-F-07-72 | (漏斗计算单调性): 在转化漏斗 $\mathcal{F} = | 引理 | Flink/09-practices/09.01-case-studies/case-clickstream-user-behavior-analytics.md |
| Lemma-F-07-73 | (检测准确率下界): 设人类用户行为特征分布为 $\mathcal{N}(\mu_h, \sigma_h^2)$，Bot特征分布为 $\mathcal{N}(\mu_b, \sigma_b^2)$，则最优分类器准确率下界为： | 引理 | Flink/09-practices/09.01-case-studies/case-clickstream-user-behavior-analytics.md |
| Lemma-F-08-01 | 性能基线引理 (Performance Baseline Lemma) | 引理 | Flink/08-roadmap/08.01-flink-24/2026-q2-flink-tasks.md |
| Lemma-F-08-02 | Q2 约束引理 (Q2 Constraints Lemma) | 引理 | Flink/08-roadmap/08.01-flink-24/2026-q2-flink-tasks.md |
| Lemma-F-08-03 | 架构兼容性引理 | 引理 | Flink/08-roadmap/08.01-flink-24/flink-2.1-frontier-tracking.md |
| Lemma-F-08-04 | 弹性响应时间 | 引理 | Flink/08-roadmap/08.01-flink-24/flink-2.1-frontier-tracking.md |
| Lemma-F-08-40 | Kafka 2PC延迟改进 | 引理 | Flink/08-roadmap/08.01-flink-24/flink-2.3-2.4-roadmap.md |
| Lemma-F-08-41 | 贡献者留存率 | 引理 | Flink/08-roadmap/08.01-flink-24/community-dynamics-tracking.md |
| Lemma-F-08-50 | 向后兼容性引理 | 引理 | Flink/08-roadmap/08.01-flink-24/flink-version-evolution-complete-guide.md |
| Lemma-F-08-51 | 迁移复杂度边界引理 | 引理 | Flink/08-roadmap/08.01-flink-24/flink-version-evolution-complete-guide.md |
| Lemma-F-08-52 | 混合执行数据一致性 | 引理 | Flink/08-roadmap/08.01-flink-24/flink-25-stream-batch-unification.md |
| Lemma-F-08-53 | 统一存储层访问性能 | 引理 | Flink/08-roadmap/08.01-flink-24/flink-25-stream-batch-unification.md |
| Lemma-F-08-60 | API兼容性保持 | 引理 | Flink/08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md |
| Lemma-F-08-61 | 迁移路径完备性 | 引理 | Flink/08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md |
| Lemma-F-08-70 | Checkpoint Optimization Effectiveness | 引理 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Lemma-F-08-71 | AI Agent Preview Stability | 引理 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Lemma-F-08-72 | Recovery Time Bound | 引理 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Lemma-F-08-73 | State Complexity Bound | 引理 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Lemma-F-09-01 | (Flink CDC 版本约束) | 引理 | Flink/09-practices/09.03-performance-tuning/jdk-11-migration-guide.md |
| Lemma-F-09-02 | (GC 性能改进边界) | 引理 | Flink/09-practices/09.03-performance-tuning/jdk-11-migration-guide.md |
| Lemma-F-09-03 | (API 移除影响传播) | 引理 | Flink/09-practices/09.03-performance-tuning/jdk-11-migration-guide.md |
| Lemma-F-09-04 | 配置向后兼容保证 | 引理 | Flink/09-practices/09.04-deployment/flink-k8s-operator-migration-1.13-to-1.14.md |
| Lemma-F-09-05 | 零停机升级条件 | 引理 | Flink/09-practices/09.04-deployment/flink-k8s-operator-migration-1.13-to-1.14.md |
| Lemma-F-09-06 | 状态迁移原子性 | 引理 | Flink/09-practices/09.04-deployment/flink-k8s-operator-migration-1.13-to-1.14.md |
| Lemma-F-09-07 | 声明式资源优化效率 | 引理 | Flink/09-practices/09.04-deployment/flink-k8s-operator-new-features-1.14.md |
| Lemma-F-09-08 | Autoscaling V2 预测准确性 | 引理 | Flink/09-practices/09.04-deployment/flink-k8s-operator-new-features-1.14.md |
| Lemma-F-09-09 | Session 集群资源利用率 | 引理 | Flink/09-practices/09.04-deployment/flink-k8s-operator-new-features-1.14.md |
| Lemma-F-09-15 | State Migration Compatibility | 引理 | Flink/03-api/09-language-foundations/05-datastream-v2-api.md |
| Lemma-F-09-16 | Typeclass Resolution Completeness | 引理 | Flink/03-api/09-language-foundations/01.03-scala3-type-system-formalization.md |
| Lemma-F-09-17 | DOT类型保持性 | 引理 |  |
| Lemma-F-09-18 | 路径类型消解引理 | 引理 |  |
| Lemma-F-09-19 | Hummock写入原子性 | 引理 |  |
| Lemma-F-09-20 | 传统流处理器固定成本下界 | 引理 | Flink/03-api/09-language-foundations/07.01-timely-dataflow-optimization.md |
| Lemma-F-09-21 | Timely Dataflow 优化后成本 | 引理 | Flink/03-api/09-language-foundations/07.01-timely-dataflow-optimization.md |
| Lemma-F-09-22 | 空间复杂度 | 引理 | Flink/03-api/09-language-foundations/07.01-timely-dataflow-optimization.md |
| Lemma-F-09-23 | 调度复杂度 | 引理 | Flink/03-api/09-language-foundations/07.01-timely-dataflow-optimization.md |
| Lemma-F-09-24 | 事件驱动调度复杂度 | 引理 |  |
| Lemma-F-09-25 | WASI能力隔离性 | 引理 |  |
| Lemma-F-09-26 | 组件接口类型保持 | 引理 |  |
| Lemma-F-09-30 | Ordered Output Guarantee | 引理 | Flink/03-api/09-language-foundations/02.03-python-async-api.md |
| Lemma-F-09-32 | Watermark 传播单调性 | 引理 | Flink/03-api/09-language-foundations/flink-datastream-api-complete-guide.md |
| Lemma-F-10-01 | 状态大小与计算成本的正相关性 | 引理 | Flink/04-runtime/04.01-deployment/cost-optimization-calculator.md |
| Lemma-F-10-20 | 状态一致性保证 | 引理 | Flink/04-runtime/04.01-deployment/flink-kubernetes-operator-deep-dive.md |
| Lemma-F-10-21 | 升级原子性 | 引理 | Flink/04-runtime/04.01-deployment/flink-kubernetes-operator-deep-dive.md |
| Lemma-F-10-22 | 扩缩容无中断性 | 引理 | Flink/04-runtime/04.01-deployment/flink-kubernetes-operator-deep-dive.md |
| Lemma-F-10-30 | 背压与并行度单调关系引理 | 引理 |  |
| Lemma-F-10-31 | 目标利用率最优性引理 | 引理 |  |
| Lemma-F-10-32 | 顶点独立扩缩容兼容性引理 | 引理 |  |
| Lemma-F-10-40 | Slot 分配完备性 | 引理 | Flink/04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md |
| Lemma-F-10-41 | 自适应调度器的收敛性 | 引理 | Flink/04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md |
| Lemma-F-10-50 | 热更新原子性保证 | 引理 | Flink/04-runtime/04.01-deployment/flink-24-deployment-improvements.md |
| Lemma-F-10-51 | 蓝绿部署零停机性 | 引理 | Flink/04-runtime/04.01-deployment/flink-24-deployment-improvements.md |
| Lemma-F-10-52 | 金丝雀流量切分一致性 | 引理 | Flink/04-runtime/04.01-deployment/flink-24-deployment-improvements.md |
| Lemma-F-10-53 | 多租户资源隔离性 | 引理 | Flink/04-runtime/04.01-deployment/flink-24-deployment-improvements.md |
| Lemma-F-11-01 | 吞吐量与延迟的权衡关系 | 引理 | Flink/09-practices/09.02-benchmarking/performance-benchmarking-guide.md |
| Lemma-F-11-02 | 扩展性线性边界 | 引理 | Flink/09-practices/09.02-benchmarking/performance-benchmarking-guide.md |
| Lemma-F-11-04 | Nexmark查询复杂度递增规律 | 引理 |  |
| Lemma-F-11-05 | 并行度扩展效率边界 | 引理 |  |
| Lemma-F-11-06 | 状态后端性能权衡 | 引理 |  |
| Lemma-F-11-07 | Checkpoint频率与恢复RTO关系 | 引理 |  |
| Lemma-F-12-01 | 参数一致性边界 | 引理 | Flink/06-ai-ml/flink-ml-architecture.md |
| Lemma-F-12-02 | (在线学习后悔界) | 引理 | Flink/06-ai-ml/online-learning-algorithms.md |
| Lemma-F-12-03 | 推理延迟分解 | 引理 | Flink/06-ai-ml/model-serving-streaming.md |
| Lemma-F-12-04 | 批量推理吞吐量增益 | 引理 | Flink/06-ai-ml/model-serving-streaming.md |
| Lemma-F-12-05 | 特征-标签关联完备性边界 | 引理 | Flink/06-ai-ml/online-learning-production.md |
| Lemma-F-12-06 | 影子模式无偏性保证 | 引理 | Flink/06-ai-ml/online-learning-production.md |
| Lemma-F-12-100 | 向量搜索精度-延迟权衡 | 引理 | Flink/06-ai-ml/flink-ai-ml-integration-complete-guide.md |
| Lemma-F-12-101 | ML_PREDICT批量推理吞吐量下界 | 引理 | Flink/06-ai-ml/flink-ai-ml-integration-complete-guide.md |
| Lemma-F-12-102 | 水平扩展线性度 | 引理 |  |
| Lemma-F-12-12 | 特征点查一致性引理 | 引理 |  |
| Lemma-F-12-13 | 特征物化视图增量更新引理 | 引理 |  |
| Lemma-F-12-15 | 流式 LLM 推理的延迟边界 | 引理 | Flink/06-ai-ml/flink-llm-integration.md |
| Lemma-F-12-16 | ML_PREDICT 的确定性保证 | 引理 | Flink/06-ai-ml/flink-llm-integration.md |
| Lemma-F-12-17 | RAG 上下文窗口约束 | 引理 | Flink/06-ai-ml/flink-llm-integration.md |
| Lemma-F-12-18 | Agent 状态一致性 | 引理 | Flink/06-ai-ml/flink-agents-flip-531.md |
| Lemma-F-12-19 | LLM 调用幂等性 | 引理 | Flink/06-ai-ml/flink-agents-flip-531.md |
| Lemma-F-12-20 | Agent 工作流延迟边界 | 引理 | Flink/06-ai-ml/flink-agents-flip-531.md |
| Lemma-F-12-50 | 显存占用边界 | 引理 | Flink/06-ai-ml/flink-25-gpu-acceleration.md |
| Lemma-F-12-51 | 流并行度上限 | 引理 | Flink/06-ai-ml/flink-25-gpu-acceleration.md |
| Lemma-F-12-90 | Agent状态持久化延迟 | 引理 | Flink/06-ai-ml/flink-ai-agents-flip-531.md |
| Lemma-F-12-91 | Agent记忆容量边界 | 引理 | Flink/06-ai-ml/flink-ai-agents-flip-531.md |
| Lemma-F-13-01 | 认证强度与攻击面关系 | 引理 | Flink/09-practices/09.04-security/security-hardening-guide.md |
| Lemma-F-13-02 | 性能开销上界 | 引理 | Flink/09-practices/09.04-security/gpu-confidential-computing.md |
| Lemma-F-13-03 | 加密性能开销上界 | 引理 | Flink/09-practices/09.04-security/flink-security-complete-guide.md |
| Lemma-F-13-04 | 审计日志完整性 | 引理 | Flink/09-practices/09.04-security/flink-security-complete-guide.md |
| Lemma-F-13-10 | 字段级加密查询兼容性 | 引理 | Flink/09-practices/09.04-security/flink-24-security-enhancements.md |
| Lemma-F-13-11 | 审计日志完整性边界 | 引理 | Flink/09-practices/09.04-security/flink-24-security-enhancements.md |
| Lemma-F-13-18 | 动态身份绑定性质 | 引理 | Flink/09-practices/09.04-security/spiffe-spire-integration-guide.md |
| Lemma-F-13-19 | 证书轮换安全性质 | 引理 | Flink/09-practices/09.04-security/spiffe-spire-integration-guide.md |
| Lemma-F-14-01 | WASM UDF 安全隔离性 | 引理 | Flink/07-rust-native/flink-rust-ecosystem-trends-2026.md |
| Lemma-F-14-02 | Rust UDF 性能优势下界 | 引理 | Flink/07-rust-native/flink-rust-ecosystem-trends-2026.md |
| Lemma-F-14-03 | 湖仓格式的时间旅行完备性 | 引理 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-architecture.md |
| Lemma-F-14-04 | 流式写入的幂等性 | 引理 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-architecture.md |
| Lemma-F-14-05 | 流式Lakehouse延迟边界 | 引理 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-deep-dive-2026.md |
| Lemma-F-14-06 | Catalog标准化后的互操作性保证 | 引理 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-deep-dive-2026.md |
| Lemma-F-14-11 | (窗口切片复杂度). 对于时间窗口 $W$，设窗口内边数为 $ | 引理 | Flink/05-ecosystem/05.04-graph/flink-gelly-streaming-graph-processing.md |
| Lemma-F-14-12 | (流式连通组件的近似边界). 在边添加流模型下，设图演化速率为 $λ$（边/秒），算法处理延迟为 $τ$，则连通组件标识的滞后误差界为： | 引理 | Flink/05-ecosystem/05.04-graph/flink-gelly-streaming-graph-processing.md |
| Lemma-F-14-13 | (三角形计数的内存边界). 对于 $k$-跳邻居存储策略，流式三角形计数的内存消耗上界为： | 引理 | Flink/05-ecosystem/05.04-graph/flink-gelly-streaming-graph-processing.md |
| Lemma-F-15-01 | Trace完整性边界 | 引理 | Flink/04-runtime/04.03-observability/distributed-tracing.md |
| Lemma-F-15-02 | Trace-Metric-Log 关联完备性 | 引理 | Flink/04-runtime/04.03-observability/opentelemetry-streaming-observability.md |
| Lemma-F-15-20 | 指标采样一致性 | 引理 | Flink/04-runtime/04.03-observability/streaming-metrics-monitoring-slo.md |
| Lemma-F-15-21 | 背压与延迟的关联性 | 引理 | Flink/04-runtime/04.03-observability/streaming-metrics-monitoring-slo.md |
| Lemma-F-15-22 | Checkpoint 指标的可恢复性 | 引理 | Flink/04-runtime/04.03-observability/streaming-metrics-monitoring-slo.md |
| Lemma-F-15-30 | 可观测性信号正交性引理 | 引理 |  |
| Lemma-F-15-31 | 追踪采样代表性引理 | 引理 |  |
| Lemma-F-15-32 | Metrics聚合准确性引理 | 引理 |  |
| Lemma-F-15-40 | 指标采样一致性引理 | 引理 |  |
| Lemma-F-15-41 | 背压与延迟关联性引理 | 引理 |  |
| Lemma-F-15-42 | Checkpoint可恢复性引理 | 引理 |  |
| Lemma-F-15-50 | Checkpoint延迟上界 | 引理 |  |
| Prop-F-01-01 | 类型安全保证 | 命题 | Flink/flink-data-types-reference.md |
| Prop-F-01-08 | 架构演进保持语义兼容性 | 命题 | Flink/01-concepts/flink-architecture-evolution-1x-to-2x.md |
| Prop-F-02-01 | 类型推导完备性 | 命题 | Flink/flink-built-in-functions-reference.md |
| Prop-F-02-02 | 资源分配最优性 | 命题 | Flink/02-core/adaptive-execution-engine-v2.md |
| Prop-F-02-03 | 性能提升下界 | 命题 | Flink/02-core/adaptive-execution-engine-v2.md |
| Prop-F-02-04 | Buffer Debloating 缩短 Checkpoint Barrier 传播时间 | 命题 | Flink/02-core/backpressure-and-flow-control.md |
| Prop-F-02-05 | Credit 系统保证接收方缓冲区不溢出 | 命题 | Flink/02-core/backpressure-and-flow-control.md |
| Prop-F-02-06 | 故障恢复时间界限 | 命题 | Flink/02-core/state-backends-deep-comparison.md |
| Prop-F-02-07 | Delta Join V2 缓存命中率下界 | 命题 | Flink/02-core/flink-2.2-frontier-features.md |
| Prop-F-02-08 | VECTOR_SEARCH 与 ML_PREDICT 的组合复杂度 | 命题 | Flink/02-core/flink-2.2-frontier-features.md |
| Prop-F-02-09 | Materialized Table V2 智能推断完备性 | 命题 | Flink/02-core/flink-2.2-frontier-features.md |
| Prop-F-02-10 | SinkUpsertMaterializer V2 性能边界 | 命题 | Flink/02-core/flink-2.2-frontier-features.md |
| Prop-F-02-11 | Python Async API 吞吐量上界 | 命题 | Flink/02-core/flink-2.2-frontier-features.md |
| Prop-F-02-12 | Balanced Scheduling 负载均衡效果 | 命题 | Flink/02-core/flink-2.2-frontier-features.md |
| Prop-F-02-13 | Delta Join V2缓存命中率下界 | 命题 |  |
| Prop-F-02-14 | VECTOR_SEARCH与ML_PREDICT组合复杂度 | 命题 |  |
| Prop-F-02-15 | 状态复杂度上界 | 命题 | Flink/02-core/delta-join.md |
| Prop-F-02-16 | Exactly-Once语义保持 | 命题 | Flink/02-core/delta-join.md |
| Prop-F-02-17 | 缓存一致性边界 | 命题 | Flink/02-core/delta-join.md |
| Prop-F-02-18 | StreamingMultiJoinOperator优化有效性 | 命题 | Flink/02-core/delta-join.md |
| Prop-F-02-19 | Delta Join V2 缓存命中率下界 | 命题 | Flink/02-core/delta-join-production-guide.md |
| Prop-F-02-20 | 投影下推 IO 减少量 | 命题 | Flink/02-core/delta-join-production-guide.md |
| Prop-F-02-21 | Delta Join 端到端延迟边界 | 命题 | Flink/02-core/delta-join-production-guide.md |
| Prop-F-02-22 | CDC 源无 DELETE 约束的业务完备性 | 命题 | Flink/02-core/delta-join-production-guide.md |
| Prop-F-02-23 | 状态后端选型决策矩阵 | 命题 |  |
| Prop-F-02-24 | 无缝重配置保证 | 命题 | Flink/02-core/flink-2.0-forst-state-backend.md |
| Prop-F-02-25 | ETL管道吞吐量边界 | 命题 |  |
| Prop-F-02-40 | (状态减少比率): 对于均匀分布的 $n$ 路等值Join，MultiJoin相对于Join链的状态减少比率为： | 命题 | Flink/02-core/multi-way-join-optimization.md |
| Prop-F-02-41 | (延迟边界): MultiJoin的端到端延迟 $L_{\text{multi}}$ 与Join链延迟 $L_{\text{chain}}$ 满足： | 命题 | Flink/02-core/multi-way-join-optimization.md |
| Prop-F-02-42 | (吞吐优势条件): MultiJoin的吞吐量优势在以下条件下显著： | 命题 | Flink/02-core/multi-way-join-optimization.md |
| Prop-F-02-50 | 检查点频率与恢复时间权衡 | 命题 | Flink/02-core/smart-checkpointing-strategies.md |
| Prop-F-02-51 | 并行度与吞吐量的最优关系 | 命题 | Flink/02-core/smart-checkpointing-strategies.md |
| Prop-F-02-60 | TTL 对 Checkpoint 大小的影响 | 命题 | Flink/02-core/flink-state-ttl-best-practices.md |
| Prop-F-02-70 | State 类型选择定理 | 命题 | Flink/02-core/flink-state-management-complete-guide.md |
| Prop-F-02-71 | Checkpoint 一致性保证 | 命题 | Flink/02-core/flink-state-management-complete-guide.md |
| Prop-F-02-72 | Exactly-Once配置决策矩阵 | 命题 |  |
| Prop-F-03-01 | 函数确定性 (Determinism) | 命题 | Flink/03-api/03.02-table-sql-api/built-in-functions-complete-list.md |
| Prop-F-03-02 | 空值传播 (Null Propagation) | 命题 | Flink/03-api/03.02-table-sql-api/built-in-functions-complete-list.md |
| Prop-F-03-03 | 类型推导规则 | 命题 | Flink/03-api/03.02-table-sql-api/built-in-functions-complete-list.md |
| Prop-F-03-04 | HOP窗口状态膨胀 | 命题 | Flink/03-api/03.02-table-sql-api/flink-sql-window-functions-deep-dive.md |
| Prop-F-03-05 | SESSION窗口状态不确定性 | 命题 | Flink/03-api/03.02-table-sql-api/flink-sql-window-functions-deep-dive.md |
| Prop-F-03-06 | 延迟数据保证 | 命题 | Flink/03-api/03.02-table-sql-api/flink-sql-window-functions-deep-dive.md |
| Prop-F-03-07 | (Python UDF选型准则): 对于给定的计算任务 $Task$，选择Python UDF的充分条件为： | 命题 | Flink/03-api/03.02-table-sql-api/flink-python-udf.md |
| Prop-F-03-100 | JSON 操作语义等价性 | 命题 | Flink/03-api/03.02-table-sql-api/ansi-sql-2023-compliance-guide.md |
| Prop-F-03-101 | MATCH_RECOGNIZE 流处理正确性 | 命题 | Flink/03-api/03.02-table-sql-api/ansi-sql-2023-compliance-guide.md |
| Prop-F-03-15 | 状态边界保证 | 命题 | Flink/03-api/03.02-table-sql-api/flink-process-table-functions.md |
| Prop-F-03-16 | exactly-once 语义传递 | 命题 | Flink/03-api/03.02-table-sql-api/flink-process-table-functions.md |
| Prop-F-03-17 | 输出单调性 | 命题 | Flink/03-api/03.02-table-sql-api/flink-process-table-functions.md |
| Prop-F-03-18 | 状态TTL推导 | 命题 | Flink/03-api/03.02-table-sql-api/flink-process-table-functions.md |
| Prop-F-03-20 | 向量搜索的单调性 | 命题 | Flink/03-api/03.02-table-sql-api/flink-vector-search-rag.md |
| Prop-F-03-21 | 近似搜索的精度-召回权衡 | 命题 | Flink/03-api/03.02-table-sql-api/flink-vector-search-rag.md |
| Prop-F-03-40 | 新鲜度与延迟的权衡关系 | 命题 | Flink/03-api/03.02-table-sql-api/flink-materialized-table-deep-dive.md |
| Prop-F-04-01 | 写入性能边界 | 命题 | Flink/05-ecosystem/05.01-connectors/elasticsearch-connector-complete-guide.md |
| Prop-F-04-02 | 版本冲突处理 | 命题 | Flink/05-ecosystem/05.01-connectors/elasticsearch-connector-complete-guide.md |
| Prop-F-04-06 | 资源利用率演进 | 命题 | Flink/04-runtime/04.01-deployment/evolution/scheduling-evolution.md |
| Prop-F-04-100 | (端到端一致性约束) | 命题 | Flink/05-ecosystem/05.01-connectors/flink-connectors-ecosystem-complete-guide.md |
| Prop-F-04-101 | (连接器并行度扩展性) | 命题 | Flink/05-ecosystem/05.01-connectors/flink-connectors-ecosystem-complete-guide.md |
| Prop-F-04-20 | (端到端Exactly-Once条件) | 命题 | Flink/05-ecosystem/05.01-connectors/04.04-cdc-debezium-integration.md |
| Prop-F-04-200 | 连接器自动发现机制 | 命题 | Flink/05-ecosystem/05.01-connectors/flink-24-connectors-guide.md |
| Prop-F-04-201 | 云原生连接器弹性伸缩性 | 命题 | Flink/05-ecosystem/05.01-connectors/flink-24-connectors-guide.md |
| Prop-F-04-202 | 流批统一连接器语义一致性 | 命题 | Flink/05-ecosystem/05.01-connectors/flink-24-connectors-guide.md |
| Prop-F-04-40 | 无锁读取的正确性 | 命题 | Flink/05-ecosystem/05.01-connectors/flink-cdc-3.0-data-integration.md |
| Prop-F-04-41 | 并行读取的线性加速比 | 命题 | Flink/05-ecosystem/05.01-connectors/flink-cdc-3.0-data-integration.md |
| Prop-F-04-50 | Flink 流式写入的幂等性保证 | 命题 | Flink/05-ecosystem/05.01-connectors/flink-iceberg-integration.md |
| Prop-F-04-51 | CDC 到 Iceberg 的变更合并一致性 | 命题 | Flink/05-ecosystem/05.01-connectors/flink-iceberg-integration.md |
| Prop-F-04-60 | CDC延迟-一致性权衡 | 命题 |  |
| Prop-F-04-61 | 模式演化兼容性边界 | 命题 |  |
| Prop-F-05-01 | (处理语义保证的范围差异) | 命题 | Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-kafka-streams.md |
| Prop-F-05-02 | Hudi Sink的幂等写入保证 | 命题 | Flink/05-ecosystem/05.01-connectors/flink-cdc-3.6.0-guide.md |
| Prop-F-06-01 | (状态后端选型的多目标优化) | 命题 | Flink/09-practices/09.03-performance-tuning/state-backend-selection.md |
| Prop-F-06-10 | (资源利用率与TCO的关系) | 命题 | Flink/09-practices/09.03-performance-tuning/flink-tco-cost-optimization-guide.md |
| Prop-F-06-100 | 向量检索准确率 | 命题 | Flink/06-ai-ml/flip-531-ai-agents-ga-guide.md |
| Prop-F-06-101 | Java异步吞吐量提升 | 命题 | Flink/06-ai-ml/flip-531-ai-agents-ga-guide.md |
| Prop-F-06-20 | 异步推理吞吐量定理 | 命题 | Flink/06-ai-ml/flink-llm-realtime-inference-guide.md |
| Prop-F-06-21 | 状态一致性保证 | 命题 | Flink/06-ai-ml/flink-llm-realtime-inference-guide.md |
| Prop-F-06-300 | 工作流执行延迟边界 | 命题 | Flink/06-ai-ml/flink-agent-workflow-engine.md |
| Prop-F-06-301 | 动态扩展性定理 | 命题 | Flink/06-ai-ml/flink-agent-workflow-engine.md |
| Prop-F-06-302 | 故障恢复时间边界 | 命题 | Flink/06-ai-ml/flink-agent-workflow-engine.md |
| Prop-F-06-40 | (分层存储成本递减) | 命题 | Flink/09-practices/09.03-performance-tuning/stream-processing-cost-optimization.md |
| Prop-F-06-41 | 资源利用率与成本关系 | 命题 |  |
| Prop-F-06-42 | 状态后端成本效率对比 | 命题 |  |
| Prop-F-06-50 | ForSt性能优势 | 命题 |  |
| Prop-F-06-51 | 自适应Join优化 | 命题 |  |
| Prop-F-06-52 | 动态分区裁剪效果 | 命题 |  |
| Prop-F-07-01 | (新鲜度收益递减): 设特征新鲜度为 $f$（分钟），CTR提升 $\Delta_{CTR}$ 满足对数关系： | 命题 | Flink/09-practices/09.01-case-studies/case-ecommerce-realtime-recommendation.md |
| Prop-F-07-02 | 响应状态码规范 | 命题 | Flink/04-runtime/04.02-operations/rest-api-complete-reference.md |
| Prop-F-07-05 | ETA 预测误差收敛性 | 命题 | Flink/09-practices/09.01-case-studies/case-logistics-realtime-tracking.md |
| Prop-F-07-06 | 多租户数据隔离正确性 | 命题 | Flink/09-practices/09.01-case-studies/case-logistics-realtime-tracking.md |
| Prop-F-07-08 | 边缘-云协同延迟边界 | 命题 |  |
| Prop-F-07-09 | 预测性维护置信度 | 命题 |  |
| Prop-F-07-211 | (端到端延迟边界): 社交媒体实时分析的端到端延迟： | 命题 | Flink/09-practices/09.01-case-studies/case-social-media-analytics.md |
| Prop-F-07-221 | (CEP检测精度): 对于欺诈模式 $\mathcal{P}$，CEP检测的精确率和召回率满足： | 命题 | Flink/09-practices/09.01-case-studies/case-fraud-detection-advanced.md |
| Prop-F-07-231 | (VRP启发式算法近似比): 对于容量约束的车辆路径问题， savings算法 + 2-opt优化的近似比： | 命题 | Flink/09-practices/09.01-case-studies/case-supply-chain-optimization.md |
| Prop-F-07-232 | (供应链实时性边界): 从事件发生到决策执行的端到端延迟： | 命题 | Flink/09-practices/09.01-case-studies/case-supply-chain-optimization.md |
| Prop-F-07-241 | (跨域关联精确率): 基于时空窗口的关联检测精确率： | 命题 | Flink/09-practices/09.01-case-studies/case-smart-city-iot.md |
| Prop-F-07-251 | (EWS敏感性): EWS评分对危重患者的敏感性满足： | 命题 | Flink/09-practices/09.01-case-studies/case-healthcare-monitoring.md |
| Prop-F-07-261 | (频率偏差控制): 在需求响应参与下，系统频率偏差满足： | 命题 | Flink/09-practices/09.01-case-studies/case-energy-grid-optimization.md |
| Prop-F-07-71 | (端到端延迟分解): 从用户行为发生到分析结果可见的总延迟 $L_{total}$ 可分解为： | 命题 | Flink/09-practices/09.01-case-studies/case-clickstream-user-behavior-analytics.md |
| Prop-F-08-01 | Q2 KPI 目标命题 (Q2 KPI Target Proposition) | 命题 | Flink/08-roadmap/08.01-flink-24/2026-q2-flink-tasks.md |
| Prop-F-08-02 | AI 推理延迟约束 | 命题 | Flink/08-roadmap/08.01-flink-24/flink-2.1-frontier-tracking.md |
| Prop-F-08-03 | 吞吐量提升分解 | 命题 | Flink/08-roadmap/08.01-flink-24/flink-2.1-frontier-tracking.md |
| Prop-F-08-40 | Agent运行时扩展性 | 命题 | Flink/08-roadmap/08.01-flink-24/flink-2.3-2.4-roadmap.md |
| Prop-F-08-41 | SSL升级兼容性 | 命题 | Flink/08-roadmap/08.01-flink-24/flink-2.3-2.4-roadmap.md |
| Prop-F-08-42 | 社区活跃度增长定律 | 命题 | Flink/08-roadmap/08.01-flink-24/community-dynamics-tracking.md |
| Prop-F-08-43 | 问题处理效率 | 命题 | Flink/08-roadmap/08.01-flink-24/community-dynamics-tracking.md |
| Prop-F-08-50 | Serverless成本优化比例 | 命题 | Flink/08-roadmap/08.01-flink-24/flink-2.5-preview.md |
| Prop-F-08-51 | 流批一体延迟边界 | 命题 | Flink/08-roadmap/08.01-flink-24/flink-2.5-preview.md |
| Prop-F-08-52 | AI推理吞吐量提升 | 命题 | Flink/08-roadmap/08.01-flink-24/flink-2.5-preview.md |
| Prop-F-08-53 | 自适应模式选择最优性 | 命题 | Flink/08-roadmap/08.01-flink-24/flink-25-stream-batch-unification.md |
| Prop-F-08-60 | 统一执行层性能特征 | 命题 | Flink/08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md |
| Prop-F-08-61 | 状态管理可扩展性 | 命题 | Flink/08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md |
| Prop-F-08-62 | 云原生弹性 | 命题 | Flink/08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md |
| Prop-F-08-70 | Serverless Cost Efficiency | 命题 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Prop-F-08-71 | Adaptive Engine Optimization Gain | 命题 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Prop-F-08-72 | Cost-Performance Tradeoff | 命题 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Prop-F-08-73 | Incremental Computation Correctness | 命题 | Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md |
| Prop-F-09-01 | 自动缩放V2收敛性命题 | 命题 | Flink/09-practices/09.04-deployment/flink-kubernetes-operator-1.14-guide.md |
| Prop-F-09-02 | 配置迁移等价性 | 命题 | Flink/09-practices/09.04-deployment/flink-k8s-operator-migration-1.13-to-1.14.md |
| Prop-F-09-03 | Autoscaling V2 收敛速度 | 命题 | Flink/09-practices/09.04-deployment/flink-k8s-operator-new-features-1.14.md |
| Prop-F-09-04 | 异步函数并发上限 | 命题 | Flink/03-api/09-language-foundations/02-python-api.md |
| Prop-F-09-05 | 超时与重试的容错边界 | 命题 | Flink/03-api/09-language-foundations/02-python-api.md |
| Prop-F-09-06 | 异步 I/O 的吞吐量优势 | 命题 | Flink/03-api/09-language-foundations/02-python-api.md |
| Prop-F-09-08 | 类型推断的边界条件 | 命题 | Flink/03-api/09-language-foundations/02.01-java-api-from-scala.md |
| Prop-F-09-09 | 函数式接口的SAM转换 | 命题 | Flink/03-api/09-language-foundations/02.01-java-api-from-scala.md |
| Prop-F-09-20 | 版本性能提升规律 | 命题 | Flink/09-practices/09.02-benchmarking/flink-24-25-benchmark-results.md |
| Prop-F-09-21 | AI Agent性能边界 | 命题 | Flink/09-practices/09.02-benchmarking/flink-24-25-benchmark-results.md |
| Prop-F-09-22 | Serverless成本优化模型 | 命题 | Flink/09-practices/09.02-benchmarking/flink-24-25-benchmark-results.md |
| Prop-F-09-30 | Nexmark查询渐进复杂度定理 | 命题 | Flink/09-practices/09.02-benchmarking/nexmark-2026-benchmark.md |
| Prop-F-09-31 | 引擎性能差异边界 | 命题 | Flink/09-practices/09.02-benchmarking/nexmark-2026-benchmark.md |
| Prop-F-09-32 | 统计显著性要求 | 命题 | Flink/09-practices/09.02-benchmarking/nexmark-2026-benchmark.md |
| Prop-F-09-40 | 成本-性能权衡曲线 | 命题 | Flink/09-practices/09.02-benchmarking/tco-analysis-2026.md |
| Prop-F-09-41 | Serverless成本效益临界点 | 命题 | Flink/09-practices/09.02-benchmarking/tco-analysis-2026.md |
| Prop-F-09-42 | 多云成本差异边界 | 命题 | Flink/09-practices/09.02-benchmarking/tco-analysis-2026.md |
| Prop-F-09-50 | Latency-Throughput Trade-off | 命题 | Flink/03-api/09-language-foundations/02.03-python-async-api.md |
| Prop-F-09-51 | Resource Utilization Efficiency | 命题 | Flink/03-api/09-language-foundations/02.03-python-async-api.md |
| Prop-F-09-52 | 沙箱隔离强度 | 命题 | Flink/03-api/09-language-foundations/flink-25-wasm-udf-ga.md |
| Prop-F-10-01 | 成本与吞吐量的次线性关系 | 命题 | Flink/04-runtime/04.01-deployment/cost-optimization-calculator.md |
| Prop-F-10-02 | 检查点频率的成本拐点 | 命题 | Flink/04-runtime/04.01-deployment/cost-optimization-calculator.md |
| Prop-F-10-03 | Spot 实例的成本节约上界 | 命题 | Flink/04-runtime/04.01-deployment/cost-optimization-calculator.md |
| Prop-F-10-10 | Application vs Session模式边界 | 命题 | Flink/04-runtime/04.01-deployment/kubernetes-deployment-production-guide.md |
| Prop-F-10-11 | 资源配额约束 | 命题 | Flink/04-runtime/04.01-deployment/kubernetes-deployment-production-guide.md |
| Prop-F-10-12 | 存储性能边界 | 命题 | Flink/04-runtime/04.01-deployment/kubernetes-deployment-production-guide.md |
| Prop-F-10-15 | 背压与并行度的单调关系 | 命题 | Flink/04-runtime/04.01-deployment/flink-kubernetes-autoscaler-deep-dive.md |
| Prop-F-10-16 | 目标利用率的最优性 | 命题 | Flink/04-runtime/04.01-deployment/flink-kubernetes-autoscaler-deep-dive.md |
| Prop-F-10-17 | 顶点独立扩缩容的兼容性 | 命题 | Flink/04-runtime/04.01-deployment/flink-kubernetes-autoscaler-deep-dive.md |
| Prop-F-10-40 | 部署模式资源隔离性排序 | 命题 | Flink/04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md |
| Prop-F-10-41 | HA 模式故障恢复时间边界 | 命题 | Flink/04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md |
| Prop-F-10-50 | 滚动升级状态保持 | 命题 | Flink/04-runtime/04.01-deployment/flink-24-deployment-improvements.md |
| Prop-F-10-51 | 状态恢复一致性 | 命题 | Flink/04-runtime/04.01-deployment/serverless-flink-ga-guide.md |
| Prop-F-11-01 | Checkpoint 间隔对性能的影响 | 命题 | Flink/09-practices/09.02-benchmarking/performance-benchmarking-guide.md |
| Prop-F-11-02 | 指标单调性约束 | 命题 | Flink/09-practices/09.02-benchmarking/streaming-benchmarks.md |
| Prop-F-11-03 | 故障恢复时间边界 | 命题 | Flink/09-practices/09.02-benchmarking/streaming-benchmarks.md |
| Prop-F-11-04 | Nexmark查询复杂度递增规律 | 命题 | Flink/09-practices/09.02-benchmarking/performance-benchmark-suite.md |
| Prop-F-11-05 | 并行度扩展效率边界 | 命题 | Flink/09-practices/09.02-benchmarking/performance-benchmark-suite.md |
| Prop-F-11-06 | 状态后端性能权衡 | 命题 | Flink/09-practices/09.02-benchmarking/performance-benchmark-suite.md |
| Prop-F-11-07 | Checkpoint频率与恢复RTO关系 | 命题 | Flink/09-practices/09.02-benchmarking/performance-benchmark-suite.md |
| Prop-F-12-01 | 流式ML的实时性保证 | 命题 | Flink/06-ai-ml/flink-ml-architecture.md |
| Prop-F-12-02 | 迭代计算的收敛性 | 命题 | Flink/06-ai-ml/flink-ml-architecture.md |
| Prop-F-12-03 | MCP 工具选择的准确性 | 命题 | Flink/06-ai-ml/flink-agents-flip-531.md |
| Prop-F-12-04 | A2A 多 Agent 协作的收敛性 | 命题 | Flink/06-ai-ml/flink-agents-flip-531.md |
| Prop-F-12-05 | 渐进发布风险边界 | 命题 | Flink/06-ai-ml/online-learning-production.md |
| Prop-F-12-08 | 特征 freshness 与准确性权衡 | 命题 |  |
| Prop-F-12-100 | Agent状态持久化延迟边界 | 命题 | Flink/06-ai-ml/flink-ai-ml-integration-complete-guide.md |
| Prop-F-12-101 | Agent工具调用幂等性 | 命题 | Flink/06-ai-ml/flink-ai-ml-integration-complete-guide.md |
| Prop-F-12-102 | A2A通信因果一致性 | 命题 | Flink/06-ai-ml/flink-ai-ml-integration-complete-guide.md |
| Prop-F-12-103 | Agent记忆容量边界 | 命题 | Flink/06-ai-ml/flink-ai-ml-integration-complete-guide.md |
| Prop-F-12-104 | LLM流式响应延迟分解 | 命题 | Flink/06-ai-ml/flink-ai-ml-integration-complete-guide.md |
| Prop-F-12-15 | 异步推理吞吐量与延迟权衡 | 命题 |  |
| Prop-F-12-16 | 批处理推理最优批次大小 | 命题 |  |
| Prop-F-12-17 | 特征时效性与模型性能关系 | 命题 |  |
| Prop-F-12-20 | Streaming RAG End-to-End Latency Decomposition | 命题 | Flink/06-ai-ml/rag-streaming-architecture.md |
| Prop-F-12-21 | Flink-MCP 集成的容错性 | 命题 | Flink/06-ai-ml/flink-mcp-protocol-integration.md |
| Prop-F-12-22 | 令牌预算与覆盖率关系 | 命题 |  |
| Prop-F-12-30 | 异步推理吞吐量下界 | 命题 | Flink/06-ai-ml/flink-realtime-ml-inference.md |
| Prop-F-12-31 | 批处理推理的延迟-吞吐权衡 | 命题 | Flink/06-ai-ml/flink-realtime-ml-inference.md |
| Prop-F-12-32 | 特征时效性与模型性能关系 | 命题 | Flink/06-ai-ml/flink-realtime-ml-inference.md |
| Prop-F-12-50 | GPU算子加速比边界 | 命题 | Flink/06-ai-ml/flink-25-gpu-acceleration.md |
| Prop-F-12-51 | 最优批大小定理 | 命题 | Flink/06-ai-ml/flink-25-gpu-acceleration.md |
| Prop-F-12-90 | Agent工具调用幂等性 | 命题 | Flink/06-ai-ml/flink-ai-agents-flip-531.md |
| Prop-F-12-91 | A2A通信因果一致性 | 命题 | Flink/06-ai-ml/flink-ai-agents-flip-531.md |
| Prop-F-13-01 | 安全配置不变式 | 命题 | Flink/09-practices/09.04-security/security-hardening-guide.md |
| Prop-F-13-02 | TEE 安全边界定理 | 命题 | Flink/09-practices/09.04-security/trusted-execution-flink.md |
| Prop-F-13-03 | 数据密封绑定定理 | 命题 | Flink/09-practices/09.04-security/trusted-execution-flink.md |
| Prop-F-13-04 | CPU-GPU 复合 TEE 安全定理 | 命题 | Flink/09-practices/09.04-security/gpu-confidential-computing.md |
| Prop-F-13-05 | GPU TEE 数据机密性定理 | 命题 | Flink/09-practices/09.04-security/gpu-confidential-computing.md |
| Prop-F-13-06 | PCIe/NVLink 加密安全定理 | 命题 | Flink/09-practices/09.04-security/gpu-confidential-computing.md |
| Prop-F-13-07 | 最小权限传递性 | 命题 | Flink/09-practices/09.04-security/flink-security-complete-guide.md |
| Prop-F-13-08 | 纵深防御完备性 | 命题 | Flink/09-practices/09.04-security/flink-security-complete-guide.md |
| Prop-F-13-12 | 跨信任域联邦性质 | 命题 | Flink/09-practices/09.04-security/spiffe-spire-integration-guide.md |
| Prop-F-13-20 | TLS 1.3 前向保密保证 | 命题 | Flink/09-practices/09.04-security/flink-24-security-enhancements.md |
| Prop-F-13-21 | OAuth 2.1 PKCE 安全性 | 命题 | Flink/09-practices/09.04-security/flink-24-security-enhancements.md |
| Prop-F-13-22 | 动态脱敏性能上界 | 命题 | Flink/09-practices/09.04-security/flink-24-security-enhancements.md |
| Prop-F-14-01 | 流处理数据库边界模糊化趋势 | 命题 | Flink/07-rust-native/flink-rust-ecosystem-trends-2026.md |
| Prop-F-14-02 | 增量消费的时间边界一致性 | 命题 | Flink/05-ecosystem/05.02-lakehouse/flink-iceberg-integration.md |
| Prop-F-14-03 | 增量消费的有序性保证 | 命题 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-architecture.md |
| Prop-F-14-04 | 存储成本优化边界 | 命题 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-architecture.md |
| Prop-F-14-05 | Streaming-First架构的成本效益 | 命题 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-deep-dive-2026.md |
| Prop-F-14-06 | S3 Tables的托管优势边界 | 命题 | Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-deep-dive-2026.md |
| Prop-F-14-21 | (状态一致性保证). Gelly Streaming 的状态更新满足： | 命题 | Flink/05-ecosystem/05.04-graph/flink-gelly-streaming-graph-processing.md |
| Prop-F-14-22 | (流式图算法选择决策树). 对于给定图分析问题，选择流式处理的准则： | 命题 | Flink/05-ecosystem/05.04-graph/flink-gelly-streaming-graph-processing.md |
| Prop-F-15-01 | 因果一致性保证 | 命题 | Flink/04-runtime/04.03-observability/distributed-tracing.md |
| Prop-F-15-02 | 上下文传播完备性 | 命题 | Flink/04-runtime/04.03-observability/distributed-tracing.md |
| Prop-F-15-03 | 事件与 Span 的映射关系 | 命题 | Flink/04-runtime/04.03-observability/event-reporting.md |
| Prop-F-15-05 | 时间分布归一性 | 命题 | Flink/04-runtime/04.03-observability/split-level-watermark-metrics.md |
| Prop-F-15-06 | Watermark对齐下的暂停时间单调性 | 命题 | Flink/04-runtime/04.03-observability/split-level-watermark-metrics.md |
| Prop-F-15-07 | 空闲检测的Watermark推进冻结 | 命题 | Flink/04-runtime/04.03-observability/split-level-watermark-metrics.md |
| Prop-F-15-20 | 质量维度独立性 | 命题 | Flink/04-runtime/04.03-observability/realtime-data-quality-monitoring.md |
| Prop-F-15-21 | 质量检查延迟边界 | 命题 | Flink/04-runtime/04.03-observability/realtime-data-quality-monitoring.md |
| Prop-F-15-22 | 误报率与检测覆盖率权衡 | 命题 | Flink/04-runtime/04.03-observability/realtime-data-quality-monitoring.md |
| Prop-F-15-23 | 质量指标聚合的单调性 | 命题 | Flink/04-runtime/04.03-observability/realtime-data-quality-monitoring.md |
| Prop-F-15-30 | 可观测性完备性 | 命题 | Flink/04-runtime/04.03-observability/flink-opentelemetry-observability.md |
| Prop-F-15-31 | OpenTelemetry 信号正交性 | 命题 | Flink/04-runtime/04.03-observability/flink-opentelemetry-observability.md |
| Prop-F-15-32 | 流处理延迟下界 | 命题 | Flink/04-runtime/04.03-observability/flink-opentelemetry-observability.md |
| Prop-F-15-50 | 指标完备性原理 | 命题 | Flink/04-runtime/04.03-observability/flink-observability-complete-guide.md |
| Prop-F-15-51 | 日志-指标-追踪关联性 | 命题 | Flink/04-runtime/04.03-observability/flink-observability-complete-guide.md |
| Prop-F-15-52 | 背压传播链 | 命题 | Flink/04-runtime/04.03-observability/flink-observability-complete-guide.md |
| Prop-F-15-53 | Checkpoint 延迟上界 | 命题 | Flink/04-runtime/04.03-observability/flink-observability-complete-guide.md |
| Cor-F-02-01 | FAQ.md | 推论 |  |
| Cor-F-06-01 | (内存配置黄金比例)：$M_{managed} : M_{network} : M_{heap} \approx 0.4 : 0.1 : 0.5$ | 推论 | Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md |
| Cor-F-06-02 | (并行度配置规则)：$P^ = \min\left(\frac{R_{target}}{R_{single}}, \sqrt{\frac{2}{\beta}}, P_{max\_available}\right)$ | 推论 | Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md |
| Cor-F-06-03 | (检查点间隔下界)：$\Delta t \geq \max\left(T_{cp} \cdot k, \frac{S_{state}}{B_{checkpoint}}\right)$ | 推论 | Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md |
| Cor-F-06-04 | (Nexmark黄金查询选择)： | 推论 | Flink/09-practices/09.03-performance-tuning/06.02-performance-optimization-complete.md |
| Cor-F-06-05 | (并行度配置黄金法则)： | 推论 | Flink/09-practices/09.03-performance-tuning/06.02-performance-optimization-complete.md |
| Cor-F-06-06 | (Checkpoint间隔约束)： | 推论 | Flink/09-practices/09.03-performance-tuning/06.02-performance-optimization-complete.md |
| Cor-F-06-50 | Flink/06-engineering/flink-24-performance-improvements.md | 推论 |  |
| Cor-F-07-05 | 预测性维护误报率边界推论 | 推论 |  |
| Cor-F-12-05 | 特征存储物化视图一致性推论 | 推论 |  |

---

*索引生成于 2026-04-11 21:06:43*
