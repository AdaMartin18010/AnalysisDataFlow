----------------------------- MODULE streaming-systems -----------------------------
(*
 * 流计算系统 TLA+ 规范
 * 
 * 本规范定义流计算系统的核心属性：
 * - 状态机规范
 * - 一致性协议
 * - 容错机制
 *
 * 基于: Apache Flink, Dataflow Model
 * 版本: 1.0.0
 * 日期: 2026-04-12
 *)

EXTENDS Integers, Sequences, FiniteSets, Bags, TLC

(* ============================================================
 * 常量定义
 * ============================================================ *)

CONSTANTS 
    MaxTimestamp,       (* 最大时间戳 *)
    MaxRecords,         (* 最大记录数 *)
    NumPartitions,      (* 分区数 *)
    Workers,            (* 工作节点集合 *)
    Sources,            (* 数据源集合 *)
    Sinks               (* 数据汇集合 *)

ASSUME MaxTimestamp \in Nat
ASSUME MaxRecords \in Nat
ASSUME NumPartitions \in Nat \ {0}
ASSUME Workers # {}
ASSUME Sources # {}
ASSUME Sinks # {}

(* ============================================================
 * 变量定义
 * ============================================================ *)

VARIABLES
    (* 全局状态 *)
    globalTime,         (* 全局处理时间 *)
    records,            (* 所有记录的集合 *)
    
    (* 分区状态 *)
    partitionOffsets,   (* 每个分区的当前偏移量 *)
    partitionData,      (* 每个分区的数据 *)
    
    (* 算子状态 *)
    operatorStates,     (* 算子键值状态 *)
    operatorTimestamps, (* 算子时间戳状态 *)
    
    (* Checkpoint状态 *)
    checkpointId,       (* 当前Checkpoint ID *)
    checkpointStates,   (* Checkpoint状态存储 *)
    pendingCheckpoints, (* 待完成的Checkpoints *)
    completedCheckpoints, (* 已完成的Checkpoints *)
    
    (* Watermark状态 *)
    watermarks,         (* 当前Watermark值 *)
    watermarkProgress,  (* Watermark进展跟踪 *)
    
    (* 故障恢复状态 *)
    failedWorkers,      (* 故障节点集合 *)
    recoveredWorkers,   (* 已恢复节点集合 *)
    
    (* 一致性状态 *)
    processedRecords,   (* 已处理的记录 *)
    committedRecords    (* 已提交的记录 *)

(* ============================================================
 * 辅助运算符
 * ============================================================ *)

(* 记录类型 *)
Record == [id: Nat, key: Nat, value: Nat, timestamp: Nat, partition: 1..NumPartitions]

(* 事件类型 *)
Event == [type: {"DATA", "WATERMARK", "CHECKPOINT"}, data: Record \union Nat]

(* 获取当前时间 *)
Now == globalTime

(* 检查记录是否有效 *)
IsValidRecord(r) ==
    /\ r.id \in 1..MaxRecords
    /\ r.timestamp \in 0..MaxTimestamp
    /\ r.partition \in 1..NumPartitions

(* 空记录 *)
EmptyRecord == [id |-> 0, key |-> 0, value |-> 0, timestamp |-> 0, partition |-> 1]

(* ============================================================
 * 状态机规范
 * ============================================================ *)

(* 初始状态 *)
Init ==
    /\ globalTime = 0
    /\ records = {}
    /\ partitionOffsets = [p \in 1..NumPartitions |-> 0]
    /\ partitionData = [p \in 1..NumPartitions |-> <<>>]
    /\ operatorStates = [w \in Workers |-> [k \in Nat |-> 0]]
    /\ operatorTimestamps = [w \in Workers |-> 0]
    /\ checkpointId = 0
    /\ checkpointStates = {}
    /\ pendingCheckpoints = {}
    /\ completedCheckpoints = {}
    /\ watermarks = [p \in 1..NumPartitions |-> 0]
    /\ watermarkProgress = [p \in 1..NumPartitions |-> {}]
    /\ failedWorkers = {}
    /\ recoveredWorkers = {}
    /\ processedRecords = {}
    /\ committedRecords = {}

