# 定理依赖验证报告

> **生成时间**: 2026-04-11 19:58:16
> **验证工具**: Theorem Dependency Validator v1.0.0

## 摘要

- **扫描文件数**: 655
- **发现元素数**: 438
- **问题总数**: 298
  - 错误: 101
  - 警告: 143
  - 信息: 54

## 统计概览

### 按类型分布

| 类型 | 数量 | 占比 |
|------|------|------|
| Cor | 4 | 0.9% |
| Def | 229 | 52.3% |
| Lemma | 99 | 22.6% |
| Prop | 27 | 6.2% |
| Thm | 79 | 18.0% |

### 按阶段分布

| 阶段 | 数量 | 说明 |
|------|------|------|
| F | 213 | Flink - Flink专项 |
| K | 137 | Knowledge - 知识结构 |
| S | 88 | Struct - 形式理论 |

### 形式化等级分布

| 等级 | 数量 |
|------|------|
| L3 | 10 |
| L4 | 20 |
| L4-L5 | 6 |
| L5 | 5 |

### 依赖覆盖

- **有依赖的元素**: 323 / 438 (73.7%)
- **有被引用的元素**: 312 / 438
- **孤立元素**: 54
- **依赖关系总数**: 794

## 关键路径

依赖图中最长的依赖链:

Def-F-14-21 -> Def-F-14-22 -> Def-F-14-23 -> Def-F-14-24 -> Def-F-14-25 -> Thm-F-14-15 -> Thm-F-14-16 -> Thm-F-14-17 -> Thm-F-14-18 -> Def-F-14-05 -> Def-F-14-06 -> Def-F-14-07 -> Def-F-14-08 -> Def-F-14-09 -> Thm-F-14-04 -> Thm-F-14-05 -> Thm-F-14-06

## 问题详情

