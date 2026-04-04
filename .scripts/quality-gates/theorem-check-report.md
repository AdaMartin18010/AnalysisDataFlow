# 定理注册表检查报告

> **生成时间**: 2026-04-04 16:02:51
> **检查版本**: v1.2.0
> **项目根目录**: E:\_src\AnalysisDataFlow

---

## 执行摘要

| 指标 | 数值 |
|------|------|
| 总形式化元素（含引用） | 4879 |
| 定义（非引用） | 2174 |
| 错误数 | 540 |
| 警告数 | 1049 |
| 注册表条目 | 2270 |

### 按类型统计（仅定义）

| 类型 | 数量 | 说明 |
|------|------|------|
| Cor | 6 | 推论 |
| Def | 1105 | 定义 |
| Lemma | 344 | 引理 |
| Prop | 431 | 命题 |
| Thm | 288 | 定理 |

### 按阶段统计（仅定义）

| 阶段 | 数量 | 说明 |
|------|------|------|
| F | 1283 | Flink |
| K | 516 | Knowledge |
| S | 375 | Struct |

---

## ❌ 错误详情 (540)

### 1. duplicate_id

- **编号**: `Def-S-03-01`
- **文件**: N/A
- **消息**: 编号 Def-S-03-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\01-foundation\01.03-actor-model-formalization.md:45`
  - `Knowledge\05-mapping-guides\struct-to-flink-mapping.md:429`

### 2. duplicate_id

- **编号**: `Def-S-03-05`
- **文件**: N/A
- **消息**: 编号 Def-S-03-05 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\01-foundation\01.03-actor-model-formalization.md:154`
  - `Knowledge\05-mapping-guides\struct-to-flink-mapping.md:467`

### 3. duplicate_id

- **编号**: `Def-S-04-01`
- **文件**: N/A
- **消息**: 编号 Def-S-04-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\01-foundation\01.04-dataflow-model-formalization.md:44`
  - `Knowledge\05-mapping-guides\struct-to-flink-mapping.md:187`

### 4. duplicate_id

- **编号**: `Def-S-04-04`
- **文件**: N/A
- **消息**: 编号 Def-S-04-04 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\01-foundation\01.04-dataflow-model-formalization.md:138`
  - `Knowledge\05-mapping-guides\struct-to-flink-mapping.md:241`

### 5. duplicate_id

- **编号**: `Def-S-04-05`
- **文件**: N/A
- **消息**: 编号 Def-S-04-05 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\01-foundation\01.04-dataflow-model-formalization.md:175`
  - `Knowledge\02-design-patterns\pattern-windowed-aggregation.md:277`

### 6. duplicate_id

- **编号**: `Lemma-S-04-02`
- **文件**: N/A
- **消息**: 编号 Lemma-S-04-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\01-foundation\01.04-dataflow-model-formalization.md:235`
  - `Knowledge\05-mapping-guides\struct-to-flink-mapping.md:241`

### 7. duplicate_id

- **编号**: `Lemma-S-06-01`
- **文件**: N/A
- **消息**: 编号 Lemma-S-06-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\01-foundation\01.06-petri-net-formalization.md:406`
  - `Struct\06-frontier\first-person-choreographies.md:99`

### 8. duplicate_id

- **编号**: `Lemma-S-06-02`
- **文件**: N/A
- **消息**: 编号 Lemma-S-06-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\01-foundation\01.06-petri-net-formalization.md:419`
  - `Struct\06-frontier\first-person-choreographies.md:125`

### 9. duplicate_id

- **编号**: `Thm-S-06-01`
- **文件**: N/A
- **消息**: 编号 Thm-S-06-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Struct\01-foundation\01.06-petri-net-formalization.md:453`
  - `Struct\06-frontier\06.04-pdot-path-dependent-types.md:458`
  - `Struct\06-frontier\first-person-choreographies.md:266`

### 10. duplicate_id

- **编号**: `Def-S-07-01`
- **文件**: N/A
- **消息**: 编号 Def-S-07-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\02-properties\02.01-determinism-in-streaming.md:48`
  - `Struct\07-tools\tla-for-flink.md:7`

### 11. duplicate_id

- **编号**: `Def-S-07-02`
- **文件**: N/A
- **消息**: 编号 Def-S-07-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\02-properties\02.01-determinism-in-streaming.md:79`
  - `Struct\07-tools\tla-for-flink.md:28`

### 12. duplicate_id

- **编号**: `Def-S-07-03`
- **文件**: N/A
- **消息**: 编号 Def-S-07-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\02-properties\02.01-determinism-in-streaming.md:109`
  - `Struct\07-tools\tla-for-flink.md:55`

### 13. duplicate_id

- **编号**: `Def-S-07-04`
- **文件**: N/A
- **消息**: 编号 Def-S-07-04 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\02-properties\02.01-determinism-in-streaming.md:136`
  - `Struct\07-tools\tla-for-flink.md:87`

### 14. duplicate_id

- **编号**: `Lemma-S-07-01`
- **文件**: N/A
- **消息**: 编号 Lemma-S-07-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Struct\02-properties\02.01-determinism-in-streaming.md:160`
  - `Struct\07-tools\model-checking-practice.md:62`
  - `Struct\07-tools\tla-for-flink.md:116`

### 15. duplicate_id

- **编号**: `Lemma-S-07-02`
- **文件**: N/A
- **消息**: 编号 Lemma-S-07-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\02-properties\02.01-determinism-in-streaming.md:175`
  - `Struct\07-tools\model-checking-practice.md:73`

### 16. duplicate_id

- **编号**: `Lemma-S-07-04`
- **文件**: N/A
- **消息**: 编号 Lemma-S-07-04 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\02-properties\02.01-determinism-in-streaming.md:203`
  - `Struct\07-tools\coq-mechanization.md:163`

### 17. duplicate_id

- **编号**: `Thm-S-07-01`
- **文件**: N/A
- **消息**: 编号 Thm-S-07-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\02-properties\02.01-determinism-in-streaming.md:326`
  - `Struct\07-tools\tla-for-flink.md:280`

### 18. duplicate_id

- **编号**: `Def-S-08-01`
- **文件**: N/A
- **消息**: 编号 Def-S-08-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\02-properties\02.02-consistency-hierarchy.md:57`
  - `Struct\08-standards\streaming-sql-standard.md:7`

### 19. duplicate_id

- **编号**: `Def-S-08-02`
- **文件**: N/A
- **消息**: 编号 Def-S-08-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\02-properties\02.02-consistency-hierarchy.md:85`
  - `Struct\08-standards\streaming-sql-standard.md:36`

### 20. duplicate_id

- **编号**: `Def-S-08-03`
- **文件**: N/A
- **消息**: 编号 Def-S-08-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\02-properties\02.02-consistency-hierarchy.md:107`
  - `Struct\08-standards\streaming-sql-standard.md:66`

### 21. duplicate_id

- **编号**: `Lemma-S-08-01`
- **文件**: N/A
- **消息**: 编号 Lemma-S-08-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\02-properties\02.02-consistency-hierarchy.md:221`
  - `Struct\08-standards\streaming-sql-standard.md:103`

### 22. duplicate_id

- **编号**: `Lemma-S-08-02`
- **文件**: N/A
- **消息**: 编号 Lemma-S-08-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\02-properties\02.02-consistency-hierarchy.md:245`
  - `Struct\08-standards\streaming-sql-standard.md:115`

### 23. duplicate_id

- **编号**: `Prop-S-08-01`
- **文件**: N/A
- **消息**: 编号 Prop-S-08-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\02-properties\02.02-consistency-hierarchy.md:348`
  - `Struct\08-standards\streaming-sql-standard.md:127`

### 24. duplicate_id

- **编号**: `Lemma-S-09-01`
- **文件**: N/A
- **消息**: 编号 Lemma-S-09-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\02-properties\02.03-watermark-monotonicity.md:125`
  - `Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:578`

### 25. duplicate_id

- **编号**: `Thm-S-09-01`
- **文件**: N/A
- **消息**: 编号 Thm-S-09-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Struct\02-properties\02.03-watermark-monotonicity.md:210`
  - `Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:468`
  - `Struct\06-frontier\06.01-open-problems-streaming-verification.md:452`

### 26. duplicate_id

- **编号**: `Thm-S-11-01`
- **文件**: N/A
- **消息**: 编号 Thm-S-11-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Struct\02-properties\02.05-type-safety-derivation.md:771`
  - `Knowledge\05-mapping-guides\struct-to-flink-mapping.md:481`
  - `Flink\09-language-foundations\01.03-scala3-type-system-formalization.md:311`

### 27. duplicate_id

- **编号**: `Def-S-17-01`
- **文件**: N/A
- **消息**: 编号 Def-S-17-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\04-proofs\04.01-flink-checkpoint-correctness.md:51`
  - `Knowledge\05-mapping-guides\struct-to-flink-mapping.md:284`

### 28. duplicate_id

- **编号**: `Def-S-17-02`
- **文件**: N/A
- **消息**: 编号 Def-S-17-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\04-proofs\04.01-flink-checkpoint-correctness.md:79`
  - `Struct\04-proofs\04.01-flink-checkpoint-correctness.md:811`
  - `Knowledge\05-mapping-guides\struct-to-flink-mapping.md:332`

### 29. duplicate_id

- **编号**: `Thm-S-17-01`
- **文件**: N/A
- **消息**: 编号 Thm-S-17-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\04-proofs\04.01-flink-checkpoint-correctness.md:657`
  - `Knowledge\02-design-patterns\pattern-checkpoint-recovery.md:441`
  - `Knowledge\02-design-patterns\pattern-checkpoint-recovery.md:445`

### 30. duplicate_id

- **编号**: `Def-S-18-01`
- **文件**: N/A
- **消息**: 编号 Def-S-18-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\04-proofs\04.02-flink-exactly-once-correctness.md:76`
  - `Knowledge\05-mapping-guides\struct-to-flink-mapping.md:374`

### 31. duplicate_id

- **编号**: `Thm-S-18-01`
- **文件**: N/A
- **消息**: 编号 Thm-S-18-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\04-proofs\04.02-flink-exactly-once-correctness.md:391`
  - `Knowledge\02-design-patterns\pattern-checkpoint-recovery.md:464`
  - `Knowledge\02-design-patterns\pattern-checkpoint-recovery.md:468`

### 32. duplicate_id

- **编号**: `Def-S-20-01`
- **文件**: N/A
- **消息**: 编号 Def-S-20-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:52`
  - `Struct\06-frontier\06.02-choreographic-streaming-programming.md:69`

### 33. duplicate_id

- **编号**: `Def-S-20-02`
- **文件**: N/A
- **消息**: 编号 Def-S-20-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:87`
  - `Struct\06-frontier\06.02-choreographic-streaming-programming.md:115`

### 34. duplicate_id

- **编号**: `Def-S-20-03`
- **文件**: N/A
- **消息**: 编号 Def-S-20-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:120`
  - `Struct\06-frontier\06.02-choreographic-streaming-programming.md:176`

### 35. duplicate_id

- **编号**: `Def-S-20-04`
- **文件**: N/A
- **消息**: 编号 Def-S-20-04 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:162`
  - `Struct\06-frontier\06.02-choreographic-streaming-programming.md:210`

### 36. duplicate_id

- **编号**: `Def-S-20-05`
- **文件**: N/A
- **消息**: 编号 Def-S-20-05 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:214`
  - `Struct\06-frontier\06.02-choreographic-streaming-programming.md:244`

### 37. duplicate_id

- **编号**: `Lemma-S-20-01`
- **文件**: N/A
- **消息**: 编号 Lemma-S-20-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:252`
  - `Struct\06-frontier\06.02-choreographic-streaming-programming.md:332`

### 38. duplicate_id

- **编号**: `Lemma-S-20-02`
- **文件**: N/A
- **消息**: 编号 Lemma-S-20-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:312`
  - `Struct\06-frontier\06.02-choreographic-streaming-programming.md:358`

### 39. duplicate_id

- **编号**: `Lemma-S-20-03`
- **文件**: N/A
- **消息**: 编号 Lemma-S-20-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:364`
  - `Struct\06-frontier\06.02-choreographic-streaming-programming.md:376`

### 40. duplicate_id

- **编号**: `Lemma-S-20-04`
- **文件**: N/A
- **消息**: 编号 Lemma-S-20-04 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:397`
  - `Struct\06-frontier\06.02-choreographic-streaming-programming.md:396`

### 41. duplicate_id

- **编号**: `Thm-S-20-01`
- **文件**: N/A
- **消息**: 编号 Thm-S-20-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\04-proofs\04.04-watermark-algebra-formal-proof.md:810`
  - `Struct\06-frontier\06.02-choreographic-streaming-programming.md:782`

### 42. duplicate_id

- **编号**: `Def-S-23-03`
- **文件**: N/A
- **消息**: 编号 Def-S-23-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\04-proofs\04.07-deadlock-freedom-choreographic.md:130`
  - `Struct\06-frontier\06.03-ai-agent-session-types.md:836`

### 43. duplicate_id

- **编号**: `Def-S-25-01`
- **文件**: N/A
- **消息**: 编号 Def-S-25-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\05-comparative-analysis\05.02-expressiveness-vs-decidability.md:56`
  - `Struct\06-frontier\06.01-open-problems-streaming-verification.md:52`

### 44. duplicate_id

- **编号**: `Def-S-25-02`
- **文件**: N/A
- **消息**: 编号 Def-S-25-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\05-comparative-analysis\05.02-expressiveness-vs-decidability.md:77`
  - `Struct\06-frontier\06.01-open-problems-streaming-verification.md:85`

### 45. duplicate_id

- **编号**: `Def-S-25-03`
- **文件**: N/A
- **消息**: 编号 Def-S-25-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\05-comparative-analysis\05.02-expressiveness-vs-decidability.md:97`
  - `Struct\06-frontier\06.01-open-problems-streaming-verification.md:110`

### 46. duplicate_id

- **编号**: `Def-S-25-04`
- **文件**: N/A
- **消息**: 编号 Def-S-25-04 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\05-comparative-analysis\05.02-expressiveness-vs-decidability.md:115`
  - `Struct\06-frontier\06.01-open-problems-streaming-verification.md:139`

### 47. duplicate_id

- **编号**: `Prop-S-25-01`
- **文件**: N/A
- **消息**: 编号 Prop-S-25-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\05-comparative-analysis\05.02-expressiveness-vs-decidability.md:140`
  - `Struct\06-frontier\06.01-open-problems-streaming-verification.md:218`

### 48. duplicate_id

- **编号**: `Def-S-06-10`
- **文件**: N/A
- **消息**: 编号 Def-S-06-10 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\06-frontier\06.04-pdot-path-dependent-types.md:147`
  - `Struct\06-frontier\first-person-choreographies.md:7`

### 49. duplicate_id

- **编号**: `Prop-S-07-03`
- **文件**: N/A
- **消息**: 编号 Prop-S-07-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\07-tools\coq-mechanization.md:145`
  - `Struct\07-tools\tla-for-flink.md:156`

### 50. duplicate_id

- **编号**: `Prop-S-07-01`
- **文件**: N/A
- **消息**: 编号 Prop-S-07-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Struct\07-tools\model-checking-practice.md:79`
  - `Struct\07-tools\tla-for-flink.md:134`

### 51. duplicate_id

- **编号**: `Def-K-01-01`
- **文件**: N/A
- **消息**: 编号 Def-K-01-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\01-concept-atlas\concurrency-paradigms-matrix.md:108`
  - `Knowledge\01-concept-atlas\streaming-models-mindmap.md:50`
  - `Knowledge\98-exercises\exercise-01-process-calculus.md:37`

### 52. duplicate_id

- **编号**: `Def-K-01-02`
- **文件**: N/A
- **消息**: 编号 Def-K-01-02 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\01-concept-atlas\concurrency-paradigms-matrix.md:127`
  - `Knowledge\01-concept-atlas\streaming-models-mindmap.md:60`
  - `Knowledge\98-exercises\exercise-01-process-calculus.md:38`

### 53. duplicate_id

- **编号**: `Def-K-01-03`
- **文件**: N/A
- **消息**: 编号 Def-K-01-03 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\01-concept-atlas\concurrency-paradigms-matrix.md:148`
  - `Knowledge\01-concept-atlas\streaming-models-mindmap.md:77`
  - `Knowledge\98-exercises\exercise-01-process-calculus.md:39`

### 54. duplicate_id

- **编号**: `Def-K-01-04`
- **文件**: N/A
- **消息**: 编号 Def-K-01-04 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\01-concept-atlas\concurrency-paradigms-matrix.md:169`
  - `Knowledge\01-concept-atlas\streaming-models-mindmap.md:87`
  - `Knowledge\98-exercises\exercise-01-process-calculus.md:40`

### 55. duplicate_id

- **编号**: `Def-K-01-05`
- **文件**: N/A
- **消息**: 编号 Def-K-01-05 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\01-concept-atlas\concurrency-paradigms-matrix.md:190`
  - `Knowledge\01-concept-atlas\streaming-models-mindmap.md:97`

### 56. duplicate_id

- **编号**: `Def-K-01-06`
- **文件**: N/A
- **消息**: 编号 Def-K-01-06 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\01-concept-atlas\concurrency-paradigms-matrix.md:228`
  - `Knowledge\01-concept-atlas\streaming-models-mindmap.md:105`

### 57. duplicate_id

- **编号**: `Def-K-01-07`
- **文件**: N/A
- **消息**: 编号 Def-K-01-07 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\01-concept-atlas\concurrency-paradigms-matrix.md:237`
  - `Knowledge\01-concept-atlas\streaming-models-mindmap.md:113`

### 58. duplicate_id

- **编号**: `Prop-K-01-01`
- **文件**: N/A
- **消息**: 编号 Prop-K-01-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\01-concept-atlas\concurrency-paradigms-matrix.md:281`
  - `Knowledge\01-concept-atlas\streaming-models-mindmap.md:123`

### 59. duplicate_id

- **编号**: `Prop-K-01-02`
- **文件**: N/A
- **消息**: 编号 Prop-K-01-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\01-concept-atlas\concurrency-paradigms-matrix.md:292`
  - `Knowledge\01-concept-atlas\streaming-models-mindmap.md:133`

### 60. duplicate_id

- **编号**: `Prop-K-01-03`
- **文件**: N/A
- **消息**: 编号 Prop-K-01-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\01-concept-atlas\concurrency-paradigms-matrix.md:303`
  - `Knowledge\01-concept-atlas\streaming-models-mindmap.md:143`

### 61. duplicate_id

- **编号**: `Def-K-02-05`
- **文件**: N/A
- **消息**: 编号 Def-K-02-05 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\02-design-patterns\pattern-async-io-enrichment.md:46`
  - `Knowledge\02-design-patterns\pattern-windowed-aggregation.md:204`

### 62. duplicate_id

- **编号**: `Def-K-02-06`
- **文件**: N/A
- **消息**: 编号 Def-K-02-06 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\02-design-patterns\pattern-async-io-enrichment.md:72`
  - `Knowledge\02-design-patterns\pattern-side-output.md:53`

### 63. duplicate_id

- **编号**: `Def-K-02-07`
- **文件**: N/A
- **消息**: 编号 Def-K-02-07 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\02-design-patterns\pattern-async-io-enrichment.md:96`
  - `Knowledge\02-design-patterns\pattern-side-output.md:73`

### 64. duplicate_id

- **编号**: `Def-K-02-08`
- **文件**: N/A
- **消息**: 编号 Def-K-02-08 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\02-design-patterns\pattern-async-io-enrichment.md:117`
  - `Knowledge\02-design-patterns\pattern-side-output.md:101`

### 65. duplicate_id

- **编号**: `Prop-K-02-01`
- **文件**: N/A
- **消息**: 编号 Prop-K-02-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\02-design-patterns\pattern-async-io-enrichment.md:137`
  - `Knowledge\02-design-patterns\pattern-windowed-aggregation.md:237`

### 66. duplicate_id

- **编号**: `Prop-K-02-02`
- **文件**: N/A
- **消息**: 编号 Prop-K-02-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\02-design-patterns\pattern-async-io-enrichment.md:160`
  - `Knowledge\02-design-patterns\pattern-windowed-aggregation.md:252`

### 67. duplicate_id

- **编号**: `Prop-K-02-03`
- **文件**: N/A
- **消息**: 编号 Prop-K-02-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\02-design-patterns\pattern-log-analysis.md:165`
  - `Knowledge\02-design-patterns\pattern-side-output.md:447`

### 68. duplicate_id

- **编号**: `Lemma-K-02-04`
- **文件**: N/A
- **消息**: 编号 Lemma-K-02-04 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\02-design-patterns\pattern-realtime-feature-engineering.md:65`
  - `Knowledge\02-design-patterns\pattern-side-output.md:152`

### 69. duplicate_id

- **编号**: `Lemma-K-02-05`
- **文件**: N/A
- **消息**: 编号 Lemma-K-02-05 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\02-design-patterns\pattern-realtime-feature-engineering.md:73`
  - `Knowledge\02-design-patterns\pattern-side-output.md:172`

### 70. duplicate_id

- **编号**: `Lemma-K-02-06`
- **文件**: N/A
- **消息**: 编号 Lemma-K-02-06 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\02-design-patterns\pattern-realtime-feature-engineering.md:81`
  - `Knowledge\02-design-patterns\pattern-side-output.md:192`

### 71. duplicate_id

- **编号**: `Def-K-02-01`
- **文件**: N/A
- **消息**: 编号 Def-K-02-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\02-design-patterns\pattern-windowed-aggregation.md:52`
  - `Knowledge\98-exercises\exercise-02-flink-basics.md:40`

### 72. duplicate_id

- **编号**: `Def-K-02-02`
- **文件**: N/A
- **消息**: 编号 Def-K-02-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\02-design-patterns\pattern-windowed-aggregation.md:78`
  - `Knowledge\98-exercises\exercise-02-flink-basics.md:41`

### 73. duplicate_id

- **编号**: `Def-K-02-03`
- **文件**: N/A
- **消息**: 编号 Def-K-02-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\02-design-patterns\pattern-windowed-aggregation.md:136`
  - `Knowledge\98-exercises\exercise-02-flink-basics.md:42`

### 74. duplicate_id

- **编号**: `Def-K-02-04`
- **文件**: N/A
- **消息**: 编号 Def-K-02-04 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\02-design-patterns\pattern-windowed-aggregation.md:164`
  - `Knowledge\98-exercises\exercise-02-flink-basics.md:43`

### 75. duplicate_id

- **编号**: `Lemma-K-03-04`
- **文件**: N/A
- **消息**: 编号 Lemma-K-03-04 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\03-business-patterns\airbnb-marketplace-dynamics.md:254`
  - `Knowledge\03-business-patterns\gaming-analytics.md:190`

### 76. duplicate_id

- **编号**: `Def-K-03-03`
- **文件**: N/A
- **消息**: 编号 Def-K-03-03 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Knowledge\03-business-patterns\gaming-analytics.md:47`
  - `Knowledge\03-business-patterns\iot-stream-processing.md:102`
  - `Knowledge\03-business-patterns\real-time-recommendation.md:88`
  - `Knowledge\98-exercises\exercise-03-checkpoint-analysis.md:41`

### 77. duplicate_id

- **编号**: `Def-K-03-04`
- **文件**: N/A
- **消息**: 编号 Def-K-03-04 在多个文件中重复定义 (5 个文件)
- **位置**:
  - `Knowledge\03-business-patterns\gaming-analytics.md:93`
  - `Knowledge\03-business-patterns\iot-stream-processing.md:118`
  - `Knowledge\03-business-patterns\log-monitoring.md:40`
  - `Knowledge\03-business-patterns\real-time-recommendation.md:131`
  - `Knowledge\98-exercises\exercise-03-checkpoint-analysis.md:42`

### 78. duplicate_id

- **编号**: `Def-K-03-05`
- **文件**: N/A
- **消息**: 编号 Def-K-03-05 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Knowledge\03-business-patterns\gaming-analytics.md:116`
  - `Knowledge\03-business-patterns\log-monitoring.md:72`
  - `Knowledge\03-business-patterns\real-time-recommendation.md:159`
  - `Knowledge\03-business-patterns\uber-realtime-platform.md:44`

### 79. duplicate_id

- **编号**: `Def-K-03-06`
- **文件**: N/A
- **消息**: 编号 Def-K-03-06 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\03-business-patterns\gaming-analytics.md:148`
  - `Knowledge\03-business-patterns\log-monitoring.md:103`
  - `Knowledge\03-business-patterns\uber-realtime-platform.md:95`

### 80. duplicate_id

- **编号**: `Lemma-K-03-03`
- **文件**: N/A
- **消息**: 编号 Lemma-K-03-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\03-business-patterns\gaming-analytics.md:168`
  - `Knowledge\03-business-patterns\spotify-music-recommendation.md:229`

### 81. duplicate_id

- **编号**: `Prop-K-03-03`
- **文件**: N/A
- **消息**: 编号 Prop-K-03-03 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Knowledge\03-business-patterns\gaming-analytics.md:216`
  - `Knowledge\03-business-patterns\iot-stream-processing.md:174`
  - `Knowledge\03-business-patterns\netflix-streaming-pipeline.md:119`
  - `Knowledge\03-business-patterns\real-time-recommendation.md:269`

### 82. duplicate_id

- **编号**: `Def-K-03-01`
- **文件**: N/A
- **消息**: 编号 Def-K-03-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\03-business-patterns\iot-stream-processing.md:56`
  - `Knowledge\98-exercises\exercise-03-checkpoint-analysis.md:39`

### 83. duplicate_id

- **编号**: `Def-K-03-02`
- **文件**: N/A
- **消息**: 编号 Def-K-03-02 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\03-business-patterns\iot-stream-processing.md:82`
  - `Knowledge\03-business-patterns\real-time-recommendation.md:56`
  - `Knowledge\98-exercises\exercise-03-checkpoint-analysis.md:40`

### 84. duplicate_id

- **编号**: `Prop-K-03-01`
- **文件**: N/A
- **消息**: 编号 Prop-K-03-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\03-business-patterns\iot-stream-processing.md:142`
  - `Knowledge\03-business-patterns\real-time-recommendation.md:204`
  - `Knowledge\03-business-patterns\uber-realtime-platform.md:184`

### 85. duplicate_id

- **编号**: `Prop-K-03-02`
- **文件**: N/A
- **消息**: 编号 Prop-K-03-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\03-business-patterns\iot-stream-processing.md:158`
  - `Knowledge\03-business-patterns\real-time-recommendation.md:224`

### 86. duplicate_id

- **编号**: `Prop-K-03-04`
- **文件**: N/A
- **消息**: 编号 Prop-K-03-04 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\03-business-patterns\iot-stream-processing.md:190`
  - `Knowledge\03-business-patterns\log-monitoring.md:125`
  - `Knowledge\03-business-patterns\netflix-streaming-pipeline.md:134`

### 87. duplicate_id

- **编号**: `Prop-K-03-05`
- **文件**: N/A
- **消息**: 编号 Prop-K-03-05 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\03-business-patterns\log-monitoring.md:147`
  - `Knowledge\03-business-patterns\stripe-payment-processing.md:146`

### 88. duplicate_id

- **编号**: `Def-K-04-01`
- **文件**: N/A
- **消息**: 编号 Def-K-04-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\04-technology-selection\engine-selection-guide.md:105`
  - `Knowledge\04-technology-selection\paradigm-selection-guide.md:61`
  - `Knowledge\98-exercises\exercise-04-consistency-models.md:39`

### 89. duplicate_id

- **编号**: `Def-K-04-02`
- **文件**: N/A
- **消息**: 编号 Def-K-04-02 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\04-technology-selection\engine-selection-guide.md:130`
  - `Knowledge\04-technology-selection\paradigm-selection-guide.md:89`
  - `Knowledge\98-exercises\exercise-04-consistency-models.md:40`

### 90. duplicate_id

- **编号**: `Def-K-04-03`
- **文件**: N/A
- **消息**: 编号 Def-K-04-03 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\04-technology-selection\engine-selection-guide.md:155`
  - `Knowledge\04-technology-selection\paradigm-selection-guide.md:110`
  - `Knowledge\98-exercises\exercise-04-consistency-models.md:41`

### 91. duplicate_id

- **编号**: `Def-K-04-04`
- **文件**: N/A
- **消息**: 编号 Def-K-04-04 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\04-technology-selection\engine-selection-guide.md:180`
  - `Knowledge\04-technology-selection\paradigm-selection-guide.md:182`
  - `Knowledge\98-exercises\exercise-04-consistency-models.md:42`

### 92. duplicate_id

- **编号**: `Def-K-04-09`
- **文件**: N/A
- **消息**: 编号 Def-K-04-09 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\04-technology-selection\engine-selection-guide.md:258`
  - `Knowledge\04-technology-selection\storage-selection-guide.md:50`

### 93. duplicate_id

- **编号**: `Lemma-K-04-01`
- **文件**: N/A
- **消息**: 编号 Lemma-K-04-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\04-technology-selection\engine-selection-guide.md:274`
  - `Knowledge\04-technology-selection\paradigm-selection-guide.md:205`

### 94. duplicate_id

- **编号**: `Lemma-K-04-02`
- **文件**: N/A
- **消息**: 编号 Lemma-K-04-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\04-technology-selection\engine-selection-guide.md:295`
  - `Knowledge\04-technology-selection\paradigm-selection-guide.md:231`

### 95. duplicate_id

- **编号**: `Prop-K-04-01`
- **文件**: N/A
- **消息**: 编号 Prop-K-04-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\04-technology-selection\engine-selection-guide.md:310`
  - `Knowledge\04-technology-selection\paradigm-selection-guide.md:256`