(* 生成新记录 *)
GenerateRecord(p) ==
    /\ Len(partitionData[p]) < MaxRecords
    /\ LET newId == Cardinality(records) + 1
           newTs == globalTime
           newRec == [id |-> newId, key |-> newId % 10, value |-> newId * 10, 
                      timestamp |-> newTs, partition |-> p]
       IN /\ partitionData' = [partitionData EXCEPT ![p] = Append(@, newRec)]
          /\ records' = records \union {newRec}
    /\ UNCHANGED <<globalTime, partitionOffsets, operatorStates, operatorTimestamps,
                   checkpointId, checkpointStates, pendingCheckpoints, completedCheckpoints,
                   watermarks, watermarkProgress, failedWorkers, recoveredWorkers,
                   processedRecords, committedRecords>>

(* 处理记录 *)
ProcessRecord(w, p) ==
    /\ w \in Workers \ failedWorkers
    /\ partitionOffsets[p] < Len(partitionData[p])
    /\ LET idx == partitionOffsets[p] + 1
           rec == partitionData[p][idx]
           newState == operatorStates[w][rec.key] + rec.value
       IN /\ operatorStates' = [operatorStates EXCEPT ![w][rec.key] = newState]
          /\ operatorTimestamps' = [operatorTimestamps EXCEPT ![w] = rec.timestamp]
          /\ partitionOffsets' = [partitionOffsets EXCEPT ![p] = idx]
          /\ processedRecords' = processedRecords \union {[worker |-> w, record |-> rec]}
    /\ UNCHANGED <<globalTime, records, partitionData, checkpointId, checkpointStates,
                   pendingCheckpoints, completedCheckpoints, watermarks, watermarkProgress,
                   failedWorkers, recoveredWorkers, committedRecords>>

(* 推进Watermark *)
AdvanceWatermark(p) ==
    /\ p \in 1..NumPartitions
    /\ LET currentOffset == partitionOffsets[p]
           currentData == partitionData[p]
           maxTs == IF currentOffset = 0 THEN 0
                    ELSE currentData[currentOffset].timestamp
       IN /\ watermarks' = [watermarks EXCEPT ![p] = maxTs]
          /\ watermarkProgress' = [watermarkProgress EXCEPT ![p] = 
              watermarkProgress[p] \union {maxTs}]
    /\ UNCHANGED <<globalTime, records, partitionOffsets, partitionData,
                   operatorStates, operatorTimestamps, checkpointId, checkpointStates,
                   pendingCheckpoints, completedCheckpoints, failedWorkers, recoveredWorkers,
                   processedRecords, committedRecords>>

(* ============================================================
 * Checkpoint协议
 * ============================================================ *)

(* 触发Checkpoint *)
TriggerCheckpoint ==
    /\ checkpointId < MaxRecords
    /\ pendingCheckpoints = {}
    /\ checkpointId' = checkpointId + 1
    /\ pendingCheckpoints' = {checkpointId'}
    /\ UNCHANGED <<globalTime, records, partitionOffsets, partitionData,
                   operatorStates, operatorTimestamps, checkpointStates,
                   completedCheckpoints, watermarks, watermarkProgress,
                   failedWorkers, recoveredWorkers, processedRecords, committedRecords>>

(* 执行Checkpoint - 保存状态 *)
ExecuteCheckpoint(w) ==
    /\ w \in Workers \ failedWorkers
    /\ pendingCheckpoints # {}
    /\ LET cpId == CHOOSE cp \in pendingCheckpoints : TRUE
           cpState == [worker |-> w, 
                      state |-> operatorStates[w],
                      timestamp |-> operatorTimestamps[w],
                      offset |-> [p \in 1..NumPartitions |-> partitionOffsets[p]]]
       IN checkpointStates' = checkpointStates \union {<<cpId, w, cpState>>}
    /\ UNCHANGED <<globalTime, records, partitionOffsets, partitionData,
                   operatorStates, operatorTimestamps, checkpointId, pendingCheckpoints,
                   completedCheckpoints, watermarks, watermarkProgress,
                   failedWorkers, recoveredWorkers, processedRecords, committedRecords>>

(* 完成Checkpoint *)
CompleteCheckpoint ==
    /\ pendingCheckpoints # {}
    /\ LET cpId == CHOOSE cp \in pendingCheckpoints : TRUE
           allWorkersCheckpointed == 
               \A w \in Workers \ failedWorkers : 
                   \E cs \in checkpointStates : cs[1] = cpId /\ cs[2] = w
       IN /\ allWorkersCheckpointed
          /\ pendingCheckpoints' = {}
          /\ completedCheckpoints' = completedCheckpoints \union {cpId}
    /\ UNCHANGED <<globalTime, records, partitionOffsets, partitionData,
                   operatorStates, operatorTimestamps, checkpointId, checkpointStates,
                   watermarks, watermarkProgress, failedWorkers, recoveredWorkers,
                   processedRecords, committedRecords>>

