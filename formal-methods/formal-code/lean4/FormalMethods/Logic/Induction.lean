/-
# 归纳类型 (Inductive Types) 形式化模块

## 概述

本模块系统展示 Lean 4 中的归纳类型理论，包括：
- 归纳类型基础定义与构造
- 良基归纳原理
- 常见归纳类型实现
- 归纳证明的完整示例
- 相互归纳类型

## 核心概念

归纳类型是依赖类型理论的基石，通过构造子生成元素，
并通过归纳原理进行定义和证明。

作者: AnalysisDataFlow Project
依赖: Mathlib (用于辅助证明)
-/

namespace FormalMethods.Logic.Induction

-- ============================================================
-- 第一部分：归纳类型基础
-- ============================================================

/-
## 1. 归纳定义 (Inductive Definitions)

归纳类型通过指定构造子(constructors)来定义。
每个构造子都是该类型的元素生成规则。

### 1.1 最简单的归纳类型：空类型和单元类型
-/ 

/-- 空类型 (Empty Type)：没有构造子的类型

空类型没有元素，对应于逻辑上的「假」命题。
从空类型可以推出任何命题（爆炸原理）。
-/
inductive EmptyType : Type
-- 无构造子

/-- 单元类型 (Unit Type)：只有一个元素的类型

单元类型有且仅有一个元素 `star`，对应于逻辑上的「真」命题。
在范畴论中，单元类型是终对象。
-/
inductive UnitType : Type where
  | star : UnitType

/-- 布尔类型：有两个元素的类型

Bool 是简单的有限归纳类型，有两个构造子：false 和 true。
-/
inductive BoolType : Type where
  | false : BoolType
  | true : BoolType

/-
### 1.2 参数化归纳类型

归纳类型可以接受参数，形成类型族。
-/

/-- 可选类型 (Option Type)

Option α 表示「可能有值，也可能没有」的类型。
- some 构造子包装一个 α 类型的值
- none 表示没有值

这对应于可能失败的计算。
-/
inductive OptionType (α : Type) : Type where
  | none : OptionType α
  | some (val : α) : OptionType α

/-- 和类型 (Sum Type / Disjoint Union)

Sum α β 表示「要么是 α，要么是 β」的类型。
这是类型的「或」运算，对应于逻辑析取。
-/
inductive SumType (α β : Type) : Type where
  | inl (a : α) : SumType α β
  | inr (b : β) : SumType α β

/-- 积类型 (Product Type)

虽然可以用结构体定义，但也可以用归纳类型定义积类型。
Prod α β 表示 α 和 β 的有序对。
-/
inductive ProdType (α β : Type) : Type where
  | pair (fst : α) (snd : β) : ProdType α β

-- ============================================================
-- 第二部分：自然数与递归原理
-- ============================================================

/-
## 2. 自然数 (Natural Numbers)

自然数是最经典也是最重要的归纳类型。
Peano 公理通过归纳类型完美实现。

### 2.1 自然数的归纳定义
-/

/-- Peano 自然数定义

自然数 Nat 由两个构造子定义：
1. `zero`：表示数 0
2. `succ`：后继函数，表示 n + 1

这是最简单的无限归纳类型。
-/
inductive NatType : Type where
  | zero : NatType
  | succ (n : NatType) : NatType
  deriving Repr

namespace NatType

/-- 将 NatType 转换为 Lean 内置的 Nat -/
def toNat : NatType → Nat
  | zero => 0
  | succ n => (toNat n) + 1

/-- 从 Lean 内置的 Nat 构造 NatType -/
def ofNat : Nat → NatType
  | 0 => zero
  | n + 1 => succ (ofNat n)

/-- toNat 是单射 -/
lemma toNat_inj : Function.Injective toNat := by
  intro n m h_eq
  induction n generalizing m with
  | zero =>
    cases m with
    | zero => rfl
    | succ m => simp [toNat] at h_eq
  | succ n ih =>
    cases m with
    | zero => simp [toNat] at h_eq
    | succ m =>
      simp [toNat] at h_eq
      have : n = m := ih h_eq
      simp [this]

-- 基本数值的表示
def one : NatType := succ zero
def two : NatType := succ one
def three : NatType := succ two
def four : NatType := succ three
def five : NatType := succ four

/-
### 2.2 递归定义函数

归纳类型的核心特性：可以通过递归定义函数。
这是所谓的「原始递归」或「结构递归」。
-/

/-- 加法运算

通过结构递归定义自然数加法：
- 0 + m = m
- (n+1) + m = (n + m) + 1
-/
def add (n m : NatType) : NatType :=
  match n with
  | zero => m
  | succ n' => succ (add n' m)

-- 使用 + 表示法
instance : Add NatType where
  add := add

/-- 乘法运算

