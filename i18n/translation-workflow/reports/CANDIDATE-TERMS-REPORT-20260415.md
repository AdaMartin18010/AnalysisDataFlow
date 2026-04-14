# Candidate Term Expansion Report

**Generated**: 2026-04-15
**Existing Terms**: 60
**Candidate Additions**: 52

## Candidate Terms (Not Yet in Terminology Database)

| # | Chinese Term | English Term | Category | Definition |
|---|--------------|--------------|----------|------------|
| 1 | 统一流理论 | Unified Streaming Theory | 形式化方法 | Unified batch and stream processing theoretical model |
| 2 | 进程演算基础 | Foundations of Process Calculus | 形式化方法 | Basic concepts of CCS, CSP, and π-calculus |
| 3 | 双模拟等价 | Bisimulation Equivalence | 形式化方法 | Strongest form of process equivalence |
| 4 | 对偶性 | Duality | 形式化方法 | Complementary relationship between session types |
| 5 | 通信兼容性 | Communication Compatibility | 形式化方法 | Guarantee that dual session types can communicate without deadlock |
| 6 | 编码存在性 | Encoding Existence | 形式化方法 | Whether one calculus can be encoded into another preserving semantics |
| 7 | 图灵完备性 | Turing Completeness | 形式化方法 | Ability of a system to simulate any Turing machine |
| 8 | 可判定性 | Decidability | 形式化方法 | Whether a property can be algorithmically decided |
| 9 | 发散语义 | Divergence Semantics | 形式化方法 | Behavioral semantics considering infinite internal computation |
| 10 | 向后兼容 | Backward Compatibility | 形式化方法 | Ability to work with older versions or models |
| 11 | 向前兼容 | Forward Compatibility | 形式化方法 | Ability to work with future versions or models |
| 12 | 到达曲线 | Arrival Curve | 形式化方法 | Network calculus concept bounding traffic arrival patterns |
| 13 | 二进制会话类型 | Binary Session Types | 形式化方法 | Session types between exactly two participants |
| 14 | 进程组合层次结构 | Process Composition Hierarchy | 形式化方法 | Hierarchical structure of process combinators |
| 15 | 内部选择 | Internal Choice | 形式化方法 | Process selects one of several branches autonomously |
| 16 | 外部选择 | External Choice | 形式化方法 | Process offers several branches to the environment |
| 17 | 流数据库 | Stream Database | 基础概念 | Database optimized for continuous stream queries |
| 18 | 物化视图 | Materialized View | 基础概念 | Pre-computed view stored for fast query access |
| 19 | 增量维护 | Incremental Maintenance | 基础概念 | Updating materialized views incrementally |
| 20 | 模型形式化 | Model Formalization | 形式化方法 | Process of giving precise mathematical meaning to a model |
| 21 | 定义动机 | Definition Motivation | 形式化方法 | Rationale behind a formal definition |
| 22 | 证明概要 | Proof Sketch | 形式化方法 | High-level outline of a formal proof |
| 23 | 由归纳假设 | By Induction Hypothesis | 形式化方法 | Standard proof step in inductive arguments |
| 24 | 大状态 | Large State | 状态管理 | State size exceeding memory capacity |
| 25 | 小状态 | Small State | 状态管理 | State size fitting in memory |
| 26 | 状态大小 | State Size | 状态管理 | Total size of operator state |
| 27 | 自适应检查点间隔 | Adaptive Checkpoint Interval | 容错 | Dynamically adjusting checkpoint frequency based on workload |
| 28 | 快照流程 | Snapshot Flow | 容错 | Procedure for taking a distributed consistent snapshot |
| 29 | 恢复时间 | Recovery Time | 容错 | Time required to restore from a checkpoint or savepoint |
| 30 | 一致性保证 | Consistency Guarantee | 一致性语义 | Promise that the system maintains a specific consistency level |
| 31 | 端到端 | End-to-End | 基础概念 | Spanning the entire data pipeline from source to sink |
| 32 | 事务性 | Transactional | 容错 | Supporting atomic commit semantics across systems |
| 33 | 低延迟 | Low Latency | 性能优化 | Minimal delay between event occurrence and processing result |
| 34 | 吞吐量 | Throughput | 性能优化 | Rate at which the system processes records |
| 35 | 访问延迟 | Access Latency | 性能优化 | Time to read or write state data |
| 36 | 存储成本 | Storage Cost | 性能优化 | Resource cost of persisting state and checkpoints |
| 37 | 堆内存 | Heap Memory | 性能优化 | JVM heap space allocated to Flink processes |
| 38 | 本地磁盘 | Local Disk | 性能优化 | Physical disk storage on the TaskManager node |
| 39 | 本地缓存 | Local Cache | 性能优化 | In-memory or on-disk cache for fast repeated access |
| 40 | 协调器 | Coordinator | 架构组件 | Component responsible for orchestrating distributed operations |
| 41 | 源码验证 | Source Code Verification | 工具 | Confirming theoretical properties against actual implementation |
| 42 | 源码位置 | Source Location | 工具 | Reference to specific files and lines in the Flink codebase |
| 43 | 源码深度分析 | In-Depth Source Analysis | 工具 | Detailed examination of Flink internal implementation |
| 44 | 源码实现 | Source Implementation | 工具 | Concrete code realization of an algorithm or mechanism |
| 45 | 配置参数 | Configuration Parameter | 部署 | Tunable setting affecting system behavior |
| 46 | 配置示例 | Configuration Example | 部署 | Sample configuration snippet |
| 47 | 适用场景 | Applicable Scenario | 业务应用 | Situation where a technology or pattern is well-suited |
| 48 | 完整示例 | Complete Example | 工程实践 | End-to-end runnable code or configuration demonstration |
| 49 | 解决方案 | Solution | 工程实践 | Approach to solving a specific engineering problem |
| 50 | 工作流程 | Workflow | 工程实践 | Sequence of steps in a process or pipeline |
| 51 | 分钟级 | Minute-Level | 性能优化 | Granularity or latency measured in minutes |
| 52 | 默认值 | Default Value | 配置 | Value used when no explicit setting is provided |

## Recommendations

1. **Priority 1**: Add all 52 candidates to core-terms.json and Flink-terms.json in the next batch.
2. **Priority 2**: Validate English translations against Apache Flink official docs for Flink-specific terms.
3. **Priority 3**: Update quality-checker.py to enforce these new terms in A/B layer documents.
