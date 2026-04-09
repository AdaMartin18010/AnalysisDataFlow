# Coq证明助手教程

> **所属教程**: Tools/Tutorials | **预计学习时间**: 6-8小时 | **前置知识**: 基本逻辑、函数式编程

## 概述

Coq是基于归纳构造演算(CIC)的证明助手，支持交互式定理证明和程序提取。本教程将带您从基础概念到独立完成正确性证明。

## 学习目标

完成本教程后，您将能够：

1. 理解Coq的基本概念和语法
2. 编写归纳定义和递归函数
3. 使用 tactics 进行交互式证明
4. 证明函数的正确性
5. 提取可执行代码

---

## 第1部分：环境搭建（30分钟）

### 1.1 安装Coq

**使用OPAM安装（推荐）**:

```bash
# 安装OPAM (如未安装)
# macOS: brew install opam
# Ubuntu: apt install opam

# 初始化OPAM
opam init
opam switch create coq 4.14.0
eval $(opam env)

# 安装Coq
opam install coq

# 验证安装
coqtop --version
```

**安装CoqIDE（可选）**:

```bash
opam install coqide
```

**安装VS Code扩展（推荐）**:

- VSCoq (官方扩展)

### 1.2 首个Coq会话

创建文件 `hello.v`：

```coq
(* 基本定义 *)
Definition my_number : nat := 42.
Definition my_message : string := "Hello, Coq!".

(* 计算 *)
Compute my_number + 8.
Compute 2 + 3.

(* 检查类型 *)
Check my_number.
Check nat.
Check Set.
```

**交互式执行**:

```bash
coqtop -l hello.v
```

或在CoqIDE中逐步执行（Ctrl+↓ / Ctrl+→）。

---

## 第2部分：基本定义与归纳类型（1.5小时）

### 2.1 归纳定义

**布尔类型**:

```coq
Inductive bool : Set :=
  | true : bool
  | false : bool.

(* 布尔函数 *)
Definition negb (b : bool) : bool :=
  match b with
  | true => false
  | false => true
  end.

Definition andb (b1 b2 : bool) : bool :=
  match b1 with
  | true => b2
  | false => false
  end.

Definition orb (b1 b2 : bool) : bool :=
  match b1 with
  | true => true
  | false => b2
  end.

(* 测试 *)
Compute (andb true false).
```

**练习1**: 实现 `xorb`（异或）并测试所有输入组合。

### 2.2 自然数

```coq
(* 标准库的自然数定义 *)
Inductive nat : Set :=
  | O : nat
  | S : nat -> nat.

(* 递归函数 *)
Fixpoint plus (n m : nat) : nat :=
  match n with
  | O => m
  | S n' => S (plus n' m)
  end.

Fixpoint mult (n m : nat) : nat :=
  match n with
  | O => O
  | S n' => plus m (mult n' m)
  end.

Fixpoint factorial (n : nat) : nat :=
  match n with
  | O => S O  (* 1 *)
  | S n' => mult (S n') (factorial n')
  end.

(* 中缀记号 *)
Notation "x + y" := (plus x y).
Notation "x * y" := (mult x y).

Compute (3 + 4).
Compute (factorial 5).
```

### 2.3 列表

```coq
Inductive list (A : Type) : Type :=
  | nil : list A
  | cons : A -> list A -> list A.

Arguments nil {A}.
Arguments cons {A} _ _.

Notation "x :: l" := (cons x l).
Notation "[ ]" := nil.
Notation "[ x ; .. ; y ]" := (cons x .. (cons y nil) ..).

(* 列表操作 *)
Fixpoint length {A : Type} (l : list A) : nat :=
  match l with
  | [] => O
  | _ :: l' => S (length l')
  end.

Fixpoint app {A : Type} (l1 l2 : list A) : list A :=
  match l1 with
  | [] => l2
  | x :: l1' => x :: app l1' l2
  end.

Notation "l1 ++ l2" := (app l1 l2).

Fixpoint rev {A : Type} (l : list A) : list A :=
  match l with
  | [] => []
  | x :: l' => rev l' ++ [x]
  end.

Compute (rev [1; 2; 3; 4]).
```

**练习2**: 实现 `map` 和 `filter` 函数。

---

## 第3部分：命题与证明（2小时）

### 3.1 基本证明

```coq
Theorem plus_O_n : forall n : nat, O + n = n.
Proof.
  intros n.
  simpl.
  reflexivity.
Qed.

Theorem plus_n_O : forall n : nat, n + O = n.
Proof.
  intros n.
  induction n as [| n' IHn'].
  - (* n = O *)
    reflexivity.
  - (* n = S n' *)
    simpl.
    rewrite IHn'.
    reflexivity.
Qed.
```

**Tactics速查**:

| Tactic | 作用 |
|--------|------|
| `intros` | 引入假设 |
| `simpl` | 简化表达式 |
| `reflexivity` | 证明 `x = x` |
| `rewrite` | 使用等式重写 |
| `induction` | 归纳证明 |
| `destruct` | 情况分析 |
| `apply` | 应用定理/假设 |
| `unfold` | 展开定义 |

### 3.2 归纳证明练习

```coq
(* 结合律 *)
Theorem plus_assoc : forall n m p : nat,
  n + (m + p) = (n + m) + p.
Proof.
  intros n m p.
  induction n as [| n' IHn'].
  - (* n = O *)
    reflexivity.
  - (* n = S n' *)
    simpl.
    rewrite IHn'.
    reflexivity.
Qed.

(* 交换律 *)
Theorem plus_comm : forall n m : nat,
  n + m = m + n.
Proof.
  intros n m.
  induction n as [| n' IHn'].
  - (* n = O *)
    simpl.
    rewrite plus_n_O.
    reflexivity.
  - (* n = S n' *)
    simpl.
    rewrite IHn'.
    assert (H: forall x y, S (x + y) = x + S y).
    { intros x y. induction x.
      - reflexivity.
      - simpl. rewrite IHx. reflexivity. }
    rewrite H.
    reflexivity.
Qed.
```

**练习3**: 证明 `length (l1 ++ l2) = length l1 + length l2`。

### 3.3 逻辑连接词

```coq
(* 合取 *)
Theorem and_example : 3 + 4 = 7 /\ 2 * 2 = 4.
Proof.
  split.
  - reflexivity.
  - reflexivity.
Qed.

(* 析取 *)
Theorem or_example : 3 + 4 = 7 \/ 3 + 4 = 8.
Proof.
  left.
  reflexivity.
Qed.

(* 蕴含 *)
Theorem impl_example : forall n m : nat,
  n = m -> n + n = m + m.
Proof.
  intros n m H.
  rewrite H.
  reflexivity.
Qed.

(* 存在量词 *)
Theorem ex_example : exists n : nat, n + n = 4.
Proof.
  exists 2.
  reflexivity.
Qed.
```

---

## 第4部分：数据结构验证（2小时）

### 4.1 二叉搜索树

```coq
(* 有序列表 *)
Inductive ordered : list nat -> Prop :=
  | ordered_nil : ordered []
  | ordered_one : forall x, ordered [x]
  | ordered_cons : forall x y l,
      x <= y -> ordered (y :: l) -> ordered (x :: y :: l).

(* 二叉树 *)
Inductive tree : Type :=
  | Leaf : tree
  | Node : tree -> nat -> tree -> tree.

(* 中序遍历 *)
Fixpoint inorder (t : tree) : list nat :=
  match t with
  | Leaf => []
  | Node l x r => inorder l ++ [x] ++ inorder r
  end.

(* BST性质 *)
Inductive bst : tree -> Prop :=
  | bst_leaf : bst Leaf
  | bst_node : forall l x r,
      (forall y, In y (inorder l) -> y < x) ->
      (forall y, In y (inorder r) -> y > x) ->
      bst l -> bst r -> bst (Node l x r).

(* 查找 *)
Fixpoint find (x : nat) (t : tree) : bool :=
  match t with
  | Leaf => false
  | Node l y r =>
      if x <? y then find x l
      else if y <? x then find x r
      else true
  end.
```

### 4.2 插入与正确性证明

```coq
Fixpoint insert (x : nat) (t : tree) : tree :=
  match t with
  | Leaf => Node Leaf x Leaf
  | Node l y r =>
      if x <? y then Node (insert x l) y r
      else if y <? x then Node l y (insert x r)
      else t
  end.

(* 辅助引理：插入不改变其他元素 *)
Lemma inorder_insert : forall x t,
  ordered (inorder t) ->
  inorder (insert x t) = insert_sorted x (inorder t).
Admitted. (* 练习：完成证明 *)

(* BST插入保持性质 *)
Theorem insert_bst : forall x t,
  bst t -> bst (insert x t).
Proof.
  intros x t H.
  induction H.
  - (* Leaf *)
    simpl. apply bst_node.
    + intros y H. inversion H.
    + intros y H. inversion H.
    + apply bst_leaf.
    + apply bst_leaf.
  - (* Node *)
    simpl.
    destruct (x <? n) eqn:E1.
    + apply bst_node.
      * intros y H. admit.
      * intros y H. admit.
      * apply IHbst1.
      * apply bst_node; assumption.
    + destruct (n <? x) eqn:E2.
      * apply bst_node.
        -- intros y H. admit.
        -- intros y H. admit.
        -- apply bst_node; assumption.
        -- apply IHbst2.
      * assumption.
Admitted.
```