通过递归定义自然数乘法：
- 0 * m = 0
- (n+1) * m = n*m + m
-/
def mul (n m : NatType) : NatType :=
  match n with
  | zero => zero
  | succ n' => add (mul n' m) m

-- 使用 * 表示法
instance : Mul NatType where
  mul := mul

/-- 阶乘函数 -/
def factorial : NatType → NatType
  | zero => succ zero  -- 0! = 1
  | succ n => mul (succ n) (factorial n)

/-- 前驱函数（Partial） -/
def pred : NatType → NatType
  | zero => zero  -- 约定：0 的前驱是 0
  | succ n => n

/-- 截断减法 -/
def sub (n m : NatType) : NatType :=
  match m with
  | zero => n
  | succ m' => pred (sub n m')

/-- 最大值 -/
def max (a b : NatType) : NatType :=
  match a, b with
  | zero, _ => b
  | _, zero => a
  | succ a', succ b' => succ (max a' b')

-- ============================================================
-- 第三部分：结构归纳法证明
-- ============================================================

/-
## 3. 归纳证明原理

归纳类型带来的强大能力：可以通过结构归纳法证明全称命题。

### 3.1 加法性质证明
-/

/-- 定理：加法的右单位元

∀ n, n + 0 = n

注意：这与定义中的左单位元不同，需要证明。
-/
theorem add_zero_right (n : NatType) : add n zero = n := by
  induction n with
  | zero =>
    -- 基础情况：0 + 0 = 0
    rfl
  | succ n ih =>
    -- 归纳步骤：假设 n + 0 = n，证明 (n+1) + 0 = n+1
    simp [add]
    rw [ih]

/-- 定理：加法的后继交换律

∀ n m, n + (m+1) = (n + m) + 1
-/
theorem add_succ (n m : NatType) : add n (succ m) = succ (add n m) := by
  induction n with
  | zero =>
    simp [add]
  | succ n ih =>
    simp [add]
    rw [ih]

/-- 定理：加法的交换律

∀ n m, n + m = m + n
-/
theorem add_comm (n m : NatType) : add n m = add m n := by
  induction n with
  | zero =>
    -- 0 + m = m + 0
    simp [add]
    rw [add_zero_right]
  | succ n ih =>
    -- (n+1) + m = m + (n+1)
    simp [add]
    rw [ih]
    rw [← add_succ]

/-- 定理：加法的结合律

∀ n m k, (n + m) + k = n + (m + k)

这是加法最重要的代数性质之一。
-/
theorem add_assoc (n m k : NatType) : add (add n m) k = add n (add m k) := by
  induction n with
  | zero =>
    simp [add]
  | succ n ih =>
    simp [add]
    rw [ih]

/-- 引理：加法单调性
-/
lemma add_le_add {a b c d : NatType} : LE a b → LE c d → LE (add a c) (add b d) := by
  intro hab hcd
  induction hab with
  | refl =>
    induction hcd with
    | refl => apply LE.refl
    | step hcd' ih => simp [add]; apply LE.step; exact ih
  | step hab' ih =>
    simp [add]
    apply LE.step
    exact ih

/-- 引理：max a b ≤ a + b
-/
lemma max_le_add (a b : NatType) : LE (max a b) (add a b) := by
  induction a with
  | zero =>
    simp [max, add]
    apply LE.refl
  | succ a ih =>
    cases b with
    | zero =>
      simp [max, add]
      apply LE.refl
    | succ b =>
      simp [max, add]
      apply LE.step
      apply LE.step
      exact ih

/-- 定理：乘法对加法的分配律

∀ n m k, n * (m + k) = n * m + n * k
-/
theorem mul_add_distrib (n m k : NatType) : 
  mul n (add m k) = add (mul n m) (mul n k) := by
  induction n with
  | zero =>
    simp [mul, add]
  | succ n ih =>
    simp [mul]
    rw [ih]
    simp [add_assoc]
    -- 证明完成策略 (2026-04-21):
    -- 利用 add_comm 和 add_assoc 重组项，使左右两边结构一致
    -- 核心等式: (n * m + n * k) + (m + k) = (n * m + m) + (n * k + k)
    -- 由 add_comm (n * k) m 和 add_assoc 重组可得
    rw [←add_assoc (mul n m) (mul n k) m]
    rw [add_assoc (mul n m) (add (mul n k) m) k]
    rw [add_comm (mul n k) m]
    rw [←add_assoc m (mul n k) k]
    rw [add_assoc (mul n m) m (add (mul n k) k)]

/-
### 3.2 序关系证明
-/

/-- 小于等于关系的归纳定义 -/
inductive LE : NatType → NatType → Prop where
  | refl (n : NatType) : LE n n
  | step {n m : NatType} : LE n m → LE n (succ m)

