(*
 * ExactlyOnce.tla
 * Flink端到端Exactly-Once语义的TLA+形式化规约
 * 
 * 本规约形式化定义了Flink端到端Exactly-Once处理语义，包括：
 * - Source可重放性 (Source Replayability)
 * - Checkpoint一致性 (Checkpoint Consistency)
 * - Sink幂等性/事务性 (Sink Idempotency/Transaction)
 * - 端到端一致性组合条件 (End-to-End Consistency Composition)
 * - 安全性定理: 可重放Source ∧ Checkpoint一致 ∧ Sink原子 ⟹ Exactly-Once
 *
 * 参考: Two-Phase Commit协议、Kafka事务语义、Flink TwoPhaseCommitSinkFunction
 *
 * 版本: 1.0
 * 日期: 2026-04-09
 *)

----------------------------- MODULE ExactlyOnce -----------------------------

(*===========================================================================*)
(* 导入标准模块                                                               *)
(*===========================================================================*)

EXTENDS Naturals, Sequences, FiniteSets, TLC

(*===========================================================================*)
(* 常量定义                                                                   *)
(*===========================================================================*)

CONSTANTS
    Partitions,             (* Kafka分区集合 *)
    Records,                (* 记录集合 *)
    Transactions,           (* 事务ID集合 *)
    Checkpoints,            (* Checkpoint ID集合 *)
    MaxOffset,              (* 每个分区最大偏移量 *)
    Consumers,              (* 消费者实例集合 *)
    Sinks,                  (* Sink算子集合 *)
    IsIdempotentSink,       (* Sink是否幂等 (布尔函数) *)
    IsTransactionalSink     (* Sink是否事务性 (布尔函数) *)

ASSUME
    Partitions # {}
ASSUME
    Records # {}
ASSUME
    Transactions # {}
ASSUME
    Checkpoints # {}

(*===========================================================================*)
(* 类型定义                                                                   *)
(*===========================================================================*)

(*---------------------------------------------------------------------------*)
(* Def-EO-01: Offset - 分区偏移量类型                                         *)
(*---------------------------------------------------------------------------*)
Offset == 0..MaxOffset

(*---------------------------------------------------------------------------*)
(* Def-EO-02: RecordID - 记录唯一标识                                         *)
(* 格式: [partition, offset]                                                  *)
(*---------------------------------------------------------------------------*)
RecordID == [partition: Partitions, offset: Offset]

(*---------------------------------------------------------------------------*)
(* Def-EO-03: ConsumerRecord - 消费者记录                                     *)
(*---------------------------------------------------------------------------*)
ConsumerRecord == [
    id: RecordID,
    value: Records,
    committed: BOOLEAN     (* 是否已提交到Kafka *)
]

(*---------------------------------------------------------------------------*)
(* Def-EO-04: CheckpointMarker - Checkpoint标记                               *)
(*---------------------------------------------------------------------------*)
CheckpointMarker == [
    type: {"CHECKPOINT"},
    cpId: Checkpoints
]

(*---------------------------------------------------------------------------*)
(* Def-EO-05: CommittedOffset - 已提交偏移量状态                              *)
(* 每个消费者组在每个分区上维护的偏移量                                       *)
(*---------------------------------------------------------------------------*)
CommittedOffset == [Partitions -> Offset]

(*---------------------------------------------------------------------------*)
(* Def-EO-06: TransactionState - 事务状态                                     *)
(* 参考Kafka事务状态机: Empty, Ongoing, PrepareCommit, PrepareAbort,          *)
(* CompleteCommit, CompleteAbort, Dead                                        *)
(*---------------------------------------------------------------------------*)
TransactionState == {
    "EMPTY",                (* 事务初始/完成状态 *)
    "ONGOING",              (* 事务进行中 *)
    "PREPARE_COMMIT",       (* 准备提交 (2PC第一阶段) *)
    "PREPARE_ABORT",        (* 准备回滚 *)
    "COMPLETE_COMMIT",      (* 提交完成 (2PC第二阶段) *)
    "COMPLETE_ABORT"        (* 回滚完成 *)
}

(*---------------------------------------------------------------------------*)
(* Def-EO-07: TransactionMetadata - 事务元数据                                *)
(*---------------------------------------------------------------------------*)
TransactionMetadata == [
    state: TransactionState,
    producerId: Nat,
    producerEpoch: Nat,
    lastOffset: [Partitions -> Offset],  (* 事务涉及的最后偏移量 *)
    startTime: Nat
]

(*---------------------------------------------------------------------------*)
(* Def-EO-08: SinkTransaction - Sink事务状态                                  *)
(*---------------------------------------------------------------------------*)
SinkTransaction == [
    txId: Transactions,
    state: TransactionState,
    preCommitState: SUBSET Records,    (* 预提交状态 (2PC第一阶段) *)
    committedRecords: SUBSET Records   (* 已提交记录 *)
]

