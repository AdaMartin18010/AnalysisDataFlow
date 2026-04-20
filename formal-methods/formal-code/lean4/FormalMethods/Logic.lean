/-
Logic.lean - 逻辑基础

本文件定义命题逻辑和谓词逻辑的基本概念，
作为形式化方法的理论基础。

内容:
- 命题逻辑的语法和语义
- 自然演绎系统
- 命题的等价关系
- 基本的逻辑定律
- 谓词逻辑的完整形式化（见 Predicate.lean）

作者: AnalysisDataFlow Project
日期: 2026-04-10
-/

-- 导入谓词逻辑模块
import FormalMethods.Logic.Predicate
-- 导入模态逻辑模块
import FormalMethods.Logic.Modal

-- 导入高阶逻辑(HOL)模块
import FormalMethods.Logic.HOL

namespace FormalMethods.Logic

/-!
## 命题逻辑

定义命题逻辑的语法。
-/

/--
命题变量
-/
abbrev PropVar := String

/--
命题公式的归纳定义
-/
inductive PropFormula : Type where
  | var : PropVar → PropFormula           -- 原子命题 p
  | not_ : PropFormula → PropFormula      -- 否定 ¬A
  | and_ : PropFormula → PropFormula → PropFormula  -- 合取 A ∧ B
  | or_  : PropFormula → PropFormula → PropFormula  -- 析取 A ∨ B
  | imp_ : PropFormula → PropFormula → PropFormula  -- 蕴含 A → B
  | iff_ : PropFormula → PropFormula → PropFormula  -- 等价 A ↔ B
  | true_lit  : PropFormula               -- 真 ⊤
  | false_lit : PropFormula               -- 假 ⊥
  deriving Repr, BEq

open PropFormula

-- 记号定义
prefix:75 "¬ₚ" => not_
infixr:70 " ∧ₚ " => and_
infixr:65 " ∨ₚ " => or_
infixr:60 " →ₚ " => imp_
infix:55 " ↔ₚ " => iff_
notation "⊤ₚ" => true_lit
notation "⊥ₚ" => false_lit
notation:max "#" p => var p

/-!
## 真值赋值与语义

定义命题的真值语义。
-/

/--
真值赋值：变量到布尔值的映射
-/
def Assignment := PropVar → Bool

/--
命题公式的求值
-/
def eval (σ : Assignment) : PropFormula → Bool
  | var p => σ p
  | not_ A => !(eval σ A)
  | and_ A B => eval σ A && eval σ B
  | or_ A B => eval σ A || eval σ B
  | imp_ A B => !(eval σ A) || eval σ B
  | iff_ A B => eval σ A == eval σ B
  | true_lit => true
  | false_lit => false

/--
命题的有效性

一个命题是有效的，如果它在所有赋值下为真。
-/
def valid (A : PropFormula) : Prop :=
  ∀ σ, eval σ A = true

/--
命题的可满足性

一个命题是可满足的，如果存在某个赋值使其为真。
-/
def satisfiable (A : PropFormula) : Prop :=
  ∃ σ, eval σ A = true

/--
逻辑后承

Γ ⊨ A 表示 A 是 Γ 的逻辑后承。
-/
def entails (Γ : List PropFormula) (A : PropFormula) : Prop :=
  ∀ σ, (∀ B ∈ Γ, eval σ B = true) → eval σ A = true

notation:50 Γ " ⊨ " A => entails Γ A

/-!
## 自然演绎系统

命题逻辑的自然演绎推理规则。
-/

/--
证明上下文 - 使用列表存储假设
-/
abbrev ProofContext := List PropFormula

/--
成员关系实例
-/
instance : Membership PropFormula ProofContext where
  mem := List.Mem

/--
可证明性关系

Γ ⊢ A 表示从假设 Γ 可以证明 A。
-/
inductive proves : ProofContext → PropFormula → Prop where
  -- 假设规则
  | assumption {Γ A} :
      A ∈ Γ → proves Γ A

  -- 合取引入 (∧I)
  | and_intro {Γ A B} :
      proves Γ A → proves Γ B → proves Γ (A ∧ₚ B)

  -- 合取消除左 (∧E₁)
  | and_elim_left {Γ A B} :
      proves Γ (A ∧ₚ B) → proves Γ A

  -- 合取消除右 (∧E₂)
  | and_elim_right {Γ A B} :
      proves Γ (A ∧ₚ B) → proves Γ B

  -- 蕴含引入 (→I)
  | imp_intro {Γ A B} :
      proves (A :: Γ) B → proves Γ (A →ₚ B)

  -- 蕴含消除/假言推理 (→E)
  | imp_elim {Γ A B} :
      proves Γ (A →ₚ B) → proves Γ A → proves Γ B

  -- 析取引入左 (∨I₁)
  | or_intro_left {Γ A B} :
      proves Γ A → proves Γ (A ∨ₚ B)

  -- 析取引入右 (∨I₂)
  | or_intro_right {Γ A B} :
      proves Γ B → proves Γ (A ∨ₚ B)

  -- 析取消除 (∨E)
  | or_elim {Γ A B C} :
      proves Γ (A ∨ₚ B) →
      proves (A :: Γ) C →
      proves (B :: Γ) C →
      proves Γ C

  -- 否定引入 (¬I)
  | not_intro {Γ A} :
      proves (A :: Γ) ⊥ₚ → proves Γ (¬ₚ A)

  -- 否定消除/矛盾 (¬E)
  | not_elim {Γ A} :
      proves Γ A → proves Γ (¬ₚ A) → proves Γ ⊥ₚ

  -- 假消除/爆炸原理 (⊥E)
  | false_elim {Γ A} :
      proves Γ ⊥ₚ → proves Γ A

  -- 真引入 (⊤I)
  | true_intro {Γ} :
      proves Γ ⊤ₚ