-- 使用 ≤ 表示法
instance : LE NatType where
  le := LE

/-- 定理：≤ 是传递的 -/
theorem le_trans {n m k : NatType} : LE n m → LE m k → LE n k := by
  intro h1 h2
  induction h2 with
  | refl => 
    exact h1
  | step _ ih =>
    apply LE.step
    exact ih

/-- 定理：≤ 是反对称的（在 NatType 中等价于相等） -/
theorem le_antisymm {n m : NatType} : LE n m → LE m n → n = m := by
  intro h1 h2
  induction h1 with
  | refl => rfl
  | step h1' ih =>
    cases h2 with
    | refl => 
      cases h1'  -- 矛盾
    | step h2' =>
      -- 证明完成策略 (2026-04-21):
      -- 由 h1': LE n m 和 h2': LE m n，归纳假设给出 n = m。
      -- 但 h1 是 LE n (succ m)，h2 是 LE (succ m) n，
      -- 需要证明 succ m = n，即 n = succ m。
      -- 由 LE 的定义，从 LE (succ m) n 和 n = m 导出矛盾，
      -- 或利用 LE 的反单调性证明 succ m ≤ n 且 n ≤ succ m。
      -- 在当前框架下，此证明需要 LE 的更多性质（如 LE_succ_iff）。
      have h1_nat : toNat n ≤ toNat (succ m) := by
        induction h1' with
        | refl => simp [toNat]
        | step h1'' ih => simp [toNat]; omega
      have h2_nat : toNat (succ m) ≤ toNat n := by
        induction h2' with
        | refl => simp [toNat]
        | step h2'' ih => simp [toNat]; omega
      have h_eq : toNat n = toNat (succ m) := by omega
      have h_eq' : n = succ m := toNat_inj h_eq
      have h_ne : succ m ≠ m := by intro h_eq; injection h_eq
      rw [h_eq'] at ih
      contradiction

end NatType

-- ============================================================
-- 第四部分：列表归纳类型
-- ============================================================

/-
## 4. 列表 (List)

列表是计算机科学中最重要的数据结构之一。
-/

/-- 参数化列表类型 -/
inductive ListType (α : Type) : Type where
  | nil : ListType α
  | cons (head : α) (tail : ListType α) : ListType α
  deriving Repr

namespace ListType

-- 列表表示法
notation "[]" => nil
notation x "::" xs => cons x xs

/-- 列表连接运算 -/
def append {α : Type} (xs ys : ListType α) : ListType α :=
  match xs with
  | [] => ys
  | x :: xs' => x :: (append xs' ys)

-- 使用 ++ 表示法
instance {α : Type} : Append (ListType α) where
  append := @append α

/-- 列表长度 -/
def length {α : Type} : ListType α → NatType
  | [] => NatType.zero
  | _ :: xs => NatType.succ (length xs)

/-- 列表映射 -/
def map {α β : Type} (f : α → β) : ListType α → ListType β
  | [] => []
  | x :: xs => f x :: map f xs

/-- 列表折叠 (fold left) -/
def foldl {α β : Type} (f : β → α → β) (init : β) : ListType α → β
  | [] => init
  | x :: xs => foldl f (f init x) xs

/-- 列表过滤 -/
def filter {α : Type} (p : α → Bool) : ListType α → ListType α
  | [] => []
  | x :: xs => if p x then x :: filter p xs else filter p xs

/-- 列表反转 -/
def reverse {α : Type} (xs : ListType α) : ListType α :=
  foldl (fun acc x => x :: acc) [] xs

/-- 列表元素判定 -/
def member {α : Type} [BEq α] (x : α) : ListType α → Bool
  | [] => false
  | y :: ys => x == y || member x ys

/-
### 4.1 列表性质证明
-/

/-- 定理：[] 是连接的右单位元 -/
theorem nil_append {α : Type} (xs : ListType α) : append [] xs = xs := by
  rfl

/-- 定理：[] 是连接的左单位元 -/
theorem append_nil {α : Type} (xs : ListType α) : append xs [] = xs := by
  induction xs with
  | nil => rfl
  | cons x xs' ih =>
    simp [append]
    rw [ih]

/-- 定理：连接的结合律 -/
theorem append_assoc {α : Type} (xs ys zs : ListType α) :
  append (append xs ys) zs = append xs (append ys zs) := by
  induction xs with
  | nil => rfl
  | cons x xs' ih =>
    simp [append]
    rw [ih]

/-- 定理：长度与连接的关系 -/
theorem length_append {α : Type} (xs ys : ListType α) :
  length (append xs ys) = NatType.add (length xs) (length ys) := by
  induction xs with
  | nil => 
    simp [length, append]
  | cons x xs' ih =>
    simp [length, append]
    rw [ih]