### 错误

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-12-01
- **元素**: Thm-S-12-01
- **位置**: Struct\Proof-Chains-Cross-Model-Encoding.md:666
- **建议**: 该编号已在 Struct\Proof-Chains-Cross-Model-Encoding.md:48 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-12-02
- **元素**: Thm-S-12-02
- **位置**: Struct\Proof-Chains-Cross-Model-Encoding.md:667
- **建议**: 该编号已在 Struct\Proof-Chains-Cross-Model-Encoding.md:260 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-13-01
- **元素**: Thm-S-13-01
- **位置**: Struct\Proof-Chains-Cross-Model-Encoding.md:668
- **建议**: 该编号已在 Struct\Proof-Chains-Cross-Model-Encoding.md:294 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-14-01
- **元素**: Thm-S-14-01
- **位置**: Struct\Proof-Chains-Cross-Model-Encoding.md:669
- **建议**: 该编号已在 Struct\Proof-Chains-Cross-Model-Encoding.md:585 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-F-02-01
- **元素**: Thm-F-02-01
- **位置**: Struct\Proof-Chains-Flink-Implementation.md:290
- **建议**: 该编号已在 Struct\Proof-Chains-Flink-Implementation.md:132 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-17-01
- **元素**: Thm-S-17-01
- **位置**: Struct\PROOF-CHAINS-INDEX.md:530
- **建议**: 该编号已在 Struct\Proof-Chains-Checkpoint-Correctness.md:54 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-18-01
- **元素**: Thm-S-18-01
- **位置**: Struct\PROOF-CHAINS-INDEX.md:531
- **建议**: 该编号已在 Struct\Proof-Chains-Exactly-Once-Correctness.md:560 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-12-01
- **元素**: Thm-S-12-01
- **位置**: Struct\PROOF-CHAINS-INDEX.md:532
- **建议**: 该编号已在 Struct\Proof-Chains-Cross-Model-Encoding.md:48 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-13-01
- **元素**: Thm-S-13-01
- **位置**: Struct\PROOF-CHAINS-INDEX.md:533
- **建议**: 该编号已在 Struct\Proof-Chains-Cross-Model-Encoding.md:294 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-04-01
- **元素**: Thm-S-04-01
- **位置**: Struct\PROOF-CHAINS-INDEX.md:534
- **建议**: 该编号已在 Struct\Proof-Chains-Dataflow-Foundation.md:624 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-F-02-45
- **元素**: Thm-F-02-45
- **位置**: Struct\PROOF-CHAINS-INDEX.md:536
- **建议**: 该编号已在 Struct\Proof-Chains-Flink-Implementation.md:199 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-F-02-50
- **元素**: Thm-F-02-50
- **位置**: Struct\PROOF-CHAINS-INDEX.md:537
- **建议**: 该编号已在 Struct\Proof-Chains-Flink-Implementation.md:335 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-17-01
- **元素**: Thm-S-17-01
- **位置**: Struct\Proof-Chains-Master-Graph.md:296
- **建议**: 该编号已在 Struct\Proof-Chains-Checkpoint-Correctness.md:54 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-18-01
- **元素**: Thm-S-18-01
- **位置**: Struct\Proof-Chains-Master-Graph.md:297
- **建议**: 该编号已在 Struct\Proof-Chains-Exactly-Once-Correctness.md:560 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-F-02-45
- **元素**: Thm-F-02-45
- **位置**: Struct\Proof-Chains-Master-Graph.md:306
- **建议**: 该编号已在 Struct\Proof-Chains-Flink-Implementation.md:199 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-F-02-50
- **元素**: Thm-F-02-50
- **位置**: Struct\Proof-Chains-Master-Graph.md:307
- **建议**: 该编号已在 Struct\Proof-Chains-Flink-Implementation.md:335 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-04-01
- **元素**: Thm-S-04-01
- **位置**: Struct\02-properties\02.03-watermark-monotonicity.md:160
- **建议**: 该编号已在 Struct\Proof-Chains-Dataflow-Foundation.md:624 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-S-04-04
- **元素**: Def-S-04-04
- **位置**: Struct\02-properties\02.03-watermark-monotonicity.md:155
- **建议**: 该编号已在 Struct\Proof-Chains-Dataflow-Foundation.md:601 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-09-01
- **元素**: Thm-S-09-01
- **位置**: Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:468
- **建议**: 该编号已在 Struct\02-properties\02.03-watermark-monotonicity.md:381 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-20-01
- **元素**: Thm-S-20-01
- **位置**: Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:634
- **建议**: 该编号已在 Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:248 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-09-01
- **元素**: Thm-S-09-01
- **位置**: Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:1160
- **建议**: 该编号已在 Struct\02-properties\02.03-watermark-monotonicity.md:381 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-20-01
- **元素**: Thm-S-20-01
- **位置**: Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:1366
- **建议**: 该编号已在 Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:248 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-S-20-02
- **元素**: Def-S-20-02
- **位置**: Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:324
- **建议**: 该编号已在 Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:264 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-S-20-01
- **元素**: Def-S-20-01
- **位置**: Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:441
- **建议**: 该编号已在 Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:419 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-S-20-02
- **元素**: Def-S-20-02
- **位置**: Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:883
- **建议**: 该编号已在 Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:264 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Lemma-S-09-01
- **元素**: Lemma-S-09-01
- **位置**: Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:576
- **建议**: 该编号已在 Struct\02-properties\02.03-watermark-monotonicity.md:263 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Lemma-S-09-01
- **元素**: Lemma-S-09-01
- **位置**: Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:578
- **建议**: 该编号已在 Struct\02-properties\02.03-watermark-monotonicity.md:263 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-09-01
- **元素**: Thm-S-09-01
- **位置**: Struct\06-frontier\06.01-open-problems-streaming-verification.md:453
- **建议**: 该编号已在 Struct\02-properties\02.03-watermark-monotonicity.md:381 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-17-01
- **元素**: Thm-S-17-01
- **位置**: Knowledge\02-design-patterns\pattern-async-io-enrichment.md:377
- **建议**: 该编号已在 Struct\Proof-Chains-Checkpoint-Correctness.md:54 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-18-01
- **元素**: Thm-S-18-01
- **位置**: Knowledge\02-design-patterns\pattern-async-io-enrichment.md:378
- **建议**: 该编号已在 Struct\Proof-Chains-Exactly-Once-Correctness.md:560 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-S-04-04
- **元素**: Def-S-04-04
- **位置**: Knowledge\02-design-patterns\pattern-async-io-enrichment.md:367
- **建议**: 该编号已在 Struct\Proof-Chains-Dataflow-Foundation.md:601 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-S-09-02
- **元素**: Def-S-09-02
- **位置**: Knowledge\02-design-patterns\pattern-async-io-enrichment.md:368
- **建议**: 该编号已在 Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:150 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Lemma-S-04-02
- **元素**: Lemma-S-04-02
- **位置**: Knowledge\02-design-patterns\pattern-async-io-enrichment.md:189
- **建议**: 该编号已在 Struct\02-properties\02.03-watermark-monotonicity.md:155 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Lemma-S-04-02
- **元素**: Lemma-S-04-02
- **位置**: Knowledge\02-design-patterns\pattern-async-io-enrichment.md:191
- **建议**: 该编号已在 Struct\02-properties\02.03-watermark-monotonicity.md:155 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Lemma-S-04-02
- **元素**: Lemma-S-04-02
- **位置**: Knowledge\02-design-patterns\pattern-async-io-enrichment.md:376
- **建议**: 该编号已在 Struct\02-properties\02.03-watermark-monotonicity.md:155 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-09-01
- **元素**: Thm-S-09-01
- **位置**: Knowledge\02-design-patterns\pattern-cep-complex-event.md:874
- **建议**: 该编号已在 Struct\02-properties\02.03-watermark-monotonicity.md:381 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-17-01
- **元素**: Thm-S-17-01
- **位置**: Knowledge\02-design-patterns\pattern-cep-complex-event.md:877
- **建议**: 该编号已在 Struct\Proof-Chains-Checkpoint-Correctness.md:54 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-S-04-04
- **元素**: Def-S-04-04
- **位置**: Knowledge\02-design-patterns\pattern-cep-complex-event.md:865
- **建议**: 该编号已在 Struct\Proof-Chains-Dataflow-Foundation.md:601 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Lemma-S-04-02
- **元素**: Lemma-S-04-02
- **位置**: Knowledge\02-design-patterns\pattern-cep-complex-event.md:875
- **建议**: 该编号已在 Struct\02-properties\02.03-watermark-monotonicity.md:155 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-17-01
- **元素**: Thm-S-17-01
- **位置**: Knowledge\02-design-patterns\pattern-checkpoint-recovery.md:406
- **建议**: 该编号已在 Struct\Proof-Chains-Checkpoint-Correctness.md:54 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-18-01
- **元素**: Thm-S-18-01
- **位置**: Knowledge\02-design-patterns\pattern-checkpoint-recovery.md:407
- **建议**: 该编号已在 Struct\Proof-Chains-Exactly-Once-Correctness.md:560 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-07-01
- **元素**: Thm-S-07-01
- **位置**: Knowledge\02-design-patterns\pattern-checkpoint-recovery.md:409
- **建议**: 该编号已在 Struct\Proof-Chains-Dataflow-Foundation.md:626 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-17-01
- **元素**: Thm-S-17-01
- **位置**: Knowledge\02-design-patterns\pattern-checkpoint-recovery.md:445
- **建议**: 该编号已在 Struct\Proof-Chains-Checkpoint-Correctness.md:54 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-18-01
- **元素**: Thm-S-18-01
- **位置**: Knowledge\02-design-patterns\pattern-checkpoint-recovery.md:468
- **建议**: 该编号已在 Struct\Proof-Chains-Exactly-Once-Correctness.md:560 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-S-17-02
- **元素**: Def-S-17-02
- **位置**: Knowledge\02-design-patterns\pattern-checkpoint-recovery.md:397
- **建议**: 该编号已在 Knowledge\02-design-patterns\pattern-async-io-enrichment.md:369 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-09-01
- **元素**: Thm-S-09-01
- **位置**: Knowledge\02-design-patterns\pattern-event-time-processing.md:230
- **建议**: 该编号已在 Struct\02-properties\02.03-watermark-monotonicity.md:381 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-09-01
- **元素**: Thm-S-09-01
- **位置**: Knowledge\02-design-patterns\pattern-event-time-processing.md:627
- **建议**: 该编号已在 Struct\02-properties\02.03-watermark-monotonicity.md:381 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-07-01
- **元素**: Thm-S-07-01
- **位置**: Knowledge\02-design-patterns\pattern-event-time-processing.md:629
- **建议**: 该编号已在 Struct\Proof-Chains-Dataflow-Foundation.md:626 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-S-04-04
- **元素**: Def-S-04-04
- **位置**: Knowledge\02-design-patterns\pattern-event-time-processing.md:618
- **建议**: 该编号已在 Struct\Proof-Chains-Dataflow-Foundation.md:601 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-S-09-02
- **元素**: Def-S-09-02
- **位置**: Knowledge\02-design-patterns\pattern-event-time-processing.md:619
- **建议**: 该编号已在 Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:150 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-S-08-04
- **元素**: Def-S-08-04
- **位置**: Knowledge\02-design-patterns\pattern-event-time-processing.md:621
- **建议**: 该编号已在 Knowledge\02-design-patterns\pattern-cep-complex-event.md:866 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Lemma-S-04-02
- **元素**: Lemma-S-04-02
- **位置**: Knowledge\02-design-patterns\pattern-event-time-processing.md:628
- **建议**: 该编号已在 Struct\02-properties\02.03-watermark-monotonicity.md:155 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-17-01
- **元素**: Thm-S-17-01
- **位置**: Knowledge\02-design-patterns\pattern-side-output.md:405
- **建议**: 该编号已在 Struct\Proof-Chains-Checkpoint-Correctness.md:54 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-S-04-04
- **元素**: Def-S-04-04
- **位置**: Knowledge\02-design-patterns\pattern-side-output.md:394
- **建议**: 该编号已在 Struct\Proof-Chains-Dataflow-Foundation.md:601 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-S-17-02
- **元素**: Def-S-17-02
- **位置**: Knowledge\02-design-patterns\pattern-side-output.md:395
- **建议**: 该编号已在 Knowledge\02-design-patterns\pattern-async-io-enrichment.md:369 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-03-01
- **元素**: Thm-S-03-01
- **位置**: Knowledge\02-design-patterns\pattern-stateful-computation.md:329
- **建议**: 该编号已在 Knowledge\02-design-patterns\pattern-cep-complex-event.md:876 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-17-01
- **元素**: Thm-S-17-01
- **位置**: Knowledge\02-design-patterns\pattern-stateful-computation.md:331
- **建议**: 该编号已在 Struct\Proof-Chains-Checkpoint-Correctness.md:54 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-18-01
- **元素**: Thm-S-18-01
- **位置**: Knowledge\02-design-patterns\pattern-stateful-computation.md:332
- **建议**: 该编号已在 Struct\Proof-Chains-Exactly-Once-Correctness.md:560 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-S-04-01
- **元素**: Def-S-04-01
- **位置**: Knowledge\02-design-patterns\pattern-stateful-computation.md:321
- **建议**: 该编号已在 Struct\Proof-Chains-Dataflow-Foundation.md:598 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-S-17-02
- **元素**: Def-S-17-02
- **位置**: Knowledge\02-design-patterns\pattern-stateful-computation.md:322
- **建议**: 该编号已在 Knowledge\02-design-patterns\pattern-async-io-enrichment.md:369 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-09-01
- **元素**: Thm-S-09-01
- **位置**: Knowledge\02-design-patterns\pattern-windowed-aggregation.md:862
- **建议**: 该编号已在 Struct\02-properties\02.03-watermark-monotonicity.md:381 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-04-01
- **元素**: Thm-S-04-01
- **位置**: Knowledge\02-design-patterns\pattern-windowed-aggregation.md:863
- **建议**: 该编号已在 Struct\Proof-Chains-Dataflow-Foundation.md:624 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-07-01
- **元素**: Thm-S-07-01
- **位置**: Knowledge\02-design-patterns\pattern-windowed-aggregation.md:864
- **建议**: 该编号已在 Struct\Proof-Chains-Dataflow-Foundation.md:626 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-S-04-04
- **元素**: Def-S-04-04
- **位置**: Knowledge\02-design-patterns\pattern-windowed-aggregation.md:855
- **建议**: 该编号已在 Struct\Proof-Chains-Dataflow-Foundation.md:601 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-S-07-01
- **元素**: Def-S-07-01
- **位置**: Knowledge\02-design-patterns\pattern-windowed-aggregation.md:856
- **建议**: 该编号已在 Knowledge\02-design-patterns\pattern-event-time-processing.md:620 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Lemma-K-06-03
- **元素**: Lemma-K-06-03
- **位置**: Knowledge\06-frontier\streaming-access-control.md:209
- **建议**: 该编号已在 Knowledge\06-frontier\risingwave-deep-dive.md:92 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-K-06-01
- **元素**: Def-K-06-01
- **位置**: Knowledge\98-exercises\exercise-06-tla-practice.md:42
- **建议**: 该编号已在 Knowledge\06-frontier\risingwave-deep-dive.md:9 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-K-06-02
- **元素**: Def-K-06-02
- **位置**: Knowledge\98-exercises\exercise-06-tla-practice.md:43
- **建议**: 该编号已在 Knowledge\06-frontier\risingwave-deep-dive.md:23 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-K-06-03
- **元素**: Def-K-06-03
- **位置**: Knowledge\98-exercises\exercise-06-tla-practice.md:44
- **建议**: 该编号已在 Knowledge\06-frontier\risingwave-deep-dive.md:29 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-K-06-04
- **元素**: Def-K-06-04
- **位置**: Knowledge\98-exercises\exercise-06-tla-practice.md:45
- **建议**: 该编号已在 Knowledge\06-frontier\risingwave-deep-dive.md:42 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-K-05-01
- **元素**: Def-K-05-01
- **位置**: Knowledge\Flink-Scala-Rust-Comprehensive\05-architecture-patterns\COMPLETION-REPORT.md:27
- **建议**: 该编号已在 Knowledge\98-exercises\exercise-05-pattern-implementation.md:39 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-K-05-02
- **元素**: Def-K-05-02
- **位置**: Knowledge\Flink-Scala-Rust-Comprehensive\05-architecture-patterns\COMPLETION-REPORT.md:28
- **建议**: 该编号已在 Knowledge\98-exercises\exercise-05-pattern-implementation.md:40 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Def-K-05-04
- **元素**: Def-K-05-04
- **位置**: Knowledge\Flink-Scala-Rust-Comprehensive\05-architecture-patterns\COMPLETION-REPORT.md:48
- **建议**: 该编号已在 Knowledge\98-exercises\exercise-05-pattern-implementation.md:42 使用

