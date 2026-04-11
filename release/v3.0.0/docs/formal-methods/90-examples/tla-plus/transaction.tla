(* ============================================================================
 * TLA+ 规约: 事务隔离级别 (Transaction Isolation Levels)
 * ============================================================================
 *
 * 本规约描述数据库事务的不同隔离级别及其异常现象。
 *
 * ANSI SQL 隔离级别:
 * - READ UNCOMMITTED: 允许脏读
 * - READ COMMITTED:   防止脏读
 * - REPEATABLE READ:  防止脏读、不可重复读
 * - SERIALIZABLE:     完全可串行化
 *
 * 常见异常:
 * - Dirty Read (脏读): 读取未提交的数据
 * - Non-repeatable Read (不可重复读): 两次读取结果不同
 * - Phantom Read (幻读): 两次范围查询结果不同
 * - Lost Update (丢失更新): 并发更新覆盖
 * - Write Skew (写偏斜): 基于过时读写的更新
 *
 * 参考: Adya et al. (2000). Generalized Isolation Level Definitions
 * ============================================================================ *)

------------------------------ MODULE Transaction -----------------------------

(* ----------------------------------------------------------------------------
 * 常量定义
 * ---------------------------------------------------------------------------- *)

CONSTANTS
    Transaction,        (* 事务集合 *)
    Key,                (* 数据键集合 *)
    Value,              (* 数据值集合 *)
    
    (* 隔离级别 *)
    READ_UNCOMMITTED,
    READ_COMMITTED,
    REPEATABLE_READ,
    SERIALIZABLE

ASSUME
    /\ Transaction # {}
    /\ Key # {}
    /\ Value # {}

(* ----------------------------------------------------------------------------
 * 变量定义
 * ---------------------------------------------------------------------------- *)

VARIABLES
    (* 数据库状态 *)
    db,                 (* Key -> Value, 已提交的数据 *)
    isolationLevel,     (* Transaction -> IsolationLevel *)
    
    (* 事务状态 *)
    txStatus,           (* Transaction -> {"active", "committed", "aborted"} *)
    txStartTime,        (* Transaction -> Nat, 开始时间戳 *)
    txReadSet,          (* Transaction -> SUBSET (Key X Value) *)
    txWriteSet,         (* Transaction -> SUBSET (Key X Value) *)
    
    (* 版本历史 - 用于实现MVCC *)
    versions,           (* Key -> Seq([value: Value, tx: Transaction, status: Status]) *)
    
    (* 锁管理器 - 用于悲观并发控制 *)
    locks,              (* Key -> Transaction | {None}, 写锁 *)
    sharedLocks,        (* Key -> SUBSET Transaction, 读锁 *)
    
    (* 全局时钟 *)
    globalTime          (* Nat *)

(* ----------------------------------------------------------------------------
 * 类型不变式
 * ---------------------------------------------------------------------------- *)

TransactionTypeOK ==
    /\ db \in [Key -> Value]
    /\ isolationLevel \in [Transaction -> 
        {READ_UNCOMMITTED, READ_COMMITTED, REPEATABLE_READ, SERIALIZABLE}]
    /\ txStatus \in [Transaction -> {"active", "committed", "aborted"}]
    /\ txStartTime \in [Transaction -> Nat]
    /\ txReadSet \in [Transaction -> SUBSET (Key \X Value)]
    /\ txWriteSet \in [Transaction -> SUBSET (Key \X Value)]
    /\ versions \in [Key -> Seq([value: Value, tx: Transaction, 
                                  status: {"committed", "active", "aborted"}])]
    /\ locks \in [Key -> Transaction \cup {None}]
    /\ sharedLocks \in [Key -> SUBSET Transaction]
    /\ globalTime \in Nat

(* ----------------------------------------------------------------------------
 * 辅助定义
 * ---------------------------------------------------------------------------- *)