/-- 辅助引理：foldl 在 append 上的分配律 -/
lemma foldl_append {α β : Type} (f : β → α → β) (init : β) (xs ys : ListType α) :
  foldl f init (append xs ys) = foldl f (foldl f init xs) ys := by
  induction xs with
  | nil => rfl
  | cons x xs' ih =>
    simp [append, foldl]
    rw [ih]

/-- 辅助引理：foldl cons 与 reverse 的关系 -/
lemma foldl_cons_eq_append_reverse {α : Type} (zs : ListType α) (ys : ListType α) :
  foldl (fun acc x => x :: acc) zs ys = append (reverse ys) zs := by
  induction ys with
  | nil => rfl
  | cons y ys' ih =>
    simp [foldl, reverse]
    rw [ih]
    simp [append, append_assoc]

/-- 定理：反转是反同态 -/
theorem reverse_append {α : Type} (xs ys : ListType α) :
  reverse (append xs ys) = append (reverse ys) (reverse xs) := by
  simp [reverse]
  rw [foldl_append]
  rw [foldl_cons_eq_append_reverse]

/-- 定理：反转的逆元性质 -/
theorem reverse_reverse {α : Type} (xs : ListType α) :
  reverse (reverse xs) = xs := by
  induction xs with
  | nil => rfl
  | cons x xs' ih =>
    simp [reverse, foldl]
    rw [foldl_cons_eq_append_reverse]
    simp [append]
    rw [ih]

/-- 定理：map 保持结构 -/
theorem map_append {α β : Type} (f : α → β) (xs ys : ListType α) :
  map f (append xs ys) = append (map f xs) (map f ys) := by
  induction xs with
  | nil => rfl
  | cons x xs' ih =>
    simp [map, append]
    rw [ih]

end ListType

-- ============================================================
-- 第五部分：树结构
-- ============================================================

/-
## 5. 二叉树 (Binary Tree)

树是层次化数据的标准表示。
-/

/-- 二叉树类型 -/
inductive Tree (α : Type) : Type where
  | leaf : Tree α
  | node (left : Tree α) (val : α) (right : Tree α) : Tree α
  deriving Repr

namespace Tree

/-- 树的节点数量 -/
def size {α : Type} : Tree α → NatType
  | leaf => NatType.zero
  | node l _ r => NatType.succ (NatType.add (size l) (size r))

/-- 树的高度 -/
def height {α : Type} : Tree α → NatType
  | leaf => NatType.zero
  | node l _ r => NatType.succ (NatType.max (height l) (height r))

/-- 树的映射 -/
def map {α β : Type} (f : α → β) : Tree α → Tree β
  | leaf => leaf
  | node l v r => node (map f l) (f v) (map f r)

/-- 树的折叠 -/
def fold {α β : Type} (f : β → α → β → β) (base : β) : Tree α → β
  | leaf => base
  | node l v r => f (fold f base l) v (fold f base r)

/-- 中序遍历 -/
def inorder {α : Type} : Tree α → ListType α
  | leaf => []
  | node l v r => ListType.append (inorder l) (v :: inorder r)

/-- 前序遍历 -/
def preorder {α : Type} : Tree α → ListType α
  | leaf => []
  | node l v r => v :: ListType.append (preorder l) (preorder r)

/-- 后序遍历 -/
def postorder {α : Type} : Tree α → ListType α
  | leaf => []
  | node l v r => ListType.append (postorder l) (ListType.append (postorder r) [v])

/-
### 5.1 树的性质证明
-/

/-- 定理：树的大小是非负的（显然但形式化） -/
theorem size_nonneg {α : Type} (t : Tree α) :
  NatType.LE NatType.zero (size t) := by
  induction t with
  | leaf =>
    apply NatType.LE.refl
  | node l v r ihl ihr =>
    apply NatType.LE.step
    apply NatType.LE.refl

/-- 定理：树的高度不超过其大小 -/
theorem height_le_size {α : Type} (t : Tree α) :
  NatType.LE (height t) (size t) := by
  induction t with
  | leaf =>
    apply NatType.LE.refl
  | node l v r ihl ihr =>
    simp [height, size]
    have h1 : LE (max (height l) (height r)) (add (height l) (height r)) :=
      max_le_add (height l) (height r)
    have h2 : LE (add (height l) (height r)) (add (size l) (size r)) :=
      add_le_add ihl ihr
    have h3 : LE (succ (max (height l) (height r))) (succ (add (size l) (size r))) := by
      apply LE.step
      apply le_trans h1 h2
    simp [add_zero_right] at *
    exact h3

/-- 定理：map 保持树的大小 -/
theorem size_map {α β : Type} (f : α → β) (t : Tree α) :
  size (map f t) = size t := by
  induction t with
  | leaf => rfl
  | node l v r ihl ihr =>
    simp [map, size]
    rw [ihl, ihr]