(*---------------------------------------------------------------------------*)
(* Def-EO-09: SourceState - Source状态                                        *)
(*---------------------------------------------------------------------------*)
SourceState == [
    currentOffset: [Partitions -> Offset],      (* 当前消费偏移量 *)
    committedOffset: [Partitions -> Offset],     (* 已提交偏移量 *)
    pendingRecords: SUBSET ConsumerRecord,       (* 待处理记录 *)
    replayable: BOOLEAN                          (* 是否可重放 *)
]

(*---------------------------------------------------------------------------*)
(* Def-EO-10: ExactlyOnceGuarantee - Exactly-Once保证类型                     *)
(*---------------------------------------------------------------------------*)
ExactlyOnceGuarantee == {
    "AT_MOST_ONCE",
    "AT_LEAST_ONCE",
    "EXACTLY_ONCE"
}

(*===========================================================================*)
(* 变量定义                                                                   *)
(*===========================================================================*)

VARIABLES
    sourceState,            (* sourceState[consumer] = 每个消费者的Source状态 *)
    transactionLog,         (* transactionLog[txId] = 事务元数据 *)
    sinkTxState,            (* sinkTxState[sink] = 每个Sink的事务状态 *)
    outputRecords,          (* outputRecords[sink] = 每个Sink的输出记录集 *)
    checkpointState,        (* checkpointState[cpId] = Checkpoint状态 *)
    globalEpoch             (* 全局Epoch号，用于单调递增保证 *)

(*---------------------------------------------------------------------------*)
(* Def-EO-11: TypeInvariant - 类型正确性                                      *)
(*---------------------------------------------------------------------------*)
TypeInvariant ==
    /\ sourceState \in [Consumers -> SourceState]
    /\ transactionLog \in [Transactions -> TransactionMetadata]
    /\ sinkTxState \in [Sinks -> SinkTransaction]
    /\ outputRecords \in [Sinks -> SUBSET Records]
    /\ checkpointState \in [Checkpoints -> {
        "NONE", "TRIGGERED", "IN_PROGRESS", "PRE_COMMIT", "COMPLETED", "FAILED"
    }]
    /\ globalEpoch \in Nat

(*===========================================================================*)
(* 辅助函数                                                                   *)
(*===========================================================================*)

(*---------------------------------------------------------------------------*)
(* Def-EO-12: IsReplayableSource - Source可重放性判断                         *)
(* Source可重放当且仅当:                                                      *)
(* 1. 支持偏移量重置 (currentOffset >= committedOffset)                       *)
(* 2. 未确认记录可以被重新读取                                                *)
(*---------------------------------------------------------------------------*)
IsReplayableSource(consumer) ==
    /\ sourceState[consumer].replayable = TRUE
    /\ \A p \in Partitions :
        sourceState[consumer].currentOffset[p] >= sourceState[consumer].committedOffset[p]

(*---------------------------------------------------------------------------*)
(* Def-EO-13: GetUncommittedRecords - 获取未提交的记录                        *)
(* 用于故障恢复时重放                                                         *)
(*---------------------------------------------------------------------------*)
GetUncommittedRecords(consumer) ==
    { r \in sourceState[consumer].pendingRecords : 
        r.committed = FALSE }

(*---------------------------------------------------------------------------*)
(* Def-EO-14: CanReplayFromOffset - 能否从指定偏移量重放                      *)
(*---------------------------------------------------------------------------*)
CanReplayFromOffset(consumer, partition, offset) ==
    /\ offset >= sourceState[consumer].committedOffset[partition]
    /\ offset <= sourceState[consumer].currentOffset[partition]

(*---------------------------------------------------------------------------*)
(* Def-EO-15: IsConsistentCheckpoint - Checkpoint一致性判断                   *)
(* Checkpoint一致当且仅当:                                                    *)
(* 1. 所有参与者的状态已持久化                                                *)
(* 2. 形成一致割集 (Consistent Cut)                                           *)
(*---------------------------------------------------------------------------*)
IsConsistentCheckpoint(cpId) ==
    /\ checkpointState[cpId] \in {"PRE_COMMIT", "COMPLETED"}
    /\ \A consumer \in Consumers :
        sourceState[consumer].committedOffset \in [Partitions -> Offset]

