# 形式化证明索引 (Proof Index)

> **项目**: AnalysisDataFlow — Phase 4 形式化验证
> **位置**: `reconstruction/phase4-verification/`
> **版本**: v4.1
> **更新日期**: 2026-04-13
> **总文件数**: 13 (9 Coq + 4 TLA+)
> **总定理数**: ~220 (Coq + TLA+ 合计)

---

## 目录

- [形式化证明索引 (Proof Index)](#形式化证明索引-proof-index)
  - [目录](#目录)
  - [快速导航](#快速导航)
  - [Coq 证明文件](#coq-证明文件)
    - [1. `coq-proofs/WatermarkAlgebraComplete.v`](#1-coq-proofswatermarkalgebracompletev)
    - [2. `coq-proofs/ExactlyOnceComplete.v`](#2-coq-proofsexactlyoncecompletev)
    - [3. `coq-proofs/ExactlyOnceCoq.v`](#3-coq-proofsexactlyoncecoqv)
    - [4. `coq-proofs/ExactlyOnceSemantics.v`](#4-coq-proofsexactlyoncesemanticsv)
    - [5. `coq-proofs/WatermarkAlgebra.v`](#5-coq-proofswatermarkalgebrav)
    - [6. `Checkpoint.v`](#6-checkpointv)
    - [7. `WatermarkCompleteness.v`](#7-watermarkcompletenessv)
    - [8. `DeterministicProcessing.v`](#8-deterministicprocessingv)
    - [9. `EventLineage.v`](#9-eventlineagev)
  - [TLA+ 规约文件](#tla-规约文件)
    - [10. `StateBackendEquivalenceComplete.tla`](#10-statebackendequivalencecompletetla)
    - [11. `StateBackendTLA.tla`](#11-statebackendtlatla)
    - [12. `ExactlyOnce.tla`](#12-exactlyoncetla)
    - [13. `Checkpoint.tla` / `Checkpoint-fixed.tla`](#13-checkpointtla-checkpoint-fixedtla)
  - [主题交叉引用](#主题交叉引用)
    - [Watermark 主题](#watermark-主题)
    - [Exactly-Once 主题](#exactly-once-主题)
    - [Checkpoint 主题](#checkpoint-主题)
    - [StateBackend 主题](#statebackend-主题)
  - [依赖关系图](#依赖关系图)
    - [Coq 文件依赖](#coq-文件依赖)
    - [TLA+ 文件依赖](#tla-文件依赖)
  - [2026-Q2 扩展覆盖速查](#2026-q2-扩展覆盖速查)
  - [相关报告](#相关报告)

---

## 快速导航

| 你想查看的主题 | 主要文件 | 关键定理 |
|----------------|----------|----------|
| Watermark 单调性与代数 | `coq-proofs/WatermarkAlgebraComplete.v` | `watermark_algebra_completeness` |
| Watermark 延迟边界与窗口触发 | `coq-proofs/WatermarkAlgebraComplete.v` | `window_firing_completeness` |
| Exactly-Once 端到端语义 | `coq-proofs/ExactlyOnceComplete.v` | `end_to_end_exactlyonce_theorem` |
| 2PC 协议正确性 | `coq-proofs/ExactlyOnceComplete.v` | `twopc_atomicity` |
| Source 可重放性 | `coq-proofs/ExactlyOnceComplete.v` | `replay_correctness` |
| Sink 幂等性/事务性 | `coq-proofs/ExactlyOnceComplete.v` | `idempotent_atleast_implies_exactlyonce` |
| 故障恢复语义保持 | `coq-proofs/ExactlyOnceComplete.v` | `complete_recovery_correctness` |
| Checkpoint 一致性 | `Checkpoint.v` | `checkpoint_consistency` |
| 处理确定性 | `DeterministicProcessing.v` | `dataflow_end_to_end_determinism` |
| 事件血缘跟踪 | `EventLineage.v` | `lineage_transitivity_theorem` |
| HashMap ↔ RocksDB 等价性 | `StateBackendEquivalenceComplete.tla` | `HashMapRocksDBEquivalence` |
| ForSt 集成正确性 | `StateBackendEquivalenceComplete.tla` | `HashMapForStEquivalence` |
| 增量 Checkpoint 语义 | `StateBackendEquivalenceComplete.tla` | `IncrementalCheckpointCorrectness` |
| 状态迁移一致性 | `StateBackendEquivalenceComplete.tla` | `StateMigrationConsistency` |

---

## Coq 证明文件

### 1. `coq-proofs/WatermarkAlgebraComplete.v`

**定位**: Watermark 代数完备性完整证明（2026-Q2 核心扩展）
**行数**: 744
**Admitted**: 0
**依赖**: `Coq.Arith.Arith`, `Coq.Arith.Max`, `Coq.Arith.Min`, `Coq.Lists.List`

**章节与核心定理**:

| 章节 | 主题 | 关键定理 |
|------|------|----------|
| Sec 1 | Watermark Monotonicity | `watermark_monotonic_consecutive`, `watermark_meet_monotonic`, `watermark_join_monotonic` |
| Sec 2 | Lateness Bound Analysis | `lateness_bound_acceptance_window`, `watermark_completeness_after_lateness` |
| Sec 3 | Multi-Stream Algebra | `watermark_meet_associative`, `join_distributes_over_meet`, `global_watermark_permutation_invariant` |
| Sec 4 | Window Triggering | `window_firing_completeness`, `watermark_guarantees_completeness`, `cascading_window_firing_order` |
| Summary | 格结构总结 | `watermark_algebra_lattice_summary`, `watermark_event_time_correctness` |

---

### 2. `coq-proofs/ExactlyOnceComplete.v`

**定位**: Exactly-Once 语义完整证明（2026-Q2 核心扩展）
**行数**: 864
**Admitted**: 0
**依赖**: 标准库 (`Arith`, `List`, `Classical`, `Permutation`, `Setoid`)

**章节与核心定理**:

| 章节 | 主题 | 关键定理 |
|------|------|----------|
| Sec 1 | Two-Phase Commit (2PC) | `twopc_coordinator_decision_correct`, `twopc_atomicity`, `twopc_safety_no_split` |
| Sec 2 | Source Replayability | `replay_correctness`, `replay_idempotent`, `monotonic_offset_preserves_replay` |
| Sec 3 | Sink Guarantees | `idempotent_atleast_implies_exactlyonce`, `transaction_atomic_preserves_exactlyonce`, `commit_makes_durable` |
| Sec 4 | Fault Recovery | `complete_recovery_correctness`, `recovery_produces_consistent_state`, `recovery_maintains_progress` |
| Sec 5 | End-to-End Composition | `end_to_end_exactlyonce_theorem` |

---

### 3. `coq-proofs/ExactlyOnceCoq.v`

**定位**: Exactly-Once 主证明脚本（v2.0 基础版）
**行数**: 1246
**Admitted**: 0
**依赖**: 标准库

**核心定理**:

- `exactly_once_guarantee` — 原子提交 + 源重放 + 一致检查点 ⇒ Exactly-Once 输出
- `end_to_end_exactly_once_theorem` — 端到端组合定理
- `source_replay_produces_same_events` — 全序 + 置换 ⇒ 列表相等
- `atomic_commit_no_duplicates` — 原子提交保证输出 ID 无重复
- `twopc_atomic_commit` — 2PC 协调器规范

**备注**: 本文件是 v2.0 阶段的基础证明，内容已被 `ExactlyOnceComplete.v` 以更模块化的方式重新组织并扩展。

---

### 4. `coq-proofs/ExactlyOnceSemantics.v`

**定位**: Exactly-Once 语义增强定义与组合定理
**行数**: 1074
**Admitted**: 3 (`exactly_once_composition`, `strong_exactly_once` 等需要额外系统假设的部分)
**依赖**: `ExactlyOnceCoq.v`, `WatermarkAlgebra.v`

**核心内容**:

- `ReplayableSource` Type Class 及 `KafkaSource` 实例
- `TransactionalSink` 事务状态机 (`TxEmpty`, `TxOngoing`, `TxPrepared`, `TxCommitted`, `TxAborted`)
- `ExactlyOnceConditions` / `exactly_once_complete` — 三条件组合主定理
- `end_to_end_exactly_once` — 端到端定理

**备注**: 3 处 `admit.` 位于需要额外 `DeterministicProcessing` 假设的复杂组合定理中，不影响 2026-Q2 完成度，因为对应内容已在 `ExactlyOnceComplete.v` 中完整证明。

---

### 5. `coq-proofs/WatermarkAlgebra.v`

**定位**: Watermark 代数基础（v2.0 基础版）
**行数**: 363
**Admitted**: 0

**核心定理**:

- `watermark_algebra_completeness` — Watermark 代数完备性
- `watermark_progression_monotonic` — 单调性定理
- `watermark_algebra_summary` — 分配格总结
- 所有格定律（交换律、结合律、吸收律、分配律）

---

### 6. `Checkpoint.v`

**定位**: Flink Checkpoint 一致性的 Coq 形式化
**行数**: 816
**Admitted**: 0

**核心定义**:

- `Message` / `Barrier` / `Event` — 消息类型
- `OperatorState` / `CheckpointSystem` — 算子与系统状态
- `ChannelConsistentCut` / `ConsistentCut` — 一致割集条件

**核心定理**:

- `checkpoint_consistency` — Checkpoint 完成时系统形成一致割集
- `liveness_checkpoint_completion` — Checkpoint 最终完成的活性
- `barrier_fifo_property` — Barrier FIFO 属性
- `flink_checkpoint_implies_chandy_lamport` — Flink Checkpoint 实现 Chandy-Lamport 算法

---

### 7. `WatermarkCompleteness.v`

**定位**: Watermark 完备格与良基性扩展
**行数**: 787
**Admitted**: 0

**核心定理**:

- `watermark_complete_lattice` (Thm-V-01-01) — 任意子集存在 glb/lub
- `watermark_well_foundedness` (Thm-V-01-02) — 无无限严格降链，有限降链长度有界
- `watermark_bounded_complete_poset` (Thm-V-01-03) — 有界完备偏序集
- `monotonic_watermark_convergence` (Thm-V-01-06) — 单调序列收敛

---

### 8. `DeterministicProcessing.v`

**定位**: 流处理确定性的形式化证明
**行数**: 1121
**Admitted**: 0

**核心定义**:

- `DeterministicPure` / `DeterministicStateful` — 纯/有状态处理确定性
- `ReplayEquivalent` / `ReplayConsistent` — 重放等价与一致性
- `FaultTolerantDeterministic` — 容错确定性

**核心定理**:

- `determinism_preservation_composition` (Thm-V-02-01) — map/filter/compose 保持确定性
- `replay_consistency_guarantee` (Thm-V-02-02) — 重放一致性保证
- `exactly_once_implies_determinism` (Thm-V-02-03) — Exactly-Once 蕴含确定性
- `dataflow_end_to_end_determinism` (Thm-V-02-05) — 数据流图端到端确定性

---

### 9. `EventLineage.v`

**定位**: 事件血缘跟踪的形式化证明
**行数**: 850
**Admitted**: 0

**核心定义**:

- `DirectLineage` / `LineageTransitive` — 直接/传递血缘
- `Traceable` / `FullyTraceable` — 可溯源性
- `LineageGraph` / `GraphPath` — 血缘图与路径
- `PersistedLineage` / `RecoveryLineageComplete` — 持久化与恢复完整性

**核心定理**:

- `lineage_transitivity_theorem` (Thm-V-03-01) — 血缘传递性 + 时间戳单调性
- `output_event_traceability` (Thm-V-03-02) — 输出事件可溯源性
- `recovery_lineage_completeness` (Thm-V-03-03) — 恢复后血缘完整性
- `lineage_security_properties` (Thm-V-03-04) — 不可伪造性 + 无环性

---

## TLA+ 规约文件

### 10. `StateBackendEquivalenceComplete.tla`

**定位**: State Backend 语义等价性完整 TLA+ 规范（2026-Q2 核心扩展）
**行数**: 810
**依赖**: `Integers`, `Sequences`, `FiniteSets`, `TLC`

**核心模块**:

| 模块 | 内容 | 关键定义/定理 |
|------|------|---------------|
| HashMapStateBackend | 内存哈希表后端 | `HashMapState` (Def-V-05-01), `HashMapRead`, `HashMapWrite` |
| RocksDBStateBackend | LSM-Tree 后端 | `RocksDBState` (Def-V-05-03), `RocksDBRead`, `RocksDBWrite` |
| ForStStateBackend | 热/温缓存日志后端 | `ForStState` (Def-V-05-05), `ForStRead`, `ForStWrite` |
| IncrementalCheckpoint | 增量检查点 | `DeltaRecord` (Def-V-05-10), `IncrementalCheckpoint`, `ApplyDeltas` |
| StateMigration | 状态迁移 | `MigrationState` (Def-V-05-15), `MigrateState`, `VerifyMigration` |
| Equivalence | 等价关系 | `ObservationalEquivalence` (Def-V-05-17), `SnapshotEquivalence`, `BehavioralEquivalence` |

**核心定理**:

- `HashMapRocksDBEquivalence` (Thm-V-05-01)
- `HashMapForStEquivalence` (Thm-V-05-02)
- `BackendConversionIsomorphism` (Thm-V-05-03)
- `FullCheckpointCorrectness` (Thm-V-05-04)
- `IncrementalCheckpointCorrectness` (Thm-V-05-05)
- `IncrementalChainConsistency` (Thm-V-05-06)
- `StateMigrationConsistency` (Thm-V-05-07)
- `CrossBackendCheckpointCompatibility` (Thm-V-05-08)

**不变式与活性**:

- `SafetyInvariant` — 组合安全不变式（Type + ReadAfterWrite + DeleteRemovesKey + SnapshotConsistency）
- `LivenessProperty` — 组合活性（CheckpointEventuallyCompletes + WriteEventuallySucceeds + MigrationEventuallyCompletes）

---

### 11. `StateBackendTLA.tla`

**定位**: State Backend TLA+ 扩展规范（增量检查点 + 异步快照）
**行数**: 480
**依赖**: `Naturals`, `Sequences`, `FiniteSets`, `TLC`

**核心内容**:

- `DeltaSnapshot` / `IncrementalCheckpointState` — 增量快照与状态
- `AsynchronousSnapshotState` — 异步快照状态
- `ExtendedBackendState` / `WriteWithTracking` — 扩展后端与变更追踪
- `CheckpointStrategy` / `CheckpointCost` / `RecoveryCost` — 成本模型

**核心定理**:

- `IncrementalCheckpointSizeBound` (Thm-V-04-01)
- `IncrementalCheckpointEquivalence` (Thm-V-04-02)
- `IncrementalChainConsistency` (Thm-V-04-03)
- `AsyncSnapshotConsistency` (Thm-V-04-04)
- `AsyncSnapshotNonBlocking` (Thm-V-04-05)
- `AsyncSnapshotRecoveryCorrectness` (Thm-V-04-06)
- `IncrementalCheckpointCostAdvantage` (Thm-V-04-07)
- `CheckpointRecoveryTradeoff` (Thm-V-04-08)
- `RocksDBIncrementalCorrectness` (Thm-V-04-09)

---

### 12. `ExactlyOnce.tla`

**定位**: Flink 端到端 Exactly-Once 语义的 TLA+ 规约
**行数**: 786
**依赖**: `Naturals`, `Sequences`, `FiniteSets`, `TLC`

**核心定义**:

- `SourceState` / `CommittedOffset` — Source 状态与偏移量
- `TransactionState` / `SinkTransaction` — 事务状态机
- `CheckpointMarker` — Checkpoint 标记

**核心不变式**:

- `SourceReplayabilityCondition` (Prop-EO-01)
- `CheckpointConsistencyCondition` (Prop-EO-02)
- `SinkAtomicityCondition` (Prop-EO-03)
- `TwoPhaseCommitCorrectness` (Prop-EO-04)
- `NoDuplicateOutput` (Prop-EO-05)

**核心定理**:

- `EndToEndExactlyOnceGuarantee` (Thm-EO-02) — 安全性: R ∧ C ∧ A ⇒ Exactly-Once
- `TwoPhaseCommitAtomicity` (Thm-EO-03)
- `SourceReplayabilityGuarantee` (Thm-EO-04)
- `CheckpointRecoveryConsistency` (Thm-EO-05)
- `CompositionTheorem` (Thm-EO-07) — Exactly-Once = SourceReplayable ∘ CheckpointConsistent ∘ SinkAtomic

**活性属性**:

- `CheckpointEventuallyCompletes` (Prop-EO-07)
- `TransactionEventuallyDecides` (Prop-EO-08)
- `RecordEventuallyProcessed` (Prop-EO-09)

---

### 13. `Checkpoint.tla` / `Checkpoint-fixed.tla`

**定位**: Flink Checkpoint 协议的 TLA+ 形式化规约
**行数**: 462 / 467
**依赖**: `Naturals`, `Sequences`, `FiniteSets`, `TLC`

**差异说明**: `Checkpoint-fixed.tla` 修复了 `Checkpoint.tla` 中 `Next` 操作符的错误（将合取改为析取），是实际用于模型检查的版本。

**核心定义**:

- `Barrier` / `Message` / `OperatorState` / `Channel`
- `TriggerCheckpoint` / `ProcessDataEvent` / `ReceiveBarrier` / `AlignBarriers` / `PropagateBarrier` / `CompleteCheckpoint`

**核心不变式**:

- `CheckpointProgressMonotonic` (Prop-V-01)
- `ConsistentCutCondition` (Prop-V-02)
- `NoBarrierLoss` (Prop-V-03)
- `CheckpointExactlyOnce` (Prop-V-04)
- `StateSnapshotConsistency` (Prop-V-05)
- `BarrierAlignmentCompleteness` (Prop-V-06)
- `ChannelFIFO` (Prop-V-07)

**核心定理**:

- `Safety` (Thm-V-01) — Spec ⇒ □SafetyInvariant
- `Liveness` (Thm-V-02) — Spec ⇒ CheckpointEventuallyCompletes
- `ConsistentCutGuarantee` (Thm-V-03) — Spec ⇒ □ConsistentCutCondition

---

## 主题交叉引用

### Watermark 主题

```
WatermarkAlgebra.v (基础格定义)
    └──> WatermarkCompleteness.v (完备格 + 良基性)
            └──> WatermarkAlgebraComplete.v (2026-Q2 扩展：单调性/延迟/多流/窗口)
```

### Exactly-Once 主题

```
ExactlyOnceCoq.v (基础定义与主定理)
    ├──> ExactlyOnceSemantics.v (Type Class 语义增强)
    ├──> DeterministicProcessing.v (处理确定性)
    ├──> EventLineage.v (事件血缘)
    └──> ExactlyOnceComplete.v (2026-Q2 扩展：2PC/源/_sink/恢复)
            └──> ExactlyOnce.tla (TLA+ 规约与活性验证)
```

### Checkpoint 主题

```
Checkpoint.v (Coq 一致割集证明)
    └──> Checkpoint.tla / Checkpoint-fixed.tla (TLA+ 分布式协议规约)
            └──> ExactlyOnce.tla (端到端集成)
```

### StateBackend 主题

```
StateBackendTLA.tla (增量检查点 + 异步快照扩展)
    └──> StateBackendEquivalenceComplete.tla (2026-Q2 扩展：等价性/迁移/增量)
```

---

## 依赖关系图

### Coq 文件依赖

```
ExactlyOnceCoq.v
    ├──> WatermarkAlgebra.v (timestamp, order)
    ├──> WatermarkCompleteness.v (lattice properties)
    └──> EventLineage.v (lineage tracking)

ExactlyOnceSemantics.v
    ├──> ExactlyOnceCoq.v
    └──> WatermarkAlgebra.v

ExactlyOnceComplete.v
    └──> (自包含，依赖标准库)

DeterministicProcessing.v
    ├──> ExactlyOnceCoq.v (event definitions)
    └──> EventLineage.v (lineage)

EventLineage.v
    └──> WatermarkCompleteness.v (timestamp)

Checkpoint.v
    └──> (自包含，依赖标准库)

WatermarkAlgebraComplete.v
    └──> WatermarkAlgebra.v (基础定义)
```

### TLA+ 文件依赖

```
StateBackendEquivalenceComplete.tla
    ├──> Integers, Sequences, FiniteSets, TLC
    └──> (自包含模块)

StateBackendTLA.tla
    ├──> Naturals, Sequences, FiniteSets, TLC
    └──> EXTENDS StateBackendEquivalence (概念依赖)

ExactlyOnce.tla
    └──> Naturals, Sequences, FiniteSets, TLC

Checkpoint-fixed.tla
    └──> Naturals, Sequences, FiniteSets, TLC
```

---

## 2026-Q2 扩展覆盖速查

| 扩展要求 | 主文件 | 关键定理 |
|----------|--------|----------|
| Watermark 单调性定理 | `WatermarkAlgebraComplete.v` | `watermark_monotonic_consecutive`, `watermark_meet_monotonic`, `watermark_join_monotonic` |
| 延迟边界分析 | `WatermarkAlgebraComplete.v` | `lateness_bound_acceptance_window`, `watermark_completeness_after_lateness` |
| 多流 Watermark 合并代数性质 | `WatermarkAlgebraComplete.v` | `watermark_meet_associative`, `meet_distributes_over_join`, `global_watermark_permutation_invariant` |
| Watermark 与窗口触发关系 | `WatermarkAlgebraComplete.v` | `window_firing_completeness`, `watermark_guarantees_completeness` |
| 2PC 协议正确性 | `ExactlyOnceComplete.v` | `twopc_atomicity`, `twopc_safety_no_split` |
| Source 可重放性 | `ExactlyOnceComplete.v` | `replay_correctness`, `replay_idempotent` |
| Sink 幂等性/事务性 | `ExactlyOnceComplete.v` | `idempotent_atleast_implies_exactlyonce`, `transaction_atomic_preserves_exactlyonce` |
| 故障恢复语义保持 | `ExactlyOnceComplete.v` | `complete_recovery_correctness`, `recovery_produces_consistent_state` |
| HashMap vs RocksDB 等价性 | `StateBackendEquivalenceComplete.tla` | `HashMapRocksDBEquivalence` (Thm-V-05-01) |
| ForSt 集成正确性 | `StateBackendEquivalenceComplete.tla` | `HashMapForStEquivalence` (Thm-V-05-02) |
| 增量 Checkpoint 语义等价性 | `StateBackendEquivalenceComplete.tla` | `IncrementalCheckpointCorrectness` (Thm-V-05-05) |
| 状态迁移一致性 | `StateBackendEquivalenceComplete.tla` | `StateMigrationConsistency` (Thm-V-05-07) |

---

## 相关报告

- [FORMAL-PROOF-COMPLETION-REPORT-v4.1.md](./FORMAL-PROOF-COMPLETION-REPORT-v4.1.md) — 2026-Q2 扩展审计与完成报告
- [COQ-COMPILATION-REPORT.md](./COQ-COMPILATION-REPORT.md) — Coq 编译验证报告 (v2.0)
- [TLA-MODEL-CHECK-REPORT.md](./TLA-MODEL-CHECK-REPORT.md) — TLA+ 模型检查报告 (v2.0)
- [FINAL-VERIFICATION-REPORT.md](./FINAL-VERIFICATION-REPORT.md) — 综合验证报告 (v2.0)

---

*索引维护: 当新增或修改形式化证明文件时，请务必同步更新本索引。*
