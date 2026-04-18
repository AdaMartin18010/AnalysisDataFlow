# 外部链接修复报告 v4.2

**生成时间**: 2026-04-13 18:09:42

## 修复统计

| 指标 | 数值 |
|------|------|
| 检测到的失效链接总数 | 2482 |
| 已修复链接 | 746 |
| 无法修复 (目标不存在) | 1333 |
| 误报 (目标实际存在) | 400 |
| 修改的文件数 | 182 |

## 修复详情 (前 100 条)

- `BENCHMARK-REPORT.md` 第675行
  - 旧: `[Flink/11-benchmarking/streaming-benchmarks.md](./Flink/11-benchmarking/streaming-benchmarks.md)`
  - 新: `[Flink/11-benchmarking/streaming-benchmarks.md](Flink/09-practices/09.02-benchmarking/streaming-benchmarks.md)`

- `BROKEN-LINK-FIX-REPORT.md` 第31行
  - 旧: `[FLINK-24-25-30-COMPLETION-REPORT.md](./FLINK-24-25-30-COMPLETION-REPORT.md)`
  - 新: `[FLINK-24-25-30-COMPLETION-REPORT.md](archive/completion-reports/FLINK-24-25-30-COMPLETION-REPORT.md)`

- `BROKEN-LINK-FIX-REPORT.md` 第81行
  - 旧: `[Flink性能调优指南](./Flink/06-engineering/performance-tuning-guide.md)`
  - 新: `[Flink性能调优指南](Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md)`

- `BROKEN-LINK-FIX-REPORT.md` 第93行
  - 旧: `[Flink/06-engineering/performance-tuning-guide.md](./Flink/06-engineering/performance-tuning-guide.md)`
  - 新: `[Flink/06-engineering/performance-tuning-guide.md](Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md)`

- `CASE-STUDIES.md` 第19行
  - 旧: `[Flink/07-case-studies/](./Flink/07-case-studies/case-realtime-analytics.md)`
  - 新: `[Flink/07-case-studies/](Flink/09-practices/09.01-case-studies/case-realtime-analytics.md)`

- `CHANGELOG.md` 第190行
  - 旧: `[FLINK-24-25-30-COMPLETION-REPORT.md](FLINK-24-25-30-COMPLETION-REPORT.md)`
  - 新: `[FLINK-24-25-30-COMPLETION-REPORT.md](archive/completion-reports/FLINK-24-25-30-COMPLETION-REPORT.md)`

- `cross-ref-error-analysis.md` 第54行
  - 旧: `[Flink核心机制](../../Flink/02-core/checkpoint-mechanism-deep-dive.md)`
  - 新: `[Flink核心机制](Flink/02-core/checkpoint-mechanism-deep-dive.md)`

- `cross-ref-error-analysis.md` 第92行
  - 旧: `[自适应执行V2](../08-roadmap/08.01-flink-24/flink-2.4-tracking.md)`
  - 新: `[自适应执行V2](Flink/08-roadmap/08.01-flink-24/flink-2.4-tracking.md)`