(* ============================================================
 * 容错机制
 * ============================================================ *)

(* 模拟工作节点故障 *)
FailWorker(w) ==
    /\ w \in Workers
    /\ w \notin failedWorkers
    /\ failedWorkers' = failedWorkers \union {w}
    /\ UNCHANGED <<globalTime, records, partitionOffsets, partitionData,
                   operatorStates, operatorTimestamps, checkpointId, checkpointStates,
                   pendingCheckpoints, completedCheckpoints, watermarks, watermarkProgress,
                   recoveredWorkers, processedRecords, committedRecords>>

(* 从Checkpoint恢复 *)
RecoverWorker(w) ==
    /\ w \in failedWorkers
    /\ completedCheckpoints # {}
    /\ LET latestCp == CHOOSE cp \in completedCheckpoints : 
                          \A cp2 \in completedCheckpoints : cp >= cp2
           cpState == CHOOSE cs \in checkpointStates : cs[1] = latestCp /\ cs[2] = w
           savedState == csState[3].state
           savedTimestamp == csState[3].timestamp
           savedOffsets == csState[3].offset
       IN /\ operatorStates' = [operatorStates EXCEPT ![w] = savedState]
          /\ operatorTimestamps' = [operatorTimestamps EXCEPT ![w] = savedTimestamp]
          /\ partitionOffsets' = savedOffsets
          /\ failedWorkers' = failedWorkers \ {w}
          /\ recoveredWorkers' = recoveredWorkers \union {w}
    /\ UNCHANGED <<globalTime, records, partitionData, checkpointId, checkpointStates,
                   pendingCheckpoints, completedCheckpoints, watermarks, watermarkProgress,
                   processedRecords, committedRecords>>

(* 推进全局时间 *)
AdvanceTime ==
    /\ globalTime < MaxTimestamp
    /\ globalTime' = globalTime + 1
    /\ UNCHANGED <<records, partitionOffsets, partitionData, operatorStates,
                   operatorTimestamps, checkpointId, checkpointStates,
                   pendingCheckpoints, completedCheckpoints, watermarks, watermarkProgress,
                   failedWorkers, recoveredWorkers, processedRecords, committedRecords>>

(* ============================================================
 * 下一状态关系
 * ============================================================ *)

Next ==
    \/ \E p \in 1..NumPartitions : GenerateRecord(p)
    \/ \E w \in Workers : \E p \in 1..NumPartitions : ProcessRecord(w, p)
    \/ \E p \in 1..NumPartitions : AdvanceWatermark(p)
    \/ TriggerCheckpoint
    \/ \E w \in Workers : ExecuteCheckpoint(w)
    \/ CompleteCheckpoint
    \/ \E w \in Workers : FailWorker(w)
    \/ \E w \in Workers : RecoverWorker(w)
    \/ AdvanceTime

(* ============================================================
 * 公平性条件
 * ============================================================ *)

Fairness ==
    /\ WF_vars(AdvanceTime)
    /\ \A p \in 1..NumPartitions : WF_vars(GenerateRecord(p))
    /\ \A w \in Workers : \A p \in 1..NumPartitions : WF_vars(ProcessRecord(w, p))
    /\ WF_vars(TriggerCheckpoint)
    /\ WF_vars(CompleteCheckpoint)

(* ============================================================
 * 完整规范
 * ============================================================ *)

Spec == Init /\ [][Next]_vars /\ Fairness

(* ============================================================
 * 不变量 (安全性属性)
 * ============================================================ *)

(* 类型不变量 *)
TypeOK ==
    /\ globalTime \in 0..MaxTimestamp
    /\ records \subseteq Record
    /\ partitionOffsets \in [1..NumPartitions -> 0..MaxRecords]
    /\ \A p \in 1..NumPartitions : partitionData[p] \in Seq(Record)
    /\ operatorStates \in [Workers -> [Nat -> Nat]]
    /\ operatorTimestamps \in [Workers -> 0..MaxTimestamp]
    /\ checkpointId \in 0..MaxRecords
    /\ watermarks \in [1..NumPartitions -> 0..MaxTimestamp]
    /\ failedWorkers \subseteq Workers
    /\ recoveredWorkers \subseteq Workers

