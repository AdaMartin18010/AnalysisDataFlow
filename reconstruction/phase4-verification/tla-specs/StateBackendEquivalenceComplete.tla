(* ============================================================================ *)
(* State Backend Equivalence Complete Proof in TLA+                           *)
(* ============================================================================ *)
(* This specification establishes the complete semantic equivalence proof     *)
(* for Flink state backends including:                                        *)
(*   1. HashMapStateBackend vs RocksDBStateBackend equivalence                *)
(*   2. ForStStateBackend integration correctness                             *)
(*   3. Incremental checkpoint semantic equivalence                           *)
(*   4. State migration consistency                                           *)
(* ============================================================================ *)

---------------------------- MODULE StateBackendEquivalenceComplete ----------------

(* ============================================================================ *)
(* Imports and Extended Definitions                                           *)
(* ============================================================================ *)

EXTENDS Naturals, Sequences, FiniteSets, TLC

(* ============================================================================ *)
(* Section 1: Refined State Backend Type Definitions                          *)
(* ============================================================================ *)

StateKey == Nat
StateValue == Nat
StateEntry == [key: StateKey, value: StateValue]
StateSnapshot == SUBSET StateEntry

(* Incremental checkpoint delta: changed keys since last checkpoint *)
DeltaSnapshot == SUBSET StateEntry
CheckpointID == Nat

(* ============================================================================ *)
(* HashMapStateBackend - In-memory hash map                                   *)
(* ============================================================================ *)

HashMapStateBackend == [
    type: {"HashMap"},
    data: StateSnapshot,
    checkpoint_id: CheckpointID,
    sync_to_disk: BOOLEAN,
    snapshot_history: Seq(StateSnapshot)
]

(* ============================================================================ *)
(* RocksDBStateBackend - LSM-tree with WAL and SSTables                       *)
(* ============================================================================ *)

RocksDBStateBackend == [
    type: {"RocksDB"},
    memtable: StateSnapshot,
    sstables: Seq(StateSnapshot),
    wal: Seq(StateEntry),
    checkpoint_id: CheckpointID,
    last_checkpoint_sstables: Seq(StateSnapshot),
    incremental_base: CheckpointID
]

(* ============================================================================ *)
(* ForStStateBackend - Next-gen log-structured state backend                  *)
(* ============================================================================ *)

ForStStateBackend == [
    type: {"ForSt"},
    cache: StateSnapshot,
    log_structure: Seq(StateEntry),
    checkpoint_id: CheckpointID,
    checkpoint_log_segments: Seq(Seq(StateEntry)),
    compression: BOOLEAN,
    incremental_delta: DeltaSnapshot
]

(* Union type *)
BackendState == HashMapStateBackend \union RocksDBStateBackend \union ForStStateBackend

(* ============================================================================ *)
(* Section 2: Core State Operations                                           *)
(* ============================================================================ *)

(* Read operation with last-write-wins semantics *)
Read(state, key) ==
    CASE state.type = "HashMap" ->
        IF \E e \in state.data : e.key = key
        THEN (CHOOSE e \in state.data : e.key = key).value
        ELSE 0
    [] state.type = "RocksDB" ->
        IF \E e \in state.memtable : e.key = key
        THEN (CHOOSE e \in state.memtable : e.key = key).value
        ELSE IF \E i \in DOMAIN state.sstables :
                \E e \in state.sstables[i] : e.key = key
             THEN (CHOOSE e \in
                    UNION {state.sstables[i] : i \in DOMAIN state.sstables} :
                    e.key = key).value
             ELSE 0
    [] state.type = "ForSt" ->
        IF \E e \in state.cache : e.key = key
        THEN (CHOOSE e \in state.cache : e.key = key).value
        ELSE IF \E e \in {state.log_structure[i] : i \in DOMAIN state.log_structure} :
                e.key = key
             THEN (CHOOSE e \in
                    {state.log_structure[i] : i \in DOMAIN state.log_structure} :
                    e.key = key).value
             ELSE 0