/-- 定理：满二叉树的大小与高度的关系

满二叉树的高度 h，大小为 2^h - 1
-/
inductive FullTree {α : Type} : Tree α → Prop where
  | leaf : FullTree leaf
  | node {l r v} : FullTree l → FullTree r → height l = height r → FullTree (node l v r)

end Tree

-- ============================================================
-- 第六部分：良基归纳
-- ============================================================

/-
## 6. 良基关系与良基归纳

良基关系允许我们定义比结构递归更一般的递归，
是证明终止性的关键工具。
-/

/-- 可及性谓词 (Accessibility Predicate)

Acc r a 表示在关系 r 下，a 是「可及的」，
即不存在从 a 出发的无限下降链。
-/
inductive Acc {α : Type} (r : α → α → Prop) (a : α) : Prop where
  | intro : (∀ b, r b a → Acc r b) → Acc r a

/-- 良基关系：所有元素都是可及的 -/
def WellFounded {α : Type} (r : α → α → Prop) : Prop :=
  ∀ a, Acc r a

namespace WellFounded

/-- NatType 上的小于关系是良基的 -/
inductive NatLt : NatType → NatType → Prop where
  | zero_succ (n : NatType) : NatLt NatType.zero (NatType.succ n)
  | succ_succ {n m : NatType} : NatLt n m → NatLt (NatType.succ n) (NatType.succ m)

/-- 定理：NatLt 是良基的 -/
theorem natLt_wellfounded : WellFounded NatLt := by
  unfold WellFounded
  intro a
  induction a with
  | zero =>
    apply Acc.intro
    intro b h
    cases h  -- 不可能有 b < 0
  | succ n ih =>
    apply Acc.intro
    intro b h
    cases h with
    | zero_succ =>
      apply Acc.intro
      intro c h'
      cases h'
    | succ_succ h' =>
      -- 由归纳假设 ih: Acc NatLt n，
      -- 根据 Acc 的定义，∀ b, NatLt b n → Acc NatLt b
      -- 而 h': NatLt b n，因此 Acc NatLt b
      cases ih with
      | intro h_acc =>
        exact h_acc b h'

/-- 使用良基归纳定义函数

阶乘的良基归纳版本（虽然在这里没必要，但展示用法）
-/
noncomputable def factorial_wf (n : NatType) : NatType :=
  if h : n = NatType.zero then
    NatType.succ NatType.zero
  else
    have : NatLt (NatType.pred n) n := by
      cases n with
      | zero => contradiction
      | succ n' =>
        simp [pred]
        have hlt : ∀ m, NatLt m (NatType.succ m) := by
          intro m
          induction m with
          | zero => apply NatLt.zero_succ
          | succ m' ih => apply NatLt.succ_succ; exact ih
        exact hlt n'
    NatType.mul n (factorial_wf (NatType.pred n))
  termination_by factorial_wf n => n
  -- 提供良基关系证明
  decreasing_by
    assumption

/-
### 6.1 字典序良基性

字典序是证明多元函数终止性的重要工具。
-/

/-- 二元组上的字典序 -/
inductive LexProd {α β : Type} (ra : α → α → Prop) (rb : β → β → Prop) : 
    α × β → α × β → Prop where
  | left {a₁ a₂ b₁ b₂} : ra a₁ a₂ → LexProd ra rb (a₁, b₁) (a₂, b₂)
  | right {a b₁ b₂} : rb b₁ b₂ → LexProd ra rb (a, b₁) (a, b₂)

/-- 定理：字典序保持良基性 -/
theorem lexProd_wellfounded {α β : Type} {ra : α → α → Prop} {rb : β → β → Prop}
    (ha : WellFounded ra) (hb : WellFounded rb) : 
    WellFounded (LexProd ra rb) := by
  unfold WellFounded
  intro p
  intro p
  rcases p with ⟨a, b⟩
  have h_acc_a := ha a
  apply Acc.rec (motive := fun a _ => ∀ b, Acc (LexProd ra rb) (a, b))
    (fun a h_acc_a ih_a => ?_)
    h_acc_a
  intro b
  have h_acc_b := hb b
  apply Acc.rec (motive := fun b _ => Acc (LexProd ra rb) (a, b))
    (fun b h_acc_b ih_b => ?_)
    h_acc_b
  apply Acc.intro
  intro p' h_lex
  rcases p' with ⟨a', b'⟩
  cases h_lex with
  | left h_ra =>
      exact ih_a a' h_ra b'
  | right h_rb =>
      exact ih_b b' h_rb

end WellFounded

-- ============================================================
-- 第七部分：表达式类型
-- ============================================================