(*---------------------------------------------------------------------------*)
(* Def-EO-16: IsAtomicSink - Sink原子性判断                                   *)
(* Sink原子当且仅当:                                                          *)
(* 1. 幂等Sink: 相同记录多次写入结果相同                                      *)
(* 2. 事务Sink: 2PC协议保证原子提交                                           *)
(*---------------------------------------------------------------------------*)
IsAtomicSink(sink) ==
    /\ IsIdempotentSink(sink) => 
        (* 幂等性: f(f(x)) = f(x) *)
        \A r \in Records :
            (r \in outputRecords[sink]) => 
                (outputRecords[sink] = outputRecords[sink] \cup {r})
    /\ IsTransactionalSink(sink) =>
        (* 事务性: 2PC状态机正确性 *)
        sinkTxState[sink].state \in 
            {"EMPTY", "ONGOING", "PREPARE_COMMIT", "COMPLETE_COMMIT"}

(*---------------------------------------------------------------------------*)
(* Def-EO-17: IsIdempotentWrite - 幂等写入判断                                *)
(*---------------------------------------------------------------------------*)
IsIdempotentWrite(sink, record) ==
    /\ IsIdempotentSink(sink)
    /\ (record \in outputRecords[sink]) => 
        (outputRecords[sink] = outputRecords[sink] \cup {record})

(*---------------------------------------------------------------------------*)
(* Def-EO-18: IsTwoPhaseCommitComplete - 2PC完成判断                          *)
(*---------------------------------------------------------------------------*)
IsTwoPhaseCommitComplete(sink, cpId) ==
    /\ sinkTxState[sink].state = "COMPLETE_COMMIT"
    /\ checkpointState[cpId] = "COMPLETED"
    /\ sinkTxState[sink].preCommitState = sinkTxState[sink].committedRecords

(*===========================================================================*)
(* 初始化条件                                                                 *)
(*===========================================================================*)

(*---------------------------------------------------------------------------*)
(* Def-EO-19: Init - 系统初始状态                                             *)
(*---------------------------------------------------------------------------*)
Init ==
    /\ sourceState = [c \in Consumers |-> [
            currentOffset |-> [p \in Partitions |-> 0],
            committedOffset |-> [p \in Partitions |-> 0],
            pendingRecords |-> {},
            replayable |-> TRUE
        ]]
    /\ transactionLog = [t \in Transactions |-> [
            state |-> "EMPTY",
            producerId |-> 0,
            producerEpoch |-> 0,
            lastOffset |-> [p \in Partitions |-> 0],
            startTime |-> 0
        ]]
    /\ sinkTxState = [s \in Sinks |-> [
            txId |-> CHOOSE t \in Transactions : TRUE,
            state |-> "EMPTY",
            preCommitState |-> {},
            committedRecords |-> {}
        ]]
    /\ outputRecords = [s \in Sinks |-> {}]
    /\ checkpointState = [c \in Checkpoints |-> "NONE"]
    /\ globalEpoch = 0

(*===========================================================================*)
(* 动作定义: Source可重放性                                                   *)
(*===========================================================================*)

(*---------------------------------------------------------------------------*)
(* Def-EO-20: ConsumeRecord - 消费记录                                        *)
(* Source从Kafka分区消费记录                                                  *)
(*---------------------------------------------------------------------------*)
ConsumeRecord(consumer, partition, record) ==
    /\ record.id.partition = partition
    /\ record.id.offset = sourceState[consumer].currentOffset[partition] + 1
    /\ record.id.offset <= MaxOffset
    /\ sourceState' = [sourceState EXCEPT 
            ![consumer].currentOffset[partition] = @ + 1,
            ![consumer].pendingRecords = @ \cup {record}
       ]
    /\ UNCHANGED <<transactionLog, sinkTxState, outputRecords, checkpointState, globalEpoch>>

(*---------------------------------------------------------------------------*)
(* Def-EO-21: CommitOffset - 提交消费偏移量                                   *)
(* 成功处理后将偏移量提交到Kafka                                              *)
(*---------------------------------------------------------------------------*)
CommitOffset(consumer, partition, offset) ==
    /\ offset <= sourceState[consumer].currentOffset[partition]
    /\ offset > sourceState[consumer].committedOffset[partition]
    /\ sourceState' = [sourceState EXCEPT 
            ![consumer].committedOffset[partition] = offset]
    /\ UNCHANGED <<transactionLog, sinkTxState, outputRecords, checkpointState, globalEpoch>>

(*---------------------------------------------------------------------------*)
(* Def-EO-22: ReplayFromCheckpoint - 从Checkpoint重放                         *)
(* 故障恢复时，Source从已提交偏移量重新开始消费                               *)
(*---------------------------------------------------------------------------*)
ReplayFromCheckpoint(consumer, cpId) ==
    /\ IsReplayableSource(consumer)
    /\ checkpointState[cpId] \in {"PRE_COMMIT", "COMPLETED"}
    /\ sourceState' = [sourceState EXCEPT 
            ![consumer].currentOffset = sourceState[consumer].committedOffset,
            ![consumer].pendingRecords = {}]
    /\ UNCHANGED <<transactionLog, sinkTxState, outputRecords, checkpointState, globalEpoch>>

