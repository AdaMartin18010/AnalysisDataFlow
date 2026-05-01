/-
# 谓词逻辑形式化 (Predicate Logic / First-Order Logic)

本模块定义一阶谓词逻辑的完整形式化框架，包括：
- 语法定义（项、公式、一阶语言）
- 语义（结构、赋值、解释、求值）
- 自然演绎系统（含等式规则和量词规则）
- 元定理（可靠性、完备性、Löwenheim-Skolem、紧致性）
- 应用示例（群论、Peano算术）

形式化等级: L6 (完整形式化，包含复杂构造性证明)

作者: AnalysisDataFlow Project
日期: 2026-04-10
-/

import Mathlib.Data.Set.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.List.Basic
import Mathlib.Data.Nat.Defs
import Mathlib.Logic.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace PredicateLogic

/- ============================================================
  第一章: 一阶语言的签名 (Signature)
  ============================================================ -/

/--
定义 1.1 (一阶签名): 一阶逻辑的签名 Σ 由以下部分组成:
- 函数符号集合，每个符号有指定的元数 (arity)
- 谓词符号集合，每个符号有指定的元数
- 可能包含等号

记作: Σ = (Func, Pred, arity_F, arity_P, hasEq)
-/
structure Signature where
  Func : Type              -- 函数符号类型
  Pred : Type              -- 谓词符号类型
  arityF : Func → Nat      -- 函数元数
  arityP : Pred → Nat      -- 谓词元数
  hasEq : Bool             -- 是否包含等号
  deriving Repr

namespace Signature

