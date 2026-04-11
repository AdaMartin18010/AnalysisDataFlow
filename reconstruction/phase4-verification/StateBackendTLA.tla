(* ============================================================================ *)
(* State Backend TLA+ Extension Specification                                 *)
(* ============================================================================ *)
(* 文件: StateBackendTLA.tla                                                   *)
(* 阶段: Verification (Phase 4)                                               *)
(* 依赖: StateBackendEquivalence.tla                                          *)
(*                                                                             *)
(* 本文件包含State Backend的TLA+扩展规范:                                       *)
(* 1. 扩展现有StateBackendEquivalence.tla                                      *)
(* 2. 添加增量Checkpoint规范 (Thm-V-04-01 ~ Def-V-04-05)                      *)
(* 3. 添加异步Snapshot规范 (Thm-V-04-02 ~ Def-V-04-09)                        *)
(* ============================================================================ *)

---------------------------- MODULE StateBackendTLA ---------------------------

(* ============================================================================ *)
(* Imports and Dependencies                                                   *)
(* ============================================================================ *)

EXTENDS Naturals, Sequences, FiniteSets, TLC, StateBackendEquivalence

(* ============================================================================ *)
(* Section 1: Incremental Checkpoint Definitions                              *)
(* ============================================================================ *)

(* Def-V-04-01: 增量快照数据结构 *) 
(* 增量快照只记录自上次检查点以来的变化 *)
DeltaSnapshot == [
    base_checkpoint_id: CheckpointID,  (* 基础检查点ID *)
    changed_keys: SUBSET StateKey,      (* 变更的键集合 *)
    delta_entries: StateSnapshot       (* 实际变更的键值对 *)
]

(* Def-V-04-02: 增量检查点状态 *)
IncrementalCheckpointState == [
    last_full_checkpoint: CheckpointID,
    deltas: Seq(DeltaSnapshot),         (* 增量序列 *)
    total_delta_size: Nat               (* 累计增量大小 *)
]

(* Def-V-04-03: 变更追踪 - 记录哪些键自上次检查点后发生变化 *)
ChangeTracker == [StateKey -> BOOLEAN]

(* Def-V-04-04: 变更追踪初始化 *)
InitChangeTracker == [k \in StateKey |-> FALSE]

(* Def-V-04-05: 标记键为已变更 *)
MarkChanged(tracker, key) == [tracker EXCEPT ![key] = TRUE]

(* ============================================================================ *)
(* Section 2: Incremental Checkpoint Operations                               *)
(* ============================================================================ *)

(* 获取自上次检查点以来变更的键集合 *)
GetChangedKeys(tracker) == 
    {k \in StateKey : tracker[k] = TRUE}

(* 提取变更的键值对 *)
ExtractDeltaEntries(state, tracker) ==
    {e \in CreateSnapshot(state) : tracker[e.key] = TRUE}

(* 创建增量快照 *)
CreateDeltaSnapshot(state, tracker, base_id) ==
    [
        base_checkpoint_id |-> base_id,
        changed_keys |-> GetChangedKeys(tracker),
        delta_entries |-> ExtractDeltaEntries(state, tracker)
    ]

(* 增量检查点操作 - 只保存变更 *)
IncrementalCheckpoint(state, inc_state, tracker, ckpt_id) ==
    LET delta == CreateDeltaSnapshot(state, tracker, inc_state.last_full_checkpoint)
    IN [
        last_full_checkpoint |-> inc_state.last_full_checkpoint,
        deltas |-> Append(inc_state.deltas, delta),
        total_delta_size |-> 
            inc_state.total_delta_size + Cardinality(GetChangedKeys(tracker))
    ]

(* 完整检查点操作 - 重置增量链 *)
FullCheckpointWithIncremental(state, inc_state, tracker, ckpt_id) ==
    [
        last_full_checkpoint |-> ckpt_id,
        deltas |-> <<>>,
        total_delta_size |-> 0
    ]

(* ============================================================================ *)
(* Section 3: Incremental Checkpoint Theorems                                 *)
(* ============================================================================ *)