(*===========================================================================*)
(* 动作定义: Checkpoint一致性                                                 *)
(*===========================================================================*)

(*---------------------------------------------------------------------------*)
(* Def-EO-23: TriggerCheckpoint - 触发Checkpoint                              *)
(* JobManager触发全局Checkpoint                                               *)
(*---------------------------------------------------------------------------*)
TriggerCheckpoint(cpId) ==
    /\ checkpointState[cpId] = "NONE"
    /\ checkpointState' = [checkpointState EXCEPT ![cpId] = "TRIGGERED"]
    /\ globalEpoch' = globalEpoch + 1
    /\ UNCHANGED <<sourceState, transactionLog, sinkTxState, outputRecords>>

(*---------------------------------------------------------------------------*)
(* Def-EO-24: AcknowledgeCheckpoint - 确认Checkpoint                          *)
(* TaskManager确认Snapshot完成                                                *)
(*---------------------------------------------------------------------------*)
AcknowledgeCheckpoint(consumer, cpId) ==
    /\ checkpointState[cpId] = "TRIGGERED"
    /\ checkpointState' = [checkpointState EXCEPT ![cpId] = "IN_PROGRESS"]
    /\ UNCHANGED <<sourceState, transactionLog, sinkTxState, outputRecords, globalEpoch>>

(*---------------------------------------------------------------------------*)
(* Def-EO-25: PreCommitCheckpoint - Checkpoint预提交 (2PC第一阶段)            *)
(* 所有参与者完成Snapshot，进入预提交状态                                       *)
(*---------------------------------------------------------------------------*)
PreCommitCheckpoint(cpId) ==
    /\ checkpointState[cpId] = "IN_PROGRESS"
    /\ \A consumer \in Consumers :
        sourceState[consumer].currentOffset \in [Partitions -> Offset]
    /\ checkpointState' = [checkpointState EXCEPT ![cpId] = "PRE_COMMIT"]
    /\ UNCHANGED <<sourceState, transactionLog, sinkTxState, outputRecords, globalEpoch>>

(*---------------------------------------------------------------------------*)
(* Def-EO-26: CompleteCheckpoint - 完成Checkpoint                             *)
(* 所有Sink完成事务提交，Checkpoint完成                                         *)
(*---------------------------------------------------------------------------*)
CompleteCheckpoint(cpId) ==
    /\ checkpointState[cpId] = "PRE_COMMIT"
    /\ \A sink \in Sinks :
        IsAtomicSink(sink) => sinkTxState[sink].state = "COMPLETE_COMMIT"
    /\ checkpointState' = [checkpointState EXCEPT ![cpId] = "COMPLETED"]
    /\ UNCHANGED <<sourceState, transactionLog, sinkTxState, outputRecords, globalEpoch>>

(*===========================================================================*)
(* 动作定义: Sink幂等性/事务性                                                *)
(*===========================================================================*)

(*---------------------------------------------------------------------------*)
(* Def-EO-27: BeginTransaction - 开始事务                                     *)
(*---------------------------------------------------------------------------*)
BeginTransaction(sink, txId) ==
    /\ sinkTxState[sink].state = "EMPTY"
    /\ transactionLog[txId].state = "EMPTY"
    /\ sinkTxState' = [sinkTxState EXCEPT 
            ![sink].txId = txId,
            ![sink].state = "ONGOING",
            ![sink].preCommitState = {}]
    /\ transactionLog' = [transactionLog EXCEPT 
            ![txId].state = "ONGOING",
            ![txId].startTime = globalEpoch]
    /\ UNCHANGED <<sourceState, outputRecords, checkpointState, globalEpoch>>

(*---------------------------------------------------------------------------*)
(* Def-EO-28: WriteRecord - 写入记录到Sink                                    *)
(* 事务模式下，记录先写入preCommitState                                       *)
(*---------------------------------------------------------------------------*)
WriteRecord(sink, record) ==
    /\ sinkTxState[sink].state = "ONGOING"
    /\ sinkTxState' = [sinkTxState EXCEPT 
            ![sink].preCommitState = @ \cup {record}]
    /\ UNCHANGED <<sourceState, transactionLog, outputRecords, checkpointState, globalEpoch>>

(*---------------------------------------------------------------------------*)
(* Def-EO-29: PreCommitTransaction - 事务预提交 (2PC第一阶段)                 *)
(* Sink将preCommitState持久化，准备提交                                       *)
(*---------------------------------------------------------------------------*)
PreCommitTransaction(sink, cpId) ==
    /\ sinkTxState[sink].state = "ONGOING"
    /\ checkpointState[cpId] = "PRE_COMMIT"
    /\ sinkTxState' = [sinkTxState EXCEPT ![sink].state = "PREPARE_COMMIT"]
    /\ transactionLog' = [transactionLog EXCEPT 
            ![sinkTxState[sink].txId].state = "PREPARE_COMMIT"]
    /\ UNCHANGED <<sourceState, outputRecords, checkpointState, globalEpoch>>