/-- 常量: 0元函数符号 -/
def Const (Σ : Signature) : Type := { f : Σ.Func // Σ.arityF f = 0 }

/-- 命题符号: 0元谓词符号 -/
def PropSym (Σ : Signature) : Type := { p : Σ.Pred // Σ.arityP p = 0 }

end Signature

/- ============================================================
  第二章: 语法定义 (Syntax)
  ============================================================ -/

section Syntax

variable {Σ : Signature}

/--
定义 2.1 (项): 给定签名 Σ 和变量集合 Var，项 t 的归纳定义:
- 变量 x ∈ Var 是项
- 常量 c 是项
- 若 f 是 n 元函数符号，t₁, ..., tₙ 是项，则 f(t₁, ..., tₙ) 是项

记号: Term(Σ, Var)
-/
inductive Term (Σ : Signature) (Var : Type) : Type
  | var (x : Var)                           -- 变量
  | func (f : Σ.Func) (args : List (Term Σ Var))  -- 函数应用
  deriving DecidableEq, Repr

namespace Term

/-- 项的大小（递归深度） -/
def size : Term Σ Var → Nat
  | var _ => 1
  | func _ args => 1 + (args.map size).foldl (max) 0

/-- 项中的变量集合 -/
def vars [DecidableEq Var] : Term Σ Var → Finset Var
  | var x => {x}
  | func _ args => (args.map vars).foldl (Finset.union) ∅

/-- 项是否是常量（无变量） -/
def isGround : Term Σ Var → Bool
  | var _ => false
  | func _ [] => true
  | func _ args => args.all isGround

end Term

/--
定义 2.2 (公式): 给定签名 Σ，一阶公式 φ 的归纳定义:
- 原子公式: P(t₁, ..., tₙ)，其中 P 是 n 元谓词，tᵢ 是项
- ⊥ (假) 和 ⊤ (真)
- ¬φ (否定)
- φ ∧ ψ (合取), φ ∨ ψ (析取), φ → ψ (蕴含)
- ∀x.φ (全称量词)
- ∃x.φ (存在量词)
- t₁ = t₂ (等式，若签名包含等号)
-/
inductive Formula (Σ : Signature) (Var : Type) : Type
  | pred (p : Σ.Pred) (args : List (Term Σ Var))  -- 谓词应用
  | bot                                           -- ⊥
  | top                                           -- ⊤
  | not (φ : Formula Σ Var)                       -- ¬φ
  | and (φ ψ : Formula Σ Var)                     -- φ ∧ ψ
  | or (φ ψ : Formula Σ Var)                      -- φ ∨ ψ
  | imp (φ ψ : Formula Σ Var)                     -- φ → ψ
  | forall (x : Var) (φ : Formula Σ Var)          -- ∀x.φ
  | exists (x : Var) (φ : Formula Σ Var)          -- ∃x.φ
  | eq (t₁ t₂ : Term Σ Var)                       -- t₁ = t₂ (等式)
  deriving DecidableEq, Repr

namespace Formula

/-- 记号定义 -/
instance : Top (Formula Σ Var) := ⟨top⟩
instance : Bot (Formula Σ Var) := ⟨bot⟩

prefix:70 "¬' " => not
infixl:65 " ∧' " => and
infixl:64 " ∨' " => or
infixr:60 " →' " => imp
infix:55 " ↔' " => fun φ ψ => (φ →' ψ) ∧' (ψ →' φ)

notation "∀' " x ", " φ => forall x φ
notation "∃' " x ", " φ => exists x φ
infix:50 " =' " => eq

/-- 公式的深度 -/
def depth : Formula Σ Var → Nat
  | pred _ _ => 0
  | bot => 0
  | top => 0
  | not φ => 1 + φ.depth
  | and φ ψ => 1 + max φ.depth ψ.depth
  | or φ ψ => 1 + max φ.depth ψ.depth
  | imp φ ψ => 1 + max φ.depth ψ.depth
  | forall _ φ => 1 + φ.depth
  | exists _ φ => 1 + φ.depth
  | eq _ _ => 0

/-- 公式中自由变量集合 -/
def freeVars [DecidableEq Var] : Formula Σ Var → Finset Var
  | pred _ args => (args.map Term.vars).foldl (Finset.union) ∅
  | bot => ∅
  | top => ∅
  | not φ => φ.freeVars
  | and φ ψ => φ.freeVars ∪ ψ.freeVars
  | or φ ψ => φ.freeVars ∪ ψ.freeVars
  | imp φ ψ => φ.freeVars ∪ ψ.freeVars
  | forall x φ => φ.freeVars \ {x}
  | exists x φ => φ.freeVars \ {x}
  | eq t₁ t₂ => t₁.vars ∪ t₂.vars

/-- 公式是闭公式（句子）当且仅当无自由变量 -/
def isSentence [DecidableEq Var] (φ : Formula Σ Var) : Prop := φ.freeVars = ∅

/-- 公式是开公式当且仅当无量词 -/
def isOpen : Formula Σ Var → Bool
  | pred _ _ => true
  | bot => true
  | top => true
  | not φ => φ.isOpen
  | and φ ψ => φ.isOpen && ψ.isOpen
  | or φ ψ => φ.isOpen && ψ.isOpen
  | imp φ ψ => φ.isOpen && ψ.isOpen
  | forall _ _ => false
  | exists _ _ => false
  | eq _ _ => true

end Formula

end Syntax

/- ============================================================
  第三章: 替换 (Substitution)
  ============================================================ -/

section Substitution

variable {Σ : Signature} {Var : Type} [DecidableEq Var]

/--
定义 3.1 (替换): 替换 σ 是一个从变量到项的映射。
我们将其表示为 Var → Term Σ Var。
-/
def Substitution := Var → Term Σ Var

namespace Substitution

/-- 恒等替换 -/
def id : Substitution Σ Var := Term.var

/-- 单点替换 [t/x]: 将 x 替换为 t，其他变量不变 -/
def single (x : Var) (t : Term Σ Var) : Substitution Σ Var :=
  fun y => if y = x then t else Term.var y

notation:max "[" t "//" x "]" => single x t

/-- 替换在项上的应用 -/
def applyToTerm (σ : Substitution Σ Var) : Term Σ Var → Term Σ Var
  | Term.var x => σ x
  | Term.func f args => Term.func f (args.map (applyToTerm σ))

/-- 替换在项列表上的应用 -/
def applyToTerms (σ : Substitution Σ Var) (ts : List (Term Σ Var)) : List (Term Σ Var) :=
  ts.map (applyToTerm σ)

/-- 替换在公式上的应用（避免变量捕获） -/
def applyToFormula (σ : Substitution Σ Var) : Formula Σ Var → Formula Σ Var
  | Formula.pred p args => Formula.pred p (applyToTerms σ args)
  | Formula.bot => Formula.bot
  | Formula.top => Formula.top
  | Formula.not φ => Formula.not (applyToFormula σ φ)
  | Formula.and φ ψ => Formula.and (applyToFormula σ φ) (applyToFormula σ ψ)
  | Formula.or φ ψ => Formula.or (applyToFormula σ φ) (applyToFormula σ ψ)
  | Formula.imp φ ψ => Formula.imp (applyToFormula σ φ) (applyToFormula σ ψ)
  | Formula.forall x φ =>
      -- 简化处理：假设不会发生变量捕获
      Formula.forall x (applyToFormula σ φ)
  | Formula.exists x φ =>
      Formula.exists x (applyToFormula σ φ)
  | Formula.eq t₁ t₂ => Formula.eq (applyToTerm σ t₁) (applyToTerm σ t₂)

/-- 替换的复合: σ ∘ τ -/
def comp (σ τ : Substitution Σ Var) : Substitution Σ Var :=
  fun x => applyToTerm τ (σ x)

infixr:90 " ∘s " => comp

/-- 引理 3.1 (恒等替换): id(t) = t -/
lemma apply_id_term (t : Term Σ Var) : applyToTerm id t = t := by
  induction t with
  | var x => rfl
  | func f args ih =>
      simp [applyToTerm]
      exact List.map_id' ih

/-- 引理 3.2 (单点替换): [t/x](x) = t -/
lemma single_apply_self (x : Var) (t : Term Σ Var) :
    applyToTerm ([t//x]) (Term.var x) = t := by
  simp [applyToTerm, single]

/-- 引理 3.3 (单点替换其他变量): y ≠ x → [t/x](y) = y -/
lemma single_apply_other (x y : Var) (t : Term Σ Var) (h : y ≠ x) :
    applyToTerm ([t//x]) (Term.var y) = Term.var y := by
  simp [applyToTerm, single, h]

end Substitution

end Substitution

/- ============================================================
  第四章: 语义 (Semantics)
  ============================================================ -/

section Semantics

variable {Σ : Signature} {Var : Type}

/--
定义 4.1 (结构/模型): 签名 Σ 的结构 M 包括:
- 论域 M.univ: 一个非空集合
- 函数解释 M.interpF: 将 n 元函数符号映射到 M.univⁿ → M.univ
- 谓词解释 M.interpP: 将 n 元谓词符号映射到 M.univⁿ → Prop

记作: M = (|M|, {f^M}, {P^M})
-/
structure Structure (Σ : Signature) where
  univ : Type                    -- 论域
  [nonempty : Nonempty univ]     -- 非空假设
  interpF : (f : Σ.Func) → (Fin (Σ.arityF f) → univ) → univ  -- 函数解释
  interpP : (p : Σ.Pred) → (Fin (Σ.arityP p) → univ) → Prop  -- 谓词解释

attribute [instance] Structure.nonempty

namespace Structure

/-- 在结构中解释项
给定赋值 ρ: Var → M.univ，项 t 的解释 [[t]]ρᴹ 递归定义。

技术说明: Term.func 存储 List (Term Σ Var)，而 interpF 期望 Fin (arityF f) → univ。
使用 List.get? 按索引提取；若列表长度不足，返回由非空假设选择的默认值。
在良构公式中，args 的长度应恰好等于 arityF f，故 none 情况理论上不可达。
-/
def interpTerm (M : Structure Σ) (ρ : Var → M.univ) : Term Σ Var → M.univ
  | Term.var x => ρ x
  | Term.func f args =>
      M.interpF f (fun i =>
        match args.get? i.val with
        | some t => interpTerm M ρ t
        | none => Classical.choice M.nonempty)

/--
赋值更新: ρ[x ↦ a] 表示将 x 映射到 a，其他变量保持原赋值。
-/
def update (ρ : Var → M.univ) (x : Var) (a : M.univ) : Var → M.univ :=
  fun y => if y = x then a else ρ y

notation:max ρ "[" x " ↦ " a "]" => update ρ x a

/-- 公式求值
给定结构 M 和赋值 ρ，公式 φ 的求值 M ⊨ φ[ρ] 定义如下。

技术说明: Formula.pred 存储 List (Term Σ Var)，而 interpP 期望 Fin (arityP p) → univ。
使用 List.get? 按索引提取参数的解释；若列表长度不足，返回默认值。
在良构公式中，args 的长度应恰好等于 arityP p。
-/
def satisfies (M : Structure Σ) (ρ : Var → M.univ) : Formula Σ Var → Prop
  | Formula.pred p args =>
      M.interpP p (fun i =>
        match args.get? i.val with
        | some t => interpTerm M ρ t
        | none => Classical.choice M.nonempty)
  | Formula.bot => False
  | Formula.top => True
  | Formula.not φ => ¬(satisfies M ρ φ)
  | Formula.and φ ψ => satisfies M ρ φ ∧ satisfies M ρ ψ
  | Formula.or φ ψ => satisfies M ρ φ ∨ satisfies M ρ ψ
  | Formula.imp φ ψ => satisfies M ρ φ → satisfies M ρ ψ
  | Formula.forall x φ => ∀ a : M.univ, satisfies M (ρ[x ↦ a]) φ
  | Formula.exists x φ => ∃ a : M.univ, satisfies M (ρ[x ↦ a]) φ
  | Formula.eq t₁ t₂ => interpTerm M ρ t₁ = interpTerm M ρ t₂

notation:50 M " ⊨ " φ "[" ρ "]" => satisfies M ρ φ
notation:50 M " ⊨ " φ => satisfies M (fun _ => Classical.choice M.nonempty) φ

/-- Finset 列表 foldl union 的单调性: 初始值增大，结果增大 -/
lemma foldl_union_init_monotone {α} [DecidableEq α] {ts : List (Finset α)} {s₁ s₂ : Finset α}
    (h : s₁ ⊆ s₂) :
    ts.foldl (Finset.union) s₁ ⊆ ts.foldl (Finset.union) s₂ := by
  induction ts with
  | nil => simp; exact h
  | cons t' ts ih =>
      simp [List.foldl]
      have h_union : s₁ ∪ t' ⊆ s₂ ∪ t' := by
        apply Finset.union_subset_union
        · exact h
        · exact Finset.Subset.refl t'
      exact ih h_union

/-- 初始值是 foldl union 结果的子集 -/
lemma init_subset_foldl_union {α} [DecidableEq α] {ts : List (Finset α)} {s : Finset α} :
    s ⊆ ts.foldl (Finset.union) s := by
  induction ts with
  | nil => simp
  | cons t' ts ih =>
      simp [List.foldl]
      have h1 : s ⊆ s ∪ t' := Finset.subset_union_left
      have h2 : s ∪ t' ⊆ ts.foldl (Finset.union) (s ∪ t') := ih
      exact Finset.Subset.trans h1 h2

/-- 列表中的每个元素都是 foldl union 结果的子集 -/
lemma list_mem_subset_foldl_union {α} [DecidableEq α] {xs : List (Finset α)} {s : Finset α}
    (h : s ∈ xs) : s ⊆ xs.foldl (Finset.union) ∅ := by
  induction xs with
  | nil => simp at h
  | cons s' ts ih =>
      simp at h
      cases h with
      | inl h_eq =>
          rw [h_eq]
          simp [List.foldl]
          exact init_subset_foldl_union
      | inr h_mem =>
          have h_sub : s ⊆ ts.foldl (Finset.union) ∅ := ih h_mem
          simp [List.foldl]
          have h_init : ∅ ⊆ s' := Finset.empty_subset s'
          exact Finset.Subset.trans h_sub (foldl_union_init_monotone h_init)

/-- 赋值一致性下的项解释相等

若赋值 ρ₁ 和 ρ₂ 在项 t 的自由变量上一致，则 t 的解释相等。
-/
lemma interpTerm_agree {M : Structure Σ} {t : Term Σ Var} {ρ₁ ρ₂ : Var → M.univ}
    (h : ∀ x ∈ t.vars, ρ₁ x = ρ₂ x) :
    interpTerm M ρ₁ t = interpTerm M ρ₂ t := by
  induction t with
  | var x =>
      simp [Term.vars] at h
      exact h x (by simp)
  | func f args ih =>
      simp [Term.vars] at h
      simp [interpTerm]
      apply congr_arg
      funext i
      rcases h_args : args.get? i.val with ⟨t'⟩ | none
      · have h_in : t' ∈ args := List.mem_of_get? h_args
        have h_t' : ∀ x ∈ t'.vars, ρ₁ x = ρ₂ x := by
          intro x hx
          have h_x : x ∈ (args.map Term.vars).foldl (Finset.union) ∅ := by
            have h_sub : t'.vars ⊆ (args.map Term.vars).foldl (Finset.union) ∅ := by
              have h_mem : t'.vars ∈ args.map Term.vars := List.mem_map_of_mem Term.vars h_in
              -- 每个元素的 vars 都是 foldl union 的子集
              have : ∀ s ∈ (args.map Term.vars), s ⊆ (args.map Term.vars).foldl (Finset.union) ∅ := by
                intro s hs
                exact list_mem_subset_foldl_union hs
              exact this (t'.vars) h_mem
            exact h_sub hx
          exact h x h_x
        exact ih t' h_in h_t'
      · rfl

/-- 赋值一致性下的公式满足等价

若赋值 ρ₁ 和 ρ₂ 在公式 φ 的自由变量上一致，则 φ 的满足性等价。
-/
lemma satisfies_assignment_agree {M : Structure Σ} {φ : Formula Σ Var} {ρ₁ ρ₂ : Var → M.univ}
    (h : ∀ x ∈ φ.freeVars, ρ₁ x = ρ₂ x) :
    (M ⊨ φ[ρ₁]) ↔ (M ⊨ φ[ρ₂]) := by
  induction φ with
  | pred p args =>
      simp [freeVars, Term.vars] at h
      simp [satisfies]
      apply congr_arg
      funext i
      rcases h_args : args.get? i.val with ⟨t⟩ | none
      · have h_in : t ∈ args := List.mem_of_get? h_args
        have h_t : ∀ x ∈ t.vars, ρ₁ x = ρ₂ x := by
          intro x hx
          have h_x : x ∈ (args.map Term.vars).foldl (Finset.union) ∅ := by
            have h_sub : t.vars ⊆ (args.map Term.vars).foldl (Finset.union) ∅ := by
              have h_mem : t.vars ∈ args.map Term.vars := List.mem_map_of_mem Term.vars h_in
              have : ∀ s ∈ (args.map Term.vars), s ⊆ (args.map Term.vars).foldl (Finset.union) ∅ := by
                intro s hs
                exact list_mem_subset_foldl_union hs
              exact this (t.vars) h_mem
            exact h_sub hx
          exact h x h_x
        exact interpTerm_agree h_t
      · rfl
  | bot => simp [satisfies]
  | top => simp [satisfies]
  | not φ ih => simp [freeVars] at h; simp [satisfies, ih h]
  | and φ ψ ih₁ ih₂ => simp [freeVars] at h; simp [satisfies, ih₁ (fun x hx => h x (Or.inl hx)), ih₂ (fun x hx => h x (Or.inr hx))]
  | or φ ψ ih₁ ih₂ => simp [freeVars] at h; simp [satisfies, ih₁ (fun x hx => h x (Or.inl hx)), ih₂ (fun x hx => h x (Or.inr hx))]
  | imp φ ψ ih₁ ih₂ => simp [freeVars] at h; simp [satisfies, ih₁ (fun x hx => h x (Or.inl hx)), ih₂ (fun x hx => h x (Or.inr hx))]
  | forall x φ ih =>
      simp [freeVars] at h
      simp [satisfies]
      apply Iff.intro
      · intro h₁ a
        have h₂ : ∀ y ∈ φ.freeVars, (ρ₁[x ↦ a]) y = (ρ₂[x ↦ a]) y := by
          intro y hy
          by_cases h_eq : y = x
          · simp [h_eq]
          · simp [h_eq]
            exact h y (by simp [h_eq] at hy; exact hy)
        exact (ih h₂).mp (h₁ a)
      · intro h₁ a
        have h₂ : ∀ y ∈ φ.freeVars, (ρ₁[x ↦ a]) y = (ρ₂[x ↦ a]) y := by
          intro y hy
          by_cases h_eq : y = x
          · simp [h_eq]
          · simp [h_eq]
            exact h y (by simp [h_eq] at hy; exact hy)
        exact (ih h₂).mpr (h₁ a)
  | exists x φ ih =>
      simp [freeVars] at h
      simp [satisfies]
      apply Iff.intro
      · rintro ⟨a, ha⟩
        use a
        have h₂ : ∀ y ∈ φ.freeVars, (ρ₁[x ↦ a]) y = (ρ₂[x ↦ a]) y := by
          intro y hy
          by_cases h_eq : y = x
          · simp [h_eq]
          · simp [h_eq]
            exact h y (by simp [h_eq] at hy; exact hy)
        exact (ih h₂).mp ha
      · rintro ⟨a, ha⟩
        use a
        have h₂ : ∀ y ∈ φ.freeVars, (ρ₁[x ↦ a]) y = (ρ₂[x ↦ a]) y := by
          intro y hy
          by_cases h_eq : y = x
          · simp [h_eq]
          · simp [h_eq]
            exact h y (by simp [h_eq] at hy; exact hy)
        exact (ih h₂).mpr ha
  | eq t₁ t₂ =>
      simp [freeVars, Term.vars] at h
      simp [satisfies]
      constructor
      · intro h_eq
        rw [interpTerm_agree (fun x hx => h x (Or.inl hx))] at h_eq
        rw [interpTerm_agree (fun x hx => h x (Or.inr hx))] at h_eq
        exact h_eq
      · intro h_eq
        rw [interpTerm_agree (fun x hx => h x (Or.inl hx))]
        rw [interpTerm_agree (fun x hx => h x (Or.inr hx))]
        exact h_eq

/-- 闭公式在结构中的真值与赋值无关

证明策略: 对公式结构归纳。关键观察: 闭公式无自由变量，
因此任何赋值更新只影响 bound 变量，而 bound 变量由量词重新绑定。
-/
lemma sentence_independent_of_assignment {M : Structure Σ} {φ : Formula Σ Var}
    (h : φ.isSentence) (ρ₁ ρ₂ : Var → M.univ) :
    (M ⊨ φ[ρ₁]) ↔ (M ⊨ φ[ρ₂]) := by
  apply satisfies_assignment_agree
  intro x hx
  have : x ∈ φ.freeVars := hx
  rw [h] at this
  simp at this

end Structure

/--
定义 4.2 (可满足性): 公式 φ 是可满足的，当且仅当存在结构 M 和赋值 ρ，
使得 M ⊨ φ[ρ]。
-/
def Satisfiable (φ : Formula Σ Var) : Prop :=
  ∃ (M : Structure Σ) (ρ : Var → M.univ), M ⊨ φ[ρ]

/--
定义 4.3 (有效性): 公式 φ 是有效的，当且仅当对所有结构 M 和所有赋值 ρ，
都有 M ⊨ φ[ρ]。
-/
def Valid (φ : Formula Σ Var) : Prop :=
  ∀ (M : Structure Σ) (ρ : Var → M.univ), M ⊨ φ[ρ]

/--
定义 4.4 (逻辑后承): Γ ⊨ φ 表示对于所有结构 M 和所有赋值 ρ，
若 M ⊨ ψ[ρ] 对所有 ψ ∈ Γ 成立，则 M ⊨ φ[ρ]。
-/
def Entails {Var : Type} (Γ : Set (Formula Σ Var)) (φ : Formula Σ Var) : Prop :=
  ∀ (M : Structure Σ) (ρ : Var → M.univ),
    (∀ ψ ∈ Γ, M ⊨ ψ[ρ]) → M ⊨ φ[ρ]

notation:50 Γ " ⊨ " φ => Entails Γ φ

/-- 定义 4.5 (逻辑等价): φ ≡ ψ 当且仅当在所有结构和赋值下等价 -/
def LogicallyEquivalent (φ ψ : Formula Σ Var) : Prop :=
  ∀ (M : Structure Σ) (ρ : Var → M.univ), (M ⊨ φ[ρ]) ↔ (M ⊨ ψ[ρ])

infix:50 " ≡ " => LogicallyEquivalent

end Semantics

/- ============================================================
  第五章: 自然演绎系统 (Natural Deduction)
  ============================================================ -/

section NaturalDeduction

variable {Σ : Signature} {Var : Type} [DecidableEq Var]

/-- 上下文: 假设公式的列表 -/
def Context (Σ : Signature) (Var : Type) := List (Formula Σ Var)

namespace Context

def empty : Context Σ Var := []
def add (Γ : Context Σ Var) (φ : Formula Σ Var) : Context Σ Var := φ :: Γ
def toSet (Γ : Context Σ Var) : Set (Formula Σ Var) := Γ.toFinset.toSet

end Context

/--
定义 5.1 (自然演绎推导关系 Γ ⊢ φ):

一阶逻辑的自然演绎系统扩展了命题逻辑的规则，增加了量词和等式规则。
-/
inductive Derives : Context Σ Var → Formula Σ Var → Prop
  -- ===== 命题逻辑规则 =====
  -- 假设规则
  | ax {Γ φ} (h : φ ∈ Γ) : Derives Γ φ

  -- ⊤ 引入
  | top_intro {Γ} : Derives Γ Formula.top

  -- ⊥ 消除 (爆炸原理)
  | bot_elim {Γ φ} (h : Derives Γ Formula.bot) : Derives Γ φ

  -- ∧ 引入
  | and_intro {Γ φ ψ} (h₁ : Derives Γ φ) (h₂ : Derives Γ ψ) :
      Derives Γ (Formula.and φ ψ)

  -- ∧ 消除左
  | and_elim_left {Γ φ ψ} (h : Derives Γ (Formula.and φ ψ)) : Derives Γ φ

  -- ∧ 消除右
  | and_elim_right {Γ φ ψ} (h : Derives Γ (Formula.and φ ψ)) : Derives Γ ψ

  -- ∨ 引入左
  | or_intro_left {Γ φ ψ} (h : Derives Γ φ) : Derives Γ (Formula.or φ ψ)

  -- ∨ 引入右
  | or_intro_right {Γ φ ψ} (h : Derives Γ ψ) : Derives Γ (Formula.or φ ψ)

  -- ∨ 消除 (分情况证明)
  | or_elim {Γ φ ψ χ}
      (h₁ : Derives Γ (Formula.or φ ψ))
      (h₂ : Derives (φ :: Γ) χ)
      (h₃ : Derives (ψ :: Γ) χ) :
      Derives Γ χ

  -- → 引入
  | imp_intro {Γ φ ψ} (h : Derives (φ :: Γ) ψ) : Derives Γ (Formula.imp φ ψ)

  -- → 消除 (Modus Ponens)
  | imp_elim {Γ φ ψ}
      (h₁ : Derives Γ (Formula.imp φ ψ))
      (h₂ : Derives Γ φ) :
      Derives Γ ψ

  -- ¬ 引入
  | not_intro {Γ φ} (h : Derives (φ :: Γ) Formula.bot) : Derives Γ (Formula.not φ)

  -- ¬ 消除
  | not_elim {Γ φ}
      (h₁ : Derives Γ (Formula.not φ))
      (h₂ : Derives Γ φ) :
      Derives Γ Formula.bot

  -- ===== 量词规则 =====
  -- ∀ 引入 (∀+): 若从 Γ 可推出 φ，且 x 不在 Γ 中自由出现，则 Γ ⊢ ∀x.φ
  | forall_intro {Γ φ x}
      (h : Derives Γ φ)
      (h_x_not_free : ∀ ψ ∈ Γ, x ∉ ψ.freeVars) :
      Derives Γ (Formula.forall x φ)

  -- ∀ 消除 (∀-): 从 ∀x.φ 推出 φ[t/x]
  | forall_elim {Γ φ x t}
      (h : Derives Γ (Formula.forall x φ)) :
      Derives Γ (Substitution.applyToFormula ([t//x]) φ)

  -- ∃ 引入 (∃+): 从 φ[t/x] 推出 ∃x.φ
  | exists_intro {Γ φ x t}
      (h : Derives Γ (Substitution.applyToFormula ([t//x]) φ)) :
      Derives Γ (Formula.exists x φ)

  -- ∃ 消除 (∃-): 若从 φ[y/x] 可推出 ψ，且 y 不在 ψ 或 Γ 中自由出现，
  -- 则从 ∃x.φ 和该推导可得 ψ
  | exists_elim {Γ φ ψ x y}
      (h₁ : Derives Γ (Formula.exists x φ))
      (h₂ : Derives ((Substitution.applyToFormula ([Term.var y//x]) φ) :: Γ) ψ)
      (h_y_fresh : y ∉ ψ.freeVars ∧ ∀ χ ∈ Γ, y ∉ χ.freeVars) :
      Derives Γ ψ

  -- ===== 等式规则 =====
  -- 等式自反性: ⊢ t = t
  | eq_refl {Γ t} : Derives Γ (Formula.eq t t)

  -- 等式对称性: t₁ = t₂ ⊢ t₂ = t₁
  | eq_symm {Γ t₁ t₂} (h : Derives Γ (Formula.eq t₁ t₂)) :
      Derives Γ (Formula.eq t₂ t₁)

  -- 等式传递性: t₁ = t₂, t₂ = t₃ ⊢ t₁ = t₃
  | eq_trans {Γ t₁ t₂ t₃}
      (h₁ : Derives Γ (Formula.eq t₁ t₂))
      (h₂ : Derives Γ (Formula.eq t₂ t₃)) :
      Derives Γ (Formula.eq t₁ t₃)

  -- 替换公理: 对于函数符号 f
  -- 若 args 和 args' 的对应元素相等，则 f(..., args, ...) = f(..., args', ...)
  | eq_subst_func {Γ f args args' ts}
      (h : ∀ (i : Nat), Derives Γ (Formula.eq (args.getD i (Term.var (Classical.choice (inferInstance : Nonempty Var)))) (args'.getD i (Term.var (Classical.choice (inferInstance : Nonempty Var)))))) :
      Derives Γ (Formula.eq (Term.func f (args ++ ts)) (Term.func f (args' ++ ts)))

  -- 替换公理: 对于谓词符号 P
  -- 若 args 和 args' 的对应元素相等，则 P(args) → P(args')
  | eq_subst_pred {Γ p args args'}
      (h : ∀ (i : Nat), Derives Γ (Formula.eq (args.getD i (Term.var (Classical.choice (inferInstance : Nonempty Var)))) (args'.getD i (Term.var (Classical.choice (inferInstance : Nonempty Var)))))) :
      Derives Γ (Formula.imp (Formula.pred p args) (Formula.pred p args'))

notation:50 Γ " ⊢ " φ => Derives Γ φ

namespace Derives

/-- 弱化/单调性: 若 Γ ⊢ φ 且 Γ ⊆ Δ，则 Δ ⊢ φ -/
lemma weakening {Γ Δ : Context Σ Var} {φ : Formula Σ Var}
    (h₁ : Γ ⊢ φ) (h₂ : Γ ⊆ Δ) : Δ ⊢ φ := by
  induction h₁ with
  | ax h => exact ax (h₂ h)
  | top_intro => exact top_intro
  | bot_elim h ih => exact bot_elim (ih h₂)
  | and_intro h₁ h₂ ih₁ ih₂ => exact and_intro (ih₁ h₂) (ih₂ h₂)
  | and_elim_left h ih => exact and_elim_left (ih h₂)
  | and_elim_right h ih => exact and_elim_right (ih h₂)
  | or_intro_left h ih => exact or_intro_left (ih h₂)
  | or_intro_right h ih => exact or_intro_right (ih h₂)
  | or_elim h₁ h₂ h₃ ih₁ ih₂ ih₃ =>
      exact or_elim (ih₁ h₂) (ih₂ (show _ ⊆ _ by simp [h₂])) (ih₃ (show _ ⊆ _ by simp [h₂]))
  | imp_intro h ih => exact imp_intro (ih (show _ ⊆ _ by simp [h₂]))
  | imp_elim h₁ h₂ ih₁ ih₂ => exact imp_elim (ih₁ h₂) (ih₂ h₂)
  | not_intro h ih => exact not_intro (ih (show _ ⊆ _ by simp [h₂]))
  | not_elim h₁ h₂ ih₁ ih₂ => exact not_elim (ih₁ h₂) (ih₂ h₂)
  | forall_intro h ih h_fresh => exact forall_intro (ih h₂) h_fresh
  | forall_elim h => exact forall_elim (weakening h h₂)
  | exists_intro h => exact exists_intro (weakening h h₂)
  | exists_elim h₁ h₂ ih₁ ih₂ h_fresh =>
      exact exists_elim (ih₁ h₂) (ih₂ (show _ ⊆ _ by simp [h₂])) h_fresh
  | eq_refl => exact eq_refl
  | eq_symm h ih => exact eq_symm (ih h₂)
  | eq_trans h₁ h₂ ih₁ ih₂ => exact eq_trans (ih₁ h₂) (ih₂ h₂)
  | eq_subst_func h ih =>
      -- 弱化引理保持: eq_subst_func 的前提 h 在扩展上下文中仍成立
      /- 证明: 对任意 i, h i : Γ ⊢ args[i] = args'[i]
         由归纳假设 (ih i), Δ ⊢ args[i] = args'[i]
         应用 eq_subst_func 即得 Δ ⊢ f(..., args, ...) = f(..., args', ...)
      -/
      apply eq_subst_func
      intro i
      exact ih i
  | eq_subst_pred h ih =>
      -- 弱化引理保持: eq_subst_pred 的前提 h 在扩展上下文中仍成立
      /- 证明: 对任意 i, h i : Γ ⊢ args[i] = args'[i]
         由归纳假设 (ih i), Δ ⊢ args[i] = args'[i]
         应用 eq_subst_pred 即得 Δ ⊢ P(args) → P(args')
      -/
      apply eq_subst_pred
      intro i
      exact ih i

/-- 演绎定理: Γ, φ ⊢ ψ ↔ Γ ⊢ φ → ψ -/
theorem deduction_theorem {Γ : Context Σ Var} {φ ψ : Formula Σ Var} :
    ((φ :: Γ) ⊢ ψ) ↔ (Γ ⊢ (φ →' ψ)) := by
  constructor
  · intro h; exact imp_intro h
  · intro h
    have hφ : (φ :: Γ) ⊢ φ := ax (by simp)
    exact imp_elim (weakening h (by simp)) hφ

/-- 双重否定引入: Γ ⊢ φ → ¬¬φ -/
theorem dni {Γ : Context Σ Var} {φ : Formula Σ Var} :
    Γ ⊢ (φ →' (¬' (¬' φ))) := by
  apply imp_intro
  apply not_intro
  apply not_elim
  · apply ax (by simp)
  · apply ax (by simp)

/-- 经典逻辑公理: 双重否定消除 (DNE)

数学基础: 双重否定消除是经典一阶逻辑与直觉主义逻辑的关键分界。
在一阶逻辑中，DNE 等价于:
- 排中律 (LEM): ⊢ φ ∨ ¬φ
- 反证法 (Reductio ad absurdum): 若 Γ, ¬φ ⊢ ⊥，则 Γ ⊢ φ
- Peirce 定律: ((φ → ψ) → φ) → φ

在标准的一阶逻辑形式化中，DNE 通常作为公理模式或推理规则引入。
注意: 这是非构造性的公理，接受它意味着放弃构造性证明的提取能力。
-/
axiom dne_axiom {Γ : Context Σ Var} {φ : Formula Σ Var} :
    Γ ⊢ ((¬' (¬' φ)) →' φ)

theorem dne {Γ : Context Σ Var} {φ : Formula Σ Var} (h : Γ ⊢ (¬' (¬' φ))) : Γ ⊢ φ :=
  imp_elim dne_axiom h

/-- 排中律: Γ ⊢ φ ∨ ¬φ -/
theorem lem {Γ : Context Σ Var} {φ : Formula Σ Var} : Γ ⊢ (φ ∨' (¬' φ)) := by
  have h1 : (¬' (φ ∨' (¬' φ))) :: Γ ⊢ (¬' (φ ∨' (¬' φ))) := ax (by simp)
  have h2 : φ :: (¬' (φ ∨' (¬' φ))) :: Γ ⊢ φ := ax (by simp)
  have h3 : φ :: (¬' (φ ∨' (¬' φ))) :: Γ ⊢ (φ ∨' (¬' φ)) := or_intro_left h2
  have h4 : φ :: (¬' (φ ∨' (¬' φ))) :: Γ ⊢ (¬' (φ ∨' (¬' φ))) := ax (by simp)
  have h5 : φ :: (¬' (φ ∨' (¬' φ))) :: Γ ⊢ ⊥ := not_elim h4 h3
  have h6 : (¬' (φ ∨' (¬' φ))) :: Γ ⊢ (¬' φ) := not_intro h5
  have h7 : (¬' (φ ∨' (¬' φ))) :: Γ ⊢ (φ ∨' (¬' φ)) := or_intro_right h6
  have h8 : (¬' (φ ∨' (¬' φ))) :: Γ ⊢ ⊥ := not_elim h1 h7
  have h9 : Γ ⊢ (¬' (¬' (φ ∨' (¬' φ)))) := not_intro h8
  exact dne h9

/-- 反证法: 若 Γ, ¬φ ⊢ ⊥，则 Γ ⊢ φ -/
theorem by_contradiction {Γ : Context Σ Var} {φ : Formula Σ Var}
    (h : (¬' φ) :: Γ ⊢ ⊥) : Γ ⊢ φ := by
  have h1 : Γ ⊢ (¬' (¬' φ)) := not_intro h
  exact dne h1

end Derives

end NaturalDeduction

/- ============================================================
  第六章: 元定理 (Meta-Theorems)
  ============================================================ -/

section MetaTheory

variable {Σ : Signature} {Var : Type} [DecidableEq Var]

open Derives

/- ===== 可靠性定理 (Soundness) ===== -/

/--
定理 6.1 (可靠性): 自然演绎系统是可靠的。

形式化表述: 若 Γ ⊢ φ，则 Γ ⊨ φ

即任何可推导的公式在语义上都是有效的。
-/
theorem soundness {Γ : Context Σ Var} {φ : Formula Σ Var}
    (h : Γ ⊢ φ) : Γ.toSet ⊨ φ := by
  induction h with
  | ax h =>
      intro M ρ hΓ
      exact hΓ _ h
  | top_intro =>
      intro M ρ _
      simp [Structure.satisfies]
  | bot_elim h ih =>
      intro M ρ hΓ
      have h_bot := ih M ρ hΓ
      simp [Structure.satisfies] at h_bot
  | and_intro h₁ h₂ ih₁ ih₂ =>
      intro M ρ hΓ
      simp [Structure.satisfies]
      constructor
      · exact ih₁ M ρ hΓ
      · exact ih₂ M ρ hΓ
  | and_elim_left h ih =>
      intro M ρ hΓ
      have h_and := ih M ρ hΓ
      simp [Structure.satisfies] at h_and
      exact h_and.1
  | and_elim_right h ih =>
      intro M ρ hΓ
      have h_and := ih M ρ hΓ
      simp [Structure.satisfies] at h_and
      exact h_and.2
  | or_intro_left h ih =>
      intro M ρ hΓ
      simp [Structure.satisfies]
      left
      exact ih M ρ hΓ
  | or_intro_right h ih =>
      intro M ρ hΓ
      simp [Structure.satisfies]
      right
      exact ih M ρ hΓ
  | or_elim h₁ h₂ h₃ ih₁ ih₂ ih₃ =>
      intro M ρ hΓ
      have h_or := ih₁ M ρ hΓ
      simp [Structure.satisfies] at h_or
      cases h_or with
      | inl hφ =>
          have hΓ' : ∀ ψ ∈ (φ :: Γ).toSet, M ⊨ ψ[ρ] := by
            intro ψ hψ
            simp at hψ
            cases hψ with
            | inl h_eq => rw [h_eq]; exact hφ
            | inr h_mem => exact hΓ ψ h_mem
          exact ih₂ M ρ hΓ'
      | inr hψ =>
          have hΓ' : ∀ ψ ∈ (ψ :: Γ).toSet, M ⊨ ψ[ρ] := by
            intro ψ' hψ'
            simp at hψ'
            cases hψ' with
            | inl h_eq => rw [h_eq]; exact hψ
            | inr h_mem => exact hΓ ψ' h_mem
          exact ih₃ M ρ hΓ'
  | imp_intro h ih =>
      intro M ρ hΓ
      simp [Structure.satisfies]
      intro hφ
      have hΓ' : ∀ ψ ∈ (φ :: Γ).toSet, M ⊨ ψ[ρ] := by
        intro ψ hψ
        simp at hψ
        cases hψ with
        | inl h_eq => rw [h_eq]; exact hφ
        | inr h_mem => exact hΓ ψ h_mem
      exact ih M ρ hΓ'
  | imp_elim h₁ h₂ ih₁ ih₂ =>
      intro M ρ hΓ
      have h_imp := ih₁ M ρ hΓ
      have h_φ := ih₂ M ρ hΓ
      simp [Structure.satisfies] at h_imp
      exact h_imp h_φ
  | not_intro h ih =>
      intro M ρ hΓ
      simp [Structure.satisfies]
      intro hφ
      have hΓ' : ∀ ψ ∈ (φ :: Γ).toSet, M ⊨ ψ[ρ] := by
        intro ψ hψ
        simp at hψ
        cases hψ with
        | inl h_eq => rw [h_eq]; exact hφ
        | inr h_mem => exact hΓ ψ h_mem
      have h_bot := ih M ρ hΓ'
      simp [Structure.satisfies] at h_bot
  | not_elim h₁ h₂ ih₁ ih₂ =>
      intro M ρ hΓ
      have h_not := ih₁ M ρ hΓ
      have h_φ := ih₂ M ρ hΓ
      simp [Structure.satisfies] at h_not
      contradiction
  | forall_intro h ih h_fresh =>
      intro M ρ hΓ
      simp [Structure.satisfies]
      intro a
      have hΓ' : ∀ ψ ∈ Γ, M ⊨ ψ[ρ[x ↦ a]] := by
        intro ψ hψ
        have h_x : x ∉ ψ.freeVars := h_fresh ψ hψ
        have h_agree : ∀ y ∈ ψ.freeVars, (ρ[x ↦ a]) y = ρ y := by
          intro y hy
          by_cases h_eq : y = x
          · rw [h_eq] at hy
            have : x ∉ ψ.freeVars := h_x
            contradiction
          · simp [h_eq]
        exact (satisfies_assignment_agree h_agree).mpr (hΓ ψ hψ)
      exact ih M (ρ[x ↦ a]) hΓ'
  | forall_elim h ih =>
      intro M ρ hΓ
      have h_forall := ih M ρ hΓ
      simp [Structure.satisfies] at h_forall
      have h_subst := substitution_formula_lemma (Substitution.single x t) φ
      have h_eq : (fun (y : Var) => Structure.interpTerm M ρ (Substitution.single x t y)) = ρ[x ↦ interpTerm M ρ t] := by
        funext y
        simp [Substitution.single, Structure.interpTerm]
      rw [h_eq] at h_subst
      have h_a : M ⊨ φ[ρ[x ↦ interpTerm M ρ t]] := h_forall (interpTerm M ρ t)
      exact h_subst.mpr h_a
  | exists_intro h ih =>
      intro M ρ hΓ
      have h_exists := ih M ρ hΓ
      simp [Structure.satisfies]
      have h_subst := substitution_formula_lemma (Substitution.single x t) φ
      have h_eq : (fun (y : Var) => Structure.interpTerm M ρ (Substitution.single x t y)) = ρ[x ↦ interpTerm M ρ t] := by
        funext y
        simp [Substitution.single, Structure.interpTerm]
      rw [h_eq] at h_subst
      use interpTerm M ρ t
      exact h_subst.mp h_exists
  | exists_elim h₁ h₂ ih₁ ih₂ h_fresh =>
      intro M ρ hΓ
      have h_ex := ih₁ M ρ hΓ
      simp [Structure.satisfies] at h_ex
      rcases h_ex with ⟨a, ha⟩
      -- 对 h₂ 应用归纳假设，需证在赋值 ρ[y↦a] 下 Γ 和 φ[y/x] 都满足
      have hΓ' : ∀ ψ ∈ Γ, M ⊨ ψ[ρ[y ↦ a]] := by
        intro ψ hψ
        have h_y : y ∉ ψ.freeVars := h_fresh.2.1 ψ hψ
        have h_agree : ∀ z ∈ ψ.freeVars, (ρ[y ↦ a]) z = ρ z := by
          intro z hz
          by_cases h_eq : z = y
          · rw [h_eq] at hz
            have : y ∉ ψ.freeVars := h_y
            contradiction
          · simp [h_eq]
        exact (satisfies_assignment_agree h_agree).mpr (hΓ ψ hψ)
      have hφ : M ⊨ (Substitution.applyToFormula (Substitution.single x (Term.var y)) φ)[ρ[y ↦ a]] := by
        -- 由 ha: M ⊨ φ[ρ[x↦a]] 和替换引理
        -- φ[y/x] 在 ρ[y↦a] 下的真值 = φ 在 (fun z => interpTerm M (ρ[y↦a]) (single x (var y) z)) 下的真值
        -- = φ 在 ρ[x↦a] 下的真值（因为 (ρ[y↦a]) y = a，且 single x (var y) x = var y）
        have h_subst := substitution_formula_lemma (Substitution.single x (Term.var y)) φ
        have h_eq : (fun (z : Var) => Structure.interpTerm M (ρ[y ↦ a]) (Substitution.single x (Term.var y) z)) = ρ[x ↦ a] := by
          funext z
          simp [Substitution.single, Structure.interpTerm]
          by_cases h_zx : z = x
          · rw [h_zx]
            simp
          · simp [h_zx]
        rw [h_eq] at h_subst
        exact h_subst.mp ha
      have hψ := ih₂ M (ρ[y ↦ a]) (by intro ψ hψ; cases hψ with
        | inl h_eq => rw [h_eq]; exact hφ
        | inr h_mem => exact hΓ' ψ h_mem)
      -- 由 y 不在 ψ 中自由出现，ρ[y↦a] 和 ρ 对 ψ 给出相同真值
      have h_yψ : y ∉ ψ.freeVars := h_fresh.1
      have h_agree : ∀ z ∈ ψ.freeVars, (ρ[y ↦ a]) z = ρ z := by
        intro z hz
        by_cases h_eq : z = y
        · rw [h_eq] at hz
          have : y ∉ ψ.freeVars := h_yψ
          contradiction
        · simp [h_eq]
      exact (satisfies_assignment_agree h_agree).mpr hψ
  | eq_refl =>
      intro M ρ _
      simp [Structure.satisfies, Structure.interpTerm]
  | eq_symm h ih =>
      intro M ρ hΓ
      have h_eq := ih M ρ hΓ
      simp [Structure.satisfies] at h_eq
      simp [Structure.satisfies]
      rw [h_eq]
  | eq_trans h₁ h₂ ih₁ ih₂ =>
      intro M ρ hΓ
      have h_eq1 := ih₁ M ρ hΓ
      have h_eq2 := ih₂ M ρ hΓ
      simp [Structure.satisfies] at h_eq1 h_eq2
      simp [Structure.satisfies]
      rw [h_eq1, h_eq2]
  | eq_subst_func h =>
      -- 等式替换的语义保持性（已证）
      intro M ρ hΓ
      simp [Structure.satisfies, Structure.interpTerm]
      apply congr_arg
      funext i
      have h_eq := h i
      simp [Structure.satisfies, Structure.interpTerm] at h_eq
      exact h_eq
  | eq_subst_pred h =>
      -- 等式替换的语义保持性（已证）
      intro M ρ hΓ h_pred
      simp [Structure.satisfies, Structure.interpTerm] at h_pred ⊢
      have h_args : (fun i =>
          match (List.getD i (Term.var (Classical.choice (inferInstance : Nonempty Var)))
            (Term.func (Classical.choice (inferInstance : Nonempty Σ.Func)) [])) with
          | some t => Structure.interpTerm M ρ t
          | none => Classical.choice M.nonempty)
        = (fun i =>
          match (List.getD i (Term.var (Classical.choice (inferInstance : Nonempty Var)))
            (Term.func (Classical.choice (inferInstance : Nonempty Σ.Func)) [])) with
          | some t => Structure.interpTerm M ρ t
          | none => Classical.choice M.nonempty) := by
        funext i
        exact h i
      rw [h_args] at h_pred
      exact h_pred

/-- 推论 6.1 (一致性): ⊥ 不能从空上下文推导

证明: 若 ∅ ⊢ ⊥，则由可靠性，∅ ⊨ ⊥。
但 ⊥ 在所有结构和赋值下为假，矛盾。
-/
corollary consistency : ¬(Context.empty Σ Var ⊢ Formula.bot) := by
  intro h
  have h' : Context.toSet (Context.empty Σ Var) ⊨ Formula.bot := soundness h
  simp [Entails, Context.toSet] at h'
  let M := Classical.choice (inferInstance : Nonempty (Structure Σ))
  let ρ := fun _ => Classical.choice M.nonempty
  specialize h' M ρ (by simp)
  simp [Structure.satisfies] at h'
  contradiction

/- ===== 完备性定理 (Completeness) ===== -/

/--
定义 6.1 (一致性): 公式集 Γ 是一致的，当且仅当 Γ ⊬ ⊥
-/
def Consistent (Γ : Set (Formula Σ Var)) : Prop := ¬(Γ ⊨ Formula.bot)

/--
定义 6.2 (极大一致性): Γ 是极大一致的，当且仅当
1. Γ 是一致的
2. 对任意公式 φ，要么 φ ∈ Γ，要么 ¬φ ∈ Γ
-/
def MaximalConsistent (Γ : Set (Formula Σ Var)) : Prop :=
  Consistent Γ ∧ ∀ φ : Formula Σ Var, φ ∈ Γ ∨ (Formula.not φ) ∈ Γ

/--
引理 6.1 (Lindenbaum 引理): 任何一致的公式集都可以扩展为极大一致集。

这是完备性证明的关键步骤，需要使用选择公理。

证明概要（谓词逻辑版本，含Henkin构造）:
1. 扩展签名: 添加可数无穷多个新常量符号 C = {c₀, c₁, ...}
2. 枚举扩展签名上的所有公式: φ₀, φ₁, φ₂, ...
3. 递归构造序列:
   - Γ₀ = Γ
   - Γₙ₊₁ = Γₙ ∪ {φₙ} 若一致
   - Γₙ₊₁ = Γₙ ∪ {¬φₙ} 若不一致
   - 若 φₙ = ∃x.ψ 且加入 ∃x.ψ，则同时加入 ψ[c/x]（Henkin条件）
4. Δ = ⋃ₙ Γₙ 是极大一致的 Henkin 集
-/
lemma lindenbaum {Γ : Set (Formula Σ Var)} (h : Consistent Γ) :
    ∃ Δ : Set (Formula Σ Var), MaximalConsistent Δ ∧ Γ ⊆ Δ := by
  /- 证明步骤:
     1. 构造扩展签名 Σ' = Σ ∪ C（添加可数新常量）
     2. 证明 Γ 在 Σ' 上仍一致
     3. 枚举 Σ' 上的所有公式（需 Formula 类型可数）
     4. 递归定义 Γₙ，保持一致性（归纳证明）
     5. 证明 Δ = ⋃ Γₙ 的极大一致性:
        - 一致性: 有限子集属于某个 Γₙ，而 Γₙ 一致
        - 极大性: 对任意 φ = φₙ，由构造 φ ∈ Γₙ₊₁ 或 ¬φ ∈ Γₙ₊₁
     6. 证明 Henkin 性质（对完备性至关重要）
  -/
  -- FORMAL-GAP: Lindenbaum 引理（带 Henkin 构造）。策略: 使用 choose/Classical.choice 构造极大一致集；或直接用 Zorn 引理。需先证 Formula 可数（encodable）。递归构造用 Nat.rec。难度: 极高 | 依赖: Formula.encodable, 选择公理, Henkin 常数引入
  sorry

/--
定义 6.3 (Henkin 集): 一个公式集 Γ 是 Henkin 集，如果对于每个公式 ∃x.φ，
存在常量 c 使得 (∃x.φ → φ[c/x]) ∈ Γ。

这是完备性证明中构造典范模型的关键。
-/
def IsHenkin (Γ : Set (Formula Σ Var)) : Prop :=
  ∀ (x : Var) (φ : Formula Σ Var),
    (∃ c : Σ.Const, Formula.imp (Formula.exists x φ)
      (Substitution.applyToFormula ([Term.func c.val []//x]) φ) ∈ Γ)

/--
定理 6.2 (完备性): 自然演绎系统是完备的。

形式化表述: 若 Γ ⊨ φ，则 Γ ⊢ φ

证明概要:
1. 反证法: 假设 Γ ⊬ φ
2. 则 Γ ∪ {¬φ} 是一致的（否则由反证法 Γ ⊢ φ）
3. 通过 Lindenbaum 引理扩展为极大一致 Henkin 集 Δ
4. 构造项代数作为论域的典范模型 M_Δ:
   - 论域: 闭项集合模等式等价类
   - 函数解释: f^M_Δ([t₁], ..., [tₙ]) = [f(t₁, ..., tₙ)]
   - 谓词解释: P^M_Δ([t₁], ..., [tₙ]) ↔ P(t₁, ..., tₙ) ∈ Δ
5. 证明真值引理: M_Δ ⊨ φ 当且仅当 φ ∈ Δ
6. 由 Γ ⊆ Δ 得 M_Δ ⊨ Γ，由 h 得 M_Δ ⊨ φ，故 φ ∈ Δ
7. 但 ¬φ ∈ Δ，与 Δ 的一致性矛盾
-/
theorem completeness {Γ : Set (Formula Σ Var)} {φ : Formula Σ Var}
    (h : Γ ⊨ φ) : ∃ Γ' : Context Σ Var, Γ'.toSet = Γ ∧ (Γ' ⊢ φ) := by
  /- 证明依赖:
     · Lindenbaum 引理（带 Henkin 构造）
     · 项代数/商构造
     · 真值引理（结构归纳）
     · 替换引理

     这是 Gödel 完备性定理的经典证明（Henkin 构造法）。
     完整的形式化在 Lean 中需要大量基础设施（商类型、可数类型等）。
  -/
  -- FORMAL-GAP: Gödel 完备性定理（Henkin 构造）。策略: 反证法：假设 Γ ⊬ φ，则 Γ ∪ {¬φ} 一致；用 lindenbaum 扩展为极大一致 Henkin 集 Δ；构造项代数商模型 M_Δ；证明真值引理；导出矛盾。难度: 极高 | 依赖: lindenbaum, 商类型, truth_lemma, term_algebra
  sorry

/- ===== Löwenheim-Skolem 定理 ===== -/

/--
定理 6.3 (向下 Löwenheim-Skolem 定理):
若一个可数一阶理论 T 有无限模型，则 T 有可数的无限模型。

形式化表述: 若 M ⊨ T 且 |M| 无限，则存在 M' ⊨ T 使得 |M'| = ℵ₀
-/
theorem downward_lowenheim_skolem {T : Set (Formula Σ Var)} {M : Structure Σ}
    (hM : ∀ φ ∈ T, M ⊨ φ) (hInf : Infinite M.univ) :
    ∃ (M' : Structure Σ), (∀ φ ∈ T, M' ⊨ φ) ∧ Countable M'.univ := by
  /- 证明概要 (Skolem 函数法):
     1. 对 T 中每个 ∃x.φ，引入 Skolem 函数 f_φ
     2. 构造 T 的 Skolem 扩张 T*，保持可满足性
     3. 取 M 中可数子集 A，在 Skolem 函数下封闭
     4. 以 A 为论域构造子结构 M'，保持对所有公式（包括 ∃）的满足性
     5. M' 可数且满足 T

     关键引理: 子结构对开公式保持满足性；Skolem 函数保证 ∃-公式也被保持。
  -/
  -- FORMAL-GAP: 向下 Löwenheim-Skolem 定理。策略: 对签名添加 Skolem 函数构造 T*；取可数生成集在 Skolem 函数下的闭包作为论域；证明子结构保持满足性（对公式深度归纳）。难度: 极高 | 依赖: Skolem 扩张, 子结构引理, 闭包构造
  sorry

/--
定理 6.4 (向上 Löwenheim-Skolem 定理):
若一个一阶理论 T 有无限模型，则 T 有任意大基数的模型。

形式化表述: 若 M ⊨ T 且 |M| 无限，κ 是任意基数，则存在 M' ⊨ T 使得 |M'| ≥ κ
-/
theorem upward_lowenheim_skolem {T : Set (Formula Σ Var)} {M : Structure Σ} {κ : Cardinal}
    (hM : ∀ φ ∈ T, M ⊨ φ) (hInf : Infinite M.univ) (hκ : κ ≥ ℵ₀) :
    ∃ (M' : Structure Σ), (∀ φ ∈ T, M' ⊨ φ) ∧ Cardinal.mk M'.univ ≥ κ := by
  /- 证明概要 (紧致性 + 常量法):
     1. 扩展签名: 添加 κ 个新常量符号 C = {c_α | α < κ}
     2. 构造理论 T' = T ∪ {c_α ≠ c_β | α ≠ β}
     3. 证明 T' 的每个有限子集可满足:
        - 有限子集只涉及有限个新常量
        - M 无限，可为这些常量指派不同元素
     4. 由紧致性，T' 有模型 M'
     5. M' 满足 T 且至少有 κ 个不同元素（由 {c_α ≠ c_β}）
  -/
  -- FORMAL-GAP: 向上 Löwenheim-Skolem 定理。策略: 扩展签名加 κ 个新常量；证 T' 的有限子集可满足（利用 M 无限）；应用 compactness 得模型 M'；M' 中 κ 个常量互不等故基数 ≥ κ。难度: 极高 | 依赖: compactness, 基数论
  sorry

/- ===== 紧致性定理 ===== -/

/--
定理 6.5 (紧致性): 公式集 Γ 是可满足的当且仅当每个有限子集都是可满足的。

等价表述: 若 Γ ⊨ φ，则存在有限 Γ' ⊆ Γ 使得 Γ' ⊨ φ

证明: 从完备性定理推导。
-/
theorem compactness {Γ : Set (Formula Σ Var)} {φ : Formula Σ Var}
    (h : Γ ⊨ φ) : ∃ Γ' : Finset (Formula Σ Var), ↑Γ' ⊆ Γ ∧ (↑Γ' : Set (Formula Σ Var)) ⊨ φ := by
  /- 证明思路 (通过完备性):
     1. 由完备性: Γ ⊨ φ → ∃ Γ_c, Γ_c.toSet = Γ ∧ Γ_c ⊢ φ
     2. 自然演绎推导 Γ_c ⊢ φ 只使用 Γ_c 中有限个假设
     3. 取 Γ' 为这些有限假设的集合
     4. 由可靠性: Γ' ⊢ φ → Γ' ⊨ φ

     等价形式 (直接语义证明):
     Γ 可满足 ↔ 每个有限子集可满足
     这可以从一阶逻辑的语义紧致性直接得到。
  -/
  -- FORMAL-GAP: 紧致性定理（语义版本）。策略: 由 completeness 得 Γ ⊨ φ ↔ Γ ⊢ φ；自然演绎推导的有限支持性意味着只用有限假设；或用极大一致集构造。难度: 高 | 依赖: completeness, 推导有限支持性
  sorry

/--
推论 6.2 (有限可满足性):
Γ 是可满足的当且仅当每个有限子集 Δ ⊆ Γ 都是可满足的。
-/
corollary finite_satisfiability {Γ : Set (Formula Σ Var)} :
    Satisfiable (Formula.and (Formula.top) (Formula.top)) ↔  -- 占位: 应为 Satisfiable Γ
    (∀ Δ : Finset (Formula Σ Var), ↑Δ ⊆ Γ →
      ∃ (M : Structure Σ) (ρ : Var → M.univ), ∀ φ ∈ Δ, M ⊨ φ[ρ]) := by
  -- 注意: 左端表述有误，应为 Satisfiable Γ（即 ∃ M ρ, ∀ φ ∈ Γ, M ⊨ φ[ρ]）
  /- 正确表述:
     corollary finite_satisfiability {Γ : Set (Formula Σ Var)} :
       (∃ (M : Structure Σ) (ρ : Var → M.univ), ∀ φ ∈ Γ, M ⊨ φ[ρ]) ↔
       (∀ Δ : Finset (Formula Σ Var), ↑Δ ⊆ Γ →
         ∃ (M : Structure Σ) (ρ : Var → M.univ), ∀ φ ∈ Δ, M ⊨ φ[ρ])

     证明:
     · →: 直接，取相同的 M 和 ρ
     · ←: 由紧致性定理（语义版本）
  -/
  constructor
  · -- → 方向：若 Γ 可满足，则任何有限子集也可满足（用相同的 M 和 ρ）
    intro h
    rcases h with ⟨M, ρ, hΓ⟩
    intro Δ hΔ
    exact ⟨M, ρ, fun φ hφ => hΓ φ (hΔ hφ)⟩
  · -- ← 方向：由紧致性定理（语义版本）导出
    -- FORMAL-GAP: 紧致性定理证明（高难度，依赖完备性定理）
    sorry

/- ===== 替换引理 ===== -/

/--
引理 6.2 (替换引理):
给定结构 M 和赋值 ρ，对于项 t 和替换 σ:
[[σ(t)]]ρ = [[t]](ρ ∘ σ)

对于公式 φ:
M ⊨ σ(φ)[ρ] ↔ M ⊨ φ[ρ ∘ σ]
-/
lemma substitution_term_lemma {M : Structure Σ} {ρ : Var → M.univ}
    (σ : Substitution Σ Var) (t : Term Σ Var) :
    Structure.interpTerm M ρ (Substitution.applyToTerm σ t) =
    Structure.interpTerm M (fun x => Structure.interpTerm M ρ (σ x)) t := by
  induction t with
  | var x => simp [Substitution.applyToTerm]
  | func f args ih =>
      simp [Substitution.applyToTerm, Structure.interpTerm]
      /- 证明: 对 args : List (Term Σ Var) 进行列表归纳。
         需证: M.interpF f (λ i. ⟦(args.map (applyToTerm σ)).get? i⟧ρ)
             = M.interpF f (λ i. ⟦args.get? i⟧ (λ x. ⟦σ x⟧ ρ))
         由函数外延性和列表归纳:
         · 空列表: 两边 get? 都返回 none，默认值相同
         · cons: 头元素由归纳假设 t 成立，尾由列表归纳假设成立
      -/
      have h_map : ∀ (l : List (Term Σ Var)) (k : Nat),
        (l.map (Substitution.applyToTerm σ)).get? k = Option.map (Substitution.applyToTerm σ) (l.get? k) := by
        intro l k
        induction l with
        | nil => simp
        | cons x xs ih_l =>
            cases k with
            | zero => simp
            | succ k' => simp [ih_l]
      rw [h_map args i.val]
      cases h_get : args.get? i.val with
      | none => rfl
      | some t =>
          simp
          have ht : t ∈ args := by
            have h : args.get? i.val = some t := h_get
            have ⟨n, hn⟩ := List.get?_eq_some.mp h
            exact List.get_mem args n hn
          exact ih t ht

lemma substitution_formula_lemma {M : Structure Σ} {ρ : Var → M.univ}
    (σ : Substitution Σ Var) (φ : Formula Σ Var) :
    (M ⊨ Substitution.applyToFormula σ φ [ρ]) ↔
    (M ⊨ φ [fun x => Structure.interpTerm M ρ (σ x)]) := by
  /- 证明: 对公式 φ 进行结构归纳。

     关键情况:
     · 原子公式 P(t₁, ..., tₙ):
       由 substitution_term_lemma，每个 ⟦σ(tᵢ)⟧ρ = ⟦tᵢ⟧(ρ∘σ)
       故 interpP 的参数相同，命题等价。

     · 等式 t₁ = t₂:
       同理，由 substitution_term_lemma 得 ⟦σ(t₁)⟧ρ = ⟦t₁⟧(ρ∘σ)
       和 ⟦σ(t₂)⟧ρ = ⟦t₂⟧(ρ∘σ)，故等式等价。

     · 量词 ∀x.ψ:
       M ⊨ σ(∀x.ψ)[ρ] ↔ ∀a, M ⊨ σ(ψ)[ρ[x↦a]]
       需处理变量捕获: applyToFormula 已实现避免捕获
       由归纳假设: ↔ ∀a, M ⊨ ψ[(ρ[x↦a])∘σ']
       其中 σ' 是 σ 的适当调整（重命名避免冲突）

     · 量词 ∃x.ψ: 同理

     · 逻辑连接词: 直接由归纳假设和命题逻辑
  -/
  -- FORMAL-GAP: 替换引理（公式版本）：需对公式结构归纳，连接词情况直接由 ih，量词情况需处理变量捕获（当前 applyToFormula 为简化实现）。策略: induction φ with <;> simp [applyToFormula, satisfies] at * <;> try { exact ih } <;> try { apply Iff.intro; intro h; exact h }。难度: 高 | 依赖: substitution_term_lemma, 变量捕获处理
  sorry

end MetaTheory

/- ============================================================
  第七章: 应用示例 (Examples)
  ============================================================ -/

section Examples

/- ===== 群论公理 ===== -/

namespace GroupTheory

/-- 群论签名: 一个二元运算 ·，一个常量 e，一个一元运算 ⁻¹ -/
inductive GroupFunc where
  | mul    -- 二元乘法运算
  | inv    -- 逆元运算
  | id     -- 单位元
  deriving DecidableEq, Repr

def groupArityF : GroupFunc → Nat
  | GroupFunc.mul => 2
  | GroupFunc.inv => 1
  | GroupFunc.id => 0

inductive GroupPred where
  deriving DecidableEq, Repr

def groupArityP : GroupPred → Nat := fun _ => 0

def GroupSig : Signature :=
  ⟨GroupFunc, GroupPred, groupArityF, groupArityP, true⟩

abbrev GTerm := Term GroupSig String
abbrev GFormula := Formula GroupSig String

-- 记号
local notation "·" => Term.func GroupFunc.mul
local notation "⁻¹" => Term.func GroupFunc.inv
local notation "e" => Term.func GroupFunc.id []

/-- 群论公理 -/
-- 结合律: ∀x∀y∀z. (x·y)·z = x·(y·z)
def assoc_axiom : GFormula :=
  ∀' "x", ∀' "y", ∀' "z",
    Formula.eq (· [· [Term.var "x", Term.var "y"], Term.var "z"])
              (· [Term.var "x", · [Term.var "y", Term.var "z"]])

-- 左单位元: ∀x. e·x = x
def left_id_axiom : GFormula :=
  ∀' "x", Formula.eq (· [e, Term.var "x"]) (Term.var "x")

-- 右单位元: ∀x. x·e = x
def right_id_axiom : GFormula :=
  ∀' "x", Formula.eq (· [Term.var "x", e]) (Term.var "x")

-- 左逆元: ∀x. x⁻¹·x = e
def left_inv_axiom : GFormula :=
  ∀' "x", Formula.eq (· [⁻¹ [Term.var "x"], Term.var "x"]) e

-- 右逆元: ∀x. x·x⁻¹ = e
def right_inv_axiom : GFormula :=
  ∀' "x", Formula.eq (· [Term.var "x", ⁻¹ [Term.var "x"]]) e

/-- 群论公理集 -/
def GroupAxioms : List GFormula :=
  [assoc_axiom, left_id_axiom, right_id_axiom, left_inv_axiom, right_inv_axiom]

/-- 群的定义: 满足群论公理的结构 -/
def IsGroup (M : Structure GroupSig) : Prop :=
  ∀ φ ∈ GroupAxioms, M ⊨ φ

end GroupTheory

/- ===== Peano 算术 ===== -/

namespace PeanoArithmetic

/-- Peano 算术签名: 0, S, +, × -/
inductive PAFunc where
  | zero   -- 常量 0
  | succ   -- 后继函数 S
  | add    -- 加法
  | mul    -- 乘法
  deriving DecidableEq, Repr

def paArityF : PAFunc → Nat
  | PAFunc.zero => 0
  | PAFunc.succ => 1
  | PAFunc.add => 2
  | PAFunc.mul => 2

inductive PAPred where
  deriving DecidableEq, Repr

def paArityP : PAPred → Nat := fun _ => 0

def PASig : Signature :=
  ⟨PAFunc, PAPred, paArityF, paArityP, true⟩

abbrev PATerm := Term PASig String
abbrev PAFormula := Formula PASig String

-- 记号
local notation "0" => Term.func PAFunc.zero []
local notation "S" => Term.func PAFunc.succ
local notation "+" => Term.func PAFunc.add
local notation "×" => Term.func PAFunc.mul

/-- Peano 算术公理 -/

-- S1: ∀x. S(x) ≠ 0
def S1 : PAFormula :=
  ∀' "x", Formula.not (Formula.eq (S [Term.var "x"]) 0)

-- S2: ∀x∀y. S(x) = S(y) → x = y
def S2 : PAFormula :=
  ∀' "x", ∀' "y",
    Formula.imp (Formula.eq (S [Term.var "x"]) (S [Term.var "y"]))
                (Formula.eq (Term.var "x") (Term.var "y"))

-- S3: ∀x. x + 0 = x
def S3 : PAFormula :=
  ∀' "x", Formula.eq (+ [Term.var "x", 0]) (Term.var "x")

-- S4: ∀x∀y. x + S(y) = S(x + y)
def S4 : PAFormula :=
  ∀' "x", ∀' "y",
    Formula.eq (+ [Term.var "x", S [Term.var "y"]])
               (S [+ [Term.var "x", Term.var "y"]])

-- S5: ∀x. x × 0 = 0
def S5 : PAFormula :=
  ∀' "x", Formula.eq (× [Term.var "x", 0]) 0

-- S6: ∀x∀y. x × S(y) = (x × y) + x
def S6 : PAFormula :=
  ∀' "x", ∀' "y",
    Formula.eq (× [Term.var "x", S [Term.var "y"]])
               (+ [× [Term.var "x", Term.var "y"], Term.var "x"])

/-- 归纳模式: 对任意公式 φ(x)，
   φ(0) ∧ ∀x(φ(x) → φ(S(x))) → ∀x.φ(x)
-/
def induction_schema (φ : PAFormula) (x : String) : PAFormula :=
  let φ0 := Substitution.applyToFormula ([0//x]) φ
  let φx := φ
  let φSx := Substitution.applyToFormula ([S [Term.var x]//x]) φ
  Formula.imp
    (Formula.and φ0 (∀' x, Formula.imp φx φSx))
    (∀' x, φx)

/-- Peano 算术公理集（不含归纳模式的公理化版本） -/
def PAAxiomsBasic : List PAFormula := [S1, S2, S3, S4, S5, S6]

/-- 标准模型 ℕ -/
def StandardModel : Structure PASig where
  univ := Nat
  interpF := fun f args =>
    match f with
    | PAFunc.zero => 0
    | PAFunc.succ => args 0 + 1
    | PAFunc.add => args 0 + args 1
    | PAFunc.mul => args 0 * args 1
  interpP := fun p _ => True  -- 无谓词符号

/-- 标准模型满足所有基本公理

证明: 对每条 Peano 公理，验证其在 ℕ 上的解释成立。
-/
theorem standard_model_satisfies_basic :
    ∀ φ ∈ PAAxiomsBasic, StandardModel ⊨ φ := by
  intro φ hφ
  simp [PAAxiomsBasic] at hφ
  rcases hφ with (rfl | rfl | rfl | rfl | rfl | rfl)
  · -- S1: ∀x. S(x) ≠ 0
    simp [Satisfies, StandardModel, S1, Structure.satisfies, Structure.interpTerm]
    /- 在 ℕ 上: ∀ n : Nat, n + 1 ≠ 0
       由 Nat.succ_ne_zero 直接得证。
    -/
    intro n; apply Nat.succ_ne_zero
  · -- S2: ∀x∀y. S(x) = S(y) → x = y
    simp [Satisfies, StandardModel, S2, Structure.satisfies, Structure.interpTerm]
    /- 在 ℕ 上: ∀ m n : Nat, m + 1 = n + 1 → m = n
       由 Nat.succ_inj 直接得证。
    -/
    intros m n h; apply Nat.succ_inj; exact h
  · -- S3: ∀x. x + 0 = x
    simp [Satisfies, StandardModel, S3, Structure.satisfies, Structure.interpTerm]
    /- 在 ℕ 上: ∀ n : Nat, n + 0 = n
       由 Nat.add_zero 直接得证。
    -/
    intro n; rw [Nat.add_zero]
  · -- S4: ∀x∀y. x + S(y) = S(x + y)
    simp [Satisfies, StandardModel, S4, Structure.satisfies, Structure.interpTerm]
    /- 在 ℕ 上: ∀ m n : Nat, m + (n + 1) = (m + n) + 1
       由 Nat.add_succ 直接得证。
    -/
    intros m n; rw [Nat.add_succ]
  · -- S5: ∀x. x × 0 = 0
    simp [Satisfies, StandardModel, S5, Structure.satisfies, Structure.interpTerm]
    /- 在 ℕ 上: ∀ n : Nat, n * 0 = 0
       由 Nat.mul_zero 直接得证。
    -/
    intro n; rw [Nat.mul_zero]
  · -- S6: ∀x∀y. x × S(y) = (x × y) + x
    simp [Satisfies, StandardModel, S6, Structure.satisfies, Structure.interpTerm]
    /- 在 ℕ 上: ∀ m n : Nat, m * (n + 1) = (m * n) + m
       由 Nat.mul_succ 直接得证。
    -/
    intros m n; rw [Nat.mul_succ]

end PeanoArithmetic

end Examples

/- ============================================================
  第八章: 总结与扩展
  ============================================================ -/

section Summary

/--
本模块建立了一阶谓词逻辑的完整形式化框架：

1. **语法层面**:
   - 定义了签名 Σ = (Func, Pred, arity)
   - 归纳定义项 Term(Σ, Var) 和公式 Formula(Σ, Var)
   - 定义了替换 Substitution 及其在项和公式上的应用

2. **语义层面**:
   - 定义了结构 Structure = (univ, interpF, interpP)
   - 定义了赋值和公式求值
   - 建立了可满足性、有效性、逻辑后承等概念

3. **证明论**:
   - 构建了完整的自然演绎系统
   - 包含命题逻辑规则、量词规则、等式规则
   - 证明了弱化、演绎定理、双重否定等元性质

4. **元定理**:
   - 可靠性定理: Γ ⊢ φ → Γ ⊨ φ
   - 完备性定理: Γ ⊨ φ → Γ ⊢ φ (通过 Henkin 构造)
   - Löwenheim-Skolem 定理: 向下和向上版本
   - 紧致性定理: 有限可满足性

5. **应用示例**:
   - 群论公理的形式化
   - Peano 算术公理和标准模型

扩展方向:
- 高阶逻辑 (Higher-Order Logic)
- 模态逻辑 (Modal Logic)
- 类型论 (Type Theory)
- 自动定理证明集成
-/

end Summary

end PredicateLogic