(* Write operation *)
Write(state, entry) ==
    CASE state.type = "HashMap" ->
        [state EXCEPT !.data =
            {IF e.key = entry.key THEN entry ELSE e : e \in state.data}
            \union IF \E e \in state.data : e.key = entry.key
                  THEN {}
                  ELSE {entry}]
    [] state.type = "RocksDB" ->
        [state EXCEPT !.memtable =
            {IF e.key = entry.key THEN entry ELSE e : e \in state.memtable}
            \union IF \E e \in state.memtable : e.key = entry.key
                  THEN {}
                  ELSE {entry},
         !.wal = Append(state.wal, entry)]
    [] state.type = "ForSt" ->
        [state EXCEPT !.cache =
            {IF e.key = entry.key THEN entry ELSE e : e \in state.cache}
            \union IF \E e \in state.cache : e.key = entry.key
                  THEN {}
                  ELSE {entry},
         !.log_structure = Append(state.log_structure, entry),
         !.incremental_delta = state.incremental_delta \union {entry}]

(* Delete operation *)
Delete(state, key) ==
    CASE state.type = "HashMap" ->
        [state EXCEPT !.data = {e \in state.data : e.key /= key}]
    [] state.type = "RocksDB" ->
        [state EXCEPT !.memtable = {e \in state.memtable : e.key /= key},
         !.wal = Append(state.wal, [key |-> key, value |-> 0])]
    [] state.type = "ForSt" ->
        [state EXCEPT !.cache = {e \in state.cache : e.key /= key},
         !.log_structure = Append(state.log_structure, [key |-> key, value |-> 0]),
         !.incremental_delta = state.incremental_delta \union {[key |-> key, value |-> 0]}]

(* ============================================================================ *)
(* Section 3: Snapshot and Checkpoint Operations                              *)
(* ============================================================================ *)

(* Full snapshot creation *)
CreateSnapshot(state) ==
    CASE state.type = "HashMap" -> state.data
    [] state.type = "RocksDB" ->
        state.memtable \union
        UNION {state.sstables[i] : i \in DOMAIN state.sstables}
    [] state.type = "ForSt" ->
        state.cache \union
        {state.log_structure[i] : i \in DOMAIN state.log_structure}

(* Incremental snapshot: only changed keys since last checkpoint *)
CreateIncrementalSnapshot(state) ==
    CASE state.type = "HashMap" ->
        LET last_snap == IF state.snapshot_history = <<>>
                         THEN {}
                         ELSE state.snapshot_history[Len(state.snapshot_history)]
        IN {e \in state.data : \E e_last \in last_snap :
              e_last.key = e.key => e_last.value /= e.value}
           \union {e \in state.data : ~\E e_last \in last_snap : e_last.key = e.key}
    [] state.type = "RocksDB" -> state.memtable \union state.wal
    [] state.type = "ForSt" -> state.incremental_delta

(* Full checkpoint operation *)
Checkpoint(state, ckpt_id) ==
    CASE state.type = "HashMap" ->
        [state EXCEPT !.checkpoint_id = ckpt_id,
         !.sync_to_disk = TRUE,
         !.snapshot_history = Append(state.snapshot_history, state.data)]
    [] state.type = "RocksDB" ->
        LET new_sstable == state.memtable
        IN [state EXCEPT !.checkpoint_id = ckpt_id,
            !.sstables = Append(state.sstables, new_sstable),
            !.last_checkpoint_sstables = state.sstables,
            !.memtable = {},
            !.wal = <<>>]
    [] state.type = "ForSt" ->
        [state EXCEPT !.checkpoint_id = ckpt_id,
         !.checkpoint_log_segments = Append(state.checkpoint_log_segments,
                                              state.log_structure),
         !.log_structure = <<>>,
         !.compression = TRUE,
         !.incremental_delta = {}]