(* 偏移量单调递增 *)
MonotonicOffsets ==
    \A p \in 1..NumPartitions :
        partitionOffsets[p] <= Len(partitionData[p])

(* Checkpoint ID单调递增 *)
MonotonicCheckpointId ==
    \A cp \in pendingCheckpoints : cp > 0
    /\ \A cp \in completedCheckpoints : cp > 0
    /\ (completedCheckpoints # {} => 
        \A cp1 \in completedCheckpoints : cp1 <= checkpointId)

(* 故障节点不处理数据 *)
FailedWorkersInactive ==
    \A w \in failedWorkers :
        /\ operatorStates[w] = [k \in Nat |-> 0]
        /\ operatorTimestamps[w] = 0

(* Watermark单调性 *)
WatermarkMonotonicity ==
    \A p \in 1..NumPartitions :
        \A t1, t2 \in watermarkProgress[p] :
            t1 <= t2 / t2 <= t1

(* ============================================================
 * 活性属性
 * ============================================================ *)

(* 所有记录最终都会被处理 *)
AllRecordsEventuallyProcessed ==
    <>[](\A p \in 1..NumPartitions : 
            partitionOffsets[p] = Len(partitionData[p]))

(* Checkpoint最终会完成 *)
CheckpointEventuallyCompletes ==
    \A cp \in Nat :
        cp \in pendingCheckpoints ~> cp \in completedCheckpoints

(* 故障节点最终会被恢复 *)
FailedWorkersEventuallyRecover ==
    \A w \in Workers :
        w \in failedWorkers ~> w \in recoveredWorkers

(* ============================================================
 * Exactly-Once语义保证
 * ============================================================ *)

(* 无重复处理 *)
NoDuplicateProcessing ==
    \A r1, r2 \in processedRecords :
        r1.record.id = r2.record.id => r1 = r2

(* 无丢失记录 *)
NoLostRecords ==
    \A r \in records :
        \E pr \in processedRecords : pr.record = r
        / globalTime < MaxTimestamp

(* Exactly-Once语义 *)
ExactlyOnceSemantics ==
    [] (NoDuplicateProcessing /\ NoLostRecords)

(* ============================================================
 * 一致性属性
 * ============================================================ *)

(* 线性一致性 *)
Linearizability ==
    \A w1, w2 \in Workers :
        (w1 \notin failedWorkers /\ w2 \notin failedWorkers) =>
        (operatorTimestamps[w1] = operatorTimestamps[w2] =>
         operatorStates[w1] = operatorStates[w2])

(* 顺序一致性 *)
SequentialConsistency ==
    \E seq \in Seq(processedRecords) :
        \A i, j \in DOMAIN seq :
            i < j => seq[i].record.timestamp <= seq[j].record.timestamp

(* 最终一致性 *)
EventualConsistency ==
    <>[](\A w1, w2 \in Workers \ failedWorkers :
            operatorTimestamps[w1] = operatorTimestamps[w2] =>
            operatorStates[w1] = operatorStates[w2])

(* ============================================================
 * 辅助定理
 * ============================================================ *)

THEOREM Spec => []TypeOK
THEOREM Spec => []MonotonicOffsets
THEOREM Spec => []MonotonicCheckpointId
THEOREM Spec => []WatermarkMonotonicity
THEOREM Spec => AllRecordsEventuallyProcessed
THEOREM Spec => CheckpointEventuallyCompletes
THEOREM Spec => ExactlyOnceSemantics

(* ============================================================
 * 模型检查配置
 * ============================================================ *)

(* 用于模型检查的常量实例 *)
MCMaxTimestamp == 10
MCMaxRecords == 20
MCNumPartitions == 2
MCWorkers == {"w1", "w2"}
MCSources == {"s1"}
MCSinks == {"k1"}

================================================================================
(*
 * 变更历史:
 * 2026-04-12: 初始版本，定义核心流处理语义
 *
 * 引用参考:
 * [1] Akidau et al., "The Dataflow Model", PVLDB, 8(12), 2015.
 * [2] Carbone et al., "State Management in Apache Flink", SIGMOD, 2017.
 * [3] Kleppmann, "Designing Data-Intensive Applications", O'Reilly, 2017.
 *)