### 96. duplicate_id

- **编号**: `Prop-K-04-02`
- **文件**: N/A
- **消息**: 编号 Prop-K-04-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\04-technology-selection\engine-selection-guide.md:325`
  - `Knowledge\04-technology-selection\paradigm-selection-guide.md:278`

### 97. duplicate_id

- **编号**: `Def-K-04-10`
- **文件**: N/A
- **消息**: 编号 Def-K-04-10 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\04-technology-selection\flink-vs-risingwave.md:59`
  - `Knowledge\04-technology-selection\storage-selection-guide.md:70`
  - `Knowledge\04-technology-selection\streaming-database-guide.md:89`

### 98. duplicate_id

- **编号**: `Def-K-04-11`
- **文件**: N/A
- **消息**: 编号 Def-K-04-11 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\04-technology-selection\flink-vs-risingwave.md:81`
  - `Knowledge\04-technology-selection\storage-selection-guide.md:88`
  - `Knowledge\04-technology-selection\streaming-database-guide.md:118`

### 99. duplicate_id

- **编号**: `Def-K-04-12`
- **文件**: N/A
- **消息**: 编号 Def-K-04-12 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\04-technology-selection\flink-vs-risingwave.md:92`
  - `Knowledge\04-technology-selection\storage-selection-guide.md:107`
  - `Knowledge\04-technology-selection\streaming-database-guide.md:140`

### 100. duplicate_id

- **编号**: `Lemma-K-04-03`
- **文件**: N/A
- **消息**: 编号 Lemma-K-04-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\04-technology-selection\flink-vs-risingwave.md:113`
  - `Knowledge\04-technology-selection\streaming-database-guide.md:414`

### 101. duplicate_id

- **编号**: `Lemma-K-04-04`
- **文件**: N/A
- **消息**: 编号 Lemma-K-04-04 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\04-technology-selection\flink-vs-risingwave.md:132`
  - `Knowledge\04-technology-selection\streaming-database-guide.md:429`

### 102. duplicate_id

- **编号**: `Lemma-K-04-06`
- **文件**: N/A
- **消息**: 编号 Lemma-K-04-06 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\04-technology-selection\storage-selection-guide.md:145`
  - `Knowledge\04-technology-selection\streaming-database-guide.md:451`

### 103. duplicate_id

- **编号**: `Prop-K-04-04`
- **文件**: N/A
- **消息**: 编号 Prop-K-04-04 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\04-technology-selection\storage-selection-guide.md:164`
  - `Knowledge\04-technology-selection\streaming-database-guide.md:475`

### 104. duplicate_id

- **编号**: `Prop-K-04-05`
- **文件**: N/A
- **消息**: 编号 Prop-K-04-05 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\04-technology-selection\storage-selection-guide.md:183`
  - `Knowledge\04-technology-selection\streaming-database-guide.md:497`

### 105. duplicate_id

- **编号**: `Def-K-05-01`
- **文件**: N/A
- **消息**: 编号 Def-K-05-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\05-mapping-guides\struct-to-flink-mapping.md:52`
  - `Knowledge\05-mapping-guides\theory-to-code-patterns.md:56`
  - `Knowledge\98-exercises\exercise-05-pattern-implementation.md:39`

### 106. duplicate_id

- **编号**: `Def-K-05-02`
- **文件**: N/A
- **消息**: 编号 Def-K-05-02 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\05-mapping-guides\struct-to-flink-mapping.md:78`
  - `Knowledge\05-mapping-guides\theory-to-code-patterns.md:68`
  - `Knowledge\98-exercises\exercise-05-pattern-implementation.md:40`

### 107. duplicate_id

- **编号**: `Def-K-05-03`
- **文件**: N/A
- **消息**: 编号 Def-K-05-03 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\05-mapping-guides\struct-to-flink-mapping.md:99`
  - `Knowledge\05-mapping-guides\theory-to-code-patterns.md:74`
  - `Knowledge\98-exercises\exercise-05-pattern-implementation.md:41`

### 108. duplicate_id

- **编号**: `Lemma-K-05-01`
- **文件**: N/A
- **消息**: 编号 Lemma-K-05-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\05-mapping-guides\struct-to-flink-mapping.md:126`
  - `Knowledge\05-mapping-guides\theory-to-code-patterns.md:84`

### 109. duplicate_id

- **编号**: `Lemma-K-05-02`
- **文件**: N/A
- **消息**: 编号 Lemma-K-05-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\05-mapping-guides\struct-to-flink-mapping.md:142`
  - `Knowledge\05-mapping-guides\theory-to-code-patterns.md:90`

### 110. duplicate_id

- **编号**: `Def-K-06-50`
- **文件**: N/A
- **消息**: 编号 Def-K-06-50 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\ai-agent-database-workloads.md:9`
  - `Knowledge\06-frontier\rust-streaming-ecosystem.md:9`

### 111. duplicate_id

- **编号**: `Def-K-06-51`
- **文件**: N/A
- **消息**: 编号 Def-K-06-51 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\ai-agent-database-workloads.md:24`
  - `Knowledge\06-frontier\rust-streaming-ecosystem.md:36`

### 112. duplicate_id

- **编号**: `Def-K-06-52`
- **文件**: N/A
- **消息**: 编号 Def-K-06-52 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\ai-agent-database-workloads.md:39`
  - `Knowledge\06-frontier\rust-streaming-ecosystem.md:67`

### 113. duplicate_id

- **编号**: `Def-K-06-08`
- **文件**: N/A
- **消息**: 编号 Def-K-06-08 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\06-frontier\cloud-edge-continuum.md:47`
  - `Knowledge\06-frontier\risingwave-integration-guide.md:57`
  - `Knowledge\06-frontier\temporal-flink-layered-architecture.md:104`

### 114. duplicate_id

- **编号**: `Def-K-06-09`
- **文件**: N/A
- **消息**: 编号 Def-K-06-09 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\cloud-edge-continuum.md:70`
  - `Knowledge\06-frontier\risingwave-integration-guide.md:78`

### 115. duplicate_id

- **编号**: `Def-K-06-10`
- **文件**: N/A
- **消息**: 编号 Def-K-06-10 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\cloud-edge-continuum.md:89`
  - `Knowledge\06-frontier\risingwave-integration-guide.md:100`

### 116. duplicate_id

- **编号**: `Def-K-06-11`
- **文件**: N/A
- **消息**: 编号 Def-K-06-11 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\cloud-edge-continuum.md:111`
  - `Knowledge\06-frontier\risingwave-integration-guide.md:127`

### 117. duplicate_id

- **编号**: `Prop-K-06-05`
- **文件**: N/A
- **消息**: 编号 Prop-K-06-05 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\06-frontier\cloud-edge-continuum.md:133`
  - `Knowledge\06-frontier\streaming-lakehouse-iceberg-delta.md:88`
  - `Knowledge\06-frontier\temporal-flink-layered-architecture.md:142`

### 118. duplicate_id

- **编号**: `Prop-K-06-06`
- **文件**: N/A
- **消息**: 编号 Prop-K-06-06 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\06-frontier\cloud-edge-continuum.md:151`
  - `Knowledge\06-frontier\streaming-lakehouse-iceberg-delta.md:104`
  - `Knowledge\06-frontier\temporal-flink-layered-architecture.md:159`

### 119. duplicate_id

- **编号**: `Prop-K-06-07`
- **文件**: N/A
- **消息**: 编号 Prop-K-06-07 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\cloud-edge-continuum.md:160`
  - `Knowledge\06-frontier\streaming-lakehouse-iceberg-delta.md:121`

### 120. duplicate_id

- **编号**: `Lemma-K-06-04`
- **文件**: N/A
- **消息**: 编号 Lemma-K-06-04 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\cloud-edge-continuum.md:169`
  - `Knowledge\06-frontier\streaming-access-control.md:291`

### 121. duplicate_id

- **编号**: `Lemma-K-06-10`
- **文件**: N/A
- **消息**: 编号 Lemma-K-06-10 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\edge-llm-realtime-inference.md:342`
  - `Knowledge\06-frontier\rust-streaming-ecosystem.md:155`

### 122. duplicate_id

- **编号**: `Def-K-06-12`
- **文件**: N/A
- **消息**: 编号 Def-K-06-12 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\06-frontier\edge-streaming-patterns.md:50`
  - `Knowledge\06-frontier\streaming-databases.md:39`
  - `Knowledge\06-frontier\wasm-dataflow-patterns.md:74`

### 123. duplicate_id

- **编号**: `Def-K-06-13`
- **文件**: N/A
- **消息**: 编号 Def-K-06-13 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\06-frontier\edge-streaming-patterns.md:77`
  - `Knowledge\06-frontier\streaming-databases.md:69`
  - `Knowledge\06-frontier\wasm-dataflow-patterns.md:141`

### 124. duplicate_id

- **编号**: `Def-K-06-14`
- **文件**: N/A
- **消息**: 编号 Def-K-06-14 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\06-frontier\edge-streaming-patterns.md:114`
  - `Knowledge\06-frontier\streaming-databases.md:95`
  - `Knowledge\06-frontier\wasm-dataflow-patterns.md:172`

### 125. duplicate_id

- **编号**: `Def-K-06-15`
- **文件**: N/A
- **消息**: 编号 Def-K-06-15 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\06-frontier\edge-streaming-patterns.md:155`
  - `Knowledge\06-frontier\streaming-access-control.md:50`
  - `Knowledge\06-frontier\wasm-dataflow-patterns.md:375`

### 126. duplicate_id

- **编号**: `Def-K-06-16`
- **文件**: N/A
- **消息**: 编号 Def-K-06-16 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\edge-streaming-patterns.md:196`
  - `Knowledge\06-frontier\streaming-access-control.md:84`

### 127. duplicate_id

- **编号**: `Prop-K-06-08`
- **文件**: N/A
- **消息**: 编号 Prop-K-06-08 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\06-frontier\edge-streaming-patterns.md:213`
  - `Knowledge\06-frontier\streaming-access-control.md:221`
  - `Knowledge\06-frontier\wasm-dataflow-patterns.md:413`

### 128. duplicate_id

- **编号**: `Prop-K-06-09`
- **文件**: N/A
- **消息**: 编号 Prop-K-06-09 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\06-frontier\edge-streaming-patterns.md:233`
  - `Knowledge\06-frontier\streaming-access-control.md:243`
  - `Knowledge\06-frontier\wasm-dataflow-patterns.md:447`

### 129. duplicate_id

- **编号**: `Prop-K-06-10`
- **文件**: N/A
- **消息**: 编号 Prop-K-06-10 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\06-frontier\edge-streaming-patterns.md:252`
  - `Knowledge\06-frontier\real-time-rag-architecture.md:91`
  - `Knowledge\06-frontier\streaming-access-control.md:267`

### 130. duplicate_id

- **编号**: `Lemma-K-06-05`
- **文件**: N/A
- **消息**: 编号 Lemma-K-06-05 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\edge-streaming-patterns.md:266`
  - `Knowledge\06-frontier\wasm-dataflow-patterns.md:483`

### 131. duplicate_id

- **编号**: `Def-K-06-05`
- **文件**: N/A
- **消息**: 编号 Def-K-06-05 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\faas-dataflow.md:50`
  - `Knowledge\06-frontier\temporal-flink-layered-architecture.md:49`

### 132. duplicate_id

- **编号**: `Def-K-06-06`
- **文件**: N/A
- **消息**: 编号 Def-K-06-06 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\faas-dataflow.md:77`
  - `Knowledge\06-frontier\temporal-flink-layered-architecture.md:70`

### 133. duplicate_id

- **编号**: `Def-K-06-07`
- **文件**: N/A
- **消息**: 编号 Def-K-06-07 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\faas-dataflow.md:97`
  - `Knowledge\06-frontier\temporal-flink-layered-architecture.md:89`

### 134. duplicate_id

- **编号**: `Prop-K-06-01`
- **文件**: N/A
- **消息**: 编号 Prop-K-06-01 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Knowledge\06-frontier\faas-dataflow.md:115`
  - `Knowledge\06-frontier\stateful-serverless.md:123`
  - `Knowledge\06-frontier\streaming-databases.md:129`
  - `Knowledge\06-frontier\streaming-slo-definition.md:135`

### 135. duplicate_id

- **编号**: `Prop-K-06-02`
- **文件**: N/A
- **消息**: 编号 Prop-K-06-02 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Knowledge\06-frontier\faas-dataflow.md:131`
  - `Knowledge\06-frontier\stateful-serverless.md:134`
  - `Knowledge\06-frontier\streaming-databases.md:143`
  - `Knowledge\06-frontier\streaming-slo-definition.md:150`

### 136. duplicate_id

- **编号**: `Lemma-K-06-01`
- **文件**: N/A
- **消息**: 编号 Lemma-K-06-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\faas-dataflow.md:147`
  - `Knowledge\06-frontier\streaming-slo-definition.md:166`

### 137. duplicate_id

- **编号**: `Def-K-06-20`
- **文件**: N/A
- **消息**: 编号 Def-K-06-20 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\materialize-comparison-guide.md:62`
  - `Knowledge\06-frontier\streaming-slo-definition.md:61`

### 138. duplicate_id

- **编号**: `Def-K-06-21`
- **文件**: N/A
- **消息**: 编号 Def-K-06-21 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\materialize-comparison-guide.md:88`
  - `Knowledge\06-frontier\streaming-slo-definition.md:80`

### 139. duplicate_id

- **编号**: `Def-K-06-22`
- **文件**: N/A
- **消息**: 编号 Def-K-06-22 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\materialize-comparison-guide.md:122`
  - `Knowledge\06-frontier\streaming-slo-definition.md:104`

### 140. duplicate_id

- **编号**: `Def-K-06-23`
- **文件**: N/A
- **消息**: 编号 Def-K-06-23 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\materialize-comparison-guide.md:146`
  - `Knowledge\06-frontier\streaming-lakehouse-iceberg-delta.md:7`

### 141. duplicate_id

- **编号**: `Lemma-K-06-20`
- **文件**: N/A
- **消息**: 编号 Lemma-K-06-20 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\materialize-comparison-guide.md:168`
  - `Knowledge\06-frontier\realtime-ai-streaming-2026.md:158`

### 142. duplicate_id

- **编号**: `Prop-K-06-20`
- **文件**: N/A
- **消息**: 编号 Prop-K-06-20 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\06-frontier\materialize-comparison-guide.md:216`
  - `Knowledge\06-frontier\realtime-ai-streaming-2026.md:120`
  - `Knowledge\06-frontier\rust-streaming-comparison.md:143`

### 143. duplicate_id

- **编号**: `Lemma-K-06-07`
- **文件**: N/A
- **消息**: 编号 Lemma-K-06-07 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\real-time-rag-architecture.md:125`
  - `Knowledge\06-frontier\risingwave-integration-guide.md:168`

### 144. duplicate_id

- **编号**: `Def-K-06-40`
- **文件**: N/A
- **消息**: 编号 Def-K-06-40 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\realtime-ai-streaming-2026.md:7`
  - `Knowledge\06-frontier\rust-streaming-comparison.md:10`

### 145. duplicate_id

- **编号**: `Def-K-06-41`
- **文件**: N/A
- **消息**: 编号 Def-K-06-41 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\realtime-ai-streaming-2026.md:25`
  - `Knowledge\06-frontier\rust-streaming-comparison.md:44`

### 146. duplicate_id

- **编号**: `Def-K-06-42`
- **文件**: N/A
- **消息**: 编号 Def-K-06-42 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\realtime-ai-streaming-2026.md:56`
  - `Knowledge\06-frontier\rust-streaming-comparison.md:73`

### 147. duplicate_id

- **编号**: `Def-K-06-43`
- **文件**: N/A
- **消息**: 编号 Def-K-06-43 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\realtime-ai-streaming-2026.md:81`
  - `Knowledge\06-frontier\rust-streaming-comparison.md:102`

### 148. duplicate_id

- **编号**: `Prop-K-06-21`
- **文件**: N/A
- **消息**: 编号 Prop-K-06-21 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\realtime-ai-streaming-2026.md:140`
  - `Knowledge\06-frontier\rust-streaming-comparison.md:162`

### 149. duplicate_id

- **编号**: `Prop-K-06-22`
- **文件**: N/A
- **消息**: 编号 Prop-K-06-22 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\realtime-ai-streaming-2026.md:174`
  - `Knowledge\06-frontier\rust-streaming-comparison.md:187`

### 150. duplicate_id

- **编号**: `Prop-K-06-03`
- **文件**: N/A
- **消息**: 编号 Prop-K-06-03 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Knowledge\06-frontier\risingwave-integration-guide.md:184`
  - `Knowledge\06-frontier\stateful-serverless.md:143`
  - `Knowledge\06-frontier\streaming-databases.md:153`

### 151. duplicate_id

- **编号**: `Prop-K-06-13`
- **文件**: N/A
- **消息**: 编号 Prop-K-06-13 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\rust-streaming-ecosystem.md:200`
  - `Knowledge\06-frontier\vector-search-streaming-convergence.md:127`

### 152. duplicate_id

- **编号**: `Thm-K-06-97`
- **文件**: N/A
- **消息**: 编号 Thm-K-06-97 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\serverless-streaming-architecture.md:126`
  - `Knowledge\06-frontier\serverless-streaming-cost-optimization.md:474`

### 153. duplicate_id

- **编号**: `Def-K-06-01`
- **文件**: N/A
- **消息**: 编号 Def-K-06-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\stateful-serverless.md:46`
  - `Knowledge\98-exercises\exercise-06-tla-practice.md:42`

### 154. duplicate_id

- **编号**: `Def-K-06-02`
- **文件**: N/A
- **消息**: 编号 Def-K-06-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\stateful-serverless.md:60`
  - `Knowledge\98-exercises\exercise-06-tla-practice.md:43`

### 155. duplicate_id

- **编号**: `Def-K-06-03`
- **文件**: N/A
- **消息**: 编号 Def-K-06-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\stateful-serverless.md:77`
  - `Knowledge\98-exercises\exercise-06-tla-practice.md:44`

### 156. duplicate_id

- **编号**: `Def-K-06-04`
- **文件**: N/A
- **消息**: 编号 Def-K-06-04 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\06-frontier\stateful-serverless.md:98`
  - `Knowledge\98-exercises\exercise-06-tla-practice.md:45`

### 157. duplicate_id

- **编号**: `Def-K-08-30`
- **文件**: N/A
- **消息**: 编号 Def-K-08-30 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\08-standards\streaming-data-governance-quality.md:9`
  - `Knowledge\08-standards\streaming-security-compliance.md:9`

### 158. duplicate_id

- **编号**: `Def-K-08-31`
- **文件**: N/A
- **消息**: 编号 Def-K-08-31 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\08-standards\streaming-data-governance-quality.md:25`
  - `Knowledge\08-standards\streaming-security-compliance.md:38`

### 159. duplicate_id

- **编号**: `Def-K-08-32`
- **文件**: N/A
- **消息**: 编号 Def-K-08-32 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\08-standards\streaming-data-governance-quality.md:67`
  - `Knowledge\08-standards\streaming-security-compliance.md:81`

### 160. duplicate_id

- **编号**: `Def-K-08-33`
- **文件**: N/A
- **消息**: 编号 Def-K-08-33 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\08-standards\streaming-data-governance-quality.md:82`
  - `Knowledge\08-standards\streaming-security-compliance.md:125`

### 161. duplicate_id

- **编号**: `Def-K-08-34`
- **文件**: N/A
- **消息**: 编号 Def-K-08-34 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Knowledge\08-standards\streaming-data-governance-quality.md:96`
  - `Knowledge\08-standards\streaming-security-compliance.md:162`

### 162. duplicate_id

- **编号**: `Def-F-01-01`
- **文件**: N/A
- **消息**: 编号 Def-F-01-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\01-architecture\datastream-v2-semantics.md:45`
  - `Flink\01-architecture\disaggregated-state-analysis.md:45`

### 163. duplicate_id

- **编号**: `Def-F-01-02`
- **文件**: N/A
- **消息**: 编号 Def-F-01-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\01-architecture\datastream-v2-semantics.md:69`
  - `Flink\01-architecture\disaggregated-state-analysis.md:69`

### 164. duplicate_id

- **编号**: `Def-F-01-03`
- **文件**: N/A
- **消息**: 编号 Def-F-01-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\01-architecture\datastream-v2-semantics.md:98`
  - `Flink\01-architecture\disaggregated-state-analysis.md:90`

### 165. duplicate_id

- **编号**: `Def-F-01-04`
- **文件**: N/A
- **消息**: 编号 Def-F-01-04 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\01-architecture\datastream-v2-semantics.md:129`
  - `Flink\01-architecture\disaggregated-state-analysis.md:124`

### 166. duplicate_id

- **编号**: `Lemma-F-01-01`
- **文件**: N/A
- **消息**: 编号 Lemma-F-01-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\01-architecture\datastream-v2-semantics.md:217`
  - `Flink\01-architecture\disaggregated-state-analysis.md:150`

### 167. duplicate_id

- **编号**: `Lemma-F-01-02`
- **文件**: N/A
- **消息**: 编号 Lemma-F-01-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\01-architecture\datastream-v2-semantics.md:230`
  - `Flink\01-architecture\disaggregated-state-analysis.md:175`

### 168. duplicate_id

- **编号**: `Prop-F-01-01`
- **文件**: N/A
- **消息**: 编号 Prop-F-01-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\01-architecture\datastream-v2-semantics.md:245`
  - `Flink\01-architecture\disaggregated-state-analysis.md:199`

### 169. duplicate_id

- **编号**: `Thm-F-01-01`
- **文件**: N/A
- **消息**: 编号 Thm-F-01-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\01-architecture\datastream-v2-semantics.md:393`
  - `Flink\01-architecture\disaggregated-state-analysis.md:303`

### 170. duplicate_id

- **编号**: `Thm-F-01-02`
- **文件**: N/A
- **消息**: 编号 Thm-F-01-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\01-architecture\datastream-v2-semantics.md:406`
  - `Flink\01-architecture\disaggregated-state-analysis.md:337`

### 171. duplicate_id

- **编号**: `Def-F-02-90`
- **文件**: N/A
- **消息**: 编号 Def-F-02-90 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\adaptive-execution-engine-v2.md:208`
  - `Flink\02-core-mechanisms\flink-state-management-complete-guide.md:23`

### 172. duplicate_id

- **编号**: `Def-F-02-91`
- **文件**: N/A
- **消息**: 编号 Def-F-02-91 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\adaptive-execution-engine-v2.md:257`
  - `Flink\02-core-mechanisms\flink-state-management-complete-guide.md:48`

### 173. duplicate_id

- **编号**: `Def-F-02-92`
- **文件**: N/A
- **消息**: 编号 Def-F-02-92 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\adaptive-execution-engine-v2.md:282`
  - `Flink\02-core-mechanisms\flink-state-management-complete-guide.md:71`

### 174. duplicate_id

- **编号**: `Lemma-F-02-05`
- **文件**: N/A
- **消息**: 编号 Lemma-F-02-05 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\adaptive-execution-engine-v2.md:367`
  - `Flink\02-core-mechanisms\forst-state-backend.md:145`

### 175. duplicate_id

- **编号**: `Prop-F-02-02`
- **文件**: N/A
- **消息**: 编号 Prop-F-02-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\adaptive-execution-engine-v2.md:397`
  - `Flink\02-core-mechanisms\backpressure-and-flow-control.md:156`

### 176. duplicate_id

- **编号**: `Prop-F-02-03`
- **文件**: N/A
- **消息**: 编号 Prop-F-02-03 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\adaptive-execution-engine-v2.md:415`
  - `Flink\02-core-mechanisms\backpressure-and-flow-control.md:164`
  - `Flink\02-core-mechanisms\forst-state-backend.md:112`

### 177. duplicate_id

- **编号**: `Def-F-02-05`
- **文件**: N/A
- **消息**: 编号 Def-F-02-05 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\async-execution-model.md:51`
  - `Flink\02-core-mechanisms\backpressure-and-flow-control.md:104`
  - `Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md:142`
  - `Flink\02-core-mechanisms\time-semantics-and-watermark.md:128`

### 178. duplicate_id

- **编号**: `Def-F-02-06`
- **文件**: N/A
- **消息**: 编号 Def-F-02-06 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\async-execution-model.md:96`
  - `Flink\02-core-mechanisms\backpressure-and-flow-control.md:118`
  - `Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md:158`
  - `Flink\02-core-mechanisms\time-semantics-and-watermark.md:146`

### 179. duplicate_id

- **编号**: `Def-F-02-07`
- **文件**: N/A
- **消息**: 编号 Def-F-02-07 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\async-execution-model.md:126`
  - `Flink\02-core-mechanisms\backpressure-and-flow-control.md:132`
  - `Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md:182`

### 180. duplicate_id

- **编号**: `Lemma-F-02-01`
- **文件**: N/A
- **消息**: 编号 Lemma-F-02-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\async-execution-model.md:216`
  - `Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md:205`
  - `Flink\02-core-mechanisms\time-semantics-and-watermark.md:173`

### 181. duplicate_id

- **编号**: `Lemma-F-02-02`
- **文件**: N/A
- **消息**: 编号 Lemma-F-02-02 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\async-execution-model.md:252`
  - `Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md:221`
  - `Flink\02-core-mechanisms\time-semantics-and-watermark.md:193`

### 182. duplicate_id

- **编号**: `Prop-F-02-01`
- **文件**: N/A
- **消息**: 编号 Prop-F-02-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\async-execution-model.md:272`
  - `Flink\02-core-mechanisms\backpressure-and-flow-control.md:150`
  - `Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md:256`

### 183. duplicate_id

- **编号**: `Thm-F-02-03`
- **文件**: N/A
- **消息**: 编号 Thm-F-02-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\async-execution-model.md:518`
  - `Flink\02-core-mechanisms\state-backends-deep-comparison.md:407`

### 184. duplicate_id

- **编号**: `Lemma-F-02-03`
- **文件**: N/A
- **消息**: 编号 Lemma-F-02-03 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\async-execution-model.md:594`
  - `Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md:236`
  - `Flink\02-core-mechanisms\time-semantics-and-watermark.md:207`

### 185. duplicate_id

- **编号**: `Def-F-02-01`
- **文件**: N/A
- **消息**: 编号 Def-F-02-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\backpressure-and-flow-control.md:50`
  - `Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md:75`
  - `Flink\02-core-mechanisms\time-semantics-and-watermark.md:50`

### 186. duplicate_id

- **编号**: `Def-F-02-02`
- **文件**: N/A
- **消息**: 编号 Def-F-02-02 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\backpressure-and-flow-control.md:62`
  - `Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md:94`
  - `Flink\02-core-mechanisms\time-semantics-and-watermark.md:66`

### 187. duplicate_id

- **编号**: `Def-F-02-03`
- **文件**: N/A
- **消息**: 编号 Def-F-02-03 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\backpressure-and-flow-control.md:79`
  - `Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md:110`
  - `Flink\02-core-mechanisms\time-semantics-and-watermark.md:82`

### 188. duplicate_id

- **编号**: `Def-F-02-04`
- **文件**: N/A
- **消息**: 编号 Def-F-02-04 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\backpressure-and-flow-control.md:91`
  - `Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md:126`
  - `Flink\02-core-mechanisms\time-semantics-and-watermark.md:98`

### 189. duplicate_id

- **编号**: `Prop-F-02-04`
- **文件**: N/A
- **消息**: 编号 Prop-F-02-04 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\backpressure-and-flow-control.md:172`
  - `Flink\02-core-mechanisms\forst-state-backend.md:132`

### 190. duplicate_id

- **编号**: `Prop-F-02-05`
- **文件**: N/A
- **消息**: 编号 Prop-F-02-05 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\backpressure-and-flow-control.md:180`
  - `Flink\02-core-mechanisms\state-backends-deep-comparison.md:222`

### 191. duplicate_id

- **编号**: `Thm-F-02-01`
- **文件**: N/A
- **消息**: 编号 Thm-F-02-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md:526`
  - `Flink\02-core-mechanisms\forst-state-backend.md:292`
  - `Flink\02-core-mechanisms\time-semantics-and-watermark.md:326`

### 192. duplicate_id

- **编号**: `Thm-F-02-02`
- **文件**: N/A
- **消息**: 编号 Thm-F-02-02 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md:569`
  - `Flink\02-core-mechanisms\forst-state-backend.md:335`
  - `Flink\02-core-mechanisms\time-semantics-and-watermark.md:352`

### 193. duplicate_id

- **编号**: `Prop-F-02-21`
- **文件**: N/A
- **消息**: 编号 Prop-F-02-21 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\delta-join-production-guide.md:186`
  - `Flink\02-core-mechanisms\flink-2.0-forst-state-backend.md:183`

### 194. duplicate_id

- **编号**: `Prop-F-02-22`
- **文件**: N/A
- **消息**: 编号 Prop-F-02-22 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\delta-join-production-guide.md:205`
  - `Flink\02-core-mechanisms\flink-2.0-forst-state-backend.md:217`

### 195. duplicate_id

- **编号**: `Def-F-02-80`
- **文件**: N/A
- **消息**: 编号 Def-F-02-80 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\flink-2.0-async-execution-model.md:166`
  - `Flink\02-core-mechanisms\flink-state-ttl-best-practices.md:9`