(* 检查事务是否可以看到某个版本 *)
CanSeeVersion(t, key, version) ==
    LET level == isolationLevel[t]
        versionTx == version.tx
    IN CASE level = READ_UNCOMMITTED -> TRUE
       []   level = READ_COMMITTED -> version.status = "committed"
       []   level = REPEATABLE_READ -> 
            /\ version.status = "committed"
            /\ versionTx \in Transaction => txStartTime[versionTx] <= txStartTime[t]
       []   level = SERIALIZABLE ->
            /\ version.status = "committed"
            /\ versionTx \in Transaction => 
                txStatus[versionTx] = "committed" /\ txStartTime[versionTx] < txStartTime[t]
       []   OTHER -> FALSE

(* 获取事务可以看到的最新版本 *)
VisibleVersion(t, key) ==
    LET visibleVersions == 
        {i \in 1..Len(versions[key]) : 
            CanSeeVersion(t, key, versions[key][i])}
    IN IF visibleVersions = {}
       THEN [value |-> db[key], status |-> "committed"]
       ELSE versions[key][Max(visibleVersions)]

(* 检查是否有锁冲突 *)
HasLockConflict(t, key, isWrite) ==
    IF isWrite THEN
        /\ locks[key] # None
        /\ locks[key] # t
    ELSE
        /\ locks[key] # None
        /\ locks[key] # t

(* 检查是否会发生脏读 *)
DirtyReadPossible ==
    \E t1, t2 \in Transaction :
        /\ t1 # t2
        /\ isolationLevel[t2] = READ_UNCOMMITTED
        /\ txStatus[t1] = "active"
        /\ \E key \in Key, val \in Value :
            <<key, val>> \in txWriteSet[t1]

(* 检查是否会发生不可重复读 *)
NonRepeatableReadPossible ==
    \E t \in Transaction :
        /\ isolationLevel[t] \in {READ_UNCOMMITTED, READ_COMMITTED}
        /\ \E key \in Key :
            LET readVals == {val : <<k, val>> \in txReadSet[t] /\ k = key}
            IN Cardinality(readVals) > 1

(* ----------------------------------------------------------------------------
 * 初始状态
 * ---------------------------------------------------------------------------- *)

Init ==
    /\ db = [k \in Key |-> CHOOSE v \in Value : TRUE]  (* 初始值 *)
    /\ isolationLevel \in [Transaction -> 
        {READ_UNCOMMITTED, READ_COMMITTED, REPEATABLE_READ, SERIALIZABLE}]
    /\ txStatus = [t \in Transaction |-> "active"]
    /\ txStartTime = [t \in Transaction |-> 0]
    /\ txReadSet = [t \in Transaction |-> {}]
    /\ txWriteSet = [t \in Transaction |-> {}]
    /\ versions = [k \in Key |-> << >>]
    /\ locks = [k \in Key |-> None]
    /\ sharedLocks = [k \in Key |-> {}]
    /\ globalTime = 0

(* ----------------------------------------------------------------------------
 * 事务操作
 * ---------------------------------------------------------------------------- *)

(* 事务开始 *)
BeginTransaction(t) ==
    /\ txStatus[t] = "active"
    /\ txStartTime[t] = 0    (* 尚未开始 *)
    /\ txStartTime' = [txStartTime EXCEPT ![t] = globalTime]
    /\ globalTime' = globalTime + 1
    /\ UNCHANGED <<db, isolationLevel, txStatus, txReadSet, txWriteSet, 
                   versions, locks, sharedLocks>>

(* 读操作 *)
Read(t, key) ==
    /\ txStatus[t] = "active"
    /\ txStartTime[t] > 0    (* 已开始 *)
    /\ LET version == VisibleVersion(t, key)
       IN txReadSet' = [txReadSet EXCEPT ![t] = @ \cup {<<key, version.value>>}]
    /\ UNCHANGED <<db, isolationLevel, txStatus, txStartTime, txWriteSet, 
                   versions, locks, sharedLocks, globalTime>>

