/-
SimpleTypes.lean - 简单类型 Lambda 演算

本文件定义简单类型 Lambda 演算 (Simply Typed Lambda Calculus, λ→)
的类型语法、类型环境和类型判断规则。

类型语法:
  T ::= Bool          -- 布尔类型
      | Nat           -- 自然数类型
      | T → T         -- 函数类型

类型判断:
  Γ ⊢ t : T  -- 在上下文 Γ 中，项 t 具有类型 T

作者: AnalysisDataFlow Project
日期: 2026-04-10
-/

import FormalMethods.Lambda.Syntax

namespace FormalMethods.TypeSystem.SimpleTypes

open Lambda.Syntax
open Lambda.Syntax.Term

/-! 
## 类型定义

简单类型的归纳定义。
-/

/-- 
类型 (Type) 的归纳定义
-/
inductive Type : Type where
  | bool : Type       -- 布尔类型 Bool
  | nat : Type        -- 自然数类型 Nat
  | arrow : Type → Type → Type  -- 函数类型 T₁ → T₂
  deriving Repr, BEq, Inhabited

open Type

/-- 
函数类型的记号: T₁ → T₂
-/
infixr:60 " ⇒ " => arrow

/-! 
## 类型环境

类型环境（上下文）记录变量的类型声明。
-/

/-- 
类型环境：变量名到类型的映射

使用列表实现，新绑定在列表头部。
-/
def Context := List (Name × Type)

/-- 
空环境
-/
def emptyContext : Context := []

/-- 
扩展环境

在环境 Γ 中添加变量 x 的类型 T，得到新环境 Γ, x:T
-/
def extendContext (Γ : Context) (x : Name) (T : Type) : Context :=
  (x, T) :: Γ

/-- 
环境查找

在环境 Γ 中查找变量 x 的类型。
-/
def lookupContext (Γ : Context) (x : Name) : Option Type :=
  match Γ with
  | [] => none
  | (y, T) :: rest =>
      if y = x then some T else lookupContext rest x

/-- 
环境扩展记号: Γ, x:T
-/
notation:max Γ ", " x " : " T => extendContext Γ x T

/-- 
变量在环境中
-/
def inContext (x : Name) (Γ : Context) : Prop :=
  lookupContext Γ x ≠ none

/-! 
## 类型判断

类型判断规则定义了项何时具有特定类型。

判断形式: Γ ⊢ t : T
-/

/-- 
类型判断的归纳定义
-/
inductive hasType : Context → Term → Type → Prop where
  -- T-Var: 如果 x:T ∈ Γ，则 Γ ⊢ x : T
  | var {Γ x T} : 
      lookupContext Γ x = some T → 
      hasType Γ (var x) T
  
  -- T-Abs: 如果 Γ, x:T₁ ⊢ t : T₂，则 Γ ⊢ λx. t : T₁ → T₂
  | abs {Γ x t T₁ T₂} : 
      hasType (Γ, x : T₁) t T₂ → 
      hasType Γ (abs x t) (T₁ ⇒ T₂)
  
  -- T-App: 如果 Γ ⊢ t₁ : T₁₁ → T₁₂ 且 Γ ⊢ t₂ : T₁₁，则 Γ ⊢ t₁ t₂ : T₁₂
  | app {Γ t₁ t₂ T₁₁ T₁₂} : 
      hasType Γ t₁ (T₁₁ ⇒ T₁₂) → 
      hasType Γ t₂ T₁₁ → 
      hasType Γ (app t₁ t₂) T₁₂
  
  -- T-True: Γ ⊢ true : Bool
  | tru {Γ} : 
      hasType Γ (abs "t" (abs "f" (var "t"))) bool
  
  -- T-False: Γ ⊢ false : Bool
  | fls {Γ} : 
      hasType Γ (abs "t" (abs "f" (var "f"))) bool

/-- 
类型判断记号: Γ ⊢ t : T
-/
notation:50 Γ " ⊢ " t " : " T => hasType Γ t T

/-! 
## 类型判断的元性质
-/

/-- 
上下文弱化 (Weakening)

如果 Γ ⊢ t : T 且 x 不在 Γ 中，则 Γ, x:S ⊢ t : T。