### 196. duplicate_id

- **编号**: `Def-F-02-81`
- **文件**: N/A
- **消息**: 编号 Def-F-02-81 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\02-core-mechanisms\flink-2.0-async-execution-model.md:188`
  - `Flink\02-core-mechanisms\flink-state-ttl-best-practices.md:17`

### 197. duplicate_id

- **编号**: `Def-F-03-01`
- **文件**: N/A
- **消息**: 编号 Def-F-03-01 在多个文件中重复定义 (5 个文件)
- **位置**:
  - `Flink\03-sql-table-api\built-in-functions-complete-list.md:9`
  - `Flink\03-sql-table-api\data-types-complete-reference.md:7`
  - `Flink\03-sql-table-api\flink-table-sql-complete-guide.md:11`
  - `Flink\03-sql-table-api\sql-functions-cheatsheet.md:9`
  - `Flink\03-sql-table-api\sql-vs-datastream-comparison.md:43`

### 198. duplicate_id

- **编号**: `Def-F-03-02`
- **文件**: N/A
- **消息**: 编号 Def-F-03-02 在多个文件中重复定义 (5 个文件)
- **位置**:
  - `Flink\03-sql-table-api\built-in-functions-complete-list.md:21`
  - `Flink\03-sql-table-api\data-types-complete-reference.md:22`
  - `Flink\03-sql-table-api\flink-table-sql-complete-guide.md:27`
  - `Flink\03-sql-table-api\sql-functions-cheatsheet.md:24`
  - `Flink\03-sql-table-api\sql-vs-datastream-comparison.md:62`

### 199. duplicate_id

- **编号**: `Prop-F-03-01`
- **文件**: N/A
- **消息**: 编号 Prop-F-03-01 在多个文件中重复定义 (5 个文件)
- **位置**:
  - `Flink\03-sql-table-api\built-in-functions-complete-list.md:41`
  - `Flink\03-sql-table-api\data-types-complete-reference.md:83`
  - `Flink\03-sql-table-api\flink-table-sql-complete-guide.md:148`
  - `Flink\03-sql-table-api\materialized-tables.md:145`
  - `Flink\03-sql-table-api\sql-vs-datastream-comparison.md:117`

### 200. duplicate_id

- **编号**: `Prop-F-03-02`
- **文件**: N/A
- **消息**: 编号 Prop-F-03-02 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Flink\03-sql-table-api\built-in-functions-complete-list.md:51`
  - `Flink\03-sql-table-api\data-types-complete-reference.md:471`
  - `Flink\03-sql-table-api\flink-table-sql-complete-guide.md:171`
  - `Flink\03-sql-table-api\materialized-tables.md:157`

### 201. duplicate_id

- **编号**: `Prop-F-03-03`
- **文件**: N/A
- **消息**: 编号 Prop-F-03-03 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\03-sql-table-api\built-in-functions-complete-list.md:59`
  - `Flink\03-sql-table-api\flink-sql-window-functions-deep-dive.md:165`
  - `Flink\03-sql-table-api\materialized-tables.md:167`

### 202. duplicate_id

- **编号**: `Def-F-03-03`
- **文件**: N/A
- **消息**: 编号 Def-F-03-03 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Flink\03-sql-table-api\data-types-complete-reference.md:40`
  - `Flink\03-sql-table-api\flink-table-sql-complete-guide.md:47`
  - `Flink\03-sql-table-api\materialized-tables.md:7`
  - `Flink\03-sql-table-api\sql-vs-datastream-comparison.md:81`

### 203. duplicate_id

- **编号**: `Lemma-F-03-01`
- **文件**: N/A
- **消息**: 编号 Lemma-F-03-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\03-sql-table-api\data-types-complete-reference.md:65`
  - `Flink\03-sql-table-api\flink-table-sql-complete-guide.md:138`
  - `Flink\03-sql-table-api\sql-vs-datastream-comparison.md:92`

### 204. duplicate_id

- **编号**: `Lemma-F-03-02`
- **文件**: N/A
- **消息**: 编号 Lemma-F-03-02 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\03-sql-table-api\data-types-complete-reference.md:76`
  - `Flink\03-sql-table-api\flink-table-sql-complete-guide.md:157`
  - `Flink\03-sql-table-api\sql-vs-datastream-comparison.md:105`

### 205. duplicate_id

- **编号**: `Def-F-03-04`
- **文件**: N/A
- **消息**: 编号 Def-F-03-04 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\03-sql-table-api\data-types-complete-reference.md:100`
  - `Flink\03-sql-table-api\flink-table-sql-complete-guide.md:84`
  - `Flink\03-sql-table-api\materialized-tables.md:36`

### 206. duplicate_id

- **编号**: `Def-F-03-05`
- **文件**: N/A
- **消息**: 编号 Def-F-03-05 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\03-sql-table-api\data-types-complete-reference.md:116`
  - `Flink\03-sql-table-api\flink-table-sql-complete-guide.md:104`
  - `Flink\03-sql-table-api\materialized-tables.md:53`

### 207. duplicate_id

- **编号**: `Def-F-03-06`
- **文件**: N/A
- **消息**: 编号 Def-F-03-06 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\03-sql-table-api\data-types-complete-reference.md:131`
  - `Flink\03-sql-table-api\materialized-tables.md:64`

### 208. duplicate_id

- **编号**: `Def-F-03-07`
- **文件**: N/A
- **消息**: 编号 Def-F-03-07 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\03-sql-table-api\data-types-complete-reference.md:146`
  - `Flink\03-sql-table-api\materialized-tables.md:74`

### 209. duplicate_id

- **编号**: `Def-F-03-08`
- **文件**: N/A
- **消息**: 编号 Def-F-03-08 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\03-sql-table-api\data-types-complete-reference.md:155`
  - `Flink\03-sql-table-api\materialized-tables.md:92`

### 210. duplicate_id

- **编号**: `Def-F-03-09`
- **文件**: N/A
- **消息**: 编号 Def-F-03-09 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\03-sql-table-api\data-types-complete-reference.md:171`
  - `Flink\03-sql-table-api\materialized-tables.md:110`

### 211. duplicate_id

- **编号**: `Def-F-03-10`
- **文件**: N/A
- **消息**: 编号 Def-F-03-10 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\03-sql-table-api\data-types-complete-reference.md:182`
  - `Flink\03-sql-table-api\materialized-tables.md:128`

### 212. duplicate_id

- **编号**: `Def-F-03-15`
- **文件**: N/A
- **消息**: 编号 Def-F-03-15 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\03-sql-table-api\data-types-complete-reference.md:289`
  - `Flink\03-sql-table-api\model-ddl-and-ml-predict.md:7`

### 213. duplicate_id

- **编号**: `Def-F-03-16`
- **文件**: N/A
- **消息**: 编号 Def-F-03-16 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\03-sql-table-api\data-types-complete-reference.md:308`
  - `Flink\03-sql-table-api\model-ddl-and-ml-predict.md:46`

### 214. duplicate_id

- **编号**: `Def-F-03-17`
- **文件**: N/A
- **消息**: 编号 Def-F-03-17 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\03-sql-table-api\data-types-complete-reference.md:328`
  - `Flink\03-sql-table-api\model-ddl-and-ml-predict.md:94`

### 215. duplicate_id

- **编号**: `Def-F-03-18`
- **文件**: N/A
- **消息**: 编号 Def-F-03-18 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\03-sql-table-api\data-types-complete-reference.md:347`
  - `Flink\03-sql-table-api\model-ddl-and-ml-predict.md:147`

### 216. duplicate_id

- **编号**: `Def-F-03-19`
- **文件**: N/A
- **消息**: 编号 Def-F-03-19 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\03-sql-table-api\data-types-complete-reference.md:372`
  - `Flink\03-sql-table-api\vector-search.md:7`

### 217. duplicate_id

- **编号**: `Def-F-03-20`
- **文件**: N/A
- **消息**: 编号 Def-F-03-20 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\03-sql-table-api\data-types-complete-reference.md:401`
  - `Flink\03-sql-table-api\vector-search.md:40`

### 218. duplicate_id

- **编号**: `Def-F-03-21`
- **文件**: N/A
- **消息**: 编号 Def-F-03-21 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\03-sql-table-api\data-types-complete-reference.md:426`
  - `Flink\03-sql-table-api\vector-search.md:72`

### 219. duplicate_id

- **编号**: `Prop-F-03-04`
- **文件**: N/A
- **消息**: 编号 Prop-F-03-04 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\03-sql-table-api\flink-sql-window-functions-deep-dive.md:176`
  - `Flink\03-sql-table-api\materialized-tables.md:175`
  - `Flink\03-sql-table-api\model-ddl-and-ml-predict.md:180`

### 220. duplicate_id

- **编号**: `Prop-F-03-05`
- **文件**: N/A
- **消息**: 编号 Prop-F-03-05 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Flink\03-sql-table-api\flink-sql-window-functions-deep-dive.md:192`
  - `Flink\03-sql-table-api\materialized-tables.md:185`
  - `Flink\03-sql-table-api\model-ddl-and-ml-predict.md:195`
  - `Flink\03-sql-table-api\vector-search.md:100`

### 221. duplicate_id

- **编号**: `Prop-F-03-06`
- **文件**: N/A
- **消息**: 编号 Prop-F-03-06 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Flink\03-sql-table-api\flink-sql-window-functions-deep-dive.md:204`
  - `Flink\03-sql-table-api\materialized-tables.md:195`
  - `Flink\03-sql-table-api\model-ddl-and-ml-predict.md:207`
  - `Flink\03-sql-table-api\vector-search.md:110`

### 222. duplicate_id

- **编号**: `Thm-F-03-01`
- **文件**: N/A
- **消息**: 编号 Thm-F-03-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\03-sql-table-api\flink-table-sql-complete-guide.md:277`
  - `Flink\03-sql-table-api\sql-vs-datastream-comparison.md:198`

### 223. duplicate_id

- **编号**: `Lemma-F-04-20`
- **文件**: N/A
- **消息**: 编号 Lemma-F-04-20 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\04.04-cdc-debezium-integration.md:207`
  - `Flink\04-connectors\cloudevents-integration-guide.md:186`

### 224. duplicate_id

- **编号**: `Lemma-F-04-21`
- **文件**: N/A
- **消息**: 编号 Lemma-F-04-21 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\04.04-cdc-debezium-integration.md:233`
  - `Flink\04-connectors\cloudevents-integration-guide.md:219`

### 225. duplicate_id

- **编号**: `Prop-F-04-20`
- **文件**: N/A
- **消息**: 编号 Prop-F-04-20 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\04.04-cdc-debezium-integration.md:252`
  - `Flink\04-connectors\cloudevents-integration-guide.md:254`

### 226. duplicate_id

- **编号**: `Thm-F-04-20`
- **文件**: N/A
- **消息**: 编号 Thm-F-04-20 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\04.04-cdc-debezium-integration.md:462`
  - `Flink\04-connectors\cloudevents-integration-guide.md:633`

### 227. duplicate_id

- **编号**: `Thm-F-04-21`
- **文件**: N/A
- **消息**: 编号 Thm-F-04-21 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\04.04-cdc-debezium-integration.md:501`
  - `Flink\04-connectors\cloudevents-integration-guide.md:670`

### 228. duplicate_id

- **编号**: `Def-F-04-01`
- **文件**: N/A
- **消息**: 编号 Def-F-04-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\elasticsearch-connector-complete-guide.md:9`
  - `Flink\04-connectors\kafka-integration-patterns.md:51`

### 229. duplicate_id

- **编号**: `Def-F-04-02`
- **文件**: N/A
- **消息**: 编号 Def-F-04-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\elasticsearch-connector-complete-guide.md:18`
  - `Flink\04-connectors\kafka-integration-patterns.md:59`

### 230. duplicate_id

- **编号**: `Def-F-04-03`
- **文件**: N/A
- **消息**: 编号 Def-F-04-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\elasticsearch-connector-complete-guide.md:36`
  - `Flink\04-connectors\kafka-integration-patterns.md:82`

### 231. duplicate_id

- **编号**: `Def-F-04-04`
- **文件**: N/A
- **消息**: 编号 Def-F-04-04 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\elasticsearch-connector-complete-guide.md:51`
  - `Flink\04-connectors\kafka-integration-patterns.md:96`

### 232. duplicate_id

- **编号**: `Prop-F-04-01`
- **文件**: N/A
- **消息**: 编号 Prop-F-04-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\04-connectors\elasticsearch-connector-complete-guide.md:65`
  - `Flink\04-connectors\fluss-integration.md:71`
  - `Flink\04-connectors\kafka-integration-patterns.md:161`

### 233. duplicate_id

- **编号**: `Prop-F-04-02`
- **文件**: N/A
- **消息**: 编号 Prop-F-04-02 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\04-connectors\elasticsearch-connector-complete-guide.md:77`
  - `Flink\04-connectors\fluss-integration.md:87`
  - `Flink\04-connectors\mongodb-connector-complete-guide.md:204`

### 234. duplicate_id

- **编号**: `Lemma-F-04-01`
- **文件**: N/A
- **消息**: 编号 Lemma-F-04-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\elasticsearch-connector-complete-guide.md:91`
  - `Flink\04-connectors\kafka-integration-patterns.md:127`

### 235. duplicate_id

- **编号**: `Thm-F-04-01`
- **文件**: N/A
- **消息**: 编号 Thm-F-04-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\04-connectors\elasticsearch-connector-complete-guide.md:202`
  - `Flink\04-connectors\fluss-integration.md:210`
  - `Flink\04-connectors\kafka-integration-patterns.md:260`

### 236. duplicate_id

- **编号**: `Thm-F-04-02`
- **文件**: N/A
- **消息**: 编号 Thm-F-04-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\elasticsearch-connector-complete-guide.md:228`
  - `Flink\04-connectors\kafka-integration-patterns.md:280`

### 237. duplicate_id

- **编号**: `Def-F-04-50`
- **文件**: N/A
- **消息**: 编号 Def-F-04-50 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\flink-cdc-3.0-data-integration.md:9`
  - `Flink\04-connectors\flink-iceberg-integration.md:9`

### 238. duplicate_id

- **编号**: `Def-F-04-51`
- **文件**: N/A
- **消息**: 编号 Def-F-04-51 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\flink-cdc-3.0-data-integration.md:26`
  - `Flink\04-connectors\flink-iceberg-integration.md:75`

### 239. duplicate_id

- **编号**: `Def-F-04-52`
- **文件**: N/A
- **消息**: 编号 Def-F-04-52 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\flink-cdc-3.0-data-integration.md:37`
  - `Flink\04-connectors\flink-iceberg-integration.md:103`

### 240. duplicate_id

- **编号**: `Def-F-04-53`
- **文件**: N/A
- **消息**: 编号 Def-F-04-53 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\flink-cdc-3.0-data-integration.md:50`
  - `Flink\04-connectors\flink-iceberg-integration.md:137`

### 241. duplicate_id

- **编号**: `Lemma-F-04-40`
- **文件**: N/A
- **消息**: 编号 Lemma-F-04-40 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\flink-cdc-3.0-data-integration.md:68`
  - `Flink\04-connectors\flink-delta-lake-integration.md:250`

### 242. duplicate_id

- **编号**: `Lemma-F-04-41`
- **文件**: N/A
- **消息**: 编号 Lemma-F-04-41 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\flink-cdc-3.0-data-integration.md:78`
  - `Flink\04-connectors\flink-delta-lake-integration.md:260`

### 243. duplicate_id

- **编号**: `Prop-F-04-40`
- **文件**: N/A
- **消息**: 编号 Prop-F-04-40 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\flink-cdc-3.0-data-integration.md:93`
  - `Flink\04-connectors\flink-delta-lake-integration.md:285`

### 244. duplicate_id

- **编号**: `Thm-F-04-40`
- **文件**: N/A
- **消息**: 编号 Thm-F-04-40 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\flink-cdc-3.0-data-integration.md:234`
  - `Flink\04-connectors\flink-iceberg-integration.md:708`

### 245. duplicate_id

- **编号**: `Thm-F-04-41`
- **文件**: N/A
- **消息**: 编号 Thm-F-04-41 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\flink-cdc-3.0-data-integration.md:268`
  - `Flink\04-connectors\flink-iceberg-integration.md:773`

### 246. duplicate_id

- **编号**: `Lemma-F-04-50`
- **文件**: N/A
- **消息**: 编号 Lemma-F-04-50 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\flink-iceberg-integration.md:310`
  - `Flink\04-connectors\flink-paimon-integration.md:243`

### 247. duplicate_id

- **编号**: `Lemma-F-04-51`
- **文件**: N/A
- **消息**: 编号 Lemma-F-04-51 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\flink-iceberg-integration.md:346`
  - `Flink\04-connectors\flink-paimon-integration.md:269`

### 248. duplicate_id

- **编号**: `Prop-F-04-50`
- **文件**: N/A
- **消息**: 编号 Prop-F-04-50 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\flink-iceberg-integration.md:411`
  - `Flink\04-connectors\flink-paimon-integration.md:296`

### 249. duplicate_id

- **编号**: `Prop-F-04-51`
- **文件**: N/A
- **消息**: 编号 Prop-F-04-51 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\flink-iceberg-integration.md:444`
  - `Flink\04-connectors\flink-paimon-integration.md:331`

### 250. duplicate_id

- **编号**: `Def-F-04-10`
- **文件**: N/A
- **消息**: 编号 Def-F-04-10 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\04-connectors\fluss-integration.md:7`
  - `Flink\04-connectors\mongodb-connector-complete-guide.md:147`

### 251. duplicate_id

- **编号**: `Def-F-05-01`
- **文件**: N/A
- **消息**: 编号 Def-F-05-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\05-vs-competitors\flink-vs-kafka-streams.md:63`
  - `Flink\05-vs-competitors\flink-vs-spark-streaming.md:53`

### 252. duplicate_id

- **编号**: `Def-F-05-02`
- **文件**: N/A
- **消息**: 编号 Def-F-05-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\05-vs-competitors\flink-vs-kafka-streams.md:91`
  - `Flink\05-vs-competitors\flink-vs-spark-streaming.md:75`

### 253. duplicate_id

- **编号**: `Def-F-05-03`
- **文件**: N/A
- **消息**: 编号 Def-F-05-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\05-vs-competitors\flink-vs-kafka-streams.md:119`
  - `Flink\05-vs-competitors\linkedin-samza-deep-dive.md:7`

### 254. duplicate_id

- **编号**: `Lemma-F-05-01`
- **文件**: N/A
- **消息**: 编号 Lemma-F-05-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\05-vs-competitors\flink-vs-kafka-streams.md:149`
  - `Flink\05-vs-competitors\flink-vs-spark-streaming.md:91`
  - `Flink\05-vs-competitors\linkedin-samza-deep-dive.md:127`

### 255. duplicate_id

- **编号**: `Lemma-F-05-02`
- **文件**: N/A
- **消息**: 编号 Lemma-F-05-02 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\05-vs-competitors\flink-vs-kafka-streams.md:166`
  - `Flink\05-vs-competitors\flink-vs-spark-streaming.md:112`
  - `Flink\05-vs-competitors\linkedin-samza-deep-dive.md:141`

### 256. duplicate_id

- **编号**: `Prop-F-05-01`
- **文件**: N/A
- **消息**: 编号 Prop-F-05-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\05-vs-competitors\flink-vs-kafka-streams.md:187`
  - `Flink\05-vs-competitors\flink-vs-spark-streaming.md:127`
  - `Flink\05-vs-competitors\linkedin-samza-deep-dive.md:155`

### 257. duplicate_id

- **编号**: `Thm-F-05-01`
- **文件**: N/A
- **消息**: 编号 Thm-F-05-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\05-vs-competitors\flink-vs-kafka-streams.md:420`
  - `Flink\05-vs-competitors\flink-vs-spark-streaming.md:241`

### 258. duplicate_id

- **编号**: `Def-F-06-05`
- **文件**: N/A
- **消息**: 编号 Def-F-06-05 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\06-engineering\06.02-performance-optimization-complete.md:73`
  - `Flink\06-engineering\state-backend-selection.md:112`

### 259. duplicate_id

- **编号**: `Def-F-06-06`
- **文件**: N/A
- **消息**: 编号 Def-F-06-06 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\06-engineering\06.02-performance-optimization-complete.md:94`
  - `Flink\06-engineering\state-backend-selection.md:124`

### 260. duplicate_id

- **编号**: `Def-F-06-01`
- **文件**: N/A
- **消息**: 编号 Def-F-06-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\06-engineering\performance-tuning-guide.md:51`
  - `Flink\06-engineering\state-backend-selection.md:49`

### 261. duplicate_id

- **编号**: `Def-F-06-02`
- **文件**: N/A
- **消息**: 编号 Def-F-06-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\06-engineering\performance-tuning-guide.md:67`
  - `Flink\06-engineering\state-backend-selection.md:61`

### 262. duplicate_id

- **编号**: `Def-F-06-03`
- **文件**: N/A
- **消息**: 编号 Def-F-06-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\06-engineering\performance-tuning-guide.md:77`
  - `Flink\06-engineering\state-backend-selection.md:77`

### 263. duplicate_id

- **编号**: `Def-F-06-04`
- **文件**: N/A
- **消息**: 编号 Def-F-06-04 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\06-engineering\performance-tuning-guide.md:90`
  - `Flink\06-engineering\state-backend-selection.md:94`

### 264. duplicate_id

- **编号**: `Lemma-F-06-01`
- **文件**: N/A
- **消息**: 编号 Lemma-F-06-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\06-engineering\performance-tuning-guide.md:104`
  - `Flink\06-engineering\state-backend-selection.md:142`

### 265. duplicate_id

- **编号**: `Lemma-F-06-02`
- **文件**: N/A
- **消息**: 编号 Lemma-F-06-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\06-engineering\performance-tuning-guide.md:118`
  - `Flink\06-engineering\state-backend-selection.md:150`

### 266. duplicate_id

- **编号**: `Lemma-F-06-03`
- **文件**: N/A
- **消息**: 编号 Lemma-F-06-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\06-engineering\performance-tuning-guide.md:128`
  - `Flink\06-engineering\state-backend-selection.md:164`

### 267. duplicate_id

- **编号**: `Thm-F-06-01`
- **文件**: N/A
- **消息**: 编号 Thm-F-06-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\06-engineering\performance-tuning-guide.md:230`
  - `Flink\06-engineering\state-backend-selection.md:291`

### 268. duplicate_id

- **编号**: `Thm-F-06-02`
- **文件**: N/A
- **消息**: 编号 Thm-F-06-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\06-engineering\performance-tuning-guide.md:250`
  - `Flink\06-engineering\state-backend-selection.md:317`

### 269. duplicate_id

- **编号**: `Def-F-07-01`
- **文件**: N/A
- **消息**: 编号 Def-F-07-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\07-case-studies\case-realtime-analytics.md:297`
  - `Flink\07-operations\rest-api-complete-reference.md:9`

### 270. duplicate_id

- **编号**: `Def-F-07-02`
- **文件**: N/A
- **消息**: 编号 Def-F-07-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\07-case-studies\case-realtime-analytics.md:319`
  - `Flink\07-operations\rest-api-complete-reference.md:23`

### 271. duplicate_id

- **编号**: `Prop-F-07-01`
- **文件**: N/A
- **消息**: 编号 Prop-F-07-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\07-case-studies\case-realtime-analytics.md:400`
  - `Flink\07-operations\rest-api-complete-reference.md:41`

### 272. duplicate_id

- **编号**: `Def-F-08-50`
- **文件**: N/A
- **消息**: 编号 Def-F-08-50 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-2.5-preview.md:7`
  - `Flink\08-roadmap\flink-30-architecture-redesign.md:64`
  - `Flink\08-roadmap\flink-version-evolution-complete-guide.md:78`
  - `Flink\08-roadmap\FLIP-TRACKING-SYSTEM.md:9`

### 273. duplicate_id

- **编号**: `Def-F-08-51`
- **文件**: N/A
- **消息**: 编号 Def-F-08-51 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-2.5-preview.md:25`
  - `Flink\08-roadmap\flink-30-architecture-redesign.md:96`
  - `Flink\08-roadmap\flink-version-evolution-complete-guide.md:103`
  - `Flink\08-roadmap\FLIP-TRACKING-SYSTEM.md:33`

### 274. duplicate_id

- **编号**: `Def-F-08-52`
- **文件**: N/A
- **消息**: 编号 Def-F-08-52 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-2.5-preview.md:51`
  - `Flink\08-roadmap\flink-30-architecture-redesign.md:142`
  - `Flink\08-roadmap\flink-version-evolution-complete-guide.md:123`
  - `Flink\08-roadmap\FLIP-TRACKING-SYSTEM.md:78`

### 275. duplicate_id

- **编号**: `Def-F-08-53`
- **文件**: N/A
- **消息**: 编号 Def-F-08-53 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-2.5-preview.md:80`
  - `Flink\08-roadmap\flink-30-architecture-redesign.md:183`
  - `Flink\08-roadmap\flink-version-evolution-complete-guide.md:159`
  - `Flink\08-roadmap\FLIP-TRACKING-SYSTEM.md:102`

### 276. duplicate_id

- **编号**: `Def-F-08-54`
- **文件**: N/A
- **消息**: 编号 Def-F-08-54 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-2.5-preview.md:110`
  - `Flink\08-roadmap\flink-30-architecture-redesign.md:222`
  - `Flink\08-roadmap\flink-version-evolution-complete-guide.md:195`

### 277. duplicate_id

- **编号**: `Def-F-08-55`
- **文件**: N/A
- **消息**: 编号 Def-F-08-55 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-2.5-preview.md:133`
  - `Flink\08-roadmap\flink-30-architecture-redesign.md:260`
  - `Flink\08-roadmap\flink-version-evolution-complete-guide.md:231`

### 278. duplicate_id

- **编号**: `Prop-F-08-50`
- **文件**: N/A
- **消息**: 编号 Prop-F-08-50 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-2.5-preview.md:156`
  - `Flink\08-roadmap\flink-30-architecture-redesign.md:298`
  - `Flink\08-roadmap\flink-version-evolution-complete-guide.md:543`
  - `Flink\08-roadmap\FLIP-TRACKING-SYSTEM.md:155`

### 279. duplicate_id

- **编号**: `Prop-F-08-51`
- **文件**: N/A
- **消息**: 编号 Prop-F-08-51 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-2.5-preview.md:166`
  - `Flink\08-roadmap\flink-30-architecture-redesign.md:316`
  - `Flink\08-roadmap\flink-version-evolution-complete-guide.md:584`
  - `Flink\08-roadmap\FLIP-TRACKING-SYSTEM.md:167`

### 280. duplicate_id

- **编号**: `Lemma-F-08-50`
- **文件**: N/A
- **消息**: 编号 Lemma-F-08-50 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-2.5-preview.md:176`
  - `Flink\08-roadmap\flink-30-architecture-redesign.md:352`
  - `Flink\08-roadmap\flink-version-evolution-complete-guide.md:521`
  - `Flink\08-roadmap\FLIP-TRACKING-SYSTEM.md:129`

### 281. duplicate_id

- **编号**: `Lemma-F-08-51`
- **文件**: N/A
- **消息**: 编号 Lemma-F-08-51 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-2.5-preview.md:186`
  - `Flink\08-roadmap\flink-30-architecture-redesign.md:362`
  - `Flink\08-roadmap\flink-version-evolution-complete-guide.md:560`
  - `Flink\08-roadmap\FLIP-TRACKING-SYSTEM.md:143`

### 282. duplicate_id

- **编号**: `Thm-F-08-50`
- **文件**: N/A
- **消息**: 编号 Thm-F-08-50 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-2.5-preview.md:356`
  - `Flink\08-roadmap\flink-30-architecture-redesign.md:588`
  - `Flink\08-roadmap\flink-version-evolution-complete-guide.md:783`
  - `Flink\08-roadmap\FLIP-TRACKING-SYSTEM.md:285`

### 283. duplicate_id

- **编号**: `Thm-F-08-51`
- **文件**: N/A
- **消息**: 编号 Thm-F-08-51 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-2.5-preview.md:371`
  - `Flink\08-roadmap\flink-30-architecture-redesign.md:616`
  - `Flink\08-roadmap\flink-version-evolution-complete-guide.md:816`
  - `Flink\08-roadmap\FLIP-TRACKING-SYSTEM.md:306`

### 284. duplicate_id

- **编号**: `Thm-F-08-52`
- **文件**: N/A
- **消息**: 编号 Thm-F-08-52 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-2.5-preview.md:388`
  - `Flink\08-roadmap\flink-30-architecture-redesign.md:634`
  - `Flink\08-roadmap\flink-version-comparison-matrix.md:260`

### 285. duplicate_id

- **编号**: `Def-F-08-56`
- **文件**: N/A
- **消息**: 编号 Def-F-08-56 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-25-stream-batch-unification.md:12`
  - `Flink\08-roadmap\flink-version-evolution-complete-guide.md:284`

### 286. duplicate_id

- **编号**: `Def-F-08-57`
- **文件**: N/A
- **消息**: 编号 Def-F-08-57 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-25-stream-batch-unification.md:53`
  - `Flink\08-roadmap\flink-version-evolution-complete-guide.md:327`

### 287. duplicate_id