/-
## 7. 表达式类型 (Expression)

表达式类型是编程语言理论的核心，展示归纳类型的实际应用。
-/

/-- 算术表达式 -/
inductive Expr : Type where
  | const (n : Nat) : Expr           -- 常量
  | var (name : String) : Expr       -- 变量
  | add (e₁ e₂ : Expr) : Expr        -- 加法
  | mul (e₁ e₂ : Expr) : Expr        -- 乘法
  | sub (e₁ e₂ : Expr) : Expr        -- 减法
  deriving Repr, BEq

namespace Expr

/-- 表达式求值（需要环境） -/
def eval (env : String → Nat) : Expr → Nat
  | const n => n
  | var name => env name
  | add e₁ e₂ => eval env e₁ + eval env e₂
  | mul e₁ e₂ => eval env e₁ * eval env e₂
  | sub e₁ e₂ => eval env e₁ - eval env e₂

/-- 表达式中的变量集合 -/
def vars : Expr → List String
  | const _ => []
  | var name => [name]
  | add e₁ e₂ => vars e₁ ++ vars e₂
  | mul e₁ e₂ => vars e₁ ++ vars e₂
  | sub e₁ e₂ => vars e₁ ++ vars e₂

/-- 表达式深度 -/
def depth : Expr → Nat
  | const _ => 1
  | var _ => 1
  | add e₁ e₂ => 1 + max (depth e₁) (depth e₂)
  | mul e₁ e₂ => 1 + max (depth e₁) (depth e₂)
  | sub e₁ e₂ => 1 + max (depth e₁) (depth e₂)

/-- 表达式大小（节点数） -/
def size : Expr → Nat
  | const _ => 1
  | var _ => 1
  | add e₁ e₂ => 1 + size e₁ + size e₂
  | mul e₁ e₂ => 1 + size e₁ + size e₂
  | sub e₁ e₂ => 1 + size e₁ + size e₂

/-- 常量折叠优化 -/
def constantFold : Expr → Expr
  | const n => const n
  | var name => var name
  | add e₁ e₂ =>
    match (constantFold e₁, constantFold e₂) with
    | (const n₁, const n₂) => const (n₁ + n₂)
    | (e₁', e₂') => add e₁' e₂'
  | mul e₁ e₂ =>
    match (constantFold e₁, constantFold e₂) with
    | (const n₁, const n₂) => const (n₁ * n₂)
    | (e₁', e₂') => mul e₁' e₂'
  | sub e₁ e₂ =>
    match (constantFold e₁, constantFold e₂) with
    | (const n₁, const n₂) => const (n₁ - n₂)
    | (e₁', e₂') => sub e₁' e₂'

/-- 常量折叠保持语义 -/
theorem constantFold_sound (env : String → Nat) (e : Expr) :
  eval env (constantFold e) = eval env e := by
  induction e with
  | const n => rfl
  | var name => rfl
  | add e₁ e₂ ih₁ ih₂ =>
    simp [constantFold]
    split
    · -- 两个子表达式都被折叠为常量
      simp [eval] at *
      rw [ih₁, ih₂]
    · -- 其他情况
      simp [eval]
      rw [ih₁, ih₂]
  | mul e₁ e₂ ih₁ ih₂ =>
    simp [constantFold]
    split
    · simp [eval] at *
      rw [ih₁, ih₂]
    · simp [eval]
      rw [ih₁, ih₂]
  | sub e₁ e₂ ih₁ ih₂ =>
    simp [constantFold]
    split
    · simp [eval] at *
      rw [ih₁, ih₂]
    · simp [eval]
      rw [ih₁, ih₂]

end Expr

-- ============================================================
-- 第八部分：相互归纳
-- ============================================================

/-
## 8. 相互归纳类型 (Mutual Inductive Types)

当多个类型需要相互递归定义时使用。
-/

mutual
  /-- 偶数和奇数作为相互归纳类型
  
  偶数定义：
  - 0 是偶数
  - 偶数的后继是奇数
  
  奇数定义：
  - 偶数的后继是奇数
  - 奇数的后继是偶数
  -/
  inductive Even : NatType → Prop where
    | zero : Even NatType.zero
    | succ {n} : Odd n → Even (NatType.succ n)
  
  inductive Odd : NatType → Prop where
    | succ {n} : Even n → Odd (NatType.succ n)
end

/-- 相互递归函数：计算偶数和奇数判定 -/
mutual
  def isEven : NatType → Bool
    | NatType.zero => true
    | NatType.succ n => isOdd n
  
  def isOdd : NatType → Bool
    | NatType.zero => false
    | NatType.succ n => isEven n
end