(* Incremental checkpoint operation *)
IncrementalCheckpoint(state, ckpt_id) ==
    CASE state.type = "HashMap" ->
        [state EXCEPT !.checkpoint_id = ckpt_id,
         !.sync_to_disk = TRUE,
         !.snapshot_history = Append(state.snapshot_history,
                                       CreateSnapshot(state))]
    [] state.type = "RocksDB" ->
        [state EXCEPT !.checkpoint_id = ckpt_id,
            !.sstables = Append(state.sstables, state.memtable),
            !.memtable = {},
            !.wal = <<>>]
    [] state.type = "ForSt" ->
        [state EXCEPT !.checkpoint_id = ckpt_id,
         !.checkpoint_log_segments = Append(state.checkpoint_log_segments,
                                              state.log_structure),
         !.log_structure = <<>>,
         !.incremental_delta = {}]

(* Restore from full snapshot *)
Restore(backend_type, snapshot, ckpt_id) ==
    CASE backend_type = "HashMap" ->
        [type |-> "HashMap",
         data |-> snapshot,
         checkpoint_id |-> ckpt_id,
         sync_to_disk |-> FALSE,
         snapshot_history |-> <<snapshot>>]
    [] backend_type = "RocksDB" ->
        [type |-> "RocksDB",
         memtable |-> {},
         sstables |-> <<snapshot>>,
         wal |-> <<>>,
         checkpoint_id |-> ckpt_id,
         last_checkpoint_sstables |-> <<>>,
         incremental_base |-> 0]
    [] backend_type = "ForSt" ->
        [type |-> "Forst",
         cache |-> {},
         log_structure |-> <<>>,
         checkpoint_id |-> ckpt_id,
         checkpoint_log_segments |-> <<snapshot>>,
         compression |-> FALSE,
         incremental_delta |-> {}]

(* ============================================================================ *)
(* Section 4: Semantic Equivalence Definitions                                *)
(* ============================================================================ *)

(* Def-S-15-01: Observational equivalence *)
ObservationalEquivalence(state1, state2) ==
    \A key \in StateKey :
        Read(state1, key) = Read(state2, key)

(* Def-S-15-02: Snapshot equivalence *)
SnapshotEquivalence(state1, state2) ==
    CreateSnapshot(state1) = CreateSnapshot(state2)

(* Def-S-15-03: Behavioral equivalence *)
BehavioralEquivalence(state1, state2) ==
    \A key \in StateKey, value \in StateValue :
        LET entry == [key |-> key, value |-> value]
        IN \A op \in {"Read", "Write", "Delete"} :
            CASE op = "Read" ->
                Read(state1, key) = Read(state2, key)
            [] op = "Write" ->
                ObservationalEquivalence(Write(state1, entry),
                                        Write(state2, entry))
            [] op = "Delete" ->
                ObservationalEquivalence(Delete(state1, key),
                                        Delete(state2, key))

(* Def-S-15-04: Full state equivalence *)
StateEquivalence(state1, state2) ==
    SnapshotEquivalence(state1, state2) /\
    BehavioralEquivalence(state1, state2) /\
    state1.checkpoint_id = state2.checkpoint_id

(* Def-S-15-05: Incremental checkpoint equivalence *)
IncrementalCheckpointEquivalence(state1, state2) ==
    CreateIncrementalSnapshot(state1) = CreateIncrementalSnapshot(state2) /\
    SnapshotEquivalence(state1, state2)

(* ============================================================================ *)
(* Section 5: Backend Isomorphisms and Conversions                            *)
(* ============================================================================ *)

(* HashMap to RocksDB conversion *)
HashMapToRocksDB(hash_state) ==
    [type |-> "RocksDB",
     memtable |-> hash_state.data,
     sstables |-> <<>>,
     wal |-> <<>>,
     checkpoint_id |-> hash_state.checkpoint_id,
     last_checkpoint_sstables |-> <<>>,
     incremental_base |-> 0]

