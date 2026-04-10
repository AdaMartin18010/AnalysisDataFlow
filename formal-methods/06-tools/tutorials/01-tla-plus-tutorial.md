# TLA+入门教程

> **所属教程**: Tools/Tutorials | **预计学习时间**: 4-6小时 | **前置知识**: 基本逻辑概念

## 概述

本教程将引导您从TLA+初学者到能够独立建模和验证简单分布式系统的水平。

## 学习目标

完成本教程后，您将能够：

1. 理解TLA+的基本概念和语法
2. 使用PlusCal编写算法规范
3. 使用TLC模型检测器验证性质
4. 解读TLC的错误轨迹和覆盖报告
5. 为简单协议建立正确性论证

---

## 第1部分：环境搭建与首个规范（1小时）

### 1.1 安装TLA+ Toolbox

**步骤1**: 下载与安装

```bash
# Windows/macOS/Linux: 从官网下载
# https://lamport.azurewebsites.net/tla/toolbox.html

# 验证安装
# 打开Toolbox → Help → About → 确认版本
```

**步骤2**: 配置Java（如需要）

- TLA+ Toolbox需要Java 11+
- 设置`JAVA_HOME`环境变量

### 1.2 创建首个TLA+规范

**目标**: 编写一个简单的时钟规范

**步骤1**: 创建新规范

1. File → Open Spec → Add New Spec
2. 命名: `Clock.tla`
3. 选择保存位置

**步骤2**: 编写基础规范

```tla
------------------------------- MODULE Clock -------------------------------
EXTENDS Naturals

VARIABLE hour

TypeInvariant == hour \in 1..12

Init == hour = 12

Next == hour' = IF hour = 12 THEN 1 ELSE hour + 1

Spec == Init /\ [][Next]_hour
=============================================================================
```

**步骤3**: 创建模型并验证

1. 在Spec Explorer中右键 → Create Model
2. Model Overview:
   - **What to check?**:
     - TypeInvariant 添加到 Invariants
   - **What is the model?**:
     - 无需设置（无常量）
3. 点击 Run TLC
4. 预期结果: "No error"

### 1.3 添加时序性质

**扩展规范**（添加到时钟之后）：

```tla
(* 安全性：时针始终在有效范围内 *)
Safety == []TypeInvariant

(* 活性：时针最终会指向每个小时 *)
Liveness == \A h \in 1..12 : <>(hour = h)
```

**模型配置**:

1. 在 Properties 中添加 `Liveness`
2. 设置 "Temporal formula" 为 `Spec`
3. 运行验证

---

## 第2部分：PlusCal算法语言（1.5小时）

### 2.1 理解PlusCal

PlusCal是伪代码风格的算法描述语言，编译为TLA+。

**PlusCal语法结构**：

```pluscal
--algorithm AlgorithmName
variables
    global_vars = initial_values;

define
    (* 常量定义和辅助谓词 *)
end define;

macro MacroName(params) begin
    (* 宏体 *)
end macro;

process ProcessName \in ProcessSet
variables
    local_vars;
begin
Label1:
    statements;
Label2:
    statements;
end process;

end algorithm
```

### 2.2 练习：互斥算法

**目标**: 实现并验证Peterson互斥算法

**步骤1**: 创建新规范 `Peterson.tla`

**步骤2**: 编写PlusCal代码

```tla
------------------------------- MODULE Peterson -------------------------------
EXTENDS TLC, Integers, Sequences

CONSTANTS N

(*--algorithm Peterson
variables
    flag = [i \in 0..N-1 |-> FALSE],
    turn = 0;

define
    (* 互斥不变式：最多一个进程在临界区 *)
    MutualExclusion ==
        \A i, j \in 0..N-1 :
            (i # j) => ~((pc[i] = "CS") /\ (pc[j] = "CS"))

    (* 活性：如果进程想进入临界区，最终会进入 *)
    Liveness ==
        \A i \in 0..N-1 :
            (pc[i] = "L2") ~> (pc[i] = "CS")
end define;

process Proc \in 0..N-1
variables
    other;
begin
L1:
    other := 1 - self;
L2:
    flag[self] := TRUE;
L3:
    turn := other;
L4:
    await (~flag[other]) \/ (turn = self);
CS:
    skip;  (* 临界区 *)
L5:
    flag[self] := FALSE;
goto L1;

end process;

end algorithm;*)
=============================================================================
```

**步骤3**: 编译PlusCal

1. 保存文件
2. File → Translate PlusCal Algorithm
3. 或按 `Ctrl+T`

**步骤4**: 创建模型验证

1. Create Model
2. Set "What is the model?" → N = 2
3. Add `MutualExclusion` to Invariants
4. Add `Liveness` to Properties
5. Run TLC

### 2.3 分析错误轨迹

**引入bug测试**：

修改L4为：

```pluscal
L4:
    await (~flag[other]);  (* 删除 \/ (turn = self) *)
```

