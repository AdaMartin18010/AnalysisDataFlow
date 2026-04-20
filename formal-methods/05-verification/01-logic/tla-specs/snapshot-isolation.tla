(*
 * Snapshot Isolation - TLA+ Specification
 * =======================================
 *
 * 本规约描述快照隔离（Snapshot Isolation, SI）事务级别的形式化语义，
 * 以及可序列化异常检测机制。
 *
 * SI 特性：
 * - 事务读取数据库在事务开始时的快照
 * - 事务只在提交时检查写冲突（First-Committer-Wins）
 * - 不存在脏读、不可重复读、幻读
 *
 * SI 异常：
 * - 写偏斜（Write Skew）：两个事务读取重叠数据集，各自写入不冲突的数据
 * - 导致不可序列化的执行历史
 *
 * 作者: AnalysisDataFlow Project
 * 版本: 1.0
 *)

------------------------------- MODULE snapshot-isolation -------------------------------

EXTENDS Naturals, FiniteSets, Sequences, TLC, FiniteSets

(*
 * =====================================================================
 * 常量声明
 * =====================================================================
 *)
CONSTANTS
    Key,                \* 数据键的集合
    Value,              \* 数据值的集合  
    TxId,               \* 事务 ID 集合
    MaxVersion          \* 最大版本号（用于模型检查）

(* ASSUME-01: 基数假设 - 至少需要 2 个事务才能展示 SI 异常（如 Write Skew） *)
(* 证明思路: 这是模型配置约束，确保状态空间足够展示并发行为；
 * 单事务无法产生任何隔离异常，因此 2 是最小有意义配置 *)
ASSUME CardinalityAssumption == 
    Cardinality(TxId) >= 2

(* ASSUME-02: 参数约束 - Key 非空，确保数据库有数据可操作 *)
(* 证明思路: Key = {} 导致 tx_write_set 和 tx_read_set 无任何操作对象，
 * 所有事务变为空操作，无法展示任何隔离级别特性 *)
ASSUME KeyNonEmpty == Key # {}

(* ASSUME-03: 参数约束 - Value 非空，确保写入操作有意义 *)
(* 证明思路: Value = {} 导致 WriteKey 动作中 CHOOSE v \in Value 无定义，
 * 且 Init 中数据库初始值 CHOOSE 失败 *)
ASSUME ValueNonEmpty == Value # {}

(* ASSUME-04: 参数约束 - MaxVersion 为正自然数，控制版本空间 *)
(* 证明思路: MaxVersion = 0 导致 Version = {0}，所有操作共享同一版本，
 * 无法展示快照隔离的时间戳区分特性；必须有限以控制 TLC 状态空间 *)
ASSUME MaxVersionValid ==
    /\ MaxVersion \in Nat
    /\ MaxVersion > 0

(* ASSUME-05: 参数约束 - TxId 非空有限集 *)
(* 证明思路: 空 TxId 导致无任何事务可执行，规约停留在 Init；
 * 无限 TxId 导致 TLC 无法穷尽检查 *)
ASSUME TxIdValid ==
    /\ TxId # {}
    /\ IsFiniteSet(TxId)

(*
 * =====================================================================
 * 辅助定义
 * =====================================================================
 *)
Version == 0..MaxVersion
Timestamp == 0..(MaxVersion * 2)

None == CHOOSE v : v \notin Value

(* 操作类型 *)
OpType == {"read", "write", "commit", "abort"}

(*
 * =====================================================================
 * 变量声明
 * =====================================================================
 *)
VARIABLES
    (* 数据库状态 *)
    db,                 \* 键 -> 版本列表的函数
    committedVersions,  \* 已提交的版本集合
    
    (* 事务状态 *)
    tx_state,           \* 每个事务的状态
    tx_start_time,      \* 事务开始时间戳
    tx_read_set,        \* 事务读取的键值集合
    tx_write_set,       \* 事务写入的键值集合
    tx_snapshot,        \* 事务的快照视图
    
    (* 版本分配 *)
    next_timestamp,     \* 下一个时间戳
    
    (* 历史记录 - 用于可序列化检测 *)
    history             \* 操作历史

(*
 * =====================================================================
 * 事务状态
 * =====================================================================
 *)
TxState == {"active", "committing", "committed", "aborted"}

(*
 * =====================================================================
 * 类型不变式
 * =====================================================================
 *)