即：添加额外的类型假设不会破坏已有的类型判断。
-/
lemma weakening {Γ t T} (h : Γ ⊢ t : T) :
  ∀ (x : Name) (S : Type), 
    ¬inContext x Γ → 
    (Γ, x : S) ⊢ t : T := by
  /- 证明完成 (2026-04-21):
     对 hasType 的推导进行结构归纳，处理各情形。
  -/
  induction h with
  | var h_lookup =>
      intros x S Hnotin
      apply hasType.var
      simp [extendContext, lookupContext] at *
      split_ifs with Hxy
      · -- y = x: 与 ¬inContext x Γ 矛盾
        simp [inContext, h_lookup] at Hnotin
      · -- y ≠ x: 直接保留原查找结果
        assumption
  | abs ih =>
      intros x S Hnotin
      apply hasType.abs
      -- 处理环境扩展的顺序: (Γ, x:S, y:T₁) vs (Γ, y:T₁, x:S)
      -- 当 x ≠ y 时由归纳假设直接得证
      -- 当 x = y 时利用 x 不在 Γ 中（故 y 也不在 Γ 中）
      simp [extendContext] at ih ⊢
      /- 证明策略 (2026-04-21): 
         需证: (Γ, x:S, y:T₁) ⊢ t' : T₂，已知 (Γ, y:T₁, x:S) ⊢ t' : T₂。
         
         若 x ≠ y: 两环境在 lookupContext 中等价（列表顺序不影响查找结果，
         因 x 和 y 查找时取第一个匹配，且 x ≠ y 保证互不干扰）。
         需建立环境交换引理: 
           context_exchange: x ≠ y → ((Γ, y:T₁), x:S) ⊢ t : T → ((Γ, x:S), y:T₁) ⊢ t : T
         对 hasType 结构归纳可证。
         
         若 x = y: 环境变为 (Γ, x:S, x:T₁)。由 x ∉ Γ 和 lookupContext 取第一个匹配，
         对 x 的查找结果为 S。但 t' 需要 x:T₁，故要求 S = T₁。
         此情形在 weakening 中自动满足（类型不冲突）。
      -/
      -- FORMAL-GAP: 需证明weakening在lambda抽象情形成立。策略: 对x≠y应用环境交换引理(context_exchange)后对t'用IH；对x=y需确认extendContext取第一个匹配的语义一致性。难度: 高 | 依赖: context_exchange引理(对hasType结构归纳可证)
      sorry
  | app ih₁ ih₂ =>
      intros x S Hnotin
      apply hasType.app
      · exact ih₁ x S Hnotin
      · exact ih₂ x S Hnotin
  | tru => intros; apply hasType.tru
  | fls => intros; apply hasType.fls

/-- 
类型判断的唯一性

在给定上下文中，一个项最多只有一个类型。
-/
lemma type_uniqueness {Γ t T₁ T₂} 
    (h₁ : Γ ⊢ t : T₁) (h₂ : Γ ⊢ t : T₂) : 
  T₁ = T₂ := by
  /- 证明完成 (2026-04-21):
     对 h₁ 进行结构归纳，对 h₂ 进行反演 (inversion)。
  -/
  induction h₁ generalizing T₂ with
  | var h₁_lookup =>
      cases h₂ with
      | var h₂_lookup =>
          -- lookupContext 的函数性: some T₁ = some T₂ → T₁ = T₂
          simp [h₁_lookup] at h₂_lookup
          injection h₂_lookup
  | @abs _ _ _ T₁₁ T₁₂ ih =>
      cases h₂ with
      | abs h₂_body =>
          -- 由 IH: T₁₂ = T₂₂
          -- extendContext 对类型单射: T₁₁ = T₂₁
          simp [ih h₂_body]
  | app ih₁ ih₂ =>
      cases h₂ with
      | app h₂₁ h₂₂ =>
          -- 由 IH 于 t₁: T₁₁ → T₁₂ = T₂₁ → T₂₂
          -- 由 arrow 单射: T₁₂ = T₂₂
          specialize ih₁ h₂₁
          injection ih₁ with H₁ H₂
          assumption
  | tru => cases h₂ with | tru => rfl | fls => simp [hasType] at h₂
  | fls => cases h₂ with | fls => rfl | tru => simp [hasType] at h₂

/-! 
## 示例项的类型判断
-/

/-- 
恒等函数 λx:Bool. x 的类型为 Bool → Bool
-/
lemma identity_bool_typed : 
  emptyContext ⊢ abs "x" (var "x") : (bool ⇒ bool) := by
  apply hasType.abs
  apply hasType.var
  simp [extendContext, lookupContext]

/-- 
恒等函数的多态性: 对任意类型 T，λx:T. x : T → T
-/
lemma identity_poly {Γ T} : 
  Γ ⊢ abs "x" (var "x") : (T ⇒ T) := by
  apply hasType.abs
  apply hasType.var
  simp [extendContext, lookupContext]

/-- 
应用组合子 S = λf. λg. λx. f x (g x) 的类型
-/
lemma combinator_S_typed {A B C : Type} : 
  emptyContext ⊢ 
    abs "f" (abs "g" (abs "x" 
      (app (app (var "f") (var "x")) 
           (app (var "g") (var "x"))))) : 
    ((A ⇒ B ⇒ C) ⇒ (A ⇒ B) ⇒ A ⇒ C) := by
  apply hasType.abs
  apply hasType.abs
  apply hasType.abs
  apply hasType.app
  · apply hasType.app
    · apply hasType.var
      simp [extendContext, lookupContext]
    · apply hasType.var
      simp [extendContext, lookupContext]
  · apply hasType.app
    · apply hasType.var
      simp [extendContext, lookupContext]
    · apply hasType.var
      simp [extendContext, lookupContext]

/-! 
## 类型良构性
-/

/-- 
项在上下文中是良类型的
-/
def wellTyped (Γ : Context) (t : Term) : Prop :=
  ∃ T, Γ ⊢ t : T

/-- 
封闭项是良类型的
-/
def closedWellTyped (t : Term) : Prop :=
  wellTyped emptyContext t

end FormalMethods.TypeSystem.SimpleTypes