重新验证，观察：

1. Error Trace显示
2. 状态序列分析
3. 死锁识别

---

## 第3部分：分布式系统建模（1.5小时）

### 3.1 两阶段提交协议

**目标**: 建模并验证2PC协议的安全性质

**创建规范** `TwoPhaseCommit.tla`：

```tla
------------------------------- MODULE TwoPhaseCommit -------------------------------
EXTENDS Integers, FiniteSets, TLC

CONSTANTS Participants, Coordinator

VARIABLES
    pc,           (* 参与者状态 *)
    coordState,   (* 协调者状态 *)
    votes,        (* 投票集合 *)
    decision      (* 最终决策 *)

Vars == <<pc, coordState, votes, decision>>

(* 类型不变式 *)
TypeInvariant ==
    /\ pc \in [Participants -> {"working", "prepared", "committed", "aborted"}]
    /\ coordState \in {"init", "collecting", "decided"}
    /\ votes \subseteq Participants
    /\ decision \in {"none", "commit", "abort"}

(* 初始化 *)
Init ==
    /\ pc = [p \in Participants |-> "working"]
    /\ coordState = "init"
    /\ votes = {}
    /\ decision = "none"

(* 参与者准备 *)
Prepare(p) ==
    /\ pc[p] = "working"
    /\ pc' = [pc EXCEPT ![p] = "prepared"]
    /\ UNCHANGED <<coordState, votes, decision>>

(* 协调者收集投票 *)
CollectVote(p) ==
    /\ coordState = "init" \/ coordState = "collecting"
    /\ pc[p] = "prepared"
    /\ p \notin votes
    /\ votes' = votes \union {p}
    /\ coordState' = "collecting"
    /\ UNCHANGED <<pc, decision>>

(* 协调者决策 *)
Decide ==
    /\ coordState = "collecting"
    /\ coordState' = "decided"
    /\ IF votes = Participants
       THEN decision' = "commit"
       ELSE decision' = "abort"
    /\ UNCHANGED <<pc, votes>>

(* 传播决策 *)
DeliverDecision(p) ==
    /\ coordState = "decided"
    /\ decision # "none"
    /\ pc[p] = "prepared"
    /\ pc' = [pc EXCEPT ![p] =
               IF decision = "commit" THEN "committed" ELSE "aborted"]
    /\ UNCHANGED <<coordState, votes, decision>>

(* 下一步 *)
Next ==
    \/ \E p \in Participants : Prepare(p)
    \/ \E p \in Participants : CollectVote(p)
    \/ Decide
    \/ \E p \in Participants : DeliverDecision(p)

Spec == Init /\ [][Next]_Vars

(* 安全性质：统一决策 *)
UniformDecision ==
    \A p1, p2 \in Participants :
        ((pc[p1] = "committed" /\ pc[p2] = "aborted") => FALSE)

(* 一致性定理 *)
Consistency == []UniformDecision
=============================================================================
```

### 3.2 模型配置与验证

**模型设置**:

1. Create Model
2. Set constant assignment:
   - `Participants <- {p1, p2, p3}`
3. Add to Invariants:
   - `TypeInvariant`
4. Add to Properties:
   - `Consistency`

**验证结果分析**:

1. 检查 "State space diameter"
2. 查看 "Distinct states"
3. 分析覆盖率

### 3.3 探索状态空间

**状态空间可视化**:

1. TLC Options → "Visualize state graph"
2. 观察可达状态
3. 识别死状态和循环

---

## 第4部分：高级验证技术（1小时）

### 4.1 对称性约简

**配置对称性**:

在Model的 "Advanced Options" 中：

```
Definition Override:
  Symmetry <- Permutations({p1, p2, p3})
```

**效果**:

- 减少状态空间
- 加速验证

### 4.2 约束状态空间

**添加状态约束**:

```tla
StateConstraint ==
    /\ Cardinality(votes) <= 3
```

在Model的 "State Constraint" 中添加。

### 4.3 使用表达式求值

**检查特定状态**:

1. 在 TLC Errors 视图中
2. 选择一个状态
3. 右键 → Evaluate Constant Expression
4. 输入: `pc["p1"]`

---

## 第5部分：综合练习（1小时）

### 5.1 练习：Raft领导选举

**任务**: 为简化版Raft领导选举建模

**要求**:

1. 定义状态变量（term, role, votedFor）
2. 实现RequestVote RPC
3. 验证安全性：同一term最多一个leader
4. 验证活性：最终会选出leader

**提示**: 参考 Raft 论文 Figure 3

**参考答案框架**:

```tla
------------------------------- MODULE Raft -------------------------------
EXTENDS Integers, TLC

CONSTANTS Servers

VARIABLES
    currentTerm,
    role,
    votedFor

(* 类型不变式 *)
TypeInvariant ==
    /\ currentTerm \in [Servers -> Nat]
    /\ role \in [Servers -> {"follower", "candidate", "leader"}]
    /\ votedFor \in [Servers -> Servers \union {Nil}]

(* 安全性：同一term最多一个leader *)
SingleLeaderPerTerm ==
    \A s1, s2 \in Servers :
        (role[s1] = "leader" /\ role[s2] = "leader" /\ s1 # s2)
            => currentTerm[s1] # currentTerm[s2]

(* 实现剩余规范... *)
=============================================================================
```

### 5.2 故障排除指南

| 问题 | 解决方案 |
|------|----------|
| "Deadlock reached" | 检查所有状态都有可能的Next |
| "Invariant violated" | 查看错误轨迹，理解违反路径 |
| "Temporal property violated" | 检查公平性假设 |
| "State space explosion" | 使用对称性、状态约束 |
| TLC运行缓慢 | 增加工作者线程数 |

---

## 总结

### 关键概念回顾

1. **TLA+核心**: 状态机 + 时序逻辑
2. **PlusCal**: 伪代码风格的高级建模
3. **TLC**: 显式状态模型检测
4. **验证流程**: 建模 → 定义性质 → 模型检测 → 分析结果

### 进一步学习资源

- [Specifying Systems](https://lamport.azurewebsites.net/tla/book.html) - Leslie Lamport的经典教材
- [TLA+ Video Course](https://lamport.azurewebsites.net/video/videos.html)
- [Learn TLA+](https://learntla.com/) - Hillel Wayne的教程

### 实践建议

1. 从简单模型开始，逐步增加复杂度
2. 始终先定义安全性质，再考虑活性
3. 善用错误轨迹调试规范
4. 保持模型抽象，避免过度实现细节

---

## 练习答案

### 练习5.1 参考答案

完整的Raft领导选举规范（简化版）：

```tla
------------------------------- MODULE RaftElection -------------------------------
EXTENDS Integers, FiniteSets, TLC

CONSTANTS Servers, MaxTerm

VARIABLES
    currentTerm,
    role,
    votedFor,
    votesGranted

vars == <<currentTerm, role, votedFor, votesGranted>>

Nil == CHOOSE s : s \notin Servers

TypeInvariant ==
    /\ currentTerm \in [Servers -> 0..MaxTerm]
    /\ role \in [Servers -> {"follower", "candidate", "leader"}]
    /\ votedFor \in [Servers -> Servers \union {Nil}]
    /\ votesGranted \in [Servers -> SUBSET Servers]

Init ==
    /\ currentTerm = [s \in Servers |-> 0]
    /\ role = [s \in Servers |-> "follower"]
    /\ votedFor = [s \in Servers |-> Nil]
    /\ votesGranted = [s \in Servers |-> {}]

(* 超时变为候选者 *)
Timeout(s) ==
    /\ role[s] \in {"follower", "candidate"}
    /\ currentTerm' = [currentTerm EXCEPT ![s] = @ + 1]
    /\ role' = [role EXCEPT ![s] = "candidate"]
    /\ votedFor' = [votedFor EXCEPT ![s] = s]
    /\ votesGranted' = [votesGranted EXCEPT ![s] = {s}]

(* 处理RequestVote RPC *)
RequestVote(s, candidate) ==
    /\ currentTerm[candidate] >= currentTerm[s]
    /\ currentTerm' = [currentTerm EXCEPT ![s] = currentTerm[candidate]]
    /\ IF role[s] = "follower" /\ (votedFor[s] = Nil \/ votedFor[s] = candidate)
       THEN
         /\ votedFor' = [votedFor EXCEPT ![s] = candidate]
         /\ votesGranted' = [votesGranted EXCEPT ![candidate] = @ \union {s}]
       ELSE
         UNCHANGED <<votedFor, votesGranted>>
    /\ role' = IF currentTerm[candidate] > currentTerm[s]
               THEN [role EXCEPT ![s] = "follower"]
               ELSE role

(* 成为Leader *)
BecomeLeader(s) ==
    /\ role[s] = "candidate"
    /\ Cardinality(votesGranted[s]) * 2 > Cardinality(Servers)
    /\ role' = [role EXCEPT ![s] = "leader"]
    /\ UNCHANGED <<currentTerm, votedFor, votesGranted>>

Next ==
    \/ \E s \in Servers : Timeout(s)
    \/ \E s, candidate \in Servers : RequestVote(s, candidate)
    \/ \E s \in Servers : BecomeLeader(s)

Spec == Init /\ [][Next]_vars

(* 安全性质 *)
SingleLeaderPerTerm ==
    \A s1, s2 \in Servers :
        (role[s1] = "leader" /\ role[s2] = "leader" /\ s1 # s2)
            => currentTerm[s1] # currentTerm[s2]

ElectionSafety == []SingleLeaderPerTerm
=============================================================================
```

模型配置:

- `Servers <- {s1, s2, s3}`
- `MaxTerm <- 3`
- Invariants: `TypeInvariant`, `SingleLeaderPerTerm`
