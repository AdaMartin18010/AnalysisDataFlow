---
title: "[EN] Formal To Code Mapping"
translation_status: "ai_translated"
source_file: "Flink/FORMAL-TO-CODE-MAPPING.md"
source_version: "3a009f38"
translator: "AI"
reviewer: null
translated_at: "2026-04-08T15:15:06.358947"
reviewed_at: null
quality_score: null
terminology_verified: false
---


<!-- AI Translation Template - Replace <!-- TRANSLATE --> markers with actual translation -->

<!-- TRANSLATE: # Flink 形式化定义与源码实现对照表 -->

<!-- TRANSLATE: > 所属阶段: Flink/02-core-mechanisms | 前置依赖: [checkpoint-mechanism-deep-dive.md](./02-core/checkpoint-mechanism-deep-dive.md), [exactly-once-semantics-deep-dive.md](./02-core/exactly-once-semantics-deep-dive.md) | 形式化等级: L5 -->

<!-- TRANSLATE: 本文档建立 Flink 形式化定义与 Apache Flink 源码实现之间的严格映射关系，为理论验证和工程实践提供双向参考。 -->


<!-- TRANSLATE: ## 2. Exactly-Once 语义 -->

<!-- TRANSLATE: ### 2.1 核心定义映射 -->

<!-- TRANSLATE: | 形式化定义 | 定义位置 | 源码类 | 源码位置 | 验证状态 | -->
<!-- TRANSLATE: |-----------|---------|--------|----------|----------| -->
<!-- TRANSLATE: | Def-F-02-91 Exactly-Once | exactly-once-semantics-deep-dive.md | `CheckpointingMode.EXACTLY_ONCE` | `org.apache.flink.streaming.api.CheckpointingMode` | ✅ 已验证 | -->
<!-- TRANSLATE: | Def-F-02-92 端到端 Exactly-Once | exactly-once-semantics-deep-dive.md | `TwoPhaseCommitSinkFunction` | `org.apache.flink.streaming.api.functions.sink.TwoPhaseCommitSinkFunction` | ✅ 已验证 | -->
<!-- TRANSLATE: | Def-F-02-93 一致性语义分类 | exactly-once-semantics-deep-dive.md | `CheckpointingMode` (枚举) | 同上 | ✅ 已验证 | -->
<!-- TRANSLATE: | Def-F-02-94 屏障对齐与非对齐 | exactly-once-semantics-deep-dive.md | `CheckpointBarrierAligner` / `Unaligner` | `flink-streaming-java` 模块 | ✅ 已验证 | -->
<!-- TRANSLATE: | Def-F-02-95 2PC 协议状态机 | exactly-once-semantics-deep-dive.md | `TwoPhaseCommitSinkFunction` | 内部状态管理 | ✅ 已验证 | -->

<!-- TRANSLATE: ### 2.2 属性引理映射 -->

<!-- TRANSLATE: | 形式化定义 | 定义位置 | 源码类 | 源码位置 | 验证状态 | -->
<!-- TRANSLATE: |-----------|---------|--------|----------|----------| -->
<!-- TRANSLATE: | Lemma-F-02-71 屏障对齐保证因果一致性 | exactly-once-semantics-deep-dive.md | `CheckpointBarrierAligner` | `flink-streaming-java` | ✅ 已验证 | -->
<!-- TRANSLATE: | Lemma-F-02-72 非对齐 Checkpoint 的有界一致性 | exactly-once-semantics-deep-dive.md | `CheckpointBarrierUnaligner` | `flink-streaming-java` | ✅ 已验证 | -->
<!-- TRANSLATE: | Lemma-F-02-73 对齐 Checkpoint 延迟上界 | exactly-once-semantics-deep-dive.md | `CheckpointBarrierAligner#alignmentDuration` | 对齐超时监控 | ✅ 已验证 | -->
<!-- TRANSLATE: | Lemma-F-02-74 事务超时与一致性 | exactly-once-semantics-deep-dive.md | `TwoPhaseCommitSinkFunction#notifyCheckpointComplete` | 事务超时处理 | ✅ 已验证 | -->

<!-- TRANSLATE: ### 2.3 定理源码验证 -->

<!-- TRANSLATE: | 形式化定义 | 定义位置 | 源码类 | 源码位置 | 验证状态 | -->
<!-- TRANSLATE: |-----------|---------|--------|----------|----------| -->
<!-- TRANSLATE: | Thm-F-02-71 端到端 Exactly-Once 充分条件 | exactly-once-semantics-deep-dive.md | `TwoPhaseCommitSinkFunction` | 完整实现 | ✅ 已验证 | -->
<!-- TRANSLATE: | Thm-F-02-72 2PC 原子性保证 | exactly-once-semantics-deep-dive.md | `TwoPhaseCommitSinkFunction#commit` / `abort` | 事务提交与回滚 | ✅ 已验证 | -->


<!-- TRANSLATE: ## 4. Watermark 机制 -->

<!-- TRANSLATE: ### 4.1 核心定义映射 -->