#### DUPLICATE_ID

- **消息**: 重复的元素编号: Thm-S-09-01
- **元素**: Thm-S-09-01
- **位置**: Flink\02-core\time-semantics-and-watermark.md:205
- **建议**: 该编号已在 Struct\02-properties\02.03-watermark-monotonicity.md:381 使用

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Def-S-04-01 -> Def-S-04-02 -> Def-S-04-03 -> Def-S-04-04 -> Def-S-04-01
- **元素**: Def-S-04-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-S-04-01 -> Thm-S-04-02 -> Thm-S-07-01 -> Thm-S-04-01
- **元素**: Thm-S-04-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-S-04-02 -> Thm-S-07-01 -> Thm-S-04-02
- **元素**: Thm-S-04-02
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-S-04-01 -> Thm-S-04-02 -> Thm-S-04-01
- **元素**: Thm-S-04-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-S-04-02 -> Thm-S-04-02
- **元素**: Thm-S-04-02
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-S-04-01 -> Thm-S-04-01
- **元素**: Thm-S-04-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Def-S-04-01 -> Def-S-04-02 -> Def-S-04-03 -> Def-S-04-01
- **元素**: Def-S-04-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Def-S-04-01 -> Def-S-04-02 -> Def-S-04-01
- **元素**: Def-S-04-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Def-S-04-01 -> Def-S-04-01
- **元素**: Def-S-04-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Lemma-S-04-02 -> Lemma-S-04-02
- **元素**: Lemma-S-04-02
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-S-18-01 -> Thm-S-18-01
- **元素**: Thm-S-18-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-S-03-01 -> Thm-S-03-01
- **元素**: Thm-S-03-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-S-13-01 -> Def-S-13-01 -> Def-S-13-02 -> Def-S-13-03 -> Def-S-13-04 -> Thm-S-13-01
- **元素**: Thm-S-13-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-S-13-01 -> Def-S-13-01 -> Def-S-13-02 -> Def-S-13-03 -> Thm-S-13-01
- **元素**: Thm-S-13-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-S-13-01 -> Def-S-13-01 -> Def-S-13-02 -> Thm-S-13-01
- **元素**: Thm-S-13-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-S-13-01 -> Def-S-13-01 -> Thm-S-13-01
- **元素**: Thm-S-13-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Def-S-16-02 -> Def-S-16-03 -> Def-S-16-04 -> Def-S-16-02
- **元素**: Def-S-16-02
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Lemma-S-13-03 -> Lemma-S-13-03
- **元素**: Lemma-S-13-03
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Def-S-20-01 -> Def-S-20-01
- **元素**: Def-S-20-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-K-06-01 -> Def-K-06-07 -> Lemma-K-06-01 -> Def-K-06-02 -> Def-K-06-03 -> Def-K-06-04 -> Def-K-06-05 -> Def-K-06-06 -> Thm-K-06-01
- **元素**: Thm-K-06-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Def-K-06-07 -> Lemma-K-06-01 -> Def-K-06-02 -> Def-K-06-03 -> Def-K-06-04 -> Def-K-06-05 -> Def-K-06-06 -> Def-K-06-07
- **元素**: Def-K-06-07
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-K-06-01 -> Def-K-06-07 -> Lemma-K-06-01 -> Def-K-06-02 -> Def-K-06-03 -> Def-K-06-04 -> Def-K-06-05 -> Thm-K-06-01
- **元素**: Thm-K-06-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Def-K-06-07 -> Lemma-K-06-01 -> Def-K-06-02 -> Def-K-06-03 -> Def-K-06-04 -> Def-K-06-05 -> Def-K-06-07
- **元素**: Def-K-06-07
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-K-05-01 -> Def-K-05-05 -> Thm-K-05-03 -> Def-K-05-07 -> Def-K-05-08 -> Thm-K-05-04 -> Def-K-05-10 -> Def-K-05-11 -> Thm-K-05-05 -> Thm-K-05-01
- **元素**: Thm-K-05-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-K-05-05 -> Thm-K-05-05
- **元素**: Thm-K-05-05
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-K-05-01 -> Def-K-05-05 -> Thm-K-05-03 -> Def-K-05-07 -> Def-K-05-08 -> Thm-K-05-04 -> Def-K-05-10 -> Def-K-05-11 -> Thm-K-05-01
- **元素**: Thm-K-05-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-K-05-01 -> Def-K-05-05 -> Thm-K-05-03 -> Def-K-05-07 -> Def-K-05-08 -> Thm-K-05-04 -> Def-K-05-10 -> Thm-K-05-01
- **元素**: Thm-K-05-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