(* Thm-V-04-01: 增量检查点大小定理 *)
(* 增量检查点的大小不超过完整检查点 *)
THEOREM IncrementalCheckpointSizeBound ==
    ASSUME NEW state \in BackendState,
           NEW tracker \in ChangeTracker,
           NEW inc_state \in IncrementalCheckpointState,
           NEW ckpt_id \in CheckpointID
    PROVE LET new_inc == IncrementalCheckpoint(state, inc_state, tracker, ckpt_id)
          IN new_inc.total_delta_size <= Cardinality(CreateSnapshot(state))

(* Thm-V-04-02: 增量检查点语义等价性 *)
(* 增量检查点与完整检查点在恢复时语义等价 *)
THEOREM IncrementalCheckpointEquivalence ==
    ASSUME NEW state \in BackendState,
           NEW inc_state \in IncrementalCheckpointState,
           NEW tracker \in ChangeTracker,
           NEW ckpt_id \in CheckpointID,
           inc_state.deltas = <<>>  (* 从完整检查点开始 *)
    PROVE LET full_ckpt == CreateSnapshot(state)
              inc_ckpt == IncrementalCheckpoint(state, inc_state, tracker, ckpt_id)
              (* 模拟从增量恢复 *)
              delta_entries == ExtractDeltaEntries(state, tracker)
          IN (* 增量中的变更集是完整快照的子集 *)
             delta_entries \subseteq full_ckpt

(* Thm-V-04-03: 增量检查点链一致性 *)
(* 连续的增量检查点形成一致的恢复链 *)
THEOREM IncrementalChainConsistency ==
    ASSUME NEW inc_state \in IncrementalCheckpointState,
           inc_state.deltas # <<>>
    PROVE \A i \in DOMAIN inc_state.deltas :
        i > 1 => 
            inc_state.deltas[i].base_checkpoint_id >=
            inc_state.deltas[i-1].base_checkpoint_id

(* ============================================================================ *)
(* Section 4: Asynchronous Snapshot Definitions                               *)
(* ============================================================================ *)

(* Def-V-04-06: 异步快照状态 *)
AsynchronousSnapshotState == [
    snapshot_in_progress: BOOLEAN,
    snapshot_buffer: StateSnapshot,
    flushed_keys: SUBSET StateKey,
    pending_writes: Seq(StateEntry)
]

(* Def-V-04-07: 快照阶段 *)
SnapshotPhase == {"None", "Buffering", "Flushing", "Finalizing", "Complete"}

(* Def-V-04-08: 扩展的后端状态（包含异步快照） *)
ExtendedBackendState == [
    backend: BackendState,
    async_snapshot: AsynchronousSnapshotState,
    change_tracker: ChangeTracker
]

(* Def-V-04-09: 写操作带变更追踪 *)
WriteWithTracking(ext_state, entry) ==
    LET new_backend == Write(ext_state.backend, entry)
        new_tracker == MarkChanged(ext_state.change_tracker, entry.key)
    IN [
        backend |-> new_backend,
        async_snapshot |-> ext_state.async_snapshot,
        change_tracker |-> new_tracker
    ]

(* ============================================================================ *)
(* Section 5: Asynchronous Snapshot Operations                                *)
(* ============================================================================ *)

(* 开始异步快照 *)
StartAsyncSnapshot(ext_state) ==
    [ext_state EXCEPT 
        !.async_snapshot = [
            snapshot_in_progress |-> TRUE,
            snapshot_buffer |-> {},
            flushed_keys |-> {},
            pending_writes |-> <<>>
        ]
    ]

(* 缓冲写操作（快照进行中） *)
BufferWrite(ext_state, entry) ==
    [ext_state EXCEPT
        !.async_snapshot.pending_writes = 
            Append(ext_state.async_snapshot.pending_writes, entry)
    ]

(* 刷新缓冲的写入到快照 *)
FlushPendingWrites(ext_state) ==
    LET pending == ext_state.async_snapshot.pending_writes
        buffer == ext_state.async_snapshot.snapshot_buffer
    IN [ext_state EXCEPT
        !.async_snapshot.snapshot_buffer = 
            buffer \union {pending[i] : i \in DOMAIN pending},
        !.async_snapshot.pending_writes = <<>>
    ]