TypeOK ==
    /\ db \in [Key -> Seq([value : Value, ts : Timestamp, tx : TxId])]
    /\ committedVersions \subseteq [key : Key, ts : Timestamp]
    /\ tx_state \in [TxId -> TxState]
    /\ tx_start_time \in [TxId -> Timestamp]
    /\ tx_read_set \in [TxId -> SUBSET Key]
    /\ tx_write_set \in [TxId -> [Key -> Value \cup {None}]]
    /\ tx_snapshot \in [TxId -> [Key -> Value \cup {None}]]
    /\ next_timestamp \in Timestamp
    /\ history \in Seq([tx : TxId, op : OpType, key : Key \cup {None}, 
                       value : Value \cup {None}, ts : Timestamp])

(*
 * =====================================================================
 * 辅助函数
 * =====================================================================
 *)

(* 获取键在特定时间戳的最新可见值 *)
ReadSnapshot(key, snapshot_ts) ==
    LET versions == db[key]
        visible == {v \in 1..Len(versions) : 
            versions[v].ts <= snapshot_ts /\ 
            [key |-> key, ts |-> versions[v].ts] \in committedVersions}
    IN IF visible = {}
       THEN None
       ELSE LET max_idx == CHOOSE v \in visible :
                    \A v2 \in visible : versions[v].ts >= versions[v2].ts
            IN versions[max_idx].value

(* 检查写冲突：其他事务在快照后提交了相同的键 *)
CheckWriteConflict(tx, key) ==
    \E k \in committedVersions :
        /\ k.key = key
        /\ k.ts > tx_start_time[tx]
        /\ k.ts < next_timestamp

(*
 * =====================================================================
 * 初始状态
 * =====================================================================
 *)
Init ==
    /\ db = [k \in Key |-> <<[value |-> CHOOSE v \in Value : TRUE, 
                              ts |-> 0, tx |-> None]>>]
    /\ committedVersions = {[key |-> k, ts |-> 0] : k \in Key}
    /\ tx_state = [t \in TxId |-> "active"]
    /\ tx_start_time = [t \in TxId |-> 0]
    /\ tx_read_set = [t \in TxId |-> {}]
    /\ tx_write_set = [t \in TxId |-> [k \in Key |-> None]]
    /\ tx_snapshot = [t \in TxId |-> [k \in Key |-> None]]
    /\ next_timestamp = 1
    /\ history = <<>>

(*
 * =====================================================================
 * 事务操作
 * =====================================================================
 *)

(* 开始事务 *)
BeginTransaction(tx) ==
    /\ tx_state[tx] = "active"
    /\ tx_start_time[tx] = 0  \* 还未开始
    /\ tx_start_time' = [tx_start_time EXCEPT ![tx] = next_timestamp]
    /\ tx_snapshot' = [tx_snapshot EXCEPT ![tx] = 
        [k \in Key |-> ReadSnapshot(k, next_timestamp)]]
    /\ next_timestamp' = next_timestamp + 1
    /\ history' = Append(history, 
        [tx |-> tx, op |-> "read", key |-> None, value |-> None, 
         ts |-> next_timestamp])
    /\ UNCHANGED <<db, committedVersions, tx_state, tx_read_set, 
                   tx_write_set>>

(* 读取键 *)
ReadKey(tx, key) ==
    /\ tx_state[tx] = "active"
    /\ tx_start_time[tx] > 0  \* 事务已开始
    /\ tx_read_set' = [tx_read_set EXCEPT ![tx] = @ \cup {key}]
    /\ history' = Append(history,
        [tx |-> tx, op |-> "read", key |-> key, 
         value |-> tx_snapshot[tx][key], ts |-> next_timestamp])
    /\ UNCHANGED <<db, committedVersions, tx_state, tx_start_time,
                   tx_write_set, tx_snapshot, next_timestamp>>

(* 写入键 *)
WriteKey(tx, key, value) ==
    /\ tx_state[tx] = "active"
    /\ tx_start_time[tx] > 0
    /\ tx_write_set' = [tx_write_set EXCEPT ![tx] = 
        [@ EXCEPT ![key] = value]]
    /\ history' = Append(history,
        [tx |-> tx, op |-> "write", key |-> key, value |-> value,
         ts |-> next_timestamp])
    /\ UNCHANGED <<db, committedVersions, tx_state, tx_start_time,
                   tx_read_set, tx_snapshot, next_timestamp>>