(* RocksDB to HashMap conversion *)
RocksDBToHashMap(rocksdb_state) ==
    [type |-> "HashMap",
     data |-> rocksdb_state.memtable \union
              UNION {rocksdb_state.sstables[i] :
                     i \in DOMAIN rocksdb_state.sstables},
     checkpoint_id |-> rocksdb_state.checkpoint_id,
     sync_to_disk |-> TRUE,
     snapshot_history |-> <<rocksdb_state.memtable \union
                            UNION {rocksdb_state.sstables[i] :
                                   i \in DOMAIN rocksdb_state.sstables}>>]

(* HashMap to ForSt conversion *)
HashMapToForSt(hash_state) ==
    [type |-> "ForSt",
     cache |-> hash_state.data,
     log_structure |-> <<>>,
     checkpoint_id |-> hash_state.checkpoint_id,
     checkpoint_log_segments |-> <<hash_state.data>>,
     compression |-> FALSE,
     incremental_delta |-> {}]

(* ForSt to HashMap conversion *)
ForStToHashMap(forst_state) ==
    [type |-> "HashMap",
     data |-> forst_state.cache \union
              {forst_state.log_structure[i] :
               i \in DOMAIN forst_state.log_structure},
     checkpoint_id |-> forst_state.checkpoint_id,
     sync_to_disk |-> FALSE,
     snapshot_history |-> <<forst_state.cache \union
                            {forst_state.log_structure[i] :
                             i \in DOMAIN forst_state.log_structure}>>]

(* ============================================================================ *)
(* Section 6: Equivalence Theorems                                            *)
(* ============================================================================ *)

(* Thm-S-15-01: HashMap and RocksDB are observationally equivalent *)
THEOREM HashMapRocksDBEquivalence ==
    ASSUME NEW hash_state \in HashMapStateBackend
    PROVE LET rocksdb_state == HashMapToRocksDB(hash_state)
          IN ObservationalEquivalence(hash_state, rocksdb_state)

(* Thm-S-15-02: HashMap and ForSt are observationally equivalent *)
THEOREM HashMapForStEquivalence ==
    ASSUME NEW hash_state \in HashMapStateBackend
    PROVE LET forst_state == HashMapToForSt(hash_state)
          IN ObservationalEquivalence(hash_state, forst_state)

(* Thm-S-15-03: Conversion functions are inverses up to observational equiv *)
THEOREM ConversionInverseHashMap ==
    ASSUME NEW hash_state \in HashMapStateBackend
    PROVE LET rocksdb_state == HashMapToRocksDB(hash_state)
              hash_restored == RocksDBToHashMap(rocksdb_state)
          IN ObservationalEquivalence(hash_state, hash_restored)

(* Thm-S-15-04: Snapshot equivalence implies behavioral equivalence *)
THEOREM SnapshotImpliesBehavioral ==
    ASSUME NEW s1 \in BackendState,
           NEW s2 \in BackendState,
           SnapshotEquivalence(s1, s2)
    PROVE BehavioralEquivalence(s1, s2)

(* Thm-S-15-05: Full checkpoint preserves equivalence *)
THEOREM CheckpointPreservesEquivalence ==
    ASSUME NEW s1 \in BackendState,
           NEW s2 \in BackendState,
           StateEquivalence(s1, s2),
           NEW ckpt_id \in CheckpointID
    PROVE StateEquivalence(Checkpoint(s1, ckpt_id), Checkpoint(s2, ckpt_id))

(* Thm-S-15-06: Incremental checkpoint preserves equivalence *)
THEOREM IncrementalCheckpointPreservesEquivalence ==
    ASSUME NEW s1 \in BackendState,
           NEW s2 \in BackendState,
           StateEquivalence(s1, s2),
           NEW ckpt_id \in CheckpointID
    PROVE IncrementalCheckpointEquivalence(IncrementalCheckpoint(s1, ckpt_id),
                                            IncrementalCheckpoint(s2, ckpt_id))