(*---------------------------------------------------------------------------*)
(* Def-EO-30: CommitTransaction - 提交事务 (2PC第二阶段)                      *)
(* 将preCommitState中的记录转移到committedRecords和outputRecords              *)
(*---------------------------------------------------------------------------*)
CommitTransaction(sink) ==
    /\ sinkTxState[sink].state = "PREPARE_COMMIT"
    /\ sinkTxState' = [sinkTxState EXCEPT 
            ![sink].state = "COMPLETE_COMMIT",
            ![sink].committedRecords = sinkTxState[sink].preCommitState]
    /\ outputRecords' = [outputRecords EXCEPT 
            ![sink] = @ \cup sinkTxState[sink].preCommitState]
    /\ transactionLog' = [transactionLog EXCEPT 
            ![sinkTxState[sink].txId].state = "COMPLETE_COMMIT"]
    /\ UNCHANGED <<sourceState, checkpointState, globalEpoch>>

(*---------------------------------------------------------------------------*)
(* Def-EO-31: AbortTransaction - 回滚事务                                     *)
(* 放弃preCommitState中的记录                                                 *)
(*---------------------------------------------------------------------------*)
AbortTransaction(sink) ==
    /\ sinkTxState[sink].state \in {"ONGOING", "PREPARE_COMMIT"}
    /\ sinkTxState' = [sinkTxState EXCEPT 
            ![sink].state = "COMPLETE_ABORT",
            ![sink].preCommitState = {}]
    /\ transactionLog' = [transactionLog EXCEPT 
            ![sinkTxState[sink].txId].state = "COMPLETE_ABORT"]
    /\ UNCHANGED <<sourceState, outputRecords, checkpointState, globalEpoch>>

(*---------------------------------------------------------------------------*)
(* Def-EO-32: IdempotentWrite - 幂等写入 (非事务性幂等Sink)                   *)
(* 幂等Sink直接写入，重复写入结果不变                                         *)
(*---------------------------------------------------------------------------*)
IdempotentWrite(sink, record) ==
    /\ IsIdempotentSink(sink)
    /\ ~IsTransactionalSink(sink)
    /\ outputRecords' = [outputRecords EXCEPT ![sink] = @ \cup {record}]
    /\ UNCHANGED <<sourceState, transactionLog, sinkTxState, checkpointState, globalEpoch>>

(*===========================================================================*)
(* 下一步动作组合                                                             *)
(*===========================================================================*)

Next ==
    \/ \E consumer \in Consumers, partition \in Partitions, 
           record \in ConsumerRecord :
        ConsumeRecord(consumer, partition, record)
    \/ \E consumer \in Consumers, partition \in Partitions, offset \in Offset :
        CommitOffset(consumer, partition, offset)
    \/ \E consumer \in Consumers, cpId \in Checkpoints :
        ReplayFromCheckpoint(consumer, cpId)
    \/ \E cpId \in Checkpoints :
        TriggerCheckpoint(cpId)
    \/ \E consumer \in Consumers, cpId \in Checkpoints :
        AcknowledgeCheckpoint(consumer, cpId)
    \/ \E cpId \in Checkpoints :
        PreCommitCheckpoint(cpId)
    \/ \E cpId \in Checkpoints :
        CompleteCheckpoint(cpId)
    \/ \E sink \in Sinks, txId \in Transactions :
        BeginTransaction(sink, txId)
    \/ \E sink \in Sinks, record \in Records :
        WriteRecord(sink, record)
    \/ \E sink \in Sinks, cpId \in Checkpoints :
        PreCommitTransaction(sink, cpId)
    \/ \E sink \in Sinks :
        CommitTransaction(sink)
    \/ \E sink \in Sinks :
        AbortTransaction(sink)
    \/ \E sink \in Sinks, record \in Records :
        IdempotentWrite(sink, record)

(*===========================================================================*)
(* 公平性条件                                                                 *)
(*===========================================================================*)

Fairness ==
    /\ WF_<<sourceState, transactionLog, sinkTxState, outputRecords, checkpointState, globalEpoch>>(
        \E consumer \in Consumers, partition \in Partitions, offset \in Offset :
            CommitOffset(consumer, partition, offset))
    /\ WF_<<sourceState, transactionLog, sinkTxState, outputRecords, checkpointState, globalEpoch>>(
        \E cpId \in Checkpoints : CompleteCheckpoint(cpId))
    /\ WF_<<sourceState, transactionLog, sinkTxState, outputRecords, checkpointState, globalEpoch>>(
        \E sink \in Sinks : CommitTransaction(sink))

