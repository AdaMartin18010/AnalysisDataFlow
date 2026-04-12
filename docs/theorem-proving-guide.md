# 定理证明指南

> 所属阶段: docs | 前置依赖: [formal-methods/](../formal-methods/) | 形式化等级: L4

本指南提供流计算系统定理证明的完整参考，涵盖 Coq 和 TLA+ 两大形式化验证工具的使用方法。

---

## 目录

1. [Coq入门指南](#1-coq入门指南)
2. [TLA+建模指南](#2-tla建模指南)
3. [证明策略手册](#3-证明策略手册)
4. [常见证明模式](#4-常见证明模式)
5. [自动化工具链](#5-自动化工具链)

---

## 1. Coq入门指南

### 1.1 安装与配置

```bash
# Ubuntu/Debian
sudo apt-get install coq libcoq-ocaml-dev

# macOS
brew install coq

# Windows (通过WSL或官方安装包)
# 下载: https://github.com/coq/coq/releases

# 验证安装
coqtop --version
```

### 1.2 基础语法

```coq
(* 定义类型 *)
Inductive nat : Type :=
  | O : nat
  | S : nat -> nat.

(* 定义函数 *)
Fixpoint plus (n m : nat) : nat :=
  match n with
  | O => m
  | S p => S (plus p m)
  end.

(* 定理陈述 *)
Theorem plus_O_n : forall n : nat, plus O n = n.
Proof.
  intros n. simpl. reflexivity.
Qed.
```

### 1.3 流计算专用库

```coq
(* 加载流计算定理库 *)
Require Import streaming-theorems.

(* 使用预定义类型 *)
Check Event.           (* Event T: 带时间戳的事件 *)
Check Stream.          (* Stream T: 事件流 *)
Check Window.          (* Window: 窗口类型 *)
```

### 1.4 核心概念映射

| 流计算概念 | Coq表示 | 说明 |
|-----------|---------|------|
| 事件 | `Event T` | 带时间戳的数据元素或Watermark |
| 数据流 | `Stream T` | 事件的序列 |
| 窗口 | `Window` | 滚动/滑动/会话窗口 |
| 算子 | `Operator A B` | 流转换操作 |
| Checkpoint | `Checkpoint T` | 状态快照 |

### 1.5 证明Exactly-Once语义

```coq
(* 示例: 证明Map操作保持Exactly-Once *)
Theorem map_preserves_exactly_once :
  forall (A B: Type) (f: A -> B) (s: Stream A),
    ExactlyOnceSemantics (fun x => apply_operator (Map f) x).
Proof.
  intros A B f s.
  unfold ExactlyOnceSemantics.
  intros input output Hprocess e Hin.
  (* 展开Map操作定义 *)
  unfold apply_operator in Hprocess.
  simpl in Hprocess.
  (* 证明每个输入产生唯一输出 *)
  exists (EventElem (f (event_value e)) (event_timestamp e)).
  split.
  - (* 证明输出在结果中 *)
    admit.
  - (* 证明唯一性 *)
    admit.
Admitted.
```

---

## 2. TLA+建模指南

### 2.1 安装与配置

```bash
# 安装TLA+ Toolbox
curl -L https://github.com/tlaplus/tlaplus/releases/download/v1.7.1/TLAToolbox-1.7.1-linux.gtk.x86_64.zip -o tla.zip
unzip tla.zip

# 或使用Apalache模型检查器
curl -L https://github.com/informalsystems/apalache/releases/download/v0.44.0/apalache.tgz | tar xz
```

### 2.2 基础模块结构

```tla
---- MODULE Example ----
EXTENDS Integers, Sequences, FiniteSets

(* 常量定义 *)
CONSTANTS MaxValue, Workers

(* 变量定义 *)
VARIABLES state, counter

(* 类型不变量 *)
TypeOK ==
    /\ state \in {"idle", "processing", "completed"}
    /\ counter \in 0..MaxValue

(* 初始状态 *)
Init ==
    /\ state = "idle"
    /\ counter = 0

(* 状态转换 *)
StartProcessing ==
    /\ state = "idle"
    /\ state' = "processing"
    /\ counter' = counter + 1

CompleteProcessing ==
    /\ state = "processing"
    /\ state' = "completed"
    /\ UNCHANGED counter

(* 下一状态 *)
Next ==
    \/ StartProcessing
    \/ CompleteProcessing

(* 规范 *)
Spec == Init /\ [][Next]_<<state, counter>>
====
```

### 2.3 流系统建模模式

```tla
(* 数据流状态 *)
VARIABLES
    records,          (* 输入记录集合 *)
    processed,        (* 已处理记录 *)
    watermarks        (* 当前Watermark值 *)

(* 处理动作 *)
ProcessRecord(r) ==
    /\ r \in records
    /\ r \notin processed
    /\ processed' = processed \union {r}
    /\ UNCHANGED <<records, watermarks>>

(* Watermark推进 *)
AdvanceWatermark(w) ==
    /\ w > watermarks
    /\ watermarks' = w
    /\ UNCHANGED <<records, processed>>
```

### 2.4 一致性验证

```tla
(* 安全性: 无重复处理 *)
NoDuplicateProcessing ==
    \A r1, r2 \in processed :
        r1.id = r2.id => r1 = r2

(* 活性: 所有记录最终处理 *)
AllRecordsProcessed ==
    <>[](processed = records)

(* Exactly-Once语义 *)
ExactlyOnce ==
    []NoDuplicateProcessing /\ AllRecordsProcessed
```

### 2.5 Checkpoint建模

```tla
(* Checkpoint触发 *)
TriggerCheckpoint ==
    /\ checkpointId' = checkpointId + 1
    /\ checkpointStates' = checkpointStates \union 
        {[id |-> checkpointId', 
          state |-> operatorStates,
          timestamp |-> Now]}

(* 从Checkpoint恢复 *)
RecoverFromCheckpoint(cid) ==
    /\ cid \in DOMAIN checkpointStates
    /\ operatorStates' = checkpointStates[cid].state
    /\ checkpointId' = cid
```

---

## 3. 证明策略手册

### 3.1 Coq证明策略

#### 基础策略

| 策略 | 用途 | 示例 |
|-----|------|------|
| `intros` | 引入假设 | `intros n m H` |
| `simpl` | 简化表达式 | `simpl` |
| `reflexivity` | 证明等式 | `reflexivity` |
| `rewrite` | 使用等式重写 | `rewrite H` |
| `apply` | 应用定理/假设 | `apply H` |
| `destruct` | 情况分析 | `destruct n` |
| `induction` | 归纳证明 | `induction n` |

#### 高级策略

```coq
(* 自动证明 *)
auto.           (* 使用hint数据库自动证明 *)
eauto.          (* 扩展的自动证明 *)
firstorder.     (* 一阶逻辑自动证明 *)

(* 自定义自动化 *)
Hint Resolve plus_O_n : arith.
auto with arith.
```

### 3.2 TLA+证明策略

#### 不变量证明

```tla
(* 证明TypeOK是不变量 *)
THEOREM TypeCorrectness ==
    Spec => []TypeOK

(* 归纳证明步骤 *)
<1>1. Init => TypeOK
    BY DEF Init, TypeOK

<1>2. TypeOK /\ [Next]_vars => TypeOK'
    BY DEF TypeOK, Next, vars

<1>3. QED
    BY <1>1, <1>2, PTL DEF Spec
```

#### 活性证明

```tla
(* 证明Eventually属性 *)
THEOREM EventuallyProcessed ==
    Spec => AllRecordsEventuallyProcessed

(* 使用公平性 *)
<1>1. SF_vars(ProcessRecord)
    BY DEF Fairness

<1>2. QED
    BY <1>1, PTL
```

### 3.3 流计算专用策略

#### Watermark单调性证明

```coq
Lemma watermark_monotonicity :
  forall (T: Type) (s: Stream T) (op: Operator T T),
    MonotonicWatermark s ->
    MonotonicWatermark (apply_operator op s).
Proof.
  intros T s op Hmono i j wi wj Hi_lt_j Hnth_i Hnth_j.
  destruct op.
  - (* Map操作符 *)
    apply map_preserves_monotonicity; assumption.
  - (* Filter操作符 *)
    apply filter_preserves_monotonicity; assumption.
  (* ... 其他操作符 ... *)
Qed.
```

#### Checkpoint一致性证明

```tla
THEOREM CheckpointConsistency ==
    Spec => [](\A cid \in completedCheckpoints :
        \A w1, w2 \in Workers :
            checkpointStates[cid][w1].timestamp = 
            checkpointStates[cid][w2].timestamp)

<1>1. Init => ...
<1>2. [Next]_vars /\ ...
<1>3. QED BY ...
```

---

## 4. 常见证明模式

### 4.1 结构归纳法

```coq
(* 流的结构归纳 *)
Fixpoint stream_induction {T P: Type}
  (P: Stream T -> Prop)
  (Hnil: P [])
  (Hcons: forall e es, P es -> P (e :: es))
  (s: Stream T) : P s.
Proof.
  destruct s.
  - apply Hnil.
  - apply Hcons. apply stream_induction; assumption.
Defined.
```

### 4.2 互模拟证明

```coq
(* 流等价性的互模拟证明 *)
CoInductive StreamEq {T: Type} : Stream T -> Stream T -> Prop :=
  | EqNil : StreamEq [] []
  | EqCons : forall e1 e2 s1 s2,
      e1 = e2 ->
      StreamEq s1 s2 ->
      StreamEq (e1 :: s1) (e2 :: s2).

(* 证明两个流等价 *)
CoFixpoint prove_stream_eq {T: Type} (s1 s2: Stream T) : StreamEq s1 s2.
Proof.
  (* 构造互模拟关系 *)
Admitted.
```

### 4.3 安全性与活性组合

```tla
(* 组合安全性和活性 *)
Correctness ==
    /\ []SafetyInvariant
    /\ LivenessProperty

(* 证明分解 *)
THEOREM SystemCorrect ==
    Spec => Correctness

<1>1. Spec => []SafetyInvariant
    (* 安全性证明 *)

<1>2. Spec => LivenessProperty
    (* 活性证明 *)

<1>3. QED BY <1>1, <1>2
```

### 4.4 容错证明模式

```tla
(* 故障恢复的规范性 *)
RecoveryCorrectness ==
    \A w \in Workers :
        w \in failedWorkers
        ~> (w \in recoveredWorkers /\ StateConsistent(w))

(* 证明恢复保持一致性 *)
THEOREM RecoveryPreservesConsistency ==
    Spec => RecoveryCorrectness
```

---

## 5. 自动化工具链

### 5.1 定理证明自动化脚本

```bash
# 运行完整验证
python .scripts/theorem-prover-automation.py

# 仅检查Coq证明
python .scripts/theorem-prover-automation.py --coq-only

# 仅检查TLA+模型
python .scripts/theorem-prover-automation.py --tla-only

# 获取证明建议
python .scripts/theorem-prover-automation.py --suggest formal-methods/coq/streaming-theorems.v
```

### 5.2 CI/CD集成

`.github/workflows/formal-verification.yml`:

```yaml
name: Formal Verification

on:
  push:
    paths:
      - 'formal-methods/**/*.v'
      - 'formal-methods/**/*.tla'
  pull_request:
    paths:
      - 'formal-methods/**/*.v'
      - 'formal-methods/**/*.tla'

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Coq
        uses: coq-community/setup-coq@v1
        with:
          coq-version: '8.17'
      
      - name: Setup TLA+
        run: |
          wget https://github.com/tlaplus/tlaplus/releases/download/v1.7.1/tla2tools.jar
      
      - name: Run Verification
        run: python .scripts/theorem-prover-automation.py --verbose
      
      - name: Upload Results
        uses: actions/upload-artifact@v3
        with:
          name: verification-reports
          path: reports/formal-verification/
```

### 5.3 覆盖率报告

```bash
# 生成证明覆盖率报告
python .scripts/theorem-prover-automation.py --coverage

# 输出格式:
# {
#   "coq": {
#     "total_theorems": 15,
#     "proved": 12,
#     "admitted": 3,
#     "coverage": 80.0
#   },
#   "tla": {
#     "total_properties": 8,
#     "verified": 8,
#     "coverage": 100.0
#   }
# }
```

---

## 6. 引用参考

[^1]: Y. Bertot and P. Castéran, "Interactive Theorem Proving and Program Development", Springer, 2004.
[^2]: L. Lamport, "Specifying Systems", Addison-Wesley, 2002.
[^3]: T. Akidau et al., "The Dataflow Model", PVLDB, 8(12), 2015.
[^4]: P. Carbone et al., "Apache Flink: Stream and Batch Processing in a Single Engine", IEEE Data Engineering Bulletin, 2015.
[^5]: M. Kleppmann, "Designing Data-Intensive Applications", O'Reilly, 2017.
[^6]: Coq Reference Manual: https://coq.inria.fr/refman/
[^7]: TLA+ Home Page: https://lamport.azurewebsites.net/tla/tla.html