notation:50 Γ " ⊢ " A => proves Γ A

/-!
## 基本逻辑定律
-/

/--
排中律: A ∨ ¬A
-/
def LEM (A : PropFormula) : PropFormula :=
  A ∨ₚ (¬ₚ A)

/--
双重否定消去: ¬¬A → A
-/
def DNE (A : PropFormula) : PropFormula :=
  (¬ₚ (¬ₚ A)) →ₚ A

/-!
## 可靠性 (Soundness)

自然演绎系统是可靠的：可证明的公式是有效的。
-/

/--
可靠性定理

如果 Γ ⊢ A，则 Γ ⊨ A。
-/
lemma soundness {Γ A} (h : Γ ⊢ A) : Γ ⊨ A := by
  /- Soundness Theorem: 自然演绎系统的可靠性定理。
     证明策略: 对证明推导 Γ ⊢ A 进行结构归纳。
     对每条推理规则，证明如果所有前提在赋值 σ 下为真，
     则结论在 σ 下也为真。 -/
  induction h with
  | assumption hmem =>
    intros σ hΓ
    exact hΓ A hmem
  | and_intro hA hB ihA ihB =>
    intros σ hΓ
    simp [eval]
    constructor
    · exact ihA σ hΓ
    · exact ihB σ hΓ
  | and_elim_left hAB ih =>
    intros σ hΓ
    have h := ih σ hΓ
    simp [eval] at h ⊢
    exact h.1
  | and_elim_right hAB ih =>
    intros σ hΓ
    have h := ih σ hΓ
    simp [eval] at h ⊢
    exact h.2
  | imp_intro hAB ih =>
    intros σ hΓ
    simp [eval]
    intros hA
    apply ih
    intros B hB
    cases hB with
    | head => exact hA
    | tail hB' => apply hΓ; exact hB'
  | imp_elim hAB hA ihAB ihA =>
    intros σ hΓ
    have h1 := ihAB σ hΓ
    have h2 := ihA σ hΓ
    simp [eval] at h1 h2 ⊢
    simp [h2] at h1
    exact h1
  | or_intro_left hA ih =>
    intros σ hΓ
    have h := ih σ hΓ
    simp [eval]
    exact Or.inl h
  | or_intro_right hB ih =>
    intros σ hΓ
    have h := ih σ hΓ
    simp [eval]
    exact Or.inr h
  | or_elim hAB hAC hBC ihAB ihAC ihBC =>
    intros σ hΓ
    have h1 := ihAB σ hΓ
    simp [eval] at h1 ⊢
    cases h1 with
    | inl hA =>
      apply ihAC
      intros C hC
      cases hC with
      | head => exact hA
      | tail hC' => apply hΓ; exact hC'
    | inr hB =>
      apply ihBC
      intros C hC
      cases hC with
      | head => exact hB
      | tail hC' => apply hΓ; exact hC'
  | not_intro hA ih =>
    intros σ hΓ
    simp [eval]
    intros hA'
    apply ih
    intros B hB
    cases hB with
    | head => exact hA'
    | tail hB' => apply hΓ; exact hB'
  | not_elim hA hNA ihA ihNA =>
    intros σ hΓ
    have h1 := ihA σ hΓ
    have h2 := ihNA σ hΓ
    simp [eval] at h1 h2 ⊢
    contradiction
  | false_elim hF ih =>
    intros σ hΓ
    have h := ih σ hΓ
    simp [eval] at h
  | true_intro =>
    intros σ hΓ
    simp [eval]

/-!
## 谓词逻辑（一阶逻辑）基础

简单的一阶谓词逻辑语法。
-/

/--
项（用于谓词逻辑）
-/
inductive TermFOL : Type where
  | var : String → TermFOL       -- 变量
  | const : String → TermFOL     -- 常量
  | func : String → List TermFOL → TermFOL  -- 函数应用
  deriving Repr

/--
一阶公式
-/
inductive FOLFormula : Type where
  | pred : String → List TermFOL → FOLFormula  -- 谓词应用
  | not_ : FOLFormula → FOLFormula
  | and_ : FOLFormula → FOLFormula → FOLFormula
  | or_  : FOLFormula → FOLFormula → FOLFormula
  | imp_ : FOLFormula → FOLFormula → FOLFormula
  | forall_ : String → FOLFormula → FOLFormula   -- 全称量词
  | exists_ : String → FOLFormula → FOLFormula   -- 存在量词
  deriving Repr

end FormalMethods.Logic