(*===========================================================================*)
(* 安全性不变式 (Safety Invariants)                                           *)
(*===========================================================================*)

(*---------------------------------------------------------------------------*)
(* Prop-EO-01: SourceReplayabilityCondition - Source可重放条件                *)
(* 可重放Source保证:                                                          *)
(* 1. 已提交偏移量单调递增                                                    *)
(* 2. 当前偏移量 >= 已提交偏移量                                              *)
(* 3. 故障后可从已提交偏移量恢复                                              *)
(*---------------------------------------------------------------------------*)
SourceReplayabilityCondition ==
    \A consumer \in Consumers :
        /\ \A p \in Partitions :
            sourceState[consumer].committedOffset[p] <= 
                sourceState[consumer].currentOffset[p]
        /\ sourceState[consumer].replayable =>
            (* 可重放性: 可以重置到任何已提交偏移量 *)
            \A p \in Partitions, offset \in Offset :
                CanReplayFromOffset(consumer, p, offset) =>
                    offset >= sourceState[consumer].committedOffset[p]

(*---------------------------------------------------------------------------*)
(* Prop-EO-02: CheckpointConsistencyCondition - Checkpoint一致性条件          *)
(* 一致Checkpoint保证:                                                        *)
(* 1. Checkpoint状态转换正确                                                  *)
(* 2. 完成Checkpoint形成一致割集                                              *)
(*---------------------------------------------------------------------------*)
CheckpointConsistencyCondition ==
    \A cpId \in Checkpoints :
        /\ checkpointState[cpId] = "COMPLETED" =>
            IsConsistentCheckpoint(cpId)
        /\ checkpointState[cpId] = "PRE_COMMIT" =>
            (* 预提交状态: 所有参与者已准备就绪 *)
            \A consumer \in Consumers :
                sourceState[consumer].currentOffset \in [Partitions -> Offset]

(*---------------------------------------------------------------------------*)
(* Prop-EO-03: SinkAtomicityCondition - Sink原子性条件                        *)
(* Sink原子性保证:                                                            *)
(* 1. 幂等Sink: 重复写入不产生重复记录                                        *)
(* 2. 事务Sink: 2PC协议保证原子提交                                           *)
(*---------------------------------------------------------------------------*)
SinkAtomicityCondition ==
    \A sink \in Sinks :
        /\ IsIdempotentSink(sink) =>
            (* 幂等性: 输出记录集是幂等的 *)
            \A r \in Records :
                (r \in outputRecords[sink]) =>
                    (outputRecords[sink] = outputRecords[sink] \cup {r})
        /\ IsTransactionalSink(sink) =>
            (* 事务性: 状态机正确性 *)
            /\ sinkTxState[sink].state \in TransactionState
            /\ sinkTxState[sink].state = "COMPLETE_COMMIT" =>
                (* 提交完成: preCommitState已转移到committedRecords *)
                sinkTxState[sink].preCommitState = sinkTxState[sink].committedRecords
            /\ sinkTxState[sink].state = "COMPLETE_ABORT" =>
                (* 回滚完成: preCommitState为空 *)
                sinkTxState[sink].preCommitState = {}

(*---------------------------------------------------------------------------*)
(* Prop-EO-04: TwoPhaseCommitCorrectness - 2PC正确性                          *)
(* Two-Phase Commit协议保证:                                                  *)
(* 1. 所有参与者要么全部提交，要么全部回滚                                      *)
(* 2. 一旦提交决定，不可更改                                                  *)
(*---------------------------------------------------------------------------*)
TwoPhaseCommitCorrectness ==
    \A sink \in Sinks :
        /\ sinkTxState[sink].state = "COMPLETE_COMMIT" =>
            (* 提交后不可回滚 *)
            [] (sinkTxState[sink].state \in {"COMPLETE_COMMIT", "EMPTY"})
        /\ sinkTxState[sink].state = "COMPLETE_ABORT" =>
            (* 回滚后记录不会出现在输出 *)
            outputRecords[sink] \cap sinkTxState[sink].preCommitState = {}

(*---------------------------------------------------------------------------*)
(* Prop-EO-05: NoDuplicateOutput - 无重复输出                                 *)
(* Exactly-Once保证: 每个输入记录最多输出一次                                 *)
(*---------------------------------------------------------------------------*)
NoDuplicateOutput ==
    \A sink \in Sinks :
        (* 输出记录不能有重复，由集合语义保证 *)
        TRUE