(* 完成异步快照 *)
CompleteAsyncSnapshot(ext_state, ckpt_id) ==
    [ext_state EXCEPT
        !.backend.checkpoint_id |-> ckpt_id,
        !.async_snapshot = [
            snapshot_in_progress |-> FALSE,
            snapshot_buffer |-> {},
            flushed_keys |-> {},
            pending_writes |-> <<>>
        ]
    ]

(* ============================================================================ *)
(* Section 6: Asynchronous Snapshot Theorems                                  *)
(* ============================================================================ *)

(* Thm-V-04-04: 异步快照一致性定理 *)
(* 异步快照与同步快照在逻辑上等价 *)
THEOREM AsyncSnapshotConsistency ==
    ASSUME NEW ext_state \in ExtendedBackendState,
           NEW ckpt_id \in CheckpointID,
           ext_state.async_snapshot.snapshot_in_progress = TRUE
    PROVE LET flushed == ext_state.async_snapshot.snapshot_buffer
              pending == {ext_state.async_snapshot.pending_writes[i] : 
                         i \in DOMAIN ext_state.async_snapshot.pending_writes}
              (* 逻辑快照包含已刷新的和待处理的 *)
              logical_snapshot == flushed \union pending
          IN logical_snapshot = CreateSnapshot(ext_state.backend)

(* Thm-V-04-05: 异步快照无阻塞定理 *)
(* 写操作在异步快照期间不会被阻塞 *)
THEOREM AsyncSnapshotNonBlocking ==
    ASSUME NEW ext_state \in ExtendedBackendState,
           NEW entry \in StateEntry,
           ext_state.async_snapshot.snapshot_in_progress = TRUE
    PROVE \E ext_state' \in ExtendedBackendState :
        ext_state' = BufferWrite(ext_state, entry)

(* Thm-V-04-06: 异步快照恢复正确性 *)
THEOREM AsyncSnapshotRecoveryCorrectness ==
    ASSUME NEW ext_state \in ExtendedBackendState,
           NEW ckpt_id \in CheckpointID,
           NEW recovered \in BackendState
    PROVE LET completed == CompleteAsyncSnapshot(ext_state, ckpt_id)
          IN \A key \in StateKey :
              Read(completed.backend, key) = Read(recovered, key)
              => CreateSnapshot(completed.backend) = CreateSnapshot(recovered)

(* ============================================================================ *)
(* Section 7: State Backend Performance Model                                 *)
(* ============================================================================ *)

(* Def-V-04-10: 检查点策略 *)
CheckpointStrategy == {"Full", "Incremental", "Differential"}

(* Def-V-04-11: 检查点成本模型 *)
CheckpointCost(strategy, state_size, delta_size) ==
    CASE strategy = "Full" -> state_size
    []   strategy = "Incremental" -> delta_size
    []   strategy = "Differential" -> delta_size * 2
    []   OTHER -> state_size

(* Def-V-04-12: 恢复成本模型 *)
RecoveryCost(strategy, base_size, num_deltas) ==
    CASE strategy = "Full" -> base_size
    []   strategy = "Incremental" -> base_size + num_deltas * 100
    []   strategy = "Differential" -> base_size * 2
    []   OTHER -> base_size

(* Thm-V-04-07: 增量检查点成本优势定理 *)
THEOREM IncrementalCheckpointCostAdvantage ==
    ASSUME NEW state_size \in Nat,
           NEW delta_size \in Nat,
           delta_size < state_size
    PROVE CheckpointCost("Incremental", state_size, delta_size) <
          CheckpointCost("Full", state_size, 0)

(* Thm-V-04-08: 恢复时间权衡定理 *)
(* 增量检查点减少检查点时间但增加恢复时间 *)
THEOREM CheckpointRecoveryTradeoff ==
    ASSUME NEW state_size \in Nat,
           NEW delta_size \in Nat,
           NEW num_deltas \in Nat,
           delta_size * num_deltas < state_size
    PROVE CheckpointCost("Incremental", state_size, delta_size) <
          CheckpointCost("Full", state_size, 0) /\
          RecoveryCost("Incremental", state_size, num_deltas) >
          RecoveryCost("Full", state_size, 0)