### 警告

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-01-04
- **元素**: Thm-S-17-01
- **建议**: 请检查依赖声明或创建 Def-S-01-04

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-02-03
- **元素**: Thm-S-17-01
- **建议**: 请检查依赖声明或创建 Def-S-02-03

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-01-03
- **元素**: Thm-S-12-01
- **建议**: 请检查依赖声明或创建 Def-S-01-03

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-03-02
- **元素**: Thm-S-12-01
- **建议**: 请检查依赖声明或创建 Def-S-03-02

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-05-01
- **元素**: Thm-S-12-01
- **建议**: 请检查依赖声明或创建 Def-S-05-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-02-03
- **元素**: Thm-S-13-01
- **建议**: 请检查依赖声明或创建 Def-S-02-03

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-05-02
- **元素**: Thm-S-14-01
- **建议**: 请检查依赖声明或创建 Def-S-05-02

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-02-03
- **元素**: Thm-S-14-01
- **建议**: 请检查依赖声明或创建 Def-S-02-03

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-01
- **元素**: Def-S-15-02
- **建议**: 请检查依赖声明或创建 Thm-S-15-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-01
- **元素**: Def-S-15-03
- **建议**: 请检查依赖声明或创建 Thm-S-15-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-02
- **元素**: Def-S-15-03
- **建议**: 请检查依赖声明或创建 Thm-S-15-02

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-01
- **元素**: Def-S-15-04
- **建议**: 请检查依赖声明或创建 Thm-S-15-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-02
- **元素**: Def-S-15-04
- **建议**: 请检查依赖声明或创建 Thm-S-15-02

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-01
- **元素**: Def-S-16-02
- **建议**: 请检查依赖声明或创建 Thm-S-16-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-01
- **元素**: Def-S-16-03
- **建议**: 请检查依赖声明或创建 Thm-S-16-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-01
- **元素**: Def-S-16-04
- **建议**: 请检查依赖声明或创建 Thm-S-16-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-06
- **元素**: Lemma-S-12-01
- **建议**: 请检查依赖声明或创建 Thm-S-12-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-03-05
- **元素**: Lemma-S-12-01
- **建议**: 请检查依赖声明或创建 Def-S-03-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-07
- **元素**: Lemma-S-12-01
- **建议**: 请检查依赖声明或创建 Thm-S-12-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-03-02
- **元素**: Lemma-S-12-01
- **建议**: 请检查依赖声明或创建 Thm-S-03-02

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-08
- **元素**: Lemma-S-12-01
- **建议**: 请检查依赖声明或创建 Thm-S-12-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-12-05
- **元素**: Lemma-S-12-01
- **建议**: 请检查依赖声明或创建 Def-S-12-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-09
- **元素**: Lemma-S-12-01
- **建议**: 请检查依赖声明或创建 Thm-S-12-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-03-04
- **元素**: Lemma-S-12-01
- **建议**: 请检查依赖声明或创建 Def-S-03-04

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-06
- **元素**: Lemma-S-12-02
- **建议**: 请检查依赖声明或创建 Thm-S-12-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-03-05
- **元素**: Lemma-S-12-02
- **建议**: 请检查依赖声明或创建 Def-S-03-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-07
- **元素**: Lemma-S-12-02
- **建议**: 请检查依赖声明或创建 Thm-S-12-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-03-02
- **元素**: Lemma-S-12-02
- **建议**: 请检查依赖声明或创建 Thm-S-03-02

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-08
- **元素**: Lemma-S-12-02
- **建议**: 请检查依赖声明或创建 Thm-S-12-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-12-05
- **元素**: Lemma-S-12-02
- **建议**: 请检查依赖声明或创建 Def-S-12-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-09
- **元素**: Lemma-S-12-02
- **建议**: 请检查依赖声明或创建 Thm-S-12-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-03-04
- **元素**: Lemma-S-12-02
- **建议**: 请检查依赖声明或创建 Def-S-03-04

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-10
- **元素**: Lemma-S-12-02
- **建议**: 请检查依赖声明或创建 Thm-S-12-10

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-06
- **元素**: Lemma-S-12-03
- **建议**: 请检查依赖声明或创建 Thm-S-12-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-03-05
- **元素**: Lemma-S-12-03
- **建议**: 请检查依赖声明或创建 Def-S-03-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-07
- **元素**: Lemma-S-12-03
- **建议**: 请检查依赖声明或创建 Thm-S-12-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-03-02
- **元素**: Lemma-S-12-03
- **建议**: 请检查依赖声明或创建 Thm-S-03-02

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-08
- **元素**: Lemma-S-12-03
- **建议**: 请检查依赖声明或创建 Thm-S-12-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-12-05
- **元素**: Lemma-S-12-03
- **建议**: 请检查依赖声明或创建 Def-S-12-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-09
- **元素**: Lemma-S-12-03
- **建议**: 请检查依赖声明或创建 Thm-S-12-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-03-04
- **元素**: Lemma-S-12-03
- **建议**: 请检查依赖声明或创建 Def-S-03-04

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-10
- **元素**: Lemma-S-12-03
- **建议**: 请检查依赖声明或创建 Thm-S-12-10

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-12-06
- **元素**: Lemma-S-12-03
- **建议**: 请检查依赖声明或创建 Def-S-12-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-06
- **元素**: Lemma-S-13-01
- **建议**: 请检查依赖声明或创建 Thm-S-13-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-13-05
- **元素**: Lemma-S-13-01
- **建议**: 请检查依赖声明或创建 Def-S-13-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-07
- **元素**: Lemma-S-13-01
- **建议**: 请检查依赖声明或创建 Thm-S-13-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-08
- **元素**: Lemma-S-13-01
- **建议**: 请检查依赖声明或创建 Thm-S-13-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-09
- **元素**: Lemma-S-13-01
- **建议**: 请检查依赖声明或创建 Thm-S-13-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-13-06
- **元素**: Lemma-S-13-01
- **建议**: 请检查依赖声明或创建 Def-S-13-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-10
- **元素**: Lemma-S-13-01
- **建议**: 请检查依赖声明或创建 Thm-S-13-10

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-06
- **元素**: Lemma-S-13-02
- **建议**: 请检查依赖声明或创建 Thm-S-13-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-13-05
- **元素**: Lemma-S-13-02
- **建议**: 请检查依赖声明或创建 Def-S-13-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-07
- **元素**: Lemma-S-13-02
- **建议**: 请检查依赖声明或创建 Thm-S-13-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-08
- **元素**: Lemma-S-13-02
- **建议**: 请检查依赖声明或创建 Thm-S-13-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-09
- **元素**: Lemma-S-13-02
- **建议**: 请检查依赖声明或创建 Thm-S-13-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-13-06
- **元素**: Lemma-S-13-02
- **建议**: 请检查依赖声明或创建 Def-S-13-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-10
- **元素**: Lemma-S-13-02
- **建议**: 请检查依赖声明或创建 Thm-S-13-10

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-13-07
- **元素**: Lemma-S-13-02
- **建议**: 请检查依赖声明或创建 Def-S-13-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-06
- **元素**: Lemma-S-13-03
- **建议**: 请检查依赖声明或创建 Thm-S-13-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-13-05
- **元素**: Lemma-S-13-03
- **建议**: 请检查依赖声明或创建 Def-S-13-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-07
- **元素**: Lemma-S-13-03
- **建议**: 请检查依赖声明或创建 Thm-S-13-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-08
- **元素**: Lemma-S-13-03
- **建议**: 请检查依赖声明或创建 Thm-S-13-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-09
- **元素**: Lemma-S-13-03
- **建议**: 请检查依赖声明或创建 Thm-S-13-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-13-06
- **元素**: Lemma-S-13-03
- **建议**: 请检查依赖声明或创建 Def-S-13-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-10
- **元素**: Lemma-S-13-03
- **建议**: 请检查依赖声明或创建 Thm-S-13-10

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-13-07
- **元素**: Lemma-S-13-03
- **建议**: 请检查依赖声明或创建 Def-S-13-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-05
- **元素**: Lemma-S-14-01
- **建议**: 请检查依赖声明或创建 Thm-S-14-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-14-04
- **元素**: Lemma-S-14-01
- **建议**: 请检查依赖声明或创建 Def-S-14-04

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-06
- **元素**: Lemma-S-14-01
- **建议**: 请检查依赖声明或创建 Thm-S-14-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-14-05
- **元素**: Lemma-S-14-01
- **建议**: 请检查依赖声明或创建 Def-S-14-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-07
- **元素**: Lemma-S-14-01
- **建议**: 请检查依赖声明或创建 Thm-S-14-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-14-06
- **元素**: Lemma-S-14-01
- **建议**: 请检查依赖声明或创建 Def-S-14-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-08
- **元素**: Lemma-S-14-01
- **建议**: 请检查依赖声明或创建 Thm-S-14-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-14-07
- **元素**: Lemma-S-14-01
- **建议**: 请检查依赖声明或创建 Def-S-14-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-05
- **元素**: Lemma-S-14-02
- **建议**: 请检查依赖声明或创建 Thm-S-14-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-14-04
- **元素**: Lemma-S-14-02
- **建议**: 请检查依赖声明或创建 Def-S-14-04

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-06
- **元素**: Lemma-S-14-02
- **建议**: 请检查依赖声明或创建 Thm-S-14-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-14-05
- **元素**: Lemma-S-14-02
- **建议**: 请检查依赖声明或创建 Def-S-14-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-07
- **元素**: Lemma-S-14-02
- **建议**: 请检查依赖声明或创建 Thm-S-14-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-14-06
- **元素**: Lemma-S-14-02
- **建议**: 请检查依赖声明或创建 Def-S-14-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-08
- **元素**: Lemma-S-14-02
- **建议**: 请检查依赖声明或创建 Thm-S-14-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-14-07
- **元素**: Lemma-S-14-02
- **建议**: 请检查依赖声明或创建 Def-S-14-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-09
- **元素**: Lemma-S-14-02
- **建议**: 请检查依赖声明或创建 Thm-S-14-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-06
- **元素**: Lemma-S-15-01
- **建议**: 请检查依赖声明或创建 Thm-S-15-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-15-05
- **元素**: Lemma-S-15-01
- **建议**: 请检查依赖声明或创建 Def-S-15-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-07
- **元素**: Lemma-S-15-01
- **建议**: 请检查依赖声明或创建 Thm-S-15-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-15-06
- **元素**: Lemma-S-15-01
- **建议**: 请检查依赖声明或创建 Def-S-15-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-08
- **元素**: Lemma-S-15-01
- **建议**: 请检查依赖声明或创建 Thm-S-15-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-15-07
- **元素**: Lemma-S-15-01
- **建议**: 请检查依赖声明或创建 Def-S-15-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-09
- **元素**: Lemma-S-15-01
- **建议**: 请检查依赖声明或创建 Thm-S-15-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-15-08
- **元素**: Lemma-S-15-01
- **建议**: 请检查依赖声明或创建 Def-S-15-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-10
- **元素**: Lemma-S-15-01
- **建议**: 请检查依赖声明或创建 Thm-S-15-10

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-06
- **元素**: Lemma-S-15-02
- **建议**: 请检查依赖声明或创建 Thm-S-15-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-15-05
- **元素**: Lemma-S-15-02
- **建议**: 请检查依赖声明或创建 Def-S-15-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-07
- **元素**: Lemma-S-15-02
- **建议**: 请检查依赖声明或创建 Thm-S-15-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-15-06
- **元素**: Lemma-S-15-02
- **建议**: 请检查依赖声明或创建 Def-S-15-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-08
- **元素**: Lemma-S-15-02
- **建议**: 请检查依赖声明或创建 Thm-S-15-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-15-07
- **元素**: Lemma-S-15-02
- **建议**: 请检查依赖声明或创建 Def-S-15-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-09
- **元素**: Lemma-S-15-02
- **建议**: 请检查依赖声明或创建 Thm-S-15-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-15-08
- **元素**: Lemma-S-15-02
- **建议**: 请检查依赖声明或创建 Def-S-15-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-10
- **元素**: Lemma-S-15-02
- **建议**: 请检查依赖声明或创建 Thm-S-15-10

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-15-09
- **元素**: Lemma-S-15-02
- **建议**: 请检查依赖声明或创建 Def-S-15-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-06
- **元素**: Lemma-S-16-01
- **建议**: 请检查依赖声明或创建 Thm-S-16-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-16-05
- **元素**: Lemma-S-16-01
- **建议**: 请检查依赖声明或创建 Def-S-16-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-07
- **元素**: Lemma-S-16-01
- **建议**: 请检查依赖声明或创建 Thm-S-16-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-16-06
- **元素**: Lemma-S-16-01
- **建议**: 请检查依赖声明或创建 Def-S-16-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-08
- **元素**: Lemma-S-16-01
- **建议**: 请检查依赖声明或创建 Thm-S-16-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-16-07
- **元素**: Lemma-S-16-01
- **建议**: 请检查依赖声明或创建 Def-S-16-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-09
- **元素**: Lemma-S-16-01
- **建议**: 请检查依赖声明或创建 Thm-S-16-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-16-08
- **元素**: Lemma-S-16-01
- **建议**: 请检查依赖声明或创建 Def-S-16-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-10
- **元素**: Lemma-S-16-01
- **建议**: 请检查依赖声明或创建 Thm-S-16-10

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-06
- **元素**: Lemma-S-16-02
- **建议**: 请检查依赖声明或创建 Thm-S-16-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-16-05
- **元素**: Lemma-S-16-02
- **建议**: 请检查依赖声明或创建 Def-S-16-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-07
- **元素**: Lemma-S-16-02
- **建议**: 请检查依赖声明或创建 Thm-S-16-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-16-06
- **元素**: Lemma-S-16-02
- **建议**: 请检查依赖声明或创建 Def-S-16-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-08
- **元素**: Lemma-S-16-02
- **建议**: 请检查依赖声明或创建 Thm-S-16-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-16-07
- **元素**: Lemma-S-16-02
- **建议**: 请检查依赖声明或创建 Def-S-16-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-09
- **元素**: Lemma-S-16-02
- **建议**: 请检查依赖声明或创建 Thm-S-16-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-16-08
- **元素**: Lemma-S-16-02
- **建议**: 请检查依赖声明或创建 Def-S-16-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-10
- **元素**: Lemma-S-16-02
- **建议**: 请检查依赖声明或创建 Thm-S-16-10

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-16-09
- **元素**: Lemma-S-16-02
- **建议**: 请检查依赖声明或创建 Def-S-16-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-05
- **元素**: Cor-S-14-01
- **建议**: 请检查依赖声明或创建 Thm-S-14-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-14-04
- **元素**: Cor-S-14-01
- **建议**: 请检查依赖声明或创建 Def-S-14-04

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-06
- **元素**: Cor-S-14-01
- **建议**: 请检查依赖声明或创建 Thm-S-14-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-14-05
- **元素**: Cor-S-14-01
- **建议**: 请检查依赖声明或创建 Def-S-14-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-07
- **元素**: Cor-S-14-01
- **建议**: 请检查依赖声明或创建 Thm-S-14-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-14-06
- **元素**: Cor-S-14-01
- **建议**: 请检查依赖声明或创建 Def-S-14-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-08
- **元素**: Cor-S-14-01
- **建议**: 请检查依赖声明或创建 Thm-S-14-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-14-07
- **元素**: Cor-S-14-01
- **建议**: 请检查依赖声明或创建 Def-S-14-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-09
- **元素**: Cor-S-14-01
- **建议**: 请检查依赖声明或创建 Thm-S-14-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-08-03
- **元素**: Cor-S-14-01
- **建议**: 请检查依赖声明或创建 Thm-S-08-03

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Lemma-S-04-01
- **元素**: Lemma-S-04-02
- **建议**: 请检查依赖声明或创建 Lemma-S-04-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-K-05-12
- **元素**: Thm-K-05-05
- **建议**: 请检查依赖声明或创建 Def-K-05-12

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Prop-K-05-01
- **元素**: Thm-K-05-05
- **建议**: 请检查依赖声明或创建 Prop-K-05-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Prop-K-05-13
- **元素**: Thm-K-05-05
- **建议**: 请检查依赖声明或创建 Prop-K-05-13

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-K-05-12
- **元素**: Def-K-05-10
- **建议**: 请检查依赖声明或创建 Def-K-05-12

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Prop-K-05-01
- **元素**: Def-K-05-10
- **建议**: 请检查依赖声明或创建 Prop-K-05-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Prop-K-05-13
- **元素**: Def-K-05-10
- **建议**: 请检查依赖声明或创建 Prop-K-05-13

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-K-05-12
- **元素**: Def-K-05-11
- **建议**: 请检查依赖声明或创建 Def-K-05-12

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Prop-K-05-01
- **元素**: Def-K-05-11
- **建议**: 请检查依赖声明或创建 Prop-K-05-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Prop-K-05-13
- **元素**: Def-K-05-11
- **建议**: 请检查依赖声明或创建 Prop-K-05-13

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-F-15-06
- **元素**: Def-F-15-05
- **建议**: 请检查依赖声明或创建 Def-F-15-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Lemma-F-15-01
- **元素**: Def-F-15-14
- **建议**: 请检查依赖声明或创建 Lemma-F-15-01