- **编号**: `Def-F-08-58`
- **文件**: N/A
- **消息**: 编号 Def-F-08-58 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-25-stream-batch-unification.md:90`
  - `Flink\08-roadmap\flink-version-evolution-complete-guide.md:396`

### 288. duplicate_id

- **编号**: `Def-F-08-59`
- **文件**: N/A
- **消息**: 编号 Def-F-08-59 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-25-stream-batch-unification.md:130`
  - `Flink\08-roadmap\flink-version-evolution-complete-guide.md:423`

### 289. duplicate_id

- **编号**: `Def-F-08-60`
- **文件**: N/A
- **消息**: 编号 Def-F-08-60 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-25-stream-batch-unification.md:171`
  - `Flink\08-roadmap\flink-version-evolution-complete-guide.md:456`

### 290. duplicate_id

- **编号**: `Def-F-08-61`
- **文件**: N/A
- **消息**: 编号 Def-F-08-61 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-25-stream-batch-unification.md:209`
  - `Flink\08-roadmap\flink-version-evolution-complete-guide.md:490`

### 291. duplicate_id

- **编号**: `Prop-F-08-52`
- **文件**: N/A
- **消息**: 编号 Prop-F-08-52 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-25-stream-batch-unification.md:257`
  - `Flink\08-roadmap\flink-30-architecture-redesign.md:335`
  - `Flink\08-roadmap\flink-version-comparison-matrix.md:112`

### 292. duplicate_id

- **编号**: `Prop-F-08-53`
- **文件**: N/A
- **消息**: 编号 Prop-F-08-53 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-25-stream-batch-unification.md:274`
  - `Flink\08-roadmap\flink-version-comparison-matrix.md:128`

### 293. duplicate_id

- **编号**: `Lemma-F-08-52`
- **文件**: N/A
- **消息**: 编号 Lemma-F-08-52 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-25-stream-batch-unification.md:291`
  - `Flink\08-roadmap\flink-version-comparison-matrix.md:102`

### 294. duplicate_id

- **编号**: `Lemma-F-08-53`
- **文件**: N/A
- **消息**: 编号 Lemma-F-08-53 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-25-stream-batch-unification.md:308`
  - `Flink\08-roadmap\flink-version-comparison-matrix.md:120`

### 295. duplicate_id

- **编号**: `Thm-F-08-53`
- **文件**: N/A
- **消息**: 编号 Thm-F-08-53 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\08-roadmap\flink-25-stream-batch-unification.md:482`
  - `Flink\08-roadmap\flink-30-architecture-redesign.md:659`
  - `Flink\08-roadmap\flink-version-comparison-matrix.md:281`

### 296. duplicate_id

- **编号**: `Def-F-09-01`
- **文件**: N/A
- **消息**: 编号 Def-F-09-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\09-language-foundations\01.01-scala-types-for-streaming.md:40`
  - `Flink\09-language-foundations\03.01-migration-guide.md:83`
  - `Flink\09-language-foundations\flink-language-support-complete-guide.md:9`

### 297. duplicate_id

- **编号**: `Def-F-09-02`
- **文件**: N/A
- **消息**: 编号 Def-F-09-02 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\09-language-foundations\01.01-scala-types-for-streaming.md:61`
  - `Flink\09-language-foundations\03.01-migration-guide.md:110`
  - `Flink\09-language-foundations\flink-language-support-complete-guide.md:19`

### 298. duplicate_id

- **编号**: `Def-F-09-03`
- **文件**: N/A
- **消息**: 编号 Def-F-09-03 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\09-language-foundations\01.01-scala-types-for-streaming.md:85`
  - `Flink\09-language-foundations\03.01-migration-guide.md:137`
  - `Flink\09-language-foundations\flink-language-support-complete-guide.md:29`

### 299. duplicate_id

- **编号**: `Lemma-F-09-01`
- **文件**: N/A
- **消息**: 编号 Lemma-F-09-01 在多个文件中重复定义 (8 个文件)
- **位置**:
  - `Flink\09-language-foundations\01.01-scala-types-for-streaming.md:115`
  - `Flink\09-language-foundations\01.02-typeinformation-derivation.md:167`
  - `Flink\09-language-foundations\02.02-flink-scala-api-community.md:133`
  - `Flink\09-language-foundations\03.01-migration-guide.md:154`
  - `Flink\09-language-foundations\06-risingwave-deep-dive.md:399`
  - `Flink\09-language-foundations\07-rust-streaming-landscape.md:180`
  - `Flink\09-language-foundations\08-flink-rust-connector-dev.md:196`
  - `Flink\09-language-foundations\flink-language-support-complete-guide.md:76`

### 300. duplicate_id

- **编号**: `Lemma-F-09-02`
- **文件**: N/A
- **消息**: 编号 Lemma-F-09-02 在多个文件中重复定义 (5 个文件)
- **位置**:
  - `Flink\09-language-foundations\01.01-scala-types-for-streaming.md:136`
  - `Flink\09-language-foundations\03.01-migration-guide.md:168`
  - `Flink\09-language-foundations\06-risingwave-deep-dive.md:420`
  - `Flink\09-language-foundations\08-flink-rust-connector-dev.md:213`
  - `Flink\09-language-foundations\flink-language-support-complete-guide.md:96`

### 301. duplicate_id

- **编号**: `Def-F-09-04`
- **文件**: N/A
- **消息**: 编号 Def-F-09-04 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\09-language-foundations\01.02-typeinformation-derivation.md:48`
  - `Flink\09-language-foundations\09-wasm-udf-frameworks.md:50`
  - `Flink\09-language-foundations\flink-language-support-complete-guide.md:37`

### 302. duplicate_id

- **编号**: `Def-F-09-05`
- **文件**: N/A
- **消息**: 编号 Def-F-09-05 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\09-language-foundations\01.02-typeinformation-derivation.md:66`
  - `Flink\09-language-foundations\09-wasm-udf-frameworks.md:82`
  - `Flink\09-language-foundations\flink-language-support-complete-guide.md:45`

### 303. duplicate_id

- **编号**: `Def-F-09-06`
- **文件**: N/A
- **消息**: 编号 Def-F-09-06 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\09-language-foundations\01.02-typeinformation-derivation.md:87`
  - `Flink\09-language-foundations\09-wasm-udf-frameworks.md:105`

### 304. duplicate_id

- **编号**: `Def-F-09-07`
- **文件**: N/A
- **消息**: 编号 Def-F-09-07 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\09-language-foundations\01.02-typeinformation-derivation.md:117`
  - `Flink\09-language-foundations\07-rust-streaming-landscape.md:55`
  - `Flink\09-language-foundations\09-wasm-udf-frameworks.md:137`

### 305. duplicate_id

- **编号**: `Prop-F-09-01`
- **文件**: N/A
- **消息**: 编号 Prop-F-09-01 在多个文件中重复定义 (9 个文件)
- **位置**:
  - `Flink\09-language-foundations\01.02-typeinformation-derivation.md:137`
  - `Flink\09-language-foundations\02-python-api.md:106`
  - `Flink\09-language-foundations\02.02-flink-scala-api-community.md:108`
  - `Flink\09-language-foundations\03-rust-native.md:63`
  - `Flink\09-language-foundations\03.01-migration-guide.md:178`
  - `Flink\09-language-foundations\04-streaming-lakehouse.md:131`
  - `Flink\09-language-foundations\06-risingwave-deep-dive.md:441`
  - `Flink\09-language-foundations\08-flink-rust-connector-dev.md:226`
  - `Flink\09-language-foundations\flink-language-support-complete-guide.md:58`

### 306. duplicate_id

- **编号**: `Prop-F-09-02`
- **文件**: N/A
- **消息**: 编号 Prop-F-09-02 在多个文件中重复定义 (8 个文件)
- **位置**:
  - `Flink\09-language-foundations\01.02-typeinformation-derivation.md:153`
  - `Flink\09-language-foundations\02-python-api.md:130`
  - `Flink\09-language-foundations\02.02-flink-scala-api-community.md:118`
  - `Flink\09-language-foundations\03-rust-native.md:82`
  - `Flink\09-language-foundations\04-streaming-lakehouse.md:165`
  - `Flink\09-language-foundations\06-risingwave-deep-dive.md:468`
  - `Flink\09-language-foundations\08-flink-rust-connector-dev.md:245`
  - `Flink\09-language-foundations\flink-language-support-complete-guide.md:68`

### 307. duplicate_id

- **编号**: `Thm-F-09-01`
- **文件**: N/A
- **消息**: 编号 Thm-F-09-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\09-language-foundations\01.02-typeinformation-derivation.md:352`
  - `Flink\09-language-foundations\02.02-flink-scala-api-community.md:234`

### 308. duplicate_id

- **编号**: `Thm-F-09-02`
- **文件**: N/A
- **消息**: 编号 Thm-F-09-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\09-language-foundations\01.02-typeinformation-derivation.md:380`
  - `Flink\09-language-foundations\02.02-flink-scala-api-community.md:249`

### 309. duplicate_id

- **编号**: `Def-F-09-34`
- **文件**: N/A
- **消息**: 编号 Def-F-09-34 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\09-language-foundations\01.03-scala3-type-system-formalization.md:51`
  - `Flink\09-language-foundations\08-flink-rust-connector-dev.md:177`
  - `Flink\09-language-foundations\10-wasi-component-model.md:195`

### 310. duplicate_id

- **编号**: `Prop-F-09-03`
- **文件**: N/A
- **消息**: 编号 Prop-F-09-03 在多个文件中重复定义 (5 个文件)
- **位置**:
  - `Flink\09-language-foundations\02-python-api.md:160`
  - `Flink\09-language-foundations\02.02-flink-scala-api-community.md:127`
  - `Flink\09-language-foundations\03-rust-native.md:92`
  - `Flink\09-language-foundations\04-streaming-lakehouse.md:200`
  - `Flink\09-language-foundations\flink-language-support-complete-guide.md:86`

### 311. duplicate_id

- **编号**: `Def-F-09-20`
- **文件**: N/A
- **消息**: 编号 Def-F-09-20 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\09-language-foundations\02-python-api.md:722`
  - `Flink\09-language-foundations\03-rust-native.md:7`

### 312. duplicate_id

- **编号**: `Def-F-09-21`
- **文件**: N/A
- **消息**: 编号 Def-F-09-21 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\09-language-foundations\02-python-api.md:813`
  - `Flink\09-language-foundations\03-rust-native.md:23`

### 313. duplicate_id

- **编号**: `Prop-F-09-04`
- **文件**: N/A
- **消息**: 编号 Prop-F-09-04 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Flink\09-language-foundations\02-python-api.md:850`
  - `Flink\09-language-foundations\07-rust-streaming-landscape.md:133`
  - `Flink\09-language-foundations\09-wasm-udf-frameworks.md:235`
  - `Flink\09-language-foundations\10-wasi-component-model.md:224`

### 314. duplicate_id

- **编号**: `Prop-F-09-05`
- **文件**: N/A
- **消息**: 编号 Prop-F-09-05 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Flink\09-language-foundations\02-python-api.md:872`
  - `Flink\09-language-foundations\07-rust-streaming-landscape.md:156`
  - `Flink\09-language-foundations\09-wasm-udf-frameworks.md:286`
  - `Flink\09-language-foundations\10-wasi-component-model.md:246`

### 315. duplicate_id

- **编号**: `Prop-F-09-06`
- **文件**: N/A
- **消息**: 编号 Prop-F-09-06 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\09-language-foundations\02-python-api.md:897`
  - `Flink\09-language-foundations\09-wasm-udf-frameworks.md:314`
  - `Flink\09-language-foundations\10-wasi-component-model.md:267`

### 316. duplicate_id

- **编号**: `Def-F-09-08`
- **文件**: N/A
- **消息**: 编号 Def-F-09-08 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\09-language-foundations\02.01-java-api-from-scala.md:45`
  - `Flink\09-language-foundations\07-rust-streaming-landscape.md:81`
  - `Flink\09-language-foundations\09-wasm-udf-frameworks.md:164`

### 317. duplicate_id

- **编号**: `Def-F-09-09`
- **文件**: N/A
- **消息**: 编号 Def-F-09-09 在多个文件中重复定义 (4 个文件)
- **位置**:
  - `Flink\09-language-foundations\02.01-java-api-from-scala.md:63`
  - `Flink\09-language-foundations\07-rust-streaming-landscape.md:107`
  - `Flink\09-language-foundations\09-wasm-udf-frameworks.md:203`
  - `Flink\09-language-foundations\flink-language-support-complete-guide.md:662`

### 318. duplicate_id

- **编号**: `Def-F-09-10`
- **文件**: N/A
- **消息**: 编号 Def-F-09-10 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\09-language-foundations\02.02-flink-scala-api-community.md:25`
  - `Flink\09-language-foundations\flink-language-support-complete-guide.md:775`

### 319. duplicate_id

- **编号**: `Def-F-09-13`
- **文件**: N/A
- **消息**: 编号 Def-F-09-13 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\09-language-foundations\02.02-flink-scala-api-community.md:81`
  - `Flink\09-language-foundations\04-streaming-lakehouse.md:9`

### 320. duplicate_id

- **编号**: `Def-F-09-14`
- **文件**: N/A
- **消息**: 编号 Def-F-09-14 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\09-language-foundations\02.02-flink-scala-api-community.md:96`
  - `Flink\09-language-foundations\04-streaming-lakehouse.md:36`

### 321. duplicate_id

- **编号**: `Prop-F-09-50`
- **文件**: N/A
- **消息**: 编号 Prop-F-09-50 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\09-language-foundations\02.03-python-async-api.md:575`
  - `Flink\09-language-foundations\flink-25-wasm-udf-ga.md:401`

### 322. duplicate_id

- **编号**: `Prop-F-09-51`
- **文件**: N/A
- **消息**: 编号 Prop-F-09-51 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\09-language-foundations\02.03-python-async-api.md:656`
  - `Flink\09-language-foundations\flink-25-wasm-udf-ga.md:444`

### 323. duplicate_id

- **编号**: `Def-F-09-30`
- **文件**: N/A
- **消息**: 编号 Def-F-09-30 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\09-language-foundations\05-datastream-v2-api.md:49`
  - `Flink\09-language-foundations\08-flink-rust-connector-dev.md:64`
  - `Flink\09-language-foundations\10-wasi-component-model.md:53`

### 324. duplicate_id

- **编号**: `Def-F-09-31`
- **文件**: N/A
- **消息**: 编号 Def-F-09-31 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\09-language-foundations\05-datastream-v2-api.md:117`
  - `Flink\09-language-foundations\08-flink-rust-connector-dev.md:111`
  - `Flink\09-language-foundations\10-wasi-component-model.md:85`

### 325. duplicate_id

- **编号**: `Def-F-09-32`
- **文件**: N/A
- **消息**: 编号 Def-F-09-32 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\09-language-foundations\05-datastream-v2-api.md:193`
  - `Flink\09-language-foundations\08-flink-rust-connector-dev.md:127`
  - `Flink\09-language-foundations\10-wasi-component-model.md:123`

### 326. duplicate_id

- **编号**: `Def-F-09-33`
- **文件**: N/A
- **消息**: 编号 Def-F-09-33 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\09-language-foundations\05-datastream-v2-api.md:297`
  - `Flink\09-language-foundations\08-flink-rust-connector-dev.md:154`
  - `Flink\09-language-foundations\10-wasi-component-model.md:154`

### 327. duplicate_id

- **编号**: `Def-F-09-50`
- **文件**: N/A
- **消息**: 编号 Def-F-09-50 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\09-language-foundations\06-risingwave-deep-dive.md:373`
  - `Flink\09-language-foundations\flink-25-wasm-udf-ga.md:64`

### 328. duplicate_id

- **编号**: `Def-F-10-01`
- **文件**: N/A
- **消息**: 编号 Def-F-10-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\10-deployment\cost-optimization-calculator.md:9`
  - `Flink\10-deployment\kubernetes-deployment.md:9`
  - `Flink\10-deployment\multi-cloud-deployment-templates.md:44`

### 329. duplicate_id

- **编号**: `Def-F-10-02`
- **文件**: N/A
- **消息**: 编号 Def-F-10-02 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\10-deployment\cost-optimization-calculator.md:24`
  - `Flink\10-deployment\kubernetes-deployment.md:33`
  - `Flink\10-deployment\multi-cloud-deployment-templates.md:58`

### 330. duplicate_id

- **编号**: `Def-F-10-03`
- **文件**: N/A
- **消息**: 编号 Def-F-10-03 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\10-deployment\cost-optimization-calculator.md:39`
  - `Flink\10-deployment\kubernetes-deployment.md:55`
  - `Flink\10-deployment\multi-cloud-deployment-templates.md:71`

### 331. duplicate_id

- **编号**: `Prop-F-10-01`
- **文件**: N/A
- **消息**: 编号 Prop-F-10-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\10-deployment\cost-optimization-calculator.md:76`
  - `Flink\10-deployment\kubernetes-deployment.md:99`
  - `Flink\10-deployment\multi-cloud-deployment-templates.md:86`

### 332. duplicate_id

- **编号**: `Prop-F-10-02`
- **文件**: N/A
- **消息**: 编号 Prop-F-10-02 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\10-deployment\cost-optimization-calculator.md:88`
  - `Flink\10-deployment\kubernetes-deployment.md:120`
  - `Flink\10-deployment\multi-cloud-deployment-templates.md:103`

### 333. duplicate_id

- **编号**: `Prop-F-10-03`
- **文件**: N/A
- **消息**: 编号 Prop-F-10-03 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\10-deployment\cost-optimization-calculator.md:101`
  - `Flink\10-deployment\kubernetes-deployment.md:137`
  - `Flink\10-deployment\multi-cloud-deployment-templates.md:131`

### 334. duplicate_id

- **编号**: `Def-F-10-50`
- **文件**: N/A
- **消息**: 编号 Def-F-10-50 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-24-deployment-improvements.md:80`
  - `Flink\10-deployment\serverless-flink-ga-guide.md:16`

### 335. duplicate_id

- **编号**: `Def-F-10-51`
- **文件**: N/A
- **消息**: 编号 Def-F-10-51 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-24-deployment-improvements.md:133`
  - `Flink\10-deployment\serverless-flink-ga-guide.md:44`

### 336. duplicate_id

- **编号**: `Def-F-10-52`
- **文件**: N/A
- **消息**: 编号 Def-F-10-52 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-24-deployment-improvements.md:187`
  - `Flink\10-deployment\serverless-flink-ga-guide.md:69`

### 337. duplicate_id

- **编号**: `Def-F-10-53`
- **文件**: N/A
- **消息**: 编号 Def-F-10-53 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-24-deployment-improvements.md:240`
  - `Flink\10-deployment\serverless-flink-ga-guide.md:94`

### 338. duplicate_id

- **编号**: `Def-F-10-54`
- **文件**: N/A
- **消息**: 编号 Def-F-10-54 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-24-deployment-improvements.md:299`
  - `Flink\10-deployment\serverless-flink-ga-guide.md:117`

### 339. duplicate_id

- **编号**: `Def-F-10-55`
- **文件**: N/A
- **消息**: 编号 Def-F-10-55 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-24-deployment-improvements.md:357`
  - `Flink\10-deployment\serverless-flink-ga-guide.md:147`

### 340. duplicate_id

- **编号**: `Lemma-F-10-50`
- **文件**: N/A
- **消息**: 编号 Lemma-F-10-50 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-24-deployment-improvements.md:673`
  - `Flink\10-deployment\serverless-flink-ga-guide.md:174`

### 341. duplicate_id

- **编号**: `Lemma-F-10-51`
- **文件**: N/A
- **消息**: 编号 Lemma-F-10-51 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-24-deployment-improvements.md:714`
  - `Flink\10-deployment\serverless-flink-ga-guide.md:230`

### 342. duplicate_id

- **编号**: `Prop-F-10-50`
- **文件**: N/A
- **消息**: 编号 Prop-F-10-50 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-24-deployment-improvements.md:788`
  - `Flink\10-deployment\serverless-flink-ga-guide.md:193`

### 343. duplicate_id

- **编号**: `Thm-F-10-50`
- **文件**: N/A
- **消息**: 编号 Thm-F-10-50 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-24-deployment-improvements.md:1014`
  - `Flink\10-deployment\serverless-flink-ga-guide.md:476`

### 344. duplicate_id

- **编号**: `Thm-F-10-51`
- **文件**: N/A
- **消息**: 编号 Thm-F-10-51 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-24-deployment-improvements.md:1077`
  - `Flink\10-deployment\serverless-flink-ga-guide.md:510`

### 345. duplicate_id

- **编号**: `Thm-F-10-52`
- **文件**: N/A
- **消息**: 编号 Thm-F-10-52 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-24-deployment-improvements.md:1137`
  - `Flink\10-deployment\serverless-flink-ga-guide.md:536`

### 346. duplicate_id

- **编号**: `Def-F-10-40`
- **文件**: N/A
- **消息**: 编号 Def-F-10-40 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-deployment-ops-complete-guide.md:64`
  - `Flink\10-deployment\flink-serverless-architecture.md:7`

### 347. duplicate_id

- **编号**: `Def-F-10-41`
- **文件**: N/A
- **消息**: 编号 Def-F-10-41 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-deployment-ops-complete-guide.md:96`
  - `Flink\10-deployment\flink-serverless-architecture.md:32`

### 348. duplicate_id

- **编号**: `Def-F-10-42`
- **文件**: N/A
- **消息**: 编号 Def-F-10-42 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-deployment-ops-complete-guide.md:126`
  - `Flink\10-deployment\flink-serverless-architecture.md:47`

### 349. duplicate_id

- **编号**: `Def-F-10-43`
- **文件**: N/A
- **消息**: 编号 Def-F-10-43 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-deployment-ops-complete-guide.md:152`
  - `Flink\10-deployment\flink-serverless-architecture.md:64`

### 350. duplicate_id

- **编号**: `Def-F-10-44`
- **文件**: N/A
- **消息**: 编号 Def-F-10-44 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-deployment-ops-complete-guide.md:176`
  - `Flink\10-deployment\flink-serverless-architecture.md:84`

### 351. duplicate_id

- **编号**: `Def-F-10-45`
- **文件**: N/A
- **消息**: 编号 Def-F-10-45 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-deployment-ops-complete-guide.md:198`
  - `Flink\10-deployment\flink-serverless-architecture.md:100`

### 352. duplicate_id

- **编号**: `Lemma-F-10-40`
- **文件**: N/A
- **消息**: 编号 Lemma-F-10-40 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-deployment-ops-complete-guide.md:221`
  - `Flink\10-deployment\flink-serverless-architecture.md:121`

### 353. duplicate_id

- **编号**: `Lemma-F-10-41`
- **文件**: N/A
- **消息**: 编号 Lemma-F-10-41 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-deployment-ops-complete-guide.md:240`
  - `Flink\10-deployment\flink-serverless-architecture.md:153`

### 354. duplicate_id

- **编号**: `Prop-F-10-40`
- **文件**: N/A
- **消息**: 编号 Prop-F-10-40 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-deployment-ops-complete-guide.md:258`
  - `Flink\10-deployment\flink-serverless-architecture.md:131`

### 355. duplicate_id

- **编号**: `Prop-F-10-41`
- **文件**: N/A
- **消息**: 编号 Prop-F-10-41 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-deployment-ops-complete-guide.md:281`
  - `Flink\10-deployment\flink-serverless-architecture.md:141`

### 356. duplicate_id

- **编号**: `Thm-F-10-40`
- **文件**: N/A
- **消息**: 编号 Thm-F-10-40 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-deployment-ops-complete-guide.md:459`
  - `Flink\10-deployment\flink-serverless-architecture.md:280`

### 357. duplicate_id

- **编号**: `Thm-F-10-41`
- **文件**: N/A
- **消息**: 编号 Thm-F-10-41 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-deployment-ops-complete-guide.md:503`
  - `Flink\10-deployment\flink-serverless-architecture.md:292`

### 358. duplicate_id

- **编号**: `Thm-F-10-42`
- **文件**: N/A
- **消息**: 编号 Thm-F-10-42 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\10-deployment\flink-deployment-ops-complete-guide.md:541`
  - `Flink\10-deployment\flink-serverless-architecture.md:307`

### 359. duplicate_id

- **编号**: `Def-F-11-04`
- **文件**: N/A
- **消息**: 编号 Def-F-11-04 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\11-benchmarking\performance-benchmark-suite.md:7`
  - `Flink\11-benchmarking\performance-benchmarking-guide.md:38`

### 360. duplicate_id

- **编号**: `Def-F-11-01`
- **文件**: N/A
- **消息**: 编号 Def-F-11-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\11-benchmarking\performance-benchmarking-guide.md:9`
  - `Flink\11-benchmarking\streaming-benchmarks.md:7`

### 361. duplicate_id

- **编号**: `Def-F-11-02`
- **文件**: N/A
- **消息**: 编号 Def-F-11-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\11-benchmarking\performance-benchmarking-guide.md:22`
  - `Flink\11-benchmarking\streaming-benchmarks.md:19`

### 362. duplicate_id

- **编号**: `Def-F-11-03`
- **文件**: N/A
- **消息**: 编号 Def-F-11-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\11-benchmarking\performance-benchmarking-guide.md:28`
  - `Flink\11-benchmarking\streaming-benchmarks.md:34`

### 363. duplicate_id

- **编号**: `Prop-F-11-01`
- **文件**: N/A
- **消息**: 编号 Prop-F-11-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\11-benchmarking\performance-benchmarking-guide.md:68`
  - `Flink\11-benchmarking\streaming-benchmarks.md:55`

### 364. duplicate_id

- **编号**: `Def-F-12-30`
- **文件**: N/A
- **消息**: 编号 Def-F-12-30 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\12-ai-ml\flink-agents-flip-531.md:9`
  - `Flink\12-ai-ml\flink-realtime-ml-inference.md:9`

### 365. duplicate_id

- **编号**: `Def-F-12-31`
- **文件**: N/A
- **消息**: 编号 Def-F-12-31 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\12-ai-ml\flink-agents-flip-531.md:30`
  - `Flink\12-ai-ml\flink-realtime-ml-inference.md:27`

### 366. duplicate_id

- **编号**: `Def-F-12-32`
- **文件**: N/A
- **消息**: 编号 Def-F-12-32 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\12-ai-ml\flink-agents-flip-531.md:49`
  - `Flink\12-ai-ml\flink-realtime-ml-inference.md:53`

### 367. duplicate_id

- **编号**: `Def-F-12-33`
- **文件**: N/A
- **消息**: 编号 Def-F-12-33 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\12-ai-ml\flink-agents-flip-531.md:83`
  - `Flink\12-ai-ml\flink-realtime-ml-inference.md:70`

### 368. duplicate_id

- **编号**: `Def-F-12-34`
- **文件**: N/A
- **消息**: 编号 Def-F-12-34 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\12-ai-ml\flink-agents-flip-531.md:108`
  - `Flink\12-ai-ml\flink-realtime-ml-inference.md:88`

### 369. duplicate_id

- **编号**: `Def-F-12-35`
- **文件**: N/A
- **消息**: 编号 Def-F-12-35 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\12-ai-ml\flink-agents-flip-531.md:130`
  - `Flink\12-ai-ml\flink-realtime-ml-inference.md:106`

### 370. duplicate_id

- **编号**: `Lemma-F-12-20`
- **文件**: N/A
- **消息**: 编号 Lemma-F-12-20 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\12-ai-ml\flink-agents-flip-531.md:183`
  - `Flink\12-ai-ml\rag-streaming-architecture.md:212`

### 371. duplicate_id

- **编号**: `Prop-F-12-04`
- **文件**: N/A
- **消息**: 编号 Prop-F-12-04 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\12-ai-ml\flink-agents-flip-531.md:213`
  - `Flink\12-ai-ml\model-serving-streaming.md:87`

### 372. duplicate_id

- **编号**: `Thm-F-12-30`
- **文件**: N/A
- **消息**: 编号 Thm-F-12-30 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\12-ai-ml\flink-agents-flip-531.md:362`
  - `Flink\12-ai-ml\flink-realtime-ml-inference.md:282`

### 373. duplicate_id

- **编号**: `Thm-F-12-31`
- **文件**: N/A
- **消息**: 编号 Thm-F-12-31 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\12-ai-ml\flink-agents-flip-531.md:392`
  - `Flink\12-ai-ml\flink-realtime-ml-inference.md:314`

### 374. duplicate_id

- **编号**: `Thm-F-12-32`
- **文件**: N/A
- **消息**: 编号 Thm-F-12-32 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\12-ai-ml\flink-agents-flip-531.md:407`
  - `Flink\12-ai-ml\flink-realtime-ml-inference.md:351`

### 375. duplicate_id

- **编号**: `Prop-F-12-01`
- **文件**: N/A
- **消息**: 编号 Prop-F-12-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\12-ai-ml\flink-ml-architecture.md:71`
  - `Flink\12-ai-ml\online-learning-algorithms.md:194`
  - `Flink\12-ai-ml\vector-database-integration.md:90`

### 376. duplicate_id

- **编号**: `Prop-F-12-02`
- **文件**: N/A
- **消息**: 编号 Prop-F-12-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\12-ai-ml\flink-ml-architecture.md:89`
  - `Flink\12-ai-ml\vector-database-integration.md:126`

### 377. duplicate_id

- **编号**: `Lemma-F-12-01`
- **文件**: N/A
- **消息**: 编号 Lemma-F-12-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\12-ai-ml\flink-ml-architecture.md:101`
  - `Flink\12-ai-ml\online-learning-algorithms.md:168`
  - `Flink\12-ai-ml\vector-database-integration.md:110`

### 378. duplicate_id

- **编号**: `Def-F-12-07`
- **文件**: N/A
- **消息**: 编号 Def-F-12-07 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\12-ai-ml\model-serving-streaming.md:7`
  - `Flink\12-ai-ml\online-learning-algorithms.md:141`