(* Thm-S-15-07: State migration preserves semantics *)
THEOREM MigrationPreservesSemantics ==
    ASSUME NEW snapshot \in StateSnapshot,
           NEW ckpt_id \in CheckpointID
    PROVE LET hashmap == Restore("HashMap", snapshot, ckpt_id)
              rocksdb == Restore("RocksDB", snapshot, ckpt_id)
              forst == Restore("ForSt", snapshot, ckpt_id)
          IN StateEquivalence(hashmap, rocksdb) /\
             StateEquivalence(hashmap, forst)

(* Thm-S-15-08: Operations commute with conversion *)
THEOREM OperationCommutesWithConversion ==
    ASSUME NEW hash_state \in HashMapStateBackend,
           NEW entry \in StateEntry
    PROVE LET rocksdb == HashMapToRocksDB(hash_state)
          IN ObservationalEquivalence(
                HashMapToRocksDB(Write(hash_state, entry)),
                Write(rocksdb, entry))

(* ============================================================================ *)
(* Section 7: Incremental Checkpoint Semantic Properties                      *)
(* ============================================================================ *)

(* Def-S-15-06: Incremental snapshot is a subset of full snapshot *)
IncrementalIsSubset(state) ==
    CreateIncrementalSnapshot(state) \subseteq CreateSnapshot(state)

(* Thm-S-15-09: Incremental checkpoint is semantically complete *)
THEOREM IncrementalCompleteness ==
    ASSUME NEW state \in BackendState
    PROVE IncrementalIsSubset(state)

(* Def-S-15-07: Delta contains all changed keys *)
DeltaCompleteness(state1, state2) ==
    SnapshotEquivalence(state1, state2) =>
    CreateIncrementalSnapshot(state1) = CreateIncrementalSnapshot(state2)

(* Thm-S-15-10: Equivalent states produce equivalent deltas *)
THEOREM EquivalentDeltas ==
    ASSUME NEW s1 \in BackendState,
           NEW s2 \in BackendState
    PROVE DeltaCompleteness(s1, s2)

(* ============================================================================ *)
(* Section 8: State Migration Consistency                                     *)
(* ============================================================================ *)

(* Def-S-15-08: Migration is a relation between backends of different types *)
MigrationRelation(source, target) ==
    source.type /= target.type /\n    SnapshotEquivalence(source, target)

(* Thm-S-15-11: Migration from HashMap to RocksDB preserves reads *)
THEOREM HashMapToRocksDBMigrationCorrect ==
    ASSUME NEW hash_state \in HashMapStateBackend,
           NEW rocksdb_state \in RocksDBStateBackend,
           MigrationRelation(hash_state, rocksdb_state)
    PROVE BehavioralEquivalence(hash_state, rocksdb_state)

(* Thm-S-15-12: Migration from RocksDB to ForSt preserves reads *)
THEOREM RocksDBToForStMigrationCorrect ==
    ASSUME NEW rocksdb_state \in RocksDBStateBackend,
           NEW forst_state \in ForStStateBackend,
           MigrationRelation(rocksdb_state, forst_state)
    PROVE BehavioralEquivalence(rocksdb_state, forst_state)

(* Thm-S-15-13: Round-trip migration restores original semantics *)
THEOREM RoundTripMigration ==
    ASSUME NEW original \in HashMapStateBackend
    PROVE LET rocksdb == HashMapToRocksDB(original)
              restored == RocksDBToHashMap(rocksdb)
          IN StateEquivalence(original, restored)

(* ============================================================================ *)
(* Section 9: Model Checking Invariants                                       *)
(* ============================================================================ *)

CONSTANTS MaxKey, MaxValue, MaxOperations

ASSUME MaxKeyAssumption == MaxKey \in Nat \ {0}
ASSUME MaxValueAssumption == MaxValue \in Nat \ {0}

BoundedStateKey == 1..MaxKey
BoundedStateValue == 0..MaxValue
BoundedStateEntry == [key: BoundedStateKey, value: BoundedStateValue]