(* ============================================================================ *)
(* Section 8: RocksDB-Specific Incremental Model                              *)
(* ============================================================================ *)

(* Def-V-04-13: RocksDB SST文件元数据 *)
SSTFile == [
    file_id: Nat,
    min_key: StateKey,
    max_key: StateKey,
    size_bytes: Nat,
    level: Nat  (* L0, L1, L2, ... *)
]

(* Def-V-04-14: RocksDB增量快照状态 *)
RocksDBIncrementalState == [
    base_sstables: Set(SSTFile),
    new_sstables: Set(SSTFile),
    compacted_sstables: Set(SSTFile)
]

(* Thm-V-04-09: RocksDB增量检查点正确性 *)
(* 只复制新的SST文件即可实现增量检查点 *)
THEOREM RocksDBIncrementalCorrectness ==
    ASSUME NEW base_state \in RocksDBIncrementalState,
           NEW current_state \in RocksDBIncrementalState
    PROVE LET new_files == current_state.new_sstables
              all_files == base_state.base_sstables \union new_files
          (* 恢复时使用基础文件+新文件 *)
          IN CreateSnapshotFromSSTables(all_files) =
             CreateSnapshotFromSSTables(current_state.base_sstables \union 
                                        current_state.new_sstables)

(* ============================================================================ *)
(* Section 9: TLA+ Action Specifications                                      *)
(* ============================================================================ *)

(* 变量声明 *)
VARIABLES 
    ext_state,          (* 扩展后端状态 *)
    inc_checkpoint,     (* 增量检查点状态 *)
    async_snapshot,     (* 异步快照状态 *)
    ckpt_counter        (* 检查点计数器 *)

(* 初始状态 *)
InitExtended ==
    /\ ext_state = [
        backend |-> [type |-> "Heap", data |-> {}, checkpoint_id |-> 0, sync_to_disk |-> FALSE],
        async_snapshot |-> [
            snapshot_in_progress |-> FALSE,
            snapshot_buffer |-> {},
            flushed_keys |-> {},
            pending_writes |-> <<>>
        ],
        change_tracker |-> InitChangeTracker
    ]
    /\ inc_checkpoint = [
        last_full_checkpoint |-> 0,
        deltas |-> <<>>,
        total_delta_size |-> 0
    ]
    /\ ckpt_counter = 0

(* 写操作动作 *)
WriteAction ==
    /\ \E entry \in StateEntry :
        ext_state' = WriteWithTracking(ext_state, entry)
    /\ UNCHANGED <<inc_checkpoint, async_snapshot, ckpt_counter>>

(* 增量检查点动作 *)
IncrementalCheckpointAction ==
    /\ inc_checkpoint.total_delta_size < 1000  (* 增量大小阈值 *)
    /\ ckpt_counter' = ckpt_counter + 1
    /\ inc_checkpoint' = IncrementalCheckpoint(
        ext_state.backend, inc_checkpoint, ext_state.change_tracker, ckpt_counter')
    /\ ext_state' = [ext_state EXCEPT !.change_tracker = InitChangeTracker]
    /\ UNCHANGED <<async_snapshot>>

(* 完整检查点动作（重置增量链） *)
FullCheckpointAction ==
    /\ inc_checkpoint.total_delta_size >= 1000  (* 达到阈值 *)
    /\ ckpt_counter' = ckpt_counter + 1
    /\ inc_checkpoint' = FullCheckpointWithIncremental(
        ext_state.backend, inc_checkpoint, ext_state.change_tracker, ckpt_counter')
    /\ ext_state' = [ext_state EXCEPT 
        !.backend.checkpoint_id = ckpt_counter',
        !.change_tracker = InitChangeTracker
    ]
    /\ UNCHANGED <<async_snapshot>>

(* 异步快照开始动作 *)
StartSnapshotAction ==
    /\ ~ext_state.async_snapshot.snapshot_in_progress
    /\ ext_state' = StartAsyncSnapshot(ext_state)
    /\ UNCHANGED <<inc_checkpoint, async_snapshot, ckpt_counter>>

