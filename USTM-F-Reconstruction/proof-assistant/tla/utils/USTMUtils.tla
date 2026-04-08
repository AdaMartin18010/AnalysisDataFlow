------------------------------- MODULE USTMUtils -------------------------------
(*
 * USTM (Unified Streaming Theory Model) 通用工具定义
 * 版本: 1.0.0
 * 描述: 提供TLA+规约中常用的辅助定义、类型和操作
 *)

EXTENDS Integers, Sequences, FiniteSets, Naturals, TLC

(* ===========================================================================
 * 基本类型定义
 * ===========================================================================*)

(* 节点标识符类型 *)
NodeId == Nat

(* 检查点ID类型 *)
CheckpointId == Nat

(* 时间戳类型 *)
Timestamp == Nat

(* 状态类型：可以是任意值，这里用Nat作为示例 *)
StateValue == Nat

(* 操作类型 *)
Operation == {"READ", "WRITE", "COMMIT", "ABORT"}

(* 消息类型 *)
MessageType == {"CHECKPOINT_TRIGGER", "CHECKPOINT_ACK", "CHECKPOINT_COMPLETE",
               "PREPARE", "PREPARE_ACK", "COMMIT", "COMMIT_ACK", 
               "ABORT", "WATERMARK", "BARRIER"}

(* ===========================================================================
 * 集合操作工具
 * ===========================================================================*)

(* 计算集合的笛卡尔积的子集 *)
AllFunctions(S, T) == [S -> T]

(* 判断集合是否为单例 *)
IsSingleton(S) == \E x \in S : S = {x}

(* 获取集合的任意元素 *)
CHOOSEOne(S) == CHOOSE x \in S : TRUE

(* 计算两个集合的差集 *)
SetDifference(S, T) == {x \in S : x \notin T}

(* 判断集合S是否是T的子集 *)
IsSubset(S, T) == \A x \in S : x \in T

(* ===========================================================================
 * 序列操作工具
 * ===========================================================================*)

(* 序列的长度 *)
SeqLength(seq) == Len(seq)

(* 获取序列的最后一个元素 *)
Last(seq) == seq[Len(seq)]

(* 判断序列是否为空 *)
IsEmpty(seq) == Len(seq) = 0

(* 序列前缀检查 *)
IsPrefix(pref, seq) == 
    Len(pref) <= Len(seq) /\ \A i \in 1..Len(pref) : pref[i] = seq[i]

(* 序列拼接（已在内建中有\circ，这里提供别名） *)
Concat(seq1, seq2) == seq1 \o seq2

(* 从序列构造集合 *)
SeqToSet(seq) == {seq[i] : i \in 1..Len(seq)}

(* 从集合构造序列（非确定性选择） *)
SetToSeq(S) == CHOOSE seq \in [1..Cardinality(S) -> S] : TRUE

(* ===========================================================================
 * 关系与函数工具
 * ===========================================================================*)

(* 关系的定义域 *)
DOMAIN_OF(R) == {r[1] : r \in R}

(* 关系的值域 *)
RANGE_OF(R) == {r[2] : r \in R}

(* 函数限制 *)
Restrict(f, S) == [x \in S |-> f[x]]

(* 函数更新 *)
Update(f, x, v) == [f EXCEPT ![x] = v]

(* 多重更新 *)
UpdateMany(f, updates) == 
    LET UpdateOne(g, pair) == [g EXCEPT ![pair[1]] = pair[2]]
    IN FoldSeq(UpdateOne, f, updates)

(* 序列折叠 *)
RECURSIVE FoldSeq(_, _, _)
FoldSeq(Op(_, _), base, seq) ==
    IF Len(seq) = 0 THEN base
    ELSE FoldSeq(Op, Op(base, Head(seq)), Tail(seq))

(* 序列头部 *)
Head(seq) == seq[1]

(* 序列尾部 *)
Tail(seq) == [i \in 1..(Len(seq)-1) |-> seq[i+1]]

(* ===========================================================================
 * 状态机工具
 * ===========================================================================*)

(* 状态转换类型 *)
StateTransition == [from: STRING, to: STRING, action: STRING]

(* 判断状态机是否可以执行转换 *)
CanTransition(currentState, transition, stateMachine) ==
    \E t \in stateMachine : 
        t.from = currentState /\ t.action = transition

(* 执行状态转换 *)
ExecuteTransition(currentState, action, stateMachine) ==
    CHOOSE t \in stateMachine : 
        t.from = currentState /\ t.action = action