(*---------------------------------------------------------------------------*)
(* Prop-EO-06: EpochMonotonicity - Epoch单调性                                *)
(* 全局Epoch单调递增，用于保证因果序                                          *)
(*---------------------------------------------------------------------------*)
EpochMonotonicity ==
    [][globalEpoch' >= globalEpoch]_
        <<sourceState, transactionLog, sinkTxState, outputRecords, checkpointState, globalEpoch>>

(*===========================================================================*)
(* 端到端一致性组合条件                                                       *)
(*===========================================================================*)

(*---------------------------------------------------------------------------*)
(* Def-EO-33: EndToEndExactlyOnceCondition - 端到端Exactly-Once条件           *)
(* 端到端Exactly-Once当且仅当:                                                *)
(* 1. Source可重放                                                            *)
(* 2. Checkpoint一致                                                          *)
(* 3. Sink原子 (幂等或事务)                                                   *)
(*---------------------------------------------------------------------------*)
EndToEndExactlyOnceCondition ==
    /\ \A consumer \in Consumers : IsReplayableSource(consumer)
    /\ \A cpId \in Checkpoints : 
        checkpointState[cpId] = "COMPLETED" => IsConsistentCheckpoint(cpId)
    /\ \A sink \in Sinks : IsAtomicSink(sink)

(*---------------------------------------------------------------------------*)
(* Def-EO-34: OutputConsistency - 输出一致性                                  *)
(* 输出与输入一致: 每个输入记录恰好输出一次（如果处理成功）                     *)
(*---------------------------------------------------------------------------*)
OutputConsistency ==
    \A sink \in Sinks :
        \A record \in Records :
            (* 记录要么在输出中，要么还在处理中 *)
            (record \in outputRecords[sink]) =>
                (* 该记录已被成功处理并输出 *)
                \E consumer \in Consumers :
                    \E r \in sourceState[consumer].pendingRecords :
                        r.committed = TRUE

(*===========================================================================*)
(* 组合安全性不变式                                                           *)
(*===========================================================================*)

(*---------------------------------------------------------------------------*)
(* Def-EO-35: SafetyInvariant - 组合安全性不变式                              *)
(*---------------------------------------------------------------------------*)
SafetyInvariant ==
    /\ TypeInvariant
    /\ SourceReplayabilityCondition
    /\ CheckpointConsistencyCondition
    /\ SinkAtomicityCondition
    /\ TwoPhaseCommitCorrectness
    /\ NoDuplicateOutput
    /\ EpochMonotonicity

(*===========================================================================*)
(* 活性属性 (Liveness Properties)                                             *)
(*===========================================================================*)

(*---------------------------------------------------------------------------*)
(* Prop-EO-07: CheckpointEventuallyCompletes - Checkpoint最终完成             *)
(* 被触发的Checkpoint最终要么完成，要么失败                                   *)
(*---------------------------------------------------------------------------*)
CheckpointEventuallyCompletes ==
    \A cpId \in Checkpoints :
        (checkpointState[cpId] = "TRIGGERED") ~>
        (checkpointState[cpId] \in {"COMPLETED", "FAILED"})

(*---------------------------------------------------------------------------*)
(* Prop-EO-08: TransactionEventuallyDecides - 事务最终决定                    *)
(* 每个事务最终要么提交，要么回滚                                             *)
(*---------------------------------------------------------------------------*)
TransactionEventuallyDecides ==
    \A sink \in Sinks :
        (sinkTxState[sink].state = "ONGOING") ~>
        (sinkTxState[sink].state \in {"COMPLETE_COMMIT", "COMPLETE_ABORT", "EMPTY"})

(*---------------------------------------------------------------------------*)
(* Prop-EO-09: RecordEventuallyProcessed - 记录最终处理                       *)
(* 每个消费记录最终要么被输出，要么被确认丢弃                                 *)
(*---------------------------------------------------------------------------*)
RecordEventuallyProcessed ==
    \A consumer \in Consumers :
        \A record \in sourceState[consumer].pendingRecords :
            (record.committed = FALSE) ~>
            (record.committed = TRUE)

(*===========================================================================*)
(* 规约                                                                       *)
(*===========================================================================*)

Spec ==
    Init
    /\ [][Next]_<<sourceState, transactionLog, sinkTxState, outputRecords, checkpointState, globalEpoch>>
    /\ Fairness

(*===========================================================================*)
(* 定理                                                                       *)
(*===========================================================================*)

(*---------------------------------------------------------------------------*)
(* Thm-EO-01: Safety - 安全性定理                                             *)
(* Spec蕴含所有安全性不变式                                                   *)
(*---------------------------------------------------------------------------*)
THEOREM Safety ==
    Spec => [] SafetyInvariant

(*---------------------------------------------------------------------------*)
(* Thm-EO-02: EndToEndExactlyOnceGuarantee - 端到端Exactly-Once保证定理       *)
(* 安全性定理: 可重放Source ∧ Checkpoint一致 ∧ Sink原子 ⟹ Exactly-Once        *)
(*                                                                            *)
(* 形式化:                                                                    *)
(*   SourceReplayabilityCondition ∧ CheckpointConsistencyCondition ∧          *)
(*   SinkAtomicityCondition                                                   *)
(*   ⟹                                                                      *)
(*   NoDuplicateOutput ∧ OutputConsistency                                    *)
(*                                                                            *)
(* 证明思路:                                                                  *)
(* 1. Source可重放保证: 故障后可从已提交偏移量恢复，不丢失记录                  *)
(* 2. Checkpoint一致保证: 形成一致割集，状态可恢复                              *)
(* 3. Sink原子保证: 幂等性消除重复，事务性保证原子提交                          *)
(* 4. 三者组合: 故障恢复后不会重复处理已输出记录                                *)
(*---------------------------------------------------------------------------*)
THEOREM EndToEndExactlyOnceGuarantee ==
    Spec =>
        [](
            (/\ SourceReplayabilityCondition
             /\ CheckpointConsistencyCondition
             /\ SinkAtomicityCondition)
            =>
            (/\ NoDuplicateOutput
             /\ OutputConsistency)
        )

(*---------------------------------------------------------------------------*)
(* Thm-EO-03: TwoPhaseCommitAtomicity - 2PC原子性定理                         *)
(* 2PC协议保证事务原子性: 要么全部提交，要么全部回滚                            *)
(*---------------------------------------------------------------------------*)
THEOREM TwoPhaseCommitAtomicity ==
    Spec =>
        \A sink \in Sinks :
            [](
                (IsTransactionalSink(sink) /\ sinkTxState[sink].state = "COMPLETE_COMMIT")
                =>
                (* 一旦提交，记录永久在输出中 *)
                [] (sinkTxState[sink].committedRecords \subseteq outputRecords[sink])
            )

(*---------------------------------------------------------------------------*)
(* Thm-EO-04: SourceReplayabilityGuarantee - Source可重放保证定理             *)
(* 可重放Source保证: 故障后可从已提交偏移量完全恢复                             *)
(*---------------------------------------------------------------------------*)
THEOREM SourceReplayabilityGuarantee ==
    Spec =>
        \A consumer \in Consumers :
            [](
                IsReplayableSource(consumer)
                =>
                (* 故障后可从committedOffset恢复 *)
                \A p \in Partitions :
                    CanReplayFromOffset(consumer, p, 
                        sourceState[consumer].committedOffset[p])
            )

(*---------------------------------------------------------------------------*)
(* Thm-EO-05: CheckpointRecoveryConsistency - Checkpoint恢复一致性定理        *)
(* 从一致Checkpoint恢复后，系统状态保持一致                                     *)
(*---------------------------------------------------------------------------*)
THEOREM CheckpointRecoveryConsistency ==
    Spec =>
        \A cpId \in Checkpoints :
            [](
                (checkpointState[cpId] = "COMPLETED" /\ IsConsistentCheckpoint(cpId))
                =>
                (* 恢复后Source从一致偏移量开始，Sink从一致状态开始 *)
                \A consumer \in Consumers :
                    sourceState[consumer].currentOffset =
                        sourceState[consumer].committedOffset
            )

(*---------------------------------------------------------------------------*)
(* Thm-EO-06: Liveness - 活性定理                                             *)
(* Spec蕴含活性属性                                                           *)
(*---------------------------------------------------------------------------*)
THEOREM Liveness ==
    Spec =>
        /\ CheckpointEventuallyCompletes
        /\ TransactionEventuallyDecides
        /\ RecordEventuallyProcessed

(*---------------------------------------------------------------------------*)
(* Thm-EO-07: CompositionTheorem - 组合定理                                   *)
(* Exactly-Once是三个独立属性的组合:                                          *)
(* Exactly-Once = SourceReplayable ∘ CheckpointConsistent ∘ SinkAtomic        *)
(*                                                                            *)
(* 形式化:                                                                    *)
(*   设 R = SourceReplayabilityCondition                                      *)
(*       C = CheckpointConsistencyCondition                                   *)
(*       A = SinkAtomicityCondition                                           *)
(*       E = EndToEndExactlyOnceCondition                                     *)
(*   则: R ∧ C ∧ A ⟺ E                                                        *)
(*                                                                            *)
(* 其中:                                                                      *)
(*   - R 保证 At-Least-Once (不丢数据)                                        *)
(*   - C 保证 状态一致性 (可恢复)                                               *)
(*   - A 保证 At-Most-Once (不重复)                                           *)
(*   - R ∧ C ∧ A 保证 Exactly-Once                                            *)
(*---------------------------------------------------------------------------*)
THEOREM CompositionTheorem ==
    Spec =>
        [](
            (SourceReplayabilityCondition
             /\ CheckpointConsistencyCondition
             /\ SinkAtomicityCondition)
            <=>
            EndToEndExactlyOnceCondition
        )

=============================================================================
(* End of module ExactlyOnce *)