- `FLINK_REVISION_REPORT.md` 第114行
  - 旧: `[02-core/checkpoint-mechanism-deep-dive.md](02-core/checkpoint-mechanism-deep-dive.md)`
  - 新: `[02-core/checkpoint-mechanism-deep-dive.md](Flink/02-core/checkpoint-mechanism-deep-dive.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第1785行
  - 旧: `[Def-F-02-04](../../02-core/time-semantics-and-watermark.md)`
  - 新: `[Def-F-02-04](Flink/02-core/time-semantics-and-watermark.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第1810行
  - 旧: `[Def-F-02-05](../../02-core/time-semantics-and-watermark.md)`
  - 新: `[Def-F-02-05](Flink/02-core/time-semantics-and-watermark.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第1847行
  - 旧: `[Def-F-02-06](../../02-core/time-semantics-and-watermark.md)`
  - 新: `[Def-F-02-06](Flink/02-core/time-semantics-and-watermark.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第6924行
  - 旧: `[Def-K-06-12](../06-frontier/streaming-databases.md)`
  - 新: `[Def-K-06-12](Knowledge/06-frontier/streaming-databases.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第7955行
  - 旧: `[Def-S-03-01](../../Struct/01-foundation/01.03-actor-model-formalization.md)`
  - 新: `[Def-S-03-01](USTM-F-Reconstruction/archive/original-struct/01-foundation/01.03-actor-model-formalization.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第8034行
  - 旧: `[Def-S-04-01 Dataflow](./01-foundation/01.04-dataflow-model-formalization.md)`
  - 新: `[Def-S-04-01 Dataflow](USTM-F-Reconstruction/archive/original-struct/01-foundation/01.04-dataflow-model-formalization.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第8060行
  - 旧: `[01.04-dataflow-model...`
- 文件: `Struct\02-properties\02.03-watermark-monotonicity.md` (第224行)
  上下文: `我们采用**结构归纳法**（structural induction）对 Dataflow 图 $\mathcal{G}$ 的拓扑排序进行证明。设 $v_1, v_2, \ldots, v_{|V|}...`
- 文件: `Knowledge\01-concept-atlas\concurrency-paradigms-matrix.md` (第532行)
  上下文: `3. **水平扩展**：Dataflow 的并行度函数 $P: V \to \mathbb{N}^+$（Def-S-04-01）支持根据数据量动态调整并行度，实现弹性扩展。...`
- 文件: `Knowledge\02-design-patterns\pattern-stateful-computation.md` (第321行)
  上下文: `| **Def-S-04-01** | Dataflow 图 (DAG) | Struct/01.04 | 状态算子作为带状态顶点 ⟨V, E, P, Σ, 𝕋⟩ |...`
- 文件: `Knowledge\05-mapping-guides\struct-to-flink-mapping.md` (第62行)
  上下文: `- $f \in \mathcal{F}$ 为形式化概念（如 Def-S-04-01 的 Dataflow 图）...`
- 文件: `Knowledge\05-mapping-guides\struct-to-flink-mapping.md` (第70行)
  上下文: `| **直接映射** | $\mathcal{M}_{direct}(f) = i$ | 理论概念直接对应代码类/方法 | Def-S-04-01 $\to$`DataStream`|...`
- 文件: `Knowledge\05-mapping-guides\struct-to-flink-mapping.md` (第187行)
  上下文: `**形式化定义** ([Def-S-04-01](../../Struct/01-foundation/01.04-dataflow-model-formalization.md)`
  - 新: `[01.04-dataflow-model...`
- 文件: `Struct\02-properties\02.03-watermark-monotonicity.md` (第224行)
  上下文: `我们采用**结构归纳法**（structural induction）对 Dataflow 图 $\mathcal{G}$ 的拓扑排序进行证明。设 $v_1, v_2, \ldots, v_{|V|}...`
- 文件: `Knowledge\01-concept-atlas\concurrency-paradigms-matrix.md` (第532行)
  上下文: `3. **水平扩展**：Dataflow 的并行度函数 $P: V \to \mathbb{N}^+$（Def-S-04-01）支持根据数据量动态调整并行度，实现弹性扩展。...`
- 文件: `Knowledge\02-design-patterns\pattern-stateful-computation.md` (第321行)
  上下文: `| **Def-S-04-01** | Dataflow 图 (DAG) | Struct/01.04 | 状态算子作为带状态顶点 ⟨V, E, P, Σ, 𝕋⟩ |...`
- 文件: `Knowledge\05-mapping-guides\struct-to-flink-mapping.md` (第62行)
  上下文: `- $f \in \mathcal{F}$ 为形式化概念（如 Def-S-04-01 的 Dataflow 图）...`
- 文件: `Knowledge\05-mapping-guides\struct-to-flink-mapping.md` (第70行)
  上下文: `| **直接映射** | $\mathcal{M}_{direct}(f) = i$ | 理论概念直接对应代码类/方法 | Def-S-04-01 $\to$`DataStream`|...`
- 文件: `Knowledge\05-mapping-guides\struct-to-flink-mapping.md` (第187行)
  上下文: `**形式化定义** ([Def-S-04-01](USTM-F-Reconstruction/archive/original-struct/01-foundation/01.04-dataflow-model-formalization.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第8082行
  - 旧: `[Dataflow 模型形式化](../../../../Struct/01-foundation/01.04-dataflow-model-formalization.md)`
  - 新: `[Dataflow 模型形式化](USTM-F-Reconstruction/archive/original-struct/01-foundation/01.04-dataflow-model-formalization.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第8103行
  - 旧: `[Def-S-04-02](../01-foundation/01.04-dataflow-model-formalization.md#def-s-04-02-算子语义)`
  - 新: `[Def-S-04-02](USTM-F-Reconstruction/archive/original-struct/01-foundation/01.04-dataflow-model-formalization.md#def-s-04-02-算子语义)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第8185行
  - 旧: `[Def-S-04-04](../../Struct/01-foundation/01.04-dataflow-model-formalization.md)`
  - 新: `[Def-S-04-04](USTM-F-Reconstruction/archive/original-struct/01-foundation/01.04-dataflow-model-formalization.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第8234行
  - 旧: `[Def-S-04-05](../../Struct/01-foundation/01.04-dataflow-model-formalization.md)`
  - 新: `[Def-S-04-05](USTM-F-Reconstruction/archive/original-struct/01-foundation/01.04-dataflow-model-formalization.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第8238行
  - 旧: `[Def-S-04-05](../../../Struct/01-foundation/01.04-dataflow-model-formalization.md)`
  - 新: `[Def-S-04-05](USTM-F-Reconstruction/archive/original-struct/01-foundation/01.04-dataflow-model-formalization.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第8245行
  - 旧: `[Def-S-05-01 CSP](./01-foundation/01.05-csp-formalization.md)`
  - 新: `[Def-S-05-01 CSP](USTM-F-Reconstruction/archive/original-struct/01-foundation/01.05-csp-formalization.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第8302行
  - 旧: `[Def-S-06-01 Petri Net](./01-foundation/01.06-petri-net-formalization.md)`
  - 新: `[Def-S-06-01 Petri Net](USTM-F-Reconstruction/archive/original-struct/01-foundation/01.06-petri-net-formalization.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第8429行
  - 旧: `[Def-S-07-01 确定性](./02-properties/02.01-determinism-in-streaming.md#def-s-07-01-确定性流处理系统)`
  - 新: `[Def-S-07-01 确定性](USTM-F-Reconstruction/archive/original-struct/02-properties/02.01-determinism-in-streaming.md#def-s-07-01-确定性流处理系统)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第8552行
  - 旧: `[Def-S-08-01 一致性层级](./02-properties/02.02-consistency-hierarchy.md)`
  - 新: `[Def-S-08-01 一致性层级](USTM-F-Reconstruction/archive/original-struct/02-properties/02.02-consistency-hierarchy.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第8552行
  - 旧: `[pattern-event-time-processi...`
- 文件: `Struct\02-properties\02.02-consistency-hierarchy.md` (第57行)
  上下文: `### Def-S-08-01 (Dataflow 执行轨迹)...`
- 文件: `Struct\06-frontier\06.01-open-problems-streaming-verification.md` (第275行)
  上下文: `| **At-Most-Once** | P-完全 | 幂等性验证 | [Def-S-08-01](../02-properties/02.02-consistency-hierarchy.md)`
  - 新: `[pattern-event-time-processi...`
- 文件: `Struct\02-properties\02.02-consistency-hierarchy.md` (第57行)
  上下文: `### Def-S-08-01 (Dataflow 执行轨迹)...`
- 文件: `Struct\06-frontier\06.01-open-problems-streaming-verification.md` (第275行)
  上下文: `| **At-Most-Once** | P-完全 | 幂等性验证 | [Def-S-08-01](USTM-F-Reconstruction/archive/original-struct/02-properties/02.02-consistency-hierarchy.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第8693行
  - 旧: `[Def-S-09-01 活性/安全性](./02-properties/02.04-liveness-and-safety.md)`
  - 新: `[Def-S-09-01 活性/安全性](USTM-F-Reconstruction/archive/original-struct/02-properties/02.04-liveness-and-safety.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第8724行
  - 旧: `[02.03-watermark-monotonicity.md](../02-properties/02.03-watermark-monotonicity.md)`
  - 新: `[02.03-watermark-monotonicity.md](USTM-F-Reconstruction/archive/original-struct/02-properties/02.03-watermark-monotonicity.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第8900行
  - 旧: `[Def-S-15-01](../03-relationships/03.04-bisimulation-equivalences.md)`
  - 新: `[Def-S-15-01](USTM-F-Reconstruction/archive/original-struct/03-relationships/03.04-bisimulation-equivalences.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第8917行
  - 旧: `[Def-S-15-02](../03-relationships/03.04-bisimulation-equivalences.md)`
  - 新: `[Def-S-15-02](USTM-F-Reconstruction/archive/original-struct/03-relationships/03.04-bisimulation-equivalences.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第9033行
  - 旧: `[Def-S-17-01](../../Struct/04-proofs/04.01-flink-checkpoint-correctness.md)`
  - 新: `[Def-S-17-01](USTM-F-Reconstruction/archive/original-struct/04-proofs/04.01-flink-checkpoint-correctness.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第9080行
  - 旧: `[Def-S-17-02](../../Struct/04-proofs/04.01-flink-checkpoint-correctness.md)`
  - 新: `[Def-S-17-02](USTM-F-Reconstruction/archive/original-struct/04-proofs/04.01-flink-checkpoint-correctness.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第9167行
  - 旧: `[Def-S-18-01](../../Struct/04-proofs/04.02-flink-exactly-once-correctness.md)`
  - 新: `[Def-S-18-01](USTM-F-Reconstruction/archive/original-struct/04-proofs/04.02-flink-exactly-once-correctness.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第11696行
  - 旧: `[Lemma-S-08-02 Watermark 单调性](./02-properties/02.03-watermark-monotonicity.md)`
  - 新: `[Lemma-S-08-02 Watermark 单调性](USTM-F-Reconstruction/archive/original-struct/02-properties/02.03-watermark-monotonicity.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第14522行
  - 旧: `[Thm-F-02-01](../../02-core/checkpoint-mechanism-deep-dive.md)`
  - 新: `[Thm-F-02-01](Flink/02-core/checkpoint-mechanism-deep-dive.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第15993行
  - 旧: `[01.02-proce...`
- 文件: `Struct\01-foundation\01.05-csp-formalization.md` (第315行)
  上下文: `存在从 CSP 到 π-演算的迹保持编码，但 π-演算支持运行时名字创建 $(\nu a)$ 与名字传递，CSP 的静态命名无法模拟动态拓扑变化。因此 **CSP $\subset$ π-演算**（严...`
- 文件: `Struct\01-foundation\01.06-petri-net-formalization.md` (第354行)
  上下文: `详见 [01.02-process-calculus-primer.md](./01.02-process-calculus-primer.md)`
  - 新: `[01.02-proce...`
- 文件: `Struct\01-foundation\01.05-csp-formalization.md` (第315行)
  上下文: `存在从 CSP 到 π-演算的迹保持编码，但 π-演算支持运行时名字创建 $(\nu a)$ 与名字传递，CSP 的静态命名无法模拟动态拓扑变化。因此 **CSP $\subset$ π-演算**（严...`
- 文件: `Struct\01-foundation\01.06-petri-net-formalization.md` (第354行)
  上下文: `详见 [01.02-process-calculus-primer.md](USTM-F-Reconstruction/archive/original-struct/01-foundation/01.02-process-calculus-primer.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第16078行
  - 旧: `[01.04-dataflow-model-formalization.md](../01-foundation/01.04-dataflow-model-formalization.md)`
  - 新: `[01.04-dataflow-model-formalization.md](USTM-F-Reconstruction/archive/original-struct/01-foundation/01.04-dataflow-model-formalization.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第16209行
  - 旧: `[02.01-determinism-in-streaming.md](../02-properties/02.01-determinism-in-streaming.md)`
  - 新: `[02.01-determinism-in-streaming.md](USTM-F-Reconstruction/archive/original-struct/02-properties/02.01-determinism-in-streaming.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第16303行
  - 旧: `[02.02-consistency-hierarchy.md](../02-properties/02.02-consistency-hierarchy.md)`
  - 新: `[02.02-consistency-hierarchy.md](USTM-F-Reconstruction/archive/original-struct/02-properties/02.02-consistency-hierarchy.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第16355行
  - 旧: `[02.03](../02-properties/02.03-watermark-monotonicity.md)`
  - 新: `[02.03](USTM-F-Reconstruction/archive/original-struct/02-properties/02.03-watermark-monotonicity.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第16415行
  - 旧: `[Thm-S-11-01](../../Struct/02-properties/02.05-type-safety-derivation.md)`
  - 新: `[Thm-S-11-01](USTM-F-Reconstruction/archive/original-struct/02-properties/02.05-type-safety-derivation.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第16450行
  - 旧: `[Thm-S-12-01 Actor→CSP Encoding](./03-relationships/03.01-actor-to-csp-encoding.md)`
  - 新: `[Thm-S-12-01 Actor→CSP Encoding](USTM-F-Reconstruction/archive/original-struct/03-relationships/03.01-actor-to-csp-encoding.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第16488行
  - 旧: `[Thm-S-13-01 Flink→Process Calculus](./03-relationships/03.02-flink-to-process-calculus.md)`
  - 新: `[Thm-S-13-01 Flink→Process Calculus](USTM-F-Reconstruction/archive/original-struct/03-relationships/03.02-flink-to-process-calculus.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第16505行
  - 旧: `[Thm-S-14-01 表达力层级](./03-relationships/03.03-expressiveness-hierarchy.md)`
  - 新: `[Thm-S-14-01 表达力层级](USTM-F-Reconstruction/archive/original-struct/03-relationships/03.03-expressiveness-hierarchy.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第16606行
  - 旧: `[Thm-S-17-01 Checkpoint 正确性](./04-proofs/04.01-flink-checkpoint-correctness.md)`
  - 新: `[Thm-S-17-01 Checkpoint 正确性](USTM-F-Reconstruction/archive/original-struct/04-proofs/04.01-flink-checkpoint-correctness.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第16697行
  - 旧: `[Thm-S-18-01 Exactly-Once](./04-proofs/04.02-flink-exactly-once-correctness.md)`
  - 新: `[Thm-S-18-01 Exactly-Once](USTM-F-Reconstruction/archive/original-struct/04-proofs/04.02-flink-exactly-once-correctness.md)`

- `FORMAL-ELEMENT-UNIQUENESS-REPORT.md` 第16769行
  - 旧: `[Thm-S-19-01 Chandy-Lamport](./04-proofs/04.03-chandy-lamport-consistency.md)`
  - 新: `[Thm-S-19-01 Chandy-Lamport](USTM-F-Reconstruction/archive/original-struct/04-proofs/04.03-chandy-lamport-consistency.md)`

- `HISTORY.md` 第612行
  - 旧: `[PROJECT-VERSION-TRACKING.md](PROJECT-VERSION-TRACKING.md)`
  - 新: `[PROJECT-VERSION-TRACKING.md](archive/tracking-reports/PROJECT-VERSION-TRACKING.md)`

- `MAINTENANCE-GUIDE.md` 第809行
  - 旧: `[PROJECT-VERSION-TRACKING.md](./PROJECT-VERSION-TRACKING.md)`
  - 新: `[PROJECT-VERSION-TRACKING.md](archive/tracking-reports/PROJECT-VERSION-TRACKING.md)`

- `NAVIGATION-INDEX.md` 第611行
  - 旧: `[PROJECT-VERSION-TRACKING.md](PROJECT-VERSION-TRACKING.md)`
  - 新: `[PROJECT-VERSION-TRACKING.md](archive/tracking-reports/PROJECT-VERSION-TRACKING.md)`

- `NAVIGATION-INDEX.md` 第631行
  - 旧: `[FULL-COMPLETION-REPORT-v3.2.md](FULL-COMPLETION-REPORT-v3.2.md)`
  - 新: `[FULL-COMPLETION-REPORT-v3.2.md](archive/completion-reports/FULL-COMPLETION-REPORT-v3.2.md)`

- `NAVIGATION-INDEX.md` 第632行
  - 旧: `[FINAL-COMPLETION-REPORT-v5.0.md](FINAL-COMPLETION-REPORT-v5.0.md)`
  - 新: `[FINAL-COMPLETION-REPORT-v5.0.md](archive/completion-reports/FINAL-COMPLETION-REPORT-v5.0.md)`

- `NAVIGATION-INDEX.md` 第633行
  - 旧: `[E1-E4-ACCURACY-FIX-COMPLETION-REPORT.md](E1-E4-ACCURACY-FIX-COMPLETION-REPORT.md)`
  - 新: `[E1-E4-ACCURACY-FIX-COMPLETION-REPORT.md](archive/completion-reports/E1-E4-ACCURACY-FIX-COMPLETION-REPORT.md)`

- `NAVIGATION-INDEX.md` 第634行
  - 旧: `[FLINK-SCALA-RUST-COMPLETION-REPORT.md](FLINK-SCALA-RUST-COMPLETION-REPORT.md)`
  - 新: `[FLINK-SCALA-RUST-COMPLETION-REPORT.md](archive/completion-reports/FLINK-SCALA-RUST-COMPLETION-REPORT.md)`

- `NAVIGATION-INDEX.md` 第635行
  - 旧: `[CONTINUOUS-EXPANSION-REPORT.md](CONTINUOUS-EXPANSION-REPORT.md)`
  - 新: `[CONTINUOUS-EXPANSION-REPORT.md](archive/completion-reports/CONTINUOUS-EXPANSION-REPORT.md)`

- `PROJECT-QUICK-REFERENCE.md` 第47行
  - 旧: `[Flink/01-architecture/flink-1.x-vs-2.0-comparison.md](Flink/01-architecture/flink-1.x-vs-2.0-comparison.md)`
  - 新: `[Flink/01-architecture/flink-1.x-vs-2.0-comparison.md](Flink/01-concepts/flink-1.x-vs-2.0-comparison.md)`

- `PROJECT-QUICK-REFERENCE.md` 第48行
  - 旧: `[Flink/06-engineering/performance-tuning-guide.md](Flink/06-engineering/performance-tuning-guide.md)`
  - 新: `[Flink/06-engineering/performance-tuning-guide.md](Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md)`

- `PROJECT-QUICK-REFERENCE.md` 第49行
  - 旧: `[Flink/03-sql-table-api/sql-vs-datastream-comparison.md](Flink/03-sql-table-api/sql-vs-datastream-comparison.md)`
  - 新: `[Flink/03-sql-table-api/sql-vs-datastream-comparison.md](Flink/03-api/03.02-table-sql-api/sql-vs-datastream-comparison.md)`

- `PROJECT-QUICK-REFERENCE.md` 第50行
  - 旧: `[Flink/12-ai-ml/flink-ai-agents-flip-531.md](Flink/12-ai-ml/flink-ai-agents-flip-531.md)`
  - 新: `[Flink/12-ai-ml/flink-ai-agents-flip-531.md](Flink/06-ai-ml/flink-ai-agents-flip-531.md)`

- `PROJECT-QUICK-REFERENCE.md` 第73行
  - 旧: `[flink-ai-agents-flip-531.md](Flink/12-ai-ml/flink-ai-agents-flip-531.md)`
  - 新: `[flink-ai-agents-flip-531.md](Flink/06-ai-ml/flink-ai-agents-flip-531.md)`

- `PROJECT-QUICK-REFERENCE.md` 第74行
  - 旧: `[flink-llm-integration.md](Flink/12-ai-ml/flink-llm-integration.md)`
  - 新: `[flink-llm-integration.md](Flink/06-ai-ml/flink-llm-integration.md)`

- `PROJECT-QUICK-REFERENCE.md` 第75行
  - 旧: `[online-learning-algorithms.md](Flink/12-ai-ml/online-learning-algorithms.md)`
  - 新: `[online-learning-algorithms.md](Flink/06-ai-ml/online-learning-algorithms.md)`

- `PROJECT-QUICK-REFERENCE.md` 第76行
  - 旧: `[realtime-feature-engineering-feature-store.md](Flink/12-ai-ml/realtime-feature-engineering-feature-store.md)`
  - 新: `[realtime-feature-engineering-feature-store.md](Flink/06-ai-ml/realtime-feature-engineering-feature-store.md)`

- `PROJECT-QUICK-REFERENCE.md` 第77行
  - 旧: `[rag-streaming-architecture.md](Flink/12-ai-ml/rag-streaming-architecture.md)`
  - 新: `[rag-streaming-architecture.md](Flink/06-ai-ml/rag-streaming-architecture.md)`

- `PROJECT-QUICK-REFERENCE.md` 第83行
  - 旧: `[flink-1.x-vs-2.0-comparison.md](Flink/01-architecture/flink-1.x-vs-2.0-comparison.md)`
  - 新: `[flink-1.x-vs-2.0-comparison.md](Flink/01-concepts/flink-1.x-vs-2.0-comparison.md)`

- `PROJECT-QUICK-REFERENCE.md` 第84行
  - 旧: `[disaggregated-state-analysis.md](Flink/01-architecture/disaggregated-state-analysis.md)`
  - 新: `[disaggregated-state-analysis.md](Flink/01-concepts/disaggregated-state-analysis.md)`

- `PROJECT-QUICK-REFERENCE.md` 第85行
  - 旧: `[flink-deployment-ops-complete-guide.md](Flink/10-deployment/flink-deployment-ops-complete-guide.md)`
  - 新: `[flink-deployment-ops-complete-guide.md](Flink/04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md)`

- `PROJECT-QUICK-REFERENCE.md` 第86行
  - 旧: `[flink-serverless-architecture.md](Flink/10-deployment/flink-serverless-architecture.md)`
  - 新: `[flink-serverless-architecture.md](Flink/04-runtime/04.01-deployment/flink-serverless-architecture.md)`

- `PROJECT-QUICK-REFERENCE.md` 第92行
  - 旧: `[flink-paimon-integration.md](Flink/14-lakehouse/flink-paimon-integration.md)`
  - 新: `[flink-paimon-integration.md](Flink/05-ecosystem/05.01-connectors/flink-paimon-integration.md)`

- `PROJECT-QUICK-REFERENCE.md` 第93行
  - 旧: `[flink-iceberg-integration.md](Flink/14-lakehouse/flink-iceberg-integration.md)`
  - 新: `[flink-iceberg-integration.md](Flink/05-ecosystem/05.01-connectors/flink-iceberg-integration.md)`

- `PROJECT-QUICK-REFERENCE.md` 第94行
  - 旧: `[streaming-lakehouse-deep-dive-2026.md](Flink/14-lakehouse/streaming-lakehouse-deep-dive-2026.md)`
  - 新: `[streaming-lakehouse-deep-dive-2026.md](Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-deep-dive-2026.md)`

- `PROJECT-QUICK-REFERENCE.md` 第100行
  - 旧: `[flink-security-complete-guide.md](Flink/13-security/flink-security-complete-guide.md)`
  - 新: `[flink-security-complete-guide.md](Flink/09-practices/09.04-security/flink-security-complete-guide.md)`

- `PROJECT-QUICK-REFERENCE.md` 第101行
  - 旧: `[trusted-execution-flink.md](Flink/13-security/trusted-execution-flink.md)`
  - 新: `[trusted-execution-flink.md](Flink/09-practices/09.04-security/trusted-execution-flink.md)`

- `PROJECT-QUICK-REFERENCE.md` 第102行
  - 旧: `[gpu-confidential-computing.md](Flink/13-security/gpu-confidential-computing.md)`
  - 新: `[gpu-confidential-computing.md](Flink/09-practices/09.04-security/gpu-confidential-computing.md)`

- `PROJECT-QUICK-REFERENCE.md` 第108行
  - 旧: `[sql-vs-datastream-comparison.md](Flink/03-sql-table-api/sql-vs-datastream-comparison.md)`
  - 新: `[sql-vs-datastream-comparison.md](Flink/03-api/03.02-table-sql-api/sql-vs-datastream-comparison.md)`

- `PROJECT-QUICK-REFERENCE.md` 第109行
  - 旧: `[query-optimization-analysis.md](Flink/03-sql-table-api/query-optimization-analysis.md)`
  - 新: `[query-optimization-analysis.md](Flink/03-api/03.02-table-sql-api/query-optimization-analysis.md)`

- `PROJECT-QUICK-REFERENCE.md` 第110行
  - 旧: `[flink-materialized-table-deep-dive.md](Flink/03-sql-table-api/flink-materialized-table-deep-dive.md)`
  - 新: `[flink-materialized-table-deep-dive.md](Flink/03-api/03.02-table-sql-api/flink-materialized-table-deep-dive.md)`

- `PROJECT-QUICK-REFERENCE.md` 第111行
  - 旧: `[vector-search.md](Flink/03-sql-table-api/vector-search.md)`
  - 新: `[vector-search.md](Flink/03-api/03.02-table-sql-api/vector-search.md)`

- `PROJECT-QUICK-REFERENCE.md` 第122行
  - 旧: `[Flink/12-ai-ml/flink-ai-ml-integration-complete-guide.md](Flink/12-ai-ml/flink-ai-ml-integration-complete-guide.md)`
  - 新: `[Flink/12-ai-ml/flink-ai-ml-integration-complete-guide.md](Flink/06-ai-ml/flink-ai-ml-integration-complete-guide.md)`

- `PROJECT-QUICK-REFERENCE.md` 第123行
  - 旧: `[Flink/13-security/flink-security-complete-guide.md](Flink/13-security/flink-security-complete-guide.md)`
  - 新: `[Flink/13-security/flink-security-complete-guide.md](Flink/09-practices/09.04-security/flink-security-complete-guide.md)`

- `PROJECT-QUICK-REFERENCE.md` 第125行
  - 旧: `[Flink/10-deployment/flink-deployment-ops-complete-guide.md](Flink/10-deployment/flink-deployment-ops-complete-guide.md)`
  - 新: `[Flink/10-deployment/flink-deployment-ops-complete-guide.md](Flink/04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md)`

- `PROJECT-QUICK-REFERENCE.md` 第126行
  - 旧: `[Flink/14-lakehouse/streaming-lakehouse-deep-dive-2026.md](Flink/14-lakehouse/streaming-lakehouse-deep-dive-2026.md)`
  - 新: `[Flink/14-lakehouse/streaming-lakehouse-deep-dive-2026.md](Flink/05-ecosystem/05.02-lakehouse/streaming-lakehouse-deep-dive-2026.md)`

- `PROJECT-QUICK-REFERENCE.md` 第127行
  - 旧: `[Flink/14-graph/flink-gelly-streaming-graph-processing.md](Flink/14-graph/flink-gelly-streaming-graph-processing.md)`
  - 新: `[Flink/14-graph/flink-gelly-streaming-graph-processing.md](Flink/05-ecosystem/05.04-graph/flink-gelly-streaming-graph-processing.md)`

- `PROJECT-QUICK-REFERENCE.md` 第128行
  - 旧: `[Flink/10-deployment/flink-serverless-architecture.md](Flink/10-deployment/flink-serverless-architecture.md)`
  - 新: `[Flink/10-deployment/flink-serverless-architecture.md](Flink/04-runtime/04.01-deployment/flink-serverless-architecture.md)`

- `PROJECT-QUICK-REFERENCE.md` 第129行
  - 旧: `[Flink/08-roadmap/flink-2.3-2.4-roadmap.md](Flink/08-roadmap/flink-2.3-2.4-roadmap.md)`
  - 新: `[Flink/08-roadmap/flink-2.3-2.4-roadmap.md](Flink/08-roadmap/08.01-flink-24/flink-2.3-2.4-roadmap.md)`

- `PROJECT-QUICK-REFERENCE.md` 第130行
  - 旧: `[Flink/12-ai-ml/flink-llm-integration.md](Flink/12-ai-ml/flink-llm-integration.md)`
  - 新: `[Flink/12-ai-ml/flink-llm-integration.md](Flink/06-ai-ml/flink-llm-integration.md)`

- `PROJECT-QUICK-REFERENCE.md` 第163行
  - 旧: `[performance-tuning-guide.md](Flink/06-engineering/performance-tuning-guide.md)`
  - 新: `[performance-tuning-guide.md](Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md)`

- `PROJECT-QUICK-REFERENCE.md` 第167行
  - 旧: `[flink-vs-spark-streaming.md](Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-kafka-streams.md)`
  - 新: `[flink-vs-spark-streaming.md](Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-spark-streaming.md)`

- `PROJECT-QUICK-REFERENCE.md` 第178行
  - 旧: `[DataStream API语义](Flink/01-architecture/datastream-v2-semantics.md)`
  - 新: `[DataStream API语义](Flink/01-concepts/datastream-v2-semantics.md)`

- `PROJECT-TRACKING.md` 第15行
  - 旧: `[完成报告](P2-CONTENT-COMPLETION-REPORT.md)`
  - 新: `[完成报告](archive/completion-reports/P2-CONTENT-COMPLETION-REPORT.md)`

- `PROJECT-TRACKING.md` 第17行
  - 旧: `[完成报告](FLINK-24-25-30-COMPLETION-REPORT.md)`
  - 新: `[完成报告](archive/completion-reports/FLINK-24-25-30-COMPLETION-REPORT.md)`

- `PROJECT-TRACKING.md` 第215行
  - 旧: `[Flink JDBC Connector指南](Flink/connectors/flink-jdbc-connector-guide.md)`
  - 新: `[Flink JDBC Connector指南](Flink/05-ecosystem/05.01-connectors/flink-jdbc-connector-guide.md)`

- `PROJECT-TRACKING.md` 第216行
  - 旧: `[Flink ES Connector指南](Flink/connectors/flink-elasticsearch-connector-guide.md)`
  - 新: `[Flink ES Connector指南](Flink/05-ecosystem/05.01-connectors/flink-elasticsearch-connector-guide.md)`

- `PROJECT-TRACKING.md` 第217行
  - 旧: `[Flink MongoDB Connector指南](Flink/connectors/flink-mongodb-connector-guide.md)`
  - 新: `[Flink MongoDB Connector指南](Flink/05-ecosystem/05.01-connectors/flink-mongodb-connector-guide.md)`

- `PROJECT-TRACKING.md` 第501行
  - 旧: `[Flink/ecosystem/risingwave-integration-guide.md](Flink/ecosystem/risingwave-integration-guide.md)`
  - 新: `[Flink/ecosystem/risingwave-integration-guide.md](Flink/risingwave-integration-guide.md)`

- `PROJECT-TRACKING.md` 第502行
  - 旧: `[Flink/ecosystem/materialize-comparison.md](Flink/ecosystem/materialize-comparison.md)`
  - 新: `[Flink/ecosystem/materialize-comparison.md](Flink/materialize-comparison.md)`

- `PROJECT-TRACKING.md` 第503行
  - 旧: `[Flink/ecosystem/kafka-streams-migration.md](Flink/ecosystem/kafka-streams-migration.md)`
  - 新: `[Flink/ecosystem/kafka-streams-migration.md](Knowledge/kafka-streams-migration.md)`

- `PROJECT-TRACKING.md` 第504行
  - 旧: `[Flink/ecosystem/pulsar-functions-integration.md](Flink/ecosystem/pulsar-functions-integration.md)`
  - 新: `[Flink/ecosystem/pulsar-functions-integration.md](Flink/pulsar-functions-integration.md)`

- `PROJECT-TRACKING.md` 第1187行
  - 旧: `[FLINK-24-25-30-COMPLETION-REPORT.md](FLINK-24-25-30-COMPLETION-REPORT.md)`
  - 新: `[FLINK-24-25-30-COMPLETION-REPORT.md](archive/completion-reports/FLINK-24-25-30-COMPLETION-REPORT.md)`

- `README-EN.md` 第226行
  - 旧: `[LICENSE-NOTICE.md](./LICENSE-NOTICE.md)`
  - 新: `[LICENSE-NOTICE.md](archive/deprecated/LICENSE-NOTICE.md)`

... 还有 646 条修复记录

## 未修复链接示例 (前 50 条)

- `.\BROKEN-LINK-FIX-REPORT.md`: `[FLINK-24-25-30-COMPLETION-REPORT.md](./FLINK-24-25-30-COMPLETION-REPORT.md)`
- `.\cross-ref-error-analysis.md`: `[自适应执行V2](flink-24/flink-24-adaptive-execution-v2.md)`
- `.\DESIGN-PRINCIPLES.md`: `[状态管理](./Flink/02-core-mechanisms/flink-state-management-complete-guide.md)`
- `.\FLINK_REVISION_REPORT.md`: `[02-core/checkpoint-mechanism-deep-dive.md](02-core/checkpoint-mechanisms-deep-dive.md)`
- `.\FORMAL-ELEMENT-UNIQUENESS-REPORT.md`: `[Dataflow 模型形式化](../../../../Struct/01-foundation/01.04-dataflow-model-formalization.md)`
- `.\FORMAL-ELEMENT-UNIQUENESS-REPORT.md`: `[Def-S-04-05](../../../Struct/01-foundation/01.04-dataflow-model-formalization.md)`
- `.\FORMAL-ELEMENT-UNIQUENESS-REPORT.md`: `[Struct/02-properties/02.03-watermark-monotonic...`
- 文件: `Knowledge\02-design-patterns\pattern-async-io-enrichment.md` (第191行)
  上下文: `> **Lemma-S-04-02**: Watermark 在 Dataflow 图中的传播保持单调不减。...`
- 文件: `Knowledge\02-design-patterns\pattern-async-io-enrichment.md` (第376行)
  上下文: `| **Lemma-S-04-02** | Watermark 单调性引理 | Struct/01.04 | 顺序保持模式下 Watermark 直接透传，单调性保持 |...`
- 文件: `Knowledge\02-design-patterns\pattern-async-io-enrichment.md` (第385行)
  上下文: `- 顺序保持模式：Watermark 透传，单调性保持 (Lemma-S-04-02)...`
- 文件: `Knowledge\02-design-patterns\pattern-async-io-enrichment.md` (第413行)
  上下文: `| 顺序保持模式 |`AsyncDataStream.orderedWait()`| Lemma-S-04-02 单调性保证 |...`
- 文件: `Knowledge\02-design-patterns\pattern-cep-complex-event.md` (第875行)
  上下文: `| **Lemma-S-04-02** | Watermark 单调性引理 | Struct/01.04 | NFA 状态机的事件时间推进保持单调 |...`
- 文件: `Knowledge\02-design-patterns\pattern-event-time-processing.md` (第628行)
  上下文: `| **Lemma-S-04-02** | Watermark 单调性引理 | Struct/01.04 | Watermark 在 Dataflow 图中传播保持单调不减 |...`
- 文件: `Knowledge\02-design-patterns\pattern-event-time-processing.md` (第642行)
  上下文: `- 恢复后的 Watermark 从 checkpointed 值继续推进，满足 Lemma-S-04-02...`
- 文件: `Knowledge\02-design-patterns\pattern-windowed-aggregation.md` (第320行)
  上下文: `**推论**：Watermark 的单调性（Lemma-S-04-02）保证了窗口触发的**幂等性**——同一窗口不会重复触发。...`
- 文件: `Knowledge\02-design-patterns\pattern-windowed-aggregation.md` (第872行)
  上下文: `| Window + Async I/O | 聚合前富化顺序保持 | Lemma-S-04-02 |...`
- 文件: `Knowledge\05-mapping-guides\struct-to-flink-mapping.md` (第241行)
  上下文: `**形式化定义** ([Def-S-04-04](../../Struct/01-foundation/01.04-dataflow-model-formalization.md)`
- `.\FORMAL-ELEMENT-UNIQUENESS-REPORT.md`: `[02.03-watermark-monotonicity.md](../02-properties/02.03-watermark-monotonicity.md)`
- `.\FORMAL-ELEMENT-UNIQUENESS-REPORT.md`: `[pattern-checkpo...`
- 文件: `Struct\Struct-to-Knowledge-Mapping.md` (第603行)
  上下文: `| [Thm-S-17-01 Checkpoint 正确性](./04-proofs/04.01-flink-checkpoint-correctness.md)`
- `.\MAINTENANCE-GUIDE.md`: `[new-feature-guide.md](./Flink/02-core-mechanisms/flink-2.2-frontier-features.md)`
- `.\PDF-EXPORT-GUIDE.md`: `[下载PDF](./whitepapers/pdf/streaming-technology-trends-2026.pdf)`
- `.\PDF-EXPORT-GUIDE.md`: `[下载PDF](./whitepapers/pdf/flink-enterprise-implementation-guide.pdf)`
- `.\PDF-EXPORT-GUIDE.md`: `[下载PDF](./whitepapers/pdf/realtime-ai-architecture-practice.pdf)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md](Flink/02-core/checkpoint-mechanism-deep-dive.md)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[Flink/02-core-mechanisms/exactly-once-end-to-end.md](Flink/02-core-mechanisms/exactly-once-end-to-end.md)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[Flink/02-core-mechanisms/time-semantics-and-watermark.md](Flink/02-core/time-semantics-and-watermark.md)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[Flink/02-core-mechanisms/backpressure-and-flow-control.md](Flink/02-core-mechanisms/backpressure-and-flow-control.md)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[checkpoint-mechanism-deep-dive.md](Flink/02-core/checkpoint-mechanism-deep-dive.md)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[exactly-once-end-to-end.md](Flink/02-core-mechanisms/exactly-once-end-to-end.md)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[time-semantics-and-watermark.md](Flink/02-core/time-semantics-and-watermark.md)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[flink-state-management-complete-guide.md](Flink/02-core-mechanisms/flink-state-management-complete-guide.md)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[backpressure-and-flow-control.md](Flink/02-core-mechanisms/backpressure-and-flow-control.md)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[Flink/12-ai-ml/flink-ai-agents-flip-531.md](Flink/12-ai-ml/flink-ai-agents-flip-531.md)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[Flink/02-core-mechanisms/flink-state-management-complete-guide.md](Flink/02-core-mechanisms/flink-state-management-complete-guide.md)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[checkpoint-mechanism-deep-dive.md](Flink/02-core/checkpoint-mechanism-deep-dive.md)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[backpressure-and-flow-control.md](Flink/02-core-mechanisms/backpressure-and-flow-control.md)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[performance-tuning-guide.md](Flink/06-engineering/performance-tuning-guide.md)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[exactly-once-end-to-end.md](Flink/02-core-mechanisms/exactly-once-end-to-end.md)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[time-semantics-and-watermark.md](Flink/02-core/time-semantics-and-watermark.md)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[performance-tuning-guide.md](Flink/06-engineering/performance-tuning-guide.md)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[sql-vs-datastream-comparison.md](Flink/03-sql-table-api/sql-vs-datastream-comparison.md)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[flink-ai-agents-flip-531.md](Flink/12-ai-ml/flink-ai-agents-flip-531.md)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[rag-streaming-architecture.md](Flink/12-ai-ml/rag-streaming-architecture.md)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[Checkpoint机制深度解析](Flink/02-core/checkpoint-mechanism-deep-dive.md)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[Exactly-Once端到端](Flink/02-core-mechanisms/exactly-once-end-to-end.md)`
- `.\PROJECT-QUICK-REFERENCE.md`: `[时间语义与Watermark](Flink/02-core/time-semantics-and-watermark.md)`
- `.\PROJECT-TRACKING.md`: `[.scripts/doc-relationship-mapper.py](./.scripts/doc-relationship-mapper.py)`
- `.\PROJECT-TRACKING.md`: `[.scripts/concept-dependency-generator.py](./.scripts/concept-dependency-generator.py)`
- `.\README-EN.md`: `[Flink/ Checkpoint Mechanism](Flink/02-core/checkpoint-mechanism-deep-dive.md)`
- `.\WHITEPAPER-PDF-EXPORT-COMPLETION-REPORT.md`: `[PDF](./whitepapers/pdf/streaming-technology-trends-2026.pdf)`
- `.\WHITEPAPER-PDF-EXPORT-COMPLETION-REPORT.md`: `[PDF](./whitepapers/pdf/flink-enterprise-implementation-guide.pdf)`
- `.\WHITEPAPER-PDF-EXPORT-COMPLETION-REPORT.md`: `[PDF](./whitepapers/pdf/realtime-ai-architecture-practice.pdf)`
- `.\archive\completion-reports\CROSS-REF-VALIDATION-REPORT-v2.md`: `[文本](Struct/01-foundation/01.01-ustm.md)`
- `.\archive\completion-reports\CROSS-REF-VALIDATION-REPORT-v2.md`: `[相关文档1](path/to/doc1.md)`
- `.\archive\completion-reports\CROSS-REF-VALIDATION-REPORT-v2.md`: `[相关文档2](path/to/doc2.md)`
- `.\archive\completion-reports\CROSS-REF-VALIDATION-REPORT-v2.md`: `[](../path)`
- `.\archive\completion-reports\CROSS-REF-VALIDATION-REPORT-v2.md`: `[text](./path/to/file.md)`
- `.\archive\completion-reports\FLINK-DOCUMENTATION-GAP-ANALYSIS.md`: `[time-semantics-and-watermark.md](Flink/02-core/time-semantics-and-watermark.md)`
- `.\archive\completion-reports\FLINK-DOCUMENTATION-GAP-ANALYSIS.md`: `[flink-state-management-complete-guide.md](Flink/02-core-mechanisms/flink-state-management-complete-guide.md)`
- `.\archive\completion-reports\FLINK-DOCUMENTATION-GAP-ANALYSIS.md`: `[checkpoint-mechanism-deep-dive.md](Flink/02-core/checkpoint-mechanism-deep-dive.md)`
- ... 还有 1283 条未修复

## 修复规则说明

1. **目录重映射**: Flink/12-ai-ml/ → Flink/06-ai-ml/ 等
2. **文件名查找**: 通过全局文件名索引自动定位目标文档
3. **相对路径保持**: 修复后的链接仍保持相对路径格式
4. **误报过滤**: 对实际存在的目标文件（如 README.md）跳过修复