(* 写操作 - 乐观并发控制 *)
WriteOptimistic(t, key, val) ==
    /\ txStatus[t] = "active"
    /\ txStartTime[t] > 0
    /\ txWriteSet' = [txWriteSet EXCEPT ![t] = @ \cup {<<key, val>>}]
    /\ versions' = [versions EXCEPT ![key] = 
        Append(@, [value |-> val, tx |-> t, status |-> "active"])]
    /\ UNCHANGED <<db, isolationLevel, txStatus, txStartTime, txReadSet, 
                   locks, sharedLocks, globalTime>>

(* 写操作 - 悲观并发控制 (需要获取写锁) *)
WritePessimistic(t, key, val) ==
    /\ txStatus[t] = "active"
    /\ txStartTime[t] > 0
    /\ ~HasLockConflict(t, key, TRUE)   (* 无写锁冲突 *)
    /\ locks' = [locks EXCEPT ![key] = t]  (* 获取写锁 *)
    /\ txWriteSet' = [txWriteSet EXCEPT ![t] = @ \cup {<<key, val>>}]
    /\ UNCHANGED <<db, isolationLevel, txStatus, txStartTime, txReadSet, 
                   versions, sharedLocks, globalTime>>

(* 提交事务 - 乐观并发控制 *)
CommitOptimistic(t) ==
    /\ txStatus[t] = "active"
    /\ txStartTime[t] > 0
    /\ txStatus' = [txStatus EXCEPT ![t] = "committed"]
    (* 检查可串行化: 检查读集合是否被修改 *)
    /\ IF isolationLevel[t] = SERIALIZABLE
       THEN \A <<key, val>> \in txReadSet[t] :
            VisibleVersion(t, key).value = val
       ELSE TRUE
    (* 应用写集合 *)
    /\ db' = [k \in Key |-> 
        IF \E v \in Value : <<k, v>> \in txWriteSet[t]
        THEN CHOOSE v \in Value : <<k, v>> \in txWriteSet[t]
        ELSE db[k]]
    (* 更新版本状态 *)
    /\ versions' = [k \in Key |->
        [i \in 1..Len(versions[k]) |->
            IF versions[k][i].tx = t
            THEN [versions[k][i] EXCEPT !.status = "committed"]
            ELSE versions[k][i]]]
    /\ UNCHANGED <<isolationLevel, txStartTime, txReadSet, txWriteSet, 
                   locks, sharedLocks, globalTime>>

(* 提交事务 - 悲观并发控制 *)
CommitPessimistic(t) ==
    /\ txStatus[t] = "active"
    /\ txStartTime[t] > 0
    /\ txStatus' = [txStatus EXCEPT ![t] = "committed"]
    (* 应用写集合 *)
    /\ db' = [k \in Key |-> 
        IF \E v \in Value : <<k, v>> \in txWriteSet[t]
        THEN CHOOSE v \in Value : <<k, v>> \in txWriteSet[t]
        ELSE db[k]]
    (* 释放锁 *)
    /\ locks' = [k \in Key |-> 
        IF locks[k] = t THEN None ELSE locks[k]]
    /\ sharedLocks' = [k \in Key |-> sharedLocks[k] \ {t}]
    /\ UNCHANGED <<isolationLevel, txStartTime, txReadSet, txWriteSet, 
                   versions, globalTime>>

(* 中止事务 *)
AbortTransaction(t) ==
    /\ txStatus[t] = "active"
    /\ txStatus' = [txStatus EXCEPT ![t] = "aborted"]
    (* 更新版本状态 *)
    /\ versions' = [k \in Key |->
        [i \in 1..Len(versions[k]) |->
            IF versions[k][i].tx = t
            THEN [versions[k][i] EXCEPT !.status = "aborted"]
            ELSE versions[k][i]]]
    (* 释放锁 *)
    /\ locks' = [k \in Key |-> 
        IF locks[k] = t THEN None ELSE locks[k]]
    /\ sharedLocks' = [k \in Key |-> sharedLocks[k] \ {t}]
    /\ UNCHANGED <<db, isolationLevel, txStartTime, txReadSet, txWriteSet, globalTime>>

(* ----------------------------------------------------------------------------
 * 下一步动作
 * ---------------------------------------------------------------------------- *)