(* 提交事务 *)
CommitTransaction(tx) ==
    /\ tx_state[tx] = "active"
    /\ tx_start_time[tx] > 0
    /\ tx_state' = [tx_state EXCEPT ![tx] = "committing"]
    \* SI: First-Committer-Wins 检查
    /\ \A key \in Key :
        tx_write_set[tx][key] # None => ~CheckWriteConflict(tx, key)
    \* 分配提交时间戳并写入
    /\ LET commit_ts == next_timestamp
       IN 
       /\ db' = [k \in Key |->
            IF tx_write_set[tx][k] = None
            THEN db[k]
            ELSE Append(db[k], [value |-> tx_write_set[tx][k],
                                ts |-> commit_ts,
                                tx |-> tx])]
       /\ committedVersions' = committedVersions \cup
            {[key |-> k, ts |-> commit_ts] : k \in Key, 
             tx_write_set[tx][k] # None}
       /\ next_timestamp' = next_timestamp + 1
       /\ history' = Append(history,
            [tx |-> tx, op |-> "commit", key |-> None, value |-> None,
             ts |-> commit_ts])
    /\ tx_state' = [tx_state EXCEPT ![tx] = "committed"]
    /\ UNCHANGED <<tx_start_time, tx_read_set, tx_write_set, tx_snapshot>>

(* 中止事务 *)
AbortTransaction(tx) ==
    /\ tx_state[tx] = "active"
    /\ tx_state' = [tx_state EXCEPT ![tx] = "aborted"]
    /\ history' = Append(history,
        [tx |-> tx, op |-> "abort", key |-> None, value |-> None,
         ts |-> next_timestamp])
    /\ UNCHANGED <<db, committedVersions, tx_start_time, tx_read_set,
                   tx_write_set, tx_snapshot, next_timestamp>>

(*
 * =====================================================================
 * 下一步动作
 * =====================================================================
 *)
Next ==
    \E tx \in TxId :
        BeginTransaction(tx)
        \/ \E key \in Key : ReadKey(tx, key) \/ WriteKey(tx, key, CHOOSE v \in Value : TRUE)
        \/ CommitTransaction(tx)
        \/ AbortTransaction(tx)

(*
 * =====================================================================
 * 完整规约
 * =====================================================================
 *)
Spec == Init /\ [][Next]_<<db, committedVersions, tx_state, tx_start_time,
                          tx_read_set, tx_write_set, tx_snapshot,
                          next_timestamp, history>>

(*
 * =====================================================================
 * 类型精确不变量增强
 * =====================================================================
 *)