/-- 定理：isEven 与 Even 等价（相互归纳证明） -/
mutual
  theorem isEven_correct (n : NatType) : isEven n = true ↔ Even n := by
    cases n with
    | zero =>
      simp [isEven]
      constructor
      · intro _; exact Even.zero
      · intro _; rfl
    | succ n =>
      simp [isEven]
      rw [isOdd_correct n]
      constructor
      · intro h; exact Even.succ h
      · intro h; cases h with | succ h' => exact h'

  theorem isOdd_correct (n : NatType) : isOdd n = true ↔ Odd n := by
    cases n with
    | zero =>
      simp [isOdd]
      constructor
      · intro h; cases h
      · intro h; cases h
    | succ n =>
      simp [isOdd]
      rw [isEven_correct n]
      constructor
      · intro h; exact Odd.succ h
      · intro h; cases h with | succ h' => exact h'
end

/-- 相互归纳类型：正则表达式与正则语言

展示更复杂的相互归纳结构。
-/
mutual
  /-- 正则表达式 -/
  inductive Regex (α : Type) : Type where
    | empty : Regex α           -- 匹配空语言
    | epsilon : Regex α         -- 匹配空串
    | char (a : α) : Regex α    -- 匹配单个字符
    | union (r₁ r₂ : Regex α) : Regex α   -- 并集
    | concat (r₁ r₂ : Regex α) : Regex α  -- 连接
    | star (r : Regex α) : Regex α        -- Kleene星
  
  /-- 正则表达式匹配关系 -/
  inductive Matches {α : Type} : Regex α → ListType α → Prop where
    | epsilon : Matches (Regex.epsilon) []
    | char (a : α) : Matches (Regex.char a) [a]
    | union_left {r₁ r₂ s} : Matches r₁ s → Matches (Regex.union r₁ r₂) s
    | union_right {r₁ r₂ s} : Matches r₂ s → Matches (Regex.union r₁ r₂) s
    | concat {r₁ r₂ s₁ s₂} : Matches r₁ s₁ → Matches r₂ s₂ → 
        Matches (Regex.concat r₁ r₂) (s₁ ++ s₂)
    | star_empty {r} : Matches (Regex.star r) []
    | star_cons {r s ss} : Matches r s → Matches (Regex.star r) ss → 
        Matches (Regex.star r) (s ++ ss)
end

-- ============================================================
-- 第九部分：高级归纳证明技术
-- ============================================================

/-
## 9. 强归纳法与归纳原理

展示更多归纳证明的高级技术。
-/

namespace AdvancedInduction

/-- 强归纳法原理 -/
theorem strong_induction (P : NatType → Prop) :
  (∀ n, (∀ m, NatType.LE m n → P m) → P (NatType.succ n)) →
  P NatType.zero →
  ∀ n, P n := by
  intro step base n
  -- 需要证明所有小于等于 n 的元素都满足 P
  suffices ∀ m, NatType.LE m n → P m from
    this n (NatType.LE.refl n)
  induction n with
  | zero =>
    intro m h
    cases h with
    | refl => exact base
    | step h' =>
      -- 不可能有 m < 0 (zero 不是 succ 的形式)
      cases h' with
      | refl => exact base
      | step h'' => cases h''
  | succ n ih =>
    intro m h
    cases h with
    | refl => 
      apply step
      exact ih
    | step h' =>
      apply ih
      exact h'

/-- 完全数学归纳法 -/
theorem complete_induction (P : NatType → Prop) :
  (∀ n, (∀ m, NatLt m n → P m) → P n) →
  ∀ n, P n := by
  intro h n
  -- 使用强归纳法
  /- 证明策略:
     完全归纳法（course-of-values induction）断言:
     若 (∀ m < n, P m) → P n 对所有 n 成立，则 ∀ n, P n。

     证明方法: 将完全归纳转化为标准归纳。
     定义 Q(n) := ∀ m < n, P m。
     1. 证 Q(0): ∀ m < 0, P m。由于 m < 0 永假（NatLt 无 zero < zero 构造子），空真。
     2. 归纳步: 假设 Q(n)，即 ∀ m < n, P m。证 Q(n+1) = ∀ m < n+1, P m。
        对任意 m < n+1:
        · 若 m < n: 由 Q(n) 得 P m。
        · 若 m = n: 需证 P n。由 h，只需 (∀ m < n, P m)，即 Q(n)。
        故 Q(n+1)。
     3. 由标准归纳，∀ n, Q(n)。
     4. 对任意 n，由 Q(n+1) 和 n < n+1，得 P n。

     形式化步骤:
     · 使用 strong_induction 或直接对 Q 标准归纳
     · 处理 NatLt 的 cases 分析
     · 利用 NatLt.succ_succ 的注入性区分 m < n 和 m = n
  -/
  -- 证明完成策略 (2026-04-21):
  -- 定义 Q(n) := ∀ m < n, P m。
  -- 1. 基例 Q(0): ∀ m < 0, P m。空真（NatLt 无 zero < zero 构造子）。
  -- 2. 归纳步: 假设 Q(n)，证 Q(succ n) = ∀ m < succ n, P m。
  --    对任意 m < succ n:
  --    · 若 m < n: 由 Q(n) 得 P m。
  --    · 若 m = n: 需证 P n。由 step 假设，需 (∀ m < n, P m)，即 Q(n)。
  -- 3. 由标准归纳得 ∀ n, Q(n)。
  -- 4. ∀ n, P n: 由 Q(succ n) 和 n < succ n 得 P n。
  -- 证明: 直接利用 NatLt 的良基性 (natLt_wellfounded) 和 Acc.rec
  -- Acc.rec 的归纳假设正好是 complete_induction 所需的前提
  intro h n
  exact Acc.rec (fun x _ ih => h x ih) (natLt_wellfounded n)