**练习4**: 完成 `insert_bst` 的证明。

### 4.3 排序算法验证

```coq
(* 选择排序 *)
Fixpoint select_min (x : nat) (l : list nat) : nat * list nat :=
  match l with
  | [] => (x, [])
  | y :: l' =>
      let (m, rest) := select_min y l' in
      if x <=? m then (x, m :: rest) else (m, x :: rest)
  end.

Fixpoint selection_sort (l : list nat) : list nat :=
  match l with
  | [] => []
  | x :: l' =>
      let (m, rest) := select_min x l' in
      m :: selection_sort rest
  end.

(* 排序正确性 *)
Definition is_sorted (l : list nat) : Prop :=
  forall i j, i < j < length l -> nth i l 0 <= nth j l 0.

Definition is_permutation (l1 l2 : list nat) : Prop :=
  forall x, count_occ Nat.eq_dec l1 x = count_occ Nat.eq_dec l2 x.

Theorem selection_sort_correct : forall l,
  is_sorted (selection_sort l) /\ is_permutation l (selection_sort l).
Proof.
  (* 练习：完成此证明 *)
Admitted.
```

---

## 第5部分：高级主题（1小时）

### 5.1 类型类

```coq
Class Eq (A : Type) := {
  eq : A -> A -> bool;
  eq_refl : forall x, eq x x = true;
  eq_sym : forall x y, eq x y = eq y x;
}.

Instance nat_Eq : Eq nat := {
  eq := Nat.eqb;
  eq_refl := Nat.eqb_refl;
  eq_sym := fun x y => eq_sym x y
}.

Definition eqb {A} `{Eq A} (x y : A) : bool := eq x y.
```

### 5.2 程序提取

```coq
Require Extraction.

(* 提取为OCaml *)
Extraction Language OCaml.

Extraction "sort.ml" selection_sort.

(* 提取为Haskell *)
Extraction Language Haskell.
Extraction "sort.hs" selection_sort.
```

### 5.3 自动化

```coq
(* 自定义tactic *)
Ltac simplify :=
  intros;
  simpl;
  try reflexivity;
  try auto;
  try omega.

(* 使用 *)
Theorem test : 1 + 1 = 2.
Proof. simplify. Qed.

(* 证明搜索 *)
Theorem auto_example : forall n m, n + m = m + n.
Proof.
  intros. auto with arith.
Qed.
```

---

## 综合练习：形式化验证栈

### 任务

定义一个栈数据结构，并验证其操作满足规范。

**要求**:

1. 定义栈ADT
2. 实现 push/pop/peek/is_empty
3. 证明栈公理（如 pop(push(x, s)) = s）
4. 提取可执行代码

**参考答案框架**:

```coq
Module Stack.

  Section StackDef.
    Variable A : Type.

    Definition stack : Type := list A.

    Definition empty : stack := [].

    Definition push (x : A) (s : stack) : stack := x :: s.

    Definition pop (s : stack) : option (A * stack) :=
      match s with
      | [] => None
      | x :: s' => Some (x, s')
      end.

    Definition peek (s : stack) : option A :=
      match s with
      | [] => None
      | x :: _ => Some x
      end.

    Definition is_empty (s : stack) : bool :=
      match s with
      | [] => true
      | _ => false
      end.

    (* 公理 *)
    Theorem push_pop : forall x s,
      pop (push x s) = Some (x, s).
    Proof.
      reflexivity.
    Qed.

    Theorem push_peek : forall x s,
      peek (push x s) = Some x.
    Proof.
      reflexivity.
    Qed.

    Theorem empty_is_empty :
      is_empty empty = true.
    Proof.
      reflexivity.
    Qed.

    Theorem push_not_empty : forall x s,
      is_empty (push x s) = false.
    Proof.
      reflexivity.
    Qed.

  End StackDef.

End Stack.

(* 提取 *)
Require Extraction.
Extraction Language OCaml.
Extraction "stack.ml" Stack.
```

---

## 总结

### 关键概念回顾

1. **归纳类型**: 定义数据的基础
2. **递归函数**: 结构递归保证终止
3. **交互式证明**: tactics驱动的证明构造
4. **程序提取**: 证明到代码的转换

### 进一步学习资源

- [Software Foundations](https://softwarefoundations.cis.upenn.edu/) - 系列教材
- [Coq'Art](https://www.labri.fr/perso/casteran/CoqArt/) - 经典教程
- [Coq Reference Manual](https://coq.inria.fr/refman/)

### 常用命令速查

| 命令 | 作用 |
|------|------|
| `coqtop` | 交互式解释器 |
| `coqc` | 编译Coq文件 |
| `coqide` | IDE |
| `coq_makefile` | 生成Makefile |

---

*本教程基于 Coq 8.16+ 版本编写*