(* ===========================================================================
 * 时间与Watermark工具
 * ===========================================================================*)

(* 判断时间戳序列是否单调递增 *)
IsMonotonicIncreasing(seq) ==
    \A i, j \in 1..Len(seq) : i < j => seq[i] <= seq[j]

(* 判断Watermark是否单调不减 *)
IsWatermarkMonotonic(watermarks) ==
    IsMonotonicIncreasing(watermarks)

(* 计算最小Watermark *)
MinWatermark(watermarks) ==
    IF watermarks = {} THEN 0
    ELSE CHOOSE w \in watermarks : \A w2 \in watermarks : w <= w2

(* 计算最大Watermark *)
MaxWatermark(watermarks) ==
    IF watermarks = {} THEN 0
    ELSE CHOOSE w \in watermarks : \A w2 \in watermarks : w >= w2

(* ===========================================================================
 * 检查点相关工具
 * ===========================================================================*)

(* 检查点状态 *)
CheckpointStatus == {"PENDING", "IN_PROGRESS", "COMPLETED", "FAILED"}

(* 检查点记录结构 *)
CheckpointRecord == [
    id: CheckpointId,
    status: CheckpointStatus,
    startTime: Timestamp,
    endTime: Timestamp,
    acks: SUBSET NodeId
]

(* 判断检查点是否完成 *)
IsCheckpointComplete(cp, allNodes) ==
    cp.status = "COMPLETED" / 
    (cp.status = "IN_PROGRESS" /\ cp.acks = allNodes)

(* ===========================================================================
 * 一致性相关工具
 * ===========================================================================*)

(* 线性化点类型 *)
LinearizationPoint == [
    operation: Operation,
    startTime: Timestamp,
    endTime: Timestamp,
    value: StateValue
]

(* 判断操作是否并发 *)
AreConcurrent(op1, op2) ==
    ~(op1.endTime < op2.startTime / op2.endTime < op1.startTime)

(* 偏序关系：happens-before *)
HappensBefore(op1, op2) == op1.endTime < op2.startTime

(* ===========================================================================
 * 错误处理工具
 * ===========================================================================*)

(* 错误类型 *)
ErrorType == {"NONE", "TIMEOUT", "NETWORK_ERROR", "NODE_FAILURE", "INCONSISTENT_STATE"}

(* 结果类型 *)
Result(ValueType) == [success: BOOLEAN, value: ValueType, error: ErrorType]

(* 成功结果构造 *)
Success(value) == [success |-> TRUE, value |-> value, error |-> "NONE"]

(* 失败结果构造 *)
Failure(error) == [success |-> FALSE, value |-> 0, error |-> error]

(* ===========================================================================
 * 数学工具
 * ===========================================================================*)

(* 最大值 *)
Max(a, b) == IF a > b THEN a ELSE b

(* 最小值 *)
Min(a, b) == IF a < b THEN a ELSE b

(* 绝对值 *)
Abs(x) == IF x < 0 THEN -x ELSE x

(* 向上取整除法 *)
CeilDiv(a, b) == (a + b - 1) \div b

(* 向下取整除法（等同于整数除法） *)
FloorDiv(a, b) == a \div b

(* 模运算 *)
Mod(a, b) == a % b

(* ===========================================================================
 * 辅助不变式工具
 * ===========================================================================*)

(* 类型不变式检查器 *)
TypeInvariant(value, expectedType) == value \in expectedType

(* 状态有效性检查 *)
ValidState(state, validStates) == state \in validStates

(* 范围约束 *)
InRange(value, min, max) == value >= min /\ value <= max

(* ===========================================================================
 * 调试与日志工具
 * ===========================================================================*)

(* 日志级别 *)
LogLevel == {"DEBUG", "INFO", "WARN", "ERROR"}

(* 日志条目 *)
LogEntry == [
    timestamp: Timestamp,
    level: LogLevel,
    component: STRING,
    message: STRING
]

(* ===========================================================================
 * 规约属性辅助
 * ===========================================================================*)

(* 最终总是（Eventual Always） *)
EF_P(P) == <>[]P

(* 总是最终（Always Eventually） *)
AF_P(P) == []<>P

(* 强公平性条件构造器 *)
StrongFairness(action, enableCond) ==
    SF_vars(action)

(* 弱公平性条件构造器 *)
WeakFairness(action, enableCond) ==
    WF_vars(action)

================================================================================
(* Last modified: 2026-04-08 *)
(* Author: USTM Formal Verification Team *)