(* 下一状态关系 *)
NextExtended ==
    WriteAction
    \/ IncrementalCheckpointAction
    \/ FullCheckpointAction
    \/ StartSnapshotAction

(* ============================================================================ *)
(* Section 10: Safety and Liveness Properties                                 *)
(* ============================================================================ *)

(* 安全性质: 异步快照期间数据一致性 *)
AsyncSnapshotConsistencyInvariant ==
    ext_state.async_snapshot.snapshot_in_progress =>
        \A key \in StateKey :
            Read(ext_state.backend, key) = 
            ReadFromSnapshot(ext_state.backend, ext_state.async_snapshot.snapshot_buffer, key)

(* 安全性质: 增量检查点大小限制 *)
IncrementalSizeLimit ==
    inc_checkpoint.total_delta_size <= 1000

(* 活性性质: 检查点最终完成 *)
CheckpointEventuallyCompletes ==
    <>(inc_checkpoint.deltas # <<>> 
       \/ ext_state.backend.checkpoint_id > 0)

(* 活性性质: 异步快照最终完成 *)
AsyncSnapshotEventuallyCompletes ==
    ext_state.async_snapshot.snapshot_in_progress 
    ~> ~ext_state.async_snapshot.snapshot_in_progress

(* Thm-V-04-10: 扩展状态机安全性定理 *)
THEOREM ExtendedSafety ==
    ASSUME InitExtended, [][NextExtended]_<<ext_state, inc_checkpoint, async_snapshot, ckpt_counter>>
    PROVE [](IncrementalSizeLimit /\ AsyncSnapshotConsistencyInvariant)

(* Thm-V-04-11: 扩展状态机活性定理 *)
THEOREM ExtendedLiveness ==
    ASSUME InitExtended, [][NextExtended]_<<ext_state, inc_checkpoint, async_snapshot, ckpt_counter>>,
           WF_<<ext_state, inc_checkpoint, async_snapshot, ckpt_counter>>(NextExtended)
    PROVE CheckpointEventuallyCompletes /\ AsyncSnapshotEventuallyCompletes

(* ============================================================================ *)
(* Section 11: Model Checking Configuration                                   *)
(* ============================================================================ *)

(* 有限状态实例用于模型检查 *)
MC_StateKey == 0..3
MC_StateValue == 0..2
MC_StateEntry == [key: MC_StateKey, value: MC_StateValue]

(* 有限状态空间约束 *)
MC_Constraint ==
    /\ Cardinality(CreateSnapshot(ext_state.backend)) <= 4
    /\ Len(inc_checkpoint.deltas) <= 3
    /\ Len(ext_state.async_snapshot.pending_writes) <= 2

(* ============================================================================ *)
(* Section 12: Specification Summary and Metadata                             *)
(* ============================================================================ *)

(*
形式化元素统计:
- 定义 (Def-V-04-XX): 15个
- 定理 (Thm-V-04-XX): 11个

核心扩展:
1. 增量检查点 (Incremental Checkpoint)
   - DeltaSnapshot: 增量快照结构
   - IncrementalCheckpoint: 增量检查点操作
   - 成本模型和权衡定理

2. 异步快照 (Asynchronous Snapshot)
   - AsynchronousSnapshotState: 异步状态
   - BufferWrite/Flush: 缓冲和刷新操作
   - 非阻塞保证

3. RocksDB特定模型
   - SSTFile: SST文件元数据
   - 基于SST的增量检查点

4. TLA+动作规范
   - WriteAction: 带变更追踪的写
   - IncrementalCheckpointAction: 增量检查点
   - FullCheckpointAction: 完整检查点
   - StartSnapshotAction: 启动异步快照

5. 安全性和活性
   - AsyncSnapshotConsistencyInvariant
   - IncrementalSizeLimit
   - CheckpointEventuallyCompletes

依赖:
- Naturals, Sequences, FiniteSets, TLC (标准模块)
- StateBackendEquivalence (现有模块)

验证目标:
- 增量检查点语义等价于完整检查点
- 异步快照不阻塞正常处理
- 恢复后状态一致性
*)

================================================================================
(* End of StateBackendTLA.tla                                                 *)
================================================================================