### 379. duplicate_id

- **编号**: `Thm-F-12-02`
- **文件**: N/A
- **消息**: 编号 Thm-F-12-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\12-ai-ml\model-serving-streaming.md:192`
  - `Flink\12-ai-ml\online-learning-algorithms.md:446`

### 380. duplicate_id

- **编号**: `Def-F-12-10`
- **文件**: N/A
- **消息**: 编号 Def-F-12-10 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\12-ai-ml\online-learning-production.md:9`
  - `Flink\12-ai-ml\vector-database-integration.md:7`

### 381. duplicate_id

- **编号**: `Def-F-12-11`
- **文件**: N/A
- **消息**: 编号 Def-F-12-11 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\12-ai-ml\online-learning-production.md:38`
  - `Flink\12-ai-ml\vector-database-integration.md:42`

### 382. duplicate_id

- **编号**: `Def-F-12-12`
- **文件**: N/A
- **消息**: 编号 Def-F-12-12 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\12-ai-ml\online-learning-production.md:65`
  - `Flink\12-ai-ml\vector-database-integration.md:68`

### 383. duplicate_id

- **编号**: `Def-F-13-14`
- **文件**: N/A
- **消息**: 编号 Def-F-13-14 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\13-security\flink-security-complete-guide.md:9`
  - `Flink\13-wasm\wasi-0.3-async-preview.md:234`

### 384. duplicate_id

- **编号**: `Def-F-13-15`
- **文件**: N/A
- **消息**: 编号 Def-F-13-15 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\13-security\flink-security-complete-guide.md:51`
  - `Flink\13-wasm\wasi-0.3-async-preview.md:269`

### 385. duplicate_id

- **编号**: `Lemma-F-13-03`
- **文件**: N/A
- **消息**: 编号 Lemma-F-13-03 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\13-security\flink-security-complete-guide.md:257`
  - `Flink\13-security\security-hardening-guide.md:61`
  - `Flink\13-security\streaming-security-best-practices.md:72`

### 386. duplicate_id

- **编号**: `Def-F-13-10`
- **文件**: N/A
- **消息**: 编号 Def-F-13-10 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\13-security\gpu-confidential-computing.md:94`
  - `Flink\13-wasm\wasi-0.3-async-preview.md:66`

### 387. duplicate_id

- **编号**: `Def-F-13-11`
- **文件**: N/A
- **消息**: 编号 Def-F-13-11 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\13-security\gpu-confidential-computing.md:131`
  - `Flink\13-wasm\wasi-0.3-async-preview.md:99`

### 388. duplicate_id

- **编号**: `Def-F-13-12`
- **文件**: N/A
- **消息**: 编号 Def-F-13-12 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\13-security\gpu-confidential-computing.md:201`
  - `Flink\13-wasm\wasi-0.3-async-preview.md:136`

### 389. duplicate_id

- **编号**: `Def-F-13-13`
- **文件**: N/A
- **消息**: 编号 Def-F-13-13 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\13-security\gpu-confidential-computing.md:280`
  - `Flink\13-wasm\wasi-0.3-async-preview.md:186`

### 390. duplicate_id

- **编号**: `Prop-F-13-04`
- **文件**: N/A
- **消息**: 编号 Prop-F-13-04 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\13-security\gpu-confidential-computing.md:312`
  - `Flink\13-wasm\wasi-0.3-async-preview.md:323`

### 391. duplicate_id

- **编号**: `Prop-F-13-05`
- **文件**: N/A
- **消息**: 编号 Prop-F-13-05 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\13-security\gpu-confidential-computing.md:342`
  - `Flink\13-wasm\wasi-0.3-async-preview.md:349`

### 392. duplicate_id

- **编号**: `Prop-F-13-06`
- **文件**: N/A
- **消息**: 编号 Prop-F-13-06 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\13-security\gpu-confidential-computing.md:359`
  - `Flink\13-wasm\wasi-0.3-async-preview.md:371`

### 393. duplicate_id

- **编号**: `Lemma-F-13-02`
- **文件**: N/A
- **消息**: 编号 Lemma-F-13-02 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\13-security\gpu-confidential-computing.md:377`
  - `Flink\13-security\security-hardening-guide.md:54`
  - `Flink\13-security\streaming-security-best-practices.md:62`

### 394. duplicate_id

- **编号**: `Def-F-13-01`
- **文件**: N/A
- **消息**: 编号 Def-F-13-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\13-security\security-hardening-guide.md:7`
  - `Flink\13-security\streaming-security-best-practices.md:9`
  - `Flink\13-wasm\wasm-streaming.md:7`

### 395. duplicate_id

- **编号**: `Def-F-13-02`
- **文件**: N/A
- **消息**: 编号 Def-F-13-02 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\13-security\security-hardening-guide.md:16`
  - `Flink\13-security\streaming-security-best-practices.md:31`
  - `Flink\13-wasm\wasm-streaming.md:25`

### 396. duplicate_id

- **编号**: `Def-F-13-03`
- **文件**: N/A
- **消息**: 编号 Def-F-13-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\13-security\security-hardening-guide.md:23`
  - `Flink\13-wasm\wasm-streaming.md:56`

### 397. duplicate_id

- **编号**: `Def-F-13-04`
- **文件**: N/A
- **消息**: 编号 Def-F-13-04 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\13-security\security-hardening-guide.md:30`
  - `Flink\13-security\trusted-execution-flink.md:7`

### 398. duplicate_id

- **编号**: `Lemma-F-13-01`
- **文件**: N/A
- **消息**: 编号 Lemma-F-13-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\13-security\security-hardening-guide.md:41`
  - `Flink\13-security\streaming-security-best-practices.md:51`
  - `Flink\13-security\trusted-execution-flink.md:160`

### 399. duplicate_id

- **编号**: `Prop-F-13-01`
- **文件**: N/A
- **消息**: 编号 Prop-F-13-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\13-security\security-hardening-guide.md:68`
  - `Flink\13-wasm\wasm-streaming.md:98`

### 400. duplicate_id

- **编号**: `Thm-F-13-01`
- **文件**: N/A
- **消息**: 编号 Thm-F-13-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\13-security\streaming-security-best-practices.md:175`
  - `Flink\13-wasm\wasi-0.3-async-preview.md:620`

### 401. duplicate_id

- **编号**: `Thm-F-13-02`
- **文件**: N/A
- **消息**: 编号 Thm-F-13-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\13-security\streaming-security-best-practices.md:187`
  - `Flink\13-wasm\wasi-0.3-async-preview.md:647`

### 402. duplicate_id

- **编号**: `Prop-F-13-02`
- **文件**: N/A
- **消息**: 编号 Prop-F-13-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\13-security\trusted-execution-flink.md:139`
  - `Flink\13-wasm\wasm-streaming.md:121`

### 403. duplicate_id

- **编号**: `Prop-F-13-03`
- **文件**: N/A
- **消息**: 编号 Prop-F-13-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\13-security\trusted-execution-flink.md:152`
  - `Flink\13-wasm\wasm-streaming.md:136`

### 404. duplicate_id

- **编号**: `Def-F-14-01`
- **文件**: N/A
- **消息**: 编号 Def-F-14-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\14-lakehouse\flink-iceberg-integration.md:9`
  - `Flink\14-lakehouse\flink-paimon-integration.md:9`

### 405. duplicate_id

- **编号**: `Def-F-14-02`
- **文件**: N/A
- **消息**: 编号 Def-F-14-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\14-lakehouse\flink-iceberg-integration.md:70`
  - `Flink\14-lakehouse\flink-paimon-integration.md:31`

### 406. duplicate_id

- **编号**: `Def-F-14-03`
- **文件**: N/A
- **消息**: 编号 Def-F-14-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\14-lakehouse\flink-iceberg-integration.md:119`
  - `Flink\14-lakehouse\flink-paimon-integration.md:58`

### 407. duplicate_id

- **编号**: `Def-F-14-04`
- **文件**: N/A
- **消息**: 编号 Def-F-14-04 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\14-lakehouse\flink-iceberg-integration.md:173`
  - `Flink\14-lakehouse\flink-paimon-integration.md:115`

### 408. duplicate_id

- **编号**: `Def-F-14-05`
- **文件**: N/A
- **消息**: 编号 Def-F-14-05 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\14-lakehouse\flink-iceberg-integration.md:225`
  - `Flink\14-lakehouse\flink-paimon-integration.md:170`
  - `Flink\14-lakehouse\streaming-lakehouse-architecture.md:9`

### 409. duplicate_id

- **编号**: `Def-F-14-06`
- **文件**: N/A
- **消息**: 编号 Def-F-14-06 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\14-lakehouse\flink-iceberg-integration.md:279`
  - `Flink\14-lakehouse\flink-paimon-integration.md:214`
  - `Flink\14-lakehouse\streaming-lakehouse-architecture.md:39`

### 410. duplicate_id

- **编号**: `Lemma-F-14-01`
- **文件**: N/A
- **消息**: 编号 Lemma-F-14-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\14-lakehouse\flink-iceberg-integration.md:320`
  - `Flink\14-lakehouse\flink-paimon-integration.md:245`

### 411. duplicate_id

- **编号**: `Prop-F-14-01`
- **文件**: N/A
- **消息**: 编号 Prop-F-14-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\14-lakehouse\flink-iceberg-integration.md:356`
  - `Flink\14-lakehouse\flink-paimon-integration.md:316`

### 412. duplicate_id

- **编号**: `Prop-F-14-02`
- **文件**: N/A
- **消息**: 编号 Prop-F-14-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\14-lakehouse\flink-iceberg-integration.md:389`
  - `Flink\14-lakehouse\flink-paimon-integration.md:357`

### 413. duplicate_id

- **编号**: `Thm-F-14-01`
- **文件**: N/A
- **消息**: 编号 Thm-F-14-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\14-lakehouse\flink-iceberg-integration.md:787`
  - `Flink\14-lakehouse\flink-paimon-integration.md:602`

### 414. duplicate_id

- **编号**: `Thm-F-14-02`
- **文件**: N/A
- **消息**: 编号 Thm-F-14-02 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\14-lakehouse\flink-iceberg-integration.md:852`
  - `Flink\14-lakehouse\flink-paimon-integration.md:657`

### 415. duplicate_id

- **编号**: `Thm-F-14-03`
- **文件**: N/A
- **消息**: 编号 Thm-F-14-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\14-lakehouse\flink-iceberg-integration.md:905`
  - `Flink\14-lakehouse\flink-paimon-integration.md:710`

### 416. duplicate_id

- **编号**: `Prop-F-15-01`
- **文件**: N/A
- **消息**: 编号 Prop-F-15-01 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\15-observability\distributed-tracing.md:142`
  - `Flink\15-observability\event-reporting.md:126`
  - `Flink\15-observability\metrics-and-monitoring.md:80`

### 417. duplicate_id

- **编号**: `Lemma-F-15-01`
- **文件**: N/A
- **消息**: 编号 Lemma-F-15-01 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\15-observability\distributed-tracing.md:155`
  - `Flink\15-observability\opentelemetry-streaming-observability.md:142`

### 418. duplicate_id

- **编号**: `Prop-F-15-02`
- **文件**: N/A
- **消息**: 编号 Prop-F-15-02 在多个文件中重复定义 (3 个文件)
- **位置**:
  - `Flink\15-observability\distributed-tracing.md:171`
  - `Flink\15-observability\event-reporting.md:140`
  - `Flink\15-observability\metrics-and-monitoring.md:96`

### 419. duplicate_id

- **编号**: `Def-F-15-12`
- **文件**: N/A
- **消息**: 编号 Def-F-15-12 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\15-observability\event-reporting.md:9`
  - `Flink\15-observability\opentelemetry-streaming-observability.md:68`

### 420. duplicate_id

- **编号**: `Def-F-15-13`
- **文件**: N/A
- **消息**: 编号 Def-F-15-13 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\15-observability\event-reporting.md:52`
  - `Flink\15-observability\opentelemetry-streaming-observability.md:89`

### 421. duplicate_id

- **编号**: `Def-F-15-14`
- **文件**: N/A
- **消息**: 编号 Def-F-15-14 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\15-observability\event-reporting.md:89`
  - `Flink\15-observability\opentelemetry-streaming-observability.md:120`

### 422. duplicate_id

- **编号**: `Prop-F-15-03`
- **文件**: N/A
- **消息**: 编号 Prop-F-15-03 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\15-observability\event-reporting.md:154`
  - `Flink\15-observability\metrics-and-monitoring.md:107`

### 423. duplicate_id

- **编号**: `Def-F-15-10`
- **文件**: N/A
- **消息**: 编号 Def-F-15-10 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\15-observability\opentelemetry-streaming-observability.md:9`
  - `Flink\15-observability\split-level-watermark-metrics.md:26`

### 424. duplicate_id

- **编号**: `Def-F-15-11`
- **文件**: N/A
- **消息**: 编号 Def-F-15-11 在多个文件中重复定义 (2 个文件)
- **位置**:
  - `Flink\15-observability\opentelemetry-streaming-observability.md:34`
  - `Flink\15-observability\split-level-watermark-metrics.md:49`

### 425. unregistered

- **编号**: `Def-F-02-14`
- **文件**: N/A
- **消息**: 编号 Def-F-02-14 未在注册表中登记
- **位置**:
  - `Flink\02-core-mechanisms\state-backends-deep-comparison.md:22`

### 426. unregistered

- **编号**: `Def-F-02-16`
- **文件**: N/A
- **消息**: 编号 Def-F-02-16 未在注册表中登记
- **位置**:
  - `Flink\02-core-mechanisms\state-backends-deep-comparison.md:66`

### 427. unregistered

- **编号**: `Def-F-02-17`
- **文件**: N/A
- **消息**: 编号 Def-F-02-17 未在注册表中登记
- **位置**:
  - `Flink\02-core-mechanisms\state-backends-deep-comparison.md:78`

### 428. unregistered

- **编号**: `Def-F-02-18`
- **文件**: N/A
- **消息**: 编号 Def-F-02-18 未在注册表中登记
- **位置**:
  - `Flink\02-core-mechanisms\state-backends-deep-comparison.md:94`

### 429. unregistered

- **编号**: `Def-F-02-19`
- **文件**: N/A
- **消息**: 编号 Def-F-02-19 未在注册表中登记
- **位置**:
  - `Flink\02-core-mechanisms\state-backends-deep-comparison.md:123`

### 430. unregistered

- **编号**: `Def-F-03-11`
- **文件**: N/A
- **消息**: 编号 Def-F-03-11 未在注册表中登记
- **位置**:
  - `Flink\03-sql-table-api\data-types-complete-reference.md:196`

### 431. unregistered

- **编号**: `Def-F-03-12`
- **文件**: N/A
- **消息**: 编号 Def-F-03-12 未在注册表中登记
- **位置**:
  - `Flink\03-sql-table-api\data-types-complete-reference.md:208`

### 432. unregistered

- **编号**: `Def-F-03-13`
- **文件**: N/A
- **消息**: 编号 Def-F-03-13 未在注册表中登记
- **位置**:
  - `Flink\03-sql-table-api\data-types-complete-reference.md:233`

### 433. unregistered

- **编号**: `Def-F-03-14`
- **文件**: N/A
- **消息**: 编号 Def-F-03-14 未在注册表中登记
- **位置**:
  - `Flink\03-sql-table-api\data-types-complete-reference.md:255`

### 434. unregistered

- **编号**: `Def-F-04-06`
- **文件**: N/A
- **消息**: 编号 Def-F-04-06 未在注册表中登记
- **位置**:
  - `Flink\04-connectors\mongodb-connector-complete-guide.md:54`

### 435. unregistered

- **编号**: `Def-F-04-07`
- **文件**: N/A
- **消息**: 编号 Def-F-04-07 未在注册表中登记
- **位置**:
  - `Flink\04-connectors\mongodb-connector-complete-guide.md:70`

### 436. unregistered

- **编号**: `Def-F-04-08`
- **文件**: N/A
- **消息**: 编号 Def-F-04-08 未在注册表中登记
- **位置**:
  - `Flink\04-connectors\mongodb-connector-complete-guide.md:87`

### 437. unregistered

- **编号**: `Def-F-04-09`
- **文件**: N/A
- **消息**: 编号 Def-F-04-09 未在注册表中登记
- **位置**:
  - `Flink\04-connectors\mongodb-connector-complete-guide.md:121`

### 438. unregistered

- **编号**: `Def-F-04-23`
- **文件**: N/A
- **消息**: 编号 Def-F-04-23 未在注册表中登记
- **位置**:
  - `Flink\04-connectors\cloudevents-integration-guide.md:151`

### 439. unregistered

- **编号**: `Def-F-06-07`
- **文件**: N/A
- **消息**: 编号 Def-F-06-07 未在注册表中登记
- **位置**:
  - `Flink\06-engineering\06.02-performance-optimization-complete.md:111`

### 440. unregistered

- **编号**: `Def-F-06-08`
- **文件**: N/A
- **消息**: 编号 Def-F-06-08 未在注册表中登记
- **位置**:
  - `Flink\06-engineering\06.02-performance-optimization-complete.md:126`

### 441. unregistered

- **编号**: `Def-F-06-09`
- **文件**: N/A
- **消息**: 编号 Def-F-06-09 未在注册表中登记
- **位置**:
  - `Flink\06-engineering\06.02-performance-optimization-complete.md:142`

### 442. unregistered

- **编号**: `Def-F-08-45`
- **文件**: N/A
- **消息**: 编号 Def-F-08-45 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\community-dynamics-tracking.md:9`

### 443. unregistered

- **编号**: `Def-F-08-46`
- **文件**: N/A
- **消息**: 编号 Def-F-08-46 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\community-dynamics-tracking.md:33`

### 444. unregistered

- **编号**: `Def-F-08-47`
- **文件**: N/A
- **消息**: 编号 Def-F-08-47 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\community-dynamics-tracking.md:52`

### 445. unregistered

- **编号**: `Def-F-08-48`
- **文件**: N/A
- **消息**: 编号 Def-F-08-48 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\community-dynamics-tracking.md:78`

### 446. unregistered

- **编号**: `Def-F-08-65`
- **文件**: N/A
- **消息**: 编号 Def-F-08-65 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\flink-version-comparison-matrix.md:11`

### 447. unregistered

- **编号**: `Def-F-08-66`
- **文件**: N/A
- **消息**: 编号 Def-F-08-66 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\flink-version-comparison-matrix.md:27`

### 448. unregistered

- **编号**: `Def-F-08-67`
- **文件**: N/A
- **消息**: 编号 Def-F-08-67 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\flink-version-comparison-matrix.md:39`

### 449. unregistered

- **编号**: `Def-F-08-68`
- **文件**: N/A
- **消息**: 编号 Def-F-08-68 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\flink-version-comparison-matrix.md:70`

### 450. unregistered

- **编号**: `Def-F-08-69`
- **文件**: N/A
- **消息**: 编号 Def-F-08-69 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\flink-version-comparison-matrix.md:83`

### 451. unregistered

- **编号**: `Def-F-08-70`
- **文件**: N/A
- **消息**: 编号 Def-F-08-70 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\flink-2.4-tracking.md:16`

### 452. unregistered

- **编号**: `Def-F-08-71`
- **文件**: N/A
- **消息**: 编号 Def-F-08-71 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\flink-2.4-tracking.md:32`

### 453. unregistered

- **编号**: `Def-F-08-72`
- **文件**: N/A
- **消息**: 编号 Def-F-08-72 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\flink-2.4-tracking.md:59`

### 454. unregistered

- **编号**: `Def-F-08-73`
- **文件**: N/A
- **消息**: 编号 Def-F-08-73 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\flink-2.4-tracking.md:90`

### 455. unregistered

- **编号**: `Def-F-08-74`
- **文件**: N/A
- **消息**: 编号 Def-F-08-74 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\flink-2.4-tracking.md:120`

### 456. unregistered

- **编号**: `Def-F-08-75`
- **文件**: N/A
- **消息**: 编号 Def-F-08-75 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\flink-2.4-tracking.md:146`

### 457. unregistered

- **编号**: `Def-F-08-76`
- **文件**: N/A
- **消息**: 编号 Def-F-08-76 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\flink-2.4-tracking.md:179`

### 458. unregistered

- **编号**: `Def-F-10-04`
- **文件**: N/A
- **消息**: 编号 Def-F-10-04 未在注册表中登记
- **位置**:
  - `Flink\10-deployment\cost-optimization-calculator.md:54`

### 459. unregistered

- **编号**: `Def-F-10-05`
- **文件**: N/A
- **消息**: 编号 Def-F-10-05 未在注册表中登记
- **位置**:
  - `Flink\10-deployment\cost-optimization-calculator.md:64`

### 460. unregistered

- **编号**: `Def-F-10-56`
- **文件**: N/A
- **消息**: 编号 Def-F-10-56 未在注册表中登记
- **位置**:
  - `Flink\10-deployment\flink-24-deployment-improvements.md:414`

### 461. unregistered

- **编号**: `Def-F-10-57`
- **文件**: N/A
- **消息**: 编号 Def-F-10-57 未在注册表中登记
- **位置**:
  - `Flink\10-deployment\flink-24-deployment-improvements.md:494`

### 462. unregistered

- **编号**: `Def-F-10-58`
- **文件**: N/A
- **消息**: 编号 Def-F-10-58 未在注册表中登记
- **位置**:
  - `Flink\10-deployment\flink-24-deployment-improvements.md:561`

### 463. unregistered

- **编号**: `Def-F-10-59`
- **文件**: N/A
- **消息**: 编号 Def-F-10-59 未在注册表中登记
- **位置**:
  - `Flink\10-deployment\flink-24-deployment-improvements.md:621`

### 464. unregistered

- **编号**: `Def-F-11-20`
- **文件**: N/A
- **消息**: 编号 Def-F-11-20 未在注册表中登记
- **位置**:
  - `Flink\11-benchmarking\flink-24-25-benchmark-results.md:7`

### 465. unregistered

- **编号**: `Def-F-11-21`
- **文件**: N/A
- **消息**: 编号 Def-F-11-21 未在注册表中登记
- **位置**:
  - `Flink\11-benchmarking\flink-24-25-benchmark-results.md:19`

### 466. unregistered

- **编号**: `Def-F-11-22`
- **文件**: N/A
- **消息**: 编号 Def-F-11-22 未在注册表中登记
- **位置**:
  - `Flink\11-benchmarking\flink-24-25-benchmark-results.md:39`

### 467. unregistered

- **编号**: `Def-F-13-30`
- **文件**: N/A
- **消息**: 编号 Def-F-13-30 未在注册表中登记
- **位置**:
  - `Flink\13-security\spiffe-spire-integration-guide.md:9`

### 468. unregistered

- **编号**: `Def-F-13-31`
- **文件**: N/A
- **消息**: 编号 Def-F-13-31 未在注册表中登记
- **位置**:
  - `Flink\13-security\spiffe-spire-integration-guide.md:41`

### 469. unregistered

- **编号**: `Def-F-13-32`
- **文件**: N/A
- **消息**: 编号 Def-F-13-32 未在注册表中登记
- **位置**:
  - `Flink\13-security\spiffe-spire-integration-guide.md:92`

### 470. unregistered

- **编号**: `Def-F-13-33`
- **文件**: N/A
- **消息**: 编号 Def-F-13-33 未在注册表中登记
- **位置**:
  - `Flink\13-security\spiffe-spire-integration-guide.md:123`

### 471. unregistered

- **编号**: `Def-K-02-07-01`
- **文件**: N/A
- **消息**: 编号 Def-K-02-07-01 未在注册表中登记
- **位置**:
  - `Knowledge\02-design-patterns\pattern-checkpoint-recovery.md:56`

### 472. unregistered

- **编号**: `Def-K-02-07-02`
- **文件**: N/A
- **消息**: 编号 Def-K-02-07-02 未在注册表中登记
- **位置**:
  - `Knowledge\02-design-patterns\pattern-checkpoint-recovery.md:87`

### 473. unregistered

- **编号**: `Def-K-02-07-03`
- **文件**: N/A
- **消息**: 编号 Def-K-02-07-03 未在注册表中登记
- **位置**:
  - `Knowledge\02-design-patterns\pattern-checkpoint-recovery.md:113`

### 474. unregistered

- **编号**: `Def-K-02-07-04`
- **文件**: N/A
- **消息**: 编号 Def-K-02-07-04 未在注册表中登记
- **位置**:
  - `Knowledge\02-design-patterns\pattern-checkpoint-recovery.md:142`

### 475. unregistered

- **编号**: `Def-K-02-07-05`
- **文件**: N/A
- **消息**: 编号 Def-K-02-07-05 未在注册表中登记
- **位置**:
  - `Knowledge\02-design-patterns\pattern-checkpoint-recovery.md:160`

### 476. unregistered

- **编号**: `Def-K-05-13-01`
- **文件**: N/A
- **消息**: 编号 Def-K-05-13-01 未在注册表中登记
- **位置**:
  - `Knowledge\05-migrations\kafka-streams-to-flink-guide.md:7`

### 477. unregistered

- **编号**: `Def-K-05-13-02`
- **文件**: N/A
- **消息**: 编号 Def-K-05-13-02 未在注册表中登记
- **位置**:
  - `Knowledge\05-migrations\kafka-streams-to-flink-guide.md:23`

### 478. unregistered

- **编号**: `Def-K-05-13-03`
- **文件**: N/A
- **消息**: 编号 Def-K-05-13-03 未在注册表中登记
- **位置**:
  - `Knowledge\05-migrations\kafka-streams-to-flink-guide.md:37`

### 479. unregistered

- **编号**: `Def-K-05-13-04`
- **文件**: N/A
- **消息**: 编号 Def-K-05-13-04 未在注册表中登记
- **位置**:
  - `Knowledge\05-migrations\kafka-streams-to-flink-guide.md:48`

### 480. unregistered

- **编号**: `Lemma-F-02-06`
- **文件**: N/A
- **消息**: 编号 Lemma-F-02-06 未在注册表中登记
- **位置**:
  - `Flink\02-core-mechanisms\state-backends-deep-comparison.md:180`

### 481. unregistered

- **编号**: `Lemma-F-02-07`
- **文件**: N/A
- **消息**: 编号 Lemma-F-02-07 未在注册表中登记
- **位置**:
  - `Flink\02-core-mechanisms\state-backends-deep-comparison.md:202`

### 482. unregistered

- **编号**: `Lemma-F-03-03`
- **文件**: N/A
- **消息**: 编号 Lemma-F-03-03 未在注册表中登记
- **位置**:
  - `Flink\03-sql-table-api\data-types-complete-reference.md:279`

### 483. unregistered

- **编号**: `Lemma-F-04-03`
- **文件**: N/A
- **消息**: 编号 Lemma-F-04-03 未在注册表中登记
- **位置**:
  - `Flink\04-connectors\mongodb-connector-complete-guide.md:168`

### 484. unregistered

- **编号**: `Lemma-F-04-04`
- **文件**: N/A
- **消息**: 编号 Lemma-F-04-04 未在注册表中登记
- **位置**:
  - `Flink\04-connectors\mongodb-connector-complete-guide.md:186`

### 485. unregistered

- **编号**: `Lemma-F-06-05`
- **文件**: N/A
- **消息**: 编号 Lemma-F-06-05 未在注册表中登记
- **位置**:
  - `Flink\06-engineering\06.02-performance-optimization-complete.md:163`

### 486. unregistered

- **编号**: `Lemma-F-06-06`
- **文件**: N/A
- **消息**: 编号 Lemma-F-06-06 未在注册表中登记
- **位置**:
  - `Flink\06-engineering\06.02-performance-optimization-complete.md:182`

### 487. unregistered

- **编号**: `Lemma-F-06-07`
- **文件**: N/A
- **消息**: 编号 Lemma-F-06-07 未在注册表中登记
- **位置**:
  - `Flink\06-engineering\06.02-performance-optimization-complete.md:199`

### 488. unregistered

- **编号**: `Lemma-F-06-08`
- **文件**: N/A
- **消息**: 编号 Lemma-F-06-08 未在注册表中登记
- **位置**:
  - `Flink\06-engineering\06.02-performance-optimization-complete.md:209`

### 489. unregistered

- **编号**: `Lemma-F-08-41`
- **文件**: N/A
- **消息**: 编号 Lemma-F-08-41 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\community-dynamics-tracking.md:145`

### 490. unregistered

- **编号**: `Lemma-F-08-70`
- **文件**: N/A
- **消息**: 编号 Lemma-F-08-70 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\flink-2.4-tracking.md:236`

### 491. unregistered