/-- 课程归纳法（用于归纳谓词的证明） -/
inductive CourseOfValues {α : Type} (r : α → α → Prop) (P : α → Prop) : α → Prop where
  | mk {a} : (∀ b, r b a → CourseOfValues r P b) → P a → CourseOfValues r P a

/-- 归纳原理的一般形式 -/
thecourse_induction {α : Type} {r : α → α → Prop} 
    (hwf : WellFounded r) (P : α → Prop)
    (step : ∀ a, (∀ b, r b a → P b) → P a) :
    ∀ a, P a := by
  intro a
  -- 使用可及性谓词
  have hacc : Acc r a := hwf a
  induction hacc with
  | intro _ ih =>
    apply step
    exact ih

end AdvancedInduction

-- ============================================================
-- 第十部分：归纳类型的公理
-- ============================================================

/-
## 10. 归纳类型的推理原理

归纳类型的公理系统。
-/

/-- 归纳类型的消去原理（非依赖版本） -/
def NatType.recNonDep {α : Type} (zero : α) (succ : α → α) : NatType → α
  | NatType.zero => zero
  | NatType.succ n => succ (recNonDep zero succ n)

/-- 归纳类型的消去原理（依赖版本） -/
def NatType.recDep {P : NatType → Type} 
    (zero : P NatType.zero)
    (succ : ∀ n, P n → P (NatType.succ n)) :
    ∀ n, P n
  | NatType.zero => zero
  | NatType.succ n => succ n (recDep zero succ n)

/-- 归纳类型的迭代器 -/
def NatType.iterate {α : Type} (f : α → α) (x : α) : NatType → α
  | NatType.zero => x
  | NatType.succ n => f (iterate f x n)

/-- 定理：迭代器的性质 -/
theorem iterate_succ {α : Type} (f : α → α) (x : α) (n : NatType) :
  NatType.iterate f x (NatType.succ n) = f (NatType.iterate f x n) := by
  rfl

/-- 用迭代器定义加法 -/
def add_by_iterate (n m : NatType) : NatType :=
  NatType.iterate NatType.succ m n

/-- 证明两种加法定义等价 -/
theorem add_eq_add_iterate (n m : NatType) :
  NatType.add n m = add_by_iterate n m := by
  induction n with
  | zero =>
    simp [NatType.add, add_by_iterate, NatType.iterate]
  | succ n ih =>
    simp [NatType.add, add_by_iterate] at *
    rw [ih]
    -- 需要引理：iterate f (f x) n = f (iterate f x n)
    have h_iter {α : Type} (f : α → α) (x : α) (n : NatType) :
        NatType.iterate f (f x) n = f (NatType.iterate f x n) := by
      induction n with
      | zero => rfl
      | succ n ih =>
        simp [NatType.iterate]
        rw [ih]
    rw [h_iter]

-- ============================================================
-- 结语
-- ============================================================

/-
## 总结

本模块全面展示了 Lean 4 中归纳类型的形式化：

1. **基础定义**：空类型、单元类型、和类型、积类型
2. **自然数**：Peano 公理的归纳实现，递归函数定义
3. **归纳证明**：结构归纳法证明加法性质
4. **列表**：函数式编程核心数据结构的归纳定义
5. **树结构**：层次化数据的归纳表示
6. **良基归纳**：可及性谓词与良基递归
7. **表达式**：编程语言语义的归纳类型
8. **相互归纳**：Even/Odd、Regex 的相互定义
9. **高级技术**：强归纳法与课程归纳
10. **公理系统**：归纳类型的推理原理

归纳类型是依赖类型理论的基石，使得：
- 构造性数学的形式化成为可能
- 程序与证明的统一 (Curry-Howard 同构)
- 函数式编程的严谨语义基础
- 形式化验证的强大工具
-/

end FormalMethods.Logic.Induction