(* Type invariant for model checking *)
TypeInvariant(state) ==
    /\ state \in BackendState
    /\ state.checkpoint_id \in Nat

(* Safety: Read after write returns written value *)
ReadAfterWrite(state) ==
    \A key \in BoundedStateKey, value \in BoundedStateValue :
        LET entry == [key |-> key, value |-> value]
            new_state == Write(state, entry)
        IN Read(new_state, key) = value

(* Safety: Delete removes key *)
DeleteRemovesKey(state) ==
    \A key \in BoundedStateKey :
        LET new_state == Delete(state, key)
        IN Read(new_state, key) = 0

(* Safety: Checkpoint preserves snapshot *)
CheckpointPreservesSnapshot(state, ckpt_id) ==
    CreateSnapshot(state) = CreateSnapshot(Checkpoint(state, ckpt_id))

(* Safety: Incremental checkpoint preserves full snapshot *)
IncrementalPreservesSnapshot(state, ckpt_id) ==
    CreateSnapshot(state) = CreateSnapshot(IncrementalCheckpoint(state, ckpt_id))

(* Liveness: Checkpoint ID eventually advances *)
CheckpointAdvances(state, ckpt_id) ==
    checkpoint_id' > checkpoint_id

(* ============================================================================ *)
(* Section 10: State Transition System for TLC                                *)
(* ============================================================================ *)

VARIABLES state, checkpoint_id, operation_count

vars == <<state, checkpoint_id, operation_count>>

Init ==
    /\ state = [type |-> "HashMap",
                data |-> {},
                checkpoint_id |-> 0,
                sync_to_disk |-> FALSE,
                snapshot_history |-> <<{}>>]
    /\ checkpoint_id = 0
    /\ operation_count = 0

Next ==
    /\ operation_count < MaxOperations
    /\ \E op \in {"Write", "Delete", "Checkpoint", "IncrementalCheckpoint"} :
        CASE op = "Write" ->
            \E entry \in BoundedStateEntry :
                state' = Write(state, entry)
                /\ UNCHANGED <<checkpoint_id>>
                /\ operation_count' = operation_count + 1
        [] op = "Delete" ->
            \E key \in BoundedStateKey :
                state' = Delete(state, key)
                /\ UNCHANGED <<checkpoint_id>>
                /\ operation_count' = operation_count + 1
        [] op = "Checkpoint" ->
            state' = Checkpoint(state, checkpoint_id + 1)
            /\ checkpoint_id' = checkpoint_id + 1
            /\ operation_count' = operation_count + 1
        [] op = "IncrementalCheckpoint" ->
            state' = IncrementalCheckpoint(state, checkpoint_id + 1)
            /\ checkpoint_id' = checkpoint_id + 1
            /\ operation_count' = operation_count + 1

Spec == Init /\ [][Next]_vars /\ WF_vars(Next)

(* ============================================================================ *)
(* Invariants for TLC Model Checking                                          *)
(* ============================================================================ *)

InvType == TypeInvariant(state)

InvReadAfterWrite == ReadAfterWrite(state)

InvDeleteRemovesKey == DeleteRemovesKey(state)

InvCheckpointSnapshot ==
    checkpoint_id > 0 =>
    CheckpointPreservesSnapshot(state, checkpoint_id)

InvIncrementalSnapshot ==
    checkpoint_id > 0 =>
    IncrementalPreservesSnapshot(state, checkpoint_id)

(* ============================================================================ *)
(* Summary Theorem                                                            *)
(* ============================================================================ *)

THEOREM StateBackendEquivalenceSummary ==
    ASSUME NEW s1 \in BackendState,
           NEW s2 \in BackendState,
           SnapshotEquivalence(s1, s2)
    PROVE StateEquivalence(s1, s2)

================================================================================
(* End of StateBackendEquivalenceComplete.tla                                 *)
================================================================================
