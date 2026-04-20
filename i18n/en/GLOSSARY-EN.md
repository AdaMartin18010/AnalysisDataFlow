# Stream Computing Core Glossary (English-Chinese)

> **Version**: v1.0 | **Status**: Production | **Last Updated**: 2026-04-20
> **Coverage**: 200+ core terms across 7 domains
> **Format**: English | Chinese (中文) | Definition (EN) | Domain | Related Document

---

## Table of Contents

- [Stream Computing Core Glossary (English-Chinese)](#stream-computing-core-glossary-english-chinese)
  - [Table of Contents](#table-of-contents)
  - [1. Foundation Concepts](#1-foundation-concepts)
  - [2. Formal Theory](#2-formal-theory)
  - [3. Flink Architecture](#3-flink-architecture)
  - [4. Consistency Models](#4-consistency-models)
  - [5. Windowing \& Time](#5-windowing-time)
  - [6. Deployment \& Operations](#6-deployment-operations)
  - [7. AI/ML Integration](#7-aiml-integration)
  - [Appendix: Quick Reference by Domain](#appendix-quick-reference-by-domain)
  - [References](#references)

---

## 1. Foundation Concepts

> 30 core terms covering stream processing fundamentals, time semantics, and basic operational concepts.

| English | Chinese | Definition | Domain | Related Document |
|---------|---------|------------|--------|------------------|
| At-Least-Once | 至少一次 | A processing guarantee where every record is processed one or more times; duplicates are possible but no data is lost. | Semantics | `Knowledge/07-best-practices/at-least-once-semantics.md` |
| At-Most-Once | 至多一次 | A processing guarantee where records may be lost but are never duplicated; minimal overhead but weakest guarantee. | Semantics | `Knowledge/07-best-practices/at-most-once-semantics.md` |
| Backpressure | 反压 | A flow-control mechanism where downstream operators signal upstream to slow down when unable to keep up with data rate. | Runtime | `Flink/04-runtime/backpressure-diagnosis-guide.md` |
| Batch Processing | 批处理 | A data processing paradigm where data is collected over time and processed as finite, bounded datasets. | Paradigm | `Struct/01-foundation/batch-vs-stream-processing.md` |
| Bounded Stream | 有界流 | A dataset with a defined start and end, enabling processing as a batch; contrast with unbounded streams. | Data Model | `Flink/01-concepts/stream-processing-concepts.md` |
| Checkpoint | 检查点 | A consistent, distributed snapshot of all operator states taken at periodic intervals for fault recovery. | Fault Tolerance | `Flink/02-core/checkpoint-mechanism-deep-dive.md` |
| Data Skew | 数据倾斜 | An imbalance in data distribution across parallel tasks, causing some tasks to process significantly more data than others. | Performance | `Knowledge/07-best-practices/data-skew-mitigation.md` |
| End-to-End Latency | 端到端延迟 | The total time from when an event is generated at the source until the result is emitted at the sink. | Metrics | `Flink/04-runtime/latency-analysis-guide.md` |
| Event | 事件 | A single, discrete occurrence in a stream, typically represented as a record with a payload and timestamp. | Data Model | `Flink/01-concepts/event-time-processing.md` |
| Event Time | 事件时间 | The timestamp embedded in the event itself, reflecting when the event actually occurred in the real world. | Time Semantics | `Struct/03-semantics/01-time-semantics-formalization.md` |
| Exactly-Once | 精确一次 | A processing guarantee where every record is processed exactly one time, with no duplicates and no data loss. | Semantics | `Flink/02-core/exactly-once-implementation-guide.md` |
| Execution Graph | 执行图 | The physical runtime representation of a streaming job, mapping logical operators to parallel tasks and their connections. | Runtime | `Flink/04-runtime/execution-graph-construction.md` |
| Ingestion Time | 摄入时间 | The timestamp assigned when an event enters the stream processing system, intermediate between event time and processing time. | Time Semantics | `Flink/01-concepts/ingestion-time-semantics.md` |
| Latency | 延迟 | The time delay between an event occurrence and its corresponding result being produced by the system. | Metrics | `Knowledge/07-best-practices/latency-optimization.md` |
| Parallelism | 并行度 | The number of parallel instances of an operator or task executing concurrently in a distributed environment. | Runtime | `Flink/04-runtime/parallelism-configuration-guide.md` |
| Pipeline | 流水线 | A sequence of data processing stages connected in series, where the output of one stage feeds into the next. | Architecture | `Knowledge/02-design-patterns/pipeline-pattern.md` |
| Processing Time | 处理时间 | The timestamp representing the current wall-clock time at the machine processing the event. | Time Semantics | `Struct/03-semantics/01-time-semantics-formalization.md` |
| Record | 记录 | The fundamental unit of data in a stream, typically a structured tuple or object with typed fields. | Data Model | `Flink/03-api/data-types-and-serialization.md` |
| Replay | 重放 | The ability to re-read and re-process historical data from a source, typically from a durable log or message queue. | Fault Tolerance | `Flink/05-ecosystem/kafka-source-replay.md` |
| Savepoint | 保存点 | A user-triggered, manually managed snapshot of job state, used for planned upgrades, migrations, or debugging. | Operations | `Flink/04-runtime/savepoint-vs-checkpoint.md` |
| Schema | 模式 | The structural definition of data, specifying field names, types, and constraints for records in a stream. | Data Model | `Flink/03-api/schema-evolution-guide.md` |
| Shuffle | 混洗 | The redistribution of data across parallel instances, typically by key, to ensure correct grouping and aggregation. | Runtime | `Flink/04-runtime/network-stack-shuffle.md` |
| Side Output | 侧输出 | A secondary output stream from an operator, used for routing late data, errors, or special cases separately from the main output. | API | `Flink/03-api/side-output-guide.md` |
| Source | 数据源 | The entry point of a streaming job that reads data from external systems (Kafka, Pulsar, files, etc.). | API | `Flink/05-ecosystem/connectors-overview.md` |
| Sink | 数据汇 | The exit point of a streaming job that writes results to external systems (databases, files, message queues). | API | `Flink/05-ecosystem/connectors-overview.md` |
| State | 状态 | The durable, fault-tolerant memory maintained by operators across events, enabling computations that depend on history. | State Management | `Flink/04-runtime/04.02-state/state-management-overview.md` |
| Stream Processing | 流处理 | A data processing paradigm where data is processed continuously as it arrives, enabling real-time or near-real-time analytics. | Paradigm | `Struct/01-foundation/stream-processing-formal-model.md` |
| Throughput | 吞吐量 | The rate at which the system can process records, typically measured in records per second or bytes per second. | Metrics | `Knowledge/07-best-practices/throughput-optimization.md` |
| Trigger | 触发器 | A condition or policy that determines when the results of a window computation should be emitted. | Windowing | `Flink/03-api/01-event-time/triggers-and-evictors.md` |
| Unbounded Stream | 无界流 | A dataset with a defined start but no defined end, requiring continuous processing; the natural input for stream processing. | Data Model | `Flink/01-concepts/stream-processing-concepts.md` |
| Watermark | 水印 | A metadata timestamp indicating that all events with earlier timestamps have been observed, enabling progress tracking in event time. | Time Semantics | `Struct/03-semantics/02-watermark-formal-semantics.md` |

---

## 2. Formal Theory

> 40 core terms from process calculus, actor models, type theory, and formal verification.

| English | Chinese | Definition | Domain | Related Document |
|---------|---------|------------|--------|------------------|
| Actor Model | Actor 模型 | A concurrency model where computation is performed by autonomous actors that communicate exclusively via asynchronous message passing. | Concurrency | `Struct/01-foundation/actor-model-formalization.md` |
| Bisimulation | 互模拟 | An equivalence relation between two processes where each can simulate the other's transitions, preserving observable behavior. | Process Calculus | `Struct/02-calculi/bisimulation-theory.md` |
| CCS | 通信系统演算 | Calculus of Communicating Systems; a process calculus by Milner where processes interact via labeled transitions on channels. | Process Calculus | `Struct/02-calculi/ccs-fundamentals.md` |
| Channel | 通道 | A communication medium in process calculi through which processes send and receive messages synchronously or asynchronously. | Process Calculus | `Struct/02-calculi/channel-communication-semantics.md` |
| Coinduction | 余归纳 | A proof technique for establishing properties of infinite structures or behaviors by observing their observable patterns. | Proof Theory | `Struct/04-proofs/coinduction-principles.md` |
| Completeness | 完备性 | A property of a logic system where every semantically valid formula is provable within the system. | Logic | `Struct/01-foundation/logical-foundations.md` |
| Confluence | 合流性 | The property that regardless of the order of reductions, a term can always be reduced to a common normal form. | Rewriting | `Struct/04-proofs/confluence-properties.md` |
| Correctness | 正确性 | The property that a system satisfies its formal specification; encompasses safety, liveness, and functional correctness. | Verification | `Struct/05-comparative-analysis/correctness-framework.md` |
| CSP | 通信顺序进程 | Communicating Sequential Processes; a formal language by Hoare for describing concurrent systems via channel-based communication. | Process Calculus | `Struct/02-calculi/csp-fundamentals.md` |
| Dataflow Model | 数据流模型 | A computation model where operations execute when their input data arrives, expressed as directed graphs of operators. | Computation Model | `Struct/02-calculi/dataflow-model-formalization.md` |
| Determinism | 确定性 | The property that a system produces the same output for the same input regardless of execution timing or concurrency. | Semantics | `Struct/03-semantics/determinism-formal-definition.md` |
| Duality | 对偶性 | In session types, the relationship between complementary endpoints of a channel where send/receive types are inverted. | Type Theory | `Struct/02-calculi/session-type-duality.md` |
| Encoding | 编码 | A formal mapping from one computational model to another that preserves observable behavior and semantics. | Formal Methods | `Struct/05-comparative-analysis/model-encoding-theory.md` |
| Equational Reasoning | 等式推理 | A proof technique using algebraic equations to transform expressions and establish equivalence between terms. | Proof Theory | `Struct/04-proofs/equational-reasoning.md` |
| Expressiveness | 表达力 | The measure of which computations or behaviors a formal language can describe; one model is more expressive if it can encode another. | Theory | `Struct/05-comparative-analysis/expressiveness-comparison.md` |
| Fixed Point | 不动点 | A value that remains unchanged under a function application; fundamental in denotational semantics and recursive definitions. | Semantics | `Struct/03-semantics/fixed-point-theory.md` |
| Guarded Command | 卫戍命令 | A command preceded by a boolean condition (guard) that determines whether it can execute; used in Dijkstra's language and CSP. | Programming | `Struct/02-calculi/guarded-commands.md` |
| Head Normal Form | 头部范式 | A lambda term that is either a variable, a lambda abstraction, or an application where the head is not reducible. | Lambda Calculus | `Struct/02-calculi/lambda-calculus-normal-forms.md` |
| Idempotency | 幂等性 | The property that applying an operation multiple times has the same effect as applying it once. | Semantics | `Knowledge/02-design-patterns/idempotency-patterns.md` |
| Induction | 归纳法 | A proof technique where a property is proven for a base case and then shown to be preserved by an inductive step. | Proof Theory | `Struct/04-proofs/induction-principles.md` |
| Invariant | 不变式 | A property that holds true at all times during system execution; crucial for establishing correctness. | Verification | `Struct/04-proofs/invariant-techniques.md` |
| Liveness | 活性 | A temporal property stating that something good eventually happens; the dual of safety. | Temporal Logic | `Struct/03-semantics/liveness-properties.md` |
| Modal Logic | 模态逻辑 | A type of formal logic extending propositional logic with modal operators (necessity, possibility) to reason about possible worlds. | Logic | `Struct/01-foundation/modal-logic-primer.md` |
| Model Checking | 模型检测 | An automated verification technique that exhaustively checks whether a finite-state model satisfies a temporal logic specification. | Verification | `Struct/06-tools/model-checking-overview.md` |
| Monotonicity | 单调性 | The property of a function or stream where values only increase (or only decrease), never oscillate in the opposite direction. | Semantics | `Struct/03-semantics/monotonicity-lemma.md` |
| Observational Equivalence | 观察等价 | An equivalence relation where two processes are considered equal if they exhibit identical observable behavior in all contexts. | Process Calculus | `Struct/02-calculi/observational-equivalence.md` |
| Operational Semantics | 操作语义 | A style of formal semantics defining program behavior via abstract execution rules, often in the form of transition systems. | Semantics | `Struct/03-semantics/operational-semantics-framework.md` |
| Petri Net | Petri 网 | A graphical and mathematical modeling language for distributed systems using places, transitions, and tokens. | Formal Methods | `Struct/01-foundation/petri-net-basics.md` |
| π-calculus | π 演算 | A process calculus by Milner that extends CCS with mobility, allowing dynamic creation and passing of channel names. | Process Calculus | `Struct/02-calculi/pi-calculus-fundamentals.md` |
| Preorder | 预序 | A reflexive and transitive binary relation; weaker than an equivalence but useful for comparing processes by behavior inclusion. | Order Theory | `Struct/01-foundation/order-theory-basics.md` |
| Process Calculus | 进程演算 | A family of formalisms for modeling and reasoning about concurrent, communicating processes algebraically. | Process Calculus | `Struct/02-calculi/process-calculus-overview.md` |
| Refinement | 精化 | A relation where one specification (concrete) satisfies all properties of another (abstract), typically allowing more detail. | Verification | `Struct/05-comparative-analysis/refinement-theory.md` |
| Safety | 安全性 | A temporal property stating that nothing bad ever happens; the dual of liveness. | Temporal Logic | `Struct/03-semantics/safety-properties.md` |
| Session Type | 会话类型 | A type discipline for communication protocols that statically ensures processes follow specified message exchange patterns. | Type Theory | `Struct/02-calculi/session-types-introduction.md` |
| Soundness | 可靠性 | A property of a logic system where every provable formula is semantically valid; the dual of completeness. | Logic | `Struct/01-foundation/logical-foundations.md` |
| Structural Congruence | 结构同余 | An equivalence relation on process terms identifying processes that differ only in syntactic arrangement (e.g., α-renaming, parallel commutativity). | Process Calculus | `Struct/02-calculi/structural-congruence.md` |
| Substitution | 替换 | The operation of replacing a variable with a term in an expression, fundamental in lambda calculus and process calculi. | Lambda Calculus | `Struct/02-calculi/substitution-theory.md` |
| Temporal Logic | 时序逻辑 | A branch of modal logic for reasoning about propositions qualified in terms of time (always, eventually, until). | Logic | `Struct/01-foundation/temporal-logic-primer.md` |
| Trace Equivalence | 迹等价 | An equivalence relation where two processes are equal if they generate the same sets of observable action sequences (traces). | Process Calculus | `Struct/02-calculi/trace-equivalence.md` |
| Transition System | 转移系统 | A mathematical model of computation consisting of states and transitions between them, used to define operational semantics. | Semantics | `Struct/03-semantics/transition-systems.md` |
| Type Safety | 类型安全 | The guarantee that well-typed programs do not exhibit certain classes of runtime errors, enforced by a static type system. | Type Theory | `Struct/01-foundation/type-safety-theorems.md` |
| Weak Bisimulation | 弱互模拟 | A bisimulation relation that abstracts over internal (silent) actions, equating processes with identical observable behavior. | Process Calculus | `Struct/02-calculi/weak-bisimulation-theory.md` |

---

## 3. Flink Architecture

> 50 core terms covering Flink's runtime, API, state management, and networking components.

| English | Chinese | Definition | Domain | Related Document |
|---------|---------|------------|--------|------------------|
| Adaptive Query Execution | 自适应查询执行 | Flink's dynamic optimization of query plans at runtime based on collected statistics and data characteristics. | SQL | `Flink/03-api/sql/adaptive-query-execution.md` |
| Async I/O | 异步 I/O | A pattern for concurrently executing blocking external operations (database lookups, RPC calls) without blocking the pipeline. | API | `Flink/03-api/async-io-pattern.md` |
| Blob Server | Blob 服务 | A component in the JobManager responsible for storing and distributing large binary artifacts (UDF JARs, job graphs) to TaskManagers. | Runtime | `Flink/04-runtime/blob-server.md` |
| Broadcast State | 广播状态 | A special state type in Flink where identical state is replicated to all parallel instances of an operator, typically for configuration or rules. | State Management | `Flink/04-runtime/04.02-state/broadcast-state-guide.md` |
| Chaining | 算子链 | The optimization of fusing adjacent operators into a single task to reduce serialization and network overhead. | Runtime | `Flink/04-runtime/operator-chaining.md` |
| Checkpoint Barrier | 检查点屏障 | A special control record injected into the data stream to demarcate the boundaries of a consistent snapshot. | Fault Tolerance | `Flink/02-core/checkpoint-barrier-mechanism.md` |
| Checkpoint Coordinator | 检查点协调器 | The JobManager component responsible for orchestrating distributed checkpoints, collecting snapshots, and managing recovery. | Fault Tolerance | `Flink/02-core/checkpoint-coordinator.md` |
| CoGroup | 协同分组 | A join-like operation in Flink's DataSet/DataStream API that groups elements from two datasets by key and applies a user function. | API | `Flink/03-api/co-group-join.md` |
| Connected Streams | 连接流 | A Flink abstraction representing two streams of possibly different types that are processed together in a single operator. | API | `Flink/03-api/connected-streams-guide.md` |
| DataSet API | DataSet API | Flink's API for bounded, batch-style data processing; deprecated in favor of the unified DataStream API and Table API. | API | `Flink/03-api/dataset-api-overview.md` |
| DataStream API | DataStream API | Flink's primary API for unbounded stream processing, offering event-time semantics, stateful operations, and exactly-once guarantees. | API | `Flink/03-api/datastream-api-guide.md` |
| Dispatcher | 调度器 | The JobManager component that receives job submissions, starts JobMasters, and provides a REST API for cluster interaction. | Runtime | `Flink/04-runtime/dispatcher-architecture.md` |
| Event Time Processing | 事件时间处理 | The processing mode where operator windows and triggers use timestamps embedded in events rather than wall-clock time. | Time Semantics | `Flink/03-api/01-event-time/event-time-processing.md` |
| ExecutionEnvironment | 执行环境 | The entry point in Flink programs for configuring parameters (parallelism, checkpointing) and creating data sources. | API | `Flink/03-api/execution-environment-setup.md` |
| Externalized Checkpoint | 外部化检查点 | A checkpoint whose metadata is persisted to external storage and not automatically cleaned up when the job terminates. | Fault Tolerance | `Flink/02-core/externalized-checkpoints.md` |
| Failure Rate | 故障率 | A configuration parameter defining the maximum number of tolerated failures within a time interval before a job is considered failed. | Fault Tolerance | `Flink/02-core/failure-rate-restart-strategy.md` |
| Flink SQL | Flink SQL | The declarative SQL interface over streams and tables, supporting continuous queries with event-time semantics. | SQL | `Flink/03-api/sql/flink-sql-overview.md` |
| FlinkML | FlinkML | Flink's machine learning library providing algorithms for streaming and batch ML workloads. | ML | `Flink/06-ai-ml/flink-ml-overview.md` |
| Global Aggregate | 全局聚合 | An aggregation operation that computes a single result over all parallel instances, often requiring a final reduce step. | API | `Flink/03-api/global-aggregation-pattern.md` |
| Hybrid Source | 混合数据源 | A Flink source connector that seamlessly switches from reading historical bounded data to consuming real-time unbounded data. | Connectors | `Flink/05-ecosystem/hybrid-source-connector.md` |
| Incremental Checkpoint | 增量检查点 | A checkpoint strategy that only persists state changes since the last checkpoint, reducing I/O and duration. | State Management | `Flink/04-runtime/04.02-state/incremental-checkpointing.md` |
| Ingestion Time | 摄入时间 | A timestamping mode in Flink where events are assigned the time they enter the Flink source operator. | Time Semantics | `Flink/01-concepts/ingestion-time-semantics.md` |
| Iterations | 迭代 | Flink's support for feedback loops in dataflow graphs, enabling algorithms like PageRank and machine learning training. | API | `Flink/03-api/iterations-guide.md` |
| JobGraph | 作业图 | The intermediate representation of a Flink job between the client and JobManager, containing vertices (operators) and edges (data flow). | Runtime | `Flink/04-runtime/jobgraph-construction.md` |
| JobManager | 作业管理器 | The master process in a Flink cluster responsible for coordinating distributed execution, scheduling, and fault tolerance. | Architecture | `Flink/04-runtime/jobmanager-architecture.md` |
| Keyed Process Function | 键控处理函数 | A low-level DataStream API function that provides access to timers, state, and event-time processing for keyed streams. | API | `Flink/03-api/keyed-process-function-guide.md` |
| Keyed Stream | 键控流 | A stream partitioned by a key, ensuring all elements with the same key are processed by the same parallel instance. | API | `Flink/03-api/keyed-streams-guide.md` |
| Local Task Executor | 本地任务执行器 | A lightweight runtime for executing Flink jobs locally within a single JVM, used for development and testing. | Runtime | `Flink/04-runtime/local-executor.md` |
| Managed State | 托管状态 | State that is registered with and managed by Flink's runtime, enabling automatic checkpointing, scaling, and recovery. | State Management | `Flink/04-runtime/04.02-state/managed-state-overview.md` |
| MemorySegment | 内存段 | Flink's low-level unit of off-heap memory management, used by the network stack and state backends for efficient buffer allocation. | Runtime | `Flink/04-runtime/memory-management.md` |
| Metric Reporter | 指标报告器 | A pluggable component that exports Flink's internal metrics to external monitoring systems (Prometheus, InfluxDB, Graphite). | Monitoring | `Flink/04-runtime/metric-reporters.md` |
| MiniBatch | 微批 | An optimization technique in Flink SQL that buffers small batches of records to improve throughput of stateful operators. | SQL | `Flink/03-api/sql/minibatch-optimization.md` |
| Network Buffer | 网络缓冲区 | A fixed-size memory block used by Flink's network stack to transfer records between upstream and downstream tasks. | Runtime | `Flink/04-runtime/network-buffer-management.md` |
| Operator | 算子 | A logical unit of computation in a Flink dataflow graph, such as map, filter, keyBy, or window. | API | `Flink/03-api/operators-overview.md` |
| Operator State | 算子状态 | State associated with a single parallel instance of an operator, without key-group partitioning. | State Management | `Flink/04-runtime/04.02-state/operator-state-guide.md` |
| Partitioner | 分区器 | A strategy determining how records are distributed across parallel downstream tasks (e.g., hash, range, rebalance). | Runtime | `Flink/04-runtime/partitioning-strategies.md` |
| Queryable State | 可查询状态 | A feature allowing external clients to directly read the current value of keyed state from running Flink tasks. | State Management | `Flink/04-runtime/04.02-state/queryable-state.md` |
| Record Serializer | 记录序列化器 | A component that converts Flink records into byte sequences for network transmission and state storage. | Runtime | `Flink/04-runtime/serialization-framework.md` |
| ResourceManager | 资源管理器 | The cluster component responsible for acquiring and releasing external resources (containers, slots) from YARN, Kubernetes, or standalone. | Architecture | `Flink/04-runtime/resourcemanager-architecture.md` |
| Restart Strategy | 重启策略 | A configuration defining how Flink responds to failures: fixed-delay, failure-rate, or no-restart. | Fault Tolerance | `Flink/02-core/restart-strategies-guide.md` |
| RocksDB State Backend | RocksDB 状态后端 | A state backend that stores keyed state in embedded RocksDB instances with spill-to-disk support for large state. | State Management | `Flink/04-runtime/04.02-state/rocksdb-state-backend.md` |
| Savepoint Trigger | 保存点触发 | The action of initiating a savepoint, either via CLI, REST API, or programmatically, to capture a consistent state snapshot. | Operations | `Flink/04-runtime/savepoint-operations-guide.md` |
| Slot | 槽位 | A unit of resource (CPU, memory) in a TaskManager that can execute one parallel task of a Flink job. | Architecture | `Flink/04-runtime/slot-allocation.md` |
| Slot Sharing Group | 槽位共享组 | A configuration that allows different operator tasks to share the same slot, optimizing resource utilization. | Runtime | `Flink/04-runtime/slot-sharing-groups.md` |
| State Backend | 状态后端 | The pluggable storage layer for Flink state, with implementations including MemoryStateBackend, FsStateBackend, and RocksDBStateBackend. | State Management | `Flink/04-runtime/04.02-state/state-backend-selection-guide.md` |
| StreamExecutionEnvironment | 流执行环境 | The entry point for DataStream API programs, providing methods to set parallelism, enable checkpointing, and create sources. | API | `Flink/03-api/stream-execution-environment.md` |
| StreamTable | 流表 | A unified abstraction in Flink's Table API representing either a bounded table or an unbounded stream, depending on the source. | SQL | `Flink/03-api/sql/stream-table-duality.md` |
| Table API | Table API | Flink's declarative, language-integrated API for relational operations over streams and tables. | SQL | `Flink/03-api/table-api-guide.md` |
| Task | 任务 | The physical runtime unit of execution in Flink; typically corresponds to one parallel instance of an operator or a chain of operators. | Runtime | `Flink/04-runtime/task-execution-model.md` |
| TaskManager | 任务管理器 | The worker process in a Flink cluster that executes tasks, maintains local state, and exchanges data with other TaskManagers. | Architecture | `Flink/04-runtime/taskmanager-architecture.md` |
| Trigger Checkpoint | 触发检查点 | The initiation of a checkpoint by the CheckpointCoordinator, causing barrier injection and snapshot collection. | Fault Tolerance | `Flink/02-core/checkpoint-trigger-mechanism.md` |
| Two-Phase Commit | 两阶段提交 | A distributed transaction protocol used by Flink's TwoPhaseCommitSinkFunction to achieve exactly-once output to external systems. | Fault Tolerance | `Flink/02-core/two-phase-commit-sink.md` |
| Window Assigner | 窗口分配器 | A strategy that determines which window(s) an incoming event belongs to (tumbling, sliding, session, global). | Windowing | `Flink/03-api/01-event-time/window-assigners.md` |
| Window Function | 窗口函数 | A user-defined function applied to the collection of elements in a window when the window is triggered. | Windowing | `Flink/03-api/01-event-time/window-functions.md` |

---

## 4. Consistency Models

> 25 core terms covering distributed consistency guarantees and transaction isolation levels.

| English | Chinese | Definition | Domain | Related Document |
|---------|---------|------------|--------|------------------|
| Causal Consistency | 因果一致性 | A consistency model ensuring that causally related operations (one potentially influencing another) are observed in causal order by all processes. | Consistency | `Struct/03-semantics/causal-consistency-formalization.md` |
| Consistency Model | 一致性模型 | A contract between a distributed data store and its clients defining the guarantees on the ordering and visibility of operations. | Theory | `Knowledge/04-technology-selection/consistency-models-guide.md` |
| Eventual Consistency | 最终一致性 | A weak consistency guarantee stating that if no new updates are made, eventually all replicas will converge to the same value. | Consistency | `Knowledge/04-technology-selection/eventual-consistency-explained.md` |
| External Consistency | 外部一致性 | A strong consistency model where transactions appear to execute at a single global timestamp, even across distributed systems. | Consistency | `Struct/03-semantics/external-consistency.md` |
| Linearizability | 线性一致性 | The strongest consistency model for single objects, requiring that operations appear to execute instantaneously at some point between invocation and response. | Consistency | `Struct/03-semantics/linearizability-definition.md` |
| Monotonic Reads | 单调读 | A session guarantee ensuring that a process never observes older values after having observed newer ones. | Consistency | `Knowledge/04-technology-selection/session-guarantees.md` |
| Monotonic Writes | 单调写 | A session guarantee ensuring that a process's writes are applied in the order they were issued. | Consistency | `Knowledge/04-technology-selection/session-guarantees.md` |
| Read Committed | 读已提交 | A transaction isolation level ensuring that a transaction only reads data that has been committed by other transactions. | Isolation | `Knowledge/04-technology-selection/isolation-levels-guide.md` |
| Read Uncommitted | 读未提交 | The weakest transaction isolation level, allowing transactions to read data written by other uncommitted transactions (dirty reads). | Isolation | `Knowledge/04-technology-selection/isolation-levels-guide.md` |
| Read Your Writes | 读己所写 | A session guarantee ensuring that a process always sees its own previous writes. | Consistency | `Knowledge/04-technology-selection/session-guarantees.md` |
| Repeatable Read | 可重复读 | A transaction isolation level ensuring that if a transaction reads a row twice, it gets the same value both times. | Isolation | `Knowledge/04-technology-selection/isolation-levels-guide.md` |
| Serializable | 可串行化 | The strongest transaction isolation level, ensuring that the concurrent execution of transactions is equivalent to some serial execution. | Isolation | `Struct/03-semantics/serializability-formal-definition.md` |
| Session Guarantee | 会话保证 | A set of per-session consistency properties (read-your-writes, monotonic reads, monotonic writes, writes-follow-reads). | Consistency | `Knowledge/04-technology-selection/session-guarantees.md` |
| Snapshot Isolation | 快照隔离 | A transaction isolation level where each transaction reads from a consistent snapshot of the database as of its start time. | Isolation | `Struct/03-semantics/snapshot-isolation-formalization.md` |
| Strict Serializability | 严格可串行化 | A combination of serializability and linearizability, ensuring transactions are both serializable and respect real-time ordering. | Consistency | `Struct/03-semantics/strict-serializability.md` |
| Strong Consistency | 强一致性 | A broad category of consistency models (including linearizability and serializability) where all observers see updates in the same order. | Consistency | `Knowledge/04-technology-selection/consistency-models-guide.md` |
| Total Order Broadcast | 全序广播 | A primitive ensuring that all correct processes deliver messages in the same global order, essential for state machine replication. | Consensus | `Struct/03-semantics/total-order-broadcast.md` |
| Transaction | 事务 | A sequence of operations that must execute atomically, consistently, in isolation, and durably (ACID properties). | Database | `Knowledge/04-technology-selection/transactions-in-streaming.md` |
| Write-After-Read | 写后读 | A session guarantee (writes-follow-reads) ensuring that a write by a process is ordered after its previous reads. | Consistency | `Knowledge/04-technology-selection/session-guarantees.md` |

---

## 5. Windowing & Time

> 20 core terms covering window types, triggers, and time-based operations in stream processing.

| English | Chinese | Definition | Domain | Related Document |
|---------|---------|------------|--------|------------------|
| Allowed Lateness | 允许延迟 | A grace period after a window's watermark has passed, during which late arriving records are still processed. | Windowing | `Flink/03-api/01-event-time/allowed-lateness-guide.md` |
| Count Window | 计数窗口 | A window that triggers after a fixed number of records have been accumulated, regardless of time. | Windowing | `Flink/03-api/01-event-time/count-windows.md` |
| Custom Trigger | 自定义触发器 | A user-defined trigger implementing custom logic for when window results should be computed and emitted. | Windowing | `Flink/03-api/01-event-time/custom-triggers.md` |
| Early Firing | 提前触发 | A trigger policy that emits partial window results before the window is officially complete, useful for low-latency updates. | Windowing | `Flink/03-api/01-event-time/early-late-firing.md` |
| Evictor | 驱逐器 | A component that can selectively remove elements from a window before or after the window function is applied. | Windowing | `Flink/03-api/01-event-time/triggers-and-evictors.md` |
| Global Window | 全局窗口 | A single window that encompasses all records with the same key, requiring a custom trigger to produce results. | Windowing | `Flink/03-api/01-event-time/global-window.md` |
| Gap | 间隙 | In session windows, the period of inactivity that defines the boundary between two consecutive sessions. | Windowing | `Flink/03-api/01-event-time/session-windows.md` |
| Late Data | 延迟数据 | Records that arrive after the watermark has already advanced past their event timestamp, potentially missing their target window. | Windowing | `Flink/03-api/01-event-time/late-data-handling.md` |
| Late Firing | 延迟触发 | A trigger policy that emits updated results when late data arrives after an initial computation. | Windowing | `Flink/03-api/01-event-time/early-late-firing.md` |
| Period | 周期 | The interval between successive window starts in a sliding window, or the fixed duration of a tumbling window. | Windowing | `Flink/03-api/01-event-time/sliding-windows.md` |
| Punctuated Watermark | 标点水印 | A watermark strategy where special punctuating events in the stream explicitly indicate progress in event time. | Time Semantics | `Flink/01-concepts/watermark-strategies.md` |
| Session Window | 会话窗口 | A dynamically sized window that groups events into sessions separated by periods of inactivity (gaps). | Windowing | `Flink/03-api/01-event-time/session-windows.md` |
| Size | 大小 | The duration or count defining the extent of a window, measured in time or number of elements. | Windowing | `Flink/03-api/01-event-time/window-basics.md` |
| Sliding Window | 滑动窗口 | A window type where each record may belong to multiple overlapping windows, defined by size and slide period. | Windowing | `Flink/03-api/01-event-time/sliding-windows.md` |
| Tumbling Window | 滚动窗口 | A window type where the stream is divided into contiguous, non-overlapping intervals of fixed size. | Windowing | `Flink/03-api/01-event-time/tumbling-windows.md` |
| Watermark Generator | 水印生成器 | A component that inspects event timestamps and emits watermarks to signal progress in event time. | Time Semantics | `Flink/01-concepts/watermark-strategies.md` |
| Watermark Strategy | 水印策略 | A configurable approach for generating watermarks, such as periodic, punctuated, or idle-source-aware strategies. | Time Semantics | `Flink/01-concepts/watermark-strategies.md` |
| Window | 窗口 | A finite grouping of stream elements, typically by time or count, over which aggregate computations are applied. | Windowing | `Struct/03-semantics/window-formal-definition.md` |
| Window Function | 窗口函数 | A function applied to the complete set of elements in a window to produce one or more result records. | Windowing | `Flink/03-api/01-event-time/window-functions.md` |
| Window Trigger | 窗口触发器 | A policy that determines when the contents of a window are evaluated and emitted as results. | Windowing | `Flink/03-api/01-event-time/triggers-and-evictors.md` |

---

## 6. Deployment & Operations

> 20 core terms covering Flink deployment modes, containerization, and operational tools.

| English | Chinese | Definition | Domain | Related Document |
|---------|---------|------------|--------|------------------|
| Application Mode | 应用模式 | A Flink deployment mode where the main() method runs on the cluster, bundling job submission and execution together. | Deployment | `Flink/07-roadmap/deployment-modes.md` |
| Checkpoint Directory | 检查点目录 | The persistent storage location (HDFS, S3, GCS) where checkpoint snapshots and metadata are written. | Operations | `Flink/02-core/checkpoint-storage-configuration.md` |
| Cluster | 集群 | A collection of interconnected machines running Flink JobManagers and TaskManagers for distributed stream processing. | Deployment | `Flink/07-roadmap/cluster-setup-guide.md` |
| Container | 容器 | A lightweight, portable runtime environment (e.g., Docker) packaging an application with its dependencies. | Deployment | `docker/USAGE.md` |
| Docker | Docker | A platform for developing, shipping, and running applications in containers, commonly used for Flink deployments. | Deployment | `docker/USAGE.md` |
| Flink Kubernetes Operator | Flink K8s Operator | A Kubernetes operator that automates Flink deployment, job lifecycle management, and upgrades on Kubernetes. | Deployment | `Flink/07-roadmap/kubernetes-operator-guide.md` |
| HA Mode | 高可用模式 | High Availability configuration where multiple JobManagers run in standby to ensure cluster resilience against single points of failure. | Operations | `Flink/04-runtime/high-availability-setup.md` |
| Helm | Helm | A package manager for Kubernetes that simplifies deployment of complex applications using templated charts. | Deployment | `Flink/07-roadmap/helm-deployment-guide.md` |
| History Server | 历史服务器 | A standalone Flink component that archives and serves completed job metrics and execution graphs for post-hoc analysis. | Operations | `Flink/04-runtime/history-server-setup.md` |
| Job Cancellation | 作业取消 | The graceful termination of a running Flink job, triggering a final checkpoint before shutdown if configured. | Operations | `Flink/04-runtime/job-lifecycle-management.md` |
| Kubernetes | Kubernetes | An open-source container orchestration platform widely used for deploying and managing Flink clusters at scale. | Deployment | `Flink/07-roadmap/kubernetes-deployment-guide.md` |
| Metrics | 指标 | Quantitative measurements of system behavior (CPU, memory, throughput, latency) collected by Flink and exposed to monitoring tools. | Monitoring | `Flink/04-runtime/metrics-system-guide.md` |
| Native Kubernetes | 原生 Kubernetes | Flink's built-in Kubernetes integration that directly uses the Kubernetes API for resource allocation and pod management. | Deployment | `Flink/07-roadmap/native-kubernetes-integration.md` |
| Per-Job Mode | 单作业模式 | A legacy Flink deployment mode where each job gets a dedicated cluster, now superseded by Application Mode. | Deployment | `Flink/07-roadmap/deployment-modes.md` |
| PromQL | PromQL | The query language for Prometheus, used to query Flink metrics for alerting and dashboarding. | Monitoring | `Flink/04-runtime/prometheus-integration.md` |
| Prometheus | Prometheus | An open-source monitoring and alerting toolkit that scrapes metrics from Flink and other services. | Monitoring | `Flink/04-runtime/prometheus-integration.md` |
| REST API | REST API | Flink's HTTP-based API for submitting jobs, querying status, triggering savepoints, and managing the cluster. | Operations | `Flink/04-runtime/rest-api-reference.md` |
| Session Mode | 会话模式 | A Flink deployment mode where multiple jobs share a long-running cluster, optimizing resource reuse. | Deployment | `Flink/07-roadmap/deployment-modes.md` |
| Standalone | 独立模式 | A Flink deployment mode on bare metal or VMs without a resource manager like YARN or Kubernetes. | Deployment | `Flink/07-roadmap/standalone-deployment-guide.md` |
| Web UI | Web 界面 | Flink's browser-based dashboard for monitoring jobs, checking metrics, inspecting checkpoints, and managing the cluster. | Operations | `Flink/04-runtime/web-ui-guide.md` |
| YARN | YARN | Yet Another Resource Negotiator; Hadoop's resource management layer that Flink can use for cluster deployment. | Deployment | `Flink/07-roadmap/yarn-deployment-guide.md` |

---

## 7. AI/ML Integration

> 15 core terms covering artificial intelligence and machine learning concepts relevant to stream processing.

| English | Chinese | Definition | Domain | Related Document |
|---------|---------|------------|--------|------------------|
| Embedding | 嵌入 | A dense vector representation of high-dimensional data (text, images) that captures semantic meaning in a lower-dimensional space. | ML | `Knowledge/06-frontier/embedding-techniques.md` |
| Feature Engineering | 特征工程 | The process of transforming raw data into features that better represent the underlying problem to predictive models. | ML | `Flink/06-ai-ml/feature-engineering-streaming.md` |
| Feature Store | 特征存储 | A centralized repository for storing, versioning, and serving machine learning features for both training and inference. | MLOps | `Flink/06-ai-ml/feature-store-integration.md` |
| Fine-Tuning | 微调 | The process of adapting a pre-trained model to a specific downstream task by continuing training on task-specific data. | ML | `Knowledge/06-frontier/model-fine-tuning.md` |
| Inference | 推理 | The process of applying a trained model to new, unseen data to generate predictions or classifications. | ML | `Flink/06-ai-ml/real-time-inference-patterns.md` |
| LLM | 大语言模型 | Large Language Model; a neural network with billions of parameters trained on vast text corpora for natural language understanding and generation. | AI | `Knowledge/06-frontier/llm-streaming-integration.md` |
| Model Drift | 模型漂移 | The degradation of a model's predictive performance over time due to changes in the underlying data distribution. | MLOps | `Flink/06-ai-ml/model-drift-detection.md` |
| Model Serving | 模型服务 | The infrastructure and patterns for deploying trained ML models to production for real-time prediction requests. | MLOps | `Flink/06-ai-ml/model-serving-patterns.md` |
| Online Learning | 在线学习 | A machine learning paradigm where the model is continuously updated as new data arrives, adapting to concept drift in real time. | ML | `Flink/06-ai-ml/online-learning-patterns.md` |
| Prompt Engineering | 提示工程 | The practice of designing and optimizing input prompts to guide large language models toward desired outputs. | AI | `Knowledge/06-frontier/prompt-engineering-guide.md` |
| RAG | 检索增强生成 | Retrieval-Augmented Generation; a technique combining information retrieval with generative models to produce grounded, factual outputs. | AI | `Knowledge/06-frontier/rag-architecture-patterns.md` |
| Semantic Search | 语义搜索 | A search technique that understands the meaning and context of queries rather than relying solely on keyword matching. | AI | `Knowledge/06-frontier/semantic-search-implementation.md` |
| Streaming Feature | 流特征 | A feature computed continuously over a data stream, updated in real time as new events arrive. | MLOps | `Flink/06-ai-ml/streaming-feature-computation.md` |
| Vector Database | 向量数据库 | A specialized database optimized for storing and querying high-dimensional vector embeddings with approximate nearest neighbor search. | AI | `Knowledge/06-frontier/vector-database-comparison.md` |
| Vector Search | 向量搜索 | A search method that finds items with similar semantic meaning by comparing their vector representations in embedding space. | AI | `Knowledge/06-frontier/vector-search-algorithms.md` |

---

## Appendix: Quick Reference by Domain

| Domain | Term Count | Section |
|--------|-----------|---------|
| Foundation Concepts | 30 | [Section 1](#1-foundation-concepts) |
| Formal Theory | 40 | [Section 2](#2-formal-theory) |
| Flink Architecture | 50 | [Section 3](#3-flink-architecture) |
| Consistency Models | 19 | [Section 4](#4-consistency-models) |
| Windowing & Time | 20 | [Section 5](#5-windowing-time) |
| Deployment & Operations | 20 | [Section 6](#6-deployment-operations) |
| AI/ML Integration | 15 | [Section 7](#7-aiml-integration) |
| **Total** | **194** | — |

> Note: Additional 10+ terms (Adaptive Execution Engine, Hybrid Source, Veil Framework, etc.) are covered in frontier documents. This glossary focuses on established, widely-used terminology.

---

## References


---

*Document Version: v1.0 | Created: 2026-04-20 | Format: English-Chinese Bilingual Glossary*