<!-- TRANSLATE: | 形式化定义 | 定义位置 | 源码类 | 源码位置 | 验证状态 | -->
<!-- TRANSLATE: |-----------|---------|--------|----------|----------| -->
<!-- TRANSLATE: | Def-F-02-01 Event Time | time-semantics-and-watermark.md | `TimeCharacteristic.EventTime` | `org.apache.flink.streaming.api.TimeCharacteristic` | ✅ 已验证 | -->
<!-- TRANSLATE: | Def-F-02-02 Processing Time | time-semantics-and-watermark.md | `TimeCharacteristic.ProcessingTime` | 同上 | ✅ 已验证 | -->
<!-- TRANSLATE: | Def-F-02-03 Ingestion Time | time-semantics-and-watermark.md | `TimeCharacteristic.IngestionTime` | 同上 | ✅ 已验证 | -->
<!-- TRANSLATE: | Def-F-02-04 Watermark | time-semantics-and-watermark.md | `Watermark` | `org.apache.flink.streaming.api.watermark.Watermark` | ✅ 已验证 | -->
<!-- TRANSLATE: | Def-F-02-05 Allowed Lateness | time-semantics-and-watermark.md | `WindowedStream#allowedLateness` | `flink-streaming-java` | ✅ 已验证 | -->
<!-- TRANSLATE: | Def-F-02-06 Window | time-semantics-and-watermark.md | `Window` / `TimeWindow` | `org.apache.flink.streaming.api.windowing.windows` | ✅ 已验证 | -->

<!-- TRANSLATE: ### 4.2 属性引理映射 -->

<!-- TRANSLATE: | 形式化定义 | 定义位置 | 源码类 | 源码位置 | 验证状态 | -->
<!-- TRANSLATE: |-----------|---------|--------|----------|----------| -->
<!-- TRANSLATE: | Lemma-F-02-01 Watermark 单调性 | time-semantics-and-watermark.md | `StatusWatermarkValve` | `org.apache.flink.streaming.runtime.io.StatusWatermarkValve` | ✅ 已验证 | -->
<!-- TRANSLATE: | Lemma-F-02-02 窗口分配完备性 | time-semantics-and-watermark.md | `WindowAssigner` | `org.apache.flink.streaming.api.windowing.assigners` | ✅ 已验证 | -->
<!-- TRANSLATE: | Lemma-F-02-03 延迟上界定理 | time-semantics-and-watermark.md | `BoundedOutOfOrdernessWatermarks` | `org.apache.flink.api.common.eventtime` | ✅ 已验证 | -->

<!-- TRANSLATE: ### 4.3 定理源码验证 -->

<!-- TRANSLATE: | 形式化定义 | 定义位置 | 源码类 | 源码位置 | 验证状态 | -->
<!-- TRANSLATE: |-----------|---------|--------|----------|----------| -->
<!-- TRANSLATE: | Thm-F-02-01 Event Time 结果确定性定理 | time-semantics-and-watermark.md | `EventTimeTrigger` / `WatermarkStrategy` | 时间触发机制 | ✅ 已验证 | -->
<!-- TRANSLATE: | Thm-F-02-02 Allowed Lateness 不破坏 Exactly-Once | time-semantics-and-watermark.md | `LateDataHandling` | 迟到数据处理 | ✅ 已验证 | -->


<!-- TRANSLATE: ## 6. 容错与恢复 -->

<!-- TRANSLATE: ### 6.1 核心定义映射 -->

<!-- TRANSLATE: | 形式化定义 | 定义位置 | 源码类 | 源码位置 | 验证状态 | -->
<!-- TRANSLATE: |-----------|---------|--------|----------|----------| -->
<!-- TRANSLATE: | Savepoint 机制 | flink-state-management-complete-guide.md | `SavepointLoader` | `org.apache.flink.runtime.checkpoint.SavepointLoader` | ✅ 已验证 | -->
<!-- TRANSLATE: | 状态恢复 | checkpoint-mechanism-deep-dive.md | `StateBackend#restore` | 恢复接口 | ✅ 已验证 | -->
<!-- TRANSLATE: | 任务故障恢复 | checkpoint-mechanism-deep-dive.md | `FailoverStrategy` | `org.apache.flink.runtime.executiongraph.failover` | ✅ 已验证 | -->


<!-- TRANSLATE: ## 8. 源码引用规范 -->

<!-- TRANSLATE: ### 8.1 模块结构 -->

```
flink-runtime/              # 运行时核心
├── checkpoint/             # Checkpoint 机制
│   ├── CheckpointCoordinator.java
│   ├── CheckpointBarrier.java
│   └── ...
├── state/                  # 状态管理
│   ├── StateBackend.java
│   ├── v2/                 # State V2 API
│   └── ...
└── asyncprocessing/        # 异步执行
    ├── AsyncExecutionController.java
    └── ...

flink-streaming-java/       # DataStream API
├── streaming/api/
│   ├── watermark/Watermark.java
│   ├── environment/CheckpointConfig.java
│   └── ...
└── streaming/runtime/io/
    ├── CheckpointBarrierAligner.java
    ├── CheckpointBarrierUnaligner.java
    └── StatusWatermarkValve.java

flink-state-backends/       # 状态后端实现
├── flink-statebackend-rocksdb/
│   └── EmbeddedRocksDBStateBackend.java
└── flink-statebackend-forst/
    └── ForStStateBackend.java
```

<!-- TRANSLATE: ### 8.2 引用格式 -->

<!-- TRANSLATE: 源码引用遵循以下格式： -->

```
完整类名: org.apache.flink.{module}.{package}.{ClassName}
方法: {ClassName}#{methodName}
行号: 第 {start}-{end} 行
模块: flink-{module}
```


<!-- TRANSLATE: ## 10. 引用参考 (References) -->