Next ==
    \/ \E t \in Transaction : BeginTransaction(t)
    \/ \E t \in Transaction, k \in Key : Read(t, k)
    \/ \E t \in Transaction, k \in Key, v \in Value : WriteOptimistic(t, k, v)
    \/ \E t \in Transaction : CommitOptimistic(t)
    \/ \E t \in Transaction : AbortTransaction(t)

(* ----------------------------------------------------------------------------
 * 规约
 * ---------------------------------------------------------------------------- *)

Spec == Init /\ [][Next]_<<db, isolationLevel, txStatus, txStartTime, txReadSet, 
                              txWriteSet, versions, locks, sharedLocks, globalTime>>

(* ----------------------------------------------------------------------------
 * 不变式 (安全性)
 * ---------------------------------------------------------------------------- *)

(* 类型不变式 *)
TypeInvariant == TransactionTypeOK

(* 已提交事务的写最终反映在数据库中 *)
CommittedWritesPersist ==
    \A t \in Transaction :
        txStatus[t] = "committed" =>
            \A <<key, val>> \in txWriteSet[t] : db[key] = val

(* 隔离级别保证: SERIALIZABLE 不会看到不一致状态 *)
SerializableConsistency ==
    \A t \in Transaction :
        isolationLevel[t] = SERIALIZABLE /\ txStatus[t] = "committed" =>
            (* 读集合在提交时仍然有效 *)
            \A <<key, val>> \in txReadSet[t] : db[key] = val

(* 锁的不变性: 只有一个事务能持有写锁 *)
LockInvariant ==
    \A k \in Key :
        locks[k] # None => 
            /\ txStatus[locks[k]] = "active"
            /\ ~\E t2 \in Transaction : 
                t2 # locks[k] /\ t2 \in sharedLocks[k]

(* ----------------------------------------------------------------------------
 * 异常检测性质
 * ---------------------------------------------------------------------------- *)

(* 脏读检测: READ_UNCOMMITTED 允许, 其他级别禁止 *)
DirtyReadAnomaly ==
    \E t \in Transaction, k \in Key :
        /\ isolationLevel[t] \in {READ_COMMITTED, REPEATABLE_READ, SERIALIZABLE}
        /\ \E <<key, val>> \in txReadSet[t] :
            /\ key = k
            /\ \E v \in versions[k] :
                /\ v.value = val
                /\ v.status = "active"

(* 不可重复读检测 *)
NonRepeatableReadAnomaly ==
    \E t \in Transaction, k \in Key :
        /\ isolationLevel[t] \in {READ_UNCOMMITTED, READ_COMMITTED}
        /\ LET reads == {v : <<key, v>> \in txReadSet[t]}
           IN Cardinality(reads) > 1

(* 幻读检测 *)
PhantomReadAnomaly ==
    \E t \in Transaction :
        /\ isolationLevel[t] \in {READ_UNCOMMITTED, READ_COMMITTED, REPEATABLE_READ}
        /\ \E k1, k2 \in Key :
            /\ k1 # k2
            /\ <<k1, db[k1]>> \in txReadSet[t]
            /\ ~\E v : <<k2, v>> \in txReadSet[t]
            /\ txStatus[t] = "committed"

(* ----------------------------------------------------------------------------
 * 模型检查配置
 * ---------------------------------------------------------------------------- *)
(*
TLC Model Checker 配置:

1. 定义常量:
   Transaction = {t1, t2}
   Key = {k1, k2}
   Value = {v1, v2, v3}
   READ_UNCOMMITTED = READ_UNCOMMITTED
   READ_COMMITTED = READ_COMMITTED
   REPEATABLE_READ = REPEATABLE_READ
   SERIALIZABLE = SERIALIZABLE

2. 不变式:
   - TypeInvariant
   - CommittedWritesPersist
   - LockInvariant

3. 检查的属性:
   - ~DirtyReadAnomaly  (验证高级别隔离禁止脏读)
   - ~NonRepeatableReadAnomaly  (验证可重复读以上级别禁止)

4. 注意: 不同隔离级别应使用不同配置测试
*)

================================================================================