- **编号**: `Lemma-F-08-71`
- **文件**: N/A
- **消息**: 编号 Lemma-F-08-71 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\flink-2.4-tracking.md:250`

### 492. unregistered

- **编号**: `Lemma-F-10-01`
- **文件**: N/A
- **消息**: 编号 Lemma-F-10-01 未在注册表中登记
- **位置**:
  - `Flink\10-deployment\cost-optimization-calculator.md:114`

### 493. unregistered

- **编号**: `Lemma-F-10-52`
- **文件**: N/A
- **消息**: 编号 Lemma-F-10-52 未在注册表中登记
- **位置**:
  - `Flink\10-deployment\flink-24-deployment-improvements.md:741`

### 494. unregistered

- **编号**: `Lemma-F-10-53`
- **文件**: N/A
- **消息**: 编号 Lemma-F-10-53 未在注册表中登记
- **位置**:
  - `Flink\10-deployment\flink-24-deployment-improvements.md:763`

### 495. unregistered

- **编号**: `Lemma-F-11-01`
- **文件**: N/A
- **消息**: 编号 Lemma-F-11-01 未在注册表中登记
- **位置**:
  - `Flink\11-benchmarking\performance-benchmarking-guide.md:50`

### 496. unregistered

- **编号**: `Lemma-F-11-02`
- **文件**: N/A
- **消息**: 编号 Lemma-F-11-02 未在注册表中登记
- **位置**:
  - `Flink\11-benchmarking\performance-benchmarking-guide.md:59`

### 497. unregistered

- **编号**: `Lemma-F-12-50`
- **文件**: N/A
- **消息**: 编号 Lemma-F-12-50 未在注册表中登记
- **位置**:
  - `Flink\12-ai-ml\flink-25-gpu-acceleration.md:244`

### 498. unregistered

- **编号**: `Lemma-F-12-51`
- **文件**: N/A
- **消息**: 编号 Lemma-F-12-51 未在注册表中登记
- **位置**:
  - `Flink\12-ai-ml\flink-25-gpu-acceleration.md:266`

### 499. unregistered

- **编号**: `Lemma-F-13-18`
- **文件**: N/A
- **消息**: 编号 Lemma-F-13-18 未在注册表中登记
- **位置**:
  - `Flink\13-security\spiffe-spire-integration-guide.md:160`

### 500. unregistered

- **编号**: `Lemma-F-13-19`
- **文件**: N/A
- **消息**: 编号 Lemma-F-13-19 未在注册表中登记
- **位置**:
  - `Flink\13-security\spiffe-spire-integration-guide.md:188`

### 501. unregistered

- **编号**: `Lemma-K-02-07-01`
- **文件**: N/A
- **消息**: 编号 Lemma-K-02-07-01 未在注册表中登记
- **位置**:
  - `Knowledge\02-design-patterns\pattern-checkpoint-recovery.md:191`

### 502. unregistered

- **编号**: `Lemma-K-02-07-02`
- **文件**: N/A
- **消息**: 编号 Lemma-K-02-07-02 未在注册表中登记
- **位置**:
  - `Knowledge\02-design-patterns\pattern-checkpoint-recovery.md:211`

### 503. unregistered

- **编号**: `Lemma-K-05-02-01`
- **文件**: N/A
- **消息**: 编号 Lemma-K-05-02-01 未在注册表中登记
- **位置**:
  - `Knowledge\05-mapping-guides\migration-guides\05.2-kafka-streams-to-flink-migration.md:67`

### 504. unregistered

- **编号**: `Lemma-K-05-03-01`
- **文件**: N/A
- **消息**: 编号 Lemma-K-05-03-01 未在注册表中登记
- **位置**:
  - `Knowledge\05-mapping-guides\migration-guides\05.3-storm-to-flink-migration.md:80`

### 505. unregistered

- **编号**: `Lemma-K-05-04-01`
- **文件**: N/A
- **消息**: 编号 Lemma-K-05-04-01 未在注册表中登记
- **位置**:
  - `Knowledge\05-mapping-guides\migration-guides\05.4-flink-1x-to-2x-migration.md:52`

### 506. unregistered

- **编号**: `Lemma-K-05-05-01`
- **文件**: N/A
- **消息**: 编号 Lemma-K-05-05-01 未在注册表中登记
- **位置**:
  - `Knowledge\05-mapping-guides\migration-guides\05.5-batch-to-streaming-migration.md:85`

### 507. unregistered

- **编号**: `Lemma-K-05-13-01`
- **文件**: N/A
- **消息**: 编号 Lemma-K-05-13-01 未在注册表中登记
- **位置**:
  - `Knowledge\05-migrations\kafka-streams-to-flink-guide.md:85`

### 508. unregistered

- **编号**: `Lemma-K-06-21`
- **文件**: N/A
- **消息**: 编号 Lemma-K-06-21 未在注册表中登记
- **位置**:
  - `Knowledge\06-frontier\materialize-comparison-guide.md:196`

### 509. unregistered

- **编号**: `Lemma-S-01-01`
- **文件**: N/A
- **消息**: 编号 Lemma-S-01-01 未在注册表中登记
- **位置**:
  - `Struct\01-foundation\stream-processing-semantics-formalization.md:128`

### 510. unregistered

- **编号**: `Prop-F-02-06`
- **文件**: N/A
- **消息**: 编号 Prop-F-02-06 未在注册表中登记
- **位置**:
  - `Flink\02-core-mechanisms\state-backends-deep-comparison.md:237`

### 511. unregistered

- **编号**: `Prop-F-07-02`
- **文件**: N/A
- **消息**: 编号 Prop-F-07-02 未在注册表中登记
- **位置**:
  - `Flink\07-operations\rest-api-complete-reference.md:50`

### 512. unregistered

- **编号**: `Prop-F-08-42`
- **文件**: N/A
- **消息**: 编号 Prop-F-08-42 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\community-dynamics-tracking.md:105`

### 513. unregistered

- **编号**: `Prop-F-08-43`
- **文件**: N/A
- **消息**: 编号 Prop-F-08-43 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\community-dynamics-tracking.md:126`

### 514. unregistered

- **编号**: `Prop-F-08-70`
- **文件**: N/A
- **消息**: 编号 Prop-F-08-70 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\flink-2.4-tracking.md:211`

### 515. unregistered

- **编号**: `Prop-F-08-71`
- **文件**: N/A
- **消息**: 编号 Prop-F-08-71 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\flink-2.4-tracking.md:224`

### 516. unregistered

- **编号**: `Prop-F-11-20`
- **文件**: N/A
- **消息**: 编号 Prop-F-11-20 未在注册表中登记
- **位置**:
  - `Flink\11-benchmarking\flink-24-25-benchmark-results.md:60`

### 517. unregistered

- **编号**: `Prop-F-11-21`
- **文件**: N/A
- **消息**: 编号 Prop-F-11-21 未在注册表中登记
- **位置**:
  - `Flink\11-benchmarking\flink-24-25-benchmark-results.md:81`

### 518. unregistered

- **编号**: `Prop-F-11-22`
- **文件**: N/A
- **消息**: 编号 Prop-F-11-22 未在注册表中登记
- **位置**:
  - `Flink\11-benchmarking\flink-24-25-benchmark-results.md:101`

### 519. unregistered

- **编号**: `Prop-F-12-51`
- **文件**: N/A
- **消息**: 编号 Prop-F-12-51 未在注册表中登记
- **位置**:
  - `Flink\12-ai-ml\flink-25-gpu-acceleration.md:219`

### 520. unregistered

- **编号**: `Prop-F-13-12`
- **文件**: N/A
- **消息**: 编号 Prop-F-13-12 未在注册表中登记
- **位置**:
  - `Flink\13-security\spiffe-spire-integration-guide.md:221`

### 521. unregistered

- **编号**: `Prop-K-02-07-01`
- **文件**: N/A
- **消息**: 编号 Prop-K-02-07-01 未在注册表中登记
- **位置**:
  - `Knowledge\02-design-patterns\pattern-checkpoint-recovery.md:233`

### 522. unregistered

- **编号**: `Prop-K-05-13-01`
- **文件**: N/A
- **消息**: 编号 Prop-K-05-13-01 未在注册表中登记
- **位置**:
  - `Knowledge\05-migrations\kafka-streams-to-flink-guide.md:62`

### 523. unregistered

- **编号**: `Prop-K-05-13-02`
- **文件**: N/A
- **消息**: 编号 Prop-K-05-13-02 未在注册表中登记
- **位置**:
  - `Knowledge\05-migrations\kafka-streams-to-flink-guide.md:76`

### 524. unregistered

- **编号**: `Thm-F-02-04`
- **文件**: N/A
- **消息**: 编号 Thm-F-02-04 未在注册表中登记
- **位置**:
  - `Flink\02-core-mechanisms\state-backends-deep-comparison.md:438`

### 525. unregistered

- **编号**: `Thm-F-04-03`
- **文件**: N/A
- **消息**: 编号 Thm-F-04-03 未在注册表中登记
- **位置**:
  - `Flink\04-connectors\mongodb-connector-complete-guide.md:392`

### 526. unregistered

- **编号**: `Thm-F-04-04`
- **文件**: N/A
- **消息**: 编号 Thm-F-04-04 未在注册表中登记
- **位置**:
  - `Flink\04-connectors\mongodb-connector-complete-guide.md:432`

### 527. unregistered

- **编号**: `Thm-F-06-03`
- **文件**: N/A
- **消息**: 编号 Thm-F-06-03 未在注册表中登记
- **位置**:
  - `Flink\06-engineering\06.02-performance-optimization-complete.md:366`

### 528. unregistered

- **编号**: `Thm-F-06-04`
- **文件**: N/A
- **消息**: 编号 Thm-F-06-04 未在注册表中登记
- **位置**:
  - `Flink\06-engineering\06.02-performance-optimization-complete.md:395`

### 529. unregistered

- **编号**: `Thm-F-08-70`
- **文件**: N/A
- **消息**: 编号 Thm-F-08-70 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\flink-2.4-tracking.md:370`

### 530. unregistered

- **编号**: `Thm-F-08-71`
- **文件**: N/A
- **消息**: 编号 Thm-F-08-71 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\flink-2.4-tracking.md:385`

### 531. unregistered

- **编号**: `Thm-F-08-72`
- **文件**: N/A
- **消息**: 编号 Thm-F-08-72 未在注册表中登记
- **位置**:
  - `Flink\08-roadmap\flink-2.4-tracking.md:401`

### 532. unregistered

- **编号**: `Thm-F-10-01`
- **文件**: N/A
- **消息**: 编号 Thm-F-10-01 未在注册表中登记
- **位置**:
  - `Flink\10-deployment\cost-optimization-calculator.md:235`

### 533. unregistered

- **编号**: `Thm-F-10-02`
- **文件**: N/A
- **消息**: 编号 Thm-F-10-02 未在注册表中登记
- **位置**:
  - `Flink\10-deployment\cost-optimization-calculator.md:260`

### 534. unregistered

- **编号**: `Thm-F-10-03`
- **文件**: N/A
- **消息**: 编号 Thm-F-10-03 未在注册表中登记
- **位置**:
  - `Flink\10-deployment\cost-optimization-calculator.md:281`

### 535. unregistered

- **编号**: `Thm-F-12-51`
- **文件**: N/A
- **消息**: 编号 Thm-F-12-51 未在注册表中登记
- **位置**:
  - `Flink\12-ai-ml\flink-25-gpu-acceleration.md:492`

### 536. unregistered

- **编号**: `Thm-F-12-52`
- **文件**: N/A
- **消息**: 编号 Thm-F-12-52 未在注册表中登记
- **位置**:
  - `Flink\12-ai-ml\flink-25-gpu-acceleration.md:541`

### 537. unregistered

- **编号**: `Thm-F-13-07`
- **文件**: N/A
- **消息**: 编号 Thm-F-13-07 未在注册表中登记
- **位置**:
  - `Flink\13-security\spiffe-spire-integration-guide.md:365`

### 538. unregistered

- **编号**: `Thm-K-05-13-01`
- **文件**: N/A
- **消息**: 编号 Thm-K-05-13-01 未在注册表中登记
- **位置**:
  - `Knowledge\05-migrations\kafka-streams-to-flink-guide.md:281`

### 539. unregistered

- **编号**: `Thm-K-06-20`
- **文件**: N/A
- **消息**: 编号 Thm-K-06-20 未在注册表中登记
- **位置**:
  - `Knowledge\06-frontier\materialize-comparison-guide.md:577`

### 540. unregistered

- **编号**: `Thm-S-20-02`
- **文件**: N/A
- **消息**: 编号 Thm-S-20-02 未在注册表中登记
- **位置**:
  - `Struct\06-frontier\06.02-choreographic-streaming-programming.md:844`


---

## ⚠️ 警告摘要 (1049)

| # | 类型 | 编号 | 消息 |
|---|------|------|------|
| 1 | duplicate_definition_same_file | `Def-S-09-02` | 编号 Def-S-09-02 在同一文件中定义了 2 次... |
| 2 | duplicate_definition_same_file | `Lemma-S-16-01` | 编号 Lemma-S-16-01 在同一文件中定义了 2 次... |
| 3 | duplicate_definition_same_file | `Lemma-S-16-02` | 编号 Lemma-S-16-02 在同一文件中定义了 2 次... |
| 4 | duplicate_definition_same_file | `Prop-S-16-01` | 编号 Prop-S-16-01 在同一文件中定义了 3 次... |
| 5 | duplicate_definition_same_file | `Prop-S-16-03` | 编号 Prop-S-16-03 在同一文件中定义了 2 次... |
| 6 | duplicate_definition_same_file | `Thm-S-16-01` | 编号 Thm-S-16-01 在同一文件中定义了 2 次... |
| 7 | duplicate_definition_same_file | `Lemma-S-17-04` | 编号 Lemma-S-17-04 在同一文件中定义了 2 次... |
| 8 | duplicate_definition_same_file | `Def-S-19-02` | 编号 Def-S-19-02 在同一文件中定义了 2 次... |
| 9 | duplicate_definition_same_file | `Lemma-S-19-02` | 编号 Lemma-S-19-02 在同一文件中定义了 2 次... |
| 10 | duplicate_definition_same_file | `Lemma-S-19-04` | 编号 Lemma-S-19-04 在同一文件中定义了 2 次... |
| 11 | duplicate_definition_same_file | `Thm-S-22-01` | 编号 Thm-S-22-01 在同一文件中定义了 2 次... |
| 12 | duplicate_definition_same_file | `Lemma-S-23-01` | 编号 Lemma-S-23-01 在同一文件中定义了 2 次... |
| 13 | duplicate_definition_same_file | `Thm-S-23-01` | 编号 Thm-S-23-01 在同一文件中定义了 2 次... |
| 14 | duplicate_definition_same_file | `Def-S-29-02` | 编号 Def-S-29-02 在同一文件中定义了 2 次... |
| 15 | duplicate_definition_same_file | `Thm-F-09-11` | 编号 Thm-F-09-11 在同一文件中定义了 4 次... |
| 16 | duplicate_definition_same_file | `Thm-F-09-12` | 编号 Thm-F-09-12 在同一文件中定义了 2 次... |
| 17 | duplicate_definition_same_file | `Lemma-F-09-16` | 编号 Lemma-F-09-16 在同一文件中定义了 2 次... |
| 18 | duplicate_definition_same_file | `Prop-F-09-21` | 编号 Prop-F-09-21 在同一文件中定义了 2 次... |
| 19 | orphaned_registry_entry | `Cor-F-02-01` | 注册表条目 Cor-F-02-01 在文档中未找到（可能已被删除）... |
| 20 | orphaned_registry_entry | `Cor-F-06-01` | 注册表条目 Cor-F-06-01 在文档中未找到（可能已被删除）... |
| 21 | orphaned_registry_entry | `Cor-F-06-02` | 注册表条目 Cor-F-06-02 在文档中未找到（可能已被删除）... |
| 22 | orphaned_registry_entry | `Cor-F-06-03` | 注册表条目 Cor-F-06-03 在文档中未找到（可能已被删除）... |
| 23 | orphaned_registry_entry | `Cor-F-06-50` | 注册表条目 Cor-F-06-50 在文档中未找到（可能已被删除）... |
| 24 | orphaned_registry_entry | `Cor-F-07-05` | 注册表条目 Cor-F-07-05 在文档中未找到（可能已被删除）... |
| 25 | orphaned_registry_entry | `Cor-F-12-05` | 注册表条目 Cor-F-12-05 在文档中未找到（可能已被删除）... |
| 26 | orphaned_registry_entry | `Cor-K-06-05` | 注册表条目 Cor-K-06-05 在文档中未找到（可能已被删除）... |
| 27 | orphaned_registry_entry | `Cor-S-02-04` | 注册表条目 Cor-S-02-04 在文档中未找到（可能已被删除）... |
| 28 | orphaned_registry_entry | `Cor-S-02-05` | 注册表条目 Cor-S-02-05 在文档中未找到（可能已被删除）... |
| 29 | orphaned_registry_entry | `Cor-S-02-06` | 注册表条目 Cor-S-02-06 在文档中未找到（可能已被删除）... |
| 30 | orphaned_registry_entry | `Cor-S-04-01` | 注册表条目 Cor-S-04-01 在文档中未找到（可能已被删除）... |
| 31 | orphaned_registry_entry | `Cor-S-04-02` | 注册表条目 Cor-S-04-02 在文档中未找到（可能已被删除）... |
| 32 | orphaned_registry_entry | `Cor-S-07-01` | 注册表条目 Cor-S-07-01 在文档中未找到（可能已被删除）... |
| 33 | orphaned_registry_entry | `Cor-S-07-02` | 注册表条目 Cor-S-07-02 在文档中未找到（可能已被删除）... |
| 34 | orphaned_registry_entry | `Cor-S-07-03` | 注册表条目 Cor-S-07-03 在文档中未找到（可能已被删除）... |
| 35 | orphaned_registry_entry | `Cor-S-23-01` | 注册表条目 Cor-S-23-01 在文档中未找到（可能已被删除）... |
| 36 | orphaned_registry_entry | `Cor-S-29-01` | 注册表条目 Cor-S-29-01 在文档中未找到（可能已被删除）... |
| 37 | orphaned_registry_entry | `Def-F-02-110` | 注册表条目 Def-F-02-110 在文档中未找到（可能已被删除）... |
| 38 | orphaned_registry_entry | `Def-F-02-111` | 注册表条目 Def-F-02-111 在文档中未找到（可能已被删除）... |
| 39 | orphaned_registry_entry | `Def-F-02-112` | 注册表条目 Def-F-02-112 在文档中未找到（可能已被删除）... |
| 40 | orphaned_registry_entry | `Def-F-02-113` | 注册表条目 Def-F-02-113 在文档中未找到（可能已被删除）... |
| 41 | orphaned_registry_entry | `Def-F-02-114` | 注册表条目 Def-F-02-114 在文档中未找到（可能已被删除）... |
| 42 | orphaned_registry_entry | `Def-F-02-115` | 注册表条目 Def-F-02-115 在文档中未找到（可能已被删除）... |
| 43 | orphaned_registry_entry | `Def-F-02-116` | 注册表条目 Def-F-02-116 在文档中未找到（可能已被删除）... |
| 44 | orphaned_registry_entry | `Def-F-02-117` | 注册表条目 Def-F-02-117 在文档中未找到（可能已被删除）... |
| 45 | orphaned_registry_entry | `Def-F-02-21` | 注册表条目 Def-F-02-21 在文档中未找到（可能已被删除）... |
| 46 | orphaned_registry_entry | `Def-F-02-22` | 注册表条目 Def-F-02-22 在文档中未找到（可能已被删除）... |
| 47 | orphaned_registry_entry | `Def-F-02-45` | 注册表条目 Def-F-02-45 在文档中未找到（可能已被删除）... |
| 48 | orphaned_registry_entry | `Def-F-02-46` | 注册表条目 Def-F-02-46 在文档中未找到（可能已被删除）... |
| 49 | orphaned_registry_entry | `Def-F-02-47` | 注册表条目 Def-F-02-47 在文档中未找到（可能已被删除）... |
| 50 | orphaned_registry_entry | `Def-F-02-48` | 注册表条目 Def-F-02-48 在文档中未找到（可能已被删除）... |

... 还有 999 个警告

---

## 🔧 修复建议

### 高优先级

1. **解决重复编号**: 为在不同文件中重复定义的编号分配新的唯一编号
   - 建议：保留原始文档中的定义，将其他文档中的改为引用
   
2. **注册未登记的编号**: 将文档中发现的未注册编号添加到 THEOREM-REGISTRY.md
   - 可以使用 `--patch` 选项生成补丁文件
   
3. **修正阶段标识**: 确保编号中的阶段标识与文件路径匹配

### 中优先级

1. **清理孤儿条目**: 从注册表中移除已不存在的条目
2. **填补编号空缺**: 考虑重新编号以消除空缺（可选）
3. **合并同一文件中的重复定义**: 检查同一文件中多次出现的定义

### 使用脚本生成补丁

```bash
# 生成注册表更新补丁
python .scripts/quality-gates/check-theorem-registry.py --patch patch.md