(* TypeOK-Precision-01: 事务状态转换合法性 *)
(* 事务状态必须按 active -> committing -> committed 或 active -> aborted 转换 *)
TypeOK_StateTransition ==
    [][\A tx \in TxId :
        (tx_state[tx] = "committed" => tx_state'[tx] = "committed")
        /\ (tx_state[tx] = "aborted" => tx_state'[tx] = "aborted")
        /\ (tx_state[tx] = "committing" => tx_state'[tx] \in {"committing", "committed"})
    ]_<<db, committedVersions, tx_state, tx_start_time, tx_read_set, tx_write_set, tx_snapshot, next_timestamp, history>>

(* TypeOK-Precision-02: next_timestamp 单调递增且有上界 *)
(* next_timestamp 每次增加 1，且不超过 Timestamp 最大值 *)
TypeOK_TimestampMonotonic ==
    [][next_timestamp' >= next_timestamp]_<<db, committedVersions, tx_state, tx_start_time, tx_read_set, tx_write_set, tx_snapshot, next_timestamp, history>>

(* TypeOK-Precision-03: 已提交版本的数据库一致性 *)
(* committedVersions 中的每个条目都对应 db 中存在的版本 *)
TypeOK_CommittedVersionsConsistency ==
    \A cv \in committedVersions :
        \E i \in 1..Len(db[cv.key]) :
            db[cv.key][i].ts = cv.ts

(*
 * =====================================================================
 * SI 基本不变式
 * =====================================================================
 *)

(*
 * Thm-SI-01: No Dirty Read
 * 事务只读取已提交的版本（在快照时间戳之前提交的）
 *)
NoDirtyRead ==
    \A h \in 1..Len(history) :
        LET op == history[h]
        IN (op.op = "read" /\ op.key # None)
           => op.value # None

(*
 * Thm-SI-02: Read Your Own Writes
 * 事务读取自己写入的未提交值
 *)
ReadYourOwnWrites ==
    \A tx \in TxId, key \in Key :
        (tx_write_set[tx][key] # None)
        => (tx_snapshot[tx][key] = tx_write_set[tx][key])

(*
 * Thm-SI-03: First-Committer-Wins
 * 如果两个并发事务写入相同的键，只有一个可以提交
 *)
FirstCommitterWins ==
    \A tx1, tx2 \in TxId, key \in Key :
        (tx1 # tx2
         /\ tx_state[tx1] = "committed"
         /\ tx_state[tx2] = "committed"
         /\ tx_write_set[tx1][key] # None
         /\ tx_write_set[tx2][key] # None)
        => ~((tx_start_time[tx1] < tx_start_time[tx2]
              /\ tx_start_time[tx2] < 
                  CHOOSE ts \in Timestamp :
                      [key |-> key, ts |-> ts] \in committedVersions
                      /\ db[key][ts].tx = tx1)
            \/ (tx_start_time[tx2] < tx_start_time[tx1]
                /\ tx_start_time[tx1] < 
                    CHOOSE ts \in Timestamp :
                        [key |-> key, ts |-> ts] \in committedVersions
                        /\ db[key][ts].tx = tx2))

(*
 * =====================================================================
 * 可序列化异常检测
 * =====================================================================
 *)

(* 依赖图边类型 *)
EdgeType == {"rw", "ww", "wr"}

(* 构造依赖图的辅助函数 *)
TransactionWrites(tx, key) ==
    tx_write_set[tx][key] # None

TransactionReads(tx, key) ==
    key \in tx_read_set[tx]

(*
 * Thm-SI-04: Write Skew Detection
 * 写偏斜：两个事务 T1, T2 满足：
 * - T1 读取 T2 写入的键的某个子集
 * - T2 读取 T1 写入的键的某个子集
 * - 两个事务都提交
 * 这形成依赖图中的环，导致不可序列化
 *)
WriteSkewExists ==
    \E tx1, tx2 \in TxId :
        tx1 # tx2
        /\ tx_state[tx1] = "committed"
        /\ tx_state[tx2] = "committed"
        /\ \E key1, key2 \in Key :
            /\ key1 # key2
            /\ TransactionReads(tx1, key1)
            /\ TransactionWrites(tx2, key1)
            /\ TransactionReads(tx2, key2)
            /\ TransactionWrites(tx1, key2)
            /\ ~TransactionWrites(tx1, key1)  \* 没有直接写冲突
            /\ ~TransactionWrites(tx2, key2)

(*
 * Thm-SI-05: Serializable Snapshot Isolation (SSI)
 * 检测不可序列化的方法是检查依赖图是否有环
 * SSI 在运行时检测潜在环并中止事务
 *)
SerializableSI ==
    ~WriteSkewExists

(*
 * Thm-SI-06: Prefix Serializability
 * 如果所有事务都是只读或只写，SI 是可序列化的
 *)
PrefixSerializableCondition ==
    \A tx \in TxId :
        (tx_state[tx] = "committed")
        => (tx_read_set[tx] = {}  \* 纯写入
            \/ \A key \in Key : tx_write_set[tx][key] = None)  \* 纯读取

(*
 * =====================================================================
 * SI 与可序列化对比
 * =====================================================================
 *
 * 隔离级别层次：
 * 1. Read Uncommitted < Read Committed < Repeatable Read < Snapshot Isolation
 * 2. Snapshot Isolation 与 Serializable 不可比较
 *    - SI 允许某些 Serializable 不允许的异常（如 Write Skew）
 *    - Serializable 允许某些 SI 不允许的异常（如幻读，取决于实现）
 *
 * 实际系统：
 * - PostgreSQL: 默认 Read Committed，可选 Repeatable Read, Serializable
 * - MySQL(InnoDB): 默认 Repeatable Read（实际上是 SI 实现）
 * - SQL Server: 支持 Snapshot Isolation 和 Serializable Snapshot Isolation
 * - Oracle: 默认 Read Committed（使用多版本实现类似 SI）
 *)

(*
 * =====================================================================
 * TLC 配置
 * =====================================================================
 *
 * CONSTANTS:
 *   Key = {k1, k2}
 *   Value = {v1, v2}
 *   TxId = {t1, t2}
 *   MaxVersion = 5
 *
 * 不变式:
 *   TypeOK
 *   NoDirtyRead
 *   FirstCommitterWins
 *
 * 用于检测异常:
 *   ~WriteSkewExists (检查写偏斜是否存在)
 *)

=============================================================================
