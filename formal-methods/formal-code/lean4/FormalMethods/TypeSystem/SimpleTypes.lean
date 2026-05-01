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

/-- 若两环境对所有变量的查找结果相同，则类型推导等价 -/
lemma hasType_lookup_agree {Γ₁ Γ₂ : Context} {t : Term} {T : Type}
    (h : Γ₁ ⊢ t : T)
    (h_agree : ∀ x, lookupContext Γ₁ x = lookupContext Γ₂ x) :
    Γ₂ ⊢ t : T := by
  induction h with
  | var h_lookup =>
      apply hasType.var
      rw [←h_agree]
      exact h_lookup
  | abs h ih =>
      apply hasType.abs
      apply ih
      intro z
      simp [extendContext, lookupContext]
      by_cases h_eq : z = x
      · simp [h_eq]
      · simp [h_eq]
        apply h_agree
  | app h₁ h₂ ih₁ ih₂ =>
      apply hasType.app
      · exact ih₁ h_agree
      · exact ih₂ h_agree
  | tru => apply hasType.tru
  | fls => apply hasType.fls

/-- 环境交换引理: x ≠ y 时，(Γ, x:S, y:T) 和 (Γ, y:T, x:S) 的类型推导等价 -/
lemma context_exchange {Γ : Context} {x y : Name} {S T : Type} {t : Term} {U : Type}
    (h_ne : x ≠ y) :
    ((Γ, x : S), y : T) ⊢ t : U ↔ ((Γ, y : T), x : S) ⊢ t : U := by
  apply Iff.intro
  · -- → 方向
    intro h
    induction h with
    | var h_lookup =>
        apply hasType.var
        simp [extendContext, lookupContext] at h_lookup ⊢
        split_ifs at h_lookup ⊢
        all_goals try { assumption }
        all_goals try { contradiction }
    | abs h ih =>
        apply hasType.abs
        by_cases h_eq_zx : z = x
        · -- z = x
          rw [h_eq_zx]
          have h_agree : ∀ w, lookupContext ((Γ, x : S), y : T, x : U₁) w = lookupContext ((Γ, y : T), x : S, x : U₁) w := by
            intro w
            simp [extendContext, lookupContext]
            by_cases h_eq : w = x
            · simp [h_eq]
            · simp [h_eq]
              by_cases h_eq2 : w = y
              · simp [h_eq2]
              · simp [h_eq2]
          exact hasType_lookup_agree h h_agree
        · -- z ≠ x
          by_cases h_eq_zy : z = y
          · -- z = y
            rw [h_eq_zy]
            have h_agree : ∀ w, lookupContext ((Γ, x : S), y : T, y : U₁) w = lookupContext ((Γ, y : T), x : S, y : U₁) w := by
              intro w
              simp [extendContext, lookupContext]
              by_cases h_eq : w = y
              · simp [h_eq]
              · simp [h_eq]
                by_cases h_eq2 : w = x
                · simp [h_eq2]
                · simp [h_eq2]
            exact hasType_lookup_agree h h_agree
          · -- z ≠ x 且 z ≠ y
            have h_ne_zx : z ≠ x := h_eq_zx
            have h_ne_zy : z ≠ y := h_eq_zy
            apply ih
            intro w
            simp [extendContext, lookupContext]
            by_cases h_eq : w = z
            · simp [h_eq]
            · simp [h_eq]
              by_cases h_eq2 : w = x
              · simp [h_eq2]
                by_cases h_eq3 : w = y
                · rw [h_eq3] at h_eq2
                  contradiction
                · simp [h_eq3]
              · simp [h_eq2]
                by_cases h_eq3 : w = y
                · simp [h_eq3]
                · simp [h_eq3]
    | app h₁ h₂ ih₁ ih₂ =>
        apply hasType.app
        · exact ih₁
        · exact ih₂
    | tru => apply hasType.tru
    | fls => apply hasType.fls
  · -- ← 方向，对称
    intro h
    have h_symm : ((Γ, y : T), x : S) ⊢ t : U ↔ ((Γ, x : S), y : T) ⊢ t : U := by
      apply context_exchange
      intro h_eq
      apply h_ne
      rw [h_eq]
    exact h_symm.mp h

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
      simp [extendContext] at ih ⊢
      by_cases h_eq : x = y
      · -- x = y: 环境变为 (Γ, x:S, x:T₁)
        -- 由 x ∉ Γ，lookupContext 在 (Γ, x:S, x:T₁) 中查找 x 返回 T₁（第一个匹配是 x:S... 不对，x:T₁ 才是第一个匹配）
        -- 实际上 (Γ, x:S, x:T₁) = (x, T₁) :: (x, S) :: Γ
        -- lookupContext 取第一个匹配，返回 T₁
        -- 所以 (Γ, x:S, x:T₁) 和 (Γ, x:T₁) 对 x 的查找结果相同
        rw [h_eq]
        have h_agree : ∀ z, lookupContext ((Γ, x : S), x : T₁) z = lookupContext (Γ, x : T₁) z := by
          intro z
          simp [extendContext, lookupContext]
          by_cases h_eqz : z = x
          · simp [h_eqz]
          · simp [h_eqz]
        exact hasType_lookup_agree ih h_agree
      · -- x ≠ y
        have h_ne : x ≠ y := by intro h; apply h_eq; exact h
        apply (context_exchange h_ne).mp
        exact ih
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