### 信息

- 孤立元素: Thm-S-02-08 - (CALM定理 — Consistency As Logical Monotonicity):
- 孤立元素: Lemma-S-18-01 - （Source 可重放引理），可重放 Source 保证故障恢复后从最后一个成功 Checkpoint $C_n$ 的偏移量重放。因此所有在 $C_n$ 之后到达的记录都会被重新处理。不存在记录被永久
- 孤立元素: Lemma-S-18-02 - ，Sink 不会重新提交 $T_n$（或即使重新提交，幂等 commit 保证无重复效果）
- 孤立元素: Thm-K-03-02 - 给定Netflix业务负载特征，Keystone平台满足：
- 孤立元素: Def-K-06-190 - [边缘流处理]: 边缘流处理是指在数据源产生地或其邻近的计算节点上，对连续到达的数据流进行实时处理、过滤、聚合和推理的计算范式。形式上，边缘流处理系统可建模为六元组：
- 孤立元素: Def-K-06-195 - [边缘运维自动化]: 边缘运维复杂度随节点数 $N$ 呈亚线性增长：
- 孤立元素: Thm-K-06-40 - (实时多模态的必要性定理): 在以下应用场景中，多模态处理的延迟约束是刚性需求：
- 孤立元素: Prop-K-06-41 - (异步推理模式): 为避免模型推理阻塞数据流，采用AsyncFunction模式：
- 孤立元素: Thm-K-06-03 - (一致性模型蕴含关系). 设：
- 孤立元素: Def-K-06-01 - (RisingWave 系统架构). RisingWave 是一个分布式流处理数据库系统，其架构可形式化定义为五元组：
- 孤立元素: Thm-K-06-115 - (视图选择NP完全性). 给定查询工作负载 $\mathcal{Q}$ 和物化视图候选集 $\mathcal{C}$，在满足存储约束 $S_{budget}$ 的前提下最大化查询性能提升的视图选择问题
- 孤立元素: Thm-K-07-01 - 对于流处理作业 $J$，测试套件 $S$ 达到完全覆盖当且仅当：
- 孤立元素: Thm-K-10-223 - (CEP检测完备性): 对于给定的CEP模式集合 $\mathcal{P}$，Flink CEP引擎能够检测所有满足模式约束的事件序列。
- 孤立元素: Thm-K-10-213 - (负荷预测准确性): 基于LSTM的短期负荷预测模型在典型场景下 MAPE < 3%。
- 孤立元素: Thm-F-02-40 - (中间结果爆炸定理): 对于 $n$ 路Join，若各流记录独立到达且匹配概率为 $p$，第 $k$ 层中间流的期望大小为：
- 孤立元素: Def-F-02-54 - (MultiJoin支持矩阵):
- 孤立元素: Lemma-F-02-01 - 的工程实现：尽管 DAG 中不同分支进度不同，但每个节点本地的 Watermark 序列都保持单调不减。
- 孤立元素: Thm-F-07-71 - (实时性价值定理): 设问题发生时刻为 $t_0$，发现时刻为 $t_d$，修复时刻为 $t_f$，则损失函数满足：
- 孤立元素: Def-F-07-01 - (实时推荐系统 Real-time Recommendation System): 实时推荐系统是一个五元组 $\mathcal{R} = (\mathcal{U}, \mathcal{I}, \ma
- 孤立元素: Def-F-07-02 - (实时协同过滤 Real-time Collaborative Filtering): 基于隐语义模型的实时协同过滤定义为：
- ... 还有 34 个信息项

---

*报告由 Theorem Dependency Validator 自动生成*