# 生成完整报告
python .scripts/quality-gates/check-theorem-registry.py --output report.md
```

---

## 附录 A: 所有检测到的定义（按类型分组）

### 定理 (288个)

| 编号 | 阶段 | 文件 | 行号 | 上下文 |
|------|------|------|------|--------|
| Thm-F-01-01 | F | Flink\01-architecture\datastream-v2-semantics.md | 393 | Thm-F-01-01 (DataStream V2 类型安... |
| Thm-F-01-01 | F | Flink\01-architecture\disaggregated-state-analysis.md | 303 | Thm-F-01-01 (分离存储下的 Exactly-On... |
| Thm-F-01-02 | F | Flink\01-architecture\datastream-v2-semantics.md | 406 | Thm-F-01-02 (异步状态访问下的 Exactly-... |
| Thm-F-01-02 | F | Flink\01-architecture\disaggregated-state-analysis.md | 337 | Thm-F-01-02 (异步策略下的最终一致性收敛) |
| Thm-F-02-01 | F | Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md | 526 | Thm-F-02-01 (Checkpoint 恢复后系统状... |
| Thm-F-02-01 | F | Flink\02-core-mechanisms\forst-state-backend.md | 292 | Thm-F-02-01: ForSt Checkpoint ... |
| Thm-F-02-01 | F | Flink\02-core-mechanisms\time-semantics-and-watermark.md | 326 | Thm-F-02-01: Event Time 结果确定性定... |
| Thm-F-02-02 | F | Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md | 569 | Thm-F-02-02 (增量 Checkpoint 完备性... |
| Thm-F-02-02 | F | Flink\02-core-mechanisms\forst-state-backend.md | 335 | Thm-F-02-02: LazyRestore 正确性定理 |
| Thm-F-02-02 | F | Flink\02-core-mechanisms\time-semantics-and-watermark.md | 352 | Thm-F-02-02: Allowed Lateness ... |
| Thm-F-02-03 | F | Flink\02-core-mechanisms\async-execution-model.md | 518 | Thm-F-02-03: 异步执行语义保持性 |
| Thm-F-02-03 | F | Flink\02-core-mechanisms\state-backends-deep-comparison.md | 407 | Thm-F-02-03: 状态后端选择完备性定理 |
| Thm-F-02-04 | F | Flink\02-core-mechanisms\state-backends-deep-comparison.md | 438 | Thm-F-02-04: Checkpoint 效率优化界限... |
| Thm-F-02-45 | F | Flink\02-core-mechanisms\flink-2.0-forst-state-backend.md | 470 | Thm-F-02-45: ForSt Checkpoint ... |
| Thm-F-02-46 | F | Flink\02-core-mechanisms\flink-2.0-forst-state-backend.md | 540 | Thm-F-02-46: 即时恢复正确性定理 |
| Thm-F-02-56 | F | Flink\02-core-mechanisms\adaptive-execution-engine-v2.md | 838 | Thm-F-02-56: 自适应执行正确性定理 |
| Thm-F-02-57 | F | Flink\02-core-mechanisms\adaptive-execution-engine-v2.md | 898 | Thm-F-02-57: 数据倾斜处理有效性定理 |
| Thm-F-02-60 | F | Flink\02-core-mechanisms\smart-checkpointing-strategies.md | 1027 | Thm-F-02-60: 智能检查点最优性定理 |
| Thm-F-02-61 | F | Flink\02-core-mechanisms\smart-checkpointing-strategies.md | 1073 | Thm-F-02-61: 自适应间隔稳定性定理 |
| Thm-F-02-62 | F | Flink\02-core-mechanisms\smart-checkpointing-strategies.md | 1115 | Thm-F-02-62: 增量检查点完备性定理 |
| Thm-F-02-63 | F | Flink\02-core-mechanisms\smart-checkpointing-strategies.md | 1153 | Thm-F-02-63: 局部检查点一致性定理 |
| Thm-F-02-90 | F | Flink\02-core-mechanisms\flink-state-management-complete-guide.md | 490 | Thm-F-02-90: State Backend 选择最... |
| Thm-F-02-91 | F | Flink\02-core-mechanisms\flink-state-management-complete-guide.md | 526 | Thm-F-02-91: Checkpoint 完备性定理 |
| Thm-F-02-92 | F | Flink\02-core-mechanisms\flink-state-management-complete-guide.md | 544 | Thm-F-02-92: State TTL 一致性定理 |
| Thm-F-03-01 | F | Flink\03-sql-table-api\flink-table-sql-complete-guide.md | 277 | Thm-F-03-01: 动态表上连续查询的语义完整性 |
| Thm-F-03-01 | F | Flink\03-sql-table-api\sql-vs-datastream-comparison.md | 198 | Thm-F-03-01 (API 选择性能影响可量化) |
| Thm-F-03-02 | F | Flink\03-sql-table-api\flink-table-sql-complete-guide.md | 294 | Thm-F-03-02: Exactly-Once 语义保证 |
| Thm-F-03-03 | F | Flink\03-sql-table-api\flink-table-sql-complete-guide.md | 312 | Thm-F-03-03: SQL Hints 的优化有效性 |
| Thm-F-03-50 | F | Flink\03-sql-table-api\flink-materialized-table-deep-dive.md | 245 | Thm-F-03-50: 物化表一致性定理 |
| Thm-F-03-51 | F | Flink\03-sql-table-api\flink-materialized-table-deep-dive.md | 271 | Thm-F-03-51: 最优分桶数下界定理 |
| Thm-F-03-52 | F | Flink\03-sql-table-api\flink-materialized-table-deep-dive.md | 296 | Thm-F-03-52: 新鲜度推断完备性 |
| Thm-F-03-70 | F | Flink\03-sql-table-api\flink-sql-hints-optimization.md | 171 | Thm-F-03-70: Broadcast Join可行性... |
| Thm-F-03-71 | F | Flink\03-sql-table-api\flink-sql-hints-optimization.md | 191 | Thm-F-03-71: State TTL与结果正确性 |
| Thm-F-03-72 | F | Flink\03-sql-table-api\flink-sql-hints-optimization.md | 207 | Thm-F-03-72: JSON聚合函数内存上界 |
| Thm-F-04-01 | F | Flink\04-connectors\elasticsearch-connector-complete-guide.md | 202 | Thm-F-04-01: ES Sink 的 At-Leas... |
| Thm-F-04-01 | F | Flink\04-connectors\fluss-integration.md | 210 | Thm-F-04-01: Fluss 在流分析场景的成本效率... |
| Thm-F-04-01 | F | Flink\04-connectors\kafka-integration-patterns.md | 260 | Thm-F-04-01 (Kafka Source Exac... |
| Thm-F-04-02 | F | Flink\04-connectors\elasticsearch-connector-complete-guide.md | 228 | Thm-F-04-02: Exactly-Once 通过幂等... |
| Thm-F-04-02 | F | Flink\04-connectors\kafka-integration-patterns.md | 280 | Thm-F-04-02 (Kafka Sink 事务原子性保... |
| Thm-F-04-03 | F | Flink\04-connectors\mongodb-connector-complete-guide.md | 392 | Thm-F-04-03 (Change Streams So... |
| Thm-F-04-04 | F | Flink\04-connectors\mongodb-connector-complete-guide.md | 432 | Thm-F-04-04 (MongoDB Sink 幂等写入... |
| Thm-F-04-20 | F | Flink\04-connectors\04.04-cdc-debezium-integration.md | 462 | Thm-F-04-20 (CDC Source Exactl... |
| Thm-F-04-20 | F | Flink\04-connectors\cloudevents-integration-guide.md | 633 | Thm-F-04-20 (CloudEvents Schem... |
| Thm-F-04-21 | F | Flink\04-connectors\04.04-cdc-debezium-integration.md | 501 | Thm-F-04-21 (事务边界保证定理) |
| Thm-F-04-21 | F | Flink\04-connectors\cloudevents-integration-guide.md | 670 | Thm-F-04-21 (CloudEvents 跨系统可传... |
| Thm-F-04-30 | F | Flink\04-connectors\flink-delta-lake-integration.md | 388 | Thm-F-04-30 (Flink-Delta Exact... |
| Thm-F-04-31 | F | Flink\04-connectors\flink-delta-lake-integration.md | 435 | Thm-F-04-31 (CDC Merge 一致性定理) |
| Thm-F-04-32 | F | Flink\04-connectors\flink-delta-lake-integration.md | 455 | Thm-F-04-32 (并发写入冲突解决定理) |
| Thm-F-04-33 | F | Flink\04-connectors\flink-delta-lake-integration.md | 474 | Thm-F-04-33 (分区修剪优化有效性) |
| Thm-F-04-40 | F | Flink\04-connectors\flink-cdc-3.0-data-integration.md | 234 | Thm-F-04-40: 全库同步的完备性 |
| Thm-F-04-40 | F | Flink\04-connectors\flink-iceberg-integration.md | 708 | Thm-F-04-40: Flink + Iceberg 端... |
| Thm-F-04-41 | F | Flink\04-connectors\flink-cdc-3.0-data-integration.md | 268 | Thm-F-04-41: Schema Evolution的... |
| Thm-F-04-41 | F | Flink\04-connectors\flink-iceberg-integration.md | 773 | Thm-F-04-41: 隐藏分区优化有效性定理 |
| Thm-F-04-42 | F | Flink\04-connectors\flink-iceberg-integration.md | 815 | Thm-F-04-42: CDC 到 Iceberg 的一致... |
| Thm-F-04-43 | F | Flink\04-connectors\flink-iceberg-integration.md | 863 | Thm-F-04-43: Iceberg vs Delta ... |
| Thm-F-04-50 | F | Flink\04-connectors\flink-paimon-integration.md | 544 | Thm-F-04-50: Paimon Exactly-On... |
| Thm-F-04-51 | F | Flink\04-connectors\flink-paimon-integration.md | 601 | Thm-F-04-51: 增量消费完备性定理 |
| Thm-F-04-52 | F | Flink\04-connectors\flink-paimon-integration.md | 656 | Thm-F-04-52: 流批查询一致性定理 |
| Thm-F-04-53 | F | Flink\04-connectors\flink-paimon-integration.md | 679 | Thm-F-04-53: 实时数仓架构选型论证 |
| Thm-F-05-01 | F | Flink\05-vs-competitors\flink-vs-kafka-streams.md | 420 | Thm-F-05-01 (流处理引擎选择决策定理) |
| Thm-F-05-01 | F | Flink\05-vs-competitors\flink-vs-spark-streaming.md | 241 | Thm-F-05-01 (流处理引擎选择定理) |
| Thm-F-06-01 | F | Flink\06-engineering\performance-tuning-guide.md | 230 | Thm-F-06-01 (最优内存配置定理) |
| Thm-F-06-01 | F | Flink\06-engineering\state-backend-selection.md | 291 | Thm-F-06-01 (状态后端选择的完备性定理) |
| Thm-F-06-02 | F | Flink\06-engineering\performance-tuning-guide.md | 250 | Thm-F-06-02 (并行度扩展效率定理) |
| Thm-F-06-02 | F | Flink\06-engineering\state-backend-selection.md | 317 | Thm-F-06-02 (增量检查点优化界限定理) |
| Thm-F-06-03 | F | Flink\06-engineering\06.02-performance-optimization-complete.md | 366 | Thm-F-06-03 (最优算子链配置定理) |
| Thm-F-06-04 | F | Flink\06-engineering\06.02-performance-optimization-complete.md | 395 | Thm-F-06-04 (SQL查询性能下界定理) |
| Thm-F-06-10 | F | Flink\06-engineering\flink-tco-cost-optimization-guide.md | 560 | Thm-F-06-10 (成本优化 ROI 定理) |
| Thm-F-06-11 | F | Flink\06-engineering\flink-tco-cost-optimization-guide.md | 610 | Thm-F-06-11 (状态后端成本选择定理) |
| Thm-F-06-12 | F | Flink\06-engineering\flink-tco-cost-optimization-guide.md | 643 | Thm-F-06-12 (预留实例成本最优定理) |
| Thm-F-06-20 | F | Flink\06-engineering\flink-dbt-integration.md | 529 | Thm-F-06-20 (dbt-Flink 集成 ROI ... |
| Thm-F-06-21 | F | Flink\06-engineering\flink-dbt-integration.md | 576 | Thm-F-06-21 (流式模型幂等性保证定理) |
| Thm-F-06-40 | F | Flink\06-engineering\stream-processing-cost-optimization.md | 675 | Thm-F-06-40 (成本优化策略决策树完备性) |
| Thm-F-06-41 | F | Flink\06-engineering\stream-processing-cost-optimization.md | 735 | Thm-F-06-41 (预留实例与按需实例平衡定理) |
| Thm-F-06-42 | F | Flink\06-engineering\stream-processing-cost-optimization.md | 784 | Thm-F-06-42 (FinOps成熟度成本节省定理) |
| Thm-F-07-01 | F | Flink\07-case-studies\case-realtime-analytics.md | 613 | Thm-F-07-01 (多层聚合结果一致性) |
| Thm-F-08-40 | F | Flink\08-roadmap\flink-2.3-2.4-roadmap.md | 211 | Thm-F-08-40: Agent可重放性定理 |
| Thm-F-08-41 | F | Flink\08-roadmap\flink-2.3-2.4-roadmap.md | 225 | Thm-F-08-41: SSL前向安全性定理 |
| Thm-F-08-50 | F | Flink\08-roadmap\flink-2.5-preview.md | 356 | Thm-F-08-50: Serverless扩缩容一致性定... |
| Thm-F-08-50 | F | Flink\08-roadmap\flink-30-architecture-redesign.md | 588 | Thm-F-08-50: 统一执行层语义等价性定理 |
| Thm-F-08-50 | F | Flink\08-roadmap\flink-version-evolution-complete-guide.md | 783 | Thm-F-08-50: 版本迁移完备性定理 |
| Thm-F-08-50 | F | Flink\08-roadmap\FLIP-TRACKING-SYSTEM.md | 285 | Thm-F-08-50: FLIP 跟踪系统的完备性 |
| Thm-F-08-51 | F | Flink\08-roadmap\flink-2.5-preview.md | 371 | Thm-F-08-51: 流批一体等价性定理 |
| Thm-F-08-51 | F | Flink\08-roadmap\flink-30-architecture-redesign.md | 616 | Thm-F-08-51: 新状态管理一致性定理 |
| Thm-F-08-51 | F | Flink\08-roadmap\flink-version-evolution-complete-guide.md | 816 | Thm-F-08-51: 版本选择决策完备性定理 |
| Thm-F-08-51 | F | Flink\08-roadmap\FLIP-TRACKING-SYSTEM.md | 306 | Thm-F-08-51: 自动更新机制的准确性 |
| Thm-F-08-52 | F | Flink\08-roadmap\flink-2.5-preview.md | 388 | Thm-F-08-52: GPU加速吞吐量下界定理 |
| Thm-F-08-52 | F | Flink\08-roadmap\flink-30-architecture-redesign.md | 634 | Thm-F-08-52: 云原生弹性保证定理 |
| Thm-F-08-52 | F | Flink\08-roadmap\flink-version-comparison-matrix.md | 260 | Thm-F-08-52: 版本选择完备性定理 |
| Thm-F-08-53 | F | Flink\08-roadmap\flink-25-stream-batch-unification.md | 482 | Thm-F-08-53: 流批一体语义保持定理 |
| Thm-F-08-53 | F | Flink\08-roadmap\flink-30-architecture-redesign.md | 659 | Thm-F-08-53: 向后兼容性保证定理 |
| Thm-F-08-53 | F | Flink\08-roadmap\flink-version-comparison-matrix.md | 281 | Thm-F-08-53: 升级路径可达性定理 |
| Thm-F-08-54 | F | Flink\08-roadmap\flink-25-stream-batch-unification.md | 520 | Thm-F-08-54: 自适应执行最优性定理 |
| Thm-F-08-55 | F | Flink\08-roadmap\flink-25-stream-batch-unification.md | 551 | Thm-F-08-55: 统一容错正确性定理 |
| Thm-F-08-56 | F | Flink\08-roadmap\flink-25-stream-batch-unification.md | 574 | Thm-F-08-56: 批处理性能不下降定理 |
| Thm-F-08-70 | F | Flink\08-roadmap\flink-2.4-tracking.md | 370 | Thm-F-08-70: Serverless Scale-... |
| Thm-F-08-71 | F | Flink\08-roadmap\flink-2.4-tracking.md | 385 | Thm-F-08-71: Adaptive Engine C... |
| Thm-F-08-72 | F | Flink\08-roadmap\flink-2.4-tracking.md | 401 | Thm-F-08-72: AI Agent Multi-Co... |
| Thm-F-09-01 | F | Flink\09-language-foundations\01.02-typeinformation-derivation.md | 352 | Thm-F-09-01: 派生方案等价性定理 |
| Thm-F-09-01 | F | Flink\09-language-foundations\02.02-flink-scala-api-community.md | 234 | Thm-F-09-01: Savepoint 兼容性不可行性 |

... 还有 188 个

### 定义 (1105个)

| 编号 | 阶段 | 文件 | 行号 | 上下文 |
|------|------|------|------|--------|
| Def-F-01-01 | F | Flink\01-architecture\datastream-v2-semantics.md | 45 | Def-F-01-01 (DataStream V2 类型抽... |
| Def-F-01-01 | F | Flink\01-architecture\disaggregated-state-analysis.md | 45 | Def-F-01-01 (分离状态存储) |
| Def-F-01-02 | F | Flink\01-architecture\datastream-v2-semantics.md | 69 | Def-F-01-02 (Source API V2) |
| Def-F-01-02 | F | Flink\01-architecture\disaggregated-state-analysis.md | 69 | Def-F-01-02 (状态后端演进) |
| Def-F-01-03 | F | Flink\01-architecture\datastream-v2-semantics.md | 98 | Def-F-01-03 (ProcessFunction V... |
| Def-F-01-03 | F | Flink\01-architecture\disaggregated-state-analysis.md | 90 | Def-F-01-03 (同步策略) |
| Def-F-01-04 | F | Flink\01-architecture\datastream-v2-semantics.md | 129 | Def-F-01-04 (Async State Acces... |
| Def-F-01-04 | F | Flink\01-architecture\disaggregated-state-analysis.md | 124 | Def-F-01-04 (一致性级别) |
| Def-F-01-05 | F | Flink\01-architecture\datastream-v2-semantics.md | 160 | Def-F-01-05 (Sink V2) |
| Def-F-01-06 | F | Flink\01-architecture\datastream-v2-semantics.md | 187 | Def-F-01-06 (Record Attributes... |
| Def-F-02-01 | F | Flink\02-core-mechanisms\backpressure-and-flow-control.md | 50 | Def-F-02-01 背压 (Backpressure) |
| Def-F-02-01 | F | Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md | 75 | Def-F-02-01 (Checkpoint 核心抽象) |
| Def-F-02-01 | F | Flink\02-core-mechanisms\time-semantics-and-watermark.md | 50 | Def-F-02-01: Event Time (事件时间) |
| Def-F-02-02 | F | Flink\02-core-mechanisms\backpressure-and-flow-control.md | 62 | Def-F-02-02 基于信用的流控 (Credit-ba... |
| Def-F-02-02 | F | Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md | 94 | Def-F-02-02 (Checkpoint Barrie... |
| Def-F-02-02 | F | Flink\02-core-mechanisms\time-semantics-and-watermark.md | 66 | Def-F-02-02: Processing Time (... |
| Def-F-02-03 | F | Flink\02-core-mechanisms\backpressure-and-flow-control.md | 79 | Def-F-02-03 TCP 背压 (Legacy TCP... |
| Def-F-02-03 | F | Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md | 110 | Def-F-02-03 (Aligned Checkpoin... |
| Def-F-02-03 | F | Flink\02-core-mechanisms\time-semantics-and-watermark.md | 82 | Def-F-02-03: Ingestion Time (摄... |
| Def-F-02-04 | F | Flink\02-core-mechanisms\backpressure-and-flow-control.md | 91 | Def-F-02-04 本地背压 vs 端到端背压 |
| Def-F-02-04 | F | Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md | 126 | Def-F-02-04 (Unaligned Checkpo... |
| Def-F-02-04 | F | Flink\02-core-mechanisms\time-semantics-and-watermark.md | 98 | Def-F-02-04: Watermark (水位线) |
| Def-F-02-05 | F | Flink\02-core-mechanisms\async-execution-model.md | 51 | Def-F-02-05: 异步执行控制器 (AEC) |
| Def-F-02-05 | F | Flink\02-core-mechanisms\backpressure-and-flow-control.md | 104 | Def-F-02-05 缓冲区消胀 (Buffer Debl... |
| Def-F-02-05 | F | Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md | 142 | Def-F-02-05 (Incremental Check... |
| Def-F-02-05 | F | Flink\02-core-mechanisms\time-semantics-and-watermark.md | 128 | Def-F-02-05: Allowed Lateness ... |
| Def-F-02-06 | F | Flink\02-core-mechanisms\async-execution-model.md | 96 | Def-F-02-06: 非阻塞状态访问 |
| Def-F-02-06 | F | Flink\02-core-mechanisms\backpressure-and-flow-control.md | 118 | Def-F-02-06 网络缓冲区池 (Network Bu... |
| Def-F-02-06 | F | Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md | 158 | Def-F-02-06 (State Backend) |
| Def-F-02-06 | F | Flink\02-core-mechanisms\time-semantics-and-watermark.md | 146 | Def-F-02-06: Window (窗口) |
| Def-F-02-07 | F | Flink\02-core-mechanisms\async-execution-model.md | 126 | Def-F-02-07: 按键有序性保持 (Per-key ... |
| Def-F-02-07 | F | Flink\02-core-mechanisms\backpressure-and-flow-control.md | 132 | Def-F-02-07 背压监控指标 |
| Def-F-02-07 | F | Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md | 182 | Def-F-02-07 (Checkpoint 协调器) |
| Def-F-02-08 | F | Flink\02-core-mechanisms\async-execution-model.md | 170 | Def-F-02-08: 无序执行与 Watermark 协... |
| Def-F-02-09 | F | Flink\02-core-mechanisms\forst-state-backend.md | 9 | Def-F-02-09: ForSt存储引擎 (ForSt ... |
| Def-F-02-10 | F | Flink\02-core-mechanisms\forst-state-backend.md | 24 | Def-F-02-10: Unified File Syst... |
| Def-F-02-11 | F | Flink\02-core-mechanisms\forst-state-backend.md | 50 | Def-F-02-11: Active State 与 Re... |
| Def-F-02-12 | F | Flink\02-core-mechanisms\forst-state-backend.md | 68 | Def-F-02-12: LazyRestore 机制 |
| Def-F-02-13 | F | Flink\02-core-mechanisms\forst-state-backend.md | 90 | Def-F-02-13: 远程 Compaction |
| Def-F-02-14 | F | Flink\02-core-mechanisms\state-backends-deep-comparison.md | 22 | Def-F-02-14: State Backend（状态后... |
| Def-F-02-15 | F | Flink\02-core-mechanisms\state-backends-deep-comparison.md | 41 | Def-F-02-15: MemoryStateBacken... |
| Def-F-02-16 | F | Flink\02-core-mechanisms\state-backends-deep-comparison.md | 66 | Def-F-02-16: FsStateBackend（文件... |
| Def-F-02-17 | F | Flink\02-core-mechanisms\state-backends-deep-comparison.md | 78 | Def-F-02-17: HashMapStateBacke... |
| Def-F-02-18 | F | Flink\02-core-mechanisms\state-backends-deep-comparison.md | 94 | Def-F-02-18: RocksDBStateBacke... |
| Def-F-02-19 | F | Flink\02-core-mechanisms\state-backends-deep-comparison.md | 123 | Def-F-02-19: ForStStateBackend... |
| Def-F-02-20 | F | Flink\02-core-mechanisms\state-backends-deep-comparison.md | 152 | Def-F-02-20: 增量 Checkpoint（Inc... |
| Def-F-02-23 | F | Flink\02-core-mechanisms\flink-2.2-frontier-features.md | 7 | Def-F-02-23: Delta Join V2 - 增... |
| Def-F-02-24 | F | Flink\02-core-mechanisms\flink-2.2-frontier-features.md | 31 | Def-F-02-24: Delta Join 缓存层级架构 |
| Def-F-02-25 | F | Flink\02-core-mechanisms\flink-2.2-frontier-features.md | 49 | Def-F-02-25: VECTOR_SEARCH 向量搜... |
| Def-F-02-26 | F | Flink\02-core-mechanisms\flink-2.2-frontier-features.md | 76 | Def-F-02-26: Materialized Tabl... |
| Def-F-02-27 | F | Flink\02-core-mechanisms\flink-2.2-frontier-features.md | 101 | Def-F-02-27: MaterializedTable... |
| Def-F-02-28 | F | Flink\02-core-mechanisms\flink-2.2-frontier-features.md | 128 | Def-F-02-28: DISTRIBUTED BY/IN... |
| Def-F-02-29 | F | Flink\02-core-mechanisms\flink-2.2-frontier-features.md | 146 | Def-F-02-29: SinkUpsertMateria... |
| Def-F-02-30 | F | Flink\02-core-mechanisms\flink-2.2-frontier-features.md | 166 | Def-F-02-30: Python Async Data... |
| Def-F-02-31 | F | Flink\02-core-mechanisms\flink-2.2-frontier-features.md | 188 | Def-F-02-31: Source RateLimite... |
| Def-F-02-32 | F | Flink\02-core-mechanisms\flink-2.2-frontier-features.md | 206 | Def-F-02-32: Balanced Tasks Sc... |
| Def-F-02-33 | F | Flink\02-core-mechanisms\flink-2.2-frontier-features.md | 231 | Def-F-02-33: Event Reporting 系... |
| Def-F-02-34 | F | Flink\02-core-mechanisms\flink-2.2-frontier-features.md | 258 | Def-F-02-34: Protobuf 4.x 序列化升... |
| Def-F-02-40 | F | Flink\02-core-mechanisms\delta-join-production-guide.md | 7 | Def-F-02-40: Delta Join V2 生产就... |
| Def-F-02-41 | F | Flink\02-core-mechanisms\delta-join-production-guide.md | 34 | Def-F-02-41: CDC 源无DELETE约束 |
| Def-F-02-42 | F | Flink\02-core-mechanisms\delta-join-production-guide.md | 62 | Def-F-02-42: 投影/过滤下推语义 |
| Def-F-02-43 | F | Flink\02-core-mechanisms\delta-join-production-guide.md | 88 | Def-F-02-43: 多级缓存架构（生产级） |
| Def-F-02-44 | F | Flink\02-core-mechanisms\delta-join-production-guide.md | 114 | Def-F-02-44: Delta Join 与 Regu... |
| Def-F-02-61 | F | Flink\02-core-mechanisms\flink-2.0-forst-state-backend.md | 9 | Def-F-02-61: ForSt 存储引擎 (ForSt... |
| Def-F-02-62 | F | Flink\02-core-mechanisms\flink-2.0-forst-state-backend.md | 34 | Def-F-02-62: 统一文件系统层 (UFS - Un... |
| Def-F-02-63 | F | Flink\02-core-mechanisms\flink-2.0-forst-state-backend.md | 65 | Def-F-02-63: 分离式存储架构 (Disaggre... |
| Def-F-02-64 | F | Flink\02-core-mechanisms\flink-2.0-forst-state-backend.md | 103 | Def-F-02-64: 即时恢复机制 (Instant R... |
| Def-F-02-65 | F | Flink\02-core-mechanisms\flink-2.0-forst-state-backend.md | 142 | Def-F-02-65: 远程 Compaction 服务 ... |
| Def-F-02-80 | F | Flink\02-core-mechanisms\flink-2.0-async-execution-model.md | 166 | 定义 Def-F-02-80**: **异步状态原语 (As... |
| Def-F-02-80 | F | Flink\02-core-mechanisms\flink-state-ttl-best-practices.md | 9 | Def-F-02-80: State TTL (Time-T... |
| Def-F-02-81 | F | Flink\02-core-mechanisms\flink-2.0-async-execution-model.md | 188 | 定义 Def-F-02-81**: **StateFutur... |
| Def-F-02-81 | F | Flink\02-core-mechanisms\flink-state-ttl-best-practices.md | 17 | Def-F-02-81: TTL 更新类型 (Update ... |
| Def-F-02-82 | F | Flink\02-core-mechanisms\flink-state-ttl-best-practices.md | 27 | Def-F-02-82: 状态可见性 (State Visi... |
| Def-F-02-83 | F | Flink\02-core-mechanisms\flink-state-ttl-best-practices.md | 33 | Def-F-02-83: 清理策略 (Cleanup Str... |
| Def-F-02-87 | F | Flink\02-core-mechanisms\adaptive-execution-engine-v2.md | 58 | Def-F-02-87: 自适应执行引擎 (Adaptive... |
| Def-F-02-88 | F | Flink\02-core-mechanisms\adaptive-execution-engine-v2.md | 121 | Def-F-02-88: 智能执行计划优化器 (Intell... |
| Def-F-02-89 | F | Flink\02-core-mechanisms\adaptive-execution-engine-v2.md | 147 | Def-F-02-89: 运行时自适应调整器 (Runtim... |
| Def-F-02-90 | F | Flink\02-core-mechanisms\adaptive-execution-engine-v2.md | 208 | Def-F-02-90: 数据倾斜检测器 (Skew Det... |
| Def-F-02-90 | F | Flink\02-core-mechanisms\flink-state-management-complete-guide.md | 23 | Def-F-02-90: State Backend（状态后... |
| Def-F-02-91 | F | Flink\02-core-mechanisms\adaptive-execution-engine-v2.md | 257 | Def-F-02-91: 资源自适应分配器 (Resourc... |
| Def-F-02-91 | F | Flink\02-core-mechanisms\flink-state-management-complete-guide.md | 48 | Def-F-02-91: HashMapStateBacke... |
| Def-F-02-92 | F | Flink\02-core-mechanisms\adaptive-execution-engine-v2.md | 282 | Def-F-02-92: Adaptive Schedule... |
| Def-F-02-92 | F | Flink\02-core-mechanisms\flink-state-management-complete-guide.md | 71 | Def-F-02-92: EmbeddedRocksDBSt... |
| Def-F-02-93 | F | Flink\02-core-mechanisms\flink-state-management-complete-guide.md | 96 | Def-F-02-93: ForStStateBackend... |
| Def-F-02-94 | F | Flink\02-core-mechanisms\flink-state-management-complete-guide.md | 113 | Def-F-02-94: Keyed State（键控状态） |
| Def-F-02-95 | F | Flink\02-core-mechanisms\flink-state-management-complete-guide.md | 133 | Def-F-02-95: Operator State（算子... |
| Def-F-02-96 | F | Flink\02-core-mechanisms\flink-state-management-complete-guide.md | 151 | Def-F-02-96: Checkpoint（检查点） |
| Def-F-02-97 | F | Flink\02-core-mechanisms\flink-state-management-complete-guide.md | 170 | Def-F-02-97: State TTL（状态生存时间） |
| Def-F-03-01 | F | Flink\03-sql-table-api\built-in-functions-complete-list.md | 9 | Def-F-03-01: 内置函数体系 (Built-in ... |
| Def-F-03-01 | F | Flink\03-sql-table-api\data-types-complete-reference.md | 7 | Def-F-03-01: 数据类型 (Data Type) |
| Def-F-03-01 | F | Flink\03-sql-table-api\flink-table-sql-complete-guide.md | 11 | Def-F-03-01: Flink SQL 语义模型 |
| Def-F-03-01 | F | Flink\03-sql-table-api\sql-functions-cheatsheet.md | 9 | Def-F-03-01: SQL内置函数分类 |
| Def-F-03-01 | F | Flink\03-sql-table-api\sql-vs-datastream-comparison.md | 43 | Def-F-03-01 (SQL API 抽象) |
| Def-F-03-02 | F | Flink\03-sql-table-api\built-in-functions-complete-list.md | 21 | Def-F-03-02: 函数分类层级 |
| Def-F-03-02 | F | Flink\03-sql-table-api\data-types-complete-reference.md | 22 | Def-F-03-02: 逻辑类型 vs 物理类型 |
| Def-F-03-02 | F | Flink\03-sql-table-api\flink-table-sql-complete-guide.md | 27 | Def-F-03-02: 动态表 (Dynamic Tabl... |
| Def-F-03-02 | F | Flink\03-sql-table-api\sql-functions-cheatsheet.md | 24 | Def-F-03-02: 版本兼容性标记 |
| Def-F-03-02 | F | Flink\03-sql-table-api\sql-vs-datastream-comparison.md | 62 | Def-F-03-02 (DataStream API 抽象... |
| Def-F-03-03 | F | Flink\03-sql-table-api\data-types-complete-reference.md | 40 | Def-F-03-03: 类型系统层次结构 |
| Def-F-03-03 | F | Flink\03-sql-table-api\flink-table-sql-complete-guide.md | 47 | Def-F-03-03: 时间属性 (Time Attrib... |

... 还有 1005 个

### 引理 (344个)

| 编号 | 阶段 | 文件 | 行号 | 上下文 |
|------|------|------|------|--------|
| Lemma-F-01-01 | F | Flink\01-architecture\datastream-v2-semantics.md | 217 | Lemma-F-01-01 (V2 状态访问类型安全性) |
| Lemma-F-01-01 | F | Flink\01-architecture\disaggregated-state-analysis.md | 150 | Lemma-F-01-01 (分离存储的位置无关性) |
| Lemma-F-01-02 | F | Flink\01-architecture\datastream-v2-semantics.md | 230 | Lemma-F-01-02 (异步状态访问单调性) |
| Lemma-F-01-02 | F | Flink\01-architecture\disaggregated-state-analysis.md | 175 | Lemma-F-01-02 (异步同步的单调版本性) |
| Lemma-F-02-01 | F | Flink\02-core-mechanisms\async-execution-model.md | 216 | Lemma-F-02-01: AEC 状态机完备性 |
| Lemma-F-02-01 | F | Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md | 205 | Lemma-F-02-01 (Barrier 对齐保证状态一... |
| Lemma-F-02-01 | F | Flink\02-core-mechanisms\time-semantics-and-watermark.md | 173 | Lemma-F-02-01: Watermark 单调性 |
| Lemma-F-02-02 | F | Flink\02-core-mechanisms\async-execution-model.md | 252 | Lemma-F-02-02: 异步状态访问的单调读 |
| Lemma-F-02-02 | F | Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md | 221 | Lemma-F-02-02 (异步 Checkpoint 的... |
| Lemma-F-02-02 | F | Flink\02-core-mechanisms\time-semantics-and-watermark.md | 193 | Lemma-F-02-02: 窗口分配完备性 |
| Lemma-F-02-03 | F | Flink\02-core-mechanisms\async-execution-model.md | 594 | Lemma-F-02-03: 按键 FIFO 保持性证明 |
| Lemma-F-02-03 | F | Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md | 236 | Lemma-F-02-03 (增量 Checkpoint 的... |
| Lemma-F-02-03 | F | Flink\02-core-mechanisms\time-semantics-and-watermark.md | 207 | Lemma-F-02-03: 延迟上界定理 |
| Lemma-F-02-04 | F | Flink\02-core-mechanisms\adaptive-execution-engine-v2.md | 329 | Lemma-F-02-04: 自适应收敛性 |
| Lemma-F-02-05 | F | Flink\02-core-mechanisms\adaptive-execution-engine-v2.md | 367 | Lemma-F-02-05: 倾斜检测完备性 |
| Lemma-F-02-05 | F | Flink\02-core-mechanisms\forst-state-backend.md | 145 | Lemma-F-02-05: 状态一致性保证 |
| Lemma-F-02-06 | F | Flink\02-core-mechanisms\state-backends-deep-comparison.md | 180 | Lemma-F-02-06: 状态后端访问延迟排序 |
| Lemma-F-02-07 | F | Flink\02-core-mechanisms\state-backends-deep-comparison.md | 202 | Lemma-F-02-07: 状态容量扩展性 |
| Lemma-F-02-23 | F | Flink\02-core-mechanisms\flink-2.0-forst-state-backend.md | 245 | Lemma-F-02-23: 成本优化下界 |
| Lemma-F-02-50 | F | Flink\02-core-mechanisms\smart-checkpointing-strategies.md | 409 | Lemma-F-02-50: 自适应间隔收敛性 |
| Lemma-F-02-51 | F | Flink\02-core-mechanisms\smart-checkpointing-strategies.md | 428 | Lemma-F-02-51: 增量检查点存储上界 |
| Lemma-F-02-52 | F | Flink\02-core-mechanisms\smart-checkpointing-strategies.md | 451 | Lemma-F-02-52: 局部检查点一致性保证 |
| Lemma-F-02-60 | F | Flink\02-core-mechanisms\flink-state-ttl-best-practices.md | 47 | Lemma-F-02-60: TTL 过期状态的单调性 |
| Lemma-F-02-61 | F | Flink\02-core-mechanisms\flink-state-ttl-best-practices.md | 55 | Lemma-F-02-61: 清理策略的及时性排序 |
| Lemma-F-02-62 | F | Flink\02-core-mechanisms\flink-state-ttl-best-practices.md | 71 | Lemma-F-02-62: 状态可见性与一致性边界 |
| Lemma-F-02-70 | F | Flink\02-core-mechanisms\flink-state-management-complete-guide.md | 189 | Lemma-F-02-70: State Backend 延... |
| Lemma-F-02-71 | F | Flink\02-core-mechanisms\flink-state-management-complete-guide.md | 209 | Lemma-F-02-71: State Backend 容... |
| Lemma-F-03-01 | F | Flink\03-sql-table-api\data-types-complete-reference.md | 65 | Lemma-F-03-01: 类型完备性 |
| Lemma-F-03-01 | F | Flink\03-sql-table-api\flink-table-sql-complete-guide.md | 138 | Lemma-F-03-01: 时间属性传递性 |
| Lemma-F-03-01 | F | Flink\03-sql-table-api\sql-vs-datastream-comparison.md | 92 | Lemma-F-03-01 (SQL 优化的全局性) |
| Lemma-F-03-02 | F | Flink\03-sql-table-api\data-types-complete-reference.md | 76 | Lemma-F-03-02: 类型可比较性 |
| Lemma-F-03-02 | F | Flink\03-sql-table-api\flink-table-sql-complete-guide.md | 157 | Lemma-F-03-02: JOIN 状态需求 |
| Lemma-F-03-02 | F | Flink\03-sql-table-api\sql-vs-datastream-comparison.md | 105 | Lemma-F-03-02 (DataStream 状态控制... |
| Lemma-F-03-03 | F | Flink\03-sql-table-api\data-types-complete-reference.md | 279 | Lemma-F-03-03: 嵌套类型限制 |
| Lemma-F-03-04 | F | Flink\03-sql-table-api\vector-search.md | 122 | Lemma-F-03-04: 嵌入模型的 Lipschitz... |
| Lemma-F-03-10 | F | Flink\03-sql-table-api\flink-vector-search-rag.md | 240 | Lemma-F-03-10: 嵌入向量的 Lipschitz... |
| Lemma-F-03-30 | F | Flink\03-sql-table-api\flink-materialized-table-deep-dive.md | 70 | Lemma-F-03-30: 物化表的幂等性 |
| Lemma-F-03-70 | F | Flink\03-sql-table-api\flink-sql-hints-optimization.md | 72 | Lemma-F-03-70: Join Hint优先级 |
| Lemma-F-03-71 | F | Flink\03-sql-table-api\flink-sql-hints-optimization.md | 78 | Lemma-F-03-71: State TTL与Check... |
| Lemma-F-03-72 | F | Flink\03-sql-table-api\flink-sql-hints-optimization.md | 86 | Lemma-F-03-72: JSON函数性能特征 |
| Lemma-F-04-01 | F | Flink\04-connectors\elasticsearch-connector-complete-guide.md | 91 | Lemma-F-04-01: 批量大小与延迟权衡 |
| Lemma-F-04-01 | F | Flink\04-connectors\kafka-integration-patterns.md | 127 | Lemma-F-04-01 (Kafka Source 偏移... |
| Lemma-F-04-02 | F | Flink\04-connectors\kafka-integration-patterns.md | 144 | Lemma-F-04-02 (事务性 Sink 的原子性边界... |
| Lemma-F-04-03 | F | Flink\04-connectors\mongodb-connector-complete-guide.md | 168 | Lemma-F-04-03 (Change Streams ... |
| Lemma-F-04-04 | F | Flink\04-connectors\mongodb-connector-complete-guide.md | 186 | Lemma-F-04-04 (批量写入原子性边界) |
| Lemma-F-04-20 | F | Flink\04-connectors\04.04-cdc-debezium-integration.md | 207 | Lemma-F-04-20 (CDC延迟边界) |
| Lemma-F-04-20 | F | Flink\04-connectors\cloudevents-integration-guide.md | 186 | Lemma-F-04-20 (CloudEvents 与 F... |
| Lemma-F-04-21 | F | Flink\04-connectors\04.04-cdc-debezium-integration.md | 233 | Lemma-F-04-21 (初始快照一致性) |
| Lemma-F-04-21 | F | Flink\04-connectors\cloudevents-integration-guide.md | 219 | Lemma-F-04-21 (CloudEvents 传输协... |
| Lemma-F-04-40 | F | Flink\04-connectors\flink-cdc-3.0-data-integration.md | 68 | Lemma-F-04-40: CDC一致性保证 |
| Lemma-F-04-40 | F | Flink\04-connectors\flink-delta-lake-integration.md | 250 | Lemma-F-04-40 (Delta 写入原子性) |
| Lemma-F-04-41 | F | Flink\04-connectors\flink-cdc-3.0-data-integration.md | 78 | Lemma-F-04-41: 延迟边界 |
| Lemma-F-04-41 | F | Flink\04-connectors\flink-delta-lake-integration.md | 260 | Lemma-F-04-41 (并发写入隔离性) |
| Lemma-F-04-42 | F | Flink\04-connectors\flink-delta-lake-integration.md | 266 | Lemma-F-04-42 (Z-Ordering 查询优化... |
| Lemma-F-04-50 | F | Flink\04-connectors\flink-iceberg-integration.md | 310 | Lemma-F-04-50: Iceberg 快照的不可变性... |
| Lemma-F-04-50 | F | Flink\04-connectors\flink-paimon-integration.md | 243 | Lemma-F-04-50: LSM 写入放大与读优化权衡 |
| Lemma-F-04-51 | F | Flink\04-connectors\flink-iceberg-integration.md | 346 | Lemma-F-04-51: 隐藏分区的查询透明性 |
| Lemma-F-04-51 | F | Flink\04-connectors\flink-paimon-integration.md | 269 | Lemma-F-04-51: 增量日志的完备性保证 |
| Lemma-F-04-52 | F | Flink\04-connectors\flink-iceberg-integration.md | 367 | Lemma-F-04-52: 增量消费完备性 |
| Lemma-F-05-01 | F | Flink\05-vs-competitors\flink-vs-kafka-streams.md | 149 | Lemma-F-05-01 (嵌入式架构的状态访问延迟上界) |
| Lemma-F-05-01 | F | Flink\05-vs-competitors\flink-vs-spark-streaming.md | 91 | Lemma-F-05-01 (微批模型延迟下界) |
| Lemma-F-05-01 | F | Flink\05-vs-competitors\linkedin-samza-deep-dive.md | 127 | Lemma-F-05-01: 状态持久化延迟特性 |
| Lemma-F-05-02 | F | Flink\05-vs-competitors\flink-vs-kafka-streams.md | 166 | Lemma-F-05-02 (集群架构的水平扩展能力) |
| Lemma-F-05-02 | F | Flink\05-vs-competitors\flink-vs-spark-streaming.md | 112 | Lemma-F-05-02 (原生流处理延迟上界) |
| Lemma-F-05-02 | F | Flink\05-vs-competitors\linkedin-samza-deep-dive.md | 141 | Lemma-F-05-02: 故障恢复时间下界 |
| Lemma-F-06-01 | F | Flink\06-engineering\performance-tuning-guide.md | 104 | Lemma-F-06-01 (内存配置的约束传播) |
| Lemma-F-06-01 | F | Flink\06-engineering\state-backend-selection.md | 142 | Lemma-F-06-01 (状态后端与一致性语义的独立性) |
| Lemma-F-06-02 | F | Flink\06-engineering\performance-tuning-guide.md | 118 | Lemma-F-06-02 (并行度与吞吐量的亚线性关系) |
| Lemma-F-06-02 | F | Flink\06-engineering\state-backend-selection.md | 150 | Lemma-F-06-02 (RocksDB 的内存-磁盘分... |
| Lemma-F-06-03 | F | Flink\06-engineering\performance-tuning-guide.md | 128 | Lemma-F-06-03 (检查点间隔与恢复时间的权衡) |
| Lemma-F-06-03 | F | Flink\06-engineering\state-backend-selection.md | 164 | Lemma-F-06-03 (增量检查点的状态边界约束) |
| Lemma-F-06-04 | F | Flink\06-engineering\performance-tuning-guide.md | 138 | Lemma-F-06-04 (序列化开销的比例边界) |
| Lemma-F-06-05 | F | Flink\06-engineering\06.02-performance-optimization-complete.md | 163 | Lemma-F-06-05 (算子链合并的收益边界) |
| Lemma-F-06-06 | F | Flink\06-engineering\06.02-performance-optimization-complete.md | 182 | Lemma-F-06-06 (SQL谓词下推的有效性条件) |
| Lemma-F-06-07 | F | Flink\06-engineering\06.02-performance-optimization-complete.md | 199 | Lemma-F-06-07 (异步I/O的并行度最优性) |
| Lemma-F-06-08 | F | Flink\06-engineering\06.02-performance-optimization-complete.md | 209 | Lemma-F-06-08 (批处理大小的吞吐-延迟权衡) |
| Lemma-F-06-10 | F | Flink\06-engineering\flink-tco-cost-optimization-guide.md | 180 | Lemma-F-06-10 (规模经济效应) |
| Lemma-F-06-11 | F | Flink\06-engineering\flink-tco-cost-optimization-guide.md | 218 | Lemma-F-06-11 (存算分离的成本边界) |
| Lemma-F-06-20 | F | Flink\06-engineering\flink-dbt-integration.md | 189 | Lemma-F-06-20 (物化策略的延迟边界) |
| Lemma-F-06-21 | F | Flink\06-engineering\flink-dbt-integration.md | 218 | Lemma-F-06-21 (流式模型幂等性条件) |
| Lemma-F-06-40 | F | Flink\06-engineering\stream-processing-cost-optimization.md | 248 | Lemma-F-06-40 (成本边界效应) |
| Lemma-F-06-41 | F | Flink\06-engineering\stream-processing-cost-optimization.md | 288 | Lemma-F-06-41 (Spot实例成本稳定性) |
| Lemma-F-07-01 | F | Flink\07-case-studies\case-realtime-analytics.md | 369 | Lemma-F-07-01 (分层聚合的单调性保证) |
| Lemma-F-07-02 | F | Flink\07-case-studies\case-realtime-analytics.md | 386 | Lemma-F-07-02 (侧输出流的负载隔离性) |
| Lemma-F-08-40 | F | Flink\08-roadmap\flink-2.3-2.4-roadmap.md | 123 | Lemma-F-08-40: Kafka 2PC延迟改进 |
| Lemma-F-08-41 | F | Flink\08-roadmap\community-dynamics-tracking.md | 145 | Lemma-F-08-41: 贡献者留存率 |
| Lemma-F-08-50 | F | Flink\08-roadmap\flink-2.5-preview.md | 176 | Lemma-F-08-50: GPU算子加速比 |
| Lemma-F-08-50 | F | Flink\08-roadmap\flink-30-architecture-redesign.md | 352 | Lemma-F-08-50: API兼容性保持 |
| Lemma-F-08-50 | F | Flink\08-roadmap\flink-version-evolution-complete-guide.md | 521 | Lemma-F-08-50: 向后兼容性引理 |
| Lemma-F-08-50 | F | Flink\08-roadmap\FLIP-TRACKING-SYSTEM.md | 129 | Lemma-F-08-50: FLIP 状态单调性 |
| Lemma-F-08-51 | F | Flink\08-roadmap\flink-2.5-preview.md | 186 | Lemma-F-08-51: WebAssembly UDF... |
| Lemma-F-08-51 | F | Flink\08-roadmap\flink-30-architecture-redesign.md | 362 | Lemma-F-08-51: 迁移路径完备性 |
| Lemma-F-08-51 | F | Flink\08-roadmap\flink-version-evolution-complete-guide.md | 560 | Lemma-F-08-51: 迁移复杂度边界引理 |
| Lemma-F-08-51 | F | Flink\08-roadmap\FLIP-TRACKING-SYSTEM.md | 143 | Lemma-F-08-51: 发布版本预测 |
| Lemma-F-08-52 | F | Flink\08-roadmap\flink-25-stream-batch-unification.md | 291 | Lemma-F-08-52: 混合执行数据一致性 |
| Lemma-F-08-52 | F | Flink\08-roadmap\flink-version-comparison-matrix.md | 102 | Lemma-F-08-52: 向后兼容性单调性 |
| Lemma-F-08-53 | F | Flink\08-roadmap\flink-25-stream-batch-unification.md | 308 | Lemma-F-08-53: 统一存储层访问性能 |
| Lemma-F-08-53 | F | Flink\08-roadmap\flink-version-comparison-matrix.md | 120 | Lemma-F-08-53: 升级路径传递性 |
| Lemma-F-08-70 | F | Flink\08-roadmap\flink-2.4-tracking.md | 236 | Lemma-F-08-70: Checkpoint Opti... |
| Lemma-F-08-71 | F | Flink\08-roadmap\flink-2.4-tracking.md | 250 | Lemma-F-08-71: AI Agent GA Sta... |

... 还有 244 个

### 命题 (431个)

| 编号 | 阶段 | 文件 | 行号 | 上下文 |
|------|------|------|------|--------|
| Prop-F-01-01 | F | Flink\01-architecture\datastream-v2-semantics.md | 245 | Prop-F-01-01 (声明式状态幂等初始化) |
| Prop-F-01-01 | F | Flink\01-architecture\disaggregated-state-analysis.md | 199 | Prop-F-01-01 (延迟与吞吐量的权衡关系) |
| Prop-F-02-01 | F | Flink\02-core-mechanisms\async-execution-model.md | 272 | Prop-F-02-01: 吞吐量-延迟权衡关系 |
| Prop-F-02-01 | F | Flink\02-core-mechanisms\backpressure-and-flow-control.md | 150 | Prop-F-02-01 CBFC 保证无死锁 |
| Prop-F-02-01 | F | Flink\02-core-mechanisms\checkpoint-mechanism-deep-dive.md | 256 | Prop-F-02-01 (Checkpoint 类型选择的... |
| Prop-F-02-02 | F | Flink\02-core-mechanisms\adaptive-execution-engine-v2.md | 397 | Prop-F-02-02: 资源分配最优性 |
| Prop-F-02-02 | F | Flink\02-core-mechanisms\backpressure-and-flow-control.md | 156 | Prop-F-02-02 背压传播保证上游速率自适应 |
| Prop-F-02-03 | F | Flink\02-core-mechanisms\adaptive-execution-engine-v2.md | 415 | Prop-F-02-03: 性能提升下界 |
| Prop-F-02-03 | F | Flink\02-core-mechanisms\backpressure-and-flow-control.md | 164 | Prop-F-02-03 缓冲区隔离保证局部故障不扩散 |
| Prop-F-02-03 | F | Flink\02-core-mechanisms\forst-state-backend.md | 112 | Prop-F-02-03: Checkpoint 时间复杂度... |
| Prop-F-02-04 | F | Flink\02-core-mechanisms\backpressure-and-flow-control.md | 172 | Prop-F-02-04 Buffer Debloating... |
| Prop-F-02-04 | F | Flink\02-core-mechanisms\forst-state-backend.md | 132 | Prop-F-02-04: 故障恢复时间界限 |
| Prop-F-02-05 | F | Flink\02-core-mechanisms\backpressure-and-flow-control.md | 180 | Prop-F-02-05 Credit 系统保证接收方缓冲区... |
| Prop-F-02-05 | F | Flink\02-core-mechanisms\state-backends-deep-comparison.md | 222 | Prop-F-02-05: Checkpoint 时间复杂度... |
| Prop-F-02-06 | F | Flink\02-core-mechanisms\state-backends-deep-comparison.md | 237 | Prop-F-02-06: 故障恢复时间界限 |
| Prop-F-02-07 | F | Flink\02-core-mechanisms\flink-2.2-frontier-features.md | 276 | Prop-F-02-07: Delta Join V2 缓存... |
| Prop-F-02-08 | F | Flink\02-core-mechanisms\flink-2.2-frontier-features.md | 286 | Prop-F-02-08: VECTOR_SEARCH 与 ... |
| Prop-F-02-09 | F | Flink\02-core-mechanisms\flink-2.2-frontier-features.md | 303 | Prop-F-02-09: Materialized Tab... |
| Prop-F-02-10 | F | Flink\02-core-mechanisms\flink-2.2-frontier-features.md | 315 | Prop-F-02-10: SinkUpsertMateri... |
| Prop-F-02-11 | F | Flink\02-core-mechanisms\flink-2.2-frontier-features.md | 327 | Prop-F-02-11: Python Async API... |
| Prop-F-02-12 | F | Flink\02-core-mechanisms\flink-2.2-frontier-features.md | 341 | Prop-F-02-12: Balanced Schedul... |
| Prop-F-02-19 | F | Flink\02-core-mechanisms\delta-join-production-guide.md | 143 | Prop-F-02-19: Delta Join V2 缓存... |
| Prop-F-02-20 | F | Flink\02-core-mechanisms\delta-join-production-guide.md | 168 | Prop-F-02-20: 投影下推 IO 减少量 |
| Prop-F-02-21 | F | Flink\02-core-mechanisms\delta-join-production-guide.md | 186 | Prop-F-02-21: Delta Join 端到端延迟... |
| Prop-F-02-21 | F | Flink\02-core-mechanisms\flink-2.0-forst-state-backend.md | 183 | Prop-F-02-21: Checkpoint 时间复杂度... |
| Prop-F-02-22 | F | Flink\02-core-mechanisms\delta-join-production-guide.md | 205 | Prop-F-02-22: CDC 源无 DELETE 约束... |
| Prop-F-02-22 | F | Flink\02-core-mechanisms\flink-2.0-forst-state-backend.md | 217 | Prop-F-02-22: 恢复速度提升界限 |
| Prop-F-02-24 | F | Flink\02-core-mechanisms\flink-2.0-forst-state-backend.md | 282 | Prop-F-02-24: 无缝重配置保证 |
| Prop-F-02-50 | F | Flink\02-core-mechanisms\smart-checkpointing-strategies.md | 467 | Prop-F-02-50: 检查点频率与恢复时间权衡 |
| Prop-F-02-51 | F | Flink\02-core-mechanisms\smart-checkpointing-strategies.md | 493 | Prop-F-02-51: 并行度与吞吐量的最优关系 |
| Prop-F-02-60 | F | Flink\02-core-mechanisms\flink-state-ttl-best-practices.md | 79 | Prop-F-02-60: TTL 对 Checkpoint... |
| Prop-F-02-70 | F | Flink\02-core-mechanisms\flink-state-management-complete-guide.md | 227 | Prop-F-02-70: State 类型选择定理 |
| Prop-F-02-71 | F | Flink\02-core-mechanisms\flink-state-management-complete-guide.md | 243 | Prop-F-02-71: Checkpoint 一致性保证 |
| Prop-F-03-01 | F | Flink\03-sql-table-api\built-in-functions-complete-list.md | 41 | Prop-F-03-01: 函数确定性 (Determini... |
| Prop-F-03-01 | F | Flink\03-sql-table-api\data-types-complete-reference.md | 83 | Prop-F-03-01: 嵌套类型深度限制 |
| Prop-F-03-01 | F | Flink\03-sql-table-api\flink-table-sql-complete-guide.md | 148 | Prop-F-03-01: 窗口聚合的单调性 |
| Prop-F-03-01 | F | Flink\03-sql-table-api\materialized-tables.md | 145 | Prop-F-03-01: 物化表与视图的语义差异 |
| Prop-F-03-01 | F | Flink\03-sql-table-api\sql-vs-datastream-comparison.md | 117 | Prop-F-03-01 (表达力-优化权衡) |
| Prop-F-03-02 | F | Flink\03-sql-table-api\built-in-functions-complete-list.md | 51 | Prop-F-03-02: 空值传播 (Null Propa... |
| Prop-F-03-02 | F | Flink\03-sql-table-api\data-types-complete-reference.md | 471 | Prop-F-03-02: 转换安全级别 |
| Prop-F-03-02 | F | Flink\03-sql-table-api\flink-table-sql-complete-guide.md | 171 | Prop-F-03-02: 物化视图与连续查询等价性 |
| Prop-F-03-02 | F | Flink\03-sql-table-api\materialized-tables.md | 157 | Prop-F-03-02: 增量刷新的可推导性 |
| Prop-F-03-03 | F | Flink\03-sql-table-api\built-in-functions-complete-list.md | 59 | Prop-F-03-03: 类型推导规则 |
| Prop-F-03-03 | F | Flink\03-sql-table-api\flink-sql-window-functions-deep-dive.md | 165 | Prop-F-03-03: TUMBLE窗口状态边界 |
| Prop-F-03-03 | F | Flink\03-sql-table-api\materialized-tables.md | 167 | Prop-F-03-03: 调度延迟下界 |
| Prop-F-03-04 | F | Flink\03-sql-table-api\flink-sql-window-functions-deep-dive.md | 176 | Prop-F-03-04: HOP窗口状态膨胀 |
| Prop-F-03-04 | F | Flink\03-sql-table-api\materialized-tables.md | 175 | Prop-F-03-04: FRESHNESS 自动推断的完... |
| Prop-F-03-04 | F | Flink\03-sql-table-api\model-ddl-and-ml-predict.md | 180 | Prop-F-03-04: ML_PREDICT 的惰性求值... |
| Prop-F-03-05 | F | Flink\03-sql-table-api\flink-sql-window-functions-deep-dive.md | 192 | Prop-F-03-05: SESSION窗口状态不确定性 |
| Prop-F-03-05 | F | Flink\03-sql-table-api\materialized-tables.md | 185 | Prop-F-03-05: 分布式分区的查询加速比 |
| Prop-F-03-05 | F | Flink\03-sql-table-api\model-ddl-and-ml-predict.md | 195 | Prop-F-03-05: 批量推理的聚合边界 |
| Prop-F-03-05 | F | Flink\03-sql-table-api\vector-search.md | 100 | Prop-F-03-05: 向量搜索的单调性 |
| Prop-F-03-06 | F | Flink\03-sql-table-api\flink-sql-window-functions-deep-dive.md | 204 | Prop-F-03-06: 延迟数据保证 |
| Prop-F-03-06 | F | Flink\03-sql-table-api\materialized-tables.md | 195 | Prop-F-03-06: SinkUpsertMateri... |
| Prop-F-03-06 | F | Flink\03-sql-table-api\model-ddl-and-ml-predict.md | 207 | Prop-F-03-06: Schema 兼容性验证 |
| Prop-F-03-06 | F | Flink\03-sql-table-api\vector-search.md | 110 | Prop-F-03-06: 近似搜索的精度-延迟权衡 |
| Prop-F-03-07 | F | Flink\03-sql-table-api\flink-sql-window-functions-deep-dive.md | 219 | Prop-F-03-07: CUMULATE窗口计算效率 |
| Prop-F-03-15 | F | Flink\03-sql-table-api\flink-process-table-functions.md | 122 | Prop-F-03-15: 状态边界保证 |
| Prop-F-03-16 | F | Flink\03-sql-table-api\flink-process-table-functions.md | 134 | Prop-F-03-16:  exactly-once 语义... |
| Prop-F-03-17 | F | Flink\03-sql-table-api\flink-process-table-functions.md | 145 | Prop-F-03-17: 输出单调性 |
| Prop-F-03-18 | F | Flink\03-sql-table-api\flink-process-table-functions.md | 153 | Prop-F-03-18: 状态TTL推导 |
| Prop-F-03-20 | F | Flink\03-sql-table-api\flink-vector-search-rag.md | 212 | Prop-F-03-20: 向量搜索的单调性 |
| Prop-F-03-21 | F | Flink\03-sql-table-api\flink-vector-search-rag.md | 222 | Prop-F-03-21: 近似搜索的精度-召回权衡 |
| Prop-F-03-40 | F | Flink\03-sql-table-api\flink-materialized-table-deep-dive.md | 83 | Prop-F-03-40: 新鲜度与延迟的权衡关系 |
| Prop-F-04-01 | F | Flink\04-connectors\elasticsearch-connector-complete-guide.md | 65 | Prop-F-04-01: 写入性能边界 |
| Prop-F-04-01 | F | Flink\04-connectors\fluss-integration.md | 71 | Prop-F-04-01: 分层存储成本优化 |
| Prop-F-04-01 | F | Flink\04-connectors\kafka-integration-patterns.md | 161 | Prop-F-04-01 (端到端 Exactly-Once... |
| Prop-F-04-02 | F | Flink\04-connectors\elasticsearch-connector-complete-guide.md | 77 | Prop-F-04-02: 版本冲突处理 |
| Prop-F-04-02 | F | Flink\04-connectors\fluss-integration.md | 87 | Prop-F-04-02: Kafka协议兼容性保证 |
| Prop-F-04-02 | F | Flink\04-connectors\mongodb-connector-complete-guide.md | 204 | Prop-F-04-02 (MongoDB Sink 幂等性... |
| Prop-F-04-20 | F | Flink\04-connectors\04.04-cdc-debezium-integration.md | 252 | Prop-F-04-20 (端到端Exactly-Once条... |
| Prop-F-04-20 | F | Flink\04-connectors\cloudevents-integration-guide.md | 254 | Prop-F-04-20 (CloudEvents 端到端可... |
| Prop-F-04-40 | F | Flink\04-connectors\flink-cdc-3.0-data-integration.md | 93 | Prop-F-04-40: 无锁读取的正确性 |
| Prop-F-04-40 | F | Flink\04-connectors\flink-delta-lake-integration.md | 285 | Prop-F-04-40 (流批一致性保证) |
| Prop-F-04-41 | F | Flink\04-connectors\flink-cdc-3.0-data-integration.md | 104 | Prop-F-04-41: 并行读取的线性加速比 |
| Prop-F-04-50 | F | Flink\04-connectors\flink-iceberg-integration.md | 411 | Prop-F-04-50: Flink 流式写入的幂等性保证 |
| Prop-F-04-50 | F | Flink\04-connectors\flink-paimon-integration.md | 296 | Prop-F-04-50: 流批读写隔离性 |
| Prop-F-04-51 | F | Flink\04-connectors\flink-iceberg-integration.md | 444 | Prop-F-04-51: CDC 到 Iceberg 的变... |
| Prop-F-04-51 | F | Flink\04-connectors\flink-paimon-integration.md | 331 | Prop-F-04-51: 主键表的幂等写入 |
| Prop-F-05-01 | F | Flink\05-vs-competitors\flink-vs-kafka-streams.md | 187 | Prop-F-05-01 (处理语义保证的范围差异) |
| Prop-F-05-01 | F | Flink\05-vs-competitors\flink-vs-spark-streaming.md | 127 | Prop-F-05-01 (状态大小与存储架构关系) |
| Prop-F-05-01 | F | Flink\05-vs-competitors\linkedin-samza-deep-dive.md | 155 | Prop-F-05-01: Exactly-Once语义实现 |
| Prop-F-06-01 | F | Flink\06-engineering\state-backend-selection.md | 172 | Prop-F-06-01 (状态后端选型的多目标优化) |
| Prop-F-06-10 | F | Flink\06-engineering\flink-tco-cost-optimization-guide.md | 246 | Prop-F-06-10 (资源利用率与TCO的关系) |
| Prop-F-06-20 | F | Flink\06-engineering\flink-dbt-integration.md | 241 | Prop-F-06-20 (dbt 构建性能与 Flink ... |
| Prop-F-06-40 | F | Flink\06-engineering\stream-processing-cost-optimization.md | 332 | Prop-F-06-40 (分层存储成本递减) |
| Prop-F-07-01 | F | Flink\07-case-studies\case-realtime-analytics.md | 400 | Prop-F-07-01 (端到端延迟上界) |
| Prop-F-07-01 | F | Flink\07-operations\rest-api-complete-reference.md | 41 | Prop-F-07-01: API 幂等性分类 |
| Prop-F-07-02 | F | Flink\07-operations\rest-api-complete-reference.md | 50 | Prop-F-07-02: 响应状态码规范 |
| Prop-F-08-01 | F | Flink\08-roadmap\release-checklist-template.md | 54 | Prop-F-08-01: 发布检查项完备性 |
| Prop-F-08-02 | F | Flink\08-roadmap\release-checklist-template.md | 70 | Prop-F-08-02: 责任矩阵完备性 |
| Prop-F-08-03 | F | Flink\08-roadmap\release-checklist-template.md | 78 | Prop-F-08-03: 时间约束 |
| Prop-F-08-40 | F | Flink\08-roadmap\flink-2.3-2.4-roadmap.md | 105 | Prop-F-08-40: Agent运行时扩展性 |
| Prop-F-08-41 | F | Flink\08-roadmap\flink-2.3-2.4-roadmap.md | 115 | Prop-F-08-41: SSL升级兼容性 |
| Prop-F-08-42 | F | Flink\08-roadmap\community-dynamics-tracking.md | 105 | Prop-F-08-42: 社区活跃度增长定律 |
| Prop-F-08-43 | F | Flink\08-roadmap\community-dynamics-tracking.md | 126 | Prop-F-08-43: 问题处理效率 |
| Prop-F-08-50 | F | Flink\08-roadmap\flink-2.5-preview.md | 156 | Prop-F-08-50: Serverless成本优化比例 |
| Prop-F-08-50 | F | Flink\08-roadmap\flink-30-architecture-redesign.md | 298 | Prop-F-08-50: 统一执行层性能特征 |
| Prop-F-08-50 | F | Flink\08-roadmap\flink-version-evolution-complete-guide.md | 543 | Prop-F-08-50: 状态迁移完备性命题 |
| Prop-F-08-50 | F | Flink\08-roadmap\FLIP-TRACKING-SYSTEM.md | 155 | Prop-F-08-50: FLIP 依赖传递性 |

... 还有 331 个

### 推论 (6个)

| 编号 | 阶段 | 文件 | 行号 | 上下文 |
|------|------|------|------|--------|
| Cor-S-02-01 | S | Struct\01-foundation\01.02-process-calculus-primer.md | 464 | Cor-S-02-01. 良类型会话进程无死锁 |
| Cor-S-14-01 | S | Struct\03-relationships\03.03-expressiveness-hierarchy.md | 421 | Cor-S-14-01. 可判定性递减推论 |
| Cor-S-15-01 | S | Struct\03-relationships\03.04-bisimulation-equivalences.md | 487 | Cor-S-15-01. 互模拟等价类构成商 LTS |
| Cor-S-22-01 | S | Struct\04-proofs\04.06-dot-subtyping-completeness.md | 1095 | - **推论计数**: 1 (Cor-S-22-01) |
| Cor-S-25-01 | S | Struct\05-comparative-analysis\05.02-expressiveness-vs-decidability.md | 367 | Cor-S-25-01. 完全可判定性消失边界 |
| Cor-S-25-02 | S | Struct\05-comparative-analysis\05.02-expressiveness-vs-decidability.md | 380 | Cor-S-25-02. 模型检验可行层次 |

---

*报告由 check-theorem-registry.py 自动生成*
